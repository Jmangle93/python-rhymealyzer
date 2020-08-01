from CMU_Phoneme_Mapper import CMUPhonemeMapper


class PhonemeRhymeAnalyzer:

    def __init__(self):
        self.mapper = CMUPhonemeMapper()
        self.rhyme_line_mappings = []
        self.rhyme_dict = {}
        self.vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
        self.ascii_counter = 64
        self.cycle_all_sections()
        # self.print_mapped_lines()
        # self.mapper.print_phoneme_map()

    def is_phoneme_in_recorded(self, phoneme):
        for existing_phoneme in self.rhyme_dict.keys():
            if phoneme in existing_phoneme and phoneme != existing_phoneme:
                return existing_phoneme
            elif phoneme in existing_phoneme:
                return existing_phoneme
        return False

    def get_sound_by_last_vowel(self, line):
        accumulated_sound = ''
        for i in range(len(line)):
            this_phoneme = line[-(1 + i)]
            first_char_in_phoneme = this_phoneme[0]
            if first_char_in_phoneme not in self.vowels:
                accumulated_sound = ''.join([this_phoneme, accumulated_sound])
            else:
                return ''.join([this_phoneme, accumulated_sound])
        print('WARNING - No vowel sound')
        return False

    def map_line_ending(self, line):
        line_ending_sound = self.get_sound_by_last_vowel(line)
        recorded_phoneme = self.is_phoneme_in_recorded(line_ending_sound)
        if recorded_phoneme:
            self.rhyme_dict[recorded_phoneme] = [chr(self.ascii_counter)]
            print('Phoneme Duplicate Recorded: {0}'.format(recorded_phoneme))
            return self.rhyme_dict[recorded_phoneme]
        elif line_ending_sound not in self.rhyme_dict.keys():
            self.ascii_counter = self.ascii_counter + 1
            self.rhyme_dict[line_ending_sound] = [chr(self.ascii_counter)]
            return self.rhyme_dict[line_ending_sound]

    def cycle_all_sections(self):
        for line in self.mapper.phoneme_lines:
            if self.mapper.is_line_a_header(line):
                self.rhyme_line_mappings.append(self.mapper.header_tag)
            else:
                self.rhyme_line_mappings.append(self.map_line_ending(line))

    def print_mapped_lines(self):
        for i, line in enumerate(self.mapper.delimited_lines):
            if self.rhyme_line_mappings[i]:
                this_mapping = self.rhyme_line_mappings[i]
                print('{0}\t\t~~~\t\t{1}'.format(line, this_mapping))
