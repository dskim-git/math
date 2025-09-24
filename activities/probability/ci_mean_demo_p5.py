# activities/probability/ci_mean_demo_p5.py
# 같은 시트(원본 탭)를 사용해 표본 100개를 뽑고,
# 각 표본의 모평균 신뢰구간을 p5.js로 시각화합니다.

from __future__ import annotations
import re
import json
from urllib.parse import urlparse, parse_qs, quote

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import t  # t-분포 임계값

META = {
    "title": "모평균 신뢰구간 체험 (p5.js)",
    "description": "같은 모집단에서 표본 100세트를 뽑아 평균의 신뢰구간을 그려보고, 신뢰도와의 관계를 체험합니다.",
    "order": 55,
}

# ─────────────────────────────────────────────────────────────────────────────
# 구글시트 공유 URL → CSV 주소로 변환
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

    if gid:
        return f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={gid}"

    sheet_enc = quote(sheet, safe="")
    return f"https://docs.google.com/spreadsheets/d/{doc_id}/gviz/tq?tqx=out:csv&sheet={sheet_enc}"

def load_population(csv_url: str) -> pd.DataFrame:
    df = pd.read_csv(csv_url)
    return df.dropna(axis=1, how="all")

def guess_numeric_cols(df: pd.DataFrame):
    """숫자열 후보와 기본 선택(첫 숫자열이 '반/학급' 같으면 제외)."""
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not num_cols:
        return [], []
    default = num_cols.copy()
    first = num_cols[0]
    s = df[first].dropna()
    looks_class = (str(first).strip() in ("반", "학급", "class", "Class") or (s.nunique() <= max(30, int(len(s)*0.1))))
    if looks_class and len(num_cols) >= 2:
        default = num_cols[1:]
    return num_cols, default

def draw_samples(values: np.ndarray, n: int, m: int, seed: int):
    """복원추출로 표본 m개 생성."""
    rng = np.random.default_rng(seed)
    N = len(values)
    samples = [values[rng.integers(0, N, size=n)] for _ in range(m)]
    return samples

def ci_mean(x: np.ndarray, conf: float):
    """
    평균의 (양측) 신뢰구간: x̄ ± t_{1-α/2, n-1} * s/√n
    conf=0.95 → 95% CI
    """
    n = len(x)
    xbar = float(np.mean(x))
    s = float(np.std(x, ddof=1)) if n > 1 else 0.0
    if n <= 1:
        return xbar, xbar, xbar, s
    alpha = 1 - conf
    crit = float(t.ppf(1 - alpha/2, df=n-1))
    half = crit * s / np.sqrt(n)
    return xbar - half, xbar + half, xbar, s

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.title("모평균 신뢰구간 체험 (p5.js)")

    # 같은 시트 기본값
    default_sheet = "https://docs.google.com/spreadsheets/d/1APFg3_bk6NdclVvpjwzCKGXBq86u9732/edit?usp=sharing"

    # ── 사이드바 (sampling_mean_demo_p5와 유사) ───────────────────
    with st.sidebar:
        st.subheader("📥 데이터 소스")
        raw_url = st.text_input("구글시트 주소", value=default_sheet,
                                help="상단 공유 URL을 그대로 붙여넣어도 됩니다.")
        sheet_name = st.text_input("시트 탭 이름", value="원본")
        csv_url = to_csv_url(raw_url, sheet=sheet_name)

    if not csv_url:
        st.info("좌측에 구글시트 주소를 입력하세요.")
        return

    try:
        df = load_population(csv_url)
    except Exception as e:
        st.error(f"모집단 데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return

    num_cols, default_sel = guess_numeric_cols(df)
    with st.sidebar.expander("➕ (선택) 사용할 숫자열 직접 선택", expanded=False):
        sel_cols = st.multiselect("키가 들어있는 열(한 개 이상)", options=num_cols, default=default_sel)
    if not num_cols:
        st.warning("시트에 숫자 데이터가 없습니다.")
        st.dataframe(df, use_container_width=True)
        return
    if not sel_cols:
        sel_cols = default_sel

    # 숫자열 벡터화 (모집단)
    values = df[sel_cols].select_dtypes(include=["number"]).to_numpy().ravel()
    values = values[~np.isnan(values)].astype(float)
    N = len(values)
    if N == 0:
        st.warning("선택한 열에서 숫자 데이터가 발견되지 않았습니다.")
        return

    pop_mu = float(np.mean(values))

    # ── 표본 설정 ──────────────────────────────────────────────────
    with st.sidebar:
        st.subheader("🎯 신뢰구간 설정")
        n = st.number_input("표본 크기 n", 2, 1000, 30, step=1)
        conf_pct = st.slider("신뢰도(%)", 50, 99, 95, step=1)
        conf = conf_pct / 100.0
        m = 100  # 고정
        seed = st.number_input("난수 시드", 0, 10000, 0, step=1)
        go = st.button("표본 100세트 추출 / 새로고침")

    if go or ("ci_samples" not in st.session_state):
        st.session_state["ci_samples"] = draw_samples(values, int(n), int(m), int(seed))

    samples = st.session_state["ci_samples"]

    # 1) 모집단 원본 보기
    st.subheader("📄 모집단 원본(선택한 숫자 열)")
    disp = df[sel_cols].copy()
    disp.columns = [f"{c}반" if not re.search(r"(반|학급|class)", str(c), flags=re.I) else str(c) for c in disp.columns]
    disp.index = pd.RangeIndex(1, len(disp)+1, name="번호")
    st.caption("열 = **학반**, 행 = **번호**")
    st.dataframe(disp, use_container_width=True, height=300)

    # 1-추가) 표본 표 + 신뢰구간 끝점 열 2개 추가
    st.subheader("🧪 표본 표와 요약 (신뢰구간 포함)")
    rows = []
    ci_list = []
    for i, s in enumerate(samples, start=1):
        lo, hi, xbar, s_hat = ci_mean(s, conf)
        ci_list.append((lo, hi, xbar))
        rows.append([i, len(s), xbar, s_hat, lo, hi])
    summary_df = pd.DataFrame(rows, columns=["표본#", "크기", "표본평균", "표본표준편차", f"{conf_pct}% CI L", f"{conf_pct}% CI R"])
    st.dataframe(summary_df, use_container_width=True, height=min(360, 40 + 28 * len(rows)))

    # 3) 100개의 신뢰구간 선분(가로) 세로 나열 + 모평균 수직선
    st.subheader("📊 100개 표본의 평균 신뢰구간")
    # 축 범위: 모든 CI를 커버하고 여백 추가
    lows  = [c[0] for c in ci_list]
    highs = [c[1] for c in ci_list]
    xmin = float(min(min(lows), pop_mu))
    xmax = float(max(max(highs), pop_mu))
    pad = (xmax - xmin) * 0.08 if xmax > xmin else 1.0
    xmin -= pad; xmax += pad

    contains = [(lo <= pop_mu <= hi) for (lo, hi, _) in ci_list]
    contain_cnt = sum(contains)

    payload = {
        "intervals": [{"lo": float(lo), "hi": float(hi), "mean": float(mu), "ok": bool(ok)}
                      for (lo, hi, mu), ok in zip(ci_list, contains)],
        "xmin": xmin, "xmax": xmax, "mu": pop_mu,
        "title": f"{conf_pct}% 신뢰구간 (표본 100개)",
    }

    # p5.js 캔버스
    row_h = 10  # 한 구간의 높이
    top_pad, bottom_pad = 50, 60
    H = top_pad + bottom_pad + len(payload["intervals"]) * row_h
    H = min(max(H, 380), 1200)  # 너무 길어지지 않게 제한
    html = f"""
<div id="ci_canvas" style="width:100%;max-width:980px;margin:0 auto;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<script>
const DATA = {json.dumps(payload)};
new p5((p)=>{
  const W=980, left=60, right=30, top=20, rowH={row_h};
  const N = DATA.intervals.length;
  const H = {H};
  function X(v){{ return p.map(v, DATA.xmin, DATA.xmax, left, W-right); }}

  p.setup = ()=>{{ p.createCanvas(W,H).parent("ci_canvas"); p.noLoop(); p.textFont('sans-serif'); }};
  p.draw = ()=>{
    p.background(255);
    // 제목
    p.fill(0); p.noStroke(); p.textSize(12); p.textAlign(p.LEFT,p.TOP);
    p.text(DATA.title, left, 6);

    // x축과 눈금
    const yAxis = H-40;
    p.stroke(0); p.strokeWeight(1); p.line(left, yAxis, W-right, yAxis);
    // 눈금(5개)
    p.textAlign(p.CENTER,p.TOP); p.noStroke(); p.fill(60);
    for(let i=0;i<=5;i++){{
      const v = DATA.xmin + (DATA.xmax-DATA.xmin)*i/5;
      const x = X(v);
      p.stroke(190); p.line(x, yAxis-5, x, yAxis+5);
      p.noStroke(); p.text(v.toFixed(1), x, yAxis+8);
    }}

    // 모평균 수직선
    const xmu = X(DATA.mu);
    p.stroke(35,102,235); p.strokeWeight(2); p.line(xmu, top, xmu, yAxis-14);
    p.noStroke(); p.fill(35,102,235);
    p.textAlign(p.CENTER,p.BOTTOM); p.text('모평균 μ', xmu, top+16);

    // 각 표본 구간 (위에서 아래로)
    const startY = 40;
    for(let i=0;i<N;i++){{
      const it = DATA.intervals[i];
      const y = startY + i*rowH + 3;
      const x1 = X(it.lo), x2 = X(it.hi), xm = X(it.mean);
      // 바탕 가이드
      p.stroke(230); p.line(left, y, W-right, y);
      // 구간: 포함 여부에 따라 색
      if(it.ok){{ p.stroke(0,160,90); }} else {{ p.stroke(230,60,60); }}
      p.strokeWeight(3); p.line(x1, y, x2, y);
      // 표본평균 점
      p.noStroke(); p.fill(0,0,0,120); p.circle(xm, y, 4);
      // 오른쪽에 라벨(✔ / ✖)
      p.textAlign(p.LEFT,p.CENTER);
      if(it.ok){{ p.fill(0,160,90); p.text('✔ 포함', x2+6, y); }}
      else     {{ p.fill(230,60,60); p.text('✖ 제외', x2+6, y); }}
    }}
  };
});
</script>
    """
    components.html(html, height=H)

    # 3-마무리) 큰 요약 박스
    expected = conf_pct
    actual_pct = contain_cnt  # 100개 중 개수
    col = "#23a559" if contain_cnt >= int(0.01*expected*100) else "#e33c3c"  # 대략적 색감
    st.markdown(
        f"""
<div style="
  margin: 18px 0 8px 0; padding: 16px 18px; border-radius: 12px;
  background: linear-gradient(180deg, rgba(245,248,255,.9), rgba(235,250,245,.9));
  border: 1px solid rgba(0,100,200,.18);">
  <div style="font-size: 18px; font-weight: 700; margin-bottom: 6px;">
    결과 요약
  </div>
  <div style="display:flex; gap:16px; align-items:center; flex-wrap:wrap;">
    <div style="font-size: 28px; font-weight: 800; color:{col}">
      포함: {contain_cnt} / 100
    </div>
    <div style="font-size: 16px;">
      선택한 신뢰도: <b>{conf_pct}%</b>  &nbsp;|&nbsp;  기대: <b>약 {conf_pct}개</b> 포함
    </div>
    <div style="opacity:.8;">
      (표본 평균 신뢰구간은 진짜 모평균을 약 {conf_pct}% 확률로 포함하도록 설계됩니다)
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True
    )
