# activities/probability_new/mini/ci_meaning_lab.py
"""
신뢰도의 의미 — 100개의 신뢰구간 실험실
- 3가지 모집단(학생 키 / 수학 시험 점수 / 줄넘기 횟수)에서 표본 100세트를 임의 추출
- 각 표본의 평균을 중심으로 95% 등의 신뢰구간을 그리고
  모평균 μ를 포함하는 구간(✔초록)과 그렇지 않은 구간(✘빨강) 개수를 시각화
- "신뢰도 95%" = "이렇게 만든 신뢰구간 중 약 95개가 μ를 포함" 의미를 체험
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🌐 미니: 신뢰도의 의미 — 100개의 신뢰구간",
    "description": "모집단에서 표본 100세트를 뽑아 평균의 신뢰구간을 그려보고, "
                   "신뢰도와 모평균 포함 비율의 관계를 직접 체험합니다.",
    "order": 22,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "신뢰도의의미"

_QUESTIONS = [
    {"type": "markdown",
     "text": "**📝 활동 성찰 — 신뢰도의 진짜 의미**"},
    {
        "key": "신뢰도95_의미",
        "label": "신뢰도를 **95%** 로 설정하고 표본 100세트를 여러 번 다시 뽑아 보았을 때, "
                 "모평균 μ를 포함하는 신뢰구간의 개수는 보통 몇 개쯤 나왔나요? "
                 "왜 정확히 매번 95개가 아니라 그 **근처에서 흔들리는지** 본인의 말로 설명해 보세요.",
        "type": "text_area", "height": 110,
        "placeholder": "보통 ___개 정도가 나왔다. 매번 정확히 95개가 아닌 이유는 ___ 이기 때문이다.",
    },
    {
        "key": "신뢰도_바꾸면",
        "label": "신뢰도를 **80% / 95% / 99%** 로 각각 바꿔 보았을 때, "
                 "녹색(포함) 구간의 비율과 신뢰구간의 길이는 어떻게 달라졌나요?",
        "type": "text_area", "height": 110,
        "placeholder": "신뢰도를 높이면 포함 비율은 ___, 구간의 길이는 ___. "
                       "신뢰도를 낮추면 ___ ...",
    },
    {
        "key": "표본크기n_바꾸면",
        "label": "표본 크기 **n** 을 작게(예: n=5)와 크게(예: n=80) 바꿔 보았을 때, "
                 "100개의 신뢰구간의 모양은 어떻게 달라졌나요?",
        "type": "text_area", "height": 100,
        "placeholder": "n이 작을 때는 구간이 ___, n이 클 때는 ___ ...",
    },
    {
        "key": "잘못된_해석",
        "label": "친구가 “95% 신뢰구간은 모평균이 그 구간 안에 들어있을 확률이 95%다”라고 말했어요. "
                 "이 활동을 본 뒤, 이 말을 어떻게 **바로잡아** 설명할 수 있을까요?",
        "type": "text_area", "height": 120,
        "placeholder": "이미 만든 구간 하나에 대해서는 μ가 그 안에 있거나 없거나 둘 중 하나이다. "
                       "신뢰도는 ___ 라는 의미이다.",
    },
    {
        "key": "신뢰도_정의_나만의말",
        "label": "이 활동을 통해 알게 된 **신뢰도(예: 95%)**의 의미를 본인의 말로 다시 한 줄로 적어 보세요.",
        "type": "text_area", "height": 80,
        "placeholder": "신뢰도 95%란 ___ 라는 뜻이다.",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area", "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 활동을 마친 후 느낀 점",
        "type": "text_area", "height": 90,
    },
]


_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#0c2742 50%,#0f172a 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}

/* ============ 헤더 ============ */
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(34,197,94,.18),rgba(244,63,94,.18));
  border:2px solid rgba(34,197,94,.45);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.55rem;font-weight:900;color:#86efac;margin-bottom:5px;letter-spacing:.3px}
.hdr p{font-size:1.05rem;color:#cbd5e1;line-height:1.6}
.hdr b{color:#fde047}

/* ============ 패널 ============ */
.panel{
  background:rgba(15,23,42,.72);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px;margin-bottom:13px;
}
.panel h2{
  font-size:1.18rem;font-weight:900;color:#a5b4fc;margin-bottom:11px;
  display:flex;align-items:center;gap:9px;letter-spacing:.3px;
}
.panel h2 .badge{
  font-size:.85rem;color:#cbd5e1;background:rgba(99,102,241,.18);
  padding:3px 9px;border-radius:999px;font-weight:700;
}

/* ============ 모집단 프리셋 ============ */
.preset-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:11px}
.preset{
  padding:10px 16px;border-radius:999px;font-size:1rem;font-weight:800;
  border:2px solid transparent;cursor:pointer;color:#fff;
  background:linear-gradient(135deg,#475569,#334155);
  transition:all .14s ease;
}
.preset:hover{transform:translateY(-1px)}
.preset.active{
  background:linear-gradient(135deg,#10b981,#047857);
  border-color:#86efac;box-shadow:0 4px 12px rgba(16,185,129,.45);color:#fff;
}

/* ============ 모집단 정보 ============ */
.pop-info{
  display:grid;grid-template-columns:repeat(4,1fr);gap:9px;
}
@media(max-width:760px){.pop-info{grid-template-columns:repeat(2,1fr)}}
.psc{
  background:rgba(34,197,94,.07);border:1.5px solid rgba(34,197,94,.4);
  border-radius:11px;padding:10px;text-align:center;
}
.psc .lab{font-size:.95rem;color:#86efac;font-weight:800;margin-bottom:3px}
.psc .val{font-size:1.4rem;color:#dcfce7;font-weight:900}

/* ============ 컨트롤 ============ */
.ctl-row{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  background:rgba(56,189,248,.07);border:1.5px solid rgba(56,189,248,.32);
  border-radius:11px;padding:10px 13px;margin-bottom:9px;
}
.ctl-lab{font-size:1.05rem;font-weight:800;color:#7dd3fc;min-width:140px}
.ctl-range{flex:1;min-width:160px;accent-color:#38bdf8;height:6px}
.ctl-val{
  font-size:1.4rem;font-weight:900;color:#fde047;min-width:78px;
  background:rgba(15,23,42,.7);padding:3px 13px;border-radius:9px;text-align:center;
}
.ctl-toggle{
  display:flex;align-items:center;gap:9px;padding:8px 12px;
  background:rgba(168,85,247,.08);border:1.5px solid rgba(168,85,247,.35);
  border-radius:11px;cursor:pointer;font-weight:800;color:#c4b5fd;font-size:.98rem;
  user-select:none;
}
.ctl-toggle input{accent-color:#a855f7;width:18px;height:18px;cursor:pointer}

.btn-row{display:flex;gap:9px;flex-wrap:wrap;margin-top:6px}
.btn{
  padding:12px 17px;border:none;border-radius:11px;
  font-size:1.05rem;font-weight:900;color:#fff;cursor:pointer;
  transition:all .15s ease;letter-spacing:.3px;
}
.btn:active{transform:scale(.96)}
.btn-pri{background:linear-gradient(135deg,#22c55e,#15803d);box-shadow:0 3px 10px rgba(34,197,94,.4);flex:1;min-width:170px}
.btn-pri:hover{background:linear-gradient(135deg,#16a34a,#14532d);transform:translateY(-1px)}
.btn-sec{background:linear-gradient(135deg,#3b82f6,#1d4ed8);box-shadow:0 3px 10px rgba(59,130,246,.4)}
.btn-sec:hover{background:linear-gradient(135deg,#2563eb,#1e40af);transform:translateY(-1px)}
.btn-ghost{background:rgba(71,85,105,.65);border:1.5px solid rgba(148,163,184,.3)}

/* ============ 캔버스 ============ */
.canvas-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.3);
  border-radius:12px;padding:12px;
}
#ciCanvas{display:block;width:100%;height:760px;background:rgba(15,23,42,.4);border-radius:8px}

/* ============ 결과 카드 ============ */
.result-card{
  display:flex;flex-wrap:wrap;align-items:center;gap:14px;
  background:linear-gradient(135deg,rgba(34,197,94,.13),rgba(56,189,248,.13));
  border:2px solid rgba(34,197,94,.5);
  border-radius:14px;padding:16px 19px;margin-top:13px;
}
.result-big{
  font-size:2.6rem;font-weight:900;letter-spacing:.5px;line-height:1;
  font-variant-numeric:tabular-nums;
}
.result-big.ok{color:#86efac}
.result-big.bad{color:#fca5a5}
.result-label{font-size:1.05rem;color:#cbd5e1;line-height:1.5}
.result-label b{color:#fde047}
.result-mini{
  font-size:.95rem;color:#94a3b8;
}

/* ============ 누적 통계 ============ */
.hist-wrap{
  display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-top:13px;
}
@media(max-width:780px){.hist-wrap{grid-template-columns:1fr}}
.hist-card{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(56,189,248,.3);
  border-radius:11px;padding:12px;
}
.hist-card h3{
  font-size:1rem;color:#7dd3fc;font-weight:800;margin-bottom:7px;letter-spacing:.3px;
  display:flex;justify-content:space-between;align-items:center;
}
.hist-card h3 .right{
  font-size:.95rem;color:#cbd5e1;font-weight:700;
}
.hist-canvas{display:block;width:100%;height:150px;background:rgba(15,23,42,.4);border-radius:8px}

/* ============ 인사이트 ============ */
.insight{
  background:rgba(251,191,36,.1);border:2px solid rgba(251,191,36,.45);
  border-radius:13px;padding:13px 16px;margin-top:12px;
  font-size:1.02rem;color:#fef3c7;line-height:1.65;
  display:flex;align-items:flex-start;gap:10px;
}
.insight .ico{font-size:1.6rem;flex-shrink:0;line-height:1.2}
.insight b{color:#fde047}
</style>
</head>
<body>

<div class="hdr">
  <h1>🌐 신뢰도의 의미 — 100개의 신뢰구간</h1>
  <p>같은 모집단에서 표본을 <b>100세트</b> 뽑아 95% 신뢰구간을 100개 만들어 봐요.<br>
     그중 모평균 <b>μ</b>를 포함하는 구간이 정말 약 <b>95개</b>인지 직접 확인해 봅시다!</p>
</div>

<!-- ① 모집단 -->
<div class="panel">
  <h2>🎒 모집단 선택 <span class="badge">실생활 데이터 3가지</span></h2>
  <div class="preset-row" id="presetRow">
    <button class="preset active" data-key="heights">📏 학생 키 (cm)</button>
    <button class="preset" data-key="scores">📝 수학 시험 점수 (점)</button>
    <button class="preset" data-key="jumprope">🪢 1분 줄넘기 횟수 (회)</button>
  </div>
  <div class="pop-info">
    <div class="psc"><div class="lab">모집단 크기 N</div><div class="val" id="kN">--</div></div>
    <div class="psc"><div class="lab">모평균 μ</div><div class="val" id="kMu">--</div></div>
    <div class="psc"><div class="lab">모표준편차 σ</div><div class="val" id="kSd">--</div></div>
    <div class="psc"><div class="lab">단위</div><div class="val" id="kUnit">--</div></div>
  </div>
</div>

<!-- ② 표본/신뢰도 설정 -->
<div class="panel">
  <h2>🎲 표본 추출과 신뢰도 설정 <span class="badge">표본 100세트를 한꺼번에</span></h2>

  <div class="ctl-row">
    <span class="ctl-lab">표본 크기 n</span>
    <input type="range" min="2" max="100" value="30" class="ctl-range" id="nRange">
    <span class="ctl-val" id="nVal">30</span>
  </div>
  <div class="ctl-row">
    <span class="ctl-lab">신뢰도 (%)</span>
    <input type="range" min="50" max="99" value="95" class="ctl-range" id="confRange">
    <span class="ctl-val" id="confVal">95%</span>
  </div>
  <div class="ctl-row">
    <label class="ctl-toggle">
      <input type="checkbox" id="useSigma" checked>
      길이를 일정하게 (모표준편차 σ 사용: z-구간)
    </label>
  </div>

  <div class="btn-row">
    <button class="btn btn-pri" id="btnDraw">🎲 표본 100세트 새로 추출</button>
    <button class="btn btn-sec" id="btnReplay">▶ 한 줄씩 다시 그리기 (애니메이션)</button>
    <button class="btn btn-ghost" id="btnClear">🔄 누적 통계 초기화</button>
  </div>
</div>

<!-- ③ 신뢰구간 시각화 -->
<div class="panel">
  <h2>📊 100개의 신뢰구간 <span class="badge">초록=μ포함, 빨강=μ제외</span></h2>
  <div class="canvas-wrap">
    <canvas id="ciCanvas" width="980" height="760"></canvas>
  </div>

  <div class="result-card">
    <div class="result-big ok" id="okCount">--</div>
    <div class="result-label">
      <div style="font-size:1.2rem;font-weight:900;color:#dcfce7">μ를 포함한 신뢰구간 / 100개</div>
      <div>선택한 신뢰도: <b id="confDisp">95%</b> · 기대: <b id="expDisp">약 95개</b> 포함</div>
    </div>
    <div class="result-big bad" id="badCount" style="margin-left:auto">--</div>
    <div class="result-label">
      <div style="font-size:1.05rem;font-weight:900;color:#fee2e2">μ 제외 / 100개</div>
      <div class="result-mini">난수 시드가 바뀔 때마다 포함 개수는 95 근처에서 흔들립니다.</div>
    </div>
  </div>

  <!-- 누적 -->
  <div class="hist-wrap">
    <div class="hist-card">
      <h3>📈 최근 추출 누적 (시도 = <span id="totTrials">0</span>회)
        <span class="right">평균 포함 비율: <b id="avgCover" style="color:#fde047">--</b></span>
      </h3>
      <canvas id="trialChart" class="hist-canvas" width="700" height="150"></canvas>
    </div>
    <div class="hist-card">
      <h3>🔍 표본평균 X̄들의 분포 <span class="right" id="binInfo"></span></h3>
      <canvas id="meanHist" class="hist-canvas" width="700" height="150"></canvas>
    </div>
  </div>

  <div class="insight">
    <span class="ico">💡</span>
    <span>
      “신뢰도 95%”는 “지금 만든 신뢰구간 안에 μ가 95% 확률로 들어있다”는 뜻이 <b>아니에요</b>.<br>
      <b>같은 방법으로 표본을 매우 많이 뽑으면, 그렇게 만든 신뢰구간들 중 약 95%가 μ를 포함한다</b>는 의미예요!
    </span>
  </div>
</div>

<script>
/* =============== 표준정규/t 분포 =============== */
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
/* 간단 t-분포 분위수 근사 (df ≥ 3일 때 충분히 정확):
   Cornish-Fisher 형태로 표준정규에서 보정. df=2 이하는 표본크기 n≥3 가정이라 무시. */
function tPpf(p, df){
  if(df > 200) return normPpf(p);
  const z = normPpf(p);
  const g1 = (z*z*z + z) / (4*df);
  const g2 = (5*z*z*z*z*z + 16*z*z*z + 3*z) / (96*df*df);
  const g3 = (3*z*z*z*z*z*z*z + 19*z*z*z*z*z + 17*z*z*z - 15*z) / (384*df*df*df);
  return z + g1 + g2 + g3;
}

/* =============== 시드 RNG =============== */
function mulberry32(seed){
  let s = seed >>> 0;
  return function(){
    s = (s + 0x6D2B79F5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function boxMuller(rng){
  let u=0,v=0;
  while(u===0) u=rng();
  while(v===0) v=rng();
  return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);
}

/* =============== 모집단 =============== */
function makeHeights(){
  const rng=mulberry32(20251); const arr=[];
  for(let i=0;i<200;i++){
    let v=168+boxMuller(rng)*6.2;
    v=Math.max(150,Math.min(188,v));
    arr.push(Math.round(v*10)/10);
  }
  return arr;
}
function makeScores(){
  const rng=mulberry32(73821); const arr=[];
  for(let i=0;i<200;i++){
    let v=72+boxMuller(rng)*14;
    v=Math.max(15,Math.min(100,v));
    arr.push(Math.round(v));
  }
  return arr;
}
function makeJumprope(){
  const rng=mulberry32(91234); const arr=[];
  for(let i=0;i<200;i++){
    const shape=4; let v=0;
    for(let k=0;k<shape;k++) v += -Math.log(1-rng())*22;
    v=v+28; v=Math.max(30,Math.min(240,v));
    arr.push(Math.round(v));
  }
  return arr;
}
const POPULATIONS = {
  heights:  {label:"학생 키", data:makeHeights(),  unit:"cm", showInt:false},
  scores:   {label:"수학 시험 점수", data:makeScores(),   unit:"점", showInt:true},
  jumprope: {label:"1분 줄넘기 횟수", data:makeJumprope(), unit:"회", showInt:true},
};

function popStats(arr){
  const n=arr.length;
  const mu = arr.reduce((a,b)=>a+b,0)/n;
  const v  = arr.reduce((s,x)=>s+(x-mu)*(x-mu),0)/n;
  return {n, mu, sd:Math.sqrt(v), var:v, min:Math.min(...arr), max:Math.max(...arr)};
}

/* =============== 상태 =============== */
let curKey="heights";
let n=30, CL=0.95, useSigma=true;
let drawRng = mulberry32(Date.now() & 0xFFFFFFFF);
let intervals = [];  // [{lo,hi,mean,ok}, ...]
let trialHistory = [];  // 매 추출당 포함 개수 (0~100)

const $ = id => document.getElementById(id);
function fmt(v,d=2){ if(!isFinite(v)) return '--'; return Number(v.toFixed(d)).toString(); }

/* =============== 표본 추출 + CI 계산 =============== */
function drawOneSample(){
  const data = POPULATIONS[curKey].data;
  const N = data.length;
  const vals = new Array(n);
  for(let i=0;i<n;i++) vals[i] = data[Math.floor(drawRng()*N)];
  let mean = vals.reduce((a,b)=>a+b,0)/n;
  let s = 0;
  if(n>1){
    const v = vals.reduce((s,x)=>s+(x-mean)*(x-mean),0)/(n-1);
    s = Math.sqrt(v);
  }
  return {vals, mean, s};
}
function makeCI(sam){
  const alpha = 1-CL;
  const ps = popStats(POPULATIONS[curKey].data);
  let half;
  if(useSigma){
    const z = normPpf(1 - alpha/2);
    half = z * (ps.sd / Math.sqrt(n));
  } else {
    const tt = tPpf(1 - alpha/2, Math.max(1, n-1));
    half = tt * (sam.s / Math.sqrt(n));
  }
  const lo = sam.mean - half;
  const hi = sam.mean + half;
  const ok = (lo <= ps.mu) && (ps.mu <= hi);
  return {lo, hi, mean:sam.mean, ok};
}
function doDraw100(){
  intervals = [];
  for(let i=0;i<100;i++){
    intervals.push(makeCI(drawOneSample()));
  }
  const okN = intervals.filter(x=>x.ok).length;
  trialHistory.push(okN);
  redraw();
}

/* =============== 캔버스: 메인 100개 신뢰구간 =============== */
let animTimer = null;
let shown = 100;  // 표시할 구간 수 (애니메이션용)
function startReplayAnim(){
  if(animTimer){ clearInterval(animTimer); animTimer=null; }
  shown = 0;
  animTimer = setInterval(()=>{
    shown += 2;
    if(shown >= 100){ shown=100; clearInterval(animTimer); animTimer=null; }
    drawCIMain();
  }, 30);
}

function drawCIMain(){
  const cv = $('ciCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=58, padR=140, padT=30, padB=44;
  const plotW=W-padL-padR, plotH=H-padT-padB;

  const ps = popStats(POPULATIONS[curKey].data);
  if(intervals.length === 0){
    ctx.fillStyle='#94a3b8';
    ctx.font='16px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('🎲 위 버튼으로 표본을 추출해 주세요', W/2, H/2);
    return;
  }

  // x 범위
  let lo = Math.min(...intervals.map(c=>c.lo), ps.mu);
  let hi = Math.max(...intervals.map(c=>c.hi), ps.mu);
  const pad = (hi-lo)*0.07 || 1;
  lo -= pad; hi += pad;
  const X = v => padL + ((v-lo)/(hi-lo))*plotW;

  // 격자
  ctx.strokeStyle='rgba(148,163,184,.15)'; ctx.setLineDash([3,3]); ctx.lineWidth=1;
  const xTicks=6;
  for(let i=0;i<=xTicks;i++){
    const v = lo + (hi-lo)*i/xTicks;
    const x = X(v);
    ctx.beginPath();
    ctx.moveTo(x, padT); ctx.lineTo(x, padT+plotH);
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // 모평균 수직선
  const xMu = X(ps.mu);
  ctx.strokeStyle='#fbbf24'; ctx.lineWidth=3;
  ctx.beginPath();
  ctx.moveTo(xMu, padT); ctx.lineTo(xMu, padT+plotH);
  ctx.stroke();
  ctx.fillStyle='#fde047';
  ctx.font='bold 15px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText('μ = '+fmt(ps.mu,2)+' '+POPULATIONS[curKey].unit, xMu, padT-7);

  // 100개 구간
  const rowH = plotH/100;
  for(let i=0;i<Math.min(shown, intervals.length);i++){
    const it = intervals[i];
    const y = padT + i*rowH + rowH/2;
    const x1 = X(it.lo), x2 = X(it.hi), xm = X(it.mean);
    ctx.strokeStyle = it.ok ? 'rgba(34,197,94,.88)' : 'rgba(244,63,94,.88)';
    ctx.lineWidth = Math.max(1.5, rowH-2);
    ctx.beginPath();
    ctx.moveTo(x1, y); ctx.lineTo(x2, y);
    ctx.stroke();
    // 평균 점
    ctx.fillStyle = it.ok ? '#dcfce7' : '#fee2e2';
    ctx.beginPath();
    ctx.arc(xm, y, Math.max(1.5, rowH*0.4), 0, Math.PI*2);
    ctx.fill();
  }

  // x축 라벨
  ctx.strokeStyle='rgba(148,163,184,.5)';
  ctx.beginPath();
  ctx.moveTo(padL, padT+plotH); ctx.lineTo(W-padR, padT+plotH);
  ctx.stroke();
  ctx.fillStyle='#cbd5e1';
  ctx.font='13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  for(let i=0;i<=xTicks;i++){
    const v = lo + (hi-lo)*i/xTicks;
    ctx.fillText(POPULATIONS[curKey].showInt ? Math.round(v)+'' : v.toFixed(1), X(v), padT+plotH+6);
  }
  ctx.fillStyle='#94a3b8';
  ctx.font='bold 13px sans-serif';
  ctx.fillText('값 ('+POPULATIONS[curKey].unit+')', W/2, H-16);

  // 오른쪽: ✔/✘ 표시
  const okCnt = intervals.slice(0,shown).filter(x=>x.ok).length;
  const badCnt = shown - okCnt;
  ctx.fillStyle='#86efac';
  ctx.font='bold 14px sans-serif';
  ctx.textAlign='left'; ctx.textBaseline='top';
  ctx.fillText('✔ μ 포함: '+okCnt, W-padR+10, padT+20);
  ctx.fillStyle='#fca5a5';
  ctx.fillText('✘ μ 제외: '+badCnt, W-padR+10, padT+44);
  ctx.fillStyle='#cbd5e1';
  ctx.font='12px sans-serif';
  ctx.fillText('진행: '+shown+'/100', W-padR+10, padT+68);

  // 표시 상단 결과 카드 업데이트
  $('okCount').textContent = okCnt;
  $('badCount').textContent = badCnt;
  $('okCount').className = 'result-big ok';
  $('badCount').className = 'result-big bad';
}

/* =============== 누적 시도 차트 =============== */
function drawTrialChart(){
  const cv = $('trialChart');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=30, padR=18, padT=10, padB=20;
  const plotW=W-padL-padR, plotH=H-padT-padB;

  // y범위: 50~100
  const yMin=50, yMax=100;
  const Y = v => padT+plotH - ((v-yMin)/(yMax-yMin))*plotH;

  // 격자 + 기대선
  ctx.strokeStyle='rgba(148,163,184,.13)'; ctx.setLineDash([3,3]); ctx.lineWidth=1;
  [60,70,80,90,100].forEach(v=>{
    ctx.beginPath();
    ctx.moveTo(padL, Y(v)); ctx.lineTo(W-padR, Y(v));
    ctx.stroke();
  });
  ctx.setLineDash([]);

  // 기대치 (신뢰도) 선
  const exp = Math.round(CL*100);
  ctx.strokeStyle='#fbbf24'; ctx.lineWidth=2;
  ctx.beginPath();
  ctx.moveTo(padL, Y(exp)); ctx.lineTo(W-padR, Y(exp));
  ctx.stroke();
  ctx.fillStyle='#fde047';
  ctx.font='bold 12px sans-serif';
  ctx.textAlign='left'; ctx.textBaseline='middle';
  ctx.fillText('기대 '+exp, padL+4, Y(exp)-8);

  // y라벨
  ctx.fillStyle='#94a3b8';
  ctx.font='11px sans-serif';
  ctx.textAlign='right'; ctx.textBaseline='middle';
  [50,75,100].forEach(v=>{
    ctx.fillText(v+'', padL-4, Y(v));
  });

  // 시도 점들
  const T = trialHistory.length;
  if(T === 0){
    ctx.fillStyle='#64748b';
    ctx.font='12px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('아직 추출이 없어요', W/2, H/2);
    return;
  }
  const X = i => padL + (T===1 ? plotW/2 : (i/(T-1))*plotW);
  // 라인
  ctx.strokeStyle='rgba(56,189,248,.6)'; ctx.lineWidth=1.5;
  ctx.beginPath();
  trialHistory.forEach((v,i)=>{
    if(i===0) ctx.moveTo(X(i), Y(v));
    else ctx.lineTo(X(i), Y(v));
  });
  ctx.stroke();
  // 점
  trialHistory.forEach((v,i)=>{
    ctx.fillStyle = v >= exp-3 && v <= exp+3 ? '#86efac' : (v < exp-3 ? '#fca5a5' : '#7dd3fc');
    ctx.beginPath();
    ctx.arc(X(i), Y(v), 4, 0, Math.PI*2);
    ctx.fill();
  });
  $('totTrials').textContent = T;
  const avg = trialHistory.reduce((a,b)=>a+b,0)/T;
  $('avgCover').textContent = fmt(avg,1) + ' / 100';
}

/* =============== 표본평균 히스토그램 =============== */
function drawMeanHist(){
  const cv = $('meanHist');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=30, padR=18, padT=10, padB=24;
  const plotW=W-padL-padR, plotH=H-padT-padB;

  if(intervals.length === 0){
    ctx.fillStyle='#64748b';
    ctx.font='12px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('표본을 추출하면 표본평균 분포가 표시돼요', W/2, H/2);
    $('binInfo').textContent='';
    return;
  }
  const means = intervals.map(c=>c.mean);
  const lo = Math.min(...means), hi = Math.max(...means);
  const nbins = 18;
  const binW = (hi-lo)/nbins || 1;
  const bins = new Array(nbins).fill(0);
  means.forEach(v=>{
    let k=Math.floor((v-lo)/binW);
    if(k<0) k=0; if(k>=nbins) k=nbins-1;
    bins[k]++;
  });
  const cMax = Math.max(...bins);
  const X = i => padL + (i/nbins)*plotW;
  const Y = c => padT+plotH - (c/Math.max(1,cMax))*plotH*0.96;

  // 모평균 라인
  const ps = popStats(POPULATIONS[curKey].data);
  const Xv = v => padL + ((v-lo)/(hi-lo || 1))*plotW;
  ctx.strokeStyle='#fbbf24'; ctx.lineWidth=2;
  ctx.beginPath();
  ctx.moveTo(Xv(ps.mu), padT); ctx.lineTo(Xv(ps.mu), padT+plotH);
  ctx.stroke();
  ctx.fillStyle='#fde047';
  ctx.font='bold 11px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText('μ', Xv(ps.mu), padT-1);

  // 막대
  ctx.fillStyle='rgba(56,189,248,.6)';
  ctx.strokeStyle='rgba(56,189,248,.95)';
  for(let i=0;i<nbins;i++){
    const x = X(i);
    const y = Y(bins[i]);
    ctx.fillRect(x+1, y, plotW/nbins - 2, padT+plotH - y);
  }

  // 축
  ctx.strokeStyle='rgba(148,163,184,.5)';
  ctx.beginPath();
  ctx.moveTo(padL, padT+plotH); ctx.lineTo(W-padR, padT+plotH);
  ctx.stroke();
  ctx.fillStyle='#94a3b8';
  ctx.font='11px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  [0,0.5,1].forEach(t=>{
    const v = lo + t*(hi-lo);
    ctx.fillText(POPULATIONS[curKey].showInt ? Math.round(v)+'' : v.toFixed(1), padL+t*plotW, padT+plotH+5);
  });
  $('binInfo').textContent = 'n='+n+' 인 표본 100개의 X̄';
}

/* =============== UI 업데이트 =============== */
function updatePopInfo(){
  const ps = popStats(POPULATIONS[curKey].data);
  $('kN').textContent = ps.n;
  $('kMu').textContent = fmt(ps.mu,2);
  $('kSd').textContent = fmt(ps.sd,2);
  $('kUnit').textContent = POPULATIONS[curKey].unit;
}
function redraw(){
  shown = 100;
  drawCIMain();
  drawTrialChart();
  drawMeanHist();
  $('confDisp').textContent = Math.round(CL*100)+'%';
  $('expDisp').textContent = '약 '+Math.round(CL*100)+'개';
}

/* =============== 이벤트 =============== */
document.querySelectorAll('.preset').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.querySelectorAll('.preset').forEach(x=>x.classList.toggle('active', x===b));
    curKey = b.dataset.key;
    intervals = [];
    trialHistory = [];
    updatePopInfo();
    doDraw100();
  });
});
$('nRange').addEventListener('input', e=>{
  n = parseInt(e.target.value);
  $('nVal').textContent = n;
});
$('confRange').addEventListener('input', e=>{
  CL = parseInt(e.target.value)/100;
  $('confVal').textContent = Math.round(CL*100)+'%';
});
$('useSigma').addEventListener('change', e=>{
  useSigma = e.target.checked;
});
$('btnDraw').addEventListener('click', doDraw100);
$('btnReplay').addEventListener('click', startReplayAnim);
$('btnClear').addEventListener('click', ()=>{
  trialHistory = [];
  drawTrialChart();
});
window.addEventListener('resize', redraw);

/* =============== 초기화 =============== */
updatePopInfo();
doDraw100();
</script>
</body>
</html>
"""


def render():
    st.subheader("🌐 신뢰도의 의미 — 100개의 신뢰구간 실험실")
    st.caption(
        "표본 100세트를 뽑아 모평균의 신뢰구간을 100개 만들어 보고, "
        "그중 몇 개가 모평균 μ를 포함하는지 직접 세어 봅니다."
    )

    components.html(_HTML, height=2200, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
