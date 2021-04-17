import requests
from bs4 import BeautifulSoup, SoupStrainer
from icecream import ic
import time

lc_st = "United KingdomCambridge"


def split_location_string(location):
    """
    Split location string into a list [Country, City]
    "United KingdomCambridge" -> ['United Kingdom', 'Cambridge']
    """
    for char_pos, char in enumerate(location):
        if char.isupper() and char_pos != 0:
            if location[char_pos - 1].islower():
                return [location[:char_pos], location[char_pos:]]


def parse_info():
    """
    Scrape reviews from book's Goodreads webpage using BeautifulSoup 4.
    Return a list of tuples (names,rating,reviews)
    """
    requests_session = requests.Session()  # Launch a requests session in order to improve performance

    page = 1
    page_url = f"https://erasmusintern.org/traineeships?f%5B0%5D=field_traineeship_field_studies%253Aparents_all%3A38&page={page}"
    webpage = requests_session.get(page_url)
    soup = BeautifulSoup(webpage.content, "lxml")

    data_list = []

    last_page = int(soup.find('a', title="Go to last page").attrs["href"][-2:])
    while page <= last_page:
        # print(page, page_url)
        page_url = f"https://erasmusintern.org/traineeships?f%5B0%5D=field_traineeship_field_studies%253Aparents_all%3A38&page={page}"
        webpage = requests_session.get(page_url)
        soup = BeautifulSoup(webpage.content, "lxml")

        page += 1

        titles_raw = soup.find_all('div', class_="ds-header")
        titles = [title.text.strip() for title in titles_raw]

        subtitles_raw = soup.find_all('div', class_="ds-top-content")
        subtitles = [subtitle.text.strip() for subtitle in subtitles_raw]

        recruiters_raw = soup.find_all('div', class_="field-name-recruiter-name") 
        recruiters = [recruiter.text.strip() for recruiter in recruiters_raw]

        locations_raw = soup.find_all('div', class_="field-name-field-traineeship-full-location")
        locations = [split_location_string(location.text) for location in locations_raw]

        durations_raw = soup.find_all('div',
                                      class_="field-name-field-traineeship-duration")
        durations = [duration.text.strip()[10:] for duration in durations_raw]

        deadlines_raw = soup.find_all('div', class_="field-name-field-traineeship-apply-deadline")
        deadlines = [deadline.text.strip()[10:] for deadline in deadlines_raw]

        full_info_links_raw = soup.find_all('a', text="Read more")
        full_info_links = [full_info_link.attrs["href"] for full_info_link in full_info_links_raw]
        # ic(full_info_links)
        info_link_base = "https://erasmusintern.org"

        periods = []
        requirements = []
        for full_info_link in full_info_links:
            full_info_webpage = requests_session.get(info_link_base + full_info_link)
            # print(info_link_base+ full_info_link)
            soup = BeautifulSoup(full_info_webpage.content, "lxml")
            period = soup.find('span', class_="date-display-range").text.strip()
            periods.append(period)

            requirement = soup.find('div', class_="panel-body")
            if requirement:
                requirements.append(requirement.text.strip())
            else:
                requirements.append(None)


        full_info = list(zip(titles, subtitles, recruiters, locations, durations, deadlines, periods, requirements))
        for offer in full_info:
            offer_dict = {"title": offer[0], "subtitle": offer[1], "recruiter": offer[2],
                          "full_location": offer[3], "duration": offer[4], "deadline": offer[5],
                          "periods": offer[6], "requirements": offer[7]}
            data_list.append(offer_dict)
    return data_list
# print(parse_info())


