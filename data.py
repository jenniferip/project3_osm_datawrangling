#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file prepares the data to be inserted into a SQL database by parsing the
elements in the OSM XML file and transforming them from document format to
tabular format, thus making it possible to write to .csv files that can then
be imported to a SQL database as tables. In the end, this file will take in
our data and write it to the csv files: nodes.csv, nodes_tags.csv, ways.csv,
ways_nodes.csv, and ways_tags.csv.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in
  the correct format
- Write each data structure to the appropriate .csv files

The shape_element function transforms each iterparse Element object into a
dictionary with the correct format, described below. We validate the output
against a schema, described in the schema.py file, to ensure correctness.

### If the element top level tag is "node":
The dictionary returned has the format {"node": .., "node_tags": ...}

The "node" field holds a dictionary of the following top level node
attributes, all other attributes are ignored:
- id
- user
- uid
- version
- lat
- lon
- timestamp
- changeset

The "node_tags" field holds a list of dictionaries, one per secondary tag
which are child tags of nodes that have the tag name/type: "tag". Each
dictionary has the following fields from the secondary tag attributes:
- id: the top level node id attribute value
- key: the full tag "k" attribute value if no colon is present or the
    characters after the colon if one is.
- value: the tag "v" attribute value
- type: either the characters before the colon in the tag "k" value or
    "regular" if a colon is not present.

Additionally,

- if the tag "k" value contains problematic characters, the tag ignored
- if the tag "k" value contains one ":" the characters before the ":" are set
    as the tag type and characters after the ":" are set as the tag key
- if there are additional ":" in the "k" value they are ignored and kept as
    part of the tag key. For example:

      <tag k="addr:street:name" v="Lincoln"/>
      is turned into:
      {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}

- If a node has no secondary tags then the "node_tags" field is an empty list.

The final return value for a "node" element looks something like:

  {'node': {'id': 757860928,
            'user': 'uboot',
            'uid': 26299,
            'version': '2',
            'lat': 41.9747374,
            'lon': -87.6920102,
            'timestamp': '2010-07-22T16:16:51Z',
            'changeset': 5288876},
   'node_tags': [{'id': 757860928,
                  'key': 'amenity',
                  'value': 'fast_food',
                  'type': 'regular'},
                 {'id': 757860928,
                  'key': 'cuisine',
                  'value': 'sausage',
                  'type': 'regular'},
                 {'id': 757860928,
                  'key': 'name',
                  'value': "Shelly's Tasty Freeze",
                  'type': 'regular'}]}

### If the element top level tag is "way":
The dictionary has the format {"way": ..., "way_tags": ..., "way_nodes": ...}

The "way" field holds a dictionary of the following top level way attributes,
all other attributes are ignored:
- id
- user
- uid
- version
- timestamp
- changeset

The "way_tags" field again holds a list of dictionaries, following the same
rules as for "node_tags".

Additionally, the dictionary has a field "way_nodes". "way_nodes" holds a list
of dictionaries, one for each nd child tag. Each dictionary has the fields:
- id: the top level element (way) id
- node_id: the ref attribute value of the nd tag
- position: the index starting at 0 of the nd tag i.e. what order the nd tag
    appears within the way element

The final return value for a "way" element looks like:

  {'way': {'id': 209809850,
           'user': 'chicago-buildings',
           'uid': 674454,
           'version': '1',
           'timestamp': '2013-03-13T15:58:04Z',
           'changeset': 15353317},
   'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
                 {'id': 209809850, 'node_id': 2199822390, 'position': 1},
                 {'id': 209809850, 'node_id': 2199822392, 'position': 2},
                 {'id': 209809850, 'node_id': 2199822369, 'position': 3},
                 {'id': 209809850, 'node_id': 2199822370, 'position': 4},
                 {'id': 209809850, 'node_id': 2199822284, 'position': 5},
                 {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
   'way_tags': [{'id': 209809850,
                 'key': 'housenumber',
                 'type': 'addr',
                 'value': '1412'},
                {'id': 209809850,
                 'key': 'street',
                 'type': 'addr',
                 'value': 'West Lexington St.'},
                {'id': 209809850,
                 'key': 'street:name',
                 'type': 'addr',
                 'value': 'Lexington'},
                {'id': '209809850',
                 'key': 'street:prefix',
                 'type': 'addr',
                 'value': 'West'},
                {'id': 209809850,
                 'key': 'street:type',
                 'type': 'addr',
                 'value': 'Street'},
                {'id': 209809850,
                 'key': 'building',
                 'type': 'regular',
                 'value': 'yes'},
                {'id': 209809850,
                 'key': 'levels',
                 'type': 'building',
                 'value': '1'},
                {'id': 209809850,
                 'key': 'building_id',
                 'type': 'chicago',
                 'value': '366409'}]}

NOTE: The concept of this code was taken from Udacity's OpenStreetMap Case
Study Lesson and Quizzes.
"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema
import audit

OSM_PATH = "london_sample.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql
# table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset',
               'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS,
                  way_attr_fields=WAY_FIELDS, problem_chars=PROBLEMCHARS,
                  default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []

    if element.tag == 'node':
        node_atts = element.attrib
        node_children = element.getchildren()
        for field in node_attr_fields:
            if field not in node_atts and field == 'user':
                node_attribs[field] = 'NO_USER'
            elif field not in node_atts and field == 'uid':
                node_attribs[field] = 0
            else:
                node_attribs[field] = node_atts[field]

            if len(node_children) == 0:
                tags = []
            else:
                for child in node_children:
                    child_dict = {}
                    child_atts = child.attrib
                    for field in NODE_TAGS_FIELDS:
                        if field == 'id':
                            child_dict[field] = node_atts[field]
                        elif field == 'key':
                            if ':' in child_atts['k']:
                                child_dict['type'], child_dict[field] = \
                                    child_atts['k'].split(':', 1)
                            else:
                                child_dict[field] = child_atts['k']
                                child_dict['type'] = 'regular'
                        elif field == 'value':
                            if audit.is_street_name(child):
                                child_dict[field] = audit.update_name(
                                    child_atts['v'], audit.mapping)
                            elif audit.is_up_for_fixing(child):
                                child_dict[field] = audit.fix(child_atts['v'])
                            else:
                                child_dict[field] = child_atts['v']
                    tags.append(child_dict)
        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':
        way_atts = element.attrib
        way_children = element.getchildren()
        for field in way_attr_fields:
            way_attribs[field] = way_atts[field]
            if len(way_children) == 0:
                tags = []
                way_nodes = []
            else:
                counter = 0
                for child in way_children:
                    if child.tag == 'tag':
                        child_dict = {}
                        child_atts = child.attrib
                        for field in WAY_TAGS_FIELDS:
                            if field == 'id':
                                child_dict[field] = way_atts[field]
                            elif field == 'key':
                                if ':' in child_atts['k']:
                                    child_dict['type'], child_dict[field] = \
                                        child_atts['k'].split(':', 1)
                                else:
                                    child_dict[field] = child_atts['k']
                                    child_dict['type'] = 'regular'
                            elif field == 'value':
                                if audit.is_street_name(child):
                                    child_dict[field] = audit.update_name(
                                        child_atts['v'], audit.mapping)
                                elif audit.is_up_for_fixing(child):
                                    child_dict[field] = audit.fix(
                                        child_atts['v'])
                                else:
                                    child_dict[field] = child_atts['v']
                        tags.append(child_dict)
                    elif child.tag == 'nd':
                        child_dict = {}
                        child_atts = child.attrib
                        for field in WAY_NODES_FIELDS:
                            if field == 'id':
                                child_dict[field] = way_atts[field]
                            elif field == 'node_id':
                                child_dict[field] = child_atts['ref']
                            else:
                                child_dict[field] = counter
                                counter += 1
                        way_nodes.append(child_dict)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = """\nElement of type '{0}' has the following errors:
                            \n{1}"""
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v
            in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
        codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
        codecs.open(WAYS_PATH, 'w') as ways_file, \
        codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
        codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file,
                                             NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
