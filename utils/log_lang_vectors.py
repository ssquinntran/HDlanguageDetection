import numpy as np
import string
import collections
import pickle
import random_idx
import log_random_idx

#HOW TO LOAD A LOG VECTOR
#postprocessed = load_log_vector(filepath, lv)
#print postprocessed

alphabet = string.lowercase+" "
#filepath = "preprocessed_texts/AliceInWonderland.txt"

k = 5000
N = 30000;
ordered = 1

cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# create language vector for Alice in Wonderland made of summed n-gram vectors for each
# n in cluster_sizes
def create_log_lang_vec(filepath, cluster_sizes, N=N, k=k):
    
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = log_random_idx.log_generate_RI_text(N, lv, cz, \
        	ordered, filepath, n_gram_frequencies, alphabet)
        total_lang += lang_vector
    return total_lang

# Creates the load log vector for specified ngrams
def load_log_vector(s,letter_vec, ngram_length):
	temp = "";
	ngrams = collections.defaultdict(int);
	for i in s:
		temp = temp+i;
		if len(temp) < ngram_length+1:
			continue;
		temp = temp[1:]
		ngrams[temp] = ngrams[temp] + 1;

	total = np.zeros(N);
	for k,v in ngrams.items():
		total += np.log2(v+1)*get_letter_vec(k, letter_vec)

	return total;

def load_ngram_vector(t,letter_vec,n):
	x = [];
	for i in range(n):
		x.append(load_log_vector(t, letter_vec,i+1));

	return x;

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

def initialize(filepath="../preprocessed_texts/AliceInWonderland.txt"):
	n_grams = []
	lv = random_idx.generate_letter_id_vectors(N,15000);
	f = open(filepath, "r");
	text = f.read();
	text = ''.join([x for x in text if x in alphabet])[0:10000];
	#for each n, dictionary of key: n gram and value: frequency
	n_gram_frequencies = [{} for _ in range(len(cluster_sizes) + 1)]

	# lang_vectors in sizes 1-8
	lang_vectors = []
	for size in cluster_sizes:
	    lang_vectors.append(create_log_lang_vec(filepath,[size]))
	lang_vectors.insert(0, np.zeros((1,N)))

	# save vectors to file
	fwrite = open("../intermediate/lv", "w")
	fwrite1 = open("../intermediate/log_lang_vectors", "w")
	fwrite2 = open("../intermediate/n_gram_frequencies", "w")
	pickle.dump(lv, fwrite)
	pickle.dump(lang_vectors, fwrite1)
	pickle.dump(n_gram_frequencies, fwrite2)
	fwrite.close()
	fwrite1.close()
	fwrite2.close()

def training_set(filepath="../preprocessed_texts/alice-only-spaced.txt"):
	n_grams = []
	lv = random_idx.generate_letter_id_vectors(N,15000);
	f = open(filepath, "r");
	text = f.read();
	text = ''.join([x for x in text if x in alphabet])[0:10000];
	#for each n, dictionary of key: n gram and value: frequency
	n_gram_frequencies = [{} for _ in range(len(cluster_sizes) + 1)]

	# lang_vectors in sizes 1-8
	lang_vectors = []
	for size in cluster_sizes:
	    lang_vectors.append(create_log_lang_vec(filepath,[size]))
	lang_vectors.insert(0, np.zeros((1,N)))

	# save vectors to file
	fwrite = open("../intermediate/train_lv", "w")
	fwrite1 = open("../intermediate/train_log_lang_vectors", "w")
	fwrite2 = open("../intermediate/train_n_gram_frequencies", "w")
	pickle.dump(lv, fwrite)
	pickle.dump(lang_vectors, fwrite1)
	pickle.dump(n_gram_frequencies, fwrite2)
	fwrite.close()
	fwrite1.close()
	fwrite2.close()


