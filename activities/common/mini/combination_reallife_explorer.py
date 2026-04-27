# activities/common/mini/combination_reallife_explorer.py
"""
조합 실생활 탐구 — 6가지 실생활 사례로 조합 C(n,r) 개념을 인터랙티브하게 탐구하는 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "조합실생활탐구"

META = {
    "title":       "🎲 조합 실생활 탐구",
    "description": "부분집합·다각형·주번·팀 구성·메뉴·악수 6가지 사례를 직접 조작하며 조합 C(n,r)을 탐구합니다.",
    "order":       330,
    "hidden":      False,
}

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "조합개념",
        "label":  "① 조합이란 무엇인가요? 오늘 탐구한 사례를 바탕으로 조합의 특징을 나만의 말로 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "순열과차이",
        "label":  "② 조합과 순열의 차이는 무엇인가요? 주번 뽑기나 팀 구성 사례를 이용해 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "공식이해",
        "label":  "③ C(n,r) = n! / (r! × (n-r)!) 에서 분모에 r!을 나누는 이유는 무엇일까요?",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "신규사례",
        "label":  "④ 활동에서 다루지 않은 조합의 실생활 사례를 1가지 이상 직접 만들고 C(n,r)로 표현해보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "새롭게알게된점",
        "label":  "💡 이 활동을 통해 새롭게 알게 된 점",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "느낀점",
        "label":  "💬 이 활동을 하면서 느낀 점",
        "type":   "text_area",
        "height": 90,
    },
]

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(145deg,#060c1a,#0a1428,#050912);
  color:#dde8ff;padding:10px 12px 16px;
}
.hdr{text-align:center;padding:8px 0 12px}
.hdr-title{font-size:1.25rem;font-weight:700;color:#34d399;
  text-shadow:0 0 18px rgba(52,211,153,.4);margin-bottom:6px}
.formula-banner{display:inline-block;background:rgba(52,211,153,.06);
  border:1px solid rgba(52,211,153,.25);border-radius:10px;padding:5px 14px;
  font-size:.82rem;color:#34d399;font-family:'Courier New',monospace;letter-spacing:.5px}
.tabs{display:flex;flex-wrap:wrap;gap:4px;margin:0 0 10px;
  background:rgba(255,255,255,.04);border-radius:12px;padding:5px}
.tab{flex:1;min-width:70px;padding:7px 4px;border:none;border-radius:8px;
  font-family:inherit;font-size:.73rem;font-weight:600;cursor:pointer;
  background:transparent;color:#7788aa;transition:all .2s;line-height:1.35}
.tab:hover{color:#dde8ff;background:rgba(255,255,255,.06)}
.tab.active{background:rgba(52,211,153,.12);color:#34d399;border:1px solid rgba(52,211,153,.3)}
.panel{display:none}.panel.active{display:block;animation:fadein .25s ease}
@keyframes fadein{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.sc-title{font-size:1rem;font-weight:700;margin-bottom:5px}
.sc-sub{font-size:.78rem;color:#7788aa;margin-bottom:10px;line-height:1.6}
.vis{background:rgba(0,0,0,.3);border-radius:12px;padding:12px 10px;margin-bottom:9px;min-height:80px}
.frm{display:flex;align-items:center;gap:7px;background:rgba(52,211,153,.05);
  border:1px solid rgba(52,211,153,.2);border-radius:9px;padding:7px 11px;
  margin-bottom:8px;flex-wrap:wrap}
.frm-lbl{font-size:.75rem;color:#7788aa}
.frm-val{font-family:'Courier New',monospace;font-size:.88rem;color:#34d399;font-weight:700}
.btn{padding:6px 14px;border-radius:8px;border:1.5px solid rgba(255,255,255,.18);
  background:rgba(255,255,255,.06);color:#dde8ff;font-family:inherit;
  font-size:.8rem;cursor:pointer;transition:all .2s}
.btn:hover{background:rgba(255,255,255,.11);transform:translateY(-1px)}
.btn.green{background:rgba(52,211,153,.09);border-color:rgba(52,211,153,.35);color:#34d399}
.btn.green:hover{background:rgba(52,211,153,.18)}
.notice{background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.22);
  border-radius:8px;padding:7px 11px;font-size:.76rem;color:#6ee7b7;
  margin-top:6px;line-height:1.65}
.badge{display:inline-block;padding:4px 12px;border-radius:99px;
  background:linear-gradient(135deg,#059669,#047857);color:#ecfdf5;
  font-size:.78rem;font-weight:700;animation:pop .3s ease}
.sumtbl{width:100%;border-collapse:collapse;font-size:.76rem}
.sumtbl th{text-align:left;padding:5px 6px;color:#7788aa;
  border-bottom:1px solid rgba(255,255,255,.1)}
.sumtbl td{padding:5px 6px;border-bottom:1px solid rgba(255,255,255,.05)}
input[type=range]{accent-color:#34d399}
@keyframes pop{0%{transform:scale(.7)}60%{transform:scale(1.1)}100%{transform:scale(1)}}
/* ELEM */
.elem-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:14px}
.elem{display:inline-flex;align-items:center;justify-content:center;
  width:124px;height:124px;border-radius:24px;font-size:2.8rem;font-weight:700;
  cursor:pointer;border:2px solid rgba(255,255,255,.15);
  background:rgba(255,255,255,.05);transition:all .2s;user-select:none;color:#9ca3af}
.elem:hover{transform:translateY(-4px);background:rgba(52,211,153,.1)}
.elem.sel{background:rgba(52,211,153,.2);border-color:#34d399;color:#34d399;animation:pop .2s ease}
.elem.dis{opacity:.25;pointer-events:none}
/* STUDENT */
.stu-grid{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;padding:4px}
.stu{display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;user-select:none}
.stu:hover .stu-icon:not(.dis){transform:translateY(-4px)}
.stu-icon{width:100px;height:100px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:2.6rem;border:2px solid rgba(255,255,255,.15);
  background:rgba(255,255,255,.06);transition:all .3s}
.stu-icon.sel{border-color:#34d399;background:rgba(52,211,153,.2);animation:pop .25s ease}
.stu-icon.dis{opacity:.25;pointer-events:none}
.stu-name{font-size:.85rem;color:#6b7280}
/* FOOD */
.food-grid{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.food{display:flex;flex-direction:column;align-items:center;gap:5px;cursor:pointer;
  padding:12px 14px;border:2px solid rgba(255,255,255,.1);border-radius:14px;
  background:rgba(255,255,255,.04);min-width:110px;transition:all .2s;user-select:none}
.food:hover{transform:translateY(-4px);background:rgba(52,211,153,.08)}
.food.sel{border-color:#34d399;background:rgba(52,211,153,.18);animation:pop .2s ease}
.food.dis{opacity:.25;pointer-events:none}
.food-emoji{font-size:3.6rem}
.food-label{font-size:.82rem;color:#9ca3af;text-align:center}
.food.sel .food-label{color:#6ee7b7}
</style>
</head>
<body>

<div class="hdr">
  <div class="hdr-title">🎲 조합 실생활 탐구</div>
  <div class="formula-banner">C(n, r) = n! / (r! × (n−r)!) — 순서 없이 r개를 선택하는 방법</div>
</div>

<div class="tabs" id="tabBar">
  <button class="tab active" onclick="switchTab(0)">📦<br>부분집합</button>
  <button class="tab" onclick="switchTab(1)">📐<br>다각형</button>
  <button class="tab" onclick="switchTab(2)">📋<br>주번 뽑기</button>
  <button class="tab" onclick="switchTab(3)">👕<br>팀 구성</button>
  <button class="tab" onclick="switchTab(4)">🍱<br>메뉴 선택</button>
  <button class="tab" onclick="switchTab(5)">🤝<br>악수하기</button>
</div>

<!-- ══ PANEL 0: 부분집합 ══ -->
<div id="p0" class="panel active">
  <div class="sc-title">📦 부분집합 구하기</div>
  <div class="sc-sub">
    집합 {가, 나, 다, 라, 마} 에서 원소를 r개 고르는 부분집합의 수를 탐구합니다.<br>
    원소를 클릭해 r개를 선택해보세요! (순서는 상관없어요)
  </div>
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap">
    <span style="font-size:.8rem;color:#7788aa">선택할 원소 수 r =</span>
    <input type="range" id="p0r" min="1" max="5" value="2"
      oninput="document.getElementById('p0rv').textContent=this.value;p0Init()" style="width:100px">
    <span id="p0rv" style="background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);
      border-radius:6px;padding:2px 10px;font-size:.95rem;font-weight:700;color:#34d399">2</span>
    <span style="font-size:.78rem;color:#7788aa">개</span>
  </div>
  <div class="vis">
    <div style="font-size:.73rem;color:#7788aa;text-align:center;margin-bottom:10px">원소를 클릭해보세요</div>
    <div id="p0elems" class="elem-row"></div>
    <div style="text-align:center;margin-bottom:4px">
      <span style="font-size:.78rem;color:#7788aa">선택된 부분집합: </span>
      <span id="p0subset" style="font-size:1.05rem;font-weight:700;color:#34d399;
        font-family:'Courier New',monospace">{  }</span>
    </div>
    <div id="p0msg" style="text-align:center;margin-top:8px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">r개짜리 부분집합 수:</span>
    <span class="frm-val" id="p0frm">C(5,2) = 10가지</span>
  </div>
  <button class="btn" onclick="p0Init()">↩ 초기화</button>
  <div class="notice" style="margin-top:8px">
    💡 <strong>{가, 나}</strong>와 <strong>{나, 가}</strong>는 같은 부분집합! 조합에서는 <strong>어떤 원소를 골랐냐</strong>만 중요합니다.<br>
    순열과 달리 순서를 무시하므로 r! 배 적어집니다. → <strong id="p0notice_val">C(5,2) = 10가지</strong>
  </div>
</div>

<!-- ══ PANEL 1: 다각형 ══ -->
<div id="p1" class="panel">
  <div class="sc-title">📐 다각형의 개수</div>
  <div class="sc-sub">
    원 위의 6개 점 중 r개를 꼭짓점으로 하는 다각형의 수를 탐구합니다.<br>
    점을 클릭해 꼭짓점을 선택해보세요!
  </div>
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap">
    <span style="font-size:.8rem;color:#7788aa">꼭짓점 수 r =</span>
    <input type="range" id="p1r" min="3" max="5" value="3"
      oninput="document.getElementById('p1rv').textContent=this.value;p1Init()" style="width:80px">
    <span id="p1rv" style="background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);
      border-radius:6px;padding:2px 10px;font-size:.95rem;font-weight:700;color:#34d399">3</span>
    <span style="font-size:.78rem;color:#7788aa">개 (3=삼각형, 4=사각형, 5=오각형)</span>
  </div>
  <div class="vis" style="display:flex;flex-direction:column;align-items:center">
    <svg id="p1svg" width="340" height="320" viewBox="0 0 340 320" style="overflow:visible"></svg>
    <div id="p1msg" style="text-align:center;margin-top:6px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">만들 수 있는 다각형 수:</span>
    <span class="frm-val" id="p1frm">C(6,3) = 20가지 삼각형</span>
  </div>
  <button class="btn" onclick="p1Reset()">↩ 다시하기</button>
  <div class="notice" style="margin-top:8px">
    💡 꼭짓점을 고르는 <strong>순서는 관계없어요</strong>. A→B→C와 C→B→A는 같은 삼각형!<br>
    6개 점 중 3개 선택: <strong>C(6,3) = 20가지</strong> 삼각형, 4개 선택: <strong>C(6,4) = 15가지</strong> 사각형.
  </div>
</div>

<!-- ══ PANEL 2: 주번 뽑기 ══ -->
<div id="p2" class="panel">
  <div class="sc-title">📋 주번 뽑기</div>
  <div class="sc-sub">
    학급에서 주번 2명을 뽑는 경우의 수를 탐구합니다.<br>
    학생을 클릭해 주번 2명을 선택하세요! (누가 1번·2번 주번인지는 상관없어요)
  </div>
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap">
    <span style="font-size:.8rem;color:#7788aa">학급 인원 n =</span>
    <input type="range" id="p2n" min="4" max="12" value="6"
      oninput="document.getElementById('p2nv').textContent=this.value;p2Init()" style="width:110px">
    <span id="p2nv" style="background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);
      border-radius:6px;padding:2px 10px;font-size:.95rem;font-weight:700;color:#34d399">6</span>
    <span style="font-size:.78rem;color:#7788aa">명</span>
  </div>
  <div class="vis">
    <div style="font-size:.73rem;color:#7788aa;text-align:center;margin-bottom:8px">학생을 클릭해 주번 2명을 선택하세요</div>
    <div id="p2grid" class="stu-grid"></div>
    <div id="p2msg" style="text-align:center;margin-top:10px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">주번 선출 방법:</span>
    <span class="frm-val" id="p2frm">C(6,2) = 15가지</span>
  </div>
  <button class="btn" onclick="p2Init()">↩ 다시하기</button>
  <div class="notice" style="margin-top:8px">
    💡 {민준, 서연}과 {서연, 민준}은 같은 주번 조합! 순서 없이 고르는 것이 조합이에요.<br>
    순열 P(n,2) = n×(n-1)에서 <strong>2! = 2로 나누면</strong> → <strong>C(n,2) = n×(n-1)/2</strong>
  </div>
</div>

<!-- ══ PANEL 3: 팀 구성 ══ -->
<div id="p3" class="panel">
  <div class="sc-title">👕 팀 구성하기</div>
  <div class="sc-sub">
    8명 중 r명으로 팀을 구성하는 경우의 수를 탐구합니다.<br>
    팀원을 클릭해 선택해보세요!
  </div>
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap">
    <span style="font-size:.8rem;color:#7788aa">팀 인원 r =</span>
    <input type="range" id="p3r" min="2" max="6" value="3"
      oninput="document.getElementById('p3rv').textContent=this.value;p3Init()" style="width:100px">
    <span id="p3rv" style="background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);
      border-radius:6px;padding:2px 10px;font-size:.95rem;font-weight:700;color:#34d399">3</span>
    <span style="font-size:.78rem;color:#7788aa">명</span>
  </div>
  <div class="vis">
    <div style="font-size:.73rem;color:#7788aa;text-align:center;margin-bottom:8px">팀원을 클릭해 선택하세요</div>
    <div id="p3grid" class="stu-grid"></div>
    <div id="p3msg" style="text-align:center;margin-top:10px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">팀 구성 방법:</span>
    <span class="frm-val" id="p3frm">C(8,3) = 56가지</span>
  </div>
  <button class="btn" onclick="p3Init()">↩ 다시하기</button>
  <div class="notice" style="margin-top:8px">
    💡 팀에서는 누가 몇 번째로 뽑혔는지 중요하지 않아요. 같은 사람들 = 같은 팀!<br>
    8명 중 3명: <strong>C(8,3) = 56가지</strong> — 생각보다 훨씬 많죠?
  </div>
</div>

<!-- ══ PANEL 4: 메뉴 선택 ══ -->
<div id="p4" class="panel">
  <div class="sc-title">🍱 급식 반찬 선택하기</div>
  <div class="sc-sub">
    오늘 급식! 7가지 반찬 중 3가지를 선택하는 경우의 수를 탐구합니다.<br>
    원하는 반찬을 3가지 골라보세요!
  </div>
  <div class="vis">
    <div style="font-size:.73rem;color:#7788aa;text-align:center;margin-bottom:10px">반찬을 클릭해 3가지를 선택하세요</div>
    <div id="p4foods" class="food-grid"></div>
    <div id="p4msg" style="text-align:center;margin-top:10px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">반찬 선택 조합:</span>
    <span class="frm-val">C(7,3) = 35가지</span>
  </div>
  <button class="btn" onclick="p4Reset()">↩ 다시하기</button>
  <div class="notice" style="margin-top:8px">
    💡 김치→된장→샐러드나 샐러드→된장→김치나 <strong>담는 순서는 달라도 같은 급식</strong>이에요!<br>
    7가지 중 3가지: <strong>C(7,3) = 35가지</strong> 급식 메뉴 조합이 나와요.
  </div>
</div>

<!-- ══ PANEL 5: 악수 ══ -->
<div id="p5" class="panel">
  <div class="sc-title">🤝 모임에서 악수하기</div>
  <div class="sc-sub">
    n명이 모여 서로 한 번씩 악수할 때 총 악수 횟수를 탐구합니다.<br>
    인원을 조절하고 '악수 시작!'을 눌러보세요!
  </div>
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap">
    <span style="font-size:.8rem;color:#7788aa">모임 인원 n =</span>
    <input type="range" id="p5n" min="3" max="8" value="5"
      oninput="document.getElementById('p5nv').textContent=this.value;p5Update()" style="width:100px">
    <span id="p5nv" style="background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);
      border-radius:6px;padding:2px 10px;font-size:.95rem;font-weight:700;color:#34d399">5</span>
    <span style="font-size:.78rem;color:#7788aa">명</span>
  </div>
  <div class="vis" style="display:flex;flex-direction:column;align-items:center">
    <svg id="p5svg" width="320" height="300" viewBox="0 0 320 300"></svg>
    <div style="margin-top:8px;display:flex;gap:8px">
      <button class="btn green" onclick="p5Animate()">🤝 악수 시작!</button>
      <button class="btn" onclick="p5Reset()">↩ 초기화</button>
    </div>
    <div id="p5count" style="text-align:center;margin-top:10px;min-height:28px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">총 악수 횟수:</span>
    <span class="frm-val" id="p5frm">C(5,2) = 10번</span>
  </div>
  <div class="notice">
    💡 A와 B의 악수 = B와 A의 악수 → <strong>순서 없는 2명 선택 = 조합</strong>!<br>
    n명 모임의 악수 횟수 = <strong>C(n,2) = n×(n-1)/2</strong> — 인원이 늘수록 폭발적으로 증가해요.
  </div>
</div>

<!-- ══ SUMMARY ══ -->
<div style="margin-top:14px;background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:11px">
  <div style="font-size:.88rem;font-weight:700;color:#34d399;margin-bottom:8px">
    📊 탐구한 조합 사례 한눈에 보기
  </div>
  <table class="sumtbl">
    <thead>
      <tr>
        <th>사례</th>
        <th style="text-align:center">C(n,r)</th>
        <th style="text-align:center">계산</th>
        <th style="text-align:right">결과</th>
      </tr>
    </thead>
    <tbody style="color:#b8c8de">
      <tr><td>📦 5개 원소 중 2개 부분집합</td>
        <td style="text-align:center;font-family:'Courier New';color:#34d399">C(5,2)</td>
        <td style="text-align:center">5×4 / 2×1</td>
        <td style="text-align:right;font-weight:700;color:#34d399">10가지</td></tr>
      <tr><td>📐 6개 점 중 3개로 삼각형</td>
        <td style="text-align:center;font-family:'Courier New';color:#34d399">C(6,3)</td>
        <td style="text-align:center">6×5×4 / 3×2×1</td>
        <td style="text-align:right;font-weight:700;color:#34d399">20가지</td></tr>
      <tr><td>📋 6명 중 주번 2명</td>
        <td style="text-align:center;font-family:'Courier New';color:#34d399">C(6,2)</td>
        <td style="text-align:center">6×5 / 2×1</td>
        <td style="text-align:right;font-weight:700;color:#34d399">15가지</td></tr>
      <tr><td>👕 8명 중 팀원 3명</td>
        <td style="text-align:center;font-family:'Courier New';color:#34d399">C(8,3)</td>
        <td style="text-align:center">8×7×6 / 3×2×1</td>
        <td style="text-align:right;font-weight:700;color:#34d399">56가지</td></tr>
      <tr><td>🍱 7가지 반찬 중 3가지 선택</td>
        <td style="text-align:center;font-family:'Courier New';color:#34d399">C(7,3)</td>
        <td style="text-align:center">7×6×5 / 3×2×1</td>
        <td style="text-align:right;font-weight:700;color:#34d399">35가지</td></tr>
      <tr><td>🤝 5명이 서로 한 번씩 악수</td>
        <td style="text-align:center;font-family:'Courier New';color:#34d399">C(5,2)</td>
        <td style="text-align:center">5×4 / 2×1</td>
        <td style="text-align:right;font-weight:700;color:#34d399">10번</td></tr>
    </tbody>
  </table>
</div>

<script>
// ─── UTILS ────────────────────────────────────────────────
function comb(n, r) {
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  r = Math.min(r, n - r);
  let v = 1;
  for (let i = 0; i < r; i++) v = v * (n - i) / (i + 1);
  return Math.round(v);
}
function switchTab(i) {
  document.querySelectorAll('.tab').forEach((t,j) => t.classList.toggle('active', i===j));
  document.querySelectorAll('.panel').forEach((p,j) => p.classList.toggle('active', i===j));
}

// ─── P0: 부분집합 ─────────────────────────────────────────
const P0E = ['가','나','다','라','마'];
let p0sel = new Set(), p0r = 2;

function p0Init() {
  p0r = parseInt(document.getElementById('p0r').value);
  p0sel = new Set();
  document.getElementById('p0msg').innerHTML = '';
  const c = comb(5, p0r);
  document.getElementById('p0frm').textContent = `C(5,${p0r}) = ${c}가지`;
  document.getElementById('p0notice_val').textContent = `C(5,${p0r}) = ${c}가지`;
  p0Render();
}

function p0Render() {
  const canAdd = p0sel.size < p0r;
  document.getElementById('p0elems').innerHTML = P0E.map((e, i) => {
    const s = p0sel.has(i), d = !s && !canAdd;
    return `<div class="elem${s?' sel':''}${d?' dis':''}" onclick="p0Toggle(${i})">${e}</div>`;
  }).join('');
  const arr = [...p0sel].sort().map(i => P0E[i]);
  document.getElementById('p0subset').textContent = arr.length ? `{ ${arr.join(', ')} }` : '{  }';
  if (p0sel.size === p0r) {
    const c = comb(5, p0r);
    document.getElementById('p0msg').innerHTML =
      `<span class="badge">✅ 부분집합 완성! C(5,${p0r})=${c}가지 중 하나예요</span>`;
  } else if (p0sel.size > 0) {
    document.getElementById('p0msg').innerHTML =
      `<span style="font-size:.76rem;color:#7788aa">${p0sel.size}/${p0r}개 선택됨</span>`;
  }
}

function p0Toggle(i) {
  if (p0sel.has(i)) { p0sel.delete(i); document.getElementById('p0msg').innerHTML = ''; }
  else { if (p0sel.size >= p0r) return; p0sel.add(i); }
  p0Render();
}
p0Init();

// ─── P1: 다각형 ──────────────────────────────────────────
let p1sel = new Set(), p1r = 3;
const P1LABELS = ['A','B','C','D','E','F'];

function p1Init() {
  p1r = parseInt(document.getElementById('p1r').value);
  p1sel = new Set();
  document.getElementById('p1msg').innerHTML = '';
  const c = comb(6, p1r);
  const names = {3:'삼각형',4:'사각형',5:'오각형'};
  document.getElementById('p1frm').textContent = `C(6,${p1r}) = ${c}가지 ${names[p1r]||p1r+'각형'}`;
  p1Render();
}

function p1Reset() { p1Init(); }

function p1Render() {
  const svg = document.getElementById('p1svg');
  const cx = 170, cy = 155, R = 125;
  const pts = Array.from({length:6}, (_, i) => {
    const a = i * 2 * Math.PI / 6 - Math.PI / 2;
    return { x: cx + R * Math.cos(a), y: cy + R * Math.sin(a) };
  });
  const canAdd = p1sel.size < p1r;

  // Outer circle guide
  let out = `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none"
    stroke="rgba(255,255,255,.06)" stroke-width="1" stroke-dasharray="4 4"/>`;

  // Filled polygon
  let poly = '';
  if (p1sel.size === p1r) {
    const sp = [...p1sel].sort((a,b)=>a-b).map(i => `${pts[i].x},${pts[i].y}`).join(' ');
    poly = `<polygon points="${sp}" fill="rgba(52,211,153,.15)"
      stroke="#34d399" stroke-width="2.5" stroke-linejoin="round"/>`;
  } else if (p1sel.size >= 2) {
    const sorted = [...p1sel].sort((a,b)=>a-b);
    let d = `M ${pts[sorted[0]].x} ${pts[sorted[0]].y}`;
    for (let k = 1; k < sorted.length; k++) d += ` L ${pts[sorted[k]].x} ${pts[sorted[k]].y}`;
    poly = `<path d="${d}" fill="none" stroke="rgba(52,211,153,.4)" stroke-width="2" stroke-dasharray="6 4"/>`;
  }

  // Points
  const circles = pts.map((p, i) => {
    const s = p1sel.has(i), d = !s && !canAdd;
    return `<g style="cursor:${d?'default':'pointer'}" onclick="${d?'':' p1Toggle('+i+')'}">
      <circle cx="${p.x}" cy="${p.y}" r="36" fill="transparent"/>
      <circle cx="${p.x}" cy="${p.y}" r="26"
        fill="${s?'rgba(52,211,153,.25)':'rgba(255,255,255,.07)'}"
        stroke="${s?'#34d399':'rgba(255,255,255,.2)'}" stroke-width="${s?2.5:1.5}"
        opacity="${d?.3:1}"/>
      <text x="${p.x}" y="${p.y+8}" text-anchor="middle" font-size="20" font-weight="700"
        fill="${s?'#34d399':d?'#374151':'#9ca3af'}" font-family="inherit">${P1LABELS[i]}</text>
    </g>`;
  }).join('');

  svg.innerHTML = out + poly + circles;

  if (p1sel.size === p1r) {
    const c = comb(6, p1r);
    const names = {3:'삼각형',4:'사각형',5:'오각형'};
    const nm = names[p1r]||p1r+'각형';
    const lbl = [...p1sel].sort((a,b)=>a-b).map(i=>P1LABELS[i]).join('');
    document.getElementById('p1msg').innerHTML =
      `<span class="badge">✅ ${nm} ${lbl} 완성! C(6,${p1r})=${c}가지 중 하나!</span>`;
  } else if (p1sel.size > 0) {
    document.getElementById('p1msg').innerHTML =
      `<span style="font-size:.76rem;color:#7788aa">${p1sel.size}/${p1r}개 선택됨</span>`;
  }
}

function p1Toggle(i) {
  if (p1sel.has(i)) { p1sel.delete(i); document.getElementById('p1msg').innerHTML = ''; }
  else { if (p1sel.size >= p1r) return; p1sel.add(i); }
  p1Render();
}
p1Init();

// ─── P2: 주번 뽑기 ───────────────────────────────────────
const STU_E = ['👦','👧','🧑','👱','🧒','👩','🧔','🧕','👮','🧙','🎓','🧑‍🏫'];
const STU_N = ['민준','서연','지우','예린','준혁','수아','태양','하늘','도현','별이','유찬','미래'];
let p2sel = new Set(), p2n = 6;

function p2Init() {
  p2n = parseInt(document.getElementById('p2n').value);
  p2sel = new Set();
  document.getElementById('p2msg').innerHTML = '';
  const c = comb(p2n, 2);
  document.getElementById('p2frm').textContent =
    `C(${p2n},2) = ${p2n}×${p2n-1}/2 = ${c}가지`;
  p2Render();
}

function p2Render() {
  const canAdd = p2sel.size < 2;
  document.getElementById('p2grid').innerHTML = Array.from({length: p2n}, (_, i) => {
    const s = p2sel.has(i), d = !s && !canAdd;
    return `<div class="stu" onclick="${d?'':'p2Toggle('+i+')'}">
      <div class="stu-icon${s?' sel':''}${d?' dis':''}">${STU_E[i]}</div>
      <div class="stu-name">${STU_N[i]}</div>
    </div>`;
  }).join('');
  if (p2sel.size === 2) {
    const [a,b] = [...p2sel].sort((x,y)=>x-y);
    const c = comb(p2n, 2);
    document.getElementById('p2msg').innerHTML =
      `<span class="badge">📋 주번: ${STU_E[a]} ${STU_N[a]} + ${STU_E[b]} ${STU_N[b]} — C(${p2n},2)=${c}가지 중 하나!</span>`;
  } else if (p2sel.size > 0) {
    document.getElementById('p2msg').innerHTML =
      `<span style="font-size:.76rem;color:#7788aa">1/2명 선택됨 — 한 명 더 선택하세요</span>`;
  }
}

function p2Toggle(i) {
  if (p2sel.has(i)) { p2sel.delete(i); document.getElementById('p2msg').innerHTML = ''; }
  else { if (p2sel.size >= 2) return; p2sel.add(i); }
  p2Render();
}
p2Init();

// ─── P3: 팀 구성 ─────────────────────────────────────────
const P3E = ['🏃','🤸','🏋️','🧗','🤾','🏊','🤼','🥋'];
const P3N = ['이슬','준서','하린','민찬','유진','소이','정훈','채원'];
const P3C = ['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#06b6d4','#ec4899','#f97316'];
let p3sel = new Set(), p3r = 3;

function p3Init() {
  p3r = parseInt(document.getElementById('p3r').value);
  p3sel = new Set();
  document.getElementById('p3msg').innerHTML = '';
  const c = comb(8, p3r);
  document.getElementById('p3frm').textContent = `C(8,${p3r}) = ${c}가지`;
  p3Render();
}

function p3Render() {
  const canAdd = p3sel.size < p3r;
  document.getElementById('p3grid').innerHTML = Array.from({length:8}, (_, i) => {
    const s = p3sel.has(i), d = !s && !canAdd;
    const borderStyle = s ? `border-color:${P3C[i]};` : '';
    return `<div class="stu" onclick="${d?'':'p3Toggle('+i+')'}">
      <div class="stu-icon${s?' sel':''}${d?' dis':''}" style="${borderStyle}">${P3E[i]}</div>
      <div class="stu-name">${P3N[i]}</div>
    </div>`;
  }).join('');
  if (p3sel.size === p3r) {
    const c = comb(8, p3r);
    const members = [...p3sel].sort((a,b)=>a-b).map(i=>P3E[i]+P3N[i]).join(' · ');
    document.getElementById('p3msg').innerHTML =
      `<span class="badge">👕 팀 완성: ${members} — C(8,${p3r})=${c}가지 중 하나!</span>`;
  } else if (p3sel.size > 0) {
    document.getElementById('p3msg').innerHTML =
      `<span style="font-size:.76rem;color:#7788aa">${p3sel.size}/${p3r}명 선택됨</span>`;
  }
}

function p3Toggle(i) {
  if (p3sel.has(i)) { p3sel.delete(i); document.getElementById('p3msg').innerHTML = ''; }
  else { if (p3sel.size >= p3r) return; p3sel.add(i); }
  p3Render();
}
p3Init();

// ─── P4: 메뉴 선택 ───────────────────────────────────────
const FOODS = [
  {e:'🥬',n:'시금치나물'},{e:'🥚',n:'계란찜'},
  {e:'🥩',n:'제육볶음'},{e:'🥗',n:'샐러드'},
  {e:'🧆',n:'두부조림'},{e:'🌽',n:'옥수수콘'},
  {e:'🥒',n:'오이무침'},
];
let p4sel = new Set();

function p4Reset() {
  p4sel = new Set();
  document.getElementById('p4msg').innerHTML = '';
  p4Render();
}

function p4Render() {
  const canAdd = p4sel.size < 3;
  document.getElementById('p4foods').innerHTML = FOODS.map((f, i) => {
    const s = p4sel.has(i), d = !s && !canAdd;
    return `<div class="food${s?' sel':''}${d?' dis':''}" onclick="${d?'':'p4Toggle('+i+')'}">
      <div class="food-emoji">${f.e}</div>
      <div class="food-label">${f.n}</div>
    </div>`;
  }).join('');
  if (p4sel.size === 3) {
    const chosen = [...p4sel].map(i=>FOODS[i].e+' '+FOODS[i].n).join(', ');
    document.getElementById('p4msg').innerHTML =
      `<span class="badge">🍱 오늘의 반찬: ${chosen} — C(7,3)=35가지 중 하나!</span>`;
  } else if (p4sel.size > 0) {
    document.getElementById('p4msg').innerHTML =
      `<span style="font-size:.76rem;color:#7788aa">${p4sel.size}/3가지 선택됨</span>`;
  }
}

function p4Toggle(i) {
  if (p4sel.has(i)) { p4sel.delete(i); document.getElementById('p4msg').innerHTML = ''; }
  else { if (p4sel.size >= 3) return; p4sel.add(i); }
  p4Render();
}
p4Reset();

// ─── P5: 악수하기 ────────────────────────────────────────
let p5n = 5, p5idx = 0, p5pairs = [], p5tmr = null;
const P5PERSON_E = ['👦','👧','🧑','👱','🧒','👩','🧔','🧕'];

function p5Update() {
  p5n = parseInt(document.getElementById('p5n').value);
  clearTimeout(p5tmr);
  p5pairs = [];
  document.getElementById('p5count').innerHTML = '';
  const c = comb(p5n, 2);
  document.getElementById('p5frm').textContent = `C(${p5n},2) = ${p5n}×${p5n-1}/2 = ${c}번`;
  p5Draw(new Set());
}

function p5Draw(shownSet) {
  const svg = document.getElementById('p5svg');
  const cx = 160, cy = 145, R = 115;
  const pts = Array.from({length: p5n}, (_, i) => {
    const a = i * 2 * Math.PI / p5n - Math.PI / 2;
    return { x: cx + R * Math.cos(a), y: cy + R * Math.sin(a) };
  });
  let lines = '';
  for (let i = 0; i < p5n; i++) {
    for (let j = i+1; j < p5n; j++) {
      const key = `${i}-${j}`, shown = shownSet.has(key);
      lines += `<line x1="${pts[i].x}" y1="${pts[i].y}" x2="${pts[j].x}" y2="${pts[j].y}"
        stroke="${shown?'#34d399':'rgba(255,255,255,.05)'}"
        stroke-width="${shown?2.5:1}" opacity="${shown?.75:.4}"/>`;
    }
  }
  const people = pts.map((p, i) =>
    `<circle cx="${p.x}" cy="${p.y}" r="26"
      fill="rgba(52,211,153,.15)" stroke="#34d399" stroke-width="2"/>
     <text x="${p.x}" y="${p.y+8}" text-anchor="middle" font-size="20"
      fill="#6ee7b7" font-family="inherit" font-weight="700">${i+1}</text>`
  ).join('');
  svg.innerHTML = lines + people;
}

function p5Animate() {
  clearTimeout(p5tmr);
  p5pairs = [];
  for (let i = 0; i < p5n; i++)
    for (let j = i+1; j < p5n; j++)
      p5pairs.push(`${i}-${j}`);
  p5idx = 0;
  p5Step();
}

function p5Step() {
  const shown = new Set(p5pairs.slice(0, p5idx));
  p5Draw(shown);
  const c = comb(p5n, 2);
  if (p5idx < p5pairs.length) {
    document.getElementById('p5count').innerHTML =
      `<span style="font-size:.78rem;color:#7788aa">악수 횟수: </span>` +
      `<span style="font-size:1.2rem;font-weight:700;color:#34d399">${p5idx} / ${c}</span>`;
    p5idx++;
    p5tmr = setTimeout(p5Step, 280);
  } else {
    document.getElementById('p5count').innerHTML =
      `<span style="font-size:.78rem;color:#7788aa">악수 횟수: </span>` +
      `<span style="font-size:1.2rem;font-weight:700;color:#34d399">${c} / ${c}</span>` +
      `<span class="badge" style="margin-left:8px">🤝 총 ${c}번! C(${p5n},2) 완성!</span>`;
  }
}

function p5Reset() {
  clearTimeout(p5tmr);
  document.getElementById('p5count').innerHTML = '';
  p5Draw(new Set());
}

p5Update();
</script>
</body>
</html>"""


def render():
    st.markdown("### 🎲 조합 실생활 탐구")
    st.markdown(
        "실생활 속 **6가지 조합 사례**를 직접 조작하며 **C(n, r)** 의 의미를 탐구해보세요!"
    )
    components.html(_HTML, height=1700, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
