import numpy as np
import string
import collections
import pickle
from ..utils import random_idx
from ..utils import log_random_idx
from ..utils import log_lang_vectors as ll

#arbitrarily setting divisions up to unigrams
divisions = 254
num_partitions = 2**divisions
partition_window = 30
alphabet = string.lowercase+" "
filepath = "../preprocessed_texts/alice-only-stream.txt"
k = 5000
N = 30000;
ordered = 1
#need to repopulate lang_vectors
cluster_sizes = [1, 2, 3, 4, 5]#, 6, 7, 8, 9, 10]
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

# start with freqs of entire text
# denominator is the same
def initialize_freqs(text, cluster_sizes):
	freq = {}
	length = len(text)
	for c in cluster_sizes:
		# print "on cluster %d" % c
		for i in range(0,length):
			# are we only considering left to right?
			ic = min(i+c,length)
			substring = text[i:ic]
			# print substring
			if substring not in freq.keys():
				freq[substring] = 1
			else:
				freq[substring] += 1
	return freq
#assign an arbitary break in the middle
#use that to partition the left and right
#subtract right frequencies from left frequencies to get left_freq
#right_freq is the complement
# assumption that partition window smaller than text
# using global frequencies
# take max instead for patterns not crossing the boundary
def update_freqs(text, partition_window, freqs, cluster_sizes):
	right_freq = {}
	length = len(text)
	mid = len(text)//2
	#find the split
	min_freq = float("inf")
	split_index = mid
	for i in range(mid-(partition_window//2), mid+(partition_window//2)):
		freq = 1
		for c in cluster_sizes:
			ic = min(i+c,length)
			freq *= freqs[text[i:i+c]]
		if freq < min_freq:
			min_freq = freq
			split_index = i
	left_part = text[:split_index]
	right_part = text[split_index:]
	# assign frequencies for left half
	left_freq = initialize_freqs(left_part, cluster_sizes)
	# assign frequencies for right half
	right_freq = initialize_freqs(right_part, cluster_sizes)
	return left_freq, right_freq, left_part, right_part, split_index


def dp_solution(text, divisions=divisions):
	dictionary = []
	# includes indices of all the spaces for easier comparison
	spaces_indices = []
	# update freqs as you build up alice. right now, don't include spaces
	# array of dictionaries where dictionary index corresponds to partition index
	# left, right order
	# empty dict first
	freqs = [initialize_freqs(text, cluster_sizes)]
	# print freqs
	file = open("../output/spaced_out", "w")
	partition_text = [text]
	for i in range(0,divisions):
		print "division %d" % i
		freq = freqs.pop(0)
		part = partition_text.pop(0)
		left_freq, right_freq, left_part, right_part, split_index = \
		update_freqs(part, partition_window, 
			freq, cluster_sizes)
		print "LEFT: " + left_part
		file.write("LEFT: " + left_part + "\n")
		print "RIGHT: " + right_part
		file.write("RIGHT: " + right_part + "\n")
		freqs.append(left_freq)
		freqs.append(right_freq)
		dictionary.append(left_part)
		dictionary.append(right_part)
		partition_text.append(left_part)
		partition_text.append(right_part)
		spaces_indices.append(split_index)
	file.close()
	return dictionary, spaces_indices
# dictionary, spaces_indices = dp_solution(text,divisions)
# spaces_indices = sorted(spaces_indices)
#file = open("spaced_out", "w")
#for i in range(0,len(text)):
#	if i in spaces_indices:
#		file.write("%s " % text[i])
#	else:
#		file.write(text[i])
#file.close()


#create an orthonormal set

def determine_words2(text, cluster_sizes, lang_vector, window_size):
	cluster_sizes = cluster_sizes[1:]
	win_start = (len(text)-partition_window)//2
	window = text[win_start:win_start+partition_window]
	first_half = ""
	second_half = ""
	w = max(cluster_sizes)
	log_counts_cum = np.zeros((w+1, window_size))
	for i in range(window_size-w+1):
		for c in cluster_sizes:
			chunk = window[i:i+c]
			n_gram = log_random_idx.id_vector(N, chunk, alphabet, lv, ordered)
			log_counts_cum[c,i] = np.dot(n_gram, lang_vector.T)
			if i > 0:
				log_counts_cum[c, i] += log_counts_cum[c, i-1]

	min_count = float("inf")
	min_index = 0
	for i in range(w, window_size-w+1):
		count = 0
		for c in cluster_sizes:
			inc = 0
			inc += 2*(log_counts_cum[c, i-1] - log_counts_cum[c, i-c])/(c-1)
			inc -= log_counts_cum[c, i] - log_counts_cum[c, i-1]
			inc -= log_counts_cum[c, i-c] - log_counts_cum[c, i-c-1]
			count += (c-1)*inc
		if count < min_count:
			min_index = i
			min_count = count
	return text[:min_index+win_start], text[min_index+win_start:]

def dp_solution2(text, divisions=divisions):
	dictionary = []
	freqs = [None]
	for c in cluster_sizes:
		freqs.append({})
	lang_vec = create_lang_vec(cluster_sizes, text, freqs, N=N, k=k)

	file = open("../output/spaced_out2.txt", "w")
	partition_text = [text]
	for i in range(0,divisions):
		print "division %d" % i
		part = partition_text.pop(0)
		left_part, right_part = determine_words2(part, cluster_sizes, lang_vec, \
			partition_window)
		print "LEFT: " + left_part
		file.write("LEFT: " + left_part + "\n")
		print "RIGHT: " + right_part
		file.write("RIGHT: " + right_part + "\n")
		dictionary.append(left_part)
		dictionary.append(right_part)
		partition_text.append(left_part)
		partition_text.append(right_part)
	file.close()
	return dictionary

dp_solution2(text, divisions)