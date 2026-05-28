# activities/common/mini/perm_comb_growth_race.py
"""
순열 vs 조합 r 증가 레이스
같은 n에서 r을 0→n으로 늘리며 ₙPᵣ과 ₙCᵣ가 어떻게 달라지는지 시각적으로 비교하는 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title":       "🏁 순열 vs 조합 — r 증가 레이스",
    "description": "n을 고정하고 r을 0→n으로 늘리며 순열은 끝없이 증가(증가 비율은 감소), 조합은 증가하다 감소하는 패턴을 시각적으로 비교합니다.",
    "order":       328,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>순열 vs 조합 r 증가 레이스</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(145deg,#0a0e1f,#0e1633,#080b1c);
  color:#e8eeff;padding:16px 18px 28px;min-height:100vh;
}

/* HEADER */
.hdr{text-align:center;margin-bottom:18px}
.hdr h1{font-size:1.75rem;font-weight:900;
  background:linear-gradient(90deg,#60a5fa,#a78bfa,#fbbf24);
  -webkit-background-clip:text;background-clip:text;color:transparent;
  margin-bottom:8px;letter-spacing:-.3px}
.hdr-sub{font-size:1.05rem;color:#a3b3d0;margin-bottom:12px}
.formula-banner{display:inline-flex;gap:14px;flex-wrap:wrap;justify-content:center}
.fb-pill{padding:10px 20px;border-radius:26px;font-family:'Courier New',monospace;
  font-size:1.1rem;font-weight:700;letter-spacing:.3px;line-height:1.3}
.fb-pill.perm{background:rgba(96,165,250,.13);border:1.8px solid rgba(96,165,250,.5);color:#bfdbfe}
.fb-pill.comb{background:rgba(251,191,36,.13);border:1.8px solid rgba(251,191,36,.5);color:#fde68a}

/* CONTROL */
.ctrl{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:16px;padding:14px 18px;margin-bottom:14px;
  box-shadow:0 6px 18px rgba(0,0,0,.2)}
.ctrl-grid{display:grid;grid-template-columns:1fr 1fr auto;gap:18px;align-items:center}
@media (max-width:820px){.ctrl-grid{grid-template-columns:1fr}}
.ctrl-cell{display:flex;align-items:center;gap:12px}
.lbl-big{font-size:1.18rem;font-weight:800;color:#cbd5e1;white-space:nowrap;
  font-family:'Courier New',monospace}
.val-big{padding:6px 18px;border-radius:11px;font-size:1.55rem;font-weight:900;
  font-family:'Courier New',monospace;min-width:62px;text-align:center;
  box-shadow:0 0 16px rgba(255,255,255,.04)}
.val-n{background:rgba(34,197,94,.18);border:2px solid rgba(34,197,94,.55);color:#86efac;
  text-shadow:0 0 8px rgba(134,239,172,.4)}
.val-r{background:rgba(244,114,182,.18);border:2px solid rgba(244,114,182,.55);color:#f9a8d4;
  text-shadow:0 0 8px rgba(249,168,212,.4)}
input[type=range]{flex:1;min-width:120px;height:8px;accent-color:#34d399}
input[type=range].rs{accent-color:#ec4899}
.btn-set{display:flex;gap:8px;flex-wrap:wrap}
.btn{padding:10px 18px;border-radius:12px;border:2px solid rgba(255,255,255,.18);
  background:rgba(255,255,255,.06);color:#e8eeff;font-family:inherit;
  font-size:1.02rem;font-weight:700;cursor:pointer;transition:all .15s;
  display:inline-flex;align-items:center;gap:6px}
.btn:hover{background:rgba(255,255,255,.14);transform:translateY(-1px)}
.btn:active{transform:translateY(0)}
.btn.play{background:linear-gradient(135deg,#10b981,#059669);border-color:transparent;color:#fff;
  box-shadow:0 4px 14px rgba(16,185,129,.35)}
.btn.play:hover{filter:brightness(1.1)}
.btn.stop{background:linear-gradient(135deg,#dc2626,#b91c1c);border-color:transparent;color:#fff;
  box-shadow:0 4px 14px rgba(220,38,38,.35)}
.btn.reset{background:rgba(167,139,250,.12);border-color:rgba(167,139,250,.45);color:#c4b5fd}

/* CHART CARDS */
.chart-card{background:rgba(255,255,255,.03);border-radius:18px;padding:14px 14px 10px;
  border:1.5px solid rgba(255,255,255,.08);margin-bottom:14px;overflow:hidden}
.chart-card.perm{border-color:rgba(96,165,250,.32);
  background:linear-gradient(180deg,rgba(96,165,250,.06),rgba(255,255,255,.02))}
.chart-card.comb{border-color:rgba(251,191,36,.32);
  background:linear-gradient(180deg,rgba(251,191,36,.06),rgba(255,255,255,.02))}
.chart-head{display:flex;align-items:center;justify-content:space-between;
  margin-bottom:10px;flex-wrap:wrap;gap:10px}
.chart-title{font-size:1.25rem;font-weight:900;display:flex;align-items:center;gap:8px;
  text-shadow:0 0 10px rgba(255,255,255,.08)}
.chart-card.perm .chart-title{color:#93c5fd}
.chart-card.comb .chart-title{color:#fcd34d}
.chart-formula{font-family:'Courier New',monospace;font-size:.96rem;
  padding:5px 14px;border-radius:10px;font-weight:700}
.chart-card.perm .chart-formula{background:rgba(96,165,250,.13);color:#dbeafe;
  border:1px solid rgba(96,165,250,.35)}
.chart-card.comb .chart-formula{background:rgba(251,191,36,.13);color:#fef3c7;
  border:1px solid rgba(251,191,36,.35)}
.chart-svg-wrap{width:100%;overflow-x:auto;display:flex;justify-content:center}
.chart-svg-wrap::-webkit-scrollbar{height:8px}
.chart-svg-wrap::-webkit-scrollbar-thumb{background:rgba(255,255,255,.15);border-radius:4px}
svg.chart{display:block;width:92%;height:auto;min-width:560px;max-width:700px;margin:0 auto}

/* COMPARISON */
.cmp-panel{background:rgba(255,255,255,.03);border:1.5px solid rgba(255,255,255,.1);
  border-radius:16px;padding:14px 16px;margin-bottom:14px}
.cmp-title{font-size:1.12rem;font-weight:800;color:#e8eeff;margin-bottom:10px;
  display:flex;align-items:center;gap:8px}
.cmp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:12px}
@media (max-width:640px){.cmp-grid{grid-template-columns:1fr}}
.cmp-cell{padding:13px;border-radius:13px;text-align:center;transition:all .25s}
.cmp-cell.perm{background:rgba(96,165,250,.09);border:1.8px solid rgba(96,165,250,.36)}
.cmp-cell.comb{background:rgba(251,191,36,.09);border:1.8px solid rgba(251,191,36,.36)}
.cmp-cell.ratio{background:rgba(167,139,250,.09);border:1.8px solid rgba(167,139,250,.36)}
.cc-lbl{font-size:1rem;color:#cbd5e1;margin-bottom:6px;font-weight:700;
  font-family:'Courier New',monospace}
.cc-val{font-size:1.85rem;font-weight:900;font-family:'Courier New',monospace;line-height:1.1;
  text-shadow:0 0 12px currentColor}
.cmp-cell.perm .cc-val{color:#60a5fa}
.cmp-cell.comb .cc-val{color:#fbbf24}
.cmp-cell.ratio .cc-val{color:#a78bfa}
.cc-formula{font-size:.92rem;color:#94a3b8;margin-top:6px;
  font-family:'Courier New',monospace;word-break:break-all;line-height:1.4}
.cmp-relation{background:linear-gradient(90deg,rgba(96,165,250,.08),rgba(167,139,250,.12),rgba(251,191,36,.08));
  border:1.2px dashed rgba(167,139,250,.5);border-radius:12px;padding:12px 14px;
  text-align:center;font-size:1.15rem;font-family:'Courier New',monospace;
  font-weight:800;line-height:1.6}
.cmp-relation .hp{color:#60a5fa;text-shadow:0 0 8px rgba(96,165,250,.4)}
.cmp-relation .hr{color:#f9a8d4;text-shadow:0 0 8px rgba(249,168,212,.4)}
.cmp-relation .hc{color:#fbbf24;text-shadow:0 0 8px rgba(251,191,36,.4)}

/* INSIGHTS */
.insights{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:820px){.insights{grid-template-columns:1fr}}
.ins{background:rgba(255,255,255,.03);border-radius:14px;padding:14px 16px;
  font-size:1.02rem;line-height:1.85;border-left:5px solid;font-weight:500}
.ins.perm{border-left-color:#60a5fa;background:linear-gradient(90deg,rgba(96,165,250,.07),rgba(255,255,255,.02))}
.ins.comb{border-left-color:#fbbf24;background:linear-gradient(90deg,rgba(251,191,36,.07),rgba(255,255,255,.02))}
.ins h3{font-size:1.15rem;font-weight:900;margin-bottom:8px;display:flex;align-items:center;gap:6px}
.ins.perm h3{color:#93c5fd}
.ins.comb h3{color:#fcd34d}
.ins .em{font-weight:900;color:#fff}
.ins .num{font-family:'Courier New',monospace;font-weight:800;color:#fff;
  background:rgba(255,255,255,.13);padding:2px 9px;border-radius:6px;font-size:.98rem;
  letter-spacing:.5px}

.pulse-r{animation:pulseR 0.45s ease}
@keyframes pulseR{
  0%{transform:scale(1)}50%{transform:scale(1.18)}100%{transform:scale(1)}
}
</style>
</head>
<body>

<div class="hdr">
  <h1>🏁 순열 vs 조합 — r 증가 레이스</h1>
  <div class="hdr-sub">같은 n에서 <b>r이 0 → n으로 커질 때</b> 두 값은 어떻게 달라질까?</div>
  <div class="formula-banner">
    <span class="fb-pill perm">ₙPᵣ = n × (n−1) × ⋯ × (n−r+1)</span>
    <span class="fb-pill comb">ₙCᵣ = ₙPᵣ ÷ r!</span>
  </div>
</div>

<div class="ctrl">
  <div class="ctrl-grid">
    <div class="ctrl-cell">
      <span class="lbl-big">n =</span>
      <input type="range" id="nSlider" min="3" max="10" value="6">
      <span class="val-big val-n" id="nVal">6</span>
    </div>
    <div class="ctrl-cell">
      <span class="lbl-big">r =</span>
      <input type="range" id="rSlider" class="rs" min="0" max="6" value="3">
      <span class="val-big val-r" id="rVal">3</span>
    </div>
    <div class="btn-set">
      <button class="btn play" id="playBtn">▶ r 자동 재생</button>
      <button class="btn reset" id="resetBtn">↻ 초기화</button>
    </div>
  </div>
</div>

<!-- PERMUTATION CHART -->
<div class="chart-card perm">
  <div class="chart-head">
    <div class="chart-title">🔵 순열 ₙPᵣ</div>
    <div class="chart-formula">r ↑ ⇒ 값 계속 ↑ &nbsp;|&nbsp; 곱하는 수는 ×n → ×1 로 ↓</div>
  </div>
  <div class="chart-svg-wrap"><svg class="chart" id="pChart"></svg></div>
</div>

<!-- COMBINATION CHART -->
<div class="chart-card comb">
  <div class="chart-head">
    <div class="chart-title">🟡 조합 ₙCᵣ</div>
    <div class="chart-formula">r ↑ ⇒ 증가 → 최댓값 → 감소 &nbsp;|&nbsp; 좌우 대칭 (산 모양!)</div>
  </div>
  <div class="chart-svg-wrap"><svg class="chart" id="cChart"></svg></div>
</div>

<!-- COMPARISON PANEL -->
<div class="cmp-panel">
  <div class="cmp-title">📍 지금 선택한 r 에서</div>
  <div class="cmp-grid">
    <div class="cmp-cell perm">
      <div class="cc-lbl"><span id="pLbl">₆P₃</span></div>
      <div class="cc-val" id="pVal">120</div>
      <div class="cc-formula" id="pFormula">6 × 5 × 4</div>
    </div>
    <div class="cmp-cell comb">
      <div class="cc-lbl"><span id="cLbl">₆C₃</span></div>
      <div class="cc-val" id="cVal">20</div>
      <div class="cc-formula" id="cFormula">120 ÷ 3!</div>
    </div>
    <div class="cmp-cell ratio">
      <div class="cc-lbl">ₙPᵣ ÷ ₙCᵣ = r!</div>
      <div class="cc-val" id="ratioVal">6</div>
      <div class="cc-formula" id="ratioFormula">= 3!</div>
    </div>
  </div>
  <div class="cmp-relation" id="cmpRel">
    <span class="hp">₆P₃</span> = <span class="hr">3!</span> × <span class="hc">₆C₃</span>
    &nbsp;⟶&nbsp;
    <span class="hp">120</span> = <span class="hr">6</span> × <span class="hc">20</span> ✓
  </div>
</div>

<!-- INSIGHTS -->
<div class="insights">
  <div class="ins perm">
    <h3>🔵 순열의 패턴</h3>
    매번 곱하는 수: <span class="num" id="pMulList">×6 ×5 ×4</span><br>
    → <span class="em">점점 작은 수</span>를 곱하므로<br>
    값은 커지지만 <span class="em">증가하는 비율은 점점 ↓</span>
  </div>
  <div class="ins comb">
    <h3>🟡 조합의 패턴</h3>
    이전 항과 비율: <span class="num" id="cMulNow">×6/1 = 6.00</span><br>
    → <span class="em">비율 &gt; 1</span> 이면 증가,<br>
    <span class="em">비율 &lt; 1</span> 이면 감소 (보통 r &gt; n/2)
  </div>
</div>

<script>
// ─── UTILS ────────────────────────────────────────────────
function fact(n){ let v=1; for(let i=2;i<=n;i++) v*=i; return v; }
function perm(n,r){ if(r<0||r>n) return 0; let v=1; for(let i=0;i<r;i++) v*=(n-i); return v; }
function comb(n,r){ if(r<0||r>n) return 0; return Math.round(perm(n,r)/fact(r)); }
function fmt(n){ return n.toLocaleString('ko-KR'); }
function sub(n){ return String(n).split('').map(d => '₀₁₂₃₄₅₆₇₈₉'[+d]).join(''); }

// ─── STATE ────────────────────────────────────────────────
let n = 6, r = 3, playing = false, playTimer = null;

const $ = id => document.getElementById(id);
const nSlider = $('nSlider'), rSlider = $('rSlider');
const nValEl  = $('nVal'),    rValEl  = $('rVal');
const playBtn = $('playBtn'),  resetBtn = $('resetBtn');

nSlider.addEventListener('input', () => {
  n = parseInt(nSlider.value);
  nValEl.textContent = n;
  rSlider.max = n;
  if (r > n) { r = n; rSlider.value = n; }
  stopPlay();
  redraw();
});
rSlider.addEventListener('input', () => {
  r = parseInt(rSlider.value);
  stopPlay();
  redraw();
});
playBtn.addEventListener('click', () => playing ? stopPlay() : startPlay());
resetBtn.addEventListener('click', () => {
  stopPlay();
  n = 6; r = 3;
  nSlider.value = 6; rSlider.value = 3; rSlider.max = 6;
  nValEl.textContent = '6';
  redraw();
});

function startPlay(){
  playing = true;
  playBtn.textContent = '■ 정지';
  playBtn.classList.remove('play'); playBtn.classList.add('stop');
  r = 0; rSlider.value = 0; redraw();
  playTimer = setTimeout(playStep, 750);
}
function stopPlay(){
  playing = false;
  clearTimeout(playTimer);
  playBtn.textContent = '▶ r 자동 재생';
  playBtn.classList.remove('stop'); playBtn.classList.add('play');
}
function playStep(){
  if (!playing) return;
  if (r >= n) { stopPlay(); return; }
  r++; rSlider.value = r; redraw();
  playTimer = setTimeout(playStep, 750);
}

// ─── CHART ────────────────────────────────────────────────
const CW = 780, CH = 380;
const PL = 55, PR = 22, PT = 48, PB = 130;
const PW = CW - PL - PR, PH = CH - PT - PB;

function drawChart(svgId, type){
  const svg = $(svgId);
  const isP = (type === 'P');
  const fn  = isP ? perm : comb;
  const values = [];
  for (let i = 0; i <= n; i++) values.push(fn(n, i));
  const maxV  = Math.max(...values, 1);
  const cellW = PW / (n + 1);
  const barW  = cellW * 0.66;

  let s = `<defs>
    <linearGradient id="${svgId}_act" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="${isP?'#bfdbfe':'#fef08a'}"/>
      <stop offset=".5" stop-color="${isP?'#60a5fa':'#fbbf24'}"/>
      <stop offset="1" stop-color="${isP?'#1d4ed8':'#b45309'}"/>
    </linearGradient>
    <linearGradient id="${svgId}_dim" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="${isP?'rgba(96,165,250,.5)':'rgba(251,191,36,.5)'}"/>
      <stop offset="1" stop-color="${isP?'rgba(37,99,235,.22)':'rgba(180,83,9,.22)'}"/>
    </linearGradient>
    <filter id="${svgId}_glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>`;

  // baseline
  s += `<line x1="${PL}" y1="${PT+PH}" x2="${PL+PW}" y2="${PT+PH}"
    stroke="rgba(255,255,255,.28)" stroke-width="1.5"/>`;

  // Bars
  for (let i = 0; i <= n; i++){
    const cx = PL + i*cellW + cellW/2;
    const x  = cx - barW/2;
    const h  = Math.max((values[i]/maxV) * PH, 2);
    const y  = PT + PH - h;
    const active = (i === r);
    const fill   = active ? `url(#${svgId}_act)` : `url(#${svgId}_dim)`;
    const stroke = active ? (isP ? '#60a5fa' : '#fbbf24') : 'none';
    const flt    = active ? ` filter="url(#${svgId}_glow)"` : '';
    s += `<rect x="${x}" y="${y}" width="${barW}" height="${h}"
      fill="${fill}" stroke="${stroke}" stroke-width="${active?2.8:0}" rx="5" ry="5"${flt}/>`;

    // value label
    if (active){
      s += `<text x="${cx}" y="${y-12}" text-anchor="middle"
        font-size="18" font-weight="900"
        fill="${isP ? '#dbeafe' : '#fef3c7'}"
        font-family="Courier New,monospace"
        style="paint-order:stroke;stroke:rgba(0,0,0,.4);stroke-width:3"
        >${fmt(values[i])}</text>`;
    } else if (h > 30) {
      s += `<text x="${cx}" y="${y-6}" text-anchor="middle"
        font-size="11.5" font-weight="700"
        fill="rgba(255,255,255,.6)"
        font-family="Courier New,monospace">${fmt(values[i])}</text>`;
    }

    // r-axis label
    s += `<text x="${cx}" y="${PT+PH+24}" text-anchor="middle"
      font-size="${active?17:14}" font-weight="${active?900:700}"
      fill="${active?'#fff':'rgba(255,255,255,.62)'}"
      font-family="Courier New,monospace">r=${i}</text>`;
  }

  // Multiplier row (below x-axis)
  const mulY = PT + PH + 62;
  for (let i = 1; i <= n; i++){
    const cx_prev = PL + (i-1)*cellW + cellW/2;
    const cx_curr = PL + i*cellW + cellW/2;
    const mid_x = (cx_prev + cx_curr) / 2;
    const mulRaw  = isP ? (n - i + 1) : ((n - i + 1) / i);
    const mulText = isP ? `×${n-i+1}` : `×${n-i+1}/${i}`;
    const isActive = (i === r);
    const color = mulRaw >= 1 ? '#34d399' : '#fb7185';
    const opacity = isActive ? 1 : 0.55;

    if (isActive){
      s += `<rect x="${mid_x-30}" y="${mulY-13}" width="60" height="22" rx="11"
        fill="rgba(255,255,255,.15)" stroke="${color}" stroke-width="1.8"/>`;
    }
    s += `<text x="${mid_x}" y="${mulY+4}" text-anchor="middle"
      font-size="${isActive?14:11.5}" font-weight="${isActive?900:800}"
      fill="${color}" opacity="${opacity}"
      font-family="Courier New,monospace">${mulText}</text>`;
  }

  // Axis caption
  s += `<text x="${PL+PW/2}" y="${PT+PH+98}" text-anchor="middle"
    font-size="13.5" fill="rgba(255,255,255,.55)" font-style="italic">
    선택할 개수 r  (아래 배지 = 이전 항 → 다음 항으로 곱하는 비율)
  </text>`;

  svg.setAttribute('viewBox', `0 0 ${CW} ${CH}`);
  svg.innerHTML = s;
}

// ─── PANEL UPDATE ────────────────────────────────────────
function updatePanel(){
  const P = perm(n, r), C = comb(n, r), R = fact(r);

  // labels with subscripts
  $('pLbl').textContent = `${sub(n)}P${sub(r)} (순열)`;
  $('cLbl').textContent = `${sub(n)}C${sub(r)} (조합)`;

  $('pVal').textContent = fmt(P);
  $('cVal').textContent = fmt(C);
  $('ratioVal').textContent = fmt(R);

  // P formula
  let pf;
  if (r === 0)      pf = '= 1 (약속)';
  else if (r === 1) pf = `${n}`;
  else { const ts = []; for(let i=0;i<r;i++) ts.push(n-i); pf = ts.join(' × '); }
  $('pFormula').textContent = pf;

  // C formula
  $('cFormula').textContent = r === 0 ? '= 1 (약속)' :
                              r === 1 ? `${fmt(P)} ÷ 1!` : `${fmt(P)} ÷ ${r}!`;
  $('ratioFormula').textContent = `= ${r}!`;

  // Relation
  $('cmpRel').innerHTML =
    `<span class="hp">${sub(n)}P${sub(r)}</span> = ` +
    `<span class="hr">${r}!</span> × ` +
    `<span class="hc">${sub(n)}C${sub(r)}</span>` +
    `&nbsp;⟶&nbsp;` +
    `<span class="hp">${fmt(P)}</span> = ` +
    `<span class="hr">${fmt(R)}</span> × ` +
    `<span class="hc">${fmt(C)}</span> ✓`;

  // Insights
  if (r === 0){
    $('pMulList').textContent = '(아직 곱한 수 없음)';
  } else {
    const list = [];
    const limit = Math.min(r, 7);
    for (let i = 1; i <= limit; i++) list.push(`×${n-i+1}`);
    if (r > 7) list.push('…');
    $('pMulList').textContent = list.join(' ');
  }

  if (r === 0){
    $('cMulNow').textContent = '(시작점)';
  } else {
    const num = n - r + 1, den = r;
    const val = num / den;
    $('cMulNow').textContent = `×${num}/${den} = ${val.toFixed(2)}`;
  }

  // pulse animation on r badge
  rValEl.classList.remove('pulse-r');
  void rValEl.offsetWidth;
  rValEl.classList.add('pulse-r');
}

function redraw(){
  rValEl.textContent = r;
  drawChart('pChart', 'P');
  drawChart('cChart', 'C');
  updatePanel();
}

// init
redraw();
</script>
</body>
</html>"""


def render():
    st.markdown("### 🏁 순열 vs 조합 — r 증가 레이스")
    st.markdown(
        "같은 **n** 에서 **r 을 0 → n** 까지 늘릴 때 "
        "**순열 ₙPᵣ** 과 **조합 ₙCᵣ** 가 어떻게 달라지는지 막대그래프로 함께 비교해 보세요!"
    )
    components.html(_HTML, height=1650, scrolling=False)
