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

        self.sub_frame1 = Frame()
        self.sub_frame1.pack()
        self.sub_frame2 = Frame()
        self.sub_frame2.pack()

        self.image1 = PhotoImage(file="image/search.png").subsample(self.button_image_size, self.button_image_size)
        self.image2 = PhotoImage(file="image/star.png").subsample(self.button_image_size, self.button_image_size)
        self.image3 = PhotoImage(file="image/graph.png").subsample(self.button_image_size, self.button_image_size)

        # 버튼과 라벨 생성 함수 호출
        self.create_button_with_label(self.left_frame, self.image1, "검색", 0, lambda: self.show_frame(self.search_frame))
        self.create_button_with_label(self.left_frame, self.image2, "즐겨찾기", 1, lambda: self.show_frame(self.favorite_frame))
        self.create_button_with_label(self.left_frame, self.image3, "통계", 2, lambda: self.show_frame(self.graph_frame))

        # 오른쪽 프레임들 생성
        self.search_frame = Frame(self.window, bg='light blue')
        self.favorite_frame = Frame(self.window, bg='light green')
        self.graph_frame = Frame(self.window, bg='light yellow')

        # 프레임 내부에 라벨 추가
        Label(self.search_frame, text="1번 프레임", font=("Arial", 16)).pack(pady=20)
        Label(self.favorite_frame, text="2번 프레임", font=("Arial", 16)).pack(pady=20)
        Label(self.graph_frame, text="3번 프레임", font=("Arial", 16)).pack(pady=20)

        self.current_frame = None
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
        if self.current_frame:
            self.current_frame.pack_forget()  # 현재 프레임 숨기기
        frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.current_frame = frame

        if self.current_frame == self.search_frame:
            self.sub_frame1.pack_forget()
            self.sub_frame2.pack_forget()

            self.sub_frame1 = Frame(self.search_frame, bg='pink')
            self.sub_frame1.pack(side=LEFT, fill=BOTH, expand=True)

            self.sub_frame2 = Frame(self.search_frame, bg='light coral')
            self.sub_frame2.pack(side=LEFT, fill=BOTH, expand=True)

            Label(self.sub_frame1, text="서브 프레임 1", font=("Arial", 16)).pack(pady=20)
            Label(self.sub_frame2, text="서브 프레임 2", font=("Arial", 16)).pack(pady=20)

        if self.current_frame == self.favorite_frame:
            self.sub_frame1.pack_forget()
            self.sub_frame2.pack_forget()

            self.sub_frame1 = Frame(self.favorite_frame, bg='red')
            self.sub_frame1.pack(side=LEFT, fill=BOTH, expand=True)

            Label(self.sub_frame1, text="서브 프레임 1", font=("Arial", 16)).pack(pady=20)

        if self.current_frame == self.graph_frame:
            self.sub_frame1.pack_forget()
            self.sub_frame2.pack_forget()

            self.sub_frame1 = Frame(self.graph_frame, bg='red')
            self.sub_frame1.pack(side=LEFT, fill=BOTH, expand=True)

            self.sub_frame2 = Frame(self.graph_frame, bg='light blue')
            self.sub_frame2.pack(side=LEFT, fill=BOTH, expand=True)

            Label(self.sub_frame1, text="서브 프레임 1", font=("Arial", 16)).pack(pady=20)
            Label(self.sub_frame2, text="서브 프레임 2", font=("Arial", 16)).pack(pady=20)


MainFrame()
