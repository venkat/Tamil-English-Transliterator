#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for transliterating Tamil to English using a predefined character map.
"""

import tamil_unicode_map
from collections import deque
import requests

class Mapper:
    def __init__(self, charmap):
        self.codepoint_to_english = {}
        self.codepoint_to_category = {}
        self.codepoint_to_char = {}
        self.populate_map(charmap)
        self.categories = {
            'consonants': 'consonants',
            'pulli': 'pulli',
            'dependent_vowels_two_part': 'vowels',
            'dependent_vowels_left': 'vowels',
            'various_signs': 'vowels',
            'independent_vowels': 'vowels',
            'dependent_vowels_right': 'vowels'
        }

    def populate_map(self, charmap):
        for category, codepoints in charmap.items():
            for codepoint, (char, in_english) in codepoints.items():
                self.codepoint_to_char[codepoint] = char
                if isinstance(in_english, tuple):
                    self.codepoint_to_english[codepoint] = in_english[0]
                else:
                    self.codepoint_to_english[codepoint] = in_english
                self.codepoint_to_category[codepoint] = category

    def in_english(self, c):
        return self.codepoint_to_english.get(c, '')

    def char_type(self, c):
        sub_type = self.codepoint_to_category.get(c, '')
        parent_type = self.categories.get(sub_type, '')
        return parent_type, sub_type

class TamilTransliterator:
    def __init__(self, charmap):
        self.mapper = Mapper(charmap)
        self.transliteration_url = "https://inputtools.google.com/request"


    def to_english(self, text):
        text = self.preprocess(text)
        text = deque(text)
        output = deque()

        while text:
            c = text.popleft()
            in_english = self.mapper.in_english(c)
            parent_type, sub_type = self.mapper.char_type(c)

            if parent_type == 'pulli':
                if output:
                    output.pop()
            elif parent_type == 'vowels' and sub_type != 'independent_vowels':
                if output:
                    output.pop()
                output.extend(deque(in_english))
            else:
                output.extend(deque(in_english))

        return ''.join(output)
    

    #TODO: use google transliterate with a transliterated text I wrote, convert to tamil words and then convert back using transliterator code
    def to_tamil(self, english_text):
        params = {
            'text': english_text,
            'itc': 'en-t-i0-und',
            'num': 13,
            'cp': 0,
            'cs': 0,
            'ie': 'utf-8',
            'oe': 'utf-8'
        }

        try:
            response = requests.get(self.transliteration_url, params=params)
            response.raise_for_status()

            data = response.json()
            # print(data)
            if data[0] == 'SUCCESS':
                return data[1][0][1][0]
            else:
                return ''
        except requests.exceptions.RequestException as e:
            print(f"Error requesting transliteration: {e}")
            return ''

    def preprocess(self, text):
        if isinstance(text, bytes):
            return text.decode('utf-8')
        return text

    def transliterate(self, text):
        words = text.split()
        transliterated_words = [self.to_english(w) for w in words]
        return 0, ' '.join(transliterated_words).lower()

if __name__ == "__main__":
    t = TamilTransliterator(tamil_unicode_map.charmap)
    
    text = "என்ன பண்ற? சாப்டியா? அம்மா அப்பா நல்லா இருக்காங்களா?"
    print("Input: ", text)
    english_text = t.transliterate(text)[1]
    print("Tamil to English: ", english_text)

