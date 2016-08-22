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

def update_unigrams(vocab, text):
    #handle case of 1 letter words:
    copy = text.split(" ")
    for word in copy:
        if len(word) == 1:
            if word in vocab[1].keys():
                vocab[1][word] += 1
            #do something about discovering unigrams

def tuples_to_text(tuples, text):
    texted = ""
    for tup in tuples:
        word = text[tup[0]:tup[1]]
        texted += " " + word
    return texted

# unioned windowing is way too slow.
# empty strings added to processed_indices. idk why
def dict_explain_away(vocab,max_length,text):
    print len(text)
    # text[:] does not make a new copy
    duplicate = "%s" % text
    #print id(text)
    #print id(duplicate)
    # make a list of disjoint tuples of (start_index, end_index)
    preprocessed_indices = []

    for i in range(len(vocab)-1, -1,-1):
        for key in vocab[i].keys():
            starts = [match.start() for match in re.finditer(re.escape(key), duplicate)]
            for start in starts:
                mask = " "*len(key)
                duplicate = duplicate[:start] + mask + duplicate[start+len(key):]
                preprocessed_indices.append([start, start + len(key)])
    processed_indices = [[pair[0],pair[1]] for pair in preprocessed_indices if pair[0] < pair[1]]

    return sorted(processed_indices)

# create a threshold > 0 so that if a word really is new 
# (not connected to any known roots), then add to vocab
def hard_e_step(word,vocab):
    cluster_size = len(vocab)
    # if word is > max vocab
    if len(word) < cluster_size:
        cluster_size = len(word)
    potential_words = []
    for i in range(cluster_size-1, -1,-1):
        for key in vocab[i].keys():
            dot_product = key.vector * word.vector
            if dot_product > 0:
                potential_words.append([dot_product, key])
    return potential_words
# ARGH FIX PSEUDOCODE

# records frequencies and word(s) in vocab
def hard_m_step(word,potential_words,vocab):
    sorted(potential_words)
    if not potential_words:
        vocab[len(word)][word] = 1 # or is it vocab[len(word)-1]
        return None
    potential_word = potential_words[len(potential_words)-1]
    vocab[len(word)][potential_word] += 1 # or is it vocab[len(word)-1]
    return potential_word

def hard_em_discover_words(processed_indices,vocab,text):
    # find the left over intervals
    undiscovered = []
    for i in range(0,len(processed_indices)-1):
        start = processed_indices[i][1]
        end = processed_indices[i+1][0]-1
        if start < end:
            undiscovered.append([start, end])
            #print text[start:end]
    print undiscovered

    processed = []
    for pair in undiscovered:
        word = text[pair[0]:pair[1]]
        potential_words = hard_e_step(word,vocab)
        potential_word = hard_m_step(word,potential_words,vocab)
        
    return undiscovered

def seed():
    filepath = "preprocessed_texts/english/alice-only-spaced.txt"
    #lvu.initialize()
    lv, lang_vectors, n_gram_frequencies = lvu.initialize_from_file()
    vocab_vec, max_word_length = lvu.vocab_vector(lv, lang_vectors)
    vocab = lvu.vocab(max_word_length)

    filepath = "preprocessed_texts/english/alice-only-stream.txt"#a_christmas_carol.txt"
    text = read_file(filepath)
    processed_indices = dict_explain_away(vocab,max_word_length,text)

    processed = tuples_to_text(processed_indices, text)

    fwrite = open("intermediate/processed_dict_explain_away_results","w")
    fwrite.write(processed)
    fwrite.close()

    # now for the em
    # not necessary in seeding phase. 
    hed = hard_em_discover_words(processed_indices, vocab, text)
    #file = open("../output/processed_array_explain_away_results","w")
    #file.write(hed)
    #file.close()

    # save data to file
    lvu.write_data_structures([lv, lang_vectors, n_gram_frequencies, vocab_vec, vocab], \
        ["intermediate/lookup_lv", "intermediate/lookup_lang_vectors", \
        "intermediate/lookup_n_gram_frequencies", "intermediate/lookup_vocab_vec", \
        "intermediate/lookup_vocab"])

seed()





