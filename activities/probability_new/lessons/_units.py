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
          {"key": "2-2-1", "label": "조건부확률", "items": [
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
          {"key": "2-2-2", "label": "확률의 곱셈정리", "items": [
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
                },
                {
                    "type": "canva",
                    "title": "AI로 공정한 게임의 확률 검증하기",
                    "src": "https://www.canva.com/design/DAG2NDANiTM/ZrgIgrdEzKG5g_7eF_gvDQ/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-2-3", "label": "사건의 독립과 종속", "items": [
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
          {"key": "2-2-4", "label": "독립시행의 확률", "items": [
                {
                    "type": "canva",
                    "title": "독립시행",
                    "src": "https://www.canva.com/design/DAGNl8UMPCw/ksQ3KQ4X1iM2Oqkeaph6AA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "독립시행의 확률",
                    "src": "https://www.canva.com/design/DAGNl5tpm-U/FDixwJ7G4_sU_sDAq0SB_A/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "몬테카를로 시뮬레이션",
                    "subject": "probability",
                    "slug": "binomial_simulator"
                }
          ]},
        ],
      },
      {
        "key": "2-3",
        "label": "대단원 문제",
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
          {"key": "3-1-2", "label": "이산확률변수의 기댓값과 표준편차", "items": [
                {
                    "type": "canva",
                    "title": "이산확률변수의 기댓값과 표준편차",
                    "src": "https://www.canva.com/design/DAGPlVNYwTY/jVyt833FOWh8vvOxJpdNmg/view?embed",
                    "height": 800
                }
          ]},
          {"key": "3-1-3", "label": "이산확률변수 aX+b의 평균, 분산, 표준편차", "items": [
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
          {"key": "3-1-4", "label": "이항분포", "items": [
                {
                    "type": "canva",
                    "title": "이항분포",
                    "src": "https://www.canva.com/design/DAGPla1Cvro/HtiMM_RVFELx46wGvk76iw/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이항분포의 평균과 표준편차",
                    "src": "https://www.canva.com/design/DAGPlRem8xg/hYCHXkQKzbCavXITM80CXw/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "이항분포의 그래프",
                    "src": "https://www.canva.com/design/DAGPlWgz3UQ/0GLwwGBBhQRa5JafSZ55cQ/view?embed",
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
                    "src": "https://www.canva.com/design/DAGPlZbIltE/uDkL0_1Qcg5b4A_tj6fQuw/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "미니: 큰 수의 법칙 이해",
                    "subject": "probability",
                    "slug": "mini/lln_binomial_simple"
                }
          ]},
          {"key": "3-1-5", "label": "정규분포", "items": [
                {
                    "type": "canva",
                    "title": "정규분포",
                    "src": "https://www.canva.com/design/DAGPlbH_5JI/ubpH_t_WTPU99u-sB-Rjew/view?embed",
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
                    "src": "https://www.canva.com/design/DAGPlg-qoNE/P2cinoqT-ioXTFKQvLtb6Q/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "정규분포의 표준화",
                    "src": "https://www.canva.com/design/DAGPlvghs60/OysmhTfWoIpbxX35Q2abzQ/view?embed",
                    "height": 800
                }
          ]},
          {"key": "3-1-6", "label": "이항분포와 정규분포의 관계", "items": [
                {
                    "type": "canva",
                    "title": "이항분포와 정규분포의 관계",
                    "src": "https://www.canva.com/design/DAGPleUNg4U/51nlL9mmKChTXvKFKr55GQ/view?embed",
                    "height": 800
                },
                {
                    "type": "activity",
                    "title": "이항분포의 정규 근사", 
                    "subject": "probability",
                    "slug": "binomial_normal_approx",
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
                    "type": "activity",
                    "title": "카드 추출하기", 
                    "subject": "probability",
                    "slug": "mini/sampling_cards",
                },
                {
                    "type": "canva",
                    "title": "모평균과 표본평균",
                    "src": "https://www.canva.com/design/DAGS91-b3vE/4oH3vpKWWgEPdmSKWo7flg/view?embed",
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
                    "title": "표본평균의 분포",
                    "src": "https://www.canva.com/design/DAGS9z4Un_I/01aa-XnuOLe4unwLzFniBQ/view?embed",
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
                }
          ]},
          {"key": "3-2-2", "label": "모평균의 추정", "items": [
                {
                    "type": "canva",
                    "title": "모평균의 추정",
                    "src": "https://www.canva.com/design/DAGS90gRVbo/9uH90_qTyrhm2goy6M41Ug/view?embed",
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
        ],
      },
      {
        "key": "3-3",
        "label": "대단원 문제",
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
      {"key": "X-3", "label": "모비율의 추정", "items": [
                {
                    "type": "canva",
                    "title": "모비율과 표본비율",
                    "src": "https://www.canva.com/design/DAGS90stL6s/rMetpkhThK6Ji_AHJuYAeQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "집합의 분할",
                    "src": "https://www.canva.com/design/DAGS99UW0Mg/8ZKtl84JYgpW9KBrW32hPg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "집합의 분할",
                    "src": "https://www.canva.com/design/DAGS99puNoY/FYgb8JOvqHhlPQgS0TGebQ/view?embed",
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
