# Weather Forecast & Alert Application

A Python-based weather monitoring system that fetches real-time weather data, analyzes conditions, and generates automated alerts for potentially dangerous weather.

## 🌟 Features

- **Real-time Weather Data**: Fetch current weather and forecasts for any city
- **Intelligent Alerts**: Automatic notifications for rain, heat waves, high humidity, and storms
- **Report Generation**: CSV reports with weather data and alerts
- **Data Visualization**: Temperature and weather trend charts
- **Simulation Mode**: Works without API keys using sample data
- **Easy Setup**: Beginner-friendly with minimal dependencies

## 🎯 Problem Statement

Traditional weather apps require manual checking multiple times daily. This system automatically monitors weather conditions and alerts users to potential dangers, helping:
- **Travelers** avoid weather emergencies
- **Event planners** reschedule outdoor activities
- **Farmers** optimize planting/harvesting windows
- **Logistics companies** reroute shipments around storms

## 🛠️ Tech Stack

- **Core**: Python 3.8+, requests, JSON, datetime
- **Data Processing**: pandas (optional)
- **Visualization**: matplotlib
- **Interface**: Streamlit (web dashboard)
- **API**: OpenWeatherMap (free tier available)
- **Storage**: CSV files for reports

## 📁 Project Structure

```
Weather-Forecast-Alert-Application/
│
├── data/              # Sample weather data for simulation
│   └── sample_weather.json
├── src/               # Core application code
│   ├── weather_app.py
│   ├── alert_engine.py
│   └── data_processor.py
├── outputs/           # Generated reports and charts
│   └── weather_reports/
├── images/            # Screenshots and visualizations
├── reports/           # CSV weather reports
├── docs/              # Documentation
├── main.py            # Main application entry point
├── dashboard.py       # Streamlit dashboard
├── requirements.txt   # Python dependencies
├── .env.example      # Environment variables template
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Weather-Forecast-Alert-Application.git
cd Weather-Forecast-Alert-Application
```

2. **Create virtual environment**
```bash
python -m venv weather_env
source weather_env/bin/activate  # On Windows: weather_env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up API key (optional)**
```bash
cp .env.example .env
# Edit .env and add your OpenWeatherMap API key
```

### Running the Application

**Option 1: Terminal Mode**
```bash
python main.py
```

**Option 2: Web Dashboard**
```bash
streamlit run dashboard.py
```

**Option 3: Simulation Mode (no API key required)**
```bash
python main.py --simulation
```

## 📊 Usage Examples

### Basic Weather Check
```python
from src.weather_app import WeatherApp

app = WeatherApp()
weather_data = app.get_weather("London")
app.display_weather(weather_data)
```

### Alert System
```python
from src.alert_engine import AlertEngine

alerts = AlertEngine()
alert_results = alerts.check_alerts(weather_data)
alerts.display_alerts(alert_results)
```

## 🔧 Configuration

### Alert Thresholds
Edit `src/alert_engine.py` to customize:
- Temperature thresholds (°C)
- Humidity thresholds (%)
- Rain probability (%)
- Wind speed thresholds (km/h)

### API Settings
- **OpenWeatherMap**: Free 1000 calls/day
- **WeatherAPI**: Free 1M calls/month
- **Simulation Mode**: Uses sample data, no API required

## 📈 Sample Output

```
🌤️  WEATHER REPORT FOR LONDON
═══════════════════════════════════════

📍 Location: London, GB
🕐 Time: 2024-01-15 14:30:00
🌡️  Temperature: 12.5°C (feels like 10.2°C)
💧 Humidity: 78%
🌧️  Rain Probability: 65%
💨 Wind Speed: 15 km/h

⚠️  WEATHER ALERTS
═══════════════════════════════════════
🔴 HIGH RAIN ALERT: 65% chance of rain in next 6 hours
🟡 MODERATE WIND: Wind speed 15 km/h detected

📊 5-DAY FORECAST
═══════════════════════════════════════
Tomorrow: 14°C / 8°C, Light rain (40%)
Day 3: 16°C / 9°C, Partly cloudy (20%)
Day 4: 18°C / 11°C, Sunny (10%)
Day 5: 15°C / 7°C, Rainy (60%)
```

## 🎓 Learning Outcomes

By building this project, you'll learn:
- **API Integration**: Working with REST APIs and JSON data
- **Data Processing**: Parsing, validation, and transformation
- **Error Handling**: Robust exception management
- **File Operations**: CSV generation and data storage
- **Visualization**: Creating charts and graphs
- **Web Development**: Building interactive dashboards
- **Best Practices**: Code organization, documentation, Git

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for weather data API
- [Streamlit](https://streamlit.io/) for the web framework
- [Matplotlib](https://matplotlib.org/) for data visualization

## 📞 Contact

- **Author**: Prarthana Sumesh Panikar
- **Email**: prarthanapanikar@gmail.com
- **GitHub**: [https://github.com/yourusername
](https://github.com/PrarthanaPanikar/Weather-Forecast-Alert-Application.git)
