# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 14:21:37 2018

@author: ABC
"""
from nltk.corpus import stopwords
from nltk import word_tokenize
import numpy as np
import nltk 

def process(file):
    raw = open(file).read()
    #print(raw)
    tokens = word_tokenize(raw)
    words= [w.lower() for w in tokens]
    #print(words)
    porter = nltk.PorterStemmer()
    stemmed_tokens = [porter.stem(t) for t in words]
    
    stop_words = set(stopwords.words('english'))
    filtered_tokens=[w for w in stemmed_tokens if not w in stop_words]
    
    print(filtered_tokens)
    
    count = nltk.defaultdict(int)
    for word in filtered_tokens:
        count[word] += 1
    return count

def cos_sim(a,b):
    dot_product = np.dot(a,b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product/(norm_a * norm_b)

def get_similarity(dict1,dict2):
    all_words_list=[]
    for key in dict1:
        all_words_list.append(key)
    for key in dict2:
        all_words_list.append(key)
    all_word_list_size = len(all_words_list)
    
    v1 = np.zeros(all_word_list_size,dtype = np.int)
    v2 = np.zeros(all_word_list_size,dtype = np.int)
    i=0
    for (key) in all_words_list:
        v1[i]=dict1.get(key,0)
        v2[i]=dict1.get(key,0)
        i=i+1
    return cos_sim(v1,v2)

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(nltk.PorterStemmer().stem(item))
    return stems


dict1 = process('E:/nishikant project/Python/Cosine/1.txt')
dict2 = process('E:/nishikant project/Python/Cosine/2.txt')
#print(dict1)
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf1 = TfidfVectorizer(tokenizer=dict1, stop_words='english')
tfidf2 = TfidfVectorizer(tokenizer=dict2, stop_words='english')
nltk.cluster.cosine_distance(dict1,dict2)
print(tfidf1)
print(tfidf2)
#tfidf_matrix = tfidf_vectorizer.fit_transform('i am a boy')

#dict2 = process('E:/nishikant project/Python/Cosine/2.txt')
#print('similarity ',get_similarity(dict1,dict2))
