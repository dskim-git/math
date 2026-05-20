# activities/probability_new/mini/sample_variance_n1_lab.py
"""
표본분산을 n-1로 나누는 이유 — 시각적 탐구 미니활동
- TAB1: 표본평균(X̄) 기준 vs 모평균(m) 기준 — 퍼짐(편차제곱합) 비교
- TAB2: 1/n 추정량 vs 1/(n-1) 추정량 경주 — 어느 쪽이 σ²에 수렴하는가?
- TAB3: (n-1)의 비밀 — 시각적 분해 [표본⇄m] = [표본⇄X̄] + [X̄⇄m]
"""
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "✨ 미니: 표본분산을 n-1로 나누는 이유 (베셀 보정)",
    "description": "X̄ 기준의 퍼짐은 m 기준의 퍼짐보다 항상 작다 — 그래서 (n-1)로 나누어 보정한다는 사실을 시각적으로 발견합니다.",
    "order": 6,
}


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: 거리 비교 — X̄ 기준과 m 기준의 편차제곱합 비교
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
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(168,85,247,.15));
  border:2px solid rgba(56,189,248,.4);border-radius:18px;
  padding:12px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.35rem;font-weight:900;color:#38bdf8;margin-bottom:4px}
.hdr p{font-size:.92rem;color:#cbd5e1;line-height:1.55}
.hdr b{color:#fbbf24}

.panel{
  background:rgba(15,23,42,.7);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px;margin-bottom:12px;
}
.panel h2{
  font-size:1.02rem;font-weight:800;color:#a5b4fc;margin-bottom:10px;
  display:flex;align-items:center;gap:8px;
}

/* ===== X-bar 표기 ===== */
.xb{
  display:inline-block;
  text-decoration:overline;
  text-decoration-thickness:1.5px;
  padding:0 1px;
  line-height:1;
}

/* ===== 수직선 ===== */
.numline-wrap{
  position:relative;width:100%;height:320px;
  background:radial-gradient(ellipse at center,rgba(30,41,59,.85),rgba(15,23,42,.95));
  border:2px solid rgba(99,102,241,.35);border-radius:14px;overflow:hidden;
}
#nlCanvas{display:block;width:100%;height:100%}

.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.btn{
  flex:1;min-width:110px;padding:9px 12px;border:none;border-radius:10px;
  font-size:.95rem;font-weight:900;color:#fff;cursor:pointer;
  transition:all .15s ease;letter-spacing:.3px;
}
.btn:active{transform:scale(.96)}
.btn-pri{background:linear-gradient(135deg,#3b82f6,#1d4ed8);box-shadow:0 3px 10px rgba(59,130,246,.4)}
.btn-pri:hover{background:linear-gradient(135deg,#2563eb,#1e40af);transform:translateY(-1px)}
.btn-sec{background:linear-gradient(135deg,#a855f7,#7c3aed);box-shadow:0 3px 10px rgba(168,85,247,.4)}
.btn-sec:hover{background:linear-gradient(135deg,#9333ea,#6d28d9);transform:translateY(-1px)}
.btn-ghost{background:rgba(71,85,105,.6);border:1.5px solid rgba(148,163,184,.3)}
.btn-ghost:hover{background:rgba(71,85,105,.9)}

.ctrl-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:8px}
.ctrl-label{font-size:.9rem;font-weight:800;color:#a5b4fc;min-width:90px}
.ctrl-range{flex:1;min-width:120px;accent-color:#fbbf24}
.ctrl-value{
  font-size:.98rem;font-weight:900;color:#fbbf24;min-width:42px;
  background:rgba(15,23,42,.6);padding:3px 9px;border-radius:8px;text-align:center;
}

/* ===== 비교 박스 ===== */
.compare{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px;
}
@media(max-width:520px){.compare{grid-template-columns:1fr}}
.cmp-card{
  background:rgba(30,41,59,.7);border-radius:12px;padding:12px;
  border:1.5px solid transparent;text-align:center;position:relative;
}
.cmp-card.m{border-color:rgba(251,113,133,.5);background:rgba(244,63,94,.10)}
.cmp-card.x{border-color:rgba(56,189,248,.5);background:rgba(14,165,233,.10)}
.cmp-card h3{
  font-size:.92rem;font-weight:800;margin-bottom:4px;letter-spacing:.3px;
}
.cmp-card.m h3{color:#fb7185}
.cmp-card.x h3{color:#38bdf8}
.cmp-val{font-size:1.65rem;font-weight:900;letter-spacing:.4px}
.cmp-card.m .cmp-val{color:#fb7185}
.cmp-card.x .cmp-val{color:#38bdf8}
.cmp-sub{font-size:.78rem;color:#94a3b8;margin-top:3px}
.cmp-card .crown{
  position:absolute;top:-12px;right:-8px;font-size:1.4rem;
  filter:drop-shadow(0 2px 4px rgba(251,191,36,.6));
  animation:pop .35s ease;
  display:none;
}
.cmp-card.winner .crown{display:block}
@keyframes pop{from{transform:scale(0) rotate(-10deg)}to{transform:scale(1) rotate(0)}}

.bar-track{
  height:18px;background:rgba(15,23,42,.7);border-radius:8px;
  overflow:hidden;margin-top:8px;position:relative;
  border:1px solid rgba(148,163,184,.15);
}
.bar-fill{
  height:100%;border-radius:8px;transition:width .35s cubic-bezier(.4,1.6,.7,.95);
}
.bar-m{background:linear-gradient(90deg,#f43f5e,#fb7185)}
.bar-x{background:linear-gradient(90deg,#0ea5e9,#38bdf8)}

.formula{
  background:rgba(15,23,42,.55);border:1px dashed rgba(99,102,241,.4);
  border-radius:8px;padding:6px 10px;font-size:.85rem;color:#cbd5e1;
  font-family:'Cambria Math','Consolas',monospace;margin-top:6px;
}
.formula b{color:#fbbf24}

.insight{
  background:rgba(168,85,247,.12);border:1.5px solid rgba(168,85,247,.4);
  border-radius:12px;padding:11px 14px;margin-top:12px;
  font-size:.93rem;color:#e9d5ff;line-height:1.65;
  display:flex;align-items:flex-start;gap:8px;
}
.insight .ico{font-size:1.3rem;flex-shrink:0}
.insight b{color:#fde047}
.insight.hidden{display:none}

.minimum-banner{
  text-align:center;padding:8px 12px;border-radius:10px;
  background:rgba(56,189,248,.12);border:1.5px solid rgba(56,189,248,.4);
  color:#7dd3fc;font-size:.92rem;font-weight:800;margin-top:8px;
  display:none;
}
.minimum-banner.on{display:block;animation:slideDown .35s ease}
@keyframes slideDown{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>

<div class="hdr">
  <h1>🔍 <span class="xb">X</span> 기준 vs m 기준 — 어느 쪽 퍼짐이 더 클까?</h1>
  <p>표본을 뽑은 뒤, <b>모평균 m</b>까지의 거리와 <b>표본평균 <span class="xb">X</span></b>까지의 거리, 어느 쪽 제곱합이 더 클지 관찰해 봐요.</p>
</div>

<div class="panel">
  <h2>📏 수직선 위에서 표본 관찰하기</h2>
  <div class="numline-wrap">
    <canvas id="nlCanvas" width="900" height="320"></canvas>
  </div>

  <div class="ctrl-row">
    <span class="ctrl-label">표본 크기 n</span>
    <input type="range" min="3" max="20" value="6" class="ctrl-range" id="nRange">
    <span class="ctrl-value" id="nVal">6</span>
  </div>

  <div class="btn-row">
    <button class="btn btn-pri" id="btnDraw">🎲 표본 새로 뽑기</button>
    <button class="btn btn-sec" id="btnAnim">📐 거리 측정 애니메이션</button>
    <button class="btn btn-ghost" id="btnMinTest">🧪 c값 직접 움직이기</button>
  </div>
</div>

<div class="panel">
  <h2>⚖️ 두 기준의 편차제곱합 비교</h2>

  <div class="compare">
    <div class="cmp-card m" id="cardM">
      <div class="crown">👑</div>
      <h3>모평균 m 기준</h3>
      <div class="cmp-val" id="sumM">--</div>
      <div class="cmp-sub">Σ(Xᵢ − m)²</div>
      <div class="bar-track"><div class="bar-fill bar-m" id="barM" style="width:0%"></div></div>
      <div class="formula">m = <b id="mVal">--</b></div>
    </div>
    <div class="cmp-card x" id="cardX">
      <div class="crown">👑</div>
      <h3 id="cardXTitle">표본평균 <span class="xb">X</span> 기준</h3>
      <div class="cmp-val" id="sumX">--</div>
      <div class="cmp-sub" id="cardXSub">Σ(Xᵢ − <span class="xb">X</span>)²</div>
      <div class="bar-track"><div class="bar-fill bar-x" id="barX" style="width:0%"></div></div>
      <div class="formula" id="cardXFormula"><span class="xb">X</span> = <b id="xVal">--</b></div>
    </div>
  </div>

  <div class="minimum-banner" id="minBanner">
    💡 <b><span class="xb">X</span></b>은 Σ(Xᵢ − c)² 를 <b>최소</b>로 만드는 c 값입니다! → 그래서 어떤 표본이라도 <span class="xb">X</span> 기준 퍼짐이 m 기준보다 항상 작거나 같습니다.
  </div>

  <div class="insight" id="insightBox">
    <span class="ico">✨</span>
    <div>
      <b>관찰해 봐요:</b><br>
      • 표본을 여러 번 새로 뽑아도 거의 항상 <b><span class="xb">X</span> 기준 퍼짐이 더 작다</b>는 사실!<br>
      • 그래서 <span class="xb">X</span> 기준으로 잰 퍼짐을 <b>n으로 나누면 σ²보다 작게</b> 나오는 거예요. → 이게 바로 편향(bias)!
    </div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);

// ===== 모집단 (1차원, 30명의 점수, 평균≈70, σ≈11) =====
// 미리 고정해서 m이 매번 같도록 함
const POP = [52,54,56,57,59,60,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,80,81,83,85,87,90,93];
const POP_MEAN = POP.reduce((a,b)=>a+b,0) / POP.length;  // = 70.7
const PMIN = 45, PMAX = 100;  // 수직선 범위

let sample = [];
let sampleXbar = 0;
let sumFromM = 0;
let sumFromXbar = 0;

// 애니메이션 상태
let animMode = null;          // null | 'm' | 'x' | 'minTest'
let animStart = 0;
let animDur = 900;

// minTest 상태
let testMode = false;
let testC = POP_MEAN;

const nl = $('nlCanvas');
const ctx = nl.getContext('2d');

function W(){return nl.width}
function H(){return nl.height}
function x2px(v){
  const padL=50, padR=30;
  return padL + (v-PMIN)/(PMAX-PMIN) * (W()-padL-padR);
}

// 캔버스에서 X̄(라벨) 그리기 — X 위에 직접 윗줄을 그어준다
function drawXbarText(ctx2, suffix, cx, y, color, fontStr){
  ctx2.font = fontStr;
  const xW = ctx2.measureText('X').width;
  const sufW = ctx2.measureText(suffix).width;
  const totalW = xW + sufW;
  const left = cx - totalW/2;
  ctx2.fillStyle = color;
  ctx2.textAlign = 'left';
  ctx2.fillText('X', left, y);
  if(suffix) ctx2.fillText(suffix, left + xW, y);
  const fs = parseInt(fontStr) || 13;
  ctx2.strokeStyle = color;
  ctx2.lineWidth = Math.max(1.2, fs/10);
  ctx2.beginPath();
  ctx2.moveTo(left + 0.5, y - fs * 0.88);
  ctx2.lineTo(left + xW - 0.5, y - fs * 0.88);
  ctx2.stroke();
  ctx2.textAlign = 'center';
}

function drawNumberLine(){
  const w=W(), h=H();
  ctx.clearRect(0,0,w,h);

  // 배경 그라데이션
  const g = ctx.createLinearGradient(0,0,0,h);
  g.addColorStop(0,'rgba(30,41,59,0)');
  g.addColorStop(1,'rgba(15,23,42,0.5)');
  ctx.fillStyle=g; ctx.fillRect(0,0,w,h);

  const baseY = h - 60;

  // 축
  ctx.strokeStyle = 'rgba(203,213,225,0.55)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(x2px(PMIN), baseY);
  ctx.lineTo(x2px(PMAX), baseY);
  ctx.stroke();

  // 눈금
  ctx.fillStyle='#94a3b8';
  ctx.font='11px sans-serif';
  ctx.textAlign='center';
  for(let v=50; v<=100; v+=10){
    const px = x2px(v);
    ctx.strokeStyle='rgba(148,163,184,0.45)';
    ctx.beginPath(); ctx.moveTo(px,baseY-4); ctx.lineTo(px,baseY+4); ctx.stroke();
    ctx.fillText(v, px, baseY+18);
  }

  // 모집단 점들 (배경, 흐릿하게)
  POP.forEach(v=>{
    const px = x2px(v);
    ctx.beginPath();
    ctx.arc(px, baseY-8, 3, 0, Math.PI*2);
    ctx.fillStyle='rgba(148,163,184,0.35)';
    ctx.fill();
  });

  // 모평균 m 선
  const mX = x2px(POP_MEAN);
  ctx.strokeStyle = '#fb7185';
  ctx.lineWidth = 2.5;
  ctx.setLineDash([6,4]);
  ctx.beginPath(); ctx.moveTo(mX, 22); ctx.lineTo(mX, baseY); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#fb7185';
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='center';
  ctx.fillText('m='+POP_MEAN.toFixed(1), mX, 14);

  if(sample.length === 0){
    ctx.fillStyle='#64748b';
    ctx.font='13px sans-serif';
    ctx.textAlign='center';
    ctx.fillText('🎲 위에서 "표본 새로 뽑기"를 눌러보세요', w/2, h/2);
    return;
  }

  // 표본평균 X̄ 선 (테스트 모드일 때는 c 선으로 대체)
  const lineV = testMode ? testC : sampleXbar;
  const xX = x2px(lineV);
  const xColor = testMode ? '#a855f7' : '#38bdf8';
  ctx.strokeStyle = xColor;
  ctx.lineWidth = 2.5;
  ctx.setLineDash([6,4]);
  ctx.beginPath(); ctx.moveTo(xX, 38); ctx.lineTo(xX, baseY); ctx.stroke();
  ctx.setLineDash([]);
  if(testMode){
    ctx.fillStyle = xColor;
    ctx.font='bold 13px sans-serif';
    ctx.textAlign='center';
    ctx.fillText('c='+testC.toFixed(1), xX, 30);
  } else {
    drawXbarText(ctx, '='+sampleXbar.toFixed(1), xX, 30, xColor, 'bold 13px sans-serif');
  }

  // 애니메이션 진행도
  const now = performance.now();
  const t = animMode ? Math.min(1, (now-animStart)/animDur) : 0;

  // 거리 선 그리기
  sample.forEach((v, i)=>{
    const px = x2px(v);
    const baseColor = '#fbbf24';

    if(animMode === 'm'){
      // m 기준 거리 선 (빨강)
      ctx.strokeStyle = `rgba(251,113,133,${0.55+0.35*t})`;
      ctx.lineWidth = 1.8;
      ctx.setLineDash([3,3]);
      ctx.beginPath();
      ctx.moveTo(px, baseY-8);
      ctx.lineTo(mX, baseY-8);
      ctx.stroke();
      ctx.setLineDash([]);
      // 사각형 표시 (제곱 = 정사각형)
      if(t>0.4){
        const side = Math.abs(px - mX) * (0.25 + 0.55*t);
        const cx = (px+mX)/2 - side/2;
        const cy = baseY - 8 - side - 4;
        ctx.fillStyle = `rgba(251,113,133,${0.18*t})`;
        ctx.strokeStyle = `rgba(251,113,133,${0.7*t})`;
        ctx.lineWidth = 1.2;
        ctx.fillRect(cx, cy, side, side);
        ctx.strokeRect(cx, cy, side, side);
      }
    }
    if(animMode === 'x'){
      ctx.strokeStyle = `rgba(56,189,248,${0.55+0.35*t})`;
      ctx.lineWidth = 1.8;
      ctx.setLineDash([3,3]);
      ctx.beginPath();
      ctx.moveTo(px, baseY-8);
      ctx.lineTo(xX, baseY-8);
      ctx.stroke();
      ctx.setLineDash([]);
      if(t>0.4){
        const side = Math.abs(px - xX) * (0.25 + 0.55*t);
        const cx = (px+xX)/2 - side/2;
        const cy = baseY - 8 - side - 4;
        ctx.fillStyle = `rgba(56,189,248,${0.18*t})`;
        ctx.strokeStyle = `rgba(56,189,248,${0.7*t})`;
        ctx.lineWidth = 1.2;
        ctx.fillRect(cx, cy, side, side);
        ctx.strokeRect(cx, cy, side, side);
      }
    }
    if(testMode){
      // c 기준 거리 선 (보라)
      ctx.strokeStyle = 'rgba(168,85,247,.5)';
      ctx.lineWidth = 1.6;
      ctx.setLineDash([3,3]);
      ctx.beginPath();
      ctx.moveTo(px, baseY-8);
      ctx.lineTo(xX, baseY-8);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // 표본 점
    ctx.beginPath();
    ctx.arc(px, baseY-8, 7, 0, Math.PI*2);
    ctx.fillStyle = baseColor;
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // 값 라벨
    ctx.fillStyle = '#fef3c7';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign='center';
    ctx.fillText(v, px, baseY-22);
  });

  // 라벨
  ctx.fillStyle='#cbd5e1';
  ctx.font='12px sans-serif';
  ctx.textAlign='left';
  ctx.fillText('모집단 30명 (희미한 점) · 표본 (노란 점)', 12, h-8);

  if(animMode){
    if(t<1) requestAnimationFrame(drawNumberLine);
    else animMode = null;
  }
}

function restoreXbarCardUI(){
  $('cardXTitle').innerHTML = '표본평균 <span class="xb">X</span> 기준';
  $('cardXSub').innerHTML  = 'Σ(Xᵢ − <span class="xb">X</span>)²';
  $('cardXFormula').innerHTML = '<span class="xb">X</span> = <b id="xVal">--</b>';
  $('minBanner').classList.remove('on');
}

function drawSample(){
  testMode = false;
  $('btnMinTest').textContent = '🧪 c값 직접 움직이기';
  restoreXbarCardUI();
  const n = parseInt($('nRange').value);
  const pool = POP.slice();
  sample = [];
  for(let i=0; i<n; i++){
    const j = Math.floor(Math.random()*pool.length);
    sample.push(pool[j]);
    pool.splice(j,1);
  }
  sampleXbar = sample.reduce((a,b)=>a+b,0)/n;
  sumFromM = sample.reduce((s,v)=>s+(v-POP_MEAN)*(v-POP_MEAN), 0);
  sumFromXbar = sample.reduce((s,v)=>s+(v-sampleXbar)*(v-sampleXbar), 0);
  updateStats();
  drawNumberLine();
}

function updateStats(){
  $('mVal').textContent = POP_MEAN.toFixed(2);
  $('xVal').textContent = sampleXbar.toFixed(2);
  $('sumM').textContent = sumFromM.toFixed(2);
  $('sumX').textContent = sumFromXbar.toFixed(2);
  const maxV = Math.max(sumFromM, sumFromXbar, 0.001);
  $('barM').style.width = ((sumFromM/maxV)*100) + '%';
  $('barX').style.width = ((sumFromXbar/maxV)*100) + '%';

  // crown — 더 작은 쪽이 "이김" (퍼짐을 더 잘 압축)
  $('cardM').classList.toggle('winner', sumFromM < sumFromXbar && sample.length>0);
  $('cardX').classList.toggle('winner', sumFromXbar <= sumFromM && sample.length>0);
}

function computeSumForC(c){
  return sample.reduce((s,v)=>s+(v-c)*(v-c), 0);
}

$('nRange').addEventListener('input', e=>{ $('nVal').textContent = e.target.value; });
$('btnDraw').addEventListener('click', drawSample);
$('btnAnim').addEventListener('click', ()=>{
  if(sample.length===0) drawSample();
  // 두 번 연달아 보여주기: m 기준 → X̄ 기준
  animMode = 'm';
  animStart = performance.now();
  drawNumberLine();
  setTimeout(()=>{
    animMode = 'x';
    animStart = performance.now();
    drawNumberLine();
  }, animDur + 200);
});

$('btnMinTest').addEventListener('click', ()=>{
  if(sample.length===0) drawSample();
  testMode = !testMode;
  $('btnMinTest').textContent = testMode ? '✋ c값 움직이기 끄기' : '🧪 c값 직접 움직이기';
  $('minBanner').classList.toggle('on', testMode);
  if(testMode){
    // 우측 카드를 c-기준 표시로 전환
    testC = sampleXbar;
    updateTestStats();
  } else {
    // 우측 카드를 표본평균 X̄ 기준 표시로 복원
    restoreXbarCardUI();
    updateStats();
  }
  drawNumberLine();
});

// 드래그로 c 조절 (testMode일 때)
function getMouseX(ev){
  const rect = nl.getBoundingClientRect();
  const px = (ev.touches ? ev.touches[0].clientX : ev.clientX) - rect.left;
  const ratio = nl.width / rect.width;
  return px * ratio;
}
function px2x(px){
  const padL=50, padR=30;
  return PMIN + (px-padL)/(W()-padL-padR) * (PMAX-PMIN);
}

let dragging = false;
function startDrag(ev){
  if(!testMode) return;
  dragging = true;
  testC = Math.max(PMIN+2, Math.min(PMAX-2, px2x(getMouseX(ev))));
  updateTestStats();
  drawNumberLine();
  ev.preventDefault();
}
function moveDrag(ev){
  if(!dragging) return;
  testC = Math.max(PMIN+2, Math.min(PMAX-2, px2x(getMouseX(ev))));
  updateTestStats();
  drawNumberLine();
  ev.preventDefault();
}
function endDrag(){ dragging=false; }
nl.addEventListener('mousedown', startDrag);
window.addEventListener('mousemove', moveDrag);
window.addEventListener('mouseup', endDrag);
nl.addEventListener('touchstart', startDrag, {passive:false});
window.addEventListener('touchmove', moveDrag, {passive:false});
window.addEventListener('touchend', endDrag);

function updateTestStats(){
  const sumC = computeSumForC(testC);
  $('sumX').textContent = sumC.toFixed(2);
  $('cardXTitle').textContent = 'c 기준 (직접 조절)';
  $('cardXSub').textContent  = 'Σ(Xᵢ − c)²';
  $('cardXFormula').innerHTML = 'c = <b>'+testC.toFixed(2)+'</b>';
  const maxV = Math.max(sumFromM, sumC, 0.001);
  $('barM').style.width = ((sumFromM/maxV)*100) + '%';
  $('barX').style.width = ((sumC/maxV)*100) + '%';
  $('cardM').classList.toggle('winner', sumFromM < sumC);
  $('cardX').classList.toggle('winner', sumC <= sumFromM);
}

// Init
drawSample();
</script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: 추정량 경주 — 1/n vs 1/(n-1)
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
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0f172a 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(244,114,182,.18),rgba(168,85,247,.15));
  border:2px solid rgba(244,114,182,.4);border-radius:18px;
  padding:12px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.35rem;font-weight:900;color:#f472b6;margin-bottom:4px}
.hdr p{font-size:.92rem;color:#cbd5e1;line-height:1.55}
.hdr b{color:#fbbf24}

/* ===== X-bar 표기 ===== */
.xb{
  display:inline-block;
  text-decoration:overline;
  text-decoration-thickness:1.5px;
  padding:0 1px;
  line-height:1;
}

.panel{
  background:rgba(15,23,42,.7);border:1.5px solid rgba(168,85,247,.3);
  border-radius:14px;padding:14px;margin-bottom:12px;
}
.panel h2{
  font-size:1.02rem;font-weight:800;color:#c4b5fd;margin-bottom:10px;
  display:flex;align-items:center;gap:8px;
}

.controls{display:flex;flex-direction:column;gap:10px;margin-bottom:12px}
.ctrl-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.ctrl-label{font-size:.92rem;font-weight:800;color:#c4b5fd;min-width:88px}
.ctrl-range{flex:1;min-width:140px;accent-color:#f472b6}
.ctrl-value{
  font-size:1rem;font-weight:900;color:#fbbf24;min-width:55px;
  background:rgba(15,23,42,.6);padding:3px 10px;border-radius:8px;text-align:center;
}

.btn{
  flex:1;min-width:130px;padding:10px 14px;border:none;border-radius:11px;
  font-size:.95rem;font-weight:900;color:#fff;cursor:pointer;
  transition:all .15s ease;
}
.btn:active{transform:scale(.96)}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btn-pri{background:linear-gradient(135deg,#ec4899,#be185d)}
.btn-pri:hover:not(:disabled){background:linear-gradient(135deg,#db2777,#9d174d);transform:translateY(-1px)}
.btn-sec{background:linear-gradient(135deg,#a855f7,#7c3aed)}
.btn-sec:hover:not(:disabled){background:linear-gradient(135deg,#9333ea,#6d28d9);transform:translateY(-1px)}
.btn-ghost{background:rgba(71,85,105,.6);border:1.5px solid rgba(148,163,184,.3)}
.btn-ghost:hover{background:rgba(71,85,105,.9)}
.btn-row{display:flex;gap:8px;flex-wrap:wrap}

/* ===== 두 추정량 카드 ===== */
.racers{
  display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;
}
@media(max-width:560px){.racers{grid-template-columns:1fr}}
.racer{
  background:rgba(30,41,59,.7);border-radius:14px;padding:14px;text-align:center;
  border:2px solid transparent;position:relative;transition:all .25s ease;
}
.racer.biased{border-color:rgba(251,113,133,.5);background:rgba(244,63,94,.10)}
.racer.unbiased{border-color:rgba(34,197,94,.5);background:rgba(34,197,94,.10)}
.racer h3{
  font-size:1rem;font-weight:900;margin-bottom:4px;letter-spacing:.3px;
}
.racer.biased h3{color:#fb7185}
.racer.unbiased h3{color:#86efac}
.racer .formula{
  font-size:.78rem;color:#94a3b8;font-family:'Cambria Math','Consolas',monospace;
  margin-bottom:6px;
}
.racer .big{font-size:1.7rem;font-weight:900;letter-spacing:.4px}
.racer.biased .big{color:#fb7185}
.racer.unbiased .big{color:#86efac}
.racer .sub{font-size:.78rem;color:#94a3b8;margin-top:3px}
.racer .verdict{
  margin-top:8px;font-size:.85rem;font-weight:800;
  padding:5px 10px;border-radius:8px;display:inline-block;
}
.racer.biased .verdict{
  background:rgba(251,113,133,.18);color:#fda4af;border:1px solid rgba(251,113,133,.4);
}
.racer.unbiased .verdict{
  background:rgba(34,197,94,.18);color:#86efac;border:1px solid rgba(34,197,94,.4);
}
.racer .flash{
  position:absolute;top:8px;right:8px;font-size:1rem;
  opacity:0;transition:opacity .2s ease;
}
.racer.flash-on .flash{opacity:1;animation:starSpin .6s ease}
@keyframes starSpin{
  0%{transform:scale(0) rotate(0)}
  50%{transform:scale(1.3) rotate(180deg)}
  100%{transform:scale(1) rotate(360deg)}
}

/* 모분산 진실 표시 */
.truth{
  background:rgba(251,191,36,.12);border:1.5px solid rgba(251,191,36,.45);
  border-radius:11px;padding:10px 12px;margin-bottom:12px;
  text-align:center;font-size:.95rem;
}
.truth .label{color:#cbd5e1;font-weight:700;letter-spacing:.3px;font-size:.85rem}
.truth .val{color:#fbbf24;font-weight:900;font-size:1.6rem;letter-spacing:.4px}
.truth .sub{color:#94a3b8;font-size:.78rem;margin-top:2px}

/* 차트 */
.chart-wrap{
  background:rgba(15,23,42,.5);border:1.5px solid rgba(99,102,241,.25);
  border-radius:12px;padding:10px;
}
.chart-title{
  display:flex;justify-content:space-between;align-items:center;
  font-size:.92rem;font-weight:800;color:#cbd5e1;margin-bottom:8px;
}
.chart-title .cnt{color:#fbbf24;font-weight:900}
#convCanvas{display:block;width:100%;height:220px;background:rgba(15,23,42,.4);border-radius:8px}
#histCanvas{display:block;width:100%;height:220px;background:rgba(15,23,42,.4);border-radius:8px;margin-top:12px}
.legend{
  display:flex;gap:18px;justify-content:center;flex-wrap:wrap;
  font-size:.85rem;color:#cbd5e1;margin-top:8px;
}
.lg-dot{display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:middle;margin-right:5px}
.lg-dot.bias{background:#fb7185}
.lg-dot.unb{background:#22c55e}
.lg-dot.sig{background:#fbbf24}

.hint{
  margin-top:12px;background:rgba(168,85,247,.12);
  border:1.5px solid rgba(168,85,247,.4);border-radius:10px;
  padding:10px 12px;font-size:.88rem;color:#e9d5ff;line-height:1.6;
}
.hint b{color:#fde047}
</style>
</head>
<body>

<div class="hdr">
  <h1>🏁 1/n 추정량 vs 1/(n-1) 추정량 — 경주!</h1>
  <p>같은 표본에서 두 가지 분산 추정량을 동시에 계산합니다. 어느 쪽이 진짜 <b>모분산 σ²</b>에 수렴할까요?</p>
</div>

<div class="truth">
  <div class="label">진짜 모분산 σ² (정답)</div>
  <div class="val" id="sigmaTrue">--</div>
  <div class="sub">모집단 30명에서 계산한 고정값</div>
</div>

<div class="panel">
  <h2>🎮 시뮬레이션 컨트롤</h2>
  <div class="controls">
    <div class="ctrl-row">
      <span class="ctrl-label">표본 크기 n</span>
      <input type="range" min="2" max="20" value="5" class="ctrl-range" id="nRange">
      <span class="ctrl-value" id="nVal">5</span>
    </div>
    <div class="btn-row">
      <button class="btn btn-pri" id="btnOne">🎲 1회</button>
      <button class="btn btn-sec" id="btnRun">⚡ 100회</button>
      <button class="btn btn-sec" id="btnBig">🚀 1000회</button>
      <button class="btn btn-ghost" id="btnReset">🔄 리셋</button>
    </div>
  </div>

  <div class="racers">
    <div class="racer biased" id="cardBias">
      <div class="flash">⭐</div>
      <h3>① 1/n 으로 나눔</h3>
      <div class="formula">S² = (1/n) Σ (Xᵢ − <span class="xb">X</span>)²</div>
      <div class="big" id="biasVal">--</div>
      <div class="sub">현재 표본의 추정값</div>
      <div class="verdict" id="biasMean">평균 = --</div>
    </div>
    <div class="racer unbiased" id="cardUnb">
      <div class="flash">⭐</div>
      <h3>② 1/(n-1) 로 나눔 ✨</h3>
      <div class="formula">S² = (1/(n−1)) Σ (Xᵢ − <span class="xb">X</span>)²</div>
      <div class="big" id="unbVal">--</div>
      <div class="sub">현재 표본의 추정값</div>
      <div class="verdict" id="unbMean">평균 = --</div>
    </div>
  </div>
</div>

<div class="panel">
  <h2>📈 추정량의 평균이 σ²에 수렴하는 모습</h2>
  <div class="chart-wrap">
    <div class="chart-title">
      <span>누적 평균(E[S²]의 추정)</span>
      <span>총 <span class="cnt" id="trialCnt">0</span>회 시행</span>
    </div>
    <canvas id="convCanvas" width="700" height="220"></canvas>
    <div class="legend">
      <span><span class="lg-dot bias"></span>1/n 추정량 평균</span>
      <span><span class="lg-dot unb"></span>1/(n−1) 추정량 평균</span>
      <span><span class="lg-dot sig"></span>진짜 σ²</span>
    </div>
  </div>

  <div class="chart-wrap" style="margin-top:12px">
    <div class="chart-title">
      <span>추정값들의 분포 (히스토그램)</span>
    </div>
    <canvas id="histCanvas" width="700" height="220"></canvas>
  </div>

  <div class="hint">
    💡 <b>관찰 포인트!</b><br>
    • <span style="color:#fda4af;font-weight:900">빨간색(1/n)</span> 곡선은 σ²보다 <b>아래</b>에 자리잡아요 → <b>과소추정</b>!<br>
    • <span style="color:#86efac;font-weight:900">초록색(1/(n-1))</span> 곡선은 σ²에 <b>딱 맞춰서</b> 수렴해요 → <b>불편추정량</b>!<br>
    • n이 작을수록 두 곡선의 차이가 더 크게 보입니다.
  </div>
</div>

<script>
const $ = id => document.getElementById(id);

const POP = [52,54,56,57,59,60,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,80,81,83,85,87,90,93];
const POP_MEAN = POP.reduce((a,b)=>a+b,0) / POP.length;
const POP_VAR  = POP.reduce((s,v)=>s+(v-POP_MEAN)*(v-POP_MEAN),0) / POP.length;  // 모분산 σ²

let sumBias = 0, sumUnb = 0;
let trials = 0;
let biasHistory = [];     // 각 시행의 1/n 추정값
let unbHistory  = [];     // 각 시행의 1/(n-1) 추정값
let runBiasMean = [];     // 누적 평균
let runUnbMean = [];

$('sigmaTrue').textContent = POP_VAR.toFixed(3);

function sampleOnce(n){
  const pool = POP.slice();
  const s = [];
  for(let i=0; i<n; i++){
    const j = Math.floor(Math.random()*pool.length);
    s.push(pool[j]);
    pool.splice(j,1);
  }
  const xb = s.reduce((a,b)=>a+b,0)/n;
  const ssq = s.reduce((a,v)=>a+(v-xb)*(v-xb), 0);
  return { bias: ssq/n, unb: n>1 ? ssq/(n-1) : 0 };
}

function runOnce(){
  const n = parseInt($('nRange').value);
  const r = sampleOnce(n);
  biasHistory.push(r.bias);
  unbHistory.push(r.unb);
  sumBias += r.bias;
  sumUnb  += r.unb;
  trials++;
  runBiasMean.push(sumBias/trials);
  runUnbMean.push(sumUnb/trials);
  $('biasVal').textContent = r.bias.toFixed(3);
  $('unbVal').textContent  = r.unb.toFixed(3);
  $('biasMean').textContent = `평균 = ${(sumBias/trials).toFixed(3)}`;
  $('unbMean').textContent  = `평균 = ${(sumUnb/trials).toFixed(3)}`;
  $('trialCnt').textContent = trials;
  // flash
  $('cardBias').classList.add('flash-on');
  $('cardUnb').classList.add('flash-on');
  setTimeout(()=>{$('cardBias').classList.remove('flash-on'); $('cardUnb').classList.remove('flash-on');}, 350);
}

function runMany(times){
  let i = 0;
  const step = ()=>{
    const batch = Math.min(50, times-i);
    for(let k=0; k<batch; k++){
      const n = parseInt($('nRange').value);
      const r = sampleOnce(n);
      biasHistory.push(r.bias);
      unbHistory.push(r.unb);
      sumBias += r.bias;
      sumUnb  += r.unb;
      trials++;
      runBiasMean.push(sumBias/trials);
      runUnbMean.push(sumUnb/trials);
    }
    i += batch;
    $('biasVal').textContent = biasHistory[biasHistory.length-1].toFixed(3);
    $('unbVal').textContent  = unbHistory[unbHistory.length-1].toFixed(3);
    $('biasMean').textContent = `평균 = ${(sumBias/trials).toFixed(3)}`;
    $('unbMean').textContent  = `평균 = ${(sumUnb/trials).toFixed(3)}`;
    $('trialCnt').textContent = trials;
    drawConv();
    drawHist();
    if(i<times) requestAnimationFrame(step);
  };
  step();
}

function reset(){
  sumBias = 0; sumUnb = 0; trials = 0;
  biasHistory = []; unbHistory = [];
  runBiasMean = []; runUnbMean = [];
  $('biasVal').textContent = '--';
  $('unbVal').textContent = '--';
  $('biasMean').textContent = '평균 = --';
  $('unbMean').textContent = '평균 = --';
  $('trialCnt').textContent = 0;
  drawConv();
  drawHist();
}

const convCanvas = $('convCanvas');
const convCtx = convCanvas.getContext('2d');
const histCanvas = $('histCanvas');
const histCtx = histCanvas.getContext('2d');

function drawConv(){
  const W = convCanvas.width, H = convCanvas.height;
  convCtx.clearRect(0,0,W,H);
  const padL = 42, padR = 14, padT = 14, padB = 30;
  const pw = W-padL-padR, ph = H-padT-padB;

  // y 범위 — σ² 중심 ± 적당히
  const sig = POP_VAR;
  const allVals = [sig, ...runBiasMean.slice(-200), ...runUnbMean.slice(-200)];
  const mn = Math.min(...allVals, sig*0.5);
  const mx = Math.max(...allVals, sig*1.5);
  const ymn = mn - (mx-mn)*0.15;
  const ymx = mx + (mx-mn)*0.15;

  // grid
  convCtx.strokeStyle = 'rgba(148,163,184,0.13)';
  convCtx.lineWidth = 1;
  for(let i=0; i<=4; i++){
    const y = padT + ph*(i/4);
    convCtx.beginPath(); convCtx.moveTo(padL, y); convCtx.lineTo(W-padR, y); convCtx.stroke();
    // y label
    const v = ymx - (ymx-ymn)*(i/4);
    convCtx.fillStyle = '#64748b';
    convCtx.font = '10px sans-serif';
    convCtx.textAlign = 'right';
    convCtx.fillText(v.toFixed(1), padL-4, y+3);
  }

  // σ² 선
  const sy = padT + (1-(sig-ymn)/(ymx-ymn))*ph;
  convCtx.strokeStyle = '#fbbf24';
  convCtx.lineWidth = 2;
  convCtx.setLineDash([6,4]);
  convCtx.beginPath(); convCtx.moveTo(padL, sy); convCtx.lineTo(W-padR, sy); convCtx.stroke();
  convCtx.setLineDash([]);
  convCtx.fillStyle = '#fbbf24';
  convCtx.font = 'bold 11px sans-serif';
  convCtx.textAlign = 'left';
  convCtx.fillText(`σ²=${sig.toFixed(2)}`, W-padR-58, sy-4);

  if(trials > 0){
    // 두 곡선 그리기
    const drawLine = (arr, color)=>{
      convCtx.strokeStyle = color;
      convCtx.lineWidth = 2.2;
      convCtx.beginPath();
      const n = arr.length;
      arr.forEach((v,i)=>{
        const x = padL + (i/(Math.max(n-1,1)))*pw;
        const y = padT + (1-(v-ymn)/(ymx-ymn))*ph;
        if(i===0) convCtx.moveTo(x,y); else convCtx.lineTo(x,y);
      });
      convCtx.stroke();
    };
    drawLine(runBiasMean, '#fb7185');
    drawLine(runUnbMean, '#22c55e');
  } else {
    convCtx.fillStyle = '#64748b';
    convCtx.font = '13px sans-serif';
    convCtx.textAlign = 'center';
    convCtx.fillText('🎲 위에서 시뮬레이션을 실행하세요', W/2, H/2);
  }

  // x label
  convCtx.fillStyle = '#94a3b8';
  convCtx.font = '11px sans-serif';
  convCtx.textAlign = 'center';
  convCtx.fillText('시행 횟수', W/2, H-8);
}

function drawHist(){
  const W = histCanvas.width, H = histCanvas.height;
  histCtx.clearRect(0,0,W,H);
  const padL = 42, padR = 14, padT = 14, padB = 28;
  const pw = W-padL-padR, ph = H-padT-padB;

  if(biasHistory.length === 0){
    histCtx.fillStyle = '#64748b';
    histCtx.font = '13px sans-serif';
    histCtx.textAlign = 'center';
    histCtx.fillText('🎲 시행을 추가하면 두 추정량의 분포가 보입니다', W/2, H/2);
    return;
  }

  const sig = POP_VAR;
  const all = biasHistory.concat(unbHistory);
  const lo = Math.min(0, ...all);
  const hi = Math.max(sig*2.2, ...all);
  const nBins = 40;
  const binW = (hi-lo)/nBins;
  const binsB = new Array(nBins).fill(0);
  const binsU = new Array(nBins).fill(0);
  biasHistory.forEach(v=>{
    let bi = Math.floor((v-lo)/binW);
    if(bi<0) bi=0; if(bi>=nBins) bi=nBins-1;
    binsB[bi]++;
  });
  unbHistory.forEach(v=>{
    let bi = Math.floor((v-lo)/binW);
    if(bi<0) bi=0; if(bi>=nBins) bi=nBins-1;
    binsU[bi]++;
  });
  const maxB = Math.max(1, ...binsB, ...binsU);

  // grid
  histCtx.strokeStyle = 'rgba(148,163,184,0.13)';
  histCtx.lineWidth = 1;
  for(let i=0; i<=4; i++){
    const y = padT + ph*(i/4);
    histCtx.beginPath(); histCtx.moveTo(padL, y); histCtx.lineTo(W-padR, y); histCtx.stroke();
  }

  // bars (overlap)
  const bw = pw/nBins - 1;
  for(let i=0; i<nBins; i++){
    const x = padL + (i/nBins)*pw;
    // bias bar
    const hB = (binsB[i]/maxB)*ph;
    histCtx.fillStyle = 'rgba(251,113,133,0.55)';
    histCtx.fillRect(x, padT+ph-hB, bw, hB);
    // unbiased bar
    const hU = (binsU[i]/maxB)*ph;
    histCtx.fillStyle = 'rgba(34,197,94,0.55)';
    histCtx.fillRect(x, padT+ph-hU, bw, hU);
  }

  // σ² 선
  const sigX = padL + ((sig-lo)/(hi-lo))*pw;
  histCtx.strokeStyle = '#fbbf24';
  histCtx.lineWidth = 2.5;
  histCtx.setLineDash([6,4]);
  histCtx.beginPath(); histCtx.moveTo(sigX, padT); histCtx.lineTo(sigX, padT+ph); histCtx.stroke();
  histCtx.setLineDash([]);
  histCtx.fillStyle = '#fbbf24';
  histCtx.font = 'bold 11px sans-serif';
  histCtx.textAlign = 'center';
  histCtx.fillText(`σ²=${sig.toFixed(2)}`, sigX, padT-2);

  // 평균 마커
  const meanB = sumBias/trials;
  const meanU = sumUnb/trials;
  const drawArrow = (v, color, label)=>{
    const x = padL + ((v-lo)/(hi-lo))*pw;
    histCtx.fillStyle = color;
    histCtx.beginPath();
    histCtx.moveTo(x, padT+ph+2);
    histCtx.lineTo(x-6, padT+ph+12);
    histCtx.lineTo(x+6, padT+ph+12);
    histCtx.closePath();
    histCtx.fill();
    histCtx.fillStyle = color;
    histCtx.font = 'bold 10px sans-serif';
    histCtx.textAlign = 'center';
    histCtx.fillText(label, x, padT+ph+24);
  };
  drawArrow(meanB, '#fb7185', '평균');
  drawArrow(meanU, '#22c55e', '평균');

  // y label
  histCtx.fillStyle = '#94a3b8';
  histCtx.font = '11px sans-serif';
  histCtx.textAlign = 'left';
  histCtx.fillText('빈도', 6, padT+ph/2);
  histCtx.textAlign='center';
  histCtx.fillText('추정값', W/2, H-4);
}

$('nRange').addEventListener('input', e=>{ $('nVal').textContent = e.target.value; reset(); });
$('btnOne').addEventListener('click', ()=>{ runOnce(); drawConv(); drawHist(); });
$('btnRun').addEventListener('click', ()=>runMany(100));
$('btnBig').addEventListener('click', ()=>runMany(1000));
$('btnReset').addEventListener('click', reset);

drawConv();
drawHist();
</script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: (n-1)의 비밀 — 시각적 분해
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
  background:linear-gradient(135deg,#0f172a 0%,#312e81 50%,#0f172a 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(251,191,36,.18),rgba(249,115,22,.12));
  border:2px solid rgba(251,191,36,.45);border-radius:18px;
  padding:12px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.35rem;font-weight:900;color:#fbbf24;margin-bottom:4px}
.hdr p{font-size:.92rem;color:#cbd5e1;line-height:1.55}
.hdr b{color:#fde047}

/* ===== X-bar 표기 ===== */
.xb{
  display:inline-block;
  text-decoration:overline;
  text-decoration-thickness:1.5px;
  padding:0 1px;
  line-height:1;
}

.panel{
  background:rgba(15,23,42,.75);border:1.5px solid rgba(251,191,36,.3);
  border-radius:14px;padding:14px;margin-bottom:12px;
}

/* ===== 단계 표시 ===== */
.steps{
  display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;
}
.step-chip{
  padding:6px 12px;border-radius:18px;font-size:.85rem;font-weight:800;
  background:rgba(71,85,105,.45);color:#94a3b8;border:1.5px solid rgba(148,163,184,.2);
  cursor:pointer;transition:all .2s ease;
}
.step-chip.active{
  background:linear-gradient(135deg,#fbbf24,#f97316);color:#1f2937;
  border-color:#fbbf24;box-shadow:0 3px 10px rgba(251,191,36,.4);
  transform:scale(1.05);
}
.step-chip.done{background:rgba(34,197,94,.18);color:#86efac;border-color:rgba(34,197,94,.45)}

/* 단계 내용 */
.step-body{
  background:rgba(15,23,42,.6);border:1.5px solid rgba(99,102,241,.25);
  border-radius:12px;padding:14px;min-height:340px;
}
.step-title{
  font-size:1.08rem;font-weight:900;color:#fde047;margin-bottom:10px;
  display:flex;align-items:center;gap:8px;
}
.step-text{font-size:.95rem;color:#e2e8f0;line-height:1.7;margin-bottom:10px}
.step-text b{color:#fbbf24}
.eqn{
  background:rgba(0,0,0,.45);border:1px solid rgba(251,191,36,.3);
  border-radius:9px;padding:10px 12px;margin:10px 0;
  font-family:'Cambria Math','Times New Roman',serif;font-size:1.05rem;
  text-align:center;color:#fef3c7;letter-spacing:.3px;
  animation:fadeIn .4s ease;
}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.highlight-red{color:#fb7185;font-weight:900}
.highlight-green{color:#86efac;font-weight:900}
.highlight-blue{color:#7dd3fc;font-weight:900}
.highlight-yellow{color:#fde047;font-weight:900}

/* 도식 */
.diagram{
  background:radial-gradient(ellipse at center,rgba(30,41,59,.85),rgba(15,23,42,.95));
  border:1.5px solid rgba(99,102,241,.3);border-radius:12px;
  padding:8px;margin:10px 0;
}
#decompCanvas{display:block;width:100%;height:310px}

/* 네비 */
.nav-row{
  display:flex;gap:8px;justify-content:space-between;margin-top:12px;
}
.btn{
  flex:1;padding:11px 14px;border:none;border-radius:11px;
  font-size:.98rem;font-weight:900;color:#fff;cursor:pointer;
  transition:all .15s ease;
}
.btn:active{transform:scale(.96)}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-prev{background:rgba(71,85,105,.7);border:1.5px solid rgba(148,163,184,.25)}
.btn-prev:hover:not(:disabled){background:rgba(71,85,105,.95)}
.btn-next{background:linear-gradient(135deg,#fbbf24,#f97316);color:#1f2937}
.btn-next:hover:not(:disabled){background:linear-gradient(135deg,#f59e0b,#ea580c);transform:translateY(-1px)}

/* 최종 카드 */
.final-card{
  background:linear-gradient(135deg,rgba(34,197,94,.22),rgba(251,191,36,.12));
  border:2px solid rgba(34,197,94,.55);border-radius:14px;
  padding:14px;text-align:center;
}
.final-card .big{
  font-family:'Cambria Math',serif;font-size:1.3rem;font-weight:900;
  color:#86efac;margin:8px 0;letter-spacing:.4px;
}
.final-card .tag{
  display:inline-block;padding:5px 14px;border-radius:18px;
  background:#22c55e;color:#fff;font-size:.85rem;font-weight:900;
  letter-spacing:.5px;margin-top:6px;
}
</style>
</head>
<body>

<div class="hdr">
  <h1>✨ (n-1)의 비밀 — 왜 정확히 n-1일까?</h1>
  <p>한 단계씩 따라가며, <b>왜 (n-1)로 나누어야 σ²가 정확히 나오는지</b> 시각적으로 알아봐요.</p>
</div>

<div class="panel">
  <div class="steps">
    <div class="step-chip active" data-step="0">① 두 가지 퍼짐</div>
    <div class="step-chip" data-step="1">② 피타고라스 같은 분해</div>
    <div class="step-chip" data-step="2">③ 기댓값으로 정리</div>
    <div class="step-chip" data-step="3">④ V(<span class="xb">X</span>) = σ²/n 대입</div>
    <div class="step-chip" data-step="4">⑤ 비밀 공개!</div>
  </div>

  <div class="step-body" id="stepBody"></div>

  <div class="nav-row">
    <button class="btn btn-prev" id="btnPrev">⬅ 이전</button>
    <button class="btn btn-next" id="btnNext">다음 ➡</button>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);

const steps = [
  // 0
  {
    title: '① 두 가지 퍼짐을 비교해 봅시다',
    text: `
      <p>표본의 각 값 Xᵢ에 대해 두 가지 "퍼짐"을 잴 수 있어요.</p>
      <ul style="padding-left:18px;line-height:1.7">
        <li><span class="highlight-red">진짜 모평균 m에서 잰 퍼짐</span> — 우리가 <b>알고 싶은 것</b> (모분산 σ²)</li>
        <li><span class="highlight-blue">표본평균 <span class="xb">X</span>에서 잰 퍼짐</span> — 우리가 <b>실제로 계산할 수 있는 것</b></li>
      </ul>
      <div class="diagram"><canvas id="decompCanvas" width="700" height="310"></canvas></div>
      <p>그림을 보면 표본들은 <span class="xb">X</span> 주위에 모여 있고, <span class="xb">X</span> 자체는 m에서 살짝 떨어져 있죠?</p>
    `,
    drawFn: () => drawStep0()
  },
  // 1
  {
    title: '② 피타고라스처럼 분해됩니다',
    text: `
      <p>놀랍게도 모평균 m 기준 퍼짐의 <b>기댓값</b>은 두 부분으로 깔끔하게 나뉩니다.</p>
      <div class="eqn">
        E[<span class="highlight-red">Σ(Xᵢ − m)²/n</span>] = E[<span class="highlight-blue">Σ(Xᵢ − <span class="xb">X</span>)²/n</span>] + <span class="highlight-yellow">V(<span class="xb">X</span>)</span>
      </div>
      <ul style="padding-left:18px;line-height:1.7">
        <li><span class="highlight-red">표본 ⇄ m 까지의 퍼짐</span> = <span class="highlight-blue">표본 ⇄ <span class="xb">X</span> 까지의 퍼짐</span> + <span class="highlight-yellow"><span class="xb">X</span> ⇄ m 까지의 흔들림</span></li>
      </ul>
      <p style="color:#cbd5e1;font-size:.88rem">📐 마치 직각삼각형의 빗변² = 밑변² + 높이² 처럼!</p>
    `,
    drawFn: () => drawStep1()
  },
  // 2
  {
    title: '③ 기댓값 양변을 정리합니다',
    text: `
      <p>왼쪽 항은 정확히 <b>모분산 σ²</b>입니다. 왜냐하면 각 Xᵢ가 모집단에서 뽑힌 값이므로 E[(Xᵢ−m)²] = σ² 이고, 평균을 내도 그대로 σ²이거든요.</p>
      <div class="eqn"><span class="highlight-yellow">σ²</span> = E[<span class="highlight-blue">Σ(Xᵢ − <span class="xb">X</span>)²/n</span>] + V(<span class="xb">X</span>)</div>
      <p>여기서 우리가 알고 싶은 부분(<span class="xb">X</span> 기준 퍼짐의 기댓값)만 옮겨 봅시다.</p>
      <div class="eqn">E[<span class="highlight-blue">Σ(Xᵢ − <span class="xb">X</span>)²/n</span>] = <span class="highlight-yellow">σ²</span> − V(<span class="xb">X</span>)</div>
    `
  },
  // 3
  {
    title: '④ V(<span class="xb">X</span>) = σ²/n을 대입!',
    text: `
      <p>이미 배웠죠? <b>표본평균의 분산</b>은 V(<span class="xb">X</span>) = σ²/n 입니다.</p>
      <div class="eqn">E[<span class="highlight-blue">Σ(Xᵢ − <span class="xb">X</span>)²/n</span>] = σ² − <span style="color:#fb7185">σ²/n</span></div>
      <div class="eqn">= <span class="highlight-green">(n − 1)/n · σ²</span></div>
      <p>👉 1/n으로 나눈 추정량의 평균은 σ²보다 <b>(n−1)/n 만큼 작게</b> 나옵니다. 그래서 살짝 모자라요!</p>
    `,
    drawFn: () => drawStep3()
  },
  // 4
  {
    title: '⑤ 비밀 공개 — 양변에 n/(n-1)을 곱하자!',
    text: `
      <p>모자란 만큼을 정확히 메꾸려면 양변에 <b>n/(n-1)</b>을 곱하면 됩니다.</p>
      <div class="eqn">
        n/(n−1) · E[<span class="highlight-blue">Σ(Xᵢ − <span class="xb">X</span>)²/n</span>] = n/(n−1) · (n−1)/n · σ² = <span class="highlight-yellow">σ²</span>
      </div>
      <div class="eqn">
        ⟹ E[<span class="highlight-green">Σ(Xᵢ − <span class="xb">X</span>)²/(n−1)</span>] = <span class="highlight-yellow">σ²</span> ✅
      </div>
      <div class="final-card">
        <div style="font-size:1.1rem;font-weight:900;color:#fde047">💎 결론</div>
        <div class="big">
          S² = <span style="font-size:1.1em">1/(n−1)</span> · Σ(Xᵢ − <span class="xb">X</span>)²
        </div>
        <div style="font-size:.92rem;color:#cbd5e1;line-height:1.6">
          이렇게 정의해야 <b>E(S²) = σ²</b>가 되어 <b>불편추정량</b>이 됩니다.<br>
          이게 바로 <b>베셀 보정 (Bessel's correction)</b>이에요!
        </div>
        <div class="tag">🎉 미션 완료!</div>
      </div>
    `,
    drawFn: () => drawStep4()
  }
];

let curr = 0;

function render(){
  const s = steps[curr];
  $('stepBody').innerHTML = `
    <div class="step-title">🌟 ${s.title}</div>
    <div class="step-text">${s.text}</div>
  `;
  // 칩 상태
  document.querySelectorAll('.step-chip').forEach((c,i)=>{
    c.classList.remove('active','done');
    if(i===curr) c.classList.add('active');
    else if(i<curr) c.classList.add('done');
  });
  $('btnPrev').disabled = curr===0;
  $('btnNext').disabled = curr===steps.length-1;
  $('btnNext').textContent = curr===steps.length-1 ? '🎉 끝!' : '다음 ➡';
  if(s.drawFn) setTimeout(s.drawFn, 30);
}

// 캔버스에서 X̄(라벨) 그리기 — X 위에 직접 윗줄을 그어준다
function drawXbarText(ctx2, suffix, cx, y, color, fontStr){
  ctx2.font = fontStr;
  const xW = ctx2.measureText('X').width;
  const sufW = ctx2.measureText(suffix).width;
  const totalW = xW + sufW;
  const left = cx - totalW/2;
  ctx2.fillStyle = color;
  ctx2.textAlign = 'left';
  ctx2.fillText('X', left, y);
  if(suffix) ctx2.fillText(suffix, left + xW, y);
  const fs = parseInt(fontStr) || 13;
  ctx2.strokeStyle = color;
  ctx2.lineWidth = Math.max(1.2, fs/10);
  ctx2.beginPath();
  ctx2.moveTo(left + 0.5, y - fs * 0.88);
  ctx2.lineTo(left + xW - 0.5, y - fs * 0.88);
  ctx2.stroke();
  ctx2.textAlign = 'center';
}

function drawStep0(){
  const cv = $('decompCanvas');
  if(!cv) return;
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  ctx.clearRect(0,0,W,H);

  const baseY = H - 65;
  const padL = 50, padR = 40;
  const xmin = 0, xmax = 100;
  const mappingX = v => padL + (v-xmin)/(xmax-xmin)*(W-padL-padR);

  // 축
  ctx.strokeStyle = 'rgba(203,213,225,0.5)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(mappingX(xmin), baseY); ctx.lineTo(mappingX(xmax), baseY); ctx.stroke();

  // 표본 5개 (시각화용 고정)
  const samp = [42, 48, 53, 60, 67];
  const xbar = samp.reduce((a,b)=>a+b,0)/samp.length;  // 54
  const m = 50;

  // m 선
  const mx = mappingX(m);
  ctx.strokeStyle = '#fb7185';
  ctx.lineWidth = 2.5;
  ctx.setLineDash([6,4]);
  ctx.beginPath(); ctx.moveTo(mx, 24); ctx.lineTo(mx, baseY); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#fb7185';
  ctx.font = 'bold 14px sans-serif';
  ctx.textAlign='center';
  ctx.fillText('m', mx, 16);

  // X̄ 선
  const xx = mappingX(xbar);
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2.5;
  ctx.setLineDash([6,4]);
  ctx.beginPath(); ctx.moveTo(xx, 44); ctx.lineTo(xx, baseY); ctx.stroke();
  ctx.setLineDash([]);
  drawXbarText(ctx, '', xx, 36, '#38bdf8', 'bold 14px sans-serif');

  // 표본 점들 & 거리선
  samp.forEach(v=>{
    const px = mappingX(v);
    // m까지 (빨강)
    ctx.strokeStyle = 'rgba(251,113,133,.45)';
    ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(px, baseY-8); ctx.lineTo(mx, baseY-8); ctx.stroke();
    // X̄까지 (파랑)
    ctx.strokeStyle = 'rgba(56,189,248,.85)';
    ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(px, baseY-28); ctx.lineTo(xx, baseY-28); ctx.stroke();
    // 점
    ctx.beginPath();
    ctx.arc(px, baseY-8, 8, 0, Math.PI*2);
    ctx.fillStyle = '#fbbf24'; ctx.fill();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
  });

  // 범례
  const lgY1 = H - 38;
  const lgY2 = H - 18;
  ctx.fillStyle = '#fb7185';
  ctx.fillRect(8, lgY1-3, 14, 3);
  ctx.fillStyle = '#cbd5e1';
  ctx.font = '12px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('━━ 표본 → m (모분산 기여)', 28, lgY1);
  ctx.fillStyle = '#38bdf8';
  ctx.fillRect(8, lgY2-3, 14, 3);
  ctx.fillStyle = '#cbd5e1';
  // 범례에서 X̄ 부분만 따로 그려 윗줄 표시
  ctx.fillText('━━ 표본 → ', 28, lgY2);
  const xbarLabelX = 28 + ctx.measureText('━━ 표본 → ').width;
  drawXbarText(ctx, ' (계산 가능)', xbarLabelX + ctx.measureText('X (계산 가능)').width/2, lgY2, '#cbd5e1', '12px sans-serif');
}

function drawStep1(){
  const cv = $('decompCanvas');
  if(!cv){
    // canvas 없으면 그냥 종료 (template에서 그릴 자리가 없을 수도)
    return;
  }
  drawStep0();  // 베이스는 같음
}

function drawStep3(){
  // 추가로 그릴 다이어그램 자리 — 생략 (단계 텍스트에 집중)
}

function drawStep4(){
  // 마지막 — 텍스트의 final-card가 핵심
}

$('btnPrev').addEventListener('click', ()=>{ if(curr>0){curr--; render();} });
$('btnNext').addEventListener('click', ()=>{ if(curr<steps.length-1){curr++; render();} });
document.querySelectorAll('.step-chip').forEach(c=>{
  c.addEventListener('click', ()=>{ curr = parseInt(c.dataset.step); render(); });
});
render();
</script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("✨ 표본분산을 n-1로 나누는 이유 (베셀 보정)")
    st.caption(
        "표본평균 X̄ 기준으로 잰 퍼짐은 모평균 m 기준 퍼짐보다 **항상 작거나 같다**는 사실에서 출발해, "
        "그 모자란 양을 정확히 (n−1)로 보정하는 과정을 시각적으로 탐구합니다."
    )

    tab1, tab2, tab3 = st.tabs([
        "🔍 거리 비교",
        "🏁 추정량 경주",
        "✨ (n-1)의 비밀",
    ])

    with tab1:
        components.html(_HTML_TAB1, height=1200, scrolling=True)
    with tab2:
        components.html(_HTML_TAB2, height=1600, scrolling=True)
    with tab3:
        components.html(_HTML_TAB3, height=900, scrolling=True)
