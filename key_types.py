#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains code which checks the "k" value for each "<tag>" and sees
if there are any potential problems. The potential problems are described by
three regular expressions that check for certain patterns in each tag. These
are:

  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.

The function key_type returns a dictionary of dictionaries in which the keys
for the outer dictionary are the potential problems described above and the
keys for the dictionaries describing each problem are count, an integer
value of the number of times we see the particular problem in all of the tags,
and text_values which is a set of the actual text value the "k" attribute has
for all tags.

NOTE: The concept of this code was taken from Udacity's OpenStreetMap Case
Study Lesson and Quizzes.
"""


import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        k_value = element.attrib['k']
        if lower.search(k_value) is not None:
            keys['lower']['count'] += 1
            keys['lower']['text_values'].add(k_value)
        elif lower_colon.search(k_value) is not None:
            keys['lower_colon']['count'] += 1
            keys['lower_colon']['text_values'].add(k_value)
        elif problemchars.search(k_value) is not None:
            keys['problemchars']['count'] += 1
            keys['problemchars']['text_values'].add(k_value)
        else:
            keys['other']['count'] += 1
            keys['other']['text_values'].add(k_value)
    return keys


def process_map(filename):
    keys = {"lower": {'count': 0, 'text_values': set()},
            "lower_colon": {'count': 0, 'text_values': set()},
            "problemchars": {'count': 0, 'text_values': set()},
            "other": {'count': 0, 'text_values': set()}}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


if __name__ == "__main__":
    keys = process_map('london_sample.osm')
    pprint.pprint(keys)
