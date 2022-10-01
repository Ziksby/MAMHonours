import numpy as np
import random
import ennvironment as envv
import auction as au
import copy
from heapq import nlargest
gamma=np.loadtxt("final_best_ones_1st_gen.txt",usecols=5)
zetas=np.loadtxt("final_best_ones_1st_gen.txt",usecols=6)
ind=np.loadtxt("final_best_ones_1st_gen.txt",usecols=-1)
avre=np.loadtxt("final_best_ones_1st_gen.txt",usecols=1)
parents=[]
children=[]
def tournamement_selection(avre=avre):
    parent=random.choices(np.arange(0,10),k=2)
    if avre[parent[0]]>avre[parent[1]]:
        return parent[0]
    else:
        return parent[1]

def crossOver(dad,mom,gammas=gamma,zetas=zetas):
    child1=au.agent(gammas[dad]+ np.random.normal(0,0.001,1)[0], zetas[mom]+ np.random.normal(0,0.001,1)[0])
    child2=au.agent(gammas[mom]+np.random.normal(0,0.001,1)[0],zetas[dad]+np.random.normal(0,0.001,1)[0])
    children.append(child1)
    children.append(child2)
def make_kids():
    for p in range(5):
        dad=tournamement_selection()
        mom=tournamement_selection()
        parents.append([dad,mom])
        crossOver(dad,mom)
make_kids()
list_of_agents=children
print(len(list_of_agents))
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

filename="final_best_ones_2nd_gen.txt"
file1 = open(filename,"w")
for i in range(len(highest)):
    file1.writelines(["Average:","\t",str(highest[i]),"\t","Seller's gamma, zeta,","\t",str(agent_played[average_via.index(highest[i])].gamma),"\t",\
        str(agent_played[average_via.index(highest[i])].zeta),"\t",str(average_via.index(highest[i])+1),"\n"])
file1.close()
filename="qualities_2nd_gen.txt"
np.savetxt(filename,np.array(qualities))
filename="parents_2nd_gen.txt"
np.savetxt(filename,np.array(parents))
