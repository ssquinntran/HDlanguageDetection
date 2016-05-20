import numpy as np
import string
import collections
from ..utils import random_idx
from ..utils import log_random_idx

alphabet = string.lowercase+" "
filepath = "preprocessed_texts/AliceInWonderland.txt"
k = 5000
N = 30000;
ordered = 1

#cluster_sizes = [1, 2, 3, 4, 5]
cluster_sizes = [1, 2, 3]
n_grams = []
#lv = random_idx.generate_letter_id_vectors(N,15000);
f = open(filepath, "r");
text = f.read();
text = ''.join([x for x in text if x in alphabet])[0:10000];
print text