from datetime import time
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


def encode(df, output_df, label_encoders):
    for column in label_encoders:  # for each column where label encoding is necessary

        for i, label in enumerate(label_encoders[column]):  # for each label in column
            df.loc[df[column]==label, column] = i
        x = df[column]
        x = x.fillna(i+1)
        output_df[column] = x
    return


def process_error_codes(df, output_df, code_columns):
    for column in code_columns:
        output_df[column] = df[column].fillna(0)
    return


def reduce_dim(df, columns, dim, pca):
    X = df[columns]
    X = X.fillna(0)

    group_key = ','.join(columns)
    if group_key not in pca:
        pca[group_key] = PCA(n_components=dim)
        pca[group_key].fit(X)

    X = pca[group_key].transform(X)
    return X


def load_columns(df, output_df, groups, kvr_duo_delta_columns, dim, pca):
    group_id = 0
    for columns in groups:
        if isinstance(columns, list): # convolve
            columns_in_df = list(set(columns) & set(kvr_duo_delta_columns))
            if not columns_in_df:
                continue
            output_df[f'Group_{columns[0]}'] = reduce_dim(df, columns, dim, pca)
            group_id+=1
        else:
            output_df[columns] = df[columns]
    return


def load_targets(df, Y, targets):
    for y in targets:
        Y[y] = df[targets[y]].mean(axis=1)
    return

# TO DO: to change when Filters_date is added
def time2num(df, columns):
    df[columns] = df[columns].astype(str)
    for column in columns:
        df[column] = df[column].apply(lambda x: np.dot(np.array(x.split(':'), dtype=float), np.array([1.0, 1.0/60, 1.0])))
    return
