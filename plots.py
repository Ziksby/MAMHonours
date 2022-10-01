import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

langs = np.loadtxt("final_best_ones_1st_gen.txt",usecols=-1)

round_r = np.loadtxt("final_best_ones_1st_gen.txt",usecols=1)
name=[]
# ['gold', 'silver', 'violet', 'lightseagreen', 'red','cyan','pink','mediumpurple','lime','skyblue']
for i in langs:
    name.append("Seller "+str(int(i)))
#['silver', 'skyblue', 'mediumpurple', 'gold', 'pink','lightseagreen','red','cyan','violet','lime']
color=['cyan','mediumpurple','pink','silver','gold','lightseagreen','violet','red','lime','skyblue']
plt.bar(name,round_r,color=color)
plt.ylabel("Average reward",fontsize=17)
plt.xticks(rotation=32)
plt.savefig("final_best_1st_gen.png")