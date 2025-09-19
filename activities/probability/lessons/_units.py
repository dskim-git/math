# activities/probability/lessons/_units.py

# 계층형 커리큘럼(순서 보장용으로 list 사용)
CURRICULUM = [
  {
    "key": "1",
    "label": "[1] 경우의 수",
    "children": [
      {
        "key": "1-1",
        "label": "(1) 순열과 조합",
        "children": [
          {"key": "1-1-1",
           "label": "1. 원순열",
           "items": [
                {
                    "type": "canva",
                    "title": "원순열",
                    "src": "https://www.canva.com/design/DAGNlyGJNp8/56f2EaBXpwemyaLtixXk8A/view?embed",
                    "height": 800
                },
                # 필요하면 여기에 추가 자료를 이어서 넣으면 됩니다.
                # {"type":"activity","title":"활동 예시","subject":"probability","slug":"binomial_simulator"},
                # {"type":"url","title":"보충 설명","src":"https://..."},
            ]},
          {"key": "1-1-2", "label": "2. 중복순열", "items": []},
          {"key": "1-1-3", "label": "3. 같은 것이 있는 순열", "items": []},
          {"key": "1-1-4", "label": "4. 중복조합", "items": []},
        ],
      },
      {
        "key": "1-2",
        "label": "(2) 이항정리",
        "children": [
          {"key": "1-2-1", "label": "1. 이항정리", "items": []},
          {"key": "1-2-2", "label": "2. 이항정리의 활용", "items": []},
        ],
      },
      {
        "key": "1-3",
        "label": "(3) 대단원 문제",
        # 소단원 없이 이 레벨에서 바로 items를 둘 수도 있습니다.
        "items": [],
      },
    ],
  },

  {
    "key": "2",
    "label": "[2] 확률",
    "children": [
      {
        "key": "2-1",
        "label": "(1) 확률의 뜻과 활용",
        "children": [
          {"key": "2-1-1", "label": "1. 확률의 뜻", "items": []},
          {"key": "2-1-2", "label": "2. 확률의 기본 성질", "items": []},
          {"key": "2-1-3", "label": "3. 확률의 덧셈정리", "items": []},
          {"key": "2-1-4", "label": "4. 여사건의 확률", "items": []},
        ],
      },
      {
        "key": "2-2",
        "label": "(2) 조건부확률",
        "children": [
          {"key": "2-2-1", "label": "1. 조건부확률", "items": []},
          {"key": "2-2-2", "label": "2. 확률의 곱셈정리", "items": []},
          {"key": "2-2-3", "label": "3. 사건의 독립과 종속", "items": []},
          {"key": "2-2-4", "label": "4. 독립시행의 확률", "items": []},
        ],
      },
      {
        "key": "2-3",
        "label": "(3) 대단원 문제",
        "items": [],
      },
    ],
  },

  {
    "key": "3",
    "label": "[3] 통계",
    "children": [
      {
        "key": "3-1",
        "label": "(1) 확률분포",
        "children": [
          {"key": "3-1-1", "label": "1. 확률변수와 확률분포", "items": []},
          {"key": "3-1-2", "label": "2. 이산확률변수의 기댓값과 표준편차", "items": []},
          {"key": "3-1-3", "label": "3. 이산확률변수 aX+b의 평균, 분산, 표준편차", "items": []},
          {"key": "3-1-4", "label": "4. 이항분포", "items": []},
          {"key": "3-1-5", "label": "5. 정규분포", "items": []},
          {"key": "3-1-6", "label": "6. 이항분포와 정규분포의 관계", "items": []},
        ],
      },
      {
        "key": "3-2",
        "label": "(2) 통계적 추정",
        "children": [
          {"key": "3-2-1", "label": "1. 모집단과 표본", "items": []},
          {"key": "3-2-2", "label": "2. 모평균의 추정", "items": []},
        ],
      },
      {
        "key": "3-3",
        "label": "(3) 대단원 문제",
        "items": [],
      },
    ],
  },

  # 교육과정 외
  {
    "key": "X",
    "label": "교육과정 외",
    "children": [
      {"key": "X-1", "label": "분할", "items": []},
      {"key": "X-2", "label": "모비율의 추정", "items": []},
    ],
  },
]

# (선택) 기존 단일 레벨 UNITS도 함께 둘 수 있습니다. 있으면 lessons_view가 자동 인식하여 사용.
UNITS = {
    # "freepack": {"label": "예시 단원", "items": [ ... ]},
}
