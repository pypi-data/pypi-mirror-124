#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from numpy import linalg as LA
import numpy as np
def shape(dt):
    return dt.shape[0],dt.shape[1],dt.shape[2],dt.shape[3]
def transpose(x): 
    a11 = x[0,0]
    a12 = x[0,1]
    a13 = x[0,2]
    a21 = x[1,0]
    a22 = x[1,1]
    a23 = x[1,2]
    a31 = x[2,0]
    a32 = x[2,1]
    a33 = x[2,2]
    x = np.array([[a11,a21,a31],[a12,a22,a32],[a13,a23,a33]])
    return x
def muiltiply(x,y):
    a11 = x[0,0]*y[0,0]+x[0,1]*y[1,0]+x[0,2]*y[2,0]
    a12 = x[0,0]*y[0,1]+x[0,1]*y[1,1]+x[0,2]*y[2,1]
    a13 = x[0,0]*y[0,2]+x[0,1]*y[1,2]+x[0,2]*y[2,2]
    a21 = x[1,0]*y[0,0]+x[1,1]*y[1,0]+x[1,2]*y[2,0]
    a22 = x[1,0]*y[0,1]+x[1,1]*y[1,1]+x[1,2]*y[2,1]
    a23 = x[1,0]*y[0,2]+x[1,1]*y[1,2]+x[1,2]*y[2,2]
    a31 = x[2,0]*y[0,0]+x[2,1]*y[1,0]+x[2,2]*y[2,0]
    a32 = x[2,0]*y[0,1]+x[2,1]*y[1,1]+x[2,2]*y[2,1]
    a33 = x[2,0]*y[0,2]+x[2,1]*y[1,2]+x[2,2]*y[2,2]
    x = np.array([[a11,a21,a31],[a12,a22,a32],[a13,a23,a33]])
    return x
def trace(x):
    tra = (x[0,0]*x[1,1]*x[2,2])
    return tra
def lambmatrix(S,Ome,nz,ny,nx):
    from numpy import linalg as LA
    lamb2 = np.zeros((nz,ny,nx),dtype=np.float32)
    for k in range(0,nz):
                for j in range(0,ny):
                    for i in range(0,nx):
                        w = LA.eigvals(S[:,:,k,j,i].dot(S[:,:,k,j,i])+Ome[:,:,k,j,i].dot(Ome[:,:,k,j,i]))
                        w = np.sort(w)
                        if w[1]<0:
                            lamb2[k,j,i] = w[1]
    return lamb2
def lambda2(datau,datav,dataw,dz,dy,dx,t):
    from numpy import linalg as LA
    nt,nz,ny,nx = shape(datau)         
    print(t)
        
    dudy,dudz,dudx= np.gradient(datau[t,:,:,:],dz,dy,dx)
    dvdy,dvdz,dvdx = np.gradient(datav[t,:,:,:],dz,dy,dx)
    dwdy,dwdz,dwdx = np.gradient(dataw[t,:,:,:],dz,dy,dx)

    J = np.array([[dudz,dudy,dudx],[dvdz,dvdy,dvdx],[dwdz,dwdy,dwdx]])
    JT = transpose(J)
    S = (J+JT)*0.5
    Ome = (J-JT)*0.5
    lamb2 = lambmatrix(S,Ome,nx,ny,nz)
    return lamb2

