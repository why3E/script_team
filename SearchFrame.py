from tkinter import *
from Calender import Calender
from xmlRead import *

class SearchFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.year = None
        self.month = None
        self.day = None

    def create(self):
        self.sub_frame1 = Frame(self, bg='pink')
        self.sub_frame2 = Frame(self, bg='light coral')
        self.label1 = Label(self.sub_frame1, text="서브 프레임 1", font=("Arial", 16))
        self.label2 = Label(self.sub_frame2, text="서브 프레임 2", font=("Arial", 16))

        self.sub_frame1.pack(side=LEFT, fill=BOTH)

        self.sub_frame2.pack(side=LEFT, fill=BOTH, expand=True)

        self.label1.pack(pady=10)
        self.label2.pack(pady=10)

        self.sub_frame_top = Frame(self.sub_frame1, bg="orange")
        self.sub_frame_top.pack(side=TOP, anchor=N, fill=X)

        self.from_calender = Calender(self.sub_frame_top)
        self.to_calender = Calender(self.sub_frame_top)

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

    def hide(self):
        self.pack_forget()
