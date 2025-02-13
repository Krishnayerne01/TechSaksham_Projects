import streamlit as st
import requests

# OpenWeather API Key
API_KEY = "775ccbf4bcdc18c8de6d16ed08774606"  # Replace with your actual OpenWeather API key

# Function to get weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Streamlit UI
st.set_page_config(page_title="🌦 OpenWeather App", page_icon="🌦", layout="centered")
st.title("🌦 OpenWeather App")

# Add a background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0");
        background-size: cover;
    }
    .weather-card {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .weather-card h2 {
        color: #333;
    }
    .weather-card p {
        font-size: 18px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# User Input
st.markdown("## Enter the name of a city to get the current weather:")
city = st.text_input("", "Mumbai")

if st.button("Get Weather"):
    weather_data = get_weather(city)
    
    if weather_data:
        st.markdown(
            f"""
            <div class="weather-card">
                <h2>Weather in {city}</h2>
                <p>🌡 <strong>Temperature:</strong> {weather_data['main']['temp']}°C</p>
                <p>🌬 <strong>Wind Speed:</strong> {weather_data['wind']['speed']} m/s</p>
                <p>🌤 <strong>Weather:</strong> {weather_data['weather'][0]['description'].title()}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("❌ City not found. Please enter a valid city name.")