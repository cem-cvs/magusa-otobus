import streamlit as st
import folium
from streamlit_folium import st_folium
from sqlalchemy.orm import Session
import time
import yaml

from yaml.loader import SafeLoader
from models.base import get_db, engine
from models.landmarks import Landmark
from models.transportation import TransportRoute
from data.landmarks import FAMAGUSTA_CENTER
from utils.map_utils import create_landmark_map, add_landmark_markers, filter_landmarks
from utils.schedule_utils import load_bus_schedules, display_schedule_table
from utils.filter_utils import filter_landmarks_by_distance, filter_landmarks_by_type, filter_landmarks_by_search
from utils.route_utils import create_route_planner, add_route_to_map
from database.init_db import init_database

st.set_page_config(
    page_title="Famagusta Bus System",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on startup
init_database()

# 🔵 Mock Bus Movement (Simulating real-time tracking)
BUS_ROUTE = [
    (35.1234, 33.9456), (35.1240, 33.9460), (35.1245, 33.9470),
    (35.1250, 33.9480), (35.1255, 33.9490), (35.1260, 33.9500)
]
if "bus_position_index" not in st.session_state:
    st.session_state.bus_position_index = 0

def update_bus_position():
    """Update only the bus marker's position without reloading the map."""
    st.session_state.bus_position_index = (st.session_state.bus_position_index + 1) % len(BUS_ROUTE)
    return BUS_ROUTE[st.session_state.bus_position_index]

# 🔵 Fetch Landmarks with Caching
def get_landmarks(db: Session, search_term: str = "", limit: int = 50) -> list:
    """Fetch landmarks with search filter and limit results."""
    query = db.query(Landmark)
    if search_term:
        search = f"%{search_term.lower()}%"
        query = query.filter(
            (Landmark.name.ilike(search)) | 
            (Landmark.description.ilike(search))
        )
    return [landmark.to_dict() for landmark in query.limit(limit).all()]
     # Debugging: Print landmarks to Streamlit
    st.write("Fetched Landmarks:", landmarks)

    if not landmarks:
        st.warning("No landmarks found in the database!")

    return [landmark.to_dict() for landmark in landmarks]

# 🔵 Main Streamlit App
def main():
    # 🔵 Dark Mode Toggle
    dark_mode = st.sidebar.toggle("Dark Mode", value=False)
    theme = "dark" if dark_mode else "light"
    st.markdown(f"""
        <style>
            body {{ background-color: {'#121212' if dark_mode else '#FFFFFF'}; color: {'#FFFFFF' if dark_mode else '#000000'} }}
        </style>
    """, unsafe_allow_html=True)

    # 🔵 Authentication
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>Famagusta Bus System</h1>", unsafe_allow_html=True)

    # 🔵 Tabs
    tab3, tab2, tab1, tab4 = st.tabs(["Bus Schedules", "Route Planner", "Landmarks", "Live Bus Tracking"])

    try:
        # Fetch Database Session
        db = next(get_db())

        # Cache landmarks in session state
        if "landmarks" not in st.session_state:
            st.session_state.landmarks = get_landmarks(db)

        landmarks = st.session_state.landmarks
        with tab1:
            st.subheader("Landmarks")
        
            # Fetch data
            db = next(get_db())
            landmarks = get_landmarks(db)
        
            if not landmarks:
                st.warning("No landmarks found in the database!")
            else:
                for landmark in landmarks:
                    with st.expander(landmark["name"]):
                        st.write(landmark["description"])
                        st.write(f"📍 Location: {landmark['latitude']}, {landmark['longitude']}")
                        
        # 🔵 Live Bus Tracking
        with tab4:
            st.subheader("Live Bus Tracking")
        
            # Fetch current bus location
            bus_lat, bus_lon = update_bus_position()
        
            # Keep the map static by only updating the bus marker
            if "bus_map" not in st.session_state:
                st.session_state.bus_map = folium.Map(
                    location=[35.123, 33.942],  # Static center of the map
                    zoom_start=13
                )
        
            # Remove previous marker before adding a new one
            for key in list(st.session_state.keys()):
                if key.startswith("bus_marker_"):
                    del st.session_state[key]
        
            # Add updated bus marker
            bus_marker_key = f"bus_marker_{bus_lat}_{bus_lon}"
            if bus_marker_key not in st.session_state:
                st.session_state[bus_marker_key] = folium.Marker(
                    location=[bus_lat, bus_lon],
                    tooltip="Bus Location",
                    icon=folium.Icon(color="red")
                )
                st.session_state[bus_marker_key].add_to(st.session_state.bus_map)
        
            # Display the static map
            st_folium(st.session_state.bus_map, width=800)
        
            # Wait a moment, then update the marker (without refreshing the map)
            time.sleep(2)
            st.rerun()
        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            
if __name__ == "__main__":
    main()
