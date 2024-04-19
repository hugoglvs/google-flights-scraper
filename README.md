# google-flights-scraping

This Python module uses Playwright to scrape flight data from Google Flights. It automates the process of searching for flights based on user input parameters such as origin, destination, departure date, and number of passengers. The scraped data includes detailed flight information, such as prices, dates, companies, duration, stops, emissions, and more.
The current script was inspired from [Arthur Chukhrai's article on scraping Google Flights with Python](https://dev.to/chukhraiartur/scrape-google-flights-with-python-4dln).

## Features

- **Automated Scraping**: Automates the retrieval of flight information from Google Flights.
- **Customizable Search**: Allows specifying various parameters like departure and destination cities, dates, and number of passengers.
- **Detailed Flight Data**: Retrieves comprehensive details about each flight option available.
- **Production Ready**: Includes production-specific configurations for optimal performance.
- **Command-Line Interface**: Provides a CLI tool for easy interaction with the scraper.
- **Configurable Options**: Supports various options like verbose output, headless mode, and pretty printing of JSON output.

## Prerequisites

Before you begin using this module, ensure you have the following installed:

- Python 3.7 or higher
- Playwright
- Selectolax
- Click

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/kurouge/google-flights-scraping.git
cd google-flights-scraping
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Module Usage

To use the module, you need to provide the parameters for your flight search. Here is an example of how to run the script:

```python
from google_flights import GoogleFlights

# Set your flight search parameters
origin = 'New York'
destination = 'London'
departure_date = '2024-09-15'
passengers = 1

scraper = GoogleFlights(headless=True)
results = scraper.search(origin, destination, departure_date, passengers)
results_json = json.dumps(results, indent=4)
print(results_json)
```

### CLI Usage

The module also includes a command-line interface (CLI) for interacting with the Google Flights scraper without directly using Python scripts. This can be especially useful for automating tasks or integrating the scraper into larger workflows.

### Installation

Ensure the CLI script is executable:

```python
chmod +x /path/to/google-flights-scraping/bin/cli_script.py
```

### Available Options

You can configure the following options via the command line:

- `--origin, -o`: Set the departure city (required).
- `--destination, -a`: Set the destination city (required).
- `--departure-date, -dd`: Set the departure date in DD-MM-YYYY format. Defaults to three days from the current date.
- `--passengers, -p`: Specify the number of passengers. Defaults to 1.
- `--verbose, -v`: Enable verbose output for more detailed logs.
- `--headless, -hl`: Run the browser in headless mode for a headless server environment.
- `--pretty, -pr`: Enable pretty printing of the output JSON.

### Running the CLI

To run the CLI tool, use the following command format:

```bash
/path/to/google-flights-scraping/cli_script.py --origin "New York" --destination "London" --departure-date "15-09-2024" --passengers 2 --verbose --headless --pretty
```

This command will search for flights from New York to London on September 15, 2024, for 2 passengers, with verbose, headless and pretty modes enabled.

## Configuration for production

In a production environment, make the following adjustments to the code:

- Reduce slow_mo for faster execution.
- Comment out debug statements and unnecessary time.sleep() calls except where absolutely necessary.

## Contributing

Contributions to this module are welcome. Please follow the standard procedures by forking the repository, making your changes, and submitting a pull request for review.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - hugoglvs@icloud.com - [Hugo Gonçalves]
Project Link: https://github.com/hugoglvs/google_flights_scraper
