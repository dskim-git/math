import gspread
import os
os.chdir('c:/git-math/math')

# streamlit secrets.toml 파일 읽기
try:
    import toml
    with open('.streamlit/secrets.toml', 'r', encoding='utf-8') as f:
        secrets = toml.load(f)
except:
    print("toml 라이브러리 필요. pip install toml 실행 후 다시 시도")
    exit(1)

# 서비스 계정 인증
creds_info = secrets['gcp_service_account']
sa = gspread.service_account_from_dict(creds_info)

# 확률과통계 스프레드시트 열기
sheet_id = secrets['reflection_spreadsheet_probability_new']
sh = sa.open_by_key(sheet_id)

print("\n=== 모비율의 추정 3개 시트 헤더 검증 ===\n")

# 3개 시트의 헤더 검증
for sheet_name in ['표본비율분포시뮬', '모비율신뢰구간챌린지', '모비율신뢰구간_뉴스해석']:
    try:
        ws = sh.worksheet(sheet_name)
        headers = ws.row_values(1)
        print(f"✓ {sheet_name}")
        print(f"  헤더 ({len(headers)}개): {headers}")
        print()
    except Exception as e:
        print(f"✗ {sheet_name}: {e}\n")

print("✅ 모비율의 추정 단원 성찰 시트 준비 완료!")
