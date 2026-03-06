# pages/98_진도표.py
"""
진도표 관리 페이지
- 관리자 모드 전용
- 수업 진도를 날짜별/반별로 기록하고 구글 시트와 실시간 연동
"""
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import json

st.set_page_config(page_title="진도표 관리", layout="wide")

# ── 기본 멀티페이지 nav 숨김 ─────────────────────────────────────────────────
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

# ── 사이드바 ─────────────────────────────────────────────────────────────────
st.sidebar.page_link("home.py", label="🏠 홈으로 돌아가기", use_container_width=True)

# ── 관리자 모드 체크 ──────────────────────────────────────────────────────────
if not st.session_state.get("_dev_mode", False):
    st.error("🔒 이 페이지는 **관리자 모드**에서만 접근할 수 있습니다.")
    st.info("홈 화면 사이드바에서 관리자 모드로 로그인한 후 다시 방문해 주세요.")
    st.stop()

# ── 상수 / 설정 ───────────────────────────────────────────────────────────────
CLASSES = [
    "1학년 9반 (공통수학)",
    "1학년 10반 (공통수학)",
    "2학년 9반 (확률과통계)",
    "2학년 10반 (확률과통계)",
    "2학년 11반 (확률과통계)",
]
STUDENT_COUNTS = {
    "1학년 9반 (공통수학)": 35,
    "1학년 10반 (공통수학)": 35,
    "2학년 9반 (확률과통계)": 34,
    "2학년 10반 (확률과통계)": 35,
    "2학년 11반 (확률과통계)": 34,
}

DAY_KR = ["월", "화", "수", "목", "금"]

# ── 기본 시간표 (이미지 시간표 기준) ─────────────────────────────────────────
# 추후 페이지에서 수정 가능. 구글 시트 반영 없이 세션에서만 관리
DEFAULT_SCHEDULE: dict = {
    "월": ["1학년 9반 (공통수학)", "1학년 10반 (공통수학)", "2학년 9반 (확률과통계)"],
    "화": ["1학년 9반 (공통수학)", "1학년 10반 (공통수학)", "2학년 10반 (확률과통계)", "2학년 11반 (확률과통계)"],
    "수": ["1학년 9반 (공통수학)", "2학년 11반 (확률과통계)"],
    "목": ["1학년 10반 (공통수학)", "2학년 9반 (확률과통계)", "2학년 10반 (확률과통계)", "2학년 11반 (확률과통계)"],
    "금": ["1학년 9반 (공통수학)", "1학년 10반 (공통수학)", "2학년 9반 (확률과통계)", "2학년 10반 (확률과통계)"],
}

# 반별 음영 색상 (공통수학 계열 / 확률과통계 계열)
CLASS_COLORS = {
    "1학년 9반 (공통수학)":    ("#fef9c3", "#854d0e"),  # 연노랑
    "1학년 10반 (공통수학)":   ("#fef9c3", "#854d0e"),  # 연노랑
    "2학년 9반 (확률과통계)":  ("#ffedd5", "#9a3412"),  # 연주황
    "2학년 10반 (확률과통계)": ("#ffedd5", "#9a3412"),  # 연주황
    "2학년 11반 (확률과통계)": ("#ffedd5", "#9a3412"),  # 연주황
}

def _get_schedule() -> dict:
    """세션 상태에서 기본 요일별 시간표를 읽습니다. 없으면 기본값 반환."""
    if "_timetable" not in st.session_state:
        st.session_state["_timetable"] = {k: list(v) for k, v in DEFAULT_SCHEDULE.items()}
    return st.session_state["_timetable"]

def _get_date_overrides() -> dict:
    """날짜별 예외 시간표를 읽습니다. { 'YYYY-MM-DD': [cls, ...] }"""
    if "_date_overrides" not in st.session_state:
        st.session_state["_date_overrides"] = {}
    return st.session_state["_date_overrides"]

def _get_active_classes(date_iso: str, day: str) -> list:
    """특정 날짜의 실제 수업 반 목록 반환. 날짜 예외 → 기본 요일 순으로 폴백."""
    overrides = _get_date_overrides()
    if date_iso in overrides:
        return overrides[date_iso]
    return _get_schedule().get(day, [])

# 학기 기간: 2026-03-02 ~ 2026-07-17 (1학기 종업식 전후)
SEMESTER_START = date(2026, 3, 2)
SEMESTER_END   = date(2026, 7, 17)

SHEET_NAME = "진도표"   # 구글 시트 내 워크시트 이름

# ── 날짜 목록 생성 (주말 제외) ────────────────────────────────────────────────
def generate_weekdays(start: date, end: date) -> list[date]:
    days = []
    cur = start
    while cur <= end:
        if cur.weekday() < 5:   # 0=월 ~ 4=금
            days.append(cur)
        cur += timedelta(days=1)
    return days

ALL_DATES: list[date] = generate_weekdays(SEMESTER_START, SEMESTER_END)

# ── 구글 시트 연결 ────────────────────────────────────────────────────────────
def _get_gspread_client():
    """gspread 클라이언트를 반환. 실패 시 None."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        # st.secrets["gcp_service_account"] 에 서비스 계정 JSON을 저장해야 합니다
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return gspread.authorize(creds)
    except Exception:
        return None


def _get_spreadsheet_id() -> str:
    """secrets에서 구글 시트 ID를 읽어옵니다."""
    try:
        return st.secrets["spreadsheet_id"]
    except Exception:
        return ""


@st.cache_data(ttl=30, show_spinner=False)
def load_sheet_data(spreadsheet_id: str) -> dict:
    """
    구글 시트에서 진도표 데이터를 읽어 dict로 반환합니다.
    반환형: { "YYYY-MM-DD": {"1학년 9반 (공통수학)": "...", ..., "비고": "..."} }
    """
    client = _get_gspread_client()
    if client is None or not spreadsheet_id:
        return {}
    try:
        sh = client.open_by_key(spreadsheet_id)
        ws = sh.worksheet(SHEET_NAME)
        records = ws.get_all_records()   # 첫 번째 행이 헤더
        result = {}
        for row in records:
            d = str(row.get("날짜", "")).strip()
            if not d:
                continue
            result[d] = {
                cls: str(row.get(cls, "")) for cls in CLASSES
            }
            result[d]["비고"] = str(row.get("비고", ""))
        return result
    except Exception as e:
        st.warning(f"구글 시트 데이터 불러오기 실패: {e}")
        return {}


def save_row_to_sheet(spreadsheet_id: str, date_str: str, row_data: dict) -> bool:
    """
    특정 날짜의 행 데이터를 구글 시트에 저장(없으면 추가, 있으면 수정).
    row_data: { "1학년 9반 (공통수학)": "...", ..., "비고": "..." }
    """
    client = _get_gspread_client()
    if client is None or not spreadsheet_id:
        return False
    try:
        sh = client.open_by_key(spreadsheet_id)
        ws = sh.worksheet(SHEET_NAME)

        # 날짜 → 요일 계산
        d = date.fromisoformat(date_str)
        day_str = DAY_KR[d.weekday()]
        new_row = [date_str, day_str] + [row_data.get(cls, "") for cls in CLASSES] + [row_data.get("비고", "")]
        num_cols = len(new_row)

        # 전체 데이터 읽기
        all_data = ws.get_all_values()

        # 헤더 확인 (빈 행 방어)
        has_header = (
            bool(all_data)
            and bool(all_data[0])
            and all_data[0][0] == "날짜"
        )
        if not has_header:
            ws.clear()
            header_row = ["날짜", "요일"] + CLASSES + ["비고"]
            ws.append_row(header_row)
            all_data = [header_row]

        # 해당 날짜 행 검색 (0-based index)
        target_sheet_row = None   # 시트 1-based row 번호
        for i, row in enumerate(all_data):
            if row and row[0] == date_str:
                target_sheet_row = i + 1  # 시트는 1-indexed
                break

        if target_sheet_row:
            # 기존 행 업데이트: update_cells 사용 (gspread v5/v6 모두 호환)
            end_col = chr(ord("A") + num_cols - 1)
            cell_list = ws.range(f"A{target_sheet_row}:{end_col}{target_sheet_row}")
            for i, cell in enumerate(cell_list):
                cell.value = new_row[i]
            ws.update_cells(cell_list)
        else:
            # 새 행 추가
            ws.append_row(new_row)

        return True
    except Exception as e:
        st.error(f"저장 실패: {e}")
        return False


def init_sheet(spreadsheet_id: str):
    """구글 시트에 헤더 행을 초기화합니다."""
    client = _get_gspread_client()
    if client is None or not spreadsheet_id:
        return False
    try:
        sh = client.open_by_key(spreadsheet_id)
        try:
            ws = sh.worksheet(SHEET_NAME)
        except Exception:
            ws = sh.add_worksheet(title=SHEET_NAME, rows=200, cols=10)
        all_data = ws.get_all_values()
        if not all_data or all_data[0][0] != "날짜":
            header_row = ["날짜", "요일"] + CLASSES + ["비고"]
            ws.clear()
            ws.append_row(header_row)
        return True
    except Exception as e:
        st.error(f"시트 초기화 실패: {e}")
        return False


# ── 메인 UI ───────────────────────────────────────────────────────────────────
st.title("📋 수업 진도표")
st.caption(f"학기: {SEMESTER_START.strftime('%Y.%m.%d')} ~ {SEMESTER_END.strftime('%Y.%m.%d')}  |  관리자 전용")

# ── 구글 시트 연결 상태 ────────────────────────────────────────────────────────
spreadsheet_id = _get_spreadsheet_id()
client_ok = _get_gspread_client() is not None

with st.expander("⚙️ 구글 시트 연동 상태 (클릭하여 확인 / 설정 안내)", expanded=not client_ok):
    if client_ok and spreadsheet_id:
        st.success(f"✅ 구글 시트 연동 중  |  Spreadsheet ID: `{spreadsheet_id}`")
        if st.button("🔧 시트 헤더 초기화 (첫 사용 시)", key="init_sheet_btn"):
            if init_sheet(spreadsheet_id):
                st.success("시트 헤더가 초기화되었습니다.")
    else:
        st.warning("⚠️ 구글 시트가 연동되어 있지 않습니다. 아래 안내에 따라 설정하세요.")
        st.markdown("""
**1.** Google Cloud → Google Sheets API / Drive API 사용 설정  
**2.** 서비스 계정 만들기 → JSON 키 다운로드  
**3.** 구글 시트 생성 → 시트 탭 이름 `진도표` → 서비스 계정 이메일과 편집자 공유  
**4.** Streamlit Cloud Secrets 또는 `.streamlit/secrets.toml` 에 아래 내용 입력:
```toml
spreadsheet_id = "구글시트ID"
[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
client_email = "...@....iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```
        """)

# ── 데이터 로드 ────────────────────────────────────────────────────────────────
if client_ok and spreadsheet_id:
    with st.spinner("구글 시트에서 데이터 불러오는 중…"):
        sheet_data: dict = load_sheet_data(spreadsheet_id)
else:
    sheet_data: dict = {}

# ── 진도표 DataFrame 생성 ─────────────────────────────────────────────────────
today = date.today()
rows = []
for d in ALL_DATES:
    date_str = d.isoformat()
    day_str = DAY_KR[d.weekday()]
    saved = sheet_data.get(date_str, {})
    row = {"날짜": f"{d.month}/{d.day}", "요일": day_str, "_date_iso": date_str}
    for cls in CLASSES:
        row[cls] = saved.get(cls, "")
    row["비고"] = saved.get("비고", "")
    rows.append(row)
df_all = pd.DataFrame(rows)

# ── 스타일 헬퍼 ───────────────────────────────────────────────────────────────
def _style_row(row) -> list:
    date_iso = row.get("_date_iso", "")
    day = row.get("요일", "")
    active = _get_active_classes(date_iso, day)
    has_override = date_iso in _get_date_overrides()
    result = []
    for col in row.index:
        if col in CLASSES and col in active:
            bg, fg = CLASS_COLORS.get(col, ("#e0f2fe", "#0c4a6e"))
            border = "border: 2px solid #f59e0b;" if has_override else ""
            result.append(f"background-color:{bg};color:{fg};font-weight:500;{border}")
        elif col == "요일":
            result.append("font-weight:bold")
        elif col == "날짜" and has_override:
            result.append("color:#d97706;font-weight:bold")  # 예외 날짜는 주황 강조
        else:
            result.append("")
    return result

def _build_styled_df(dates_list: list) -> "pd.io.formats.style.Styler":
    display_cols = ["날짜", "요일", "_date_iso"] + CLASSES + ["비고"]
    df = df_all[df_all["_date_iso"].isin([d.isoformat() for d in dates_list])][display_cols].copy()
    df = df.reset_index(drop=True)
    return df.style.apply(_style_row, axis=1), df

# ── 기간 필터 (탭 공통) ───────────────────────────────────────────────────────
month_map = {"3월": 3, "4월": 4, "5월": 5, "6월": 6, "7월": 7}
sel_filter = st.radio(
    "기간 필터", ["전체 기간", "3월", "4월", "5월", "6월", "7월"],
    horizontal=True, index=0, label_visibility="collapsed"
)
filtered_dates = (
    [d for d in ALL_DATES if d.month == month_map[sel_filter]]
    if sel_filter != "전체 기간" else ALL_DATES
)

# ══════════════════════════════════════════════════════════════════════════════
# 탭 구성
# ══════════════════════════════════════════════════════════════════════════════
tab_schedule, tab_data = st.tabs(["🗓️ 시간표 설정 (음영 기준)", "📝 진도 입력 / 조회"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 : 시간표 설정
# ─────────────────────────────────────────────────────────────────────────────
with tab_schedule:
    st.subheader("1️⃣ 기본 요일별 시간표")
    st.caption("매주 반복되는 기본 시간표입니다. 특정 날짜만 바꾸려면 아래 '날짜별 예외'를 사용하세요.")

    schedule = _get_schedule()
    day_cols = st.columns(5)
    new_schedule: dict = {}
    for i, day in enumerate(DAY_KR):
        with day_cols[i]:
            st.markdown(f"**{day}요일**")
            selected = []
            for cls in CLASSES:
                short = cls.replace(" (공통수학)", " (공수)").replace(" (확률과통계)", " (확통)")
                if st.checkbox(short, value=(cls in schedule.get(day, [])), key=f"sch_{day}_{cls}"):
                    selected.append(cls)
            new_schedule[day] = selected

    if st.button("✅ 기본 시간표 저장", type="primary", use_container_width=True, key="save_default_schedule"):
        st.session_state["_timetable"] = new_schedule
        st.success("기본 시간표가 저장되었습니다.")
        st.rerun()

    st.divider()
    st.subheader("2️⃣ 날짜별 예외 시간표")
    st.caption("특정 날짜만 수업이 바뀔 때 사용합니다. 설정하면 해당 날짜 진도표에 주황 테두리로 표시됩니다.")

    overrides = _get_date_overrides()

    # 새 예외 추가
    with st.form("override_form"):
        ov_date = st.date_input(
            "날짜 선택",
            value=today if today in ALL_DATES else ALL_DATES[0],
            min_value=SEMESTER_START, max_value=SEMESTER_END,
            key="override_date_input",
        )
        ov_cols = st.columns(len(CLASSES))
        ov_selected = []
        ov_date_iso = ov_date.isoformat()
        existing_ov = overrides.get(ov_date_iso, _get_schedule().get(DAY_KR[ov_date.weekday()], []))
        for i, cls in enumerate(CLASSES):
            with ov_cols[i]:
                short = cls.replace(" (공통수학)", "\n(공수)").replace(" (확률과통계)", "\n(확통)")
                if st.checkbox(short, value=(cls in existing_ov), key=f"ov_{cls}"):
                    ov_selected.append(cls)
        col_add, col_del = st.columns(2)
        with col_add:
            add_btn = st.form_submit_button("➕ 예외 저장", type="primary", use_container_width=True)
        with col_del:
            del_btn = st.form_submit_button("🗑️ 이 날짜 예외 삭제", use_container_width=True)

    if add_btn:
        st.session_state["_date_overrides"][ov_date_iso] = ov_selected
        st.success(f"{ov_date.strftime('%m/%d')} ({DAY_KR[ov_date.weekday()]}) 예외가 저장되었습니다.")
        st.rerun()
    if del_btn:
        st.session_state.get("_date_overrides", {}).pop(ov_date_iso, None)
        st.success(f"{ov_date.strftime('%m/%d')} 예외가 삭제되었습니다.")
        st.rerun()

    # 현재 예외 목록
    if overrides:
        st.markdown("**현재 설정된 예외 목록:**")
        for iso, cls_list in sorted(overrides.items()):
            try:
                d = date.fromisoformat(iso)
                label = f"{d.month}/{d.day} ({DAY_KR[d.weekday()]})"
            except Exception:
                label = iso
            cls_names = ", ".join([c.split(" (")[0] for c in cls_list]) if cls_list else "수업 없음"
            st.markdown(f"- 🔶 **{label}**: {cls_names}")
    else:
        st.caption("설정된 날짜별 예외가 없습니다.")

    # 범례
    st.divider()
    st.caption("음영 범례:")
    leg_cols = st.columns(len(CLASSES))
    for i, cls in enumerate(CLASSES):
        bg, fg = CLASS_COLORS[cls]
        with leg_cols[i]:
            st.markdown(
                f'<span style="background:{bg};color:{fg};padding:3px 8px;border-radius:4px;font-size:0.82em">'
                f'{cls.split(" (")[0]} ({STUDENT_COUNTS[cls]}명)</span>',
                unsafe_allow_html=True
            )
    st.caption("🔶 날짜 주황 표시 = 예외 시간표 적용 중")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 : 진도 입력 / 조회
# ─────────────────────────────────────────────────────────────────────────────
with tab_data:
    col_r, col_ref = st.columns([4, 1])
    with col_ref:
        if st.button("🔄 새로고침", use_container_width=True, key="refresh_btn"):
            st.cache_data.clear()
            st.rerun()

    # ── 컬러 진도표 (음영 적용, 읽기 전용) ─────────────────────────────────
    st.subheader("📅 진도표 현황")
    _styled_unused, df_view = _build_styled_df(filtered_dates)

    # _date_iso 컬럼을 column_config에서 None으로 숨김, 스타일은 전체 row에 적용
    st.dataframe(
        df_view.style.apply(_style_row, axis=1),
        use_container_width=True,
        hide_index=True,
        column_config={
            "_date_iso": None,  # 화면에서 숨김
            "날짜": st.column_config.TextColumn("날짜", width="small"),
            "요일": st.column_config.TextColumn("요일", width="small"),
            **{cls: st.column_config.TextColumn(cls, width="medium") for cls in CLASSES},
            "비고": st.column_config.TextColumn("비고", width="medium"),
        },
    )

    # 범례 (간소화)
    leg_c = st.columns(len(CLASSES) + 1)
    with leg_c[0]:
        st.caption("범례:")
    for i, cls in enumerate(CLASSES):
        bg, fg = CLASS_COLORS[cls]
        with leg_c[i + 1]:
            st.markdown(
                f'<span style="background:{bg};color:{fg};padding:2px 6px;border-radius:4px;font-size:0.78em">'
                f'{cls.split(" (")[0]}</span>',
                unsafe_allow_html=True
            )

    # ── 날짜 선택하여 진도 입력/수정 ────────────────────────────────────────
    st.divider()
    st.subheader("✏️ 날짜 선택하여 진도 입력 / 수정")

    today_idx = next((i for i, d in enumerate(ALL_DATES) if d == today), 0)
    sel_idx = st.selectbox(
        "날짜 선택",
        options=range(len(ALL_DATES)),
        format_func=lambda i: (
            f"{'★ ' if ALL_DATES[i] == today else ''}"
            f"{ALL_DATES[i].month}/{ALL_DATES[i].day}"
            f" ({DAY_KR[ALL_DATES[i].weekday()]})"
            f"{'  ← 오늘' if ALL_DATES[i] == today else ''}"
        ),
        index=today_idx,
        key="data_date_sel",
    )
    sel_date = ALL_DATES[sel_idx]
    sel_iso = sel_date.isoformat()
    sel_day = DAY_KR[sel_date.weekday()]
    active_cls = _get_active_classes(sel_iso, sel_day)
    is_override = sel_iso in _get_date_overrides()

    # 선택 날짜 요약
    override_badge = " 🔶 예외 시간표 적용" if is_override else ""
    _cls_badges = " / ".join(
        '<span style="background:{};color:{};padding:1px 6px;border-radius:3px;font-size:0.9em">{}</span>'.format(
            CLASS_COLORS[c][0], CLASS_COLORS[c][1], c.split(" (")[0]
        )
        for c in active_cls
    ) if active_cls else "수업 없음"
    st.markdown(
        f"**{sel_date.strftime('%Y년 %m월 %d일')} ({sel_day}요일)**{override_badge}  \n"
        f"수업 반: {_cls_badges}",
        unsafe_allow_html=True
    )

    existing = sheet_data.get(sel_iso, {})

    with st.form("data_input_form", border=True):
        # 수업 있는 반만 우선 표시, 나머지도 표시하되 비수업일 칸은 흐리게
        input_cols = st.columns(len(CLASSES))
        inputs: dict = {}
        for i, cls in enumerate(CLASSES):
            with input_cols[i]:
                is_active = cls in active_cls
                bg, fg = CLASS_COLORS[cls]
                # 헤더 레이블에 색상 뱃지
                if is_active:
                    st.markdown(
                        f'<div style="background:{bg};color:{fg};padding:4px 8px;border-radius:6px;'
                        f'font-size:0.82em;font-weight:600;margin-bottom:4px">'
                        f'{cls.split(" (")[0]}<br>({STUDENT_COUNTS[cls]}명) 📌</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div style="color:#9ca3af;font-size:0.82em;margin-bottom:4px">'
                        f'{cls.split(" (")[0]} (비수업일)</div>',
                        unsafe_allow_html=True
                    )
                inputs[cls] = st.text_area(
                    label=cls,
                    value=existing.get(cls, ""),
                    height=110,
                    key=f"inp_{cls}",
                    label_visibility="collapsed",
                    disabled=False,
                )
        note = st.text_input("비고", value=existing.get("비고", ""), key="inp_note")

        c1, c2 = st.columns([3, 1])
        with c1:
            submitted = st.form_submit_button(
                "💾 저장 (구글 시트 반영)",
                type="primary", use_container_width=True,
                disabled=not (client_ok and bool(spreadsheet_id)),
            )
        with c2:
            clear_btn = st.form_submit_button("🗑️ 이 날짜 초기화", use_container_width=True)

    if submitted:
        row_data = {cls: inputs[cls] for cls in CLASSES}
        row_data["비고"] = note
        with st.spinner("저장 중…"):
            ok = save_row_to_sheet(spreadsheet_id, sel_iso, row_data)
        if ok:
            st.success(f"✅ {sel_date.strftime('%m/%d')} 진도 내용이 저장되었습니다.")
            st.cache_data.clear()
            st.rerun()

    if clear_btn:
        row_data = {cls: "" for cls in CLASSES}
        row_data["비고"] = ""
        with st.spinner("초기화 중…"):
            ok = save_row_to_sheet(spreadsheet_id, sel_iso, row_data)
        if ok:
            st.success(f"✅ {sel_date.strftime('%m/%d')} 데이터가 초기화되었습니다.")
            st.cache_data.clear()
            st.rerun()

    if not client_ok or not spreadsheet_id:
        st.info("💡 구글 시트 연동 설정 후 저장이 가능합니다. 상단 '구글 시트 연동 상태'를 확인하세요.")

