
from statistics import multimode
import numpy as np
import auction as au
from heapq import nlargest
import matplotlib.pyplot as plt
import ennvironment as envv
import random
import copy
from heapq import nlargest
list_of_agents=[]
agent_played=[]
average_via=[]
qualities=[]
n=10
def no0 (seller_1,seller_2):
    buyer=au.Buyer()
    r1=au.payoffMatrix(seller_1,seller_2,buyer).max()
    r2=au.payoffMatrix(seller_2,seller_1,buyer).max()
    while r1==0 or r2==0 :
            buyer=au.Buyer()
            r1=au.payoffMatrix(seller_1,seller_2,buyer).max()
            r2=au.payoffMatrix(seller_2,seller_1,buyer).max()
    return buyer

for _ in range(n):
    list_of_agents.append(au.agent(random.uniform(0,1),random.uniform(0.01,0.06)))
    average_via.append([])
    qualities.append([])
lis=copy.deepcopy(list_of_agents)
for j in range(n-1):
    agent=list_of_agents.pop(0)
    agent_played.append(agent)
    k=j
    for _ in range(len(list_of_agents)):
        buyer=no0(agent,list_of_agents[_])
        av1,av2= envv.play(agent,list_of_agents[_],buyer,j+1,k+1+1)
        average_via[j].append(av1)
        average_via[k+1].append(av2)
        qualities[j].append(agent.product.quality)
        qualities[k+1].append(list_of_agents[_].product.quality)
        k+=1
agent_played.append(list_of_agents[-1])
for u in range(len(average_via)):
    average_via[u]=np.nanmean(average_via[u])
    print(u,average_via[u],average_via[u])
highest=nlargest(10,average_via)

filename="final_best_ones_1st_gen.txt"
file1 = open(filename,"w")
for i in range(len(highest)):
    file1.writelines(["Average:","\t",str(highest[i]),"\t","Seller's gamma, zeta,","\t",str(agent_played[average_via.index(highest[i])].gamma),"\t",\
        str(agent_played[average_via.index(highest[i])].zeta),"\t",str(average_via.index(highest[i])+1),"\n"])
file1.close()
filename="qualities_1st_gen.txt"
np.savetxt(filename,np.array(qualities))