# activities/probability/binomial_galton_board.py
import time
from math import comb
from typing import Optional

import numpy as np
import plotly.graph_objects as go
import streamlit as st

META = {
    "title": "갈톤보드(이항분포) 시뮬레이터",
    "description": "핀을 통과하며 좌/우로 움직이는 공을 모사해 막대그래프가 이항분포로 수렴하는 모습을 봅니다.",
    "order": 20,
}

def _binom_counts(n_rows: int, n_balls: int, p: float, seed: Optional[int] = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    # 각 공이 오른쪽으로 간 횟수 ~ Binomial(n_rows, p)
    rights = rng.binomial(n_rows, p, size=n_balls)
    # 슬롯 인덱스 = rights (0..n_rows)
    counts = np.bincount(rights, minlength=n_rows + 1)
    return counts

def _binom_theory(n_rows: int, p: float, total: int) -> np.ndarray:
    k = np.arange(n_rows + 1)
    pmf = np.array([comb(n_rows, int(i)) * (p ** i) * ((1 - p) ** (n_rows - i)) for i in k], dtype=float)
    return pmf * total  # 총 공 개수에 맞게 스케일

def _plot_hist_with_theory(counts: np.ndarray, theory: np.ndarray, p: float) -> go.Figure:
    n_rows = len(counts) - 1
    x = np.arange(n_rows + 1)
    fig = go.Figure()
    fig.add_bar(x=x, y=counts, name="실험(슬롯별 개수)", opacity=0.75)
    fig.add_scatter(x=x, y=theory, mode="lines", name="이론(이항분포)", line=dict(width=2))
    fig.update_layout(
        xaxis_title="오른쪽으로 간 횟수 (슬롯 인덱스)",
        yaxis_title="개수",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_xaxes(dtick=1)
    return fig

def render():
    st.header("🧪 갈톤보드(이항분포) 시뮬레이터")

    with st.expander("설명", expanded=False):
        st.write(
            "- 공이 핀을 **n**번 통과할 때, 각 핀에서 오른쪽으로 갈 확률을 **p**라 두면\n"
            "  오른쪽으로 간 총 횟수 **K**는 `K ~ Binomial(n, p)`을 따릅니다.\n"
            "- 아래 그래프에서 막대는 **실험 결과**, 선은 **이론값**(이항분포)입니다."
        )
        st.latex(r"P(K=k)=\binom{n}{k}p^k(1-p)^{n-k}")

    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1])
    with c1:
        n_rows = st.slider("핀(충돌) 횟수 n", 3, 20, 12, 1)
    with c2:
        n_balls = st.slider("공의 개수", 50, 50_000, 5_000, step=50)
    with c3:
        p = st.slider("오른쪽으로 갈 확률 p", 0.0, 1.0, 0.5, 0.01)
    with c4:
        seed_opt = st.text_input("시드(선택)", value="", help="재현 가능한 결과가 필요하면 숫자를 입력하세요.")
        seed = None
        if seed_opt.strip():
            try:
                seed = int(seed_opt)
            except Exception:
                st.warning("시드는 정수만 입력하세요. (빈칸이면 무작위)")

    run_col, step_col, clear_col = st.columns([1, 1, 1])
    placeholder = st.empty()

    if "gb_counts" not in st.session_state:
        st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
        st.session_state["gb_total"] = 0
        st.session_state["gb_n_rows"] = n_rows

    def _reset_state():
        st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
        st.session_state["gb_total"] = 0
        st.session_state["gb_n_rows"] = n_rows

    # n_rows 변경 시 상태도 맞춰 초기화
    if st.session_state.get("gb_n_rows") != n_rows:
        _reset_state()

    with run_col:
        if st.button("▶ 한 번에 실행"):
            counts = _binom_counts(n_rows, n_balls, p, seed)
            st.session_state["gb_counts"] = counts
            st.session_state["gb_total"] = int(counts.sum())
    with step_col:
        if st.button("⏩ 점점 늘리기(애니)"):
            _reset_state()
            batch = max(50, n_balls // 50)
            done = 0
            while done < n_balls:
                this = min(batch, n_balls - done)
                counts = _binom_counts(n_rows, this, p, None if seed is None else seed + done)
                st.session_state["gb_counts"] += counts
                st.session_state["gb_total"] += int(counts.sum())
                theory = _binom_theory(n_rows, p, st.session_state["gb_total"])
                fig = _plot_hist_with_theory(st.session_state["gb_counts"], theory, p)
                placeholder.plotly_chart(fig, use_container_width=True)
                done += this
                time.sleep(0.03)
    with clear_col:
        if st.button("🧹 초기화"):
            _reset_state()

    # 최종 그래프
    total_now = st.session_state["gb_total"]
    if total_now == 0:
        counts = _binom_counts(n_rows, 1, p, seed) * 0  # 빈 그래프용
        theory = _binom_theory(n_rows, p, 1) * 0
    else:
        counts = st.session_state["gb_counts"]
        theory = _binom_theory(n_rows, p, total_now)

    fig = _plot_hist_with_theory(counts, theory, p)
    placeholder.plotly_chart(fig, use_container_width=True)

    # 요약
    k = np.arange(n_rows + 1)
    mean_emp = (k * counts).sum() / max(1, total_now)
    var_emp = (((k - mean_emp) ** 2) * counts).sum() / max(1, total_now)
    st.caption(
        f"실험 개수: **{total_now:,}** · 경험적 평균 **{mean_emp:.3f}** / 분산 **{var_emp:.3f}**  "
        f"· 이론 평균 **{n_rows * p:.3f}** / 이론 분산 **{n_rows * p * (1 - p):.3f}**"
    )
