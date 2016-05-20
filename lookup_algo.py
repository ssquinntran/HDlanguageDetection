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
    f = open(filepath, "r")
    text = f.read()
    text = ''.join([x for x in text if x in alphabet])[0:10000]
    f.close()
    processing = "" #leftovers 
    #unioned windows and processing will handle the rest
    #window of 20 letters

    i = 0
    for i in range(0,(len(text)/20)*20):
        window = text[i:i+20]
        print window
        #theoretically less words than you think bc a lot of repeat words
        for j in range(1,len(vocab_array),-1):
            for k,v in vocab_array[j+1].items():
                windex = window.find(k)
                if windex > -1:
                    vocab_array[j+1][k] += 1
                    #word at the beginning
                    if windex == 0:
                        window = window[windex+len(k):]
                    elif windex + len(k) == len(window):
                    #word at the end
                        window = window[:windex]
                    else:
                        window = window[:windex] + " " + window[windex+len(k):]
        #how lame
        if len(window) > 0:
            processing += window[0]
    #edge case
    window = text[(len(text)/20)*20:len(text)]
    for i in range(1,len(vocab_array)-1):
        for k,v in vocab_array[i+1].items():
            windex = window.find(k)
            if windex > -1:
                    vocab_array[j+1][k] += 1
                    #word at the beginning
                    if windex == 0:
                        window = window[windex+len(k):]
                    elif windex + len(k) == len(window):
                    #word at the end
                        window = window[:windex]
                    else:
                        window = window[:windex] + " " + window[windex+len(k):]
        #how lame
        if len(window) > 0:
            processing += window[0]
    return processing
    
#lvu.initialize()
lv, lang_vectors, n_gram_frequencies = lvu.initialize_from_file()
vocab_vec, max_length = lvu.vocab_vector(lv, lang_vectors)
vocab_array, max_length = lvu.vocab_array()
for i in range(0,len(vocab_array)):
    if not vocab_array[i].keys():
        vocab_array = vocab_array[:i]
        break
aea = array_explain_away(vocab_array,max_length,"preprocessed_texts/alice-only-spaced.txt")
file = open("array_explain_away_results","w")
file.write(aea)
file.close()
    



    """
        #handle case of 1 letter words:
        new_window = ""
        for l in range(1,len(window)-1):
            temp = window[l-1:l+1]
            if temp.count(" ") == 2:
                vocab_array[j+1][k] += 1
                new_window += window[l+1:]
        processing += new_window
    #processing has spaces
   
    #if there are any words that aren't explained away, run em to decide what exactly is a word. 
    #don't include 1 letter words for now bc they're very popular and are probably already explained away
    #1 letter words may leave gaps in actual undiscovered words though
    #how can you tell if actual 1 letter word?
    #we should do 1-2 letter words separately.
    em_discover_words(processing, vocab_dict,max_length,filepath)
"""
def em_discover_words(processing, vocab_dict,max_length,filepath="preprocessed_texts/alice-only-spaced.txt"):
    pass
def vec_explain_away(vocab_vec,max_length,filepath="preprocessed_texts/alice-only-spaced.txt"):
    f = open(filepath, "r");
    text = f.read();
    text = text.split(" ")
    #text = ''.join([x for x in text if x in alphabet])[0:10000];
    f.close()



