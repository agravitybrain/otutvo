"""
A module for getting a friend list and their locations(lat,long).
"""
import requests
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable


def get_user_friends(username):
    """
    Gets data about a specific twitter profile
    """
    base_url = "https://api.twitter.com/"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAFx4MwEAAAAA%2FZcsDE86L0w2He8EjBi1JbfDiMc%3DKysXA5FGeaV53qiLXXdmmXl62pa43vwhpFbpioTgromw6asmqZ"
    search_url = f"{base_url}1.1/friends/list.json"
    search_headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    search_params = {
        "screen_name": f"{username}",
        "count": 12
    }

    user_info = requests.get(f"{base_url}1.1/users/show.json", headers=search_headers, params={"screen_name":username})
    user_json = user_info.json()
    response = requests.get(search_url, headers=search_headers, params=search_params)
    json_response = response.json()

    friend_list = [(user_json["screen_name"], user_json["location"])]
    for friend in json_response["users"]:
        if friend["location"]:
            friend_list.append((friend["screen_name"], friend["location"]))
    # print(friend_list)
    return friend_list

def friends_geolocator(friend_list):
    """
    Finds coords using geopy
    """
    geolocator = Nominatim(user_agent="TwitterFriendMap")
    friend_loc_list = []
    loc_dict = {}
    for friend in friend_list:
        loc = loc_dict.get(friend[1], False)  # check if this is a new location
        if not loc and loc != 'unavailable':  # if this is a new location entry
            try:
                loc_dict[friend[1]] = geolocator.geocode(friend[1])
                if loc_dict[friend[1]] == None:  # generalize the location if geopy can't find it
                    temp_loc_list = friend[1].split(",")
                    shorter_loc = ", ".join(temp_loc_list[1:])
                    loc_dict[friend[1]] = geolocator.geocode(shorter_loc)
            except GeocoderUnavailable:
                loc_dict[friend[1]] = 'unavailable'
        loc = loc_dict.get(friend[1], False)
        if loc and loc != 'unavailable':  # if geopy found the location
            loc = loc.point[:-1]
        friend_loc_list.append((friend[0], loc))

    friend_loc_list_clean = [i for i in friend_loc_list if i[1] is not None and i[1] != 'unavailable']
    return friend_loc_list_clean
