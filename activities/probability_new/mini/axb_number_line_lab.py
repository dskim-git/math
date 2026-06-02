import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "aX+b수직선변환"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 aX+b 수직선 변환 활동 성찰**"},
    {"key": "b변화관찰",
     "label": "🔄 a=1로 두고 b만 바꿔 보았을 때, 수직선 위의 데이터·평균·분산은 각각 어떻게 변했나요? 그렇게 변한 이유를 점들 사이의 간격으로 설명해 보세요.",
     "type": "text_area", "height": 100},
    {"key": "a변화관찰",
     "label": "📏 b=0으로 두고 a를 바꿨을 때(특히 a를 키우거나 음수로 만들었을 때) 데이터 점들의 위치와 평균, 분산은 어떻게 달라졌나요?",
     "type": "text_area", "height": 100},
    {"key": "분산제곱이유",
     "label": "🤔 분산이 a²배가 되는 이유를, 수직선 위 점들 사이의 거리 변화를 이용해 자신의 말로 설명해 보세요.",
     "type": "text_area", "height": 100},
    {"key": "실생활변환",
     "label": "🌡️ 섭씨 ℃를 화씨 ℉로 바꾸는 식 ℉ = 1.8·℃ + 32 처럼, aX+b 변환을 활용하는 실생활 사례를 하나 떠올려 보고 a, b의 의미를 적어 보세요.",
     "type": "text_area", "height": 100},
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",          "type": "text_area", "height": 90},
]

META = {
    "title":       "📊 aX+b 수직선 변환 실험실",
    "description": "수직선 위 데이터의 변화로 aX+b의 평균·분산에 a, b가 미치는 영향을 시각적으로 탐험합니다.",
    "order":       53,
    "hidden":      True,
}

_HTML = r"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;
     background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);
     min-height:100vh;padding:14px 12px 20px;color:#e2e8f0;font-size:17px}

/* ── 헤더 ── */
.hero{text-align:center;background:linear-gradient(135deg,rgba(96,165,250,.14),rgba(192,132,252,.10));
      border:1px solid rgba(96,165,250,.30);border-radius:20px;padding:18px 16px;margin-bottom:14px}
.hero h1{font-size:28px;font-weight:900;background:linear-gradient(90deg,#60a5fa,#c084fc);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
         text-shadow:0 0 24px rgba(96,165,250,.30)}
.hero p{font-size:16px;color:#94a3b8;margin-top:6px;line-height:1.55}

/* ── 카드 ── */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.10);
      border-radius:18px;padding:16px 18px;margin:12px 0;backdrop-filter:blur(8px)}
.card-title{font-size:20px;font-weight:700;color:#fbbf24;margin-bottom:12px;
            display:flex;align-items:center;gap:8px}

/* ── 데이터 프리셋 ── */
.preset-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.preset-btn{background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.10);
            border-radius:14px;padding:12px 8px;cursor:pointer;text-align:center;
            transition:all .22s;color:#e2e8f0;user-select:none}
.preset-btn:hover{background:rgba(96,165,250,.10);border-color:rgba(96,165,250,.40);
                  transform:translateY(-2px)}
.preset-btn.active{background:rgba(96,165,250,.16);border-color:#60a5fa;
                   box-shadow:0 0 14px rgba(96,165,250,.30)}
.preset-icon{font-size:34px;margin-bottom:4px;line-height:1}
.preset-name{font-size:17px;font-weight:800;color:#93c5fd}
.preset-desc{font-size:14px;color:#94a3b8;margin-top:3px;line-height:1.4}
.preset-data{font-size:13px;color:#64748b;margin-top:6px;font-family:'Consolas',monospace;
             word-break:break-all;line-height:1.4}

/* ── 슬라이더 ── */
.slider-row{display:flex;align-items:center;gap:14px;margin:10px 0;flex-wrap:wrap}
.slider-lbl{font-size:24px;font-weight:800;color:#fbbf24;min-width:120px;
            font-family:'Times New Roman',serif;font-style:italic}
.slider-lbl small{font-size:14px;color:#94a3b8;font-style:normal;font-weight:600;
                  margin-left:5px;font-family:'Segoe UI',sans-serif}
input[type=range]{flex:1;min-width:180px;-webkit-appearance:none;height:9px;
                  border-radius:5px;outline:none;cursor:pointer}
input[type=range].a-range{background:linear-gradient(90deg,#ef4444,#f59e0b,#facc15,#22c55e,#3b82f6,#a855f7)}
input[type=range].b-range{background:linear-gradient(90deg,#0ea5e9,#94a3b8,#fbbf24)}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;
                                        border-radius:50%;background:#fff;border:3px solid #fbbf24;
                                        cursor:pointer;box-shadow:0 0 12px rgba(251,191,36,.50)}
input[type=range]::-moz-range-thumb{width:22px;height:22px;border-radius:50%;background:#fff;
                                    border:3px solid #fbbf24;cursor:pointer}
.slider-val{min-width:78px;background:linear-gradient(135deg,#fbbf24,#f97316);
            border-radius:10px;padding:5px 14px;font-weight:900;font-size:22px;
            text-align:center;color:#1c1917;font-family:'Consolas',monospace}
.quick-btns{display:flex;gap:6px;flex-wrap:wrap;margin-top:4px}
.qbtn{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);
      border-radius:8px;padding:6px 13px;cursor:pointer;color:#cbd5e1;
      font-size:14px;font-weight:700;transition:all .15s;font-family:'Consolas',monospace}
.qbtn:hover{background:rgba(251,191,36,.18);border-color:#fbbf24;color:#fbbf24}

/* ── SVG 시각화 ── */
.viz-wrap{position:relative;width:100%;background:rgba(0,0,0,.20);border-radius:12px;
          padding:8px 4px;border:1px solid rgba(255,255,255,.06)}
.viz-wrap svg{display:block;width:100%;height:auto}
.viz-legend{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;
            margin-top:8px;font-size:15px;color:#cbd5e1}
.viz-legend .ll{display:flex;align-items:center;gap:6px}
.viz-legend .dot{width:14px;height:14px;border-radius:50%;display:inline-block;
                 border:2px solid #fff}
.viz-legend .bar{display:inline-block;width:18px;height:4px;background:#fbbf24}
.viz-legend .band{display:inline-block;width:18px;height:14px;
                  background:rgba(251,191,36,.22);border:1px solid rgba(251,191,36,.6);
                  border-radius:3px}

/* ── 통계 비교 ── */
.stat-cmp{display:grid;grid-template-columns:1fr 50px 1fr;gap:10px;
          align-items:stretch;margin-top:6px}
.stat-col{background:rgba(255,255,255,.04);border:1.5px solid rgba(255,255,255,.10);
          border-radius:14px;padding:13px 12px}
.stat-col.X{border-color:rgba(96,165,250,.50);background:rgba(96,165,250,.10)}
.stat-col.Y{border-color:rgba(192,132,252,.50);background:rgba(192,132,252,.10)}
.stat-col h4{font-size:20px;font-weight:800;text-align:center;margin-bottom:10px;
             font-family:'Consolas',monospace}
.stat-col.X h4{color:#93c5fd}
.stat-col.Y h4{color:#d8b4fe;word-break:break-all}
.stat-line{display:flex;justify-content:space-between;align-items:center;
           padding:7px 4px;border-top:1px dashed rgba(255,255,255,.10);font-size:17px}
.stat-line:first-of-type{border-top:none}
.stat-line .key{color:#cbd5e1;font-weight:700;font-family:'Consolas',monospace}
.stat-line .val{color:#fbbf24;font-weight:900;font-size:21px;font-family:'Consolas',monospace;
                transition:color .25s}
.stat-line .val.flash{color:#fde68a;text-shadow:0 0 12px rgba(251,191,36,.7)}
.stat-arrow{display:flex;align-items:center;justify-content:center;font-size:36px;color:#fbbf24}

/* ── 공식 칩 ── */
.fml-row{display:flex;gap:9px;flex-wrap:wrap;margin-top:14px}
.fml-chip{flex:1;min-width:170px;background:rgba(251,191,36,.08);
          border:1px solid rgba(251,191,36,.28);border-radius:10px;
          padding:11px 8px;text-align:center;font-size:14px;color:#fde68a;line-height:1.55}
.fml-chip strong{display:block;font-size:18px;color:#fbbf24;
                 font-family:'Consolas',monospace;margin-bottom:4px;letter-spacing:.5px}

/* ── 관찰 가이드 ── */
.obs-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:4px}
.obs-card{background:rgba(255,255,255,.04);border-left:4px solid;border-radius:0 12px 12px 0;
          padding:12px 14px;display:flex;flex-direction:column;justify-content:space-between}
.obs-card.bb{border-color:#fbbf24}
.obs-card.aa{border-color:#a855f7}
.obs-card h5{font-size:17px;font-weight:800;margin-bottom:6px}
.obs-card.bb h5{color:#fbbf24}
.obs-card.aa h5{color:#c084fc}
.obs-card p{font-size:15px;color:#cbd5e1;line-height:1.65}
.obs-card p b{color:#fde68a}
.obs-card .try{display:inline-block;background:rgba(255,255,255,.06);border-radius:8px;
               padding:6px 12px;font-size:14px;color:#93c5fd;cursor:pointer;
               margin-top:8px;font-weight:700;border:1px solid rgba(255,255,255,.14);
               align-self:flex-start;transition:all .15s;font-family:'Consolas',monospace}
.obs-card .try:hover{background:rgba(96,165,250,.18);color:#dbeafe;border-color:#60a5fa}

/* ── 데이터 점/평균/시그마 애니메이션 ── */
.dpt{transition:cx .35s cubic-bezier(.4,.2,.2,1), cy .35s cubic-bezier(.4,.2,.2,1)}
.mline{transition:x1 .35s, x2 .35s}
.mbox{transition:x .35s}
.mtxt{transition:x .35s}
.sband{transition:x .35s, width .35s}
.cnx{transition:x1 .35s, x2 .35s}

@media (max-width:680px){
  .preset-grid{grid-template-columns:repeat(1,1fr)}
  .obs-grid{grid-template-columns:1fr}
  .stat-cmp{grid-template-columns:1fr;gap:6px}
  .stat-arrow{transform:rotate(90deg);font-size:28px}
}
</style>
</head>
<body>

<div class="hero">
  <h1>📊 aX + b 수직선 변환 실험실</h1>
  <p>슬라이더로 <b>a</b>(스케일)와 <b>b</b>(이동)를 바꾸며<br>수직선 위 데이터가 어떻게 움직이는지, 평균과 분산이 어떻게 달라지는지 직접 확인해 보세요</p>
</div>

<!-- ① 데이터 X 선택 -->
<div class="card">
  <div class="card-title">🎯 데이터 X 선택</div>
  <div class="preset-grid" id="presetGrid"></div>
</div>

<!-- ② a, b 슬라이더 -->
<div class="card">
  <div class="card-title">🎚️ 상수 <em>a</em>, <em>b</em> 조절하기</div>

  <div class="slider-row">
    <span class="slider-lbl">a <small>(스케일)</small> = <span id="aVal" class="slider-val">1</span></span>
    <input type="range" id="aSlider" class="a-range" min="-2" max="3" step="0.1" value="1" oninput="render()">
  </div>
  <div class="quick-btns">
    <button class="qbtn" onclick="setA(1)">a = 1</button>
    <button class="qbtn" onclick="setA(2)">a = 2</button>
    <button class="qbtn" onclick="setA(0.5)">a = 0.5</button>
    <button class="qbtn" onclick="setA(-1)">a = −1</button>
    <button class="qbtn" onclick="setA(-2)">a = −2</button>
  </div>

  <div class="slider-row" style="margin-top:14px">
    <span class="slider-lbl">b <small>(이동)</small> = <span id="bVal" class="slider-val">0</span></span>
    <input type="range" id="bSlider" class="b-range" min="-40" max="40" step="0.5" value="0" oninput="render()">
  </div>
  <div class="quick-btns">
    <button class="qbtn" onclick="setB(0)">b = 0</button>
    <button class="qbtn" onclick="setB(5)">b = 5</button>
    <button class="qbtn" onclick="setB(-5)">b = −5</button>
    <button class="qbtn" onclick="setB(10)">b = 10</button>
    <button class="qbtn" onclick="setB(20)">b = 20</button>
  </div>
</div>

<!-- ③ 수직선 시각화 -->
<div class="card">
  <div class="card-title">📍 수직선 위 데이터 변환</div>
  <div class="viz-wrap">
    <svg id="viz" viewBox="0 0 820 310" preserveAspectRatio="xMidYMid meet" style="display:block;width:100%"></svg>
  </div>
  <div class="viz-legend">
    <div class="ll"><span class="dot" style="background:#60a5fa"></span>X (원본)</div>
    <div class="ll"><span class="dot" style="background:#c084fc"></span>aX + b (변환)</div>
    <div class="ll"><span class="bar"></span>평균 E</div>
    <div class="ll"><span class="band"></span>±σ 구간</div>
  </div>
</div>

<!-- ④ 통계 비교 -->
<div class="card">
  <div class="card-title">🔢 평균 · 분산 · 표준편차 비교</div>
  <div class="stat-cmp">
    <div class="stat-col X">
      <h4>X (원본)</h4>
      <div class="stat-line"><span class="key">E(X)</span><span class="val" id="EX">—</span></div>
      <div class="stat-line"><span class="key">V(X)</span><span class="val" id="VX">—</span></div>
      <div class="stat-line"><span class="key">σ(X)</span><span class="val" id="SX">—</span></div>
    </div>
    <div class="stat-arrow">➡</div>
    <div class="stat-col Y">
      <h4 id="YTitle">aX + b</h4>
      <div class="stat-line"><span class="key" id="EYkey">E(aX+b)</span><span class="val" id="EY">—</span></div>
      <div class="stat-line"><span class="key" id="VYkey">V(aX+b)</span><span class="val" id="VY">—</span></div>
      <div class="stat-line"><span class="key" id="SYkey">σ(aX+b)</span><span class="val" id="SY">—</span></div>
    </div>
  </div>
  <div class="fml-row">
    <div class="fml-chip"><strong>E(aX+b) = a·E(X) + b</strong>평균은 a배 한 뒤 b만큼 이동</div>
    <div class="fml-chip"><strong>V(aX+b) = a²·V(X)</strong>분산은 a²배 (b의 영향 없음!)</div>
    <div class="fml-chip"><strong>σ(aX+b) = |a|·σ(X)</strong>표준편차는 |a|배 (b의 영향 없음!)</div>
  </div>
</div>

<!-- ⑤ 직접 확인해 보세요 -->
<div class="card">
  <div class="card-title">🔍 직접 확인해 보세요</div>
  <div class="obs-grid">
    <div class="obs-card bb">
      <div>
        <h5>① b만 바꾸면?</h5>
        <p>a=1로 두고 b를 움직여 보세요. 데이터가 통째로 옆으로 이동하지만 점 사이의 <b>간격은 그대로</b> → 분산 변화 없음!</p>
      </div>
      <span class="try" onclick="setA(1);setB(15)">▶ a=1, b=15 적용</span>
    </div>
    <div class="obs-card aa">
      <div>
        <h5>② a만 바꾸면?</h5>
        <p>b=0으로 두고 a를 키워 보세요. 점들이 <b>원점 기준으로 퍼지거나 모입니다</b> → 분산이 a²배로 변화!</p>
      </div>
      <span class="try" onclick="setA(2);setB(0)">▶ a=2, b=0 적용</span>
    </div>
    <div class="obs-card aa">
      <div>
        <h5>③ a가 음수면?</h5>
        <p>a=−1로 해 보세요. 데이터가 <b>좌우로 뒤집힙니다</b>. 하지만 분산은 (−1)²=1배라 그대로!</p>
      </div>
      <span class="try" onclick="setA(-1);setB(0)">▶ a=−1, b=0 적용</span>
    </div>
    <div class="obs-card bb">
      <h5>🌡️ 챌린지: ℃를 ℉로!</h5>
      <p>"섭씨 온도" 데이터를 골라 ℉ = 1.8·℃ + 32 를 적용해 보세요. 평균과 표준편차가 어떻게 바뀌나요?</p>
      <span class="try" onclick="selectPreset(2);setA(1.8);setB(32)">▶ 화씨 변환 적용</span>
    </div>
  </div>
</div>

<script>
/* ── 데이터 프리셋 ───────────────────────────────────────── */
const PRESETS = [
  {
    icon:"📝", name:"시험 점수", desc:"7명의 원점수",
    values:[60, 65, 70, 75, 80, 85, 90], unit:"점"
  },
  {
    icon:"📏", name:"평균 키 편차", desc:"평균에서의 차이",
    values:[-8, -5, -2, 0, 3, 6, 10], unit:"cm"
  },
  {
    icon:"🌡️", name:"섭씨 온도", desc:"하루 7시각의 기온",
    values:[0, 5, 10, 15, 20, 25, 30], unit:"℃"
  }
];

let curPreset = 0;

/* ── 유틸 ─────────────────────────────────────────────── */
function r3(x){ return Math.round(x*1000)/1000; }
function fmt(x){
  const v = r3(x);
  if(Math.abs(v) < 1e-9) return '0';
  if(Number.isInteger(v)) return v.toString();
  return parseFloat(v.toFixed(3)).toString();
}
function calcStats(arr){
  const n = arr.length;
  const m = arr.reduce((s,x)=>s+x, 0) / n;
  const v = arr.reduce((s,x)=>s+(x-m)*(x-m), 0) / n;
  const s = Math.sqrt(Math.max(v, 0));
  return {m, v, s};
}

/* ── 프리셋 카드 빌드 ───────────────────────────────────── */
function buildPresets(){
  const g = document.getElementById('presetGrid');
  g.innerHTML = PRESETS.map((p, i) => `
    <div class="preset-btn ${i===curPreset?'active':''}" onclick="selectPreset(${i})">
      <div class="preset-icon">${p.icon}</div>
      <div class="preset-name">${p.name}</div>
      <div class="preset-desc">${p.desc}</div>
      <div class="preset-data">[${p.values.join(', ')}] ${p.unit}</div>
    </div>
  `).join('');
}
function selectPreset(i){
  curPreset = i;
  buildPresets();
  render();
}

/* ── 슬라이더 빠른 설정 ────────────────────────────────── */
function setA(v){
  const sl = document.getElementById('aSlider');
  sl.value = v;
  render();
}
function setB(v){
  const sl = document.getElementById('bSlider');
  sl.value = v;
  render();
}

/* ── 메인 렌더 ─────────────────────────────────────────── */
function flashVals(){
  ['EY','VY','SY'].forEach(id => {
    const el = document.getElementById(id);
    el.classList.add('flash');
    setTimeout(() => el.classList.remove('flash'), 280);
  });
}

let lastA = null, lastB = null;

function render(){
  const a = parseFloat(document.getElementById('aSlider').value);
  const b = parseFloat(document.getElementById('bSlider').value);
  document.getElementById('aVal').textContent = fmt(a);
  document.getElementById('bVal').textContent = fmt(b);

  const X = PRESETS[curPreset].values.slice();
  const Y = X.map(x => a * x + b);

  /* 통계 */
  const sx = calcStats(X);
  const sy = calcStats(Y);
  document.getElementById('EX').textContent = fmt(sx.m);
  document.getElementById('VX').textContent = fmt(sx.v);
  document.getElementById('SX').textContent = fmt(sx.s);
  document.getElementById('EY').textContent = fmt(sy.m);
  document.getElementById('VY').textContent = fmt(sy.v);
  document.getElementById('SY').textContent = fmt(sy.s);

  /* Y 타이틀 표시 */
  const aDisp = (a === 1) ? 'X' : ((a === -1) ? '−X' : (a < 0 ? '('+fmt(a)+')X' : fmt(a)+'X'));
  const bDisp = (b === 0) ? '' : (b > 0 ? ' + ' + fmt(b) : ' − ' + fmt(-b));
  const yTitle = aDisp + bDisp || 'X';
  document.getElementById('YTitle').textContent = yTitle;
  document.getElementById('EYkey').textContent = 'E(' + yTitle + ')';
  document.getElementById('VYkey').textContent = 'V(' + yTitle + ')';
  document.getElementById('SYkey').textContent = 'σ(' + yTitle + ')';

  /* 값이 실제로 바뀌었을 때만 깜빡 효과 */
  if(lastA !== a || lastB !== b){
    flashVals();
    lastA = a; lastB = b;
  }

  drawViz(X, Y, sx, sy, a, b);
}

/* ── SVG 시각화 ────────────────────────────────────────── */
function drawViz(X, Y, sx, sy, a, b){
  const svg = document.getElementById('viz');
  const W = 820, H = 310;
  const padX = 14;
  const yX = 80;       // 위쪽 수직선 (X)
  const yY = 248;      // 아래쪽 수직선 (aX+b)

  /* 공유 스케일 (X와 Y 모두 한 화면에 보이도록) */
  const candidates = X.concat(Y, [sx.m - sx.s, sx.m + sx.s, sy.m - sy.s, sy.m + sy.s]);
  let lo = Math.min.apply(null, candidates);
  let hi = Math.max.apply(null, candidates);
  let range = hi - lo;
  if(range < 1e-6){
    lo -= 1; hi += 1; range = 2;
  }
  lo -= range * 0.10;
  hi += range * 0.10;

  function px(v){ return padX + (v - lo) / (hi - lo) * (W - 2*padX); }

  /* 깔끔한 눈금 생성 */
  function niceTicks(lo, hi, count){
    const span = hi - lo;
    const step0 = span / count;
    const mag = Math.pow(10, Math.floor(Math.log10(step0)));
    const norms = [1, 2, 2.5, 5, 10];
    let step = mag * 10;
    for(const n of norms){ if(n * mag >= step0){ step = n * mag; break; } }
    const first = Math.ceil(lo / step) * step;
    const out = [];
    for(let v = first; v <= hi + step*0.001; v += step){
      out.push(Math.round(v/step) * step);
    }
    return out;
  }
  const ticks = niceTicks(lo, hi, 9);

  /* 부품 SVG 문자열 */
  function tickLines(yLine){
    return ticks.map(t => {
      const x = px(t);
      const lbl = (Math.abs(t) < 1e-9) ? '0'
                 : (Number.isInteger(t) ? t : parseFloat(t.toFixed(2)).toString());
      return `<g>
        <line x1="${x}" y1="${yLine-6}" x2="${x}" y2="${yLine+6}" stroke="#64748b" stroke-width="1.2"/>
        <text x="${x}" y="${yLine+26}" text-anchor="middle" fill="#cbd5e1" font-size="18"
              font-weight="700" font-family="Consolas,monospace">${lbl}</text>
      </g>`;
    }).join('');
  }

  function sigmaBand(yLine, mean, sigma){
    const x1 = px(mean - sigma), x2 = px(mean + sigma);
    return `<rect class="sband" x="${x1}" y="${yLine-22}" width="${Math.max(x2-x1, 0)}" height="44"
                  rx="5" fill="#fbbf24" fill-opacity="0.18"
                  stroke="#fbbf24" stroke-opacity="0.45" stroke-width="1"/>`;
  }

  function meanMarker(yLine, mean, label){
    const x = px(mean);
    const lblW = Math.max(110, 11 * label.length + 18);
    /* 라벨 박스가 화면 밖으로 나가지 않게 클램프 */
    let bx = x - lblW/2;
    if(bx < 2) bx = 2;
    if(bx + lblW > W - 2) bx = W - 2 - lblW;
    return `
      <line class="mline" x1="${x}" y1="${yLine-28}" x2="${x}" y2="${yLine+28}"
            stroke="#fbbf24" stroke-width="3" stroke-dasharray="5 4"/>
      <rect class="mbox" x="${bx}" y="${yLine-58}" width="${lblW}" height="28" rx="6"
            fill="#fbbf24"/>
      <text class="mtxt" x="${bx + lblW/2}" y="${yLine-38}" text-anchor="middle" fill="#1c1917"
            font-size="19" font-weight="900" font-family="Consolas,monospace">${label}</text>
    `;
  }

  function dataPoints(yLine, arr, color){
    const pxs = arr.map(v => px(v));
    return pxs.map((cx, i) => {
      /* 가까이 있는 점들이 겹치지 않도록 위로 살짝 분산 */
      let stack = 0;
      for(let j = 0; j < i; j++){
        if(Math.abs(pxs[j] - cx) < 11) stack++;
      }
      const cy = yLine - stack * 12;
      return `<circle class="dpt" cx="${cx}" cy="${cy}" r="7"
                      fill="${color}" stroke="#fff" stroke-width="1.5"/>`;
    }).join('');
  }

  /* X → aX+b 대응 화살표 (각 점을 점선으로 연결) */
  function connectionLines(X, Y){
    return X.map((x, i) => {
      const x1 = px(x), x2 = px(Y[i]);
      const same = Math.abs(x1 - x2) < 0.5;
      return `<line class="cnx" x1="${x1}" y1="${yX+14}" x2="${x2}" y2="${yY-14}"
                    stroke="${same?'#475569':'#fbbf24'}" stroke-width="1"
                    stroke-dasharray="3 4" opacity="${same?0.25:0.45}"/>`;
    }).join('');
  }

  /* 0 표시선 (원점 강조) */
  function zeroLine(yLine){
    if(lo > 0 || hi < 0) return '';
    const x = px(0);
    return `<line x1="${x}" y1="${yLine-26}" x2="${x}" y2="${yLine+26}"
                  stroke="#475569" stroke-width="1" stroke-dasharray="2 3" opacity="0.5"/>`;
  }

  /* 수직선 본체 */
  function axisLine(yLine){
    return `<line x1="${padX-5}" y1="${yLine}" x2="${W-padX+5}" y2="${yLine}"
                  stroke="#cbd5e1" stroke-width="2"/>
            <polygon points="${W-padX+5},${yLine} ${W-padX-4},${yLine-5} ${W-padX-4},${yLine+5}"
                     fill="#cbd5e1"/>`;
  }

  /* X / Y 축 라벨 (axis line 시작점 위쪽에 배치 — viewBox 안에 안전하게 들어가도록 start 정렬) */
  const xLab = `<text x="${padX + 4}" y="${yX - 12}" text-anchor="start" fill="#93c5fd"
                      font-size="24" font-weight="900" font-family="Times New Roman,serif" font-style="italic">X</text>`;
  const yLab = `<text x="${padX + 4}" y="${yY - 12}" text-anchor="start" fill="#d8b4fe"
                      font-size="24" font-weight="900" font-family="Times New Roman,serif" font-style="italic">Y</text>`;

  /* 변환식 표시 */
  const aStr = (a >= 0) ? fmt(a) : '('+fmt(a)+')';
  const bStrSign = (b >= 0) ? ' + ' + fmt(b) : ' − ' + fmt(-b);
  const eqStr = `Y = ${aStr} · X${bStrSign}`;

  svg.innerHTML = `
    ${connectionLines(X, Y)}

    <!-- 위 수직선: X -->
    ${sigmaBand(yX, sx.m, sx.s)}
    ${zeroLine(yX)}
    ${axisLine(yX)}
    ${tickLines(yX)}
    ${dataPoints(yX, X, '#60a5fa')}
    ${meanMarker(yX, sx.m, 'E(X)=' + fmt(sx.m))}
    ${xLab}
    <text x="${W - padX - 4}" y="${yX - 12}" text-anchor="end" fill="#fbbf24"
          font-size="18" font-weight="800" font-family="Consolas,monospace">
      σ(X) = ${fmt(sx.s)}
    </text>

    <!-- 변환식 -->
    <rect x="${W/2 - 170}" y="${(yX+yY)/2 - 22}" width="340" height="44" rx="11"
          fill="rgba(168,85,247,.18)" stroke="rgba(168,85,247,.55)" stroke-width="1.5"/>
    <text x="${W/2}" y="${(yX+yY)/2 + 9}" text-anchor="middle" fill="#f3e8ff"
          font-size="24" font-weight="800" font-family="Consolas,monospace">${eqStr}</text>

    <!-- 아래 수직선: aX+b -->
    ${sigmaBand(yY, sy.m, sy.s)}
    ${zeroLine(yY)}
    ${axisLine(yY)}
    ${tickLines(yY)}
    ${dataPoints(yY, Y, '#c084fc')}
    ${meanMarker(yY, sy.m, 'E(Y)=' + fmt(sy.m))}
    ${yLab}
    <text x="${W - padX - 4}" y="${yY - 12}" text-anchor="end" fill="#fbbf24"
          font-size="18" font-weight="800" font-family="Consolas,monospace">
      σ(Y) = ${fmt(sy.s)}  =  |${fmt(a)}| · σ(X)
    </text>
  `;
}

/* ── 초기화 ────────────────────────────────────────────── */
buildPresets();
window.addEventListener('load', render);
</script>
</body>
</html>
"""


def render():
    st.header("📊 aX + b 수직선 변환 실험실")
    components.html(_HTML, height=2180, scrolling=False)

    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
