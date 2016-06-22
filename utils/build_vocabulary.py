import re

def build_vocabulary():
	file = open('raw_texts/texts_english/alice_in_wonderland.txt', 'r')
	# .lower() returns a version with all upper case characters replaced with lower case characters.
	text = file.read().lower()
	file.close()
	# replaces anything that is not a lowercase letter, a space, or an apostrophe with a space:
	text = re.sub('[^a-z\ \']+', " ", text)
	words = list(text.split())
	vocab_dict = {}
	for word in words:
		if word in vocab_dict.keys():
			vocab_dict[word] += 1
		else:
			vocab_dict[word] = 1
	words.sort()
	words = set(words)
	vocab = [(w, vocab_dict[w]) for w in words]

	file = open('vocab.txt', 'w')
	for v in vocab:
		file.write("%s: %d" % (v[0], v[1]))
		file.write('\n')
	file.close()

