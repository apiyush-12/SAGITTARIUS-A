import tkinter as tk
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np
from sgp4.api import Satrec, jday
from datetime import datetime
from scipy.integrate import ode
import mpl_toolkits.mplot3d.axes3d as p3
import ReadingFile as rf

# gravitational constant
G_meters = 6.67430e-11       # m**3 / kg / s**2
G = G_meters * 10**-9 # km**3/ kg / s**2
#CONSTS
EARTH_MU = 5.972e24 * G

class Debris(object):
    def __init__(self, s, t):
        self.t = t
        self.s = s
        self.satellite = Satrec.twoline2rv(s, t)
        self.trayectory = []

    def propagar(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        now = now.split()
        year, month, day = now[0].split('-')
        hour, minute, seconds = now[1].split(':')
        self.jd, self.fr = jday(int(year), int(month), int(day), int(hour), int(minute), int(seconds))
        e, self.position, self.velocity = self.satellite.sgp4(self.jd, self.fr)
        return self.position, self.velocity

    def two_body(self, t, y, mu=EARTH_MU):
        rx, ry, rz, vx, vy, vz = y
        r = np.array([rx, ry, rz])
        norm_r = np.linalg.norm(r)
        ax, ay, az = r * mu / norm_r**3
        return [vx, vy, vz, ax, ay, az]

    def get_trayectory(self, tspan=100.0*60.0, dt=100.0, mu=EARTH_MU):
        r0 = [*self.position]
        v0 = [*self.velocity]
        n_steps = int(np.ceil(tspan / dt))
        ys = np.zeros((n_steps, 6))
        ts = np.zeros((n_steps, 1))
        y0 = r0 + v0
        ys[0] = np.array(y0)
        step = 1
        solver = ode(self.two_body)
        solver.set_integrator('lsoda')
        solver.set_initial_value(y0, 0)
        solver.set_f_params(mu)
        while step < n_steps:
            solver.integrate(solver.t + dt)
            ts[step] = solver.t
            ys[step] = solver.y
            step += 1
        self.rs = ys[:, :3]
        return self.rs

    def animate(self, i):
        self.propagar()
        self.pos = self.get_trayectory()
        self.pos = self.pos[-1:]
        self.last_pos = self.pos[-1]
        self.trayectory.append(self.last_pos.tolist())
        self.trayectory_f = np.asarray(self.trayectory)

# Initialize Tkinter window
window = tk.Tk()
window.geometry("600x600")
window.title("Mapping Space Trash")

# Load and display satellite image
sat_image = Image.open("sat.png")
sat_photo = ImageTk.PhotoImage(sat_image)
sat_label = tk.Label(window, image=sat_photo)
sat_label.pack()

# Create matplotlib figure for 3D animation
fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)
ax.set_axis_off()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Read debris data
info = rf.ReadFile('IRIDIUM33.txt')
debris = [Debris(*line) for line in info]

# Define animation function
def animate(i):
    ax.clear()
    ax.set_axis_off()
    ax.grid(False)
    ax.plot([0], [0], [0], 'bo', markersize=9, label="Earth")
    for d in debris:
        d.animate(i)
        ax.plot(d.trayectory_f[::, 0], d.trayectory_f[::, 1], d.trayectory_f[::, 2], 'w--')

# Start animation
ani = animation.FuncAnimation(fig, animate, interval=1000)

# Run Tkinter event loop
window.mainloop()
