import random_idx
import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys
import lang_vectors_utils as lvu

k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alphabet = string.lowercase + ' '

def array_explain_away(vocab_dict,max_length,filepath="preprocessed_texts/alice-only-spaced.txt"):
	f = open(filepath, "r");
    text = f.read();
    text = ''.join([x for x in text if x in alphabet])[0:10000];
    f.close()
    processing = "" #leftovers because windows are disjoint (for now)
    #should not be disjoint. the union would be quickly diminished by lookup. lel
    #window of 20 letters
    #let's do disjoint windows instead

    i = 0
    for i in range(0,(len(text)/20)*20,20):
    	window = text[i:i+20]
    	#theoretically less words than you think bc a lot of repeat words
    	for j in range(0,len(vocab_array),-1):
    		for k,v in vocab_array[j+1].items():
    			windex = window.find(k)
    			if windex > -1
    				vocab_array[j+1][k] += 1
    				#need to check if windex+1 is in bounds
    				window = window[:windex] + window[windex+1:]
    	processing += window
    #edge case. possibly not enough
    for i in range(0,len(text)):



def vec_explain_away(vocab_vec,max_length,filepath="preprocessed_texts/alice-only-spaced.txt"):
	f = open(filepath, "r");
    text = f.read();
    text = text.split(" ")
    #text = ''.join([x for x in text if x in alphabet])[0:10000];
    f.close()


#lvu.initialize()
lv, lang_vectors, n_gram_frequencies = lvu.initialize_from_file()
vocab_vec, max_length = lvu.vocab_vector(lv, lang_vectors)
vocab_array, max_length = lvu.vocab_array()
for i in range(0,len(vocab_array)):
	if not vocab_array[i].keys():
		vocab_array = vocab_array[:i]
		break

    
