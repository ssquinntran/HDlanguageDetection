import random_idx
import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys
import Queue

k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alph = string.lowercase + ' '

# create language vector for Alice in Wonderland made of summed n-gram vectors for each
# n in cluster_sizes
def create_lang_vec(cluster_sizes, N=N, k=k):
    
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = random_idx.generate_RI_text_fast(N, RI_letters, cz, ordered, "preprocessed_texts/AliceInWonderland.txt", alph)
        total_lang += lang_vector
    return total_lang

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
def clamp(n, bitWidth):
    if bitWidth == 1:
        if n > 0:
            return 1
        else:
            return 0
    else:
        maxn = pow(2, bitWidth-1)-1
        minn = -1 * pow(2, bitWidth-1)
        return max(min(maxn, n), minn)

#returns a priority queue of most likely letter after prefix
def predict(pref, length):
    ngram = lang_vectors[length+1]
    #clamp the ngram. can clamp out of predict method
    #for n in ngram:
    #    for num in n:
    #        print n
    #        print ""
    prefix = random_idx.id_vector(N, word[0:length], alph, RI_letters, ordered)
    sprefix = np.roll(prefix, 1)
    prefix_ngram = np.multiply(ngram, sprefix)
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
    f = open("letter_prediction_results_clipped.txt", "w")
    for word in search_words:
        for i in range(0, len(word)-1):
            queue = predict(word[0:i+1], i+1)
            while not queue.empty():
                tpl = queue.get()
                f.write("dot product of %d-gram*s%s vector and %s letter vector is %d\n\n" % (tpl[2], tpl[3], tpl[4], tpl[1]))
    
    f.close()












