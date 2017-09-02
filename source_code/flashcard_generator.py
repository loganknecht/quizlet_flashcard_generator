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


def write_vocabulary_to_file(filepath, flashcards):
    with open(filepath, 'w') as file:
        for flashcard in flashcards:
            pass
            # file.write()


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",
                        "--version",
                        help="Print version number")
    # These should probably be positional arguments
    parser.add_argument("-i",
                        "--input_file",
                        type=str,
                        help="The absolute path to line separated file of terms")
    parser.add_argument("-o",
                        "--output_directory",
                        help="The directory to output the flash cards formatted for quizlet",
                        action="store_true")
    return parser

if __name__ == '__main__':
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    input_file_path = args.input_file
    output_directory_path = args.output_directory

    # See Stack Overflow for a more "clever" solution
    # https://stackoverflow.com/questions/11540854/file-as-command-line-argument-for-argparse-error-message-if-argument-is-not-va
    is_input_file_is_actually_a_file = os.path.isfile(input_file_path)
    if is_input_file_is_actually_a_file:
        terms = read_input_file(input_file_path)
    else:
        print("Hey homie, the input file was not a file, maybe it's the wrong filepath?")

    print("// " + "=" * 77)
    print("// Flashcard terms to create")
    print("// " + "=" * 77)
    print("\n".join(terms))

    # generate_flashcards(["用語"])
    flashcards = generate_flashcards(terms)

    print("// " + "=" * 77)
    print("// Flashcard information")
    print("// " + "=" * 77)
    for flashcard in flashcards:
        print("// " + "-" * 77)
        print(flashcard)

    is_output_file_is_actually_a_directory = os.path.isdir(output_directory_path)
    if is_input_file_is_actually_a_file:
        # Write flashcards to files
        write_vocabulary_to_file(output_directory_path, flashcards)
    else:
        print("Hey homie, the output file was not a directory, maybe it's the wrong filepath?")
