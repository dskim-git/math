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
    "title": "모평균과 표본평균의 관계 (p5.js)",
    "description": "구글시트의 모집단에서 표본을 여러 번 추출해 표본평균 분포를 시각화합니다.",
    "order": 50,
}

# ─────────────────────────────────────────────────────────────────────────────
# 유틸: 구글시트 공유 URL → CSV 주소로 정규화
def to_csv_url(url: str, sheet: str = "원본") -> str:
    """
    1) '웹에 게시' CSV 주소는 그대로 사용
    2) /export?format=csv 도 그대로
    3) 공유 /edit 주소는 gid가 있으면 export?format=csv&gid=... 로,
       없으면 gviz/tq?tqx=out:csv&sheet=... (sheet는 URL 인코딩)
    """
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
    # #gid=... (fragment)에서 추출
    m_gid = re.search(r"gid=(\d+)", parsed.fragment or "")
    if m_gid:
        gid = m_gid.group(1)
    # query에도 있을 수 있음
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
    """원본 CSV를 DataFrame으로 로드(숫자열만 따로 선택 가능)."""
    df = pd.read_csv(csv_url)
    df = df.dropna(axis=1, how="all")
    return df

def _guess_numeric_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    숫자열 후보 반환 + 기본 선택 추천.
    - 첫 번째 숫자열이 '반/학급'처럼 범주가 적은 정수열이면 **자동 제외**.
    """
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not num_cols:
        return [], []

    default = num_cols.copy()
    first = num_cols[0]
    s = df[first].dropna()
    looks_class = (
        str(first).strip() in ("반", "학급", "class", "Class")
        or (s.nunique() <= max(30, int(len(s) * 0.1)))  # 범주가 매우 적으면 학급/분반으로 가정
    )
    if looks_class and len(num_cols) >= 2:
        default = num_cols[1:]  # 첫 숫자열 제외
    return num_cols, default

def _draw_samples(values: np.ndarray, n: int, m: int, seed: int) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """values(모집단)에서 크기 n 표본을 m개 생성(복원추출)."""
    rng = np.random.default_rng(seed)
    N = len(values)
    samples = []
    idx_lists = []
    for _ in range(m):
        idx = rng.integers(0, N, size=n)  # 복원추출
        samp = values[idx]
        samples.append(samp)
        idx_lists.append(idx)
    return samples, idx_lists

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.title("모평균과 표본평균의 관계 (p5.js)")

    # 기본 시트(질문에서 주신 주소)
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

    # 사용할 열 선택(숫자열 중)
    num_cols, default_sel = _guess_numeric_columns(df)
    with st.sidebar:
        st.subheader("📊 사용할 열 선택")
        sel_cols = st.multiselect(
            "키(숫자) 데이터가 들어있는 열을 선택하세요.",
            options=num_cols,
            default=default_sel
        )

        st.subheader("🎲 표본 설정")
        n = st.number_input("표본 크기 n", 2, 1000, 30, step=1)
        m = st.number_input("표본 개수 m", 1, 300, 30, step=1)
        seed = st.number_input("난수 시드", 0, 10_000, 0, step=1)
        go = st.button("표본 추출/새로고침")

    if not sel_cols:
        st.warning("숫자 열을 한 개 이상 선택해 주세요. (A열 '반/학급'은 기본 제외됩니다)")
        st.dataframe(df, use_container_width=True)
        return

    # 선택한 열만 펼쳐서 1차원 벡터로
    num_df = df[sel_cols].select_dtypes(include=["number"])
    values = num_df.to_numpy().ravel()
    values = values[~np.isnan(values)].astype(float)

    N = len(values)
    if N == 0:
        st.warning("선택한 열에서 숫자 데이터가 발견되지 않았습니다.")
        st.dataframe(df, use_container_width=True)
        return

    # 1) 모집단의 로우 데이터 보기 (숫자열만)
    st.subheader("📄 모집단 원본 데이터(선택한 숫자 열)")
    st.caption("A열의 '반/학급' 등 범주형 숫자열은 기본으로 제외했으며, 좌측에서 직접 열을 선택할 수 있습니다.")
    st.dataframe(num_df, use_container_width=True, height=300)
    with st.expander("전체 원본 보기"):
        st.dataframe(df, use_container_width=True, height=400)

    # 모집단 기술통계
    pop_mu = float(np.mean(values))
    pop_sigma = float(np.std(values, ddof=0))          # 표준편차 σ
    pop_var = float(pop_sigma ** 2)                    # 분산 σ^2
    st.markdown(
        f"**모집단 크기** N = {N:,}  \n"
        f"**모평균** μ = {pop_mu:.3f} , **모분산** σ² = {pop_var:.3f} (σ = {pop_sigma:.3f})"
    )

    # 2) 3) 표본 추출
    if go:
        st.session_state["smd_samples"], st.session_state["smd_idxlists"] = _draw_samples(values, int(n), int(m), int(seed))

    samples: List[np.ndarray] = st.session_state.get("smd_samples")
    idx_lists: List[np.ndarray] = st.session_state.get("smd_idxlists")

    if not samples:
        # 초기 렌더에서 자동 생성
        samples, idx_lists = _draw_samples(values, int(n), int(m), int(seed))
        st.session_state["smd_samples"] = samples
        st.session_state["smd_idxlists"] = idx_lists

    # 4) 각 표본 표 + 표본 통계
    st.subheader("🧪 표본 표와 요약")
    sample_rows = []
    for i, samp in enumerate(samples, start=1):
        sample_rows.append([i, len(samp), float(np.mean(samp)), float(np.std(samp, ddof=1))])
    summary_df = pd.DataFrame(sample_rows, columns=["표본#", "크기", "표본평균", "표본표준편차"])
    st.dataframe(summary_df, use_container_width=True, height=min(300, 40 + 28 * len(samples)))

    with st.expander("각 표본의 원소 보기(상위 8개 표본만 미리보기)"):
        cap = min(8, len(samples))
        cols = st.columns(2)
        for i in range(cap):
            with cols[i % 2]:
                st.markdown(f"**표본 #{i+1} (n={len(samples[i])})**")
                st.dataframe(pd.DataFrame({"값": samples[i]}), use_container_width=True, height=200)

    # 5) 가로 수직선(모집단) + 선택 표본 강조 (p5.js)
    st.subheader("📍 모집단 가로 수직선에서 표본의 위치(강조)")
    sel_idx = st.selectbox("강조할 표본 선택", options=list(range(len(samples))), format_func=lambda i: f"표본 #{i+1}", index=0)

    vmin, vmax = float(np.min(values)), float(np.max(values))
    payload1 = {
        "values": values.tolist(),
        "sel_indices": [int(x) for x in idx_lists[sel_idx].tolist()],
        "vmin": vmin, "vmax": vmax,
        "title": f"모집단({N}명) 가로 수직선과 표본 #{sel_idx+1} (n={len(samples[sel_idx])})"
    }
    html1 = """
<div id="popline" style="width:100%;max-width:980px;margin:0 auto;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<script>
const DATA1 = """ + json.dumps(payload1) + """;
new p5((p)=>{
  let W=980,H=220, pad=40;
  p.setup=()=>{ p.createCanvas(W,H).parent("popline"); p.noLoop(); p.textFont('sans-serif'); };
  p.draw=()=>{
    p.background(255);
    const yAxis = H*0.6;
    // 축(가로)
    p.stroke(50); p.strokeWeight(2);
    p.line(pad, yAxis, W-pad, yAxis);
    p.noStroke(); p.fill(0); p.textSize(12); p.textAlign(p.CENTER,p.TOP);
    p.text(DATA1.title, W/2, 8);
    p.textAlign(p.LEFT,p.TOP);  p.text(DATA1.vmin.toFixed(2), pad, yAxis+8);
    p.textAlign(p.RIGHT,p.TOP); p.text(DATA1.vmax.toFixed(2), W-pad, yAxis+8);

    const sel = new Set(DATA1.sel_indices);
    // 겹침 완화: 약간의 수직 난수 지터
    for (let i=0;i<DATA1.values.length;i++){
      const v = DATA1.values[i];
      const x = p.map(v, DATA1.vmin, DATA1.vmax, pad, W-pad);
      const jitter = (Math.random()-0.5)*8;
      if(sel.has(i)){ p.fill(230,49,70); p.circle(x, yAxis+jitter, 7); }
      else          { p.fill(160);       p.circle(x, yAxis+jitter, 5); }
    }
  };
});
</script>
"""
    components.html(html1, height=240)

    # 6) 정규곡선(모집단 vs 표본평균) + 표본평균 점 (p5.js)
    st.subheader("📈 정규곡선: 모집단 N(μ, σ²) vs 표본평균 N(μ, σ²/n)")
    sample_means = [float(np.mean(s)) for s in samples]
    highlight = float(np.mean(samples[sel_idx]))

    theo_sigma = pop_sigma / np.sqrt(float(n))  # 표본평균의 표준편차
    payload2 = {
        "mu_pop": pop_mu, "sd_pop": pop_sigma,
        "mu_bar": pop_mu, "sd_bar": theo_sigma,
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

    // x범위 & y최댓값
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

    # 7) 모수 vs 표본평균(경험적) 비교
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

    st.caption(
        "- 표본평균의 **이론 분산**은 σ²/n, **이론 표준편차**는 σ/√n 입니다.  \n"
        "- ‘경험’ 값은 방금 만든 m개의 표본평균으로 계산한 결과입니다."
    )
