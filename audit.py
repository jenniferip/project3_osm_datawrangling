#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file audits the London OSM data in the following ways:

- create and manage a'mapping' that reflect the changes needed to fix the
    unexpected street types to the appropriate ones in the expected list.
- actually fix the street name in the function update_name which takes a
    string with street name as an argument and should return the fixed name.

NOTE: The concept of this code was taken from Udacity's OpenStreetMap Case
Study Lesson and Quizzes.
"""


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from datetime import datetime

OSMFILE = "london_sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE TO MAP OTHER PROBLEM NAMES
mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Ave.": "Avenue",
           "Rd": "Road",
           "Rd.": "Road"
           }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_up_for_fixing(elem):
    return (elem.attrib['k'] == 'fixme:date')


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    fixes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_up_for_fixing(tag):
                    fixes.add(tag.attrib['v'])
    osm_file.close()
    return street_types, fixes


def update_name(name, mapping):
    for key in mapping:
        if key in name:
            if name.endswith('.'):
                if key.endswith('.'):
                    name = name.replace(key, mapping[key])
                    break
                else:
                    continue
            else:
                name = name.replace(key, mapping[key])
    return name


def fix(to_fix):
    datetime_object = datetime.strptime(to_fix, '%Y-%m-%d')
    if datetime_object > datetime.today():
        fixed = datetime.today().strftime('%Y-%m-%d')
    return fixed


if __name__ == '__main__':
    st_types, fixes = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    pprint.pprint(fixes)
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
    for f in fixes:
        new_date = fix(f)
        print f, '=>', new_date 

