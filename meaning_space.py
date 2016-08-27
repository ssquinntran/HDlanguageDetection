from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import string
import numpy as np
from utils import random_idx
from utils import utils
from utils import lang_vectors_utils as lvu

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

num_topics = 50
passes = 20
topn = 10
k = 5000
N = 10000
# cluster_sizes is mapping to n-gram size
# cluster_sz in random_idx referring to specific element (int) in cluster_sizes, array
cluster_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
ordered = 1
#assuming this is the alphabet bc of precedent in generate_text.py
#alph = 'abc' 
alphabet = string.lowercase + ' '
RI_letters = random_idx.generate_letter_id_vectors(N, k, alphabet)

def create_doc_set(path, files):
    doc_set = []
    for filename in files:
        f = open(path + filename, "r")
        doc_set.append(f.read())
        f.close()
    return doc_set


def tokenize(doc_set):
    # list for tokenized documents in loop
    texts = []
    # loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        # add tokens to list
        texts.append(stemmed_tokens)
    return texts

def create_meaning_matrix(ldamodel, topicid, topn, dictionary):
    # token 2 id dictionary
    # print dictionary.token2id
    matrix = np.zeros((N,N))
    id2token = dictionary.id2token
    topic_terms = []

    for tup in ldamodel.get_topic_terms(topicid, topn):
        topic_terms.append(str(id2token[tup[0]]))

    for i in range(0,topn):
        term_vector = random_idx.id_vector(N, topic_terms[i], alphabet, RI_letters, ordered)
        matrix[i] = term_vector
    return matrix


def create_meaning_matrices(ldamodel, num_topics, topn, dictionary):
    matrices = np.zeros((num_topics,N,N))
    for topicid in range(0,num_topics):
        matrices[topicid] = create_meaning_matrix(ldamodel, topicid, topn, dictionary)
    return matrices


def run():
    # create sample documents
    raw_path = "raw_texts/texts_english/"
    preprocessed_path = "preprocessed_texts/english/"
    training_preprocessed_path = "preprocessed_texts/english/with_spaces/"

    training_files = ["a_christmas_carol.txt", "alice_in_wonderland.txt"]
    # this is for testing accuracy against the 
    # actual stream that will be the test input
    test_files = ["hamlet_english.txt", "percy_addleshaw.txt"]

    training_doc_set = create_doc_set(training_preprocessed_path, training_files)
    test_doc_set = create_doc_set(preprocessed_path, test_files)

    tokenized_training_documents = tokenize(training_doc_set)
    tokenized_test_documents = tokenize(test_doc_set)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(tokenized_training_documents)
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in tokenized_training_documents]
    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)

    # for i in range(0,num_topics):
    #     topici = ldamodel.show_topic(i, topn)
    #     print topici

    # meaning matrix
    # https://radimrehurek.com/gensim/models/word2vec.html  ?????
    meaning_matrices = create_meaning_matrices(ldamodel, num_topics, topn, dictionary)
    print meaning_matrices[0][0]
    # need to fix configs to make working meaning matrices
    # token 2 id dictionary
    # print dictionary.token2id

    # was going to measure accuracy by multiplying or dot producting a
    # token vector with a meaning matrix

run()
