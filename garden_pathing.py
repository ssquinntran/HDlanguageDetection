import numpy as np
import string
import collections
import pickle
from ..utils import random_idx as ri
from ..utils import log_random_idx as lri
from ..utils import log_lang_vectors as llv
from copy import deepcopy

alphabet = string.lowercase+" "
filepath = "../raw_texts/texts_english/alice_in_wonderland.txt"
N = 100000;
f = open(filepath, "r");
text = f.read().lower();
text = ''.join([x for x in text if x in alphabet]);
f.close();

# array is the array of log vectors
# Returns a list of possible successors to string
def get_predictions(string, array, lv):
	assert(len(string) < len(array))
	n = len(string)+1;
	x = [];
	for j in alphabet:
		text_mod = string+j;
		num = llv.recover_frequency(lv, text_mod, array[len(text_mod)-1]);
		x.append((num, j));

	x = sorted(x, key=lambda k:k[0], reverse = True)
	return x;



# def garden_path(stripped_text, array, n):
# 	testing_text = stripped_text[:n];

# 	combos = [[0,testing_text]]; #track top 5 results

# 	for i in stripped_text[n:]:
# 		new_combo = [];
# 		for k in combos:
# 			test_string = k[1][-(n):];
# 			out = get_predictions(test_string, array);
# 			entry_for_space = 0;
# 			entry_for_char = 0;
# 			for j in out:
# 				if j[1] == ' ':
# 					entry_for_space = j;
# 				if j[1] == i:
# 					entry_for_char = j;

# 			out = get_predictions(test_string[1:]+' ', array);
# 			for j in out:
# 				if j[1] == i:
# 					entry_for_space_char = j;

# 			conglomerate_value = (.75*entry_for_space[0]+.25*entry_for_space_char[0])

# 			new_combo.append((.95*k[0]+conglomerate_value, k[1]+' '+i));
# 			new_combo.append((.95*k[0]+entry_for_char[0], k[1]+i));

# 		combos = sorted(new_combo, key=lambda t:t[0], reverse=True)[:15];

# 	return combos;

def streaming_training(next_character, array1, array2, lv1, lv2, trellis,n):
	if next_character == ' ':
		#No training because it'll correctly classify
		return;
	nospace = trellis[0][1][-n+1:]+next_character
	space = trellis[0][1][-n+1:]+' '
	nospace_val = llv.recover_frequency(lv1, nospace, array1)+llv.recover_frequency(lv2, nospace, array2)
	space_val = llv.recover_frequency(lv1, space, array1)+llv.recover_frequency(lv2, space, array2)
	# print " = "
	if (space_val>nospace_val):
		# print array1[len(nospace)-1]
		array1[len(nospace)-1] = array1[len(nospace)-1] + llv.get_letter_vec(nospace, lv1)
		array2[len(nospace)-1] = array2[len(nospace)-1] + llv.get_letter_vec(nospace, lv2)
		# print array1[len(nospace)-1]
	return array1, array2;

def garden_path(stripped_text, array1, array2, n, original, training = 0):
	test_text = stripped_text[:n-1]
	trellis = [(0, test_text)];
	count = 0;

	for i in stripped_text[n-1:]:
		count = count+1
		if count%100 == 0:
			print count
		seen = set();
		k = [];
		for j in trellis:
			no_space = j[1][-n+1:]+i;
			# if no_space == 'cards':
			# 	print "cards"+ str(recover_frequency(lv, no_space, array))
			# if no_space == 'car ds':
			# 	print "cards"+str(space_first_freq = recover_frequency(lv, space_first, array))
			if(not no_space in seen):
				seen.add(no_space)
				no_space_cost = llv.recover_frequency(lv1, no_space, array1)+llv.recover_frequency(lv2, no_space, array2)
				k.append((j[0]+no_space_cost, j[1]+i));

			space_first = j[1][-n+1:] + ' ';
			if(not space_first in seen):
				seen.add(space_first)
				space_second = j[1][-n+1:][1:]+' '+i;
				space_first_freq = llv.recover_frequency(lv1, space_first, array1)+llv.recover_frequency(lv2, space_first, array2)

				space_cost = .9*space_first_freq
				k.append((j[0]+space_cost, j[1]+' '+i));
			if training:
				array1, array2 = streaming_training(i, array1, array2, lv1, lv2, trellis, 5)
			# print array1[len(no_space)-1]
			# print array1[0]



		k = sorted(k, key=lambda t:t[0], reverse=True);
		trellis = k[:25];

	# count = 0;
	# correct = 0;
	# for v in trellis[0][1]:
	# 	if(len(original) == count):
	# 		print correct/float(len(''.join([x for x in trellis[0][1] if x == ' '])))
	# 		break;
	# 	if original[count] == ' ' and v == ' ':
	# 		correct = correct+1;
	# 		count = count+1;
	# 		continue;
	# 	while original[count] == ' ':
	# 		count = count+1;
	# 	if original[count] == v:
	# 		count = count+1;
	# 		continue;

	# 	if v == ' ':
	# 		continue;


	# print "Correct percentage: "
	# print correct/float(len(''.join([x for x in trellis[0][1] if x == ' '])))

	return trellis


"""
The interface that you should interact with
"""
def wrapper_garden(s, n, training = 0):
	return garden_path(s, postprocessed_array1, postprocessed_array2, n, "", training)



try:
	postprocessed_array1 = np.load('../output/log/preprocessedngrams_100k.p')
	lv1 = np.load('../output/log/lv_100k.p')
except Exception as e:
	lv1 = ri.generate_letter_id_vectors(N,N/2);
	lv1.dump('../output/log/lv_100k.p')
	postprocessed_array1 = np.array(llv.load_ngram_vector(text, lv1, 6)) #creates the array up to 5 grams
	postprocessed_array1.dump('../output/log/preprocessedngrams_100k.p');
	print "finished generating"

try:
	postprocessed_array2 = np.load('../output/log/preprocessedngrams_2_100k.p')
	lv2 = np.load('../output/log/lv_2_100k.p')
except Exception as e:
	lv2 = ri.generate_letter_id_vectors(N,N/2);
	lv2.dump('../output/log/lv_2_100k.p')
	postprocessed_array2 = np.array(llv.load_ngram_vector(text, lv2, 6)) #creates the array up to 5 grams
	postprocessed_array2.dump('../output/log/preprocessedngrams_2_100k.p');
	print "finished generating"

# n = random_idx.generate_letter_id_vectors(10, 6)
# print n


def garden_path_accuracy(stripped_text, array, n, original):
	count = 0;
	test_text = original[:n-1]
	trellis = [(0, test_text, 0)];
	next_space = False;
	for i in original[n-1:]:
		count = count+1;
		if count%100 == 0:
			print count;
		if i == ' ':
			next_space = True;
			continue;
		k = [];
		for j in trellis:
			no_space = j[1][-n+1:]+i;
			space_first = j[1][-n+1:] + ' ';
			space_second = j[1][-n+1:][1:]+' '+i;

			no_space_cost = llv.recover_frequency(lv1, no_space, array)
			space_first_freq = llv.recover_frequency(lv1, space_first, array)
			space_second_freq = llv.recover_frequency(lv1, space_second, array)


			space_cost = (.50*space_first_freq+.50*space_second_freq)
			k.append([j[0]+no_space_cost, j[1]+i, j[2]]);
			k.append([j[0]+space_cost, j[1]+' '+i, j[2]]);


		k = sorted(k, key=lambda t:t[0], reverse=True);
		if(len(k) < 5):
			trellis = k;
		else:
			trellis = k[:30];


		if next_space:
			for j in range(len(trellis)):
				if trellis[j][1][-2] == ' ':
					trellis[j][2] = trellis[j][2]+1;
			next_space = False

	return trellis

#starts tests

test = wrapper_garden("thecatjumpedovertheillegalbrowndog", 4);
print test

# test = garden_path_accuracy(''.join(text[:1000].split()), postprocessed_array, 5, text[:1000])
# print ""
# print test[0];
# print test[0][2]/float(len(''.join([x for x in test[0][1] if x == ' '])))
# print ""

# string = "Edward Snowden has seemingly called on the British public to help oust David Cameron following the prime minister's admission that he profited from his late father's offshore trust. Cameron on Thursday finally conceded he and his wife, Samantha, owned shares in Ian Cameron's Blairmore Holdings, before selling them for around 30,000 in 2010. Snowden, who this time last week"
# string = string.lower();
# string = string.join([x for x in string if x in string.lowercase]);
# print string

# string = text[100:900]

# test = garden_path("enincheshighandherfacebrightenedupa", postprocessed_array1, postprocessed_array2, 5, "")#, "alice she had grown to her full size by this time youre nothing but a pack of cards")
# # print "Expected: " + "alice she had grown to her full size by this time youre nothing but a pack of cards"
# print test[0:5];
# print ""

# test = garden_path(''.join(string.split()), postprocessed_array1,postprocessed_array2, 5, string)#, "alice she had grown to her full size by this time youre nothing but a pack of cards")





# test = garden_path("cameflyingdownuponhershegavea", postprocessed_array, 4)
# print "Expected: " + "came flying down upon her she gave a"
# print test[0:5];
# print ""

# test = garden_path("unditmadenomarkbuthenowhastily", postprocessed_array, 4)
# print "Expected: " + "und it made no mark but he now hastily"
# print test[0:5];
# print ""

# print "Non alice english snippets"
# print "======="

# test = garden_path("soiwantedtostartoffbysaying", postprocessed_array, 4)
# print "Expected: " + "so i wanted to start off by saying"
# print test[0:5];
# print ""

# test = garden_path("nothinglikethefreshsmellof", postprocessed_array, 4)
# print "Expected: " + "nothing like the fresh smell of"
# print test[0:5];
# print ""
# print "Alice has only one occurence of 'fresh' and no occurence of 'smell'"

# test = garden_path("responsetoathreadontheirforums", postprocessed_array, 4)
# print "Expected: " + "response to a thread on their forums"
# print test[0:5];
# print ""
# print "No occurence of 'response', 'thread', 'forums'"

# test = garden_path("beginwiththereisnodoubtwhateveraboutthat ", postprocessed_array, 4)
# print "Expected: " + "begin with there is no doubt whatever about that "
# print test[0:5];
# print ""
# # print "First choice was incorrect, but second choice is"

# print "Long alice prediction"
# print "======"

# test = garden_path("threegardenersoblongandflatwiththeirhandsandfeetatthecornersnextthetencourtiersthesewereornamentedalloverwithdiamondsandwalkedtwoandtwoasthesoldiersdidafterthesecametheroyalchildrenthereweretenofthemandthelittledearscamejumpingmerrilyalonghandinhandincouplestheywereallornamentedwithheartsnextcametheguestsmostlykingsandqueensandamongthemalicerecognisedthewhiterabbititwastalkinginahurriednervousmannersmilingateverythingthatwassaidandwentbywithoutnoticingherthenfollowedtheknaveofheartscarryingthekings ", postprocessed_array, 5)
# print test[0:5];
# print ""
# print "Got:"
# print "three garden er so b long and flat with their hands and feet at the corner s next the ten court i ers the se were or namented all over with d i am o nds and walked two and two as the soldier s did after the se came the royal children there were ten of them and the little d e a r s camejumpingme rr il y alongh and inh and in couples they were all or name n t e d w it hh eartsnex t came the guests m os t lyk i ngs and queens and among them alicere c o gni sed the white rabbit it was talking in a hurried nervousmanner smiling at everything that was said and went by without noticing her the nfo l l ow ed the knave of hearts carrying the kings"

# # use neural_net to read percentage of inputs and outputs to predict space or not

##perceptron learning algorithm
##For incorrect classified streams, we add them into the classifer.