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

# pages/ 에서 root 디렉터리를 sys.path에 추가
_root = str(Path(__file__).parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="회원 관리", layout="wide")

# 기본 멀티페이지 내비게이션 숨김
st.markdown("""
<style>
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavContainer"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavLink"],
section[data-testid="stSidebar"] nav
{ display: none !important; visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

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
    _cached_grade_perms, _cached_group_perms, _cached_lockout,
    _get_users_spreadsheet_id,
    update_user_status, reset_user_password,
    update_user_group, save_grade_permissions,
    save_group_permissions, delete_group,
    get_all_groups, batch_register_students,
    check_password_policy,
    is_account_locked, reset_lockout,
)

# ─────────────────────────────────────────────────────────────────────────────
st.title("👥 회원 관리")
st.caption("회원 가입 승인, 과목 권한 설정 등 사용자 관리 기능입니다.")
st.divider()

# 새로고침
if st.button("🔄 데이터 새로고침", key="mgmt_refresh"):
    st.cache_data.clear()
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
        for row in pending_s:
            uid   = str(row.get("아이디", ""))
            name  = str(row.get("이름", ""))
            num   = str(row.get("학번", ""))
            grade = str(row.get("학년", ""))
            joined = str(row.get("가입일", ""))
            with st.container(border=True):
                st.markdown(
                    f"**{name}** (`{uid}`)  |  학번: `{num}`  |  "
                    f"학년: {grade}  |  가입일: {joined}"
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ 승인", key=f"apv_s_{uid}",
                                 use_container_width=True, type="primary"):
                        if update_user_status("student", uid, STATUS_APPROVED):
                            st.success(f"{name} 승인 완료")
                            st.cache_data.clear()
                            st.rerun()
                with c2:
                    if st.button("❌ 거부", key=f"rej_s_{uid}",
                                 use_container_width=True):
                        if update_user_status("student", uid, STATUS_REJECTED):
                            st.warning(f"{name} 거부됨")
                            st.cache_data.clear()
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
                            st.cache_data.clear()
                            st.rerun()
                with c2:
                    if st.button("❌ 거부", key=f"rej_g_{uid}",
                                 use_container_width=True):
                        if update_user_status("general", uid, STATUS_REJECTED):
                            st.warning(f"{name} 거부됨")
                            st.cache_data.clear()
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
                    st.cache_data.clear(); st.rerun()
        with c2:
            if st.button("⏸ 대기로 변경", key="mgmt_s_pending",
                         use_container_width=True):
                if update_user_status("student", sel_uid, STATUS_PENDING):
                    st.info("대기 상태로 변경됨")
                    st.cache_data.clear(); st.rerun()
        with c3:
            if st.button("❌ 거부로 변경", key="mgmt_s_reject",
                         use_container_width=True):
                if update_user_status("student", sel_uid, STATUS_REJECTED):
                    st.warning("거부 상태로 변경됨")
                    st.cache_data.clear(); st.rerun()

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
                    st.cache_data.clear(); st.rerun()
        with col_st2:
            if st.button("✅ 승인", key="mgmt_g_approve",
                         use_container_width=True):
                if update_user_status("general", sel_gid, STATUS_APPROVED):
                    st.success("승인 완료"); st.cache_data.clear(); st.rerun()
        with col_st3:
            if st.button("❌ 거부", key="mgmt_g_reject",
                         use_container_width=True):
                if update_user_status("general", sel_gid, STATUS_REJECTED):
                    st.warning("거부됨"); st.cache_data.clear(); st.rerun()

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
                        st.cache_data.clear(); st.rerun()
                    else:
                        st.error("저장에 실패했습니다.")

    # 그룹별
    with perm_tab_group:
        st.subheader("그룹별 허용 과목 설정")
        st.caption("그룹에 속한 일반인은 체크된 과목만 볼 수 있습니다.")
        group_perms = _cached_group_perms(sheet_id)
        all_groups  = get_all_groups()

        if not all_groups:
            st.info("등록된 그룹이 없습니다. [그룹 관리] 탭에서 먼저 그룹을 만드세요.")
        else:
            sel_grp_p = st.selectbox("그룹 선택", all_groups,
                                     key="perm_grp_sel")
            current_g = group_perms.get(sel_grp_p, set())
            selected_g = []
            cols_g = st.columns(3)
            for i, (key, label) in enumerate(ALL_SUBJECTS.items()):
                with cols_g[i % 3]:
                    if st.checkbox(label, value=(key in current_g),
                                   key=f"grpp_{sel_grp_p}_{key}"):
                        selected_g.append(key)
            if st.button("그룹 권한 저장", key="save_group_perm",
                         type="primary"):
                if save_group_permissions(sel_grp_p, selected_g):
                    st.success(f"'{sel_grp_p}' 그룹 권한 저장 완료")
                    st.cache_data.clear(); st.rerun()
                else:
                    st.error("저장에 실패했습니다.")


# ─── 5. 그룹 관리 ─────────────────────────────────────────────────────────────
with tab_groups:
    st.subheader("그룹 관리")
    st.caption("일반인 사용자를 그룹으로 묶어 과목 권한을 일괄 적용합니다.")

    all_groups = get_all_groups()
    if all_groups:
        st.markdown("**현재 그룹 목록**")
        for g in all_groups:
            c1, c2 = st.columns([4, 1])
            with c1:
                perms = _cached_group_perms(sheet_id).get(g, set())
                label_list = [ALL_SUBJECTS.get(k, k) for k in perms]
                st.write(f"**{g}** — {', '.join(sorted(label_list)) or '(과목 없음)'}")
            with c2:
                if st.button("삭제", key=f"del_grp_{g}",
                             use_container_width=True):
                    if delete_group(g):
                        st.warning(f"'{g}' 그룹 삭제됨")
                        st.cache_data.clear(); st.rerun()
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
                st.cache_data.clear(); st.rerun()
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
                        st.cache_data.clear()
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
        st.cache_data.clear()
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
                                st.cache_data.clear()
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
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("초기화에 실패했습니다.")

