import numpy as np
import os
import matplotlib.pyplot as plt

path= "C:/Users/batsy/OneDrive - University of Cape Town/Shock's_course-DESKTOP-E46VEO0/project/P_Q_auction/game_1st_gen/Game_%1.0f_of_%1.0f_%1.0f"%(1,1,2)
os.chdir(path)
price1=np.loadtxt("Prices_2.txt")
price1=np.sign(-price1[4036]+price1)
plt.plot(np.arange(4030,4050),price1[4030:4050])    
plt.scatter(np.arange(4036,4038),price1[4036:4038],color='red')
plt.scatter([4039],price1[4039],color='red')

plt.annotate("Point $p_1$", (4036, price1[4036]))
plt.annotate("Point $p_2$", (4037, price1[4037]))
plt.annotate("Point $p_3$", (4039, price1[4039]))


plt.ylabel("sgn$(\Delta p)(t)$")
plt.xlabel("time steps")
plt.grid()
plt.show()