import requests
import xml.etree.ElementTree as ET


class xmlRead:
    def __init__(self):
        self.api_key = '7c1a4e6d58d34c01b1aeacb1b685df78'
        self.base_url = "http://www.kopis.or.kr/openApi/restful/"

    def fetch_and_parse_show_data(self, stdate, eddate, rows, cpage):
        # URL 구성
        url = f"{self.base_url}pblprfr?service={self.api_key}&stdate={stdate}&eddate={eddate}&rows={rows}&cpage={cpage}&newsql=Y"
        # 데이터 요청
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.text
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

        # XML 파싱 시작
        root = ET.fromstring(xml_data)

        # 얻은 DB를 저장할 리스트
        performances = []
        for db_elem in root.findall('.//db'):
            performance_info = {
                "mt20id": db_elem.findtext("mt20id"),  # 공연 ID
                "prfnm": db_elem.findtext("prfnm"),  # 공연명
                "genrenm": db_elem.findtext("genrenm"),  # 장르명
                "prfstate": db_elem.findtext("prfstate"),  # 공연 상태
                "prfpdfrom": db_elem.findtext("prfpdfrom"),  # 공연 시작일
                "prfpdto": db_elem.findtext("prfpdto"),  # 공연 종료일
                "poster": db_elem.findtext("poster"),  # 공연 포스터 경로
                "fcltynm": db_elem.findtext("fcltynm"),  # 공연 시설명
                "openrun": db_elem.findtext("openrun"),  # 오픈런 여부
            }
            performances.append(performance_info)
        return performances

    def fetch_and_parse_place_data(self, mt10id, newsql='Y'):
        # URL 구성
        url = f"{self.base_url}prfplc/{mt10id}?service={self.api_key}&newsql={newsql}"
        # 데이터 요청
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.text
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

        # XML 파싱 시작
        root = ET.fromstring(xml_data)

        # 얻은 DB를 저장할 리스트
        performances = []
        for db_elem in root.findall('.//db'):
            performance_info = {
                "fcltynm": db_elem.findtext("fcltynm"),  # 공연 시설명
                "fcltynm": db_elem.findtext("fcltynm"),
                "mt10id": db_elem.findtext("mt10id"),
                "mt13cnt": db_elem.findtext("mt13cnt"),
                "fcltychartr": db_elem.findtext("fcltychartr"),
                "opende": db_elem.findtext("opende"),
                "seatscale": db_elem.findtext("seatscale"),
                "telno": db_elem.findtext("telno"),
                "relateurl": db_elem.findtext("relateurl"),
                "adres": db_elem.findtext("adres"),
                "la": db_elem.findtext("la"),
                "lo": db_elem.findtext("lo"),
                "restaurant": db_elem.findtext("restaurant"),
                "cafe": db_elem.findtext("cafe"),
                "store": db_elem.findtext("store"),
                "nolibang": db_elem.findtext("nolibang"),
                "suyu": db_elem.findtext("suyu"),
                "parkbarrier": db_elem.findtext("parkbarrier"),
                "restbarrier": db_elem.findtext("restbarrier"),
                "runwbarrier": db_elem.findtext("runwbarrier"),
                "elevbarrier": db_elem.findtext("elevbarrier"),
                "parkinglot": db_elem.findtext("parkinglot"),
                "prfplcnm": db_elem.findtext("prfplcnm"),
                "mt13id": db_elem.findtext("mt13id"),
                "seatscale": db_elem.findtext("seatscale"),
                "stageorchat": db_elem.findtext("stageorchat"),
                "stagepracat": db_elem.findtext("stagepracat"),
                "stagedresat": db_elem.findtext("stagedresat"),
                "stageoutdrat": db_elem.findtext("stageoutdrat"),
                "disabledseatscale": db_elem.findtext("disabledseatscale"),
                "stagearea": db_elem.findtext("stagearea")
            }
            performances.append(performance_info)
        return performances

    def fetch_and_parse_show_detail_data(self, mt20id):
        # URL 구성
        url = f"{self.base_url}pblprfr/{mt20id}?service={self.api_key}&newsql=Y"

        # 데이터 요청
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.text
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

        # XML 파싱 시작
        root = ET.fromstring(xml_data)

        # 얻은 DB를 저장할 리스트
        performances = []
        for db_elem in root.findall('.//db'):
            # 공연 정보 저장
            performance_info = {
                "mt20id": db_elem.findtext('mt20id'),
                "prfnm": db_elem.findtext('prfnm'),
                "prfpdfrom": db_elem.findtext('prfpdfrom'),
                "prfpdto": db_elem.findtext('prfpdto'),
                "fcltynm": db_elem.findtext('fcltynm'),
                "prfcast": db_elem.findtext('prfcast'),
                "prfcrew": db_elem.findtext('prfcrew'),
                "prfruntime": db_elem.findtext('prfruntime'),
                "prfage": db_elem.findtext('prfage'),
                "entrpsnm": db_elem.findtext('entrpsnm'),
                "entrpsnmP": db_elem.findtext('entrpsnmP'),
                "entrpsnmA": db_elem.findtext('entrpsnmA'),
                "entrpsnmH": db_elem.findtext('entrpsnmH'),
                "entrpsnmS": db_elem.findtext('entrpsnmS'),
                "pcseguidance": db_elem.findtext('pcseguidance'),
                "poster": db_elem.findtext('poster'),
                "sty": db_elem.findtext('sty'),
                "area": db_elem.findtext('area'),
                "genrenm": db_elem.findtext('genrenm'),
                "openrun": db_elem.findtext('openrun'),
                "visit": db_elem.findtext('visit'),
                "child": db_elem.findtext('child'),
                "daehakro": db_elem.findtext('daehakro'),
                "festival": db_elem.findtext('festival'),
                "musicallicense": db_elem.findtext('musicallicense'),
                "musicalcreate": db_elem.findtext('musicalcreate'),
                "updatedate": db_elem.findtext('updatedate'),
                "prfstate": db_elem.findtext('prfstate'),
                "styurls": [img.text for img in db_elem.findall('styurls/styurl')],
                "mt10id": db_elem.findtext('mt10id'),
                "dtguidance": db_elem.findtext('dtguidance'),
                "relates": [
                    {
                        "relatenm": relate.findtext('relatenm') if relate.find('relatenm') is not None else '',
                        "relateurl": relate.findtext('relateurl') if relate.find('relateurl') is not None else ''
                    }
                    for relate in db_elem.findall('.//relate')
                ]
            }
            performances.append(performance_info)
        return performances

# fetcher = xmlRead()
# performances = fetcher.fetch_and_parse_show_data(stdate='20250101', eddate='20250102', rows=10000, cpage=1)
# places = fetcher.fetch_and_parse_place_data(mt10id='FC001431')
# details = fetcher.fetch_and_parse_show_detail_data("PF132236")
