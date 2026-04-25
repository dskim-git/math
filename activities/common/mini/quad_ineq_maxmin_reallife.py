# activities/common/mini/quad_ineq_maxmin_reallife.py
"""
최댓값·최솟값을 구하는 실생활 문제 탐구 (표 vs 수식)
볼펜 판매가·카페 아메리카노·주차장 요금 3가지 실생활 상황에서
표(스프레드시트)로 탐색하는 방법과 함수 식을 세워 해결하는 방법을 비교하며
다양한 문제 해결 전략을 체험하는 미니활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "이차부등식최대최소실생활"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "표_방법_장단점",
        "label":  "① 표(스프레드시트)로 최댓값을 찾는 방법의 장점과 단점을 각각 설명해 보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "수식_방법_장단점",
        "label":  "② 변수를 설정하고 이차함수 식을 세워 최댓값을 구하는 방법의 장점과 단점을 각각 설명해 보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "두_방법_비교",
        "label":  "③ 두 방법(표 vs 수식)을 비교했을 때, 어떤 상황에서 각각의 방법이 더 유용할까요? 실제 예를 들어 설명해 보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "변수_설정_중요성",
        "label":  "④ 세 문제 모두 '판매가를 x원 낮춘다' 또는 '요금을 x원 낮춘다'처럼 변수를 설정했습니다. 이처럼 변화량을 x로 놓는 전략이 왜 편리한지 설명해 보세요.",
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

META = {
    "title":       "🛒 최댓값 찾기: 표 vs 수식",
    "description": "볼펜·아메리카노·주차장 3가지 실생활 상황에서 표(스프레드시트)로 탐색하는 방법과 이차함수 식을 세워 해결하는 방법을 비교하며 다양한 문제 해결 전략을 체험합니다.",
    "order":       292,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>최댓값 찾기: 표 vs 수식</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(155deg,#060917 0%,#0e1630 60%,#080f1c 100%);
  color:#e2e8ff;
  padding:10px 12px 16px;
  overflow-x:hidden;
}
/* ── 탭 ── */
.tabs{display:flex;gap:4px;border-bottom:2px solid #1e3060;margin-bottom:0;flex-wrap:wrap}
.tab-btn{padding:7px 12px;border:none;border-radius:9px 9px 0 0;background:#0a1020;color:#556688;cursor:pointer;font-size:.8rem;font-family:inherit;transition:all .2s;border-bottom:2px solid transparent;margin-bottom:-2px;white-space:nowrap}
.tab-btn:hover{background:#131e38;color:#99aacc}
.tab-btn.active{background:#151f3a;color:#ffd700;border-bottom:2px solid #ffd700;font-weight:700}
.tab-panel{display:none;padding-top:10px}
.tab-panel.active{display:block}

/* ── 문제 카드 ── */
.problem-card{
  background:linear-gradient(135deg,#0d1a38,#131e30);
  border:1px solid #2e4070;border-radius:12px;
  padding:14px 16px;margin-bottom:12px;
}
.problem-title{font-size:1rem;font-weight:700;color:#ffd700;margin-bottom:8px}
.problem-body{font-size:.85rem;line-height:1.75;color:#c0d0ee}
.problem-body strong{color:#77ccff}
.problem-formula{
  background:#040a18;border-left:3px solid #4488ff;
  padding:8px 12px;border-radius:0 8px 8px 0;
  font-size:.88rem;color:#88ccff;margin:8px 0;font-style:italic;
}
.ask{
  background:#0a1828;border:1px dashed #ffd700;border-radius:8px;
  padding:8px 12px;margin-top:8px;font-size:.85rem;color:#ffe080;font-weight:600;
}

/* ── 2열 레이아웃 ── */
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
@media(max-width:700px){.two-col{grid-template-columns:1fr}}

/* ── 방법 패널 공통 ── */
.method-panel{
  background:#080f20;border:1px solid #1e3060;border-radius:10px;
  padding:12px;display:flex;flex-direction:column;gap:8px;
}
.method-title{
  font-size:.88rem;font-weight:700;padding:4px 10px;border-radius:6px;
  display:inline-block;margin-bottom:4px;
}
.method-a .method-title{background:#1a3a1a;color:#66ff88}
.method-b .method-title{background:#1a1a3a;color:#88aaff}

/* ── 인터랙티브 표 (방법 A) ── */
.table-wrap{overflow-x:auto;overflow-y:auto;max-height:200px;border-radius:8px}
table{border-collapse:collapse;width:100%;min-width:240px;font-size:.78rem}
thead tr{background:#0d1e38}
th{padding:5px 8px;color:#88aaff;text-align:center;border-bottom:2px solid #1e3060;white-space:nowrap}
td{padding:4px 7px;text-align:center;border-bottom:1px solid #0d1828;color:#c0d0e0;transition:background .15s}
tr.highlight td{background:#1a3a10;color:#66ff88;font-weight:700}
tr.near-max td{background:#2a3a10;color:#aaddaa}
.table-hint{font-size:.75rem;color:#556688;margin-top:5px;text-align:center}

/* 표 탐색 슬라이더 */
.slider-section{display:flex;flex-direction:column;gap:4px;margin-bottom:6px}
.slider-row{display:flex;align-items:center;gap:8px}
.slider-lbl{font-size:.78rem;color:#99aacc;white-space:nowrap;min-width:60px}
input[type=range]{flex:1;accent-color:#27ae60;cursor:pointer}
.slider-val{font-size:.85rem;font-weight:700;color:#66ff88;min-width:60px;text-align:right;white-space:nowrap}
.table-result{
  font-size:.82rem;font-weight:700;color:#66ff88;
  background:#0a1a0a;border:1px solid #1a4a1a;border-radius:6px;
  padding:5px 10px;text-align:center;
}

/* ── 수식 풀이 (방법 B) ── */
.step-list{display:flex;flex-direction:column;gap:1px}
.step-item{background:#06101e;border-bottom:1px solid #0d1828;cursor:pointer;transition:background .15s;border-radius:0}
.step-item:first-child{border-radius:8px 8px 0 0}
.step-item:last-child{border-radius:0 0 8px 8px;border-bottom:none}
.step-item:hover{background:#0a1628}
.step-hdr{display:flex;align-items:center;gap:7px;padding:7px 10px}
.step-num{width:20px;height:20px;border-radius:50%;font-weight:700;font-size:.72rem;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.s1 .step-num{background:#e74c3c;color:#fff}
.s2 .step-num{background:#e67e22;color:#fff}
.s3 .step-num{background:#d4ac0d;color:#111}
.s4 .step-num{background:#27ae60;color:#fff}
.s5 .step-num{background:#2980b9;color:#fff}
.s6 .step-num{background:#9b59b6;color:#fff}
.step-htxt{font-size:.78rem;color:#b0c0e0;font-weight:600;flex:1}
.step-arr{color:#445577;transition:transform .2s;font-size:.65rem}
.step-item.open .step-arr{transform:rotate(180deg)}
.step-body{display:none;padding:6px 10px 9px 37px;font-size:.77rem;color:#99aacc;line-height:1.7;border-top:1px solid #0d1828}
.step-item.open .step-body{display:block}
.hi{color:#ffd700;font-weight:700}
.formula{font-family:'Courier New',monospace;background:#040a14;padding:4px 9px;border-radius:5px;margin:4px 0;font-size:.8rem;color:#66ffcc;border-left:2px solid #27ae60;display:block}

/* 빈칸 입력 */
.q-box{background:#030810;border:1px dashed #2a4878;border-radius:7px;padding:7px 10px;margin-top:6px}
.q-label{display:block;font-size:.76rem;color:#88ccff;font-weight:700;margin-bottom:4px}
.q-row{display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin-top:2px}
.q-text{font-size:.78rem;color:#aabbdd}
.q-input{width:64px;padding:3px 5px;background:#070e1c;border:1.5px solid #336699;border-radius:5px;color:#e2e8ff;font-size:.84rem;text-align:center;font-family:inherit}
.q-input:focus{outline:none;border-color:#77aaee}
.q-input.ok{border-color:#27ae60;color:#66ffcc;background:#040e08}
.q-input.err{border-color:#e74c3c}
.q-btn{padding:3px 9px;background:#1a3560;border:none;border-radius:5px;color:#88aaff;cursor:pointer;font-family:inherit;font-size:.75rem;font-weight:700;transition:all .2s;white-space:nowrap}
.q-btn:hover{background:#234580;color:#aaccff}
.mc-opts{display:flex;gap:4px;flex-wrap:wrap;margin-top:5px}
.mc-btn{padding:4px 10px;background:#0c1d38;border:1px solid #2a3d6a;border-radius:6px;color:#99aacc;cursor:pointer;font-family:inherit;font-size:.76rem;transition:all .2s}
.mc-btn:hover:not(:disabled){background:#182a50;border-color:#4488ff;color:#aabbee}
.mc-btn.mc-ok{background:#0a2c18;border-color:#27ae60;color:#66ffcc;font-weight:700}
.mc-btn.mc-ng{background:#2c0a0a;border-color:#e74c3c;color:#ff9999}
.q-fb{margin-top:4px;font-size:.76rem;font-weight:700;padding:2px 7px;border-radius:4px;min-height:18px}
.q-fb.ok{color:#66ffcc;background:rgba(39,174,96,.13)}
.q-fb.ng{color:#ff8888;background:rgba(231,76,60,.13)}
.reveal{display:none;margin-top:5px;border-top:1px dashed #1e3060;padding-top:5px}

/* ── 미니 차트 ── */
.mini-chart{width:100%;height:90px;background:#040810;border-radius:8px;border:1px solid #1a2840;display:block;margin-top:6px}
</style>
</head>
<body>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab(0)">🖊️ 볼펜 판매가</button>
  <button class="tab-btn" onclick="switchTab(1)">☕ 아메리카노 가격</button>
  <button class="tab-btn" onclick="switchTab(2)">🅿️ 주차장 요금</button>
</div>

<!-- ═══════════════════════════ TAB 1 ═══════════════════════════ -->
<div class="tab-panel active" id="panel0">

  <div class="problem-card">
    <div class="problem-title">🖊️ 상황 1. 볼펜 하루 매출액을 최대로 하는 판매가</div>
    <div class="problem-body">
      A 문구점에서는 <strong>1200원</strong>짜리 볼펜을 하루에 <strong>80개</strong>씩 판매하고 있는데,
      판매가를 <strong>10원 낮출 때마다</strong> 하루 판매량은 <strong>3개 증가</strong>한다고 한다.
    </div>
    <div class="problem-formula">하루 매출액 = 판매가 × 하루 판매량</div>
    <div class="ask">❓ 하루 매출액이 최대가 되는 볼펜의 판매가를 구하시오.</div>
  </div>

  <div class="two-col">
    <!-- 방법 A: 표 -->
    <div class="method-panel method-a">
      <span class="method-title">📊 방법 A: 표로 탐색하기 (아영이 방법)</span>
      <div class="slider-section">
        <div style="font-size:.76rem;color:#667799;margin-bottom:2px">슬라이더로 판매가를 조절하며 최댓값을 찾아보세요!</div>
        <div class="slider-row">
          <span class="slider-lbl">판매가:</span>
          <input type="range" id="sl_p1" min="600" max="1200" step="10" value="1000" oninput="updateTable1()">
          <span class="slider-val" id="sv_p1">1000원</span>
        </div>
      </div>
      <canvas class="mini-chart" id="chart_p1"></canvas>
      <div class="table-result" id="tr_p1">판매가 1000원 → 매출액 계산 중...</div>
      <div class="table-wrap">
        <table id="tbl_p1">
          <thead><tr><th>판매가(원)</th><th>하루 판매량(개)</th><th>하루 매출액(원)</th></tr></thead>
          <tbody id="tbody_p1"></tbody>
        </table>
      </div>
      <div class="table-hint">🔍 표에서 매출액이 가장 큰 행이 강조됩니다</div>
    </div>

    <!-- 방법 B: 수식 -->
    <div class="method-panel method-b">
      <span class="method-title">📐 방법 B: 수식으로 해결하기 (성환이 방법)</span>
      <div class="step-list" id="steps_p1">

        <div class="step-item s1" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">①</span><span class="step-htxt">판매가를 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>판매가를 <span class="hi">10원씩 x번</span> 낮췄다고 하면</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 판매가 = 1200 − □·x &nbsp; □에 알맞은 수는?</span>
              <div class="q-row">
                <span class="q-text">판매가 = 1200 −</span>
                <input class="q-input" id="i_p1_s1" type="number" placeholder="?">
                <span class="q-text">x (원)</span>
                <button class="q-btn" onclick="checkFill('p1_s1',10,0.1,'rv_p1_s1')">확인</button>
              </div>
              <div class="q-fb" id="fb_p1_s1"></div>
              <div class="reveal" id="rv_p1_s1"><span class="formula">판매가 = 1200 − 10x (원)</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s2" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">②</span><span class="step-htxt">하루 판매량을 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>10원 낮출 때마다 <span class="hi">3개 증가</span> → x번 낮추면?</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 하루 판매량 = 80 + □·x &nbsp; □에 알맞은 수는?</span>
              <div class="q-row">
                <span class="q-text">판매량 = 80 +</span>
                <input class="q-input" id="i_p1_s2" type="number" placeholder="?">
                <span class="q-text">x (개)</span>
                <button class="q-btn" onclick="checkFill('p1_s2',3,0.1,'rv_p1_s2')">확인</button>
              </div>
              <div class="q-fb" id="fb_p1_s2"></div>
              <div class="reveal" id="rv_p1_s2"><span class="formula">하루 판매량 = 80 + 3x (개)</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s3" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">③</span><span class="step-htxt">하루 매출액 y를 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>y = 판매가 × 판매량 = (1200−10x)(80+3x)</p>
            <p>전개하면: y = 96000 + 3600x − 800x − 30x²</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ y = −30x² + □x + 96000 &nbsp; □는?</span>
              <div class="q-row">
                <span class="q-text">y = −30x² +</span>
                <input class="q-input" id="i_p1_s3" type="number" placeholder="?">
                <span class="q-text">x + 96000</span>
                <button class="q-btn" onclick="checkFill('p1_s3',2800,1,'rv_p1_s3')">확인</button>
              </div>
              <div class="q-fb" id="fb_p1_s3"></div>
              <div class="reveal" id="rv_p1_s3"><span class="formula">3600−800 = 2800 → y = −30x²+2800x+96000</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s4" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">④</span><span class="step-htxt">y의 값이 최대가 되는 x의 값 구하기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>y = −30x²+2800x+96000 = −30(x−□)²+□</p>
            <p>꼭짓점 x = 2800÷(2×30) = 2800÷60 ≈ 46.67</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ y가 최대가 되는 x의 값으로 알맞은 것은? (자연수)</span>
              <div class="mc-opts">
                <button class="mc-btn" onclick="checkMC('p1_s4',this,false,'rv_p1_s4','x=40이면 자연수이지만 최댓값이 아닙니다.')">① x=40</button>
                <button class="mc-btn" onclick="checkMC('p1_s4',this,true,'rv_p1_s4','')">② x=47</button>
                <button class="mc-btn" onclick="checkMC('p1_s4',this,false,'rv_p1_s4','x=50이면 자연수이지만 최댓값이 아닙니다.')">③ x=50</button>
                <button class="mc-btn" onclick="checkMC('p1_s4',this,false,'rv_p1_s4','x=60이면 판매가가 600원이 됩니다.')">④ x=60</button>
              </div>
              <div class="q-fb" id="fb_p1_s4"></div>
              <div class="reveal" id="rv_p1_s4">
                <span class="formula">46.67은 자연수가 아님 → x=46, x=47 비교</span>
                <span class="formula">x=46: y=−30(2116)+2800(46)+96000=162,120</span>
                <span class="formula">x=47: y=−30(2209)+2800(47)+96000=162,030</span>
                <span class="formula">→ x=46일 때 최대 (y=162,120원)</span>
              </div>
            </div>
          </div>
        </div>

        <div class="step-item s5" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">⑤</span><span class="step-htxt">하루 매출액이 최대가 되는 판매가 정하기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>x=46일 때 판매가 = 1200−10×46 = ?</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 매출액이 최대가 되는 볼펜의 판매가는?</span>
              <div class="q-row">
                <span class="q-text">판매가 =</span>
                <input class="q-input" id="i_p1_s5" type="number" placeholder="?">
                <span class="q-text">원</span>
                <button class="q-btn" onclick="checkFill('p1_s5',740,1,'rv_p1_s5')">확인</button>
              </div>
              <div class="q-fb" id="fb_p1_s5"></div>
              <div class="reveal" id="rv_p1_s5"><span class="formula">판매가 = 1200−460 = 740원, 최대 매출액 = 162,120원</span></div>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ TAB 2 ═══════════════════════════ -->
<div class="tab-panel" id="panel1">

  <div class="problem-card">
    <div class="problem-title">☕ 상황 2. 카페 아메리카노 하루 매출액을 최대로 하는 판매가</div>
    <div class="problem-body">
      B 카페에서는 <strong>3500원</strong>짜리 아메리카노를 하루에 <strong>60잔</strong>씩 판매하고 있는데,
      판매가를 <strong>100원 낮출 때마다</strong> 하루 판매량은 <strong>5잔 증가</strong>한다고 한다.
    </div>
    <div class="problem-formula">하루 매출액 = 판매가 × 하루 판매량</div>
    <div class="ask">❓ 하루 매출액이 최대가 되는 아메리카노의 판매가를 구하시오.</div>
  </div>

  <div class="two-col">
    <!-- 방법 A: 표 -->
    <div class="method-panel method-a">
      <span class="method-title">📊 방법 A: 표로 탐색하기</span>
      <div class="slider-section">
        <div style="font-size:.76rem;color:#667799;margin-bottom:2px">슬라이더로 판매가를 조절하며 최댓값을 찾아보세요!</div>
        <div class="slider-row">
          <span class="slider-lbl">판매가:</span>
          <input type="range" id="sl_p2" min="1500" max="3500" step="100" value="2500" oninput="updateTable2()">
          <span class="slider-val" id="sv_p2">2500원</span>
        </div>
      </div>
      <canvas class="mini-chart" id="chart_p2"></canvas>
      <div class="table-result" id="tr_p2">판매가 2500원 → 매출액 계산 중...</div>
      <div class="table-wrap">
        <table id="tbl_p2">
          <thead><tr><th>판매가(원)</th><th>하루 판매량(잔)</th><th>하루 매출액(원)</th></tr></thead>
          <tbody id="tbody_p2"></tbody>
        </table>
      </div>
      <div class="table-hint">🔍 표에서 매출액이 가장 큰 행이 강조됩니다</div>
    </div>

    <!-- 방법 B: 수식 -->
    <div class="method-panel method-b">
      <span class="method-title">📐 방법 B: 수식으로 해결하기</span>
      <div class="step-list">

        <div class="step-item s1" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">①</span><span class="step-htxt">판매가를 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>판매가를 <span class="hi">100원씩 x번</span> 낮췄다고 하면</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 판매가 = 3500 − □·x (원) &nbsp; □는?</span>
              <div class="q-row">
                <span class="q-text">판매가 = 3500 −</span>
                <input class="q-input" id="i_p2_s1" type="number" placeholder="?">
                <span class="q-text">x (원)</span>
                <button class="q-btn" onclick="checkFill('p2_s1',100,0.1,'rv_p2_s1')">확인</button>
              </div>
              <div class="q-fb" id="fb_p2_s1"></div>
              <div class="reveal" id="rv_p2_s1"><span class="formula">판매가 = 3500 − 100x (원)</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s2" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">②</span><span class="step-htxt">하루 판매량을 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>100원 낮출 때마다 <span class="hi">5잔 증가</span></p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 판매량 = 60 + □·x (잔) &nbsp; □는?</span>
              <div class="q-row">
                <span class="q-text">판매량 = 60 +</span>
                <input class="q-input" id="i_p2_s2" type="number" placeholder="?">
                <span class="q-text">x (잔)</span>
                <button class="q-btn" onclick="checkFill('p2_s2',5,0.1,'rv_p2_s2')">확인</button>
              </div>
              <div class="q-fb" id="fb_p2_s2"></div>
              <div class="reveal" id="rv_p2_s2"><span class="formula">하루 판매량 = 60 + 5x (잔)</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s3" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">③</span><span class="step-htxt">하루 매출액 y를 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>y = (3500−100x)(60+5x) 전개:</p>
            <p>= 210000 + 17500x − 6000x − 500x²</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ y = −500x² + □x + 210000 &nbsp; □는?</span>
              <div class="q-row">
                <span class="q-text">y = −500x² +</span>
                <input class="q-input" id="i_p2_s3" type="number" placeholder="?">
                <span class="q-text">x + 210000</span>
                <button class="q-btn" onclick="checkFill('p2_s3',11500,5,'rv_p2_s3')">확인</button>
              </div>
              <div class="q-fb" id="fb_p2_s3"></div>
              <div class="reveal" id="rv_p2_s3"><span class="formula">17500−6000 = 11500 → y = −500x²+11500x+210000</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s4" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">④</span><span class="step-htxt">y가 최대가 되는 자연수 x의 값 구하기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>꼭짓점: x = 11500÷(2×500) = 11500÷1000 = 11.5</p>
            <p>자연수이어야 하므로 x=11, x=12 비교</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ y가 최대인 자연수 x의 값은?</span>
              <div class="mc-opts">
                <button class="mc-btn" onclick="checkMC('p2_s4',this,false,'rv_p2_s4','x=10이면 최댓값이 아닙니다.')">① x=10</button>
                <button class="mc-btn" onclick="checkMC('p2_s4',this,false,'rv_p2_s4','x=11일 때 y=276,500, x=12일 때도 확인해보세요.')">② x=11</button>
                <button class="mc-btn" onclick="checkMC('p2_s4',this,false,'rv_p2_s4','x=11과 x=12의 y값을 비교해보세요.')">③ x=12 </button>
                <button class="mc-btn" onclick="checkMC('p2_s4',this,true,'rv_p2_s4','')">④ x=11 또는 x=12</button>
              </div>
              <div class="q-fb" id="fb_p2_s4"></div>
              <div class="reveal" id="rv_p2_s4">
                <span class="formula">x=11: y=−500(121)+11500(11)+210000=276,500</span>
                <span class="formula">x=12: y=−500(144)+11500(12)+210000=276,000</span>
                <span class="formula">→ x=11일 때 y 최대 = 276,500원</span>
              </div>
            </div>
          </div>
        </div>

        <div class="step-item s5" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">⑤</span><span class="step-htxt">하루 매출액이 최대가 되는 판매가 정하기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>x=11일 때 판매가 = 3500−100×11 = ?</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 매출액이 최대가 되는 아메리카노 판매가는?</span>
              <div class="q-row">
                <span class="q-text">판매가 =</span>
                <input class="q-input" id="i_p2_s5" type="number" placeholder="?">
                <span class="q-text">원</span>
                <button class="q-btn" onclick="checkFill('p2_s5',2400,1,'rv_p2_s5')">확인</button>
              </div>
              <div class="q-fb" id="fb_p2_s5"></div>
              <div class="reveal" id="rv_p2_s5"><span class="formula">판매가 = 2400원, 최대 매출액 = 276,500원</span></div>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ TAB 3 ═══════════════════════════ -->
<div class="tab-panel" id="panel2">

  <div class="problem-card">
    <div class="problem-title">🅿️ 상황 3. 주차장 하루 수입을 최대로 하는 주차 요금</div>
    <div class="problem-body">
      C 주차장에서는 시간당 <strong>2000원</strong>의 주차 요금으로 하루에 <strong>50대</strong>가 이용하고 있는데,
      요금을 <strong>200원 낮출 때마다</strong> 하루 이용 대수는 <strong>8대 증가</strong>한다고 한다.
      (단, 1대당 하루 이용 시간은 모두 동일하게 <strong>1시간</strong>으로 가정한다.)
    </div>
    <div class="problem-formula">하루 수입 = 시간당 요금 × 하루 이용 대수</div>
    <div class="ask">❓ 하루 수입이 최대가 되는 주차 요금을 구하시오.</div>
  </div>

  <div class="two-col">
    <!-- 방법 A: 표 -->
    <div class="method-panel method-a">
      <span class="method-title">📊 방법 A: 표로 탐색하기</span>
      <div class="slider-section">
        <div style="font-size:.76rem;color:#667799;margin-bottom:2px">슬라이더로 요금을 조절하며 최댓값을 찾아보세요!</div>
        <div class="slider-row">
          <span class="slider-lbl">시간당 요금:</span>
          <input type="range" id="sl_p3" min="400" max="2000" step="200" value="1200" oninput="updateTable3()">
          <span class="slider-val" id="sv_p3">1200원</span>
        </div>
      </div>
      <canvas class="mini-chart" id="chart_p3"></canvas>
      <div class="table-result" id="tr_p3">요금 1200원 → 수입 계산 중...</div>
      <div class="table-wrap">
        <table id="tbl_p3">
          <thead><tr><th>시간당 요금(원)</th><th>하루 이용 대수(대)</th><th>하루 수입(원)</th></tr></thead>
          <tbody id="tbody_p3"></tbody>
        </table>
      </div>
      <div class="table-hint">🔍 표에서 수입이 가장 큰 행이 강조됩니다</div>
    </div>

    <!-- 방법 B: 수식 -->
    <div class="method-panel method-b">
      <span class="method-title">📐 방법 B: 수식으로 해결하기</span>
      <div class="step-list">

        <div class="step-item s1" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">①</span><span class="step-htxt">요금을 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>요금을 <span class="hi">200원씩 x번</span> 낮췄다고 하면</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 시간당 요금 = 2000 − □·x (원) &nbsp; □는?</span>
              <div class="q-row">
                <span class="q-text">요금 = 2000 −</span>
                <input class="q-input" id="i_p3_s1" type="number" placeholder="?">
                <span class="q-text">x (원)</span>
                <button class="q-btn" onclick="checkFill('p3_s1',200,0.1,'rv_p3_s1')">확인</button>
              </div>
              <div class="q-fb" id="fb_p3_s1"></div>
              <div class="reveal" id="rv_p3_s1"><span class="formula">시간당 요금 = 2000 − 200x (원)</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s2" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">②</span><span class="step-htxt">하루 이용 대수를 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>200원 낮출 때마다 <span class="hi">8대 증가</span></p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 이용 대수 = 50 + □·x (대) &nbsp; □는?</span>
              <div class="q-row">
                <span class="q-text">이용 대수 = 50 +</span>
                <input class="q-input" id="i_p3_s2" type="number" placeholder="?">
                <span class="q-text">x (대)</span>
                <button class="q-btn" onclick="checkFill('p3_s2',8,0.1,'rv_p3_s2')">확인</button>
              </div>
              <div class="q-fb" id="fb_p3_s2"></div>
              <div class="reveal" id="rv_p3_s2"><span class="formula">하루 이용 대수 = 50 + 8x (대)</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s3" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">③</span><span class="step-htxt">하루 수입 y를 x에 대한 식으로 나타내기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>y = (2000−200x)(50+8x)</p>
            <p>= 100000 + 16000x − 10000x − 1600x²</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ y = −1600x² + □x + 100000 &nbsp; □는?</span>
              <div class="q-row">
                <span class="q-text">y = −1600x² +</span>
                <input class="q-input" id="i_p3_s3" type="number" placeholder="?">
                <span class="q-text">x + 100000</span>
                <button class="q-btn" onclick="checkFill('p3_s3',6000,5,'rv_p3_s3')">확인</button>
              </div>
              <div class="q-fb" id="fb_p3_s3"></div>
              <div class="reveal" id="rv_p3_s3"><span class="formula">16000−10000 = 6000 → y = −1600x²+6000x+100000</span></div>
            </div>
          </div>
        </div>

        <div class="step-item s4" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">④</span><span class="step-htxt">y가 최대가 되는 x의 값 구하기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>꼭짓점: x = 6000÷(2×1600) = 6000÷3200 = 1.875</p>
            <p>자연수이어야 하므로 x=1, x=2 비교</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ y가 최대인 자연수 x의 값은?</span>
              <div class="mc-opts">
                <button class="mc-btn" onclick="checkMC('p3_s4',this,true,'rv_p3_s4','')">① x=2</button>
                <button class="mc-btn" onclick="checkMC('p3_s4',this,false,'rv_p3_s4','x=1일 때와 x=2일 때를 비교해보세요.')">② x=1</button>
                <button class="mc-btn" onclick="checkMC('p3_s4',this,false,'rv_p3_s4','x=3이면 요금이 1400원, 더 크지 않습니다.')">③ x=3</button>
                <button class="mc-btn" onclick="checkMC('p3_s4',this,false,'rv_p3_s4','x=4이면 요금이 1200원입니다.')">④ x=4</button>
              </div>
              <div class="q-fb" id="fb_p3_s4"></div>
              <div class="reveal" id="rv_p3_s4">
                <span class="formula">x=1: y=−1600+6000+100000=104,400</span>
                <span class="formula">x=2: y=−6400+12000+100000=105,600</span>
                <span class="formula">→ x=2일 때 y 최대 = 105,600원</span>
              </div>
            </div>
          </div>
        </div>

        <div class="step-item s5" onclick="toggleStep(this)">
          <div class="step-hdr"><span class="step-num">⑤</span><span class="step-htxt">하루 수입이 최대가 되는 주차 요금 정하기</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>x=2일 때 시간당 요금 = 2000−200×2 = ?</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 수입이 최대가 되는 시간당 주차 요금은?</span>
              <div class="q-row">
                <span class="q-text">요금 =</span>
                <input class="q-input" id="i_p3_s5" type="number" placeholder="?">
                <span class="q-text">원</span>
                <button class="q-btn" onclick="checkFill('p3_s5',1600,1,'rv_p3_s5')">확인</button>
              </div>
              <div class="q-fb" id="fb_p3_s5"></div>
              <div class="reveal" id="rv_p3_s5"><span class="formula">요금 = 1600원, 하루 수입 최댓값 = 105,600원</span></div>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>
</div>

<script>
/* ══ TAB ══ */
function switchTab(idx){
  document.querySelectorAll('.tab-btn').forEach((b,i)=>b.classList.toggle('active',i===idx));
  document.querySelectorAll('.tab-panel').forEach((p,i)=>p.classList.toggle('active',i===idx));
  if(idx===0)updateTable1();
  if(idx===1)updateTable2();
  if(idx===2)updateTable3();
}
function toggleStep(el){
  const wasOpen=el.classList.contains('open');
  el.closest('.step-list').querySelectorAll('.step-item').forEach(s=>s.classList.remove('open'));
  if(!wasOpen)el.classList.add('open');
}

/* ══ ANSWER CHECK ══ */
function checkFill(id,ans,tol,revId){
  const inp=document.getElementById('i_'+id);
  const fb=document.getElementById('fb_'+id);
  const val=parseFloat(inp.value);
  if(isNaN(val)){fb.textContent='❌ 숫자를 입력해 주세요.';fb.className='q-fb ng';return;}
  if(Math.abs(val-ans)<=tol){
    fb.textContent='✅ 정답입니다!';fb.className='q-fb ok';
    inp.classList.add('ok');inp.disabled=true;
    const rv=document.getElementById(revId);if(rv)rv.style.display='block';
  }else{
    fb.textContent='❌ 다시 계산해 보세요.';fb.className='q-fb ng';
    inp.classList.add('err');setTimeout(()=>inp.classList.remove('err'),600);
  }
}
function checkMC(id,btn,isOk,revId,hint){
  const fb=document.getElementById('fb_'+id);
  if(isOk){
    btn.classList.add('mc-ok');
    btn.closest('.mc-opts').querySelectorAll('.mc-btn').forEach(b=>b.disabled=true);
    fb.textContent='✅ 정답입니다!';fb.className='q-fb ok';
    const rv=document.getElementById(revId);if(rv)rv.style.display='block';
  }else{
    btn.classList.add('mc-ng');
    fb.textContent='❌ '+hint;fb.className='q-fb ng';
    setTimeout(()=>btn.classList.remove('mc-ng'),800);
    setTimeout(()=>{if(fb.className==='q-fb ng')fb.textContent='';},2500);
  }
}

/* ══ TABLE 1: 볼펜 (기준 1200원, 80개, 10원↓→3개↑) ══ */
function rev1(p){return p*(80+3*(1200-p)/10);}
function updateTable1(){
  const sel=parseInt(document.getElementById('sl_p1').value);
  document.getElementById('sv_p1').textContent=sel+'원';
  const rows=[];
  for(let p=1200;p>=600;p-=10){
    const qty=80+3*(1200-p)/10;
    const rev=p*qty;
    rows.push({p,qty,rev});
  }
  const maxRev=Math.max(...rows.map(r=>r.rev));
  let tbody='';
  rows.forEach(r=>{
    const isSel=r.p===sel;
    const isMax=r.rev===maxRev;
    const cls=isMax?'highlight':Math.abs(r.rev-maxRev)<3000?'near-max':'';
    tbody+=`<tr class="${cls}${isSel?' sel-row':''}"><td>${r.p}</td><td>${r.qty}</td><td>${r.rev.toLocaleString()}</td></tr>`;
  });
  document.getElementById('tbody_p1').innerHTML=tbody;
  const cur=rev1(sel);
  document.getElementById('tr_p1').textContent=`판매가 ${sel}원 → 매출액 ${cur.toLocaleString()}원 ${cur===maxRev?'🏆 최댓값!':''}`;
  drawChart('chart_p1',rows.map(r=>r.p),rows.map(r=>r.rev),sel,maxRev);
}

/* ══ TABLE 2: 아메리카노 (기준 3500원, 60잔, 100원↓→5잔↑) ══ */
function updateTable2(){
  const sel=parseInt(document.getElementById('sl_p2').value);
  document.getElementById('sv_p2').textContent=sel+'원';
  const rows=[];
  for(let p=3500;p>=1500;p-=100){
    const qty=60+5*(3500-p)/100;
    const rev=p*qty;
    rows.push({p,qty,rev});
  }
  const maxRev=Math.max(...rows.map(r=>r.rev));
  let tbody='';
  rows.forEach(r=>{
    const isSel=r.p===sel;
    const isMax=r.rev===maxRev;
    const cls=isMax?'highlight':Math.abs(r.rev-maxRev)<5000?'near-max':'';
    tbody+=`<tr class="${cls}${isSel?' sel-row':''}"><td>${r.p}</td><td>${r.qty}</td><td>${r.rev.toLocaleString()}</td></tr>`;
  });
  document.getElementById('tbody_p2').innerHTML=tbody;
  const curRow=rows.find(r=>r.p===sel)||rows[0];
  const cur=curRow.rev;
  document.getElementById('tr_p2').textContent=`판매가 ${sel}원 → 매출액 ${cur.toLocaleString()}원 ${cur===maxRev?'🏆 최댓값!':''}`;
  drawChart('chart_p2',rows.map(r=>r.p),rows.map(r=>r.rev),sel,maxRev);
}

/* ══ TABLE 3: 주차장 (기준 2000원, 50대, 200원↓→8대↑) ══ */
function updateTable3(){
  const sel=parseInt(document.getElementById('sl_p3').value);
  document.getElementById('sv_p3').textContent=sel+'원';
  const rows=[];
  for(let p=2000;p>=400;p-=200){
    const qty=50+8*(2000-p)/200;
    const rev=p*qty;
    rows.push({p,qty,rev});
  }
  const maxRev=Math.max(...rows.map(r=>r.rev));
  let tbody='';
  rows.forEach(r=>{
    const isSel=r.p===sel;
    const isMax=r.rev===maxRev;
    const cls=isMax?'highlight':Math.abs(r.rev-maxRev)<2000?'near-max':'';
    tbody+=`<tr class="${cls}${isSel?' sel-row':''}"><td>${r.p}</td><td>${r.qty}</td><td>${r.rev.toLocaleString()}</td></tr>`;
  });
  document.getElementById('tbody_p3').innerHTML=tbody;
  const curRow=rows.find(r=>r.p===sel)||rows[0];
  const cur=curRow.rev;
  document.getElementById('tr_p3').textContent=`요금 ${sel}원 → 수입 ${cur.toLocaleString()}원 ${cur===maxRev?'🏆 최댓값!':''}`;
  drawChart('chart_p3',rows.map(r=>r.p),rows.map(r=>r.rev),sel,maxRev);
}

/* ══ MINI CHART ══ */
function drawChart(canvasId,prices,revs,selP,maxRev){
  const cv=document.getElementById(canvasId);
  if(!cv)return;
  const ctx=cv.getContext('2d');
  const W=cv.clientWidth||cv.width;
  cv.width=W;
  const H=cv.height;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#040810';ctx.fillRect(0,0,W,H);

  const pad={l:10,r:10,t:10,b:10};
  const iW=W-pad.l-pad.r,iH=H-pad.t-pad.b;
  const minR=Math.min(...revs),maxR=Math.max(...revs);
  const minP=Math.min(...prices),maxP=Math.max(...prices);

  const px=p=>pad.l+((maxP-p)/(maxP-minP))*iW; // prices go right-to-left on x? actually descending order
  // Actually prices array goes from high to low, let's use index
  const n=prices.length;
  const ix=i=>pad.l+(i/(n-1))*iW;
  const iy=r=>pad.t+iH-((r-minR)/(maxR-minR+1))*iH;

  // draw curve
  ctx.beginPath();
  revs.forEach((r,i)=>{i===0?ctx.moveTo(ix(i),iy(r)):ctx.lineTo(ix(i),iy(r));});
  ctx.strokeStyle='#4488ff';ctx.lineWidth=1.5;ctx.stroke();

  // fill area
  ctx.beginPath();
  revs.forEach((r,i)=>{i===0?ctx.moveTo(ix(i),iy(r)):ctx.lineTo(ix(i),iy(r));});
  ctx.lineTo(ix(n-1),H);ctx.lineTo(ix(0),H);ctx.closePath();
  ctx.fillStyle='rgba(68,136,255,.12)';ctx.fill();

  // max dot
  const maxIdx=revs.indexOf(maxRev);
  ctx.beginPath();ctx.arc(ix(maxIdx),iy(maxRev),4,0,Math.PI*2);ctx.fillStyle='#ffd700';ctx.fill();

  // sel dot
  const selIdx=prices.indexOf(selP);
  if(selIdx>=0){
    ctx.beginPath();ctx.arc(ix(selIdx),iy(revs[selIdx]),3.5,0,Math.PI*2);ctx.fillStyle='#66ffcc';ctx.fill();
  }

  ctx.fillStyle='#445577';ctx.font='8px sans-serif';ctx.textAlign='left';
  ctx.fillText('높은 가격 →',pad.l+2,H-3);
  ctx.textAlign='right';
  ctx.fillText('← 낮은 가격',W-pad.r-2,H-3);
}

/* ══ INIT ══ */
window.addEventListener('load',()=>{
  updateTable1();
  // lazy init for tabs 2,3
});
window.addEventListener('resize',()=>{
  const active=[...document.querySelectorAll('.tab-panel.active')];
  if(active[0]?.id==='panel0')updateTable1();
  else if(active[0]?.id==='panel1')updateTable2();
  else if(active[0]?.id==='panel2')updateTable3();
});
</script>
</body>
</html>"""


def render():
    st.markdown("### 🛒 최댓값 찾기: 표 vs 수식")
    st.markdown(
        "볼펜·아메리카노·주차장 3가지 실생활 상황에서 **표로 탐색하는 방법**과 "
        "**이차함수 식을 세워 해결하는 방법**을 직접 비교해 봅니다."
    )
    components.html(_HTML, height=720, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
