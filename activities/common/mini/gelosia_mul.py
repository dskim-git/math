# activities/common/mini/gelosia_mul.py
"""
갤로시아 곱셈 (Gelosia Multiplication) 탐구
p5.js 인터랙티브 활동 – 수 버전 & 다항식 버전 빈칸 채우기
"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests

# ── Google Sheets 연동 (공통수학1 전용) ─────────────────────────────────────
_GAS_URL    = "https://script.google.com/macros/s/AKfycbySLDnSYGfQmqrtpuMyIju5hiEf7Lesp6bnWzplm3oZD4WHXESl1XJmsXT_EVcKOJI/exec"
_SHEET_NAME = "갤로시아곱셈"

META = {
    "title":       "✖️ 갤로시아 곱셈 탐구",
    "description": "12세기 인도 수학자 바스카라의 갤로시아 기법으로 정수·다항식 곱셈을 직접 체험하는 활동",
    "order":       31,
    "hidden":      True,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>갤로시아 곱셈 탐구</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
  onload="renderAllMath()"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#e2e8f0;
     padding:14px 10px;min-height:600px}

/* ── Tabs ── */
.tabs{display:flex;gap:6px;margin-bottom:18px;flex-wrap:wrap}
.tab-btn{padding:9px 22px;border-radius:10px;border:2px solid #1e293b;
         background:#141c2b;color:#7a8ea8;cursor:pointer;font-size:14px;
         font-weight:700;transition:all .2s}
.tab-btn.active{background:#1a3a1a;border-color:#22c55e;color:#86efac}
.tab-panel{display:none}.tab-panel.active{display:block}

/* ── Card ── */
.card{background:#161e2e;border:1px solid #1e293b;border-radius:14px;
      padding:18px 20px;margin-bottom:14px}
.card-title{font-size:15px;font-weight:800;color:#7dd3fc;margin-bottom:10px;
            display:flex;align-items:center;gap:7px}
.hint-box{background:#0c2a0c;border:1px solid #166534;border-radius:10px;
          padding:12px 16px;margin-bottom:12px;font-size:13px;color:#a7f3d0;line-height:1.9}

/* ── Problem selector ── */
.prob-selector{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.prob-btn{padding:7px 16px;border-radius:8px;border:2px solid #1e293b;
          background:#141c2b;color:#7a8ea8;cursor:pointer;font-size:12.5px;
          font-weight:700;transition:all .2s}
.prob-btn.active{background:#14532d;border-color:#22c55e;color:#86efac}
.prob-btn.solved{border-color:#0ea5e9;background:#0c2a3e;color:#7dd3fc}

/* ── Gelosia Grid ── */
.gelosia-wrap{display:flex;justify-content:center;margin:16px 0;overflow-x:auto}
.gelosia-outer{position:relative;display:inline-block}

/* header labels */
.col-header{display:flex;justify-content:center;gap:0}
.col-lbl{width:80px;text-align:center;font-size:18px;font-weight:700;color:#fbbf24;
          padding-bottom:6px}
.row-side{display:flex;flex-direction:column;justify-content:center}
.row-lbl{height:80px;display:flex;align-items:center;justify-content:center;
          font-size:18px;font-weight:700;color:#f97316;padding:0 8px}
.gelosia-grid{display:inline-grid;border:3px solid #3b82f6}

/* each cell: 80×80, diagonal line /방향 (왼쪽 상단→오른쪽 하단 경계)
   upper = 왼쪽 위 삼각형 (십의 자리, 10-11시 방향)
   lower = 오른쪽 아래 삼각형 (일의 자리, 4-5시 방향) */
.g-cell{position:relative;width:80px;height:80px;border:1px solid #3b82f6;
         overflow:hidden;background:#0d1b2e}
.g-cell .diag-line{position:absolute;top:0;left:0;width:0;height:0;
  border-style:solid;border-width:80px 80px 0 0;
  border-color:#1e3a5f transparent transparent transparent;pointer-events:none}
.g-cell .upper{position:absolute;top:10px;left:12px;font-size:18px;font-weight:700;
                color:#e2e8f0;z-index:1}
.g-cell .lower{position:absolute;bottom:10px;right:10px;font-size:18px;font-weight:700;
                color:#e2e8f0;z-index:1}
/* input version: 십의자리=왼쪽위(10-11시), 일의자리=오른쪽아래(4-5시) */
.g-cell .inp-upper{position:absolute;top:6px;left:8px;width:30px;height:28px;
  background:#0f172a;border:2px solid #334155;border-radius:5px;
  color:#e2e8f0;text-align:center;font-size:14px;font-weight:700;z-index:2;outline:none}
.g-cell .inp-lower{position:absolute;bottom:6px;right:8px;width:30px;height:28px;
  background:#0f172a;border:2px solid #334155;border-radius:5px;
  color:#e2e8f0;text-align:center;font-size:14px;font-weight:700;z-index:2;outline:none}
.inp-upper.ok,.inp-lower.ok{border-color:#22c55e!important;background:#052e16!important;color:#4ade80!important}
.inp-upper.ng,.inp-lower.ng{border-color:#ef4444!important;background:#2d0a0a!important;color:#f87171!important}

/* diagonal sum area */
.diag-sums{display:flex;gap:0;margin-top:4px;justify-content:flex-end}
.diag-slot{width:80px;text-align:center}
.diag-val{font-size:17px;font-weight:700;color:#86efac;padding:4px 0}
.diag-inp{width:44px;padding:5px 2px;border:2px solid #334155;border-radius:6px;
          background:#0f172a;color:#e2e8f0;font-size:14px;font-weight:700;
          text-align:center;outline:none;transition:.2s}
.diag-inp:focus{border-color:#22c55e}
.diag-inp.ok{border-color:#22c55e!important;background:#052e16!important;color:#4ade80!important}
.diag-inp.ng{border-color:#ef4444!important;background:#2d0a0a!important;color:#f87171!important}

/* result row */
.result-row{display:flex;align-items:center;gap:12px;margin-top:8px;flex-wrap:wrap;justify-content:center}
.result-label{font-size:15px;color:#94a3b8;font-weight:600}
.result-val{font-size:22px;font-weight:800;color:#fbbf24}

/* poly labels */
.poly-lbl{font-size:15px;font-weight:700;color:#fbbf24;font-family:Georgia,serif}
.poly-lbl-blue{color:#7dd3fc}
.poly-coef-lbl{font-size:16px;font-weight:700;color:#fbbf24}

/* carry info */
.carry-box{background:#1a1a0a;border:1px dashed #a16207;border-radius:8px;
           padding:10px 16px;font-size:12.5px;color:#fcd34d;margin-top:8px;line-height:1.8}

/* progress / check button */
.check-btn{padding:10px 28px;border:none;border-radius:9px;background:#15803d;
           color:#fff;font-size:14px;font-weight:700;cursor:pointer;transition:.2s;margin-top:10px}
.check-btn:hover{background:#166534}
.check-btn.all-ok{background:#1d4ed8}
.feedback{margin-top:8px;font-size:13px;font-weight:700;min-height:20px}
.feedback.ok{color:#4ade80}.feedback.ng{color:#f87171}

/* progress bar */
.prog-wrap{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.prog-track{flex:1;height:7px;background:#1e293b;border-radius:99px;overflow:hidden}
.prog-bar{height:100%;background:linear-gradient(90deg,#22c55e,#0ea5e9);
          transition:width .4s;border-radius:99px}
.score-badge{background:#14532d;color:#86efac;border-radius:99px;
             padding:3px 12px;font-size:12px;font-weight:700}

/* intro info box */
.intro-box{background:#0c1a2e;border:1px solid #1e3a5f;border-radius:12px;
           padding:16px 18px;margin-bottom:16px}
.intro-box h3{font-size:14px;font-weight:700;color:#7dd3fc;margin-bottom:8px}
.intro-box p,.intro-box li{font-size:13px;color:#b0c4de;line-height:1.9}
.intro-box ul{padding-left:18px}

/* step highlight */
.hl-orange{color:#fb923c;font-weight:700}
.hl-green{color:#4ade80;font-weight:700}
.hl-blue{color:#60a5fa;font-weight:700}
.hl-yellow{color:#fbbf24;font-weight:700}

@media(max-width:500px){
  .col-lbl,.row-lbl{font-size:14px}
  .g-cell{width:62px;height:62px}
  .g-cell .diag-line{border-width:62px 62px 0 0}
  .col-lbl{width:62px}
  .row-lbl{height:62px}
  .diag-slot{width:62px}
  .g-cell .inp-upper{width:24px;height:22px;font-size:11px;top:4px;left:4px}
  .g-cell .inp-lower{width:24px;height:22px;font-size:11px;bottom:4px;right:4px}
  .diag-inp{width:36px;font-size:12px}
}
</style>
</head>
<body>

<!-- ────────────────── Header ────────────────── -->
<div style="text-align:center;margin-bottom:16px">
  <div style="font-size:1.5rem;font-weight:800;color:#86efac;margin-bottom:4px">
    ✖️ 갤로시아 곱셈 탐구
  </div>
  <div style="font-size:12.5px;color:#64748b">
    12세기 인도 수학자 바스카라의 《릴라바티》에 소개된 격자 곱셈법
  </div>
</div>

<!-- progress -->
<div class="prog-wrap">
  <div class="prog-track"><div class="prog-bar" id="progBar" style="width:0%"></div></div>
  <div class="score-badge">해결 <span id="progTxt">0 / 0</span></div>
</div>

<!-- ────────────────── Tabs ────────────────── -->
<div class="tabs">
  <button class="tab-btn active" id="tabNumBtn" onclick="switchTab('num',this)">🔢 수 버전</button>
  <button class="tab-btn" id="tabPolyBtn" onclick="switchTab('poly',this)">📐 다항식 버전</button>
</div>

<!-- ══════════════ TAB: 수 버전 ══════════════ -->
<div id="tab-num" class="tab-panel active">

  <div class="intro-box">
    <h3>🔹 갤로시아 곱셈 방법 (수 버전)</h3>
    <ul>
      <li><span class="hl-yellow">각 자릿수끼리의 곱</span>을 격자 셀 안에 
          <span class="hl-orange">십의 자리</span>(위쪽 삼각형)와 
          <span class="hl-blue">일의 자리</span>(아래쪽 삼각형)로 분리해서 씁니다.</li>
      <li>셀을 모두 채웠으면 <span class="hl-green">대각선 방향으로 숫자들의 합</span>을 구합니다 (오른쪽 위→왼쪽 아래).</li>
      <li>대각선 합이 10 이상이면 <span class="hl-orange">올림(carry)</span>을 합니다.</li>
      <li>결과를 위→아래, 왼쪽→오른쪽 순서로 읽으면 최종 곱이 됩니다.</li>
    </ul>
  </div>

  <div class="card">
    <div class="card-title">✏️ 문제 선택</div>
    <div class="prob-selector" id="numProbSel"></div>
  </div>

  <div class="card" id="numProbCard">
    <div class="card-title" id="numProbTitle">문제</div>
    <div class="hint-box" id="numHint"></div>
    <div id="numGridWrap"></div>
    <button class="check-btn" id="numCheckBtn" onclick="checkNum()">✅ 채점하기</button>
    <div class="feedback" id="numFeedback"></div>
    <div id="numResult" style="display:none;margin-top:12px;padding:14px;
         background:#052e16;border:1px solid #166534;border-radius:10px">
      <div id="numResultText" style="font-size:14px;color:#a7f3d0;line-height:2"></div>
    </div>
  </div>
</div>

<!-- ══════════════ TAB: 다항식 버전 ══════════════ -->
<div id="tab-poly" class="tab-panel">

  <div class="intro-box">
    <h3>🔹 갤로시아 곱셈 방법 (다항식 버전)</h3>
    <ul>
      <li>수 버전과 완전히 같은 격자 구조! 단, 각 자릿수 대신 
          <span class="hl-yellow">각 항의 계수끼리의 곱</span>을 씁니다.</li>
      <li>셀 안에는 <span class="hl-orange">곱의 계수값</span>만 기록합니다 (부호 포함).</li>
      <li>셀들의 대각선 방향이 <span class="hl-green">같은 차수의 항</span>을 의미합니다.</li>
      <li>대각선 합 = 해당 차수의 <span class="hl-blue">최종 계수</span></li>
      <li>아래쪽의 계수들을 조합하면 <span class="hl-yellow">곱 다항식</span>이 완성됩니다.</li>
    </ul>
  </div>

  <div class="card">
    <div class="card-title">✏️ 문제 선택</div>
    <div class="prob-selector" id="polyProbSel"></div>
  </div>

  <div class="card" id="polyProbCard">
    <div class="card-title" id="polyProbTitle">문제</div>
    <div class="hint-box" id="polyHint"></div>
    <div id="polyGridWrap"></div>
    <button class="check-btn" id="polyCheckBtn" onclick="checkPoly()">✅ 채점하기</button>
    <div class="feedback" id="polyFeedback"></div>
    <div id="polyResult" style="display:none;margin-top:12px;padding:14px;
         background:#052e16;border:1px solid #166534;border-radius:10px">
      <div id="polyResultText" style="font-size:14px;color:#a7f3d0;line-height:2"></div>
    </div>
  </div>
</div>

<!-- ══════════════ SCRIPT ══════════════ -->
<script>
// ── KaTeX ──
function renderAllMath(){
  if(!window.renderMathInElement) return;
  renderMathInElement(document.body,{
    delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
    throwOnError:false
  });
}
function renderNode(el){
  if(!window.renderMathInElement){setTimeout(()=>renderNode(el),150);return;}
  renderMathInElement(el,{
    delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
    throwOnError:false
  });
}

// ── Tab switch ──
let curTab='num';
function switchTab(id,btn){
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  btn.classList.add('active');
  curTab=id;
  updateProgress();
  renderAllMath();
}

// ── Progress ──
const solvedNum=new Set(), solvedPoly=new Set();
function updateProgress(){
  const total = NUM_PROBS.length + POLY_PROBS.length;
  const done  = solvedNum.size + solvedPoly.size;
  document.getElementById('progBar').style.width = (done/total*100)+'%';
  document.getElementById('progTxt').textContent = done+' / '+total;
}

// ═══════════════════════════════════════════════
// 수 버전 문제 데이터
// 각 셀: row=0..R-1, col=0..C-1
// product digit A[row] * B[col] → tens (upper), units (lower)
// ═══════════════════════════════════════════════
const NUM_PROBS = [
  {
    label:'①  61 × 45',
    numA: [6,1], numB: [4,5],
    title: '61 × 45 를 갤로시아 격자로 계산하기'
  },
  {
    label:'②  73 × 28',
    numA: [7,3], numB: [2,8],
    title: '73 × 28 를 갤로시아 격자로 계산하기'
  },
  {
    label:'③  94 × 37',
    numA: [9,4], numB: [3,7],
    title: '94 × 37 를 갤로시아 격자로 계산하기'
  },
  {
    label:'④  328 × 45',
    numA: [3,2,8], numB: [4,5],
    title: '328 × 45 를 갤로시아 격자로 계산하기'
  },
  {
    label:'⑤  156 × 237',
    numA: [1,5,6], numB: [2,3,7],
    title: '156 × 237 를 갤로시아 격자로 계산하기'
  },
];

let curNumProb = 0;

function buildNumProbSel(){
  const sel = document.getElementById('numProbSel');
  sel.innerHTML = '';
  NUM_PROBS.forEach((p,i)=>{
    const btn = document.createElement('button');
    btn.className = 'prob-btn'
      +(i===curNumProb?' active':'')
      +(solvedNum.has(i)?' solved':'');
    btn.textContent = p.label + (solvedNum.has(i)?' ✅':'');
    btn.onclick = ()=>loadNumProb(i);
    sel.appendChild(btn);
  });
}

function loadNumProb(idx){
  curNumProb = idx;
  buildNumProbSel();
  const p = NUM_PROBS[idx];
  document.getElementById('numProbTitle').textContent = '✏️ ' + p.title;

  const R = p.numB.length, C = p.numA.length;
  document.getElementById('numHint').innerHTML =
    `<strong>방법 안내:</strong><br>
     ① 각 셀에 <span class="hl-yellow">${p.numA.join('')} 의 각 자리</span>(열) ×
        <span class="hl-orange">${p.numB.join('')} 의 각 자리</span>(행) 곱을 구하세요.<br>
     ② 곱의 <span class="hl-orange">십의 자리</span>는 <strong>왼쪽 위(▲, 10-11시 방향)</strong>에,
        <span class="hl-blue">일의 자리</span>는 <strong>오른쪽 아래(▼, 4-5시 방향)</strong>에 입력하세요.<br>
     ③ 각 대각선의 합을 구하고 (10 이상이면 올림), 결과를 읽으세요.`;

  renderNumGrid(p);
  document.getElementById('numFeedback').textContent='';
  document.getElementById('numFeedback').className='feedback';
  document.getElementById('numResult').style.display='none';
  document.getElementById('numCheckBtn').className='check-btn';
  document.getElementById('numCheckBtn').textContent='✅ 채점하기';
  document.getElementById('numCheckBtn').disabled=false;
}

function renderNumGrid(p){
  const R=p.numB.length, C=p.numA.length;
  const wrap=document.getElementById('numGridWrap');
  const CELL=80, LW=52, RW=46, HDR=32;

  // Cell products
  const cellVals=[];
  for(let r=0;r<R;r++){
    const row=[];
    for(let c=0;c<C;c++) row.push(p.numB[r]*p.numA[c]);
    cellVals.push(row);
  }

  // Diagonal sums: nDiag=R+C
  // upper(r,c) → diagonal d = r+c  (십의 자리, 왼쪽 위 삼각형)
  // lower(r,c) → diagonal d = r+c+1 (일의 자리, 오른쪽 아래 삼각형)
  const nDiag=R+C;
  const diagSumsFinal=new Array(nDiag).fill(0);
  for(let r=0;r<R;r++)
    for(let c=0;c<C;c++){
      const prod=cellVals[r][c];
      diagSumsFinal[r+c]  +=Math.floor(prod/10);
      diagSumsFinal[r+c+1]+=prod%10;
    }
  // Carry propagation (least → most significant)
  const resultDigits=[...diagSumsFinal];
  for(let d=nDiag-1;d>0;d--){
    if(resultDigits[d]>=10){
      resultDigits[d-1]+=Math.floor(resultDigits[d]/10);
      resultDigits[d]%=10;
    }
  }

  // HTML layout:
  //   [LW 왼쪽 대각선 칸] [위쪽 열 레이블] [RW 오른쪽 행 레이블]
  //   [diag d=r 왼쪽]     [격자 row r]     [numB[r] 오른쪽]
  //                        [아래쪽 대각선 칸: col 0..C-1]
  let html=`<div style="overflow-x:auto"><div style="display:inline-flex;flex-direction:column;align-items:flex-start">`;

  // 위쪽 열 레이블 행
  html+=`<div style="display:flex;align-items:flex-end;height:${HDR}px">`;
  html+=`<div style="width:${LW}px"></div>`;
  p.numA.forEach(d=>{
    html+=`<div style="width:${CELL}px;text-align:center;font-size:19px;font-weight:700;color:#fbbf24;padding-bottom:4px">${d}</div>`;
  });
  html+=`<div style="width:${RW}px"></div>`;
  html+=`</div>`;

  // 격자 행: [왼쪽 대각선 입력] [셀들] [오른쪽 행 레이블]
  for(let r=0;r<R;r++){
    html+=`<div style="display:flex;align-items:center">`;
    // 왼쪽 대각선 입력 (d=r)
    html+=`<div style="width:${LW}px;height:${CELL}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px">
      <div style="font-size:9px;color:#f97316;font-weight:700">대각${r+1}</div>
      <input class="diag-inp" id="numDiag_${r}" data-ans="${diagSumsFinal[r]}" type="number" placeholder="?" style="width:40px">
    </div>`;
    // 셀들
    html+=`<div style="display:inline-grid;grid-template-columns:repeat(${C},${CELL}px)">`;
    for(let c=0;c<C;c++){
      const prod=cellVals[r][c], u=Math.floor(prod/10), l=prod%10;
      html+=`<div class="g-cell"><div class="diag-line"></div>
        <input class="inp-upper" data-r="${r}" data-c="${c}" data-ans-u="${u}" type="number" min="0" max="9" placeholder="?">
        <input class="inp-lower" data-r="${r}" data-c="${c}" data-ans-l="${l}" type="number" min="0" max="9" placeholder="?">
      </div>`;
    }
    html+=`</div>`;
    // 오른쪽 행 레이블
    html+=`<div style="width:${RW}px;height:${CELL}px;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:700;color:#f97316">${p.numB[r]}</div>`;
    html+=`</div>`;
  }

  // 아래쪽 대각선 입력 (d=R..R+C-1), 열 0..C-1 아래에 정렬
  html+=`<div style="display:flex;align-items:flex-start;margin-top:3px">`;
  html+=`<div style="width:${LW}px"></div>`;
  for(let c=0;c<C;c++){
    const d=R+c;
    html+=`<div style="width:${CELL}px;display:flex;flex-direction:column;align-items:center;gap:2px">
      <div style="font-size:9px;color:#f97316;font-weight:700">대각${d+1}</div>
      <input class="diag-inp" id="numDiag_${d}" data-ans="${diagSumsFinal[d]}" type="number" placeholder="?" style="width:40px">
    </div>`;
  }
  html+=`<div style="width:${RW}px"></div>`;
  html+=`</div>`;

  html+=`</div></div>`;

  // 올림 전 힌트 + 정답 공개
  const carryInfo=diagSumsFinal.map((v,i)=>`대각${i+1}합=${v}`).join(' / ');
  html+=`<div class="carry-box" style="margin-top:8px">💡 올림 전 대각선 합 → ${carryInfo}<br>
         올림 처리 후 결과: <strong id="numFinalAns" style="color:#fbbf24">?</strong>
         <span style="color:#64748b;font-size:11px"> (채점 후 공개)</span></div>`;

  wrap.innerHTML=html;
}

function checkNum(){
  const p = NUM_PROBS[curNumProb];
  // Check cell inputs
  const uppers = document.querySelectorAll('#numGridWrap .inp-upper');
  const lowers  = document.querySelectorAll('#numGridWrap .inp-lower');
  const diagInps= document.querySelectorAll('#numGridWrap .diag-inp');
  let allOk=true, wrong=0;

  uppers.forEach(inp=>{
    const ans=parseInt(inp.dataset.ansU);
    const val=parseInt(inp.value);
    if(isNaN(val)||val!==ans){inp.classList.add('ng');inp.classList.remove('ok');allOk=false;wrong++;}
    else{inp.classList.add('ok');inp.classList.remove('ng');}
  });
  lowers.forEach(inp=>{
    const ans=parseInt(inp.dataset.ansL);
    const val=parseInt(inp.value);
    if(isNaN(val)||val!==ans){inp.classList.add('ng');inp.classList.remove('ok');allOk=false;wrong++;}
    else{inp.classList.add('ok');inp.classList.remove('ng');}
  });
  diagInps.forEach(inp=>{
    const ans=parseInt(inp.dataset.ans);
    const val=parseInt(inp.value);
    if(isNaN(val)||val!==ans){inp.classList.add('ng');inp.classList.remove('ok');allOk=false;wrong++;}
    else{inp.classList.add('ok');inp.classList.remove('ng');}
  });

  const expectedAnswer = p.numA.reduce((a,b,i)=>{
    return a+(b*Math.pow(10,p.numA.length-1-i));
    },0) * p.numB.reduce((a,b,i)=>{
    return a+(b*Math.pow(10,p.numB.length-1-i));
    },0);

  const fb=document.getElementById('numFeedback');
  if(allOk){
    fb.textContent='🎉 모두 정답입니다!'; fb.className='feedback ok';
    document.getElementById('numCheckBtn').className='check-btn all-ok';
    document.getElementById('numCheckBtn').disabled=true;
    document.getElementById('numFinalAns').textContent = expectedAnswer;
    document.getElementById('numResult').style.display='block';
    document.getElementById('numResultText').innerHTML =
      `<strong>${p.numA.join('')} × ${p.numB.join('')} = <span style="color:#fbbf24;font-size:22px">${expectedAnswer}</span></strong><br>
       갤로시아 격자가 정확히 완성됐습니다! ✅`;
    solvedNum.add(curNumProb);
    buildNumProbSel(); updateProgress();
  } else {
    fb.textContent=`❌ 틀린 칸이 ${wrong}개 있습니다. 다시 확인해보세요.`;
    fb.className='feedback ng';
  }
}

// ═══════════════════════════════════════════════
// 다항식 버전 문제 데이터
// coeffA, coeffB: 내림차순 계수 배열
// termLabelsA, termLabelsB: 각 항의 표현 문자열
// ═══════════════════════════════════════════════
const POLY_PROBS = [
  {
    label:'① (2x+3)(x−1)',
    coeffA:[2,3], coeffB:[1,-1],
    labelsA:['2x','3'], labelsB:['x','−1'],
    degA:1, degB:1,
    title:'(2x+3)(x−1) 를 갤로시아 격자로 계산하기',
  },
  {
    label:'② (3x+1)(2x²−5x+4)',
    coeffA:[3,1], coeffB:[2,-5,4],
    labelsA:['3x','1'], labelsB:['2x²','−5x','4'],
    degA:1, degB:2,
    title:'(3x+1)(2x²−5x+4) 를 갤로시아 격자로 계산하기',
  },
  {
    label:'③ (x²−3x+2)(x+4)',
    coeffA:[1,-3,2], coeffB:[1,4],
    labelsA:['x²','−3x','2'], labelsB:['x','4'],
    degA:2, degB:1,
    title:'(x²−3x+2)(x+4) 를 갤로시아 격자로 계산하기',
  },
  {
    label:'④ (2x²−x+3)(x²+2x−1)',
    coeffA:[2,-1,3], coeffB:[1,2,-1],
    labelsA:['2x²','−x','3'], labelsB:['x²','2x','−1'],
    degA:2, degB:2,
    title:'(2x²−x+3)(x²+2x−1) 를 갤로시아 격자로 계산하기',
  },
];

let curPolyProb=0;

function buildPolyProbSel(){
  const sel=document.getElementById('polyProbSel');
  sel.innerHTML='';
  POLY_PROBS.forEach((p,i)=>{
    const btn=document.createElement('button');
    btn.className='prob-btn'
      +(i===curPolyProb?' active':'')
      +(solvedPoly.has(i)?' solved':'');
    btn.textContent=p.label+(solvedPoly.has(i)?' ✅':'');
    btn.onclick=()=>loadPolyProb(i);
    sel.appendChild(btn);
  });
}

function loadPolyProb(idx){
  curPolyProb=idx;
  buildPolyProbSel();
  const p=POLY_PROBS[idx];
  document.getElementById('polyProbTitle').textContent='✏️ '+p.title;

  document.getElementById('polyHint').innerHTML =
    `<strong>방법 안내:</strong><br>
     ① 열: <span class="hl-yellow">${p.labelsA.join(', ')}</span> (첫 번째 다항식의 각 항)<br>
     ② 행: <span class="hl-orange">${p.labelsB.join(', ')}</span> (두 번째 다항식의 각 항)<br>
     ③ 각 셀에 <span class="hl-blue">두 항 계수의 곱</span>을 입력하세요 (부호 포함).<br>
     ④ 같은 대각선(= 같은 차수)들의 합이 해당 차수의 최종 계수입니다.`;

  renderPolyGrid(p);
  document.getElementById('polyFeedback').textContent='';
  document.getElementById('polyFeedback').className='feedback';
  document.getElementById('polyResult').style.display='none';
  document.getElementById('polyCheckBtn').className='check-btn';
  document.getElementById('polyCheckBtn').textContent='✅ 채점하기';
  document.getElementById('polyCheckBtn').disabled=false;
  renderAllMath();
}

// Power string helper
function powStr(deg,base='x'){
  if(deg===0) return '';
  if(deg===1) return base;
  return base+'<sup>'+deg+'</sup>';
}
function termStr(coef,deg){
  if(coef===0) return '';
  const s=Math.abs(coef)===1&&deg>0?'':Math.abs(coef).toString();
  const sign=coef<0?'−':'+';
  return sign+s+powStr(deg);
}

function renderPolyGrid(p){
  const R=p.coeffB.length, C=p.coeffA.length;
  const wrap=document.getElementById('polyGridWrap');
  const CELL=80, LW=62, RW=70, HDR=32;

  // Cell products
  const cellVals=[];
  for(let r=0;r<R;r++){
    const row=[];
    for(let c=0;c<C;c++) row.push(p.coeffB[r]*p.coeffA[c]);
    cellVals.push(row);
  }

  // Diagonal sums: nDiag=R+C-1, d=r+c (0=최고차항)
  const nDiag=R+C-1;
  const diagSums=new Array(nDiag).fill(0);
  for(let r=0;r<R;r++)
    for(let c=0;c<C;c++)
      diagSums[r+c]+=cellVals[r][c];

  const maxDeg=p.degA+p.degB;

  function degLabel(d){
    const deg=maxDeg-d;
    if(deg>1) return `x<sup>${deg}</sup>항`;
    if(deg===1) return `x항`;
    return `상수`;
  }

  // HTML layout:
  //   [LW 왼쪽 대각선 칸] [위쪽 열 레이블] [RW 오른쪽 행 레이블]
  //   [diag d=r]           [격자 row r]     [labelsB[r]]
  //                         [col0 여백] [d=R..nDiag-1 열1..C-1 아래]
  let html=`<div style="overflow-x:auto"><div style="display:inline-flex;flex-direction:column;align-items:flex-start">`;

  // 위쪽 열 레이블
  html+=`<div style="display:flex;align-items:flex-end;height:${HDR}px">`;
  html+=`<div style="width:${LW}px"></div>`;
  p.labelsA.forEach(l=>{
    html+=`<div style="width:${CELL}px;text-align:center;font-size:13px;font-weight:700;color:#fbbf24;padding-bottom:4px">${l}</div>`;
  });
  html+=`<div style="width:${RW}px"></div>`;
  html+=`</div>`;

  // 격자 행
  for(let r=0;r<R;r++){
    html+=`<div style="display:flex;align-items:center">`;
    // 왼쪽 대각선 입력 d=r
    html+=`<div style="width:${LW}px;height:${CELL}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px">
      <div style="font-size:9px;color:#7dd3fc;text-align:center">${degLabel(r)}</div>
      <input class="diag-inp" id="polyDiag_${r}" data-ans="${diagSums[r]}" type="number" placeholder="?" style="width:44px">
    </div>`;
    // 셀들 (다항식 버전은 중앙 단일 입력)
    html+=`<div style="display:inline-grid;grid-template-columns:repeat(${C},${CELL}px)">`;
    for(let c=0;c<C;c++){
      const ans=cellVals[r][c];
      html+=`<div class="g-cell" style="background:#0d1b30"><div class="diag-line"></div>
        <input class="inp-upper" style="width:44px;top:50%;left:50%;transform:translate(-50%,-50%);font-size:13px"
               data-r="${r}" data-c="${c}" data-ans="${ans}" type="number" placeholder="?">
      </div>`;
    }
    html+=`</div>`;
    // 오른쪽 행 레이블
    html+=`<div style="width:${RW}px;height:${CELL}px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#f97316">${p.labelsB[r]}</div>`;
    html+=`</div>`;
  }

  // 아래쪽 대각선 입력: d=R..nDiag-1, 열1..C-1 아래 (열0 아래는 여백)
  if(C>1){
    html+=`<div style="display:flex;align-items:flex-start;margin-top:4px">`;
    html+=`<div style="width:${LW}px"></div>`;
    html+=`<div style="width:${CELL}px"></div>`; // 열 0 아래 여백 (LEFT 마지막 대각선이 담당)
    for(let c=1;c<C;c++){
      const d=R-1+c; // c=1→d=R, c=2→d=R+1, ..., c=C-1→d=R+C-2=nDiag-1
      html+=`<div style="width:${CELL}px;display:flex;flex-direction:column;align-items:center;gap:2px">
        <div style="font-size:9px;color:#7dd3fc;text-align:center">${degLabel(d)}</div>
        <input class="diag-inp" id="polyDiag_${d}" data-ans="${diagSums[d]}" type="number" placeholder="?" style="width:44px">
      </div>`;
    }
    html+=`<div style="width:${RW}px"></div>`;
    html+=`</div>`;
  }

  // 결과 다항식 표시 영역
  html+=`<div id="polyResultPoly" style="margin-top:12px;padding:10px 14px;
         background:#0c1a30;border:1px solid #1e3a5f;border-radius:8px;
         font-size:14px;color:#a5b4fc;display:none">
    결과 다항식: <span id="polyResultExpr" style="color:#fbbf24;font-size:16px;font-weight:700"></span>
  </div>`;

  html+=`</div></div>`;
  wrap.innerHTML=html;
}

function checkPoly(){
  const p=POLY_PROBS[curPolyProb];
  const cellInps=document.querySelectorAll('#polyGridWrap .inp-upper');
  const diagInps=document.querySelectorAll('#polyGridWrap .diag-inp');
  let allOk=true, wrong=0;

  cellInps.forEach(inp=>{
    const ans=parseInt(inp.dataset.ans);
    const val=parseInt(inp.value);
    if(isNaN(val)||val!==ans){inp.classList.add('ng');inp.classList.remove('ok');allOk=false;wrong++;}
    else{inp.classList.add('ok');inp.classList.remove('ng');}
  });
  diagInps.forEach(inp=>{
    const ans=parseInt(inp.dataset.ans);
    const val=parseInt(inp.value);
    if(isNaN(val)||val!==ans){inp.classList.add('ng');inp.classList.remove('ok');allOk=false;wrong++;}
    else{inp.classList.add('ok');inp.classList.remove('ng');}
  });

  // Build result polynomial string (d=r+c 공식 사용)
  const R=p.coeffB.length, C=p.coeffA.length;
  const nDiag=R+C-1;
  const maxDeg=p.degA+p.degB;
  const diagSums=new Array(nDiag).fill(0);
  for(let r=0;r<R;r++)
    for(let c=0;c<C;c++){
      const d=r+c;
      diagSums[d]+=p.coeffB[r]*p.coeffA[c];
    }
  let polyStr='';
  for(let d=0;d<nDiag;d++){
    const coef=diagSums[d];
    const deg=maxDeg-d;
    if(coef===0) continue;
    polyStr+=termStr(coef,deg);
  }
  polyStr=polyStr.replace(/^\+/,'');

  const fb=document.getElementById('polyFeedback');
  if(allOk){
    fb.textContent='🎉 모두 정답입니다!'; fb.className='feedback ok';
    document.getElementById('polyCheckBtn').className='check-btn all-ok';
    document.getElementById('polyCheckBtn').disabled=true;
    document.getElementById('polyResult').style.display='block';
    document.getElementById('polyResultText').innerHTML=
      `결과: <strong style="color:#fbbf24;font-size:17px">${polyStr}</strong><br>
       갤로시아 격자로 다항식 곱셈 완성! ✅`;
    const rp=document.getElementById('polyResultPoly');
    if(rp){rp.style.display='block'; document.getElementById('polyResultExpr').innerHTML=polyStr;}
    solvedPoly.add(curPolyProb);
    buildPolyProbSel(); updateProgress();
  } else {
    fb.textContent=`❌ 틀린 칸이 ${wrong}개 있습니다. 다시 확인해보세요.`;
    fb.className='feedback ng';
  }
}

// ── Init ──
window.onload=()=>{
  buildNumProbSel(); loadNumProb(0);
  buildPolyProbSel(); loadPolyProb(0);
  updateProgress();
};
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────

def render():
    st.title("✖️ 갤로시아 곱셈 탐구")
    st.markdown(
        "12세기 인도 수학자 **바스카라**의 《릴라바티》에 소개된 **격자 곱셈법(Gelosia)**으로 "
        "정수 곱셈과 다항식 곱셈을 직접 체험해 보세요."
    )
    components.html(_HTML, height=1100, scrolling=False)
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_reflection_form(sheet_name: str, gas_url: str):
    st.divider()
    st.subheader("✍️ 활동 후 성찰 기록")
    st.caption("아래 질문에 답하고 **제출하기** 버튼을 눌러 선생님께 전달해 주세요.")

    with st.form(f"reflection_{sheet_name}", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            student_id = st.text_input("학번")
        with c2:
            name = st.text_input("이름")

        st.markdown("**📝 수 버전 한 문제를 직접 선택해 풀고 과정을 기록해보세요**")
        q_num = st.text_area(
            "선택한 수 곱셈 문제 (예: 73 × 28 등)",
            placeholder="예) 73 × 28",
            height=56
        )
        a_num = st.text_input("격자를 채우고 얻은 최종 답")

        st.markdown("**📝 다항식 버전 한 문제를 직접 선택해 풀고 과정을 기록해보세요**")
        q_poly = st.text_area(
            "선택한 다항식 곱셈 문제",
            placeholder="예) (3x+1)(2x²−5x+4)",
            height=56
        )
        a_poly = st.text_input("격자를 채우고 얻은 곱 다항식")

        new_learning = st.text_area(
            "💡 이 활동을 통해 새롭게 알게 된 점\n"
            "(예: 갤로시아 곱셈과 일반 곱셈이 어떻게 연결되는지 등)",
            height=100
        )
        feeling = st.text_area("💬 이 활동을 하면서 느낀 점", height=90)

        submitted = st.form_submit_button("📤 제출하기", use_container_width=True, type="primary")

    if submitted:
        if not student_id or not name:
            st.warning("학번과 이름을 입력해주세요.")
        else:
            payload = {
                "sheet":        sheet_name,
                "timestamp":    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "학번":         student_id,
                "이름":         name,
                "수문제":       q_num,
                "수답":         a_num,
                "다항식문제":   q_poly,
                "다항식답":     a_poly,
                "새롭게알게된점": new_learning,
                "느낀점":       feeling,
            }
            try:
                resp = requests.post(gas_url, json=payload, timeout=10)
                if resp.status_code == 200:
                    st.success(f"✅ {name}님의 기록이 제출되었습니다!")
                    st.balloons()
                else:
                    st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"네트워크 오류: {e}")
