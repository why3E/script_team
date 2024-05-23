from tkinter import *
from InfoFrame import *
from Calender import Calender
from xmlRead import *


class SearchFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.year = None
        self.month = None
        self.day = None

        self.sub_frame1 = Frame(self, bg='pink')
        self.sub_frame1.grid(row=0, column=0, sticky='nsew')

        self.sub_frame2 = ShowInfoFrame(self)
        self.sub_frame2.grid(row=0, column=1, sticky='nsew')

        self.sub_frame_top = Frame(self.sub_frame1, bg="orange")
        self.sub_frame_top.pack(side=TOP, anchor=N, fill=X)
        self.from_calender = Calender(self.sub_frame_top)
        self.to_calender = Calender(self.sub_frame_top)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

    def hide(self):
        self.pack_forget()

