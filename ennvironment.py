from math import gamma
import os 
from statistics import multimode
import numpy as np
import auction as au
import matplotlib.pyplot as plt
import matplotlib
import random
import copy 
diff_qualities=[[0.9,1.0],[1.0,0.9]]
list_of_agents=[]
agent_played=[]
average_via=[]
def make_folders(y,ind_1,ind_2):
    path = "C:/Users/batsy/OneDrive - University of Cape Town/Shock's_course-DESKTOP-E46VEO0/project/P_Q_auction/game_2nd_gen/Game_%1.0f_of_%1.0f_%1.0f"%(y,ind_1,ind_2)
    try: 
        os.mkdir(path) 
        return path
    except OSError as error: 
        print(error) 
    
def assignQualities(seller_1,seller_2,diff_qual):
    seller_1.product.quality=diff_qual[0]
    seller_2.product.quality=diff_qual[1]
    seller_1.product.cost=0.1*(1+seller_1.product.quality)
    seller_2.product.cost=0.1*(1+seller_2.product.quality)

def play(s_1,s_2,buyer,ind_1,ind_2):
    avg1=[]
    avg2=[]
    q_for_game=random.choice(diff_qualities)  
    for y in range(1,2):
        assignQualities(s_1,s_2,q_for_game)
        seller_1=copy.deepcopy(s_1)
        seller_2=copy.deepcopy(s_2)
        path=make_folders(y,ind_1,ind_2)
        price1=[]
        price2=[]


        actionsTaken1=[]
        actionsTaken2=[]
        
        seller_1.setMaxVandS(seller_2,buyer)
        seller_2.setMaxVandS(seller_1,buyer)
        filename="Trail_p1M.txt"
        completeName=os.path.join(path,filename)
        file=open(completeName,"w")
        content = str(seller_1.piM)
        file.write(content)
        file.close()
        filename="Trail_p2M.txt"
        completeName=os.path.join(path,filename)
        file=open(completeName,"w")
        content = str(seller_2.piM)
        file.write(content)
        file.close()

        seller_1.setLearningRate()
        seller_2.setLearningRate()


        state=0
        t=1
        #print("price:",seller_1.product.price,seller_2.product.price)
        seller_1.action(state,t)
        seller_2.action(state,t)
        actionsTaken1.append(seller_1.act)
        actionsTaken2.append(seller_2.act)
        price1.append(seller_1.product.price)
        price2.append(seller_2.product.price)

        r1,r2,ja1=au.sell(seller_1,seller_2,buyer)


        seller_1.ri.append(r1)
        seller_2.ri.append(r2)
        _,__,ja2=au.sell(seller_2,seller_1,buyer)
        newstate_1=au.matchStatesToIndex(seller_1,ja1)
        newstate_2=au.matchStatesToIndex(seller_2,ja2)
        seller_1.updateQ(state,newstate_1,seller_1.act,t)
        seller_2.updateQ(state,newstate_2,seller_2.act,t)
        seller_1.updateEverything(state,t)
        seller_2.updateEverything(state,t)
        seller_1.product.price=au.Pr[0]
        seller_2.product.price=au.Pr[0]


        theAmountOfGames=10000
        p=625
        for _ in range(theAmountOfGames-2):
            t=t+1
            state1=newstate_1
            state2=newstate_2
            seller_1.action(state1,t)
            seller_2.action(state2,t)
            actionsTaken1.append(seller_1.act)
            actionsTaken2.append(seller_2.act)
            price1.append(seller_1.product.price)
            price2.append(seller_2.product.price)
            r1,r2,ja1=au.sell(seller_1,seller_2,buyer)
        
            seller_1.ri.append(r1)
            seller_2.ri.append(r2)
            _,__,ja2=au.sell(seller_2,seller_1,buyer)
            newstate_1=au.matchStatesToIndex(seller_1,ja1)
            newstate_2=au.matchStatesToIndex(seller_2,ja2)
            seller_1.updateQ(state1,newstate_1,seller_1.act,t)
            seller_2.updateQ(state2,newstate_2,seller_2.act,t)
            seller_1.updateEverything(state1,t)

            seller_2.updateEverything(state2,t)
            seller_1.product.price=au.Pr[0]
            seller_2.product.price=au.Pr[0]

        
        plt.plot(np.linspace(1,t,len(seller_1.vAVG[0::p])),seller_1.vAVG[0::p],".",markersize=8,label="$v_%1.0f^{{AVG}}$"%ind_1)
        plt.grid()
        plt.xlabel("Time")
        plt.ylabel("Average reward ($v_i^{{AVG}}$)")
        plt.plot(np.linspace(1,t,len(seller_2.vAVG[0::p])),seller_2.vAVG[0::p],"^",markersize=8,alpha=0.54,label="$v_{%1.0f}^{{AVG}}$"%ind_2)
        plt.legend()
        filename="Trail_viavg.png"
        completeName=os.path.join(path,filename)
        plt.savefig(completeName)
        plt.close()
        
        plt.plot(np.linspace(1,t,len(seller_1.Liaccum[0::p])),seller_1.Liaccum[0::p],".",markersize=8,label="Child %1.0f's accumulated loss"%ind_1)
        plt.plot(np.linspace(1,t,len(seller_2.Liaccum[0::p])),seller_2.Liaccum[0::p],"^",markersize=8,alpha=0.5,label="Child %1.0f's accumulated loss"%ind_2)
        plt.xlabel("Time")
        plt.ylabel("$L_i^{accum}$")
        plt.legend()
        plt.grid()
        
        filename="Trail_acummloss.png"
        completeName=os.path.join(path,filename)
        plt.savefig(completeName)
        plt.close()
        
        
        plt.plot(np.linspace(1,t,len(seller_1.ri[0::p])),seller_1.ri[0::p],".",markersize=8,label="Child %1.0f's rewards "%ind_1)
        plt.plot(np.linspace(1,t,len(seller_2.ri[0::p])),seller_2.ri[0::p],"^",markersize=8,alpha=0.5,label="Child %1.0f's rewards"%ind_2)
        plt.grid()
        plt.xlabel("Time")
        plt.ylabel("The rewards")
        plt.legend()
        filename="Trail_REWARDS.png"
        completeName=os.path.join(path,filename)
        plt.savefig(completeName)
        plt.close()

        
        plt.plot(np.linspace(1,t,len(actionsTaken1[0::p])),actionsTaken1[0::p],".",markersize=8,label="Child %1.0f's action"%ind_1)
        plt.plot(np.linspace(1,t,len(actionsTaken2[0::p])),actionsTaken2[0::p],"^",markersize=8,alpha=0.5,label="Child %1.0f's action"%ind_2)
        plt.xlabel("Time")
        plt.ylabel("Actions taken by the agents")
        plt.legend()
        plt.grid()
        filename="_actions.png"
        completeName=os.path.join(path,filename)
        plt.savefig(completeName)
        plt.close()

    #Game_%1.0f_of_%1.0f_%1.0f. 

    
        

        

        



        filename="Detials_.txt"
        completeName=os.path.join(path,filename)
        fil1=open(completeName,"w")
        fil1.writelines([" Mode for actions seller 1: ",str(multimode(actionsTaken1)),\
            "\n","Actions mode for seller 2 the seller 2  ",str(multimode(actionsTaken2)),\
                "\n","prices1 mode ",str(multimode(price1)),"  how may : ",str(price1.count(multimode(price1)[0])),"\n",\
                    "prices2:  ",str(multimode(price2)),"  how may : ",str(price2.count(multimode(price2)[0])),\
                    "\n","Zeta1: ",str(seller_1.zeta),"\n","Zeta2: " ,str(seller_2.zeta),"\n",\
                        "S1: ", str(len(seller_1.S)),"\n","S2: " ,str(len(seller_2.S)),"\n",\
                            "Quality1:  ",str(seller_1.product.quality),"\n","Quality2: ",str(seller_2.product.quality),\
                                "\n","Q_table max and min respectively for seller 1:  ",str(seller_1.Q_table.max()),"  ",str(seller_1.Q_table.min()),\
                                "\n","Q_table max and min respectively for seller 2:  ",str(seller_2.Q_table.max()),"  ",str(seller_2.Q_table.min()),\
                                "\n","Risk tolerance for s1 and s2 respectively " ,str(seller_1.Ltol) ,"  ",str(seller_2.Ltol)  ,\
                                    "\n Buyer chi and buyer.pb res; ",str(buyer.chi),"  ",str(buyer.pb),\
                                        "\n Learning rate 1 and 2 res:  ",str(seller_1.alpha)," ",str(seller_2.alpha),\
                                            "\n viMM:  ",str(seller_1.viMM),"  ",str(seller_2.viMM),\
                                                "\n state max:  ","  ",str(seller_1.state_counter.max()),"  ",str(seller_2.state_counter.max()),\
                                                    "\n eplison:  ",str(seller_1.eplison),"  ",str(seller_2.eplison),\
                                                        "\n The avg reward over the whole thing :  ",str(seller_1.vAVG[-1]),"  ",str(seller_2.vAVG[-1]),\
                                                            "\n viMM/1-gamma:  ",str(seller_1.viMM/(1-seller_1.gamma)),"  ",str(seller_2.viMM/(1-seller_2.gamma)),\
                                                                "\nThe gamma values res:  ",str(seller_1.gamma),"  ",str(seller_2.gamma)])
        fil1.close()
        filename="Prices_%1.0f.txt"%ind_1
        completeName=os.path.join(path,filename)
        np.savetxt(completeName,np.array(price1))
        filename="Prices_%1.0f.txt"%ind_2
        completeName=os.path.join(path,filename)
        np.savetxt(completeName,np.array(price2))
        avg1.append(seller_1.vAVG[-1])
        avg2.append(seller_2.vAVG[-1])
    #print(np.mean(avg1),np.mean(avg2))
    return np.nanmean(avg1),np.nanmean(avg2)
