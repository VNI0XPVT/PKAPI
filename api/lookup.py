import os, re, time, json, requests
from bs4 import BeautifulSoup

TARGET_BASE = "https://pakistandatabase.com"
TARGET_PATH = "/databases/sim.php"
MIN_INTERVAL = 1.0
LAST_CALL = {"ts": 0.0}

def is_mobile(value: str) -> bool:
    return bool(re.fullmatch(r"92\d{9,12}", value.strip()))

def is_cnic(value: str) -> bool:
    return bool(re.fullmatch(r"\d{13}", value.strip()))

def classify_query(value: str):
    v = value.strip()
    if is_mobile(v): return "mobile", v
    if is_cnic(v): return "cnic", v
    raise ValueError("Invalid number format")

def rate_limit_wait():
    now = time.time()
    diff = now - LAST_CALL["ts"]
    if diff < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - diff)
    LAST_CALL["ts"] = time.time()

def fetch(q):
    rate_limit_wait()
    s = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0", "Referer": TARGET_BASE}
    data = {"search_query": q}
    r = s.post(TARGET_BASE + TARGET_PATH, headers=headers, data=data, timeout=20)
    r.raise_for_status()
    return r.text

