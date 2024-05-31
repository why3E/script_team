from tkinter import *
from InfoFrame import ShowInfoFrame
from SearchList import ShowSearchFrame
from xmlRead import *


class SearchFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)

        self.main_frame = main_frame
        self.year = None
        self.month = None
        self.day = None

        self.sub_frame1 = ShowSearchFrame(self)
        self.sub_frame1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.sub_frame2 = ShowInfoFrame(self)
        self.sub_frame2.email_button.configure(bg='orange')
        self.sub_frame2.favorite_button.configure(bg='orange')
        self.sub_frame2.place_button.configure(bg='orange')
        self.sub_frame2.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

    def hide(self):
        self.pack_forget()

