import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "🎲 몬테카를로 시뮬레이션",
    "description": "독립시행을 무작위로 반복해 이항분포를 확인하고 π를 추정하는 몬테카를로 방법을 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>몬테카를로 시뮬레이션</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#060d1f 0%,#0b1a2e 50%,#060d1f 100%);
  color:#e2e8f0;padding:12px 12px 28px;min-height:100vh;
}
/* ── Header ───────────────────────────────────────── */
.hdr{
  text-align:center;padding:16px 18px 13px;
  background:linear-gradient(135deg,rgba(6,182,212,.12),rgba(99,102,241,.14));
  border:1px solid rgba(6,182,212,.28);border-radius:16px;margin-bottom:14px;
}
.hdr h1{font-size:1.35rem;color:#22d3ee;margin-bottom:5px;letter-spacing:-.01em}
.hdr p{font-size:.8rem;color:#94a3b8;line-height:1.65}
/* ── Tabs ─────────────────────────────────────────── */
.tab-nav{display:flex;gap:7px;margin-bottom:13px;flex-wrap:wrap}
.tab-btn{
  flex:1;min-width:120px;padding:10px 8px;border-radius:11px;
  border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04);
  cursor:pointer;text-align:center;font-size:.82rem;font-weight:700;
  color:#94a3b8;transition:all .2s;
}
.tab-btn:hover{background:rgba(255,255,255,.09);transform:translateY(-1px)}
.tab-btn.active{background:rgba(99,102,241,.2);color:#a5b4fc;border-color:rgba(99,102,241,.45)}
.tab-pane{display:none}
.tab-pane.active{display:block;animation:fadeIn .25s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
/* ── Card ─────────────────────────────────────────── */
.card{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
  border-radius:18px;padding:16px 18px;margin-bottom:12px;
  backdrop-filter:blur(8px);
}
.card-title{font-size:1rem;font-weight:700;color:#e2e8f0;margin-bottom:11px}
.info-box{
  font-size:.81rem;color:#94a3b8;line-height:1.7;
  background:rgba(6,182,212,.06);border:1px solid rgba(6,182,212,.18);
  border-radius:11px;padding:10px 14px;margin-bottom:13px;
}
.info-box strong{color:#22d3ee}
/* ── Controls ─────────────────────────────────────── */
.ctrl-row{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end;margin-bottom:12px}
.ctrl-item{display:flex;flex-direction:column;gap:5px}
.ctrl-label{font-size:.73rem;color:#94a3b8;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.vb{
  display:inline-block;min-width:44px;
  background:linear-gradient(135deg,#6366f1,#8b5cf6);
  border-radius:7px;padding:2px 9px;font-weight:800;font-size:.85rem;
  text-align:center;color:#fff;box-shadow:0 2px 8px rgba(99,102,241,.38);margin-left:4px;
}
input[type=range]{
  -webkit-appearance:none;height:5px;border-radius:3px;
  background:linear-gradient(90deg,#6366f1,#8b5cf6);
  outline:none;width:140px;cursor:pointer;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none;width:15px;height:15px;border-radius:50%;
  background:#fff;border:3px solid #6366f1;cursor:pointer;
  box-shadow:0 0 6px rgba(99,102,241,.5);
}
select{
  padding:6px 10px;border-radius:8px;border:1px solid rgba(255,255,255,.14);
  background:rgba(255,255,255,.06);color:#e2e8f0;font-size:.82rem;
  cursor:pointer;outline:none;
}
select option{background:#0b1a2e}
/* ── Buttons ──────────────────────────────────────── */
.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.btn{
  padding:7px 15px;border-radius:9px;border:none;cursor:pointer;
  font-weight:700;font-size:.8rem;transition:all .15s;color:#fff;white-space:nowrap;
}
.btn:hover{filter:brightness(1.15)}
.btn:active{transform:scale(.97)}
.btn-blue{background:linear-gradient(135deg,#6366f1,#4f46e5)}
.btn-green{background:linear-gradient(135deg,#10b981,#059669)}
.btn-amber{background:linear-gradient(135deg,#f59e0b,#d97706)}
.btn-red{background:rgba(239,68,68,.7)}
.btn-ghost{background:rgba(255,255,255,.08);color:#94a3b8}
.btn:disabled{opacity:.4;cursor:not-allowed}
/* ── Stats grid ───────────────────────────────────── */
.stat-grid{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:12px}
.stat-box{
  flex:1;min-width:100px;background:rgba(0,0,0,.28);
  border:1px solid rgba(255,255,255,.07);border-radius:12px;
  padding:10px 12px;text-align:center;
}
.stat-num{font-size:1.5rem;font-weight:900;color:#22d3ee;line-height:1.2}
.stat-lbl{font-size:.67rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:.05em;margin-top:3px}
/* ── Formula box ──────────────────────────────────── */
.fbox{
  background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.28);
  border-radius:12px;padding:12px 16px;margin-bottom:12px;text-align:center;
}
.fexpr{font-size:.95rem;font-weight:700;color:#34d399;font-family:monospace;margin-bottom:4px;line-height:1.6}
.fans{font-size:1.9rem;font-weight:900;color:#10b981;margin:4px 0}
.fnote{font-size:.72rem;color:#6ee7b7;margin-top:4px}
/* ── Coin animation area ──────────────────────────── */
.anim-area{
  background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.06);
  border-radius:13px;min-height:78px;display:flex;align-items:center;
  justify-content:center;flex-wrap:wrap;gap:5px;padding:10px 12px;
  margin-bottom:12px;overflow:hidden;
}
.coin{
  width:26px;height:26px;border-radius:50%;display:inline-flex;
  align-items:center;justify-content:center;font-size:13px;font-weight:700;
  border:2px solid;flex-shrink:0;animation:popIn .3s cubic-bezier(.25,1.5,.5,1) backwards;
}
.coin.suc{background:rgba(34,211,238,.2);border-color:#22d3ee;color:#22d3ee}
.coin.fail{background:rgba(100,116,139,.15);border-color:#475569;color:#64748b}
@keyframes popIn{from{transform:scale(0);opacity:0}to{transform:scale(1);opacity:1}}
/* ── Pi area ──────────────────────────────────────── */
.pi-layout{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-start;margin-bottom:12px}
.pi-side{flex:1;min-width:160px;display:flex;flex-direction:column;gap:9px}
.pi-estimate{
  font-size:2.8rem;font-weight:900;text-align:center;
  background:linear-gradient(135deg,#22d3ee,#818cf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin:4px 0;
}
.progress-bar{background:rgba(255,255,255,.07);border-radius:4px;height:7px;overflow:hidden}
.progress-fill{height:100%;border-radius:4px;transition:width .35s;
  background:linear-gradient(90deg,#22d3ee,#6366f1)}
.pi-note{font-size:.72rem;color:#64748b;text-align:center;margin-top:2px}
/* ── Chart label ──────────────────────────────────── */
.chart-label{font-size:.73rem;color:#64748b;margin-bottom:5px}
.chart-wrap{overflow-x:auto;margin-bottom:8px}
/* ── Binom chips ──────────────────────────────────── */
.chip{
  display:inline-block;background:rgba(99,102,241,.12);
  border:1px solid rgba(99,102,241,.28);border-radius:7px;
  padding:3px 9px;font-size:.73rem;font-family:monospace;
  color:#a5b4fc;margin:3px 2px;cursor:pointer;transition:.15s;
}
.chip:hover{background:rgba(99,102,241,.25)}
.chip.hl{background:rgba(245,158,11,.2);border-color:#f59e0b;color:#fcd34d}
/* ── Scrollbar ────────────────────────────────────── */
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(99,102,241,.4);border-radius:3px}
</style>
</head>
<body>

<!-- ── Header ──────────────────────────────────────── -->
<div class="hdr">
  <h1>🎲 몬테카를로 시뮬레이션</h1>
  <p>무작위 실험을 수없이 반복해 확률을 추정하는 방법 – 독립시행의 세계를 직접 체험해 봅시다!</p>
</div>

<!-- ── Tab nav ─────────────────────────────────────── -->
<div class="tab-nav">
  <button class="tab-btn active" id="tbn0" onclick="showTab(0)">🪙 동전·주사위 시뮬레이터</button>
  <button class="tab-btn" id="tbn1" onclick="showTab(1)">🔵 π 추정 실험</button>
  <button class="tab-btn" id="tbn2" onclick="showTab(2)">📊 이항분포 계산기</button>
</div>

<!-- ════════════════════════════════════════════════════
     TAB 0 : Bernoulli / Binomial Simulator
     ════════════════════════════════════════════════════ -->
<div class="tab-pane active" id="tab0">
<div class="card">
  <div class="card-title">🎮 독립시행 시뮬레이터</div>
  <div class="info-box">
    동전/주사위를 <strong>n번 독립적으로</strong> 던지는 시행을 반복합니다.<br>
    "성공 횟수"의 분포가 이론값인 <strong>이항분포 B(n, p)</strong>에 점점 수렴하는 것을 확인해 보세요!
  </div>
  <div class="ctrl-row">
    <div class="ctrl-item">
      <span class="ctrl-label">실험 종류</span>
      <select id="modeSelect" onchange="resetSim()">
        <option value="coin">🪙 동전 던지기 (p = 1/2)</option>
        <option value="dice">🎲 주사위 특정 눈 (p = 1/6)</option>
        <option value="custom">⚙️ 확률 직접 설정</option>
      </select>
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">1세트 시행 수 n = <span class="vb" id="s-nv">10</span></span>
      <input type="range" id="s-nSlider" min="1" max="30" value="10" oninput="onNChange()">
    </div>
    <div class="ctrl-item" id="s-pCtrl" style="display:none">
      <span class="ctrl-label">성공 확률 p = <span class="vb" id="s-pv">0.35</span></span>
      <input type="range" id="s-pSlider" min="1" max="99" value="35" oninput="onPChange()">
    </div>
  </div>
  <!-- Coin animation display -->
  <div class="anim-area" id="s-anim">
    <span style="font-size:.85rem;color:#475569">버튼을 눌러 시행을 시작해 보세요!</span>
  </div>
  <!-- Buttons -->
  <div class="btn-row">
    <button class="btn btn-blue" onclick="doRoll(1)">1세트</button>
    <button class="btn btn-green" onclick="doRoll(100)">100세트</button>
    <button class="btn btn-amber" onclick="doRoll(1000)">1000세트</button>
    <button class="btn btn-blue" id="s-autoBtn" onclick="toggleSimAuto()">▶ 자동</button>
    <button class="btn btn-ghost" onclick="resetSim()">↺ 초기화</button>
  </div>
  <!-- Stats -->
  <div class="stat-grid">
    <div class="stat-box"><div class="stat-num" id="s-sets">0</div><div class="stat-lbl">총 세트 수</div></div>
    <div class="stat-box"><div class="stat-num" id="s-succ">0</div><div class="stat-lbl">총 성공 횟수</div></div>
    <div class="stat-box"><div class="stat-num" id="s-emp" style="color:#f59e0b">-</div><div class="stat-lbl">경험적 확률</div></div>
    <div class="stat-box"><div class="stat-num" id="s-theo" style="color:#86efac">-</div><div class="stat-lbl">이론 확률 p</div></div>
  </div>
  <div class="chart-label">📈 성공 횟수 분포 &nbsp;–&nbsp; <span style="color:rgba(99,102,241,.9)">■</span> 시뮬레이션 &nbsp; <span style="color:#34d399">── </span> 이론 이항분포 B(n,p)</div>
  <div class="chart-wrap">
    <canvas id="s-hist" height="200" style="border-radius:10px;border:1px solid rgba(255,255,255,.06)"></canvas>
  </div>
</div>
</div>

<!-- ════════════════════════════════════════════════════
     TAB 1 : π Estimation
     ════════════════════════════════════════════════════ -->
<div class="tab-pane" id="tab1">
<div class="card">
  <div class="card-title">🔵 몬테카를로로 π 추정하기</div>
  <div class="info-box">
    한 변의 길이가 2인 정사각형 안에 점을 <strong>무작위(독립적으로)</strong> 던집니다.<br>
    반지름 1인 원 안에 들어올 확률은 <strong>π/4</strong>이므로,<br>
    <strong>π ≈ 4 × (원 안 점 수) / (전체 점 수)</strong> 로 추정할 수 있습니다.
  </div>
  <div class="pi-layout">
    <canvas id="pi-canvas" width="270" height="270"
      style="border-radius:14px;border:1px solid rgba(255,255,255,.1);flex-shrink:0;max-width:270px;width:100%"></canvas>
    <div class="pi-side">
      <div class="stat-grid" style="flex-direction:column;gap:8px">
        <div class="stat-box"><div class="stat-num" id="pi-total">0</div><div class="stat-lbl">총 점</div></div>
        <div class="stat-box"><div class="stat-num" id="pi-in" style="color:#22d3ee">0</div><div class="stat-lbl">원 안 <span style="color:#22d3ee">●</span></div></div>
        <div class="stat-box"><div class="stat-num" id="pi-out" style="color:#f87171">0</div><div class="stat-lbl">원 밖 <span style="color:#f87171">●</span></div></div>
      </div>
      <div class="pi-estimate" id="pi-est">–</div>
      <div class="pi-note">실제 π = 3.14159…</div>
      <div style="display:flex;align-items:center;gap:6px;margin-top:4px;justify-content:center">
        <span style="font-size:.72rem;color:#64748b">추정 오차:</span>
        <span id="pi-err" style="font-weight:800;color:#f59e0b;font-size:.88rem">–</span>
      </div>
      <div class="progress-bar" style="margin-top:8px">
        <div class="progress-fill" id="pi-prog" style="width:0%"></div>
      </div>
      <div class="pi-note" id="pi-pct">0 / 10,000</div>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-blue" onclick="piAdd(10)">+10점</button>
    <button class="btn btn-green" onclick="piAdd(100)">+100점</button>
    <button class="btn btn-amber" onclick="piAdd(1000)">+1000점</button>
    <button class="btn btn-blue" id="pi-autoBtn" onclick="piToggleAuto()">▶ 자동</button>
    <button class="btn btn-ghost" onclick="piReset()">↺ 초기화</button>
  </div>
  <div class="chart-label">📈 점 수에 따른 π 추정값 수렴 — <span style="color:#f59e0b">──</span> 추정값 &nbsp; <span style="color:rgba(34,211,238,.55)">- -</span> 실제 π</div>
  <canvas id="pi-conv" height="180" style="border-radius:10px;border:1px solid rgba(255,255,255,.06);width:100%;display:block"></canvas>
</div>
</div>

<!-- ════════════════════════════════════════════════════
     TAB 2 : Binomial Distribution Calculator
     ════════════════════════════════════════════════════ -->
<div class="tab-pane" id="tab2">
<div class="card">
  <div class="card-title">📊 이항분포 이론 계산기</div>
  <div class="info-box">
    n번의 독립시행에서 성공 확률이 p일 때,<br>
    정확히 r번 성공할 확률: <strong>P(X = r) = C(n,r) × p<sup>r</sup> × (1−p)<sup>n−r</sup></strong>
  </div>
  <div class="ctrl-row">
    <div class="ctrl-item">
      <span class="ctrl-label">시행 횟수 n = <span class="vb" id="b-nv">10</span></span>
      <input type="range" id="b-nSlider" min="1" max="30" value="10" oninput="updateBinom()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">성공 확률 p = <span class="vb" id="b-pv">0.50</span></span>
      <input type="range" id="b-pSlider" min="1" max="99" value="50" oninput="updateBinom()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">성공 횟수 r = <span class="vb" id="b-rv">5</span></span>
      <input type="range" id="b-rSlider" min="0" max="30" value="5" oninput="updateBinom()">
    </div>
  </div>
  <div class="fbox">
    <div class="fexpr" id="b-expr">...</div>
    <div class="fans" id="b-ans">...</div>
    <div class="fnote" id="b-note">...</div>
  </div>
  <div class="chart-label">📊 이항분포 B(n, p) 전체 분포 — 막대 클릭으로 r 변경 &nbsp; <span style="color:#f59e0b">■</span> 선택된 r</div>
  <div class="chart-wrap">
    <canvas id="b-chart" height="220" style="border-radius:10px;border:1px solid rgba(255,255,255,.06)"></canvas>
  </div>
  <div class="chart-label" style="margin-top:6px">각 k에서의 확률 (클릭하면 r로 선택):</div>
  <div id="b-chips"></div>
</div>
</div>

<script>
// ── Global helpers ─────────────────────────────────────────────
function comb(n, r) {
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  r = r > n - r ? n - r : r;
  let c = 1;
  for (let i = 0; i < r; i++) c = c * (n - i) / (i + 1);
  return Math.round(c);
}
function binomPMF(n, p, k) {
  if (k < 0 || k > n) return 0;
  return comb(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
}
function showTab(i) {
  document.querySelectorAll('.tab-pane').forEach((el, j) => el.classList.toggle('active', i === j));
  document.querySelectorAll('.tab-btn').forEach((el, j) => el.classList.toggle('active', i === j));
  if (i === 0) drawSimHist();
  if (i === 1) { piDrawBg(); piDrawConv(); }
  if (i === 2) { updateBinom(); }
}

// ═══════════════════════════════════════════════════════════════
// TAB 0 : Coin/Dice Simulation
// ═══════════════════════════════════════════════════════════════
let simN = 10, simP = 0.5;
let simSets = 0, simSuccTotal = 0;
let simCounts = new Array(11).fill(0);   // simCounts[k] = sets with k successes
let simAutoTimer = null;

function getSimP() {
  const m = document.getElementById('modeSelect').value;
  if (m === 'coin') return 0.5;
  if (m === 'dice') return 1 / 6;
  return parseInt(document.getElementById('s-pSlider').value) / 100;
}
function onNChange() {
  simN = parseInt(document.getElementById('s-nSlider').value);
  document.getElementById('s-nv').textContent = simN;
  resetSim();
}
function onPChange() {
  const v = parseInt(document.getElementById('s-pSlider').value) / 100;
  document.getElementById('s-pv').textContent = v.toFixed(2);
  resetSim();
}
document.getElementById('modeSelect').addEventListener('change', function() {
  document.getElementById('s-pCtrl').style.display = this.value === 'custom' ? '' : 'none';
  resetSim();
});
function resetSim() {
  stopSimAuto();
  simN = parseInt(document.getElementById('s-nSlider').value);
  simP = getSimP();
  simSets = 0; simSuccTotal = 0;
  simCounts = new Array(simN + 1).fill(0);
  document.getElementById('s-sets').textContent = '0';
  document.getElementById('s-succ').textContent = '0';
  document.getElementById('s-emp').textContent = '-';
  document.getElementById('s-theo').textContent = simP.toFixed(4);
  document.getElementById('s-anim').innerHTML =
    '<span style="font-size:.85rem;color:#475569">버튼을 눌러 시행을 시작해 보세요!</span>';
  drawSimHist();
}
function stopSimAuto() {
  if (simAutoTimer) { clearInterval(simAutoTimer); simAutoTimer = null; }
  document.getElementById('s-autoBtn').textContent = '▶ 자동';
}
function toggleSimAuto() {
  if (simAutoTimer) { stopSimAuto(); return; }
  document.getElementById('s-autoBtn').textContent = '⏹ 정지';
  simAutoTimer = setInterval(() => doRoll(1, true), 110);
}
function doRoll(sets, fromAuto) {
  simN = parseInt(document.getElementById('s-nSlider').value);
  simP = getSimP();
  if (simCounts.length !== simN + 1) simCounts = new Array(simN + 1).fill(0);

  let lastResults = [];
  for (let s = 0; s < sets; s++) {
    let k = 0;
    const res = [];
    for (let i = 0; i < simN; i++) {
      const ok = Math.random() < simP;
      res.push(ok);
      if (ok) k++;
    }
    simSets++;
    simSuccTotal += k;
    simCounts[k]++;
    if (s === sets - 1) lastResults = res;
  }
  showSimAnim(lastResults);
  updateSimStats();
  drawSimHist();
}
function showSimAnim(results) {
  const mode = document.getElementById('modeSelect').value;
  const area = document.getElementById('s-anim');
  if (!results.length) return;
  const coins = results.map((ok, i) => {
    const cls = ok ? 'coin suc' : 'coin fail';
    const lbl = mode === 'coin' ? (ok ? '앞' : '뒤') : (ok ? '★' : '×');
    const delay = Math.min(i * 18, 400);
    return `<div class="${cls}" style="animation-delay:${delay}ms">${lbl}</div>`;
  });
  area.innerHTML = coins.join('');
}
function updateSimStats() {
  const totalTrials = simSets * simN;
  const emp = totalTrials > 0 ? simSuccTotal / totalTrials : 0;
  document.getElementById('s-sets').textContent = simSets.toLocaleString();
  document.getElementById('s-succ').textContent = simSuccTotal.toLocaleString();
  document.getElementById('s-emp').textContent = totalTrials > 0 ? emp.toFixed(4) : '-';
  document.getElementById('s-theo').textContent = simP.toFixed(4);
}
function drawSimHist() {
  const canvas = document.getElementById('s-hist');
  const W = Math.max(300, canvas.parentElement.clientWidth || 520);
  canvas.width = W; const H = canvas.height;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = 'rgba(0,0,0,.22)'; ctx.fillRect(0, 0, W, H);

  const n = simN, p = simP;
  const pad = {l:44, r:14, t:14, b:32};
  const iW = W - pad.l - pad.r, iH = H - pad.t - pad.b;
  const theo = Array.from({length: n + 1}, (_, k) => binomPMF(n, p, k));
  const total = simCounts.reduce((a, b) => a + b, 0);
  const emp = simCounts.map(c => total > 0 ? c / total : 0);
  const yMax = Math.max(...theo, ...emp, 0.02) * 1.22;
  const gap = iW / (n + 1);
  const bw = Math.max(3, Math.min(38, gap * 0.6));

  // Grid
  ctx.strokeStyle = 'rgba(255,255,255,.06)'; ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + iH - iH * i / 4;
    ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(W - pad.r, y); ctx.stroke();
    ctx.fillStyle = '#475569'; ctx.font = '10px sans-serif'; ctx.textAlign = 'right';
    ctx.fillText((yMax * i / 4).toFixed(2), pad.l - 4, y + 4);
  }
  // Empirical bars
  for (let k = 0; k <= n; k++) {
    const x = pad.l + k * gap + (gap - bw) / 2;
    const h = iH * (emp[k] / yMax);
    const y = pad.t + iH - h;
    if (h > 0.5) {
      const g = ctx.createLinearGradient(0, y, 0, pad.t + iH);
      g.addColorStop(0, 'rgba(99,102,241,.9)'); g.addColorStop(1, 'rgba(67,56,202,.4)');
      ctx.fillStyle = g; ctx.fillRect(x, y, bw, h);
    }
    ctx.fillStyle = '#475569'; ctx.font = n > 20 ? '8px sans-serif' : '10px sans-serif';
    ctx.textAlign = 'center'; ctx.fillText(String(k), x + bw / 2, H - 16);
  }
  // Theoretical line
  ctx.beginPath(); ctx.strokeStyle = '#34d399'; ctx.lineWidth = 2.5;
  ctx.setLineDash([4, 3]);
  for (let k = 0; k <= n; k++) {
    const x = pad.l + k * gap + gap / 2;
    const y = pad.t + iH - iH * (theo[k] / yMax);
    k === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.stroke(); ctx.setLineDash([]);
  for (let k = 0; k <= n; k++) {
    const x = pad.l + k * gap + gap / 2;
    const y = pad.t + iH - iH * (theo[k] / yMax);
    ctx.beginPath(); ctx.arc(x, y, 3.5, 0, 2 * Math.PI);
    ctx.fillStyle = '#34d399'; ctx.fill();
  }
  // x-axis label
  ctx.fillStyle = '#475569'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText('성공 횟수 k', W / 2, H - 2);
}

// Init
resetSim();

// ═══════════════════════════════════════════════════════════════
// TAB 1 : π Estimation
// ═══════════════════════════════════════════════════════════════
const PI_MAX = 10000;
let piTotal = 0, piInside = 0;
let piHistory = [];
let piAutoTimer = null;

const piCanvas = document.getElementById('pi-canvas');
const piCtx = piCanvas.getContext('2d');
const convCanvas = document.getElementById('pi-conv');
const convCtx = convCanvas.getContext('2d');

function piReset() {
  piStopAuto();
  piTotal = 0; piInside = 0; piHistory = [];
  document.getElementById('pi-total').textContent = '0';
  document.getElementById('pi-in').textContent = '0';
  document.getElementById('pi-out').textContent = '0';
  document.getElementById('pi-est').textContent = '–';
  document.getElementById('pi-err').textContent = '–';
  document.getElementById('pi-prog').style.width = '0%';
  document.getElementById('pi-pct').textContent = '0 / 10,000';
  piDrawBg();
  piDrawConv();
}
function piStopAuto() {
  if (piAutoTimer) { clearInterval(piAutoTimer); piAutoTimer = null; }
  document.getElementById('pi-autoBtn').textContent = '▶ 자동';
}
function piToggleAuto() {
  if (piAutoTimer) { piStopAuto(); return; }
  document.getElementById('pi-autoBtn').textContent = '⏹ 정지';
  piAutoTimer = setInterval(() => {
    if (piTotal >= PI_MAX) { piStopAuto(); return; }
    piAdd(50, true);
  }, 60);
}
function piAdd(n) {
  if (piTotal >= PI_MAX) { piStopAuto(); return; }
  n = Math.min(n, PI_MAX - piTotal);
  const sz = piCanvas.width;
  const cx = sz / 2, cy = sz / 2, r = sz / 2 - 1;
  for (let i = 0; i < n; i++) {
    const x = Math.random() * sz;
    const y = Math.random() * sz;
    const inside = (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r;
    if (inside) piInside++;
    piTotal++;
    piCtx.beginPath();
    piCtx.arc(x, y, 1.7, 0, 2 * Math.PI);
    piCtx.fillStyle = inside ? 'rgba(34,211,238,.72)' : 'rgba(248,113,113,.6)';
    piCtx.fill();
  }
  if (!piHistory.length || piTotal - piHistory[piHistory.length - 1].n >= 50 || piTotal === PI_MAX)
    piHistory.push({n: piTotal, est: 4 * piInside / piTotal});
  piUpdateStats();
  piDrawConv();
  if (piTotal >= PI_MAX) piStopAuto();
}
function piUpdateStats() {
  const est = piTotal > 0 ? 4 * piInside / piTotal : 0;
  const err = piTotal > 0 ? Math.abs(est - Math.PI) : 0;
  document.getElementById('pi-total').textContent = piTotal.toLocaleString();
  document.getElementById('pi-in').textContent = piInside.toLocaleString();
  document.getElementById('pi-out').textContent = (piTotal - piInside).toLocaleString();
  document.getElementById('pi-est').textContent = piTotal > 0 ? est.toFixed(4) : '–';
  document.getElementById('pi-err').textContent = piTotal > 0 ? ('±' + err.toFixed(4)) : '–';
  const pct = Math.round(piTotal / PI_MAX * 100);
  document.getElementById('pi-prog').style.width = pct + '%';
  document.getElementById('pi-pct').textContent = piTotal.toLocaleString() + ' / 10,000';
}
function piDrawBg() {
  const sz = piCanvas.width;
  const cx = sz / 2, cy = sz / 2, r = sz / 2 - 1;
  piCtx.clearRect(0, 0, sz, sz);
  // Background
  const bg = piCtx.createRadialGradient(cx, cy, 0, cx, cy, r);
  bg.addColorStop(0, '#0b1e3a'); bg.addColorStop(1, '#060d1f');
  piCtx.fillStyle = bg; piCtx.fillRect(0, 0, sz, sz);
  // Square border
  piCtx.strokeStyle = 'rgba(99,102,241,.35)'; piCtx.lineWidth = 1.5;
  piCtx.strokeRect(1, 1, sz - 2, sz - 2);
  // Circle fill hint
  piCtx.beginPath(); piCtx.arc(cx, cy, r, 0, 2 * Math.PI);
  piCtx.fillStyle = 'rgba(6,182,212,.04)'; piCtx.fill();
  piCtx.strokeStyle = 'rgba(6,182,212,.5)'; piCtx.lineWidth = 1.8; piCtx.stroke();
  // Labels
  piCtx.fillStyle = 'rgba(6,182,212,.35)'; piCtx.font = '11px sans-serif';
  piCtx.textAlign = 'center'; piCtx.fillText('r = 1', cx, sz - 7);
  piCtx.fillStyle = 'rgba(99,102,241,.3)'; piCtx.textAlign = 'left';
  piCtx.fillText('2×2 정사각형', 5, 14);
}
function piDrawConv() {
  const W = Math.max(300, convCanvas.parentElement.clientWidth || 520);
  convCanvas.width = W; const H = convCanvas.height;
  convCtx.clearRect(0, 0, W, H);
  convCtx.fillStyle = 'rgba(0,0,0,.2)'; convCtx.fillRect(0, 0, W, H);

  if (piHistory.length < 2) {
    convCtx.fillStyle = '#475569'; convCtx.font = '12px sans-serif';
    convCtx.textAlign = 'center';
    convCtx.fillText('점을 추가하면 수렴 그래프가 표시됩니다', W / 2, H / 2);
    return;
  }
  const pad = {l:50, r:18, t:18, b:26};
  const iW = W - pad.l - pad.r, iH = H - pad.t - pad.b;
  const yMin = Math.PI - 1.3, yMax = Math.PI + 1.3;
  // Grid
  convCtx.strokeStyle = 'rgba(255,255,255,.05)'; convCtx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + iH * i / 4;
    convCtx.beginPath(); convCtx.moveTo(pad.l, y); convCtx.lineTo(W - pad.r, y); convCtx.stroke();
    const v = yMax - (yMax - yMin) * i / 4;
    convCtx.fillStyle = '#475569'; convCtx.font = '10px sans-serif';
    convCtx.textAlign = 'right'; convCtx.fillText(v.toFixed(2), pad.l - 4, y + 4);
  }
  // π reference line
  const piY = pad.t + iH * (yMax - Math.PI) / (yMax - yMin);
  convCtx.beginPath(); convCtx.moveTo(pad.l, piY); convCtx.lineTo(W - pad.r, piY);
  convCtx.strokeStyle = 'rgba(34,211,238,.45)'; convCtx.lineWidth = 1.5;
  convCtx.setLineDash([5, 4]); convCtx.stroke(); convCtx.setLineDash([]);
  convCtx.fillStyle = '#22d3ee'; convCtx.font = 'bold 10px sans-serif';
  convCtx.textAlign = 'left'; convCtx.fillText('π = 3.14159', pad.l + 4, piY - 4);
  // Estimate line
  convCtx.beginPath(); convCtx.strokeStyle = '#f59e0b'; convCtx.lineWidth = 2;
  piHistory.forEach((pt, i) => {
    const x = pad.l + iW * pt.n / PI_MAX;
    const yv = Math.max(yMin, Math.min(yMax, pt.est));
    const y = pad.t + iH * (yMax - yv) / (yMax - yMin);
    i === 0 ? convCtx.moveTo(x, y) : convCtx.lineTo(x, y);
  });
  convCtx.stroke();
  // X axis ticks
  convCtx.fillStyle = '#475569'; convCtx.font = '10px sans-serif'; convCtx.textAlign = 'center';
  for (const t of [0, 2500, 5000, 7500, 10000]) {
    const x = pad.l + iW * t / PI_MAX;
    convCtx.fillText(t.toLocaleString(), x, H - 6);
  }
  convCtx.textAlign = 'center'; convCtx.fillStyle = '#475569';
  convCtx.fillText('점 수', W / 2, H - 1);
}
piDrawBg(); piDrawConv();

// ═══════════════════════════════════════════════════════════════
// TAB 2 : Binomial Distribution Calculator
// ═══════════════════════════════════════════════════════════════
function updateBinom() {
  const n = parseInt(document.getElementById('b-nSlider').value);
  const p = parseInt(document.getElementById('b-pSlider').value) / 100;
  const rSlider = document.getElementById('b-rSlider');
  rSlider.max = n;
  let r = parseInt(rSlider.value);
  if (r > n) { r = n; rSlider.value = n; }

  document.getElementById('b-nv').textContent = n;
  document.getElementById('b-pv').textContent = p.toFixed(2);
  document.getElementById('b-rv').textContent = r;

  const prob = binomPMF(n, p, r);
  const q = 1 - p;
  const c = comb(n, r);
  document.getElementById('b-expr').textContent =
    `P(X = ${r}) = C(${n},${r}) × ${p.toFixed(2)}^${r} × ${q.toFixed(2)}^${n - r}`;
  document.getElementById('b-ans').textContent = prob > 0 ? prob.toFixed(6) : '≈ 0';
  document.getElementById('b-note').textContent =
    `C(${n},${r}) = ${c}   ·   기댓값 E(X) = ${(n*p).toFixed(2)}   ·   표준편차 σ = ${Math.sqrt(n*p*q).toFixed(3)}`;

  drawBinomChart(n, p, r);
  drawBinomChips(n, p, r);
}
function drawBinomChart(n, p, hl) {
  const canvas = document.getElementById('b-chart');
  const W = Math.max(300, canvas.parentElement.clientWidth || 520);
  canvas.width = W; const H = canvas.height;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = 'rgba(0,0,0,.2)'; ctx.fillRect(0, 0, W, H);

  const pmf = Array.from({length: n + 1}, (_, k) => binomPMF(n, p, k));
  const yMax = Math.max(...pmf) * 1.22;
  const pad = {l:44, r:14, t:16, b:32};
  const iW = W - pad.l - pad.r, iH = H - pad.t - pad.b;
  const gap = iW / (n + 1), bw = Math.max(3, Math.min(38, gap * 0.65));

  // Grid
  ctx.strokeStyle = 'rgba(255,255,255,.06)'; ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + iH - iH * i / 4;
    ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(W - pad.r, y); ctx.stroke();
    ctx.fillStyle = '#475569'; ctx.font = '10px sans-serif'; ctx.textAlign = 'right';
    ctx.fillText((yMax * i / 4).toFixed(2), pad.l - 4, y + 4);
  }
  // Bars
  for (let k = 0; k <= n; k++) {
    const x = pad.l + k * gap + (gap - bw) / 2;
    const h = iH * (pmf[k] / yMax);
    const y = pad.t + iH - h;
    if (h > 0.5) {
      if (k === hl) {
        const g = ctx.createLinearGradient(0, y, 0, pad.t + iH);
        g.addColorStop(0, '#fbbf24'); g.addColorStop(1, 'rgba(245,158,11,.4)');
        ctx.fillStyle = g;
      } else {
        const g = ctx.createLinearGradient(0, y, 0, pad.t + iH);
        g.addColorStop(0, 'rgba(99,102,241,.85)'); g.addColorStop(1, 'rgba(67,56,202,.4)');
        ctx.fillStyle = g;
      }
      ctx.fillRect(x, y, bw, h);
    }
    ctx.fillStyle = k === hl ? '#fbbf24' : '#475569';
    ctx.font = n > 22 ? '8px sans-serif' : '10px sans-serif';
    ctx.textAlign = 'center'; ctx.fillText(String(k), x + bw / 2, H - 16);
  }
  // x-axis label
  ctx.fillStyle = '#475569'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText('성공 횟수 k', W / 2, H - 2);
  // Click handler
  canvas.onclick = function(e) {
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (W / rect.width);
    const k = Math.round((mx - pad.l - gap / 2) / gap);
    const clamp = Math.max(0, Math.min(n, k));
    document.getElementById('b-rSlider').value = clamp;
    updateBinom();
  };
}
function drawBinomChips(n, p, hl) {
  const el = document.getElementById('b-chips');
  el.innerHTML = Array.from({length: n + 1}, (_, k) => {
    const v = binomPMF(n, p, k);
    if (v < 0.0005 && k !== hl) return '';
    const cls = k === hl ? 'chip hl' : 'chip';
    return `<span class="${cls}" onclick="selectR(${k})">k=${k}: ${v.toFixed(4)}</span>`;
  }).join('');
}
function selectR(k) {
  document.getElementById('b-rSlider').value = k;
  updateBinom();
}
updateBinom();

// ── Resize ─────────────────────────────────────────────────────
window.addEventListener('resize', () => {
  drawSimHist();
  piDrawConv();
  const tab2Active = document.getElementById('tab2').classList.contains('active');
  if (tab2Active) drawBinomChart(
    parseInt(document.getElementById('b-nSlider').value),
    parseInt(document.getElementById('b-pSlider').value) / 100,
    parseInt(document.getElementById('b-rSlider').value)
  );
});
</script>
</body>
</html>"""


def render():
    components.html(_HTML, height=860, scrolling=True)
