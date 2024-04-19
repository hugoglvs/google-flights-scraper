"""
google_flights_scraper - A Python package for scraping flight data from Google Flights.

This package provides easy-to-use tools to interact with Google Flights to fetch flight
details like prices, emissions, durations, and stops programmatically using Python scripts.
"""

__author__ = """hugoglvs (Hugo Gonçalves)"""
__email__ = 'hugoglvs@icloud.com'
__version__ = '0.0.1'

from playwright.sync_api import sync_playwright
from selectolax.lexbor import LexborHTMLParser
from .google_flights import GoogleFlights


__all__ = ['GoogleFlights']
