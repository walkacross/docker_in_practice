#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:01:26 2019

@author: allen
"""
import numpy as np
import pandas as pd

def print_df():
    print("task begin")
    for i in range(10):
        print(pd.DataFrame(np.random.randn(2,3)))
    print("task done")

if __name__ == "__main__":
    print_df()