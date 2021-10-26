import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import solve 

Re=[# *10^5
    1,
    2,
    5,
    10]

Cl=[
    1.1919,
    1.1478,
    1.1100,
    1.0423
]

Re=np.array(Re)
Cl=np.array(Cl)


x_array=Re.copy()
y_array=Cl.copy()

m=len(Re)
n=1

order=np.array([len(Re)*[i for i in range(0,n+1)]]).reshape(-1,n+1)
Re2=np.repeat(Re,n+1,0).reshape(m,-1)
#order=np.repeat(order,n+1,1)
print(Re2)
print(order)
X=Re2**order
print(X)




X = solve(np.matmul(X.T,X),np.matmul(X.T,Cl))
print(X)

a1,a2=X

x=np.array([i for i in range(1,10)])
print(x.shape)
y=a1*x+a2
plt.scatter(Re,Cl)
plt.plot(x,y)
plt.show()