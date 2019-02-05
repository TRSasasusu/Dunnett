# coding: utf-8

import os
import sys
from typing import Tuple
import numpy as np
import pandas as pd
import pyper

FLUSH_BUFFERS_RANGE = 10 

def get_df() -> pd.DataFrame:
    if get_split_filename()[1] == '.csv':
        return pd.read_csv(sys.argv[1], header=None)
    return pd.read_excel(sys.argv[1], header=None)

def get_r() -> pyper.R:
    return pyper.R(use_pandas='True')

def flush_buffer():
    """In Windows, library() makes some buffers which should be flushed to display your results."""
    for i in range(FLUSH_BUFFERS_RANGE):
        r('1')

def get_split_filename() -> Tuple[str, str]:
    return os.path.splitext(sys.argv[1])

def remove_nan(x) -> np.ndarray:
    return x[~np.isnan(x)]
