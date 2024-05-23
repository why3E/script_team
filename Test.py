import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO

# URL에서 이미지를 다운로드하는 함수
def load_image_from_url(url):
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    image = Image.open(BytesIO(raw_data))
    return image

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("Canvas with Frames")

# 캔버스 생성
canvas = tk.Canvas(root, width=800, height=600,bg='yellow')
canvas.pack(fill=tk.BOTH, expand=True)

# 프레임 생성 및 캔버스에 배치
frame1 = ttk.Frame(canvas, width=400, height=300, relief=tk.RAISED, borderwidth=2)
frame2 = ttk.Frame(canvas, width=400, height=300, relief=tk.RAISED, borderwidth=2)

# 프레임1 배치
canvas.create_window((200, 150), window=frame1, anchor=tk.CENTER)
# 프레임2 배치
canvas.create_window((600, 450), window=frame2, anchor=tk.CENTER)

# 이미지 URL
url = "http://www.kopis.or.kr/upload/pfmPoster/PF_PF233234_240102_103045.jpg"

# 이미지 로드
image = load_image_from_url(url)

# 이미지 크기를 조정 (필요한 경우)
image = image.resize((200, 300), Image.LANCZOS)

# 이미지 변환
photo = ImageTk.PhotoImage(image)

# 프레임1에 라벨과 이미지 넣기
label1 = ttk.Label(frame1, text="Frame 1")
label1.pack(pady=10)
image_label1 = ttk.Label(frame1, image=photo)
image_label1.image = photo  # 이 줄이 없으면 이미지가 가비지 컬렉션에 의해 삭제됨
image_label1.pack()

# 프레임2에 다른 라벨 넣기
label2 = ttk.Label(frame2, text="Frame 2")
label2.pack(pady=10)

# Tkinter 메인 루프 시작
root.mainloop()
