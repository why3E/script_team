from tkinter import *
from tkinter import messagebox

from Calender import Calender
from xmlRead import xmlRead
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
from functools import partial
import spam

class SearchListFrame(Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)

        self.page = 1
        self.label_list = ['poster', 'prfnm', 'genrenm', 'fcltynm', 'prfstate']
        self.data = xmlRead()
        self.main_frame = main_frame

        super().grid_rowconfigure(0, weight=1)
        super().grid_rowconfigure(1, weight=9)
        super().grid_columnconfigure(0, weight=1)

        self.top_frame = Frame(self, bg='orange')
        self.top_frame.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame = Frame(self, bg='orange')
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.setTop()
        self.setBottom()

    def setTop(self):
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)

        self.top_frame_left = Frame(self.top_frame, bg='dark orange')
        self.top_frame_left.propagate(False)
        self.top_frame_left.grid(row=0, column=0, sticky="nsew")

        self.top_frame_right = Frame(self.top_frame, bg='dark orange')
        self.top_frame_right.propagate(False)
        self.top_frame_right.grid(row=0, column=1, sticky="nsew")

        self.from_calender = Calender(self.top_frame_left)
        self.from_calender.date_selector_frame.place(x=50, y=25)

        self.to_calender = Calender(self.top_frame_right)
        self.to_calender.date_selector_frame.place(x=50, y=25)

        self.top_frame_right_end = Frame(self.top_frame, bg='dark orange')
        self.top_frame_right_end.propagate(False)
        self.top_frame_right_end.grid(row=0, column=2, sticky="nsew")

        self.searchButton = Button(self.top_frame_right_end, text="검색", command=self.searchData)
        self.searchButton.place(x=50, y=25)

    def searchData(self):
        if not self.from_calender.get_date() or not self.to_calender.get_date():
            messagebox.showwarning('알림', '날짜가 선택되지 않았습니다.')
            return

        if self.from_calender.get_date() > self.to_calender.get_date():
            messagebox.showwarning('알림', '종료일은 시작일보다 앞설 수 없습니다.')
            return

        stdate = self.from_calender.get_date()
        eddate = self.to_calender.get_date()

        self.dataList = self.data.fetch_and_parse_show_data(stdate, eddate, 10, self.page)
        self.draw_canvas()


    def draw_canvas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 새로운 데이터로 라벨 생성
        # print(self.dataList)
        Labels = [[None for _ in range(5)] for _ in range(len(self.dataList))]

        for row in range(len(self.dataList)):

            for col in range(5):
                if col == 0:
                    url = self.dataList[row][self.label_list[col]]
                    with urllib.request.urlopen(url) as u:
                        raw_data = u.read()

                    im = Image.open(BytesIO(raw_data))
                    im = im.resize((100, 100))  # 이미지 크기를 조절
                    image = ImageTk.PhotoImage(im)
                    Labels[row][col] = Label(self.scrollable_frame, image=image)
                    Labels[row][col].image = image  # 이미지에 대한 참조 유지를 위해 속성에 할당

                    Labels[row][col].grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

                    Labels[row][col].bind("<Button-1>", partial(self.searchID, self.dataList[row]["mt20id"]))
                else:
                    Labels[row][col] = Label(self.scrollable_frame, text=self.dataList[row][self.label_list[col]],
                                             font=("Arial bold", 10), bg="white", fg="black", width=14, height=7,
                                             wraplength=100)
                    Labels[row][col].grid(row=row, column=col, pady=1, sticky="nsew")

    def searchID(self, ID, event=None):
        self.main_frame.sub_frame2.setInfo(ID)

    def sort_by_prfnm(self, tag, order):
        reverse_order = False
        if order == "down":
            reverse_order = True

        tag_values = [item[tag] for item in self.dataList]

        # 2. 그 값을 정렬한다.
        sorted_tag_values = spam.sort(tag_values, reverse_order)

        # 3. 정렬된 값을 기준으로 원래 리스트를 정렬한다.
        self.dataList = sorted(self.dataList, key=lambda x: sorted_tag_values.index(x[tag]))

        self.draw_canvas()


    def setBottom(self):
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(1, weight=11)
        self.bottom_frame.grid_rowconfigure(2, weight=1)

        self.bottom_frame_first = Frame(self.bottom_frame, bg='orange')
        self.bottom_frame_first.propagate(False)
        self.bottom_frame_first.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame_second = Frame(self.bottom_frame, bg='orange')
        self.bottom_frame_second.propagate(False)
        self.bottom_frame_second.grid(row=1, column=0, sticky="nsew")

        self.bottom_frame_third = Frame(self.bottom_frame, bg='orange')
        self.bottom_frame_third.propagate(False)
        self.bottom_frame_third.grid(row=2, column=0, sticky="nsew")
        self.setDataValue()
        self.setDataLog()

        self.setPage()

    def setPage(self):
        self.bottom_frame_third.columnconfigure([0, 1, 2], weight=1)
        self.bottom_frame_third.grid_rowconfigure(0, weight=1)

        self.bottom_frame_third_left = Frame(self.bottom_frame_third, bg='orange')
        self.bottom_frame_third_left.propagate(False)
        self.bottom_frame_third_left.grid(row=0, column=0, sticky="nsew")
        button_left = Button(self.bottom_frame_third_left, text="◀",
                             command=lambda: self.setPageButton("left"))
        button_left.pack(side='right')

        # Middle frame with an entry box
        self.bottom_frame_third_mid = Frame(self.bottom_frame_third, bg='orange')
        self.bottom_frame_third_mid.propagate(False)
        self.bottom_frame_third_mid.grid(row=0, column=1, sticky="nsew")
        self.entry_mid = Entry(self.bottom_frame_third_mid, width=2)
        self.entry_mid.place(x=90, y=15)
        self.entry_mid.insert(0, self.page)
        self.entry_mid.bind('<Return>', self.save_page)

        # Right frame with a button
        self.bottom_frame_third_right = Frame(self.bottom_frame_third, bg='orange')
        self.bottom_frame_third_right.propagate(False)
        self.bottom_frame_third_right.grid(row=0, column=2, sticky="nsew")

        button_right = Button(self.bottom_frame_third_right, text="▶",
                              command=lambda: self.setPageButton("right"))
        button_right.pack(side='left')

    def save_page(self, event=None):
        self.page = int(self.entry_mid.get())
        self.searchData()

    def setPageButton(self, button):
        if button == "right":
            self.page += 1
            self.searchData()
            self.entry_mid.delete(0, "end")
            self.entry_mid.insert(0, self.page)
        elif button == "left":
            if self.page > 1:
                self.page -= 1
                self.searchData()
                self.entry_mid.delete(0, "end")
                self.entry_mid.insert(0, self.page)

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

            right_frame_up = Frame(right_frame, bg="orange")
            right_frame_up.propagate(False)
            right_frame_up.grid(row=0, column=0, sticky="nsew")

            right_frame_down = Frame(right_frame, bg="orange")
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

    def setDataLog(self):
        # 캔버스 생성
        self.bottom_frame_second.grid_columnconfigure(0, weight=40)  # 캔버스의 열을 확장
        self.bottom_frame_second.grid_columnconfigure(1, weight=1)  # 스크롤바의 열을 고정
        self.bottom_frame_second.grid_rowconfigure(0, weight=1)  # 캔버스의 열을 확장

        self.bottom_frame_second_left = Frame(self.bottom_frame_second, bg='white')
        self.bottom_frame_second_left.propagate(False)
        self.bottom_frame_second_left.grid(row=0, column=0, sticky="nsew")

        self.canvas = Canvas(self.bottom_frame_second_left)
        self.canvas.pack(side=LEFT, fill='both', expand=True)

        self.bottom_frame_second_right = Frame(self.bottom_frame_second, bg='orange')
        self.bottom_frame_second_right.propagate(False)
        self.bottom_frame_second_right.grid(row=0, column=1, sticky="nsew")

        # 수직 스크롤바 생성 및 캔버스와 연결
        vscrollbar = Scrollbar(self.bottom_frame_second_right, orient='vertical', command=self.canvas.yview)
        vscrollbar.pack(side=LEFT, fill='both')

        self.canvas.configure(yscrollcommand=vscrollbar.set)

        # 캔버스 내부에 위젯을 담을 프레임 생성
        self.scrollable_frame = Frame(self.canvas, bg='orange')
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # 프레임 내에 라벨 배치
        for row in range(10):
            for col in range(5):
                label = Label(self.scrollable_frame, text=f"", bg="white", fg="black", font=("Arial", 10), width=14,
                              height=6)
                label.grid(row=row, column=col, pady=1)

        # 캔버스의 크기가 변경될 때 스크롤 영역을 적절하게 조정
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class ShowSearchFrame(SearchListFrame):
    def __init__(self, parent):
        super().__init__(parent)
