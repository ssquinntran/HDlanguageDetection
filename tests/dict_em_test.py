import pickle
import unittest
from markdown_adapter import run_markdown
from algos import lookup_algo as la
class TestAlice(unittest.TestCase):
 
    def setUp(self):
    	la.seed()
    	fread = open("../intermediate/processing_array_explain_away_results", "r")
    	fread1 = open("../intermediate/lookup_lv","r")
    	fread2 = open("../intermediate/lookup_lang_vectors", "r")
    	fread3 = open("../intermediate/lookup_n_gram_frequencies", "r")
    	fread4 = open("../intermediate/lookup_vocab_vec", "r")
    	fread5 = open("../intermediate/lookup_vocab_array", "r")
    	self.processing = fread.read()
    	self.lv = pickle.load(fread1)
    	self.lang_vectors = pickle.load(fread2)
    	self.n_gram_frequencies = pickle.load(fread3)
    	self.vocab_vec = pickle.load(fread4)
    	self.vocab_array = pickle.load(fread5)
    	fread.close()
    	fread1.close()
    	fread2.close()
    	fread3.close()
    	fread4.close()
    	fread5.close()

 
    def test_alice(self):
    	filepath = "../preprocessed_texts/english/alice-only-stream.txt"
    	hed = hard_em_discover_words(self.processing, self.vocab_array, \
    		len(max(self.vocab_array.keys()), filepath)
    	wrong = 0
    	fread = open("../preprocessed_texts/english/alice-only-spaced.txt")
    	ground_truth = fread.read()
    	ground_truth = ground_truth.split(" ")
    	result = hed.split(" ")
    	differences = len(list(set(ground_truth) - set(result)))
    	self.assertEqual(0, differences)

    	fwrite = open("../intermediate/lookup_lang_vectors", "w")
    	fwrite1 = open("../intermediate/lookup_n_gram_frequencies", "w")
    	fwrite2 = open("../intermediate/lookup_vocab_vec", "w")
    	fwrite3 = open("../intermediate/lookup_vocab_array", "w")
    	fwrite4 = open("../output/em_alice", "w")
	    pickle.dump(lang_vectors, fwrite)
	    pickle.dump(n_gram_frequencies, fwrite1)
	    pickle.dump(vocab_vec, fwrite2)
	    pickle.dump(vocab_array, fwrite3)
	    fwrite4.write(result)
	    fwrite.close()
	    fwrite1.close()
	    fwrite2.close()
	    fwrite3.close()
	    fwrite4.close()

class TestHamlet(unittest.TestCase):
 
    def setUp(self):
        la.seed()
 		fread = open("../intermediate/processing_array_explain_away_results", "r")
    	fread1 = open("../intermediate/lookup_lv","r")
    	fread2 = open("../intermediate/lookup_lang_vectors", "r")
    	fread3 = open("../intermediate/lookup_n_gram_frequencies", "r")
    	fread4 = open("../intermediate/lookup_vocab_vec", "r")
    	fread5 = open("../intermediate/lookup_vocab_array", "r")
    	self.processing = fread.read()
    	self.lv = pickle.load(fread1)
    	self.lang_vectors = pickle.load(fread2)
    	self.n_gram_frequencies = pickle.load(fread3)
    	self.vocab_vec = pickle.load(fread4)
    	self.vocab_array = pickle.load(fread5)
    	fread.close()
    	fread1.close()
    	fread2.close()
    	fread3.close()
    	fread4.close()
    	fread5.close()

    def test_hamlet(self):
    	filepath = "../preprocessed_texts/english/hamlet_english.txt"
    	hed = hard_em_discover_words(self.processing, self.vocab_array, \
    		len(max(self.vocab_array.keys()), filepath)
    	wrong = 0
    	fread = open(filepath)
    	ground_truth = fread.read()
    	ground_truth = ground_truth.split(" ")
    	result = hed.split(" ")
    	differences = len(list(set(ground_truth) - set(result)))
    	self.assertLessEqual(.8, float((len(ground_truth)-differences)/len(ground_truth)))
    	fwrite = open("../intermediate/lookup_lang_vectors", "w")
    	fwrite1 = open("../intermediate/lookup_n_gram_frequencies", "w")
    	fwrite2 = open("../intermediate/lookup_vocab_vec", "w")
    	fwrite3 = open("../intermediate/lookup_vocab_array", "w")
    	fwrite4 = open("../output/em_hamlet")
	    pickle.dump(lang_vectors, fwrite)
	    pickle.dump(n_gram_frequencies, fwrite1)
	    pickle.dump(vocab_vec, fwrite2)
	    pickle.dump(vocab_array, fwrite3)
	    fwrite4.write(result)
	    fwrite.close()
	    fwrite1.close()
	    fwrite2.close()
	    fwrite3.close()
	    fwrite4.close()

class TestPercy(unittest.TestCase):
	def setUp(self):
        la.seed()
 		fread = open("../intermediate/processing_array_explain_away_results", "r")
    	fread1 = open("../intermediate/lookup_lv","r")
    	fread2 = open("../intermediate/lookup_lang_vectors", "r")
    	fread3 = open("../intermediate/lookup_n_gram_frequencies", "r")
    	fread4 = open("../intermediate/lookup_vocab_vec", "r")
    	fread5 = open("../intermediate/lookup_vocab_array", "r")
    	self.processing = fread.read()
    	self.lv = pickle.load(fread1)
    	self.lang_vectors = pickle.load(fread2)
    	self.n_gram_frequencies = pickle.load(fread3)
    	self.vocab_vec = pickle.load(fread4)
    	self.vocab_array = pickle.load(fread5)
    	fread.close()
    	fread1.close()
    	fread2.close()
    	fread3.close()
    	fread4.close()
    	fread5.close()

    def test_percy(self):
    	filepath = "../preprocessed_texts/english/percy_addleshaw.txt"
    	hed = hard_em_discover_words(self.processing, self.vocab_array, \
    		len(max(self.vocab_array.keys()), filepath)
    	wrong = 0
    	fread = open(filepath)
    	ground_truth = fread.read()
    	ground_truth = ground_truth.split(" ")
    	result = hed.split(" ")
    	differences = len(list(set(ground_truth) - set(result)))
    	self.assertLessEqual(.8, float((len(ground_truth)-differences)/len(ground_truth)))
    	fwrite = open("../intermediate/lookup_lang_vectors", "w")
    	fwrite1 = open("../intermediate/lookup_n_gram_frequencies", "w")
    	fwrite2 = open("../intermediate/lookup_vocab_vec", "w")
    	fwrite3 = open("../intermediate/lookup_vocab_array", "w")
    	fwrite4 = open("../output/em_percy")
	    pickle.dump(lang_vectors, fwrite)
	    pickle.dump(n_gram_frequencies, fwrite1)
	    pickle.dump(vocab_vec, fwrite2)
	    pickle.dump(vocab_array, fwrite3)
	    fwrite4.write(result)
	    fwrite.close()
	    fwrite1.close()
	    fwrite2.close()
	    fwrite3.close()
	    fwrite4.close()
if __name__ == '__main__':
    unittest.main()