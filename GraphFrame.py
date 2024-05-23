from tkinter import *
from xmlRead import xmlRead
from Calender import Calender
from tkinter.ttk import Combobox


class GraphFrame(Frame):
    cate_category = [
        '연극',
        '뮤지컬',
        '서양음악',
        '한국음악',
        '대중음악',
        '무용',
        '대중무용',
        '서커스/마술',
        '복합'
    ]

    def __init__(self, parent, main_frame):
        super().__init__(parent)

        self.state = True  # True : 티켓 정보, False : 횟수 정보
        self.data = {category: {} for category in GraphFrame.cate_category}

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=12)
        self.grid_columnconfigure(0, weight=1)

        self.sub_frame_top = Frame(self, bg="orange")
        self.sub_frame_top.grid(row=0, column=0, sticky='nsew')

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
        self.circular_frame.grid_rowconfigure(0, weight=1)
        self.circular_frame.grid_columnconfigure(0, weight=1)
        self.circular_frame.grid(row=0, column=1, sticky='nsew')
        self.circular_canvas = Canvas(self.circular_frame, bg='gray')
        self.circular_canvas.grid(row=0, column=0, sticky='nsew')

        self.from_calender = Calender(self.sub_frame_top)
        self.to_calender = Calender(self.sub_frame_top)

        self.mode_selector = Combobox(self.sub_frame_top, values=['지역', '장르'])
        self.mode_selector.pack(side=LEFT, padx=20, pady=10)

        Button(self.sub_frame_top, command=self.draw_graph).pack(side=LEFT, padx=20, pady=10)

    def show(self):
        self.pack(side=RIGHT, fill=BOTH, expand=True)

    def hide(self):
        self.pack_forget()

    def getInfo(self, mode):
        fetcher = xmlRead()

        from_date = self.from_calender.get_date()
        to_date = self.from_calender.get_date()

        if mode == '장르':
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

    def draw_graph(self):
        self.bar_canvas.delete('all')
        self.circular_canvas.delete('all')

        mode = self.mode_selector.get()

        self.getInfo(mode)

        self.draw_bar_graph()
        self.draw_circular_graph()

        self.state = not self.state  # 테스트

    def draw_bar_graph(self):
        self.bar_canvas.create_line(50, self.bar_canvas.winfo_height() - 70, self.bar_canvas.winfo_width() - 50,
                                    self.bar_canvas.winfo_height() - 70)
        self.bar_canvas.create_line(50, self.bar_canvas.winfo_height() - 70, 50, 50)

        if self.state:
            col = 1
            gap = (self.bar_canvas.winfo_width() - 100) // len(GraphFrame.cate_category)
            bh = self.get_max_value('nmrs')

            for dk, dv in self.data.items():
                self.bar_canvas.create_text(20 + col * gap, self.bar_canvas.winfo_height() - 35, text=dk)
                for k, v in dv.items():
                    if k == 'nmrs' and int(v) != 0:
                        h = (self.bar_canvas.winfo_height() - 190) * int(v) / bh
                        self.bar_canvas.create_rectangle(5 + col * gap, self.bar_canvas.winfo_height() - 70 - h,
                                                         35 + col * gap, self.bar_canvas.winfo_height() - 70, fill='blue')
                col += 1
        else:
            col = 1
            gap = (self.bar_canvas.winfo_width() - 100) // len(GraphFrame.cate_category)
            bh = self.get_max_value('prfdtcnt')

            for dk, dv in self.data.items():
                self.bar_canvas.create_text(20 + col * gap, self.bar_canvas.winfo_height() - 35, text=dk)
                for k, v in dv.items():
                    if k == 'prfdtcnt' and int(v) != 0:
                        h = (self.bar_canvas.winfo_height() - 190) * int(v) / bh
                        self.bar_canvas.create_rectangle(5 + col * gap, self.bar_canvas.winfo_height() - 70 - h,
                                                         35 + col * gap, self.bar_canvas.winfo_height() - 70, fill='blue')
                col += 1

    def draw_circular_graph(self):
        pass
