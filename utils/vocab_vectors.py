"""
We will be experimenting with two 10,000-dimensional
vocabulary vectors, (1) a Full-Words Vector and (2) a
Substrings Vector.

The Full-Words vector is the sum of L-gram vectors, one
per vocabulary word, where L is the length of the word.

The Substrings vector is a bit more challenging.  It is the
sum that includes every N-gram of every vocabulary word, but
excludes 1-grams (individual letters) of words that have 2
or more letters.  How many N-grams are there anyway in an
L-letter word? L-1?
"""
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

ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alph = string.lowercase + ' '

# create language vector for Alice in Wonderland made of summed n-gram vectors for each
# n in cluster_sizes
def create_full_words_vec(vocab_file, N=N, k=k):
    fread = open(vocab_file, "r")
    fwrite = open("../intermediate/alice_full_words_vec", "w")
    total_lang = np.zeros((1,N))

    for line in fread:
        word = line[:line.index(":")]
        word_vector = random_idx.id_vector(N, word, alph, RI_letters, ordered)
        total_lang += word_vector
    
    pickle.dump(total_lang, fwrite)
    fread.close()
    fwrite.close()
    return total_lang

def create_substrings_vec(vocab_file, N=N, k=k):
    fread = open(vocab_file, "r")
    fwrite = open("../intermediate/alice_substring_vec", "w")
    total_lang = np.zeros((1,N))
    
    for line in fread:
        word = line[:line.index(":")]
        sub_vector = np.zeros((1,N))
        for i in range(1,len(word)):
            sub_vector += random_idx.id_vector(N, word, alph, RI_letters, ordered)
        total_lang += sub_vector
    
    pickle.dump(total_lang, fwrite)
    fread.close()
    fwrite.close()
    return total_lang

if __name__ == "__main__":
    #read from serialized files
    fread = open("../intermediate/alice_RI_letters", "r")
    RI_letters = pickle.load(fread)

    vocab_vec = create_full_words_vec("../intermediate/vocab.txt")
    fread1 = open("../intermediate/alice_full_words_vec", "r")
    vocab_vec = pickle.load(fread1)
    print(vocab_vec)

    substring_vec = create_substrings_vec("../intermediate/vocab.txt")
    fread2 = open("../intermediate/alice_substring_vec", "r")
    substring_vec = pickle.load(fread2)
    print(substring_vec)

    fread.close()
    fread1.close()
    fread2.close()
    
