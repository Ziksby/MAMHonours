import numpy as np
import matplotlib.pyplot as plt

filed=np.loadtxt("qualities_2nd_gen.txt")
name=[]
round_r=[]
print(filed)
for i in range(len(filed)):
    name.append("Child "+str(int(i+1)))
    round_r.append(np.count_nonzero(filed[i] == 1))
#['cyan','red','skyblue','gold','lime','violet','silver','pink','mediumpurple','lightseagreen']
color=['silver', 'skyblue', 'mediumpurple', 'gold', 'pink','lightseagreen','red','cyan','violet','lime']
plt.bar(name,round_r,color=color)
plt.ylabel("Games played with the better quality product",fontsize=13)
plt.xticks(rotation=32)
#plt.xlabel("The sellers",fontsize=13)
plt.savefig("qual_2nd_gen.png")