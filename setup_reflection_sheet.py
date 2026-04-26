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
sheet_name = '독립과배반탐구'

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
    headers = ['timestamp', '학번', '이름', '배반vs독립', '혼동이유', '독립4쌍', '비추이성', '새롭게알게된점', '느낀점']
    ws.append_row(headers)
    print(f'✓ 헤더가 생성되었습니다: {headers}')

print('\n✅ 성찰 기록 시트 준비 완료!')
