from CMU_Phoneme_Mapper import CMUPhonemeMapper
from nltk.corpus import cmudict
from nltk.corpus import stopwords as nltk_stopwords


class PhonemeRhymeAnalyzer:

    def __init__(self):
        self.mapper = CMUPhonemeMapper()
        self.rhyme_line_mappings = []
        self.rhyme_dict = {}
        self.VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y']
        self.RHYME_LENGTH = 4
        self.rhyme_counter = 64
        self.cycle_all_sections()
        print(self.rhyme_dict)

    def is_phoneme_subset_of_recorded(self, phoneme):
        for existing_phoneme in self.rhyme_dict.keys():
            if phoneme in existing_phoneme and phoneme != existing_phoneme:
                return existing_phoneme
        return False

    def get_line_ending(self, line):
        if len(line) >= self.RHYME_LENGTH:
            return ' '.join(line[-self.RHYME_LENGTH:])
        else:
            return ' '.join(line[-len(line):])

    def map_line_ending(self, line):
        line_ending_phoneme = self.get_line_ending(line)
        recorded_phoneme = self.is_phoneme_subset_of_recorded(line_ending_phoneme)
        if recorded_phoneme:
            self.rhyme_line_mappings.append(self.rhyme_dict[recorded_phoneme])
        elif line_ending_phoneme not in self.rhyme_dict.keys():
            self.rhyme_counter = self.rhyme_counter + 1
            self.rhyme_dict[line_ending_phoneme] = [chr(self.rhyme_counter)]
            self.rhyme_line_mappings.append(self.rhyme_dict[line_ending_phoneme])

    def cycle_all_sections(self):
        for line in self.mapper.phoneme_lines:
            if self.mapper.is_line_a_header(line):
                self.rhyme_line_mappings.append(self.mapper.header_tag)
            else:
                self.rhyme_line_mappings.append(self.map_line_ending(line))