
# MW 2022-03-23
# Python simulation of damped driven pendulum

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# time parameters 
dt = 0.01             # time step
dt2 = dt/2            # half time step
t = 0  	              # start time 

# initial conditions
theta = np.pi/2.   # initial angular position 
p = 0.                 # initial angular velocity

# model parameters (set m=g=L=1)
omega0 = 1           # natural frequency
omega02 = omega0**2       
gamma = 1          # damping coefficient
#omega = 2/3          # drive frequency
#A = 1.0              # amplitude of drive force

position = []         # list to store angular position
momentum = []         # list to store angular momentum

#spara amplituder och tiden för "turning point" (när p = 0)
amplitudes = []
turning_point_times = []

# set up the figure and the plot element to animate
fig = plt.figure(figsize=(10,10),dpi=80)
ax1 = plt.subplot(211, aspect='equal', autoscale_on=False, xlim=(-1.1,1.1), ylim=(-1.1,1.1))
pendulum, = ax1.plot([], [], c='r', lw=10)
ax1.axis('off')
ax2 = plt.subplot(212, aspect='equal', autoscale_on=False, xlim=(-np.pi, np.pi), ylim=(-3, 3))
phaseportrait, = ax2.plot([], [], 'bo', markersize=0.5)# c='black', lw=0)
ax2.set_xlabel(r'$\theta$')
ax2.set_ylabel(r'p')

def f(theta, p, t):
    accel = -omega02*np.sin(theta) # pendulum
    accel += -gamma*p              # damping  
    #accel += A*np.cos(omega*t)     # drive force
    return accel

def rk4(x, v, t):
    xk1 = dt*v
    vk1 = dt*f(x, v, t)
    xk2 = dt*(v+vk1/2)
    vk2 = dt*f(x+xk1/2, v+vk1/2, t+dt/2)
    xk3 = dt*(v+vk2/2)
    vk3 = dt*f(x+xk2/2, v+vk2/2, t+dt/2)
    xk4 = dt*(v+vk3)
    vk4 = dt*f(x+xk3, v+vk3, t+dt)
    x += (xk1+2*xk2+2*xk3+xk4)/6
    v += (vk1+2*vk2+2*vk3+vk4)/6
    t += dt
    return x, v, t

def step():
    global xx, yy, t, p, theta, H, time, ene, position, momentum
    p_temp = p
    theta, p, t = rk4(theta, p, t)


    if p_temp*p < 0: #kollar när p byter tecken, alltså hittar två p runt p=0
        #amplituden är inte nödvändigtvis väldefinerat vad man menar så instruktioner
        #skulle kunna vara tydligare. Men jag antar att A = abs(theta)
        amplitudes.append(abs(theta)) #theta inte nödvändigtvis bättre än theta värdet innan
        turning_point_times.append(t)

    # energy
    #H = 0.5*p**2 + 1 - np.cos(theta)

    # position
    xx = (0, np.sin(theta))
    yy = (0, -np.cos(theta))

    position.append(theta)
    momentum.append(p)

    if theta>np.pi: theta -= 2*np.pi
    if theta<-np.pi: theta += 2*np.pi
    
def init():
    pendulum.set_data([], [])
    phaseportrait.set_data([], [])
    return pendulum, phaseportrait, 

def animate(i):
    step()
    pendulum.set_data(xx, yy)
    phaseportrait.set_data(position, momentum)
    return pendulum, phaseportrait, 

anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=2000, interval=1, blit=True, repeat=True)

plt.show()

def plotA_mot_t():

    plt.figure()
    plt.plot(turning_point_times, amplitudes, 'o-')
    plt.xlabel('tid')
    plt.ylabel('amplitud')
    plt.title('amplitud mot "turning point" tid')
    plt.show()

def plot_logA_mot_t():
    logA = np.log(amplitudes)

    plt.figure()
    plt.plot(turning_point_times, logA, 'o-')
    plt.xlabel('tid')
    plt.ylabel('log(amplitud)')
    plt.title('log(amplitud) mot tid')
    plt.show()

def fit_log_decay():
    logA = np.log(amplitudes)

    #polynom av grad 1
    k, m = np.polyfit(turning_point_times, logA, 1)


    #logplot med interpolationen under
    plt.figure()
    plt.plot(turning_point_times, logA, 'o', label='data')
    plt.plot(turning_point_times, k*np.array(turning_point_times)+m, label='linjär fit')
    plt.xlabel('tid')
    plt.ylabel('log(amplitud)')
    plt.legend()
    plt.title('Log-plot med linjär anpassning')
    plt.show()

    return k

def half_time(k):
    tau = np.log(2)/(-k)
    return tau


plotA_mot_t()
plot_logA_mot_t()
k = fit_log_decay()
tau = half_time(k)
print(f'tau = {tau}')








def first_amplitude(theta0, gamma_val):
    global theta, p, t, gamma

    theta = theta0
    p = 0
    t = 0
    gamma = gamma_val

    crossed_zero = False

    for i in range(100000):
        theta_old = theta
        theta, p, t = rk4(theta, p, t)

        # kolla om vi passerar theta = 0
        if theta_old * theta < 0:
            crossed_zero = True

        # turning point (p byter tecken)
        if i > 0 and p * p_old < 0:
            return abs(theta), crossed_zero

        p_old = p

    return abs(theta), crossed_zero


def sweep_gamma():
    gammas = np.array([0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0])
    amplitudes = []
    crosses = []

    for g in gammas:
        A, crossed = first_amplitude(np.pi/2, g)
        amplitudes.append(A)
        crosses.append(crossed)

    return gammas, np.array(amplitudes), np.array(crosses)




def plot_gamma_dependence():
    gammas, amps, crosses = sweep_gamma()

    plt.figure()
    plt.plot(gammas, amps, 'o-')
    plt.xlabel(r'$\gamma$')
    plt.ylabel('första amplitud')
    plt.title('Amplitud vs $\gamma$')
    plt.show()

    plt.figure()
    plt.plot(1/gammas, amps, 'o-')
    plt.xlabel(r'$1/\gamma$')
    plt.ylabel('första amplitud')
    plt.title('Amplitud vs $1/\gamma$')
    plt.show()

    # skriv ut ungefärlig gräns
    for g, c in zip(gammas, crosses):
        if not c:
            print(f"Överdämpning börjar ungefär vid gamma ≈ {g}")
            break

plot_gamma_dependence()
