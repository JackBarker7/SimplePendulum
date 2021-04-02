import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from vpython import *
from time import sleep

mainScene =canvas(title = "Simple Pendulum", height = 700, width = 1000, background = color.green, align = "left")
mainScene.camera.pos = vector(0, -0.5, 0)
pi = np.pi
#constants:
m=1
L=1
b=0.5 #damping
g=9.81
dt = 0.02
tmax = 20
theta1_0 = pi/2
theta2_0=0.
theta_init = (theta1_0, theta2_0)

t=np.linspace(0, tmax, tmax/dt) #array with all times

def int_pendulum_sim(theta_init, t, L=L, m=m, b=b, g=g):
    '''returns values for theta1_dot and theta2_dot'''
    theta1_dot = theta_init[1] #theta 2
    theta2_dot = -(b/m)*theta_init[1] - (g/L)*np.sin(theta_init[0])
    return theta1_dot, theta2_dot

theta_vals_int = integrate.odeint(int_pendulum_sim, theta_init, t) #performs integration to get values

theta=np.zeros(int(tmax/dt))
omega=np.zeros(int(tmax/dt))


def graphing(theta, omega, timestamps):
    for i in range(int(tmax/dt)):
        theta[i] = theta_vals_int[i][0]
        omega[i] = theta_vals_int[i][1]

    plt.plot(t,theta, color="red", label = "angle")
    plt.plot(t,omega, color="blue", label = "angular velocity")
    leg = plt.legend(loc = "lower right", frameon = False)
    plt.show()



def animate():
    #puts theta and omega values into separate arrays
    for i in range(int(tmax/dt)):
        theta[i] = theta_vals_int[i][0]
        omega[i] = theta_vals_int[i][1]
    #sets up GPE and KE graphs
    gd = graph(title = "energy graph", 
                  ytitle = "Energy (J)", 
                  xtitle = "Time (s)",
                  align = "right")
    gpe_graph = gcurve(color = color.red, label = "GPE")
    ke_graph = gcurve(color = color.blue, label = "KE")

    #sets up ball, rod and data labels
    rod = curve(vector( (L*np.sin(theta1_0)), (-L*np.cos(theta1_0)), 0 ), vector(0,0,0), color = color.red)
    ball = sphere(pos = vector( (L*np.sin(theta1_0)), (-L*np.cos(theta1_0)), 0 ),
                  radius = 0.1, color = color.blue)

    angle_label = label(pos = vector(-1,0,0), text = "Angle:")
    omega_label = label(pos = vector(1,0,0), text = "Angular Velocity:")
    sleep(0.5)

    #moves line and ball
    for i in range(int(tmax/dt)):
        angle = theta[i]
        angv = omega[i]
        xpos = L*np.sin(angle)
        ypos = -L*np.cos(angle)
        

        rod.modify(0, pos = vector(xpos, ypos, 0))
        ball.pos = vector(xpos, ypos, 0)

        #changes label values
        angle_label.text = "Angle: "+str(np.around(angle, 2))
        omega_label.text = "Angular Velocity: "+str(np.around(angv, 2))

        #plots GPE and KE graphs
        gpe_graph.plot(t[i], m*g*(L-L*np.cos(angle)))
        ke_graph.plot(t[i], 0.5*m*(L**2)*(angv**2))

        sleep(dt)

    label(pos = vector(0,0,0), text = "Finished") #label that appears when programme has finished

animate()
graphing(theta, omega, t)

