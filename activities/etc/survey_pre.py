"""사전 설문 — 수학 탐구 웹앱 활용 효과 연구"""
import streamlit as st
from survey_research_utils import (
    SHEET_PRE,
    get_config, has_submitted, submit_survey,
    current_user, is_student, is_admin,
)

META = {
    "title": "사전 설문",
    "description": "수학 탐구 웹앱 활용 효과 연구 — 사전 설문",
    "order": 51,
    "hidden": False,
}

SCALE = ["1 - 전혀 그렇지 않다", "2 - 그렇지 않다", "3 - 보통이다", "4 - 그렇다", "5 - 매우 그렇다"]

CATEGORIES = [
    {
        "id": "A",
        "title": "A. 수학 학습 흥미도",
        "desc": "수학 학습에 대한 흥미와 관심에 관한 문항입니다.",
        "questions": [
            ("[A]흥미1", "나는 수학 시간이 기다려진다."),
            ("[A]흥미2", "나는 수학 문제를 풀 때 즐거움을 느낀다."),
            ("[A]흥미3", "나는 수학이 실생활과 연결된다고 느낀다."),
            ("[A]흥미4", "나는 새로운 수학 개념을 배울 때 설레는 편이다."),
        ],
        "reverse": [],
    },
    {
        "id": "B",
        "title": "B. 수학 자기효능감",
        "desc": "수학 학습에 대한 자신감에 관한 문항입니다.",
        "questions": [
            ("[B]효능1", "나는 새로운 수학 개념을 스스로 이해할 수 있다고 생각한다."),
            ("[B]효능2", "나는 어려운 수학 문제도 노력하면 풀 수 있다고 생각한다."),
            ("[B]효능3", "나는 수학 개념들 사이의 연결 관계를 스스로 찾아낼 수 있다고 생각한다."),
            ("[B]효능4", "나는 수학 문제를 풀기 위한 다양한 방법을 스스로 생각해낼 수 있다."),
        ],
        "reverse": [],
    },
    {
        "id": "C",
        "title": "C. 수학 불안감",
        "desc": "수학 학습 시 느끼는 불안감에 관한 문항입니다. (★ 역방향 문항)",
        "questions": [
            ("[C]불안1", "★ 수학 시험이 다가오면 불안하고 초조해진다."),
            ("[C]불안2", "★ 수학 문제가 잘 풀리지 않으면 포기하고 싶어진다."),
            ("[C]불안3", "★ 수학은 나에게 너무 어렵게 느껴진다."),
        ],
        "reverse": ["[C]불안1", "[C]불안2", "[C]불안3"],
    },
    {
        "id": "D",
        "title": "D. ICT 활용 학습 태도",
        "desc": "디지털 도구를 활용한 수학 학습에 대한 생각을 묻는 문항입니다.",
        "questions": [
            ("[D]ICT1", "나는 디지털 도구를 활용하면 수학 개념을 더 잘 이해할 수 있을 것 같다."),
            ("[D]ICT2", "나는 시각적 자료(그래프, 애니메이션)가 수학 이해에 도움이 된다고 생각한다."),
            ("[D]ICT3", "나는 인터랙티브(직접 조작하는) 학습 도구에 관심이 있다."),
        ],
        "reverse": [],
    },
    {
        "id": "E",
        "title": "E. 수학적 시각화에 대한 인식",
        "desc": "수학 개념의 시각적 표현에 관한 생각을 묻는 문항입니다.",
        "questions": [
            ("[E]시각1", "나는 그래프나 그림으로 표현된 수학 개념이 더 이해하기 쉽다."),
            ("[E]시각2", "나는 수학 공식을 외우는 것보다 개념의 원리를 이해하는 것이 더 중요하다고 생각한다."),
            ("[E]시각3", "나는 수학 개념이 변화하는 과정을 눈으로 보면서 배우고 싶다."),
        ],
        "reverse": [],
    },
    {
        "id": "F",
        "title": "F. 수학 학습 방법에 대한 인식",
        "desc": "수학을 배우는 방법에 대한 생각을 묻는 문항입니다.",
        "questions": [
            ("[F]학습1", "나는 수학을 배울 때 직접 조작하거나 탐구하는 활동이 강의식 수업보다 효과적이라고 생각한다."),
            ("[F]학습2", "나는 수학 개념을 배울 때 실생활 맥락이 함께 제시되면 이해가 더 잘 된다."),
            ("[F]학습3", "나는 수학 학습에서 내가 직접 규칙이나 패턴을 발견하는 경험이 중요하다고 생각한다."),
        ],
        "reverse": [],
    },
]

TOTAL_PAGES = len(CATEGORIES)


def _progress_bar(page: int):
    frac = 0.0 if page <= 0 else min(page / TOTAL_PAGES, 1.0)
    st.progress(frac, text=f"진행률 {int(frac * 100)}%  ({max(0, page)}/{TOTAL_PAGES} 카테고리)")


def _render_consent():
    st.subheader("📋 설문 시작 전 안내")
    st.markdown("""
이 설문은 수학 탐구 웹앱이 여러분의 수학 학습에 어떤 도움이 되는지 알아보기 위한 것입니다.

- 응답 내용은 수업 연구 목적으로만 활용되며, **성적에 전혀 영향을 주지 않습니다.**
- 솔직하게 답할수록 더 좋은 수업을 만드는 데 도움이 됩니다.
- 참여를 원하지 않으면 언제든 중단할 수 있습니다.
""")
    with st.form(key="pre_consent_form"):
        agreed = st.checkbox(
            "안내 내용을 확인했으며, 설문에 참여합니다.",
            key="_pre_agree",
        )
        submitted = st.form_submit_button("설문 시작 →", type="primary", use_container_width=False)

    if submitted:
        if not agreed:
            st.error("체크박스에 체크해야 설문을 시작할 수 있습니다.")
        else:
            st.session_state["_pre_page"] = 1
            st.rerun()


def _save_page_answers(cat: dict, answers: dict):
    """현재 폼의 위젯 값을 answers 딕셔너리에 저장. 페이지 이동 전 반드시 호출."""
    for key, _ in cat["questions"]:
        val = st.session_state.get(f"pre_{key}")
        if val is not None:
            answers[key] = val


def _render_category_page(page: int, uid: str):
    cat = CATEGORIES[page - 1]
    is_last = (page == TOTAL_PAGES)
    reverse_keys = set(cat.get("reverse", []))

    # ── 누적 answers 딕셔너리 (페이지 이동해도 유지) ─────────────────────────
    if "_pre_answers" not in st.session_state:
        st.session_state["_pre_answers"] = {}
    answers = st.session_state["_pre_answers"]

    st.subheader(cat["title"])
    st.caption(cat["desc"])
    st.markdown("---")

    with st.form(key=f"pre_cat_{page}"):
        for key, label in cat["questions"]:
            suffix = " ★" if key in reverse_keys else ""
            # 이전에 저장된 답이 있으면 index로 복원 (페이지 이동 후 돌아올 때)
            saved = answers.get(key)
            idx = SCALE.index(saved) if saved in SCALE else None
            st.radio(
                f"**{label}**{suffix}",
                options=SCALE,
                index=idx,
                key=f"pre_{key}",
                horizontal=True,
            )
            st.markdown("")

        st.markdown("---")
        col_back, col_next = st.columns([1, 1])
        with col_back:
            back = st.form_submit_button("← 이전", use_container_width=True)
        with col_next:
            btn_label = "제출하기 ✓" if is_last else "다음 →"
            nxt = st.form_submit_button(btn_label, type="primary", use_container_width=True)

    # ── 폼 제출 처리 ──────────────────────────────────────────────────────────
    if back:
        _save_page_answers(cat, answers)          # 현재 페이지 답 저장
        st.session_state["_pre_answers"] = answers
        st.session_state["_pre_page"] = page - 1
        st.rerun()

    elif nxt:
        _save_page_answers(cat, answers)          # 현재 페이지 답 저장

        # 미응답 검사 (저장된 answers 기준)
        unanswered = [k for k, _ in cat["questions"] if not answers.get(k)]
        if unanswered:
            st.error(f"⚠️ {len(unanswered)}개 문항에 응답하지 않았습니다. 모든 문항에 응답해 주세요.")
            return

        st.session_state["_pre_answers"] = answers

        if is_last:
            # 최종 제출: 누적된 answers 딕셔너리를 한 번에 구글 시트로 전송
            with st.spinner("제출 중..."):
                ok = submit_survey(SHEET_PRE, uid, answers)
            if ok:
                st.session_state["_pre_page"] = TOTAL_PAGES + 1
                st.rerun()
        else:
            st.session_state["_pre_page"] = page + 1
            st.rerun()


def render():
    st.title("📋 사전 설문")
    st.caption("수학 탐구 웹앱 활용 효과 연구")

    user = current_user()

    if not user["authenticated"]:
        st.warning("로그인 후 참여할 수 있습니다.")
        return
    if is_admin():
        st.info("관리자 계정으로는 설문에 참여할 수 없습니다. 설문 관리 페이지를 이용해 주세요.")
        return
    if not is_student():
        st.warning("학생 계정으로만 참여할 수 있습니다.")
        return

    uid = user["id"]

    if not get_config("pre_active"):
        st.info("📌 사전 설문이 아직 시작되지 않았습니다. 선생님의 안내를 기다려 주세요.")
        return

    # 사용자가 바뀌면 이전 세션의 설문 진행 상태를 초기화
    if st.session_state.get("_pre_survey_uid") != uid:
        st.session_state["_pre_page"] = 0
        st.session_state.pop("_pre_answers", None)
        st.session_state["_pre_survey_uid"] = uid

    if has_submitted(SHEET_PRE, uid):
        st.success("✅ 사전 설문을 완료하셨습니다. 참여해 주셔서 감사합니다!")
        return

    if "_pre_page" not in st.session_state:
        st.session_state["_pre_page"] = 0

    page = st.session_state["_pre_page"]

    _progress_bar(page)
    st.markdown("---")

    if page == 0:
        _render_consent()
    elif 1 <= page <= TOTAL_PAGES:
        _render_category_page(page, uid)
    else:
        st.balloons()
        st.success("✅ 사전 설문이 완료되었습니다. 참여해 주셔서 감사합니다!")
        st.markdown(f"**{user['name']}** 학생의 소중한 응답이 저장되었습니다.")
