# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import inspect
import json
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================ External-Library.
import requests
# ============================================================ My-Library.
import idebug as dbg
# ============================================================ Project.
from naverapi import auth
# ============================================================ Constant.
SAMPLE_HEADERS = {

}


# ============================================================
# ============================================================
def _headers_():
    id, secret = auth.get_apikey()
    return {
        'X-Naver-Client-Id':id,
        'X-Naver-Client-Secret':secret
    }

def get(url, **kw):
    try:
        r = requests.get(url, headers=_headers_(), **kw)
    except Exception as e:
        print(f"e:{e}")
    else:
        if r.status_code is 200:
            return json.loads(r.text)
        else:
            dbg.clsattrs(cls=r, console=True)
