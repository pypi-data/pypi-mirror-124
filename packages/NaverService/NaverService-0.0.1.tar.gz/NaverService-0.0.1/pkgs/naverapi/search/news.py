# -*- coding: utf-8 -*-
"""
검색 > 뉴스.
https://developers.naver.com/docs/search/news/

API 특성상, 최근 데이터만 얻을 수 있고,
과거의 특정일의 데이터를 수집할 수 없다.


DB에 저장할 필요가 있는가?
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import math
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================ External-Library.
import pandas as pd
# ============================================================ My-Library.
from ipy import idatetime
# import idebug as dbg
# ============================================================ Project.
from naverapi import req
from naverapi import parser
from naverapi import models
from naverapi.search import queryword
# ============================================================ Constant.
URL = 'https://openapi.naver.com/v1/search/news.json'



# ============================================================
"""Library."""
# ============================================================
def filter_dt(df, **kw):
    if len(df) is 0:
        print(f"{__name__}.{inspect.stack()[0][3]} | len(df) is 0.")
    else:
        if 'sdt' in kw:
            sdt = idatetime.parse(dt=sdt)
            print(f"sdt: {sdt}")
            df = df.query(f'dt >= "{sdt}"')
        if 'edt' in kw:
            edt = idatetime.parse(dt=edt)
            print(f"edt: {edt}")
            df = df.query(f'dt <= "{edt}"')
        if 'dt' in kw:
            dt = idatetime.parse(dt=dt)
            print(f"dt: {dt}")
            df = df.query(f'dt')
    return df

def _setup_sdt_edt_(sdt=None, edt=None):
    if sdt is None:
        sdt = idatetime.today(tz=+9)
    else:
        sdt = idatetime.parse(dt=sdt)
    if edt is None:
        edt = idatetime.delta_dt(delta=1, dt=None, tz=+9)
    else:
        edt = idatetime.parse(dt=edt)
    return sdt, edt
# ============================================================
"""DataModel."""
# ============================================================
class NewsDS:
    sample_schema = {
        '_id':'ObjectId',
        'dt':'',
        'head':'',
        'body':'',
        'link':'',
        'olink':'',
    }
    id_cols = ['dt','link']
    cols_map = {
        'title':'head',
        'pubDate':'dt',
        'description':'body',
        'link':'link',
        'originallink':'olink',
    }
    dt_cols= ['dt']
    def __init__(self):
        pass

class NewsIO(models.News, NewsDS):
    def __init__(self):
        super().__init__()
    def load(self, **filter):
        df = self.load_tbl(filter=self.clean_filter(**filter)).df.copy()
        if len(df) is 0:
            pass
        else:
            df.dt = df.dt.apply(idatetime.astimezone, (+9,))
            self.df = df.sort_values('dt', ascending=False).reset_index(drop=True)
        return self
    def save(self, data):
        if data is None:
            pass
        else:
            for d in data:
                filter = {k:v for k, v in d.items() if k in self.id_cols}
                update = {'$set':d}
                self.update_one(filter=filter, update=update, upsert=True)
        return self
# ============================================================
"""Library."""
# ============================================================
def _calc_totParts_(meta):
    f, i = math.modf(meta['total'] / meta['display'])
    if f > 0: i += 1
    else: pass
    meta['n_parts'] = int(i)
    return meta
# ============================================================
"""Collector."""
# ============================================================
def fetch(query, display=100, start=1, sort='sim'):
    print(f"{__name__}.{inspect.stack()[0][3]} | {locals()}")
    qs = {
        'query':query,
        'display':display,
        'start':start,
        'sort':sort
    }
    return req.get(url=URL, params=qs)

def parse(jsdata):
    if jsdata is None:
        return jsdata
    else:
        if len(jsdata) is 0:
            return jsdata
        else:
            meta = jsdata.copy()
            rawdata = meta.pop('items')
            cls = NewsDS()
            data = parser.parse_rawdata(rawdata, cols_map=cls.cols_map, dt_cols=cls.dt_cols)
            data = _clean_htmltags_(data)
    return meta, data

def _clean_htmltags_(data):
    df = pd.DataFrame(data)
    for c in ['head', 'body']:
        df[c] = df[c].str.replace(pat='\</*b\>|\&quot;', repl='')

    return df.to_dict('records')

def collect_aDisplay(query, display=100, start=1, sort='sim'):
    info = locals()

    jsdata = fetch(query=query, display=display, start=start, sort=sort)
    meta, data = parse(jsdata)

    info.update(meta)
    pp.pprint(info)
    # NewsIO().save(data)

class CollectIterator(models.GenBaseModel):
    def __init__(self, query, sdt=None, sort='date'):
        self.io = NewsIO()
        self.qw = queryword.QueryWord(q=query)
        self.sdt, edt = _setup_sdt_edt_(sdt=sdt)
        self.sort = sort
    def collect_firstDisplay(self):
        jsdata = fetch(query=self.qw.q, start=1, sort=self.sort)
        meta, self.data = parse(jsdata)
        meta = _calc_totParts_(meta)
        return self.attributize(dic=meta)
    def save(self):
        self.io.data = data
        self.io.save(qw=self.qw)

    # def collect_restDisplay(self):

def collect_byDate(query, sdt=None, sort='date'):
    """
    Naver API 시스템 특성상, edt 는 필요가 없다.
    """
    qw = queryword.QueryWord(q=query)
    sdt, edt = _setup_sdt_edt_(sdt=sdt)
    """1번째 수집."""
    cls = NewsIO()
    jsdata = fetch(query=query, start=1, sort=sort)
    meta, cls.data = parse(jsdata)
    meta = _calc_totParts_(meta)
    # return meta
    cls.save(qw=qw)
    df = pd.DataFrame(cls.data)
    min_dt = df.dt.min()
    """2 ~ Nth 수집."""
    while (min_dt >= sdt):
        meta['start'] += 100
        # print(f"{'-'*100} meta['start']: {meta['start']}")
        jsdata = fetch(query=query, start=meta['start'], sort=sort)
        _meta_, cls.data = parse(jsdata)
        cls.save(qw=qw)
        df = pd.DataFrame(cls.data)
        min_dt = df.dt.min()
    else:
        print(f"{__name__}.{inspect.stack()[0][3]} | While Loop 끝. | sdt: {sdt} | min_dt: {min_dt}")
# ============================================================
"""DataIO."""
# ============================================================
# ============================================================
"""APIs."""
# ============================================================
def search(query, display=100, start=1, sort='sim', **kw):
    jsdata = fetch(query=query, display=display, start=start, sort=sort)
    meta, data = parse(jsdata)
    df = pd.DataFrame(data).sort_values('dt', ascending=False).reset_index(drop=True)

    df = filter_dt(df, **kw)
    if len(df) is 0:
        print(f"{__name__}.{inspect.stack()[0][3]} | len(df) is 0.")

    return report(df=df)

# ============================================================
"""Report."""
# ============================================================
def report(df, ascending=False):
    for i, d in enumerate(df.sort_values('dt', ascending=ascending).to_dict('records'), start=1):
        print(f"{'-'*130} {i}/{len(df)}")
        print(f"dt: {d['dt']}")
        print(f"head: {d['head']}")
        print(f"body: {d['body']}")
        print(f"link: {d['link']}")
