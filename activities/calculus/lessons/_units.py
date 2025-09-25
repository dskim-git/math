# activities/probability/lessons/_units.py

# 계층형 커리큘럼(순서 보장용으로 list 사용)
CURRICULUM = [
  {
    "key": "1",
    "label": "[1] 수열의 극한",
    "children": [
      {
        "key": "1-1",
        "label": "(1) 수열의 극한",
        "children": [
          {"key": "1-1-1", "label": "수열의 극한", "items": [
                {
                    "type": "canva",
                    "title": "원순열",
                    "src": "https://www.canva.com/design/DAGNlyGJNp8/56f2EaBXpwemyaLtixXk8A/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "원순열 이해하기", 
                    "subject": "probability",
                    "slug": "mini/circular_perm_anchor_p5",
                }
            ]},
          {"key": "1-1-2", "label": "수열의 극한값의 계산", "items": [
                {
                    "type": "canva",
                    "title": "중복순열",
                    "src": "https://www.canva.com/design/DAGNl8s3A0s/Nbs_N2gbTcqYSpIrfu6cBQ/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-1-3", "label": "등비수열의 극한", "items": [
                {
                    "type": "canva",
                    "title": "같은 것이 있는 순열",
                    "src": "https://www.canva.com/design/DAGNl2vhKYA/ObtbLokxlZBoJgazUpFQYg/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-1-4", "label": "중단원 마무리하기", "items": [
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
        "label": "(2) 급수",
        "children": [
          {"key": "1-2-1", "label": "급수", "items": [
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
          {"key": "1-2-2", "label": "등비급수", "items": [
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
          {"key": "1-2-3", "label": "등비급수의 활용", "items": [
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
          {"key": "1-2-4", "label": "중단원 마무리하기", "items": [
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
            ]}
        ],
      },
      {
        "key": "1-3",
        "label": "(3) 대단원 평가하기",
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
    "label": "[2] 미분법",
    "children": [
      {
        "key": "2-1",
        "label": "(1) 여러 가지 함수의 미분",
        "children": [
          {"key": "2-1-1", "label": "지수함수와 로그함수의 극한", "items": [
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
                    "title": "미니: 주사위 실험(애니메이션)", 
                    "subject": "probability",
                    "slug": "mini/dice_lab",
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
          {"key": "2-1-2", "label": "지수함수와 로그함수의 미분", "items": [
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
          {"key": "2-1-3", "label": "삼각함수의 덧셈정리", "items": [
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
          {"key": "2-1-4", "label": "삼각함수의 극한", "items": [
                {
                    "type": "canva",
                    "title": "여사건",
                    "src": "https://www.canva.com/design/DAGNlwRyb0Q/uFGi82VwEUHsPNn50t5RPg/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-1-5", "label": "삼각함수의 미분", "items": [
                {
                    "type": "canva",
                    "title": "여사건",
                    "src": "https://www.canva.com/design/DAGNlwRyb0Q/uFGi82VwEUHsPNn50t5RPg/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-1-6", "label": "중단원 마무리하기", "items": [
                {
                    "type": "canva",
                    "title": "여사건",
                    "src": "https://www.canva.com/design/DAGNlwRyb0Q/uFGi82VwEUHsPNn50t5RPg/view?embed",
                    "height": 800
                }
          ]}
        ],
      },
      {
        "key": "2-2",
        "label": "(2) 여러 가지 미분법",
        "children": [
          {"key": "2-2-1", "label": "함수의 몫의 미분법", "items": [
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
                },
                {
                    "type": "activity",
                    "title": "미니: 확률 수렴 관찰(10,100,1,000...)", 
                    "subject": "probability",
                    "slug": "mini/odd_prime_convergence",
                }
          ]},
          {"key": "2-2-2", "label": "합성함수의 미분법", "items": [
                {
                    "type": "canva",
                    "title": "확률의 곱셈정리",
                    "src": "https://www.canva.com/design/DAGNlxAwu88/yD-UCHkAqRJGp1wInKifRA/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "신기한 주사위", 
                    "subject": "probability",
                    "slug": "mini/nontransitive_dice_lab",
                }
          ]},
          {"key": "2-2-3", "label": "매개변수로 나타낸 함수의 미분법", "items": [
                {
                    "type": "canva",
                    "title": "사건의 독립과 종속",
                    "src": "https://www.canva.com/design/DAGNlxAwu88/yD-UCHkAqRJGp1wInKifRA/view?embed",
                    "height": 800
                },
                {
                    "type": "youtube",
                    "title": "상금 분배 문제",
                    "src": "https://youtu.be/InAIZ3tP_Mk?si=pQoxDuxJBC1AsC3b&start=535",
                    "height": 800
                }
          ]},
          {"key": "2-2-4", "label": "음함수와 역함수의 미분법", "items": [
                {
                    "type": "canva",
                    "title": "독립시행",
                    "src": "https://www.canva.com/design/DAGNl8UMPCw/ksQ3KQ4X1iM2Oqkeaph6AA/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-2-5", "label": "이계도함수", "items": [
                {
                    "type": "canva",
                    "title": "독립시행",
                    "src": "https://www.canva.com/design/DAGNl8UMPCw/ksQ3KQ4X1iM2Oqkeaph6AA/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-2-6", "label": "중단원 마무리하기", "items": [
                {
                    "type": "canva",
                    "title": "독립시행",
                    "src": "https://www.canva.com/design/DAGNl8UMPCw/ksQ3KQ4X1iM2Oqkeaph6AA/view?embed",
                    "height": 800
                }
          ]}
        ],
      },
      {
        "key": "2-3",
        "label": "(3) 도함수의 활용",
        "children": [
          {"key": "2-3-1", "label": "접선의 방정식", "items": [
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
                },
                {
                    "type": "activity",
                    "title": "미니: 확률 수렴 관찰(10,100,1,000...)", 
                    "subject": "probability",
                    "slug": "mini/odd_prime_convergence",
                }
          ]},
          {"key": "2-3-2", "label": "함수의 그래프", "items": [
                {
                    "type": "canva",
                    "title": "확률의 곱셈정리",
                    "src": "https://www.canva.com/design/DAGNlxAwu88/yD-UCHkAqRJGp1wInKifRA/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "신기한 주사위", 
                    "subject": "probability",
                    "slug": "mini/nontransitive_dice_lab",
                }
          ]},
          {"key": "2-3-3", "label": "방정식과 부등식에의 활용", "items": [
                {
                    "type": "canva",
                    "title": "사건의 독립과 종속",
                    "src": "https://www.canva.com/design/DAGNlxAwu88/yD-UCHkAqRJGp1wInKifRA/view?embed",
                    "height": 800
                },
                {
                    "type": "youtube",
                    "title": "상금 분배 문제",
                    "src": "https://youtu.be/InAIZ3tP_Mk?si=pQoxDuxJBC1AsC3b&start=535",
                    "height": 800
                }
          ]},
          {"key": "2-3-4", "label": "속도와 가속도", "items": [
                {
                    "type": "canva",
                    "title": "독립시행",
                    "src": "https://www.canva.com/design/DAGNl8UMPCw/ksQ3KQ4X1iM2Oqkeaph6AA/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-3-5", "label": "중단원 마무리하기", "items": [
                {
                    "type": "canva",
                    "title": "독립시행",
                    "src": "https://www.canva.com/design/DAGNl8UMPCw/ksQ3KQ4X1iM2Oqkeaph6AA/view?embed",
                    "height": 800
                }
          ]}
        ],
      }
      {
        "key": "2-4",
        "label": "(3) 대단원 문제",
        "items": [
                {
                    "type": "pdf",
                    "title": "단원평가문제",
                    "src": "https://drive.google.com/file/d/1viXzZ3ETiz7kdmHfyLk91Lhfu-1HBUYu/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1viXzZ3ETiz7kdmHfyLk91Lhfu-1HBUYu"  # (선택) 다운로드 버튼 표시용
                }
        ],
      },
    ],
  },

  {
    "key": "3",
    "label": "[3] 적분법",
    "children": [
      {
        "key": "3-1",
        "label": "(1) 여러 가지 적분법",
        "children": [
          {"key": "3-1-1", "label": "여러 가지 함수의 적분", "items": [
                {
                    "type": "canva",
                    "title": "확률변수",
                    "src": "https://www.canva.com/design/DAGPlXhzlhY/SxhvEidQ8E8E2NcPxBSXDw/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이산확률변수와 확률질량함수",
                    "src": "https://www.canva.com/design/DAGPlRs_7yA/CEbhOvfHuo8JL5PnKtbUiQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "연속확률변수와 확률밀도함수",
                    "src": "https://www.canva.com/design/DAGPlflvccI/Ita2MhE6WA61T6wbNILfsA/view?embed",
                    "height": 800
                }
          ]},
          {"key": "3-1-2", "label": "치환적분법", "items": [
                {
                    "type": "canva",
                    "title": "이산확률변수의 기댓값과 표준편차",
                    "src": "https://www.canva.com/design/DAGPlVNYwTY/jVyt833FOWh8vvOxJpdNmg/view?embed",
                    "height": 800
                }
          ]},
          {"key": "3-1-3", "label": "부분적분법", "items": [
                {
                    "type": "canva",
                    "title": "이산확률변수 aX+b의 평균과 표준편차",
                    "src": "https://www.canva.com/design/DAGPlSwzIeE/R_uZ69JnP1om6lBeE5UijA/view?embed",
                    "height": 800
                },
                {
                    "type": "iframe",
                    "title": "확률변수 aX+b의 평균과 표준편차 확인 (통그라미)",
                    "src": "https://tong.kostat.go.kr/tongramy_web/main.do?menuSn=163#",
                    "height": 800
                }
          ]},
          {"key": "3-1-4", "label": "중단원 마무리하기", "items": [
                {
                    "type": "canva",
                    "title": "이항분포",
                    "src": "https://www.canva.com/design/DAGPla1Cvro/HtiMM_RVFELx46wGvk76iw/view?embed",
                    "height": 800
                }
          ]}
        ],
      },
      {
        "key": "3-2",
        "label": "(2) 정적분의 활용",
        "children": [
          {"key": "3-2-1", "label": "정적분과 급수의 합 사이의 관계", "items": [
                {
                    "type": "canva",
                    "title": "모집단과 표본",
                    "src": "https://www.canva.com/design/DAGS9opzh4Y/uefQkrReWXgNcqXPqPmD9g/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "표본추출",
                    "src": "https://www.canva.com/design/DAGS9xLh_3g/BXrxqAs_K6enUC7eEfXEeg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "모평균과 표본평균",
                    "src": "https://www.canva.com/design/DAGS91-b3vE/4oH3vpKWWgEPdmSKWo7flg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "표본평균의 분포",
                    "src": "https://www.canva.com/design/DAGS9z4Un_I/01aa-XnuOLe4unwLzFniBQ/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "표본평균의 분포", 
                    "subject": "probability",
                    "slug": "sampling_mean_demo_p5",
                }
          ]},
          {"key": "3-2-2", "label": "넓이", "items": [
                {
                    "type": "canva",
                    "title": "모평균의 추정",
                    "src": "https://www.canva.com/design/DAGS90gRVbo/9uH90_qTyrhm2goy6M41Ug/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "신뢰도의 의미", 
                    "subject": "probability",
                    "slug": "ci_mean_demo_p5",
                },
                {
                    "type": "activity",
                    "title": "신뢰구간의 길이에 영향을 주는 요인", 
                    "subject": "probability",
                    "slug": "ci_length_lab",
                }
          ]},
          {"key": "3-2-3", "label": "부피", "items": [
                {
                    "type": "canva",
                    "title": "모평균의 추정",
                    "src": "https://www.canva.com/design/DAGS90gRVbo/9uH90_qTyrhm2goy6M41Ug/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "신뢰도의 의미", 
                    "subject": "probability",
                    "slug": "ci_mean_demo_p5",
                },
                {
                    "type": "activity",
                    "title": "신뢰구간의 길이에 영향을 주는 요인", 
                    "subject": "probability",
                    "slug": "ci_length_lab",
                }
          ]},
          {"key": "3-2-4", "label": "속도와 거리", "items": [
                {
                    "type": "canva",
                    "title": "모평균의 추정",
                    "src": "https://www.canva.com/design/DAGS90gRVbo/9uH90_qTyrhm2goy6M41Ug/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "신뢰도의 의미", 
                    "subject": "probability",
                    "slug": "ci_mean_demo_p5",
                },
                {
                    "type": "activity",
                    "title": "신뢰구간의 길이에 영향을 주는 요인", 
                    "subject": "probability",
                    "slug": "ci_length_lab",
                }
          ]},
          {"key": "3-2-5", "label": "중단원 마무리하기기", "items": [
                {
                    "type": "canva",
                    "title": "모평균의 추정",
                    "src": "https://www.canva.com/design/DAGS90gRVbo/9uH90_qTyrhm2goy6M41Ug/view?embed",
                    "height": 800
                }
          ]}
        ],
      },
      {
        "key": "3-3",
        "label": "(3) 대단원 문제",
        "items": [
                {
                    "type": "pdf",
                    "title": "단원평가문제",
                    "src": "https://drive.google.com/file/d/1GzpmbrVEvP48zQ60gkh7TYDKJAV31Hsv/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1GzpmbrVEvP48zQ60gkh7TYDKJAV31Hsv"  # (선택) 다운로드 버튼 표시용
                }
        ],
      },
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


#<유튜브>
      #{
      #  "type": "youtube",
      #  "title": "베르누이 시행 개념",
      #  "src": "https://www.youtube.com/watch?v=VIDEO_ID",   # youtu.be/… , shorts/… 도 OK
      #  "height": 420
      #},
      #{
      #  "type": "youtube",
      #  "title": "플레이리스트(전체 강의)",
      #  "src": "https://www.youtube.com/playlist?list=PLAYLIST_ID",
      #  "height": 420
      #},
      #{
      #  "type": "youtube",
      #  "title": "시작 1분 뒤부터",
      #  "src": "https://www.youtube.com/watch?v=VIDEO_ID&start=60",  # 60초부터
      #  "height": 420
      #}
