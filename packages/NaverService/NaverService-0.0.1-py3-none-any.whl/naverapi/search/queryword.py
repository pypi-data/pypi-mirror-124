# -*- coding: utf-8 -*-
"""
검색어.
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import inspect
# ============================================================ External-Library.
import pandas as pd
# ============================================================ My-Library.
# import idebug as dbg
# ============================================================ Project.
from naverapi import models
# ============================================================ Constant.


# ============================================================
"""DataModel."""
# ============================================================
class QueryWordDS:
    sample_schema = {
        '_id':'ObjectId',
        'q':'씨젠',
    }
    id_cols = ['q']
    def __init__(self):
        pass

class QueryWordIO(models.QueryWord, QueryWordDS):
    def __init__(self):
        super().__init__()

class QueryWord(models.GenBaseModel, QueryWordDS):
    def __init__(self, q):
        self.q = q
        self.save().find_attr()
    def save(self):
        filter = {'q':self.q}
        QueryWordIO().update_one(filter, {'$set':filter}, upsert=True)
        return self
    def find_attr(self):
        io = QueryWordIO().load_tbl({'q':self.q})
        return self.attributize(dic=io.df.to_dict('records')[0])
# ============================================================
"""DataIO."""
# ============================================================
# ============================================================
"""APIs."""
# ============================================================
# ============================================================
"""Report."""
# ============================================================
