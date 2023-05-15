# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 20:39
# @Author  : Shark
# @Site    : 
# @File    : backtest.py
# @Software: PyCharm
from model import MLP
class BackTest:
    def __init__(self):
        self.model = None
        self.data = None
        self.dictionary = {
            'MLP':MLP
        }
        pass
    '''set variable'''
    def set(self,data,factor_name,model_type,limit):
        self.data = data
        self.model = self.dictionary[model_type]
        pass
    '''to get backtest res'''
    def run(self):
        pass