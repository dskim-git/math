# activities/probability_new/mini/ci_length_factors_lab.py
"""
신뢰구간의 길이에 영향을 주는 요인 — 시각 탐험 미니활동
- 공식 L = 2 · z_{α/2} · σ/√n 을 그대로 시각화
- σ, n, 신뢰도 세 슬라이더를 직접 움직여 보며 길이 막대가 실시간으로 변하는 모습 관찰
- 옆에는 세 개의 작은 곡선(L vs n, L vs σ, L vs 신뢰도)이 함께 갱신되어
  세 요인이 길이에 미치는 영향의 형태(반비례·비례·증가)를 한눈에 비교
"""
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "📏 미니: 신뢰구간 길이를 결정하는 3가지 요인",
    "description": "L = 2·z·σ/√n 의 세 요인(σ, n, 신뢰도)을 직접 움직여 보며 "
                   "신뢰구간 길이가 어떻게 달라지는지 시각으로 탐험합니다.",
    "order": 23,
}


_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}

/* ============ 헤더 ============ */
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(168,85,247,.18));
  border:2px solid rgba(56,189,248,.5);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.6rem;font-weight:900;color:#7dd3fc;margin-bottom:5px;letter-spacing:.3px}
.hdr p{font-size:1.05rem;color:#cbd5e1;line-height:1.6}
.hdr b{color:#fde047}

/* ============ 공식 박스 ============ */
.formula{
  background:linear-gradient(135deg,rgba(56,189,248,.13),rgba(168,85,247,.13));
  border:2px solid rgba(56,189,248,.5);border-radius:14px;
  padding:16px 22px;text-align:center;margin-bottom:13px;
}
.formula .eq{
  font-size:1.85rem;color:#bfdbfe;font-weight:900;letter-spacing:.5px;
  font-family:'Cambria','Times New Roman',serif;
  line-height:1.4;
}
.formula .eq .v{color:#fde047}
.formula .eq sub{font-size:.7em}
.formula .desc{
  font-size:1rem;color:#cbd5e1;margin-top:6px;
}

/* ============ 패널 ============ */
.panel{
  background:rgba(15,23,42,.72);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px;margin-bottom:13px;
}
.panel h2{
  font-size:1.18rem;font-weight:900;color:#a5b4fc;margin-bottom:10px;
  display:flex;align-items:center;gap:8px;letter-spacing:.3px;
}
.panel h2 .badge{
  font-size:.85rem;color:#cbd5e1;background:rgba(99,102,241,.2);
  padding:3px 9px;border-radius:999px;font-weight:700;
}

/* ============ 컨트롤 ============ */
.ctl-grid{display:grid;grid-template-columns:1fr;gap:9px}
.ctl-row{
  display:flex;align-items:center;gap:11px;flex-wrap:wrap;
  background:rgba(56,189,248,.07);border:1.5px solid rgba(56,189,248,.32);
  border-radius:11px;padding:11px 13px;
}
.ctl-row.sigma{background:rgba(244,114,182,.07);border-color:rgba(244,114,182,.4)}
.ctl-row.sigma .ctl-lab{color:#f9a8d4}
.ctl-row.n     {background:rgba(34,197,94,.08);border-color:rgba(34,197,94,.38)}
.ctl-row.n     .ctl-lab{color:#86efac}
.ctl-row.conf  {background:rgba(168,85,247,.09);border-color:rgba(168,85,247,.4)}
.ctl-row.conf  .ctl-lab{color:#c4b5fd}
.ctl-lab{font-size:1.1rem;font-weight:800;min-width:185px;display:flex;align-items:center;gap:7px}
.ctl-lab .icon{font-size:1.4rem}
.ctl-range{flex:1;min-width:180px;height:7px}
.ctl-row.sigma .ctl-range{accent-color:#ec4899}
.ctl-row.n     .ctl-range{accent-color:#22c55e}
.ctl-row.conf  .ctl-range{accent-color:#a855f7}
.ctl-val{
  font-size:1.55rem;font-weight:900;color:#fde047;min-width:90px;
  background:rgba(15,23,42,.7);padding:3px 14px;border-radius:9px;text-align:center;
}

/* ============ 길이 막대 (큰 시각) ============ */
.lenbar-wrap{
  background:rgba(15,23,42,.5);border:1.5px solid rgba(56,189,248,.3);
  border-radius:11px;padding:18px 18px;margin-bottom:13px;
}
.lenbar-head{
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;
  font-size:1rem;color:#cbd5e1;font-weight:700;margin-bottom:10px;
}
.lenbar-head .L{color:#fde047;font-size:1.3rem;font-weight:900}
#lenbar{display:block;width:100%;height:140px;background:rgba(15,23,42,.5);border-radius:8px}

/* ============ 카드 ============ */
.card-grid{
  display:grid;grid-template-columns:repeat(4,1fr);gap:9px;
}
@media(max-width:780px){.card-grid{grid-template-columns:repeat(2,1fr)}}
.card{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.3);
  border-radius:11px;padding:10px;text-align:center;
}
.card .lab{font-size:.95rem;color:#a5b4fc;font-weight:800;margin-bottom:3px;letter-spacing:.3px}
.card .val{font-size:1.5rem;color:#fef3c7;font-weight:900}
.card.high .val{color:#fda4af}
.card.low  .val{color:#86efac}

/* ============ 3개의 작은 차트 ============ */
.chart-grid{
  display:grid;grid-template-columns:repeat(3,1fr);gap:11px;
}
@media(max-width:860px){.chart-grid{grid-template-columns:1fr}}
.chart-card{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(56,189,248,.3);
  border-radius:11px;padding:11px;
}
.chart-card h3{
  font-size:1rem;color:#7dd3fc;font-weight:800;margin-bottom:6px;
  text-align:center;letter-spacing:.3px;
}
.chart-card.pink {border-color:rgba(244,114,182,.45)}
.chart-card.pink h3 {color:#f9a8d4}
.chart-card.green{border-color:rgba(34,197,94,.45)}
.chart-card.green h3{color:#86efac}
.chart-card.purp {border-color:rgba(168,85,247,.45)}
.chart-card.purp h3 {color:#c4b5fd}
.chart-canvas{display:block;width:100%;height:170px;background:rgba(15,23,42,.5);border-radius:8px}

/* ============ 인사이트 ============ */
.insight{
  background:rgba(251,191,36,.1);border:2px solid rgba(251,191,36,.45);
  border-radius:13px;padding:13px 16px;margin-top:12px;
  font-size:1.02rem;color:#fef3c7;line-height:1.7;
  display:flex;align-items:flex-start;gap:10px;
}
.insight .ico{font-size:1.6rem;flex-shrink:0;line-height:1.2}
.insight b{color:#fde047}
.insight .pink {color:#f9a8d4;font-weight:900}
.insight .green{color:#86efac;font-weight:900}
.insight .purp {color:#c4b5fd;font-weight:900}
</style>
</head>
<body>

<div class="hdr">
  <h1>📏 신뢰구간의 길이 = ?</h1>
  <p>모평균 신뢰구간의 길이가 <b>σ, n, 신뢰도</b> 세 가지에 어떻게 영향을 받는지 직접 조작해 봐요!</p>
</div>

<!-- 공식 -->
<div class="formula">
  <div class="eq">L &nbsp;=&nbsp; 2 · z<sub>α/2</sub> · <span class="v">σ</span> / √<span class="v">n</span></div>
  <div class="desc">신뢰도가 높아질수록 <b>z<sub>α/2</sub></b>가, σ가 커질수록 <b>분자</b>가, n이 커질수록 <b>분모</b>가 커집니다.</div>
</div>

<!-- 컨트롤 -->
<div class="panel">
  <h2>🎛 세 슬라이더를 자유롭게 움직여 보세요 <span class="badge">실시간 반영</span></h2>
  <div class="ctl-grid">
    <div class="ctl-row sigma">
      <span class="ctl-lab"><span class="icon">📐</span>모표준편차 σ</span>
      <input type="range" min="0.5" max="30" step="0.1" value="10" class="ctl-range" id="sigRange">
      <span class="ctl-val" id="sigVal">10.0</span>
    </div>
    <div class="ctl-row n">
      <span class="ctl-lab"><span class="icon">🧮</span>표본 크기 n</span>
      <input type="range" min="2" max="500" step="1" value="30" class="ctl-range" id="nRange">
      <span class="ctl-val" id="nVal">30</span>
    </div>
    <div class="ctl-row conf">
      <span class="ctl-lab"><span class="icon">🎯</span>신뢰도 (%)</span>
      <input type="range" min="50" max="99.9" step="0.1" value="95" class="ctl-range" id="cfRange">
      <span class="ctl-val" id="cfVal">95.0%</span>
    </div>
  </div>
</div>

<!-- 길이 막대 -->
<div class="panel">
  <h2>📊 지금 설정에서의 신뢰구간 길이 <span class="badge">길이 L 을 막대로 시각화</span></h2>
  <div class="lenbar-wrap">
    <div class="lenbar-head">
      <span>표본평균을 중심으로 좌우 대칭 신뢰구간</span>
      <span class="L">L = <span id="LVal">--</span></span>
    </div>
    <canvas id="lenbar" width="980" height="140"></canvas>
  </div>

  <div class="card-grid">
    <div class="card">
      <div class="lab">z<sub>α/2</sub></div>
      <div class="val" id="zVal">--</div>
    </div>
    <div class="card">
      <div class="lab">표준오차 σ/√n</div>
      <div class="val" id="seVal">--</div>
    </div>
    <div class="card">
      <div class="lab">반길이 L/2</div>
      <div class="val" id="halfVal">--</div>
    </div>
    <div class="card">
      <div class="lab">전체 길이 L</div>
      <div class="val" id="LVal2">--</div>
    </div>
  </div>
</div>

<!-- 3개 차트 -->
<div class="panel">
  <h2>📈 각 요인을 바꿀 때 길이는 어떤 모양으로 변할까?
       <span class="badge">노란 점 = 현재 설정 위치</span></h2>
  <div class="chart-grid">
    <div class="chart-card green">
      <h3>L vs n  (반비례, ∝ 1/√n)</h3>
      <canvas id="chartN" class="chart-canvas" width="600" height="170"></canvas>
    </div>
    <div class="chart-card pink">
      <h3>L vs σ  (정비례, ∝ σ)</h3>
      <canvas id="chartSig" class="chart-canvas" width="600" height="170"></canvas>
    </div>
    <div class="chart-card purp">
      <h3>L vs 신뢰도  (증가, ∝ z<sub>α/2</sub>)</h3>
      <canvas id="chartConf" class="chart-canvas" width="600" height="170"></canvas>
    </div>
  </div>

  <div class="insight">
    <span class="ico">💡</span>
    <span>
      <span class="green">n이 커지면</span> 길이가 <b>1/√n</b> 만큼 줄어들어요 → 표본을 많이 모을수록 정확해집니다.<br>
      <span class="pink">σ가 커지면</span> 길이가 σ에 <b>정비례</b>해서 늘어나요 → 자료가 흩어져 있을수록 추정이 어려워요.<br>
      <span class="purp">신뢰도를 높이면</span> <b>z<sub>α/2</sub></b> 가 커져서 길이가 늘어나요 →
      99.9%로 갈수록 가팔라집니다.
    </span>
  </div>
</div>

<script>
/* =============== 표준정규 분위수 =============== */
function normPpf(p){
  if(p<=0) return -Infinity; if(p>=1) return Infinity;
  const a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,
           1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00];
  const b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,
            6.680131188771972e+01,-1.328068155288572e+01];
  const c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,
           -2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00];
  const d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,
           3.754408661907416e+00];
  const plow=0.02425, phigh=1-plow;
  if(p<plow){const q=Math.sqrt(-2*Math.log(p));
    return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);}
  if(p>phigh){const q=Math.sqrt(-2*Math.log(1-p));
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);}
  const q=p-0.5, r=q*q;
  return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q /
         (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);
}
function zHalf(confPct){
  const a = 1 - confPct/100;
  return normPpf(1 - a/2);
}
function lengthOf(sig, n, confPct){
  return 2 * zHalf(confPct) * sig / Math.sqrt(n);
}

const $ = id => document.getElementById(id);
function fmt(v,d=3){ if(!isFinite(v)) return '--'; return Number(v.toFixed(d)).toString(); }

/* =============== 상태 =============== */
let sig=10, n=30, conf=95;

/* =============== 큰 길이 막대 =============== */
function drawLenBar(){
  const cv = $('lenbar');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=40, padR=40, padT=30, padB=44;
  const plotW=W-padL-padR;

  // 최대 가능 길이 (n=2, σ=30, conf=99.9%) 정도를 기준 (시각화 안정성)
  const Lmax = lengthOf(30, 2, 99.9);
  const L    = lengthOf(sig, n, conf);
  const ratio = L / Lmax;

  // 가운데를 0(표본평균), 좌우 대칭으로 ±L/2
  const cx = padL + plotW/2;
  const halfPx = ratio * plotW/2;

  // 축
  ctx.strokeStyle='rgba(148,163,184,.5)';
  ctx.lineWidth=1.5;
  ctx.beginPath();
  ctx.moveTo(padL, H-padB+8); ctx.lineTo(W-padR, H-padB+8);
  ctx.stroke();

  // 표본평균 점선
  ctx.strokeStyle='rgba(251,191,36,.6)';
  ctx.setLineDash([5,4]);
  ctx.beginPath();
  ctx.moveTo(cx, padT-4); ctx.lineTo(cx, H-padB+12);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#fde047';
  ctx.font='bold 14px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText('표본평균 X̄', cx, padT-6);

  // 막대 (그라데이션)
  const grad = ctx.createLinearGradient(cx-halfPx, 0, cx+halfPx, 0);
  grad.addColorStop(0, '#22d3ee');
  grad.addColorStop(0.5, '#38bdf8');
  grad.addColorStop(1, '#22d3ee');
  ctx.fillStyle = grad;
  ctx.beginPath();
  const yMid = padT + 35;
  const barH = 36;
  ctx.fillRect(cx-halfPx, yMid, halfPx*2, barH);
  ctx.strokeStyle='#0ea5e9'; ctx.lineWidth=2;
  ctx.strokeRect(cx-halfPx, yMid, halfPx*2, barH);

  // 끝점 막대
  ctx.strokeStyle='#f43f5e'; ctx.lineWidth=3;
  ctx.beginPath();
  ctx.moveTo(cx-halfPx, yMid-8); ctx.lineTo(cx-halfPx, yMid+barH+8);
  ctx.moveTo(cx+halfPx, yMid-8); ctx.lineTo(cx+halfPx, yMid+barH+8);
  ctx.stroke();

  // 길이 화살표
  ctx.strokeStyle='#fda4af'; ctx.lineWidth=2;
  const yArrow = yMid + barH + 18;
  ctx.beginPath();
  ctx.moveTo(cx-halfPx, yArrow); ctx.lineTo(cx+halfPx, yArrow);
  // 화살촉
  ctx.moveTo(cx-halfPx, yArrow); ctx.lineTo(cx-halfPx+8, yArrow-5);
  ctx.moveTo(cx-halfPx, yArrow); ctx.lineTo(cx-halfPx+8, yArrow+5);
  ctx.moveTo(cx+halfPx, yArrow); ctx.lineTo(cx+halfPx-8, yArrow-5);
  ctx.moveTo(cx+halfPx, yArrow); ctx.lineTo(cx+halfPx-8, yArrow+5);
  ctx.stroke();

  // L 라벨
  ctx.fillStyle='#fde047';
  ctx.font='bold 16px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  ctx.fillText('L = '+fmt(L,3), cx, yArrow+5);

  // 좌/우 라벨
  ctx.fillStyle='#fca5a5';
  ctx.font='bold 12px sans-serif';
  ctx.textAlign='right'; ctx.textBaseline='middle';
  ctx.fillText('X̄ − L/2', cx-halfPx-6, yMid+barH/2);
  ctx.textAlign='left';
  ctx.fillText('X̄ + L/2', cx+halfPx+6, yMid+barH/2);
}

/* =============== 3개 작은 차트 =============== */
function drawSubChart(cvId, xVals, yVals, curX, color, xFmt, yFmt){
  const cv = $(cvId);
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=44, padR=14, padT=10, padB=28;
  const plotW=W-padL-padR, plotH=H-padT-padB;
  const xMin = xVals[0], xMax = xVals[xVals.length-1];
  const yMin = 0, yMax = Math.max(...yVals)*1.1;
  const X = x => padL + ((x-xMin)/(xMax-xMin))*plotW;
  const Y = y => padT+plotH - ((y-yMin)/(yMax-yMin))*plotH;

  // 격자
  ctx.strokeStyle='rgba(148,163,184,.13)';
  ctx.setLineDash([3,3]);
  for(let i=1;i<=4;i++){
    const y = padT + (i/4)*plotH;
    ctx.beginPath();
    ctx.moveTo(padL, y); ctx.lineTo(W-padR, y);
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // 곡선
  ctx.strokeStyle = color;
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  for(let i=0;i<xVals.length;i++){
    if(i===0) ctx.moveTo(X(xVals[i]), Y(yVals[i]));
    else ctx.lineTo(X(xVals[i]), Y(yVals[i]));
  }
  ctx.stroke();

  // 현재 점
  let yCur=0;
  // 가까운 점 보간
  for(let i=1;i<xVals.length;i++){
    if(xVals[i-1] <= curX && curX <= xVals[i]){
      const t = (curX-xVals[i-1])/(xVals[i]-xVals[i-1] || 1);
      yCur = yVals[i-1] + t*(yVals[i]-yVals[i-1]);
      break;
    }
  }
  ctx.fillStyle='#fde047';
  ctx.beginPath();
  ctx.arc(X(curX), Y(yCur), 6, 0, Math.PI*2);
  ctx.fill();
  ctx.strokeStyle='#fde047'; ctx.setLineDash([3,3]); ctx.lineWidth=1.4;
  ctx.beginPath();
  ctx.moveTo(X(curX), padT); ctx.lineTo(X(curX), padT+plotH);
  ctx.stroke();
  ctx.setLineDash([]);

  // 축
  ctx.strokeStyle='rgba(148,163,184,.5)';
  ctx.beginPath();
  ctx.moveTo(padL, padT+plotH); ctx.lineTo(W-padR, padT+plotH);
  ctx.moveTo(padL, padT); ctx.lineTo(padL, padT+plotH);
  ctx.stroke();

  // x눈금
  ctx.fillStyle='#94a3b8';
  ctx.font='11px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  const ticks=4;
  for(let i=0;i<=ticks;i++){
    const v = xMin + (xMax-xMin)*i/ticks;
    ctx.fillText(xFmt(v), X(v), padT+plotH+4);
  }
  // y눈금
  ctx.textAlign='right'; ctx.textBaseline='middle';
  for(let i=0;i<=4;i++){
    const v = yMin + (yMax-yMin)*i/4;
    ctx.fillText(yFmt(v), padL-4, padT+plotH - (i/4)*plotH);
  }
}

function drawAll(){
  // 텍스트 업데이트
  $('sigVal').textContent = fmt(sig,1);
  $('nVal').textContent = n;
  $('cfVal').textContent = fmt(conf,1)+'%';
  const z  = zHalf(conf);
  const se = sig/Math.sqrt(n);
  const L  = 2*z*se;
  $('zVal').textContent = fmt(z,3);
  $('seVal').textContent = fmt(se,3);
  $('halfVal').textContent = fmt(L/2,3);
  $('LVal').textContent = fmt(L,3);
  $('LVal2').textContent = fmt(L,3);

  drawLenBar();

  // L vs n (n=2..500)
  const nGrid=[], LN=[];
  for(let nn=2; nn<=500; nn+=2){ nGrid.push(nn); LN.push(lengthOf(sig, nn, conf)); }
  drawSubChart('chartN', nGrid, LN, n, '#22c55e',
    v=>Math.round(v)+'', v=>v.toFixed(1));

  // L vs σ (σ=0.5..30)
  const sigGrid=[], LS=[];
  for(let s=0.5; s<=30; s+=0.5){ sigGrid.push(s); LS.push(lengthOf(s, n, conf)); }
  drawSubChart('chartSig', sigGrid, LS, sig, '#ec4899',
    v=>v.toFixed(0), v=>v.toFixed(1));

  // L vs 신뢰도 (50..99.5)
  const cGrid=[], LC=[];
  for(let c=50; c<=99.5; c+=0.5){ cGrid.push(c); LC.push(lengthOf(sig, n, c)); }
  drawSubChart('chartConf', cGrid, LC, conf, '#a855f7',
    v=>v.toFixed(0)+'%', v=>v.toFixed(1));
}

$('sigRange').addEventListener('input', e=>{ sig = parseFloat(e.target.value); drawAll(); });
$('nRange').addEventListener('input',   e=>{ n   = parseInt(e.target.value);   drawAll(); });
$('cfRange').addEventListener('input',  e=>{ conf= parseFloat(e.target.value); drawAll(); });
window.addEventListener('resize', drawAll);
drawAll();
</script>
</body>
</html>
"""


def render():
    st.subheader("📏 신뢰구간의 길이를 결정하는 3가지 요인")
    st.caption(
        "L = 2·z·σ/√n 의 세 요인(σ, n, 신뢰도)을 직접 움직여 보며 "
        "신뢰구간 길이가 어떤 모양으로 변하는지 시각으로 탐험합니다."
    )
    components.html(_HTML, height=1500, scrolling=True)
