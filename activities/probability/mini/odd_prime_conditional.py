# activities/probability/mini/odd_prime_conditional.py
import random
import streamlit as st

META = {
    "title": "미니: 홀수일 때 소수일 확률 (주사위)",
    "description": "주사위를 n번 던져서 ‘홀수’가 나온 경우 중 ‘소수(3,5)’의 비율을 추정합니다.",
    "hidden": True,     # 👈 사이드바/교과메인 숨김
    "order": 9999999,
}

def _trial(n: int):
    p = 0  # 홀수 횟수
    q = 0  # (홀수이면서) 소수(3,5) 횟수
    for _ in range(n):
        a = random.randint(1, 6)
        if a % 2 == 1:     # 1,3,5
            p += 1
            if a in (3, 5):
                q += 1
    return p, q

def render():
    st.subheader("🎲 미니 실험: P(소수 | 홀수)")
    st.caption("주사위를 n번 던져 ‘홀수(1,3,5)’가 나온 시도들 중 ‘소수(3,5)’ 비율을 추정합니다. 이론값은 2/3.")

    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        n = st.slider("시행 횟수 n", min_value=10, max_value=200000, value=5000, step=10)
    with c2:
        seed_on = st.toggle("시드 고정", value=False)
    with c3:
        seed_val = st.number_input("seed", value=42, step=1, help="시드 고정이 켜진 경우 사용")

    run = st.button("실험 실행", type="primary", use_container_width=True)

    if run:
        if seed_on:
            random.seed(int(seed_val))
        p, q = _trial(int(n))
        st.divider()
        st.write(f"홀수(1,3,5) 횟수 **p = {p}**, 그중 소수(3,5) 횟수 **q = {q}**")
        if p == 0:
            st.warning("이번 실험에서 홀수가 한 번도 나오지 않았습니다. n을 늘려 다시 실행해 보세요.")
            return
        est = q / p
        st.metric("추정값  q/p", f"{est:.6f}")
        st.latex(r"P(\text{prime}\mid \text{odd})=\frac{|\{3,5\}|}{|\{1,3,5\}|}=\frac{2}{3}\approx 0.666666\ldots")
        st.write(f"오차(추정−이론): **{est - 2/3:+.6f}**")
