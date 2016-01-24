#!/usr/bin/python
import subprocess
import re,fileinput
import text_cleaner

root_dir = '~/raw_texts/texts_'

 all_texts = [root_dir "afrikaans/digters_uit_Suid_afrika.txt",
        root_dir + "danish/det_hvide_hus.txt",
        root_dir + "dutch/hermaphrodisie_en_uranisme.txt",
        root_dir + "english/AliceInWonderland.txt",
        root_dir + "english/a_christmas_carol.txt", 
        root_dir + "english/hamlet_english.txt",
        root_dir + "english/percy_addleshaw.txt",
        root_dir + "finnish/Finnish-Kivi-7.txt",	
        root_dir + "finnish/hamlet_finnish.txt"
        root_dir + "french/les_miserables_tome_I.txt",
        root_dir + "german/freud.txt",
        root_dir + "norwegian/hamsun_markens.txt",
        root_dir + "spanish/tres_comedias_modernas.txt",
        root_dir + "swedish/Swedish-Topelius-Historisk.txt"
 ]
# all_texts = [root_dir + 'english/alice_in_wonderland.txt']

for file_name in all_texts:
