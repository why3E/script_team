from tkinter import *
from FavoriteSearchFrame import ShowFavoriteSearchFrame
from InfoFrame import ShowInfoFrame, PlaceInfoFrame


class FavoriteFrame(Frame):
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
        self.sub_frame1 = ShowFavoriteSearchFrame(self)
        self.sub_frame1.propagate(False)
        self.sub_frame1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # 두 번째 서브 프레임
        self.sub_frame2 = ShowInfoFrame(self)
        self.sub_frame2.propagate(False)
        self.sub_frame2.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        self.sub_frame3 = PlaceInfoFrame(self)
        self.sub_frame3.propagate(False)

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

    def hide(self):
        self.pack_forget()
