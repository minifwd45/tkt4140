# src-ch5/couette_Flow_FTCS.py;Visualization.py @ git@lrhgit/tkt4140/src/src-ch5/Visualization.py;

import matplotlib; matplotlib.use('Qt4Agg')
import matplotlib.pylab as plt
plt.get_current_fig_manager().window.raise_()

import numpy as np
from math import exp, sin, pi

def analyticSolution_old(y, t, N=100):
    
    """ Method that calculates the analytical solution to the differential equation:
        du/dt = d^2(u)/dx^2 , u = u(y,t), 0 < y < 1
        Boundary conditions: u(0, t) = 1, u(1, t) = 0
        Initial condition: u(t, 0) = 0 t<0,  u(t, 0) = 1 t>0
            
        Args:
            y(float): radial coordinat
            t(float): time
            N(int): truncation integer. Truncate sumation after N elements

    
        Returns:
            w(float): velocity, us - ur
    """
    sumValue = 0
    for n in range(1,N+1):
        temp = exp(-t*(n*pi)**2)*sin(n*pi*y)/n
        sumValue += temp
    u = 1 - y - (2/pi)*sumValue
    return u

def analyticSolution(y, t, N=100):
    
    """ Method that calculates the analytical solution to the differential equation:
        du/dt = d^2(u)/dx^2 , u = u(y,t), 0 < y < 1
        Boundary conditions: u(0, t) = 1, u(1, t) = 0
        Initial condition: u(t, 0) = 0 t<0,  u(t, 0) = 1 t>0
            
        Args:
            y(np.array): radial coordinat
            t(float): time
            N(int): truncation integer. Truncate sumation after N elements

    
        Returns:
            w(float): velocity, us - ur
    """
    sumValue = 0
    for n in range(1,N+1):
        temp = np.exp(-t*(n*np.pi)**2)*np.sin(n*np.pi*y)/n
        sumValue += temp
    u = 1 - y - (2/pi)*sumValue
    return u

def solveNextTimestepFTCS(Uold, D):
    """ Method that solves the transient couetteflow using the FTCS-scheme..
        At time t=t0 the plate starts moving at y=0
        The method solves only for the next time-step.
        The Governing equation is:
        
        du/dt = d^2(u)/dx^2 , u = u(y,t), 0 < y < 1
        
        Boundary conditions: u(0, t) = 1, u(1, t) = 0
        
        Initial condition: u(t, 0) = 0 t<0,  u(t, 0) = 1 t>0
        
        Args:
            uold(array): solution from previous iteration
            D(float): Numerical diffusion number
            
        Returns:
            unew(array): solution at time t^n+1
    """
    Unew = np.zeros_like(Uold)
    
    Uold_plus = Uold[2:]
    Uold_minus = Uold[:-2]
    Uold_mid = Uold[1:-1]
    
    Unew[1:-1] = D*(Uold_plus + Uold_minus) + (1 - 2*D)*Uold_mid
    Unew[0] = 1
    
    return Unew
            
if __name__ == '__main__':
    
    import numpy as np
    from Visualization import createAnimation


    D = 0.5 # numerical diffusion number
    
    N = 20 
    Y = np.linspace(0, 1, N + 1)
    h = Y[1] - Y[0]
    dt = D*h**2 
    T = 0.2 # simulation time
    time = np.arange(0, T + dt, dt)
    
    # solution matrices:
    U = np.zeros((len(time), N + 1))
    U[0, 0] = 1 # no slip condition at the plate boundary
    
    Uanalytic = np.zeros((len(time), N + 1))
    Uanalytic[0, 0] = U[0,0]
    
    
    for n, t in enumerate(time[1:]):
        
        Uold = U[n, :]
        
        U[n + 1, :] = solveNextTimestepFTCS(Uold, D)

        Uanalytic[n + 1, :] = analyticSolution(Y, t, 100) 
               
    U_Visualization = np.zeros((1, len(time), N + 1))
    U_Visualization[0, :, :] = U
    
    createAnimation(U_Visualization, Uanalytic, ["FTCS"], Y, time, symmetric=False)

    
    

