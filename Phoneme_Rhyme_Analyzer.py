from CMU_Phoneme_Mapper import CMUPhonemeMapper
from nltk.corpus import cmudict
from nltk.corpus import stopwords as nltk_stopwords


class PhonemeRhymeAnalyzer:

    def __init__(self):
        self.mapper = CMUPhonemeMapper()
        self.rhyme_line_mappings = []
        self.rhyme_dict = {}

    def trim_line_ending(self, line):
        print('stub')

    def map_line_ending(self, line):
        print('stub')

    def cycle_all_sections(self):
        for line in self.mapper.phoneme_lines:
            if self.mapper.is_line_a_header(line):
                self.rhyme_line_mappings.append('')
            else:
                self.rhyme_line_mappings.append(self.map_line_ending(line))