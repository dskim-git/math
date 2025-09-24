# activities/probability/confint_mean_demo_p5.py
# 모평균 신뢰구간(표본 100세트) 시각화: 구글시트 모집단 → 표본평균 t-구간

from __future__ import annotations
import re
import json
from urllib.parse import urlparse, parse_qs, quote
from typing import List, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import t  # t-분포 임계값

META = {
    "title": "모평균 신뢰구간의 의미 (p5.js)",
    "description": "구글시트 모집단에서 표본 100세트를 추출하여, 각 표본의 모평균 신뢰구간과 참모평균 포함 여부를 시각화합니다.",
    "order": 55,
}

# ─────────────────────────────────────────────────────────────────────────────
# Google Sheets 공유 URL → CSV 주소로 정규화
def to_csv_url(url: str, sheet: str = "원본") -> str:
    s = (url or "").strip()
    if not s:
        return s
    sl = s.lower()
    if ("output=csv" in sl) or ("/export?format=csv" in sl) or ("/gviz/tq?tqx=out:csv" in sl):
        return s

    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", s)
    if not m:
        return s
    doc_id = m.group(1)

    parsed = urlparse(s)
    gid = None
    m_gid = re.search(r"gid=(\d+)", parsed.fragment or "")
    if m_gid:
        gid = m_gid.group(1)
    if not gid:
        qs = parse_qs(parsed.query or "")
        if "gid" in qs and qs["gid"]:
            gid = qs["gid"][0]

    if gid:  # 특정 탭 gid가 있으면 export 사용
        return f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={gid}"

    sheet_enc = quote(sheet, safe="")
    return f"https://docs.google.com/spreadsheets/d/{doc_id}/gviz/tq?tqx=out:csv&sheet={sheet_enc}"

def _load_population(csv_url: str) -> pd.DataFrame:
    df = pd.read_csv(csv_url)
    df = df.dropna(axis=1, how="all")
    return df

def _guess_numeric_columns(df: pd.DataFrame):
    """숫자열 후보와 기본 선택(첫 숫자열이 '반/학급'처럼 보이면 제외)."""
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not num_cols:
        return [], []
    default = num_cols.copy()
    first = num_cols[0]
    s = df[first].dropna()
    looks_class = (
        str(first).strip() in ("반", "학급", "class", "Class")
        or (s.nunique() <= max(30, int(len(s) * 0.1)))
    )
    if looks_class and len(num_cols) >= 2:
        default = num_cols[1:]
    return num_cols, default

def _draw_samples(values: np.ndarray, n: int, m: int, seed: int):
    rng = np.random.default_rng(seed)
    N = len(values)
    samples = []
    for _ in range(m):
        idx = rng.integers(0, N, size=n)
        samples.append(values[idx])
    return samples

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.title("모평균 신뢰구간의 의미 (p5.js)")

    # ── 데이터 소스 (sampling_mean_demo_p5 와 동일한 기본값)
    default_sheet_url = "https://docs.google.com/spreadsheets/d/1APFg3_bk6NdclVvpjwzCKGXBq86u9732/edit?usp=sharing"
    with st.sidebar:
        st.subheader("📥 데이터 소스")
        raw_url = st.text_input(
            "구글시트 주소",
            value=default_sheet_url,
            help="상단 공유 URL을 그대로 붙여넣어도 됩니다. 코드가 CSV 주소로 변환합니다."
        )
        sheet_name = st.text_input("시트 탭 이름", value="원본")
        csv_url = to_csv_url(raw_url, sheet=sheet_name)

    if not csv_url:
        st.info("좌측에 구글시트 주소를 입력하세요.")
        return

    # 모집단 로드
    try:
        df = _load_population(csv_url)
    except Exception as e:
        st.error(f"모집단 데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return

    # 숫자열 선택(덜 눈에 띄게 expander 안)
    num_cols, default_sel = _guess_numeric_columns(df)
    with st.sidebar.expander("➕ (선택) 사용할 숫자열 직접 선택", expanded=False):
        sel_cols = st.multiselect(
            "키가 들어있는 열(한 개 이상)",
            options=num_cols,
            default=default_sel,
            help="A열이 '반/학급' 등으로 숫자로 보이는 경우 기본에서 제외됩니다."
        )
    if not num_cols:
        st.warning("시트에 숫자 데이터가 없습니다.")
        st.dataframe(df, use_container_width=True)
        return
    if not sel_cols:
        sel_cols = default_sel

    # 숫자열만 펼쳐서 벡터화
    num_df = df[sel_cols].select_dtypes(include=["number"])
    values = num_df.to_numpy().ravel()
    values = values[~np.isnan(values)].astype(float)

    N = len(values)
    if N == 0:
        st.warning("선택한 열에서 숫자 데이터가 발견되지 않았습니다.")
        st.dataframe(df, use_container_width=True)
        return

    # 모집단 통계(참 모평균)
    mu = float(np.mean(values))
    sigma = float(np.std(values, ddof=0))

    # ── 표본/신뢰도 설정
    with st.sidebar:
        st.subheader("🎲 표본 설정")
        n = st.number_input("표본 크기 n", 2, 1000, 30, step=1)
        conf = st.slider("신뢰수준 (%)", 50, 99, 95, step=1, help="100이나 0은 이론적으로 무의미하므로 50~99% 범위를 권장합니다.")
        seed = st.number_input("난수 시드", 0, 10_000, 0, step=1)
        st.caption("※ 표본의 개수는 항상 **100세트**로 고정합니다.")
        go = st.button("표본 100세트 추출 / 갱신")

    M = 100  # 표본 개수 고정

    # 표본 100세트 생성(버튼 누를 때만 갱신)
    if go:
        st.session_state["ci_samples"] = _draw_samples(values, int(n), M, int(seed))

    samples = st.session_state.get("ci_samples")
    if not samples:
        samples = _draw_samples(values, int(n), M, int(seed))
        st.session_state["ci_samples"] = samples

    # 1) 모집단 원본(선택한 숫자 열) 보기
    st.subheader("📄 모집단 원본(선택한 숫자 열)")
    disp = df[sel_cols].copy()
    disp.columns = [f"{c}반" if not re.search(r"(반|학급|class)", str(c), flags=re.I) else str(c) for c in disp.columns]
    disp.index = pd.RangeIndex(1, len(disp) + 1, name="번호")
    st.caption("열 = **학반**,  행 = **번호**  (필요 열만 표시)")
    st.dataframe(disp, use_container_width=True, height=300)

    # 2) 표본 표 + 요약(+ CI 좌/우 끝)
    st.subheader("🧪 표본 표와 요약 (각 표본의 모평균 신뢰구간 포함)")
    alpha = 1 - (conf / 100.0)
    # 극단 회피: t.ppf(1 - alpha/2, df)에서 p가 0 또는 1이 안되도록 clamp
    p_right = max(1e-8, min(1 - alpha/2, 1 - 1e-8))

    rows = []
    ci_list = []  # [(lo, hi, contains_mu)]
    for i, s in enumerate(samples, start=1):
        s = np.asarray(s, dtype=float)
        xbar = float(np.mean(s))
        s_hat = float(np.std(s, ddof=1))  # 표본표준편차
        se = s_hat / np.sqrt(len(s))
        tcrit = float(t.ppf(p_right, df=len(s) - 1))
        half = tcrit * se
        lo, hi = xbar - half, xbar + half
        contains = (lo <= mu <= hi)
        rows.append([i, len(s), xbar, s_hat, lo, hi])
        ci_list.append((lo, hi, contains))

    summary_df = pd.DataFrame(rows, columns=["표본#", "크기", "표본평균", "표본표준편차", "CI_L", "CI_R"])
    st.dataframe(summary_df, use_container_width=True, height=32 + 28 * min(M, 10))

    # 3) 100개 구간을 p5.js로 세로 나열 + 모평균 수직선
    st.subheader("📍 100개 표본의 모평균 신뢰구간 시각화")
    # x축 범위: 전체 구간의 최소/최대에 여백
    all_los = [x[0] for x in ci_list]
    all_his = [x[1] for x in ci_list]
    xmin = float(min(min(all_los), np.min(values)))
    xmax = float(max(max(all_his), np.max(values)))
    span = xmax - xmin if xmax > xmin else 1.0
    xmin -= 0.05 * span
    xmax += 0.05 * span

    contain_count = int(sum(1 for lo, hi, c in ci_list if c))
    hit_rate = contain_count / M * 100

    payload = {
        "cis": ci_list,      # [ [lo, hi, contains], ... ]
        "mu": mu,
        "xmin": xmin, "xmax": xmax,
        "conf": int(conf),
        "contain": contain_count,
        "M": M,
        "hitRate": hit_rate,
    }

    html = """
<div id="ci_board" style="width:100%;max-width:1000px;margin:0 auto;"></div>
<style>
.badge-wrap{display:flex;justify-content:center;gap:16px;margin-top:8px}
.badge{
  padding:10px 16px;border-radius:12px;font-weight:700;
  background:linear-gradient(180deg,#f8fbff,#eef5ff);
  border:1px solid #9bbcff33; box-shadow:0 2px 10px rgba(40,90,200,.08);
}
.badge .big{font-size:28px;letter-spacing:.5px}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<script>
const D = """ + json.dumps(payload) + """;
new p5((p)=>{
  const W=1000, H=760, padL=70, padR=40, padT=30, padB=80;
  const rows=Math.min(D.cis.length, 100), rowGap=(H-padT-padB)/rows;

  function X(x){ return p.map(x, D.xmin, D.xmax, padL, W-padR); }

  p.setup=()=>{ p.createCanvas(W,H).parent("ci_board"); p.noLoop(); p.textFont('sans-serif'); };
  p.draw=()=>{
    p.background(255);
    // 제목
    p.noStroke(); p.fill(0); p.textAlign(p.CENTER,p.TOP); p.textSize(13);
    p.text('각 표본의 모평균 신뢰구간 ('+rows+'개, 신뢰수준 '+D.conf+'%)', W/2, 6);

    // x축 눈금(5등분)
    p.stroke(0); p.strokeWeight(1);
    p.line(padL, H-padB, W-padR, H-padB);
    p.fill(0); p.textAlign(p.CENTER,p.TOP); p.textSize(11);
    for(let i=0;i<=5;i++){
      const v = D.xmin + (D.xmax-D.xmin)*i/5;
      const xx = X(v); p.stroke(200); p.line(xx, H-padB, xx, H-padB+6);
      p.noStroke(); p.text(v.toFixed(1), xx, H-padB+8);
    }
    // 참모평균 수직선
    const xm = X(D.mu);
    p.stroke(30,120,255); p.strokeWeight(2);
    p.line(xm, padT-4, xm, H-padB+2);
    p.noStroke(); p.fill(30,120,255); p.textAlign(p.CENTER,p.BOTTOM);
    p.text('μ = '+D.mu.toFixed(2), xm, padT-6);

    // 구간들
    for(let i=0;i<rows;i++){
      const [lo,hi,ok] = D.cis[i];
      const y = padT + i*rowGap + rowGap*0.5;

      // 배경 줄무늬(가독성)
      if(i%2===1){ p.noStroke(); p.fill(245); p.rect(padL-8, y-rowGap*0.5, W-padL-padR+16, rowGap); }

      // 구간 선
      const x1=X(lo), x2=X(hi);
      p.stroke(ok? p.color(0,160,95): p.color(230,60,60));
      p.strokeWeight(ok? 3: 2);
      p.line(x1, y, x2, y);

      // 끝 마커
      p.strokeWeight(4);
      p.point(x1,y); p.point(x2,y);

      // 포함 여부 표시(체크/엑스)
      p.noStroke(); p.textAlign(p.LEFT,p.CENTER); p.textSize(12);
      if(ok){ p.fill(0,150,85); p.text('✓ 포함', x2+8, y); }
      else  { p.fill(230,60,60); p.text('✕ 제외', x2+8, y); }

      // 표본 번호
      p.fill(90); p.textAlign(p.RIGHT,p.CENTER);
      p.text('#'+(i+1), x1-10, y);
    }

    // 하단 큰 배지: 포함 개수 vs 신뢰수준
    const good = (D.hitRate >= D.conf-1); // 대략적 비교(±1% 허용)
    p.noStroke();
    p.fill(0); p.textAlign(p.CENTER,p.TOP); p.textSize(12);
    const msg = '모평균을 포함한 구간: '+D.contain+' / '+D.M+' ('+D.hitRate.toFixed(1)+'%)   ·   신뢰수준 설정: '+D.conf+'%';
    p.text(msg, W/2, H-54);

    // 시각적 배지(사각형 + 큰 숫자)
    const cx=W/2, cy=H-22;
    p.noStroke();
    if(good){ p.fill(237,251,242); } else { p.fill(255,244,244); }
    p.rect(cx-200, cy-20, 400, 40, 12);
    p.textAlign(p.CENTER,p.CENTER);
    p.fill(good? p.color(0,150,85): p.color(230,60,60));
    p.textSize(22);
    p.text( (good?'✅ ':'⚠️ ')+ D.contain+' / '+D.M+'  ( '+D.hitRate.toFixed(1)+'% )', cx, cy );
  };
});
</script>
"""
    components.html(html, height=800)

    st.caption("※ 각 구간은 **t-분포 기반 신뢰구간**:  x̄ ± t(1−α/2; df=n−1)·s/√n  으로 계산했습니다.")
