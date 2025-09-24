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
    사용자가 보통 복사해 오는 형태들을 모두 CSV 주소로 바꿔줍니다.

    1) '파일 > 웹에 게시' 주소(이미 CSV):
       https://docs.google.com/spreadsheets/d/e/2P.../pub?gid=0&single=true&output=csv
       → 그대로 사용

    2) 상단 공유 URL(문서 화면의 /edit 주소):
       https://docs.google.com/spreadsheets/d/<ID>/edit#gid=123456789
       → gid가 있으면: https://docs.google.com/spreadsheets/d/<ID>/export?format=csv&gid=<gid>
       → gid가 없으면: https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&sheet=<sheet 인코딩>

    3) export 형식(/export?format=csv ...):
       → 그대로 사용
    """
    s = (url or "").strip()
    if not s:
        return s

    # 이미 CSV export/gviz면 그대로 사용
    sl = s.lower()
    if ("output=csv" in sl) or ("/export?format=csv" in sl) or ("/gviz/tq?tqx=out:csv" in sl):
        return s

    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", s)
    if not m:
        return s
    doc_id = m.group(1)

    # gid가 있으면 export?format=csv&gid=... 사용 (탭명이 한글이어도 안전)
    parsed = urlparse(s)
    # google 링크는 '#gid=...' 형태가 많아 fragment에도 gid가 들어있을 수 있음
    gid = None
    # fragment에서 gid 추출
    frag = parsed.fragment or ""
    m_gid = re.search(r"gid=(\d+)", frag)
    if m_gid:
        gid = m_gid.group(1)
    # query에도 있을 수 있음
    if not gid:
        qs = parse_qs(parsed.query or "")
        if "gid" in qs and len(qs["gid"]) > 0:
            gid = qs["gid"][0]

    if gid:
        return f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={gid}"

    # gid가 없으면 gviz + sheet 사용 (sheet는 반드시 퍼센트 인코딩!)
    sheet_enc = quote(sheet, safe="")
    return f"https://docs.google.com/spreadsheets/d/{doc_id}/gviz/tq?tqx=out:csv&sheet={sheet_enc}"

# ─────────────────────────────────────────────────────────────────────────────
def _load_population(csv_url: str) -> Tuple[pd.DataFrame, np.ndarray]:
    """구글시트 CSV를 읽어 원본 DF와 '키' 값 1차원 배열을 반환."""
    # 구글시트 CSV는 UTF-8이므로 기본 read_csv로 충분
    df = pd.read_csv(csv_url)
    # 완전 빈 열 제거
    df = df.dropna(axis=1, how="all")

    # 숫자 열만 모아 하나의 벡터로
    num = df.select_dtypes(include=["number"])
    values = num.to_numpy().ravel()
    values = values[~np.isnan(values)]
    values = values.astype(float)

    return df, values

def _draw_samples(values: np.ndarray, n: int, m: int, seed: int) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    values(모집단)에서 크기 n 표본을 m개 생성(복원추출).
    반환: (표본값 배열 리스트, 표본 '원본 인덱스' 배열 리스트)
    """
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

    # 기본 시트(질문에서 주신 주소). 필요시 직접 입력/수정 가능하도록 인풋 제공.
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

        st.subheader("🎲 표본 설정")
        n = st.number_input("표본 크기 n", 2, 1000, 30, step=1)
        m = st.number_input("표본 개수 m", 1, 300, 30, step=1)
        seed = st.number_input("난수 시드", 0, 10_000, 0, step=1)
        go = st.button("표본 추출/새로고침")

    if not csv_url:
        st.info("좌측에 구글시트 주소를 입력하세요.")
        return

    # 모집단 로드
    try:
        df, values = _load_population(csv_url)
    except Exception as e:
        st.error(f"모집단 데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return

    N = len(values)
    if N == 0:
        st.warning("숫자 데이터가 발견되지 않았습니다. 시트의 '원본' 탭에 숫자(키) 데이터가 있는지 확인하세요.")
        st.dataframe(df, use_container_width=True)
        return

    # 1) 모집단의 로우 데이터 보기
    st.subheader("📄 모집단 원본 데이터(숫자 열)")
    st.caption("아래 표는 CSV의 숫자 열만 모아서 보여줍니다. 전체 원본은 ‘전체 원본 보기’를 펼치세요.")
    st.dataframe(df.select_dtypes("number"), use_container_width=True, height=300)
    with st.expander("전체 원본 보기"):
        st.dataframe(df, use_container_width=True, height=400)

    # 모집단 기술통계
    pop_mu = float(np.mean(values))
    pop_sigma = float(np.std(values, ddof=0))
    st.markdown(
        f"**모집단 크기** N = {N:,}  \n"
        f"**모평균** μ = {pop_mu:.3f} , **모표준편차** σ = {pop_sigma:.3f}"
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

    # 5) 수직선(모집단) + 선택 표본 강조 (p5.js)
    st.subheader("📍 모집단 수직선에서 표본의 위치(강조)")
    sel_idx = st.selectbox("강조할 표본 선택", options=list(range(len(samples))), format_func=lambda i: f"표본 #{i+1}", index=0)

    vmin, vmax = float(np.min(values)), float(np.max(values))
    payload1 = {
        "values": values.tolist(),
        "sel_indices": [int(x) for x in idx_lists[sel_idx].tolist()],
        "vmin": vmin, "vmax": vmax,
        "title": f"모집단({N}명) 수직선과 표본 #{sel_idx+1} (n={len(samples[sel_idx])})"
    }
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
    const leftX = W*0.15;
    // axis
    p.stroke(50); p.strokeWeight(2);
    p.line(leftX, pad, leftX, H-pad);
    p.noStroke(); p.fill(0); p.textSize(13);
    p.textAlign(p.RIGHT,p.CENTER);
    p.text(DATA1.vmax.toFixed(2), leftX-6, pad);
    p.text(DATA1.vmin.toFixed(2), leftX-6, H-pad);
    p.textAlign(p.LEFT,p.TOP);
    p.text(DATA1.title, W*0.18, 8);

    const sel = new Set(DATA1.sel_indices);
    for (let i=0;i<DATA1.values.length;i++){
      const v = DATA1.values[i];
      const y = p.map(v, DATA1.vmax, DATA1.vmin, pad, H-pad);
      if(sel.has(i)){ p.fill(230,49,70); p.circle(leftX, y, 7); }
      else          { p.fill(160);       p.circle(leftX, y, 5); }
    }
  };
});
</script>
"""
    components.html(html1, height=280)

    # 6) 정규곡선(모집단 vs 표본평균) + 표본평균 점 (p5.js)
    st.subheader("📈 정규곡선: 모집단 N(μ,σ) vs 표본평균 N(μ, σ/√n)")
    sample_means = [float(np.mean(s)) for s in samples]
    highlight = float(np.mean(samples[sel_idx]))

    theo_sigma = pop_sigma / np.sqrt(float(n))
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

    // 모집단 곡선(파랑)
    p.noFill(); p.stroke(35,102,235); p.strokeWeight(2); p.beginShape();
    for(let i=0;i<600;i++){ const x=xmin+(xmax-xmin)*i/599; p.vertex(X(x), Y(pdf(x,mu,sd))); } p.endShape();

    // 표본평균 곡선(주황)
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
    p.fill(35,102,235); p.rect(left, H-28, 18, 3); p.fill(0); p.text('모집단 N(μ,σ)', left+26, H-34);
    p.fill(245,128,37); p.rect(left+140, H-28, 18, 3); p.fill(0); p.text('표본평균 N(μ,σ/√n)', left+168, H-34);
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
            ["모집단(이론)", pop_mu, pop_sigma**2, pop_sigma],
            ["표본평균(이론)", pop_mu, (pop_sigma**2)/float(n), pop_sigma/np.sqrt(float(n))],
            ["표본평균(경험)", mean_of_means, var_of_means, std_of_means],
        ],
        columns=["항목", "평균", "분산", "표준편차"]
    )
    st.dataframe(comp, use_container_width=True, hide_index=True)

    st.caption(
        "- 표본평균의 이론 분산은 σ²/n, 표준편차는 σ/√n 입니다.  \n"
        "- ‘경험’ 값은 방금 만든 m개의 표본평균으로 계산한 결과입니다."
    )
