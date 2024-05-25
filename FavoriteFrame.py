from tkinter import *
from FavoriteSearchFrame import *
from SearchList import *
from InfoFrame import *

class FavoriteFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.year = None
        self.month = None
        self.day = None
        self.sub_frame_sub1 = None
        self.sub_frame_sub2 = None
        self.sub_frame2 = None
        self.current_sub_frame = None  # 현재 표시되는 서브 프레임을 추적하는 변수
        self.sub_frame1_visible = False  # sub_frame_sub1이 보이는지 여부를 추적하는 변수

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sub_frames()

    def create_sub_frames(self):
        # 첫 번째 서브 프레임
        self.sub_frame_sub1 = ShowFavoriteSearchFrame(self)
        self.sub_frame_sub1.propagate(False)

        self.sub_frame_sub2 = ShowSearchFrame(self)
        self.sub_frame_sub2.propagate(False)

        # 두 번째 서브 프레임
        self.sub_frame2 = ShowInfoFrame(self)

        # 초기에는 sub_frame_sub1을 표시합니다.
        self.current_sub_frame = self.sub_frame_sub1
        self.current_sub_frame.grid(row=0, column=0, sticky="nsew")

    def toggle_sub_frames(self):
        # 현재 표시된 서브 프레임을 숨깁니다.
        self.current_sub_frame.grid_forget()

        # 서브 프레임을 토글합니다.
        if self.sub_frame1_visible:
            self.sub_frame_sub2.grid(row=0, column=0, sticky="nsew")
            self.current_sub_frame = self.sub_frame_sub2
        else:
            self.sub_frame_sub1.grid(row=0, column=0, sticky="nsew")
            self.current_sub_frame = self.sub_frame_sub1

        # 토글 상태를 업데이트합니다.
        self.sub_frame1_visible = not self.sub_frame1_visible

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

    def hide(self):
        self.pack_forget()


# 버튼을 누를 때 toggle_sub_frames 함수를 호출하도록 연결합니다.
# 예를 들어, Toggle 버튼을 만들고 이 버튼의 명령에 toggle_sub_frames 함수를 연결할 수 있습니다.
