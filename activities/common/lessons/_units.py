# activities/common/lessons/_units.py
#
# 공통수학 커리큘럼 정의 파일
# ─────────────────────────────────────────────────────────────────────────────
# CURRICULUM 구조:
#   대단원 (key: "1", "2", ...)
#     └ 중단원 (key: "1-1", "1-2", ...)
#         └ 소단원 (key: "1-1-1", ...) ← items 목록을 가짐
#
# items 타입:
#   {"type": "canva",    "title": "제목", "src": "임베드 URL", "height": 800}
#   {"type": "gslides",  "title": "제목", "src": "임베드 URL", "height": 600}
#   {"type": "gsheet",   "title": "제목", "src": "임베드 URL", "height": 700}
#   {"type": "youtube",  "title": "제목", "src": "유튜브 URL", "height": 480}
#   {"type": "url",      "title": "제목", "src": "https://..."}
#   {"type": "activity", "title": "제목", "subject": "common", "slug": "intro_numbers"}
#
# 대/중/소 단원명과 실제 수업 자료(items)는 아래에서 직접 수정하세요.
# ─────────────────────────────────────────────────────────────────────────────

CURRICULUM = [
    {
        "key": "1",
        "label": "[1] 다항식",
        "children": [
            {
                "key": "1-1",
                "label": "(1) 다항식의 연산",
                "children": [
                    {
                        "key": "1-1-1",
                        "label": "다항식의 덧셈과 뺄셈",
                        "items": [
                            # 예시 — 실제 자료로 교체하세요
                            # {
                            #     "type": "canva",
                            #     "title": "다항식의 덧셈과 뺄셈",
                            #     "src": "https://www.canva.com/design/...",
                            #     "height": 800
                            # },
                        ],
                    },
                    {
                        "key": "1-1-2",
                        "label": "다항식의 곱셈",
                        "items": [],
                    },
                    {
                        "key": "1-1-3",
                        "label": "다항식의 나눗셈",
                        "items": [],
                    },
                ],
            },
            {
                "key": "1-2",
                "label": "(2) 나머지정리",
                "children": [
                    {
                        "key": "1-2-1",
                        "label": "나머지정리",
                        "items": [],
                    },
                    {
                        "key": "1-2-2",
                        "label": "인수정리",
                        "items": [],
                    },
                ],
            },
            {
                "key": "1-3",
                "label": "(3) 인수분해",
                "children": [
                    {
                        "key": "1-3-1",
                        "label": "인수분해",
                        "items": [],
                    },
                ],
            },
        ],
    },
    {
        "key": "2",
        "label": "[2] 방정식과 부등식",
        "children": [
            {
                "key": "2-1",
                "label": "(1) 복소수와 이차방정식",
                "children": [
                    {
                        "key": "2-1-1",
                        "label": "복소수",
                        "items": [],
                    },
                    {
                        "key": "2-1-2",
                        "label": "이차방정식",
                        "items": [],
                    },
                    {
                        "key": "2-1-3",
                        "label": "이차방정식과 이차함수의 관계",
                        "items": [],
                    },
                ],
            },
            {
                "key": "2-2",
                "label": "(2) 이차방정식과 이차부등식",
                "children": [
                    {
                        "key": "2-2-1",
                        "label": "이차방정식의 근과 계수의 관계",
                        "items": [],
                    },
                    {
                        "key": "2-2-2",
                        "label": "이차부등식",
                        "items": [],
                    },
                ],
            },
        ],
    },
    {
        "key": "3",
        "label": "[3] 경우의 수",
        "children": [
            {
                "key": "3-1",
                "label": "(1) 경우의 수",
                "children": [
                    {
                        "key": "3-1-1",
                        "label": "합의 법칙과 곱의 법칙",
                        "items": [],
                    },
                    {
                        "key": "3-1-2",
                        "label": "순열",
                        "items": [],
                    },
                    {
                        "key": "3-1-3",
                        "label": "조합",
                        "items": [],
                    },
                ],
            },
        ],
    },
]
