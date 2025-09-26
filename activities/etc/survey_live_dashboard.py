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

        # ⬇️ PC/모바일 입력칸을 분리
        pc_url = st.text_input(
            "PC에서 복사한 시트/CSV URL",
            placeholder="https://docs.google.com/spreadsheets/d/.../edit#gid=0 (PC에서 복사)",
            help="PC의 브라우저 주소창에서 복사한 링크를 붙여넣으세요."
        )
        mobile_url = st.text_input(
            "모바일에서 복사한 시트/CSV URL",
            placeholder="https://docs.google.com/spreadsheets/d/... (모바일/드라이브앱 공유 링크 등)",
            help="모바일 브라우저/드라이브 앱에서 복사한 링크를 붙여넣으세요."
        )

        # 둘 다 있으면 어떤 걸 쓸지 선택, 하나만 있으면 그걸 자동 선택
        source_choice = None
        options = []
        if mobile_url:
            options.append("모바일 URL")
        if pc_url:
            options.append("PC URL")

        if len(options) >= 2:
            source_choice = st.radio("사용할 주소 선택", options, index=0, horizontal=True)
        elif len(options) == 1:
            source_choice = options[0]
        else:
            source_choice = None  # 아직 아무 것도 입력 안 됨

        # 실제로 사용할 URL 결정
        if source_choice == "모바일 URL":
            active_url = mobile_url
        elif source_choice == "PC URL":
            active_url = pc_url
        else:
            active_url = ""

        # 자동 새로고침
        refresh_sec = st.slider("자동 새로고침(초)", 0, 120, 10, help="0은 자동 새로고침 끔")
        # 수동 새로고침
        force = st.button("🔁 지금 새로고침")

        # ⬇️ 미리보기: 각 URL을 CSV export로 변환해 보여주고, 현재 사용 중인 URL도 표시
        preview_pc = make_csv_export_url(pc_url) if pc_url else ""
        preview_mobile = make_csv_export_url(mobile_url) if mobile_url else ""
        preview_active = make_csv_export_url(active_url) if active_url else ""

        st.caption("PC → CSV 주소 미리보기")
        st.text_area("PC CSV URL", preview_pc, height=60, label_visibility="collapsed")

        st.caption("모바일 → CSV 주소 미리보기")
        st.text_area("모바일 CSV URL", preview_mobile, height=60, label_visibility="collapsed")

        st.caption("✅ 현재 사용 중 CSV 주소")
        st.text_area("Active CSV URL", preview_active, height=60, label_visibility="collapsed")

        show_raw = st.checkbox("원시 데이터 보기", False)

    # 자동 새로고침 트리거(있을 때만)
    if active_url and refresh_sec > 0:
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

    if not active_url:
        st.info("좌측에서 **PC 또는 모바일 URL**을 붙여넣으면 그래프가 나타납니다.")
        return

    try:
        df = _load(active_url, bust_val)
    except Exception as e:
        st.error(f"CSV를 불러오는 중 오류: {e}")
        return

    if df.empty:
        st.warning("시트가 비어있거나 접근 권한이 없습니다. 공유 설정을 확인하세요(링크 공개 보기 권장).")
        return

    st.success(
        f"행 {len(df):,}개, 열 {len(df.columns)}개 로드됨 "
        f"(자동 새로고침: {refresh_sec}s, 강제갱신: {st.session_state['_survey_force_bust']})"
    )
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