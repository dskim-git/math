# activities/common/mini/matrix_population_migration.py
"""
행렬로 보는 두 도시 인구 이동
전이행렬 A를 이용하여 Z 광역시와 신도시의 인구 변화를 시뮬레이션하는 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "행렬인구이동탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 '행렬로 보는 두 도시 인구 이동' 활동을 마치고 생각을 정리해보세요**"},
    {"key": "matrix_meaning",
     "label": "1️⃣ 전이행렬 A의 1행 2열 성분(0.05)과 2행 1열 성분(0.1)은 각각 무엇을 의미하나요?",
     "type": "text_area", "height": 100},
    {"key": "surprise",
     "label": "2️⃣ 신도시 인구가 100만 명이 되는 데 몇 년이 걸렸나요? 예상과 달랐나요? 왜 그런지 설명해보세요.",
     "type": "text_area", "height": 110},
    {"key": "application",
     "label": "3️⃣ 행렬의 거듭제곱 Aⁿ을 이용하면 수십 년 후의 인구를 예측할 수 있어요. 이 방법을 다른 실생활 문제에 어떻게 적용할 수 있을까요?",
     "type": "text_area", "height": 110},
    {"key": "새롭게알게된점",
     "label": "💡 이 활동을 통해 새롭게 알게 된 점",
     "type": "text_area", "height": 90},
    {"key": "느낀점",
     "label": "💬 이 활동을 하면서 느낀 점",
     "type": "text_area", "height": 90},
]

META = {
    "title":       "🏙️ 행렬로 보는 두 도시 인구 이동",
    "description": "전이행렬 A^n을 이용해 Z 광역시와 신도시의 인구 변화를 시뮬레이션하고, 신도시가 100만 명을 넘는 시기를 예측하는 활동",
    "order":       9,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>행렬로 보는 두 도시 인구 이동</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#060c18;color:#bdd1e8;padding:10px;min-height:100vh}

.tab-bar{display:flex;gap:6px;margin-bottom:14px}
.tb{flex:1;padding:10px 4px;text-align:center;border-radius:11px;
  border:2px solid #152035;background:#0a1525;color:#3d5878;
  font-size:.88rem;font-weight:800;cursor:pointer;transition:all .2s;line-height:1.5}
.tb.on{background:linear-gradient(135deg,#1d4ed8,#7c3aed);color:#fff;
  border-color:transparent;box-shadow:0 3px 16px rgba(99,102,241,.35)}
.tb:hover:not(.on){background:#0f2035;color:#7dd3fc}
.panel{display:none}.panel.on{display:block}

.card{background:#0d1a2e;border:1px solid #1e3050;border-radius:14px;padding:16px;margin-bottom:12px}
.card-title{font-size:1.1rem;font-weight:900;color:#fbbf24;margin-bottom:14px}

/* matrix brackets */
.mw{display:inline-flex;align-items:stretch;vertical-align:middle}
.ml,.mr{width:9px;flex-shrink:0}
.ml{border-top:3px solid currentColor;border-bottom:3px solid currentColor;
  border-left:3px solid currentColor;border-radius:4px 0 0 4px}
.mr{border-top:3px solid currentColor;border-bottom:3px solid currentColor;
  border-right:3px solid currentColor;border-radius:0 4px 4px 0}
.mg{display:grid;gap:5px;padding:7px 4px}
.mc{display:flex;align-items:center;justify-content:center;border-radius:7px;
  font-family:'Courier New',monospace;font-weight:700;border:2px solid;
  background:rgba(0,0,0,.35)}

/* city diagram */
.city-row{display:flex;align-items:center;justify-content:center;gap:0;padding:10px 0 6px;flex-wrap:nowrap}
.city-box{display:flex;flex-direction:column;align-items:center;gap:8px;width:130px;flex-shrink:0}
.city-icon{font-size:3.8rem;animation:float 3s ease-in-out infinite;line-height:1}
.city-icon.d2{animation-delay:1.5s}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
.city-name{font-size:1rem;font-weight:900;text-align:center}
.city-pop{font-size:.88rem;padding:5px 12px;border-radius:8px;font-family:'Courier New',monospace;font-weight:700;text-align:center}

.arrow-col{display:flex;flex-direction:column;align-items:center;gap:6px;width:120px;flex-shrink:0;padding:0 4px}
.arr-row{display:flex;align-items:center;gap:4px;width:100%}
.pct{font-size:1rem;font-weight:900;padding:4px 8px;border-radius:7px;white-space:nowrap;flex-shrink:0;line-height:1.2}
.aline{flex:1;height:2.5px;border-radius:2px;position:relative}
.arr-right::after{content:'';position:absolute;right:-2px;top:-4px;
  border-top:5.5px solid transparent;border-bottom:5.5px solid transparent;border-left:9px solid currentColor}
.arr-left::before{content:'';position:absolute;left:-2px;top:-4px;
  border-top:5.5px solid transparent;border-bottom:5.5px solid transparent;border-right:9px solid currentColor}
.arr-sub{font-size:.68rem;color:#475569;text-align:center}

/* pop bars */
.bar-wrap{margin-bottom:10px}
.bar-label{font-size:.82rem;font-weight:700;margin-bottom:5px}
.bar-track{background:#060c18;border-radius:7px;height:28px;position:relative;overflow:hidden;border:1px solid #152035}
.bar-fill{height:100%;border-radius:7px;transition:width .7s cubic-bezier(.4,0,.2,1);
  display:flex;align-items:center;padding-left:10px}
.bar-val{font-size:.82rem;font-weight:800;font-family:'Courier New',monospace;white-space:nowrap;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.6)}
.bar-note{font-size:.7rem;font-weight:700;color:#fbbf24;margin-top:3px}

/* year badge */
.year-badge{font-size:2.2rem;font-weight:900;padding:7px 22px;border-radius:13px;
  background:rgba(99,102,241,.12);border:2px solid rgba(99,102,241,.35);
  color:#a78bfa;font-family:'Courier New',monospace;display:inline-block;
  box-shadow:0 0 20px rgba(99,102,241,.15)}

.eq-area{background:#060c18;border-radius:12px;padding:14px;margin-top:10px;overflow-x:auto}
.eq-label{font-size:.75rem;color:#64748b;font-weight:700;margin-bottom:10px;letter-spacing:.04em}
.eq-row{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:nowrap;min-width:380px}
.op{font-size:2rem;font-weight:900;color:#475569}

.hint{background:rgba(56,189,248,.07);border-left:3px solid #38bdf8;
  border-radius:0 8px 8px 0;padding:9px 13px;font-size:.84rem;color:#7dd3fc;
  line-height:1.7;margin:10px 0}

/* milestone */
.milestone{border-radius:12px;padding:13px 16px;text-align:center;margin-top:12px;
  display:none;animation:popIn .5s ease}
.milestone.show{display:block}
@keyframes popIn{0%{transform:scale(.8);opacity:0}70%{transform:scale(1.05)}100%{transform:scale(1);opacity:1}}

/* challenge */
.ch-inp{background:#0a1525;border:2.5px solid #1e3050;border-radius:10px;
  color:#e2e8f0;font-size:1.8rem;font-weight:800;font-family:'Courier New',monospace;
  padding:10px 16px;text-align:center;width:110px;outline:none;transition:all .2s;
  -moz-appearance:textfield}
.ch-inp::-webkit-inner-spin-button,.ch-inp::-webkit-outer-spin-button{-webkit-appearance:none}
.ch-inp:focus{border-color:#fbbf24;box-shadow:0 0 14px rgba(245,158,11,.25)}
.ch-inp.ok{border-color:#22c55e;background:rgba(34,197,94,.1);color:#4ade80}
.ch-inp.bad{border-color:#ef4444;animation:shk .35s}
@keyframes shk{0%,100%{transform:translateX(0)}25%,75%{transform:translateX(-5px)}50%{transform:translateX(5px)}}
.fb{margin-top:10px;font-size:.88rem;font-weight:700;padding:11px 14px;border-radius:10px;display:none;line-height:1.6}
.fb.ok{display:block;background:rgba(34,197,94,.1);color:#4ade80;border:1px solid rgba(34,197,94,.3)}
.fb.bad{display:block;background:rgba(239,68,68,.08);color:#f87171;border:1px solid rgba(239,68,68,.25)}

/* buttons */
.btn{padding:10px 20px;border-radius:10px;border:none;cursor:pointer;
  font-size:.9rem;font-weight:800;transition:all .18s}
.btn:hover:not(:disabled){transform:translateY(-2px);opacity:.9}
.btn:disabled{opacity:.4;cursor:default;transform:none}
.btn-go{background:linear-gradient(135deg,#1d4ed8,#7c3aed);color:#fff;box-shadow:0 3px 12px rgba(99,102,241,.3)}
.btn-reset{background:#0d1a2e;color:#64748b;border:1px solid #1e3050}
.btn-check{background:linear-gradient(135deg,#d97706,#fbbf24);color:#000;box-shadow:0 3px 12px rgba(217,119,6,.25)}
.btn-reveal{background:linear-gradient(135deg,#059669,#10b981);color:#fff;box-shadow:0 3px 12px rgba(5,150,105,.3)}

/* graph legend */
.legend-row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:10px}
.legend-item{display:flex;align-items:center;gap:6px;font-size:.8rem;color:#94a3b8}
.legend-line{width:22px;height:3px;border-radius:2px}

canvas{border-radius:10px;background:#060c18;width:100%;display:block}

/* particle */
.pt{position:fixed;pointer-events:none;border-radius:50%;z-index:9999;animation:ptf 1s ease-out forwards}
@keyframes ptf{0%{opacity:1;transform:translate(0,0)scale(1)}100%{opacity:0;transform:translate(var(--tx),var(--ty))scale(0)}}
</style>
</head>
<body>

<div class="tab-bar">
  <div class="tb on" id="tb-setup" onclick="switchTab('setup')">📐 상황 파악</div>
  <div class="tb"    id="tb-sim"   onclick="switchTab('sim')">📊 연도별 시뮬레이션</div>
  <div class="tb"    id="tb-chall" onclick="switchTab('chall')">🎯 도전!</div>
  <div class="tb"    id="tb-ext"   onclick="switchTab('ext')">🌐 확장하기</div>
</div>

<!-- ════ TAB 1 : 상황 파악 ════ -->
<div class="panel on" id="panel-setup">

  <div class="card">
    <div class="card-title">🏙️ 두 도시의 인구 이동 상황</div>
    <div class="city-row" id="city-diag"></div>
    <div class="hint">
      💡 총 인구는 변하지 않아요. 이동하는 비율만큼 서로 주고받을 뿐이에요!
    </div>
  </div>

  <div class="card">
    <div class="card-title">📋 행렬로 나타내기</div>
    <div style="text-align:center;margin-bottom:14px">
      <div style="font-size:.9rem;color:#64748b;margin-bottom:14px;line-height:1.8">
        이동 비율을 <strong style="color:#fbbf24">전이행렬 A</strong>로,&nbsp;
        현재 인구를 <strong style="color:#38bdf8">행렬 B</strong>로 나타내요
      </div>
      <div id="setup-mats"></div>
    </div>

    <div style="background:#060c18;border-radius:12px;padding:16px;text-align:center;line-height:2.6">
      <div style="font-size:1.05rem">
        <span style="color:#fbbf24;font-weight:900">1년 후</span> 인구
        &nbsp;=&nbsp;
        <span style="color:#fbbf24;font-weight:900;font-size:1.3rem">A</span>
        &nbsp;×&nbsp;
        <span style="color:#38bdf8;font-weight:900;font-size:1.3rem">B</span>
      </div>
      <div style="font-size:1.05rem">
        <span style="color:#a78bfa;font-weight:900">n년 후</span> 인구
        &nbsp;=&nbsp;
        <span style="color:#fbbf24;font-weight:900;font-size:1.3rem">A<sup style="font-size:.7rem">n</sup></span>
        &nbsp;×&nbsp;
        <span style="color:#38bdf8;font-weight:900;font-size:1.3rem">B</span>
      </div>
    </div>
  </div>

  <div class="card" style="background:rgba(16,185,129,.06);border-color:rgba(16,185,129,.25)">
    <div style="font-size:1rem;font-weight:900;color:#10b981;margin-bottom:8px">🤔 생각해봐요</div>
    <div style="font-size:.95rem;line-height:1.85;color:#94a3b8">
      신도시 인구는 현재 <strong style="color:#10b981">2만 명</strong>에 불과해요.<br>
      매년 광역시 인구의 10%가 이동해 온다면,<br>
      <strong style="color:#fbbf24;font-size:1.05rem">신도시 인구가 100만 명이 되는 데 몇 년이 걸릴까요?</strong>
    </div>
  </div>

  <div style="text-align:center;margin-bottom:8px">
    <button class="btn btn-go" onclick="switchTab('sim')">📊 시뮬레이션으로 확인하기 ▶</button>
  </div>
</div>

<!-- ════ TAB 2 : 시뮬레이션 ════ -->
<div class="panel" id="panel-sim">

  <div class="card">
    <div class="card-title">📊 연도별 인구 변화 시뮬레이션</div>

    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:16px">
      <div class="year-badge" id="year-badge">0년</div>
      <button class="btn btn-go" id="btn-next" onclick="nextYear()">▶ 다음 해</button>
      <button class="btn btn-reset" onclick="resetSim()">↺ 처음으로</button>
    </div>

    <div id="sim-bars"></div>

    <div id="sim-eq" style="display:none">
      <div class="eq-area">
        <div class="eq-label" id="eq-label"></div>
        <div class="eq-row" id="eq-content"></div>
        <div id="eq-breakdown" style="margin-top:10px;font-size:.8rem;color:#64748b;line-height:1.9"></div>
      </div>
    </div>

    <div class="milestone" id="ms-new"
      style="background:rgba(34,197,94,.08);border:2px solid #22c55e">
      <div style="font-size:2rem;margin-bottom:6px">🎉</div>
      <div style="font-size:1.1rem;font-weight:900;color:#4ade80">신도시 인구 100만 명 돌파!</div>
      <div style="font-size:.85rem;color:#64748b;margin-top:4px" id="ms-new-val"></div>
    </div>
    <div class="milestone" id="ms-city"
      style="background:rgba(56,189,248,.06);border:2px solid rgba(56,189,248,.3)">
      <div style="font-size:.95rem;font-weight:700;color:#7dd3fc" id="ms-city-msg"></div>
    </div>
  </div>

  <div style="text-align:center;margin-bottom:8px">
    <button class="btn btn-go" onclick="switchTab('chall')">🎯 도전 문제 풀기 ▶</button>
  </div>
</div>

<!-- ════ TAB 3 : 도전 ════ -->
<div class="panel" id="panel-chall">

  <div class="card">
    <div class="card-title">🎯 도전 문제</div>
    <div style="font-size:1rem;line-height:1.9;color:#94a3b8;margin-bottom:18px">
      시뮬레이션에서 확인한 것처럼 신도시 인구는 매년 늘어나요.<br>
      <strong style="color:#fbbf24;font-size:1.1rem">신도시 인구가 처음으로 100만 명을 넘는 것은 몇 년 후일까요?</strong>
    </div>
    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <input class="ch-inp" id="ch-inp" type="number" min="1" max="20" placeholder="?">
      <span style="font-size:1.2rem;color:#64748b;font-weight:700">년 후</span>
      <button class="btn btn-check" onclick="checkAnswer()">✓ 확인</button>
    </div>
    <div class="fb" id="ch-fb"></div>
  </div>

  <div class="card" id="graph-card">
    <div class="card-title">📈 인구 변화 그래프</div>
    <canvas id="chart" height="260"></canvas>
    <div class="legend-row">
      <div class="legend-item">
        <div class="legend-line" style="background:#38bdf8"></div>Z 광역시
      </div>
      <div class="legend-item">
        <div class="legend-line" style="background:#10b981"></div>신도시
      </div>
      <div class="legend-item">
        <div class="legend-line" style="background:#fbbf24;border-top:2px dashed #fbbf24;height:0"></div>100만 명 기준
      </div>
    </div>
    <div class="hint" id="graph-hint" style="display:none;margin-top:10px">
      📌 초록 선이 노란 점선을 처음 넘는 시점이 바로 <strong style="color:#fbbf24">5년 후</strong>예요!<br>
      5년 후 신도시 인구 ≈ <strong style="color:#10b981">112만 9천 명</strong>
    </div>
    <div id="reveal-wrap" style="text-align:center;margin-top:12px">
      <button class="btn btn-reveal" onclick="revealGraph()">📈 그래프 전체 공개</button>
    </div>
  </div>

</div>

<script>
/* ══ CONSTANTS ══ */
const A = [[0.9, 0.05],[0.1, 0.95]];
const INIT = [3000000, 20000];
const MAX_YEAR = 10;
const TARGET = 1000000;

/* ══ PRECOMPUTE POPULATIONS ══ */
const POP = [INIT.slice()];
for(let y = 1; y <= MAX_YEAR; y++) {
  const p = POP[y-1];
  POP.push([
    A[0][0]*p[0] + A[0][1]*p[1],
    A[1][0]*p[0] + A[1][1]*p[1]
  ]);
}
const ANSWER = POP.findIndex(p => p[1] >= TARGET); // 5

/* ══ HELPERS ══ */
function fmtPop(n) { return Math.round(n).toLocaleString('ko-KR') + '명'; }
function fmtMan(n) { return (Math.round(n/1000)/10).toFixed(1) + '만'; }

function matHtml(rows, color, cw, ch, fs) {
  cw = cw||70; ch = ch||44; fs = fs||'1rem';
  const cols = rows[0].length;
  let cells = '';
  rows.forEach(r => r.forEach(v => {
    cells += `<div class="mc" style="min-width:${cw}px;height:${ch}px;font-size:${fs};border-color:${color};color:${color}">${v}</div>`;
  }));
  return `<span class="mw" style="color:${color}"><span class="ml"></span>`+
    `<span class="mg" style="grid-template-columns:repeat(${cols},${cw}px)">${cells}</span>`+
    `<span class="mr"></span></span>`;
}

/* ══ TAB 1: SETUP ══ */
function buildSetup() {
  // city diagram
  document.getElementById('city-diag').innerHTML = `
    <div class="city-box">
      <div class="city-icon">🏙️</div>
      <div class="city-name" style="color:#38bdf8">Z 광역시</div>
      <div class="city-pop" style="background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.3);color:#38bdf8">300만 명</div>
    </div>

    <div class="arrow-col">
      <div class="arr-row">
        <span class="pct" style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);color:#10b981">10%</span>
        <div class="aline arr-right" style="background:#10b981;color:#10b981"></div>
      </div>
      <div class="arr-sub">매년 이동</div>
      <div class="arr-row">
        <div class="aline arr-left" style="background:#ef4444;color:#ef4444"></div>
        <span class="pct" style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);color:#ef4444">5%</span>
      </div>
    </div>

    <div class="city-box">
      <div class="city-icon d2">🏘️</div>
      <div class="city-name" style="color:#10b981">신도시</div>
      <div class="city-pop" style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);color:#10b981">2만 명</div>
    </div>`;

  // matrix display
  const Adisp = [['0.9','0.05'],['0.1','0.95']];
  const Bdisp = [['300만'],['2만']];
  document.getElementById('setup-mats').innerHTML = `
    <div style="display:flex;align-items:flex-start;justify-content:center;gap:28px;flex-wrap:wrap">
      <div style="text-align:center">
        <div style="font-size:1rem;font-weight:900;color:#fbbf24;margin-bottom:10px">전이행렬 A</div>
        ${matHtml(Adisp,'#fbbf24',72,48,'1rem')}
        <div style="margin-top:8px;font-size:.75rem;color:#475569;line-height:1.7">
          1행: 광역시에 <em>남는</em> 비율<br>2행: 신도시로 <em>이동</em> 비율
        </div>
      </div>
      <div style="text-align:center">
        <div style="font-size:1rem;font-weight:900;color:#38bdf8;margin-bottom:10px">초기 인구 B₀</div>
        ${matHtml(Bdisp,'#38bdf8',80,48,'1rem')}
        <div style="margin-top:8px;font-size:.75rem;color:#475569;line-height:1.7">
          1행: Z 광역시<br>2행: 신도시
        </div>
      </div>
    </div>`;
}

/* ══ TAB 2: SIMULATION ══ */
let curYear = 0, msNew = false, msCity = false;

function buildBars(y) {
  const [city, news] = POP[y];
  const maxRef = INIT[0]; // 300만 기준
  const cp = Math.min(city/maxRef*100, 100).toFixed(1);
  const np = Math.min(news/maxRef*100, 100).toFixed(1);
  const newPassed = news >= TARGET;

  return `
    <div class="bar-wrap">
      <div class="bar-label" style="color:#38bdf8">🏙️ Z 광역시 &nbsp;<span style="font-size:.75rem;color:#475569;font-weight:400">(이전 해 대비 ${y>0?(city<POP[y-1][0]?'▼':'▲'):''})</span></div>
      <div class="bar-track">
        <div class="bar-fill" style="width:${cp}%;background:linear-gradient(90deg,#1d4ed8,#38bdf8)">
          <span class="bar-val">${fmtPop(city)}</span>
        </div>
      </div>
    </div>
    <div class="bar-wrap">
      <div class="bar-label" style="color:#10b981">🏘️ 신도시</div>
      <div class="bar-track">
        <div class="bar-fill" style="width:${np}%;background:linear-gradient(90deg,#059669,#10b981)">
          <span class="bar-val">${fmtPop(news)}</span>
        </div>
      </div>
      ${newPassed ? `<div class="bar-note">★ 100만 명 돌파!</div>` : ''}
    </div>`;
}

function buildEq(fromY) {
  const [c0, n0] = POP[fromY];
  const [c1, n1] = POP[fromY+1];
  const Adisp = [['0.9','0.05'],['0.1','0.95']];
  const Bdisp = [[fmtMan(c0)],[fmtMan(n0)]];
  const Rdisp = [[fmtMan(c1)],[fmtMan(n1)]];

  const cCalc = `0.9 × ${fmtMan(c0)} + 0.05 × ${fmtMan(n0)} = <strong style="color:#38bdf8">${fmtMan(c1)}</strong>`;
  const nCalc = `0.1 × ${fmtMan(c0)} + 0.95 × ${fmtMan(n0)} = <strong style="color:#10b981">${fmtMan(n1)}</strong>`;

  document.getElementById('eq-label').textContent = `A × B${fromY} = B${fromY+1} 계산 과정 (단위: 만 명)`;
  document.getElementById('eq-content').innerHTML =
    matHtml(Adisp,'#fbbf24',65,40,'.82rem') +
    `<span class="op">×</span>` +
    matHtml(Bdisp,'#38bdf8',72,40,'.82rem') +
    `<span class="op">=</span>` +
    matHtml(Rdisp,'#10b981',72,40,'.82rem');
  document.getElementById('eq-breakdown').innerHTML =
    `<span style="color:#38bdf8">광역시</span>: ${cCalc}<br>`+
    `<span style="color:#10b981">신도시</span>: ${nCalc}`;
}

function updateSim() {
  document.getElementById('year-badge').textContent = curYear + '년';
  document.getElementById('sim-bars').innerHTML = buildBars(curYear);
  document.getElementById('btn-next').disabled = (curYear >= MAX_YEAR);

  if(curYear > 0) {
    document.getElementById('sim-eq').style.display = 'block';
    buildEq(curYear - 1);
  } else {
    document.getElementById('sim-eq').style.display = 'none';
  }

  const [city, news] = POP[curYear];

  if(!msNew && news >= TARGET) {
    msNew = true;
    document.getElementById('ms-new-val').textContent =
      `${curYear}년 후 신도시 인구 ≈ ${fmtPop(news)}`;
    document.getElementById('ms-new').classList.add('show');
    burst();
  }
  if(!msCity && city < 2000000 && curYear > 0) {
    msCity = true;
    document.getElementById('ms-city-msg').textContent =
      `📉 Z 광역시 인구가 200만 명 아래로 내려갔어요 (${fmtPop(city)})`;
    document.getElementById('ms-city').classList.add('show');
  }
}

function nextYear() { if(curYear < MAX_YEAR){ curYear++; updateSim(); } }

function resetSim() {
  curYear = 0; msNew = false; msCity = false;
  document.getElementById('ms-new').classList.remove('show');
  document.getElementById('ms-city').classList.remove('show');
  updateSim();
}

/* ══ TAB 3: CHALLENGE ══ */
let graphRevealed = false;

function checkAnswer() {
  const inp = document.getElementById('ch-inp');
  const fb  = document.getElementById('ch-fb');
  const val = parseInt(inp.value);
  inp.classList.remove('ok','bad'); fb.className='fb';

  if(isNaN(val)||val<1){ fb.textContent='⚠️ 숫자를 입력해주세요.'; fb.className='fb bad'; return; }

  if(val === ANSWER) {
    inp.classList.add('ok'); inp.disabled = true;
    fb.innerHTML = `🎉 정답! <strong>${ANSWER}년 후</strong>에 신도시 인구가 처음으로 100만 명을 넘어요!<br>
      <span style="font-size:.85em">${ANSWER}년 후 신도시 인구 ≈ ${fmtPop(POP[ANSWER][1])}</span>`;
    fb.className = 'fb ok';
    burst();
    setTimeout(revealGraph, 600);
  } else {
    inp.classList.add('bad');
    const hint = val < ANSWER ? '더 오래 걸려요. 시뮬레이션에서 다시 확인해봐요!' : '더 빨리 넘어요!';
    fb.textContent = '❌ 다시 생각해보세요. ' + hint;
    fb.className = 'fb bad';
  }
}

function revealGraph() {
  if(graphRevealed) return;
  graphRevealed = true;
  document.getElementById('reveal-wrap').style.display = 'none';
  document.getElementById('graph-hint').style.display = 'block';
  drawChart(true);
}

/* ══ CHART ══ */
function drawChart(full) {
  const canvas = document.getElementById('chart');
  const W = canvas.parentElement.clientWidth || 500;
  canvas.width = W;
  const H = 260;
  canvas.style.height = H + 'px';
  const ctx = canvas.getContext('2d');
  const pad = {t:20,r:16,b:38,l:58};
  const cw = W - pad.l - pad.r;
  const ch = H - pad.t - pad.b;
  const maxY = 3300000;
  const drawTo = full ? MAX_YEAR : 2;

  ctx.clearRect(0,0,W,H);

  // grid
  [0,500000,1000000,1500000,2000000,2500000,3000000].forEach(v => {
    const y = pad.t + ch - (v/maxY)*ch;
    ctx.strokeStyle = 'rgba(30,48,80,.5)'; ctx.lineWidth = 1; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(pad.l+cw,y); ctx.stroke();
    ctx.fillStyle='#334155'; ctx.font='10px monospace'; ctx.textAlign='right';
    ctx.fillText((v/10000)+'만', pad.l-5, y+4);
  });

  // 100만 dashed
  const ty = pad.t + ch - (TARGET/maxY)*ch;
  ctx.strokeStyle='#fbbf24'; ctx.lineWidth=1.5; ctx.setLineDash([6,4]);
  ctx.beginPath(); ctx.moveTo(pad.l,ty); ctx.lineTo(pad.l+cw,ty); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#fbbf24'; ctx.font='10px monospace'; ctx.textAlign='left';
  ctx.fillText('100만', pad.l+4, ty-4);

  // x axis labels
  ctx.fillStyle='#475569'; ctx.textAlign='center'; ctx.font='11px monospace';
  for(let i=0; i<=MAX_YEAR; i+=2){
    const x = pad.l + (i/MAX_YEAR)*cw;
    ctx.fillText(i+'년', x, H-6);
  }

  function drawLine(getV, color, upto) {
    ctx.strokeStyle=color; ctx.lineWidth=2.5; ctx.setLineDash([]);
    ctx.beginPath();
    for(let i=0;i<=upto;i++){
      const x=pad.l+(i/MAX_YEAR)*cw;
      const y=pad.t+ch-(getV(i)/maxY)*ch;
      i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
    }
    ctx.stroke();
    for(let i=0;i<=upto;i++){
      const x=pad.l+(i/MAX_YEAR)*cw;
      const y=pad.t+ch-(getV(i)/maxY)*ch;
      ctx.fillStyle=color; ctx.beginPath(); ctx.arc(x,y,3.5,0,Math.PI*2); ctx.fill();
    }
  }

  drawLine(i=>POP[i][0],'#38bdf8',drawTo);
  drawLine(i=>POP[i][1],'#10b981',drawTo);

  if(full) {
    // highlight answer year
    const ax = pad.l+(ANSWER/MAX_YEAR)*cw;
    const ay = pad.t+ch-(POP[ANSWER][1]/maxY)*ch;
    ctx.fillStyle='#fbbf24'; ctx.strokeStyle='#fbbf24'; ctx.lineWidth=2;
    ctx.beginPath(); ctx.arc(ax,ay,7,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#fbbf24'; ctx.font='bold 10px monospace'; ctx.textAlign='left';
    ctx.fillText(ANSWER+'년 후!', ax+9, ay-6);

    // vertical dashed at answer
    ctx.strokeStyle='rgba(245,158,11,.35)'; ctx.lineWidth=1; ctx.setLineDash([4,3]);
    ctx.beginPath(); ctx.moveTo(ax,pad.t); ctx.lineTo(ax,pad.t+ch); ctx.stroke();
    ctx.setLineDash([]);
  }

  // partial hint
  if(!full) {
    ctx.fillStyle='rgba(56,189,248,.15)';
    ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
    ctx.fillText('시뮬레이션을 진행하거나', W/2, H/2-6);
    ctx.fillText('정답을 맞히면 전체 그래프를 볼 수 있어요!', W/2, H/2+12);
  }
}

/* ══ PARTICLES ══ */
function burst() {
  const cols=['#22c55e','#fbbf24','#38bdf8','#a78bfa','#f87171','#fb923c'];
  const cx=window.innerWidth/2, cy=window.innerHeight/3;
  for(let i=0;i<24;i++){
    const p=document.createElement('div'); p.className='pt';
    const a=Math.random()*Math.PI*2, d=70+Math.random()*150;
    p.style.cssText=`left:${cx}px;top:${cy}px;background:${cols[i%6]};`+
      `width:${5+Math.random()*7}px;height:${5+Math.random()*7}px;`+
      `--tx:${Math.cos(a)*d}px;--ty:${Math.sin(a)*d-70}px;`+
      `animation-delay:${Math.random()*.15}s`;
    document.body.appendChild(p);
    setTimeout(()=>p.remove(),1150);
  }
}

/* ══ 3-CITY EXTENSION ══ */
const A3 = [[0.85,0.05,0.03],[0.08,0.83,0.02],[0.07,0.12,0.95]];
const INIT3 = [2000000, 1000000, 50000];
const POP3 = [INIT3.slice()];
for(let y3=1; y3<=MAX_YEAR; y3++){
  const p3=POP3[y3-1];
  POP3.push([
    A3[0][0]*p3[0]+A3[0][1]*p3[1]+A3[0][2]*p3[2],
    A3[1][0]*p3[0]+A3[1][1]*p3[1]+A3[1][2]*p3[2],
    A3[2][0]*p3[0]+A3[2][1]*p3[1]+A3[2][2]*p3[2]
  ]);
}
let curYear3=0, msNew3=false;

function buildMatCompare() {
  const m22=[['0.9','0.05'],['0.1','0.95']];
  const m33=[['0.85','0.05','0.03'],['0.08','0.83','0.02'],['0.07','0.12','0.95']];
  const mnn=[['a₁₁','···','a₁ₙ'],['⋮','⋱','⋮'],['aₙ₁','···','aₙₙ']];
  document.getElementById('mat-compare').innerHTML=`
    <div style="text-align:center">
      <div style="font-size:.78rem;font-weight:800;color:#38bdf8;margin-bottom:8px">2도시 → 2×2 행렬</div>
      ${matHtml(m22,'#38bdf8',56,40,'.82rem')}
    </div>
    <div style="font-size:1.6rem;color:#475569;align-self:center">→</div>
    <div style="text-align:center">
      <div style="font-size:.78rem;font-weight:800;color:#fbbf24;margin-bottom:8px">3도시 → 3×3 행렬</div>
      ${matHtml(m33,'#fbbf24',54,38,'.75rem')}
    </div>
    <div style="font-size:1.6rem;color:#475569;align-self:center">→</div>
    <div style="text-align:center">
      <div style="font-size:.78rem;font-weight:800;color:#a78bfa;margin-bottom:8px">n도시 → n×n 행렬</div>
      ${matHtml(mnn,'#a78bfa',54,38,'.78rem')}
    </div>`;
}

function buildMat3Display() {
  const m33=[['0.85','0.05','0.03'],['0.08','0.83','0.02'],['0.07','0.12','0.95']];
  const B3=[['200만'],['100만'],['5만']];
  document.getElementById('mat3-display').innerHTML=`
    <div style="font-size:.82rem;color:#64748b;margin-bottom:10px">
      전이행렬 A (3×3) &nbsp;×&nbsp; 초기 인구 B₀
    </div>
    <div style="display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap">
      ${matHtml(m33,'#fbbf24',58,40,'.78rem')}
      <span style="font-size:1.8rem;color:#475569;font-weight:900">×</span>
      ${matHtml(B3,'#38bdf8',70,40,'.82rem')}
    </div>`;
}

function buildBars3(y) {
  const [a,b,c]=POP3[y];
  const maxR=INIT3[0];
  const ap=Math.min(a/maxR*100,100).toFixed(1);
  const bp=Math.min(b/maxR*100,100).toFixed(1);
  const cp=Math.min(c/maxR*100,100).toFixed(1);
  return `
    <div class="bar-wrap">
      <div class="bar-label" style="color:#38bdf8">🏙️ A시 (광역시 A)</div>
      <div class="bar-track"><div class="bar-fill" style="width:${ap}%;background:linear-gradient(90deg,#1d4ed8,#38bdf8)">
        <span class="bar-val">${fmtPop(a)}</span></div></div>
    </div>
    <div class="bar-wrap">
      <div class="bar-label" style="color:#a78bfa">🏙️ B시 (광역시 B)</div>
      <div class="bar-track"><div class="bar-fill" style="width:${bp}%;background:linear-gradient(90deg,#6d28d9,#a78bfa)">
        <span class="bar-val">${fmtPop(b)}</span></div></div>
    </div>
    <div class="bar-wrap">
      <div class="bar-label" style="color:#10b981">🏘️ 신도시</div>
      <div class="bar-track"><div class="bar-fill" style="width:${cp}%;background:linear-gradient(90deg,#059669,#10b981)">
        <span class="bar-val">${fmtPop(c)}</span></div></div>
      ${c>=TARGET?`<div class="bar-note">★ 100만 명 돌파!</div>`:''}
    </div>`;
}

function buildEq3(fromY) {
  const [a0,b0,c0]=POP3[fromY];
  const [a1,b1,c1]=POP3[fromY+1];
  const Adisp=A3.map(r=>r.map(v=>v.toFixed(2)));
  const Bdisp=[[fmtMan(a0)],[fmtMan(b0)],[fmtMan(c0)]];
  const Rdisp=[[fmtMan(a1)],[fmtMan(b1)],[fmtMan(c1)]];
  document.getElementById('eq3-label').textContent=`A × B${fromY} = B${fromY+1} 계산 (단위: 만 명)`;
  document.getElementById('eq3-content').innerHTML=
    matHtml(Adisp,'#fbbf24',56,34,'.7rem')+
    `<span class="op" style="font-size:1.5rem">×</span>`+
    matHtml(Bdisp,'#38bdf8',62,34,'.75rem')+
    `<span class="op" style="font-size:1.5rem">=</span>`+
    matHtml(Rdisp,'#10b981',62,34,'.75rem');
}

function updateExt() {
  if(!document.getElementById('year3-badge')) return;
  document.getElementById('year3-badge').textContent=curYear3+'년';
  document.getElementById('ext-bars').innerHTML=buildBars3(curYear3);
  document.getElementById('btn-next3').disabled=(curYear3>=MAX_YEAR);
  if(curYear3>0){
    document.getElementById('ext-eq').style.display='block';
    buildEq3(curYear3-1);
  } else {
    document.getElementById('ext-eq').style.display='none';
  }
  if(!msNew3 && POP3[curYear3][2]>=TARGET){
    msNew3=true;
    document.getElementById('ms-new3-val').textContent=
      `${curYear3}년 후 신도시 인구 ≈ ${fmtPop(POP3[curYear3][2])}`;
    document.getElementById('ms-new3').classList.add('show');
    burst();
  }
}

function nextYear3(){ if(curYear3<MAX_YEAR){ curYear3++; updateExt(); } }

function resetExt(){
  curYear3=0; msNew3=false;
  document.getElementById('ms-new3').classList.remove('show');
  updateExt();
}

/* ══ TABS ══ */
function switchTab(tab) {
  ['setup','sim','chall','ext'].forEach(t=>{
    document.getElementById('panel-'+t).classList.toggle('on',t===tab);
    document.getElementById('tb-'+t).classList.toggle('on',t===tab);
  });
  if(tab==='chall') setTimeout(()=>drawChart(graphRevealed),60);
  if(tab==='ext') updateExt();
}

/* ══ INIT ══ */
buildSetup();
updateSim();
buildMatCompare();
buildMat3Display();
updateExt();
setTimeout(()=>drawChart(false),120);
</script>

<!-- ════ TAB 4 : 확장하기 ════ -->
<div class="panel" id="panel-ext">

  <div class="card">
    <div class="card-title">🔢 도시 수 → 행렬 크기</div>
    <div style="text-align:center;font-size:.85rem;color:#64748b;margin-bottom:14px;line-height:1.8">
      도시가 늘어날수록 행렬도 커져요 — 하지만 <strong style="color:#fbbf24">계산 원리는 동일</strong>해요!
    </div>
    <div style="display:flex;gap:12px;justify-content:center;align-items:flex-start;flex-wrap:wrap" id="mat-compare"></div>
    <div class="hint" style="margin-top:12px">
      💡 A의 <strong style="color:#fbbf24">(i행, j열) 성분</strong> = j번째 도시 인구 중 i번째 도시로 이동하는 비율<br>
      &nbsp;&nbsp;&nbsp;→ 각 <strong style="color:#a78bfa">열의 합 = 1</strong> (인구는 어딘가로 반드시 이동!)
    </div>
  </div>

  <div class="card">
    <div class="card-title">🌐 세 도시 시나리오</div>
    <div style="text-align:center;margin-bottom:4px">
      <svg viewBox="0 0 300 200" style="width:100%;max-width:320px;display:inline-block">
        <defs>
          <marker id="mg" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M0,0 L8,4 L0,8z" fill="#10b981"/>
          </marker>
          <marker id="mr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M0,0 L8,4 L0,8z" fill="#ef4444"/>
          </marker>
          <marker id="mb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M0,0 L8,4 L0,8z" fill="#38bdf8"/>
          </marker>
          <marker id="mp" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M0,0 L8,4 L0,8z" fill="#a78bfa"/>
          </marker>
        </defs>
        <!-- A시→B시 (green, 8%) -->
        <line x1="140" y1="47" x2="62" y2="146" stroke="#10b981" stroke-width="2" marker-end="url(#mg)"/>
        <!-- B시→A시 (red, 5%) -->
        <line x1="52" y1="143" x2="130" y2="44" stroke="#ef4444" stroke-width="2" marker-end="url(#mr)"/>
        <!-- A시→신도시 (blue, 7%) -->
        <line x1="160" y1="47" x2="238" y2="146" stroke="#38bdf8" stroke-width="2" marker-end="url(#mb)"/>
        <!-- 신도시→A시 (purple, 3%) -->
        <line x1="248" y1="143" x2="170" y2="44" stroke="#a78bfa" stroke-width="2" marker-end="url(#mp)"/>
        <!-- B시→신도시 (green, 12%) -->
        <line x1="76" y1="163" x2="222" y2="163" stroke="#10b981" stroke-width="2" marker-end="url(#mg)"/>
        <!-- 신도시→B시 (purple, 2%) -->
        <line x1="220" y1="173" x2="78" y2="173" stroke="#a78bfa" stroke-width="2" marker-end="url(#mp)"/>
        <!-- Arrow labels -->
        <text x="86" y="88" font-size="9.5" fill="#10b981" font-weight="bold">8%→</text>
        <text x="96" y="106" font-size="9.5" fill="#ef4444" font-weight="bold">←5%</text>
        <text x="196" y="88" font-size="9.5" fill="#38bdf8" font-weight="bold">7%→</text>
        <text x="184" y="106" font-size="9.5" fill="#a78bfa" font-weight="bold">←3%</text>
        <text x="128" y="159" font-size="9.5" fill="#10b981" font-weight="bold">12%→</text>
        <text x="128" y="182" font-size="9.5" fill="#a78bfa" font-weight="bold">←2%</text>
        <!-- City A box -->
        <rect x="115" y="8" width="70" height="36" rx="8" fill="rgba(56,189,248,.15)" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="150" y="23" text-anchor="middle" font-size="12" fill="#38bdf8" font-weight="bold">A시</text>
        <text x="150" y="37" text-anchor="middle" font-size="9" fill="#64748b">200만 명</text>
        <text x="150" y="52" text-anchor="middle" font-size="8" fill="#3d5878">85% 잔류</text>
        <!-- City B box -->
        <rect x="5" y="148" width="68" height="36" rx="8" fill="rgba(167,139,250,.15)" stroke="#a78bfa" stroke-width="1.5"/>
        <text x="39" y="163" text-anchor="middle" font-size="12" fill="#a78bfa" font-weight="bold">B시</text>
        <text x="39" y="177" text-anchor="middle" font-size="9" fill="#64748b">100만 명</text>
        <text x="39" y="192" text-anchor="middle" font-size="8" fill="#3d5878">83% 잔류</text>
        <!-- 신도시 box -->
        <rect x="227" y="148" width="68" height="36" rx="8" fill="rgba(16,185,129,.15)" stroke="#10b981" stroke-width="1.5"/>
        <text x="261" y="163" text-anchor="middle" font-size="12" fill="#10b981" font-weight="bold">신도시</text>
        <text x="261" y="177" text-anchor="middle" font-size="9" fill="#64748b">5만 명</text>
        <text x="261" y="192" text-anchor="middle" font-size="8" fill="#3d5878">95% 잔류</text>
      </svg>
    </div>
    <div style="text-align:center;margin-top:12px" id="mat3-display"></div>
  </div>

  <div class="card">
    <div class="card-title">📊 세 도시 인구 변화 시뮬레이션</div>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px">
      <div class="year-badge" id="year3-badge">0년</div>
      <button class="btn btn-go" id="btn-next3" onclick="nextYear3()">▶ 다음 해</button>
      <button class="btn btn-reset" onclick="resetExt()">↺ 처음으로</button>
    </div>
    <div id="ext-bars"></div>
    <div id="ext-eq" style="display:none">
      <div class="eq-area">
        <div class="eq-label" id="eq3-label"></div>
        <div class="eq-row" id="eq3-content" style="min-width:500px"></div>
      </div>
    </div>
    <div class="milestone" id="ms-new3" style="background:rgba(34,197,94,.08);border:2px solid #22c55e">
      <div style="font-size:2rem;margin-bottom:5px">🎉</div>
      <div style="font-size:1.1rem;font-weight:900;color:#4ade80">신도시 인구 100만 명 돌파!</div>
      <div style="font-size:.85rem;color:#64748b;margin-top:4px" id="ms-new3-val"></div>
    </div>
  </div>

  <div class="card" style="background:rgba(251,191,36,.04);border-color:rgba(251,191,36,.25)">
    <div class="card-title">💡 발견한 것들</div>
    <div style="font-size:.9rem;line-height:2.2;color:#94a3b8">
      <div>📐 도시가 <strong style="color:#fbbf24">n개</strong>이면 전이행렬은 <strong style="color:#fbbf24">n×n 행렬</strong></div>
      <div>🔁 계산 원리는 동일: <strong style="color:#a78bfa">B<sub>n+1</sub> = A × B<sub>n</sub></strong></div>
      <div>🌐 각 도시의 내년 인구는 <strong style="color:#38bdf8">현재 모든 도시</strong>의 인구로 결정됨</div>
      <div>🖥️ 수십~수백 개 도시 → 컴퓨터가 행렬 계산으로 순식간에 처리!</div>
    </div>
    <div style="background:#060c18;border-radius:10px;padding:12px;margin-top:10px;font-size:.82rem;color:#64748b;line-height:1.9">
      📊 <strong style="color:#fbbf24">두 시나리오 비교</strong><br>
      · 2도시 (광역시 300만 + 신도시 2만): 신도시 100만 돌파 → <strong style="color:#10b981">5년 후</strong><br>
      · 3도시 (A시 200만 + B시 100만 + 신도시 5만): 신도시 100만 돌파 → <strong style="color:#10b981">5년 후</strong><br>
      <span style="color:#475569">초기 조건과 행렬이 달라도 같은 결과가 나올 수 있어요!</span>
    </div>
  </div>

</div>
</body>
</html>"""


def render():
    st.markdown("### 🏙️ 행렬로 보는 두 도시 인구 이동")
    st.caption("전이행렬 Aⁿ을 이용해 두 도시의 인구 변화를 시뮬레이션하고, 신도시가 100만 명을 넘는 시기를 예측해봐요!")
    components.html(_HTML, height=1700, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
