# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 20:39
# @Author  : Shark
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import pandas as pd
from backtest import BackTest
'''test'''
if __name__ == '__main__':
    df = pd.read_csv('data.csv')
    param = {
        'data' : df,
        'factor_name':['vol'],
        'model_type':'MLP',
        'limit':True
    }
    backtrader = BackTest()
    backtrader.set(**param)
    res = backtrader.run()