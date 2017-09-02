# Standard Python Libraries
# import logging
# import time
# import sys
# Third-Party Libraries
# import requests
# Custom Libraries
import jisho_scraper
import tatoeba_scraper
import version


def generate_flashcards():
    print("// " + "-" * 77)
    print("// Generating Flash Cards")
    print("// " + "-" * 77)
    definition_dictionary = jisho_scraper.generate_jisho_definition("用語")
    example_sentences = tatoeba_scraper.generate_example_sentences("用語")

generate_flashcards()
