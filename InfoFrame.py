from tkinter import *
from xmlRead import xmlRead
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
import webbrowser
from Map import Map
import os
import pickle
from msg import msg

Facilities = ['restaurant', 'cafe', 'store', 'nolibang', 'suyu', 'parkbarrier',
              'restbarrier', 'runwbarrier', 'elevbarrier', 'parkinglot']


class InfoFrame(Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)

        self.favorites = {}
        self.favorite_datas = {}
        self.in_favorite = False

        if not os.path.exists('favorites.txt'):
            f = open('favorites.txt', 'wb')
            pickle.dump(self.favorites, f)
            f.close()
        else:
            f = open('favorites.txt', 'rb')
            self.favorites = pickle.load(f)
            f.close()

        self.sub_frame1 = Frame(self)
        self.sub_frame1.grid(row=0, column=0, sticky="nsew")

        self.email_image = PhotoImage(file="image/email.png")
        self.email_button = Button(self.sub_frame1, image=self.email_image, command=self.sendEmail)
        self.email_button.grid(row=0, column=0, sticky="nsew")

        self.sub_frame2 = Frame(self)
        self.sub_frame2.grid(row=1, column=0, sticky="nsew")

        self.informations = []
        self.information = Canvas(self.sub_frame2, bg='white')
        self.information.grid(row=0, column=0, sticky="nsew")

        self.information_xscroll = Scrollbar(self.information, orient='horizontal', command=self.information.xview)
        self.information_xscroll.pack(side="bottom", fill=X)
        self.information_yscroll = Scrollbar(self.information, orient='vertical', command=self.information.yview)
        self.information_yscroll.pack(side="right", fill=Y)
        self.information.configure(xscrollcommand=self.information_xscroll.set, yscrollcommand=self.information_yscroll.set)

        self.sub_frame3 = Frame(self, bg='white')
        self.sub_frame3.grid(row=2, column=0, sticky="nsew")

        self.grid_propagate_configure()

    def is_in_favorite(self, id):
        f = open('favorites.txt', 'rb')
        self.favorites = pickle.load(f)
        f.close()

        if id in self.favorites.keys():
            self.in_favorite = True
            return True
        else:
            self.in_favorite = False
            return False

    def sendEmail(self):
        pass

    def addRemoveFavorite(self, id):
        if not id:
            return False

        if self.is_in_favorite(id):
            self.removeFavorite(id)
        else:
            self.addFavorite(id)

    def addFavorite(self, id):
        f = open('favorites.txt', 'wb')
        self.favorites[id] = self.favorite_datas
        pickle.dump(self.favorites, f)
        f.close()

        self.favorite_image = PhotoImage(file="image/removefavorite.png")
        self.favorite_button.configure(image=self.favorite_image)

    def removeFavorite(self, id):
        f = open('favorites.txt', 'wb')
        del self.favorites[id]
        pickle.dump(self.favorites, f)
        f.close()

        self.favorite_image = PhotoImage(file="image/addfavorite.png")
        self.favorite_button.configure(image=self.favorite_image)

    def grid_propagate_configure(self):
        super().grid_rowconfigure(0, weight=1)
        super().grid_rowconfigure(1, weight=9)
        super().grid_rowconfigure(2, weight=3)
        super().grid_columnconfigure(0, weight=1)

        self.sub_frame1.grid_propagate(False)
        self.sub_frame1.grid_rowconfigure(0, weight=1)
        self.sub_frame1.grid_columnconfigure(0, weight=1)
        self.sub_frame1.grid_columnconfigure(1, weight=1)
        self.sub_frame1.grid_columnconfigure(2, weight=1)

        self.sub_frame2.grid_propagate(False)
        self.sub_frame2.grid_rowconfigure(0, weight=1)
        self.sub_frame2.grid_columnconfigure(0, weight=2)

        self.sub_frame3.grid_propagate(False)
        self.sub_frame3.grid_rowconfigure(0, weight=1)
        self.sub_frame3.grid_columnconfigure(0, weight=1)

    def get_favorite_dats(self):
        return self.favorites


class ShowInfoFrame(InfoFrame):
    fields = {'mt20id': '공연 ID',
              'prfnm': '공연명',
              'prfpdfrom': '공연 시작일',
              'prfpdto': '공연 종료일',
              'fcltynm': '공연시설명',
              'prfcast': '공연 출연진',
              'prfcrew': '공연 제작진',
              'prfruntime': '공연 런타임',
              'prfage': '공연 관람 연령',
              'entrpsnm': '기획제작사',
              'entrpsnmP': '제작사',
              'entrpsnmA': '기획사',
              'entrpsnmH': '주최',
              'entrpsnmS': '주관',
              'pcseguidance': '티켓 가격',
              'sty': '줄거리',
              'area': '지역',
              'genrenm': '장르',
              'openrun': '오픈런',
              'visit': '내한',
              'child': '아동',
              'daehakro': '대학로',
              'festival': '축제',
              'musicallicense': '뮤지컬 라이센스',
              'musicalcreate': '뮤지컬 창작',
              'updatedate': '최종 수정일',
              'prfstate': '공연 상태',
              'mt10id': '공연시설 ID',
              'dtguidance': '공연 시간'
              }

    def __init__(self, parent):
        super().__init__(parent)

        self.show_id = None
        self.place_id = None
        self.data = None

        self.favorite_image = PhotoImage(file='image/favorite.png')
        self.favorite_data_fields = ['mt20id', 'prfnm', 'genrenm', 'prfstate', 'poster', 'fcltynm']
        self.favorite_button = Button(self.sub_frame1, image=self.favorite_image, command=lambda: self.addRemoveFavorite(self.show_id))
        self.favorite_button.grid(row=0, column=1, sticky="nsew")

        self.place_image = PhotoImage(file='image/map.png')
        self.place_button = Button(self.sub_frame1, image=self.place_image, command=self.showPlaceInfo)
        self.place_button.grid(row=0, column=2, sticky="nsew")

        self.poster_refs = []
        self.poster = Canvas(self.sub_frame2)
        self.poster.grid_propagate(False)
        self.poster.grid(row=0, column=1, sticky="nsew")
        self.poster.bind('<Configure>', self.on_resize)

        self.poster_yscroll = Scrollbar(self.poster, orient='vertical', command=self.poster.yview)
        self.poster_yscroll.pack(side="right", fill=Y)
        self.poster.configure(yscrollcommand=self.poster_yscroll.set)

        self.sub_frame2.grid_columnconfigure(1, weight=1)
        self.sub_frame3.grid_columnconfigure(1, weight=9)

        self.urls = []

    def sendEmail(self):
        if self.data:
            message = msg('공연 '+self.data['prfnm']+' 상세 정보')

            msgtext = ''
            msgtext += (ShowInfoFrame.fields['mt20id'] + ' : ' + self.data['mt20id'] + '<br>')
            msgtext += (ShowInfoFrame.fields['mt10id'] + ' : ' + self.data['mt10id'] + '<br><br>')
            msgtext += (ShowInfoFrame.fields['genrenm'] + ' : ' + self.data['genrenm'] + '<br>')
            msgtext += (ShowInfoFrame.fields['prfstate'] + ' : ' + self.data['prfstate'] + '<br><br>')
            msgtext += (ShowInfoFrame.fields['fcltynm'] + ' : ' + self.data['fcltynm'] + '<br>')
            msgtext += (ShowInfoFrame.fields['prfruntime'] + ' : ' + self.data['prfruntime'] + '<br>')
            msgtext += (ShowInfoFrame.fields['prfage'] + ' : ' + self.data['prfage'] + '<br><br>')
            msgtext += (ShowInfoFrame.fields['prfpdfrom'] + ' : ' + self.data['prfpdfrom'] + '<br>')
            msgtext += (ShowInfoFrame.fields['prfpdto'] + ' : ' + self.data['prfpdto'] + '<br><br>')
            for d in self.data['relates']:
                msgtext += (d['relatenm'] + ' : ' + d['relateurl'] + '<br>')

            message.attach_show_details(self.data['prfnm'], msgtext, self.data['poster'])

            message.send()

    def getInfo(self):
        self.place_id = None
        self.informations.clear()
        self.poster_refs.clear()
        self.urls.clear()

        fetcher = xmlRead()
        self.data = fetcher.fetch_and_parse_show_detail_data(self.show_id)[0]
        self.images = []

        for k, v in self.data.items():
            if k == 'styurls':
                for url in v:
                    with urllib.request.urlopen(url) as u:
                        raw_data = u.read()
                    im = Image.open(BytesIO(raw_data))
                    self.images.append(im)
                    im = im.resize((self.poster.winfo_width() - 19, (self.poster.winfo_width() - 19) * im.height // im.width))
                    image = ImageTk.PhotoImage(im)

                    self.poster_refs.append(image)
            elif k == 'relates':
                for url in v:
                    self.urls.append(
                        (Label(self.sub_frame3, text=url['relatenm']),
                         Label(self.sub_frame3, text=url['relateurl'], fg='blue')))
            else:
                if k == 'mt10id':
                    self.place_id = v
                if k in self.favorite_data_fields:
                    self.favorite_datas[k] = v
                if k != 'poster' and v != ' ':
                    self.informations.append(ShowInfoFrame.fields[k] + ' : ' + str(v))

    def setInfo(self, id):
        self.information.delete("all")
        self.poster.delete("all")

        self.show_id = id
        self.getInfo()

        if self.is_in_favorite(self.show_id):
            self.favorite_image = PhotoImage(file="image/removefavorite.png")
            self.favorite_button.configure(image=self.favorite_image)
        else:
            self.favorite_image = PhotoImage(file="image/addfavorite.png")
            self.favorite_button.configure(image=self.favorite_image)

        h = 0
        for i in range(len(self.informations)):
            if '\n' in self.informations[i]:
                h += 1
                informations = self.informations[i].split('\n')
                for information in informations:
                    if information != '\r':
                        self.information.create_text(5, 25 * (i + h + 1), anchor=W, text=information, font=('arial', 10, 'bold'))
                        h += 1
            else:
                self.information.create_text(5, 25 * (i + h + 1), anchor=W, text=self.informations[i], font=('arial', 10, 'bold'))
        self.information.config(scrollregion=self.information.bbox(ALL))

        r = 0
        for t in self.urls:
            t[0].grid(row=r, column=0, padx=2, pady=2, sticky='nsew')
            t[1].grid(row=r, column=1, padx=2, pady=2, sticky='nsew')
            t[1].bind("<Button-1>", self.open_url(t[1].cget('text')))
            self.sub_frame3.grid_rowconfigure(r, weight=1)
            r += 1

    def on_resize(self, event):
        if not self.data:
            return

        self.poster.delete("all")
        self.poster_refs.clear()

        loc = 0
        for image in self.images:
            im = image.resize((self.poster.winfo_width() - 19, (self.poster.winfo_width() - 19) * image.height // image.width))
            image = ImageTk.PhotoImage(im)
            self.poster.create_image(0, loc, anchor=NW, image=image)
            self.poster_refs.append(image)
            loc += (self.poster.winfo_width() - 19) * image.height() // image.width()
        self.poster.config(scrollregion=self.poster.bbox(ALL))

    def open_url(self, url):
        def callback(event):
            webbrowser.open_new(url)

        return callback

    def showPlaceInfo(self):
        if self.place_id:
            place_info_frame = Toplevel()
            place_info_frame.geometry("800x700")
            place_info_frame.title("공연 장소 정보")

            place_info_frame.grid_rowconfigure(0, weight=1)
            place_info_frame.grid_columnconfigure(0, weight=1)

            place_info = PlaceInfoFrame(place_info_frame)
            place_info.email_button.configure(bg=self.email_button['bg'])
            place_info.favorite_button.configure(bg=self.email_button['bg'])
            place_info.toggle_button.configure(bg=self.email_button['bg'])
            place_info.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
            place_info.setInfo(self.place_id)


class PlaceInfoFrame(InfoFrame):
    fields = {
        'fcltynm': '공연시설명',
        'mt10id': '공연시설 ID',
        'mt13cnt': '공연장 수',
        'fcltychartr': '시설 특성',
        'opende': '개관연도',
        'seatscale': '객석 수',
        'telno': '전화번호',
        'relateurl': '홈페이지',
        'adres': '주소',
        'la': '위도',
        'lo': '경도',
        'prfplcnm': '공연장명',
        'mt13id': '고유식별 ID',
        'seatscale': '좌석 규모',
        'stageorchat': '무대시설_오케스트라피트',
        'stagepracat': '무대시설_연습실',
        'stagedresat': '무대시설_분장실',
        'stageoutdrat': '무대시설_야외공연장',
        'disabledseatscale': '장애인시설_관객석',
        'stagearea': '무대시설_무대넓이'
    }

    def __init__(self, parent):
        super().__init__(parent)

        self.place_id = None
        self.status = True  # True : 공연 장소 정보, False : 편의 시설 정보
        self.data = None
        self.favorite_image = None
        self.favorite_data_fields = ['fcltynm', 'adres']
        self.facility_image = {
            'restaurant': PhotoImage(file="image/restaurant.png"),
            'cafe': PhotoImage(file="image/cafe.png"),
            'store': PhotoImage(file="image/store.png"),
            'nolibang': PhotoImage(file="image/nolibang.png"),
            'suyu': PhotoImage(file="image/suyu.png"),
            'parkinglot': PhotoImage(file="image/parkinglot.png"),
            'parkbarrier': PhotoImage(file="image/parkbarrier.png"),
            'restbarrier': PhotoImage(file="image/restbarrier.png"),
            'elevbarrier': PhotoImage(file="image/elevbarrier.png")
        }
        self.map = Map()

        self.favorite_image = PhotoImage(file='image/favorite.png')
        self.favorite_button = Button(self.sub_frame1, image=self.favorite_image, command=lambda: self.addRemoveFavorite(self.place_id))
        self.favorite_button.grid(row=0, column=1, sticky="nsew")

        self.toggle_image = PhotoImage(file='image/information.png')
        self.toggle_button = Button(self.sub_frame1, image=self.toggle_image, command=self.toggleInfo)
        self.toggle_button.grid(row=0, column=2, sticky="nsew")

    def sendEmail(self):

        if self.data:
            message = msg(self.data['fcltynm']+' 상세 정보')

            msgtext = ''
            msgtext += (PlaceInfoFrame.fields['mt10id'] + ' : ' + self.data['mt10id'] + '<br><br>')
            msgtext += (PlaceInfoFrame.fields['fcltychartr'] + ' : ' + self.data['fcltychartr'] + '<br><br>')
            msgtext += (PlaceInfoFrame.fields['adres'] + ' : ' + self.data['adres'] + '<br><br>')
            msgtext += ('레스토랑 : ' + self.data['restaurant'] + '<br>')
            msgtext += ('카페 : ' + self.data['cafe'] + '<br>')
            msgtext += ('놀이방 : ' + self.data['nolibang'] + '<br>')
            msgtext += ('수유실 : ' + self.data['suyu'] + '<br>')
            msgtext += ('주차장 : ' + self.data['parkinglot'] + '<br>')
            msgtext += ('장애인 주차장 : ' + self.data['parkbarrier'] + '<br>')
            msgtext += ('장애인 화장실 : ' + self.data['restbarrier'] + '<br>')
            msgtext += ('장애인 엘리베이터 : ' + self.data['elevbarrier'] + '<br><br>')
            msgtext += (PlaceInfoFrame.fields['relateurl'] + ' : ' + self.data['relateurl'] + '<br>')

            message.attach_place_details(self.data['fcltynm'], msgtext)

            message.send()

    def getInfo(self):
        self.informations.clear()

        fetcher = xmlRead()
        self.data = fetcher.fetch_and_parse_place_data(self.place_id)[0]

        for k, v in self.data.items():
            if k == 'la':
                self.latitude = v
                continue
            elif k == 'lo':
                self.longitude = v
                continue
            elif k in self.favorite_data_fields:
                self.favorite_datas[k] = v

            if self.status:
                if k not in Facilities and v != ' ':
                    if k == 'mt13s':
                        for mt13d in v:
                            for mt13k, mt13v in mt13d.items():
                                if mt13v != ' ':
                                    self.informations.append(PlaceInfoFrame.fields[mt13k] + ' : ' + mt13v)
                    else:
                        self.informations.append(PlaceInfoFrame.fields[k] + ' : ' + v)
            else:
                if k in Facilities and v != 'N':
                    self.informations.append(k)

    def setInfo(self, id):
        self.information.delete('all')

        self.place_id = id
        self.getInfo()

        if self.is_in_favorite(self.place_id):
            self.favorite_image = PhotoImage(file="image/removefavorite.png")
            self.favorite_button.configure(image=self.favorite_image)
        else:
            self.favorite_image = PhotoImage(file="image/addfavorite.png")
            self.favorite_button.configure(image=self.favorite_image)

        h = 0
        if self.status:
            for i in range(len(self.informations)):
                if '공연장명' in self.informations[i]:
                    h += 1
                self.information.create_text(5, 25 * (i + h + 1), anchor=W, text=self.informations[i], font=('arial', 10, 'bold'))
            self.information.config(scrollregion=self.information.bbox(ALL))
            self.toggle_image = PhotoImage(file="image/information.png")
            self.toggle_button.configure(image=self.toggle_image)
        else:
            self.drawStatistics()
            self.information.config(scrollregion=self.information.bbox(ALL))
            self.toggle_image = PhotoImage(file="image/map.png")
            self.toggle_button.configure(image=self.toggle_image)

        if self.map.get_coordinate() != (self.latitude, self.longitude):
            self.map.show_map(self.sub_frame3, self.latitude, self.longitude)

    def toggleInfo(self):
        if not self.place_id:
            return

        self.status = not self.status

        self.setInfo(self.place_id)

    def drawStatistics(self):
        self.information.create_line(50, self.information.winfo_height() - 70,
                                     self.information.winfo_width() - 50, self.information.winfo_height() - 70)
        self.information.create_line(50, self.information.winfo_height() - 70, 50, 50)

        col = 1
        gap = (self.information.winfo_width() - 100) // len(self.facility_image)
        for k, v in self.facility_image.items():
            self.information.create_image(20 + col * gap, self.information.winfo_height() - 35, image=v)
            if k in self.informations:
                self.information.create_rectangle(5 + col * gap, 120,
                                                  35 + col * gap, self.information.winfo_height() - 70,
                                                  fill='blue')
            col += 1
