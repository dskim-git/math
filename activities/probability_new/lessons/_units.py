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
          {"key": "1-1-1", "label": "여러 가지 순열", "items": [
                {
                    "type": "canva",
                    "title": "중복순열",
                    "src": "https://www.canva.com/design/DAHC5PirjcY/uvXHr_miHQ-AwSZ32-cB3Q/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 비밀번호 경우의 수 탐색기",
                    "subject": "probability_new",
                    "slug": "mini/rep_perm_password",
                },
                {
                    "type": "activity",
                    "title": "미니: 모스 부호와 중복순열",
                    "subject": "probability_new",
                    "slug": "mini/rep_perm_morse",
                },
                {
                    "type": "activity",
                    "title": "미니: 색깔 타일 배열기",
                    "subject": "probability_new",
                    "slug": "mini/rep_perm_tiles",
                },
                {
                    "type": "activity",
                    "title": "미니: 주사위 연속 던지기와 중복순열",
                    "subject": "probability_new",
                    "slug": "mini/rep_perm_dice",
                },
                {
                    "type": "canva",
                    "title": "같은 것이 있는 순열",
                    "src": "https://www.canva.com/design/DAHC5Lf4DO0/SRtT5-ot2uNc1t3WKf1qag/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 삼색기와 같은 것이 있는 순열",
                    "subject": "probability_new",
                    "slug": "mini/tricolor_flag_perm",
                },
                {
                    "type": "activity",
                    "title": "미니: 정육면체 최단경로와 같은 것이 있는 순열",
                    "subject": "probability_new",
                    "slug": "mini/cube_path_perm",
                },
                {
                    "type": "activity",
                    "title": "미니: 단어 다이아몬드와 같은 것이 있는 순열",
                    "subject": "probability_new",
                    "slug": "mini/word_diamond_perm",
                },
            ]},
          {"key": "1-1-2", "label": "중복조합", "items": [
                {
                    "type": "canva",
                    "title": "중복조합",
                    "src": "https://www.canva.com/design/DAHC5BwlzB0/5UHPurQTyTDyvihjWyhvZg/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 중복조합의 3가지 이해 방법",
                    "subject": "probability_new",
                    "slug": "mini/rep_comb_stars_bars",
                },
                {
                    "type": "activity",
                    "title": "미니: 다항식 전개의 항의 개수",
                    "subject": "probability_new",
                    "slug": "mini/poly_expand_term_count",
                },
                {
                    "type": "activity",
                    "title": "미니: 함수의 개수와 경우의 수",
                    "subject": "probability_new",
                    "slug": "mini/function_count_lab",
                },
            ]},
          {"key": "1-1-3", "label": "중단원 마무리 문제", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리 문제",
                    "src": "https://drive.google.com/file/d/1D_DEPylJ9dNV8yDruIDKrjd4v5LhjMwP/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1D_DEPylJ9dNV8yDruIDKrjd4v5LhjMwP"  # (선택) 다운로드 버튼 표시용
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
                    "src": "https://www.canva.com/design/DAHDnrsVQ_I/5wfhrpP9svjGEfanwHR0hA/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 이항정리 계수의 탄생",
                    "subject": "probability_new",
                    "slug": "mini/binomial_coeff_viz",
                },
                {
                    "type": "canva",
                    "title": "이항정리의 활용",
                    "src": "https://www.canva.com/design/DAHDnr-AdUg/f09JAABVbg4QfGwUTfPeug/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 이항정리의 활용",
                    "subject": "probability_new",
                    "slug": "mini/binomial_theorem_apply",
                },
                {
                    "type": "canva",
                    "title": "파스칼의 삼각형",
                    "src": "https://www.canva.com/design/DAHDnplxYaU/QNqLkvHNlUrPG5kyd2253A/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "갈톤보드 시뮬레이션",
                    "subject": "probability_new",
                    "slug": "mini/galton_board",
                },
                {
                    "type": "activity",
                    "title": "파스칼의 삼각형 성질 탐구",
                    "subject": "probability_new",
                    "slug": "mini/pascal_triangle_properties",
                },
                {
                    "type": "activity",
                    "title": "🔵 원 위의 점으로 만든 도형으로 파스칼의 삼각형 발견",
                    "subject": "probability_new",
                    "slug": "mini/polygon_count_circles",
                },
                {
                    "type": "gsheet",
                    "title": "엑셀로 만든 파스칼의 삼각형",
                    "src": "https://docs.google.com/spreadsheets/d/17F8RhpLp8XNhiOICfUlxnFFjDEQCCjLVAQyUADkUjz8/edit?usp=drivesdk",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 파스칼 삼각형에서 찾아보는 프랙털",
                    "subject": "probability_new",
                    "slug": "mini/pascal_fractal",
                },
                {
                    "type": "activity",
                    "title": "미니: 손가락 게임 '모라'와 같은 것이 있는 순열",
                    "subject": "probability_new",
                    "slug": "mini/morra_game",
                },
                # 필요하면 여기에 추가 자료를 이어서 넣으면 됩니다.
                # {"type":"activity","title":"활동 예시","subject":"probability","slug":"binomial_simulator"},
                # {"type":"url","title":"보충 설명","src":"https://..."},
            ]},
          {"key": "1-2-2", "label": "중단원 마무리 문제", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리 문제",
                    "src": "https://drive.google.com/file/d/1RUqvu5ANdTAYE8NJX8Jvby0vOKEr8ICC/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1RUqvu5ANdTAYE8NJX8Jvby0vOKEr8ICC"  # (선택) 다운로드 버튼 표시용
                }
            ]},
        ],
      },
      {
        "key": "1-3",
        "label": "대단원 평가 문제",
        # 소단원 없이 이 레벨에서 바로 items를 둘 수도 있습니다.
        "items": [
                {
                    "type": "pdf",
                    "title": "대단원 평가 문제",
                    "src": "https://drive.google.com/file/d/1cbOtEmSGo-LbEInmixGozEc49KZyWbK-/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1cbOtEmSGo-LbEInmixGozEc49KZyWbK-"  # (선택) 다운로드 버튼 표시용
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
        "label": "(1) 확률의 개념과 활용",
        "children": [
          {"key": "2-1-1", "label": "확률", "items": [
                {
                    "type": "canva",
                    "title": "시행과 사건",
                    "src": "https://www.canva.com/design/DAHE0hTDc-E/DlS4JYShiG-MNQ80eKsleg/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "🎯 확률 용어 마스터",
                    "subject": "probability_new",
                    "slug": "mini/trial_event_vocab_game",
                },
                {
                    "type": "canva",
                    "title": "수학적 확률",
                    "src": "https://www.canva.com/design/DAHE0uTouFM/D7xBQtE_fDy1tiLEYssFMQ/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 이상한 주사위와 수학적 확률",
                    "subject": "probability_new",
                    "slug": "mini/weird_dice_sim",
                },
                {
                    "type": "canva",
                    "title": "통계적 확률",
                    "src": "https://www.canva.com/design/DAHE0hrexZA/HyEwTJ5kxX2q-uU2AcqkzA/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 통계적 확률 탐험대 (윷놀이·기상예보·야구 타율)",
                    "subject": "probability_new",
                    "slug": "mini/statistical_prob_sim",
                },
                {
                    "type": "activity",
                    "title": "미니: 통계적 확률 실험실 (동전·주사위·카드)",
                    "subject": "probability_new",
                    "slug": "mini/stat_prob_experiment",
                },
                {
                    "type": "activity",
                    "title": "미니: 주사위 실험(애니메이션)", 
                    "subject": "probability",
                    "slug": "mini/dice_lab",
                },
                {
                    "type": "activity",
                    "title": "미니: 뷔퐁의 바늘 실험 (π 추정 시뮬레이터)",
                    "subject": "probability_new",
                    "slug": "mini/buffon_needle_mini",
                },
                {
                    "type": "activity",
                    "title": "미니: 베르트랑의 역설 시뮬레이터",
                    "subject": "probability_new",
                    "slug": "mini/bertrand_paradox_mini",
                },
                {
                    "type": "canva",
                    "title": "확률의 기본 성질",
                    "src": "https://www.canva.com/design/DAHE0hzig3g/gCebYuXyGrimsNtlwODBkw/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 확률의 기본 성질 탐험 (공사건·전사건)",
                    "subject": "probability_new",
                    "slug": "mini/prob_basic_properties",
                },
                #{
                #    "type": "gsheet",
                #    "title": "수학적 확률과 통계적 확률의 관계",
                #    "src": "https://docs.google.com/spreadsheets/d/1oz2DHhzrRxRFRn92RcGZdupPGvXUzWTk/edit?usp=drivesdk",
                #    "height": 800
                #},
                #{
                #    "type": "iframe",
                #    "title": "수학적 확률과 통계적 확률의 관계 (통그라미)",
                #    "src": "https://tong.kostat.go.kr/tongramy_web/main.do?menuSn=163#",
                #    "height": 800
                #},
                #{
                #    "type": "activity",
                #    "title": "뷔퐁의 바늘 실험",
                #    "subject": "probability",
                #    "slug": "buffon_needle_p5"
                #},
                #{
                #    "type": "iframe",
                #    "title": "뷔퐁의 바늘 실험(일리노이대)",
                #    "src": "https://mste.illinois.edu/activity/buffon/",
                #    "height": 800
                #}
          ]},
          {"key": "2-1-2", "label": "확률의 덧셈정리", "items": [
                {
                    "type": "canva",
                    "title": "확률의 덧셈정리",
                    "src": "https://www.canva.com/design/DAHE0irIk_8/bhCvdYrxMvhSBd59OtrXmg/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 확률의 덧셈정리 탐험",
                    "subject": "probability_new",
                    "slug": "mini/prob_addition_theorem",
                },
                {
                    "type": "canva",
                    "title": "여사건의 확률",
                    "src": "https://www.canva.com/design/DAHE0qz9KNg/F37GtZ99uPIUJzWdiKEk7Q/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 생일 역설 탐구",
                    "subject": "probability_new",
                    "slug": "mini/birthday_paradox_mini",
                },
                {
                    "type": "activity",
                    "title": "🔀 미니: 심프슨의 역설",
                    "subject": "probability_new",
                    "slug": "mini/simpsons_paradox_mini",
                },
                #{
                #    "type": "activity",
                #    "title": "몬티홀 문제",
                #    "subject": "probability",
                #    "slug": "monty_hall_p5"
                #},
                #{
                #    "type": "activity",
                #    "title": "몬티홀 문제(확장)",
                #    "subject": "probability",
                #    "slug": "monty_hall_extended_p5"
                #}
          ]},
          {"key": "2-1-3", "label": "중단원 마무리 문제", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리 문제",
                    "src": "https://drive.google.com/file/d/1S4WxvVAEazBJXPR0ek6Sfo4JS0X0eDp8/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1S4WxvVAEazBJXPR0ek6Sfo4JS0X0eDp8"  # (선택) 다운로드 버튼 표시용
                }
          ]},
        ],
      },
      {
        "key": "2-2",
        "label": "(2) 조건부확률",
        "children": [
          {"key": "2-2-1", "label": "조건부확률", "items": [
                {
                    "type": "canva",
                    "title": "조건부확률",
                    "src": "https://www.canva.com/design/DAHHjd-T0pM/t7BwcejOtZqBjDgCMNdJWw/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "베이즈 정리와 몬티홀 문제",
                    "src": "https://www.canva.com/design/DAHHun0TwPc/dfBTMOWl1vTJYQvoKsKGMQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "확률의 곱셈정리",
                    "src": "https://www.canva.com/design/DAHHtj9V3gk/MAt-nX9jo26AolBCJa5vVQ/view?embed",
                    "height": 800
                },
                #{
                #    "type": "activity",
                #    "title": "미니: 몬티홀 문제 시뮬레이터",
                #    "subject": "probability",
                #    "slug": "mini/monty_hall_mini",
                #},
                #{
                #    "type": "activity",
                #    "title": "미니: 홀수일 때 소수일 확률 (한 번 실행)",
                #    "subject": "probability",
                #    "slug": "mini/odd_prime_conditional",   # 👈 파일명
                #},
                #{
                #    "type": "activity",
                #    "title": "미니: 확률 수렴 관찰(10,100,1,000...)", 
                #    "subject": "probability",
                #    "slug": "mini/odd_prime_convergence",
                #}
          ]},
          {"key": "2-2-2", "label": "사건의 독립과 종속", "items": [
                {
                    "type": "canva",
                    "title": "사건의 독립과 종속",
                    "src": "https://www.canva.com/design/DAHHtjXp3tM/YHLc81eRZyMuS30Pb8OMXg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "독립시행",
                    "src": "https://www.canva.com/design/DAGNlxAwu88/yD-UCHkAqRJGp1wInKifRA/view?embed",
                    "height": 800
                },
                #{
                #    "type": "activity",
                #    "title": "신기한 주사위", 
                #    "subject": "probability",
                #    "slug": "mini/nontransitive_dice_lab",
                #},
                #{
                #    "type": "canva",
                #    "title": "AI로 공정한 게임의 확률 검증하기",
                #    "src": "https://www.canva.com/design/DAG2NDANiTM/ZrgIgrdEzKG5g_7eF_gvDQ/view?embed",
                #    "height": 800
                #},
                {
                    "type": "youtube",
                    "title": "상금 분배 문제",
                    "src": "https://youtu.be/InAIZ3tP_Mk?si=pQoxDuxJBC1AsC3b&start=535",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "몬테카를로 시뮬레이션",
                    "subject": "probability",
                    "slug": "binomial_simulator"
                }
          ]},
          {"key": "2-2-3", "label": "중단원 마무리 문제", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리 문제",
                    "src": "https://drive.google.com/file/d/1-0MKRkeaYx_-5X6yWR7ASIbI5mNTg0Dn/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1-0MKRkeaYx_-5X6yWR7ASIbI5mNTg0Dn"  # (선택) 다운로드 버튼 표시용
                }
          ]},
        ],
      },
      {
        "key": "2-3",
        "label": "대단원 평가 문제",
        "items": [
                {
                    "type": "pdf",
                    "title": "대단원 평가 문제",
                    "src": "https://drive.google.com/file/d/1QOGba8ty59JZbRV7K4QmkUWa6DUk-RTw/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1QOGba8ty59JZbRV7K4QmkUWa6DUk-RTw"  # (선택) 다운로드 버튼 표시용
                }
        ],
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
          {"key": "3-1-1", "label": "확률변수와 확률분포", "items": [
                {
                    "type": "canva",
                    "title": "확률변수",
                    "src": "https://www.canva.com/design/DAHHjRnO0ko/J64Bs8aj0bS4hYD50_CpGw/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이산확률변수와 확률분포",
                    "src": "https://www.canva.com/design/DAHHtpfVIuY/fjt5cjcVR2Kdi4xj0UrF4g/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "연속확률변수와 확률분포",
                    "src": "https://www.canva.com/design/DAHHtvKWtZM/e1YwzLcb0TIGtuMYa9D4Kw/view?embed",
                    "height": 800
                }
          ]},
          {"key": "3-1-2", "label": "이산확률변수의 기댓값과 표준편차", "items": [
                {
                    "type": "canva",
                    "title": "이산확률변수의 기댓값과 표준편차",
                    "src": "https://www.canva.com/design/DAHHtqGo-6k/DQusCYDoZYH9bAtF_kwPug/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이산확률변수 aX+b의 평균과 표준편차",
                    "src": "https://www.canva.com/design/DAHHtj_-9Aw/9v2LPxicZwwbfuDekrCVVg/view?embed",
                    "height": 800
                },
                {
                    "type": "iframe",
                    "title": "확률변수 aX+b의 평균과 표준편차 확인 (통그라미)",
                    "src": "https://tong.kostat.go.kr/tongramy_web/main.do?menuSn=163#",
                    "height": 800
                }
          ]},
          {"key": "3-1-3", "label": "이항분포", "items": [
                {
                    "type": "canva",
                    "title": "이항분포",
                    "src": "https://www.canva.com/design/DAHHtsAfOrM/SD11sAaEr-VB4V1NRgUbuQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이항분포의 평균, 분산, 표준편차",
                    "src": "https://www.canva.com/design/DAHHthQw6HA/2jFxEgrrAK_wxhoHz2cmHA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이항분포의 그래프",
                    "src": "https://www.canva.com/design/DAHHtlDw-2I/EybNje4V8ld_PBWQqOYwOg/view?embed",
                    "height": 800
                },
                {
                    "type": "iframe",
                    "title": "이항분포의 그래프 (통그라미)",
                    "src": "https://tong.kostat.go.kr/tongramy_web/main.do?menuSn=163#",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "큰 수의 법칙",
                    "src": "https://www.canva.com/design/DAHHtmIHxYQ/NDR1ngyJdVyRL0e_AkoCLg/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 큰 수의 법칙 이해",
                    "subject": "probability",
                    "slug": "mini/lln_binomial_simple"
                }
          ]},
          {"key": "3-1-4", "label": "정규분포", "items": [
                {
                    "type": "canva",
                    "title": "정규분포",
                    "src": "https://www.canva.com/design/DAHHttZIu5s/sPcx8s1EV6pD_13IYxJ8MA/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "정규분포곡선 비교", 
                    "subject": "probability",
                    "slug": "mini/normal_compare_p5",
                },
                {
                    "type": "canva",
                    "title": "표준정규분포",
                    "src": "https://www.canva.com/design/DAHHth-zVlo/dBt59aVjfTzSB53aYrk-Wg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "정규분포의 표준화",
                    "src": "https://www.canva.com/design/DAHHtiQHdp8/XpN9BZZmdcrUyobqH_y8Jg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이항분포와 정규분포의 관계",
                    "src": "https://www.canva.com/design/DAHHtlDD220/Go3VKHllAg4LBe-HbcovKw/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "이항분포의 정규 근사", 
                    "subject": "probability",
                    "slug": "binomial_normal_approx",
                }
          ]},
          {"key": "3-1-5", "label": "중단원 마무리 문제", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리 문제",
                    "src": "https://drive.google.com/file/d/1mSG1Iq91ghij6RGu4TD8pI3FdSjuWWsO/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1mSG1Iq91ghij6RGu4TD8pI3FdSjuWWsO"  # (선택) 다운로드 버튼 표시용
                }
          ]},
        ],
      },
      {
        "key": "3-2",
        "label": "(2) 통계적 추정",
        "children": [
          {"key": "3-2-1", "label": "모집단과 표본", "items": [
                {
                    "type": "canva",
                    "title": "모집단과 표본",
                    "src": "https://www.canva.com/design/DAHHjWpeMM4/1TFOK8RjuqLGfjsgFtpg4Q/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "임의추출",
                    "src": "https://www.canva.com/design/DAHHuXg-Lcs/k5ZtC2VJ-xpslK3ffT4Hiw/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "카드 추출하기", 
                    "subject": "probability",
                    "slug": "mini/sampling_cards",
                }
          ]},
          {"key": "3-2-2", "label": "모평균의 추정", "items": [
                {
                    "type": "canva",
                    "title": "모평균과 표본평균",
                    "src": "https://www.canva.com/design/DAHHuYYnToQ/9KwMXGYRpyFzn7LEPj_33A/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "표본분산을 n-1로 나누는 이유", 
                    "subject": "probability",
                    "slug": "mini/sample_variance_unbiased",
                },
                {
                    "type": "canva",
                    "title": "표본평균의 평균, 분산, 표준편차",
                    "src": "https://www.canva.com/design/DAHHuVkY5Nk/_WjjnmteoptPg3Cu1nsfbw/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "표본평균의 분포",
                    "src": "https://www.canva.com/design/DAHHubQNSZ0/s9MAmaWQRfhqnf_uQn5gAQ/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "표본평균의 분포 확인하기", 
                    "subject": "probability",
                    "slug": "mini/sample_mean_dist",
                },
                {
                    "type": "activity",
                    "title": "표본평균의 분포", 
                    "subject": "probability",
                    "slug": "sampling_mean_demo_p5",
                },
                {
                    "type": "canva",
                    "title": "모평균의 추정",
                    "src": "https://www.canva.com/design/DAHHuebhCRE/pZdi-cCqw6KItUAt2WXCgw/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "신뢰도 vs 정확도", 
                    "subject": "probability",
                    "slug": "mini/confidence_tradeoff",
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
          {"key": "3-2-3", "label": "모비율의 추정", "items": [
                {
                    "type": "canva",
                    "title": "모비율과 표본비율",
                    "src": "https://www.canva.com/design/DAHHubI7TPY/TE4S7QmetsL7EWiTgCAITg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "표본비율의 분포",
                    "src": "https://www.canva.com/design/DAHHuURQStE/HiQwUmv9U6WlYoxcgSj6HA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "모비율의 추정",
                    "src": "https://www.canva.com/design/DAHHuZyUjs4/3nw4kr83Dw90dK7kvv5eUA/view?embed",
                    "height": 800
                },
          ]},
          {"key": "3-2-4", "label": "중단원 마무리 문제", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리 문제",
                    "src": "https://drive.google.com/file/d/1fuMquRZOaueDf_JoGXeBWh9SJSyigt9G/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1fuMquRZOaueDf_JoGXeBWh9SJSyigt9G"  # (선택) 다운로드 버튼 표시용
                }
          ]}
        ],
      },
      {
        "key": "3-3",
        "label": "대단원 문제",
        "items": [
                {
                    "type": "pdf",
                    "title": "단원평가문제",
                    "src": "https://drive.google.com/file/d/1PT-xpGi6feHIS2lUEJy1skBvbgBlIrUo/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1PT-xpGi6feHIS2lUEJy1skBvbgBlIrUo"  # (선택) 다운로드 버튼 표시용
                }
        ],
      },
    ],
  },

  # 교육과정 외
  {
    "key": "X",
    "label": "교육과정 외",
    "children": [
      {"key": "X-1", "label": "원순열", "items": [
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
                },
                {
                    "type": "activity",
                    "title": "다각형 변 위에 숫자 배열하기", 
                    "subject": "probability",
                    "slug": "mini/polygon_edge_arrangements_p5",
                }
      ]},
      {"key": "X-2", "label": "분할", "items": [
                {
                    "type": "canva",
                    "title": "자연수의 분할",
                    "src": "https://www.canva.com/design/DAGS9swrMnU/-MrWr69kFUAK2DiiJ-nZOA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "집합의 분할",
                    "src": "https://www.canva.com/design/DAGS9oZDjH0/fNsFxjitrj0nTZrAwmBccA/view?embed",
                    "height": 800
                }
      ]},
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
