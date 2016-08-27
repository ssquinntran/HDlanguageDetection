#!/usr/bin/python
# -*- coding: UTF-8 -*-

# text_cleaner.py
# preprocesses text so that it preserves only lowercase latin letters
# there are still empty lines in the text. without any spaces or \n they should not affect the clusters?
import sys
import string
import codecs
import re

from unidecode import unidecode

include = string.lowercase
exclude = string.punctuation


try:
		if len(sys.argv)> 1 and len(sys.argv) < 4 or len(sys.argv)>4:
				print "Usage: python script.py <inputFile.txt> <outputFile.txt> <'space' or 'nospace'>"
				sys.exit()
		run = 1
		inputfn = sys.argv[1]
		outputfn = sys.argv[2]
		with_space = sys.argv[3]

except IndexError:
		run = 0

def cleaner_fn(inputfn, outputfn):
		inputFile = codecs.open(str(sys.argv[1]), encoding='utf-8')
		outputFile = open(str(sys.argv[2]), 'w')

		for s in inputFile:
				t = cleaner(s)
				outputFile.write(t)

		inputFile.close()
		outputFile.close()

def cleaner(s):
		s = re.sub(u'ø', 'oe', s) # ø -> oe
		s = re.sub(u'å', 'aa', s) # å -> aa
		s = re.sub(u'æ', 'ae', s) # æ -> ae
		s = re.sub(u'ä', 'ae', s) # ä -> ae
		s = re.sub(u'ö', 'oe', s) # ö -> oe
		s = re.sub(u'ü', 'ue', s) # ü -> ue
		s = re.sub(u'ß', 'ss', s) # ß -> ss
		s = unidecode(s)

		# s = s.strip()
		string_split = s.split()
		new_s = ''

		# check for all uppercase
		for word in string_split:
				for ch in include:
						lowercase_exist = 0
						if ch in word:
								lowercase_exist = 1
								break
				num_exist = 0
				for num in '0123456789':
						if num in word:
								num_exist = 1
				if lowercase_exist and not num_exist:
						if with_space == "space":
							new_s += " " + word
						else:
							new_s += word
		# make all letters lowercase
		new_s = new_s.lower()

		# remove punctuation
		t = ''.join(ch for ch in new_s if ch not in exclude)
		return t

if run:
		cleaner_fn(inputfn,outputfn)
