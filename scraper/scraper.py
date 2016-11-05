#!/usr/bin/env python
# encoding: utf-8

from lxml import etree
import re
import requests


import sys


def scrape(url):
    '''

    :param args: A URL to an xml file
    :return:
    '''

    try:
        r = requests.get(url)
        code = r.status_code
        if code == 200:
            print(url)
            return r
        else:
            # we're not interested in non 200 codes
            return None
            # ADD SOMETHING HERE AS LOG INFORMATION

    except Exception as e:
        #if url is badly formed or something
        print("Something went wrong when trying to scrape.")
        raise e
        # ADD SOMETHING HERE AS LOG INFORMATION

def extract_xml_and_clean(response):
    '''
    Grab xml from a response object and clean it
    :param data: GET response object
    :return:
    '''

    xml_dirty = response.text
    # lxml chokes if encoding is specified in XML, so strip it out
    xml_dirty = re.sub('encoding="ISO-\d\d\d\d-\d"', "", xml_dirty)

    # Consider also dropping all \n \t \r

    xml_clean = etree.fromstring(xml_dirty)
    print(type(xml_clean))
    return xml_clean

def get_data(url):
    '''
    A wrapper for scrape and extract_xml_and_clean
    :param url: A valid weather url
    :return:
    '''

    return extract_xml_and_clean(scrape(url))



if __name__ == "__main__":
    url = sys.argv[1]
    scrape(url)