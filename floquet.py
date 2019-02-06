# Floquet analysis of an oscillating boundary layer flow
# Bryan Kaiser
# 2/5/19

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
from functions import make_Lap_inv, steady_nonrotating_solution, xforcing_nonrotating_solution, make_d, make_e, make_Lap_inv, make_partial_z, make_DI, make_D4, make_A13, make_A14, make_A34, make_A43, check_matrix, rk4, ordered_prod, time_step

figure_path = "/home/bryan/data/floquet/figures/"
stat_path = "./"


# =============================================================================


# fluid properties:
nu = 2.0e-6 # m^2/s, kinematic viscosity
Pr = 1. # Prandtl number
kap = nu/Pr # m^2/s, thermometric diffusivity


# flow characteristics:
T = 44700.0 # s, M2 tide period
omg = 2.0*np.pi/T # rads/s
f = 1e-4 # 1/s, inertial frequency
N = 1e-3 # 1/s, buoyancy frequency
U = 0.001 # m/s, oscillation velocity amplitude
L = U/omg # m, excursion length
thtc= ma.asin(omg/N) # radians    
tht = 1./4.*thtc # radians
Re = omg*L**2./nu # Reynolds number
dRe = np.sqrt(2.*nu/omg) # Stokes' 2nd problem BL thickness


# grid:
H = dRe*20.
Nz = 6 #int(H*10)
z = np.linspace((H/Nz)/2. , H, num=Nz) # m 
dz = z[1]-z[0] # m


# non-dimensional perturbation wavenumbers, non-dimensionalized by L=U/omega:
k0=1. 
l0=1.


# time series:
Nt = int(T*1000) 
t = np.linspace( 0. , T*1. , num=Nt , endpoint=True , dtype=float) #[0.] 
dt = t[1]-t[0]
print('CFL =', U*dt/dz)
print('CFLx =', U*dt*np.sqrt(k0**2.+l0**2.))


# time advancement:
Phi0 = np.eye(int(4*Nz),int(4*Nz),0,dtype=complex) # initial condition (prinicipal fundamental solution matrix)
Phin = time_step( Nz, N, omg, tht, nu, kap, U, t, z, dz, l0, k0, Phi0 , dt, 10)


# Floquet mode/multiplier solutions:
eigval,eigvec = np.linalg.eig(Phin) # eigenvals, eigenvecs | eigenvals = floquet multipliers
"""
# checks w,v decomposition:
print('Should be zero =',np.dot((Phin-np.eye(int(2),int(2),0,dtype=complex)*w[0]),v[:,0])) # C*v_k=lambda*I*v_k
print('Should be zero =',np.dot((Phin-np.eye(int(2),int(2),0,dtype=complex)*w[1]),v[:,1]))
"""
eigvalr = np.real(eigval)
eigvali = np.imag(eigval)
eigvecr = np.real(eigvec)
eigveci = np.imag(eigvec)
print(eigval)
print(eigvec)

# save results to .h5:
h5_filename = stat_path + 'eigvals.h5' 
f2 = h5py.File(h5_filename, "w")
dset = f2.create_dataset('t', data=t, dtype='f8')
dset = f2.create_dataset('z', data=z, dtype='f8')
dset = f2.create_dataset('k', data=k0, dtype='f8')
dset = f2.create_dataset('l', data=l0, dtype='f8')
dset = f2.create_dataset('eigvalr', data=eigvalr, dtype='f8')
dset = f2.create_dataset('eigvali', data=eigvali, dtype='f8')
dset = f2.create_dataset('eigvecr', data=eigvecr, dtype='f8')
dset = f2.create_dataset('eigveci', data=eigveci, dtype='f8')
dset = f2.create_dataset('U', data=U, dtype='f8')
dset = f2.create_dataset('N', data=N, dtype='f8')
dset = f2.create_dataset('tht', data=tht, dtype='f8')
dset = f2.create_dataset('Pr', data=Pr, dtype='f8')
dset = f2.create_dataset('omg', data=omg, dtype='f8')
print('\nfile written!\n')
