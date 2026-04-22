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
                            {
                                "type": "canva",
                                "title": "다항식의 정리",
                                "src": "https://www.canva.com/design/DAHDEJoHCTU/X7qpJ4Y2F_fkfxUuqZyfXw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🃏 항 카드 정렬 게임",
                                "subject": "common",
                                "slug": "mini/poly_sort_game"
                            },
                            {
                                "type": "canva",
                                "title": "다항식의 덧셈과 뺄셈",
                                "src": "https://www.canva.com/design/DAHDEHRkj2Q/JGbuWNdqt5iDUUdE3UHSsw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🔗 동류항 연결 게임",
                                "subject": "common",
                                "slug": "mini/poly_add_sub_game"
                            },
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
                                "type": "activity",
                                "title": "🧮 곱셈 공식 확장 탐구",
                                "subject": "common",
                                "slug": "mini/poly_mul_expand"
                            },
                            {
                                "type": "activity",
                                "title": "🧩 대수막대로 곱셈 공식 탐구",
                                "subject": "common",
                                "slug": "mini/algebra_tile_formulas"
                            },
                            {
                                "type": "activity",
                                "title": "✖️ 갤로시아 곱셈 탐구 (수·다항식)",
                                "subject": "common",
                                "slug": "mini/gelosia_mul"
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
                            },
                            {
                                "type": "activity",
                                "title": "🔢 조립제법 원리 탐구 – 계수 비교법으로 이해하기",
                                "subject": "common",
                                "slug": "mini/synthetic_div_principle"
                            },
                            {
                                "type": "activity",
                                "title": "🃏 나머지가 같은 식 탐험",
                                "subject": "common",
                                "slug": "mini/remainder_same_expressions"
                            },
                            {
                                "type": "activity",
                                "title": "📊 스프레드시트로 조립제법 구현하기",
                                "subject": "common",
                                "slug": "mini/synthetic_div_spreadsheet"
                            },
                            {
                                "type": "activity",
                                "title": "➗ 갤로시아 나눗셈 탐구 (다항식)",
                                "subject": "common",
                                "slug": "mini/gelosia_div"
                            },
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
                                "download": "https://drive.google.com/uc?export=download&id=1jRdV1GXgwqkhnpTWn0rllrpnLljMllRN"  # (선택) 다운로드 버튼 표시용
                }
                        ],
                    },
                ],
            },
            {
                "key": "1-2",
                "label": "(2) 나머지정리와 인수분해",
                "children": [
                    {
                        "key": "1-2-1",
                        "label": "항등식과 나머지정리",
                        "items": [
                            {
                                "type": "canva",
                                "title": "항등식의 성질",
                                "src": "https://www.canva.com/design/DAHDI99sxS4/US6oIgAJSCE_fcZ1-zPuVg/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🔍 항등식 탐정 게임",
                                "subject": "common",
                                "slug": "mini/identity_game"
                            },
                            {
                                "type": "canva",
                                "title": "미정계수법",
                                "src": "https://www.canva.com/design/DAHDI3-7ioc/s3qyHF1rQDw-tpdE71lt5Q/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🔑 미정계수법 탐정 게임",
                                "subject": "common",
                                "slug": "mini/undefined_coefficients"
                            },
                            {
                                "type": "canva",
                                "title": "나머지정리",
                                "src": "https://www.canva.com/design/DAHDI2U-E3c/g1DY6SWInl5nESlFjFqQ3A/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "인수정리",
                                "src": "https://www.canva.com/design/DAHDI5T663c/gICWu0Vt7S-nB_ooShr16w/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🚀 거듭제곱 나머지 부스터",
                                "subject": "common",
                                "slug": "mini/power_remainder_booster"
                            },
                            {
                                "type": "activity",
                                "title": "🎯 인수 후보 레이더",
                                "subject": "common",
                                "slug": "mini/factor_candidate_radar"
                            }
                        ],
                    },
                    {
                        "key": "1-2-2",
                        "label": "인수분해",
                        "items": [
                            {
                                "type": "canva",
                                "title": "다항식의 인수분해",
                                "src": "https://www.canva.com/design/DAHDI90xSJQ/tDqzeZZF5OrIkMI1rLl55A/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "인수정리를 이용한 인수분해",
                                "src": "https://www.canva.com/design/DAHDIxwQ-UE/sevPmqArsV_F-L-PS-mEpA/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🔐 소수·합성수 잠금 해제",
                                "subject": "common",
                                "slug": "mini/prime_composite_lock"
                            },
                            {
                                "type": "activity",
                                "title": "🧭 인수분해 패스파인더 아케이드",
                                "subject": "common",
                                "slug": "mini/factor_pathfinder_arcade"
                            }
                        ],
                    },
                    {
                        "key": "1-2-3",
                        "label": "중단원 점검하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "중단원 마무리 문제",
                                "src": "https://drive.google.com/file/d/133FQCx_vxoJhjjHm9CbgxwPBBSqe9auw/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=133FQCx_vxoJhjjHm9CbgxwPBBSqe9auw"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
                    },
                ],
            },
            {
                "key": "1-3",
                "label": "대단원 평가하기",
                "children": [
                    {
                        "key": "1-3-1",
                        "label": "대단원 평가하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "대단원 평가하기",
                                "src": "https://drive.google.com/file/d/1CzgyQMHmO8gvnRlpOcW9StJp4nDB81Tp/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=1CzgyQMHmO8gvnRlpOcW9StJp4nDB81Tp"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
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
                        "label": "복소수와 그 연산",
                        "items": [
                            {
                                "type": "canva",
                                "title": "복소수",
                                "src": "https://www.canva.com/design/DAHE7Y54NZc/mHc_ORmkl8Dq8ktg41gGww/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🌀 복소수 정복! 용어 마스터",
                                "subject": "common",
                                "slug": "mini/complex_number_terms"
                            },
                            {
                                "type": "canva",
                                "title": "복소수의 상등",
                                "src": "https://www.canva.com/design/DAHE7fXzzbA/fR5NLflGzEZj9PxQWD4s0Q/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "복소수의 사칙연산",
                                "src": "https://www.canva.com/design/DAHE7feMZCQ/RZ7PX17_7b5e0F0jjDOpKA/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "⚡ 복소수 계산 배틀!",
                                "subject": "common",
                                "slug": "mini/complex_arithmetic_game"
                            },
                            {
                                "type": "activity",
                                "title": "🔄 허수단위 i의 순환 탐구",
                                "subject": "common",
                                "slug": "mini/imaginary_unit_cycle"
                            },
                            {
                                "type": "canva",
                                "title": "음수의 제곱근",
                                "src": "https://www.canva.com/design/DAHE7bz4Y8k/hBokecIfrDCrgKjL066XKA/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🚨 음수의 제곱근 함정 탈출!",
                                "subject": "common",
                                "slug": "mini/negative_sqrt_trap"
                            },
                        ],
                    },
                    {
                        "key": "2-1-2",
                        "label": "이차방정식의 판별식",
                        "items": [
                            {
                                "type": "canva",
                                "title": "이차방정식의 실근과 허근",
                                "src": "https://www.canva.com/design/DAHE7ZbcVqk/HOl66xoID5jUtOMoco6zIw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🔮 켤레근 탐정단!",
                                "subject": "common",
                                "slug": "mini/conjugate_roots_explorer"
                            },
                            {
                                "type": "canva",
                                "title": "이차방정식의 근의 판별",
                                "src": "https://www.canva.com/design/DAHE7eJoQMA/-k4-Gza3fyNMvL36jXriDg/view?embed",
                                "height": 800
                            },
                        ],
                    },
                    {
                        "key": "2-1-3",
                        "label": "이차방정식의 근과 계수의 관계",
                        "items": [
                            {
                                "type": "canva",
                                "title": "이차방정식의 근과 계수의 관계",
                                "src": "https://www.canva.com/design/DAHE7fwzHpE/CRIktU5PpLGtLQ8cjAh3cw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "두 수를 근으로 하는 이차방정식",
                                "src": "https://www.canva.com/design/DAHE7WZLuiM/fO7Mg0KWO-qAWXcCcQJKyw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "이차식의 인수분해",
                                "src": "https://www.canva.com/design/DAHE7WwixW4/gSt96iFCzcayYLyluWm-gg/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🔑 근과 계수의 관계 탐정단",
                                "subject": "common",
                                "slug": "mini/vieta_roots_game"
                            },
                        ],
                    },
                    {
                        "key": "2-1-4",
                        "label": "중단원 점검하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "중단원 마무리 문제",
                                "src": "https://drive.google.com/file/d/1F1fsHZYTIjpXP2KNlEL6HVGtj6satJ_k/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=1F1fsHZYTIjpXP2KNlEL6HVGtj6satJ_k"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
                    },
                ],
            },
            {
                "key": "2-2",
                "label": "(2) 이차방정식과 이차함수",
                "children": [
                    {
                        "key": "2-2-1",
                        "label": "이차함수의 그래프와 이차방정식",
                        "items": [
                            {
                                "type": "canva",
                                "title": "이차방정식과 이차함수의 관계",
                                "src": "https://www.canva.com/design/DAHE7ZmrZj4/WsFUKXwn4SK9xuDGectYGA/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "📈 이차함수·방정식 그래프 탐구",
                                "subject": "common",
                                "slug": "mini/quad_func_equation_explorer"
                            },
                            {
                                "type": "canva",
                                "title": "이차방정식의 그래프와 직선의 위치 관계",
                                "src": "https://www.canva.com/design/DAHE7ZMRi-s/1RnXe5hXXX1eOBJrecMJeg/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "📐 이차함수·직선 위치관계 실험실",
                                "subject": "common",
                                "slug": "mini/quad_line_position_explorer"
                            },
                        ],
                    },
                    {
                        "key": "2-2-2",
                        "label": "이차함수의 최대, 최소",
                        "items": [
                            {
                                "type": "canva",
                                "title": "이차함수의 최댓값과 최솟값",
                                "src": "https://www.canva.com/design/DAHE7ahKu-U/5aeRTEoegGPGYQPrnFjQag/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "제한된 범위에서 이차함수의 최대, 최소",
                                "src": "https://www.canva.com/design/DAHE7l6rADk/ByrggqhWTQFvOcGijaIaGA/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "📈 이차함수의 최대·최소 탐구 (미니활동)",
                                "slug": "mini/quad_maxmin_explorer",
                                "subject": "common",
                            },
                            {
                                "type": "activity",
                                "title": "🏗️ 이차함수 최대·최소 실생활 탐구 (미니활동)",
                                "slug": "mini/quad_maxmin_reallife",
                                "subject": "common",
                            },
                            {
                                "type": "activity",
                                "title": "🌉 다리에서 이차함수 찾기 (미니활동)",
                                "slug": "mini/quad_bridge_curve_fit",
                                "subject": "common",
                            },
                        ],
                    },
                    {
                        "key": "2-2-3",
                        "label": "중단원 점검하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "중단원 마무리 문제",
                                "src": "https://drive.google.com/file/d/15fVSyJmqeznQmz59U1TEYw6bdd_FVyv9/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=15fVSyJmqeznQmz59U1TEYw6bdd_FVyv9"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
                    },
                ],
            },
            {
                "key": "2-3",
                "label": "(3) 여러 가지 방정식과 부등식",
                "children": [
                    {
                        "key": "2-3-1",
                        "label": "삼차방정식과 사차방정식",
                        "items": [
                            {
                                "type": "canva",
                                "title": "삼차방정식과 사차방정식의 풀이",
                                "src": "https://www.canva.com/design/DAHHbyPhIYs/lsLR_Pm-rR__YK36OcU5eQ/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🔢 삼·사차방정식 풀이 탐구",
                                "subject": "common",
                                "slug": "mini/cubic_quartic_equation_explorer"
                            },
                            {
                                "type": "canva",
                                "title": "삼차방정식과 사차방정식의 활용",
                                "src": "https://www.canva.com/design/DAHHbxzHqBM/4GDOralpxhcXeYumy4vngA/view?embed",
                                "height": 800
                            },
                            {
                                "type": "activity",
                                "title": "🏺 바빌로니아인의 방정식 풀이",
                                "subject": "common",
                                "slug": "mini/babylonian_cubic_solver"
                            },
                            {
                                "type": "activity",
                                "title": "📜 방정식 해법의 역사",
                                "subject": "common",
                                "slug": "mini/equation_history_flash"
                            },
                            {
                                "type": "canva",
                                "title": "w-법칙",
                                "src": "https://www.canva.com/design/DAHHbyJLhtY/t8IhmlA4upQDfvON6Ns_FQ/view?embed",
                                "height": 800
                            },
                        ],
                    },
                    {
                        "key": "2-3-2",
                        "label": "연립이차방정식",
                        "items": [
                            {
                                "type": "canva",
                                "title": "미지수가 2개인 연립이차방정식",
                                "src": "https://www.canva.com/design/DAHHb5kNV0E/L2ivZ9Pjbvc8JGvuo7gwvw/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "2-3-3",
                        "label": "연립일차부등식",
                        "items": [
                            {
                                "type": "canva",
                                "title": "미지수가 1개인 연립일차부등식",
                                "src": "https://www.canva.com/design/DAHHb9jqa8Y/mo9f4Ug5I51hZdYMR7DQ-g/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "절댓값을 포함한 일차부등식",
                                "src": "https://www.canva.com/design/DAHHb8CZid4/GsuMyDU3dOwz751vtqsUxg/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "2-3-4",
                        "label": "이차부등식과 연립이차부등식",
                        "items": [
                            {
                                "type": "canva",
                                "title": "이차부등식과 이차함수의 그래프",
                                "src": "https://www.canva.com/design/DAHHbz03zgQ/rmNIom715GhwzWOkxiQaSQ/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "이차부등식의 해",
                                "src": "https://www.canva.com/design/DAHHb2VlOsk/xOY-27XtUEJLSqg7umpGuw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "연립이차부등식",
                                "src": "https://www.canva.com/design/DAHHb97cGSM/jkWhZ_wESwri1jWVyCNdHQ/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "2-3-5",
                        "label": "중단원 점검하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "중단원 마무리 문제",
                                "src": "https://drive.google.com/file/d/1hgaLWiQJykeYwNGd0fTiBHC7N8PjbFZc/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=1hgaLWiQJykeYwNGd0fTiBHC7N8PjbFZc"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
                    },
                ],
            },
            {
                "key": "2-4",
                "label": "대단원 평가하기",
                "children": [
                    {
                        "key": "2-4-1",
                        "label": "대단원 평가하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "대단원 평가하기",
                                "src": "https://drive.google.com/file/d/1timYD43ZracPLnhuWL2XRNpa2EavY0ia/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=1timYD43ZracPLnhuWL2XRNpa2EavY0ia"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
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
                        "items": [
                            {
                                "type": "canva",
                                "title": "합의 법칙",
                                "src": "https://www.canva.com/design/DAHHb314kpY/i0bcYzULGOHOIVP6lH07ow/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "곱의 법칙",
                                "src": "https://www.canva.com/design/DAHHb6IfcsU/4y09zB97RqVnLDwllsI0Tw/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "3-1-2",
                        "label": "순열",
                        "items": [
                            {
                                "type": "canva",
                                "title": "순열",
                                "src": "https://www.canva.com/design/DAHHbz68Whc/2SUTctbM_Lbyj3VYHPnpgg/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "계승",
                                "src": "https://www.canva.com/design/DAHHb07u12o/aq-lMHKzEYjpT0lr_FvXOA/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "3-1-3",
                        "label": "조합",
                        "items": [
                            {
                                "type": "canva",
                                "title": "조합",
                                "src": "https://www.canva.com/design/DAHHbwVkFrk/hC2D0U2rHWq0t7PN_R2xqw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "조합의 성질",
                                "src": "https://www.canva.com/design/DAHHb1kmgnw/bbS8YERDM__q_I_rzAqgGw/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "경우의 수 관련 활동",
                                "src": "https://www.canva.com/design/DAHHb_e10w8/ivJuDyifG4baDWLyP-y7jg/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "3-1-4",
                        "label": "중단원 점검하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "중단원 마무리 문제",
                                "src": "https://drive.google.com/file/d/10krBfUGNSiQ1zIHEneodCLUW7M1cYF2_/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=10krBfUGNSiQ1zIHEneodCLUW7M1cYF2_"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
                    },
                ],
            },
            {
                "key": "3-2",
                "label": "대단원 평가하기",
                "children": [
                    {
                        "key": "3-2-1",
                        "label": "대단원 평가하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "대단원 평가하기",
                                "src": "https://drive.google.com/file/d/1WnMPm0cknbDnpz3XjCKzMfvVY0e4AUCF/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=1WnMPm0cknbDnpz3XjCKzMfvVY0e4AUCF"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
                    },
                ],
            },
        ],
    },
    {
        "key": "4",
        "label": "[4] 행렬",
        "children": [
            {
                "key": "4-1",
                "label": "(1) 행렬과 그 연산",
                "children": [
                    {
                        "key": "4-1-1",
                        "label": "행렬의 뜻",
                        "items": [
                            {
                                "type": "canva",
                                "title": "행렬의 뜻",
                                "src": "https://www.canva.com/design/DAHHb01kNB0/pxxJqS1xQ7yeCBJ4kzF9zQ/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "행렬의 상등",
                                "src": "https://www.canva.com/design/DAHHb95LzP0/pqciQUO17pfhVG1G8ejdDA/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "4-1-2",
                        "label": "행렬의 덧셈과 뺄셈, 실수배",
                        "items": [
                            {
                                "type": "canva",
                                "title": "행렬의 덧셈",
                                "src": "https://www.canva.com/design/DAHHb1C-BsM/9uR7gp5SPjYxSk6uh2EJCQ/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "행렬의 뺄셈",
                                "src": "https://www.canva.com/design/DAHHb-hTRcY/IgIp03ne1WQUo78avIrRPg/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "행렬의 실수배",
                                "src": "https://www.canva.com/design/DAHHb5Z-Crw/bawSGqne4wR7H4EUEXGBVQ/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "4-1-3",
                        "label": "행렬의 곱셈",
                        "items": [
                            {
                                "type": "canva",
                                "title": "행렬의 곱셈",
                                "src": "https://www.canva.com/design/DAHHbw2oB4Y/XssuVNyVUSmqe-a9mauyPg/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "단위행렬",
                                "src": "https://www.canva.com/design/DAHHb-iwSlk/GVIsVzdXBEIM021Rhd6YQg/view?embed",
                                "height": 800
                            },
                            {
                                "type": "canva",
                                "title": "행렬 관련 활동",
                                "src": "https://www.canva.com/design/DAHHb7ei_6w/HMyIdZzwGqvG__ryj5Wr3w/view?embed",
                                "height": 800
                            }
                        ],
                    },
                    {
                        "key": "4-1-4",
                        "label": "중단원 점검하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "중단원 마무리 문제",
                                "src": "https://drive.google.com/file/d/1Ax1WNJnEshA2YXYjOaZpK19w-N6goGBG/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=1Ax1WNJnEshA2YXYjOaZpK19w-N6goGBG"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
                    },
                ],
            },
            {
                "key": "4-2",
                "label": "대단원 평가하기",
                "children": [
                    {
                        "key": "4-2-1",
                        "label": "대단원 평가하기",
                        "items": [
                            {
                                "type": "pdf",
                                "title": "대단원 평가하기",
                                "src": "https://drive.google.com/file/d/1Ecc7Lhm5UhHL7BFRoPKoZY1Fvk7VZH3p/preview",
                                #"height": 900,
                                "download": "https://drive.google.com/uc?export=download&id=1Ecc7Lhm5UhHL7BFRoPKoZY1Fvk7VZH3p"  # (선택) 다운로드 버튼 표시용
                            }
                        ],
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
