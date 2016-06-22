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
def create_lang_vec(filename, lv, cluster_sizes, N=N, k=k):
    
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = random_idx.generate_RI_text_fast(N, lv, cz, ordered, filename, alphabet)#"preprocessed_texts/AliceInWonderland.txt", alph)
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
        lang_vectors.append(create_lang_vec(filepath, lv, [size]))
    lang_vectors.insert(0, np.zeros((1,N)))

    # save vectors to file
    fwrite = open("intermediate/lv", "w")
    fwrite1 = open("intermediate/lang_vectors", "w")
    fwrite2 = open("intermediate/n_gram_frequencies", "w")
    pickle.dump(lv, fwrite)
    pickle.dump(lang_vectors, fwrite1)
    pickle.dump(n_gram_frequencies, fwrite2)
    fwrite.close()
    fwrite1.close()
    fwrite2.close()

def initialize_from_file():
    # save vectors to file
    fread = open("intermediate/lv", "r")
    fread1 = open("intermediate/lang_vectors", "r")
    fread2 = open("intermediate/n_gram_frequencies", "r")
    lv = pickle.load(fread)
    lang_vectors = pickle.load(fread1)
    n_gram_frequencies = pickle.load(fread2)
    fread.close()
    fread1.close()
    fread2.close()
    return lv, lang_vectors, n_gram_frequencies

def write_data_structures(data_structures=[], file_paths=[]):
    for i in range(0,len(file_paths)):
        fwrite = open(file_paths[i], "w")
        pickle.dump(data_structures[i], fwrite)
        fwrite.close()

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
#should we separate by cluster sizes? following precedent, guess not
def vocab_vector(lv, lang_vectors, filepath="preprocessed_texts/alice-only-spaced.txt"):
    f = open(filepath, "r");
    text = f.read()
    text = text.split(" ")
    #text = ''.join([x for x in text if x in alphabet])[0:10000];
    vocab_vec = np.zeros((1,N))
    max_length = 0
    for word in text:
        #print "generating vocab vector of cluster size", len(word)
        word_vec = random_idx.id_vector(N, word, alphabet, lv, ordered)
        vocab_vec += word_vec
        if len(word) > max_length:
            max_length = len(word)
    f.close()
    return vocab_vec, max_length
#array with cluster size as index, the dictionary of words in that index
def vocab_dict(max_word_length, filepath="preprocessed_texts/alice-only-spaced.txt"):
    f = open(filepath, "r");
    text = f.read();
    text = text.split(" ")
    #text = ''.join([x for x in text if x in alphabet])[0:10000];
    #max word length is 20 letters lol
    vocab_dict = [{} for i in range(0,max_word_length)]

    for word in text:
        if word not in vocab_dict[len(word)-1].keys():
            vocab_dict[len(word)-1][word] = 1
        else:
            vocab_dict[len(word)-1][word] += 1
    f.close()
    return vocab_dict
