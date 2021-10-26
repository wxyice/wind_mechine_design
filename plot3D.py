import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def update_line3D(frame, line, x, y, z):
    frame = int(frame)
    print(frame)
    line.set_data(x[:frame], y[:frame])
    line.set_3d_properties(z[:frame])
    return line

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
    line_ani = animation.FuncAnimation(fig, update_line3D, frames=len(Z), fargs=(line, x, y, z), interval=200, blit=False, repeat=False)
    line_ani.save('test.gif', writer='pillow')

    plt.show()

def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

if __name__ == '__main__':
    
    x = np.linspace(-6,6,30)
    y = np.linspace(-6,6,30)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    z = f(x, y)
    draw3D(X=X, Y=Y, Z=Z, x=x, y=y, z=z)