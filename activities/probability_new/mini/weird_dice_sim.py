# activities/probability_new/mini/weird_dice_sim.py
"""
이상한 주사위 시뮬레이터 – 수학적 확률의 조건 탐구
다양한 형태의 주사위를 굴려보며 수학적 확률이 성립하기 위한 조건을 직접 탐구합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎲 이상한 주사위와 수학적 확률",
    "description": "다양한 형태의 주사위 시뮬레이션으로 수학적 확률이 성립하기 위한 조건을 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "이상한주사위"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 이상한 주사위와 수학적 확률**"},
    {
        "key": "조건발견",
        "label": "수학적 확률을 정의하기 위해 필요한 조건 두 가지를 이 활동을 통해 발견한 것을 정리해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "조건 1: ...\n조건 2: ..."
    },
    {
        "key": "어느주사위",
        "label": "각 주사위가 수학적 확률을 성립시키는지 여부와 그 이유를 설명하세요.",
        "type": "text_area",
        "height": 120,
        "placeholder": "정육면체: ...\n사각뿔대: ...\n구형: ...\n정팔면체: ..."
    },
    {
        "key": "구형특이점",
        "label": "구형 주사위에서 특이한 결과가 나왔나요? 이것이 수학적 확률과 어떤 관련이 있는지 설명하세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) '경계' 결과가 나왔는데, 이것은 두 사건이 동시에..."
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area",
        "height": 80
    },
    {
        "key": "느낀점",
        "label": "💬 이 활동을 하면서 느낀 점",
        "type": "text_area",
        "height": 80
    },
]

_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>이상한 주사위 시뮬레이터</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 60%,#0f172a 100%);
  color:#e2e8f0;
  padding:14px 12px 24px;
  min-height:100vh;
}

/* ─── 헤더 ─── */
.hdr{
  text-align:center;margin-bottom:16px;
  padding:14px 16px;
  background:rgba(255,255,255,.06);
  border-radius:14px;
  border:1px solid rgba(255,255,255,.1);
}
.hdr h1{font-size:1.25rem;color:#a78bfa;margin-bottom:5px;}
.hdr p{font-size:.8rem;color:#94a3b8;line-height:1.6;}

/* ─── 주사위 선택 그리드 ─── */
.dice-grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:10px;
  margin-bottom:14px;
}
@media(max-width:680px){.dice-grid{grid-template-columns:repeat(2,1fr);}}
.dice-card{
  background:rgba(255,255,255,.05);
  border:2px solid rgba(255,255,255,.1);
  border-radius:14px;
  padding:12px 8px 10px;
  cursor:pointer;
  transition:all .2s;
  text-align:center;
  user-select:none;
}
.dice-card:hover{
  background:rgba(255,255,255,.09);
  transform:translateY(-3px);
  box-shadow:0 8px 24px rgba(0,0,0,.5);
}
.dice-card.selected{
  border-color:#a78bfa;
  background:rgba(167,139,250,.13);
  box-shadow:0 0 20px rgba(167,139,250,.25);
}
.dice-card svg{width:76px;height:76px;display:block;margin:0 auto 8px;}
.dice-name{font-weight:700;font-size:.9rem;margin-bottom:3px;}
.dice-sub{font-size:.7rem;color:#94a3b8;line-height:1.35;margin-bottom:6px;}

/* ─── 컨트롤 바 ─── */
.ctrl-bar{
  display:flex;align-items:center;gap:10px;
  flex-wrap:wrap;
  background:rgba(255,255,255,.05);
  border-radius:12px;
  padding:10px 14px;
  margin-bottom:12px;
}
.ctrl-label{font-size:.78rem;color:#94a3b8;white-space:nowrap;}
input[type=range]{accent-color:#a78bfa;width:110px;cursor:pointer;}
.n-val{font-weight:700;color:#a78bfa;min-width:42px;font-size:.88rem;}
.total-label{margin-left:auto;font-size:.78rem;color:#94a3b8;}
.total-num{color:#a78bfa;font-weight:700;}
.btn{
  padding:8px 18px;border-radius:10px;border:none;
  cursor:pointer;font-weight:700;font-size:.85rem;
  transition:all .15s;white-space:nowrap;
}
.btn:hover{filter:brightness(1.12);}
.btn:active{transform:scale(.97);}
.btn-roll{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff;}
.btn-reset{background:rgba(255,255,255,.08);color:#94a3b8;font-size:.75rem;padding:6px 12px;}
.btn:disabled{opacity:.45;cursor:not-allowed;pointer-events:none;}

/* ─── 굴리기 영역 ─── */
.roll-box{
  background:rgba(0,0,0,.35);
  border-radius:16px;
  border:1px solid rgba(255,255,255,.07);
  min-height:130px;
  display:flex;align-items:center;justify-content:center;
  flex-direction:column;gap:8px;
  margin-bottom:12px;
  position:relative;overflow:hidden;
}
.roll-prompt{font-size:.88rem;color:#475569;text-align:center;padding:0 20px;}
#rollAnim{
  font-size:4rem;display:none;
  animation:spin .1s linear infinite;
}
#rollResult{
  font-size:3.2rem;font-weight:900;display:none;
  animation:pop .28s cubic-bezier(.25,1.5,.5,1);
}
#rollLabel{font-size:.82rem;color:#94a3b8;display:none;}
.boundary-result{
  background:linear-gradient(135deg,#7c3aed,#ec4899);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  font-weight:900;
}
@keyframes spin{
  to{transform:rotate(360deg) scale(1.05);}
}
@keyframes pop{
  0%{transform:scale(.2);opacity:0;}
  65%{transform:scale(1.18);}
  100%{transform:scale(1);opacity:1;}
}

/* ─── 통계 영역 ─── */
.stats-wrap{
  background:rgba(255,255,255,.04);
  border-radius:14px;
  border:1px solid rgba(255,255,255,.07);
  padding:13px 14px;
  margin-bottom:12px;
  display:none;
}
.stats-hdr{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:11px;
}
.stats-title{font-size:.86rem;font-weight:700;color:#a78bfa;}
.stats-count{font-size:.76rem;color:#64748b;}
.bar-row{margin-bottom:9px;}
.bar-meta{
  display:flex;justify-content:space-between;
  font-size:.74rem;color:#94a3b8;margin-bottom:3px;
}
.bar-track{
  background:rgba(255,255,255,.07);
  border-radius:6px;height:20px;position:relative;overflow:hidden;
}
.bar-fill{
  height:100%;border-radius:6px;
  transition:width .35s ease;
  display:flex;align-items:center;justify-content:flex-end;
  padding-right:5px;
  font-size:.68rem;font-weight:700;color:rgba(255,255,255,.9);
}
.bar-ideal{
  position:absolute;top:0;bottom:0;width:2px;
  background:rgba(255,255,255,.45);
  pointer-events:none;
  z-index:2;
}
.ideal-tip{
  font-size:.62rem;color:rgba(255,255,255,.35);
  position:absolute;top:1px;left:3px;
  white-space:nowrap;
}
.ideal-note{font-size:.68rem;color:#334155;margin-top:6px;text-align:right;}

/* ─── 인사이트 ─── */
.insight{
  border-radius:12px;padding:12px 14px;
  font-size:.8rem;line-height:1.65;
  border-left:4px solid;
  display:none;
  margin-bottom:8px;
  animation:fadeIn .4s ease;
}
.ins-ok  {background:rgba(16,185,129,.1);border-color:#10b981;color:#a7f3d0;}
.ins-warn{background:rgba(245,158,11,.1);border-color:#f59e0b;color:#fde68a;}
.ins-bad {background:rgba(236,72,153,.1); border-color:#ec4899;color:#fbcfe8;}
.ins-title{font-weight:700;margin-bottom:5px;font-size:.86rem;}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px);}to{opacity:1;transform:none;}}
</style>
</head>
<body>

<!-- 헤더 -->
<div class="hdr">
  <h1>🎲 이상한 주사위와 수학적 확률</h1>
  <p>주사위 모양이 달라지면 수학적 확률을 정의할 수 있을까요?<br>
  여러 형태의 주사위를 직접 굴려보며 조건을 탐구해보세요!</p>
</div>

<!-- 주사위 카드 그리드 -->
<div class="dice-grid" id="diceGrid"></div>

<!-- 컨트롤 -->
<div class="ctrl-bar">
  <span class="ctrl-label">한 번에 굴리기</span>
  <input type="range" id="nRange" min="1" max="1000" value="1" oninput="updateN(this.value)">
  <span class="n-val" id="nVal">1회</span>
  <span class="total-label">누적: <span class="total-num" id="totalCount">0</span>번</span>
  <button class="btn btn-roll" id="rollBtn" onclick="doRoll()">🎲 굴리기!</button>
  <button class="btn btn-reset" onclick="resetStats()">↺ 초기화</button>
</div>

<!-- 굴리기 결과 -->
<div class="roll-box">
  <div class="roll-prompt" id="rollPrompt">위에서 주사위를 선택하고 굴려보세요!</div>
  <div id="rollAnim">🎲</div>
  <div id="rollResult"></div>
  <div id="rollLabel"></div>
</div>

<!-- 누적 통계 -->
<div class="stats-wrap" id="statsWrap">
  <div class="stats-hdr">
    <span class="stats-title">📊 누적 통계</span>
    <span class="stats-count" id="statsCount"></span>
  </div>
  <div id="barsArea"></div>
</div>

<!-- 인사이트 패널 -->
<div class="insight" id="insightBox">
  <div class="ins-title" id="insTitle"></div>
  <div id="insBody"></div>
</div>

<script>
// ──────────────────────────────────────────────────────────
// 주사위 데이터
// ──────────────────────────────────────────────────────────
const DICE = [
  {
    id: "cube",
    name: "정육면체",
    sub: "일반 주사위 (6면)",
    faces: ["1","2","3","4","5","6"],
    probs: [1/6,1/6,1/6,1/6,1/6,1/6],
    colors: ["#3b82f6","#60a5fa","#93c5fd","#2563eb","#1d4ed8","#3b82f6"],
    works: true,
    insight: {
      cls: "ins-ok",
      title: "✅ 수학적 확률 성립!",
      body: "정육면체의 6개 면은 넓이가 모두 동일합니다.<br>" +
            "따라서 각 근원사건이 일어날 확률이 모두 <b>1/6로 동일</b>합니다.<br>" +
            "→ 수학적 확률을 정의할 수 있습니다."
    },
    svgHtml: `<svg viewBox="0 0 100 92" xmlns="http://www.w3.org/2000/svg">
  <polygon points="50,4 92,26 50,48 8,26" fill="#60a5fa" stroke="#1d4ed8" stroke-width="1.5"/>
  <polygon points="8,26 50,48 50,88 8,66" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
  <polygon points="92,26 50,48 50,88 92,66" fill="#1e40af" stroke="#1d4ed8" stroke-width="1.5"/>
  <circle cx="50" cy="26" r="5" fill="white" opacity=".85"/>
  <circle cx="26" cy="53" r="3.5" fill="white" opacity=".8"/>
  <circle cx="34" cy="74" r="3.5" fill="white" opacity=".8"/>
  <circle cx="66" cy="53" r="3.5" fill="white" opacity=".8"/>
  <circle cx="74" cy="74" r="3.5" fill="white" opacity=".8"/>
</svg>`
  },
  {
    id: "frustum",
    name: "사각뿔대",
    sub: "위아래 크기가 다른 육면체",
    faces: ["위면(1)","앞면(2)","오른면(3)","뒷면(4)","왼면(5)","아래면(6)"],
    probs: [0.04, 0.165, 0.165, 0.165, 0.165, 0.30],
    colors: ["#fbbf24","#fb923c","#f97316","#ea580c","#dc2626","#ef4444"],
    works: false,
    insight: {
      cls: "ins-warn",
      title: "⚠️ 수학적 확률 불성립!",
      body: "사각뿔대는 면마다 넓이가 다릅니다.<br>" +
            "▸ <b>아래면(6)</b>: 면적 가장 큼 → 가장 자주 나옴<br>" +
            "▸ <b>위면(1)</b>: 면적 가장 작음 → 거의 안 나옴<br>" +
            "→ 각 근원사건의 확률이 <b>동일하지 않아</b> 수학적 확률을 정의할 수 없습니다."
    },
    svgHtml: `<svg viewBox="0 0 100 96" xmlns="http://www.w3.org/2000/svg">
  <polygon points="30,6 70,6 70,18 30,18" fill="#fbbf24" stroke="#b45309" stroke-width="1.5"/>
  <polygon points="4,92 96,92 96,78 4,78" fill="#ef4444" stroke="#991b1b" stroke-width="1.5"/>
  <polygon points="4,78 30,18 30,6 4,66" fill="#f97316" stroke="#c2410c" stroke-width="1.5"/>
  <polygon points="96,78 70,18 70,6 96,66" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
  <polygon points="4,78 96,78 70,18 30,18" fill="#fb923c" stroke="#c2410c" stroke-width="1.5"/>
  <text x="50" y="14" text-anchor="middle" fill="#1c1917" font-size="7" font-weight="bold">작은 면</text>
  <text x="50" y="88" text-anchor="middle" fill="white" font-size="7" font-weight="bold">큰 면</text>
  <line x1="10" y1="50" x2="20" y2="50" stroke="#fbbf24" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="22" y="53" fill="#fbbf24" font-size="6">넓이 불균등</text>
</svg>`
  },
  {
    id: "sphere",
    name: "구형",
    sub: "공 모양 주사위 (6구역)",
    faces: ["1구역","2구역","3구역","4구역","5구역","6구역","⚡경계"],
    probs: [0.155,0.155,0.155,0.155,0.155,0.155,0.07],
    colors: ["#a855f7","#9333ea","#7c3aed","#6d28d9","#5b21b6","#4c1d95","#ec4899"],
    works: false,
    insight: {
      cls: "ins-bad",
      title: "❗ 두 가지 심각한 문제!",
      body: "① <b>경계 문제</b>: 구역을 나누는 선이 바닥에 닿으면 두 사건이 동시에 발생합니다.<br>" +
            "→ 근원사건들이 <b>배반관계</b>가 아닐 수 있습니다.<br>" +
            "② <b>정의 불가</b>: '경계에 걸침'은 어느 사건에도 속하지 않는 애매한 결과입니다.<br>" +
            "→ 수학적 확률의 기본 전제가 모두 무너집니다."
    },
    svgHtml: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="sphG" cx="35%" cy="32%">
      <stop offset="0%" stop-color="white" stop-opacity=".35"/>
      <stop offset="100%" stop-color="black" stop-opacity=".25"/>
    </radialGradient>
    <clipPath id="sphClip"><circle cx="50" cy="50" r="43"/></clipPath>
  </defs>
  <circle cx="50" cy="50" r="43" fill="#9333ea" stroke="#6d28d9" stroke-width="1.5"/>
  <circle cx="50" cy="50" r="43" fill="url(#sphG)"/>
  <ellipse cx="50" cy="50" rx="43" ry="12" fill="none" stroke="#c084fc" stroke-width="1.3" opacity=".7" clip-path="url(#sphClip)"/>
  <line x1="50" y1="7" x2="50" y2="93" stroke="#c084fc" stroke-width="1.3" opacity=".7"/>
  <path d="M 12 28 Q 50 50 88 72" fill="none" stroke="#c084fc" stroke-width="1.3" opacity=".7"/>
  <text x="30" y="34" fill="white" font-size="10" font-weight="bold" opacity=".9">1</text>
  <text x="60" y="34" fill="white" font-size="10" font-weight="bold" opacity=".9">2</text>
  <text x="26" y="57" fill="white" font-size="10" font-weight="bold" opacity=".9">3</text>
  <text x="56" y="57" fill="white" font-size="10" font-weight="bold" opacity=".9">4</text>
  <text x="30" y="78" fill="white" font-size="10" font-weight="bold" opacity=".9">5</text>
  <text x="62" y="78" fill="white" font-size="10" font-weight="bold" opacity=".9">6</text>
  <text x="70" y="20" fill="#f472b6" font-size="15" opacity=".95">⚡</text>
</svg>`
  },
  {
    id: "octa",
    name: "정팔면체",
    sub: "정삼각형 8면체",
    faces: ["1","2","3","4","5","6","7","8"],
    probs: [1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8],
    colors: ["#10b981","#34d399","#6ee7b7","#10b981","#059669","#10b981","#34d399","#059669"],
    works: true,
    insight: {
      cls: "ins-ok",
      title: "✅ 수학적 확률 성립!",
      body: "정팔면체는 <b>8개의 정삼각형</b>으로 이루어집니다.<br>" +
            "모든 면의 넓이가 동일하여 각 근원사건의 확률이 <b>1/8로 동일</b>합니다.<br>" +
            "→ 표본공간은 {1,2,3,4,5,6,7,8}, 수학적 확률 성립!"
    },
    svgHtml: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <polygon points="50,4 12,56 88,56" fill="#34d399" stroke="#065f46" stroke-width="1.5"/>
  <polygon points="50,96 12,56 88,56" fill="#10b981" stroke="#065f46" stroke-width="1.5"/>
  <polygon points="50,4 12,56 50,40" fill="#6ee7b7" stroke="#065f46" stroke-width="1" opacity=".6"/>
  <polygon points="50,4 88,56 50,40" fill="#059669" stroke="#065f46" stroke-width="1" opacity=".6"/>
  <line x1="50" y1="4" x2="50" y2="96" stroke="#065f46" stroke-width="1" opacity=".4"/>
  <line x1="12" y1="56" x2="88" y2="56" stroke="#065f46" stroke-width="1" opacity=".4"/>
  <text x="36" y="40" fill="white" font-size="10" font-weight="bold">1</text>
  <text x="56" y="40" fill="white" font-size="10" font-weight="bold">2</text>
  <text x="22" y="55" fill="white" font-size="9" opacity=".6">3</text>
  <text x="72" y="55" fill="white" font-size="9" opacity=".6">4</text>
  <text x="36" y="76" fill="white" font-size="10" font-weight="bold">5</text>
  <text x="56" y="76" fill="white" font-size="10" font-weight="bold">6</text>
  <text x="24" y="68" fill="#a7f3d0" font-size="8" opacity=".5">7</text>
  <text x="68" y="68" fill="#a7f3d0" font-size="8" opacity=".5">8</text>
</svg>`
  }
];

// ──────────────────────────────────────────────────────────
// 상태
// ──────────────────────────────────────────────────────────
let selId    = null;
let counts   = {};
let total    = 0;
let rolling  = false;
let curN     = 1;

// ──────────────────────────────────────────────────────────
// 초기화
// ──────────────────────────────────────────────────────────
(function init() {
  const grid = document.getElementById('diceGrid');
  DICE.forEach(d => {
    const card = document.createElement('div');
    card.className = 'dice-card';
    card.id = 'card-' + d.id;
    card.onclick = () => selectDice(d.id);
    card.innerHTML = d.svgHtml +
      `<div class="dice-name">${d.name}</div>` +
      `<div class="dice-sub">${d.sub}</div>`;
    grid.appendChild(card);
  });
})();

// ──────────────────────────────────────────────────────────
// 주사위 선택
// ──────────────────────────────────────────────────────────
function selectDice(id) {
  selId = id;
  document.querySelectorAll('.dice-card').forEach(c => c.classList.remove('selected'));
  document.getElementById('card-' + id).classList.add('selected');
  resetStats(false);

  const d = DICE.find(x => x.id === id);
  setPrompt(`${d.name}을(를) 선택했습니다. 굴려보세요! 🎲`);
  hide('rollResult'); hide('rollLabel'); hide('rollAnim');
  show('rollPrompt');
}

// ──────────────────────────────────────────────────────────
// 리셋
// ──────────────────────────────────────────────────────────
function resetStats(resetPrompt = true) {
  if (!selId) return;
  const d = DICE.find(x => x.id === selId);
  counts = {};
  d.faces.forEach(f => counts[f] = 0);
  total = 0;
  document.getElementById('totalCount').textContent = '0';
  document.getElementById('statsWrap').style.display = 'none';
  document.getElementById('insightBox').style.display = 'none';
  if (resetPrompt) setPrompt('위에서 주사위를 선택하고 굴려보세요!');
}

// ──────────────────────────────────────────────────────────
// N 슬라이더
// ──────────────────────────────────────────────────────────
function updateN(v) {
  curN = parseInt(v);
  document.getElementById('nVal').textContent = curN >= 1000 ? '1000회' : curN + '회';
}

// ──────────────────────────────────────────────────────────
// 굴리기
// ──────────────────────────────────────────────────────────
function doRoll() {
  if (!selId) { alert('먼저 주사위를 선택하세요!'); return; }
  if (rolling) return;
  rolling = true;
  const btn = document.getElementById('rollBtn');
  btn.disabled = true;

  const d = DICE.find(x => x.id === selId);

  if (curN <= 10) {
    // 애니메이션
    hide('rollPrompt'); hide('rollResult'); hide('rollLabel');
    const animEl = document.getElementById('rollAnim');
    animEl.textContent = d.id === 'sphere' ? '🔴' :
                         d.id === 'frustum' ? '🔺' :
                         d.id === 'octa' ? '💎' : '🎲';
    show('rollAnim');

    setTimeout(() => {
      let last = '';
      for (let i = 0; i < curN; i++) {
        last = pick(d.faces, d.probs);
        counts[last]++;
      }
      total += curN;
      hide('rollAnim');

      const rEl = document.getElementById('rollResult');
      const lEl = document.getElementById('rollLabel');
      const isBoundary = (last === '⚡경계');

      rEl.style.color = '#a78bfa';
      if (isBoundary) {
        rEl.innerHTML = '<span class="boundary-result">⚡ 경계!</span>';
      } else {
        rEl.textContent = last;
        const idx = d.faces.indexOf(last);
        rEl.style.color = d.colors[idx] || '#a78bfa';
      }
      show('rollResult');

      lEl.innerHTML = curN === 1
        ? (isBoundary
          ? '<span style="color:#ec4899">두 구역 경계에 걸쳤습니다!</span>'
          : `"${last}" 이(가) 나왔습니다`)
        : `${curN}번 굴렸습니다 (마지막: ${last})`;
      show('rollLabel');

      document.getElementById('totalCount').textContent = total;
      renderStats(d);
      rolling = false;
      btn.disabled = false;
    }, 550);

  } else {
    // 즉시 다량 처리
    hide('rollPrompt'); hide('rollAnim');
    for (let i = 0; i < curN; i++) counts[pick(d.faces, d.probs)]++;
    total += curN;

    const rEl = document.getElementById('rollResult');
    rEl.textContent = `+${curN}번!`;
    rEl.style.color = '#a78bfa';
    show('rollResult');
    const lEl = document.getElementById('rollLabel');
    lEl.textContent = `총 ${total}번 굴렸습니다`;
    show('rollLabel');

    document.getElementById('totalCount').textContent = total;
    renderStats(d);
    rolling = false;
    btn.disabled = false;
  }
}

// ──────────────────────────────────────────────────────────
// 가중 랜덤
// ──────────────────────────────────────────────────────────
function pick(faces, probs) {
  const r = Math.random();
  let cum = 0;
  for (let i = 0; i < probs.length; i++) {
    cum += probs[i];
    if (r < cum) return faces[i];
  }
  return faces[faces.length - 1];
}

// ──────────────────────────────────────────────────────────
// 통계 렌더링
// ──────────────────────────────────────────────────────────
function renderStats(d) {
  const wrap = document.getElementById('statsWrap');
  const area = document.getElementById('barsArea');
  wrap.style.display = 'block';
  document.getElementById('statsCount').textContent = `총 ${total}번`;

  const idealPct = (1 / d.faces.length * 100);
  let html = '';

  d.faces.forEach((face, i) => {
    const cnt   = counts[face] || 0;
    const pct   = total > 0 ? cnt / total * 100 : 0;
    const w     = Math.min(pct, 100).toFixed(1);
    const color = d.colors[i] || '#a78bfa';
    const isBnd = face === '⚡경계';
    const bg    = isBnd ? 'linear-gradient(90deg,#7c3aed,#ec4899)' : color;
    const idealW = Math.min(idealPct, 100).toFixed(1);

    html += `<div class="bar-row">
      <div class="bar-meta">
        <span style="color:${isBnd?'#f472b6':color}">${face}</span>
        <span>${cnt}회 (${pct.toFixed(1)}%)</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill" style="width:${w}%;background:${bg}">
          ${parseFloat(w) > 9 ? pct.toFixed(1)+'%' : ''}
        </div>
        <div class="bar-ideal" style="left:${idealW}%">
          <span class="ideal-tip">이론</span>
        </div>
      </div>
    </div>`;
  });

  html += `<div class="ideal-note">흰 선 = 균등 이론 확률 (${idealPct.toFixed(1)}%)</div>`;
  area.innerHTML = html;

  if (total >= 30) renderInsight(d);
}

// ──────────────────────────────────────────────────────────
// 인사이트 패널
// ──────────────────────────────────────────────────────────
function renderInsight(d) {
  const box = document.getElementById('insightBox');
  box.className = 'insight ' + d.insight.cls;
  document.getElementById('insTitle').textContent = d.insight.title;

  let body = d.insight.body;
  if (d.id === 'sphere') {
    const bndCnt = counts['⚡경계'] || 0;
    if (bndCnt > 0) {
      body += `<br><br>🔍 <b>실제 경계 발생: ${bndCnt}번</b> `
            + `(전체의 ${(bndCnt/total*100).toFixed(1)}%)`;
    }
  }
  document.getElementById('insBody').innerHTML = body;
  box.style.display = 'block';
}

// ──────────────────────────────────────────────────────────
// 헬퍼
// ──────────────────────────────────────────────────────────
function show(id){ document.getElementById(id).style.display = 'block'; }
function hide(id){ document.getElementById(id).style.display = 'none'; }
function setPrompt(t){ document.getElementById('rollPrompt').textContent = t; }
</script>
</body>
</html>"""


def render():
    st.subheader("🎲 이상한 주사위와 수학적 확률")
    components.html(_HTML, height=1400, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
