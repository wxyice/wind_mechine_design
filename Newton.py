import math
from main import cal_f as y



def Newton():
    dx=1e-6
    err=1000
    n=72
    r=30
    v1=13
    R=72
    a=0.5
    a1=0
    r_hub=2
    while err>1e-6:
        dy=(y(n,r,v1,R,r_hub,a, a1+dx)-y(n,r,v1,R,r_hub,a, a1))/dx
        a1=a1-y(n,r,v1,R,r_hub,a, a1)/(dy+1e-8)
        #print(a1)
        err=abs(y(n,r,v1,R,r_hub,a, a1))
    print("a1={0:8.4f}".format(a1))
    return a1


Newton()