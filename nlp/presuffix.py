import numpy as np 
import string
import collections
from ..utils import random_idx
from ..utils import log_lang_vectors as llv

alphabet = string.lowercase+' ~'
N = 100000
# ~ Tilde represents end character

def get_alice_space():
	#filepath = "raw_texts/texts_english/alice_in_wonderland.txt"
	filepath = "../preprocessed_texts/alice-only-spaced.txt"
	f = open(filepath, "r")
	text = f.read().lower();
	text = ''.join([x for x in text if x in alphabet])
	return text


"""
Creates an orthonormal letter vector for suffixes.
 - Takes in a 
 	string s which is the preprocessed text
    integer dim which is the dimension of vectors
    integer n which is the ngram desired
    letter_vecs lv which is the letter_vecs basis 
    	(optional, generates own if not supplied)

 Returns A total vector of suffices and a letter vector
"""
def suffix_gram(s, dim, n, lv = None):
	if type(lv) is type(None):
		lv = random_idx.generate_letter_id_vectors(dim,dim/2, alph = alphabet);
	words = s.split(' ');
	suffix = np.zeros(dim);
	for i in range(len(words)):
		padding = len(words[i])-n;
		if padding < 0:
		    words[i] = '~'+words[i]; 
		else:
			words[i] = words[i][-n:]

		svec = llv.get_letter_vec(words[i], lv);
		suffix = suffix+svec;

	return suffix, lv



"""
Creates an orthonormal letter vector including tilde.
 - Takes in a 
 	string s which is the preprocessed text
    integer dim which is the dimension of vectors
    integer n which is the ngram desired
    letter_vecs lv which is the letter_vecs basis 
    	(optional, generates own if not supplied)

 Returns A total vector of prefixes and a letter vector
"""
def prefix_gram(s, dim, n, lv = None):
	if type(lv) is type(None):
		lv = random_idx.generate_letter_id_vectors(dim,dim/2, alph = alphabet);
	words = s.split(' ');
	prefix = np.zeros(dim);
	for i in range(len(words)):
		padding = len(words[i])-n;
		if padding < 0:
		    words[i] = words[i]+'~'; 
		else:
			words[i] = words[i][:n]

		pvec = llv.get_letter_vec(words[i], lv);
		prefix = prefix+pvec;

	return prefix, lv

def recover_pref_freq(s):
	return llv.get_letter_vec(s, letter_vec).dot(ptotal)

def recover_suf_freq(s):
	return llv.get_letter_vec(s, letter_vec).dot(stotal)

"""
Tries to find a space in:
   string s with no spaces
   n uses ngram to compute (n>1)

By computing with prefix and suffix frequencies

returns a string with space

"""
def find_a_space(s, n):
	cross_values = [];
	for i in range(len(s)):
		if i == 0:
			# don't stick space in front of s
			continue
		before = s[:i]
		after = s[i:];
		if(len(before) < n):
			before = '~'+before;

		if(len(after) < n):
			after = after+'~'

		suf = before[-3:];
		pre = after[:3];

		cross_values.append(recover_pref_freq(pre)+recover_suf_freq(suf));

	location = np.argmax(cross_values)+1 #offset


	return s[:location]+' '+s[location:]




		

text = get_alice_space();
try:
	letter_vec = np.load("../intermediate/100k_presuf.p")
	ptotal = np.load("../intermediate/alice_100k_pre.p")
	stotal = np.load("../intermediate/alice_100k_suf.p");
except:
	tot = suffix_gram(text, N, 3);
	ptotal = stot[0]
	letter_vec = stot[1]
	stotal = prefix_gram(text, N, 3, letter_vec);

test = text[1000:1500];



print find_a_space("offflipped", 3);





