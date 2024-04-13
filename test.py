#!/usr/bin/python3
import numpy as np

evaluates = {}
evaluates = np.load('evaluate.npy', allow_pickle=True).item()

import pandas as pd
pd.set_option('display.max_rows', None)

table = pd.DataFrame(evaluates.items())
print(table)