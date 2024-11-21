import requests
import pandas as pd
from datetime import datetime
import os

class EarthquakeDataExporter:
    def __init__(self, base_url='http://127.0.0.1'):
        self.base_url = base_url
        self.output_dir = 'earthquake_data'
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_data(self, endpoint):
        try:
            response = requests.get(f'{self.base_url}/{endpoint}')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def export_recent_earthquakes(self):
        data = self.get_data('recent-earthquakes')
        if data:
            try:
                df = pd.DataFrame(data)
                # Extract latitude and longitude from coordinates
                df['latitude'] = df['coordinates'].apply(lambda x: x[0])
                df['longitude'] = df['coordinates'].apply(lambda x: x[1])
                df.drop('coordinates', axis=1, inplace=True)
                
                filename = os.path.join(
                    self.output_dir,
                    f'recent_earthquakes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                )
                df.to_csv(filename, index=False)
                print(f"Recent earthquakes exported to {filename}")
            except Exception as e:
                print(f"Error exporting data: {e}")
    
    def export_predictions(self):
        data = self.get_data('prediction')
        if data:
            try:
                df = pd.DataFrame([data])
                filename = os.path.join(
                    self.output_dir,
                    f'predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                )
                df.to_csv(filename, index=False)
                print(f"Predictions exported to {filename}")
            except Exception as e:
                print(f"Error exporting predictions: {e}")
    
    def export_all(self):
        print("Exporting all earthquake data...")
        self.export_recent_earthquakes()
        self.export_predictions()
        print("Export complete!")

# Usage example
if __name__ == "__main__":
    exporter = EarthquakeDataExporter()
    exporter.export_all()
