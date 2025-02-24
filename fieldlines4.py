import tkinter as tk
from tkinter import ttk
import turtle
import turtle as t
import random as r
import math as m
import ctypes
import os

def draw():
    no_of_electrons = slider1.get()
    no_of_protons = slider2.get()
    no_of_fieldlines = slider3.get()
    multi = slider4.get()  # Controls the space around the screen where te field lines generate
    g = slider5.get()  # Any constant. Acts as  an equivalent to k(9x10^-9) in electrostatics
    inaccuracy = slider6.get() / 1000  # Values higher than 0.05 cause the program to get stuck, failure rate becomes non-zero


    scr_width_2, scr_height_2 = scr_width * multi, scr_height * multi
    t.speed("fastest")

    oipo = 100
    t.pendown()
    t.goto(-scr_width+oipo,-scr_height+oipo)
    t.goto(scr_width-oipo,scr_height-oipo)
    window.update()
    canvas.update()
    cv.update()
    turtlecanvas.update()

    turtlecanvas.tracer(0, 0)
    progress_counter = 0
    electrons = []
    protons = []

    for i in range(no_of_protons):
        coordinates = [r.randint(-scr_width, scr_width), r.randint(-scr_height, scr_height)]
        protons.append(coordinates)

    for i in range(no_of_electrons):
        coordinates = [r.randint(-scr_width, scr_width), r.randint(-scr_height, scr_height)]
        electrons.append(coordinates)

    # Field lines from each proton
    for p in range(len(protons)):
        for counter in range(no_of_fieldlines):  # No. of field lines
            t.penup()
            t.goto(protons[p][0], protons[p][1])
            t.right(360 / no_of_fieldlines)  # 360 degrees / no. of field lines
            t.forward(1)
            t.pendown()
            h, k = t.pos()
            while (-scr_width_2) < h < scr_width_2 and (-scr_height_2) < k < scr_height_2:
                h, k = t.pos()
                i, j = fnet(h, k, electrons, protons, g)
                near_electron = False
                for o in range(len(electrons)):
                    if m.fabs(h - electrons[o][0]) < 1 and m.fabs(k - electrons[o][1]) < 1:
                        near_electron = True
                        break
                if near_electron is True:
                    break
                if m.fabs((inaccuracy * j) / m.fabs(i)) < 10:
                    if i > 0:
                        t.goto(h + inaccuracy, k + ((inaccuracy * j) / m.fabs(i)))
                    if i < 0:
                        t.goto(h - inaccuracy, k + ((inaccuracy * j) / m.fabs(i)))
                else:
                    if i > 0:
                        t.goto(h + inaccuracy, (k + sgn(j) * 10))
                    if i < 0:
                        t.goto(h - inaccuracy, (k + sgn(j) * 10))
            progress_counter += 1
            progress_bar(progress_counter, no_of_fieldlines, no_of_protons)


def fnet(x, y, electrons, protons, g):  # Net force at any point
    fi_net = 0
    fj_net = 0
    for q in range(len(protons)):
        relative_x = x - protons[q][0]  # position of the pen in the x - direction w.r.t the pen
        relative_y = y - protons[q][1]  # position of the pen in the y - direction w.r.t the pen
        f = g / (relative_x ** 2 + relative_y ** 2)  # magnitude of the net force exerted at that point, only by x1, y1
        fi_net += relative_x / (m.fabs(relative_x) + m.fabs(relative_y)) * f  # x - component of that force
        fj_net += relative_y / (m.fabs(relative_x) + m.fabs(relative_y)) * f  # y - component of that force
    for q in range(len(electrons)):
        relative_x = x - electrons[q][0]  # position of the pen in the x - direction w.r.t the pen
        relative_y = y - electrons[q][1]  # position of the pen in the y - direction w.r.t the pen
        f = -g / (relative_x ** 2 + relative_y ** 2)  # magnitude of the net force exerted at that point, only by x1, y1
        fi_net += relative_x / (m.fabs(relative_x) + m.fabs(relative_y)) * f  # x - component of that force
        fj_net += relative_y / (m.fabs(relative_x) + m.fabs(relative_y)) * f  # y - component of that force
    return fi_net, fj_net


def sgn(x):  # Typical mathematical sgn function
    if x != 0:
        sign = m.fabs(x) / x
    else:
        sign = 0
    return sign


def progress_bar(progress_no, no_of_fieldlines, no_of_protons):
    progress = m.floor((progress_no / (no_of_fieldlines * no_of_protons)) * 100)
    progressbar['value'] = progress
    right_panel.update()
    done_label['text'] = "{}%".format(progress)
    if progress == 100:
        done_label['text'] = "Done!"
        button.configure(command= restart)

def restart():
    turtlecanvas.clearscreen()
    draw()


# Setup
user32 = ctypes.windll.user32


# Initializing tkinter
window = tk.Tk()
window.title("Field Lines")
window.attributes('-fullscreen',True)


# Creating the main window
canvas = tk.Canvas(window, width=user32.GetSystemMetrics(78), height=user32.GetSystemMetrics(79))
canvas.grid(row=0, column=0, padx=10, pady=10)

# Creating a right panel
right_panel = tk.Frame(window)
right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nes")

# Create sliders
slider1_label = tk.Label(right_panel, text="No. of electrons:")
slider1_label.grid(row=0, column=0, sticky="w")
slider1 = tk.Scale(right_panel, from_=0, to=10, orient=tk.HORIZONTAL)
slider1.grid(row=0, column=1, padx=10)
slider1.set(2)

slider2_label = tk.Label(right_panel, text="No. of protons:")
slider2_label.grid(row=1, column=0, sticky="w")
slider2 = tk.Scale(right_panel, from_=1, to=10, orient=tk.HORIZONTAL)
slider2.grid(row=1, column=1, padx=10)
slider2.set(3)

slider3_label = tk.Label(right_panel, text="No. of fieldlines:")
slider3_label.grid(row=2, column=0, sticky="w")
slider3 = tk.Scale(right_panel, from_=18, to=72, orient=tk.HORIZONTAL)
slider3.grid(row=2, column=1, padx=10)
slider3.set(36)

slider4_label = tk.Label(right_panel, text="Simulation Area Multiplier:")
slider4_label.grid(row=3, column=0, sticky="w")
slider4 = tk.Scale(right_panel, from_=1, to=5, orient=tk.HORIZONTAL)
slider4.grid(row=3, column=1, padx=10)
slider4.set(2)

slider5_label = tk.Label(right_panel, text="Force Constant:")
slider5_label.grid(row=4, column=0, sticky="w")
slider5 = tk.Scale(right_panel, from_=1, to=200, orient=tk.HORIZONTAL)
slider5.grid(row=4, column=1, padx=10)
slider5.set(10)

slider6_label = tk.Label(right_panel, text="Inaccuracy:")
slider6_label.grid(row=5, column=0, sticky="w")
slider6 = tk.Scale(right_panel, from_=1, to=50, orient=tk.HORIZONTAL)
slider6.grid(row=5, column=1, padx=10)
slider6.set(50)

# Create checkbox
progressbar = ttk.Progressbar(right_panel, orient= tk.HORIZONTAL, length=200)
progressbar.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

done_label = tk.Label(right_panel, text="")
done_label.grid(row=6, column=1, padx=10, pady=10, sticky="e")

button = ttk.Button(right_panel, text="Draw", command=draw)
button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")

exit_button = ttk.Button(right_panel, text="Exit", command=exit)
exit_button.grid(row=7, column=1, columnspan=2, padx=10, pady=10, sticky="e")

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
right_panel.grid_rowconfigure(0, weight=1)
right_panel.grid_rowconfigure(1, weight=1)
right_panel.grid_rowconfigure(2, weight=1)
right_panel.grid_rowconfigure(3, weight=1)
right_panel.grid_rowconfigure(4, weight=1)
right_panel.grid_rowconfigure(5, weight=1)

# Turtle canvas
window.update()
cv = tk.Canvas(canvas,width=int(user32.GetSystemMetrics(78))-right_panel.winfo_width(), height=user32.GetSystemMetrics(79))
cv.grid(row=0, column=0, padx=10, pady=10, sticky = "news")
cv.update()
scr_width, scr_height = int((window.winfo_width() - right_panel.winfo_width()) / 2), int((window.winfo_height() - 10)/ 2)
print(scr_width, scr_height)
turtlecanvas = t.TurtleScreen(cv)
print(turtlecanvas.screensize())
t = t.RawTurtle(turtlecanvas)
# t.hideturtle()
turtlecanvas.clearscreen()
window.update()
window.update_idletasks()


tk.mainloop()
