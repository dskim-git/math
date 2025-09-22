# activities/probability/binomial_galton_board.py
from __future__ import annotations
import time
import math
import random
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

META = {
    "title": "갈톤보드 (이항분포 실험기)",
    "description": "핀을 통과하며 좌/우로 튕기는 공을 떨어뜨려 이항분포가 어떻게 생기는지 관찰합니다.",
    "order": 200,  # 사이드바 정렬을 원하면 숫자 조정
}

# ─────────────────────────────────────────────────────────────────────────────
# 내부 상태
@dataclass
class BoardState:
    rows: int               # 핀의 줄 수 = 시행 횟수 n
    p_right: float          # 오른쪽으로 튕길 확률 p
    counts: List[int]       # 각 칸(0..rows) 도착 개수
    last_path: List[Tuple[int, int]]  # 마지막 공의 (level i, right_count r) 궤적
    running: bool           # 자동 실행 ON/OFF
    total_balls: int        # 총 떨어뜨린 공 개수

SESSION_KEY = "_galton_state"

def _new_state(rows: int, p_right: float) -> BoardState:
    return BoardState(
        rows=rows,
        p_right=p_right,
        counts=[0]*(rows+1),
        last_path=[],
        running=False,
        total_balls=0,
    )

def _get_state(rows: int, p: float) -> BoardState:
    st_state = st.session_state.get(SESSION_KEY)
    if isinstance(st_state, BoardState):
        # 행/확률이 바뀌면 리셋
        if st_state.rows != rows or abs(st_state.p_right - p) > 1e-12:
            st_state = _new_state(rows, p)
            st.session_state[SESSION_KEY] = st_state
    else:
        st_state = _new_state(rows, p)
        st.session_state[SESSION_KEY] = st_state
    return st_state

# ─────────────────────────────────────────────────────────────────────────────
# 시뮬레이션
def _drop_one_ball(state: BoardState):
    """공 1개를 떨어뜨려 끝 칸을 결정하고 카운트를 갱신."""
    r = 0
    path = []
    for i in range(1, state.rows+1):
        # i번째 핀을 지난 뒤 현재까지 오른쪽으로 튄 횟수 r
        go_right = random.random() < state.p_right
        if go_right:
            r += 1
        path.append((i, r))  # (현재 level i, 오른쪽으로 간 누적 r)
    state.counts[r] += 1
    state.total_balls += 1
    state.last_path = path

# ─────────────────────────────────────────────────────────────────────────────
# 그리기
def _draw_board(state: BoardState, show_path: bool):
    """삼각 격자 핀 + 마지막 공의 경로 시각화"""
    rows = state.rows
    # 좌표 설정: x = r - (i-r) = 2r - i  (레벨 i에서의 수평 위치), y = -i
    xs_pegs, ys_pegs = [], []
    for i in range(1, rows+1):  # i번째 줄 핀: 개수 i
        for r in range(i+1):    # 좌표는 중앙정렬 보정 위해 r- i/2 사용
            xs_pegs.append(r - i/2)
            ys_pegs.append(-i)

    fig, ax = plt.subplots(figsize=(5.2, 5.6))
    ax.scatter(xs_pegs, ys_pegs, s=16, alpha=0.7)

    # 마지막 경로
    if show_path and state.last_path:
        x_path = [0.0]  # 시작점(상단 중앙)
        y_path = [0.0]
        for i, r in state.last_path:
            x_path.append(r - i/2)
            y_path.append(-i)
        ax.plot(x_path, y_path, linewidth=2)

    ax.set_title("갈톤보드(핀) & 마지막 공 경로")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-rows/2 - 0.8, rows/2 + 0.8)
    ax.set_ylim(-rows - 0.5, 1.0)
    ax.axhline(0, linewidth=0.8)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def _binom_pmf(n: int, p: float) -> np.ndarray:
    k = np.arange(n+1)
    # 조합수
    comb = np.array([math.comb(n, int(kk)) for kk in k], dtype=float)
    return comb * (p**k) * ((1-p)**(n-k))

def _draw_histogram(state: BoardState, overlay: bool):
    counts = np.array(state.counts, dtype=float)
    n = state.rows
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    ax.bar(np.arange(n+1), counts, width=0.85, edgecolor="black")
    ax.set_xlabel("도착한 칸 번호 (오른쪽으로 튄 횟수 k)")
    ax.set_ylabel("개수")
    ax.set_title(f"누적 히스토그램  —  총 {state.total_balls:,}개")

    if overlay:
        pmf = _binom_pmf(n, state.p_right)
        expected = pmf * max(1, counts.sum())
        ax.plot(np.arange(n+1), expected, linewidth=2)
        ax.legend(["이론값(스케일)", "실험치"], loc="upper right")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.title("🎯 갈톤보드 (이항분포 실험기)")

    # ── 좌측 설정, 우측 그래프 배치
    colL, colR = st.columns([1, 1])

    with colL:
        st.subheader("설정")
        rows = st.slider("핀 줄 수 (시행 횟수 n)", 3, 20, 10, help="아래 칸 개수는 n+1개가 됩니다.")
        p = st.slider("오른쪽으로 튕길 확률 p", 0.0, 1.0, 0.5, 0.01)

    state = _get_state(rows, p)

    with colL:
        st.markdown("---")
        c1, c2, c3 = st.columns([1,1,1])

        if c1.button("공 1개 떨어뜨리기"):
            _drop_one_ball(state)

        # 자동 실행 토글
        if not state.running:
            if c2.button("▶ 자동 실행"):
                state.running = True
                st.session_state[SESSION_KEY] = state
                st.experimental_rerun()
        else:
            if c2.button("⏸ 정지"):
                state.running = False

        if c3.button("🔄 초기화"):
            st.session_state[SESSION_KEY] = _new_state(rows, p)
            st.experimental_rerun()

        speed = st.slider("속도(틱당 공 개수)", 1, 200, 20,
                          help="자동 실행 중 매 틱마다 몇 개의 공을 떨어뜨릴지 정합니다.")
        show_path = st.checkbox("마지막 공의 경로 보기", value=True)
        show_theory = st.checkbox("이론적 분포(이항분포) 겹쳐 보기", value=True)

        st.caption(
            "이론적으로 마지막 칸의 분포는  **Binomial(n, p)** 입니다. "
            "즉, k번째 칸에 도착할 확률은  "
            r"$\displaystyle \binom{n}{k} p^k (1-p)^{\,n-k}$ 입니다."
        )

    # 자동 실행 루프: 틱 당 speed개 드롭 후 즉시 rerun
    if state.running:
        for _ in range(speed):
            _drop_one_ball(state)
        # 너무 과도한 리렌더를 막기 위해 아주 짧게 쉬고 리런
        time.sleep(0.01)
        st.session_state[SESSION_KEY] = state
        st.experimental_rerun()

    # ── 그림들
    with colR:
        _draw_board(state, show_path)
    with colR:
        _draw_histogram(state, overlay=show_theory)
