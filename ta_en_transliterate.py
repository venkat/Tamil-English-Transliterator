#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for transliterating tamil to english.
"""

import tamil_unicode_map
from collections import deque

class Mapper(object):
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
        for category in charmap:
            codepoints = charmap[category]
            for codepoint in codepoints:
                self.codepoint_to_char[codepoint] = codepoints[codepoint][0]
                in_english = codepoints[codepoint][1]
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

class TamilTransliterator(object):
    def __init__(self, charmap):
        self.mapper = Mapper(charmap)

    #this is for just one word
    def to_english(self, text):
        text = self.preprocess(text)
        text = deque(text)
        output = deque()
        l = len(text)

        while text:
            c = text.popleft()
            in_english = self.mapper.in_english(c)
            parent_type, sub_type = self.mapper.char_type(c)
            #print c, parent_type, sub_type
            if parent_type is 'pulli':
                output.pop() # na followed by pulli becomes n
            elif parent_type is 'vowels' and sub_type is not 'independent_vowels':
                output.pop()
                output.extend(deque(in_english))
            else:
                output.extend(deque(in_english))
        return u''.join(output)  

    def preprocess(self, text):
        return unicode(text, 'utf-8')

    #this is for the whole text
    def transliterate(self, text):
        words = text.split()
        transliterated_words = [self.to_english(w) for w in words]
        return 0, u' '.join(transliterated_words).lower()

if __name__ == "__main__":
    t = TamilTransliterator(tamil_unicode_map.charmap)
    text = "எப்பிடி என்ன எதுக்கு என்னிக்கு எப்போதாவது புத்தகங்களை சரியான            " 
    print text
    print t.transliterate(text)[1]
#TODO: use google transliterate with a transliterated text I wrote, convert to tamil words and then convert back using transliterator code.
