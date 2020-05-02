#from __future__ import division, unicode_literals, print_function  # for compatibility with Python 3 and 3

import pims
import matplotlib.pyplot as plt
import matplotlib as mpl
import trackpy as tp


### DEFINE INPUT PARAMETERS ###

diameter=input("Enter particle diameter: ")    ##input var is a string
diameter=float(diameter)
#print("Diameter="+str(aa))

last=input("Input Number of image Frames: ")   ##input number of frames for batch process 
last=int(last)
#print("# of Frames:"+str(last))
#T=input("Enter Temperature in Kelvin:")
#print("Temperature="+str(T))




### Import Images   ###

frames=pims.ImageSequence('40Data/Sample3/Video4/images*.png', as_grey=True)     ##import images using pims
plt.imshow(frames[0])    	 ##show the first frame
#print(frames[0]) 		##print the matrix values of the first frame

#####



### 	DEFAULT FEATURE FINDING ROUTINE    ###
plt.figure()
f=tp.locate(frames[0],diameter,minmass=250,invert=True)  ##locates features based on args
#f = tp.locate(frames[0],diameter = , minmass=400.0, maxsize=None, separation=50, noise_size=1,percentile=99, smoothing_size=None,threshold=None,invert=True, topn=None, preprocess= True, max_iterations=10, filter_before=None, filter_after=True, characterize=True)
tp.annotate(f,frames[0])  ##annotates first frame based on default args
plt.show()

####

print(f.head())  ##prints the first 10 lines of image data
print(f.tail())  ## 	       last 10 lines


##prints a histogram of mass values (we should use this to choose min mass value)
fig, ax =plt.subplots()
ax.hist(f['mass'],bins=20)  
ax.set(xlabel='mass',ylabel='count')
ax.set_title("Mass Histogram")
plt.show()     
##note this should be a relative Gaussian distribution
##using this we can set the min mass value




### USER INPUT FOR FEATURE FINDING ###

mass=input("Enter particle brightness: ")     ##minimum brightness to track (~1500)
mass=float(mass)
#print("Min. Brightness="+str(mass))


###VISUAL FEATURE FINDING ROUTINE

R=tp.locate(frames[0],diameter,minmass=mass,invert=True)  ##user define feature params

plt.figure()
tp.annotate(R,frames[0])    		##circle the 'features' in the frame
tp.subpx_bias(R)    			##check x,y displacement distrobution
plt.show()


##Batch Processes ##
#perform same feature finding but on frames 0:last
L=tp.batch(frames[:last],diameter,minmass=mass,invert=True)


##link trajectories using memory
tra=tp.link_df(L,5,memory=2)    		 ##max displacement b/w frames, memory b/w frames
print(tra.head())    
print(tra.tail())

memory=float(last*(.95))     ##set memory to be 80% of total frames

tra1=tp.filter_stubs(tra,memory)   		##keep only trajectories that last 80% of frames


##trajectory Filtering##
print('Before filter:', tra['particle'].nunique())    
print('After filter:', tra1['particle'].nunique())



plt.figure()
tp.mass_size(tra1.groupby('particle').mean());  ##plots size vs mass




fig,(ax1,ax2,ax3)=plt.subplots(1,3)
fig.suptitle("Trajectories with/without Overall Drift")


plt.figure()
tp.plot_traj(tra1);




d =tp.compute_drift(tra1)    			##subtract overall drift from trajectory
d.plot()
plt.show()
tm=tp.subtract_drift(tra1.copy(),d)   		##plot filtered trajectory
ax=tp.plot_traj(tm)
plt.show()


##MSD Calculation and Plot
im=tp.imsd(tm,1/5.,60)    ##microns per pixel, frames per second=60
fig, ax = plt.subplots()
ax.plot(im.index, im, 'k-', alpha=0.1)  # black lines, semitransparent
ax.set(ylabel=r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]',
       xlabel='lag time $t$',title='MSD')
ax.set_xscale('log')
ax.set_yscale('log')



##Total Ensemble MSD and Plot
em=tp.emsd(tm,1/5.,60)
fig, ax = plt.subplots()
ax.plot(em.index, em, 'o-')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set(ylabel=r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]', xlabel='lag time $t$', title='Ensemble MSD')
ax.set(ylim=(1e-2, 10));




##Fitting the EMSD

#plt.figure()
plt.ylabel(r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]')
plt.title("EMSD Fit")
plt.xlabel('lag time $t$');
print(tp.utils.fit_powerlaw(em))  # performs linear best fit in log space, plots]
print("Diamter:",diameter)
print("Mass:",mass)
print("Frames:",last)


