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
### 🛠️ 구글 시트 연동 설정 방법

**1. Google Cloud 프로젝트 및 서비스 계정 만들기**
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. **API 및 서비스 → 라이브러리** → **Google Sheets API** 및 **Google Drive API** 사용 설정
4. **API 및 서비스 → 사용자 인증 정보** → **서비스 계정 만들기**
5. 서비스 계정 생성 후 → **키 추가 → JSON** 키 파일 다운로드

**2. 구글 시트 만들기 및 공유**
1. Google Drive에서 새 스프레드시트 생성
2. 시트 이름(하단 탭)을 **`진도표`** 로 변경
3. 스프레드시트를 서비스 계정 이메일(`...@...iam.gserviceaccount.com`)과 **편집자** 권한으로 공유
4. 스프레드시트 URL에서 **ID 복사** (예: `https://docs.google.com/spreadsheets/d/<ID>/edit`)

**3. Streamlit Secrets 설정**

프로젝트 루트에 `.streamlit/secrets.toml` 파일을 만들고 아래 내용을 입력하세요:

```toml
spreadsheet_id = "여기에_구글_시트_ID_붙여넣기"

[gcp_service_account]
type = "service_account"
project_id = "프로젝트_ID"
private_key_id = "키_ID"
private_key = "-----BEGIN RSA PRIVATE KEY-----\\n...\\n-----END RSA PRIVATE KEY-----\\n"
client_email = "서비스계정@프로젝트.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
universe_domain = "googleapis.com"
```

> 📌 다운로드한 서비스 계정 JSON 파일의 내용을 그대로 복사하면 됩니다.

**4. `시트 헤더 초기화` 버튼 클릭** (페이지 새로고침 후)
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
    display_date = f"{d.month}/{d.day}"
    saved = sheet_data.get(date_str, {})
    row = {
        "날짜": display_date,
        "요일": day_str,
    }
    for cls in CLASSES:
        row[cls] = saved.get(cls, "")
    row["비고"] = saved.get("비고", "")
    row["_date_iso"] = date_str   # 내부 키 (표시 안 함)
    row["_is_today"] = (d == today)
    rows.append(row)

df_display = pd.DataFrame(rows)

# ── 진도표 표시 ────────────────────────────────────────────────────────────────
st.subheader("📅 진도표 현황")

# 인원수 정보 표시
col_info = st.columns(len(CLASSES) + 1)
with col_info[0]:
    st.markdown("&nbsp;", unsafe_allow_html=True)
for i, cls in enumerate(CLASSES):
    with col_info[i + 1]:
        st.caption(f"{cls}\n**{STUDENT_COUNTS[cls]}명**")

# 오늘 날짜 강조 필터
show_options = ["전체 기간", "3월", "4월", "5월", "6월", "7월"]
sel_filter = st.radio("기간 필터", show_options, horizontal=True, index=0, label_visibility="collapsed")

month_map = {"3월": 3, "4월": 4, "5월": 5, "6월": 6, "7월": 7}
if sel_filter != "전체 기간":
    target_month = month_map[sel_filter]
    filtered_dates = [d for d in ALL_DATES if d.month == target_month]
else:
    filtered_dates = ALL_DATES

# 표시용 DataFrame
display_cols = ["날짜", "요일"] + CLASSES + ["비고"]
df_view = df_display[df_display["_date_iso"].isin([d.isoformat() for d in filtered_dates])][display_cols].copy()
df_view = df_view.reset_index(drop=True)

# 데이터 편집기 (읽기 전용 열: 날짜, 요일)
edited_df = st.data_editor(
    df_view,
    use_container_width=True,
    hide_index=True,
    disabled=["날짜", "요일"],
    column_config={
        "날짜": st.column_config.TextColumn("날짜", width="small"),
        "요일": st.column_config.TextColumn("요일", width="small"),
        **{cls: st.column_config.TextColumn(cls, width="medium") for cls in CLASSES},
        "비고": st.column_config.TextColumn("비고", width="medium"),
    },
    key="progress_editor",
)

# ── 변경사항 감지 및 저장 ─────────────────────────────────────────────────────
has_changes = not df_view.equals(edited_df)

st.divider()

col_save, col_refresh = st.columns([2, 1])
with col_save:
    save_btn = st.button(
        "💾 변경사항 저장 (구글 시트 반영)",
        type="primary",
        use_container_width=True,
        disabled=not (has_changes and client_ok and bool(spreadsheet_id)),
    )
with col_refresh:
    if st.button("🔄 데이터 새로고침", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if not client_ok or not spreadsheet_id:
    st.info("💡 구글 시트 연동 시 변경사항 자동 저장이 가능합니다. 위 '구글 시트 연동 상태'를 참고해 설정하세요.")

if save_btn and has_changes:
    date_to_iso = {f"{d.month}/{d.day}": d.isoformat() for d in ALL_DATES}
    saved_count = 0
    errors = []
    with st.spinner("저장 중…"):
        for idx in range(len(df_view)):
            orig_series = df_view.iloc[idx][CLASSES + ["비고"]]
            new_series  = edited_df.iloc[idx][CLASSES + ["비고"]]
            if not orig_series.equals(new_series):
                date_display = edited_df.iloc[idx]["날짜"]
                date_iso = date_to_iso.get(str(date_display), "")
                if not date_iso:
                    continue
                row_data = {cls: str(edited_df.iloc[idx][cls]) for cls in CLASSES}
                row_data["비고"] = str(edited_df.iloc[idx]["비고"])
                ok = save_row_to_sheet(spreadsheet_id, date_iso, row_data)
                if ok:
                    saved_count += 1
                else:
                    errors.append(date_display)
    if saved_count:
        st.success(f"✅ {saved_count}개 행이 구글 시트에 저장되었습니다.")
        st.cache_data.clear()
        st.rerun()
    if errors:
        st.error(f"저장 실패한 날짜: {', '.join(errors)}")

# ── 빠른 입력 폼 (단건 입력) ─────────────────────────────────────────────────
st.divider()
with st.expander("✏️ 날짜 선택하여 빠르게 수업 내용 입력하기"):
    # 오늘 날짜를 기본값으로
    default_date = today if today in ALL_DATES else ALL_DATES[0] if ALL_DATES else SEMESTER_START
    date_options = ALL_DATES
    date_labels  = [f"{d.month}/{d.day} ({DAY_KR[d.weekday()]})" for d in date_options]
    default_idx = date_options.index(default_date) if default_date in date_options else 0

    sel_idx = st.selectbox(
        "날짜 선택",
        options=range(len(date_options)),
        format_func=lambda i: date_labels[i],
        index=default_idx,
        key="quick_date_sel",
    )
    sel_date = date_options[sel_idx]
    sel_date_iso = sel_date.isoformat()

    existing = sheet_data.get(sel_date_iso, {})

    st.caption(f"선택 날짜: **{sel_date.strftime('%Y년 %m월 %d일')} ({DAY_KR[sel_date.weekday()]})**")

    with st.form("quick_input_form"):
        cols = st.columns(len(CLASSES))
        inputs = {}
        for i, cls in enumerate(CLASSES):
            with cols[i]:
                inputs[cls] = st.text_area(
                    f"{cls}\n({STUDENT_COUNTS[cls]}명)",
                    value=existing.get(cls, ""),
                    height=100,
                    key=f"quick_input_{cls}",
                )
        note = st.text_input("비고", value=existing.get("비고", ""), key="quick_input_note")
        submitted = st.form_submit_button("💾 저장", type="primary", use_container_width=True)

    if submitted:
        if not client_ok or not spreadsheet_id:
            st.warning("구글 시트가 연동되지 않아 저장할 수 없습니다. 상단 설정 안내를 확인하세요.")
        else:
            row_data = {cls: inputs[cls] for cls in CLASSES}
            row_data["비고"] = note
            with st.spinner("저장 중…"):
                ok = save_row_to_sheet(spreadsheet_id, sel_date_iso, row_data)
            if ok:
                st.success(f"✅ {sel_date.strftime('%m/%d')} 진도 내용이 저장되었습니다.")
                st.cache_data.clear()
                st.rerun()
