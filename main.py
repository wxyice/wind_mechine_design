import random
from math import acos, atan, e, pi, sin,cos, sqrt
from matplotlib import pyplot as plt

import numpy as np


def cal_F(r,R,n,r_hub,phi):
    """
    This is a groups style docs.
    
    Parameters:
    param1 - r 半径位置 m 
    param2 - R 风轮半径 m
    param3 - n 转速     rps
    param4 - r_hub 轮毂半径 m
    param5 - phi 入流角 rad

    Returns:
    F
    
    Raises:
    KeyError - raises an exception
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

def cal_l(a,F,phi,n,r,Cl):
    k1=8*pi*a*F*(1-a*F)*sin(phi)**2
    k2=(1-a)**2*cos(phi)
    
    k3=r/(n*Cl)

    return k1/k2*k3

def cal_sigma(a,F,phi):
    k1=a*F*(1-a*F)*sin(phi)**2
    k2=(1-a)**2*cos(phi)
    return k1/k2

def cal_a1(a,r,R,n,r_hub,v1):

    def cal_f(n,r,v1,R,r_hub,a,a1):
        lamda=(n*2*pi)*r/v1
        phi=cal_phi(a,a1,lamda)
        F=cal_F(r,R,n,r_hub,phi)
        f=a1*(1+a1)*(lamda**2)-(a*(1-a*F))
        #print('f={}'.format(f))
        return f

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
    return a_new,cal_a1(a_new,r,R,n,r_hub,v1),cal_Cp(a_new,r,R,n,r_hub,v1)


def Re2Cl(Re):
    '''
    R² = 0.9996
    '''
    if Re>10e5:
       Cl=1.0423
    if 2e5<Re<10e5:
        Cl=-(1e-7)*Re + 1.175
    elif 1e5<Re<2e5:
        print(Re)
        Cl=-(4e-7)*Re + 1.236
    elif Re<1e5:
        print(Re)
        Cl=(1e-5)*Re + 0.0231
    return Cl



def cal_l_Re(a,a1,r,R,n,r_hub,v1):

    def cal_W(a,a1,lamda,v1):
        return v1*sqrt((1-a)**2+(1-a1)**2*lamda**2)
    def cal_Re(W,l,v=1.511e-5):
        return W*l/v
    
    def cal_f(l,W,F,phi,n,r):
        Re=cal_Re(W,l,v=1.511e-5)
        Cl=Re2Cl(Re)   
        return cal_l(a,F,phi,n,r,Cl)-l


    lamda=(n*2*pi)*r/v1
    phi=cal_phi(a, a1, lamda)
    F=cal_F(r, R, n, r_hub, phi)
    W=cal_W(a,a1,lamda,v1)

    err=10000
    l=1.5
    dx=1e-6
    
    while err>1e-6:
        dy=(cal_f(l+dx,W,F,phi,n,r)-cal_f(l,W,F,phi,n,r))/dx
        l=l-cal_f(l,W,F,phi,n,r)/(dy+1e-8)
        err=abs(cal_f(l,W,F,phi,n,r))
    return l
    



if __name__ == '__main__':
    R=12.7
    r_hub=0.3
    v1=13
    n=72/60
    Cl=1.0423
    omega=n*2*pi

    step=30
    delta=0.01


    #------------------------calculate---------------------------
    rlist=iter(np.linspace(r_hub+delta,R-delta,step))
    alist=[]
    Cplist=[]
    a1list=[]

    while True:
        try:
            r=next(rlist)
        except :
            break
        a,a1,cp=cal_CPmax(r=r,R=R,n=n,r_hub=r_hub,v1=v1)
        alist.append(a)
        a1list.append(a1)
        Cplist.append(cp)

        print("r={3:6.4f} a={0:6.4f} a1={1:6.4f} cp={2:6.4f}".format(a,a1,cp,r))

    rlist=np.linspace(r_hub+delta,R-delta,step).tolist()
    aa1iter=iter(zip(rlist,alist,a1list))

    philist,Flist,llist,sigmalist,lamdalist=[],[],[],[],[]

    while True:
        try:
            r,a,a1=next(aa1iter)
        except :
            break
        lamda=(n*2*pi)*r/v1
        phi=cal_phi(a,a1,lamda)
        F=cal_F(r,R,n,r_hub,phi)
        l=cal_l_Re(a,a1,r,R,n,r_hub,v1)
        sigma=cal_sigma(a,F,phi)

        lamdalist.append(lamda)
        philist.append(phi)
        Flist.append(F)
        llist.append(l)
        sigmalist.append(sigma)

        print("r={3:6.4f} lamda={0:6.4f} phi={1:6.4f} F={2:6.4f} l={4:6.4f} sigma={5:6.4f}".format(lamda,phi,F,r,l,sigma))
    
    
    av1list=np.array(alist)*v1
    omegarlist=np.linspace(r_hub+delta,R-delta,step)*omega*np.array(a1list)
    W=(v1*np.sqrt((1-np.array(alist))**2+(1+np.array(a1list))**2*np.array(lamdalist)**2)).tolist()
    av1list=av1list.tolist()
    omegarlist=omegarlist.tolist()

    rlist=np.linspace(r_hub+delta,R-delta,step)

    value=[alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W]
    
    save=True
    if save:
        #--------------------------save data as txt-------------------------

        with open('result_Re_liner_cut.txt','w') as f:
            for i in range(len(rlist)):
                f.write("{0} ".format(rlist[i]))
                for j in value:
                    f.write("{0} ".format(j[i]))
                f.write('\n')

        list1=[rlist,alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W]
        
        #--------------------------save data as xls-------------------------------
        with open('data_Re_liner_cut.xls','w',encoding='gbk') as output:

            for i in range(len(list1)):
                for j in range(len(list1[i])):
                    output.write(str(list1[i][j]))    
                    output.write('\t')   
                output.write('\n')       
        output.close()

    #-----------------------------draw---------------------------------------

    draw=True
    if draw:
        for i in range(len(value)):
            plt.subplot(5,2,i+1)
            plt.plot(rlist,value[i])
        plt.show()



    


    





