import random_idx
import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys
import Queue
from ..exercises import lang_vec

k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alph = string.lowercase + ' '

RI_letters = random_idx.generate_letter_id_vectors(N, k, alph)
# lang_vectors in sizes 1-8

lang_vectors = []
for size in cluster_sizes:
    lang_vectors.append(lang_vec.create_lang_vec([size]))
lang_vectors.insert(0, np.zeros((1,N)))


# fread = open("alice_RI_letters", "r")
# fread1 = open("alice_lang_vectors", "r")
# RI_letters = pickle.load(fread)
# lang_vectors = pickle.load(fread1)
# fread.close()
# fread1.close()


search_words = ["foot", "runs"]#, "consider", "vanish", "the", "she", "lady"]
added_lvls = [lang_vectors[1]]
added_lvls.append(lang_vectors[2])
lvl2_3 = np.add(lang_vectors[2], lang_vectors[3])
lvl2_3_4 = np.add(lvl2_3, lang_vectors[4])
added_lvls.append(lvl2_3)
added_lvls.append(lvl2_3_4)


"""
Clipping basically means limiting or saturating the max/min value of each element in a vector. In other words, we want to reduce the precision of vector. 
You can use a function like below to limit the max/min value of each element: n is the input value, and bitWidth is the number of bits that can be used to represent each element (bitWidth of 1 makes the vector as a binary vector). 

"""

def clamp(lang_vec, Min, Max):
    for i in range(0, len(lang_vec)):
        for j in range(0, len(lang_vec[0])):
            if lang_vec[i][j] > Max:
                lang_vec[i][j] = Max
            elif lang_vec[i][j] < Min:
                lang_vec[i][j] = Min

def clamp_to_binary(lang_vec, boundary):
    #print lang_vec
    for i in range(0, len(lang_vec)):
        for j in range(0, len(lang_vec[0])):
            if lang_vec[i][j] >= 0:
                lang_vec[i][j] = 1
            else:
                lang_vec[i][j] = -1
# predicts based on crossing with prefixes then dotting with each letter
# lvl_n where n is len(prefix)+1
#multiply Lv234 with r(O + OO + FOO)
def predict2(lvl_n, pref):
    v = ""
    prefix = np.zeros((1, 10000))
    pref_reversed = pref[::-1];
    for i in pref_reversed:
        v = i+v
        p = random_idx.id_vector(N, v, alph, RI_letters, ordered)
        prefix = np.add(p,prefix)


    sprefix = np.roll(prefix, 1);
    t = np.multiply(lvl_n, sprefix)

    q = Queue.PriorityQueue()

    for i in range(26):
        result = np.dot(t, RI_letters[i])
        q.put((-result, result, len(pref)+1, pref, alph[i]))

    return q


#returns a priority queue of most likely letter after prefix
def predict(pref, length, lang_vec):
    ngram = lang_vec
    clamp_to_binary(ngram, 0)
    #clamp(ngram, -27, 27)
    #clamp(ngram, -10, 10)
    prefix = random_idx.id_vector(N, word[0:length], alph, RI_letters, ordered)
    sprefix = np.roll(prefix, 1)
    prefix_ngram = np.multiply(ngram, sprefix)
    #print prefix_ngram

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
    #f = open("letter_prediction_results_added.txt", "w")
    #f = open("letter_prediction_results_clipped_binary.txt", "w")
    #f = open("letter_prediction_results_w_alphabet_clipped.txt", "w")
    f = open("../output/letter_prediction_results_predict2.txt", "w")
    for word in search_words:
        for i in range(0, len(word)-1):
            #queue = predict(word[0:i+1], i+1, lang_vectors[i+1])
            # queue = predict(word[0:i+1], i+1, added_lvls[i+1])
            queue = predict2(added_lvls[i+1], word[0:i+1]);
            while not queue.empty():
                tpl = queue.get()
                f.write("dot product of %d-gram*s%s vector and %s letter vector is %d\n\n" % (tpl[2], tpl[3], tpl[4], tpl[1]))
    
    f.close()



#tried clamping only the language vector. results less accurate
#tried clamping RI_letters as well








