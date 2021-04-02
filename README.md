# SimplePendulum - Python Simple Pendulum Simulation with Damping
Numerically solves the pendulum 2nd order differential equation 

![equation](https://latex.codecogs.com/gif.latex?\frac{d^2\theta}{dt^2}&space;&plus;&space;\frac{b}{m}\frac{d\theta}{dt}=-\frac{g}{l}\sin{\theta})

Using `scipy.integrate.odeint`. Results are then used to generate an animation using `vpython`, or to generate a graph of anglular displacement and velocity against time using `matplotlib`.
