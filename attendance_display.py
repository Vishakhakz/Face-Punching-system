import streamlit as st
import pandas as pd
import time 
from datetime import datetime
import os  # Import os module to check file existence
from streamlit_autorefresh import st_autorefresh

# Get current timestamp and formatted date
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

# Set up auto-refresh for Streamlit
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# Check if the attendance file for today exists
attendance_file = f"Attendance/Attendance_{date}.csv"

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

# Display the attendance file only if it exists
if os.path.exists(attendance_file):
    df = pd.read_csv(attendance_file)
    st.dataframe(df.style.highlight_max(axis=0))
else:
    st.write(f"No attendance data found for today ({date}). Please ensure the attendance system is running and logged attendance.")
