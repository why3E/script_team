from tkinter import *
import calendar


class Calender:
    def __init__(self, parent):
        self.date_selector_frame = Frame(parent)
        self.date_selector_frame.pack(side=LEFT, pady=10)

        self.selected_date_label = Label(self.date_selector_frame, text="시작일: 없음", font=("Arial", 10))
        self.selected_date_label.pack(side=LEFT)

        select_date_button = Button(self.date_selector_frame, text="날짜 선택", command=lambda: self.open_date_popup())
        select_date_button.pack(side=LEFT)

    def open_date_popup(self):
        self.year = 2024
        self.month = 1
        self.day = 0

        self.window = Toplevel()
        self.window.title("날짜 선택")

        # 년도와 월 선택
        control_frame = Frame(self.window)
        control_frame.pack(fill=X)

        year_left_button = Button(control_frame, text="<", command=lambda: self.update_calendar(-1, 0))
        year_left_button.pack(side=LEFT)

        self.year_label = Label(control_frame, text=str(self.year), font=("Arial", 10))
        self.year_label.pack(side=LEFT, pady=10)

        year_right_button = Button(control_frame, text=">", command=lambda: self.update_calendar(1, 0))
        year_right_button.pack(side=LEFT)

        month_left_button = Button(control_frame, text="<", command=lambda: self.update_calendar(0, -1))
        month_left_button.pack(side=LEFT)

        self.month_label = Label(control_frame, text=str(self.month), font=("Arial", 10))
        self.month_label.pack(side=LEFT, pady=10)

        month_right_button = Button(control_frame, text=">", command=lambda: self.update_calendar(0, 1))
        month_right_button.pack(side=LEFT)

        # 달력 생성
        self.calendar_frame = Frame(self.window)
        self.calendar_frame.pack(fill=BOTH, expand=True)

        self.create_calendar()

        select_button = Button(self.window, text="선택", command=lambda: self.select_date(self.window))
        select_button.pack()

    def update_calendar(self, year_delta, month_delta):
        self.year += year_delta
        self.month += month_delta

        if self.month > 12:
            self.month = 1
            self.year += 1
        elif self.month < 1:
            self.month = 12
            self.year -= 1

        self.year_label.config(text=str(self.year))
        self.month_label.config(text=str(self.month))

        self.create_calendar()

    def create_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar()
        dates = cal.monthdatescalendar(self.year, self.month)

        for week in dates:
            week_frame = Frame(self.calendar_frame)
            week_frame.pack(fill=X)

            for date in week:
                self.create_day_button(week_frame, date)

    def create_day_button(self, parent, date):
        day_button = Button(
            parent, text=date.day,  #
            width=4, height=2,  # 픽셀 단위로 버튼 크기 지정
            state=NORMAL if date.month == self.month else DISABLED,
            command=self.create_day_button_command(date)
        )
        day_button.pack(side=LEFT, padx=5, pady=5)  # 버튼 간격 조정

    def create_day_button_command(self, day):
        def command():
            self.set_selected_day(day)

        return command

    def set_selected_day(self, day):
        self.date = day
        self.selected_date_label.config(text=f"{self.date}")

        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day  #

    def select_date(self, top):
        try:
            selected_date = f"{self.date.year}-{self.date.month:02}-{self.date.day:02}"  #
            self.selected_date_label.config(text=f"{selected_date}")

            self.year = self.date.year
            self.month = self.date.month
            self.day = self.date.day  #

        except Exception as e:
            self.selected_date_label.config(text="시작일: 없음")
        top.destroy()
