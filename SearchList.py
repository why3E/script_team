from tkinter import *
from Calender import Calender


class SearchListFrame(Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)
        super().grid_rowconfigure(0, weight=1)
        super().grid_rowconfigure(1, weight=9)
        super().grid_columnconfigure(0, weight=1)

        self.top_frame = Frame(self, bg='red')
        self.top_frame.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame = Frame(self, bg='green')
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)

        self.top_frame_left = Frame(self.top_frame, bg='red')
        self.top_frame_left.grid(row=0, column=0, sticky="nsew")

        self.top_frame_right = Frame(self.top_frame, bg='blue')
        self.top_frame_right.grid(row=0, column=1, sticky="nsew")


        self.from_calender = Calender(self.top_frame_left)
        self.to_calender = Calender(self.top_frame_right)


        self.top_frame_right_end = Frame(self.top_frame, bg='black')
        self.top_frame_right_end.grid(row=0, column=2, sticky="nsew")


class ShowSearchFrame(SearchListFrame):
    def __init__(self, parent):
        super().__init__(parent)
