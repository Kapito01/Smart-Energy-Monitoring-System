import streamlit as st
import time

# Import your simulation data
from Blynk.py import latest_data  

st.set_page_config(page_title="Smart Energy Monitor", layout="wide")

st.title("Smart Energy Monitoring System")

# Layout
col1, col2, col3 = st.columns(3)

# Metrics placeholders
voltage_box = col1.empty()
current_box = col2.empty()
power_box = col3.empty()

energy_box = col1.empty()
bill_box = col2.empty()
alert_box = col3.empty()

# Chart data
power_history = []

while True:
    voltage = latest_data["voltage"]
    current = latest_data["current"]
    power = latest_data["power"]
    energy = latest_data["energy"]
    bill = latest_data["bill"]
    alert = latest_data["alert"]

    # Metrics display
    voltage_box.metric("Voltage (V)", f"{voltage}")
    current_box.metric("Current (A)", f"{current}")
    power_box.metric("Power (W)", f"{power}")

    energy_box.metric("Energy (kWh)", f"{energy:.4f}")
    bill_box.metric("Estimated Bill", f"₹ {bill}")

    if alert == 1:
        alert_box.error("🚨 HIGH USAGE")
    else:
        alert_box.success("✅ Normal Usage")

    # Update chart
    power_history.append(power)
    if len(power_history) > 50:
        power_history.pop(0)

    st.line_chart(power_history)

    time.sleep(2)