# -*- coding: utf-8 -*-
import random
from life import Life

class ga(object):
    def __init__(self,StartCity,gene,PCross,PMutation,GeneLength,LifeCount,MatchFun= lambda life: 1):
        self.StartCity=StartCity
        self.gene=gene
        self.PCross=PCross  #杂交概率
        self.PMutation=PMutation #突变概率
        self.GeneLength=GeneLength #基因长度，即经过的城市数
        self.LifeCount=LifeCount #当代种群数
        self.MatchFun=MatchFun #适配函数

        self.lives=[] #当代种群
        self.best=None #当代最优个体
        self.generation=1 #当前代数
        self.crosscount=0 #杂交次数
        self.mutationcount=0 #突变次数

        self.scoresum=0.0 #适配数之和，用于轮盘赌筛选

        self.initPopulation() #初始化种群

    def initPopulation(self):
        self.lives=[]#当代种群
        for i in range(self.LifeCount):
            gene=self.gene
            random.shuffle(gene) #产生LifeCount个随机gene序列
            for i in range(self.GeneLength):
                if gene[i] == self.StartCity:
                    gene[0], gene[i] = gene[i], gene[0]


            life=Life(gene)
            self.lives.append(life)

    def judge(self):
        self.scoresum=0.0
        self.best=self.lives[0]

        for life in self.lives:
            life.score=self.MatchFun(life)
            self.scoresum+=life.score

            if self.best.score < life.score:
                self.best = life

    def cross(self, parent1, parent2):
        '''杂交'''
        index1 = random.randint(1, self.GeneLength - 1)
        index2 = random.randint(index1, self.GeneLength - 1)
        tempGene = parent2.gene[index1:index2]  # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        self.crosscount += 1
        return newGene

    def mutation(self,gene):
        '''交换两基因位置以突变'''
        index1=random.randint(1,self.GeneLength-1)
        index2=random.randint(index1,self.GeneLength-1)
        newGene=gene[:]
        newGene[index1],newGene[index2]=newGene[index2],newGene[index1]
        self.mutationcount += 1
        return newGene

    def getOne(self):
        """选择一个个体"""
        r = random.uniform(0, self.scoresum)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life

        raise Exception("选择错误", self.scoresum)

    def newChild(self):
        """产生新后代"""
        parent1 = self.getOne()
        rate = random.random()

        # 按概率交叉
        if rate < self.PCross:
            # 交叉
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene

        # 按概率突变
        rate = random.random()
        if rate < self.PMutation:
            gene = self.mutation(gene)

        return Life(gene)

    def next(self):
        """产生下一代"""
        self.judge()
        newLives = []
        newLives.append(self.best)  # 把最好的个体加入下一代
        while len(newLives) < self.LifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1



