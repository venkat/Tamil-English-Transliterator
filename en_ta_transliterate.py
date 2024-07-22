#!/usr/bin/env python

"""
Module for transliterating Tamil to English using Google's transliteration API
"""

import requests

def transliterate(english_text):
    url = "https://inputtools.google.com/request"
    params = {
        'text': english_text,
        'itc': 'ta-t-i0-und',
        'num': 13,
        'cp': 0,
        'cs': 0,
        'ie': 'utf-8',
        'oe': 'utf-8'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 

        data = response.json()
        # print(data)
        if data[0] == 'SUCCESS':
            return 0, data[1][0][1][0]
        else:
            return 1, ''
    except requests.exceptions.RequestException as e:
        print(f"Error requesting transliteration: {e}")
        return 1, ''

if __name__ == "__main__":
    text = "Enna panra? saptiya? Amma appa nalla irukangala?"
    print(text)
    print(transliterate(text)[1])
