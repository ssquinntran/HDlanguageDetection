#from ..utils import random_idx
#from ..utils import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys
#from ..utils import lang_vectors_utils as lvu

k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alphabet = string.lowercase + ' '

def vec_explain_away(vocab_vec,max_length,filepath="../preprocessed_texts/english/alice-only-spaced.txt"):
    f = open(filepath, "r");
    text = f.read();
    text = text.split(" ")
    #text = ''.join([x for x in text if x in alphabet])[0:10000];
    f.close()

def update_unigrams(vocab_array, text):
    #handle case of 1 letter words:
    copy = text.split(" ")
    for word in copy:
        if len(word) == 1:
            if word in vocab_array[1].keys():
                vocab_array[1][word] += 1
            #do something about discovering unigrams

def array_explain_away(vocab_dict,max_length,filepath="../preprocessed_texts/english/alice-only-spaced.txt"):
    f = open(filepath, "r")
    text = f.read()
    #text = ''.join([x for x in text if x in alphabet])[0:10000]
    f.close()
    processing = "" 
    #unioned windows and processing will handle the rest
    #window of 20 letters
    #add padding to fit window
    num_padds = len(text)%20
    pads = " " * num_padds
    text += pads
    i = 0
    for i in range(0,(len(text)/20)*20):
        window = text[i:i+20]
        #theoretically less words than you think bc a lot of repeat words
        for j in range(1,len(vocab_array),-1):
            for k,v in vocab_array[j+1].items():
                windex = window.find(k)
                if windex > -1:
                    vocab_array[j+1][k] += 1
                    #word at the beginning
                    if windex == 0:
                        window = k + " " + window[windex+len(k):]
                    elif windex + len(k) == len(window):
                    #word at the end
                        window = window[:windex] + " " + k
                    else:
                        window = window[:windex] + " " + window[windex+len(k):]
        #how lame
        if len(window) > 0:
            processing += window[0]
    # apparently case of 1 letter words implicitly handled
    # can do a count to keep frequencies consistent
    update_unigrams(vocab_array,text)
    return processing

#doesn't consider words we've already known. compound words and/or similar words may be awko taco
def hard_e_step(word,new_phrases):
    for cluster_sz in range(0,len(word)):
            #edge case handled in windowing starting from left
            for i in range(0,(len(word)/cluster_sz)*cluster_sz):
                temp = word[i:i+cluster_sz]
                if temp not in new_phrases[cluster_sz].keys():
                    new_phrases[cluster_sz][temp] = 1
                else:
                    new_phrases[cluster_sz][temp] += 1
#returns split or not split word depending on location of most popular prefix of word
#denominators all the same per cluster size
#records frequencies and word(s) in vocab_array
def hard_m_step(word,new_phrases,vocab_array):
    prefindex = {}
    for i in range(0,len(word)):
        prefindex[i] = 1
        #tailored cluster size
        for j in range(i+1,len(word)):
            prefindex[i] *= new_phrases[len(word[j:])][word[j:]]
    #find max and break ties by prioritizing longer string aka smaller index
    freq = 0
    index = 0
    for k,v in prefindex.items():
        if v > freq:
            freq = v
            index = k
        if v == freq and k < index:
            index = k
    if k > 0 and k < len(word)-1:
        return [word[:index],word[index:]]
    return [word]

"""
if there are any words that aren't explained away, run em to decide what exactly is a word. 
#include 1 letter words LATER for now bc they're very popular and are probably already explained away
#denominators all the same so just compare ngrams with the same size
#for each phrase, determine words as you run through text again. max step
"""
def hard_em_discover_words(processing,vocab_array,max_length,filepath="../preprocessed_texts/english/alice-only-stream.txt"):
    all_words = processing.split(" ")
    new_words = set()
    new_phrases = [{} for i in range(0,len(vocab_array)+1)]
    processed = ""
    for word in all_words:
        if word not in vocab_array[len(word)].keys():
            new_words.add(word)
            hard_e_step(word,new_phrases)

    for word in all_words:
        if word in new_words and word not in vocab_array[len(word)].keys():
            ws = hard_m_step(word,new_phrases,vocab_array)
            for w in ws:
                vocab_array[len(w)][w] = 1
                processed += ws + " "
        elif word in new_words: #if repeated discovered word
            processed += word + " "
            vocab_array[len(word)][word] += 1
        else: #if already known word
            processed += word + " "
    return processed
def seed():
    filepath = "../preprocessed_texts/english/alice-only-spaced.txt"
    #lvu.initialize()
    lv, lang_vectors, n_gram_frequencies = lvu.initialize_from_file()
    vocab_vec, max_length = lvu.vocab_vector(lv, lang_vectors)
    vocab_array, max_length = lvu.vocab_array()
    for i in range(0,len(vocab_array)):
        if not vocab_array[i].keys():
            vocab_array = vocab_array[:i]
            break

    aea = array_explain_away(vocab_array,max_length,filepath)
    file = open("../intermediate/processing_array_explain_away_results","w")
    file.write(aea)
    file.close()

    #now for the em
    #not necessary in seeding phase. 
    #hed = hard_em_discover_words(aea, vocab_array, max_length, filepath)
    #file = open("../output/processed_array_explain_away_results","w")
    #file.write(hed)
    #file.close()

    # save data to file
    fwrite = open("../intermediate/lookup_lv", "w")
    fwrite1 = open("../intermediate/lookup_lang_vectors", "w")
    fwrite2 = open("../intermediate/lookup_n_gram_frequencies", "w")
    fwrite3 = open("../intermediate/lookup_vocab_vec", "w")
    fwrite4 = open("../intermediate/lookup_vocab_array", "w")
    pickle.dump(lv, fwrite)
    pickle.dump(lang_vectors, fwrite1)
    pickle.dump(n_gram_frequencies, fwrite2)
    pickle.dump(vocab_vec, fwrite3)
    pickle.dump(vocab_array, fwrite4)
    fwrite.close()
    fwrite1.close()
    fwrite2.close()
    fwrite3.close()
    fwrite4.close()


