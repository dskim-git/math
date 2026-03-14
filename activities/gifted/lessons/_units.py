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
            
        ],
    },
    {
        "key": "2",
        "label": "시어핀스키 삼각형과 카오스 게임",
        "items": [
            # 수업 자료를 여기에 추가하세요.
        ],
    },
    {
        "key": "3",
        "label": "사진과 그림을 활용한 시선에 대한 연구",
        "items": [
            # 수업 자료를 여기에 추가하세요.
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
