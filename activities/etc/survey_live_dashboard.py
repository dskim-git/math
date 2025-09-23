# activities/etc/survey_live_dashboard.py
import streamlit as st
import pandas as pd

from survey_utils import (
    load_published_csv, parse_mcq_series,
    basic_tokenize_korean, top_n_tokens
)

# ── 메타 ─────────────────────────────────────────
META = {
    "title": "실시간 설문 대시보드",
    "description": "구글폼→시트(웹에 게시·CSV)를 실시간으로 읽어 그래프/워드클라우드 표시",
    "order": 10,
    # "hidden": True,  # mini에 넣거나 숨기고 싶으면 True
}

# ── WordCloud 옵션(선택) ────────────────────────
# 워드클라우드를 쓰려면 wordcloud, matplotlib가 필요합니다.
# requirements.txt에: wordcloud, matplotlib 추가
WC_AVAILABLE = True
try:
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
except Exception:
    WC_AVAILABLE = False


def render():
    st.header("🗳️ 실시간 설문 대시보드")

    with st.sidebar:
        st.subheader("⚙️ 설정")
        csv_url = st.text_input(
            "구글시트(웹에 게시·CSV) 주소",
            placeholder="https://docs.google.com/spreadsheets/d/e/2PACX-.../pub?gid=0&single=true&output=csv",
            help="시트 > 파일 > 웹에 게시 > (특정 시트 탭, 형식: CSV) 후 나온 링크를 붙여넣으세요."
        )
        refresh_sec = st.slider("자동 새로고침(초)", 5, 60, 10)
        show_raw = st.checkbox("원시 데이터 보기", False)

        # 자동 새로고침
        st.autorefresh(interval=refresh_sec * 1000, key="auto_refresh_survey")

    # 데이터 로드 (TTL=refresh_sec-1로 캐시)
    @st.cache_data(ttl=30)
    def _load(url: str) -> pd.DataFrame:
        return load_published_csv(url)

    if not csv_url:
        st.info("좌측에 **CSV 주소**를 입력하면 그래프가 나타납니다.")
        return

    try:
        df = _load(csv_url)
    except Exception as e:
        st.error(f"CSV를 불러오는 중 오류가 발생했어요: {e}")
        return

    if df.empty:
        st.warning("시트가 비어있거나 접근이 불가합니다. 주소/공개 설정을 확인해 주세요.")
        return

    st.success(f"행 {len(df):,}개, 열 {len(df.columns)}개 로드됨")

    if show_raw:
        st.dataframe(df, use_container_width=True)

    # ── 컬럼 선택 UI ─────────────────────────────
    st.subheader("📊 그래프")
    cols = df.columns.tolist()

    # 1) 객관식/체크박스 그래프(막대)
    with st.expander("객관식/체크박스 빈도 막대그래프", expanded=True):
        col_mcq = st.selectbox("질문(객관식/체크박스 열 선택)", options=cols)
        normalize = st.checkbox("백분율(%)로 보기", True)
        if col_mcq:
            counts = parse_mcq_series(df[col_mcq])
            if counts:
                s = pd.Series(counts).sort_values(ascending=False)
                if normalize:
                    s = (s / s.sum() * 100).round(1)
                    st.bar_chart(s, use_container_width=True)
                    st.caption(f"총 응답 수: {int(s.sum() if not normalize else counts.total())} / 범주 수: {len(s)}")
                else:
                    st.bar_chart(s, use_container_width=True)
                    st.caption(f"총 응답 수: {counts.total()} / 범주 수: {len(s)}")
            else:
                st.info("집계할 응답이 없습니다.")

    # 2) 자유응답(워드클라우드/상위 토큰표)
    with st.expander("주관식(자유응답) 워드클라우드 & 상위 단어", expanded=True):
        col_text = st.selectbox("질문(자유응답 열 선택)", options=cols, index=min(1, len(cols)-1))
        max_words = st.slider("단어 수(워드클라우드)", 20, 300, 120)
        user_stop = st.text_area("제외할 단어(쉼표로 구분)", "입니다, 그리고, 또는, 학생, 수업, 정말")
        stopwords = [w.strip() for w in user_stop.split(",") if w.strip()]

        if col_text:
            texts = df[col_text].dropna().astype(str).tolist()
            tokens = basic_tokenize_korean(texts)
            top_tokens = top_n_tokens(tokens, n=50, stopwords=stopwords)

            # 상위 토큰 테이블
            if top_tokens:
                st.write("상위 단어")
                st.dataframe(
                    pd.DataFrame(top_tokens, columns=["단어", "빈도"]),
                    use_container_width=True, hide_index=True
                )
            else:
                st.info("표시할 단어가 없습니다(모두 stopwords로 제외되었거나 응답이 비어있습니다).")

            # 워드클라우드
            if WC_AVAILABLE and tokens:
                # 한글 폰트 경로 지정 (프로젝트에 폰트를 넣어 사용 권장)
                # 예: assets/NanumGothic.ttf 를 추가하고 아래 경로 지정
                FONT_PATH = "assets/NanumGothic.ttf"  # 경로에 맞게 수정
                try:
                    wc = WordCloud(
                        width=900, height=500,
                        background_color="white",
                        font_path=FONT_PATH,
                        max_words=max_words,
                    ).generate(" ".join(tokens))
                    import matplotlib.pyplot as plt
                    fig = plt.figure(figsize=(9, 5))
                    plt.imshow(wc, interpolation="bilinear")
                    plt.axis("off")
                    st.pyplot(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"워드클라우드를 표시하려면 한글 폰트(.ttf)가 필요합니다. 현재 오류: {e}")
            elif not WC_AVAILABLE:
                st.info("워드클라우드를 쓰려면 requirements.txt에 `wordcloud`, `matplotlib`를 추가하세요.")

    # 3) 빠른 요약(선택)
    with st.expander("빠른 요약", expanded=False):
        st.write(df.describe(include="all").transpose())
