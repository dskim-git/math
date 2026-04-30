# activities/common/mini/matrix_ops_explore.py
"""
행렬 연산 탐험 – 합·차·실수배
3×3 행렬의 괄호 표기와 성분별 계산 과정을 직접 보고, 2×2 챌린지로 실력을 확인하는 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "행렬연산탐험"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 '행렬 연산 탐험' 활동을 마치고 배운 내용을 정리해보세요**"},
    {"key": "덧셈뺄셈",
     "label": "1️⃣ 행렬의 덧셈과 뺄셈이 가능한 조건은 무엇인가요? 자신이 만든 예시를 들어 계산 방법을 설명해보세요.",
     "type": "text_area", "height": 100},
    {"key": "실수배",
     "label": "2️⃣ 행렬의 실수배란 무엇인가요? k(A+B)=kA+kB가 성립함을 예시 행렬로 직접 확인해보세요.",
     "type": "text_area", "height": 110},
    {"key": "발견점",
     "label": "3️⃣ 챌린지 중 가장 어렵거나 실수하기 쉬운 유형은 무엇이었나요? 그 이유와 주의할 점을 써보세요.",
     "type": "text_area", "height": 100},
    {"key": "새롭게알게된점",
     "label": "💡 이 활동을 통해 새롭게 알게 된 점",
     "type": "text_area", "height": 90},
    {"key": "느낀점",
     "label": "💬 이 활동을 하면서 느낀 점",
     "type": "text_area", "height": 90},
]

META = {
    "title":       "🔢 행렬 연산 탐험",
    "description": "3×3 행렬의 합·차·실수배를 성분별로 확인하고, 2×2 챌린지로 직접 계산하는 활동",
    "order":       3,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>행렬 연산 탐험</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#060c18;color:#bdd1e8;padding:10px;min-height:100vh}

/* ── tabs ── */
.tabs{display:flex;gap:6px;margin-bottom:12px}
.tb{flex:1;padding:9px 4px;text-align:center;border-radius:10px;border:1.5px solid #152035;
  background:#0a1525;color:#3d5878;font-size:.8rem;font-weight:700;cursor:pointer;transition:all .2s}
.tb.on{background:linear-gradient(135deg,#0369a1,#4f46e5);color:#fff;border-color:transparent;
  box-shadow:0 3px 14px rgba(3,105,161,.35)}
.panel{display:none}.panel.on{display:block}

/* ── op buttons ── */
.op-row{display:flex;gap:6px;justify-content:center;margin:0 0 12px}
.ob{padding:8px 18px;border-radius:9px;border:1.5px solid #1a3050;background:#0a1828;
  color:#3d6080;font-size:.88rem;font-weight:700;cursor:pointer;transition:all .18s;
  font-family:'Courier New',monospace}
.ob.on{background:linear-gradient(135deg,#0c4a6e,#312e81);color:#7dd3fc;border-color:#0369a1}
.ob:hover:not(.on){background:#0f2035;color:#7dd3fc}

/* ── matrix equation layout ── */
.mat-eq{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;margin:10px 0}
.mat-block{display:flex;flex-direction:column;align-items:center;gap:4px}
.mat-name{font-size:.75rem;font-weight:800;letter-spacing:.08em;text-align:center}
.mat-wrap{display:inline-flex;align-items:stretch}
.mat-bl,.mat-br{width:8px;flex-shrink:0}
.mat-bl{border-top:2.5px solid currentColor;border-bottom:2.5px solid currentColor;
  border-left:2.5px solid currentColor;border-radius:4px 0 0 4px}
.mat-br{border-top:2.5px solid currentColor;border-bottom:2.5px solid currentColor;
  border-right:2.5px solid currentColor;border-radius:0 4px 4px 0}
.mat-grid{display:grid;gap:4px;padding:6px 5px}
.mc{width:38px;height:32px;display:flex;align-items:center;justify-content:center;
  background:#0d1e30;border:1px solid #1a3050;border-radius:4px;
  font-size:.95rem;font-weight:700;color:#e2e8f0;font-family:'Courier New',monospace}
.mc.res{border-color:#1e4a35;background:#0a1e14;color:#6ee7b7}
.op-big{font-size:1.8rem;font-weight:900;color:#f59e0b;align-self:center}
.eq-big{font-size:1.6rem;font-weight:900;color:#64748b;align-self:center}
.k-badge{font-size:1.2rem;font-weight:900;color:#fbbf24;font-family:'Courier New',monospace;
  background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);
  border-radius:8px;padding:6px 14px;align-self:center}

/* ── picker buttons ── */
.picker-row{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin:0 0 10px}
.pc-btn{cursor:pointer;background:#0d1e30;border:1.5px solid #1a3050;border-radius:8px;
  padding:5px 10px;transition:all .18s;font-size:.75rem;font-weight:700;
  font-family:'Courier New',monospace;color:#475569;text-align:center;line-height:1.6}
.pc-btn.a-on{border-color:#f59e0b;background:rgba(245,158,11,.08);color:#fbbf24}
.pc-btn.b-on{border-color:#a78bfa;background:rgba(167,139,250,.08);color:#a78bfa}
.pc-btn:hover:not(.a-on):not(.b-on){border-color:#2a4060;color:#7dd3fc}

/* ── k slider ── */
.ctrl{background:#0a1525;border:1px solid #152035;border-radius:10px;padding:10px 14px;margin:10px 0}
.ctitle{font-size:.72rem;color:#64748b;font-weight:700;margin-bottom:6px}
.k-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.kv{font-size:1.2rem;font-weight:900;color:#fbbf24;min-width:40px;text-align:right}
.kv.pop{animation:kpop .2s ease-out}
@keyframes kpop{0%{transform:scale(1)}40%{transform:scale(1.45)}100%{transform:scale(1)}}
input[type=range]{width:100%;accent-color:#38bdf8;height:4px;cursor:pointer}
.ticks{display:flex;justify-content:space-between;font-size:.6rem;color:#334155;margin-top:3px}

/* ── computation steps ── */
.steps-wrap{background:#0a1525;border:1px solid #152035;border-radius:10px;padding:10px 12px;margin:10px 0}
.steps-title{font-size:.7rem;color:#64748b;font-weight:700;margin-bottom:8px;letter-spacing:.06em}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(135px,1fr));gap:5px}
.step-item{background:#060c18;border:1px solid #152035;border-radius:6px;
  padding:5px 8px;font-size:.72rem;font-family:'Courier New',monospace;line-height:1.7}
.si-pos{color:#64748b;font-size:.62rem}
.si-val{color:#e2e8f0}
.si-res{color:#4ade80;font-weight:700}

/* ── formula strip ── */
.fml{background:#0a1525;border:1px solid #152035;border-left:3px solid #0369a1;
  border-radius:0 8px 8px 0;padding:8px 12px;font-size:.76rem;
  color:#94a3b8;font-family:'Courier New',monospace;margin:8px 0;line-height:1.8}
.fl{color:#7dd3fc;font-weight:700}.fl2{color:#fbbf24;font-weight:700}.fl3{color:#a78bfa;font-weight:700}

/* ── challenge header ── */
.ch-hdr{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.ch-num{font-size:.85rem;font-weight:900;color:#fbbf24;background:rgba(251,191,36,.12);
  border-radius:6px;padding:3px 10px}
.ch-dots{display:flex;gap:4px;margin-left:auto}
.cdot{width:9px;height:9px;border-radius:50%;background:#152035;transition:all .3s}
.cdot.done{background:#22c55e;box-shadow:0 0 5px rgba(34,197,94,.5)}
.cdot.cur{background:#38bdf8;transform:scale(1.3)}
.ch-banner{background:rgba(0,80,160,.12);border:1px solid rgba(0,150,255,.18);
  border-radius:10px;padding:9px 13px;font-size:.8rem;color:#94a3b8;
  line-height:1.55;margin-bottom:12px}
.op-tag{font-size:.72rem;font-weight:800;color:#f59e0b;margin-right:6px}
.pcard{background:#0a1525;border:1px solid #1e3a5c;border-radius:12px;padding:12px}
.ptitle{font-size:.85rem;color:#7dd3fc;font-weight:800;margin-bottom:10px;
  display:flex;align-items:center;gap:6px}
.ptitle::before{content:'';display:block;width:4px;height:15px;background:#38bdf8;border-radius:2px}

/* ── answer input ── */
.ac{width:38px;height:32px;background:rgba(0,50,30,.6);border:2px solid #065f46;
  border-radius:4px;font-size:.9rem;font-weight:700;color:#6ee7b7;
  text-align:center;outline:none;font-family:'Courier New',monospace;
  transition:border-color .2s,background .2s}
.ac:focus{border-color:#10b981;box-shadow:0 0 10px rgba(16,185,129,.4);background:rgba(0,70,45,.8)}
.ac.ok{border-color:#22c55e!important;background:rgba(34,197,94,.2)!important;color:#bbf7d0!important}
.ac.bad{border-color:#ef4444!important;background:rgba(239,68,68,.15)!important;
  color:#fca5a5!important;animation:shk .35s}
@keyframes shk{0%,100%{transform:translateX(0)}25%,75%{transform:translateX(-4px)}50%{transform:translateX(4px)}}

/* ── feedback ── */
.result-msg{text-align:center;font-size:.82rem;font-weight:700;padding:8px 12px;
  border-radius:8px;margin-top:8px;display:none}
.result-msg.ok{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.3)}
.result-msg.bad{background:rgba(239,68,68,.12);color:#f87171;border:1px solid rgba(239,68,68,.3)}
.hint-box{display:none;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);
  border-radius:8px;padding:7px 12px;font-size:.75rem;color:#fcd34d;margin-top:6px;line-height:1.6}

/* ── buttons ── */
.btn-row{display:flex;gap:8px;justify-content:center;margin-top:12px}
.btn{padding:9px 22px;border-radius:9px;border:none;cursor:pointer;font-size:.85rem;font-weight:800;transition:all .18s}
.btn-check{background:linear-gradient(135deg,#0ea5e9,#6366f1);color:#fff;box-shadow:0 4px 14px rgba(14,165,233,.3)}
.btn-check:hover{transform:translateY(-2px)}
.btn-next{background:linear-gradient(135deg,#10b981,#059669);color:#fff;display:none;box-shadow:0 4px 14px rgba(16,185,129,.3)}
.btn-next:hover{transform:translateY(-2px)}

/* ── fin ── */
.fin{display:none;text-align:center;padding:20px;background:rgba(251,191,36,.05);
  border:1px solid rgba(251,191,36,.25);border-radius:14px;margin-top:10px}
.fin-ico{font-size:2.5rem;margin-bottom:6px;animation:bounce 1s ease infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.fin-ttl{font-size:1.2rem;font-weight:900;color:#fbbf24;margin-bottom:4px}
.fin-sub{font-size:.78rem;color:#94a3b8}

/* ── particles ── */
.pt{position:fixed;pointer-events:none;border-radius:50%;z-index:999;animation:ptf .9s ease-out forwards}
@keyframes ptf{0%{opacity:1;transform:translate(0,0) scale(1)}100%{opacity:0;transform:translate(var(--tx),var(--ty)) scale(0)}}
</style>
</head>
<body>

<div class="tabs">
  <div class="tb on" id="tb-exp" onclick="switchTab('exp')">🔢 행렬 연산 탐험</div>
  <div class="tb"    id="tb-ch"  onclick="switchTab('ch')">✏️ 계산 챌린지</div>
</div>

<!-- ═══════════ EXPLORE ═══════════ -->
<div class="panel on" id="panel-exp">
  <div class="op-row">
    <button class="ob on" id="ob-kA"  onclick="setOp('kA')">k × A</button>
    <button class="ob"    id="ob-add" onclick="setOp('add')">A + B</button>
    <button class="ob"    id="ob-sub" onclick="setOp('sub')">A − B</button>
  </div>

  <div class="picker-row" id="a-picker"></div>
  <div class="mat-eq" id="mat-eq-area"></div>
  <div id="k-ctrl-area"></div>
  <div id="b-ctrl-area"></div>

  <div class="steps-wrap">
    <div class="steps-title">📐 성분별 계산 과정</div>
    <div class="steps-grid" id="steps-grid"></div>
  </div>
  <div class="fml" id="exp-fml"></div>
</div>

<!-- ═══════════ CHALLENGE ═══════════ -->
<div class="panel" id="panel-ch">
  <div class="ch-hdr">
    <span class="ch-num" id="ch-num">미션 1 / 6</span>
    <div class="ch-dots" id="ch-dots"></div>
  </div>
  <div class="ch-banner" id="ch-banner"></div>
  <div class="pcard">
    <div class="ptitle" id="ch-ptitle"></div>
    <div class="mat-eq" id="ch-mat-eq"></div>
    <div class="result-msg" id="result-msg"></div>
    <div class="hint-box"   id="hint-box"></div>
    <div class="btn-row">
      <button class="btn btn-check" id="checkBtn" onclick="checkAnswer()">✓ 정답 확인</button>
      <button class="btn btn-next"  id="nextBtn"  onclick="nextCh()">다음 문제 ▶</button>
    </div>
  </div>
  <div class="fin" id="fin-box">
    <div class="fin-ico">🏅</div>
    <div class="fin-ttl">전체 챌린지 클리어!</div>
    <div class="fin-sub">행렬의 합·차·실수배를 모두 정복했습니다!<br>아래 성찰을 작성해보세요.</div>
  </div>
</div>

<script>
/* ═══ DATA ═══ */
// 3×3 presets for exploration
const PA = {
  'A₁': [[2,1,-1],[0,3,2],[-1,1,4]],
  'A₂': [[3,0,2],[1,-2,1],[0,3,-1]],
  'A₃': [[-1,2,0],[4,-1,3],[2,0,-2]],
};
const PB = {
  'B₁': [[1,2,3],[1,1,0],[2,-1,1]],
  'B₂': [[-2,1,0],[3,-1,2],[0,1,-3]],
  'B₃': [[2,-1,2],[0,2,1],[1,0,2]],
};
const KVALS = [-2,-1,0,0.5,1,2,3];
const KDEF  = 4; // index of k=1

// 2×2 challenge problems
const CHAL = [
  { type:'add', label:'➕ 행렬의 합',
    story:'두 행렬을 더하세요. 같은 행·열 위치의 성분끼리 더합니다.',
    title:'A + B = ?',
    A:[[3,1],[2,4]], B:[[1,5],[3,2]], ans:[[4,6],[5,6]],
    hint:'C[i][j] = A[i][j] + B[i][j] → 3+1=4, 1+5=6, 2+3=5, 4+2=6' },
  { type:'add', label:'➕ 행렬의 합 (음수 포함)',
    story:'음수 성분이 섞인 덧셈입니다. 부호를 꼼꼼히 확인하세요.',
    title:'A + B = ?',
    A:[[5,-2],[0,7]], B:[[-3,4],[1,-5]], ans:[[2,2],[1,2]],
    hint:'5+(−3)=2, (−2)+4=2, 0+1=1, 7+(−5)=2' },
  { type:'sub', label:'➖ 행렬의 차',
    story:'두 행렬을 빼세요. 같은 위치의 성분끼리 뺍니다.',
    title:'A − B = ?',
    A:[[7,3],[5,9]], B:[[2,1],[3,4]], ans:[[5,2],[2,5]],
    hint:'C[i][j] = A[i][j] − B[i][j] → 7-2=5, 3-1=2, 5-3=2, 9-4=5' },
  { type:'sub', label:'➖ 행렬의 차 (음수 주의)',
    story:'a − (−b) = a + b 임을 잊지 마세요!',
    title:'A − B = ?',
    A:[[4,-1],[0,6]], B:[[-2,3],[4,-2]], ans:[[6,-4],[-4,8]],
    hint:'4−(−2)=6, (−1)−3=−4, 0−4=−4, 6−(−2)=8' },
  { type:'scalar', k:3, label:'✖️ 실수배 (k=3)',
    story:'행렬의 모든 성분에 k=3을 곱하세요. 이것이 실수배입니다.',
    title:'3A = ?',
    A:[[2,-1],[0,4]], ans:[[6,-3],[0,12]],
    hint:'3×2=6, 3×(−1)=−3, 3×0=0, 3×4=12' },
  { type:'scalar', k:-1, label:'✖️ 실수배 (k=−1)',
    story:'(−1)A는 모든 성분의 부호를 반전해 −A를 만듭니다.',
    title:'(−1)A = ?',
    A:[[4,2],[-3,1]], ans:[[-4,-2],[3,-1]],
    hint:'(−1)×4=−4, (−1)×2=−2, (−1)×(−3)=3, (−1)×1=−1' },
];

/* ═══ STATE ═══ */
let expAKey = 'A₁', expBKey = 'B₁', expOp = 'kA', expKIdx = KDEF;
let chIdx = 0, chTries = 0;

/* ═══ MATRIX HTML HELPERS ═══ */
function mkMat(mat, color, resCls) {
  const cols = mat[0].length;
  const cells = mat.map(row =>
    row.map(v => `<div class="mc${resCls?' '+resCls:''}">${v}</div>`).join('')
  ).join('');
  return `<div class="mat-wrap" style="color:${color}">
    <div class="mat-bl"></div>
    <div class="mat-grid" style="grid-template-columns:repeat(${cols},38px)">${cells}</div>
    <div class="mat-br"></div>
  </div>`;
}

function mkAns(rows, cols) {
  let cells = '';
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++)
      cells += `<input class="ac" id="ans_${r}_${c}" type="text" maxlength="5"
        autocomplete="off" inputmode="numeric">`;
  return `<div class="mat-wrap" style="color:#10b981">
    <div class="mat-bl"></div>
    <div class="mat-grid" style="grid-template-columns:repeat(${cols},38px)">${cells}</div>
    <div class="mat-br"></div>
  </div>`;
}

function blk(label, color, inner) {
  return `<div class="mat-block">
    <div class="mat-name" style="color:${color}">${label}</div>${inner}
  </div>`;
}

/* ═══ EXPLORE ═══ */
function buildAPicker() {
  document.getElementById('a-picker').innerHTML =
    Object.keys(PA).map(key =>
      `<div class="pc-btn${key===expAKey?' a-on':''}" onclick="selectA('${key}')">
        ${key}<br><span style="font-size:.6rem;color:#475569">[${PA[key][0].join(', ')} …]</span>
      </div>`
    ).join('');
}

function selectA(key) { expAKey = key; buildAPicker(); renderExplore(); }
function selectB(key) { expBKey = key; buildBCtrl();   renderExplore(); }

function buildBCtrl() {
  const title = expOp === 'add' ? '더할 행렬 B 선택' : '뺄 행렬 B 선택';
  document.getElementById('b-ctrl-area').innerHTML =
    `<div class="ctrl"><div class="ctitle">${title}</div>
     <div class="picker-row">${
       Object.keys(PB).map(bk =>
         `<div class="pc-btn${bk===expBKey?' b-on':''}" onclick="selectB('${bk}')">
           ${bk}<br><span style="font-size:.6rem;color:#475569">[${PB[bk][0].join(', ')} …]</span>
         </div>`
       ).join('')
     }</div></div>`;
}

function setOp(op) {
  expOp = op;
  ['kA','add','sub'].forEach(o =>
    document.getElementById('ob-'+o).classList.toggle('on', o === op));

  if (op === 'kA') {
    document.getElementById('k-ctrl-area').innerHTML =
      `<div class="ctrl">
        <div class="k-row">
          <span class="ctitle">스칼라 k 값 조절</span>
          <span class="kv" id="kv">${KVALS[expKIdx]}</span>
        </div>
        <input type="range" id="k-sl" min="0" max="6" step="1" value="${expKIdx}"
          oninput="onKSlide(this.value)">
        <div class="ticks">
          <span>−2</span><span>−1</span><span>0</span><span>½</span>
          <span>1</span><span>2</span><span>3</span>
        </div>
      </div>`;
    document.getElementById('b-ctrl-area').innerHTML = '';
  } else {
    document.getElementById('k-ctrl-area').innerHTML = '';
    buildBCtrl();
  }
  renderExplore();
}

function onKSlide(val) {
  expKIdx = parseInt(val);
  const k = KVALS[expKIdx];
  const el = document.getElementById('kv');
  el.textContent = k;
  el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');
  renderExplore();
}

function renderExplore() {
  const A = PA[expAKey], B = PB[expBKey], k = KVALS[expKIdx];
  const C = A.map((row, r) => row.map((v, c) => {
    if (expOp === 'kA')  return Math.round(k * v * 100) / 100;
    if (expOp === 'add') return v + B[r][c];
    return v - B[r][c];
  }));
  const rows = A.length, cols = A[0].length;

  // Matrix equation
  let eq = '';
  if (expOp === 'kA') {
    eq += `<div class="k-badge">k = ${k}</div>`;
    eq += `<div class="op-big">×</div>`;
    eq += blk('A', '#38bdf8', mkMat(A, '#38bdf8', ''));
    eq += `<div class="eq-big">=</div>`;
    eq += blk('C = kA', '#22c55e', mkMat(C, '#22c55e', 'res'));
  } else {
    eq += blk('A', '#38bdf8', mkMat(A, '#38bdf8', ''));
    eq += `<div class="op-big">${expOp === 'add' ? '+' : '−'}</div>`;
    eq += blk('B', '#a78bfa', mkMat(B, '#a78bfa', ''));
    eq += `<div class="eq-big">=</div>`;
    eq += blk(expOp === 'add' ? 'C = A+B' : 'C = A−B', '#22c55e', mkMat(C, '#22c55e', 'res'));
  }
  document.getElementById('mat-eq-area').innerHTML = eq;

  // Step-by-step computation
  let steps = '';
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const av = A[r][c], cv = C[r][c];
      let calc = '';
      if (expOp === 'kA') {
        calc = `${k} × ${av} = <span class="si-res">${cv}</span>`;
      } else {
        const bv = B[r][c];
        const sign = expOp === 'add' ? '+' : '−';
        const bshow = (expOp === 'sub' && bv < 0) ? `(${bv})` : `${bv}`;
        calc = `${av} ${sign} ${bshow} = <span class="si-res">${cv}</span>`;
      }
      steps += `<div class="step-item">
        <div class="si-pos">C[${r+1}][${c+1}]</div>
        <div class="si-val">${calc}</div>
      </div>`;
    }
  }
  document.getElementById('steps-grid').innerHTML = steps;

  // Formula definition
  const fml = document.getElementById('exp-fml');
  if (expOp === 'kA') {
    fml.innerHTML = `정의: (<span class="fl2">k</span>A)<sub>ij</sub> = <span class="fl2">k</span> · a<sub>ij</sub>`
      + ` &nbsp;·&nbsp; 현재 k = <span class="fl2">${k}</span>`
      + ` &nbsp;·&nbsp; 분배법칙: k(A+B) = kA+kB`;
  } else if (expOp === 'add') {
    fml.innerHTML = `정의: (A<span class="fl">+</span>B)<sub>ij</sub> = a<sub>ij</sub> <span class="fl">+</span> b<sub>ij</sub>`
      + ` &nbsp;·&nbsp; 같은 꼴(크기)의 행렬끼리만 덧셈 가능`;
  } else {
    fml.innerHTML = `정의: (A<span class="fl">−</span>B)<sub>ij</sub> = a<sub>ij</sub> <span class="fl">−</span> b<sub>ij</sub>`
      + ` &nbsp;·&nbsp; A−B = A + (<span class="fl2">−1</span>)B`;
  }
}

/* ═══ CHALLENGE ═══ */
function buildChDots() {
  document.getElementById('ch-dots').innerHTML =
    CHAL.map((_, i) =>
      `<div class="cdot${i < chIdx ? ' done' : i === chIdx ? ' cur' : ''}"></div>`
    ).join('');
}

function renderCh() {
  if (chIdx >= CHAL.length) { showFin(); return; }
  const ch = CHAL[chIdx];
  chTries = 0;

  document.getElementById('ch-num').textContent = `미션 ${chIdx+1} / ${CHAL.length}`;
  document.getElementById('ch-banner').innerHTML =
    `<span class="op-tag">${ch.label}</span>${ch.story}`;
  document.getElementById('ch-ptitle').textContent = ch.title;
  buildChDots();

  const rows = ch.ans.length, cols = ch.ans[0].length;
  let html = '';
  if (ch.type === 'scalar') {
    html += `<div class="k-badge">k = ${ch.k}</div>`;
    html += `<div class="op-big">×</div>`;
    html += blk('A', '#38bdf8', mkMat(ch.A, '#38bdf8', ''));
  } else {
    html += blk('A', '#38bdf8', mkMat(ch.A, '#38bdf8', ''));
    html += `<div class="op-big">${ch.type === 'add' ? '+' : '−'}</div>`;
    html += blk('B', '#a78bfa', mkMat(ch.B, '#a78bfa', ''));
  }
  html += `<div class="eq-big">=</div>`;
  html += blk('?', '#10b981', mkAns(rows, cols));
  document.getElementById('ch-mat-eq').innerHTML = html;

  document.getElementById('result-msg').style.display = 'none';
  document.getElementById('hint-box').style.display   = 'none';
  document.getElementById('checkBtn').style.display   = 'inline-block';
  document.getElementById('nextBtn').style.display    = 'none';

  setTimeout(() => {
    const inputs = document.querySelectorAll('.ac');
    if (inputs.length) inputs[0].focus();
    inputs.forEach((inp, i, all) => {
      inp.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === 'Tab') {
          e.preventDefault();
          if (i + 1 < all.length) all[i+1].focus(); else checkAnswer();
        }
      });
    });
  }, 80);
}

function checkAnswer() {
  const ch = CHAL[chIdx];
  const rows = ch.ans.length, cols = ch.ans[0].length;
  chTries++;
  let allOK = true;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const inp = document.getElementById(`ans_${r}_${c}`);
      const uv  = parseFloat(inp.value.trim().replace('−', '-'));
      inp.classList.remove('ok', 'bad');
      if (uv === ch.ans[r][c]) inp.classList.add('ok');
      else { inp.classList.add('bad'); allOK = false; }
    }
  }

  const msg = document.getElementById('result-msg');
  if (allOK) {
    particles();
    msg.textContent = chTries === 1 ? '🎯 정답! 완벽합니다!' : '✅ 정답!';
    msg.className = 'result-msg ok'; msg.style.display = 'block';
    document.getElementById('checkBtn').style.display = 'none';
    document.getElementById('nextBtn').style.display  = 'inline-block';
  } else {
    msg.textContent = '❌ 빨간 칸을 다시 확인하세요.';
    msg.className = 'result-msg bad'; msg.style.display = 'block';
    const hb = document.getElementById('hint-box');
    hb.innerHTML = '💡 ' + ch.hint; hb.style.display = 'block';
  }
}

function nextCh() {
  chIdx++;
  document.getElementById('result-msg').style.display = 'none';
  document.getElementById('hint-box').style.display   = 'none';
  renderCh();
}

function showFin() {
  document.getElementById('fin-box').style.display  = 'block';
  document.getElementById('ch-mat-eq').innerHTML    = '';
  document.getElementById('ch-ptitle').textContent  = '';
  document.getElementById('ch-banner').textContent  = '';
  document.getElementById('checkBtn').style.display = 'none';
  document.getElementById('nextBtn').style.display  = 'none';
  particles(); particles();
}

/* ═══ TAB SWITCH ═══ */
function switchTab(tab) {
  ['exp', 'ch'].forEach(t => {
    document.getElementById('panel-' + t).classList.toggle('on', t === tab);
    document.getElementById('tb-'    + t).classList.toggle('on', t === tab);
  });
}

/* ═══ PARTICLES ═══ */
function particles() {
  const cols = ['#22c55e','#fbbf24','#38bdf8','#a78bfa','#f87171','#fb923c'];
  const cx = window.innerWidth / 2, cy = 200;
  for (let i = 0; i < 20; i++) {
    const p = document.createElement('div'); p.className = 'pt';
    const ang = Math.random() * Math.PI * 2, dist = 80 + Math.random() * 120;
    p.style.cssText =
      `left:${cx}px;top:${cy}px;` +
      `background:${cols[Math.floor(Math.random() * cols.length)]};` +
      `width:${5 + Math.random() * 5}px;height:${5 + Math.random() * 5}px;` +
      `--tx:${Math.cos(ang) * dist}px;--ty:${Math.sin(ang) * dist - 40}px;` +
      `animation-delay:${Math.random() * .2}s`;
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 1100);
  }
}

/* ═══ INIT ═══ */
buildAPicker();
setOp('kA');
renderCh();
</script>
</body>
</html>"""


def render():
    components.html(_HTML, height=960, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
