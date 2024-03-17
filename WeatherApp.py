#importing modules

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import ttkbootstrap

#getting weather info function
def get_weather(city):
    API_key = "{Your API KEY from}"
    url = f"{Your url_adress from API website}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "Invalid city name")
        return None

    #JSON response to getweather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']
    icon_url = f"{Your icon_url from API website, including {icon_id}}"
    return (icon_url, temperature, description, city, country)

#searching function
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return 

    icon_url, temperature, description, city, country = result
    
    location_label.configure(text=f"{city}")
    
    try:
        # Fetching the image
        response = requests.get(icon_url, stream=True)
        if response.status_code == 200:
            # Checking if the response contains image data
            if 'image' in response.headers.get('Content-Type', ''):
                image = Image.open(response.raw)
                icon = ImageTk.PhotoImage(image)
                icon_label.configure(image=icon)
                icon_label.image = icon
            else:
                messagebox.showerror("Error", "Failed to fetch image: No image data received")
        else:
            messagebox.showerror("Error", f"Failed to fetch image: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch image: {str(e)}")

    temperature_label.configure(text=f"Temperature: {temperature:.2f}C")
    description_label.configure(text=f"Description: {description}")
#root form

root = ttkbootstrap.Window(themename="morph")
root.title("WeatherLiveApp")
root.geometry("400x400")

#widgets

city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

#buttons
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

#location label
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

#label icon
icon_label = tk.Label(root)
icon_label.pack()

#label temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

#description label
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()
