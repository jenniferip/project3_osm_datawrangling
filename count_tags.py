#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The purpose of this file is to find out what types of tags are used and also
how many of each tag are used. This is done in the count_tags function which
returns a dictionary with the tag name as the key and number of times the tag
is encountered in the map file as the value.

NOTE: The concept of this code was taken from Udacity's OpenStreetMap Case
Study Lesson and Quizzes.
"""

import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
        parse_tree = ET.iterparse(filename)
        tag_dict = {}
        for event, item in parse_tree:
            current_tag = item.tag
            if current_tag not in tag_dict:
                tag_dict[current_tag] = 1
            else:
                tag_dict[current_tag] += 1
        return tag_dict


if __name__ == "__main__":
    tag_dict = count_tags('london_sample.osm')
    pprint.pprint(tag_dict)
