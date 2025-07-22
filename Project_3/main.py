"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Nela Friedlová
email: nela.friedl@gmail.com
"""

from requests import get, exceptions
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import csv
import argparse
import os
import re

ELECTIONS_URL = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

def main(location: str, csv_file: str):
    """
    Directs the individual steps of election data scraping for a given location 
    and saves it into a new CSV file.

    Args:
        location (str): The name of the location/district for which to scrape election results (e.g., "Praha").
        csv_file (str): The desired name of the CSV file to save the results (e.g., "Praha_elections.csv").
    """
    print(f"Collecting data for location: '{location}'.")

    location_url = find_url(location)    # find URL of specified location
    if not location_url:
        print(f"Could not find the URL for location '{location}'.")
        return
    
    cities_url_code = find_city_urls(location_url)    # find URLs of cities in a given location
    if not cities_url_code:
        print(f"No city data found for location '{location}'. Cannot proceed with data collection.")
    
    election_data, party_names = scrape_city_election_data(cities_url_code)    # get data from all cities    
    if not election_data:
        print("No election data was scraped from cities. Nothing to save.")
        return
    
    create_csv_file(election_data, party_names, csv_file)

def url_upload(url: str) -> bs | None:
    """
    Loads URL content, handles potential errors, and returns a BeautifulSoup object.
    
    Args: 
        url (str): URL address for data mining.

    Returns:
        BeautifulSoup | None: A BeautifulSoup object if successful, None otherwise.

    """
    try:
        response = get(url, timeout=15)
        if response.status_code == 200:
            response.encoding = "utf-8"
            return bs(response.text, features="html.parser")
        else:
            print(f"Error: Request to '{url}' returned status code {response.status_code}.")
            return None
    except exceptions.RequestException as e:
        print(f"Error: Network or connection issue for URL '{url}': {e}")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None

def find_url(location: str) -> str | None:
    """
    Searches the URL for the given location.
    
    Args:
        location (str): The name of the location (e.g., "Praha").

    Returns:
        str | None: The absolute URL of the location's overview page if found, None otherwise.
    """
    source_url_soup = url_upload(ELECTIONS_URL)
    if not source_url_soup:
        print(f"Could not load the main election page: {ELECTIONS_URL}")
        return None

    all_tables = source_url_soup.find_all('table')      # Finds all <table> elements on the page

    for table in all_tables:
        location_td = table.find('td', string=lambda text: text and text.strip() == location)
        
        if location_td:
            parent_row = location_td.find_parent('tr')
            if parent_row:
                all_tds = parent_row.find_all('td')
                if len(all_tds) > 3:
                    url_td = all_tds[3]
                    link_tag = url_td.find('a', href=True) # Ensure it has an href attribute
                    if link_tag:
                        relative_url = link_tag['href']
                        absolute_url = urljoin(ELECTIONS_URL, relative_url)
                        return absolute_url

    print(f"Overview URL for '{location}' not found on {ELECTIONS_URL}.")
    return None

def find_city_urls(location_url: str) -> list[dict[str, str]]:
    """
    Takes the URL of a given location and extracts links to individual city election results.
    
    Args: 
        location_url (str): The URL of the location's election results.
    
    Returns:
        list[dict[str, str]]: A list of dictionaries, where each dictionary contains
                              'url' (absolute URL) and 'code' (city code) for each city.    
    """
    location_url_soup = url_upload(location_url)
    if not location_url_soup:
        print(f"Could not load location page.")
        return []
    
    city_data = []
    all_tables = location_url_soup.find_all('table')

    for table in all_tables:
        for row in table.find_all('tr'):          
            link_td = row.find('td', class_="cislo")
            if link_td:
                link_tag = link_td.find('a', href=True)
                if link_tag:
                    relative_url = link_tag['href']
                    absolute_url = urljoin(location_url, relative_url) 
                    city_code = link_tag.get_text(strip=True)  

                    if absolute_url and city_code:
                        city_data.append({
                            'url': absolute_url,
                            'code': city_code
                        })                                  
    return city_data

def scrape_city_election_data(cities_url_code: list[dict[str, str]]) -> tuple[list[dict], set[str]]:
    """
    Retrieves election data (city code, name, number of voters, envelopes, valid votes, and party votes)
    from individual city URLs.

    Args:
        cities_url_code (list): A list of dicts, where each contains 'url' and 'code' for each city.
    
    Returns:
        tuple[list[dict], set[str]]: A tuple containing a list of dicts, each with city and party data,
                                                        a set of party names.
    """
    all_extracted_data = []
    party_names = set()
    
    for city_info in cities_url_code:
        city_url = city_info['url']
        city_code = city_info['code']
        city_data_soup = url_upload(city_url)

        city_specific_data = {
            'code': city_code,
            'city': None,
            'reg_voters': None,
            'num_envelopes': None,
            'num_valid_votes': None
        }

        # extract City Name
        city_name_h3 = city_data_soup.find('h3', string=lambda text: text and "Obec:" in text)
        if city_name_h3:
            city_specific_data["city"] = city_name_h3.get_text(strip=True).replace("Obec:", "").strip()

        # extract general data
        data_table = city_data_soup.find('table')   # the first table contains general election data
        if data_table:
            rows = data_table.find_all('tr')
            if len(rows) > 2:   
                target_row = rows[2]    # the third row contains the relevant data
                tds = target_row.find_all('td')     # get all td elements in the row
                
                if len(tds) > 3:
                    city_specific_data["reg_voters"] = tds[3].get_text(strip=True).replace('\xa0', '')

                if len(tds) > 4:
                    city_specific_data["num_envelopes"] = tds[4].get_text(strip=True).replace('\xa0', '')

                if len(tds) > 7:
                    city_specific_data["num_valid_votes"] = tds[7].get_text(strip=True).replace('\xa0', '')
        else:
            print(f"No general data table found for city {city_code}.")
       
        # extract party names and number of votes
        current_city_party_votes = {}   
        party_tables = city_data_soup.find_all('table')

        for party_table in party_tables:
            party_td = party_table.find('td', class_='overflow_name')   # search for table with party data
            if party_td:
                for row in party_table.find_all('tr'):
                    tds = row.find_all('td')    

                    if len(tds) >= 3:        
                        party_name_td = tds[1]  # party name in column 2 (index 1)
                        votes_td = tds[2]       # votes in column 3 (index 2)

                        party_name = party_name_td.get_text(strip=True)
                        cleaned_party_name = party_name.strip()     

                        votes = votes_td.get_text(strip=True).replace('\xa0', '')

                        if cleaned_party_name and votes:
                            current_city_party_votes[cleaned_party_name] = votes
                            party_names.add(cleaned_party_name)     # collect all unique party names
        
        city_specific_data.update(current_city_party_votes)    # merge general data and party-specific votes
        all_extracted_data.append(city_specific_data)          # add all data from the current city

    return all_extracted_data, party_names

def validate_filename(filename: str) -> str:
    """
    Validates a filename for prohibited characters.

    Args:
        filename (str): The filename string to validate.

    Returns:
        str: The original filename if valid.
    """
    prohibited_chars_pattern = r'[<>:"/\\|?*\x00-\x1F]'   # \x00-\x1F refer to ASCII control characters

    if re.search(prohibited_chars_pattern, filename):
        raise argparse.ArgumentTypeError(
            f"Filename '{filename}' contains prohibited characters.\nProhibited characters include: < > : \" / \\ | ? * and control characters."
        )
    return filename

def get_unique_filename(filename: str) -> str:
    """
    Generates a unique filename by appending a number if the user-specified name already exists.

    Args:
        filename (str): The desired filename (e.g., "Praha_elections.csv").

    Returns:
        str: A unique filename (e.g., "Praha_elections.csv", "Praha_elections_2.csv").
    """
    if not os.path.exists(filename):
        return filename

    name, ext = os.path.splitext(filename)
    index = 1
    while True:
        index += 1
        new_filename = f"{name}_{index}{ext}"
        if not os.path.exists(new_filename):
            return new_filename

def create_csv_file(data: list[dict], parties: set[str], csv_file_name: str):
    """
    Saves the extracted data to a CSV file.
    
    Args:
        data (list[dict]): A list of dicts, each dict represents a row of city-specific data.
        parties (set[str]): A set of all unique party names.
        csv_file_name (str): The name of the CSV file.
    """ 
    if not data:
        print("No data extracted to save to CSV.")
        return
    unique_filename = get_unique_filename(csv_file_name)
    headers = ['code', 'city', 'reg_voters', 'num_envelopes', 'num_valid_votes']
    sorted_party_names = sorted(list(parties))
    headers.extend(sorted_party_names)

    if data:
        try:
            with open(unique_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader() # Write the header row
                for row_data in data:
                    full_row = {header: row_data.get(header) for header in headers}
                    writer.writerow(full_row)    
            print(f"Data successfully saved to {unique_filename}.")
        except IOError as e:
            print(f"Error writing to CSV file {unique_filename}: {e}")
    else:
        print("No data extracted to save to CSV.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape election data from a given Czech location and save to a CSV file.")
    parser.add_argument("location", 
                        type=str,
                        help="The name of district/region for which to scrape election results (e.g., 'Praha').")
    parser.add_argument("output_file", 
                        type=validate_filename,
                        help="The name of the CSV file to save the results (e.g., 'Praha_elections.csv').")
    
    args = parser.parse_args()

    main(args.location, args.output_file)    # call the main function with parsed arguments