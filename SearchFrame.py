from tkinter import *
from InfoFrame import *
from xmlRead import *
from SearchList import *

class SearchFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)

        self.main_frame = main_frame
        self.year = None
        self.month = None
        self.day = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 첫 번째 서브 프레임
        self.sub_frame1 = ShowSearchFrame(self)
        self.sub_frame1.grid(row=0, column=0, sticky="nsew")

        # 두 번째 서브 프레임
        self.sub_frame2 = ShowInfoFrame(self)
        self.sub_frame2.grid(row=0, column=1, sticky="nsew")



    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

    def hide(self):
        self.pack_forget()

