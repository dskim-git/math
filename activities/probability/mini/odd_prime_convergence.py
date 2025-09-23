# activities/probability/mini/odd_prime_convergence.py
import random
import math
import streamlit as st
import pandas as pd

META = {
    "title": "미니: P(소수 | 홀수) 수렴 관찰",
    "description": "n=10, 100, …처럼 시행수를 키우며 q/p가 2/3로 수렴하는 모습을 봅니다.",
    "hidden": True,     # 👈 사이드바/교과메인 숨김
    "order": 9999999,
}

def _estimate(n: int, seed: int | None = None) -> tuple[int,int,float]:
    if seed is not None:
        random.seed(seed)
    p = q = 0
    for _ in range(n):
        a = random.randint(1, 6)
        if a % 2 == 1:
            p += 1
            if a in (3, 5):
                q += 1
    est = (q / p) if p > 0 else float("nan")
    return p, q, est

def render():
    st.subheader("📈 시행수를 키우며 수렴 관찰")
    st.caption("표본 크기를 10, 100, 1,000 … 순서로 늘려가며 q/p가 2/3로 수렴하는지 봅니다.")

    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        max_exp = st.slider("최대 지수 k (10^k 까지)", min_value=2, max_value=6, value=5,
                            help="k=6이면 최대 1,000,000회까지 실행합니다(시간 소요).")
    with c2:
        seed_on = st.toggle("시드 고정", value=False)
    with c3:
        seed_val = st.number_input("seed", value=123, step=1)

    go = st.button("실행", type="primary", use_container_width=True)

    if not go:
        return

    rows = []
    for i in range(1, max_exp + 1):
        n = 10 ** i
        p, q, est = _estimate(n, seed=int(seed_val) if seed_on else None)
        rows.append({"n": n, "홀수(p)": p, "소수(3,5)=q": q, "추정 q/p": est})

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    # 선 그래프(추정값) + 기준선 2/3
    st.line_chart(df.set_index("n")["추정 q/p"])
    st.caption("참고: 이론값 2/3 ≈ 0.6667 (그래프 y축에서 해당 값으로 수렴하는지 관찰)")
