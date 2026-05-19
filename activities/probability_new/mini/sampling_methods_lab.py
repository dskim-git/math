# activities/probability_new/mini/sampling_methods_lab.py
"""
복원추출 · 비복원추출 · 동시추출 비교 실험실 — 세 가지 추출 방법으로
모집단에서 표본을 뽑아보고 가능한 표본의 수가 왜 달라지는지 직접 체험.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎁 복원·비복원·동시추출 실험실",
    "description": "모집단에서 표본을 복원추출·비복원추출·동시추출할 때 가능한 표본의 수가 어떻게 달라지는지 직접 뽑아보고 비교합니다.",
    "order": 11,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "복원비복원동시추출실험실"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 복원·비복원·동시추출 실험실**"},
    {
        "key": "복원비복원차이",
        "label": "복원추출과 비복원추출은 무엇이 다른가요? 직접 뽑아본 경험을 바탕으로 설명해 보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "예) 복원추출은 ___, 비복원추출은 ___. 따라서 ...",
    },
    {
        "key": "비복원동시차이",
        "label": "비복원추출과 동시추출에서 가능한 표본의 수가 다른 이유는 무엇일까요? (예: 5개 중 2개 뽑기 → 비복원 20가지 vs 동시 10가지)",
        "type": "text_area",
        "height": 110,
        "placeholder": "비복원추출에서는 순서를 ___ 하지만, 동시추출에서는 순서를 ___. 그래서...",
    },
    {
        "key": "크기비교",
        "label": "n개 중 r개를 뽑을 때 ₙΠᵣ, ₙPᵣ, ₙCᵣ 의 크기를 부등호로 비교하고, 그 이유를 설명해 보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "ₙΠᵣ ___ ₙPᵣ ___ ₙCᵣ. 왜냐하면 ___",
    },
    {
        "key": "일상예시",
        "label": "주변에서 복원추출/비복원추출/동시추출의 예시를 각각 하나씩 들어 보세요. (예: 주사위 굴리기, 카드 뽑기, 로또, 반장 뽑기 등)",
        "type": "text_area",
        "height": 110,
        "placeholder": "복원추출 — ...\n비복원추출 — ...\n동시추출 — ...",
    },
    {
        "key": "모집단큰경우",
        "label": "모집단의 크기가 충분히 크면 비복원추출도 복원추출처럼 간주할 수 있다고 하는 이유는 무엇일까요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) 모집단이 매우 크면 한 번 뽑은 원소가 다시 뽑힐 확률이 ...",
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
# TAB 1: 추출 시뮬레이션 (Interactive Sampling Simulator)
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
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#312e81 100%);
  color:#e2e8f0;padding:18px 14px;min-height:100vh;font-size:16px;line-height:1.55;
}
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(251,191,36,.18),rgba(244,114,182,.12));
  border:2px solid rgba(251,191,36,.4);border-radius:18px;
  padding:16px 20px;margin-bottom:14px;
}
.hdr h1{font-size:1.55rem;font-weight:900;color:#fde68a;margin-bottom:6px}
.hdr p{font-size:1.02rem;color:#cbd5e1;line-height:1.65}

/* === control bar === */
.controls{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
  gap:14px;margin-bottom:14px;
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.32);
  border-radius:14px;padding:14px 16px;
}
.ctrl-block{display:flex;flex-direction:column;gap:8px}
.ctrl-label{font-size:1rem;font-weight:800;color:#a5b4fc;display:flex;align-items:center;gap:6px}
.mode-btns{display:flex;gap:8px;flex-wrap:wrap}
.mode-btn{
  flex:1;min-width:90px;padding:10px 12px;border-radius:10px;
  border:2px solid rgba(148,163,184,.32);background:rgba(30,41,59,.6);
  color:#cbd5e1;font-size:1rem;font-weight:800;cursor:pointer;
  transition:all .18s ease;
}
.mode-btn:hover{transform:translateY(-1px);border-color:rgba(165,180,252,.55)}
.mode-btn.on{background:linear-gradient(135deg,#6366f1,#22d3ee);color:#fff;border-color:#fff;box-shadow:0 4px 14px rgba(99,102,241,.45)}
.mode-btn[data-mode="rep"].on{background:linear-gradient(135deg,#10b981,#22d3ee)}
.mode-btn[data-mode="perm"].on{background:linear-gradient(135deg,#f59e0b,#f97316)}
.mode-btn[data-mode="comb"].on{background:linear-gradient(135deg,#ec4899,#a855f7)}

.r-row{display:flex;gap:10px;align-items:center}
.r-btn{
  width:46px;height:46px;border-radius:10px;border:2px solid rgba(148,163,184,.32);
  background:rgba(30,41,59,.6);color:#cbd5e1;font-size:1.15rem;font-weight:900;cursor:pointer;
  transition:all .18s ease;
}
.r-btn:hover{transform:translateY(-1px);border-color:#fbbf24}
.r-btn.on{background:#fbbf24;color:#1f2937;border-color:#fff;box-shadow:0 4px 12px rgba(251,191,36,.5)}

.btn-row{display:flex;gap:10px;flex-wrap:wrap}
.action-btn{
  flex:1;min-width:120px;padding:12px;border-radius:11px;border:none;cursor:pointer;
  font-size:1.02rem;font-weight:900;color:#fff;transition:all .2s ease;
  box-shadow:0 4px 12px rgba(0,0,0,.3);
}
.btn-draw{background:linear-gradient(135deg,#22c55e,#16a34a)}
.btn-all{background:linear-gradient(135deg,#6366f1,#4f46e5)}
.btn-reset{background:linear-gradient(135deg,#64748b,#475569)}
.action-btn:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.4)}
.action-btn:disabled{opacity:.42;cursor:not-allowed}

/* === mode info banner === */
.mode-info{
  background:rgba(15,23,42,.65);border-left:4px solid #fbbf24;
  border-radius:8px;padding:10px 14px;margin-bottom:14px;font-size:1rem;color:#fde68a;
}
.mode-info b{color:#fff}

/* === stage === */
.stage{
  background:rgba(15,23,42,.55);border:2px solid rgba(99,102,241,.3);
  border-radius:16px;padding:18px 16px;margin-bottom:14px;min-height:330px;
  position:relative;overflow:hidden;
}

.stage-row{display:grid;grid-template-columns:1fr auto 1fr;gap:14px;align-items:center}

.pop-box{
  position:relative;border:3px solid #fbbf24;border-radius:14px;
  padding:18px 14px 14px;background:rgba(0,0,0,.4);min-height:260px;
}
.pop-label{
  position:absolute;top:-13px;left:50%;transform:translateX(-50%);
  background:#1e1b4b;padding:2px 14px;font-size:1.05rem;font-weight:900;color:#fbbf24;
  letter-spacing:.5px;border-radius:6px;
}
.balls{
  display:flex;flex-wrap:wrap;justify-content:center;align-items:center;
  gap:10px;padding:14px 4px;min-height:200px;
}
.ball{
  width:62px;height:62px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:1.7rem;font-weight:900;color:#fff;
  box-shadow:0 6px 14px rgba(0,0,0,.45),inset 2px 4px 0 rgba(255,255,255,.35);
  cursor:default;user-select:none;
  transition:transform .25s ease,opacity .25s ease;
}
.ball.b1{background:radial-gradient(circle at 30% 28%,#fca5a5,#dc2626)}
.ball.b2{background:radial-gradient(circle at 30% 28%,#fcd34d,#d97706)}
.ball.b3{background:radial-gradient(circle at 30% 28%,#86efac,#16a34a)}
.ball.b4{background:radial-gradient(circle at 30% 28%,#7dd3fc,#0284c7)}
.ball.b5{background:radial-gradient(circle at 30% 28%,#c4b5fd,#7c3aed)}
.ball.b6{background:radial-gradient(circle at 30% 28%,#f9a8d4,#db2777)}

.ball.gone{opacity:.18;filter:grayscale(.6)}
.ball.flying{
  position:absolute;z-index:50;pointer-events:none;
  transition:transform .9s cubic-bezier(.5,.05,.4,1.2),opacity .35s ease;
}

.arrow-zone{
  display:flex;flex-direction:column;align-items:center;gap:8px;color:#fde68a;
  font-size:1rem;font-weight:800;min-width:80px;
}
.arrow-ex{font-size:2rem;animation:arrowMove 1.6s ease-in-out infinite}
.arrow-back{font-size:2rem;color:#22d3ee;opacity:.7}
@keyframes arrowMove{0%,100%{transform:translateX(-5px)}50%{transform:translateX(5px)}}

.sample-box{
  border:3px dashed #22d3ee;border-radius:14px;
  padding:18px 14px 14px;background:rgba(0,0,0,.35);min-height:260px;position:relative;
}
.sample-label{
  position:absolute;top:-13px;left:50%;transform:translateX(-50%);
  background:#1e1b4b;padding:2px 14px;font-size:1.05rem;font-weight:900;color:#22d3ee;
  letter-spacing:.5px;border-radius:6px;
}
.sample-zone{
  display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:10px;
  padding:14px 4px;min-height:200px;
}
.sample-zone.empty::before{
  content:"여기에 뽑힌 공이 와요";color:#64748b;font-size:.95rem;font-style:italic;
}
.sample-zone.empty{align-items:center;justify-content:center}

.sample-zone .ball{position:relative}
.sample-zone .order-tag{
  position:absolute;top:-8px;right:-8px;width:22px;height:22px;
  background:#fbbf24;color:#1f2937;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:.78rem;font-weight:900;box-shadow:0 2px 6px rgba(0,0,0,.4);
}

/* === results === */
.result-bar{
  display:flex;gap:14px;flex-wrap:wrap;justify-content:space-between;align-items:center;
  background:rgba(15,23,42,.55);border:1.5px solid rgba(34,211,238,.32);
  border-radius:14px;padding:14px 18px;margin-bottom:14px;
}
.res-cell{display:flex;flex-direction:column;align-items:center;min-width:120px}
.res-num{font-size:2.2rem;font-weight:900;color:#fde68a;line-height:1.1}
.res-cap{font-size:.92rem;color:#94a3b8;margin-top:4px}
.res-formula{font-size:1.05rem;font-weight:800;color:#a5b4fc;margin-top:2px}

/* === found samples list === */
.found-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(168,85,247,.3);
  border-radius:14px;padding:14px 16px;
}
.found-hdr{font-size:1.08rem;font-weight:900;color:#c4b5fd;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}
.found-hdr .cnt{color:#fbbf24}
.found-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));
  gap:10px;max-height:280px;overflow-y:auto;padding-right:6px;
}
.found-grid::-webkit-scrollbar{width:8px}
.found-grid::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:4px}
.found-grid::-webkit-scrollbar-thumb{background:#475569;border-radius:4px}

.sample-card{
  background:rgba(0,0,0,.35);border:1.5px solid rgba(148,163,184,.25);
  border-radius:10px;padding:8px;display:flex;justify-content:center;
  align-items:center;gap:4px;min-height:56px;position:relative;
}
.sample-card.fresh{
  animation:freshPop .6s ease;
  border-color:#fbbf24;box-shadow:0 0 16px rgba(251,191,36,.4);
}
@keyframes freshPop{
  0%{transform:scale(.4);opacity:0}
  60%{transform:scale(1.1);opacity:1}
  100%{transform:scale(1)}
}
.mini-ball{
  width:34px;height:34px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:.95rem;font-weight:900;color:#fff;
  box-shadow:0 2px 5px rgba(0,0,0,.4),inset 1px 2px 0 rgba(255,255,255,.3);
}
.mini-ball.b1{background:radial-gradient(circle at 30% 28%,#fca5a5,#dc2626)}
.mini-ball.b2{background:radial-gradient(circle at 30% 28%,#fcd34d,#d97706)}
.mini-ball.b3{background:radial-gradient(circle at 30% 28%,#86efac,#16a34a)}
.mini-ball.b4{background:radial-gradient(circle at 30% 28%,#7dd3fc,#0284c7)}
.mini-ball.b5{background:radial-gradient(circle at 30% 28%,#c4b5fd,#7c3aed)}
.mini-ball.b6{background:radial-gradient(circle at 30% 28%,#f9a8d4,#db2777)}
.sep{color:#64748b;font-size:1.05rem;font-weight:900}
.brace{color:#fbbf24;font-size:1.4rem;font-weight:900}

.toast{
  position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);
  background:rgba(15,23,42,.96);color:#fde68a;border:2px solid #fbbf24;
  padding:12px 22px;border-radius:12px;font-size:1.02rem;font-weight:800;
  box-shadow:0 8px 26px rgba(0,0,0,.5);opacity:0;transition:all .35s ease;
  z-index:1000;pointer-events:none;
}
.toast.on{transform:translateX(-50%) translateY(0);opacity:1}

.empty-msg{text-align:center;color:#64748b;font-size:.95rem;font-style:italic;padding:18px}

@media(max-width:760px){
  .stage-row{grid-template-columns:1fr;gap:10px}
  .arrow-zone{flex-direction:row}
  .ball{width:52px;height:52px;font-size:1.45rem}
}
</style>
</head>
<body>

<div class="hdr">
  <h1>🎁 뽑아보면 달라지는 표본의 수!</h1>
  <p>모집단(5개의 공) 에서 표본을 직접 뽑아보고, 추출 방식에 따라 가능한 표본이 어떻게 달라지는지 살펴봐요</p>
</div>

<div class="controls">
  <div class="ctrl-block">
    <div class="ctrl-label">🔧 추출 방식</div>
    <div class="mode-btns">
      <button class="mode-btn on" data-mode="rep">복원추출</button>
      <button class="mode-btn" data-mode="perm">비복원추출</button>
      <button class="mode-btn" data-mode="comb">동시추출</button>
    </div>
  </div>
  <div class="ctrl-block">
    <div class="ctrl-label">🎯 뽑을 개수 r</div>
    <div class="r-row">
      <button class="r-btn" data-r="1">1</button>
      <button class="r-btn on" data-r="2">2</button>
      <button class="r-btn" data-r="3">3</button>
    </div>
  </div>
  <div class="ctrl-block">
    <div class="ctrl-label">▶️ 실행</div>
    <div class="btn-row">
      <button class="action-btn btn-draw" id="btnDraw">🎲 한 번 뽑기</button>
      <button class="action-btn btn-all" id="btnAll">🌐 모든 경우 보기</button>
      <button class="action-btn btn-reset" id="btnReset">🗑️ 초기화</button>
    </div>
  </div>
</div>

<div class="mode-info" id="modeInfo"></div>

<div class="stage">
  <div class="stage-row">
    <div class="pop-box">
      <div class="pop-label">모집단</div>
      <div class="balls" id="popBalls"></div>
    </div>
    <div class="arrow-zone" id="arrowZone">
      <div class="arrow-ex">➡️</div>
      <div>추출</div>
      <div class="arrow-back" id="arrowBack">⬅️</div>
    </div>
    <div class="sample-box">
      <div class="sample-label">추출된 표본</div>
      <div class="sample-zone empty" id="sampleZone"></div>
    </div>
  </div>
</div>

<div class="result-bar">
  <div class="res-cell">
    <div class="res-num" id="foundCount">0</div>
    <div class="res-cap">지금까지 발견한<br>서로 다른 표본</div>
  </div>
  <div class="res-cell">
    <div class="res-num" id="totalCount">25</div>
    <div class="res-cap">이론상 가능한<br>모든 표본의 수</div>
    <div class="res-formula" id="totalFormula">₅Π₂ = 5² = 25</div>
  </div>
  <div class="res-cell">
    <div class="res-num" id="drawCount">0</div>
    <div class="res-cap">총 뽑기 시도 횟수</div>
  </div>
</div>

<div class="found-wrap">
  <div class="found-hdr">
    <span>🗂️ 발견한 표본 목록</span>
    <span class="cnt"><span id="foundCount2">0</span> / <span id="totalCount2">25</span></span>
  </div>
  <div class="found-grid" id="foundGrid">
    <div class="empty-msg" style="grid-column:1/-1">아직 뽑은 표본이 없어요. <b>한 번 뽑기</b> 버튼을 눌러보세요!</div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const N = 5;
let r = 2;
let mode = 'rep'; // rep | perm | comb
let foundSet = new Set();
let drawCount = 0;
let isAnimating = false;

const $ = (id) => document.getElementById(id);
const popBalls = $('popBalls');
const sampleZone = $('sampleZone');
const stage = document.querySelector('.stage');
const arrowBack = $('arrowBack');

// === setup balls in 모집단 ===
function buildPop(){
  popBalls.innerHTML = '';
  for(let i=1;i<=N;i++){
    const el = document.createElement('div');
    el.className = `ball b${i}`;
    el.id = `pop-b${i}`;
    el.textContent = i;
    popBalls.appendChild(el);
  }
}
buildPop();

// === MODE info ===
const MODE_INFO = {
  rep:  '🟢 <b>복원추출</b> — 뽑은 공을 다시 모집단에 되돌려 놓은 후 다음 공을 뽑아요. <b>같은 공을 여러 번 뽑을 수 있어요!</b>',
  perm: '🟠 <b>비복원추출</b> — 뽑은 공을 되돌려 놓지 않고 다음 공을 뽑아요. <b>순서를 구분해요</b> (1→2와 2→1 은 다른 표본)',
  comb: '🟣 <b>동시추출</b> — 한 번에 r개를 동시에 뽑아요. <b>순서를 구분하지 않아요</b> ({1,2}와 {2,1}은 같은 표본)',
};
function updateModeInfo(){ $('modeInfo').innerHTML = MODE_INFO[mode]; }
updateModeInfo();

// === counts ===
function fact(n){let f=1;for(let i=2;i<=n;i++)f*=i;return f}
function nPr(n,r){let v=1;for(let i=0;i<r;i++)v*=(n-i);return v}
function nCr(n,r){return Math.round(nPr(n,r)/fact(r))}
function totalForMode(){
  if(mode==='rep') return Math.pow(N,r);
  if(mode==='perm') return nPr(N,r);
  return nCr(N,r);
}
function formulaStr(){
  const sub = (s)=>s.replace(/0/g,'₀').replace(/1/g,'₁').replace(/2/g,'₂').replace(/3/g,'₃')
                    .replace(/4/g,'₄').replace(/5/g,'₅').replace(/6/g,'₆').replace(/7/g,'₇')
                    .replace(/8/g,'₈').replace(/9/g,'₉');
  if(mode==='rep'){
    const exp = r===1?'':r===2?'²':'³';
    return `${sub(String(N))}Π${sub(String(r))} = ${N}${exp} = ${Math.pow(N,r)}`;
  }
  if(mode==='perm'){
    if(r===1) return `${sub(String(N))}P${sub(String(r))} = ${nPr(N,r)}`;
    if(r===2) return `${sub(String(N))}P${sub(String(r))} = 5 × 4 = ${nPr(N,r)}`;
    return `${sub(String(N))}P${sub(String(r))} = 5 × 4 × 3 = ${nPr(N,r)}`;
  }
  if(r===1) return `${sub(String(N))}C${sub(String(r))} = ${nCr(N,r)}`;
  if(r===2) return `${sub(String(N))}C${sub(String(r))} = (5×4)/(2×1) = ${nCr(N,r)}`;
  return `${sub(String(N))}C${sub(String(r))} = (5×4×3)/(3×2×1) = ${nCr(N,r)}`;
}

function updateResultBar(){
  const total = totalForMode();
  $('foundCount').textContent = foundSet.size;
  $('foundCount2').textContent = foundSet.size;
  $('totalCount').textContent = total;
  $('totalCount2').textContent = total;
  $('drawCount').textContent = drawCount;
  $('totalFormula').textContent = formulaStr();
  arrowBack.style.opacity = mode==='rep'?'1':'.15';
}

// === toast ===
let toastTimer=null;
function toast(msg){
  $('toast').innerHTML = msg;
  $('toast').classList.add('on');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(()=>$('toast').classList.remove('on'), 1700);
}

// === sample key/label ===
function sampleKey(arr){
  if(mode==='comb') return [...arr].sort((a,b)=>a-b).join(',');
  return arr.join(',');
}
function sampleHTML(arr, asMini=true){
  const cls = asMini?'mini-ball':'ball';
  let sorted = mode==='comb' ? [...arr].sort((a,b)=>a-b) : arr;
  const inner = sorted.map(n=>`<span class="${cls} b${n}">${n}</span>`).join(
    mode==='comb' ? '<span class="sep">,</span>' : '<span class="sep">→</span>'
  );
  if(mode==='comb') return `<span class="brace">{</span>${inner}<span class="brace">}</span>`;
  return inner;
}

// === draw animation ===
async function drawOne(){
  if(isAnimating) return;
  isAnimating = true;
  sampleZone.classList.remove('empty');
  sampleZone.innerHTML = '';
  drawCount++;

  // generate
  let arr;
  if(mode==='rep'){
    arr = Array.from({length:r}, ()=>1+Math.floor(Math.random()*N));
  } else {
    const pool = [1,2,3,4,5];
    for(let i=pool.length-1;i>0;i--){
      const j = Math.floor(Math.random()*(i+1));
      [pool[i],pool[j]] = [pool[j],pool[i]];
    }
    arr = pool.slice(0,r);
    if(mode==='comb') arr.sort((a,b)=>a-b);
  }

  // animate
  if(mode==='comb'){
    // 동시추출: 모든 공이 한꺼번에 날아옴
    // 1) 빈 슬롯들을 미리 만들어 sampleZone 위치를 확정
    const slots = [];
    for(let i=0;i<arr.length;i++){
      const slot = document.createElement('div');
      slot.className = 'ball-slot';
      slot.style.cssText = 'width:62px;height:62px';
      sampleZone.appendChild(slot);
      slots.push(slot);
    }
    // 2) 모든 공을 병렬로 애니메이션 (정렬된 순서대로 슬롯에 도착)
    await Promise.all(arr.map((n,i)=>animatePick(n, i, arr.length, slots[i])));
  } else {
    for(let i=0;i<arr.length;i++){
      await animatePick(arr[i], i, arr.length, null);
    }
  }

  // record
  const key = sampleKey(arr);
  const isNew = !foundSet.has(key);
  if(isNew){
    foundSet.add(key);
    addFoundCard(arr, true);
    if(foundSet.size === totalForMode()){
      toast('🎉 모든 표본을 다 발견했어요!');
    } else {
      toast('✨ 새로운 표본을 찾았어요!');
    }
  } else {
    toast('🔁 이미 발견한 표본이에요');
  }
  updateResultBar();
  isAnimating = false;
}

function getCenterRect(el, parent){
  const r1 = el.getBoundingClientRect();
  const r2 = parent.getBoundingClientRect();
  return {
    x: r1.left - r2.left + r1.width/2,
    y: r1.top  - r2.top  + r1.height/2,
    w: r1.width, h: r1.height,
  };
}

async function animatePick(num, idx, total, preSlot){
  return new Promise(resolve=>{
    const popEl = $(`pop-b${num}`);
    if(!popEl){ resolve(); return; }

    const startRect = getCenterRect(popEl, stage);

    // ghost flyer
    const fly = document.createElement('div');
    fly.className = `ball b${num} flying`;
    fly.textContent = num;
    fly.style.left = (startRect.x - startRect.w/2)+'px';
    fly.style.top  = (startRect.y - startRect.h/2)+'px';
    stage.appendChild(fly);

    // hide source visually
    popEl.style.opacity = '0';

    setTimeout(()=>{
      // pre-allocated slot for 동시추출, otherwise create now
      let slot;
      if(preSlot){
        slot = preSlot;
      } else {
        slot = document.createElement('div');
        slot.className = 'ball-slot';
        slot.style.cssText = 'width:62px;height:62px';
        sampleZone.appendChild(slot);
      }
      const slotRect = getCenterRect(slot, stage);

      const dx = slotRect.x - startRect.x;
      const dy = slotRect.y - startRect.y;
      fly.style.transform = `translate(${dx}px,${dy}px) scale(1.05)`;

      setTimeout(()=>{
        // flash 확인
        fly.style.filter = 'drop-shadow(0 0 18px #fde047) brightness(1.3)';
        setTimeout(()=>{
          fly.style.filter = '';

          if(mode==='rep'){
            // return to pop
            fly.style.transform = `translate(0,0) scale(1)`;
            setTimeout(()=>{
              fly.remove();
              popEl.style.opacity = '1';
              const stayBall = document.createElement('div');
              stayBall.className = `ball b${num}`;
              stayBall.textContent = num;
              const tag = document.createElement('div');
              tag.className = 'order-tag';
              tag.textContent = idx+1;
              stayBall.appendChild(tag);
              slot.replaceWith(stayBall);
              resolve();
            }, 600);
          } else {
            // non-replacement (비복원 or 동시): stay
            fly.remove();
            popEl.classList.add('gone');
            const stayBall = document.createElement('div');
            stayBall.className = `ball b${num}`;
            stayBall.textContent = num;
            if(mode==='perm'){
              const tag = document.createElement('div');
              tag.className = 'order-tag';
              tag.textContent = idx+1;
              stayBall.appendChild(tag);
            }
            // replaceWith preserves slot position (important for parallel comb animation)
            slot.replaceWith(stayBall);
            resolve();
          }
        }, 320);
      }, 700);
    }, 30);
  }).then(()=> new Promise(r=>setTimeout(r,180)));
}

// === reset visual after draw ===
function clearSampleZone(){
  sampleZone.innerHTML = '';
  sampleZone.classList.add('empty');
  // restore gone balls
  document.querySelectorAll('#popBalls .ball.gone').forEach(b=>b.classList.remove('gone'));
  document.querySelectorAll('#popBalls .ball').forEach(b=>b.style.opacity='1');
}

// === found grid ===
function addFoundCard(arr, fresh=false){
  const grid = $('foundGrid');
  if(grid.querySelector('.empty-msg')) grid.innerHTML = '';
  const card = document.createElement('div');
  card.className = 'sample-card' + (fresh?' fresh':'');
  card.innerHTML = sampleHTML(arr, true);
  grid.appendChild(card);
  setTimeout(()=>card.classList.remove('fresh'), 700);
}

function rebuildFoundGrid(){
  const grid = $('foundGrid');
  grid.innerHTML = '';
  if(foundSet.size===0){
    grid.innerHTML = '<div class="empty-msg" style="grid-column:1/-1">아직 뽑은 표본이 없어요. <b>한 번 뽑기</b> 버튼을 눌러보세요!</div>';
    return;
  }
  [...foundSet].forEach(k=>{
    const arr = k.split(',').map(Number);
    const card = document.createElement('div');
    card.className = 'sample-card';
    card.innerHTML = sampleHTML(arr, true);
    grid.appendChild(card);
  });
}

// === all-cases generator ===
function* allRep(n,r){
  const cur = Array(r).fill(1);
  while(true){
    yield [...cur];
    let i = r-1;
    while(i>=0 && cur[i]===n){ cur[i]=1; i--; }
    if(i<0) return;
    cur[i]++;
  }
}
function* allPerm(arr, k){
  if(k===0){ yield []; return; }
  for(let i=0;i<arr.length;i++){
    const rest = [...arr.slice(0,i), ...arr.slice(i+1)];
    for(const sub of allPerm(rest, k-1)){
      yield [arr[i], ...sub];
    }
  }
}
function* allComb(arr, k, start=0){
  if(k===0){ yield []; return; }
  for(let i=start;i<=arr.length-k;i++){
    for(const sub of allComb(arr, k-1, i+1)){
      yield [arr[i], ...sub];
    }
  }
}
function getAll(){
  const out = [];
  if(mode==='rep'){
    for(const s of allRep(N,r)) out.push(s);
  } else if(mode==='perm'){
    for(const s of allPerm([1,2,3,4,5], r)) out.push(s);
  } else {
    for(const s of allComb([1,2,3,4,5], r)) out.push(s);
  }
  return out;
}

function showAll(){
  if(isAnimating) return;
  const all = getAll();
  foundSet.clear();
  all.forEach(a=>foundSet.add(sampleKey(a)));
  rebuildFoundGrid();
  updateResultBar();
  toast(`📊 모든 ${all.length}가지 경우를 보여줄게요!`);
}

// === control wiring ===
document.querySelectorAll('.mode-btn').forEach(b=>{
  b.addEventListener('click', ()=>{
    if(isAnimating) return;
    document.querySelectorAll('.mode-btn').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    mode = b.dataset.mode;
    foundSet.clear(); drawCount=0;
    clearSampleZone(); rebuildFoundGrid(); updateResultBar();
    updateModeInfo();
  });
});

document.querySelectorAll('.r-btn').forEach(b=>{
  b.addEventListener('click', ()=>{
    if(isAnimating) return;
    document.querySelectorAll('.r-btn').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    r = +b.dataset.r;
    foundSet.clear(); drawCount=0;
    clearSampleZone(); rebuildFoundGrid(); updateResultBar();
  });
});

$('btnDraw').addEventListener('click', ()=>{
  if(isAnimating) return;
  clearSampleZone();
  setTimeout(drawOne, 80);
});
$('btnAll').addEventListener('click', showAll);
$('btnReset').addEventListener('click', ()=>{
  if(isAnimating) return;
  foundSet.clear(); drawCount=0;
  clearSampleZone(); rebuildFoundGrid(); updateResultBar();
  toast('🗑️ 처음으로 돌아갔어요');
});

updateResultBar();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: 한눈에 비교 (Side-by-side comparison)
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
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0c4a6e 100%);
  color:#e2e8f0;padding:18px 14px;min-height:100vh;font-size:16px;line-height:1.55;
}
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(34,211,238,.18),rgba(168,85,247,.12));
  border:2px solid rgba(34,211,238,.4);border-radius:18px;
  padding:16px 20px;margin-bottom:14px;
}
.hdr h1{font-size:1.55rem;font-weight:900;color:#bae6fd;margin-bottom:6px}
.hdr p{font-size:1.02rem;color:#cbd5e1}

.ctrl-bar{
  display:flex;flex-wrap:wrap;gap:18px;justify-content:center;align-items:center;
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.32);
  border-radius:14px;padding:14px 18px;margin-bottom:14px;
}
.ctrl-cell{display:flex;align-items:center;gap:10px}
.ctrl-lab{font-size:1rem;font-weight:800;color:#a5b4fc}
.slider{
  -webkit-appearance:none;width:160px;height:8px;
  background:linear-gradient(90deg,#334155,#475569);border-radius:4px;outline:none;
}
.slider::-webkit-slider-thumb{
  -webkit-appearance:none;width:22px;height:22px;border-radius:50%;
  background:radial-gradient(circle at 30% 30%,#fde68a,#f59e0b);
  cursor:pointer;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.4);
}
.val-pill{
  display:inline-block;min-width:38px;text-align:center;
  background:#fbbf24;color:#1f2937;font-weight:900;font-size:1.1rem;
  padding:4px 10px;border-radius:8px;
}

/* === three columns === */
.compare-grid{
  display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px;
}
@media(max-width:900px){.compare-grid{grid-template-columns:1fr}}

.col{
  background:rgba(15,23,42,.55);border-radius:14px;padding:14px 14px 12px;
  border:2px solid rgba(99,102,241,.3);position:relative;overflow:hidden;
}
.col.rep{border-color:rgba(34,197,94,.5)}
.col.perm{border-color:rgba(245,158,11,.5)}
.col.comb{border-color:rgba(236,72,153,.5)}

.col-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}
.col-title{font-size:1.18rem;font-weight:900}
.col.rep .col-title{color:#86efac}
.col.perm .col-title{color:#fcd34d}
.col.comb .col-title{color:#f9a8d4}
.col-tag{font-size:.8rem;color:#94a3b8}

.col-formula{
  background:rgba(0,0,0,.4);border-radius:10px;padding:10px 12px;
  text-align:center;font-size:1.05rem;font-weight:800;color:#e2e8f0;margin-bottom:10px;
  border:1px dashed rgba(148,163,184,.3);
}
.col-formula b{color:#fde68a;font-size:1.3rem}

.col-list{
  display:flex;flex-wrap:wrap;gap:6px;
  max-height:340px;overflow-y:auto;padding:8px;
  background:rgba(0,0,0,.28);border-radius:10px;
}
.col-list::-webkit-scrollbar{width:7px}
.col-list::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:4px}
.col-list::-webkit-scrollbar-thumb{background:#475569;border-radius:4px}

.tinytag{
  background:rgba(30,41,59,.7);border:1px solid rgba(148,163,184,.25);
  border-radius:8px;padding:5px 7px;display:flex;align-items:center;gap:3px;
  font-size:.78rem;color:#cbd5e1;
}
.tinytag .mb{
  width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:.7rem;font-weight:900;color:#fff;
  box-shadow:0 1px 3px rgba(0,0,0,.4),inset 1px 1px 0 rgba(255,255,255,.3);
}
.mb.b1{background:radial-gradient(circle at 30% 28%,#fca5a5,#dc2626)}
.mb.b2{background:radial-gradient(circle at 30% 28%,#fcd34d,#d97706)}
.mb.b3{background:radial-gradient(circle at 30% 28%,#86efac,#16a34a)}
.mb.b4{background:radial-gradient(circle at 30% 28%,#7dd3fc,#0284c7)}
.mb.b5{background:radial-gradient(circle at 30% 28%,#c4b5fd,#7c3aed)}
.mb.b6{background:radial-gradient(circle at 30% 28%,#f9a8d4,#db2777)}

.col-key{font-size:.92rem;color:#94a3b8;margin-top:6px;text-align:center;font-style:italic}
.col-key b{color:#fbbf24}

/* === bar comparison === */
.bar-area{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(168,85,247,.32);
  border-radius:14px;padding:14px 16px;margin-bottom:14px;
}
.bar-title{font-size:1.05rem;font-weight:900;color:#c4b5fd;margin-bottom:12px;text-align:center}
.bar-row{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.bar-row:last-child{margin-bottom:0}
.bar-name{
  flex:0 0 110px;font-size:.98rem;font-weight:800;text-align:right;
}
.bar-row.rep .bar-name{color:#86efac}
.bar-row.perm .bar-name{color:#fcd34d}
.bar-row.comb .bar-name{color:#f9a8d4}
.bar-track{flex:1;height:34px;background:rgba(0,0,0,.4);border-radius:8px;overflow:hidden;position:relative}
.bar-fill{
  height:100%;border-radius:8px;
  display:flex;align-items:center;justify-content:flex-end;padding-right:10px;
  color:#fff;font-weight:900;font-size:1rem;
  transition:width .55s cubic-bezier(.4,0,.2,1);
}
.bar-row.rep .bar-fill{background:linear-gradient(90deg,#16a34a,#86efac)}
.bar-row.perm .bar-fill{background:linear-gradient(90deg,#d97706,#fcd34d)}
.bar-row.comb .bar-fill{background:linear-gradient(90deg,#db2777,#f9a8d4)}

.insight{
  background:rgba(15,23,42,.65);border-left:4px solid #fbbf24;
  border-radius:10px;padding:14px 16px;font-size:1rem;color:#e2e8f0;line-height:1.7;
}
.insight b{color:#fde68a}
.insight .lbl{display:inline-block;background:rgba(251,191,36,.18);padding:1px 8px;border-radius:6px;color:#fde68a;font-weight:800;margin-right:4px}
</style>
</head>
<body>

<div class="hdr">
  <h1>🔭 한눈에 비교해 보기</h1>
  <p>n과 r을 직접 바꿔보며 세 가지 추출 방법으로 가능한 표본을 모두 펼쳐봐요</p>
</div>

<div class="ctrl-bar">
  <div class="ctrl-cell">
    <span class="ctrl-lab">모집단 크기 n</span>
    <input type="range" min="2" max="6" value="4" class="slider" id="sn">
    <span class="val-pill" id="vn">4</span>
  </div>
  <div class="ctrl-cell">
    <span class="ctrl-lab">뽑을 개수 r</span>
    <input type="range" min="1" max="3" value="2" class="slider" id="sr">
    <span class="val-pill" id="vr">2</span>
  </div>
</div>

<div class="compare-grid">
  <div class="col rep">
    <div class="col-head">
      <div class="col-title">🟢 복원추출</div>
      <div class="col-tag">순서 O · 중복 O</div>
    </div>
    <div class="col-formula" id="fRep"></div>
    <div class="col-list" id="lRep"></div>
    <div class="col-key">한 번 뽑은 공도 <b>다시</b> 뽑힐 수 있어요</div>
  </div>

  <div class="col perm">
    <div class="col-head">
      <div class="col-title">🟠 비복원추출</div>
      <div class="col-tag">순서 O · 중복 X</div>
    </div>
    <div class="col-formula" id="fPerm"></div>
    <div class="col-list" id="lPerm"></div>
    <div class="col-key">뽑은 공은 빼놓고, <b>순서</b>를 구분해요</div>
  </div>

  <div class="col comb">
    <div class="col-head">
      <div class="col-title">🟣 동시추출</div>
      <div class="col-tag">순서 X · 중복 X</div>
    </div>
    <div class="col-formula" id="fComb"></div>
    <div class="col-list" id="lComb"></div>
    <div class="col-key">한 번에 동시에, <b>순서 무시</b>해요</div>
  </div>
</div>

<div class="bar-area">
  <div class="bar-title">📊 가능한 표본의 수 비교</div>
  <div class="bar-row rep">
    <div class="bar-name">복원 ₙΠᵣ</div>
    <div class="bar-track"><div class="bar-fill" id="bRep">0</div></div>
  </div>
  <div class="bar-row perm">
    <div class="bar-name">비복원 ₙPᵣ</div>
    <div class="bar-track"><div class="bar-fill" id="bPerm">0</div></div>
  </div>
  <div class="bar-row comb">
    <div class="bar-name">동시 ₙCᵣ</div>
    <div class="bar-track"><div class="bar-fill" id="bComb">0</div></div>
  </div>
</div>

<div class="insight" id="insight"></div>

<script>
const $ = id => document.getElementById(id);

function fact(n){let f=1;for(let i=2;i<=n;i++)f*=i;return f}
function nPr(n,r){if(r>n)return 0;let v=1;for(let i=0;i<r;i++)v*=(n-i);return v}
function nCr(n,r){if(r>n)return 0;return Math.round(nPr(n,r)/fact(r))}
function nPi(n,r){return Math.pow(n,r)}

const SUB = {0:'₀',1:'₁',2:'₂',3:'₃',4:'₄',5:'₅',6:'₆',7:'₇',8:'₈',9:'₉'};
const sub = (x)=>String(x).split('').map(c=>SUB[c]||c).join('');

function* allRep(n,r){
  const cur = Array(r).fill(1);
  while(true){
    yield [...cur];
    let i = r-1;
    while(i>=0 && cur[i]===n){ cur[i]=1; i--; }
    if(i<0) return;
    cur[i]++;
  }
}
function* allPerm(arr,k){
  if(k===0){ yield []; return; }
  for(let i=0;i<arr.length;i++){
    const rest=[...arr.slice(0,i),...arr.slice(i+1)];
    for(const sb of allPerm(rest,k-1)) yield [arr[i],...sb];
  }
}
function* allComb(arr,k,start=0){
  if(k===0){ yield []; return; }
  for(let i=start;i<=arr.length-k;i++){
    for(const sb of allComb(arr,k-1,i+1)) yield [arr[i],...sb];
  }
}

function tagHTML(arr, sep='→', brace=false){
  const inner = arr.map(n=>`<span class="mb b${((n-1)%6)+1}">${n}</span>`).join(`<span style="color:#64748b;font-weight:900">${sep}</span>`);
  if(brace) return `<div class="tinytag"><span style="color:#fbbf24;font-weight:900">{</span>${inner}<span style="color:#fbbf24;font-weight:900">}</span></div>`;
  return `<div class="tinytag">${inner}</div>`;
}

function render(){
  const n = +$('sn').value;
  const r = +$('sr').value;
  $('vn').textContent = n;
  $('vr').textContent = r;

  const repCnt  = nPi(n,r);
  const permCnt = nPr(n,r);
  const combCnt = nCr(n,r);

  // formulas
  $('fRep').innerHTML  = `${sub(n)}Π${sub(r)} = ${n}<sup>${r}</sup> = <b>${repCnt}</b>`;
  const permMul = r===0?'1':Array.from({length:r},(_,i)=>n-i).join('×');
  $('fPerm').innerHTML = `${sub(n)}P${sub(r)} = ${permMul} = <b>${permCnt}</b>`;
  const facMul = r<=1?String(Math.max(r,1)):Array.from({length:r},(_,i)=>r-i).join('×');
  $('fComb').innerHTML = `${sub(n)}C${sub(r)} = (${permMul})/(${facMul}) = <b>${combCnt}</b>`;

  // lists
  let hRep='', hPerm='', hComb='';
  for(const s of allRep(n,r)) hRep  += tagHTML(s, '→');
  for(const s of allPerm(Array.from({length:n},(_,i)=>i+1), r)) hPerm += tagHTML(s, '→');
  for(const s of allComb(Array.from({length:n},(_,i)=>i+1), r)) hComb += tagHTML(s, ',', true);
  $('lRep').innerHTML  = hRep || '<div style="color:#64748b;font-style:italic;padding:8px">(없음)</div>';
  $('lPerm').innerHTML = hPerm|| '<div style="color:#64748b;font-style:italic;padding:8px">(없음)</div>';
  $('lComb').innerHTML = hComb|| '<div style="color:#64748b;font-style:italic;padding:8px">(없음)</div>';

  // bars
  const mx = Math.max(repCnt, permCnt, combCnt, 1);
  const pct = v => Math.max(8, (v/mx)*100);
  $('bRep').style.width  = pct(repCnt)+'%';   $('bRep').textContent  = repCnt;
  $('bPerm').style.width = pct(permCnt)+'%';  $('bPerm').textContent = permCnt;
  $('bComb').style.width = pct(combCnt)+'%';  $('bComb').textContent = combCnt;

  // insight
  const order = [['복원',repCnt],['비복원',permCnt],['동시',combCnt]];
  let ins = `<span class="lbl">현재 n=${n}, r=${r}</span> `;
  if(r>n){
    ins += `r이 n보다 크면 <b>비복원·동시추출은 불가능</b>해요 (뽑을 수가 없죠!). 하지만 <b>복원추출은 가능</b>해서 같은 공을 여러 번 뽑을 수 있어요.`;
  } else if(r===1){
    ins += `r=1일 때는 세 방법 모두 결과가 같아요 (₅Π₁ = ₅P₁ = ₅C₁ = ${repCnt}). 한 개만 뽑으니 순서·복원의 차이가 없죠!`;
  } else {
    const ratio1 = (repCnt/permCnt).toFixed(2);
    const ratio2 = (permCnt/combCnt);
    ins += `<b>복원 ${repCnt}</b> > <b>비복원 ${permCnt}</b> > <b>동시 ${combCnt}</b> `;
    ins += `<br>· 복원 ÷ 비복원 = <b>${ratio1}</b> (중복을 허용하면 그만큼 경우가 늘어나요)`;
    ins += `<br>· 비복원 ÷ 동시 = <b>${ratio2}</b> = ${r}! (같은 표본의 ${r}! = ${fact(r)}가지 순서가 동시추출에서는 1가지로 합쳐져요)`;
  }
  $('insight').innerHTML = ins;
}

$('sn').addEventListener('input', render);
$('sr').addEventListener('input', render);
render();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: 시나리오 챌린지 (Real-world matching quiz)
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
  background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#0f172a 100%);
  color:#e2e8f0;padding:18px 14px;min-height:100vh;font-size:16px;line-height:1.55;
}
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(168,85,247,.2),rgba(236,72,153,.12));
  border:2px solid rgba(168,85,247,.4);border-radius:18px;
  padding:16px 20px;margin-bottom:14px;
}
.hdr h1{font-size:1.55rem;font-weight:900;color:#e9d5ff;margin-bottom:6px}
.hdr p{font-size:1.02rem;color:#cbd5e1}

.score-bar{
  display:flex;justify-content:space-between;align-items:center;
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.32);
  border-radius:12px;padding:10px 18px;margin-bottom:14px;
}
.score-bar .left{font-size:1rem;font-weight:800;color:#a5b4fc}
.score-bar .right{font-size:1.1rem;font-weight:900;color:#fbbf24}
.prog-track{height:8px;background:#1e293b;border-radius:5px;overflow:hidden;flex:1;margin:0 14px}
.prog-fill{height:100%;background:linear-gradient(90deg,#a855f7,#ec4899);width:0;transition:width .45s ease}

.q-card{
  background:rgba(15,23,42,.55);border:2px solid rgba(168,85,247,.3);
  border-radius:16px;padding:18px 18px 16px;margin-bottom:14px;min-height:200px;
}
.q-num{font-size:.92rem;color:#a5b4fc;font-weight:800;margin-bottom:8px}
.q-stem{font-size:1.18rem;font-weight:800;color:#fef9c3;margin-bottom:14px;line-height:1.55}
.q-stem .hi{color:#fde68a;background:rgba(251,191,36,.15);padding:2px 7px;border-radius:6px}

.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.opt{
  position:relative;background:rgba(30,41,59,.65);border:2px solid rgba(148,163,184,.3);
  border-radius:12px;padding:14px;font-size:1rem;cursor:pointer;
  transition:all .18s ease;color:#e2e8f0;text-align:center;
}
.opt:hover:not(.locked){transform:translateY(-2px);border-color:#a5b4fc;background:rgba(67,56,202,.25)}
.opt .em{font-size:1.4rem;display:block;margin-bottom:6px}
.opt .tt{font-weight:900;font-size:1.02rem}
.opt .dd{font-size:.86rem;color:#94a3b8;margin-top:4px}
.opt.locked{cursor:default}
.opt.correct{border-color:#22c55e;background:rgba(34,197,94,.22);box-shadow:0 0 18px rgba(34,197,94,.4)}
.opt.wrong{border-color:#ef4444;background:rgba(239,68,68,.18);opacity:.7}
.opt.show-ans{border-color:#fbbf24;background:rgba(251,191,36,.18)}

.fb{
  background:rgba(0,0,0,.42);border-radius:12px;padding:14px;margin-top:12px;
  border-left:4px solid #fbbf24;display:none;
}
.fb.on{display:block;animation:slideDown .35s ease}
@keyframes slideDown{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}
.fb .res-tag{font-size:1.05rem;font-weight:900;margin-bottom:6px}
.fb .res-tag.ok{color:#86efac}
.fb .res-tag.no{color:#fca5a5}
.fb .expl{font-size:.98rem;color:#cbd5e1;line-height:1.7}
.fb .expl b{color:#fde68a}

.nav-btns{display:flex;justify-content:space-between;gap:10px;margin-top:14px}
.nav-btn{
  flex:1;padding:12px;border-radius:11px;border:none;cursor:pointer;
  font-size:1rem;font-weight:900;color:#fff;transition:all .2s ease;
}
.btn-next{background:linear-gradient(135deg,#22c55e,#16a34a)}
.btn-show{background:linear-gradient(135deg,#f59e0b,#d97706)}
.btn-restart{background:linear-gradient(135deg,#64748b,#475569)}
.nav-btn:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.4)}
.nav-btn:disabled{opacity:.42;cursor:not-allowed}

.final-card{
  background:linear-gradient(135deg,rgba(168,85,247,.2),rgba(34,211,238,.15));
  border:2px solid rgba(168,85,247,.5);border-radius:18px;
  padding:30px 20px;text-align:center;display:none;
}
.final-card.on{display:block}
.final-card .emoji{font-size:4.5rem;margin-bottom:10px}
.final-card h2{font-size:1.5rem;font-weight:900;color:#e9d5ff;margin-bottom:8px}
.final-card .score{font-size:1.4rem;font-weight:900;color:#fbbf24;margin:14px 0}
.final-card p{font-size:1.05rem;color:#cbd5e1;line-height:1.7;margin-bottom:14px}
</style>
</head>
<body>

<div class="hdr">
  <h1>🎬 시나리오 챌린지</h1>
  <p>일상 속 상황은 어떤 추출에 해당할까? 답을 고르고 이유를 확인해 봐요!</p>
</div>

<div class="score-bar">
  <span class="left" id="qInfo">문제 1 / 6</span>
  <div class="prog-track"><div class="prog-fill" id="prog"></div></div>
  <span class="right" id="score">⭐ 0점</span>
</div>

<div id="qWrap"></div>

<div class="final-card" id="final">
  <div class="emoji" id="finalEmoji">🎉</div>
  <h2 id="finalTitle">참 잘했어요!</h2>
  <div class="score" id="finalScore">0 / 6</div>
  <p id="finalMsg">세 가지 추출 방법의 차이를 잘 이해했어요!</p>
  <button class="nav-btn btn-restart" id="btnRestart" style="max-width:200px;margin:0 auto;display:block">🔄 다시 풀어보기</button>
</div>

<script>
const QUESTIONS = [
  {
    stem: '주사위를 <span class="hi">3번 던져서</span> 나온 눈을 차례로 기록한다. 가능한 결과의 수를 구하는 추출 방법은?',
    ans: 'rep',
    expl: '주사위는 던져도 1~6의 눈이 그대로 남아 있어 <b>다음 던질 때도 같은 눈이 나올 수 있어요</b>. 또 던지는 순서를 구분해서 기록하므로 <b>복원추출</b>에 해당해요. (6³ = 216가지)'
  },
  {
    stem: '카드 5장 중에서 <span class="hi">한 장씩 뽑아 일렬로 놓는다</span> (단, 뽑은 카드는 되돌려 놓지 않는다). 가능한 배열의 수는?',
    ans: 'perm',
    expl: '되돌려 놓지 않으니 한 번 뽑은 카드는 다시 못 뽑아요. 그리고 <b>일렬로 놓으니 순서를 구분</b>하죠. 따라서 <b>비복원추출(순열)</b>에 해당해요.'
  },
  {
    stem: '학급 30명 중에서 <span class="hi">청소 당번 4명을 동시에</span> 뽑는다. 가능한 경우의 수는?',
    ans: 'comb',
    expl: '4명을 한꺼번에 뽑으니 누가 먼저인지 <b>순서를 구분하지 않아요</b>. {철수, 영희, 민수, 지영} = {지영, 민수, 영희, 철수}로 같은 표본이죠. 따라서 <b>동시추출(조합)</b>이에요.'
  },
  {
    stem: '로또에서 1~45 중 <span class="hi">서로 다른 숫자 6개</span>를 한 번에 뽑는 경우의 수는?',
    ans: 'comb',
    expl: '로또는 6개를 한꺼번에 뽑고 어떤 순서로 나왔는지는 상관없어요. 같은 6개 숫자면 같은 결과죠. <b>동시추출</b>(₄₅C₆)에 해당해요.'
  },
  {
    stem: '비밀번호 4자리를 <span class="hi">0~9</span> 중에서 만든다 (같은 숫자 사용 가능). 가능한 비밀번호의 수는?',
    ans: 'rep',
    expl: '같은 숫자를 여러 번 써도 되고(예: 1111), 자리에 따라 1234와 4321은 <b>다른 비밀번호</b>예요. 따라서 <b>복원추출</b>(10⁴ = 10000가지)에 해당해요.'
  },
  {
    stem: '8명의 학생 중에서 <span class="hi">반장 1명, 부반장 1명, 서기 1명</span>을 뽑는다 (한 사람이 두 자리를 겸할 수 없음). 가능한 경우의 수는?',
    ans: 'perm',
    expl: '한 사람이 여러 역할을 못 하니 한 번 뽑힌 사람은 다시 못 뽑혀요 (비복원). 그리고 반장·부반장·서기는 <b>서로 다른 역할</b>이라 순서를 구분하죠. <b>비복원추출(순열)</b>이에요. (₈P₃ = 336)'
  },
];

const OPTIONS = [
  {key:'rep',  em:'🟢', tt:'복원추출',  dd:'순서O · 중복O'},
  {key:'perm', em:'🟠', tt:'비복원추출', dd:'순서O · 중복X'},
  {key:'comb', em:'🟣', tt:'동시추출',  dd:'순서X · 중복X'},
];

const $ = id => document.getElementById(id);
let idx = 0, score = 0, locked = false;

function render(){
  $('final').classList.remove('on');
  if(idx>=QUESTIONS.length){ showFinal(); return; }
  const q = QUESTIONS[idx];
  $('qInfo').textContent = `문제 ${idx+1} / ${QUESTIONS.length}`;
  $('prog').style.width = `${(idx/QUESTIONS.length)*100}%`;
  $('score').textContent = `⭐ ${score}점`;

  let h = `<div class="q-card">
    <div class="q-num">Q${idx+1}.</div>
    <div class="q-stem">${q.stem}</div>
    <div class="opts">`;
  for(const o of OPTIONS){
    h += `<div class="opt" data-k="${o.key}">
      <span class="em">${o.em}</span>
      <div class="tt">${o.tt}</div>
      <div class="dd">${o.dd}</div>
    </div>`;
  }
  h += `</div>
    <div class="fb" id="fb"></div>
    <div class="nav-btns">
      <button class="nav-btn btn-show" id="btnShow">👀 정답 보기</button>
      <button class="nav-btn btn-next" id="btnNext" disabled>다음 문제 ➜</button>
    </div>
  </div>`;
  $('qWrap').innerHTML = h;
  locked = false;

  document.querySelectorAll('.opt').forEach(el=>{
    el.addEventListener('click', ()=>pick(el.dataset.k, el));
  });
  $('btnShow').addEventListener('click', showAnswer);
  $('btnNext').addEventListener('click', ()=>{ idx++; render(); });
}

function pick(k, el){
  if(locked) return;
  locked = true;
  const q = QUESTIONS[idx];
  const ok = k===q.ans;
  if(ok){ el.classList.add('correct'); score++; }
  else  { el.classList.add('wrong'); document.querySelector(`.opt[data-k="${q.ans}"]`).classList.add('correct'); }
  document.querySelectorAll('.opt').forEach(o=>o.classList.add('locked'));
  const fb = $('fb');
  fb.innerHTML = `<div class="res-tag ${ok?'ok':'no'}">${ok?'✅ 정답이에요!':'❌ 다시 한번 생각해봐요'}</div><div class="expl">${q.expl}</div>`;
  fb.classList.add('on');
  $('btnNext').disabled = false;
  $('btnShow').disabled = true;
}

function showAnswer(){
  if(locked) return;
  locked = true;
  const q = QUESTIONS[idx];
  document.querySelector(`.opt[data-k="${q.ans}"]`).classList.add('show-ans');
  document.querySelectorAll('.opt').forEach(o=>o.classList.add('locked'));
  const fb = $('fb');
  fb.innerHTML = `<div class="res-tag" style="color:#fbbf24">👀 정답을 확인했어요</div><div class="expl">${q.expl}</div>`;
  fb.classList.add('on');
  $('btnNext').disabled = false;
  $('btnShow').disabled = true;
}

function showFinal(){
  $('qWrap').innerHTML = '';
  $('qInfo').textContent = `완료!`;
  $('prog').style.width = '100%';
  $('score').textContent = `⭐ ${score}점`;
  $('finalScore').textContent = `${score} / ${QUESTIONS.length}`;
  let em='🎉', tt='참 잘했어요!', msg='세 가지 추출 방법의 차이를 잘 이해했어요!';
  if(score===QUESTIONS.length){ em='🏆'; tt='완벽해요!'; msg='모든 문제를 맞췄어요! 복원·비복원·동시추출의 차이를 완벽하게 이해하고 있군요!'; }
  else if(score>=QUESTIONS.length*0.5){ em='🌟'; tt='잘하고 있어요!'; msg='조금만 더 연습하면 완벽해질 거예요. 틀린 문제의 해설을 다시 한 번 살펴봐요!'; }
  else { em='💪'; tt='다시 도전해 봐요!'; msg='추출 방법의 차이를 다시 한 번 정리해 보고 도전해 봐요. 시뮬레이션 탭에서 직접 뽑아보면 도움이 될 거예요!'; }
  $('finalEmoji').textContent = em;
  $('finalTitle').textContent = tt;
  $('finalMsg').textContent = msg;
  $('final').classList.add('on');
}

$('btnRestart').addEventListener('click', ()=>{ idx=0; score=0; render(); });
render();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("🎁 복원·비복원·동시추출 실험실")
    st.caption(
        "모집단에서 표본을 뽑는 세 가지 방법 — "
        "**복원추출 · 비복원추출 · 동시추출** — 을 직접 체험하며 "
        "가능한 표본의 수가 왜 다르게 나오는지 알아봐요!"
    )

    tab1, tab2, tab3 = st.tabs([
        "🎲 직접 뽑아보기",
        "🔭 한눈에 비교",
        "🎬 시나리오 챌린지",
    ])

    with tab1:
        components.html(_HTML_TAB1, height=1200, scrolling=True)

    with tab2:
        components.html(_HTML_TAB2, height=1250, scrolling=True)

    with tab3:
        components.html(_HTML_TAB3, height=900, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
