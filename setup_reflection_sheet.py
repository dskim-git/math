import gspread
from google.oauth2.service_account import Credentials
import tomllib

# secrets 로드
with open('.streamlit/secrets.toml', 'rb') as f:
    secrets = tomllib.load(f)

# GCP 인증
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

creds_dict = secrets['gcp_service_account']
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)


def ensure_sheet(sh, sheet_name, headers):
    """시트가 없으면 생성하고 헤더를 설정합니다."""
    try:
        ws = sh.worksheet(sheet_name)
        first_row = ws.row_values(1)
        print(f'[OK] "{sheet_name}" 시트 이미 존재 / 헤더: {first_row}')
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=sheet_name, rows=10000, cols=len(headers) + 2)
        ws.append_row(headers)
        print(f'[NEW] "{sheet_name}" 시트 생성 완료 / 헤더: {headers}')
    return ws


# ── 공통수학 스프레드시트 ────────────────────────────────────────────────────
sh_common = client.open_by_key(secrets['reflection_spreadsheet_common'])
print('=== 공통수학 ===')

ensure_sheet(sh_common, '조합등식탐구', [
    'timestamp', '학번', '이름',
    'eq1_insight', 'eq2_insight', 'eq3_insight', 'eq4_insight',
    '새롭게알게된점', '느낀점',
])

ensure_sheet(sh_common, '지도색칠경우의수', [
    'timestamp', '학번', '이름',
    '색칠방법수', '색최솟값', '4색정리연결', '조건영향',
    '새롭게알게된점', '느낀점',
])

# ── 확률과통계 스프레드시트 ────────────────────────────────────────────────
sh_prob = client.open_by_key(secrets['reflection_spreadsheet_probability_new'])
print('=== 확률과통계 ===')

ensure_sheet(sh_prob, '독립시행실생활', [
    'timestamp', '학번', '이름',
    '독립시행이유', '공식분해', '나만의예시',
    '새롭게알게된점', '느낀점',
])

ensure_sheet(sh_prob, '솔직한설문의비밀', [
    'timestamp', '학번', '이름',
    '독립시행이유', '조사자모름이유', '확률계산', '한계와개선',
    '새롭게알게된점', '느낀점',
])

print('\n✅ 성찰 기록 시트 준비 완료!')
