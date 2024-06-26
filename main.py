from tkinter import *
from SearchFrame import SearchFrame
from FavoriteFrame import FavoriteFrame
from GraphFrame import GraphFrame
from telegram import Telegram
import os
import sys


class MainGUI:
    def __init__(self):
        self.window_width = 1450
        self.window_height = 700

        self.window = Tk()
        self.window.title("공연 보러 가자")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.geometry(f"{self.window_width}x{self.window_height}")

        self.frame = Frame(self.window, bg='white')
        self.frame.pack(side=LEFT, fill=Y)

        self.menu = Frame(self.frame)
        self.menu.pack(side=LEFT, fill=Y)
        self.menu.grid_rowconfigure(0, weight=1)
        self.menu.grid_rowconfigure(1, weight=1)
        self.menu.grid_rowconfigure(2, weight=1)
        self.menu.grid_columnconfigure(0, weight=1)

        self.search_frame = SearchFrame(self.window, self)
        self.favorite_frame = FavoriteFrame(self.window, self)
        self.graph_frame = GraphFrame(self.window, self)

        self.button_image_size = 2
        self.image1 = PhotoImage(file="image/search.png").subsample(self.button_image_size, self.button_image_size)
        self.image2 = PhotoImage(file="image/star.png").subsample(self.button_image_size, self.button_image_size)
        self.image3 = PhotoImage(file="image/graph.png").subsample(self.button_image_size, self.button_image_size)

        # 버튼과 라벨 생성 함수 호출
        self.create_button_with_label(self.menu, self.image1, "검색", 0, self.show_search_frame)
        self.create_button_with_label(self.menu, self.image2, "즐겨찾기", 1, self.show_favorite_frame)
        self.create_button_with_label(self.menu, self.image3, "통계", 2, self.show_graph_frame)

        self.current_frame = self.graph_frame  # 임시, 타이틀 화면 추가 시 해당 프레임으로 설정
        self.show_search_frame()  # 초기 화면을 검색 프레임으로 설정

        Telegram()

        self.window.mainloop()

    def on_closing(self):
        if not self.search_frame.sub_frame2.favorites:
            os.remove('favorites.txt')
        sys.exit(0)

    def create_button_with_label(self, parent, image, text, row, command):
        frame = Frame(parent)
        frame.grid(row=row, column=0, padx=45, pady=self.window_height / 30)

        button = Button(frame, image=image, compound=TOP, width=150, height=150, command=command, bg='gray')
        button.pack()

        label = Label(frame, text=text, font=("Arial", 12), compound=TOP)
        label.pack()

    def show_search_frame(self):
        self.show_frame(self.search_frame)

    def show_favorite_frame(self):
        self.show_frame(self.favorite_frame)

    def show_graph_frame(self):
        self.show_frame(self.graph_frame)

    def show_frame(self, frame):
        if (self.current_frame == frame):
            return

        self.current_frame.hide()  # 현재 프레임 숨기기

        self.current_frame = frame
        self.current_frame.show()


MainGUI()
