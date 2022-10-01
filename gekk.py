# from gekko import GEKKO
# import numpy as np
# m = GEKKO(remote=False)
# m.options.SOLVER = 1

# ni = 17  # number of rows
# nj = 1  # number of columns
# a=np.ones((17,17))
# r=87
# for i in range(len(a)):
#     for j in range(len(a[i])):
#         a[i][j]=r
#         r-=13

# # best method: use m.Array function
# x = m.Array(m.Var,(ni,nj))

# m.Equations([x[i][j]>=0 for i in range(ni) for j in range(nj)])
# m.Equation(1==sum([sum([x[i][j] for i in range(ni)]) for j in range(nj)]))

# z = m.Var()
# m.Equation(0<=z-(sum([sum([a[j][i]*x[i][j] for i in range(ni)]) for j in range(nj)])))
# m.Minimize(z)
# m.solve()

# print('x:')
# x=x.flatten()

# t=[]
# for i in range(len(x)):
#     t.append(x[i][0])
# t=np.array(t)
# print(t)
# print('z')
# print(z.value)

import numpy as np
import statistics


print(statistics.mode([1,2,3,4,4,4,5,5,5,5]))