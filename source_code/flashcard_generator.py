# Standard Python Libraries
import argparse
import os
# import logging
# import time
# import sys
# Third-Party Libraries
# import requests
# Custom Libraries
import jisho_scraper
import tatoeba_scraper
import version


def generate_flashcard(term):
    print("// " + "=" * 77)
    print("// Generating Flash Card For 「{}」".format(term))
    print("// " + "=" * 77)
    definition_dictionary = jisho_scraper.generate_jisho_definition(term)
    # Default searches tatoeba for shortest, allegdly native-created, first result
    example_sentences = tatoeba_scraper.generate_example_sentences(term)
    # TODO: Check definition_dictionary.pronounciation != "MISSING"
    #       if it is then use pykakasi to convert the term to be in hiragana?
    # Not sure will work  if term isn't returned as well
    if example_sentences:
        english_example_sentence, japanese_example_sentence = example_sentences[0]
        definition_dictionary["example_sentence_english"] = english_example_sentence
        definition_dictionary["example_sentence_japanese"] = japanese_example_sentence
    else:
        definition_dictionary["example_sentence_english"] = ("No english sentence found for {}"
                                                             ).format(term)
        definition_dictionary["example_sentence_japanese"] = ("No japanese sentence found for {}"
                                                              ).format(term)

    print(definition_dictionary)

    return definition_dictionary


def generate_flashcards(terms):
    flash_cards_to_return = []

    for term in terms:
        flash_cards_to_return.append(generate_flashcard(term))

    return flash_cards_to_return


def generate_vocabulary_file_paths(input_directory_path):
    print(input_directory_path)
    vocabulary_files = []

    # See Stack Overflow for a more "clever" solution
    # https://stackoverflow.com/questions/11540854/file-as-command-line-argument-for-argparse-error-message-if-argument-is-not-va
    is_input_directory_actually_a_directory = os.path.isdir(input_directory_path)
    is_input_directory_empty = (len(os.listdir(input_directory_path)) == 0)
    if not is_input_directory_actually_a_directory:
        print("Hey homie, the input files directory is not a directory.")
    elif is_input_directory_empty:
        print("Hey homie, the input directory is empty.")
    else:

        vocabulary_files = [os.path.join(input_directory_path, file)
                            for file
                            in os.listdir(input_directory_path)
                            if os.path.isfile(os.path.join(input_directory_path,
                                                           file))]

    return vocabulary_files


def read_input_file(input_file_path):
    terms = []

    with open(input_file_path) as file:
        for line in file:
            sanitized_line = line.strip()
            terms.append(sanitized_line)

    return terms


def format_flashcard_for_quizlet(term, definition):
    formatted_flashcard_string = ""
    formatted_flashcard_string += term
    formatted_flashcard_string += " - "
    formatted_flashcard_string += definition
    formatted_flashcard_string += "\n\n"

    return formatted_flashcard_string


def write_vocabulary_to_file(vocabulary_file_path, output_directory_path, flashcards):
    vocabulary_file_name_with_extension = os.path.basename(vocabulary_file_path)
    vocabulary_file_name, vocabulary_file_extension = os.path.splitext(vocabulary_file_name_with_extension)
    print(vocabulary_file_name)
    print(vocabulary_file_extension)

    output_vocabulary_filename = (vocabulary_file_name + ".txt")
    output_example_sentences_filename = (vocabulary_file_name + "例文.txt")
    print(output_vocabulary_filename)
    print(output_example_sentences_filename)

    # kanji
    # hiragana
    # part_of_speech
    # example_sentence_english
    # example_sentence_japanese
    with open(output_vocabulary_filename, 'w') as file:
        for flashcard in flashcards:
            # print(flashcard)
            print("// " + "-" * 77)
            string_to_write = ("TERM: {term}"
                               "\nPRONOUNCIATION: {pronounciation}"
                               "\nDEFINITION: {definition}"
                               "\nPART OF SPEECH: {part_of_speech}").format(term=flashcard["kanji"],
                                                                            pronounciation=flashcard["hiragana"],
                                                                            definition=flashcard["english_definition"],
                                                                            part_of_speech=flashcard["part_of_speech"])
            print(string_to_write)
            # file.write()


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",
                        "--version",
                        help="Print version number")
    # These should probably be positional arguments
    parser.add_argument("-i",
                        "--input_directory",
                        type=str,
                        help="The absolute path to line separated file of terms")
    parser.add_argument("-o",
                        "--output_directory",
                        type=str,
                        help="The directory to output the flash cards formatted for quizlet")
    return parser

if __name__ == '__main__':
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    input_directory_path = args.input_directory
    output_directory_path = args.output_directory

    vocabulary_file_paths = generate_vocabulary_file_paths(input_directory_path)

    for vocabulary_file_path in vocabulary_file_paths:
        print("Generating flash cards for: {}".format(vocabulary_file_path))
        terms_for_flashcards = read_input_file(vocabulary_file_path)

        print("// " + "=" * 77)
        print("// Flashcard terms to create")
        print("// " + "=" * 77)
        print("\n".join(terms_for_flashcards))

        flashcards = generate_flashcards(terms_for_flashcards)
        # flashcards = []

        print("// " + "=" * 77)
        print("// Flashcard information")
        print("// " + "=" * 77)
        for flashcard in flashcards:
            print("// " + "-" * 77)
            print(flashcard)

        is_output_file_is_actually_a_directory = os.path.isdir(output_directory_path)
        if is_output_file_is_actually_a_directory:
            # Write flashcards to files
            write_vocabulary_to_file(vocabulary_file_path,
                                     output_directory_path,
                                     flashcards)
        else:
            print("Hey homie, the output file was not a directory, maybe it's the wrong filepath?")
