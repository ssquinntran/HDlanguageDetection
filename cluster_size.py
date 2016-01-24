import subprocess
import tempfile
root_dir = "~/Documents/Pentti/language_detection_with_memory/"
			"raw_texts/texts_"
all_texts = [root_dir "afrikaans/digters_uit_Suid_afrika.txt",
	     root_dir "danish/det_hvide_hus.txt",
	     root_dir "dutch/hermaphrodisie_en_uranisme.txt",
	     root_dir "english/AliceInWonderland.txt",
	     root_dir "english/a_christmas_carol.txt", 
	     root_dir "english/hamlet_english.txt",
	     root_dir "english/percy_addleshaw.txt",
	     root_dir "finnish/Finnish-Kivi-7.txt",
	     root_dir "finnish/hamlet_finnish.txt"
	     root_dir "french/les_miserables_tome_I.txt",
	     root_dir "german/freud.txt",
	     root_dir "norwegian/hamsun_markens.txt",
	     root_dir "spanish/tres_comedias_modernas.txt",
	     root_dir "swedish/Swedish-Topelius-Historisk.txt"

	     
]
max_cluster_size = 0
for url in all_texts:
	byteString = subprocess.check_output(["wc", url])
	# extract digits of character count from the string
	# only for positive numbers
	all_counts = [int(s) for s in byteString.split() if s.isdigit()]
	n = all_counts[2]
	if max_cluster_size < n:
		max_cluster_size = n
	# in root dir so do we have to provide full path?
	n_string = str(n)
	with open("n_gram_sizes.txt", "a+") as f:
		f.write(n_string)
		f.write("\n")
# print the max_cluster_size
with open("n_gram_sizes.txt", "a+") as f:
	f.write(str(max_cluster_size))

print(max_cluster_size)


