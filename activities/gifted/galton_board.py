import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 갈톤보드 시뮬레이션",
    "description": "구슬이 파스칼의 삼각형 경로를 따라 떨어지며 이항분포가 만들어지는 과정을 시뮬레이션합니다.",
    "order": 25,
    "hidden": True,
}

HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0f172a; color: #f1f5f9; font-family: 'Segoe UI', system-ui, sans-serif; }
#wrap { max-width: 980px; margin: 0 auto; padding: 10px 14px 20px; }

/* ── 컨트롤 ── */
.controls {
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  background: #1e293b; border-radius: 12px; padding: 9px 13px; margin-bottom: 10px;
}
.ctrl-group { display: flex; align-items: center; gap: 5px; }
.ctrl-group label { font-size: 0.78rem; color: #94a3b8; white-space: nowrap; }
.ctrl-group input[type=range] { width: 80px; accent-color: #f59e0b; }
.ctrl-group select {
  background: #334155; color: #f1f5f9; border: 1px solid #475569;
  border-radius: 6px; padding: 3px 7px; font-size: 0.8rem; cursor: pointer;
}
.val-badge {
  min-width: 30px; text-align: center; font-size: 0.8rem; font-weight: 700;
  color: #fbbf24; background: #292524; border-radius: 6px; padding: 2px 5px;
}
.sep { width: 1px; height: 24px; background: #334155; }

/* ── 버튼 ── */
.btn {
  padding: 6px 13px; border-radius: 8px; border: none; cursor: pointer;
  font-size: 0.81rem; font-weight: 700; transition: all .15s; white-space: nowrap;
}
.btn:hover { filter: brightness(1.1); }
.btn:active { transform: translateY(1px); }
.btn-go   { background: #f59e0b; color: #1c1917; }
.btn-auto { background: #3b82f6; color: #fff; }
.btn-fast { background: #10b981; color: #fff; }
.btn-reset{ background: #ef4444; color: #fff; }

/* ── 메인 레이아웃 ── */
.main-area { display: flex; gap: 12px; align-items: flex-start; flex-wrap: wrap; }
#boardWrap { flex: 0 0 auto; }
canvas#board { border-radius: 12px; background: #0f172a; display: block; }

/* ── 오른쪽 패널 ── */
#right-panel {
  flex: 1 1 200px; display: flex; flex-direction: column; gap: 8px; min-width: 200px;
}
.stat-card {
  background: #1e293b; border-radius: 10px; padding: 10px 12px;
}
.stat-card h3 {
  font-size: 0.73rem; color: #64748b; font-weight: 700; letter-spacing: .5px;
  text-transform: uppercase; margin-bottom: 7px;
}

/* ── 총계 ── */
.total-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.total-label { font-size: 0.8rem; color: #94a3b8; }
.total-val   { font-size: 1.15rem; font-weight: 800; color: #fbbf24; }
.meta-row  { font-size: 0.78rem; color: #94a3b8; }
.meta-val  { font-weight: 700; color: #34d399; }

/* ── 분포 표 ── */
#dist-table {
  width: 100%; border-collapse: collapse; font-size: 0.76rem; margin-top: 4px;
}
#dist-table th {
  color: #64748b; font-weight: 700; text-align: center;
  padding: 3px 4px; border-bottom: 1px solid #334155;
}
#dist-table td {
  text-align: center; padding: 2px 4px; color: #e2e8f0;
}
#dist-table tr:nth-child(even) td { background: rgba(255,255,255,0.02); }
#dist-table td.k-col  { color: #94a3b8; font-weight: 600; }
#dist-table td.cnt-col { color: #fbbf24; font-weight: 700; }
#dist-table td.emp-col { color: #f59e0b; }
#dist-table td.th-col  { color: #60a5fa; }
#dist-table .total-row-tr td { border-top: 1px solid #334155; color: #94a3b8; font-style: italic; font-size: 0.72rem; }

/* ── 막대 범례 ── */
.legend { display: flex; gap: 10px; font-size: 0.73rem; color: #94a3b8; margin-bottom: 6px; flex-wrap: wrap; }
.legend span { display: flex; align-items: center; gap: 4px; }
.dot { width:9px; height:9px; border-radius:50%; display:inline-block; }
.dot.emp { background: #f59e0b; }
.dot.th  { background: #3b82f6; }

/* ── 막대 ── */
.pb-row { display: flex; align-items: center; gap: 4px; margin: 2px 0; }
.pb-lbl { font-size: 0.7rem; color: #94a3b8; min-width: 16px; text-align: right; }
.pb-track { flex: 1; height: 9px; background: #334155; border-radius: 4px; position: relative; overflow: hidden; }
.pb-th  { position: absolute; top: 0; height: 100%; background: rgba(59,130,246,0.55); border-radius: 4px; }
.pb-emp { position: absolute; top: 0; height: 100%; background: #f59e0b; border-radius: 4px; opacity: 0.85; }
</style>
</head>
<body>
<div id="wrap">

  <!-- 컨트롤 -->
  <div class="controls">
    <div class="ctrl-group">
      <label>줄 수 n</label>
      <input type="range" id="rowsSlider" min="3" max="12" value="7" step="1">
      <span class="val-badge" id="rowsVal">7</span>
    </div>
    <div class="ctrl-group">
      <label>우측 확률 p</label>
      <input type="range" id="pSlider" min="0.1" max="0.9" value="0.5" step="0.05">
      <span class="val-badge" id="pVal">0.50</span>
    </div>
    <div class="ctrl-group">
      <label>속도</label>
      <select id="speedSel">
        <option value="slow">느리게</option>
        <option value="normal" selected>보통</option>
        <option value="fast">빠르게</option>
      </select>
    </div>
    <div class="sep"></div>
    <button class="btn btn-go"   id="dropOne">구슬 1개 ▼</button>
    <button class="btn btn-auto" id="autoBtn">▶ 자동 투하</button>
    <button class="btn btn-fast" id="drop100">100개 즉시</button>
    <button class="btn btn-reset" id="resetBtn">초기화</button>
  </div>

  <!-- 메인 -->
  <div class="main-area">
    <div id="boardWrap">
      <canvas id="board" width="520" height="500"></canvas>
    </div>

    <div id="right-panel">
      <!-- 총계 카드 -->
      <div class="stat-card">
        <div class="total-row">
          <span class="total-label">총 투하 구슬</span>
          <span class="total-val" id="total-val">0</span>
        </div>
        <div class="meta-row">
          p = <span class="meta-val" id="p-display">0.50</span>
          &nbsp;&nbsp;
          기대값 np = <span class="meta-val" id="mean-display">3.50</span>
        </div>
      </div>

      <!-- 분포 표 -->
      <div class="stat-card">
        <h3>칸별 분포</h3>
        <table id="dist-table">
          <thead>
            <tr>
              <th>k</th>
              <th>개수</th>
              <th>비율%</th>
              <th>이론%</th>
            </tr>
          </thead>
          <tbody id="dist-body"></tbody>
        </table>
      </div>

      <!-- 막대 비교 -->
      <div class="stat-card" style="flex:1">
        <h3>분포 비교</h3>
        <div class="legend">
          <span><span class="dot emp"></span>경험(노랑)</span>
          <span><span class="dot th"></span>이론(파랑)</span>
        </div>
        <div id="barArea"></div>
      </div>
    </div>
  </div>

</div>

<script>
(function(){
"use strict";

const canvas = document.getElementById('board');
const ctx    = canvas.getContext('2d');

// ── 상태 ──
let rows      = 7;
let p         = 0.5;
let balls     = [];
let buckets   = [];
let totalDropped = 0;
let autoMode  = false;
let autoTimer = null;
let speedMode = 'normal';

// ── 레이아웃 상수 ──
const PAD_TOP  = 36;
const PAD_SIDE = 28;
const BUCKET_AREA_H = 110;

function getLayout() {
  const W = canvas.width;
  const H = canvas.height;
  const boardH  = H - PAD_TOP - BUCKET_AREA_H;
  const rowH    = boardH / (rows + 0.5);
  const nails   = [];
  for (let r = 0; r <= rows; r++) {
    const cnt    = r + 1;
    const rowY   = PAD_TOP + r * rowH;
    const span   = W - PAD_SIDE * 2;
    const gap    = cnt > 1 ? span / (cnt - 1) : 0;
    const startX = cnt === 1 ? W / 2 : PAD_SIDE;
    for (let c = 0; c <= r; c++) {
      nails.push({ r, c, x: startX + c * gap, y: rowY });
    }
  }
  const bucketTop = PAD_TOP + (rows + 0.5) * rowH;
  const bucketW   = (W - PAD_SIDE * 2) / (rows + 1);
  const bucketMaxH = H - bucketTop - 8;
  return { W, H, rowH, nails, bucketTop, bucketW, bucketMaxH };
}

function nailAt(r, c) {
  return getLayout().nails.find(n => n.r === r && n.c === c);
}

function C(n, k) {
  if (k < 0 || k > n) return 0;
  if (k === 0 || k === n) return 1;
  k = Math.min(k, n - k);
  let r = 1;
  for (let i = 0; i < k; i++) r = r * (n - i) / (i + 1);
  return Math.round(r);
}
function binomProb(n, k, pp) {
  return C(n, k) * Math.pow(pp, k) * Math.pow(1 - pp, n - k);
}

class Ball {
  constructor() {
    const L = getLayout();
    this.col     = 0;
    this.pathIdx = 0;
    this.path = [];
    for (let i = 0; i < rows; i++) {
      this.path.push(Math.random() < p ? 'R' : 'L');
    }
    this.finalCol = this.path.filter(d => d === 'R').length;
    this.phase    = 'fall';
    this.t        = 0;
    this.color    = `hsl(${35 + Math.random()*30},95%,${55 + Math.random()*15}%)`;
    this._setNextTarget();
  }

  _setNextTarget() {
    const L = getLayout();
    if (this.pathIdx === 0) {
      this.fromX = L.W / 2;
      this.fromY = PAD_TOP - 18;
      const n = nailAt(0, 0);
      this.toX = n.x;
      this.toY = n.y;
    } else if (this.pathIdx <= rows) {
      const dir     = this.path[this.pathIdx - 1];
      const fromCol = this.col - (dir === 'R' ? 1 : 0);
      const pn      = nailAt(this.pathIdx - 1, fromCol);
      this.fromX = pn.x;
      this.fromY = pn.y;
      if (this.pathIdx === rows) {
        this.toX = PAD_SIDE + this.finalCol * L.bucketW + L.bucketW / 2;
        this.toY = L.bucketTop + 14;
      } else {
        const nn = nailAt(this.pathIdx, this.col);
        this.toX = nn.x;
        this.toY = nn.y;
      }
    }
    this.t = 0;
  }

  update() {
    if (this.phase === 'done') return;
    const speed = { slow: 0.022, normal: 0.05, fast: 0.11 }[speedMode] || 0.05;
    this.t = Math.min(1, this.t + speed);
    const ease = t => t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
    const et   = ease(this.t);
    this.x = this.fromX + (this.toX - this.fromX) * et;
    const arc = Math.sin(Math.PI * this.t) * 5;
    this.y = this.fromY + (this.toY - this.fromY) * et + arc;
    if (this.t >= 1) {
      this.x = this.toX;
      this.y = this.toY;
      this.pathIdx++;
      if (this.pathIdx > rows) {
        this.phase = 'done';
        buckets[this.finalCol]++;
        totalDropped++;
        updateStats();
      } else {
        const dir = this.path[this.pathIdx - 1];
        if (dir === 'R') this.col++;
        this._setNextTarget();
      }
    }
  }

  draw() {
    if (this.phase === 'done') return;
    ctx.beginPath();
    ctx.arc(this.x, this.y, 6, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
    ctx.strokeStyle = 'rgba(0,0,0,0.35)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }
}

function draw() {
  const L = getLayout();
  const { W, H, rowH, nails, bucketTop, bucketW, bucketMaxH } = L;
  ctx.clearRect(0, 0, W, H);
  const bg = ctx.createLinearGradient(0, 0, 0, H);
  bg.addColorStop(0, '#0f172a');
  bg.addColorStop(1, '#1a2535');
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  const maxBucket = Math.max(1, ...buckets);
  for (let i = 0; i <= rows; i++) {
    const bx  = PAD_SIDE + i * bucketW;
    const bh  = (buckets[i] / maxBucket) * bucketMaxH;
    const thP = binomProb(rows, i, p);
    const thH = thP * bucketMaxH * (rows + 1);
    ctx.strokeStyle = '#334155';
    ctx.lineWidth   = 1;
    ctx.strokeRect(bx + 1, bucketTop, bucketW - 2, bucketMaxH);
    const thBarH = Math.min(thH, bucketMaxH);
    ctx.fillStyle = 'rgba(59,130,246,0.28)';
    ctx.fillRect(bx + 2, bucketTop + bucketMaxH - thBarH, bucketW - 4, thBarH);
    if (bh > 0) {
      const grad = ctx.createLinearGradient(0, bucketTop + bucketMaxH - bh, 0, bucketTop + bucketMaxH);
      grad.addColorStop(0, '#fcd34d');
      grad.addColorStop(1, '#d97706');
      ctx.fillStyle = grad;
      ctx.fillRect(bx + 2, bucketTop + bucketMaxH - bh, bucketW - 4, bh);
    }
    ctx.fillStyle  = '#64748b';
    ctx.font       = `${Math.max(9, 11 - rows * 0.3)}px 'Segoe UI', sans-serif`;
    ctx.textAlign  = 'center';
    ctx.fillText(String(i), bx + bucketW / 2, bucketTop + bucketMaxH + 13);
    if (buckets[i] > 0) {
      ctx.fillStyle = '#fbbf24';
      ctx.font      = `bold ${Math.max(8, 10 - rows * 0.3)}px 'Segoe UI', sans-serif`;
      ctx.fillText(String(buckets[i]), bx + bucketW / 2, bucketTop + bucketMaxH - bh - 3);
    }
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c <= r; c++) {
      const curr  = nailAt(r, c);
      const left  = nailAt(r + 1, c);
      const right = nailAt(r + 1, c + 1);
      ctx.strokeStyle = 'rgba(100,116,139,0.35)';
      ctx.lineWidth   = 1;
      if (left)  { ctx.beginPath(); ctx.moveTo(curr.x, curr.y); ctx.lineTo(left.x,  left.y);  ctx.stroke(); }
      if (right) { ctx.beginPath(); ctx.moveTo(curr.x, curr.y); ctx.lineTo(right.x, right.y); ctx.stroke(); }
    }
  }

  const nailR = Math.max(3.5, 5.5 - rows * 0.15);
  for (const nail of nails) {
    ctx.beginPath();
    ctx.arc(nail.x, nail.y, nailR, 0, Math.PI * 2);
    ctx.fillStyle   = '#cbd5e1';
    ctx.fill();
    ctx.strokeStyle = '#475569';
    ctx.lineWidth   = 1;
    ctx.stroke();
    if (rows <= 8) {
      const val = C(nail.r, nail.c);
      ctx.fillStyle = 'rgba(148,163,184,0.7)';
      ctx.font      = `${Math.max(7, 9 - rows * 0.3)}px 'Segoe UI', sans-serif`;
      ctx.textAlign = 'center';
      ctx.fillText(String(val), nail.x, nail.y - nailR - 3);
    }
  }

  for (const ball of balls) ball.draw();
  ctx.fillStyle  = '#f59e0b';
  ctx.font       = 'bold 13px sans-serif';
  ctx.textAlign  = 'center';
  ctx.fillText('▼', W / 2, PAD_TOP - 20);
}

function loop() {
  for (const ball of balls) ball.update();
  for (let i = balls.length - 1; i >= 0; i--) {
    if (balls[i].phase === 'done') balls.splice(i, 1);
  }
  draw();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

function updateStats() {
  document.getElementById('total-val').textContent    = totalDropped.toLocaleString();
  document.getElementById('p-display').textContent    = p.toFixed(2);
  document.getElementById('mean-display').textContent = (rows * p).toFixed(2);

  const tbody = document.getElementById('dist-body');
  tbody.innerHTML = '';
  const maxThP = binomProb(rows, Math.round(rows * p), p) || 0.001;

  for (let i = 0; i <= rows; i++) {
    const thP  = binomProb(rows, i, p);
    const empP = totalDropped > 0 ? buckets[i] / totalDropped : 0;
    const tr   = document.createElement('tr');
    tr.innerHTML = `
      <td class="k-col">${i}</td>
      <td class="cnt-col">${buckets[i]}</td>
      <td class="emp-col">${totalDropped > 0 ? (empP * 100).toFixed(1) : '-'}</td>
      <td class="th-col">${(thP * 100).toFixed(1)}</td>`;
    tbody.appendChild(tr);
  }
  const totTr = document.createElement('tr');
  totTr.className = 'total-row-tr';
  totTr.innerHTML = `
    <td>합계</td>
    <td class="cnt-col">${totalDropped}</td>
    <td class="emp-col">${totalDropped > 0 ? '100.0' : '-'}</td>
    <td class="th-col">100.0</td>`;
  tbody.appendChild(totTr);

  const barArea = document.getElementById('barArea');
  barArea.innerHTML = '';
  for (let i = 0; i <= rows; i++) {
    const thP  = binomProb(rows, i, p);
    const empP = totalDropped > 0 ? buckets[i] / totalDropped : 0;
    const thW  = Math.min(100, (thP  / maxThP) * 85);
    const empW = Math.min(100, (empP / maxThP) * 85);
    const row  = document.createElement('div');
    row.className = 'pb-row';
    row.innerHTML = `
      <div class="pb-lbl">${i}</div>
      <div class="pb-track">
        <div class="pb-th"  style="width:${thW }%"></div>
        <div class="pb-emp" style="width:${empW}%"></div>
      </div>`;
    barArea.appendChild(row);
  }
}

function dropBall() {
  if (balls.length < 25) balls.push(new Ball());
}

function drop100() {
  stopAuto();
  for (let i = 0; i < 100; i++) {
    let c = 0;
    for (let r = 0; r < rows; r++) { if (Math.random() < p) c++; }
    buckets[c]++;
    totalDropped++;
  }
  updateStats();
}

function stopAuto() {
  autoMode = false;
  clearInterval(autoTimer);
  document.getElementById('autoBtn').textContent = '▶ 자동 투하';
  document.getElementById('autoBtn').style.background = '#3b82f6';
}

function setup() {
  stopAuto();
  buckets = new Array(rows + 1).fill(0);
  balls   = [];
  totalDropped = 0;
  updateStats();
  draw();
}

document.getElementById('dropOne').addEventListener('click', dropBall);

document.getElementById('autoBtn').addEventListener('click', () => {
  autoMode = !autoMode;
  if (autoMode) {
    document.getElementById('autoBtn').textContent = '■ 자동 정지';
    document.getElementById('autoBtn').style.background = '#7c3aed';
    const interval = { slow: 700, normal: 300, fast: 120 }[speedMode] || 300;
    autoTimer = setInterval(() => { if (balls.length < 18) dropBall(); }, interval);
  } else {
    stopAuto();
  }
});

document.getElementById('drop100').addEventListener('click', drop100);
document.getElementById('resetBtn').addEventListener('click', setup);

document.getElementById('rowsSlider').addEventListener('input', e => {
  rows = +e.target.value;
  document.getElementById('rowsVal').textContent = rows;
  setup();
});

document.getElementById('pSlider').addEventListener('input', e => {
  p = +e.target.value;
  document.getElementById('pVal').textContent = p.toFixed(2);
  setup();
});

document.getElementById('speedSel').addEventListener('change', e => {
  speedMode = e.target.value;
  if (autoMode) {
    clearInterval(autoTimer);
    const interval = { slow: 700, normal: 300, fast: 120 }[speedMode] || 300;
    autoTimer = setInterval(() => { if (balls.length < 18) dropBall(); }, interval);
  }
});

setup();

})();
</script>
</body>
</html>
"""


def render():
    st.header("🎰 갈톤보드 (Galton Board) 시뮬레이션")
    st.caption("구슬이 각 못에서 좌(L) 또는 우(R)로 떨어지며, 최종 위치의 분포는 이항분포를 따릅니다.")

    components.html(HTML, height=660, scrolling=False)

    with st.expander("💡 활동 안내", expanded=False):
        st.markdown(
            """
**갈톤보드란?**
- 영국 통계학자 프랜시스 갈톤(Francis Galton)이 고안한 장치
- 구슬이 각 못에서 좌(L) 또는 우(R)로 떨어지며, 최종 위치의 분포는 **이항분포 B(n, p)** 를 따릅니다

**탐구 방법**
1. 줄 수 n = 7, p = 0.5로 시작 → 구슬을 여러 개 투하해 분포 관찰
2. p를 0.3, 0.7로 바꿔 분포가 어떻게 달라지는지 비교
3. n을 늘릴수록 분포가 정규분포에 가까워지는지 확인 (중심극한정리!)

**파스칼의 삼각형과의 연결**
- 각 못의 숫자(이항계수 ₙCᵣ)는 그 경로를 지나는 구슬의 상대적 빈도를 나타냅니다
- n번째 줄의 이항계수의 합 = 2ⁿ (전체 경로의 수)
            """
        )
