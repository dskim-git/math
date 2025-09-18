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
    "description": "무작위로 꼭짓점을 선택해 중점으로 이동하는 과정을 점점 늘려가며 애니메이션으로 관찰합니다.",
}

# ---- 세션 키 ----
K_NMAX   = "sier_nmax"      # 목표(최대) 점 개수
K_CUR    = "sier_cur"       # 현재 그릴 점 개수
K_WARMUP = "sier_warmup"    # 버릴 단계 수
K_SIZE   = "sier_dot_size"  # 점 크기
K_SEED   = "sier_seed"      # 난수 시드
K_AUTO   = "sier_auto"      # 자동재생 on/off
K_SPEED  = "sier_speed"     # 자동재생 속도(초/스텝)

# 가중치(정점 선택 확률의 원시 가중치 → 내부에서 정규화)
K_W1 = "sier_w1"
K_W2 = "sier_w2"
K_W3 = "sier_w3"

# 내부 상태(캐시)
K_SIG     = "sier_signature"  # 파라미터 서명값 → 바뀌면 시퀀스 리셋
K_IDX     = "sier_idx"        # 미리 뽑아둔 꼭짓점 선택 인덱스 (길이 = Nmax + warmup)
K_PTS     = "sier_pts"        # 점 좌표 캐시 (shape = [Nmax, 2])
K_DONE    = "sier_done"       # 현재까지 계산된 점 개수 (캐시에 저장된 개수)
K_P_LAST  = "sier_plast"      # 마지막 점 좌표(다음 스텝 시작점)

DEFAULTS = {
    K_NMAX:   50_000,  # 목표 점 개수(최대치)
    K_CUR:    1,       # 시작은 1점부터
    K_WARMUP: 20,
    K_SIZE:   2,
    K_SEED:   42,
    K_AUTO:   False,
    K_SPEED:  0.10,    # 초/스텝 (작을수록 빠름)
    K_W1:     1.0,
    K_W2:     1.0,
    K_W3:     1.0,
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _signature(nmax, warmup, seed, w1, w2, w3):
    # 파라미터 기반 서명(변하면 시퀀스 재생성)
    return (int(nmax), int(warmup), int(seed), float(w1), float(w2), float(w3))

def _reset_sequence(nmax, warmup, seed, p_vec):
    """선택 인덱스/점 배열/초기점 등을 리셋."""
    # 정삼각형 꼭짓점 (정규화 좌표)
    V = np.array([[0.0, 0.0],
                  [1.0, 0.0],
                  [0.5, np.sqrt(3)/2.0]], dtype=np.float32)

    rng = np.random.default_rng(int(seed))
    # 미리 꼭짓점 선택 시퀀스를 한 번에 뽑아둠
    idx = rng.choice(3, size=int(nmax) + int(warmup), p=p_vec)
    # 시작점: 무게중심 근처
    p = V.mean(axis=0) + rng.normal(0, 0.01, size=2).astype(np.float32)

    # 워밍업(버리기) 먼저 진행
    for i in range(int(warmup)):
        v = V[idx[i]]
        p = (p + v) / 2.0

    # 캐시 초기화
    st.session_state[K_IDX] = idx
    st.session_state[K_PTS] = np.empty((int(nmax), 2), dtype=np.float32)
    st.session_state[K_DONE] = 0
    st.session_state[K_P_LAST] = p

def _extend_points_to(target_n):
    """캐시에 들어있는 점을 target_n개까지 확장 계산."""
    # 정삼각형 꼭짓점
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

    # 한 번에 너무 큰 루프를 돌면 프레임이 길어질 수 있으므로, 적당히 나눠서 처리
    # (여기서는 최대 10_000개씩 확장)
    CHUNK = 10_000
    cur = done
    while cur < target:
        end = min(target, cur + CHUNK)
        for i in range(cur, end):
            v = V[idx[i + st.session_state[K_WARMUP]]]  # 워밍업 뒤의 인덱스를 사용
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
        # 목표(최대) 점 개수: 1부터 시작 가능하도록
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
        if s <= 0:
            p_vec = np.array([1/3, 1/3, 1/3], dtype=float)
        else:
            p_vec = np.array([w1/s, w2/s, w3/s], dtype=float)
        st.caption(f"선택 확률: p(A)={p_vec[0]:.3f}, p(B)={p_vec[1]:.3f}, p(C)={p_vec[2]:.3f}")

        st.divider()
        st.subheader("▶ 자동 재생")
        st.toggle("자동재생 켜기", value=st.session_state[K_AUTO], key=K_AUTO)
        st.slider("⏱️ 속도 (초/스텝)", 0.03, 0.60, key=K_SPEED, step=0.01)
        st.caption("작을수록 빠르게 그려집니다.")

    # ---- 파라미터 읽기 & 서명 확인 (변경 시 시퀀스 리셋) ----
    Nmax   = int(st.session_state[K_NMAX])
    warmup = int(st.session_state[K_WARMUP])
    seed   = int(st.session_state[K_SEED])
    w1, w2, w3 = float(st.session_state[K_W1]), float(st.session_state[K_W2]), float(st.session_state[K_W3])
    s = w1 + w2 + w3
    if s <= 0:
        p_vec = np.array([1/3, 1/3, 1/3], dtype=float)
    else:
        p_vec = np.array([w1/s, w2/s, w3/s], dtype=float)

    sig = _signature(Nmax, warmup, seed, w1, w2, w3)
    if st.session_state.get(K_SIG) != sig:
        # 새 파라미터에 맞춰 전체 시퀀스 초기화
        _reset_sequence(Nmax, warmup, seed, p_vec)
        st.session_state[K_SIG] = sig
        # 현재 점 개수가 목표 초과 중이면 줄이고, 최소 1 보장
        st.session_state[K_CUR] = max(1, min(int(st.session_state[K_CUR]), Nmax))

    # ---- 현재 점 개수 업데이트 ----
    # 자동재생이면 프레임마다 증가, 아니면 수동 슬라이더 제공
    anchor("graph")

    if not st.session_state[K_AUTO]:
        # 수동 모드: 현재 점 개수 직접 조절 (1부터)
        st.slider("현재 점 개수 (수동)", 1, Nmax, key=K_CUR, step=1)
    else:
        # 자동 모드: 한 스텝에서 얼마나 늘릴지 → Nmax를 100 스텝 정도에 도달하도록 증가량 설정
        steps_target = 100
        inc = max(1, math.ceil(Nmax / steps_target))
        st.session_state[K_CUR] = min(Nmax, int(st.session_state[K_CUR]) + inc)

    # 캐시를 target까지 확장 계산
    target = int(st.session_state[K_CUR])
    _extend_points_to(target)

    # ---- 시각화 ----
    pts = st.session_state[K_PTS][:target]
    sz  = int(st.session_state[K_SIZE])

    fig = go.Figure()
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

    # 진행 바 & 상태 표시
    st.progress(target / Nmax if Nmax > 0 else 0.0, text=f"{target:,} / {Nmax:,}")

    # 자동재생 프레임 딜레이 + 리런
    if st.session_state[K_AUTO] and target < Nmax:
        time.sleep(float(st.session_state[K_SPEED]))
        scroll_to("graph")
        st.rerun()  # 최신 API (호환은 상단 _do_rerun 없이 여기서 직접)
