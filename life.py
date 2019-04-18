# -*- encoding: utf-8 -*-

class Life():
    '''一个基因序列，即一种巡回路径'''
    def __init__(self,agene=None):
        self.gene=agene #序列gene
        self.score= -1 #初始适应度值