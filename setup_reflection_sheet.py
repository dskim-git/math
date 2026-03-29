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

# 확률과통계 스프레드시트 열기
spreadsheet_id = secrets['reflection_spreadsheet_probability_new']
sh = client.open_by_key(spreadsheet_id)

# 시트명
sheet_name = '통계적확률실험실'

# 기존 시트 확인
try:
    ws = sh.worksheet(sheet_name)
    print(f'✓ "{sheet_name}" 시트가 이미 존재합니다')
    # 헤더 확인
    first_row = ws.row_values(1)
    print(f'현재 헤더: {first_row}')
except gspread.exceptions.WorksheetNotFound:
    # 새 시트 생성
    ws = sh.add_worksheet(title=sheet_name, rows=10000, cols=12)
    print(f'✓ "{sheet_name}" 시트를 생성했습니다')
    
    # 헤더 설정
    headers = ['timestamp', '학번', '이름', '수학적확률비교', '수렴과정', '대수의법칙', '통계적확률의미', '흥미로운시행', '새롭게알게된점', '느낀점']
    ws.append_row(headers)
    print(f'✓ 헤더가 생성되었습니다: {headers}')

print('\n✅ 성찰 기록 시트 준비 완료!')

# ── 뷔퐁의 바늘 미니 시트 ──
sheet_name2 = '뷔퐁의바늘미니'
try:
    ws2 = sh.worksheet(sheet_name2)
    print(f'✓ "{sheet_name2}" 시트가 이미 존재합니다')
    first_row2 = ws2.row_values(1)
    print(f'현재 헤더: {first_row2}')
except gspread.exceptions.WorksheetNotFound:
    ws2 = sh.add_worksheet(title=sheet_name2, rows=10000, cols=12)
    print(f'✓ "{sheet_name2}" 시트를 생성했습니다')
    headers2 = ['timestamp', '학번', '이름', '공식이해', '수렴관찰', '바늘길이탐구', '통계적확률연결', 'pi추정의의', '새롭게알게된점', '느낀점']
    ws2.append_row(headers2)
    print(f'✓ 헤더가 생성되었습니다: {headers2}')

print('\n✅ 뷔퐁의 바늘 미니 시트 준비 완료!')
