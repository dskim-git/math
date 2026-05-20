# activities/probability_new/mini/pop_sample_mean_lab.py
"""
모평균과 표본평균 — 비밀 모집단 추적 시뮬레이션 + 전국 미세먼지 지도 표본 추출
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎯 모평균 vs 표본평균 — 비밀 모집단 추적",
    "description": "비밀 모집단에서 표본을 뽑아 표본평균을 계산해 보며 모평균과 표본평균의 관계를 탐구합니다.",
    "order": 5,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "모평균표본평균추적"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 모평균 vs 표본평균**"},
    {
        "key": "모평균표본평균차이",
        "label": "활동을 통해 알게 된 **모평균(m)**과 **표본평균(X̄)**의 차이는 무엇인가요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "모평균은 ___이고, 표본평균은 ___이다. 모평균은 고정된 ___이지만, 표본평균은 ___...",
    },
    {
        "key": "표본평균변화",
        "label": "같은 모집단에서 표본을 여러 번 뽑았을 때, 표본평균 X̄ 값은 어떻게 변했나요? 왜 그런 결과가 나왔다고 생각하나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "표본을 뽑을 때마다 X̄ 값이 ___, 왜냐하면...",
    },
    {
        "key": "표본크기영향",
        "label": "표본의 크기 n을 작게(예: n=3) 했을 때와 크게(예: n=30) 했을 때 표본평균의 분포는 어떻게 달랐나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "n이 작을수록 ___, n이 클수록 ___ 했다. 즉 n이 커지면 표본평균이...",
    },
    {
        "key": "미세먼지비교",
        "label": "미세먼지 지도 활동에서, 친구와 똑같이 3개 시도를 임의추출했는데도 표본평균이 서로 달랐던 이유는 무엇일까요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "친구와 내가 뽑은 표본이 서로 ___ 때문이다. 즉 표본평균은...",
    },
    {
        "key": "확률변수이해",
        "label": "왜 표본평균 X̄을 '확률변수'라고 부르는지, 이번 활동을 바탕으로 설명해 보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "표본평균은 표본을 어떻게 뽑는지에 따라 ___ 값을 가지므로...",
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
# TAB 1: 비밀 모집단 추적 시뮬레이션
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
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0f172a 100%);
  color:#e2e8f0;padding:16px 12px;min-height:100vh;
}
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(168,85,247,.15));
  border:2px solid rgba(56,189,248,.4);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.45rem;font-weight:900;color:#38bdf8;margin-bottom:4px}
.hdr p{font-size:.98rem;color:#cbd5e1;line-height:1.55}

.layout{display:grid;grid-template-columns:1fr 360px;gap:14px}
@media(max-width:900px){.layout{grid-template-columns:1fr}}

.panel{
  background:rgba(15,23,42,.7);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px;
}
.panel h2{
  font-size:1.05rem;font-weight:800;color:#a5b4fc;margin-bottom:10px;
  display:flex;align-items:center;gap:8px;
}

/* ===== 모집단 시각화 ===== */
.pop-wrap{
  position:relative;width:100%;aspect-ratio:1.55;
  background:radial-gradient(ellipse at center,rgba(30,41,59,.85),rgba(15,23,42,.95));
  border:2px solid rgba(99,102,241,.35);border-radius:14px;overflow:hidden;
}
.pop-label{
  position:absolute;top:8px;left:12px;font-size:.85rem;font-weight:800;
  color:#94a3b8;background:rgba(15,23,42,.7);padding:3px 9px;border-radius:8px;
  letter-spacing:.5px;z-index:5;
}
.pop-info{
  position:absolute;top:8px;right:12px;font-size:.9rem;font-weight:900;
  color:#fbbf24;background:rgba(15,23,42,.85);padding:5px 12px;border-radius:8px;
  border:1.5px solid rgba(251,191,36,.4);z-index:5;display:none;
}
.pop-info.on{display:block;animation:fadeIn .3s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}

#popCanvas{display:block;width:100%;height:100%}

/* ===== 표본 박스 ===== */
.sample-box{
  margin-top:12px;background:rgba(34,197,94,.08);
  border:2px solid rgba(34,197,94,.4);border-radius:12px;padding:12px;
  min-height:90px;position:relative;
}
.sb-title{
  font-size:.95rem;font-weight:800;color:#86efac;margin-bottom:8px;
  display:flex;justify-content:space-between;align-items:center;
}
.sb-mean{color:#fef3c7;font-weight:900;font-size:1.1rem}
.sb-list{
  display:flex;flex-wrap:wrap;gap:6px;min-height:32px;
}
.sb-chip{
  display:inline-flex;align-items:center;justify-content:center;
  min-width:42px;height:30px;padding:0 8px;border-radius:8px;
  font-size:.88rem;font-weight:800;color:#1e293b;
  animation:chipIn .3s cubic-bezier(.34,1.56,.64,1);
}
@keyframes chipIn{from{opacity:0;transform:scale(.3) translateY(-10px)}to{opacity:1;transform:scale(1) translateY(0)}}
.sb-empty{color:#64748b;font-size:.9rem;font-style:italic;padding:6px 0}

/* ===== 컨트롤 ===== */
.controls{
  display:flex;flex-direction:column;gap:10px;margin-bottom:12px;
}
.ctrl-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.ctrl-label{
  font-size:.92rem;font-weight:800;color:#a5b4fc;min-width:80px;
}
.ctrl-range{flex:1;min-width:140px;accent-color:#38bdf8}
.ctrl-value{
  font-size:1rem;font-weight:900;color:#fbbf24;min-width:55px;
  background:rgba(15,23,42,.6);padding:3px 10px;border-radius:8px;text-align:center;
}

.btn{
  flex:1;min-width:120px;
  padding:10px 14px;border:none;border-radius:11px;cursor:pointer;
  font-size:.98rem;font-weight:900;color:#fff;
  transition:all .15s ease;letter-spacing:.3px;
}
.btn:active{transform:scale(.96)}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btn-pri{background:linear-gradient(135deg,#3b82f6,#1d4ed8);box-shadow:0 3px 10px rgba(59,130,246,.4)}
.btn-pri:hover:not(:disabled){background:linear-gradient(135deg,#2563eb,#1e40af);transform:translateY(-1px)}
.btn-sec{background:linear-gradient(135deg,#a855f7,#7c3aed);box-shadow:0 3px 10px rgba(168,85,247,.4)}
.btn-sec:hover:not(:disabled){background:linear-gradient(135deg,#9333ea,#6d28d9);transform:translateY(-1px)}
.btn-rev{background:linear-gradient(135deg,#f97316,#ea580c)}
.btn-rev:hover:not(:disabled){background:linear-gradient(135deg,#ea580c,#c2410c)}
.btn-ghost{background:rgba(71,85,105,.6);border:1.5px solid rgba(148,163,184,.3)}
.btn-ghost:hover:not(:disabled){background:rgba(71,85,105,.9)}

.btn-row{display:flex;gap:8px;flex-wrap:wrap}

/* ===== 통계 카드 ===== */
.stats-grid{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;
}
.stat-card{
  background:rgba(30,41,59,.7);border:1.5px solid rgba(99,102,241,.3);
  border-radius:11px;padding:10px;text-align:center;position:relative;
}
.stat-card.pop{border-color:rgba(251,113,133,.5);background:rgba(244,63,94,.1)}
.stat-card.sample{border-color:rgba(56,189,248,.5);background:rgba(14,165,233,.1)}
.sc-label{font-size:.78rem;font-weight:700;color:#94a3b8;margin-bottom:4px;letter-spacing:.3px}
.sc-val{font-size:1.55rem;font-weight:900;letter-spacing:.5px}
.stat-card.pop .sc-val{color:#fb7185}
.stat-card.sample .sc-val{color:#38bdf8}
.sc-sub{font-size:.78rem;color:#94a3b8;margin-top:3px}
.locked{filter:blur(6px);user-select:none;color:#64748b !important}

/* ===== 히스토그램 ===== */
.histo-wrap{position:relative}
.histo-info{
  font-size:.85rem;color:#cbd5e1;margin-bottom:8px;
  display:flex;justify-content:space-between;align-items:center;
}
.histo-info .cnt{color:#fbbf24;font-weight:900}
#histoCanvas{
  display:block;width:100%;height:200px;
  background:rgba(15,23,42,.6);border:1.5px solid rgba(99,102,241,.25);
  border-radius:10px;
}

/* ===== 미니 결과 ===== */
.recent{
  margin-top:10px;font-size:.85rem;color:#cbd5e1;
  background:rgba(15,23,42,.5);border-radius:8px;padding:8px 10px;
  border:1px solid rgba(99,102,241,.2);
  max-height:80px;overflow-y:auto;
}
.recent-item{
  display:inline-block;margin:2px 4px;padding:2px 8px;
  background:rgba(56,189,248,.15);border:1px solid rgba(56,189,248,.35);
  border-radius:6px;font-weight:700;color:#7dd3fc;font-size:.85rem;
}
.recent-empty{color:#64748b;font-style:italic;font-size:.82rem}

.hint{
  margin-top:12px;background:rgba(168,85,247,.12);
  border:1.5px solid rgba(168,85,247,.35);border-radius:10px;
  padding:10px 12px;font-size:.88rem;color:#e9d5ff;line-height:1.6;
}
.hint b{color:#c4b5fd}

/* ===== flash animation ===== */
.flash{animation:flash .8s ease}
@keyframes flash{
  0%,100%{box-shadow:0 0 0 0 rgba(251,191,36,0)}
  30%{box-shadow:0 0 0 8px rgba(251,191,36,.4)}
}
</style>
</head>
<body>

<div class="hdr">
  <h1>🎯 비밀 모집단을 추적하라!</h1>
  <p>200명의 학생들의 <b>수학 점수 모집단</b>에서 표본을 뽑아 <b>모평균 m</b>의 정체를 알아내 봐요.</p>
</div>

<div class="layout">
  <!-- 좌: 모집단 시각화 + 표본 -->
  <div class="panel">
    <h2>🔬 모집단 (Population)</h2>
    <div class="pop-wrap">
      <div class="pop-label">📊 200명의 점수 분포</div>
      <div class="pop-info" id="popInfo">진짜 모평균 m = <span id="popMean">--</span></div>
      <canvas id="popCanvas" width="700" height="450"></canvas>
    </div>

    <div class="sample-box" id="sampleBox">
      <div class="sb-title">
        <span>📦 이번에 뽑은 표본</span>
        <span class="sb-mean" id="curMean">X̄ = --</span>
      </div>
      <div class="sb-list" id="sbList">
        <div class="sb-empty">아직 표본을 뽑지 않았어요. 오른쪽에서 표본을 뽑아 보세요 →</div>
      </div>
    </div>
  </div>

  <!-- 우: 컨트롤 + 통계 -->
  <div class="panel">
    <h2>🎲 표본 추출 (Sampling)</h2>

    <div class="controls">
      <div class="ctrl-row">
        <span class="ctrl-label">표본 크기 n</span>
        <input type="range" min="3" max="50" value="10" class="ctrl-range" id="nRange">
        <span class="ctrl-value" id="nVal">10</span>
      </div>
      <div class="btn-row">
        <button class="btn btn-pri" id="btnDraw">🎲 표본 1번 뽑기</button>
        <button class="btn btn-sec" id="btnDraw50">⚡ 50번 뽑기</button>
      </div>
      <div class="btn-row">
        <button class="btn btn-rev" id="btnReveal">🔍 모평균 m 공개</button>
        <button class="btn btn-ghost" id="btnReset">🔄 처음부터</button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card pop">
        <div class="sc-label">모평균 m</div>
        <div class="sc-val locked" id="mDisplay">??.?</div>
        <div class="sc-sub">고정된 상수</div>
      </div>
      <div class="stat-card sample">
        <div class="sc-label">최근 표본평균 X̄</div>
        <div class="sc-val" id="xbarDisplay">--</div>
        <div class="sc-sub" id="diffDisplay">차이: --</div>
      </div>
    </div>

    <div class="histo-wrap">
      <div class="histo-info">
        <span>📈 표본평균 X̄ 의 분포</span>
        <span>누적: <span class="cnt" id="histoCnt">0</span>회</span>
      </div>
      <canvas id="histoCanvas" width="340" height="200"></canvas>
      <div class="recent">
        <div id="recentList"><span class="recent-empty">최근 X̄ 값이 여기에 나타나요</span></div>
      </div>
    </div>

    <div class="hint">
      💡 <b>관찰해 봐요!</b><br>
      • 표본을 뽑을 때마다 X̄ 값이 바뀌나요?<br>
      • 표본평균 X̄들의 분포는 어디 근처에 모이나요?<br>
      • n을 키우면 X̄의 변동은 어떻게 변하나요?
    </div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);

/* === 모집단 생성 (Box-Muller로 정규분포 근사, 30~95 점수) === */
const N_POP = 200;
let population = [];
let popPositions = [];

function gauss(mean, std){
  // Box-Muller
  let u=0, v=0;
  while(u===0) u=Math.random();
  while(v===0) v=Math.random();
  return mean + std * Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);
}

function buildPopulation(){
  population = [];
  // 정규분포 + 약간의 비대칭
  for(let i=0; i<N_POP; i++){
    let v = gauss(62, 11);
    v = Math.max(30, Math.min(98, Math.round(v)));
    population.push(v);
  }
  // 위치
  popPositions = [];
  const W = 700, H = 450;
  // 격자 위에 약간의 jitter
  const cols = 20, rows = 10;
  const cellW = W/cols, cellH = H/rows;
  for(let i=0; i<N_POP; i++){
    const r = Math.floor(i/cols), c = i%cols;
    const x = (c+0.5)*cellW + (Math.random()-0.5)*cellW*0.55;
    const y = (r+0.5)*cellH + (Math.random()-0.5)*cellH*0.55;
    popPositions.push({x, y});
  }
}

function popMean(){
  return population.reduce((a,b)=>a+b,0) / population.length;
}

/* === 색상: 점수에 따라 === */
function colorFor(v){
  // 30→파랑, 60→초록, 95→빨강
  const t = Math.max(0, Math.min(1, (v-30)/65));
  const hue = 220 - t*220;  // 220(파랑) → 0(빨강)
  return `hsl(${hue},75%,60%)`;
}

/* === 모집단 캔버스 그리기 === */
const popCanvas = $('popCanvas');
const popCtx = popCanvas.getContext('2d');

let highlightSet = new Set();
let highlightAlpha = 0;

function drawPop(){
  const W = popCanvas.width, H = popCanvas.height;
  popCtx.clearRect(0,0,W,H);

  // 어두운 배경 그라데이션
  const grad = popCtx.createRadialGradient(W/2,H/2,50,W/2,H/2,W/1.4);
  grad.addColorStop(0,'rgba(30,41,59,0.0)');
  grad.addColorStop(1,'rgba(15,23,42,0.4)');
  popCtx.fillStyle = grad;
  popCtx.fillRect(0,0,W,H);

  // 도트들
  for(let i=0; i<N_POP; i++){
    const p = popPositions[i];
    const v = population[i];
    const isH = highlightSet.has(i);
    const r = isH ? 11 : 7;
    if(isH){
      // 글로우
      popCtx.beginPath();
      popCtx.arc(p.x, p.y, r+8, 0, Math.PI*2);
      popCtx.fillStyle = `rgba(251,191,36,${0.18 * highlightAlpha})`;
      popCtx.fill();
    }
    // 본체
    popCtx.beginPath();
    popCtx.arc(p.x, p.y, r, 0, Math.PI*2);
    popCtx.fillStyle = isH ? '#fbbf24' : colorFor(v);
    popCtx.globalAlpha = isH ? 1 : (highlightSet.size>0 ? 0.32 : 0.92);
    popCtx.fill();
    popCtx.globalAlpha = 1;
    // 테두리
    popCtx.lineWidth = isH ? 2 : 1;
    popCtx.strokeStyle = isH ? '#fff' : 'rgba(15,23,42,0.6)';
    popCtx.stroke();
  }
}

/* === 히스토그램 === */
const histoCanvas = $('histoCanvas');
const histoCtx = histoCanvas.getContext('2d');
let xbarHistory = [];

function drawHisto(){
  const W = histoCanvas.width, H = histoCanvas.height;
  histoCtx.clearRect(0,0,W,H);

  // 축
  const padL = 30, padR = 12, padT = 14, padB = 28;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;

  // bins (30~95 범위, 13개 bin)
  const lo = 30, hi = 95;
  const nBins = 26;
  const binW = (hi-lo)/nBins;
  const bins = new Array(nBins).fill(0);
  xbarHistory.forEach(v=>{
    let idx = Math.floor((v-lo)/binW);
    if(idx<0) idx=0; if(idx>=nBins) idx=nBins-1;
    bins[idx]++;
  });
  const maxBin = Math.max(1, ...bins);

  // 그리드
  histoCtx.strokeStyle = 'rgba(148,163,184,0.12)';
  histoCtx.lineWidth = 1;
  for(let i=0; i<=4; i++){
    const y = padT + plotH*(i/4);
    histoCtx.beginPath();
    histoCtx.moveTo(padL, y);
    histoCtx.lineTo(W-padR, y);
    histoCtx.stroke();
  }

  // 막대
  for(let i=0; i<nBins; i++){
    const x = padL + (i/nBins)*plotW;
    const w = plotW/nBins - 1;
    const h = (bins[i]/maxBin) * plotH;
    const binCenter = lo + (i+0.5)*binW;
    histoCtx.fillStyle = colorFor(binCenter);
    histoCtx.globalAlpha = 0.7;
    histoCtx.fillRect(x, padT+plotH-h, w, h);
    histoCtx.globalAlpha = 1;
  }

  // 모평균 선 (revealed일 때만)
  if(revealed){
    const m = popMean();
    const mx = padL + ((m-lo)/(hi-lo))*plotW;
    histoCtx.strokeStyle = '#fb7185';
    histoCtx.lineWidth = 2.5;
    histoCtx.setLineDash([6,4]);
    histoCtx.beginPath();
    histoCtx.moveTo(mx, padT);
    histoCtx.lineTo(mx, padT+plotH);
    histoCtx.stroke();
    histoCtx.setLineDash([]);
    histoCtx.fillStyle = '#fb7185';
    histoCtx.font = 'bold 11px sans-serif';
    histoCtx.fillText('m='+m.toFixed(1), mx+4, padT+12);
  }

  // 최근 X̄ 표시
  if(xbarHistory.length>0){
    const v = xbarHistory[xbarHistory.length-1];
    const vx = padL + ((v-lo)/(hi-lo))*plotW;
    histoCtx.fillStyle = '#38bdf8';
    histoCtx.beginPath();
    histoCtx.moveTo(vx, padT+plotH+4);
    histoCtx.lineTo(vx-5, padT+plotH+12);
    histoCtx.lineTo(vx+5, padT+plotH+12);
    histoCtx.closePath();
    histoCtx.fill();
  }

  // x축 라벨
  histoCtx.fillStyle = '#94a3b8';
  histoCtx.font = '11px sans-serif';
  histoCtx.textAlign = 'center';
  [30,45,60,75,90].forEach(v=>{
    const x = padL + ((v-lo)/(hi-lo))*plotW;
    histoCtx.fillText(v, x, H-padB+15);
  });
  histoCtx.textAlign = 'left';
  histoCtx.fillText('X̄', 4, padT+plotH/2);
}

/* === 표본 추출 === */
let revealed = false;

function sampleOnce(n){
  const idx = [];
  const pool = Array.from({length:N_POP}, (_,i)=>i);
  for(let i=0; i<n; i++){
    const j = Math.floor(Math.random()*pool.length);
    idx.push(pool[j]);
    pool.splice(j,1);
  }
  const vals = idx.map(i=>population[i]);
  const xbar = vals.reduce((a,b)=>a+b,0)/vals.length;
  return {idx, vals, xbar};
}

function updateStats(){
  const m = popMean();
  $('popMean').textContent = m.toFixed(2);
  if(revealed){
    $('mDisplay').textContent = m.toFixed(2);
    $('mDisplay').classList.remove('locked');
    $('popInfo').classList.add('on');
  } else {
    $('mDisplay').textContent = '??.?';
    $('mDisplay').classList.add('locked');
    $('popInfo').classList.remove('on');
  }
}

function renderSample(s){
  const list = $('sbList');
  list.innerHTML = '';
  s.vals.forEach((v,i)=>{
    const c = document.createElement('span');
    c.className = 'sb-chip';
    c.style.background = colorFor(v);
    c.style.animationDelay = (i*0.025)+'s';
    c.textContent = v;
    list.appendChild(c);
  });
  $('curMean').textContent = `X̄ = ${s.xbar.toFixed(2)} (n=${s.vals.length})`;
  $('xbarDisplay').textContent = s.xbar.toFixed(2);
  if(revealed){
    const diff = (s.xbar - popMean()).toFixed(2);
    const sign = diff>=0 ? '+' : '';
    $('diffDisplay').textContent = `X̄ − m = ${sign}${diff}`;
  } else {
    $('diffDisplay').textContent = `차이: ?? (m을 공개해 보세요)`;
  }
}

function renderRecent(){
  const el = $('recentList');
  if(xbarHistory.length===0){
    el.innerHTML = '<span class="recent-empty">최근 X̄ 값이 여기에 나타나요</span>';
    return;
  }
  const last = xbarHistory.slice(-12).reverse();
  el.innerHTML = last.map(v=>`<span class="recent-item">${v.toFixed(2)}</span>`).join(' ');
}

function doSample(){
  const n = parseInt($('nRange').value);
  const s = sampleOnce(n);
  // highlight
  highlightSet = new Set(s.idx);
  highlightAlpha = 1;
  renderSample(s);
  xbarHistory.push(s.xbar);
  $('histoCnt').textContent = xbarHistory.length;
  drawPop();
  drawHisto();
  renderRecent();
  $('xbarDisplay').parentElement.classList.add('flash');
  setTimeout(()=>$('xbarDisplay').parentElement.classList.remove('flash'), 800);
}

function doBatch(times){
  const n = parseInt($('nRange').value);
  let i = 0;
  const step = ()=>{
    if(i>=times) return;
    const s = sampleOnce(n);
    xbarHistory.push(s.xbar);
    if(i===times-1){
      highlightSet = new Set(s.idx);
      highlightAlpha = 1;
      renderSample(s);
    }
    i++;
    if(i%5===0 || i===times){
      $('histoCnt').textContent = xbarHistory.length;
      drawHisto();
    }
    if(i<times) requestAnimationFrame(step);
    else { drawPop(); renderRecent(); }
  };
  step();
}

/* === Init === */
buildPopulation();
updateStats();
drawPop();
drawHisto();

$('nRange').addEventListener('input', e=>{ $('nVal').textContent = e.target.value; });
$('btnDraw').addEventListener('click', doSample);
$('btnDraw50').addEventListener('click', ()=>doBatch(50));
$('btnReveal').addEventListener('click', ()=>{
  revealed = !revealed;
  $('btnReveal').textContent = revealed ? '🙈 모평균 m 숨기기' : '🔍 모평균 m 공개';
  updateStats();
  drawHisto();
  if(xbarHistory.length>0){
    // 다시 표시 갱신
    const last = xbarHistory[xbarHistory.length-1];
    const m = popMean();
    const diff = (last - m).toFixed(2);
    const sign = diff>=0 ? '+' : '';
    $('diffDisplay').textContent = revealed
      ? `X̄ − m = ${sign}${diff}`
      : `차이: ?? (m을 공개해 보세요)`;
  }
});
$('btnReset').addEventListener('click', ()=>{
  buildPopulation();
  xbarHistory = [];
  highlightSet = new Set();
  $('histoCnt').textContent = 0;
  $('xbarDisplay').textContent = '--';
  $('diffDisplay').textContent = '차이: --';
  $('curMean').textContent = 'X̄ = --';
  $('sbList').innerHTML = '<div class="sb-empty">표본을 뽑아 보세요 →</div>';
  updateStats();
  drawPop();
  drawHisto();
  renderRecent();
});
</script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: 미세먼지 대기 오염도 지도 (실제 한국 시도 GeoJSON 사용)
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
  background:linear-gradient(135deg,#0f172a 0%,#312e81 50%,#0f172a 100%);
  color:#e2e8f0;padding:16px 12px;min-height:100vh;
}
.hdr{
  text-align:center;background:linear-gradient(135deg,rgba(244,114,182,.2),rgba(168,85,247,.15));
  border:2px solid rgba(244,114,182,.4);border-radius:18px;padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.45rem;font-weight:900;color:#f472b6;margin-bottom:4px}
.hdr p{font-size:.96rem;color:#cbd5e1;line-height:1.55}

.layout{display:grid;grid-template-columns:1fr 350px;gap:14px}
@media(max-width:900px){.layout{grid-template-columns:1fr}}

.panel{
  background:rgba(15,23,42,.7);border:1.5px solid rgba(168,85,247,.3);
  border-radius:14px;padding:14px;
}
.panel h2{
  font-size:1.05rem;font-weight:800;color:#c4b5fd;margin-bottom:10px;
  display:flex;align-items:center;gap:8px;
}

/* ===== 지도 영역 ===== */
.map-wrap{
  position:relative;width:100%;aspect-ratio:.78;
  background:radial-gradient(ellipse at 50% 40%,rgba(76,29,149,.25),rgba(15,23,42,.95));
  border:2px solid rgba(168,85,247,.3);border-radius:14px;overflow:hidden;
}
#koreaMap{display:block;width:100%;height:100%}

.map-legend{
  position:absolute;bottom:10px;right:10px;background:rgba(15,23,42,.88);
  border:1.5px solid rgba(99,102,241,.3);border-radius:10px;padding:8px 10px;
  font-size:.78rem;line-height:1.65;z-index:8;color:#cbd5e1;
}

.map-hint{
  position:absolute;top:10px;left:10px;background:rgba(15,23,42,.88);
  border:1.5px solid rgba(251,191,36,.4);border-radius:10px;padding:6px 12px;
  font-size:.85rem;font-weight:700;color:#fef3c7;z-index:8;
}
.map-hint b{color:#fbbf24}

.map-loading{
  position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:12px;
  background:rgba(15,23,42,.88);color:#cbd5e1;z-index:10;
  transition:opacity .35s ease;text-align:center;padding:20px;
}
.map-loading.gone{opacity:0;pointer-events:none}
.spinner{
  width:38px;height:38px;border:3px solid rgba(168,85,247,.25);
  border-top-color:#a855f7;border-radius:50%;animation:spin 1s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}
.map-loading .msg{font-size:.95rem;font-weight:700;color:#c4b5fd}
.map-loading .sub{font-size:.82rem;color:#94a3b8}
.map-loading.error .spinner{display:none}
.map-loading.error .msg{color:#fb7185}

/* ===== SVG 시도 ===== */
.province{
  stroke:rgba(255,255,255,0.55);
  stroke-width:0.8;
  stroke-linejoin:round;
  transition:all .25s ease;
  cursor:default;
}
.province.dimmed{opacity:.32}
.province.sampled{
  stroke:#fef3c7;
  stroke-width:2.2;
  filter:drop-shadow(0 0 8px #fbbf24);
  animation:provPulse 1.4s ease-in-out infinite;
}
@keyframes provPulse{
  0%,100%{filter:drop-shadow(0 0 6px #fbbf24)}
  50%{filter:drop-shadow(0 0 18px #fbbf24)}
}

/* 내부 라벨 (큰 도) */
.prov-label{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  pointer-events:none;
  transition:opacity .25s ease;
}
.prov-label .name{
  font-weight:800;font-size:11.5px;fill:#0f172a;
  paint-order:stroke;stroke:rgba(255,255,255,0.7);stroke-width:2.5;
  stroke-linejoin:round;text-anchor:middle;
}
.prov-label .val{
  font-weight:900;font-size:13px;fill:#0f172a;
  paint-order:stroke;stroke:rgba(255,255,255,0.85);stroke-width:2.8;
  stroke-linejoin:round;text-anchor:middle;
}
.prov-label.dim{opacity:.3}

/* 외부 콜아웃 (작은 광역시) */
.callout-line{
  stroke:rgba(203,213,225,.55);stroke-width:1;fill:none;
  transition:opacity .25s ease;
}
.callout-box{
  fill:rgba(15,23,42,.88);stroke:rgba(168,85,247,.45);stroke-width:1;
  transition:all .25s ease;
}
.callout-text{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  pointer-events:none;transition:opacity .25s ease;
}
.callout-text .name{font-weight:800;font-size:10.5px;fill:#e2e8f0;text-anchor:middle}
.callout-text .val{font-weight:900;font-size:11.5px;fill:#fbbf24;text-anchor:middle}
.callout.dim .callout-line,
.callout.dim .callout-box,
.callout.dim .callout-text{opacity:.3}
.callout.sampled .callout-box{
  fill:rgba(251,191,36,.18);stroke:#fbbf24;stroke-width:1.8;
  filter:drop-shadow(0 0 6px rgba(251,191,36,.6));
}
.callout.sampled .callout-text .name{fill:#fef3c7}

/* ===== 컨트롤 ===== */
.controls{display:flex;flex-direction:column;gap:10px;margin-bottom:12px}
.ctrl-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.ctrl-label{font-size:.92rem;font-weight:800;color:#c4b5fd;min-width:90px}
.ctrl-range{flex:1;min-width:120px;accent-color:#f472b6}
.ctrl-value{
  font-size:1rem;font-weight:900;color:#fbbf24;min-width:55px;
  background:rgba(15,23,42,.6);padding:3px 10px;border-radius:8px;text-align:center;
}

.btn{
  flex:1;min-width:130px;padding:10px 14px;border:none;border-radius:11px;
  cursor:pointer;font-size:.98rem;font-weight:900;color:#fff;transition:all .15s ease;
}
.btn:active{transform:scale(.96)}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btn-pri{background:linear-gradient(135deg,#ec4899,#be185d)}
.btn-pri:hover:not(:disabled){background:linear-gradient(135deg,#db2777,#9d174d);transform:translateY(-1px)}
.btn-sec{background:linear-gradient(135deg,#a855f7,#7c3aed)}
.btn-sec:hover:not(:disabled){background:linear-gradient(135deg,#9333ea,#6d28d9);transform:translateY(-1px)}
.btn-ghost{background:rgba(71,85,105,.6);border:1.5px solid rgba(148,163,184,.3)}
.btn-ghost:hover:not(:disabled){background:rgba(71,85,105,.9)}
.btn-row{display:flex;gap:8px;flex-wrap:wrap}

/* ===== 통계 카드 ===== */
.stats{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;
}
.stat-card{
  background:rgba(30,41,59,.7);border-radius:11px;padding:10px;text-align:center;
}
.stat-card.pop{border:1.5px solid rgba(251,113,133,.5);background:rgba(244,63,94,.1)}
.stat-card.sample{border:1.5px solid rgba(56,189,248,.5);background:rgba(14,165,233,.1)}
.sc-label{font-size:.78rem;font-weight:700;color:#94a3b8;margin-bottom:4px}
.sc-val{font-size:1.5rem;font-weight:900;letter-spacing:.3px}
.stat-card.pop .sc-val{color:#fb7185}
.stat-card.sample .sc-val{color:#38bdf8}
.sc-sub{font-size:.78rem;color:#94a3b8;margin-top:3px}

/* ===== 표본 영역 ===== */
.sample-box{
  background:rgba(34,197,94,.08);border:2px solid rgba(34,197,94,.4);
  border-radius:12px;padding:11px;margin-bottom:10px;min-height:78px;
}
.sb-title{
  font-size:.95rem;font-weight:800;color:#86efac;margin-bottom:7px;
  display:flex;justify-content:space-between;
}
.sb-mean{color:#fef3c7;font-weight:900}
.sb-chips{display:flex;flex-wrap:wrap;gap:5px}
.sb-chip{
  display:inline-flex;align-items:center;gap:4px;
  padding:4px 9px;border-radius:8px;font-size:.82rem;font-weight:800;
  background:rgba(15,23,42,.7);border:1.5px solid rgba(99,102,241,.4);
  animation:chipIn .25s cubic-bezier(.34,1.56,.64,1);
}
@keyframes chipIn{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}
.sb-chip .name{color:#e2e8f0}
.sb-chip .val{color:#fbbf24}
.sb-empty{color:#64748b;font-size:.86rem;font-style:italic}

/* ===== 히스토리 ===== */
.hist-wrap{
  background:rgba(15,23,42,.5);border:1.5px solid rgba(99,102,241,.25);
  border-radius:10px;padding:10px;
}
.hist-title{
  display:flex;justify-content:space-between;font-size:.88rem;
  font-weight:700;color:#cbd5e1;margin-bottom:8px;
}
.hist-cnt{color:#fbbf24;font-weight:900}
#xbarCanvas{
  display:block;width:100%;height:140px;
  background:rgba(15,23,42,.5);border-radius:8px;
}

.hint{
  margin-top:12px;background:rgba(244,114,182,.1);
  border:1.5px solid rgba(244,114,182,.35);border-radius:10px;
  padding:10px 12px;font-size:.88rem;color:#fbcfe8;line-height:1.6;
}
.hint b{color:#f9a8d4}

.flash-card{animation:flash .8s ease}
@keyframes flash{
  0%,100%{box-shadow:0 0 0 0 rgba(251,191,36,0)}
  30%{box-shadow:0 0 0 8px rgba(251,191,36,.4)}
}
</style>
</head>
<body>

<div class="hdr">
  <h1>🗺️ 미세먼지 지도 — 시도 표본 추출</h1>
  <p>전국 <b>17개 시도</b>를 모집단으로 두고, <b>크기 n인 표본</b>을 임의추출하여 표본평균을 구해 봐요!</p>
</div>

<div class="layout">
  <!-- 좌: 지도 -->
  <div class="panel">
    <h2>🌏 모집단 = 17개 시도</h2>
    <div class="map-wrap">
      <div class="map-hint">📌 단위: μg/m³ · <b>모평균 m = 53</b></div>
      <svg id="koreaMap" viewBox="0 0 540 700" preserveAspectRatio="xMidYMid meet"
           xmlns="http://www.w3.org/2000/svg"></svg>
      <div class="map-loading" id="loadingMsg">
        <div class="spinner"></div>
        <div class="msg">🌏 한국 지도를 불러오는 중...</div>
        <div class="sub">통계청 행정구역 데이터 (GeoJSON)</div>
      </div>
      <div class="map-legend">
        <div>🎨 색: 시도 구분</div>
        <div>🔢 숫자: μg/m³</div>
      </div>
    </div>
  </div>

  <!-- 우: 컨트롤 -->
  <div class="panel">
    <h2>🎯 표본 추출</h2>

    <div class="controls">
      <div class="ctrl-row">
        <span class="ctrl-label">표본 크기 n</span>
        <input type="range" min="1" max="16" value="3" class="ctrl-range" id="nRange">
        <span class="ctrl-value" id="nVal">3</span>
      </div>
      <div class="btn-row">
        <button class="btn btn-pri" id="btnDraw">🎯 표본 1번 뽑기</button>
        <button class="btn btn-sec" id="btnDraw20">⚡ 20번 뽑기</button>
      </div>
      <div class="btn-row">
        <button class="btn btn-ghost" id="btnReset">🔄 처음부터</button>
      </div>
    </div>

    <div class="stats">
      <div class="stat-card pop">
        <div class="sc-label">모평균 m</div>
        <div class="sc-val">53.00</div>
        <div class="sc-sub">17개 시도 평균</div>
      </div>
      <div class="stat-card sample" id="sampleCard">
        <div class="sc-label">표본평균 X̄</div>
        <div class="sc-val" id="xbarDisp">--</div>
        <div class="sc-sub" id="diffDisp">X̄ − m = --</div>
      </div>
    </div>

    <div class="sample-box">
      <div class="sb-title">
        <span>📦 이번에 뽑힌 시도</span>
        <span class="sb-mean" id="curN">n = --</span>
      </div>
      <div class="sb-chips" id="sbChips">
        <div class="sb-empty">아직 추출하지 않았어요</div>
      </div>
    </div>

    <div class="hist-wrap">
      <div class="hist-title">
        <span>📈 표본평균 X̄들의 분포</span>
        <span>누적 <span class="hist-cnt" id="histCnt">0</span>회</span>
      </div>
      <canvas id="xbarCanvas" width="320" height="140"></canvas>
    </div>

    <div class="hint">
      💡 <b>실험해 봐요!</b><br>
      • n=3일 때와 n=10일 때, X̄ 값들이 m=53 주위에 얼마나 모이나요?<br>
      • 친구와 같은 n으로 뽑아도 X̄이 서로 다른 이유는?<br>
      • X̄들의 평균은 m=53과 가까워지나요?
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script>
const $ = id => document.getElementById(id);
const SVG_NS = 'http://www.w3.org/2000/svg';

const MAP_W = 540, MAP_H = 700;

/* === 17개 시도 미세먼지 데이터 (교과서 생각열기) === */
const CITY_DATA = {
  '서울':62,'부산':29,'대구':70,'인천':47,
  '광주':61,'대전':46,'울산':52,'세종':59,
  '경기':67,'강원':30,'충북':77,'충남':53,
  '경북':74,'경남':57,'전북':65,'전남':28,'제주':24
};
const POP_MEAN = Object.values(CITY_DATA).reduce((a,b)=>a+b,0) / Object.keys(CITY_DATA).length;

/* 외부 콜아웃을 쓸 작은 광역시 */
const EXTERNAL_NAMES = new Set(['서울','부산','대구','인천','광주','대전','울산','세종']);

/* === 17개 시도의 실제 지리 중심 좌표 (경도, 위도) ===
 * GeoJSON 속성 형식이 들쭉날쭉해서 이름 매칭에 의존하면 자주 틀린다.
 * 대신 각 feature의 지리 중심을 계산해서 가장 가까운 시도로 매칭하면 100% 정확.
 */
const PROVINCE_CENTROIDS = {
  '서울': [126.99, 37.55],
  '부산': [129.07, 35.18],
  '대구': [128.60, 35.87],
  '인천': [126.55, 37.46],
  '광주': [126.85, 35.15],
  '대전': [127.38, 36.35],
  '울산': [129.31, 35.54],
  '세종': [127.29, 36.48],
  '경기': [127.20, 37.43],
  '강원': [128.30, 37.85],
  '충북': [127.70, 36.80],
  '충남': [126.80, 36.60],
  '경북': [128.85, 36.30],
  '경남': [128.25, 35.30],
  '전북': [127.15, 35.72],
  '전남': [126.90, 34.80],
  '제주': [126.55, 33.40],
};

/* === 시도별 고유 색상 (17가지) === */
const PROVINCE_COLORS = {
  '서울':'#ef4444', '부산':'#f97316', '대구':'#f59e0b', '인천':'#eab308',
  '광주':'#84cc16', '대전':'#22c55e', '울산':'#10b981', '세종':'#06b6d4',
  '경기':'#0ea5e9', '강원':'#3b82f6', '충북':'#6366f1', '충남':'#8b5cf6',
  '경북':'#a855f7', '경남':'#d946ef', '전북':'#ec4899', '전남':'#f43f5e',
  '제주':'#14b8a6',
};

function colorFor(name){
  return PROVINCE_COLORS[name] || '#64748b';
}

/* === 위치 기반 그리디 매칭: 각 feature → 가장 가까운 미배정 시도 === */
function assignProvinces(features){
  const pairs = [];
  features.forEach((feat, fi) => {
    let lon, lat;
    try {
      [lon, lat] = d3.geoCentroid(feat);
    } catch(e){ return; }
    if(!isFinite(lon) || !isFinite(lat)) return;
    for(const [name, [pLon, pLat]] of Object.entries(PROVINCE_CENTROIDS)){
      const dx = lon - pLon, dy = lat - pLat;
      pairs.push({fi, name, d: dx*dx + dy*dy});
    }
  });
  pairs.sort((a,b) => a.d - b.d);
  const fUsed = new Set(), nUsed = new Set();
  const assignment = new Map();
  for(const p of pairs){
    if(fUsed.has(p.fi) || nUsed.has(p.name)) continue;
    fUsed.add(p.fi); nUsed.add(p.name);
    assignment.set(p.fi, p.name);
  }
  return assignment;
}

/* === 지도 로드 === */
const GEO_URLS = [
  'https://cdn.jsdelivr.net/gh/southkorea/southkorea-maps@master/kostat/2013/json/skorea_provinces_geo_simple.json',
  'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_provinces_geo_simple.json',
  'https://cdn.jsdelivr.net/gh/southkorea/southkorea-maps@master/kostat/2018/json/skorea-provinces-2018-geo.json',
  'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea-provinces-2018-geo.json',
  'https://cdn.jsdelivr.net/gh/southkorea/southkorea-maps@master/kostat/2013/json/skorea_provinces_geo.json',
];

async function loadGeo(){
  let lastErr = null;
  for(const url of GEO_URLS){
    try{
      const data = await d3.json(url);
      if(data && data.features && data.features.length >= 15){
        return data;
      }
    } catch(e){
      lastErr = e;
    }
  }
  throw lastErr || new Error('지도 데이터를 가져올 수 없습니다');
}

const svgMap = $('koreaMap');
let features = [];     // {name, value, d, cx, cy, area, isExt, ext?}
let highlightIdx = new Set();
let xbarHistory = [];

/* === 외부 콜아웃 위치 계산: 지도 중심으로부터 바깥 방향으로 밀기 === */
function computeExternalLabel(cx, cy){
  const mcx = MAP_W/2, mcy = MAP_H/2;
  let dx = cx - mcx, dy = cy - mcy;
  const d = Math.hypot(dx, dy) || 1;
  dx /= d; dy /= d;
  // 작은 시도일수록 더 멀리 밀어내기
  const dist = 55;
  const lx = cx + dx * dist;
  const ly = cy + dy * dist;
  // 가장자리 boundary 안으로
  const clampX = Math.max(28, Math.min(MAP_W-28, lx));
  const clampY = Math.max(20, Math.min(MAP_H-24, ly));
  return {
    boxX: clampX, boxY: clampY,
    polyX: cx, polyY: cy
  };
}

function buildMap(geo){
  while(svgMap.firstChild) svgMap.removeChild(svgMap.firstChild);

  const projection = d3.geoMercator().fitSize([MAP_W, MAP_H], geo);
  const pathGen = d3.geoPath(projection);

  features = [];
  const assignment = assignProvinces(geo.features);
  geo.features.forEach((feat, fi) => {
    const name = assignment.get(fi);
    if(!name || !(name in CITY_DATA)) return;
    const value = CITY_DATA[name];
    const d = pathGen(feat);
    const [cx, cy] = pathGen.centroid(feat);
    const area = pathGen.area(feat);
    if(!d || isNaN(cx) || isNaN(cy)) return;
    features.push({
      name, value, d, cx, cy, area,
      isExt: EXTERNAL_NAMES.has(name),
      idx: features.length,
    });
  });

  if(features.length < 15){
    throw new Error(`시도 데이터 ${features.length}개만 매칭됨 (17개 필요)`);
  }

  // 큰 도 먼저, 광역시 나중에 (z-order)
  const sorted = [...features].sort((a,b)=> b.area - a.area);

  // 1) 폴리곤
  sorted.forEach(f => {
    const p = document.createElementNS(SVG_NS, 'path');
    p.setAttribute('d', f.d);
    p.setAttribute('fill', colorFor(f.name));
    p.setAttribute('class', 'province');
    p.dataset.idx = f.idx;
    svgMap.appendChild(p);
  });

  // 2) 라벨 (큰 도는 내부, 광역시는 외부 콜아웃)
  // 외부 라벨 — 폴리곤 위에 그려야 함
  sorted.forEach(f => {
    if(f.isExt){
      const ext = computeExternalLabel(f.cx, f.cy);
      f.ext = ext;
      // 콜아웃 선
      const g = document.createElementNS(SVG_NS, 'g');
      g.setAttribute('class', 'callout');
      g.dataset.idx = f.idx;

      const line = document.createElementNS(SVG_NS, 'line');
      line.setAttribute('x1', f.cx);
      line.setAttribute('y1', f.cy);
      line.setAttribute('x2', ext.boxX);
      line.setAttribute('y2', ext.boxY);
      line.setAttribute('class', 'callout-line');
      g.appendChild(line);

      // 박스 (이름 + 값)
      const boxW = 42, boxH = 30;
      const bx = ext.boxX - boxW/2, by = ext.boxY - boxH/2;
      const rect = document.createElementNS(SVG_NS, 'rect');
      rect.setAttribute('x', bx);
      rect.setAttribute('y', by);
      rect.setAttribute('width', boxW);
      rect.setAttribute('height', boxH);
      rect.setAttribute('rx', 6);
      rect.setAttribute('class', 'callout-box');
      g.appendChild(rect);

      const txt = document.createElementNS(SVG_NS, 'text');
      txt.setAttribute('class', 'callout-text');
      const t1 = document.createElementNS(SVG_NS, 'tspan');
      t1.setAttribute('x', ext.boxX);
      t1.setAttribute('y', ext.boxY - 2);
      t1.setAttribute('class', 'name');
      t1.textContent = f.name;
      txt.appendChild(t1);
      const t2 = document.createElementNS(SVG_NS, 'tspan');
      t2.setAttribute('x', ext.boxX);
      t2.setAttribute('y', ext.boxY + 11);
      t2.setAttribute('class', 'val');
      t2.textContent = f.value;
      txt.appendChild(t2);
      g.appendChild(txt);

      svgMap.appendChild(g);
    }
  });

  // 내부 라벨 (큰 도 + 제주)
  sorted.forEach(f => {
    if(!f.isExt){
      const g = document.createElementNS(SVG_NS, 'g');
      g.setAttribute('class', 'prov-label');
      g.dataset.idx = f.idx;

      const t1 = document.createElementNS(SVG_NS, 'text');
      t1.setAttribute('x', f.cx);
      t1.setAttribute('y', f.cy - 2);
      t1.setAttribute('class', 'name');
      t1.textContent = f.name;
      g.appendChild(t1);

      const t2 = document.createElementNS(SVG_NS, 'text');
      t2.setAttribute('x', f.cx);
      t2.setAttribute('y', f.cy + 13);
      t2.setAttribute('class', 'val');
      t2.textContent = f.value;
      g.appendChild(t2);

      svgMap.appendChild(g);
    }
  });
}

function applyHighlight(){
  const has = highlightIdx.size > 0;
  // 폴리곤
  svgMap.querySelectorAll('.province').forEach(p=>{
    const i = parseInt(p.dataset.idx);
    p.classList.remove('sampled','dimmed');
    if(!has) return;
    if(highlightIdx.has(i)) p.classList.add('sampled');
    else p.classList.add('dimmed');
  });
  // 내부 라벨
  svgMap.querySelectorAll('.prov-label').forEach(g=>{
    const i = parseInt(g.dataset.idx);
    g.classList.remove('dim');
    if(!has) return;
    if(!highlightIdx.has(i)) g.classList.add('dim');
  });
  // 외부 콜아웃
  svgMap.querySelectorAll('.callout').forEach(g=>{
    const i = parseInt(g.dataset.idx);
    g.classList.remove('sampled','dim');
    if(!has) return;
    if(highlightIdx.has(i)) g.classList.add('sampled');
    else g.classList.add('dim');
  });
}

/* === X̄ 히스토리 시각화 === */
const xbarCanvas = $('xbarCanvas');
const xbarCtx = xbarCanvas.getContext('2d');

function drawXbar(){
  const W = xbarCanvas.width, H = xbarCanvas.height;
  xbarCtx.clearRect(0,0,W,H);

  const padL = 28, padR = 12, padT = 12, padB = 26;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;
  const lo = 0, hi = 100;

  // 축 그리드
  xbarCtx.strokeStyle = 'rgba(148,163,184,0.12)';
  xbarCtx.lineWidth = 1;
  for(let i=0; i<=5; i++){
    const x = padL + plotW*(i/5);
    xbarCtx.beginPath();
    xbarCtx.moveTo(x, padT);
    xbarCtx.lineTo(x, padT+plotH);
    xbarCtx.stroke();
  }

  // m 선
  const mx = padL + ((POP_MEAN-lo)/(hi-lo))*plotW;
  xbarCtx.strokeStyle = '#fb7185';
  xbarCtx.lineWidth = 2;
  xbarCtx.setLineDash([5,3]);
  xbarCtx.beginPath();
  xbarCtx.moveTo(mx, padT);
  xbarCtx.lineTo(mx, padT+plotH);
  xbarCtx.stroke();
  xbarCtx.setLineDash([]);
  xbarCtx.fillStyle = '#fb7185';
  xbarCtx.font = 'bold 10px sans-serif';
  xbarCtx.textAlign = 'center';
  xbarCtx.fillText('m=53', mx, padT-2);

  // 점 쌓기
  const nBins = 40;
  const binW = (hi-lo)/nBins;
  const bins = new Array(nBins).fill(0);
  const dotR = 3.5;
  xbarHistory.forEach((v, idx)=>{
    let bi = Math.floor((v-lo)/binW);
    if(bi<0) bi=0; if(bi>=nBins) bi=nBins-1;
    const x = padL + (bi+0.5)*(plotW/nBins);
    const stackH = bins[bi];
    const y = padT+plotH - (stackH+0.5)*(dotR*2+1);
    if(y > padT){
      xbarCtx.beginPath();
      xbarCtx.arc(x, y, dotR, 0, Math.PI*2);
      const isLast = (idx===xbarHistory.length-1);
      xbarCtx.fillStyle = isLast ? '#fbbf24' : 'rgba(56,189,248,0.75)';
      xbarCtx.fill();
      if(isLast){
        xbarCtx.strokeStyle = '#fff';
        xbarCtx.lineWidth = 1.5;
        xbarCtx.stroke();
      }
      bins[bi]++;
    }
  });

  xbarCtx.fillStyle = '#94a3b8';
  xbarCtx.font = '10px sans-serif';
  xbarCtx.textAlign = 'center';
  [0,25,50,75,100].forEach(v=>{
    const x = padL + ((v-lo)/(hi-lo))*plotW;
    xbarCtx.fillText(v, x, H-padB+13);
  });
  xbarCtx.textAlign = 'left';
  xbarCtx.fillText('X̄', 4, padT+plotH/2);
}

/* === 표본 추출 === */
function sampleOnce(n){
  const idx = [];
  const pool = features.map((_,i)=>i);
  for(let i=0; i<n; i++){
    const j = Math.floor(Math.random()*pool.length);
    idx.push(pool[j]);
    pool.splice(j,1);
  }
  const vals = idx.map(i=>features[i].value);
  const xbar = vals.reduce((a,b)=>a+b,0)/vals.length;
  return {idx, vals, xbar};
}

function renderSample(s){
  const list = $('sbChips');
  list.innerHTML = '';
  s.idx.forEach((i, k)=>{
    const f = features[i];
    const el = document.createElement('span');
    el.className = 'sb-chip';
    el.style.animationDelay = (k*0.03)+'s';
    el.style.borderColor = colorFor(f.name);
    el.innerHTML = `<span class="name">${f.name}</span> <span class="val">${f.value}</span>`;
    list.appendChild(el);
  });
  $('curN').textContent = `n = ${s.vals.length}`;
  $('xbarDisp').textContent = s.xbar.toFixed(2);
  const diff = s.xbar - POP_MEAN;
  const sign = diff>=0 ? '+' : '';
  $('diffDisp').textContent = `X̄ − m = ${sign}${diff.toFixed(2)}`;
}

function doSample(){
  if(features.length === 0) return;
  const n = Math.min(parseInt($('nRange').value), features.length);
  const s = sampleOnce(n);
  highlightIdx = new Set(s.idx);
  renderSample(s);
  xbarHistory.push(s.xbar);
  $('histCnt').textContent = xbarHistory.length;
  applyHighlight();
  drawXbar();
  $('sampleCard').classList.add('flash-card');
  setTimeout(()=>$('sampleCard').classList.remove('flash-card'), 800);
}

function doBatch(times){
  if(features.length === 0) return;
  const n = Math.min(parseInt($('nRange').value), features.length);
  let i = 0;
  const step = ()=>{
    if(i>=times) return;
    const s = sampleOnce(n);
    xbarHistory.push(s.xbar);
    if(i===times-1){
      highlightIdx = new Set(s.idx);
      renderSample(s);
    }
    i++;
    if(i%4===0 || i===times){
      $('histCnt').textContent = xbarHistory.length;
      drawXbar();
    }
    if(i<times) requestAnimationFrame(step);
    else applyHighlight();
  };
  step();
}

/* === 이벤트 리스너 === */
drawXbar();
$('nRange').addEventListener('input', e=>{ $('nVal').textContent = e.target.value; });
$('btnDraw').addEventListener('click', doSample);
$('btnDraw20').addEventListener('click', ()=>doBatch(20));
$('btnReset').addEventListener('click', ()=>{
  highlightIdx = new Set();
  xbarHistory = [];
  $('histCnt').textContent = 0;
  $('xbarDisp').textContent = '--';
  $('diffDisp').textContent = 'X̄ − m = --';
  $('curN').textContent = 'n = --';
  $('sbChips').innerHTML = '<div class="sb-empty">아직 추출하지 않았어요</div>';
  applyHighlight();
  drawXbar();
});

/* === 지도 로드 시작 === */
loadGeo().then(geo => {
  buildMap(geo);
  $('loadingMsg').classList.add('gone');
}).catch(err => {
  console.error('Korea map load failed:', err);
  const el = $('loadingMsg');
  el.classList.add('error');
  el.innerHTML = '<div class="msg">⚠️ 한국 지도 데이터를 불러올 수 없어요</div>' +
                 '<div class="sub">네트워크 연결을 확인하고 새로고침해 주세요.<br>(' + (err.message || err) + ')</div>';
});
</script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("🎯 모평균 vs 표본평균 — 비밀 모집단 추적")
    st.caption(
        "**모평균(m)**은 모집단의 고정된 평균이지만, **표본평균(X̄)**은 표본을 어떻게 뽑는지에 따라 달라지는 **확률변수**입니다. "
        "두 시뮬레이션으로 직접 확인해 봐요!"
    )

    tab1, tab2 = st.tabs([
        "🎲 비밀 모집단 추적",
        "🗺️ 미세먼지 지도",
    ])

    with tab1:
        components.html(_HTML_TAB1, height=1150, scrolling=True)

    with tab2:
        components.html(_HTML_TAB2, height=1250, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
