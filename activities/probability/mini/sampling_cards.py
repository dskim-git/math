import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go

PAGE_META = {
    "title": "숫자카드 표본 추출",
    "group": "확률과통계",
    "icon": "🧺",
}

# ----------------------------
# 유틸: 주머니(가방) + 카드 이미지 그리기 (Plotly)
# ----------------------------
def draw_bag_with_cards(N: int):
    # 레이아웃 좌표계 [0,1]x[0,1]
    fig = go.Figure()
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 1], scaleanchor="x", scaleratio=1)
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=340,
    )

    # 주머니(rounded rectangle 느낌)
    bag_x0, bag_x1 = 0.05, 0.95
    bag_y0, bag_y1 = 0.10, 0.90
    fig.add_shape(
        type="rect",
        x0=bag_x0, y0=bag_y0, x1=bag_x1, y1=bag_y1,
        fillcolor="rgba(245, 170, 110, 0.35)",
        line=dict(color="rgba(120, 80, 50, 0.8)", width=2),
        layer="below",
        xref="x", yref="y"
    )
    # 주머니 입구 띠
    fig.add_shape(
        type="rect",
        x0=bag_x0, y0=0.86, x1=bag_x1, y1=0.92,
        fillcolor="rgba(200, 120, 70, 0.6)",
        line=dict(color="rgba(120, 80, 50, 0.8)", width=1),
        layer="above",
        xref="x", yref="y"
    )

    # 카드 배치: 가로 cols, 세로 rows
    cols = 5 if N >= 5 else N
    rows = math.ceil(N / cols) if N > 0 else 0
    # 카드 크기/간격
    pad_x = 0.02
    pad_y = 0.02
    inner_w = (bag_x1 - bag_x0) - 2*pad_x
    inner_h = (bag_y1 - bag_y0) - 2*pad_y
    if rows == 0:
        return fig

    card_w = inner_w / max(cols, 1) * 0.8
    card_h = inner_h / max(rows, 1) * 0.6

    xs = []
    ys = []
    for k in range(N):
        r = k // cols
        c = k % cols
        cx = bag_x0 + pad_x + (c + 0.5) * inner_w / cols
        cy = bag_y1 - pad_y - (r + 0.6) * inner_h / rows
        xs.append(cx); ys.append(cy)

        # 카드 모양
        fig.add_shape(
            type="rect",
            x0=cx - card_w/2, x1=cx + card_w/2,
            y0=cy - card_h/2, y1=cy + card_h/2,
            fillcolor="white",
            line=dict(color="rgba(60,60,60,0.6)", width=1.2),
            layer="above",
        )
        # 숫자
        fig.add_annotation(
            x=cx, y=cy, text=str(k+1),
            showarrow=False,
            font=dict(size=16, color="black")
        )

    # 주머니 제목
    fig.add_annotation(
        x=0.5, y=0.96, text=f"모집단: 1부터 {N}까지 숫자카드",
        showarrow=False, font=dict(size=14, color="black")
    )
    return fig

# ----------------------------
# 유틸: 경우의 수 & 수식 LaTeX
# ----------------------------
def count_formulas(mode: str, N: int, n: int):
    """
    mode:
      - "복원추출"                 → 중복순열: N^n
      - "한 개씩 비복원 추출"     → 순열: N!/(N-n)!
      - "n개를 한번에 추출"       → 조합: C(N,n)
    """
    if mode == "복원추출":
        count = N**n
        latex = r"N^n \;(\text{중복순열})"
        ok = True
    elif mode == "한 개씩 비복원 추출":
        if n > N:
            return 0, r"\text{불가능: } n>N \Rightarrow \frac{N!}{(N-n)!}\ \text{정의불가}", False
        count = math.perm(N, n) if hasattr(math, "perm") else math.factorial(N)//math.factorial(N-n)
        latex = r"\frac{N!}{(N-n)!} \;(\text{순열})"
        ok = True
    else:  # "n개를 한번에 추출"
        if n > N:
            return 0, r"\text{불가능: } n>N \Rightarrow {N \choose n}\ \text{정의불가}", False
        # 조합
        try:
            from math import comb
            count = comb(N, n)
        except Exception:
            count = math.factorial(N)//(math.factorial(n)*math.factorial(N-n))
        latex = r"{N \choose n} \;(\text{조합})"
        ok = True
    return int(count), latex, ok

# ----------------------------
# 유틸: 표본 추출
# ----------------------------
def sample_once(mode: str, N: int, n: int, rng: np.random.Generator):
    items = np.arange(1, N+1)
    if mode == "복원추출":
        # with replacement, ordered
        return list(rng.choice(items, size=n, replace=True))
    elif mode == "한 개씩 비복원 추출":
        if n > N: return None
        # without replacement, ordered 추출 느낌을 위해 섞인 순서로 표시
        return list(rng.choice(items, size=n, replace=False))
    else:  # "n개를 한번에 추출"
        if n > N: return None
        sample = list(rng.choice(items, size=n, replace=False))
        sample.sort()  # 조합: 순서 무시 → 보기 좋게 정렬
        return sample

# ----------------------------
# 카드 UI(추출 결과) 렌더
# ----------------------------
def render_cards_row(sample):
    if not sample:
        st.warning("표본이 비어 있습니다.")
        return
    cols = st.columns(len(sample))
    for i, v in enumerate(sample):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    display:flex;align-items:center;justify-content:center;
                    width:80px;height:110px;margin:auto;
                    border:1.5px solid rgba(60,60,60,0.5);
                    border-radius:10px;background:white;
                    box-shadow:0 2px 6px rgba(0,0,0,0.08);">
                    <span style="font-size:26px;font-weight:700;color:#222;">{v}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

# ----------------------------
# 메인 렌더
# ----------------------------
def render():
    st.sidebar.subheader("⚙️ 설정")
    N = st.sidebar.slider("모집단 최대값 N", 2, 10, 6, step=1)
    n = st.sidebar.slider("표본 크기 n", 1, 10, 4, step=1)
    mode = st.sidebar.selectbox("추출 방식", ["복원추출", "한 개씩 비복원 추출", "n개를 한번에 추출"])
    seed = st.sidebar.number_input("난수 시드", value=0, step=1)

    # 경우의 수 & 수식
    cnt, latex, ok = count_formulas(mode, N, n)

    st.markdown("### 숫자카드 표본 추출 시뮬레이션")
    st.caption("주머니 안에는 **1부터 N까지 자연수**가 적힌 카드가 들어 있습니다. 설정한 방식에 따라 표본을 뽑아 보세요.")

    # 주머니 + 카드 그림
    st.plotly_chart(draw_bag_with_cards(N), use_container_width=True)

    # 수식/경우의 수 안내
    st.markdown("#### 가능한 표본의 개수")
    st.latex(latex.replace("N", str(N)).replace("n", str(n)))
    if ok:
        st.success(f"가능한 표본의 수: **{cnt:,}**")
    else:
        st.error("현재 설정에서는 표본을 만들 수 없습니다. (예: n > N 인 비복원 추출)")

    # 표본 추출 버튼
    rng = np.random.default_rng(int(seed))
    if "__draw_count__" not in st.session_state:
        st.session_state["__draw_count__"] = 0
    if st.button("🎲 표본 추출하기", use_container_width=True):
        st.session_state["__draw_count__"] += 1
        # 클릭마다 시드를 살짝 변화시켜 새 표본
        rng = np.random.default_rng(int(seed) + st.session_state["__draw_count__"])
        st.session_state["__last_sample__"] = sample_once(mode, N, n, rng)

    # 결과 표시
    sample = st.session_state.get("__last_sample__", None)
    st.markdown("#### 추출된 표본")
    if not ok:
        st.info("표본을 만들 수 없는 설정입니다. (n ≤ N이 되도록 조정하세요)")
    else:
        if sample is None:
            st.info("아래 버튼을 눌러 표본을 추출하세요.")
        else:
            render_cards_row(sample)

    with st.expander("ℹ️ 해설: 경우의 수와 표본 표현"):
        st.markdown(
            """
- **복원추출**: 한 번 뽑은 카드를 다시 넣고 뽑기 → **중복순열** \(N^n\) (순서가 중요)
- **한 개씩 비복원 추출**: 하나씩 뽑고 다시 넣지 않음 → **순열** \\(\\dfrac{N!}{(N-n)!}\\) (순서가 중요)
- **n개를 한번에 추출**: 한 번에 n장을 뽑아 **순서는 보지 않음** → **조합** \\({N \\choose n}\\)

표본을 화면에 표시할 때  
- “복원/비복원(한 개씩)”은 **나온 순서대로** 일렬 표시,  
- “n개를 한번에”는 **정렬(작은 수→큰 수)** 하여 **조합**처럼 표시했습니다.
            """
        )
