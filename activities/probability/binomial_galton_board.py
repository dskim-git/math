# activities/probability/binomial_galton_board.py
import time
from math import comb
from typing import Optional

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

META = {
    "title": "갈톤보드(이항분포) 시뮬레이터",
    "description": "핀을 통과하며 좌/우로 움직이는 공을 모사해 막대그래프가 이항분포로 수렴하는 모습을 봅니다. (실시간 경로 보기 지원)",
    "order": 20,
}

# ─────────────────────────────────────────────────────────────────────────────
# 공통 유틸
def _binom_counts(n_rows: int, n_balls: int, p: float, seed: Optional[int] = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    rights = rng.binomial(n_rows, p, size=n_balls)
    return np.bincount(rights, minlength=n_rows + 1)

def _binom_theory(n_rows: int, p: float, total: int) -> np.ndarray:
    k = np.arange(n_rows + 1)
    pmf = np.array([comb(n_rows, int(i)) * (p ** i) * ((1 - p) ** (n_rows - i)) for i in k], dtype=float)
    return pmf * total

def _plot_hist_with_theory(counts: np.ndarray, theory: np.ndarray) -> go.Figure:
    n_rows = len(counts) - 1
    x = np.arange(n_rows + 1)
    fig = go.Figure()
    fig.add_bar(x=x, y=counts, name="실험(슬롯별 개수)", opacity=0.8)
    fig.add_scatter(x=x, y=theory, mode="lines", name="이론(이항분포)", line=dict(width=2))
    fig.update_layout(
        xaxis_title="오른쪽으로 간 횟수 (슬롯 인덱스)",
        yaxis_title="개수",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_xaxes(dtick=1)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# 실시간(경로) 전용: 보드/핀 좌표, 프레임 렌더링
def _peg_xy(n_rows: int):
    """삼각격자 핀 좌표 (x=j-r/2, y=r)"""
    xs, ys = [], []
    for r in range(n_rows):
        for j in range(r + 1):
            xs.append(j - r / 2.0)
            ys.append(r)
    return np.array(xs), np.array(ys)

def _ball_xy_at_step(row_r: int, rights_so_far: int) -> tuple[float, float]:
    """해당 단계에서 공 위치 (핀 격자 좌표계)"""
    x = rights_so_far - row_r / 2.0
    y = row_r
    return x, y

def _make_live_figure(n_rows: int, ball_pos: Optional[tuple[float, float]],
                      counts: np.ndarray) -> go.Figure:
    """좌측: 핀 + 공 / 우측: 누적 히스토그램"""
    peg_x, peg_y = _peg_xy(n_rows)
    x_range = (-n_rows / 2 - 1, n_rows / 2 + 1)
    y_range = (-0.8, n_rows + 0.8)

    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.60, 0.40],
        specs=[[{"type": "scatter"}, {"type": "bar"}]],
        horizontal_spacing=0.10,
    )

    # 왼쪽: 핀
    fig.add_trace(
        go.Scatter(
            x=peg_x, y=peg_y, mode="markers",
            marker=dict(size=8, color="lightgray"),
            name="핀",
            showlegend=False,
        ),
        row=1, col=1,
    )

    # 왼쪽: 공
    if ball_pos is not None:
        bx, by = ball_pos
        fig.add_trace(
            go.Scatter(
                x=[bx], y=[by], mode="markers",
                marker=dict(size=14, color="crimson"),
                name="공",
                showlegend=False,
            ),
            row=1, col=1,
        )

    fig.update_xaxes(range=x_range, row=1, col=1, zeroline=False)
    fig.update_yaxes(range=y_range, row=1, col=1, zeroline=False, scaleanchor="x", scaleratio=1)

    # 오른쪽: 히스토그램
    x = np.arange(n_rows + 1)
    fig.add_trace(
        go.Bar(x=x, y=counts, name="누적", opacity=0.85),
        row=1, col=2,
    )
    fig.update_xaxes(title_text="슬롯(오른쪽 횟수)", dtick=1, row=1, col=2)
    fig.update_yaxes(title_text="개수", row=1, col=2)

    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# 실시간 엔진 (한 프레임씩 전진 → 다음 프레임 자동 rerun)
def _live_init(n_rows: int, n_balls: int, p: float, seed: Optional[int]):
    rng = np.random.default_rng(seed)
    # 미리 모든 경로를 생성(리런 간 일관성 확보)
    moves = rng.binomial(1, p, size=(n_balls, n_rows)).astype(np.int8)  # 1=오른쪽, 0=왼쪽
    st.session_state["gb_live"] = dict(
        running=True,
        n_rows=n_rows,
        n_balls=n_balls,
        p=float(p),
        interval_ms=60,
        moves=moves,
        ball_i=0,
        row_r=0,
        rights=0,
        counts=np.zeros(n_rows + 1, dtype=int),
        total=0,
    )

def _live_tick():
    S = st.session_state.get("gb_live")
    if not S or not S.get("running", False):
        return

    n_rows = S["n_rows"]
    n_balls = S["n_balls"]
    moves = S["moves"]

    # 아직 남은 공?
    if S["ball_i"] >= n_balls:
        S["running"] = False
        return

    # 현재 공이 아직 떨어지는 중 → 다음 핀으로 한 칸
    if S["row_r"] < n_rows:
        step = int(moves[S["ball_i"], S["row_r"]])  # 1 or 0
        S["rights"] += step
        S["row_r"] += 1
    else:
        # 바닥 도착 → 슬롯 기록, 다음 공으로 전환
        S["counts"][S["rights"]] += 1
        S["total"] += 1
        S["ball_i"] += 1
        S["row_r"] = 0
        S["rights"] = 0

def render():
    st.header("🧪 갈톤보드(이항분포) 시뮬레이터")

    tab_fast, tab_live = st.tabs(["누적(빠름)", "실시간(경로)"])

    # ────────────────────────────────────────────────────────────────────
    # 1) 누적(빠름)
    with tab_fast:
        with st.expander("설명", expanded=False):
            st.write(
                "- 공이 핀을 **n**번 통과, 각 핀에서 오른쪽으로 갈 확률 **p**일 때\n"
                "  오른쪽으로 간 총 횟수 **K**는 `K ~ Binomial(n,p)`입니다."
            )
            st.latex(r"P(K=k)=\binom{n}{k}p^k(1-p)^{n-k}")

        c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1])
        with c1:
            n_rows = st.slider("핀(충돌) 횟수 n", 3, 20, 12, 1, key="gb_fast_n")
        with c2:
            n_balls = st.slider("공의 개수", 50, 50_000, 5_000, step=50, key="gb_fast_b")
        with c3:
            p = st.slider("오른쪽 확률 p", 0.0, 1.0, 0.5, 0.01, key="gb_fast_p")
        with c4:
            seed_text = st.text_input("시드(선택)", value="", key="gb_fast_seed")
            seed = int(seed_text) if seed_text.strip().isdigit() else None

        # 상태: 누적 결과 유지
        if "gb_counts" not in st.session_state:
            st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
            st.session_state["gb_total"] = 0
            st.session_state["gb_n_rows"] = n_rows

        def _reset_fast():
            st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
            st.session_state["gb_total"] = 0
            st.session_state["gb_n_rows"] = n_rows

        # 행 수 바뀌면 리셋
        if st.session_state.get("gb_n_rows") != n_rows:
            _reset_fast()

        run_col, step_col, clear_col = st.columns([1, 1, 1])
        placeholder = st.empty()

        with run_col:
            if st.button("▶ 한 번에 실행", key="gb_fast_run"):
                counts = _binom_counts(n_rows, n_balls, p, seed)
                st.session_state["gb_counts"] = counts
                st.session_state["gb_total"] = int(counts.sum())

        with step_col:
            if st.button("⏩ 점점 늘리기(애니)", key="gb_fast_anim"):
                _reset_fast()
                batch = max(50, n_balls // 50)
                done = 0
                while done < n_balls:
                    this = min(batch, n_balls - done)
                    counts = _binom_counts(n_rows, this, p, None if seed is None else seed + done)
                    st.session_state["gb_counts"] += counts
                    st.session_state["gb_total"] += int(counts.sum())
                    theory = _binom_theory(n_rows, p, st.session_state["gb_total"])
                    fig = _plot_hist_with_theory(st.session_state["gb_counts"], theory)
                    placeholder.plotly_chart(fig, use_container_width=True)
                    done += this
                    time.sleep(0.03)

        with clear_col:
            if st.button("🧹 초기화", key="gb_fast_clear"):
                _reset_fast()

        total_now = st.session_state["gb_total"]
        if total_now == 0:
            counts = np.zeros(n_rows + 1, dtype=int)
            theory = np.zeros(n_rows + 1, dtype=float)
        else:
            counts = st.session_state["gb_counts"]
            theory = _binom_theory(n_rows, p, total_now)

        fig = _plot_hist_with_theory(counts, theory)
        placeholder.plotly_chart(fig, use_container_width=True)

        # 요약
        k = np.arange(n_rows + 1)
        mean_emp = (k * counts).sum() / max(1, total_now)
        var_emp = (((k - mean_emp) ** 2) * counts).sum() / max(1, total_now)
        st.caption(
            f"실험 개수: **{total_now:,}** · 경험적 평균 **{mean_emp:.3f}** / 분산 **{var_emp:.3f}**  "
            f"· 이론 평균 **{n_rows * p:.3f}** / 이론 분산 **{n_rows * p * (1 - p):.3f}**"
        )

    # ────────────────────────────────────────────────────────────────────
    # 2) 실시간(경로)
    with tab_live:
        lc1, lc2, lc3 = st.columns([1.2, 1.2, 1.2])
        with lc1:
            n_rows_l = st.slider("핀(충돌) 횟수 n (실시간)", 3, 15, 10, 1, key="gb_live_n")
        with lc2:
            n_balls_l = st.slider("공의 개수(실시간)", 10, 800, 200, 10, key="gb_live_b")
        with lc3:
            p_l = st.slider("오른쪽 확률 p", 0.0, 1.0, 0.5, 0.01, key="gb_live_p")

        colA, colB, colC, colD = st.columns([1, 1, 1, 1])
        with colA:
            start = st.button("▶ 실시간 시작", key="gb_live_start")
        with colB:
            stop = st.button("⏸ 일시정지", key="gb_live_stop")
        with colC:
            clear = st.button("🧹 리셋", key="gb_live_reset")
        with colD:
            interval = st.slider("속도(프레임 간 ms)", 10, 200, 60, 10, key="gb_live_interval")

        # 시작/정지/리셋
        if start:
            _live_init(n_rows_l, n_balls_l, p_l, seed=None)
            st.session_state["gb_live"]["interval_ms"] = interval

        S = st.session_state.get("gb_live")
        if S:
            if stop:
                S["running"] = False
            if clear:
                st.session_state.pop("gb_live", None)
                S = None
            elif not stop and S.get("running", False):
                S["interval_ms"] = interval

        # 현재 프레임 렌더
        placeholder_live = st.empty()

        # 현재 공 위치(있으면) 계산
        ball_pos = None
        counts_view = np.zeros(n_rows_l + 1, dtype=int)
        if S and S["n_rows"] == n_rows_l:
            counts_view = S["counts"].copy()
            if S["row_r"] > 0 and S["row_r"] <= n_rows_l and S["ball_i"] < S["n_balls"]:
                ball_pos = _ball_xy_at_step(S["row_r"], S["rights"])

        fig_live = _make_live_figure(n_rows_l, ball_pos, counts_view)
        placeholder_live.plotly_chart(fig_live, use_container_width=True)

        # 한 프레임 전진 + 자동 재호출
        if S and S.get("running", False):
            _live_tick()  # 상태를 한 스텝 업데이트
            time.sleep(S.get("interval_ms", 60) / 1000.0)
            st.rerun()
