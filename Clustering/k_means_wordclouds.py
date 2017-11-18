# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:09:37 2016
#The k-means problem is solved using Lloyd’s algorithm
@author: YPC
"""
import json
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline
import numpy as np
from random import shuffle
from sklearn.feature_extraction import text 


f=open('petitions.json', 'r')
met=json.load(f)
f.close()
def get_desc():
    rows = []
    for i in range(len(met)):
        text=met[i]['petition']['description'].encode('ascii','replace')
        if text!='':
            rows.append(text)
        else:
            print 'no text'
            rows.append('nil')
    return rows
data= get_desc()
shuffle(data)
data=data[:len(met)]
petition_stop_words=['uk', 'people','government', 'petition', 'petitions',
                     'signatures','sign','british','undersigned','support','signature',
                     'united','uk','kingdom']

stopwords = text.ENGLISH_STOP_WORDS.union(petition_stop_words)
vectorizer = TfidfVectorizer(stop_words=stopwords,ngram_range=(1,2),max_features= 5000)
X = vectorizer.fit_transform(data)
#%%
true_k = 6
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=20)
model.fit(X)
print("Computing central terms per cluster.")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
v_oc =  model.cluster_centers_
terms = vectorizer.get_feature_names()
for i in range(true_k):
    f = open('cluster_terms_2grams%s_%s.txt'%(true_k,i), 'w')
   # f.write("Cluster %d:" % i)
   # f.write("\n")
   # f.write("\n")
    print "next cluster"
    for ind in order_centroids[i, :50]:
        f.write('%s: %s' % (terms[ind], np.round(v_oc[i, ind]*100, decimals=4)))
        print '%s: %s' % (terms[ind], np.round(v_oc[i, ind]*100, decimals=4))
        f.write("\n")
    f.close()
    
#%%
