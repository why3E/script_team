from tkinter import *

def clicked():
    print("Button Clicked!")

root = Tk()
root.title("원 모양의 버튼")

canvas = Canvas(root, width=200, height=200, bg='white')
canvas.pack()

button = canvas.create_oval(50, 50, 150, 150, fill="blue", outline="black", width=2)
text = canvas.create_text(100, 100, text="Click Me", fill="white", font=("Helvetica", 12))

# 원 모양 버튼에 클릭 이벤트 바인딩
canvas.tag_bind(button, "<Button-1>", lambda event: clicked())

root.mainloop()
