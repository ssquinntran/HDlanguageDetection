import random_idx
import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys
import Queue
import lang_vec

k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alph = string.lowercase + ' '

#read from serialized files
fread = open("alice_RI_letters", "r")
fread1 = open("alice_lang_vectors", "r")
RI_letters = pickle.load(fread)
lang_vectors = pickle.load(fread1)
fread.close()
fread1.close()


search_words = ["foot"]#, "consider", "vanish", "the", "birthday", "she", "lady"]
lvl1_2 = np.add(lang_vectors[1], lang_vectors[2])
lvl1_2_3 = np.add(lvl1_2, lang_vectors[3])
qu_vector = random_idx.id_vector(N, "qu", alph, RI_letters, ordered)

"""
Clipping basically means limiting or saturating the max/min value of each element in a vector. In other words, we want to reduce the precision of vector. 
You can use a function like below to limit the max/min value of each element: n is the input value, and bitWidth is the number of bits that can be used to represent each element (bitWidth of 1 makes the vector as a binary vector). 

"""
def clamp_alphabet(alph_vecs):
    for letter_vec in RI_letters:
        for i in range(0, len(letter_vec)):
            if letter_vec[i] >= 0:
                letter_vec[i] = 1
            else:
                letter_vec[i] = -1

#def clamp(lang_vec, max, min):
def clamp_to_binary(lang_vec, boundary):
    print lang_vec
    for i in range(0, len(lang_vec)):
        for j in range(0, len(lang_vec[0])):
            if lang_vec[i][j] >= 0:
                lang_vec[i][j] = 1
            else:
                lang_vec[i][j] = -1

#returns a priority queue of most likely letter after prefix
def predict(pref, length):
    ngram = lang_vectors[length+1]
    #clamp the ngram. can clamp out of predict method
    prefix = random_idx.id_vector(N, word[0:length], alph, RI_letters, ordered)
    sprefix = np.roll(prefix, 1)
    prefix_ngram = np.multiply(ngram, sprefix)
    clamp_to_binary(prefix_ngram, 0)
    print prefix_ngram

    q = Queue.PriorityQueue()
    
    for i in range(26):
        #may need to np.transpose(vector)
        result = np.dot(prefix_ngram, RI_letters[i])
        #q.put((-n ,n))
        #priority, value
        #ranks the next letter by their dot products
        q.put((-result, result, length+1, pref, alph[i]))
    return q

if __name__ == "__main__":
    #f = open("letter_prediction_results.txt", "w")
    #f = open("letter_prediction_results_clipped.txt", "w")
    f = open("letter_prediction_results_w_alphabet_clipped.txt", "w")
    clamp_alphabet(RI_letters)
    for word in search_words:
        for i in range(0, len(word)-1):
            queue = predict(word[0:i+1], i+1)
            while not queue.empty():
                tpl = queue.get()
                f.write("dot product of %d-gram*s%s vector and %s letter vector is %d\n\n" % (tpl[2], tpl[3], tpl[4], tpl[1]))
    
    f.close()



#tried clamping only the language vector. results less accurate
#tried clamping RI_letters as well








