import streamlit as st
import pydeck as pdk
from streamlit_folium import st_folium
from sqlalchemy.orm import Session
import time

from models.base import get_db, engine
from models.landmarks import Landmark
from models.transportation import TransportRoute
from data.landmarks import FAMAGUSTA_CENTER
from utils.map_utils import create_landmark_map, add_landmark_markers
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
    #(35.1234, 33.9456), (35.1240, 33.9460), (35.1245, 33.9470),
    #(35.1250, 33.9480), (35.1255, 33.9490), (35.1260, 33.9500)
    (35.159032, 33.911035),
    (35.158907, 33.909440),
    (35.157989, 33.906709),
    (35.157258, 33.904158),
    (35.155954, 33.904234),
    (35.153367, 33.905906),
    (35.151594, 33.906952),
    (35.148850, 33.908674),
    (35.145877, 33.911328),
    (35.143425, 33.913548),
    (35.142079, 33.914594),
    (35.141245, 33.915232),
    (35.139523, 33.916495),
    (35.138250, 33.918167),
    (35.137030, 33.920476),
    (35.133607, 33.923436),
    (35.131833, 33.925095),
    (35.129924, 33.928450),
    (35.128807, 33.930198),
    (35.125990, 33.932699),
    (35.123934, 33.934562),
    (35.121346, 33.937815),
    (35.120626, 33.940405),
    (35.120563, 33.944144),
    (35.121836, 33.947257),
    (35.122337, 33.948469),
    (35.121064, 33.953866)
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
    landmarks = query.limit(limit).all()

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

        # 🔵 Landmarks Tab
        with tab1:
            st.subheader("Landmarks")
            
            if not landmarks:
                st.warning("No landmarks found in the database!")
            else:
                landmark_map = folium.Map(location=[35.123, 33.942], zoom_start=13)
        
                for landmark in landmarks:
                    folium.Marker(
                        location=[landmark["latitude"], landmark["longitude"]],
                        popup=f"{landmark['name']}: {landmark['description']}",
                        icon=folium.Icon(color="blue", icon="info-sign")
                    ).add_to(landmark_map)
        
                folium_static(landmark_map)  # Display the map in Streamlit
        
                for landmark in landmarks:
                    with st.expander(landmark["name"]):
                        st.write(landmark["description"])
                        st.write(f"📍 Location: {landmark['latitude']}, {landmark['longitude']}")

        # 🔵 Live Bus Tracking (Updated Pydeck Version)
        with tab4:
            st.subheader("Live Bus Tracking")

            bus_lat, bus_lon = update_bus_position()

            # Define Pydeck layer (only updates bus marker)
            layer = pdk.Layer(
                "IconLayer",
                data=[{
                    "lat": bus_lat,
                    "lon": bus_lon,
                    "icon_data": {
                        "url": "https://img.icons8.com/ios-filled/50/bus.png",
                        "width": 50,
                        "height": 50,
                        "anchorY": 50
                    },
                    "direction": 90  # Set dynamically from GPS data
                }],
                get_position=["lon", "lat"],
                get_icon="icon_data",
                get_size=4,
                size_scale=10,
                pickable=True,
            )

            # Render Pydeck Map
            map = pdk.Deck(
                map_style="mapbox://styles/mapbox/streets-v11",
                initial_view_state=pdk.ViewState(
                    latitude=35.123,
                    longitude=33.942,
                    zoom=13,
                    pitch=50,
                    tooltip={"text": "{name}\n{address}"},
                ),
                layers=[layer],
            )

            st.pydeck_chart(map)

            # Update the bus location every 2 seconds
            time.sleep(2)
            st.rerun()  # Re-run the script, but only the marker updates!

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
