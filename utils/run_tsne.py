import random_idx
import lang_vectors_utils
import numpy as np 
import string
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import sys
from sklearn import manifold, datasets


k = 500
N = 1000
n_components = 2 
n_neighbors = 10
method = 'hessian'
alphabet = string.lowercase + ' '
a = '../preprocessed_texts/english/with_spaces/alice_in_wonderland.txt'

one_hot_encoding = random_idx.generate_letter_id_vectors(N, k)
lst = []

with open(a, 'r') as f:
	for line in f:
		for word in line.split():
			beta = random_idx.id_vector(N, word, alphabet, one_hot_encoding)
			lst.append(beta)

tup = tuple(lst)

big_matrix = np.vstack(lst)
big_matrix = big_matrix[0:1000]
print big_matrix.shape

print "compressing data"

fig = plt.figure(figsize=(15, 8))

tsne = manifold.TSNE(n_components=n_components, init='pca', random_state=0)
Y = tsne.fit_transform(big_matrix)

plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
plt.show()
se = manifold.SpectralEmbedding(n_components=n_components,n_neighbors=n_neighbors)
Y = se.fit_transform(big_matrix)
plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
plt.show()

