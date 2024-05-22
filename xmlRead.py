import requests
import xml.etree.ElementTree as ET


class xmlRead:
    def __init__(self):
        self.api_key = '7c1a4e6d58d34c01b1aeacb1b685df78'
        self.base_url = "http://www.kopis.or.kr/openApi/restful/pblprfr"

    def fetch_and_parse_data(self, stdate, eddate, rows, cpage):
        # URL 구성
        url = f"{self.base_url}?service={self.api_key}&stdate={stdate}&eddate={eddate}&rows={rows}&cpage={cpage}"
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


fetcher = xmlRead()

performances = fetcher.fetch_and_parse_data(stdate='20250101', eddate='20250102', rows=10000, cpage=1)

print(len(performances))
