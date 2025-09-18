# activities/etc/fractal/sierpinski_chaos.py
import time
import math
import streamlit as st
import numpy as np
import plotly.graph_objects as go

try:
    from utils import page_header, anchor, scroll_to
except Exception:
    def page_header(t, s="", icon="", top_rule=True):
        if top_rule: st.markdown("---")
        st.markdown(f"### {icon+' ' if icon else ''}{t}")
        if s: st.caption(s)
    def anchor(name="content"): st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)
    def scroll_to(name="content"):
        import streamlit.components.v1 as components
        components.html(f"<script>window.location.hash='{name}'</script>", height=0)

META = {
    "title": "시에르핀스키 삼각형 (Chaos Game)",
    "description": "무작위 꼭짓점으로 중점을 반복 이동하며, 점이 하나씩 쌓이는 과정을 애니메이션으로 관찰합니다.",
}

# ---- 세션 키 ----
K_NMAX   = "sier_nmax"
K_CUR    = "sier_cur"
K_WARMUP = "sier_warmup"
K_SIZE   = "sier_dot_size"
K_SEED   = "sier_seed"
K_AUTO   = "sier_auto"
K_SPEED  = "sier_speed"
K_W1 = "sier_w1"; K_W2 = "sier_w2"; K_W3 = "sier_w3"
K_TRI_ON = "sier_triangle_on"

# 내부 상태
K_SIG  = "sier_signature"
K_IDX  = "sier_idx"
K_PTS  = "sier_pts"
K_DONE = "sier_done"
K_P_LAST = "sier_plast"

DEFAULTS = {
    K_NMAX:   50_000,
    K_CUR:    1,
    K_WARMUP: 20,
    K_SIZE:   2,
    K_SEED:   42,
    K_AUTO:   False,
    K_SPEED:  0.10,
    K_W1:     1.0, K_W2: 1.0, K_W3: 1.0,
    K_TRI_ON: False,
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _signature(nmax, warmup, seed, w1, w2, w3):
    return (int(nmax), int(warmup), int(seed), float(w1), float(w2), float(w3))

def _reset_sequence(nmax, warmup, seed, p_vec):
    V = np.array([[0.0, 0.0],
                  [1.0, 0.0],
                  [0.5, np.sqrt(3)/2.0]], dtype=np.float32)
    rng = np.random.default_rng(int(seed))
    idx = rng.choice(3, size=int(nmax) + int(warmup), p=p_vec)
    p = V.mean(axis=0) + rng.normal(0, 0.01, size=2).astype(np.float32)
    for i in range(int(warmup)):
        v = V[idx[i]]
        p = (p + v) / 2.0
    st.session_state[K_IDX] = idx
    st.session_state[K_PTS] = np.empty((int(nmax), 2), dtype=np.float32)
    st.session_state[K_DONE] = 0
    st.session_state[K_P_LAST] = p

def _extend_points_to(target_n):
    V = np.array([[0.0, 0.0],
                  [1.0, 0.0],
                  [0.5, np.sqrt(3)/2.0]], dtype=np.float32)
    done = int(st.session_state[K_DONE])
    target = int(target_n)
    if target <= done:
        return
    idx = st.session_state[K_IDX]
    pts = st.session_state[K_PTS]
    p   = st.session_state[K_P_LAST]
    CHUNK = 10_000
    cur = done
    while cur < target:
        end = min(target, cur + CHUNK)
        for i in range(cur, end):
            v = V[idx[i + st.session_state[K_WARMUP]]]
            p = (p + v) / 2.0
            pts[i] = p
        cur = end
    st.session_state[K_P_LAST] = p
    st.session_state[K_DONE] = target

def render():
    _ensure_defaults()
    page_header("시에르핀스키 삼각형 (Chaos Game)", "점이 하나씩 쌓이며 패턴이 형성되는 과정을 관찰합니다.", icon="🌀", top_rule=True)

    # ---- 사이드바 ----
    with st.sidebar:
        st.subheader("⚙️ 설정")
        st.slider("최대 점 개수 Nₘₐₓ", 1, 300_000, key=K_NMAX, step=1)
        st.slider("워밍업 단계(버리기)", 0, 500, key=K_WARMUP, step=5)
        st.slider("점 크기(px)", 1, 6, key=K_SIZE, step=1)
        st.number_input("난수 시드", value=int(st.session_state[K_SEED]), step=1, key=K_SEED)

        st.divider()
        st.subheader("🎯 꼭짓점 선택 가중치")
        st.caption("세 가중치를 내부에서 정규화하여 확률 p₁,p₂,p₃로 사용합니다.")
        st.slider("가중치 w₁ (정점 A)", 0.0, 10.0, key=K_W1, step=0.1)
        st.slider("가중치 w₂ (정점 B)", 0.0, 10.0, key=K_W2, step=0.1)
        st.slider("가중치 w₃ (정점 C)", 0.0, 10.0, key=K_W3, step=0.1)

        # 정규화된 확률 표시
        w1, w2, w3 = float(st.session_state[K_W1]), float(st.session_state[K_W2]), float(st.session_state[K_W3])
        s = w1 + w2 + w3
        p_vec = np.array([1/3, 1/3, 1/3], dtype=float) if s <= 0 else np.array([w1/s, w2/s, w3/s], dtype=float)
        st.caption(f"선택 확률: p(A)={p_vec[0]:.3f}, p(B)={p_vec[1]:.3f}, p(C)={p_vec[2]:.3f}")

        st.divider()
        st.subheader("▶ 자동 재생")
        st.slider("⏱️ 속도 (초/스텝)", 0.03, 0.60, key=K_SPEED, step=0.01)
        def _toggle_auto():
            st.session_state[K_AUTO] = not st.session_state[K_AUTO]
        play_label = "⏸ 자동재생 정지" if st.session_state[K_AUTO] else "▶ 자동재생 시작"
        st.button(play_label, key="sier_play_btn", on_click=_toggle_auto, use_container_width=True)

        st.divider()
        st.subheader("🟦 표시 옵션")
        def _toggle_tri():
            st.session_state[K_TRI_ON] = not st.session_state[K_TRI_ON]
        tri_label = "△ ABC 숨기기" if st.session_state[K_TRI_ON] else "△ ABC 보이기"
        st.button(tri_label, key="sier_tri_btn", on_click=_toggle_tri, use_container_width=True)

    # ---- 파라미터 & 서명(변경 시 리셋) ----
    Nmax   = int(st.session_state[K_NMAX])
    warmup = int(st.session_state[K_WARMUP])
    seed   = int(st.session_state[K_SEED])
    w1, w2, w3 = float(st.session_state[K_W1]), float(st.session_state[K_W2]), float(st.session_state[K_W3])
    s = w1 + w2 + w3
    p_vec = np.array([1/3, 1/3, 1/3], dtype=float) if s <= 0 else np.array([w1/s, w2/s, w3/s], dtype=float)

    sig = _signature(Nmax, warmup, seed, w1, w2, w3)
    if st.session_state.get(K_SIG) != sig:
        _reset_sequence(Nmax, warmup, seed, p_vec)
        st.session_state[K_SIG] = sig
        st.session_state[K_CUR] = max(1, min(int(st.session_state[K_CUR]), Nmax))

    # ---- 현재 점 개수 업데이트 ----
    anchor("graph")

    if not st.session_state[K_AUTO]:
        # 수동 모드: − / ＋ 버튼으로 1씩 조정
        st.session_state[K_CUR] = max(1, min(int(st.session_state[K_CUR]), Nmax))
        c_slider, c_minus, c_plus = st.columns([8, 1, 1])
        with c_minus:
            dec_clicked = st.button("−", key="sier_dec", help="점 1개 감소", use_container_width=True)
        with c_plus:
            inc_clicked = st.button("＋", key="sier_inc", help="점 1개 증가", use_container_width=True)  # ← 전각 플러스
        if dec_clicked:
            st.session_state[K_CUR] = max(1, int(st.session_state[K_CUR]) - 1)
        if inc_clicked:
            st.session_state[K_CUR] = min(Nmax, int(st.session_state[K_CUR]) + 1)
        with c_slider:
            st.slider("현재 점 개수 (수동)", 1, Nmax, key=K_CUR, step=1)
    else:
        steps_target = 100
        inc = max(1, math.ceil(Nmax / steps_target))
        st.session_state[K_CUR] = min(Nmax, int(st.session_state[K_CUR]) + inc)

    target = int(st.session_state[K_CUR])
    _extend_points_to(target)

    # ---- 시각화 ----
    pts = st.session_state[K_PTS][:target]
    sz  = int(st.session_state[K_SIZE])
    fig = go.Figure()

    # (옵션) 배경 삼각형 + 라벨(겹치지 않도록 x/yshift 적용)
    if st.session_state[K_TRI_ON]:
        V = np.array([[0.0, 0.0],
                      [1.0, 0.0],
                      [0.5, np.sqrt(3)/2.0]], dtype=float)
        shapes = [
            dict(type="line", x0=V[0,0], y0=V[0,1], x1=V[1,0], y1=V[1,1],
                 line=dict(width=2, color="rgba(60,60,60,0.7)"), layer="below"),
            dict(type="line", x0=V[1,0], y0=V[1,1], x1=V[2,0], y1=V[2,1],
                 line=dict(width=2, color="rgba(60,60,60,0.7)"), layer="below"),
            dict(type="line", x0=V[2,0], y0=V[2,1], x1=V[0,0], y1=V[0,1],
                 line=dict(width=2, color="rgba(60,60,60,0.7)"), layer="below"),
        ]
        fig.update_layout(shapes=shapes)
        # 점 이름이 선과 겹치지 않도록 픽셀 단위로 살짝 띄우기
        fig.add_annotation(x=V[0,0], y=V[0,1], text="A", showarrow=False,
                           font=dict(size=14), xshift=-14, yshift=-12)
        fig.add_annotation(x=V[1,0], y=V[1,1], text="B", showarrow=False,
                           font=dict(size=14), xshift=14, yshift=-12)
        fig.add_annotation(x=V[2,0], y=V[2,1], text="C", showarrow=False,
                           font=dict(size=14), yshift=14)

    fig.add_scattergl(
        x=pts[:, 0], y=pts[:, 1],
        mode="markers",
        marker=dict(size=sz, opacity=0.9),
        showlegend=False
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_layout(
        title=f"시에르핀스키 삼각형 — 현재 점 개수: {target:,} / 최대 {Nmax:,}",
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        dragmode="pan",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.progress(target / Nmax if Nmax > 0 else 0.0, text=f"{target:,} / {Nmax:,}")

    # 자동재생 제어
    if st.session_state[K_AUTO]:
        if target >= Nmax:
            st.session_state[K_AUTO] = False
        else:
            time.sleep(float(st.session_state[K_SPEED]))
            scroll_to("graph")
            st.rerun()
