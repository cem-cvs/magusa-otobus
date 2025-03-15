from geopy.distance import geodesic

def filter_landmarks_by_distance(landmarks, center_lat, center_lng, max_distance):
    """Filter landmarks based on distance from a given center point."""
    filtered = []
    for landmark in landmarks:
        landmark_coords = (landmark["latitude"], landmark["longitude"])
        center_coords = (center_lat, center_lng)
        distance = geodesic(center_coords, landmark_coords).km
        if distance <= max_distance:
            landmark["distance"] = round(distance, 2)  # Store the calculated distance
            filtered.append(landmark)
    return filtered

def filter_landmarks_by_type(landmarks, selected_types):
    """Filter landmarks based on selected types."""
    return [landmark for landmark in landmarks if landmark["type"] in selected_types]

def filter_landmarks_by_search(landmarks, search_term):
    """Filter landmarks based on search term (name or description)."""
    search_term = search_term.lower()
    return [
        landmark for landmark in landmarks
        if search_term in landmark["name"].lower() or search_term in landmark["description"].lower()
    ]
