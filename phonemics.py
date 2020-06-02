from g2p_en import G2p
from nltk.corpus import stopwords as nltk_stopwords
import shelve
from MainArtistsDicts import MainArtistsDicts as artists
from MainCorpusMetadataCollector import MetadataCollector

g2p = G2p()
collector = MetadataCollector()
stopwords = set(nltk_stopwords.words('english'))

###############################################################################
# 	Notes: 	
# 			~ G2p-en maps words to the CMU Pronouncing Dictionary.
#				- G2p-en will guess on OOV words.
#			~ Song sections are delimited by square bracketed headers,
#				eg: [Chorus]
#			~ Callbacks/background vocals occur in parentheses, often at line
#				endings.
###############################################################################

#
# Collect phonemes for all words in each song.
#

def map_phonemes_by_line(lines):
	phoneme_map = []
	for line in lines:
		mapped_line = []
		for token in line.split():
			mapped_line.append(g2p(token))
		phoneme_map.append(mapped_line)
	return phoneme_map


all_songs = collector.collect_genres_artists_songs()
collector.genres_artists_songs = all_songs
one_song_per_genre = []
#for genre in all_songs:
#	for artist in all_songs[genre]:
#		for i, song in enumerate(all_songs[genre][artist]):
#			if i == 0:
#				one_song_per_genre.append(all_songs[genre][artist][song])

rock_only = {}
rock_only['Rock Alt'] = all_songs['Rock Alt']

#all_songs_mapped = collector.do_func_per_genre_artist_song(rock_only, map_phonemes_by_line)
#one_song_mapped = map_phonemes_by_line(one_song_per_genre[0].split('\n'))
#print(one_song_mapped[0:4])
#print(one_song_per_genre[0].split('\n')[1:5])

###############################################################################
# Apply tupled labels, same word and rhyme, to the tokenized songs.
###############################################################################

#
# Word mapper:
#	~ Unique words receive X# label, with # being the index of unique words as
#		they appear in order.
#	~ D# applies to delimiting/common words.
#		How would we define this 'common words' list statistically?
#

# Restructure genre_artist_song as:
#	{genre: {artist: {song: {lyrics: [...], word_map: [...], phoneme_map: [...]}}}}

#for genre in all_songs:
#	for artist in all_songs[genre]:
#		for song in all_songs[genre][artist]:
#			lyrics = all_songs[genre][artist][song]
#			all_songs[genre][artist][song] = {}
#			all_songs[genre][artist][song]['lyrics'] = lyrics
#			all_songs[genre][artist][song]['word_map'] = []
#			all_songs[genre][artist][song]['phoneme_map'] = []

#
# Map words for every song:
#	To do: Normalzie stop-word flags; Decide whether this is important for training.
#

def map_words_by_line(lines):
	lex = []
	word_map = []
	stop_label = 'S'
	word_label = 'X'
	for line in lines:
		if '[' in line:
			continue
		this_word_map = []
		for token in line.split():
			if token in stopwords:
				this_word_map.append(stop_label)
			elif token in lex:
				this_word_map.append(word_label + str(lex.index(token)))
			else:
				lex.append(token)
				this_word_map.append(word_label + str(len(lex)-1))
		word_map.append(this_word_map)
	return word_map

# Map all the songs.

#for genre in all_songs:
#	for artist in all_songs[genre]:
#		for song in all_songs[genre][artist]:
#			these_lines = all_songs[genre][artist][song]['lyrics'].split('\n')
#			all_songs[genre][artist][song]['word_map'] = map_words_by_line(these_lines)

#
# Map rhymes for every song
#

#for genre in all_songs:
#	for artist in all_songs[genre]:
#		for song in all_songs[genre][artist]:
#			these_lines = all_songs[genre][artist][song]['lyrics'].split('\n')
#			all_songs[genre][artist][song]['phoneme_map'] = map_phonemes_by_line(these_lines)

#
# Pickle new dict
#

pickle_dir = 'Pickled Song Data/Pickled Phonemes/'

#for genre in all_songs:
#	this_shelf = shelve.open(pickle_dir + '/' + genre)
#	this_shelf[genre] = all_songs[genre]

all_songs = {}
for genre in collector.genres:
	this_shelf = shelve.open(pickle_dir + genre)
	all_songs[genre] = this_shelf[genre]
	this_shelf.close()

#
# Map Line Endingd for Rhyme, Same Word, per song
#

def get_last_word_from_phoneme_line(phoneme_line):
	if len(phoneme_line) == 0:
		return []
	return phoneme_line[-1]

def get_rhyme_ending_from_last_word(phonemes, rhyme_length, break_symbol):
	if len(phonemes) == 0:
		return(break_symbol)
	elif len(phonemes) < rhyme_length:
		return phonemes
	else:
		return phonemes[-rhyme_length:]

def map_rhymed_endings_by_line(phoneme_lines, rhyme_length=4, break_symbol='BREAK'):
	rhyme_lex = []
	rhyme_map = []
	for phoneme_line in phoneme_lines:
		phonemes = get_last_word_from_phoneme_line(phoneme_line)
		rhyme_ending = get_rhyme_ending_from_last_word(phonemes, rhyme_length, break_symbol)
		if rhyme_ending == break_symbol:
			rhyme_map.append(break_symbol)
			continue
		print(rhyme_ending)
		rhyme_symbol = '+'.join(rhyme_ending)
		if not (rhyme_symbol in rhyme_lex):
			rhyme_lex.append(rhyme_symbol)
		rhyme_map.append(chr(rhyme_lex.index(rhyme_symbol) + ord('A')))
	return rhyme_map


californication_phoneme_lines = all_songs['Rock Alt']['Red Hot Chili Peppers']['Californication']['phoneme_map']

californication_rhyme_endings = map_rhymed_endings_by_line(californication_phoneme_lines, rhyme_length=3)
for i, line in enumerate(all_songs['Rock Alt']['Red Hot Chili Peppers']['Californication']['lyrics'].split('\n')):
	print('{0}\n\t{1}'.format(line, californication_rhyme_endings[i]))
