from CMU_Phoneme_Mapper import CMUPhonemeMapper
from nltk.corpus import cmudict
from nltk.corpus import stopwords as nltk_stopwords


class PhonemeRhymeAnalyzer:

    def __init__(self):
        self.mapper = CMUPhonemeMapper()
        self.rhyme_line_mappings = []
        self.rhyme_dict = {}
        self.VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y']
        self.ascii_label_counter = 64
        self.cycle_all_sections()
        print(self.rhyme_dict)

    def is_phoneme_subset_of_recorded(self, phoneme):
        for existing_phoneme in self.rhyme_dict.keys():
            if phoneme in existing_phoneme and phoneme != existing_phoneme:
                return existing_phoneme
        return False

    def get_sound_by_last_vowel(self, line):
        accumulated_sound = ''
        for i in range(len(line)):
            this_phoneme = line[-(1 + i)]
            first_char_in_phoneme = this_phoneme[0]
            if first_char_in_phoneme not in self.VOWELS:
                accumulated_sound = ''.join([this_phoneme, accumulated_sound])
            else:
                return ''.join([this_phoneme, accumulated_sound])

    def map_line_ending(self, line):
        line_ending_phonemes = self.get_sound_by_last_vowel(line)
        recorded_phoneme = self.is_phoneme_subset_of_recorded(line_ending_phonemes)
        if recorded_phoneme:
            self.rhyme_line_mappings.append(self.rhyme_dict[recorded_phoneme])
        elif line_ending_phonemes not in self.rhyme_dict.keys():
            self.ascii_label_counter = self.ascii_label_counter + 1
            self.rhyme_dict[line_ending_phonemes] = [chr(self.ascii_label_counter)]
            self.rhyme_line_mappings.append(self.rhyme_dict[line_ending_phonemes])

    def cycle_all_sections(self):
        for line in self.mapper.phoneme_lines:
            if self.mapper.is_line_a_header(line):
                self.rhyme_line_mappings.append(self.mapper.header_tag)
            else:
                self.rhyme_line_mappings.append(self.map_line_ending(line))