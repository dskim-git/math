import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict

PAGE_META = {
    "title": "큰 수의 법칙(이항·심플)",
    "group": "확률과통계",
    "icon": "🎯",
}

def _bigN_from_inside(inside_row: np.ndarray) -> int:
    """
    inside_row[k, n-1] = True  ⇔  |X_n/n - p| < eps
    '빅 N' = 그 이후(모든 n ≥ N)에 항상 inside인 최초의 N.
    구현: 마지막으로 inside=False가 나타난 위치 idx_last_false를 찾아 N = idx_last_false + 2
         (n은 1부터 시작이므로 +1, 그리고 그 다음 시점이 N이므로 추가로 +1)
    모든 시점이 inside이면 N = 1 로 정의.
    """
    if inside_row.all():
        return 1
    last_false = np.where(~inside_row)[0].max()
    return int(last_false + 2)

def render():
    st.sidebar.subheader("⚙️ 파라미터")
    p = st.sidebar.slider("수학적 확률 p (성공확률)", 0.0, 1.0, 0.5, 0.01)
    n_max = st.sidebar.slider("시행 횟수 n (최대)", 50, 5000, 800, step=50)
    paths = st.sidebar.slider("경로(반복) 수", 1, 50, 10, step=1)  # 1~50, 기본 10

    eps = st.sidebar.number_input("ε (허용 오차)", value=0.1, min_value=0.0, step=0.01, format="%.2f")
    seed = st.sidebar.number_input("난수 시드", value=0, step=1)

    st.sidebar.subheader("🧭 빅 N 표시 옵션")
    mark_mode = st.sidebar.selectbox("표시 방식", ["세로선(권장)", "표로만"], index=0)
    mark_count_max = min(20, paths)
    mark_count = st.sidebar.slider("빅 N 표시할 경로 수(상위부터)", 1, mark_count_max, min(10, mark_count_max))

    st.markdown("### 이항 시뮬레이션으로 보는 큰 수의 법칙")
    st.caption(
        r"베르누이 시행을 $n$번 했을 때 $X_n$=성공 횟수. "
        r"상대도수 $\frac{X_n}{n}$ 은 수학적 확률 $p$ 에 **확률적으로 수렴**합니다."
    )

    rng = np.random.default_rng(int(seed))
    # 각 경로의 상대도수 곡선 (X_n/n)
    ratios = np.zeros((paths, n_max))
    for k in range(paths):
        x = rng.binomial(1, p, size=n_max).astype(float)
        ratios[k] = np.cumsum(x) / np.arange(1, n_max + 1)

    # n별 밴드 내 여부와 경험적 비율
    inside = np.abs(ratios - p) < eps
    prop_inside = inside.mean(axis=0)

    # --------- 그림 1: 상대도수 경로 + 빅 N 표시 ---------
    fig1 = go.Figure()
    # 경로 선
    strong = min(8, paths)  # 앞의 몇 개는 강조
    for i in range(paths):
        width = 2 if i < strong else 1
        opacity = 0.9 if i < strong else 0.35
        fig1.add_scatter(
            x=np.arange(1, n_max + 1),
            y=ratios[i],
            mode="lines",
            line=dict(width=width),
            opacity=opacity,
            showlegend=False,
            hoverinfo="x+y",
            name=f"path {i+1}"
        )

    # p 기준선 & ε-밴드
    fig1.add_hline(y=p, line_width=2, line_dash="dash", annotation_text=f"p = {p:.2f}")
    if eps > 0:
        fig1.add_hline(y=p + eps, line_width=1, line_dash="dot")
        fig1.add_hline(y=p - eps, line_width=1, line_dash="dot")
        fig1.add_shape(
            type="rect",
            x0=1, x1=n_max,
            y0=p - eps, y1=p + eps,
            fillcolor="LightSkyBlue", opacity=0.18, line_width=0, layer="below"
        )

    # --- 빅 N 계산 ---
    bigNs = np.array([_bigN_from_inside(inside[i]) for i in range(paths)], dtype=int)

    # 표시(겹침 최소화): 같은 N에 여러 경로가 몰릴 수 있으니 yshift를 스택
    if mark_mode == "세로선(권장)":
        # 상위 mark_count개 경로만 표시 (시각적 과밀 방지)
        # "상위" 기준: i 인덱스 순서(앞쪽 라인을 강조했으므로 동일 기준 사용)
        idxs_to_mark = list(range(min(mark_count, paths)))

        stack_count_by_N = defaultdict(int)
        for j, i in enumerate(idxs_to_mark):
            N = int(bigNs[i])
            # v-line
            fig1.add_vline(x=N, line_width=1, line_dash="dot", opacity=0.6)

            # 라벨 위치 스택: 같은 x=N에 여러 개가 겹치면 위로 조금씩 올림
            stack = stack_count_by_N[N]
            stack_count_by_N[N] += 1

            # 라벨 y 좌표: 밴드 위쪽 + 약간 마진, 범위 [0,1] 안으로 클리핑
            y_base = p + eps if eps > 0 else p
            y_annot = min(1.0, y_base + 0.02 + 0.05 * stack)

            fig1.add_annotation(
                x=N,
                y=y_annot,
                text=f"N={N} (path {i+1})",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                ax=0,
                ay=-20 - 6 * stack,  # 스택마다 화살 길이 조금씩 조정
                bgcolor="rgba(255,255,255,0.7)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1,
                font=dict(size=11)
            )

    fig1.update_layout(
        title="상대도수 Xₙ/n 의 경로들 & 경로별 '빅 N' 표시",
        xaxis_title="시행 횟수 n",
        yaxis_title="상대도수 Xₙ/n",
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 빅 N 표/다운로드
    with st.expander("🧾 경로별 빅 N 값 (표/다운로드)"):
        import pandas as pd
        dfN = pd.DataFrame({"path": np.arange(1, paths + 1), "big_N": bigNs})
        st.dataframe(dfN, use_container_width=True)
        csv = dfN.to_csv(index=False).encode("utf-8-sig")
        st.download_button("CSV 다운로드", data=csv, file_name="bigN_by_path.csv", mime="text/csv")

    # --------- 특정 n에서 밴드 안 비율 ----------
    n_check = st.slider("🔍 특정 n에서 |Xₙ/n − p| < ε 인 경로 비율", 1, n_max, int(0.6 * n_max), step=1)
    st.info(
        f"n = {n_check} 에서  |Xₙ/n − p| < ε  비율: **{prop_inside[n_check-1]:.3f}**  "
        f"(경로 {paths}개 중 {int(prop_inside[n_check-1]*paths)}개)"
    )

    # --------- 그림 2: n에 따른 비율 P(|Xₙ/n − p| < ε)의 경험적 추정 ----------
    fig2 = go.Figure()
    fig2.add_scatter(
        x=np.arange(1, n_max + 1),
        y=prop_inside,
        mode="lines",
        line=dict(width=3),
        name="경험적 비율"
    )

    # (선택) 체비셰프 부등식 하한선 안내: 간단 설명만 텍스트로 남김 (그래프 혼잡도 낮춤)
    fig2.update_layout(
        title="n에 따른  P(|Xₙ/n − p| < ε)  (시뮬레이션 경로 비율)",
        xaxis_title="n",
        yaxis_title="비율",
        yaxis=dict(range=[0, 1.0])
    )
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📘 수열의 극한 vs 큰 수의 법칙(확률적 수렴) 간단 비교"):
        st.markdown(
            r"""
**수열의 극한(결정적 수렴)**  
- 임의의 $\varepsilon>0$에 대해, 어떤 $N$이 있어 **모든** $n\ge N$에 대해 $|a_n-L|<\varepsilon$.

**큰 수의 법칙(확률적 수렴)**  
- 임의의 $\varepsilon>0$에 대해, $n\to\infty$ 이면  
  $\mathsf{P}(|X_n/n - p|<\varepsilon)\to 1$.

이 페이지의 '빅 N'은 **각 경로마다 다르게** 표시됩니다.  
수열 극한에서는 하나의 고정된 $N$으로 설명하지만, 확률적 수렴에서는 경로별 우연성 때문에  
'안으로 들어온 뒤 다시 나가는 경우'가 있을 수 있어 **경로별 $N$이 달라집니다**.
"""
        )

    st.caption("Tip: 표시 경로 수를 5~10개로 두면 v-line과 라벨이 가장 깔끔하게 보입니다.")
