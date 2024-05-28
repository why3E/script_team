# http://www.kopis.or.kr/openApi/restful/pblprfr/PF132236?service={SeriveKey}&newsql=Y

# 인증 키 : 6ecd0d874783499b86ad42078f5d7ff9

from urllib.request import urlopen

url = 'http://www.kopis.or.kr/openApi/restful/pblprfr/PF132236?service=6ecd0d874783499b86ad42078f5d7ff9&newsql=Y'

res_body = urlopen(url).read()

print(res_body.decode('utf-8'))