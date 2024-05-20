from tkinter import *
import calendar


class MainFrame:
    def __init__(self):
        self.window_width = 1200
        self.window_height = 700
        self.x_position = 250  # x 좌표
        self.y_position = 100  # y 좌표

        self.button_image_size = 2
        self.window = Tk()
        self.window.title("프레임")
        self.window.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")

        self.frame = Frame(self.window, bg='dim gray')
        self.frame.pack(side=LEFT, fill=Y)

        self.left_frame = Frame(self.frame, bg='gray')
        self.left_frame.pack(side=LEFT, fill=Y)

        self.search_frame = Frame(self.window, bg='light blue')
        self.favorite_frame = Frame(self.window, bg='light green')
        self.graph_frame = Frame(self.window, bg='light yellow')

        self.sub_frame1 = Frame()
        self.sub_frame1.pack()
        self.sub_frame2 = Frame()
        self.sub_frame2.pack()

        self.image1 = PhotoImage(file="image/search.png").subsample(self.button_image_size, self.button_image_size)
        self.image2 = PhotoImage(file="image/star.png").subsample(self.button_image_size, self.button_image_size)
        self.image3 = PhotoImage(file="image/graph.png").subsample(self.button_image_size, self.button_image_size)

        # 버튼과 라벨 생성 함수 호출
        self.create_button_with_label(self.left_frame, self.image1, "검색", 0, lambda: self.show_frame(self.search_frame))
        self.create_button_with_label(self.left_frame, self.image2, "즐겨찾기", 1,
                                      lambda: self.show_frame(self.favorite_frame))
        self.create_button_with_label(self.left_frame, self.image3, "통계", 2, lambda: self.show_frame(self.graph_frame))

        self.current_frame = self.search_frame
        self.show_frame(self.search_frame)  # 초기 화면을 검색 프레임로 설정

        self.window.mainloop()

    def create_button_with_label(self, parent, image, text, row, command):
        frame = Frame(parent)
        frame.grid(row=row, column=0, padx=45, pady=self.window_height / 30)

        button = Button(frame, image=image, compound=TOP, width=150, height=150, command=command)
        button.pack()

        label = Label(frame, text=text, font=("Arial", 12), compound=TOP)
        label.pack()

    def show_frame(self, frame):

        print("버튼 실행1")
        if self.current_frame:
            self.current_frame.pack_forget()  # 현재 프레임 숨기기
        frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.current_frame = frame

        if self.current_frame == self.search_frame:
            self.create_sub_frames(self.search_frame)

        if self.current_frame == self.favorite_frame:
            self.create_sub_frames(self.favorite_frame)

        if self.current_frame == self.graph_frame:
            self.create_sub_frames(self.graph_frame)

    def create_sub_frames(self, parent):
        self.sub_frame1 = Frame(parent, bg='pink')
        self.sub_frame1.pack(side=LEFT, fill=BOTH, expand=True)

        if parent != self.graph_frame:
            self.sub_frame2 = Frame(parent, bg='light coral')
            self.sub_frame2.pack(side=LEFT, fill=BOTH, expand=True)

        Label(self.sub_frame1, text="서브 프레임 1", font=("Arial", 16)).pack(pady=20)
        if parent != self.graph_frame:
            Label(self.sub_frame2, text="서브 프레임 2", font=("Arial", 16)).pack(pady=20)

        self.create_date_selector(self.sub_frame1)



    def create_date_selector(self, parent):
        date_selector_frame = Frame(parent)
        date_selector_frame.pack(side=TOP, pady=20)

        self.selected_date_label = Label(date_selector_frame, text="시작일 : 없음", font=("Arial", 12))
        self.selected_date_label.pack(side=LEFT, padx=10)

        select_date_button = Button(date_selector_frame, text="날짜 선택", command=self.open_date_popup)
        select_date_button.pack(side=LEFT)

    def open_date_popup(self):
        self.selected_year = 2024
        self.selected_month = 1

        top = Toplevel(self.window)
        top.title("날짜 선택")

        # 년도와 월 선택
        control_frame = Frame(top)
        control_frame.pack(fill=X)

        year_left_button = Button(control_frame, text="<", command=lambda: self.update_calendar(-1, 0))
        year_left_button.pack(side=LEFT)

        self.year_label = Label(control_frame, text=str(self.selected_year), font=("Arial", 12))
        self.year_label.pack(side=LEFT, padx=10)

        year_right_button = Button(control_frame, text=">", command=lambda: self.update_calendar(1, 0))
        year_right_button.pack(side=LEFT)

        month_left_button = Button(control_frame, text="<", command=lambda: self.update_calendar(0, -1))
        month_left_button.pack(side=LEFT)

        self.month_label = Label(control_frame, text=str(self.selected_month), font=("Arial", 12))
        self.month_label.pack(side=LEFT, padx=10)

        month_right_button = Button(control_frame, text=">", command=lambda: self.update_calendar(0, 1))
        month_right_button.pack(side=LEFT)

        # 달력 생성
        self.calendar_frame = Frame(top)
        self.calendar_frame.pack(fill=BOTH, expand=True)

        self.create_calendar()

        select_button = Button(top, text="선택", command=lambda: self.select_date(top))
        select_button.pack()

    def update_calendar(self, year_delta, month_delta):
        self.selected_year += year_delta
        self.selected_month += month_delta

        if self.selected_month > 12:
            self.selected_month = 1
            self.selected_year += 1
        elif self.selected_month < 1:
            self.selected_month = 12
            self.selected_year -= 1

        self.year_label.config(text=str(self.selected_year))
        self.month_label.config(text=str(self.selected_month))

        self.create_calendar()



MainFrame()