from g2p_en import G2p
import nltk
import re


class CMUPhonemeMapper:

    def __init__(self, txt_filename=None, comment_indicator='//', section_header_regex='[\[.*\]]'):
        self.g2p = G2p()
        self.comment_indicator = comment_indicator
        self.section_header_regex = re.compile(section_header_regex)
        self.header_tag = '<HEADER>'
        self.split_regex = ' |-'
        self.tokenizer = nltk.RegexpTokenizer(r"\w+")

        self.txt_file = self.open_txt_file(txt_filename)
        self.delimited_lines = self.txt_to_delimited(self.txt_file)
        self.word_separated_phoneme_lines = self.delimited_to_phonemes(self.delimited_lines)
        self.phoneme_lines = self.consolidate_phoneme_lines(self.word_separated_phoneme_lines)

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
        elif self.is_line_a_header(line):
            return line
        else:
            return self.tokenizer.tokenize(line)

    def is_line_a_header(self, line):
        if type(line) is str and self.section_header_regex.match(line):
            return True
        elif line == self.header_tag:
            return True
        else:
            return False

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
        word_separated_phoneme_lines = []
        for line in delimited_lines:
            if self.is_line_a_header(line):
                word_separated_phoneme_lines.append(self.header_tag)
            else:
                word_separated_phoneme_lines.append(self.phoneme_map_line(line))
        return word_separated_phoneme_lines

    @staticmethod
    def consolidate_phoneme_lines(word_separated_phoneme_lines):
        phoneme_lines = []
        for line in word_separated_phoneme_lines:
            phoneme_lines.append([phoneme for word in line for phoneme in word])
        return phoneme_lines

    @staticmethod
    def concat_phonemes(line):
        concat_line = []
        for word in line:
            concat_line.append('_'.join(word))
        return concat_line

    def print_phoneme_map(self):
        for i, line in enumerate(self.word_separated_phoneme_lines):
            if line == self.header_tag:
                print(self.delimited_lines[i])
            else:
                line = self.concat_phonemes(line)
                print('\t{0}'.format(' '.join(line)))
