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
    "description": "핀을 통과하며 좌/우로 움직이는 공을 모사합니다. 실시간 경로 보기 + 이론 곡선 표시.",
    "order": 20,
}

# ── 스크롤 복원(Fallback 포함)
try:
    from utils import keep_scroll  # 앱에 이미 있음
except Exception:
    import streamlit.components.v1 as components
    def keep_scroll(key: str = "default", mount: str = "sidebar"):
        html = f"""
        <html><body>
        <script>
          (function(){{
            const KEY='st_scroll::{key}::'+location.pathname+location.search;
            function restore(){{
              const y=sessionStorage.getItem(KEY); if(y!==null) window.scrollTo(0, parseFloat(y));
            }}
            restore(); setTimeout(restore,50); setTimeout(restore,250);
            let t=false; window.addEventListener('scroll',function(){{
              if(!t){{ requestAnimationFrame(function(){{ sessionStorage.setItem(KEY, window.scrollY); t=false; }}); t=true;}}
            }});
            setInterval(function(){{ sessionStorage.setItem(KEY, window.scrollY); }},500);
          }})();
        </script></body></html>"""
        components.html(html, height=1, scrolling=False)

# ─────────────────────────────────────────────────────────────────────────────
# 공통 유틸
def _binom_counts(n_rows: int, n_balls: int, p: float, seed: Optional[int] = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    rights = rng.binomial(n_rows, p, size=n_balls)
    return np.bincount(rights, minlength=n_rows + 1)

def _binom_theory(n_rows: int, p: float, total: int) -> np.ndarray:
    if total <= 0:
        return np.zeros(n_rows + 1, dtype=float)
    k = np.arange(n_rows + 1)
    pmf = np.array([comb(n_rows, int(i)) * (p ** i) * ((1 - p) ** (n_rows - i)) for i in k], dtype=float)
    return pmf * total

# ── (실시간) 핀/공 좌표: y를 음수로 둬서 **위→아래** 낙하
def _peg_xy(n_rows: int):
    xs, ys = [], []
    for r in range(n_rows):
        for j in range(r + 1):
            xs.append(j - r / 2.0)
            ys.append(-float(r))  # 위(0) → 아래(-n)
    return np.array(xs), np.array(ys)

def _ball_xy_at_step(row_r: int, rights_so_far: int) -> tuple[float, float]:
    x = rights_so_far - row_r / 2.0
    y = -float(row_r)
    return x, y

def _plot_hist_with_theory(counts: np.ndarray, theory: np.ndarray) -> go.Figure:
    n_rows = len(counts) - 1
    x = np.arange(n_rows + 1)
    fig = go.Figure()
    fig.add_bar(x=x, y=counts, name="실험(누적)", opacity=0.85)
    fig.add_scatter(x=x, y=theory, mode="lines", name="이론(이항)", line=dict(width=2))
    fig.update_layout(
        xaxis_title="오른쪽으로 간 횟수 (슬롯)",
        yaxis_title="개수",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_xaxes(dtick=1)
    return fig

def _make_live_figure(n_rows: int, ball_pos: Optional[tuple[float, float]],
                      counts: np.ndarray, theory: np.ndarray) -> go.Figure:
    """좌: 핀+공(위→아래), 우: 누적 히스토그램 + 이론선"""
    peg_x, peg_y = _peg_xy(n_rows)
    # x 범위 여유, y는 0(위) ~ -n(아래)
    x_range = (-n_rows / 2 - 1, n_rows / 2 + 1)
    y_range = (-(n_rows + 0.8), 0.8)

    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.60, 0.40],
        specs=[[{"type": "scatter"}, {"type": "bar"}]],
        horizontal_spacing=0.10,
    )

    # 왼쪽: 핀
    fig.add_trace(
        go.Scatter(x=peg_x, y=peg_y, mode="markers",
                   marker=dict(size=8, color="lightgray"),
                   name="핀", showlegend=False),
        row=1, col=1,
    )

    # 왼쪽: 공
    if ball_pos is not None:
        bx, by = ball_pos
        fig.add_trace(
            go.Scatter(x=[bx], y=[by], mode="markers",
                       marker=dict(size=14, color="crimson"),
                       name="공", showlegend=False),
            row=1, col=1,
        )

    fig.update_xaxes(range=x_range, row=1, col=1, zeroline=False)
    fig.update_yaxes(range=y_range, row=1, col=1, zeroline=False, scaleanchor="x", scaleratio=1)

    # 오른쪽: 히스토그램 + 이론선
    x = np.arange(n_rows + 1)
    fig.add_trace(go.Bar(x=x, y=counts, name="누적", opacity=0.85), row=1, col=2)
    fig.add_trace(go.Scatter(x=x, y=theory, mode="lines", name="이론(이항)", line=dict(width=2)), row=1, col=2)

    fig.update_xaxes(title_text="슬롯(오른쪽 횟수)", dtick=1, row=1, col=2)
    fig.update_yaxes(title_text="개수", row=1, col=2)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    return fig

# ── 실시간 엔진 상태 초기화
def _live_init(n_rows: int, n_balls: int, p: float, seed: Optional[int]):
    rng = np.random.default_rng(seed)
    moves = rng.binomial(1, p, size=(n_balls, n_rows)).astype(np.int8)  # 1=오른쪽, 0=왼쪽
    st.session_state["gb_live"] = dict(
        running=True,
        n_rows=n_rows,
        n_balls=n_balls,
        p=float(p),
        moves=moves,
        ball_i=0,         # 진행 중인 공 인덱스
        row_r=0,          # 현재 공의 행(핀 index)
        rights=0,         # 현재 공의 오른쪽 누계
        counts=np.zeros(n_rows + 1, dtype=int),
        total=0,
        interval_ms=60,   # 프레임 간 목표 시간
        _last_ts=time.perf_counter(),  # 속도 제어(경과 시간 기반)
    )

# 한 스텝(핀 하나) 진행
def _live_tick_once(S: dict):
    n_rows = S["n_rows"]
    n_balls = S["n_balls"]
    moves = S["moves"]

    if S["ball_i"] >= n_balls:  # 전부 완료
        S["running"] = False
        return

    if S["row_r"] < n_rows:
        step = int(moves[S["ball_i"], S["row_r"]])  # 0/1
        S["rights"] += step
        S["row_r"] += 1
    else:
        S["counts"][S["rights"]] += 1
        S["total"] += 1
        S["ball_i"] += 1
        S["row_r"] = 0
        S["rights"] = 0
        if S["ball_i"] >= n_balls:
            S["running"] = False

# 경과 시간만큼 여러 스텝 진행(속도 체감 ↑)
def _live_tick_by_elapsed():
    S = st.session_state.get("gb_live")
    if not S or not S.get("running", False):
        return
    now = time.perf_counter()
    interval = max(0.01, S.get("interval_ms", 60) / 1000.0)  # 최소 10ms
    elapsed = now - S.get("_last_ts", now)
    steps = max(1, int(elapsed // interval))  # 경과시간/간격 → 처리할 스텝 수
    for _ in range(steps):
        if not S.get("running", False):
            break
        _live_tick_once(S)
    # 남은 잔여시간 보존
    leftover = elapsed - steps * interval
    S["_last_ts"] = now - max(0.0, leftover)

# ─────────────────────────────────────────────────────────────────────────────
def render():
    keep_scroll(key="probability/galton_live", mount="sidebar")  # 스크롤 튐 방지(추가 주입)
    st.header("🧪 갈톤보드(이항분포) 시뮬레이터")

    tab_fast, tab_live = st.tabs(["누적(빠름)", "실시간(경로)"])

    # ── 1) 누적(빠름)
    with tab_fast:
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

        if "gb_counts" not in st.session_state:
            st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
            st.session_state["gb_total"] = 0
            st.session_state["gb_n_rows"] = n_rows

        def _reset_fast():
            st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
            st.session_state["gb_total"] = 0
            st.session_state["gb_n_rows"] = n_rows

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
        counts = st.session_state["gb_counts"] if total_now > 0 else np.zeros(n_rows + 1, dtype=int)
        theory = _binom_theory(n_rows, p, total_now)
        fig = _plot_hist_with_theory(counts, theory)
        placeholder.plotly_chart(fig, use_container_width=True)

        k = np.arange(n_rows + 1)
        mean_emp = (k * counts).sum() / max(1, total_now)
        var_emp = (((k - mean_emp) ** 2) * counts).sum() / max(1, total_now)
        st.caption(
            f"실험 개수: **{total_now:,}** · 경험적 평균 **{mean_emp:.3f}** / 분산 **{var_emp:.3f}**  "
            f"· 이론 평균 **{n_rows * p:.3f}** / 이론 분산 **{n_rows * p * (1 - p):.3f}**"
        )

    # ── 2) 실시간(경로)
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
            interval = st.slider("속도(작을수록 빠름, ms)", 10, 250, 60, 5, key="gb_live_interval")

        # 상태 초기화/제어
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
                _live_tick_by_elapsed()  # 경과시간만큼 여러 스텝 진행

        # 고정 placeholder(레이아웃 높이 안정 → 스크롤 튐 완화)
        info_ph = st.empty()
        fig_ph = st.empty()

        # 현재 상태로 그림/정보 표시
        counts_view = np.zeros(n_rows_l + 1, dtype=int)
        ball_pos = None
        total_so_far = 0
        remaining = 0
        if S and S["n_rows"] == n_rows_l:
            counts_view = S["counts"].copy()
            total_so_far = int(S["total"])
            remaining = max(0, S["n_balls"] - total_so_far)
            if 0 < S["row_r"] <= n_rows_l and S["ball_i"] < S["n_balls"]:
                ball_pos = _ball_xy_at_step(S["row_r"], S["rights"])

        theory_live = _binom_theory(n_rows_l, p_l, total_so_far)
        fig_live = _make_live_figure(n_rows_l, ball_pos, counts_view, theory_live)
        fig_ph.plotly_chart(fig_live, use_container_width=True)

        info_ph.markdown(
            f"**진행:** {total_so_far:,} / {n_balls_l:,}  "
            f"· **남은 공:** {remaining:,}  "
            f"· **속도(ms/step):** {interval}"
        )

        # 계속 진행 중이면 짧게 쉬고 rerun (keep_scroll이 스크롤 복원)
        if S and S.get("running", False):
            time.sleep(0.03)  # CPU 과점유 방지
            st.rerun()
