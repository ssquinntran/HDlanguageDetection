# log_random_idx.py
# creates random index vectors for a number of languages

# libraries
import sys
import numpy as np
import string
import utils
import pandas as pd
import os
import random_idx
import math
alphabet = string.lowercase + " "
lang_dir = '../preprocessed_texts/'

cluster_cache = {}

def generate_letter_id_vectors(N, k, alph=alphabet):
    # build row-wise k-sparse random index matrix
    # each row is random index vector for letter
    return random_idx.generate_letter_id_vectors(N, K, alph)
 
def generate_vocab_lang_vectors(N, RI_letters, cluster_sz, ordered, text_name, min_, max_,alph=alphabet):
    return random_idx.generate_vocab_lang_vectors(N, RI_letters, cluster_sz, ordered, text_name, min_, max_, alph)

def id_vector(N, cluster, alphabet, RI_letters,ordered=0):
    return random_idx.id_vector(N, cluster, alphabet, RI_letters, ordered)

def log_generate_RI_str(N, RI_letters, cluster_sz, ordered, string, alph=alphabet):
    # generate RI vector for string
    text_vector = random_idx.generate_RI_str(N, RI_letters, cluster_sz, ordered, string, alph)
    text_vector = np.log2(text_vector)
    return text_vector


def log_generate_RI_text(N, RI_letters, cluster_sz, ordered, text_name, \
n_gram_frequencies, alph=alphabet):
    # generate RI vector for "text_name"
    # assumes text_name has .txt

    text_vector = np.zeros((1, N))
    text = utils.load_text_spaces(text_name)
    for char_num in xrange(len(text)):

        if char_num < cluster_sz:
            continue
        else:
            # build cluster
            cluster = ''
            for j in xrange(cluster_sz):
                cluster = text[char_num - j] + cluster
            #record cluster sighting to frequencies

            if cluster not in n_gram_frequencies[cluster_sz].keys():
                n_gram_frequencies[cluster_sz][cluster] = 1
            else:
                n_gram_frequencies[cluster_sz][cluster] += 1
            text_vector += math.exp(-n_gram_frequencies[cluster_sz][cluster])*id_vector(N, cluster, alph,RI_letters, ordered)
    return text_vector

def log_generate_RI_text_fast(N, RI_letters, cluster_sz, ordered, text_name, alph=alphabet):
    text_vector = random_idx.generate_RI_text_fast(N, RI_letters, cluster_sz, ordered, text_name, alph)
    text_vector = np.log2(text_vector)
    return text_vector

def log_generate_RI_text_partitioned(N, RI_letters, cluster_sz, ordered, text, \
n_gram_frequencies, alph=alphabet):
    # generate RI vector for "text_name"
    # assumes text_name has .txt

    text_vector = np.zeros((1, N))
    for char_num in xrange(len(text)):

        if char_num < cluster_sz:
            continue
        else:
            # build cluster
            cluster = ''
            for j in xrange(cluster_sz):
                cluster = text[char_num - j] + cluster
            #record cluster sighting to frequencies

            if cluster not in n_gram_frequencies[cluster_sz].keys():
                n_gram_frequencies[cluster_sz][cluster] = 1
            else:
                n_gram_frequencies[cluster_sz][cluster] += 1
            text_vector += math.exp(-n_gram_frequencies[cluster_sz][cluster])*id_vector(N, cluster, alph,RI_letters, ordered)
    return text_vector

def log_generate_RI_text_words(N, RI_letters, text_name, alph=alphabet):
    text_vector = random_idx.generate_RI_text_words(N, RI_letters, text_name, alph)    
    text_vector = np.log2(text_vector)
    return text_vector

def log_generate_RI_text_history(N, RI_letters, text_name, alph=alphabet):
    text_vector = random_idx.generate_RI_text_history(N, RI_letters, text_name, alph)
    text_vector = np.log2(text_vector)
    return text_vector

def generate_RI_lang(N,RI_letters, cluster_sz, ordered, languages=None):
	return random_idx.generate_RI_lang(N,RI_letters, cluster_sz, ordered, languages)

def generate_RI_lang_history(N,RI_letters, languages=None):
	return random_idx.generate_RI_lang_history(N, RI_letters, languages)
       
def generate_RI_lang_words(N, RI_letters, languages=None):
	return random_idx.generate_RI_lang_words(N, RI_letters, languages)

def encode_sentence(N,RI_letters, cluster_sz, ordered, sentence, lang_vectors, \
    n_gram_frequencies, alph=alphabet):
	#find vector for each n-gram. 
	#scale it by frequency: dot product of vector and general n-gram vector for the entire text?
	# generate RI vector for string
    text_vector = np.zeros((1,N))
    for char_num in xrange(len(sentence)):

        if char_num < cluster_sz:
                continue
        else:
            # build cluster
            cluster = ''
            for j in xrange(cluster_sz):
                    cluster = sentence[char_num - j] + cluster
            part = id_vector(N, cluster, alph, RI_letters, ordered)
            #probability = np.dot(lang_vectors[len(cluster)], part)
            #need to / by total # bigrams. how do???
            probability = n_gram_frequencies[cluster_sz][cluster]/float(sum(n_gram_frequencies[cluster_sz].values()))
            part *= probability
            text_vector += part
    return text_vector


















