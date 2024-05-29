from tkinter import *
from tkinter import messagebox
from xmlRead import xmlRead
from Calender import Calender
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

font_path = "font/malgunbd.ttf"  # 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

plt.rcParams.update({'font.size': 15})  # 전체 글자 크기 설정
plt.rcParams.update({'axes.titlesize': 20})  # 축 제목 크기 설정
plt.rcParams.update({'axes.labelsize': 20})  # 축 레이블 크기 설정
plt.rcParams.update({'legend.fontsize': 15})  # 범례 글자 크기 설정


class GraphFrame(Frame):
    cate_category = ['연극', '뮤지컬', '서양음악', '한국음악', '대중음악', '무용', '대중무용', '서커스/마술', '복합']

    region_category = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원',
                       '강원', '충북', '충남', '전북', '전북', '전남', '경북', '경남', '제주']

    def __init__(self, parent, main_frame):
        super().__init__(parent)

        self.state = ''  # nmrs : 티켓 정보, prfprocnt : 횟수 정보
        self.mode = None
        self.data = None
        self.is_toggle = False

        self.sub_frame_top = Frame(self, bg='lightgray')
        self.sub_frame_top.grid(row=0, column=0, pady=5, sticky='nsew')

        self.calender_frame = Frame(self.sub_frame_top, bg='lightgray')
        self.calender_frame.grid(row=0, column=0, sticky='nsew')
        self.from_calender = Calender(self.calender_frame)
        self.from_calender.date_selector_frame.grid(row=0, column=0)
        self.to_calender = Calender(self.calender_frame)
        self.to_calender.date_selector_frame.grid(row=0, column=1)

        self.mode_selector = Combobox(self.sub_frame_top, values=['지역', '장르'])
        self.mode_selector.grid(row=0, column=1)

        self.checkbutton_frame = Frame(self.sub_frame_top, bg='lightgray')
        self.checkbutton_frame.grid(row=0, column=2)
        self.nmrsVar = IntVar()
        Checkbutton(self.checkbutton_frame, text='티켓 판매', variable=self.nmrsVar, command=self.toggle_graph).grid(row=0, column=0, padx=10)
        self.prfprocntVar = IntVar()
        Checkbutton(self.checkbutton_frame, text='공연 횟수', variable=self.prfprocntVar, command=self.toggle_graph).grid(row=0, column=1, padx=10)

        image = PhotoImage(file="image/small_search.png")
        button = Button(self.sub_frame_top, image=image, command=self.draw_graph)
        button.image = image
        button.grid(row=0, column=3)

        self.sub_frame1 = Frame(self, bg='pink')
        self.sub_frame1.grid(row=1, column=0, pady=5, sticky='nsew')

        self.bar_frame = Frame(self.sub_frame1, bg='white')
        self.bar_frame.grid(row=0, column=0, sticky='nsew')
        self.bar_canvas = Canvas(self.bar_frame, bg='white')
        self.bar_canvas.grid(row=0, column=0, sticky='nsew')

        self.circular_frame = Frame(self.sub_frame1, bg='white')
        self.circular_frame.grid(row=0, column=1, sticky='nsew')
        self.circular_canvas = None

        self.grid_propagate_configure()

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, padx=5, pady=5, expand=True)

    def hide(self):
        self.pack_forget()

    def setInfo(self, mode):
        fetcher = xmlRead()

        from_date = self.from_calender.get_date()
        to_date = self.from_calender.get_date()

        if self.mode == '지역':
            self.distance = self.sub_frame_top.winfo_width()
            self.gap = (self.distance - 100) // (len(GraphFrame.region_category) - 2)
        else:
            self.distance = self.sub_frame_top.winfo_width() * 2 // 3
            self.gap = (self.distance - 100) // len(GraphFrame.cate_category)

        if self.nmrsVar.get() and self.prfprocntVar.get():
            self.state = 'both'
        elif self.nmrsVar.get():
            self.state = 'nmrs'
        elif self.prfprocntVar.get():
            self.state = 'prfprocnt'
        else:
            self.state = None
            return

        if not self.is_toggle:
            if mode == '지역':
                self.sub_frame1.grid_columnconfigure(1, weight=0)
                self.data = {region: {} for region in GraphFrame.region_category}

                data = fetcher.fetch_and_parse_region_data(from_date, to_date)

                for i, d in enumerate(data):
                    if self.data[GraphFrame.region_category[i]]: continue
                    for k, v in d.items():
                        self.data[GraphFrame.region_category[i]][k] = v
            elif mode == '장르':
                self.sub_frame1.grid_columnconfigure(1, weight=1)
                self.data = {category: {} for category in GraphFrame.cate_category}

                data = fetcher.fetch_and_parse_genre_data(from_date, to_date)

                for i, d in enumerate(data):
                    for k, v in d.items():
                        self.data[GraphFrame.cate_category[i]][k] = v

    def get_max_value(self, key):
        maxValue = 0

        for dv in self.data.values():
            if maxValue < int(dv[key]):
                maxValue = int(dv[key])

        return maxValue

    def toggle_graph(self):
        if self.mode != self.mode_selector.get() or not self.state:
            return

        self.is_toggle = True
        self.draw_graph()
        self.is_toggle = False

    def draw_graph(self):
        if not self.from_calender.get_date() or not self.to_calender.get_date():
            messagebox.showwarning('알림', '날짜가 선택되지 않았습니다.')
            return

        if self.from_calender.get_date() > self.to_calender.get_date():
            messagebox.showwarning('알림', '종료일은 시작일보다 앞설 수 없습니다.')
            return

        self.bar_canvas.delete('all')
        if self.circular_canvas:
            self.circular_canvas.get_tk_widget().delete('all')

        self.mode = self.mode_selector.get()

        if self.mode:
            self.setInfo(self.mode)

        if self.state == None:
            return

        self.bar_canvas.create_line(50, self.bar_canvas.winfo_height() - 70, self.distance - 50, self.bar_canvas.winfo_height() - 70)
        self.bar_canvas.create_line(50, self.bar_canvas.winfo_height() - 70, 50, 50)
        self.bar_canvas.create_line(self.distance - 50, self.bar_canvas.winfo_height() - 70, self.distance - 50, 50)
        self.bar_canvas.create_text(50, 30, text='티켓 판매 수')
        self.bar_canvas.create_text(self.distance - 50, 37, text='티켓 판매액')
        self.bar_canvas.create_text(self.distance - 50, 23, text='(단위 : 억)')

        gap = (self.distance - 100) // 5
        self.bar_canvas.create_rectangle(50 + gap * 1 - 10 - 5, 30 - 5,
                                         50 + gap * 1 - 10 + 5, 30 + 5,
                                         fill='red')
        self.bar_canvas.create_text(50 + gap * 1 + 45, 30, text=': 총 티켓 판매 수')

        self.bar_canvas.create_rectangle(50 + gap * 2 - 10 - 5, 30 - 5,
                                         50 + gap * 2 - 10 + 5, 30 + 5,
                                         fill='blue')
        self.bar_canvas.create_text(50 + gap * 2 + 35, 30, text=': 티켓 판매액')

        self.bar_canvas.create_line(50 + gap * 3 - 10 - 10, 30, 50 + gap * 3 - 10 + 10, 30, width=3)
        self.bar_canvas.create_oval(50 + gap * 3 - 10 - 5, 30 - 5,
                                    50 + gap * 3 - 10 + 5, 30 + 5,
                                    fill='white', width=3)
        self.bar_canvas.create_text(50 + gap * 3 + 35, 30, text=': 개막 편수')

        self.bar_canvas.create_line(50 + gap * 4 - 10 - 10, 30, 50 + gap * 4 - 10 + 10, 30, width=3, fill='gray')
        self.bar_canvas.create_oval(50 + gap * 4 - 10 - 5, 30 - 5,
                                    50 + gap * 4 - 10 + 5, 30 + 5,
                                    outline='gray', fill='white', width=3)
        self.bar_canvas.create_text(50 + gap * 4 + 35, 30, text=': 상연 횟수')

        if self.state != 'prfprocnt':
            self.draw_bar_graph()

        if self.state != 'nmrs':
            self.draw_line_graph()

        if self.mode == '장르':
            self.draw_circular_graph()

    def draw_bar_graph(self):
        col = 1

        for dk, dv in self.data.items():
            self.bar_canvas.create_text(20 + col * self.gap, self.bar_canvas.winfo_height() - 35, text=dk)
            for k, v in dv.items():
                if k == 'nmrs' and int(v) != 0:
                    bh1 = self.get_max_value('nmrs')
                    h = (self.bar_canvas.winfo_height() - 190) * int(v) / bh1
                    self.bar_canvas.create_rectangle(5 + col * self.gap, self.bar_canvas.winfo_height() - 70 - h,
                                                     20 + col * self.gap, self.bar_canvas.winfo_height() - 70,
                                                     fill='red')
                if k == 'amount' and int(v) != 0:
                    bh2 = self.get_max_value('amount')
                    h = (self.bar_canvas.winfo_height() - 190) * int(v) / bh2
                    self.bar_canvas.create_rectangle(20 + col * self.gap, self.bar_canvas.winfo_height() - 70 - h,
                                                     35 + col * self.gap, self.bar_canvas.winfo_height() - 70,
                                                     fill='blue')
            col += 1

        digit1 = 10 ** (len(str(bh1)) - 1)
        for i in range(1, bh1 // digit1 + 1):
            h = (self.bar_canvas.winfo_height() - 190) * int(digit1 * i) / bh1
            self.bar_canvas.create_line(45, self.bar_canvas.winfo_height() - 70 - h,
                                        55, self.bar_canvas.winfo_height() - 70 - h)
            self.bar_canvas.create_text(25, self.bar_canvas.winfo_height() - 70 - h, text=str(digit1 * i))

        digit2 = 10 ** (len(str(bh2)) - 2)
        for i in range(1, bh2 // digit2 + 1):
            if i % 5 == 0:
                h = (self.bar_canvas.winfo_height() - 190) * int(digit2 * i) / bh2
                self.bar_canvas.create_line(self.distance - 45, self.bar_canvas.winfo_height() - 70 - h,
                                            self.distance - 55, self.bar_canvas.winfo_height() - 70 - h)
                self.bar_canvas.create_text(self.distance - 25, self.bar_canvas.winfo_height() - 70 - h, text=str(digit2 * i // 100000000))

    def draw_line_graph(self):
        col = 1
        prfprocnt_points = []
        prfdtcnt_points = []
        prfprocnt_values = []
        prfdtcnt_values = []

        for dk, dv in self.data.items():
            if self.state == 'prfprocnt': self.bar_canvas.create_text(20 + col * self.gap, self.bar_canvas.winfo_height() - 35, text=dk)
            for k, v in dv.items():
                if k == 'prfprocnt':
                    lh = self.get_max_value('prfprocnt')
                    h = (self.bar_canvas.winfo_height() - 190) * int(v) / lh
                    prfprocnt_points.append((20 + col * self.gap, self.bar_canvas.winfo_height() - 70 - h))
                    prfprocnt_values.append(int(v))
                if k == 'prfdtcnt':
                    lh = self.get_max_value('prfdtcnt')
                    h = (self.bar_canvas.winfo_height() - 190) * int(v) / lh
                    prfdtcnt_points.append((20 + col * self.gap, self.bar_canvas.winfo_height() - 70 - h))
                    prfdtcnt_values.append(int(v))
            col += 1

        for i in range(len(prfprocnt_points)):
            if i != len(prfprocnt_points) - 1:
                self.bar_canvas.create_line(prfprocnt_points[i][0], prfprocnt_points[i][1],
                                            prfprocnt_points[i + 1][0], prfprocnt_points[i + 1][1],
                                            width=3)
                self.bar_canvas.create_line(prfdtcnt_points[i][0], prfdtcnt_points[i][1],
                                            prfdtcnt_points[i + 1][0], prfdtcnt_points[i + 1][1],
                                            fill='gray', width=3)

        for i in range(len(prfprocnt_points)):
            self.bar_canvas.create_oval(prfprocnt_points[i][0] - 5, prfprocnt_points[i][1] - 5,
                                        prfprocnt_points[i][0] + 5, prfprocnt_points[i][1] + 5,
                                        fill='white', width=3)
            self.bar_canvas.create_oval(prfdtcnt_points[i][0] - 5, prfdtcnt_points[i][1] - 5,
                                        prfdtcnt_points[i][0] + 5, prfdtcnt_points[i][1] + 5,
                                        outline='gray', fill='white', width=3)

            if (prfprocnt_points[i][1] >= prfdtcnt_points[i][1]): g1, g2 = 19, -17
            else: g1, g2 = -17, 19

            if prfprocnt_values[i] != 0:
                for dx in range(-2, 2 + 1):
                    for dy in range(-2, 2 + 1):
                        if dx != 0 or dy != 0:
                            self.bar_canvas.create_text(prfprocnt_points[i][0] + dx, prfprocnt_points[i][1] + g1 + dy,
                                                        text=str(prfprocnt_values[i]), font=('arial', 15, 'bold'))
                self.bar_canvas.create_text(prfprocnt_points[i][0], prfprocnt_points[i][1] + g1,
                                            text=str(prfprocnt_values[i]), font=('arial', 15, 'bold'), fill='white')
            if prfdtcnt_values[i] != 0:
                for dx in range(-2, 2 + 1):
                    for dy in range(-2, 2 + 1):
                        if dx != 0 or dy != 0:
                            self.bar_canvas.create_text(prfdtcnt_points[i][0] + dx, prfdtcnt_points[i][1] + g2 + dy,
                                                        text=str(prfdtcnt_values[i]), font=('arial', 15, 'bold'),
                                                        fill='gray')
                self.bar_canvas.create_text(prfdtcnt_points[i][0], prfdtcnt_points[i][1] + g2,
                                            text=str(prfdtcnt_values[i]), font=('arial', 15, 'bold'), fill='white')

    def draw_circular_graph(self):
        shr = []
        labels = []
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'azure', 'purple', 'gray', 'black']
        for dk, dv in self.data.items():
            for k, v in dv.items():
                if k == 'amountshr':
                    shr.append(float(v))
                    if float(v) > 10.0:
                        labels.append(dk)
                    else:
                        labels.append('')

        max_index = shr.index(max(shr))
        explode = [0.1 if i == max_index else 0 for i in range(len(shr))]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(shr, labels=labels, colors=colors, shadow=True, explode=explode, autopct=self.autopct_func, startangle=90)
        ax.axis('equal')  # 원형 유지

        self.circular_canvas = FigureCanvasTkAgg(fig, master=self.circular_frame)
        self.circular_canvas.draw()
        self.circular_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

    def autopct_func(self, pct):
        return f'{pct:.1f}%' if pct >= 10 else ''

    def grid_propagate_configure(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=12)
        self.grid_columnconfigure(0, weight=1)

        self.sub_frame_top.grid_rowconfigure(0, weight=1)
        self.sub_frame_top.grid_columnconfigure(0, weight=2)
        self.sub_frame_top.grid_columnconfigure(1, weight=1)
        self.sub_frame_top.grid_columnconfigure(2, weight=1)
        self.sub_frame_top.grid_columnconfigure(3, weight=1)

        self.calender_frame.grid_rowconfigure(0, weight=1)
        self.calender_frame.grid_columnconfigure(0, weight=1)
        self.calender_frame.grid_columnconfigure(1, weight=1)

        self.checkbutton_frame.grid_columnconfigure(0, weight=1)
        self.checkbutton_frame.grid_columnconfigure(1, weight=1)

        self.sub_frame1.grid_rowconfigure(0, weight=1)
        self.sub_frame1.grid_columnconfigure(0, weight=2)
        self.sub_frame1.grid_columnconfigure(1, weight=1)

        self.bar_frame.grid_propagate(False)
        self.bar_frame.grid_rowconfigure(0, weight=1)
        self.bar_frame.grid_columnconfigure(0, weight=1)

        self.circular_frame.grid_propagate(False)
        self.circular_frame.grid_rowconfigure(0, weight=1)
        self.circular_frame.grid_columnconfigure(0, weight=1)
