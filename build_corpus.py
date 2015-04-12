#!/usr/bin/env python

"""
Builds or updates an existing corups of transliterated files.
All input files for building the corpus must be in one directory.
All files with tamil files must have their names being with ta_ and end with .txt
For english files, it should begin with en_ and end with .txt
All output files will have _out.txt suffix. So, if the input file is named
ta_sample.txt then its corresponding transliterated English content will be
in ta_sample_out.txt

python build_corpus.py -h for help
"""

import argparse
import os
import codecs
import en_ta_transliterate
import tamil_unicode_map
from ta_en_transliterate import TamilTransliterator

ta_en_transliterator = TamilTransliterator(tamil_unicode_map.charmap)

transliterators = {
    'en_ta': en_ta_transliterate.transliterate,
    'ta_en': ta_en_transliterator.transliterate,
}

def output_filename(filename):
    return '%s_out.txt' % (filename.split('.txt')[0])

def needs_translation(corpus_path, filename):
    if filename.endswith('_out.txt'):
        return False

    in_filepath = os.path.join(corpus_path, filename)
    out_filepath = os.path.join(corpus_path, output_filename(filename))

    if not os.path.isfile(out_filepath):
        return True

    in_file_details = os.stat(in_filepath)
    out_file_details = os.stat(out_filepath)

    if out_file_details.st_mtime < in_file_details.st_mtime:
        return True

    return False 

def get_transliterator(filename):
    if filename.startswith("en_"):
        return transliterators['en_ta']
    elif filename.startswith("ta_"):
        return transliterators['ta_en']
    else:
        return None

def main(corpus_path):
    filenames = os.listdir(corpus_path)
    for filename in filenames:
        if needs_translation(corpus_path, filename):
            transliterator = get_transliterator(filename)
            if not transliterator:
                continue
            with open(os.path.join(corpus_path, filename)) as text_file:
                text = text_file.read()
                return_code, transliterated_text = transliterator(text)
                if return_code == 0 and transliterated_text:
                    out_filename = output_filename(filename)
                    with codecs.open(os.path.join(corpus_path, out_filename), 'w', "utf-8") as out_file:
                        out_file.write(transliterated_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update transliteration corpus")
    parser.add_argument('-c', '--corpus-path', type=str, help="Path to the corpus folder")
    args = parser.parse_args()
    main(args.corpus_path)
