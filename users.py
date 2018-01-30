#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file's main function, process_map, finds out how many unique users
have contributed to the map for London by returning a set of unique user IDs
("uid").

NOTE: The concept of this code was taken from Udacity's OpenStreetMap Case
Study Lesson and Quizzes.
"""

import xml.etree.cElementTree as ET
import pprint


def get_user(element):
    if 'user' in element.attrib:
        return element.attrib['user']


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:
            users.add(element.attrib['uid'])
    return users


if __name__ == "__main__":
    users = process_map('london_sample.osm')
    print 'There are ' + str(len(users)) + ' unique users.'
