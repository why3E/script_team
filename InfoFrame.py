from tkinter import *
from xmlRead import xmlRead
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
import webbrowser
from Map import Map

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
        self.informations = []
        self.information = Canvas(self.sub_frame2, bg='white')
        self.information.grid(row=0, column=0, sticky="nsew")
        self.sub_frame2.grid_rowconfigure(0, weight=1)
        self.sub_frame2.grid_columnconfigure(0, weight=2)

        self.information_xscroll = Scrollbar(self.information, orient='horizontal', command=self.information.xview)
        self.information_xscroll.pack(side="bottom", fill=X)
        self.information_yscroll = Scrollbar(self.information, orient='vertical', command=self.information.yview)
        self.information_yscroll.pack(side="right", fill=Y)
        self.information.configure(xscrollcommand=self.information_xscroll.set,
                                   yscrollcommand=self.information_yscroll.set)

        self.sub_frame3 = Frame(self, bg='white')
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

        self.posters = []
        self.poster = Canvas(self.sub_frame2)
        self.poster.grid_propagate(False)
        self.poster.grid(row=0, column=1, sticky="nsew")

        self.poster_yscroll = Scrollbar(self.poster, orient='vertical', command=self.poster.yview)
        self.poster_yscroll.pack(side="right", fill=Y)
        self.poster.configure(yscrollcommand=self.poster_yscroll.set)

        self.sub_frame2.grid_columnconfigure(1, weight=1)

        self.urls = []

    def getInfo(self, id):
        fetcher = xmlRead()

        self.data = fetcher.fetch_and_parse_show_detail_data(id)[0]

    def setInfo(self, id):
        self.place_id = None
        self.informations.clear()
        self.information.delete("all")
        self.posters.clear()
        self.poster.delete("all")
        self.urls.clear()

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
                    self.urls.append(
                        (Label(self.sub_frame3, text=url['relatenm']),
                         Label(self.sub_frame3, text=url['relateurl'], fg='blue')))
            else:
                if k == 'mt10id':
                    self.place_id = v
                self.informations.append(k + ' : ' + str(v))

        for i in range(len(self.informations)):
            self.information.create_text(5, 25 * (i + 1), anchor=W, text=self.informations[i],
                                         font=('arial', 10, 'bold'))
        self.information.config(scrollregion=self.information.bbox(ALL))

        loc = 0
        for p in self.posters:
            self.poster.create_image(0, loc, anchor=NW, image=p)
            self.poster.image_names = p
            loc += (self.poster.winfo_width() - 19) * p.height() // p.width()
        self.poster.config(scrollregion=self.poster.bbox(ALL))

        r = 0
        for t in self.urls:
            t[0].grid(row=r, column=0, padx=2, pady=2, sticky='nsew')
            t[1].grid(row=r, column=1, padx=2, pady=2, sticky='nsew')
            t[1].bind("<Button-1>", self.open_url(t[1].cget('text')))
            self.sub_frame3.grid_rowconfigure(r, weight=1)
            r += 1

    def open_url(self, url):
        def callback(event):
            webbrowser.open_new(url)

        return callback

    def showPlaceInfo(self):
        if self.place_id:
            PlaceInfoFrame(self.place_id)


class PlaceInfoFrame(InfoFrame):
    def __init__(self, id):
        self.place_id = id
        self.status = True  # True : 공연 장소 정보, False : 편의 시설 정보
        self.map = Map()

        place_info_frame = Toplevel()
        place_info_frame.geometry("800x700")
        place_info_frame.title("공연 장소 정보")

        super().__init__(place_info_frame)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.setInfo(self.place_id)

        self.toggle_button = Button(self.sub_frame1, command=self.toggleInfo)
        self.toggle_button.grid(row=0, column=2, sticky="nsew")

    def getInfo(self, id):
        fetcher = xmlRead()

        self.data = fetcher.fetch_and_parse_place_data(id)[0]

    def setInfo(self, id):
        self.informations.clear()
        self.information.delete('all')

        self.getInfo(id)

        for k, v in self.data.items():
            if k == 'la':
                self.latitude = v
                continue
            if k == 'lo':
                self.longitude = v
                continue

            if self.status:
                if k not in Facilities:
                    if k == 'mt13s':
                        for mt13d in v:
                            for mt13k, mt13v in mt13d.items():
                                self.informations.append(mt13k + ' : ' + mt13v)
                    else:
                        self.informations.append(k + ' : ' + v)
            else:
                if k in Facilities:
                    self.informations.append(k + ' : ' + v)

        for i in range(len(self.informations)):
            self.information.create_text(5, 25 * (i + 1), anchor=W, text=self.informations[i],
                                         font=('arial', 10, 'bold'))
        self.information.config(scrollregion=self.information.bbox(ALL))

        if self.map.get_coordinate() != (self.latitude, self.longitude):
            self.map.show_map(self.sub_frame3, self.latitude, self.longitude)

    def toggleInfo(self):
        self.status = not self.status

        self.setInfo(self.place_id)
