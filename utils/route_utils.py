import folium
from geopy.distance import geodesic
import streamlit as st

def create_route_planner(landmarks):
    """Create a simple UI to select start and end landmarks for routing."""
    st.subheader("Route Planner")
    start_point = st.selectbox("Select Starting Point", landmarks, format_func=lambda x: x["name"])
    end_point = st.selectbox("Select Destination", landmarks, format_func=lambda x: x["name"])

    return start_point, end_point

def add_route_to_map(route_map, start_point, end_point):
    """Draw a route between two landmarks and calculate distance."""
    start_coords = (start_point["latitude"], start_point["longitude"])
    end_coords = (end_point["latitude"], end_point["longitude"])

    # Calculate distance
    distance = geodesic(start_coords, end_coords).km

    # Add route to map
    folium.Marker(start_coords, popup=start_point["name"], icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker(end_coords, popup=end_point["name"], icon=folium.Icon(color="red")).add_to(route_map)
    folium.PolyLine([start_coords, end_coords], color="blue", weight=5).add_to(route_map)

    return distance
