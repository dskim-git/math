"""
원 위의 점으로 만든 도형 개수 — 파스칼의 삼각형 발견
점의 개수에 따라 선분, 삼각형, 사각형, 오각형의 개수를 조사하면 파스칼의 삼각형이 나타난다.
"""
import streamlit as st
import streamlit.components.v1 as components

from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "원위도형개수탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이 활동을 통해 발견한 파스칼의 삼각형의 패턴을 설명해 보세요**"},
    {
        "key": "발견한패턴",
        "label": "원 위의 점 개수에 따라 만들어지는 도형 개수와 파스칼의 삼각형의 관계는?",
        "type": "text_area",
        "height": 100,
    },
    {
        "key": "이항계수연결",
        "label": "점 n개일 때 r개를 선택해 만든 도형의 개수가 C(n,r)인 이유를 설명하세요",
        "type": "text_area",
        "height": 100,
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 새롭게 알게 된 점",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 느낀 점",
        "type": "text_area",
        "height": 90,
    },
]

META = {
    "title": "🔵 원 위의 점으로 만든 도형으로 파스칼의 삼각형 발견",
    "description": "원 위의 등간격 점들로 만든 선분, 삼각형, 사각형, 오각형의 개수를 표로 정리하면 파스칼의 삼각형이 나타난다는 것을 직접 탐구합니다.",
    "order": 63,
}

_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>원 위의 점으로 만든 도형</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  color: #f1f5f9;
  padding: 16px;
  min-height: 100vh;
}

.shell { max-width: 1200px; margin: 0 auto; }

.hero {
  background: linear-gradient(135deg, rgba(30,27,75,0.8), rgba(15,23,42,0.9));
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: 18px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.hero h1 { font-size: 2rem; margin-bottom: 8px; color: #fbbf24; }
.hero p { font-size: 0.95rem; color: #cbd5e1; line-height: 1.6; max-width: 800px; }

.topbar {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 14px;
}
.panel {
  background: rgba(30,41,59,0.8);
  border: 1px solid rgba(148,163,184,0.2);
  border-radius: 14px;
  padding: 14px;
}
.panel-title { font-size: 0.86rem; font-weight: 800; color: #a0f472; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; }
.panel-text { font-size: 0.84rem; line-height: 1.6; color: #cbd5e1; }

.controls {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(30,41,59,0.6);
  border-radius: 12px;
}
.control-label { font-size: 0.88rem; font-weight: 700; color: #f1f5f9; }
.slider-wrapper { display: flex; align-items: center; gap: 8px; }
input[type="range"] {
  width: 140px;
  height: 5px;
  border-radius: 3px;
  background: linear-gradient(to right, #6f46e6 0%, #3b82f6 100%);
  outline: none;
  cursor: pointer;
}
input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fbbf24;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(251,191,36,0.5);
}
input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fbbf24;
  cursor: pointer;
  border: none;
  box-shadow: 0 0 10px rgba(251,191,36,0.5);
}
.point-count { font-size: 1.1rem; font-weight: 900; color: #fbbf24; min-width: 30px; text-align: right; }

.canvas-container {
  background: rgba(15,23,42,0.8);
  border: 2px solid rgba(99,102,241,0.3);
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 320px;
}
#canvas { max-width: 100%; height: auto; }

.shapes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}
.shape-card {
  background: rgba(30,41,59,0.7);
  border: 2px solid rgba(148,163,184,0.2);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}
.shape-card:hover {
  border-color: rgba(99,102,241,0.5);
  background: rgba(30,41,59,0.9);
  transform: translateY(-2px);
}
.shape-card.selected {
  background: linear-gradient(135deg, rgba(99,102,241,0.4), rgba(168,85,247,0.3));
  border-color: #a78bfa;
  box-shadow: 0 0 12px rgba(167,139,250,0.3);
}
.shape-icon { font-size: 1.8rem; margin-bottom: 4px; }
.shape-name { font-size: 0.85rem; font-weight: 700; color: #f1f5f9; margin-bottom: 4px; }
.shape-value-input {
  background: rgba(15,23,42,0.8);
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: 6px;
  color: #fbbf24;
  font-size: 0.9rem;
  font-weight: 800;
  padding: 4px 8px;
  width: 100%;
  text-align: center;
  transition: all 0.2s;
}
.shape-value-input:focus {
  outline: none;
  border-color: #a78bfa;
  box-shadow: 0 0 8px rgba(167,139,250,0.3);
}

.table-wrapper {
  background: rgba(30,41,59,0.8);
  border: 1px solid rgba(148,163,184,0.2);
  border-radius: 14px;
  padding: 14px;
  overflow-x: auto;
  margin-bottom: 16px;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
th {
  background: rgba(99,102,241,0.2);
  color: #fbbf24;
  padding: 8px;
  text-align: center;
  font-weight: 800;
  border-bottom: 2px solid rgba(99,102,241,0.4);
}
td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid rgba(148,163,184,0.15);
  color: #cbd5e1;
}
td.filled {
  background: rgba(34,197,94,0.15);
  color: #86efac;
  font-weight: 700;
}
td.partial { background: rgba(251,191,36,0.1); }

.result-box {
  background: linear-gradient(135deg, rgba(34,197,94,0.2), rgba(99,102,241,0.2));
  border: 2px solid rgba(34,197,94,0.4);
  border-radius: 14px;
  padding: 16px;
  text-align: center;
  display: none;
  margin-bottom: 16px;
}
.result-box.show {
  display: block;
  animation: slideUp 0.4s ease;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.result-title { font-size: 1.2rem; font-weight: 900; color: #86efac; margin-bottom: 8px; }
.result-text { font-size: 0.9rem; line-height: 1.6; color: #d1fae5; }

.button-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
button {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(59,130,246,0.3); }
.btn-secondary {
  background: rgba(99,102,241,0.2);
  color: #c7d2fe;
  border: 1px solid rgba(99,102,241,0.4);
}
.btn-secondary:hover { background: rgba(99,102,241,0.3); }

.hint-box {
  background: rgba(251,191,36,0.1);
  border: 1px solid rgba(251,191,36,0.3);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 0.82rem;
  color: #fcd34d;
  margin-bottom: 12px;
}

@media (max-width: 768px) {
  .topbar { grid-template-columns: 1fr; }
  .shapes-grid { grid-template-columns: repeat(2, 1fr); }
  .controls { flex-direction: column; align-items: flex-start; }
  .hero h1 { font-size: 1.5rem; }
}
</style>
</head>
<body>

<div class="shell">
  <div class="hero">
    <h1>🔵 원 위의 점으로 만든 도형</h1>
    <p>
      원 위에 등간격으로 배치된 점들을 이어서 만든 선분, 삼각형, 사각형, 오각형의 개수를 조사하세요.
      표를 완성하면 <strong>파스칼의 삼각형</strong>이 나타나는 마법을 경험하게 됩니다!
    </p>
  </div>

  <div class="topbar">
    <div class="panel">
      <div class="panel-title">📌 활동 규칙</div>
      <div class="panel-text">
        1️⃣ 원 위의 점 개수를 선택<br>
        2️⃣ 각 도형(선분, 삼각형, 사각형, 오각형)의 개수를 입력<br>
        3️⃣ 표를 완성하면 파스칼의 삼각형을 발견!
      </div>
    </div>
    <div class="panel">
      <div class="panel-title">💡 핵심 개념</div>
      <div class="panel-text">
        r개의 도형 = r개의 점을 선택하는 경우의 수 = C(n, r)<br>
        n개 중 r개를 선택하는 이항계수가 각 행에 나타남
      </div>
    </div>
  </div>

  <div class="hint-box">
    💡 <strong>팁:</strong> 원 위의 모든 점들을 직선으로 연결할 때, 몇 개를 선택하느냐에 따라 도형 개수가 결정됩니다. 
    예를 들어 선분은 2개, 삼각형은 3개, 사각형은 4개, 오각형은 5개를 선택할 때 만들어집니다.
  </div>

  <div class="controls">
    <div class="control-label">점의 개수:</div>
    <div class="slider-wrapper">
      <input type="range" id="pointSlider" min="1" max="8" value="3" step="1">
      <span class="point-count" id="pointCount">3</span>
      <span style="font-size: 0.82rem; color: #cbd5e1;">개</span>
    </div>
  </div>

  <div class="canvas-container">
    <canvas id="canvas" width="300" height="300"></canvas>
  </div>

  <div class="shapes-grid">
    <div class="shape-card" data-shape="점">
      <div class="shape-icon">⚪</div>
      <div class="shape-name">점</div>
      <div style="font-size: 0.75rem; color: #94a3b8;">C(n, 1)</div>
    </div>
    <div class="shape-card" data-shape="선분">
      <div class="shape-icon">─</div>
      <div class="shape-name">선분</div>
      <div style="font-size: 0.75rem; color: #94a3b8;">C(n, 2)</div>
    </div>
    <div class="shape-card" data-shape="삼각형">
      <div class="shape-icon">△</div>
      <div class="shape-name">삼각형</div>
      <div style="font-size: 0.75rem; color: #94a3b8;">C(n, 3)</div>
    </div>
    <div class="shape-card" data-shape="사각형">
      <div class="shape-icon">□</div>
      <div class="shape-name">사각형</div>
      <div style="font-size: 0.75rem; color: #94a3b8;">C(n, 4)</div>
    </div>
    <div class="shape-card" data-shape="오각형">
      <div class="shape-icon">⬠</div>
      <div class="shape-name">오각형</div>
      <div style="font-size: 0.75rem; color: #94a3b8;">C(n, 5)</div>
    </div>
  </div>

  <div class="button-group">
    <button class="btn-primary" onclick="fillInputs()">💾 정답 확인</button>
    <button class="btn-secondary" onclick="resetAll()">🔄 초기화</button>
  </div>

  <div class="result-box" id="resultBox">
    <div class="result-title">✅ 표 완성 완료!</div>
    <div class="result-text" id="resultText"></div>
  </div>

  <div class="table-wrapper">
    <table>
      <thead>
        <tr>
          <th colspan="6" style="background: linear-gradient(90deg, rgba(251,191,36,0.3), rgba(99,102,241,0.3)); padding: 12px; font-size: 0.95rem;">
            📊 파스칼의 삼각형과 원 위의 도형 개수
          </th>
        </tr>
        <tr>
          <th>n (점)</th>
          <th>⚪ (점)</th>
          <th>─ (선분)</th>
          <th>△ (삼각형)</th>
          <th>□ (사각형)</th>
          <th>⬠ (오각형)</th>
        </tr>
      </thead>
      <tbody id="tableBody"></tbody>
    </table>
  </div>

</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const pointSlider = document.getElementById('pointSlider');
const pointCount = document.getElementById('pointCount');
const shapeCards = document.querySelectorAll('.shape-card');
const tableBody = document.getElementById('tableBody');

const data = {
  1: { 점: 1, 선분: 0, 삼각형: 0, 사각형: 0, 오각형: 0 },
  2: { 점: 2, 선분: 1, 삼각형: 0, 사각형: 0, 오각형: 0 },
  3: { 점: 3, 선분: 3, 삼각형: 1, 사각형: 0, 오각형: 0 },
  4: { 점: 4, 선분: 6, 삼각형: 4, 사각형: 1, 오각형: 0 },
  5: { 점: 5, 선분: 10, 삼각형: 10, 사각형: 5, 오각형: 1 },
  6: { 점: 6, 선분: 15, 삼각형: 20, 사각형: 15, 오각형: 6 },
  7: { 점: 7, 선분: 21, 삼각형: 35, 사각형: 35, 오각형: 21 },
  8: { 점: 8, 선분: 28, 삼각형: 56, 사각형: 70, 오각형: 56 }
};

let userInputs = {};

function drawCircleWithPoints(n, indices = null) {
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = Math.min(canvas.width, canvas.height) / 2 - 30;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 원 그리기
  ctx.strokeStyle = 'rgba(99, 102, 241, 0.3)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
  ctx.stroke();

  // 점의 좌표 계산
  const angleStep = (2 * Math.PI) / n;
  const points = [];

  for (let i = 0; i < n; i++) {
    const angle = -Math.PI / 2 + i * angleStep;
    const x = centerX + radius * Math.cos(angle);
    const y = centerY + radius * Math.sin(angle);
    points.push({ x, y });
  }

  // 선택된 도형에 따라 시각화
  const selectedShape = document.querySelector('.shape-card.selected');
  const shapeName = selectedShape ? selectedShape.dataset.shape : null;

  if (shapeName === '점') {
    // 모든 점을 강조
    ctx.fillStyle = '#86efac';
    ctx.strokeStyle = '#86efac';
    ctx.lineWidth = 3;
    for (let i = 0; i < n; i++) {
      ctx.beginPath();
      ctx.arc(points[i].x, points[i].y, 8, 0, 2 * Math.PI);
      ctx.fill();
    }
  } else if (shapeName === '선분' && indices && indices.length === 2) {
    // 두 점을 이으면 선분
    ctx.strokeStyle = 'rgba(251, 191, 36, 0.8)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(points[indices[0]].x, points[indices[0]].y);
    ctx.lineTo(points[indices[1]].x, points[indices[1]].y);
    ctx.stroke();
  } else if (shapeName === '삼각형' && indices && indices.length === 3) {
    // 세 점을 이으면 삼각형
    ctx.strokeStyle = 'rgba(34, 197, 94, 0.8)';
    ctx.lineWidth = 2.5;
    ctx.fillStyle = 'rgba(34, 197, 94, 0.15)';
    ctx.beginPath();
    ctx.moveTo(points[indices[0]].x, points[indices[0]].y);
    ctx.lineTo(points[indices[1]].x, points[indices[1]].y);
    ctx.lineTo(points[indices[2]].x, points[indices[2]].y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  } else if (shapeName === '사각형' && indices && indices.length === 4) {
    // 네 점을 이으면 사각형
    ctx.strokeStyle = 'rgba(59, 130, 246, 0.8)';
    ctx.lineWidth = 2.5;
    ctx.fillStyle = 'rgba(59, 130, 246, 0.15)';
    ctx.beginPath();
    ctx.moveTo(points[indices[0]].x, points[indices[0]].y);
    ctx.lineTo(points[indices[1]].x, points[indices[1]].y);
    ctx.lineTo(points[indices[2]].x, points[indices[2]].y);
    ctx.lineTo(points[indices[3]].x, points[indices[3]].y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  } else if (shapeName === '오각형' && indices && indices.length === 5) {
    // 다섯 점을 이으면 오각형
    ctx.strokeStyle = 'rgba(168, 85, 247, 0.8)';
    ctx.lineWidth = 2.5;
    ctx.fillStyle = 'rgba(168, 85, 247, 0.15)';
    ctx.beginPath();
    ctx.moveTo(points[indices[0]].x, points[indices[0]].y);
    ctx.lineTo(points[indices[1]].x, points[indices[1]].y);
    ctx.lineTo(points[indices[2]].x, points[indices[2]].y);
    ctx.lineTo(points[indices[3]].x, points[indices[3]].y);
    ctx.lineTo(points[indices[4]].x, points[indices[4]].y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  }

  // 선택된 점들을 강조
  if (indices && indices.length > 0) {
    ctx.fillStyle = '#fbbf24';
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 2.5;
    for (let idx of indices) {
      ctx.beginPath();
      ctx.arc(points[idx].x, points[idx].y, 7, 0, 2 * Math.PI);
      ctx.fill();
    }
  }

  // 모든 점을 그리기 (항상 표시)
  ctx.fillStyle = '#fbbf24';
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 2;

  for (let i = 0; i < n; i++) {
    ctx.beginPath();
    ctx.arc(points[i].x, points[i].y, 6, 0, 2 * Math.PI);
    ctx.fill();
  }

  // 점 번호 표시
  ctx.fillStyle = 'rgba(251, 191, 36, 0.9)';
  ctx.font = 'bold 12px sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let i = 0; i < n; i++) {
    ctx.fillText(i + 1, points[i].x, points[i].y);
  }
}

function combinations(arr, r) {
  if (r === 1) return arr.map(x => [x]);
  const combs = [];
  for (let i = 0; i < arr.length - r + 1; i++) {
    const head = arr[i];
    const tail = combinations(arr.slice(i + 1), r - 1);
    for (let t of tail) {
      combs.push([head, ...t]);
    }
  }
  return combs;
}

function randomCombination(n, r) {
  const indices = Array.from({length: n}, (_, i) => i);
  const allCombs = combinations(indices, r);
  if (allCombs.length === 0) return null;
  return allCombs[Math.floor(Math.random() * allCombs.length)];
}

function updateTable() {
  tableBody.innerHTML = '';
  for (let n = 1; n <= 8; n++) {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td style="font-weight: 700; color: #fbbf24;">n = ${n}</td>
      <td class="${userInputs[n]?.점 !== undefined ? 'filled' : ''}">
        <input type="number" class="shape-value-input" 
               placeholder="?" data-n="${n}" data-shape="점" 
               value="${userInputs[n]?.점 !== undefined ? userInputs[n].점 : ''}"
               onchange="updateInput(this)">
      </td>
      <td class="${userInputs[n]?.선분 !== undefined ? 'filled' : ''}">
        <input type="number" class="shape-value-input" 
               placeholder="?" data-n="${n}" data-shape="선분"
               value="${userInputs[n]?.선분 !== undefined ? userInputs[n].선분 : ''}"
               onchange="updateInput(this)">
      </td>
      <td class="${userInputs[n]?.삼각형 !== undefined ? 'filled' : ''}">
        <input type="number" class="shape-value-input" 
               placeholder="?" data-n="${n}" data-shape="삼각형"
               value="${userInputs[n]?.삼각형 !== undefined ? userInputs[n].삼각형 : ''}"
               onchange="updateInput(this)">
      </td>
      <td class="${userInputs[n]?.사각형 !== undefined ? 'filled' : ''}">
        <input type="number" class="shape-value-input" 
               placeholder="?" data-n="${n}" data-shape="사각형"
               value="${userInputs[n]?.사각형 !== undefined ? userInputs[n].사각형 : ''}"
               onchange="updateInput(this)">
      </td>
      <td class="${userInputs[n]?.오각형 !== undefined ? 'filled' : ''}">
        <input type="number" class="shape-value-input" 
               placeholder="?" data-n="${n}" data-shape="오각형"
               value="${userInputs[n]?.오각형 !== undefined ? userInputs[n].오각형 : ''}"
               onchange="updateInput(this)">
      </td>
    `;
    tableBody.appendChild(row);
  }
}

function updateInput(input) {
  const n = parseInt(input.dataset.n);
  const shape = input.dataset.shape;
  const value = input.value;

  if (!userInputs[n]) userInputs[n] = {};
  userInputs[n][shape] = value ? parseInt(value) : undefined;

  if (value && parseInt(value) === data[n][shape]) {
    input.parentElement.classList.add('filled');
  } else {
    input.parentElement.classList.remove('filled');
  }

  checkCompletion();
}

function fillInputs() {
  for (let n = 1; n <= 8; n++) {
    if (!userInputs[n]) userInputs[n] = {};
    for (let shape of ['점', '선분', '삼각형', '사각형', '오각형']) {
      userInputs[n][shape] = data[n][shape];
    }
  }
  updateTable();
  checkCompletion();
}

function resetAll() {
  userInputs = {};
  updateTable();
  document.getElementById('resultBox').classList.remove('show');
}

function checkCompletion() {
  let allCorrect = true;
  for (let n = 1; n <= 8; n++) {
    for (let shape of ['점', '선분', '삼각형', '사각형', '오각형']) {
      if (!userInputs[n] || userInputs[n][shape] !== data[n][shape]) {
        allCorrect = false;
      }
    }
  }

  if (allCorrect) {
    const resultBox = document.getElementById('resultBox');
    resultBox.classList.add('show');
    document.getElementById('resultText').innerHTML = `
      🎉 <strong>파스칼의 삼각형을 발견했습니다!</strong><br><br>
      각 행의 수들이 파스칼의 삼각형의 이항계수와 일치합니다.<br>
      이는 <strong>n개의 점 중 r개를 선택해 만든 도형의 개수 = C(n, r)</strong>이기 때문입니다!
    `;
  } else {
    document.getElementById('resultBox').classList.remove('show');
  }
}

pointSlider.addEventListener('input', (e) => {
  const n = parseInt(e.target.value);
  pointCount.textContent = n;
  
  // 선택된 도형이 있으면 그에 맞게 갱신
  const selectedShape = document.querySelector('.shape-card.selected');
  if (selectedShape) {
    const shapeName = selectedShape.dataset.shape;
    let indices = null;
    
    if (shapeName === '점') {
      indices = Array.from({length: n}, (_, i) => i);
    } else if (shapeName === '선분' && n >= 2) {
      indices = randomCombination(n, 2);
    } else if (shapeName === '삼각형' && n >= 3) {
      indices = randomCombination(n, 3);
    } else if (shapeName === '사각형' && n >= 4) {
      indices = randomCombination(n, 4);
    } else if (shapeName === '오각형' && n >= 5) {
      indices = randomCombination(n, 5);
    }
    
    drawCircleWithPoints(n, indices);
  } else {
    drawCircleWithPoints(n);
  }
});

shapeCards.forEach(card => {
  card.addEventListener('click', () => {
    // 다른 카드의 selected 제거
    shapeCards.forEach(c => c.classList.remove('selected'));
    // 클릭한 카드에만 selected 추가
    card.classList.add('selected');
    
    // 도형에 맞는 랜덤 인덱스 생성
    const n = parseInt(pointSlider.value);
    const shapeName = card.dataset.shape;
    let indices = null;
    
    if (shapeName === '점') {
      indices = Array.from({length: n}, (_, i) => i); // 모든 점
    } else if (shapeName === '선분' && n >= 2) {
      indices = randomCombination(n, 2);
    } else if (shapeName === '삼각형' && n >= 3) {
      indices = randomCombination(n, 3);
    } else if (shapeName === '사각형' && n >= 4) {
      indices = randomCombination(n, 4);
    } else if (shapeName === '오각형' && n >= 5) {
      indices = randomCombination(n, 5);
    }
    
    // 캔버스 다시 그리기
    drawCircleWithPoints(n, indices);
  });
});

drawCircleWithPoints(3);
updateTable();
</script>

</body>
</html>
"""


def render():
    st.set_page_config(page_title="원 위의 점으로 만든 도형", layout="wide")

    st.markdown(
        """
        <style>
        .main { max-width: 100%; }
        iframe { width: 100% !important; height: 1850px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(_HTML, height=1850, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
