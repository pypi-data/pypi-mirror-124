# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
from datetime import datetime
import re
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================ External-Library.
import pandas as pd
# ============================================================ My-Library.
import idebug as dbg
from ipy import inumber
from ipy import idatetime
# ============================================================ Project.
# ============================================================ Constant.
def clean_dtcols(df, dt_cols):
    """
    어떠한 형태의 스트링 날짜일시를 datetime 타입으로 변환한다.
    로컬 시간대를 반드시 적용한다. 항상 한국 기준으로. 왜냐? KRX 는 한국에 있거든.
    """
    for c in dt_cols:
        try:
            df[c] = df[c].apply(idatetime.parse)
        except Exception as e:
            # dbg.exception(e, f"{__name__}.{inspect.stack()[0][3]}")
            # print(e)
            pass
    return df

def clean_numcols(df, num_cols):
    for c in num_cols:
        try:
            df[c] = df[c].apply(inumber.convert_numberstr)
        except Exception as e:
            # dbg.exception(e, f"{__name__}.{inspect.stack()[0][3]}")
            pass
    return df

def clean_intcols(df, int_cols):
    for c in int_cols:
        try:
            df[c] = df[c].apply(lambda x: int(x.replace(',', '')))
        except Exception as e:
            # dbg.exception(e, f"{__name__}.{inspect.stack()[0][3]}")
            pass
    return df

def clean_floatcols(df, float_cols):
    for c in float_cols:
        try:
            df[c] = df[c].apply(lambda x: float(x.replace(',', '')))
        except Exception as e:
            # dbg.exception(e, f"{__name__}.{inspect.stack()[0][3]}")
            pass
    return df

p_pct = re.compile('%$')
def clean_pctcols(df, pct_cols):
    """단위가 %인 수를 소수점으로 변환."""
    def _clean_(x):
        if isinstance(x, str):
            x = p_pct.sub(string=x, repl='')
            x = float(x.strip().replace(',', ''))
        return x / 100

    for c in pct_cols:
        try:
            df[c] = df[c].apply(_clean_)
        except Exception as e:
            # dbg.exception(e, f"{__name__}.{inspect.stack()[0][3]}")
            print(e)
    return df

def parse_rawdata(rawdata, **kw):
    """
    파싱을 하는 함수기 때문에 반환값에 대한 일관적인 규칙을 적용해야 한다.
    즉, rawdata가 None 이든 정상이든 반환값은 json-list 여야 한다.
    """
    # pp.pprint(kw)
    if rawdata is None:
        return rawdata
    else:
        if len(rawdata) is 0:
            return rawdata
        else:
            df = pd.DataFrame(rawdata)
            if 'cols_map' in kw: df = df.rename(columns=kw['cols_map'])
            if 'dt_cols' in kw: df = clean_dtcols(df, kw['dt_cols'])
            if 'num_cols' in kw: df = clean_numcols(df, kw['num_cols'])
            if 'pct_cols' in kw: df = clean_pctcols(df, kw['pct_cols'])
            return df.to_dict('records')
