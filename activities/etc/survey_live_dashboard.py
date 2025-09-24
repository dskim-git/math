# activities/etc/survey_live_dashboard.py
import time
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from survey_utils import (
    load_csv_live, make_csv_export_url, parse_mcq_series,
    basic_tokenize_korean, top_n_tokens
)

META = {
    "title": "실시간 설문 대시보드",
    "description": "구글폼→시트 URL만 붙여넣으면 CSV로 자동 변환해 실시간 시각화",
    "order": 10,
}

# 워드클라우드(선택)
WC_AVAILABLE = True
try:
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
except Exception:
    WC_AVAILABLE = False


def _auto_refresh(seconds: int, key: str = "auto_refresh_survey"):
    """가능하면 streamlit-autorefresh 사용, 없으면 meta-refresh로 폴백"""
    if seconds <= 0:
        return 0  # 카운터 없음
    try:
        from streamlit_autorefresh import st_autorefresh
        return st_autorefresh(interval=seconds * 1000, key=key)
    except Exception:
        # 폴백: 페이지 전체 새로고침
        components.html(f"<meta http-equiv='refresh' content='{int(seconds)}'>", height=0)
        return 0


def render():
    st.header("🗳️ 실시간 설문 대시보드")

    with st.sidebar:
        st.subheader("⚙️ 설정")

        csv_or_sheet_url = st.text_input(
            "시트 URL 또는 CSV URL",
            placeholder="https://docs.google.com/spreadsheets/d/.../edit#gid=0 (그냥 붙여넣기)",
            help="시트 상단 주소를 그대로 붙여넣으면 자동으로 CSV export 주소로 변환합니다."
        )
        # 자동 새로고침
        refresh_sec = st.slider("자동 새로고침(초)", 0, 120, 10,
                                help="0은 자동 새로고침 끔")
        # 수동 새로고침
        force = st.button("🔁 지금 새로고침")

        # 미리보기: 변환된 CSV URL
        csv_preview = make_csv_export_url(csv_or_sheet_url) if csv_or_sheet_url else ""
        st.caption("↓ 변환된 CSV 주소 미리보기")
        st.text_area("CSV URL", csv_preview, height=60, label_visibility="collapsed")

        show_raw = st.checkbox("원시 데이터 보기", False)

    # 자동 새로고침 트리거(있을 때만)
    if csv_or_sheet_url and refresh_sec > 0:
        _auto_refresh(refresh_sec, key="auto_refresh_survey")

    # bust 값 계산: 자동 주기 + 수동 버튼
    if "_survey_force_bust" not in st.session_state:
        st.session_state["_survey_force_bust"] = 0
    if force:
        st.session_state["_survey_force_bust"] += 1

    # 자동 주기에 따른 bust(초 단위로 구간화해서 매 주기마다 값 변경)
    auto_bust = int(time.time() // max(1, refresh_sec)) if refresh_sec > 0 else 0
    bust_val = auto_bust + st.session_state["_survey_force_bust"]

    @st.cache_data(show_spinner=False)
    def _load(url: str, bust: int) -> pd.DataFrame:
        # bust가 함수 인자로 들어가므로, 값이 바뀔 때마다 캐시가 무효화됩니다.
        return load_csv_live(url, cache_bust=bust)

    if not csv_or_sheet_url:
        st.info("좌측에 **시트 URL**을 붙여넣으면 그래프가 나타납니다.")
        return

    try:
        df = _load(csv_or_sheet_url, bust_val)
    except Exception as e:
        st.error(f"CSV를 불러오는 중 오류: {e}")
        return

    if df.empty:
        st.warning("시트가 비어있거나 접근 권한이 없습니다. 공유 설정을 확인하세요(링크 공개 보기 권장).")
        return

    st.success(f"행 {len(df):,}개, 열 {len(df.columns)}개 로드됨 "
               f"(자동 새로고침: {refresh_sec}s, 강제갱신: {st.session_state['_survey_force_bust']})")
    if show_raw:
        st.dataframe(df, use_container_width=True)

    cols = df.columns.tolist()

    # ── 객관식/체크박스 막대그래프 ─────────────────────────────────
    st.subheader("📊 그래프")
    with st.expander("객관식/체크박스 빈도 막대그래프", expanded=True):
        if cols:
            col_mcq = st.selectbox("질문(객관식/체크박스 열 선택)", options=cols)
            normalize = st.checkbox("백분율(%)로 보기", True)
            if col_mcq:
                counts = parse_mcq_series(df[col_mcq])
                if counts:
                    s = pd.Series(counts).sort_values(ascending=False)
                    if normalize:
                        s = (s / s.sum() * 100).round(1)
                    st.bar_chart(s, use_container_width=True)
                    st.caption(f"총 응답 수: {sum(counts.values())} / 범주 수: {len(s)}")
                else:
                    st.info("집계할 응답이 없습니다.")
        else:
            st.info("표시할 열이 없습니다.")

    # ── 자유응답 워드클라우드 & 상위 단어 ─────────────────────────
    with st.expander("주관식(자유응답) 워드클라우드 & 상위 단어", expanded=True):
        if cols:
            col_text = st.selectbox("질문(자유응답 열 선택)", options=cols, index=min(1, len(cols)-1))
            max_words = st.slider("단어 수(워드클라우드)", 20, 300, 120)
            user_stop = st.text_area("제외할 단어(쉼표로 구분)", "입니다, 그리고, 또는, 정말")
            stopwords = [w.strip() for w in user_stop.split(",") if w.strip()]

            texts = df[col_text].dropna().astype(str).tolist()
            tokens = basic_tokenize_korean(texts)
            top_tokens = top_n_tokens(tokens, n=50, stopwords=stopwords)

            if top_tokens:
                st.write("상위 단어")
                st.dataframe(
                    pd.DataFrame(top_tokens, columns=["단어", "빈도"]),
                    use_container_width=True, hide_index=True
                )
            else:
                st.info("표시할 단어가 없습니다.")

            if WC_AVAILABLE and tokens:
                FONT_PATH = "assets/NanumGothic.ttf"  # 프로젝트에 폰트 파일을 두고 경로를 맞추세요.
                try:
                    wc = WordCloud(
                        width=900, height=500, background_color="white",
                        font_path=FONT_PATH, max_words=max_words,
                    ).generate(" ".join(tokens))
                    fig = plt.figure(figsize=(9, 5))
                    plt.imshow(wc, interpolation="bilinear")
                    plt.axis("off")
                    st.pyplot(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"워드클라우드를 표시하려면 한글 폰트(.ttf)가 필요합니다. 오류: {e}")
            elif not WC_AVAILABLE:
                st.info("워드클라우드를 쓰려면 requirements.txt에 `wordcloud`, `matplotlib`를 추가하세요.")
        else:
            st.info("표시할 열이 없습니다.")

    with st.expander("빠른 요약", expanded=False):
        st.write(df.describe(include="all").transpose())
