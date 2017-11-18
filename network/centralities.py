# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 21:28:06 2016

@author: YPC
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
uu=np.load('mentions.npy')
G_dir = nx.from_edgelist(uu,create_using=nx.DiGraph())
G = nx.from_edgelist(uu)
G_dir.remove_edges_from(G_dir.selfloop_edges())
G.remove_edges_from(G.selfloop_edges())
#%%
katz_cen_pic=False 
if katz_cen_pic==True:
    c_ka=sorted(nx.katz_centrality(G_dir,max_iter=800, alpha=0.02).values(),reverse=True)
    #c_clo= nx.closeness_centrality(G)
    c_ka=np.array(c_ka)
    y = np.log(c_ka[c_ka!=0][10:10000]) 
    x= np.log(range(10, len(y)+10))
    
    m,b = np.polyfit(x, y, 1)
    y10= np.exp(m*np.log(10) +b)
    y100= np.exp(m*np.log(50000 )+b)
    

    fig=plt.figure(figsize=(7, 4.5))
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    plt.loglog(c_ka,'-',color='darkblue',marker='x')
    plt.loglog([10,50000],[y10,y100] ,'-', marker='.',color='orange',linewidth=3,markersize=10)
    plt.title("Katz centrality")
    plt.ylabel("Katz centrality")
    plt.legend(["Katz centrality","Power-law fit, c=%s"%np.round(m,2)], fontsize=11)
    plt.xlabel("Rank")
    
    c_in=G_dir.in_degree().values()
    c_out= G_dir.out_degree().values()
    fig, (ax1,ax2) = plt.subplots(1,2)
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    fig.set_size_inches(7, 4.5)  
    ax1.loglog(c_in, c_ka, '.', markersize=4, alpha=0.6,color='darkblue')
    ax1.set_xlabel('In-degree')
    ax1.set_ylabel('PageRank')
    ax2.loglog(c_out, c_ka,'.', markersize=4, alpha=0.6,color='darkblue')
    ax2.set_xlabel('Out-degree')
    #fig.savefig('Katz_dist', dpi=500)

#%%
make_pagerank_pic=False
if make_pagerank_pic==True:
    c_pr=sorted(nx.pagerank_scipy(G_dir, alpha=0.85, max_iter=1000).values(),reverse=True)
    #c_clo= nx.closeness_centrality(G)
    c_pr=np.array(c_pr)
    y = np.log(c_pr[c_pr!=0][10:10000]) 
    x= np.log(range(10, len(y)+10))
    
    m,b = np.polyfit(x, y, 1)
    y10= np.exp(m*np.log(10) +b)
    y100= np.exp(m*np.log(50000 )+b)
    
    fig=plt.figure(figsize=(7, 4.5))
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    plt.loglog(c_pr,'-',color='darkblue',marker='x')
    plt.loglog([10,50000],[y10,y100] ,'-', marker='.',color='orange',linewidth=3,markersize=10)
    plt.title("Centrality rank plot of mentions network")
    plt.ylabel("PageRank centrality")
    plt.legend(["PageRank","Power-law fit, c=%s"%np.round(m,2)], fontsize=11)
    plt.xlabel("Rank")
   # fig.savefig('PageRank_dist', dpi=500)
#%%
make_centrality_degree_comparison=True
if make_centrality_degree_comparison:
    c_pr=nx.pagerank_scipy(G_dir,tol=1e-09).values()
    c_in=G_dir.in_degree().values()
    c_deg=G.degree().values()
    c_out= G_dir.out_degree().values()
    fig, (ax1,ax2) = plt.subplots(1,2)
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    fig.set_size_inches(7, 4.5)  
    ax1.loglog(c_in, c_pr, '.', markersize=4, alpha=0.6,color='darkblue')
    ax1.set_xlabel('In-degree')
    ax1.set_ylabel('PageRank')
    ax2.loglog(c_out, c_pr,'.', markersize=4, alpha=0.6,color='darkblue')
    ax2.set_xlabel('Out-degree')
       # ax2.set_ylabel('PageRank')
    fig.suptitle('PageRank centrality vs in- and out-degree', x=0.5, y=0.99)
    fig.tight_layout()
    fig.savefig('PageRank_vs_in_out', dpi=500)
#%%
if False:
    # keep original graph
    G2=G_dir.to_undirected() # copy
    for (u,v) in G.edges():
        if not G_dir.has_edge(v,u):
            G2.remove_edge(u,v)
    float(G2.number_of_edges())/float(G_dir.number_of_edges())