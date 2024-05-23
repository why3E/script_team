from tkinter import *
from xmlRead import xmlRead
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
import folium
import os
from selenium import webdriver  # pip install selenium webdriver-manager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

Facilities = ['restaurant', 'cafe', 'store', 'nolibang', 'suyu', 'parkbarrier',
              'restbarrier', 'runwbarrier', 'elevbarrier', 'parkinglot']


class InfoFrame(Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)
        super().grid_rowconfigure(0, weight=1)
        super().grid_rowconfigure(1, weight=9)
        super().grid_rowconfigure(2, weight=3)
        super().grid_columnconfigure(0, weight=1)

        self.sub_frame1 = Frame(self)
        self.sub_frame1.grid(row=0, column=0, sticky="nsew")
        Button(self.sub_frame1, command=self.sendEmail).grid(row=0, column=0, sticky="nsew")
        Button(self.sub_frame1, command=self.addRemoveFavorite).grid(row=0, column=1, sticky="nsew")
        self.sub_frame1.grid_rowconfigure(0, weight=1)
        self.sub_frame1.grid_columnconfigure(0, weight=1)
        self.sub_frame1.grid_columnconfigure(1, weight=1)
        self.sub_frame1.grid_columnconfigure(2, weight=1)

        self.sub_frame2 = Frame(self)
        self.sub_frame2.grid_propagate(False)
        self.sub_frame2.grid(row=1, column=0, sticky="nsew")
        self.information = Listbox(self.sub_frame2)
        self.information.grid(row=0, column=0, sticky="nsew")
        self.sub_frame2.grid_rowconfigure(0, weight=1)
        self.sub_frame2.grid_columnconfigure(0, weight=2)

        self.sub_frame3 = Frame(self, bg='blue')
        self.sub_frame3.grid_propagate(False)
        self.sub_frame3.grid(row=2, column=0, sticky="nsew")
        self.sub_frame3.grid_rowconfigure(0, weight=1)
        self.sub_frame3.grid_columnconfigure(0, weight=1)

    def sendEmail(self):
        self.setInfo('PF132236')  # 테스트

    def addRemoveFavorite(self):
        pass

    def addFavorite(self):
        pass

    def removeFavorite(self):
        pass


class ShowInfoFrame(InfoFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.place_id = None

        Button(self.sub_frame1, command=self.showPlaceInfo).grid(row=0, column=2, sticky="nsew")

        self.information_xscroll = Scrollbar(self.information, orient='horizontal', command=self.information.xview)
        self.information_xscroll.pack(side="bottom", fill=X)
        self.information_yscroll = Scrollbar(self.information, orient='vertical', command=self.information.yview)
        self.information_yscroll.pack(side="right", fill=Y)
        self.information.configure(xscrollcommand=self.information_xscroll.set,
                                   yscrollcommand=self.information_yscroll.set)

        self.posters = []
        self.poster = Canvas(self.sub_frame2, bg='blue')
        self.poster.grid_propagate(False)
        self.poster.grid(row=0, column=1, sticky="nsew")

        self.poster_yscroll = Scrollbar(self.poster, orient='vertical', command=self.poster.yview)
        self.poster_yscroll.pack(side="right", fill=Y)
        self.poster.configure(yscrollcommand=self.poster_yscroll.set)

        self.sub_frame2.grid_columnconfigure(1, weight=1)

        self.urls = Listbox(self.sub_frame3)
        self.urls.grid(row=0, column=0, sticky="nsew")

    def getInfo(self, id):
        fetcher = xmlRead()

        self.data = fetcher.fetch_and_parse_show_detail_data(id)[0]

    def setInfo(self, id):
        self.posters.clear()
        self.poster.delete("all")
        self.urls.delete(0, END)
        self.place_id = None
        self.information.delete(0, END)

        self.getInfo(id)

        for k, v in self.data.items():
            if k == 'styurls':
                for url in v:
                    with urllib.request.urlopen(url) as u:
                        raw_data = u.read()
                    im = Image.open(BytesIO(raw_data))
                    im = im.resize(
                        (self.poster.winfo_width() - 19, (self.poster.winfo_width() - 19) * im.height // im.width))
                    image = ImageTk.PhotoImage(im)

                    self.posters.append(image)
            elif k == 'relates':
                for url in v:
                    self.urls.insert(END, url['relateurl'])
            else:
                if k == 'mt10id':
                    self.place_id = v
                self.information.insert(END, k + ' : ' + str(v))

        loc = 0
        for poster in self.posters:
            self.poster.create_image(0, loc, anchor=NW, image=poster)
            self.poster.image_names = poster
            loc += (self.poster.winfo_width() - 19) * poster.height() // poster.width()
        self.poster.config(scrollregion=self.poster.bbox(ALL))

    def showPlaceInfo(self):
        if self.place_id:
            place_info_frame = Toplevel()
            place_info_frame.geometry("800x700")
            place_info_frame.title("공연 장소 정보")

            place_info = PlaceInfoFrame(place_info_frame)
            place_info.pack(side=LEFT, fill=BOTH, expand=True)
            # place_info.setInfo(self.place_id)
            place_info.setInfo('FC001247')  # 테스트


class PlaceInfoFrame(InfoFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.status = True  # True : 공연 장소 정보, False : 편의 시설 정보

        self.toggle_button = Button(self.sub_frame1, command=self.toggleInfo)
        self.toggle_button.grid(row=0, column=2, sticky="nsew")

    def getInfo(self, id):
        fetcher = xmlRead()

        self.data = fetcher.fetch_and_parse_place_data(id)[0]

    def setInfo(self, id):
        self.getInfo(id)

        for k, v in self.data.items():
            if k not in Facilities:
                if k == 'la':
                    self.latitutde = v
                elif k == 'lo':
                    self.longitude = v
                if k == 'mt13s':
                    for mt13d in v:
                        for mt13k, mt13v in mt13d.items():
                            self.information.insert(END, mt13k + ' : ' + mt13v)
                else:
                    self.information.insert(END, k + ' : ' + str(v))

        map_osm = folium.Map(location=[self.latitutde, self.longitude], zoom_start=10)
        folium.Marker([self.latitutde, self.longitude]).add_to(map_osm)
        map_osm.save('osm.html')
        self.save_map_as_image('osm.html', 'osm.png')
        map_image = Image.open('osm.png')
        map_photo = ImageTk.PhotoImage(map_image)

        self.map = Canvas(self.sub_frame3)
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

    def toggleInfo(self):
        self.information.delete(0, END)

        self.status = not self.status

        for k, v in self.data.items():
            if self.status:
                if k not in Facilities:
                    if k == 'mt13s':
                        for mt13d in v:
                            for mt13k, mt13v in mt13d.items():
                                self.information.insert(END, mt13k + ' : ' + mt13v)
                    else:
                        self.information.insert(END, k + ' : ' + str(v))
            else:
                if k in Facilities:
                    self.information.insert(END, k + ' : ' + str(v))
