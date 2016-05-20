import random_idx
import utils
import numpy as np
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys

k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alph = string.lowercase + ' '

# create language vector for Alice in Wonderland made of summed n-gram vectors for each
# n in cluster_sizes
def create_lang_vec(cluster_sizes, N=N, k=k):
    
    total_lang = np.zeros((1,N))
    # generate english vector
    for cz in cluster_sizes:
        print "generating language vector of cluster size", cz
        # which alphabet to use
        lang_vector = random_idx.generate_RI_text_fast(N, RI_letters, cz, ordered, "preprocessed_texts/AliceInWonderland.txt", alph)
        total_lang += lang_vector
    return total_lang


# RI_letters = random_idx.generate_letter_id_vectors(N, k, alph)

# # lang_vectors in sizes 1-8
# lang_vectors = []
# for size in cluster_sizes:
#     lang_vectors.append(create_lang_vec([size]))
# lang_vectors.insert(0, np.zeros((1,N)))

# # save vectors to file
# fwrite = open("alice_RI_letters", "w")
# fwrite1 = open("alice_lang_vectors", "w")
# pickle.dump(RI_letters, fwrite)
# pickle.dump(lang_vectors, fwrite1)
# fwrite.close()
# fwrite1.close()

#read from serialized files
fread = open("alice_RI_letters", "r")
fread1 = open("alice_lang_vectors", "r")
RI_letters = pickle.load(fread)
lang_vectors = pickle.load(fread1)
fread.close()
fread1.close()

up2_lang_vec = np.add(lang_vectors[1], lang_vectors[2])
up3_lang_vec = np.add(up2_lang_vec, lang_vectors[3])
qu_vector = random_idx.id_vector(N, "qu", alph, RI_letters, ordered)

#qu_vector = np.add(RI_letters[alph.find("u")], np.roll(RI_letters[alph.find("q")], 1))
if __name__ == "__main__":
    f = open("exercise_results.txt", "w")
    f.write("Take the language vector representing single letters of\n\
    Alice and compute its dot product with the 26 different\n\
    letter vectors.  Can you see a relation between the dot\n\
    products and the letter counts in Alice?  Alice has\n\
    about 300 instances of 'q'.  I'd expect a dot product\n\
    with the Q-vector to be around 3 million.\n\n")
    for i in range(26):
        result = np.dot(lang_vectors[1], RI_letters[i])
        f.write("dot product of single-letter vector and %s-vector is %d\n" % (alph[i], result))

    f.write("\nThen take the language vector representing the bigrams\n\
    of Alice and compute its dot product with QU.  What do\n\
    you get?  And what is this language vector's dot\n\
    product with Q?\n\n")

    result = np.dot(lang_vectors[2], np.transpose(qu_vector))
    f.write("dot product of bigrams vector and qu is %d\n\n" % (result))

    f.write("Next, add the two language vectors into a single vector\n\
    that represents both individual letters and bigrams.\n\
    Compute its dot product with Q and with QU.  What do\n\
    you get?\n\n")
    
    result = np.dot(up2_lang_vec, RI_letters[alph.find("q")])
    f.write("dot product of up2_lang_vec and q is %d\n" % (result)) 
    result = np.dot(up2_lang_vec, np.transpose(qu_vector))
    f.write("dot product of up2_lang_vec and qu is %d\n\n" % (result))

    f.write("One more set of tests: Take the language vector for\n\
    bigrams and (pointwise) multiply it with sQ (Q shifted\n\
    once).  Compare the resulting vector (with dot product\n\
    or cosine) to the letter vectors A, B, C, ....  Which\n\
    letter wins?  Do the same using the language vector for\n\
    individual letters, and once more using a language\n\
    vector that is the sum of the above two.\n\n")
    
    # assuming that shifting is rolling...
    sQ = np.roll(RI_letters[alph.find("q")], 1)
    bigrams_sQ = np.multiply(lang_vectors[2], sQ)
    # still need to compare to see which letter wins
    for i in range(26):
        result = np.dot(RI_letters[i], np.transpose(bigrams_sQ))
        f.write("dot product of bigrams_sQ and %s is %d\n" % (alph[i], result))

    f.write("\n");
    single_sQ = np.multiply(lang_vectors[1], sQ)
    for i in range(26):
        result = np.dot(RI_letters[i], np.transpose(single_sQ))
        f.write("dot product of single_sQ and %s is %d\n" % (alph[i], result))

    f.write("\n");
    up2_lang_vec_sQ = np.multiply(up2_lang_vec, sQ)
    for i in range(26):
        result = np.dot(RI_letters[i], np.transpose(up2_lang_vec_sQ))
        f.write("dot product of up2_lang_vec_sQ and %s is %d\n" % (alph[i], result))

    f.write("\nSo try this: make a language vector of bigrams only.\n\
    If you test it with (calculate its dot produce with)\n\
    the letter vectors, you should get numbers like those\n\
    in the second block of 'results.txt' that starts with\n\
    dot product of bigrams_sQ and a is -31528\n\
    Some are positive, some negative, and none is in the\n\
    hundreds of thousands.  All that is 'noise' in\n\
    signal-processing terms.  But if you test it with the\n\
    vector for QU (which equals sQ * U) or with any other\n\
    bigram vector, you should get that bigram's frequency\n\
    times 10K.  That's referred to as signal.\n\n")
    
    for i in range(26):
        result = np.dot(lang_vectors[2], RI_letters[i])
        f.write("dot product of bigrams vector and %s-vector is %d\n" % (alph[i], result))

    f.write("\nAfter you have gotten this far, make a language vector\n\
    that combines individual letters, bigrams and trigrams:\n\
    just add those three language vectors into a single\n\
    vector (by normal vector addition.).  Then test it for\n\
    single letters and bigrams as above.  Also, multiply it\n\
    with sQ and test the result as above.  The dot products\n\
    should be close to what you got before.\n\n")
    for i in range(26):
        result = np.dot(up3_lang_vec, RI_letters[i])
        f.write("dot product of up3_lang_vec vector and %s-vector is %d\n" % (alph[i], result))

    f.write("\n");
    result = np.dot(up3_lang_vec, np.transpose(lang_vectors[2]))
    f.write("dot product of up3_lang_vec vector and bigrams vector is %d\n" % (result))

    f.write("\n");
    up3_lang_vec_sQ = np.multiply(up3_lang_vec, sQ)
    for i in range(26):
        result = np.dot(up3_lang_vec_sQ, RI_letters[i])
        f.write("dot product of up3_lang_vec_sQ vector and %s-vector is %d\n" % (alph[i], result))

    result = np.dot(up3_lang_vec_sQ, np.transpose(lang_vectors[2]))
    f.write("\ndot product of up3_lang_vec_sQ and bigrams vector is %d\n" % (result))

    f.write("\nWhat is the dot product of the\n\
    single-letter language vector with itself?  What is the\n\
    dot product of the bigrams vector with itself?  What is\n\
    the dot product of the bigrams vector with the sum of\n\
    the the single-letter vector and the bigrams vector?\n\
    All should be around 1.2 billion, I think.\n\
    Some of the dot products with letter vectors are very\n\
    large negative (-362566580680).  You could be\n\
    multiplying vectors when you should be adding them.\n")

    result = np.dot(lang_vectors[1], np.transpose(lang_vectors[1]))
    f.write("\ndot product of single letter vector with itself is %d\n" % (result)) 

    result = np.dot(lang_vectors[2], np.transpose(lang_vectors[1]))
    f.write("\ndot product of bigrams vector with single-letter vector is %d\n" % (result))

    result = np.dot(lang_vectors[2], np.transpose(lang_vectors[2]))
    f.write("\ndot product of bigrams vector with itself is %d\n" % (result)) 

    result = np.dot(up2_lang_vec, np.transpose(lang_vectors[2]))
    f.write("dot product of bigrams vector and up2_lang_vec is %d\n" % (result))

    #too much noise because other bigrams like th much more common. 
    #that's why get negative number
    result = np.dot(bigrams_sQ, np.transpose(RI_letters[alph.find("u")]))
    f.write("dot product of bigrams_sQ vector and u vector is %d\n" % (result))


    #manual_qu_vector = np.multiply(sQ, RI_letters[alph.find("u")])
    #f.write("qu_vector\n")
    #print qu_vector
    #f.write("\nmanual_qu_vector\n")
    #print manual_qu_vector
    #sQ_squared = np.multiply(sQ, sQ)
    #print sQ_squared
    
    #if predict poor, bc bigram poor, or at end of word
    #then do the up#_lang_vecs to predict bigrams, ngrams, etc simultaneously
    av26 = np.zeros((1,N))

    print av26
    for i in range(26):
        av26 += RI_letters[i]
    print av26
    result = np.dot(av26, np.transpose(RI_letters[alph.find("a")]))
    f.write("dot product of av26 vector and a vector is %d\n" % (result))

    result = np.dot(av26, np.transpose(av26))
    f.write("dot product of av26 vector and itself is %d\n" % (result))

    result = np.dot(av26, np.transpose(lang_vectors[1]))
    f.write("dot product of av26 vector and unigrams is %d\n" % (result))
    f.close()
    
