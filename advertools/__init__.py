# -*- coding: utf-8 -*-

"""Top-level package for advertools."""

__author__ = """Elias Dabbas"""
__email__ = 'eliasdabbas@gmail.com'
__version__ = '0.3.0'

from advertools.ad_create import ad_create
from advertools.ad_from_string import ad_from_string
from advertools.extract import extract_mentions, extract_hashtags, extract_emoji
from advertools.kw_generate import *
from advertools.stopwords import stopwords
from advertools.url_builders import url_utm_ga
from advertools.word_frequency import word_frequency
from . import twitter
from .twitter import FUNCTIONS
