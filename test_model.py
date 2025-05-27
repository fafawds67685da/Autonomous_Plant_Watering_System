import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import joblib

# Function to test model loading and prediction
def test_model(model_name):
    try:
        # Load the model based on the model name passed
        if model_name == 'moisture_duration':
            data = pd.read_csv('Soil/soil_moisture_duration (1).csv')
            data['moisture_percent'] = 100 - (data['raw_moisture'] / 1023) * 100
            y = data['moisture_duration_hrs']
            x = data.drop(['moisture_duration_hrs', 'timestamp'], axis=1)
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            model = GradientBoostingRegressor(random_state=42)
            model.fit(X_train, y_train)
            joblib.dump(model, 'moisture_duration_model.pkl')
            print(f"{model_name} model loaded and saved successfully.")
            sample_data = pd.DataFrame({
            'raw_moisture': [600],  # Example moisture value
            'temperature': [25],    # Example temperature value
            'moisture_percent': [100 - (600 / 1023) * 100]
        })
            prediction = model.predict(sample_data)
            print(f"Prediction for {model_name}: {prediction[0]}")
        
        elif model_name == 'soil_wellbeing':
            data = pd.read_csv('Soil/soil_wellbeing_index (1).csv')
            data['moisture_percent'] = 100 - (data['raw_moisture'] / 1023) * 100
            y = data['soil_wellbeing_index']
            x = data.drop(['timestamp', 'soil_wellbeing_index'], axis=1)

            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            model = GradientBoostingRegressor(random_state=42)
            model.fit(X_train, y_train)
            joblib.dump(model, 'soil_wellbeing_model.pkl')
            print(f"{model_name} model loaded and saved successfully.")
            sample_data = pd.DataFrame({
            'raw_moisture': [600],  # Example moisture value
            'temperature': [25],    # Example temperature value
            'moisture_percent': [100 - (600 / 1023) * 100]
        })
            prediction = model.predict(sample_data)
            print(f"Prediction for {model_name}: {prediction[0]}")
        
        else:
            print("Invalid model name.")
            return
        
        
        
        # Test prediction on sample data
        
        
       
    
    except FileNotFoundError:
        print("CSV file not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_model('moisture_duration')  # Test moisture_duration model
    test_model('soil_wellbeing')    # Test soil_wellbeing model
