import numpy as np
from scipy.constants import R
from scipy.constants import Avogadro as Na
A=input("Enter A value: ")
#R=8.314462618
pi=np.pi
eta=0.892*10**-3
r=.495*10**-6
T=295
N=(4*R*T)/(6*pi*eta*float(A)*r)
print(N)
print(Na/N*10**-12)


Gas=(6*pi*eta*float(A)*10**-12*r*Na)/(4*T)
print(Gas)
print(Gas/R)
