from math import gamma
import os 
from statistics import multimode
import numpy as np
import auction as au
import auction as au
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
def sgn_p(x):
    p=[]
    y=np.array(x)
    a=y[0]
    for i in y:
        if i-a<0:
            p.append(-1)
        elif i-a==0:
            p.append(0)
        else:
            p.append(1)
    #p=np.sign(a-y)
    #print(a-y)
    return p
def make_folders(ind_1,ind_2,s,y=1):
    path = "C:/Users/batsy/OneDrive - University of Cape Town/Shock's_course-DESKTOP-E46VEO0/project/P_Q_auction/game_2nd_gen/Game_%1.0f_of_%1.0f_%1.0f/REAL_%1.0f"%(y,ind_1,ind_2,s)
    try: 
        os.mkdir(path) 
        return path
    except OSError as error: 
        print(error) 

def foldersName(ind_1,ind_2,y=1):
    path = "C:/Users/batsy/OneDrive - University of Cape Town/Shock's_course-DESKTOP-E46VEO0/project/P_Q_auction/game_2nd_gen/Game_%1.0f_of_%1.0f_%1.0f"%(y,ind_1,ind_2)
    filename2="Prices_%1.0f.txt"%ind_2
    filename1="Prices_%1.0f.txt"%ind_1
    completeName1=os.path.join(path,filename1)
    completeName2=os.path.join(path,filename2)

    return completeName1,completeName2
def ploting(c1,ind_1,ind_2,s):
    price1=np.loadtxt(c1)
    #price1=sgn_p(price1)
    n=200
    path=make_folders(ind_1,ind_2,s)
    for i in range(1,51):
        fig=plt.figure()
        if i==50:
            plt.plot(range(n*(i-1),n*i-1),price1[n*(i-1):n*i],"-")
        else:
            plt.plot(range(n*(i-1),n*i),price1[n*(i-1):n*i],"-")
        plt.ylabel("Prices")
        #plt.ylabel("Prices")
        plt.axis([n*(i-1),n*i,-1.5,1.5])
        #plt.xticks(np.arange(1000,n+100))
        plt.xlabel("time steps")
        plt.grid()
        filename="Prices_%1.0f"%i
        plt.savefig(os.path.join(path,filename))
        plt.close('all')
        #plt.clf()

list_of_agents=[1,2,3,4,5,6,7,8,9,10]
print(len(list_of_agents))
for j in range(1,10-1):
    list_of_agents.pop(0)
    k=j+1
    for _ in range(len(list_of_agents)):
        c1,c2=foldersName(j,k)
        ploting(c1,j,k,j)
        ploting(c2,j,k,k)

        k+=1