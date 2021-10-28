# =====================================================
# 1.坐标轴选项调节注释的Setting the axes properties
# 2.animation.FuncAnimation(fig, update_line3D, frames=len(z), fargs=(line, x, y, z), interval=200, blit=False, repeat=False)
# interval为步进间隔，单位ms，是否重复播放repeat
# 3.大写XYZ为需要输入的全部图像的数据，小写xyz为迭代过程中产生的数据
# =====================================================

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


p3.rcParams['font.sans-serif'] = ['FangSong']
p3.rcParams['axes.unicode_minus']=False #用来正常显示负号

def update_line3D(frame, line,time_text,point_2,x, y, z):
    frame = int(frame)
    line.set_data(x[:frame+1], y[:frame+1])
    line.set_3d_properties(z[:frame+1])
    time_text.set_text('iter = {0}'.format(frame))
    point_2.set_data(x[:frame+1], y[:frame+1])
    point_2.set_3d_properties(z[:frame+1])
    return line

def update_point2D(frame, point,time_text,point_2,x, y):
    frame = int(frame)
    point.set_data(x[:frame+1], y[:frame+1])
    time_text.set_text('iter = {0}'.format(frame))
    point_2.set_data(x[:frame+1], y[:frame+1])
    
    return point


def draw3D(X=[], Y=[], Z=[], x=[], y=[], z=[]):
    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    
    # Setting Cp
    # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')  # 绘制3d面
    ax.plot_wireframe(X, Y, Z, color='c', linewidth=0.3)  # 绘制3d网格

    # Setting the axes properties
    # ax.set_xlim3d([0.0, 1.0])
    ax.set_xlabel('a',fontsize=15)

    # ax.set_ylim3d([0.0, 1.0])
    ax.set_ylabel('a\'',fontsize=15)

    # ax.set_zlim3d([0.0, 1.0])
    ax.set_zlabel('Cp',fontsize=15)# pangzhentao biexuele kuaihuilaiba

    ax.set_title('梯度下降Cp优化过程')
    line = ax.plot([], [], 'r-', animated=False, linewidth=3.0)[0]
    point_2=ax.plot([],[],'r*', animated=False, markersize=8)[0]
    time_text = ax.text(0.07, 0.5 ,14,'',fontsize=20,horizontalalignment='left',verticalalignment='top', transform=ax.transAxes) 

    # Creating the Animation object
    line_ani = animation.FuncAnimation(fig, update_line3D, frames=len(z), fargs=(line,time_text,point_2,x, y, z), interval=200, blit=False, repeat=True)
    line_ani.save('3D2.gif', writer='pillow')

    #plt.show()

    print('-------------------------------------------Drawing 3D finished!!!------------------------------------------')

def draw2D(X=[], Y=[], x=[], y=[]):


    fig, ax = plt.subplots()
    ax.plot(X, Y)  # Draw 2d
    
    # Setting the axes properties
    #ax.set_xlim([0.0, 3.0])
    ax.set_xlabel('a\'',fontsize=15)

    #ax.set_ylim([0.0, 35])
    #ax.set_ylabel('f',fontsize=15)
    

    ax.set_title('Newton迭代求解过程')

    point = ax.plot([], [], 'r-', animated=False, linewidth=1.0)[0]
    point_2=ax.plot([],[],'r*', animated=False, markersize=15)[0]
    time_text = ax.text(0.07, 0.9,'',fontsize=20,horizontalalignment='left',verticalalignment='top', transform=ax.transAxes) 

    # Creating the Animation object
    point_ani = animation.FuncAnimation(fig, update_point2D, frames=len(y), fargs=(point,time_text,point_2,x, y), interval=600, blit=False, repeat=False)
    point_ani.save('N12.gif', writer='pillow')

    #plt.show()

    print('-------------------------------------------Drawing 2D finished!!!-------------------------------------------')




if __name__ == '__main__':
    def f(x, y):
            return np.sin(np.sqrt(x ** 2 + y ** 2))
    # Code testing
    x = np.linspace(-6,6,30)
    y = np.linspace(-3,9,30)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    z = f(x, y)
    # draw3D(X=X, Y=Y, Z=Z, x=x, y=y, z=z)
    # draw2D(X=X, Y=Y, x=x, y=y)