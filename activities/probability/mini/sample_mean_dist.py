import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from math import sqrt
from typing import List, Dict

PAGE_META = {
    "title": "표본평균의 분포(복원추출)",
    "group": "확률과통계",
    "icon": "🧮",
}

# ---------- 바구니 시각화 ----------
def draw_basket(values: List[int]):
    N = len(values)
    fig = go.Figure()
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 1], scaleanchor="x", scaleratio=1)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10),
                      plot_bgcolor="white", paper_bgcolor="white", height=340)

    bag_x0, bag_x1 = 0.05, 0.95
    bag_y0, bag_y1 = 0.10, 0.90
    fig.add_shape(type="rect", x0=bag_x0, y0=bag_y0, x1=bag_x1, y1=bag_y1,
                  fillcolor="rgba(245,170,110,0.35)",
                  line=dict(color="rgba(120,80,50,0.8)", width=2))
    fig.add_shape(type="rect", x0=bag_x0, y0=0.86, x1=bag_x1, y1=0.92,
                  fillcolor="rgba(200,120,70,0.6)",
                  line=dict(color="rgba(120,80,50,0.8)", width=1))

    cols = 5 if N >= 5 else N
    rows = int(np.ceil(N / max(cols, 1)))
    pad_x, pad_y = 0.02, 0.02
    inner_w = (bag_x1 - bag_x0) - 2 * pad_x
    inner_h = (bag_y1 - bag_y0) - 2 * pad_y
    if rows == 0:
        return fig

    card_w = inner_w / max(cols, 1) * 0.8
    card_h = inner_h / max(rows, 1) * 0.6

    for idx, val in enumerate(values):
        r = idx // max(cols, 1)
        c = idx % max(cols, 1)
        cx = bag_x0 + pad_x + (c + 0.5) * inner_w / max(cols, 1)
        cy = bag_y1 - pad_y - (r + 0.6) * inner_h / max(rows, 1)

        fig.add_shape(type="rect",
                      x0=cx - card_w / 2, x1=cx + card_w / 2,
                      y0=cy - card_h / 2, y1=cy + card_h / 2,
                      fillcolor="white",
                      line=dict(color="rgba(60,60,60,0.6)", width=1.3))
        fig.add_annotation(x=cx, y=cy, text=str(val),
                           showarrow=False, font=dict(size=16, color="#111"))

    fig.add_annotation(x=0.5, y=0.96,
                       text=f"모집단: {values}",
                       showarrow=False, font=dict(size=14, color="#111"))
    return fig

# ---------- 합 분포(정확/근사) ----------
def pmf_sum_via_power(values: List[int], n: int) -> Dict[int, float]:
    """단일 추출 pmf를 다항식으로 보고 n제곱(분할정복) → S_n의 정확 분포."""
    vals = np.array(values, dtype=int)
    m = len(vals)
    minv, maxv = vals.min(), vals.max()
    base_len = maxv - minv + 1
    base = np.zeros(base_len)
    for v in vals:
        base[v - minv] += 1.0 / m

    def poly_conv(a, b):
        c = np.convolve(a, b)
        c[c < 1e-14] = 0.0
        nz = np.nonzero(c)[0]
        if len(nz) == 0:
            return np.zeros(1)
        return c[nz.min(): nz.max() + 1]

    res = np.array([1.0]); shift = 0
    base_poly = base.copy(); base_shift = minv
    k = n
    while k > 0:
        if k & 1:
            res = poly_conv(res, base_poly)
            shift += base_shift
        base_poly = poly_conv(base_poly, base_poly)
        base_shift *= 2
        k >>= 1

    sums = np.arange(shift, shift + len(res))
    pmf = {int(s): float(p) for s, p in zip(sums, res / res.sum())}
    return pmf

def pmf_sum(values: List[int], n: int) -> Dict[int, float]:
    """
    가능하면 항상 '정확' 방법을 사용.
    spread*n이 적정(≤4000)하면 다항식 거듭제곱을 강제하고,
    그 외 극단적 상황만 몬테카를로로 근사.
    """
    spread = max(values) - min(values) if len(values) > 0 else 0
    if spread * n <= 4000:
        return pmf_sum_via_power(values, n)

    # 근사(희귀 합이 누락될 수 있으므로 가능한 한 위 조건을 만족시키도록 안내)
    rng = np.random.default_rng(0)
    trials = min(300_000, 6000 * max(1, n))
    vals = np.array(values)
    sums = rng.choice(vals, size=(trials, n), replace=True).sum(axis=1)
    unique, counts = np.unique(sums, return_counts=True)
    probs = counts / counts.sum()
    return {int(s): float(p) for s, p in zip(unique, probs)}

# ---------- 예시 표본 ----------
def make_examples(values: List[int], n: int, k: int = 5, seed: int = 0):
    rng = np.random.default_rng(seed)
    vals = np.array(values)
    samples, means = [], []
    for _ in range(k):
        s = list(rng.choice(vals, size=n, replace=True))
        samples.append(s)
        means.append(float(np.mean(s)))
    return samples, means

def card_html(v: int) -> str:
    return (f'<div style="display:flex;align-items:center;justify-content:center;'
            f'width:64px;height:84px;margin-right:6px;'
            f'border:1.5px solid rgba(60,60,60,0.5);border-radius:8px;background:white;'
            f'box-shadow:0 2px 6px rgba(0,0,0,0.06);">'
            f'<span style="font-size:22px;font-weight:700;color:#222;">{v}</span></div>')

# ─────────────────────────────
# 🔧 사이드바용 스텝퍼 슬라이더 헬퍼 (± 버튼 + 슬라이더)
# ─────────────────────────────
def sidebar_stepper_slider(label: str, min_value: int, max_value: int, key: str, default: int, step: int = 1) -> int:
    cont = st.sidebar.container()
    cont.caption(label)
    c1, c2, c3 = cont.columns([6, 1, 1], gap="small")

    # 초기화
    if key not in st.session_state:
        st.session_state[key] = default

    # 버튼 먼저 처리(즉시 반영)
    if c2.button("−", key=f"{key}__minus"):
        st.session_state[key] = max(min_value, st.session_state[key] - step)
        st.rerun()
    if c3.button("+", key=f"{key}__plus"):
        st.session_state[key] = min(max_value, st.session_state[key] + step)
        st.rerun()

    # 슬라이더(레이블 숨김)
    val = c1.slider(
        label, min_value=min_value, max_value=max_value,
        value=int(st.session_state[key]), step=step,
        key=f"{key}__slider", label_visibility="collapsed"
    )
    if val != st.session_state[key]:
        st.session_state[key] = int(val)
    return int(st.session_state[key])

# ---------- 메인 ----------
def render():
    st.sidebar.subheader("⚙️ 모집단 & 표본 설정")
    m = st.sidebar.slider("모집단 원소의 개수", 1, 10, 4, step=1)
    default_vals = [2, 4, 6, 8] + [i for i in range(1, 11)]
    defaults = default_vals[:m]
    values = []
    col_num = 2 if m <= 6 else 3
    cols = st.sidebar.columns(col_num)
    for i in range(m):
        with cols[i % col_num]:
            v = st.number_input(f"원소 {i+1}", value=int(defaults[i]), step=1, format="%d")
            values.append(int(v))

    # ✅ 표본 크기 n 슬라이더를 스텝퍼(± 버튼) 있는 버전으로 교체
    n = sidebar_stepper_slider("표본 크기 n (복원추출)", 1, 100, key="sampmean_n", default=2, step=1)

    st.markdown("### 표본평균의 분포(복원추출)")
    st.plotly_chart(draw_basket(values), use_container_width=True)

    # 모집단 모수
    pop_mean = float(np.mean(values))
    pop_var  = float(np.var(values, ddof=0))
    pop_std  = float(np.sqrt(pop_var))
    c1, c2, c3 = st.columns(3)
    c1.metric("모평균 μ", f"{pop_mean:.4f}")
    c2.metric("모분산 σ²", f"{pop_var:.4f}")
    c3.metric("모표준편차 σ", f"{pop_std:.4f}")

    st.divider()

    # 예시 표본 5개
    st.subheader("예시 표본 5개 (복원추출)")
    samples, means = make_examples(values, n, k=5, seed=42)
    for i, (s, mval) in enumerate(zip(samples, means), start=1):
        row = st.columns([6, 1.8])
        with row[0]:
            card_cols = st.columns(len(s))
            for j, val in enumerate(s):
                with card_cols[j]:
                    st.markdown(card_html(val), unsafe_allow_html=True)
        with row[1]:
            st.metric(f"표본평균 {i}", f"{mval:.4f}")

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    st.divider()

    # ===== 표본평균의 분포(가능한 값만, 가로형 표) =====
    st.subheader("표본평균의 분포표")
    pmfS = pmf_sum(values, n)          # S_n의 (정확한) 분포 또는 근사
    pmfS = {s: p for s, p in pmfS.items() if p > 1e-15}  # 수치잡음 제거
    sums_sorted = sorted(pmfS.keys())  # 가능한 합(정수)만 포함됨 → 불가능 평균 자동 배제
    probs_sorted = [pmfS[s] for s in sums_sorted]

    # 가로 테이블: 열이 "s/n (=decimal)"
    means_decimal = [s / n for s in sums_sorted]
    labels = [f"{s}/{n} ({s / n:.4f})" for s in sums_sorted]

    import pandas as pd
    df_row = pd.DataFrame([np.round(probs_sorted, 6)], columns=labels)
    st.dataframe(df_row, use_container_width=True, hide_index=True)

    # 히스토그램
    st.subheader("표본평균 분포 히스토그램")
    df_hist = pd.DataFrame({"mean": means_decimal, "prob": probs_sorted})
    fig = px.bar(df_hist, x="mean", y="prob")
    fig.update_layout(xaxis_title="표본평균", yaxis_title="확률", bargap=0.05)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ===== 모집단 vs 표본평균 비교 =====
    st.subheader("모집단 vs 표본평균 비교")
    mean_bar = pop_mean
    var_bar  = pop_var / n
    std_bar  = sqrt(var_bar)

    left, right = st.columns(2)
    with left:
        st.markdown("**모집단 (원자료 \\(X\\))**")
        st.latex(r"\mu=\mathrm{E}[X]")
        st.metric("값", f"{pop_mean:.6f}")
        st.latex(r"\sigma^2=\mathrm{Var}(X)")
        st.metric("값", f"{pop_var:.6f}")
        st.latex(r"\sigma=\sqrt{\mathrm{Var}(X)}")
        st.metric("값", f"{pop_std:.6f}")

    with right:
        st.markdown("**표본평균 (\\(\overline{X}\\))**")
        st.latex(r"\mathrm{E}[\overline{X}]=\mu")
        st.metric("값", f"{mean_bar:.6f}")
        st.latex(r"\mathrm{Var}(\overline{X})=\dfrac{\sigma^2}{n}")
        st.metric("값", f"{var_bar:.6f}")
        st.latex(r"\mathrm{SD}(\overline{X})=\dfrac{\sigma}{\sqrt{n}}")
        st.metric("값", f"{std_bar:.6f}")

    st.caption("해석: 표본평균은 모평균은 같고, 분산은 σ²/n로 작아져 n이 커질수록 분포가 가운데로 모입니다.")
