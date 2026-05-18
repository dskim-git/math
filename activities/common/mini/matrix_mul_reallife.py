# activities/common/mini/matrix_mul_reallife.py
"""
행렬 곱셈 실생활 탐구
카페 주문 · 운동 효과 · 독서 효과 3가지 상황에서 행렬 곱셈의 의미를 체험하는 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "행렬곱셈실생활탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 '행렬 곱셈 실생활 탐구' 활동을 마치고 생각을 정리해보세요**"},
    {"key": "favorite",
     "label": "1️⃣ 세 가지 상황(카페·운동·독서) 중 행렬 곱셈을 가장 잘 이해할 수 있었던 상황은? 그 이유는?",
     "type": "text_area", "height": 100},
    {"key": "rule",
     "label": "2️⃣ (AB)의 (i,j)성분을 구할 때 A의 몇 번째 행과 B의 몇 번째 열을 곱하나요? 규칙을 자신의 말로 설명해보세요.",
     "type": "text_area", "height": 110},
    {"key": "why",
     "label": "3️⃣ 행렬 곱셈이 실생활 문제에서 왜 편리한지, 새로운 예시를 만들어 설명해보세요.",
     "type": "text_area", "height": 110},
    {"key": "새롭게알게된점",
     "label": "💡 이 활동을 통해 새롭게 알게 된 점",
     "type": "text_area", "height": 90},
    {"key": "느낀점",
     "label": "💬 이 활동을 하면서 느낀 점",
     "type": "text_area", "height": 90},
]

META = {
    "title":       "🛒 행렬 곱셈 실생활 탐구",
    "description": "카페·운동·독서 3가지 일상 사례로 행렬 곱셈의 의미를 직접 체험하는 활동",
    "order":       100,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>행렬 곱셈 실생활 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#060c18;color:#bdd1e8;padding:10px;min-height:100vh}

/* ── tabs ── */
.tab-bar{display:flex;gap:6px;margin-bottom:14px}
.tab-btn{flex:1;padding:10px 4px;border-radius:11px;border:2px solid #152035;background:#0a1525;
  color:#3d5878;font-weight:800;font-size:.8rem;cursor:pointer;transition:all .2s;text-align:center;line-height:1.4}
.tab-btn.active{color:#fff;border-color:transparent}
.tab-btn.t0.active{background:linear-gradient(135deg,#92400e,#d97706)}
.tab-btn.t1.active{background:linear-gradient(135deg,#064e3b,#059669)}
.tab-btn.t2.active{background:linear-gradient(135deg,#4c1d95,#7c3aed)}
.tab-btn:hover:not(.active){background:#0f2035;color:#7dd3fc}
.sc-panel{display:none}.sc-panel.active{display:block}

/* ── story card ── */
.story-card{border-radius:14px;padding:14px 16px;margin-bottom:14px;display:flex;gap:12px;align-items:flex-start}
.story-icon{font-size:3rem;flex-shrink:0;animation:bob 2.5s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.story-title{font-size:1.15rem;font-weight:900;margin-bottom:5px}
.story-desc{font-size:.84rem;line-height:1.7;opacity:.88}

/* ── tip bar ── */
.tip-bar{background:rgba(56,189,248,.07);border:1px solid rgba(56,189,248,.2);
  border-left:3px solid #38bdf8;border-radius:0 8px 8px 0;
  padding:8px 12px;font-size:.78rem;color:#7dd3fc;margin-bottom:14px;line-height:1.6}

/* ── multiplication layout ── */
.mul-wrap{overflow-x:auto;padding-bottom:6px;margin-bottom:14px}
.mul-area{display:flex;align-items:flex-start;gap:10px;min-width:560px;padding:4px 2px}
.mat-block{display:flex;flex-direction:column;align-items:center;flex-shrink:0}
.mat-badge{font-size:.9rem;font-weight:900;letter-spacing:.06em;background:rgba(255,255,255,.07);
  border-radius:7px;padding:3px 14px;margin-bottom:6px}
.mat-col-area{display:flex;flex-direction:column}
.col-hdr-row{display:flex;gap:5px;padding:0 6px;margin-bottom:3px}
.cl{min-width:58px;height:20px;display:flex;align-items:center;justify-content:center;
  font-size:.68rem;color:#475569;font-weight:700;text-align:center}
.cl-r{min-width:70px;height:20px;display:flex;align-items:center;justify-content:center;
  font-size:.65rem;color:#475569;font-weight:700;text-align:center}
.mat-with-labels{display:flex;gap:0}
.rl-col{display:flex;flex-direction:column;gap:5px;padding-bottom:8px;padding-right:5px;justify-content:flex-end}
.rl{min-height:46px;display:flex;align-items:center;justify-content:flex-end;
  font-size:.72rem;color:#64748b;font-weight:700;white-space:nowrap}
.mat-wrap{display:inline-flex;align-items:stretch}
.mat-bl,.mat-br{width:8px;flex-shrink:0}
.mat-bl{border-top:2.5px solid currentColor;border-bottom:2.5px solid currentColor;
  border-left:2.5px solid currentColor;border-radius:4px 0 0 4px}
.mat-br{border-top:2.5px solid currentColor;border-bottom:2.5px solid currentColor;
  border-right:2.5px solid currentColor;border-radius:0 4px 4px 0}
.mat-grid{display:grid;gap:5px;padding:8px 5px}
.mc{min-width:58px;height:46px;display:flex;align-items:center;justify-content:center;
  background:#0d1e30;border:1.5px solid #1a3050;border-radius:7px;
  font-size:1.05rem;font-weight:700;color:#cbd5e1;
  font-family:'Courier New',monospace;transition:all .3s}
.mc.hl-row{background:rgba(251,191,36,.2)!important;border-color:#f59e0b!important;
  color:#fbbf24!important;box-shadow:0 0 14px rgba(251,191,36,.4);transform:scale(1.07)}
.mc.hl-col{background:rgba(167,139,250,.2)!important;border-color:#8b5cf6!important;
  color:#c4b5fd!important;box-shadow:0 0 14px rgba(167,139,250,.4);transform:scale(1.07)}
.mc-r{min-width:70px;height:46px;display:flex;align-items:center;justify-content:center;
  background:#0a1525;border:2px dashed #1e3050;border-radius:7px;
  font-size:1.05rem;font-weight:800;color:#334155;
  font-family:'Courier New',monospace;cursor:pointer;transition:all .25s;user-select:none}
.mc-r:hover{border-color:#38bdf8;color:#7dd3fc;border-style:solid}
.mc-r.selected{border-style:solid;border-color:#38bdf8;color:#7dd3fc;background:rgba(56,189,248,.09);box-shadow:0 0 14px rgba(56,189,248,.3)}
.mc-r.challenge-cell{border-style:solid;border-color:#f59e0b;color:#fbbf24;background:rgba(245,158,11,.1);animation:glowch 2s ease-in-out infinite}
@keyframes glowch{0%,100%{box-shadow:0 0 7px rgba(245,158,11,.3)}50%{box-shadow:0 0 18px rgba(245,158,11,.55)}}
.mc-r.revealed{border-style:solid;border-color:#22c55e;color:#4ade80;background:rgba(34,197,94,.1);cursor:default;animation:none}
.mc-r.ch-correct{border-style:solid;border-color:#fbbf24;color:#fbbf24;background:rgba(245,158,11,.15);cursor:default;animation:none}
.op-sym{font-size:2.2rem;font-weight:900;color:#334155;align-self:center;margin-top:30px;flex-shrink:0;padding:0 2px}
.mat-subdesc{font-size:.68rem;color:#334155;margin-top:4px;text-align:center}

/* ── calc panel ── */
.calc-panel{background:#090f1e;border:1px solid #1a3050;border-radius:13px;
  padding:14px 15px;margin-bottom:14px;display:none}
.calc-panel.show{display:block}
.calc-hdr{font-size:.8rem;color:#64748b;font-weight:700;margin-bottom:10px;letter-spacing:.05em}
.calc-inner{background:#060c18;border:1px solid #152035;border-radius:10px;padding:13px 15px;font-family:'Courier New',monospace}
.calc-pos{font-size:.78rem;color:#475569;margin-bottom:8px}
.calc-eq-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:1rem;margin-bottom:8px}
.calc-row-v{color:#fbbf24;font-weight:800;font-size:1.05rem;
  background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.3);border-radius:6px;padding:4px 10px}
.calc-col-v{color:#c4b5fd;font-weight:800;font-size:1.05rem;
  background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.3);border-radius:6px;padding:4px 10px}
.calc-dot{font-size:1.3rem;color:#475569}
.calc-eqsign{font-size:1.3rem;color:#475569}
.calc-steps{font-size:.95rem;color:#94a3b8;line-height:1.9;margin-top:4px}
.calc-result-box{margin-top:8px;padding:8px 14px;background:rgba(34,197,94,.1);
  border:1px solid rgba(34,197,94,.3);border-radius:8px;
  font-size:1.15rem;font-weight:900;color:#4ade80;text-align:center}
.calc-meaning{margin-top:5px;font-size:.8rem;color:#64748b;text-align:center}
.calc-hint{color:#fbbf24;font-size:.82rem;margin-top:8px}

/* ── challenge section ── */
.ch-section{background:#090f1e;border:1px solid #1e3050;border-radius:13px;padding:14px 15px;margin-bottom:14px}
.ch-hdr{font-size:1rem;font-weight:900;color:#fbbf24;margin-bottom:6px}
.ch-desc{font-size:.82rem;color:#94a3b8;line-height:1.65;margin-bottom:12px}
.ch-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.ch-input{width:110px;padding:10px;background:#0d1e30;border:2px solid #1a3050;
  border-radius:9px;color:#e2e8f0;font-size:1.05rem;font-weight:800;
  text-align:center;outline:none;transition:all .2s;font-family:'Courier New',monospace}
.ch-input:focus{border-color:#fbbf24;box-shadow:0 0 10px rgba(245,158,11,.25)}
.ch-input.ok{border-color:#22c55e;background:rgba(34,197,94,.1);color:#4ade80}
.ch-input.bad{border-color:#ef4444;background:rgba(239,68,68,.08);color:#fca5a5;animation:shk .35s}
@keyframes shk{0%,100%{transform:translateX(0)}25%,75%{transform:translateX(-4px)}50%{transform:translateX(4px)}}
.btn{padding:10px 20px;border-radius:9px;border:none;cursor:pointer;font-size:.87rem;font-weight:800;transition:all .18s}
.btn:hover{transform:translateY(-1px);opacity:.88}
.btn-check{background:linear-gradient(135deg,#0ea5e9,#6366f1);color:#fff}
.ch-fb{margin-top:9px;font-size:.84rem;font-weight:700;padding:8px 13px;border-radius:9px;display:none}
.ch-fb.ok{display:block;background:rgba(34,197,94,.1);color:#4ade80;border:1px solid rgba(34,197,94,.3)}
.ch-fb.bad{display:block;background:rgba(239,68,68,.08);color:#f87171;border:1px solid rgba(239,68,68,.25)}

/* ── reveal all ── */
.reveal-row{text-align:center;margin-bottom:10px}
.btn-reveal{padding:10px 26px;border-radius:10px;border:none;cursor:pointer;
  font-size:.88rem;font-weight:800;
  background:linear-gradient(135deg,#4c1d95,#7c3aed);color:#fff;
  transition:all .18s;box-shadow:0 4px 14px rgba(124,58,237,.3)}
.btn-reveal:hover{transform:translateY(-1px)}

/* ── particles ── */
.pt{position:fixed;pointer-events:none;border-radius:50%;z-index:9999;animation:ptf 1s ease-out forwards}
@keyframes ptf{0%{opacity:1;transform:translate(0,0) scale(1)}100%{opacity:0;transform:translate(var(--tx),var(--ty)) scale(0)}}
</style>
</head>
<body>

<div class="tab-bar" id="tabBar"></div>
<div id="scenarioArea"></div>

<script>
const S = [
  {
    id:0, icon:'☕', title:'카페 주문 분석',
    color:'#f59e0b', colorBg:'rgba(245,158,11,.12)', colorBorder:'rgba(245,158,11,.3)',
    storyDesc:'A반과 B반이 현장학습 후 카페를 방문했어요.<br>두 반이 카페 P, Q 중 어디서 주문하면 얼마를 내야 할까요?',
    A:{data:[[3,5],[4,2]],rowLabels:['A반','B반'],colLabels:['아메리카노','라떼'],name:'A',subdesc:'주문 수량 (잔)'},
    B:{data:[[3000,2500],[4500,4000]],rowLabels:['아메리카노','라떼'],colLabels:['카페 P','카페 Q'],name:'B',subdesc:'음료 가격 (원)'},
    R:{data:[[31500,27500],[21000,18000]],rowLabels:['A반','B반'],colLabels:['카페 P','카페 Q'],unit:'원',
      meanings:[['A반이 카페 P에 낼 금액','A반이 카페 Q에 낼 금액'],['B반이 카페 P에 낼 금액','B반이 카페 Q에 낼 금액']]},
    ch:{r:0,c:1},
    chQ:'(AB)의 (1행, 2열)은 A반이 카페 Q에서 낼 총 금액이에요.<br>아메리카노 3잔 × 2500원 + 라떼 5잔 × 4000원을 계산해보세요!'
  },
  {
    id:1, icon:'🏃', title:'운동 효과 분석',
    color:'#10b981', colorBg:'rgba(16,185,129,.12)', colorBorder:'rgba(16,185,129,.3)',
    storyDesc:'지현과 태오가 일주일 동안 줄넘기와 수영을 꾸준히 했어요.<br>각자 얼마나 칼로리를 소모하고 심폐 능력이 향상될까요?',
    A:{data:[[4,3],[2,5]],rowLabels:['지현','태오'],colLabels:['줄넘기','수영'],name:'A',subdesc:'주간 운동 시간 (h)'},
    B:{data:[[600,3],[500,4]],rowLabels:['줄넘기','수영'],colLabels:['칼로리(kcal)','심폐지수'],name:'B',subdesc:'1시간당 효과'},
    R:{data:[[3900,24],[3700,26]],rowLabels:['지현','태오'],colLabels:['칼로리(kcal)','심폐지수'],unit:'',
      meanings:[['지현의 주간 칼로리 소모','지현의 심폐지수 향상'],['태오의 주간 칼로리 소모','태오의 심폐지수 향상']]},
    ch:{r:1,c:1},
    chQ:'(AB)의 (2행, 2열)은 태오의 심폐지수 향상이에요.<br>줄넘기 2h × 3 + 수영 5h × 4를 계산해보세요!'
  },
  {
    id:2, icon:'📚', title:'독서 효과 분석',
    color:'#8b5cf6', colorBg:'rgba(139,92,246,.12)', colorBorder:'rgba(139,92,246,.3)',
    storyDesc:'수아와 준호는 매주 소설과 과학책을 읽어요.<br>이 독서 습관이 국어·과학 점수에 얼마나 도움이 될까요?',
    A:{data:[[5,3],[2,7]],rowLabels:['수아','준호'],colLabels:['소설','과학책'],name:'A',subdesc:'주간 독서 시간 (h)'},
    B:{data:[[8,2],[3,9]],rowLabels:['소설','과학책'],colLabels:['국어점수','과학점수'],name:'B',subdesc:'시간당 점수 향상 (점/h)'},
    R:{data:[[49,37],[37,67]],rowLabels:['수아','준호'],colLabels:['국어 향상','과학 향상'],unit:'점',
      meanings:[['수아의 국어 점수 향상','수아의 과학 점수 향상'],['준호의 국어 점수 향상','준호의 과학 점수 향상']]},
    ch:{r:0,c:0},
    chQ:'(AB)의 (1행, 1열)은 수아의 국어 점수 향상이에요.<br>소설 5h × 8점 + 과학책 3h × 3점을 계산해보세요!'
  }
];

const chSolved = [false,false,false];

/* ── build HTML ─────────────────────────────────────────────────────── */

function mkMat(sid, s, prefix, isR) {
  const data = isR ? s.R.data : (prefix==='A' ? s.A.data : s.B.data);
  const rl   = isR ? s.R.rowLabels : (prefix==='A' ? s.A.rowLabels : s.B.rowLabels);
  const cl   = isR ? s.R.colLabels : (prefix==='A' ? s.A.colLabels : s.B.colLabels);
  const name = isR ? 'AB' : prefix;
  const subdesc = isR ? '← 클릭해서 계산 과정 확인!' : (prefix==='A' ? s.A.subdesc : s.B.subdesc);
  const color = isR ? '#22c55e' : (prefix==='A' ? '#38bdf8' : '#a78bfa');
  const colW  = isR ? 70 : 58;

  // col headers
  let chRow = `<div class="col-hdr-row">`;
  cl.forEach(c => chRow += `<div class="${isR?'cl-r':'cl'}">${c}</div>`);
  chRow += `</div>`;

  // row labels
  let rlHtml = `<div class="rl-col">`;
  rl.forEach(r => rlHtml += `<div class="rl">${r}</div>`);
  rlHtml += `</div>`;

  // cells
  let cells = '';
  for(let r=0;r<2;r++) for(let c=0;c<2;c++) {
    if(isR) {
      const isCh = (r===s.ch.r && c===s.ch.c);
      cells += `<div class="mc-r ${isCh?'challenge-cell':''}" id="mcr-${sid}-${r}-${c}"
        onclick="clickResult(${sid},${r},${c})"
        style="grid-column:${c+1};grid-row:${r+1}">?</div>`;
    } else {
      cells += `<div class="mc" id="mc-${sid}-${prefix.toLowerCase()}-${r}-${c}"
        style="grid-column:${c+1};grid-row:${r+1}">${data[r][c]}</div>`;
    }
  }

  return `<div class="mat-block">
    <div class="mat-badge" style="color:${color}">${name}</div>
    <div class="mat-col-area">
      ${chRow}
      <div class="mat-with-labels">
        ${rlHtml}
        <div class="mat-wrap" style="color:${color}">
          <div class="mat-bl"></div>
          <div class="mat-grid" style="grid-template-columns:repeat(2,${colW}px)">${cells}</div>
          <div class="mat-br"></div>
        </div>
      </div>
    </div>
    <div class="mat-subdesc">${subdesc}</div>
  </div>`;
}

function buildPanel(s) {
  return `<div class="sc-panel ${s.id===0?'active':''}" id="sc-${s.id}">
    <div class="story-card" style="background:${s.colorBg};border:1px solid ${s.colorBorder}">
      <div class="story-icon">${s.icon}</div>
      <div>
        <div class="story-title" style="color:${s.color}">${s.title}</div>
        <div class="story-desc">${s.storyDesc}</div>
      </div>
    </div>

    <div class="tip-bar">
      💡 <strong style="color:#fbbf24">노란 테두리 칸</strong>의 값을 직접 계산해서 입력해보세요!
      &nbsp;나머지 칸을 클릭하면 계산 과정을 확인할 수 있어요.
    </div>

    <div class="mul-wrap">
      <div class="mul-area">
        ${mkMat(s.id, s, 'A', false)}
        <div class="op-sym">×</div>
        ${mkMat(s.id, s, 'B', false)}
        <div class="op-sym">=</div>
        ${mkMat(s.id, s, 'R', true)}
      </div>
    </div>

    <div class="calc-panel" id="calc-${s.id}">
      <div class="calc-hdr">📐 계산 과정</div>
      <div class="calc-inner" id="calc-inner-${s.id}"></div>
    </div>

    <div class="ch-section">
      <div class="ch-hdr">✏️ 직접 계산해보기</div>
      <div class="ch-desc">${s.chQ}</div>
      <div class="ch-row">
        <input class="ch-input" id="ch-inp-${s.id}" type="number" placeholder="답 입력"
          onkeydown="if(event.key==='Enter')checkCh(${s.id})">
        <button class="btn btn-check" onclick="checkCh(${s.id})">✓ 확인</button>
      </div>
      <div class="ch-fb" id="ch-fb-${s.id}"></div>
    </div>

    <div class="reveal-row">
      <button class="btn-reveal" onclick="revealAll(${s.id})">🔓 전체 결과 확인하기</button>
    </div>
  </div>`;
}

/* ── init ───────────────────────────────────────────────────────────── */

function init() {
  const tabBar = document.getElementById('tabBar');
  S.forEach((s, i) => {
    const btn = document.createElement('button');
    btn.className = `tab-btn t${i} ${i===0?'active':''}`;
    btn.innerHTML = `${s.icon}<br>${s.title}`;
    btn.onclick = () => switchTab(i);
    tabBar.appendChild(btn);
  });
  document.getElementById('scenarioArea').innerHTML = S.map(buildPanel).join('');
}

function switchTab(sid) {
  document.querySelectorAll('.tab-btn').forEach((b,i)=>b.classList.toggle('active',i===sid));
  document.querySelectorAll('.sc-panel').forEach((p,i)=>p.classList.toggle('active',i===sid));
}

/* ── click result cell ──────────────────────────────────────────────── */

function clickResult(sid, r, c) {
  const s = S[sid];
  // clear highlights
  for(let rr=0;rr<2;rr++) for(let cc=0;cc<2;cc++) {
    const a=document.getElementById(`mc-${sid}-a-${rr}-${cc}`);
    const b=document.getElementById(`mc-${sid}-b-${rr}-${cc}`);
    if(a){a.classList.remove('hl-row','hl-col')}
    if(b){b.classList.remove('hl-row','hl-col')}
  }
  // highlight row r of A
  for(let cc=0;cc<2;cc++){const e=document.getElementById(`mc-${sid}-a-${r}-${cc}`);if(e)e.classList.add('hl-row')}
  // highlight col c of B
  for(let rr=0;rr<2;rr++){const e=document.getElementById(`mc-${sid}-b-${rr}-${c}`);if(e)e.classList.add('hl-col')}
  // mark selected
  document.querySelectorAll(`[id^="mcr-${sid}-"]`).forEach(el=>{
    if(!el.classList.contains('revealed')&&!el.classList.contains('ch-correct')) el.classList.remove('selected');
  });
  const rc=document.getElementById(`mcr-${sid}-${r}-${c}`);
  if(rc&&!rc.classList.contains('revealed')&&!rc.classList.contains('ch-correct')) rc.classList.add('selected');

  showCalc(sid, r, c);
}

function showCalc(sid, r, c) {
  const s = S[sid];
  const A = s.A.data, B = s.B.data;
  const v0=A[r][0], v1=A[r][1], w0=B[0][c], w1=B[1][c];
  const result=s.R.data[r][c];
  const meaning=s.R.meanings[r][c];
  const unit = s.R.unit ? ' '+s.R.unit : '';
  const isCh=(r===s.ch.r && c===s.ch.c);
  const n1=v0*w0, n2=v1*w1;
  const rowVec = `[ ${v0} &nbsp; ${v1} ]`;
  const colVec = `[ ${w0}, ${w1} ]`;
  let html = `<div class="calc-pos">(${r+1}행, ${c+1}열) = A의 ${r+1}번째 행 · B의 ${c+1}번째 열</div>
    <div class="calc-eq-row">
      <span class="calc-row-v">${rowVec}</span>
      <span class="calc-dot">·</span>
      <span class="calc-col-v">${colVec}</span>
    </div>`;

  if(isCh && !chSolved[sid]) {
    html += `<div class="calc-steps">${v0} × ${w0} + ${v1} × ${w1} = <strong style="color:#fbbf24">?</strong></div>
      <div class="calc-hint">👇 아래에 직접 계산해서 입력해보세요!</div>`;
  } else {
    html += `<div class="calc-steps">= ${v0} × ${w0} + ${v1} × ${w1}<br>= ${n1} + ${n2}</div>
      <div class="calc-result-box">= ${result}${unit}</div>
      <div class="calc-meaning">📌 ${meaning}</div>`;
  }

  const panel=document.getElementById(`calc-${sid}`);
  document.getElementById(`calc-inner-${sid}`).innerHTML=html;
  panel.classList.add('show');
  panel.scrollIntoView({behavior:'smooth',block:'nearest'});
}

/* ── challenge check ────────────────────────────────────────────────── */

function checkCh(sid) {
  const s=S[sid];
  const inp=document.getElementById(`ch-inp-${sid}`);
  const fb=document.getElementById(`ch-fb-${sid}`);
  const {r,c}=s.ch;
  const correct=s.R.data[r][c];
  const val=parseFloat(inp.value.trim());
  inp.classList.remove('ok','bad'); fb.className='ch-fb';

  if(isNaN(val)){fb.textContent='⚠️ 숫자를 입력해주세요.';fb.className='ch-fb bad';return;}

  if(Math.abs(val-correct)<0.001){
    inp.classList.add('ok'); inp.disabled=true;
    const unit=s.R.unit?' '+s.R.unit:'';
    fb.innerHTML=`🎉 정답! <strong>${correct}${unit}</strong> — ${s.R.meanings[r][c]}`;
    fb.className='ch-fb ok';
    chSolved[sid]=true;
    const rcell=document.getElementById(`mcr-${sid}-${r}-${c}`);
    if(rcell){rcell.textContent=correct;rcell.className='mc-r ch-correct';}
    showCalc(sid,r,c);
    particles();
  } else {
    inp.classList.add('bad');
    const A=s.A.data, B=s.B.data;
    fb.innerHTML=`❌ 다시 계산해보세요! 힌트: ${A[r][0]} × ${B[0][c]} + ${A[r][1]} × ${B[1][c]} = ?`;
    fb.className='ch-fb bad';
  }
}

/* ── reveal all ─────────────────────────────────────────────────────── */

function revealAll(sid) {
  const s=S[sid];
  for(let r=0;r<2;r++) for(let c=0;c<2;c++){
    const cell=document.getElementById(`mcr-${sid}-${r}-${c}`);
    if(!cell||cell.classList.contains('ch-correct')) continue;
    cell.textContent=s.R.data[r][c];
    cell.classList.remove('challenge-cell','selected');
    cell.classList.add('revealed');
  }
  particles();
}

/* ── particles ──────────────────────────────────────────────────────── */

function particles() {
  const cols=['#22c55e','#fbbf24','#38bdf8','#a78bfa','#f87171','#fb923c'];
  const cx=window.innerWidth/2, cy=Math.min(300,window.innerHeight/2);
  for(let i=0;i<24;i++){
    const p=document.createElement('div'); p.className='pt';
    const ang=Math.random()*Math.PI*2, dist=80+Math.random()*150;
    p.style.cssText=`left:${cx}px;top:${cy}px;`+
      `background:${cols[Math.floor(Math.random()*cols.length)]};`+
      `width:${5+Math.random()*6}px;height:${5+Math.random()*6}px;`+
      `--tx:${Math.cos(ang)*dist}px;--ty:${Math.sin(ang)*dist-70}px;`+
      `animation-delay:${Math.random()*.15}s`;
    document.body.appendChild(p);
    setTimeout(()=>p.remove(),1200);
  }
}

init();
</script>
</body>
</html>"""


def render():
    st.markdown("### 🛒 행렬 곱셈 실생활 탐구")
    st.caption("카페·운동·독서 3가지 상황에서 행렬 곱셈의 의미를 직접 탐구해봐요!")
    components.html(_HTML, height=1100, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
