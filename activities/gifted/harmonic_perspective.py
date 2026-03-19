import base64
import io
import os

import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 등간격 사물 → 화폭에서 조화수열",
    "description": "실제 공간에서 등간격으로 놓인 사물을 화폭에 담으면 화폭에서의 투영 높이가 조화수열을 이루는 원리를 인터랙티브하게 탐구합니다.",
    "order": 36,
    "hidden": True,
}

_HTML = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f172a; color: #e2e8f0;
  font-family: 'Segoe UI', 'Noto Sans KR', system-ui, sans-serif;
  font-size: 14px; line-height: 1.5;
}
#app { max-width: 920px; margin: 0 auto; padding: 14px 14px 24px; }

.intro-box {
  background: #1e293b; border-left: 4px solid #facc15;
  border-radius: 0 10px 10px 0;
  padding: 12px 16px; margin-bottom: 16px;
  font-size: 0.82rem; color: #cbd5e1; line-height: 1.7;
}
.intro-box b { color: #facc15; }
.intro-box .red { color: #f87171; }

/* Controls */
.ctrl-panel {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 12px; padding: 14px 16px; margin-bottom: 14px;
}
.ctrl-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 12px 24px;
}
@media (max-width: 600px) { .ctrl-grid { grid-template-columns: 1fr; } }
.ctrl-row { display: flex; flex-direction: column; gap: 4px; }
.ctrl-lbl {
  font-size: 0.76rem; color: #7dd3fc; font-weight: 700;
  display: flex; justify-content: space-between;
}
.ctrl-lbl .val { color: #fbbf24; font-size: 0.82rem; }
input[type=range] {
  width: 100%; cursor: pointer; accent-color: #38bdf8;
  height: 5px;
}

/* Diagram */
.diagram-wrap {
  background: #0d1b2a; border: 1px solid #1e3a5f;
  border-radius: 12px; overflow: hidden; margin-bottom: 14px;
  position: relative;
}
.diagram-label {
  position: absolute; top: 8px; left: 12px;
  font-size: 0.72rem; color: #475569; font-weight: 700; letter-spacing: .05em;
}
canvas { display: block; width: 100%; }

/* Results */
.results-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 10px; margin-bottom: 14px;
}
.res-box {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 10px; padding: 10px 12px; text-align: center;
}
.res-lbl { font-size: 0.7rem; color: #94a3b8; margin-bottom: 2px; }
.res-val { font-size: 1.35rem; font-weight: 800; }
.res-sub { font-size: 0.7rem; color: #64748b; margin-top: 2px; }

/* Harmony panel */
.harmony-panel {
  background: #1e293b; border: 1.5px solid #334155;
  border-radius: 12px; padding: 14px 16px; margin-bottom: 14px;
}
.harm-title {
  font-size: 0.8rem; font-weight: 800; color: #7dd3fc;
  margin-bottom: 10px; letter-spacing: .04em;
}
.harm-row {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 8px; flex-wrap: wrap;
}
.harm-item {
  background: #0f172a; border: 1px solid #334155;
  border-radius: 8px; padding: 6px 12px;
  font-size: 0.78rem; min-width: 100px; text-align: center;
}
.harm-item .name { color: #94a3b8; font-size: 0.7rem; }
.harm-item .num { font-weight: 800; font-size: 1rem; }
.arrow { color: #475569; font-size: 1.1rem; }
.harm-note {
  font-size: 0.75rem; color: #94a3b8; margin-top: 6px;
  padding: 8px 10px; background: #0f172a; border-radius: 8px;
  border: 1px solid #1e3a5f;
}
.harm-note .hi { color: #4ade80; font-weight: 700; }
.harm-note .warn { color: #fbbf24; font-weight: 700; }

/* Canvas view */
.canvas-view-wrap {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 12px; overflow: hidden; margin-bottom: 14px;
}
.canvas-view-header {
  padding: 10px 14px 0;
  font-size: 0.78rem; font-weight: 800; color: #7dd3fc;
  letter-spacing: .04em;
}
.canvas-view-sub {
  padding: 2px 14px 8px;
  font-size: 0.72rem; color: #64748b;
}

/* N trees challenge */
.challenge-panel {
  background: #1e293b; border: 1.5px solid #334155;
  border-radius: 12px; padding: 14px 16px;
}
.challenge-title {
  font-size: 0.8rem; font-weight: 800; color: #f0abfc;
  margin-bottom: 10px;
}
.n-ctrl { display: flex; align-items: center; gap: 14px; margin-bottom: 12px; flex-wrap: wrap; }
.n-ctrl label { font-size: 0.76rem; color: #7dd3fc; }
.n-ctrl input[type=range] { flex: 1; min-width: 120px; max-width: 260px; accent-color: #f0abfc; }
.n-ctrl .n-val { font-size: 0.88rem; font-weight: 800; color: #fbbf24; min-width: 20px; }
.ntree-bars { display: flex; align-items: flex-end; gap: 6px; height: 120px; padding: 0 4px; }
.ntree-bar-wrap { display: flex; flex-direction: column; align-items: center; flex: 1; }
.ntree-bar {
  width: 100%; border-radius: 4px 4px 0 0;
  transition: height .3s ease;
  position: relative;
}
.ntree-bar-lbl { font-size: 0.6rem; color: #64748b; margin-top: 3px; }
.ntree-note {
  font-size: 0.73rem; color: #94a3b8; margin-top: 10px;
  padding: 8px 10px; background: #0f172a; border-radius: 8px;
  border: 1px solid #1e3a5f;
}
.ntree-note .formula { color: #f0abfc; font-weight: 700; }
</style>
</head>
<body>
<div id="app">

  <!-- Intro -->
  <div class="intro-box">
    실제 공간에서 <b>등간격(등차수열)</b>으로 서 있는 나무들을 정면에서 화폭(캔버스)에 담으면,
    화폭 위의 나무 높이들은 <span class="red"><b>조화수열</b></span>을 이룹니다.
    슬라이더를 조정하며 이 원리를 직접 확인해 보세요.
  </div>

  <!-- Controls -->
  <div class="ctrl-panel">
    <div class="ctrl-grid">
      <div class="ctrl-row">
        <div class="ctrl-lbl">화폭까지 거리 <span style="font-weight:400;color:#64748b">(OP)</span>
          <span class="val" id="lbl-OP">100</span>
        </div>
        <input type="range" id="sl-OP" min="40" max="180" value="100" step="2">
      </div>
      <div class="ctrl-row">
        <div class="ctrl-lbl">첫 번째 나무까지 거리 <span style="font-weight:400;color:#64748b">(OB₁)</span>
          <span class="val" id="lbl-OB1">200</span>
        </div>
        <input type="range" id="sl-OB1" min="120" max="320" value="200" step="5">
      </div>
      <div class="ctrl-row">
        <div class="ctrl-lbl">나무 사이 간격 <span style="font-weight:400;color:#64748b">(등차)</span>
          <span class="val" id="lbl-gap">100</span>
        </div>
        <input type="range" id="sl-gap" min="40" max="200" value="100" step="5">
      </div>
      <div class="ctrl-row">
        <div class="ctrl-lbl">나무 실제 높이 <span style="font-weight:400;color:#64748b">(AB)</span>
          <span class="val" id="lbl-H">80</span>
        </div>
        <input type="range" id="sl-H" min="30" max="140" value="80" step="5">
      </div>
    </div>
  </div>

  <!-- Geometric Diagram -->
  <div class="diagram-wrap">
    <div class="diagram-label">기하학적 도식 (측면도)</div>
    <canvas id="cvDiagram" height="300"></canvas>
  </div>

  <!-- PQ PR PS results -->
  <div class="results-grid">
    <div class="res-box">
      <div class="res-lbl">첫 번째 투영 <b style="color:#f472b6">PQ</b></div>
      <div class="res-val" id="val-PQ" style="color:#f472b6">—</div>
      <div class="res-sub" id="sub-PQ"></div>
    </div>
    <div class="res-box">
      <div class="res-lbl">두 번째 투영 <b style="color:#a78bfa">PR</b></div>
      <div class="res-val" id="val-PR" style="color:#a78bfa">—</div>
      <div class="res-sub" id="sub-PR"></div>
    </div>
    <div class="res-box">
      <div class="res-lbl">세 번째 투영 <b style="color:#60a5fa">PS</b></div>
      <div class="res-val" id="val-PS" style="color:#60a5fa">—</div>
      <div class="res-sub" id="sub-PS"></div>
    </div>
  </div>

  <!-- Harmony verification -->
  <div class="harmony-panel">
    <div class="harm-title">📊 조화수열 확인 — 역수가 등차수열을 이루는지 보자</div>
    <div class="harm-row" id="harm-row">
      <!-- filled by JS -->
    </div>
    <div class="harm-note" id="harm-note"></div>
  </div>

  <!-- Painter's canvas view -->
  <div class="canvas-view-wrap">
    <div class="canvas-view-header">🖼️ 화폭에서의 모습</div>
    <div class="canvas-view-sub">화폭 위에 투영된 나무 높이 — 실제 나무는 같은 높이, 화폭에서는 점점 작아짐</div>
    <canvas id="cvPainter" height="200"></canvas>
  </div>

  <!-- N-trees challenge -->
  <div class="challenge-panel">
    <div class="challenge-title">🌳 나무가 n그루라면? — 조화수열 확장</div>
    <div class="n-ctrl">
      <label>나무 수 n =</label>
      <input type="range" id="sl-N" min="2" max="10" value="3" step="1">
      <span class="n-val" id="lbl-N">3</span>
      <span style="font-size:0.72rem; color:#64748b; margin-left:4px">그루</span>
    </div>
    <div class="ntree-bars" id="ntree-bars"></div>
    <div class="ntree-note" id="ntree-note"></div>
  </div>

</div>

<script>
const cvD = document.getElementById('cvDiagram');
const ctxD = cvD.getContext('2d');
const cvP = document.getElementById('cvPainter');
const ctxP = cvP.getContext('2d');

const COLORS = ['#f472b6','#a78bfa','#60a5fa','#34d399','#fb923c','#facc15','#e879f9','#38bdf8','#4ade80','#f97316'];

function getP() {
  return {
    OP:  +document.getElementById('sl-OP').value,
    OB1: +document.getElementById('sl-OB1').value,
    gap: +document.getElementById('sl-gap').value,
    H:   +document.getElementById('sl-H').value,
    N:   +document.getElementById('sl-N').value,
  };
}

function calcProj(OP, OBi, H) {
  return H * OP / OBi;
}

// ── Geometric diagram ──────────────────────────────────────────────────────
function drawDiagram(p) {
  const {OP, OB1, gap, H} = p;
  const W = cvD.offsetWidth || 860;
  cvD.width = W;
  const CH = 300;
  const ctx = ctxD;

  ctx.clearRect(0, 0, W, CH);

  const N = 3;
  const OBs = Array.from({length:N}, (_,i) => OB1 + i*gap);
  const OBmax = OBs[N-1];

  // scene extents
  const sceneW = OBmax * 1.12;
  const sceneH = H * 1.9;
  const padL = 32, padR = 16, padB = 36, padT = 28;
  const drawW = W - padL - padR;
  const drawH = CH - padT - padB;
  const scX = drawW / sceneW;
  const scY = drawH / sceneH;
  const sc = Math.min(scX, scY);

  const toX = x => padL + x * sc;
  const toY = y => CH - padB - y * sc;

  const gndY = toY(0);

  // ── Grid lines (light)
  ctx.strokeStyle = '#1e3a5f';
  ctx.lineWidth = 1;
  for (let yi = 0; yi <= sceneH; yi += Math.round(sceneH/4)) {
    const cy = toY(yi);
    ctx.beginPath(); ctx.moveTo(padL, cy); ctx.lineTo(W - padR, cy); ctx.stroke();
  }

  // ── Ground line
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(padL, gndY); ctx.lineTo(W - padR, gndY); ctx.stroke();

  // ── Canvas (화폭) — blue vertical line at P
  const px = toX(OP);
  const cvTop = toY(H * 1.7);
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(px, gndY + 6); ctx.lineTo(px, cvTop); ctx.stroke();
  // shade canvas area
  ctx.fillStyle = 'rgba(56,189,248,0.07)';
  ctx.fillRect(px - 1, cvTop, 3, gndY - cvTop + 6);

  // label P
  ctx.fillStyle = '#7dd3fc';
  ctx.font = 'bold 13px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('P', px, gndY + 22);
  ctx.fillText('화폭', px, cvTop - 8);

  // ── Trees
  OBs.forEach((OBi, i) => {
    const tx = toX(OBi);
    const th = H * sc;  // tree height in pixels

    // trunk
    ctx.strokeStyle = '#92400e';
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(tx, gndY); ctx.lineTo(tx, toY(H)); ctx.stroke();

    // canopy
    const cr = Math.max(7, th * 0.18);
    const cy_top = toY(H) - cr * 0.3;
    ctx.fillStyle = ['#16a34a','#15803d','#14532d'][i];
    ctx.strokeStyle = ['#4ade80','#86efac','#bbf7d0'][i];
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(tx, cy_top, cr, 0, Math.PI*2);
    ctx.fill(); ctx.stroke();

    // A_i label
    ctx.fillStyle = '#e2e8f0';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`A${i+1}`, tx, cy_top - cr - 4);

    // B_i label (below ground)
    ctx.fillStyle = '#64748b';
    ctx.fillText(`B${i+1}`, tx, gndY + 22);
  });

  // ── Projection lines & points on canvas
  const projColors = COLORS;
  const projLabels = ['Q','R','S'];
  OBs.forEach((OBi, i) => {
    const pProj = calcProj(OP, OBi, H);
    const tx = toX(OBi);
    const ty = toY(H); // tree top y
    const projY = toY(pProj);

    // dashed ray from O=(0,0) to tree top
    ctx.strokeStyle = projColors[i];
    ctx.lineWidth = 1.5;
    ctx.setLineDash([5, 4]);
    ctx.beginPath();
    ctx.moveTo(toX(0), toY(0));
    ctx.lineTo(tx, ty);
    ctx.stroke();
    ctx.setLineDash([]);

    // dot on canvas
    ctx.fillStyle = projColors[i];
    ctx.beginPath();
    ctx.arc(px, projY, 5, 0, Math.PI*2);
    ctx.fill();

    // colored segment on canvas line showing height
    ctx.strokeStyle = projColors[i];
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(px, gndY); ctx.lineTo(px, projY); ctx.stroke();

    // label
    ctx.fillStyle = projColors[i];
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(projLabels[i], px + 7, projY + 4);
  });

  // ── Eye O
  ctx.fillStyle = '#facc15';
  ctx.beginPath(); ctx.arc(toX(0), toY(0), 6, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = '#facc15';
  ctx.font = 'bold 13px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('O', toX(0), toY(0) + 22);
  // eye emoji above
  ctx.font = '16px sans-serif';
  ctx.fillText('👁', toX(0), toY(0) - 10);
}

// ── Painter's canvas view ──────────────────────────────────────────────────
function drawPainter(p) {
  const {OP, OB1, gap, H} = p;
  const W = cvP.offsetWidth || 860;
  cvP.width = W;
  const CH = 200;
  const ctx = ctxP;
  ctx.clearRect(0, 0, W, CH);

  // background sky
  const skyGrad = ctx.createLinearGradient(0, 0, 0, CH * 0.65);
  skyGrad.addColorStop(0, '#1e3a5f');
  skyGrad.addColorStop(1, '#0d2137');
  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, W, CH * 0.65);

  // ground
  ctx.fillStyle = '#1a2e1a';
  ctx.fillRect(0, CH * 0.65, W, CH * 0.35);

  // horizon
  ctx.strokeStyle = '#1e3a5f';
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 6]);
  ctx.beginPath(); ctx.moveTo(0, CH * 0.65); ctx.lineTo(W, CH * 0.65); ctx.stroke();
  ctx.setLineDash([]);

  const N = 3;
  const OBs = Array.from({length:N}, (_,i) => OB1 + i*gap);
  const projs = OBs.map(OBi => calcProj(OP, OBi, H));
  const maxP = projs[0];
  const maxBarH = CH * 0.55;
  const scale = maxBarH / maxP;

  const xs = [W*0.2, W*0.45, W*0.7];
  const treeColors = [['#16a34a','#4ade80'],['#15803d','#86efac'],['#14532d','#bbf7d0']];
  const projColors = [COLORS[0], COLORS[1], COLORS[2]];
  const gndY = CH * 0.65;

  projs.forEach((pj, i) => {
    const barH = pj * scale;
    const tx = xs[i];
    const trunkTop = gndY - barH;
    const cr = Math.max(6, barH * 0.22);

    // height bar on canvas edge (left side strip)
    const stripX = 14;
    ctx.fillStyle = projColors[i] + '55';
    ctx.fillRect(stripX, gndY - barH, 8, barH);
    ctx.fillStyle = projColors[i];
    ctx.font = 'bold 10px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(pj.toFixed(1), stripX + 10, gndY - barH + 4);

    // trunk
    ctx.strokeStyle = '#92400e';
    ctx.lineWidth = Math.max(2, barH * 0.07);
    ctx.beginPath(); ctx.moveTo(tx, gndY); ctx.lineTo(tx, trunkTop); ctx.stroke();

    // canopy
    ctx.fillStyle = treeColors[i][0];
    ctx.strokeStyle = treeColors[i][1];
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(tx, trunkTop - cr * 0.3, cr, 0, Math.PI*2);
    ctx.fill(); ctx.stroke();

    // label
    ctx.fillStyle = '#94a3b8';
    ctx.font = `${Math.max(9, 11 - i)}px sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillText(`A${i+1}`, tx, trunkTop - cr - 5);
  });

  // vanishing point hint
  ctx.fillStyle = '#fbbf2488';
  ctx.beginPath(); ctx.arc(W * 0.85, gndY, 4, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = '#64748b';
  ctx.font = '10px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('소실점 →', W * 0.85, gndY - 10);
}

// ── Results & harmony panel ────────────────────────────────────────────────
function updateResults(p) {
  const {OP, OB1, gap, H} = p;
  const OBs = [OB1, OB1+gap, OB1+2*gap];
  const projs = OBs.map(OBi => calcProj(OP, OBi, H));
  const [PQ, PR, PS] = projs;
  const labels = ['PQ','PR','PS'];
  const colors = [COLORS[0], COLORS[1], COLORS[2]];
  const valEls = ['val-PQ','val-PR','val-PS'];
  const subEls = ['sub-PQ','sub-PR','sub-PS'];

  projs.forEach((pj, i) => {
    document.getElementById(valEls[i]).textContent = pj.toFixed(2);
    document.getElementById(subEls[i]).textContent =
      `= PQ × ${(OB1/OBs[i]).toFixed(3)}   (OB₁/OB${i+1})`;
  });

  // Harmony rows: show 1/PQ, 1/PR, 1/PS
  const invs = projs.map(pj => 1/pj);
  const diffs = [invs[1]-invs[0], invs[2]-invs[1]];
  const isArith = Math.abs(diffs[0]-diffs[1]) < 1e-9;

  const harmRow = document.getElementById('harm-row');
  harmRow.innerHTML = '';

  invs.forEach((inv, i) => {
    if (i > 0) {
      const arrow = document.createElement('span');
      arrow.className = 'arrow';
      const diff = diffs[i-1];
      arrow.innerHTML = `<span style="font-size:0.7rem;color:${isArith?'#4ade80':'#fbbf24'}">+${diff.toFixed(4)}</span><br>→`;
      harmRow.appendChild(arrow);
    }
    const el = document.createElement('div');
    el.className = 'harm-item';
    el.innerHTML = `<div class="name" style="color:${colors[i]}">1/${labels[i]}</div>
      <div class="num" style="color:${colors[i]}">${inv.toFixed(4)}</div>`;
    harmRow.appendChild(el);
  });

  const note = document.getElementById('harm-note');
  if (isArith) {
    const d = diffs[0];
    note.innerHTML = `<span class="hi">✅ 공차 = ${d.toFixed(4)}</span> 로 역수들이 등차수열 →
      <span class="hi">PQ, PR, PS 는 조화수열!</span><br>
      <span style="color:#7dd3fc">공식: P_n = <b>A₁B₁ × OP / OB_n</b>  이므로, OB_n 이 등차수열이면 1/P_n 도 등차수열</span>`;
  } else {
    note.innerHTML = `<span class="warn">역수 차이: ${diffs[0].toFixed(6)} vs ${diffs[1].toFixed(6)}</span> — 부동소수점 오차 확인`;
  }
}

// ── N-trees challenge ──────────────────────────────────────────────────────
function updateNTrees(p) {
  const {OP, OB1, gap, H, N} = p;
  const barsEl = document.getElementById('ntree-bars');
  barsEl.innerHTML = '';

  const projs = Array.from({length:N}, (_,i) => calcProj(OP, OB1 + i*gap, H));
  const maxP = projs[0];
  const maxBarPx = 100;

  projs.forEach((pj, i) => {
    const barPx = (pj / maxP) * maxBarPx;
    const hue = Math.round(210 + i * (330/N));
    const wrap = document.createElement('div');
    wrap.className = 'ntree-bar-wrap';
    wrap.innerHTML = `
      <div style="font-size:0.62rem;color:#94a3b8;margin-bottom:2px;">${pj.toFixed(1)}</div>
      <div class="ntree-bar" style="height:${barPx}px; background:hsl(${hue},70%,55%);"></div>
      <div class="ntree-bar-lbl">P${i+1}</div>`;
    barsEl.appendChild(wrap);
  });

  // Show formula
  const note = document.getElementById('ntree-note');
  note.innerHTML = `<span class="formula">P_n = A₁B₁ × OP / OB_n = ${(H*OP).toFixed(0)} / (${OB1} + ${gap}(n-1))</span><br>
    역수: 1/P_n = (${OB1} + ${gap}(n-1)) / ${(H*OP).toFixed(0)} — 공차 <b style="color:#fbbf24">${(gap/(H*OP)).toFixed(5)}</b> 인 등차수열 ✅`;
}

// ── Main update ────────────────────────────────────────────────────────────
function update() {
  const p = getP();
  document.getElementById('lbl-OP').textContent  = p.OP;
  document.getElementById('lbl-OB1').textContent = p.OB1;
  document.getElementById('lbl-gap').textContent = p.gap;
  document.getElementById('lbl-H').textContent   = p.H;
  document.getElementById('lbl-N').textContent   = p.N;

  // Guard: OP < OB1
  if (p.OP >= p.OB1) {
    document.getElementById('sl-OP').value = Math.min(+document.getElementById('sl-OP').value, p.OB1 - 10);
    return update();
  }

  drawDiagram(p);
  drawPainter(p);
  updateResults(p);
  updateNTrees(p);
}

// Bind all sliders
['sl-OP','sl-OB1','sl-gap','sl-H','sl-N'].forEach(id => {
  document.getElementById(id).addEventListener('input', update);
});

window.addEventListener('resize', update);
update();
</script>
</body>
</html>
"""

# ─── Proof tab ────────────────────────────────────────────────────────────────

_HTML_PROOF = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f172a; color: #e2e8f0;
  font-family: 'Segoe UI', 'Noto Sans KR', system-ui, sans-serif;
  font-size: 14px; line-height: 1.5;
}
#app { max-width: 920px; margin: 0 auto; padding: 14px 14px 24px; }

.intro-box {
  background: #1e293b; border-left: 4px solid #4ade80;
  border-radius: 0 10px 10px 0;
  padding: 12px 16px; margin-bottom: 14px;
  font-size: 0.82rem; color: #cbd5e1; line-height: 1.7;
}
.intro-box b { color: #4ade80; }
.intro-box .red { color: #f87171; }

.ctrl-panel {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 12px; padding: 14px 16px; margin-bottom: 14px;
}
.ctrl-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 24px; }
@media (max-width: 600px) { .ctrl-grid { grid-template-columns: 1fr; } }
.ctrl-row { display: flex; flex-direction: column; gap: 4px; }
.ctrl-lbl {
  font-size: 0.76rem; color: #7dd3fc; font-weight: 700;
  display: flex; justify-content: space-between;
}
.ctrl-lbl .val { color: #fbbf24; }
input[type=range] { width: 100%; cursor: pointer; accent-color: #38bdf8; height: 5px; }

.diagram-wrap {
  background: #0d1b2a; border: 1px solid #1e3a5f;
  border-radius: 12px; overflow: hidden; margin-bottom: 14px;
}
canvas { display: block; width: 100%; }

.formula-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 8px; margin-bottom: 14px;
}
@media (max-width: 600px) { .formula-grid { grid-template-columns: repeat(2, 1fr); } }
.formula-card {
  border-radius: 10px; padding: 10px 8px 8px;
  text-align: center; border: 1px solid;
}
.formula-card .fc-label { font-size: 0.82rem; font-weight: 800; margin-bottom: 3px; }
.formula-card .fc-fml { font-size: 0.68rem; color: #94a3b8; margin-bottom: 2px; font-family: monospace; line-height: 1.4; }
.formula-card .fc-val { font-size: 1.3rem; font-weight: 800; margin-top: 4px; }

.denom-strip {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 12px; padding: 12px 16px; margin-bottom: 14px;
}
.denom-title { font-size: 0.8rem; font-weight: 800; color: #7dd3fc; margin-bottom: 10px; }
.denom-row { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.denom-item {
  background: #0f172a; border-radius: 8px; padding: 6px 12px;
  font-size: 0.78rem; border: 1px solid #334155;
}
.denom-item .di-lbl { color: #94a3b8; font-size: 0.68rem; }
.denom-item .di-val { font-weight: 800; }
.denom-arrow { color: #475569; font-size: 1rem; }
.denom-note {
  margin-top: 8px; padding: 8px 12px;
  background: #0f172a; border: 1px solid #1e3a5f;
  border-radius: 8px; font-size: 0.75rem; color: #64748b;
}
.denom-note .hi { color: #4ade80; font-weight: 700; }

.proof-panel {
  background: #0f172a; border: 1px solid #1e3a5f;
  border-radius: 12px; overflow: hidden; margin-bottom: 14px;
}
.proof-header {
  padding: 10px 14px; background: #1e293b;
  font-size: 0.88rem; font-weight: 800; color: #86efac;
  border-bottom: 1px solid #334155; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
}
.proof-body { padding: 14px; }
.proof-step { display: flex; gap: 10px; margin-bottom: 14px; }
.proof-step:last-child { margin-bottom: 0; }
.proof-num {
  width: 26px; height: 26px; border-radius: 50%; background: #14532d;
  color: #86efac; font-size: 0.78rem; font-weight: 800;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.proof-content { font-size: 0.8rem; color: #94a3b8; line-height: 1.85; }
.proof-content strong { color: #86efac; }
.proof-content .fml {
  display: inline-block; background: #0d2a1e; border: 1px solid #166534;
  border-radius: 6px; padding: 3px 10px; margin: 2px 0;
  font-family: monospace; font-size: 0.82rem; color: #4ade80;
}

.harm-verify {
  background: #1e0a3c; border: 2px solid #7c3aed;
  border-radius: 12px; padding: 14px 16px;
}
.hv-title { font-size: 0.88rem; font-weight: 800; color: #c4b5fd; margin-bottom: 12px; }
.hv-chain {
  background: #0f172a; border: 1px solid #4c1d95;
  border-radius: 10px; padding: 12px 14px;
  font-size: 0.8rem; color: #a78bfa; line-height: 2.2;
  font-family: monospace;
}
.hv-chain .eq-step { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
.hv-chain .sym { color: #6d28d9; min-width: 16px; }
.hv-chain .expr { color: #e2e8f0; }
.hv-chain .note { color: #64748b; font-size: 0.72rem; font-family: sans-serif; }
.hv-chain .final { color: #4ade80; font-weight: 800; font-size: 0.9rem; }
.hv-numeric {
  margin-top: 10px; padding: 8px 12px;
  background: #0f172a; border: 1px solid #166534;
  border-radius: 8px; font-size: 0.78rem; color: #6ee7b7;
}
.hv-numeric .hi { color: #4ade80; font-weight: 700; }
</style>
</head>
<body>
<div id="app">

<div class="intro-box">
  <b>공간에서 같은 간격 c, 같은 길이 x</b>로 배치된 선분 ①②③④를 눈(A)에서 화면에 투영할 때,<br>
  화면 위 투영 길이 ①'②'③'④'의 <span class="red"><b>분모가 등차수열</b></span>을 이루기 때문에 투영 길이는 <b>조화수열</b>이 됩니다.<br>
  슬라이더로 파라미터를 바꿔가며 이 원리를 직접 확인해보세요.
</div>

<div class="ctrl-panel">
  <div class="ctrl-grid">
    <div class="ctrl-row">
      <div class="ctrl-lbl">a — 눈(A)에서 화면까지 거리
        <span class="val" id="lbl-a">100</span></div>
      <input type="range" id="sl-a" min="40" max="200" value="100" step="2">
    </div>
    <div class="ctrl-row">
      <div class="ctrl-lbl">b — 화면에서 ①까지 거리
        <span class="val" id="lbl-b">80</span></div>
      <input type="range" id="sl-b" min="30" max="200" value="80" step="2">
    </div>
    <div class="ctrl-row">
      <div class="ctrl-lbl">c — 선분 사이 간격
        <span class="val" id="lbl-c">60</span></div>
      <input type="range" id="sl-c" min="20" max="150" value="60" step="2">
    </div>
    <div class="ctrl-row">
      <div class="ctrl-lbl">x — 선분 길이
        <span class="val" id="lbl-x">70</span></div>
      <input type="range" id="sl-x" min="20" max="140" value="70" step="2">
    </div>
  </div>
</div>

<div class="diagram-wrap">
  <canvas id="cvProof" height="320"></canvas>
</div>

<div class="formula-grid" id="fmlGrid"></div>

<div class="denom-strip">
  <div class="denom-title">📐 분모를 나열하면 — 등차수열이므로 역수(투영 길이)는 조화수열</div>
  <div class="denom-row" id="denomRow"></div>
  <div class="denom-note" id="denomNote"></div>
</div>

<div class="proof-panel">
  <div class="proof-header" id="proofToggle">
    🔎 닮음 삼각형으로 공식 유도하기 <span id="proofArrow">▼</span>
  </div>
  <div class="proof-body" id="proofBody" style="display:none">
    <div class="proof-step">
      <div class="proof-num">1</div>
      <div class="proof-content">
        <strong>△ABC ~ △ADE (AA 닮음)</strong><br>
        눈(A)에서 화면(BC)과 선분①(DE)을 향한 시선이 동일 직선이므로 공통각 ∠A를 공유.<br>
        BC ∥ DE (둘 다 화면과 평행) → 동위각 ∠ABC = ∠ADE<br>
        ∴ AA 닮음
      </div>
    </div>
    <div class="proof-step">
      <div class="proof-num">2</div>
      <div class="proof-content">
        <strong>닮음비 a : (a+b) 도출</strong><br>
        A에서 화면까지 수평 거리 = a &nbsp;|&nbsp; A에서 ① 아래까지 수평 거리 = a+b<br>
        <span class="fml">닮음비 = AC : AE = a : (a+b)</span>
      </div>
    </div>
    <div class="proof-step">
      <div class="proof-num">3</div>
      <div class="proof-content">
        <strong>①' = ax/(a+b) 도출</strong><br>
        <span class="fml">①' = BC = DE × a/(a+b) = x · a/(a+b) = ax/(a+b)</span><br>
        마찬가지로 n번째 선분의 투영:<br>
        <span class="fml">n번째' = ax / (a + b + (n−1)c)</span>
      </div>
    </div>
    <div class="proof-step">
      <div class="proof-num">4</div>
      <div class="proof-content">
        <strong>분모 분석</strong><br>
        분모: a+b, &nbsp; a+b+c, &nbsp; a+b+2c, &nbsp; a+b+3c, &nbsp; …<br>
        → 첫째항 a+b, 공차 c인 <strong style="color:#fbbf24">등차수열</strong><br>
        → 분자 ax는 상수, 분모가 등차수열 → 투영 길이는 <strong>조화수열</strong> ✓
      </div>
    </div>
  </div>
</div>

<div class="harm-verify">
  <div class="hv-title">✅ 조화평균 검증 — 수식으로 확인</div>
  <div class="hv-chain">
    <div class="eq-step">
      <span class="sym"></span>
      <span class="expr">조화평균(①', ③') = 2 ÷ (1/①' + 1/③')</span>
    </div>
    <div class="eq-step">
      <span class="sym">=</span>
      <span class="expr">2 ÷ ( (a+b)/ax + (a+b+2c)/ax )</span>
    </div>
    <div class="eq-step">
      <span class="sym">=</span>
      <span class="expr">2ax ÷ ( (a+b) + (a+b+2c) )</span>
    </div>
    <div class="eq-step">
      <span class="sym">=</span>
      <span class="expr">2ax ÷ (2a+2b+2c)</span>
    </div>
    <div class="eq-step">
      <span class="sym">=</span>
      <span class="final">ax/(a+b+c) = ②'</span>
      <span class="note">← 슬라이더를 어떻게 바꿔도 항상 성립!</span>
    </div>
  </div>
  <div class="hv-numeric" id="hvNum"></div>
</div>

</div><!-- #app -->

<script>
const COLORS  = ['#f472b6','#a78bfa','#60a5fa','#34d399'];
const LABELS  = ['①','②','③','④'];
const CV      = document.getElementById('cvProof');
const CTX     = CV.getContext('2d');

function getP() {
  return {
    a: +document.getElementById('sl-a').value,
    b: +document.getElementById('sl-b').value,
    c: +document.getElementById('sl-c').value,
    x: +document.getElementById('sl-x').value,
  };
}
function proj(a,b,c,x,n){ return a*x/(a+b+n*c); }

// ── Diagram ────────────────────────────────────────────────────────────────
function drawDiagram({a,b,c,x}){
  const W = CV.offsetWidth || 860;
  CV.width = W;
  const CH = 320;

  // Eye height fixed at 2×x or minimum 140 scene units
  const eyeH = Math.max(x * 2.0, 140);

  const padL=28, padR=28, padT=36, padB=48;
  const sceneW = a + b + 3*c + a*0.08;
  const sceneH = eyeH + x*0.3;
  const sc = Math.min((W-padL-padR)/sceneW, (CH-padT-padB)/sceneH);

  // canvas coords: A' at right (scene x=0), scene x increases leftward
  const tX = sx => W - padR - sx*sc;
  const tY = sy => CH - padB - sy*sc;

  const floorY = tY(0);
  const Ax = tX(0);
  const Ay = tY(eyeH);
  const ppX = tX(a);   // picture plane

  // object foot x-positions and top y
  const objXs = [0,1,2,3].map(i => tX(a+b+i*c));
  const topY  = tY(x);

  // projection ①' ②' ③' ④' y on picture plane
  const projYs = objXs.map(ox => {
    const t = (ppX - Ax) / (ox - Ax);
    return Ay + t*(topY - Ay);
  });

  CTX.clearRect(0,0,W,CH);
  CTX.fillStyle = '#0d1b2a';
  CTX.fillRect(0,0,W,CH);

  // Light grid
  CTX.strokeStyle = '#1e3a5f'; CTX.lineWidth = 0.8;
  for(let gy=padT; gy<CH-padB; gy+=50){
    CTX.beginPath(); CTX.moveTo(padL,gy); CTX.lineTo(W-padR,gy); CTX.stroke();
  }

  // ── Similar triangle highlights (drawn first, behind everything) ──────────
  // Big triangle △ADE: A, top of ①, foot of ①
  CTX.fillStyle   = 'rgba(250,204,21,0.07)';
  CTX.strokeStyle = 'rgba(250,204,21,0.35)';
  CTX.lineWidth = 1.5; CTX.setLineDash([5,4]);
  CTX.beginPath();
  CTX.moveTo(Ax, Ay);
  CTX.lineTo(objXs[0], topY);
  CTX.lineTo(objXs[0], floorY);
  CTX.lineTo(Ax, floorY);
  CTX.closePath(); CTX.fill(); CTX.stroke();
  CTX.setLineDash([]);

  // Small triangle △ABC: A, ①' on canvas, foot of canvas
  CTX.fillStyle   = 'rgba(56,189,248,0.09)';
  CTX.strokeStyle = 'rgba(56,189,248,0.38)';
  CTX.lineWidth = 1.5; CTX.setLineDash([5,4]);
  CTX.beginPath();
  CTX.moveTo(Ax, Ay);
  CTX.lineTo(ppX, projYs[0]);
  CTX.lineTo(ppX, floorY);
  CTX.lineTo(Ax, floorY);
  CTX.closePath(); CTX.fill(); CTX.stroke();
  CTX.setLineDash([]);

  // Triangle labels
  CTX.font = 'italic bold 11px "Segoe UI",sans-serif'; CTX.textAlign='left';
  CTX.fillStyle='rgba(250,204,21,0.75)';
  CTX.fillText('△ADE', objXs[0]+5, Ay+18);
  CTX.fillStyle='rgba(56,189,248,0.75)';
  CTX.fillText('△ABC', ppX+6, Ay+18);

  // ── Floor line ────────────────────────────────────────────────────────────
  CTX.strokeStyle='#334155'; CTX.lineWidth=2;
  CTX.beginPath(); CTX.moveTo(padL,floorY); CTX.lineTo(W-padR,floorY); CTX.stroke();

  // Right-angle markers at floor
  function rightAngle(cx, cy, size=8) {
    CTX.strokeStyle='#475569'; CTX.lineWidth=1.5;
    CTX.beginPath();
    CTX.moveTo(cx-size,cy); CTX.lineTo(cx-size,cy-size); CTX.lineTo(cx,cy-size);
    CTX.stroke();
  }
  rightAngle(ppX, floorY);
  rightAngle(objXs[0], floorY);

  // ── Floor distance annotations ─────────────────────────────────────────────
  function brace(x1,x2,y,lbl,col){
    CTX.strokeStyle=col; CTX.lineWidth=1.5;
    CTX.beginPath(); CTX.moveTo(x1,y); CTX.lineTo(x2,y); CTX.stroke();
    [x1,x2].forEach(xp=>{
      CTX.beginPath(); CTX.moveTo(xp,y-5); CTX.lineTo(xp,y+5); CTX.stroke();
    });
    CTX.fillStyle=col; CTX.font='bold 12px "Segoe UI",sans-serif';
    CTX.textAlign='center'; CTX.fillText(lbl,(x1+x2)/2,y+15);
  }
  brace(ppX, Ax,             floorY+10, 'a', '#7dd3fc');
  brace(tX(a+b), ppX,        floorY+10, 'b', '#86efac');
  brace(tX(a+b+c), tX(a+b),  floorY+10, 'c', '#fbbf24');
  brace(tX(a+b+2*c), tX(a+b+c), floorY+10, 'c', '#fbbf24');
  brace(tX(a+b+3*c), tX(a+b+2*c), floorY+10, 'c', '#fbbf24');

  // ── Picture plane ──────────────────────────────────────────────────────────
  const ppTop = Math.min(projYs[0]-8, Ay+20);
  CTX.strokeStyle='#38bdf8'; CTX.lineWidth=3.5;
  CTX.beginPath(); CTX.moveTo(ppX, floorY+4); CTX.lineTo(ppX, ppTop); CTX.stroke();
  CTX.fillStyle='rgba(56,189,248,0.08)';
  CTX.fillRect(ppX-2, ppTop, 4, floorY-ppTop+4);

  // ── Objects ①②③④ ─────────────────────────────────────────────────────────
  [0,1,2,3].forEach(i=>{
    const fx=objXs[i];
    CTX.strokeStyle=COLORS[i]; CTX.lineWidth=3;
    CTX.beginPath(); CTX.moveTo(fx,floorY); CTX.lineTo(fx,topY); CTX.stroke();
    // arrowhead
    CTX.fillStyle=COLORS[i];
    CTX.beginPath(); CTX.moveTo(fx,topY-9); CTX.lineTo(fx-5,topY); CTX.lineTo(fx+5,topY); CTX.closePath(); CTX.fill();
    // circle number labels
    const lblY = topY - 18;
    CTX.beginPath(); CTX.arc(fx, lblY-2, 11, 0, Math.PI*2);
    CTX.fillStyle='rgba(0,0,0,0.6)'; CTX.fill();
    CTX.strokeStyle=COLORS[i]; CTX.lineWidth=1.5; CTX.stroke();
    CTX.fillStyle=COLORS[i]; CTX.font='bold 11px sans-serif'; CTX.textAlign='center';
    CTX.fillText(LABELS[i], fx, lblY+2);
  });

  // x-length double-arrow on first object
  const xAnnX = objXs[0]+14;
  CTX.strokeStyle='rgba(251,191,36,0.7)'; CTX.lineWidth=1;
  CTX.beginPath(); CTX.moveTo(xAnnX, floorY); CTX.lineTo(xAnnX, topY); CTX.stroke();
  CTX.fillStyle='#fbbf24'; CTX.font='bold 12px "Segoe UI",sans-serif'; CTX.textAlign='left';
  CTX.fillText('x', xAnnX+4, (floorY+topY)/2+5);

  // ── Projection rays ─────────────────────────────────────────────────────────
  [0,1,2,3].forEach(i=>{
    CTX.strokeStyle=COLORS[i]+'99'; CTX.lineWidth=1.2;
    CTX.setLineDash([4,4]);
    CTX.beginPath(); CTX.moveTo(Ax,Ay); CTX.lineTo(objXs[i],topY); CTX.stroke();
    CTX.setLineDash([]);
  });

  // ── Projection marks on canvas ─────────────────────────────────────────────
  [0,1,2,3].forEach(i=>{
    const py=projYs[i];
    CTX.strokeStyle=COLORS[i]; CTX.lineWidth=3;
    CTX.beginPath(); CTX.moveTo(ppX, floorY); CTX.lineTo(ppX, py); CTX.stroke();
    CTX.fillStyle=COLORS[i];
    CTX.beginPath(); CTX.arc(ppX, py, 4, 0, Math.PI*2); CTX.fill();
    CTX.font='bold 11px sans-serif'; CTX.textAlign='left';
    CTX.fillText(LABELS[i]+"'", ppX+7, py+4);
  });

  // ── ①' label with size indicator ──────────────────────────────────────────
  CTX.strokeStyle='rgba(244,114,182,0.5)'; CTX.lineWidth=1;
  CTX.beginPath(); CTX.moveTo(ppX-10,floorY); CTX.lineTo(ppX-10,projYs[0]); CTX.stroke();
  CTX.fillStyle='#f472b6'; CTX.font='bold 10px sans-serif'; CTX.textAlign='right';
  CTX.fillText("①'", ppX-12, (floorY+projYs[0])/2+4);

  // ── Eye A ──────────────────────────────────────────────────────────────────
  CTX.fillStyle='#facc15';
  CTX.beginPath(); CTX.arc(Ax, Ay, 8, 0, Math.PI*2); CTX.fill();
  CTX.fillStyle='#0f172a'; CTX.font='bold 9px sans-serif'; CTX.textAlign='center';
  CTX.fillText('A', Ax, Ay+3);

  // Dashed vertical A→A'
  CTX.strokeStyle='#475569'; CTX.lineWidth=1; CTX.setLineDash([3,4]);
  CTX.beginPath(); CTX.moveTo(Ax,Ay+8); CTX.lineTo(Ax,floorY); CTX.stroke();
  CTX.setLineDash([]);

  // A, A', D, E, B, C labels near their positions
  function txtShadow(txt,x,y,col,align='center'){
    CTX.font='bold 12px "Segoe UI",sans-serif'; CTX.textAlign=align;
    CTX.fillStyle='rgba(0,0,0,0.8)';
    CTX.fillText(txt,x+1,y+1);
    CTX.fillStyle=col;
    CTX.fillText(txt,x,y);
  }
  txtShadow("A'", Ax, floorY+24, '#7dd3fc');
  txtShadow('D', objXs[0], topY-30, '#facc15');
  txtShadow('E', objXs[0], floorY-8, '#facc15');
  txtShadow('B', ppX-8, projYs[0]-6, '#38bdf8', 'right');
  txtShadow('C', ppX-8, floorY-8, '#38bdf8', 'right');

  // Ratio labels on sides
  CTX.fillStyle='rgba(250,204,21,0.8)'; CTX.font='italic 11px sans-serif';
  CTX.textAlign='center';
  CTX.fillText('a+b', (Ax+objXs[0])/2, floorY-6);
  CTX.fillStyle='rgba(56,189,248,0.8)';
  CTX.fillText('a', (Ax+ppX)/2, floorY-6);
}

// ── Formula cards ──────────────────────────────────────────────────────────
function updateFormulas({a,b,c,x}){
  const grid = document.getElementById('fmlGrid');
  const denoms = [0,1,2,3].map(i=>a+b+i*c);
  const vals   = denoms.map(d=>a*x/d);
  const bg   = ['rgba(244,114,182,0.1)','rgba(167,139,250,0.1)','rgba(96,165,250,0.1)','rgba(52,211,153,0.1)'];
  const bd   = ['#f472b6','#a78bfa','#60a5fa','#34d399'];
  const suffixes = ['b)','b+c)','b+2c)','b+3c)'];

  grid.innerHTML = [0,1,2,3].map(i=>`
    <div class="formula-card" style="background:${bg[i]};border-color:${bd[i]}">
      <div class="fc-label" style="color:${bd[i]}">${LABELS[i]}' (n=${i+1})</div>
      <div class="fc-fml">= ax/(a+${suffixes[i]}</div>
      <div class="fc-fml" style="color:#64748b">= ${a}·${x}/${denoms[i]}</div>
      <div class="fc-val" style="color:${bd[i]}">${vals[i].toFixed(2)}</div>
    </div>`).join('');
}

// ── Denominator strip ──────────────────────────────────────────────────────
function updateDenoms({a,b,c,x}){
  const denoms = [0,1,2,3].map(i=>a+b+i*c);
  const row = document.getElementById('denomRow');
  row.innerHTML = denoms.map((d,i)=>`
    ${i>0?`<span class="denom-arrow">+${c} →</span>`:''}
    <div class="denom-item">
      <div class="di-lbl" style="color:${COLORS[i]}">분모 ${LABELS[i]}'</div>
      <div class="di-val" style="color:${COLORS[i]}">${d}</div>
    </div>`).join('');
  const diffs = [0,1,2].map(i=>denoms[i+1]-denoms[i]);
  const allSame = diffs.every(d=>d===diffs[0]);
  document.getElementById('denomNote').innerHTML =
    `공차: <span class="hi">${diffs[0]}</span> ${allSame?'(등차수열 ✅)':'—'} &nbsp;|&nbsp; `+
    `분자 ax = ${a}×${x} = <span class="hi">${a*x}</span> (상수) → 투영 길이는 <span class="hi">조화수열</span>`;
}

// ── Harmonic numeric ───────────────────────────────────────────────────────
function updateHV({a,b,c,x}){
  const p1 = proj(a,b,c,x,0), p2 = proj(a,b,c,x,1), p3 = proj(a,b,c,x,2);
  const hm = 2*p1*p3/(p1+p3);
  document.getElementById('hvNum').innerHTML =
    `수치 확인 (현재 a=${a}, b=${b}, c=${c}, x=${x}):<br>`+
    `①'=${p1.toFixed(3)}, ②'=${p2.toFixed(3)}, ③'=${p3.toFixed(3)}<br>`+
    `조화평균(①',③') = 2×${p1.toFixed(3)}×${p3.toFixed(3)}/(${p1.toFixed(3)}+${p3.toFixed(3)}) = `+
    `<span class="hi">${hm.toFixed(3)}</span> ≈ ②' = <span class="hi">${p2.toFixed(3)}</span>`;
}

// ── Main update ────────────────────────────────────────────────────────────
function update(){
  const p = getP();
  document.getElementById('lbl-a').textContent = p.a;
  document.getElementById('lbl-b').textContent = p.b;
  document.getElementById('lbl-c').textContent = p.c;
  document.getElementById('lbl-x').textContent = p.x;
  drawDiagram(p);
  updateFormulas(p);
  updateDenoms(p);
  updateHV(p);
}

['sl-a','sl-b','sl-c','sl-x'].forEach(id=>{
  document.getElementById(id).addEventListener('input', update);
});
document.getElementById('proofToggle').addEventListener('click',()=>{
  const b = document.getElementById('proofBody');
  const a = document.getElementById('proofArrow');
  const open = b.style.display==='block';
  b.style.display = open?'none':'block';
  a.textContent = open?'▼':'▲';
});
window.addEventListener('resize', update);
update();
</script>
</body>
</html>
"""

# ─── Painting tab template ────────────────────────────────────────────────────

_PAINTING_TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f172a; color: #e2e8f0;
  font-family: 'Segoe UI', 'Noto Sans KR', sans-serif;
  user-select: none; -webkit-user-select: none;
}
#app { max-width: 940px; margin: 0 auto; padding: 10px; }

.painting-intro {
  background: #1e293b; border-left: 4px solid #a78bfa;
  border-radius: 0 10px 10px 0;
  padding: 10px 14px; margin-bottom: 10px;
  font-size: 0.82rem; color: #cbd5e1; line-height: 1.7;
}
.painting-intro strong { color: #e2e8f0; }
.painting-intro span { color: #94a3b8; }

.toolbar {
  background: #1e293b; border: 1px solid #334155; border-radius: 12px;
  padding: 8px 12px; margin-bottom: 8px;
  display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
}
.tool-group { display: flex; align-items: center; gap: 5px; }
.vsep { width: 1px; height: 26px; background: #334155; flex-shrink: 0; }
.tl-btn {
  padding: 5px 11px; border-radius: 7px; border: 1.5px solid #334155;
  background: #0f172a; color: #94a3b8; cursor: pointer;
  font-size: 0.77rem; font-weight: 700; transition: all .15s; white-space: nowrap;
}
.tl-btn.active { background: #78350f; color: #fde68a; border-color: #f59e0b; }
#btnRuler.active { background: #1e3a5f; color: #bfdbfe; border-color: #3b82f6; }
.tl-btn:hover:not(.active) { border-color: #475569; color: #cbd5e1; }
.tl-lbl { font-size: 0.72rem; color: #64748b; white-space: nowrap; }
.cswatch {
  width: 22px; height: 22px; border-radius: 5px; cursor: pointer;
  border: 2px solid transparent; transition: all .1s; flex-shrink: 0;
}
.cswatch.active { border-color: #f8fafc; transform: scale(1.2); box-shadow: 0 0 0 1px #0f172a; }
.cswatch:hover { transform: scale(1.1); }
input[type=color] {
  width: 26px; height: 26px; border: none; padding: 0;
  cursor: pointer; background: none; border-radius: 5px; overflow: hidden;
}
input[type=range] { width: 76px; accent-color: #14b8a6; }
#thickVal { font-size: 0.78rem; color: #5eead4; font-weight: 700; min-width: 14px; }
.act-btn {
  padding: 5px 11px; border-radius: 7px; border: 1.5px solid #334155;
  background: #0f172a; color: #94a3b8; cursor: pointer;
  font-size: 0.77rem; font-weight: 700; transition: all .15s; white-space: nowrap;
}
.act-btn:hover { border-color: #f43f5e; color: #fecdd3; }

.canvas-outer {
  background: #111827; border: 1px solid #334155; border-radius: 10px;
  overflow-x: auto; overflow-y: hidden; line-height: 0; position: relative;
}
#cvs { display: block; cursor: crosshair; touch-action: none; }
.canvas-loading {
  display: none; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%,-50%); font-size: 0.85rem; color: #475569;
}

.ruler-tip {
  margin-top: 6px; padding: 8px 12px; background: #1e3a5f;
  border-left: 3px solid #3b82f6; border-radius: 6px;
  font-size: 0.75rem; color: #93c5fd; display: none;
}
.ruler-color-row {
  display: flex; align-items: center; gap: 6px; margin-top: 8px; flex-wrap: wrap;
}
.ruler-color-lbl { font-size: 0.72rem; color: #64748b; white-space: nowrap; }
.rswatch {
  width: 22px; height: 22px; border-radius: 5px; cursor: pointer;
  border: 2px solid transparent; transition: all .1s; flex-shrink: 0;
}
.rswatch.active { border-color: #f8fafc; transform: scale(1.25); box-shadow: 0 0 0 1px #0f172a; }
.rswatch:hover { transform: scale(1.12); }
input[type=color]#rcpicker {
  width: 26px; height: 26px; border: none; padding: 0;
  cursor: pointer; background: none; border-radius: 5px; overflow: hidden;
}

.steps-panel {
  margin-top: 10px; background: #0f172a;
  border: 1px solid #1e3a5f; border-radius: 10px; overflow: hidden;
}
.steps-header {
  padding: 10px 14px; background: #1e293b;
  font-size: 0.88rem; font-weight: 800; color: #93c5fd;
  border-bottom: 1px solid #334155; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
}
.steps-body { padding: 14px; }
.step { display: flex; gap: 10px; margin-bottom: 12px; }
.step:last-child { margin-bottom: 0; }
.step-num {
  width: 24px; height: 24px; border-radius: 50%; background: #1e3a5f;
  color: #bfdbfe; font-size: 0.75rem; font-weight: 800;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.step-content { font-size: 0.8rem; color: #94a3b8; line-height: 1.7; }
.step-content strong { color: #bfdbfe; }
.step-content em { color: #64748b; font-style: normal; }

/* ── Harmonic checker panel ── */
.harm-panel {
  margin-top: 10px; background: #0d1b2a;
  border: 1px solid #4c1d95; border-radius: 10px; padding: 14px;
}
.harm-panel-title {
  font-size: 0.88rem; font-weight: 800; color: #c4b5fd; margin-bottom: 12px;
}
.harm-input-row {
  display: flex; gap: 8px; align-items: center; margin-bottom: 10px; flex-wrap: wrap;
}
.harm-input-lbl { font-size: 0.78rem; color: #a78bfa; min-width: 200px; }
.harm-input {
  flex: 1; min-width: 200px; max-width: 380px;
  padding: 6px 10px; border-radius: 7px;
  background: #1e0a3c; border: 1.5px solid #6d28d9; color: #ede9fe;
  font-size: 0.82rem; outline: none;
}
.harm-input:focus { border-color: #a78bfa; }
.harm-input::placeholder { color: #4c1d95; }
.harm-btn {
  padding: 7px 18px; border-radius: 7px;
  border: 1.5px solid #7c3aed; background: #2e1065; color: #c4b5fd;
  cursor: pointer; font-size: 0.8rem; font-weight: 700; transition: all .15s;
}
.harm-btn:hover { background: #3b0764; color: #ede9fe; }
.harm-result {
  display: none; margin-top: 12px; padding: 12px;
  background: #1e0a3c; border-radius: 8px;
  font-size: 0.8rem; color: #a78bfa; line-height: 1.9;
}
.harm-result strong { color: #ede9fe; }
.harm-result .ok { color: #4ade80; font-weight: 800; }
.harm-result .warn { color: #fbbf24; font-weight: 800; }
.harm-result .val { color: #f0abfc; font-weight: 700; }
.harm-result table {
  width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 0.77rem;
}
.harm-result th {
  padding: 4px 10px; background: #2e1065; color: #c4b5fd;
  border: 1px solid #4c1d95; text-align: center; font-weight: 700;
}
.harm-result td {
  padding: 4px 10px; border: 1px solid #2e1065;
  text-align: center; color: #e2e8f0;
}
.harm-result tr:nth-child(even) td { background: #1a0a2e; }

.hint-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.hint-btn {
  padding: 5px 14px; border-radius: 7px;
  border: 1.5px solid #334155; background: #0f172a; color: #64748b;
  cursor: pointer; font-size: 0.77rem; font-weight: 700; transition: all .15s;
}
.hint-btn:hover { border-color: #facc15; color: #fde68a; }
.hint-box {
  display: none; margin-top: 8px; padding: 10px 14px;
  background: #1c1c04; border: 1px solid #854d0e;
  border-radius: 8px; font-size: 0.78rem; color: #fde68a; line-height: 1.9;
}
.hint-box strong { color: #facc15; }

@media (max-width: 600px) {
  .vsep { display: none; }
  .toolbar { gap: 6px; padding: 6px 8px; }
  .harm-input-lbl { min-width: unset; width: 100%; }
}
</style>
</head>
<body>
<div id="app">

<div class="painting-intro">
  🎨 <strong>그리스도의 채찍질</strong> — 피에로 델라 프란체스카 (~1455)<br>
  <span>자 도구로 바닥 타일 또는 천장 격자의 간격을 측정하고, 아래 조화수열 확인기로 검증해보세요.</span>
</div>

<div class="toolbar">
  <div class="tool-group">
    <button class="tl-btn active" id="btnLine">📏 직선</button>
    <button class="tl-btn" id="btnFree">✏️ 자유선</button>
    <button class="tl-btn" id="btnRuler">📐 자</button>
    <button class="tl-btn" id="btnEraser">🧹 지우개</button>
  </div>
  <div class="vsep"></div>
  <div class="tool-group">
    <span class="tl-lbl">색상</span>
    <div class="cswatch active" style="background:#ef4444" data-c="#ef4444"></div>
    <div class="cswatch" style="background:#f97316" data-c="#f97316"></div>
    <div class="cswatch" style="background:#facc15" data-c="#facc15"></div>
    <div class="cswatch" style="background:#22c55e" data-c="#22c55e"></div>
    <div class="cswatch" style="background:#38bdf8" data-c="#38bdf8"></div>
    <div class="cswatch" style="background:#a78bfa" data-c="#a78bfa"></div>
    <div class="cswatch" style="background:#f8fafc" data-c="#f8fafc"></div>
    <input type="color" id="cpicker" value="#ef4444" title="색상 직접 선택">
  </div>
  <div class="vsep"></div>
  <div class="tool-group">
    <span class="tl-lbl">두께</span>
    <input type="range" id="thickSlider" min="1" max="12" value="2">
    <span id="thickVal">2</span>
  </div>
  <div class="vsep"></div>
  <div class="tool-group">
    <button class="act-btn" id="btnUndo">↩ 되돌리기</button>
    <button class="act-btn" id="btnClear">🗑 모두 지우기</button>
  </div>
</div>

<div class="ruler-tip" id="rulerTip">
  📐 <strong>자 도구</strong>: 드래그하면 자가 생기고 픽셀 수가 표시됩니다. 끝점(원)을 드래그해 조정, 우클릭으로 삭제.
  <div class="ruler-color-row">
    <span class="ruler-color-lbl">자 색상</span>
    <div class="rswatch active" style="background:#fbbf24" data-rc="#fbbf24"></div>
    <div class="rswatch" style="background:#f8fafc" data-rc="#f8fafc"></div>
    <div class="rswatch" style="background:#f43f5e" data-rc="#f43f5e"></div>
    <div class="rswatch" style="background:#34d399" data-rc="#34d399"></div>
    <div class="rswatch" style="background:#60a5fa" data-rc="#60a5fa"></div>
    <div class="rswatch" style="background:#e879f9" data-rc="#e879f9"></div>
    <input type="color" id="rcpicker" value="#fbbf24" title="자 색상 선택">
  </div>
</div>

<div class="canvas-outer" id="cvsOuter">
  <canvas id="cvs"></canvas>
  <div class="canvas-loading" id="loadMsg">이미지 불러오는 중...</div>
</div>

<!-- Steps panel -->
<div class="steps-panel">
  <div class="steps-header" id="stepsToggle">
    🔍 단계별 안내 <span id="stepsArrow">▼</span>
  </div>
  <div class="steps-body" id="stepsBody" style="display:none">
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-content">
        <strong>📐 자 도구</strong>를 선택하세요. 측정하고 싶은 곳에서 드래그하면 자가 생기고 픽셀 수가 표시됩니다.<br>
        <em>자의 끝점(원)을 드래그해 위치를 정밀하게 조정할 수 있습니다.</em>
      </div>
    </div>
    <div class="step">
      <div class="step-num">2</div>
      <div class="step-content">
        <strong>바닥 타일 높이 측정</strong> — 그림 왼쪽 아래 체크무늬 바닥 타일을 보세요.<br>
        가장 <strong style="color:#f472b6">가까운 줄</strong>·<strong style="color:#a78bfa">중간 줄</strong>·<strong style="color:#60a5fa">먼 줄</strong>의 타일 높이(세로 크기)를 각각 재보세요.<br>
        <em>자 색상을 바꿔가며 3개의 자를 남겨두면 비교하기 편합니다.</em>
      </div>
    </div>
    <div class="step">
      <div class="step-num">3</div>
      <div class="step-content">
        <strong>천장 격자 간격 측정</strong> — 그림 위쪽 천장의 사각 격자(코퍼)를 보세요.<br>
        가까운 것부터 순서대로 <strong>4칸의 높이(세로 간격)</strong>를 각각 측정해보세요.
      </div>
    </div>
    <div class="step">
      <div class="step-num">4</div>
      <div class="step-content">
        아래 <strong>조화수열 확인기</strong>에 측정한 픽셀값을 쉼표로 구분해 입력하면<br>
        조화수열 여부와 각 역수의 공차를 자동으로 계산합니다.
      </div>
    </div>
  </div>
</div>

<!-- Harmonic checker panel -->
<div class="harm-panel">
  <div class="harm-panel-title">🔢 조화수열 확인기</div>
  <div class="harm-input-row">
    <span class="harm-input-lbl">측정값 (쉼표로 구분, 가까운 것부터)</span>
    <input type="text" class="harm-input" id="harmInput" placeholder="예: 95, 116, 148   또는   2.3, 2.6, 3">
    <button class="harm-btn" id="harmBtn">확인 →</button>
  </div>
  <div class="harm-result" id="harmResult"></div>

  <div class="hint-row">
    <button class="hint-btn" id="hintTile">💡 타일 힌트</button>
    <button class="hint-btn" id="hintCeil">💡 천장 힌트</button>
  </div>
  <div class="hint-box" id="hintTileBox">
    PPT에서 실측한 바닥 타일 높이: <strong>3 cm → 2.6 cm → 2.3 cm</strong> (가까운 것 → 먼 것)<br>
    역수: 1/3 ≈ 0.333 &nbsp; 1/2.6 ≈ 0.385 &nbsp; 1/2.3 ≈ 0.435 — 공차 ≈ 0.051 (등차수열 ✅)<br>
    조화평균: 2/(1/2.3 + 1/3) ≈ <strong>2.604 ≈ 2.6</strong>
  </div>
  <div class="hint-box" id="hintCeilBox">
    PPT에서 실측한 천장 격자 간격: <strong>7.75 → 9.5 → 11.75 → 15.25 cm</strong> (가까운 것 → 먼 것 역순, 즉 먼 것부터)<br>
    역수: 1/7.75≈0.129, 1/9.5≈0.105, 1/11.75≈0.085, 1/15.25≈0.066 — 공차 ≈ 0.021 (등차수열 ✅)<br>
    조화평균 체크: 2/(1/7.75+1/11.75) ≈ <strong>9.34 ≈ 9.5</strong> &nbsp; 2/(1/9.5+1/15.25) ≈ <strong>11.71 ≈ 11.75</strong>
  </div>
</div>

</div><!-- #app -->

<script>
(function(){
'use strict';

const CANVAS_W  = 880;
const IMG_MAX_W = 820;
const IMG_PAD_T = 20;
const IMG_PAD_B = 30;
const IMAGE_B64 = "__IMAGE_B64__";
const IMG_MIME  = "image/png";

const S = {
  tool: 'line', color: '#ef4444', thick: 2,
  rulerColor: '#fbbf24',
  drawing: false, sx: 0, sy: 0, freeStroke: null,
  strokes: [], rulers: [], rulerDrag: null, selectedRuler: -1,
  bgImg: null, imgX: 0, imgY: IMG_PAD_T, imgW: 0, imgH: 0,
};

const cvs = document.getElementById('cvs');
const ctx = cvs.getContext('2d');

function pxCoords(e) {
  const r = cvs.getBoundingClientRect();
  const scX = cvs.width / r.width, scY = cvs.height / r.height;
  const src = e.touches ? e.touches[0] : e;
  return { x: (src.clientX - r.left)*scX, y: (src.clientY - r.top)*scY };
}
function dist2(ax,ay,bx,by){ return Math.sqrt((ax-bx)**2+(ay-by)**2); }
function distToSeg(px,py,ax,ay,bx,by){
  const dx=bx-ax,dy=by-ay,len2=dx*dx+dy*dy;
  if(len2<1) return dist2(px,py,ax,ay);
  const t=Math.max(0,Math.min(1,((px-ax)*dx+(py-ay)*dy)/len2));
  return dist2(px,py,ax+t*dx,ay+t*dy);
}
function hitStroke(st,x,y){
  const r=Math.max(8,st.thick/2+5);
  if(!st.pts||st.pts.length<2) return false;
  if(st.type==='line'){const p=st.pts,last=p[p.length-1];return distToSeg(x,y,p[0].x,p[0].y,last.x,last.y)<=r;}
  for(let i=1;i<st.pts.length;i++) if(distToSeg(x,y,st.pts[i-1].x,st.pts[i-1].y,st.pts[i].x,st.pts[i].y)<=r) return true;
  return false;
}
function findHitStroke(arr,x,y){for(let i=arr.length-1;i>=0;i--) if(hitStroke(arr[i],x,y)) return i; return -1;}

async function init(){
  document.getElementById('loadMsg').style.display='block';
  const img=await new Promise(res=>{
    if(!IMAGE_B64){res(null);return;}
    const i=new Image();
    i.onload=()=>res(i); i.onerror=()=>res(null);
    i.src='data:'+IMG_MIME+';base64,'+IMAGE_B64;
  });
  document.getElementById('loadMsg').style.display='none';
  S.bgImg=img;
  if(img){
    const sc=Math.min(IMG_MAX_W/img.naturalWidth,1);
    S.imgW=Math.round(img.naturalWidth*sc);
    S.imgH=Math.round(img.naturalHeight*sc);
    S.imgX=Math.round((CANVAS_W-S.imgW)/2);
  } else {
    S.imgW=IMG_MAX_W; S.imgH=420; S.imgX=Math.round((CANVAS_W-S.imgW)/2);
  }
  cvs.width=CANVAS_W;
  cvs.height=S.imgY+S.imgH+IMG_PAD_B;
  cvs.style.width=CANVAS_W+'px';
  cvs.style.height=cvs.height+'px';
  redraw();
}

function drawStroke(c,st){
  if(!st.pts||st.pts.length<2) return;
  c.save(); c.strokeStyle=st.color; c.lineWidth=st.thick;
  c.lineCap='round'; c.lineJoin='round'; c.beginPath();
  if(st.type==='line'){
    c.moveTo(st.pts[0].x,st.pts[0].y); c.lineTo(st.pts[st.pts.length-1].x,st.pts[st.pts.length-1].y);
  } else {
    c.moveTo(st.pts[0].x,st.pts[0].y);
    for(let i=1;i<st.pts.length;i++) c.lineTo(st.pts[i].x,st.pts[i].y);
  }
  c.stroke(); c.restore();
}

function drawRuler(c,r,selected){
  const dx=r.x2-r.x1,dy=r.y2-r.y1;
  const len=Math.sqrt(dx*dx+dy*dy);
  if(len<3) return;
  const angle=Math.atan2(dy,dx);
  const col=r.color||'#fbbf24';
  c.save(); c.translate(r.x1,r.y1); c.rotate(angle);
  c.shadowColor='rgba(0,0,0,0.85)'; c.shadowBlur=5;
  c.lineCap='square';
  c.strokeStyle='rgba(0,0,0,0.7)'; c.lineWidth=7;
  c.beginPath(); c.moveTo(0,0); c.lineTo(len,0); c.stroke();
  c.strokeStyle=col; c.lineWidth=4;
  c.beginPath(); c.moveTo(0,0); c.lineTo(len,0); c.stroke();
  [0,len].forEach(tx=>{
    c.strokeStyle='rgba(0,0,0,0.7)'; c.lineWidth=5;
    c.beginPath(); c.moveTo(tx,-13); c.lineTo(tx,13); c.stroke();
    c.strokeStyle=col; c.lineWidth=3;
    c.beginPath(); c.moveTo(tx,-13); c.lineTo(tx,13); c.stroke();
  });
  c.shadowBlur=0;
  for(let t=0;t<=len;t+=20){
    const h=t%100===0?10:t%50===0?7:4;
    c.strokeStyle='rgba(0,0,0,0.6)'; c.lineWidth=3;
    c.beginPath(); c.moveTo(t,0); c.lineTo(t,h); c.stroke();
    c.strokeStyle=col; c.lineWidth=1.5;
    c.beginPath(); c.moveTo(t,0); c.lineTo(t,h); c.stroke();
  }
  c.save();
  const flip=Math.abs(angle)>Math.PI/2;
  c.translate(len/2,0);
  if(flip) c.rotate(Math.PI);
  const label=Math.round(len)+' px';
  c.font='bold 14px "Segoe UI",sans-serif';
  const tw=c.measureText(label).width;
  c.fillStyle='rgba(0,0,0,0.75)'; c.beginPath();
  c.roundRect(-tw/2-6,-32,tw+12,20,5); c.fill();
  c.fillStyle=col; c.textAlign='center'; c.textBaseline='alphabetic';
  c.fillText(label,0,-15);
  c.restore(); c.restore();
  [[r.x1,r.y1],[r.x2,r.y2]].forEach(([x,y])=>{
    c.beginPath(); c.arc(x,y,9,0,Math.PI*2);
    c.fillStyle='rgba(0,0,0,0.6)'; c.fill();
    c.beginPath(); c.arc(x,y,7,0,Math.PI*2);
    c.fillStyle=selected?'#f97316':col; c.fill();
    c.beginPath(); c.arc(x,y,7,0,Math.PI*2);
    c.strokeStyle='#f8fafc'; c.lineWidth=1.5; c.stroke();
  });
}

function redraw(previewStroke,previewRuler){
  ctx.clearRect(0,0,cvs.width,cvs.height);
  ctx.fillStyle='#111827'; ctx.fillRect(0,0,cvs.width,cvs.height);
  if(S.bgImg) ctx.drawImage(S.bgImg,S.imgX,S.imgY,S.imgW,S.imgH);
  else {
    ctx.fillStyle='#1e293b'; ctx.fillRect(S.imgX,S.imgY,S.imgW,S.imgH||420);
    ctx.fillStyle='#475569'; ctx.font='bold 16px Segoe UI'; ctx.textAlign='center';
    ctx.fillText('이미지를 불러올 수 없습니다',CANVAS_W/2,S.imgY+210);
    ctx.textAlign='left';
  }
  ctx.save(); ctx.strokeStyle='#334155'; ctx.lineWidth=1;
  ctx.setLineDash([5,5]); ctx.strokeRect(S.imgX,S.imgY,S.imgW,S.imgH); ctx.restore();
  S.strokes.forEach(st=>drawStroke(ctx,st));
  if(previewStroke){ctx.globalAlpha=0.75; drawStroke(ctx,previewStroke); ctx.globalAlpha=1;}
  S.rulers.forEach((r,i)=>drawRuler(ctx,r,i===S.selectedRuler));
  if(previewRuler){ctx.globalAlpha=0.8; drawRuler(ctx,previewRuler,false); ctx.globalAlpha=1;}
}

function hitRuler(x,y){
  for(let i=S.rulers.length-1;i>=0;i--){
    const r=S.rulers[i];
    if(dist2(x,y,r.x1,r.y1)<10) return {idx:i,type:'ep1'};
    if(dist2(x,y,r.x2,r.y2)<10) return {idx:i,type:'ep2'};
    if(distToSeg(x,y,r.x1,r.y1,r.x2,r.y2)<8) return {idx:i,type:'body'};
  }
  return null;
}

cvs.addEventListener('pointerdown',e=>{
  e.preventDefault(); const {x,y}=pxCoords(e);
  if(S.tool==='ruler'){
    const hit=hitRuler(x,y);
    if(hit){
      S.selectedRuler=hit.idx;
      const r=S.rulers[hit.idx];
      S.rulerDrag={type:hit.type,idx:hit.idx,ox:x,oy:y,ox1:r.x1,oy1:r.y1,ox2:r.x2,oy2:r.y2};
    } else {
      S.selectedRuler=-1; S.rulerDrag={type:'new',x1:x,y1:y};
    }
    cvs.setPointerCapture(e.pointerId); redraw(); return;
  }
  S.selectedRuler=-1; S.drawing=true; S.sx=x; S.sy=y;
  if(S.tool==='eraser'){
    const idx=findHitStroke(S.strokes,x,y);
    if(idx!==-1){S.strokes.splice(idx,1);redraw();} S.drawing=false; return;
  }
  if(S.tool==='free'){
    S.freeStroke={type:'free',color:S.color,thick:S.thick,pts:[{x,y}]};
    S.strokes.push(S.freeStroke);
  }
  cvs.setPointerCapture(e.pointerId);
});

cvs.addEventListener('pointermove',e=>{
  const {x,y}=pxCoords(e);
  if(S.tool==='ruler'){
    if(S.rulerDrag){
      const d=S.rulerDrag;
      if(d.type==='new'){
        redraw(null,{x1:d.x1,y1:d.y1,x2:x,y2:y,color:S.rulerColor});
      } else {
        const r=S.rulers[d.idx]; const dx=x-d.ox,dy=y-d.oy;
        if(d.type==='ep1'){r.x1=d.ox1+dx;r.y1=d.oy1+dy;}
        else if(d.type==='ep2'){r.x2=d.ox2+dx;r.y2=d.oy2+dy;}
        else{r.x1=d.ox1+dx;r.y1=d.oy1+dy;r.x2=d.ox2+dx;r.y2=d.oy2+dy;}
        redraw();
      }
    } else {
      const hit=hitRuler(x,y);
      cvs.style.cursor=hit?(hit.type.startsWith('ep')?'grab':'move'):'crosshair';
    }
    return;
  }
  if(!S.drawing) return;
  e.preventDefault();
  if(S.tool==='line') redraw({type:'line',color:S.color,thick:S.thick,pts:[{x:S.sx,y:S.sy},{x,y}]});
  else if(S.tool==='free'&&S.freeStroke){S.freeStroke.pts.push({x,y});redraw();}
});

cvs.addEventListener('pointerup',e=>{
  const {x,y}=pxCoords(e);
  if(S.tool==='ruler'){
    if(S.rulerDrag){
      const d=S.rulerDrag;
      if(d.type==='new'&&dist2(d.x1,d.y1,x,y)>10){
        S.rulers.push({x1:d.x1,y1:d.y1,x2:x,y2:y,color:S.rulerColor});
        S.selectedRuler=S.rulers.length-1;
      }
      S.rulerDrag=null; redraw();
    }
    return;
  }
  if(!S.drawing) return;
  S.drawing=false;
  if(S.tool==='line'){
    const dx=x-S.sx,dy=y-S.sy;
    if(dx*dx+dy*dy>25) S.strokes.push({type:'line',color:S.color,thick:S.thick,pts:[{x:S.sx,y:S.sy},{x,y}]});
    redraw();
  }
  S.freeStroke=null;
});

cvs.addEventListener('pointerleave',()=>{
  if(S.drawing&&S.tool==='line'){S.drawing=false;redraw();}
});

cvs.addEventListener('contextmenu',e=>{
  e.preventDefault(); const {x,y}=pxCoords(e);
  const hit=hitRuler(x,y);
  if(hit){
    S.rulers.splice(hit.idx,1);
    if(S.selectedRuler===hit.idx) S.selectedRuler=-1;
    else if(S.selectedRuler>hit.idx) S.selectedRuler--;
    redraw();
  }
});

function setTool(t){
  S.tool=t;
  const map={btnLine:'line',btnFree:'free',btnRuler:'ruler',btnEraser:'eraser'};
  Object.entries(map).forEach(([id,val])=>document.getElementById(id).classList.toggle('active',val===t));
  cvs.style.cursor=t==='eraser'?'cell':'crosshair';
  document.getElementById('rulerTip').style.display=t==='ruler'?'block':'none';
}
document.getElementById('btnLine').addEventListener('click',()=>setTool('line'));
document.getElementById('btnFree').addEventListener('click',()=>setTool('free'));
document.getElementById('btnRuler').addEventListener('click',()=>setTool('ruler'));
document.getElementById('btnEraser').addEventListener('click',()=>setTool('eraser'));

document.querySelectorAll('.rswatch').forEach(el=>{
  el.addEventListener('click',()=>{
    document.querySelectorAll('.rswatch').forEach(s=>s.classList.remove('active'));
    el.classList.add('active'); S.rulerColor=el.dataset.rc;
    document.getElementById('rcpicker').value=S.rulerColor;
    if(S.selectedRuler>=0){S.rulers[S.selectedRuler].color=S.rulerColor;redraw();}
  });
});
document.getElementById('rcpicker').addEventListener('input',e=>{
  S.rulerColor=e.target.value;
  document.querySelectorAll('.rswatch').forEach(s=>s.classList.remove('active'));
  if(S.selectedRuler>=0){S.rulers[S.selectedRuler].color=S.rulerColor;redraw();}
});
document.querySelectorAll('.cswatch').forEach(el=>{
  el.addEventListener('click',()=>{
    document.querySelectorAll('.cswatch').forEach(s=>s.classList.remove('active'));
    el.classList.add('active'); S.color=el.dataset.c;
    document.getElementById('cpicker').value=S.color;
  });
});
document.getElementById('cpicker').addEventListener('input',e=>{
  S.color=e.target.value;
  document.querySelectorAll('.cswatch').forEach(s=>s.classList.remove('active'));
});
document.getElementById('thickSlider').addEventListener('input',e=>{
  S.thick=+e.target.value; document.getElementById('thickVal').textContent=S.thick;
});
document.getElementById('btnUndo').addEventListener('click',()=>{
  if(S.tool==='ruler'&&S.rulers.length){S.rulers.pop();S.selectedRuler=-1;}
  else if(S.strokes.length){S.strokes.pop();}
  redraw();
});
document.getElementById('btnClear').addEventListener('click',()=>{
  S.strokes=[];S.rulers=[];S.selectedRuler=-1;redraw();
});
document.getElementById('stepsToggle').addEventListener('click',()=>{
  const body=document.getElementById('stepsBody');
  const arrow=document.getElementById('stepsArrow');
  const open=body.style.display==='block';
  body.style.display=open?'none':'block';
  arrow.textContent=open?'▼':'▲';
});

// ── Harmonic checker ────────────────────────────────────────────────────────
document.getElementById('harmBtn').addEventListener('click', () => {
  const raw = document.getElementById('harmInput').value;
  const nums = raw.split(/[,\s]+/).map(Number).filter(n => !isNaN(n) && n > 0);
  const res = document.getElementById('harmResult');
  res.style.display = 'block';

  if (nums.length < 3) {
    res.innerHTML = '<span class="warn">⚠️ 숫자를 3개 이상 입력해주세요.</span>';
    return;
  }

  // Sort ascending (farther objects = smaller projection → sort small→large means far→near)
  // But user enters near→far (large→small) or far→near (small→large)?
  // We just check both sorted orders; harmonic sequences are monotone
  const sorted = [...nums].sort((a,b)=>a-b);
  const invs = sorted.map(n => 1/n);
  const diffs = invs.slice(1).map((v,i) => v - invs[i]);
  const avgDiff = diffs.reduce((a,b)=>a+b,0)/diffs.length;
  const maxErr = Math.max(...diffs.map(d => Math.abs(d-avgDiff)));
  const relErr = Math.abs(avgDiff) > 1e-12 ? maxErr/Math.abs(avgDiff) : 0;
  const isHarm = relErr < 0.08;  // 8% tolerance

  // Build table
  let tHead = '<tr><th>순서</th><th>측정값</th><th>역수 (1/값)</th><th>역수 공차</th></tr>';
  let tBody = sorted.map((v,i) => {
    const invStr = invs[i].toFixed(5);
    const diffStr = i===0 ? '—' : (diffs[i-1]>=0?'+':'')+diffs[i-1].toFixed(5);
    const diffColor = i===0 ? '' : (Math.abs(diffs[i-1]-avgDiff)<maxErr*1.01?'color:#4ade80':'color:#fbbf24');
    return `<tr><td>${i+1}</td><td class="val">${v.toFixed(3)}</td>`+
           `<td class="val">${invStr}</td>`+
           `<td style="${diffColor}">${diffStr}</td></tr>`;
  }).join('');

  const harmMeans = [];
  for(let i=0;i<sorted.length-2;i++){
    const hm = 2/(1/sorted[i]+1/sorted[i+2]);
    harmMeans.push(`2/(1/${sorted[i].toFixed(2)}+1/${sorted[i+2].toFixed(2)}) = <span class="val">${hm.toFixed(3)}</span> ≈ ${sorted[i+1].toFixed(3)}`);
  }

  res.innerHTML = `
<table><thead>${tHead}</thead><tbody>${tBody}</tbody></table>
<br>
<b>역수 공차 평균:</b> <span class="val">${avgDiff.toFixed(5)}</span> &nbsp;|&nbsp;
<b>최대 편차:</b> <span class="${isHarm?'ok':'warn'}">${maxErr.toFixed(5)}</span>
(상대오차 ${(relErr*100).toFixed(1)}%)<br><br>
${harmMeans.map(s=>'<b>조화평균 검증:</b> '+s+'<br>').join('')}
<br>
${isHarm
  ? '<span class="ok">✅ 조화수열입니다! 역수들이 등차수열을 이룹니다.</span>'
  : '<span class="warn">⚠️ 완전한 조화수열은 아닙니다. 측정값을 다시 확인해보세요.</span>'
}`;
});

// Hint buttons
document.getElementById('hintTile').addEventListener('click',()=>{
  const b=document.getElementById('hintTileBox');
  b.style.display=b.style.display==='block'?'none':'block';
});
document.getElementById('hintCeil').addEventListener('click',()=>{
  const b=document.getElementById('hintCeilBox');
  b.style.display=b.style.display==='block'?'none':'block';
});

init();
})();
</script>
</body>
</html>
"""


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _b64(fname: str, max_w: int = 1100) -> str:
    """Load image from assets/gifted_art, resize if wider than max_w, return base64."""
    try:
        from PIL import Image  # type: ignore
        root = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "gifted_art")
        )
        fpath = os.path.join(root, fname)
        img = Image.open(fpath)
        if img.width > max_w:
            ratio = max_w / img.width
            img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        if fname.lower().endswith(".png"):
            img.save(buf, format="PNG")
        else:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


def _make_painting_html(img_b64: str) -> str:
    return _PAINTING_TEMPLATE.replace("__IMAGE_B64__", img_b64)


# ─── render ───────────────────────────────────────────────────────────────────

def render():
    st.header("📐 등간격 사물 → 화폭에서 조화수열")

    tab1, tab2, tab3 = st.tabs(["🧮 원리 탐구", "📐 증명 탐구", "🖼️ 그림에서 찾기"])

    with tab1:
        components.html(_HTML, height=1600, scrolling=True)

    with tab2:
        components.html(_HTML_PROOF, height=1800, scrolling=True)

    with tab3:
        img_b64 = _b64("christ.png")
        components.html(_make_painting_html(img_b64), height=1100, scrolling=True)
