# -*- coding: utf-8 -*-
"""
Request.
= = = = = Collector Rules = = = = =
입력한 조회기간(연도들)을 '연초일~연말일' 식으로 강제설정한다.
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import json
import os
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================ External-Library.
import requests
# ============================================================ My-Library.
import idebug as dbg
import eproxy
# ============================================================ Project.
# ============================================================ Constant.
TIMEOUT = 10


# ============================================================
"""Models."""
# ============================================================
class Request:
    """
    OTP-Code가 없을 경우, 더이상 작업을 진행하지 않는다. 리턴된 빈 데이터는 저장할 가치도 없다.
    """
    def __init__(self):
        self.headers = _headers_()
        self.set_proxies()
    def set_proxies(self, rand=True, protocol='HTTP'):
        try:
            proxyON = bool(int(os.environ['NAVER_PROXY']))
        except Exception as e:
            proxyON = True
        finally:
            # print(f"proxyON : {proxyON}")
            if proxyON:
                self.Proxy = eproxy.Proxy().setup(rand=rand, protocol='HTTP', port={'$ne':443}, alive=True)
                self.proxies = self.Proxy.next()
            else:
                self.proxies = None
            return self
    def next_proxies(self):
        self.proxies = self.Proxy.next()
        return self
    def post(self, url, form, **kw):
        while True:
            data = post(url, form, proxies=self.proxies, **kw)
            if self.proxies is None:
                break
            elif data is None:
                self.next_proxies()
            else:
                break
        return data
    def get(self, url, **kw):
        return get(url, proxies=self.proxies, **kw)
# ============================================================
"""GenFunctions."""
# ============================================================
def _headers_():
    h = { 'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,es;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': None,
        'DNT': '1',
        'Host': 'marketdata.krx.co.kr',
        'Referer': 'http://marketdata.krx.co.kr/mdi',
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'X-Requested-With': 'XMLHttpRequest'}
    """Update Cookie."""
    h.update({'Cookie': '__utma=139639017.1350543225.1569547430.1569547430.1569547430.1; __utmc=139639017; __utmz=139639017.1569547430.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=139639017.1.10.1569547430; JSESSIONID=379F3578E253019FFEEB7EBEA3DF71D9.103tomcat1; WMONID=5x_O32k4ksC; __utma=70557324.1111960620.1569547469.1569547469.1569547469.1; __utmc=70557324; __utmz=70557324.1569547469.1.1.utmcsr=krx.co.kr|utmccn=(referral)|utmcmd=referral|utmcct=/main/main.jsp; __utmb=70557324.2.10.1569547469'})
    return h

@dbg.fruntime
def get(url, **kw):
    try:
        r = requests.get(url, **kw)
    except Exception as e:
        dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
    else:
        try:
            return r.text
        except Exception as e:
            dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
            dbg.clsattrs(r)

@dbg.fruntime
def post(url, form, **kw):
    """
    post 용 timeout 은 수동으로 하지말고, 각 서비스별로 과거경험을 분석해서 최적의 값을 찾아낸 뒤, 프로그램이 자동으로 설정하도록 만들자.
    """
    # pp.pprint(locals())
    try:
        if 'timeout' not in list(kw):
            kw['timeout'] = TIMEOUT
        r = requests.post(url, data=form, headers=_headers_(), **kw)
    except Exception as e:
        # dbg.exception(e, f"{__name__}.{inspect.stack()[0][3]}")
        # print(e)
        # pp.pprint(locals())
        return None
    else:
        try:
            return list( json.loads(r.text).values() )[0]
        except Exception as e:
            # dbg.exception(e, f"{__name__}.{inspect.stack()[0][3]}")
            # print(e)
            # dbg.clsattrs(r)
            # pp.pprint(r.__dict__)
            return None
