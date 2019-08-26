#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 09:33:00 2018

@author: kateschulz
"""
import json
import re
import string
import numpy as np
import pandas as pd 
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


#read in twitter data file and tokenize
text = []
with open('data.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        text.append(tweet['text'])
    
text_str =  ' '.join(text)
tokens = word_tokenize(text_str)   

#remove punctuation, stopwords, Twitter tags, and non-alphabetic characters
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'https']
real_words = [word for word in tokens if word.lower() not in stop if word.isalpha()]

#stem remaining tokens
stemmer = SnowballStemmer("english")
terms =  ' '.join(real_words)
stem_words = stemmer.stem(terms)
word_list = re.sub("[^\w]", " ",  stem_words).split()

#create lists of tokens with frequency counts
count_words = list(Counter(word_list).keys())
count_nums = list(Counter(word_list).values())

#create csvs for all words and unique words with frequency counts
data_arr = np.array([np.array(xi) for xi in word_list])
data_df = pd.DataFrame(data_arr)
data_df.to_csv("data.csv", header = None, index = None)

data_counts_df = pd.DataFrame(np.column_stack([count_words, count_nums]), 
                               columns=['words', 'counts',])
data_counts_df.to_csv("data_with_counts.csv", header = None, index = None)


#create python word cloud of tweet words
words =  ' '.join(word_list)
wordcloud = WordCloud().generate(words)

plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

