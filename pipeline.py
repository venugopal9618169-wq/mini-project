import os
import pandas as pd

def run_analytics_pipeline():
    # Check possible locations for the CSV file
    possible_paths = [
        'smart_meter_data.csv',
        'data/smart_meter_data.csv',
        './smart_meter_data.csv',
        './data/smart_meter_data.csv'
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if not file_path:
        raise FileNotFoundError("Could not find smart_meter_data.csv in the root or data/ folder. Please upload it!")
        
    df = pd.read_csv(file_path)
    
    # Preprocessing
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Map Anomaly Label to binary flag (1 for Abnormal, 0 for Normal)
    df['is_anomaly'] = df['Anomaly_Label'].apply(lambda x: 1 if str(x).strip().lower() == 'abnormal' else 0)
    
    return df

if __name__ == '__main__':
    df = run_analytics_pipeline()
    print("Pipeline executed successfully. Total records:", len(df))
    print("Anomalies detected:", df['is_anomaly'].sum())