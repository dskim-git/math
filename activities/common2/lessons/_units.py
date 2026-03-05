# activities/common2/lessons/_units.py
#
# 공통수학2 커리큘럼 정의 파일
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
#   {"type": "activity", "title": "제목", "subject": "common2", "slug": "..."}
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
                            {
                                "type": "canva",
                                "title": "다항식의 정리",
                                "src": "https://www.canva.com/design/DAHDEJoHCTU/X7qpJ4Y2F_fkfxUuqZyfXw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "다항식의 덧셈과 뺄셈",
                                "src": "https://www.canva.com/design/DAHDEHRkj2Q/JGbuWNdqt5iDUUdE3UHSsw/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "1-1-2",
                        "label": "다항식의 곱셈과 나눗셈",
                        "items": [
                            {
                                "type": "canva",
                                "title": "다항식의 곱셈",
                                "src": "https://www.canva.com/design/DAHDEK3KszI/OT-O0r2rMc4wlEG1nHOZ2g/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "다항식의 나눗셈",
                                "src": "https://www.canva.com/design/DAHDENEx56I/UnmJrokl7f2SUX0U6KY4xA/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "조립제법",
                                "src": "https://www.canva.com/design/DAHDEE2Z5ow/n7VqS7JZ12LjPOfOFGUkoQ/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "1-1-3",
                        "label": "중단원 점검하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "중단원 마무리 문제",
                                "src": "https://drive.google.com/file/d/1jRdV1GXgwqkhnpTWn0rllrpnLljMllRN/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=1jRdV1GXgwqkhnpTWn0rllrpnLljMllRN"
                            }
                        ],
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
    # 교육과정 외
    {
        "key": "X",
        "label": "교육과정 외",
        "children": [
            {"key": "X-1", "label": "중등 기하", "items": [
                {
                    "type": "canva",
                    "title": "삼각형의 합동과 닮음",
                    "src": "https://www.canva.com/design/DAHC5OxGYD4/Wz6XA9IJNE-WkVffPBElHg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "삼각형의 성질",
                    "src": "https://www.canva.com/design/DAHC5HyRFvA/U1SeoXLFac9VcVpT3D94Ig/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "삼각형의 무게중심, 외심, 내심",
                    "src": "https://www.canva.com/design/DAHC5P3F-nY/iivCAv3Yyomhh2B0MEQ5GA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "원의 성질",
                    "src": "https://www.canva.com/design/DAHC5HH_w_M/C-8ZtVtMTvGfOFr8dhWfgg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "사각형의 성질",
                    "src": "https://www.canva.com/design/DAHC5C632MI/dkfuH14cRqF-yQKv0A-XYA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "문제 풀이",
                    "src": "https://www.canva.com/design/DAHC5IfBCP0/b7zKPYtrtvixYB3lFk5o4g/view?embed",
                    "height": 800
                }
            ]},
        ],
    },
]
