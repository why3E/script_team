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

        self.search_frame = SearchFrame(self.window, self)
        self.favorite_frame = FavoriteFrame(self.window, self)
        self.graph_frame = GraphFrame(self.window, self)

        self.search_frame.creatSearch()
        self.favorite_frame.creatFavorite()
        self.graph_frame.creatGraph()

        self.image1 = PhotoImage(file="image/search.png").subsample(self.button_image_size, self.button_image_size)
        self.image2 = PhotoImage(file="image/star.png").subsample(self.button_image_size, self.button_image_size)
        self.image3 = PhotoImage(file="image/graph.png").subsample(self.button_image_size, self.button_image_size)

        # 버튼과 라벨 생성 함수 호출
        self.create_button_with_label(self.left_frame, self.image1, "검색", 0, self.show_search_frame)
        self.create_button_with_label(self.left_frame, self.image2, "즐겨찾기", 1, self.show_favorite_frame)
        self.create_button_with_label(self.left_frame, self.image3, "통계", 2, self.show_graph_frame)

        self.current_frame = self.search_frame
        self.show_search_frame()  # 초기 화면을 검색 프레임로 설정

        self.window.mainloop()

    def create_button_with_label(self, parent, image, text, row, command):
        frame = Frame(parent)
        frame.grid(row=row, column=0, padx=45, pady=self.window_height / 30)

        button = Button(frame, image=image, compound=TOP, width=150, height=150, command=command)
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
        if self.current_frame:
            self.current_frame.pack_forget()  # 현재 프레임 숨기기
        frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.current_frame = frame

        if frame == self.search_frame:
            self.search_frame.sub_frame1.pack_forget()
            self.search_frame.sub_frame2.pack_forget()
            self.search_frame.creatSearch()

        if frame == self.favorite_frame:
            self.favorite_frame.sub_frame1.pack_forget()
            self.favorite_frame.sub_frame2.pack_forget()
            self.favorite_frame.creatFavorite()

        if frame == self.graph_frame:
            self.graph_frame.sub_frame1.pack_forget()
            self.graph_frame.creatGraph()

    def create_date_selector(self, parent, frame):
        date_selector_frame = Frame(parent)
        date_selector_frame.pack(side=LEFT, padx=20, pady=20)

        frame.selected_date_label = Label(date_selector_frame, text="시작일: 없음", font=("Arial", 10))
        frame.selected_date_label.pack(side=LEFT, padx=10)

        select_date_button = Button(date_selector_frame, text="날짜 선택", command=lambda: self.open_date_popup(frame))
        select_date_button.pack(side=LEFT)

    def open_date_popup(self, frame):
        self.selected_year = 2024
        self.selected_month = 1
        self.target_frame = frame

        top = Toplevel(self.window)
        top.title("날짜 선택")

        # 년도와 월 선택
        control_frame = Frame(top)
        control_frame.pack(fill=X)

        year_left_button = Button(control_frame, text="<", command=lambda: self.update_calendar(-1, 0))
        year_left_button.pack(side=LEFT)

        self.year_label = Label(control_frame, text=str(self.selected_year), font=("Arial", 10))
        self.year_label.pack(side=LEFT, padx=10)

        year_right_button = Button(control_frame, text=">", command=lambda: self.update_calendar(1, 0))
        year_right_button.pack(side=LEFT)

        month_left_button = Button(control_frame, text="<", command=lambda: self.update_calendar(0, -1))
        month_left_button.pack(side=LEFT)

        self.month_label = Label(control_frame, text=str(self.selected_month), font=("Arial", 10))
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

    def create_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar()
        dates = cal.monthdatescalendar(self.selected_year, self.selected_month)

        for week in dates:
            week_frame = Frame(self.calendar_frame)
            week_frame.pack(fill=X)

            for day in week:
                self.create_day_button(week_frame, day)

    def create_day_button(self, parent, day):
        day_button = Button(
            parent, text=day.day,
            width=4, height=2,  # 픽셀 단위로 버튼 크기 지정
            state=NORMAL if day.month == self.selected_month else DISABLED,
            command=self.create_day_button_command(day)
        )
        day_button.pack(side=LEFT, padx=5, pady=5)  # 버튼 간격 조정

    def create_day_button_command(self, day):
        def command():
            self.set_selected_day(day)

        return command

    def set_selected_day(self, day):
        self.selected_day = day
        self.target_frame.selected_date_label.config(text=f"시작일: {self.selected_day}")

    def select_date(self, top):
        try:
            selected_date = f"{self.selected_day.year}-{self.selected_day.month:02}-{self.selected_day.day:02}"
            self.target_frame.selected_date_label.config(text=f"시작일: {selected_date}")

            self.target_frame.selected_year = self.selected_day.year
            self.target_frame.selected_month = self.selected_day.month
            self.target_frame.selected_day = self.selected_day.day

        except Exception as e:
            self.target_frame.selected_date_label.config(text="시작일: 없음")
        top.destroy()

class SearchFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.selected_year = None
        self.selected_month = None
        self.selected_day = None

        self.selected_year = None
        self.selected_month = None
        self.selected_day = None

    def creatSearch(self):
        self.sub_frame1 = Frame(self, bg='pink')
        self.sub_frame2 = Frame(self, bg='light coral')
        self.label1 = Label(self.sub_frame1, text="서브 프레임 1", font=("Arial", 16))
        self.label2 = Label(self.sub_frame2, text="서브 프레임 2", font=("Arial", 16))

        self.sub_frame1.pack(side=LEFT, fill=BOTH, expand=True)
        self.sub_frame2.pack(side=LEFT, fill=BOTH, expand=True)
        self.label1.pack()
        self.label2.pack()

        self.sub_frame_top = Frame(self.sub_frame1, bg="orange")
        self.sub_frame_top.pack(side=TOP, anchor=N, fill=X, expand=True)

        self.main_frame.create_date_selector(self.sub_frame_top, self)
        self.main_frame.create_date_selector(self.sub_frame_top, self)

class FavoriteFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.selected_year = None
        self.selected_month = None
        self.selected_day = None

    def creatFavorite(self):
        self.sub_frame1 = Frame(self, bg='dim gray')
        self.sub_frame2 = Frame(self, bg='light blue')
        self.label1 = Label(self.sub_frame1, text="서브 프레임 1", font=("Arial", 16))
        self.label2 = Label(self.sub_frame2, text="서브 프레임 2", font=("Arial", 16))

        self.sub_frame1.pack(side=LEFT, fill=BOTH, expand=True)
        self.sub_frame2.pack(side=LEFT, fill=BOTH, expand=True)
        self.label1.pack(pady=20)
        self.label2.pack(pady=20)

        self.sub_frame_top = Frame(self.sub_frame1, bg="orange")
        self.sub_frame_top.pack(side=TOP, anchor=N, fill=X, expand=True)

        self.main_frame.create_date_selector(self.sub_frame_top, self)
        self.main_frame.create_date_selector(self.sub_frame_top, self)

class GraphFrame(Frame):
    def __init__(self, parent, main_frame):
        super().__init__(parent)
        self.main_frame = main_frame
        self.selected_year = None
        self.selected_month = None
        self.selected_day = None

    def creatGraph(self):
        self.sub_frame1 = Frame(self, bg='pink')
        self.label1 = Label(self.sub_frame1, text="서브 프레임 1", font=("Arial", 16))

        self.sub_frame1.pack(side=LEFT, fill=BOTH, expand=True)
        self.label1.pack(pady=20)

        self.sub_frame_top = Frame(self.sub_frame1, bg="orange")
        self.sub_frame_top.pack(side=TOP, anchor=N, fill=X, expand=True)

        self.main_frame.create_date_selector(self.sub_frame_top, self)


MainFrame()
