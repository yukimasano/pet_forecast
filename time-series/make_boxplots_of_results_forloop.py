     # -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 19:14:04 2016

@author: asano
"""
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from scipy import stats as st
import datetime
import sys
from matplotlib import rc


''' WITH CENTRALITY'''
A=np.zeros(shape=(6,1))
for i in range(1,12):
    x= np.load('cen_12clusterNum_%s.npy'%i)
    print x.shape
    A=np.append(A,x, axis=1)   
#%%
B=np.zeros(shape=(6,1))
for i in range(1,12):
    x= np.load('no_cen_12clusterNum_%s.npy'%i)
    print x.shape
    B=np.append(B,x, axis=1)    
#%%    
    
x3 = np.load('np_10_%s.npy'%3)

for i in [0,3]:
    print i ,"new "
    print np.median(x1[i,:]), np.median(x1p[i,:])
    print x1[i,:].mean(), x1p[i,:].mean()
    
    print
    print np.median(x2[i,:]), np.median(x2p[i,:])
    print x2[i,:].mean(), x2p[i,:].mean()
    print 
    print np.median(x3[i,:]), np.median(x3p[i,:])
    print x3[i,:].mean(), x3p[i,:].mean()
#%%
def mb(x,k):
    bp = ax.boxplot(x,positions=[k], widths=0.85)
    plt.setp(bp['boxes'], color='black',lw=2)
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], marker='x')
    plt.setp(bp['medians'], color='red',lw=2)
   # plt.plot(k,np.mean(x),'kx')
    
my_xticks = ['C0','C0 (wp)','C1','C1 (wp)','C3','C3 (wp)']


#%%
fig=plt.figure(figsize=(10, 4.5))
ax = plt.subplot(1,2,1)
plt.rc('font', family='serif')
plt.rcParams.update({'font.size': 14})

mb(x1[0,:]/24.,0)
mb(x1p[0,:]/24.,1)

mb(x3[0,:]/24.,3)
mb(x3p[0,:]/24.,4)

mb(x2[0,:]/24.,6)
mb(x2p[0,:]/24.,7)
plt.xlim([-0.5,7.5])
plt.xlabel('Cluster')
plt.ylabel('Within 90% CI')
plt.title('24 1-hour forecasts')
plt.xticks([0,1,3,4,6,7], my_xticks)
ax = plt.subplot(1,2,2)
plt.rc('font', family='serif')
plt.rcParams.update({'font.size': 12})

mb(x1[3,:]/24.,0)
mb(x1p[3,:]/24.,1)

mb(x3[3,:]/24.,3)
mb(x3p[3,:]/24.,4)

mb(x2[3,:]/24.,6)
mb(x2p[3,:]/24.,7)
plt.xlim([-0.5,7.5])
plt.xticks([0,1,3,4,6,7], my_xticks)
plt.ylabel('Within 90% CI')
plt.title('Final 24-hour forecast')
plt.xlabel('Cluster')
fig.tight_layout()
fig.savefig('results_CI',dpi=500)
plt.show()
#%%
if False:
    fig=plt.figure(figsize=(7, 4.5))
    for i in range(6):
        ax = plt.subplot(2,3,i)
        plt.rc('font', family='serif')
        plt.rcParams.update({'font.size': 12})
    
        ax.hist(p1[:,i],histtype='step',bins= 20,log=True)
        ax.hist(p2[:,i],histtype='step',bins= 20,log=True)
        ax.hist(p3[:,i],histtype='step',bins= 20,log=True)
        plt.title(r'$\lambda_%i$'%i)
        ax.set_xscale('log')
        fig.tight_layout()
            