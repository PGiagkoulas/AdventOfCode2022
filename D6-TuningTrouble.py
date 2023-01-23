class Marker:
    characters:         list
    start_of_packet:    bool
    marker_length:      int

    def __init__(self, marker_length):
        self.characters = []
        self.start_of_packet = False
        self.marker_length = marker_length

    def __slide_right_characters(self, new_start_index: int):
        self.characters = self.characters[new_start_index+1:]

    def __check_start_of_packet(self):
        if len(self.characters) == self.marker_length:
            print(f'[!] Start-of-packet detected: {self.characters}')
            self.start_of_packet = True
        return self.start_of_packet

    def __add_character(self, character: str):
        if character in self.characters:
            self.characters.append(character)
            first_occurrence_index = self.characters.index(character)
            self.__slide_right_characters(first_occurrence_index)
            print(f'[!] Character was present already. Window has slid by {first_occurrence_index} positions.')
        else:
            self.characters.append(character)
            print(f'[>] Character added for the first time')
        _ = self.__check_start_of_packet()

    def find_marker(self, seq: str):
        seq_index = 0

        while not self.start_of_packet and seq_index < len(seq):
            self.__add_character(seq[seq_index])
            seq_index += 1
        print(f'[>] Start-of-packet marker appears after character: {seq_index}')
        print(f'[>] Start-of-packet {self.characters}')


if __name__ == '__main__':
    with open('d6-input.txt') as f:
        lines = f.readlines()
    sequence = lines[0]
    start_packet_marker_object = Marker(4)
    start_packet_marker_object.find_marker(sequence)

    start_message_marker_object = Marker(14)
    start_message_marker_object.find_marker(sequence)
