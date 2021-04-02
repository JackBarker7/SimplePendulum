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

g=9.81
dt = 0.02
tmax = 20
theta1_0 = pi/6
theta_init = (theta1_0, 0.)

toplot = 4 # 0 for gpe, 1 for ke, 2 for both, 3 for divergence from real, 4 for total energy

t=np.linspace(0, tmax, tmax/dt) #array with all times

def regular_pendulum(theta_init, t, L=L, m=m, g=g):
    '''returns values for theta1_dot and theta2_dot'''
    theta1_dot = theta_init[1] #theta 2
    theta2_dot = -(g/L)*np.sin(theta_init[0])
    return theta1_dot, theta2_dot

real_vals = integrate.odeint(regular_pendulum, theta_init, t) #performs integration to get values

#generates values using small angle approximation
approx_thetas = theta1_0*np.cos(np.sqrt(g/L)*t)
approx_omegas = -theta1_0*np.sqrt(g/L)*np.sin(np.sqrt(g/L)*t)

theta=np.zeros(((int(tmax/dt)), 2))
omega=np.zeros(((int(tmax/dt)), 2))

def animate():
    #puts theta and omega values into separate arrays
    for i in range(int(tmax/dt)):
        theta[i][0] = real_vals[i][0]
        omega[i][0] = real_vals[i][1]
        theta[i][1] = approx_thetas[i]
        omega[i][1] = approx_omegas[i]

    #sets up GPE and KE graphs
    gd = graph(title = "energy graph", 
                  ytitle = "Energy (J)", 
                  xtitle = "Time (s)",
                  align = "right")

    if toplot == 0:
        real_gpe_graph = gcurve(color = color.red, label = "Real GPE")
        approx_gpe_graph = gcurve(color = color.purple, label = "Approx GPE")
    
    elif toplot == 1:
        real_ke_graph = gcurve(color = color.orange, label = "Real KE")
        approx_ke_graph = gcurve(color = color.blue, label = "Approx KE")

    elif toplot == 2:
        real_gpe_graph = gcurve(color = color.red, label = "Real GPE")
        approx_gpe_graph = gcurve(color = color.purple, label = "Approx GPE")
        real_ke_graph = gcurve(color = color.orange, label = "Real KE")
        approx_ke_graph = gcurve(color = color.blue, label = "Approx KE")

    elif toplot == 3:
        gpe_divergence_graph = gcurve(color = color.red, label = "GPE Divergence")
        ke_divergence_graph = gcurve(color = color.blue, label = "KE Divergence")
        total_divergence_graph = gcurve(color = color.green, label = "Total Divergence")

    elif toplot == 4:
        real_total_graph = gcurve(color = color.red, label = "Real Total Energy")
        approx_total_graph = gcurve(color = color.blue, label = "Approx Total Energy")

    #sets up ball and rod 
    real_rod = curve(vector( (L*np.sin(theta1_0)), (-L*np.cos(theta1_0)), 0 ), vector(0,0,0), color = color.red)
    real_ball = sphere(pos = vector( (L*np.sin(theta1_0)), (-L*np.cos(theta1_0)), 0 ),
                  radius = 0.1, color = color.red)

    approx_rod = curve(vector( (L*np.sin(theta1_0)), (-L*np.cos(theta1_0)), 0 ), vector(0,0,0), color = color.blue)
    approx_ball = sphere(pos = vector( (L*np.sin(theta1_0)), (-L*np.cos(theta1_0)), 0 ),
                  radius = 0.1, color = color.blue)

    sleep(0.5)

    #moves line and ball
    for i in range(int(tmax/dt)):
        angles = theta[i]
        angvs = omega[i]
        xposs = L*np.sin(angles)
        yposs = -L*np.cos(angles)
        
        real_rod.modify(0, pos = vector(xposs[0], yposs[0], 0))
        real_ball.pos = vector(xposs[0], yposs[0], 0)

        approx_rod.modify(0, pos = vector(xposs[1], yposs[1], 0))
        approx_ball.pos = vector(xposs[1], yposs[1], 0)


        #plots GPE and KE graphs
        real_gpe = m*g*(L-L*np.cos(angles[0]))
        real_ke = 0.5*m*(L**2)*(angvs[0]**2)
        approx_gpe = m*g*(L-L*np.cos(angles[1]))
        approx_ke = 0.5*m*(L**2)*(angvs[1]**2)
        gpe_divergence = approx_gpe - real_gpe
        ke_divergence = approx_ke - real_ke

        if toplot == 0:
            real_gpe_graph.plot(t[i], real_gpe)
            real_ke_graph.plot(t[i], real_ke)
        
        elif toplot == 1:
            approx_gpe_graph.plot(t[i], approx_gpe)
            approx_ke_graph.plot(t[i], approx_ke)

        elif toplot == 2:
            real_gpe_graph.plot(t[i], real_gpe)
            real_ke_graph.plot(t[i], real_ke)
            approx_gpe_graph.plot(t[i], approx_gpe)
            approx_ke_graph.plot(t[i], approx_ke)

        elif toplot == 3:
            gpe_divergence_graph.plot(t[i], gpe_divergence)
            ke_divergence_graph.plot(t[i], ke_divergence)
            total_divergence_graph.plot(t[i], gpe_divergence+ke_divergence)

        elif toplot == 4:
            real_total_graph.plot(t[i], real_gpe+real_ke)
            approx_total_graph.plot(t[i], approx_gpe+approx_ke)


        sleep(dt)

    label(pos = vector(0,0,0), text = "Finished") #label that appears when programme has finished

animate()


