# activities/common/mini/remainder_same_expressions.py
"""
나머지가 같은 식 탐험 – 수행과제 활동
6장의 다항식 카드에서 A를 뽑고, x²+1로 나누어 나머지를 탐구하는 인터랙티브 활동
(공통수학1 · 다항식의 나눗셈 단원)
"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 (공통수학1 전용) ─────────────────────────────────────
_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "나머지같은식"

_QUESTIONS = [
    {"type": 'markdown', "text": '**📝 스스로 문제 2개를 만들고 풀어보세요**'},
    {"key": '문제1', "label": '문제 1 (나눠지는 다항식과 나누는 일차식 또는 x²+1을 적어주세요)', "type": 'text_area', "height": 70},
    {"key": '답1', "label": '문제 1의 답 (몫과 나머지)', "type": 'text_input'},
    {"key": '문제2', "label": '문제 2 (나눠지는 다항식과 나누는 일차식 또는 x²+1을 적어주세요)', "type": 'text_area', "height": 70},
    {"key": '답2', "label": '문제 2의 답 (몫과 나머지)', "type": 'text_input'},
    {"key": '새롭게알게된점', "label": '💡 이 활동을 통해 새롭게 알게 된 점', "type": 'text_area', "height": 100},
    {"key": '느낀점', "label": '💬 이 활동을 하면서 느낀 점', "type": 'text_area', "height": 90},
]

META = {
    "title":       "🃏 나머지가 같은 식 탐험",
    "description": "6장의 다항식 카드 중 하나를 골라 x²+1로 나눈 나머지를 탐구하고, 나머지가 같은 식의 성질을 발견하는 수행과제 활동",
    "order":       37,
    "hidden":      True,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>나머지가 같은 식</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})"></script>
<style>
/* ── Base ── */
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
  color:#e2e8f0;padding:18px 14px;min-height:100vh;
  font-size:16px
}

/* ── Phase indicator ── */
.phase-bar{display:flex;justify-content:center;gap:8px;margin-bottom:22px;flex-wrap:wrap}
.phase-dot{
  display:flex;align-items:center;justify-content:center;
  width:40px;height:40px;border-radius:50%;
  border:2px solid #334155;background:#1a1a2e;
  color:#64748b;font-size:14px;font-weight:800;
  transition:all .3s;cursor:default
}
.phase-dot.done{background:#0369a1;border-color:#38bdf8;color:#fff}
.phase-dot.active{
  background:linear-gradient(135deg,#6d28d9,#1d4ed8);
  border-color:#a78bfa;color:#fff;
  box-shadow:0 0 0 5px rgba(167,139,250,.2);
  transform:scale(1.1)
}
.phase-connector{width:28px;height:2px;background:#334155;align-self:center;border-radius:2px}
.phase-connector.done{background:#0369a1}

/* ── Cards ── */
.card{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  border-radius:16px;padding:22px 24px;margin-bottom:18px;
  backdrop-filter:blur(4px)
}
.card-title{font-size:17px;font-weight:800;margin-bottom:14px;
  display:flex;align-items:center;gap:9px}

/* ── Phase panels ── */
.phase-panel{display:none}.phase-panel.active{display:block;animation:slideIn .4s ease}
@keyframes slideIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}

/* ── Polynomial Cards (the 6 cards to pick) ── */
.cards-grid{
  display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0
}
.poly-card{
  background:#1a1a2e;border:2px solid #334155;border-radius:14px;
  padding:0;cursor:pointer;transition:all .3s;
  perspective:600px;aspect-ratio:3/2;
  position:relative
}
.poly-card .card-inner{
  position:absolute;inset:0;
  transform-style:preserve-3d;
  transition:transform .6s cubic-bezier(.4,0,.2,1)
}
.poly-card.flipped .card-inner{transform:rotateY(180deg)}
.poly-card .card-front,.poly-card .card-back{
  position:absolute;inset:0;
  border-radius:12px;
  display:flex;align-items:center;justify-content:center;
  backface-visibility:hidden;-webkit-backface-visibility:hidden
}
.poly-card .card-front{
  background:linear-gradient(135deg,#1e3a5f,#0f2340);
  border:2px solid #1e40af;
  flex-direction:column;gap:6px
}
.poly-card .card-back{
  background:linear-gradient(135deg,#312e81,#1e1b4b);
  border:2px solid #6d28d9;
  transform:rotateY(180deg);
  flex-direction:column;gap:4px;padding:10px
}
.card-number{
  font-size:34px;font-weight:900;
  background:linear-gradient(135deg,#60a5fa,#818cf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent
}
.card-deco{font-size:13px;color:#475569;letter-spacing:.1em}
.card-formula{font-size:16px;color:#c4b5fd;text-align:center;line-height:1.6}

.poly-card.selected .card-back{
  border-color:#fbbf24;
  box-shadow:0 0 24px rgba(251,191,36,.4)
}
.poly-card.disabled{cursor:not-allowed;opacity:.45}
.poly-card:not(.disabled):not(.flipped):hover{
  transform:translateY(-4px);
  box-shadow:0 10px 30px rgba(96,165,250,.2)
}

/* ── Division visualization ── */
.div-scene{
  background:#0d1b2e;border:1px solid #1e3a5f;border-radius:14px;
  padding:20px;overflow-x:auto
}
.division-table{
  font-family:'JetBrains Mono','Courier New',monospace;
  border-collapse:collapse;margin:0 auto;font-size:14px;
  min-width:340px
}
.division-table td{
  padding:7px 14px;text-align:center;
  border:none;white-space:nowrap
}
.division-table .divisor-cell{
  border-right:3px solid #60a5fa;
  color:#60a5fa;font-weight:800;font-size:15px
}
.division-table .dividend-row td{color:#fbbf24;font-weight:700}
.division-table .subtracted-row td{color:#94a3b8}
.division-table .remainder-row td{color:#f87171;font-weight:700}
.division-table .quotient-row td{color:#4ade80;font-weight:700}
.division-table .line-row td{border-top:2px solid #334155}

.step-highlight{
  animation:stepPulse .8s ease;
  border-radius:6px
}
@keyframes stepPulse{
  0%{background:rgba(251,191,36,.3)}
  100%{background:transparent}
}

/* ── Step navigation ── */
.step-nav{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap;align-items:center}
.nav-btn{
  padding:10px 24px;border-radius:10px;border:none;
  font-size:15px;font-weight:700;cursor:pointer;transition:all .2s
}
.btn-primary{background:#1d4ed8;color:#fff}.btn-primary:hover{background:#2563eb}
.btn-secondary{background:#1e293b;color:#94a3b8}.btn-secondary:hover{background:#263547}
.btn-success{background:#166534;color:#4ade80}.btn-success:hover{background:#15803d}
.btn-warning{background:#92400e;color:#fcd34d}.btn-warning:hover{background:#b45309}
.nav-btn:disabled{background:#1a1a2e;color:#374151;cursor:not-allowed}

/* ── Remainder badge ── */
.remainder-badge{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(248,113,113,.1);border:1.5px solid #ef4444;
  border-radius:20px;padding:8px 18px;font-size:15px;font-weight:700;
  color:#f87171;margin:8px 4px
}
.remainder-badge.zero{
  background:rgba(74,222,128,.1);border-color:#22c55e;color:#4ade80
}

/* ── B builder ── */
.b-builder{
  background:#0d1b2e;border:1px solid #1e3a5f;border-radius:14px;padding:18px
}
.b-builder-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:12px 0}
.coef-group{display:flex;flex-direction:column;align-items:center;gap:5px}
.coef-label{font-size:12px;color:#64748b;font-weight:600}
.coef-input{
  width:62px;padding:9px 6px;border:2px solid #334155;border-radius:8px;
  background:#141c2b;color:#e2e8f0;font-size:16px;font-weight:700;
  text-align:center;font-family:inherit;outline:none;transition:.2s
}
.coef-input:focus{border-color:#6d28d9;box-shadow:0 0 0 3px rgba(109,40,217,.2)}
.op-label{font-size:20px;color:#64748b;font-weight:800;padding:0 4px;margin-top:18px}
.poly-display{
  font-size:16px;color:#c4b5fd;min-height:36px;display:flex;align-items:center;
  font-family:'JetBrains Mono',monospace
}
.poly-remainder-chip{
  padding:4px 12px;border-radius:8px;font-size:12px;font-weight:700;
  border:1.5px solid;display:inline-block;margin:4px 0
}

/* ── Results table ── */
.results-table{width:100%;border-collapse:collapse;font-size:14px;margin:10px 0}
.results-table th{
  background:#0f2340;color:#7dd3fc;font-weight:700;
  padding:12px 14px;text-align:center;border:1px solid #1e3a5f
}
.results-table td{
  padding:11px 14px;text-align:center;border:1px solid #1e3a5f;
  color:#c0cce0;background:#0b1629
}
.results-table td.b-poly{color:#a5b4fc;font-family:'JetBrains Mono',monospace;font-size:13px}
.results-table td.r1-cell{color:#fbbf24;font-weight:700}
.results-table td.ab-cell{color:#94a3b8;font-family:'JetBrains Mono',monospace;font-size:13px}
.results-table td.r2-cell.zero{color:#4ade80;font-weight:700}
.results-table td.r2-cell.nonzero{color:#f87171}
.results-table tr.empty td{color:#334155;font-style:italic}

/* ── Discovery animation ── */
.discovery-box{
  background:linear-gradient(135deg,rgba(109,40,217,.15),rgba(29,78,216,.15));
  border:2px solid #6d28d9;border-radius:16px;padding:28px;
  text-align:center;margin:16px 0;
  animation:discoveryPop .6s cubic-bezier(.34,1.56,.64,1)
}
@keyframes discoveryPop{
  from{opacity:0;transform:scale(.85)}
  to{opacity:1;transform:scale(1)}
}
.discovery-title{
  font-size:22px;font-weight:900;margin-bottom:12px;
  background:linear-gradient(135deg,#a78bfa,#60a5fa);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent
}

/* ── Hint boxes ── */
.hint-box{
  background:rgba(251,191,36,.06);border-left:4px solid #fbbf24;
  border-radius:0 10px 10px 0;padding:13px 18px;margin:12px 0;
  font-size:15px;color:#fcd34d;line-height:1.9
}
.info-box{
  background:rgba(96,165,250,.06);border-left:4px solid #3b82f6;
  border-radius:0 10px 10px 0;padding:13px 18px;margin:12px 0;
  font-size:15px;color:#93c5fd;line-height:1.9
}
.success-box{
  background:rgba(74,222,128,.06);border-left:4px solid #22c55e;
  border-radius:0 10px 10px 0;padding:13px 18px;margin:12px 0;
  font-size:15px;color:#4ade80;line-height:1.9
}

/* ── Progress ── */
.progress-wrap{display:flex;align-items:center;gap:8px;margin-bottom:18px}
.progress-track{flex:1;height:8px;background:#1e293b;border-radius:99px;overflow:hidden}
.progress-fill{
  height:100%;
  background:linear-gradient(90deg,#6d28d9,#1d4ed8,#0ea5e9);
  border-radius:99px;transition:width .5s ease
}
.score-badge{
  background:#1d3557;color:#93c5fd;border-radius:99px;
  padding:5px 14px;font-size:14px;font-weight:700;white-space:nowrap
}

/* ── Katex override ── */
.katex{font-size:1.55em}
.math-block{
  background:rgba(109,40,217,.08);border:1px solid rgba(109,40,217,.2);
  border-radius:10px;padding:16px 20px;margin:10px 0;overflow-x:auto;
  text-align:center
}

/* ── Misc ── */
.section-title{font-size:16px;font-weight:700;color:#7dd3fc;margin:16px 0 8px}
.badge{
  display:inline-block;padding:3px 12px;border-radius:99px;
  font-size:13px;font-weight:700
}
.badge-yellow{background:rgba(251,191,36,.15);color:#fbbf24;border:1.5px solid #fbbf24}
.badge-blue{background:rgba(96,165,250,.15);color:#60a5fa;border:1.5px solid #60a5fa}
.badge-purple{background:rgba(167,139,250,.15);color:#a78bfa;border:1.5px solid #a78bfa}
.badge-green{background:rgba(74,222,128,.15);color:#4ade80;border:1.5px solid #22c55e}

.fade-in{animation:fi .5s ease}
@keyframes fi{from{opacity:0}to{opacity:1}}

@media(max-width:480px){
  .cards-grid{grid-template-columns:repeat(2,1fr)}
  .b-builder-row{gap:6px}
}
</style>
</head>
<body>

<!-- ─── HEADER ─── -->
<div style="text-align:center;margin-bottom:22px">
  <div style="font-size:1.9rem;font-weight:900;
    background:linear-gradient(135deg,#a78bfa,#60a5fa,#34d399);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px">
    🃏 나머지가 같은 식 탐험
  </div>
  <div style="font-size:15px;color:#94a3b8">
    6장의 다항식 카드에서 하나를 뽑고, $x^2+1$로 나눈 나머지의 비밀을 탐구해 보세요!
  </div>
</div>

<!-- Progress -->
<div class="progress-wrap">
  <div class="progress-track">
    <div class="progress-fill" id="progressFill" style="width:0%"></div>
  </div>
  <div class="score-badge" id="scoreBadge">단계 1/4</div>
</div>

<!-- Phase Indicator -->
<div class="phase-bar" id="phaseBar">
  <div class="phase-dot active" id="ph1">1</div>
  <div class="phase-connector" id="pc1"></div>
  <div class="phase-dot" id="ph2">2</div>
  <div class="phase-connector" id="pc2"></div>
  <div class="phase-dot" id="ph3">3</div>
  <div class="phase-connector" id="pc3"></div>
  <div class="phase-dot" id="ph4">4</div>
</div>

<!-- ══════════════════ PHASE 1: 카드 뽑기 ══════════════════ -->
<div id="phase1" class="phase-panel active">
  <div class="card">
    <div class="card-title">
      <span>🃏</span>
      <span style="color:#a78bfa">단계 1</span>
      <span style="color:#e2e8f0">다항식 카드 뽑기</span>
    </div>
    <div class="info-box">
      아래 6장의 카드 중 <strong>한 장을 클릭</strong>하여 뒤집어 보세요.
      뒤집힌 카드의 다항식이 오늘의 탐구 대상 <strong>A</strong>입니다.
    </div>
    <div class="cards-grid" id="cardsGrid"></div>
    <div id="selectedInfo" style="display:none;margin-top:12px">
      <div class="success-box">
        ✅ <strong id="selectedName"></strong>을(를) 선택했습니다!<br>
        선택한 다항식: <span id="selectedFormula" style="color:#fcd34d;font-weight:700"></span>
      </div>
      <div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap">
        <button class="nav-btn btn-secondary" onclick="resetCard()">↩ 다시 선택</button>
        <button class="nav-btn btn-primary" onclick="goPhase(2)">다음 단계 → 나머지 구하기</button>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════ PHASE 2: R₁ 구하기 ══════════════════ -->
<div id="phase2" class="phase-panel">
  <div class="card">
    <div class="card-title">
      <span>✏️</span>
      <span style="color:#60a5fa">단계 2</span>
      <span style="color:#e2e8f0">다항식을 $x^2+1$로 나눠 나머지 R₁ 구하기</span>
    </div>

    <div class="hint-box" id="phase2Hint">
      선택한 카드: <span id="p2PolyName" style="font-weight:700;color:#fcd34d"></span>
    </div>

    <!-- Division steps -->
    <div class="section-title">📖 나눗셈 과정 단계별 보기</div>
    <div class="div-scene">
      <div id="divStepsDisplay"></div>
    </div>

    <div class="step-nav" style="margin-top:14px">
      <button class="nav-btn btn-secondary" id="btnDivPrev" onclick="divStep(-1)">◀ 이전</button>
      <button class="nav-btn btn-primary" id="btnDivNext" onclick="divStep(1)">다음 ▶</button>
      <span id="divStepCounter" style="font-size:12px;color:#64748b"></span>
    </div>

    <div id="r1Result" style="display:none;margin-top:16px">
      <div class="success-box">
        🎯 <strong>나머지 R₁ =</strong>
        <span id="r1Value" style="font-size:18px;color:#fcd34d;font-weight:800;margin-left:8px"></span>
      </div>
      <div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap">
        <button class="nav-btn btn-secondary" onclick="goPhase(1)">← 이전 단계</button>
        <button class="nav-btn btn-primary" onclick="goPhase(3)">다음 단계 → B 다항식 만들기</button>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════ PHASE 3: B 만들기 ══════════════════ -->
<div id="phase3" class="phase-panel">
  <div class="card">
    <div class="card-title">
      <span>🔧</span>
      <span style="color:#fbbf24">단계 3</span>
      <span style="color:#e2e8f0">나머지가 같은 B 다항식 4개 만들기</span>
    </div>

    <div class="info-box">
      💡 나머지가 같은 다항식을 만들려면?<br>
      <strong>B = (임의의 다항식) × (x²+1) + R₁</strong> 형태로 만들면 됩니다.<br>
      아래에서 $(ax^2+bx+c) \times (x^2+1) + R_1$ 의 계수를 마음대로 정해보세요!
    </div>

    <div id="phase3R1Info" style="margin:8px 0"></div>

    <!-- 4 B builders -->
    <div id="bBuilders"></div>

    <div id="bComplete" style="display:none;margin-top:12px">
      <div class="success-box">
        ✅ B 다항식 4개를 모두 완성했습니다!
      </div>
      <div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap">
        <button class="nav-btn btn-secondary" onclick="goPhase(2)">← 이전 단계</button>
        <button class="nav-btn btn-primary" onclick="goPhase(4)">다음 단계 → 표 완성하기</button>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════ PHASE 4: 표 완성 & 패턴 발견 ══════════════════ -->
<div id="phase4" class="phase-panel">
  <div class="card">
    <div class="card-title">
      <span>📊</span>
      <span style="color:#34d399">단계 4</span>
      <span style="color:#e2e8f0">표를 완성하고 패턴 발견하기</span>
    </div>

    <div class="info-box">
      A − B를 x²+1로 나누면 나머지 R₂가 어떻게 될까요?<br>
      표를 확인하고 규칙을 찾아보세요!
    </div>

    <div style="overflow-x:auto;margin:12px 0">
      <table class="results-table" id="resultsTable">
        <thead>
          <tr>
            <th>A</th>
            <th>R₁ (A ÷ (x²+1) 나머지)</th>
            <th>B</th>
            <th>A − B</th>
            <th>R₂ ((A−B) ÷ (x²+1) 나머지)</th>
          </tr>
        </thead>
        <tbody id="resultsBody"></tbody>
      </table>
    </div>

    <div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap">
      <button class="nav-btn btn-secondary" onclick="goPhase(3)">← 이전 단계</button>
      <button class="nav-btn btn-success" id="btnReveal" onclick="revealPattern()">
        🔍 패턴 발견하기
      </button>
    </div>

    <!-- Pattern discovery -->
    <div id="patternBox" style="display:none">
      <div class="discovery-box">
        <div class="discovery-title">💡 발견한 수학적 규칙!</div>
        <div style="font-size:16px;color:#c4b5fd;line-height:2;margin-bottom:14px">
          A와 B를 $x^2+1$로 나눈 나머지가 같으면 (R₁이 같으면)<br>
          <strong style="color:#fcd34d">A − B는 항상 x²+1로 나누어 떨어집니다! (R₂ = 0)</strong>
        </div>
        <div class="math-block">
          $$A \equiv B \pmod{x^2+1} \iff (x^2+1) \mid (A-B)$$
        </div>
        <div style="font-size:14px;color:#7dd3fc;margin-top:12px;line-height:2">
          이것은 정수에서의 합동(modular arithmetic)과 똑같은 원리예요!<br>
          예) 7과 3은 4로 나눈 나머지가 같음 → 7-3=4는 4의 배수!
        </div>
      </div>

      <div class="card" style="margin-top:12px">
        <div class="card-title">
          <span>🤔</span>
          <span style="color:#fbbf24">왜 항상 0일까요?</span>
        </div>
        <div id="whyBox" style="font-size:15px;color:#c0cce0;line-height:2"></div>
      </div>
    </div>
  </div>
</div>

<script>
// ═══════════════════ 데이터 ═══════════════════
const CARDS = [
  {
    id: 0,
    label: "카드 ①",
    latex: "x^3 - 3x^2 + 2x + 1",
    str:   "x³−3x²+2x+1",
    // 계수 [x³, x², x¹, x⁰]
    coef:  [1, -3, 2, 1],
    // 나눗셈 단계 (x²+1로 나누기)
    //   A = x³ − 3x² + 2x + 1
    //   x³ → x·(x²+1) → subtract → remain: −3x² + x + 1
    //   −3x² → −3·(x²+1) → subtract → remain: x + 4
    quotient: [1, -3],       // 몫의 계수 [x, const]
    remainder: [1, 4],       // 나머지 계수 [x, const]
    divSteps: [
      {
        title: "① 첫 번째 나눗셈",
        equation: "x^3 - 3x^2 + 2x + 1 = x \\cdot (x^2+1) + (-3x^2+x+1)",
        memo: "$x^3 \\div x^2 = x$ 이므로 $x$를 몫으로 잡고 뺍니다."
      },
      {
        title: "② 두 번째 나눗셈",
        equation: "-3x^2+x+1 = (-3) \\cdot (x^2+1) + (x+4)",
        memo: "$-3x^2 \\div x^2 = -3$ 이므로 $-3$을 몫으로 잡고 뺍니다."
      },
      {
        title: "③ 나눗셈 완료",
        equation: "x^3-3x^2+2x+1 = (x-3)(x^2+1) + (x+4)",
        memo: "나머지 $x+4$의 차수(1) < $x^2+1$의 차수(2) → 나눗셈 끝!"
      }
    ],
    r1Latex:  "x + 4",
  },
  {
    id: 1,
    label: "카드 ②",
    latex: "x^3 - x",
    str:   "x³−x",
    coef:  [1, 0, -1, 0],
    quotient: [1, 0],
    remainder: [-2, 0],
    divSteps: [
      {
        title: "나눗셈 완료",
        equation: "x^3 - x = x(x^2+1) + (-2x)",
        memo: "$x^3 \\div x^2 = x$로 한 번만 나누면 끝! 나머지 $-2x$의 차수(1) < 2"
      }
    ],
    r1Latex: "-2x",
  },
  {
    id: 2,
    label: "카드 ③",
    latex: "2x^3 - 4x^2",
    str:   "2x³−4x²",
    coef:  [2, -4, 0, 0],
    quotient: [2, -4],
    remainder: [-2, 4],
    divSteps: [
      {
        title: "① 첫 번째 나눗셈",
        equation: "2x^3 - 4x^2 = 2x \\cdot (x^2+1) + (-4x^2-2x)",
        memo: "$2x^3 \\div x^2 = 2x$, 빼면 $-4x^2-2x$가 남습니다."
      },
      {
        title: "② 두 번째 나눗셈",
        equation: "-4x^2-2x = (-4)(x^2+1) + (-2x+4)",
        memo: "$-4x^2 \\div x^2 = -4$, 빼면 $-2x+4$가 남습니다."
      },
      {
        title: "③ 나눗셈 완료",
        equation: "2x^3-4x^2 = (2x-4)(x^2+1) + (-2x+4)",
        memo: "나머지 $-2x+4$의 차수(1) < 2 → 나눗셈 끝!"
      }
    ],
    r1Latex: "-2x + 4",
  },
  {
    id: 3,
    label: "카드 ④",
    latex: "x^3 + x - 1",
    str:   "x³+x−1",
    coef:  [1, 0, 1, -1],
    quotient: [1, 0],
    remainder: [0, -1],
    divSteps: [
      {
        title: "나눗셈 완료",
        equation: "x^3+x-1 = x(x^2+1) + (-1)",
        memo: "$x^3 \\div x^2 = x$로 한 번만 나누면 끝! 나머지 $-1$의 차수(0) < 2"
      }
    ],
    r1Latex: "-1",
  },
  {
    id: 4,
    label: "카드 ⑤",
    latex: "x^3 + 1",
    str:   "x³+1",
    coef:  [1, 0, 0, 1],
    quotient: [1, 0],
    remainder: [-1, 1],
    divSteps: [
      {
        title: "나눗셈 완료",
        equation: "x^3+1 = x(x^2+1)+(-x+1)",
        memo: "$x^3 \\div x^2 = x$로 한 번만 나누면 끝! 나머지 $-x+1$의 차수(1) < 2"
      }
    ],
    r1Latex: "-x + 1",
  },
  {
    id: 5,
    label: "카드 ⑥",
    latex: "x^3 + x^2 + 1",
    str:   "x³+x²+1",
    coef:  [1, 1, 0, 1],
    quotient: [1, 1],
    remainder: [-1, 0],
    divSteps: [
      {
        title: "① 첫 번째 나눗셈",
        equation: "x^3+x^2+1 = x \\cdot (x^2+1) + (x^2-x+1)",
        memo: "$x^3 \\div x^2 = x$, 빼면 $x^2-x+1$이 남습니다."
      },
      {
        title: "② 두 번째 나눗셈",
        equation: "x^2-x+1 = 1 \\cdot (x^2+1) + (-x)",
        memo: "$x^2 \\div x^2 = 1$, 빼면 $-x$가 남습니다."
      },
      {
        title: "③ 나눗셈 완료",
        equation: "x^3+x^2+1 = (x+1)(x^2+1)+(-x)",
        memo: "나머지 $-x$의 차수(1) < 2 → 나눗셈 끝!"
      }
    ],
    r1Latex: "-x",
  }
];

// ═══════════════════ 상태 ═══════════════════
let selectedCard = null;
let currentDivStep = 0;
const bPolys = [null, null, null, null];  // B1~B4 계수 [x³,x²,x,1]
let bConfirmed = [false,false,false,false];
let currentPhase = 1;

function safeRenderMath(root, delimiters) {
  if (!root) return;
  if (typeof renderMathInElement !== 'function') return;
  renderMathInElement(root, {
    delimiters: delimiters || [{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}]
  });
}

function toKatexHtml(latex, displayMode) {
  if (window.katex && typeof katex.renderToString === 'function') {
    return katex.renderToString(latex, { throwOnError: false, displayMode: !!displayMode });
  }
  return displayMode ? `$$${latex}$$` : `$${latex}$`;
}

// ═══════════════════ 초기화 ═══════════════════
function init() {
  renderCards();
  updateProgress();
}

// ═══════════════════ 카드 렌더링 ═══════════════════
function renderCards() {
  const grid = document.getElementById('cardsGrid');
  grid.innerHTML = '';
  CARDS.forEach((card, i) => {
    const div = document.createElement('div');
    div.className = 'poly-card';
    div.id = `card${i}`;
    div.innerHTML = `
      <div class="card-inner">
        <div class="card-front">
          <div class="card-number">${i+1}</div>
          <div class="card-deco">POLYNOMIAL CARD</div>
        </div>
        <div class="card-back">
          <div class="card-deco" style="color:#7c3aed;font-size:9px;letter-spacing:.1em">
            ${card.label}
          </div>
          <div class="card-formula">$${card.latex}$</div>
        </div>
      </div>
    `;
    div.addEventListener('click', () => flipCard(i));
    grid.appendChild(div);
  });
  // Re-render KaTeX
  if (window._katexReady || typeof renderMathInElement !== 'undefined') {
    setTimeout(() => {
      safeRenderMath(grid, [{left:'$',right:'$',display:false}]);
    }, 700);
  }
}

function flipCard(i) {
  if (selectedCard !== null) return;
  selectedCard = i;
  const card = CARDS[i];
  document.getElementById(`card${i}`).classList.add('flipped');
  // Disable others
  setTimeout(() => {
    CARDS.forEach((_, j) => {
      if (j !== i) {
        document.getElementById(`card${j}`).classList.add('disabled');
      } else {
        document.getElementById(`card${j}`).classList.add('selected');
      }
    });
    const info = document.getElementById('selectedInfo');
    info.style.display = 'block';
    document.getElementById('selectedName').textContent = card.label;
    document.getElementById('selectedFormula').textContent = card.str;
    // Render KaTeX in info
    safeRenderMath(info);
  }, 650);
}

// ═══════════════════ 페이즈 전환 ═══════════════════
function goPhase(n) {
  document.getElementById('phase' + currentPhase).classList.remove('active');
  currentPhase = n;
  document.getElementById('phase' + n).classList.add('active');
  updateProgress();

  if (n === 2) initPhase2();
  if (n === 3) initPhase3();
  if (n === 4) initPhase4();

  // Scroll to top
  window.scrollTo({top:0,behavior:'smooth'});
}

function updateProgress() {
  const pct = ((currentPhase-1)/3)*100;
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('scoreBadge').textContent = `단계 ${currentPhase}/4`;
  [1,2,3,4].forEach(n => {
    const el = document.getElementById('ph' + n);
    el.classList.remove('active','done');
    if (n < currentPhase) el.classList.add('done');
    if (n === currentPhase) el.classList.add('active');
    if (n < 4) {
      const con = document.getElementById('pc' + n);
      con.classList.toggle('done', n < currentPhase);
    }
  });
}

// ═══════════════════ 페이즈 2: 나눗셈 단계 ═══════════════════
function initPhase2() {
  const card = CARDS[selectedCard];
  document.getElementById('p2PolyName').textContent =
    card.label + ' : A = ' + card.str;
  currentDivStep = 0;
  renderDivStep();
}

function renderDivStep() {
  const card = CARDS[selectedCard];
  const steps = card.divSteps;
  const s = steps[currentDivStep];
  const total = steps.length;

  document.getElementById('divStepCounter').textContent =
    `(${currentDivStep+1} / ${total} 단계)`;

  // Progress dots for sub-steps
  let dotHtml = '';
  for (let i = 0; i < total; i++) {
    dotHtml += `<span style="
      display:inline-block;width:10px;height:10px;border-radius:50%;margin:0 3px;
      background:${i < currentDivStep ? '#0ea5e9' : (i === currentDivStep ? '#a78bfa' : '#334155')};
      vertical-align:middle
    "></span>`;
  }

  const html = `
    <div style="margin-bottom:6px;text-align:center">${dotHtml}</div>
    <div style="
      background:#0d1b2e;border:1.5px solid #1e3a5f;border-radius:12px;
      padding:20px 22px;line-height:2
    ">
      <div style="font-size:16px;font-weight:800;color:#7dd3fc;margin-bottom:14px">
        ${s.title}
      </div>
      <div class="math-block">
        ${toKatexHtml(s.equation, true)}
      </div>
      <div style="font-size:15px;color:#fbbf24;margin-top:12px">
        💡 ${s.memo}
      </div>
    </div>
    ${currentDivStep === total-1 ? `
    <div style="
      margin-top:12px;background:rgba(248,113,113,.08);
      border:1.5px solid #ef4444;border-radius:10px;
      padding:14px 18px;font-size:16px;color:#fca5a5
    ">
      🎯 <strong>최종 나머지 R₁ =</strong>
      <span style="font-size:18px;color:#fcd34d;font-weight:900;margin-left:8px">$${card.r1Latex}$</span>
    </div>` : ''}
  `;

  document.getElementById('divStepsDisplay').innerHTML = html;
  safeRenderMath(document.getElementById('divStepsDisplay'));

  // Buttons
  document.getElementById('btnDivPrev').disabled = (currentDivStep === 0);
  const isLast = currentDivStep === total - 1;
  document.getElementById('btnDivNext').disabled = isLast;
  if (isLast) {
    const r1Div = document.getElementById('r1Result');
    r1Div.style.display = 'block';
    document.getElementById('r1Value').textContent = '';
    document.getElementById('r1Value').innerHTML = `$${CARDS[selectedCard].r1Latex}$`;
    r1Div.classList.add('fade-in');
    safeRenderMath(r1Div);
  }
}

function resetCard() {
  selectedCard = null;
  bConfirmed.fill(false);
  bPolys.fill(null);
  renderCards();
  document.getElementById('selectedInfo').style.display = 'none';
}

function divStep(dir) {
  const total = CARDS[selectedCard].divSteps.length;
  currentDivStep = Math.max(0, Math.min(total-1, currentDivStep + dir));
  renderDivStep();
}

// ═══════════════════ 페이즈 3: B 만들기 ═══════════════════
function initPhase3() {
  const card = CARDS[selectedCard];
  const r1Info = document.getElementById('phase3R1Info');
  r1Info.innerHTML = `
    <div class="hint-box">
      A = <strong>${card.str}</strong>,  나머지 R₁ = <strong>$${card.r1Latex}$</strong><br>
      B는 <strong>$B = (ax^2 + bx + c)(x^2+1) + R_1$</strong> 형태로 만듭니다.
    </div>
  `;
  safeRenderMath(r1Info);

  const container = document.getElementById('bBuilders');
  container.innerHTML = '';
  for (let k = 0; k < 4; k++) {
    container.appendChild(buildBEditor(k));
  }
}

function buildBEditor(k) {
  const wrap = document.createElement('div');
  wrap.className = 'b-builder fade-in';
  wrap.style.marginBottom = '12px';
  wrap.innerHTML = `
    <div style="font-size:13px;font-weight:700;color:#fbbf24;margin-bottom:10px">
      B${k+1} 만들기
    </div>
    <div class="b-builder-row">
      <div class="coef-group">
        <div class="coef-label">a (x²항)</div>
        <input class="coef-input" type="number" value="1" id="ba${k}"
          oninput="updateBDisplay(${k})" step="1">
      </div>
      <span class="op-label">x²</span>
      <span class="op-label" style="color:#334155">+</span>
      <div class="coef-group">
        <div class="coef-label">b (x항)</div>
        <input class="coef-input" type="number" value="0" id="bb${k}"
          oninput="updateBDisplay(${k})" step="1">
      </div>
      <span class="op-label">x</span>
      <span class="op-label" style="color:#334155">+</span>
      <div class="coef-group">
        <div class="coef-label">c (상수항)</div>
        <input class="coef-input" type="number" value="0" id="bc${k}"
          oninput="updateBDisplay(${k})" step="1">
      </div>
    </div>
    <div style="font-size:12px;color:#64748b;margin:4px 0 8px">
      ↑ 위 계수 a, b, c를 자유롭게 바꿔보세요
    </div>
    <div id="bDisplay${k}" class="poly-display" style="margin-bottom:8px"></div>
    <button class="nav-btn btn-warning" id="bConfirmBtn${k}" onclick="confirmB(${k})">
      ✔ 이 B${k+1} 사용하기
    </button>
    <div id="bConfirmInfo${k}" style="display:none;margin-top:6px"></div>
  `;
  setTimeout(() => updateBDisplay(k), 10);
  return wrap;
}

function computeB(k) {
  const a = parseInt(document.getElementById(`ba${k}`)?.value) || 0;
  const b = parseInt(document.getElementById(`bb${k}`)?.value) || 0;
  const c = parseInt(document.getElementById(`bc${k}`)?.value) || 0;
  // (ax²+bx+c)(x²+1) = ax⁴+ax²+bx³+bx+cx²+c
  // = ax⁴ + bx³ + (a+c)x² + bx + c
  // But we want degree ≤ 3 so let a=0, just ax² terms
  // Actually we allow ax²+bx+c: just degree 2 multiplier
  // B = (ax²+bx+c)(x²+1) + R1_coef
  const card = CARDS[selectedCard];
  const r = card.remainder; // [rx, r0]
  // (ax²+bx+c)(x²+1) = ax⁴ + bx³ + (a+c)x² + bx + c
  // Then + R₁ = + r[0]x + r[1]
  // Full polynomial: 0*x⁵ + a*x⁴ + b*x³ + (a+c)*x² + (b+r[0])*x + (c+r[1])
  // We'll only show up to degree 4 (truncate to degree 3 for display)
  // For the purpose of this activity, let a = 0 always to keep it degree 3
  // Actually let's keep it but note it could be degree 4 if a≠0
  return {
    // Coefficients for the multiplier part
    ma: a, mb: b, mc: c,
    // Full B polynomial coefficients [x⁴, x³, x², x, 1]
    fullCoef: [a, b, a+c, b+r[0], c+r[1]]
  };
}

function polyToLatex(coef, maxDeg) {
  // coef[0] = highest degree term (degree = maxDeg)
  let terms = [];
  for (let i = 0; i < coef.length; i++) {
    const deg = maxDeg - i;
    const val = coef[i];
    if (val === 0) continue;
    let t = '';
    const absV = Math.abs(val);
    const sign = val < 0 ? '-' : '+';
    if (deg === 0) {
      t = `${absV}`;
    } else if (deg === 1) {
      t = absV === 1 ? 'x' : `${absV}x`;
    } else {
      t = absV === 1 ? `x^{${deg}}` : `${absV}x^{${deg}}`;
    }
    terms.push({sign, t, deg});
  }
  if (terms.length === 0) return '0';
  let latex = '';
  terms.forEach((item, idx) => {
    if (idx === 0) {
      latex += (item.sign === '-' ? '-' : '') + item.t;
    } else {
      latex += ' ' + item.sign + ' ' + item.t;
    }
  });
  return latex || '0';
}

function updateBDisplay(k) {
  const bData = computeB(k);
  const { fullCoef } = bData;
  const maxDeg = fullCoef.length - 1; // 4
  const latex = polyToLatex(fullCoef, maxDeg);

  const disp = document.getElementById(`bDisplay${k}`);
  if (!disp) return;
  disp.innerHTML = `B${k+1} = $${latex}$`;
  safeRenderMath(disp, [{left:'$',right:'$',display:false}]);
}

function confirmB(k) {
  if (bConfirmed[k]) return;
  const bData = computeB(k);
  const { fullCoef } = bData;
  const maxDeg = fullCoef.length - 1;
  const latex = polyToLatex(fullCoef, maxDeg);

  const card = CARDS[selectedCard];
  const r = card.remainder;

  // Verify remainder of B ÷ (x²+1) = R₁ (always true by construction)
  bConfirmed[k] = true;
  bPolys[k] = fullCoef; // store [x⁴,x³,x²,x,1] or shorter

  document.getElementById(`bConfirmBtn${k}`).style.display = 'none';
  document.getElementById(`ba${k}`).disabled = true;
  document.getElementById(`bb${k}`).disabled = true;
  document.getElementById(`bc${k}`).disabled = true;

  const infoDiv = document.getElementById(`bConfirmInfo${k}`);
  infoDiv.style.display = 'block';
  infoDiv.innerHTML = `
    <div class="success-box" style="font-size:12px;">
      ✅ B${k+1} = <strong>$${latex}$</strong> 확정!<br>
      이 다항식을 $x^2+1$로 나누면 나머지 = <strong>$${card.r1Latex}$</strong> (= R₁과 같음!)
    </div>
  `;
  safeRenderMath(infoDiv, [{left:'$',right:'$',display:false}]);

  if (bConfirmed.every(v => v)) {
    document.getElementById('bComplete').style.display = 'block';
  }
}

// ═══════════════════ 페이즈 4: 표 & 패턴 ═══════════════════
function initPhase4() {
  const card = CARDS[selectedCard];
  const tbody = document.getElementById('resultsBody');
  tbody.innerHTML = '';

  for (let k = 0; k < 4; k++) {
    const bCoef = bPolys[k];       // [x⁴,x³,x²,x,1]
    const aCoef = [0, ...card.coef]; // [0, x³,x²,x,1] → pad to 5

    // A−B
    let abCoef = [];
    const len = Math.max(aCoef.length, bCoef.length);
    for (let i = 0; i < len; i++) {
      const ai = aCoef[aCoef.length - len + i] || 0;
      const bi = bCoef[bCoef.length - len + i] || 0;
      abCoef.push(ai - bi);
    }
    // Trim leading zeros
    while (abCoef.length > 1 && abCoef[0] === 0) abCoef.shift();
    const abMaxDeg = abCoef.length - 1;
    const abLatex = polyToLatex(abCoef, abMaxDeg);

    // R₂: remainder of (A−B) ÷ (x²+1)
    // Since B = q(x²+1) + R₁ and A = p(x²+1) + R₁
    // A−B = (p-q)(x²+1) → R₂ = 0 always
    const r2Latex = '0';
    const bMaxDeg = bCoef.length - 1;
    const bLatex = polyToLatex(bCoef, bMaxDeg);

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${card.str}</td>
      <td class="r1-cell">$${card.r1Latex}$</td>
      <td class="b-poly">$${bLatex}$</td>
      <td class="ab-cell">$${abLatex}$</td>
      <td class="r2-cell zero">$${r2Latex}$</td>
    `;
    tbody.appendChild(tr);
  }

  safeRenderMath(tbody, [{left:'$',right:'$',display:false}]);
}

function revealPattern() {
  document.getElementById('btnReveal').style.display = 'none';
  const pb = document.getElementById('patternBox');
  pb.style.display = 'block';
  pb.classList.add('fade-in');

  const card = CARDS[selectedCard];
  document.getElementById('whyBox').innerHTML = `
    <div class="math-block">
      A = $(x^2+1) \\cdot Q_A(x) + R_1$<br>
      B = $(x^2+1) \\cdot Q_B(x) + R_1$
    </div>
    <div style="font-size:13px;line-height:2;color:#c0cce0;margin-top:8px">
      위 두 식을 빼면:<br>
    </div>
    <div class="math-block">
      $A - B = (x^2+1)(Q_A(x) - Q_B(x)) + R_1 - R_1$
      $= (x^2+1)(Q_A(x) - Q_B(x))$
    </div>
    <div style="font-size:13px;line-height:2;color:#c0cce0">
      따라서 $A - B$는 $x^2+1$로 <strong style="color:#4ade80">나누어 떨어집니다!</strong>
      (나머지 = 0)
    </div>
    <div style="margin-top:12px;font-size:13px;color:#c0cce0;line-height:2">
      📌 <strong style="color:#fbbf24">핵심:</strong>
      두 다항식의 나머지가 같다 ⟺ 두 다항식의 차가 나누는 식의 <strong>배수</strong>이다!
    </div>
  `;
  safeRenderMath(document.getElementById('whyBox'));
}

// ═══════════════════ 시작 ═══════════════════
window.addEventListener('load', init);
</script>
</body>
</html>
"""


def render():
    st.markdown(
        "**나머지가 같은 식** 수행과제 활동입니다. "
        "6장의 다항식 카드 중 하나를 골라 $x^2+1$로 나눈 나머지를 구하고, "
        "같은 나머지를 가지는 다항식을 직접 만들어 패턴을 탐구해 보세요."
    )
    components.html(_HTML, height=1700, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
