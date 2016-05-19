import random_idx
import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys

k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alphabet = string.lowercase + ' '

# create language vector for Alice in Wonderland made of summed n-gram vectors for each
# n in cluster_sizes
def create_lang_vec(filename, cluster_sizes, N=N, k=k):
    
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = random_idx.generate_RI_text_fast(N, alphabet, cz, ordered, filename, alphabet)#"preprocessed_texts/AliceInWonderland.txt", alph)
        total_lang += lang_vector
    return total_lang

def initialize(filepath="preprocessed_texts/alice-only-spaced.txt"):#AliceInWonderland.txt"):
    n_grams = []
    # RI_letters = random_idx.generate_letter_id_vectors(N, k, alph)
    lv = random_idx.generate_letter_id_vectors(N,15000);
    f = open(filepath, "r");
    text = f.read();
    text = ''.join([x for x in text if x in alphabet])[0:10000];
    #for each n, dictionary of key: n gram and value: frequency
    n_gram_frequencies = [{} for _ in range(len(cluster_sizes) + 1)]

    # lang_vectors in sizes 1-8
    lang_vectors = []
    for size in cluster_sizes:
        lang_vectors.append(create_lang_vec(filepath,[size]))
    lang_vectors.insert(0, np.zeros((1,N)))

    # save vectors to file
    fwrite = open("lv", "w")
    fwrite1 = open("lang_vectors", "w")
    fwrite2 = open("n_gram_frequencies", "w")
    pickle.dump(lv, fwrite)
    pickle.dump(lang_vectors, fwrite1)
    pickle.dump(n_gram_frequencies, fwrite2)
    fwrite.close()
    fwrite1.close()
    fwrite2.close()

def initialize_from_file():
    # save vectors to file
    fread = open("lv", "r")
    fread1 = open("lang_vectors", "r")
    fread2 = open("n_gram_frequencies", "r")
    lv = pickle.load(fread)
    lang_vectors = pickle.load(fread1)
    n_gram_frequencies = pickle.load(fread2)
    fread.close()
    fread1.close()
    fread2.close()
    return lv, lang_vectors, n_gram_frequencies

def get_letter_vec(s, letter_vec):
    if(len(s) == 1):
        return letter_vec[alphabet.index(s)];
    vec = letter_vec[alphabet.index(s[0])];
    for i in s[1:]:
        vec = np.multiply(np.roll(vec, 1), letter_vec[alphabet.index(i)]);
    return vec;


def recover_frequency(letter_vec, s, array):
    vec = get_letter_vec(s, letter_vec);
    return np.dot(vec, array[len(s)-1]);
