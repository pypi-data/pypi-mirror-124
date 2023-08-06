# 
# from naver import *
# import requests
# import json
#
# class Romanizer:
#     """한글인명-로마자 변환"""
#     def __init__(self):
#         self.tblname = 'Hangul_romanization'
#         self.name = None
#         self.url = "https://openapi.naver.com/v1/krdict/romanization"
#         self.headers = {
#             'Host':'openapi.naver.com',
#             'User-Agent':'curl/7.49.1',
#             'Accept':'*/*',
#             'X-Naver-Client-Id': os.environ.get('NAVER_CLIENT_ID'),
#             'X-Naver-Client-Secret': os.environ.get('NAVER_CLIENT_SECRET'),
#         }
#
#     def romanize(self, name):
#         self.name = name
#         res = requests.get(url= self.url + f"?query={name}", headers=self.headers)
#         self.res = res
#         if res.status_code == 200:
#             jsdata = json.loads(res.text)
#             df = pd.DataFrame(jsdata['aResult'])
#             df = df.assign(input_name= name)
#             self.InsertManyResult = db[self.tblname].insert_many(df.to_dict('records'))
#         else:
#             print('\n\n dbg.res')
#
#     def find_name(self, name=None):
#         name = self.name if name is None else name
#         self.cursor = db[self.tblname].find(filter={'input_name':name})
#         return list(self.cursor)
#
#     def find_all(self):
#         self.cursor = db[self.tblname].find()
#         return list(self.cursor)
