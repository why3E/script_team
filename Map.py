from tkinter import *
from PIL import Image, ImageTk
import requests
import io

url = "https://naveropenapi.apigw.ntruss.com/map-static/v2/raster"
client_id = 'b5gc0qz8xe'
client_secret = 'rmjbtghgRe2yJDl0DZEPwK8BmBW9VSNKSanHZuWG'


class Map:
    def __init__(self):
        self.latitude = ''
        self.longitude = ''

    def get_coordinate(self):
        return (self.latitude, self.longitude)

    def show_map(self, frame, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
        }

        center = f'{longitude},{latitude}'
        level = 10  # 줌 레벨, 0 ~ 20
        width, height = 800, 160
        maptype = "basic"
        format = "png"
        scale = 1
        markers = f"type:d|size:mid|pos:{longitude} {latitude}|color:red"
        lang = "ko"
        public_transit = True
        dataversion = ""

        URL = f"{url}?center={center}&level={level}&w={width}&h={height}&maptype={maptype}&format={format}&scale={scale}&markers={markers}&lang={lang}&public_transit={public_transit}&dataversion={dataversion}"
        res = requests.get(URL, headers=headers)

        image_data = io.BytesIO(res.content)
        self.map_image = Image.open(image_data)
        map_photo = ImageTk.PhotoImage(self.map_image)

        self.map = Canvas(frame, bg='blue')
        self.map.bind('<Configure>', self.on_resize)
        self.map.create_image(400, 80, image=map_photo)
        self.map.image_names = map_photo
        self.map.grid(row=0, column=0, sticky="nsew")

    def on_resize(self, event):
        self.map.delete("all")
        # 가로 Down, 세로 Up
        if (self.map.winfo_height() > self.map.winfo_width() * 160 // 800):
            map_image = self.map_image.resize((800 * self.map.winfo_height() // 160, self.map.winfo_height()))
        else:
            map_image = self.map_image.resize((self.map.winfo_width(), self.map.winfo_width() * 160 // 800))
        map_photo = ImageTk.PhotoImage(map_image)

        self.map.create_image(self.map.winfo_width() // 2, self.map.winfo_height() // 2, anchor=CENTER, image=map_photo)
        self.map.image_names = map_photo
