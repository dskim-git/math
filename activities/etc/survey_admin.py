"""설문 관리 대시보드 — 관리자 전용"""
import streamlit as st
import pandas as pd
from survey_research_utils import (
    SHEET_PRE, SHEET_POST, PRE_HEADER, POST_HEADER,
    get_config, set_config,
    current_user, is_admin,
    _get_spreadsheet, _get_or_create_ws,
)

META = {
    "title": "설문 관리",
    "description": "사전/사후 설문 활성화 및 응답 결과 조회 (관리자 전용)",
    "order": 50,
    "hidden": False,
}

# ── 문항 키 → 질문 전체 텍스트 매핑 ──────────────────────────────────────────
QUESTION_LABELS: dict[str, str] = {
    # A. 수학 학습 흥미도
    "[A]흥미1": "A-1. 나는 수학 시간이 기다려진다.",
    "[A]흥미2": "A-2. 나는 수학 문제를 풀 때 즐거움을 느낀다.",
    "[A]흥미3": "A-3. 나는 수학이 실생활과 연결된다고 느낀다.",
    "[A]흥미4": "A-4. 나는 새로운 수학 개념을 배울 때 설레는 편이다.",
    # B. 수학 자기효능감
    "[B]효능1": "B-1. 나는 새로운 수학 개념을 스스로 이해할 수 있다고 생각한다.",
    "[B]효능2": "B-2. 나는 어려운 수학 문제도 노력하면 풀 수 있다고 생각한다.",
    "[B]효능3": "B-3. 나는 수학 개념들 사이의 연결 관계를 스스로 찾아낼 수 있다고 생각한다.",
    "[B]효능4": "B-4. 나는 수학 문제를 풀기 위한 다양한 방법을 스스로 생각해낼 수 있다.",
    # C. 수학 불안감 (★ 역채점)
    "[C]불안1": "C-1★. 수학 시험이 다가오면 불안하고 초조해진다.",
    "[C]불안2": "C-2★. 수학 문제가 잘 풀리지 않으면 포기하고 싶어진다.",
    "[C]불안3": "C-3★. 수학은 나에게 너무 어렵게 느껴진다.",
    # D. ICT 활용 학습 태도
    "[D]ICT1":  "D-1. 디지털 도구를 활용하면 수학 개념을 더 잘 이해할 수 있을 것 같다.",
    "[D]ICT2":  "D-2. 시각적 자료(그래프, 애니메이션)가 수학 이해에 도움이 된다.",
    "[D]ICT3":  "D-3. 인터랙티브(직접 조작하는) 학습 도구에 관심이 있다.",
    # E. 수학적 시각화
    "[E]시각1": "E-1. 그래프나 그림으로 표현된 수학 개념이 더 이해하기 쉽다.",
    "[E]시각2": "E-2. 수학 공식을 외우는 것보다 개념의 원리를 이해하는 것이 더 중요하다.",
    "[E]시각3": "E-3. 수학 개념이 변화하는 과정을 눈으로 보면서 배우고 싶다.",
    # F. 수학 학습 방법
    "[F]학습1": "F-1. 직접 조작하거나 탐구하는 활동이 강의식 수업보다 효과적이라고 생각한다.",
    "[F]학습2": "F-2. 수학 개념을 배울 때 실생활 맥락이 함께 제시되면 이해가 더 잘 된다.",
    "[F]학습3": "F-3. 수학 학습에서 내가 직접 규칙이나 패턴을 발견하는 경험이 중요하다.",
    # G. 웹앱 활용 경험
    "[G]앱1":   "G-1. 웹앱의 시각적 자료(그래프, 시뮬레이션)는 개념 이해에 도움이 되었다.",
    "[G]앱2":   "G-2. 웹앱의 인터랙티브 활동은 수업에 대한 흥미를 높여주었다.",
    "[G]앱3":   "G-3. 웹앱은 교과서만으로 이해하기 어려운 개념을 이해하는 데 도움이 되었다.",
    # H. 개념 이해 효과
    "[H]개념1": "H-1. 웹앱 활동을 통해 수학 개념의 원리를 더 잘 이해하게 되었다.",
    "[H]개념2": "H-2. 값을 직접 바꿔가며 결과를 확인하는 과정이 개념 이해에 효과적이었다.",
    "[H]개념3": "H-3. 웹앱 활동 후 비슷한 유형의 문제를 스스로 풀어보고 싶다는 생각이 들었다.",
    # I. 수업 방식 선호
    "[I]수업1": "I-1. 웹앱 활용 수업이 기존 강의식 수업보다 더 효과적이었다.",
    "[I]수업2": "I-2. 앞으로도 이와 같은 디지털 탐구 활동이 수업에 포함되었으면 한다.",
}

# ── 시트 전체 로드 ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=30, show_spinner=False)
def _load_sheet(sheet_name: str, _bust: int = 0) -> pd.DataFrame:
    try:
        sh = _get_spreadsheet()
        if sh is None:
            return pd.DataFrame()
        header = PRE_HEADER if sheet_name == SHEET_PRE else POST_HEADER
        ws = _get_or_create_ws(sh, sheet_name, header)
        records = ws.get_all_records(numericise_ignore=["all"])
        return pd.DataFrame(records) if records else pd.DataFrame(columns=header)
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return pd.DataFrame()


def _score_col(col: str) -> float | None:
    """'3 - 보통이다' 형식에서 숫자만 추출."""
    try:
        return float(str(col).split("-")[0].strip().split()[0])
    except Exception:
        return None


def _add_score_cols(df: pd.DataFrame, likert_cols: list[str]) -> pd.DataFrame:
    """리커트 문항을 숫자형 열로 추가."""
    for col in likert_cols:
        if col in df.columns:
            df[col + "_점수"] = df[col].apply(_score_col)
    return df


def _render_stats(df: pd.DataFrame, likert_cols: list[str], label: str):
    """카테고리별 평균 점수 표와 막대 차트."""
    if df.empty:
        st.info("응답 데이터가 없습니다.")
        return

    df2 = _add_score_cols(df.copy(), likert_cols)
    score_cols = [c + "_점수" for c in likert_cols if c in df.columns]

    if not score_cols:
        st.info("집계할 점수 열이 없습니다.")
        return

    means = df2[score_cols].mean()
    # 키를 전체 질문 텍스트로 변환
    means.index = [
        QUESTION_LABELS.get(c.replace("_점수", ""), c.replace("_점수", ""))
        for c in means.index
    ]

    means_df = means.reset_index()
    means_df.columns = ["문항", "평균 점수"]
    means_df["평균 점수"] = means_df["평균 점수"].round(2)

    st.markdown(f"**{label} 문항별 평균 점수** (1~5점)")
    st.bar_chart(means, use_container_width=True)
    st.dataframe(means_df, use_container_width=True, hide_index=True)


# ── 학년/학급 필터 ─────────────────────────────────────────────────────────────
def _filter_df(df: pd.DataFrame, key_prefix: str = "pre") -> pd.DataFrame:
    if df.empty:
        return df

    grades  = sorted(df["학년"].dropna().unique().tolist()) if "학년" in df.columns else []
    classes = sorted(df["학급"].dropna().unique().tolist()) if "학급" in df.columns else []

    col1, col2 = st.columns(2)
    with col1:
        sel_grade = st.multiselect("학년 필터", options=grades, default=grades, key=f"_adm_grade_{key_prefix}")
    with col2:
        sel_class = st.multiselect("학급 필터", options=classes, default=classes, key=f"_adm_class_{key_prefix}")

    mask = pd.Series([True] * len(df), index=df.index)
    if sel_grade and "학년" in df.columns:
        mask &= df["학년"].astype(str).isin([str(g) for g in sel_grade])
    if sel_class and "학급" in df.columns:
        mask &= df["학급"].astype(str).isin([str(c) for c in sel_class])

    return df[mask]


# ── CSV 다운로드 버튼 ──────────────────────────────────────────────────────────
def _download_btn(df: pd.DataFrame, filename: str):
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="⬇️ CSV 다운로드",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )


# ── 응답 현황 요약 ─────────────────────────────────────────────────────────────
def _render_response_summary(pre_df: pd.DataFrame, post_df: pd.DataFrame):
    st.subheader("📊 응답 현황")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("사전 설문 응답 수", len(pre_df))
    with c2:
        st.metric("사후 설문 응답 수", len(post_df))

    if not pre_df.empty and "학년" in pre_df.columns and "학급" in pre_df.columns:
        st.markdown("**학년·학급별 사전 설문 응답 현황**")
        grp = pre_df.groupby(["학년", "학급"]).size().reset_index(name="응답 수")
        st.dataframe(grp, use_container_width=True, hide_index=True)


# ── 메인 렌더 ─────────────────────────────────────────────────────────────────
def render():
    st.title("🗂️ 설문 관리 대시보드")

    user = current_user()

    if not user["authenticated"] or not is_admin():
        st.error("관리자 계정으로 로그인해야 접근할 수 있습니다.")
        return

    # ════════════════════════════════════════════════════════════════════════
    # 섹션 1: 활성화 토글
    # ════════════════════════════════════════════════════════════════════════
    st.subheader("⚙️ 설문 활성화 설정")
    st.caption("설문을 활성화하면 학생들이 해당 설문에 참여할 수 있습니다.")

    pre_active  = get_config("pre_active")
    post_active = get_config("post_active")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**사전 설문**")
        status_pre = "🟢 활성화됨" if pre_active else "🔴 비활성화됨"
        st.markdown(status_pre)
        if pre_active:
            if st.button("사전 설문 비활성화", key="pre_off", type="secondary"):
                with st.spinner("저장 중..."):
                    ok = set_config("pre_active", False)
                if ok:
                    st.success("사전 설문이 비활성화되었습니다.")
                    st.rerun()
        else:
            if st.button("사전 설문 활성화", key="pre_on", type="primary"):
                with st.spinner("저장 중..."):
                    ok = set_config("pre_active", True)
                if ok:
                    st.success("사전 설문이 활성화되었습니다.")
                    st.rerun()

    with col2:
        st.markdown("**사후 설문**")
        status_post = "🟢 활성화됨" if post_active else "🔴 비활성화됨"
        st.markdown(status_post)
        if post_active:
            if st.button("사후 설문 비활성화", key="post_off", type="secondary"):
                with st.spinner("저장 중..."):
                    ok = set_config("post_active", False)
                if ok:
                    st.success("사후 설문이 비활성화되었습니다.")
                    st.rerun()
        else:
            if st.button("사후 설문 활성화", key="post_on", type="primary"):
                with st.spinner("저장 중..."):
                    ok = set_config("post_active", True)
                if ok:
                    st.success("사후 설문이 활성화되었습니다.")
                    st.rerun()

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    # 섹션 2: 데이터 로드
    # ════════════════════════════════════════════════════════════════════════
    bust = st.session_state.get("_adm_bust", 0)
    if st.button("🔁 데이터 새로고침"):
        st.session_state["_adm_bust"] = bust + 1
        st.cache_data.clear()
        st.rerun()

    with st.spinner("데이터 불러오는 중..."):
        pre_df  = _load_sheet(SHEET_PRE,  bust)
        post_df = _load_sheet(SHEET_POST, bust)

    _render_response_summary(pre_df, post_df)
    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    # 섹션 3: 사전 설문 결과
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("📋 사전 설문 결과 조회", expanded=True):
        if pre_df.empty:
            st.info("사전 설문 응답이 없습니다.")
        else:
            st.markdown(f"총 **{len(pre_df)}명** 응답")
            filtered_pre = _filter_df(pre_df, key_prefix="pre")
            st.markdown(f"필터 적용 후: **{len(filtered_pre)}명**")

            likert_pre = [c for c in PRE_HEADER[4:] if not c.startswith("[J]")]
            _render_stats(filtered_pre, likert_pre, "사전 설문")

            with st.expander("원시 데이터 보기"):
                st.dataframe(filtered_pre, use_container_width=True, hide_index=True)
            _download_btn(filtered_pre, "pre_survey_results.csv")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    # 섹션 4: 사후 설문 결과
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("📋 사후 설문 결과 조회", expanded=True):
        if post_df.empty:
            st.info("사후 설문 응답이 없습니다.")
        else:
            st.markdown(f"총 **{len(post_df)}명** 응답")
            filtered_post = _filter_df(post_df, key_prefix="post")
            st.markdown(f"필터 적용 후: **{len(filtered_post)}명**")

            likert_post = [c for c in POST_HEADER[4:] if not c.startswith("[J]")]
            _render_stats(filtered_post, likert_post, "사후 설문")

            with st.expander("원시 데이터 보기"):
                st.dataframe(filtered_post, use_container_width=True, hide_index=True)
            _download_btn(filtered_post, "post_survey_results.csv")

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    # 섹션 5: 사전-사후 비교 (공통 학번 기준)
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("📈 사전-사후 비교 (공통 응답자)", expanded=False):
        if pre_df.empty or post_df.empty:
            st.info("사전·사후 설문 응답이 모두 있어야 비교가 가능합니다.")
        else:
            common_ids = set(pre_df["학번"].astype(str)) & set(post_df["학번"].astype(str))
            st.markdown(f"사전·사후 **모두 응답한 학생 수: {len(common_ids)}명**")

            if common_ids:
                # 공통 리커트 문항 (사전·사후에 동일하게 존재하는 열)
                common_likert = [
                    "[A]흥미1", "[A]흥미2",
                    "[B]효능1", "[B]효능2",
                    "[C]불안1", "[C]불안2",
                    "[D]ICT1",  "[D]ICT2",
                    "[E]시각1", "[E]시각2",
                    "[F]학습1", "[F]학습2",
                ]

                pre_sub  = pre_df[pre_df["학번"].astype(str).isin(common_ids)]
                post_sub = post_df[post_df["학번"].astype(str).isin(common_ids)]

                rows = []
                for col in common_likert:
                    if col not in pre_sub.columns or col not in post_sub.columns:
                        continue
                    pre_mean  = pre_sub[col].apply(_score_col).mean()
                    post_mean = post_sub[col].apply(_score_col).mean()
                    diff      = (post_mean - pre_mean) if (pre_mean and post_mean) else None
                    rows.append({
                        "문항": QUESTION_LABELS.get(col, col),
                        "사전 평균": round(pre_mean, 2) if pre_mean else "-",
                        "사후 평균": round(post_mean, 2) if post_mean else "-",
                        "변화량 (사후-사전)": round(diff, 2) if diff is not None else "-",
                    })

                if rows:
                    cmp_df = pd.DataFrame(rows)
                    st.dataframe(cmp_df, use_container_width=True, hide_index=True)
                    _download_btn(cmp_df, "pre_post_comparison.csv")

    # ════════════════════════════════════════════════════════════════════════
    # 섹션 6: 서술형 응답 (사후)
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("✏️ 서술형 응답 (사후 설문 J)", expanded=False):
        if post_df.empty:
            st.info("사후 설문 응답이 없습니다.")
        elif "[J]서술1" not in post_df.columns:
            st.info("서술형 응답 열이 없습니다.")
        else:
            for q_col, q_label in [
                ("[J]서술1", "가장 도움이 되었던 활동"),
                ("[J]서술2", "수학에 대한 생각·태도 변화"),
            ]:
                if q_col in post_df.columns:
                    st.markdown(f"**{q_label}**")
                    answers_only = post_df[post_df[q_col].astype(str).str.strip() != ""]
                    for _, row in answers_only.iterrows():
                        st.markdown(
                            f"> {row.get('학년', '?')}학년 {row.get('학급', '?')}반 — "
                            f"{row[q_col]}"
                        )
                    st.markdown("")
