# activities/common/mini/quad_func_equation_explorer.py
"""
이차함수와 이차방정식의 관계 탐구
이차방정식 ax²+bx+c=0의 근과 y=ax²+bx+c 그래프의 x절편이
같음을 인터랙티브 그래프로 탐구합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "이차함수방정식관계"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "근과x절편관계",
        "label":  "이차방정식 ax²+bx+c=0의 근과 이차함수 y=ax²+bx+c 그래프의 x절편이 같은 이유를 판별식 D=b²−4ac와 연결하여 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "판별식의미",
        "label":  "D>0, D=0, D<0일 때 이차함수 그래프와 x축의 위치 관계(교점의 개수)가 어떻게 다른지 설명하세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "근의범위조건",
        "label":  "a>0인 이차함수 f(x)=ax²+bx+c에서 f(p)<0이면 p가 두 근 사이에 있다고 할 수 있는 이유를 그래프로 설명하세요.",
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
    "title":       "📈 이차함수·방정식 그래프 탐구",
    "description": "이차방정식의 근과 이차함수 그래프의 x절편 관계, 판별식, 근의 범위를 인터랙티브 그래프로 직접 탐구합니다.",
    "order":       230,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>이차함수와 이차방정식 탐구</title>
<style>
html { font-size: 16px; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', system-ui, sans-serif;
  background: linear-gradient(155deg, #060917 0%, #0e1630 60%, #080f1c 100%);
  color: #e2e8ff;
  padding: 14px 12px 24px;
  min-height: 100vh;
}

/* ── Tabs ── */
.tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
}
.tab {
  flex: 1;
  padding: 10px 4px;
  border: none;
  border-radius: 10px;
  background: rgba(255,255,255,0.06);
  color: #94a3b8;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: 0.2s;
  font-family: inherit;
  line-height: 1.4;
}
.tab.active {
  background: linear-gradient(135deg, #7c3aed, #1d4ed8);
  color: #fff;
}
.tab.done { background: rgba(52,211,153,0.15); color: #6ee7b7; }
.tab:hover:not(.active) { background: rgba(255,255,255,0.12); color: #c4b5fd; }

/* ── Screens ── */
.screen { display: none; animation: fadeIn 0.3s ease; }
.screen.active { display: block; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: none; }
}

/* ── Card ── */
.card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 14px;
  padding: 14px 16px;
  margin-bottom: 12px;
}
.card-title {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #a78bfa;
  margin-bottom: 10px;
}

/* ── Canvas ── */
.canvas-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}
canvas {
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.1);
  display: block;
  max-width: 100%;
}

/* ── Sliders ── */
.slider-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.slider-lbl {
  font-family: 'Times New Roman', Georgia, serif;
  font-style: italic;
  font-size: 1.15rem;
  color: #fde68a;
  min-width: 18px;
  text-align: center;
}
.slider-val {
  min-width: 38px;
  text-align: center;
  font-weight: 700;
  color: #c4b5fd;
  font-size: 1rem;
}
input[type="range"] {
  flex: 1;
  accent-color: #7c3aed;
  cursor: pointer;
  height: 4px;
  border-radius: 4px;
}

/* ── Info panel ── */
.info-panel {
  background: rgba(124,58,237,0.1);
  border: 1px solid rgba(124,58,237,0.25);
  border-radius: 10px;
  padding: 12px 14px;
  margin-top: 8px;
  font-size: 0.92rem;
  line-height: 1.9;
}
.disc-badge {
  font-size: 0.88rem;
  font-weight: 800;
  padding: 2px 9px;
  border-radius: 6px;
  display: inline-block;
  margin-left: 6px;
}
.disc-pos { background: rgba(52,211,153,0.18); color: #34d399; border: 1px solid rgba(52,211,153,0.35); }
.disc-zero { background: rgba(251,191,36,0.18); color: #fbbf24; border: 1px solid rgba(251,191,36,0.35); }
.disc-neg { background: rgba(248,113,113,0.18); color: #f87171; border: 1px solid rgba(248,113,113,0.35); }

/* ── Equation display ── */
.eq-display {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 1.25rem;
  font-style: italic;
  color: #e2e8ff;
  text-align: center;
  padding: 8px 10px;
  background: rgba(255,255,255,0.04);
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 10px;
}

/* ── Summary boxes ── */
.sum-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.sum-box {
  flex: 1;
  min-width: 100px;
  border-radius: 10px;
  padding: 10px 10px;
  text-align: center;
  font-size: 0.82rem;
  line-height: 1.7;
}
.sum-pos { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); }
.sum-zero { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.3); }
.sum-neg { background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3); }
.sum-head { font-weight: 800; margin-bottom: 3px; }
.sum-head-pos { color: #34d399; }
.sum-head-zero { color: #fbbf24; }
.sum-head-neg { color: #f87171; }

/* ── Quiz ── */
.quiz-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.score-bar { display: flex; gap: 5px; flex-wrap: wrap; }
.s-dot {
  width: 26px; height: 26px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.72rem; font-weight: 700;
  background: rgba(255,255,255,0.08);
  color: #64748b;
  border: 1px solid rgba(255,255,255,0.1);
  transition: 0.3s;
}
.s-dot.ok   { background: rgba(52,211,153,0.25); color: #34d399; border-color: rgba(52,211,153,0.5); }
.s-dot.fail { background: rgba(248,113,113,0.2); color: #f87171; border-color: rgba(248,113,113,0.4); }

.quiz-choices {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 12px;
}
@media (max-width: 440px) {
  .quiz-choices { grid-template-columns: 1fr; }
}
.qchoice {
  padding: 12px 6px;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  font-size: 0.84rem;
  font-weight: 700;
  color: #e2e8ff;
  transition: 0.18s;
  user-select: none;
  font-family: inherit;
  line-height: 1.5;
}
.qchoice:hover:not(:disabled)  { background: rgba(124,58,237,0.2); border-color: #7c3aed; }
.qchoice.correct    { background: rgba(52,211,153,0.2); border-color: #34d399; color: #6ee7b7; }
.qchoice.wrong      { background: rgba(248,113,113,0.15); border-color: #f87171; color: #f87171; }
.qchoice.show-right { background: rgba(52,211,153,0.12); border-color: rgba(52,211,153,0.5); color: #34d399; }

.quiz-fb {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 10px 12px;
  margin-top: 10px;
  font-size: 0.88rem;
  display: none;
}

/* ── Range analysis ── */
.cond-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.88rem;
  margin-bottom: 5px;
  flex-wrap: wrap;
}
.cond-badge {
  padding: 1px 8px;
  border-radius: 99px;
  font-size: 0.78rem;
  font-weight: 700;
}
.cond-ok { background: rgba(52,211,153,0.2); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.cond-no { background: rgba(248,113,113,0.2); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
.cond-na { background: rgba(100,116,139,0.2); color: #94a3b8; border: 1px solid rgba(100,116,139,0.3); }

.analysis-box {
  border-radius: 10px;
  padding: 12px 14px;
  margin-top: 10px;
  border: 1px solid rgba(255,255,255,0.1);
}

/* ── Buttons ── */
.btn {
  padding: 8px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.88rem;
  font-family: inherit;
  transition: 0.2s;
  background: linear-gradient(135deg, #7c3aed, #1d4ed8);
  color: #fff;
}
.btn:hover { opacity: 0.85; transform: translateY(-1px); }

/* ── Final score ── */
.final-card {
  display: none;
  text-align: center;
  padding: 20px;
}
.final-score { font-size: 2.2rem; font-weight: 800; color: #fde68a; margin: 8px 0; }

/* ── Range summary cards ── */
.range-sum { display: flex; flex-direction: column; gap: 8px; }
.rs-box {
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 0.84rem;
  line-height: 1.7;
}
.rs-box .rs-title { font-weight: 800; margin-bottom: 2px; }
.rs-purple { background: rgba(124,58,237,0.12); border: 1px solid rgba(124,58,237,0.3); }
.rs-yellow { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.3); }
.rs-green  { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); }
.math { font-family: 'Times New Roman', Georgia, serif; font-style: italic; color: #fde68a; }
</style>
</head>
<body>

<!-- ──────────── TABS ──────────── -->
<div class="tabs">
  <button class="tab active" onclick="switchTab(0)" id="tab0">🔍 탐구 1<br>그래프 조작</button>
  <button class="tab" onclick="switchTab(1)" id="tab1">📊 탐구 2<br>판별식 퀴즈</button>
  <button class="tab" onclick="switchTab(2)" id="tab2">🎯 탐구 3<br>근의 범위</button>
</div>

<!-- ══════════ SCREEN 1: 그래프 탐구 ══════════ -->
<div class="screen active" id="screen0">

  <div class="card">
    <div class="card-title">📐 이차함수 그래프 조작</div>
    <div class="eq-display" id="eq1">y = x²</div>
    <div class="canvas-wrap">
      <canvas id="mainCanvas" width="460" height="360"></canvas>
    </div>
    <div class="slider-row">
      <span class="slider-lbl">a</span>
      <input type="range" id="sA" min="-3" max="3" step="0.5" value="1">
      <span class="slider-val" id="vA">1</span>
    </div>
    <div class="slider-row">
      <span class="slider-lbl">b</span>
      <input type="range" id="sB" min="-6" max="6" step="0.5" value="0">
      <span class="slider-val" id="vB">0</span>
    </div>
    <div class="slider-row">
      <span class="slider-lbl">c</span>
      <input type="range" id="sC" min="-6" max="6" step="0.5" value="-4">
      <span class="slider-val" id="vC">-4</span>
    </div>
    <div class="info-panel" id="info1"></div>
  </div>

  <div class="card">
    <div class="card-title">💡 판별식과 그래프의 관계</div>
    <div style="font-size:0.88rem; color:#cbd5e1; line-height:1.8; margin-bottom:10px;">
      이차함수 <span class="math">y = ax² + bx + c</span>의 그래프와 <span class="math">x</span>축의 교점의 <span class="math">x</span>좌표가
      이차방정식 <span class="math">ax² + bx + c = 0</span>의 <b>해(근)</b>임을 슬라이더로 확인해 보세요.
    </div>
    <div class="sum-grid">
      <div class="sum-box sum-pos">
        <div class="sum-head sum-head-pos">D &gt; 0</div>
        <div>서로 다른 두 실근<br>x축과 두 점 교차<br>🟢🟢</div>
      </div>
      <div class="sum-box sum-zero">
        <div class="sum-head sum-head-zero">D = 0</div>
        <div>중근 (겹치는 근)<br>x축에 접함<br>🟡</div>
      </div>
      <div class="sum-box sum-neg">
        <div class="sum-head sum-head-neg">D &lt; 0</div>
        <div>서로 다른 두 허근<br>x축과 만나지 않음<br>🔴</div>
      </div>
    </div>
  </div>

</div>

<!-- ══════════ SCREEN 2: 판별식 퀴즈 ══════════ -->
<div class="screen" id="screen1">

  <div class="card">
    <div class="card-title">📊 그래프 보고 판별식 맞추기</div>
    <div class="quiz-nav">
      <div class="score-bar" id="scoreBar"></div>
      <span style="font-size:0.88rem; color:#64748b;" id="qProg">Q1 / 6</span>
    </div>
    <div class="eq-display" id="quizEq">y = ?</div>
    <div class="canvas-wrap">
      <canvas id="quizCanvas" width="400" height="300"></canvas>
    </div>
    <p style="font-size:0.84rem; color:#94a3b8; text-align:center; margin-bottom:2px;">
      이 이차방정식 <span class="math" id="quizEqEq">...</span> = 0의 근의 종류는?
    </p>
    <div class="quiz-choices">
      <button class="qchoice" onclick="checkAns(0)">
        서로 다른 두 실근<br><span style="color:#34d399; font-size:0.82rem;">D &gt; 0</span>
      </button>
      <button class="qchoice" onclick="checkAns(1)">
        중근<br><span style="color:#fbbf24; font-size:0.82rem;">D = 0</span>
      </button>
      <button class="qchoice" onclick="checkAns(2)">
        서로 다른 두 허근<br><span style="color:#f87171; font-size:0.82rem;">D &lt; 0</span>
      </button>
    </div>
    <div class="quiz-fb" id="quizFb"></div>
    <div style="display:flex; justify-content:flex-end; margin-top:10px;">
      <button class="btn" onclick="nextQ()" id="nextBtn" style="display:none;">다음 →</button>
    </div>
  </div>

  <div class="card final-card" id="finalCard">
    <div class="card-title">🏆 퀴즈 완료!</div>
    <div class="final-score" id="finalScore">0 / 6</div>
    <div style="color:#94a3b8; font-size:0.9rem;" id="finalMsg">-</div>
    <button class="btn" onclick="resetQuiz()" style="margin-top:14px;">다시 도전 🔄</button>
  </div>

</div>

<!-- ══════════ SCREEN 3: 근의 범위 ══════════ -->
<div class="screen" id="screen2">

  <div class="card">
    <div class="card-title">🎯 근의 범위 탐구 (a = 1 고정)</div>
    <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:8px;">
      슬라이더로 포물선 모양과 점 <span class="math" style="color:#f0abfc;">p</span>의 위치를 바꿔 보세요.
    </div>
    <div class="eq-display" id="eq3">y = x² − 4x + 3</div>
    <div class="canvas-wrap">
      <canvas id="rangeCanvas" width="460" height="360"></canvas>
    </div>
    <div class="slider-row">
      <span class="slider-lbl">b</span>
      <input type="range" id="rB" min="-6" max="6" step="0.5" value="-4">
      <span class="slider-val" id="rvB">-4</span>
    </div>
    <div class="slider-row">
      <span class="slider-lbl">c</span>
      <input type="range" id="rC" min="-6" max="6" step="0.5" value="3">
      <span class="slider-val" id="rvC">3</span>
    </div>
    <div class="slider-row">
      <span class="slider-lbl" style="color:#f0abfc;">p</span>
      <input type="range" id="rP" min="-5" max="5" step="0.25" value="4">
      <span class="slider-val" id="rvP" style="color:#f0abfc;">4</span>
    </div>
    <div class="analysis-box" id="rangeBox"></div>
  </div>

  <div class="card">
    <div class="card-title">📌 근의 범위 조건 정리 (a &gt; 0)</div>
    <div class="range-sum">
      <div class="rs-box rs-purple">
        <div class="rs-title" style="color:#c4b5fd;">두 실근이 모두 p보다 작다</div>
        <div style="font-family:'Times New Roman',serif; font-style:italic; color:#e2e8ff;">D ≥ 0, &nbsp; −b/2a &lt; p, &nbsp; f(p) &gt; 0</div>
      </div>
      <div class="rs-box rs-yellow">
        <div class="rs-title" style="color:#fde68a;">두 실근 사이에 p가 있다</div>
        <div style="font-family:'Times New Roman',serif; font-style:italic; color:#e2e8ff;">f(p) &lt; 0</div>
      </div>
      <div class="rs-box rs-green">
        <div class="rs-title" style="color:#34d399;">두 실근이 모두 p보다 크다</div>
        <div style="font-family:'Times New Roman',serif; font-style:italic; color:#e2e8ff;">D ≥ 0, &nbsp; p &lt; −b/2a, &nbsp; f(p) &gt; 0</div>
      </div>
    </div>
  </div>

</div>

<script>
// ═══════════════════════════════════════════════════════
//  UTILITIES
// ═══════════════════════════════════════════════════════
function round2(n) { return Math.round(n * 100) / 100; }

function fmtCoeff(n, isFirst) {
  const r = round2(n);
  if (isFirst) {
    if (r === 1) return '';
    if (r === -1) return '−';
    if (r < 0) return '−' + round2(-r);
    return '' + r;
  } else {
    if (r === 0) return null;   // will be skipped
    if (r === 1) return ' + ';
    if (r === -1) return ' − ';
    if (r > 0) return ' + ' + r;
    return ' − ' + round2(-r);
  }
}

function buildEq(a, b, c) {
  const ra = round2(a), rb = round2(b), rc = round2(c);
  let s = 'y = ';
  if (ra === 0) {
    // linear or constant
    if (rb !== 0) {
      s += (rb === 1 ? '' : rb === -1 ? '−' : rb < 0 ? '−' + round2(-rb) : '' + rb) + 'x';
      if (rc > 0) s += ' + ' + rc;
      else if (rc < 0) s += ' − ' + round2(-rc);
    } else {
      s += rc;
    }
    return s;
  }
  // a term
  if (ra === 1) s += 'x²';
  else if (ra === -1) s += '−x²';
  else if (ra < 0) s += '−' + round2(-ra) + 'x²';
  else s += ra + 'x²';
  // b term
  if (rb === 1) s += ' + x';
  else if (rb === -1) s += ' − x';
  else if (rb > 0) s += ' + ' + rb + 'x';
  else if (rb < 0) s += ' − ' + round2(-rb) + 'x';
  // c term
  if (rc > 0) s += ' + ' + rc;
  else if (rc < 0) s += ' − ' + round2(-rc);
  return s;
}

function buildEqRHS(a, b, c) {
  return buildEq(a, b, c).replace('y = ', '');
}

// ═══════════════════════════════════════════════════════
//  CANVAS DRAWING HELPERS
// ═══════════════════════════════════════════════════════
const SC = 38;   // scale: pixels per unit

function drawBG(ctx, W, H) {
  const g = ctx.createLinearGradient(0, 0, W, H);
  g.addColorStop(0, '#080d1e');
  g.addColorStop(1, '#0c1628');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, W, H);
}

function drawGrid(ctx, W, H, ox, oy) {
  ctx.strokeStyle = 'rgba(255,255,255,0.065)';
  ctx.lineWidth = 0.8;
  const minX = Math.floor(-ox / SC), maxX = Math.ceil((W - ox) / SC);
  const minY = Math.floor(-(H - oy) / SC), maxY = Math.ceil(oy / SC);
  for (let x = minX; x <= maxX; x++) {
    ctx.beginPath();
    ctx.moveTo(ox + x * SC, 0);
    ctx.lineTo(ox + x * SC, H);
    ctx.stroke();
  }
  for (let y = minY; y <= maxY; y++) {
    ctx.beginPath();
    ctx.moveTo(0, oy - y * SC);
    ctx.lineTo(W, oy - y * SC);
    ctx.stroke();
  }
}

function drawAxes(ctx, W, H, ox, oy) {
  ctx.strokeStyle = 'rgba(255,255,255,0.32)';
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(6, oy); ctx.lineTo(W - 6, oy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ox, 6); ctx.lineTo(ox, H - 6); ctx.stroke();

  // Arrow tips
  ctx.fillStyle = 'rgba(255,255,255,0.32)';
  ctx.beginPath(); ctx.moveTo(W - 6, oy); ctx.lineTo(W - 14, oy - 4); ctx.lineTo(W - 14, oy + 4); ctx.fill();
  ctx.beginPath(); ctx.moveTo(ox, 6); ctx.lineTo(ox - 4, 14); ctx.lineTo(ox + 4, 14); ctx.fill();

  // Axis labels
  ctx.fillStyle = 'rgba(255,255,255,0.5)';
  ctx.font = 'italic 13px Times New Roman';
  ctx.textAlign = 'left';   ctx.fillText('x', W - 8, oy - 7);
  ctx.textAlign = 'center'; ctx.fillText('y', ox + 12, 14);

  // Tick marks and numbers
  const minX = Math.floor(-ox / SC), maxX = Math.ceil((W - ox) / SC);
  const minY = Math.floor(-(H - oy) / SC), maxY = Math.ceil(oy / SC);
  ctx.fillStyle = 'rgba(255,255,255,0.32)';
  ctx.font = '10px Malgun Gothic';

  ctx.textAlign = 'center';
  for (let x = minX + 1; x < maxX; x++) {
    if (x === 0) continue;
    const px = ox + x * SC;
    ctx.fillText(x, px, oy + 13);
    ctx.beginPath(); ctx.moveTo(px, oy - 3); ctx.lineTo(px, oy + 3); ctx.stroke();
  }
  ctx.textAlign = 'right';
  for (let y = minY + 1; y < maxY; y++) {
    if (y === 0) continue;
    const py = oy - y * SC;
    ctx.fillText(y, ox - 5, py + 4);
    ctx.beginPath(); ctx.moveTo(ox - 3, py); ctx.lineTo(ox + 3, py); ctx.stroke();
  }
}

function drawParabola(ctx, W, H, ox, oy, a, b, c, color, glow) {
  if (Math.abs(a) < 0.001) return;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2.6;
  if (glow) { ctx.shadowColor = color; ctx.shadowBlur = 8; }
  ctx.beginPath();
  const xMin = (-ox / SC) - 0.2, xMax = ((W - ox) / SC) + 0.2;
  const steps = 280;
  let pen = false;
  for (let i = 0; i <= steps; i++) {
    const x = xMin + (xMax - xMin) * i / steps;
    const y = a * x * x + b * x + c;
    const px = ox + x * SC, py = oy - y * SC;
    if (py < -30 || py > H + 30) { if (pen) { ctx.stroke(); ctx.beginPath(); pen = false; } continue; }
    if (!pen) { ctx.moveTo(px, py); pen = true; } else { ctx.lineTo(px, py); }
  }
  if (pen) ctx.stroke();
  if (glow) ctx.shadowBlur = 0;
}

function drawXIntercepts(ctx, ox, oy, a, b, c) {
  const D = b * b - 4 * a * c;
  if (D < -1e-9) return;
  const sqD = Math.sqrt(Math.max(0, D));
  const x1 = (-b - sqD) / (2 * a), x2 = (-b + sqD) / (2 * a);
  const pts = Math.abs(x1 - x2) < 1e-9 ? [x1] : [x1, x2];
  for (const x of pts) {
    const px = ox + x * SC;
    // Glow ring
    ctx.strokeStyle = 'rgba(253,230,138,0.35)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(px, oy, 9, 0, Math.PI * 2); ctx.stroke();
    // Dot
    ctx.fillStyle = '#fde68a';
    ctx.shadowColor = '#fde68a'; ctx.shadowBlur = 10;
    ctx.beginPath(); ctx.arc(px, oy, 5, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
    // Label
    ctx.fillStyle = '#fde68a';
    ctx.font = 'bold 10px Malgun Gothic';
    ctx.textAlign = 'center';
    ctx.fillText('(' + round2(x) + ', 0)', px, oy - 15);
  }
}

function drawVertex(ctx, ox, oy, a, b, c) {
  if (Math.abs(a) < 0.001) return;
  const vx = -b / (2 * a), vy = c - b * b / (4 * a);
  const px = ox + vx * SC, py = oy - vy * SC;
  if (py < -20 || py > 9999) return;
  ctx.fillStyle = '#a78bfa';
  ctx.shadowColor = '#a78bfa'; ctx.shadowBlur = 8;
  ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.fillStyle = 'rgba(196,181,253,0.85)';
  ctx.font = '10px Malgun Gothic';
  ctx.textAlign = px > ox ? 'right' : 'left';
  const offset = px > ox ? -8 : 8;
  ctx.fillText('꼭짓점(' + round2(vx) + ', ' + round2(vy) + ')', px + offset, py - 8);
}

// ═══════════════════════════════════════════════════════
//  TAB 1 — MAIN GRAPH
// ═══════════════════════════════════════════════════════
const mc = document.getElementById('mainCanvas');
const mctx = mc.getContext('2d');
const MW = mc.width, MH = mc.height, MOX = MW / 2, MOY = MH / 2;

function updateMain() {
  const a = parseFloat(document.getElementById('sA').value);
  const b = parseFloat(document.getElementById('sB').value);
  const c = parseFloat(document.getElementById('sC').value);
  document.getElementById('vA').textContent = a;
  document.getElementById('vB').textContent = b;
  document.getElementById('vC').textContent = c;
  document.getElementById('eq1').textContent = buildEq(a, b, c);

  mctx.clearRect(0, 0, MW, MH);
  drawBG(mctx, MW, MH);
  drawGrid(mctx, MW, MH, MOX, MOY);
  drawAxes(mctx, MW, MH, MOX, MOY);

  if (Math.abs(a) < 0.001) {
    document.getElementById('info1').innerHTML =
      '<span style="color:#f87171;">⚠️ a = 0이면 이차함수가 아닙니다. a ≠ 0으로 설정해 주세요.</span>';
    return;
  }

  const D = b * b - 4 * a * c;
  const Dv = round2(D);
  let pColor, dClass, dText;
  if (D > 1e-9)       { pColor = '#34d399'; dClass = 'disc-pos';  dText = 'D &gt; 0'; }
  else if (D > -1e-9) { pColor = '#fbbf24'; dClass = 'disc-zero'; dText = 'D = 0'; }
  else                { pColor = '#f87171'; dClass = 'disc-neg';   dText = 'D &lt; 0'; }

  drawParabola(mctx, MW, MH, MOX, MOY, a, b, c, pColor, true);
  drawXIntercepts(mctx, MOX, MOY, a, b, c);
  drawVertex(mctx, MOX, MOY, a, b, c);

  // Info panel
  let rootLine;
  if (D > 1e-9) {
    const sq = Math.sqrt(D);
    const x1 = round2((-b - sq) / (2 * a)), x2 = round2((-b + sq) / (2 * a));
    const [lo, hi] = x1 < x2 ? [x1, x2] : [x2, x1];
    rootLine = `서로 다른 두 실근: <span style="color:#fde68a; font-style:italic;">x = ${lo}, &nbsp; x = ${hi}</span>`;
  } else if (D > -1e-9) {
    const x0 = round2(-b / (2 * a));
    rootLine = `중근: <span style="color:#fde68a; font-style:italic;">x = ${x0}</span>`;
  } else {
    rootLine = `<span style="color:#f87171;">실수 근 없음 (두 허근)</span>`;
  }

  const bSign = b < 0 ? `(${b})` : b === 0 ? '0' : `${b}`;
  const formulaD = `(${b})² − 4×(${a})×(${c}) = ${round2(b*b)} − ${round2(4*a*c)} = <b>${Dv}</b>`;

  document.getElementById('info1').innerHTML = `
    <div style="margin-bottom:6px;">
      판별식 <span style="font-family:'Times New Roman',serif;font-style:italic;color:#fde68a;">D = b² − 4ac</span>
      = ${formulaD}
      <span class="disc-badge ${dClass}">${dText}</span>
    </div>
    <div>이차방정식의 근: ${rootLine}</div>
  `;
}

['sA','sB','sC'].forEach(id => document.getElementById(id).addEventListener('input', updateMain));

// ═══════════════════════════════════════════════════════
//  TAB 2 — QUIZ
// ═══════════════════════════════════════════════════════
const QUIZ = [
  { a: 1,  b: -4, c: 3,  ans: 0, hint: 'D = (−4)² − 4×1×3 = 16 − 12 = 4 &gt; 0 → 서로 다른 두 실근' },
  { a: 1,  b:  2, c: 2,  ans: 2, hint: 'D = 2² − 4×1×2 = 4 − 8 = −4 &lt; 0 → 두 허근' },
  { a: 1,  b:  2, c: 1,  ans: 1, hint: 'D = 2² − 4×1×1 = 4 − 4 = 0 → 중근' },
  { a: -1, b:  2, c: 3,  ans: 0, hint: 'D = 2² − 4×(−1)×3 = 4 + 12 = 16 &gt; 0 → 서로 다른 두 실근' },
  { a: -1, b:  4, c: -4, ans: 1, hint: 'D = 4² − 4×(−1)×(−4) = 16 − 16 = 0 → 중근' },
  { a: -1, b:  0, c: -1, ans: 2, hint: 'D = 0² − 4×(−1)×(−1) = 0 − 4 = −4 &lt; 0 → 두 허근' },
];

const qc = document.getElementById('quizCanvas');
const qctx = qc.getContext('2d');
const QW = qc.width, QH = qc.height, QOX = QW / 2, QOY = QH / 2;
const QSC = 34;

let qIdx = 0, qDone = false;
const qRecord = Array(QUIZ.length).fill(null);

function drawQuizGraph(i, revealed) {
  const { a, b, c } = QUIZ[i];
  const D = b * b - 4 * a * c;
  qctx.clearRect(0, 0, QW, QH);
  drawBG(qctx, QW, QH);
  // Use QSC scale (slightly smaller than main)
  const qDrawGrid = (ctx, W, H, ox, oy) => {
    ctx.strokeStyle = 'rgba(255,255,255,0.065)'; ctx.lineWidth = 0.8;
    const mx = Math.floor(-ox / QSC), Mx = Math.ceil((W - ox) / QSC);
    const my = Math.floor(-(H - oy) / QSC), My = Math.ceil(oy / QSC);
    for (let x = mx; x <= Mx; x++) { ctx.beginPath(); ctx.moveTo(ox + x*QSC,0); ctx.lineTo(ox + x*QSC,H); ctx.stroke(); }
    for (let y = my; y <= My; y++) { ctx.beginPath(); ctx.moveTo(0,oy - y*QSC); ctx.lineTo(W,oy - y*QSC); ctx.stroke(); }
  };
  qDrawGrid(qctx, QW, QH, QOX, QOY);

  // Axes
  qctx.strokeStyle = 'rgba(255,255,255,0.32)'; qctx.lineWidth = 1.5;
  qctx.beginPath(); qctx.moveTo(6, QOY); qctx.lineTo(QW-6, QOY); qctx.stroke();
  qctx.beginPath(); qctx.moveTo(QOX, 6); qctx.lineTo(QOX, QH-6); qctx.stroke();
  qctx.fillStyle = 'rgba(255,255,255,0.32)';
  qctx.beginPath(); qctx.moveTo(QW-6,QOY); qctx.lineTo(QW-14,QOY-4); qctx.lineTo(QW-14,QOY+4); qctx.fill();
  qctx.beginPath(); qctx.moveTo(QOX,6); qctx.lineTo(QOX-4,14); qctx.lineTo(QOX+4,14); qctx.fill();
  qctx.fillStyle = 'rgba(255,255,255,0.45)'; qctx.font = 'italic 12px Times New Roman';
  qctx.textAlign = 'left'; qctx.fillText('x', QW-8, QOY-6);
  qctx.textAlign = 'center'; qctx.fillText('y', QOX+11, 14);
  // Tick numbers
  qctx.fillStyle = 'rgba(255,255,255,0.3)'; qctx.font = '9px Malgun Gothic';
  qctx.textAlign = 'center';
  for (let x = -5; x <= 5; x++) { if(!x) continue; qctx.fillText(x, QOX+x*QSC, QOY+12); }
  qctx.textAlign = 'right';
  for (let y = -4; y <= 4; y++) { if(!y) continue; qctx.fillText(y, QOX-5, QOY-y*QSC+4); }

  // Draw parabola - neutral blue until revealed
  let col = '#60a5fa';
  if (revealed) {
    if (D > 1e-9) col = '#34d399'; else if (D > -1e-9) col = '#fbbf24'; else col = '#f87171';
  }
  // Mini parabola drawing with QSC
  qctx.strokeStyle = col; qctx.lineWidth = 2.4;
  qctx.shadowColor = col; qctx.shadowBlur = revealed ? 8 : 4;
  qctx.beginPath();
  const xMn = -QOX/QSC - 0.2, xMx = (QW-QOX)/QSC + 0.2;
  let pen = false;
  for (let i2 = 0; i2 <= 260; i2++) {
    const x = xMn + (xMx - xMn) * i2 / 260;
    const y = a*x*x + b*x + c;
    const px = QOX + x*QSC, py = QOY - y*QSC;
    if (py < -30 || py > QH+30) { if(pen){ qctx.stroke(); qctx.beginPath(); pen=false; } continue; }
    if (!pen) { qctx.moveTo(px,py); pen=true; } else { qctx.lineTo(px,py); }
  }
  if (pen) qctx.stroke();
  qctx.shadowBlur = 0;

  if (revealed && D >= -1e-9) {
    // Show x-intercepts
    const sqD = Math.sqrt(Math.max(0,D));
    const xi1 = (-b-sqD)/(2*a), xi2 = (-b+sqD)/(2*a);
    const pts = Math.abs(xi1-xi2) < 1e-9 ? [xi1] : [xi1,xi2];
    for (const x of pts) {
      const px = QOX + x*QSC;
      qctx.fillStyle = '#fde68a'; qctx.shadowColor = '#fde68a'; qctx.shadowBlur = 8;
      qctx.beginPath(); qctx.arc(px, QOY, 5, 0, Math.PI*2); qctx.fill();
      qctx.shadowBlur = 0;
    }
  }
}

function initScoreBar() {
  const bar = document.getElementById('scoreBar');
  bar.innerHTML = '';
  for (let i = 0; i < QUIZ.length; i++) {
    const d = document.createElement('div');
    d.className = 's-dot';
    d.id = 'sd' + i;
    d.textContent = i + 1;
    bar.appendChild(d);
  }
}

function loadQuestion(i) {
  const { a, b, c } = QUIZ[i];
  document.getElementById('qProg').textContent = `Q${i+1} / ${QUIZ.length}`;
  document.getElementById('quizEq').textContent = buildEq(a, b, c);
  document.getElementById('quizEqEq').textContent = buildEqRHS(a, b, c);
  document.getElementById('quizFb').style.display = 'none';
  document.getElementById('nextBtn').style.display = 'none';
  document.querySelectorAll('.qchoice').forEach(b => { b.className = 'qchoice'; b.disabled = false; });
  qDone = false;
  drawQuizGraph(i, false);
}

function checkAns(choice) {
  if (qDone) return;
  qDone = true;
  const { ans, hint } = QUIZ[qIdx];
  const btns = document.querySelectorAll('.qchoice');
  btns.forEach(b => b.disabled = true);

  const ok = (choice === ans);
  qRecord[qIdx] = ok;

  btns[choice].classList.add(ok ? 'correct' : 'wrong');
  if (!ok) btns[ans].classList.add('show-right');

  const dot = document.getElementById('sd' + qIdx);
  dot.classList.add(ok ? 'ok' : 'fail');
  dot.textContent = ok ? '✓' : '✗';

  const fb = document.getElementById('quizFb');
  fb.style.display = 'block';
  fb.style.borderColor = ok ? 'rgba(52,211,153,0.3)' : 'rgba(248,113,113,0.3)';
  fb.style.background  = ok ? 'rgba(52,211,153,0.07)' : 'rgba(248,113,113,0.06)';
  fb.innerHTML = (ok ? '🎉 정답! ' : '💡 오답! ') + hint;

  // Reveal parabola color
  drawQuizGraph(qIdx, true);

  const nb = document.getElementById('nextBtn');
  nb.style.display = 'inline-block';
  nb.textContent = qIdx < QUIZ.length - 1 ? '다음 →' : '결과 보기 🏆';
}

function nextQ() {
  if (qIdx >= QUIZ.length - 1) { showResult(); return; }
  qIdx++;
  loadQuestion(qIdx);
}

function showResult() {
  const score = qRecord.filter(Boolean).length;
  const card = document.getElementById('finalCard');
  card.style.display = 'block';
  document.getElementById('finalScore').textContent = `${score} / ${QUIZ.length} 점`;
  const msgs = ['아직 어렵나요? 그래프를 다시 탐구해봐요 💪', '조금만 더 연습하면 완벽해져요!', '절반 이상 맞혔어요! 잘하고 있어요 😊', '훌륭해요! 판별식을 잘 이해하고 있어요 👍', '대단해요! 거의 완벽해요 ⭐', '아주 우수해요! 대단해요! 🌟', '완벽해요! 이차함수 마스터 🏆'];
  document.getElementById('finalMsg').textContent = msgs[score];
  card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function resetQuiz() {
  qIdx = 0;
  qRecord.fill(null);
  document.getElementById('finalCard').style.display = 'none';
  initScoreBar();
  loadQuestion(0);
}

// ═══════════════════════════════════════════════════════
//  TAB 3 — ROOT RANGE
// ═══════════════════════════════════════════════════════
const rc = document.getElementById('rangeCanvas');
const rctx = rc.getContext('2d');
const RW = rc.width, RH = rc.height, ROX = RW / 2, ROY = RH / 2;

function updateRange() {
  const b = parseFloat(document.getElementById('rB').value);
  const c = parseFloat(document.getElementById('rC').value);
  const p = parseFloat(document.getElementById('rP').value);
  document.getElementById('rvB').textContent = b;
  document.getElementById('rvC').textContent = c;
  document.getElementById('rvP').textContent = p;
  document.getElementById('eq3').textContent = buildEq(1, b, c);

  rctx.clearRect(0, 0, RW, RH);
  drawBG(rctx, RW, RH);
  drawGrid(rctx, RW, RH, ROX, ROY);
  drawAxes(rctx, RW, RH, ROX, ROY);

  const a = 1, D = b * b - 4 * c;
  const fp = p * p + b * p + c;
  const vx = -b / 2;

  // ── Vertical line at p ──
  const ppx = ROX + p * SC;
  rctx.setLineDash([5, 5]);
  rctx.strokeStyle = 'rgba(240,171,252,0.75)'; rctx.lineWidth = 1.8;
  rctx.beginPath(); rctx.moveTo(ppx, 12); rctx.lineTo(ppx, RH - 12); rctx.stroke();
  rctx.setLineDash([]);

  // p label
  rctx.fillStyle = '#f0abfc';
  rctx.font = 'bold italic 14px Times New Roman';
  rctx.textAlign = 'center';
  rctx.fillText('p', ppx, 26);

  // ── Parabola color ──
  let pCol;
  if (D < -1e-9)       pCol = '#f87171';
  else if (fp < -1e-9) pCol = '#fbbf24'; // between roots
  else                 pCol = '#34d399'; // same side

  drawParabola(rctx, RW, RH, ROX, ROY, a, b, c, pCol, true);
  drawVertex(rctx, ROX, ROY, a, b, c);
  if (D >= -1e-9) drawXIntercepts(rctx, ROX, ROY, a, b, c);

  // ── f(p) point ──
  const fppx = ppx, fppy = ROY - fp * SC;
  if (fppy > -20 && fppy < RH + 20) {
    // Dashed vertical segment from x-axis to f(p)
    rctx.setLineDash([3, 3]);
    rctx.strokeStyle = 'rgba(240,171,252,0.45)'; rctx.lineWidth = 1;
    rctx.beginPath(); rctx.moveTo(fppx, ROY); rctx.lineTo(fppx, fppy); rctx.stroke();
    rctx.setLineDash([]);
    // Dot
    rctx.fillStyle = '#e879f9';
    rctx.shadowColor = '#e879f9'; rctx.shadowBlur = 10;
    rctx.beginPath(); rctx.arc(fppx, fppy, 5, 0, Math.PI * 2); rctx.fill();
    rctx.shadowBlur = 0;
    // f(p) label
    rctx.fillStyle = '#e879f9'; rctx.font = '11px Malgun Gothic';
    const align = ppx < RW * 0.6 ? 'left' : 'right';
    rctx.textAlign = align;
    const off = align === 'left' ? 8 : -8;
    rctx.fillText('f(p) = ' + round2(fp), fppx + off, fppy - 8);
  }

  // ── Analysis ──
  buildRangeAnalysis(D, fp, vx, p);
}

function buildRangeAnalysis(D, fp, vx, p) {
  const Dv = round2(D), fpv = round2(fp), vxv = round2(vx), pv = round2(p);
  const dGe0 = D >= -1e-9;
  const fpNeg = fp < -1e-9, fpPos = fp > 1e-9;
  const vLtP  = vx < p - 1e-9, vGtP = vx > p + 1e-9;

  let title, titleColor, bg;
  if (!dGe0) {
    title = '판별식 D < 0 → 실근이 없습니다 (그래프가 x축과 만나지 않음)';
    titleColor = '#f87171'; bg = 'rgba(248,113,113,0.07)';
  } else if (fpNeg) {
    title = '✅ f(p) < 0 → p가 두 근 사이에 있습니다!';
    titleColor = '#fbbf24'; bg = 'rgba(251,191,36,0.07)';
  } else if (fpPos && vLtP) {
    title = '✅ D ≥ 0, 꼭짓점 x좌표 < p, f(p) > 0 → 두 근 모두 p보다 작습니다!';
    titleColor = '#34d399'; bg = 'rgba(52,211,153,0.07)';
  } else if (fpPos && vGtP) {
    title = '✅ D ≥ 0, p < 꼭짓점 x좌표, f(p) > 0 → 두 근 모두 p보다 큽니다!';
    titleColor = '#60a5fa'; bg = 'rgba(96,165,250,0.07)';
  } else {
    title = '경계 케이스 (p = 근 또는 꼭짓점). 슬라이더를 더 조절해보세요!';
    titleColor = '#94a3b8'; bg = 'rgba(255,255,255,0.04)';
  }

  const ci = (v, ok) => `<span class="cond-badge ${ok ? 'cond-ok' : 'cond-no'}">${v}</span>`;

  document.getElementById('rangeBox').style.background = bg;
  document.getElementById('rangeBox').innerHTML = `
    <div style="font-weight:700; color:${titleColor}; margin-bottom:8px; font-size:0.92rem;">${title}</div>
    <div class="cond-row">
      <span>D = b² − 4c = ${Dv}</span>
      ${ci(dGe0 ? 'D ≥ 0  ✓' : 'D < 0  ✗', dGe0)}
    </div>
    <div class="cond-row">
      <span>꼭짓점 x좌표 −b/2 = ${vxv}  &nbsp; vs &nbsp;  p = ${pv}</span>
      ${ci(vLtP ? '꼭짓점 < p ✓' : vGtP ? 'p < 꼭짓점 ✓' : '꼭짓점 = p', vLtP || vGtP)}
    </div>
    <div class="cond-row">
      <span>f(p) = ${fpv}</span>
      ${ci(fpPos ? 'f(p) > 0  ✓' : fpNeg ? 'f(p) < 0' : 'f(p) = 0', fpPos)}
    </div>
  `;
}

['rB','rC','rP'].forEach(id => document.getElementById(id).addEventListener('input', updateRange));

// ═══════════════════════════════════════════════════════
//  TAB SWITCHING
// ═══════════════════════════════════════════════════════
function switchTab(idx) {
  document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', i === idx));
  document.querySelectorAll('.screen').forEach((s, i) => s.classList.toggle('active', i === idx));
}

// ═══════════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════════
updateMain();
initScoreBar();
loadQuestion(0);
updateRange();
</script>
</body>
</html>"""


def render():
    components.html(_HTML, height=1350, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
