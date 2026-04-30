# activities/common/mini/matrix_equality_game.py
"""
행렬 상등 탐정 게임
행렬 읽기 퀴즈와 상등 방정식 풀기를 통해 행렬의 뜻과 상등 개념을 재미있게 익히는 인터랙티브 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 ───────────────────────────────────────────────────────
_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "행렬상등탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이 활동을 통해 알게 된 내용을 정리해보세요**"},
    {"key": "상등조건",
     "label": "1️⃣ 두 행렬이 서로 같다(상등)고 하기 위한 조건 2가지를 자신의 말로 설명해보세요.",
     "type": "text_area", "height": 90},
    {"key": "성분방정식",
     "label": "2️⃣ 행렬의 상등을 이용해 미지수 값을 구하는 방법을, 예시를 들어 설명해보세요.",
     "type": "text_area", "height": 90},
    {"key": "어려운문제",
     "label": "3️⃣ 활동에서 가장 어려웠던 문제와, 어떻게 해결했는지 서술해보세요.",
     "type": "text_area", "height": 90},
    {"key": "새롭게알게된점",
     "label": "💡 이 활동을 통해 새롭게 알게 된 점",
     "type": "text_area", "height": 90},
    {"key": "느낀점",
     "label": "💬 이 활동을 하면서 느낀 점",
     "type": "text_area", "height": 90},
]

META = {
    "title":       "🕵️ 행렬 상등 탐정 게임",
    "description": "행렬 읽기 퀴즈와 상등 방정식 풀기로 행렬의 뜻과 상등 개념을 재미있게 익히는 활동",
    "order":       1,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>행렬 상등 탐정 게임</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}
.tabs{display:flex;gap:6px;margin-bottom:16px}
.tb{
  flex:1;padding:10px 8px;border-radius:11px;
  border:2px solid #1e293b;background:#1e293b;
  color:#64748b;font-weight:700;cursor:pointer;
  font-size:.88rem;transition:all .2s;
}
.tb.on{
  background:linear-gradient(135deg,#4f46e5,#7c3aed);
  color:#fff;border-color:transparent;
}
.tb:hover:not(.on){background:#273549;color:#e2e8f0}
.panel{display:none}.panel.on{display:block}
.stitle{font-size:1.05rem;font-weight:800;color:#c7d2fe;margin-bottom:2px}
.ssub{font-size:.78rem;color:#475569;margin-bottom:12px}
.stats{display:flex;gap:8px;margin-bottom:12px}
.stat{
  flex:1;background:#1e293b;border:1px solid #2d3748;
  border-radius:10px;padding:8px 6px;text-align:center;
}
.sv{font-size:1.45rem;font-weight:800;color:#a5b4fc}
.sl{font-size:.68rem;color:#475569;margin-top:1px}
.mat-outer{display:inline-flex;align-items:center}
.mat-inner{
  display:grid;gap:5px 8px;
  padding:8px 6px;position:relative;margin:0 11px;
}
.mat-inner::before,.mat-inner::after{
  content:'';position:absolute;top:0;bottom:0;width:9px;
  border:2.5px solid #818cf8;
}
.mat-inner::before{left:-9px;border-right:none;border-radius:3px 0 0 3px}
.mat-inner::after{right:-9px;border-left:none;border-radius:0 3px 3px 0}
.cell{
  min-width:46px;height:35px;
  display:flex;align-items:center;justify-content:center;
  background:#1e293b;border:1px solid #334155;
  border-radius:7px;font-size:.92rem;font-weight:600;
  padding:0 7px;white-space:nowrap;
}
.cell.unk{color:#fbbf24;background:#1c1408;border-color:#92400e}
.cell.grn{color:#86efac;background:#0a2e1c;border-color:#15803d}
.cell.hl{box-shadow:0 0 0 2px #fbbf24;background:#292217}
.qbox{
  font-size:.93rem;font-weight:600;
  background:#1e293b;border-left:4px solid #4f46e5;
  border-radius:0 10px 10px 0;padding:9px 13px;margin:8px 0 7px;
}
.choices{display:flex;gap:6px;flex-wrap:wrap;margin:5px 0 7px}
.ch{
  flex:1;min-width:72px;padding:9px 6px;
  border-radius:9px;border:2px solid #334155;
  background:#1e293b;color:#cbd5e1;
  font-size:.9rem;font-weight:700;cursor:pointer;
  text-align:center;transition:all .15s;
}
.ch:hover{border-color:#4f46e5;background:#273549;color:#fff}
.ch.ok{background:#064e3b;border-color:#10b981;color:#6ee7b7;pointer-events:none}
.ch.ng{background:#450a0a;border-color:#ef4444;color:#fca5a5;pointer-events:none}
.ch.dim{opacity:.45;pointer-events:none}
.trow{display:flex;gap:8px;margin:5px 0 7px}
.trow input{
  flex:1;padding:9px;background:#1e293b;border:2px solid #334155;
  border-radius:9px;color:#e2e8f0;font-size:.95rem;font-weight:700;
  text-align:center;outline:none;
}
.trow input:focus{border-color:#4f46e5}
.fb{font-size:.87rem;font-weight:600;padding:7px 12px;border-radius:8px;margin:4px 0;display:none;}
.fb.ok{display:block;background:#064e3b;color:#6ee7b7}
.fb.ng{display:block;background:#450a0a;color:#fca5a5}
.done-box{
  text-align:center;padding:22px 16px;
  background:linear-gradient(135deg,#312e81,#1e1b4b);
  border:2px solid #4f46e5;border-radius:14px;
  margin-top:10px;display:none;
}
.done-box.show{display:block}
.detnav{display:flex;align-items:center;justify-content:space-between;margin-bottom:11px}
.stars-lbl{color:#fbbf24;font-size:1rem;letter-spacing:2px}
.lv-txt{font-size:.73rem;color:#475569;margin-top:2px}
.dots{display:flex;gap:5px}
.dot{width:9px;height:9px;border-radius:50%;background:#334155;transition:all .3s}
.dot.done{background:#22c55e}
.dot.active{background:#6366f1;box-shadow:0 0 0 2.5px rgba(99,102,241,.4)}
.pcnt{background:#1e293b;border:1px solid #334155;border-radius:99px;padding:3px 11px;font-size:.77rem;color:#64748b;}
.eq-row{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:4px 0 6px}
.mlbl{font-size:1.25rem;font-weight:800;color:#a5b4fc}
.eqsign{font-size:1.7rem;font-weight:800;color:#e2e8f0}
.var-bar{
  display:flex;gap:10px;flex-wrap:wrap;
  background:#1e293b;border:1px solid #334155;
  border-radius:10px;padding:10px 13px;margin:8px 0;
}
.vg{display:flex;flex-direction:column;align-items:center;gap:3px}
.vl{font-size:.71rem;color:#64748b;font-weight:700}
.vi{
  width:60px;padding:7px 4px;background:#0f172a;
  border:2px solid #334155;border-radius:8px;
  color:#e2e8f0;font-size:.95rem;font-weight:700;
  text-align:center;outline:none;transition:border-color .2s;
}
.vi:focus{border-color:#4f46e5}
.vi.ok{border-color:#22c55e;background:#0a2e1c;color:#86efac}
.vi.ng{border-color:#ef4444;background:#1f0505;color:#fca5a5}
.btn-row{display:flex;gap:7px;flex-wrap:wrap;margin:7px 0}
.btn{padding:8px 16px;border-radius:9px;border:none;font-size:.84rem;font-weight:700;cursor:pointer;transition:all .15s;}
.btn:hover{opacity:.88;transform:translateY(-1px)}
.b-pri{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff}
.b-sec{background:#1e293b;color:#94a3b8;border:2px solid #334155}
.b-sec:hover{background:#273549;color:#e2e8f0}
.b-warn{background:linear-gradient(135deg,#d97706,#f59e0b);color:#1f2937}
.res{padding:10px 14px;border-radius:9px;font-size:.87rem;font-weight:600;margin:5px 0;display:none;}
.res.show{display:block}
.res.ok{background:#064e3b;border:1px solid #10b981;color:#6ee7b7}
.res.ng{background:#450a0a;border:1px solid #ef4444;color:#fca5a5}
.res.hint{background:#292217;border:1px solid #f59e0b;color:#fcd34d}
.nav2{display:flex;gap:8px;justify-content:space-between;margin-top:11px}
.page-head{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.concept-card{
  background:#1e293b;border:1px solid #334155;border-radius:11px;
  padding:10px 14px;margin-bottom:12px;
  font-size:.82rem;line-height:1.6;color:#94a3b8;
}
.concept-card strong{color:#c7d2fe}
.concept-card .tag{
  display:inline-block;background:#312e81;color:#a5b4fc;
  border-radius:5px;padding:1px 8px;font-size:.75rem;
  font-weight:700;margin-right:4px;
}
</style>
</head>
<body>

<div class="page-head">
  <div style="font-size:1.8rem">🕵️</div>
  <div>
    <div style="font-size:1.1rem;font-weight:800;color:#c7d2fe">행렬 상등 탐정 게임</div>
    <div style="font-size:.77rem;color:#475569">행렬의 뜻과 상등 개념을 게임으로 완벽하게 익혀보자!</div>
  </div>
</div>

<div class="tabs">
  <button class="tb on" onclick="showTab(0)">🔍 행렬 읽기 퀴즈</button>
  <button class="tb" onclick="showTab(1)">🕵️ 상등 탐정</button>
</div>

<!-- ══════════ TAB 1: 행렬 읽기 퀴즈 ══════════ -->
<div class="panel on" id="p0">

  <div class="concept-card">
    <span class="tag">핵심 개념</span>
    <strong>m×n 행렬</strong>: 행이 m개, 열이 n개인 행렬 &nbsp;|&nbsp;
    <strong>(i,j)성분</strong>: 제i행과 제j열이 만나는 성분 &nbsp;|&nbsp;
    <strong>정사각행렬</strong>: 행의 수 = 열의 수
  </div>

  <div class="stitle">🔍 행렬 읽기 퀴즈</div>
  <div class="ssub">랜덤 행렬을 보고 질문에 답하세요! <span style="color:#fbbf24">8문제 연속 정답</span>이 목표!</div>

  <div class="stats">
    <div class="stat"><div class="sv" id="q-sc">0</div><div class="sl">점수</div></div>
    <div class="stat"><div class="sv" id="q-str">0</div><div class="sl">연속 정답</div></div>
    <div class="stat"><div class="sv" id="q-tot">0</div><div class="sl">총 문제 수</div></div>
  </div>

  <div id="q-mat" style="text-align:center;margin:4px 0 8px;min-height:60px"></div>
  <div class="qbox" id="q-q">잠시 후 문제가 표시됩니다...</div>
  <div id="q-ans"></div>
  <div class="fb" id="q-fb"></div>

  <div class="done-box" id="q-done">
    <div style="font-size:2.2rem">🎉</div>
    <div style="font-size:1.2rem;font-weight:800;color:#a5b4fc;margin:6px 0">퀴즈 완료!</div>
    <div id="q-done-msg" style="color:#64748b;font-size:.87rem;margin-bottom:14px"></div>
    <button class="btn b-pri" onclick="initQuiz()">다시 도전!</button>
  </div>
</div>

<!-- ══════════ TAB 2: 상등 탐정 ══════════ -->
<div class="panel" id="p1">

  <div class="concept-card">
    <span class="tag">핵심 개념</span>
    두 행렬 A, B가 <strong>같은 꼴</strong>이고 <strong>대응하는 모든 성분이 같으면</strong> A = B라고 한다.
    미지수가 있는 성분 방정식을 세워 풀면 된다.
  </div>

  <div class="stitle">🕵️ 상등 탐정</div>
  <div class="ssub">A = B를 만족하는 미지수를 찾아라! <span style="color:#fbbf24">노란 칸</span>이 미지수가 포함된 식이에요.</div>

  <div class="detnav">
    <div>
      <div class="stars-lbl" id="d-stars">⭐</div>
      <div class="lv-txt" id="d-lv">난이도 1</div>
    </div>
    <div class="dots" id="d-dots"></div>
    <div class="pcnt"><span id="d-cur">1</span> / <span id="d-tot">5</span></div>
  </div>

  <div id="d-prob"></div>
  <div id="d-vars"></div>

  <div class="btn-row">
    <button class="btn b-pri" onclick="checkDet()">✅ 정답 확인</button>
    <button class="btn b-sec" onclick="resetDet()">🔄 초기화</button>
    <button class="btn b-warn" onclick="hintDet()">💡 힌트</button>
  </div>

  <div class="res" id="d-res"></div>

  <div class="nav2">
    <button class="btn b-sec" id="d-prev" onclick="moveDet(-1)">◀ 이전</button>
    <button class="btn b-pri" id="d-next" onclick="moveDet(1)">다음 ▶</button>
  </div>
</div>

<script>
function showTab(i){
  document.querySelectorAll('.tb').forEach((b,j)=>b.classList.toggle('on',i===j));
  document.querySelectorAll('.panel').forEach((p,j)=>p.classList.toggle('on',i===j));
}

// ── QUIZ ────────────────────────────────────────────────────────────────────
let qSc=0,qStr=0,qTot=0,cMat=null,cQ=null,qRot=0;
const TARGET=8;

function ri(a,b){return Math.floor(Math.random()*(b-a+1))+a}

function genMat(){
  const r=ri(2,3),c=ri(2,3),d=[];
  for(let i=0;i<r*c;i++) d.push(ri(-9,9));
  return {r,c,d};
}

function initQuiz(){
  qSc=0;qStr=0;qTot=0;
  document.getElementById('q-done').classList.remove('show');
  document.getElementById('q-q').style.display='';
  document.getElementById('q-fb').className='fb';
  upStats();
  nextQ();
}

function upStats(){
  document.getElementById('q-sc').textContent=qSc;
  document.getElementById('q-str').textContent=qStr;
  document.getElementById('q-tot').textContent=qTot;
}

function matHtml(r,c,d,hlIdx){
  let h=`<div class="mat-outer"><div class="mat-inner" style="grid-template-columns:repeat(${c},1fr)">`;
  for(let i=0;i<r*c;i++) h+=`<div class="cell${i===hlIdx?' hl':''}">${d[i]}</div>`;
  h+='</div></div>';
  return h;
}

function nextQ(){
  if(qStr>=TARGET){showDone();return;}
  document.getElementById('q-fb').className='fb';
  cMat=genMat();
  const {r,c,d}=cMat;
  const type=['size','entry','square'][qRot%3];
  qRot++;

  if(type==='size'){
    document.getElementById('q-mat').innerHTML=matHtml(r,c,d,-1);
    cQ={type:'size',ans:`${r}×${c}`};
    document.getElementById('q-q').textContent='이 행렬의 꼴(m×n)은?';
    const all=['1×2','1×3','2×1','2×2','2×3','3×1','3×2','3×3'];
    const correct=`${r}×${c}`;
    const wrongs=all.filter(x=>x!==correct).sort(()=>Math.random()-.5).slice(0,3);
    renderChoices([correct,...wrongs].sort(()=>Math.random()-.5),correct);

  } else if(type==='entry'){
    const idx=ri(0,r*c-1);
    document.getElementById('q-mat').innerHTML=matHtml(r,c,d,idx);
    const row=Math.floor(idx/c)+1,col=(idx%c)+1;
    cQ={type:'entry',ans:d[idx]};
    document.getElementById('q-q').innerHTML=
      `<span style="color:#fbbf24">강조된 칸</span>의 값은? <span style="color:#64748b;font-size:.83rem">((${row},${col})성분)</span>`;
    document.getElementById('q-ans').innerHTML=
      `<div class="trow">
        <input type="number" id="q-inp" placeholder="숫자 입력" onkeydown="if(event.key==='Enter')subQ()">
        <button class="btn b-pri" onclick="subQ()">확인</button>
      </div>`;
    setTimeout(()=>{const e=document.getElementById('q-inp');if(e)e.focus();},30);

  } else {
    document.getElementById('q-mat').innerHTML=matHtml(r,c,d,-1);
    const sq=(r===c);
    cQ={type:'square',ans:sq?'예':'아니오'};
    document.getElementById('q-q').innerHTML=
      `이 행렬은 <span style="color:#fbbf24">정사각행렬</span>인가요?`;
    renderChoices(['예','아니오'],sq?'예':'아니오');
  }
}

function renderChoices(chs,correct){
  let h='<div class="choices">';
  for(const ch of chs)
    h+=`<button class="ch" onclick="ansQ(this,'${ch}','${correct}')">${ch}</button>`;
  h+='</div>';
  document.getElementById('q-ans').innerHTML=h;
}

function ansQ(btn,chosen,correct){
  const ok=(chosen===correct);
  procAns(ok,correct);
  document.querySelectorAll('.ch').forEach(b=>{
    const v=b.textContent.trim();
    if(v===correct) b.classList.add('ok');
    else if(b===btn&&!ok) b.classList.add('ng');
    else b.classList.add('dim');
  });
  setTimeout(nextQ,1050);
}

function subQ(){
  const e=document.getElementById('q-inp');
  if(!e||e.value==='')return;
  const ok=parseInt(e.value)===cQ.ans;
  procAns(ok,String(cQ.ans));
  e.disabled=true;
  const b=document.querySelector('.trow .btn');if(b)b.disabled=true;
  setTimeout(nextQ,1050);
}

function procAns(ok,correct){
  qTot++;
  const fb=document.getElementById('q-fb');
  if(ok){
    qSc+=10;qStr++;
    fb.textContent=`✅ 정답! +10점 (연속: ${qStr}/${TARGET})`;
    fb.className='fb ok';
  } else {
    qStr=0;
    fb.textContent=`❌ 오답. 정답: ${correct}`;
    fb.className='fb ng';
  }
  upStats();
}

function showDone(){
  document.getElementById('q-mat').innerHTML='';
  document.getElementById('q-q').style.display='none';
  document.getElementById('q-ans').innerHTML='';
  document.getElementById('q-fb').className='fb';
  const box=document.getElementById('q-done');
  box.classList.add('show');
  document.getElementById('q-done-msg').textContent=
    `총 ${qTot}문제 풀이 · 최종 점수: ${qSc}점 🏆`;
}

// ── DETECTIVE ───────────────────────────────────────────────────────────────
const PROBS=[
  {
    lv:1, stars:'⭐', name:'난이도 1 · 2×2',
    size:[2,2],
    A:[{d:'x',u:1},{d:'3',u:0},{d:'2',u:0},{d:'y',u:1}],
    B:[5,3,2,-4],
    vars:[{n:'x',v:5},{n:'y',v:-4}],
    hint:'A=B이면 같은 위치의 성분이 같아요. (1,1)성분: x=5, (2,2)성분: y=−4'
  },
  {
    lv:2, stars:'⭐⭐', name:'난이도 2 · 2×2',
    size:[2,2],
    A:[{d:'2a',u:1},{d:'b+1',u:1},{d:'-3',u:0},{d:'c',u:1}],
    B:[6,4,-3,7],
    vars:[{n:'a',v:3},{n:'b',v:3},{n:'c',v:7}],
    hint:'2a=6 → a=3 / b+1=4 → b=3 / c=7'
  },
  {
    lv:3, stars:'⭐⭐⭐', name:'난이도 3 · 2×3',
    size:[2,3],
    A:[{d:'x+y',u:1},{d:'2',u:0},{d:'z-1',u:1},
       {d:'4',u:0},{d:'x-y',u:1},{d:'8',u:0}],
    B:[5,2,3,4,1,8],
    vars:[{n:'x',v:3},{n:'y',v:2},{n:'z',v:4}],
    hint:'x+y=5, x-y=1 → 더하면 2x=6 → x=3, y=2. z-1=3 → z=4'
  },
  {
    lv:4, stars:'⭐⭐⭐⭐', name:'난이도 4 · 2×3',
    size:[2,3],
    A:[{d:'2p-q',u:1},{d:'p+q',u:1},{d:'5',u:0},
       {d:'3r',u:1},{d:'r+2s',u:1},{d:'8',u:0}],
    B:[3,6,5,9,5,8],
    vars:[{n:'p',v:3},{n:'q',v:3},{n:'r',v:3},{n:'s',v:1}],
    hint:'2p-q=3, p+q=6 → 더하면 3p=9 → p=3, q=3. 3r=9 → r=3, r+2s=5 → s=1'
  },
  {
    lv:5, stars:'⭐⭐⭐⭐⭐', name:'난이도 5 · 3×2',
    size:[3,2],
    A:[{d:'a+b',u:1},{d:'a-b',u:1},
       {d:'c',u:1},{d:'2c+1',u:1},
       {d:'a-c',u:1},{d:'4',u:0}],
    B:[8,2,3,7,2,4],
    vars:[{n:'a',v:5},{n:'b',v:3},{n:'c',v:3}],
    hint:'a+b=8, a-b=2 → 더하면 2a=10 → a=5, b=3. c=3, a-c=5-3=2(✓)'
  },
];

let dIdx=0, solvedSet=new Set();

function initDet(){
  dIdx=0;
  solvedSet=new Set();
  buildDots();
  loadProb();
}

function buildDots(){
  let h='';
  PROBS.forEach((_,i)=>h+=`<div class="dot" id="dd${i}"></div>`);
  document.getElementById('d-dots').innerHTML=h;
}

function syncDots(){
  PROBS.forEach((_,i)=>{
    const d=document.getElementById('dd'+i);
    if(!d)return;
    d.className='dot'+(solvedSet.has(i)?' done':(i===dIdx?' active':''));
  });
}

function loadProb(){
  const p=PROBS[dIdx];
  const [rows,cols]=p.size;
  document.getElementById('d-cur').textContent=dIdx+1;
  document.getElementById('d-tot').textContent=PROBS.length;
  document.getElementById('d-stars').textContent=p.stars;
  document.getElementById('d-lv').textContent=p.name;
  syncDots();

  let aH=`<div class="mat-inner" style="grid-template-columns:repeat(${cols},1fr)">`;
  p.A.forEach(c=>aH+=`<div class="cell${c.u?' unk':''}">${c.d}</div>`);
  aH+='</div>';

  let bH=`<div class="mat-inner" style="grid-template-columns:repeat(${cols},1fr)">`;
  p.B.forEach(v=>bH+=`<div class="cell grn">${v}</div>`);
  bH+='</div>';

  document.getElementById('d-prob').innerHTML=
    `<div class="eq-row">
      <span class="mlbl">A</span>
      <div class="mat-outer">${aH}</div>
      <span class="eqsign">=</span>
      <span class="mlbl" style="color:#86efac">B</span>
      <div class="mat-outer">${bH}</div>
    </div>
    <div style="font-size:.76rem;color:#475569;margin:3px 0">
      📌 꼴: ${rows}×${cols} 행렬 &nbsp;|&nbsp; 미지수: ${p.vars.map(v=>v.n).join(', ')}
    </div>`;

  let vh='<div class="var-bar">';
  p.vars.forEach(v=>
    vh+=`<div class="vg">
      <div class="vl">${v.n} =</div>
      <input class="vi" id="vi-${v.n}" type="number" step="any" placeholder="?">
    </div>`
  );
  vh+='</div>';
  document.getElementById('d-vars').innerHTML=vh;

  const r=document.getElementById('d-res');
  r.className='res';r.textContent='';

  document.getElementById('d-prev').disabled=(dIdx===0);
  document.getElementById('d-next').textContent=
    dIdx===PROBS.length-1?'🏆 완료':'다음 ▶';
}

function checkDet(){
  const p=PROBS[dIdx];
  let allOk=true;
  p.vars.forEach(v=>{
    const e=document.getElementById('vi-'+v.n);
    if(!e||e.value===''){allOk=false;if(e)e.className='vi ng';return;}
    const ok=Math.abs(parseFloat(e.value)-v.v)<0.001;
    e.className='vi '+(ok?'ok':'ng');
    if(!ok)allOk=false;
  });
  const r=document.getElementById('d-res');
  r.classList.add('show');
  if(allOk){
    r.className='res show ok';
    r.innerHTML='🎉 완벽합니다! 모든 미지수를 정확히 찾았어요!';
    solvedSet.add(dIdx);
    syncDots();
  } else {
    r.className='res show ng';
    r.innerHTML='❌ 틀린 값이 있어요. 성분 방정식을 다시 확인해보세요!';
  }
}

function resetDet(){
  const p=PROBS[dIdx];
  p.vars.forEach(v=>{
    const e=document.getElementById('vi-'+v.n);
    if(e){e.value='';e.className='vi';}
  });
  const r=document.getElementById('d-res');
  r.className='res';r.textContent='';
}

function hintDet(){
  const r=document.getElementById('d-res');
  r.className='res show hint';
  r.innerHTML='💡 힌트: '+PROBS[dIdx].hint;
}

function moveDet(dir){
  const nx=dIdx+dir;
  if(nx<0||nx>=PROBS.length)return;
  dIdx=nx;
  loadProb();
}

initQuiz();
initDet();
</script>
</body>
</html>
"""


def render():
    st.markdown("### 🕵️ 행렬 상등 탐정 게임")
    st.caption("행렬 읽기 퀴즈와 상등 방정식 풀기로 개념을 탄탄하게 다져봐요!")

    components.html(_HTML, height=780, scrolling=False)

    # ── 성찰 기록 폼 ──────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
