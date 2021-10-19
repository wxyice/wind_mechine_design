from math import acos,cos,asin,sin,atan
from math import e,pi
import numpy as np
import random


def cal_F(r,R,n,r_hub,phi):
    """
    :param: r 半径位置 m
    :param: R 风轮半径 m
    :param: n 转速     rpm
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
    lamda=(n*pi/60)*r/v1
    phi=cal_phi(a,a1,lamda)
    F=cal_F(r,R,n,r_hub,phi)

    Cp=4*(1-a)*a1*F*lamda**2
    return Cp

def cal_phi(a,a1,lamda):
    phi=atan((1-a)/(lamda*(1+a1)))
    return phi

def cal_f(n,r,v1,R,r_hub,a,a1):
    lamda=(n*pi/60)*r/v1
    phi=cal_phi(a,a1,lamda)
    F=cal_F(r,R,n,r_hub,phi)
    f=a1*(1+a1)*lamda**2-(a*(1-a*F))
    #print('f={}'.format(f))
    return f


def cal_Cp2max(a,r,R,n,r_hub,v1):
    
    err=100
    deltaA=0.0001

    count=0
    a_new=a+deltaA
    while err>0.00001:
        
        df=cal_Cp(a_new,r,R,n,r_hub,v1)-cal_Cp(a,r,R,n,r_hub,v1)
        if df<0:
            deltaA = -deltaA
        a=a_new
        a_new=a+deltaA

        err=abs(df)
        print('err={}'.format(err))
        print(a_new)
        count+=1
        if count>300:
            print('break')
            break
    return a_new,cal_Cp(a_new,r,R,n,r_hub,v1)

def cal_a1(a,r,R,n,r_hub,v1):
    
    err=100
    deltaA=0.00001
    a1=random.random()
    a1_new=a1+deltaA
    count=0
    while err>0.001:
        
        df=(abs(cal_f(n,r,v1,R,r_hub,a,a1_new))-abs(cal_f(n,r,v1,R,r_hub,a,a1)))
        if df>0:
            deltaA = -deltaA

        a1=a1_new
        a1_new=a1+deltaA

        err=abs(cal_f(n, r, v1, R, r_hub, a, a1_new))

        count+=1
        if count>10e8:
            #print('break={}'.format(count))
            break
    
    return a1_new

def Newton():
    


    

if __name__ == '__main__':

    # a1=cal_a1(a=0.34,r=20,R=70,n=72,r_hub=2,v1=13)
    a,cp=cal_Cp2max(a=0.34,r=20,R=70,n=72,r_hub=2,v1=13)
    print(a,cp)
    #print(a1)
    # a11=[]
    # f11=[]
    # for a1 in range(0,30):
    #     a1=a1/1000
    #     f=cal_f(n=10,r=30,v1=13,R=40,r_hub=15,a=0.30,a1=a1)
    #     f11.append(f)
    #     a11.append(a1)
    
    # import numpy as np
    # from matplotlib import pyplot as plt

    # plt.plot(a11,f11)
    # plt.show()



