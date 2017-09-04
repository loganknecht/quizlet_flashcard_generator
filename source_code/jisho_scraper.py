# Standard Python Libraries
import logging
import time
import sys
# Third-Party Libraries
import pykakasi
import requests
# Custom Libraries
import version

jisho_search_endpoint = "http://jisho.org/api/v1/search/words"

kakasi = pykakasi.kakasi()
kakasi.setMode("K", "H")  # Input: Katakana / Output: Hiragana
kakasi.setMode("J", "H")  # Input: Japanese / Output: Hiragana
hiragana_text_normalizer = kakasi.getConverter()


def request_jisho_term(search_keyword):
    """Iterates through the jisho request and creates a list of dictionary
    objects that contains the jisho information returned. The jisho response has
    two categories 'japanese', 'senses'. Each of their respective indexes are
    assumed to map.
    """
    response = requests.get(jisho_search_endpoint,
                            data={
                                "keyword": search_keyword,
                            })
    # print(response)
    response_json = response.json()
    term_list = response_json["data"]

    # Jisho term is just a container class for the list of information
    # Indexes for separate propreties are assumed to map to each other
    jisho_terms = []
    for term in term_list:
        print("// " + "-" * 77)
        print("// Parsing definition")
        print("// " + "-" * 77)
        print(term)

        kanji_spelling_found = []
        hiragana_spelling_found = []
        definitions_found = []

        # Traverses the response for Japanese
        # contains the term
        # contains the pronounciation
        for japanese_word in term["japanese"]:
            # Kanji - should be a single value getting appended
            if "word" in japanese_word:
                kanji_spelling_found.append(japanese_word["word"])
            # Hiragana - should be a single value getting appended
            if "reading" in japanese_word:
                hiragana_spelling_found.append(japanese_word["reading"])
            else:
                hiragana_spelling_found = hiragana_text_normalizer.do(japanese_word["word"])

        # Traverses the response for  Senses
        # contains the part of speech
        # contains the english definitions
        senses_list = term["senses"]

        for sense in senses_list:
            # English Definition - should be a list getting appended?
            definitions_found.append(sense)

        print("English definitions: {}".format(definitions_found))
        print("Hiragana: {}".format(hiragana_spelling_found))
        print("Kanji: {}".format(kanji_spelling_found))

        new_jisho_term = {
            "definitions": definitions_found,
            "hiragana": hiragana_spelling_found,
            "kanji": kanji_spelling_found,
        }
        jisho_terms.append(new_jisho_term)

    return jisho_terms


def generate_jisho_definition(search_keyword):
    jisho_terms = request_jisho_term(search_keyword)

    # Ok, at this point jisho has returned a bunch of stuff from the search right?
    # Right.
    # So, because we're relying on jisho to do the hard work of finding the most
    # relevant search for the term we're going to take the top item returned

    if jisho_terms:
        definition_to_return = jisho_terms[0]
    else:
        return None

    return definition_to_return

if __name__ == '__main__':
    generate_jisho_definition("用語")
