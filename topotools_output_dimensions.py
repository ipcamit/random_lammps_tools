import os
import sys

filename = sys.argv[1]
if not os.path.exists(str(filename)):
    print "file does not exist"
    exit()
filename = str(filename)    
shall_i_start=0
x=[99999.0,-99999.0] #assuming dimensions of box remain between 99999 and -99999, why would it be more?
y=[99999.0,-99999.0]
z=[99999.0,-99999.0]
lines_passed=1
#i=0
with open(filename,'r') as f:
    f.readline()
    total_atoms = int(f.readline().split()[0]) #assuming second line is total number of atoms. as is the case in topotools
    for line in f:
#        i+=1
        if shall_i_start==1:
            if lines_passed>total_atoms:
                print "all done!"
                break
            coord=line.split()
            if float(coord[4])<x[0]:
                x[0]=float(coord[4])
            if float(coord[4])>x[1]:
                x[1]=float(coord[4])
            if float(coord[5])<y[0]:
                y[0]=float(coord[5])
            if float(coord[5])>y[1]:
                y[1]=float(coord[5])
            if float(coord[6])<z[0]:
                z[0]=float(coord[6])
            if float(coord[6])>z[1]:
                z[1]=float(coord[6])
            lines_passed += 1
        if (line == ' Atoms\n') and (shall_i_start==0):
            f.next()
            shall_i_start=1
#        if i>60000:
#            break
print " %f  %f xlo xhi\n %f  %f ylo yhi\n %f  %f zlo zhi" %(x[0]-0.79,x[1]+0.79,y[0]-0.79,y[1]+0.79,z[0]-1,z[1]+1)

#print x[0],x[1]