import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

class EarthquakeTracker:
    def __init__(self):
        self.base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.historical_data = None
        
    def fetch_earthquakes(self, start_date, end_date, min_magnitude=2.5):
        """
        Fetch earthquake data from USGS for a given time period
        """
        params = {
            'format': 'geojson',
            'starttime': start_date.isoformat(),
            'endtime': end_date.isoformat(),
            'minmagnitude': min_magnitude
        }
        
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['features']
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")
    
    def process_earthquake_data(self, earthquakes):
        """
        Process raw earthquake data into a pandas DataFrame
        """
        processed_data = []
        for eq in earthquakes:
            properties = eq['properties']
            geometry = eq['geometry']
            processed_data.append({
                'time': datetime.fromtimestamp(properties['time'] / 1000.0),
                'magnitude': properties['mag'],
                'latitude': geometry['coordinates'][1],
                'longitude': geometry['coordinates'][0],
                'depth': geometry['coordinates'][2],
                'place': properties['place']
            })
        return pd.DataFrame(processed_data)
    
    def update_historical_data(self):
        """
        Update historical earthquake data for the last 30 days
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        earthquakes = self.fetch_earthquakes(start_date, end_date)
        self.historical_data = self.process_earthquake_data(earthquakes)
        
    def predict_next_earthquake(self):
        """
        Simple prediction model based on historical patterns
        """
        if self.historical_data is None or len(self.historical_data) < 2:
            raise Exception("Insufficient historical data for prediction")
            
        # Group by date and count earthquakes
        daily_counts = self.historical_data.groupby(
            self.historical_data['time'].dt.date
        ).size().reset_index()
        daily_counts.columns = ['date', 'count']
        
        # Prepare data for prediction
        X = np.arange(len(daily_counts)).reshape(-1, 1)
        y = daily_counts['count'].values
        
        # Fit linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next day
        next_day_pred = model.predict([[len(daily_counts)]])[0]
        
        return {
            'predicted_earthquakes': max(0, round(next_day_pred)),
            'confidence': model.score(X, y)
        }