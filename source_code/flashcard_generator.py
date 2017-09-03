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
    jisho_term = jisho_scraper.generate_jisho_definition(term)
    # Default searches tatoeba for shortest, allegdly native-created, first result
    example_sentences = tatoeba_scraper.generate_example_sentences(term)

    # TODO: Check jisho_term.pronounciation != "MISSING"
    #       if it is then use pykakasi to convert the term to be in hiragana?
    # Not sure will work  if term isn't returned as well
    # if example_sentences:
    #     english_example_sentence, japanese_example_sentence = example_sentences[0]
    #     jisho_term["example_sentence_english"] = english_example_sentence
    #     jisho_term["example_sentence_japanese"] = japanese_example_sentence
    # else:
    #     jisho_term["example_sentence_english"] = ("No english sentence found for {}"
    #                                                          ).format(term)
    #     jisho_term["example_sentence_japanese"] = ("No japanese sentence found for {}"
    #                                                           ).format(term)
    # print(jisho_term)
    new_flashcard = {
        "jisho_term": jisho_term,
        "example_sentences": example_sentences,
    }

    return new_flashcard


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


def serialize_flashcard_vocabulary_term_to_quizlet_format(flashcard):
    jisho_term = flashcard["jisho_term"]
    example_sentences = flashcard["example_sentences"]

    # Takes the first element because there's an assumption that it's the only
    # term returned?
    # I haven't seen multiple terms and such returned?
    term = jisho_term["kanji"][0]

    return term


# lol naming
def serialize_flashcard_vocabulary_definition_to_quizlet_format(flashcard):
    jisho_term = flashcard["jisho_term"]
    example_sentences = flashcard["example_sentences"]

    definition = ""

    # Takes the first element because there's an assumption that it's the only
    # term returned?
    # I haven't seen multiple terms and such returned?
    definition += "{}\n".format(jisho_term["hiragana"][0])

    # Definition
    for sense in jisho_term["definitions"]:
        parts_of_speech = sense["parts_of_speech"]
        english_definitions = sense["english_definitions"]

        if parts_of_speech:
            definition += "~"
            definition += ", ".join(parts_of_speech)
            definition += "~"
            definition += "\n"

        if english_definitions:
            definition += ", ".join(english_definitions)
            definition += "\n"

    return definition


def serialize_flashcard_example_sentence_term_to_quizlet_format(flashcard):
    jisho_term = flashcard["jisho_term"]
    example_sentences = flashcard["example_sentences"]

    japanese_example_sentence = ""
    english_example_sentence = ""

    # Example Sentence
    if example_sentences:
        japanese_example_sentence, english_example_sentence = example_sentences[0]

    term = japanese_example_sentence

    return term


def serialize_flashcard_example_sentence_definition_to_quizlet_format(flashcard):
    jisho_term = flashcard["jisho_term"]
    example_sentences = flashcard["example_sentences"]

    japanese_example_sentence = ""
    english_example_sentence = ""

    # Example Sentence
    if example_sentences:
        japanese_example_sentence, english_example_sentence = example_sentences[0]

    definition = english_example_sentence

    return definition


def write_vocabulary_to_file(vocabulary_file_path, output_directory_path, flashcards):
    vocabulary_file_name_with_extension = os.path.basename(vocabulary_file_path)
    vocabulary_file_name, vocabulary_file_extension = os.path.splitext(vocabulary_file_name_with_extension)
    print(vocabulary_file_name)
    print(vocabulary_file_extension)

    output_vocabulary_filename = (vocabulary_file_name + ".txt")
    output_example_sentences_filename = (vocabulary_file_name + "例文.txt")

    vocabulary_output_file_path = os.path.join(output_directory_path,
                                               output_vocabulary_filename)
    example_sentences_output_file_path = os.path.join(output_directory_path,
                                                      output_example_sentences_filename)
    print(output_vocabulary_filename)
    print(output_example_sentences_filename)
    print(vocabulary_output_file_path)
    print(example_sentences_output_file_path)

    term_and_definition_delimeter = "=="
    card_delimeter = "\n\n"

    vocabulary_lines = []
    example_sentences_lines = []

    for flashcard in flashcards:
        # serialize_flashcard_vocabulary_term_to_quizlet_format
        # serialize_flashcard_vocabulary_definition_to_quizlet_format
        # serialize_flashcard_example_sentence_term_to_quizlet_format
        # serialize_flashcard_example_sentence_definition_to_quizlet_format

        vocabulary_term = serialize_flashcard_vocabulary_term_to_quizlet_format(flashcard)
        vocabulary_definition = serialize_flashcard_vocabulary_definition_to_quizlet_format(flashcard)
        new_vocabulary_line = ("{term}"
                               "{term_and_definition_delimeter}"
                               "{definition}"
                               "{card_delimeter}").format(term=vocabulary_term,
                                                          term_and_definition_delimeter=term_and_definition_delimeter,
                                                          definition=vocabulary_definition,
                                                          card_delimeter=card_delimeter)
        vocabulary_lines.append(new_vocabulary_line)

        example_sentence_term = serialize_flashcard_example_sentence_term_to_quizlet_format(flashcard)
        example_sentence_definition = serialize_flashcard_example_sentence_definition_to_quizlet_format(flashcard)
        example_sentence_line = ("{term}"
                                 "{term_and_definition_delimeter}"
                                 "{definition}"
                                 "{card_delimeter}").format(term=example_sentence_term,
                                                            term_and_definition_delimeter=term_and_definition_delimeter,
                                                            definition=example_sentence_definition,
                                                            card_delimeter=card_delimeter)
        example_sentences_lines.append(example_sentence_line)

    print("".join(vocabulary_lines))
    print("-" * 40)
    print("".join(example_sentences_lines))

    with open(vocabulary_output_file_path, 'w') as file:
        for line in vocabulary_lines:
            file.write(line)

    # print(flashcard)
    # print("// " + "-" * 77)
    # string_to_write = ("TERM: {term}"
    #                    "\nPRONOUNCIATION: {pronounciation}"
    #                    "\nDEFINITION: {definition}"
    #                    "\nPART OF SPEECH: {part_of_speech}").format(term=flashcard["kanji"],
    #                                                                 pronounciation=flashcard["hiragana"],
    #                                                                 definition=flashcard["english_definition"],
    #                                                                 part_of_speech=flashcard["part_of_speech"])
    # print(string_to_write)
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
