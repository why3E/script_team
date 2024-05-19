from tkinter import *


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

        self.image1 = PhotoImage(file="image/search.png").subsample(self.button_image_size, self.button_image_size)
        self.image2 = PhotoImage(file="image/star.png").subsample(self.button_image_size, self.button_image_size)
        self.image3 = PhotoImage(file="image/graph.png").subsample(self.button_image_size, self.button_image_size)

        # 1번 버튼과 라벨을 포함하는 프레임 생성
        self.search_button_label = Frame(self.left_frame)
        self.search_button_label.grid(row=0, column=0, padx=45, pady=self.window_height / 30)

        self.button1 = Button(self.search_button_label, image=self.image1, compound=TOP, width=150, height=150,
                              command=lambda: self.show_frame(self.search_frame))
        self.button1.pack()

        self.label1 = Label(self.search_button_label, text='검색', font=("Arial", 12), compound=TOP)
        self.label1.pack()

        # 2번 버튼과 라벨
        self.favorite_button_label = Frame(self.left_frame)
        self.favorite_button_label.grid(row=1, column=0, padx=45, pady=self.window_height / 30)

        self.button2 = Button(self.favorite_button_label, image=self.image2, compound=TOP, width=150, height=150,
                              command=lambda: self.show_frame(self.favorite_frame))
        self.button2.pack()

        self.label2 = Label(self.favorite_button_label, text='즐겨찾기', font=("Arial", 12), compound=TOP)
        self.label2.pack()

        # 3번 버튼과 라벨
        self.graph_button_label = Frame(self.left_frame)
        self.graph_button_label.grid(row=2, column=0, padx=45, pady=self.window_height / 30)

        self.button3 = Button(self.graph_button_label, image=self.image3, compound=TOP, width=150, height=150,
                              command=lambda: self.show_frame(self.graph_frame))
        self.button3.pack()

        self.label3 = Label(self.graph_button_label, text='통계', font=("Arial", 12), compound=TOP)
        self.label3.pack()

        # 오른쪽 프레임들 생성
        self.search_frame = Frame(self.window, bg='light blue')
        self.favorite_frame = Frame(self.window, bg='light green')
        self.graph_frame = Frame(self.window, bg='light yellow')

        # 프레임 내부에 버튼 추가 (예시)
        Label(self.search_frame, text="1번 프레임", font=("Arial", 16)).pack(pady=20)
        Label(self.favorite_frame, text="2번 프레임", font=("Arial", 16)).pack(pady=20)
        Label(self.graph_frame, text="3번 프레임", font=("Arial", 16)).pack(pady=20)

        self.current_frame = None
        self.show_frame(self.search_frame)  # 초기화면을 프레임 1로 설정

        self.window.mainloop()

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()  # 현재 프레임 숨기기
        frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.current_frame = frame


MainFrame()
