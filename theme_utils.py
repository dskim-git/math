# theme_utils.py — MathLab 전역 다크 테마 CSS 주입 유틸
"""
home.py와 pages/ 하위 파일 모두에서 동일한 다크 테마를 적용하기 위해
공통 CSS를 이 파일 한 곳에서 관리합니다.
"""
import streamlit as st

_DARK_THEME_CSS = """
<style>
/* ══════════════════════════════════════════════════════════════════════
   배경 — 다크 그리드
══════════════════════════════════════════════════════════════════════ */
.stApp {
    background-color: #0f172a !important;
    background-image:
        linear-gradient(rgba(99,102,241,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.06) 1px, transparent 1px) !important;
    background-size: 50px 50px !important;
}
.stApp > .main,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
}
header[data-testid="stHeader"], .stDeployButton, footer { display: none !important; }

/* ══════════════════════════════════════════════════════════════════════
   CSS 변수
══════════════════════════════════════════════════════════════════════ */
:root {
    --text-color: rgba(255,255,255,0.87) !important;
    --secondary-text-color: rgba(255,255,255,0.50) !important;
    --background-color: #0f172a !important;
    --secondary-background-color: rgba(255,255,255,0.04) !important;
}

/* ══════════════════════════════════════════════════════════════════════
   텍스트
══════════════════════════════════════════════════════════════════════ */
.stApp, body { color: rgba(255,255,255,0.87) !important; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
.stMarkdown p, .stMarkdown li { color: rgba(255,255,255,0.85) !important; }
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6,
h1, h2, h3, h4, h5, h6 { color: rgba(255,255,255,0.95) !important; }
[data-testid="stCaptionContainer"] p, .stCaption p {
    color: rgba(255,255,255,0.48) !important;
}
code {
    background: rgba(99,102,241,0.18) !important;
    color: #c4b5fd !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
}

/* ══════════════════════════════════════════════════════════════════════
   사이드바
══════════════════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: rgba(8, 14, 32, 0.97) !important;
    border-right: 1px solid rgba(99,102,241,0.18) !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span:not(.st-emotion-cache-hidden),
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] li { color: rgba(255,255,255,0.80) !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(99,102,241,0.20) !important; }
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: 1px solid rgba(99,102,241,0.20) !important;
    border-radius: 8px !important;
    background: rgba(255,255,255,0.02) !important;
    margin-bottom: 4px !important;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: rgba(255,255,255,0.85) !important;
}

/* ── 사이드바 버튼 (secondary / default) ── */
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] .stButton > button[kind="secondary"],
section[data-testid="stSidebar"] .stButton > button[kind="secondaryFormSubmit"] {
    background: rgba(255,255,255,0.06) !important;
    color: rgba(255,255,255,0.82) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 8px !important;
    transition: all 0.18s ease !important;
}
section[data-testid="stSidebar"] button:hover,
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99,102,241,0.20) !important;
    border-color: rgba(139,92,246,0.50) !important;
    color: #c4b5fd !important;
}
/* 사이드바 page_link */
section[data-testid="stSidebar"] [data-testid="stPageLink"] a,
section[data-testid="stSidebar"] [data-testid="stPageLink"] a:visited {
    background: rgba(255,255,255,0.04) !important;
    color: rgba(255,255,255,0.80) !important;
    border: 1px solid rgba(99,102,241,0.20) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
    background: rgba(99,102,241,0.18) !important;
    color: #c4b5fd !important;
}

/* ══════════════════════════════════════════════════════════════════════
   컨테이너 (border=True) — 유리 카드
══════════════════════════════════════════════════════════════════════ */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
}

/* ══════════════════════════════════════════════════════════════════════
   버튼 (메인 영역)
══════════════════════════════════════════════════════════════════════ */
.stButton > button,
.stButton > button[kind="secondary"],
.stButton > button[kind="secondaryFormSubmit"] {
    background: rgba(255,255,255,0.06) !important;
    color: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(99,102,241,0.28) !important;
    border-radius: 8px !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover,
.stButton > button[kind="secondary"]:hover {
    background: rgba(99,102,241,0.18) !important;
    border-color: rgba(139,92,246,0.55) !important;
    color: #c4b5fd !important;
}
.stButton > button[kind="primary"],
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.30) !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button:hover {
    box-shadow: 0 6px 24px rgba(124,58,237,0.48) !important;
    transform: translateY(-1px) !important;
}
.stLinkButton > a {
    background: rgba(255,255,255,0.06) !important;
    color: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(99,102,241,0.28) !important;
    border-radius: 8px !important;
}
.stLinkButton > a:hover {
    background: rgba(99,102,241,0.18) !important;
    border-color: rgba(139,92,246,0.50) !important;
    color: #c4b5fd !important;
}

/* ══════════════════════════════════════════════════════════════════════
   셀렉트박스 — 닫힌 상태(트리거) + 열린 상태(드롭다운) 통합
══════════════════════════════════════════════════════════════════════ */

/* 1) 컨트롤 박스 배경 */
[data-baseweb="select"],
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] {
    background: rgba(10,18,42,0.92) !important;
    border-color: rgba(99,102,241,0.35) !important;
    border-radius: 8px !important;
}

/* 2) 선택된 값 텍스트 — div/span/p 전부 흰색으로
      (버전마다 요소 종류가 달라서 범용으로 처리) */
[data-baseweb="select"] div,
[data-baseweb="select"] span,
[data-baseweb="select"] p,
[data-baseweb="select"] input,
[data-testid="stSelectbox"] div,
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p {
    color: rgba(255,255,255,0.87) !important;
}
/* 배경은 컨트롤 박스 외부 자식에만 transparent (드롭다운 배경 덮어쓰기 방지) */
[data-baseweb="select"] > div > div,
[data-baseweb="select"] > div > div > div {
    background: transparent !important;
}

/* 3) 화살표 아이콘 */
[data-baseweb="select"] svg,
[data-testid="stSelectbox"] svg {
    fill: rgba(255,255,255,0.55) !important;
    color: rgba(255,255,255,0.55) !important;
}

/* 4) 드롭다운이 열렸을 때 (portal 렌더링) */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="popover"] > div > div,
[data-baseweb="popover"] > div > div > div {
    background: #0e1a33 !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.60) !important;
}
[data-baseweb="menu"],
[data-baseweb="menu"] > div,
ul[data-baseweb="menu"] {
    background: #0e1a33 !important;
}
[data-baseweb="option"],
[data-baseweb="option"] > div,
li[role="option"],
[role="option"] {
    background: #0e1a33 !important;
    color: rgba(255,255,255,0.87) !important;
}
[data-baseweb="option"] div,
[data-baseweb="option"] span,
[data-baseweb="option"] p,
li[role="option"] div,
li[role="option"] span {
    color: rgba(255,255,255,0.87) !important;
    background: transparent !important;
}
[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"],
li[role="option"]:hover,
[role="option"]:hover {
    background: rgba(99,102,241,0.28) !important;
    color: #c4b5fd !important;
}
[data-baseweb="option"]:hover div,
[data-baseweb="option"]:hover span,
[data-baseweb="option"][aria-selected="true"] div,
[data-baseweb="option"][aria-selected="true"] span {
    color: #c4b5fd !important;
}
[role="listbox"] {
    background: #0e1a33 !important;
    border: 1px solid rgba(99,102,241,0.30) !important;
}

/* ══════════════════════════════════════════════════════════════════════
   텍스트 인풋 / 텍스트에리어
══════════════════════════════════════════════════════════════════════ */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
.stTextInput input,
.stTextArea textarea,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(15,23,42,0.80) !important;
    border-color: rgba(99,102,241,0.30) !important;
    color: rgba(255,255,255,0.87) !important;
    border-radius: 8px !important;
    caret-color: #a78bfa !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: rgba(139,92,246,0.55) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder,
.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.25) !important; }
.stTextInput label, .stTextArea label, .stSelectbox label,
[data-testid="stTextInput"] label, [data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label { color: rgba(255,255,255,0.55) !important; }

/* Number input 화살표 버튼 */
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(99,102,241,0.25) !important;
    color: rgba(255,255,255,0.75) !important;
}

/* ══════════════════════════════════════════════════════════════════════
   체크박스 / 라디오
══════════════════════════════════════════════════════════════════════ */
[data-testid="stCheckbox"] span, [data-testid="stRadio"] span {
    color: rgba(255,255,255,0.82) !important;
}
[data-testid="stRadio"] label, [data-testid="stCheckbox"] label {
    color: rgba(255,255,255,0.82) !important;
}

/* ══════════════════════════════════════════════════════════════════════
   멀티셀렉트
══════════════════════════════════════════════════════════════════════ */
[data-testid="stMultiSelect"] > div > div {
    background: rgba(15,23,42,0.80) !important;
    border-color: rgba(99,102,241,0.30) !important;
    border-radius: 8px !important;
}
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background: rgba(99,102,241,0.30) !important;
    color: #c4b5fd !important;
}

/* ══════════════════════════════════════════════════════════════════════
   슬라이더
══════════════════════════════════════════════════════════════════════ */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #7c3aed !important;
    border-color: #a78bfa !important;
}
[data-testid="stSlider"] label { color: rgba(255,255,255,0.55) !important; }

/* ══════════════════════════════════════════════════════════════════════
   익스팬더 (메인 영역)
══════════════════════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    border: 1px solid rgba(99,102,241,0.20) !important;
    border-radius: 10px !important;
    background: rgba(255,255,255,0.02) !important;
}
/* ── 헤더(토글) 부분 배경 — details>summary 또는 첫 번째 div ── */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] details > summary,
[data-testid="stExpander"] > div:first-of-type,
[data-testid="stExpander"] details {
    background: rgba(255,255,255,0.04) !important;
    color: rgba(255,255,255,0.87) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] > div:first-of-type p {
    color: rgba(255,255,255,0.87) !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: rgba(255,255,255,0.015) !important;
}
/* 사이드바 expander 헤더도 동일하게 */
section[data-testid="stSidebar"] [data-testid="stExpander"] summary,
section[data-testid="stSidebar"] [data-testid="stExpander"] details > summary,
section[data-testid="stSidebar"] [data-testid="stExpander"] > div:first-of-type,
section[data-testid="stSidebar"] [data-testid="stExpander"] details {
    background: rgba(255,255,255,0.05) !important;
    color: rgba(255,255,255,0.87) !important;
    border-radius: 7px !important;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary p,
section[data-testid="stSidebar"] [data-testid="stExpander"] summary span {
    color: rgba(255,255,255,0.85) !important;
}

/* ══════════════════════════════════════════════════════════════════════
   알림 박스
══════════════════════════════════════════════════════════════════════ */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-width: 1px !important;
    border-style: solid !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div { color: rgba(255,255,255,0.87) !important; }
[data-testid="stAlert"][data-baseweb="notification"],
div.stAlert { background: rgba(99,102,241,0.10) !important; border-color: rgba(99,102,241,0.30) !important; }
div.stAlert[data-testid="stAlert-warning"] { background: rgba(251,191,36,0.08) !important; border-color: rgba(251,191,36,0.30) !important; }
div.stAlert[data-testid="stAlert-error"]   { background: rgba(239,68,68,0.10)  !important; border-color: rgba(239,68,68,0.30)  !important; }
div.stAlert[data-testid="stAlert-success"] { background: rgba(34,197,94,0.10)  !important; border-color: rgba(34,197,94,0.30)  !important; }

/* ══════════════════════════════════════════════════════════════════════
   구분선 / 탭 / 스크롤바
══════════════════════════════════════════════════════════════════════ */
hr, [data-testid="stDivider"] hr { border-color: rgba(99,102,241,0.20) !important; }
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(99,102,241,0.20) !important;
}
.stTabs [data-baseweb="tab"] { background: transparent !important; color: rgba(255,255,255,0.40) !important; }
.stTabs [aria-selected="true"] { color: #a78bfa !important; border-bottom: 2px solid #a78bfa !important; }
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.35); border-radius: 3px; }

/* ══════════════════════════════════════════════════════════════════════
   DataFrame / 테이블
══════════════════════════════════════════════════════════════════════ */
/* 외부 컨테이너 — 흰 박스 제거, 어두운 테두리로 자연스럽게 녹아들기 */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] > div,
[data-testid="stDataFrame"] > div > div {
    background: transparent !important;
    border-radius: 8px !important;
    border-color: rgba(99,102,241,0.20) !important;
}
/* 내부 iframe 렌더링 — 색 반전으로 다크 처리 */
[data-testid="stDataFrame"] iframe {
    filter: invert(1) hue-rotate(180deg);
    border-radius: 6px;
}
.stDataFrame table th, .stDataFrame table td { color: rgba(255,255,255,0.85) !important; }

/* ══════════════════════════════════════════════════════════════════════
   코드 블록 (st.code / markdown 펜스)
══════════════════════════════════════════════════════════════════════ */
[data-testid="stMarkdownContainer"] pre,
[data-testid="stMarkdownContainer"] code,
[data-testid="stCode"] pre,
[data-testid="stCode"] code,
.stCodeBlock pre,
.stCodeBlock code {
    background: rgba(10,18,42,0.88) !important;
    border: 1px solid rgba(99,102,241,0.28) !important;
    border-radius: 8px !important;
    color: #c4b5fd !important;
}
[data-testid="stCode"] {
    background: transparent !important;
}

/* ══════════════════════════════════════════════════════════════════════
   파일 업로더
══════════════════════════════════════════════════════════════════════ */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(15,23,42,0.60) !important;
    border: 2px dashed rgba(99,102,241,0.38) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] div {
    color: rgba(255,255,255,0.55) !important;
    background: transparent !important;
}
[data-testid="stFileUploaderDropzone"] svg {
    fill: rgba(255,255,255,0.40) !important;
    color: rgba(255,255,255,0.40) !important;
}
/* 업로드 버튼 영역 */
[data-testid="stFileUploaderDropzoneInstructions"] {
    background: transparent !important;
}
[data-testid="baseButton-secondary"][kind="secondary"] {
    background: rgba(99,102,241,0.15) !important;
    border-color: rgba(99,102,241,0.35) !important;
    color: rgba(255,255,255,0.80) !important;
}

/* ══════════════════════════════════════════════════════════════════════
   Plotly 차트 컨테이너 래퍼
══════════════════════════════════════════════════════════════════════ */
[data-testid="stPlotlyChart"],
[data-testid="stPlotlyChart"] > div {
    background: transparent !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ══════════════════════════════════════════════════════════════════════
   메트릭 카드
══════════════════════════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(99,102,241,0.20) !important;
    border-radius: 10px !important;
    padding: 0.6rem 0.8rem !important;
}
[data-testid="stMetricLabel"] p { color: rgba(255,255,255,0.50) !important; }
[data-testid="stMetricValue"]   { color: rgba(255,255,255,0.92) !important; }
[data-testid="stMetricDelta"]   { color: rgba(255,255,255,0.60) !important; }

/* ══════════════════════════════════════════════════════════════════════
   스피너
══════════════════════════════════════════════════════════════════════ */
[data-testid="stSpinner"] p { color: rgba(255,255,255,0.60) !important; }
</style>
"""

# 멀티페이지 nav 숨김 CSS
_HIDE_NAV_CSS = """
<style>
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavContainer"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavLink"],
section[data-testid="stSidebar"] nav
{ display: none !important; visibility: hidden !important; }
</style>
"""


def inject_dark_theme():
    """MathLab 다크 테마를 현재 페이지에 주입합니다. 매 rerun마다 주입해야 합니다."""
    st.markdown(_DARK_THEME_CSS, unsafe_allow_html=True)


def inject_hide_nav():
    """Streamlit 기본 멀티페이지 네비게이션을 숨깁니다."""
    st.markdown(_HIDE_NAV_CSS, unsafe_allow_html=True)
