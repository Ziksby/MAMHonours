import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from fractions import Fraction
from collections import OrderedDict
import auction as au
import os
import matplotlib
matplotlib.use('Agg')

Pr1=[1.19/6,1.19/3,119/200,119/150,119/120,1.19]
Pr=["$\\frac{1.19}{6}$", "$\\frac{1.19}{3}$","$\\frac{1.19}{2}$","$\\frac{1.19}{1.5}$","$\\frac{1.19}{1.2}$","1.19"]
X_axis = np.arange(len(Pr))

def pMs(path,ind):
    name=os.path.join(path,'Trail_p%1.0fM.txt'%ind)
    with open(name) as f:
        lines = f.read().splitlines(1)
    lines=lines[0]
    p1M=[]
    lines=lines[1:-1].split()
    j=0
    if any( float(i)>=0.3 for i in lines):
        j=i
    [p1M.append(str(Fraction(float(i)).limit_denominator())) for i in lines]
    return p1M,float(j)
def add_value_label(x,y,p):
    for i in range(len(x)):
        plt.text(i-0.2, y[i], p[i],ha = 'center')
def add_value_label1(x,y,p):
    for i in range(len(x)):
        plt.text(i+0.2, y[i], p[i],ha = 'center')

agents=list(range(1,11))
agents_played=[]
n=10
for j in range(n-1):
    agents_played.append(agents.pop(0))
    k=j
    for _ in range(len(agents)):
        k+=1
        ind_1=j+1
        ind_2=k+1
        path = "C:/Users/batsy/OneDrive - University of Cape Town/Shock's_course-DESKTOP-E46VEO0/project/P_Q_auction/game_2nd_gen/Game_1_of_%1.0f_%1.0f/"%(ind_1,ind_2)
        name=os.path.join(path,"Detials_.txt")
        buyer_chi=np.loadtxt(name,skiprows=13,usecols=5,max_rows=1)
        buyer_pb=np.loadtxt(name,skiprows=13,usecols=6,max_rows=1)
        avg1=np.loadtxt(name,skiprows=18,usecols=8,max_rows=1)
        avg2=np.loadtxt(name,skiprows=18,usecols=9,max_rows=1)
        q1=np.loadtxt(name,skiprows=8,usecols=1,max_rows=1)
        q2=np.loadtxt(name,skiprows=9,usecols=1,max_rows=1)
        p1M,ele1=pMs(path,1)
        p2M,ele2=pMs(path,2)
        price1=np.loadtxt(os.path.join(path,"Prices_%1.0f.txt"%ind_1))
        price2=np.loadtxt(os.path.join(path,"Prices_%1.0f.txt"%ind_2))
        i,= np.where(np.isclose(Pr1, buyer_pb))
        p=Counter(price1)
        p = OrderedDict(sorted(p.items()))
        p2=Counter(price2)
        p2 = OrderedDict(sorted(p2.items()))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(X_axis - 0.2, list(p.values()), 0.4, label = 'Child %1.0f with quality %1.1f'%(ind_1,q1))
        add_value_label(X_axis,list(p.values()),p1M)
        ax.bar(X_axis + 0.2, list(p2.values()), 0.4, label = 'Child %1.0f with quality %1.1f'%(ind_2,q2))
        add_value_label1(X_axis,list(p2.values()),p2M)
        plt.xticks(X_axis, Pr)
        [ax.xaxis.get_ticklabels()[i[0]].set_color('red')]
        matplotlib.rc('xtick', labelsize=10.5) 
        matplotlib.rc('ytick', labelsize=10.5) 
        plt.xlabel("Prices",fontsize=10.5)
        plt.ylabel("Number of times selected",fontsize=10.5)
        plt.legend(prop={'size': 10.5})
        plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
        name=os.path.join(path,"GameSummary.png")
        plt.savefig(name)
        plt.close()
        if abs(avg1-avg2)<=0.035 or abs(avg1-avg2)>=0.22 or float(ele1)>0.3 or float(ele2)>0.3:
            filename="GamesToCheckGEn2.txt"
            fil1=open(filename,"a")
            fil1.writelines([str(ind_1),"_",str(ind_2),'\n'])
            fil1.close()

        