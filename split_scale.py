import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

def split_my_data(df, train_pct):
    '''
    Takes in df, train_pct and returns 2 items:
    train, test

    When using this function, in order to have usable datasets, be sure to call it thusly:
    train, test = split_my_data(df, train_pct)
    '''
    return train_test_split(df, train_size = train_pct, random_state = 294)

def iqr_robust_scaler(train, test):
    '''
    Uses the train & test datasets created by the split_my_data function
    Returns 3 items: iqr_scaler, train_scaled_iqr, test_scaled_iqr

    Used for data with outliers. Median is removed, and data is scaled to the IQR
    '''
    iqr_scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(train)
    train_scaled_iqr = pd.DataFrame(iqr_scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled_iqr = pd.DataFrame(iqr_scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return iqr_scaler, train_scaled_iqr, test_scaled_iqr


