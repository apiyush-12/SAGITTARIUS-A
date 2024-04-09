import tkinter as tk
from PIL import ImageTk, Image
#import reading files for tle
import ReadingFile as rf
from satelites import Debris

window = tk.Tk()
window.geometry("300x400")
window.resizable(0,0)
window.title("Mapping Space Trash in Real Time")
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
    
tk.Button(window,command=lambda: get_grafica(satelite.get()), text = "Map", width=10, bg='#25387d', fg='white').place(x=110,y=300)

window.mainloop()