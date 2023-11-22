import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        # API key from OpenWeatherMap
        self.api_key = "YOUR_OPENWEATHERMAP_API_KEY"

        # GUI components
        self.location_label = ttk.Label(root, text="Enter Location:")
        self.location_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.location_entry = ttk.Entry(root)
        self.location_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.search_button = ttk.Button(root, text="Search", command=self.get_weather)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.weather_label = ttk.Label(root, text="")
        self.weather_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.weather_icon_label = ttk.Label(root, image=None)
        self.weather_icon_label.grid(row=2, column=0, columnspan=3, pady=10)

    def get_weather(self):
        location = self.location_entry.get()

        if not location:
            return

        try:
            # API request to OpenWeatherMap
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
            response = requests.get(url)
            data = response.json()

            # Parse and display weather information
            weather_description = data["weather"][0]["description"].capitalize()
            temperature = round(data["main"]["temp"] - 273.15, 1)  # Convert Kelvin to Celsius

            # Display weather information
            weather_text = f"Location: {location}\nWeather: {weather_description}\nTemperature: {temperature}°C"
            self.weather_label.config(text=weather_text)

            # Display weather icon
            icon_id = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_id}.png"
            icon_data = requests.get(icon_url).content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_image = icon_image.resize((50, 50), Image.ANTIALIAS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.weather_icon_label.config(image=icon_photo)
            self.weather_icon_label.image = icon_photo
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            self.weather_label.config(text="Error fetching weather data.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
