
import pandas as pd
import numpy as np 
from insar.ts_utils import build_A_matrix
from apertools import utils, plotting
slc_list = pd.date_range(start=datetime.date(2020, 1, 1), end=datetime.date(2020,1, 5), freq='1D').date.tolist()