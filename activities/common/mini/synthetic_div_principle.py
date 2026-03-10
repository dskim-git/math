# activities/common/mini/synthetic_div_principle.py
"""
조립제법 원리 탐구 – 계수 비교법으로 이해하기
p5.js + KaTeX 인터랙티브 활동
"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 (공통수학1 전용) ─────────────────────────────────────
_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "조립제법원리탐구"

_QUESTIONS = [
    {"type": 'markdown', "text": '**📝 스스로 조립제법 문제 2개를 만들고 풀어보세요**'},
    {"key": '문제1', "label": '문제 1 (나눠지는 다항식과 나누는 일차식을 적어주세요)', "type": 'text_area', "height": 70},
    {"key": '답1', "label": '문제 1의 답 (몫과 나머지)', "type": 'text_input'},
    {"key": '문제2', "label": '문제 2 (나눠지는 다항식과 나누는 일차식을 적어주세요)', "type": 'text_area', "height": 70},
    {"key": '답2', "label": '문제 2의 답 (몫과 나머지)', "type": 'text_input'},
    {"key": '새롭게알게된점', "label": '💡 이 활동을 통해 새롭게 알게 된 점\n(예: 조립제법에서 각 계수가 어떤 계산으로 구해지는지 등)', "type": 'text_area', "height": 100},
    {"key": '느낀점', "label": '💬 이 활동을 하면서 느낀 점', "type": 'text_area', "height": 90},
]

META = {
    "title":       "🔢 조립제법 원리 탐구",
    "description": "계수 비교법으로 조립제법 공식이 어떻게 만들어지는지 직접 탐구하는 활동",
    "order":       35,
    "hidden":      True,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>조립제법 원리 탐구</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
  onload="window._katexReady=true; renderAllMath()"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#e2e8f0;
     padding:14px 10px;min-height:600px}

/* ── Tabs ── */
.tabs{display:flex;gap:6px;margin-bottom:18px;flex-wrap:wrap}
.tab-btn{padding:9px 20px;border-radius:10px;border:2px solid #1e293b;
         background:#141c2b;color:#7a8ea8;cursor:pointer;font-size:13.5px;
         font-weight:700;transition:all .2s}
.tab-btn.active{background:#1d3557;border-color:#3b82f6;color:#93c5fd}
.tab-panel{display:none}.tab-panel.active{display:block}

/* ── Cards ── */
.card{background:#161e2e;border:1px solid #1e293b;border-radius:14px;
      padding:18px 20px;margin-bottom:14px}
.card-title{font-size:15px;font-weight:800;color:#7dd3fc;margin-bottom:12px;
            display:flex;align-items:center;gap:7px}

/* ── Step navigator ── */
.step-nav{display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.step-dot{width:28px;height:28px;border-radius:50%;border:2px solid #334155;
          background:#1e293b;color:#64748b;font-size:11px;font-weight:700;
          display:flex;align-items:center;justify-content:center;cursor:pointer;
          transition:all .25s}
.step-dot.done{background:#0369a1;border-color:#0ea5e9;color:#fff}
.step-dot.active{background:#1d4ed8;border-color:#60a5fa;color:#fff;
                 transform:scale(1.15);box-shadow:0 0 0 4px rgba(96,165,250,.2)}
.step-label{font-size:12px;color:#475569}
.nav-btns{display:flex;gap:8px;margin-top:10px}
.nav-btn{padding:8px 20px;border-radius:8px;border:none;font-size:13px;
         font-weight:700;cursor:pointer;transition:all .2s}
.btn-prev{background:#1e293b;color:#94a3b8}.btn-prev:hover{background:#263547}
.btn-next{background:#1d4ed8;color:#fff}.btn-next:hover{background:#2563eb}
.btn-next:disabled{background:#1e293b;color:#475569;cursor:not-allowed}

/* ── Step content ── */
.step-box{background:#0d1b2e;border:1px solid #1e3a5f;border-radius:12px;
          padding:16px 18px;min-height:160px;animation:fadeIn .35s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.step-box h3{font-size:14px;font-weight:700;color:#7dd3fc;margin-bottom:10px}
.step-box p,.step-box li{font-size:13px;line-height:2;color:#c0cce0}
.step-box ul{padding-left:18px;margin-top:4px}

/* ── Math highlight ── */
.math-block{background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.18);
            border-radius:10px;padding:12px 18px;margin:10px 0;text-align:center;
            overflow-x:auto}
.math-block .katex{font-size:1.1em}
.highlight-red{color:#f87171;font-weight:800}
.highlight-blue{color:#60a5fa;font-weight:800}
.highlight-green{color:#4ade80;font-weight:800}
.highlight-yellow{color:#fbbf24;font-weight:800}

/* ── Coefficient comparison table ── */
.coef-table{width:100%;border-collapse:collapse;font-size:13px;margin:10px 0}
.coef-table th,.coef-table td{border:1px solid #1e3a5f;padding:8px 12px;text-align:center}
.coef-table th{background:#0f2340;color:#7dd3fc;font-weight:700}
.coef-table td{background:#0b1629;color:#c0cce0}
.coef-table td.a-cell{color:#fbbf24;font-weight:700}
.coef-table td.b-cell{color:#4ade80;font-weight:700}
.coef-table td.r-cell{color:#f87171;font-weight:700}
.coef-table td.formula{color:#a5b4fc;font-size:12px}

/* ── Synthetic division table ── */
.syn-table-wrap{overflow-x:auto;margin:10px 0}
.syn-table{border-collapse:collapse;font-size:14px}
.syn-table td{border:1px solid #1e3a5f;padding:9px 14px;text-align:center;
              min-width:60px;background:#0b1629}
.syn-table .alpha-cell{background:#0f2340;color:#f59e0b;font-weight:800;
                       border-right:3px solid #f59e0b}
.syn-table .row1{color:#fbbf24;font-weight:700}
.syn-table .row2{color:#60a5fa;font-size:12px}
.syn-table .row3{color:#4ade80;font-weight:700;border-top:3px solid #4b5563}
.syn-table .r-cell{border-left:3px solid #f87171;color:#f87171;font-weight:800}
.syn-table .fade-in{animation:cellFade .5s ease}
@keyframes cellFade{from{background:#1a3a1a}to{background:#0b1629}}
.syn-table .step-pointer{color:#fbbf24;font-size:18px}

/* ── Practice section ── */
.problem-header{display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.problem-selector{display:flex;gap:6px;flex-wrap:wrap}
.prob-btn{padding:6px 14px;border-radius:8px;border:2px solid #1e293b;
          background:#141c2b;color:#7a8ea8;cursor:pointer;font-size:12.5px;
          font-weight:700;transition:all .2s}
.prob-btn.active{background:#1d3557;border-color:#3b82f6;color:#93c5fd}
.prob-meta{font-size:13px;color:#94a3b8;margin-bottom:10px}

/* Input cells in practice table */
.syn-input{width:60px;padding:6px 4px;border:2px solid #334155;border-radius:6px;
           background:#0d1b2e;color:#e2e8f0;font-size:14px;font-weight:700;
           text-align:center;font-family:inherit;outline:none;transition:.2s}
.syn-input:focus{border-color:#3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,.2)}
.syn-input.correct{border-color:#22c55e!important;background:#052e16!important;color:#4ade80!important}
.syn-input.wrong{border-color:#ef4444!important;background:#2d0a0a!important;color:#f87171!important}

/* Check button */
.check-btn{padding:9px 24px;border:none;border-radius:8px;background:#1d4ed8;
           color:#fff;font-size:13.5px;font-weight:700;cursor:pointer;transition:.2s;
           margin-top:10px}
.check-btn:hover{background:#2563eb}
.check-btn.all-correct{background:#166534;color:#4ade80}

.feedback-msg{margin-top:8px;font-size:13px;font-weight:700;min-height:20px}
.feedback-msg.ok{color:#4ade80}.feedback-msg.ng{color:#f87171}

/* Progress bar */
.progress-wrap{display:flex;align-items:center;gap:8px;margin-bottom:12px}
.progress-track{flex:1;height:7px;background:#1e293b;border-radius:99px;overflow:hidden}
.progress-bar{height:100%;background:linear-gradient(90deg,#1d4ed8,#7c3aed);
              transition:width .4s;border-radius:99px}
.score-badge{background:#1d3557;color:#93c5fd;border-radius:99px;
             padding:3px 12px;font-size:12px;font-weight:700}

/* Step arrows for derivation */
.arrow-row{display:flex;align-items:center;justify-content:center;
           gap:4px;margin:6px 0;flex-wrap:wrap}
.arrow-btn{padding:4px 12px;border:2px solid #334155;border-radius:6px;
           color:#94a3b8;font-size:12px;cursor:pointer;background:#141c2b;
           transition:.2s}
.arrow-btn.show-step{border-color:#1d4ed8;color:#93c5fd;background:#1d3557}

/* Recurrence formula display */
.recur-list{display:flex;flex-direction:column;gap:10px;margin:10px 0}
.recur-item{display:flex;align-items:center;gap:10px;padding:10px 14px;
            background:#0d1b2e;border:1px solid #1e3a5f;border-radius:10px}
.recur-num{width:28px;height:28px;border-radius:50%;background:#1d3557;
           color:#7dd3fc;font-size:11px;font-weight:700;
           display:flex;align-items:center;justify-content:center;flex-shrink:0}
.recur-text{font-size:12.5px;color:#c0cce0;flex:1}
.recur-formula{font-size:12px;color:#a5b4fc}
</style>
</head>
<body>

<!-- ────────────────────────────── HEADER ────────────────────────────── -->
<div style="text-align:center;margin-bottom:18px">
  <div style="font-size:1.4rem;font-weight:800;color:#7dd3fc;margin-bottom:4px">
    🔢 조립제법 원리 탐구
  </div>
  <div style="font-size:12.5px;color:#64748b">
    계수 비교법으로 조립제법의 공식이 어떻게 만들어지는지 단계별로 확인해 보세요
  </div>
</div>

<!-- Progress -->
<div class="progress-wrap">
  <div class="progress-track"><div class="progress-bar" id="progressBar" style="width:0%"></div></div>
  <div class="score-badge">진행 <span id="progressTxt">0/5</span></div>
</div>

<!-- ────────────────────────────── TABS ────────────────────────────── -->
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('theory',this)">📖 원리 이해</button>
  <button class="tab-btn" onclick="switchTab('practice',this)">✏️ 조립제법 연습</button>
</div>

<!-- ══════════════════════ TAB: 원리 이해 ══════════════════════ -->
<div id="tab-theory" class="tab-panel active">

  <!-- Step dots -->
  <div class="step-nav">
    <span class="step-label">단계:</span>
    <div id="step-dots"></div>
    <div class="nav-btns">
      <button class="nav-btn btn-prev" onclick="changeStep(-1)">◀ 이전</button>
      <button class="nav-btn btn-next" id="btnNext" onclick="changeStep(1)">다음 ▶</button>
    </div>
  </div>

  <!-- Step content area -->
  <div id="stepContent" class="step-box"></div>

  <!-- Synthetic division animated table -->
  <div class="card" id="synthTableCard" style="display:none">
    <div class="card-title">📊 조립제법 표 (애니메이션)</div>
    <div style="font-size:12.5px;color:#64748b;margin-bottom:10px">
      예시: <span style="color:#fbbf24">3x³ - 2x² + x - 4</span>를
      <span style="color:#f87171">x - 2</span>로 나눌 때 (α = 2)
    </div>
    <div class="syn-table-wrap">
      <table class="syn-table" id="animTheoTable">
        <tr id="animRow1"><td class="alpha-cell" rowspan="3">2</td></tr>
        <tr id="animRow2"></tr>
        <tr id="animRow3"></tr>
      </table>
    </div>
    <div id="tableStepMsg" style="margin-top:10px;font-size:13px;color:#94a3b8"></div>
    <div style="display:flex;gap:8px;margin-top:10px">
      <button class="nav-btn btn-prev" onclick="animPrev()">◀ 이전</button>
      <button class="nav-btn btn-next" id="animNextBtn" onclick="animNext()">▶ 다음 계산</button>
      <button class="nav-btn btn-prev" onclick="resetAnimTable()">↩ 처음</button>
    </div>
  </div>

</div><!-- /tab-theory -->

<!-- ══════════════════════ TAB: 연습 ══════════════════════ -->
<div id="tab-practice" class="tab-panel">

  <div class="problem-header">
    <div style="font-size:14px;font-weight:700;color:#7dd3fc">문제 선택:</div>
    <div class="problem-selector" id="probSelector"></div>
  </div>

  <div class="card" id="practiceCard">
    <div class="card-title" id="practiceTitle">✏️ 조립제법 연습</div>
    <div class="prob-meta" id="probMeta"></div>

    <div style="font-size:12.5px;color:#94a3b8;margin-bottom:10px">
      💡 <strong>빈 칸</strong>에 값을 입력하고 <strong>채점하기</strong>를 눌러보세요.
      <br>• 2행: α × (바로 앞 3행의 값)을 입력
      <br>• 3행: 1행 + 2행의 값을 입력 (맨 앞은 그대로)
    </div>

    <div class="syn-table-wrap" id="practiceTableWrap"></div>
    <button class="check-btn" id="checkBtn" onclick="checkAnswer()">✅ 채점하기</button>
    <div class="feedback-msg" id="practiceFeedback"></div>

    <div id="resultDisplay" style="display:none;margin-top:14px;padding:14px;
         background:#0d2a0d;border:1px solid #166534;border-radius:10px">
      <div style="font-size:13px;color:#4ade80;font-weight:700;margin-bottom:6px">🎉 정답입니다!</div>
      <div id="resultText" style="font-size:13px;color:#c0cce0;line-height:1.9"></div>
    </div>
  </div>

</div><!-- /tab-practice -->

<!-- ─────────────────────────────────────────────────────── -->
<script>
// ━━━━━━━━━━━━━━━━━━ MATH RENDER ━━━━━━━━━━━━━━━━━━
function renderAllMath() {
  if (!window.renderMathInElement) return;
  renderMathInElement(document.body, {
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '$', right: '$', display: false}
    ],
    throwOnError: false
  });
}
function renderNode(el) {
  if (!window.renderMathInElement) {
    setTimeout(() => renderNode(el), 200);
    return;
  }
  renderMathInElement(el, {
    delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
    throwOnError:false
  });
}

// ━━━━━━━━━━━━━━━━━━ TAB SWITCH ━━━━━━━━━━━━━━━━━━
function switchTab(id, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  btn.classList.add('active');
  if (id === 'theory') renderAllMath();
}

// ━━━━━━━━━━━━━━━━━━ THEORY STEPS ━━━━━━━━━━━━━━━━━━
const STEPS = [
  {
    title: '📌 Step 1 · 나눗셈의 기본 식',
    content: `
      <h3>다항식 나눗셈의 기본 식</h3>
      <p>차수가 <span class="highlight-yellow">n</span>인 다항식 $P(x)$를 일차식 $(x - \\alpha)$로 나눌 때,
      몫 $Q(x)$의 차수는 <span class="highlight-green">n-1</span>이고 나머지 $R$은 상수입니다.</p>
      <div class="math-block">
        $$P(x) = (x - \\alpha) \\cdot Q(x) + R$$
      </div>
      <ul>
        <li>$P(x) = a_n x^n + a_{n-1}x^{n-1} + \\cdots + a_1 x + a_0$</li>
        <li>$Q(x) = b_{n-1}x^{n-1} + b_{n-2}x^{n-2} + \\cdots + b_1 x + b_0$</li>
        <li>$R$ : 나머지 (상수)</li>
      </ul>
      <p style="margin-top:10px;color:#64748b;font-size:12px">
        💡 우리의 목표: <strong>주어진 $a$ 계수들</strong>로부터
        <strong>$b$ 계수들과 $R$</strong>을 효율적으로 계산하는 방법을 찾는 것!
      </p>
    `
  },
  {
    title: '📌 Step 2 · 우변을 전개',
    content: `
      <h3>$(x-\\alpha) \\cdot Q(x)$를 전개해 봅시다</h3>
      <p>$Q(x) = b_{n-1}x^{n-1} + b_{n-2}x^{n-2} + \\cdots + b_1x + b_0$로 놓으면:</p>
      <div class="math-block">
        $$(x-\\alpha)Q(x) = \\underbrace{b_{n-1}x^n}_{x \\cdot b_{n-1}x^{n-1}}
        + \\underbrace{(b_{n-2} - \\alpha b_{n-1})x^{n-1}}_{x \\cdot b_{n-2}x^{n-2} - \\alpha b_{n-1}x^{n-1}}
        + \\cdots$$
      </div>
      <p>전개를 계속하면:</p>
      <div class="math-block">
        $$= b_{n-1}x^n + (b_{n-2}-\\alpha b_{n-1})x^{n-1} + (b_{n-3}-\\alpha b_{n-2})x^{n-2}
        + \\cdots + (b_0 - \\alpha b_1)x + (R - \\alpha b_0)$$
      </div>
      <p style="font-size:12px;color:#94a3b8;margin-top:8px">
        🔑 핵심: 각 차수의 계수는 <span class="highlight-green">현재 b</span>와 
        <span class="highlight-blue">α × 이전 b</span>의 조합으로 표현됩니다.
      </p>
    `
  },
  {
    title: '📌 Step 3 · 계수 비교',
    content: `
      <h3>양변의 계수를 비교합니다</h3>
      <p>$P(x) = (x-\\alpha)Q(x)+R$의 양변에서 같은 차수의 계수를 비교하면:</p>
      <table class="coef-table">
        <thead>
          <tr><th>차수</th><th>P(x) 계수</th><th>우변 계수</th><th>결론</th></tr>
        </thead>
        <tbody>
          <tr><td>$x^n$</td><td class="a-cell">$a_n$</td>
              <td>$b_{n-1}$</td>
              <td class="formula">$b_{n-1} = a_n$</td></tr>
          <tr><td>$x^{n-1}$</td><td class="a-cell">$a_{n-1}$</td>
              <td>$b_{n-2} - \\alpha b_{n-1}$</td>
              <td class="formula">$b_{n-2} = a_{n-1} + \\alpha b_{n-1}$</td></tr>
          <tr><td>$x^{n-2}$</td><td class="a-cell">$a_{n-2}$</td>
              <td>$b_{n-3} - \\alpha b_{n-2}$</td>
              <td class="formula">$b_{n-3} = a_{n-2} + \\alpha b_{n-2}$</td></tr>
          <tr><td>$\\vdots$</td><td class="a-cell">$\\vdots$</td>
              <td>$\\vdots$</td><td class="formula">$\\vdots$</td></tr>
          <tr><td>$x$</td><td class="a-cell">$a_1$</td>
              <td>$b_0 - \\alpha b_1$</td>
              <td class="formula">$b_0 = a_1 + \\alpha b_1$</td></tr>
          <tr><td>$1$ (상수)</td><td class="a-cell">$a_0$</td>
              <td>$R - \\alpha b_0$</td>
              <td class="formula r-cell">$R = a_0 + \\alpha b_0$</td></tr>
        </tbody>
      </table>
    `
  },
  {
    title: '📌 Step 4 · 점화식(재귀식) 정리',
    content: `
      <h3>계산 순서를 정리하면</h3>
      <p>점화식 형태로 정리하면 모든 $b_k$와 $R$을 단계적으로 계산할 수 있습니다:</p>
      <div class="recur-list">
        <div class="recur-item">
          <div class="recur-num">①</div>
          <div>
            <div class="recur-formula">$b_{n-1} = a_n$</div>
            <div class="recur-text">맨 앞 계수는 그대로 내려씁니다</div>
          </div>
        </div>
        <div class="recur-item">
          <div class="recur-num">②</div>
          <div>
            <div class="recur-formula">$b_{k-1} = a_k + \\alpha \\cdot b_k \\ \\ (k = n-1, n-2, \\ldots, 1)$</div>
            <div class="recur-text">앞의 $b$에 $\\alpha$를 곱해서 다음 $a$ 계수에 더합니다</div>
          </div>
        </div>
        <div class="recur-item">
          <div class="recur-num">③</div>
          <div>
            <div class="recur-formula r-cell">$R = a_0 + \\alpha \\cdot b_0$</div>
            <div class="recur-text">마지막으로 나머지 $R$을 구합니다</div>
          </div>
        </div>
      </div>
      <p style="font-size:12px;color:#94a3b8;margin-top:8px">
        💡 이 계산을 표로 정리한 것이 <strong>조립제법 표</strong>입니다!
      </p>
    `
  },
  {
    title: '📌 Step 5 · 조립제법 표 (예시)',
    content: `
      <h3>예시: $3x^3 - 2x^2 + x - 4$를 $x-2$로 나누기 (α = 2)</h3>
      <p>아래 버튼을 눌러 표가 채워지는 과정을 단계별로 확인하세요!</p>
      <p style="font-size:12px;color:#64748b;margin-top:6px">
        표 구조: <br>
        • 1행: α (맨 왼쪽), 그 다음 $a_n, a_{n-1}, \\ldots, a_0$<br>
        • 2행: α × (바로 앞 3행의 값)<br>
        • 3행: 1행 + 2행 → 몫의 계수 $b_k$, 마지막이 나머지 $R$
      </p>
    `
  },
];

let curStep = 0;

function buildStepDots() {
  const container = document.getElementById('step-dots');
  container.innerHTML = '';
  const wrap = document.createElement('div');
  wrap.style.display = 'flex'; wrap.style.gap = '6px';
  for (let i = 0; i < STEPS.length; i++) {
    const d = document.createElement('div');
    d.className = 'step-dot' + (i < curStep ? ' done' : '') + (i === curStep ? ' active' : '');
    d.textContent = i + 1;
    d.onclick = () => gotoStep(i);
    wrap.appendChild(d);
  }
  container.appendChild(wrap);
}

function gotoStep(n) {
  curStep = n;
  renderStep();
}

function changeStep(dir) {
  curStep = Math.max(0, Math.min(STEPS.length - 1, curStep + dir));
  renderStep();
}

function renderStep() {
  buildStepDots();
  const s = STEPS[curStep];
  const box = document.getElementById('stepContent');
  box.innerHTML = `<h3>${s.title}</h3>` + s.content;
  renderNode(box);

  document.getElementById('btnNext').disabled = (curStep >= STEPS.length - 1);

  // Last step shows animated table card
  const tableCard = document.getElementById('synthTableCard');
  if (curStep === STEPS.length - 1) {
    tableCard.style.display = 'block';
    if (!window._animInitDone) { initAnimTable(); window._animInitDone = true; }
  } else {
    tableCard.style.display = 'none';
  }
}

// ━━━━━━━━━━━━━━━━━━ ANIMATED SYNTH TABLE ━━━━━━━━━━━━━━━━━━
// Example: 3x³ - 2x² + x - 4, α=2
const EX_COEFFS = [3, -2, 1, -4];
const EX_ALPHA  = 2;
let animStep = 0;

// b values & row2
let exRow3 = []; let exRow2 = new Array(EX_COEFFS.length).fill(null);

function computeAnswer(coeffs, alpha) {
  const r3 = []; const r2 = new Array(coeffs.length).fill(null);
  r3.push(coeffs[0]);
  for (let i = 1; i < coeffs.length; i++) {
    r2[i] = alpha * r3[i-1];
    r3.push(coeffs[i] + r2[i]);
  }
  return {r2, r3};
}

function initAnimTable() {
  const res = computeAnswer(EX_COEFFS, EX_ALPHA);
  exRow3 = res.r3; exRow2 = res.r2;

  const r1 = document.getElementById('animRow1');
  const r2 = document.getElementById('animRow2');
  const r3 = document.getElementById('animRow3');
  r2.innerHTML = ''; r3.innerHTML = '';
  // alpha-cell(첫 번째 child)은 유지하고 계수 셀만 제거
  while (r1.children.length > 1) r1.removeChild(r1.lastChild);

  // Row 1: coefficients (visible immediately)
  EX_COEFFS.forEach(c => {
    const td = document.createElement('td');
    td.className = 'row1';
    td.textContent = fmtNum(c);
    r1.appendChild(td);
  });

  // Row 2: alpha*b cells (initially empty)
  r2.appendChild(document.createElement('td')); // empty first
  for (let i = 1; i < EX_COEFFS.length; i++) {
    const td = document.createElement('td');
    td.id = `at2-${i}`; td.className = 'row2';
    td.textContent = '';
    r2.appendChild(td);
  }

  // Row 3: b cells (initially empty)
  for (let i = 0; i < EX_COEFFS.length; i++) {
    const td = document.createElement('td');
    td.id = `at3-${i}`;
    td.className = (i === EX_COEFFS.length -1) ? 'row3 r-cell' : 'row3';
    td.textContent = '';
    r3.appendChild(td);
  }

  animStep = 0;
  document.getElementById('animNextBtn').disabled = false;
  updateAnimMsg();
}

function fmtNum(n) { if (n === null || n === undefined) return ''; return n >= 0 ? String(n) : '−'+Math.abs(n); }

const ANIM_MSGS = [
  '① α = 2, 계수 [3, −2, 1, −4]를 1행에 씁니다.',
  '② b₂ = a₃ = 3 (맨 앞 계수 그대로 내려씁니다)',
  '③ 2×b₂ = 2×3 = 6 → 2행에 기록',
  '④ b₁ = a₂ + 6 = −2 + 6 = 4 → 3행에 기록',
  '⑤ 2×b₁ = 2×4 = 8 → 2행에 기록',
  '⑥ b₀ = a₁ + 8 = 1 + 8 = 9 → 3행에 기록',
  '⑦ 2×b₀ = 2×9 = 18 → 2행에 기록',
  '⑧ R = a₀ + 18 = −4 + 18 = 14 → 나머지!  ✅ 몫: 3x² + 4x + 9, 나머지: 14',
];

const ANIM_ACTIONS = [
  () => {}, // step 0: already shown row1 
  () => { // step 1: show b[0]=3
    const td = document.getElementById('at3-0');
    td.textContent = fmtNum(exRow3[0]); td.classList.add('fade-in');
  },
  () => { // step 2: show row2[1]
    const td = document.getElementById('at2-1');
    td.textContent = fmtNum(exRow2[1]); td.classList.add('fade-in');
  },
  () => { // step 3: show b[1]
    const td = document.getElementById('at3-1');
    td.textContent = fmtNum(exRow3[1]); td.classList.add('fade-in');
  },
  () => { // step 4: show row2[2]
    const td = document.getElementById('at2-2');
    td.textContent = fmtNum(exRow2[2]); td.classList.add('fade-in');
  },
  () => { // step 5: show b[2]
    const td = document.getElementById('at3-2');
    td.textContent = fmtNum(exRow3[2]); td.classList.add('fade-in');
  },
  () => { // step 6: show row2[3]
    const td = document.getElementById('at2-3');
    td.textContent = fmtNum(exRow2[3]); td.classList.add('fade-in');
  },
  () => { // step 7: show R
    const td = document.getElementById('at3-3');
    td.textContent = fmtNum(exRow3[3]); td.classList.add('fade-in');
  }
];

function updateAnimMsg() {
  const msg = document.getElementById('tableStepMsg');
  if (animStep < ANIM_MSGS.length) msg.textContent = ANIM_MSGS[animStep];
}

function animNext() {
  if (animStep < ANIM_ACTIONS.length - 1) animStep++;
  ANIM_ACTIONS[animStep]();
  updateAnimMsg();
  if (animStep >= ANIM_ACTIONS.length - 1)
    document.getElementById('animNextBtn').disabled = true;
}
function animPrev() {
  animStep = 0;
  initAnimTable();
}
function resetAnimTable() {
  window._animInitDone = false;
  animStep = 0;
  initAnimTable();
}

// ━━━━━━━━━━━━━━━━━━ PRACTICE PROBLEMS ━━━━━━━━━━━━━━━━━━
const PROBS = [
  {
    label: '문제①', degree: 3,
    coeffs: [3,-2,1,-4], alpha: 2,
    polyStr: '3x³ − 2x² + x − 4',  divisor: 'x − 2',
  },
  {
    label: '문제②', degree: 2,
    coeffs: [2,1,-3], alpha: -1,
    polyStr: '2x² + x − 3',  divisor: 'x + 1',
  },
  {
    label: '문제③', degree: 3,
    coeffs: [1,0,0,-8], alpha: 2,
    polyStr: 'x³ − 8',  divisor: 'x − 2',
  },
  {
    label: '문제④', degree: 3,
    coeffs: [1,-4,5,-2], alpha: 1,
    polyStr: 'x³ − 4x² + 5x − 2',  divisor: 'x − 1',
  },
  {
    label: '문제⑤', degree: 4,
    coeffs: [2,-3,0,4,-1], alpha: 3,
    polyStr: '2x⁴ − 3x³ + 4x − 1',  divisor: 'x − 3',
  },
];

let curProb = 0;
const solvedSet = new Set();

function buildProbSelector() {
  const sel = document.getElementById('probSelector');
  sel.innerHTML = '';
  PROBS.forEach((p, i) => {
    const btn = document.createElement('button');
    btn.className = 'prob-btn' + (i === curProb ? ' active' : '');
    btn.textContent = p.label + (solvedSet.has(i) ? ' ✅' : '');
    btn.onclick = () => loadProb(i);
    sel.appendChild(btn);
  });
}

function loadProb(idx) {
  curProb = idx;
  buildProbSelector();
  const p = PROBS[idx];
  document.getElementById('practiceTitle').textContent = `✏️ ${p.polyStr} ÷ (${p.divisor})`;
  document.getElementById('probMeta').innerHTML =
    `α = <strong style="color:#f59e0b">${p.alpha > 0 ? p.alpha : '('+p.alpha+')'}</strong> &nbsp;|&nbsp; 차수: ${p.degree}차`;

  const res = computeAnswer(p.coeffs, p.alpha);
  renderPracticeTable(p, res.r2, res.r3);
  document.getElementById('practiceFeedback').textContent = '';
  document.getElementById('practiceFeedback').className = 'feedback-msg';
  document.getElementById('resultDisplay').style.display = 'none';
  document.getElementById('checkBtn').className = 'check-btn';
  document.getElementById('checkBtn').textContent = '✅ 채점하기';
}

function renderPracticeTable(p, ansRow2, ansRow3) {
  const wrap = document.getElementById('practiceTableWrap');
  const n = p.coeffs.length;

  let html = '<table class="syn-table">';
  // Row 1
  html += '<tr><td class="alpha-cell" rowspan="3" style="font-size:18px;font-weight:800;color:#f59e0b">'
        + (p.alpha < 0 ? '−'+Math.abs(p.alpha) : p.alpha) + '</td>';
  for (let i = 0; i < n; i++) {
    html += `<td class="row1">${fmtNum(p.coeffs[i])}</td>`;
  }
  html += '</tr>';

  // Row 2
  html += '<tr><td></td>'; // empty under alpha*b[0] (doesn't exist)
  for (let i = 1; i < n; i++) {
    html += `<td class="row2"><input class="syn-input" data-row="2" data-col="${i}"
      data-ans="${ansRow2[i]}" type="number" placeholder="?"></td>`;
  }
  html += '</tr>';

  // Row 3
  html += '<tr>';
  for (let i = 0; i < n; i++) {
    const cls = (i === n-1) ? 'row3 r-cell' : 'row3';
    if (i === 0) {
      // First cell is given (= a_n)
      html += `<td class="${cls}">${fmtNum(ansRow3[0])}</td>`;
    } else {
      html += `<td class="${cls}"><input class="syn-input" data-row="3" data-col="${i}"
        data-ans="${ansRow3[i]}" type="number" placeholder="?"></td>`;
    }
  }
  html += '</tr></table>';
  wrap.innerHTML = html;
}

function checkAnswer() {
  const inputs = document.querySelectorAll('#practiceTableWrap .syn-input');
  let allOk = true;
  let wrongCount = 0;

  inputs.forEach(inp => {
    const ans = parseInt(inp.dataset.ans);
    const val = parseInt(inp.value);
    if (isNaN(val)) { inp.classList.add('wrong'); inp.classList.remove('correct'); allOk = false; wrongCount++; return; }
    if (val === ans) {
      inp.classList.add('correct'); inp.classList.remove('wrong');
    } else {
      inp.classList.add('wrong'); inp.classList.remove('correct');
      allOk = false; wrongCount++;
    }
  });

  const fb = document.getElementById('practiceFeedback');
  const btn = document.getElementById('checkBtn');

  if (allOk) {
    fb.textContent = '🎉 모두 정답입니다!';
    fb.className = 'feedback-msg ok';
    btn.className = 'check-btn all-correct';
    btn.textContent = '✅ 정답!';
    solvedSet.add(curProb);
    buildProbSelector();
    showResult();
    updateProgress();
  } else {
    fb.textContent = `❌ ${wrongCount}개 틀렸습니다. 다시 확인해 보세요.`;
    fb.className = 'feedback-msg ng';
  }
}

function showResult() {
  const p = PROBS[curProb];
  const res = computeAnswer(p.coeffs, p.alpha);
  const bArr = res.r3;
  const n = p.coeffs.length;
  const R = bArr[n-1];

  // Build quotient polynomial string
  let quotientTerms = [];
  for (let i = 0; i < n-1; i++) {
    const exp = n-2-i;
    const coef = bArr[i];
    if (coef === 0) continue;
    let term = '';
    const abs = Math.abs(coef);
    const sign = coef < 0 ? '−' : (quotientTerms.length > 0 ? '+' : '');
    if (exp === 0) term = sign + abs;
    else if (exp === 1) term = sign + (abs === 1 ? '' : abs) + 'x';
    else term = sign + (abs === 1 ? '' : abs) + 'x' + toSup(exp);
    quotientTerms.push(term);
  }
  const qStr = quotientTerms.join(' ') || '0';

  document.getElementById('resultText').innerHTML =
    `<strong>몫</strong>: Q(x) = ${qStr}<br>
     <strong>나머지</strong>: R = ${R < 0 ? '−'+Math.abs(R) : R}<br><br>
     <strong>확인</strong>: ${p.polyStr} = (${p.divisor})(${qStr}) + ${R < 0 ? '('+R+')' : R}`;
  document.getElementById('resultDisplay').style.display = 'block';
}

function toSup(n) {
  const sups = ['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹'];
  return String(n).split('').map(d=>sups[+d]).join('');
}

function updateProgress() {
  const count = solvedSet.size;
  const total = PROBS.length;
  document.getElementById('progressBar').style.width = (count/total*100)+'%';
  document.getElementById('progressTxt').textContent = count+'/'+total;
}

// ━━━━━━━━━━━━━━━━━━ INIT ━━━━━━━━━━━━━━━━━━
renderStep();
buildProbSelector();
loadProb(0);
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────

def render():
    st.header("🔢 조립제법 원리 탐구")
    st.caption(
        "**계수 비교법**으로 조립제법 공식이 어떻게 유도되는지 단계별로 확인하고, "
        "직접 조립제법 표를 완성해 보세요."
    )
    components.html(_HTML, height=960, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
