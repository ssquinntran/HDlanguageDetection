# corpus_test.py
# experiment to test language identification on fixed corpus

# libraries
from ..utils import random_idx
from ..utils import utils
import sys
import scipy.io as scio
import numpy as np
import glob
import os
from tqdm import trange
from ..utils import text_cleaner
import codecs
import locale

# important directories
main_base = os.getcwd()
test_dir = '../lang_texts/test/processed_test'

# parameters
Ns = [10000] # dimension of random index vectors
ks = [0.5] # number of + (or -)
cluster_min = 4
cluster_max = 4 # size of max letter cluster
ordy = [1]
lang_map = {'af':'afr','bg':'bul','cs':'ces','da':'dan','nl':'nld','de':'deu','en':'eng','et':'est','fi':'fin','fr':'fra','el':'ell','hu':'hun','it':'ita','lv':'lav','lt':'lit','pl':'pol','pt':'por','ro':'ron','sk':'slk','sl':'slv','es':'spa','sv':'swe'}
#lang_map = {'af':'afrikaans','bg':'bulgarian','cs':'czech','da':'danish','nl':'dutch','de':'german','en':'english','et':'estonian','fi':'finnish','fr':'french','el':'greek','hu':'hungarian','it':'italian','pl':'polish','pt':'portuguese','ro':'romanian','sk':'slovak','sl':'slovenian','es':'spanish','sv':'swedish'}
languages = lang_map.values()[1:2]
languages.append('nob')
#languages = ['french','italian','finnish','estonian']



for N in Ns:
	for kk in ks:
		k = int(N * kk)
		###############################
		# generate random indexing for letters, reused throughout
		cluster_sizes = xrange(cluster_min,cluster_max+1)
		RI_letters = random_idx.generate_letter_id_vectors(N,k)

		
		##############################
		# iterate over cluster sizes for language vectors ONLY
		for ordered in ordy:
			
				if ordered == 0:
						ord_str = 'unordered'
				else:
						ord_str = 'ordered'
			
				print "N =", N, ", k =", k, ", ", ord_str
				for cluster_sz in cluster_sizes:
							
							##print "~~~~~~~~~~"
							total_vectors = []
							# calculate language vectors
							lang_vectors = random_idx.generate_RI_lang(N, RI_letters, cluster_sz, ordered, languages=languages)
							#lang_vectors = random_idx.generate_RI_lang_words(N, RI_letters, languages=languages)
							total_vectors.append(lang_vectors)

							# print cosine angles 
							#print '=========='
							

						#	print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster_sz) + ', ' + ord_str + '\n'
							cosangles = utils.cosangles(lang_vectors, languages)
							variance = utils.var_measure(cosangles)
							#print "variance of language values: " + str(utils.var_measure(cosangles))
							final_lang = sum(total_vectors)

							###############################
							# iterate through test files and calculate correctness
							print "Now waiting for input"
							while True:
								sentence = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
								unknown_tots = []
								sentence = text_cleaner.cleaner(sentence)
								unknown_vector = random_idx.generate_RI_sentence(N, RI_letters, cluster_sz, ordered,sentence)
								unknown_tots.append(unknown_vector)
								final_unknown = sum(unknown_tots)
								likely_lang = utils.find_language(sentence, final_unknown, final_lang, languages,display=0)
								print "likely language:", likely_lang
							
