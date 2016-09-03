import numpy as np
import string
import collections
import pickle
from ..utils import random_idx
from ..utils import log_random_idx
from ..utils import log_lang_vectors as llv

"""
This is an exercise to calculate the standard deviation as post processing for the
language vectors. For now, you cannot calculate a running variance because of the 
result of "explaining away" nearly every word you encounter.

Reference for running variance:
http://www.johndcook.com/blog/standard_deviation/
"""
alphabet = string.lowercase+" "
#filepath = "preprocessed_texts/AliceInWonderland.txt"

k = 5000
N = 30000;
ordered = 1

cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
def load_all(filepath="../preprocessed_texts/AliceInWonderland.txt"):
	fread = open("../intermediate/lv", "r")
	fread1 = open("../intermediate/log_lang_vectors", "r")
	fwrite2 = open("../intermediate/n_gram_frequencies", "r")
	lv = pickle.load(fread)
	lang_vectors = pickle.load(fread1)
	n_gram_frequencies = pickle.load(fread2)
	fread.close()
	fread1.close()
	fread2.close()
	return lv, lang_vectors, n_gram_frequencies
"""
Subtracts the s vector from lang vector log wise
"""
def subtract(lang_vec, s):
	s_vec = llv.get_letter_vec(s, lang_vec)
	freq = np.dot(lang_vec, s_vec)
	for i in range(0,freq):
		lang_vec -= np.log2(i+1)*s_vec

"""
Picks out n-grams of size c with > 1 std frequency and subtracts them
from the language vector. Saves these n-grams as vocab
"""
def filter(lang_vec, n_gram_frequencies):
	arr = np.array([v for k,v in n_gram_frequencies.items()])
	std = np.std(arr)
	mean = np.mean(arr)
	cutoff = mean + std
	vocab = []
	for k, v in n_gram_frequencies.items():
		if v > cutoff:
			vocab.append(k)
			subtract(lang_vec, k)
			n_gram_frequencies.remove(k)
	return vocab

def explain_away(filepath="../preprocessed_texts/AliceInWonderland.txt"):
	lv, lang_vectors, n_gram_frequencies = load_all(filepath)
	max_cluster_size = len(lang_vectors)
	#empty inner array is for cluster size 0
	vocab = [[]]
	for c in range(0,max_cluster_size):
		vocab.append(filter(lang_vectors[c], n_gram_frequencies[c], lv))
	return lang_vectors, n_gram_frequencies, vocab















