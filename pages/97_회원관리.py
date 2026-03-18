# pages/97_회원관리.py
"""
회원 관리 페이지

접근 권한:
  - 관리자(admin)  : 모든 탭 사용 가능
  - 휘문고 수학과 교사 : '가입 승인'·'학생 관리' 탭만 사용 가능 (담당 학급만 표시)

탭 구성 (관리자):
  1. 가입 승인   – 대기 중인 신청 승인/거부
  2. 학생 관리   – 학생 목록, 상태 변경, 비밀번호 재설정
  3. 일반인 관리 – 일반인 목록, 그룹 배정, 비밀번호 재설정 / 교사 설정
  4. 과목 권한   – 학년별·그룹별 허용 과목 설정
  5. 그룹 관리   – 그룹 생성/삭제
  6. 대량 등록   – CSV로 학생 계정 일괄 생성
  7. 계정 잠금   – 잠금 계정 해제
"""
import sys
from pathlib import Path
import ast
import re

_root = str(Path(__file__).parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import streamlit as st
import pandas as pd
from io import StringIO
import auth_utils as _auth_utils

st.set_page_config(page_title="회원 관리", layout="wide")

from theme_utils import inject_dark_theme, inject_hide_nav
inject_dark_theme()
inject_hide_nav()

st.sidebar.page_link("home.py", label="🏠 홈으로 돌아가기",
                     use_container_width=True)

if st.session_state.get("_dev_mode", False):
    st.sidebar.divider()
    st.sidebar.caption("🔧 관리자 기능")
    if st.sidebar.button("📋 진도표 관리", use_container_width=True, key="_97_nav_schedule"):
        st.switch_page("pages/98_진도표.py")
    if st.sidebar.button("📥 피드백 게시판", use_container_width=True, key="_97_nav_feedback"):
        st.session_state["_nav_to"] = "feedback_board"
        st.switch_page("home.py")
    if st.sidebar.button("📊 방문자 통계", use_container_width=True, key="_97_nav_stats"):
        st.session_state["_nav_to"] = "visit_stats"
        st.switch_page("home.py")

# ── 접근 제어 ─────────────────────────────────────────────────────────────────
if not st.session_state.get("_authenticated", False):
    st.error("🔒 로그인이 필요합니다.")
    st.info("홈 화면에서 관리자 계정으로 로그인하세요.")
    st.stop()

_is_admin        = st.session_state.get("_dev_mode", False)
_current_user_id = st.session_state.get("_user_id", "")
_current_user_type = st.session_state.get("_user_type", "")

# 교사 여부 확인 (일반인 중 "휘문고 수학과" 그룹)
_is_teacher      = False
_teacher_settings: dict | None = None
_teacher_classes: list[str]    = []

if not _is_admin and _current_user_type == "general":
    from auth_utils import (
        is_math_teacher, get_teacher_settings, get_teacher_managed_classes,
    )
    _is_teacher = is_math_teacher(_current_user_id)
    if _is_teacher:
        _teacher_settings = get_teacher_settings(_current_user_id)
        _teacher_classes  = get_teacher_managed_classes(_current_user_id)

if not _is_admin and not _is_teacher:
    st.error("🔒 이 페이지는 **관리자** 또는 **담당 교사**만 접근할 수 있습니다.")
    st.stop()

# ── 임포트 ───────────────────────────────────────────────────────────────────
from auth_utils import (
    ALL_SUBJECTS,
    MATH_TEACHER_GROUP,
    WS_STUDENTS, WS_GENERAL, WS_LOCKOUT,
    STATUS_PENDING, STATUS_APPROVED, STATUS_REJECTED,
    _cached_students, _cached_general,
    _cached_grade_perms, _cached_group_perms, _cached_group_lesson_perms, _cached_lockout,
    _cached_roster, _cached_teacher_settings,
    get_roster_student_counts, verify_roster_student,
    get_roster_debug_info,
    _get_users_spreadsheet_id,
    update_user_status, reset_user_password,
    update_user_group, save_grade_permissions,
    save_group_permissions, save_group_lesson_permissions, delete_group,
    get_all_groups, batch_register_students,
    check_password_policy,
    is_account_locked, reset_lockout,
    get_teacher_settings, save_teacher_settings,
    is_math_teacher, get_teacher_managed_classes,
    verify_teacher_roster_student, _cached_teacher_roster,
    TEACHER_ROSTER_WS,
)


def _clear_auth_caches_safe(**kwargs):
    clear_fn = getattr(_auth_utils, "_clear_auth_caches", None)
    if callable(clear_fn):
        clear_fn(**kwargs)
    else:
        st.cache_data.clear()


def _gifted_lesson_labels() -> dict[str, str]:
    """영재 lessons/_units.py에서 단원 key→표시 라벨을 읽어옵니다."""
    units_py = Path(_root) / "activities" / "gifted" / "lessons" / "_units.py"
    if not units_py.exists():
        return {}
    try:
        labels: dict[str, str] = {}
        source = units_py.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(units_py))

        curriculum = None
        units = None
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id == "CURRICULUM":
                    curriculum = ast.literal_eval(node.value)
                elif target.id == "UNITS":
                    units = ast.literal_eval(node.value)

        if isinstance(curriculum, list) and curriculum:
            def walk(nodes: list, prefix: list[str]):
                for node in nodes:
                    if not isinstance(node, dict):
                        continue
                    key = str(node.get("key", "")).strip()
                    label = str(node.get("label", "")).strip()
                    if not key:
                        continue
                    path = prefix + ([label] if label else [key])
                    labels[key] = " > ".join(path)
                    children = node.get("children", [])
                    if isinstance(children, list) and children:
                        walk(children, path)

            walk(curriculum, [])
            if labels:
                return labels

        if isinstance(units, dict):
            for k, v in units.items():
                key = str(k).strip()
                if not key:
                    continue
                if isinstance(v, dict):
                    labels[key] = str(v.get("label", key))
                else:
                    labels[key] = key
        return labels
    except Exception:
        return {}


def _is_gifted_group_name(group_name: str) -> bool:
    name = str(group_name)
    name = name.replace("\u200b", "").replace("\ufeff", "").strip()
    name = name.replace("（", "(").replace("）", ")")
    return bool(re.fullmatch(r"영재\s*\(\s*\d{6}\s*\)", name))


def _normalize_group_name(group_name: str) -> str:
    name = str(group_name or "")
    name = name.replace("\u200b", "").replace("\ufeff", "").strip()
    name = name.replace("（", "(").replace("）", ")")
    return name


def _get_student_class_from_roster(student_num: str, roster_all: list[dict]) -> str:
    """학번으로 학생의 반을 로스터에서 조회합니다."""
    for r in roster_all:
        if str(r.get("학번", "")).strip() == student_num:
            return str(r.get("반", "") or r.get("학급", "")).strip()
    return ""


def _class_from_num(num: str) -> str:
    """학번 앞자리에서 학급명을 추출합니다.

    형식: 첫째 자리 = 학년, 둘째~셋째 자리 = 반 (예: '207XXXX' → '2학년 7반')
    """
    num = num.strip()
    if len(num) < 3:
        return ""
    grade = num[0]
    cls   = str(int(num[1:3]))  # 앞의 0 제거: '07' → '7'
    return f"{grade}학년 {cls}반"


# ─────────────────────────────────────────────────────────────────────────────
if _is_admin:
    st.title("👥 회원 관리")
    st.caption("회원 가입 승인, 과목 권한 설정 등 사용자 관리 기능입니다.")
else:
    teacher_name = st.session_state.get("_user_name", "선생님")
    st.title(f"👥 회원 관리 — {teacher_name}")
    st.caption(
        f"담당 학급: {', '.join(_teacher_classes) if _teacher_classes else '(설정 없음)'}"
    )
st.divider()

# 새로고침
if st.button("🔄 데이터 새로고침", key="mgmt_refresh"):
    _clear_auth_caches_safe(
        clear_users=True,
        clear_grade_perms=True,
        clear_group_perms=True,
        clear_group_lesson_perms=True,
        clear_lockout=True,
        clear_roster=True,
        clear_teacher_settings=True,
    )
    st.rerun()

sheet_id = _get_users_spreadsheet_id()

# ── 교사 명단 사전 로드 (교사 모드일 때만) ────────────────────────────────────
# 교사의 "수강생명단" 탭을 먼저 불러 가입 승인·학생 관리 필터에 사용합니다.
_teacher_roster_id: str = ""
_teacher_roster_all: list[dict] = []
_teacher_roster_has_class: bool = False  # '반' 컬럼 존재 여부

if _is_teacher and _teacher_settings:
    _teacher_roster_id = _teacher_settings.get("명단시트ID", "")
    if _teacher_roster_id:
        _teacher_roster_all = _cached_teacher_roster(_teacher_roster_id)
        _teacher_roster_has_class = any(
            str(r.get("반", "")).strip() for r in _teacher_roster_all
        )


_teacher_nums: set[str] = {
    str(r.get("학번", "")).strip()
    for r in _teacher_roster_all
    if str(r.get("학번", "")).strip()
}


def _teacher_filter(student_num: str) -> bool:
    """교사 모드에서 이 학번이 담당 학생인지 확인합니다.

    우선순위:
    1. 교사 명단(수강생명단)의 '반' 컬럼이 있으면 → 반 이름으로 매칭
    2. 명단에 학번이 있으면 → 담당 학생으로 간주
    3. 명단이 없으면 → 학번 형식(첫째자리=학년, 둘째~셋째자리=반)으로 파생
    """
    num = student_num.strip()
    if not num:
        return False
    if _teacher_roster_all:
        if _teacher_roster_has_class:
            cls = next(
                (str(r.get("반", "")).strip()
                 for r in _teacher_roster_all if str(r.get("학번", "")).strip() == num),
                "",
            )
            return cls in _teacher_classes
        else:
            return num in _teacher_nums
    # 폴백: 학번 앞자리에서 학급 파생
    return _class_from_num(num) in _teacher_classes


# ── 탭 구성 ───────────────────────────────────────────────────────────────────
if _is_admin:
    (tab_approve, tab_students, tab_general,
     tab_perms, tab_groups, tab_bulk, tab_lockout) = st.tabs([
        "✅ 가입 승인",
        "🎓 학생 관리",
        "👤 일반인 관리",
        "🔑 과목 권한",
        "📂 그룹 관리",
        "📥 대량 등록",
        "🔒 계정 잠금",
    ])
else:
    tab_approve, tab_students = st.tabs([
        "✅ 가입 승인",
        "🎓 학생 관리",
    ])


# ─── 1. 가입 승인 ─────────────────────────────────────────────────────────────
with tab_approve:
    st.subheader("가입 승인 대기 목록")

    students_all = _cached_students(sheet_id)
    general_all  = _cached_general(sheet_id)
    roster_all   = _cached_roster(sheet_id)

    # 교사 모드: 담당 학급에 속한 학생만 필터링
    if _is_teacher:
        pending_s = [r for r in students_all
                     if str(r.get("승인상태", "")).strip() == STATUS_PENDING
                     and _teacher_filter(str(r.get("학번", "")).strip())]
        pending_g = []  # 교사는 일반인 승인 없음
    else:
        pending_s = [r for r in students_all
                     if str(r.get("승인상태", "")).strip() == STATUS_PENDING]
        pending_g = [r for r in general_all
                     if str(r.get("승인상태", "")).strip() == STATUS_PENDING]

    total_pending = len(pending_s) + len(pending_g)
    if total_pending == 0:
        st.success("✅ 승인 대기 중인 가입 신청이 없습니다.")
    else:
        if _is_teacher:
            st.info(f"총 **{total_pending}건** 대기 중 (담당 학급 학생 {len(pending_s)}명)")
        else:
            st.info(f"총 **{total_pending}건** 대기 중 (학생 {len(pending_s)}명 / 일반인 {len(pending_g)}명)")

    # _teacher_roster_id 는 탭 외부에서 이미 설정됨

    # 학생 대기
    if pending_s:
        st.markdown("#### 📚 학생")
        for row in pending_s:
            uid   = str(row.get("아이디", ""))
            name  = str(row.get("이름", ""))
            num   = str(row.get("학번", ""))
            grade = str(row.get("학년", ""))
            joined = str(row.get("가입일", ""))

            # 명단 검증 — 교사는 자신의 명단 우선, 없으면 전체 명단으로 폴백
            if _is_teacher and _teacher_roster_id:
                in_roster = verify_teacher_roster_student(_teacher_roster_id, num, name)
            else:
                in_roster = verify_roster_student(sheet_id, num, name)
            roster_badge = (
                "✅ 명단 확인됨"  if in_roster
                else "⚠️ 명단에 없음 (학번·이름 불일치 또는 미등록)"
            )
            roster_color = "green" if in_roster else "red"

            # 담당 학급 표시 (교사 명단 우선, 없으면 관리자 명단)
            _ref_r = _teacher_roster_all if (_is_teacher and _teacher_roster_all) else roster_all
            cls_name = _get_student_class_from_roster(num, _ref_r)

            with st.container(border=True):
                st.markdown(
                    f"**{name}** (`{uid}`)  |  학번: `{num}`  |  "
                    f"학년: {grade}  |  학급: {cls_name or '미확인'}  |  가입일: {joined}"
                )
                st.markdown(
                    f'<span style="color:{roster_color};font-size:0.88em">'
                    f'{roster_badge}</span>',
                    unsafe_allow_html=True,
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ 승인", key=f"apv_s_{uid}",
                                 use_container_width=True, type="primary"):
                        if update_user_status("student", uid, STATUS_APPROVED):
                            st.success(f"{name} 승인 완료")
                            st.rerun()
                with c2:
                    if st.button("❌ 거부", key=f"rej_s_{uid}",
                                 use_container_width=True):
                        if update_user_status("student", uid, STATUS_REJECTED):
                            st.warning(f"{name} 거부됨")
                            st.rerun()

    # 일반인 대기 (관리자만)
    if pending_g:
        st.markdown("#### 👤 일반인")
        for row in pending_g:
            uid     = str(row.get("아이디", ""))
            name    = str(row.get("이름", ""))
            purpose = str(row.get("사용목적", ""))
            joined  = str(row.get("가입일", ""))
            with st.container(border=True):
                st.markdown(
                    f"**{name}** (`{uid}`)  |  가입일: {joined}"
                )
                st.caption(f"사용 목적: {purpose}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ 승인", key=f"apv_g_{uid}",
                                 use_container_width=True, type="primary"):
                        if update_user_status("general", uid, STATUS_APPROVED):
                            st.success(f"{name} 승인 완료")
                            st.rerun()
                with c2:
                    if st.button("❌ 거부", key=f"rej_g_{uid}",
                                 use_container_width=True):
                        if update_user_status("general", uid, STATUS_REJECTED):
                            st.warning(f"{name} 거부됨")
                            st.rerun()


# ─── 2. 학생 관리 ─────────────────────────────────────────────────────────────
with tab_students:
    students_all = _cached_students(sheet_id)
    roster_all   = _cached_roster(sheet_id)

    # 교사 모드: 담당 학급 학생만 필터
    if _is_teacher:
        st.subheader(f"학생 목록 (담당 학급: {', '.join(_teacher_classes) or '없음'})")
        students_view = [
            r for r in students_all
            if _teacher_filter(str(r.get("학번", "")).strip())
        ]
    else:
        st.subheader("학생 목록")
        students_view = students_all

    if not students_view:
        st.info("해당 조건에 맞는 학생이 없습니다.")
    else:
        df_s = pd.DataFrame(students_view)
        display_cols = [c for c in df_s.columns if c != "해시비밀번호"]
        st.dataframe(df_s[display_cols], use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("#### 상태 변경 / 비밀번호 재설정")

        def _s_label(r):
            return f"{r.get('이름', '')}({r.get('아이디', '')})"
        student_options = {_s_label(r): str(r.get("아이디", "")) for r in students_view}
        sel_label_s = st.selectbox("학생 선택", list(student_options.keys()),
                                   key="mgmt_sel_student")
        sel_uid = student_options[sel_label_s]
        sel_row = next((r for r in students_view
                        if str(r.get("아이디", "")) == sel_uid), {})
        st.caption(
            f"이름: {sel_row.get('이름', '')}  |  "
            f"학번: {sel_row.get('학번', '')}  |  "
            f"학년: {sel_row.get('학년', '')}  |  "
            f"현재 상태: {sel_row.get('승인상태', '')}"
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✅ 승인으로 변경", key="mgmt_s_approve",
                         use_container_width=True):
                if update_user_status("student", sel_uid, STATUS_APPROVED):
                    st.success("승인 완료")
                    st.rerun()
        with c2:
            if st.button("⏸ 대기로 변경", key="mgmt_s_pending",
                         use_container_width=True):
                if update_user_status("student", sel_uid, STATUS_PENDING):
                    st.info("대기 상태로 변경됨")
                    st.rerun()
        with c3:
            if st.button("❌ 거부로 변경", key="mgmt_s_reject",
                         use_container_width=True):
                if update_user_status("student", sel_uid, STATUS_REJECTED):
                    st.warning("거부 상태로 변경됨")
                    st.rerun()

        st.divider()
        with st.expander("🔑 비밀번호 재설정"):
            new_pw = st.text_input("새 비밀번호", type="password",
                                   key="mgmt_s_new_pw",
                                   help="8자 이상, 숫자 포함")
            if st.button("비밀번호 변경", key="mgmt_s_pw_btn"):
                errs = check_password_policy(new_pw)
                if errs:
                    for e in errs:
                        st.error(e)
                elif reset_user_password("student", sel_uid, new_pw):
                    st.success(f"{sel_uid} 비밀번호 재설정 완료")
                else:
                    st.error("비밀번호 재설정에 실패했습니다.")

    # ── 학급별 가입 현황 ──────────────────────────────────────────────────────
    st.divider()
    st.subheader("📊 학급별 가입 현황")

    # 교사 모드: 교사 전용 명단(수강생명단)을 우선 사용
    _ref_roster = _teacher_roster_all if (_is_teacher and _teacher_roster_all) else roster_all
    if _is_teacher and _teacher_roster_all:
        st.caption("교사 명단(수강생명단)을 기준으로 가입 상태를 확인합니다.")
    elif _is_teacher:
        st.caption("학번 형식(첫째자리=학년, 둘째~셋째자리=반)으로 학급을 구분합니다.")
    else:
        st.caption("구글 시트 '수강생명단'을 기준으로 가입 상태를 확인합니다.")

    # 교사 모드는 명단 없어도 학번 파생 방식으로 진행 가능
    _show_roster_section = bool(_ref_roster) or _is_teacher
    if not _show_roster_section:
        debug = get_roster_debug_info(sheet_id)
        if debug["ok"]:
            st.info("ℹ️ '수강생명단' 시트에 데이터가 없습니다.")
        else:
            st.error(f"❌ 명단 로드 실패: {debug['error']}")
    else:
        if _is_teacher and _teacher_roster_id and not _teacher_roster_all:
            st.warning("⚠️ 교사 명단(수강생명단)을 불러오지 못했습니다. 학번 기반으로 표시합니다.")
        registered_nums = {
            str(r.get("학번", "")).strip()
            for r in students_all
            if str(r.get("승인상태", "")).strip() in (STATUS_APPROVED, STATUS_PENDING)
        }

        # 반 목록 추출
        # 교사 모드 + 반 컬럼 없음 → 학번 앞자리에서 학급 파생
        if _is_teacher and _teacher_roster_all and not _teacher_roster_has_class:
            # 학번에서 학급 파생하여 담당 학급만 그룹핑
            all_classes_in_roster = sorted(_teacher_classes)

        elif _is_teacher and not _teacher_roster_all:
            # 명단 없음 → 등록된 학생 학번에서 담당 학급 파생
            all_classes_in_roster = sorted(_teacher_classes)

        else:
            # 반 컬럼이 있으면 그 값으로, 없으면 학번에서 파생
            _roster_has_class = any(
                str(r.get("반", "") or r.get("학급", "")).strip()
                for r in _ref_roster
            )
            all_classes_in_roster = []
            seen = set()
            for r in _ref_roster:
                if _roster_has_class:
                    cls = str(r.get("반", "") or r.get("학급", "")).strip()
                else:
                    cls = _class_from_num(str(r.get("학번", "")).strip())
                if cls and cls not in seen:
                    if _is_teacher and cls not in _teacher_classes:
                        continue
                    all_classes_in_roster.append(cls)
                    seen.add(cls)
            all_classes_in_roster = sorted(all_classes_in_roster)

        if not all_classes_in_roster:
            st.info("표시할 학급이 없습니다.")
        else:
            sel_cls = st.selectbox(
                "학급 선택",
                all_classes_in_roster,
                key="roster_cls_sel",
            )

            # 해당 학급 학생 목록 구성
            if _is_teacher and _teacher_roster_all and not _teacher_roster_has_class:
                # 교사 명단 있지만 반 컬럼 없음 → 학번에서 파생
                cls_students = [
                    r for r in _teacher_roster_all
                    if _class_from_num(str(r.get("학번", "")).strip()) == sel_cls
                ]
            elif _is_teacher and not _teacher_roster_all:
                # 교사 명단 없음 → 등록된 학생 중 학번 기반 필터
                cls_students = [
                    {"학번": str(r.get("학번", "")).strip(),
                     "이름": str(r.get("이름", "")).strip()}
                    for r in students_all
                    if _class_from_num(str(r.get("학번", "")).strip()) == sel_cls
                ]
            elif _roster_has_class:
                # 반 컬럼 있음 → 컬럼 값으로 필터
                cls_students = [
                    r for r in _ref_roster
                    if str(r.get("반", "") or r.get("학급", "")).strip() == sel_cls
                ]
            else:
                # 반 컬럼 없음(관리자 포함) → 학번에서 파생하여 필터
                cls_students = [
                    r for r in _ref_roster
                    if _class_from_num(str(r.get("학번", "")).strip()) == sel_cls
                ]
            total_cnt  = len(cls_students)
            joined_cnt = sum(1 for r in cls_students
                             if str(r.get("학번", "")).strip() in registered_nums)
            not_joined = [r for r in cls_students
                          if str(r.get("학번", "")).strip() not in registered_nums]

            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("전체 수강생", f"{total_cnt}명")
            col_m2.metric("가입 완료", f"{joined_cnt}명")
            col_m3.metric("미가입", f"{total_cnt - joined_cnt}명")

            with st.expander("📋 전체 명단 보기", expanded=False):
                roster_display = []
                for r in cls_students:
                    num  = str(r.get("학번", "")).strip()
                    nm   = str(r.get("이름", "")).strip()
                    is_joined = num in registered_nums
                    matched = next(
                        (s for s in students_all
                         if str(s.get("학번", "")).strip() == num),
                        None
                    )
                    status_str = matched.get("승인상태", "") if matched else ""
                    if not is_joined:
                        disp_status = "미가입"
                    elif status_str == STATUS_APPROVED:
                        disp_status = "승인"
                    elif status_str == STATUS_PENDING:
                        disp_status = "대기"
                    elif status_str == STATUS_REJECTED:
                        disp_status = "거부"
                    else:
                        disp_status = status_str
                    roster_display.append({"학번": num, "이름": nm, "가입상태": disp_status})

                df_roster = pd.DataFrame(roster_display, columns=["학번", "이름", "가입상태"])

                def _color_status(val):
                    if val == "승인":
                        return "background-color:#166534;color:#bbf7d0"
                    if val == "대기":
                        return "background-color:#854d0e;color:#fef9c3"
                    if val == "거부":
                        return "background-color:#7f1d1d;color:#fecaca"
                    return "background-color:#334155;color:#94a3b8"

                if df_roster.empty:
                    st.info("명단 데이터가 없습니다.")
                else:
                    try:
                        styled = df_roster.style.map(_color_status, subset=["가입상태"])
                    except AttributeError:
                        styled = df_roster.style.applymap(_color_status, subset=["가입상태"])
                    st.dataframe(styled, use_container_width=True, hide_index=True)

            if not_joined:
                with st.expander(f"⚠️ 미가입 학생 ({len(not_joined)}명)", expanded=True):
                    cols_nj = st.columns(4)
                    for i, r in enumerate(not_joined):
                        with cols_nj[i % 4]:
                            num = str(r.get("학번", "")).strip()
                            nm  = str(r.get("이름", "")).strip()
                            st.markdown(
                                f'<div style="background:#1e293b;border:1px solid #334155;border-radius:8px;'
                                f'padding:10px 12px;margin-bottom:8px;text-align:center">'
                                f'<span style="font-size:1.05em;font-weight:700;color:#e2e8f0">{nm}</span>'
                                f'<br><span style="font-size:0.95em;color:#94a3b8;letter-spacing:0.03em">{num}</span>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
            else:
                st.success(f"🎉 {sel_cls} 학생 전원이 가입되어 있습니다!")


# ─── 이하 탭은 관리자 전용 ────────────────────────────────────────────────────
if not _is_admin:
    st.stop()


# ─── 3. 일반인 관리 ──────────────────────────────────────────────────────────
with tab_general:
    subtab_general, subtab_teacher = st.tabs(["👤 일반인 관리", "🏫 교사 설정"])

    # ── 3-1. 일반인 관리 (기존) ───────────────────────────────────────────────
    with subtab_general:
        st.subheader("일반인 목록")
        general_all = _cached_general(sheet_id)
        if not general_all:
            st.info("등록된 일반인이 없습니다.")
        else:
            df_g = pd.DataFrame(general_all)
            display_cols_g = [c for c in df_g.columns if c != "해시비밀번호"]
            st.dataframe(df_g[display_cols_g], use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("#### 그룹 배정 / 상태 변경 / 비밀번호 재설정")

            def _g_label(r):
                return f"{r.get('이름', '')}({r.get('아이디', '')})"
            general_options = {_g_label(r): str(r.get("아이디", "")) for r in general_all}
            sel_glabel = st.selectbox("일반인 선택", list(general_options.keys()),
                                      key="mgmt_sel_general")
            sel_gid = general_options[sel_glabel]
            sel_grow = next((r for r in general_all
                             if str(r.get("아이디", "")) == sel_gid), {})
            st.caption(
                f"이름: {sel_grow.get('이름', '')}  |  "
                f"목적: {sel_grow.get('사용목적', '')}  |  "
                f"현재 그룹: {sel_grow.get('그룹', '(없음)')}  |  "
                f"현재 상태: {sel_grow.get('승인상태', '')}"
            )

            all_groups = get_all_groups()
            group_opts = ["(없음)"] + all_groups
            cur_group  = str(sel_grow.get("그룹", "")).strip() or "(없음)"
            default_gi = group_opts.index(cur_group) if cur_group in group_opts else 0

            col_grp, col_st1, col_st2, col_st3 = st.columns([2, 1, 1, 1])
            with col_grp:
                new_group = st.selectbox("그룹 선택", group_opts,
                                         index=default_gi, key="mgmt_g_group_sel")
            with col_st1:
                if st.button("그룹 저장", key="mgmt_g_grp_save",
                             use_container_width=True, type="primary"):
                    grp = "" if new_group == "(없음)" else new_group
                    if update_user_group(sel_gid, grp):
                        st.success("그룹 저장 완료")
                        st.rerun()
            with col_st2:
                if st.button("✅ 승인", key="mgmt_g_approve",
                             use_container_width=True):
                    if update_user_status("general", sel_gid, STATUS_APPROVED):
                        st.success("승인 완료"); st.rerun()
            with col_st3:
                if st.button("❌ 거부", key="mgmt_g_reject",
                             use_container_width=True):
                    if update_user_status("general", sel_gid, STATUS_REJECTED):
                        st.warning("거부됨"); st.rerun()

            with st.expander("🔑 비밀번호 재설정"):
                new_pw_g = st.text_input("새 비밀번호", type="password",
                                         key="mgmt_g_new_pw",
                                         help="8자 이상, 숫자 포함")
                if st.button("비밀번호 변경", key="mgmt_g_pw_btn"):
                    errs = check_password_policy(new_pw_g)
                    if errs:
                        for e in errs:
                            st.error(e)
                    elif reset_user_password("general", sel_gid, new_pw_g):
                        st.success(f"{sel_gid} 비밀번호 재설정 완료")
                    else:
                        st.error("비밀번호 재설정에 실패했습니다.")

    # ── 3-2. 교사 설정 (신규) ─────────────────────────────────────────────────
    with subtab_teacher:
        st.subheader("🏫 교사 설정")
        st.caption(
            f"그룹이 **'{MATH_TEACHER_GROUP}'**인 사용자에 대해 담당 과목·학년·반을 설정합니다. "
            "설정된 교사는 이 페이지에서 담당 학생의 가입 승인과 학생 관리를 할 수 있습니다."
        )

        general_all_t = _cached_general(sheet_id)
        math_teachers = [
            r for r in general_all_t
            if _normalize_group_name(r.get("그룹", "")) == MATH_TEACHER_GROUP
        ]

        if not math_teachers:
            st.info(
                f"'{MATH_TEACHER_GROUP}' 그룹에 속한 사용자가 없습니다. "
                "'일반인 관리' 탭에서 그룹을 먼저 설정하세요."
            )
        else:
            def _t_label(r):
                return f"{r.get('이름', '')} ({r.get('아이디', '')})"

            t_options   = {_t_label(r): str(r.get("아이디", "")) for r in math_teachers}
            sel_t_label = st.selectbox("교사 선택", list(t_options.keys()),
                                       key="teacher_cfg_sel")
            sel_t_id    = t_options[sel_t_label]

            # 현재 설정 로드
            cur_t         = get_teacher_settings(sel_t_id) or {}
            cur_email     = cur_t.get("이메일",    "")
            cur_roster_id = cur_t.get("명단시트ID", "")
            cur_subj_cfg  = cur_t.get("과목설정",  {})  # {subj_key: {grades, classes, sheet_id}}

            # 서비스 계정 이메일 (참고용 — 한 번만 표시)
            _svc_email = ""
            try:
                _svc_email = st.secrets["gcp_service_account"].get("client_email", "")
            except Exception:
                pass

            # ── ① 이메일 ──────────────────────────────────────────────────────
            teacher_email = st.text_input(
                "📧 이메일 주소 (가입 알림 수신)",
                value=cur_email,
                placeholder="teacher@example.com",
                key=f"t_email_{sel_t_id}",
            )

            # ── ② 학생 명단 스프레드시트 ──────────────────────────────────────
            with st.expander(
                "👥 학생 명단 스프레드시트 설정",
                expanded=not cur_roster_id,
            ):
                st.caption(
                    f"선생님 담당 학생 명단이 담긴 구글 스프레드시트 ID를 입력하세요.  \n"
                    f"해당 시트 안에 **`{TEACHER_ROSTER_WS}`** 탭을 만들고 "
                    f"첫 행에 `학번`, `이름` 헤더를 넣어주세요.  \n"
                    "학생이 가입 신청을 하면 이 명단과 대조하여 재학 여부를 표시합니다."
                )
                if _svc_email:
                    st.info(f"서비스 계정 이메일: `{_svc_email}`  \n편집자로 공유해 주세요.")
                teacher_roster_id = st.text_input(
                    "명단 스프레드시트 ID",
                    value=cur_roster_id,
                    placeholder="예: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
                    key=f"t_roster_{sel_t_id}",
                    help="Google Sheets URL에서 /d/ 와 /edit 사이의 긴 문자열",
                )
                # 명단 연결 테스트
                if teacher_roster_id and st.button(
                    "🔍 명단 연결 테스트", key=f"t_roster_test_{sel_t_id}"
                ):
                    with st.spinner("연결 확인 중..."):
                        rows = _cached_teacher_roster(teacher_roster_id)
                    if rows:
                        st.success(f"✅ 명단 {len(rows)}명 확인됨")
                    else:
                        st.error(
                            f"❌ 명단을 읽지 못했습니다. "
                            f"스프레드시트 ID와 `{TEACHER_ROSTER_WS}` 탭, "
                            "서비스 계정 공유 여부를 확인하세요."
                        )

            st.divider()

            # ── ② 담당 과목 선택 (multiselect) ───────────────────────────────
            st.markdown("##### 담당 과목 선택")
            valid_cur_subj = [s for s in cur_subj_cfg if s in ALL_SUBJECTS]
            sel_subjects = st.multiselect(
                "담당 과목 (복수 선택 가능)",
                list(ALL_SUBJECTS.keys()),
                default=valid_cur_subj,
                format_func=lambda k: ALL_SUBJECTS.get(k, k),
                key=f"t_subj_{sel_t_id}",
            )

            # ── ③ 과목별 설정 탭 (학년 · 반 · 성찰 스프레드시트) ─────────────
            new_subj_settings: dict = {}
            if sel_subjects:
                st.markdown("##### 과목별 설정")
                st.caption(
                    "각 과목 탭에서 담당 학년·반과 성찰 기록용 스프레드시트를 설정하세요. "
                    "한 선생님이 여러 학년을 담당하는 경우 해당 학년을 모두 체크하면 됩니다."
                )
                if _svc_email:
                    st.info(
                        f"📌 서비스 계정 이메일: `{_svc_email}`  \n"
                        "스프레드시트를 이 이메일로 **편집자** 공유해야 기록이 저장됩니다."
                    )

                all_class_nums  = [str(i) for i in range(1, 13)]
                subj_tab_labels = [ALL_SUBJECTS.get(s, s) for s in sel_subjects]
                subj_tabs       = st.tabs(subj_tab_labels)

                for tab, subj_key in zip(subj_tabs, sel_subjects):
                    with tab:
                        cfg        = cur_subj_cfg.get(subj_key, {})
                        cur_grades = cfg.get("grades",   [])
                        cur_cls    = cfg.get("classes",  [])
                        cur_sid    = cfg.get("sheet_id", "")

                        # 학년 선택
                        st.markdown("**담당 학년**")
                        grade_cols = st.columns(3)
                        sel_g = []
                        for gi, g in enumerate(["1", "2", "3"]):
                            with grade_cols[gi]:
                                if st.checkbox(
                                    f"{g}학년",
                                    value=(g in cur_grades),
                                    key=f"t_{sel_t_id}_{subj_key}_g{g}",
                                ):
                                    sel_g.append(g)

                        # 반 선택
                        st.markdown("**담당 반 (1~12반)**")
                        valid_cur_cls = [c for c in cur_cls if c in all_class_nums]
                        sel_c = st.multiselect(
                            "반 선택",
                            all_class_nums,
                            default=valid_cur_cls,
                            format_func=lambda x: f"{x}반",
                            key=f"t_{sel_t_id}_{subj_key}_cls",
                        )

                        # 담당 학급 미리보기
                        if sel_g and sel_c:
                            preview = [f"{g}학년 {c}반" for g in sel_g for c in sel_c]
                            st.caption(f"담당 학급: {', '.join(preview)}")
                        elif sel_g or sel_c:
                            st.warning("학년과 반을 모두 선택해야 담당 학급이 완성됩니다.")

                        # 성찰 스프레드시트 ID (과목별)
                        st.markdown("**성찰 기록 스프레드시트**")
                        sel_sid = st.text_input(
                            "스프레드시트 ID",
                            value=cur_sid,
                            placeholder="예: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
                            key=f"t_{sel_t_id}_{subj_key}_sid",
                            help="Google Sheets URL에서 /d/ 와 /edit 사이의 긴 문자열",
                        )

                        new_subj_settings[subj_key] = {
                            "grades":   sel_g,
                            "classes":  sel_c,
                            "sheet_id": sel_sid,
                        }
            else:
                st.info("담당 과목을 1개 이상 선택하면 학년·반·스프레드시트 설정 탭이 나타납니다.")

            st.divider()
            if st.button("💾 교사 설정 저장", key=f"save_t_{sel_t_id}",
                         type="primary", use_container_width=True):
                if save_teacher_settings(sel_t_id, teacher_email,
                                         teacher_roster_id, new_subj_settings):
                    lines = [f"✅ **{sel_t_label}** 설정 저장 완료"]
                    for sk, cfg in new_subj_settings.items():
                        subj_name = ALL_SUBJECTS.get(sk, sk)
                        cls_list  = [f"{g}학년 {c}반"
                                     for g in cfg["grades"] for c in cfg["classes"]]
                        sid_short = (cfg["sheet_id"][:20] + "…") if len(cfg["sheet_id"]) > 20 else cfg["sheet_id"]
                        lines.append(
                            f"- **{subj_name}**: {', '.join(cls_list) or '없음'}"
                            + (f"  |  시트: `{sid_short}`" if sid_short else "")
                        )
                    st.success("\n\n".join(lines))
                    _clear_auth_caches_safe(clear_teacher_settings=True)
                else:
                    st.error("저장에 실패했습니다.")

            # 현재 저장된 설정 미리보기
            if cur_subj_cfg:
                with st.expander("📋 현재 저장된 담당 현황"):
                    for sk, cfg in cur_subj_cfg.items():
                        subj_name = ALL_SUBJECTS.get(sk, sk)
                        cls_list  = [f"{g}학년 {c}반"
                                     for g in cfg.get("grades", [])
                                     for c in cfg.get("classes", [])]
                        sid = cfg.get("sheet_id", "")
                        sid_short = (sid[:30] + "…") if len(sid) > 30 else sid
                        st.markdown(
                            f"**{subj_name}**: {', '.join(cls_list) or '없음'}"
                            + (f"  |  시트: `{sid_short}`" if sid_short else "")
                        )


# ─── 4. 과목 권한 ─────────────────────────────────────────────────────────────
with tab_perms:
    perm_tab_grade, perm_tab_group = st.tabs(
        ["🎓 학년별 과목 권한", "📂 그룹별 과목 권한"]
    )

    with perm_tab_grade:
        st.subheader("학년별 허용 과목 설정")
        st.caption("학년이 일치하는 학생은 체크된 과목만 볼 수 있습니다.")
        grade_perms = _cached_grade_perms(sheet_id)

        for grade_label in ["1", "2", "3"]:
            with st.expander(f"{grade_label}학년 과목 설정", expanded=True):
                current = grade_perms.get(grade_label, set())
                selected = []
                cols = st.columns(3)
                for i, (key, label) in enumerate(ALL_SUBJECTS.items()):
                    with cols[i % 3]:
                        if st.checkbox(label, value=(key in current),
                                       key=f"gp_{grade_label}_{key}"):
                            selected.append(key)
                if st.button(f"{grade_label}학년 저장",
                             key=f"save_grade_{grade_label}",
                             type="primary"):
                    if save_grade_permissions(grade_label, selected):
                        st.success(f"{grade_label}학년 권한 저장 완료")
                        st.rerun()
                    else:
                        st.error("저장에 실패했습니다.")

    with perm_tab_group:
        st.subheader("그룹별 허용 과목 설정")
        st.caption("그룹에 속한 일반인은 체크된 과목만 볼 수 있습니다.")
        group_perms = _cached_group_perms(sheet_id)
        group_lesson_perms = _cached_group_lesson_perms(sheet_id)
        all_groups  = get_all_groups()

        if not all_groups:
            st.info("등록된 그룹이 없습니다. [그룹 관리] 탭에서 먼저 그룹을 만드세요.")
        else:
            sel_grp_p = st.selectbox("그룹 선택", all_groups, key="perm_grp_sel")
            norm_sel_grp = _normalize_group_name(sel_grp_p)
            current_g = group_perms.get(norm_sel_grp, set())
            group_sync_sig = (norm_sel_grp, tuple(sorted(current_g)))
            if st.session_state.get("_grpp_sync_sig") != group_sync_sig:
                for key in ALL_SUBJECTS.keys():
                    st.session_state[f"grpp_{sel_grp_p}_{key}"] = (key in current_g)
                st.session_state["_grpp_sync_sig"] = group_sync_sig

            selected_g = []
            cols_g = st.columns(3)
            for i, (key, label) in enumerate(ALL_SUBJECTS.items()):
                with cols_g[i % 3]:
                    if st.checkbox(label, key=f"grpp_{sel_grp_p}_{key}"):
                        selected_g.append(key)
            if st.button("그룹 권한 저장", key="save_group_perm", type="primary"):
                if save_group_permissions(sel_grp_p, selected_g):
                    st.success(f"'{sel_grp_p}' 그룹 권한 저장 완료")
                    st.rerun()
                else:
                    st.error("저장에 실패했습니다.")

            st.divider()
            st.markdown("#### 🌟 영재 수업(단원) 접근 권한")
            st.caption("그룹명이 영재(yymmdd) 형식인 그룹에 한해, 접근 가능한 영재 수업 단원을 세부 설정합니다.")

            current_lesson = group_lesson_perms.get(norm_sel_grp, {}).get("gifted", set())

            if not _is_gifted_group_name(sel_grp_p):
                st.info("이 기능은 그룹명이 영재(yymmdd) 형식인 그룹에서만 사용할 수 있습니다. 예: 영재(260315)")
            elif "gifted" not in current_g:
                st.info("현재 이 그룹은 '영재' 교과가 허용되지 않았습니다. 먼저 위에서 영재 교과를 체크하세요.")
            else:
                lesson_labels = _gifted_lesson_labels()
                if not lesson_labels:
                    st.warning("영재 수업 목록을 불러오지 못했습니다.")
                else:
                    lesson_sync_sig = (sel_grp_p, tuple(sorted(current_lesson)))
                    if st.session_state.get("_glp_sync_sig") != lesson_sync_sig:
                        for unit_key in lesson_labels.keys():
                            st.session_state[f"glp_{sel_grp_p}_{unit_key}"] = (unit_key in current_lesson)
                        st.session_state["_glp_sync_sig"] = lesson_sync_sig

                    selected_units = []
                    for unit_key in lesson_labels.keys():
                        label = lesson_labels[unit_key]
                        if st.checkbox(label, key=f"glp_{sel_grp_p}_{unit_key}"):
                            selected_units.append(unit_key)

                    if st.button("영재 수업 권한 저장", key="save_group_gifted_lessons",
                                 type="primary"):
                        if save_group_lesson_permissions(sel_grp_p, "gifted", selected_units):
                            st.success(f"'{sel_grp_p}' 그룹 영재 수업 권한 저장 완료")
                            st.rerun()
                        else:
                            st.error("저장에 실패했습니다.")


# ─── 5. 그룹 관리 ─────────────────────────────────────────────────────────────
with tab_groups:
    st.subheader("그룹 관리")
    st.caption("일반인 사용자를 그룹으로 묶어 과목 권한을 일괄 적용합니다.")

    all_groups = get_all_groups()
    group_lesson_perms = _cached_group_lesson_perms(sheet_id)
    if all_groups:
        st.markdown("**현재 그룹 목록**")
        for g in all_groups:
            c1, c2 = st.columns([4, 1])
            with c1:
                perms = _cached_group_perms(sheet_id).get(g, set())
                label_list = [ALL_SUBJECTS.get(k, k) for k in perms]
                extra = ""
                if _is_gifted_group_name(g):
                    gifted_units = group_lesson_perms.get(g, {}).get("gifted", set())
                    extra = f" | 영재 단원 {len(gifted_units)}개 허용"
                is_teacher_grp = (_normalize_group_name(g) == MATH_TEACHER_GROUP)
                teacher_badge = " 🏫" if is_teacher_grp else ""
                st.write(
                    f"**{g}**{teacher_badge} — "
                    f"{', '.join(sorted(label_list)) or '(과목 없음)'}{extra}"
                )
            with c2:
                if st.button("삭제", key=f"del_grp_{g}", use_container_width=True):
                    if delete_group(g):
                        st.warning(f"'{g}' 그룹 삭제됨")
                        st.rerun()
    else:
        st.info("등록된 그룹이 없습니다.")

    st.divider()
    st.markdown("**새 그룹 추가**")
    new_group_name = st.text_input("그룹명", placeholder="예: 외부교사, 연구팀",
                                   key="new_group_input")
    if st.button("그룹 추가", key="add_group_btn", type="primary"):
        if not new_group_name.strip():
            st.error("그룹명을 입력하세요.")
        elif new_group_name.strip() in all_groups:
            st.error("이미 존재하는 그룹명입니다.")
        else:
            if save_group_permissions(new_group_name.strip(), []):
                st.success(f"'{new_group_name.strip()}' 그룹 생성 완료")
                st.rerun()
            else:
                st.error("그룹 생성에 실패했습니다.")


# ─── 6. 대량 등록 ─────────────────────────────────────────────────────────────
with tab_bulk:
    st.subheader("학생 대량 등록 (CSV)")
    st.caption(
        "학생 목록을 CSV 파일로 업로드하면 일괄 등록 및 자동 승인 처리합니다."
    )
    st.markdown("""
**CSV 형식** (헤더 포함):
```
학번,이름,비밀번호,학년
10101,홍길동,password1,1
20202,김철수,password2,2
```
- 아이디는 `등록연도 + 학번` 으로 자동 생성됩니다.
- 비밀번호는 8자 이상, 숫자 1개 이상 포함 필수
- 학년: 1, 2, 3 중 하나
    """)

    uploaded = st.file_uploader("CSV 파일 업로드", type=["csv"],
                                key="bulk_csv_upload")
    if uploaded:
        try:
            content = uploaded.read().decode("utf-8-sig")
            df_bulk = pd.read_csv(StringIO(content), dtype=str)
            df_bulk.columns = [c.strip() for c in df_bulk.columns]
            st.dataframe(df_bulk, use_container_width=True, hide_index=True)
            required_cols = {"학번", "이름", "비밀번호", "학년"}
            if not required_cols.issubset(set(df_bulk.columns)):
                st.error(f"필수 컬럼 누락: {required_cols - set(df_bulk.columns)}")
            else:
                rows = df_bulk.to_dict("records")
                if st.button("✅ 대량 등록 실행", key="bulk_run_btn", type="primary"):
                    with st.spinner("등록 중..."):
                        ok, fail, errors = batch_register_students(rows)
                    st.success(f"성공 {ok}건 / 실패 {fail}건")
                    if errors:
                        with st.expander("오류 목록"):
                            for e in errors:
                                st.warning(e)
                    if ok > 0:
                        _clear_auth_caches_safe(clear_users=True)
        except Exception as e:
            st.error(f"파일 파싱 오류: {e}")


# ─── 7. 계정 잠금 ─────────────────────────────────────────────────────────────
with tab_lockout:
    st.subheader("🔒 계정 잠금 관리")
    st.caption(
        "로그인 실패가 5회 이상 누적된 계정입니다. "
        "확인 후 잠금을 해제해 주세요."
    )

    if st.button("🔄 새로고침", key="lockout_refresh"):
        _clear_auth_caches_safe(clear_lockout=True)
        st.rerun()

    lockout_rows = _cached_lockout(sheet_id)

    if not lockout_rows:
        st.info("로그인 실패 기록이 없습니다.")
    else:
        df_lock = pd.DataFrame(lockout_rows)

        locked_df = (
            df_lock[df_lock["잠금상태"] == "잠금"].copy()
            if "잠금상태" in df_lock.columns
            else pd.DataFrame()
        )

        if locked_df.empty:
            st.success("✅ 현재 잠긴 계정이 없습니다.")
        else:
            st.error(f"⚠️ 잠금 계정 **{len(locked_df)}개**")
            for _, row in locked_df.iterrows():
                uid       = str(row.get("아이디", ""))
                fail_cnt  = int(row.get("실패횟수", 0) or 0)
                last_fail = str(row.get("최근실패시각", ""))
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(
                            f"**`{uid}`**  |  실패 횟수: **{fail_cnt}회**  |  "
                            f"최근 실패: {last_fail}"
                        )
                    with c2:
                        if st.button("🔓 잠금 해제", key=f"unlock_{uid}",
                                     use_container_width=True, type="primary"):
                            if reset_lockout(uid):
                                st.success(f"`{uid}` 잠금 해제 완료")
                                st.rerun()
                            else:
                                st.error("잠금 해제에 실패했습니다.")

        st.divider()
        st.markdown("#### 전체 실패 기록")
        st.dataframe(
            df_lock.sort_values("최근실패시각", ascending=False).reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.markdown("#### 개별 잠금 해제")
        all_lock_ids = [str(r.get("아이디", "")) for r in lockout_rows]
        if all_lock_ids:
            sel_lock_uid = st.selectbox("아이디 선택", all_lock_ids,
                                        key="lockout_sel_uid")
            sel_lock_row = next(
                (r for r in lockout_rows if str(r.get("아이디", "")) == sel_lock_uid), {}
            )
            st.caption(
                f"실패 횟수: {sel_lock_row.get('실패횟수', 0)}회  |  "
                f"최근 실패: {sel_lock_row.get('최근실패시각', '-')}  |  "
                f"상태: {sel_lock_row.get('잠금상태', '-')}"
            )
            if st.button("🔓 선택 계정 잠금 해제 / 횟수 초기화",
                         key="lockout_manual_reset", type="primary"):
                if reset_lockout(sel_lock_uid):
                    st.success(f"`{sel_lock_uid}` 초기화 완료")
                    st.rerun()
                else:
                    st.error("초기화에 실패했습니다.")
