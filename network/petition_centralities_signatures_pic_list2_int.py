# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 21:28:06 2016

@author: YPC
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
if False:
    uu=np.load('mentions.npy')
    G_dir = nx.from_edgelist(uu,create_using=nx.DiGraph())
    G = nx.from_edgelist(uu)
    G_dir.remove_edges_from(G_dir.selfloop_edges())
    G.remove_edges_from(G.selfloop_edges())
    
    #uids=G_dir.nodes()
    c_pr=nx.pagerank_scipy(G_dir,tol=1e-09)
#%%
import pandas as pd
from email.utils import parsedate_tz, mktime_tz
if False:
    df = pd.read_csv('../twitter/output_tweets.csv',sep='\t')#,dtype=np.str)  
    t_uid = df.user_id.values
    t_time = df.created_at.values
    t_tid = df.tweet_id.values
    t_cen=np.zeros(shape=(len(t_uid)))
    
    for i in range(len(t_uid)):
        try:
            t_cen[i] = c_pr['%s'%t_uid[i]]  #c_pr.get('%s'%t_uid[i])
        except:
            t_cen[i]=0
    
    df2 = pd.read_csv('../twitter/output_petitions.csv',sep='\t')#,dtype=np.str)   
    p_pid= df2.pet_id.values
    p_tid= df2.tweet_id.values
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
def get_cen_for_pet(pet_in,p_pid,p_tid, t_cen,t0_in): 
    C = []
    T = []
    missing=0
    for i in range(len(p_pid)):
        try:
            if int(p_pid[i]) == int(pet_in):
                ti = datetime.datetime.fromtimestamp(mktime_tz(parsedate_tz(t_time[i])))    
                ind = np.argwhere(t_tid == p_tid[i])[0][0]
                C.append(t_cen[ind])
                T.append(ti)
        except IndexError:
            missing+=1
            #print 'Could not find tweet %s'%p_tid[i]
            continue
    try:
       # t0 = min(T)
        T = [(x-t0_in).total_seconds()/60. for x in T] 
        T = np.array(T)
        C = np.array(C)
        indx = np.argsort(T)
        C = C[indx]
        T = T[indx]
        return C,T, missing
    except:
        print 'something wrong'
        return 'no','no'    

def give_opening_time(pet_in):
    import json  
    f = open('../petitions.json', 'r')
    met = json.load(f)
    f.close()
    for i in range(len(met)):
        if str(met[i]['petition']['id'])==str(pet_in):
            t = met[i]['petition']['created_datetime']
            break
    dt = t.encode()[0:10]
    tim = t.encode()[11:-1]
    #tweets are in utc time so substract one here
    dt_tim = datetime.datetime(int(dt[0:4]),int(dt[5:7]),int(dt[8:10]),
                             int(tim[0:2]),int(tim[3:5]),int(tim[6:8]))
    dt_tim -= datetime.timedelta(hours=1)  # UK GMT, twitter: UTC
    return dt_tim
if True:
    pet_list=[]
#    pet_list.append( int(54958))
#    pet_list.append( int(49528))
#    pet_list.append( int(38257))
#    pet_list.append( int(62490))
#    pet_list.append( int(45969)) 
    pet_list.append( int(62385))
#    pet_list.append( int(46455))
#    pet_list.append( int(73911))
#    pet_list.append( int(53523))
for pet in pet_list:
    print pet
    t0 = give_opening_time(pet)
    c_vec, t_vec, mis = get_cen_for_pet(pet,p_pid,p_tid, t_cen,t0)
    print mis
    t_vec2 = t_vec/60.
    sigs = np.load('../time-series/signatures/sig%s.npy'%pet)
    sig_t = range(len(sigs))
    c_vec2 = c_vec*(10**6)
    fig = plt.figure(figsize=(7, 4.5))
    plt.rcParams.update({'font.size': 14})
    plt.rc('font', family='serif')
    plt.semilogy(sig_t, sigs) 
    plt.semilogy(t_vec2, c_vec2, 'x',markersize=5)   
    plt.xlabel('Time since start of petition in h')   # sollte time since petition start
    #plt.ylabel('PageRank of tweet author')
    plt.legend(['Signatures','Scaled PageRank of tweet author'],loc=2,fontsize=9)
    plt.title('Centralities  and signatures for petition %s'%pet)
    plt.xlim([-3000,3000+20])
    fig.savefig('c_sigs3000_%s'%pet, dpi=500)
    plt.close()

#%%
#fig = plt.figure(figsize=(7, 4.5))
#plt.rcParams.update({'font.size': 14})
#plt.rc('font', family='serif')
#plt.xlabel('Time since start of petition in h')   # sollte time since petition start
#plt.ylabel('PageRank of tweet author')
#plt.semilogy(t_vec2,c_vec2, 'gx')
#plt.semilogy(sig_t, sigs) 
#plt.legend(['Signatures','Scaled PageRank of tweet author'],loc=1,fontsize=9)
#plt.title('Centralities  and signatures for petition %s'%pet)
#plt.xlim([0,250])
#fig.savefig('c_sigs250_%s'%pet, dpi=500)


#%%


import winsound
# Play Windows exit sound.
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)