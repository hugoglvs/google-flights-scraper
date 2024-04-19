from playwright.sync_api import sync_playwright
from selectolax.lexbor import LexborHTMLParser
import json
import time

class GoogleFlights:
    """Class to interact with Google Flights for fetching flight data

    Attributes:
        headless (bool): Run in headless mode (no visible browser)
    """

    def __init__(self, headless=True):
        self.headless = headless

    def _get_page(self, origin, destination, departure_date, passengers=1):
        """
        Navigate to the Google Flights page and input flight search parameters.

        Args:
            origin (str): Departure city.
            destination (str): Arrival city.
            departure_date (str): Date of departure.
            passengers (int): Number of passengers.

        Returns:
            page: A playwright page instance after loading search results.
        """
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=self.headless, slow_mo=100)
            page = browser.new_page()

            try:
                # Navigation to Google Flights page
                page.goto("https://www.google.com/travel/flights?hl=fr&curr=EUR")

                # Cookie acceptance
                accept_cookies_selector = "text='Tout accepter'"
                page.wait_for_selector(accept_cookies_selector, timeout=10000)
                page.click(accept_cookies_selector)

                # Select ticket type
                page.get_by_role("combobox", name="Modifier le type de billet. ​").locator("div").click()
                time.sleep(0.4)
                page.get_by_role("option", name="Aller simple").click()


                # Set number of passengers
                page.get_by_label("1 passager").click()
                page.get_by_label("Nombre de passagers adultes").get_by_text("1").click()
                page.get_by_label("Ajouter un adulte").click(click_count=passengers-1)

                # Set origin
                page.get_by_label("D'où partez-vous ?").click()
                page.get_by_label("Autres points de départ ?").fill(origin)
                page.get_by_label("Autres points de départ ?").press("Enter")
                # page.get_by_role("combobox", name="D'où partez-vous ?").fill(origin)
                # page.get_by_role("combobox", name="D'où partez-vous ?").press("Enter")


                # Set destination
                page.get_by_role("combobox", name="Où allez-vous ?").click()
                page.get_by_role("combobox", name="Où allez-vous ?").fill(destination)
                page.get_by_role("combobox", name="Où allez-vous ?").press("Enter")
                time.sleep(0.4)


                # Set departure date
                page.get_by_role("textbox", name="Départ").click()
                page.get_by_role("textbox", name="Départ").fill(departure_date)
                page.get_by_role("textbox", name="Départ").press("Enter")
                time.sleep(0.7)

                # Start search
                page.get_by_label("OK. Rechercher un aller").click()
                page.get_by_label("Rechercher", exact=True).click()
                time.sleep(1)

                # Ensure search results are loaded
                results_selector = "[jscontroller='muK14'] .VfPpkd-RLmnJb"
                page.wait_for_selector(results_selector, state="visible", timeout=3000)
                locators = page.locator(results_selector).all()
                for locator in locators:
                    locator.click()

                # Final content retrieval
                page.pause()
                return page.content()

            except TimeoutError as e:
                print("A timeout error occurred:", e)
                return None
            except Exception as e:
                print("An unexpected error occurred:", e)
                return None
            finally:
                # Ensure the browser is closed properly
                browser.close()



    def _parse(self, page_content):
        parser = LexborHTMLParser(page_content)
        data = {}
        categories = parser.root.css('.zBTtmb')
        category_results = parser.root.css('.Rk10dc')

        for category, category_result in zip(categories, category_results):
            category_data = []
            for result in category_result.css('.pIav2d'):
                main_information = result.css_first('.yR1fYc')
                if main_information is None:
                    continue  # Skip this iteration if main_information is not found

                date = main_information.css('[jscontroller="cNtv4b"] span') if main_information.css('[jscontroller="cNtv4b"] span') else None
                departure_date = date[0].text() if date else None
                arrival_date = date[1].text() if date else None
                company = main_information.css_first('.Ir0Voe .sSHqwe').text() if main_information.css_first('.Ir0Voe .sSHqwe') else None
                duration = main_information.css_first('.AdWm1c.gvkrdb').text() if main_information.css_first('.AdWm1c.gvkrdb') else None
                stops = main_information.css_first('.EfT7Ae .ogfYpf').text() if main_information.css_first('.EfT7Ae .ogfYpf') else None
                emissions = main_information.css_first('.V1iAHe .AdWm1c').text() if main_information.css_first('.V1iAHe .AdWm1c') else None
                emission_comparison = main_information.css_first('.N6PNV').text() if main_information.css_first('.N6PNV') else None
                price = main_information.css_first('.U3gSDe .FpEdX span').text() if main_information.css_first('.U3gSDe .FpEdX span') else 0
                price_type = main_information.css_first('.U3gSDe .N872Rd').text() if main_information.css_first('.U3gSDe .N872Rd') else None

                extra_information = result.css_first('.m9ravf .xOMPfb.MNvMJb')
                if extra_information is None:
                    continue  # Skip this iteration if extra_information is not found
                trips = extra_information.css(".c257Jb.eWArhb") if extra_information.css(".c257Jb.eWArhb") else None
                if trips:
                    departure_airport = trips[0].css_first(".FFbonc .dPzsIb span[dir='ltr']").text()[1:-1]
                    airports = [departure_airport]
                    for trip in trips:
                        intermediate_airports = trip.css_first(".FFbonc .SWFQlc span[dir='ltr']").text()[1:-1] if trip.css_first(".FFbonc .SWFQlc span[dir='ltr']") else None
                        airports.append(intermediate_airports)
                else:
                     airports = None

                flight_data = {
                    'departure_date': departure_date,
                    'arrival_date': arrival_date,
                    'company': company,
                    'duration': duration,
                    'stops': stops,
                    'emissions': emissions,
                    'emission_comparison': emission_comparison,
                    'price': price,
                    'price_type': price_type,
                    'airports': airports
                }


                category_data.append(flight_data)
            data[category.text().lower().replace(' ', '_')] = category_data
        return data

    def search(self, origin, destination, departure_date, passengers=1):
        """
                Search for flights using specified parameters and scrape the results.

                Args:
                    origin (str): Departure city.
                    destination (str): Arrival city.
                    departure_date (str): Date of departure.
                    passengers (int): Number of passengers.

                Returns:
                    dict: Parsed flight data.
                """
        page = self._get_page(origin, destination, departure_date, passengers)
        results = self._parse(page)
        return results

if __name__ == "__main__":
    flights = GoogleFlights(headless=False)
    result = flights.search("Paris", "Lisbon", "2024-05-03", 3)
    result_json = json.dumps(result, ensure_ascii=False, indent=4)
    print(result_json)
