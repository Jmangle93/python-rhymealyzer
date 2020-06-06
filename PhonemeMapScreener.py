# Given phoneme maps such as:
#	[['S', 'IH1', 'K', 'ER0'], ['DH', 'AE1', 'N'],
#	 ['DH', 'AH0'], ['R', 'EH1', 'S', 'T', ' ', ',']]
# Remove punctuation including spaces and empty items
#
# from nltk.corpus import cmudict
# cmudict = cmudict.dict()

import re
import shelve

pickle_dir = 'Pickled Song Data/Pickled Phonemes/'

all_songs = {}
for genre in ['Country', 'Pop', 'Rap', 'Rock Alt']:
	this_shelf = shelve.open(pickle_dir + genre)
	all_songs[genre] = this_shelf[genre]
	this_shelf.close()


sample_phoneme_map = all_songs['Rock Alt']['Red Hot Chili Peppers']['Californication']['phoneme_map']
# Should use the actual CMU dictionary for screening?
# The ARPAbet (which CMU dict is based on) makes use of other punctuation,
# But it seems CMU dict applies only 39 strict phonemes and emphasis markers, 0, 1, 2.
punct_to_remove = ['', ' ', '?', '!', '.', ',', ';', ':', '\'']

def screen_punct_from_phoneme_line(phoneme_line, punct_to_remove):
	for i, word in enumerate(phoneme_line):
		word[:] = [phoneme for phoneme in word if not phoneme in punct_to_remove]
		phoneme_line[i] = word
	return phoneme_line

new_map = []
for phoneme_line in sample_phoneme_map:
	new_map.append(screen_punct_from_phoneme_line(phoneme_line, punct_to_remove))

# Need to start testing the lyric data at this point.
#	Will run back down the genius->formatted_lyrics pipeline to attempt reusability.
