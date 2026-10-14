import os
import pandas as pd

def run_analytics_pipeline():
    file_path = 'data/smart_meter_data.csv'
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find {file_path}. Ensure it is inside the 'data/' folder.")
        
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