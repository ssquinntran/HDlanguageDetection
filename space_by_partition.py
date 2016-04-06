import numpy as np
import string
import collections
import pickle
import random_idx
import log_random_idx
import log_lang_vectors as ll

#arbitrarily setting divisions up to unigrams
divisions = 10000
partitions = 2**divisions

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
def create_lang_vec(cluster_sizes, N=N, k=k, text):
    
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = log_random_idx.log_generate_RI_text_partitioned(N, lv, cz, \
        	ordered, text, \
        	n_gram_frequencies, alphabet)
        total_lang += lang_vector
    return total_lang

#what does this even do??
postprocessed = ll.load_log_vector(filepath, lv)
partitions_lang_vecs = [[] for _ in range(len(num_divisions)+1)]
for d in range(1,num_divisions):
	for p in range( )
# lang_vectors in sizes 1-10
lang_vectors = []
for size in cluster_sizes:
    lang_vectors.append(ll.create_log_lang_vec([size],N,k))
lang_vectors.insert(0, np.zeros((1,N)))


"""

lv = pickle.load(fread)
lang_vectors = pickle.load(fread1)
n_gram_frequencies = pickle.load(fread2)
fread.close()
fread1.close()
fread2.close()
alphabet = string.lowercase+" "
filepath = "preprocessed_texts/AliceInWonderland.txt"
k = 5000
N = 30000;
ordered = 1
#need to repopulate lang_vectors
cluster_sizes = [1, 2, 3]#, 4]#, 5, 6#, 7, 8] #, 9, 10]

#lv = random_idx.generate_letter_id_vectors(N,15000);
f = open(filepath, "r");
text = f.read();
text = ''.join([x for x in text if x in alphabet])[0:10000];
#for each n, dictionary of key: n gram and value: frequency
#n_gram_frequencies = [{} for _ in range(len(cluster_sizes) + 1)]
#dictionary has to account for partitions as well. 
#need to encode conditional probabilities as well as absolute probabilities
#partitions = 2^number of divisions
#haven't defined base case yet
#not yet encoded optimizations
def populate_dictionary(partitions, text, cluster_sizes, lang_vectors):
	# use memoization to update frequencies of every type of substring
	length = len(text)
	num_divisions = np.log2(partitions)
	#print "length of text is %d" % (length)
	#+1 may be off by one
	#each division has first half, second half as partitions
	partition_dictionary = [[{},{}] for _ in range(len(num_divisions))]
	for d in range(0,num_divisions):
		for p in range(0,2):
			length = len(text)//pow(2,d)
			for c in cluster_sizes:
				for i in range(0,len(text[]),c):
					if i+c < length:
						substring = text[i:i+c]
						
						if substring not in dictionary.keys():
							#print substring
							partition_dictionary[d][p][substring] = 
							np.dot(random_idx.id_vector(N, substring, alphabet, lv, ordered),
								np.transpose(lang_vectors[c]))
					# handle edge case of end of stream
					else:
						substring = text[i:length]
						if substring not in dictionary.keys():
							partition_dictionary[d][p][substring] = np.dot(random_idx.id_vector(N, substring, alphabet, lv, ordered),
								np.transpose(lang_vectors[length-i]))
	return partition_dictionary


def determine_words(text, cluster_sizes, lang_vectors):
	length_partition = len(text)
	partitions = [text]
	words = []
	# find the weight for each word pattern. assume overlap
	# min = min weight of 1*2*3...*10 ngram
	# while there are still partitions to process
	while partitions:
		partition = partitions[0]

		partitions = partitions[1:]



postprocessed = ll.load_log_vector(filepath, lv)
print postprocessed
print len(lang_vectors)
dictionary = populate_dictionary(text, cluster_sizes, lang_vectors)
print dictionary


# save vectors to file
#fwrite = open("lv", "w")
#fwrite1 = open("log_lang_vectors", "w")
#fwrite2 = open("n_gram_frequencies", "w")
#pickle.dump(lv, fwrite)
#pickle.dump(lang_vectors, fwrite1)
#pickle.dump(n_gram_frequencies, fwrite2)
#fwrite.close()
#fwrite1.close()
#fwrite2.close()
"""
