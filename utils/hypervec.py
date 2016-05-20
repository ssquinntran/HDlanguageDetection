import string
import random_idx
import numpy as np

"""
Converts a text file into individual words, splitting
on puncuation, whitespaces, and so on. Everything is lower case
"""
def create_wordlist(textfile):
    fdict = open(textfile)
    text = fdict.read().lower()

    punct = string.punctuation

    for i in punct:
        text = text.replace(i, ' ');

        
    word_list = set(text.strip().split()[1:]);
    return word_list;

"""
Generates a letter vector (aka RI_letters) with the alphabet
and encoded by a N-dimensional vector
"""
def create_letter_vector(alphabet, N):
    """ """
    letter_vectors = np.zeros((len(alphabet), N))

    for i,let in enumerate(alphabet):
        r = 2 * (np.random.randn(N) > 0.5) - 1
        letter_vectors[i,:] = r
    return letter_vectors


# def substring_dictionary(word_list, letter_vectors):
#     N = letter_vectors.shape[1];
#     hyperdictionary = np.zeros(N)
#     count = 0
#     vals = []
#     subwords = []
#     skip = 100

#     for word in word_list:
#     #for word in ['accelerate','aardvark', 'accordion', 'accordionists',  'apple', 'betazoid', 'betakeratine']:
#     #for word in ['a', 'b', 'c', 'd','e', 'f']:
#         #print ""
#         print(word);
#         subword = ''
#         subvec = np.ones(N)
#         for i,letter in enumerate(word):
#             letter_idx = random_idx.alphabet.find(letter)
#             subvec = np.roll(subvec, 1) * letter_vectors[letter_idx,:]
#             subword += letter
            
#             # check to see if the subvec is already present in the hyperdictionary
#             val = np.dot(subvec.T, hyperdictionary) / N
#             #vals.append(val)
#             #subwords.append(subword)
            
#             # If the substring is not present, then val should be near 0
#             if val < 0.5:
#                 # then add the substring
#                 hyperdictionary += subvec
#                 count += 1
#                 #print subword, 
#     return hyperdictionary

def substring_dictionary(word_list, letter_vectors, N):
    hyperdictionary = np.zeros(N)
    count = 0
    vals = []
    subwords = []

    for word in word_list:
        subword = ''
        subvec = np.ones(N)
        print word
        for i,letter in enumerate(word):
            letter_idx = random_idx.alphabet.find(letter)
            subvec = np.roll(subvec, 1) * letter_vectors[letter_idx,:]
            subword += letter           
            # check to see if the subvec is already present in the hyperdictionary
            val = np.dot(subvec.T, hyperdictionary) / N
            #vals.append(val)
            #subwords.append(subword)
                
            # If the substring is not present, then val should be near 0
            if val < 0.5:
                # then add the substring
                hyperdictionary += subvec
                count += 1
        letter_idx = random_idx.alphabet.find(' ')
        subvec = np.roll(subvec, 1) * letter_vectors[letter_idx,:]
        subword += letter           
        # check to see if the subvec is already present in the hyperdictionary
        val = np.dot(subvec.T, hyperdictionary) / N
        #vals.append(val)
        #subwords.append(subword)
            
        # If the substring is not present, then val should be near 0
        if val < 0.5:
            # then add the substring
            hyperdictionary += subvec
            count += 1


    return hyperdictionary
        
def word_dictionary(word_list, letter_vectors):
    N = letter_vectors.shape[1]
    hyperdictionary = np.zeros(N)
    count = 0
    vals = []
    subwords = []
    skip = 100

    for word in word_list:
    #for word in ['accelerate','aardvark', 'accordion', 'accordionists',  'apple', 'betazoid', 'betakeratine']:
    #for word in ['a', 'b', 'c', 'd','e', 'f']:
        #print ""
        subword = ''
        subvec = np.ones(N)
        for i,letter in enumerate(word):
            letter_idx = random_idx.alphabet.find(letter)
            subvec = np.roll(subvec, 1) * letter_vectors[letter_idx,:]
            subword += letter
            
        # check to see if the subvec is already present in the hyperdictionary
        val = np.dot(subvec.T, hyperdictionary) / N
        #vals.append(val)
        #subwords.append(subword)
        
        # If the substring is not present, then val should be near 0
        if val < 0.5:
            # then add the substring
            hyperdictionary += subvec
            count += 1
            #print subword, 

    return hyperdictionary


def preprocess_text(s):
    punct = string.punctuation
    s.lower()
    for i in punct:
        s = s.replace(i, '');

    s = s.replace(" ", "");

    return s;





