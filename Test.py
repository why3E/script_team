import tkinter as tk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.page = ""  # 초기값 설정

        self.bottom_frame_third = tk.Frame(root)
        self.bottom_frame_third.grid(row=0, column=0)

        self.bottom_frame_third_mid = tk.Frame(self.bottom_frame_third, bg='blue')
        self.bottom_frame_third_mid.propagate(False)
        self.bottom_frame_third_mid.grid(row=0, column=1, sticky="nsew")

        self.entry_mid = tk.Entry(self.bottom_frame_third_mid, width=20)
        self.entry_mid.pack()
        self.entry_mid.insert(0, self.page)
        self.entry_mid.bind('<Return>', self.save_page)

        self.save_button = tk.Button(self.bottom_frame_third_mid, text="Save", command=self.save_page)
        self.save_button.pack()

    def save_page(self):
        self.page = self.entry_mid.get()
        print(f"Page value saved: {self.page}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
