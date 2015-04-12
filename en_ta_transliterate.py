#!/usr/bin/env python

"""
Module for transliterating tamil to english by using Google's transliteration API
"""

import urllib2
import urllib
import json
from StringIO import StringIO


def transliterate(english_text):

    response = urllib2.urlopen("https://inputtools.google.com/request?%s&itc=ta-t-i0-und&num=13&cp=0&cs=0&ie=utf-8&oe=utf-8" % urllib.urlencode({'text': english_text}))
    output = response.read()
    output = StringIO(output)
    t =  json.load(output)
    if t[0] == 'SUCCESS':
        return 0, t[1][0][1][0]
    else:
        return 1, ''

if __name__ == "__main__":
    text = "eppidi enna ethukku ennikku eppothaavathu puththakangkalai sariyaana"
    print text
    print transliterate(text)[1]
