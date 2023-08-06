# -*- coding: utf-8 -*-
"""
Batch 실행파일.
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import sys
import os
import threading


if __name__ == "__main__":
    # ============================================================ Intro.
    print(f"{'+'*50} {__name__}")
    print(f"""
        sys.argv : {sys.argv}
    """)
    # ============================================================ My-Library.
    PJT_PATH = os.path.dirname(os.path.abspath(__file__))
    os.environ['LOG_PATH'] = f"{PJT_PATH}/log/batch"
    # ============================================================ Project.
    from stock import util
    util.pcinfo()
    # ============================================================ Job-List.
    XXX_jobs = []
    jobs = XXX_jobs
    # ============================================================ Run.
    threads = []
    for job in jobs:
        # print(job.__name__)
        # break
        t = threading.Thread(target=job, name=job.__name__)
        threads.append(t)
    for t in threads:
        print(f"{'+'*50} {t}")
        t.start()
    for t in threads:
        t.join()
