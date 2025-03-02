import os
import requests
from dotenv import load_dotenv

def get_weather(city):
    load_dotenv()  # Load environment variables
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        return "Error: Please set your OpenWeather API key in the .env file"
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key.strip(),  # Ensure no whitespace in API key
        'units': 'metric'  # Use Celsius for temperature
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 401:
            return "Error: Invalid API key. Please check your OpenWeather API key"
        elif response.status_code == 404:
            return f"Error: City '{city}' not found"
        
        response.raise_for_status()
        weather_data = response.json()
        
        return f"""
Weather in {city}:
Temperature: {weather_data['main']['temp']}°C
Feels like: {weather_data['main']['feels_like']}°C
Humidity: {weather_data['main']['humidity']}%
Conditions: {weather_data['weather'][0]['description'].capitalize()}
Wind Speed: {weather_data['wind']['speed']} m/s
"""
    except requests.RequestException as e:
        return f"Error fetching weather data: {str(e)}"

def main():
    print("Welcome to the Weather App!")
    print("You can get current weather for any city in the world.")
    while True:
        city = input("\nEnter city name (or 'quit' to exit): ")
        if city.lower() == 'quit':
            print("Thank you for using the Weather App!")
            break
        print(get_weather(city))

if __name__ == "__main__":
    main()