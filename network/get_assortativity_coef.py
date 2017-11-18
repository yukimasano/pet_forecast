# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:47:20 2016

@author: YPC
"""
import networkx as nx
import numpy as np
uu=np.load('mentions.npy')
G_dir = nx.from_edgelist(uu,create_using=nx.DiGraph())
G = nx.from_edgelist(uu)
#r= nx.degree_assortativity_coefficient(G_dir)
r= nx.average_clustering(G)
print r