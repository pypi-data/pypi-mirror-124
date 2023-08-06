# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import os
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================ External-Library.
# ============================================================ My-Library.
import idebug as dbg
# ============================================================ Project.
# ============================================================ Constant.

# ============================================================
# ============================================================
def get_apikey():
    try:
        id = os.environ['NAVER_CLIENT_ID']
        secret = os.environ['NAVER_CLIENT_SECRET']
    except Exception as e:
        print(f"e:{e}")
        raise
    else:
        return id, secret
