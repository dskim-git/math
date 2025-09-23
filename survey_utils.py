# survey_utils.py
from __future__ import annotations
import io
import re
import time
from collections import Counter
from typing import Iterable, List, Tuple
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import pandas as pd

# requests가 없으면 pandas의 read_csv로도 동작하지만,
# 실시간성을 높이기 위해 가능하면 requirements.txt에 'requests'를 추가해 주세요.
try:
    import requests  # type: ignore
    _HAS_REQUESTS = True
except Exception:
    _HAS_REQUESTS = False


# ─────────────────────────────────────────────────────────────────────────────
# Google Sheets 도우미

def _extract_file_id_and_gid(url: str) -> tuple[str | None, str | None]:
    """일반 시트 URL에서 FILE_ID와 gid를 뽑아냅니다."""
    m_file = re.search(r"/spreadsheets/d/([a-zA-Z0-9\-_]+)", url)
    file_id = m_file.group(1) if m_file else None
    m_gid = re.search(r"[#?&]gid=(\d+)", url)
    gid = m_gid.group(1) if m_gid else None
    return file_id, gid


def make_csv_export_url(url_or_csv: str) -> str:
    """
    입력이 '일반 시트 URL'이든 '이미 CSV URL'이든 상관 없이
    항상 CSV export URL을 반환합니다.
    """
    u = (url_or_csv or "").strip()
    if not u:
        return u

    # 이미 CSV 엔드포인트라면 그대로 사용
    if ("output=csv" in u) or ("/export" in u and "format=csv" in u):
        return u

    # gviz 스타일을 CSV로 강제
    if "/gviz/tq" in u:
        parsed = urlparse(u)
        qs = parse_qs(parsed.query)
        qs["tqx"] = ["out:csv"]
        new_q = urlencode(qs, doseq=True)
        return urlunparse(parsed._replace(query=new_q))

    # 일반 시트 URL → export CSV로 변환
    file_id, gid = _extract_file_id_and_gid(u)
    if file_id:
        gid = gid or "0"
        return f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid={gid}"

    # 그 밖의 경우: 사용자가 CSV를 준 것으로 보고 그대로 리턴
    return u


def load_csv_live(url_or_sheet: str, cache_bust: int | None = None) -> pd.DataFrame:
    """
    실시간 로드를 위한 CSV 가져오기.
    - 일반 시트 URL/게시 링크/CSV 링크 모두 입력 가능
    - cache_bust(정수)가 달라질 때마다 새로 다운로드(캐시 무력화)
    """
    if not url_or_sheet:
        return pd.DataFrame()

    csv_url = make_csv_export_url(url_or_sheet)
    if cache_bust is None:
        cache_bust = int(time.time())

    # 캐시 무력화 쿼리 파라미터 추가
    sep = "&" if "?" in csv_url else "?"
    final_url = f"{csv_url}{sep}_ts={cache_bust}"

    try:
        if _HAS_REQUESTS:
            r = requests.get(final_url, headers={"Cache-Control": "no-cache"})
            r.raise_for_status()
            df = pd.read_csv(io.BytesIO(r.content))
        else:
            # requests가 없으면 pandas가 직접 다운로드(약간 캐싱될 수 있음)
            df = pd.read_csv(final_url)
    except Exception:
        # 혹시 모를 예외 시 재시도 없이 빈 DF
        return pd.DataFrame()

    # 가끔 생기는 완전 빈 열 제거
    df = df.dropna(axis=1, how="all")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 집계/토큰화 유틸

def parse_mcq_series(s: pd.Series) -> Counter:
    """
    구글폼 객관식/체크박스 응답을 집계합니다.
    체크박스형은 '옵션1; 옵션2' 같은 합쳐진 문자열을 분해해서 집계합니다.
    """
    cnt = Counter()
    for v in s.dropna().astype(str):
        parts = re.split(r"[;,]\s*", v.strip())
        for p in parts:
            if p:
                cnt[p] += 1
    return cnt


def basic_tokenize_korean(texts: Iterable[str]) -> List[str]:
    """
    초간단 한국어 토큰화(공백/문장부호 분리).
    정확한 형태소 분석이 필요하면 konlpy/kiwipiepy를 사용하세요.
    """
    tokens: List[str] = []
    for t in texts:
        t = str(t)
        t = re.sub(r"http[s]?://\S+", " ", t)       # URL 제거
        t = re.sub(r"[^\w\sㄱ-힣]", " ", t)           # 기호 제거
        for tok in t.split():
            if len(tok) >= 2:
                tokens.append(tok)
    return tokens


def top_n_tokens(tokens: List[str], n: int = 50, stopwords: Iterable[str] = ()) -> List[Tuple[str, int]]:
    sw = set(x.strip() for x in stopwords if x)
    c = Counter(tok for tok in tokens if tok not in sw)
    return c.most_common(n)
