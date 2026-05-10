"""
Alert Engine Module
Handles weather alert generation and threshold checking
"""

from typing import Dict, List, Tuple
from datetime import datetime
import os


class AlertEngine:
    """Weather alert engine for generating weather-based alerts"""
    
    def __init__(self):
        """Initialize alert engine with default thresholds"""
        self.thresholds = self._load_thresholds()
        self.alert_history = []
    
    def _load_thresholds(self) -> Dict:
        """Load alert thresholds from environment or defaults"""
        return {
            'temp_high': float(os.getenv('TEMP_HIGH_THRESHOLD', 35.0)),
            'temp_low': float(os.getenv('TEMP_LOW_THRESHOLD', 0.0)),
            'humidity_high': float(os.getenv('HUMIDITY_HIGH_THRESHOLD', 80.0)),
            'rain_probability': float(os.getenv('RAIN_PROBABILITY_THRESHOLD', 60.0)),
            'wind_speed': float(os.getenv('WIND_SPEED_THRESHOLD', 30.0)),
            'uv_high': float(os.getenv('UV_HIGH_THRESHOLD', 8.0)),
            'visibility_low': float(os.getenv('VISIBILITY_LOW_THRESHOLD', 5.0))
        }
    
    def check_alerts(self, weather_data: Dict) -> List[Dict]:
        """
        Check weather data against thresholds and generate alerts
        
        Args:
            weather_data: Dictionary containing current and forecast weather data
            
        Returns:
            List of alert dictionaries
        """
        alerts = []
        current = weather_data['current']
        forecast = weather_data['forecast']
        
        # Check current weather alerts
        alerts.extend(self._check_current_alerts(current))
        
        # Check forecast alerts
        alerts.extend(self._check_forecast_alerts(forecast))
        
        # Remove duplicates and sort by severity
        unique_alerts = self._deduplicate_alerts(alerts)
        sorted_alerts = sorted(unique_alerts, key=lambda x: self._severity_priority(x['severity']), reverse=True)
        
        self.alert_history.extend(sorted_alerts)
        return sorted_alerts
    
    def _check_current_alerts(self, current: Dict) -> List[Dict]:
        """Check current weather conditions for alerts"""
        alerts = []
        
        # Temperature alerts
        temp = current.get('temperature', 0)
        if temp >= self.thresholds['temp_high']:
            alerts.append({
                'type': 'temperature',
                'severity': 'critical',
                'message': f"EXTREME HEAT: Temperature {temp}°C exceeds safe limit of {self.thresholds['temp_high']}°C",
                'recommendation': 'Stay indoors, stay hydrated, avoid outdoor activities',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        elif temp <= self.thresholds['temp_low']:
            alerts.append({
                'type': 'temperature',
                'severity': 'warning',
                'message': f"COLD ALERT: Temperature {temp}°C below safe limit of {self.thresholds['temp_low']}°C",
                'recommendation': 'Dress warmly, protect exposed skin, be cautious of ice',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Humidity alerts
        humidity = current.get('humidity', 0)
        if humidity >= self.thresholds['humidity_high']:
            alerts.append({
                'type': 'humidity',
                'severity': 'info',
                'message': f"HIGH HUMIDITY: Humidity level {humidity}% is very high",
                'recommendation': 'May feel uncomfortable, risk of mold growth',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Wind alerts
        wind_speed = current.get('wind_speed', 0)
        if wind_speed >= self.thresholds['wind_speed']:
            alerts.append({
                'type': 'wind',
                'severity': 'warning',
                'message': f"HIGH WIND: Wind speed {wind_speed} km/h exceeds {self.thresholds['wind_speed']} km/h",
                'recommendation': 'Secure outdoor objects, avoid high-profile vehicles',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # UV alerts
        uv_index = current.get('uv_index', 0)
        if uv_index >= self.thresholds['uv_high']:
            alerts.append({
                'type': 'uv',
                'severity': 'warning',
                'message': f"HIGH UV INDEX: UV level {uv_index} is dangerous",
                'recommendation': 'Wear sunscreen, protective clothing, avoid midday sun',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Visibility alerts
        visibility = current.get('visibility', 100)
        if visibility <= self.thresholds['visibility_low']:
            alerts.append({
                'type': 'visibility',
                'severity': 'warning',
                'message': f"LOW VISIBILITY: Visibility reduced to {visibility} km",
                'recommendation': 'Drive carefully, use headlights, consider postponing travel',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return alerts
    
    def _check_forecast_alerts(self, forecast: List[Dict]) -> List[Dict]:
        """Check forecast weather conditions for alerts"""
        alerts = []
        
        # Check next 3 days for concerning conditions
        for day in forecast[:3]:
            date = day['date']
            temp_max = day.get('temp_max', 0)
            rain_prob = day.get('rain_probability', 0)
            wind_speed = day.get('wind_speed', 0)
            weather = day.get('weather', '').lower()
            
            # Extreme heat forecast
            if temp_max >= self.thresholds['temp_high']:
                alerts.append({
                    'type': 'forecast_heat',
                    'severity': 'critical',
                    'message': f"HEAT WAVE FORECAST: {temp_max}°C expected on {date}",
                    'recommendation': 'Plan indoor activities, prepare cooling measures',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'forecast_date': date
                })
            
            # High rain probability
            if rain_prob >= self.thresholds['rain_probability']:
                severity = 'critical' if rain_prob >= 80 else 'warning'
                alerts.append({
                    'type': 'forecast_rain',
                    'severity': severity,
                    'message': f"HEAVY RAIN EXPECTED: {rain_prob}% chance on {date}",
                    'recommendation': 'Plan indoor activities, check drainage, avoid flood-prone areas',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'forecast_date': date
                })
            
            # Storm conditions
            if any(storm in weather for storm in ['thunderstorm', 'storm', 'tornado']):
                alerts.append({
                    'type': 'forecast_storm',
                    'severity': 'critical',
                    'message': f"STORM WARNING: {weather.title()} expected on {date}",
                    'recommendation': 'Seek shelter, secure property, monitor weather updates',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'forecast_date': date
                })
            
            # High wind forecast
            if wind_speed >= self.thresholds['wind_speed']:
                alerts.append({
                    'type': 'forecast_wind',
                    'severity': 'warning',
                    'message': f"WIND ADVISORY: {wind_speed} km/h winds expected on {date}",
                    'recommendation': 'Secure outdoor items, avoid travel if possible',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'forecast_date': date
                })
        
        return alerts
    
    def _deduplicate_alerts(self, alerts: List[Dict]) -> List[Dict]:
        """Remove duplicate alerts based on type and message"""
        seen = set()
        unique_alerts = []
        
        for alert in alerts:
            # Create a unique key based on alert type and main message
            key = (alert['type'], alert['message'].split(':')[0])
            
            if key not in seen:
                seen.add(key)
                unique_alerts.append(alert)
        
        return unique_alerts
    
    def _severity_priority(self, severity: str) -> int:
        """Return priority level for sorting alerts"""
        priorities = {'critical': 3, 'warning': 2, 'info': 1}
        return priorities.get(severity.lower(), 0)
    
    def display_alerts(self, alerts: List[Dict]):
        """Display alerts in a formatted way"""
        if not alerts:
            print("\n✅ No weather alerts at this time")
            return
        
        print(f"\n⚠️  WEATHER ALERTS ({len(alerts)} active)")
        print("═══════════════════════════════════════")
        
        for i, alert in enumerate(alerts, 1):
            severity_icon = {'critical': '🔴', 'warning': '🟡', 'info': '🔵'}
            icon = severity_icon.get(alert['severity'], '⚪')
            
            print(f"{icon} {alert['message']}")
            print(f"   💡 Recommendation: {alert['recommendation']}")
            if 'forecast_date' in alert:
                print(f"   📅 Date: {alert['forecast_date']}")
            print(f"   🕐 Time: {alert['timestamp']}")
            print()
    
    def get_alert_summary(self, alerts: List[Dict]) -> Dict:
        """Get a summary of alerts by severity"""
        summary = {'critical': 0, 'warning': 0, 'info': 0}
        
        for alert in alerts:
            severity = alert['severity'].lower()
            if severity in summary:
                summary[severity] += 1
        
        return summary
    
    def should_send_notification(self, alerts: List[Dict]) -> bool:
        """Determine if alerts are severe enough to warrant notification"""
        return any(alert['severity'] == 'critical' for alert in alerts)
    
    def format_for_notification(self, alerts: List[Dict]) -> str:
        """Format alerts for notification (SMS/email)"""
        if not alerts:
            return "No weather alerts"
        
        critical_alerts = [a for a in alerts if a['severity'] == 'critical']
        warning_alerts = [a for a in alerts if a['severity'] == 'warning']
        
        message_parts = []
        
        if critical_alerts:
            message_parts.append(f"🚨 CRITICAL: {len(critical_alerts)} critical alert(s)")
            for alert in critical_alerts[:2]:  # Limit to 2 most critical
                message_parts.append(f"• {alert['message']}")
        
        if warning_alerts:
            message_parts.append(f"⚠️ WARNING: {len(warning_alerts)} warning(s)")
            for alert in warning_alerts[:1]:  # Limit to 1 warning
                message_parts.append(f"• {alert['message']}")
        
        return '\n'.join(message_parts)
