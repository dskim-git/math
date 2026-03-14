import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 에라토스테네스의 체와 소수정리",
    "description": "직접 조작하며 소수를 걸러내는 에라토스테네스의 체를 체험합니다.",
    "order": 11,
    "hidden": True,
}

HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Noto Sans KR', sans-serif; background: #f8fafc; color: #1e293b; }

  #app { max-width: 900px; margin: 0 auto; padding: 12px; }

  h2 { font-size: 1.25rem; font-weight: 700; margin-bottom: 6px; }

  /* ── 컨트롤 바 ── */
  .ctrl-bar {
    display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
    background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 10px 14px; margin-bottom: 10px;
  }
  .ctrl-bar label { font-size: 0.85rem; font-weight: 600; }
  select, input[type=number] {
    padding: 5px 8px; border-radius: 8px; border: 1px solid #cbd5e1;
    font-size: 0.85rem; background: #f8fafc;
  }
  button {
    padding: 6px 14px; border-radius: 8px; border: none;
    font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all .15s;
  }
  button:active { transform: translateY(1px); }
  .btn-step  { background: #3b82f6; color: #fff; }
  .btn-step:hover { background: #2563eb; }
  .btn-step:disabled { background: #93c5fd; cursor: not-allowed; }
  .btn-auto  { background: #10b981; color: #fff; }
  .btn-auto:hover { background: #059669; }
  .btn-auto.running { background: #f59e0b; }
  .btn-reset { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
  .btn-reset:hover { background: #fecaca; }
  .btn-mark  { background: #a78bfa; color: #fff; }
  .btn-mark:disabled { background: #c4b5fd; cursor: not-allowed; }

  /* ── 상태 배너 ── */
  .status-bar {
    background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px;
    padding: 8px 14px; margin-bottom: 10px;
    font-size: 0.88rem; display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
  }
  .status-bar .tag { font-weight: 700; }
  .status-bar .prime-tag { color: #1d4ed8; }
  .status-bar .step-tag  { color: #7c3aed; }
  .status-bar .count-tag { color: #065f46; }
  .hint-msg { font-size: 0.82rem; color: #475569; margin-top: 4px; }

  /* ── 진행 바 ── */
  .prog-wrap { background: #e2e8f0; border-radius: 999px; height: 6px; margin-bottom: 10px; overflow: hidden; }
  .prog-bar  { height: 6px; border-radius: 999px; background: #3b82f6; transition: width .3s; }

  /* ── 격자 ── */
  #grid-wrap {
    background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 10px; overflow-x: auto;
  }
  #grid {
    display: grid;
    gap: 3px;
  }
  .cell {
    width: 100%; aspect-ratio: 1;
    display: flex; align-items: center; justify-content: center;
    border-radius: 6px; font-size: 0.72rem; font-weight: 600;
    cursor: pointer; border: 1.5px solid transparent;
    transition: background .2s, transform .1s, border-color .2s;
    user-select: none;
  }
  .cell:hover { transform: scale(1.12); z-index: 2; position: relative; }
  .cell.normal  { background: #f1f5f9; color: #475569; border-color: #e2e8f0; }
  .cell.sieved  { background: #f8d7da; color: #aaa; border-color: #f5c6cb; text-decoration: line-through; }
  .cell.prime   { background: #dbeafe; color: #1e40af; border-color: #93c5fd; }
  .cell.current { background: #fef3c7; color: #92400e; border-color: #fbbf24; animation: pulse .5s infinite alternate; }
  .cell.twin1   { background: #d1fae5; color: #065f46; border-color: #6ee7b7; }
  .cell.twin2   { background: #d1fae5; color: #065f46; border-color: #6ee7b7; }
  .cell.highlight { background: #fde68a; border-color: #f59e0b; color: #78350f; animation: flash .25s; }

  @keyframes pulse { from { box-shadow: 0 0 0 0 #fbbf24; } to { box-shadow: 0 0 0 6px rgba(251,191,36,0); } }
  @keyframes flash { 0%{background:#fbbf24;} 100%{background:#dbeafe;} }

  /* ── 소수 목록 ── */
  #prime-list-wrap {
    margin-top: 10px; background: #fff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 10px 14px;
  }
  #prime-list-wrap h3 { font-size: 0.9rem; font-weight: 700; margin-bottom: 6px; }
  #prime-list { display: flex; flex-wrap: wrap; gap: 4px; min-height: 24px; }
  .p-badge {
    padding: 2px 8px; border-radius: 999px;
    background: #dbeafe; border: 1px solid #93c5fd;
    color: #1e40af; font-size: 0.78rem; font-weight: 700;
    animation: popIn .2s;
  }
  .p-badge.twin { background: #d1fae5; border-color: #6ee7b7; color: #065f46; }
  @keyframes popIn { from { transform: scale(0.6); opacity: 0; } to { transform: scale(1); opacity: 1; } }

  /* ── 재미있는 사실 ── */
  #fact-box {
    margin-top: 10px; padding: 10px 14px;
    background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px;
    font-size: 0.85rem; color: #166534; display: none;
  }
  #fact-box strong { font-weight: 700; }

  /* ── 모드 탭 ── */
  .tab-row { display: flex; gap: 6px; margin-bottom: 10px; }
  .tab-btn {
    padding: 6px 14px; border-radius: 8px; border: 1.5px solid #e2e8f0;
    background: #f8fafc; font-size: 0.82rem; font-weight: 600; cursor: pointer;
    color: #64748b;
  }
  .tab-btn.active { background: #3b82f6; color: #fff; border-color: #3b82f6; }
</style>
</head>
<body>
<div id="app">
  <h2>🔢 에라토스테네스의 체</h2>
  <p class="hint-msg" style="margin-bottom:8px;">
    소수를 직접 골라내 보세요! 숫자를 클릭하거나, <b>단계별 진행</b>으로 체험합니다.
  </p>

  <!-- 탭 -->
  <div class="tab-row">
    <button class="tab-btn active" id="tab-sieve" onclick="switchTab('sieve')">🧮 체 조작</button>
    <button class="tab-btn" id="tab-twin"  onclick="switchTab('twin')">👯 쌍둥이 소수</button>
    <button class="tab-btn" id="tab-density" onclick="switchTab('density')">📊 소수 밀도</button>
  </div>

  <!-- 체 조작 탭 -->
  <div id="pane-sieve">
    <div class="ctrl-bar">
      <label>범위</label>
      <select id="rangeSelect" onchange="init()">
        <option value="50">2 ~ 50</option>
        <option value="100" selected>2 ~ 100</option>
        <option value="200">2 ~ 200</option>
      </select>
      <label>열 수</label>
      <select id="colSelect" onchange="buildGrid()">
        <option value="10" selected>10</option>
        <option value="5">5</option>
        <option value="20">20</option>
      </select>
      <button class="btn-step" id="btnStep" onclick="step()">▶ 다음 단계</button>
      <button class="btn-auto" id="btnAuto" onclick="toggleAuto()">⚡ 자동 진행</button>
      <button class="btn-mark" id="btnMark" onclick="markCurrent()" title="현재 소수의 배수를 한 번에 표시">🗑 배수 지우기</button>
      <button class="btn-reset" onclick="init()">↺ 초기화</button>
    </div>

    <div class="status-bar">
      <span>현재 소수: <span class="tag prime-tag" id="curPrime">-</span></span>
      <span>단계: <span class="tag step-tag" id="curStep">0</span></span>
      <span>발견된 소수: <span class="tag count-tag" id="primeCount">0</span>개</span>
      <span id="doneMsg" style="display:none;color:#059669;font-weight:700;">✅ 완료! 모든 소수를 찾았습니다.</span>
    </div>

    <div class="prog-wrap"><div class="prog-bar" id="progBar" style="width:0%"></div></div>

    <div id="grid-wrap"><div id="grid"></div></div>

    <div id="prime-list-wrap">
      <h3>🎯 발견된 소수 목록 <span style="font-weight:400;color:#64748b;font-size:0.8rem">(쌍둥이 소수는 초록색)</span></h3>
      <div id="prime-list"></div>
    </div>

    <div id="fact-box"></div>
  </div>

  <!-- 쌍둥이 소수 탭 -->
  <div id="pane-twin" style="display:none;">
    <div class="ctrl-bar">
      <label>범위</label>
      <select id="twinRange" onchange="renderTwinTab()">
        <option value="100">~ 100</option>
        <option value="500" selected>~ 500</option>
        <option value="1000">~ 1000</option>
      </select>
    </div>
    <div id="twin-content" style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:14px;">
      <p style="color:#64748b;font-size:0.85rem;">탭을 클릭하면 로딩됩니다.</p>
    </div>
  </div>

  <!-- 소수 밀도 / 소수 정리 탭 -->
  <div id="pane-density" style="display:none;">

    <!-- ① π(N) vs N/lnN 비교표 -->
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:14px;margin-bottom:10px;">
      <div style="font-size:1rem;font-weight:700;margin-bottom:6px;">
        📋 소수 정리: π(N) ≈ N / ln N
      </div>
      <p style="font-size:0.83rem;color:#475569;margin-bottom:10px;">
        N이 커질수록 <b>N/π(N)</b>은 <b>ln N</b>에 가까워집니다.
        아래 표에서 직접 확인해 보세요!
      </p>
      <div style="overflow-x:auto;">
        <table id="pntTable" style="width:100%;border-collapse:collapse;font-size:0.85rem;">
          <thead>
            <tr style="background:#7c3aed;color:#fff;">
              <th style="padding:8px 12px;text-align:right;">N</th>
              <th style="padding:8px 12px;text-align:right;">ln N</th>
              <th style="padding:8px 12px;text-align:right;">π(N) <span style="font-weight:400;font-size:0.78rem;">(실제 소수 개수)</span></th>
              <th style="padding:8px 12px;text-align:right;">N / π(N)</th>
              <th style="padding:8px 12px;text-align:right;">차이(%)</th>
            </tr>
          </thead>
          <tbody id="pntBody"></tbody>
        </table>
      </div>
      <p style="font-size:0.78rem;color:#94a3b8;margin-top:6px;">* N이 클수록 차이(%)가 0에 가까워져요. (큰 N은 근삿값 사용)</p>
    </div>

    <!-- ② 직접 입력해서 확인하기 -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;">

      <!-- 소수일 확률 -->
      <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:14px;">
        <div style="font-size:0.95rem;font-weight:700;margin-bottom:6px;">🎲 정수 N이 소수일 확률 ≈ 1/ln N</div>
        <p style="font-size:0.82rem;color:#475569;margin-bottom:8px;">
          N 근처의 수 중에서 소수가 얼마나 촘촘히 있는지 나타냅니다.
        </p>
        <div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;">
          <input id="probN" type="number" value="1000" min="10" style="width:110px;">
          <button class="btn-step" onclick="calcProb()">계산</button>
        </div>
        <div id="probResult" style="font-size:0.88rem;line-height:1.8;"></div>
      </div>

      <!-- N번째 소수 -->
      <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:14px;">
        <div style="font-size:0.95rem;font-weight:700;margin-bottom:6px;">🔢 N번째 소수 ≈ N · ln N</div>
        <p style="font-size:0.82rem;color:#475569;margin-bottom:8px;">
          N번째 소수의 크기는 N · ln N 에 가까워집니다.
        </p>
        <div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;">
          <input id="nthN" type="number" value="100" min="1" max="10000" style="width:110px;">
          <button class="btn-step" onclick="calcNth()">계산</button>
        </div>
        <div id="nthResult" style="font-size:0.88rem;line-height:1.8;"></div>
      </div>
    </div>

    <!-- ③ π(x) vs x/lnx 그래프 -->
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:14px;">
      <div style="font-size:0.95rem;font-weight:700;margin-bottom:6px;">📈 π(x) vs x / ln x 그래프</div>
      <div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;">
        <label style="font-size:0.85rem;font-weight:600;">범위</label>
        <select id="graphRange" onchange="renderDensityTab()">
          <option value="500">~ 500</option>
          <option value="1000" selected>~ 1,000</option>
          <option value="5000">~ 5,000</option>
        </select>
        <span style="font-size:0.8rem;color:#64748b;">— 파란선: 실제 π(x)&nbsp;&nbsp;주황점선: 근사 x/ln x</span>
      </div>
      <canvas id="densityCanvas" width="840" height="300" style="max-width:100%;border-radius:8px;display:block;"></canvas>
      <!-- 마우스 오버 정보 -->
      <div id="graphInfo" style="font-size:0.82rem;color:#475569;margin-top:6px;min-height:18px;"></div>
    </div>

  </div>
</div>

<script>
// ── 전역 상태 ──────────────────────────────────────────────
let N = 100;
let sieved = [];    // true = 지워짐(합성수)
let confirmed = []; // true = 소수 확정
let primes = [];
let curP = 2;       // 현재 처리 중인 소수
let done = false;
let autoTimer = null;
let autoRunning = false;
let currentTab = 'sieve';

// ── 초기화 ────────────────────────────────────────────────
function init() {
  N = +document.getElementById('rangeSelect').value;
  sieved    = new Array(N + 1).fill(false);
  confirmed = new Array(N + 1).fill(false);
  primes = [];
  curP = 2;
  done = false;
  sieved[0] = sieved[1] = true;

  stopAuto();
  document.getElementById('doneMsg').style.display = 'none';
  document.getElementById('btnStep').disabled = false;
  document.getElementById('btnMark').disabled = false;
  document.getElementById('btnAuto').textContent = '⚡ 자동 진행';
  document.getElementById('btnAuto').classList.remove('running');
  document.getElementById('fact-box').style.display = 'none';
  document.getElementById('prime-list').innerHTML = '';
  updateStatus();
  buildGrid();
}

// ── 격자 생성 ────────────────────────────────────────────
function buildGrid() {
  const cols = +document.getElementById('colSelect').value;
  const grid = document.getElementById('grid');
  grid.style.gridTemplateColumns = `repeat(${cols}, minmax(28px, 1fr))`;
  grid.innerHTML = '';
  for (let n = 2; n <= N; n++) {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.id = 'c' + n;
    cell.textContent = n;
    cell.onclick = () => toggleCell(n);
    grid.appendChild(cell);
  }
  refreshGrid();
}

function refreshGrid() {
  for (let n = 2; n <= N; n++) {
    const cell = document.getElementById('c' + n);
    if (!cell) continue;
    cell.className = 'cell ' + getCellClass(n);
  }
  updateProgress();
}

function getCellClass(n) {
  if (!done && n === curP && !sieved[n] && !confirmed[n]) return 'current';
  if (confirmed[n]) return 'prime';
  if (sieved[n]) return 'sieved';
  return 'normal';
}

// ── 사용자 수동 클릭 ──────────────────────────────────────
function toggleCell(n) {
  if (done) return;
  if (n === curP) return; // 현재 소수는 클릭 안 됨
  if (confirmed[n]) return;
  sieved[n] = !sieved[n];
  refreshGrid();
}

// ── 단계 진행 ─────────────────────────────────────────────
function step() {
  if (done) return;

  // curP 소수 확정
  confirmed[curP] = true;
  sieved[curP] = false;
  primes.push(curP);
  addPrimeBadge(curP);
  updateStatus();

  // 배수 지우기 (애니메이션)
  animateMultiples(curP, () => {
    // 다음 소수 찾기
    advanceCurP();
    refreshGrid();
    showFact();
  });
}

function animateMultiples(p, callback) {
  const multiples = [];
  for (let k = p * p; k <= N; k += p) {
    if (!sieved[k] && !confirmed[k]) multiples.push(k);
    sieved[k] = true;
  }
  // 순차 하이라이트
  let i = 0;
  function next() {
    if (i < multiples.length) {
      const cell = document.getElementById('c' + multiples[i]);
      if (cell) { cell.classList.add('highlight'); }
      i++;
      setTimeout(next, autoRunning ? 30 : 60);
    } else {
      refreshGrid();
      if (callback) callback();
    }
  }
  next();
}

function markCurrent() {
  if (done) return;
  step();
}

function advanceCurP() {
  let next = curP + 1;
  while (next <= N && sieved[next]) next++;
  if (next * next > N) {
    // 나머지 모두 소수 확정
    for (let n = next; n <= N; n++) {
      if (!sieved[n] && !confirmed[n]) {
        confirmed[n] = true;
        primes.push(n);
        addPrimeBadge(n);
      }
    }
    done = true;
    stopAuto();
    document.getElementById('doneMsg').style.display = '';
    document.getElementById('btnStep').disabled = true;
    document.getElementById('btnMark').disabled = true;
    document.getElementById('btnAuto').disabled = true;
    updateStatus();
    refreshGrid();
    markTwinPrimes();
    showFinalFact();
    return;
  }
  curP = next;
}

// ── 자동 진행 ─────────────────────────────────────────────
function toggleAuto() {
  if (done) return;
  if (autoRunning) {
    stopAuto();
  } else {
    autoRunning = true;
    document.getElementById('btnAuto').textContent = '⏸ 일시정지';
    document.getElementById('btnAuto').classList.add('running');
    runAuto();
  }
}

function runAuto() {
  if (!autoRunning || done) { stopAuto(); return; }
  step();
  autoTimer = setTimeout(runAuto, 800);
}

function stopAuto() {
  autoRunning = false;
  clearTimeout(autoTimer);
  const btn = document.getElementById('btnAuto');
  btn.textContent = '⚡ 자동 진행';
  btn.classList.remove('running');
}

// ── 상태 업데이트 ─────────────────────────────────────────
function updateStatus() {
  document.getElementById('curPrime').textContent = done ? '-' : curP;
  document.getElementById('curStep').textContent  = primes.length;
  document.getElementById('primeCount').textContent = primes.length;
}

function updateProgress() {
  const composites = sieved.filter(Boolean).length;
  const pct = Math.round((composites / (N - 1)) * 100);
  document.getElementById('progBar').style.width = pct + '%';
}

// ── 소수 배지 ─────────────────────────────────────────────
function addPrimeBadge(p) {
  const list = document.getElementById('prime-list');
  const b = document.createElement('span');
  b.className = 'p-badge';
  b.id = 'badge' + p;
  b.textContent = p;
  list.appendChild(b);
}

function markTwinPrimes() {
  for (let i = 0; i < primes.length - 1; i++) {
    if (primes[i + 1] - primes[i] === 2) {
      const b1 = document.getElementById('badge' + primes[i]);
      const b2 = document.getElementById('badge' + primes[i + 1]);
      if (b1) b1.classList.add('twin');
      if (b2) b2.classList.add('twin');
    }
  }
}

// ── 재미있는 사실 ─────────────────────────────────────────
const FACTS = [
  `<strong>에라토스테네스</strong>는 기원전 276년경 그리스의 수학자로, 지구 둘레도 최초로 계산했어요! 🌍`,
  `소수는 <strong>2, 3, 5, 7, 11, 13…</strong> — 2를 제외하면 모두 홀수입니다.`,
  `<strong>골드바흐의 추측</strong>: 2보다 큰 모든 짝수는 두 소수의 합이다. (아직 미증명!)`,
  `<strong>메르센 소수</strong>: 2ⁿ-1 형태의 소수. 현재 가장 큰 소수도 메르센 형태!`,
  `소수의 역수 합 <strong>1/2 + 1/3 + 1/5 + 1/7 + …</strong> 은 무한대로 발산합니다.`,
  `100 이하 소수는 <strong>25개</strong>, 1000 이하는 168개, 10000 이하는 1229개!`,
];
let factIdx = 0;

function showFact() {
  const box = document.getElementById('fact-box');
  box.innerHTML = '💡 ' + FACTS[factIdx % FACTS.length];
  box.style.display = 'block';
  factIdx++;
}

function showFinalFact() {
  const cnt = primes.length;
  const twinCount = countTwins();
  const box = document.getElementById('fact-box');
  box.innerHTML = `
    🎉 <strong>${N} 이하 소수: ${cnt}개</strong> (비율: ${(cnt/(N-1)*100).toFixed(1)}%)<br>
    👯 쌍둥이 소수 쌍: <strong>${twinCount}쌍</strong><br>
    가장 큰 소수: <strong>${primes[primes.length-1]}</strong><br>
    <span style="color:#166534;">소수 정리: π(N) ≈ N / ln(N) = ${Math.round(N / Math.log(N))} (이론값)</span>
  `;
  box.style.display = 'block';
}

function countTwins() {
  let c = 0;
  for (let i = 0; i < primes.length - 1; i++) {
    if (primes[i+1] - primes[i] === 2) c++;
  }
  return c;
}

// ── 탭 전환 ───────────────────────────────────────────────
function switchTab(tab) {
  currentTab = tab;
  ['sieve','twin','density'].forEach(t => {
    document.getElementById('pane-' + t).style.display = t === tab ? '' : 'none';
    document.getElementById('tab-' + t).classList.toggle('active', t === tab);
  });
  if (tab === 'twin') renderTwinTab();
  if (tab === 'density') renderDensityTab();
}

// ── 쌍둥이 소수 탭 ────────────────────────────────────────
function getPrimesUpTo(max) {
  const s = new Array(max + 1).fill(false);
  s[0] = s[1] = true;
  for (let p = 2; p * p <= max; p++) {
    if (!s[p]) for (let k = p*p; k <= max; k += p) s[k] = true;
  }
  const ps = [];
  for (let n = 2; n <= max; n++) if (!s[n]) ps.push(n);
  return ps;
}

function renderTwinTab() {
  const max = +document.getElementById('twinRange').value;
  const ps = getPrimesUpTo(max);
  const twins = [];
  for (let i = 0; i < ps.length - 1; i++) {
    if (ps[i+1] - ps[i] === 2) twins.push([ps[i], ps[i+1]]);
  }
  const div = document.getElementById('twin-content');
  div.innerHTML = `
    <p style="font-size:0.88rem;color:#475569;margin-bottom:10px;">
      <strong>쌍둥이 소수</strong>: 차이가 2인 소수 쌍 (예: (3,5), (11,13), (17,19)…)<br>
      무한히 많은지 여부는 아직 미해결 문제입니다! 🤔
    </p>
    <p style="margin-bottom:8px;font-weight:700;">
      ${max} 이하 쌍둥이 소수: <span style="color:#059669;">${twins.length}쌍</span>
    </p>
    <div style="display:flex;flex-wrap:wrap;gap:6px;">
      ${twins.map(([a,b]) => `<span style="padding:4px 10px;background:#d1fae5;border:1px solid #6ee7b7;border-radius:999px;font-size:0.8rem;color:#065f46;font-weight:700;">(${a}, ${b})</span>`).join('')}
    </div>
    <hr style="margin:14px 0;border-color:#e2e8f0;">
    <p style="font-size:0.82rem;color:#64748b;">
      📌 <strong>쌍둥이 소수 추측</strong>: 쌍둥이 소수는 무한히 많다 — 여전히 미증명!<br>
      📌 2013년 장익탕(Zhang Yitang)이 차이 7,000만 이하인 소수 쌍이 무한히 많음을 최초 증명.
    </p>
  `;
}

// ── 소수 밀도 / 소수 정리 탭 ──────────────────────────────

// 큰 N의 π(N) 근삿값 (실제 계산 불가한 경우)
const KNOWN_PI = [
  [1e3,   168],
  [1e4,   1229],
  [1e5,   9592],
  [1e6,   78498],
  [1e9,   50847534],
  [1e12,  37607912018],
  [1e15,  29844570422669],
  [1e18,  24739954287740860],
  [1e21,  21127269486018731928],
];

function buildPntTable() {
  const body = document.getElementById('pntBody');
  if (!body) return;
  const rows = [
    [100,     25],
    [1000,    168],
    [10000,   1229],
    [100000,  9592],
    [1000000, 78498],
  ];
  // 큰 수 (근삿값)
  const bigRows = [
    [1e9,  50847534],
    [1e12, 37607912018],
    [1e15, 29844570422669],
    [1e18, 24739954287740860],
    [1e21, 21127269486018731928],
  ];
  let html = '';
  const allRows = [...rows, ...bigRows];
  allRows.forEach(([N, piN], i) => {
    const lnN = Math.log(N);
    const ratio = N / piN;
    const diff = Math.abs(ratio - lnN) / lnN * 100;
    const isBig = i >= rows.length;
    const bg = i % 2 === 0 ? '#faf5ff' : '#fff';
    const nStr = N >= 1e6 ? N.toExponential(0).replace('e+', '×10^').replace(/\^(\d+)/, (m, p) => `<sup>${p}</sup>`) : N.toLocaleString();
    html += `<tr style="background:${bg};">
      <td style="padding:7px 12px;text-align:right;font-weight:700;">${isBig ? N.toExponential(0) : N.toLocaleString()}</td>
      <td style="padding:7px 12px;text-align:right;">${lnN.toFixed(4)}</td>
      <td style="padding:7px 12px;text-align:right;color:#1d4ed8;">${isBig ? piN.toLocaleString() + ' <span style="color:#94a3b8;font-size:0.75rem;">(알려진 값)</span>' : piN.toLocaleString()}</td>
      <td style="padding:7px 12px;text-align:right;color:#7c3aed;font-weight:700;">${ratio.toFixed(4)}</td>
      <td style="padding:7px 12px;text-align:right;color:${diff < 5 ? '#059669' : '#b45309'};">${diff.toFixed(4)}%</td>
    </tr>`;
  });
  body.innerHTML = html;
}

function calcProb() {
  const N = Math.max(10, +document.getElementById('probN').value || 1000);
  const lnN = Math.log(N);
  const prob = 1 / lnN;

  // 실제 소수 개수로 경험 확률 계산 (N <= 100000 만)
  let empirical = '';
  if (N <= 100000) {
    const ps = getPrimesUpTo(N);
    const lo = Math.max(2, N - 100), hi = Math.min(N + 100, N);
    // N 근처 101개 수 중 소수 비율
    const nearby = getPrimesUpTo(N + 100).filter(p => p >= N - 100);
    const empProb = nearby.length / 201;
    empirical = `<br>📊 실제 (${N-100}~${N+100} 근처): <b>${nearby.length} / 201 = ${empProb.toFixed(4)}</b>`;
  }

  document.getElementById('probResult').innerHTML = `
    <div style="background:#eff6ff;border-radius:8px;padding:10px;">
      N = <b>${N.toLocaleString()}</b><br>
      ln N = <b>${lnN.toFixed(4)}</b><br>
      1 / ln N = <b style="color:#1d4ed8;font-size:1.05em;">${prob.toFixed(4)}</b>
      <span style="color:#64748b;">(약 ${(prob*100).toFixed(2)}%)</span><br>
      → N 근처 수를 무작위로 고르면 약 <b>${Math.round(1/prob)}개 중 1개</b>가 소수!
      ${empirical}
    </div>
  `;
}

// N번째 소수 실제 리스트 (최대 10000번째까지)
let _cachedPrimes10k = null;
function getPrimes10k() {
  if (_cachedPrimes10k) return _cachedPrimes10k;
  _cachedPrimes10k = getPrimesUpTo(105000).slice(0, 10000);
  return _cachedPrimes10k;
}

function calcNth() {
  const n = Math.max(1, Math.min(10000, +document.getElementById('nthN').value || 100));
  const ps = getPrimes10k();
  const actual = ps[n - 1];
  const approx = Math.round(n * Math.log(n));
  const diff = Math.abs(approx - actual) / actual * 100;

  // 더 좋은 근사: n*(lnN + ln(lnN) - 1)
  const lnn = Math.log(n);
  const approx2 = Math.round(n * (lnn + Math.log(lnn) - 1));
  const diff2 = Math.abs(approx2 - actual) / actual * 100;

  document.getElementById('nthResult').innerHTML = `
    <div style="background:#f0fdf4;border-radius:8px;padding:10px;">
      <b>${n}번째</b> 소수 = <b style="color:#065f46;font-size:1.1em;">${actual?.toLocaleString() ?? '?'}</b><br>
      근사 N·ln N = <b>${approx.toLocaleString()}</b>
      <span style="color:${diff<5?'#059669':'#b45309'};">(오차 ${diff.toFixed(2)}%)</span><br>
      개선 근사 N·(ln N + ln ln N − 1) = <b>${approx2.toLocaleString()}</b>
      <span style="color:${diff2<3?'#059669':'#b45309'};">(오차 ${diff2.toFixed(2)}%)</span>
    </div>
    <p style="font-size:0.78rem;color:#94a3b8;margin-top:4px;">* N이 클수록 근사가 더 정확해집니다.</p>
  `;
}

function renderDensityTab() {
  buildPntTable();
  calcProb();
  calcNth();

  const canvas = document.getElementById('densityCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const MAX = +document.getElementById('graphRange').value;

  // 소수 배열 계산
  const sArr = new Array(MAX + 1).fill(false);
  sArr[0] = sArr[1] = true;
  for (let p = 2; p*p <= MAX; p++) if (!sArr[p]) for (let k=p*p; k<=MAX; k+=p) sArr[k]=true;

  // π(x) 누적 배열
  const piArr = new Array(MAX + 1).fill(0);
  let c = 0;
  for (let n = 2; n <= MAX; n++) { if (!sArr[n]) c++; piArr[n] = c; }

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = '#f8fafc'; ctx.fillRect(0, 0, W, H);

  const pad = { l: 52, r: 20, t: 24, b: 36 };
  const iW = W - pad.l - pad.r;
  const iH = H - pad.t - pad.b;
  const yMax = piArr[MAX] * 1.1;

  // 그리드 + 축
  ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, pad.t + iH);
  ctx.lineTo(pad.l + iW, pad.t + iH);
  ctx.stroke();

  ctx.fillStyle = '#64748b'; ctx.font = '11px sans-serif';
  for (let i = 0; i <= 4; i++) {
    const val = Math.round(yMax * i / 4);
    const yy = pad.t + iH - (iH * i / 4);
    ctx.textAlign = 'right'; ctx.fillText(val.toLocaleString(), pad.l - 5, yy + 4);
    ctx.strokeStyle = '#e2e8f0'; ctx.beginPath();
    ctx.moveTo(pad.l, yy); ctx.lineTo(pad.l + iW, yy); ctx.stroke();
  }
  for (let i = 0; i <= 5; i++) {
    const val = Math.round(MAX * i / 5);
    const xx = pad.l + iW * i / 5;
    ctx.textAlign = 'center'; ctx.fillStyle = '#64748b';
    ctx.fillText(val.toLocaleString(), xx, pad.t + iH + 16);
  }

  // 실제 π(x) — 파란선
  ctx.strokeStyle = '#3b82f6'; ctx.lineWidth = 2.5; ctx.setLineDash([]); ctx.beginPath();
  for (let n = 2; n <= MAX; n++) {
    const xx = pad.l + iW * (n / MAX);
    const yy = pad.t + iH - (iH * piArr[n] / yMax);
    n === 2 ? ctx.moveTo(xx, yy) : ctx.lineTo(xx, yy);
  }
  ctx.stroke();

  // 근사 x/ln(x) — 주황 점선
  ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 2; ctx.setLineDash([7, 4]); ctx.beginPath();
  for (let n = 3; n <= MAX; n++) {
    const approx = n / Math.log(n);
    const xx = pad.l + iW * (n / MAX);
    const yy = pad.t + iH - (iH * approx / yMax);
    n === 3 ? ctx.moveTo(xx, yy) : ctx.lineTo(xx, yy);
  }
  ctx.stroke();
  ctx.setLineDash([]);

  // 범례
  ctx.fillStyle = '#3b82f6'; ctx.fillRect(pad.l + 8, pad.t + 8, 22, 3);
  ctx.fillStyle = '#1e40af'; ctx.font = '12px sans-serif'; ctx.textAlign = 'left';
  ctx.fillText('π(x)  실제 소수 개수', pad.l + 36, pad.t + 13);
  ctx.strokeStyle = '#f59e0b'; ctx.setLineDash([7,4]); ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(pad.l + 8, pad.t + 26); ctx.lineTo(pad.l + 30, pad.t + 26); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#b45309'; ctx.fillText('x / ln x  (근사)', pad.l + 36, pad.t + 30);

  // 마우스 오버
  canvas.onmousemove = function(e) {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const n = Math.round((mx - pad.l) / iW * MAX);
    if (n < 2 || n > MAX) { document.getElementById('graphInfo').textContent = ''; return; }
    const info = document.getElementById('graphInfo');
    info.innerHTML = `x = <b>${n.toLocaleString()}</b> &nbsp;|&nbsp; π(x) = <b style="color:#1d4ed8;">${piArr[n]}</b> &nbsp;|&nbsp; x/ln x = <b style="color:#b45309;">${(n/Math.log(n)).toFixed(1)}</b> &nbsp;|&nbsp; 오차 = <b>${(Math.abs(piArr[n] - n/Math.log(n))/piArr[n]*100).toFixed(2)}%</b>`;
  };
  canvas.onmouseleave = () => { document.getElementById('graphInfo').textContent = ''; };
}

// ── 시작 ──────────────────────────────────────────────────
init();
</script>
</body>
</html>
"""

def render():
    st.header("🔢 미니: 에라토스테네스의 체")
    st.caption("소수를 직접 골라내 보세요! 단계별 체험, 쌍둥이 소수, 소수 밀도 분석까지.")

    components.html(HTML, height=2200, scrolling=True)
