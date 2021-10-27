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

def update_line3D(frame, line, x, y, z):
    frame = int(frame)
    line.set_data(x[:frame], y[:frame])
    line.set_3d_properties(z[:frame])
    return line

def update_point2D(frame, point, x, y):
    frame = int(frame)
    point.set_data(x[:frame], y[:frame])
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
    # ax.set_xlabel('a')

    # ax.set_ylim3d([0.0, 1.0])
    # ax.set_ylabel('a\'')

    # ax.set_zlim3d([0.0, 1.0])
    # ax.set_zlabel('Z')pangzhentao biexuele kuaihuilaiba

    ax.set_title('3D Test')
    line = ax.plot([], [], 'r-', animated=False, linewidth=3.0)[0]

    # Creating the Animation object
    line_ani = animation.FuncAnimation(fig, update_line3D, frames=len(z), fargs=(line, x, y, z), interval=200, blit=False, repeat=False)
    line_ani.save('3D.gif', writer='pillow')

    plt.show()

    return print('-------------------------------------------Drawing 3D finished!!!------------------------------------------')

def draw2D(X=[], Y=[], x=[], y=[]):


    fig, ax = plt.subplots()
    ax.plot(X, Y)  # Draw 2d
    
    # Setting the axes properties
    # ax.set_xlim3d([0.0, 1.0])
    # ax.set_xlabel('a')

    # ax.set_ylim3d([0.0, 1.0])
    # ax.set_ylabel('a\'')

    point = ax.plot([], [], 'r-', animated=False, linewidth=3.0)[0]

    # Creating the Animation object
    point_ani = animation.FuncAnimation(fig, update_point2D, frames=len(y), fargs=(point, x, y), interval=600, blit=False, repeat=False)
    point_ani.save('2D.gif', writer='pillow')

    plt.show()

    return print('-------------------------------------------Drawing 2D finished!!!-------------------------------------------')




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