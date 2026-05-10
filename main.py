"""
Weather Forecast & Alert Application
Main entry point for the weather monitoring system
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from weather_app import WeatherApp
from alert_engine import AlertEngine
from data_processor import DataProcessor


def main():
    """Main application function"""
    parser = argparse.ArgumentParser(description='Weather Forecast & Alert Application')
    parser.add_argument('--city', type=str, default='London', help='City name for weather forecast')
    parser.add_argument('--simulation', action='store_true', help='Use simulation mode (no API key required)')
    parser.add_argument('--save-report', action='store_true', help='Save weather report to CSV')
    parser.add_argument('--generate-charts', action='store_true', help='Generate weather charts')
    parser.add_argument('--show-statistics', action='store_true', help='Display weather statistics')
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('WEATHER_API_KEY')
    
    # Initialize components
    print("🌤️  Weather Forecast & Alert Application")
    print("=" * 50)
    
    try:
        # Initialize weather app
        weather_app = WeatherApp(api_key=api_key)
        alert_engine = AlertEngine()
        data_processor = DataProcessor()
        
        # Get weather data
        print(f"📍 Fetching weather data for {args.city}...")
        weather_data = weather_app.get_weather(args.city, use_simulation=args.simulation)
        
        # Display weather information
        weather_app.display_weather(weather_data)
        
        # Check for alerts
        print("\n" + "=" * 50)
        alerts = alert_engine.check_alerts(weather_data)
        alert_engine.display_alerts(alerts)
        
        # Display alert summary
        alert_summary = alert_engine.get_alert_summary(alerts)
        if sum(alert_summary.values()) > 0:
            print(f"\n📊 Alert Summary: {alert_summary['critical']} Critical, {alert_summary['warning']} Warning, {alert_summary['info']} Info")
        
        # Display statistics if requested
        if args.show_statistics:
            print("\n" + "=" * 50)
            data_processor.display_weather_statistics(weather_data)
        
        # Save report if requested
        if args.save_report:
            print("\n" + "=" * 50)
            report_path = weather_app.save_report(weather_data)
            if report_path:
                print(f"✅ Report saved successfully!")
        
        # Generate charts if requested
        if args.generate_charts:
            print("\n" + "=" * 50)
            print("📈 Generating weather charts...")
            
            try:
                temp_chart_path = data_processor.create_temperature_chart(weather_data)
                if temp_chart_path:
                    print(f"✅ Temperature chart saved: {temp_chart_path}")
                
                overview_chart_path = data_processor.create_weather_overview_chart(weather_data)
                if overview_chart_path:
                    print(f"✅ Weather overview chart saved: {overview_chart_path}")
                
                # Export data to CSV
                csv_path = data_processor.export_to_csv(weather_data)
                if csv_path:
                    print(f"✅ Data exported to CSV: {csv_path}")
                    
            except Exception as e:
                print(f"⚠️  Chart generation failed: {str(e)}")
                print("   This might be due to missing matplotlib. Install with: pip install matplotlib")
        
        # Notification check
        if alert_engine.should_send_notification(alerts):
            notification_message = alert_engine.format_for_notification(alerts)
            print(f"\n📱 NOTIFICATION RECOMMENDED:")
            print(notification_message)
        
        print("\n" + "=" * 50)
        print("✅ Weather analysis completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
        if "API" in str(e) and not args.simulation:
            print("\n💡 Suggestions:")
            print("   1. Check your API key in .env file")
            print("   2. Run with --simulation flag to use sample data")
            print("   3. Verify city name spelling")
        
        sys.exit(1)


def interactive_mode():
    """Interactive mode for user input"""
    print("🌤️  Weather Forecast & Alert Application - Interactive Mode")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('WEATHER_API_KEY')
    
    # Initialize components
    weather_app = WeatherApp(api_key=api_key)
    alert_engine = AlertEngine()
    data_processor = DataProcessor()
    
    while True:
        print("\n" + "=" * 60)
        print("📋 MENU OPTIONS:")
        print("1. Check weather for a city")
        print("2. Use simulation mode (sample data)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            city = input("Enter city name: ").strip()
            if not city:
                print("❌ City name cannot be empty!")
                continue
            
            try:
                weather_data = weather_app.get_weather(city, use_simulation=False)
                process_weather_data(weather_app, alert_engine, data_processor, weather_data)
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                print("💡 Try simulation mode or check your API key")
        
        elif choice == '2':
            print("\n📊 Available sample cities: London, New York, Mumbai")
            city = input("Enter city name from sample data: ").strip()
            
            if not city:
                print("❌ City name cannot be empty!")
                continue
            
            try:
                weather_data = weather_app.get_weather(city, use_simulation=True)
                process_weather_data(weather_app, alert_engine, data_processor, weather_data)
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        elif choice == '3':
            print("👋 Thank you for using Weather Forecast & Alert Application!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")


def process_weather_data(weather_app, alert_engine, data_processor, weather_data):
    """Process and display weather data"""
    # Display weather
    weather_app.display_weather(weather_data)
    
    # Check alerts
    alerts = alert_engine.check_alerts(weather_data)
    alert_engine.display_alerts(alerts)
    
    # Display statistics
    data_processor.display_weather_statistics(weather_data)
    
    # Ask for additional options
    print("\n" + "=" * 50)
    print("🔧 ADDITIONAL OPTIONS:")
    save_report = input("Save report to CSV? (y/n): ").strip().lower() == 'y'
    generate_charts = input("Generate weather charts? (y/n): ").strip().lower() == 'y'
    
    if save_report:
        report_path = weather_app.save_report(weather_data)
        if report_path:
            print(f"✅ Report saved: {report_path}")
    
    if generate_charts:
        try:
            temp_chart_path = data_processor.create_temperature_chart(weather_data)
            overview_chart_path = data_processor.create_weather_overview_chart(weather_data)
            csv_path = data_processor.export_to_csv(weather_data)
            
            print(f"✅ Charts and data saved successfully!")
        except Exception as e:
            print(f"⚠️  Chart generation failed: {str(e)}")


if __name__ == "__main__":
    # Check if running in interactive mode
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        main()
