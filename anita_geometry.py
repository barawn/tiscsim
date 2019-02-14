##ANITA-IV antenna positions and orientation:
#---EJO 11/2016
#---

import numpy as np

#antenna names / array organization
phisector=[]
loc=[]
for j in ['T', 'M', 'B']:
    for i in range(16):
        phisector.append(i+1)
        loc.append(j)

#phi, degrees
phi_ant=np.array([0,22.5,45,67.5,90,112.5,135,157.5,180,202.5,225,247.5,270,292.5,315,337.5,
     0,22.5,45,67.5,90,112.5,135,157.5,180,202.5,225,247.5,270,292.5,315,337.5,
     0,22.5,45,67.5,90,112.5,135,157.5,180,202.5,225,247.5,270,292.5,315,337.5]	) 		     

#radial position, meters
r_ant=np.array([0.9675,0.7402,0.9675,0.7402,0.9675,0.7402,0.9675,0.7402,
   0.9675,0.7402,0.9675,0.7402,0.9675,0.7402,0.9675,0.7402,
   2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,
   2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,
   2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,
   2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,2.0447,2.0447])

#vertical position, meters
z_ant=np.array([-1.4407,-2.4135,-1.4407,-2.4135,-1.4407,-2.4135,-1.4407,-2.4135,
   -1.4407,-2.4135,-1.4407,-2.4135,-1.4407,-2.4135,-1.4407,-2.4135,
   -5.1090,-5.1090,-5.1090,-5.1090,-5.1090,-5.1090,-5.1090,-5.1090,
   -5.1090,-5.1090,-5.1090,-5.1090,-5.1090,-5.1090,-5.1090,-5.1090,
   -6.1951,-6.1951,-6.1951,-6.1951,-6.1951,-6.1951,-6.1951,-6.1951,
   -6.1951,-6.1951,-6.1951,-6.1951,-6.1951,-6.1951,-6.1951,-6.1951])

x_ant = r_ant * np.cos(np.radians(phi_ant)) # Antenna x positions (m)
y_ant = r_ant * np.sin(np.radians(phi_ant)) # Antenna y positions (m)

#theta, degrees
theta_ant=-10.*np.ones(len(z_ant))

def drawAnita():
    import myplot    
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_ant, y_ant, z_ant, marker='s', color='gray', alpha=.7, s=120)

    plt.figure(figsize=(6,8))
    plt.plot(x_ant, z_ant, 's', color='gray', ms=30, alpha=.7)
    plt.xlabel('ANITA x [m]')
    plt.ylabel('ANITA z [m]')
    plt.ylim([-8, 0])
    plt.show()

if __name__=='__main__':
    drawAnita()
