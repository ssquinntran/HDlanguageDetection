import os
import re
import sys
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle

from utils import random_idx
from utils import utils
from utils import lang_vectors_utils as lvu


k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alphabet = string.lowercase + ' '

def read_file(filepath="preprocessed_texts/english/alice-only-spaced.txt"):
    f = open(filepath, "r")
    text = f.read()
    #text = ''.join([x for x in text if x in alphabet])[0:10000]
    f.close()
    return text

def vec_explain_away(vocab_vec,max_length,text):
    #f = open(filepath, "r");
    #text = f.read();
    text = text.split(" ")
    #text = ''.join([x for x in text if x in alphabet])[0:10000];
    #f.close()

def update_unigrams(vocab_array, text):
    #handle case of 1 letter words:
    copy = text.split(" ")
    for word in copy:
        if len(word) == 1:
            if word in vocab_array[1].keys():
                vocab_array[1][word] += 1
            #do something about discovering unigrams

def tuples_to_text(tuples, text):
    texted = ""
    for tup in tuples:
        word = text[tup[0]:tup[1]]
        texted += " " + word
    return texted

# unioned windowing is way too slow.
# empty strings added to processed_indices. idk why
def dict_explain_away(vocab_dict,max_length,text):
    print len(text)
    # text[:] does not make a new copy
    duplicate = "%s" % text
    #print id(text)
    #print id(duplicate)
    # make a list of disjoint tuples of (start_index, end_index)
    processed_indices = []

    for i in range(len(vocab_dict)-1, -1,-1):
        for key in vocab_dict[i].keys():
            starts = [match.start() for match in re.finditer(re.escape(key), duplicate)]
            for start in starts:
                mask = " "*len(key)
                duplicate = duplicate[:start] + mask + duplicate[start+len(key):]
                processed_indices.append((start, start + len(key)))
    indices = [(pair[0],pair[1]) for pair in processed_indices if pair[0] < pair[1]]

    return sorted(indices)

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
def hard_em_discover_words(processing,vocab_array,max_length,filepath="preprocessed_texts/english/alice-only-stream.txt"):
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
    filepath = "preprocessed_texts/english/alice-only-spaced.txt"
    #lvu.initialize()
    lv, lang_vectors, n_gram_frequencies = lvu.initialize_from_file()
    vocab_vec, max_word_length = lvu.vocab_vector(lv, lang_vectors)
    vocab_dict = lvu.vocab_dict(max_word_length)

    filepath = "preprocessed_texts/english/alice-only-stream.txt"#a_christmas_carol.txt"
    text = read_file(filepath)
    processed_indices = dict_explain_away(vocab_dict,max_word_length,text)

    processed = tuples_to_text(processed_indices, text)

    fwrite = open("intermediate/processed_dict_explain_away_results","w")
    fwrite.write(processed)
    fwrite.close()

    #now for the em
    #not necessary in seeding phase. 
    #hed = hard_em_discover_words(aea, vocab_array, max_length, filepath)
    #file = open("../output/processed_array_explain_away_results","w")
    #file.write(hed)
    #file.close()

    # save data to file
    lvu.write_data_structures([lv, lang_vectors, n_gram_frequencies, vocab_vec, vocab_dict], \
        ["intermediate/lookup_lv", "intermediate/lookup_lang_vectors", \
        "intermediate/lookup_n_gram_frequencies", "intermediate/lookup_vocab_vec", \
        "intermediate/lookup_vocab_dict"])

seed()





