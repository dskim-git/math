"""사후 설문 — 수학 탐구 웹앱 활용 효과 연구"""
import streamlit as st
from survey_research_utils import (
    SHEET_POST,
    get_config, has_submitted, submit_survey,
    current_user, is_student, is_admin,
)

META = {
    "title": "사후 설문",
    "description": "수학 탐구 웹앱 활용 효과 연구 — 사후 설문",
    "order": 52,
    "hidden": False,
}

SCALE = ["1 - 전혀 그렇지 않다", "2 - 그렇지 않다", "3 - 보통이다", "4 - 그렇다", "5 - 매우 그렇다"]

CATEGORIES = [
    {
        "id": "AB",
        "title": "A. 수학 학습 흥미도 / B. 수학 자기효능감",
        "desc": "수학 학습에 대한 흥미와 자신감에 관한 문항입니다.",
        "type": "likert",
        "questions": [
            ("[A]흥미1", "나는 수학 시간이 기다려진다."),
            ("[A]흥미2", "나는 수학이 실생활과 연결된다고 느낀다."),
            ("[B]효능1", "나는 새로운 수학 개념을 스스로 이해할 수 있다고 생각한다."),
            ("[B]효능2", "나는 어려운 수학 문제도 노력하면 풀 수 있다고 생각한다."),
        ],
        "reverse": [],
    },
    {
        "id": "CD",
        "title": "C. 수학 불안감 / D. ICT 활용 학습 태도",
        "desc": "수학 불안감과 디지털 도구 활용 학습에 대한 문항입니다. (★ 역방향 문항)",
        "type": "likert",
        "questions": [
            ("[C]불안1", "★ 수학 시험이 다가오면 불안하고 초조해진다."),
            ("[C]불안2", "★ 수학 문제가 잘 풀리지 않으면 포기하고 싶어진다."),
            ("[D]ICT1",  "나는 디지털 도구를 활용하면 수학 개념을 더 잘 이해할 수 있다."),
            ("[D]ICT2",  "나는 시각적 자료(그래프, 애니메이션)가 수학 이해에 도움이 된다."),
        ],
        "reverse": ["[C]불안1", "[C]불안2"],
    },
    {
        "id": "EF",
        "title": "E. 수학적 시각화 / F. 수학 학습 방법",
        "desc": "수학 개념의 시각적 표현과 학습 방법에 관한 문항입니다.",
        "type": "likert",
        "questions": [
            ("[E]시각1", "나는 그래프나 그림으로 표현된 수학 개념이 더 이해하기 쉽다."),
            ("[E]시각2", "나는 수학 개념이 변화하는 과정을 눈으로 보면서 배우고 싶다."),
            ("[F]학습1", "직접 조작하거나 탐구하는 활동이 강의식 수업보다 효과적이라고 생각한다."),
            ("[F]학습2", "수학 학습에서 내가 직접 규칙이나 패턴을 발견하는 경험이 중요하다고 생각한다."),
        ],
        "reverse": [],
    },
    {
        "id": "G",
        "title": "G. 웹앱 활용 경험",
        "desc": "이번 수업에서 사용한 수학 탐구 웹앱에 대한 경험을 묻는 문항입니다.",
        "type": "likert",
        "questions": [
            ("[G]앱1", "이 웹앱의 시각적 자료(그래프, 시뮬레이션)는 개념 이해에 도움이 되었다."),
            ("[G]앱2", "이 웹앱의 인터랙티브 활동은 수업에 대한 흥미를 높여주었다."),
            ("[G]앱3", "이 웹앱은 교과서만으로 이해하기 어려운 개념을 이해하는 데 도움이 되었다."),
        ],
        "reverse": [],
    },
    {
        "id": "HI",
        "title": "H. 개념 이해 효과 / I. 수업 방식 선호",
        "desc": "웹앱 활용 후 개념 이해와 수업 방식에 대한 생각을 묻는 문항입니다.",
        "type": "likert",
        "questions": [
            ("[H]개념1", "이 웹앱 활동을 통해 수학 개념의 원리를 더 잘 이해하게 되었다."),
            ("[H]개념2", "이 웹앱에서 값을 직접 바꿔가며 결과를 확인하는 과정이 개념 이해에 효과적이었다."),
            ("[H]개념3", "이 웹앱 활동 후 비슷한 유형의 문제를 스스로 풀어보고 싶다는 생각이 들었다."),
            ("[I]수업1", "이 웹앱을 활용한 수업 방식이 기존 강의식 수업보다 더 효과적이었다."),
            ("[I]수업2", "앞으로도 이와 같은 디지털 탐구 활동이 수학 수업에 포함되었으면 한다."),
        ],
        "reverse": [],
    },
    {
        "id": "J",
        "title": "J. 자유 서술",
        "desc": "아래 질문에 자유롭게 답변해 주세요. (비워두어도 됩니다.)",
        "type": "text",
        "questions": [
            ("[J]서술1", "이 웹앱을 사용하면서 수학 개념 이해에 가장 도움이 되었던 활동은 무엇인가요? 이유도 함께 써주세요."),
            ("[J]서술2", "이 웹앱이 수학에 대한 나의 생각이나 태도에 어떤 변화를 주었나요?"),
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
이 설문은 수학 탐구 웹앱을 활용한 수업이 여러분의 수학 학습에 어떤 도움이 되었는지 알아보기 위한 것입니다.

- 응답 내용은 수업 연구 목적으로만 활용되며, **성적에 전혀 영향을 주지 않습니다.**
- 솔직하게 답할수록 더 좋은 수업을 만드는 데 도움이 됩니다.
- 참여를 원하지 않으면 언제든 중단할 수 있습니다.
""")
    with st.form(key="post_consent_form"):
        agreed = st.checkbox(
            "안내 내용을 확인했으며, 설문에 참여합니다.",
            key="_post_agree",
        )
        submitted = st.form_submit_button("설문 시작 →", type="primary", use_container_width=False)

    if submitted:
        if not agreed:
            st.error("체크박스에 체크해야 설문을 시작할 수 있습니다.")
        else:
            st.session_state["_post_page"] = 1
            st.rerun()


def _save_page_answers(cat: dict, answers: dict):
    """현재 폼의 위젯 값을 answers 딕셔너리에 저장. 페이지 이동 전 반드시 호출."""
    for key, _ in cat["questions"]:
        val = st.session_state.get(f"post_{key}")
        if val is not None:
            answers[key] = val


def _render_category_page(page: int, uid: str):
    cat = CATEGORIES[page - 1]
    is_last = (page == TOTAL_PAGES)
    reverse_keys = set(cat.get("reverse", []))

    # ── 누적 answers 딕셔너리 ──────────────────────────────────────────────
    if "_post_answers" not in st.session_state:
        st.session_state["_post_answers"] = {}
    answers = st.session_state["_post_answers"]

    st.subheader(cat["title"])
    st.caption(cat["desc"])
    st.markdown("---")

    with st.form(key=f"post_cat_{page}"):
        if cat["type"] == "likert":
            for key, label in cat["questions"]:
                suffix = " ★" if key in reverse_keys else ""
                saved = answers.get(key)
                idx = SCALE.index(saved) if saved in SCALE else None
                st.radio(
                    f"**{label}**{suffix}",
                    options=SCALE,
                    index=idx,
                    key=f"post_{key}",
                    horizontal=True,
                )
                st.markdown("")

        elif cat["type"] == "text":
            for key, label in cat["questions"]:
                saved = answers.get(key, "")
                st.text_area(
                    f"**{label}**",
                    value=saved,
                    key=f"post_{key}",
                    height=100,
                    placeholder="자유롭게 작성해 주세요. (비워두어도 됩니다.)",
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
        _save_page_answers(cat, answers)
        st.session_state["_post_answers"] = answers
        st.session_state["_post_page"] = page - 1
        st.rerun()

    elif nxt:
        _save_page_answers(cat, answers)

        if cat["type"] == "likert":
            unanswered = [k for k, _ in cat["questions"] if not answers.get(k)]
            if unanswered:
                st.error(f"⚠️ {len(unanswered)}개 문항에 응답하지 않았습니다. 모든 문항에 응답해 주세요.")
                return

        st.session_state["_post_answers"] = answers

        if is_last:
            with st.spinner("제출 중..."):
                ok = submit_survey(SHEET_POST, uid, answers)
            if ok:
                st.session_state["_post_page"] = TOTAL_PAGES + 1
                st.rerun()
        else:
            st.session_state["_post_page"] = page + 1
            st.rerun()


def render():
    st.title("📋 사후 설문")
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

    if not get_config("post_active"):
        st.info("📌 사후 설문이 아직 시작되지 않았습니다. 선생님의 안내를 기다려 주세요.")
        return

    # 사용자가 바뀌면 이전 세션의 설문 진행 상태를 초기화
    if st.session_state.get("_post_survey_uid") != uid:
        st.session_state["_post_page"] = 0
        st.session_state.pop("_post_answers", None)
        st.session_state["_post_survey_uid"] = uid

    if has_submitted(SHEET_POST, uid):
        st.success("✅ 사후 설문을 완료하셨습니다. 참여해 주셔서 감사합니다!")
        return

    if "_post_page" not in st.session_state:
        st.session_state["_post_page"] = 0

    page = st.session_state["_post_page"]

    _progress_bar(page)
    st.markdown("---")

    if page == 0:
        _render_consent()
    elif 1 <= page <= TOTAL_PAGES:
        _render_category_page(page, uid)
    else:
        st.balloons()
        st.success("✅ 사후 설문이 완료되었습니다. 참여해 주셔서 감사합니다!")
        st.markdown(f"**{user['name']}** 학생의 소중한 응답이 저장되었습니다.")
