# simple test of RK4 and eigenvalue computation for Floquet analysis
# Bryan Kaiser
# 2/4/2018

# Note: see LaTeX document "floquet_primer" for analytical solution derivation

import h5py
import numpy as np
import math as ma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy
from scipy.stats import chi2
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.patches as mpatches
from matplotlib.colors import colorConverter as cc


from functions import make_Lap_inv, steady_nonrotating_solution, xforcing_nonrotating_solution, make_d, make_e, make_Lap_inv, make_partial_z, make_DI, make_D4, make_A13, make_A14, make_A34, make_A43, check_matrix, rk4, rk4_test, ordered_prod

figure_path = "./figures/"


# =============================================================================

T = 100.0 # s, period
omg = 2.0*np.pi/T # rads/s

M = [10,50,100,200,500,1000,10000] 
Linf = np.zeros(np.shape(M))
dT = np.zeros(np.shape(M))

for m in range(0,np.shape(M)[0]):

 Nt = int(T*M[m]) 

 # time series
 t = np.linspace( 0. , T*1. , num=Nt , endpoint=True , dtype=float) #[0.] 
 dt = t[1]-t[0]
 dT[m] = dt

 alph = 0.5 + 0.*1j
 beta = 0.1 + 0.*1j

 Phin = np.eye(int(2),int(2),0,dtype=complex)
 Tf = t[0]

 # time advancement:
 for n in range(0,2):
  print(n)
  Tf=t[n]
  time = t[n]

  # Runge-Kutta, 4th order: 
  k1 =  rk4_test( alph, beta, omg, time, Phin )
  k2 =  rk4_test( alph, beta, omg, time + dt/2., Phin + k1*(dt/2.)  )
  k3 =  rk4_test( alph, beta, omg, time + dt/2., Phin + k2*(dt/2.)  )
  k4 =  rk4_test( alph, beta, omg, time + dt, Phin  + k3*dt )
  Phin = Phin + ( k1 + k2*2. + k3*2. + k4 )*dt/6.; # now at t[n+1]
 

 # analytical solution:
 Phia = np.matrix([[np.exp(-alph*(Tf+dt)),0.],[0.,np.exp(-beta*(Tf+dt))]],dtype=complex)
 wa,va = np.linalg.eig(Phia)

 # computed solution:
 w,v = np.linalg.eig(Phin) # eigenvals, eigenvecs | eigenvals = floquet multipliers

 percent_error_mu1 = abs((w[0]-wa[0]))/abs(wa[0])*100.
 percent_error_mu2 = abs((w[1]-wa[1]))/abs(wa[1])*100.
 Linf[m] = np.amax([percent_error_mu1,percent_error_mu2])


plotname = figure_path +'local_loglog_error.png' 
plottitle = r"Floquet multiplier % error, for $\alpha=0.5,\beta=0.1$" 
fig = plt.figure()
plt.loglog(dT/T,Linf,'k',label="computed")
plt.loglog(dT/T,(dT**4.),'b',label=r"O$(dt^4)$")
plt.xlabel(r"$\Delta{t}/T$ normalized time step",fontsize=13);
plt.ylabel(r"$|error|_\infty$",fontsize=13); 
plt.legend(loc=2,fontsize=14); 
plt.title(plottitle);
plt.grid()
plt.savefig(plotname,format="png"); plt.close(fig);

plotname = figure_path +'local_semilogy_error.png' #%(start_time,end_time)
plottitle = r"Floquet multiplier % LTE, for $\alpha=0.5,\beta=0.1$" #, $\tau_w/U_0^2$ Re=%.2f, Pr=%.1f" #%(Re,Pr)
fig = plt.figure()
plt.semilogy(dT,Linf,'k')
plt.xlabel(r"$N=T/\Delta{t}$ time steps",fontsize=13); 
plt.ylabel(r"$|E|_\infty$",fontsize=13); 
plt.title(plottitle);
plt.grid()
plt.savefig(plotname,format="png"); plt.close(fig);