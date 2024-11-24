import pandas as pd
from datetime import datetime, timedelta
import random
import time
import pytz  # For timezone handling

def generate_test_csv(file_name="data/csv/test.csv"):
    # Define the CDT timezone
    cdt = pytz.timezone('US/Central')
    
    # Define the time range
    now = datetime.now(cdt)  # Current time in CDT
    start_time = now - timedelta(days=14)  # A week from now
    end_time = now + timedelta(days=7)    # Two days after now
    prediction_start_time = now  # Predictions begin from the current time

    # Initialize an empty list to store data
    data = []

    # Generate data
    current_time = start_time
    while current_time <= end_time:
        measurement = random.randint(70, 75)
        measurement2 = random.randint(70, 80)
        prediction = measurement - 5 if current_time >= prediction_start_time else None
        prediction2 = measurement2 - 5 if current_time >= prediction_start_time else None
        
        # Format date in 12-hour format with CDT explicitly stated
        formatted_time = current_time.strftime("%Y-%m-%d %I:%M:%S %p")
        data.append({
            "Date": formatted_time,
            "Water Measurement": measurement,
            "Water Prediction": prediction,
            "Air Measurement": measurement2,
            "Air Prediction": prediction2,
            
        })
        current_time += timedelta(hours=6)  # Increment by specified time

    df = pd.DataFrame(data)

    # Ensure the directory exists
    import os
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    # Write the DataFrame to a CSV file
    df.to_csv(file_name, index=False)
    print(f"Data written to {file_name}")
    
    time.sleep(5)

if __name__ == "__main__":

    generate_test_csv("data/csv/test.csv")
