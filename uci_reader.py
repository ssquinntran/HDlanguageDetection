import numpy as np
import os 



def read_file(data_file):
	data = []
	labels = []
	if os.path.exists(data_file):
		with open(data_file) as f:
			for line in f:
				labels.append(line[0])
				counter = 2 
				letter_features = []
				while counter < len(line):
					letter_features.append(line[counter])
					# skip by 2 because of commas
					counter += 2
				data.append(letter_features)
		real_data = np.array(data)
		real_labels = np.array(labels)
		return real_data, real_labels

	else:
		raise Exception("File is not valid")
