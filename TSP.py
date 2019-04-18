# -*- encoding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import random
import math
import sys
from geopy.distance import geodesic


from ga import ga

window = tk.Tk()
window.title=("TSP")
window.geometry('1600x1600')
canvas=tk.Canvas(window,bg="white",height='600',width="700")
img_open=Image.open('map.jpg')
img_jpg=ImageTk.PhotoImage(img_open)
canvas.create_image(0,0,anchor='nw',image=img_jpg)
canvas.pack()

class TSP_WIN(object):
    def __init__(self):
        self.window=window
        self.citys = [['西安',108.95,34.27],['北京',116.46,39.92],
                       ['南京',118.78,32.04],['广州',113.23,23.16],
                       ['成都',104.06,30.67],['武汉',114.31,30.52],
                       ['兰州',103.73,36.03],['昆明',102.73,25.04],
                       ['拉萨',91.11,29.97],['上海',121.48,31.22]]
        self.position=[[414,299],[474,192],[522,306],[500,455],[324,346],
                       [474,358],[353,280],[317,442],[154,341],[555,326]]
        self.var0 = tk.IntVar()
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()
        self.var4 = tk.IntVar()
        self.var5 = tk.IntVar()
        self.var6 = tk.IntVar()
        self.var7 = tk.IntVar()
        self.var8 = tk.IntVar()
        self.var9 = tk.IntVar()
        self.cmbChosen = ttk.Combobox(window)
        self.ltt = tk.Text(window, width=50, height=20)
        self.ltt.place(x=1150, y=200)
        self.button= tk.Button(window, text='选择完毕后请确定',command=self.Ok_command).place(x=150,y=500)
        self.createCombobox()
        self.createCheckbutton()
         #这里设置文本框高，可以容纳两行



        self.citys2=[]

    def createCombobox(self):
        l1=tk.Label(window,text="请选择起始城市",bg='white',font=('Arial',12),width=15,height=2).place(x=50,y=50)


        self.cmbChosen['values'] = ('西安','北京','南京','广州','成都','武汉','兰州','昆明','拉萨','上海')
        self.cmbChosen.current(0)
        self.cmbChosen.place(x=250,y=60)

    def createCheckbutton(self):
        l2=tk.Label(window,text="除起点外要经过的城市",bg='white',font=('Arial',12),width=20,height=2).place(x=50,y=200)




        c1=tk.Checkbutton(window,text="西安",variable=self.var0,onvalue=1,offvalue=0).place(x=250,y=210)
        c2=tk.Checkbutton(window,text="北京",variable=self.var1,onvalue=1,offvalue=0).place(x=250,y=230)
        c3=tk.Checkbutton(window,text="南京",variable=self.var2,onvalue=1,offvalue=0).place(x=250,y=250)
        c4=tk.Checkbutton(window,text="广州",variable=self.var3,onvalue=1,offvalue=0).place(x=250,y=270)
        c5=tk.Checkbutton(window,text="成都",variable=self.var4,onvalue=1,offvalue=0).place(x=250,y=290)
        c6=tk.Checkbutton(window,text="武汉",variable=self.var5,onvalue=1,offvalue=0).place(x=250,y=310)
        c7=tk.Checkbutton(window,text="兰州",variable=self.var6,onvalue=1,offvalue=0).place(x=250,y=330)
        c8=tk.Checkbutton(window,text="昆明",variable=self.var7,onvalue=1,offvalue=0).place(x=250,y=350)
        c9=tk.Checkbutton(window,text="拉萨",variable=self.var8,onvalue=1,offvalue=0).place(x=250,y=370)
        c10=tk.Checkbutton(window,text="上海",variable=self.var9,onvalue=1,offvalue=0).place(x=250,y=390)


    def initCitys(self):
        self.citys2=[]
        val = self.cmbChosen.get()

        for i in range(10):
                if str(val)== str(self.citys[i][0]):
                    self.citys2.append(self.citys[i])
        if self.var0.get()==1:
            self.citys2.append(self.citys[0])
        if self.var1.get()==1:
            self.citys2.append(self.citys[1])
        if self.var2.get()==1:
            self.citys2.append(self.citys[2])
        if self.var3.get()==1:
            self.citys2.append(self.citys[3])
        if self.var4.get()==1:
            self.citys2.append(self.citys[4])
        if self.var5.get()==1:
            self.citys2.append(self.citys[5])
        if self.var6.get()==1:
            self.citys2.append(self.citys[6])
        if self.var7.get()==1:
            self.citys2.append(self.citys[7])
        if self.var8.get()==1:
            self.citys2.append(self.citys[8])
        if self.var9.get()==1:
            self.citys2.append(self.citys[9])

    def get_CityOrder(self):
        self.CityOrder=[]
        for i in range(len(self.citys2)):
            for j in range(len(self.citys)):
                if self.citys2[i]==self.citys[j]:
                    self.CityOrder.append(j)

    def line(self):
        canvas.delete("line")
        for i in range(len(self.ga.best.gene) - 1):
            p1 = self.position[self.ga.best.gene[i]]
            p2 = self.position[self.ga.best.gene[i+1]]
            canvas.create_line(p1, p2, fill="#ff0000", tags="line",width=3)
        canvas.create_line(self.position[self.ga.best.gene[-1]], self.position[self.ga.best.gene[0]], fill="#ff0000", tags="line", width=3)

    def Ok_command(self):
        self.initCitys()
        self.get_CityOrder()
        self.ga = ga(StartCity=self.CityOrder[0],gene=self.CityOrder,PCross=0.8,
                                     PMutation=0.02,
                                     LifeCount=100,
                                     GeneLength=len(self.CityOrder),
                                     MatchFun=self.matchFun())
        n=100
        while n > 1:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
            n -= 1



        self.ltt.insert(tk.INSERT,'最佳路径为：\n')
        for i in range(len(self.ga.best.gene)-1):

            self.ltt.insert(tk.INSERT,self.citys[self.ga.best.gene[i]][0]+'-------->'+self.citys[self.ga.best.gene[i+1]][0]
                            +'    '+str(geodesic((self.citys[self.ga.best.gene[i]][2],self.citys[self.ga.best.gene[i]][1]),(self.citys[self.ga.best.gene[i+1]][2],self.citys[self.ga.best.gene[i+1]][1])
                                                 ))+'\n')
        self.ltt.insert(tk.INSERT,
            self.citys[self.ga.best.gene[-1]][0] + '-------->' + self.citys[self.ga.best.gene[0]][0]
            + '    ' + str(
            geodesic((self.citys[self.ga.best.gene[-1]][2], self.citys[self.ga.best.gene[-1]][1]), (
            self.citys[self.ga.best.gene[0]][2], self.citys[self.ga.best.gene[0]][1])
                            )) + '\n')
        self.ltt.insert(tk.INSERT, '路程共计为：\n'+str(self.distance(self.CityOrder)))

        self.line()

    def distance(self, order):
        distance = 0.0
            #i从-1到32,-1是倒数第一个
        for i in range(len(self.CityOrder)-1):
                citya, cityb = self.citys[self.CityOrder[i]], self.citys[self.CityOrder[i+1]]
                distance += geodesic((citya[2],citya[1]),(cityb[2],cityb[1])).km

        distance+=geodesic((self.citys[self.CityOrder[-1]][2],self.citys[self.CityOrder[-1]][1]),(self.citys[self.CityOrder[0]][2],self.citys[self.CityOrder[0]][1])).km

        return distance

    # 适应度函数，因为我们要从种群中挑选距离最短的，作为最优解，所以（1/距离）最长的就是我们要求的
    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)





    def mainloop(self):
        self.window.mainloop()
def main():


            tsp = TSP_WIN()

            tsp.mainloop()


if __name__ == '__main__':
        main()



