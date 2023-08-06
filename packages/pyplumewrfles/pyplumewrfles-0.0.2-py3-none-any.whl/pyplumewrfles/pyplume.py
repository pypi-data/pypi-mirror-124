#!/usr/bin/env python
# coding: utf-8


import numpy as np
import time

def version():
    print("Version 0.0002");

#Transpose of 3x3 matrix
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

#multiply of 3x3 matrices
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

#trace of 3x3 matrix(AT A)
def trace(x):
    tra = (x[0,0]*x[1,1]*x[2,2])
    return tra


def timemean(data):
    wmean = np.mean(data,0)
    wmean = np.squeeze(wmean)
    return wmean

def centermean(data):
    mean = timemean(data)
    del data
    a = np.int(np.ceil(mean.shape[0]/2))
    b = np.int(np.floor(mean.shape[0]/2))
    c = np.int(np.ceil(mean.shape[1]/2))
    d = np.int(np.floor(mean.shape[1]/2))
    if(a == b and c == d):                   #even even
        wc1 = mean[a,c,:]
        wc2 = mean[a,c-1,:]
        wc3 = mean[a-1,c-1,:]
        wc4 = mean[a-1,c,:]
        wc = (wc1+wc2+wc3+wc4)/4
    if(a != b and c == d):                   #odd even
        wc1 = mean[b,c,:]
        wc2 = mean[b,c-1,:]
        wc = (wc1+wc2)/2
    if(a == b and c != d):                   #even odd
        wc1 = mean[b,d,:]
        wc2 = mean[b-1,d,:]
        wc = (wc1+wc2)/2
    if(a!=b and c!=d):
        wc = mean[b,d,:]
    return wc       

def percentage(t,nt):
    percent = np.str(np.round(t/nt*100))+"%"
    print('{}\r'.format(percent), end="")


def omega_single(datau,datav,dataw,dz,dy,dx,t):
    nt = datau.shape[0]
    percentage(t,nt)

    gu = np.gradient(datau[:,:,:,t],dz,dy,dx)
    gv = np.gradient(datav[:,:,:,t],dz,dy,dx)
    gw = np.gradient(dataw[:,:,:,t],dz,dy,dx)
    
    GV = np.array([[gu[2],gv[2],gw[2]],[gu[0],gv[0],gw[0]],[gu[1],gv[1],gw[1]]])
    GVT = transpose(GV)

    A = 0.5*(GV+GVT)
    B = 0.5*(GV-GVT)
    AT = transpose(A)
    BT = transpose(B)
    ATA = muiltiply(AT,A)
    BTB = muiltiply(BT,B)
    a = trace(ATA)
    b = trace(BTB)
    ef=0.001*np.max(b-a)
    result = (b/(a+b+ef))
    return result


def omega(datau,datav,dataw,dz,dy,dx):
    if (sameshape3(datau,datav,dataw) is False):
        return
    np.seterr(divide='ignore', invalid='ignore')
    ome=np.zeros((datau.shape[0],datau.shape[1],datau.shape[2],datau.shape[3]),dtype=np.float32)
    for t in range(0,datau.shape[3]):
        ome[t,:,:,:] = omega_single(datau,datav,dataw,dx,dy,dz,t)
    ome = np.nan_to_num(ome)
    print('Omega Vortex Identification Completed')
    return ome


def vorticity(datau,datav,dataw,dt,dz,dy,dx):
    if (sameshape3(datau,datav,dataw) is False):
        return

    gu = np.gradient(datau,dt,dz,dy,dx)
    gu1 = np.array(gu[1],dtype =np.float32)
    gu2 = np.array(gu[0],dtype =np.float32)
    del gu
    
    gv = np.gradient(datav,dt,dz,dy,dx)
    gv0 = np.array(gv[2],dtype =np.float32)
    gv2 = np.array(gv[0],dtype =np.float32)
    del gv
    
    gw = np.gradient(dataw,dt,dz,dy,dx)
    gw0 = np.array(gw[2],dtype =np.float32)
    gw1 = np.array(gw[1],dtype =np.float32)
    del gw
    
    omgx = (gw1-gv2)
    del gw1, gv2
    omgy = (gu2-gw0)
    del gu2, gw0
    omgz = (gv0-gu1)
    del gv0,gu1
    
    vor = np.array([omgz,omgy,omgx])
    return vor

def lamb2sec(datau,datav,dataw,dz,dy,dx,nt):
    import multifluidlab
    import multiprocessing as mp
    from multiprocessing import Pool
    nt,nz,ny,nx = shape(datau)
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(multifluidlab.lambda2,[(datau,datav,dataw,dz,dy,dx,t) for t in range(nt)])
    lamb2=np.zeros((nt,nz,ny,nx),dtype=np.float32)
    for t in range(nt):
        lamb2[t,:,:,:] = results[t]     
    return lamb2

def lambda2multicore(datau,datav,dataw,dz,dy,dx):
    import multiprocessing as mps
    nt,nz,ny,nx = shape(datau)
    lamb2=np.zeros((nt,nz,ny,nx),dtype=np.float32)
    sectime =24
    nts = 0
    nte = nts+sectime
    while (nts < nt):
        percentage(nts,nt)
        u = datau[nts:nte,:,:,:]
        v = datav[nts:nte,:,:,:]
        w = dataw[nts:nte,:,:,:]
        temp = lamb2sec(u,v,w,dz,dy,dx,nte-nts)
        for i in range (nts,nte):
            j = i-nts
            lamb2[i,:,:,:] = temp[j,:,:,:]
        nts = nte 
        nte = nts + sectime
        if (nte > nt):
            nte = nt   
    return lamb2

def lambda2single(datau,datav,dataw,dz,dy,dx,t):
    from numpy import linalg as LA
    import multifluidlab
    nt,nz,ny,nx = shape(datau)        
        
    dudy,dudz,dudx= np.gradient(datau[t,:,:,:],dz,dy,dx)
    dvdy,dvdz,dvdx = np.gradient(datav[t,:,:,:],dz,dy,dx)
    dwdy,dwdz,dwdx = np.gradient(dataw[t,:,:,:],dz,dy,dx)

    J = np.array([[dudz,dudy,dudx],[dvdz,dvdy,dvdx],[dwdz,dwdy,dwdx]])
    JT = transpose(J)
    S = (J+JT)*0.5
    Ome = (J-JT)*0.5
    lamb2 = multifluidlab.lambmatrix(S,Ome,nz,ny,nx)
    return lamb2

def lambda2(datau,datav,dataw,dz,dy,dx):
    nt,nz,ny,nx = shape(datau)
    lamb2 = np.zeros((nt,nz,ny,nx),dtype=np.float32)
    for i in range(nt):
        percentage(i,nt)
        lamb2[i,:,:,:] = lambda2single(datau,datav,dataw,dz,dy,dx,i)
    print('{}\r'.format("Lambda2 Vortex Identification Completed "), end="")
    return lamb2

def cart2pol(datau,datav,dataw,dz,dy,dx):
    nt,nz,ny,nx = shape(datau)
    
    #creating x y z 
    x = np.linspace(start = -((nx-1)/2)*dx, stop = ((nx-1)/2)*dx, num = nx)
    y = np.linspace(start = -((ny-1)/2)*dy, stop = ((ny-1)/2)*dy, num = ny)
    z = np.linspace(start = 0, stop = (nz-1)*dz, num = nz)
    
    r = np.sqrt(x*x+y*y)
    np.seterr(divide='ignore', invalid = 'ignore')
    theta = np.arctan(y/x)
    theta = np.nan_to_num(theta)
    
    theta = np.zeros((nz,ny,nx), dtype = np.float32)
    r = np.zeros((nz,ny,nx), dtype = np.float32)
    zpol = np.zeros((nz,ny,nx), dtype = np.float32)
    np.seterr(divide='ignore', invalid = 'ignore')
    for i in range (nx):
        for j in range (ny):
            for k in range (nz):
                r[k,j,i] = np.sqrt(x[i]*x[i]+y[j]*y[j])
                zpol[k,j,i] = z[k]
                theta[k,j,i] = np.arctan(y[j]/x[i])
    theta = np.nan_to_num(theta)
    Ur = np.zeros((nt,nz,ny,nx), dtype = np.float32)
    Utheta = np.zeros((nt,nz,ny,nx), dtype = np.float32)
    
    for t in range(nt):
        u = datau[t,:,:,:]
        v = datav[t,:,:,:]
        Ur[t,:,:,:] = u*np.cos(theta)+v*np.sin(theta)
        Utheta[t,:,:,:] = -u*np.sin(theta)+v*np.cos(theta)
        
    return Ur, Utheta, dataw 


def savecsv(data,nametypedata):
    import time
    import csv
    tic = time.perf_counter()
    filename = nametypedata+'.csv'
    nx,ny,nz,nt = data.shape[0],data.shape[1],data.shape[2],data.shape[3]
    data = np.reshape(data, (nx*ny*nz*nt,1), order="F")
    with open(filename, 'w') as csvfile:   
        csvwriter = csv.writer(csvfile)   
        csvwriter.writerows(data)
    toc1 = time.perf_counter()
    print(f"Saved"+filename+"Time: {((toc1 - tic)/60):0.4f} minutes")

def images2video(path,videopath = 'None',speed = 5):
    import os 
    import cv2 
    image_folder = '.' # make sure to use your folder 
    end = len(path)
    j = 0
    for i in range (end):
        if (path[i] == "\\" ):
            j = i +1
    if (j!=0):
        filename = path[j:end]
    else:
        filename = path
    video_name = filename + '.avi'
    os.chdir(path) 
    images = [img for img in os.listdir(image_folder) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
    frame = cv2.imread(os.path.join(image_folder, images[0])) 
    height, width, layers = frame.shape   
    speed = np.int(speed)
    if (videopath != 'None'):
        video_name = videopath +'\\'+video_name
    video = cv2.VideoWriter(video_name, 0, speed, (width, height))  
    for image in images:  
        video.write(cv2.imread(os.path.join(image_folder, image)))  
    cv2.destroyAllWindows()  
    video.release()  
      

def loadcsv(filename,nz,ny,nx):
    import pandas as pd #reading data from csv
    sk = 0
    df = pd.read_csv(filename,skiprows = sk,nrows = 2, header = None)
    check = df[0][0]
    try:
        check = check+1
    except:
        sk = 1
    df = pd.read_csv(filename,skiprows = sk, dtype =np.float32, header = None)
    data = df.to_numpy()
    del df
    datasize = np.shape(data)[0]
    nt = int(datasize /nx/ny/nz)
    data = np.reshape(data,(nt,nz,ny,nx),order="F")
    return data

def loadmat(filename):
    from scipy import io
    import numpy as np
    import mat73
    try:
        data = io.loadmat(filename)
        key = sorted(data.keys(),reverse=True)[0]
        data = data[key]
        data = np.array(data)
    except:
        data = mat73.loadmat(filename)
        key = sorted(data.keys(),reverse=True)[0]
        data = data[key]
        data = np.array(data)
    return data

def savemat(data,filename):
    from scipy import io
    try:
        io.savemat(filename+".mat", {"data": data})
    except:
        data = np.array(data,dtype=np.float32)
        io.savemat(filename+".mat", {"data": data})

def csv2mat(filename,nz,ny,nx):
    data = loadcsv(filename,nz,ny,nx)
    savemat(data,filename)

def helicity(datau,datav,dataw,dz,dy,dx):
    if (sameshape3(datau,datav,dataw) is False):
        return
    np.seterr(divide='ignore', invalid='ignore')
    nt, nz, ny, nx = shape(datau)
    H_n = np.zeros((nt,nz,ny,nx), dtype = np.float32)
    H=H_n
    for t in range (nt):
        percentage(t,nt)
        dudy,dudz,dudx= np.gradient(datau[t,:,:,:],dz,dy,dx)
        dvdy,dvdz,dvdx = np.gradient(datav[t,:,:,:],dz,dy,dx)
        dwdy,dwdz,dwdx = np.gradient(dataw[t,:,:,:],dz,dy,dx)
        u = datau[t,:,:,:]
        v = datav[t,:,:,:]
        w = dataw[t,:,:,:]
        Vorticity_x = dwdy - dvdz
        Vorticity_y= dudz - dwdx
        Vorticity_z= dvdx - dudy
        H_n[t,:,:,:]=(w*Vorticity_z+v*Vorticity_y+u*Vorticity_x)/(np.sqrt(w**2+v**2+u**2)*np.sqrt(Vorticity_z**2+Vorticity_y**2+Vorticity_x**2));
    print('Helicity Vortex Identification Completed')
    return H_n

def filmax(data):
    for i in range(0,np.size(data)):
        if data[i] == np.max(data):
            data = data[:i]
            return data
        
def plumeheight(data,threshold,dt,dz):
    nt,nz,ny,nx = np.shape(data)
    data = data/np.max(data)
    data[data<threshold] = 0
    data = np.sum(data,2)
    data = np.sum(data,2)
    plheight = np.zeros(nt)
    for i in range(nt):
        for j in range (nz):
            if data[i,j] > 1:
                plheight[i]=j*dz;
    plheight = filmax(plheight)
    plheight = np.array(plheight)
    from scipy.signal import savgol_filter
    plheight = savgol_filter(plheight, 15, 3)
    return plheight

def frontvelocity(data,threshold,dt,dz):
    from scipy.signal import savgol_filter
    height = plumeheight(data,threshold,dt,dz)
    height = np.gradient(height)/dt
    # height = savgol_filter(height, 15, 3)
    return height

def frontvelocityplot(data,dataname,dt,marksize=250):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,5))
    color = 'k'
    nt = np.shape(data)[0]
    x = list(range(0,(nt)*dt,dt))
    plt.plot(x[0:np.shape(data)[0]],data,color = color)
    plt.locator_params(axis='x', nbins=300)
    plt.grid()
    plt.xticks(np.arange(min(x), max(x)+1, marksize))
    plt.ylabel('Wf/D');plt.xlabel('Time')
    plt.savefig(dataname +' Front Velocity.png')

def frontplot(data,dataname,dt,marksize=500):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,5))
    color = 'k'
    nt = np.shape(data)[0]
    x = list(range(0,(nt)*dt,dt))
    plt.plot(x[0:np.shape(data)[0]],data,color = color)
    plt.locator_params(axis='x', nbins=500)
    plt.grid()
    plt.xticks(np.arange(min(x), max(x)+1, marksize))
    plt.ylabel('Wf/D');plt.xlabel('Time (s)')
    plt.savefig(dataname +' Front.png')

def gprimeT(data,Ta,g):
    data = data*g/Ta
    return data

def gprimeRho(Q,density_gas,density_air,g):
    gp = g*(density_air - density_gas)/density_air;
    Q = -Q*gp
    return Q


def wcentermax(data,dz,D):
    nt,nz,ny,nx = np.shape(data)
    data = np.mean(data,0)
    x = int((nx-1)/2)
    y = int((ny-1)/2)
    maxc = max(data[:,y,x])
    for i in range(nz):
        if (maxc==data[i,y,x]):
            cl = i+1
    cl = cl
    return maxc,cl

def reynoldswc(plumeradius_timeaverage,W,threshold,dx,dz,D,nu):
    wc, cl = wcentermax(W,dz,D)
    r = plumeradius_timeaverage
    l = r[cl]
    re = wc*l*D/nu
    return re

def gT0(data):
    print(np.shape(data))
    nt,nz,ny,nx = np.shape(data)
    data = np.mean(data,0)
    x = int((nx-1)/2)
    y = int((ny-1)/2)
    gT =data[1,y,x]
    return gT

def wb(data,D):
    nt,nz,ny,nx = np.shape(data)
    data = np.mean(data,0)
    x = int((nx-1)/2)
    y = int((ny-1)/2)
    wb = np.sqrt(data[1,y,x]*D)
    return wb

def froudewc(gT,W,dz,D):
    wc, cl = wcentermax(W,dz,D)
    wbouyance = wb(gT,D)
    fr = wc/wbouyance
    return fr

def namelist2dict(path):
    import pandas as pd
    df = pd.read_csv(path, delimiter = "\t")
    namelist = np.squeeze(np.array(df))
    namelist_shape = np.shape(namelist)
    namelist_name = [];namelist_value = []
    for i in range (int(namelist_shape[0])):
        length = len(namelist[i])
        temp = namelist[i]
        for j in range(length):
            if temp[j]=='=':
                a=j+1
            if temp[j]==',':
                b=j
                if temp[j-1]=='.':
                    b = j-1
                break
        name = str(namelist[i][:a-1])
        name = name.replace(' ','')
        namelist_name.append(name)
        try:
            namelist_value.append(float(namelist[i][a:b]))
        except:
            string = str(namelist[i][a:b])
            string = string.replace(' ','')
            string = string.replace('.','')
            namelist_value.append(string)
    dic = dict(zip(namelist_name,namelist_value))
    return dic

def reshape_ntnznynx(path):
    data = np.load(path)
    nx,ny,nz,nt = np.shape(data)
    nD = np.zeros([nt,nz,ny,nx])
    for t in range(nt):
        for i in range(nx):
            nD[t,:,:,i] = data[i,:,:,t].T
    np.save(path,nD)

# def hf_csv2array (data):
#     temp = np.array(data)
#     nt = np.shape(temp)[0]
#     a_string = temp[1,0]
#     a_list = a_string.split()
#     map_object = map(float, a_list)
#     list_of_integers = list(map_object)
#     testnz = np.array(list_of_integers)
    
#     nz = int(np.shape(testnz)[0])
#     newarray = np.zeros((nt,nz))
    
#     for i in range (nt):
#         a_string = temp[i,0]
#         a_list = a_string.split()
#         map_object = map(float, a_list)
#         list_of_integers = list(map_object)
#         newarray[i,:] = np.array(list_of_integers)
#     return newarray

# def hf_loadcsv(filename):
#     temp = pd.read_csv(filename,skiprows=1,header=None)
#     temp= hf_csv2array(temp)
#     temp = temp.T
#     return temp

# def hf_loadcsvfulldata(folder,dataname,nx):
#     temp= hf_loadcsv(folder+'\\c0001.d01.'+dataname)
#     nz,nt = np.shape(temp)
#     hfdata = np.zeros((nx,nz,nt))
#     hfdata[int((nx-1)/2),:,:] = temp
#     for i in range(1,int((nx+1)/2)):
#         hfdata[int((nx-1)/2)+i,:,:] = hf_loadcsv(folder+'\\i00'+str(i).zfill(2)+".d01."+dataname)
#     for i in range(1,int((nx+1)/2)):
#         hfdata[int((nx-1)/2)-i,:,:] = hf_loadcsv(folder+'\\j00'+str(i).zfill(2)+".d01."+dataname)
#     return hfdata

# def hf_csv2mat(folder,datatype,nx):
#     data = hf_fulldata(folder,datatype,nx)
#     filename = folder+"\\"+datatype
#     savemat(data[0:int(nx/2+1)],filename+'_1')
#     savemat(data[int(nx/2+1):nx],filename+'_2')
    
# def hf_loadmat(file):
#     d1 = loadmat(file+"_1")
#     d2 = loadmat(file+"_2")
#     data = np.concatenate((d1,d2),axis=3)
#     return data

# def fluctuation(data):
#     nx,nz,nt = np.shape(data)
#     dmean = np.mean(data,2)
#     dprime = np.zeros(np.shape(data))
#     for t in range(nt):
#         dprime[:,:,t] = data[:,:,t]-dmean
#     return dprime

# def hf_contour(data,interface,dx,dz,D,threshold,title):
#     import numpy as np
#     import matplotlib.pyplot as plt
#     data = data.T
#     interface = interface.T
#     nz,nx = np.shape(data)
#     plt.style.use('seaborn-white')
#     xi = np.linspace(-nx*.5*dx/D, nx*.5*dx/D, nx)
#     zi = np.linspace(0, nz*dz/D, nz)
#     plt.figure(figsize=(10, 10))
#     contours  = plt.contour(xi,zi,interface, colors='black');
# #     plt.clabel(contours, inline=True, fontsize=15)
#     plt.ylabel("$z/D$",fontsize=14)
#     plt.xlabel("$x/D$", rotation=0, fontsize=14, labelpad=10)
# #     plt.title(title,fontsize=18,pad = 20)
#     plt.imshow(data, extent=[-nx*.5*dx/D, nx*.5*dx/D,0, nz*dz/D], origin='lower',cmap='jet',alpha=1,aspect='auto')
#     plt.colorbar()
#     plt.savefig(title+".png")

# def plot_plume_spacial_data(data,x1,x2,n,title,axis,dx,dy,dz,D):
#     import matplotlib.pyplot as plt
#     data = np.mean(data,3) #Time average the data [45,45,700,541] to [45,45,700]
#     color = 'k'
#     nx,ny,nz = np.shape(data)
#     def d2x(x1,nx,D):
#         if (x1<0):
#             x1=x1*-1
#             x1 = int(nx/2)-int(x1*D/dx)
#         if (x1==0):
#             x1 = int((nx-1)/2)
#         else:
#             x1 = int(x1*2*D/dx)-1
#         return x1
    
#     if n == 0:
#         plt.figure(figsize=(10,5))
#         xaxis = "x/D"
#         yaxis = axis
#         x1 = d2x(x1,ny,D)
#         if x2 != 0:
#             x2 = int(x2*D/dz)-1
#         try:
#             data = data[:,x1,x2] # Take a slide of data at y=x1 and z=x2
#         except:
#             print("Out of range")
#             print("x/D range: ",float(-(nx)*dx/2/D)," to ",float((nx)*dx/2/D))
#             print("z/D range: ",0," to ",float((nz)*dz/D))
#         x = np.linspace(float(-(nx)*dx/2/D),float((nx)*dx/2/D),int(nx))
#         plt.plot(x[0:np.shape(data)[0]],data,linewidth=1,color=color,
#         marker = 'o',ms =5  ,mfc = color,
#         label=title,markevery = 1)
        
#     if n == 1:
#         plt.figure(figsize=(10,5))
#         xaxis = "y/D"
#         yaxis = axis
#         x1 = d2x(x1,nx,D)
#         if x2 != 0:
#             x2 = int(x2*D/dz)-1
#         try:
#             data = data[x1,:,x2] # Take a slide of data at x=x1 and z=x2
#         except:
#             print("Out of range")
#             print("y/D range: ",float(-(ny)*dy/2/D)," to ",float((ny)*dy/2/D))
#             print("z/D range: ",0," to ",float((nz)*dz/D))
#         x = np.linspace(float(-(ny)*dy/2/D),float((ny)*dy/2/D),int(ny))
#         plt.plot(x[0:np.shape(data)[0]],data,linewidth=1,color=color,
#         marker = 'o',ms =5  ,mfc = color,
#         label=title,markevery = 1)
    
#     if n == 2:
#         yaxis = "z/D"
#         xaxis = axis
#         plt.figure(figsize=(5,10))
#         x1 = d2x(x1,nx,D)
#         x2 = d2x(x2,ny,D)
#         print(x1,x2)
#         data = data[x1,x2,5:] #Take a slide of data at x=x1, y=x2 and z is range from 5 to 700 
#         x = np.linspace(0,float((nz)*dz/D),int(nz))
#         plt.plot(data,x[0:np.shape(data)[0]],linewidth=1,color=color,
#         marker = 'o',ms =1.5,mfc = color,
#         label=title,markevery = 1)
#     try:
#         plt.ylabel("$"+yaxis+"$",fontsize=14)
#         plt.xlabel("$"+xaxis+"$", rotation=0, fontsize=14, labelpad=20)
# #         plt.title(title,fontsize=18,pad = 20)
#     except:
#         print("n=0 : xz plane ")
#         print("n=1 : yz plane ")
#         print("n=2 : xy plane ")
#     plt.savefig(title+".png")

# def hf_plume_interface(data,threshold):
#     data = data/np.max(data)
#     data = np.mean(data,2)
#     data[data<threshold] = 0
#     data[data>threshold] = 1
#     return data

        
class plume_metadata:
    def __init__(self,namelist_path):
        namelist_dictionary = namelist2dict(namelist_path)
        self.nx_original = int(namelist_dictionary["nx_original"])
        self.ny_original = int(namelist_dictionary["ny_original"])
        self.nz_original = int(namelist_dictionary["nz_original"])
        self.nt_original = int(namelist_dictionary["nt_original"])
        self.nx_trimmed = int(namelist_dictionary["nx_trimmed"])
        self.ny_trimmed = int(namelist_dictionary["ny_trimmed"])
        self.nz_trimmed = int(namelist_dictionary["nz_trimmed"])
        self.nt_trimmed = int(namelist_dictionary["nt_trimmed"])
        self.dx = namelist_dictionary["dx"]
        self.dy = namelist_dictionary["dy"]
        self.dz = namelist_dictionary["dz"]
        self.dt = namelist_dictionary["dt"]
        self.Ho =  namelist_dictionary["tke_heat_flux_hot"]
        self.gas_constant = namelist_dictionary["plume_gas_constant"]
        self.plume_gas = namelist_dictionary["plume_gas"]
        self.D = namelist_dictionary["source_dia"]
        self.g = namelist_dictionary["gravity"]
        self.threshold = namelist_dictionary["plume_threshold"]
        self.Ta = namelist_dictionary["ambient_temperature"]
        self.nu = namelist_dictionary["dynamic_viscosity"]
        self.density_ref = namelist_dictionary["density_reference"]
        self.density_amb = namelist_dictionary["density_ambient"]

class plume_metrics:
    def __init__(self,gT,W,dt,dz,dy,dx,D,threshold,Ta,g,density_ref,density_amb):
        self.front_height = plumeheight(gT,threshold,dt,dz);
        self.front_velocity = frontvelocity(gT,threshold,dt,dz);
    
class plume_polar_coordinates:
    def __init__(self,dataU,dataV,dataW,dz,dy,dx):
        self.Ur, self.Utheta, self.W = cart2pol(dataU,dataV,dataW,dz,dy,dx)

class plume_centerline_metrics:
    def __init__(self,gT,W,dt,dz,dy,dx,D,threshold,nu): #v=0.00004765
        nt,nz,ny,nx = np.shape(gT)
        self.gprimeT0 = gT0(gT)
        self.wcmax,self.wcmax_location = wcentermax(W,dz,D)
        self.z_wmax = self.wcmax_location*dz/D
        self.lwcm = self.rtimeaverage[self.wcmax_location]
        self.Reynolds_max_centerline = reynoldswc(self.rtimeaverage,W,threshold,dx,dz,D,nu)
        self.Froude_max_centerline = froudewc(gT,W,dz,D)
        
# class high_frequency_profile:
#     def __init__(self,T,U,V,W,dx,dz,D,Ta,g,threshold):
#         nx,nz,nt = np.shape(T)
#         T = T - Ta
#         T = gprimeT(T,Ta,g)
#         self.interface = hf_plume_interface(T,threshold)
#         shear = (np.gradient(np.mean(W,2),dx,dz))[0]
#         dTdz = (np.gradient(np.mean(T,2),dx,dz))[0]
#         U = fluctuation(U)
#         V = fluctuation(V)
#         W = fluctuation(W)
#         T = fluctuation(T)
#         nx,nz,nt = np.shape(T)
#         self.Re_stress_UW = np.mean(U*W,2)
#         self.Re_stress_VW = np.mean(V*W,2)
#         self.U_rms = np.mean(U*U,2)
#         self.V_rms = np.mean(V*V,2)
#         self.W_rms = np.mean(W*W,2)
#         self.TKE_shear_pro_UW = -(self.Re_stress_UW*shear)
#         self.TKE_shear_pro_VW = -(self.Re_stress_VW*shear)
#         self.TKE_buoyant_production_I = np.mean(W*T,2)
#         self.TKE_buoyant_production_II = self.TKE_buoyant_production_I*dTdz
#         self.TKE = self.U_rms+self.V_rms+self.W_rms
#         centerline = int((nx-1)/2)
#         self.U_rms_centerline = self.U_rms[centerline,:]
#         self.V_rms_centerline = self.V_rms[centerline,:]
#         self.W_rms_centerline = self.W_rms[centerline,:]
#         self.TKE_centerline = self.TKE[centerline,:]
#         self.TKE_buoyant_production_I_centerline = self.TKE_buoyant_production_I[centerline,:]
#         self.TKE_buoyant_production_II_centerline = self.TKE_buoyant_production_II[centerline,:]
#         self.TKE_shear_pro_UW_centerline = self.TKE_shear_pro_UW[centerline,:]
#         self.TKE_shear_pro_VW_centerline = self.TKE_shear_pro_VW[centerline,:]
        
        
#         mark = 20
#         plt.figure(figsize=(10, 7))
#         zi = np.linspace(0, nz*dz/D, nz)
#         plotdata = self.U_rms_centerline/self.U_rms_centerline.max()
#         plt.plot(zi,plotdata,'bo--', label='U_rms_centerline', markevery = mark, linewidth=3)
#         plotdata = self.V_rms_centerline/self.V_rms_centerline.max()
#         plt.plot(zi,plotdata,'gs--', label='V_rms_centerline',markevery = mark, linewidth=3)
#         plotdata = self.W_rms_centerline/self.W_rms_centerline.max()
#         plt.plot(zi,plotdata,'rv--', label='W_rms_centerline',markevery = mark, linewidth=3)
#         plotdata = self.TKE_centerline/self.TKE_centerline.max()
#         plt.plot(zi,plotdata,'c8--', label='TKE_centerline',markevery = mark, linewidth=3)
#         plotdata = self.TKE_buoyant_production_I_centerline/self.TKE_buoyant_production_I_centerline.max()
#         plt.plot(zi,plotdata,'mx--', label='TKE_buoyant_production_I_centerline',markevery = mark, linewidth=3)
#         plotdata = self.TKE_buoyant_production_II_centerline/self.TKE_buoyant_production_II_centerline.max()
#         plt.plot(zi,plotdata,'yp--', label='TKE_buoyant_production_II_centerline', markevery = mark,linewidth=3)
#         plotdata = self.TKE_shear_pro_UW_centerline/self.TKE_shear_pro_UW_centerline.max()
#         plt.plot(zi,plotdata,'kD--', label='TKE_shear_pro_UW_centerline', markevery = mark,linewidth=3)
#         plotdata = self.TKE_shear_pro_VW_centerline/self.TKE_shear_pro_VW_centerline.max()
#         plt.plot(zi,plotdata,'o|--', label='TKE_shear_pro_VW_centerline', markevery = mark,linewidth=3)
#         plt.legend()
#         plt.xlabel("$z/D$")
#         current_directory = os.getcwd()
#         final_directory = os.path.join(current_directory, r'Plots')
#         if not os.path.exists(final_directory):
#            os.makedirs(final_directory) 
#         plt.savefig(final_directory+"\\HighFrequency_Centerline_Profile.png")
        


