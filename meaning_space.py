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
raw_path = "raw_texts/texts_english/"
preprocessed_path = "preprocessed_texts/english/"
training_preprocessed_path = "preprocessed_texts/english/with_spaces/"
training_files = ["a_christmas_carol.txt", "alice_in_wonderland.txt"]
test_files = ["hamlet_english.txt", "percy_addleshaw.txt"]
training_doc_set = []
# this is for testing accuracy against the 
# actual stream that will be the test input
def create_doc_set(path, files):
    doc_set = []
    for filename in files:
        f = open(path + filename, "r")
        doc_set.append(f.read())
        f.close()
    print doc_set[0]

exit()

num_topics = 10
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
print dictionary
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=passes)

for i in range(0,num_topics):
    topici = ldamodel.show_topic(i, topn=10)
    print topici

# can update the lda model
# lda model doesn't do continuous streams bc needs spaces to label words














