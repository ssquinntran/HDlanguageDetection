from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
# create sample documents
path = "raw_texts/texts_english/"
files = ["a_christmas_carol.txt", "alice_in_wonderland.txt", "hamlet_english.txt", \
"percy_addleshaw.txt"]
doc_set = []
for filename in files:
	f = open(path + filename, "r")
	doc_set.append(f.read())
	f.close()

num_topics = 100
passes = 20
topn = 10
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

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=passes)

for i in range(0,num_topics):
	topici = ldamodel.show_topic(i, topn=10)
	print topici

# can update the lda model
# lda model doesn't do continuous streams bc needs spaces to label words














