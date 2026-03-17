# activities/common/mini/undefined_coefficients.py
"""
미정계수법 – 미정계수 탐정 게임
계수비교법과 수치대입법을 선택하여 미정계수를 구하는 활동
"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 ─────────────────────────────────────────────────────
_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "미정계수법"

_QUESTIONS = [
    {"type": 'markdown', "text": '**📝 미정계수법의 두 가지 방법에 대해 서술하세요**'},
    {"key": '계수비교법설명', "label": '계수비교법이 무엇인지 설명하고, 어떤 상황에 사용하기 좋은지 서술하세요.', "type": 'text_area', "height": 80},
    {"key": '수치대입법설명', "label": '수치대입법이 무엇인지 설명하고, 어떤 상황에 사용하기 좋은지 서술하세요.', "type": 'text_area', "height": 80},
    {"key": '문제만들기', "label": '직접 미정계수가 있는 항등식 문제를 만들고 풀어보세요.', "type": 'text_area', "height": 80},
    {"key": '새롭게알게된점', "label": '💡 이 활동을 통해 새롭게 알게 된 점', "type": 'text_area', "height": 90},
    {"key": '느낀점', "label": '💬 이 활동을 하면서 느낀 점', "type": 'text_area', "height": 90},
]

META = {
    "title":       "🔑 미정계수법 : 미정계수 탐정 게임",
    "description": "계수비교법과 수치대입법으로 미정계수를 구하는 문제를 풀며 각 방법의 특징을 체험합니다.",
    "order":       100,
}

# ─────────────────────────────────────────────────────────────────────────────
_GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>미정계수법 탐정 게임</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
  onload="renderMath()"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#1f2937 0%,#111827 100%);
  color:#e5e7eb;
  padding:14px 10px;
  min-height:600px
}

h2{color:#60a5fa;text-align:center;margin-bottom:8px;font-size:1.3rem}
.subtitle{text-align:center;color:#93c5fd;font-size:0.85rem;margin-bottom:16px}

/* ── 진행도 ── */
.progress-wrap{
  display:flex;align-items:center;gap:10px;margin-bottom:14px;
  background:rgba(255,255,255,0.05);padding:10px 12px;border-radius:10px
}
.progress-bar{flex:1;height:10px;background:rgba(255,255,255,0.1);border-radius:99px;overflow:hidden}
.progress-fill{
  height:100%;background:linear-gradient(90deg,#8b5cf6,#06b6d4);
  transition:width 0.3s ease
}
.score-badge{
  background:#ec4899;color:#fff;border-radius:99px;
  padding:4px 14px;font-size:0.85rem;font-weight:700;white-space:nowrap
}

/* ── 카드 레이아웃 ── */
.card{
  background:rgba(31,41,55,0.8);border:2px solid #374151;
  border-radius:14px;padding:16px;margin-bottom:16px;
  backdrop-filter:blur(10px)
}

/* ── 문제 식 ── */
.problem-title{
  font-size:0.75rem;color:#60a5fa;font-weight:700;
  text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px
}
.formula-box{
  background:rgba(59,130,246,0.1);border-left:4px solid #3b82f6;
  padding:12px 14px;border-radius:8px;margin:8px 0;
  font-size:1.05rem;color:#e0e7ff;font-weight:600;line-height:1.6
}

/* ── 방법 선택 ── */
.method-selector{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0
}
.method-btn{
  padding:12px 14px;border-radius:10px;cursor:pointer;
  transition:all 0.2s;border:2px solid;font-weight:700;
  text-align:center;font-size:0.9rem;user-select:none
}
.method-btn.coeff{
  border-color:#8b5cf6;background:rgba(139,92,246,0.1);color:#c4b5fd
}
.method-btn.coeff:hover{background:rgba(139,92,246,0.2);transform:translateY(-2px)}
.method-btn.coeff.active{background:rgba(139,92,246,0.3);border-color:#a78bfa;box-shadow:0 0 12px rgba(139,92,246,0.4)}
.method-btn.subst{
  border-color:#06b6d4;background:rgba(6,182,212,0.1);color:#67e8f9
}
.method-btn.subst:hover{background:rgba(6,182,212,0.2);transform:translateY(-2px)}
.method-btn.subst.active{background:rgba(6,182,212,0.3);border-color:#22d3ee;box-shadow:0 0 12px rgba(6,182,212,0.4)}

/* ── 풀이 섹션 ── */
.solution-section{display:none}
.solution-section.active{display:block}
.section-title{
  font-size:0.9rem;color:#fbbf24;font-weight:700;margin-top:12px;margin-bottom:8px;
  display:flex;align-items:center;gap:6px
}
.step-box{
  background:rgba(255,255,255,0.05);border:1px solid #4b5563;
  border-radius:8px;padding:10px 12px;margin:8px 0;
  font-size:0.9rem;line-height:1.5
}
.step-label{color:#93c5fd;font-weight:700}
.step-content{color:#e5e7eb;margin-top:4px}

/* ── 입력 필드 ── */
.coef-input-group{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));
  gap:10px;margin:12px 0
}
.coef-input{
  display:flex;flex-direction:column;gap:4px
}
.coef-label{
  font-size:0.8rem;color:#9ca3af;font-weight:700
}
.coef-input input{
  padding:8px 10px;border:2px solid #4b5563;border-radius:6px;
  background:rgba(0,0,0,0.3);color:#e5e7eb;
  font-size:0.95rem;font-weight:600;
  transition:all 0.2s
}
.coef-input input:focus{
  outline:none;border-color:#60a5fa;background:rgba(0,0,0,0.5);
  box-shadow:0 0 8px rgba(96,165,250,0.3)
}
.coef-input input.error{
  border-color:#ef4444;background:rgba(239,68,68,0.15);
  animation:shake 0.3s ease
}
.coef-input input.success{
  border-color:#10b981;background:rgba(16,185,129,0.15)
}

@keyframes shake{
  0%, 100%{transform:translateX(0)}
  25%{transform:translateX(-6px)}
  75%{transform:translateX(6px)}
}

/* ── 피드백 ── */
.feedback{
  margin:12px 0;padding:12px 14px;border-radius:10px;
  text-align:center;font-size:0.95rem;display:none;font-weight:700
}
.feedback.success{
  background:rgba(16,185,129,0.15);color:#86efac;border:1.5px solid #10b981;
  display:block
}
.feedback.error{
  background:rgba(239,68,68,0.15);color:#fca5a5;border:1.5px solid #ef4444;
  display:block
}

/* ── 버튼 ── */
.btn-row{
  display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:14px
}
.btn{
  padding:10px 20px;border:none;border-radius:10px;cursor:pointer;
  font-size:0.9rem;font-weight:700;transition:all 0.2s;
  text-transform:uppercase;letter-spacing:0.05em
}
.btn-check{
  background:linear-gradient(135deg,#10b981,#059669);color:#fff;
  box-shadow:0 4px 12px rgba(16,185,129,0.3)
}
.btn-check:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 6px 16px rgba(16,185,129,0.5)}
.btn-check:disabled{
  background:#6b7280;cursor:not-allowed;opacity:0.5
}
.btn-next{
  background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:#fff;
  box-shadow:0 4px 12px rgba(59,130,246,0.3)
}
.btn-next:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(59,130,246,0.5)}
.btn-reset{
  background:rgba(107,114,128,0.5);color:#d1d5db;
  border:1px solid #6b7280
}

/* ── 최종 요약 ── */
.summary-box{
  background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(59,130,246,0.1));
  border:2px solid #10b981;border-radius:12px;padding:16px;
  text-align:center;margin-top:16px;display:none
}
.summary-title{font-size:1.1rem;color:#86efac;font-weight:700;margin-bottom:8px}
.summary-text{color:#d1fae5;margin:8px 0;line-height:1.5}
.summary-icon{font-size:2rem;margin-bottom:8px}

@media(max-width:600px){
  body{padding:10px}
  .method-selector{grid-template-columns:1fr}
  h2{font-size:1.1rem}
  .formula-box{font-size:0.95rem}
}
</style>
</head>
<body>

<h2>🔑 미정계수법 탐정</h2>
<p class="subtitle">계수비교법과 수치대입법으로 미정계수를 찾아보세요!</p>

<div class="progress-wrap">
  <div class="progress-bar">
    <div class="progress-fill" id="progressFill" style="width:0%"></div>
  </div>
  <div class="score-badge">
    <span id="scoreText">0</span> / 6 정답
  </div>
</div>

<div id="gameContainer">
  <!-- 동적 렌더링 -->
</div>

<div class="summary-box" id="summaryBox">
  <div class="summary-icon">🎉</div>
  <div class="summary-title">축하합니다!</div>
  <div class="summary-text">모든 문제를 풀었습니다!</div>
  <div class="summary-text">두 방법의 특징을 정리하여 아래 성찰 폼을 완성하세요 ✏️</div>
</div>

<script>
// ── 데이터베이스 ──────────────────────────────────────────────────────────
const PROBLEMS = [
  {
    id: 1,
    left: "3x^2 - x + 4",
    right: "a(x-1)^2 + b(x-1) + c",
    type: "expand",
    answers: {a: 3, b: 5, c: 6},
    hint: "우변을 전개하면 $3x^2 + (undefined)x + (undefined)$입니다. 계수를 비교해보세요.",
    steps: {
      coeff: [
        "$a(x-1)^2 = x^2 - 2x + 1$이므로",
        "$a(x-1)^2 = ax^2 - 2ax + a$",
        "$b(x-1) = bx - b$",
        "우변을 정리하면 $ax^2 + (-2a+b)x + (a-b+c)$",
        "계수 비교: $a=3, -2a+b=-1, a-b+c=4$",
        "$a=3$을 대입하면 $b=5, c=6$"
      ],
      subst: [
        "$x=1$을 대입: $3-1+4=0+0+c$ → $c=6$",
        "$x=0$을 대입: $4=a-b+c$ → $a-b=-2$",
        "$x=2$을 대입: $12-2+4=14=a+b+c$ → $a+b=8$",
        "$a-b=-2$와 $a+b=8$에서 $a=3, b=5$ ✓"
      ]
    }
  },
  {
    id: 2,
    left: "2x - 4",
    right: "a(x - 2)",
    type: "simple",
    answers: {a: 2},
    steps: {
      coeff: [
        "$a(x-2) = ax - 2a$",
        "좌변: $2x - 4$",
        "계수 비교: $a=2, -2a=-4$ ✓ ⭐ 계수비교가 더 편함!"
      ],
      subst: [
        "$x=2$를 대입: $2(2)-4=0$ → $a(0)=0$ (정보 없음)",
        "$x=0$를 대입: $-4=-2a$ → $a=2$ ✓",
        "$x=1$를 대입: $-2=-a$ → $a=2$ ✓"
      ]
    }
  },
  {
    id: 3,
    left: "x^2 - 2x + 3",
    right: "a(x-1)^2 + b",
    type: "expand",
    answers: {a: 1, b: 2},
    steps: {
      coeff: [
        "$a(x-1)^2 + b = ax^2 - 2ax + a + b$",
        "좌변: $x^2 - 2x + 3$",
        "계수 비교: $a=1, -2a=-2$ ✓, $a+b=3$",
        "$1+b=3$ → $b=2$ ✓ ⭐ 계수비교가 더 편함!"
      ],
      subst: [
        "$x=1$를 대입: $1-2+3=2$ → $0+b=2$ → $b=2$ ✓",
        "$x=0$을 대입: $3=a+b$ → $a=1$ ✓",
        "$x=2$를 대입: $4-4+3=3=a+b$ → 확인됨 ✓"
      ]
    }
  },
  {
    id: 4,
    left: "x^2 + 2x",
    right: "a(x+1)^2 + b(x+1) + c",
    type: "expand",
    answers: {a: 1, b: 0, c: -1},
    steps: {
      coeff: [
        "$a(x+1)^2 + b(x+1) + c = ax^2 + (2a+b)x + (a+b+c)$",
        "좌변: $x^2 + 2x + 0$",
        "계수 비교: $a=1, 2a+b=2$ → $b=0, a+b+c=0$ → $c=-1$"
      ],
      subst: [
        "$x=-1$을 대입: $1-2=0$ → $0+0+c=0$ → $c=-1$ ✓",
        "$x=0$을 대입: $0=a+b+c$ (확인용)",
        "$x=1$을 대입: $1+2=3=4a+2b+c$ → $3=4+0-1$ ✓"
      ]
    }
  },
  {
    id: 5,
    left: "2x^2 + 5x + 3",
    right: "ax^2 + bx + c",
    type: "direct",
    answers: {a: 2, b: 5, c: 3},
    steps: {
      coeff: [
        "좌변과 우변이 이미 표준형입니다!",
        "계수를 직접 비교하면: $a=2, b=5, c=3$",
        "거의 순간적으로 답을 찾을 수 있습니다! ⭐⭐ 계수비교가 압도적으로 편함!"
      ],
      subst: [
        "$x=0$을 대입: $3=c$ → $c=3$ ✓",
        "$x=1$을 대입: $2+5+3=10$ → $a+b+3=10$ → $a+b=7$",
        "$x=-1$을 대입: $2-5+3=0$ → $a-b+3=0$ → $a-b=-3$",
        "$a+b=7$와 $a-b=-3$를 풀면 $a=2, b=5$ ✓",
        "수치대입법은 연립방정식을 풀어야 해서 훨씬 복잡합니다!"
      ]
    }
  },
  {
    id: 6,
    left: "(x-2)(x+3)",
    right: "(x-p)(x-q)",
    type: "factored",
    answers: {p: 2, q: -3},
    steps: {
      coeff: [
        "좌변을 전개: $(x-2)(x+3) = x^2 + x - 6$",
        "우변을 전개: $(x-p)(x-q) = x^2 - (p+q)x + pq$",
        "계수 비교: $1 = -(p+q)$ → $p+q=-1$",
        "$-6 = pq$",
        "$p+q=-1$과 $pq=-6$의 연립방정식을 풀면 $p=2, q=-3$ (또는 역순)",
        "계수비교법은 복잡한 연립방정식이 필요합니다!"
      ],
      subst: [
        "인수형이므로 근을 쉽게 찾을 수 있습니다!",
        "$x=2$를 대입: $(2-2)(2+3)=0$ → $(2-p)(2-q)=0$",
        "따라서 $p=2$ 또는 $q=2$입니다. $x=-3$로 확인하면 $p=2, q=-3$",
        "$x=-3$를 대입: $(-3-2)(-3+3)=0$ → $(-3-p)(-3-q)=0$",
        "따라서 $p=-3$ 또는 $q=-3$ → $q=-3$ ✓",
        "수치대입법이 압도적으로 편합니다! ⭐⭐ 근을 대입하면 순간적으로 답이 나옵니다!"
      ]
    }
  }
];

let currentProblemIndex = 0;
let answers = {};
let score = 0;

function renderMath(){
  if(window.renderMathInElement){
    renderMathInElement(document.body, {
      delimiters:[
        {left:'$$',right:'$$',display:true},
        {left:'$',right:'$',display:false}
      ]
    });
  }
}

function renderProblem(index){
  if(index >= PROBLEMS.length){
    showSummary();
    return;
  }

  const p = PROBLEMS[index];
  const container = document.getElementById('gameContainer');
  
  const coeffFields = p.answers;
  const coeffKeysArray = Object.keys(coeffFields);
  let coefInputsHtml = coeffKeysArray.map(k => `
    <div class="coef-input">
      <label class="coef-label">$${k}$ =</label>
      <input type="number" id="input_${k}" step="0.1" placeholder="값">
    </div>
  `).join('');

  const html = `
    <div class="card">
      <div class="problem-title">문제 ${index + 1} / 4</div>
      <div class="formula-box">
        $$${p.left} = ${p.right}$$
      </div>
      <div style="color:#93c5fd;font-size:0.85rem;margin:8px 0">
        💡 아래 두 방법 중 하나를 선택하여 미정계수를 구하세요
      </div>
      
      <div class="method-selector">
        <button class="method-btn coeff" onclick="selectMethod(${index}, 'coeff')">
          📊 계수비교법<br><small style="font-size:0.75rem;opacity:0.8">동류항의 계수 비교</small>
        </button>
        <button class="method-btn subst" onclick="selectMethod(${index}, 'subst')">
          🔢 수치대입법<br><small style="font-size:0.75rem;opacity:0.8">적당한 수를 대입</small>
        </button>
      </div>

      <div id="coeffSolution" class="solution-section">
        <div class="section-title">📊 계수비교법 풀이</div>
        <div id="coeffSteps"></div>
      </div>

      <div id="substSolution" class="solution-section">
        <div class="section-title">🔢 수치대입법 풀이</div>
        <div id="substSteps"></div>
      </div>

      <div style="margin-top:14px;padding:12px;background:rgba(255,255,255,0.05);border-radius:8px">
        <strong style="color:#e5e7eb">미정계수 입력:</strong>
        <div class="coef-input-group" style="margin-top:10px">
          ${coefInputsHtml}
        </div>
      </div>

      <div class="feedback" id="feedback"></div>

      <div class="btn-row">
        <button class="btn btn-check" id="btnCheck" onclick="checkAnswer(${index})" disabled>
          ✅ 답 확인
        </button>
        <button class="btn btn-reset" onclick="resetProblem()">🔄 초기화</button>
        <button class="btn btn-next" id="btnNext" onclick="nextProblem()" style="display:none">➡️ 다음</button>
      </div>
    </div>
  `;

  container.innerHTML = html;
  
  setTimeout(() => {
    renderMath();
    setupInputListeners(index);
  }, 100);
  
  updateProgress();
}

function selectMethod(pIdx, method){
  const p = PROBLEMS[pIdx];
  
  document.querySelectorAll('.coeff, .subst').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.solution-section').forEach(s => s.classList.remove('active'));
  
  if(method === 'coeff'){
    document.querySelector('.method-btn.coeff').classList.add('active');
    document.getElementById('coeffSolution').classList.add('active');
    renderSteps('coeffSteps', p.steps.coeff);
  } else {
    document.querySelector('.method-btn.subst').classList.add('active');
    document.getElementById('substSolution').classList.add('active');
    renderSteps('substSteps', p.steps.subst);
  }
  
  document.getElementById('btnCheck').disabled = false;
  renderMath();
}

function renderSteps(containerId, steps){
  const html = steps.map((step, i) => `
    <div class="step-box">
      <span class="step-label">Step ${i+1}:</span>
      <div class="step-content">${step}</div>
    </div>
  `).join('');
  document.getElementById(containerId).innerHTML = html;
}

function setupInputListeners(pIdx){
  const p = PROBLEMS[pIdx];
  Object.keys(p.answers).forEach(k => {
    const input = document.getElementById(`input_${k}`);
    if(input){
      input.addEventListener('input', (e) => {
        input.classList.remove('error', 'success');
      });
    }
  });
}

function checkAnswer(pIdx){
  const p = PROBLEMS[pIdx];
  const feedback = document.getElementById('feedback');
  let allCorrect = true;
  let correctCount = 0;

  Object.entries(p.answers).forEach(([key, expectedVal]) => {
    const input = document.getElementById(`input_${key}`);
    const userVal = parseFloat(input.value);
    
    if(!input.value || isNaN(userVal)){
      input.classList.add('error');
      allCorrect = false;
      return;
    }

    if(Math.abs(userVal - expectedVal) < 0.01){
      input.classList.add('success');
      correctCount++;
    } else {
      input.classList.add('error');
      allCorrect = false;
    }
  });

  if(allCorrect){
    feedback.className = 'feedback success';
    feedback.innerHTML = `✅ 정답! 모든 미정계수를 올바르게 구했습니다!`;
    score++;
    answers[pIdx] = true;
    document.getElementById('btnCheck').style.display = 'none';
    document.getElementById('btnNext').style.display = 'inline-block';
  } else {
    feedback.className = 'feedback error';
    const total = Object.keys(p.answers).length;
    feedback.innerHTML = `⚠️ ${correctCount}/${total} 정답입니다. 계산을 다시 확인해보세요.`;
  }

  updateProgress();
}

function resetProblem(){
  Object.keys(PROBLEMS[currentProblemIndex].answers).forEach(k => {
    const input = document.getElementById(`input_${k}`);
    input.value = '';
    input.classList.remove('error', 'success');
  });
  document.getElementById('feedback').className = 'feedback';
  document.getElementById('feedback').innerHTML = '';
}

function nextProblem(){
  currentProblemIndex++;
  renderProblem(currentProblemIndex);
}

function updateProgress(){
  const filled = Object.keys(answers).length;
  const percent = (filled / PROBLEMS.length) * 100;
  document.getElementById('progressFill').style.width = percent + '%';
  document.getElementById('scoreText').textContent = score;
}

function showSummary(){
  const container = document.getElementById('gameContainer');
  container.innerHTML = '';
  document.getElementById('summaryBox').style.display = 'block';
}

renderProblem(0);
</script>

</body>
</html>
"""


def render():
    st.set_page_config(page_title="미정계수법 - 미정계수 탐정 게임", layout="wide")
    
    st.markdown("""
    <style>
    .main { max-width: 100%; }
    iframe { width: 100% !important; height: 900px !important; }
    </style>
    """, unsafe_allow_html=True)
    
    components.html(_GAME_HTML, height=1400, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
