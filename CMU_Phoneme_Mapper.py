from g2p_en import G2p
from nltk.corpus import cmudict
from nltk.corpus import stopwords as nltk_stopwords
import re


class CMUPhonemeMapper:

    def __init__(self, txt_filename=None, comment_indicator='//', section_header_regex='[\[.*\]]'):
        self.g2p = G2p()
        self.comment_indicator = comment_indicator
        self.section_header_regex = re.compile(section_header_regex)
        self.header_tag = '<HEADER>'
        self.split_regex = ' |-'

        self.txt_file = self.open_txt_file(txt_filename)
        self.delimited_lines = self.txt_to_delimited(self.txt_file)
        self.phoneme_lines = self.delimited_to_phonemes(self.delimited_lines)
        self.print_phoneme_map()

    @staticmethod
    def open_txt_file(txt_filename):
        if txt_filename is None:
            print('No txt provided - opening default.txt for phoneme mapping.')
            return open('default.txt', 'r', encoding="utf-8")
        elif not txt_filename.endswith('.txt'):
            raise Exception('Must provide a file with .txt extension.')
        try:
            return open(txt_filename, 'r', encoding="utf-8")
        except IOError:
            print('There was a problem opening the file.')

    def split_line(self, line):
        return re.split(self.split_regex, line)

    def parse_line(self, line):
        if line.startswith(self.comment_indicator) or line in ('', '\n'):
            return False
        elif self.section_header_regex.match(line):
            return line
        else:
            return self.split_line(line)

    def phoneme_map_line(self, line):
        mapped_line = []
        for token in line:
            mapped_line.append(self.g2p(token))
        return mapped_line

    def txt_to_delimited(self, txt_file):
        delimited_lines = []
        for line in txt_file.readlines():
            parsed_line = self.parse_line(line)
            if parsed_line:
                delimited_lines.append(parsed_line)
        txt_file.close()
        return delimited_lines

    def delimited_to_phonemes(self, delimited_lines):
        phoneme_lines = []
        for line in delimited_lines:
            if type(line) is str and self.section_header_regex.match(line):
                phoneme_lines.append(self.header_tag)
            else:
                phoneme_lines.append(self.phoneme_map_line(line))
        return phoneme_lines

    @staticmethod
    def concat_phonemes(line):
        concat_line = []
        for word in line:
            concat_line.append('_'.join(word))
        return concat_line

    def print_phoneme_map(self):
        for i, line in enumerate(self.phoneme_lines):
            if line == self.header_tag:
                print(self.delimited_lines[i])
            else:
                line = self.concat_phonemes(line)
                print('\t{0}'.format(' '.join(line)))
