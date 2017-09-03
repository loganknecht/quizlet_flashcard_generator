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


def generate_jisho_definition(search_keyword):
    response = requests.get(jisho_search_endpoint,
                            data={
                                "keyword": search_keyword,
                            })
    # print(response)
    response_json = response.json()
    term_list = response_json["data"]
    for term in term_list:
        print("// " + "-" * 77)
        print("// Parsing definition")
        print("// " + "-" * 77)
        print(term)
        # MINIMUM
        # TODO: Consider changing these from singular values to lists of output
        kanji_spelling = "MISSING"
        hiragana_spelling = "MISSING"

        english_definitions_found = []
        english_definition_to_return = "MISSING"

        parts_of_speech_found = []
        part_of_speech_to_return = "MISSING"

        # Traverses the response for Japanese, which contains the term and its
        # pronounciation
        japanese_list = term["japanese"]
        japanese_word = japanese_list[0]

        # Traverses the response for  Senses, which contains the part of speech
        senses_list = term["senses"]

        if(japanese_word is not None and
                japanese_word != ""):
            print(japanese_word)
            # Kanji
            if "word" in japanese_word:
                kanji_spelling = japanese_word["word"]
            # Hiragana
            if "reading" in japanese_word:
                hiragana_spelling = japanese_word["reading"]
            else:
                hiragana_spelling = hiragana_text_normalizer.do(search_keyword)

        for sense in senses_list:
            # English Definition
            english_definitions = sense["english_definitions"]
            for english_definition in english_definitions:
                english_definitions_found.append(english_definition)

            # Part of Speech
            parts_of_speech = sense["parts_of_speech"]
            for part_of_speech in parts_of_speech:
                parts_of_speech_found.append(part_of_speech)

        english_definitions_to_return = ", ".join(english_definitions_found)
        part_of_speech_to_return = ", ".join(parts_of_speech_found)

        print("Kanji: {}".format(kanji_spelling))
        print("Hiragana: {}".format(hiragana_spelling))
        print("Part of speech: {}".format(part_of_speech))
        print("English definitions: {}".format(english_definitions))

    dictionary_to_return = {
        "english_definition": english_definitions_to_return,
        "kanji": kanji_spelling,
        "hiragana": hiragana_spelling,
        "part_of_speech": part_of_speech_to_return,
    }

    return dictionary_to_return

if __name__ == '__main__':
    generate_jisho_definition("用語")
