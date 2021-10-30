import os,shutil
from math import sqrt,atan,cos,sin,pi
import numpy as np
from cal_funtion import main_cal

def cal_model_xyr(path,X,Y,l,beta,r):
    x,y=[],[]
    for x0,y0 in zip(X,Y):
        C=l*sqrt(x0**2+y0**2)
        try:
            phi1=atan(y0/x0)
        except ZeroDivisionError:
            phi1=0
        x.append(C*cos(phi1+beta))
        y.append(C*sin(phi1+beta))
    rlist=[r for i in range(len(X))]
    with open(os.path.join(path,'24112_{0:6.4f}_tan.txt'.format(r)),'w') as f:
        for xi,yi,ri in zip(x,y,rlist):
            f.write('{0}\t{1}\t{2}\n'.format(xi,yi,ri))
    print('24112_{0:6.4f} done'.format(r))

def cal_martix(path,X,Y,l,beta,r):

    M=np.array([[cos(beta),-sin(beta)],[sin(beta),cos(beta)]])
    V=[np.array([x,y]) for x,y in zip(X,Y)]
    #V=np.reshape(V,(-1,2))
    NewV=[]
    for v in V:
        v=v*l
        NewV.append(np.matmul(M,v).tolist())
        #print(NewV.tolist())
    rlist=[1000*r for i in range(len(X))]
    with open(os.path.join(path,'24112_{0:6.4f}.txt'.format(r)),'w') as f:
        for (xi,yi),ri in zip(NewV,rlist):
            f.write('{0}\t{1}\t{2}\n'.format(xi,yi,ri))
    print('24112_{0:6.4f} done'.format(r))

def read_model_base(path):

    with open(path,'r') as f:
        allline=f.readlines()
        X,Y=[],[]
        for line in allline:
            line=line[:-1].split('\t')
            for i in range(len(line)):
                try:
                    line.remove('')
                except ValueError:
                    break
            #line.pop(len(line)-1)
            X.append(float(line[0]))
            Y.append(float(line[1]))
            # print(line,X[-1],Y[-1])
    return X,Y

if __name__ == '__main__':
     # 基本参数数据
    R=12.7      # m
    r_hub=0.3   # m
    v1=13       # m/s
    n=72/60     # 圈/s

    # case名称,保存路径
    name='test1'
    path='result'

    if os.path.exists(path)==False:
        os.mkdir(path)

    value=main_cal(R,r_hub,v1,n,step=25)

    rlist,alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W,alpha=value
    #value=[alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W,alpha]
    # r=0
    # l=1.4
    # beta=7.5*pi/180

    path='model_arg2'
    model_base_path='24112.txt'
    X,Y=read_model_base(model_base_path)
    X=[1000*x for x in X]
    Y=[1000*y for y in Y]
    
    if os.path.exists(path)!=True:
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)
    
    betalist=((np.array(philist)-np.array(alpha))*np.pi/180).tolist()

    for r,l,beta in zip(rlist,llist,betalist):
        cal_martix(path,X,Y,l,beta,r)

