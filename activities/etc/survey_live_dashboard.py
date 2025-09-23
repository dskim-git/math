# activities/etc/survey_live_dashboard.py
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from survey_utils import (
    make_csv_export_url,
    load_csv_live,
    parse_mcq_series,
    basic_tokenize_korean,
    top_n_tokens,
)

META = {
    "title": "실시간 설문 대시보드",
    "description": "구글시트 CSV를 실시간으로 읽어 그래프/워드클라우드를 만듭니다.",
    "order": 10,
    # "hidden": True,
}

# 워드클라우드(선택)
WC_AVAILABLE = True
try:
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
except Exception:
    WC_AVAILABLE = False


def _auto_refresh(seconds: int, key: str = "auto_refresh_survey"):
    """최신 스트림릿은 st.autorefresh, 구버전은 meta refresh로 폴백."""
    if seconds <= 0:
        return
    try:
        st.autorefresh(interval=seconds * 1000, key=key)  # type: ignore[attr-defined]
    except Exception:
        components.html(f"<meta http-equiv='refresh' content='{int(seconds)}'>", height=0)


def render():
    st.header("🗳️ 실시간 설문 대시보드")

    with st.sidebar:
        st.subheader("⚙️ 데이터 소스")
        csv_or_sheet_url = st.text_input(
            "시트 URL 또는 CSV 내보내기 URL",
            placeholder=(
                "예) https://docs.google.com/spreadsheets/d/FILE_ID/edit#gid=0 "
                "또는 https://docs.google.com/spreadsheets/d/FILE_ID/export?format=csv&gid=0"
            ),
            help=(
                "① 시트를 열고 주소표시줄의 링크 그대로 붙여도 됩니다.\n"
                "   (앱이 자동으로 CSV 내보내기 주소로 변환)\n"
                "② 만약 '웹에 게시' 링크를 쓰면 반영이 늦을 수 있어요. "
                "가능하면 export?format=csv&gid=... 형태가 가장 빠릅니다."
            ),
        )

        st.caption("🔗 변환된 CSV 주소(읽기 전용)")
        csv_preview = make_csv_export_url(csv_or_sheet_url) if csv_or_sheet_url else ""
        st.text_area("CSV URL", csv_preview, height=60, label_visibility="collapsed")

        st.subheader("🔁 새로고침")
        refresh_sec = st.slider("자동 새로고침(초)", 0, 60, 10, help="0이면 자동 새로고침 없음")
        manual = st.button("🔄 지금 새로고침")

        show_raw = st.checkbox("원시 데이터 보기", False)

    # 자동 새로고침
    if csv_or_sheet_url and refresh_sec > 0:
        _auto_refresh(refresh_sec, key="auto_refresh_survey")

    # 캐시 무력화용 'bust' 값 생성
    if manual:
        bust = int(time.time())  # 버튼 누를 때마다 강제 재다운로드
    elif refresh_sec > 0:
        bust = int(time.time() // max(refresh_sec, 1))  # n초 단위로 값이 바뀜
    else:
        bust = 0  # 같은 세션 동안 캐시 유지

    @st.cache_data(show_spinner=False)
    def _load(url: str, bust_val: int) -> pd.DataFrame:
        return load_csv_live(url, cache_bust=bust_val)

    if not csv_or_sheet_url:
        st.info("좌측에 **시트 URL 또는 CSV URL**을 입력하면 그래프가 나타납니다.")
        return

    try:
        df = _load(csv_or_sheet_url, bust)
    except Exception as e:
        st.error(f"CSV를 불러오는 중 오류가 발생했어요: {e}")
        return

    if df.empty:
        st.warning("시트가 비어있거나 접근이 불가합니다. 주소/공개 설정을 확인해 주세요.")
        return

    st.success(f"행 {len(df):,}개 · 열 {len(df.columns)}개 로드됨 · {time.strftime('%H:%M:%S')} 기준")
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
                    st.caption(f"총 응답 수: {int(s.sum() if not normalize else (s.sum()/100*len(s)))} / 범주 수: {len(s)}")
                else:
                    st.info("집계할 응답이 없습니다.")
        else:
            st.info("표시할 열이 없습니다.")

    # ── 자유응답 워드클라우드 & 상위 단어 ─────────────────────────
    with st.expander("주관식(자유응답) 워드클라우드 & 상위 단어", expanded=True):
        if cols:
            # 보통 첫 열이 타임스탬프인 경우가 많아 index=1을 기본값으로 둠
            default_idx = 1 if len(cols) > 1 else 0
            col_text = st.selectbox("질문(자유응답 열 선택)", options=cols, index=default_idx)
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
                FONT_PATH = "assets/NanumGothic.ttf"  # 프로젝트에 폰트 파일을 두세요.
                try:
                    wc = WordCloud(
                        width=900, height=500,
                        background_color="white",
                        font_path=FONT_PATH,
                        max_words=max_words,
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
