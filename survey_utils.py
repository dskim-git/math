# survey_utils.py
from __future__ import annotations
import re, time, urllib.parse
from collections import Counter
from typing import Iterable, List, Tuple
import pandas as pd

# ── (A) 구글 시트/퍼블리시 URL ⇒ CSV export URL로 자동 변환 ─────────────────
def make_csv_export_url(url: str) -> str:
    if not url:
        return ""
    u = url.strip()

    # 이미 CSV export면 그대로 사용
    if "export?format=csv" in u or "output=csv" in u:
        return u

    # gviz 쿼리 주소: tqx=out:csv 형태면 그대로 OK (없으면 붙여줌)
    if "/gviz/tq" in u:
        parsed = urllib.parse.urlparse(u)
        qs = urllib.parse.parse_qs(parsed.query)
        qs["tqx"] = ["out:csv"]
        new_q = urllib.parse.urlencode(qs, doseq=True)
        return urllib.parse.urlunparse(parsed._replace(query=new_q))

    # 일반 편집 주소: /d/<FILE_ID>/edit#gid=<GID>
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)/", u)
    if m:
        file_id = m.group(1)
        gid_match = re.search(r"[?#&]gid=([0-9]+)", u)
        gid = gid_match.group(1) if gid_match else "0"
        return f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid={gid}"

    # 공개 퍼블리시(d/e/…/pub) 유형이면 그대로 사용(이미 CSV일 확률 높음)
    if "/spreadsheets/d/e/" in u and "/pub" in u:
        return u if "output=csv" in u else (u + ("&" if "?" in u else "?") + "output=csv")

    # 마지막 안전망: 그대로 반환
    return u

# ── (B) 실시간 로딩: cache_bust 값을 파라미터로 받아 매번 다른 URL 사용 ─────
def load_csv_live(csv_or_sheet_url: str, cache_bust: int = 0) -> pd.DataFrame:
    if not csv_or_sheet_url:
        return pd.DataFrame()
    csv_url = make_csv_export_url(csv_or_sheet_url)
    # 캐시 무력화 쿼리(구글은 무시해도, 캐싱 계층과 pandas가 새로 받아오도록 유도)
    sep = "&" if "?" in csv_url else "?"
    busted = f"{csv_url}{sep}_ts={int(time.time())}_{cache_bust}"
    df = pd.read_csv(busted)
    df = df.dropna(axis=1, how="all")
    return df

# ── (C) 이하 기존 유틸 ──────────────────────────────────────────────────────
def parse_mcq_series(s: pd.Series) -> Counter:
    cnt = Counter()
    for v in s.dropna().astype(str):
        parts = re.split(r"[;,]\s*", v.strip())
        for p in parts:
            if p:
                cnt[p] += 1
    return cnt

def basic_tokenize_korean(texts: Iterable[str]) -> List[str]:
    tokens: List[str] = []
    for t in texts:
        t = str(t)
        t = re.sub(r"http[s]?://\S+", " ", t)
        t = re.sub(r"[^\w\sㄱ-힣]", " ", t)
        for tok in t.split():
            if len(tok) >= 2:
                tokens.append(tok)
    return tokens

def top_n_tokens(tokens: List[str], n: int = 50, stopwords: Iterable[str] =()) -> List[Tuple[str,int]]:
    sw = set(x.strip() for x in stopwords if x)
    c = Counter(tok for tok in tokens if tok not in sw)
    return c.most_common(n)
