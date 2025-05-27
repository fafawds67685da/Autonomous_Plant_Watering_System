from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

app = FastAPI()

# ----------------------------- Models Initialization -----------------------------
moisture_duration_model = None
soil_wellbeing_model = None

def load_moisture_duration_model():
    global moisture_duration_model
    if moisture_duration_model is None:
        data = pd.read_csv('D:\Autonomous_Plant_Watering_System\Soil\soil_moisture_duration (1).csv')
        data['moisture_percent'] = 100 - (data['raw_moisture'] / 1023) * 100
        y = data['moisture_duration_hrs']
        x = data.drop(['moisture_duration_hrs'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        moisture_duration_model = GradientBoostingRegressor(random_state=42)
        moisture_duration_model.fit(X_train, y_train)
    return moisture_duration_model

def load_soil_wellbeing_model():
    global soil_wellbeing_model
    if soil_wellbeing_model is None:
        data = pd.read_csv('D:\Autonomous_Plant_Watering_System\Soil\soil_wellbeing_index (1).csv')
        data['moisture_percent'] = 100 - (data['raw_moisture'] / 1023) * 100
        y = data['soil_wellbeing_index']
        x = data.drop(['soil_wellbeing_index'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        soil_wellbeing_model = GradientBoostingRegressor(random_state=42)
        soil_wellbeing_model.fit(X_train, y_train)
    return soil_wellbeing_model

# ----------------------------- Dynamic Sensor Data and Prediction Endpoints -----------------------------

@app.get("/api/sensordata/{plant_id}")
def get_sensor_data(plant_id: int):
    # Fetch real sensor data based on plant_id or return dummy data
    if plant_id == 1:
        return {"temperature": 22, "moisture": 600}
    elif plant_id == 2:
        return {"temperature": 23, "moisture": 550}
    else:
        return {"temperature": 25, "moisture": 650}

@app.get("/api/predict_moisture_duration/{plant_id}")
def predict_moisture_duration(plant_id: int):
    model = load_moisture_duration_model()
    
    # Fetch the actual sensor data for the plant
    sensor_data = get_sensor_data(plant_id)
    raw_moisture = sensor_data['moisture']
    temperature = sensor_data['temperature']
    
    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'raw_moisture': [raw_moisture],
        'temperature': [temperature],
        'moisture_percent': [100 - (raw_moisture / 1023) * 100]
    })
    
    # Make prediction
    prediction = model.predict(input_data)
    
    return {"predicted_moisture_duration": round(prediction[0], 2)}

@app.get("/api/predict_soil_wellbeing/{plant_id}")
def predict_soil_wellbeing(plant_id: int):
    model = load_soil_wellbeing_model()
    
    # Fetch the actual sensor data for the plant
    sensor_data = get_sensor_data(plant_id)
    raw_moisture = sensor_data['moisture']
    temperature = sensor_data['temperature']
    
    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'raw_moisture': [raw_moisture],
        'temperature': [temperature],
        'moisture_percent': [100 - (raw_moisture / 1023) * 100]
    })
    
    # Make prediction
    prediction = model.predict(input_data)
    
    return {"predicted_soil_wellbeing_index": round(prediction[0], 2)}
