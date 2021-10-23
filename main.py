import random
from math import acos, atan, e, pi, sin,cos
from matplotlib import pyplot as plt

import numpy as np


def cal_F(r,R,n,r_hub,phi):
    """
    :param: r 半径位置 m
    :param: R 风轮半径 m
    :param: n 转速     rps
    :param: r_hub 轮毂半径 m
    :param: phi 入流角 rad
    """
    Fte=e**(-n*(R-r)/(2*R*sin(phi)))
    Ft=2*acos(Fte)/pi
    Fhe=e**(-n*(r-r_hub)/(2*r_hub*sin(phi)))
    Fh=2*acos(Fhe)/pi
    F=Ft*Fh
    return F

def cal_Cp(a,r,R,n,r_hub,v1):
    """
    :param: a 轴向干涉因子
    a1 周向干涉因子
    F  总损失系数
    lamda 当地叶尖速比
    """
    a1=cal_a1(a,r,R,n,r_hub,v1)
    lamda=(n*2*pi)*r/v1
    phi=cal_phi(a,a1,lamda)
    F=cal_F(r,R,n,r_hub,phi)

    Cp=4*(1-a)*a1*F*lamda**2
    return Cp

def cal_phi(a,a1,lamda):
    phi=atan((1-a)/(lamda*(1+a1)))
    return phi

def cal_f(n,r,v1,R,r_hub,a,a1):
    lamda=(n*2*pi)*r/v1
    phi=cal_phi(a,a1,lamda)
    F=cal_F(r,R,n,r_hub,phi)
    f=a1*(1+a1)*(lamda**2)-(a*(1-a*F))
    #print('f={}'.format(f))
    return f

def cal_a1(a,r,R,n,r_hub,v1):
    dx=1e-6
    err=1000
    a1=0
    while err>1e-6:
        dy=(cal_f(n,r,v1,R,r_hub,a, a1+dx)-cal_f(n,r,v1,R,r_hub,a, a1))/dx
        a1=a1-cal_f(n,r,v1,R,r_hub,a, a1)/(dy+1e-8)
        err=abs(cal_f(n,r,v1,R,r_hub,a, a1))
    return a1

def cal_CPmax(r,R,n,r_hub,v1):
    err=100
    da=1e-5
    a=random.random()
    learning_rate=0.01
    iternum=0
    while True:
        dCp=(cal_Cp(a+da,r,R,n,r_hub,v1)-cal_Cp(a,r,R,n,r_hub,v1))/da

        a_new = a + dCp * learning_rate
        err=abs(a_new-a)  
        iternum+=1
        #print('err={}'.format(err))   
        if err<1e-6:
            break
        else:
            a=a_new
            #print("a={},iter={}".format(a_new,iternum))
        # if iternum>10000:
        #     a=random.random()
        #     iternum=0
    return a_new,cal_a1(a_new,r,R,n,r_hub,v1),cal_Cp(a_new,r,R,n,r_hub,v1)
# l=2
# sigma=0.05
# 4/5 pi

def cal_l(a,F,phi,n,r,Cl):
    k1=8*pi*a*F*(1-a*F)*sin(phi)**2
    k2=(1-a)**2*cos(phi)
    
    k3=r/(n*Cl)

    return k1/k2*k3

def cal_sigma(a,F,phi):
    k1=a*F*(1-a*F)*sin(phi)**2
    k2=(1-a)**2*cos(phi)
    return k1/k2


if __name__ == '__main__':
    R=12.7
    r_hub=0.3
    v1=13
    n=72/60
    Cl=1.0423
    omega=n*2*pi

    skip=100
    delta=0.01


    # a a1 cp 
    rlist=iter(np.linspace(r_hub+delta,R-delta,skip))
    alist=[]
    Cplist=[]
    a1list=[]

    while True:
        try:
            r=next(rlist)
        except :
            break
        a,a1,cp=cal_CPmax(r=r,R=R,n=n,r_hub=r_hub,v1=v1)
        #rlist.append(i)
        alist.append(a)
        a1list.append(a1)
        Cplist.append(cp)

        print("r={3},a={0},a1={1},cp={2}".format(a,a1,cp,r))


    # F phi l 
    rlist=np.linspace(r_hub+delta,R-delta,skip)
    rlist=rlist.tolist()
    aa1iter=iter(zip(rlist,alist,a1list))

    philist=[]
    Flist=[]
    llist=[]
    sigmalist=[]
    lamdalist=[]

    while True:
        try:
            r,a,a1=next(aa1iter)
        except :
            break
        lamda=(n*2*pi)*r/v1
        phi=cal_phi(a,a1,lamda)
        F=cal_F(r,R,n,r_hub,phi)
        l=cal_l(a,F,phi,n,r,Cl)
        sigma=cal_sigma(a,F,phi)

        lamdalist.append(lamda)
        philist.append(phi)
        Flist.append(F)
        llist.append(l)
        sigmalist.append(sigma)
    
    
    av1list=np.array(alist)*v1
    omegarlist=np.linspace(r_hub+delta,R-delta,skip)*omega*np.array(a1list)
    W=(v1*np.sqrt((1-np.array(alist))**2+(1+np.array(a1list))**2*np.array(lamdalist)**2)).tolist()
    av1list=av1list.tolist()
    omegarlist=omegarlist.tolist()

    #--------------------draw--------------------------------

    rlist=np.linspace(r_hub+delta,R-delta,skip)

    value=[alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W]
    with open('result.txt','w') as f:
        for i in range(len(rlist)):
            f.write("{0} ".format(rlist[i]))
            for j in value:
                f.write("{0} ".format(j[i]))
            f.write('\n')

    list1=[rlist,alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W]
    
    
    with open('data.xls','w',encoding='gbk') as output:

        for i in range(len(list1)):
            for j in range(len(list1[i])):
                output.write(str(list1[i][j]))    
                output.write('\t')   
            output.write('\n')       
    output.close()


    for i in range(len(value)):
        plt.subplot(5,2,i+1)
        plt.plot(rlist,value[i])

    plt.show()





    
    


    





