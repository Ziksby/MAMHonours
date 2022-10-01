
import numpy as np
from gekko import GEKKO
import random
import copy 

Pr=[1.19/6,1.19/3,119/200,119/150,119/120,1.19]
Qr=[0.9,1.0]

def setPis(seller):
    rows, cols = (seller.H_s_size, seller.act_set_size)
    arr=[]
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(1/seller.act_set_size)
        arr.append(col)

    return arr

def matchStatesToIndex(seller,list):
    return seller.H_s.index(list)

def sell(seller_1,seller_2,buyer):
    profit=0
    if buyer.pickOne(seller_1.product.price, seller_1.product.quality,seller_2.product.price,seller_2.product.quality)==0:
        return (0),(0),[seller_1.act,seller_2.act]
    elif buyer.pickOne(seller_1.product.price, seller_1.product.quality,seller_2.product.price,seller_2.product.quality)==1:
        if seller_1.product.price-seller_1.product.cost>0:
            profit=seller_1.product.price-seller_1.product.cost
        return (profit),(0),[seller_1.act,seller_2.act]
    else:
        if seller_2.product.price-seller_2.product.cost>0:
            profit=seller_2.product.price-seller_2.product.cost

        return (0),(profit),[seller_1.act,seller_2.act]


def H(*seqs): # https://stackoverflow.com/questions/15099647/cross-product-of-sets-using-recursion
    if not seqs:
        return [[]]
    else:
        return [[x] + p for x in seqs[0] for p in H(*seqs[1:])]

class Product():
    def __init__(self):
        self.price=Pr[0]
        self.quality=random.choice(Qr)
        self.cost=0.1*(1+self.quality)


    def changePrice(self,x):
        price_max=Pr[-1]
        price_min=Pr[0]
        self.price+=x
        if self.price> price_max:
            self.price=Pr[-1]

        elif self.price<price_min:
            self.price=Pr[0]

class Buyer():
    def __init__(self):
        self.chi=random.uniform(0,1)
        self.qb=0.1
        self.pb=random.choice(Pr)


    def stepfunction(self,x):
        if x>=0:
            return 1.0
        else:
            return 0.0
        
    def utility(self,p,q):
        return (self.chi*(q-self.qb)+(1-self.chi)*(self.pb-p))*self.stepfunction(q-self.qb)*self.stepfunction(self.pb-p)


    def pickOne(self,p1,q1,p2,q2):
        if self.utility(p1,q1)==self.utility(p2,q2) and self.utility(p2,q2)==0:
            return 0
        elif (self.utility(p1,q1))<(self.utility(p2,q2)):
            return 2
        elif (self.utility(p1,q1))>(self.utility(p2,q2)):
            return 1
        else:
            return random.randint(1,2)

class agent( ):
    def __init__(self,gamma=random.uniform(0,1),zeta=random.uniform(0.01,0.06)):
        self.act_set=np.array([0,1.19/6,1.19/3,119/200,119/150,119/120])
        self.act=0 # previous action
        self.viMM=0
        self.piM=[]
        self.alpha=0
        self.act_set_size=len(self.act_set)
        self.product=Product()
        self.zeta=zeta
        self.gamma=gamma
        self.vAVG=[]
        self.H_s=H(self.act_set,self.act_set)
        self.H_s_size=len(self.H_s)
        self.policy=setPis(self)
        self.eplison=(1000)*0.04/(1000+1)
        self.Ltol=self.act_set_size*self.H_s_size*self.zeta*500
        self.Q_table=np.full((self.H_s_size,self.act_set_size),1/(1-self.gamma))
        self.state_counter=np.zeros(self.H_s_size)
        self.Liaccum=[]
        self.ri=[]
        self.beta=0
        self.V=0
        self.Sprev=[]
        self.Sstar=[]
        self.S=[]
    

    def updateBeta(self,t):
        if any( i>=self.Ltol for i in self.Liaccum):
            self.beta=1

        else:
            self.beta=(self.Liaccum[t-1]/self.Ltol)**2

    def populatingSprev(self,state):
        if len(self.Sprev)<self.H_s_size:
            self.Sprev.append(state)

        else:
            self.Sprev.pop(0)
            self.Sprev.append(state)

    def populatingSstar(self, state):
        if abs(self.Q_table[state].max()-self.Q_table.max())<1e-18:
            self.Sstar.append(state)

    def populatingS(self,state,t):
        if t==1:
            pass
        else:
            self.populatingSprev(state)
            self.populatingSstar(state)
            if state in self.Sprev and state in self.Sstar:
                if len(self.S)<self.H_s_size:
                    self.S.append(state)
                else:
                    self.S.pop(0)
                    self.S.append(state)
            else:
                if len(self.S)>0:
                    self.S.pop(0)
                else:
                    pass

    def updateEplison(self,t):
        if t>=1:
            self.eplison=(1000)*0.4/(1000+self.state_counter.max())

    def updateStateCounter(self,state):
        self.state_counter[state]+=1

    def action(self,state,t):
        if t==1:
            
            self.act=np.random.choice(self.act_set)

        else:
            self.act=self.updatepolicy(state)
        self.product.changePrice(self.act)


    def updateEverything(self,state,t):
        self.updateAvg(t)
        self.updateLiaccum(t)
        self.populatingS(state,t)
        self.updateBeta(t)
        self.updateStateCounter(state)
        self.updateEplison(t)
    



    def updateAvg(self,t):
        self.vAVG.append(np.mean(self.ri))

    def updateLiaccum(self,t):
        list=[0,t*(self.viMM-self.vAVG[t-1])]
        self.Liaccum.append(max(list))

    def setMaxVandS(self,seller_2,buyer):
        self.piM, self.viMM=piMM(self,seller_2,buyer)

    def setLearningRate(self):
        power=(self.zeta*self.act_set_size*self.H_s_size)/(self.Ltol)
        upper_bracket=((self.zeta)/(1-self.viMM+self.zeta))**power
        self.alpha=(1-upper_bracket)/(1-self.gamma)

    def bestResponse(self,state):
        """
        returns how much the price changes by.
        """
        if self.Q_table[state].max()>self.viMM/(1-self.gamma):
            
            return self.act_set[self.Q_table[state].argmax()]
        else:
            ai=np.random.choice(self.act_set,p=self.piM)
            return ai

    def cautiousLB(self,state):
        """
        returns the actual action not the index of the action
        """
        if all(i<self.Ltol for i in self.Liaccum):
            
            return self.act_set[self.Q_table[state].argmax()]
        else:
            ai=np.random.choice(self.act_set,p=self.piM)
            return ai

    def updateV(self,state,t):
        if t==1:
            pass
        else:
            self.V=sum((1/self.act_set_size)*self.Q_table[state])

    def updateQ(self,state,newstate,action,t):
        if t==1:
            pass
        else:
            self.updateV(newstate,t)
            copyA=copy.deepcopy(self.act_set)
            copyA=copyA.tolist()
            index=copyA.index(action)
            self.Q_table[state][index]+=self.alpha*(self.ri[t-1]+self.gamma*self.V-self.Q_table[state][index])



    def bestPolicy(self,state):
        list=[0,1]
        pick=np.random.choice(list,p=[self.beta,1-self.beta])
        if pick ==1:
            return self.bestResponse(state)

        else:
           return self.cautiousLB(state)



    def updatepolicy(self,state):
        if self.beta==1 or len(self.S)>0:
            return self.bestPolicy(state)
        else:
            list=[0,1]
            pick=np.random.choice(list,p=[self.eplison,1-self.eplison])
            if pick ==1:
                return self.bestPolicy(state)
            else:
                return np.random.choice(self.act_set)    


def payoffMatrix(seller_1,seller_2,buyer):
    """
    Return the payoff matrix for player/seller 1.
    """
    payoff=np.zeros((seller_1.act_set_size,seller_2.act_set_size))
    s1=copy.deepcopy(seller_1)# to ensure no changes happen to the seller's product while calculating the payoff matrix
    s2=copy.deepcopy(seller_2)
    for i in range(len(payoff)):
        s1.product.changePrice(s1.act_set[i])
        for j in range(len(payoff[i])):
            s2=copy.deepcopy(seller_2)
            s2.product.changePrice(s2.act_set[j])
            payoff[i][j],_,__=sell(s1,s2,buyer)
        s1=copy.deepcopy(seller_1)
    return payoff

def piMM(seller_1,seller_2,buyer):
    """
    http://apmonitor.com/me575/index.php/Main/MiniMax
    """
    payoff=payoffMatrix(seller_1,seller_2,buyer)
    m = GEKKO(remote=False)
    m.options.SOLVER = 1
    ni = seller_1.act_set_size  # number of rows
    nj = 1  # number of columns
    # best method: use m.Array function
    x = m.Array(m.Var,(ni,nj))
    m.Equations([x[i][j]>=0 for i in range(ni) for j in range(nj)])
    m.Equation(1==sum([sum([x[i][j] for i in range(ni)]) for j in range(nj)]))
    z = m.Var()
    m.Equation((z-(sum([sum([payoff[j][i]*x[i][j] for i in range(ni)]) for j in range(nj)])))<=0)
    m.Maximize(z)
    m.solve(disp=False)
    x=x.flatten()
    V=[]
    for i in range(len(x)):
        V.append(x[i][0])
    V=np.array(V)

    return V, z[0]