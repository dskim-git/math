# activities/probability/binomial_normal_approx.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom, norm

try:
    from utils import page_header, anchor, scroll_to
except Exception:
    def page_header(title, subtitle="", icon="", top_rule=True):
        if top_rule: st.markdown("---")
        st.markdown(f"### {icon+' ' if icon else ''}{title}")
        if subtitle: st.caption(subtitle)
    def anchor(name="content"): st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)
    def scroll_to(name="content"):
        import streamlit.components.v1 as components
        components.html(f"<script>window.location.hash='{name}'</script>", height=0)

META = {
    "title": "이항→정규 근사",
    "description": "이항분포 pmf와 정규 근사(연속성 보정 포함/제외)를 비교하고, 구간확률을 계산합니다.",
}

K_N="bna_n"; K_P="bna_p"; K_CC="bna_cc"; K_SHOWPMF="bna_showpmf"; K_A="bna_a"; K_B="bna_b"; JUMP="bna_jump"
DEFAULTS={K_N:50, K_P:0.30, K_CC:True, K_SHOWPMF:True, K_A:15, K_B:25}

def _ensure_defaults():
    for k,v in DEFAULTS.items():
        if k not in st.session_state: st.session_state[k]=v

def _mark_changed(): st.session_state[JUMP]="graph"

def _normal_pmf_approx(k_vals, mu, sd, cc=True):
    if cc:
        lo=(k_vals-0.5-mu)/sd; hi=(k_vals+0.5-mu)/sd
        return norm.cdf(hi)-norm.cdf(lo)
    return norm.pdf((k_vals-mu)/sd)*1.0

def render():
    _ensure_defaults()
    page_header("이항분포의 정규 근사","연속성 보정 유무에 따른 비교 및 구간확률 계산",icon="🧮",top_rule=True)

    with st.sidebar:
        st.subheader("⚙️ 설정")
        st.slider("시행 수 n",1,500,value=int(st.session_state[K_N]),key=K_N,on_change=_mark_changed)
        st.slider("성공확률 p",0.0,1.0,value=float(st.session_state[K_P]),step=0.01,key=K_P,on_change=_mark_changed)
        st.checkbox("연속성 보정 사용",value=bool(st.session_state[K_CC]),key=K_CC,on_change=_mark_changed)
        st.checkbox("근사 pmf 곡선도 표시",value=bool(st.session_state[K_SHOWPMF]),key=K_SHOWPMF,on_change=_mark_changed)
        st.markdown("**🎯 구간확률 P(a ≤ X ≤ b)**")
        st.number_input("a (정수)",value=int(st.session_state[K_A]),step=1,key=K_A,on_change=_mark_changed)
        st.number_input("b (정수, a≤b)",value=int(st.session_state[K_B]),step=1,key=K_B,on_change=_mark_changed)

    n=int(st.session_state[K_N]); p=float(st.session_state[K_P])
    cc=bool(st.session_state[K_CC]); show_curve=bool(st.session_state[K_SHOWPMF])
    a=int(st.session_state[K_A]);   b=int(st.session_state[K_B])

    mu=n*p; sd=np.sqrt(n*p*(1-p))

    k_min=max(0,int(np.floor(mu-4*sd))); k_max=min(n,int(np.ceil(mu+4*sd)))
    k=np.arange(k_min,k_max+1)

    anchor("graph")

    pmf = binom.pmf(k,n,p)
    approx_pmf = _normal_pmf_approx(k,mu,sd,cc=cc)

    # ── 강조 구간 마스크 ──
    if a>b: a,b=b,a
    a_clip=max(0,min(n,a)); b_clip=max(0,min(n,b))
    in_mask = (k>=a_clip)&(k<=b_clip)

    # 막대별 색 배열(하나의 trace만 사용)
    colors = np.where(in_mask, "rgba(239,68,68,0.95)", "rgba(156,163,175,0.60)")

    fig = go.Figure()
    fig.add_bar(
        x=k, y=pmf,
        name="이항 pmf(정확)",
        marker=dict(color=colors),
        hovertemplate="k=%{x}<br>pmf=%{y:.6f}<extra></extra>",
        showlegend=True
    )

    if show_curve:
        fig.add_scatter(
            x=k, y=approx_pmf, mode="lines+markers",
            name=f"정규 근사 pmf ({'CC' if cc else 'no CC'})",
            line=dict(width=2, color="rgba(37,99,235,1)"),
            marker=dict(size=5)
        )

    fig.update_layout(
        title=f"Bin(n={n}, p={p:.3f}) vs Normal(μ={mu:.2f}, σ={sd:.2f})",
        xaxis_title="k (성공 횟수)", yaxis_title="확률",
        legend_title="범례", bargap=0.05,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---- 구간확률: 정확 vs 근사 ----
    exact = float(binom.cdf(b_clip,n,p) - (binom.cdf(a_clip-1,n,p) if a_clip>0 else 0.0))
    if cc:
        z_hi=(b_clip+0.5-mu)/sd; z_lo=(a_clip-0.5-mu)/sd
        approx=float(norm.cdf(z_hi)-norm.cdf(z_lo))
    else:
        z_hi=(b_clip-mu)/sd; z_lo=(a_clip-mu)/sd
        approx=float(norm.cdf(z_hi)-norm.cdf(z_lo))

    st.markdown(
        f"**구간확률** P({a_clip} ≤ X ≤ {b_clip})  →  "
        f"정확: **{exact:.6f}**,  정규근사({ 'CC' if cc else 'no CC' }): **{approx:.6f}**,  "
        f"오차: **{(approx - exact):+.6f}**"
    )

    with st.expander("📘 개념 설명: 연속성 보정(continuity correction)", expanded=False):
        st.markdown("**왜 보정이 필요한가?**  \n이항분포는 *이산* 분포(정수 k), 정규분포는 *연속* 분포이기 때문에, 이항의 “막대 하나(폭=1)”를 정규의 “면적”으로 바꿔야 합니다.")
        st.markdown("**핵심 공식(정규근사)**")
        st.latex(r"Y \sim \mathcal{N}(\mu,\sigma)")
        st.latex(r"P(X=k)\ \approx\ P\!\left(k-\tfrac{1}{2}\ \le\ Y\ \le\ k+\tfrac{1}{2}\right)")
        st.latex(r"P(X\le b)\ \approx\ P(Y \le b+\tfrac{1}{2}),\quad P(X\ge a)\ \approx\ P(Y \ge a-\tfrac{1}{2})")
        st.latex(r"P(a\le X\le b)\ \approx\ P\!\left(a-\tfrac{1}{2}\ \le\ Y\ \le\ b+\tfrac{1}{2}\right)")
        st.markdown("**현재 설정**:")
        st.latex(fr"n={n},\ p={p:.3f}\ \Rightarrow\ \mu=np={mu:.2f},\ \sigma=\sqrt{{np(1-p)}}={sd:.2f}")
        st.info(f"정규 근사가 타당하려면 보통 **np ≥ 10**, **n(1−p) ≥ 10** 정도가 권장됩니다. (현재: np = {n*p:.1f}, n(1−p) = {n*(1-p):.1f})")

    if st.session_state.get(JUMP)=="graph":
        scroll_to("graph"); st.session_state[JUMP]=None
