import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "기댓값분산표준편차"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 기댓값 · 분산 · 표준편차 탐험 성찰**"},
    {"key": "기댓값의미",   "label": "💭 기댓값 E(X)는 어떤 의미인지 자신의 말로 설명해 보세요.",
     "type": "text_area", "height": 80},
    {"key": "분산표준편차", "label": "📊 분산 V(X)와 표준편차 σ(X)의 차이는 무엇이고, 표준편차가 더 유용한 이유는?",
     "type": "text_area", "height": 80},
    {"key": "axb변환",     "label": "🔄 aX+b 변환에서 b를 아무리 바꿔도 분산이 변하지 않는 이유를 설명해 보세요.",
     "type": "text_area", "height": 80},
    {"key": "실생활사례",  "label": "🌍 기댓값 개념을 활용할 수 있는 실생활 사례를 하나 만들어 보세요.",
     "type": "text_area", "height": 80},
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",         "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title":       "미니: 기댓값·분산·표준편차 탐험",
    "description": "실생활 시나리오로 E(X), V(X), σ(X)와 aX+b 변환을 시각적으로 탐험합니다.",
    "order":       999,
    "hidden":      True,
}

_HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);padding:14px 12px;color:#e2e8f0}

.hero{text-align:center;background:linear-gradient(135deg,rgba(251,191,36,.1),rgba(245,101,101,.07));border:1px solid rgba(251,191,36,.22);border-radius:20px;padding:18px 16px;margin-bottom:14px}
.hero h1{font-size:19px;font-weight:900;color:#fbbf24;text-shadow:0 0 24px rgba(251,191,36,.45)}
.hero p{font-size:11px;color:#94a3b8;margin-top:5px}

.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:16px 18px;margin:11px 0;backdrop-filter:blur(8px)}
.card-title{font-size:13px;font-weight:700;color:#fbbf24;margin-bottom:11px;display:flex;align-items:center;gap:7px}

/* Scenario selector */
.sc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:10px}
.sc-btn{background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.1);border-radius:15px;padding:13px 7px;cursor:pointer;text-align:center;transition:all .22s;color:#e2e8f0;user-select:none}
.sc-btn:hover{background:rgba(251,191,36,.1);border-color:rgba(251,191,36,.35);transform:translateY(-2px)}
.sc-btn.active{background:rgba(251,191,36,.14);border-color:#fbbf24;box-shadow:0 0 16px rgba(251,191,36,.2)}
.sc-icon{font-size:28px;margin-bottom:5px}
.sc-name{font-size:12px;font-weight:700;color:#fbbf24}
.sc-desc{font-size:10px;color:#94a3b8;margin-top:2px}

.ctx-box{font-size:12px;color:#cbd5e1;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:9px 13px;margin:8px 0;line-height:1.5}

/* Probability table */
table{width:100%;border-collapse:collapse;margin:9px 0;font-size:12px}
th{background:rgba(251,191,36,.14);color:#fbbf24;padding:7px 5px;text-align:center;border:1px solid rgba(255,255,255,.08);font-weight:700}
td{background:rgba(255,255,255,.03);color:#e2e8f0;padding:7px 5px;text-align:center;border:1px solid rgba(255,255,255,.06);font-family:monospace;font-size:12px}

/* Stats row */
.stats-row{display:flex;gap:9px;flex-wrap:wrap;margin:11px 0}
.stat-card{flex:1;min-width:95px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:13px;padding:13px 9px;text-align:center;transition:all .4s}
.stat-card.pop{background:rgba(251,191,36,.15);border-color:rgba(251,191,36,.4);transform:scale(1.04)}
.stat-lbl{font-size:10px;color:#94a3b8;font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin-bottom:5px}
.stat-val{font-size:23px;font-weight:900;color:#fbbf24;font-family:monospace}
.stat-fml{font-size:9px;color:#475569;margin-top:4px}

/* Tabs */
.tab-bar{display:flex;gap:7px;margin-bottom:11px}
.tab-btn{padding:6px 14px;border-radius:9px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04);cursor:pointer;font-size:12px;font-weight:600;color:#94a3b8;transition:.2s}
.tab-btn.active{background:rgba(251,191,36,.2);color:#fbbf24;border-color:rgba(251,191,36,.4)}

/* Steps */
.step-wrap{display:flex;flex-direction:column;gap:5px}
.step-item{display:flex;align-items:flex-start;gap:8px;padding:8px 12px;background:rgba(255,255,255,.03);border-radius:9px;border-left:3px solid rgba(99,102,241,.4);font-size:11px;font-family:monospace;color:#cbd5e1;opacity:0;transform:translateX(-7px);transition:all .32s}
.step-item.vis{opacity:1;transform:translateX(0)}
.step-num{background:rgba(99,102,241,.3);color:#a5b4fc;border-radius:5px;padding:2px 7px;font-size:10px;font-weight:700;flex-shrink:0;min-width:48px;text-align:center}

/* Sliders */
.slider-row{display:flex;align-items:center;gap:11px;margin:8px 0;flex-wrap:wrap}
.slider-lbl{font-size:12px;font-weight:700;color:#e2e8f0;min-width:85px;display:flex;align-items:center;gap:6px}
input[type=range]{flex:1;min-width:130px;-webkit-appearance:none;height:7px;border-radius:4px;background:linear-gradient(90deg,#6366f1,#a855f7);outline:none;cursor:pointer}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:19px;height:19px;border-radius:50%;background:#fff;border:3px solid #6366f1;cursor:pointer;box-shadow:0 0 8px rgba(99,102,241,.5)}
.slider-val{min-width:42px;background:linear-gradient(135deg,#6366f1,#a855f7);border-radius:8px;padding:2px 9px;font-weight:800;font-size:14px;text-align:center;color:#fff}

/* Transform boxes */
.tf-grid{display:grid;grid-template-columns:1fr 40px 1fr;gap:7px;align-items:center;margin-top:13px}
.tf-box{border-radius:13px;padding:11px}
.tf-box.orig{background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3)}
.tf-box.trsf{background:rgba(168,85,247,.1);border:1px solid rgba(168,85,247,.3)}
.tf-box .lbl{font-size:10px;color:#94a3b8;margin-bottom:5px;text-align:center;font-weight:600}
.tf-box .line{font-size:11px;font-family:monospace;line-height:1.75;text-align:center}
.tf-box.orig .line{color:#a5b4fc}
.tf-box.trsf .line{color:#d8b4fe}
.tf-arrow{text-align:center;font-size:26px;color:#fbbf24}

.fml-row{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
.fml-chip{flex:1;min-width:120px;background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.2);border-radius:9px;padding:7px;text-align:center;font-size:10px;color:#fde68a;font-family:monospace;line-height:1.5}

/* mean line badge */
.mean-badge{display:inline-block;background:rgba(251,191,36,.15);border:1px solid rgba(251,191,36,.3);border-radius:8px;padding:3px 10px;font-size:11px;color:#fde68a;margin:5px 0}

::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(251,191,36,.4);border-radius:3px}
</style>
</head>
<body>

<div class="hero">
  <h1>📊 이산확률변수의 기댓값 · 분산 · 표준편차</h1>
  <p>실생활 시나리오를 선택해 E(X), V(X), σ(X)를 직접 탐험해 보세요</p>
</div>

<!-- ① 시나리오 선택 -->
<div class="card">
  <div class="card-title">🌍 실생활 시나리오 선택</div>
  <div class="sc-grid">
    <div class="sc-btn active" onclick="selectSc(0)">
      <div class="sc-icon">🏪</div>
      <div class="sc-name">편의점 뽑기</div>
      <div class="sc-desc">당첨 금액의 기댓값</div>
    </div>
    <div class="sc-btn" onclick="selectSc(1)">
      <div class="sc-icon">☔</div>
      <div class="sc-name">우산 판매</div>
      <div class="sc-desc">날씨별 하루 판매량</div>
    </div>
    <div class="sc-btn" onclick="selectSc(2)">
      <div class="sc-icon">🎮</div>
      <div class="sc-name">게임 보상</div>
      <div class="sc-desc">몬스터 처치 포인트</div>
    </div>
  </div>
  <div id="ctxBox" class="ctx-box"></div>
  <div id="tblWrap"></div>
</div>

<!-- ② 확률분포 그래프 -->
<div class="card">
  <div class="card-title">📈 확률분포 그래프</div>
  <canvas id="distChart" height="140"></canvas>
</div>

<!-- ③ 통계량 계산 -->
<div class="card">
  <div class="card-title">🔢 기댓값 · 분산 · 표준편차</div>
  <div class="tab-bar">
    <button class="tab-btn active" id="btnRes"  onclick="showTab('res')">📐 결과 보기</button>
    <button class="tab-btn"        id="btnStep" onclick="showTab('step')">🪜 계산 과정</button>
  </div>
  <div id="tabRes">
    <div class="stats-row">
      <div class="stat-card" id="cardE">
        <div class="stat-lbl">기댓값 E(X)</div>
        <div class="stat-val" id="valE">—</div>
        <div class="stat-fml">Σ xᵢpᵢ</div>
      </div>
      <div class="stat-card" id="cardV">
        <div class="stat-lbl">분산 V(X)</div>
        <div class="stat-val" id="valV">—</div>
        <div class="stat-fml">E(X²) − {E(X)}²</div>
      </div>
      <div class="stat-card" id="cardS">
        <div class="stat-lbl">표준편차 σ(X)</div>
        <div class="stat-val" id="valS">—</div>
        <div class="stat-fml">√V(X)</div>
      </div>
    </div>
  </div>
  <div id="tabStep" style="display:none">
    <div id="stepList" class="step-wrap"></div>
  </div>
</div>

<!-- ④ aX+b 변환 실험실 -->
<div class="card">
  <div class="card-title">🔄 <em>aX + b</em> 변환 실험실</div>
  <div style="font-size:11px;color:#94a3b8;margin-bottom:10px">슬라이더로 a, b를 바꿔 평균·분산·표준편차가 어떻게 달라지는지 확인하세요.</div>
  <div class="slider-row">
    <span class="slider-lbl">a&nbsp;= <span id="aVal" class="slider-val">2</span></span>
    <input type="range" id="aSlider" min="-4" max="5" step="0.5" value="2" oninput="updateTF()">
  </div>
  <div class="slider-row">
    <span class="slider-lbl">b&nbsp;= <span id="bVal" class="slider-val">3</span></span>
    <input type="range" id="bSlider" min="-20" max="30" step="1" value="3" oninput="updateTF()">
  </div>
  <div id="tfResult"></div>
  <div style="margin-top:12px">
    <canvas id="tfChart" height="140"></canvas>
  </div>
</div>

<script>
/* ── E(X) 수직선 플러그인 ──────────────────────────────── */
const meanLinePlugin = {
  id: 'meanLine',
  afterDatasetsDraw(chart) {
    const opts = chart.options.plugins && chart.options.plugins.meanLine;
    if (!opts || opts.x === undefined) return;
    const meta = chart.getDatasetMeta(0);
    if (!meta || !meta.data || !meta.data.length) return;
    const bars = meta.data;
    const vals = opts.vals;
    const meanX = opts.x;
    let px = null;
    if (meanX <= vals[0]) px = bars[0].x;
    else if (meanX >= vals[vals.length-1]) px = bars[bars.length-1].x;
    else {
      for (let i = 0; i < vals.length-1; i++) {
        if (meanX >= vals[i] && meanX <= vals[i+1]) {
          const t = (meanX - vals[i]) / (vals[i+1] - vals[i]);
          px = bars[i].x + t * (bars[i+1].x - bars[i].x);
          break;
        }
      }
    }
    if (px === null) return;
    const ctx = chart.ctx;
    const {top, bottom} = chart.chartArea;
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(px, top + 2);
    ctx.lineTo(px, bottom);
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 2.5;
    ctx.setLineDash([6, 4]);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.font = 'bold 11px Segoe UI,sans-serif';
    ctx.fillStyle = '#0f2027';
    ctx.textAlign = 'center';
    const lbl = 'E(X)=' + opts.label;
    const tw = ctx.measureText(lbl).width;
    ctx.fillRect(px - tw/2 - 4, top - 1, tw + 8, 16);
    ctx.fillStyle = '#fbbf24';
    ctx.fillText(lbl, px, top + 12);
    ctx.restore();
  }
};
Chart.register(meanLinePlugin);

/* ── 데이터 ─────────────────────────────────────────────── */
const SC = [
  {
    name:"편의점 뽑기", icon:"🏪",
    context:"🏪 한 편의점에서 500원짜리 뽑기를 운영합니다. 뽑기 한 번에 기대할 수 있는 당첨 금액은 얼마일까요? 뽑기를 500원에 사도 이득일까요?",
    unit:"원", xlabel:"당첨 금액 X (원)",
    values:[0, 500, 1000, 3000, 5000],
    probs:[0.40, 0.30, 0.15, 0.10, 0.05],
    color:"#fbbf24"
  },
  {
    name:"우산 판매", icon:"☔",
    context:"☔ 어느 상점의 하루 우산 판매량 X의 확률분포입니다. 날씨가 맑으면 적게, 비가 오면 많이 팔립니다. 평균 판매량과 판매량의 변동성을 알아볼까요?",
    unit:"개", xlabel:"하루 판매량 X (개)",
    values:[0, 1, 2, 3, 4],
    probs:[0.10, 0.20, 0.40, 0.20, 0.10],
    color:"#38bdf8"
  },
  {
    name:"게임 보상", icon:"🎮",
    context:"🎮 RPG 게임에서 몬스터를 처치할 때 얻는 포인트 X의 확률분포입니다. 평균적으로 얼마를 획득할 수 있을까요? 포인트가 들쭉날쭉한 정도는?",
    unit:"pt", xlabel:"획득 포인트 X",
    values:[10, 20, 50, 100, 200],
    probs:[0.35, 0.30, 0.20, 0.10, 0.05],
    color:"#a78bfa"
  }
];

let cur = 0;
let distChart = null;
let tfChart = null;

/* ── 유틸 ─────────────────────────────────────────────── */
function r3(x){ return Math.round(x * 1000) / 1000; }
function fmt(x){
  const v = r3(x);
  if(Number.isInteger(v)) return v.toLocaleString('ko-KR');
  return v.toLocaleString('ko-KR', {maximumFractionDigits:3});
}
function calcStats(sc){
  const E  = sc.values.reduce((s,x,i) => s + x * sc.probs[i], 0);
  const E2 = sc.values.reduce((s,x,i) => s + x * x * sc.probs[i], 0);
  const V  = E2 - E * E;
  const S  = Math.sqrt(V < 1e-12 ? 0 : V);
  return {E, V, S, E2};
}

/* ── 시나리오 선택 ──────────────────────────────────────── */
function selectSc(idx){
  cur = idx;
  document.querySelectorAll('.sc-btn').forEach((b,i) => {
    b.className = 'sc-btn' + (i === idx ? ' active' : '');
  });
  update();
}

/* ── 확률표 생성 ─────────────────────────────────────────── */
function buildTable(sc){
  let h = `<table><thead><tr><th>X</th>`;
  sc.values.forEach(v => h += `<th>${v.toLocaleString()}</th>`);
  h += `<th>합계</th></tr></thead><tbody><tr><th>P</th>`;
  sc.probs.forEach(p => h += `<td>${p}</td>`);
  h += `<td>1</td></tr></tbody></table>`;
  return h;
}

/* ── 분포 차트 ──────────────────────────────────────────── */
function buildDistChart(sc){
  const ctx = document.getElementById('distChart').getContext('2d');
  if(distChart) distChart.destroy();
  const {E} = calcStats(sc);
  distChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sc.values.map(v => v.toLocaleString() + ' ' + sc.unit),
      datasets: [{
        label: 'P(X = x)',
        data: sc.probs,
        backgroundColor: sc.color + '88',
        borderColor: sc.color,
        borderWidth: 2,
        borderRadius: 8,
      }]
    },
    options: {
      responsive: true,
      animation: {duration: 600},
      plugins: {
        legend: {labels: {color:'#e2e8f0', font:{size:12}}},
        tooltip: {callbacks: {label: c => `확률: ${c.parsed.y}`}},
        meanLine: {x: E, vals: sc.values, label: fmt(E) + ' ' + sc.unit}
      },
      scales: {
        x: {ticks:{color:'#94a3b8'}, grid:{color:'rgba(255,255,255,.05)'}},
        y: {
          beginAtZero: true,
          ticks: {color:'#94a3b8'},
          grid: {color:'rgba(255,255,255,.05)'},
          title: {display:true, text:'확률 P', color:'#94a3b8'}
        }
      }
    }
  });
}

/* ── 변환 차트 ──────────────────────────────────────────── */
function buildTfChart(sc, a, b){
  const newVals = sc.values.map(x => r3(a * x + b));
  const ctx = document.getElementById('tfChart').getContext('2d');
  if(tfChart) tfChart.destroy();
  tfChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sc.values.map((v,i) => `${v} → ${newVals[i]}`),
      datasets: [
        {
          label: 'X (원본)',
          data: sc.probs,
          backgroundColor: sc.color + '55',
          borderColor: sc.color,
          borderWidth: 2,
          borderRadius: 6,
        },
        {
          label: `aX+b (a=${a}, b=${b})`,
          data: sc.probs,
          backgroundColor: '#f4729455',
          borderColor: '#f47294',
          borderWidth: 2,
          borderRadius: 6,
        }
      ]
    },
    options: {
      responsive: true,
      animation: {duration: 400},
      plugins: {
        legend: {labels: {color:'#e2e8f0', font:{size:11}}},
        tooltip: {callbacks: {label: c => `확률: ${c.parsed.y}`}}
      },
      scales: {
        x: {ticks:{color:'#94a3b8', font:{size:10}}, grid:{color:'rgba(255,255,255,.05)'}},
        y: {beginAtZero:true, ticks:{color:'#94a3b8'}, grid:{color:'rgba(255,255,255,.05)'}}
      }
    }
  });
}

/* ── 계산 과정 생성 ──────────────────────────────────────── */
function buildSteps(sc){
  const {E, V, S, E2} = calcStats(sc);
  const pe  = sc.values.map((x,i) => `${x.toLocaleString()}×${sc.probs[i]}`).join(' + ');
  const pe2 = sc.values.map((x,i) => `${(x*x).toLocaleString()}×${sc.probs[i]}`).join(' + ');
  return [
    {n:'① E(X)',  t:`E(X) = Σ xᵢpᵢ = ${pe}`},
    {n:'   =',    t:`= ${fmt(E)} (${sc.unit})`},
    {n:'② E(X²)', t:`E(X²) = Σ xᵢ²pᵢ = ${pe2}`},
    {n:'   =',    t:`= ${fmt(E2)}`},
    {n:'③ V(X)',  t:`V(X) = E(X²) − {E(X)}² = ${fmt(E2)} − (${fmt(E)})² = ${fmt(E2)} − ${fmt(E*E)} = ${fmt(V)}`},
    {n:'④ σ(X)',  t:`σ(X) = √V(X) = √${fmt(V)} ≈ ${fmt(S)} (${sc.unit})`},
  ];
}

/* ── 탭 전환 ────────────────────────────────────────────── */
function showTab(tab){
  document.getElementById('tabRes').style.display  = tab==='res'  ? '' : 'none';
  document.getElementById('tabStep').style.display = tab==='step' ? '' : 'none';
  document.getElementById('btnRes').className  = 'tab-btn' + (tab==='res'  ? ' active' : '');
  document.getElementById('btnStep').className = 'tab-btn' + (tab==='step' ? ' active' : '');
  if(tab === 'step'){
    const sl = document.getElementById('stepList');
    sl.innerHTML = '';
    buildSteps(SC[cur]).forEach((s, i) => {
      const d = document.createElement('div');
      d.className = 'step-item';
      d.innerHTML = `<span class="step-num">${s.n}</span><span>${s.t}</span>`;
      sl.appendChild(d);
      setTimeout(() => d.classList.add('vis'), i * 140);
    });
  }
}

/* ── aX+b 변환 갱신 ─────────────────────────────────────── */
function updateTF(){
  const a = parseFloat(document.getElementById('aSlider').value);
  const b = parseFloat(document.getElementById('bSlider').value);
  document.getElementById('aVal').textContent = a;
  document.getElementById('bVal').textContent = b;

  const sc = SC[cur];
  const {E, V, S} = calcStats(sc);
  const nE = r3(a * E + b);
  const nV = r3(a * a * V);
  const nS = r3(Math.abs(a) * S);

  const aDisp = a < 0 ? `(${a})` : `${a}`;
  document.getElementById('tfResult').innerHTML = `
    <div class="tf-grid">
      <div class="tf-box orig">
        <div class="lbl">X 의 통계량</div>
        <div class="line">E(X) = ${fmt(E)}</div>
        <div class="line">V(X) = ${fmt(V)}</div>
        <div class="line">σ(X) = ${fmt(S)}</div>
      </div>
      <div class="tf-arrow">⟹</div>
      <div class="tf-box trsf">
        <div class="lbl">${a}X + ${b} 의 통계량</div>
        <div class="line">E = ${aDisp}×${fmt(E)} + ${b} = ${fmt(nE)}</div>
        <div class="line">V = ${aDisp}²×${fmt(V)} = ${fmt(nV)}</div>
        <div class="line">σ = |${a}|×${fmt(S)} = ${fmt(nS)}</div>
      </div>
    </div>
    <div class="fml-row">
      <div class="fml-chip">E(aX+b)<br>= a·E(X) + b</div>
      <div class="fml-chip">V(aX+b)<br>= a²·V(X)</div>
      <div class="fml-chip">σ(aX+b)<br>= |a|·σ(X)</div>
    </div>`;
  buildTfChart(sc, a, b);
}

/* ── 전체 갱신 ──────────────────────────────────────────── */
function popCard(id){
  const el = document.getElementById(id);
  el.classList.add('pop');
  setTimeout(() => el.classList.remove('pop'), 600);
}

function update(){
  const sc = SC[cur];
  document.getElementById('ctxBox').textContent = sc.context;
  document.getElementById('tblWrap').innerHTML  = buildTable(sc);

  const {E, V, S} = calcStats(sc);
  document.getElementById('valE').textContent = fmt(E);
  document.getElementById('valV').textContent = fmt(V);
  document.getElementById('valS').textContent = fmt(S);
  ['cardE','cardV','cardS'].forEach(id => popCard(id));

  buildDistChart(sc);
  updateTF();

  if(document.getElementById('tabStep').style.display !== 'none') showTab('step');
}

window.addEventListener('load', update);
</script>
</body>
</html>
"""


def render():
    st.header("📊 이산확률변수의 기댓값 · 분산 · 표준편차")
    components.html(_HTML, height=2400, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
