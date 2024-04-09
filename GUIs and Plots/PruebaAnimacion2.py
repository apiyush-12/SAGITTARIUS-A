import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

satellites_values = [[1.0, 2.0, 0.50, 0.0, 30.0, 0.0], [1.0, 1.0, 0.20, 0.0, 90.0, 0.0], [10.0, 2.0, 0.39, 0.0, 180.0, 0.0]]
satellites_pos = []
red_dots_pos = []
fig = plt.figure()
ax = p3.Axes3D(fig)
anim = []

def animate(i, pos, red_dot):
    red_dot.set_data([pos[i][1], pos[i][0]])
    red_dot.set_3d_properties(pos[i][2])
    return red_dot,

def create_system(satellites_list):
    for satellite in satellites_list:
        t = np.linspace(0, 4, 200)
        orbit = pyasl.KeplerEllipse(a=satellite[0], per=satellite[1], e=satellite[2], Omega=satellite[3], i=satellite[4], w=satellite[5])
        pos = orbit.xyzPos(t)
        red_dot, = ax.plot(pos[::, 1], pos[::, 0], pos[::, 2], 'ro')
        anim.append(animation.FuncAnimation(fig, animate, 200, fargs=(pos, red_dot),
                              interval=100, blit=False))
        ax.plot(pos[::, 1], pos[::, 0], pos[::, 2], 'k-')        

create_system(satellites_values)
ax.plot([0], [0], [0], 'bo', markersize=9, label="Earth")

# Hide grid lines
ax.grid(False)

# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
plt.style.use('default')
plt.legend()
plt.show()