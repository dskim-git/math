META = {
    "title": "웜업: 몸풀기 게임",
    "description": "컴퍼스와 자를 이용한 작도 규칙을 익히는 몸풀기 문제 2개.",
    "order": 41,
    "hidden": True,
}

import streamlit as st
import streamlit.components.v1 as components

_PROBLEMS = [
    {
        "tab":   "① 2배 연장선",
        "title": "몸풀기 게임 — 2배 연장선",
        "badge": "3L · 3E",
        "desc":  (
            "컴퍼스만 사용하여 $\\overline{AC} = 2\\overline{AB}$ 가 되도록 "
            "직선 AB 위에 점 C를 작도하세요."
        ),
        "url":   "https://www.geogebra.org/calculator/epnvm2m9",
    },
    {
        "tab":   "② 원의 중심",
        "title": "몸풀기 게임 — 원의 중심",
        "badge": "2L · 5E",
        "desc":  "주어진 원의 중심을 작도하세요.",
        "url":   "https://www.geogebra.org/calculator/uksz8cbf",
    },
]

_BTN_HTML = """
<style>
.gg-warmup-btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 18px;
  padding: 9px 20px;
  border-radius: 8px;
  border: 1.5px solid #166534;
  background: #14532d;
  color: #4ade80;
  text-decoration: none;
  font-size: 0.92rem;
  font-weight: 800;
  transition: all .15s;
}}
.gg-warmup-btn:hover {{
  background: #15803d;
  border-color: #4ade80;
  color: #f0fdf4;
}}
.badge {{
  display: inline-block;
  padding: 2px 10px;
  border-radius: 5px;
  background: #1e3a5f;
  color: #7dd3fc;
  font-size: 0.82rem;
  font-weight: 800;
  border: 1px solid #0ea5e9;
  margin-left: 6px;
}}
</style>
<a class="gg-warmup-btn" href="{url}" target="_blank" rel="noopener">
  🔗 GeoGebra에서 풀기
</a>
"""


def render():
    st.header("🧩 작도 몸풀기 게임")
    st.caption("컴퍼스와 눈금 없는 자를 이용한 작도 규칙을 익히는 몸풀기 문제입니다.")

    tabs = st.tabs([p["tab"] for p in _PROBLEMS])

    for tab, prob in zip(tabs, _PROBLEMS):
        with tab:
            st.subheader(prob["title"])
            st.markdown(
                f'<span class="badge">{prob["badge"]}</span>',
                unsafe_allow_html=True,
            )
            st.markdown(prob["desc"])
            components.html(_BTN_HTML.format(url=prob["url"]), height=70)
