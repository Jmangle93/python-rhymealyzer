from CMU_Phoneme_Mapper import CMUPhonemeMapper
from nltk.corpus import cmudict
from nltk.corpus import stopwords as nltk_stopwords


class PhonemeRhymeAnalyzer:

    def __init__(self):
        self.mapper = CMUPhonemeMapper()
        self.rhyme_line_mappings = []
        self.rhyme_dict = {}
        self.RHYME_LENGTH = 4
        self.rhyme_counter = 64

    def get_line_ending(self, line):
        if len(line) >= self.RHYME_LENGTH:
            return line[-self.RHYME_LENGTH:]
        else:
            return line[-len(line):]

    def map_line_ending(self, line):
        line_ending = self.get_line_ending(line)
        if line_ending not in self.rhyme_dict.keys():
            self.rhyme_counter = self.rhyme_counter + 1
            self.rhyme_dict[line_ending] = [chr(self.rhyme_counter)]
        # else... if it is not *exactly* a key, check if ending is *in* one of the keys?



    def cycle_all_sections(self):
        for line in self.mapper.phoneme_lines:
            if self.mapper.is_line_a_header(line):
                self.rhyme_line_mappings.append(self.mapper.header_tag)
            else:
                self.rhyme_line_mappings.append(self.map_line_ending(line))