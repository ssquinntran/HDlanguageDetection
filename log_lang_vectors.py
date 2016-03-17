import numpy as np
import string
import collections
import random_idx
import log_random_idx

alphabet = string.lowercase+" "
filepath = "preprocessed_texts/AliceInWonderland.txt"
k = 5000
N = 30000;
ordered = 1

cluster_sizes = [1, 2, 3, 4, 5]
n_grams = []
lv = random_idx.generate_letter_id_vectors(N,15000);
f = open(filepath, "r");
text = f.read();
text = ''.join([x for x in text if x in alphabet])[0:10000];
#for each n, dictionary of key: n gram and value: frequency
n_gram_frequencies = [{} for _ in range(len(cluster_sizes) + 1)]
# create language vector for Alice in Wonderland made of summed n-gram vectors for each
# n in cluster_sizes
def create_log_lang_vec(cluster_sizes, N=N, k=k):
    
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = log_random_idx.log_generate_RI_text(N, lv, cz, \
        	ordered, "preprocessed_texts/AliceInWonderland.txt", \
        	n_gram_frequencies, alphabet)
        total_lang += lang_vector
    return total_lang

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
		#total += 1/float(recover_frequency(letter_vec, k, ))*get_letter_vec(k, letter_vec)

	return total;

def get_letter_vec(s, letter_vec):
	if(len(s) == 1):
		return letter_vec[alphabet.index(s)];
	vec = letter_vec[alphabet.index(s[0])];
	for i in s[1:]:
		vec = np.multiply(np.roll(vec, 1), letter_vec[alphabet.index(i)]);
	return vec;

def recover_frequency(letter_vec, s, total):
	vec = get_letter_vec(s, letter_vec);
	return np.dot(vec, total);
#right now, determine if a specific position in the window (in big picture, the text)
#should include a space. frequency of the n grams should be small
#how to determine if a sequence is particularly weak:
"""
My idea for a "particularly weak" link is that the first and
the last trigrams in that window are much more frequent than
the middle trigrams that cress the boundary.  For example,
if ABCDEF is in the window, it should turn into ABC_DEF if
ABC and DEF are frequent and BCD and CDE are infrequent.
Just add the end frequencies and subtract the middle
frequencies and compare the result to a threshold.

The threshold should be a parameter that is a simple
function of the frequencies.  Then see if you can find
thresholds that insert spaces in Alice stream that are, say,
.90 correct, .95 correct, and .99 correct.  Ignore missing
spaces--there will be plenty--count only misplaced spaces.
No need to write a program to do the checking--just eye-ball
to see how well we can do with trigrams and how it responds
to parameter setting.
"""
def determine_space(text, window_size, n_gram_frequencies):
	text_size = len(text)
	total_freq = sum(n_gram_frequencies[3].values())
	space_indices = []
	#choosing an arbitary threshold right now
	
	for i in range(0, text_size, window_size):
		window = text[i:window_size]
		first_freq = n_gram_frequencies[3][window[:3]]
		last_freq = n_gram_frequencies[3][window[3:]]
		threshold = (first_freq + last_freq)/float(3)
		min_index = 0
		min_freq = float('inf')
		for j in range(window_size):
			trigram_s = window[j:j+3]
			freq = n_gram_frequencies[3][trigram_s]
			if freq < min_freq:
				min_index = j #i+j in text
				min_freq = freq
		#insert space
		if min_freq < threshold:
			space_indices.append(i+min_index)
	
	#edge case. laterrrrr
	#for i in range(window_size*(text_size//window_size), text_size):
	return space_indices

postprocessed = load_log_vector(filepath, lv)
print postprocessed

print ("s")
print recover_frequency(lv, "s", postprocessed)
print text.count("s");
print("a")
print recover_frequency(lv, "a", postprocessed)
print text.count("a")

# lang_vectors in sizes 1-8
lang_vectors = []
for size in cluster_sizes:
    lang_vectors.append(create_log_lang_vec([size]))
lang_vectors.insert(0, np.zeros((1,N)))

print lang_vectors

#for vec in lang_vectors:
#	print vec
print determine_space(text, 6, n_gram_frequencies)

"""
ERROR
Traceback (most recent call last):
  File "log_lang_vectors.py", line 134, in <module>
    print determine_space(text, 6, n_gram_frequencies)
  File "log_lang_vectors.py", line 102, in determine_space
    freq = n_gram_frequencies[3][trigram_s]
KeyError: 'ec'
"""
