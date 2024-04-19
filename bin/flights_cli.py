#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""CLI Tool for scraping Google Flights using the GoogleFlights class"""
import sys, os
import click
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from google_flights.google_flights import GoogleFlights  # Ensure correct import path based on your project structure

# Usage: google_flights_cli.py --help

@click.command()
@click.option(
    '--origin', '-o',
    type=str,
    help='Origin city (example: Paris)',
    required=True,
)
@click.option(
    '--destination', '-d',
    type=str,
    help='Destination city (example: Lisbon)',
    required=True,
)
@click.option(
    '--departure-date', '-dd',
    type=str,
    help='Departure date (format: DD-MM-YYYY)',
    default=(datetime.now() + timedelta(days=3)).strftime("%d-%m-%Y"),
    show_default=True,
)
@click.option(
    '--passengers', '-p',
    type=int,
    help='Number of passengers',
    default=1,
    show_default=True,
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Verbose mode',
)
@click.option(
    '--headed', '-hd',
    is_flag=True,
    default=False,
    help='Run in headed mode (visible browser) instead of headed mode',
)
@click.option(
    '--pretty', '-pr',
    is_flag=True,
    help='Pretty print JSON output',
)
def main(origin, destination, departure_date, passengers, verbose, headed, pretty):
    if verbose:
        print(f'Searching for flights from {origin} to {destination} on {departure_date} for {passengers} passengers...')

    # Create a GoogleFlights instance with the specified headed mode
    google_flights = GoogleFlights(headless=not headed)

    # Search for flights and obtain results
    results = google_flights.search(origin, destination, departure_date, passengers)

    # Print results in JSON format
    if results:
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2) if pretty else json.dumps(results, ensure_ascii=False))
    else:
        print("No results found or there was an error during the scraping process.")

if __name__ == '__main__':
    main()
