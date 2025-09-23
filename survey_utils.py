# survey_utils.py
from __future__ import annotations
import re
from collections import Counter
from typing import Iterable, List, Tuple
import pandas as pd

def load_published_csv(csv_url: str) -> pd.DataFrame:
    """구글시트 '웹에 게시' CSV 주소에서 DataFrame 로드."""
    if not csv_url:
        return pd.DataFrame()
    # 구글시트는 헤더 1행이 보통 질문 텍스트입니다.
    df = pd.read_csv(csv_url)
    # 완전 빈 컬럼 제거(가끔 생김)
    df = df.dropna(axis=1, how="all")
    return df

def parse_mcq_series(s: pd.Series) -> Counter:
    """
    구글폼 객관식/체크박스 응답을 집계.
    체크박스형은 '옵션1; 옵션2'처럼 세미콜론/쉼표로 합쳐지는 경우가 많아 분해 집계합니다.
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
    초간단 한국어 토큰화(공백/문장부호 분할).
    정확한 형태소분석이 필요하면 konlpy/kiwipiepy 등을 추가하면 됩니다.
    """
    tokens: List[str] = []
    for t in texts:
        t = str(t)
        # URL/이모지 제거(대략)
        t = re.sub(r"http[s]?://\S+", " ", t)
        t = re.sub(r"[^\w\sㄱ-힣]", " ", t)
        for tok in t.split():
            if len(tok) >= 2:  # 너무 짧은 토큰 제거
                tokens.append(tok)
    return tokens

def top_n_tokens(tokens: List[str], n: int = 50, stopwords: Iterable[str] =()) -> List[Tuple[str,int]]:
    sw = set(x.strip() for x in stopwords if x)
    c = Counter(tok for tok in tokens if tok not in sw)
    return c.most_common(n)
