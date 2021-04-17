from pymongo import MongoClient
from pprint import pprint
import parser


connection = 'CONNECTION URL WAS REMOVED DUE TO SAFETY REASONS'
connection = 'mongodb+srv://admin:ucuhacathon2021@cluster0.xqgj4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(connection)
db = client['internships']
collection = db['internship_locations']


def pass_to_db(courses: list):
    ''' Pass courses info to the database '''
    added = 0
    all_courses = 0
    for course in courses:
        if not already_in_db(course):
            collection.insert_one(course)
            added += 1
        all_courses += 1
    return f'all: {all_courses}, added: {added}'


def find(filters: dict):
    '''
    Find all courses that satisfy given filters
    dictionary contains: {'country': smth, 'title': 'title'}
    '''
    country = filters['full_location']
    title = filters['specialization']

    match_filt = []
    courses = collection.find({'specialization': title})
    for c in courses:
        pprint(c['full_location'])
    # for course in courses:
    #     if country in course['full_location']:
    #         match_filt.append(course)

    # return match_filt


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



if __name__ == '__main__':
    # courses = parser.parse_info("https://erasmusintern.org/traineeships?f%5B0%5D=field_traineeship_field_studies%253Aparents_all%3A38&page=", 
    #                "Engineering and technology")
    # pass_to_db(courses)
    pprint(find({'full_location': 'United States', 'specialization': 'Engineering and technology'}))
    # collection.delete_many({})
