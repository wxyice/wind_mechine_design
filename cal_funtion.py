import random
from math import acos, atan, cos, e, pi, sin, sqrt

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
    gama=0.9
    iternum=0
    while True:
        dCp=(cal_Cp(a+da,r,R,n,r_hub,v1)-cal_Cp(a,r,R,n,r_hub,v1))/da

        a_new =a + dCp * learning_rate
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
    

def main_cal(R,r_hub,v1,n):
    #Cl=1.0423
    omega=n*2*pi
    step=100
    delta=0.1

    #------------------------calculate---------------------------
    rlist=iter(np.linspace(r_hub+delta,R-delta,step))
    alist,a1list,Cplist=[],[],[]
    philist,Flist,llist,sigmalist,lamdalist=[],[],[],[],[]

    while True:
        try:
            r=next(rlist)
        except :
            break
        a,a1,cp=cal_CPmax(r=r,R=R,n=n,r_hub=r_hub,v1=v1)
        lamda=(n*2*pi)*r/v1
        phi=cal_phi(a,a1,lamda)
        F=cal_F(r,R,n,r_hub,phi)
        l=cal_l_Re(a,a1,r,R,n,r_hub,v1)
        sigma=cal_sigma(a,F,phi)
        
        alist.append(a)
        a1list.append(a1)
        Cplist.append(cp)
        lamdalist.append(lamda)
        philist.append(phi)
        Flist.append(F)
        llist.append(l)
        sigmalist.append(sigma)

        print("r={0:6.2f} a={1:6.4f} a1={2:6.4f} cp={3:6.4f} lamda={4:6.4f} phi={5:6.4f} F={6:6.4f} l={7:6.4f} sigma={8:6.4f}".format(r,a,a1,cp,lamda,phi,F,l,sigma))

    rlist=np.linspace(r_hub+delta,R-delta,step).tolist()
    av1list=np.array(alist)*v1
    omegarlist=np.linspace(r_hub+delta,R-delta,step)*omega*np.array(a1list)
    W=(v1*np.sqrt((1-np.array(alist))**2+(1+np.array(a1list))**2*np.array(lamdalist)**2)).tolist()

    av1list=av1list.tolist()
    omegarlist=omegarlist.tolist()

    #rlist=np.linspace(r_hub+delta,R-delta,step)
    value=[rlist,alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W]

    return value


def cal_a1_for_draw(a,r,R,n,r_hub,v1):
    def cal_f(n,r,v1,R,r_hub,a,a1):
        lamda=(n*2*pi)*r/v1
        phi=cal_phi(a,a1,lamda)
        F=cal_F(r,R,n,r_hub,phi)
        f=a1*(1+a1)*(lamda**2)-(a*(1-a*F))
        #print('f={}'.format(f))
        return f

    a1_all=[i/100 for i in range(300)]
    f_all=[]
    for num in a1_all:
        f_all.append(cal_f(n,r,v1,R,r_hub,a,num))

    dx=1e-6
    err=1000
    a1=2#random.random()
    a1_iter_list=[]
    f_iter_list=[]
    while err>1e-6:
        a1_iter_list.append(a1)
        f_iter_list.append(cal_f(n,r,v1,R,r_hub,a,a1))
        dy=(cal_f(n,r,v1,R,r_hub,a, a1+dx)-cal_f(n,r,v1,R,r_hub,a, a1))/dx
        a1=a1-cal_f(n,r,v1,R,r_hub,a, a1)/(dy+1e-8)
        err=abs(cal_f(n,r,v1,R,r_hub,a, a1))
        
    return a1_all,f_all,a1_iter_list,f_iter_list

def cal_CPmax_for_draw(r,R,n,r_hub,v1):
    lamda=(n*2*pi)*r/v1

    def cal_Cp_all(a,a1,r,R,n,r_hub,lamda):
        phi=np.arctan((1-a)/(lamda*(1+a1)))

        Fte=np.exp((-n*(R-r)/(2*R*np.sin(phi))))
        Ft=2*np.arccos(Fte)/np.pi
        Fhe=np.exp((-n*(r-r_hub)/(2*r_hub*np.sin(phi))))
        Fh=2*np.arccos(Fhe)/np.pi
        F=Ft*Fh
        return 4*(1-a)*a1*F*lamda**2
    
    a_all=np.linspace(0.05,0.5,200)
    a1_all=np.linspace(0.001,0.2,200)
    a_all,a1_all=np.meshgrid(a_all,a1_all)
    Cp_all=cal_Cp_all(a_all, a1_all, r, R, n, r_hub, lamda)

    err=100
    da=1e-5
    a=0.1
    learning_rate=0.01
    iternum=0
    a_iter_list,a1_iter_list,Cp_iter_list=[],[],[]
    while True:
        a_iter_list.append(a)
        a1=cal_a1(a,r,R,n,r_hub,v1)
        a1_iter_list.append(a1)
        Cp_old=cal_Cp(a,r,R,n,r_hub,v1)
        Cp_iter_list.append(Cp_old)

        dCp=(cal_Cp(a+da,r,R,n,r_hub,v1)-Cp_old)/da
        a_new =a + dCp * learning_rate
        err=abs(a_new-a)  
        iternum+=1
        #print('err={}'.format(err))   
        if err<1e-6:
            break
        else:
            a=a_new
            #print("a={},iter={}".format(a_new,iternum))

    a_iter_list=np.array(a_iter_list)
    a1_iter_list=np.array(a1_iter_list)
    Cp_iter_list=np.array(Cp_iter_list)
    return a_all,a1_all,Cp_all,a_iter_list,a1_iter_list,Cp_iter_list


def cal_l_Re_for_draw(a,a1,r,R,n,r_hub,v1):

    def cal_f(l,W,F,phi,n,r,v):
        Re=W*l/v
        Cl=Re2Cl(Re)   
        return cal_l(a,F,phi,n,r,Cl)-l

    lamda=(n*2*pi)*r/v1
    W=v1*sqrt((1-a)**2+(1-a1)**2*lamda**2)
    v=1.511e-5

    phi=cal_phi(a, a1, lamda)
    F=cal_F(r, R, n, r_hub, phi)

    l_all=np.linspace(0.1,6,100)
    f_all=[]
    for l in l_all:
        f_all.append(cal_f(l,W,F,phi,n,r,v))

    err=10000
    l=5
    dx=1e-6

    l_iter_list=[]
    f_iter_list=[]

    while err>1e-6:
        l_iter_list.append(l)
        f_iter_list.append(cal_f(l,W,F,phi,n,r,v))

        kkk=cal_f(l+dx,W,F,phi,n,r,v)
        kkk=cal_f(l,W,F,phi,n,r,v)


        dy=(cal_f(l+dx,W,F,phi,n,r,v)-cal_f(l,W,F,phi,n,r,v))/dx
        l=l-cal_f(l,W,F,phi,n,r,v)/(dy+1e-8)

        kkk=cal_f(l,W,F,phi,n,r,v)
        print(kkk)
        err=abs(kkk)
    l_iter_list.append(l)
    f_iter_list.append(cal_f(l,W,F,phi,n,r,v))
    return l_all,np.array(f_all),np.array(l_iter_list),np.array(f_iter_list)



if __name__ == '__main__':
    from plot2D3D import draw2D,draw3D

    # 基本参数数据
    R=12.7      # m
    r_hub=0.3   # m
    v1=13       # m/s
    n=72/60     # 圈/s

    r=3
    a=0.35

    #a1_all,f_all,a1_iter_list,f_iter_list=cal_a1_for_draw(a,r,R,n,r_hub,v1)
    #draw2D(X=a1_all,Y=f_all,x=a1_iter_list,y=f_iter_list)

    a_all,a1_all,Cp_all,a_iter_list,a1_iter_list,Cp_iter_list=cal_CPmax_for_draw(r,R,n,r_hub,v1)
    draw3D(X=a_all,Y=a1_all,Z=Cp_all,x=a_iter_list[0:50],y=a1_iter_list[0:50],z=Cp_iter_list[0:50])
    #a1=a1_iter_list[-1]
    
    #l_all,f_all,l_iter_list,f_iter_list=cal_l_Re_for_draw(a,a1,r,R,n,r_hub,v1)
    #print(l_all)
    #draw2D(X=l_all,Y=f_all,x=l_iter_list,y=f_iter_list)
    
