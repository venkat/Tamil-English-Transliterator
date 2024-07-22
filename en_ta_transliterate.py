#!/usr/bin/env python

"""
Module for transliterating tamil to english by using Google's transliteration API
"""

# import urllib2
import urllib
import json
from io import StringIO
import urllib.request
import urllib.parse


def transliterate(english_text):

    response = urllib.request.urlopen("https://inputtools.google.com/request?%s&itc=ta-t-i0-und&num=13&cp=0&cs=0&ie=utf-8&oe=utf-8" % urllib.parse.urlencode({'text': english_text}))
    output = response.read()
    output = output.decode('utf-8')

    output = StringIO(output)
    t =  json.load(output)
    if t[0] == 'SUCCESS':
        return 0, t[1][0][1][0]
    else:
        return 1, ''

if __name__ == "__main__":
    text = "eppidi enna ethukku ennikku eppothaavathu puththakangkalai sariyaana"
    print(text)
    print(transliterate(text)[1])
