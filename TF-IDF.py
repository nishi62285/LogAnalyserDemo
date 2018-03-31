# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 20:50:38 2018

@author: ABC
"""

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform('i am a boy')
print(tfidf_matrix.shape)