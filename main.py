from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import os

app = FastAPI()

# ----------------------------- Global Model Variables -----------------------------
moisture_duration_model = None
soil_wellbeing_model = None

# ----------------------------- Helper Function -----------------------------
def calculate_moisture_percent(raw_moisture):
    return 100 - (raw_moisture / 1023) * 100

# ----------------------------- Load Models -----------------------------
def load_moisture_duration_model():
    global moisture_duration_model
    if moisture_duration_model is None:
        data = pd.read_csv(os.path.join('Soil', 'soil_moisture_duration (1).csv'))
        data['moisture_percent'] = calculate_moisture_percent(data['raw_moisture'])
        y = data['moisture_duration_hrs']
        x = data.drop(['moisture_duration_hrs', 'timestamp'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        moisture_duration_model = GradientBoostingRegressor(random_state=42)
        moisture_duration_model.fit(X_train, y_train)
    return moisture_duration_model

def load_soil_wellbeing_model():
    global soil_wellbeing_model
    if soil_wellbeing_model is None:
        data = pd.read_csv(os.path.join('Soil', 'soil_wellbeing_index (1).csv'))
        data['moisture_percent'] = calculate_moisture_percent(data['raw_moisture'])
        y = data['soil_wellbeing_index']
        x = data.drop(['soil_wellbeing_index', 'timestamp'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        soil_wellbeing_model = GradientBoostingRegressor(random_state=42)
        soil_wellbeing_model.fit(X_train, y_train)
    return soil_wellbeing_model

# ----------------------------- Dummy Sensor Data -----------------------------
@app.get("/api/sensordata/{plant_id}")
def get_sensor_data(plant_id: int):
    dummy_data = {
        1: {"temperature": 22, "moisture": 600},
        2: {"temperature": 23, "moisture": 550},
        3: {"temperature": 25, "moisture": 650}
    }
    return dummy_data.get(plant_id, {"temperature": 26, "moisture": 580})

# ----------------------------- Moisture Duration Prediction -----------------------------
@app.get("/api/predict_moisture_duration/{plant_id}")
def predict_moisture_duration(plant_id: int):
    model = load_moisture_duration_model()
    sensor_data = get_sensor_data(plant_id)
    raw_moisture = sensor_data['moisture']
    temperature = sensor_data['temperature']
    moisture_percent = calculate_moisture_percent(raw_moisture)

    input_df = pd.DataFrame([{
        'raw_moisture': raw_moisture,
        'temperature': temperature,
        'moisture_percent': moisture_percent
    }])

    prediction = model.predict(input_df)[0]
    return {"plant_id": plant_id, "predicted_moisture_duration_hrs": round(prediction, 2)}

# ----------------------------- Soil Wellbeing Prediction -----------------------------
@app.get("/api/predict_soil_wellbeing/{plant_id}")
def predict_soil_wellbeing(plant_id: int):
    model = load_soil_wellbeing_model()
    sensor_data = get_sensor_data(plant_id)
    raw_moisture = sensor_data['moisture']
    temperature = sensor_data['temperature']
    moisture_percent = calculate_moisture_percent(raw_moisture)

    input_df = pd.DataFrame([{
        'raw_moisture': raw_moisture,
        'temperature': temperature,
        'moisture_percent': moisture_percent
    }])

    prediction = model.predict(input_df)[0]
    return {"plant_id": plant_id, "predicted_soil_wellbeing_index": round(prediction, 2)}
