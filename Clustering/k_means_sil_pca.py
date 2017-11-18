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
data=data[:len(met)/2]
petition_stop_words=['uk', 'people','government', 'petition', 'petitions',
                     'signatures','sign','british','undersigned','support','signature',
                     'united','uk','kingdom']

stop_words = text.ENGLISH_STOP_WORDS.union(petition_stop_words)
vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=(1,2),max_features=5000) # full 1grams=62595
X = vectorizer.fit_transform(data)
#%% finding good value for k
plt.close("all")
if True:
    range_n_clusters = [4,5,6]
    for n_clusters in range_n_clusters:
        # Initialize the clusterer
        clusterer = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=1000, n_init=20)
        cluster_labels = clusterer.fit_predict(X)
        
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)
        fig, (ax1,ax2) = plt.subplots(1,2)
        fig.set_size_inches(7, 4.5)
        ax1.set_ylim([0, len(data) + (n_clusters + 1) * 10])
        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
        ax1.set_xlim([-0.02, 0.1])
        y_lower = 50
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]
    
            ith_cluster_silhouette_values.sort()
    
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
    
            color = cm.spectral(float(i) / n_clusters)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)
    
            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.01, y_lower + 0.5 * size_cluster_i, str(i))
    
            # Compute the new y_lower for next plot
            y_lower = y_upper + 50  # 10 for the 0 samples
    
        ax1.set_title("Silhouette plot for the various clusters",fontsize=12)
        ax1.set_xlabel("Silhouette coefficient")
        ax1.set_ylabel("Cluster label")
    
        # The vertical line for average silhoutte score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    
        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([0, 0.02, 0.04, 0.06, 0.08, .1])
        plt.show()
 #       fig.savefig('silhouette50_%s'%n_clusters, dpi=700)
    #    # 2nd Plot showing the actual clusters formed

        pca = RandomizedPCA(n_components=2)
        reduced_data = pca.fit_transform(X.toarray())
        print "PCA done"
        centroids = pca.transform(clusterer.cluster_centers_)
        for i in range(n_clusters):
            col = cm.spectral(float(i) / n_clusters) 
            ax2.plot(reduced_data[np.argwhere(cluster_labels==i), 0], reduced_data[np.argwhere(cluster_labels==i), 1], \
                     '.', markersize=4, alpha=0.6,color=col)
            ax2.scatter(centroids[:, 0], centroids[:, 1],
                        marker='x', s=169, linewidths=3,
                        color='w', zorder=10)
            ax2.set_xticks([])
            ax2.set_yticks([])
            ax2.set_xticklabels([])
            ax2.set_xlabel("1st PCA component")
            ax2.set_ylabel("2nd PCA component")
            ax2.set_title("PCA Projection",fontsize=12)
        plt.suptitle(("Silhouette analysis for K-Means clustering "
                      "with %d clusters" % n_clusters),y=0.98,
                     fontsize=14, fontweight='bold')
        plt.show()
        fig.savefig('1_and_2_gram_silhouette50_pca_%s'%n_clusters, dpi=700)
#%%
if False:
    print " Computing PCA decomp and projection"
    from sklearn.decomposition import RandomizedPCA
    for true_k in range(4,6):
        pca = RandomizedPCA(n_components=2)
        reduced_data = pca.fit_transform(X.toarray())
        print "PCA finished"
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=500, n_init=10)
        
        fig = plt.figure()
        plt.clf()
        
        do_in_pca=False
        if do_in_pca==True:
            m = model.fit(reduced_data) 
            labs = m.labels_
            centroids = m.cluster_centers_
        else:
            m = model.fit(X) 
            labs = m.labels_
            centroids = pca.transform(m.cluster_centers_)
            
        for i in range(true_k):
            col = cm.spectral(float(i) / true_k) 
            plt.plot(reduced_data[np.argwhere(labs==i), 0], reduced_data[np.argwhere(labs==i), 1], \
            '.', markersize=4, alpha=0.8,color=col)
           
        # Plot the centroids as a white X
        plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='x', s=169, linewidths=3,
                    color='w', zorder=10)
        plt.title('K-means clustering projected to first two PCA dimensions\n'
                  'Centroids are marked with white cross')
        plt.xticks(())
        plt.yticks(())
        plt.show()
      #  fig.savefig('rPCA100_5k_%s'%true_k, dpi=700)

