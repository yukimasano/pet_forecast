# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 21:28:06 2016

@author: YPC
"""
import numpy as np
from email.utils import parsedate_tz, mktime_tz
import datetime

import sys
def make_pr():
    import networkx as nx
    uu=np.load('../network/mentions.npy')
    G_dir = nx.from_edgelist(uu,create_using=nx.DiGraph())
    G = nx.from_edgelist(uu)
    G_dir.remove_edges_from(G_dir.selfloop_edges())
    G.remove_edges_from(G.selfloop_edges())
    c_pr=nx.pagerank_scipy(G_dir,tol=1e-09)
    return c_pr
    
def make_df(c_pr):
    import pandas as pd
    df = pd.read_csv('../twitter/output_tweets.csv',sep='\t')#,dtype=np.str)  
    t_uid = df.user_id.values
    t_time = df.created_at.values.astype('S60')
    t_tid = df.tweet_id.values
    t_cen=np.zeros(shape=(len(t_uid)))
    t_fol= df.user_followers_count.values()
    for i in range(len(t_uid)):
        try:
            t_cen[i] = c_pr['%s'%t_uid[i]]  # save centralities per tweet
        except:
            t_cen[i]=0
    
    df2 = pd.read_csv('../twitter/output_petitions.csv',sep='\t')#,dtype=np.str)   
    p_pid= np.int32(df2.pet_id.values)
    p_tid= df2.tweet_id.values
    
    
    return  t_time, t_tid, t_cen, p_pid, p_tid,t_fol  # t_uid,
    
def get_t0(pet_in):
    import json
    pet_in = np.int64(pet_in)
    f = open('../petitions.json', 'r')
    met = json.load(f)
    f.close()
    time_list=[]
    pet_list= []
    for i in range(len(met)):
        num= (pet_in==int(met[i]['petition']['id']))
        if any(num):
            pet_list.append(met[i]['petition']['id'])
            t = met[i]['petition']['created_datetime']
            dt = t.encode()[0:10]
            tim = t.encode()[11:-1]
            t0 = datetime.datetime(int(dt[0:4]),int(dt[5:7]),int(dt[8:10]),
                                   int(tim[0:2]),int(tim[3:5]),int(tim[6:8]))
            t0 -= datetime.timedelta(hours=1)
            time_list.append(t0)
            # e.g. '2011-07-28T23:57:50Z'
      # UK GMT, twitter: UTC
    return np.array(time_list), np.array(pet_list)
def get_cen_for_pet(pet_in, t_time, t_tid, t_cen, p_pid, p_tid,t0,p_times):
    C = np.zeros(shape=(len(p_pid),len(pet_in))) # or len(p_pid)
    print len(pet_in)
    T = np.zeros(shape=(len(p_pid),len(pet_in)))
    missing=0
    counter= np.zeros(shape=( len(pet_in)))
    pet_in = np.int64(pet_in)
    l= datetime.datetime.now()
    for i in range(len(p_pid)):
        num = (pet_in==int(p_pid[i]))
        if any(num):
            try:
                indx= np.argwhere(num)[0][0]
                ind = np.argwhere(t_tid == p_tid[i])[0][0]
                #ti = datetime.datetime.fromtimestamp(mktime_tz(parsedate_tz(t_time[i])))   
                ti = t_time[ind].replace(" +0000 "," ")
                ti = datetime.datetime.strptime(ti,"%a %b %d %H:%M:%S %Y")
                t0_of_pat = t0[np.argwhere(p_times==int(p_pid[i]))[0][0]]
                ti= (ti - t0_of_pat).total_seconds()/60.                
                C[counter[indx],indx]= t_cen[ind] 
                T[counter[indx],indx]= ti
                counter[indx]+=1
            except:
               # print sys.exc_info()
                missing+=1
                #print 'Could not find tweet %s'%p_tid[i]
                continue
    cut= np.max(np.sum(T!=0, axis=0))
    print 'going through tweets took %s s'% (datetime.datetime.now()-l).total_seconds()
    #T = np.array([(x-t0).total_seconds()/60. for x in T])
  #  indx = np.argsort(T)
   # C = C[indx]
    #T = T[indx]
    if cut==0:
        print 'no centralities for all pets found'
        cut=1
    return C[:cut,:],T[:cut,:], missing