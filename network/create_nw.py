# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 19:53:49 2016

@author: YPC
"""
import numpy as np
from scipy.sparse import csr_matrix
import csv
row = np.array([0, 0, 1, 2, 2, 2])
col = np.array([0, 2, 2, 0, 1, 2])
data = np.array([1, 2, 3, 4, 5, 6])
csr_matrix((data, (row, col)), shape=(3, 3)).toarray()


#%%
with open('../twitter/output_mentions.csv','rb') as csvfile:
     reader = csv.reader(csvfile, delimiter=',')
     k=0
     next(reader)
     u=[]

     for row in reader:
         k+=1
         r=row[0].split('\t') 
         u.append([r[0],r[1]])

u=np.array(u)
b = np.ascontiguousarray(u).view(np.dtype((np.void, u.dtype.itemsize * u.shape[1])))
_, idx = np.unique(b, return_index=True)
unique_mentions = u[idx]
#np.save('mentions.npy',unique_mentions)

#%%    NUMBER OF people who created tweet etc.
#l=np.load('id1.npy')
#
#len(np.unique(l))
#Out[36]: 201918
#
#k=np.load('id2.npy')
#
#len(np.unique(k))
#Out[38]: 142267




#%% wow wasted 3-4h
if False:
    id1=[]
    id2=[]
    all_u =np.unique(unique_mentions[:,:],return_index =False)
    all_u.sort()
    unique_mentions_ints=np.zeros(shape=unique_mentions.shape, dtype=int)
    for i in range(unique_mentions.shape[0]):
         a,b = unique_mentions[i,:]
         unique_mentions_ints[i,:]= [np.searchsorted(all_u, a),np.searchsorted(all_u, b)]
    #     if any(id1==a):
    #         sd
    #     else:
    #         id1.append(np.searchsorted(all_u, a))
    #         id2.append(np.searchsorted(all_u, b))
    
    id1=unique_mentions_ints[:,0]
    id2=unique_mentions_ints[:,1]
    data=np.ones(len(id1))
    print unique_mentions.shape, len(all_u), len(id1), len(np.unique(id1))
    number_of_people= np.max([np.max(id1), np.max(id2)]) +1
    #np.save('id1.npy',id1)
    #np.save('id2.npy',id2)
    """construct with:"""
    A= csr_matrix((data, (id1, id2)), shape=(number_of_people, number_of_people),dtype=int)