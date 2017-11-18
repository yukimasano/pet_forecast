# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 21:28:06 2016

@author: YPC
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import csv
import sys
if True:
    uu=np.load('mentions.npy')
    G_dir = nx.from_edgelist(uu,create_using=nx.DiGraph())
    G = nx.from_edgelist(uu)
    G_dir.remove_edges_from(G_dir.selfloop_edges())
    G.remove_edges_from(G.selfloop_edges())
    
    #uids=G_dir.nodes()
    c_pr=nx.pagerank_scipy(G_dir)
#%%
import pandas as pd
from email.utils import parsedate_tz, mktime_tz
if True:
    df = pd.read_csv('../twitter/output_tweets.csv',sep='\t')#,dtype=np.str)  
       ##### df = df.sort_values('created_at')
    t_uid = df.user_id
    t_time= df.created_at
    t_tid = df.tweet_id
    t_cen=np.zeros(shape=(len(t_uid)))
    
    for i in range(len(t_uid)):
        t_cen[i] = c_pr.get('%s'%t_uid[i])
    
    df2 = pd.read_csv('../twitter/output_petitions.csv',sep='\t')#,dtype=np.str)   
    p_pid= df2.pet_id
    p_tid= df2.tweet_id
#%%
    
    """
    tu=np.unique(t_tid)
    pu=np.unique(p_tid)
    len(tu) # 996048
    len(pu) # 1014276
    len(t_tid) # 1007928
    len(p_tid) # 1029688
    --> also tweet file contains less tweets than patent file. 
    """

import datetime
"""add petition_starting time"""
def get_cen_for_pet(pet,p_pid,p_tid, t_cen): 
    C = []
    T = []
    missing=0
    initial = True
    for i in range(len(p_pid)):
        if p_pid[i] == pet:
            if initial == True:
                timestamp = mktime_tz(parsedate_tz(t_time[i]))
                t0 = datetime.datetime.fromtimestamp(timestamp)
                initial=False
            try:
                ti = datetime.datetime.fromtimestamp(mktime_tz(parsedate_tz(t_time[i])))
                     
                ind = np.argwhere(t_tid == p_tid[i])[0][0]
                C.append(t_cen[ind])
                T.append(ti)
            except IndexError:
                missing+=1
                #print 'Could not find tweet %s'%p_tid[i]
                continue
    try:
        tmin = min(T)
        T=[(x-tmin).total_seconds()/60 for x in T]
        #t = (ti-tmin).total_seconds()/60         
        T=np.array(T)
       # T= T-tmin
        C=np.array(C)
        indx= np.argsort(T)
        C=C[indx]
        T=T[indx]
        return C,T, missing
    except:
        return 'no','no'    
if True:      
    pet=int(49528)
    c_vec, t_vec,mis = get_cen_for_pet(pet,p_pid,p_tid, t_cen)     #or try int(38257)
    print mis
    sigs= np.load('../time-series/sig49528.npy')
    sigs=sigs/10000000.
    fig=plt.figure(figsize=(7, 4.5))
    plt.rcParams.update({'font.size': 14})
    plt.rc('font', family='serif')
    plt.loglog(sigs, 'x',markersize=2) 
    plt.loglog(t_vec, c_vec, '.',markersize=2)   
    plt.xlabel('Time of tweet (s)')   # sollte time since petition start
    #plt.ylabel('PageRank of tweet author')
    plt.legend(['Signatures*e-7','PageRank of tweet author'])
    plt.title('Centrality time-series for petition %s'%pet)
#    fig.savefig('centrality_tweets_%s'%pet, dpi=500)

#%%

import winsound
# Play Windows exit sound.
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)