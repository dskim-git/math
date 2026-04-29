import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "이항정규근사"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이항분포의 정규 근사 활동 성찰**"},
    {"key": "근사조건", "label": "이항분포 B(n, p)를 정규분포로 근사할 때 필요한 조건을 쓰고, 그 이유를 설명해 보세요.", "type": "text_area", "height": 90},
    {"key": "연속성보정이유", "label": "연속성 보정(continuity correction)이 필요한 이유를 이산분포와 연속분포의 차이를 활용하여 설명해 보세요.", "type": "text_area", "height": 90},
    {"key": "계산문제", "label": "X ~ B(100, 0.3)일 때, P(25 ≤ X ≤ 35)를 정규 근사(연속성 보정 포함)로 구하는 과정을 써 보세요. (μ=30, σ=√21≈4.58)", "type": "text_area", "height": 120},
    {"key": "새롭게알게된점", "label": "💡 이 활동을 통해 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점", "label": "💬 이 활동을 통해 느낀 점", "type": "text_area", "height": 90},
]

META = {
    "title": "미니: 이항분포의 정규 근사",
    "description": "이항분포 B(n,p)와 정규 근사를 직접 비교하고 연속성 보정의 원리를 시각적으로 탐구합니다.",
    "order": 75,
}

# ─────────────────────────────────────────────────────────────────────────────
# 공통 CSS  (세 탭 HTML에서 반복 사용)
# ─────────────────────────────────────────────────────────────────────────────
_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#e2e8f0;font-size:15px;padding:10px 14px 28px}
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:16px 20px;margin-bottom:14px;backdrop-filter:blur(8px)}
.card-title{font-size:15px;font-weight:700;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.ctrl-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:520px){.ctrl-row{grid-template-columns:1fr}}
.ctrl-group{display:flex;flex-direction:column;gap:6px}
.ctrl-label{font-size:13px;color:#94a3b8;font-weight:600;display:flex;justify-content:space-between;align-items:center}
.badge{background:linear-gradient(135deg,#f59e0b,#ef4444);border-radius:8px;padding:2px 14px;font-weight:900;font-size:16px;color:#fff;min-width:60px;text-align:center;box-shadow:0 0 10px rgba(245,158,11,.4)}
.badge-p{background:linear-gradient(135deg,#6366f1,#8b5cf6);box-shadow:0 0 10px rgba(99,102,241,.4)}
.badge-g{background:linear-gradient(135deg,#10b981,#059669);box-shadow:0 0 10px rgba(16,185,129,.4)}
input[type=range]{-webkit-appearance:none;width:100%;height:7px;border-radius:4px;outline:none;cursor:pointer;margin-top:2px}
.rn{background:linear-gradient(90deg,#f59e0b,#ef4444)}
.rp{background:linear-gradient(90deg,#6366f1,#8b5cf6)}
.ra{background:linear-gradient(90deg,#10b981,#06b6d4)}
.rb{background:linear-gradient(90deg,#f43f5e,#fb923c)}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;background:#fff;border:3px solid #f59e0b;cursor:pointer;box-shadow:0 0 12px rgba(245,158,11,.7);transition:transform .15s}
.rp::-webkit-slider-thumb{border-color:#8b5cf6;box-shadow:0 0 12px rgba(139,92,246,.7)}
.ra::-webkit-slider-thumb{border-color:#10b981;box-shadow:0 0 12px rgba(16,185,129,.7)}
.rb::-webkit-slider-thumb{border-color:#fb923c;box-shadow:0 0 12px rgba(251,146,60,.7)}
input[type=range]::-webkit-slider-thumb:hover{transform:scale(1.25)}
.stat-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.sc{flex:1;min-width:80px;border-radius:14px;padding:11px 8px;text-align:center;border:1.5px solid rgba(255,255,255,.08);background:rgba(0,0,0,.25)}
.sc-mu{border-color:rgba(245,158,11,.45);background:rgba(245,158,11,.07)}
.sc-si{border-color:rgba(16,185,129,.45);background:rgba(16,185,129,.07)}
.sc-np{border-color:rgba(99,102,241,.45);background:rgba(99,102,241,.07)}
.sc-nq{border-color:rgba(244,114,182,.45);background:rgba(244,114,182,.07)}
.sv{font-size:20px;font-weight:900}
.sc-mu .sv{color:#fbbf24}.sc-si .sv{color:#6ee7b7}.sc-np .sv{color:#a5b4fc}.sc-nq .sv{color:#f9a8d4}
.sl{font-size:11px;color:#64748b;font-weight:600;margin-top:3px;letter-spacing:.04em;text-transform:uppercase}
.valid-box{padding:12px 18px;border-radius:14px;margin-bottom:14px;display:flex;align-items:center;gap:12px;font-size:14px;font-weight:600;transition:.3s}
.valid-ok{background:rgba(16,185,129,.12);border:1.5px solid rgba(16,185,129,.4);color:#6ee7b7}
.valid-warn{background:rgba(245,158,11,.12);border:1.5px solid rgba(245,158,11,.4);color:#fbbf24}
.valid-fail{background:rgba(239,68,68,.12);border:1.5px solid rgba(239,68,68,.4);color:#fca5a5}
.presets{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.preset{padding:5px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.05);cursor:pointer;font-size:12px;font-weight:700;color:#94a3b8;transition:.2s}
.preset:hover{background:rgba(245,158,11,.15);color:#fbbf24;border-color:rgba(245,158,11,.4)}
.obs{display:flex;gap:10px;padding:11px 14px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:12px;margin-bottom:8px;font-size:13.5px;color:#cbd5e1;line-height:1.6}
.obs-icon{font-size:20px;flex-shrink:0;line-height:1.4}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(99,102,241,.4);border-radius:3px}
"""

# ─────────────────────────────────────────────────────────────────────────────
# 공통 JS (logFact, binomPMF, normCDF)
# ─────────────────────────────────────────────────────────────────────────────
_MATHJS = """
const _MAXN = 302;
const _LF = new Array(_MAXN).fill(0);
for (let i = 1; i < _MAXN; i++) _LF[i] = _LF[i-1] + Math.log(i);
function bPMF(k, n, p) {
  if (k < 0 || k > n || n >= _MAXN) return 0;
  if (p <= 0) return k === 0 ? 1 : 0;
  if (p >= 1) return k === n ? 1 : 0;
  return Math.exp(_LF[n]-_LF[k]-_LF[n-k]+k*Math.log(p)+(n-k)*Math.log(1-p));
}
function bCDF(b, n, p) {
  let s = 0;
  for (let k = 0; k <= Math.min(b, n); k++) s += bPMF(k, n, p);
  return Math.min(1, s);
}
function nCDF(z) {
  if (z > 8) return 1; if (z < -8) return 0;
  const a = Math.abs(z), t = 1/(1+0.2316419*a);
  const d = Math.exp(-a*a/2)/Math.sqrt(2*Math.PI);
  const q = d*t*(0.319381530+t*(-0.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))));
  return z >= 0 ? 1-q : q;
}
function nPDF(x, mu, si) {
  return Math.exp(-0.5*((x-mu)/si)**2)/(si*Math.sqrt(2*Math.PI));
}
function fmt(v, d=2) { return parseFloat(v).toFixed(d); }
function pct(v) { return (v*100).toFixed(4)+'%'; }
"""

# ─────────────────────────────────────────────────────────────────────────────
# Tab 1 : 정규 근사 시뮬레이터
# ─────────────────────────────────────────────────────────────────────────────
_HTML_SIM = r"""<!doctype html>
<html><head><meta charset="utf-8"><style>
""" + _CSS + r"""
</style></head>
<body>

<div class="card">
  <div class="card-title" style="color:#fbbf24">⚙️ 이항분포 B(n, p) 설정</div>
  <div class="presets">
    <span style="font-size:12px;color:#64748b;font-weight:700;align-self:center">프리셋→</span>
    <button class="preset" onclick="setPreset(10,.5)">B(10, 0.5)</button>
    <button class="preset" onclick="setPreset(30,.4)">B(30, 0.4)</button>
    <button class="preset" onclick="setPreset(50,.3)">B(50, 0.3)</button>
    <button class="preset" onclick="setPreset(100,.5)">B(100, 0.5)</button>
    <button class="preset" onclick="setPreset(200,.3)">B(200, 0.3)</button>
  </div>
  <div class="ctrl-row">
    <div class="ctrl-group">
      <div class="ctrl-label">시행 횟수 <strong>n</strong><span class="badge" id="dN">50</span></div>
      <input type="range" id="rN" class="rn" min="5" max="300" step="1" value="50" oninput="update()">
    </div>
    <div class="ctrl-group">
      <div class="ctrl-label">성공 확률 <strong>p</strong><span class="badge badge-p" id="dP">0.30</span></div>
      <input type="range" id="rP" class="rp" min="1" max="99" step="1" value="30" oninput="update()">
    </div>
  </div>
</div>

<div class="card" style="padding:6px 6px 4px">
  <canvas id="cvs" style="display:block;width:100%;border-radius:12px"></canvas>
</div>

<div class="stat-row">
  <div class="sc sc-mu"><div class="sv" id="sM">—</div><div class="sl">μ = np</div></div>
  <div class="sc sc-si"><div class="sv" id="sS">—</div><div class="sl">σ = √(npq)</div></div>
  <div class="sc sc-np"><div class="sv" id="sNP">—</div><div class="sl">np (≥10?)</div></div>
  <div class="sc sc-nq"><div class="sv" id="sNQ">—</div><div class="sl">n(1−p) (≥10?)</div></div>
</div>

<div class="valid-box" id="validBox">
  <span id="validIcon">⏳</span>
  <span id="validMsg">계산 중...</span>
</div>

<div class="card">
  <div class="card-title" style="color:#f9a8d4">💡 탐구 관찰</div>
  <div id="obsBox"></div>
</div>

<script>
""" + _MATHJS + r"""
const PAD = {l:52, r:22, t:26, b:44};
let cN=50, cP=0.30;

function setPreset(n,p){
  document.getElementById('rN').value=n;
  document.getElementById('rP').value=Math.round(p*100);
  cN=n; cP=p; update();
}
function update(){
  cN=parseInt(document.getElementById('rN').value);
  cP=parseInt(document.getElementById('rP').value)/100;
  document.getElementById('dN').textContent=cN;
  document.getElementById('dP').textContent=fmt(cP);
  const mu=cN*cP, si=Math.sqrt(cN*cP*(1-cP));
  const np=cN*cP, nq=cN*(1-cP);
  document.getElementById('sM').textContent=fmt(mu);
  document.getElementById('sS').textContent=fmt(si,3);
  document.getElementById('sNP').textContent=fmt(np,1);
  document.getElementById('sNQ').textContent=fmt(nq,1);
  // Validity
  const vBox=document.getElementById('validBox');
  if(np>=5&&nq>=5){
    vBox.className='valid-box valid-ok';
    document.getElementById('validIcon').textContent='✅';
    document.getElementById('validMsg').textContent=
      `정규 근사 조건 만족! np=${fmt(np,1)} ≥ 5 이고 n(1−p)=${fmt(nq,1)} ≥ 5 — n이 충분히 큽니다.`;
  } else {
    vBox.className='valid-box valid-fail';
    document.getElementById('validIcon').textContent='❌';
    document.getElementById('validMsg').textContent=
      `조건 불만족: np=${fmt(np,1)}, n(1−p)=${fmt(nq,1)} — np와 n(1−p)가 모두 5 이상이어야 합니다.`;
  }
  updateObs(cN,cP,mu,si);
  draw(cN,cP,mu,si);
}

function updateObs(n,p,mu,si){
  const obs=[];
  if(n<20) obs.push(['🔍',`n이 작을 때(n=${n}) 이항분포는 정규분포와 많이 다릅니다. n을 늘려보세요!`]);
  else if(n>=100) obs.push(['🎯',`n이 충분히 크면(n=${n}) 이항분포의 막대가 정규곡선과 거의 일치합니다!`]);
  else obs.push(['📊',`n이 커질수록 이항분포가 정규분포에 점점 가까워지는 것을 확인하세요.`]);
  if(Math.abs(p-0.5)<0.05) obs.push(['⚖️',`p≈0.5이면 분포가 좌우 대칭으로 나타납니다.`]);
  else if(p<0.3) obs.push(['📐',`p가 작으면(p=${fmt(p)}) 오른쪽으로 치우친 분포가 됩니다. n을 키워 보정해 보세요.`]);
  else if(p>0.7) obs.push(['📐',`p가 크면(p=${fmt(p)}) 왼쪽으로 치우친 분포가 됩니다. n을 키워 보정해 보세요.`]);
  obs.push(['🔢',`μ=${fmt(mu,2)},  σ=${fmt(si,3)},  분산 σ²=${fmt(si**2,2)}`]);
  document.getElementById('obsBox').innerHTML=obs.map(([ic,tx])=>
    `<div class="obs"><span class="obs-icon">${ic}</span><span>${tx}</span></div>`).join('');
}

function draw(n,p,mu,si){
  const cvs=document.getElementById('cvs');
  const ratio=window.devicePixelRatio||1;
  const W=cvs.parentElement.clientWidth||860, H=300;
  cvs.width=W*ratio; cvs.height=H*ratio;
  cvs.style.width=W+'px'; cvs.style.height=H+'px';
  const ctx=cvs.getContext('2d'); ctx.scale(ratio,ratio);

  // background gradient
  const bg=ctx.createLinearGradient(0,0,0,H);
  bg.addColorStop(0,'#0b0f1a'); bg.addColorStop(1,'#060810');
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);

  const kMin=Math.max(0,Math.floor(mu-4.5*si));
  const kMax=Math.min(n,Math.ceil(mu+4.5*si));
  const nBars=kMax-kMin+1;
  if(nBars<=0) return;

  let pmf=[], maxP=0;
  for(let k=kMin;k<=kMax;k++){const v=bPMF(k,n,p);pmf.push(v);if(v>maxP)maxP=v;}

  const yMax=maxP*1.28;
  const cW=W-PAD.l-PAD.r, cH=H-PAD.t-PAD.b;
  const baseY=PAD.t+cH;
  const toX=k=>PAD.l+(k-kMin+0.5)/nBars*cW;
  const toY=y=>PAD.t+cH*(1-Math.min(y,yMax)/yMax);
  const bW=Math.max(1.5, cW/nBars*0.82);

  // μ±σ band
  const bandX1=Math.max(PAD.l, PAD.l+(mu-si-kMin)/nBars*cW);
  const bandX2=Math.min(PAD.l+cW, PAD.l+(mu+si-kMin+1)/nBars*cW);
  ctx.fillStyle='rgba(16,185,129,.06)';
  ctx.fillRect(bandX1,PAD.t,bandX2-bandX1,cH);

  // grid lines (subtle)
  ctx.strokeStyle='rgba(255,255,255,.035)'; ctx.lineWidth=1; ctx.setLineDash([]);
  const step=Math.max(1,Math.round(nBars/10));
  for(let k=kMin;k<=kMax;k+=step){
    const x=toX(k); ctx.beginPath();ctx.moveTo(x,PAD.t);ctx.lineTo(x,baseY);ctx.stroke();
  }

  // normal fill
  ctx.beginPath(); let first=true;
  for(let px=0;px<=cW;px+=0.5){
    const xv=kMin+px/cW*nBars-0.5;
    const yv=nPDF(xv,mu,si);
    const cx=PAD.l+px, cy=toY(yv);
    if(first){ctx.moveTo(cx,cy);first=false;}else ctx.lineTo(cx,cy);
  }
  ctx.lineTo(PAD.l+cW,baseY);ctx.lineTo(PAD.l,baseY);ctx.closePath();
  ctx.fillStyle='rgba(245,158,11,.08)'; ctx.fill();

  // bars
  pmf.forEach((v,i)=>{
    const k=kMin+i;
    const x=toX(k)-bW/2, y=toY(v), bh=baseY-y;
    const g=ctx.createLinearGradient(0,y,0,baseY);
    g.addColorStop(0,'rgba(99,102,241,.95)');
    g.addColorStop(1,'rgba(99,102,241,.35)');
    ctx.fillStyle=g; ctx.fillRect(x,y,bW,bh);
    ctx.strokeStyle='rgba(165,180,252,.35)'; ctx.lineWidth=.5;
    ctx.strokeRect(x,y,bW,bh);
  });

  // normal curve
  ctx.beginPath(); first=true;
  for(let px=0;px<=cW;px+=0.5){
    const xv=kMin+px/cW*nBars-0.5;
    const yv=nPDF(xv,mu,si);
    const cx=PAD.l+px, cy=toY(yv);
    if(first){ctx.moveTo(cx,cy);first=false;}else ctx.lineTo(cx,cy);
  }
  ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2.8;
  ctx.shadowBlur=14; ctx.shadowColor='#f59e0b'; ctx.setLineDash([]);
  ctx.stroke(); ctx.shadowBlur=0;

  // μ vertical line
  const xMu=toX(mu);
  ctx.beginPath();ctx.moveTo(xMu,PAD.t);ctx.lineTo(xMu,baseY);
  ctx.strokeStyle='rgba(255,255,255,.5)'; ctx.lineWidth=1.5; ctx.setLineDash([5,4]);
  ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle='rgba(255,255,255,.85)'; ctx.font='bold 11px Segoe UI,sans-serif';
  ctx.textAlign='center'; ctx.fillText('μ',xMu,PAD.t+14);

  // x axis
  ctx.beginPath();ctx.moveTo(PAD.l,baseY);ctx.lineTo(W-PAD.r,baseY);
  ctx.strokeStyle='rgba(255,255,255,.2)'; ctx.lineWidth=1.5; ctx.setLineDash([]);
  ctx.stroke();
  ctx.fillStyle='#475569'; ctx.font='11px Segoe UI,sans-serif'; ctx.textAlign='center';
  for(let k=kMin;k<=kMax;k+=step) ctx.fillText(k,toX(k),baseY+16);

  // y axis label
  ctx.fillStyle='#334155'; ctx.font='10px Segoe UI,sans-serif'; ctx.textAlign='right';
  for(let i=1;i<=3;i++){
    const yv=maxP*i/3.5;
    ctx.fillText(fmt(yv,3),PAD.l-5,toY(yv)+4);
    ctx.strokeStyle='rgba(255,255,255,.04)'; ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(PAD.l,toY(yv));ctx.lineTo(W-PAD.r,toY(yv));ctx.stroke();
  }

  // legend
  ctx.textAlign='left'; ctx.font='11.5px Segoe UI,sans-serif';
  const lx=PAD.l+8, ly=PAD.t+8;
  ctx.fillStyle='rgba(99,102,241,.85)'; ctx.fillRect(lx,ly,14,10);
  ctx.fillStyle='#a5b4fc'; ctx.fillText('이항분포 B(n,p)',lx+18,ly+9);
  ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2.5; ctx.shadowBlur=8; ctx.shadowColor='#f59e0b';
  ctx.beginPath();ctx.moveTo(lx,ly+22);ctx.lineTo(lx+14,ly+22);ctx.stroke(); ctx.shadowBlur=0;
  ctx.fillStyle='#fbbf24'; ctx.fillText('정규 근사 N(μ, σ²)',lx+18,ly+25);
}

update();
window.addEventListener('resize',()=>draw(cN,cP,cN*cP,Math.sqrt(cN*cP*(1-cP))));
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# Tab 2 : 연속성 보정 탐구
# ─────────────────────────────────────────────────────────────────────────────
_HTML_CC = r"""<!doctype html>
<html><head><meta charset="utf-8"><style>
""" + _CSS + r"""
.cmp-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px}
@media(max-width:540px){.cmp-grid{grid-template-columns:1fr}}
.cmp-card{border-radius:16px;padding:14px 12px;text-align:center;border:1.5px solid}
.cmp-exact{background:rgba(99,102,241,.1);border-color:rgba(99,102,241,.4)}
.cmp-nocc{background:rgba(239,68,68,.1);border-color:rgba(239,68,68,.4)}
.cmp-cc{background:rgba(16,185,129,.1);border-color:rgba(16,185,129,.4)}
.cmp-title{font-size:12px;font-weight:700;letter-spacing:.04em;margin-bottom:8px;text-transform:uppercase}
.cmp-exact .cmp-title{color:#a5b4fc}
.cmp-nocc .cmp-title{color:#fca5a5}
.cmp-cc .cmp-title{color:#6ee7b7}
.cmp-val{font-size:22px;font-weight:900;line-height:1.1}
.cmp-exact .cmp-val{color:#c4b5fd}
.cmp-nocc .cmp-val{color:#f87171}
.cmp-cc .cmp-val{color:#34d399}
.cmp-sub{font-size:11px;color:#64748b;margin-top:6px}
.err-chip{display:inline-block;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:700;margin-top:4px}
.err-better{background:rgba(16,185,129,.2);color:#6ee7b7;border:1px solid rgba(16,185,129,.3)}
.err-worse{background:rgba(239,68,68,.2);color:#fca5a5;border:1px solid rgba(239,68,68,.3)}
.formula-box{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:14px 18px;margin-bottom:8px}
.formula-box p{font-size:13.5px;color:#cbd5e1;line-height:1.7;margin:0}
.formula-box .hl{font-weight:700;color:#fbbf24}
.formula-box .hlg{font-weight:700;color:#6ee7b7}
.formula-box .hlr{font-weight:700;color:#f87171}
.step-box{background:rgba(255,255,255,.03);border-left:3px solid;padding:10px 14px;border-radius:0 10px 10px 0;margin-bottom:8px;font-size:13.5px;color:#cbd5e1;line-height:1.7}
.step-exact{border-color:rgba(99,102,241,.5)}
.step-nocc{border-color:rgba(239,68,68,.5)}
.step-cc{border-color:rgba(16,185,129,.5)}
.step-title{font-size:12px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;margin-bottom:4px}
.step-exact .step-title{color:#a5b4fc}
.step-nocc .step-title{color:#f87171}
.step-cc .step-title{color:#6ee7b7}
</style></head>
<body>

<!-- 개념 설명 -->
<div class="card">
  <div class="card-title" style="color:#fbbf24">🔬 왜 연속성 보정이 필요할까요?</div>
  <div class="obs">
    <span class="obs-icon">📊</span>
    <span><strong>이항분포</strong>는 <em>이산(discrete)</em> 확률변수입니다. 확률이 막대 하나하나에 담겨 있어요.<br>
    반면 <strong>정규분포</strong>는 <em>연속(continuous)</em> 확률변수로, 확률이 곡선 아래의 <em>넓이(면적)</em>로 표현됩니다.</span>
  </div>
  <div class="obs">
    <span class="obs-icon">🎯</span>
    <span>이항분포의 막대 하나(예: X=k)의 넓이는 <strong>가로 1, 세로 P(X=k)</strong>인 직사각형입니다.<br>
    정규곡선으로 이 넓이를 근사하려면 <strong>k−½ 부터 k+½ 까지의 면적</strong>을 써야 합니다.<br>
    이렇게 ±½를 더해주는 것이 바로 <span style="color:#6ee7b7;font-weight:700">연속성 보정(Continuity Correction)</span>입니다.</span>
  </div>
</div>

<!-- 설정 -->
<div class="card">
  <div class="card-title" style="color:#a5b4fc">⚙️ 범위 설정  <span style="font-size:13px;color:#64748b;font-weight:400">(n과 p를 바꾸며 관찰해 보세요)</span></div>
  <div class="ctrl-row" style="margin-bottom:14px">
    <div class="ctrl-group">
      <div class="ctrl-label">시행 수 <strong>n</strong><span class="badge" id="dN2">20</span></div>
      <input type="range" id="rN2" class="rn" min="10" max="100" step="1" value="20" oninput="upd2()">
    </div>
    <div class="ctrl-group">
      <div class="ctrl-label">성공 확률 <strong>p</strong><span class="badge badge-p" id="dP2">0.50</span></div>
      <input type="range" id="rP2" class="rp" min="5" max="95" step="1" value="50" oninput="upd2()">
    </div>
  </div>
  <div class="ctrl-row">
    <div class="ctrl-group">
      <div class="ctrl-label">범위 하한 <strong>a</strong><span class="badge badge-g" id="dA">7</span></div>
      <input type="range" id="rA" class="ra" min="0" max="100" step="1" value="7" oninput="upd2()">
    </div>
    <div class="ctrl-group">
      <div class="ctrl-label">범위 상한 <strong>b</strong><span class="badge" style="background:linear-gradient(135deg,#f43f5e,#fb923c)" id="dB">13</span></div>
      <input type="range" id="rB" class="rb" min="0" max="100" step="1" value="13" oninput="upd2()">
    </div>
  </div>
</div>

<!-- 캔버스 -->
<div class="card" style="padding:6px 6px 4px">
  <canvas id="cvs2" style="display:block;width:100%;border-radius:12px"></canvas>
  <div style="display:flex;gap:18px;flex-wrap:wrap;padding:8px 6px 4px;font-size:12px;font-weight:700">
    <span><span style="display:inline-block;width:12px;height:12px;background:rgba(99,102,241,.85);border-radius:3px;margin-right:5px;vertical-align:middle"></span>이항분포 막대</span>
    <span><span style="display:inline-block;width:12px;height:12px;background:rgba(56,189,248,.7);border-radius:3px;margin-right:5px;vertical-align:middle"></span>선택 범위 [a, b]</span>
    <span><span style="display:inline-block;width:22px;height:3px;background:#f87171;margin-right:5px;vertical-align:middle"></span>보정 없음 경계 (a, b)</span>
    <span><span style="display:inline-block;width:22px;height:3px;background:#34d399;margin-right:5px;vertical-align:middle"></span>보정 있음 경계 (a−½, b+½)</span>
  </div>
</div>

<!-- 비교 결과 -->
<div class="cmp-grid">
  <div class="cmp-card cmp-exact">
    <div class="cmp-title">🎯 정확값 (이항분포)</div>
    <div class="cmp-val" id="cExact">—</div>
    <div class="cmp-sub" id="cExactSub">P(a ≤ X ≤ b)</div>
  </div>
  <div class="cmp-card cmp-nocc">
    <div class="cmp-title">❌ 정규 근사 (보정 없음)</div>
    <div class="cmp-val" id="cNoCC">—</div>
    <div class="cmp-sub">P(a ≤ Y ≤ b)</div>
    <div id="errNoCC"></div>
  </div>
  <div class="cmp-card cmp-cc">
    <div class="cmp-title">✅ 정규 근사 (연속성 보정)</div>
    <div class="cmp-val" id="cCC">—</div>
    <div class="cmp-sub">P(a−½ ≤ Y ≤ b+½)</div>
    <div id="errCC"></div>
  </div>
</div>

<!-- 계산 과정 -->
<div class="card">
  <div class="card-title" style="color:#e2e8f0">📐 계산 과정 비교</div>
  <div class="step-box step-exact"><div class="step-title">정확값</div><div id="stepExact">—</div></div>
  <div class="step-box step-nocc"><div class="step-title">보정 없음</div><div id="stepNoCC">—</div></div>
  <div class="step-box step-cc"><div class="step-title">연속성 보정</div><div id="stepCC">—</div></div>
</div>

<!-- 핵심 공식 -->
<div class="card">
  <div class="card-title" style="color:#fbbf24">📌 연속성 보정 공식 요약</div>
  <div class="formula-box">
    <p>이항분포 X ~ B(n, p)를 Y ~ N(μ, σ²)로 근사할 때 (μ = np, σ = √(npq)):</p>
  </div>
  <div class="formula-box">
    <p>
      <span class="hlr">보정 없음:</span>  P(a ≤ X ≤ b) ≈ Φ(<sup>b − μ</sup>⁄σ) − Φ(<sup>a − μ</sup>⁄σ)<br>
      → 막대의 경계를 정수 그대로 사용 → <em>불정확</em>
    </p>
  </div>
  <div class="formula-box">
    <p>
      <span class="hlg">연속성 보정:</span>  P(a ≤ X ≤ b) ≈ Φ(<sup>b + ½ − μ</sup>⁄σ) − Φ(<sup>a − ½ − μ</sup>⁄σ)<br>
      → 막대 양 끝에 ½씩 더해 넓이를 맞춤 → <em>더 정확!</em>
    </p>
  </div>
</div>

<script>
""" + _MATHJS + r"""
const PAD2={l:52,r:22,t:26,b:44};
let cN2=20, cP2=0.5, cA=7, cB=13;

function upd2(){
  cN2=parseInt(document.getElementById('rN2').value);
  cP2=parseInt(document.getElementById('rP2').value)/100;
  cA=parseInt(document.getElementById('rA').value);
  cB=parseInt(document.getElementById('rB').value);
  // Clamp a,b
  if(cA>cN2){cA=cN2;document.getElementById('rA').value=cA;}
  if(cB>cN2){cB=cN2;document.getElementById('rB').value=cB;}
  if(cA>cB){cB=cA;document.getElementById('rB').value=cB;}
  document.getElementById('dN2').textContent=cN2;
  document.getElementById('dP2').textContent=fmt(cP2);
  document.getElementById('dA').textContent=cA;
  document.getElementById('dB').textContent=cB;
  // Adjust slider ranges
  document.getElementById('rA').max=cN2;
  document.getElementById('rB').max=cN2;

  const mu=cN2*cP2, si=Math.sqrt(cN2*cP2*(1-cP2));
  // Exact
  const exact=bCDF(cB,cN2,cP2)-(cA>0?bCDF(cA-1,cN2,cP2):0);
  // No CC
  const nocc=nCDF((cB-mu)/si)-nCDF((cA-mu)/si);
  // CC
  const cc=nCDF((cB+0.5-mu)/si)-nCDF((cA-0.5-mu)/si);

  document.getElementById('cExact').textContent=fmt(exact,6);
  document.getElementById('cExactSub').textContent=`P(${cA} ≤ X ≤ ${cB})`;
  document.getElementById('cNoCC').textContent=fmt(nocc,6);
  document.getElementById('cCC').textContent=fmt(cc,6);

  const errNoCCv=(nocc-exact);
  const errCCv=(cc-exact);
  document.getElementById('errNoCC').innerHTML=
    `<span class="err-chip ${Math.abs(errNoCCv)>Math.abs(errCCv)?'err-worse':'err-better'}">오차 ${errNoCCv>=0?'+':''}${fmt(errNoCCv,6)}</span>`;
  document.getElementById('errCC').innerHTML=
    `<span class="err-chip ${Math.abs(errCCv)<=Math.abs(errNoCCv)?'err-better':'err-worse'}">오차 ${errCCv>=0?'+':''}${fmt(errCCv,6)}</span>`;

  // Steps
  const zA_nocc=fmt((cA-mu)/si,3), zB_nocc=fmt((cB-mu)/si,3);
  const zA_cc=fmt((cA-0.5-mu)/si,3), zB_cc=fmt((cB+0.5-mu)/si,3);
  document.getElementById('stepExact').innerHTML=
    `∑ P(X=k) for k = ${cA} ~ ${cB} &nbsp;=&nbsp; <strong>${fmt(exact,6)}</strong>`;
  document.getElementById('stepNoCC').innerHTML=
    `Φ(${zB_nocc}) − Φ(${zA_nocc}) &nbsp;=&nbsp; <strong>${fmt(nocc,6)}</strong>`;
  document.getElementById('stepCC').innerHTML=
    `Φ(<sup>${cB}+½−${fmt(mu,2)}</sup>⁄${fmt(si,3)}) − Φ(<sup>${cA}−½−${fmt(mu,2)}</sup>⁄${fmt(si,3)})
    = Φ(${zB_cc}) − Φ(${zA_cc}) &nbsp;=&nbsp; <strong>${fmt(cc,6)}</strong>`;

  drawCC(cN2,cP2,mu,si,cA,cB);
}

function drawCC(n,p,mu,si,a,b){
  const cvs=document.getElementById('cvs2');
  const ratio=window.devicePixelRatio||1;
  const W=cvs.parentElement.clientWidth||860, H=280;
  cvs.width=W*ratio; cvs.height=H*ratio;
  cvs.style.width=W+'px'; cvs.style.height=H+'px';
  const ctx=cvs.getContext('2d'); ctx.scale(ratio,ratio);

  const bg=ctx.createLinearGradient(0,0,0,H);
  bg.addColorStop(0,'#0b0f1a'); bg.addColorStop(1,'#060810');
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);

  const kMin=Math.max(0,Math.floor(mu-4*si));
  const kMax=Math.min(n,Math.ceil(mu+4*si));
  const nBars=kMax-kMin+1;
  if(nBars<=0) return;

  let pmf=[],maxP=0;
  for(let k=kMin;k<=kMax;k++){const v=bPMF(k,n,p);pmf.push(v);if(v>maxP)maxP=v;}
  const yMax=maxP*1.3;
  const cW=W-PAD2.l-PAD2.r, cH=H-PAD2.t-PAD2.b;
  const baseY=PAD2.t+cH;
  const toX=k=>PAD2.l+(k-kMin+0.5)/nBars*cW;
  const toXc=x=>PAD2.l+(x-kMin+0.5)/nBars*cW;
  const toY=y=>PAD2.t+cH*(1-Math.min(y,yMax)/yMax);
  const bW=Math.max(1.5,cW/nBars*0.82);

  // normal fill under [a-0.5, b+0.5] (green tint)
  ctx.beginPath(); let first=true;
  for(let px=0;px<=cW;px+=0.5){
    const xv=kMin+px/cW*nBars-0.5;
    if(xv<a-0.5||xv>b+0.5){first=true;continue;}
    const yv=nPDF(xv,mu,si);
    const cx=PAD2.l+px, cy=toY(yv);
    if(first){ctx.moveTo(toXc(a-0.5),baseY);ctx.lineTo(cx,cy);first=false;}
    else ctx.lineTo(cx,cy);
  }
  ctx.lineTo(toXc(b+0.5),baseY); ctx.closePath();
  ctx.fillStyle='rgba(16,185,129,.15)'; ctx.fill();

  // normal fill under [a, b] (red tint - no CC area)
  ctx.beginPath(); first=true;
  for(let px=0;px<=cW;px+=0.5){
    const xv=kMin+px/cW*nBars-0.5;
    if(xv<a||xv>b){first=true;continue;}
    const yv=nPDF(xv,mu,si);
    const cx=PAD2.l+px, cy=toY(yv);
    if(first){ctx.moveTo(toXc(a),baseY);ctx.lineTo(cx,cy);first=false;}
    else ctx.lineTo(cx,cy);
  }
  ctx.lineTo(toXc(b),baseY); ctx.closePath();
  ctx.fillStyle='rgba(239,68,68,.15)'; ctx.fill();

  // Bars (gray for outside, blue for [a,b])
  pmf.forEach((v,i)=>{
    const k=kMin+i;
    const x=toX(k)-bW/2, y=toY(v), bh=baseY-y;
    const inRange=(k>=a&&k<=b);
    const g=ctx.createLinearGradient(0,y,0,baseY);
    if(inRange){g.addColorStop(0,'rgba(56,189,248,.95)');g.addColorStop(1,'rgba(56,189,248,.35)');}
    else{g.addColorStop(0,'rgba(99,102,241,.6)');g.addColorStop(1,'rgba(99,102,241,.2)');}
    ctx.fillStyle=g; ctx.fillRect(x,y,bW,bh);
    ctx.strokeStyle=inRange?'rgba(125,211,252,.5)':'rgba(165,180,252,.2)';
    ctx.lineWidth=.5; ctx.strokeRect(x,y,bW,bh);
  });

  // Normal curve
  ctx.beginPath(); first=true;
  for(let px=0;px<=cW;px+=0.5){
    const xv=kMin+px/cW*nBars-0.5;
    const yv=nPDF(xv,mu,si);
    const cx=PAD2.l+px, cy=toY(yv);
    if(first){ctx.moveTo(cx,cy);first=false;}else ctx.lineTo(cx,cy);
  }
  ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2.5; ctx.shadowBlur=12; ctx.shadowColor='#f59e0b';
  ctx.setLineDash([]); ctx.stroke(); ctx.shadowBlur=0;

  // No-CC boundary lines (red dashed) at a and b
  function vLine(xv,color,lw,dash){
    const xp=toXc(xv);
    ctx.beginPath();ctx.moveTo(xp,PAD2.t);ctx.lineTo(xp,baseY);
    ctx.strokeStyle=color;ctx.lineWidth=lw;ctx.setLineDash(dash);ctx.stroke();ctx.setLineDash([]);
  }
  vLine(a,'rgba(239,68,68,.85)',1.8,[5,4]);
  vLine(b+1,'rgba(239,68,68,.85)',1.8,[5,4]);  // b right edge = b+1
  // CC boundary lines (green solid) at a-0.5 and b+0.5
  vLine(a-0.5,'rgba(16,185,129,.95)',2.2,[]);
  vLine(b+0.5,'rgba(16,185,129,.95)',2.2,[]);

  // Labels on boundaries
  ctx.font='bold 10px Segoe UI,sans-serif'; ctx.textAlign='center';
  ctx.fillStyle='rgba(239,68,68,.9)';
  ctx.fillText('a='+a, toXc(a), PAD2.t+10);
  ctx.fillText('b='+b, toXc(b+1), PAD2.t+10);
  ctx.fillStyle='rgba(16,185,129,.9)';
  ctx.fillText('a−½', toXc(a-0.5), PAD2.t+20);
  ctx.fillText('b+½', toXc(b+0.5), PAD2.t+20);

  // X axis
  ctx.beginPath();ctx.moveTo(PAD2.l,baseY);ctx.lineTo(W-PAD2.r,baseY);
  ctx.strokeStyle='rgba(255,255,255,.2)';ctx.lineWidth=1.5;ctx.setLineDash([]);ctx.stroke();
  ctx.fillStyle='#475569';ctx.font='11px Segoe UI,sans-serif';ctx.textAlign='center';
  const step=Math.max(1,Math.round(nBars/12));
  for(let k=kMin;k<=kMax;k+=step) ctx.fillText(k,toX(k),baseY+16);
}

upd2();
window.addEventListener('resize',upd2);
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# Tab 3 : 구간 확률 계산기
# ─────────────────────────────────────────────────────────────────────────────
_HTML_CALC = r"""<!doctype html>
<html><head><meta charset="utf-8"><style>
""" + _CSS + r"""
.res-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px}
@media(max-width:540px){.res-grid{grid-template-columns:1fr}}
.rc{border-radius:16px;padding:14px 12px;text-align:center;border:1.5px solid}
.rc-ex{background:rgba(99,102,241,.1);border-color:rgba(99,102,241,.45)}
.rc-nc{background:rgba(239,68,68,.1);border-color:rgba(239,68,68,.45)}
.rc-cc{background:rgba(16,185,129,.1);border-color:rgba(16,185,129,.45)}
.rc-title{font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}
.rc-ex .rc-title{color:#a5b4fc}.rc-nc .rc-title{color:#fca5a5}.rc-cc .rc-title{color:#6ee7b7}
.rc-val{font-size:24px;font-weight:900;line-height:1.1}
.rc-ex .rc-val{color:#c4b5fd}.rc-nc .rc-val{color:#f87171}.rc-cc .rc-val{color:#34d399}
.rc-err{font-size:12px;margin-top:6px}
.errneg{color:#6ee7b7}.errpos{color:#fca5a5}
.prob-range{font-size:13px;color:#64748b;margin-top:4px}
.info-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.ic{flex:1;min-width:70px;border-radius:12px;padding:10px 8px;text-align:center;border:1.5px solid rgba(255,255,255,.08);background:rgba(0,0,0,.25)}
.ic .iv{font-size:18px;font-weight:900;color:#a5b4fc}.ic .il{font-size:11px;color:#64748b;margin-top:2px;letter-spacing:.03em}
.bar-chart-wrap{height:6px;background:rgba(255,255,255,.1);border-radius:3px;margin-top:8px;overflow:hidden}
.bar-chart-fill{height:100%;border-radius:3px;transition:width .5s ease}
.tip-box{background:rgba(245,158,11,.07);border:1px solid rgba(245,158,11,.25);border-radius:12px;padding:12px 16px;font-size:13.5px;color:#fde68a;line-height:1.7}
</style></head>
<body>

<!-- 설정 -->
<div class="card">
  <div class="card-title" style="color:#fbbf24">🧮 구간 확률 계산기 — P(a ≤ X ≤ b)</div>
  <div class="ctrl-row" style="margin-bottom:14px">
    <div class="ctrl-group">
      <div class="ctrl-label">시행 수 <strong>n</strong><span class="badge" id="dN3">100</span></div>
      <input type="range" id="rN3" class="rn" min="10" max="300" step="1" value="100" oninput="upd3()">
    </div>
    <div class="ctrl-group">
      <div class="ctrl-label">성공 확률 <strong>p</strong><span class="badge badge-p" id="dP3">0.30</span></div>
      <input type="range" id="rP3" class="rp" min="5" max="95" step="1" value="30" oninput="upd3()">
    </div>
  </div>
  <div class="ctrl-row">
    <div class="ctrl-group">
      <div class="ctrl-label">범위 하한 <strong>a</strong><span class="badge badge-g" id="dA3">25</span></div>
      <input type="range" id="rA3" class="ra" min="0" max="300" step="1" value="25" oninput="upd3()">
    </div>
    <div class="ctrl-group">
      <div class="ctrl-label">범위 상한 <strong>b</strong><span class="badge" style="background:linear-gradient(135deg,#f43f5e,#fb923c)" id="dB3">35</span></div>
      <input type="range" id="rB3" class="rb" min="0" max="300" step="1" value="35" oninput="upd3()">
    </div>
  </div>
</div>

<!-- 분포 정보 -->
<div class="info-row">
  <div class="ic"><div class="iv" id="i3mu">—</div><div class="il">μ = np</div></div>
  <div class="ic"><div class="iv" id="i3si">—</div><div class="il">σ = √(npq)</div></div>
  <div class="ic"><div class="iv" id="i3np">—</div><div class="il">np</div></div>
  <div class="ic"><div class="iv" id="i3nq">—</div><div class="il">n(1−p)</div></div>
</div>

<!-- 캔버스 -->
<div class="card" style="padding:6px 6px 4px">
  <canvas id="cvs3" style="display:block;width:100%;border-radius:12px"></canvas>
</div>

<!-- 결과 -->
<div class="res-grid">
  <div class="rc rc-ex">
    <div class="rc-title">🎯 정확값</div>
    <div class="rc-val" id="r3ex">—</div>
    <div class="prob-range" id="r3exRange">P(a ≤ X ≤ b)</div>
    <div class="bar-chart-wrap"><div class="bar-chart-fill" id="b3ex" style="background:#6366f1;width:0%"></div></div>
  </div>
  <div class="rc rc-nc">
    <div class="rc-title">❌ 보정 없음</div>
    <div class="rc-val" id="r3nc">—</div>
    <div class="prob-range">P(a ≤ Y ≤ b)</div>
    <div class="rc-err" id="e3nc"></div>
    <div class="bar-chart-wrap"><div class="bar-chart-fill" id="b3nc" style="background:#ef4444;width:0%"></div></div>
  </div>
  <div class="rc rc-cc">
    <div class="rc-title">✅ 연속성 보정</div>
    <div class="rc-val" id="r3cc">—</div>
    <div class="prob-range">P(a−½ ≤ Y ≤ b+½)</div>
    <div class="rc-err" id="e3cc"></div>
    <div class="bar-chart-wrap"><div class="bar-chart-fill" id="b3cc" style="background:#10b981;width:0%"></div></div>
  </div>
</div>

<!-- 계산 단계 -->
<div class="card">
  <div class="card-title" style="color:#e2e8f0">📐 계산 단계별 보기</div>
  <div class="obs" id="stepInfo">—</div>
  <div class="tip-box" id="tipBox">결과를 계산 중입니다...</div>
</div>

<script>
""" + _MATHJS + r"""
const PAD3={l:52,r:22,t:26,b:44};
let cN3=100, cP3=0.30, cA3=25, cB3=35;

function upd3(){
  cN3=parseInt(document.getElementById('rN3').value);
  cP3=parseInt(document.getElementById('rP3').value)/100;
  cA3=parseInt(document.getElementById('rA3').value);
  cB3=parseInt(document.getElementById('rB3').value);
  document.getElementById('rA3').max=cN3;
  document.getElementById('rB3').max=cN3;
  if(cA3>cN3){cA3=cN3;document.getElementById('rA3').value=cA3;}
  if(cB3>cN3){cB3=cN3;document.getElementById('rB3').value=cB3;}
  if(cA3>cB3){cB3=cA3;document.getElementById('rB3').value=cB3;}
  document.getElementById('dN3').textContent=cN3;
  document.getElementById('dP3').textContent=fmt(cP3);
  document.getElementById('dA3').textContent=cA3;
  document.getElementById('dB3').textContent=cB3;

  const mu=cN3*cP3, si=Math.sqrt(cN3*cP3*(1-cP3));
  document.getElementById('i3mu').textContent=fmt(mu);
  document.getElementById('i3si').textContent=fmt(si,3);
  document.getElementById('i3np').textContent=fmt(cN3*cP3,1);
  document.getElementById('i3nq').textContent=fmt(cN3*(1-cP3),1);

  const exact=bCDF(cB3,cN3,cP3)-(cA3>0?bCDF(cA3-1,cN3,cP3):0);
  const nocc=nCDF((cB3-mu)/si)-nCDF((cA3-mu)/si);
  const cc=nCDF((cB3+0.5-mu)/si)-nCDF((cA3-0.5-mu)/si);

  document.getElementById('r3ex').textContent=fmt(exact,5);
  document.getElementById('r3nc').textContent=fmt(nocc,5);
  document.getElementById('r3cc').textContent=fmt(cc,5);
  document.getElementById('r3exRange').textContent=`P(${cA3} ≤ X ≤ ${cB3})`;

  const eNC=nocc-exact, eCC=cc-exact;
  const ePct=(v,base)=>base>0?fmt(Math.abs(v/base)*100,2)+'%':'—';
  document.getElementById('e3nc').innerHTML=
    `<span class="${Math.abs(eNC)>Math.abs(eCC)?'errpos':'errneg'}">오차 ${eNC>=0?'+':''}${fmt(eNC,6)}</span>`;
  document.getElementById('e3cc').innerHTML=
    `<span class="${Math.abs(eCC)<=Math.abs(eNC)?'errneg':'errpos'}">오차 ${eCC>=0?'+':''}${fmt(eCC,6)}</span>`;

  // Bar progress
  const maxV=Math.max(exact,nocc,cc,0.001);
  document.getElementById('b3ex').style.width=(exact/maxV*100)+'%';
  document.getElementById('b3nc').style.width=(nocc/maxV*100)+'%';
  document.getElementById('b3cc').style.width=(cc/maxV*100)+'%';

  // Step info
  const zA_nc=fmt((cA3-mu)/si,3), zB_nc=fmt((cB3-mu)/si,3);
  const zA_cc=fmt((cA3-0.5-mu)/si,3), zB_cc=fmt((cB3+0.5-mu)/si,3);
  document.getElementById('stepInfo').innerHTML=
    `<span class="obs-icon">📌</span>
    <span>
      μ = ${fmt(mu,2)},  σ = ${fmt(si,3)}<br>
      <span style="color:#fca5a5">보정없음:</span> z<sub>a</sub> = ${zA_nc},  z<sub>b</sub> = ${zB_nc}  →  Φ(${zB_nc}) − Φ(${zA_nc}) = <strong>${fmt(nocc,5)}</strong><br>
      <span style="color:#6ee7b7">연속보정:</span> z<sub>a</sub> = ${zA_cc},  z<sub>b</sub> = ${zB_cc}  →  Φ(${zB_cc}) − Φ(${zA_cc}) = <strong>${fmt(cc,5)}</strong>
    </span>`;

  // Tip
  const absNC=Math.abs(eNC), absCC=Math.abs(eCC);
  const improvement=absNC>0?(((absNC-absCC)/absNC)*100).toFixed(1):0;
  let tip='';
  if(absCC<absNC){
    tip=`✅ 연속성 보정을 사용하면 오차가 <strong>${fmt(absNC,5)}</strong> → <strong>${fmt(absCC,5)}</strong>로 줄어듭니다! (약 ${improvement}% 개선)`;
  } else {
    tip=`이 경우 보정 없는 근사의 오차(${fmt(absNC,5)})와 보정 있는 근사의 오차(${fmt(absCC,5)})가 비슷합니다.`;
  }
  document.getElementById('tipBox').innerHTML=tip;

  drawCalc(cN3,cP3,mu,si,cA3,cB3);
}

function drawCalc(n,p,mu,si,a,b){
  const cvs=document.getElementById('cvs3');
  const ratio=window.devicePixelRatio||1;
  const W=cvs.parentElement.clientWidth||860, H=280;
  cvs.width=W*ratio; cvs.height=H*ratio;
  cvs.style.width=W+'px'; cvs.style.height=H+'px';
  const ctx=cvs.getContext('2d'); ctx.scale(ratio,ratio);

  const bg=ctx.createLinearGradient(0,0,0,H);
  bg.addColorStop(0,'#0b0f1a'); bg.addColorStop(1,'#060810');
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);

  const kMin=Math.max(0,Math.floor(mu-4.5*si));
  const kMax=Math.min(n,Math.ceil(mu+4.5*si));
  const nBars=kMax-kMin+1;
  if(nBars<=0) return;

  let pmf=[],maxP=0;
  for(let k=kMin;k<=kMax;k++){const v=bPMF(k,n,p);pmf.push(v);if(v>maxP)maxP=v;}
  const yMax=maxP*1.3;
  const cW=W-PAD3.l-PAD3.r, cH=H-PAD3.t-PAD3.b;
  const baseY=PAD3.t+cH;
  const toX=k=>PAD3.l+(k-kMin+0.5)/nBars*cW;
  const toXc=x=>PAD3.l+(x-kMin+0.5)/nBars*cW;
  const toY=y=>PAD3.t+cH*(1-Math.min(y,yMax)/yMax);
  const bW=Math.max(1.5,cW/nBars*0.82);

  // Highlighted normal fill [a-0.5, b+0.5]
  ctx.beginPath(); let first=true;
  for(let px=0;px<=cW;px+=0.5){
    const xv=kMin+px/cW*nBars-0.5;
    if(xv<a-0.5||xv>b+0.5){first=true;continue;}
    const yv=nPDF(xv,mu,si);
    const cx=PAD3.l+px, cy=toY(yv);
    if(first){ctx.moveTo(toXc(a-0.5),baseY);ctx.lineTo(cx,cy);first=false;}
    else ctx.lineTo(cx,cy);
  }
  ctx.lineTo(toXc(b+0.5),baseY); ctx.closePath();
  ctx.fillStyle='rgba(16,185,129,.12)'; ctx.fill();

  // Bars
  pmf.forEach((v,i)=>{
    const k=kMin+i;
    const x=toX(k)-bW/2, y=toY(v), bh=baseY-y;
    const inR=(k>=a&&k<=b);
    const g=ctx.createLinearGradient(0,y,0,baseY);
    if(inR){g.addColorStop(0,'rgba(56,189,248,.95)');g.addColorStop(1,'rgba(56,189,248,.35)');}
    else{g.addColorStop(0,'rgba(99,102,241,.55)');g.addColorStop(1,'rgba(99,102,241,.18)');}
    ctx.fillStyle=g; ctx.fillRect(x,y,bW,bh);
    ctx.strokeStyle=inR?'rgba(125,211,252,.4)':'rgba(165,180,252,.15)';
    ctx.lineWidth=.5; ctx.strokeRect(x,y,bW,bh);
  });

  // Normal curve
  ctx.beginPath(); first=true;
  for(let px=0;px<=cW;px+=0.5){
    const xv=kMin+px/cW*nBars-0.5;
    const yv=nPDF(xv,mu,si);
    const cx=PAD3.l+px, cy=toY(yv);
    if(first){ctx.moveTo(cx,cy);first=false;}else ctx.lineTo(cx,cy);
  }
  ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2.5; ctx.shadowBlur=12; ctx.shadowColor='#f59e0b';
  ctx.setLineDash([]); ctx.stroke(); ctx.shadowBlur=0;

  // CC boundary lines
  function vLine(xv,color,lw,dash){
    const xp=toXc(xv);
    ctx.beginPath();ctx.moveTo(xp,PAD3.t);ctx.lineTo(xp,baseY);
    ctx.strokeStyle=color;ctx.lineWidth=lw;ctx.setLineDash(dash);ctx.stroke();ctx.setLineDash([]);
  }
  vLine(a,'rgba(239,68,68,.7)',1.5,[4,4]);
  vLine(b+1,'rgba(239,68,68,.7)',1.5,[4,4]);
  vLine(a-0.5,'rgba(16,185,129,.9)',2,[]);
  vLine(b+0.5,'rgba(16,185,129,.9)',2,[]);

  // X axis
  ctx.beginPath();ctx.moveTo(PAD3.l,baseY);ctx.lineTo(W-PAD3.r,baseY);
  ctx.strokeStyle='rgba(255,255,255,.2)';ctx.lineWidth=1.5;ctx.setLineDash([]);ctx.stroke();
  ctx.fillStyle='#475569';ctx.font='11px Segoe UI,sans-serif';ctx.textAlign='center';
  const step=Math.max(1,Math.round(nBars/12));
  for(let k=kMin;k<=kMax;k+=step) ctx.fillText(k,toX(k),baseY+16);

  // μ line
  const xMu=toX(mu);
  ctx.beginPath();ctx.moveTo(xMu,PAD3.t);ctx.lineTo(xMu,baseY);
  ctx.strokeStyle='rgba(255,255,255,.4)';ctx.lineWidth=1.5;ctx.setLineDash([5,4]);ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='rgba(255,255,255,.75)';ctx.font='bold 11px Segoe UI,sans-serif';
  ctx.textAlign='center';ctx.fillText('μ',xMu,PAD3.t+13);

  // legend
  ctx.textAlign='left';ctx.font='11px Segoe UI,sans-serif';
  const lx=PAD3.l+8, ly=PAD3.t+6;
  ctx.fillStyle='rgba(56,189,248,.85)';ctx.fillRect(lx,ly,12,10);
  ctx.fillStyle='#7dd3fc';ctx.fillText('P(a≤X≤b) 범위',lx+16,ly+9);
  ctx.strokeStyle='rgba(16,185,129,.9)';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(lx,ly+22);ctx.lineTo(lx+12,ly+22);ctx.stroke();
  ctx.fillStyle='#6ee7b7';ctx.fillText('보정 경계 (a−½, b+½)',lx+16,ly+24);
}

upd3();
window.addEventListener('resize',upd3);
</script>
</body></html>"""


# ─────────────────────────────────────────────────────────────────────────────
# render
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.header("📊 이항분포의 정규 근사")
    st.markdown(
        "이항분포 **B(n, p)**에서 n이 충분히 크면 정규분포 **N(np, npq)**로 근사할 수 있습니다. "
        "세 가지 탭을 통해 직접 시뮬레이션하며 원리를 탐구해 보세요."
    )

    t1, t2, t3 = st.tabs([
        "🎯 정규 근사 시뮬레이터",
        "🔬 연속성 보정 탐구",
        "🧮 구간 확률 계산기",
    ])
    with t1:
        components.html(_HTML_SIM, height=1020, scrolling=False)
    with t2:
        components.html(_HTML_CC, height=1950, scrolling=False)
    with t3:
        components.html(_HTML_CALC, height=1080, scrolling=False)

    st.markdown("---")
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
