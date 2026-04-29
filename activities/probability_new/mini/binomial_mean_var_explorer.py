import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "이항분포평균분산탐험"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 내용을 바탕으로 아래 질문에 답해보세요**"},
    {"key": "실생활예시",
     "label": "🌍 이 활동에서 나온 실생활 사례 중 하나를 골라, B(n, p)로 나타내고 평균·분산·표준편차를 직접 계산해보세요.",
     "type": "text_area", "height": 100},
    {"key": "np변화관찰",
     "label": "📊 n 또는 p를 바꿨을 때 분포 모양이 어떻게 달라졌나요? 평균과 표준편차의 변화와 함께 설명해보세요.",
     "type": "text_area", "height": 100},
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title": "미니: 이항분포 평균·분산 탐험",
    "description": "n, p를 조절하며 이항분포의 평균·분산·표준편차를 시각적으로 탐색하고 실생활 사례를 분석합니다.",
    "order": 62,
}

HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);min-height:100vh;padding:14px 12px 24px;color:#e2e8f0;font-size:15px}

/* ── 카드 ── */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:18px 22px;margin-bottom:14px;backdrop-filter:blur(10px)}
.card-title{font-size:17px;font-weight:700;color:#fbbf24;margin-bottom:14px;display:flex;align-items:center;gap:7px;letter-spacing:.02em}

/* ── 수식 박스 ── */
.formula-row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:16px}
.fbox{flex:1;min-width:150px;max-width:220px;background:rgba(0,0,0,.3);border-radius:14px;padding:14px 10px;text-align:center;border:1.5px solid rgba(255,255,255,.08);transition:all .4s}
.fbox.mean  {border-color:rgba(245,158,11,.5);background:rgba(245,158,11,.08)}
.fbox.var   {border-color:rgba(99,102,241,.5);background:rgba(99,102,241,.08)}
.fbox.sigma {border-color:rgba(16,185,129,.5);background:rgba(16,185,129,.08)}
.fbox .lbl  {font-size:13px;color:#94a3b8;font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin-bottom:4px}
.fbox .val  {font-size:31px;font-weight:900;margin-bottom:2px;transition:all .35s}
.fbox.mean  .val{color:#fbbf24}
.fbox.var   .val{color:#a5b4fc}
.fbox.sigma .val{color:#6ee7b7}
.fbox .formula{font-size:14px;color:#64748b;margin-top:2px}

/* ── 슬라이더 ── */
.slider-row{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
.slider-group{display:flex;flex-direction:column;gap:5px;flex:1;min-width:200px}
.slider-group label{font-size:14px;color:#94a3b8;font-weight:600;display:flex;justify-content:space-between;align-items:center}
.slider-group label span{background:linear-gradient(135deg,#fbbf24,#f97316);border-radius:8px;padding:2px 12px;font-weight:900;font-size:17px;color:#1c1917}
input[type=range]{-webkit-appearance:none;height:7px;border-radius:3px;outline:none;width:100%;cursor:pointer}
.range-n{background:linear-gradient(90deg,#f59e0b,#ef4444)}
.range-p{background:linear-gradient(90deg,#6366f1,#8b5cf6)}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#fff;border:3px solid #f59e0b;cursor:pointer;box-shadow:0 0 10px rgba(245,158,11,.5)}
.range-p::-webkit-slider-thumb{border-color:#8b5cf6;box-shadow:0 0 10px rgba(139,92,246,.5)}

/* ── 막대그래프 ── */
.chart-wrap{position:relative;height:200px;overflow:hidden;margin-top:8px}
.chart-wrap canvas{width:100%;height:200px;display:block}
.axis-label{font-size:12px;color:#64748b;text-align:center;margin-top:5px}

/* ── 통계 요약 칩 ── */
.stat-chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.chip{display:flex;flex-direction:column;align-items:center;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:10px 16px;flex:1;min-width:90px}
.chip .cv{font-size:22px;font-weight:800}
.chip .cl{font-size:12px;color:#64748b;font-weight:600;margin-top:3px;text-transform:uppercase;letter-spacing:.04em}

/* ── 시나리오 탭 ── */
.tabs{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px}
.tab-btn{padding:8px 17px;border-radius:10px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);cursor:pointer;font-size:14px;font-weight:600;color:#94a3b8;transition:all .2s}
.tab-btn:hover{background:rgba(255,255,255,.08)}
.tab-btn.active{background:rgba(245,158,11,.2);color:#fbbf24;border-color:rgba(245,158,11,.4)}

/* ── 시나리오 카드 ── */
.scenario-card{background:rgba(0,0,0,.25);border-radius:14px;padding:16px 18px;border:1px solid rgba(255,255,255,.07)}
.sc-header{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.sc-emoji-big{font-size:44px;line-height:1}
.sc-head-text{}
.sc-title{font-size:18px;font-weight:800;color:#f1f5f9;margin-bottom:3px}
.sc-base-desc{font-size:14px;color:#94a3b8;line-height:1.5}
.sc-slider-row{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0 8px}
.sc-slider-group{display:flex;flex-direction:column;gap:5px;flex:1;min-width:180px}
.sc-slider-group label{font-size:14px;color:#94a3b8;font-weight:600;display:flex;justify-content:space-between;align-items:center}
.sc-slider-group label span{background:linear-gradient(135deg,#fbbf24,#f97316);border-radius:7px;padding:1px 10px;font-weight:900;font-size:15px;color:#1c1917}
.sc-result{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:10px 0}
.sc-stat{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:9px 16px;text-align:center;flex:1;min-width:90px}
.sc-stat .sv{font-size:24px;font-weight:900}
.sc-stat .sl{font-size:12px;color:#64748b;margin-top:2px;font-weight:600}
.sc-stat.mean-s .sv{color:#fbbf24}
.sc-stat.var-s  .sv{color:#a5b4fc}
.sc-stat.sig-s  .sv{color:#6ee7b7}
.sc-chart-wrap{height:140px;overflow:hidden;margin:4px 0}
.sc-chart-wrap canvas{width:100%;height:140px;display:block}
.interp{background:rgba(255,255,255,.04);border-left:3px solid #fbbf24;border-radius:0 10px 10px 0;padding:11px 15px;font-size:15px;color:#e2e8f0;line-height:1.75;margin-top:10px}

/* ── 애니메이션 ── */
@keyframes popIn{0%{transform:scale(.7);opacity:0}60%{transform:scale(1.15)}100%{transform:scale(1);opacity:1}}
.pop{animation:popIn .4s ease forwards}

/* ── 시뮬레이션 버튼 ── */
.sim-btn{display:block;width:100%;padding:12px;border-radius:12px;border:none;background:linear-gradient(135deg,#f59e0b,#ef4444);color:#1c1917;font-size:17px;font-weight:800;cursor:pointer;margin-top:10px;transition:all .2s;letter-spacing:.02em}
.sim-btn:hover{filter:brightness(1.1);transform:translateY(-1px)}
.sim-btn:active{transform:translateY(0)}
.sim-result{margin-top:10px;font-size:15px;color:#94a3b8;text-align:center;min-height:22px;line-height:1.7}
.sim-balls{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;margin-top:8px;max-height:80px;overflow:hidden}
.ball{width:20px;height:20px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700}
.ball.hit{background:rgba(245,158,11,.8);color:#1c1917}
.ball.miss{background:rgba(100,116,139,.4);color:#94a3b8}

::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(245,158,11,.4);border-radius:3px}
</style>
</head>
<body>

<!-- ① 수식 카드 -->
<div class="card">
  <div class="card-title">📐 이항분포 B(n, p)의 평균·분산·표준편차</div>
  <div class="formula-row">
    <div class="fbox mean">
      <div class="lbl">E(X) = np</div>
      <div class="val" id="valMean">—</div>
      <div class="formula">평균 = n × p</div>
    </div>
    <div class="fbox var">
      <div class="lbl">V(X) = npq</div>
      <div class="val" id="valVar">—</div>
      <div class="formula">분산 = n × p × (1−p)</div>
    </div>
    <div class="fbox sigma">
      <div class="lbl">σ(X) = √npq</div>
      <div class="val" id="valSigma">—</div>
      <div class="formula">표준편차 = √분산</div>
    </div>
  </div>
  <div class="slider-row">
    <div class="slider-group">
      <label>시행 횟수 &nbsp;<strong>n</strong> = <span id="dispN">20</span></label>
      <input type="range" id="rangeN" class="range-n" min="5" max="60" value="20" step="1">
    </div>
    <div class="slider-group">
      <label>성공 확률 &nbsp;<strong>p</strong> = <span id="dispP">0.50</span></label>
      <input type="range" id="rangeP" class="range-p" min="5" max="95" value="50" step="5">
    </div>
  </div>
  <div class="chart-wrap" id="chartWrap"><canvas id="barchart"></canvas></div>
  <div class="axis-label">← X값 (성공 횟수) → &nbsp;|&nbsp; 노란 점선 = 평균(E(X)) &nbsp;|&nbsp; 초록 영역 = μ ± σ</div>
  <div class="stat-chips">
    <div class="chip"><div class="cv" id="chipMean" style="color:#fbbf24">—</div><div class="cl">평균 E(X)</div></div>
    <div class="chip"><div class="cv" id="chipVar"  style="color:#a5b4fc">—</div><div class="cl">분산 V(X)</div></div>
    <div class="chip"><div class="cv" id="chipSig"  style="color:#6ee7b7">—</div><div class="cl">표준편차 σ</div></div>
    <div class="chip"><div class="cv" id="chipQ"    style="color:#f472b6">—</div><div class="cl">q = 1−p</div></div>
  </div>
</div>

<!-- ② 시뮬레이션 -->
<div class="card">
  <div class="card-title">🎲 n번 시행 시뮬레이션</div>
  <button class="sim-btn" onclick="runSim()">▶ 지금 n번 시행해보기!</button>
  <div class="sim-result" id="simResult"></div>
  <div class="sim-balls" id="simBalls"></div>
</div>

<!-- ③ 실생활 시나리오 -->
<div class="card">
  <div class="card-title">🌍 실생활 속 이항분포</div>
  <div class="tabs" id="scenTabs"></div>
  <div id="scenPanels"></div>
</div>

<script>
// ── 공통 유틸 ────────────────────────────────────────
function comb(n, k) {
  if (k < 0 || k > n) return 0;
  if (k === 0 || k === n) return 1;
  let r = 1;
  for (let i = 0; i < Math.min(k, n - k); i++) r = r * (n - i) / (i + 1);
  return r;
}
function binomPMF(n, p, k) {
  return comb(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
}
function drawBinomChart(canvasEl, wrapEl, n, p, H) {
  const W = wrapEl.clientWidth || 500;
  canvasEl.width = W; canvasEl.height = H;
  const ctx = canvasEl.getContext('2d');
  ctx.clearRect(0, 0, W, H);
  const q = 1 - p, mean = n * p, sigma = Math.sqrt(n * p * q);
  const probs = Array.from({length: n + 1}, (_, k) => binomPMF(n, p, k));
  const maxP  = Math.max(...probs);
  const xMin  = Math.max(0, Math.floor(mean - 4 * sigma) - 1);
  const xMax  = Math.min(n, Math.ceil(mean + 4 * sigma) + 1);
  const cnt   = xMax - xMin + 1;
  const padL = 28, padR = 10, padT = 14, padB = 28;
  const plotW = W - padL - padR, plotH = H - padT - padB;
  const barW  = Math.max(1, plotW / cnt - 2);
  const xPos  = k => padL + (k - xMin + 0.5) * (plotW / cnt);
  // μ±σ 배경
  ctx.fillStyle = 'rgba(16,185,129,.08)';
  ctx.fillRect(xPos(mean - sigma), padT, xPos(mean + sigma) - xPos(mean - sigma), plotH);
  // 막대
  for (let k = xMin; k <= xMax; k++) {
    const bh = plotH * (probs[k] / maxP);
    const dist = Math.abs(k - mean) / sigma;
    const alpha = Math.max(0.4, 1 - dist * 0.18);
    ctx.fillStyle = (k >= mean - sigma && k <= mean + sigma)
      ? `rgba(99,102,241,${alpha})`
      : `rgba(99,102,241,${alpha * 0.55})`;
    ctx.beginPath();
    ctx.roundRect(xPos(k) - barW / 2, padT + plotH - bh, barW, bh, 3);
    ctx.fill();
  }
  // 평균 점선
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2.5;
  ctx.setLineDash([5, 3]);
  ctx.beginPath(); ctx.moveTo(xPos(mean), padT); ctx.lineTo(xPos(mean), padT + plotH); ctx.stroke();
  ctx.setLineDash([]);
  // x축 레이블
  ctx.fillStyle = '#64748b'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
  const step = cnt > 20 ? Math.ceil(cnt / 12) : 1;
  for (let k = xMin; k <= xMax; k += step) ctx.fillText(k, xPos(k), H - 6);
  // 평균 레이블
  ctx.fillStyle = '#fbbf24'; ctx.font = '11px sans-serif';
  ctx.fillText('μ=' + mean.toFixed(1), xPos(mean), padT - 2);
}
function animVal(id, txt) {
  const el = document.getElementById(id);
  el.textContent = txt;
  el.classList.remove('pop');
  void el.offsetWidth;
  el.classList.add('pop');
}

// ── ① 메인 탐색기 ────────────────────────────────────
let curN = 20, curP = 0.5;
document.getElementById('rangeN').addEventListener('input', e => { curN = +e.target.value; updateMain(); });
document.getElementById('rangeP').addEventListener('input', e => { curP = +e.target.value / 100; updateMain(); });
function updateMain() {
  const n = curN, p = curP, q = 1 - p;
  const mean = n * p, vari = n * p * q, sigma = Math.sqrt(vari);
  document.getElementById('dispN').textContent = n;
  document.getElementById('dispP').textContent = p.toFixed(2);
  animVal('valMean',  mean.toFixed(2));
  animVal('valVar',   vari.toFixed(2));
  animVal('valSigma', sigma.toFixed(2));
  document.getElementById('chipMean').textContent = mean.toFixed(2);
  document.getElementById('chipVar').textContent  = vari.toFixed(2);
  document.getElementById('chipSig').textContent  = sigma.toFixed(2);
  document.getElementById('chipQ').textContent    = q.toFixed(2);
  drawBinomChart(
    document.getElementById('barchart'),
    document.getElementById('chartWrap'), n, p, 200
  );
}

// ── ② 시뮬레이션 ─────────────────────────────────────
function runSim() {
  const n = curN, p = curP;
  let hits = 0;
  const outcomes = [];
  for (let i = 0; i < n; i++) { const ok = Math.random() < p; if (ok) hits++; outcomes.push(ok); }
  document.getElementById('simResult').innerHTML =
    `<strong style="color:#fbbf24;font-size:19px">${n}번 시행 → ${hits}번 성공!</strong><br>` +
    `(이론 평균 ${(n*p).toFixed(2)}, 표준편차 ${Math.sqrt(n*p*(1-p)).toFixed(2)})`;
  const bd = document.getElementById('simBalls');
  bd.innerHTML = '';
  outcomes.forEach(ok => {
    const b = document.createElement('span');
    b.className = 'ball ' + (ok ? 'hit' : 'miss');
    b.textContent = ok ? '✓' : '·';
    bd.appendChild(b);
  });
}

// ── ③ 실생활 시나리오 ─────────────────────────────────
const SCENARIOS = [
  {
    emoji: '🏀', title: '농구 자유투',
    baseDesc: '자유투 성공 여부를 베르누이 시행으로 분석합니다.',
    unit: '골', verb: '성공',
    nMin:5, nMax:30, nDefault:10, nStep:1,
    pMin:10, pMax:99, pDefault:70, pStep:5,
    nLabel: '던지는 횟수',  pLabel: '자유투 성공률'
  },
  {
    emoji: '📝', title: '객관식 찍기',
    baseDesc: '선택지 중 하나를 무작위로 찍을 때 정답 수를 분석합니다.',
    unit: '문제', verb: '정답',
    nMin:5, nMax:50, nDefault:20, nStep:1,
    pMin:10, pMax:90, pDefault:25, pStep:5,
    nLabel: '문제 수',  pLabel: '정답 확률 (선택지 수의 역수)'
  },
  {
    emoji: '🏭', title: '제품 불량률',
    baseDesc: '생산 제품 중 불량품 개수를 이항분포로 모델링합니다.',
    unit: '개', verb: '불량',
    nMin:50, nMax:500, nDefault:200, nStep:10,
    pMin:1, pMax:20, pDefault:3, pStep:1,
    nLabel: '검수 개수',  pLabel: '불량률 (%)'
  },
  {
    emoji: '🌧️', title: '비 오는 날',
    baseDesc: '일별 강수 여부를 베르누이 시행으로 봅니다.',
    unit: '일', verb: '강수',
    nMin:10, nMax:90, nDefault:30, nStep:1,
    pMin:5, pMax:95, pDefault:40, pStep:5,
    nLabel: '관측 기간 (일)',  pLabel: '일별 강수 확률'
  },
  {
    emoji: '🎯', title: '양궁 10점',
    baseDesc: '10점 과녁 명중 여부를 베르누이 시행으로 분석합니다.',
    unit: '발', verb: '10점',
    nMin:5, nMax:30, nDefault:15, nStep:1,
    pMin:10, pMax:99, pDefault:80, pStep:5,
    nLabel: '발사 횟수',  pLabel: '10점 명중률'
  },
];

// 각 시나리오의 현재 n, p 상태
const scState = SCENARIOS.map(s => ({
  n: s.nDefault,
  p: s.pDefault / 100
}));

function buildInterpText(sc, n, p) {
  const q = 1 - p, mean = n * p, sigma = Math.sqrt(n * p * q);
  const lo = Math.max(0, Math.round(mean - sigma));
  const hi = Math.min(n, Math.round(mean + sigma));
  return `<strong>B(${n}, ${p.toFixed(2)})</strong> 이항분포 기준 —
    평균 <b style="color:#fbbf24">${mean.toFixed(1)}${sc.unit}</b> ${sc.verb},
    표준편차 <b style="color:#6ee7b7">${sigma.toFixed(2)}</b>.
    대부분의 경우 <b style="color:#a5b4fc">${lo}~${hi}${sc.unit}</b> 범위에 분포해요.
    (분산 = ${(n*p*q).toFixed(2)})`;
}

function updateScen(idx) {
  const sc = SCENARIOS[idx];
  const nEl = document.getElementById(`scN_${idx}`);
  const pEl = document.getElementById(`scP_${idx}`);
  if (!nEl) return;
  const n = +document.getElementById(`scRangeN_${idx}`).value;
  const p = +document.getElementById(`scRangeP_${idx}`).value / 100;
  scState[idx] = {n, p};
  nEl.textContent = n;
  pEl.textContent = p.toFixed(2);
  const q = 1 - p, mean = n * p, vari = n * p * q, sigma = Math.sqrt(vari);
  animVal(`scMean_${idx}`, mean.toFixed(2));
  animVal(`scVar_${idx}`,  vari.toFixed(2));
  animVal(`scSig_${idx}`,  sigma.toFixed(2));
  document.getElementById(`scInterp_${idx}`).innerHTML = buildInterpText(sc, n, p);
  drawBinomChart(
    document.getElementById(`scCanvas_${idx}`),
    document.getElementById(`scChartWrap_${idx}`), n, p, 140
  );
}

function buildScenPanel(sc, idx) {
  const {n, p} = scState[idx];
  const q = 1 - p, mean = n * p, vari = n * p * q, sigma = Math.sqrt(vari);
  const div = document.createElement('div');
  div.id = `scenPanel_${idx}`;
  div.style.display = 'none';
  div.innerHTML = `
    <div class="scenario-card">
      <div class="sc-header">
        <span class="sc-emoji-big">${sc.emoji}</span>
        <div class="sc-head-text">
          <div class="sc-title">${sc.title}</div>
          <div class="sc-base-desc">${sc.baseDesc}</div>
        </div>
      </div>
      <div class="sc-slider-row">
        <div class="sc-slider-group">
          <label>${sc.nLabel} <strong>n</strong> = <span id="scN_${idx}">${n}</span></label>
          <input type="range" id="scRangeN_${idx}" class="range-n"
            min="${sc.nMin}" max="${sc.nMax}" value="${sc.nDefault}" step="${sc.nStep}"
            oninput="updateScen(${idx})">
        </div>
        <div class="sc-slider-group">
          <label>${sc.pLabel} <strong>p</strong> = <span id="scP_${idx}">${p.toFixed(2)}</span></label>
          <input type="range" id="scRangeP_${idx}" class="range-p"
            min="${sc.pMin}" max="${sc.pMax}" value="${sc.pDefault}" step="${sc.pStep}"
            oninput="updateScen(${idx})">
        </div>
      </div>
      <div class="sc-result">
        <div class="sc-stat mean-s"><div class="sv" id="scMean_${idx}">${mean.toFixed(2)}</div><div class="sl">평균 E(X) = np</div></div>
        <div class="sc-stat var-s" ><div class="sv" id="scVar_${idx}">${vari.toFixed(2)}</div><div class="sl">분산 V(X) = npq</div></div>
        <div class="sc-stat sig-s" ><div class="sv" id="scSig_${idx}">${sigma.toFixed(2)}</div><div class="sl">표준편차 σ(X)</div></div>
      </div>
      <div class="sc-chart-wrap" id="scChartWrap_${idx}"><canvas id="scCanvas_${idx}"></canvas></div>
      <div class="axis-label" style="margin-bottom:6px">← 성공 횟수 → &nbsp;|&nbsp; 노란 점선 = 평균 &nbsp;|&nbsp; 초록 영역 = μ ± σ</div>
      <div class="interp" id="scInterp_${idx}">${buildInterpText(sc, n, p)}</div>
    </div>`;
  return div;
}

let activeScen = 0;
function selectScen(idx) {
  document.querySelectorAll('#scenTabs .tab-btn').forEach((b, i) => {
    b.className = 'tab-btn' + (i === idx ? ' active' : '');
  });
  document.querySelectorAll('[id^="scenPanel_"]').forEach(el => el.style.display = 'none');
  const panel = document.getElementById(`scenPanel_${idx}`);
  panel.style.display = '';
  activeScen = idx;
  // 차트는 DOM이 보여야 그려짐
  setTimeout(() => drawBinomChart(
    document.getElementById(`scCanvas_${idx}`),
    document.getElementById(`scChartWrap_${idx}`),
    scState[idx].n, scState[idx].p, 140
  ), 20);
}

function initScenarios() {
  const tabsDiv    = document.getElementById('scenTabs');
  const panelsDiv  = document.getElementById('scenPanels');
  SCENARIOS.forEach((sc, i) => {
    const btn = document.createElement('button');
    btn.className = 'tab-btn' + (i === 0 ? ' active' : '');
    btn.textContent = sc.emoji + ' ' + sc.title;
    btn.onclick = () => selectScen(i);
    tabsDiv.appendChild(btn);
    panelsDiv.appendChild(buildScenPanel(sc, i));
  });
  selectScen(0);
}

// ── 초기화 ────────────────────────────────────────────
updateMain();
initScenarios();
window.addEventListener('resize', () => {
  drawBinomChart(document.getElementById('barchart'), document.getElementById('chartWrap'), curN, curP, 200);
  drawBinomChart(
    document.getElementById(`scCanvas_${activeScen}`),
    document.getElementById(`scChartWrap_${activeScen}`),
    scState[activeScen].n, scState[activeScen].p, 140
  );
});
</script>
</body>
</html>
"""

def render():
    st.header("📊 이항분포의 평균·분산·표준편차 탐험")

    components.html(HTML, height=1600, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
