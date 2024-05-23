from tkinter import *
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=12)
        self.grid_columnconfigure(0, weight=1)

        self.sub_frame_top = Frame(self, bg="orange")
        self.sub_frame_top.grid(row=0, column=0, sticky='nsew')
        self.sub_frame_top.grid_rowconfigure(0, weight=1)
        self.sub_frame_top.grid_columnconfigure(0, weight=2)
        self.sub_frame_top.grid_columnconfigure(1, weight=1)
        self.sub_frame_top.grid_columnconfigure(2, weight=1)
        self.sub_frame_top.grid_columnconfigure(3, weight=1)

        calender_frame = Frame(self.sub_frame_top, bg='orange')
        calender_frame.grid(row=0, column=0, sticky='nsew')
        calender_frame.grid_rowconfigure(0, weight=1)
        calender_frame.grid_columnconfigure(0, weight=1)
        calender_frame.grid_columnconfigure(1, weight=1)
        self.from_calender = Calender(calender_frame)
        self.from_calender.date_selector_frame.grid(row=0, column=0)
        self.to_calender = Calender(calender_frame)
        self.to_calender.date_selector_frame.grid(row=0, column=1)

        self.mode_selector = Combobox(self.sub_frame_top, values=['지역', '장르'])
        self.mode_selector.grid(row=0, column=1)

        checkbutton_frame = Frame(self.sub_frame_top, bg='white')
        checkbutton_frame.grid(row=0, column=2)
        checkbutton_frame.grid_columnconfigure(0, weight=1)
        checkbutton_frame.grid_columnconfigure(1, weight=1)
        self.nmrsVar = IntVar()
        nmrs = Checkbutton(checkbutton_frame, text='티켓 판매', variable=self.nmrsVar, command=self.toggle_graph)
        nmrs.grid(row=0, column=0, padx=10)
        self.prfprocntVar = IntVar()
        prfprocnt = Checkbutton(checkbutton_frame, text='공연 횟수', variable=self.prfprocntVar, command=self.toggle_graph)
        prfprocnt.grid(row=0, column=1, padx=10)

        image = PhotoImage(file="image/small_search.png")
        button = Button(self.sub_frame_top, image=image, command=self.draw_graph)
        button.image = image
        button.grid(row=0, column=3)

        self.sub_frame1 = Frame(self, bg='pink')
        self.sub_frame1.grid(row=1, column=0, sticky='nsew')
        self.sub_frame1.grid_rowconfigure(0, weight=1)
        self.sub_frame1.grid_columnconfigure(0, weight=2)
        self.sub_frame1.grid_columnconfigure(1, weight=1)

        self.bar_frame = Frame(self.sub_frame1, bg='white')
        self.bar_frame.grid_propagate(False)
        self.bar_frame.grid(row=0, column=0, sticky='nsew')
        self.bar_frame.grid_rowconfigure(0, weight=1)
        self.bar_frame.grid_columnconfigure(0, weight=1)
        self.bar_canvas = Canvas(self.bar_frame, bg='white')
        self.bar_canvas.grid(row=0, column=0, sticky='nsew')

        self.circular_frame = Frame(self.sub_frame1, bg='white')
        self.circular_frame.grid_propagate(False)
        self.circular_frame.grid(row=0, column=1, sticky='nsew')
        self.circular_frame.grid_rowconfigure(0, weight=1)
        self.circular_frame.grid_columnconfigure(0, weight=1)
        self.circular_canvas = None

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

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
        if self.mode != self.mode_selector.get():
            return

        self.is_toggle = True
        self.draw_graph()
        self.is_toggle = False

    def draw_graph(self):
        self.bar_canvas.delete('all')
        if self.circular_canvas:
            self.circular_canvas.get_tk_widget().delete('all')

        self.mode = self.mode_selector.get()

        if self.mode:
            self.setInfo(self.mode)
        else:
            return

        self.bar_canvas.create_line(50, self.bar_canvas.winfo_height() - 70,
                                    self.distance - 50, self.bar_canvas.winfo_height() - 70)
        self.bar_canvas.create_line(50, self.bar_canvas.winfo_height() - 70, 50, 50)

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
                    bh = self.get_max_value('nmrs')
                    h = (self.bar_canvas.winfo_height() - 190) * int(v) / bh
                    self.bar_canvas.create_rectangle(5 + col * self.gap, self.bar_canvas.winfo_height() - 70 - h,
                                                     20 + col * self.gap, self.bar_canvas.winfo_height() - 70,
                                                     fill='red')
                if k == 'amount' and int(v) != 0:
                    bh = self.get_max_value('amount')
                    h = (self.bar_canvas.winfo_height() - 190) * int(v) / bh
                    self.bar_canvas.create_rectangle(20 + col * self.gap, self.bar_canvas.winfo_height() - 70 - h,
                                                     35 + col * self.gap, self.bar_canvas.winfo_height() - 70,
                                                     fill='blue')
            col += 1

    def draw_line_graph(self):
        col = 1
        prfprocnt_points = []
        prfdtcnt_points = []

        for dk, dv in self.data.items():
            if self.state == 'prfprocnt': self.bar_canvas.create_text(20 + col * self.gap,
                                                                      self.bar_canvas.winfo_height() - 35, text=dk)
            for k, v in dv.items():
                if k == 'prfprocnt':
                    lh = self.get_max_value('prfprocnt')
                    h = (self.bar_canvas.winfo_height() - 190) * int(v) / lh
                    prfprocnt_points.append((20 + col * self.gap, self.bar_canvas.winfo_height() - 70 - h))
                if k == 'prfdtcnt':
                    lh = self.get_max_value('prfdtcnt')
                    h = (self.bar_canvas.winfo_height() - 190) * int(v) / lh
                    prfdtcnt_points.append((20 + col * self.gap, self.bar_canvas.winfo_height() - 70 - h))
            col += 1

        for i in range(len(prfprocnt_points)):
            if i != len(prfprocnt_points) - 1:
                self.bar_canvas.create_line(prfprocnt_points[i][0], prfprocnt_points[i][1], prfprocnt_points[i + 1][0],
                                            prfprocnt_points[i + 1][1], width=3)
                self.bar_canvas.create_line(prfdtcnt_points[i][0], prfdtcnt_points[i][1],
                                            prfdtcnt_points[i + 1][0], prfdtcnt_points[i + 1][1],
                                            fill='gray', width=3)
            self.bar_canvas.create_oval(prfprocnt_points[i][0] - 5, prfprocnt_points[i][1] - 5,
                                        prfprocnt_points[i][0] + 5, prfprocnt_points[i][1] + 5, fill='white', width=3)
            self.bar_canvas.create_oval(prfdtcnt_points[i][0] - 5, prfdtcnt_points[i][1] - 5,
                                        prfdtcnt_points[i][0] + 5, prfdtcnt_points[i][1] + 5,
                                        outline='gray', fill='white', width=3)

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
        ax.pie(shr, labels=labels, colors=colors, shadow=True, explode=explode, autopct=self.autopct_func,
               startangle=90)
        ax.axis('equal')  # 원형 유지

        self.circular_canvas = FigureCanvasTkAgg(fig, master=self.circular_frame)
        self.circular_canvas.draw()
        self.circular_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

    def autopct_func(self, pct):
        return f'{pct:.1f}%' if pct >= 10 else ''
