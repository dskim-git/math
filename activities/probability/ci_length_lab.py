# activities/probability/ci_length_lab.py
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import norm, t

META = {
    "title": "신뢰구간 길이 실험실 (모분산·표본크기·신뢰도의 영향)",
    "description": "가상 모집단을 만들고 표본을 여러 번 뽑아 평균의 신뢰구간을 그리며, 길이가 세 요인에 따라 어떻게 변하는지 확인합니다.",
    "order": 56,
}

# ─────────────────────────────────────────────────────────────────────────────
def _sample_intervals(pop: np.ndarray, m: int, n: int, conf: float, known_sigma: bool, sigma: float, seed: int):
    """표본 m개를 뽑아 평균의 신뢰구간(lo, hi), 길이, 포함여부를 반환."""
    rng = np.random.default_rng(seed)
    mu = float(np.mean(pop))
    rows = []
    for _ in range(m):
        x = rng.choice(pop, size=n, replace=True)
        xbar = float(np.mean(x))
        if known_sigma:
            z = norm.ppf(1 - (1 - conf) / 2.0)
            half = z * sigma / np.sqrt(n)
        else:
            s = float(np.std(x, ddof=1))
            crit = t.ppf(1 - (1 - conf) / 2.0, df=n - 1)
            half = crit * s / np.sqrt(n)
        lo, hi = xbar - half, xbar + half
        rows.append((lo, hi, hi - lo, (lo <= mu <= hi), xbar))
    return pd.DataFrame(rows, columns=["lo", "hi", "length", "contains", "xbar"]), mu

def _theory_length(conf: float, n: int, sigma: float, known_sigma: bool):
    """이론(또는 근사) 길이. 모분산 알려짐: 2*z*σ/√n, 모분산 미지: 2*t_{n-1}*σ/√n (σ→대푯값 근사)."""
    alpha = 1 - conf
    if known_sigma:
        crit = norm.ppf(1 - alpha/2)
    else:
        crit = t.ppf(1 - alpha/2, df=max(n-1, 1))
    return float(2.0 * crit * sigma / np.sqrt(n))

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.title("신뢰구간 길이 실험실")

    # ── 사이드바 설정
    with st.sidebar:
        st.subheader("⚙️ 가상 모집단")
        mu = st.number_input("모평균 μ", -100.0, 100.0, 170.0, step=0.5)
        sigma = st.number_input("모표준편차 σ", 0.1, 50.0, 6.0, step=0.1)
        N = st.slider("모집단 크기(표본추출용)", 1_000, 100_000, 20_000, step=1_000)

        st.subheader("🎯 신뢰구간 설정")
        known_sigma = st.toggle("모분산(σ) **알려짐** 가정 사용", value=False, help="끄면 표본표준편차와 t-분포를 사용합니다.")
        n = st.slider("표본 크기 n", 2, 500, 30)
        conf_pct = st.slider("신뢰도(%)", 50, 99, 95)
        conf = conf_pct / 100.0
        m = st.slider("표본 세트 수 m", 10, 300, 100, step=10)
        seed = st.number_input("난수 시드", 0, 9999, 0, step=1)
        run = st.button("표본 뽑고 신뢰구간 그리기", use_container_width=True)

    # ── 가상 모집단 생성
    rng = np.random.default_rng(seed)
    population = rng.normal(loc=mu, scale=sigma, size=N).astype(float)

    # ── 표본 추출 & 신뢰구간
    if run or ("_ci_lab_df" not in st.session_state):
        df, true_mu = _sample_intervals(population, m=m, n=n, conf=conf, known_sigma=known_sigma, sigma=sigma, seed=seed)
        st.session_state["_ci_lab_df"] = df
        st.session_state["_ci_lab_mu"] = true_mu
    else:
        df = st.session_state["_ci_lab_df"]
        true_mu = st.session_state["_ci_lab_mu"]

    # ── 상단 요약
    contain_rate = df["contains"].mean()
    mean_len = df["length"].mean()
    theo_len = _theory_length(conf, n, sigma, known_sigma)
    colOK = "#23a559" if abs(contain_rate - conf) < 0.05 else "#e33c3c"
    st.markdown(
        f"""
<div style="padding:12px 16px; border-radius:12px; border:1px solid rgba(0,0,0,.08);
            background:linear-gradient(180deg,rgba(248,250,255,.95),rgba(240,248,255,.9));">
  <b>포함 비율</b>: <span style="color:{colOK}; font-weight:800;">{contain_rate*100:.1f}%</span>
  &nbsp;|&nbsp; <b>평균 길이</b>: <b>{mean_len:.3f}</b>
  &nbsp;|&nbsp; <b>이론 길이</b> (기대값): <b>{theo_len:.3f}</b>
  <div style="opacity:.7; margin-top:6px;">
    길이 공식: {r"$\;2\\,z_{1-\\alpha/2}\\,\\sigma/\\sqrt{n}$" if known_sigma else r"$\;2\\,t_{1-\\alpha/2,n-1}\\,\\hat\\sigma/\\sqrt{n}$"}  
    (여기서는 이론 비교를 위해 σ 또는 표본 σ의 대표값으로 근사)
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── ① p5.js로 100개(또는 m개) 신뢰구간 그리드
    st.subheader("① 표본들의 평균 신뢰구간(수평선)과 모평균(수직선)")
    payload = {
        "intervals": [{"lo": float(a), "hi": float(b), "ok": bool(c), "xbar": float(x)}
                      for a, b, c, x in zip(df["lo"], df["hi"], df["contains"], df["xbar"])],
        "mu": float(true_mu),
        "xmin": float(min(df["lo"].min(), true_mu) - sigma*1.5),
        "xmax": float(max(df["hi"].max(), true_mu) + sigma*1.5),
        "title": f"신뢰도 {conf_pct}%  |  n={n},  σ={sigma:.2f}  |  포함 {contain_rate*100:.1f}%",
    }
    row_h = 10
    H = max(380, min(1200, 60 + row_h * len(payload["intervals"]) + 70))
    html = """
<div id="ci_len_canvas" style="width:100%%;max-width:980px;margin:0 auto;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<script>
const DATA = %s;
new p5((p)=>{
  const W=980, padL=60, padR=30, padT=20, padB=45, rowH=%d;
  const N = DATA.intervals.length;
  const H = %d;
  function X(v){ return p.map(v, DATA.xmin, DATA.xmax, padL, W-padR); }

  p.setup = ()=>{ p.createCanvas(W,H).parent("ci_len_canvas"); p.noLoop(); p.textFont('sans-serif'); };
  p.draw = ()=>{
    p.background(255);
    p.fill(0); p.textSize(12); p.noStroke();
    p.textAlign(p.LEFT,p.TOP); p.text(DATA.title, padL, 6);

    const yAxis = H - padB;
    p.stroke(0); p.strokeWeight(1); p.line(padL, yAxis, W-padR, yAxis);
    p.textAlign(p.CENTER,p.TOP); p.noStroke(); p.fill(60);
    for(let i=0;i<=5;i++){ const v=DATA.xmin+(DATA.xmax-DATA.xmin)*i/5; const x=X(v);
      p.stroke(190); p.line(x, yAxis-5, x, yAxis+5); p.noStroke(); p.text(v.toFixed(1), x, yAxis+8); }

    const xmu = X(DATA.mu);
    p.stroke(35,102,235); p.strokeWeight(2); p.line(xmu, padT+8, xmu, yAxis-14);
    p.noStroke(); p.fill(35,102,235); p.textAlign(p.CENTER,p.BOTTOM); p.text('μ', xmu, padT+12);

    const startY = 40;
    for(let i=0;i<N;i++){
      const it = DATA.intervals[i], y = startY + i*rowH + 3;
      const x1=X(it.lo), x2=X(it.hi), xm=X(it.xbar);
      p.stroke(235); p.line(padL, y, W-padR, y);
      if(it.ok){ p.stroke(0,160,90); } else { p.stroke(230,60,60); }
      p.strokeWeight(3); p.line(x1, y, x2, y);
      p.noStroke(); p.fill(0,0,0,120); p.circle(xm, y, 4);
    }
  };
});
</script>
""" % (json.dumps(payload), row_h, H)
    components.html(html, height=H)

    # ── ② 길이 분포(히스토그램) + 이론 길이 마커
    st.subheader("② 신뢰구간 길이 분포")
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        fig = px.histogram(df, x="length", nbins=25, title="신뢰구간 길이 히스토그램")
        fig.add_vline(x=theo_len, line_width=2, line_dash="dash", line_color="royalblue",
                      annotation_text="이론 길이", annotation_position="top right")
        fig.add_vline(x=mean_len, line_width=2, line_color="seagreen",
                      annotation_text="표본 평균 길이", annotation_position="top left")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.line_chart(df["length"])

    # ── ③ 요인별 길이 변화 곡선 (n / σ / 신뢰도)
    st.subheader("③ 세 요인에 따른 이론 길이 변화(다른 값 고정)")
    try:
        import plotly.graph_objects as go
        cols = st.columns(3)
        # n 효과
        with cols[0]:
            n_grid = np.arange(2, max(3, n*2+10))
            y = [_theory_length(conf, int(k), sigma, known_sigma) for k in n_grid]
            st.plotly_chart(go.Figure(data=[go.Scatter(x=n_grid, y=y, mode="lines")])
                            .update_layout(title="n(표본크기) ↑ → 길이 ↓", xaxis_title="n", yaxis_title="길이"),
                            use_container_width=True)
        # sigma 효과
        with cols[1]:
            s_grid = np.linspace(max(0.2, sigma*0.3), sigma*2.0, 80)
            y = [_theory_length(conf, n, float(s), known_sigma) for s in s_grid]
            st.plotly_chart(go.Figure(data=[go.Scatter(x=s_grid, y=y, mode="lines")])
                            .update_layout(title="σ(모표준편차) ↑ → 길이 ↑", xaxis_title="σ", yaxis_title="길이"),
                            use_container_width=True)
        # 신뢰도 효과
        with cols[2]:
            c_grid = np.linspace(0.60, 0.99, 120)
            y = [_theory_length(float(c), n, sigma, known_sigma) for c in c_grid]
            st.plotly_chart(go.Figure(data=[go.Scatter(x=c_grid*100, y=y, mode="lines")])
                            .update_layout(title="신뢰도 ↑ → 길이 ↑", xaxis_title="신뢰도(%)", yaxis_title="길이"),
                            use_container_width=True)
    except Exception:
        st.info("Plotly가 없으면 선 그래프 대신 수치를 위에서 확인하세요.")

    # ── ④ 개념 요약
    with st.expander("📘 수업용 메모: 길이를 좌우하는 세 요인", expanded=False):
        st.markdown(
            r"""
- (모분산 **알려짐**) 평균의 신뢰구간 길이  
  \[
    L = 2\,z_{1-\alpha/2}\,\frac{\sigma}{\sqrt{n}}
  \]
- (모분산 **미지**) 보통
  \[
    L \approx 2\,t_{1-\alpha/2,n-1}\,\frac{s}{\sqrt{n}}
  \]
  를 사용합니다. \(s\)는 표본표준편차. 표본마다 달라지므로 길이도 약간씩 달라집니다.
- **요약**  
  ① \(n\)이 커질수록 \(\frac{1}{\sqrt{n}}\) 때문에 길이는 **짧아집니다**.  
  ② \(\sigma\)가 클수록 길이는 **길어집니다**.  
  ③ 신뢰도(=포함 확률)를 높일수록 임계값이 커져 길이가 **길어집니다**.
"""
        )
