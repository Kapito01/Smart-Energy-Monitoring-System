import requests
import random
import time

BLYNK_TOKEN = "O8yka32DNbH8OXJRpVG4aqHRekq4VcIe"

base_url = "https://blynk.cloud/external/api/update"
get_url = "https://blynk.cloud/external/api/get"

energy = 0  # kWh
cost_per_kwh = 0.5

current = 2.0  
alert_state = 0
alert_counter = 0

# Shared data for Streamlit
latest_data = {
    "voltage": 0,
    "current": 0,
    "power": 0,
    "energy": 0,
    "bill": 0,
    "alert": 0
}

while True:
    # Read switch from Blynk (V5)
    try:
        response = requests.get(f"{get_url}?token={BLYNK_TOKEN}&V5")
        appliance = int(response.text)
    except:
        appliance = 0

    # Simulate time of day
    hour = int((time.time() / 10) % 24)

    if 18 <= hour <= 23:
        base_current = random.uniform(3.0, 5.0)
    elif 6 <= hour <= 9:
        base_current = random.uniform(2.0, 3.5)
    else:
        base_current = random.uniform(0.5, 2.0)

    # Switch effect
    if appliance == 1:
        base_current *= 1.8
        voltage = random.uniform(220, 245)
    else:
        voltage = random.uniform(210, 230)

    # Smooth current
    current += (base_current - current) * 0.3
    current = round(current, 2)

    voltage = round(voltage, 2)
    power = round(voltage * current, 2)

    # Energy + billing
    energy += power / 30000  
    bill = round(energy * cost_per_kwh, 2)

    if bill > 600:
        bill = 600

    # Alert logic
    if power > 1000:
        alert_counter += 1
    else:
        alert_counter -= 1

    alert_counter = max(0, min(alert_counter, 3))
    alert_state = 1 if alert_counter >= 2 else 0

    # UPDATE STREAMLIT DATA
    latest_data["voltage"] = voltage
    latest_data["current"] = current
    latest_data["power"] = power
    latest_data["energy"] = energy
    latest_data["bill"] = bill
    latest_data["alert"] = alert_state

    # Send to Blynk
    requests.get(
        f"{base_url}?token={BLYNK_TOKEN}"
        f"&V0={voltage}&V1={current}&V2={power}"
        f"&V3={round(energy, 5)}&V4={bill}&V6={alert_state}"
    )

    print(f"""
--- SMART METER LIVE ---
Switch: {"ON" if appliance == 1 else "OFF"}

Voltage: {voltage} V
Current: {current} A
Power: {power} W

Energy: {energy:.5f} kWh
Bill: {bill}

Alert: {" HIGH USAGE" if alert_state else "Normal"}
-------------------------
""")

    time.sleep(2)