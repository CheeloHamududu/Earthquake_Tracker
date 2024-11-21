# Earthquake Tracking and Prediction Application

This application tracks real-time earthquake data and provides basic predictions for future seismic activity.

## Features

- Fetches real-time earthquake data from USGS
- Tracks historical earthquake patterns
- Provides simple predictions for future earthquake activity
- REST API endpoints for accessing earthquake data and predictions
- Automatic hourly updates of earthquake data

## Installation

1. Clone this repository
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python app.py
```

## API Endpoints

- `/recent-earthquakes`: Get the 10 most recent earthquakes
- `/prediction`: Get prediction for earthquake activity for the next day

## Data Source

This application uses the USGS Earthquake API for real-time earthquake data.

## Note

The prediction model used in this application is a simple linear regression based on historical patterns. It should not be used as a sole source for earthquake predictions or emergency planning.