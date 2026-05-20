# activities/probability_new/mini/ci_confidence_tradeoff_lab.py
"""
신뢰도 ↔ 신뢰구간 길이(정확도) 트레이드오프 실험실
- (Part 1) 같은 신뢰도에서 왼쪽 꼬리 비율을 바꿔보며 "왜 대칭이 최단인가"를 시각화
- (Part 2) 신뢰도를 1%p씩 올릴 때 길이가 얼마나 늘어나는지(증가분 ΔL) 막대 차트로 비교
"""
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "🎯 미니: 신뢰도 ↔ 신뢰구간 길이 트레이드오프",
    "description": "같은 신뢰도에서 왜 대칭 신뢰구간이 가장 짧은지, 그리고 신뢰도를 올릴수록 길이가 얼마나 늘어나는지 시각적으로 탐험합니다.",
    "order": 21,
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
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0f172a 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}

/* ============ 헤더 ============ */
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(244,114,182,.2),rgba(56,189,248,.2));
  border:2px solid rgba(244,114,182,.5);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.55rem;font-weight:900;color:#f9a8d4;margin-bottom:4px;letter-spacing:.3px}
.hdr p{font-size:1.05rem;color:#cbd5e1;line-height:1.6}
.hdr b{color:#fde047}

/* ============ 패널 ============ */
.panel{
  background:rgba(15,23,42,.72);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:16px;margin-bottom:14px;
}
.panel h2{
  font-size:1.2rem;font-weight:900;color:#a5b4fc;margin-bottom:11px;
  display:flex;align-items:center;gap:9px;letter-spacing:.3px;
}
.panel h2 .badge{
  font-size:.85rem;color:#cbd5e1;background:rgba(99,102,241,.18);
  padding:3px 9px;border-radius:999px;font-weight:700;
}

/* ============ 슬라이더 ============ */
.ctl-row{
  display:flex;align-items:center;gap:11px;flex-wrap:wrap;
  background:rgba(56,189,248,.07);border:1.5px solid rgba(56,189,248,.32);
  border-radius:11px;padding:11px 13px;margin-bottom:9px;
}
.ctl-lab{font-size:1.05rem;font-weight:800;color:#7dd3fc;min-width:170px}
.ctl-range{flex:1;min-width:170px;accent-color:#38bdf8;height:6px}
.ctl-val{
  font-size:1.45rem;font-weight:900;color:#fde047;min-width:84px;
  background:rgba(15,23,42,.7);padding:3px 13px;border-radius:9px;text-align:center;
}

/* ============ 분포 캔버스 ============ */
.canvas-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(56,189,248,.3);
  border-radius:12px;padding:12px;
}
#normCanvas{display:block;width:100%;height:320px;background:rgba(15,23,42,.4);border-radius:8px}

/* ============ 지표 카드 ============ */
.metrics{
  display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:11px;
}
@media(max-width:760px){.metrics{grid-template-columns:1fr 1fr}}
.mc{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(168,85,247,.4);
  border-radius:11px;padding:11px;text-align:center;
}
.mc .lab{font-size:.95rem;color:#c4b5fd;font-weight:800;margin-bottom:3px;letter-spacing:.3px}
.mc .val{font-size:1.5rem;color:#fef3c7;font-weight:900}
.mc.diff .val{color:#fda4af}
.mc.best .val{color:#86efac}

/* ============ 길이 곡선 작은 그래프 ============ */
.minichart-wrap{
  margin-top:12px;background:rgba(15,23,42,.55);
  border:1.5px solid rgba(168,85,247,.3);border-radius:11px;padding:11px;
}
.minichart-wrap h3{
  font-size:1rem;color:#c4b5fd;font-weight:800;margin-bottom:6px;letter-spacing:.3px;
}
#lengthMini{display:block;width:100%;height:170px;background:rgba(15,23,42,.4);border-radius:8px}

/* ============ Part2 바 차트 ============ */
#stepChart{display:block;width:100%;height:380px;background:rgba(15,23,42,.4);border-radius:8px}
.legend{
  display:flex;flex-wrap:wrap;gap:13px;justify-content:center;
  font-size:.95rem;color:#cbd5e1;font-weight:700;margin-top:9px;
}
.lg{display:flex;align-items:center;gap:6px}
.lg .swatch{display:inline-block;width:22px;height:12px;border-radius:3px}

/* ============ 인사이트 ============ */
.insight{
  background:rgba(251,191,36,.1);border:2px solid rgba(251,191,36,.45);
  border-radius:13px;padding:13px 16px;margin-top:12px;
  font-size:1.02rem;color:#fef3c7;line-height:1.65;
  display:flex;align-items:flex-start;gap:10px;
}
.insight .ico{font-size:1.6rem;flex-shrink:0;line-height:1.2}
.insight b{color:#fde047}
.insight em{color:#fda4af;font-style:normal;font-weight:800}

/* ============ 형성평가 박스 ============ */
.formula-box{
  background:linear-gradient(135deg,rgba(56,189,248,.13),rgba(168,85,247,.13));
  border:2px solid rgba(56,189,248,.4);border-radius:12px;
  padding:13px 17px;text-align:center;margin-bottom:10px;
}
.formula-box .eq{
  font-size:1.5rem;color:#7dd3fc;font-weight:900;letter-spacing:.5px;
  font-family:'Cambria','Times New Roman',serif;
}
.formula-box .eq sub{font-size:.7em}
.formula-box .desc{font-size:.95rem;color:#cbd5e1;margin-top:5px}
</style>
</head>
<body>

<div class="hdr">
  <h1>🎯 신뢰도와 신뢰구간 길이의 트레이드오프</h1>
  <p>같은 신뢰도에서 <b>대칭 신뢰구간</b>이 최단이 되는 이유를 보고,<br>
     신뢰도를 1%p 올릴 때마다 길이가 얼마나 늘어나는지 비교해 봐요!</p>
</div>

<!-- ===================== Part 1 ===================== -->
<div class="panel">
  <h2>① 같은 신뢰도에서 <span style="color:#fde047">대칭</span>이 왜 최단일까?
       <span class="badge">표준정규 N(0,1) 위에서 비교</span></h2>

  <div class="formula-box">
    <div class="eq">L &nbsp;=&nbsp; (z<sub>R</sub> − z<sub>L</sub>) × σ/√n</div>
    <div class="desc">파란 면적(=신뢰도)을 그대로 둔 채로 양쪽 경계만 움직여 봅니다.</div>
  </div>

  <div class="ctl-row">
    <span class="ctl-lab">신뢰도 (1−α)</span>
    <input type="range" min="0.50" max="0.999" step="0.001" value="0.95" class="ctl-range" id="confRange">
    <span class="ctl-val" id="confVal">95.0%</span>
  </div>
  <div class="ctl-row">
    <span class="ctl-lab">왼쪽 꼬리 비율 α<sub>L</sub>/α</span>
    <input type="range" min="0.001" max="0.999" step="0.001" value="0.500" class="ctl-range" id="shareRange">
    <span class="ctl-val" id="shareVal">0.500</span>
  </div>

  <div class="canvas-wrap">
    <canvas id="normCanvas" width="980" height="320"></canvas>
  </div>

  <div class="metrics">
    <div class="mc">
      <div class="lab">현재 길이 L (단위: σ/√n)</div>
      <div class="val" id="curLen">--</div>
    </div>
    <div class="mc best">
      <div class="lab">대칭 길이 L<sub>min</sub></div>
      <div class="val" id="symLen">--</div>
    </div>
    <div class="mc diff">
      <div class="lab">길이 차이 (현재 − 대칭)</div>
      <div class="val" id="diffLen">--</div>
    </div>
  </div>

  <div class="minichart-wrap">
    <h3>📈 왼쪽 꼬리 비율을 0 → 1 로 바꿀 때 길이 L 의 변화</h3>
    <canvas id="lengthMini" width="980" height="170"></canvas>
  </div>

  <div class="insight">
    <span class="ico">💡</span>
    <span>
      파란 면적(신뢰도)을 그대로 둔 채로 양쪽 꼬리를 비대칭으로 만들면 길이가 길어져요.
      길이가 가장 짧은 지점은 항상 <b>왼쪽 꼬리 = 오른쪽 꼬리 = α/2</b>인 <em>대칭</em>이에요!
    </span>
  </div>
</div>

<!-- ===================== Part 2 ===================== -->
<div class="panel">
  <h2>② 신뢰도를 1%p 올리면 <span style="color:#fda4af">길이(정확도)</span>는 얼마나 희생될까?
       <span class="badge">대칭 신뢰구간 기준</span></h2>

  <div class="canvas-wrap">
    <canvas id="stepChart" width="980" height="380"></canvas>
    <div class="legend">
      <span class="lg"><span class="swatch" style="background:#38bdf8"></span> 신뢰구간 길이 L</span>
      <span class="lg"><span class="swatch" style="background:#f43f5e"></span> 직전 단계 대비 늘어난 ΔL</span>
      <span class="lg"><span class="swatch" style="background:#fde047"></span> 현재 선택한 신뢰도</span>
    </div>
  </div>

  <div class="insight">
    <span class="ico">⚖️</span>
    <span>
      50%에서 95%까지 1%p씩 올리는 데 들어가는 비용은 <b>천천히</b> 늘어나지만,
      95% → 99%로 가는 마지막 4%p는 길이가 <em>가파르게</em> 늘어나요.<br>
      → 학교 통계에서 <b>95%</b>를 표준처럼 쓰는 이유 중 하나예요!
    </span>
  </div>
</div>

<script>
/* =============== 표준정규 분위수(Acklam 근사) =============== */
function normPpf(p){
  if(p <= 0) return -Infinity;
  if(p >= 1) return  Infinity;
  const a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,
           1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00];
  const b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,
            6.680131188771972e+01,-1.328068155288572e+01];
  const c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,
           -2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00];
  const d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,
           3.754408661907416e+00];
  const plow=0.02425, phigh=1-plow;
  if(p<plow){
    const q=Math.sqrt(-2*Math.log(p));
    return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
           ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
  }
  if(p>phigh){
    const q=Math.sqrt(-2*Math.log(1-p));
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
            ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
  }
  const q=p-0.5, r=q*q;
  return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q /
         (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);
}
function pdf(x){ return (1/Math.sqrt(2*Math.PI))*Math.exp(-x*x/2); }
function fmt(v,d=3){ if(!isFinite(v)) return '--'; return Number(v.toFixed(d)).toString(); }

/* =============== 상태 =============== */
let CL = 0.95;
let share = 0.5;     // α_L / α
const $ = id => document.getElementById(id);

/* =============== Part 1: 분포 캔버스 =============== */
function drawNorm(){
  const cv = $('normCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=44, padR=22, padT=22, padB=44;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;

  const xMin = -4.0, xMax = 4.0;
  const X = x => padL + ((x-xMin)/(xMax-xMin))*plotW;
  const yMaxPdf = 0.42;
  const Y = y => padT + plotH - (y/yMaxPdf)*plotH;

  // 격자
  ctx.strokeStyle='rgba(148,163,184,.13)'; ctx.setLineDash([3,3]); ctx.lineWidth=1;
  for(let i=1;i<=4;i++){
    const y = padT + (i/4)*plotH;
    ctx.beginPath(); ctx.moveTo(padL,y); ctx.lineTo(W-padR,y); ctx.stroke();
  }
  ctx.setLineDash([]);

  // 면적 채우기 (현재 구간)
  const alpha = 1 - CL;
  const eps = 1e-6;
  const aL = alpha * (eps + (1-2*eps)*share);
  const aR = alpha - aL;
  const zl = normPpf(aL);
  const zr = normPpf(1 - aR);

  // 색 면적
  ctx.fillStyle = 'rgba(56,189,248,.32)';
  ctx.beginPath();
  ctx.moveTo(X(zl), Y(0));
  const steps = 200;
  for(let i=0;i<=steps;i++){
    const x = zl + (zr-zl)*(i/steps);
    ctx.lineTo(X(x), Y(pdf(x)));
  }
  ctx.lineTo(X(zr), Y(0));
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle = 'rgba(56,189,248,.7)';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // 정규분포 곡선
  ctx.strokeStyle = '#a5b4fc';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  for(let i=0;i<=400;i++){
    const x = xMin + (xMax-xMin)*i/400;
    if(i===0) ctx.moveTo(X(x),Y(pdf(x)));
    else ctx.lineTo(X(x),Y(pdf(x)));
  }
  ctx.stroke();

  // 대칭 경계 (참조선)
  const zSym = normPpf(1 - alpha/2);
  ctx.strokeStyle = 'rgba(134,239,172,.85)';
  ctx.setLineDash([6,4]);
  ctx.lineWidth = 2;
  [-zSym, zSym].forEach(z=>{
    ctx.beginPath();
    ctx.moveTo(X(z), padT); ctx.lineTo(X(z), padT+plotH);
    ctx.stroke();
  });
  ctx.setLineDash([]);
  ctx.fillStyle = '#86efac';
  ctx.font = 'bold 12px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='bottom';
  ctx.fillText('대칭 −z', X(-zSym), padT-2);
  ctx.fillText('대칭 +z', X(zSym),  padT-2);

  // 현재 경계
  ctx.strokeStyle = '#f43f5e';
  ctx.lineWidth = 3;
  [zl, zr].forEach(z=>{
    ctx.beginPath();
    ctx.moveTo(X(z), padT+8); ctx.lineTo(X(z), padT+plotH);
    ctx.stroke();
  });
  ctx.fillStyle = '#fda4af';
  ctx.font = 'bold 14px sans-serif';
  ctx.fillText('z_L='+fmt(zl,2), X(zl), padT+8);
  ctx.fillText('z_R='+fmt(zr,2), X(zr), padT+8);

  // x축
  ctx.strokeStyle = 'rgba(148,163,184,.5)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(padL, padT+plotH); ctx.lineTo(W-padR, padT+plotH);
  ctx.stroke();
  ctx.fillStyle = '#94a3b8';
  ctx.font = '13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  for(let v=-4;v<=4;v++){
    const x = X(v);
    ctx.beginPath();
    ctx.strokeStyle='rgba(148,163,184,.4)';
    ctx.moveTo(x, padT+plotH); ctx.lineTo(x, padT+plotH+5);
    ctx.stroke();
    ctx.fillText(v+'', x, padT+plotH+8);
  }
  ctx.fillStyle = '#cbd5e1';
  ctx.font = 'bold 13px sans-serif';
  ctx.fillText('Z (표준화)', W/2, H-14);

  // 면적 라벨
  ctx.fillStyle = '#7dd3fc';
  ctx.font = 'bold 14px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText('면적 = '+fmt(CL*100,1)+'%', X((zl+zr)/2), Y(pdf((zl+zr)/2)*0.55));

  // 길이 표시 (수치)
  $('curLen').textContent = fmt(zr - zl, 3);
  $('symLen').textContent = fmt(2*zSym, 3);
  $('diffLen').textContent = fmt((zr-zl) - 2*zSym, 3);
}

/* =============== Part 1 보조: 길이 미니 그래프 =============== */
function drawLenMini(){
  const cv = $('lengthMini');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=44, padR=22, padT=18, padB=34;
  const plotW=W-padL-padR, plotH=H-padT-padB;
  const alpha = 1-CL, eps=1e-6;

  // r ∈ [0,1] → L(r)
  const N=201;
  const rs=[], Ls=[];
  for(let i=0;i<N;i++){
    const r = i/(N-1);
    const aL = alpha*(eps + (1-2*eps)*r);
    const aR = alpha - aL;
    const zl = normPpf(aL);
    const zr = normPpf(1 - aR);
    rs.push(r); Ls.push(zr-zl);
  }
  const lmin = Math.min(...Ls), lmax = Math.max(...Ls);
  const X = r => padL + r*plotW;
  const Y = L => padT+plotH - ((L-lmin)/Math.max(1e-9, lmax-lmin))*plotH*0.9 - 6;

  // 축
  ctx.strokeStyle='rgba(148,163,184,.5)';
  ctx.beginPath();
  ctx.moveTo(padL, padT+plotH); ctx.lineTo(W-padR, padT+plotH);
  ctx.stroke();

  // 곡선
  ctx.strokeStyle='#a5b4fc'; ctx.lineWidth=2.5;
  ctx.beginPath();
  for(let i=0;i<N;i++){
    if(i===0) ctx.moveTo(X(rs[i]),Y(Ls[i]));
    else ctx.lineTo(X(rs[i]),Y(Ls[i]));
  }
  ctx.stroke();

  // 대칭(최단) 마크
  ctx.strokeStyle='#86efac'; ctx.setLineDash([6,4]); ctx.lineWidth=2;
  ctx.beginPath();
  ctx.moveTo(X(0.5), padT); ctx.lineTo(X(0.5), padT+plotH);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#86efac';
  ctx.font='bold 12px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  ctx.fillText('대칭(최단)', X(0.5), padT+2);

  // 현재 위치 표시
  const aL2 = alpha*(eps + (1-2*eps)*share);
  const aR2 = alpha - aL2;
  const Lcur = normPpf(1-aR2) - normPpf(aL2);
  ctx.fillStyle='#fde047';
  ctx.beginPath();
  ctx.arc(X(share), Y(Lcur), 6, 0, Math.PI*2);
  ctx.fill();
  ctx.strokeStyle='#fde047'; ctx.setLineDash([3,3]); ctx.lineWidth=1.5;
  ctx.beginPath();
  ctx.moveTo(X(share), padT); ctx.lineTo(X(share), padT+plotH);
  ctx.stroke();
  ctx.setLineDash([]);

  // x 라벨
  ctx.fillStyle='#94a3b8';
  ctx.font='12px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  [0,0.25,0.5,0.75,1].forEach(r=>{
    ctx.fillText(r.toFixed(2), X(r), padT+plotH+6);
  });
  ctx.fillStyle='#cbd5e1';
  ctx.font='bold 12px sans-serif';
  ctx.fillText('왼쪽 꼬리 비율  α_L / α', W/2, H-14);
}

/* =============== Part 2: 1%p 막대 차트 =============== */
function drawStepChart(){
  const cv = $('stepChart');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=52, padR=22, padT=28, padB=64;
  const plotW=W-padL-padR, plotH=H-padT-padB;

  const CLs=[], Ls=[];
  for(let p=50; p<=99; p++){
    const a = 1 - p/100;
    const z = normPpf(1 - a/2);
    CLs.push(p); Ls.push(2*z);
  }
  const Lmax = Math.max(...Ls);
  const bw = plotW / CLs.length;
  const X = i => padL + i*bw;
  const Y = L => padT + plotH - (L/Lmax)*plotH*0.96;

  // 격자
  ctx.strokeStyle='rgba(148,163,184,.13)'; ctx.setLineDash([3,3]);
  for(let i=1;i<=5;i++){
    const y = padT + (i/5)*plotH;
    ctx.beginPath(); ctx.moveTo(padL,y); ctx.lineTo(W-padR,y); ctx.stroke();
  }
  ctx.setLineDash([]);

  // 막대 (L)
  for(let i=0;i<CLs.length;i++){
    const x = X(i), y = Y(Ls[i]);
    ctx.fillStyle='rgba(56,189,248,.6)';
    ctx.fillRect(x+1, y, bw-2, padT+plotH-y);
  }
  // ΔL (마지막에서 직전 대비 차이) — 위에 빨간 막대
  for(let i=1;i<CLs.length;i++){
    const dL = Ls[i] - Ls[i-1];
    if(dL <= 0) continue;
    const x = X(i);
    const yT = Y(Ls[i]);
    const yB = Y(Ls[i] - dL);
    ctx.fillStyle = 'rgba(244,63,94,.85)';
    ctx.fillRect(x+1, yT, bw-2, yB-yT);
  }

  // 현재 선택 강조
  const sel = Math.round(CL*100);
  const selIdx = sel - 50;
  if(selIdx >= 0 && selIdx < CLs.length){
    ctx.strokeStyle = '#fde047';
    ctx.lineWidth = 3;
    const x = X(selIdx), y = Y(Ls[selIdx]);
    ctx.strokeRect(x, y-2, bw, padT+plotH-y+2);
    ctx.fillStyle='#fde047';
    ctx.font='bold 13px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='bottom';
    ctx.fillText('L='+fmt(Ls[selIdx],2), x+bw/2, y-4);
  }

  // x축 라벨
  ctx.fillStyle='#cbd5e1';
  ctx.font='12px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  [50,60,70,80,90,95,99].forEach(p=>{
    const i = p-50;
    ctx.fillText(p+'%', X(i)+bw/2, padT+plotH+6);
  });
  ctx.strokeStyle='rgba(148,163,184,.5)';
  ctx.beginPath();
  ctx.moveTo(padL, padT+plotH); ctx.lineTo(W-padR, padT+plotH);
  ctx.stroke();

  // y축 라벨 (값)
  ctx.fillStyle='#94a3b8';
  ctx.textAlign='right'; ctx.textBaseline='middle';
  for(let i=0;i<=5;i++){
    const L = Lmax*(i/5);
    const y = padT+plotH - (L/Lmax)*plotH*0.96;
    ctx.fillText(L.toFixed(1), padL-6, y);
  }

  // 제목
  ctx.fillStyle='#cbd5e1';
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  ctx.fillText('신뢰도 (%)', W/2, H-22);
  ctx.save();
  ctx.translate(14, H/2);
  ctx.rotate(-Math.PI/2);
  ctx.fillText('구간 길이 L (단위: σ/√n)', 0, 0);
  ctx.restore();
}

/* =============== 이벤트 =============== */
function updateAll(){
  $('confVal').textContent = (CL*100).toFixed(1) + '%';
  $('shareVal').textContent = share.toFixed(3);
  drawNorm();
  drawLenMini();
  drawStepChart();
}

$('confRange').addEventListener('input', e=>{
  CL = parseFloat(e.target.value);
  updateAll();
});
$('shareRange').addEventListener('input', e=>{
  share = parseFloat(e.target.value);
  updateAll();
});
window.addEventListener('resize', updateAll);
updateAll();
</script>
</body>
</html>
"""


def render():
    st.subheader("🎯 신뢰도 ↔ 신뢰구간 길이 트레이드오프 실험실")
    st.caption(
        "같은 신뢰도에서 **대칭 신뢰구간**이 왜 가장 짧은지 시각으로 확인하고, "
        "신뢰도를 1%p씩 올릴 때 길이가 어떻게 변하는지 비교해 봅니다."
    )
    components.html(_HTML, height=2300, scrolling=True)
