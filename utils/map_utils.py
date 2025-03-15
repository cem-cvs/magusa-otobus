import folium

def create_landmark_map(latitude, longitude):
    m = folium.Map(location=[latitude, longitude], zoom_start=13)
    return m

def add_landmark_markers(map_obj, landmarks):
    for landmark in landmarks:
        folium.Marker(
            location=[landmark["latitude"], landmark["longitude"]],
            popup=landmark["name"],
            tooltip=landmark["name"]
        ).add_to(map_obj)
