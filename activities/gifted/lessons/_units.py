# activities/gifted/lessons/_units.py
#
# 영재 수업 커리큘럼 정의 파일
# ─────────────────────────────────────────────────────────────────────────────
# CURRICULUM 구조:
#   수업 주제 (key: "1", "2", ...)  ← items 목록을 바로 가짐 (단층 구조)
#
# items 타입:
#   {"type": "canva",    "title": "제목", "src": "임베드 URL", "height": 800}
#   {"type": "gslides",  "title": "제목", "src": "임베드 URL", "height": 600}
#   {"type": "gsheet",   "title": "제목", "src": "임베드 URL", "height": 700}
#   {"type": "youtube",  "title": "제목", "src": "유튜브 URL", "height": 480}
#   {"type": "pdf",      "title": "제목", "src": "Drive preview URL", "download": "다운로드 URL"}
#   {"type": "url",      "title": "제목", "src": "https://..."}
#   {"type": "activity", "title": "제목", "subject": "gifted", "slug": "파일명"}
#   {"type": "iframe",   "title": "제목", "src": "https://...", "height": 800}
#
# ─────────────────────────────────────────────────────────────────────────────

CURRICULUM = [
    {
        "key": "1",
        "label": "기이한 소수의 세계",
        "items": [
            {
                "type": "canva",
                "title": "Intro",
                "src": "https://www.canva.com/design/DAHD5LMHQfo/Wbj346X7lGusCY5yVP4DQQ/view?embed",
                "height": 800
            },
            {
                "type": "canva",
                "title": "소수와 리만가설",
                "src": "https://www.canva.com/design/DAHD5LJD7BI/1AX4h8M2mF3ewTuVSdLzfQ/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 에라토스테네스의 체와 소수정리",
                "subject": "gifted",
                "slug": "sieve_eratosthenes",
            },
            {
                "type": "canva",
                "title": "산술함수와 곱셈함수",
                "src": "https://www.canva.com/design/DAHD5HOoNBw/tf71lw0Erw4t_FTcN9qK_Q/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 산술함수와 곱셈함수 탐구",
                "subject": "gifted",
                "slug": "multiplicative_functions",
            },
            {
                "type": "canva",
                "title": "제타함수",
                "src": "https://www.canva.com/design/DAHDhAAK3IQ/rYmEOCarMu7uZhfSz3fgww/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 리만 제타함수 탐험",
                "subject": "gifted",
                "slug": "zeta_explorer",
            },
            {
                "type": "canva",
                "title": "제타함수와 산술함수의 관계",
                "src": "https://www.canva.com/design/DAHD5CIkUFI/a35IjIcviQ5ArnAcsemrxQ/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 제타함수와 산술함수의 관계",
                "subject": "gifted",
                "slug": "zeta_arithmetic",
            },
        ],
    },
    {
        "key": "2",
        "label": "시어핀스키 삼각형과 카오스 게임",
        "items": [
            {
                "type": "canva",
                "title": "프랙털",
                "src": "https://www.canva.com/design/DAHD5HHqt2Y/AOPdrz4lXeVPmO3XuzPYhg/view?embed",
                "height": 800
            },
            {
                "type": "canva",
                "title": "카오스",
                "src": "https://www.canva.com/design/DAHD5FRQrWU/N54TY2k5dSGI5EO4V6VbLw/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 이중진자 시뮬레이션",
                "subject": "gifted",
                "slug": "double_pendulum",
            },
            {
                "type": "activity",
                "title": "미니: 나비효과 — 로렌츠의 기상 모델",
                "subject": "gifted",
                "slug": "lorenz_butterfly",
            },
            {
                "type": "activity",
                "title": "미니: 로렌츠 끌개 — 불규칙 속의 규칙성",
                "subject": "gifted",
                "slug": "lorenz_attractor",
            },
            {
                "type": "canva",
                "title": "다양한 프랙털 도형",
                "src": "https://www.canva.com/design/DAHD5JsqxbI/6dfNM09iN6uDmYC7IytVdg/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 프랙털 — 길이·넓이·부피와 차원 탐구",
                "subject": "gifted",
                "slug": "fractal_dimensions",
            },
            {
                "type": "canva",
                "title": "시에르핀스키 삼각형",
                "src": "https://www.canva.com/design/DAHD5IG1GG4/XR0RX4RCEMDknSfkDQTuOw/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 시에르핀스키 삼각형 — 단계별 분석",
                "subject": "gifted",
                "slug": "sierpinski_props",
            },
            {
                "type": "canva",
                "title": "파스칼의 삼각형의 비밀",
                "src": "https://www.canva.com/design/DAHD5CslE68/-sWcAMCzq2edQEi2xpjnDQ/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 갈톤보드 시뮬레이션",
                "subject": "gifted",
                "slug": "galton_board",
            },
            {
                "type": "activity",
                "title": "미니: 파스칼의 삼각형 성질 탐구",
                "subject": "gifted",
                "slug": "pascal_triangle_props",
            },
            {
                "type": "canva",
                "title": "카오스 게임",
                "src": "https://www.canva.com/design/DAHD5CdyCP8/aa1HvPgknv6BW6zdUwQnNw/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 카오스 게임으로 이해하는 시에르핀스키 삼각형",
                "subject": "gifted",
                "slug": "chaosgame_address",
            },
            {
                "type": "canva",
                "title": "인터넷 카오스 게임",
                "src": "https://www.canva.com/design/DAHD4zEWKHQ/FpmkwsTl-3d4Ezyw6ldBfQ/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 카오스 게임",
                "subject": "etc",
                "slug": "chaosgame",
            },
        ],
    },
    {
        "key": "3",
        "label": "사진과 그림을 활용한 시선에 대한 연구",
        "items": [
            {
                "type": "canva",
                "title": "원근법",
                "src": "https://www.canva.com/design/DAHD5AeS3rM/6s_eBGEgqif4Nt1_xzEycA/view?embed",
                "height": 800
            },
            {
                "type": "canva",
                "title": "소실점",
                "src": "https://www.canva.com/design/DAHD5PdSLCc/sxzTgo_NqG5pQL4sLgmmAg/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 소실점 찾기 — 직선 그리기 활동",
                "subject": "gifted",
                "slug": "vanishing_point_draw",
            },
            {
                "type": "canva",
                "title": "투시원근법에서의 거리 측정",
                "src": "https://www.canva.com/design/DAHD5JryAbM/SFA8M6MMJV7vUa4n0B0VhQ/view?embed",
                "height": 800
            },
            {
                "type": "activity",
                "title": "미니: 거리점과 화가까지의 실제 거리",
                "subject": "gifted",
                "slug": "measuring_point_distance",
            },
            {
                "type": "canva",
                "title": "그림 속 실제 사물과 그림 사이의 거리",
                "src": "https://www.canva.com/design/DAHD5DczdKk/R77ntzzhXDc18cht19ns7A/view?embed",
                "height": 800
            },
            {
                "type": "canva",
                "title": "등간격으로 나열된 사물의 화폭에서의 간격",
                "src": "https://www.canva.com/design/DAHD5EOnQ_w/101r0AgevDf4vJtBt5WBeQ/view?embed",
                "height": 800
            },
            {
                "type": "canva",
                "title": "성 삼위일체(마사초) 분석",
                "src": "https://www.canva.com/design/DAHD490esgo/XIZ5XR5G1LnzInU9ysyhqw/view?embed",
                "height": 800
            },
        ],
    },
    {
        "key": "4",
        "label": "작도 게임",
        "items": [
            # 수업 자료를 여기에 추가하세요.
        ],
    },
]
