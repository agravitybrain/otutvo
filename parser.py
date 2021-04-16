import requests
from bs4 import BeautifulSoup, SoupStrainer
from icecream import ic
import time

def scrape_reviews(isbn):
    """
    Scrape reviews from book's Goodreads webpage using BeautifulSoup 4.
    Return a list of tuples (names,rating,reviews)
    """
    requests_session = requests.Session()  # Launch a requests session in order to improve performance

    page_url = "https://erasmusintern.org/traineeships?f%5B0%5D=field_traineeship_field_studies%253Aparents_all%3A47"

    webpage = requests_session.get(page_url)

    soup = BeautifulSoup(webpage.content, "lxml")
    # reviews_raw = soup.find_all('div', class_='gr_review_text')
    # reviews = [review.text.strip() for review in reviews_raw]

    titles_raw = soup.find_all('div', class_="ds-header")  # find names of the review authors
    titles = [title.text.strip() for title in titles_raw]

    subtitles_raw = soup.find_all('div', class_="ds-top-content")  # find names of the review authors
    subtitles = [subtitle.text.strip() for subtitle in subtitles_raw    ]
    # print(subtitles)
    recruiters_raw = soup.find_all('div', class_="field-name-recruiter-name")  # find names of the review authors
    recruiters = [recruiter.text.strip() for recruiter in recruiters_raw]

    locations_raw = soup.find_all('div', class_="field-name-field-traineeship-full-location")  # find names of the review authors
    locations = [location.text.strip() for location in locations_raw]

    full_info = list(zip(titles,subtitles, recruiters, locations))
    data_list=[]

    for offer in full_info:
        offer_dict ={"title":offer[0],"subtitle":offer[1], "recruiter": offer[2], "location": offer[3]}
        data_list.append(offer_dict)
    ic(offer_dict)
    print(data_list)
    # durations_raw = soup.find_all('div', class_="field-name-field-traineeship-full-location")  # find names of the review authors
    # locations = [location.text for location in locations_raw]
    # ratings_raw = soup.find_all('span', class_="gr_rating")  # find ratings of the review
    # ratings = [rating.text.count("★") for rating in ratings_raw]  # convert starred rating into integer value
    # ic(ratings, names)
    #
    # start_time = time.time()
    # reviews = []
    # full_review_links = soup.find_all('link',itemprop="url")  # find links to the full reviews
    # only_review_tags = SoupStrainer(itemprop="reviewBody")  # use special bs4 object to load the webpage partially
    # for full_review_link in full_review_links:
    #     ic(full_review_link.attrs["href"])
    #     full_review_webpage = requests_session.get(full_review_link.attrs["href"])
    #     soup = BeautifulSoup(full_review_webpage.content, "lxml", parse_only=only_review_tags)
    #     review_raw_text = soup.find('div', class_="reviewText")  # find full text of the review
    #     reviews.append(review_raw_text.text.strip())  # add review text to the reviews list
    #     ic(time.time() - start_time)
    #     start_time = time.time()
    # full_reviews = list(zip(names, ratings, reviews)) # make a list of tuples containing full info about reviews
    # ic(full_reviews)
    # return full_reviews
    pass
scrape_reviews(9780807014295)