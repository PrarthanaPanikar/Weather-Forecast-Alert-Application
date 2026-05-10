"""
Data Processor Module
Handles data analysis, statistics, and visualization
"""

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os


class DataProcessor:
    """Data processor for weather analysis and visualization"""
    
    def __init__(self):
        """Initialize data processor"""
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set matplotlib style
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
    def analyze_weather_trends(self, weather_data: Dict) -> Dict:
        """
        Analyze weather trends from current and forecast data
        
        Args:
            weather_data: Dictionary containing weather data
            
        Returns:
            Dictionary with trend analysis
        """
        current = weather_data['current']
        forecast = weather_data['forecast']
        
        # Temperature trends
        temps = [day['temp_max'] for day in forecast]
        temp_trend = self._calculate_trend(temps)
        
        # Humidity trends
        humidities = [day['humidity'] for day in forecast]
        humidity_trend = self._calculate_trend(humidities)
        
        # Rain probability trends
        rain_probs = [day['rain_probability'] for day in forecast]
        rain_trend = self._calculate_trend(rain_probs)
        
        # Wind speed trends
        wind_speeds = [day['wind_speed'] for day in forecast]
        wind_trend = self._calculate_trend(wind_speeds)
        
        return {
            'temperature': {
                'current': current['temperature'],
                'average_forecast': sum(temps) / len(temps),
                'max_forecast': max(temps),
                'min_forecast': min(temps),
                'trend': temp_trend
            },
            'humidity': {
                'current': current['humidity'],
                'average_forecast': sum(humidities) / len(humidities),
                'max_forecast': max(humidities),
                'min_forecast': min(humidities),
                'trend': humidity_trend
            },
            'rain_probability': {
                'current': current.get('rain_probability', 0),
                'average_forecast': sum(rain_probs) / len(rain_probs),
                'max_forecast': max(rain_probs),
                'min_forecast': min(rain_probs),
                'trend': rain_trend
            },
            'wind_speed': {
                'current': current['wind_speed'],
                'average_forecast': sum(wind_speeds) / len(wind_speeds),
                'max_forecast': max(wind_speeds),
                'min_forecast': min(wind_speeds),
                'trend': wind_trend
            }
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear trend calculation
        n = len(values)
        x = list(range(n))
        
        # Calculate slope
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def create_temperature_chart(self, weather_data: Dict, save_chart: bool = True) -> Optional[str]:
        """
        Create temperature trend chart
        
        Args:
            weather_data: Weather data dictionary
            save_chart: Whether to save the chart to file
            
        Returns:
            Path to saved chart file (if saved)
        """
        current = weather_data['current']
        forecast = weather_data['forecast']
        
        # Prepare data
        dates = ['Current'] + [day['date'] for day in forecast]
        temps = [current['temperature']] + [day['temp_max'] for day in forecast]
        min_temps = [current['temperature']] + [day['temp_min'] for day in forecast]
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot lines
        ax.plot(dates, temps, 'ro-', linewidth=2, markersize=8, label='Max Temperature')
        ax.plot(dates, min_temps, 'bo-', linewidth=2, markersize=8, label='Min Temperature')
        
        # Fill area between max and min
        ax.fill_between(dates, temps, min_temps, alpha=0.3, color='skyblue')
        
        # Customize
        ax.set_title(f'Temperature Trend - {weather_data["city"]}', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        
        # Add temperature zones
        ax.axhspan(35, 50, alpha=0.1, color='red', label='Extreme Heat Zone')
        ax.axhspan(-10, 0, alpha=0.1, color='blue', label='Cold Zone')
        
        plt.tight_layout()
        
        if save_chart:
            filename = f"temperature_chart_{weather_data['city']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return filepath
        else:
            plt.show()
            return None
    
    def create_weather_overview_chart(self, weather_data: Dict, save_chart: bool = True) -> Optional[str]:
        """
        Create comprehensive weather overview chart
        
        Args:
            weather_data: Weather data dictionary
            save_chart: Whether to save the chart to file
            
        Returns:
            Path to saved chart file (if saved)
        """
        forecast = weather_data['forecast']
        
        # Prepare data
        dates = [day['date'] for day in forecast]
        temps = [day['temp_max'] for day in forecast]
        humidity = [day['humidity'] for day in forecast]
        rain_prob = [day['rain_probability'] for day in forecast]
        wind_speed = [day['wind_speed'] for day in forecast]
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Weather Overview - {weather_data["city"]}', fontsize=16, fontweight='bold')
        
        # Temperature chart
        ax1.plot(dates, temps, 'ro-', linewidth=2, markersize=6)
        ax1.set_title('Temperature (°C)')
        ax1.set_ylabel('Temperature (°C)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Humidity chart
        ax2.plot(dates, humidity, 'bo-', linewidth=2, markersize=6)
        ax2.set_title('Humidity (%)')
        ax2.set_ylabel('Humidity (%)')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        # Rain probability chart
        ax3.bar(dates, rain_prob, color='skyblue', alpha=0.7)
        ax3.set_title('Rain Probability (%)')
        ax3.set_ylabel('Probability (%)')
        ax3.set_ylim(0, 100)
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # Wind speed chart
        ax4.plot(dates, wind_speed, 'go-', linewidth=2, markersize=6)
        ax4.set_title('Wind Speed (km/h)')
        ax4.set_ylabel('Wind Speed (km/h)')
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_chart:
            filename = f"weather_overview_{weather_data['city']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return filepath
        else:
            plt.show()
            return None
    
    def create_weather_summary_table(self, weather_data: Dict) -> pd.DataFrame:
        """
        Create a summary table of weather data
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            Pandas DataFrame with weather summary
        """
        current = weather_data['current']
        forecast = weather_data['forecast']
        
        # Create summary data
        summary_data = []
        
        # Current weather
        summary_data.append({
            'Date': 'Current',
            'Max Temp (°C)': current['temperature'],
            'Min Temp (°C)': current['temperature'],
            'Humidity (%)': current['humidity'],
            'Rain Probability (%)': current.get('rain_probability', 0),
            'Wind Speed (km/h)': current['wind_speed'],
            'Weather': current['weather']
        })
        
        # Forecast
        for day in forecast:
            summary_data.append({
                'Date': day['date'],
                'Max Temp (°C)': day['temp_max'],
                'Min Temp (°C)': day['temp_min'],
                'Humidity (%)': day['humidity'],
                'Rain Probability (%)': day['rain_probability'],
                'Wind Speed (km/h)': day['wind_speed'],
                'Weather': day['weather']
            })
        
        return pd.DataFrame(summary_data)
    
    def export_to_csv(self, weather_data: Dict, filename: Optional[str] = None) -> Optional[str]:
        """
        Export weather data to CSV file
        
        Args:
            weather_data: Weather data dictionary
            filename: Optional filename
            
        Returns:
            Path to saved CSV file
        """
        if filename is None:
            filename = f"weather_data_{weather_data['city']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create summary table
        df = self.create_weather_summary_table(weather_data)
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        
        return filepath
    
    def display_weather_statistics(self, weather_data: Dict):
        """Display weather statistics and trends"""
        trends = self._analyze_weather_trends(weather_data)
        
        print(f"\n📊 WEATHER STATISTICS FOR {weather_data['city'].upper()}")
        print("═══════════════════════════════════════")
        
        # Temperature statistics
        temp_stats = trends['temperature']
        print(f"🌡️  TEMPERATURE:")
        print(f"   Current: {temp_stats['current']}°C")
        print(f"   Forecast Average: {temp_stats['average_forecast']:.1f}°C")
        print(f"   Range: {temp_stats['min_forecast']:.1f}°C to {temp_stats['max_forecast']:.1f}°C")
        print(f"   Trend: {temp_stats['trend'].title()}")
        
        # Humidity statistics
        humidity_stats = trends['humidity']
        print(f"\n💧 HUMIDITY:")
        print(f"   Current: {humidity_stats['current']}%")
        print(f"   Forecast Average: {humidity_stats['average_forecast']:.1f}%")
        print(f"   Range: {humidity_stats['min_forecast']:.1f}% to {humidity_stats['max_forecast']:.1f}%")
        print(f"   Trend: {humidity_stats['trend'].title()}")
        
        # Rain probability statistics
        rain_stats = trends['rain_probability']
        print(f"\n🌧️  RAIN PROBABILITY:")
        print(f"   Current: {rain_stats['current']}%")
        print(f"   Forecast Average: {rain_stats['average_forecast']:.1f}%")
        print(f"   Range: {rain_stats['min_forecast']:.1f}% to {rain_stats['max_forecast']:.1f}%")
        print(f"   Trend: {rain_stats['trend'].title()}")
        
        # Wind speed statistics
        wind_stats = trends['wind_speed']
        print(f"\n💨 WIND SPEED:")
        print(f"   Current: {wind_stats['current']} km/h")
        print(f"   Forecast Average: {wind_stats['average_forecast']:.1f} km/h")
        print(f"   Range: {wind_stats['min_forecast']:.1f} to {wind_stats['max_forecast']:.1f} km/h")
        print(f"   Trend: {wind_stats['trend'].title()}")
    
    def _analyze_weather_trends(self, weather_data: Dict) -> Dict:
        """Analyze weather trends (internal method)"""
        current = weather_data['current']
        forecast = weather_data['forecast']
        
        # Temperature trends
        temps = [day['temp_max'] for day in forecast]
        temp_trend = self._calculate_trend(temps)
        
        # Humidity trends
        humidities = [day['humidity'] for day in forecast]
        humidity_trend = self._calculate_trend(humidities)
        
        # Rain probability trends
        rain_probs = [day['rain_probability'] for day in forecast]
        rain_trend = self._calculate_trend(rain_probs)
        
        # Wind speed trends
        wind_speeds = [day['wind_speed'] for day in forecast]
        wind_trend = self._calculate_trend(wind_speeds)
        
        return {
            'temperature': {
                'current': current['temperature'],
                'average_forecast': sum(temps) / len(temps),
                'max_forecast': max(temps),
                'min_forecast': min(temps),
                'trend': temp_trend
            },
            'humidity': {
                'current': current['humidity'],
                'average_forecast': sum(humidities) / len(humidities),
                'max_forecast': max(humidities),
                'min_forecast': min(humidities),
                'trend': humidity_trend
            },
            'rain_probability': {
                'current': current.get('rain_probability', 0),
                'average_forecast': sum(rain_probs) / len(rain_probs),
                'max_forecast': max(rain_probs),
                'min_forecast': min(rain_probs),
                'trend': rain_trend
            },
            'wind_speed': {
                'current': current['wind_speed'],
                'average_forecast': sum(wind_speeds) / len(wind_speeds),
                'max_forecast': max(wind_speeds),
                'min_forecast': min(wind_speeds),
                'trend': wind_trend
            }
        }
