# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:47:29 2016

@author: asano
"""


import matplotlib.pyplot as plt
import json
import numpy as np

f=open('../petitions.json', 'r')
met=json.load(f)
f.close()
s=[]
s2=[]
pets=np.array([62385,67911,19149,67752,67165,57])
""" this plots the signature distribution function"""
#%%
for i in range(len(met)):
    if any( pets==met[i]['petition']['id']):
        print 'id', met[i]['petition']['id']
        print 'title', met[i]['petition']['title'].encode(errors='ignore')
       # print met[i]['petition']['description'].encode(errors='ignore')
        print 'date', met[i]['petition']['last_update_datetime'].encode(errors='ignore')
        print 'signature_count', met[i]['petition']['signature_count']
       # if met[i]['petition']['response'] != None:
        #    print met[i]['petition']['response'] .encode(errors='ignore')