#!/usr/bin/env python3

import sys
import os
import numpy as np
import pandas as pd

f = sys.argv[1]

m = {}

counts = []

for root, dirs, files in os.walk(f):
    for f in files:
        if f.endswith(".summary"):
            fn = os.path.join(root, f)
            counts.append(fn)

for f in counts:
    with open(fn) as hanler:
        df = pd.read_csv(fn, sep = "\t")
        print(df.iloc[0])
    break
