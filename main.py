import random
from math import acos, atan, e, pi, sin
from matplotlib import pyplot as plt




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
    da=0.0001
    a=random.random()
    learning_rate=0.001

    while True:
        dCp=(cal_Cp(a+da,r,R,n,r_hub,v1)-cal_Cp(a,r,R,n,r_hub,v1))/da

        a_new = a + dCp * learning_rate
        err=abs(a_new-a)  
        #print('err={}'.format(err))   
        if err<1e-6:
            break
        else:
            a=a_new
            #print("a={}".format(a_new))

    return a_new,cal_a1(a_new,r,R,n,r_hub,v1),cal_Cp(a_new,r,R,n,r_hub,v1)


# def cal_Cp2max(a,r,R,n,r_hub,v1):
    
#     err=100
#     deltaA=0.0001

#     count=0
#     a_new=a+deltaA
#     while err>0.00001:
        
#         df=cal_Cp(a_new,r,R,n,r_hub,v1)-cal_Cp(a,r,R,n,r_hub,v1)

#         if df<0:
#             deltaA = -deltaA
#         a=a_new
#         a_new=a+deltaA

#         err=abs(df)
#         print('err={}'.format(err))
#         print(a_new)
#         count+=1
#         if count>300:
#             print('break')
#             break
#     return a_new,cal_Cp(a_new,r,R,n,r_hub,v1)

# def cal_a1(a,r,R,n,r_hub,v1):
#     dx=1e-6
#     err=1000
#     a1=0
#     while err>1e-6:
#         dy=(cal_f(n,r,v1,R,r_hub,a, a1+dx)-cal_f(n,r,v1,R,r_hub,a, a1))/dx
#         a1=a1-cal_f(n,r,v1,R,r_hub,a, a1)/(dy+1e-8)
#         err=abs(cal_f(n,r,v1,R,r_hub,a, a1))
#     #print("a1={0:8.4f}".format(a1))
#     return a1

# def cal_CPmax(r,R,n,r_hub,v1):
#     err=100
#     da=0.0001
#     a=random.random()
#     #count=0
#     learning_rate=0.001

#     while True:
#         dCp=(cal_Cp(a+da,r,R,n,r_hub,v1)-cal_Cp(a,r,R,n,r_hub,v1))/da

#         a_new = a + dCp * learning_rate
#         err=abs(a_new-a)  
#         print('err={}'.format(err))   
#         if err<1e-4:
#             break
#         else:
#             a=a_new
#             print("a={}".format(a_new))
#         # count+=1
#         # if count>300:
#         #     print('break')
#         #     break
#     return a_new,cal_Cp(a_new,r,R,n,r_hub,v1)
if __name__ == '__main__':

    rlist=[]
    alist=[]
    Cplist=[]
    a1list=[]

    for i in range(4,72,4):
        a,a1,cp=cal_CPmax(r=i,R=70,n=72,r_hub=2,v1=13)
        rlist.append(i)
        alist.append(a)
        a1list.append(a1)
        
        print("r={3},a={0},a1={1},cp={2}".format(a,a1,cp,i))

    plt.plot(rlist,a1list)
    plt.show()
    

    





