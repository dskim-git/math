# activities/probability_new/mini/random_sampling_lab.py
"""
임의추출 방법 시뮬레이션 — 4가지 방법(제비뽑기·난수주사위·난수표·엑셀)을
직접 시뮬레이션해 보는 미니 활동.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎲 임의추출 방법 시뮬레이션",
    "description": "제비뽑기·난수주사위·난수표·엑셀 4가지 방법으로 표본을 임의추출하는 과정을 직접 체험합니다.",
    "order": 10,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "임의추출방법시뮬레이션"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 임의추출 방법 시뮬레이션**"},
    {
        "key": "임의추출의미",
        "label": "이 활동에서 '임의추출(무작위추출)'이란 어떻게 표본을 뽑는 것이라고 정의할 수 있을까요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) 모집단의 모든 대상이 ___ 확률로 뽑힐 수 있도록 ___ 하게 뽑는 것...",
    },
    {
        "key": "방법비교",
        "label": "4가지 방법(제비뽑기·난수주사위·난수표·엑셀) 중 모집단이 클 때 가장 효율적이라고 생각되는 방법은? 그 이유는 무엇인가요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "모집단의 크기가 클수록 ... 가 가장 효율적이다. 왜냐하면...",
    },
    {
        "key": "방법장단점",
        "label": "제비뽑기와 컴퓨터 프로그램(엑셀)으로 임의추출하는 것을 비교했을 때, 각각의 장점과 단점은 무엇인가요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "제비뽑기 — 장점: 모두가 직관적으로 공정함을 확인 가능 / 단점: 인원이 많으면 ...\n엑셀 — 장점: ... / 단점: ...",
    },
    {
        "key": "난수표주사위주의",
        "label": "난수주사위로 300명 중 5명을, 난수표로 50명 중 5명을 뽑을 때 중복된 번호나 모집단 크기를 벗어난 번호가 나오면 어떻게 처리해야 할까요? 그 이유는?",
        "type": "text_area",
        "height": 100,
        "placeholder": "예) 이미 뽑힌 번호나 범위를 벗어난 번호는 다시 뽑아야 한다. 왜냐하면...",
    },
    {
        "key": "공정성의의미",
        "label": "만약 어떤 사람이 '키가 큰 순서대로 5명을 뽑겠다'고 한다면, 이것은 임의추출이라고 할 수 있을까요? 왜 그렇게 생각하나요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "임의추출이 아니다/맞다. 왜냐하면...",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 활동을 마친 후 느낀 점",
        "type": "text_area",
        "height": 90,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: 제비뽑기 (Drawing Lots)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB1 = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#1e293b 100%);
  color:#e2e8f0;padding:18px 14px;min-height:100vh;
}
.hdr{
  text-align:center;background:linear-gradient(135deg,rgba(251,191,36,.18),rgba(249,115,22,.12));
  border:2px solid rgba(251,191,36,.4);border-radius:18px;padding:16px 20px;margin-bottom:14px;
}
.hdr h1{font-size:1.5rem;font-weight:900;color:#fbbf24;margin-bottom:6px}
.hdr p{font-size:1rem;color:#cbd5e1;line-height:1.6}

.controls{
  display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px 16px;
}
.ctrl{display:flex;flex-direction:column;align-items:center;gap:6px;min-width:200px}
.ctrl label{font-size:1rem;font-weight:800;color:#a5b4fc}
.ctrl input[type=range]{width:100%;accent-color:#fbbf24}
.ctrl .val{font-size:1.4rem;font-weight:900;color:#fbbf24;font-family:'Courier New',monospace}

.stage{
  display:grid;grid-template-columns:1fr 1fr;gap:14px;
}
@media(max-width:680px){.stage{grid-template-columns:1fr}}

.jar-zone{
  background:rgba(15,23,42,.55);border:2px dashed rgba(251,191,36,.5);
  border-radius:18px;padding:18px;text-align:center;position:relative;min-height:360px;
}
.jar-title{font-size:1.15rem;font-weight:900;color:#fef3c7;margin-bottom:10px}
.jar{
  width:200px;height:230px;margin:0 auto;position:relative;
  perspective:600px;
}
.jar-body{
  position:absolute;left:50%;top:35px;transform:translateX(-50%);
  width:170px;height:195px;
  background:linear-gradient(180deg,rgba(165,180,252,.25) 0%,rgba(99,102,241,.4) 100%);
  border:3px solid rgba(165,180,252,.8);border-radius:6px 6px 60px 60px / 6px 6px 30px 30px;
  box-shadow:inset -10px 0 20px rgba(0,0,0,.25),inset 10px 0 20px rgba(255,255,255,.12);
  overflow:hidden;
}
.jar-mouth{
  position:absolute;left:50%;top:30px;transform:translateX(-50%);
  width:175px;height:18px;background:#1e1b4b;
  border:3px solid rgba(165,180,252,.95);border-radius:50%;
  z-index:2;
}
.slips-inside{
  position:absolute;inset:25px 10px 14px;display:flex;flex-wrap:wrap;
  align-items:flex-end;justify-content:center;gap:3px;
}
.slip{
  display:inline-block;width:14px;height:18px;background:#fef3c7;border-radius:2px;
  box-shadow:0 1px 2px rgba(0,0,0,.3);
  animation:wiggle 1.8s ease-in-out infinite;
}
.slip:nth-child(2n){background:#fed7aa;animation-delay:.3s}
.slip:nth-child(3n){background:#bfdbfe;animation-delay:.6s}
.slip:nth-child(5n){background:#fbcfe8;animation-delay:.9s}
@keyframes wiggle{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-1px) rotate(3deg)}}

.jar.shaking{animation:shakeIt .4s ease-in-out 4}
@keyframes shakeIt{
  0%,100%{transform:rotate(0)}
  25%{transform:rotate(-9deg)}
  75%{transform:rotate(9deg)}
}

.flying-slip{
  position:absolute;width:60px;height:42px;background:#fef3c7;
  border:2px solid #f59e0b;border-radius:6px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.2rem;font-weight:900;color:#92400e;
  box-shadow:0 8px 18px rgba(0,0,0,.4);
  z-index:5;opacity:0;transition:all .9s cubic-bezier(.5,-.3,.5,1.3);
  font-family:'Courier New',monospace;
}
.flying-slip.fly{opacity:1}

.btn-row{
  display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:14px;
}
.btn{
  font-size:1.05rem;font-weight:900;padding:11px 20px;border:none;
  border-radius:12px;cursor:pointer;transition:all .2s;
}
.btn-pri{
  background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#1e293b;
  box-shadow:0 4px 14px rgba(251,191,36,.4);
}
.btn-pri:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 7px 20px rgba(251,191,36,.6)}
.btn-pri:disabled{opacity:.4;cursor:default;transform:none;box-shadow:none}
.btn-sec{
  background:rgba(99,102,241,.18);color:#a5b4fc;border:2px solid rgba(99,102,241,.4);
}
.btn-sec:hover{background:rgba(99,102,241,.32);transform:translateY(-2px)}

.results-zone{
  background:rgba(15,23,42,.55);border:2px solid rgba(34,197,94,.35);
  border-radius:18px;padding:18px;
}
.res-title{
  font-size:1.15rem;font-weight:900;color:#86efac;margin-bottom:12px;text-align:center;
}
.res-grid{
  display:grid;grid-template-columns:repeat(auto-fit, minmax(86px, 1fr));gap:10px;
}
.res-card{
  background:rgba(34,197,94,.12);border:2px solid rgba(34,197,94,.4);
  border-radius:12px;padding:14px 6px;text-align:center;
  animation:popRes .5s cubic-bezier(.34,1.56,.64,1);
}
.res-card .lab{font-size:.78rem;color:#86efac;font-weight:800}
.res-card .num{font-size:2rem;font-weight:900;color:#fef3c7;font-family:'Courier New',monospace;line-height:1.2}
@keyframes popRes{from{opacity:0;transform:scale(.5)}to{opacity:1;transform:scale(1)}}

.res-empty{
  text-align:center;color:#64748b;font-size:1rem;padding:50px 10px;
}

.done-msg{
  margin-top:14px;padding:14px;background:rgba(34,197,94,.18);
  border:2px solid #22c55e;border-radius:12px;text-align:center;
  font-size:1.1rem;font-weight:900;color:#86efac;
  display:none;animation:popRes .5s ease;
}
.done-msg.on{display:block}
</style>
</head>
<body>
<div class="hdr">
  <h1>🎟️ 제비뽑기로 임의추출하기</h1>
  <p>학생 수만큼 종이쪽지에 번호를 적어 통에 넣고, 잘 섞은 뒤 한 장씩 뽑아요!</p>
</div>

<div class="controls">
  <div class="ctrl">
    <label>👥 모집단 크기 (학생 수): <span class="val" id="vN">30</span>명</label>
    <input type="range" id="rN" min="10" max="50" value="30" step="1">
  </div>
  <div class="ctrl">
    <label>🎯 표본 크기 (뽑을 인원): <span class="val" id="vK">5</span>명</label>
    <input type="range" id="rK" min="2" max="10" value="5" step="1">
  </div>
</div>

<div class="stage">
  <div class="jar-zone">
    <div class="jar-title">📦 번호가 적힌 쪽지가 든 통</div>
    <div class="jar" id="jar">
      <div class="jar-mouth"></div>
      <div class="jar-body">
        <div class="slips-inside" id="slipsInside"></div>
      </div>
    </div>
    <div class="btn-row">
      <button class="btn btn-sec" id="btnShake">🌀 통 흔들기</button>
      <button class="btn btn-pri" id="btnDraw">✋ 한 장 뽑기</button>
    </div>
  </div>

  <div class="results-zone">
    <div class="res-title">🏆 뽑힌 번호 (표본)</div>
    <div class="res-grid" id="resGrid">
      <div class="res-empty">아직 뽑힌 번호가 없어요.<br>오른쪽 통을 흔들고 쪽지를 뽑아 보세요!</div>
    </div>
    <div class="done-msg" id="doneMsg">🎉 5명 표본 추출 완료!</div>
    <div class="btn-row">
      <button class="btn btn-sec" id="btnReset">🔄 다시 시작</button>
    </div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);
let N = 30, K = 5;
let pool = [];      // remaining numbers
let drawn = [];     // already drawn

function renderSlipsInside(){
  const inside = $('slipsInside');
  inside.innerHTML = '';
  const cnt = Math.min(pool.length, 30);
  for(let i=0; i<cnt; i++){
    const s = document.createElement('div');
    s.className = 'slip';
    inside.appendChild(s);
  }
}

function renderResults(){
  const g = $('resGrid');
  if(drawn.length === 0){
    g.innerHTML = '<div class="res-empty">아직 뽑힌 번호가 없어요.<br>오른쪽 통을 흔들고 쪽지를 뽑아 보세요!</div>';
    return;
  }
  g.innerHTML = drawn.map((n,i)=>(
    `<div class="res-card">
       <div class="lab">${i+1}번째</div>
       <div class="num">${String(n).padStart(2,'0')}</div>
     </div>`
  )).join('');
}

function reset(){
  N = parseInt($('rN').value);
  K = parseInt($('rK').value);
  pool = Array.from({length:N}, (_,i) => i+1);
  drawn = [];
  $('doneMsg').classList.remove('on');
  $('btnDraw').disabled = false;
  renderSlipsInside();
  renderResults();
}

$('rN').oninput = e => { $('vN').textContent = e.target.value; reset(); };
$('rK').oninput = e => { $('vK').textContent = e.target.value; reset(); };
$('btnReset').onclick = reset;

$('btnShake').onclick = () => {
  $('jar').classList.add('shaking');
  setTimeout(()=>$('jar').classList.remove('shaking'), 1700);
};

$('btnDraw').onclick = () => {
  if(drawn.length >= K || pool.length === 0) return;
  // shake briefly
  $('jar').classList.add('shaking');
  setTimeout(()=>$('jar').classList.remove('shaking'), 600);

  // pick random
  const idx = Math.floor(Math.random() * pool.length);
  const num = pool[idx];
  pool.splice(idx, 1);

  // animate flying slip
  const fly = document.createElement('div');
  fly.className = 'flying-slip';
  fly.textContent = String(num).padStart(2,'0');
  const jar = $('jar');
  jar.appendChild(fly);
  fly.style.left = '70px';
  fly.style.top = '70px';
  requestAnimationFrame(()=>{
    fly.classList.add('fly');
    fly.style.left = '20px';
    fly.style.top = '-40px';
    fly.style.transform = 'rotate(-22deg) scale(1.3)';
  });

  setTimeout(()=>{
    drawn.push(num);
    renderSlipsInside();
    renderResults();
    fly.remove();
    if(drawn.length >= K){
      $('btnDraw').disabled = true;
      $('doneMsg').classList.add('on');
    }
  }, 950);
};

reset();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: 난수주사위 (Random Dice — 3 icosahedrons giving 000~999)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB2 = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#312e81 100%);
  color:#e2e8f0;padding:18px 14px;min-height:100vh;
}
.hdr{
  text-align:center;background:linear-gradient(135deg,rgba(168,85,247,.18),rgba(236,72,153,.12));
  border:2px solid rgba(168,85,247,.4);border-radius:18px;padding:16px 20px;margin-bottom:14px;
}
.hdr h1{font-size:1.5rem;font-weight:900;color:#e9d5ff;margin-bottom:6px}
.hdr p{font-size:1rem;color:#cbd5e1;line-height:1.6}

.problem-box{
  background:rgba(15,23,42,.6);border:2px solid rgba(168,85,247,.35);
  border-radius:14px;padding:14px 18px;margin-bottom:14px;text-align:center;
  font-size:1.1rem;font-weight:800;color:#fef3c7;line-height:1.7;
}
.problem-box .hi{color:#fbbf24;font-size:1.25rem}

.dice-stage{
  background:rgba(15,23,42,.55);border:2px dashed rgba(168,85,247,.45);
  border-radius:18px;padding:24px 18px;text-align:center;margin-bottom:14px;
}
.dice-row{
  display:flex;gap:18px;justify-content:center;align-items:center;flex-wrap:wrap;
  min-height:170px;margin-bottom:14px;
}
.die{
  width:130px;height:130px;position:relative;
  display:flex;align-items:center;justify-content:center;
}
.die-shape{
  width:100%;height:100%;
  background:
    radial-gradient(circle at 30% 25%, rgba(255,255,255,.45), transparent 45%),
    linear-gradient(135deg, var(--c1), var(--c2));
  clip-path:polygon(50% 0%, 95% 25%, 95% 75%, 50% 100%, 5% 75%, 5% 25%);
  border:none;box-shadow:0 6px 20px rgba(0,0,0,.45);
  display:flex;align-items:center;justify-content:center;
  position:relative;
}
.die-shape::before{
  content:'';position:absolute;inset:8%;
  clip-path:polygon(50% 0%, 95% 25%, 95% 75%, 50% 100%, 5% 75%, 5% 25%);
  background:
    linear-gradient(45deg, transparent 48%, rgba(255,255,255,.18) 49%, rgba(255,255,255,.18) 51%, transparent 52%),
    linear-gradient(-45deg, transparent 48%, rgba(0,0,0,.18) 49%, rgba(0,0,0,.18) 51%, transparent 52%);
}
.die-num{
  font-size:3.8rem;font-weight:900;color:#fff;
  font-family:'Courier New',monospace;
  text-shadow:0 3px 8px rgba(0,0,0,.7), 0 0 12px rgba(255,255,255,.3);
  z-index:2;
}
.die.d1 .die-shape{--c1:#a855f7;--c2:#7c3aed}
.die.d2 .die-shape{--c1:#f97316;--c2:#c2410c}
.die.d3 .die-shape{--c1:#10b981;--c2:#047857}
.die.rolling .die-shape{animation:rollDie .6s linear}
.die.rolling .die-num{animation:flicker .08s linear infinite}
@keyframes rollDie{
  0%{transform:rotate(0) scale(1)}
  50%{transform:rotate(180deg) scale(1.15)}
  100%{transform:rotate(360deg) scale(1)}
}
@keyframes flicker{
  0%{opacity:1}50%{opacity:.3}100%{opacity:1}
}

.combined{
  font-size:1.6rem;font-weight:900;color:#fef3c7;margin:10px 0 6px;
}
.combined .num{
  font-size:3.2rem;color:#fbbf24;font-family:'Courier New',monospace;
  letter-spacing:6px;display:inline-block;min-width:200px;
  text-shadow:0 4px 12px rgba(251,191,36,.4);
}
.status{
  font-size:1.05rem;font-weight:800;margin:8px 0;padding:8px 14px;
  border-radius:10px;display:inline-block;min-height:38px;
}
.status.ok{background:rgba(34,197,94,.18);color:#86efac;border:1.5px solid #22c55e}
.status.bad{background:rgba(239,68,68,.16);color:#fca5a5;border:1.5px solid #ef4444}
.status.idle{background:rgba(100,116,139,.18);color:#cbd5e1}

.btn-row{
  display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:14px;
}
.btn{
  font-size:1.1rem;font-weight:900;padding:12px 24px;border:none;
  border-radius:12px;cursor:pointer;transition:all .2s;
}
.btn-pri{
  background:linear-gradient(135deg,#a855f7,#ec4899);color:#fff;
  box-shadow:0 4px 14px rgba(168,85,247,.4);
}
.btn-pri:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 7px 20px rgba(168,85,247,.6)}
.btn-pri:disabled{opacity:.4;cursor:default;transform:none;box-shadow:none}
.btn-sec{
  background:rgba(99,102,241,.18);color:#a5b4fc;border:2px solid rgba(99,102,241,.4);
}
.btn-sec:hover{background:rgba(99,102,241,.32);transform:translateY(-2px)}

.history-zone{
  background:rgba(15,23,42,.55);border:2px solid rgba(99,102,241,.3);
  border-radius:18px;padding:16px;
}
.hist-row{
  display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;
}
.hist-title{font-size:1.1rem;font-weight:900;color:#a5b4fc}
.hist-count{
  font-size:.95rem;font-weight:800;color:#fbbf24;
  background:rgba(251,191,36,.12);padding:5px 11px;border-radius:8px;
  border:1.5px solid rgba(251,191,36,.4);
}
.hist-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(78px,1fr));gap:8px;
  margin-bottom:10px;
}
.hist-item{
  background:rgba(30,41,59,.7);border:2px solid;border-radius:10px;
  padding:9px 4px;text-align:center;
  font-family:'Courier New',monospace;font-size:1.25rem;font-weight:900;
  animation:popIn .35s cubic-bezier(.34,1.56,.64,1);
}
.hist-item.ok{border-color:rgba(34,197,94,.5);color:#86efac;background:rgba(34,197,94,.1)}
.hist-item.dup{border-color:rgba(251,191,36,.5);color:#fbbf24;text-decoration:line-through;opacity:.7}
.hist-item.over{border-color:rgba(239,68,68,.5);color:#f87171;text-decoration:line-through;opacity:.7}
@keyframes popIn{from{opacity:0;transform:scale(.5)}to{opacity:1;transform:scale(1)}}

.sample-result{
  margin-top:14px;padding:14px;background:rgba(34,197,94,.15);
  border:2px solid #22c55e;border-radius:14px;display:none;
}
.sample-result.on{display:block;animation:popIn .5s ease}
.sample-result .sr-title{font-size:1.1rem;font-weight:900;color:#86efac;margin-bottom:8px;text-align:center}
.sample-result .sr-list{
  display:flex;gap:10px;justify-content:center;flex-wrap:wrap;
}
.sample-result .sr-num{
  font-size:1.7rem;font-weight:900;color:#fef3c7;font-family:'Courier New',monospace;
  padding:8px 16px;background:rgba(34,197,94,.25);border-radius:10px;
  border:2px solid #22c55e;
}
</style>
</head>
<body>
<div class="hdr">
  <h1>🎲 난수주사위로 임의추출하기</h1>
  <p>각 면에 0~9가 두 번씩 적힌 <b>정이십면체 주사위</b> 3개를 동시에 굴려 3자리 수를 만들어요!</p>
</div>

<div class="problem-box">
  📌 <span class="hi">300명</span>의 학생 중에서 <span class="hi">5명</span>을 임의추출하기<br>
  <span style="font-size:.95rem;color:#cbd5e1;font-weight:600">→ 0~299 범위의 번호만 유효 · 중복 번호는 제외</span>
</div>

<div class="dice-stage">
  <div class="dice-row">
    <div class="die d1" id="die1">
      <div class="die-shape"><span class="die-num" id="num1">?</span></div>
    </div>
    <div class="die d2" id="die2">
      <div class="die-shape"><span class="die-num" id="num2">?</span></div>
    </div>
    <div class="die d3" id="die3">
      <div class="die-shape"><span class="die-num" id="num3">?</span></div>
    </div>
  </div>
  <div class="combined">→ 결과: <span class="num" id="combined">___</span></div>
  <div class="status idle" id="status">주사위를 굴려보세요!</div>
  <div class="btn-row">
    <button class="btn btn-pri" id="btnRoll">🎲 주사위 굴리기</button>
    <button class="btn btn-sec" id="btnAuto">⚡ 5명 모두 자동 추출</button>
    <button class="btn btn-sec" id="btnReset">🔄 다시 시작</button>
  </div>
</div>

<div class="history-zone">
  <div class="hist-row">
    <div class="hist-title">📜 추출 기록</div>
    <div class="hist-count"><span id="okCnt">0</span>/5명 추출 · 총 <span id="totCnt">0</span>회 시행</div>
  </div>
  <div class="hist-grid" id="histGrid"></div>
  <div class="sample-result" id="sampleResult">
    <div class="sr-title">🏆 최종 표본 5명</div>
    <div class="sr-list" id="srList"></div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);
const POPULATION = 300;
const TARGET = 5;

let drawn = [];   // accepted numbers
let history = []; // {n, status: 'ok'|'dup'|'over'}
let rolling = false;

function rollOnce(){
  if(rolling) return;
  if(drawn.length >= TARGET) return;
  rolling = true;
  $('btnRoll').disabled = true;

  // animate spinning numbers
  const dice = [$('die1'), $('die2'), $('die3')];
  const nums = [$('num1'), $('num2'), $('num3')];
  dice.forEach(d => d.classList.add('rolling'));
  const flicker = setInterval(()=>{
    nums.forEach(n => n.textContent = Math.floor(Math.random()*10));
  }, 80);

  setTimeout(()=>{
    clearInterval(flicker);
    dice.forEach(d => d.classList.remove('rolling'));
    const d1 = Math.floor(Math.random()*10);
    const d2 = Math.floor(Math.random()*10);
    const d3 = Math.floor(Math.random()*10);
    nums[0].textContent = d1;
    nums[1].textContent = d2;
    nums[2].textContent = d3;
    const num = d1*100 + d2*10 + d3;
    $('combined').textContent = String(num).padStart(3,'0');

    // judge
    let st;
    if(num >= POPULATION){
      st = 'over';
      $('status').className = 'status bad';
      $('status').textContent = `❌ ${String(num).padStart(3,'0')}번 → 300명 범위(0~299) 밖! 다시 굴려요`;
    } else if(drawn.includes(num)){
      st = 'dup';
      $('status').className = 'status bad';
      $('status').textContent = `⚠️ ${String(num).padStart(3,'0')}번 → 이미 뽑힌 번호! 다시 굴려요`;
    } else {
      st = 'ok';
      drawn.push(num);
      $('status').className = 'status ok';
      $('status').textContent = `✅ ${String(num).padStart(3,'0')}번 채택! (${drawn.length}/${TARGET})`;
    }
    history.push({n:num, st});
    renderHistory();
    rolling = false;
    if(drawn.length >= TARGET){
      $('btnRoll').disabled = true;
      $('btnAuto').disabled = true;
      showFinalSample();
    } else {
      $('btnRoll').disabled = false;
    }
  }, 700);
}

function autoRoll(){
  if(rolling || drawn.length >= TARGET) return;
  rollOnce();
  const t = setInterval(()=>{
    if(drawn.length >= TARGET){
      clearInterval(t);
      return;
    }
    if(!rolling) rollOnce();
  }, 850);
}

function renderHistory(){
  $('okCnt').textContent = drawn.length;
  $('totCnt').textContent = history.length;
  $('histGrid').innerHTML = history.map(h => {
    const cls = h.st === 'ok' ? 'ok' : (h.st === 'dup' ? 'dup' : 'over');
    return `<div class="hist-item ${cls}">${String(h.n).padStart(3,'0')}</div>`;
  }).join('');
}

function showFinalSample(){
  $('sampleResult').classList.add('on');
  $('srList').innerHTML = drawn.map(n =>
    `<div class="sr-num">${String(n).padStart(3,'0')}</div>`
  ).join('');
}

function reset(){
  drawn = [];
  history = [];
  rolling = false;
  $('num1').textContent = '?';
  $('num2').textContent = '?';
  $('num3').textContent = '?';
  $('combined').textContent = '___';
  $('status').className = 'status idle';
  $('status').textContent = '주사위를 굴려보세요!';
  $('btnRoll').disabled = false;
  $('btnAuto').disabled = false;
  $('sampleResult').classList.remove('on');
  renderHistory();
}

$('btnRoll').onclick = rollOnce;
$('btnAuto').onclick = autoRoll;
$('btnReset').onclick = reset;
reset();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: 난수표 (Random Number Table — digit-stream reading)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB3 = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
  color:#e2e8f0;padding:18px 14px;min-height:100vh;
}
.hdr{
  text-align:center;background:linear-gradient(135deg,rgba(34,211,238,.18),rgba(59,130,246,.12));
  border:2px solid rgba(34,211,238,.4);border-radius:18px;padding:16px 20px;margin-bottom:14px;
}
.hdr h1{font-size:1.5rem;font-weight:900;color:#a5f3fc;margin-bottom:6px}
.hdr p{font-size:1rem;color:#cbd5e1;line-height:1.6}

.problem-box{
  background:rgba(15,23,42,.6);border:2px solid rgba(34,211,238,.35);
  border-radius:14px;padding:14px 18px;margin-bottom:14px;text-align:center;
  font-size:1.1rem;font-weight:800;color:#fef3c7;line-height:1.7;
}
.problem-box .hi{color:#22d3ee;font-size:1.25rem}

.guide{
  background:rgba(99,102,241,.1);border-left:5px solid #6366f1;
  border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:14px;
  font-size:1rem;color:#c7d2fe;line-height:1.8;
}
.guide b{color:#fef3c7}
.example{
  background:rgba(15,23,42,.5);border:1.5px solid rgba(251,191,36,.3);
  border-radius:10px;padding:10px 14px;margin-top:8px;
  font-size:.95rem;color:#fde68a;line-height:1.8;
}
.example .demo{
  display:inline-block;font-family:'Courier New',monospace;font-weight:900;
  background:#fff;color:#1e293b;padding:3px 10px;border-radius:6px;margin:0 4px;letter-spacing:3px;
}
.example .demo .pick{background:#fef08a;color:#92400e;padding:2px 4px;border-radius:3px;box-shadow:0 0 0 2px #ca8a04}
.example .demo .nx{background:#86efac;color:#065f46;padding:2px 4px;border-radius:3px}
.example .demo .nx2{background:#bfdbfe;color:#1e3a8a;padding:2px 4px;border-radius:3px}

.controls{
  display:flex;gap:12px;justify-content:center;flex-wrap:wrap;
  margin-bottom:12px;
}
.dir-btn{
  font-size:1rem;font-weight:900;padding:9px 18px;
  border:2px solid rgba(34,211,238,.4);border-radius:10px;cursor:pointer;
  background:rgba(34,211,238,.08);color:#a5f3fc;transition:all .2s;
}
.dir-btn.active{background:rgba(34,211,238,.3);border-color:#22d3ee;color:#fff;box-shadow:0 0 18px rgba(34,211,238,.4)}
.dir-btn:hover{transform:translateY(-2px)}
.dir-btn:disabled{opacity:.55;cursor:not-allowed}

.stage{
  display:grid;grid-template-columns:1.4fr 1fr;gap:14px;
}
@media(max-width:780px){.stage{grid-template-columns:1fr}}

.table-wrap{
  background:rgba(248,250,252,.95);color:#0f172a;
  border-radius:14px;padding:14px 10px;
  box-shadow:0 6px 22px rgba(0,0,0,.35);
  border:3px solid rgba(99,102,241,.4);
  position:relative;overflow:auto;
}
.table-wrap::before{
  content:'난 수 표';position:absolute;top:6px;right:14px;
  font-size:.85rem;font-weight:800;color:#64748b;letter-spacing:.15em;
}
table.rt{border-collapse:separate;border-spacing:8px 6px;margin:18px auto 4px;font-family:'Courier New',monospace}
table.rt td{
  padding:0;background:transparent;
}
.cellbox{
  display:inline-flex;gap:2px;background:rgba(99,102,241,.06);
  border-radius:6px;padding:3px;
}
.digit{
  display:inline-block;width:30px;padding:6px 0;
  text-align:center;font-size:1.3rem;font-weight:900;color:#1e293b;
  cursor:pointer;border-radius:4px;transition:all .15s;
  user-select:none;
}
.digit:hover{background:rgba(99,102,241,.18);transform:scale(1.13)}
.digit.start{background:#fef08a !important;box-shadow:0 0 0 3px #ca8a04;color:#92400e !important}
.digit.ok{background:#86efac;color:#065f46}
.digit.dup{background:#fde68a;color:#92400e;opacity:.75}
.digit.over{background:#fca5a5;color:#7f1d1d;opacity:.75}

.side{display:flex;flex-direction:column;gap:12px}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.btn{
  font-size:1.05rem;font-weight:900;padding:11px 20px;border:none;
  border-radius:12px;cursor:pointer;transition:all .2s;
}
.btn-pri{
  background:linear-gradient(135deg,#22d3ee,#3b82f6);color:#fff;
  box-shadow:0 4px 14px rgba(34,211,238,.4);
}
.btn-pri:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 7px 20px rgba(34,211,238,.6)}
.btn-pri:disabled{opacity:.4;cursor:default;transform:none;box-shadow:none}
.btn-sec{
  background:rgba(99,102,241,.18);color:#a5b4fc;border:2px solid rgba(99,102,241,.4);
}
.btn-sec:hover{background:rgba(99,102,241,.32);transform:translateY(-2px)}

.status{
  font-size:1rem;font-weight:800;padding:11px 14px;border-radius:12px;
  background:rgba(30,41,59,.65);border:1.5px solid rgba(99,102,241,.35);
  color:#e2e8f0;text-align:center;min-height:50px;
}
.status.ok{background:rgba(34,197,94,.18);color:#86efac;border-color:#22c55e}
.status.bad{background:rgba(239,68,68,.16);color:#fca5a5;border-color:#ef4444}

.result-zone{
  background:rgba(15,23,42,.55);border:2px solid rgba(34,197,94,.35);
  border-radius:14px;padding:14px;
}
.rz-title{font-size:1.05rem;font-weight:900;color:#86efac;margin-bottom:10px;text-align:center}
.rz-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(70px,1fr));gap:8px}
.rz-card{
  background:rgba(34,197,94,.15);border:2px solid #22c55e;border-radius:10px;
  padding:9px 4px;text-align:center;font-family:'Courier New',monospace;
  font-size:1.3rem;font-weight:900;color:#fef3c7;
  animation:popRes .4s ease;
}
@keyframes popRes{from{opacity:0;transform:scale(.5)}to{opacity:1;transform:scale(1)}}
.rz-empty{text-align:center;color:#64748b;font-size:.95rem;padding:20px 8px}

.done{
  margin-top:10px;padding:12px;background:rgba(34,197,94,.2);
  border:2px solid #22c55e;border-radius:12px;text-align:center;
  font-size:1.05rem;font-weight:900;color:#86efac;display:none;
}
.done.on{display:block;animation:popRes .4s ease}
</style>
</head>
<body>
<div class="hdr">
  <h1>📋 난수표로 임의추출하기</h1>
  <p>0~9 한 자리 숫자가 가득한 난수표에서 <b>한 자리씩 두 개를 묶어</b> 두 자리 수를 만들어요!</p>
</div>

<div class="problem-box">
  📌 <span class="hi">50명</span>의 학생 중에서 <span class="hi">5명</span>을 임의추출하기<br>
  <span style="font-size:.95rem;color:#cbd5e1;font-weight:600">→ 01~50 범위만 채택 · 중복은 제외 · 51 이상·00은 건너뛰기</span>
</div>

<div class="guide">
  💡 <b>사용법</b><br>
  ① 방향(➡️ 가로 또는 ⬇️ 세로)을 먼저 선택<br>
  ② 표에서 <b>시작 숫자(어떤 칸의 십의자리 또는 일의자리)</b>를 클릭<br>
  ③ 그 숫자부터 정해진 방향으로 <b>두 자리씩 묶어</b> 표본 5명을 모아요
  <div class="example">
    예) 가로 방향에서
    <span class="demo">2<span class="pick">9</span><span class="nx">&nbsp;3</span>5&nbsp;<span class="nx2">40</span></span>
    의 <b>9</b>를 클릭하면 → 첫 수 <b style="color:#22c55e">93</b>, 다음 수 <b style="color:#3b82f6">54</b>, …
  </div>
</div>

<div class="controls">
  <button class="dir-btn active" id="dirH" data-dir="h">➡️ 가로 방향</button>
  <button class="dir-btn" id="dirV" data-dir="v">⬇️ 세로 방향</button>
</div>

<div class="stage">
  <div class="table-wrap">
    <table class="rt" id="rtable"></table>
  </div>

  <div class="side">
    <div class="status" id="status">시작 숫자를 클릭하세요!</div>
    <div class="btn-row">
      <button class="btn btn-pri" id="btnNext" disabled>▶️ 다음 수 읽기</button>
      <button class="btn btn-sec" id="btnAuto" disabled>⚡ 자동 진행</button>
      <button class="btn btn-sec" id="btnReset">🔄 다시 시작</button>
    </div>

    <div class="result-zone">
      <div class="rz-title">🏆 뽑힌 번호 (<span id="okN">0</span>/5)</div>
      <div class="rz-grid" id="rzGrid">
        <div class="rz-empty">아직 뽑힌 번호가 없어요</div>
      </div>
      <div class="done" id="doneMsg">🎉 5명 표본 추출 완료!</div>
    </div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);
const POPULATION = 50;
const TARGET = 5;

/* 6행 × 8칸(=16개 한자리 디지트/행) — 총 96개 디지트 */
const ROWS = 6;
const COLS_CELLS = 8;
const DCOLS = COLS_CELLS * 2;   // digit columns per row

let grid = [];          // grid[r][dc] = 0~9 digit
let direction = 'h';
let sequence = [];      // 디지트 진행 순서 [{r, dc}]
let startIdx = -1;
let readPos = -1;
let drawn = [];
let visited = [];
let auto = null;

function genGrid(){
  grid = [];
  for(let r=0; r<ROWS; r++){
    const row = [];
    for(let dc=0; dc<DCOLS; dc++){
      row.push(Math.floor(Math.random()*10));
    }
    grid.push(row);
  }
}

function buildSequence(){
  sequence = [];
  if(direction === 'h'){
    for(let r=0; r<ROWS; r++){
      for(let dc=0; dc<DCOLS; dc++){
        sequence.push({r, dc});
      }
    }
  } else {
    for(let dc=0; dc<DCOLS; dc++){
      for(let r=0; r<ROWS; r++){
        sequence.push({r, dc});
      }
    }
  }
}

function renderTable(){
  let html = '';
  for(let r=0; r<ROWS; r++){
    html += '<tr>';
    for(let cc=0; cc<COLS_CELLS; cc++){
      const dc1 = cc*2, dc2 = cc*2+1;
      html += `<td><span class="cellbox">
        <span class="digit" id="d_${r}_${dc1}" data-r="${r}" data-dc="${dc1}">${grid[r][dc1]}</span>
        <span class="digit" id="d_${r}_${dc2}" data-r="${r}" data-dc="${dc2}">${grid[r][dc2]}</span>
      </span></td>`;
    }
    html += '</tr>';
  }
  $('rtable').innerHTML = html;
  document.querySelectorAll('.digit').forEach(d => {
    d.onclick = () => {
      if(startIdx >= 0) return;
      const r = +d.dataset.r, dc = +d.dataset.dc;
      const idx = sequence.findIndex(s => s.r === r && s.dc === dc);
      if(idx < 0) return;
      pickStart(idx);
    };
  });
}

function pickStart(idx){
  startIdx = idx;
  readPos = idx;
  const s = sequence[idx];
  $(`d_${s.r}_${s.dc}`).classList.add('start');
  $('btnNext').disabled = false;
  $('btnAuto').disabled = false;
  // 방향 변경 잠금 (시작점부터의 흐름이 깨지지 않도록)
  document.querySelectorAll('.dir-btn').forEach(b => b.disabled = true);
  $('status').textContent = `🎯 시작점: 행 ${s.r+1}의 디지트 "${grid[s.r][s.dc]}"에서 출발 — "다음 수 읽기" 버튼을 누르세요`;
}

function readNextPair(){
  if(drawn.length >= TARGET) return;
  if(readPos < 0) return;
  if(readPos + 1 >= sequence.length){
    $('status').className = 'status bad';
    $('status').textContent = '⚠️ 표 끝까지 도달했어요. 다시 시작하거나 시작점을 바꿔보세요.';
    $('btnNext').disabled = true;
    $('btnAuto').disabled = true;
    if(auto){clearInterval(auto); auto = null; $('btnAuto').textContent = '⚡ 자동 진행';}
    return;
  }
  const a = sequence[readPos];
  const b = sequence[readPos+1];
  const num = grid[a.r][a.dc] * 10 + grid[b.r][b.dc];

  let st;
  if(num >= 1 && num <= POPULATION){
    if(drawn.includes(num)){
      st = 'dup';
    } else {
      st = 'ok';
      drawn.push(num);
    }
  } else {
    st = 'over';
  }

  // 색칠: 시작 강조는 첫 쌍에서만 의미가 있으므로 첫 디지트의 'start'를 제거 후 상태 색을 적용
  $(`d_${a.r}_${a.dc}`).classList.remove('start');
  $(`d_${a.r}_${a.dc}`).classList.add(st);
  $(`d_${b.r}_${b.dc}`).classList.add(st);
  visited.push({a, b, num, st});
  readPos += 2;

  const stEl = $('status');
  const ns = String(num).padStart(2,'0');
  if(st === 'ok'){
    stEl.className = 'status ok';
    stEl.textContent = `✅ ${ns}번 채택! (${drawn.length}/${TARGET})`;
  } else if(st === 'dup'){
    stEl.className = 'status bad';
    stEl.textContent = `⚠️ ${ns}번 → 이미 뽑힌 번호! 다음으로`;
  } else {
    stEl.className = 'status bad';
    stEl.textContent = `❌ ${ns}번 → 1~50 범위 밖! 다음으로`;
  }
  renderResults();

  if(drawn.length >= TARGET){
    $('btnNext').disabled = true;
    $('btnAuto').disabled = true;
    $('doneMsg').classList.add('on');
    if(auto){clearInterval(auto); auto = null; $('btnAuto').textContent = '⚡ 자동 진행';}
  }
}

function renderResults(){
  $('okN').textContent = drawn.length;
  const g = $('rzGrid');
  if(drawn.length === 0){
    g.innerHTML = '<div class="rz-empty">아직 뽑힌 번호가 없어요</div>';
    return;
  }
  g.innerHTML = drawn.map(n =>
    `<div class="rz-card">${String(n).padStart(2,'0')}</div>`
  ).join('');
}

function reset(regen){
  if(auto){clearInterval(auto); auto = null;}
  if(regen) genGrid();
  buildSequence();
  renderTable();
  startIdx = -1; readPos = -1;
  drawn = []; visited = [];
  $('btnNext').disabled = true;
  $('btnAuto').disabled = true;
  $('btnAuto').textContent = '⚡ 자동 진행';
  $('status').className = 'status';
  $('status').textContent = '시작 숫자를 클릭하세요!';
  $('doneMsg').classList.remove('on');
  document.querySelectorAll('.dir-btn').forEach(b => b.disabled = false);
  renderResults();
}

document.querySelectorAll('.dir-btn').forEach(b => {
  b.onclick = () => {
    if(b.disabled) return;
    document.querySelectorAll('.dir-btn').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    direction = b.dataset.dir;
    buildSequence();
  };
});

$('btnNext').onclick = readNextPair;
$('btnAuto').onclick = () => {
  if(auto){clearInterval(auto); auto = null; $('btnAuto').textContent = '⚡ 자동 진행'; return;}
  $('btnAuto').textContent = '⏸ 멈춤';
  auto = setInterval(readNextPair, 650);
};
$('btnReset').onclick = () => reset(true);

genGrid();
reset(false);
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: 엑셀 시뮬레이터 (Excel-like simulator with =RANDBETWEEN)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB4 = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
  color:#e2e8f0;padding:16px 12px;min-height:100vh;
}
.hdr{
  text-align:center;background:linear-gradient(135deg,rgba(16,185,129,.18),rgba(34,211,238,.12));
  border:2px solid rgba(16,185,129,.4);border-radius:18px;padding:14px 20px;margin-bottom:12px;
}
.hdr h1{font-size:1.45rem;font-weight:900;color:#a7f3d0;margin-bottom:5px}
.hdr p{font-size:.98rem;color:#cbd5e1;line-height:1.6}

.problem-box{
  background:rgba(15,23,42,.6);border:2px solid rgba(16,185,129,.35);
  border-radius:12px;padding:12px 16px;margin-bottom:12px;text-align:center;
  font-size:1.05rem;font-weight:800;color:#fef3c7;line-height:1.7;
}
.problem-box .hi{color:#10b981;font-size:1.2rem}

.guide{
  background:rgba(16,185,129,.08);border-left:5px solid #10b981;
  border-radius:0 10px 10px 0;padding:11px 14px;margin-bottom:12px;
  font-size:.95rem;color:#a7f3d0;line-height:1.8;
}
.guide b{color:#fef3c7}
.guide .step{
  display:inline-block;background:#10b981;color:#0f172a;font-weight:900;
  padding:1px 9px;border-radius:50%;margin-right:5px;font-size:.85rem;
}

/* ============ EXCEL UI ============ */
.excel{
  background:#fff;border-radius:8px;overflow:hidden;
  box-shadow:0 8px 28px rgba(0,0,0,.4);
  border:1px solid #b3b3b3;
  margin-bottom:14px;
}
.ribbon{
  background:#217346;color:#fff;padding:8px 14px;
  font-size:.95rem;font-weight:700;display:flex;align-items:center;gap:14px;
}
.ribbon::before{content:'📊';font-size:1.2rem}
.ribbon-tabs{display:flex;gap:0;font-size:.85rem;font-weight:600;margin-left:auto}
.ribbon-tab{padding:5px 12px;background:rgba(255,255,255,.15);border-radius:3px 3px 0 0}
.ribbon-tab.active{background:#fff;color:#217346}

.formula-bar{
  display:flex;align-items:center;gap:6px;background:#fff;
  padding:5px 10px;border-bottom:1px solid #d4d4d4;
}
.cell-ref{
  font-family:'Calibri','Segoe UI',sans-serif;font-size:.95rem;font-weight:600;
  background:#f3f3f3;border:1px solid #b3b3b3;border-radius:3px;
  padding:4px 10px;min-width:62px;text-align:center;color:#000;
}
.fx{font-family:'Cambria Math',serif;font-style:italic;color:#666;font-size:1.05rem;margin:0 4px}
.formula-input{
  flex:1;font-family:'Calibri','Segoe UI',sans-serif;font-size:1rem;
  border:1px solid #d4d4d4;padding:5px 8px;color:#000;outline:none;
  background:#fff;
}
.formula-input:focus{border-color:#217346;box-shadow:0 0 0 1px #217346}

.sheet-wrap{
  overflow:auto;max-height:420px;background:#fff;
}
table.sheet{
  border-collapse:collapse;font-family:'Calibri','Segoe UI',sans-serif;
  font-size:.95rem;color:#000;background:#fff;
}
table.sheet th, table.sheet td{
  border:1px solid #d4d4d4;min-width:78px;max-width:120px;height:24px;
  text-align:center;padding:2px 5px;background:#fff;
}
table.sheet th{
  background:#f3f3f3;font-weight:600;color:#444;
  position:sticky;top:0;z-index:2;
}
table.sheet th.rowh{position:sticky;left:0;z-index:1;min-width:38px;width:38px}
table.sheet td.rowh{
  background:#f3f3f3;font-weight:600;color:#444;
  position:sticky;left:0;z-index:1;min-width:38px;width:38px;
}
table.sheet td{cursor:cell;text-align:right;padding-right:6px;font-variant-numeric:tabular-nums}
table.sheet td.sel{
  background:#fff !important;border:2px solid #217346 !important;
  box-shadow:inset 0 0 0 1px #217346;
}
table.sheet td.sel-range{
  background:rgba(33,115,70,.12) !important;border:1px solid #217346 !important;
}
table.sheet td.fill-handle::after{
  content:'';position:absolute;
}
.sel-wrapper{position:relative}
.fill-mark{
  position:absolute;width:8px;height:8px;background:#217346;
  border:1.5px solid #fff;cursor:crosshair;z-index:3;
  bottom:-4px;right:-4px;
}

/* status footer */
.foot{
  background:#f3f3f3;border-top:1px solid #d4d4d4;padding:5px 12px;
  font-size:.82rem;color:#555;display:flex;justify-content:space-between;
}
.foot .ok{color:#217346;font-weight:700}

/* ============ HINT BUTTONS ============ */
.action-row{
  display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:12px;
}
.btn{
  font-size:1rem;font-weight:900;padding:10px 18px;border:none;
  border-radius:10px;cursor:pointer;transition:all .2s;
}
.btn-pri{
  background:linear-gradient(135deg,#10b981,#22d3ee);color:#fff;
  box-shadow:0 4px 14px rgba(16,185,129,.4);
}
.btn-pri:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 7px 20px rgba(16,185,129,.6)}
.btn-pri:disabled{opacity:.4;cursor:default;transform:none;box-shadow:none}
.btn-sec{
  background:rgba(99,102,241,.18);color:#a5b4fc;border:2px solid rgba(99,102,241,.4);
}
.btn-sec:hover{background:rgba(99,102,241,.32);transform:translateY(-2px)}
.btn-warn{
  background:rgba(251,191,36,.18);color:#fbbf24;border:2px solid rgba(251,191,36,.4);
}
.btn-warn:hover{background:rgba(251,191,36,.32);transform:translateY(-2px)}

.result-zone{
  background:rgba(15,23,42,.55);border:2px solid rgba(16,185,129,.35);
  border-radius:14px;padding:13px;
}
.rz-title{font-size:1.05rem;font-weight:900;color:#a7f3d0;margin-bottom:10px;text-align:center}
.rz-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(72px,1fr));gap:8px}
.rz-card{
  background:rgba(16,185,129,.15);border:2px solid #10b981;border-radius:10px;
  padding:9px 4px;text-align:center;font-family:'Courier New',monospace;
  font-size:1.25rem;font-weight:900;color:#fef3c7;
  animation:popRes .4s ease;
}
@keyframes popRes{from{opacity:0;transform:scale(.5)}to{opacity:1;transform:scale(1)}}
.rz-empty{text-align:center;color:#64748b;font-size:.92rem;padding:18px 6px}

.toast{
  position:fixed;bottom:24px;left:50%;transform:translateX(-50%);
  background:rgba(15,23,42,.95);color:#fef3c7;
  padding:12px 20px;border-radius:12px;
  border:2px solid #fbbf24;font-weight:800;font-size:1rem;
  box-shadow:0 8px 24px rgba(0,0,0,.45);
  z-index:999;display:none;animation:slideUp .35s ease;
}
.toast.on{display:block}
@keyframes slideUp{from{opacity:0;transform:translate(-50%,12px)}to{opacity:1;transform:translate(-50%,0)}}
</style>
</head>
<body>
<div class="hdr">
  <h1>💻 컴퓨터 프로그램(엑셀)로 임의추출하기</h1>
  <p>실제 엑셀과 비슷한 화면에서 <b>=RANDBETWEEN(1, N)</b> 함수로 무작위 번호를 뽑아 봐요!</p>
</div>

<div class="problem-box">
  📌 어느 전시회에 입장한 <span class="hi">500명</span>의 관객 중에서 <span class="hi">10명</span>을 임의추출하기
</div>

<div class="guide">
  <span class="step">1</span> 셀 <b>A1</b>을 클릭한다.<br>
  <span class="step">2</span> 수식 입력줄에 <b>=RANDBETWEEN(1,500)</b> 을 입력하고 Enter (또는 <b>"수식 입력"</b> 버튼)<br>
  <span class="step">3</span> 셀 오른쪽 아래의 <b style="color:#10b981">초록 점(자동 채우기 핸들)</b>을 드래그하거나 <b>"자동 채우기"</b> 버튼으로 A10까지 채워요
</div>

<div class="action-row">
  <button class="btn btn-pri" id="btnFormula">📝 A1에 수식 입력</button>
  <button class="btn btn-warn" id="btnFill">⬇️ A10까지 자동 채우기</button>
  <button class="btn btn-sec" id="btnRecalc">🔄 F9 (재계산)</button>
  <button class="btn btn-sec" id="btnReset">🗑️ 새 워크시트</button>
</div>

<div class="excel">
  <div class="ribbon">
    Microsoft Excel - 임의추출.xlsx
    <div class="ribbon-tabs">
      <div class="ribbon-tab active">홈</div>
      <div class="ribbon-tab">삽입</div>
      <div class="ribbon-tab">수식</div>
    </div>
  </div>
  <div class="formula-bar">
    <div class="cell-ref" id="cellRef">A1</div>
    <span class="fx">𝑓𝑥</span>
    <input class="formula-input" id="formulaInput" type="text"
           placeholder="셀을 선택하고 수식을 입력하세요" />
  </div>
  <div class="sheet-wrap">
    <table class="sheet" id="sheet"></table>
  </div>
  <div class="foot">
    <span>준비</span>
    <span class="ok" id="footStatus">평균: — &nbsp;|&nbsp; 개수: <span id="footCnt">0</span> &nbsp;|&nbsp; 합계: <span id="footSum">0</span></span>
  </div>
</div>

<div class="result-zone">
  <div class="rz-title">🏆 추출된 표본 (셀 A1 ~ A10)</div>
  <div class="rz-grid" id="rzGrid">
    <div class="rz-empty">아직 데이터가 없어요. 위에서 수식을 입력해 보세요!</div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const $ = id => document.getElementById(id);
const COLS = ['A','B','C','D','E'];
const ROWS = 15;
const TARGET = 10;
const POPULATION = 500;

let cells = {};        // {'A1': {value: 484, formula: '=RANDBETWEEN(1,500)'}}
let selected = 'A1';

function buildSheet(){
  let html = '<thead><tr><th class="rowh"></th>';
  COLS.forEach(c => html += `<th>${c}</th>`);
  html += '</tr></thead><tbody>';
  for(let r=1; r<=ROWS; r++){
    html += `<tr><td class="rowh">${r}</td>`;
    COLS.forEach(c => {
      const k = c+r;
      html += `<td id="cell-${k}" data-cell="${k}"></td>`;
    });
    html += '</tr>';
  }
  html += '</tbody>';
  $('sheet').innerHTML = html;
  $('sheet').querySelectorAll('td[data-cell]').forEach(td => {
    td.onclick = () => selectCell(td.dataset.cell);
  });
}

function selectCell(k){
  selected = k;
  $('cellRef').textContent = k;
  document.querySelectorAll('td.sel').forEach(t => t.classList.remove('sel'));
  const td = $('cell-'+k);
  if(td) td.classList.add('sel');
  // show formula or value in input
  const c = cells[k];
  $('formulaInput').value = c ? (c.formula || c.value) : '';
}

function setCell(k, val, formula){
  cells[k] = {value: val, formula: formula || ''};
  $('cell-'+k).textContent = val;
}

function clearCell(k){
  delete cells[k];
  $('cell-'+k).textContent = '';
}

function recalcAll(){
  Object.keys(cells).forEach(k => {
    const c = cells[k];
    if(c.formula && c.formula.toUpperCase().startsWith('=RANDBETWEEN')){
      const m = c.formula.match(/=RANDBETWEEN\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)/i);
      if(m){
        const lo = parseInt(m[1]), hi = parseInt(m[2]);
        const v = Math.floor(Math.random() * (hi-lo+1)) + lo;
        c.value = v;
        $('cell-'+k).textContent = v;
      }
    }
  });
  updateFoot();
  updateResults();
}

function evalFormulaInput(){
  const f = $('formulaInput').value.trim();
  if(!f){clearCell(selected); return;}
  if(f.toUpperCase().startsWith('=RANDBETWEEN')){
    const m = f.match(/=RANDBETWEEN\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)/i);
    if(m){
      const lo = parseInt(m[1]), hi = parseInt(m[2]);
      const v = Math.floor(Math.random() * (hi-lo+1)) + lo;
      setCell(selected, v, f);
      showToast(`✅ ${selected}에 수식 입력! 결과: ${v}`);
      updateFoot();
      updateResults();
      return;
    }
  }
  // plain number
  if(!isNaN(+f)){
    setCell(selected, +f, '');
    updateFoot();
    updateResults();
  } else {
    showToast(`⚠️ 수식 형식을 확인해 주세요: =RANDBETWEEN(1,500)`);
  }
}

function fillDown(){
  const c = cells[selected];
  if(!c || !c.formula){
    showToast('⚠️ 먼저 A1에 수식을 입력해 주세요!');
    return;
  }
  // animate fill A2 ~ A10
  const m = /^([A-E])(\d+)$/.exec(selected);
  if(!m){return;}
  const col = m[1];
  const startRow = parseInt(m[2]);
  let i = startRow + 1;
  const endRow = startRow + (TARGET - 1);
  const ti = setInterval(()=>{
    if(i > endRow){
      clearInterval(ti);
      showToast(`✅ ${col}${startRow}~${col}${endRow}까지 자동 채우기 완료!`);
      return;
    }
    const cellKey = col+i;
    const m2 = c.formula.match(/=RANDBETWEEN\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)/i);
    const lo = parseInt(m2[1]), hi = parseInt(m2[2]);
    const v = Math.floor(Math.random() * (hi-lo+1)) + lo;
    setCell(cellKey, v, c.formula);
    $('cell-'+cellKey).style.animation = 'none';
    void $('cell-'+cellKey).offsetWidth;
    $('cell-'+cellKey).style.animation = 'highlight .4s ease';
    updateFoot();
    updateResults();
    i++;
  }, 200);
}

function updateFoot(){
  // show summary of A1:A10
  const vals = [];
  for(let r=1; r<=TARGET; r++){
    const c = cells['A'+r];
    if(c && typeof c.value === 'number') vals.push(c.value);
  }
  $('footCnt').textContent = vals.length;
  const sum = vals.reduce((a,b)=>a+b, 0);
  $('footSum').textContent = sum;
  if(vals.length){
    $('footStatus').innerHTML = `평균: ${(sum/vals.length).toFixed(1)} &nbsp;|&nbsp; 개수: <span id="footCnt">${vals.length}</span> &nbsp;|&nbsp; 합계: <span id="footSum">${sum}</span>`;
  }
}

function updateResults(){
  const vals = [];
  for(let r=1; r<=TARGET; r++){
    const c = cells['A'+r];
    if(c && typeof c.value === 'number') vals.push(c.value);
  }
  const g = $('rzGrid');
  if(vals.length === 0){
    g.innerHTML = '<div class="rz-empty">아직 데이터가 없어요. 위에서 수식을 입력해 보세요!</div>';
    return;
  }
  g.innerHTML = vals.map(v =>
    `<div class="rz-card">${v}</div>`
  ).join('');
}

function showToast(msg){
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('on');
  clearTimeout(window._toastT);
  window._toastT = setTimeout(()=>t.classList.remove('on'), 2400);
}

// keyboard handling
$('formulaInput').addEventListener('keydown', e => {
  if(e.key === 'Enter'){
    e.preventDefault();
    evalFormulaInput();
  }
});

$('btnFormula').onclick = () => {
  selectCell('A1');
  $('formulaInput').value = '=RANDBETWEEN(1,500)';
  $('formulaInput').focus();
  // simulate typing animation
  const text = '=RANDBETWEEN(1,500)';
  let i = 0;
  $('formulaInput').value = '';
  const ti = setInterval(()=>{
    if(i >= text.length){
      clearInterval(ti);
      setTimeout(evalFormulaInput, 220);
      return;
    }
    $('formulaInput').value += text[i];
    i++;
  }, 40);
};

$('btnFill').onclick = fillDown;
$('btnRecalc').onclick = () => {recalcAll(); showToast('🔄 모든 RANDBETWEEN 셀이 재계산됐어요!');};
$('btnReset').onclick = () => {
  cells = {};
  buildSheet();
  selectCell('A1');
  $('formulaInput').value = '';
  updateFoot();
  updateResults();
  showToast('🗑️ 새 워크시트로 초기화됐어요');
};

// inject highlight animation
const stl = document.createElement('style');
stl.textContent = '@keyframes highlight{0%{background:#fef08a !important}100%{background:#fff !important}}';
document.head.appendChild(stl);

buildSheet();
selectCell('A1');
updateFoot();
updateResults();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("🎲 임의추출 방법 시뮬레이션")
    st.caption(
        "표본을 임의추출(무작위추출)하는 4가지 대표적 방법 — "
        "**제비뽑기 · 난수주사위 · 난수표 · 컴퓨터 프로그램(엑셀)** — 을 직접 체험해 봐요!"
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🎟️ 제비뽑기",
        "🎲 난수주사위",
        "📋 난수표",
        "💻 엑셀로 추출",
    ])

    with tab1:
        components.html(_HTML_TAB1, height=820, scrolling=True)

    with tab2:
        components.html(_HTML_TAB2, height=1100, scrolling=True)

    with tab3:
        components.html(_HTML_TAB3, height=900, scrolling=True)

    with tab4:
        components.html(_HTML_TAB4, height=1300, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
