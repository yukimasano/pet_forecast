# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:32:52 2016

@author: YPC
"""

import numpy as np
import csv


def get_growth(pet_in,sig_full,pet_full,N):
    if N==0:
        N = len(pet_full)
    pet_in=int(pet_in)
    g=[]
    for i in range(len(pet_full)):
        if pet_full[i]==pet_in:
            g.append(sig_full[i])
            if len(g)>N+1:
                break
    return np.array(g)

def get_growth_tsv(pet_in, N):
    if N==0:
        N= 1e20
    pet_in=int(pet_in)
   # with open('C:/Users/YPC/Documents/growth/%s.tsv'%pet_in,'rb') as csvfile:
    with open('/mi/share/scratch/asano/growth/%s.tsv'%pet_in,'rb') as csvfile:
     reader = csv.reader(csvfile, delimiter='\t')
     sig=[]
     k=0
     for row in reader: 
         k+=1
         sig.append(int(row[2]))
         if k>N:
             break
    return sig
            
        