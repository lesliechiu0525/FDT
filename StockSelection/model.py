# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 20:39
# @Author  : Shark
# @Site    : 
# @File    : model.py
# @Software: PyCharm
import torch
from torch import nn
'''MLP Simple'''
class MLP(nn.Module):
    def __init__(self,input_size):
        super(MLP,self).__init__()
        self.input_size = input_size
        self.layers = nn.ModuleList([nn.Linear(input_size,input_size) for i in range(5)])
        self.activation = nn.ReLU()
    def forward(self,x):
        for layer in self.layers:
            x = layer(x)
            x = self.activation(x)
        return x

'''TO DO LIST'''
class LSTM:
    pass

'''test'''
if __name__ == '__main__':
    x = torch.randn((1000,10))
    model = MLP(input_size=10)
    print(model(x))