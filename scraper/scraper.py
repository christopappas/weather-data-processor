#!/usr/bin/env python
# encoding: utf-8

import logging
from lxml import etree
import re
import requests


import sys

logger = logging.getLogger(__name__)

def scrape(url):
    '''

    :param args: A URL to an xml file
    :return:
    '''

    try:
        r = requests.get(url)
        code = r.status_code
        if code == 200:
            logger.info("200 response from {}".format(url))
            return r
        else:
            # we're not interested in non 200 codes
            logger.warning("Non-200 response from {}".format(url))
            return None

    except Exception as e:
        #if url is badly formed or something
        logger.critical("Something went wrong when trying to scrape: "
            "{}".format(e)
            )
        raise e

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

    return xml_clean

def get_data(url):
    '''
    A wrapper for scrape and extract_xml_and_clean
    :param url: A valid weather url
    :return:
    '''

    return extract_xml_and_clean(scrape(url))

def convert_xml_to_dict(xml):
    '''
    Take clean xml object and take relevant fields
    and put it into a dictionary

    Helper functions here would be overkill.
    :param xml:
    :return:
    '''
    datadict = {}

    # Splitting up data extraction from dictionary insertion in case
    # there needs to be any formatting done
    extraction = xml.find('credit').text
    datadict['credit'] = extraction

    extraction = xml.find('suggested_pickup').text
    datadict['suggested_pickup'] = extraction

    extraction = xml.find('suggested_pickup_period').text
    datadict['suggested_pickup_period'] = extraction

    extraction = xml.find('location').text
    datadict['location'] = extraction

    extraction = xml.find('station_id').text
    datadict['station_id'] = extraction

    extraction = xml.find('latitude').text
    datadict['latitude'] = extraction

    extraction = xml.find('longitude').text
    datadict['longitude'] = extraction

    extraction = xml.find('observation_time').text
    datadict['observation_time'] = extraction

    extraction = xml.find('observation_time_rfc822').text
    datadict['observation_time_rfc822'] = extraction

    extraction = xml.find('weather').text
    datadict['weather'] = extraction

    extraction = xml.find('temp_f').text
    datadict['temp_f'] = extraction

    extraction = xml.find('temp_c').text
    datadict['temp_c'] = extraction

    extraction = xml.find('relative_humidity').text
    datadict['relative_humidity'] = extraction

    extraction = xml.find('wind_dir').text
    datadict['wind_dir'] = extraction

    extraction = xml.find('wind_degrees').text
    datadict['wind_degrees'] = extraction

    extraction = xml.find('wind_mph').text
    datadict['wind_mph'] = extraction

    extraction = xml.find('wind_gust_mph').text
    datadict['wind_gust_mph'] = extraction

    extraction = xml.find('wind_kt').text
    datadict['wind_kt'] = extraction

    extraction = xml.find('wind_gust_kt').text
    datadict['wind_gust_kt'] = extraction

    extraction = xml.find('pressure_mb').text
    datadict['pressure_mb'] = extraction

    extraction = xml.find('pressure_in').text
    datadict['pressure_in'] = extraction

    extraction = xml.find('dewpoint_f').text
    datadict['dewpoint_f'] = extraction

    extraction = xml.find('dewpoint_c').text
    datadict['dewpoint_c'] = extraction

    extraction = xml.find('windchill_f').text
    datadict['windchill_f'] = extraction

    extraction = xml.find('windchill_c').text
    datadict['windchill_c'] = extraction

    extraction = xml.find('visibility_mi').text
    datadict['visibility_mi'] = extraction

    return datadict


if __name__ == "__main__":
    url = sys.argv[1]
    scrape(url)