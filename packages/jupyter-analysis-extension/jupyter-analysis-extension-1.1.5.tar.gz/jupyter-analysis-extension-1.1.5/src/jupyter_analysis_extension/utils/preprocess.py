import numpy as np


def preprocess_values(df):
    # Preprocess the data for inf or nan values
    # Draft ver: only remove the rows
    # TODO.
    # Should be changed to user can choose the methods.

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    return df
