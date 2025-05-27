import pandas as pd

def test_csv_path():
    try:
        # Adjust this path to match your actual CSV file name in the same directory
        data = pd.read_csv('Soil\soil_wellbeing_index (1).csv')
        print("CSV file loaded successfully!")
        print(data.head())  # Display the first few rows of the data
    except FileNotFoundError:
        print("CSV file not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_csv_path()
