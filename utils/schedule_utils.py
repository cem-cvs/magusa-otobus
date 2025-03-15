import pandas as pd
import streamlit as st

def load_bus_schedules():
    """Mock function to load bus schedules (Replace with actual database query if needed)."""
    return pd.DataFrame([
        {"Route": "Line 1", "Departure": "08:00", "Arrival": "08:30"},
        {"Route": "Line 2", "Departure": "09:00", "Arrival": "09:45"},
        {"Route": "Line 3", "Departure": "10:30", "Arrival": "11:15"},
    ])

def display_schedule_table(schedule_data):
    """Display bus schedule as a table."""
    st.subheader("Bus Schedules")
    st.dataframe(schedule_data)
