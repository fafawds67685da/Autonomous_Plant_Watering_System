import streamlit as st
import requests

st.set_page_config(page_title="Smart Plant Monitor", page_icon="🌿")
st.title("🌱 Smart Plant Monitor")

# ➕ Add a new plant
st.header("➕ Add a New Plant")
name = st.text_input("Plant Name")
thresh = st.number_input("Moisture Threshold", min_value=0, max_value=1023, value=500)

if st.button("Add Plant"):
    if name:
        try:
            res = requests.post("http://localhost:8000/api/plants", json={
                "name": name,
                "moisture_threshold": thresh
            })
            if res.status_code == 200:
                st.success("✅ Plant Added!")
            else:
                st.error("❌ Failed to add plant.")
        except Exception as e:
            st.error("🚫 Could not connect to backend.")
            st.code(str(e))
    else:
        st.warning("⚠️ Please enter a plant name.")

# 📊 View plants and their data
st.header("🌿 Your Plants")

plants = [
    {"id": 1, "name": "Plant A", "moisture_threshold": 500, "avatar": "🌵"},
    {"id": 2, "name": "Plant B", "moisture_threshold": 600, "avatar": "🌻"},
]

for plant in plants:
    st.subheader(f"{plant['avatar']} {plant['name']}")
    st.write(f"Moisture Threshold: {plant['moisture_threshold']}")

    st.write("📊 Latest Sensor Data")
    try:
        response = requests.get(f"http://localhost:8000/api/sensordata/{plant['id']}")
        response.raise_for_status()
        data = response.json()
        st.write(f"🌡️ Temperature: {data['temperature']} °C")
        st.write(f"💧 Moisture: {data['moisture']}")
    except Exception as e:
        st.error("🚫 Could not fetch sensor data.")
        st.code(str(e))

    # Prediction buttons
    if st.button(f"Get Predictions for {plant['name']}"):
        try:
            moisture_duration_pred = requests.get(f"http://localhost:8000/api/predict_moisture_duration/{plant['id']}").json()
            soil_wellbeing_pred = requests.get(f"http://localhost:8000/api/predict_soil_wellbeing/{plant['id']}").json()

            # ✅ Use correct keys
            st.write(f"⏳ Predicted Moisture Duration: {moisture_duration_pred['predicted_moisture_duration_hrs']} hrs")
            st.write(f"🌱 Predicted Soil Wellbeing Index: {soil_wellbeing_pred['predicted_soil_wellbeing_index']}")
        except Exception as e:
            st.error("🤖 Prediction models not connected or response malformed.")
            st.code(str(e))
