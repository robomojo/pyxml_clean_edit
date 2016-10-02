import xml.etree.ElementTree as ET
import xml.dom.minidom

from . import utils
reload(utils)

def add(file_path, elements, parent_element_tag):
    '''
    '''
    # guard against common exceptions
    utils.guard(file_path, parent_element_tag)
    # get the sourcelines
    srclines = utils.get_sourcelines_of_element(file_path, parent_element_tag, {})
    srclines.insertion_mode = utils.EnumInsertionMode.End
    # get a list of lines
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # reverse elements, as we will be inserting them into the same index
    elements.reverse()
    # derive leading space from previous line
    leading_space = utils.get_leading_whitespace(lines[srclines.get_insertion_index() - 1])
    # get the clip as a list
    for xml_element in elements:
        str_element = utils.get_parsed_xml(xml_element, leading_space=leading_space)
        lines.insert(srclines.get_insertion_index(), str_element)
    # write it back
    with open(file_path, 'w') as f:
        f.write(''.join(lines))

def remove(file_path=None, tag_matches=None, attrib_matches=None, parent_element_tag=None):
    '''
    Remove certain elements from the file.
    '''
    # guard against common exceptions
    utils.guard(file_path, parent_element_tag)
    # ensure arg types
    tag_matches = utils.handle_tag_matches(tag_matches)
    attrib_matches = utils.handle_attrib_matches(attrib_matches)
    srcline_objs = []
    for tag in tag_matches:
        for attrib in attrib_matches:
            srclines = utils.get_sourcelines_of_element(file_path, tag, attrib)
            srcline_objs.append(srclines)
    # get a list of lines
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # reverse srcline_objs as we will now go and remove the lines
    srcline_objs.reverse()
    # pop all the lines inbetween start and end
    for srclines in srcline_objs:
        if srclines.is_multiline():
            del lines[srclines.start:srclines.end]
        else:
            del lines[srclines.start]
    # write it back
    with open(file_path, 'w') as f:
        f.write(''.join(lines))

def replace_children(file_path, elements, parent_element_tag):
    '''
    Replace all the child elements of parent_element_tag.
    '''
    # guard against common exceptions
    utils.guard(file_path, parent_element_tag)
    # get the sourcelines
    srclines = utils.get_sourcelines_of_element(file_path, parent_element_tag, {})
    # get a list of lines
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # reverse elements, as we will be inserting them into the same index
    elements.reverse()
    # derive leading space from target line
    leading_space = utils.get_leading_whitespace(lines[srclines.get_insertion_index()])
    # pop all the lines inbetween start and end
    del lines[srclines.start+1:srclines.end]
    # get the clip as a list
    for xml_element in elements:
        str_element = utils.get_parsed_xml(xml_element, leading_space=leading_space)
        lines.insert(srclines.get_insertion_index(), str_element)
    # write it back
    with open(file_path, 'w') as f:
        f.write(''.join(lines))
