#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is used to sample the large london_data.osm file, which is useful
when initially building the Python functions to audit the data, as you can run
and check those functions on a smaller sample of the data before running it on
the whole dataset.

To get a smaller sample, increase the value of k. To get a larger sample,
decrease the value of k. k specifies every k-th top level element to extract.

NOTE: This code was taken directly from Udacity's Wrangle OpenStreetMap Data
Project details.
"""

import xml.etree.ElementTree as ET

OSM_FILE = "london_data.osm"
SAMPLE_FILE = "london_sample.osm"

k = 20


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-
    generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')
