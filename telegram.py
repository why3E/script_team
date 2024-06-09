import sys
import telepot
import traceback
from InfoFrame import *
import xmlRead

TOKEN = '7278767188:AAE0SRryTZMFa30KhYDBags0uUtfGw4YPNE'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

class Telegram:
    def __init__(self):
        bot = telepot.Bot(TOKEN)
        bot.message_loop(self.handle)

    def sendMessage(self, user, msg):
        try:
            bot.sendMessage(user, msg)
        except:
            traceback.print_exc(file=sys.stdout)


    def replyAptData(self, date_param, user, args):
        msg = ''

        fetcher = xmlRead.xmlRead()

        if date_param == 'date':
            res_list = fetcher.fetch_and_parse_show_data(stdate=args[0], eddate=args[1], rows=10, cpage=1)

            for d in res_list:
                msg = ''

                msg += ('공연 ID : ' + d['mt20id'] + '\n')
                msg += ('공연명 : ' + d['prfnm'] + '\n\n')
                msg += ('장르 : ' + d['genrenm'] + '\n')
                msg += ('공연 상태 : ' + d['prfstate'] + '\n\n')
                msg += ('포스터 : ' + d['poster'] + '\n')

                self.sendMessage(user, msg)
        elif date_param == 'mt20id':
            res_list = fetcher.fetch_and_parse_show_detail_data(mt20id=args)

            msg += (ShowInfoFrame.fields['mt20id'] + ' : ' + res_list[0]['mt20id'] + '\n')
            msg += (ShowInfoFrame.fields['mt10id'] + ' : ' + res_list[0]['mt10id'] + '\n\n')
            msg += (ShowInfoFrame.fields['genrenm'] + ' : ' + res_list[0]['genrenm'] + '\n')
            msg += (ShowInfoFrame.fields['prfstate'] + ' : ' + res_list[0]['prfstate'] + '\n\n')
            msg += (ShowInfoFrame.fields['fcltynm'] + ' : ' + res_list[0]['fcltynm'] + '\n')
            msg += (ShowInfoFrame.fields['prfruntime'] + ' : ' + res_list[0]['prfruntime'] + '\n')
            msg += (ShowInfoFrame.fields['prfage'] + ' : ' + res_list[0]['prfage'] + '\n\n')
            msg += (ShowInfoFrame.fields['prfpdfrom'] + ' : ' + res_list[0]['prfpdfrom'] + '\n')
            msg += (ShowInfoFrame.fields['prfpdto'] + ' : ' + res_list[0]['prfpdto'] + '\n\n')
            msg += ('포스터 : ' + res_list[0]['poster'] + '\n\n')
            for d in res_list[0]['relates']:
                msg += (d['relatenm'] + ' : ' + d['relateurl'] + '\n')

            self.sendMessage(user, msg)
        elif date_param == 'mt10id':
            res_list = fetcher.fetch_and_parse_place_data(mt10id=args)

            msg += (PlaceInfoFrame.fields['mt10id'] + ' : ' + res_list[0]['mt10id'] + '\n\n')
            msg += (PlaceInfoFrame.fields['fcltychartr'] + ' : ' + res_list[0]['fcltychartr'] + '\n\n')
            msg += (PlaceInfoFrame.fields['adres'] + ' : ' + res_list[0]['adres'] + '\n\n')
            msg += (PlaceInfoFrame.fields['relateurl'] + ' : ' + res_list[0]['relateurl'] + '\n')

            self.sendMessage(user, msg)


    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            self.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')

        if text.startswith('기간') and len(args) > 1:
            self.replyAptData('date', chat_id, (args[1], args[2]))
        elif text.startswith('공연시설') and len(args) > 1:
            self.replyAptData('mt10id', chat_id, args[1])
        elif text.startswith('공연') and len(args) > 1:
            self.replyAptData('mt20id', chat_id, args[1])
        else:
            self.sendMessage(chat_id, '모르는 명령어입니다.\n기간 [기간], 공연 [공연ID], 공연시설 [공연시설ID] 중 하나의 명령을 입력하세요.')
