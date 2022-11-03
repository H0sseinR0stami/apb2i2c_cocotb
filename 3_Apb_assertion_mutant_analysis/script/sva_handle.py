import os

Apb_properties_sva = '../properties_sva/Apb_properties.sva'
temp_file = "../properties_sva/temp.txt"


def add_text_to_beginning_of_the_line(source_text, searched_word, added_word, added_word_index):
    with open(source_text, 'r') as input_file:
        lines = []
        for line in input_file:
            if searched_word in line:
                split_line = line.split()
                split_line.insert(added_word_index, added_word)
                lines.append(' '.join(split_line) + '\n')
            else:
                lines.append(line)

    with open(temp_file, 'w') as f:
        for line in lines:
            f.write(line)
        f.close()
    os.replace(temp_file, Apb_properties_sva)




