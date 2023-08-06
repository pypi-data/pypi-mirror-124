# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
import os
import sys

pkgs = ['idebug','ipy','krx']
for p in pkgs:
    sys.path.append(f"{os.environ['PJTS_PATH']}/{p}")
