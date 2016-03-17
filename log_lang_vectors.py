import numpy as np
import string
import collections
import random_idx

alphabet = string.lowercase+" "
filepath = "preprocessed_texts/AliceInWonderland.txt"
N = 30000;
lv = random_idx.generate_letter_id_vectors(N,15000);
f = open(filepath, "r");
text = f.read();
text = ''.join([x for x in text if x in alphabet])[0:10000];

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

	return total;

def get_letter_vec(s, letter_vec):
	if(len(s) == 1):
		return letter_vec[alphabet.index(s)];
	vec = letter_vec[alphabet.index(s[0])];
	for i in s[1:]:
		vec = np.multiply(np.roll(vec, 1), letter_vec[alphabet.index(i)]);
	return vec;

postprocessed = load_log_vector(filepath, lv)

print postprocessed

def recover_frequency(letter_vec, s, total):
	vec = get_letter_vec(s, letter_vec);
	return np.dot(vec, total);

print ("s")
print recover_frequency(lv, "s", postprocessed)
print text.count("s");
print("a")
print recover_frequency(lv, "a", postprocessed)
print text.count("a")


