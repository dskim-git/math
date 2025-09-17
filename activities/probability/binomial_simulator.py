# activities/probability/binomial_simulator.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

# utils: 제목/라인 렌더(간격 최소), (keep_scroll은 home.py에서 호출)
try:
    from utils import page_header
except Exception:
    # 최소 폴백(간격은 기본값)
    def page_header(title: str, subtitle: str = "", icon: str = "", top_rule: bool = True):
        if top_rule:
            st.markdown("---")
        if icon:
            st.markdown(f"### {icon} {title}")
        else:
            st.markdown(f"### {title}")
        if subtitle:
            st.caption(subtitle)

META = {
    "title": "확률 시뮬레이터 (이항분포 비교)",
    "description": "베르누이/동전/주사위 실험을 반복 시뮬레이션하고 이론 이항분포와 비교합니다.",
}

# ---- 위젯 키 & 기본값 (세션 충돌 방지용 고유 키) ----
K_MODE     = "prob_mode"
K_N        = "prob_n"
K_REPEATS  = "prob_repeats"
K_FACE     = "prob_face"
K_P        = "prob_p"

DEFAULTS = {
    K_MODE:    "동전 던지기(공정)",
    K_N:       30,
    K_REPEATS: 3000,
    K_FACE:    6,
    K_P:       0.35,
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def render():
    _ensure_defaults()

    # ✅ 회색 라인 + 제목을 '한 세트'로 출력(간격 최소)
    page_header("확률 시뮬레이터", "베르누이/동전/주사위 실험과 이론 분포 비교", icon="📊", top_rule=True)

    # ----- 사이드바 설정 (변경 즉시 rerun → 그래프 갱신) -----
    with st.sidebar:
        st.subheader("⚙️ 실험 설정")

        st.selectbox(
            "실험 종류",
            ["동전 던지기(공정)", "주사위(특정 눈)", "일반 베르누이(p)"],
            key=K_MODE,
        )

        st.slider(
            "1회 실험 시행 수 (n)", 1, 200,
            value=st.session_state[K_N],
            key=K_N,
        )

        st.slider(
            "반복 횟수 (시뮬레이션 반복)", 100, 20000,
            value=st.session_state[K_REPEATS],
            step=100,
            key=K_REPEATS,
        )

        if st.session_state[K_MODE] == "주사위(특정 눈)":
            st.number_input(
                "성공 눈 (1~6)",
                min_value=1, max_value=6,
                value=st.session_state[K_FACE],
                step=1, key=K_FACE,
            )

        if st.session_state[K_MODE] == "일반 베르누이(p)":
            st.slider(
                "성공확률 p", 0.0, 1.0,
                value=float(st.session_state[K_P]),
                step=0.01,
                key=K_P,
            )

    # ----- 현재 설정 읽기 -----
    mode    = st.session_state[K_MODE]
    n       = int(st.session_state[K_N])
    repeats = int(st.session_state[K_REPEATS])
    face    = int(st.session_state[K_FACE])
    p_user  = float(st.session_state[K_P])

    if mode == "동전 던지기(공정)":
        p_eff, label = 0.5, "앞면(성공)"
    elif mode == "주사위(특정 눈)":
        p_eff, label = 1/6, f"{face} 눈"
    else:  # 일반 베르누이(p)
        p_eff, label = p_user, "성공"

    st.write(f"**성공 조건:** {label} | **성공확률 p:** {p_eff:.3f}")

    # ----- 시뮬레이션 -----
    rng = np.random.default_rng()
    sim = rng.binomial(n=n, p=p_eff, size=repeats)  # 각 반복에서의 성공 횟수

    # 경험적 분포(상대도수)
    counts = np.bincount(sim, minlength=n+1)
    k_emp = np.nonzero(counts)[0]
    emp_prob = counts[counts > 0] / repeats

    # 이론 분포
    k = np.arange(0, n + 1)
    theo = binom.pmf(k, n, p_eff)

    # ----- 시각화 -----
    fig = go.Figure()
    fig.add_bar(x=k_emp, y=emp_prob, name="시뮬레이션", opacity=0.7)
    fig.add_scatter(x=k, y=theo, mode="lines+markers", name="이론(이항분포)", line=dict(width=2))
    fig.update_layout(
        title=f"이항분포 비교 (n={n}, p={p_eff:.3f})",
        xaxis_title="성공 횟수",
        yaxis_title="확률",
        legend_title="범례",
        bargap=0.05,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**포인트**: 시행 수가 커질수록 시뮬레이션 막대와 이론 곡선이 점점 가까워집니다 (대수의 법칙).")

    with st.expander("📎 시뮬레이션 원자료 보기"):
        st.dataframe({"성공횟수": sim[: min(1000, repeats)]})
