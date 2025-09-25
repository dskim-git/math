# activities/calculus/lessons/_units.py

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
                    "title": "수열의 수렴",
                    "src": "https://www.canva.com/design/DAGTJINtKYU/Omd1Mu2Y_XJKnm44J_bk-g/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "수열의 발산",
                    "src": "https://www.canva.com/design/DAGTf3HgzqQ/_T3BOPY0NCtiVCxCq4A_Jg/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-1-2", "label": "수열의 극한값의 계산", "items": [
                {
                    "type": "canva",
                    "title": "수열의 극한에 대한 기본성질",
                    "src": "https://www.canva.com/design/DAGTf5506F8/jqmAWGR-Fe_H0k3O-FU8BQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "수열의 극한값의 계산",
                    "src": "https://www.canva.com/design/DAGTf8NezAE/FrGbQNUZjv_gCD6L7e8-lQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "수열의 극한의 대소 관계",
                    "src": "https://www.canva.com/design/DAGTfwJ2rMo/XBGrfAbVC0CRibSHZFvydQ/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-1-3", "label": "등비수열의 극한", "items": [
                {
                    "type": "canva",
                    "title": "등비수열의 수렴과 발산",
                    "src": "https://www.canva.com/design/DAGTf1cAoVk/Ji9iUiiw0BHsV9sedKvcSg/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-1-4", "label": "중단원 마무리하기", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리하기",
                    "src": "https://drive.google.com/file/d/1XitTrbBjh9z85lhvNqCOsYumdMFww9DD/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1XitTrbBjh9z85lhvNqCOsYumdMFww9DD"  # (선택) 다운로드 버튼 표시용
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
                    "title": "급수의 수렴과 발산",
                    "src": "https://www.canva.com/design/DAGTJPLiRrM/ouvXdrUIwaMhG0PoXdOwVA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "급수와 일반항 사이의 관계",
                    "src": "https://www.canva.com/design/DAGTf8_81gE/nTBONRA5I4whXQF6SZ0czg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "급수의 성질",
                    "src": "https://www.canva.com/design/DAGTf_-3v98/Pdxm2ulfjgH5hb_G-5iNvw/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-2-2", "label": "등비급수", "items": [
                {
                    "type": "canva",
                    "title": "등비급수의 수렴과 발산",
                    "src": "https://www.canva.com/design/DAGTf7j07N4/LQgVszRRtQk8ED0sxDS3wQ/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-2-3", "label": "등비급수의 활용", "items": [
                {
                    "type": "canva",
                    "title": "등비급수의 활용",
                    "src": "https://www.canva.com/design/DAGTf_W89GU/pB46cRNTKkHaM-ER6Ruw6w/view?embed",
                    "height": 800
                }
            ]},
          {"key": "1-2-4", "label": "중단원 마무리하기", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리하기",
                    "src": "https://drive.google.com/file/d/1UyLwsyPIMWWqCjz-BuNc-0eCZ6Lq2fiT/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1UyLwsyPIMWWqCjz-BuNc-0eCZ6Lq2fiT"  # (선택) 다운로드 버튼 표시용
                }
            ]}
        ],
      },
      {
        "key": "1-3",
        "label": "대단원 평가하기",
        # 소단원 없이 이 레벨에서 바로 items를 둘 수도 있습니다.
        "items": [
                {
                    "type": "pdf",
                    "title": "단원평가문제",
                    "src": "https://drive.google.com/file/d/1vUmdk6F_vLs4EBrMsw4YcvU1RTbm0fd1/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1vUmdk6F_vLs4EBrMsw4YcvU1RTbm0fd1"  # (선택) 다운로드 버튼 표시용
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
                    "title": "지수함수와 로그함수의 극한",
                    "src": "https://www.canva.com/design/DAGTJOLHg9k/-TdpYRAftQG5NZnYUZP35A/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "무리수 e와 자연로그",
                    "src": "https://www.canva.com/design/DAGTgFsAY9E/mcl3wIIc1y5H5iWcdDHYMg/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-1-2", "label": "지수함수와 로그함수의 미분", "items": [
                {
                    "type": "canva",
                    "title": "지수함수의 도함수",
                    "src": "https://www.canva.com/design/DAGTf5uDEKo/7PXATsA2bmb6cgcgXZKiGA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "로그함수의 도함수",
                    "src": "https://www.canva.com/design/DAGTgN5nxvU/7MLGgHJhsKkZFv0oIwE0XQ/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-1-3", "label": "삼각함수의 덧셈정리", "items": [
                {
                    "type": "canva",
                    "title": "삼각함수 csc, sec, cot",
                    "src": "https://www.canva.com/design/DAGTfxyahrw/sxF-q74yaBouWz2fgR5kzA/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "삼각함수의 덧셈정리",
                    "src": "https://www.canva.com/design/DAGTgFqtQIs/kG10fPbCb4fF_Sr3T9lQaA/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-1-4", "label": "삼각함수의 극한", "items": [
                {
                    "type": "canva",
                    "title": "삼각함수의 극한",
                    "src": "https://www.canva.com/design/DAGTfzOmRw8/Ey8xu_Jx_jluzgfKUNGMiQ/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "함수 sinx/x의 극한",
                    "src": "https://www.canva.com/design/DAGTgOvpQvE/K73Y4tEgwQbqPdSWnIKZ_A/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-1-5", "label": "삼각함수의 미분", "items": [
                {
                    "type": "canva",
                    "title": "삼각함수의 도함수",
                    "src": "https://www.canva.com/design/DAGTfz-tZaU/eL-ZCerVU523qt2Ozwwj_Q/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-1-6", "label": "중단원 마무리하기", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리하기",
                    "src": "https://drive.google.com/file/d/13eV3v_W_XA_ietxyyKcUCCRSi8p5JRPb/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=13eV3v_W_XA_ietxyyKcUCCRSi8p5JRPb"  # (선택) 다운로드 버튼 표시용
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
                    "title": "함수의 몫의 미분법",
                    "src": "https://www.canva.com/design/DAGTJCfzwUs/xsmP_1x7-N1jGOan8vwr_Q/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "함수 y=x^n (n은 정수)의 도함수",
                    "src": "https://www.canva.com/design/DAGTgP2DKTg/HPMYK6i-1fDYfxl99MENKg/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-2-2", "label": "합성함수의 미분법", "items": [
                {
                    "type": "canva",
                    "title": "합성함수의 미분법",
                    "src": "https://www.canva.com/design/DAGTgA55y9Y/TqfP4VjJJ6A5O9HJij39iw/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "함수 y=x^n (n은 실수)의 도함수",
                    "src": "https://www.canva.com/design/DAGTgK1QPik/B4MoH-lJtuLl9Wp6_BPKiQ/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-2-3", "label": "매개변수로 나타낸 함수의 미분법", "items": [
                {
                    "type": "canva",
                    "title": "매개변수로 나타낸 함수",
                    "src": "https://www.canva.com/design/DAGTgEykzsU/0DNM-bJ5FwB1SyoDpXBwAg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "매개변수로 나타낸 함수의 미분법",
                    "src": "https://www.canva.com/design/DAGTgO71PFU/RvDE9TFYZIcv3nxRCzekPw/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-2-4", "label": "음함수와 역함수의 미분법", "items": [
                {
                    "type": "canva",
                    "title": "음함수의 미분법",
                    "src": "https://www.canva.com/design/DAGTgPzQEI0/UFXL0KGeJlhVDEc1QbFiAw/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "역함수의 미분법",
                    "src": "https://www.canva.com/design/DAGTgHmGH2o/9Kwr_MGN66woxTtl0cZI3w/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-2-5", "label": "이계도함수", "items": [
                {
                    "type": "canva",
                    "title": "이계도함수",
                    "src": "https://www.canva.com/design/DAGTgH_lLFw/2wzCQXPoA60ecz0KnB01SQ/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-2-6", "label": "중단원 마무리하기", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리하기",
                    "src": "https://drive.google.com/file/d/1O2SbanhKp3fOwVrgWOoA7bwwfkKurDhA/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1O2SbanhKp3fOwVrgWOoA7bwwfkKurDhA"  # (선택) 다운로드 버튼 표시용
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
                    "title": "접선의 방정식",
                    "src": "https://www.canva.com/design/DAGTJFATDO4/RFej0XWGWp5Ni1TeRbBFKg/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-3-2", "label": "함수의 그래프", "items": [
                {
                    "type": "canva",
                    "title": "함수의 증가와 감소, 극대와 극소",
                    "src": "https://www.canva.com/design/DAGTg9Snfts/azVJqiUxdzCcF7kwgIS_Hg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "곡선의 오목과 볼록",
                    "src": "https://www.canva.com/design/DAGTg4nd_bY/s140hd92wu7B4ngZvhPKcg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "함수의 그래프",
                    "src": "https://www.canva.com/design/DAGTg6TRReM/gK5YTlkucfOm0q4741PFHg/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "함수의 최대와 최소",
                    "src": "https://www.canva.com/design/DAGTg_Z2WfQ/bQwiYC1S0Ftwf-Zcrmt9-w/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-3-3", "label": "방정식과 부등식에의 활용", "items": [
                {
                    "type": "canva",
                    "title": "방정식에의 활용",
                    "src": "https://www.canva.com/design/DAGTgwmUeY4/J0_m3exRzgeJEnLuPGkk9g/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "부등식에의 활용",
                    "src": "https://www.canva.com/design/DAGTg3oijls/RLgzbWDOki614QsiR9jiVQ/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-3-4", "label": "속도와 가속도", "items": [
                {
                    "type": "canva",
                    "title": "직선 운동에서의 속도와 가속도",
                    "src": "https://www.canva.com/design/DAGTgz882-M/O-R6dhouOg4qJQ5h_LfIew/view?embed",
                    "height": 800
                },
                {
                    "type": "canva",
                    "title": "평면 운동에서의 속도와 가속도",
                    "src": "https://www.canva.com/design/DAGTg9FTQNg/BNC4m0pTXDZgFdjuH5kHCQ/view?embed",
                    "height": 800
                }
          ]},
          {"key": "2-3-5", "label": "중단원 마무리하기", "items": [
                {
                    "type": "pdf",
                    "title": "중단원 마무리하기",
                    "src": "https://drive.google.com/file/d/12NgdxTgz5I0mD0z2bWwezfbidZgKR3MJ/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=12NgdxTgz5I0mD0z2bWwezfbidZgKR3MJ"  # (선택) 다운로드 버튼 표시용
                }
          ]}
        ],
      },
      {
        "key": "2-4",
        "label": "대단원 문제",
        "items": [
                {
                    "type": "pdf",
                    "title": "단원평가문제",
                    "src": "https://drive.google.com/file/d/1msRUWn2RP7RG9zdmrik6o8-FMORM0wIC/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=1msRUWn2RP7RG9zdmrik6o8-FMORM0wIC"  # (선택) 다운로드 버튼 표시용
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
                    "type": "pdf",
                    "title": "중단원 마무리하기",
                    "src": "https://drive.google.com/file/d/13eV3v_W_XA_ietxyyKcUCCRSi8p5JRPb/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=13eV3v_W_XA_ietxyyKcUCCRSi8p5JRPb"  # (선택) 다운로드 버튼 표시용
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
                    "type": "pdf",
                    "title": "중단원 마무리하기",
                    "src": "https://drive.google.com/file/d/13eV3v_W_XA_ietxyyKcUCCRSi8p5JRPb/preview",
                    #"height": 900,
                    "download": "https://drive.google.com/uc?export=download&id=13eV3v_W_XA_ietxyyKcUCCRSi8p5JRPb"  # (선택) 다운로드 버튼 표시용
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
