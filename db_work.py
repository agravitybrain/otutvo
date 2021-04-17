from pymongo import MongoClient
from pprint import pprint
from geopy.geocoders import Nominatim
import parser


connection = 'CONNECTION URL WAS REMOVED DUE TO SAFETY REASONS'
client = MongoClient(connection)
db = client['internships']
collection = db['internship_locations']


def pass_to_db(courses: list):
    ''' Pass courses info to the database '''
    added = 0
    all_courses = 0
    for course in courses:
        if not already_in_db(course):
            coordinates = location_to_coordinates(course['full_location'])
            if coordinates:
                course['coordinates'] = coordinates
                collection.insert_one(course)
                added += 1
        all_courses += 1
    return f'all: {all_courses}, added: {added}'


def find(filters: dict):
    '''
    Find all courses that satisfy given filters
    filters: full_location,
             specialization,
             commitmet (part-time or full-time)
    '''
    country = filters['full_location']
    title = filters['specialization']
    commitment = filters['commitment']

    match_filt = []
    courses = collection.find({'specialization': title})
    for course in courses:
        if (country in course['full_location']) and (course['commitment'] == commitment):
            match_filt.append(course)

    return match_filt


def already_in_db(course: dict):
    '''
    Check if spesific course already exists in a database
    if exists -> return True
    does not exist -> return False
    '''
    exists = collection.find_one(course)
    if not exists:
        return False
    print('here')
    return True


def location_to_coordinates(loc_name: list):
    ''' Convert location name to its coordinates '''
    country = loc_name[0]
    locator = Nominatim(user_agent='myGeocoder')
    
    location = locator.geocode(f'{country}, {loc_name[1]}')
    if location is None:
        return None

    return location.latitude, location.longitude



if __name__ == '__main__':
    courses = parser.parse_info("https://erasmusintern.org/traineeships?f%5B0%5D=field_traineeship_field_studies%253Aparents_all%3A38&f%5B1%5D=field_traineeship_dot%3A0&f%5B2%5D=field_traineeship_commitment%253Aparents_all%3A1&page=", 'Engineering and technology', 'part-time')
    print(pass_to_db(courses))

    # pprint(find({'full_location': 'United States', 'specialization': 'Engineering and technology', 'commitment': 'part-time'}))
    # collection.delete_many({})

    # locs = location_to_coordinates(["Canada", "Toronto, Montreal, Ottawa"])
    # print(locs)

