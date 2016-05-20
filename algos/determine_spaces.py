import numpy as np
import string
import collections
import pickle
from ..utils import random_idx
from ..utils import log_random_idx

#read from serialized files
fread = open("../intermediate/lv", "r")
fread1 = open("../intermediate/log_lang_vectors", "r")
fread2 = open("../intermediate/n_gram_frequencies", "r")
lv = pickle.load(fread)
lang_vectors = pickle.load(fread1)
n_gram_frequencies = pickle.load(fread2)
fread.close()
fread1.close()
fread2.close()
alphabet = string.lowercase+" "
filepath = "../preprocessed_texts/AliceInWonderland.txt"
k = 5000
N = 30000;
ordered = 1

cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
n_grams = []
#lv = random_idx.generate_letter_id_vectors(N,15000);
f = open(filepath, "r");
text = f.read();
text = ''.join([x for x in text if x in alphabet])[0:10000];
#for each n, dictionary of key: n gram and value: frequency
#n_gram_frequencies = [{} for _ in range(len(cluster_sizes) + 1)]

def load_log_vector(filepath,letter_vec):
	temp = "";
	ngrams = collections.defaultdict(int);
	for i in text:
		temp = temp+i;
		if len(temp) < 2:
			continue;
		temp = temp[1:]
		ngrams[temp] = ngrams[temp] + 1;

	total = np.zeros(N);
	for k,v in ngrams.items():
		total += np.log2(v+1)*get_letter_vec(k, letter_vec)
		print k
		print v
		

	return total;

def determine_space(text, window_size, n_gram_frequencies):
	text_size = len(text)
	total_freq = sum(n_gram_frequencies[3].values())
	space_indices = []
	#choosing an arbitary threshold right now
	#threshold = .001
	#print text
	fwrite = open("../preprocessed_texts/alice_with_spaces.txt", "w")
	for i in range(0,(text_size//window_size)*window_size,window_size):
		window = text[i:i+window_size]
		#print window
		min_index = 0
		min_freq = float('inf')
		threshold = (n_gram_frequencies[3][window[:3]] + \
		n_gram_frequencies[3][window[window_size-3:window_size]]) / float(total_freq)
		#threshold = (n_gram_frequencies[3][window[:3]] + \
		#n_gram_frequencies[3][window[window_size-3:window_size]])/float(2)
		for j in range(window_size):
			trigram_s = window[j:j+3]
			#print trigram_s
			#this check shouldn't be necessary though
			if trigram_s in n_gram_frequencies[3].keys():
				#print "%s is in n_gram_frequencies" % (trigram_s)
				freq = n_gram_frequencies[3][trigram_s]/float(total_freq)
				#freq = n_gram_frequencies[3][trigram_s]
				if freq < min_freq:
					min_index = j #i+j in text
					min_freq = freq
		#insert space
		if min_freq < threshold:
			space_indices.append(i+min_index)
			fwrite.write(window[0:min_index+1] + " " + window[min_index+1:])
			fwrite.write("\n")
	
	#edge case. laterrrrr
	#for i in range(window_size*(text_size//window_size), text_size):
	fwrite.close()
	return space_indices

postprocessed = load_log_vector(filepath, lv)
print postprocessed


spaces = determine_space(text, 8, n_gram_frequencies)
print "length of alice %d" % (len(text))
print "length of alice with spaces %d" %(len(text) + len(spaces))
