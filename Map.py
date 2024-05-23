from tkinter import *
from PIL import Image, ImageTk
import folium
import os
from selenium import webdriver  # pip install selenium webdriver-manager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


class Map:
    def __init__(self):
        self.latitude = 0
        self.longitude = 0

    def get_coordinate(self):
        return (self.latitude, self.longitude)

    def show_map(self, frame, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

        map_osm = folium.Map(location=[self.latitude, self.longitude], zoom_start=10)
        folium.Marker([self.latitude, self.longitude]).add_to(map_osm)
        map_osm.save('osm.html')
        self.save_map_as_image('osm.html', 'osm.png')
        map_image = Image.open('osm.png')
        map_photo = ImageTk.PhotoImage(map_image)

        self.map = Canvas(frame)
        self.map.create_image(400, 80, image=map_photo)
        self.map.image_names = map_photo
        self.map.grid(row=0, column=0, sticky="nsew")

    def save_map_as_image(self, map_file, output_file):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('window-size=1024x768')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        driver.get('file://' + os.path.realpath(map_file))
        time.sleep(2.5)  # 지도 로딩 시간

        driver.save_screenshot(output_file)
        driver.quit()
