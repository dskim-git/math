# activities/etc/fractal/sierpinski_chaos.py
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
    "description": "무작위로 꼭짓점을 선택해 중점으로 이동하는 과정을 반복하면 프랙털이 나타납니다.",
}

# 세션 키
K_NPTS   = "sier_npts"
K_WARMUP = "sier_warmup"
K_SIZE   = "sier_dot_size"
K_SEED   = "sier_seed"
JUMP     = "sier_jump"

DEFAULTS = {
    K_NPTS:   40000,  # 그릴 점 개수
    K_WARMUP: 20,     # 초기 버릴 단계
    K_SIZE:   2,      # 점 크기(px)
    K_SEED:   42,     # 시드
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _mark_changed():
    st.session_state[JUMP] = "graph"

def render():
    _ensure_defaults()

    page_header("시에르핀스키 삼각형 (Chaos Game)", "무작위 반복에서 나타나는 자기유사", icon="🌀", top_rule=True)

    with st.sidebar:
        st.subheader("⚙️ 설정")
        st.slider("점 개수 (N)", 1000, 200_000, step=1000, key=K_NPTS, on_change=_mark_changed)
        st.slider("워밍업 단계(버리기)", 0, 200, step=5, key=K_WARMUP, on_change=_mark_changed)
        st.slider("점 크기(px)", 1, 5, step=1, key=K_SIZE, on_change=_mark_changed)
        st.number_input("난수 시드", value=int(st.session_state[K_SEED]), step=1, key=K_SEED, on_change=_mark_changed)

    # 현재 설정
    N   = int(st.session_state[K_NPTS])
    B   = int(st.session_state[K_WARMUP])
    sz  = int(st.session_state[K_SIZE])
    seed= int(st.session_state[K_SEED])

    # 그래프 위치 앵커
    anchor("graph")

    # 정삼각형 꼭짓점 (정규화 좌표)
    V = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.5, np.sqrt(3)/2.0],
    ], dtype=float)

    rng = np.random.default_rng(seed)
    # 시작점: 삼각형 내부 임의의 점(가중 랜덤)
    p = np.mean(V, axis=0) + rng.normal(0, 0.01, size=2)

    # Chaos game
    total_steps = B + N
    idx = rng.integers(0, 3, size=total_steps)
    pts = np.empty((N, 2), dtype=np.float32)
    c = 0
    for i in range(total_steps):
        v = V[idx[i]]
        p = (p + v) / 2.0
        if i >= B:
            pts[c] = p
            c += 1

    # 시각화 (Plotly Scattergl 성능 모드)
    fig = go.Figure()
    fig.add_scattergl(
        x=pts[:,0], y=pts[:,1],
        mode="markers",
        marker=dict(size=sz, opacity=0.9),
        showlegend=False
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)  # 정비율
    fig.update_layout(
        title=f"시에르핀스키 삼각형 (N={N:,}, seed={seed})",
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        dragmode="pan",
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📘 포인트"):
        st.markdown(
            "- 아무 꼭짓점이나 무작위로 고르고 **중점으로 이동**하는 과정을 반복하면 프랙털이 나타나요.  \n"
            "- 정사각형/오각형 등 다른 다각형으로 바꿔 실험해 보세요(확장 가능).  \n"
            "- 분수 차원과 자기유사성에 대해 토론해 보세요."
        )

    # 변경 직후 그래프 위치로 복귀
    if st.session_state.get(JUMP) == "graph":
        scroll_to("graph")
        st.session_state[JUMP] = None
