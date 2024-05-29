from tkinter import *
from Calender import Calender
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
from functools import partial
import pickle

# 파일 경로 설정

image_size = 105


class SearchListFrame(Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)

        self.type = False

        self.main_frame = main_frame
        self.toggleType = True
        self.page = 1
        self.label_list = ['poster', 'prfnm', 'genrenm', 'fcltynm', 'prfstate']
        self.label_state_list = ['fcltynm', 'adres']
        self.dataList = []

        super().grid_rowconfigure(0, weight=10)
        super().grid_columnconfigure(0, weight=1)


        self.bottom_frame = Frame(self, bg='orange')
        self.bottom_frame.grid(row=0, column=0, sticky="nsew")

        file_path = 'favorites.txt'

        # 파일에서 데이터 불러오기
        with open(file_path, 'rb') as file:
            self.favorites_dict = pickle.load(file)

        self.filtered_dict = self.filter_dict(self.favorites_dict)
        # 불러온 데이터 출력

        self.setBottom()

        self.checkDict()

    def checkDict(self):
        file_path = 'favorites.txt'
        # 파일에서 데이터 불러오기
        with open(file_path, 'rb') as file:
            self.favorites_dict = pickle.load(file)
        self.filtered_dict = self.filter_dict(self.favorites_dict)

    def searchData(self, Dict):

        if self.toggleType:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
        else:
            for widget in self.scrollable_frame2.winfo_children():
                widget.destroy()

        # 새로운 데이터로 라벨 생성
        for row, (k, v) in enumerate(Dict.items()):
            if self.toggleType:
                # self.label_list를 사용하여 'PF'로 시작하는 항목들 처리
                for col, label_key in enumerate(self.label_list):
                    if col == 0 and 'poster' in v:
                        url = v['poster']
                        with urllib.request.urlopen(url) as u:
                            raw_data = u.read()

                        im = Image.open(BytesIO(raw_data))
                        im = im.resize((image_size, image_size))  # 이미지 크기를 조절
                        image = ImageTk.PhotoImage(im)
                        label = Label(self.scrollable_frame, image=image)
                        label.image = image  # 이미지에 대한 참조 유지를 위해 속성에 할당

                        label.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                        label.bind("<Button-1>", partial(self.searchID, k))
                    else:
                        label_text = v.get(label_key, 'N/A')
                        label = Label(self.scrollable_frame, text=label_text,
                                      font=("Arial bold", 10), bg="white", fg="black", width=14, height=7,
                                      wraplength=100)
                        label.grid(row=row, column=col, pady=1, sticky="nsew")
            else:
                # self.label_state_list를 사용하여 'FC'로 시작하는 항목들 처리
                for col, label_key in enumerate(self.label_state_list):
                    label_text = v.get(label_key, 'N/A')
                    label = Label(self.scrollable_frame2, text=label_text,
                                  font=("Arial bold", 10), bg="white", fg="black", width=36, height=7, wraplength=200)
                    label.grid(row=row, column=col, pady=1, sticky="nsew")
                    if col == 0:
                        label.bind("<Button-1>", partial(self.searchID_state, k))

    def searchID(self, ID, event=None):
        self.main_frame.sub_frame2.setInfo(ID)

    def searchID_state(self, ID, event=None):
        self.main_frame.sub_frame3.setInfo(ID)

    def filter_dict(self, data):
        if self.toggleType:
            # 'PF'로 시작하는 항목들만
            return {k: v for k, v in data.items() if k.startswith('PF')}
        else:
            # 'FC'로 시작하는 항목들만
            return {k: v for k, v in data.items() if k.startswith('FC')}

    def sort_by_prfnm(self, tag, order):
        reverse_order = (order == "down")
        # 정렬된 튜플 리스트 생성
        sorted_items = sorted(self.filtered_dict.items(), key=lambda x: x[1][tag], reverse=reverse_order)
        # 정렬된 튜플 리스트를 다시 딕셔너리로 변환
        self.filtered_dict = dict(sorted_items)
        # UI 갱신
        self.searchData(self.filtered_dict)

    def setBottom(self):
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(1, weight=11)
        self.bottom_frame.grid_rowconfigure(2, weight=1)

        self.bottom_frame_first1 = Frame(self.bottom_frame, bg='orange')
        self.bottom_frame_first1.propagate(False)

        self.bottom_frame_first2 = Frame(self.bottom_frame, bg='orange')
        self.bottom_frame_first2.propagate(False)

        self.bottom_frame_first = self.bottom_frame_first1
        self.bottom_frame_first.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame_second1 = Frame(self.bottom_frame)
        self.bottom_frame_second1.propagate(False)
        self.bottom_frame_second2 = Frame(self.bottom_frame)
        self.bottom_frame_second2.propagate(False)

        self.bottom_frame_second = self.bottom_frame_second1
        self.bottom_frame_second.grid(row=1, column=0, sticky="nsew")

        self.bottom_frame_third = Frame(self.bottom_frame, bg='orange')
        self.bottom_frame_third.propagate(False)
        self.bottom_frame_third.grid(row=2, column=0, sticky="nsew")

        self.setDataValue()
        self.setDataLog()

        self.setDataValue2()
        self.setDataLog2()

        self.setPage()

    def setPage(self):
        self.bottom_frame_third.columnconfigure([0, 1, 2], weight=1)
        self.bottom_frame_third.grid_rowconfigure(0, weight=1)

        bottom_frame_third_left = Frame(self.bottom_frame_third, bg='orange')
        bottom_frame_third_left.propagate(False)
        bottom_frame_third_left.grid(row=0, column=0, sticky="nsew")
        button_left = Button(bottom_frame_third_left, text="Left Button",
                             command=lambda: self.setPageButton("left"))
        button_left.pack()

        # Middle frame with an entry box
        self.bottom_frame_third_mid = Frame(self.bottom_frame_third, bg='orange')
        self.bottom_frame_third_mid.propagate(False)
        self.bottom_frame_third_mid.grid(row=0, column=1, sticky="nsew")
        self.entry_mid = Entry(self.bottom_frame_third_mid, width=2)
        self.entry_mid.pack()
        self.entry_mid.insert(0, self.page)
        self.entry_mid.bind('<Return>', self.save_page)

        # Right frame with a button
        bottom_frame_third_right = Frame(self.bottom_frame_third, bg='orange')
        bottom_frame_third_right.propagate(False)
        bottom_frame_third_right.grid(row=0, column=2, sticky="nsew")

        button_right = Button(bottom_frame_third_right, text="Left Button", command=lambda: self.setPageButton("left"))
        button_right.pack()

        button_right_bottom = Button(bottom_frame_third_right, text="토글", command=lambda: self.toggle_sub_frames())
        button_right_bottom.pack(side="right")

    def setDataValue(self):
        for i in range(5):
            self.bottom_frame_first1.grid_columnconfigure(i, weight=1)
        self.bottom_frame_first1.grid_rowconfigure(0, weight=1)

        self.frames = []  # 각 열의 프레임을 저장할 리스트
        for col in range(5):
            frame = Frame(self.bottom_frame_first1)
            frame.propagate(False)
            frame.grid(row=0, column=col, sticky="nsew")
            frame.grid_columnconfigure(0, weight=2)  # 라벨이 들어갈 곳의 column
            frame.grid_columnconfigure(1, weight=1)  # 버튼이 들어갈 곳의 column
            frame.grid_rowconfigure(0, weight=1)
            self.frames.append(frame)

        label_texts = ["포스터", "공연제목", "장르", "공연장소", "공연유무"]
        for col in range(5):
            left_frame = Frame(self.frames[col], bg="orange")
            left_frame.propagate(False)
            left_frame.grid(row=0, column=0, sticky="nsew")

            # 왼쪽 프레임에 라벨 추가
            label_text = label_texts[col]  # 라벨의 텍스트를 설정합니다.
            label = Label(left_frame, text=label_text, bg="white", fg="black",
                          font=("Arial bold", 10, "bold"))  # 라벨을 생성합니다.
            label.pack(expand=True, fill="both", padx=5, pady=5)

            right_frame = Frame(self.frames[col], bg="orange")
            right_frame.propagate(False)
            right_frame.grid(row=0, column=1, sticky="nsew")

            right_frame.grid_rowconfigure(0, weight=1)  # 라벨이 들어갈 곳의 column
            right_frame.grid_rowconfigure(1, weight=1)  # 버튼이 들어갈 곳의 column
            right_frame.grid_columnconfigure(0, weight=1)

            right_frame_up = Frame(right_frame,bg='orange')
            right_frame_up.propagate(False)
            right_frame_up.grid(row=0, column=0, sticky="nsew")

            right_frame_down = Frame(right_frame,bg='orange')
            right_frame_down.propagate(False)
            right_frame_down.grid(row=1, column=0, sticky="nsew")

            up_button = Button(right_frame_up, text="▲", bg="white", fg="black",
                               command=partial(self.sort_by_prfnm, self.label_list[col],
                                               "up"))  # partial을 사용하여 고유한 값을 전달합니다.
            up_button.pack(expand=True, fill="both", padx=5, pady=5)

            down_button = Button(right_frame_down, text="▼", bg="white", fg="black",
                                 command=partial(self.sort_by_prfnm, self.label_list[col],
                                                 "down"))  # partial을 사용하여 고유한 값을 전달합니다.
            down_button.pack(expand=True, fill="both", padx=5, pady=5)

    def setDataValue2(self):
        for i in range(2):
            self.bottom_frame_first2.grid_columnconfigure(i, weight=1)
        self.bottom_frame_first2.grid_rowconfigure(0, weight=1)

        self.frames_state = []  # 각 열의 프레임을 저장할 리스트

        for col in range(2):
            frame = Frame(self.bottom_frame_first2)
            frame.propagate(False)
            frame.grid(row=0, column=col, sticky="nsew")
            frame.grid_columnconfigure(0, weight=2)  # 라벨이 들어갈 곳의 column
            frame.grid_columnconfigure(1, weight=1)  # 버튼이 들어갈 곳의 column
            frame.grid_rowconfigure(0, weight=1)
            self.frames_state.append(frame)

        label_texts = ["공연시설명", "지역(시,도)", "지역(구,군)"]
        for col in range(2):
            left_frame = Frame(self.frames_state[col], bg="orange")
            left_frame.propagate(False)
            left_frame.grid(row=0, column=0, sticky="nsew")

            # 왼쪽 프레임에 라벨 추가
            label_text = label_texts[col]  # 라벨의 텍스트를 설정합니다.
            label = Label(left_frame, text=label_text, bg="white", fg="black",
                          font=("Arial bold", 10, "bold"))  # 라벨을 생성합니다.
            label.pack(expand=True, fill="both", padx=5, pady=5)

            right_frame = Frame(self.frames_state[col], bg="orange")
            right_frame.propagate(False)
            right_frame.grid(row=0, column=1, sticky="nsew")

            right_frame.grid_rowconfigure(0, weight=1)  # 라벨이 들어갈 곳의 column
            right_frame.grid_rowconfigure(1, weight=1)  # 버튼이 들어갈 곳의 column
            right_frame.grid_columnconfigure(0, weight=1)

            right_frame_up = Frame(right_frame,bg='orange')
            right_frame_up.propagate(False)
            right_frame_up.grid(row=0, column=0, sticky="nsew")

            right_frame_down = Frame(right_frame,bg='orange')
            right_frame_down.propagate(False)
            right_frame_down.grid(row=1, column=0, sticky="nsew")

            up_button = Button(right_frame_up, text="▲", bg="white", fg="black",
                               command=partial(self.sort_by_prfnm, self.label_state_list[col],
                                               "up"))  # partial을 사용하여 고유한 값을 전달합니다.
            up_button.pack(expand=True, fill="both", padx=5, pady=5)

            down_button = Button(right_frame_down, text="▼", bg="white", fg="black",
                                 command=partial(self.sort_by_prfnm, self.label_state_list[col],
                                                 "down"))  # partial을 사용하여 고유한 값을 전달합니다.
            down_button.pack(expand=True, fill="both", padx=5, pady=5)

    def setDataLog(self):
        # 캔버스 생성
        self.bottom_frame_second1.grid_columnconfigure(0, weight=40)  # 캔버스의 열을 확장
        self.bottom_frame_second1.grid_columnconfigure(1, weight=1)  # 스크롤바의 열을 고정
        self.bottom_frame_second1.grid_rowconfigure(0, weight=1)  # 캔버스의 열을 확장

        self.bottom_frame_second_left = Frame(self.bottom_frame_second1,bg='orange')
        self.bottom_frame_second_left.propagate(False)
        self.bottom_frame_second_left.grid(row=0, column=0, sticky="nsew")

        self.canvas = Canvas(self.bottom_frame_second_left)
        self.canvas.pack(side=LEFT, fill='both', expand=True)

        self.bottom_frame_second_right = Frame(self.bottom_frame_second1)
        self.bottom_frame_second_right.propagate(False)
        self.bottom_frame_second_right.grid(row=0, column=1, sticky="nsew")

        # 수직 스크롤바 생성 및 캔버스와 연결
        vscrollbar = Scrollbar(self.bottom_frame_second_right, orient='vertical', command=self.canvas.yview)
        vscrollbar.pack(side=LEFT, fill='both')

        self.canvas.configure(yscrollcommand=vscrollbar.set)

        # 캔버스 내부에 위젯을 담을 프레임 생성
        self.scrollable_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # 프레임 내에 라벨 배치
        self.searchData(self.filtered_dict)

        # 캔버스의 크기가 변경될 때 스크롤 영역을 적절하게 조정
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

    def setDataLog2(self):
        # 캔버스 생성
        self.bottom_frame_second2.grid_columnconfigure(0, weight=40)  # 캔버스의 열을 확장
        self.bottom_frame_second2.grid_columnconfigure(1, weight=1)  # 스크롤바의 열을 고정
        self.bottom_frame_second2.grid_rowconfigure(0, weight=1)  # 캔버스의 열을 확장

        self.bottom_frame_second_left2 = Frame(self.bottom_frame_second2)
        self.bottom_frame_second_left2.propagate(False)
        self.bottom_frame_second_left2.grid(row=0, column=0, sticky="nsew")

        self.canvas2 = Canvas(self.bottom_frame_second_left2)
        self.canvas2.pack(side=LEFT, fill='both', expand=True)

        self.bottom_frame_second_right2 = Frame(self.bottom_frame_second2)
        self.bottom_frame_second_right2.propagate(False)
        self.bottom_frame_second_right2.grid(row=0, column=1, sticky="nsew")

        # 수직 스크롤바 생성 및 캔버스와 연결
        vscrollbar = Scrollbar(self.bottom_frame_second_right2, orient='vertical', command=self.canvas2.yview)
        vscrollbar.pack(side=LEFT, fill='both')

        self.canvas2.configure(yscrollcommand=vscrollbar.set)

        # 캔버스 내부에 위젯을 담을 프레임 생성
        self.scrollable_frame2 = Frame(self.canvas2)
        self.canvas2.create_window((0, 0), window=self.scrollable_frame2, anchor="nw")

        # 프레임 내에 라벨 배치
        self.searchData(self.filtered_dict)

        # 캔버스의 크기가 변경될 때 스크롤 영역을 적절하게 조정
        self.scrollable_frame2.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save_page(self, event=None):
        self.page = int(self.entry_mid.get())
        self.searchData(self.filtered_dict)

    def setPageButton(self, button):
        if button == "right":
            self.page += 1
            self.searchData(self.filtered_dict)
            self.entry_mid.delete(0, "end")
            self.entry_mid.insert(0, self.page)
        elif button == "left":
            if self.page > 1:
                self.page -= 1
                self.searchData(self.filtered_dict)
                self.entry_mid.delete(0, "end")
                self.entry_mid.insert(0, self.page)

    def toggle_sub_frames(self):
        # 현재 표시된 서브 프레임을 숨깁니다.
        if self.bottom_frame_first == self.bottom_frame_first1:
            type_frame = False
            self.main_frame.sub_frame2.grid_forget()
            self.main_frame.sub_frame3.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        else:
            type_frame = True
            self.main_frame.sub_frame3.grid_forget()
            self.main_frame.sub_frame2.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        self.bottom_frame_first.grid_forget()
        self.bottom_frame_second.grid_forget()

        # 서브 프레임을 토글합니다.
        if type_frame:
            self.toggleType = True
            self.bottom_frame_first = self.bottom_frame_first1
            self.bottom_frame_second = self.bottom_frame_second1
        else:
            self.toggleType = False
            self.bottom_frame_first = self.bottom_frame_first2
            self.bottom_frame_second = self.bottom_frame_second2

        self.bottom_frame_first.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame_second.grid(row=1, column=0, sticky="nsew")

        self.checkDict()
        self.searchData(self.filtered_dict)


class ShowFavoriteSearchFrame(SearchListFrame):
    def __init__(self, parent):
        super().__init__(parent)
