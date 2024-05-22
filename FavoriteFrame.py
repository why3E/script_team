from tkinter import *
from Calender import Calender


class FavoriteFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.year = None
        self.month = None
        self.day = None

        self.sub_frame1 = Frame(self, bg='dim gray')
        self.sub_frame1.pack(side=LEFT, fill=BOTH)

        self.sub_frame_top = Frame(self.sub_frame1, bg="orange")
        self.sub_frame_top.pack(side=TOP, anchor=N, fill=X)

        self.sub_frame2 = Frame(self, bg='light blue')
        self.sub_frame2.pack(side=LEFT, fill=BOTH, expand=True)

        self.from_calender = Calender(self.sub_frame_top)
        self.to_calender = Calender(self.sub_frame_top)

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

    def hide(self):
        self.pack_forget()
