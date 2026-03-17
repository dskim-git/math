# activities/common/mini/identity_game.py
"""
항등식의 성질 – 항등식 탐정 게임
주어진 식에 여러 값을 대입하여 항등식과 방정식을 구분하는 활동
"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 ─────────────────────────────────────────────────────
_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "항등식의성질"

_QUESTIONS = [
    {"type": 'markdown', "text": '**📝 이 활동을 하면서 찾은 항등식의 성질에 대해 서술하세요**'},
    {"key": '항등식조건', "label": '어떤 등식이 "항등식"이 되기 위한 조건을 설명해보세요.', "type": 'text_area', "height": 80},
    {"key": '문제만들기', "label": '배운 항등식의 성질을 이용하여 항등식 1개를 직접 만들어보세요. (예: 좌변 = 우변)', "type": 'text_area', "height": 80},
    {"key": '새롭게알게된점', "label": '💡 이 활동을 통해 새롭게 알게 된 점', "type": 'text_area', "height": 90},
    {"key": '느낀점', "label": '💬 이 활동을 하면서 느낀 점', "type": 'text_area', "height": 90},
]

META = {
    "title":       "🔍 항등식 탐정 : 항등식의 성질",
    "description": "여러 값을 대입하여 항등식과 방정식을 구분하고, 항등식의 성질을 탐구하는 활동입니다.",
    "order":       99,
}

# ─────────────────────────────────────────────────────────────────────────────
_GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>항등식 탐정 게임</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
  onload="renderMath()"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);
  color:#e2e8f0;
  padding:14px 10px;
  min-height:600px
}

h2{color:#a78bfa;text-align:center;margin-bottom:8px;font-size:1.3rem}
.subtitle{text-align:center;color:#c4b5fd;font-size:0.85rem;margin-bottom:16px}

/* ── 진행도 ── */
.progress-wrap{
  display:flex;align-items:center;gap:10px;margin-bottom:14px;
  background:rgba(255,255,255,0.05);padding:10px 12px;border-radius:10px
}
.progress-bar{flex:1;height:10px;background:rgba(255,255,255,0.1);border-radius:99px;overflow:hidden}
.progress-fill{
  height:100%;background:linear-gradient(90deg,#fbbf24,#f97316);
  transition:width 0.3s ease
}
.score-badge{
  background:#10b981;color:#fff;border-radius:99px;
  padding:4px 14px;font-size:0.85rem;font-weight:700;white-space:nowrap
}

/* ── 카드 레이아웃 ── */
.card{
  background:rgba(30,27,75,0.8);border:2px solid #6366f1;
  border-radius:14px;padding:16px;margin-bottom:16px;
  backdrop-filter:blur(10px)
}

/* ── 문제 식 ── */
.problem-title{
  font-size:0.75rem;color:#a78bfa;font-weight:700;
  text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px
}
.formula-box{
  background:rgba(99,102,241,0.1);border-left:4px solid #818cf8;
  padding:12px 14px;border-radius:8px;margin:8px 0;
  font-size:1.1rem;color:#e0e7ff;font-weight:600
}

/* ── 값 대입 섹션 ── */
.substitution-grid{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
  gap:10px;margin:12px 0
}
.sub-item{
  background:rgba(255,255,255,0.08);border:1.5px solid #4f46e5;
  border-radius:10px;padding:10px 12px;text-align:center;
  cursor:pointer;transition:all 0.2s;user-select:none
}
.sub-item:hover{
  background:rgba(99,102,241,0.2);border-color:#818cf8;
  transform:translateY(-2px);box-shadow:0 4px 12px rgba(129,142,248,0.3)
}
.sub-item.checked{
  background:rgba(16,185,129,0.15);border-color:#10b981;
  box-shadow:0 0 12px rgba(16,185,129,0.4)
}
.sub-item.error{
  background:rgba(239,68,68,0.15);border-color:#ef4444;
  animation:shake 0.3s ease
}
.sub-label{font-size:0.75rem;color:#a1a5b8;margin-bottom:4px}
.sub-values{font-size:1rem;color:#e0e7ff;font-weight:700}

@keyframes shake{
  0%, 100%{transform:translateX(0)}
  25%{transform:translateX(-6px)}
  75%{transform:translateX(6px)}
}

/* ── 결과 표시 ── */
.result-table{
  width:100%;border-collapse:collapse;
  font-size:0.9rem;margin:10px 0
}
.result-table th{
  background:rgba(99,102,241,0.2);color:#a78bfa;
  padding:8px;text-align:left;font-weight:700;border-bottom:2px solid #4f46e5
}
.result-table td{
  padding:8px;border-bottom:1px solid rgba(79,70,229,0.3)
}
.result-table tr:hover{background:rgba(99,102,241,0.1)}
.result-left{color:#38bdf8}
.result-right{color:#facc15}
.result-match{color:#10b981;font-weight:700}
.result-nomatch{color:#ef4444;font-weight:700}

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
.btn-check:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(16,185,129,0.5)}
.btn-check:disabled{
  background:#6b7280;cursor:not-allowed;
  box-shadow:none;transform:none
}
.btn-next{
  background:linear-gradient(135deg,#818cf8,#6366f1);color:#fff;
  box-shadow:0 4px 12px rgba(99,102,241,0.3)
}
.btn-next:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(99,102,241,0.5)}
.btn-reset{
  background:rgba(107,114,128,0.5);color:#d1d5db;
  border:1px solid #6b7280
}

/* ── 피드백 ── */
.feedback{
  margin:12px 0;padding:12px 14px;border-radius:10px;
  text-align:center;font-size:0.95rem;display:none
}
.feedback.success{
  background:rgba(16,185,129,0.15);color:#86efac;border:1.5px solid #10b981;
  display:block
}
.feedback.error{
  background:rgba(239,68,68,0.15);color:#fca5a5;border:1.5px solid #ef4444;
  display:block
}

/* ── 최종 요약 ── */
.summary-box{
  background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(99,102,241,0.1));
  border:2px solid #10b981;border-radius:12px;padding:16px;
  text-align:center;margin-top:16px;display:none
}
.summary-title{font-size:1.1rem;color:#86efac;font-weight:700;margin-bottom:8px}
.summary-text{color:#d1fae5;margin:8px 0;line-height:1.5}
.summary-icon{font-size:2rem;margin-bottom:8px}

@media(max-width:600px){
  body{padding:10px}
  .substitution-grid{grid-template-columns:1fr 1fr}
  h2{font-size:1.1rem}
  .formula-box{font-size:1rem}
}
</style>
</head>
<body>

<h2>🔍 항등식 탐정</h2>
<p class="subtitle">각 식에 여러 값을 대입하여 항등식과 방정식을 구분해보세요!</p>

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
  <div class="summary-text">항등식: <strong id="identitiesCount">0</strong>개 / 방정식: <strong id="equationsCount">0</strong>개</div>
  <div class="summary-text">항등식의 성질을 정리하여 아래 성찰 폼을 완성하세요 ✏️</div>
</div>

<script>
// ── 데이터베이스 ──────────────────────────────────────────────────────────
const PROBLEMS = [
  {
    id: 1,
    left: "x^2 - 3x",
    right: "x(x - 3)",
    type: "항등식",
    tests: [
      {x: 0, leftVal: 0, rightVal: 0},
      {x: 1, leftVal: -2, rightVal: -2},
      {x: 2, leftVal: -2, rightVal: -2},
      {x: -1, leftVal: 4, rightVal: 4}
    ]
  },
  {
    id: 2,
    left: "2x - 4",
    right: "0",
    type: "방정식",
    tests: [
      {x: 0, leftVal: -4, rightVal: 0},
      {x: 1, leftVal: -2, rightVal: 0},
      {x: 2, leftVal: 0, rightVal: 0},
      {x: 3, leftVal: 2, rightVal: 0}
    ]
  },
  {
    id: 3,
    left: "(a+b)^2",
    right: "a^2 + 2ab + b^2",
    variable: "multiple",
    type: "항등식",
    tests: [
      {a: 1, b: 1, leftVal: 4, rightVal: 4},
      {a: 2, b: 1, leftVal: 9, rightVal: 9},
      {a: -1, b: 2, leftVal: 1, rightVal: 1},
      {a: 3, b: -2, leftVal: 1, rightVal: 1}
    ]
  },
  {
    id: 4,
    left: "x^2",
    right: "16",
    type: "방정식",
    tests: [
      {x: 0, leftVal: 0, rightVal: 16},
      {x: 2, leftVal: 4, rightVal: 16},
      {x: 4, leftVal: 16, rightVal: 16},
      {x: -4, leftVal: 16, rightVal: 16}
    ]
  },
  {
    id: 5,
    left: "3(x+2)",
    right: "3x + 6",
    type: "항등식",
    tests: [
      {x: 0, leftVal: 6, rightVal: 6},
      {x: 1, leftVal: 9, rightVal: 9},
      {x: -2, leftVal: 0, rightVal: 0},
      {x: 5, leftVal: 21, rightVal: 21}
    ]
  },
  {
    id: 6,
    left: "x + 2",
    right: "3",
    type: "방정식",
    tests: [
      {x: 0, leftVal: 2, rightVal: 3},
      {x: 1, leftVal: 3, rightVal: 3},
      {x: 2, leftVal: 4, rightVal: 3},
      {x: 3, leftVal: 5, rightVal: 3}
    ]
  }
];

// ── 글로벌 상태 ──────────────────────────────────────────────────────────
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
  
  let subGrid = '';
  if(p.variable === 'multiple'){
    subGrid = p.tests.map((t,i) => `
      <div class="sub-item" onclick="checkSubstitution(${index}, ${i})">
        <div class="sub-label">$a=${t.a}, b=${t.b}$</div>
        <div class="sub-values">좌: ${t.leftVal} | 우: ${t.rightVal}</div>
      </div>
    `).join('');
  } else {
    subGrid = p.tests.map((t,i) => `
      <div class="sub-item" onclick="checkSubstitution(${index}, ${i})">
        <div class="sub-label">$x = ${t.x}$</div>
        <div class="sub-values">좌: ${t.leftVal} | 우: ${t.rightVal}</div>
      </div>
    `).join('');
  }

  const html = `
    <div class="card">
      <div class="problem-title">문제 ${index + 1} / 6</div>
      <div class="formula-box">
        $$${p.left} ${p.variable === 'multiple' ? '=' : '='} ${p.right}$$
      </div>
      <div style="color:#a78bfa;font-size:0.85rem;margin:8px 0">
        💡 다양한 값을 대입하여 이 식이 <strong>항등식</strong>인지 <strong>방정식</strong>인지 판별하세요
      </div>
      <div class="substitution-grid">${subGrid}</div>
      <div class="result-table" id="resultTable" style="display:none">
        <thead>
          <tr>
            <th>대입값</th>
            <th>좌변</th>
            <th>우변</th>
            <th>결과</th>
          </tr>
        </thead>
        <tbody id="resultBody"></tbody>
      </div>
      <div class="feedback" id="feedback"></div>
      <div style="margin-top:12px;padding:12px;background:rgba(255,255,255,0.05);border-radius:8px;text-align:center">
        <strong style="color:#e0e7ff">현재 판단:</strong> 
        <div style="margin-top:8px;display:flex;gap:8px;justify-content:center">
          <button class="btn" style="background:rgba(99,102,241,0.3);border:2px solid #818cf8;color:#a78bfa" 
            onclick="selectAnswer(${index}, '항등식')">
            항등식 ✔️
          </button>
          <button class="btn" style="background:rgba(239,68,68,0.3);border:2px solid #ef4444;color:#fca5a5" 
            onclick="selectAnswer(${index}, '방정식')">
            방정식 ❌
          </button>
        </div>
      </div>
    </div>
  `;

  container.innerHTML = html;
  updateProgress();
  renderMath();
}

function checkSubstitution(pIdx, tIdx){
  const p = PROBLEMS[pIdx];
  const t = p.tests[tIdx];
  const resultTable = document.getElementById('resultTable');
  
  if(!resultTable.style.display || resultTable.style.display === 'none'){
    resultTable.style.display = 'table';
    document.getElementById('resultBody').innerHTML = '';
  }

  const tbody = document.getElementById('resultBody');
  let varStr = '';
  if(p.variable === 'multiple'){
    varStr = `$a=${t.a}, b=${t.b}$`;
  } else {
    varStr = `$x = ${t.x}$`;
  }

  const match = t.leftVal === t.rightVal;
  const row = `
    <tr>
      <td>${varStr}</td>
      <td class="result-left">${t.leftVal}</td>
      <td class="result-right">${t.rightVal}</td>
      <td class="${match ? 'result-match' : 'result-nomatch'}">
        ${match ? '✓ 같음' : '✗ 다름'}
      </td>
    </tr>
  `;
  tbody.innerHTML += row;
  renderMath();
  
  const items = document.querySelectorAll('.sub-item');
  items[tIdx].classList.add('checked');
}

function selectAnswer(pIdx, answer){
  const p = PROBLEMS[pIdx];
  const feedback = document.getElementById('feedback');
  const isCorrect = (answer === p.type);

  if(isCorrect){
    feedback.className = 'feedback success';
    feedback.innerHTML = `✅ 정답! 이것은 <strong>${p.type}</strong>입니다.`;
    score++;
    answers[pIdx] = true;
  } else {
    feedback.className = 'feedback error';
    feedback.innerHTML = `❌ 틀렸습니다. 정답은 <strong>${p.type}</strong>입니다.`;
    answers[pIdx] = false;
  }

  updateProgress();

  setTimeout(() => {
    currentProblemIndex++;
    renderProblem(currentProblemIndex);
  }, 1500);
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
  
  const identities = Object.values(answers).filter(v => v).length;
  const equations = Object.values(answers).filter(v => !v).length;

  document.getElementById('identitiesCount').textContent = 
    PROBLEMS.filter(p => p.type === '항등식' && answers[PROBLEMS.indexOf(p)]).length;
  document.getElementById('equationsCount').textContent = 
    PROBLEMS.filter(p => p.type === '방정식' && answers[PROBLEMS.indexOf(p)]).length;
  document.getElementById('summaryBox').style.display = 'block';
}

// 초기 실행
renderProblem(0);
</script>

</body>
</html>
"""


def render():
    st.set_page_config(page_title="항등식의 성질 - 항등식 탐정 게임", layout="wide")
    
    st.markdown("""
    <style>
    .main { max-width: 100%; }
    iframe { width: 100% !important; height: 800px !important; }
    </style>
    """, unsafe_allow_html=True)
    
    components.html(_GAME_HTML, height=850, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
