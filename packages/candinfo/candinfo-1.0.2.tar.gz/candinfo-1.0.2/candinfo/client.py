import requests
import xmltodict
import json


class Candidate:
    def __init__(self, key):
        self.key = key
        self.BASE_URL = "http://apis.data.go.kr/9760000/PofelcddInfoInqireService/getPoelpcddRegistSttusInfoInqire?serviceKey={0}".format(
            key
        )

    def checkKey(self):
        return self.key

    def findCandidate(self, id, code, sggname="", sdname="", page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}&pageNo={page}&numOfRows={number}&sgId={id}&sgTypecode={code}&sggName={sggname}&sdName={sdname}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["body"]["items"]["item"]
        except:
            return jsonData["result"]

    def serverStatus(self, id, code, sggname="", sdname="", page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}&pageNo={page}&numOfRows={number}&sgId={id}&sgTypecode={code}&sggName={sggname}&sdName={sdname}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["header"]
        except:
            return jsonData["result"]

    def candiCount(self, id, code, sggname="", sdname="", page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}&pageNo={page}&numOfRows={number}&sgId={id}&sgTypecode={code}&sggName={sggname}&sdName={sdname}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["body"]["totalCount"]
        except:
            return jsonData["result"]


class Code:
    def __init__(self, key):
        self.key = key
        self.BASE_URL = "http://apis.data.go.kr/9760000/CommonCodeService"

    def jobCode(self, id, page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}/getCommonJobCodeList?serviceKey={self.key}&pageNo={page}&numOfRows={number}&sgId={id}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["body"]["items"]["item"]
        except:
            return jsonData["result"]

    def eduCode(self, id, page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}/getCommonEduBckgrdCodeList?serviceKey={self.key}&pageNo={page}&numOfRows={number}&sgId={id}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["body"]["items"]["item"]
        except:
            return jsonData["result"]

    def sgCode(self, page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}/getCommonSgCodeList?serviceKey={self.key}&pageNo={page}&numOfRows={number}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["body"]["items"]["item"]
        except:
            return jsonData["result"]

    def gusigunCode(self, id, sdName, page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}/getCommonGusigunCodeList?serviceKey={self.key}&pageNo={page}&numOfRows={number}&sgId={id}&sdName={sdName}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["body"]["items"]["item"]
        except:
            return jsonData["result"]

    def sggCode(self, id, code, page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}/getCommonSggCodeList?serviceKey={self.key}&pageNo={page}&numOfRows={number}&sgId={id}&sgTypecode={code}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["body"]["items"]["item"]
        except:
            return jsonData["result"]

    def partyCode(self, id, page="1", number="999"):
        try:
            response = requests.get(
                f"{self.BASE_URL}/getCommonPartyCodeList?serviceKey={self.key}&pageNo={page}&numOfRows={number}&sgId={id}"
            ).text
            jsonData = json.loads(json.dumps(xmltodict.parse(response)))
            return jsonData["response"]["body"]["items"]["item"]
        except:
            return jsonData["result"]
