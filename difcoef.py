"""
Diffusion Coefficient Calculator
(note: with values of a=.55 eta=0.892 @ 25*C=278K A=1.66)
("     " : a=.555 ... A=1.64, "     "; a=0.5 ... A=1.82)
Using laser thermometer I saw temps of 27-30*C consistently
across the slide after ~15 minutes of runtime at full brightness. I have substited values according to 
79F=26.1C=279K
77F=25C=278K
"""
import numpy as np

Kb=1.380649*10**-23  #[J/K] source: wikipedia commons
pi=np.pi
eta=0.892*10**-3  ##[Pa] @27*C  source:hyperphysics viscosity tables
a=.5*10**-6    ##1 micrometer particle diameter 
T=input("Enter Temperature: ")
print("Temperature:"+str(T))

D=(Kb*T)/(6*pi*eta*a)
print(D)

A=D*4
print(A*10**12)


