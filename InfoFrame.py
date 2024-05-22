from tkinter import *
from xmlRead import xmlRead
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk


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
        self.setInfo()  # 테스트

    def addRemoveFavorite(self):
        pass

    def addFavorite(self):
        pass

    def removeFavorite(self):
        pass


class ShowInfoFrame(InfoFrame):
    def __init__(self, parent):
        super().__init__(parent)

        Button(self.sub_frame1, command=self.showPlaceInfo).grid(row=0, column=2, sticky="nsew")

        self.information_xscroll = Scrollbar(self.information, orient='horizontal', command=self.information.xview)
        self.information_xscroll.pack(side="bottom", fill=X)
        self.information_yscroll = Scrollbar(self.information, orient='vertical', command=self.information.yview)
        self.information_yscroll.pack(side="right", fill=Y)
        self.information.configure(xscrollcommand=self.information_xscroll.set, yscrollcommand=self.information_yscroll.set)

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

        data = fetcher.fetch_and_parse_show_detail_data(id)[0]

        for k, v in data.items():
            if k == 'styurls':
                for url in v:
                    with urllib.request.urlopen(url) as u:
                        raw_data = u.read()
                    im = Image.open(BytesIO(raw_data))
                    im = im.resize((self.poster.winfo_width() - 19, (self.poster.winfo_width() - 19) * im.height // im.width))
                    image = ImageTk.PhotoImage(im)

                    self.posters.append(image)
            elif k == 'relates':
                for url in v:
                    self.urls.insert(END, url['relateurl'])
            else:
                self.information.insert(END, k + ' : ' + str(v))

    def setInfo(self):
        self.posters.clear()
        self.urls.delete(0, END)
        self.information.delete(0, END)

        self.getInfo('PF132236')

        loc = 0
        for poster in self.posters:
            self.poster.create_image(0, loc, anchor=NW, image=poster)
            self.poster.image_names = poster
            loc += (self.poster.winfo_width() - 19) * poster.height() // poster.width()
        self.poster.config(scrollregion=self.poster.bbox(ALL))

    def showPlaceInfo(self):
        place_info_frame = Toplevel()
        place_info_frame.geometry("600x700")
        place_info_frame.title("공연 장소 정보")

        place_info = PlaceInfoFrame(place_info_frame)
        place_info.pack(side=LEFT, fill=BOTH, expand=True)


class PlaceInfoFrame(InfoFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.toggle_button = Button(self.sub_frame1, command=self.toggleInfo)
        self.toggle_button.grid(row=0, column=2, sticky="nsew")

    def getInfo(self, id):
        pass

    def showInfo(self):
        pass

    def toggleInfo(self):
        pass
