from matplotlib.pyplot import step
from numpy.linalg import norm
from sgp4.api import Satrec
from sgp4.api import jday
from datetime import datetime
from scipy.integrate import ode
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import ReadingFile as rf

#CONSTS
# gravitational constant
G_meters = 6.67430e-11       # m**3 / kg / s**2
G = G_meters * 10**-9 # km**3/ kg / s**2
EARTH_EQUATORIAL_RADIUS = 6378.135  # equatorial radius
EARTH_FLATTENING_CONSTANT = 1 / 298.26
GEO_SYNC_RADIUS = 42164.57
EARTH_MU=5.972e24 * G

class Debris(object):
    def __init__(self,s,t):
        self.t=t
        self.s=s
        self.satellite = Satrec.twoline2rv(s, t)
        self.propagar
        self.get_trayectory
        self.trayectory=[]
    
    def propagar(self):
        #get actual date
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        now = now.split()
        #separar la fecha y la hora
        year,month,day=now[0].split('-')
        hour,minute,seconds=now[1].split(':')
        #get jd and fr from jday funcation
        self.jd, self.fr = jday(int(year),int(month),int(day),int(hour),int(minute),int(seconds))
        
        #get position and velocity based on jd and fr
        e, self.position, self.velocity = self.satellite.sgp4(self.jd, self.fr)
        
        return self.position,self.velocity
    def two_body(self,t,y,mu=EARTH_MU):
        rx,ry,rz,vx,vy,vz=y
        r=np.array([rx,ry,rz])
        #calc norm of r
        norm_r=np.linalg.norm(r)

        #two body aceleration
        ax,ay,az= r*mu/norm_r**3
        return [vx,vy,vz,ax,ay,az]
    
    def get_trayectory(self,tspan=100.0*60.0,dt=100.0,mu=EARTH_MU):
        #r0,v0=d.propagar()
        r0=[*self.position]
        v0=[*self.velocity]
        
        #number of steps
        n_steps=int(np.ceil(tspan/dt))
        ys=np.zeros((n_steps,6))
        ts=np.zeros((n_steps,1))

        #initial conditions
        y0=r0+v0
        ys[0]=np.array(y0)
        step=1

        #solver
        solver=ode(self.two_body)
        solver.set_integrator('lsoda')
        solver.set_initial_value(y0,0)
        solver.set_f_params(mu)

        while step<n_steps:
            solver.integrate(solver.t+dt)
            #print(solver.t,solver.y)
            ts[step]=solver.t
            ys[step]=solver.y
            step+=1

        self.rs=ys[:,:3]

        return self.rs
    def animate(self,i):
        self.propagar()
        self.pos = self.get_trayectory()
        self.pos = self.pos[-1:]
        
        self.last_pos = self.pos[-1]
        self.trayectory.append(self.last_pos.tolist())
        self.trayectory_f = np.asarray(self.trayectory)
        
        #ax.clear()
        ax.plot([0], [0], [0], 'bo', markersize=9, label="Earth")
        #ax.plot(self.pos[::, 0], self.pos[::, 1], self.pos[::, 2], 'ro')
        ax.plot(self.trayectory_f[::, 0], self.trayectory_f[::, 1], self.trayectory_f[::, 2], 'w--')
        
def graficar(info):
    #plot grafica
    plt.style.use('dark_background')
    fig = plt.figure()
    fig.set_facecolor('black')
    global ax
    ax = p3.Axes3D(fig)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    #ax.set_visible(False)

    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    debris=[]
    anim=[]
    for line in info: 
        debris.append(Debris(*line))
    for i in range(0, 15):
        try:
            anim.append(animation.FuncAnimation(fig, debris[i].animate, interval=1000, cache_frame_data=False))

        except:
            pass
    plt.axis('off')
    plt.show()    
    
#gui
import tkinter as tk
from PIL import ImageTk, Image


window = tk.Tk()
window.geometry("300x400")
window.resizable(0,0)
window.title("Mapping Space Trash")
ico = tk.PhotoImage(file = 'sat.png')
window.iconphoto(False, ico)

satimg = Image.open("sat.png")
test = ImageTk.PhotoImage(satimg)
lab1 = tk.Label(image=test)
lab1.image = test
lab1.place(x=100, y= 45)

lab2 = tk.Label(window, text='Select the debris you want to map').place(x=60, y=210)

satelites = [
    "COSMOS", 
    "FENGYUN", 
    "IRIDIUM33", 
    "MICROSAT"
    ]

satelite = tk.StringVar(window)
satelite.set(satelites[0])
sat_menu = tk.OptionMenu(window, satelite, *satelites)
sat_menu.place(x=100, y=250, width=100)


def get_grafica(name):
    
    info = rf.ReadFile(name + ".txt")
    graficar(info)
    
tk.Button(window,command=lambda: get_grafica(satelite.get()), text = "Map", width=10, bg='#25387d', fg='white').place(x=110,y=300)

window.mainloop()