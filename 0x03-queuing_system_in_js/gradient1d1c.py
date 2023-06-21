#!/usr/bin/env python3

import numpy as np
from numpy import log
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


################################################################################
################################################################################
################################################################################
first_five = np.linspace(1, 6, 41)
next_fifteen = np.linspace(6, 21, 61)
last_eighty = np.linspace(21, 101, 21)
nodes = np.concatenate((first_five, next_fifteen, last_eighty))
nodes = np.unique(nodes)
NGRID = len(nodes)
print(f'number of nodes = {NGRID}')
le = np.diff(nodes)
num_elem = len(le)

def get_laplacian(n):
  kn = np.zeros(NGRID)
  kn[0] = n[0]
  for i in range(1,NGRID-1):
    kn[i] = -n[i-1]/le[i-1] + (1/le[i-1] + 1/le[i])*n[i] - n[i+1]/le[i]
  kn[-1] = -n[-2]/le[-2] + n[-1]/le[-2]
  return kn

def get_nonlinear(x):
  nonlinear = np.zeros(NGRID)
  nonlinear[0] = 0
  nonlinear[-1] = le[-2]/4*x[-2] + le[-2]/4*x[-1] 
  for i in range(1,NGRID-1):
    nonlinear[i] = le[i-1]/6*x[i-1] + (le[i-1]/3 + le[i]/3)*x[i] + le[i]/6*x[i+1]
  return nonlinear


################################################################################
def get_mures(n, T):
    term1 = T*( - log(1 - n) + n/(1 - n))
    term2 = np.log((1+(1+np.sqrt(2.0))*n)/((1+(1-np.sqrt(2.0))*n))) / (2**1.5)
    term3 = n/(1+2*n-n**2)
    return term1 - term2 - term3

def get_u(z):
    zinv = d/z
    repul = zinv**9 / 45.0
    attr = zinv**3 / 6.0
    pot = W*(repul - attr)
    return pot

W = 6.4
d = 1
T = 0.160
nBulk = 0.1165



################################################################################
def residual(n):

  F = []

  
  kn = get_laplacian(n)
  
  nonlinear_g = np.zeros(NGRID)
  for i in range(NGRID):

    ideal = 0.0
    if (i>0):
      ideal = T*np.log(n[i]/nBulk) + get_u(nodes[i])
    Delta_mu_res = get_mures(n[i], T) - get_mures(nBulk, T)
    nonlinear_g[i] = ideal + Delta_mu_res 

  nonlinear = get_nonlinear(nonlinear_g)    

  for i in range(NGRID):
    F.append( kn[i] + nonlinear[i] )


    
  return F


################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
  
  first_five = np.linspace(1, 6, 41)
  next_fifteen = np.linspace(6, 21, 61)
  last_eighty = np.linspace(21, 101, 21)
  nodes = np.concatenate((first_five, next_fifteen, last_eighty))
  nodes = np.unique(nodes)

  
  nGuess = [0.1165]*NGRID
  

  z = fsolve(residual, nGuess)
  plt.plot(nodes, z);
  plt.xlim(0, 28)
  plt.ylim(0, 0.3)
  plt.xlabel("DISTANCE FROM WALL, x")
  plt.ylabel("DENSITY, n")
  plt.show()
  

################################################################################
################################################################################
################################################################################
  
