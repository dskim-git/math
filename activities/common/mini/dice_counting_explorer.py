# activities/common/mini/dice_counting_explorer.py
"""
주사위로 경우의 수 탐구
주사위 1~3개의 결과를 표로 보며 경우의 수를 직관적으로 헤아리는 탐구 활동
"""
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title":       "🎲 주사위로 경우의 수 탐구",
    "description": "주사위 1~3개를 던졌을 때의 결과를 표로 보며 경우의 수를 직관적으로 세는 탐구 활동입니다.",
    "order":       312,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>주사위로 경우의 수 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(145deg,#080d1c 0%,#0c1428 55%,#06091a 100%);
  color:#e2e8ff;
  padding:12px 14px 24px;
  min-height:100vh;
}

.hdr{text-align:center;margin-bottom:14px}
.hdr h1{font-size:1.3rem;color:#ffd700;text-shadow:0 0 18px rgba(255,215,0,.4);margin-bottom:3px}
.hdr p{font-size:.78rem;color:#7788aa}

/* ── 탭 ── */
.tabs{display:flex;gap:6px;margin-bottom:14px;justify-content:center;flex-wrap:wrap}
.tab-btn{
  padding:8px 14px;border-radius:10px;border:1.5px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.04);color:#7788aa;font-size:.82rem;font-weight:600;
  cursor:pointer;font-family:inherit;transition:all .2s
}
.tab-btn.active{background:rgba(124,58,237,.18);border-color:#7c3aed;color:#c084fc}
.tab-btn:hover:not(.active){background:rgba(255,255,255,.08);color:#ccd}

.panel{display:none}
.panel.active{display:block}

/* ── 질문 리스트 ── */
.q-list{display:flex;flex-direction:column;gap:5px;margin-bottom:12px}
.q-btn{
  text-align:left;padding:9px 13px;border-radius:9px;
  border:1.5px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04);
  color:#aabbcc;font-size:.81rem;cursor:pointer;font-family:inherit;
  transition:all .2s;line-height:1.45
}
.q-btn:hover{background:rgba(255,255,255,.08);border-color:#7c3aed55}
.q-btn.sel{background:rgba(124,58,237,.15);border-color:#7c3aed;color:#e2e8ff}

/* ── 결과 박스 ── */
.result-box{
  display:none;text-align:center;padding:11px 14px;
  background:rgba(124,58,237,.12);border:1.5px solid #7c3aed;
  border-radius:12px;margin-bottom:12px;animation:fadein .3s ease
}
.result-box.show{display:block}
.result-count{
  font-size:2rem;font-weight:700;
  background:linear-gradient(135deg,#ffd700,#ff9944);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent
}
.result-hint{font-size:.76rem;color:#8899bb;margin-top:4px;line-height:1.55}

/* ── 범례 ── */
.legend{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px;align-items:center}
.legend-item{display:flex;align-items:center;gap:5px;font-size:.74rem;color:#7788aa}
.ld{width:14px;height:14px;border-radius:3px}
.ld-hl{background:rgba(255,215,0,.35);border:1px solid #ffd700}
.ld-no{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1)}

/* ── Tab1: 주사위 1개 ── */
.dice-row-wrap{
  display:flex;gap:8px;justify-content:center;flex-wrap:wrap;
  padding:18px 12px;background:rgba(0,0,0,.25);border-radius:12px;margin-bottom:12px
}
.die-face{
  width:64px;height:64px;border-radius:13px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.12);
  transition:all .25s
}
.die-face .die-num{font-size:1.65rem;font-weight:700;color:#e2e8ff;line-height:1}
.die-face .die-sub{font-size:.6rem;color:#7788aa;margin-top:2px}
.die-face.hl{
  background:rgba(255,215,0,.22)!important;border-color:#ffd700!important;
  box-shadow:0 0 18px rgba(255,215,0,.45);transform:scale(1.1)
}
.die-face.dim{opacity:.28;transform:scale(.95)}

/* ── Tab2: 주사위 2개 ── */
.mode-row{display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap}
.mode-btn{
  padding:6px 13px;border-radius:8px;border:1.5px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.04);color:#7788aa;font-size:.79rem;font-weight:600;
  cursor:pointer;font-family:inherit;transition:all .2s
}
.mode-btn.active{background:rgba(8,145,178,.16);border-color:#0891b2;color:#22d3ee}
.mode-btn:hover:not(.active){background:rgba(255,255,255,.07)}

.tbl-wrap{overflow-x:auto;margin-bottom:12px}
table.dtbl{border-collapse:collapse;margin:0 auto}
table.dtbl th,table.dtbl td{
  width:46px;height:44px;text-align:center;vertical-align:middle;
  font-size:.88rem;border:1px solid rgba(255,255,255,.07)
}
table.dtbl th{font-size:.74rem;font-weight:700;background:rgba(0,0,0,.3)}
table.dtbl th.corner{
  background:rgba(0,0,0,.45);font-size:.62rem;color:#445566;
  line-height:1.3;padding:2px
}
table.dtbl th.hc{color:#c084fc;background:rgba(124,58,237,.14)}
table.dtbl th.hr{color:#38bdf8;background:rgba(14,165,233,.1)}
table.dtbl td{
  background:rgba(255,255,255,.04);color:#99aabb;
  transition:background .15s,color .15s
}
table.dtbl td.hl{
  background:rgba(255,215,0,.28)!important;color:#ffd700!important;
  font-weight:700;box-shadow:inset 0 0 8px rgba(255,215,0,.25)
}

/* ── Tab3: 주사위 3개 ── */
.info3{
  font-size:.79rem;color:#7788aa;margin-bottom:10px;
  padding:8px 11px;background:rgba(0,0,0,.2);border-radius:8px;line-height:1.6
}
.grids3{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:12px}
.mg-card{
  background:rgba(0,0,0,.22);border:1px solid rgba(255,255,255,.07);
  border-radius:9px;padding:7px;text-align:center
}
.mg-label{font-size:.7rem;font-weight:700;color:#7788aa;margin-bottom:4px}
.mg-label span{color:#22d3ee;font-size:.78rem}
table.mt{border-collapse:collapse;margin:0 auto}
table.mt th,table.mt td{
  width:22px;height:22px;text-align:center;vertical-align:middle;
  font-size:.58rem;border:1px solid rgba(255,255,255,.05)
}
table.mt th{background:rgba(0,0,0,.3);color:#445566;font-weight:600}
table.mt th.rh{color:#c084fc}
table.mt th.ch{color:#fbbf24}
table.mt td{
  background:rgba(255,255,255,.04);color:transparent;
  transition:background .15s
}
table.mt td.hl{
  background:rgba(255,215,0,.35)!important;
  box-shadow:inset 0 0 6px rgba(255,215,0,.3)
}
.mg-cnt{margin-top:4px;font-size:.67rem;color:#556677}
.mg-cnt span{color:#ffd700;font-weight:700}

@keyframes fadein{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}

@media(max-width:460px){
  .grids3{grid-template-columns:repeat(2,1fr)}
  table.dtbl th,table.dtbl td{width:38px;height:38px;font-size:.8rem}
}
</style>
</head>
<body>

<div class="hdr">
  <h1>🎲 주사위로 경우의 수 탐구</h1>
  <p>조건에 맞는 경우를 표에서 직접 찾아 경우의 수를 헤아려 보세요!</p>
</div>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab(1)">🎲 주사위 1개</button>
  <button class="tab-btn" onclick="switchTab(2)">🎲🎲 주사위 2개</button>
  <button class="tab-btn" onclick="switchTab(3)">🎲🎲🎲 주사위 3개</button>
</div>

<!-- ══ Tab 1 ══ -->
<div class="panel active" id="panel1">
  <div class="q-list" id="qList1"></div>
  <div class="result-box" id="result1">
    <div class="result-count" id="cnt1"></div>
    <div class="result-hint" id="hint1"></div>
  </div>
  <div class="dice-row-wrap" id="diceRow"></div>
  <div class="legend">
    <div class="legend-item"><div class="ld ld-hl"></div>조건에 맞는 경우</div>
    <div class="legend-item"><div class="ld ld-no"></div>조건에 맞지 않는 경우</div>
  </div>
</div>

<!-- ══ Tab 2 ══ -->
<div class="panel" id="panel2">
  <div class="mode-row">
    <button class="mode-btn active" onclick="setMode('sum')">⊕ 두 눈의 합</button>
    <button class="mode-btn" onclick="setMode('prod')">✕ 두 눈의 곱</button>
    <button class="mode-btn" onclick="setMode('min')">↓ 최솟값</button>
    <button class="mode-btn" onclick="setMode('max')">↑ 최댓값</button>
  </div>
  <div class="q-list" id="qList2"></div>
  <div class="result-box" id="result2">
    <div class="result-count" id="cnt2"></div>
    <div class="result-hint" id="hint2"></div>
  </div>
  <div class="tbl-wrap"><table class="dtbl" id="tbl2"></table></div>
  <div class="legend">
    <div class="legend-item"><div class="ld ld-hl"></div>조건에 맞는 경우</div>
    <div class="legend-item"><div class="ld ld-no"></div>조건에 맞지 않는 경우</div>
  </div>
</div>

<!-- ══ Tab 3 ══ -->
<div class="panel" id="panel3">
  <div class="info3">
    <strong style="color:#22d3ee">파랑 주사위</strong> 값에 따라 6개의 표로 나누었어요.
    각 표에서 <strong style="color:#c084fc">빨강(행)</strong>과 <strong style="color:#fbbf24">초록(열)</strong>의 결과를 확인하세요.
    &nbsp;전체 경우의 수: <strong style="color:#ffd700">6 × 6 × 6 = 216</strong>가지
  </div>
  <div class="q-list" id="qList3"></div>
  <div class="result-box" id="result3">
    <div class="result-count" id="cnt3"></div>
    <div class="result-hint" id="hint3"></div>
  </div>
  <div class="grids3" id="grids3"></div>
  <div class="legend">
    <div class="legend-item"><div class="ld ld-hl"></div>조건에 맞는 경우</div>
    <div class="legend-item"><div class="ld ld-no"></div>조건에 맞지 않는 경우</div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);

// ── 탭 전환 ─────────────────────────────────────────────────────
function switchTab(n) {
  [1,2,3].forEach(i => $('panel'+i).classList.toggle('active', i===n));
  document.querySelectorAll('.tab-btn').forEach((b,i) => b.classList.toggle('active', i===n-1));
}

// ═══════════════════════════════════════════════════════════════
// Tab 1: 주사위 1개
// ═══════════════════════════════════════════════════════════════
const Q1 = [
  {
    q:"짝수의 눈이 나오는 경우는?",
    cond:d=>d%2===0, answer:3,
    hint:"해당: {2, 4, 6} → 3가지"
  },
  {
    q:"홀수의 눈이 나오는 경우는?",
    cond:d=>d%2===1, answer:3,
    hint:"해당: {1, 3, 5} → 3가지"
  },
  {
    q:"소수의 눈이 나오는 경우는?",
    cond:d=>[2,3,5].includes(d), answer:3,
    hint:"해당: {2, 3, 5} → 3가지  (1은 소수가 아니에요!)"
  },
  {
    q:"4 이상의 눈이 나오는 경우는?",
    cond:d=>d>=4, answer:3,
    hint:"해당: {4, 5, 6} → 3가지"
  },
  {
    q:"3의 배수의 눈이 나오는 경우는?",
    cond:d=>d%3===0, answer:2,
    hint:"해당: {3, 6} → 2가지"
  },
  {
    q:"짝수이거나 3의 배수인 눈이 나오는 경우는? (합의 법칙 적용!)",
    cond:d=>d%2===0||d%3===0, answer:4,
    hint:"짝수 {2,4,6} 3가지, 3의 배수 {3,6} 2가지, 공통 {6} → 3 + 2 − 1 = 4가지"
  },
];

function buildTab1() {
  const ql = $('qList1');
  Q1.forEach((q,i) => {
    const b = document.createElement('button');
    b.className = 'q-btn';
    b.textContent = `Q${i+1}. ${q.q}`;
    b.onclick = () => selQ1(i);
    ql.appendChild(b);
  });
  const row = $('diceRow');
  for(let d=1;d<=6;d++){
    const div = document.createElement('div');
    div.className = 'die-face';
    div.id = 'd1'+d;
    div.innerHTML = `<div class="die-num">${d}</div><div class="die-sub">눈 ${d}</div>`;
    row.appendChild(div);
  }
}

function selQ1(i) {
  document.querySelectorAll('#qList1 .q-btn').forEach((b,j)=>b.classList.toggle('sel',j===i));
  const q = Q1[i];
  for(let d=1;d<=6;d++){
    const el=$('d1'+d);
    const m=q.cond(d);
    el.classList.toggle('hl',m);
    el.classList.toggle('dim',!m);
  }
  $('result1').classList.add('show');
  $('cnt1').textContent = q.answer + ' 가지';
  $('hint1').textContent = q.hint;
}

// ═══════════════════════════════════════════════════════════════
// Tab 2: 주사위 2개
// ═══════════════════════════════════════════════════════════════
const MODES = {
  sum: { fn:(a,b)=>a+b },
  prod:{ fn:(a,b)=>a*b },
  min: { fn:(a,b)=>Math.min(a,b) },
  max: { fn:(a,b)=>Math.max(a,b) },
};

const Q2 = {
  sum:[
    { q:"두 눈의 합이 7인 경우는?",
      cond:(a,b)=>a+b===7, answer:6,
      hint:"(1,6)(2,5)(3,4)(4,3)(5,2)(6,1) → 6가지" },
    { q:"두 눈의 합이 5 이하인 경우는?",
      cond:(a,b)=>a+b<=5, answer:10,
      hint:"(1,1)(1,2)(1,3)(1,4)(2,1)(2,2)(2,3)(3,1)(3,2)(4,1) → 10가지" },
    { q:"두 눈의 합이 짝수인 경우는?",
      cond:(a,b)=>(a+b)%2===0, answer:18,
      hint:"둘 다 짝수(3×3=9가지) 또는 둘 다 홀수(3×3=9가지) → 9+9 = 18가지" },
    { q:"두 눈의 합이 10 이상인 경우는?",
      cond:(a,b)=>a+b>=10, answer:6,
      hint:"(4,6)(5,5)(5,6)(6,4)(6,5)(6,6) → 6가지" },
  ],
  prod:[
    { q:"두 눈의 곱이 12인 경우는?",
      cond:(a,b)=>a*b===12, answer:4,
      hint:"(2,6)(3,4)(4,3)(6,2) → 4가지" },
    { q:"두 눈의 곱이 6 이하인 경우는?",
      cond:(a,b)=>a*b<=6, answer:14,
      hint:"(1,1~6): 6가지, (2,1~3): 3가지, (3,1~2): 2가지, (4,1)(5,1)(6,1) → 14가지" },
    { q:"두 눈의 곱이 홀수인 경우는?",
      cond:(a,b)=>(a*b)%2===1, answer:9,
      hint:"두 눈 모두 홀수여야 함 → {1,3,5}×{1,3,5} = 3×3 = 9가지" },
    { q:"두 눈의 곱이 완전제곱수인 경우는?",
      cond:(a,b)=>{const v=a*b;return [1,4,9,16,25,36].includes(v);}, answer:14,
      hint:"곱이 1,4,9,16,25,36인 경우를 표에서 세어 보세요 → 14가지" },
  ],
  min:[
    { q:"두 눈의 최솟값이 3인 경우는?",
      cond:(a,b)=>Math.min(a,b)===3, answer:7,
      hint:"(3,3)(3,4)(3,5)(3,6)(4,3)(5,3)(6,3) → 7가지" },
    { q:"두 눈의 최솟값이 4 이상인 경우는?",
      cond:(a,b)=>Math.min(a,b)>=4, answer:9,
      hint:"두 눈 모두 4 이상 → {4,5,6}×{4,5,6} = 3×3 = 9가지" },
    { q:"두 눈의 최솟값이 2 이하인 경우는?",
      cond:(a,b)=>Math.min(a,b)<=2, answer:20,
      hint:"전체 36 − 최솟값이 3 이상인 경우(4×4=16) = 36−16 = 20가지" },
    { q:"두 눈의 최솟값과 최댓값이 같은 경우는?",
      cond:(a,b)=>a===b, answer:6,
      hint:"두 눈이 같은 경우 → (1,1)(2,2)(3,3)(4,4)(5,5)(6,6) → 6가지" },
  ],
  max:[
    { q:"두 눈의 최댓값이 4인 경우는?",
      cond:(a,b)=>Math.max(a,b)===4, answer:7,
      hint:"(4,1)(4,2)(4,3)(4,4)(1,4)(2,4)(3,4) → 7가지" },
    { q:"두 눈의 최댓값이 3 이하인 경우는?",
      cond:(a,b)=>Math.max(a,b)<=3, answer:9,
      hint:"두 눈 모두 3 이하 → {1,2,3}×{1,2,3} = 3×3 = 9가지" },
    { q:"두 눈의 최댓값이 5 이상인 경우는?",
      cond:(a,b)=>Math.max(a,b)>=5, answer:20,
      hint:"전체 36 − 최댓값이 4 이하인 경우(4×4=16) = 36−16 = 20가지" },
    { q:"두 눈의 최댓값이 최솟값의 2배 이상인 경우는?",
      cond:(a,b)=>Math.max(a,b)>=2*Math.min(a,b), answer:17,
      hint:"표를 보며 해당 칸을 세어 보세요 → 17가지" },
  ],
};

let mode2='sum', sel2=-1;

function setMode(m) {
  mode2=m; sel2=-1;
  const keys=['sum','prod','min','max'];
  document.querySelectorAll('.mode-btn').forEach((b,i)=>b.classList.toggle('active',keys[i]===m));
  $('result2').classList.remove('show');
  buildQList2(); buildTable2();
}

function buildQList2() {
  const ql=$('qList2'); ql.innerHTML='';
  Q2[mode2].forEach((q,i)=>{
    const b=document.createElement('button');
    b.className='q-btn';
    b.textContent=`Q${i+1}. ${q.q}`;
    b.onclick=()=>selQ2(i);
    ql.appendChild(b);
  });
}

function buildTable2() {
  const tbl=$('tbl2'), fn=MODES[mode2].fn;
  let h='<thead><tr>';
  h+=`<th class="corner" style="font-size:.6rem;color:#556677;line-height:1.4">보라<br>──<br>파랑</th>`;
  for(let c=1;c<=6;c++) h+=`<th class="hc">${c}</th>`;
  h+='</tr></thead><tbody>';
  for(let r=1;r<=6;r++){
    h+=`<tr><th class="hr">${r}</th>`;
    for(let c=1;c<=6;c++) h+=`<td id="t2-${r}-${c}">${fn(r,c)}</td>`;
    h+='</tr>';
  }
  h+='</tbody>';
  tbl.innerHTML=h;
  if(sel2>=0) applyHL2();
}

function selQ2(i) {
  sel2=i;
  document.querySelectorAll('#qList2 .q-btn').forEach((b,j)=>b.classList.toggle('sel',j===i));
  applyHL2();
  const q=Q2[mode2][i];
  $('result2').classList.add('show');
  $('cnt2').textContent=q.answer+' 가지';
  $('hint2').textContent=q.hint;
}

function applyHL2() {
  if(sel2<0) return;
  const q=Q2[mode2][sel2];
  for(let r=1;r<=6;r++) for(let c=1;c<=6;c++)
    $('t2-'+r+'-'+c).classList.toggle('hl',q.cond(r,c));
}

// ═══════════════════════════════════════════════════════════════
// Tab 3: 주사위 3개
// ═══════════════════════════════════════════════════════════════
const Q3 = [
  {
    q:"세 눈이 모두 같은 경우는?",
    cond:(a,b,c)=>a===b&&b===c, answer:6,
    hint:"(1,1,1)(2,2,2)(3,3,3)(4,4,4)(5,5,5)(6,6,6) → 6가지"
  },
  {
    q:"세 눈의 합이 15 이상인 경우는?",
    cond:(a,b,c)=>a+b+c>=15, answer:20,
    hint:"합 15: 10가지, 합 16: 6가지, 합 17: 3가지, 합 18: 1가지 → 20가지"
  },
  {
    q:"세 눈의 최솟값이 4인 경우는?",
    cond:(a,b,c)=>Math.min(a,b,c)===4, answer:19,
    hint:"세 눈 모두 ≥4인 경우(3³=27) − 세 눈 모두 ≥5인 경우(2³=8) = 27−8 = 19가지"
  },
  {
    q:"세 눈의 최댓값이 3인 경우는?",
    cond:(a,b,c)=>Math.max(a,b,c)===3, answer:19,
    hint:"세 눈 모두 ≤3인 경우(3³=27) − 세 눈 모두 ≤2인 경우(2³=8) = 27−8 = 19가지"
  },
  {
    q:"세 눈 중 적어도 하나가 6인 경우는?",
    cond:(a,b,c)=>a===6||b===6||c===6, answer:91,
    hint:"전체 216 − 세 눈 모두 6이 아닌 경우(5³=125) = 216−125 = 91가지"
  },
];

function buildQList3() {
  const ql=$('qList3'); ql.innerHTML='';
  Q3.forEach((q,i)=>{
    const b=document.createElement('button');
    b.className='q-btn';
    b.textContent=`Q${i+1}. ${q.q}`;
    b.onclick=()=>selQ3(i);
    ql.appendChild(b);
  });
}

function buildGrids3() {
  const wrap=$('grids3'); wrap.innerHTML='';
  for(let k=1;k<=6;k++){
    const card=document.createElement('div');
    card.className='mg-card';
    let h=`<div class="mg-label">파랑 = <span>${k}</span></div>`;
    h+='<table class="mt"><thead><tr><th></th>';
    for(let c=1;c<=6;c++) h+=`<th class="ch">${c}</th>`;
    h+='</tr></thead><tbody>';
    for(let r=1;r<=6;r++){
      h+=`<tr><th class="rh">${r}</th>`;
      for(let c=1;c<=6;c++) h+=`<td id="t3-${k}-${r}-${c}"></td>`;
      h+='</tr>';
    }
    h+=`</tbody></table><div class="mg-cnt">해당: <span id="mc${k}">0</span>칸</div>`;
    card.innerHTML=h;
    wrap.appendChild(card);
  }
}

function selQ3(i) {
  document.querySelectorAll('#qList3 .q-btn').forEach((b,j)=>b.classList.toggle('sel',j===i));
  const q=Q3[i];
  let total=0;
  for(let k=1;k<=6;k++){
    let cnt=0;
    for(let r=1;r<=6;r++) for(let c=1;c<=6;c++){
      const m=q.cond(k,r,c);
      $('t3-'+k+'-'+r+'-'+c).classList.toggle('hl',m);
      if(m) cnt++;
    }
    $('mc'+k).textContent=cnt;
    total+=cnt;
  }
  $('result3').classList.add('show');
  $('cnt3').textContent=total+' 가지';
  $('hint3').textContent=q.hint;
}

// ── 초기화 ────────────────────────────────────────────────────
buildTab1();
buildQList2(); buildTable2();
buildQList3(); buildGrids3();
</script>
</body>
</html>"""


def render():
    st.markdown("### 🎲 주사위로 경우의 수 탐구")
    st.markdown(
        "주사위를 던졌을 때 나올 수 있는 결과를 **표**로 정리하고, "
        "조건에 맞는 경우의 수를 직접 헤아려 보세요!"
    )
    components.html(_HTML, height=1100, scrolling=True)
