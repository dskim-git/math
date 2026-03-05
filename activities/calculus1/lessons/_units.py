# activities/calculus1/lessons/_units.py
#
# 미적분1 커리큘럼 정의 파일 (2022 개정 교육과정)
# ─────────────────────────────────────────────────────────────────────────────

CURRICULUM = [
    {
        "key": "1",
        "label": "[1] 함수의 극한과 연속",
        "children": [
            {
                "key": "1-1",
                "label": "(1) 함수의 극한",
                "children": [
                    {"key": "1-1-1", "label": "함수의 극한", "items": []},
                    {"key": "1-1-2", "label": "함수의 극한에 대한 성질", "items": []},
                    {"key": "1-1-3", "label": "미정계수의 결정", "items": []},
                ],
            },
            {
                "key": "1-2",
                "label": "(2) 함수의 연속",
                "children": [
                    {"key": "1-2-1", "label": "함수의 연속", "items": []},
                    {"key": "1-2-2", "label": "연속함수의 성질", "items": []},
                ],
            },
        ],
    },
    {
        "key": "2",
        "label": "[2] 다항함수의 미분",
        "children": [
            {
                "key": "2-1",
                "label": "(1) 미분계수와 도함수",
                "children": [
                    {"key": "2-1-1", "label": "미분계수", "items": []},
                    {"key": "2-1-2", "label": "도함수", "items": []},
                    {"key": "2-1-3", "label": "도함수의 계산", "items": []},
                ],
            },
            {
                "key": "2-2",
                "label": "(2) 도함수의 활용",
                "children": [
                    {"key": "2-2-1", "label": "접선의 방정식", "items": []},
                    {"key": "2-2-2", "label": "함수의 증가와 감소, 극값", "items": []},
                    {"key": "2-2-3", "label": "함수의 최댓값과 최솟값", "items": []},
                    {"key": "2-2-4", "label": "방정식과 부등식에의 활용", "items": []},
                    {"key": "2-2-5", "label": "속도와 가속도", "items": []},
                ],
            },
        ],
    },
    {
        "key": "3",
        "label": "[3] 다항함수의 적분",
        "children": [
            {
                "key": "3-1",
                "label": "(1) 부정적분",
                "children": [
                    {"key": "3-1-1", "label": "부정적분", "items": []},
                    {"key": "3-1-2", "label": "부정적분의 계산", "items": []},
                ],
            },
            {
                "key": "3-2",
                "label": "(2) 정적분",
                "children": [
                    {"key": "3-2-1", "label": "정적분", "items": []},
                    {"key": "3-2-2", "label": "정적분의 계산", "items": []},
                    {"key": "3-2-3", "label": "정적분으로 정의된 함수", "items": []},
                ],
            },
            {
                "key": "3-3",
                "label": "(3) 정적분의 활용",
                "children": [
                    {"key": "3-3-1", "label": "넓이", "items": []},
                    {"key": "3-3-2", "label": "속도와 거리", "items": []},
                ],
            },
        ],
    },
]
