import os
from cal_funtion import main_cal,cal_a1_for_draw,cal_CPmax_for_draw
import matplotlib.pyplot as plt
import numpy as np
from plot2D3D import draw3D,draw2D


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

    #-----------------------------draw3D---------------------------------------
    draw3D=True
    if draw3D:
        r=3
        a=0.35

        a1_all,f_all,a1_iter_list,f_iter_list=cal_a1_for_draw(a,r,R,n,r_hub,v1)
        draw2D(X=a1_all,Y=f_all,x=a1_iter_list,y=f_iter_list)

        a_all,a1_all,Cp_all,a_iter_list,a1_iter_list,Cp_iter_list=cal_CPmax_for_draw(r,R,n,r_hub,v1)
        draw3D(X=a_all,Y=a1_all,Z=Cp_all,x=a_iter_list,y=a1_iter_list,z=Cp_iter_list)

    


    





