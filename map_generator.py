import folium
import random
from folium.plugins import MarkerCluster

def generate_map(loc_list):


    fl_map = folium.Map(location=loc_list[0]["coordinates"],
                        zoom_start=7,
                        tiles="https://{s}.tile.jawg.io/jawg-terrain/{z}/{x}/{y}{r}.png?access-token=ZIQ84swFii6yZwUalCwfg1ZmkzUHslHAaaQCLzEUfOU5wDlZTvk35SWBp1IPehjv",
                        attr='<a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                        min_zoom=2)

    fg = folium.FeatureGroup(name="Twitter Friends map")
    fill_colors = ["#4CC9F0","#4895EF", "#4361EE","#3F37C9","#3A0CA3","#480CA8","#560BAD","#F72585","#7209B7","#B5179E"]

    marker_cluster = MarkerCluster().add_to(fl_map)

    # fill_colors = ["#3B0209","#4E030C", "#6A040F","#9D0208","#D00000","#DC2F02","#E85D04","#F48C06","#FAA307","#FAA307"]

    for offer in loc_list:
        popup_template = f"""
        <div class="internship_container" style="font-family: fantasy;">
                    <h4 class="internship_title"><span class="underline--magical">{offer["title"]}</span></h4>
                    <p class="internship_date">From {offer["periods"]}. Application deadline: {offer["deadline"]}</p>
                    <p class="internship_desc"> Recruiter {offer["recruiter"]}</p>
                    <p class="internship_desc"> Requirements: {offer["requirements"]}</p>
                    <p class="internship_desc"> {offer["requirements"]}</p>
                </div>
        </html>
        """

        popup = folium.Popup(max_width=500, html =popup_template )

        folium.CircleMarker(location=offer["coordinates"],
                                        radius=10,
                                        popup=popup,
                                        fill_color=random.choice(fill_colors),
                                        color="#FFFFFF",
                                        fill_opacity=0.7).add_to(marker_cluster)

        fl_map.add_child(fg)
    return fl_map
