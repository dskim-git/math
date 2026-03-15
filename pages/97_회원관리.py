# pages/97_회원관리.py
"""
회원 관리 페이지 (관리자 전용)

탭 구성:
  1. 가입 승인   – 대기 중인 신청 승인/거부
  2. 학생 관리   – 학생 목록, 상태 변경, 비밀번호 재설정
  3. 일반인 관리 – 일반인 목록, 그룹 배정, 비밀번호 재설정
  4. 과목 권한   – 학년별·그룹별 허용 과목 설정
  5. 그룹 관리   – 그룹 생성/삭제
  6. 대량 등록   – CSV로 학생 계정 일괄 생성
"""
import sys
from pathlib import Path
import ast
import re

# pages/ 에서 root 디렉터리를 sys.path에 추가
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

# 관리자 기능 바로가기
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

if not st.session_state.get("_dev_mode", False):
    st.error("🔒 이 페이지는 **관리자 모드**에서만 접근할 수 있습니다.")
    st.stop()

# ── 임포트 ───────────────────────────────────────────────────────────────────
from auth_utils import (
    ALL_SUBJECTS,
    WS_STUDENTS, WS_GENERAL, WS_LOCKOUT,
    STATUS_PENDING, STATUS_APPROVED, STATUS_REJECTED,
    _cached_students, _cached_general,
    _cached_grade_perms, _cached_group_perms, _cached_group_lesson_perms, _cached_lockout,
    _cached_roster, get_roster_student_counts, verify_roster_student,
    get_roster_debug_info,
    _get_users_spreadsheet_id,
    update_user_status, reset_user_password,
    update_user_group, save_grade_permissions,
    save_group_permissions, save_group_lesson_permissions, delete_group,
    get_all_groups, batch_register_students,
    check_password_policy,
    is_account_locked, reset_lockout,
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
    """영재 수업 단원 권한을 부여할 수 있는 그룹명 형식인지 검사합니다."""
    name = str(group_name)
    # 시트에서 복사된 보이지 않는 공백/전각 괄호를 허용
    name = name.replace("\u200b", "").replace("\ufeff", "").strip()
    name = name.replace("（", "(").replace("）", ")")
    return bool(re.fullmatch(r"영재\s*\(\s*\d{6}\s*\)", name))


def _normalize_group_name(group_name: str) -> str:
    name = str(group_name or "")
    name = name.replace("\u200b", "").replace("\ufeff", "").strip()
    name = name.replace("（", "(").replace("）", ")")
    return name

# ─────────────────────────────────────────────────────────────────────────────
st.title("👥 회원 관리")
st.caption("회원 가입 승인, 과목 권한 설정 등 사용자 관리 기능입니다.")
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
    )
    st.rerun()

sheet_id = _get_users_spreadsheet_id()

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


# ─── 1. 가입 승인 ─────────────────────────────────────────────────────────────
with tab_approve:
    st.subheader("가입 승인 대기 목록")

    students_all = _cached_students(sheet_id)
    general_all  = _cached_general(sheet_id)

    pending_s = [r for r in students_all
                 if str(r.get("승인상태", "")).strip() == STATUS_PENDING]
    pending_g = [r for r in general_all
                 if str(r.get("승인상태", "")).strip() == STATUS_PENDING]

    total_pending = len(pending_s) + len(pending_g)
    if total_pending == 0:
        st.success("✅ 승인 대기 중인 가입 신청이 없습니다.")
    else:
        st.info(f"총 **{total_pending}건** 대기 중 (학생 {len(pending_s)}명 / 일반인 {len(pending_g)}명)")

    # 학생 대기
    if pending_s:
        st.markdown("#### 📚 학생")
        roster_rows = _cached_roster(sheet_id)
        for row in pending_s:
            uid   = str(row.get("아이디", ""))
            name  = str(row.get("이름", ""))
            num   = str(row.get("학번", ""))
            grade = str(row.get("학년", ""))
            joined = str(row.get("가입일", ""))

            # 명단 검증
            in_roster = verify_roster_student(sheet_id, num, name)
            roster_badge = (
                "✅ 명단 확인됨"  if in_roster
                else "⚠️ 명단에 없음 (학번·이름 불일치 또는 미등록)"
            )
            roster_color = "green" if in_roster else "red"

            with st.container(border=True):
                st.markdown(
                    f"**{name}** (`{uid}`)  |  학번: `{num}`  |  "
                    f"학년: {grade}  |  가입일: {joined}"
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

    # 일반인 대기
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
    st.subheader("학생 목록")
    students_all = _cached_students(sheet_id)
    if not students_all:
        st.info("등록된 학생이 없습니다.")
    else:
        df_s = pd.DataFrame(students_all)
        # 해시비밀번호 컬럼은 표시하지 않음
        display_cols = [c for c in df_s.columns if c != "해시비밀번호"]
        st.dataframe(df_s[display_cols], use_container_width=True,
                     hide_index=True)

        st.divider()
        st.markdown("#### 상태 변경 / 비밀번호 재설정")

        # "이름(아이디)" 형식으로 표시
        def _s_label(r):
            return f"{r.get('이름', '')}({r.get('아이디', '')})"
        student_options = {_s_label(r): str(r.get("아이디", "")) for r in students_all}
        sel_label_s = st.selectbox("학생 선택", list(student_options.keys()),
                                   key="mgmt_sel_student")
        sel_uid = student_options[sel_label_s]
        sel_row = next((r for r in students_all
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
    st.caption("구글 시트 '2026수강생명단'을 기준으로 가입 상태를 확인합니다.")

    roster_all = _cached_roster(sheet_id)
    if not roster_all:
        debug = get_roster_debug_info(sheet_id)
        if debug["ok"]:
            st.info("ℹ️ '2026수강생명단' 시트에 데이터가 없습니다.")
        else:
            st.error(f"❌ 명단 로드 실패: {debug['error']}")
            if debug.get("worksheets"):
                st.caption(f"스프레드시트({debug['sheet_id'][:20]}…) 탭 목록: {', '.join(debug['worksheets'])}")
            else:
                st.caption(f"접근한 스프레드시트 ID: `{debug['sheet_id']}`")
            st.caption(
                "💡 '2026수강생명단' 시트가 **회원관리 구글시트** (`users_spreadsheet_id`)에 있는지 확인하세요. "
                "진도표용 시트(`spreadsheet_id`)가 아닌 회원관리용 시트에 추가해야 합니다."
            )
    else:
        # 이미 가입된 학생의 (학번, 이름) 집합
        registered_nums = {
            str(r.get("학번", "")).strip()
            for r in students_all
            if str(r.get("승인상태", "")).strip() in (STATUS_APPROVED, STATUS_PENDING)
        }

        # 반 목록 추출 (시트 순서 유지)
        all_classes_in_roster = []
        seen = set()
        for r in roster_all:
            cls = str(r.get("반", "") or r.get("학급", "")).strip()
            if cls and cls not in seen:
                all_classes_in_roster.append(cls)
                seen.add(cls)

        # 학급 선택 탭 (사이드 탭)
        sel_cls = st.selectbox(
            "학급 선택",
            all_classes_in_roster,
            key="roster_cls_sel",
        )

        cls_students = [
            r for r in roster_all
            if str(r.get("반", "") or r.get("학급", "")).strip() == sel_cls
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

        # 전체 명단 (가입 여부 포함)
        with st.expander("📋 전체 명단 보기", expanded=False):
            roster_display = []
            for r in cls_students:
                num  = str(r.get("학번", "")).strip()
                nm   = str(r.get("이름", "")).strip()
                is_joined = num in registered_nums
                # 가입 상태 상세
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
                return "background-color:#334155;color:#94a3b8"  # 미가입

            if df_roster.empty:
                st.info("명단 데이터가 없습니다.")
            else:
                # pandas 버전에 따라 applymap → map 폴백
                try:
                    styled = df_roster.style.map(_color_status, subset=["가입상태"])
                except AttributeError:
                    styled = df_roster.style.applymap(_color_status, subset=["가입상태"])
                st.dataframe(styled, use_container_width=True, hide_index=True)

        # 미가입 학생 목록
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


# ─── 3. 일반인 관리 ──────────────────────────────────────────────────────────
with tab_general:
    st.subheader("일반인 목록")
    general_all = _cached_general(sheet_id)
    if not general_all:
        st.info("등록된 일반인이 없습니다.")
    else:
        df_g = pd.DataFrame(general_all)
        display_cols_g = [c for c in df_g.columns if c != "해시비밀번호"]
        st.dataframe(df_g[display_cols_g], use_container_width=True,
                     hide_index=True)

        st.divider()
        st.markdown("#### 그룹 배정 / 상태 변경 / 비밀번호 재설정")

        # "이름(아이디)" 형식으로 표시
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


# ─── 4. 과목 권한 ─────────────────────────────────────────────────────────────
with tab_perms:
    perm_tab_grade, perm_tab_group = st.tabs(
        ["🎓 학년별 과목 권한", "📂 그룹별 과목 권한"]
    )

    # 학년별
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

    # 그룹별
    with perm_tab_group:
        st.subheader("그룹별 허용 과목 설정")
        st.caption("그룹에 속한 일반인은 체크된 과목만 볼 수 있습니다.")
        group_perms = _cached_group_perms(sheet_id)
        group_lesson_perms = _cached_group_lesson_perms(sheet_id)
        all_groups  = get_all_groups()

        if not all_groups:
            st.info("등록된 그룹이 없습니다. [그룹 관리] 탭에서 먼저 그룹을 만드세요.")
        else:
            sel_grp_p = st.selectbox("그룹 선택", all_groups,
                                     key="perm_grp_sel")
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
            if st.button("그룹 권한 저장", key="save_group_perm",
                         type="primary"):
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
                    st.warning("영재 수업 목록을 불러오지 못했습니다. activities/gifted/lessons/_units.py를 확인하세요.")
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

                    if st.button("영재 수업 권한 저장", key="save_group_gifted_lessons", type="primary"):
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
                st.write(f"**{g}** — {', '.join(sorted(label_list)) or '(과목 없음)'}{extra}")
            with c2:
                if st.button("삭제", key=f"del_grp_{g}",
                             use_container_width=True):
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
            # 빈 허용과목으로 그룹 생성
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
                if st.button("✅ 대량 등록 실행", key="bulk_run_btn",
                             type="primary"):
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
        import pandas as pd

        df_lock = pd.DataFrame(lockout_rows)

        # 잠금 계정만 별도 표시
        locked_df = df_lock[df_lock["잠금상태"] == "잠금"].copy() if "잠금상태" in df_lock.columns else pd.DataFrame()

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
        st.caption("잠금 여부와 관계없이 1회 이상 실패한 모든 계정 기록입니다.")
        st.dataframe(
            df_lock.sort_values("최근실패시각", ascending=False)
                   .reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.markdown("#### 개별 잠금 해제")
        st.caption("잠기지 않은 계정의 실패 횟수도 여기서 초기화할 수 있습니다.")
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

