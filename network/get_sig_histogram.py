# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 12:54:52 2016

@author: YPC
"""

import matplotlib.pyplot as plt
import json
import numpy

f=open('../petitions.json', 'r')
met=json.load(f)
f.close()
s=[]
s2=[]

""" this plots the signature distribution function"""
if False:
    for i in range(len(met)):
        s.append( met[i]['petition']['signature_count'])
    s=numpy.array(s)
    s=sorted(s, reverse=True)
    fig=plt.figure(figsize=(7, 4.5))
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    plt.loglog(s,'-',color='darkblue',marker='x')
    plt.loglog([1,len(s)],[100000,100000])
    plt.loglog([1,len(s)],[10000,10000])
    plt.title("Signatures distribution")
    plt.xlabel("Rank")
    plt.ylabel("Number of Signatures")
    plt.tight_layout()
    plt.legend(['Signatures','100,000','10,000'],loc=3,fontsize=12)
    fig.savefig('Signatures_dist', dpi=500)

#%%

""" this plots the distr of len(text) """
if True:
    for i in range(len(met)):
        s.append( len(met[i]['petition']['description']))
        if len(met[i]['petition']['description']) ==1000:
            print met[i]['petition']['description']
    fig=plt.figure(figsize=(4.5, 4.5))
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    hist(s, bins=1000)
    plt.title("Histogram of textlengths")
    plt.ylabel("Number of petitions")
    plt.xlabel("Length of text")
    plt.tight_layout()
    #fig.savefig('textlen_dist', dpi=500)
#%%
    """ this plots the distr of len(text) """
if False:
    for i in range(len(met)):
        if met[i]['petition']['signature_count'] >1000:
            s.append( len(met[i]['petition']['description']))
        s2.append( len(met[i]['petition']['description']))
    
    
    plt.rcParams.update({'font.size': 12})
    plt.rc('font', family='serif')
    _,bins, _= hist(s, bins=50)
    fig, ax1 = plt.subplots()
    fig.set_size_inches(7,4.5)
    ax1.hist(s2,bins=bins,color='k',histtype='step')
    ax1.set_ylabel('Petitions', color='k')
    ax2 = ax1.twinx()
    
    ax2.hist(s,bins=bins,color='b',histtype='step')
    ax2.set_ylabel('Petitions with \n >1,000 signatures',color='b')
    plt.title("Histogram of textlengths")
    ax1.set_xlabel("Length of text")
    plt.show()
    fig.tight_layout()
    fig.savefig('textlen_s_dist', dpi=500)
    #%%
    
    """ this plots the cum number of len(text)"""
if False:
    k=0
    for i in range(len(met)):
        k=k+1
        t = met[i]['petition']['created_datetime']
        dt = t.encode()[0:10]
        t0 = datetime.datetime(int(dt[0:4]),int(dt[5:7]),int(dt[8:10]))
        s.append(t0)
        s2.append(k) 
    fig, ax = plt.subplots()
    fig.set_size_inches(8,3)
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    ax.plot(s,s2,color='darkblue')
    plt.title("Cumulative number of petitions")
    plt.ylabel("Number of Petitions",fontsize=15)
    ax.set_xlim([734300,735687])
    for label in ax.xaxis.get_ticklabels()[1::2]:
        label.set_visible(False)
    ax.xaxis.get_ticklabels()[0].set_visible(True)
    ax.xaxis.get_ticklabels()[-1].set_visible(True)
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()
    fig.savefig('pets_vs_time', dpi=500)
    #%%
if False:  
    for i in range(len(met)):
        if int(met[i]['petition']['signature_count'])<100000 and int(met[i]['petition']['signature_count'])>5000:
                print met[i]['petition']['id'], met[i]['petition']['signature_count']
            
#347 148373
#885 149470
#1535 113490
#2199 156218
#7337 258276
#8903 118875
#19149 118475
#19658 145544
#22321 102701
#22670 179466
#29349 154662
#29399 110704
#29664 108848
#31778 114499
#33133 117469
#35788 109306
#37180 174578
#38257 304255
#40925 106210
#41492 153828
#43154 104818
#45969 134835
#46455 170931
#48389 106410
#48628 104068
#49528 111572
#52740 110561
#53523 123881
#56810 107261
#58166 103063
#60164 113797
#62385 327877
#62490 123307
#63445 103479
#64331 118956
#64997 112285
#67165 124511
#67911 102170
#71455 118068
#73911 103841
#74830 135408