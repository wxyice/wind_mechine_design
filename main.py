import os
from cal_funtion import main_cal,cal_phi,cal_F
import matplotlib.pyplot as plt
import numpy as np
from plot2D3D import draw3D,draw2D
from math import pi,e


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

    value=main_cal(R,r_hub,v1,n)

    rlist,alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W=value
    value=[alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W]

    save=False
    if save:
        #--------------------------save data as txt-------------------------

        with open(os.path.join(path,name+'.txt'),'w') as f:
            for i in range(len(rlist)):
                f.write("{0} ".format(rlist[i]))
                for j in value:
                    f.write("{0} ".format(j[i]))
                f.write('\n')

        list1=[rlist,alist,a1list,Flist,philist,Cplist,llist,sigmalist,av1list,omegarlist,W]
        
        #--------------------------save data as xls-------------------------------
        with open(os.path.join(path,name+'.xls'),'w',encoding='gbk') as output:
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



    


    





