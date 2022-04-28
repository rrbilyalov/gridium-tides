import datetime
import re

from bs4 import BeautifulSoup
import requests


cities = {'Half Moon Bay, California': 'https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest',
          'Huntington Beach, California': 'https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest',
          'Providence, Rhode Island': 'https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest',
          'Wrightsville Beach, North Carolina': 'https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest',
          }

def time_string_adjustment(time_str):
    """Convert instances of '00' hours to '12' hours."""
    
    time_list = list(time_str.partition(':'))
    time_list[0] = time_list[0].replace('00', '12')
    time_str = ''.join(time_list)
    
    return time_str

def get_low_tide_info(url):
    """Get today's day-time low tide height/time for a location.
    
    Given the URL of the tide-forecast.com page for the
    desired location, extract tide information for today's
    date. Only low tide instances between sunrise and
    sunset are included. A tuple is returned with today's
    date and low tide information. For each low tide
    occurrence, the tide height (in feet) and the time of
    are included.
    
    Parameters
    ----------
    url : str
        The URL of the tide-forecast.com page for the desired
        location.
    
    Returns
    -------
    date : str
        Today's date. The format follows this sample:
        'Thursday 28 April 2022'.
    low_tides : list
        Each element is a tuple with the tide height in feet
        (float) and the time (string following this sample:
        '3:48 PM').
    """
    
    # get the HTML of the page as a BeautifulSoup object
    page = BeautifulSoup(requests.get(url).content, 'html.parser')
    
    # first get the summary paragraph and extract the sunrise/sunset times
    summary = page.find('p', class_ = 'tide-header-summary')
    search_object = re.search(r'Sunrise is at (.*) and sunset is at (.*)\.', summary.text)
    if search_object:
        sunrise = search_object.group(1).strip()
        sunrise = datetime.datetime.strptime(time_string_adjustment(sunrise), '%I:%M%p')
        sunset = search_object.group(2).strip()
        sunset = datetime.datetime.strptime(time_string_adjustment(sunset), '%I:%M%p')
    
    # this array will store tuples of height/time for each day-time low tide
    low_tides = []
    
    # the data for today's tide is in a table; we extract the header and the table
    container = page.find('div', class_ = 'tide-header-today tide-header__card')
    header = container.find('h3')
    date = header.text.rpartition(': ')[-1] # today's date
    table = container.find('table')
    
    # extract info from every "low tide" row in the table
    rows = table.find_all('tr')
    for row in rows[1:]: # ignore the header row
        cols = row.find_all('td')
        tide_type = cols[0].text
        tide_time_str = cols[1].text
        tide_height = cols[2].text
        # we only care about low tide
        if not 'low' in tide_type.strip().lower():
            continue
        # check if the time is between sunrise and sunset
        tide_time_str = tide_time_str.partition('(')[0].strip()
        tide_time = datetime.datetime.strptime(time_string_adjustment(tide_time_str), '%I:%M %p')
        if not sunrise <= tide_time <= sunset:
            continue
        tide_height_ft = tide_height.partition('ft')[0].strip()
        low_tides.append((float(tide_height_ft), tide_time_str))
    
    return (date, low_tides)

if __name__ == '__main__':
    date_shown = False
    for location, url in cities.items():
        date, low_tides = get_low_tide_info(url)
        if not date_shown:
            print(f"Data for {date}:")
            date_shown = True
        print(f"  {location}")
        for low_tide in low_tides:
            print(f"    Low tide of {low_tide[0]} ft at {low_tide[1]}")