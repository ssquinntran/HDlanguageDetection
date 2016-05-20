import random_idx
import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt

k = 5000
cluster_sz = [3]
ordered = 1
#alph = 'abc' 
alph = string.lowercase + ' '

def gen_lets(N=N,k=k):
        # generate letter vectors
        RI_letters = random_idx.generate_letter_id_vectors(N,k)
        RI_letters_n = RI_letters/np.linalg.norm(RI_letters)
        return RI_letters, RI_letters_n

def create_english_vec(N=N,k=k, cluster_sz = [2]):
        print "generating english vector of cluster size", cluster_sz
        total_eng = np.zeros((1,N))
        # generate english vector
        for cz in cluster_sz:
                english_vector = random_idx.generate_RI_lang(N, RI_letters, cz, ordered, languages=['eng'])
        total_eng += english_vector


        normed_eng = total_eng/np.linalg.norm(total_eng)
        return total_eng, normed_eng

RI_letters, RI_letters_n = gen_lets()
english_vector, normed_eng = create_english_vec(cluster_sz=cluster_sz)

def generate_words(cluster_sz, english_vector=english_vector, normed_eng=normed_eng):
        print "generating english vector of cluster size", cluster_sz
        # generate english vector
        #english_vector = random_idx.generate_RI_text_words(N, RI_letters, './lang_texts/texts_english/eng.txt')
        # generate new string of letters
        length = 30
        alphy = utils.generate_ordered_clusters(alph, cluster_sz=cluster_sz)
        gstr = alph[np.random.randint(len(alph))]
        temp_str = gstr
        for i in xrange(length):
                max_idx = 0
                maxabs = 0
                for j in xrange(len(alphy)):
                        temp_str = gstr + alphy[j]
                        temp_id = random_idx.generate_RI_str(N,RI_letters,cluster_sz,ordered,temp_str)
                        #temp_id += 1e1*np.random.randn(1,N)
                        temp_id /= np.linalg.norm(temp_id)
                        absy = np.abs(temp_id.dot(normed_eng.T))
                        #print temp_str, absy
                        if absy > maxabs:
                                max_idx = j
                                maxabs = absy
                gstr += alphy[max_idx]
                print len(gstr), maxabs, gstr

def generate_RI_block_vectors(cz=2):
        # generate letter block values for total comparison
        RI_blocks = utils.generate_ordered_clusters(alph,cluster_sz=cz)
        #print RI_blocks
        RI_block_vectors = np.zeros((len(RI_blocks),N))
        for i in xrange(len(RI_blocks)):
            block = RI_blocks[i]
            #print block
            block_vec = random_idx.id_vector(N,block,alph, RI_letters,ordered=ordered)
            RI_block_vectors[i,:] = block_vec
        return RI_blocks, RI_block_vectors


def find_letter_partner(test_letter, english_vector=english_vector):
        # testing letter blocks for their "block partners"
        test_vec = random_idx.id_vector(N,test_letter,alph, RI_letters, ordered=ordered)
        #test_vec = test_vec/np.linalg.norm(test_vec)
        '''
        sub_eng = np.copy(english_vector)
        for r in xrange(len(blocks)):
            block = blocks[r]
            if test_letter != block[0]:
                sub_eng[:, RI_blocks[r,:] != 0] = 1e-2
        print sub_eng
        '''
        cz = len(test_letter)
        #if cz > 1:
        #    for i in xrange(len(alph)):
        #        english_vector -= RI_letters[i,:]
        #english_vector /= np.linalg.norm(english_vector)

        #factored_eng = np.multiply(english_vector, np.roll(letter, 1))
        factored_eng = np.multiply(english_vector, np.roll(test_vec, 1))
        #factored_eng = np.roll(np.multiply(english_vector, letter), -1)
        #factored_RI_letters = RI_letters, np.roll(letter,1))


        #if len(test_letter) == 1:
        likely_block_partner, values, partners = utils.find_language(test_letter, factored_eng, RI_letters, alph, display=1)
        '''else:
                #RI_blocks, RI_block_vectors = generate_RI_block_vectors(cz=cz)
                #likely_block_partner, values, partners = utils.find_language(test_letter, factored_eng, RI_block_vectors, RI_blocks, display=1)
        '''
        return likely_block_partner, values, partners


block_list = ['th']

for block in block_list:
    likely_block_partner, values, partners = find_letter_partner(block)
