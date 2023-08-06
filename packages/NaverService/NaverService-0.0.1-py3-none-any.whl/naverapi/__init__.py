# -*- coding: utf-8 -*-
"""
Service API.
https://developers.naver.com/docs/datalab/search/


[ API Structure ]
- Datalab
- Search
    - Blog
    - News
    - ...
    - Documents
- Shortened URL
- ...
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import os
# ============================================================ External-Library.
# ============================================================ My-Library.
# ============================================================ Project.
# ============================================================ Constant.
PJT_NAME = os.path.basename(os.path.dirname(__file__))

# print('='*50)
# print(f"{' '*20} Top Module.")
# print('='*50)
# print(f"__file__: {__file__}")
# print(f"PJT_NAME: {PJT_NAME}")

# ============================================================ APIs.
from naverapi.search import news
