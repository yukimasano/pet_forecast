# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:09:37 2016
#The k-means problem is solved using Lloyd’s algorithm
@author: YPC
"""
import json
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import RandomizedPCA
import numpy as np
from random import shuffle
from sklearn.feature_extraction import text 





def make_cluster(range_n_clusters,max_feature_num, grams):
    f=open('../cluster_desc/petitions.json', 'r')
    met=json.load(f)
    f.close()
    ids=[]
    def get_desc():
        rows = []
        for i in range(len(met)):
            text=met[i]['petition']['description'].encode('ascii','replace')
            ids.append(met[i]['petition']['id'])
            if text!='':
                rows.append(text)
            else:
                print 'no text'
                rows.append('nil')
        return rows


    data= get_desc()
    ids=np.array(ids)
    data=data[:len(met)]
    petition_stop_words=['uk', 'people','government', 'petition', 'petitions',
                         'signatures','sign','british','undersigned','support','signature',
                         'united','uk','kingdom']
    
    stop_words = text.ENGLISH_STOP_WORDS.union(petition_stop_words)
    vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=grams,max_features=max_feature_num) # full 1grams=62595
    X = vectorizer.fit_transform(data)
        # Initialize the clusterer
    clusterer = KMeans(n_clusters=range_n_clusters, init='k-means++', max_iter=5000, n_init=10)
    cluster_labels = clusterer.fit_predict(X)
    id_cluster= np.array([ids, cluster_labels])
    np.save('cluster_info/%s-%s_grams_%sclustering.npy'%(grams[0],grams[1],range_n_clusters), id_cluster)