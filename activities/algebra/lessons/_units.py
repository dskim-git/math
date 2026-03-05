# activities/algebra/lessons/_units.py
#
# 대수 커리큘럼 정의 파일 (2022 개정 교육과정)
# ─────────────────────────────────────────────────────────────────────────────

CURRICULUM = [
    {
        "key": "1",
        "label": "[1] 지수와 로그",
        "children": [
            {
                "key": "1-1",
                "label": "(1) 지수",
                "children": [
                    {"key": "1-1-1", "label": "거듭제곱과 거듭제곱근", "items": []},
                    {"key": "1-1-2", "label": "지수의 확장", "items": []},
                    {"key": "1-1-3", "label": "지수함수", "items": []},
                    {"key": "1-1-4", "label": "지수방정식과 지수부등식", "items": []},
                ],
            },
            {
                "key": "1-2",
                "label": "(2) 로그",
                "children": [
                    {"key": "1-2-1", "label": "로그", "items": []},
                    {"key": "1-2-2", "label": "상용로그", "items": []},
                    {"key": "1-2-3", "label": "로그함수", "items": []},
                    {"key": "1-2-4", "label": "로그방정식과 로그부등식", "items": []},
                ],
            },
        ],
    },
    {
        "key": "2",
        "label": "[2] 수열",
        "children": [
            {
                "key": "2-1",
                "label": "(1) 등차수열과 등비수열",
                "children": [
                    {"key": "2-1-1", "label": "수열", "items": []},
                    {"key": "2-1-2", "label": "등차수열", "items": []},
                    {"key": "2-1-3", "label": "등비수열", "items": []},
                ],
            },
            {
                "key": "2-2",
                "label": "(2) 수열의 합",
                "children": [
                    {"key": "2-2-1", "label": "합의 기호 Σ", "items": []},
                    {"key": "2-2-2", "label": "여러 가지 수열의 합", "items": []},
                    {"key": "2-2-3", "label": "점화식", "items": []},
                ],
            },
            {
                "key": "2-3",
                "label": "(3) 수학적 귀납법",
                "children": [
                    {"key": "2-3-1", "label": "수학적 귀납법", "items": []},
                ],
            },
        ],
    },
]
