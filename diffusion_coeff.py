'''python "diffusion_coeff.py <dump_file_name> <atom_id atom_mass> <Total number of atoms in molecule> [-region from_x to_x from_y to_y from_z to_z]"'''
import os
import sys
import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#import pdb
from copy import deepcopy

try:
    variables = sys.argv
    region_specified = True
    region_position = variables.index('-region')
    region = sys.argv[region_position+1:len(sys.argv)]
    del sys.argv[region_position:len(sys.argv)]
except ValueError:
    print "No region specified, all molecules will be considered\n"
    region_specified = False


total_variables = len(sys.argv)


atoms = {}
atom_list = []


atoms_length = int(sys.argv[-1])
del sys.argv[-1]

for i in range(2,len(sys.argv),2):
    atoms[float(sys.argv[i])]=float(sys.argv[i+1])                              
    ##create dictionary for saving mass of each atom type
    atom_list.append(sys.argv[i])

timesteps=[]
positions=[]
frame=1
distance_array=[]

in_frame= False
with open(sys.argv[1]) as data_file:
    try:
        while True:
            data_COM=[]
            data_file.readline() #skipping lines of texts
            if frame == 1:                                                  
            #only do it for first frame, else skip 2 lines as they have already taken care of in :line 75
                timesteps.append(int(data_file.readline()))
            data_file.readline() #skipping lines of texts
            if frame == 1:
                number_of_atoms = int(data_file.readline())
            data_file.readline() #skipping lines of texts
            if frame == 1:    
                pp_x = map(float,data_file.readline().split()) #skipping lines of texts
                pp_y = map(float,data_file.readline().split())#skipping lines of texts
                pp_z = map(float,data_file.readline().split())#skipping lines of texts
            else:
                data_file.readline()
                data_file.readline()
                data_file.readline()
            data_file.readline() #skipping lines of texts
            in_frame = True
            counter=1
            while in_frame:                                                      
            #while in same frame
                next_mol=data_file.readline().split()
                if next_mol[1] in atom_list:
                    coord=[]                                                      
                    ##create empty list for coord
                    coord.append(map(float,next_mol[1:5]))
                    for i in range(atoms_length-1):
                       coord.append(map(float,data_file.readline().split()[1:5])) 
                       ##read the coordinates o single molecule, convert it to fload and save in 'coord' list
                    comX=0
                    comY=0
                    comZ=0
                    molecular_mass=0
                    for atom in coord:                                             
                    #find centre of mass for a molecule and append it to data_COM list
                        comX += atom[1]*atoms[atom[0]]
                        comY += atom[2]*atoms[atom[0]]
                        comZ += atom[3]*atoms[atom[0]]
                        molecular_mass+=atoms[atom[0]]
                    data_COM.append([comX/molecular_mass,comY/molecular_mass,comZ/molecular_mass])
                    counter+=1
                else:
                    if next_mol[1]=='TIMESTEP':
                        timesteps.append(int(data_file.readline()))                 
                        ## if TIMESTEP word is encountered it mean one frame finished hence set in_frame =false
                        in_frame = False                                            
                        ## to breakout of COM calculation of 1 frame 
            if frame != 1:
                xyz_data=np.array(frame0 - np.array(data_COM))                      
                ##if first frame then set it as refernce (frame0) else calculate and append distance to list
                xyz=xyz_data[:,0]**2+xyz_data[:,1]**2+xyz_data[:,2]**2
                distance_array.append(xyz)
            else:
                number_of_molecules_in_group = len(data_COM)
                frame0 = np.array(data_COM)
            
            frame += 1
    except IndexError:
        pass    
data_file.close()
total_data_points = frame -2 
# first and last are ignored as first is zero and last is just an increment

time = np.cumsum(np.array([timesteps[i+1]-timesteps[i] for i in range(len(timesteps)-1)]))
t = np.delete(time,-1)
#plt.hold()
####Get proper regios for folded trajectories
###Begin
pp_frame0=deepcopy(frame0);

total_pp_sum  =  np.sum(np.where(pp_frame0<pp_x[0])) \
             + np.sum(np.where(pp_frame0>pp_x[1])) \
             + np.sum(np.where(pp_frame0<pp_y[0])) \
             + np.sum(np.where(pp_frame0>pp_y[1])) \
             + np.sum(np.where(pp_frame0<pp_z[0])) \
             + np.sum(np.where(pp_frame0>pp_z[1]))
dif_pp_sum = total_pp_sum

x_pp_delta = pp_x[1] - pp_x[0]
y_pp_delta = pp_y[1] - pp_y[0]
z_pp_delta = pp_z[1] - pp_z[0]

while dif_pp_sum!=0: 
#check if all COM are within periodic boundary    
    mask = np.where(pp_frame0[:,0] < pp_x[0])
    pp_frame0[np.transpose(mask),0]+= x_pp_delta
    mask = np.where(pp_frame0[:,1] < pp_y[0])
    pp_frame0[np.transpose(mask),1]+= y_pp_delta
    mask = np.where(pp_frame0[:,2] < pp_z[0])
    pp_frame0[np.transpose(mask),2]+= z_pp_delta
    #if less than minima then add maxima
    mask = np.where(pp_frame0[:,0] > pp_x[1])
    pp_frame0[np.transpose(mask),0]-= x_pp_delta
    mask = np.where(pp_frame0[:,1] > pp_y[1])
    pp_frame0[np.transpose(mask),1]-= y_pp_delta
    mask = np.where(pp_frame0[:,2] > pp_z[1])
    pp_frame0[np.transpose(mask),2]-= z_pp_delta
    #if greater then maxima then subtract maxima and add minima
    
    new_total_pp_sum = np.sum(np.where(pp_frame0<pp_x[0])) \
                 + np.sum(np.where(pp_frame0>pp_x[1])) \
                 + np.sum(np.where(pp_frame0<pp_y[0])) \
                 + np.sum(np.where(pp_frame0>pp_y[1])) \
                 + np.sum(np.where(pp_frame0<pp_z[0])) \
                 + np.sum(np.where(pp_frame0>pp_z[1])) 
    dif_pp_sum = total_pp_sum - new_total_pp_sum
    total_pp_sum = new_total_pp_sum
    #for some reason RHS is not going to zero. hence when it converges, loop will break
    
    #print dif_pp_sum


z_min=np.amin(pp_frame0[:,2])
print pp_z[0], z_min
z_max=np.amax(pp_frame0[:,2])
print pp_z[1], z_max
##End

if region_specified:
    region_sieve= np.zeros(number_of_molecules_in_group)
    region = map(float,region)
    for i in xrange(len(pp_frame0)):    #initial position of molecules
        if region[0] <= pp_frame0[i][0] and pp_frame0[i][0] <= region[1] \
        and region[2] <= pp_frame0[i][1] and pp_frame0[i][1] <= region[3]\
        and region[4] <= pp_frame0[i][2] and pp_frame0[i][2] <= region[5]:
            region_sieve[i]=1
else:
    region_sieve= np.ones(number_of_molecules_in_group)
    region=[0,0] # for filename purposes

average_msd=np.zeros(total_data_points)

for i in range(number_of_molecules_in_group):
    data_for_plotting=[]
    for j in range(total_data_points): 
        data_for_plotting.append(distance_array[j][i]*region_sieve[i])
    average_msd+=np.array(data_for_plotting)
#    plt.plot(np.array(data_for_plotting))   ##comment out these lines to see all individual MSD
#plt.show()

average_msd=average_msd/np.count_nonzero(region_sieve)
#plt.plot(average_msd) ## comment out these lines to plot average MSD of the region
#plt.show()

print "timestep between two data points as 1.00 ps; if not please modify line 122, char 54 and line 126 char 56 accordingly (= timestep)"

df_fit=np.polyfit(np.arange(1.00,total_data_points+1,1.00),average_msd[0:total_data_points],1)/6
print "Diffusion coeff =%f Angstrom^2/ps" %(df_fit[0])



filename = "file_type_"+'_'.join(map(str,atom_list))+'_region_xyz_'+'_'.join(map(str,region))+'.dat'
with open(filename,'w') as data_file:
    for x,y in zip(np.arange(1.00,total_data_points+1,1.00),average_msd[0:total_data_points]):       #*******Modify Accordingly********
        data_file.write(str(x)+'    '+str(y)+'\n')
data_file.close()

#fig = plt.figure()                                    ##comment out these lines to see Centre of mass of selected molecules
#ax = fig.add_subplot(111, projection='3d')
#for i in xrange(len(frame0)):
#    frame0[i]*=region_sieve[i]
#ax.scatter(frame0[:,0],frame0[:,1],frame0[:,2])
#plt.show()#
