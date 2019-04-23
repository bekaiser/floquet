# verifies first and second derivative Lagrange polynomial computation
# Bryan Kaiser

import numpy as np
import math as ma
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/path/to/application/app/folder')
import functions as fn

figure_path = './verification_tests/figures/discretization_test/'


# SET A THRESHOLD
# DO OPEN BC CHECK!

# add uniform case with known coefficients
# problem with case 3 second derivative, lower BC


# =============================================================================
# loop over Nz resolution Chebyshev node grid

max_exp = 11 # power of two, must be equal to or greater than 5 (maximum N = 2^max)
Nr = np.power(np.ones([max_exp-3])*2.,np.linspace(4.,max_exp,max_exp-3)) # resolution 
Ng = int(np.shape(Nr)[0]) # number of resolutions to try

# case 1:
Linf1 = np.zeros([Ng]) # infinity norm, 1st derivative, uniform grid
Linf1c = np.zeros([Ng]) # infinity norm, 1st derivative, cosine grid
Linf2 = np.zeros([Ng]) # infinity norm, 2nd derivative, uniform grid 
Linf2c = np.zeros([Ng]) # infinity norm, 2nd derivative, cosine grid 
Linfp = np.zeros([Ng]) # infinity norm, Poisson solution, uniform grid
Linfpc = np.zeros([Ng]) # infinity norm, Poisson solution, cosine grid
LinfpFB = np.zeros([Ng]) # infinity norm, Poisson solution, uniform grid
LinfpcFB = np.zeros([Ng]) # infinity norm, Poisson solution, cosine grid

# case 2:
Linf12 = np.zeros([Ng]) # infinity norm, 1st derivative, uniform grid
Linf1c2 = np.zeros([Ng]) # infinity norm, 1st derivative, cosine grid
Linf22 = np.zeros([Ng]) # infinity norm, 2nd derivative, uniform grid 
Linf2c2 = np.zeros([Ng]) # infinity norm, 2nd derivative, cosine grid 

# case 3:
Linf13 = np.zeros([Ng]) # infinity norm, 1st derivative, uniform grid
Linf1c3 = np.zeros([Ng]) # infinity norm, 1st derivative, cosine grid
Linf23 = np.zeros([Ng]) # infinity norm, 2nd derivative, uniform grid 
Linf2c3 = np.zeros([Ng]) # infinity norm, 2nd derivative, cosine grid 
Linf23f = np.zeros([Ng]) # infinity norm, 2nd derivative, uniform grid 
Linf2c3f = np.zeros([Ng]) # infinity norm, 2nd derivative, cosine grid 
Linfp3 = np.zeros([Ng]) # infinity norm, Poisson solution, uniform grid
Linfpc3 = np.zeros([Ng]) # infinity norm, Poisson solution, cosine grid
Linfp3FB = np.zeros([Ng]) # infinity norm, Poisson solution, uniform grid
Linfpc3FB = np.zeros([Ng]) # infinity norm, Poisson solution, cosine grid
Linfp3f = np.zeros([Ng])
Linfpc3f = np.zeros([Ng])
Linfp3FBf = np.zeros([Ng]) # infinity norm, Poisson solution, uniform grid
Linfpc3FBf = np.zeros([Ng]) # infinity norm, Poisson solution, cosine grid

Linf10a = np.zeros([Ng])
Linf10b = np.zeros([Ng])

output_plot_no = 6
 
H = 1.0 # domain height
Hd = H*3

for n in range(0, Ng): 
      
    Nz = int(Nr[n]) # resolution
    #print('Number of grid points: ',Nz)
 
    dz = H/Nz
    z = np.linspace(dz, Nz*dz, num=Nz)-dz/2. # uniform grid

    zc = -np.cos(((np.linspace(1., 2.*Nz, num=int(2*Nz)))*2.-1.)/(4.*Nz)*np.pi)*H+H
    zc = zc[0:Nz] # half cosine grid
    dzc = zc[1:Nz] - zc[0:Nz-1]

    wall_flag = 'null'
    params = {'H': H, 'Hd': Hd, 'Nz':Nz, 'wall_flag':wall_flag, 
              'z':z, 'dz':dz} # non-dimensional grid for functions
    paramsc = {'H': H, 'Hd': Hd, 'Nz':Nz, 'wall_flag':wall_flag, 
               'z':zc, 'dz':dzc} # non-dimensional grid for functions

    z = z*Hd
    zc = zc*Hd

    if n == 0:
        plotname = figure_path + 'grid.png'
        fig = plt.figure(figsize=(16,8)); plt.subplot(1,2,1)
        plt.plot(np.linspace(0.5, Nz-0.5, num=Nz)/Nz, z, 'ob', label=r"centers")
        plt.xlabel(r"$i^{th}$ grid point divided by N where i={1,N}", fontsize=13)
        plt.ylabel(r"$z$",fontsize=13); plt.grid()
        plt.title(r"uniform grid N = %i" %(Nz),fontsize=13)
        plt.legend(loc=2,fontsize=13); plt.subplot(1,2,2)
        plt.plot(np.linspace(0.5, Nz-0.5, num=Nz)/Nz, zc, 'ob', label=r"centers")
        plt.xlabel(r"$i^{th}$ grid point divided by N where i={1,N}", fontsize=13)
        plt.ylabel(r"$z$", fontsize=13); plt.grid()
        plt.title(r"cosine grid N = %i" %(Nz), fontsize=13)
        plt.legend(loc=2, fontsize=13); plt.savefig(plotname,format="png")
        plt.close(fig);

    U0 = 2. # free stream velocity
    m = np.pi/(2.*Hd)
    q = 2.*np.pi/Hd

    # case 1:
    u = np.zeros([Nz,1]); uz = np.zeros([Nz,1]); uzz = np.zeros([Nz,1])
    u[:,0] = U0*np.sin(m*z) # signal velocity u
    uz[:,0] = U0*m*np.cos(m*z) # du/dz
    uzz[:,0] = -U0*m**2.*np.sin(m*z) # d^2u/dz^2
    uc = np.zeros([Nz,1]); uzc = np.zeros([Nz,1]); uzzc = np.zeros([Nz,1])
    uc[:,0] = U0*np.sin(m*zc) 
    uzc[:,0] = U0*m*np.cos(m*zc) 
    uzzc[:,0] = -U0*m**2.*np.sin(m*zc)

    # case 2:
    b = np.zeros([Nz,1]); bz = np.zeros([Nz,1]); bzz = np.zeros([Nz,1])
    b[:,0] = U0*np.cos(q*z)
    bz[:,0] = -U0*q*np.sin(q*z) 
    bzz[:,0] = -U0*q**2.*np.cos(q*z) 
    bc = np.zeros([Nz,1]); bzc = np.zeros([Nz,1]); bzzc = np.zeros([Nz,1])
    bc[:,0] = U0*np.cos(q*zc) 
    bzc[:,0] = -U0*q*np.sin(q*zc) 
    bzzc[:,0] = -U0*q**2.*np.cos(q*zc)

    # case 3:

    p = np.zeros([Nz,1]); pz = np.zeros([Nz,1]); pzz = np.zeros([Nz,1])
    p[:,0] = U0*np.cos(q*z) - U0
    pz[:,0] = -U0*q*np.sin(q*z) 
    pzz[:,0] = -U0*q**2.*np.cos(q*z) 
    #zetazz = np.zeros([Nz,1]); zeta[:,0] = U0*q**4.*np.cos(q*z)
    pc = np.zeros([Nz,1]); pzc = np.zeros([Nz,1]); pzzc = np.zeros([Nz,1])
    pc[:,0] = U0*np.cos(q*zc) - U0
    pzc[:,0] = -U0*q*np.sin(q*zc) 
    pzzc[:,0] = -U0*q**2.*np.cos(q*zc)
    #zetazzc = np.zeros([Nz,1]); zetac[:,0] = U0*q**4.*np.cos(q*zc)
    """
    p = np.zeros([Nz,1]); pz = np.zeros([Nz,1]); pzz = np.zeros([Nz,1])
    p[:,0] = U0*( np.cos(q*z) - np.cos(2.*q*z) )
    pz[:,0] = -U0*q*( np.sin(q*z) - 2.*np.sin(2.*q*z) )
    pzz[:,0] = -U0*q**2.*( np.cos(q*z) - 4.*np.cos(2.*q*z) )
    pc = np.zeros([Nz,1]); pzc = np.zeros([Nz,1]); pzzc = np.zeros([Nz,1])
    pc[:,0] = U0*( np.cos(q*zc) - np.cos(2.*q*zc) )
    pzc[:,0] = -U0*q*( np.sin(q*zc) - 2.*np.sin(2.*q*zc) )
    pzzc[:,0] = -U0*q**2.*( np.cos(q*zc) - 4.*np.cos(2.*q*zc) )
    """    
     
    m2 = 5*2.*np.pi/(4.*Hd)
    # case 4: zero at z=H at lowest order
    zeta = np.zeros([Nz,1]); zetazz = np.zeros([Nz,1])
    zetac = np.zeros([Nz,1]); zetazzc = np.zeros([Nz,1])
    zeta[:,0] = U0*np.cos(m2*z) #U0*(np.cos(z-np.pi) - np.sin(2.*z))
    zetazz[:,0] = -U0*m2**2.*np.cos(m2*z) #U0*(np.cos(z) + 4.*np.sin(2.*z))
    zetac[:,0] = U0*np.cos(m2*zc) #U0*(np.cos(zc-np.pi) - np.sin(2.*zc))
    zetazzc[:,0] = -U0*m2**2.*np.cos(m2*zc) #U0*(np.cos(zc) + 4.*np.sin(2.*zc))

    if n == output_plot_no:
  
        plotname = figure_path + 'analytical_solutions.png'
        fig = plt.figure(figsize=(18,10))
        plt.subplot(2,4,3)
        plt.plot(p/U0,z,'b',label=r"$\psi$")
        plt.plot(pz/(q*U0),z,'k',label=r"$\psi_z$")
        plt.plot(pzz/(q**2.*U0),z,'--r',label=r"$\psi_{zz}$")
        #plt.plot(zetazz/(q**4.*U0),z,'--b',label=r"$\zeta_{zz}$")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3",fontsize=13)
        plt.grid(); plt.legend(loc=3,fontsize=13)
        plt.subplot(2,4,7)
        plt.plot(pc/U0,zc,'b',label=r"$\psi$")
        plt.plot(pzc/(q*U0),zc,'k',label=r"$\psi_z$")
        plt.plot(pzzc/(q**2.*U0),zc,'--r',label=r"$\psi_{zz}$")
        #plt.plot(zetazzc/(q**4.*U0),zc,'--b',label=r"$\zeta_{zz}$")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3",fontsize=13)
        plt.grid(); plt.legend(loc=3,fontsize=13)
        plt.subplot(2,4,2)
        plt.plot(b/U0,z,'b',label=r"$b$")
        plt.plot(bz/(q*U0),z,'k',label=r"$b_z$")
        plt.plot(bzz/(q**2.*U0),z,'--r',label=r"$b_{zz}$")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 2",fontsize=13)
        plt.grid(); plt.legend(loc=3,fontsize=13)
        plt.subplot(2,4,6)
        plt.plot(bc/U0,zc,'b',label=r"$b$")
        plt.plot(bzc/(q*U0),zc,'k',label=r"$b_z$")
        plt.plot(bzzc/(q**2.*U0),zc,'--r',label=r"$b_{zz}$")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 2",fontsize=13)
        plt.grid(); plt.legend(loc=3,fontsize=13)
        plt.subplot(2,4,1)
        plt.plot(u/U0,z,'b',label=r"$u$")
        plt.plot(uz/(m*U0),z,'k',label=r"$u_z$")
        plt.plot(uzz/(m**2.*U0),z,'--r',label=r"$u_{zz}$")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 1",fontsize=13)
        plt.grid(); plt.legend(loc=3,fontsize=13)
        plt.subplot(2,4,5)
        plt.plot(uc/U0,zc,'b',label=r"$u$")
        plt.plot(uzc/(m*U0),zc,'k',label=r"$u_z$")
        plt.plot(uzzc/(m**2.*U0),zc,'--r',label=r"$u_{zz}$")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 1",fontsize=13)
        plt.grid(); plt.legend(loc=3,fontsize=13)
        plt.subplot(2,4,4)
        plt.plot(zeta/U0,z,'b',label=r"$\zeta$")
        plt.plot(zetazz/(U0*m2**2.),z,'--r',label=r"$\zeta_{zz}$")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 4",fontsize=13)
        plt.grid(); plt.legend(loc=3,fontsize=13)
        plt.subplot(2,4,8)
        plt.plot(zetac/U0,zc,'b',label=r"$\zeta$")
        plt.plot(zetazzc/(U0*m2**2.),zc,'--r',label=r"$\zeta_{zz}$")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 4",fontsize=13)
        plt.grid(); plt.legend(loc=3,fontsize=13)

        plt.savefig(plotname,format="png"); plt.close(fig);

    # case 1:
    # 1st derivatives:
    uz0 = np.dot( fn.partial_z( params , 'dirchlet' , 'neumann' ) , u ) # uniform grid  
    uz0c = np.dot( fn.partial_z( paramsc , 'dirchlet' , 'neumann' ) , uc ) # cosine grid
    # 2nd derivatives:
    uzz0 = np.dot( fn.partial_zz( params , 'dirchlet' , 'neumann' ) , u ) # uniform grid
    uzz0c = np.dot( fn.partial_zz( paramsc , 'dirchlet' , 'neumann' ) , uc ) # cosine grid

    # Poisson equation solution:
    u0 =  np.dot( np.linalg.inv( fn.partial_zz(  params , 'dirchlet' , 'neumann' ) ) , uzz  ) # uniform grid
    u0c = np.dot( np.linalg.inv( fn.partial_zz( paramsc , 'dirchlet' , 'neumann' ) ) , uzzc ) # cosine grid
    u0FB =  np.dot( np.linalg.inv( fn.partial_zz(  params , 'dirchlet' , 'neumann' ) ) , uzz0  ) # uniform grid
    u0cFB = np.dot( np.linalg.inv( fn.partial_zz( paramsc , 'dirchlet' , 'neumann' ) ) , uzz0c ) # cosine grid

    # case 2:
    # 1st derivatives:
    bz0 = np.dot( fn.partial_z( params , 'neumann' , 'neumann' ) , b ) # uniform grid  
    bz0c = np.dot( fn.partial_z( paramsc , 'neumann' , 'neumann' ) , bc ) # cosine grid
    # 2nd derivatives:
    bzz0 = np.dot( fn.partial_zz( params , 'neumann' , 'neumann' ) , b ) # uniform grid
    bzz0c = np.dot( fn.partial_zz( paramsc , 'neumann' , 'neumann' ) , bc ) # cosine grid
    # Poisson equation solution: both neumann: ERROR! the matrix is singular

    # case 3:
    # 1st derivatives, case 3: (the forward derivative needs no mean information)
    pz0 = np.dot( fn.partial_z( params , 'neumann' , 'neumann'   ) , p ) # uniform grid
    pz0c = np.dot( fn.partial_z( paramsc , 'neumann' , 'neumann'   ) , pc ) # cosine grid 
    # 2nd derivatives, case 3:
    case3_upper_BC = 'dirchlet'
    pzz0 = np.dot( fn.partial_zz( params , 'robin' , case3_upper_BC  ) , p ) # uniform grid
    pzz0c = np.dot( fn.partial_zz( paramsc , 'robin' , case3_upper_BC ) , pc ) # cosine grid   (use 'open','dirchlet' for vorticity)
    pzz0f = np.dot( fn.diff_matrix( params , 'thom' , case3_upper_BC , diff_order=2 , stencil_size=3 ) , p ) # uniform grid
    pzz0cf = np.dot( fn.diff_matrix( paramsc , 'thom' , case3_upper_BC , diff_order=2 , stencil_size=3 ) , pc ) # cosine grid

    zetazz0 = np.dot( fn.diff_matrix( params , 'open' , case3_upper_BC , diff_order=2 , stencil_size=3 ) , zeta ) # uniform grid
    zetazz0c = np.dot( fn.diff_matrix( paramsc , 'open' , case3_upper_BC , diff_order=2 , stencil_size=3 ) , zetac ) # cosine grid

    # Poisson equation solution: (the backward derivative needs mean information, hence the robin BC)
    p0 =  np.dot( np.linalg.inv( fn.partial_zz(  params , 'robin' , case3_upper_BC ) ) , pzz  ) # uniform grid
    p0c = np.dot( np.linalg.inv( fn.partial_zz( paramsc , 'robin' , case3_upper_BC ) ) , pzzc ) # cosine grid 
    p0f =  np.dot( np.linalg.inv( fn.diff_matrix( params , 'thom' , case3_upper_BC , diff_order=2 , stencil_size=3 ) ) , pzz  ) # uniform grid
    p0cf = np.dot( np.linalg.inv( fn.diff_matrix( paramsc , 'thom' , case3_upper_BC , diff_order=2 , stencil_size=3 ) ) , pzzc ) # cosine grid 
    p0FB =  np.dot( np.linalg.inv( fn.partial_zz(  params , 'robin' , case3_upper_BC ) ) , pzz0  ) # uniform grid
    p0cFB = np.dot( np.linalg.inv( fn.partial_zz( paramsc , 'robin' , case3_upper_BC ) ) , pzz0c ) # cosine grid
    p0FBf =  np.dot( np.linalg.inv( fn.diff_matrix(  params , 'thom' , case3_upper_BC , diff_order=2 , stencil_size=3 ) ) , pzz0f  ) # uniform grid
    p0cFBf = np.dot( np.linalg.inv( fn.diff_matrix( paramsc , 'thom' , case3_upper_BC , diff_order=2 , stencil_size=3 ) ) , pzz0cf ) # cosine grid

    if n == output_plot_no:

        plotname = figure_path + 'poisson_solutions_case3_robin.png'
        fig = plt.figure(figsize=(10,10))
        plt.subplot(2,2,1)
        plt.plot(p/(U0),z,'k',label=r"analytical")
        plt.plot(p0/(U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=2,fontsize=13)
        plt.subplot(2,2,2)
        plt.plot(pc/(U0),zc,'k',label=r"analytical")
        plt.plot(p0c/(U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=2,fontsize=13)
        plt.subplot(2,2,3)
        plt.semilogx(abs(p-p0)/abs(U0),z,'k')
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); 
        plt.subplot(2,2,4)
        plt.semilogx(abs(pc-p0c)/abs(U0),zc,'k')
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); 
        plt.savefig(plotname,format="png"); plt.close(fig);

        plotname = figure_path + 'poisson_solutions_case3_thom.png'
        fig = plt.figure(figsize=(10,10))
        plt.subplot(2,2,1)
        plt.plot(p/(U0),z,'k',label=r"analytical")
        plt.plot(p0FBf/(U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=2,fontsize=13)
        plt.subplot(2,2,2)
        plt.plot(pc/(U0),zc,'k',label=r"analytical")
        plt.plot(p0cFBf/(U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=2,fontsize=13)
        plt.subplot(2,2,3)
        plt.semilogx(abs(p-p0FBf)/abs(U0),z,'k')
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); 
        plt.subplot(2,2,4)
        plt.semilogx(abs(pc-p0cFBf)/abs(U0),zc,'k')
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); 
        plt.savefig(plotname,format="png"); plt.close(fig);


        plotname = figure_path + 'poisson_solutions_case1.png'
        fig = plt.figure(figsize=(10,10))
        plt.subplot(2,2,1)
        plt.plot(u/(U0),z,'k',label=r"analytical")
        plt.plot(u0/(U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=2,fontsize=13)
        plt.subplot(2,2,2)
        plt.plot(uc/(U0),zc,'k',label=r"analytical")
        plt.plot(u0c/(U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=2,fontsize=13)
        plt.subplot(2,2,3)
        plt.semilogx(abs(u-u0)/abs(U0),z,'k')
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); 
        plt.subplot(2,2,4)
        plt.semilogx(abs(uc-u0c)/abs(U0),zc,'k')
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); 
        plt.savefig(plotname,format="png"); plt.close(fig);

        plotname = figure_path + 'first_derivative_solutions.png'
        fig = plt.figure(figsize=(18,20))
        plt.subplot(4,3,1)
        plt.plot(uz/(m*U0),z,'k',label=r"analytical")
        plt.plot(uz0/(m*U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,2)
        plt.plot(bz/(q*U0),z,'k',label=r"analytical")
        plt.plot(bz0/(q*U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 2, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,3)
        plt.plot(pz/(q*U0),z,'k',label=r"analytical")
        plt.plot(pz0/(q*U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,4)
        #plt.plot(abs(uz-uz0)/abs(m*U0), z, 'k') 
        plt.semilogx(abs(uz-uz0)/abs(m*U0), z, 'k') 
        plt.ylabel(r"$z$", fontsize=13)
        plt.title(r"uniform grid, case 1, N = %i" %(Nz), fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,5)
        #plt.plot(abs(bz-bz0)/abs(q*U0), z, 'k') 
        plt.semilogx(abs(bz-bz0)/abs(q*U0), z, 'k') 
        plt.ylabel(r"$z$", fontsize=13)
        plt.title(r"uniform grid, case 2, N = %i" %(Nz), fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,6)
        #plt.plot(abs(pz-pz0)/abs(q*U0), z, 'k') 
        plt.semilogx(abs(pz-pz0)/abs(q*U0), z, 'k') 
        plt.ylabel(r"$z$", fontsize=13)
        plt.title(r"uniform grid, case 3, N = %i" %(Nz), fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,7)
        plt.plot(uzc/(m*U0),zc,'k',label=r"analytical")
        plt.plot(uz0c/(m*U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,8)
        plt.plot(bzc/(q*U0),zc,'k',label=r"analytical")
        plt.plot(bz0c/(q*U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 2, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,9)
        plt.plot(pzc/(q*U0),zc,'k',label=r"analytical")
        plt.plot(pz0c/(q*U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,10)
        #plt.plot(abs(uzc-uz0c)/abs(m*U0),z,'k') 
        plt.semilogx(abs(uzc-uz0c)/abs(m*U0),z,'k') 
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,11)
        #plt.plot(abs(bzc-bz0c)/abs(q*U0),z,'k') 
        plt.semilogx(abs(bzc-bz0c)/abs(q*U0),z,'k') 
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 2, N = %i" %(Nz),fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,3,12)
        #plt.plot(abs(pzc-pz0c)/abs(q*U0),z,'k') 
        plt.semilogx(abs(pzc-pz0c)/abs(q*U0),z,'k') 
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.savefig(plotname,format="png"); plt.close(fig);

        plotname = figure_path + 'second_derivative_solutions_case4.png'
        fig = plt.figure(figsize=(10,10))
        plt.subplot(2,2,1)
        plt.plot(zetazz/(U0),z,'k',label=r"analytical")
        plt.plot(zetazz0/(U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 4, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=2,fontsize=13)
        plt.subplot(2,2,2)
        plt.plot(zetazzc/(U0),zc,'k',label=r"analytical")
        plt.plot(zetazz0c/(U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 4, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=2,fontsize=13)
        plt.subplot(2,2,3)
        plt.semilogx(abs(zetazz-zetazz0)/abs(U0),z,'k')
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 4, N = %i" %(Nz),fontsize=13)
        plt.grid(); 
        plt.subplot(2,2,4)
        plt.semilogx(abs(zetazzc-zetazz0c)/abs(U0),zc,'k')
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 4, N = %i" %(Nz),fontsize=13)
        plt.grid(); 
        plt.savefig(plotname,format="png"); plt.close(fig); 


        plotname = figure_path + 'second_derivative_solutions.png'
        fig = plt.figure(figsize=(18,20))
        plt.subplot(4,4,1)
        plt.plot(uzz/(m**2.*U0),z,'k',label=r"analytical")
        plt.plot(uzz0/(m**2.*U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,2)
        plt.plot(bzz/(q**2.*U0),z,'k',label=r"analytical")
        plt.plot(bzz0/(q**2.*U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 2, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,3)
        plt.plot(pzz/(q**2.*U0),z,'k',label=r"analytical")
        plt.plot(pzz0/(q**2.*U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3, Robin BC N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,4)
        plt.plot(pzz/(q**2.*U0),z,'k',label=r"analytical")
        plt.plot(pzz0f/(q**2.*U0),z,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3, Thom BC N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,5)
        #plt.plot(abs(uz-uz0)/abs(m*U0), z, 'k') 
        plt.semilogx(abs(uzz-uzz0)/abs(m**2.*U0), z, 'k') 
        plt.ylabel(r"$z$", fontsize=13)
        plt.title(r"uniform grid, case 1, N = %i" %(Nz), fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,6)
        #plt.plot(abs(bz-bz0)/abs(q*U0), z, 'k') 
        plt.semilogx(abs(bzz-bzz0)/abs(q**2.*U0), z, 'k') 
        plt.ylabel(r"$z$", fontsize=13)
        plt.title(r"uniform grid, case 2, N = %i" %(Nz), fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,7)
        #plt.plot(abs(pz-pz0)/abs(q*U0), z, 'k') 
        plt.semilogx(abs(pzz-pzz0)/abs(q**2.*U0), z, 'k') 
        plt.ylabel(r"$z$", fontsize=13)
        plt.title(r"uniform grid, case 3, Robin BC", fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,8)
        plt.semilogx(abs(pzz-pzz0f)/abs(q**2.*U0),z,'k') #,label=r"analytical")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"uniform grid, case 3, Thom BC",fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,9)
        plt.plot(uzzc/(m**2.*U0),zc,'k',label=r"analytical")
        plt.plot(uzz0c/(m**2.*U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,10)
        plt.plot(bzzc/(q**2.*U0),zc,'k',label=r"analytical")
        plt.plot(bzz0c/(q**2.*U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 2, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,11)
        plt.plot(pzzc/(q**2.*U0),zc,'k',label=r"analytical")
        plt.plot(pzz0c/(q**2.*U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,12)
        plt.plot(pzzc/(q**2.*U0),zc,'k',label=r"analytical")
        plt.plot(pzz0cf/(q**2.*U0),zc,'--r',label=r"computed")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, N = %i" %(Nz),fontsize=13)
        plt.grid(); plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,13)
        #plt.plot(abs(uzc-uz0c)/abs(m*U0),z,'k') 
        plt.semilogx(abs(uzzc-uzz0c)/abs(m**2.*U0),zc,'k') 
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 1, N = %i" %(Nz),fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,14)
        #plt.plot(abs(bzc-bz0c)/abs(q*U0),z,'k') 
        plt.semilogx(abs(bzzc-bzz0c)/abs(q**2.*U0),zc,'k') 
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 2, N = %i" %(Nz),fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,15)
        #plt.plot(abs(pzc-pz0c)/abs(q*U0),z,'k') 
        plt.semilogx(abs(pzzc-pzz0c)/abs(q**2.*U0),zc,'k') 
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, Robin BC",fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.subplot(4,4,16)
        plt.semilogx(abs(pzzc-pzz0cf)/abs(q**2.*U0),zc,'k') #label=r"analytical")
        plt.ylabel(r"$z$",fontsize=13)
        plt.title(r"cosine grid, case 3, Thom BC",fontsize=13)
        plt.grid(); #plt.legend(loc=1,fontsize=13)
        plt.savefig(plotname,format="png"); plt.close(fig);


    # case 1:
    Linf1[n] = np.amax(abs(uz-uz0)/abs(m*U0)) 
    Linf1c[n] = np.amax(abs(uzc-uz0c)/abs(m*U0))
    Linf2[n] = np.amax(abs(uzz-uzz0)/abs(m**2.*U0)) 
    Linf2c[n] = np.amax(abs(uzzc-uzz0c)/abs(m**2.*U0))
    Linfp[n] = np.amax(abs(u-u0)/abs(U0)) 
    Linfpc[n] = np.amax(abs(uc-u0c)/abs(U0))
    LinfpFB[n] = np.amax(abs(u-u0FB)/abs(U0)) 
    LinfpcFB[n] = np.amax(abs(uc-u0cFB)/abs(U0))

    # case 2:
    Linf12[n] = np.amax(abs(bz-bz0)/abs(q*U0)) 
    Linf1c2[n] = np.amax(abs(bzc-bz0c)/abs(q*U0))
    Linf22[n] = np.amax(abs(bzz-bzz0)/abs(q**2.*U0)) 
    Linf2c2[n] = np.amax(abs(bzzc-bzz0c)/abs(q**2.*U0))

    # case 3:
    Linf13[n] = np.amax(abs(pz-pz0)/abs(q*U0)) 
    Linf1c3[n] = np.amax(abs(pzc-pz0c)/abs(q*U0))
    Linf23[n] = np.amax(abs(pzz-pzz0)/abs(q**2.*U0)) 
    Linf2c3[n] = np.amax(abs(pzzc-pzz0c)/abs(q**2.*U0))
    Linfp3[n] = np.amax(abs(p-p0)/abs(U0)) 
    Linfpc3[n] = np.amax(abs(pc-p0c)/abs(U0))
    Linfp3f[n] = np.amax(abs(p-p0f)/abs(U0)) 
    Linfpc3f[n] = np.amax(abs(pc-p0cf)/abs(U0))
    Linfp3FB[n] = np.amax(abs(p-p0FB)/abs(U0)) 
    Linfpc3FB[n] = np.amax(abs(pc-p0cFB)/abs(U0))
    Linfp3FBf[n] = np.amax(abs(p-p0FBf)/abs(U0)) 
    Linfpc3FBf[n] = np.amax(abs(pc-p0cFBf)/abs(U0))
    Linf23f[n] = np.amax(abs(pzz-pzz0f)/abs(q**2.*U0)) 
    Linf2c3f[n] = np.amax(abs(pzzc-pzz0cf)/abs(q**2.*U0))

    Linf10a[n] = np.amax(abs(zetazz-zetazz0)/abs(m2**2.*U0)) 
    Linf10b[n] = np.amax(abs(zetazzc-zetazz0c)/abs(m2**2.*U0))

plotname = figure_path + 'poisson_error_curves.png'
fig = plt.figure(figsize=(24,8))
plt.subplot(1,3,1)
plt.loglog(Nr,Linfp, 'r', label=r"uniform")
plt.loglog(Nr,Linfpc, 'b', label=r"cosine")
plt.xlabel(r"$N$ grid points", fontsize=13)
plt.ylabel(r"L$_\infty$ error", fontsize=13)
plt.title(r"Dirchlet LBC, Neumann UBC, case 1", fontsize=13) 
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,3,2)
plt.loglog(Nr,Linfp3,'r',label=r"uniform")
plt.loglog(Nr,Linfpc3,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"Robin LBC, Dirchlet UBC, case 3",fontsize=13) 
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,3,3)
plt.loglog(Nr,Linfp3f,'r',label=r"uniform")
plt.loglog(Nr,Linfpc3f,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"Thom LBC, Dirchlet UBC, case 3",fontsize=13) 
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.savefig(plotname,format="png"); plt.close(fig);

plotname = figure_path + 'forward_backward_error_curves.png'
fig = plt.figure(figsize=(24,8))
plt.subplot(1,3,1)
plt.loglog(Nr,LinfpFB, 'r', label=r"uniform")
plt.loglog(Nr,LinfpcFB, 'b', label=r"cosine")
plt.xlabel(r"$N$ grid points", fontsize=13)
plt.ylabel(r"L$_\infty$ error", fontsize=13)
plt.title(r"Dirchlet LBC, Neumann UBC, case 1", fontsize=13) 
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,3,2)
plt.loglog(Nr,Linfp3FB,'r',label=r"uniform")
plt.loglog(Nr,Linfpc3FB,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"Robin LBC, Dirchlet UBC, case 3",fontsize=13) 
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,3,3)
plt.loglog(Nr,Linfp3FBf,'r',label=r"uniform")
plt.loglog(Nr,Linfpc3FBf,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"Thom LBC, Dirchlet UBC, case 3",fontsize=13) 
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.savefig(plotname,format="png"); plt.close(fig);



plotname = figure_path + 'first_derivative_error_curve.png'
fig = plt.figure(figsize=(24,8))
plt.subplot(1,3,1)
plt.loglog(Nr,Linf1,'r',label=r"uniform")
plt.loglog(Nr,Linf1c,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"case 1",fontsize=13)
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,3,2)
plt.loglog(Nr,Linf12,'r',label=r"uniform")
plt.loglog(Nr,Linf1c2,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"case 2",fontsize=13)
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,3,3)
plt.loglog(Nr,Linf13,'r',label=r"uniform")
plt.loglog(Nr,Linf1c3,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"case 3",fontsize=13)
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.savefig(plotname,format="png"); plt.close(fig);



plotname = figure_path + 'second_derivative_error_curve.png'
fig = plt.figure(figsize=(30,8))
plt.subplot(1,5,1)
plt.loglog(Nr,Linf2,'r',label=r"uniform")
plt.loglog(Nr,Linf2c,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"case 1",fontsize=13)
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,5,2)
plt.loglog(Nr,Linf22,'r',label=r"uniform")
plt.loglog(Nr,Linf2c2,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"case 2",fontsize=13)
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,5,3)
plt.loglog(Nr,Linf23,'r',label=r"uniform")
plt.loglog(Nr,Linf2c3,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"case 3, Robin z=0 BC",fontsize=13)
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,5,4)
plt.loglog(Nr,Linf23f,'r',label=r"uniform")
plt.loglog(Nr,Linf2c3f,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"case 3, Thom z=0 BC",fontsize=13)
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.subplot(1,5,5)
plt.loglog(Nr,Linf10a,'r',label=r"uniform")
plt.loglog(Nr,Linf10b,'b',label=r"cosine")
plt.xlabel(r"$N$ grid points",fontsize=13)
plt.ylabel(r"L$_\infty$ error",fontsize=13)
plt.title(r"case 4, open z=0 BC",fontsize=13)
plt.grid(); plt.legend(loc=1,fontsize=13)
plt.savefig(plotname,format="png"); plt.close(fig);
