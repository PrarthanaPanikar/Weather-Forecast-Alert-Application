"""
Weather Application Module
Handles API requests, data fetching, and weather data processing
"""

import requests
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import csv


class WeatherApp:
    """Main weather application class"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize weather app with optional API key
        
        Args:
            api_key: OpenWeatherMap API key (optional for simulation mode)
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.sample_data = self._load_sample_data()
        
    def _load_sample_data(self) -> Dict:
        """Load sample weather data for simulation mode"""
        try:
            sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_weather.json')
            with open(sample_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  Sample data file not found. API mode required.")
            return {}
    
    def get_weather(self, city: str, use_simulation: bool = False) -> Dict:
        """
        Get weather data for a city
        
        Args:
            city: Name of the city
            use_simulation: Use sample data instead of API
            
        Returns:
            Dictionary containing weather data
        """
        if use_simulation or not self.api_key:
            return self._get_simulation_weather(city)
        else:
            return self._get_api_weather(city)
    
    def _get_simulation_weather(self, city: str) -> Dict:
        """Get weather data from sample data"""
        city_data = self.sample_data.get(city)
        
        if not city_data:
            available_cities = list(self.sample_data.keys())
            raise ValueError(f"City '{city}' not found in sample data. Available cities: {available_cities}")
        
        return {
            'city': city,
            'source': 'simulation',
            'current': city_data['current'],
            'forecast': city_data['forecast'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _get_api_weather(self, city: str) -> Dict:
        """Get weather data from OpenWeatherMap API"""
        try:
            # Get current weather
            current_url = f"{self.base_url}/weather"
            current_params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            current_response = requests.get(current_url, params=current_params)
            current_response.raise_for_status()
            current_data = current_response.json()
            
            # Get 5-day forecast
            forecast_url = f"{self.base_url}/forecast"
            forecast_params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            forecast_response = requests.get(forecast_url, params=forecast_params)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            # Process the data
            processed_current = self._process_current_data(current_data)
            processed_forecast = self._process_forecast_data(forecast_data)
            
            return {
                'city': city,
                'source': 'api',
                'current': processed_current,
                'forecast': processed_forecast,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except KeyError as e:
            raise Exception(f"Invalid API response format: {str(e)}")
    
    def _process_current_data(self, data: Dict) -> Dict:
        """Process current weather data from API response"""
        return {
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'visibility': data.get('visibility', 0) / 1000,  # Convert to km
            'uv_index': 0,  # Not available in free API
            'wind_speed': data['wind']['speed'] * 3.6,  # Convert m/s to km/h
            'wind_direction': self._degrees_to_direction(data['wind'].get('deg', 0)),
            'weather': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _process_forecast_data(self, data: Dict) -> List[Dict]:
        """Process forecast data from API response"""
        forecast_list = []
        
        # Group forecasts by date
        daily_forecasts = {}
        for item in data['list']:
            date = item['dt_txt'].split(' ')[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        # Process each day's forecast
        for date, forecasts in list(daily_forecasts.items())[:5]:  # Next 5 days
            temps = [f['main']['temp'] for f in forecasts]
            humidities = [f['main']['humidity'] for f in forecasts]
            wind_speeds = [f['wind']['speed'] * 3.6 for f in forecasts]  # Convert to km/h
            
            # Calculate rain probability (simplified)
            rain_prob = 0
            for f in forecasts:
                if 'rain' in f:
                    rain_prob = max(rain_prob, 60)
                elif f['weather'][0]['main'].lower() in ['rain', 'drizzle', 'thunderstorm']:
                    rain_prob = max(rain_prob, 40)
            
            forecast_list.append({
                'date': date,
                'temp_max': round(max(temps), 1),
                'temp_min': round(min(temps), 1),
                'humidity': round(sum(humidities) / len(humidities), 1),
                'rain_probability': rain_prob,
                'wind_speed': round(max(wind_speeds), 1),
                'weather': forecasts[0]['weather'][0]['main'],
                'description': forecasts[0]['weather'][0]['description']
            })
        
        return forecast_list
    
    def _degrees_to_direction(self, degrees: float) -> str:
        """Convert wind direction degrees to compass direction"""
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                      'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def display_weather(self, weather_data: Dict):
        """Display weather information in a formatted way"""
        print(f"\n🌤️  WEATHER REPORT FOR {weather_data['city'].upper()}")
        print("═══════════════════════════════════════")
        print(f"📍 Location: {weather_data['city']}")
        print(f"🕐 Time: {weather_data['timestamp']}")
        print(f"📡 Source: {weather_data['source'].upper()}")
        
        current = weather_data['current']
        print(f"\n🌡️  Temperature: {current['temperature']}°C (feels like {current['feels_like']}°C)")
        print(f"💧 Humidity: {current['humidity']}%")
        print(f"🌧️  Rain Probability: {current.get('rain_probability', 'N/A')}%")
        print(f"💨 Wind Speed: {current['wind_speed']} km/h ({current['wind_direction']})")
        print(f"🌤️  Weather: {current['weather']} - {current['description']}")
        print(f"👁️  Visibility: {current['visibility']} km")
        print(f"📊 Pressure: {current['pressure']} hPa")
        
        # Display forecast
        forecast = weather_data['forecast']
        print(f"\n📊 5-DAY FORECAST")
        print("═══════════════════════════════════════")
        
        for day in forecast:
            date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
            day_name = date_obj.strftime('%A')
            print(f"{day_name} ({day['date']}): {day['temp_max']}°C / {day['temp_min']}°C, "
                  f"{day['weather']} ({day['rain_probability']}% rain)")
    
    def save_report(self, weather_data: Dict, filename: Optional[str] = None):
        """Save weather report to CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weather_report_{weather_data['city']}_{timestamp}.csv"
        
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Weather Report', ''])
                writer.writerow(['City', weather_data['city']])
                writer.writerow(['Timestamp', weather_data['timestamp']])
                writer.writerow(['Source', weather_data['source']])
                writer.writerow(['', ''])
                
                # Write current weather
                writer.writerow(['Current Weather', ''])
                current = weather_data['current']
                for key, value in current.items():
                    writer.writerow([key.replace('_', ' ').title(), value])
                
                writer.writerow(['', ''])
                writer.writerow(['5-Day Forecast', ''])
                writer.writerow(['Date', 'Max Temp (°C)', 'Min Temp (°C)', 'Humidity (%)', 
                               'Rain Probability (%)', 'Wind Speed (km/h)', 'Weather', 'Description'])
                
                # Write forecast
                for day in weather_data['forecast']:
                    writer.writerow([
                        day['date'], day['temp_max'], day['temp_min'], day['humidity'],
                        day['rain_probability'], day['wind_speed'], day['weather'], day['description']
                    ])
            
            print(f"\n📄 Report saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving report: {str(e)}")
            return None
