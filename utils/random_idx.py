# random_idx.py
# creates random index vectors for a number of languages

# libraries
import sys
import numpy as np
import string
import utils
import pandas as pd
import os
import pickle

alphabet = string.lowercase + " "
lang_dir = 'preprocessed_texts/'

cluster_cache = {}



k = 500
N = 1000
alphabet = string.lowercase + ' '


def check_serialization(which_file):
    if which_file == 1:
        return os.path.isfile('letter_encoding.p')
    else:
        return os.path.isfile('word_dictionary.p')


def make_serialization(make_encoding=False, make_word_dict=False):
    if make_encoding:
        one_hot_encoding = generate_letter_id_vectors(N, k)
        pickle.dump(one_hot_encoding, open("letter_encoding.p", "wb"))
    if make_word_dict:
        word_dict = {}
        pickle.dump(word_dict, open("word_dictionary.p", "wb"))


def save_components(save_encoding=False, save_word_dict=False, encoding=None, dictionary=None):
    if save_encoding:
        pickle.dump(encoding, open("letter_encoding.p", "wb"))
    if save_word_dict:
        pickle.dump(dictionary, open("word_dictionary.p", "wb"))

def read_components(read_encoding):
    if read_encoding:
        if not check_serialization(1):
            return None
        return pickle.load(open("letter_encoding.p", "rb"))
    else:
        if not check_serialization(0):
            return None
        return pickle.load(open("word_dictionary.p", "rb"))

def fetch_serialized_encoding():
    if not check_serialization(1):
        print "stepping into this case"
        make_serialization(True, False)
    encoding = read_components(True)
    if not check_serialization(0):
        make_serialization(False, True)
    word_dict = read_components(False)
    return encoding, word_dict


def word_hypervec(word, alph=alphabet, N=N):
    one_hot_encoding, word_dict = fetch_serialized_encoding()
    if word in word_dict:
        return word_dict[word]
    hypervector = id_vector(N, word,alph, one_hot_encoding)
    word_dict[word] = hypervector
    save_components(save_word_dict=True, dictionary=word_dict)
    return hypervector

def stack_list(lst):
    all_words = []
    for word in lst:
        all_words.append(word_hypervec(word))
    return np.vstack(all_words)







def generate_letter_id_vectors(N, k, alph=alphabet):
    # build row-wise k-sparse random index matrix
    # each row is random index vector for letter
    num_letters = len(alphabet)
    RI_letters = np.zeros((num_letters,N))
    for i in xrange(num_letters):
            rand_idx = np.random.permutation(N)
            RI_letters[i,rand_idx[0:k]] = 1
            RI_letters[i,rand_idx[k:2*k]] = -1
    return RI_letters

# def generate_id(RI_letters,alph=alphabet,cluster_sz=1, ordered=0):
#       # generate id vectors of clusters from "alphabet" with size "cluster_sz"
#
#       # generate clusters
#       if ordered == 0:
#           clusters = utils.generate_unordered_clusters(alph,cluster_sz=cluster_sz)
#       else:
#           clusters = utils.generate_ordered_clusters(alph,cluster_sz=cluster_sz)
#
#       M = len(clusters) # number of letter clusters
#       num_letters,N = RI_letters.shape
#       #RI_letters = generate_letter_id_vectors(N, k, alphabet)
#
#       RI = np.zeros((M,N))
#       for i in xrange(M):
#               # calculate repeats
#               cluster = clusters[i]
#               RI[i,:] = id_vector(N, cluster, alphabet, RI_letters, ordered=ordered)
#       dictionary = {}
#       for i in range(len(clusters)):
#           dictionary[clusters[i]] = RI[i]
#       return dictionary

def generate_text_vector(N, RI_letters, cluster_sz, text_name):
    text_vector = np.zeros((1,N))

    text = utils.load_text(text_name)

    for char_idx in xrange(len(text)-cluster_sz+1):
        sidx = char_idx
        eidx = char_idx+cluster_sz
        
        cluster = text[sidx:eidx]
        
        vector = np.ones((1,N))
        for letter in cluster:
            letter_idx = alphabet.find(letter)
            vector = np.roll(vector, 1)
            vector = np.multiply(vector, RI_letters[letter_idx, :])
            
        text_vector += vector
    return text_vector / (len(text)-cluster_sz+1)
    
 
"""
Returns lang_vec and then vocab_vec

min-max will be a dot product value, so it
should be a multiple of 10k.
"""
def generate_vocab_lang_vectors(N, RI_letters, cluster_sz, ordered, text_name, min_, max_,alph=alphabet):
    text_vector = np.zeros((1, N))
    vocab_vec = np.zeros((1,N))
    text = utils.load_text(text_name)
    cluster = ''
    vector = np.ones((1,N))
    for char_num in xrange(len(text)):      
        cluster = cluster + text[char_num]
        if len(cluster) < cluster_sz:
            continue
        elif len(cluster) > cluster_sz:
            prev_letter = cluster[0]
            prev_letter_idx = alphabet.find(prev_letter)
            inverse = np.roll(RI_letters[prev_letter_idx,:], cluster_sz-1)
            vector = np.multiply(vector, inverse)
            vector = np.roll(vector, 1)
            letter = text[char_num]
            letter_idx = alphabet.find(letter)
            vector = np.multiply(vector, RI_letters[letter_idx,:])
            cluster = cluster[1:]
        else: # (len(cluster) == cluster_size), happens once
            letters = list(cluster)
            for letter in letters:
                vector = np.roll(vector,1)
                letter_idx = alphabet.find(letter)
                vector = np.multiply(vector, RI_letters[letter_idx,:])

        if(np.dot(vocab_vec, vector.T)<-10000):
            text_vector += vector;

        else:
            vocab_vec+= vector;
            if(np.dot(vocab_vec, vector.T) > min_):
                while(True):
                    if(np.dot(vocab_vec, vector.T)<-10000):
                        break;
                    else:
                        vocab_vec -= vector;


    return text_vector, vocab_vec

def id_vector(N, cluster, alphabet, RI_letters,ordered=0):
        if cluster == '':
                        return 0
        if ordered == 0:
                # unordered clusters
                cluster = ''.join(sorted(cluster))

#if it's already calculated, just return it
        if cluster in cluster_cache:
                return cluster_cache[cluster]
                
        vector = np.zeros(N)
        
                        
        # ordered clusters
        letters = list(cluster)
        prod = np.ones((1,N))
        roller = len(letters)-1
        for letter in letters:
                        # working code
                        #letter_idx = alphabet.find(letter)
                        #prod = np.multiply(prod, RI_letters[letter_idx,:])
                        #prod = np.roll(prod,1)
                        
                        # testing permutations
                        letter_idx = alphabet.find(letter)
                        prod = np.multiply(prod, np.roll(RI_letters[letter_idx, :],roller))
                        roller -= 1
        vector = prod

        if len(cluster_cache) > 100000:
                cluster_cache.clear()
                print "clearing cache"
        cluster_cache[cluster] = vector
        return vector

def generate_RI_str(N, RI_letters, cluster_sz, ordered, string, alph=alphabet):
        # generate RI vector for string

        text_vector = np.zeros((1,N))
        for char_num in xrange(len(string)):

                if char_num < cluster_sz:
                        continue
                else:
                        # build cluster
                        cluster = ''
                        for j in xrange(cluster_sz):
                                cluster = string[char_num - j] + cluster
                        text_vector += id_vector(N, cluster, alph,RI_letters, ordered)
        return text_vector

def generate_RI_text(N, RI_letters, cluster_sz, ordered, text_name, alph=alphabet):
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
                        print cluster
                        text_vector += id_vector(N, cluster, alph,RI_letters, ordered)
        return text_vector

def generate_RI_sentence(N, RI_letters, cluster_sz, ordered, text, alph=alphabet):
        # generate RI vector for "text_name"
        # assumes text_name has .txt

        text_vector = np.zeros((1, N))
        ##text = utils.load_text_spaces(text_name)
        for char_num in xrange(len(text)):

                if char_num < cluster_sz:
                        continue
                else:
                        # build cluster
                        cluster = ''
                        for j in xrange(cluster_sz):
                                cluster = text[char_num - j] + cluster
                        text_vector += id_vector(N, cluster, alph,RI_letters, ordered)
        return text_vector

    #Not really fast. Theoretically faster, but not for real (not using cache)  
def generate_RI_text_fast(N, RI_letters, cluster_sz, ordered, text_name, alph=alphabet):
    text_vector = np.zeros((1, N))
    text = text_name # utils.load_text(text_name)
    cluster = ''
    vector = np.ones((1,N))
    for char_num in xrange(len(text)):    
        if (char_num % 1000) == 0:
            print char_num,
            
        cluster = cluster + text[char_num]
        print cluster
        if len(cluster) < cluster_sz:
            continue
        elif len(cluster) > cluster_sz:
            prev_letter = cluster[0]
            prev_letter_idx = alphabet.find(prev_letter)
            inverse = np.roll(RI_letters[prev_letter_idx,:], cluster_sz-1)
            vector = np.multiply(vector, inverse)
            vector = np.roll(vector, 1)
            letter = text[char_num]
            letter_idx = alphabet.find(letter)
            vector = np.multiply(vector, RI_letters[letter_idx,:])
            cluster = cluster[1:]
        else: # (len(cluster) == cluster_size), happens once
            print cluster
            letters = list(cluster)
            for letter in letters:
                vector = np.roll(vector,1)
                letter_idx = alphabet.find(letter)
                vector = np.multiply(vector, RI_letters[letter_idx,:])
        text_vector += vector
    return text_vector

def generate_RI_text_words(N, RI_letters, text_name, alph=alphabet):
        # generate RI vector for "text_name"
        # assumes text_name has .txt

        text_vector = np.zeros((1, N))
        text = utils.load_text_spaces(text_name)
        cluster = ''
        for char_num in xrange(len(text)):
                char = text[char_num]
                if char == ' ':
                        text_vector += id_vector(N, cluster, alph, RI_letters)
                        # reset cluster
                        cluster = ''
                else:
                        cluster += text[char_num]
        return text_vector

def generate_RI_text_history(N, RI_letters, text_name, alph=alphabet):
        # generate RI vector for "text_name"
        # assumes text_name has .txt

        text_vector = np.zeros((1, N))
        history_vector = np.zeros((1,N))
        text = utils.load_text(text_name)
        for char_num in xrange(len(text)):
            char = text[char_num]
            letter_idx = alphabet.find(char)
            history_vector = 0.75*history_vector + RI_letters[letter_idx,:]
            text_vector += history_vector   
                
        return text_vector

def generate_RI_lang(N,RI_letters, cluster_sz, ordered, languages=None):

        cluster_cache.clear()

        if languages == None:
                languages = ['english','german','norwegian','finnish']


        num_lang = len(languages)

        lang_vectors = np.zeros((num_lang,N))

        for i in xrange(num_lang):
                # load text one at a time (to save mem), English, German, Norwegian
                print 'loading ' + languages[i]
                lang_vectors[i,:] = generate_RI_text(N, RI_letters, cluster_sz, ordered, lang_dir + languages[i] + '.txt')

        return lang_vectors


def generate_RI_lang_history(N,RI_letters, languages=None):

        cluster_cache.clear()

        if languages == None:
                languages = ['english','german','norwegian','finnish']


        num_lang = len(languages)

        lang_vectors = np.zeros((num_lang,N))

        for i in xrange(num_lang):
                print 'loading ' + languages[i]
                # load text one at a time (to save mem), English, German, Norwegian
                lang_vectors[i,:] = generate_RI_text_history(N, RI_letters, lang_dir + languages[i] + '.txt')

        return lang_vectors

def generate_RI_lang_words(N, RI_letters, languages=None):

        cluster_cache.clear()

        if languages == None:
                languages = ['english','german','norwegian','finnish']


        num_lang = len(languages)

        lang_vectors = np.zeros((num_lang,N))

        for i in xrange(num_lang):
                print 'loading ' + languages[i]
                # load text one at a time (to save mem), English, German, Norwegian
                lang_vectors[i,:] = generate_RI_text_words(N, RI_letters, lang_dir + languages[i] + '.txt')

        return lang_vectors
