# Standard Python Libraries
import html.parser
import logging
import time
import sys
# Third-Party Libraries
from bs4 import BeautifulSoup
import requests
# Custom Libraries
import version

parser = html.parser.HTMLParser()


def request_sentences():
    # TODO: Create with keyword parameters
    pass


def generate_example_sentences(keyword_to_search_for):
    endpoint = "https://tatoeba.org/eng/sentences/search"
    language_from = "jpn"
    language_to = "eng"

    # https://tatoeba.org/eng/sentences/search
    # ?
    # from=jpn
    # has_audio=
    # list=
    # native=yes
    # orphans=no
    # query=%E7%94%A8%E8%AA%9E
    # sort=words
    # tags=
    # to=eng
    # trans_filter=limit
    # trans_has_audio=
    # trans_link=
    # trans_orphan=
    # trans_to=eng
    # trans_unapproved=
    # trans_user=
    # unapproved=no
    # user=
    response = requests.get(
        endpoint,
        params={
            "from": language_from,
            "native": "yes",
            "orphans": "no",
            "query": keyword_to_search_for,
            "sort": "words",
            "to": language_to,
            "trans_to": "eng",
            "unapproved": "no",
        }
    )
    soup = BeautifulSoup(response.text, "html.parser")
    sentences_and_translations = soup.findAll(
        "div", {"class": "sentence-and-translations"}
    )

    # list of tuples, where first index is japanese sentence, second index is
    # english sentence [(source, translation), ...]
    sentences_found = []
    for sentence_and_translation in sentences_and_translations:
        print("-" * 80)
        # print(sentence_and_translation)
        japanese_sentence = "MISSING"
        english_sentence = "MISSING"

        # Japanese sentence selection
        sentence_elements = sentence_and_translation.findAll(
            "div", {"class": "sentence"}
        )
        for sentence_element in sentence_elements:
            text_elements = sentence_element.findAll("div", {"class": "text"})
            # Should really be only one element
            for text_element in text_elements:
                japanese_sentence = text_element.text.strip()

        # English sentence selection
        translation_elements = sentence_and_translation.findAll(
            "div", {"class": "translation"}
        )
        for translation_element in translation_elements:
            text_elements = translation_element.findAll(
                "div", {"class": "text"}
            )
            # Should really be only one element
            for text_element in text_elements:
                english_sentence = text_element.string.strip()

        print("japanese_sentence: {}".format(japanese_sentence))
        print("english_sentence: {}".format(english_sentence))
        sentences_found.append((japanese_sentence, english_sentence))
    return sentences_found


if __name__ == "__main__":
    generate_example_sentences("用語")
