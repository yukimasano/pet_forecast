# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 21:28:06 2016

@author: YPC
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
uu=np.load('mentions.npy')
G = nx.from_edgelist(uu,create_using=nx.DiGraph())

G.remove_edges_from(G.selfloop_edges())
#%%

#%%
if True:
    out_degrees=sorted(G.out_degree().values(),reverse=True)
    dmax=max(out_degrees)
    out_degrees=np.array(out_degrees)
    y = np.log(out_degrees[out_degrees!=0][10:50000]) 
    x= np.log(range(10, len(y)+10))
    
    m,b = np.polyfit(x, y, 1)
    y10= np.exp(m*np.log(10) +b)
    y100= np.exp(m*np.log(50000 )+b)
    """
    degree_sequence=np.array(degree_sequence)
    >>> sum(degree_sequence==0)
    62
    >>> sum(degree_sequence==1)
    169940
    >>> sum(degree_sequence>1000)
    106
    """
    fig=plt.figure(figsize=(7, 4.5))
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    plt.loglog(out_degrees,'-',color='darkblue',marker='x')
    plt.loglog([10,50000],[y10,y100] ,'-', marker='.',color='orange',linewidth=3,markersize=10)
    plt.title("Cumulative Out-degree distribution")
    plt.ylabel("Out-degree")
    plt.legend(["Out-degree distribution","Power-law fit, c=%s"%np.round(m,2)], fontsize=11)
    plt.xlabel("Rank")
    
    fig.savefig('out_degree_rank', dpi=500)
    G=nx.DiGraph(G)
    in_degrees=sorted(G.in_degree().values(),reverse=True)
    
    dmax=max(in_degrees)
    in_degrees=np.array(in_degrees)
    y = np.log(in_degrees[in_degrees!=0][10:10000]) 
    x= np.log(range(10, len(y)+10))
    
    m,b = np.polyfit(x, y, 1)
    y10= np.exp(m*np.log(10) +b)
    y100= np.exp(m*np.log(50000 )+b)
    """
    degree_sequence=np.array(degree_sequence)
    >>> sum(degree_sequence==0)
    62
    >>> sum(degree_sequence==1)
    169940
    >>> sum(degree_sequence>1000)
    106
    """
    fig=plt.figure(figsize=(7, 4.5))
    plt.rcParams.update({'font.size': 15})
    plt.rc('font', family='serif')
    plt.loglog(in_degrees,'-',color='darkblue',marker='x')
    plt.loglog([10,50000],[y10,y100] ,'-', marker='.',color='orange',linewidth=3,markersize=10)
    plt.title("Cumulative In-degree distribution")
    plt.ylabel("In-Degree")
    plt.legend(["In-degree distribution","Power-law fit, c=%s"%np.round(m,2)], fontsize=11)
    plt.xlabel("Rank")
    
    fig.savefig('in_degree_rank', dpi=500)

