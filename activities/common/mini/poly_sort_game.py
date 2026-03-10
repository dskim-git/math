# activities/common/poly_sort_game.py
"""
다항식의 정리 – 항 카드 정렬 게임
x의 내림차순 / 오름차순으로 항 카드를 드래그·정렬하는 인터랙티브 게임
"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 ─────────────────────────────────────────────────────
_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "다항식의정리"

_QUESTIONS = [
    {"type": 'markdown', "text": '**📝 이 활동과 관련된 문제 2개를 스스로 만들고, 풀어보세요**'},
    {"key": '문제1', "label": '문제 1 (스스로 만든 다항식 정리 문제)', "type": 'text_area', "height": 70},
    {"key": '답1', "label": '문제 1의 정답', "type": 'text_input'},
    {"key": '문제2', "label": '문제 2 (스스로 만든 다항식 정리 문제)', "type": 'text_area', "height": 70},
    {"key": '답2', "label": '문제 2의 정답', "type": 'text_input'},
    {"key": '새롭게알게된점', "label": '💡 이 활동을 통해 새롭게 알게 된 점', "type": 'text_area', "height": 90},
    {"key": '느낀점', "label": '💬 이 활동을 하면서 느낀 점', "type": 'text_area', "height": 90},
]

META = {
    "title":       "다항식의 정리 : 항 카드 정렬 게임",
    "description": "다항식의 항을 내림차순·오름차순으로 드래그해 정렬하는 게임입니다.",
    "order":       10,
}

# ── HTML / JS 게임 ──────────────────────────────────────────────────────────
_GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>다항식 정렬 게임</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#f0f4ff 0%,#e8f5e9 100%);min-height:100vh;padding:12px}
h2{text-align:center;color:#3730a3;font-size:1.15rem;margin-bottom:6px}
.subtitle{text-align:center;color:#6b7280;font-size:.82rem;margin-bottom:14px}
/* 진행 바 */
.progress-wrap{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.progress-bar{flex:1;height:8px;background:#e5e7eb;border-radius:99px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,#6366f1,#22d3ee);transition:width .4s}
.score-badge{background:#6366f1;color:#fff;border-radius:99px;padding:2px 12px;font-size:.8rem;font-weight:700;white-space:nowrap}
/* 모드 버튼 */
.mode-row{display:flex;gap:8px;justify-content:center;margin-bottom:12px}
.mode-btn{padding:6px 22px;border:2px solid #6366f1;border-radius:99px;background:#fff;color:#6366f1;font-size:.85rem;font-weight:700;cursor:pointer;transition:.2s}
.mode-btn.active{background:#6366f1;color:#fff}
/* 카드 영역 */
.pool-label,.slot-label{font-size:.78rem;color:#6b7280;margin-bottom:4px;font-weight:600;letter-spacing:.03em}
.card-pool{display:flex;flex-wrap:wrap;gap:8px;min-height:52px;background:#fff;border:2px dashed #c7d2fe;border-radius:12px;padding:10px;margin-bottom:10px;align-items:center}
/* 드롭 슬롯 */
.slots-wrap{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:12px}
.slot{width:90px;min-height:52px;border:2px dashed #a5b4fc;border-radius:10px;background:#f5f3ff;display:flex;align-items:center;justify-content:center;font-size:.78rem;color:#a78bfa;transition:.15s;position:relative}
.slot.over{background:#ede9fe;border-color:#6366f1}
.slot-num{position:absolute;top:2px;left:6px;font-size:.65rem;color:#c4b5fd}
/* 카드 */
.card{display:inline-flex;align-items:center;justify-content:center;padding:8px 14px;border-radius:10px;font-size:1rem;font-weight:700;cursor:grab;user-select:none;min-width:70px;text-align:center;box-shadow:0 2px 6px rgba(0,0,0,.12);transition:transform .1s,box-shadow .1s;border:2px solid transparent}
.card:active{cursor:grabbing;transform:scale(1.06);box-shadow:0 6px 16px rgba(0,0,0,.2)}
.card.dragging{opacity:.4}
/* 카드 색깔 (차수별) */
.deg4{background:#fce7f3;border-color:#f9a8d4;color:#be185d}
.deg3{background:#ede9fe;border-color:#c4b5fd;color:#5b21b6}
.deg2{background:#dbeafe;border-color:#93c5fd;color:#1d4ed8}
.deg1{background:#d1fae5;border-color:#6ee7b7;color:#065f46}
.deg0{background:#fef3c7;border-color:#fcd34d;color:#92400e}
/* 버튼 */
.btn-row{display:flex;gap:8px;justify-content:center;margin-bottom:10px;flex-wrap:wrap}
.btn{padding:8px 24px;border-radius:99px;border:none;font-size:.88rem;font-weight:700;cursor:pointer;transition:.2s}
.btn-check{background:#6366f1;color:#fff}
.btn-check:hover{background:#4f46e5}
.btn-next{background:#22c55e;color:#fff}
.btn-next:hover{background:#16a34a}
.btn-hint{background:#f59e0b;color:#fff}
.btn-hint:hover{background:#d97706}
.btn-reset{background:#e5e7eb;color:#374151}
.btn-reset:hover{background:#d1d5db}
/* 피드백 */
.feedback{text-align:center;font-size:.95rem;font-weight:700;min-height:26px;margin-bottom:8px;transition:opacity .3s}
.feedback.correct{color:#059669}
.feedback.wrong{color:#dc2626}
.feedback.hint{color:#92400e}
/* 문제 표시 */
.problem-box{background:#fff;border:1.5px solid #e0e7ff;border-radius:12px;padding:10px 16px;text-align:center;margin-bottom:10px}
.problem-poly{font-size:1.1rem;font-weight:700;color:#1e1b4b;letter-spacing:.02em}
.problem-ask{font-size:.8rem;color:#6b7280;margin-top:4px}
/* 정답 표시 */
.answer-reveal{background:#ecfdf5;border:1.5px solid #6ee7b7;border-radius:10px;padding:8px 14px;text-align:center;font-size:.92rem;color:#065f46;font-weight:600;margin-bottom:8px;display:none}
/* confetti canvas */
#confetti{position:fixed;top:0;left:0;pointer-events:none;width:100%;height:100%;z-index:9999}
</style>
</head>
<body>
<canvas id="confetti"></canvas>

<h2>🃏 다항식의 정리 – 항 카드 정렬 게임</h2>
<p class="subtitle">항 카드를 드래그하여 목표 순서에 맞게 아래 칸에 놓으세요!</p>

<div class="progress-wrap">
  <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
  <div class="score-badge">점수 <span id="scoreDisp">0</span></div>
</div>

<div class="mode-row">
  <button class="mode-btn active" id="btnDesc" onclick="setMode('desc')">내림차순</button>
  <button class="mode-btn" id="btnAsc" onclick="setMode('asc')">오름차순</button>
</div>

<div class="problem-box">
  <div class="problem-poly" id="problemPoly">—</div>
  <div class="problem-ask" id="problemAsk">x에 대하여 내림차순으로 정리하세요.</div>
</div>

<div class="pool-label">📦 항 카드 (여기서 드래그)</div>
<div class="card-pool" id="cardPool"></div>

<div class="slot-label">🎯 정렬 칸 (카드를 순서대로 놓으세요)</div>
<div class="slots-wrap" id="slotsWrap"></div>

<div class="answer-reveal" id="answerReveal"></div>
<div class="feedback" id="feedback"></div>

<div class="btn-row">
  <button class="btn btn-check" onclick="checkAnswer()">✅ 확인</button>
  <button class="btn btn-hint" onclick="showHint()">💡 힌트</button>
  <button class="btn btn-reset" onclick="resetSlots()">🔄 초기화</button>
  <button class="btn btn-next" id="btnNext" onclick="nextProblem()" style="display:none">➡️ 다음 문제</button>
</div>

<script>
// ── 문제 데이터 ─────────────────────────────────────────────────────────────
// term: {text, degree}
const PROBLEMS = [
  {
    label:"① 일차·이차·삼차·상수항",
    terms:[
      {text:"3x",    deg:1},
      {text:"x³",    deg:3},
      {text:"-2x²",  deg:2},
      {text:"+5",    deg:0},
      {text:"-4x",   deg:1, dup:true, skip:true},  // 헷갈림용 동류항 포함 (동류항X - 별개 문제로)
    ]
  },
  {label:"① 4차 다항식",
   terms:[{text:"3x",deg:1},{text:"x⁴",deg:4},{text:"-2x²",deg:2},{text:"+5",deg:0},{text:"-x³",deg:3}]},
  {label:"② 3차 다항식",
   terms:[{text:"-x³",deg:3},{text:"+4",deg:0},{text:"-2x",deg:1},{text:"+3x²",deg:2}]},
  {label:"③ 4차 다항식",
   terms:[{text:"2x²",deg:2},{text:"-x⁴",deg:4},{text:"+3x³",deg:3},{text:"-5",deg:0}]},
  {label:"④ 5차 다항식",
   terms:[{text:"x",deg:1},{text:"+4x³",deg:3},{text:"-3x²",deg:2},{text:"-2",deg:0},{text:"+x⁵",deg:5}]},
  {label:"⑤ 4차 다항식",
   terms:[{text:"5x²",deg:2},{text:"+2",deg:0},{text:"-3x³",deg:3},{text:"+x",deg:1},{text:"-x⁴",deg:4}]},
  {label:"⑥ 3차 다항식",
   terms:[{text:"-2x",deg:1},{text:"+4x³",deg:3},{text:"-3",deg:0},{text:"+5x²",deg:2}]},
  {label:"⑦ 4차 다항식 (x 기준)",
   terms:[{text:"2x⁴",deg:4},{text:"-x",deg:1},{text:"+3x²",deg:2},{text:"-5x³",deg:3},{text:"+7",deg:0}]},
];

// 첫 번째 entry는 dup 테스트용으로 제거, 실제 문제 배열
const problems = PROBLEMS.slice(1);

let currentProblem = 0;
let mode = 'desc'; // 'desc' | 'asc'
let score = 0;
let dragSrcCard = null;
let dragSrcIsPool = true;
let dragSrcSlotIdx = -1;

// 슬롯 상태 (카드 객체 or null)
let slots = [];
// 풀 상태
let pool = [];

const DEG_CLASS = ['deg0','deg1','deg2','deg3','deg4','deg4']; // 5차도 deg4 색상

function setMode(m){
  mode = m;
  document.getElementById('btnDesc').classList.toggle('active', m==='desc');
  document.getElementById('btnAsc').classList.toggle('active', m==='asc');
  document.getElementById('problemAsk').textContent =
    m==='desc' ? 'x에 대하여 내림차순으로 정리하세요.' : 'x에 대하여 오름차순으로 정리하세요.';
  loadProblem();
}

function loadProblem(){
  const p = problems[currentProblem];
  // 풀 초기화: 섞기
  pool = shuffle([...p.terms]);
  slots = Array(p.terms.length).fill(null);
  renderAll();
  setFeedback('','');
  document.getElementById('answerReveal').style.display='none';
  document.getElementById('btnNext').style.display='none';
  // 진행 바
  document.getElementById('progressFill').style.width = ((currentProblem/problems.length)*100)+'%';
  // 문제 다항식 표시 (무작위 순서로)
  document.getElementById('problemPoly').textContent = pool.map(t=>t.text).join(' ');
}

function shuffle(arr){
  for(let i=arr.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [arr[i],arr[j]]=[arr[j],arr[i]];
  }
  return arr;
}

function getSortedDegs(){
  const p = problems[currentProblem];
  const degs = p.terms.map(t=>t.deg);
  return mode==='desc'
    ? [...degs].sort((a,b)=>b-a)
    : [...degs].sort((a,b)=>a-b);
}

function degClass(d){ return DEG_CLASS[Math.min(d,4)]; }

function renderAll(){
  renderPool();
  renderSlots();
}

function makeCardEl(term, fromPool, slotIdx){
  const el = document.createElement('div');
  el.className = `card ${degClass(term.deg)}`;
  el.textContent = term.text;
  el.draggable = true;
  el.dataset.deg = term.deg;
  el.dataset.text = term.text;

  el.addEventListener('dragstart', e=>{
    dragSrcCard = term;
    dragSrcIsPool = fromPool;
    dragSrcSlotIdx = slotIdx;
    el.classList.add('dragging');
    e.dataTransfer.effectAllowed='move';
  });
  el.addEventListener('dragend', ()=>el.classList.remove('dragging'));

  // 클릭으로 빈 슬롯에 자동 배치
  el.addEventListener('click', ()=>{
    if(fromPool){
      const emptyIdx = slots.findIndex(s=>s===null);
      if(emptyIdx>=0){
        slots[emptyIdx]=term;
        pool = pool.filter(t=>t!==term);
        renderAll();
      }
    } else {
      // 슬롯→풀으로 반환
      pool.push(term);
      slots[slotIdx]=null;
      renderAll();
    }
  });
  return el;
}

function renderPool(){
  const wrap = document.getElementById('cardPool');
  wrap.innerHTML='';
  pool.forEach(t=>{
    wrap.appendChild(makeCardEl(t, true, -1));
  });
  // 드롭 이벤트
  wrap.ondragover = e=>{ e.preventDefault(); wrap.style.borderColor='#6366f1'; };
  wrap.ondragleave = ()=>{ wrap.style.borderColor='#c7d2fe'; };
  wrap.ondrop = e=>{
    e.preventDefault();
    wrap.style.borderColor='#c7d2fe';
    if(!dragSrcIsPool && dragSrcSlotIdx>=0){
      pool.push(slots[dragSrcSlotIdx]);
      slots[dragSrcSlotIdx]=null;
      renderAll();
    }
  };
}

function renderSlots(){
  const wrap = document.getElementById('slotsWrap');
  wrap.innerHTML='';
  const n = problems[currentProblem].terms.length;
  for(let i=0;i<n;i++){
    const slot = document.createElement('div');
    slot.className='slot';
    const num = document.createElement('span');
    num.className='slot-num';
    num.textContent=(i+1)+'번';
    slot.appendChild(num);

    if(slots[i]){
      slot.appendChild(makeCardEl(slots[i], false, i));
    }

    const idx = i; // closure
    slot.ondragover = e=>{ e.preventDefault(); slot.classList.add('over'); };
    slot.ondragleave = ()=>slot.classList.remove('over');
    slot.ondrop = e=>{
      e.preventDefault();
      slot.classList.remove('over');
      if(dragSrcIsPool){
        // pool → slot
        if(slots[idx]){
          // 기존 카드 → 풀로 반환
          pool.push(slots[idx]);
        }
        slots[idx]=dragSrcCard;
        pool = pool.filter(t=>t!==dragSrcCard);
      } else {
        // slot → slot (교환)
        const tmp = slots[idx];
        slots[idx]=slots[dragSrcSlotIdx];
        slots[dragSrcSlotIdx]=tmp;
      }
      renderAll();
    };
    wrap.appendChild(slot);
  }
}

function checkAnswer(){
  const filled = slots.every(s=>s!==null);
  if(!filled){ setFeedback('⚠️ 모든 칸을 채운 후 확인하세요.','wrong'); return; }

  const sortedDegs = getSortedDegs();
  const myDegs = slots.map(s=>s.deg);
  const correct = sortedDegs.every((d,i)=>d===myDegs[i]);

  if(correct){
    score += 10;
    document.getElementById('scoreDisp').textContent=score;
    setFeedback('🎉 정답입니다! +10점','correct');
    document.getElementById('btnNext').style.display='inline-block';
    launchConfetti();
    highlightSlots(true);
  } else {
    setFeedback('❌ 틀렸습니다. 다시 시도하거나 힌트를 사용해보세요.','wrong');
    highlightSlots(false);
  }
}

function highlightSlots(ok){
  const sortedDegs = getSortedDegs();
  const slotEls = document.querySelectorAll('.slot');
  slotEls.forEach((el,i)=>{
    if(!slots[i]) return;
    if(ok){
      el.style.background='#d1fae5';
      el.style.borderColor='#34d399';
    } else {
      const correct = slots[i].deg === sortedDegs[i];
      el.style.background = correct ? '#d1fae5' : '#fee2e2';
      el.style.borderColor = correct ? '#34d399' : '#f87171';
    }
  });
  setTimeout(()=>{
    document.querySelectorAll('.slot').forEach(el=>{
      el.style.background=''; el.style.borderColor='';
    });
  }, ok ? 3000 : 1500);
}

function showHint(){
  const sortedDegs = getSortedDegs();
  const p = problems[currentProblem];
  const ordered = [...p.terms].sort((a,b)=> mode==='desc' ? b.deg-a.deg : a.deg-b.deg);
  const ansText = ordered.map(t=>t.text).join(' ');
  const box = document.getElementById('answerReveal');
  box.textContent = (mode==='desc' ? '내림차순 정답: ' : '오름차순 정답: ') + ansText;
  box.style.display='block';
  setFeedback('💡 힌트: 가장 높은 차수의 항을 먼저 찾아보세요!','hint');
}

function resetSlots(){
  const p = problems[currentProblem];
  pool = shuffle([...p.terms]);
  slots = Array(p.terms.length).fill(null);
  renderAll();
  setFeedback('','');
  document.getElementById('answerReveal').style.display='none';
  document.getElementById('btnNext').style.display='none';
}

function nextProblem(){
  currentProblem = (currentProblem+1) % problems.length;
  if(currentProblem===0){
    setFeedback('🏆 모든 문제를 완료했습니다! 처음부터 다시 시작합니다.','correct');
  }
  loadProblem();
}

function setFeedback(msg, cls){
  const el=document.getElementById('feedback');
  el.textContent=msg;
  el.className='feedback'+(cls?' '+cls:'');
}

// confetti
function launchConfetti(){
  const canvas=document.getElementById('confetti');
  canvas.width=window.innerWidth; canvas.height=window.innerHeight;
  const ctx=canvas.getContext('2d');
  const pieces=Array.from({length:80},()=>({
    x:Math.random()*canvas.width, y:Math.random()*canvas.height-canvas.height,
    r:Math.random()*4+2, dx:(Math.random()-.5)*2,
    dy:Math.random()*3+2, color:`hsl(${Math.random()*360},80%,60%)`,
    rot:Math.random()*360, drot:(Math.random()-.5)*5
  }));
  let frame=0;
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    pieces.forEach(p=>{
      ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot*Math.PI/180);
      ctx.fillStyle=p.color;ctx.fillRect(-p.r,-p.r,p.r*2,p.r*2);
      ctx.restore();
      p.x+=p.dx; p.y+=p.dy; p.rot+=p.drot;
    });
    frame++;
    if(frame<90) requestAnimationFrame(draw);
    else ctx.clearRect(0,0,canvas.width,canvas.height);
  }
  draw();
}

// 초기 로드
loadProblem();
</script>
</body>
</html>
"""

def render():
    st.header("🃏 다항식의 정리 – 항 카드 정렬 게임")
    st.caption(
        "x에 대한 내림차순·오름차순 배열을 카드 드래그로 연습합니다. "
        "카드를 드래그하거나 클릭하여 아래 칸에 순서대로 놓으세요."
    )

    components.html(_GAME_HTML, height=620, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
