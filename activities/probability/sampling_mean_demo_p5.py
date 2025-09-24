# activities/probability/sampling_mean_demo_p5.py
# 모집단(구글시트) → 표본 다중 추출 → 표본평균 분포를 p5.js로 시각화

from __future__ import annotations
import re
import json
from typing import List, Tuple
from urllib.parse import urlparse, parse_qs, quote

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "모평균과 표본평균의 관계",
    "description": "구글시트의 모집단에서 표본을 여러 번 추출해 표본평균 분포를 시각화합니다.",
    "order": 50,
}

# ─────────────────────────────────────────────────────────────────────────────
# 유틸: 구글시트 공유 URL → CSV 주소로 정규화
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

# ─────────────────────────────────────────────────────────────────────────────
def _load_population(csv_url: str) -> pd.DataFrame:
    df = pd.read_csv(csv_url)
    df = df.dropna(axis=1, how="all")
    return df

def _guess_numeric_columns(df: pd.DataFrame):
    """숫자열 후보와 기본 선택(첫 숫자열이 '반/학급' 같으면 제외)."""
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
    """values(모집단)에서 크기 n 표본을 m개 생성(복원추출)."""
    rng = np.random.default_rng(seed)
    N = len(values)
    samples, idx_lists = [], []
    for _ in range(m):
        idx = rng.integers(0, N, size=n)
        samples.append(values[idx])
        idx_lists.append(idx)
    return samples, idx_lists

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.title("모평균과 표본평균의 관계 (p5.js)")

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

    # 숫자열 선택(덜 눈에 띄게: 접기)
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

    # 표본 설정
    with st.sidebar:
        st.subheader("🎲 표본 설정")
        n = st.number_input("표본 크기 n", 2, 1000, 30, step=1)
        m = st.number_input("표본 개수 m", 1, 300, 30, step=1)
        seed = st.number_input("난수 시드", 0, 10_000, 0, step=1)
        show_5ticks = st.checkbox("가로축 5의 배수 눈금 표시", True)
        go = st.button("표본 추출/새로고침")

    # 모집단 통계
    pop_mu = float(np.mean(values))
    pop_sigma = float(np.std(values, ddof=0))
    pop_var = float(pop_sigma ** 2)

    # 2·3) 표본 추출
    if go:
        st.session_state["smd_samples"], st.session_state["smd_idxlists"] = _draw_samples(values, int(n), int(m), int(seed))

    samples = st.session_state.get("smd_samples")
    idx_lists = st.session_state.get("smd_idxlists")
    if not samples:
        samples, idx_lists = _draw_samples(values, int(n), int(m), int(seed))
        st.session_state["smd_samples"] = samples
        st.session_state["smd_idxlists"] = idx_lists

    # 1) 모집단 원본 데이터(행: 번호 / 열: 학반) 보기
    st.subheader("📄 모집단 원본(선택한 숫자 열)")
    disp = df[sel_cols].copy()
    # 열 이름에 '반' 명시
    disp.columns = [f"{c}반" if not re.search(r"(반|학급|class)", str(c), flags=re.I) else str(c) for c in disp.columns]
    disp.index = pd.RangeIndex(1, len(disp) + 1, name="번호")
    st.caption("열 = **학반**,  행 = **번호**  (필요 열만 표시)")
    st.dataframe(disp, use_container_width=True, height=300)

    with st.expander("전체 원본 보기"):
        tmp = df.copy()
        tmp.index = pd.RangeIndex(1, len(tmp) + 1, name="번호")
        st.dataframe(tmp, use_container_width=True, height=400)

    # 4) 표본 표 + 요약
    st.subheader("🧪 표본 표와 요약")
    sample_rows = []
    for i, samp in enumerate(samples, start=1):
        sample_rows.append([i, len(samp), float(np.mean(samp)), float(np.std(samp, ddof=1))])
    summary_df = pd.DataFrame(sample_rows, columns=["표본#", "크기", "표본평균", "표본표준편차"])
    st.dataframe(summary_df, use_container_width=True, height=min(300, 40 + 28 * len(samples)))

    with st.expander("각 표본의 원소 보기(상위 8개 표본만)"):
        cap = min(8, len(samples))
        cols = st.columns(2)
        for i in range(cap):
            with cols[i % 2]:
                st.markdown(f"**표본 #{i+1} (n={len(samples[i])})**")
                st.dataframe(pd.DataFrame({"값": samples[i]}), use_container_width=True, height=200)

    # 5) 모집단 가로 수직선 + 표본 강조 (드롭박스 → 슬라이더)
    st.subheader("📍 모집단 가로 수직선에서 표본의 위치(강조)")
    sel_idx = st.slider("강조할 표본 선택", 1, len(samples), value=1, help="아래 그래프를 가리지 않도록 슬라이더로 선택합니다.") - 1

    vmin, vmax = float(np.min(values)), float(np.max(values))
    payload1 = {
        "values": values.tolist(),
        "sel_indices": [int(x) for x in idx_lists[sel_idx].tolist()],
        "vmin": vmin, "vmax": vmax,
        "title": f"모집단({N}명) 가로 수직선과 표본 #{sel_idx+1} (n={len(samples[sel_idx])})",
        "showTicks": bool(show_5ticks)
    }
    # 빨간 점 + 짧은 수직막대(캔버스 높이의 1/4 길이)
    html1 = """
<div id="popline" style="width:100%;max-width:980px;margin:0 auto;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<script>
const DATA1 = """ + json.dumps(payload1) + """;
new p5((p)=>{
  let W=980,H=260, pad=40;
  p.setup=()=>{ p.createCanvas(W,H).parent("popline"); p.noLoop(); p.textFont('sans-serif'); };
  p.draw=()=>{
    p.background(255);
    const yAxis = H*0.60;
    // 축(가로)
    p.stroke(50); p.strokeWeight(2);
    p.line(pad, yAxis, W-pad, yAxis);

    // 제목
    p.noStroke(); p.fill(0); p.textSize(12); p.textAlign(p.CENTER,p.TOP);
    p.text(DATA1.title, W/2, 8);

    // 좌우 끝값
    p.textAlign(p.LEFT,p.TOP);  p.text(DATA1.vmin.toFixed(1), pad, yAxis+10);
    p.textAlign(p.RIGHT,p.TOP); p.text(DATA1.vmax.toFixed(1), W-pad, yAxis+10);

    // 5의 배수 눈금 표시(옵션)
    if (DATA1.showTicks){
      const min5 = Math.floor(DATA1.vmin/5)*5;
      const max5 = Math.ceil(DATA1.vmax/5)*5;
      p.textAlign(p.CENTER,p.TOP);
      for(let v=min5; v<=max5; v+=5){
        if (v>DATA1.vmin && v<DATA1.vmax){
          const x = p.map(v, DATA1.vmin, DATA1.vmax, pad, W-pad);
          p.stroke(180); p.strokeWeight(1); p.line(x, yAxis-6, x, yAxis+6);
          p.noStroke(); p.fill(90); p.text(v.toFixed(0), x, yAxis+16);
        }
      }
    }

    // 점들
    const sel = new Set(DATA1.sel_indices);
    for (let i=0;i<DATA1.values.length;i++){
      const v = DATA1.values[i];
      const x = p.map(v, DATA1.vmin, DATA1.vmax, pad, W-pad);
      const jitter = (Math.random()-0.5)*8;  // 겹침 완화
      if(sel.has(i)){
        // 빨간 점 + 수직 막대(캔버스 높이의 1/4 길이)
        const half = (H*0.25)/2.0;
        p.stroke(230,49,70); p.strokeWeight(2);
        p.line(x, yAxis-half, x, yAxis+half);
        p.noStroke(); p.fill(230,49,70);
        p.circle(x, yAxis+jitter, 7);
      }else{
        p.noStroke(); p.fill(160);
        p.circle(x, yAxis+jitter, 5);
      }
    }
  };
});
</script>
"""
    components.html(html1, height=280)

    # 6) 정규곡선(모집단 vs 표본평균) + 표본평균 점 (p5.js)
    st.subheader("📈 정규곡선: 모집단 N(μ, σ²) vs 표본평균 N(μ, σ²/n)")
    sample_means = [float(np.mean(s)) for s in samples]
    highlight = float(np.mean(samples[sel_idx]))
    theo_sigma = pop_sigma / np.sqrt(float(n))

    payload2 = {
        "mu_pop": float(pop_mu), "sd_pop": float(pop_sigma),
        "mu_bar": float(pop_mu), "sd_bar": float(theo_sigma),
        "sample_means": sample_means,
        "highlight": highlight,
        "title": "정규곡선과 표본평균 위치 표시"
    }
    html2 = """
<div id="gauss" style="width:100%;max-width:980px;margin:0 auto;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<script>
const D2 = """ + json.dumps(payload2) + """;
new p5((p)=>{
  let W=980,H=340, left=60, right=30, top=30, bottom=60;
  function pdf(x,mu,sd){ return (1/(sd*Math.sqrt(2*Math.PI)))*Math.exp(-0.5*Math.pow((x-mu)/sd,2)); }
  p.setup=()=>{ p.createCanvas(W,H).parent("gauss"); p.noLoop(); p.textFont('sans-serif'); };
  p.draw=()=>{
    p.background(255);
    const mu=D2.mu_pop, sd=D2.sd_pop, muB=D2.mu_bar, sdB=D2.sd_bar||1e-6;
    const xmin=Math.min(mu-4*sd, muB-6*sdB), xmax=Math.max(mu+4*sd, muB+6*sdB);
    let ymax=0;
    for(let i=0;i<600;i++){
      const x=xmin+(xmax-xmin)*i/599;
      ymax=Math.max(ymax, pdf(x,mu,sd), pdf(x,muB,sdB));
    }
    const X = x => p.map(x, xmin, xmax, left, W-right);
    const Y = y => p.map(y, 0,   ymax, H-bottom, top);

    // 축
    p.stroke(0); p.strokeWeight(1);
    p.line(left, H-bottom, W-right, H-bottom);
    p.noStroke(); p.fill(0); p.textSize(12); p.textAlign(p.LEFT,p.TOP);
    p.text(D2.title, left, 6);

    // 모집단 곡선(파랑)  N(μ, σ²)
    p.noFill(); p.stroke(35,102,235); p.strokeWeight(2); p.beginShape();
    for(let i=0;i<600;i++){ const x=xmin+(xmax-xmin)*i/599; p.vertex(X(x), Y(pdf(x,mu,sd))); } p.endShape();

    // 표본평균 곡선(주황)  N(μ, σ²/n)
    p.noFill(); p.stroke(245,128,37); p.strokeWeight(2); p.beginShape();
    for(let i=0;i<600;i++){ const x=xmin+(xmax-xmin)*i/599; p.vertex(X(x), Y(pdf(x,muB,sdB))); } p.endShape();

    // 표본평균 점들(연한 검정)
    p.noStroke(); p.fill(0,0,0,70);
    for(const m of D2.sample_means){ p.circle(X(m), H-bottom-12, 5); }

    // 선택 표본 평균(빨강)
    p.fill(230,49,70); p.circle(X(D2.highlight), H-bottom-12, 8);
    p.textAlign(p.CENTER,p.BOTTOM); p.fill(0);
    p.text('현재 표본 평균 '+D2.highlight.toFixed(2), X(D2.highlight), H-bottom-18);

    // 범례
    p.textAlign(p.LEFT,p.BOTTOM);
    p.fill(35,102,235); p.rect(left, H-28, 18, 3); p.fill(0); p.text('모집단 N(μ, σ²)', left+26, H-34);
    p.fill(245,128,37); p.rect(left+140, H-28, 18, 3); p.fill(0); p.text('표본평균 N(μ, σ²/n)', left+168, H-34);
  };
});
</script>
"""
    components.html(html2, height=360)

    # 7) 모수 vs 표본평균(경험) 비교
    st.subheader("📊 모수 vs 표본평균(경험적) 비교")
    sample_means_list = [float(np.mean(s)) for s in samples]
    mean_of_means = float(np.mean(sample_means_list))
    var_of_means = float(np.var(sample_means_list, ddof=1)) if len(sample_means_list) > 1 else float("nan")
    std_of_means = float(np.sqrt(var_of_means)) if np.isfinite(var_of_means) else float("nan")

    comp = pd.DataFrame(
        [
            ["모집단(이론)", pop_mu, pop_var, pop_sigma],
            ["표본평균(이론)", pop_mu, (pop_var)/float(n), pop_sigma/np.sqrt(float(n))],
            ["표본평균(경험)", mean_of_means, var_of_means, std_of_means],
        ],
        columns=["항목", "평균(μ)", "분산(σ²)", "표준편차(σ)"]
    )
    st.dataframe(comp, use_container_width=True, hide_index=True)
    st.caption("- 표본평균의 **이론 분산**은 σ²/n, **이론 표준편차**는 σ/√n 입니다.")
