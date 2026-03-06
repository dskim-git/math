# activities/common/poly_add_sub_game.py
"""
다항식의 덧셈과 뺄셈 – 동류항 연결 게임
두 다항식의 동류항을 클릭하여 계산하는 인터랙티브 활동
"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests

# ── Google Sheets 연동 ─────────────────────────────────────────────────────
_GAS_URL    = "https://script.google.com/macros/s/AKfycbySLDnSYGfQmqrtpuMyIju5hiEf7Lesp6bnWzplm3oZD4WHXESl1XJmsXT_EVcKOJI/exec"   # ← 선생님이 발급한 GAS URL로 교체
_SHEET_NAME = "다항식의덧셈뺄셈"

META = {
    "title":       "다항식의 덧셈과 뺄셈 : 동류항 연결 게임",
    "description": "두 다항식의 동류항을 클릭하여 짝짓고 계산 과정을 직접 확인하는 활동입니다.",
    "order":       11,
}

_GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>동류항 연결 게임</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#fdf4ff 0%,#eff6ff 100%);min-height:100vh;padding:12px}
h2{text-align:center;color:#6d28d9;font-size:1.15rem;margin-bottom:4px}
.subtitle{text-align:center;color:#6b7280;font-size:.8rem;margin-bottom:12px}

/* 진행 */
.progress-wrap{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.progress-bar{flex:1;height:8px;background:#e5e7eb;border-radius:99px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,#a855f7,#3b82f6);transition:width .4s}
.score-badge{background:#a855f7;color:#fff;border-radius:99px;padding:2px 12px;font-size:.8rem;font-weight:700;white-space:nowrap}

/* 문제 박스 */
.problem-box{background:#fff;border:2px solid #e0e7ff;border-radius:14px;padding:12px 16px;margin-bottom:12px}
.problem-label{font-size:.75rem;color:#8b5cf6;font-weight:700;margin-bottom:6px;letter-spacing:.04em}
.poly-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;min-height:52px}
.op-sign{font-size:1.5rem;font-weight:800;color:#374151;padding:0 4px}

/* 항 카드 */
.term-card{display:inline-flex;align-items:center;justify-content:center;
  padding:9px 16px;border-radius:10px;font-size:1rem;font-weight:700;
  cursor:pointer;user-select:none;min-width:64px;text-align:center;
  transition:transform .15s,box-shadow .15s,border-color .15s;
  border:2.5px solid transparent;box-shadow:0 2px 6px rgba(0,0,0,.1)}
.term-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.15)}
.term-card.selected{transform:translateY(-3px) scale(1.06);
  box-shadow:0 6px 18px rgba(0,0,0,.25);border-color:#f59e0b !important}
.term-card.used{opacity:.35;cursor:default;transform:none;box-shadow:none}
.term-card.flash{animation:flashGreen .5s ease}
@keyframes flashGreen{0%,100%{background:inherit}50%{background:#d1fae5}}

/* 차수별 색 */
.tc-5{background:#fdf2f8;border-color:#f0abfc;color:#86198f}
.tc-4{background:#fce7f3;border-color:#f9a8d4;color:#be185d}
.tc-3{background:#ede9fe;border-color:#c4b5fd;color:#5b21b6}
.tc-2{background:#dbeafe;border-color:#93c5fd;color:#1d4ed8}
.tc-1{background:#d1fae5;border-color:#6ee7b7;color:#065f46}
.tc-0{background:#fef3c7;border-color:#fcd34d;color:#92400e}

/* 안내 메시지 */
.hint-box{background:#fffbeb;border:1.5px solid #fcd34d;border-radius:10px;
  padding:8px 14px;font-size:.82rem;color:#92400e;margin-bottom:10px;text-align:center}

/* 계산 단계 */
.steps-wrap{background:#fff;border:1.5px solid #e0e7ff;border-radius:12px;
  padding:12px 14px;margin-bottom:10px}
.steps-title{font-size:.78rem;font-weight:700;color:#4f46e5;margin-bottom:8px}
.step-item{display:flex;align-items:center;gap:8px;padding:5px 0;
  border-bottom:1px dashed #e5e7eb;font-size:.88rem;flex-wrap:wrap}
.step-item:last-child{border-bottom:none}
.step-deg{min-width:70px;font-size:.75rem;color:#6b7280;font-weight:600}
.step-calc{color:#374151}
.step-result{font-weight:700;color:#4f46e5;margin-left:4px}
.step-zero{color:#9ca3af;text-decoration:line-through}

/* 결과 */
.result-box{background:linear-gradient(135deg,#f5f3ff,#eff6ff);border:2px solid #a5b4fc;
  border-radius:12px;padding:12px 16px;margin-bottom:12px;text-align:center;display:none}
.result-label{font-size:.78rem;color:#6366f1;font-weight:700;margin-bottom:4px}
.result-poly{font-size:1.15rem;font-weight:800;color:#312e81}

/* 계수 입력 */
.answer-section{background:#fff;border:1.5px solid #e5e7eb;border-radius:12px;
  padding:12px 14px;margin-bottom:10px;display:none}
.answer-label{font-size:.8rem;color:#4f46e5;font-weight:700;margin-bottom:4px}
.answer-note{font-size:.74rem;color:#6b7280;margin-bottom:8px;line-height:1.5}
.coef-row{display:flex;align-items:center;gap:4px;flex-wrap:wrap;justify-content:center;padding:8px 0}
.coef-box{width:54px;padding:7px 4px;border:2.5px solid #c7d2fe;border-radius:8px;
  font-size:1rem;font-weight:700;text-align:center;font-family:inherit;
  outline:none;transition:.2s;background:#fff;color:#1e1b4b}
.coef-box:focus{border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.15)}
.coef-box.ok{border-color:#34d399!important;background:#d1fae5!important;color:#065f46!important}
.coef-box.ng{border-color:#f87171!important;background:#fee2e2!important;color:#991b1b!important}
.coef-var{font-size:1rem;font-weight:800;color:#312e81;white-space:nowrap}
.coef-sep{font-size:1rem;color:#6b7280;font-weight:700;padding:0 2px}
.coef-zero-hint{font-size:.78rem;color:#6366f1;margin-top:6px;text-align:center}

/* 버튼 */
.btn-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:8px}
.btn{padding:8px 22px;border-radius:99px;border:none;font-size:.87rem;font-weight:700;cursor:pointer;transition:.2s}
.btn-auto{background:#8b5cf6;color:#fff}.btn-auto:hover{background:#7c3aed}
.btn-check{background:#6366f1;color:#fff}.btn-check:hover{background:#4f46e5}
.btn-next{background:#22c55e;color:#fff;display:none}.btn-next:hover{background:#16a34a}
.btn-reset{background:#e5e7eb;color:#374151}.btn-reset:hover{background:#d1d5db}

/* 피드백 */
.feedback{text-align:center;font-size:.93rem;font-weight:700;min-height:24px;margin-bottom:6px}
.feedback.correct{color:#059669}
.feedback.wrong{color:#dc2626}

/* confetti */
#confetti{position:fixed;top:0;left:0;pointer-events:none;width:100%;height:100%;z-index:9999}
</style>
</head>
<body>
<canvas id="confetti"></canvas>

<h2>🔗 다항식의 덧셈과 뺄셈 – 동류항 연결 게임</h2>
<p class="subtitle">두 다항식에서 동류항(같은 차수의 항)끼리 클릭하여 짝지어 계산하세요!</p>

<div class="progress-wrap">
  <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
  <div class="score-badge">점수 <span id="scoreDisp">0</span></div>
</div>

<div class="problem-box">
  <div class="problem-label" id="problemLabel">문제 ①</div>
  <div style="display:flex;align-items:flex-start;gap:4px;flex-wrap:wrap">
    <div>
      <div style="font-size:.72rem;color:#6b7280;margin-bottom:4px">A</div>
      <div class="poly-row" id="polyA"></div>
    </div>
    <div class="op-sign" id="opSign" style="margin-top:24px">+</div>
    <div>
      <div style="font-size:.72rem;color:#6b7280;margin-bottom:4px">B</div>
      <div class="poly-row" id="polyB"></div>
    </div>
  </div>
</div>

<div class="hint-box" id="hintBox">
  🖱️ A와 B 중 <strong>같은 차수의 항</strong>을 하나씩 클릭하여 짝지으세요. 짝이 없는 항은 한 번 클릭하면 바로 결과로 이동합니다.
</div>

<div class="steps-wrap">
  <div class="steps-title">📋 계산 단계 (동류항끼리 계산 중...)</div>
  <div id="stepsList"></div>
</div>

<div class="result-box" id="resultBox">
  <div class="result-label">🏆 완성된 다항식</div>
  <div class="result-poly" id="resultPoly"></div>
</div>

<div class="answer-section" id="answerSection">
  <div class="answer-label">✏️ 각 항의 계수를 입력하세요</div>
  <div class="answer-note">⚠️ 음수이면 - 부호를 포함하여 입력 (예: -3) &nbsp;|&nbsp; '+' 사이 계수에 부호까지 포함</div>
  <div class="coef-row" id="coefRow"></div>
  <div class="coef-zero-hint" id="coefZeroHint" style="display:none"></div>
</div>

<div class="feedback" id="feedback"></div>

<div class="btn-row">
  <button class="btn btn-auto" onclick="autoMatchNext()">⚡ 자동 연결 1개</button>
  <button class="btn btn-check" id="btnCheck" onclick="checkFinalAnswer()" style="display:none">✅ 답 확인</button>
  <button class="btn btn-reset" onclick="resetProblem()">🔄 초기화</button>
  <button class="btn btn-next" id="btnNext" onclick="nextProblem()">➡️ 다음 문제</button>
</div>

<script>
// ── 유틸리티 ─────────────────────────────────────────────────────────────────
const SUP=['\u2070','\u00b9','\u00b2','\u00b3','\u2074','\u2075'];
function superscript(n){ return SUP[n]||String(n); }

function shuffle(arr){
  const a=[...arr];
  for(let i=a.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
  return a;
}

// 항 표시 문자열(isFirst=true이면 양수에 + 안 붙임)
function termText(c,d,isFirst){
  if(c===0) return '0';
  const abs=Math.abs(c);
  const sign=c<0?'-':(isFirst?'':'+');
  const varStr=d===0?'':(d===1?'x':('x'+superscript(d)));
  const numStr=(abs===1&&d>0)?'':String(abs);
  return sign+numStr+varStr;
}
function tcClass(d){ return 'tc-'+Math.min(d,4); }
const DEG_NAMES=['상수항','일차항','이차항','삼차항','사차항'];

// ── 문제 데이터 ──────────────────────────────────────────────────────────────
// 항은 의도적으로 뒤섞어 저장 + render 시 추가 shuffle
// ans: {차수: 계수} — 0인 항 생략
const PROBLEMS = [
  {
    label:"① 덧셈 (3차)",
    op:'+',
    a:[{d:1,c:-2},{d:3,c:1},{d:0,c:1},{d:2,c:3}],
    b:[{d:2,c:-1},{d:3,c:2},{d:1,c:4},{d:0,c:2}],
    ans:{3:3,2:2,1:2,0:3}
  },
  {
    label:"② 뺄셈 (3차)",
    op:'-',
    a:[{d:0,c:-1},{d:2,c:5},{d:3,c:4},{d:1,c:3}],
    b:[{d:1,c:2},{d:3,c:1},{d:2,c:-3},{d:0,c:-4}],
    ans:{3:3,2:8,1:1,0:3}
  },
  {
    label:"③ 덧셈 – 이차·상수 소거 (3차)",
    op:'+',
    a:[{d:3,c:2},{d:0,c:3},{d:2,c:-1}],
    b:[{d:1,c:2},{d:2,c:1},{d:0,c:-3}],
    ans:{3:2,1:2}
  },
  {
    label:"④ 뺄셈 (4차)",
    op:'-',
    a:[{d:2,c:2},{d:4,c:3},{d:1,c:-1},{d:0,c:6}],
    b:[{d:4,c:1},{d:2,c:-3},{d:1,c:2},{d:0,c:-4}],
    ans:{4:2,2:5,1:-3,0:10}
  },
  {
    label:"⑤ 덧셈 – 짝 없는 항 포함 (4차)",
    op:'+',
    a:[{d:4,c:2},{d:0,c:1},{d:2,c:-4}],
    b:[{d:2,c:2},{d:3,c:3},{d:1,c:-3},{d:0,c:5}],
    ans:{4:2,3:3,2:-2,1:-3,0:6}
  },
  {
    label:"⑥ 뺄셈 (4차) – 일부 항 소거",
    op:'-',
    a:[{d:4,c:2},{d:3,c:-1},{d:2,c:3},{d:0,c:4}],
    b:[{d:4,c:2},{d:1,c:2},{d:2,c:1},{d:0,c:-2}],
    ans:{3:-1,2:2,1:-2,0:6}
  },
  {
    label:"⑦ 뺄셈 – 전항 소거",
    op:'-',
    a:[{d:2,c:3},{d:1,c:2},{d:0,c:-5}],
    b:[{d:1,c:2},{d:2,c:3},{d:0,c:-5}],
    ans:{}
  },
];

// ── 상태 ──────────────────────────────────────────────────────────────────────
let cur=0, score=0, selCard=null;
let usedA=new Set(), usedB=new Set();
let steps=[];

// ── 렌더 ──────────────────────────────────────────────────────────────────────
function renderPoly(containerId,terms,poly){
  const shuffled=shuffle([...terms]);
  const wrap=document.getElementById(containerId);
  wrap.innerHTML='';
  shuffled.forEach((t,i)=>{
    const el=document.createElement('div');
    el.className=`term-card ${tcClass(t.d)}`;
    el.id=`card-${poly}-${t.d}`;
    el.textContent=termText(t.c,t.d,i===0);
    el.addEventListener('click',()=>onCardClick(poly,t.d,el,t.c));
    wrap.appendChild(el);
  });
}

function loadProblem(){
  const p=PROBLEMS[cur];
  usedA=new Set(); usedB=new Set();
  steps=[]; selCard=null;
  document.getElementById('problemLabel').textContent=p.label;
  document.getElementById('opSign').textContent=p.op;
  renderPoly('polyA',p.a,'a');
  renderPoly('polyB',p.b,'b');
  document.getElementById('stepsList').innerHTML=
    '<div style="color:#9ca3af;font-size:.8rem">아직 연결된 동류항이 없습니다.</div>';
  document.getElementById('resultBox').style.display='none';
  document.getElementById('answerSection').style.display='none';
  document.getElementById('btnCheck').style.display='none';
  document.getElementById('btnNext').style.display='none';
  document.getElementById('feedback').textContent='';
  document.getElementById('feedback').className='feedback';
  document.getElementById('coefRow').innerHTML='';
  document.getElementById('coefZeroHint').style.display='none';
  document.getElementById('progressFill').style.width=
    ((cur/PROBLEMS.length)*100)+'%';
  setHint('A와 B 중 <strong>같은 차수의 항</strong>을 하나씩 클릭하여 짝지으세요.<br>짝이 없는 항은 해당 카드를 <strong>두 번 클릭</strong>하면 바로 결과로 이동합니다.');
}

// ── 카드 클릭 ─────────────────────────────────────────────────────────────────
function onCardClick(poly,deg,el,coef){
  if((poly==='a'?usedA:usedB).has(deg)) return;
  const p=PROBLEMS[cur];
  const effectiveCoef=(poly==='b'&&p.op==='-')?-coef:coef;
  if(!selCard){
    selCard={poly,deg,ecoef:effectiveCoef,el};
    el.classList.add('selected');
    setHint(`<strong>${termText(coef,deg,true)}</strong> 선택됨 (${DEG_NAMES[Math.min(deg,4)]}). 같은 차수의 다른 항을 클릭하세요.<br>짝이 없으면 이 카드를 <strong>한 번 더 클릭</strong>!`);
  } else if(selCard.poly===poly && selCard.deg===deg){
    commitSingle(poly,deg,selCard.ecoef,el);
    selCard=null;
  } else if(selCard.deg===deg && selCard.poly!==poly){
    commitPair(selCard,poly,deg,effectiveCoef,el);
    selCard=null;
  } else {
    selCard.el.classList.remove('selected');
    selCard={poly,deg,ecoef:effectiveCoef,el};
    el.classList.add('selected');
    setHint(`⚠️ 차수가 다릅니다. <strong>${termText(coef,deg,true)}</strong>(${DEG_NAMES[Math.min(deg,4)]})을 선택했습니다. 동일 차수끼리 짝지어야 합니다.`);
  }
}

// ── commit ────────────────────────────────────────────────────────────────────
function commitSingle(poly,deg,ecoef,el){
  (poly==='a'?usedA:usedB).add(deg);
  el.classList.remove('selected'); el.classList.add('used');
  const p=PROBLEMS[cur];
  const term=(poly==='a'?p.a:p.b).find(t=>t.d===deg);
  const raw=termText(term.c,deg,true);
  const opStr=(poly==='b'&&p.op==='-')?`-(${raw})`:raw;
  steps.push({deg,expr:opStr,coef:ecoef});
  updateSteps(); checkAllUsed();
}

function commitPair(sel,poly2,deg2,ecoef2,el2){
  (sel.poly==='a'?usedA:usedB).add(sel.deg);
  (poly2==='a'?usedA:usedB).add(deg2);
  sel.el.classList.remove('selected'); sel.el.classList.add('used');
  el2.classList.add('used');
  const p=PROBLEMS[cur];
  const t1=(sel.poly==='a'?p.a:p.b).find(t=>t.d===sel.deg);
  const t2=(poly2==='a'?p.a:p.b).find(t=>t.d===deg2);
  const raw1=termText(t1.c,t1.d,true);
  const raw2=termText(t2.c,t2.d,true);
  const op1str=(sel.poly==='b'&&p.op==='-')?`-(${raw1})`:raw1;
  const op2str=(poly2==='b'&&p.op==='-')?`-(${raw2})`:raw2;
  const sumCoef=sel.ecoef+ecoef2;
  steps.push({deg:sel.deg,expr:`${op1str}  ${ecoef2>=0?'+ ':''}${op2str}`,coef:sumCoef});
  updateSteps();
  flashEl(sel.el); flashEl(el2);
  checkAllUsed();
}

function flashEl(el){
  el.classList.add('flash');
  setTimeout(()=>el.classList.remove('flash'),450);
}

// ── 계산 단계 표시 ────────────────────────────────────────────────────────────
function updateSteps(){
  const wrap=document.getElementById('stepsList');
  if(!steps.length){
    wrap.innerHTML='<div style="color:#9ca3af;font-size:.8rem">아직 연결된 동류항이 없습니다.</div>';
    return;
  }
  const sorted=[...steps].sort((a,b)=>b.deg-a.deg);
  wrap.innerHTML='';
  sorted.forEach(s=>{
    const di=document.createElement('div');
    di.className='step-item';
    const resStr=termText(s.coef,s.deg,true)||'0';
    di.innerHTML=`
      <span class="step-deg">${DEG_NAMES[Math.min(s.deg,4)]}</span>
      <span class="step-calc">${s.expr}</span>
      <span class="step-eq">=</span>
      <span class="${s.coef===0?'step-zero':'step-result'}">${s.coef===0?'0 (소거)':resStr}</span>`;
    wrap.appendChild(di);
  });
}

function checkAllUsed(){
  const p=PROBLEMS[cur];
  if(usedA.size===p.a.length && usedB.size===p.b.length) buildResult();
}

// ── 결과 & 계수 입력 박스 ─────────────────────────────────────────────────────
function buildResult(){
  const sorted=[...steps].sort((a,b)=>b.deg-a.deg);
  const nonZero=sorted.filter(s=>s.coef!==0);
  const polyStr=nonZero.length
    ? nonZero.map((s,i)=>termText(s.coef,s.deg,i===0)).join(' ')
    : '0';
  document.getElementById('resultPoly').textContent=polyStr;
  document.getElementById('resultBox').style.display='block';

  const row=document.getElementById('coefRow');
  row.innerHTML='';
  if(!nonZero.length){
    const inp=document.createElement('input');
    inp.className='coef-box'; inp.type='text'; inp.placeholder='?';
    inp.dataset.expected='0'; inp.dataset.deg='_zero';
    row.appendChild(inp);
    const lbl=document.createElement('span');
    lbl.className='coef-var';
    lbl.innerHTML='&nbsp;(모든 항 소거 → ?)';
    row.appendChild(lbl);
    const h=document.getElementById('coefZeroHint');
    h.textContent='힌트: 모든 동류항이 소거되면 결과는 0입니다.';
    h.style.display='block';
  } else {
    nonZero.forEach((s,i)=>{
      if(i>0){
        const sep=document.createElement('span');
        sep.className='coef-sep'; sep.textContent='+';
        row.appendChild(sep);
      }
      const inp=document.createElement('input');
      inp.className='coef-box'; inp.type='text'; inp.placeholder='?';
      inp.dataset.expected=String(s.coef);
      inp.dataset.deg=String(s.deg);
      row.appendChild(inp);
      const lbl=document.createElement('span');
      lbl.className='coef-var';
      lbl.textContent=s.deg===0?'':(s.deg===1?'x':('x'+superscript(s.deg)));
      row.appendChild(lbl);
    });
  }
  document.getElementById('answerSection').style.display='block';
  document.getElementById('btnCheck').style.display='inline-block';
  document.getElementById('resultBox').scrollIntoView({behavior:'smooth',block:'nearest'});
  setHint('🎯 계산 단계를 참고하여 각 항의 <strong>계수</strong>를 입력하세요.<br>음수이면 - 포함 (예: -3), 계수 1·-1도 정확히 입력');
}

// ── 정답 확인 ─────────────────────────────────────────────────────────────────
function checkFinalAnswer(){
  const boxes=document.querySelectorAll('.coef-box');
  let allOk=true;
  boxes.forEach(box=>{
    const exp=parseInt(box.dataset.expected);
    const val=parseInt(box.value.trim());
    const ok=(!isNaN(val)&&val===exp&&box.value.trim()!=='');
    box.classList.toggle('ok',ok);
    box.classList.toggle('ng',!ok);
    if(!ok) allOk=false;
  });
  if(allOk){
    score+=15;
    document.getElementById('scoreDisp').textContent=score;
    setFeedback('🎉 정답! 완벽한 계산입니다! +15점','correct');
    document.getElementById('btnNext').style.display='inline-block';
    launchConfetti();
  } else {
    setFeedback('❌ 빨간 칸을 다시 확인하세요. 음수(-) 부호도 확인!','wrong');
  }
}

// ── 자동 연결 ─────────────────────────────────────────────────────────────────
function autoMatchNext(){
  const p=PROBLEMS[cur];
  for(const tA of p.a){
    if(usedA.has(tA.d)) continue;
    for(const tB of p.b){
      if(usedB.has(tB.d)||tA.d!==tB.d) continue;
      const e1=document.getElementById(`card-a-${tA.d}`);
      const e2=document.getElementById(`card-b-${tB.d}`);
      commitPair({poly:'a',deg:tA.d,ecoef:tA.c,el:e1},'b',tB.d,
        p.op==='-'?-tB.c:tB.c,e2);
      return;
    }
  }
  for(const tA of p.a){
    if(!usedA.has(tA.d)){
      commitSingle('a',tA.d,tA.c,document.getElementById(`card-a-${tA.d}`));
      return;
    }
  }
  for(const tB of p.b){
    if(!usedB.has(tB.d)){
      commitSingle('b',tB.d,p.op==='-'?-tB.c:tB.c,
        document.getElementById(`card-b-${tB.d}`));
      return;
    }
  }
  setHint('✅ 모든 항이 이미 처리되었습니다!');
}

function resetProblem(){ loadProblem(); }
function nextProblem(){
  cur=(cur+1)%PROBLEMS.length;
  if(cur===0) setFeedback('🏆 모든 문제 완료! 처음부터 다시 시작합니다.','correct');
  loadProblem();
}
function setFeedback(msg,cls){
  const el=document.getElementById('feedback');
  el.innerHTML=msg; el.className='feedback'+(cls?' '+cls:'');
}
function setHint(html){
  document.getElementById('hintBox').innerHTML=html;
}

// ── confetti ──────────────────────────────────────────────────────────────────
function launchConfetti(){
  const canvas=document.getElementById('confetti');
  canvas.width=window.innerWidth; canvas.height=window.innerHeight;
  const ctx=canvas.getContext('2d');
  const pieces=Array.from({length:110},()=>({
    x:Math.random()*canvas.width,y:Math.random()*canvas.height-canvas.height,
    r:Math.random()*5+2,dx:(Math.random()-.5)*3,dy:Math.random()*3+2,
    color:`hsl(${Math.random()*360},80%,60%)`,
    rot:Math.random()*360,drot:(Math.random()-.5)*6
  }));
  let frame=0;
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    pieces.forEach(p=>{
      ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot*Math.PI/180);
      ctx.fillStyle=p.color;ctx.fillRect(-p.r,-p.r,p.r*2,p.r*2);ctx.restore();
      p.x+=p.dx;p.y+=p.dy;p.rot+=p.drot;
    });
    frame++;
    if(frame<100) requestAnimationFrame(draw);
    else ctx.clearRect(0,0,canvas.width,canvas.height);
  }
  draw();
}

loadProblem();

</script>
</body>
</html>
"""

def render():
    st.header("🔗 다항식의 덧셈과 뺄셈 – 동류항 연결 게임")
    st.caption(
        "두 다항식에서 **동류항**(같은 문자, 같은 차수의 항)끼리 클릭하여 짝짓고 계산 과정을 확인하세요.  \n"
        "⚡ 자동 연결 버튼으로 힌트를 하나씩 확인할 수도 있습니다."
    )

    components.html(_GAME_HTML, height=720, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_reflection_form(sheet_name: str, gas_url: str):
    st.divider()
    st.subheader("✍️ 활동 후 성찰 기록")
    st.caption("아래 질문에 답하고 **제출하기** 버튼을 눌러주세요.")

    with st.form(f"reflection_{sheet_name}", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            student_id = st.text_input("학번")
        with c2:
            name = st.text_input("이름")

        st.markdown("**📝 이 활동과 관련된 문제 2개를 스스로 만들고, 풀어보세요**")
        q1 = st.text_area("문제 1 (두 다항식의 덧셈 또는 뺄셈 문제)", height=70)
        a1 = st.text_input("문제 1의 정답")
        q2 = st.text_area("문제 2 (두 다항식의 덧셈 또는 뺄셈 문제)", height=70)
        a2 = st.text_input("문제 2의 정답")

        new_learning = st.text_area("💡 이 활동을 통해 새롭게 알게 된 점", height=90)
        feeling      = st.text_area("💬 이 활동을 하면서 느낀 점", height=90)

        submitted = st.form_submit_button("📤 제출하기", use_container_width=True, type="primary")

    if submitted:
        if not student_id or not name:
            st.warning("학번과 이름을 입력해주세요.")
        elif gas_url == "YOUR_COMMON1_GAS_WEB_APP_URL":
            st.error(
                "⚠️ Google Sheets 연동 URL이 아직 설정되지 않았습니다.  \n"
                "선생님이 Google Apps Script를 배포하고 `_GAS_URL`을 교체해야 합니다."
            )
        else:
            payload = {
                "sheet":     sheet_name,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "학번":      student_id,
                "이름":      name,
                "문제1":     q1, "답1": a1,
                "문제2":     q2, "답2": a2,
                "새롭게알게된점": new_learning,
                "느낀점":    feeling,
            }
            try:
                resp = requests.post(gas_url, json=payload, timeout=10)
                if resp.status_code == 200:
                    st.success(f"✅ {name}님의 기록이 제출되었습니다!")
                    st.balloons()
                else:
                    st.error(f"제출 중 오류 (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"네트워크 오류: {e}")
