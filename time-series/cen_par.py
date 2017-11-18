# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:17:21 2016

@author: YPC
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 11:40:03 2016

@author: YPC
"""
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from scipy import stats as st
import final_cens, get_sigs, cluster_making 
import datetime
import sys
from matplotlib import rc
from joblib import Parallel



def p_model(lam, c, sigma,t_in,s_in):
    s_s = s_star(lam,c, t_in)
    #temp = 
    p = np.exp(- (np.log(s_in/s_s) **2) / (2*sigma**2))/(s_in*sigma*np.sqrt(2*np.pi))
    return p
    
def s_star(lam,c,t_in):
    l1,l2,l3,l4= lam
    s_s = (l3*t_in**l1 )/(l2+t_in**l1 ) +l4*c
    return s_s

def LL(x, *args):
    r = 0
    l1, l2, l3,l4,sigma = x
    t, obs, cens = args
    t=0
    for o in obs: # number of obs is K
        c = cens[t]
        t += 1
        r += np.log(p_model([ l1, l2, l3,l4],c,sigma,t,o)) 
    return -r 
    
def do_st(i):
    print 'cluster %s'%i
    pets = clusters[0,clusters[1,:]==i]
    print 'contains ' , len(pets)
    para_list = np.array([])
    
   # x0_list= np.load('para_%sc.npy'%i)     # list of priors
  #  x0_prior = x0_list.mean(axis=0)
    
    # save whether within 90% CI (Good) or not (Bad) and same for Prediction
    g=[]
    b=[]
    g_p=[]
    b_p=[]
    pet_list=[]
    final_list=[]
    
    
    times, p_times = final_cens.get_t0(pets)  # very 
    start_tweet_col = datetime.datetime(2013, 07, 01) 
    good_pets = [x<start_tweet_col for x in times]
    pets = np.array(np.ma.compressed(np.ma.masked_where(good_pets, pets)))
    times = np.array(np.ma.compressed(np.ma.masked_where(good_pets,times)))
    p_times = np.array(np.ma.compressed(np.ma.masked_where(good_pets,p_times)))

    c_vecs, t_vecs,_ = final_cens.get_cen_for_pet(pets, t_time,t_tid, t_cen, p_pid, p_tid,times,p_times)
    print 'done with getting all the c_vecs and t_vecs for cluster %s'%i

    for pet in pets:
        c_vec=c_vecs[:, np.argwhere(pets==pet)[0][0]]
        t_vec=t_vecs[:, np.argwhere(pets==pet)[0][0]]/60
        """ get the growth of signatures """
        # fast for low value of N
        start_skip=0
        predictforward=24
        ff=24
        N = predictforward + ff + start_skip
        try:
            obsv = get_sigs.get_growth_tsv(pet,N)  
            obsv[obsv==0] = 1
            if obsv[-1]==1:
                continue
        except:
            print 'could not find tsv for pet ' ,pet
            continue
        while len(obsv)<=N+1:
            obsv.append(obsv[-1])
        times=range(1, len(obsv))
        cen_f=[] 
        good=0
        bad =0
        
        good_p = 0
        bad_p = 0
        
        for j in range(start_skip):
            cen_f.append( np.sum( (np.exp( (t_vec[t_vec<j]-j) *0.4 )* 1e3 * c_vec[t_vec<j])))
        for t in times[start_skip:ff]:
            c = np.sum( (np.exp( (t_vec[t_vec<t]-t) *0.4 )* 1e3 * c_vec[t_vec<t]))
            cen_f.append(c)
            if c==0:
                l4_lim = 0
            else:
                l4_lim = 1e6
            res= optimize.differential_evolution(LL, popsize=12,strategy='best1bin',
                                                 init='random', polish=False,
                                                 mutation=(0.8, 1.8), 
                                                 args=tuple([t,obsv[:t],cen_f]),
                                                 bounds=((0.1,10),(1e4,1e6),(1e4,1e6),
                                                         (1e-1,l4_lim),(1e-4,1)))   
            s_pred=s_star(res.x[0:4],c, t)
            if obsv[t+1] > s_pred*np.exp(-CI*res.x[4]) and obsv[t+1] < s_pred*np.exp(CI*res.x[4]):
                good+=1
            else:
                bad+=1
            para_list= np.append(para_list, np.array(res.x))
        para_list=para_list.reshape((len(para_list)/5,5))
        if predictforward!=0:
            avg_sig = para_list[-6:-1,:].mean(axis=0)[4]
            avg_lam = para_list[-6:-1,:].mean(axis=0)[0:4]
            # print avg_sig,avg_lam
            for t2 in times[ff:ff+predictforward]:
                s_pred=s_star(avg_lam, c, t2)
                if obsv[t2+1] > s_pred*np.exp(-CI*avg_sig) and obsv[t2+1] < s_pred*np.exp(CI*avg_sig):
                    good_p+=1
                else:
                    bad_p+=1
                    
        pet_list.append(pet)
        final_list.append(obsv[-1])
        g.append(good)
        b.append(bad)
        b_p.append(bad_p)
        g_p.append(good_p)
        print good,bad,good_p,bad_p, obsv[-1]
    np.save('cen_%sclusterNum_%s.npy'%(cluster_num,i), np.array([pet_list,final_list, g,b,g_p,b_p]))
if __name__ =='__main__':
    CI=st.norm.ppf(0.95)
    #%%  This can plot either the final fit (boring) or the next step prediction
    """ general stuff used for every petition """ 
    c_pr=np.load('c_pr.npy')    # centralities (pageranks) of users
    t_time=np.load('t_time.npy') # times of tweets
    t_tid=np.load('t_tid.npy')   # tweet-id of tweets
    t_cen=np.load('t_cen.npy')   # centralities of tweets
    t_fol=np.load('t_fol.npy')   # tweet followers
    p_pid=np.load('p_pid.npy')   # petition id
    p_tid=np.load('p_tid.npy')   # petition tweet-id

    missing_tsv=0
    
    # Start clustering run cluster script
    cluster_num = 12
    max_feature_num=5000
    grams=(1,1)
    reclassify=False
    if reclassify==True:
        cluster_making.make_cluster(cluster_num,max_feature_num,grams)  # 
    clusters = np.load('cluster_info/%s-%s_grams_%sclustering.npy'%(grams[0],grams[1],cluster_num))
    print 'now doing Bayes'
    Parallel(n_jobs=6)(do_st(i) for i in range(1,cluster_num+1))
    
    