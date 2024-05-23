from tkinter import *
from Calender import Calender
from xmlRead import xmlRead
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk


class SearchListFrame(Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)

        self.page = 1

        super().grid_rowconfigure(0, weight=1)
        super().grid_rowconfigure(1, weight=9)
        super().grid_columnconfigure(0, weight=1)

        self.top_frame = Frame(self, bg='red')
        self.top_frame.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame = Frame(self, bg='green')
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.setTop()
        self.setBottom()

    def setTop(self):
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)

        self.top_frame_left = Frame(self.top_frame, bg='red')
        self.top_frame_left.propagate(False)
        self.top_frame_left.grid(row=0, column=0, sticky="nsew")

        self.top_frame_right = Frame(self.top_frame, bg='blue')
        self.top_frame_right.propagate(False)
        self.top_frame_right.grid(row=0, column=1, sticky="nsew")

        self.from_calender = Calender(self.top_frame_left)
        self.to_calender = Calender(self.top_frame_right)

        self.top_frame_right_end = Frame(self.top_frame, bg='black')
        self.top_frame_right.propagate(False)
        self.top_frame_right_end.grid(row=0, column=2, sticky="nsew")

        self.searchButton = Button(self.top_frame_right_end, text="검색", command=self.searchDate)
        self.searchButton.pack(side=LEFT)

    def searchDate(self):

        stdate = f"{self.from_calender.year}{self.from_calender.month:02}{self.from_calender.day:02}"
        eddate = f"{self.to_calender.year}{self.to_calender.month:02}{self.to_calender.day:02}"
        print(stdate)
        print(eddate)

        data = xmlRead()
        dataList = data.fetch_and_parse_show_data(stdate, eddate, 10, 1)

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

            # 새로운 데이터로 라벨 생성
        label_list = ['poster', 'prfnm', 'genrenm', 'fcltynm', 'prfstate']
        for row in range(len(dataList)):
            for col in range(5):
                if col == 0:
                    url = dataList[row][label_list[col]]
                    with urllib.request.urlopen(url) as u:
                        raw_data = u.read()

                    im = Image.open(BytesIO(raw_data))
                    im = im.resize((100, 100))  # 이미지 크기를 조절
                    image = ImageTk.PhotoImage(im)
                    label = Label(self.scrollable_frame, image=image, height=100, width=100)
                    label.image = image  # 이미지에 대한 참조 유지를 위해 속성에 할당
                    label.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                else:
                    label = Label(self.scrollable_frame, text=dataList[row][label_list[col]], font=("Arial bold", 10),
                                  bg="white", fg="black", width=14, height=7, wraplength=100)
                    label.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

        print(dataList)

    def setBottom(self):
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(1, weight=11)
        self.bottom_frame.grid_rowconfigure(2, weight=1)

        self.bottom_frame_first = Frame(self.bottom_frame, bg='gray')
        self.bottom_frame_first.propagate(False)
        self.bottom_frame_first.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame_second = Frame(self.bottom_frame)
        self.bottom_frame_second.propagate(False)
        self.bottom_frame_second.grid(row=1, column=0, sticky="nsew")

        self.bottom_frame_third = Frame(self.bottom_frame, bg='black')
        self.bottom_frame_third.propagate(False)
        self.bottom_frame_third.grid(row=2, column=0, sticky="nsew")
        self.setDataValue()
        self.setDataLog()

    def setDataValue(self):
        for i in range(5):
            self.bottom_frame_first.grid_columnconfigure(i, weight=1)
        self.bottom_frame_first.grid_rowconfigure(0, weight=1)

        self.frames = []  # 각 열의 프레임을 저장할 리스트
        for col in range(5):
            frame = Frame(self.bottom_frame_first)
            frame.propagate(False)
            frame.grid(row=0, column=col, sticky="nsew")
            frame.grid_columnconfigure(0, weight=2)  # 라벨이 들어갈 곳의 column
            frame.grid_columnconfigure(1, weight=1)  # 버튼이 들어갈 곳의 column
            frame.grid_rowconfigure(0, weight=1)
            self.frames.append(frame)
        label_texts = ["포스터", "공연제목", "장르", "공연장소", "공연유무"]
        for col in range(5):
            left_frame = Frame(self.frames[col], bg="red")
            left_frame.propagate(False)
            left_frame.grid(row=0, column=0, sticky="nsew")

            # 왼쪽 프레임에 라벨 추가
            label_text = label_texts[col]  # 라벨의 텍스트를 설정합니다.
            label = Label(left_frame, text=label_text, bg="white", fg="black",
                          font=("Arial bold", 10, "bold"))  # 라벨을 생성합니다.
            label.pack(expand=True, fill="both", padx=5, pady=5)

            right_frame = Frame(self.frames[col], bg="white")
            right_frame.propagate(False)
            right_frame.grid(row=0, column=1, sticky="nsew")

            # 오른쪽 프레임에 버튼 추가
            button = Button(right_frame, text="정렬", bg="white", fg="black")  # 버튼을 생성합니다.
            button.pack(expand=True, fill="both", padx=5, pady=5)  # 버튼을 오른쪽 프레임에 패킹합니다.

    def setDataLog(self):
        # 캔버스 생성
        self.bottom_frame_second.grid_columnconfigure(0, weight=40)  # 캔버스의 열을 확장
        self.bottom_frame_second.grid_columnconfigure(1, weight=1)  # 스크롤바의 열을 고정
        self.bottom_frame_second.grid_rowconfigure(0, weight=1)  # 캔버스의 열을 확장

        self.bottom_frame_second_left = Frame(self.bottom_frame_second)
        self.bottom_frame_second_left.propagate(False)
        self.bottom_frame_second_left.grid(row=0, column=0, sticky="nsew")

        self.canvas = Canvas(self.bottom_frame_second_left)
        self.canvas.pack(side=LEFT, fill='both', expand=True)

        self.bottom_frame_second_right = Frame(self.bottom_frame_second)
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
        for row in range(10):
            for col in range(5):
                label = Label(self.scrollable_frame, text=f"", bg="white", fg="black",
                              font=("Arial", 10), width=14, height=6)
                label.grid(row=row, column=col, padx=1, pady=1)

        # 캔버스의 크기가 변경될 때 스크롤 영역을 적절하게 조정
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class ShowSearchFrame(SearchListFrame):
    def __init__(self, parent):
        super().__init__(parent)