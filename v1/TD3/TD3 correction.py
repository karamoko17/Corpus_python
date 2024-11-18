#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/05/2020

@author: julien and antoine
"""

# needs praw package, cf.: 
#https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
import praw

  
# Reddit

reddit = praw.Reddit(client_id='***identifiant***', client_secret='***motdepasse***', user_agent='***nom***')

subr = reddit.subreddit('Coronavirus')

textes_Reddit = []
#auteurs_Reddit = []
for post in subr.hot(limit=100):
#for post in subr.controversial(limit=10):
    texte = post.title
    texte = texte.replace("\n", " ")
    textes_Reddit.append(texte)
#    textes_Reddit = textes_Reddit + [post.title]
    #auteurs_Reddit = auteurs_Reddit + [post.author]

#txt = txt.replace('\n', ' ')

import urllib.request
import xmltodict 

textes_Arxiv = []

query = "covid"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()

# url_read est un "byte stream" qui a besoin d'être décodé
data =  url_read.decode()

dico = xmltodict.parse(data) #xmltodict permet d'obtenir un objet ~JSON
docs = dico['feed']['entry']
for d in docs:
    texte = d['title']+ ". " + d['summary']
    texte = texte.replace("\n", " ")
    textes_Arxiv.append(texte)

# on concatène tout ça :
    
corpus = textes_Reddit + textes_Arxiv

#print("Corpus length: %d" % len(corpus))
print("Longueur du corpus : " + str(len(corpus)))

for doc in corpus:
    # nombre de phrases
    print("Nombre de phrases : " + str(len(doc.split("."))))
    print("Nombre de mots : " + str(len(doc.split(" "))))

import numpy as np    

nb_phrases = [len(doc.split(".")) for doc in corpus]
print("Moyenne du nombre de phrases : " + str(np.mean(nb_phrases)))

nb_mots = [len(doc.split(" ")) for doc in corpus]
print("Moyenne du nombre de mots : " + str(np.mean(nb_mots)))

print("Nombre total de mots dans le corpus : " + str(np.sum(nb_mots)))

corpus_plus100 = [doc for doc in corpus if len(doc)>100]

chaine_unique = " ".join(corpus_plus100)

import pickle

with open("out.pkl", "wb") as f:
    pickle.dump(corpus_plus100, f)
    
with open("out.pkl", "rb") as f:
    corpus_plus100 = pickle.load(f)
    
import datetime

aujourdhui = datetime.datetime.now()
print(aujourdhui)






    
    