"""
Weather Dashboard using Streamlit
Interactive web interface for weather monitoring
"""

import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from weather_app import WeatherApp
from alert_engine import AlertEngine
from data_processor import DataProcessor


def main():
    """Main dashboard application"""
    st.set_page_config(
        page_title="Weather Forecast & Alert Dashboard",
        page_icon="🌤️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #1f77b4;
            margin-bottom: 2rem;
        }
        .alert-critical {
            background-color: #ffcccc;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #ff0000;
            margin: 0.5rem 0;
        }
        .alert-warning {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #ffc107;
            margin: 0.5rem 0;
        }
        .alert-info {
            background-color: #d1ecf1;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #17a2b8;
            margin: 0.5rem 0;
        }
        .metric-card {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #dee2e6;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🌤️ Weather Forecast & Alert Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("⚙️ Settings")
    
    # API Key input
    api_key = st.sidebar.text_input(
        "OpenWeatherMap API Key",
        type="password",
        help="Get your free API key from https://openweathermap.org/api"
    )
    
    # Mode selection
    mode = st.sidebar.radio(
        "Data Source",
        ["API Mode", "Simulation Mode"],
        help="API Mode uses real weather data, Simulation Mode uses sample data"
    )
    
    use_simulation = mode == "Simulation Mode"
    
    # City input
    if use_simulation:
        st.sidebar.info("Sample cities available: London, New York, Mumbai")
        city = st.sidebar.selectbox("Select City", ["London", "New York", "Mumbai"])
    else:
        city = st.sidebar.text_input("Enter City Name", "London", help="Enter any city name")
    
    # Action buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        fetch_button = st.button("🔄 Fetch Weather", type="primary")
    
    with col2:
        if st.button("📊 Generate Charts"):
            if 'weather_data' in st.session_state:
                generate_charts(st.session_state.weather_data)
    
    # Initialize session state
    if 'weather_data' not in st.session_state:
        st.session_state.weather_data = None
    if 'alerts' not in st.session_state:
        st.session_state.alerts = []
    
    # Fetch weather data
    if fetch_button:
        if not use_simulation and not api_key:
            st.sidebar.error("Please enter an API key for API mode!")
        else:
            with st.spinner("Fetching weather data..."):
                try:
                    # Initialize components
                    weather_app = WeatherApp(api_key=api_key if not use_simulation else None)
                    alert_engine = AlertEngine()
                    
                    # Get weather data
                    weather_data = weather_app.get_weather(city, use_simulation=use_simulation)
                    
                    # Check alerts
                    alerts = alert_engine.check_alerts(weather_data)
                    
                    # Store in session state
                    st.session_state.weather_data = weather_data
                    st.session_state.alerts = alerts
                    
                    st.success(f"Weather data fetched successfully for {city}!")
                    
                except Exception as e:
                    st.error(f"Error fetching weather data: {str(e)}")
    
    # Display weather data
    if st.session_state.weather_data:
        display_weather_dashboard(st.session_state.weather_data, st.session_state.alerts)
    else:
        # Display welcome message
        st.markdown("""
        ## 🌍 Welcome to Weather Forecast & Alert Dashboard
        
        ### Features:
        - **Real-time Weather Data**: Fetch current weather and forecasts for any city
        - **Intelligent Alerts**: Automatic notifications for dangerous weather conditions
        - **Interactive Charts**: Visualize weather trends and patterns
        - **Data Export**: Download weather reports and data
        
        ### Getting Started:
        1. **API Mode**: Enter your OpenWeatherMap API key and any city name
        2. **Simulation Mode**: Use sample data without API key (London, New York, Mumbai)
        3. Click "🔄 Fetch Weather" to get started
        
        ### About:
        This dashboard helps you monitor weather conditions and receive timely alerts for:
        - Extreme temperatures (heat waves, cold snaps)
        - Heavy rain and storms
        - High winds and severe weather
        - Low visibility conditions
        """)


def display_weather_dashboard(weather_data, alerts):
    """Display comprehensive weather dashboard"""
    
    # Current Weather Section
    st.markdown("## 🌡️ Current Weather")
    
    current = weather_data['current']
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Temperature",
            f"{current['temperature']}°C",
            f"Feels like {current['feels_like']}°C"
        )
    
    with col2:
        st.metric(
            "Humidity",
            f"{current['humidity']}%",
            "High" if current['humidity'] > 70 else "Normal"
        )
    
    with col3:
        st.metric(
            "Wind Speed",
            f"{current['wind_speed']} km/h",
            current['wind_direction']
        )
    
    with col4:
        st.metric(
            "Weather",
            current['weather'],
            current['description']
        )
    
    # Additional current weather details
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**👁️ Visibility:** {current['visibility']} km")
    
    with col2:
        st.markdown(f"**📊 Pressure:** {current['pressure']} hPa")
    
    with col3:
        st.markdown(f"**☀️ UV Index:** {current.get('uv_index', 'N/A')}")
    
    # Alerts Section
    st.markdown("## ⚠️ Weather Alerts")
    
    if alerts:
        for alert in alerts:
            severity_class = f"alert-{alert['severity']}"
            st.markdown(f"""
            <div class="{severity_class}">
                <strong>{alert['severity'].upper()}:</strong> {alert['message']}<br>
                <em>💡 {alert['recommendation']}</em>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No weather alerts at this time")
    
    # Forecast Section
    st.markdown("## 📊 5-Day Forecast")
    
    forecast = weather_data['forecast']
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame(forecast)
    forecast_df['Date'] = pd.to_datetime(forecast_df['date']).dt.strftime('%a, %b %d')
    
    # Display forecast table
    st.dataframe(
        forecast_df[['Date', 'temp_max', 'temp_min', 'humidity', 'rain_probability', 'wind_speed', 'weather']],
        column_config={
            'Date': 'Date',
            'temp_max': 'Max Temp (°C)',
            'temp_min': 'Min Temp (°C)',
            'humidity': 'Humidity (%)',
            'rain_probability': 'Rain Chance (%)',
            'wind_speed': 'Wind (km/h)',
            'weather': 'Conditions'
        },
        hide_index=True
    )
    
    # Charts Section
    st.markdown("## 📈 Weather Trends")
    
    # Temperature chart
    fig_temp = go.Figure()
    
    dates = ['Current'] + [day['date'] for day in forecast]
    max_temps = [current['temperature']] + [day['temp_max'] for day in forecast]
    min_temps = [current['temperature']] + [day['temp_min'] for day in forecast]
    
    fig_temp.add_trace(go.Scatter(
        x=dates,
        y=max_temps,
        mode='lines+markers',
        name='Max Temperature',
        line=dict(color='red', width=3),
        marker=dict(size=8)
    ))
    
    fig_temp.add_trace(go.Scatter(
        x=dates,
        y=min_temps,
        mode='lines+markers',
        name='Min Temperature',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    fig_temp.update_layout(
        title=f'Temperature Trend - {weather_data["city"]}',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Rain probability chart
    fig_rain = go.Figure()
    
    rain_probs = [current.get('rain_probability', 0)] + [day['rain_probability'] for day in forecast]
    
    fig_rain.add_trace(go.Bar(
        x=dates,
        y=rain_probs,
        name='Rain Probability',
        marker_color='skyblue',
        text=rain_probs,
        textposition='auto'
    ))
    
    fig_rain.update_layout(
        title=f'Rain Probability - {weather_data["city"]}',
        xaxis_title='Date',
        yaxis_title='Probability (%)',
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig_rain, use_container_width=True)
    
    # Export options
    st.markdown("## 💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download CSV Report"):
            csv_data = create_csv_report(weather_data, alerts)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"weather_report_{weather_data['city']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Download JSON"):
            json_data = json.dumps({
                'weather_data': weather_data,
                'alerts': alerts,
                'timestamp': datetime.now().isoformat()
            }, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"weather_data_{weather_data['city']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("📊 Generate Full Report"):
            generate_full_report(weather_data, alerts)


def create_csv_report(weather_data, alerts):
    """Create CSV report for download"""
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Weather Report', ''])
    writer.writerow(['City', weather_data['city']])
    writer.writerow(['Timestamp', weather_data['timestamp']])
    writer.writerow(['Source', weather_data['source']])
    writer.writerow(['', ''])
    
    # Current weather
    writer.writerow(['Current Weather', ''])
    current = weather_data['current']
    for key, value in current.items():
        writer.writerow([key.replace('_', ' ').title(), value])
    
    # Alerts
    writer.writerow(['', ''])
    writer.writerow(['Alerts', ''])
    for alert in alerts:
        writer.writerow([alert['severity'].upper(), alert['message']])
        writer.writerow(['Recommendation', alert['recommendation']])
        writer.writerow(['', ''])
    
    # Forecast
    writer.writerow(['5-Day Forecast', ''])
    writer.writerow(['Date', 'Max Temp (°C)', 'Min Temp (°C)', 'Humidity (%)', 
                    'Rain Probability (%)', 'Wind Speed (km/h)', 'Weather', 'Description'])
    
    for day in weather_data['forecast']:
        writer.writerow([
            day['date'], day['temp_max'], day['temp_min'], day['humidity'],
            day['rain_probability'], day['wind_speed'], day['weather'], day['description']
        ])
    
    return output.getvalue()


def generate_charts(weather_data):
    """Generate and display additional charts"""
    st.markdown("## 📊 Advanced Weather Analysis")
    
    # Create multiple charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Humidity trend
        forecast = weather_data['forecast']
        dates = [day['date'] for day in forecast]
        humidities = [day['humidity'] for day in forecast]
        
        fig_humidity = px.line(
            x=dates, y=humidities,
            title='Humidity Trend',
            labels={'x': 'Date', 'y': 'Humidity (%)'}
        )
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    with col2:
        # Wind speed trend
        wind_speeds = [day['wind_speed'] for day in forecast]
        
        fig_wind = px.line(
            x=dates, y=wind_speeds,
            title='Wind Speed Trend',
            labels={'x': 'Date', 'y': 'Wind Speed (km/h)'}
        )
        st.plotly_chart(fig_wind, use_container_width=True)


def generate_full_report(weather_data, alerts):
    """Generate comprehensive report"""
    st.markdown("## 📋 Comprehensive Weather Report")
    
    # Summary statistics
    forecast = weather_data['forecast']
    
    temps_max = [day['temp_max'] for day in forecast]
    temps_min = [day['temp_min'] for day in forecast]
    humidities = [day['humidity'] for day in forecast]
    rain_probs = [day['rain_probability'] for day in forecast]
    
    st.markdown("### 📊 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Max Temp", f"{sum(temps_max)/len(temps_max):.1f}°C")
    
    with col2:
        st.metric("Avg Humidity", f"{sum(humidities)/len(humidities):.1f}%")
    
    with col3:
        st.metric("Max Rain Chance", f"{max(rain_probs)}%")
    
    with col4:
        st.metric("Active Alerts", str(len(alerts)))
    
    # Detailed analysis
    st.markdown("### 🔍 Detailed Analysis")
    
    # Weather patterns
    weather_types = [day['weather'] for day in forecast]
    weather_counts = {}
    for weather in weather_types:
        weather_counts[weather] = weather_counts.get(weather, 0) + 1
    
    st.write("**Weather Pattern Distribution:**")
    for weather, count in weather_counts.items():
        st.write(f"- {weather}: {count} day(s)")


if __name__ == "__main__":
    main()
