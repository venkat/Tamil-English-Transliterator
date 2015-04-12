# Tamil-English-Transliterator

Transliterate between English and Tamil

For example, transliteration converts எப்பிடி to eppidi (and vice-versa).

Put the files you want to be transliterated in some directory, begin files with tamil characters with the prefix ta_ (ending with .txt). en_ prefix for contents with english characters.
Then run `python build_corpus.py --corpus-path <dirname>`. This will produce output in files suffixed _out.txt in the `<dirname>` directory. Take a look at the included `corpus/` folder with sample contents.

`build_corpus.py` internally uses `ta_en_transliterate.py` or `en_ta_transliterate.py` which it chooses on a per-file basis based on the prefix in the filename. The tamil to english transliterator basically calls out to Google's transliteration API. English to Tamil transliterator uses the `tamil_unicode_map.py` which is a mapping between the unicode codepoints to their english character mapping.
