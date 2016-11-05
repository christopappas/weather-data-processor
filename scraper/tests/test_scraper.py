#!/usr/bin/env python
# encoding: utf-8


from lxml import etree
from nose.tools import *
import requests
import vcr

import os

from scraper import scraper

class TestScraper:

    cassette_library_dir = os.path.join(os.path.dirname(__file__), 'files')

    def __init__(self):

        self.good_url = "http://w1.weather.gov/xml/current_obs/KBOS.xml"
        self.bad_url = "ahtdwtp://w1.weather.gov/xml/current_obs/KBOS.xml"
        self.url404 = "http://w1.weather.gov/christopappas_is_the_man"

        self.response200 = self._run_200_get()
        self.response404 = self._run_404_get()

    @vcr.use_cassette(os.path.join(cassette_library_dir, '200_get.yaml'))
    def _run_200_get(self):
        '''
        Helper script to create a good get response object.

        TODO: Use VCR to only run this once!
        :param self:
        :return:
        '''

        r = requests.get(self.good_url)

        return r

    @vcr.use_cassette(os.path.join(cassette_library_dir, '404_get.yaml'))
    def _run_404_get(self):
        '''
        Helper script to create a good get response object.

        TODO: Use VCR to only run this once!
        :param self:
        :return:
        '''

        r = requests.get(self.url404)

        return r

    @vcr.use_cassette(os.path.join(cassette_library_dir, '200_get.yaml'))
    def test_scrape(self):
        '''
        Scrape should return requests object
        :return:
        '''

        response = scraper.scrape(self.good_url)

        assert(isinstance(response, requests.models.Response))

    @vcr.use_cassette(os.path.join(cassette_library_dir, '404_get.yaml'))
    def test_scrape_non200(self):
        '''
        Scrape should throw exception on non 200 response
        :return:
        '''

        response = scraper.scrape(self.url404)

        assert(response == None)

    @raises(Exception)
    def test_scrape_badurl(self):
        '''
        Scrape should throw exception on bad url
        :return:
        '''
        response = scraper.scrape(self.bad_url)


    def test_extract_xml_and_clean(self):
        '''
        Well formed XML should be returned from response object containing XML
        :return:
        '''

        response = self.response200
        xml = scraper.extract_xml_and_clean(response)

        assert(isinstance(xml, etree._Element))