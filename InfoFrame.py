from tkinter import *


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
        self.sub_frame2.grid(row=1, column=0, sticky="nsew")
        self.information = Label(self.sub_frame2, bg='yellow')
        self.information.grid(row=0, column=0, sticky="nsew")
        self.sub_frame2.grid_rowconfigure(0, weight=1)
        self.sub_frame2.grid_columnconfigure(0, weight=2)

        self.sub_frame3 = Frame(self, bg='blue')
        self.sub_frame3.grid(row=2, column=0, sticky="nsew")

    def showInfo(self, mt20id):
        pass

    def sendEmail(self):
        pass

    def addRemoveFavorite(self):
        pass

    def addFavorite(self):
        pass

    def removeFavorite(self):
        pass

    def showPlaceInfo(self):
        place_info_frame = Toplevel()
        place_info_frame.geometry("600x700")
        place_info_frame.title("공연 장소 정보")

        place_info = PlaceInfoFrame(place_info_frame)
        place_info.pack(side=LEFT, fill=BOTH, expand=True)


class ShowInfoFrame(InfoFrame):
    def __init__(self, parent):
        super().__init__(parent)

        Button(self.sub_frame1, command=self.showPlaceInfo).grid(row=0, column=2, sticky="nsew")

        self.poster = Label(self.sub_frame2, bg='green')
        self.poster.grid(row=0, column=1, sticky="nsew")
        self.sub_frame2.grid_columnconfigure(1, weight=1)


class PlaceInfoFrame(InfoFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.toggle_button = Button(self.sub_frame1, command=self.toggleInfo)
        self.toggle_button.grid(row=0, column=2, sticky="nsew")

    def toggleInfo(self):
        pass
