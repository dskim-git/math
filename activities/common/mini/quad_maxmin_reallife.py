# activities/common/mini/quad_maxmin_reallife.py
"""
이차함수 최대·최소 실생활 문제 탐구
강아지 놀이터, 채소밭 리모델링, 불꽃놀이 로켓 3가지 실생활 상황에서
이차함수의 최대·최소를 5단계 풀이 과정 + 빈칸채우기/객관식으로 탐구하는 미니활동
시뮬레이션이 상단, 문제+풀이가 하단에 배치 / 스크롤 없이 한 화면
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "이차함수최대최소실생활"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "풀이순서중요성",
        "label":  "① 5단계 풀이 순서(조건 확인 → 변수 결정 → 관계식 → 최대최솟값 → 해석)로 문제를 풀어봤습니다. 이 순서가 왜 중요한지 설명하고, 어느 단계가 가장 어려웠는지 적어보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "변수범위의미",
        "label":  "② 세 문제 모두 변수의 범위를 구해야 했습니다. 범위를 구하지 않으면 어떤 문제가 생길 수 있을까요? 예를 들어 설명해 보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "시뮬레이션발견",
        "label":  "③ 시뮬레이션을 직접 조작하면서 새롭게 발견하거나 확인한 점이 있나요? 수식으로만 풀었을 때와 다른 점은 무엇이었나요?",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "공통구조",
        "label":  "④ 세 문제(놀이터·채소밭·로켓)가 서로 다른 상황임에도 이차함수의 최대·최소 문제로 변환되는 공통적인 이유는 무엇인가요?",
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
    "title":       "🏗️ 이차함수 최대·최소 실생활 탐구",
    "description": "강아지 놀이터·채소밭 리모델링·불꽃놀이 로켓 등 실생활 3가지 상황을 5단계 풀이 과정+빈칸채우기/객관식으로 탐구하고 인터랙티브 시뮬레이션으로 확인합니다.",
    "order":       241,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>이차함수 최대·최소 실생활 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(155deg,#060917 0%,#0e1630 60%,#080f1c 100%);
  color:#e2e8ff;
  padding:10px 12px 16px;
  overflow:hidden; /* 외부 스크롤 제거 */
}

/* ── 탭 ── */
.tabs{display:flex;gap:4px;border-bottom:2px solid #1e3060;margin-bottom:0}
.tab-btn{padding:7px 14px;border:none;border-radius:9px 9px 0 0;background:#0a1020;color:#556688;cursor:pointer;font-size:.82rem;font-family:inherit;transition:all .2s;border-bottom:2px solid transparent;margin-bottom:-2px}
.tab-btn:hover{background:#131e38;color:#99aacc}
.tab-btn.active{background:#151f3a;color:#ffd700;border-bottom:2px solid #ffd700;font-weight:700}

/* ── 각 탭 패널: 상단 시뮬 + 하단 문제·풀이 2단 ── */
.tab-panel{display:none}
.tab-panel.active{display:grid;grid-template-rows:auto 1fr;gap:8px;padding-top:8px}

/* 상단 시뮬레이션 */
.sim-box{
  background:#060c1a;border:1px solid #1e3060;border-radius:10px;
  padding:8px 10px;
}
.sim-header{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.sim-title{font-size:.82rem;font-weight:700;color:#88aaff}
.sim-result{font-size:.92rem;font-weight:700;color:#66ffcc;flex:1;text-align:right}
.sim-note{font-size:.75rem;color:#ff9944;text-align:right}
.sim-body{display:flex;align-items:flex-start;gap:10px;flex-wrap:wrap}
canvas{display:block;border-radius:7px;flex-shrink:0}
.sim-right{flex:1;min-width:160px;display:flex;flex-direction:column;gap:6px}
.slider-row{display:flex;align-items:center;gap:7px}
.slider-lbl{font-size:.78rem;color:#99aacc;white-space:nowrap}
input[type=range]{flex:1;accent-color:#4f9cf9;cursor:pointer;min-width:60px}
.slider-val{font-size:.85rem;font-weight:700;color:#ffd700;min-width:52px;text-align:right;white-space:nowrap}
.rocket-btns{display:flex;gap:7px}
.btn{padding:6px 16px;border:none;border-radius:7px;cursor:pointer;font-size:.82rem;font-family:inherit;font-weight:700;transition:all .2s}
.btn-fire{background:#e74c3c;color:#fff}.btn-fire:hover{background:#c0392b}
.btn-rst{background:#1e3060;color:#99aacc}.btn-rst:hover{background:#2e4080}

/* 하단 2단: 왼쪽 문제카드 + 오른쪽 풀이단계 */
.bottom-row{display:grid;grid-template-columns:1fr 1.7fr;gap:8px;min-height:0}

/* 문제 카드 */
.problem-card{
  background:linear-gradient(135deg,#151f3a,#1a2848);
  border:1px solid #2e4070;border-radius:10px;
  padding:11px 13px;
  display:flex;flex-direction:column;gap:7px;
}
.problem-icon{font-size:2.2rem;text-align:center}
.problem-title{font-size:.9rem;font-weight:700;color:#ffd700}
.problem-desc{font-size:.8rem;line-height:1.65;color:#b0c0e0}
.problem-desc strong{color:#77ccff}
.problem-question{background:#080e1c;border-left:3px solid #ffd700;padding:6px 10px;border-radius:0 7px 7px 0;font-size:.8rem;color:#ffe080;line-height:1.6}

/* 풀이 단계 패널 (내부 스크롤) */
.steps-panel{
  display:flex;flex-direction:column;gap:0;
  overflow-y:hidden;
  border:1px solid #1e3060;border-radius:10px;
  background:#07101f;
}
.steps-label{font-size:.78rem;font-weight:700;color:#88aaff;padding:7px 12px 5px;border-bottom:1px solid #131e38}
.steps-container{display:flex;flex-direction:column;gap:0}
.step-item{background:#07101f;border-bottom:1px solid #131e38;cursor:pointer;transition:background .15s}
.step-item:hover{background:#0c1928}
.step-header{display:flex;align-items:center;gap:7px;padding:8px 11px}
.step-num{display:flex;align-items:center;justify-content:center;width:21px;height:21px;border-radius:50%;font-weight:700;font-size:.75rem;flex-shrink:0}
.s1 .step-num{background:#e74c3c;color:#fff}
.s2 .step-num{background:#e67e22;color:#fff}
.s3 .step-num{background:#d4ac0d;color:#111}
.s4 .step-num{background:#27ae60;color:#fff}
.s5 .step-num{background:#2980b9;color:#fff}
.step-htxt{font-size:.8rem;color:#b0c0e0;font-weight:600;flex:1}
.step-arr{color:#445577;transition:transform .2s;font-size:.7rem;margin-left:auto}
.step-item.open .step-arr{transform:rotate(180deg)}
.step-body{display:none;padding:7px 11px 10px 39px;font-size:.79rem;color:#99aacc;line-height:1.7;border-top:1px solid #0d1828}
.step-item.open .step-body{display:block}
.step-body p{margin-bottom:2px}
.hi{color:#ffd700;font-weight:700}
.formula{font-family:'Courier New',monospace;background:#050a14;padding:4px 9px;border-radius:5px;margin:4px 0;font-size:.82rem;color:#66ffcc;border-left:2px solid #27ae60}

/* 빈칸 / 객관식 */
.q-box{background:#040810;border:1px dashed #2a4878;border-radius:8px;padding:8px 11px;margin-top:7px}
.q-label{display:block;font-size:.78rem;color:#88ccff;font-weight:700;margin-bottom:5px}
.q-row{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:2px}
.q-text{font-size:.8rem;color:#aabbdd}
.q-input{width:66px;padding:4px 6px;background:#080f1e;border:1.5px solid #336699;border-radius:5px;color:#e2e8ff;font-size:.86rem;text-align:center;font-family:inherit}
.q-input:focus{outline:none;border-color:#77aaee}
.q-input.ok{border-color:#27ae60;color:#66ffcc;background:#050e08}
.q-input.err{border-color:#e74c3c}
.q-btn{padding:4px 11px;background:#1a3560;border:none;border-radius:5px;color:#88aaff;cursor:pointer;font-family:inherit;font-size:.77rem;font-weight:700;transition:all .2s;white-space:nowrap}
.q-btn:hover{background:#234580;color:#aaccff}
.mc-opts{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}
.mc-btn{padding:5px 11px;background:#0d1e38;border:1px solid #2a3d6a;border-radius:7px;color:#99aacc;cursor:pointer;font-family:inherit;font-size:.78rem;transition:all .2s}
.mc-btn:hover:not(:disabled){background:#182a50;border-color:#4488ff;color:#aabbee}
.mc-btn.mc-ok{background:#0a2c18;border-color:#27ae60;color:#66ffcc;font-weight:700}
.mc-btn.mc-ng{background:#2c0a0a;border-color:#e74c3c;color:#ff9999}
.q-fb{margin-top:5px;font-size:.78rem;font-weight:700;padding:3px 8px;border-radius:4px;min-height:20px}
.q-fb.ok{color:#66ffcc;background:rgba(39,174,96,.13)}
.q-fb.ng{color:#ff8888;background:rgba(231,76,60,.13)}
.reveal{display:none;margin-top:6px;border-top:1px dashed #1e3060;padding-top:6px}

/* 5단계 인트로 배너 */
.intro-bar{
  display:flex;gap:4px;flex-wrap:wrap;
  background:#0c1526;border:1px solid #1e3060;border-radius:8px;
  padding:6px 9px;margin-bottom:7px;
}
.is{flex:1;min-width:70px;display:flex;flex-direction:column;align-items:center;gap:2px}
.is .n{width:18px;height:18px;border-radius:50%;background:#4f9cf9;color:#fff;font-weight:700;font-size:.68rem;line-height:18px;text-align:center}
.is .l{font-size:.65rem;color:#99aacc;text-align:center;line-height:1.3}
</style>
</head>
<body>

<!-- 탭 버튼 -->
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab(0)">🐕 강아지 놀이터</button>
  <button class="tab-btn" onclick="switchTab(1)">🌱 채소밭 리모델링</button>
  <button class="tab-btn" onclick="switchTab(2)">🚀 불꽃놀이 로켓</button>
</div>

<!-- ══════════════════════ TAB 1 ══════════════════════ -->
<div class="tab-panel active" id="panel0">

  <!-- 시뮬레이션 (상단) -->
  <div class="sim-box">
    <div class="sim-header">
      <span class="sim-title">🎮 시뮬레이션 — 슬라이더로 철망 배치를 바꿔 보세요!</span>
      <span class="sim-result" id="sr1">넓이 S = 72.0 m²</span>
    </div>
    <div class="sim-body">
      <canvas id="c1" width="380" height="200"></canvas>
      <div class="sim-right">
        <div class="slider-row">
          <span class="slider-lbl">수직 변 x (m):</span>
          <input type="range" id="sl1" min="0.5" max="11.5" step="0.1" value="6" oninput="drawP1()">
          <span class="slider-val" id="sv1">6.0 m</span>
        </div>
        <div class="sim-note" id="sn1">🏆 최댓값: x=6m일 때 72m²</div>
      </div>
    </div>
  </div>

  <!-- 하단: 문제 + 풀이 -->
  <div class="bottom-row">
    <div class="problem-card">
      <div class="problem-icon">🐕</div>
      <div class="problem-title">상황 1. 강아지 놀이터 설계</div>
      <div class="problem-desc">반려견 카페에서 총 <strong>24 m</strong>의 철망을 사용하여 건물 벽면 한쪽을 이용한 <strong>직사각형</strong> 모양의 강아지 놀이터를 만들려고 합니다. 철망은 벽과 마주 보는 방향 1곳과 벽에 수직인 방향 2곳에만 사용합니다.</div>
      <div class="problem-question">❓ 강아지 놀이터 바닥의 넓이의 <strong>최댓값</strong>을 구하시오.</div>
      <div class="intro-bar">
        <div class="is"><span class="n">①</span><span class="l">조건·목표<br>확인</span></div>
        <div class="is"><span class="n">②</span><span class="l">변수·<br>범위</span></div>
        <div class="is"><span class="n">③</span><span class="l">관계식<br>세우기</span></div>
        <div class="is"><span class="n">④</span><span class="l">최댓값<br>찾기</span></div>
        <div class="is"><span class="n">⑤</span><span class="l">답<br>해석</span></div>
      </div>
    </div>

    <div class="steps-panel">
      <div class="steps-label">📋 각 단계를 클릭하고 빈칸을 채워보세요!</div>
      <div class="steps-container">

        <div class="step-item s1" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">①</span><span class="step-htxt">주어진 조건과 구하려는 것을 확인한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>• 총 철망 길이: <span class="hi">24 m</span></p>
            <p>• 한쪽은 건물 벽 → 철망은 <span class="hi">3면</span>에만 설치</p>
            <p>• 구하려는 것: 직사각형 넓이의 <span class="hi">최댓값</span></p>
          </div>
        </div>

        <div class="step-item s2" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">②</span><span class="step-htxt">변수를 결정하고, 변수의 범위를 구한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>• 벽에 수직인 변: <span class="hi">x m</span>, 벽에 평행한 변: <span class="hi">y m</span></p>
            <p>• 철망 3면의 합 = 총 철망 길이</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 철망의 관계식: &nbsp; 2x + y = ?</span>
              <div class="q-row">
                <span class="q-text">2x + y =</span>
                <input class="q-input" id="i_p1_s2" type="number" placeholder="?">
                <button class="q-btn" onclick="checkFill('p1_s2',24,0.1,'rv_p1_s2')">확인</button>
              </div>
              <div class="q-fb" id="fb_p1_s2"></div>
              <div class="reveal" id="rv_p1_s2">
                <div class="formula">2x + y = 24 → y = 24−2x, &nbsp; 범위: 0 &lt; x &lt; 12</div>
              </div>
            </div>
          </div>
        </div>

        <div class="step-item s3" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">③</span><span class="step-htxt">변수 사이의 관계식을 세운다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>• S = x·y = x(24−2x) 를 전개하면</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ S = −2x² + □x &nbsp; □를 구하세요</span>
              <div class="q-row">
                <span class="q-text">S = −2x² +</span>
                <input class="q-input" id="i_p1_s3" type="number" placeholder="?">
                <span class="q-text">x</span>
                <button class="q-btn" onclick="checkFill('p1_s3',24,0.1,'rv_p1_s3')">확인</button>
              </div>
              <div class="q-fb" id="fb_p1_s3"></div>
              <div class="reveal" id="rv_p1_s3">
                <div class="formula">S = −2x²+24x = −2(x−6)²+72</div>
              </div>
            </div>
          </div>
        </div>

        <div class="step-item s4" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">④</span><span class="step-htxt">구하는 값을 관계식을 이용하여 찾는다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>S = −2(x−6)²+72 의 꼭짓점: (6, 72) / 0&lt;x&lt;12 내 포함</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ S가 최대가 되는 x의 값은?</span>
              <div class="mc-opts">
                <button class="mc-btn" onclick="checkMC('p1_s4',this,false,'rv_p1_s4','x=4이면 S=64입니다.')">① x=4</button>
                <button class="mc-btn" onclick="checkMC('p1_s4',this,true,'rv_p1_s4','')">② x=6</button>
                <button class="mc-btn" onclick="checkMC('p1_s4',this,false,'rv_p1_s4','x=8이면 S=64입니다.')">③ x=8</button>
                <button class="mc-btn" onclick="checkMC('p1_s4',this,false,'rv_p1_s4','x=10이면 S=40입니다.')">④ x=10</button>
              </div>
              <div class="q-fb" id="fb_p1_s4"></div>
              <div class="reveal" id="rv_p1_s4"><div class="formula">x=6일 때 S 최댓값 = 72 m²</div></div>
            </div>
          </div>
        </div>

        <div class="step-item s5" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">⑤</span><span class="step-htxt">문제에 맞게 답을 해석한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>x=6 → y = 24−12 = 12 m (수직 6m, 평행 12m)</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 강아지 놀이터 넓이의 최댓값은?</span>
              <div class="q-row">
                <input class="q-input" id="i_p1_s5" type="number" placeholder="?">
                <span class="q-text">m²</span>
                <button class="q-btn" onclick="checkFill('p1_s5',72,0.5,'rv_p1_s5')">확인</button>
              </div>
              <div class="q-fb" id="fb_p1_s5"></div>
              <div class="reveal" id="rv_p1_s5"><div class="formula">넓이 최댓값 = 72 m²</div></div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════ TAB 2 ══════════════════════ -->
<div class="tab-panel" id="panel1">

  <div class="sim-box">
    <div class="sim-header">
      <span class="sim-title">🎮 시뮬레이션 — 슬라이더로 채소밭 크기를 바꿔 보세요!</span>
      <span class="sim-result" id="sr2">새 넓이 S ≈ 40.3 m²</span>
    </div>
    <div class="sim-body">
      <canvas id="c2" width="380" height="200"></canvas>
      <div class="sim-right">
        <div class="slider-row">
          <span class="slider-lbl">줄이는 가로 x (m):</span>
          <input type="range" id="sl2" min="0.1" max="5.9" step="0.05" value="2.33" oninput="drawP2()">
          <span class="slider-val" id="sv2">2.33 m</span>
        </div>
        <div class="sim-note" id="sn2">🏆 최댓값: x=7/3m일 때 121/3≈40.3m²</div>
      </div>
    </div>
  </div>

  <div class="bottom-row">
    <div class="problem-card">
      <div class="problem-icon">🌱</div>
      <div class="problem-title">상황 2. 채소밭 리모델링</div>
      <div class="problem-desc">가로 <strong>6 m</strong>, 세로 <strong>4 m</strong>인 직사각형 채소밭이 있습니다. 가로를 <strong>x m</strong> 줄이고, 세로를 <strong>3x m</strong> 늘려서 새로운 채소밭을 만들려고 합니다.</div>
      <div class="problem-question">❓ 새로운 채소밭의 넓이의 <strong>최댓값</strong>을 구하시오. (단, 0 &lt; x &lt; 6)</div>
      <div class="intro-bar">
        <div class="is"><span class="n">①</span><span class="l">조건·목표<br>확인</span></div>
        <div class="is"><span class="n">②</span><span class="l">변수·<br>범위</span></div>
        <div class="is"><span class="n">③</span><span class="l">관계식<br>세우기</span></div>
        <div class="is"><span class="n">④</span><span class="l">최댓값<br>찾기</span></div>
        <div class="is"><span class="n">⑤</span><span class="l">답<br>해석</span></div>
      </div>
    </div>

    <div class="steps-panel">
      <div class="steps-label">📋 각 단계를 클릭하고 빈칸을 채워보세요!</div>
      <div class="steps-container">

        <div class="step-item s1" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">①</span><span class="step-htxt">주어진 조건과 구하려는 것을 확인한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>• 원래 채소밭: 가로 <span class="hi">6 m</span>, 세로 <span class="hi">4 m</span>, 넓이 24 m²</p>
            <p>• 가로를 x m 줄이고, 세로를 3x m 늘림</p>
            <p>• 구하려는 것: 새 채소밭 넓이의 <span class="hi">최댓값</span></p>
          </div>
        </div>

        <div class="step-item s2" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">②</span><span class="step-htxt">변수를 결정하고, 변수의 범위를 구한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>• 새 가로 = 6−x &gt; 0 이어야 하므로 x &lt; 6</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ x의 범위로 알맞은 것은?</span>
              <div class="mc-opts">
                <button class="mc-btn" onclick="checkMC('p2_s2',this,false,'rv_p2_s2','가로 조건에서 x&lt;6입니다.')">① 0&lt;x&lt;4</button>
                <button class="mc-btn" onclick="checkMC('p2_s2',this,true,'rv_p2_s2','')">② 0&lt;x&lt;6</button>
                <button class="mc-btn" onclick="checkMC('p2_s2',this,false,'rv_p2_s2','x=6이면 가로=0, 열린구간입니다.')">③ 0≤x≤6</button>
                <button class="mc-btn" onclick="checkMC('p2_s2',this,false,'rv_p2_s2','x&gt;6이면 가로가 음수입니다.')">④ 0&lt;x&lt;12</button>
              </div>
              <div class="q-fb" id="fb_p2_s2"></div>
              <div class="reveal" id="rv_p2_s2"><div class="formula">범위: 0 &lt; x &lt; 6</div></div>
            </div>
          </div>
        </div>

        <div class="step-item s3" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">③</span><span class="step-htxt">변수 사이의 관계식을 세운다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>• 새 넓이 S = (6−x)(4+3x) = 24+18x−4x−3x²</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ S = −3x² + □x + 24 &nbsp; □를 구하세요</span>
              <div class="q-row">
                <span class="q-text">S = −3x² +</span>
                <input class="q-input" id="i_p2_s3" type="number" placeholder="?">
                <span class="q-text">x + 24</span>
                <button class="q-btn" onclick="checkFill('p2_s3',14,0.1,'rv_p2_s3')">확인</button>
              </div>
              <div class="q-fb" id="fb_p2_s3"></div>
              <div class="reveal" id="rv_p2_s3"><div class="formula">18x−4x = 14x → S = −3x²+14x+24</div></div>
            </div>
          </div>
        </div>

        <div class="step-item s4" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">④</span><span class="step-htxt">구하는 값을 관계식을 이용하여 찾는다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>꼭짓점 x = 14÷(2×3) ≈ 2.33 (0&lt;x&lt;6 내 포함)</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 꼭짓점 x좌표를 소수로 입력하세요 (반올림 둘째자리)</span>
              <div class="q-row">
                <span class="q-text">x =</span>
                <input class="q-input" id="i_p2_s4" type="number" step="0.01" placeholder="?">
                <button class="q-btn" onclick="checkFill('p2_s4',2.333,0.06,'rv_p2_s4')">확인</button>
              </div>
              <div class="q-fb" id="fb_p2_s4"></div>
              <div class="reveal" id="rv_p2_s4"><div class="formula">x=7/3≈2.33 일 때 S 최댓값 = 121/3 ≈ 40.3 m²</div></div>
            </div>
          </div>
        </div>

        <div class="step-item s5" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">⑤</span><span class="step-htxt">문제에 맞게 답을 해석한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>x=7/3일 때 &nbsp;새 세로 = 4+3×(7/3) = 4+7 = ?</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ x=7/3일 때 새 세로의 길이는?</span>
              <div class="q-row">
                <span class="q-text">새 세로 =</span>
                <input class="q-input" id="i_p2_s5" type="number" placeholder="?">
                <span class="q-text">m</span>
                <button class="q-btn" onclick="checkFill('p2_s5',11,0.1,'rv_p2_s5')">확인</button>
              </div>
              <div class="q-fb" id="fb_p2_s5"></div>
              <div class="reveal" id="rv_p2_s5"><div class="formula">새 가로≈3.67m, 새 세로=11m → 최댓값=121/3≈40.3 m²</div></div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════ TAB 3 ══════════════════════ -->
<div class="tab-panel" id="panel2">

  <div class="sim-box">
    <div class="sim-header">
      <span class="sim-title">🎮 시뮬레이션 — 로켓을 직접 발사해 보세요!</span>
      <span class="sim-result" id="sr3">발사 대기 중... 🚀</span>
    </div>
    <div class="sim-body">
      <canvas id="c3" width="380" height="200"></canvas>
      <div class="sim-right">
        <div class="rocket-btns">
          <button class="btn btn-fire" onclick="launchRocket()">🚀 발사!</button>
          <button class="btn btn-rst" onclick="resetRocket()">🔄 초기화</button>
        </div>
        <div class="sim-note">최고 높이: 발사 후 1.4초에 12.8 m 도달</div>
      </div>
    </div>
  </div>

  <div class="bottom-row">
    <div class="problem-card">
      <div class="problem-icon">🚀</div>
      <div class="problem-title">상황 3. 불꽃놀이 로켓 발사</div>
      <div class="problem-desc">로켓을 지면으로부터 <strong>3 m 높이</strong> 발사대에서 발사합니다. 발사 후 t초의 높이 h m는 <strong>h = −5t² + at + 3</strong> 이고, <strong>3초 후</strong> 지면에 떨어졌습니다.</div>
      <div class="problem-question">❓ (1) 상수 a의 값을 구하시오.<br>❓ (2) 로켓 높이의 <strong>최댓값</strong>을 구하시오.</div>
      <div class="intro-bar">
        <div class="is"><span class="n">①</span><span class="l">조건·목표<br>확인</span></div>
        <div class="is"><span class="n">②</span><span class="l">변수·<br>범위</span></div>
        <div class="is"><span class="n">③</span><span class="l">a값<br>구하기</span></div>
        <div class="is"><span class="n">④</span><span class="l">최댓값<br>찾기</span></div>
        <div class="is"><span class="n">⑤</span><span class="l">답<br>해석</span></div>
      </div>
    </div>

    <div class="steps-panel">
      <div class="steps-label">📋 각 단계를 클릭하고 빈칸을 채워보세요!</div>
      <div class="steps-container">

        <div class="step-item s1" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">①</span><span class="step-htxt">주어진 조건과 구하려는 것을 확인한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>• t=0일 때 h=3 (발사대 높이 3m)</p>
            <p>• h = −5t²+at+3 (높이 공식)</p>
            <p>• t=3일 때 h=0 (3초 후 지면)</p>
            <p>• 구하려는 것: ① a의 값 &nbsp; ② 높이의 <span class="hi">최댓값</span></p>
          </div>
        </div>

        <div class="step-item s2" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">②</span><span class="step-htxt">변수를 결정하고, 변수의 범위를 구한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>• 변수: 경과 시간 <span class="hi">t 초</span></p>
            <p>• 발사 t=0, 지면 t=3</p>
            <div class="formula">범위: 0 ≤ t ≤ 3</div>
          </div>
        </div>

        <div class="step-item s3" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">③</span><span class="step-htxt">관계식으로 상수 a를 구한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>h(3)=0: −5(9)+3a+3=0 → −45+3a+3=0 → 3a=42</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 상수 a의 값은?</span>
              <div class="q-row">
                <span class="q-text">a =</span>
                <input class="q-input" id="i_p3_s3" type="number" placeholder="?">
                <button class="q-btn" onclick="checkFill('p3_s3',14,0.1,'rv_p3_s3')">확인</button>
              </div>
              <div class="q-fb" id="fb_p3_s3"></div>
              <div class="reveal" id="rv_p3_s3"><div class="formula">a=14 → h = −5t²+14t+3</div></div>
            </div>
          </div>
        </div>

        <div class="step-item s4" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">④</span><span class="step-htxt">구하는 값을 관계식을 이용하여 찾는다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>꼭짓점 t = 14÷(2×5) = 1.4초 &nbsp;(0≤t≤3 내 포함)</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ h(1.4)를 계산하여 최대 높이를 구하세요:</span>
              <div class="q-row">
                <span class="q-text">h 최댓값 =</span>
                <input class="q-input" id="i_p3_s4" type="number" step="0.1" placeholder="?">
                <span class="q-text">m</span>
                <button class="q-btn" onclick="checkFill('p3_s4',12.8,0.15,'rv_p3_s4')">확인</button>
              </div>
              <div class="q-fb" id="fb_p3_s4"></div>
              <div class="reveal" id="rv_p3_s4"><div class="formula">−5(1.96)+14(1.4)+3 = −9.8+19.6+3 = 12.8 m</div></div>
            </div>
          </div>
        </div>

        <div class="step-item s5" onclick="toggleStep(this)">
          <div class="step-header"><span class="step-num">⑤</span><span class="step-htxt">문제에 맞게 답을 해석한다</span><span class="step-arr">▼</span></div>
          <div class="step-body">
            <p>(1) a=14 &nbsp;&nbsp; (2) 발사 후 1.4초에 최고 높이 도달</p>
            <div class="q-box" onclick="event.stopPropagation()">
              <span class="q-label">✏️ 로켓 높이의 최댓값으로 알맞은 것은?</span>
              <div class="mc-opts">
                <button class="mc-btn" onclick="checkMC('p3_s5',this,false,'rv_p3_s5','9.8m은 최고점이 아닙니다.')">① 9.8 m</button>
                <button class="mc-btn" onclick="checkMC('p3_s5',this,true,'rv_p3_s5','')">② 12.8 m</button>
                <button class="mc-btn" onclick="checkMC('p3_s5',this,false,'rv_p3_s5','14는 a의 값이지 높이가 아닙니다.')">③ 14 m</button>
                <button class="mc-btn" onclick="checkMC('p3_s5',this,false,'rv_p3_s5','17m는 잘못된 계산입니다.')">④ 17 m</button>
              </div>
              <div class="q-fb" id="fb_p3_s5"></div>
              <div class="reveal" id="rv_p3_s5"><div class="formula">로켓 높이의 최댓값 = 12.8 m (발사 후 1.4초)</div></div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>

<script>
/* ══ TAB / STEP ══ */
function switchTab(idx){
  document.querySelectorAll('.tab-btn').forEach((b,i)=>b.classList.toggle('active',i===idx));
  document.querySelectorAll('.tab-panel').forEach((p,i)=>p.classList.toggle('active',i===idx));
  if(idx===0) setTimeout(drawP1,30);
  if(idx===1) setTimeout(drawP2,30);
  if(idx===2) setTimeout(initRocket,30);
}
function toggleStep(el){
  const panel=el.closest('.steps-container');
  const wasOpen=el.classList.contains('open');
  panel.querySelectorAll('.step-item').forEach(s=>s.classList.remove('open'));
  if(!wasOpen) el.classList.add('open');
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
  } else {
    fb.textContent='❌ 다시 계산해 보세요.';fb.className='q-fb ng';
    inp.classList.add('err');setTimeout(()=>inp.classList.remove('err'),600);
  }
}
function checkMC(id,btn,isOk,revId,hint){
  const fb=document.getElementById('fb_'+id);
  if(isOk){
    btn.classList.add('mc-ok');
    btn.parentElement.querySelectorAll('.mc-btn').forEach(b=>b.disabled=true);
    fb.textContent='✅ 정답입니다!';fb.className='q-fb ok';
    const rv=document.getElementById(revId);if(rv)rv.style.display='block';
  } else {
    btn.classList.add('mc-ng');
    fb.textContent='❌ '+hint;fb.className='q-fb ng';
    setTimeout(()=>btn.classList.remove('mc-ng'),800);
    setTimeout(()=>{if(fb.className==='q-fb ng')fb.textContent='';},2500);
  }
}

/* ══ CANVAS ══ */
function cw(id){
  const c=document.getElementById(id);
  const W=Math.min(380,document.body.clientWidth*0.46);
  c.width=W;return W;
}

/* ══ SIM 1 ══ */
function drawP1(){
  const W=cw('c1');
  const c=document.getElementById('c1'),ctx=c.getContext('2d'),H=c.height;
  const x=parseFloat(document.getElementById('sl1').value);
  const y=24-2*x,S=x*y,isMax=Math.abs(x-6)<0.12;
  document.getElementById('sv1').textContent=x.toFixed(1)+' m';
  document.getElementById('sr1').textContent='넓이 S = '+S.toFixed(1)+' m²';
  const sn=document.getElementById('sn1');
  sn.textContent=isMax?'🏆 최댓값 달성! S = 72 m²':'🏆 최댓값: x=6m일 때 72m²';
  sn.style.color=isMax?'#ffd700':'#ff9944';

  ctx.clearRect(0,0,W,H);ctx.fillStyle='#060c1a';ctx.fillRect(0,0,W,H);
  const sc=Math.min((W-60)/Math.max(y,2),(H-72)/Math.max(x,1))*0.75;
  const rW=y*sc,rH=x*sc,ox=(W-rW)/2,oy=36;

  ctx.fillStyle='#4a3a2a';ctx.fillRect(ox-6,oy-17,rW+12,17);
  ctx.fillStyle='#6a5a4a';
  for(let bx=0;bx<rW+12;bx+=24){ctx.fillRect(ox-6+bx+1,oy-17+1,22,7);ctx.fillRect(ox-6+bx-11+1,oy-10+1,22,7);}
  ctx.fillStyle='#aaa';ctx.font='10px sans-serif';ctx.textAlign='center';
  ctx.fillText('🏠 건물 벽',ox+rW/2,oy-5);

  const g=ctx.createLinearGradient(ox,oy,ox,oy+rH);
  g.addColorStop(0,'#1a4a1a');g.addColorStop(1,'#0d2e0d');
  ctx.fillStyle=g;ctx.fillRect(ox,oy,rW,rH);

  const fc=isMax?'#ffd700':'#27ae60';
  ctx.strokeStyle=fc;ctx.lineWidth=2.5;
  [[ox,oy,ox,oy+rH],[ox+rW,oy,ox+rW,oy+rH],[ox,oy+rH,ox+rW,oy+rH]].forEach(([x1,y1,x2,y2])=>{
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
  });

  ctx.font='18px serif';ctx.textAlign='center';
  ctx.fillText('🐕',ox+rW*0.45,oy+rH*0.52+7);
  ctx.fillText('🎾',ox+rW*0.72,oy+rH*0.6+7);

  ctx.fillStyle='#99aacc';ctx.font='11px Malgun Gothic';ctx.textAlign='center';
  ctx.fillText('y='+y.toFixed(1)+'m',ox+rW/2,oy+rH+16);
  ctx.save();ctx.translate(ox-18,oy+rH/2);ctx.rotate(-Math.PI/2);
  ctx.fillText('x='+x.toFixed(1)+'m',0,0);ctx.restore();

  /* mini graph */
  const gx=W-82,gy=6,gw=76,gh=56;
  ctx.fillStyle='rgba(8,14,28,.9)';ctx.fillRect(gx,gy,gw,gh);
  ctx.strokeStyle='#2a3d6a';ctx.lineWidth=1;ctx.strokeRect(gx,gy,gw,gh);
  ctx.beginPath();
  for(let i=0;i<=80;i++){const xi=0.5+i*0.1375;const si=xi*(24-2*xi);
    const px=gx+2+(xi-0.5)/11*(gw-4);const py=gy+gh-2-si/72*(gh-4);
    i===0?ctx.moveTo(px,py):ctx.lineTo(px,py);}
  ctx.strokeStyle='#4488ff';ctx.lineWidth=1.5;ctx.stroke();
  const mx=gx+2+(x-0.5)/11*(gw-4);const my=gy+gh-2-S/72*(gh-4);
  ctx.beginPath();ctx.arc(mx,my,3.5,0,Math.PI*2);ctx.fillStyle='#ffd700';ctx.fill();
  ctx.fillStyle='#446688';ctx.font='8px sans-serif';ctx.textAlign='center';
  ctx.fillText('S(x)',gx+gw/2,gy+8);
}

/* ══ SIM 2 ══ */
function drawP2(){
  const W=cw('c2');
  const c=document.getElementById('c2'),ctx=c.getContext('2d'),H=c.height;
  const x=parseFloat(document.getElementById('sl2').value);
  const nw=6-x,nh=4+3*x,S=nw*nh,isMax=Math.abs(x-7/3)<0.08;
  document.getElementById('sv2').textContent=x.toFixed(2)+' m';
  document.getElementById('sr2').textContent='새 넓이 S = '+S.toFixed(2)+' m²';
  const sn=document.getElementById('sn2');
  sn.textContent=isMax?'🏆 최댓값 달성! 121/3≈40.3m²':'🏆 최댓값: x=7/3m일 때 121/3≈40.3m²';
  sn.style.color=isMax?'#ffd700':'#ff9944';

  ctx.clearRect(0,0,W,H);ctx.fillStyle='#060c1a';ctx.fillRect(0,0,W,H);
  const maxD=Math.max(6,nw,4,nh);
  const sc=Math.min((W/2-36)/maxD,(H-60)/maxD)*0.82;
  const mid=W/2;
  const oW=6*sc,oH=4*sc,oX=mid-oW-16,oY=(H-oH)/2+2;
  ctx.fillStyle='#1a2540';ctx.fillRect(oX,oY,oW,oH);
  ctx.strokeStyle='#4488ff';ctx.lineWidth=2;ctx.strokeRect(oX,oY,oW,oH);
  ctx.fillStyle='#88aaff';ctx.font='10px Malgun Gothic';ctx.textAlign='center';
  ctx.fillText('원래 채소밭',oX+oW/2,oY-5);
  ctx.fillStyle='#667799';ctx.font='9px Malgun Gothic';
  ctx.fillText('6m×4m=24m²',oX+oW/2,oY+oH+12);
  ctx.font='16px serif';ctx.fillText('🥕🌽',oX+oW/2,oY+oH/2+6);

  ctx.fillStyle='#445577';ctx.font='16px serif';ctx.textAlign='center';
  ctx.fillText('→',mid,H/2+5);

  const nW2=nw*sc,nH2=nh*sc,nX=mid+16,nY=(H-nH2)/2+2;
  const ng=ctx.createLinearGradient(nX,nY,nX+nW2,nY+nH2);
  ng.addColorStop(0,isMax?'#2a4a12':'#152a10');ng.addColorStop(1,isMax?'#1a3a08':'#0a1e08');
  ctx.fillStyle=ng;ctx.fillRect(nX,nY,nW2,nH2);
  ctx.strokeStyle=isMax?'#ffd700':'#27ae60';ctx.lineWidth=2;ctx.strokeRect(nX,nY,nW2,nH2);
  ctx.fillStyle=isMax?'#ffd700':'#aaddaa';ctx.font='10px Malgun Gothic';ctx.textAlign='center';
  ctx.fillText('새 채소밭',nX+nW2/2,nY-5);
  ctx.fillStyle=isMax?'#ffd700':'#889977';ctx.font='9px Malgun Gothic';
  ctx.fillText(nw.toFixed(1)+'m×'+nh.toFixed(1)+'m',nX+nW2/2,nY+nH2+12);
  ctx.fillText('='+S.toFixed(1)+'m²',nX+nW2/2,nY+nH2+23);
  ctx.font=Math.min(16,nH2*0.25)+'px serif';ctx.fillText('🥦🌿',nX+nW2/2,nY+nH2/2+6);

  /* mini graph */
  const gx=W-82,gy=6,gw=76,gh=56;
  ctx.fillStyle='rgba(8,14,28,.9)';ctx.fillRect(gx,gy,gw,gh);
  ctx.strokeStyle='#2a3d6a';ctx.lineWidth=1;ctx.strokeRect(gx,gy,gw,gh);
  ctx.beginPath();
  for(let i=0;i<=80;i++){const xi=0.1+i*0.0725;const si=(6-xi)*(4+3*xi);
    const px=gx+2+(xi-0.1)/5.8*(gw-4);const py=gy+gh-2-si/(121/3)*(gh-4);
    i===0?ctx.moveTo(px,py):ctx.lineTo(px,py);}
  ctx.strokeStyle='#27ae60';ctx.lineWidth=1.5;ctx.stroke();
  const mx2=gx+2+(x-0.1)/5.8*(gw-4);const my2=gy+gh-2-S/(121/3)*(gh-4);
  ctx.beginPath();ctx.arc(mx2,my2,3.5,0,Math.PI*2);ctx.fillStyle='#ffd700';ctx.fill();
  ctx.fillStyle='#336633';ctx.font='8px sans-serif';ctx.textAlign='center';
  ctx.fillText('S(x)',gx+gw/2,gy+8);
}

/* ══ SIM 3: ROCKET ══ */
let rafId=null,rT=0,trail=[],launched=false;
function hRkt(t){return -5*t*t+14*t+3;}
function initRocket(){resetRocket();}
function resetRocket(){
  if(rafId){cancelAnimationFrame(rafId);rafId=null;}
  rT=0;trail=[];launched=false;
  document.getElementById('sr3').textContent='발사 대기 중... 🚀';
  drawRocketFrame(0);
}
function launchRocket(){
  if(launched){resetRocket();return;}
  launched=true;rT=0;trail=[];step3();
}
function step3(){
  rT+=0.025;
  if(rT>3.05){
    document.getElementById('sr3').textContent='💥 지면 도달! (3초 후)';
    drawRocketFrame(3.05);launched=false;return;
  }
  const h=Math.max(0,hRkt(rT));
  const peak=rT>=1.35&&rT<=1.45;
  document.getElementById('sr3').textContent='t='+rT.toFixed(2)+'초  h='+h.toFixed(2)+'m'+(peak?' ✨ 최고점!':'');
  trail.push({t:rT,h});drawRocketFrame(rT);rafId=requestAnimationFrame(step3);
}
function drawRocketFrame(t){
  const W=cw('c3');
  const c=document.getElementById('c3'),ctx=c.getContext('2d'),H=c.height;
  ctx.clearRect(0,0,W,H);ctx.fillStyle='#060c1a';ctx.fillRect(0,0,W,H);
  /* stars */
  ctx.fillStyle='rgba(255,255,255,.4)';
  [[50,14],[120,30],[200,10],[280,26],[340,7],[60,46],[300,42]].forEach(([sx,sy])=>{
    if(sx<W){ctx.beginPath();ctx.arc(sx,sy,1,0,Math.PI*2);ctx.fill();}
  });
  const maxH=16,groundY=H-28,scY=(groundY-38)/maxH,rX=W*0.36;
  ctx.fillStyle='#3a2a1a';ctx.fillRect(0,groundY,W,H-groundY);
  ctx.fillStyle='#5a7a3a';ctx.fillRect(0,groundY-2,W,4);
  const platY=groundY-3*scY;
  ctx.fillStyle='#5a5a6a';ctx.fillRect(rX-16,platY,32,3*scY);
  ctx.fillStyle='#7a7a8a';ctx.fillRect(rX-18,platY-3,36,6);
  /* y axis */
  ctx.strokeStyle='#1e3060';ctx.lineWidth=1;ctx.setLineDash([2,3]);
  ctx.beginPath();ctx.moveTo(W*0.13,22);ctx.lineTo(W*0.13,groundY);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='#445577';ctx.font='9px Malgun Gothic';ctx.textAlign='right';
  [0,3,6,9,12,15].forEach(hm=>{
    const hy=groundY-hm*scY;if(hy>20){
      ctx.fillText(hm+'m',W*0.13-3,hy+3);
      ctx.beginPath();ctx.strokeStyle='#1a2d40';ctx.lineWidth=.5;
      ctx.moveTo(W*0.13,hy);ctx.lineTo(W*0.16,hy);ctx.stroke();
    }
  });
  /* max line */
  const mY=groundY-12.8*scY;
  ctx.strokeStyle='rgba(255,215,0,.35)';ctx.lineWidth=1;ctx.setLineDash([4,3]);
  ctx.beginPath();ctx.moveTo(W*0.13,mY);ctx.lineTo(W*0.72,mY);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='rgba(255,215,0,.7)';ctx.font='9px Malgun Gothic';ctx.textAlign='left';
  if(W*0.73<W-2)ctx.fillText('12.8m',W*0.73,mY+3);
  /* trail */
  if(trail.length>1){
    ctx.beginPath();trail.forEach((pt,i)=>{const py=groundY-Math.max(0,pt.h)*scY;i===0?ctx.moveTo(rX,py):ctx.lineTo(rX,py);});
    ctx.strokeStyle='rgba(255,140,50,.55)';ctx.lineWidth=2;ctx.stroke();
    trail.forEach((pt,i)=>{if(i%8===0){ctx.beginPath();ctx.arc(rX,groundY-Math.max(0,pt.h)*scY,2,0,Math.PI*2);ctx.fillStyle='rgba(255,200,80,.6)';ctx.fill();}});
    /* mini h(t) */
    const gx=W-80,gy=6,gw=74,gh=52;
    ctx.fillStyle='rgba(8,14,28,.9)';ctx.fillRect(gx,gy,gw,gh);
    ctx.strokeStyle='#2a3d6a';ctx.lineWidth=1;ctx.strokeRect(gx,gy,gw,gh);
    ctx.beginPath();trail.forEach((pt,i)=>{const px=gx+3+pt.t/3*(gw-6);const py=gy+gh-3-Math.max(0,pt.h)/13*(gh-6);i===0?ctx.moveTo(px,py):ctx.lineTo(px,py);});
    ctx.strokeStyle='#4f9cf9';ctx.lineWidth=1.5;ctx.stroke();
    ctx.fillStyle='#4466aa';ctx.font='8px sans-serif';ctx.textAlign='center';ctx.fillText('h(t)',gx+gw/2,gy+8);
  }
  const h=Math.max(0,hRkt(Math.min(t,3)));
  const rY=groundY-h*scY;
  if(t>0&&t<3.05&&h>0.1){
    const fg=ctx.createRadialGradient(rX,rY+13,0,rX,rY+16,10);
    fg.addColorStop(0,'rgba(255,220,50,.9)');fg.addColorStop(.4,'rgba(255,100,30,.7)');fg.addColorStop(1,'rgba(255,50,0,0)');
    ctx.fillStyle=fg;ctx.beginPath();ctx.ellipse(rX,rY+15,4,11,0,0,Math.PI*2);ctx.fill();
  }
  ctx.font='20px serif';ctx.textAlign='center';
  if(t>=3.05||h<0.05)ctx.fillText('💥',rX,groundY-3);
  else ctx.fillText('🚀',rX,rY+8);
  ctx.fillStyle='#99aacc';ctx.font='10px Malgun Gothic';ctx.textAlign='left';
  const td=Math.min(t,3);
  ctx.fillText('t='+td.toFixed(2)+'초',W*0.5,30);
  ctx.fillText('h='+Math.max(0,hRkt(td)).toFixed(2)+'m',W*0.5,44);
}

/* ══ 레이아웃 높이 자동 조정 ══ */
function setLayout(){
  const vh=window.innerHeight||700;
  /* 탭버튼: ~34px, 바디패딩: 26px */
  const avail=vh-34-26;
  const simH=Math.round(avail*0.34);
  const botH=avail-simH-8;
  document.querySelectorAll('.sim-box canvas').forEach(cv=>{cv.height=Math.max(140,simH-52);});
  document.querySelectorAll('.bottom-row').forEach(r=>{r.style.height=botH+'px';});
  /* steps-panel은 overflow hidden — 높이만 맞춤 */
  document.querySelectorAll('.steps-panel').forEach(p=>{p.style.height=botH+'px';});
}

window.addEventListener('load',()=>{setLayout();drawP1();});
window.addEventListener('resize',()=>{setLayout();
  const active=[...document.querySelectorAll('.tab-panel.active')];
  if(active[0]?.id==='panel0')drawP1();
  else if(active[0]?.id==='panel1')drawP2();
  else drawRocketFrame(0);
});
</script>
</body>
</html>"""


def render():
    st.markdown("### 🏗️ 이차함수 최대·최소 실생활 탐구")
    st.markdown(
        "실생활 속 이차함수의 최대·최소 문제를 **5단계 풀이 순서**로 분석하고, "
        "각 단계에서 **직접 계산하여 빈칸을 채워보세요!**"
    )
    components.html(_HTML, height=940, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
