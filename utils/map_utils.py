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

def filter_landmarks(landmarks, search_term):
    """Filter landmarks based on a search term."""
    return [
        landmark for landmark in landmarks
        if search_term.lower() in landmark["name"].lower()
        or search_term.lower() in landmark["description"].lower()
    ]
