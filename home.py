# home.py  — 메인 라우터 & 레지스트리 (etc 토픽 단계 포함)
from dataclasses import dataclass
import importlib
import streamlit as st

# 공통 UI 유틸 (없어도 최소 동작하도록 폴백 제공)
try:
    from utils import page_header, keep_scroll
except Exception:
    def page_header(title: str, subtitle: str = "", icon: str = "", top_rule: bool = True):
        if top_rule:
            st.markdown("---")
        st.markdown(f"### {icon + ' ' if icon else ''}{title}")
        if subtitle:
            st.caption(subtitle)
    def keep_scroll(key: str = "default", mount: str = "sidebar"):
        # 최소 폴백: 아무 동작 안 함
        pass


# ----------------------------
# 데이터 모델
# ----------------------------
@dataclass
class Activity:
    """일반 교과(공통/미적/확통/기하) 및 etc-토픽 하위에서 공통으로 쓰는 액티비티 스펙"""
    slug: str         # URL 세그먼트 (교과/토픽 내부에서 유일)
    title: str        # 버튼에 보일 이름
    module: str       # importlib로 불러올 모듈 경로: e.g. 'activities.probability.binomial_simulator'


@dataclass
class TopicMeta:
    """etc(기타) 전용 토픽 메타"""
    slug: str
    title: str
    icon: str = "🧩"
    description: str = ""


# ----------------------------
# 교과 표시용(홈 카드 라벨/아이콘)
# 필요 시 여기에 교과를 더 추가하세요.
# ----------------------------
SUBJECT_UI = {
    "common":      {"title": "공통수학",   "icon": "📚"},
    "calculus":    {"title": "미적분학",   "icon": "∫"},
    "probability": {"title": "확률과통계", "icon": "🎲"},
    "geometry":    {"title": "기하학",     "icon": "📐"},
    "etc":         {"title": "기타",       "icon": "🧭"},  # ✅ 새 최상위 교과
}

# 홈에서 보일 교과 순서 (원하는 대로 바꾸세요)
SUBJECT_ORDER = ["common", "calculus", "probability", "geometry", "etc"]


# ----------------------------
# 레지스트리: 일반 교과(바로 액티비티 나열)
# - 여기엔 '기타'를 비워둡니다(etc는 토픽 단계가 있으니까)
# - 네가 이미 갖고 있는 액티비티들만 예시로 넣어둠. 더 추가/삭제해도 됨.
# ----------------------------
SUBJECTS = {
    "common":      [
        # Activity(slug="...", title="...", module="activities.common. ..."),
    ],
    "calculus":    [
        # Activity(slug="...", title="...", module="activities.calculus. ..."),
    ],
    "probability": [
        # ✅ 이미 만든 확률 액티비티들 (원하는 것만 남기세요)
        Activity(slug="binomial",   title="확률 시뮬레이터 (이항)", module="activities.probability.binomial_simulator"),
        Activity(slug="normal-samp",title="정규분포 표본추출",     module="activities.probability.normal_sampling"),
        Activity(slug="clt",        title="CLT: 표본평균의 분포",  module="activities.probability.clt_sample_mean"),
        Activity(slug="bino-norm",  title="이항→정규 근사",        module="activities.probability.binomial_normal_approx"),
        Activity(slug="pascal-mod", title="파스칼 삼각형 (mod m)", module="activities.probability.pascal_modulo_view"),
    ],
    "geometry":    [
        # Activity(slug="...", title="...", module="activities.geometry. ..."),
    ],
    "etc":         [],  # ✅ 기타는 여기서 액티비티를 직접 나열하지 않습니다 (토픽 단계가 따로 있음)
}


# ----------------------------
# 레지스트리: 기타(etc) — 토픽 메타 & 토픽별 액티비티
# - 여기에 토픽을 계속 추가하면 됩니다.
# ----------------------------
ETC_TOPICS_META = {
    # ✅ 예시 토픽: 프랙털
    "fractal": TopicMeta(
        slug="fractal",
        title="프랙털",
        icon="🌀",
        description="자기유사성과 반복 규칙으로 만들어지는 도형을 탐구합니다.",
    ),
    # "number-theory": TopicMeta(slug="number-theory", title="수론", icon="🔢", description="합동/소수/잔여계..."),
}

ETC_TOPICS = {
    # ✅ 프랙털 토픽의 액티비티 예시
    "fractal": [
        Activity(
            slug="sierpinski-chaos",
            title="시에르핀스키 삼각형 (Chaos Game)",
            module="activities.etc.fractal.sierpinski_chaos",
        ),
        # Activity(... 추가 가능 ...)
    ],
    # "number-theory": [Activity(...), ...],
}


# ----------------------------
# 라우팅 헬퍼
# ----------------------------
def set_route(name: str, **params):
    st.session_state["route"] = name
    for k, v in params.items():
        st.session_state[k] = v


def _do_rerun():
    st.experimental_rerun()


def _init_route():
    if "route" not in st.session_state:
        st.session_state["route"] = "home"


# ----------------------------
# 뷰: 홈
# ----------------------------
def home_view():
    page_header("수학 시뮬레이션 허브", "교과나 주제를 선택해서 들어가세요.", icon="🏠", top_rule=False)

    # 2~3열 그리드로 교과 카드 배치
    cols = st.columns(3)
    for i, key in enumerate(SUBJECT_ORDER):
        if key not in SUBJECT_UI:
            continue
        title = SUBJECT_UI[key]["title"]
        icon  = SUBJECT_UI[key]["icon"]
        with cols[i % len(cols)]:
            st.markdown(f"#### {icon} {title}")
            if st.button("열기", key=f"open-subject-{key}", use_container_width=True):
                set_route("subject", subject=key)
                _do_rerun()


# ----------------------------
# 뷰: 일반 교과 메인 (공통/미적/확통/기하)
# ----------------------------
def subject_view(subject_key: str):
    meta = SUBJECT_UI.get(subject_key, {"title": subject_key, "icon": "📁"})
    title, icon = meta["title"], meta["icon"]

    # 상단 내비
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("🏠 홈", use_container_width=True):
            set_route("home"); _do_rerun()

    page_header(f"{title}", "이 교과의 활동들을 선택하세요.", icon=icon, top_rule=True)

    acts = SUBJECTS.get(subject_key, [])
    if not acts:
        st.info("아직 등록된 액티비티가 없습니다.")
        return

    for act in acts:
        if st.button(f"▶ {act.title}", key=f"{subject_key}-{act.slug}", use_container_width=True):
            set_route("activity", subject=subject_key, slug=act.slug)
            _do_rerun()


# ----------------------------
# 뷰: 일반 교과 액티비티
# ----------------------------
def activity_view(subject_key: str, slug: str):
    acts = SUBJECTS.get(subject_key, [])
    act = next((a for a in acts if a.slug == slug), None)
    if not act:
        st.error("해당 활동을 찾을 수 없습니다."); return

    # 상단 내비 (여백 최소)
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("← 교과 메인", type="secondary", use_container_width=True):
            set_route("subject", subject=subject_key); _do_rerun()
    with c2:
        if st.button("🏠 홈", type="secondary", use_container_width=True):
            set_route("home"); _do_rerun()

    # 스크롤 유지 스크립트(사이드바 주입 → 본문 여백 X)
    keep_scroll(key=f"{subject_key}/{slug}", mount="sidebar")

    # 액티비티 모듈 렌더
    try:
        mod = importlib.import_module(act.module)
        mod.render()
    except Exception as e:
        st.exception(e)


# ----------------------------
# 뷰: 기타(etc) 메인 — 토픽 리스트
# ----------------------------
def etc_subject_view():
    page_header("기타", "주제(토픽) 페이지를 먼저 선택하세요.", icon="🧭", top_rule=True)

    metas = list(ETC_TOPICS_META.values())
    if not metas:
        st.info("아직 등록된 주제(토픽)가 없습니다."); return

    cols = st.columns(3)
    for i, meta in enumerate(metas):
        with cols[i % len(cols)]:
            st.markdown(f"### {meta.icon} {meta.title}")
            if meta.description:
                st.caption(meta.description)
            if st.button("열기", key=f"open-topic-{meta.slug}", use_container_width=True):
                set_route("topic", subject="etc", topic=meta.slug); _do_rerun()


# ----------------------------
# 뷰: 특정 토픽 메인 — 해당 토픽의 액티비티 리스트
# ----------------------------
def topic_view(topic_slug: str):
    meta = ETC_TOPICS_META.get(topic_slug)
    if not meta:
        st.error("해당 토픽을 찾을 수 없습니다."); return

    # 상단 내비
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("← 기타 메인", use_container_width=True):
            set_route("subject", subject="etc"); _do_rerun()
    with c2:
        if st.button("🏠 홈", use_container_width=True):
            set_route("home"); _do_rerun()

    page_header(f"{meta.title}", meta.description, icon=meta.icon, top_rule=True)

    acts = ETC_TOPICS.get(topic_slug, [])
    if not acts:
        st.info("아직 등록된 액티비티가 없습니다."); return

    for act in acts:
        if st.button(f"▶ {act.title}", key=f"act-{topic_slug}-{act.slug}", use_container_width=True):
            set_route("activity", subject="etc", topic=topic_slug, slug=act.slug)
            _do_rerun()


# ----------------------------
# 뷰: 토픽 하위 액티비티 (etc 전용)
# ----------------------------
def activity_view_topic(topic_slug: str, slug: str):
    acts = ETC_TOPICS.get(topic_slug, [])
    act = next((a for a in acts if a.slug == slug), None)
    if not act:
        st.error("해당 활동을 찾을 수 없습니다."); return

    # 상단 내비
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("← 토픽 메인", type="secondary", use_container_width=True):
            set_route("topic", subject="etc", topic=topic_slug); _do_rerun()
    with c2:
        if st.button("← 기타 메인", type="secondary", use_container_width=True):
            set_route("subject", subject="etc"); _do_rerun()
    with c3:
        if st.button("🏠 홈", type="secondary", use_container_width=True):
            set_route("home"); _do_rerun()

    # 스크롤 유지(사이드바 주입)
    keep_scroll(key=f"etc/{topic_slug}/{slug}", mount="sidebar")

    # 액티비티 모듈 렌더
    try:
        mod = importlib.import_module(act.module)
        mod.render()
    except Exception as e:
        st.exception(e)


# ----------------------------
# 엔트리 포인트
# ----------------------------
def main():
    _init_route()

    # 라우터
    route = st.session_state.get("route", "home")

    if route == "home":
        home_view()

    elif route == "subject":
        subject_key = st.session_state.get("subject")
        if subject_key == "etc":
            etc_subject_view()          # ✅ 기타는 토픽 리스트로 진입
        else:
            subject_view(subject_key)   # 공통/미적/확통/기하

    elif route == "topic":
        topic_slug = st.session_state.get("topic")
        topic_view(topic_slug)          # ✅ etc 전용

    elif route == "activity":
        if st.session_state.get("subject") == "etc" and st.session_state.get("topic"):
            activity_view_topic(st.session_state["topic"], st.session_state.get("slug"))  # ✅ etc 전용 액티비티
        else:
            activity_view(st.session_state.get("subject"), st.session_state.get("slug"))  # 일반 교과 액티비티

    else:
        # 알 수 없는 라우트면 홈으로
        set_route("home")
        home_view()


# 스트림릿 실행 시 진입
main()
