import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error as mae
from sklearn.model_selection import train_test_split

import time

from .columns import targets, time_columns, label_encoders, error_codes, groups, exclude, predictors
from .preprocessing import time2num, encode, process_error_codes, load_columns, load_targets
from .important_features import get_important_features

sns.set()


class MechModel:
    def __init__(self, targets, is_features_invoked=False):
        self.targets = targets
        self.pca = {}
        self.performance = {key: {} for key in self.targets}
        self.features = []
        self.models = {}
        self.tsne_images = {}
        self.is_features_invoked = is_features_invoked

    def preprocess_columns(self, df, reduced_group_dim):

        not_startswith = ['ДУО_ПРОХ', 'ДУО_ХОЛОСТ', 'ДУО_Т_3_ПР', 'ДУО_Т_ПОСЛ',
                          'КВР_Т_ПЛАН', 'КВР_Т_1_ПР', 'КВР_Т_ПОСЛ', 'КВР_ПРОХ',
                          'КВР_ХОЛОСТ', 'ДУО_ВРЕМЯ', 'ДУО_КВР', 'КВР_ВРЕМЯ']

        data = pd.DataFrame()
        Y = pd.DataFrame()

        time2num(df, time_columns)
        encode(df, data, label_encoders)
        process_error_codes(df, data, error_codes)

        # an array with КВР, ДУО и DELTA columns for correct PCA compression
        kvr_duo_delta_columns = []
        if self.is_features_invoked:
            kvr_duo_delta_columns = [col for col in self.features
                                    if ((col.startswith('КВР') or col.startswith('ДУО') or col.startswith('DELTA'))
                                    and not (col in not_startswith))]
        else:
            kvr_duo_delta_columns = df.columns

        load_columns(df, data, groups, kvr_duo_delta_columns, reduced_group_dim, self.pca)

        if data.shape[0] == 0:
            raise ValueError('0 rows in dataset after filtering')

        load_targets(df, Y, {target:targets[target] for target in self.targets})

        return data, Y

    # a function to replace string elements in list
    def _list_replace(self, lst: list[str], to_replace: str, value: str):
        for i, element in enumerate(lst):
            if element == to_replace:
                lst[i] = value[:-2]+'01'
        return lst

    def to_features(self, data, y, target):
        prefixes_to_replace = [
            'ДУО_ОБЖ', 'ДУО_УСС', 'ДУО_УСП', 'ДУО_СКР',
            'КВР_ОБЖ', 'КВР_УСС', 'КВР_УСП', 'КВР_СКР',
            'DELTA'
        ]

        features_temp = self.features.copy()
        for prefix in prefixes_to_replace:
            columns_with_prefix = [col for col in features_temp
                                   if col.startswith(prefix)]
            for column in columns_with_prefix:
                features_temp = self._list_replace(features_temp, column,
                                                   f'Group_{columns_with_prefix[0]}')
            features_temp = list(set(features_temp))
        features_temp = list(set(features_temp)&set(predictors))

        features_temp = list(set(features_temp)-set(exclude[target]))
        fts = data.drop(exclude[target], axis=1, errors='ignore')
        return fts[features_temp]

    def fit(self, df, features):
        # 0.
        if features:
            self.features = features
            self.is_features_invoked = True
        else:
            self.is_features_invoked = False

        # 1. drop
        filtered = set(df[df['NOMP'].str.contains('П')].index) | set(df[df['NOMP'].str.contains('У')].index) | set(df[df['NOMP'].str.startswith('9')].index)
        df.drop(index=list(filtered), inplace=True)

        # 2. preprocess columns - return all possible columns
        data, Y = self.preprocess_columns(df, reduced_group_dim=1)

        # 3. for each target get important features
        if not self.is_features_invoked:
            temp = set()
            for target in self.targets:
                fts = data.drop(exclude[target], axis=1, errors='ignore')

                start_time = time.time()
                important_columns = get_important_features(fts, Y[target])
                print("--- Getting important features for %s: %s seconds ---" % (target, (time.time() - start_time)))

                if len(important_columns)==0:
                    raise ValueError('0 allowed predictors chosen')

                temp.update(important_columns)
            self.features = list(temp)

        print('Before fitting: ', self.features)

        # 5. fit models for each target
        for target in self.targets:
            X = self.to_features(data, Y[target], target)
            print('Fitting ', target, ', predictors: ', X.columns)
            start_time = time.time()
            self.fit_model(X, Y[target], target)
            print("--- Fitting model for %s: %s seconds ---" % (target, (time.time() - start_time)))

        return 0

    def fit_model(self, X, y, target):
        print('fitting ', target)
        X, y = X.values, y.values

        # 1. drop nan
        sl = ~np.logical_or(np.isnan(X).any(axis=1), np.isnan(y))
        X, y = X[sl], y[sl]

        if X.shape[0]==0:
            raise ValueError('0 samples without NaN for fitting')
        # 2. filter out
        X_embedded = TSNE(
            n_components=2, learning_rate=200, init='random'
            ).fit_transform(X)
        # save image
        self.save_image(X_embedded, y, target)

        clustering = DBSCAN(eps=10, min_samples=5).fit(np.hstack((X_embedded, y.reshape(-1,1))))
        normal = clustering.labels_ != -1
        X, y = X[normal], y[normal]

        if X.shape[0]==0:
            raise ValueError('0 samples after outliers filtering')
        self.performance[target]['Samples'] = X.shape[0]
        print(X.shape[0])

        # 3. Set up model
        model = RandomForestRegressor(n_estimators=60)
        # 4. Calc performance
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        # 5. Train model
        model.fit(X, y)
        self.models[target] = model

        y_pred = model.predict(X)
        self.performance[target]['MAE'] = np.round(mae(y, y_pred), 2)
        self.performance[target]['P95'] = np.round(np.percentile(np.abs(y-y_pred), 95), 2)
        self.performance[target]['MAE train'] = np.round(mae(y_train, y_pred_train), 2)
        self.performance[target]['MAE test'] = np.round(mae(y_test, y_pred_test), 2)

        return 0

    def save_image(self, X, y, target):
        si = np.argsort(y)
        fig, ax = plt.subplots(1, figsize=(10,10))
        sns.scatterplot(x=X[si, 0], y=X[si, 1], hue=y[si],
                        legend=True,
                        s=50, alpha=0.8,
                        palette='icefire', linewidth=0.3, edgecolor='k')
        #sns.set(rc={'figure.figsize':(30,30)})

        plt.title(target, weight='bold').set_fontsize('14')
        plt.xlabel('Component 1', weight='bold').set_fontsize('14')
        plt.ylabel('Component 2', weight='bold').set_fontsize('14')

        # plt.show()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        self.tsne_images[target] = buf
        return

    def predict(self, df):
        data, _ = self.preprocess_columns(df, reduced_group_dim=1)
        # print(data)
        Y = ()
        for target in self.targets:
            X = data[self.features].values
            sl = np.isnan(X).any(axis=1)
            X = np.nan_to_num(X)

            y = self.models[target].predict(X)
            y[sl] = np.nan
            Y += (y,)

        Y = np.vstack(Y).T
        # print(Y)
        return pd.DataFrame(data=Y, columns=self.targets)

        # return pd.DataFrame(index=df.index, columns=self.targets).fillna(0)


if __name__ == "__main__":
    model = MechModel(['FPT', 'FVS'])
    df = pd.read_csv('D:/work/17Г1С-У.csv')
    fts = [
          'H_СЛЯБ',  # 1
          'B_СЛЯБ',  # 1
          'L_СЛЯБ',
          'ВЕС_СЛ',  # 4
          'ВЕСФ_СЛ',  # 9
          'H_ЛИСТ',  # 5
          'B_ЛИСТ',  # 9
          'L_ЛИСТ',  # 3
          ]
    print(df.head(5))
    print(model.features)

    model.fit(df)
    print(model.features)
    print(model.performance)
