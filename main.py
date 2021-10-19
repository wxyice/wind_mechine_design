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

def Cp(a,a1,F,lamda):
    """
    :param: a 轴向干涉因子
    a1 周向干涉因子
    F  总损失系数
    lamda 当地叶尖速比
    """
    Cp=4*(1-a)*a1*F*lamda**2
    return Cp

def cal_phi(a,a1,lamda):
    phi=atan((1-a)/(lamda*(1+a1)))
    return phi

def cal_f(n,r,v1,R,r_hub,a,a1):
    lamda=(n*pi/60)*r/v1
    phi=cal_phi(a,a1,lamda)
    F=cal_F(r,R,n,r_hub,phi)
    f=a1*(1+a1)*lamda-(a*(1-a*F))
    print('fff={}'.format(f))
    return f

def cal_a1(a,r,R,n,r_hub,v1):
    
    err=100
    deltaA=0.0001
    a1=random.random()*10
    a1_new=a1+deltaA

    count=0
    while err>0.001:
        
        df=(cal_f(n,r,v1,R,r_hub,a,a1_new)-cal_f(n,r,v1,R,r_hub,a,a1))
        if df<0:
            deltaA = -deltaA

        print('-'*50)
        print(cal_f(n,r,v1,R,r_hub,a,a1_new))
        print(cal_f(n,r,v1,R,r_hub,a,a1))
        print(df)
        print(df/abs(df))
        print('-'*50)

        a1=a1_new
        a1_new=a1+deltaA
        print(cal_f(n, r, v1, R, r_hub, a, a1_new))
        err=abs(cal_f(n, r, v1, R, r_hub, a, a1_new))
        #err=a1_new-a1
        print(a1)
        count+=1
        if count>300:
            print('break')
            break
    
    return a1_new




    

if __name__ == '__main__':

    a1=cal_a1(a=0.34,r=20,R=70,n=72,r_hub=2,v1=13)
    print(a1)

