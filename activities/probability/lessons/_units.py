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
          {"key": "1-1-1", "label": "원순열", "items": [
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
          {"key": "1-1-2", "label": "중복순열", "items": [
                {
                    "type": "canva",
                    "title": "중복순열",
                    "src": "https://www.canva.com/design/DAGNl8s3A0s/Nbs_N2gbTcqYSpIrfu6cBQ/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-1-3", "label": "같은 것이 있는 순열", "items": [
                {
                    "type": "canva",
                    "title": "같은 것이 있는 순열",
                    "src": "https://www.canva.com/design/DAGNl2vhKYA/ObtbLokxlZBoJgazUpFQYg/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-1-4", "label": "중복조합", "items": [
                {
                    "type": "canva",
                    "title": "중복조합",
                    "src": "https://www.canva.com/design/DAGNly2hs8o/pnOkCbXhNC0Ca0L-2hIObg/view?embed",
                    "height": 800
                }
            ]},
        ],
      },
      {
        "key": "1-2",
        "label": "(2) 이항정리",
        "children": [
          {"key": "1-2-1", "label": "이항정리", "items": [
                {
                    "type": "canva",
                    "title": "이항정리",
                    "src": "https://www.canva.com/design/DAGNl1q_da0/TXTFw1qR_ph2kjpXxzdivQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "파스칼의 삼각형",
                    "src": "https://www.canva.com/design/DAGNlypGJuM/dZGjjww0s4Ix0bH_wUY5nQ/view?embed",
                    "height": 800
                },
                {
                    "type": "gsheet",
                    "title": "엑셀로 만든 파스칼의 삼각형",
                    "src": "https://docs.google.com/spreadsheets/d/17F8RhpLp8XNhiOICfUlxnFFjDEQCCjLVAQyUADkUjz8/edit?usp=drivesdk",
                    "height": 800
                }
                # 필요하면 여기에 추가 자료를 이어서 넣으면 됩니다.
                # {"type":"activity","title":"활동 예시","subject":"probability","slug":"binomial_simulator"},
                # {"type":"url","title":"보충 설명","src":"https://..."},
            ]},
          {"key": "1-2-2", "label": "이항정리의 활용", "items": [
                {
                    "type": "canva",
                    "title": "이항정리의 활용",
                    "src": "https://www.canva.com/design/DAGNl0IVvy0/Sk5roP86VF-FxyTI3pZ6HQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이항계수의 성질",
                    "src": "https://www.canva.com/design/DAGNl45UHuA/G9hddVZMCJM13F43M7hZYw/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "파스칼의 삼각형에서 찾아보는 프랙털",
                    "subject": "probability",
                    "slug": "pascal_modulo_view"
                }
            ]},
        ],
      },
      {
        "key": "1-3",
        "label": "(3) 대단원 문제",
        # 소단원 없이 이 레벨에서 바로 items를 둘 수도 있습니다.
        "items": [
                {
                    "type": "pdf",
                    "title": "단원평가문제",
                    "src": "https://drive.google.com/file/d/1P6TGjB_BKCNZRSts-aE-sPG7L7pyyZZW/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1P6TGjB_BKCNZRSts-aE-sPG7L7pyyZZW"  # (선택) 다운로드 버튼 표시용
                }
        ],
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
          {"key": "2-1-1", "label": "확률의 뜻", "items": [
                {
                    "type": "canva",
                    "title": "시행과 사건",
                    "src": "https://www.canva.com/design/DAGNl7Kpmdc/qH9Yd9_aa6jpJsh0TcVY2A/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "수학적 확률",
                    "src": "https://www.canva.com/design/DAGNl1df9hA/vZkiHQlTQrGwOUnAtdxe1Q/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "통계적 확률",
                    "src": "https://www.canva.com/design/DAGNl3VnqaM/rJz9C3d1irXdI7fap2Mzjg/view?embed",
                    "height": 800
                },
                {
                    "type": "gsheet",
                    "title": "수학적 확률과 통계적 확률의 관계",
                    "src": "https://docs.google.com/spreadsheets/d/1oz2DHhzrRxRFRn92RcGZdupPGvXUzWTk/edit?usp=drivesdk",
                    "height": 800
                },
                {
                    "type": "iframe",
                    "title": "수학적 확률과 통계적 확률의 관계 (통그라미)",
                    "src": "https://tong.kostat.go.kr/tongramy_web/main.do?menuSn=163#",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "뷔퐁의 바늘 실험",
                    "subject": "probability",
                    "slug": "buffon_needle_p5"
                },
                {
                    "type": "iframe",
                    "title": "뷔퐁의 바늘 실험(일리노이대)",
                    "src": "https://mste.illinois.edu/activity/buffon/",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "베르트랑의 역설",
                    "subject": "probability",
                    "slug": "bertrand_paradox_p5"
                }
          ]},
          {"key": "2-1-2", "label": "확률의 기본 성질", "items": [
                {
                    "type": "canva",
                    "title": "확률의 기본 성질",
                    "src": "https://www.canva.com/design/DAGNl4QjJQk/In6tmF5d2maLToc3tJkPwQ/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "몬티홀 문제",
                    "subject": "probability",
                    "slug": "monty_hall_p5"
                },
                {
                    "type": "activity",
                    "title": "몬티홀 문제(확장)",
                    "subject": "probability",
                    "slug": "monty_hall_extended_p5"
                }
          ]},
          {"key": "2-1-3", "label": "확률의 덧셈정리", "items": [
                {
                    "type": "canva",
                    "title": "배반사건",
                    "src": "https://www.canva.com/design/DAGNl4WLA34/0B49FEc9BXaV-f033EiDrA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "확률의 덧셈정리",
                    "src": "https://www.canva.com/design/DAGNl4dXCFU/wU2f46tNJIQxIAkx6WH_sw/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-1-4", "label": "여사건의 확률", "items": [
                {
                    "type": "canva",
                    "title": "여사건",
                    "src": "https://www.canva.com/design/DAGNlwRyb0Q/uFGi82VwEUHsPNn50t5RPg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "여사건의 확률",
                    "src": "https://www.canva.com/design/DAGNlwT2t6Y/8nByHtuP-3HKQ_4WkCsN4A/view?embed",
                    "height": 800
                },
                {
                    "type": "image",
                    "title": "생일 예시",
                    "src": "assets/birth.png",
                    "width":640,
                    "caption": "생일"
                },
          ]},
        ],
      },
      {
        "key": "2-2",
        "label": "(2) 조건부확률",
        "children": [
          {"key": "2-2-1", "label": "1. 조건부확률", "items": [
                {
                    "type": "canva",
                    "title": "조건부확률",
                    "src": "https://www.canva.com/design/DAGNl-3fzAo/dG6Ih5DHeLzB3_-3yFkWmw/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 홀수일 때 소수일 확률 (한 번 실행)",
                    "subject": "probability",
                    "slug": "mini/odd_prime_conditional",   # 👈 파일명
                }
          ]},
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




#<이미지 넣는 법>
# 1) 픽셀 고정
#{"type":"image", "title":"도형 예", "src":"assets/geom/a.png", "width":640, "caption":"정다각형"}

# 2) 여러 장을 한 줄에 3칸
#{"type":"image", "title":"예제 모음", "srcs":["a.png","b.png","c.png"], "cols":3}

# 3) 반응형(열 폭 가득)
#{"type":"image", "title":"반응형", "src":"assets/foo.png"}  # use_container_width=True가 기본
