import streamlit as st
import streamlit.components.v1 as components
import requests
import datetime

META = {"title": "대수막대로 곱셈 공식 탐구", "order": 25}

_GAS_URL    = "https://script.google.com/macros/s/AKfycbySLDnSYGfQmqrtpuMyIju5hiEf7Lesp6bnWzplm3oZD4WHXESl1XJmsXT_EVcKOJI/exec"
_SHEET_NAME = "대수막대곱셈공식"

_GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR','Segoe UI',sans-serif;background:#0b1120;color:#e2e8f0;padding:12px;font-size:15px;min-height:100vh}
.ftabs{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:16px}
.ftab{padding:7px 14px;border-radius:20px;border:2px solid #1e293b;background:#1a2236;color:#64748b;cursor:pointer;font-size:.78rem;transition:all .2s;user-select:none}
.ftab:hover{border-color:#334155;color:#94a3b8}
.ftab.active{border-color:#06b6d4;background:#0c2e3e;color:#a5f3fc;font-weight:700}
.ftab.done{border-color:#10b981!important;background:#032017!important;color:#6ee7b7!important}
.ftab.done::before{content:'\2713 '}
.panel{display:none}.panel.active{display:block}
.card{background:#111827;border:1px solid #1e293b;border-radius:14px;padding:16px;margin-bottom:14px}
.card-title{font-size:1rem;font-weight:700;color:#7dd3fc;margin-bottom:12px}
.formula-box{background:#0c1830;border:1px solid #1e3a5f;border-radius:10px;padding:12px 18px;font-size:1.1rem;text-align:center;margin-bottom:14px}
.tile-workspace{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap;margin-bottom:14px}
.tile-pool{background:#0f172a;border:2px dashed #334155;border-radius:12px;padding:10px;min-width:150px;min-height:80px}
.tile-pool-title{font-size:.75rem;color:#64748b;margin-bottom:8px;font-weight:600}
.tile-pool .tiles-row{display:flex;flex-wrap:wrap;gap:6px}
.tile{padding:6px 10px;border-radius:8px;font-size:.78rem;font-weight:700;cursor:grab;user-select:none;transition:all .15s;display:inline-flex;align-items:center;justify-content:center;border:2px solid transparent;min-width:44px;text-align:center}
.tile:active{cursor:grabbing;transform:scale(1.1)}
.tile.dragging{opacity:.5}
.tile-x2{background:#1e3a5f;border-color:#3b82f6;color:#bfdbfe}
.tile-abx{background:#1c3a2e;border-color:#10b981;color:#6ee7b7}
.tile-b2{background:#2d1b4e;border-color:#8b5cf6;color:#c4b5fd}
.tile-neg{opacity:.7}
.tile-unit{background:#2d2a1b;border-color:#f59e0b;color:#fde68a}
.grid-cell{width:48px;height:48px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:.7rem;color:#fff;font-weight:700;cursor:pointer;transition:all .15s}
.grid-cell.empty{background:#0f172a;border:2px dashed #334155}
.grid-cell.empty:hover{border-color:#06b6d4;background:#0c2a3a}
.grid-cell.placed{cursor:default}
.placed.tile-x2{background:#1e3a5f;border:2px solid #60a5fa}
.placed.tile-abx{background:#1c3a2e;border:2px solid #34d399}
.placed.tile-b2{background:#2d1b4e;border:2px solid #a78bfa}
.placed.tile-neg{opacity:.75}
.placed.tile-unit{background:#2d2a1b;border:2px solid #fbbf24}
.hint-btn,.check-btn,.reset-btn{padding:7px 18px;border:none;border-radius:8px;cursor:pointer;font-size:.82rem;font-weight:600;transition:all .2s;margin-right:6px;margin-bottom:6px}
.check-btn{background:#0e7490;color:#fff}.check-btn:hover{background:#0891b2}
.hint-btn{background:#1c3a2e;color:#6ee7b7;border:1px solid #10b981}
.reset-btn{background:#2d1b1b;color:#fca5a5;border:1px solid #dc2626}
.msg-box{padding:12px 16px;border-radius:10px;font-size:.9rem;margin-top:10px;display:none}
.msg-box.show{display:block}
.msg-success{background:#032017;border:1px solid #10b981;color:#6ee7b7}
.msg-error{background:#1b0808;border:1px solid #dc2626;color:#fca5a5}
.msg-hint{background:#1c2a3e;border:1px solid #3b82f6;color:#93c5fd}
.prog-bar-wrap{margin-bottom:14px}
.prog-track{height:6px;background:#1e293b;border-radius:99px;overflow:hidden;margin-top:4px}
.prog-fill{height:100%;background:linear-gradient(90deg,#06b6d4,#7c3aed);border-radius:99px;transition:width .5s}
.prog-lbl{font-size:.72rem;color:#64748b;display:flex;justify-content:space-between;margin-top:2px}
.scene{width:260px;height:260px;perspective:800px;margin:0 auto;cursor:grab}
.scene:active{cursor:grabbing}
.cube-wrap{width:260px;height:260px;position:relative;transform-style:preserve-3d;transform-origin:130px 130px 0}
.cube-block{position:absolute;width:0;height:0;transform-style:preserve-3d}
.face{position:absolute;display:flex;align-items:center;justify-content:center;font-size:.65rem;font-weight:700;backface-visibility:visible;opacity:.88;border-radius:3px}
.cube-controls{display:flex;gap:8px;justify-content:center;margin-top:10px;flex-wrap:wrap}
.cube-controls button{padding:5px 12px;border-radius:6px;border:1px solid #334155;background:#1a2236;color:#94a3b8;cursor:pointer;font-size:.75rem}
.cube-controls button:hover{background:#0c2e3e;color:#a5f3fc}
.parts-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.part-badge{padding:5px 12px;border-radius:6px;font-size:.78rem;font-weight:700;cursor:pointer;transition:all .2s;border:1px solid transparent;color:#fff}
.part-badge:hover{filter:brightness(1.3)}
@media(max-width:600px){.tile-workspace{flex-direction:column}.scene{width:200px;height:200px}}
</style>
</head>
<body>

<div class="prog-bar-wrap">
  <div class="prog-lbl"><span>진행도</span><span id="prog-text">0 / 8 완료</span></div>
  <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
</div>

<div class="ftabs" id="ftabs">
  <div class="ftab active" onclick="showTab(0)" id="tab0">① $(a+b)^2$</div>
  <div class="ftab" onclick="showTab(1)" id="tab1">② $(a-b)^2$</div>
  <div class="ftab" onclick="showTab(2)" id="tab2">③ $(a+b)(a-b)$</div>
  <div class="ftab" onclick="showTab(3)" id="tab3">④ $(x+a)(x+b)$</div>
  <div class="ftab" onclick="showTab(4)" id="tab4">⑤ $(ax+b)(cx+d)$</div>
  <div class="ftab" onclick="showTab(5)" id="tab5">⑥ $(a+b+c)^2$</div>
  <div class="ftab" onclick="showTab(6)" id="tab6">⑦ $(a+b)^3$ 3D</div>
  <div class="ftab" onclick="showTab(7)" id="tab7">⑧ $a^3+b^3$ 3D</div>
</div>

<!-- Panel 0 -->
<div class="panel active" id="panel0">
  <div class="card">
    <div class="card-title">중학교 복습 ① — $(a+b)^2$ 탐구</div>
    <div class="formula-box">$(a+b)^2 = (a+b)(a+b) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">왼쪽 타일 창고에서 타일을 <b>드래그</b>하여 격자에 끌어다 놓으세요. 놓인 타일을 <b>클릭</b>하면 제거됩니다.</p>
    <div class="tile-workspace" id="ws0"></div>
    <div><button class="check-btn" onclick="checkGrid(0)">✔ 확인</button><button class="hint-btn" onclick="showHint(0)">힌트</button><button class="reset-btn" onclick="resetGrid(0)">↺ 초기화</button></div>
    <div class="msg-box" id="msg0"></div>
  </div>
</div>
<!-- Panel 1 -->
<div class="panel" id="panel1">
  <div class="card">
    <div class="card-title">중학교 복습 ② — $(a-b)^2$ 탐구</div>
    <div class="formula-box">$(a-b)^2 = (a-b)(a-b) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">빨간(어두운) 테두리 타일은 <b>음(−) 넓이</b>를 나타냅니다.</p>
    <div class="tile-workspace" id="ws1"></div>
    <div><button class="check-btn" onclick="checkGrid(1)">✔ 확인</button><button class="hint-btn" onclick="showHint(1)">힌트</button><button class="reset-btn" onclick="resetGrid(1)">↺ 초기화</button></div>
    <div class="msg-box" id="msg1"></div>
  </div>
</div>
<!-- Panel 2 -->
<div class="panel" id="panel2">
  <div class="card">
    <div class="card-title">중학교 복습 ③ — $(a+b)(a-b)$ 탐구</div>
    <div class="formula-box">$(a+b)(a-b) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">가로 $(a+b)$, 세로 $(a-b)$인 직사각형을 채워보세요.</p>
    <div class="tile-workspace" id="ws2"></div>
    <div><button class="check-btn" onclick="checkGrid(2)">✔ 확인</button><button class="hint-btn" onclick="showHint(2)">힌트</button><button class="reset-btn" onclick="resetGrid(2)">↺ 초기화</button></div>
    <div class="msg-box" id="msg2"></div>
  </div>
</div>
<!-- Panel 3 -->
<div class="panel" id="panel3">
  <div class="card">
    <div class="card-title">중학교 복습 ④ — $(x+a)(x+b)$ 탐구</div>
    <div class="formula-box">$(x+a)(x+b) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">가로 $(x+a)$, 세로 $(x+b)$인 직사각형을 채워보세요.</p>
    <div class="tile-workspace" id="ws3"></div>
    <div><button class="check-btn" onclick="checkGrid(3)">✔ 확인</button><button class="hint-btn" onclick="showHint(3)">힌트</button><button class="reset-btn" onclick="resetGrid(3)">↺ 초기화</button></div>
    <div class="msg-box" id="msg3"></div>
  </div>
</div>
<!-- Panel 4 -->
<div class="panel" id="panel4">
  <div class="card">
    <div class="card-title">중학교 복습 ⑤ — $(ax+b)(cx+d)$ 탐구</div>
    <div class="formula-box">$(ax+b)(cx+d) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">가로 $(ax+b)$, 세로 $(cx+d)$인 직사각형을 채워보세요.</p>
    <div class="tile-workspace" id="ws4"></div>
    <div><button class="check-btn" onclick="checkGrid(4)">✔ 확인</button><button class="hint-btn" onclick="showHint(4)">힌트</button><button class="reset-btn" onclick="resetGrid(4)">↺ 초기화</button></div>
    <div class="msg-box" id="msg4"></div>
  </div>
</div>
<!-- Panel 5 -->
<div class="panel" id="panel5">
  <div class="card">
    <div class="card-title">새 공식 ① — $(a+b+c)^2$ 탐구</div>
    <div class="formula-box">$(a+b+c)^2 = (a+b+c)(a+b+c) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">가로·세로 모두 $(a+b+c)$인 3×3 정사각형을 채워보세요.</p>
    <div class="tile-workspace" id="ws5"></div>
    <div><button class="check-btn" onclick="checkGrid(5)">✔ 확인</button><button class="hint-btn" onclick="showHint(5)">힌트</button><button class="reset-btn" onclick="resetGrid(5)">↺ 초기화</button></div>
    <div class="msg-box" id="msg5"></div>
  </div>
</div>
<!-- Panel 6 -->
<div class="panel" id="panel6">
  <div class="card">
    <div class="card-title">입체 신공식 ② — $(a+b)^3$ 탐구</div>
    <div class="formula-box">$(a+b)^3 = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">한 변이 $(a+b)$인 정육면체를 8개 조각으로 나눠보세요. 드래그로 회전, 조각 클릭하면 강조됩니다.</p>
    <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start">
      <div style="flex:0 0 240px">
        <div style="font-size:.85rem;color:#7dd3fc;font-weight:700;margin-bottom:8px">8개 조각 (클릭하면 강조)</div>
        <div class="parts-list" id="parts6"></div>
        <div class="msg-box" id="msg6" style="margin-top:12px"></div>
        <div style="margin-top:12px">
          <button class="check-btn" onclick="checkCube(6)">✔ 공식 확인</button>
          <button class="reset-btn" onclick="resetCubeHL(6)">↺ 강조 해제</button>
        </div>
      </div>
      <div>
        <div class="scene" id="scene6"><div class="cube-wrap" id="cubeWrap6"></div></div>
        <div class="cube-controls">
          <button onclick="rotateCube(6,-30,0)">◀</button>
          <button onclick="rotateCube(6,30,0)">▶</button>
          <button onclick="rotateCube(6,0,-30)">▲</button>
          <button onclick="rotateCube(6,0,30)">▼</button>
          <button onclick="resetCubeRot(6)">↺</button>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- Panel 7 -->
<div class="panel" id="panel7">
  <div class="card">
    <div class="card-title">입체 신공식 ③ — $a^3+b^3$ 인수분해 탐구</div>
    <div class="formula-box">$a^3 + b^3 = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">$(a+b)^3$ 전개식에서 어떤 항들이 상쇄되면 $a^3+b^3$이 남을까요? 조각을 클릭해서 확인해보세요.</p>
    <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start">
      <div style="flex:0 0 240px">
        <div style="font-size:.85rem;color:#7dd3fc;font-weight:700;margin-bottom:8px">조각 목록 (클릭시 강조)</div>
        <div class="parts-list" id="parts7"></div>
        <div class="msg-box" id="msg7" style="margin-top:12px"></div>
        <div style="margin-top:12px">
          <button class="check-btn" onclick="checkCube(7)">✔ 공식 확인</button>
          <button class="reset-btn" onclick="resetCubeHL(7)">↺ 강조 해제</button>
        </div>
      </div>
      <div>
        <div class="scene" id="scene7"><div class="cube-wrap" id="cubeWrap7"></div></div>
        <div class="cube-controls">
          <button onclick="rotateCube(7,-30,0)">◀</button>
          <button onclick="rotateCube(7,30,0)">▶</button>
          <button onclick="rotateCube(7,0,-30)">▲</button>
          <button onclick="rotateCube(7,0,30)">▼</button>
          <button onclick="resetCubeRot(7)">↺</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
// ── 공식 데이터 ──
const FDATA = [
  {cols:2,rows:2,cL:['a','b'],rL:['a','b'],
   pool:[{type:'tile-x2',tex:'a^2',cnt:1},{type:'tile-abx',tex:'ab',cnt:2},{type:'tile-b2',tex:'b^2',cnt:1}],
   ans:[['tile-x2','tile-abx'],['tile-abx','tile-b2']],
   result:'(a+b)^2 = a^2 + 2ab + b^2',
   hint:'좌상: a², 우상: ab, 좌하: ab, 우하: b²'},
  {cols:2,rows:2,cL:['a','(-b)'],rL:['a','(-b)'],
   pool:[{type:'tile-x2',tex:'a^2',cnt:1},{type:'tile-abx tile-neg',tex:'-ab',cnt:2},{type:'tile-b2',tex:'b^2',cnt:1}],
   ans:[['tile-x2','tile-abx tile-neg'],['tile-abx tile-neg','tile-b2']],
   result:'(a-b)^2 = a^2 - 2ab + b^2',
   hint:'(-b)×a = -ab, a×(-b) = -ab. (-b)×(-b) = b² (양수!)'},
  {cols:2,rows:2,cL:['a','b'],rL:['a','(-b)'],
   pool:[{type:'tile-x2',tex:'a^2',cnt:1},{type:'tile-abx',tex:'ab',cnt:1},{type:'tile-abx tile-neg',tex:'-ab',cnt:1},{type:'tile-b2 tile-neg',tex:'-b^2',cnt:1}],
   ans:[['tile-x2','tile-abx'],['tile-abx tile-neg','tile-b2 tile-neg']],
   result:'(a+b)(a-b) = a^2 - b^2',
   hint:'ab와 -ab가 서로 상쇄돼서 a²-b²만 남아요!'},
  {cols:2,rows:2,cL:['x','a'],rL:['x','b'],
   pool:[{type:'tile-x2',tex:'x^2',cnt:1},{type:'tile-abx',tex:'ax',cnt:1},{type:'tile-abx',tex:'bx',cnt:1},{type:'tile-unit',tex:'ab',cnt:1}],
   ans:[['tile-x2','tile-abx'],['tile-abx','tile-unit']],
   result:'(x+a)(x+b) = x^2 + (a+b)x + ab',
   hint:'좌상: x², 우상: ax, 좌하: bx, 우하: ab'},
  {cols:2,rows:2,cL:['ax','b'],rL:['cx','d'],
   pool:[{type:'tile-x2',tex:'acx^2',cnt:1},{type:'tile-abx',tex:'adx',cnt:1},{type:'tile-abx',tex:'bcx',cnt:1},{type:'tile-unit',tex:'bd',cnt:1}],
   ans:[['tile-x2','tile-abx'],['tile-abx','tile-unit']],
   result:'(ax+b)(cx+d) = acx^2 + (ad+bc)x + bd',
   hint:'(cx)(ax)=acx², d·ax=adx, (cx)b=bcx, d·b=bd'},
  {cols:3,rows:3,cL:['a','b','c'],rL:['a','b','c'],
   pool:[{type:'tile-x2',tex:'a^2',cnt:1},{type:'tile-x2',tex:'b^2',cnt:1},{type:'tile-x2',tex:'c^2',cnt:1},
         {type:'tile-abx',tex:'ab',cnt:2},{type:'tile-abx',tex:'bc',cnt:2},{type:'tile-b2',tex:'ca',cnt:2}],
   ans:[['tile-x2','tile-abx','tile-b2'],['tile-abx','tile-x2','tile-abx'],['tile-b2','tile-abx','tile-x2']],
   result:'(a+b+c)^2 = a^2+b^2+c^2+2ab+2bc+2ca',
   hint:'대각선: a², b², c². 나머지는 두 변수의 곱 (각 2개씩)'},
];

// ── 상태 ──
const gS = {}, pC = {};

function initState(fi) {
  const f = FDATA[fi];
  if (!gS[fi]) {
    gS[fi] = Array.from({length:f.rows}, () => new Array(f.cols).fill(null));
    pC[fi] = f.pool.map(p => p.cnt);
  }
}

// ── 격자 빌드 ──
function buildGrid(fi) {
  const f = FDATA[fi]; initState(fi);
  const ws = document.getElementById('ws' + fi); ws.innerHTML = '';
  // 타일 창고
  const poolDiv = document.createElement('div'); poolDiv.className = 'tile-pool';
  poolDiv.innerHTML = '<div class="tile-pool-title">타일 창고</div><div class="tiles-row" id="pr' + fi + '"></div>';
  ws.appendChild(poolDiv);
  // 격자
  const table = document.createElement('div');
  table.style.cssText = 'display:inline-grid;gap:3px;grid-template-columns:auto ' + ('48px '.repeat(f.cols)).trim();
  const corner = document.createElement('div'); corner.style.cssText = 'width:36px;height:36px'; table.appendChild(corner);
  f.cL.forEach(l => {
    const d = document.createElement('div');
    d.style.cssText = 'width:48px;height:36px;display:flex;align-items:center;justify-content:center;color:#fbbf24;font-weight:700;font-size:.82rem';
    d.innerHTML = katex.renderToString(l, {throwOnError:false}); table.appendChild(d);
  });
  for (let r = 0; r < f.rows; r++) {
    const rl = document.createElement('div');
    rl.style.cssText = 'width:36px;display:flex;align-items:center;justify-content:center;color:#fbbf24;font-weight:700;font-size:.82rem';
    rl.innerHTML = katex.renderToString(f.rL[r], {throwOnError:false}); table.appendChild(rl);
    for (let c = 0; c < f.cols; c++) {
      const cell = document.createElement('div'); cell.id = 'cell-' + fi + '-' + r + '-' + c;
      cell.dataset.fi = fi; cell.dataset.r = r; cell.dataset.c = c;
      const placed = gS[fi][r][c];
      if (placed) setCellPlaced(cell, fi, r, c, placed); else cell.className = 'grid-cell empty';
      cell.addEventListener('dragover', e => { e.preventDefault(); if (!gS[fi][r][c]) cell.style.borderColor = '#06b6d4'; });
      cell.addEventListener('dragleave', () => { if (!gS[fi][r][c]) cell.style.borderColor = ''; });
      cell.addEventListener('drop', e => { e.preventDefault(); cell.style.borderColor = ''; doDropOnCell(fi, r, c, JSON.parse(e.dataTransfer.getData('text/plain'))); });
      cell.addEventListener('click', () => { if (gS[fi][r][c]) removeFromCell(fi, r, c); });
      table.appendChild(cell);
    }
  }
  ws.appendChild(table);
  renderPool(fi);
}

function renderPool(fi) {
  const f = FDATA[fi]; const row = document.getElementById('pr' + fi);
  if (!row) return; row.innerHTML = '';
  f.pool.forEach((item, pi) => {
    const rem = pC[fi][pi];
    for (let i = 0; i < rem; i++) {
      const tile = document.createElement('div'); tile.className = 'tile ' + item.type;
      tile.innerHTML = katex.renderToString(item.tex, {throwOnError:false});
      tile.draggable = true; tile.dataset.pi = pi; tile.dataset.fi = fi; tile.dataset.type = item.type;
      tile.addEventListener('dragstart', e => { tile.classList.add('dragging'); e.dataTransfer.setData('text/plain', JSON.stringify({pi, fi, type:item.type, tex:item.tex})); });
      tile.addEventListener('dragend', () => tile.classList.remove('dragging'));
      tile.addEventListener('touchstart', touchStart, {passive:false});
      row.appendChild(tile);
    }
    if (rem === 0) {
      const ph = document.createElement('div'); ph.className = 'tile ' + item.type; ph.style.opacity = '.18';
      ph.innerHTML = katex.renderToString(item.tex, {throwOnError:false}); row.appendChild(ph);
    }
  });
}

function doDropOnCell(fi, r, c, data) {
  if (gS[fi][r][c]) returnToPool(fi, gS[fi][r][c]);
  pC[fi][data.pi]--; gS[fi][r][c] = data.type;
  const cell = document.getElementById('cell-' + fi + '-' + r + '-' + c);
  setCellPlaced(cell, fi, r, c, data.type); renderPool(fi);
}

function setCellPlaced(cell, fi, r, c, type) {
  cell.className = 'grid-cell placed ' + type;
  const item = FDATA[fi].pool.find(p => p.type === type);
  cell.innerHTML = katex.renderToString(item ? item.tex : '?', {throwOnError:false});
  cell.title = '클릭해서 제거';
}

function removeFromCell(fi, r, c) {
  returnToPool(fi, gS[fi][r][c]); gS[fi][r][c] = null;
  const cell = document.getElementById('cell-' + fi + '-' + r + '-' + c);
  cell.className = 'grid-cell empty'; cell.innerHTML = ''; cell.title = ''; renderPool(fi);
}

function returnToPool(fi, type) {
  const idx = FDATA[fi].pool.findIndex(p => p.type === type); if (idx !== -1) pC[fi][idx]++;
}

// ── 확인 / 힌트 / 초기화 ──
function checkGrid(fi) {
  const f = FDATA[fi]; let allFilled = true, allOk = true;
  for (let r = 0; r < f.rows; r++) for (let c = 0; c < f.cols; c++) {
    const placed = gS[fi][r][c], exp = f.ans[r][c];
    const cell = document.getElementById('cell-' + fi + '-' + r + '-' + c);
    if (!placed) { allFilled = false; continue; }
    if (placed === exp) cell.style.outline = '2px solid #10b981';
    else { cell.style.outline = '2px solid #ef4444'; allOk = false; }
  }
  const msg = document.getElementById('msg' + fi); msg.className = 'msg-box show';
  if (!allFilled) { msg.className = 'msg-box msg-hint show'; msg.innerHTML = '⚠ 빈 칸이 있어요!'; return; }
  if (allOk) {
    msg.className = 'msg-box msg-success show';
    msg.innerHTML = '정답! ' + katex.renderToString(f.result, {throwOnError:false});
    document.getElementById('tab' + fi).classList.add('done'); updateProg();
  } else {
    msg.className = 'msg-box msg-error show';
    msg.innerHTML = '✗ 틀린 칸이 있어요 (빨간 테두리 확인)';
  }
}

function showHint(fi) {
  const msg = document.getElementById('msg' + fi); msg.className = 'msg-box msg-hint show';
  msg.innerHTML = '💡 ' + FDATA[fi].hint;
}

function resetGrid(fi) {
  const f = FDATA[fi]; gS[fi] = Array.from({length:f.rows}, () => new Array(f.cols).fill(null)); pC[fi] = f.pool.map(p => p.cnt);
  buildGrid(fi); document.getElementById('msg' + fi).className = 'msg-box';
}

// ── 3D 정육면체 ──
const CUBE_PARTS = {
  6: [{key:'a3', label:'a^3', color:'#1e3a5f', border:'#3b82f6', count:1},
      {key:'a2b',label:'a^2b',color:'#1c3a2e', border:'#10b981', count:3},
      {key:'ab2',label:'ab^2',color:'#2d1b4e', border:'#8b5cf6', count:3},
      {key:'b3', label:'b^3', color:'#2d2a1b', border:'#f59e0b', count:1}],
  7: [{key:'a3', label:'a^3', color:'#1e3a5f', border:'#3b82f6', count:1, keep:true},
      {key:'a2b',label:'a^2b',color:'#1c3a2e',border:'#10b981', count:3, keep:false},
      {key:'ab2',label:'ab^2',color:'#2d1b4e',border:'#8b5cf6', count:3, keep:false},
      {key:'b3', label:'b^3', color:'#2d2a1b', border:'#f59e0b', count:1, keep:true}],
};
const cubeRot = {6:{x:30,y:-20}, 7:{x:30,y:-20}};

function buildCube(idx, wrapId) {
  const wrap = document.getElementById(wrapId); wrap.innerHTML = '';
  const A = 76, B = 44, dims = [A,B], offs = [0,A], total = A+B;
  const parts = CUBE_PARTS[idx];
  for (let ix = 0; ix < 2; ix++) for (let iy = 0; iy < 2; iy++) for (let iz = 0; iz < 2; iz++) {
    const bc = ix + iy + iz; const part = parts[bc];
    const bk = document.createElement('div'); bk.className = 'cube-block'; bk.dataset.key = part.key;
    const w=dims[ix], h=dims[iy], d=dims[iz], ox=offs[ix], oy=offs[iy], oz=offs[iz], cx=total/2, cy=total/2, cz=total/2;
    bk.style.cssText = 'position:absolute;width:0;height:0;transform-style:preserve-3d;left:' + cx + 'px;top:' + cy + 'px;transform:translate3d(' + (ox-cx) + 'px,' + (oy-cy) + 'px,' + (oz-cz) + 'px)';
    bk.addEventListener('click', () => hlPart(idx, part.key));
    [{fw:w,fh:h,tx:0,ty:0,tz:d/2,rx:0,ry:0,lbl:true},
     {fw:w,fh:h,tx:0,ty:0,tz:-d/2,rx:0,ry:180,lbl:true},
     {fw:d,fh:h,tx:-w/2,ty:0,tz:0,rx:0,ry:-90,lbl:true},
     {fw:d,fh:h,tx:w/2,ty:0,tz:0,rx:0,ry:90,lbl:true},
     {fw:w,fh:d,tx:0,ty:-h/2,tz:0,rx:-90,ry:0,lbl:true},
     {fw:w,fh:d,tx:0,ty:h/2,tz:0,rx:90,ry:0,lbl:true}].forEach(fd => {
      const face = document.createElement('div'); face.className = 'face';
      face.style.cssText = 'width:' + fd.fw + 'px;height:' + fd.fh + 'px;margin-left:' + (-fd.fw/2) + 'px;margin-top:' + (-fd.fh/2) + 'px;background:' + part.color + ';border:1px solid ' + part.border + ';transform:translate3d(' + fd.tx + 'px,' + fd.ty + 'px,' + fd.tz + 'px) rotateY(' + fd.ry + 'deg) rotateX(' + fd.rx + 'deg)';
      if (fd.lbl) face.innerHTML = katex.renderToString(part.label, {throwOnError:false});
      bk.appendChild(face);
    });
    wrap.appendChild(bk);
  }
  applyCubeRot(idx);
}

function applyCubeRot(idx) { const w = document.getElementById('cubeWrap' + idx); const r = cubeRot[idx]; w.style.transform = 'rotateX(' + r.x + 'deg) rotateY(' + r.y + 'deg)'; }
function rotateCube(idx, dy, dx) { cubeRot[idx].y += dy; cubeRot[idx].x += dx; applyCubeRot(idx); }
function resetCubeRot(idx) { cubeRot[idx] = {x:30, y:-20}; applyCubeRot(idx); }

let dragPtr = null;
function initDrag(sceneId, idx) {
  const el = document.getElementById(sceneId);
  el.addEventListener('pointerdown', e => { dragPtr = {x:e.clientX, y:e.clientY}; el.setPointerCapture(e.pointerId); });
  el.addEventListener('pointermove', e => { if (!dragPtr) return; cubeRot[idx].y += (e.clientX - dragPtr.x) * 0.6; cubeRot[idx].x += (e.clientY - dragPtr.y) * 0.4; dragPtr = {x:e.clientX, y:e.clientY}; applyCubeRot(idx); });
  el.addEventListener('pointerup', () => { dragPtr = null; });
}

function hlPart(idx, key) { document.querySelectorAll('#cubeWrap' + idx + ' .cube-block').forEach(b => { b.style.filter = b.dataset.key === key ? 'brightness(2) drop-shadow(0 0 8px #fff)' : 'brightness(.35)'; }); }
function resetCubeHL(idx) { document.querySelectorAll('#cubeWrap' + idx + ' .cube-block').forEach(b => b.style.filter = ''); document.getElementById('msg' + idx).className = 'msg-box'; }

function buildPartBadges(idx) {
  const con = document.getElementById('parts' + idx); con.innerHTML = '';
  CUBE_PARTS[idx].forEach(p => {
    const badge = document.createElement('div'); badge.className = 'part-badge';
    badge.style.cssText = 'background:' + p.color + ';border-color:' + p.border;
    badge.innerHTML = katex.renderToString(p.label, {throwOnError:false});
    if (p.count > 1) badge.innerHTML += ' <small style="opacity:.7">×' + p.count + '</small>';
    if (idx === 7 && p.keep === false) badge.style.opacity = '.55';
    badge.addEventListener('click', () => hlPart(idx, p.key));
    con.appendChild(badge);
  });
  if (idx === 7) {
    const note = document.createElement('div'); note.style.cssText = 'font-size:.75rem;color:#94a3b8;margin-top:8px';
    note.textContent = '연한 조각은 상쇄되므로 a³+b³만 남아요.'; con.appendChild(note);
  }
}

function checkCube(idx) {
  const r = {6:'(a+b)^3=a^3+3a^2b+3ab^2+b^3', 7:'a^3+b^3=(a+b)(a^2-ab+b^2)'};
  const n = {6:'8조각: a³(×1)+a²b(×3)+ab²(×3)+b³(×1)', 7:'a²b와 ab²항들이 상쇄되어 a³+b³=(a+b)(a²-ab+b²)'};
  const msg = document.getElementById('msg' + idx);
  msg.className = 'msg-box msg-success show';
  msg.innerHTML = '정답! ' + katex.renderToString(r[idx], {throwOnError:false}) + '<br><small style="color:#6ee7b7;font-size:.75rem">' + n[idx] + '</small>';
  document.getElementById('tab' + idx).classList.add('done'); updateProg();
}

// ── 터치 드래그 ──
let tData = null, tGhost = null;
function touchStart(e) {
  const t = e.currentTarget;
  tData = {pi:+t.dataset.pi, fi:+t.dataset.fi, type:t.dataset.type, tex:FDATA[+t.dataset.fi].pool[+t.dataset.pi].tex};
  e.preventDefault();
}
document.addEventListener('touchmove', e => {
  if (!tData) return; e.preventDefault();
  if (!tGhost) { tGhost = document.createElement('div'); tGhost.style.cssText = 'position:fixed;pointer-events:none;z-index:999;background:#1e3a5f;border-radius:8px;padding:8px;color:#fff;font-size:.8rem;opacity:.85'; tGhost.textContent = '★'; document.body.appendChild(tGhost); }
  tGhost.style.left = (e.touches[0].clientX + 12) + 'px'; tGhost.style.top = (e.touches[0].clientY + 12) + 'px';
}, {passive:false});
document.addEventListener('touchend', e => {
  if (tGhost) { tGhost.remove(); tGhost = null; }
  if (!tData) return;
  const t = e.changedTouches[0]; const el = document.elementFromPoint(t.clientX, t.clientY);
  if (el && el.classList.contains('grid-cell')) { const fi = +el.dataset.fi, r = +el.dataset.r, c = +el.dataset.c; doDropOnCell(fi, r, c, tData); }
  tData = null;
}, {passive:false});

// ── 탭 & 진행도 ──
function showTab(idx) {
  document.querySelectorAll('.ftab').forEach((t, i) => t.classList.toggle('active', i === idx));
  document.querySelectorAll('.panel').forEach((p, i) => p.classList.toggle('active', i === idx));
}
function updateProg() {
  const done = document.querySelectorAll('.ftab.done').length;
  document.getElementById('prog-fill').style.width = (done / 8 * 100) + '%';
  document.getElementById('prog-text').textContent = done + ' / 8 완료';
}

window.addEventListener('load', () => {
  for (let i = 0; i < 6; i++) buildGrid(i);
  buildCube(6, 'cubeWrap6'); buildCube(7, 'cubeWrap7');
  buildPartBadges(6); buildPartBadges(7);
  initDrag('scene6', 6); initDrag('scene7', 7);
  renderMathInElement(document.getElementById('ftabs'), {delimiters:[{left:'$', right:'$', display:false}]});
});
</script>
</body>
</html>"""


def render():
    st.markdown("## 대수막대로 곱셈 공식 탐구")
    st.caption(
        "대수막대를 직접 드래그해서 격자를 채우세요. "
        "중학교 복습 5개 + 새 공식 3개 = 전 8개!"
    )
    components.html(_GAME_HTML, height=920, scrolling=True)
    st.divider()
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_reflection_form(sheet_name: str, gas_url: str):
    st.markdown("### 활동 소감 기록")
    with st.form("reflection_form"):
        c1, c2 = st.columns(2)
        with c1:
            student_id = st.text_input("학번")
        with c2:
            student_name = st.text_input("이름")
        q1 = st.text_area("문제 1", height=70)
        a1 = st.text_area("문제 1 답", height=70)
        q2 = st.text_area("문제 2", height=70)
        a2 = st.text_area("문제 2 답", height=70)
        learned = st.text_area("새롭게 알게 된 점", height=80)
        feelings = st.text_area("느낀 점", height=80)
        submitted = st.form_submit_button("제출하기")
    if submitted:
        if not student_id or not student_name:
            st.warning("학번과 이름을 입력해주세요.")
            return
        payload = {
            "sheet": sheet_name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "학번": student_id,
            "이름": student_name,
            "문제1": q1, "답1": a1,
            "문제2": q2, "답2": a2,
            "새롭게알게된점": learned,
            "느낀점": feelings,
        }
        try:
            resp = requests.post(gas_url, json=payload, timeout=10)
            if resp.status_code == 200:
                st.success("✅ 제출 완료!")
            else:
                st.error(f"제출 오류 (status {resp.status_code})")
        except Exception as e:
            st.error(f"전송 실패: {e}")
