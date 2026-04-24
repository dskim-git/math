# activities/common/mini/quad_ineq_graph_explorer.py
"""
이차부등식과 이차함수 그래프의 관계 탐구
이차함수 y=ax²+bx+c의 그래프에서 y>0, y<0인 x의 범위를
슬라이더로 조작하며 직접 탐구합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "이차부등식그래프탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "a부호와포물선",
        "label":  "a > 0일 때와 a < 0일 때 포물선의 모양이 어떻게 다르고, 이것이 부등식의 해에 어떤 영향을 미치는지 설명하세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "판별식과부등식해",
        "label":  "판별식 D의 값(D>0, D=0, D<0)에 따라 이차부등식 ax²+bx+c>0의 해가 어떻게 달라지는지 구체적으로 설명하세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "부등호변화",
        "label":  "y>0에서 y≥0으로 바뀔 때 또는 y>0에서 y<0으로 바뀔 때 해의 범위가 어떻게 달라지나요?",
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
    "title":       "📊 이차부등식과 그래프 탐구",
    "description": "이차함수 y=ax²+bx+c의 그래프를 조작하며 y>0, y<0인 x의 범위를 직접 발견하고 부등식의 해를 이해합니다.",
    "order":       240,
    "hidden":      False,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>이차부등식과 그래프 탐구</title>
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

/* ── Info panels ── */
.info-panel {
  background: rgba(124,58,237,0.1);
  border: 1px solid rgba(124,58,237,0.25);
  border-radius: 10px;
  padding: 12px 14px;
  margin-top: 8px;
  font-size: 0.92rem;
  line-height: 1.9;
}

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

/* ── Inequality selector ── */
.ineq-selector {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.ineq-btn {
  flex: 1;
  min-width: 70px;
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.06);
  color: #94a3b8;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Times New Roman', serif;
  font-style: italic;
  transition: 0.2s;
}
.ineq-btn:hover { background: rgba(255,255,255,0.12); }
.ineq-btn.active {
  background: linear-gradient(135deg, #7c3aed, #1d4ed8);
  color: #fff;
  border-color: #7c3aed;
}

/* ── Solution display ── */
.solution-box {
  background: rgba(255,255,255,0.04);
  border: 2px solid rgba(124,58,237,0.3);
  border-radius: 10px;
  padding: 14px 16px;
  margin-top: 10px;
  font-size: 0.95rem;
}
.solution-title {
  font-weight: 800;
  color: #a78bfa;
  margin-bottom: 6px;
  font-size: 0.82rem;
}
.solution-content {
  font-family: 'Times New Roman', Georgia, serif;
  font-style: italic;
  font-size: 1.15rem;
  color: #fde68a;
  text-align: center;
  padding: 8px;
}

/* ── Condition checks ── */
.cond-box {
  background: rgba(255,255,255,0.04);
  border-radius: 8px;
  padding: 10px 12px;
  margin-top: 8px;
  font-size: 0.85rem;
  line-height: 1.8;
}
.cond-row {
  display: flex;
  align-items: center;
  gap: 8px;
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

/* ── Summary grid ── */
.sum-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 10px;
}
.sum-box {
  flex: 1;
  min-width: 90px;
  border-radius: 10px;
  padding: 10px 8px;
  text-align: center;
  font-size: 0.8rem;
  line-height: 1.6;
}
.sum-box.up { background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3); }
.sum-box.down { background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3); }
.sum-head { font-weight: 800; margin-bottom: 2px; color: #fde68a; }

/* ── Activity intro ── */
.intro-section {
  background: rgba(124,58,237,0.08);
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: 10px;
  padding: 12px 14px;
  margin-bottom: 12px;
  font-size: 0.88rem;
  line-height: 1.8;
}

.math { font-family: 'Times New Roman', Georgia, serif; font-style: italic; color: #fde68a; }

/* ── Quiz (TAB 2) ── */
.quiz-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.score-bar { display: flex; gap: 5px; flex-wrap: wrap; }
.s-dot {
  width: 28px; height: 28px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700;
  background: rgba(255,255,255,0.08);
  color: #64748b;
  border: 1px solid rgba(255,255,255,0.1);
  transition: 0.3s;
}
.s-dot.ok   { background: rgba(52,211,153,0.25); color: #34d399; border-color: rgba(52,211,153,0.5); }
.s-dot.fail { background: rgba(248,113,113,0.2);  color: #f87171; border-color: rgba(248,113,113,0.4); }

.quiz-choices {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 12px;
}
.qchoice {
  padding: 14px 10px;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  font-size: 0.88rem;
  font-weight: 600;
  color: #e2e8ff;
  transition: 0.18s;
  user-select: none;
  font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Times New Roman', serif;
  line-height: 1.5;
}
.qchoice:hover:not(:disabled)  { background: rgba(124,58,237,0.2); border-color: #7c3aed; }
.qchoice.correct    { background: rgba(52,211,153,0.2);  border-color: #34d399; color: #6ee7b7; }
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
  line-height: 1.7;
}

/* ── Final score ── */
.final-card {
  display: none;
  text-align: center;
  padding: 20px;
}
.final-score { font-size: 2.2rem; font-weight: 800; color: #fde68a; margin: 8px 0; }

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
</style>
</head>
<body>

<!-- ──────────── TABS ──────────── -->
<div class="tabs">
  <button class="tab active" onclick="switchTab(0)" id="tab0">🔍 탐구 1<br>그래프 조작</button>
  <button class="tab" onclick="switchTab(1)" id="tab1">🎯 탐구 2<br>부등식 풀기</button>
</div>

<!-- ══════════ SCREEN 1: 그래프 탐구 ══════════ -->
<div class="screen active" id="screen0">

  <div class="intro-section">
    <b>💡 활동 소개</b><br>
    아래 슬라이더로 이차함수 그래프를 조작해 보세요. 노란색(양수) 영역과 주황색(음수) 영역을 보며
    <span class="math">y > 0</span>, <span class="math">y < 0</span>인 <span class="math">x</span>의 범위를 발견합니다.
  </div>

  <div class="card">
    <div class="card-title">📐 이차함수 그래프 조작</div>
    <div class="eq-display" id="eq1">y = x² − 4</div>
    <div class="canvas-wrap">
      <canvas id="mainCanvas" width="460" height="380"></canvas>
    </div>
    <div class="slider-row">
      <span class="slider-lbl">a</span>
      <input type="range" id="sA" min="-2" max="2" step="0.25" value="1">
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
    <div class="card-title">🔤 부등식 선택하기</div>
    <div class="ineq-selector">
      <button class="ineq-btn active" onclick="selectIneq(0)">y <span class="math">&gt;</span> 0</button>
      <button class="ineq-btn" onclick="selectIneq(1)">y <span class="math">≥</span> 0</button>
      <button class="ineq-btn" onclick="selectIneq(2)">y <span class="math">&lt;</span> 0</button>
      <button class="ineq-btn" onclick="selectIneq(3)">y <span class="math">≤</span> 0</button>
    </div>
    <div class="solution-box">
      <div class="solution-title">해의 범위</div>
      <div class="solution-content" id="solutionText">계산 중...</div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">📌 a의 부호에 따른 해의 범위</div>
    <div class="sum-grid">
      <div class="sum-box up">
        <div class="sum-head">a &gt; 0 (위로 볼록)</div>
        <div><span class="math">y&gt;0</span>: 양 옆<br><span class="math">y&lt;0</span>: 사이</div>
      </div>
      <div class="sum-box down">
        <div class="sum-head">a &lt; 0 (아래로 볼록)</div>
        <div><span class="math">y&gt;0</span>: 사이<br><span class="math">y&lt;0</span>: 양 옆</div>
      </div>
    </div>
    <div class="cond-box">
      <div class="cond-row">
        <span>판별식 <span class="math">D</span> = <span class="math">b² − 4ac</span></span>
        <span class="cond-badge" id="discBadge">계산 중...</span>
      </div>
      <div class="cond-row">
        <span id="discInfo" style="font-size:0.88rem; color:#cbd5e1;">판별식 정보...</span>
      </div>
    </div>
  </div>

</div>

<!-- ══════════ SCREEN 2: 부등식 풀이 ══════════ -->
<div class="screen" id="screen1">

  <div class="intro-section">
    <b>💡 여러 부등식 풀어보기</b><br>
    아래 부등식들을 직접 풀어보세요. 그래프에서 해당 영역을 찾아 조건을 확인합니다.
  </div>

  <div class="card">
    <div class="card-title">🎯 부등식 풀이 선택</div>
    <div class="quiz-nav">
      <div class="score-bar" id="scoreBar2"></div>
      <span style="font-size:0.88rem; color:#64748b;" id="qProg2">Q1 / 5</span>
    </div>
    <div class="eq-display" id="quizEq2">문제 로딩 중...</div>
    <div style="font-size:0.9rem; color:#cbd5e1; text-align:center; margin-bottom:12px;">
      다음 부등식을 풀어 정답을 선택하세요.
    </div>
    <div class="quiz-choices" id="quizChoices2"></div>
    <div class="quiz-fb" id="quizFb2"></div>
    <div style="display:flex; justify-content:flex-end; margin-top:10px;">
      <button class="btn" onclick="nextQ2()" id="nextBtn2" style="display:none;">다음 →</button>
    </div>
  </div>

  <div class="card final-card" id="finalCard2">
    <div class="card-title">🏆 퀴즈 완료!</div>
    <div class="final-score" id="finalScore2">0 / 5</div>
    <div style="color:#94a3b8; font-size:0.9rem;" id="finalMsg2">-</div>
    <button class="btn" onclick="resetQuiz2()" style="margin-top:14px;">다시 도전 🔄</button>
  </div>

</div>

<script>
// ═══════════════════════════════════════════════════════
//  UTILITIES
// ═══════════════════════════════════════════════════════
function round2(n) { return Math.round(n * 100) / 100; }

function buildEq(a, b, c) {
  const ra = round2(a), rb = round2(b), rc = round2(c);
  if (Math.abs(ra) < 0.001) {
    if (Math.abs(rb) < 0.001) return 'y = ' + rc;
    const sx = rb === 1 ? 'x' : rb === -1 ? '−x' : rb < 0 ? '−' + round2(-rb) + 'x' : rb + 'x';
    if (rc === 0) return 'y = ' + sx;
    return 'y = ' + sx + (rc > 0 ? ' + ' + rc : ' − ' + round2(-rc));
  }
  let s = 'y = ';
  if (ra === 1) s += 'x²';
  else if (ra === -1) s += '−x²';
  else if (ra < 0) s += '−' + round2(-ra) + 'x²';
  else s += ra + 'x²';
  if (Math.abs(rb) > 0.001) {
    if (rb === 1) s += ' + x';
    else if (rb === -1) s += ' − x';
    else if (rb > 0) s += ' + ' + rb + 'x';
    else s += ' − ' + round2(-rb) + 'x';
  }
  if (Math.abs(rc) > 0.001) {
    s += rc > 0 ? ' + ' + rc : ' − ' + round2(-rc);
  }
  return s;
}

// ═══════════════════════════════════════════════════════
//  CANVAS HELPERS
// ═══════════════════════════════════════════════════════
const SC = 38;

function drawBG(ctx, W, H) {
  const g = ctx.createLinearGradient(0, 0, W, H);
  g.addColorStop(0, '#080d1e'); g.addColorStop(1, '#0c1628');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
}

function drawGrid(ctx, W, H, ox, oy) {
  ctx.strokeStyle = 'rgba(255,255,255,0.065)'; ctx.lineWidth = 0.8;
  const minX = Math.floor(-ox / SC), maxX = Math.ceil((W - ox) / SC);
  const minY = Math.floor(-(H - oy) / SC), maxY = Math.ceil(oy / SC);
  for (let x = minX; x <= maxX; x++) {
    ctx.beginPath(); ctx.moveTo(ox + x*SC, 0); ctx.lineTo(ox + x*SC, H); ctx.stroke();
  }
  for (let y = minY; y <= maxY; y++) {
    ctx.beginPath(); ctx.moveTo(0, oy - y*SC); ctx.lineTo(W, oy - y*SC); ctx.stroke();
  }
}

function drawAxes(ctx, W, H, ox, oy) {
  ctx.strokeStyle = 'rgba(255,255,255,0.32)'; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(6, oy); ctx.lineTo(W - 6, oy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ox, 6); ctx.lineTo(ox, H - 6); ctx.stroke();
  ctx.fillStyle = 'rgba(255,255,255,0.32)';
  ctx.beginPath(); ctx.moveTo(W - 6, oy); ctx.lineTo(W - 14, oy - 4); ctx.lineTo(W - 14, oy + 4); ctx.fill();
  ctx.beginPath(); ctx.moveTo(ox, 6); ctx.lineTo(ox - 4, 14); ctx.lineTo(ox + 4, 14); ctx.fill();
  ctx.fillStyle = 'rgba(255,255,255,0.5)'; ctx.font = 'italic 13px Times New Roman';
  ctx.textAlign = 'left'; ctx.fillText('x', W - 8, oy - 7);
  ctx.textAlign = 'center'; ctx.fillText('y', ox + 12, 14);

  const minX = Math.floor(-ox / SC), maxX = Math.ceil((W - ox) / SC);
  const minY = Math.floor(-(H - oy) / SC), maxY = Math.ceil(oy / SC);
  ctx.fillStyle = 'rgba(255,255,255,0.32)'; ctx.font = '10px Malgun Gothic';
  ctx.textAlign = 'center';
  for (let x = minX + 1; x < maxX; x++) {
    if (x === 0) continue;
    const px = ox + x * SC;
    ctx.fillText(x, px, oy + 13);
  }
  ctx.textAlign = 'right';
  for (let y = minY + 1; y < maxY; y++) {
    if (y === 0) continue;
    const py = oy - y * SC;
    ctx.fillText(y, ox - 5, py + 4);
  }
}

function drawParabola(ctx, W, H, ox, oy, a, b, c, selectColor, selectedIneq) {
  if (Math.abs(a) < 0.001) return;

  // Shade regions
  const xMin = (-ox / SC) - 0.2, xMax = ((W - ox) / SC) + 0.2;
  const steps = 280;

  for (let i = 0; i < steps; i++) {
    const x1 = xMin + (xMax - xMin) * i / steps;
    const x2 = xMin + (xMax - xMin) * (i + 1) / steps;
    const y1 = a * x1 * x1 + b * x1 + c;
    const y2 = a * x2 * x2 + b * x2 + c;
    const px1 = ox + x1 * SC, py1 = oy - y1 * SC;
    const px2 = ox + x2 * SC, py2 = oy - y2 * SC;

    // Determine shade color
    let shadeColor = null;
    if (selectedIneq === 0 && y1 > 1e-9) shadeColor = 'rgba(253,230,138,0.15)'; // y > 0
    else if (selectedIneq === 1 && y1 > -1e-9) shadeColor = 'rgba(253,230,138,0.15)'; // y ≥ 0
    else if (selectedIneq === 2 && y1 < -1e-9) shadeColor = 'rgba(248,113,113,0.15)'; // y < 0
    else if (selectedIneq === 3 && y1 < 1e-9) shadeColor = 'rgba(248,113,113,0.15)'; // y ≤ 0

    if (shadeColor) {
      ctx.fillStyle = shadeColor;
      if (a > 0) {
        ctx.beginPath(); ctx.moveTo(px1, oy); ctx.lineTo(px1, py1); ctx.lineTo(px2, py2); ctx.lineTo(px2, oy); ctx.fill();
      } else {
        ctx.beginPath(); ctx.moveTo(px1, oy); ctx.lineTo(px1, py1); ctx.lineTo(px2, py2); ctx.lineTo(px2, oy); ctx.fill();
      }
    }
  }

  // Draw curve
  ctx.strokeStyle = selectColor;
  ctx.lineWidth = 2.8;
  ctx.shadowColor = selectColor;
  ctx.shadowBlur = 8;
  ctx.beginPath();
  let pen = false;
  for (let i = 0; i <= steps; i++) {
    const x = xMin + (xMax - xMin) * i / steps;
    const y = a * x * x + b * x + c;
    const px = ox + x * SC, py = oy - y * SC;
    if (py < -30 || py > H + 30) { if (pen) { ctx.stroke(); ctx.beginPath(); pen = false; } continue; }
    if (!pen) { ctx.moveTo(px, py); pen = true; } else { ctx.lineTo(px, py); }
  }
  if (pen) ctx.stroke();
  ctx.shadowBlur = 0;
}

function drawXIntercepts(ctx, ox, oy, a, b, c) {
  const D = b * b - 4 * a * c;
  if (D < -1e-9) return;
  const sqD = Math.sqrt(Math.max(0, D));
  const x1 = (-b - sqD) / (2 * a), x2 = (-b + sqD) / (2 * a);
  const pts = Math.abs(x1 - x2) < 1e-9 ? [x1] : [Math.min(x1, x2), Math.max(x1, x2)];
  for (const x of pts) {
    const px = ox + x * SC;
    ctx.strokeStyle = 'rgba(253,230,138,0.35)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(px, oy, 9, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = '#fde68a';
    ctx.shadowColor = '#fde68a'; ctx.shadowBlur = 10;
    ctx.beginPath(); ctx.arc(px, oy, 5, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
  }
}

// ═══════════════════════════════════════════════════════
//  MAIN GRAPH SCREEN
// ═══════════════════════════════════════════════════════
const mc = document.getElementById('mainCanvas');
const mctx = mc.getContext('2d');
const MW = mc.width, MH = mc.height, MOX = MW / 2, MOY = MH / 2;

let currentIneq = 0;
const ineqSymbols = ['>', '≥', '<', '≤'];
const ineqChecks = [(y) => y > 1e-9, (y) => y > -1e-9, (y) => y < -1e-9, (y) => y < 1e-9];

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
    document.getElementById('info1').innerHTML = '<span style="color:#f87171;">⚠️ a = 0이면 이차함수가 아닙니다.</span>';
    document.getElementById('solutionText').textContent = '(a ≠ 0으로 설정해 주세요)';
    return;
  }

  const D = b * b - 4 * a * c;
  const selectColor = currentIneq <= 1 ? '#34d399' : '#f87171';
  drawParabola(mctx, MW, MH, MOX, MOY, a, b, c, selectColor, currentIneq);
  drawXIntercepts(mctx, MOX, MOY, a, b, c);

  // Solution
  buildSolution(a, b, c);
  buildInfo(a, b, c);
}

function buildSolution(a, b, c) {
  const D = b * b - 4 * a * c;
  const ineq = ineqSymbols[currentIneq];
  let solutionText;

  if (Math.abs(D) < 1e-9) {
    // D = 0: one root
    const x0 = round2(-b / (2 * a));
    if (currentIneq === 0) solutionText = 'x ≠ ' + x0 + '인 모든 실수'; // a는 항상 양수 (조작에서 a가 0 근처)
    else if (currentIneq === 1) solutionText = '모든 실수';
    else if (currentIneq === 2) solutionText = '해가 없습니다';
    else solutionText = 'x = ' + x0 + '만 해당';
  } else if (D > 1e-9) {
    // D > 0: two roots
    const sqD = Math.sqrt(D);
    const x1 = round2((-b - sqD) / (2 * a));
    const x2 = round2((-b + sqD) / (2 * a));
    const [lo, hi] = x1 < x2 ? [x1, x2] : [x2, x1];

    if (a > 0) {
      if (currentIneq === 0) solutionText = 'x < ' + lo + ' 또는 x > ' + hi;
      else if (currentIneq === 1) solutionText = 'x ≤ ' + lo + ' 또는 x ≥ ' + hi;
      else if (currentIneq === 2) solutionText = lo + ' < x < ' + hi;
      else solutionText = lo + ' ≤ x ≤ ' + hi;
    } else {
      if (currentIneq === 0) solutionText = lo + ' < x < ' + hi;
      else if (currentIneq === 1) solutionText = lo + ' ≤ x ≤ ' + hi;
      else if (currentIneq === 2) solutionText = 'x < ' + lo + ' 또는 x > ' + hi;
      else solutionText = 'x ≤ ' + lo + ' 또는 x ≥ ' + hi;
    }
  } else {
    // D < 0: no real roots
    if (a > 0) {
      if (currentIneq <= 1) solutionText = '모든 실수';
      else solutionText = '해가 없습니다';
    } else {
      if (currentIneq <= 1) solutionText = '해가 없습니다';
      else solutionText = '모든 실수';
    }
  }

  document.getElementById('solutionText').textContent = solutionText;
}

function buildInfo(a, b, c) {
  const D = b * b - 4 * a * c;
  const Dv = round2(D);
  let dBadge, dText;
  if (D > 1e-9) { dBadge = '> 0'; dText = '서로 다른 두 실근'; }
  else if (D > -1e-9) { dBadge = '= 0'; dText = '중근'; }
  else { dBadge = '< 0'; dText = '실근 없음'; }

  document.getElementById('discBadge').textContent = 'D ' + dBadge;
  document.getElementById('discInfo').innerHTML =
    '판별식 <span class="math">D = ' + Dv + '</span> → ' + dText +
    (a > 0 ? ' (a > 0)' : ' (a < 0)');
}

function selectIneq(idx) {
  currentIneq = idx;
  document.querySelectorAll('.ineq-btn').forEach((btn, i) => btn.classList.toggle('active', i === idx));
  updateMain();
}

['sA','sB','sC'].forEach(id => document.getElementById(id).addEventListener('input', updateMain));

// ═══════════════════════════════════════════════════════
//  TAB 2 — INEQUALITY QUIZ
// ═══════════════════════════════════════════════════════
const INEQ_QUIZ = [
  {
    expr: 'x² − 4x + 3',
    ineq: '>',
    roots: [1, 3],
    a: 1,
    ans: 0,
    choices: [
      'x < 1 또는 x > 3',
      '1 < x < 3',
      '1 ≤ x ≤ 3',
      '모든 실수'
    ],
    hint: '(x − 1)(x − 3) > 0: a > 0이므로 양 옆'
  },
  {
    expr: 'x² − 2x − 8',
    ineq: '≤',
    roots: [-2, 4],
    a: 1,
    ans: 1,
    choices: [
      'x < −2 또는 x > 4',
      '−2 ≤ x ≤ 4',
      'x ≤ −2 또는 x ≥ 4',
      '모든 실수'
    ],
    hint: '(x + 2)(x − 4) ≤ 0: a > 0이므로 사이'
  },
  {
    expr: '−x² + 6x − 5',
    ineq: '<',
    roots: [1, 5],
    a: -1,
    ans: 2,
    choices: [
      '1 < x < 5',
      '−1 < x < 5',
      'x < 1 또는 x > 5',
      '1 ≤ x ≤ 5'
    ],
    hint: '−(x − 1)(x − 5) < 0: a < 0이므로 양 옆'
  },
  {
    expr: '−x² + 4',
    ineq: '≥',
    roots: [-2, 2],
    a: -1,
    ans: 1,
    choices: [
      'x < −2 또는 x > 2',
      '−2 ≤ x ≤ 2',
      'x는 모든 실수',
      '−2 < x < 2'
    ],
    hint: '−(x² − 4) ≥ 0: a < 0이므로 사이'
  },
  {
    expr: 'x² + 2x + 2',
    ineq: '>',
    roots: null,
    a: 1,
    ans: 3,
    choices: [
      '해가 없습니다',
      '−1',
      'x = −1만',
      '모든 실수'
    ],
    hint: 'D < 0: 실근 없음, a > 0이므로 모든 실수'
  }
];

let qIdx2 = 0, qDone2 = false;
const qRecord2 = Array(INEQ_QUIZ.length).fill(null);

function initScoreBar2() {
  const bar = document.getElementById('scoreBar2');
  bar.innerHTML = '';
  for (let i = 0; i < INEQ_QUIZ.length; i++) {
    const d = document.createElement('div');
    d.className = 's-dot';
    d.id = 'sd2_' + i;
    d.textContent = i + 1;
    bar.appendChild(d);
  }
}

function loadQuestion2(i) {
  const { expr, ineq } = INEQ_QUIZ[i];
  document.getElementById('qProg2').textContent = `Q${i+1} / ${INEQ_QUIZ.length}`;
  document.getElementById('quizEq2').innerHTML = '<span class="math">' + expr + ' ' + ineq + ' 0</span>';
  document.getElementById('quizFb2').style.display = 'none';
  document.getElementById('nextBtn2').style.display = 'none';

  const choicesDiv = document.getElementById('quizChoices2');
  choicesDiv.innerHTML = '';
  INEQ_QUIZ[i].choices.forEach((choice, idx) => {
    const btn = document.createElement('button');
    btn.className = 'qchoice';
    btn.textContent = String.fromCharCode(9312 + idx) + ' ' + choice;  // ①②③④
    btn.onclick = () => checkAns2(idx);
    choicesDiv.appendChild(btn);
  });

  qDone2 = false;
}

function checkAns2(choice) {
  if (qDone2) return;
  qDone2 = true;
  const { ans, hint } = INEQ_QUIZ[qIdx2];
  const btns = document.querySelectorAll('#quizChoices2 .qchoice');
  btns.forEach(b => b.disabled = true);

  const ok = (choice === ans);
  qRecord2[qIdx2] = ok;

  btns[choice].classList.add(ok ? 'correct' : 'wrong');
  if (!ok) btns[ans].classList.add('show-right');

  const dot = document.getElementById('sd2_' + qIdx2);
  dot.classList.add(ok ? 'ok' : 'fail');
  dot.textContent = ok ? '✓' : '✗';

  const fb = document.getElementById('quizFb2');
  fb.style.display = 'block';
  fb.style.borderColor = ok ? 'rgba(52,211,153,0.3)' : 'rgba(248,113,113,0.3)';
  fb.style.background  = ok ? 'rgba(52,211,153,0.07)' : 'rgba(248,113,113,0.06)';
  fb.innerHTML = (ok ? '🎉 정답! ' : '💡 틀렸어요. ') + hint;

  const nb = document.getElementById('nextBtn2');
  nb.style.display = 'inline-block';
  nb.textContent = qIdx2 < INEQ_QUIZ.length - 1 ? '다음 →' : '결과 보기 🏆';
}

function nextQ2() {
  if (qIdx2 >= INEQ_QUIZ.length - 1) { showResult2(); return; }
  qIdx2++;
  loadQuestion2(qIdx2);
}

function showResult2() {
  const score = qRecord2.filter(Boolean).length;
  const card = document.getElementById('finalCard2');
  card.style.display = 'block';
  document.getElementById('finalScore2').textContent = `${score} / ${INEQ_QUIZ.length} 점`;
  const msgs = ['더 열심히 풀어보세요 💪', '좋은 시작입니다!', '절반 이상 맞혔어요! 잘하고 있어요 😊', '훌륭해요! 거의 다 왔어요 👍', '완벽해요! 부등식 마스터 🏆'];
  document.getElementById('finalMsg2').textContent = msgs[Math.min(score, 4)];
  card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function resetQuiz2() {
  qIdx2 = 0;
  qRecord2.fill(null);
  document.getElementById('finalCard2').style.display = 'none';
  initScoreBar2();
  loadQuestion2(0);
}

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
initScoreBar2();
loadQuestion2(0);
</script>
</body>
</html>"""


def render():
    components.html(_HTML, height=1400, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
