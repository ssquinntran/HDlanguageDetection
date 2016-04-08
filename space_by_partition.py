import numpy as np
import string
import collections
import pickle
import random_idx
import log_random_idx
import log_lang_vectors as ll

#arbitrarily setting divisions up to unigrams
divisions = 2
num_partitions = 2**divisions

alphabet = string.lowercase+" "
filepath = "preprocessed_texts/AliceInWonderland.txt"
k = 5000
N = 30000;
ordered = 1
#need to repopulate lang_vectors
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lv = random_idx.generate_letter_id_vectors(N,15000);
f = open(filepath, "r");
text = f.read();
text = ''.join([x for x in text if x in alphabet])[0:10000];

# create language vector for Alice in Wonderland made of summed n-gram vectors for each
# n in cluster_sizes
# have to create lang_vecs for every partition 
# because at every division you're removing a set of n grams
def create_lang_vec(cluster_sizes, text, n_gram_frequencies, N=N, k=k):
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = log_random_idx.log_generate_RI_text_partitioned(N, lv, cz, \
        	ordered, text, n_gram_frequencies, alphabet)
        total_lang += lang_vector
    return total_lang
# window = largest n_gram
def determine_words(text, cluster_sizes, lang_vectors, window_size):
	length = len(text)
	first_half = ""
	second_half = ""
	# find the weight for each word pattern. assume overlap
	# min = min weight of 1*2*3...*10 ngram
	# set by window
	# because denominators are the same across substrings, only have to compare numerators
	min_freq = float("inf")
	min_index = 0
	for i in range(0,(length//window_size)*window_size):
		window = text[i:i+window_size]
		#print window
		freq = 1
		for c in cluster_sizes:
			# just check beginning because the way 
			# windowing works already conditions on checking every possible
			# position for a space
			n_gram  = log_random_idx.id_vector(N, window[:c], alphabet, lv, ordered)
			# to calculate joint probability
			# assuming independence across n grams in this window. sounds sketch
			freq *= np.dot(n_gram, np.transpose(lang_vectors[c]))
		if freq < min_freq:
			min_index = i
			min_freq = freq
	return text[:min_index], text[min_index:]

#what does this even do??
postprocessed = ll.load_log_vector(filepath, lv)
# right now dictionary has all the partitions -> at some point = words

def naive_solution():
	dictionary = []
	partition_text = [text]
	# may be off by one
	# partition as you create lang_vecs
	for d in range(0,divisions):
		string = partition_text.pop(0)
		# joy division lang vecs haha
		nth_division_lang_vecs = []
		# dictionary with key: cluster_size value: dictionary
		# where dictionary with key: n_gram value: frequency
		n_gram_frequencies = {}
		for size in cluster_sizes:
			n_gram_frequencies[size] = {}
			nth_division_lang_vecs.append(create_lang_vec([size],string, \
				n_gram_frequencies, N,k))
		nth_division_lang_vecs.insert(0, np.zeros((1,N)))
		first_half, second_half = determine_words(string, cluster_sizes, \
			nth_division_lang_vecs, max(cluster_sizes))
		dictionary.append(string)
		partition_text.append(first_half)
		partition_text.append(second_half)
		print "finished division %d" % d
	file = open("dictionary", "w")
	for word in dictionary:
		file.write(word + "\n")
	file.close()
	
def update_freqs_and_words(freqs, text, cluster_sizes, window_size):
	length = len(text)
	first_half = ""
	second_half = ""
	# find the weight for each word pattern. assume overlap
	# min = min weight of 1*2*3...*10 ngram
	# set by window
	# because denominators are the same across substrings, only have to compare numerators
	min_freq = float("inf")
	min_index = 0
	for i in range(0,(length//window_size)*window_size):
		window = text[i:i+window_size]
		#print window
		freq = 1
		for c in cluster_sizes:
			# just check beginning because the way 
			# windowing works already conditions on checking every possible
			# position for a space
			n_gram  = log_random_idx.id_vector(N, window[:c], alphabet, lv, ordered)
			# to calculate joint probability
			# assuming independence across n grams in this window. sounds sketch
			freq *= np.dot(n_gram, np.transpose(lang_vectors[c]))
		if freq < min_freq:
			min_index = i
			min_freq = freq
	return text[:min_index], text[min_index:]

def dp_solution():
	dictionary = []
	freqs = []
	partition_text = [s for s in text]
	while partition_text:
		first_part = partition_text.pop(0)
		second_part = partition_text.pop(0)
		if first_part in freqs.keys():
			freqs[first_part] += 1
		else:
			freqs[first_part] = 1
		if second_part in freqs.keys():
			freqs[second_part] += 1
		else:
			freqs[second_part] = 1
		# need to choose to insert spaces or just concatenate
		word = update_freqs_and_words(freqs, part, cluster_sizes, max(cluster_sizes))
		dictionary.append(word)
		partition_text.append(word)
