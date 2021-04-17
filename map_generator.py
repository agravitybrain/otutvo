import folium
from friend_searcher import friends_geolocator, get_user_friends
import random
from folium.plugins import MarkerCluster
from icecream import ic
# print(friends_loc_list)


# def group_duplicates(loc_list):
#     loc_dict = {}
#     for offer in loc_list:
#         loc_dict[offer["coordinates"]] = loc_dict.get(offer["coordinates"], []) + [offer]
#
#     grouped_loc_list = []
#     for location, offers in loc_dict.items():
#         for offer in offers:
#             grouped_loc_list.append((name,location))
#     return grouped_loc_list



def generate_map(loc_list):


    fl_map = folium.Map(location=loc_list[0]["coordinates"],
                        zoom_start=7,
                        tiles="https://{s}.tile.jawg.io/jawg-terrain/{z}/{x}/{y}{r}.png?access-token=ZIQ84swFii6yZwUalCwfg1ZmkzUHslHAaaQCLzEUfOU5wDlZTvk35SWBp1IPehjv",
                        attr='<a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                        min_zoom=2)
    # folium.TileLayer('mapquestopen').add_to(fl_map)
    # folium.TileLayer('openstreetmap').add_to(fl_map)
    # folium.TileLayer('Mapbox Bright').add_to(fl_map)

    fg = folium.FeatureGroup(name="Twitter Friends map")
    fill_colors = ["#4CC9F0","#4895EF", "#4361EE","#3F37C9","#3A0CA3","#480CA8","#560BAD","#F72585","#7209B7","#B5179E"]

    marker_cluster = MarkerCluster().add_to(fl_map)

    # fill_colors = ["#3B0209","#4E030C", "#6A040F","#9D0208","#D00000","#DC2F02","#E85D04","#F48C06","#FAA307","#FAA307"]

    for offer in loc_list:
        # icon = folium.features.CustomIcon("images/map_pin.png", icon_size=(30, 30))

        popup_template = {offer["title"]}

        popup = folium.Popup(max_width=200, html =popup_template )

        folium.CircleMarker(location=offer["coordinates"],
                                        radius=10,
                                        popup=popup_template,
                                        fill_color=random.choice(fill_colors),
                                        color="#FFFFFF",
                                        fill_opacity=0.7).add_to(marker_cluster)

        fl_map.add_child(fg)
    # fl_map.save('templates/raw_map.html')
    return fl_map
