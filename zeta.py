
import h5py
import numpy as np
import math as ma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy   
from scipy import signal
import functions as fn

figure_path = "./figures/"
stat_path = "./output/"
email_flag = 1
ic_plot_flag = 0

if email_flag == 1:
    import smtplib, ssl
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "my.sent.data.kaiser@gmail.com"  # Enter your address
    receiver_email = "my.sent.data.kaiser@gmail.com"  # Enter receiver address
    password = 'wh$0i1BTu' #input("Type your password and press enter: ")


# =============================================================================

def count_points( params ):
    #dS = params['dS']
    z = params['z']
    #Hd = params['Hd']
    #Nz = params['Nz']
    count = 0
    for j in range(0,Nz):
         #if (z[j]*dS) <= dS:
         if (z[j]) <= 1.:
             count = count + 1
    return count


# =============================================================================
# need a resolution requirement. From the analytical solution?

T = 2.*np.pi # s, period
omg = 2.*np.pi/44700. # rads/s
nu = 1e-6
dS = np.sqrt(2.*nu/omg) # Stokes' 2nd problem BL thickness

Nj = 3 # 3
Ni = 3 # 18
#Rej = np.array([1500])
#ai = np.array([0.475]) #36666666666666666])
Rej = np.linspace(1333.33333333333,1400,num=Nj,endpoint=True)
ai = np.linspace(0.033333333333,0.1,num=Ni,endpoint=True)

# grid
grid_flag = 'hybrid cosine' #'  'cosine' # # 
wall_BC_flag = 'Thom'
wall_BC_off_flag = ' ' 
plot_freq = 0
Nz = 260 # 100 has a slight spurious mode
H = 500. # = Hd/dS, non-dimensional grid height
CFL = 0.5 # 0.25 fine for 150, 0.1 for 200
#Nz = np.array([50,75,100,125,150,175,200,225,250,300,350,400,450,500,550,600,650])
#H = np.array([2.,3.,4.,5.,6.,7.,8.,9.,10.,12.,14.,16.,18.,20.,22.,24.,26.])
Hd = H*dS # m, dimensional domain height (arbitrary choice)
z,dz = fn.grid_choice( grid_flag , Nz , H ) # non-dimensional grid
grid_params_dzz = {'H':H, 'Hd':Hd,'z':z,'dz':dz,'Nz':Nz, 'wall_BC_flag':wall_BC_flag} 
grid_params_inv = {'H':H, 'Hd':Hd,'z':z,'dz':dz,'Nz':Nz, 'wall_BC_flag':wall_BC_off_flag} 
# dzz_zeta: could try neumann LBC. Upper BC irrotational (no-stress).
dzz_zeta,lBC = fn.diff_matrix( grid_params_dzz , 'dirchlet' , 'dirchlet' , diff_order=2 , stencil_size=3 ) # non-dimensional
# inv_psi: lower BCs are no-slip, impermiable, upper BC is impermiable, free-slip
eye_matrix = np.eye( Nz , Nz , 0 , dtype=complex ) #np.ones([Nz,Nz],dtype=complex) A BIG DIFFERENCE!


# all parts of the forcing need to be complex arrays:
dzz_zeta = np.multiply(dzz_zeta,np.ones(np.shape(dzz_zeta)),dtype=complex)
#inv_psi = np.multiply(inv_psi,np.ones(np.shape(inv_psi)),dtype=complex)
lBC = lBC + 0.j


M = np.zeros([Nj,Ni]);
Mr = np.zeros([Nj,Ni]);
Mi = np.zeros([Nj,Ni]);

MP = np.zeros([Nj,Ni]);
MrP = np.zeros([Nj,Ni]);
MiP = np.zeros([Nj,Ni]);

print('\nGrid:',grid_flag)
print('Nz/H:',Nz/H)
for i in range(0,Ni):
    for j in range(0,Nj):

        print('\nReynolds number: %.1f' %(Rej[j]) )
        print('disturbance wavenumber: %.2f' %(ai[i]) )
        print('H: %.1f' %(H), 'Nz: %i' %(Nz), 'CFL: %.2f' %(CFL) )

        Re = Rej[j]
        a = ai[i]
        U = Re * (nu/dS) # Re = U*dS/nu, so ReB=Re/2
    
        #dt = CFL*(np.amin(dz)/Re) 
        dt = CFL*(z[0]/Re) 
        Nt = int(2.*np.pi/dt)
      
        freq = int(Nt/10)
        print('number of time steps, Nt = ',Nt)

        # pre-constructed matrices:
        dzz_psi = fn.diff_matrix( grid_params_inv , 'dirchlet' , 'dirchlet' , diff_order=2 , stencil_size=3 )
        dzz_psi = np.multiply(dzz_psi,np.ones(np.shape(dzz_psi)),dtype=complex)
        inv_psi = np.linalg.inv( dzz_psi - (a**2.*eye_matrix) ) 
        A0 = np.zeros( [Nz,Nz] , dtype=complex ) # initial propogator matrix 

        phi_path = '/home/bryan/git_repos/Floquet/figures/phi/'
        psi_path = '/home/bryan/git_repos/Floquet/figures/psi/'
        #phi_path = '/home/bryan/Desktop/Floquet/figures/phi/'
        #psi_path = '/home/bryan/Desktop/Floquet/figures/psi/'
        params = {'nu': nu, 'omg': omg, 'T': T, 'Td':T, 'U': U, 'inv_psi':inv_psi, 'plot_freq':plot_freq, 
          'Nz':Nz, 'Nt':Nt, 'Re':Re,'a':a, 'H':H, 'Hd':Hd, 'dzz_zeta':dzz_zeta, 'CFL':CFL, 'A0':A0,
          'dS':dS, 'z':z, 'dz':dz, 'eye_matrix':eye_matrix,'freq':freq, 'lBC':lBC, 'phi_path':phi_path, 'psi_path':psi_path} 

        Nc = count_points( params )
        print('number of points within delta = %i' %(Nc))

        Phi0 = np.eye(int(Nz),int(Nz),0,dtype=complex) # initial condition (prinicipal fundamental solution matrix)

        if ic_plot_flag == 1.: 
            # Plot of initial streamfunction and vorticity
            Psi0 = np.real(np.dot(params['inv_psi'],Phi0))
            H = params['H']
            plotname = params['psi_path'] +'ic.png' #%(count)
            fig = plt.figure(figsize=(16,4.5))
            plt.subplot(131); plt.plot(Psi0,params['z'],'b')
            plt.xlabel(r"$\Psi$",fontsize=13); plt.ylabel(r"$z/H$",fontsize=13)
            plt.ylim([-1.,H]); plt.grid()
            plt.subplot(132); plt.plot(Psi0,params['z'],'b')
            plt.xlabel(r"$\Psi$",fontsize=13); plt.ylabel(r"$z/H$",fontsize=13) 
            plt.axis([-5.,5.,-0.001,H/500.]); plt.grid()
            plt.subplot(133); plt.semilogy(Psi0,params['z'],'b')
            plt.xlabel(r"$\Psi$",fontsize=13); plt.ylabel(r"$z/H$",fontsize=13)
            plt.axis([-10,10,1e-2,H]); plt.grid()
            plt.savefig(plotname,format="png"); plt.close(fig);

            H = params['H']
            plotname = params['phi_path'] +'ic.png' #%(count)
            fig = plt.figure(figsize=(16,4.5))
            plt.subplot(131); plt.plot(np.real(Phi0),params['z'],'b')
            plt.xlabel(r"$\Phi$",fontsize=13); plt.ylabel(r"$z/H$",fontsize=13)
            plt.ylim([-1.,H]); plt.grid()
            plt.subplot(132); plt.plot(np.real(Phi0),params['z'],'b')
            plt.xlabel(r"$\Phi$",fontsize=13); plt.ylabel(r"$z/H$",fontsize=13) 
            plt.axis([-5.,5.,-0.001,H/500.]); plt.grid()
            plt.subplot(133); plt.semilogy(np.real(Phi0),params['z'],'b')
            plt.xlabel(r"$\Phi$",fontsize=13); plt.ylabel(r"$z/H$",fontsize=13)
            plt.axis([-1.1*np.amax(abs(np.real(Phi0[0:10]))),1.1*np.amax(abs(np.real(Phi0[0:10]))),1e-2,H]); plt.grid()
            plt.savefig(plotname,format="png"); plt.close(fig);

        Phin,final_time = fn.rk4_time_step( params, Phi0 , T/Nt, T , 'blennerhassett' )
        Fmult = np.linalg.eigvals(Phin)
        M[j,i] = np.amax(np.abs(Fmult)) # maximum modulus, eigenvals = floquet multipliers
        Mr[j,i] = np.amax(np.real(Fmult))
        Mi[j,i] = np.amax(np.imag(Fmult))
        print('\nmaximum modulus Phi = ',M[j,i])
        print('\nmaximum real mu Phi = ',Mr[j,i])      
        print('\nmaximum imag mu Phi = ',Mi[j,i]) 

        #Psin = np.real(np.dot(params['inv_psi'],Phin))
        Fmult_Psi = np.linalg.eigvals(np.dot(params['inv_psi'],Phin))
        MP[j,i] = np.amax(np.abs(Fmult_Psi)) # maximum modulus, eigenvals = floquet multipliers
        MrP[j,i] = np.amax(np.real(Fmult_Psi))
        MiP[j,i] = np.amax(np.imag(Fmult_Psi))
        print('\nmaximum modulus Psi = ',MP[j,i])
        print('\nmaximum real mu Psi = ',MrP[j,i])      
        print('\nmaximum imag mu Psi = ',MiP[j,i]) 
        # add plots of psi final solutions

        if email_flag == 1:
            Fmult = np.array2string(Fmult, precision=6, separator=',',suppress_small=True)
            Fmult_Psi = np.array2string(Fmult_Psi, precision=6, separator=',',suppress_small=True)
            message = """\
            Subject: data k = %.3f Re = %.1f

            Nz = %i\n
            CFL = %.3f\n
            maximum modulus zeta = %.3f\n 
            maximum modulus psi = %.3f\n zeta multiplier:\n""" %(ai[i],Rej[j],Nz,CFL,M[j,i],MP[j,i])
            message = message + Fmult + """\n psi multiplier:\n""" + Fmult_Psi
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)


print('Reynolds number range = ',Rej)
print('wavenumber range = ', ai)
print('Nz = ',Nz)
print('CFL = ',CFL)
print('Grid = ',grid_flag)
print('number of points within delta = %i' %(Nc))
print('\nmaximum modulus Phi = ',M)
print('\nmaximum modulus Psi = ',MP)
h5_filename = stat_path + "multiplier_Re%i_Re%i_a%i_a%i.h5" %(Rej[0],Rej[Ni-1],int(ai[0]*1000),int(ai[Nj-1]*1000))
print(h5_filename)
f2 = h5py.File(h5_filename, "w")
dset = f2.create_dataset('CFL', data=CFL, dtype='f8')
dset = f2.create_dataset('Nz', data=Nz, dtype='f8')
dset = f2.create_dataset('H', data=H, dtype='f8')
dset = f2.create_dataset('M', data=M, dtype='f8')
dset = f2.create_dataset('MP', data=MP, dtype='f8')
dset = f2.create_dataset('Mr', data=M, dtype='f8')
dset = f2.create_dataset('MrP', data=MP, dtype='f8')
dset = f2.create_dataset('Mi', data=M, dtype='f8')
dset = f2.create_dataset('MiP', data=MP, dtype='f8')
print('\nMultipliers computed and written to file' + h5_filename + '.\n')

