import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 정규분포곡선 탐색기",
    "description": "평균(μ)과 표준편차(σ)를 조절하며 정규분포 곡선의 모양 변화를 실시간으로 탐색합니다.",
    "order": 70,
}

_HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;font-family:'Segoe UI',system-ui,sans-serif;background:#0b0f1a;color:#e2e8f0;font-size:15px}
body{padding:10px 10px 28px}

/* ── 탭 ── */
.tabs{display:flex;gap:8px;margin-bottom:16px}
.tab{padding:9px 22px;border-radius:12px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);cursor:pointer;font-size:14px;font-weight:600;color:#64748b;transition:all .2s;letter-spacing:.01em}
.tab:hover{background:rgba(255,255,255,.07);color:#94a3b8}
.tab.active{background:rgba(99,102,241,.2);color:#a5b4fc;border-color:rgba(99,102,241,.4);box-shadow:0 0 16px rgba(99,102,241,.2)}

/* ── 카드 ── */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:16px 20px;margin-bottom:14px;backdrop-filter:blur(8px)}
.card-title{font-size:15px;font-weight:700;margin-bottom:14px;display:flex;align-items:center;gap:8px;letter-spacing:.02em}

/* ── 슬라이더 ── */
.slider-group{margin-bottom:16px}
.slider-label{font-size:13px;color:#94a3b8;font-weight:600;display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.badge{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;font-weight:900;font-size:16px;padding:3px 16px;border-radius:10px;min-width:64px;text-align:center;box-shadow:0 2px 12px rgba(99,102,241,.4)}
.badge-s{background:linear-gradient(135deg,#f59e0b,#ef4444);box-shadow:0 2px 12px rgba(245,158,11,.4)}
.badge-b{background:linear-gradient(135deg,#f59e0b,#fb923c);box-shadow:0 2px 12px rgba(245,158,11,.35)}
input[type=range]{-webkit-appearance:none;width:100%;height:7px;border-radius:4px;outline:none;cursor:pointer;margin-top:2px}
.r-mu{background:linear-gradient(90deg,#6366f1,#8b5cf6)}
.r-si{background:linear-gradient(90deg,#f59e0b,#ef4444)}
.r-mub{background:linear-gradient(90deg,#f59e0b,#fb923c)}
.r-sib{background:linear-gradient(90deg,#f43f5e,#f97316)}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;background:#fff;border:3px solid #8b5cf6;cursor:pointer;box-shadow:0 0 14px rgba(139,92,246,.7);transition:transform .15s}
.r-si::-webkit-slider-thumb,.r-sib::-webkit-slider-thumb{border-color:#f59e0b;box-shadow:0 0 14px rgba(245,158,11,.7)}
.r-mub::-webkit-slider-thumb{border-color:#fb923c;box-shadow:0 0 14px rgba(251,146,60,.7)}
.r-sib::-webkit-slider-thumb{border-color:#f43f5e;box-shadow:0 0 14px rgba(244,63,94,.7)}
input[type=range]::-webkit-slider-thumb:hover{transform:scale(1.25)}

/* ── 캔버스 ── */
.canvas-wrap{width:100%;border-radius:14px;overflow:hidden;background:linear-gradient(180deg,#0a0e1a 0%,#060810 100%);border:1px solid rgba(255,255,255,.08)}
canvas{display:block;width:100%}

/* ── 경험법칙 카드 ── */
.emp-row{display:flex;gap:10px;flex-wrap:wrap}
.emp-card{flex:1;min-width:100px;border-radius:16px;padding:14px 10px;text-align:center;border:1.5px solid}
.emp-1{background:rgba(99,102,241,.1);border-color:rgba(99,102,241,.35)}
.emp-2{background:rgba(16,185,129,.1);border-color:rgba(16,185,129,.35)}
.emp-3{background:rgba(245,158,11,.1);border-color:rgba(245,158,11,.35)}
.emp-pct{font-size:26px;font-weight:900}
.emp-1 .emp-pct{color:#a5b4fc}
.emp-2 .emp-pct{color:#6ee7b7}
.emp-3 .emp-pct{color:#fde68a}
.emp-range{font-size:11px;color:#64748b;margin-top:4px;font-weight:600;letter-spacing:.03em}
.emp-label{font-size:12px;margin-top:2px}
.emp-1 .emp-label{color:#818cf8}
.emp-2 .emp-label{color:#34d399}
.emp-3 .emp-label{color:#fbbf24}

/* ── 통계 수치 카드 ── */
.stat-row{display:flex;gap:8px;flex-wrap:wrap}
.scard{flex:1;min-width:80px;background:rgba(0,0,0,.28);border-radius:14px;padding:11px 8px;text-align:center;border:1.5px solid rgba(255,255,255,.08)}
.sv{font-size:20px;font-weight:900;color:#a5b4fc}
.sl{font-size:11px;color:#475569;font-weight:600;margin-top:3px;letter-spacing:.04em;text-transform:uppercase}

/* ── 관찰 박스 ── */
.obs{display:flex;align-items:flex-start;gap:12px;padding:12px 16px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:14px;margin-bottom:10px;transition:background .3s}
.obs-icon{font-size:21px;flex-shrink:0;line-height:1.3}
.obs-text{font-size:13.5px;color:#cbd5e1;line-height:1.6}
.obs-text strong{color:#e2e8f0}

/* ── 프리셋 버튼 ── */
.preset-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:4px}
.preset-btn{padding:6px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.06);cursor:pointer;font-size:12px;font-weight:700;color:#94a3b8;transition:all .2s;letter-spacing:.02em}
.preset-btn:hover{background:rgba(99,102,241,.2);color:#a5b4fc;border-color:rgba(99,102,241,.4)}
.preset-btn.act{background:rgba(99,102,241,.25);color:#c7d2fe;border-color:rgba(99,102,241,.5)}

/* ── 비교 탭 그리드 ── */
.cmp-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:520px){.cmp-grid{grid-template-columns:1fr}}
.card-a{border-color:rgba(99,102,241,.45)!important}
.card-b{border-color:rgba(251,146,60,.45)!important}

/* ── 비교 인사이트 칩 ── */
.insight{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;border-radius:12px;margin-bottom:8px;border:1px solid}

/* ── 스크롤바 ── */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(99,102,241,.4);border-radius:3px}
</style>
</head>
<body>

<div class="tabs">
  <button class="tab active" id="tabBtn0" onclick="switchTab(0)">🔍 단일 곡선 탐색</button>
  <button class="tab"        id="tabBtn1" onclick="switchTab(1)">📊 두 곡선 비교</button>
</div>

<!-- ════════════════════════════════════════════════════════
     Tab 0 : 단일 곡선 탐색
════════════════════════════════════════════════════════ -->
<div id="pane0">

  <!-- 파라미터 컨트롤 -->
  <div class="card">
    <div class="card-title" style="color:#a5b4fc">⚙️ 파라미터 조절</div>

    <div class="slider-group">
      <div class="slider-label">
        <span>μ (평균) — 곡선의 <em>위치</em>를 결정합니다</span>
        <span class="badge" id="mu1Disp">0.0</span>
      </div>
      <input type="range" class="r-mu" id="mu1" min="-4" max="4" step="0.1" value="0">
    </div>

    <div class="slider-group" style="margin-bottom:6px">
      <div class="slider-label">
        <span>σ (표준편차) — 곡선의 <em>퍼짐</em>을 결정합니다</span>
        <span class="badge badge-s" id="si1Disp">1.0</span>
      </div>
      <input type="range" class="r-si" id="si1" min="0.3" max="3.0" step="0.1" value="1.0">
    </div>

    <div class="preset-row" style="margin-top:12px">
      <span style="font-size:12px;color:#475569;font-weight:700;align-self:center">빠른 설정 →</span>
      <button class="preset-btn" onclick="setPreset1(0,1)">표준정규 N(0,1)</button>
      <button class="preset-btn" onclick="setPreset1(0,0.5)">좁은 곡선 σ=0.5</button>
      <button class="preset-btn" onclick="setPreset1(0,2)">넓은 곡선 σ=2.0</button>
      <button class="preset-btn" onclick="setPreset1(3,1)">오른쪽 이동 μ=3</button>
    </div>
  </div>

  <!-- 캔버스 -->
  <div class="card canvas-wrap" style="padding:0">
    <canvas id="c1" width="860" height="320"></canvas>
  </div>

  <!-- 경험 법칙 -->
  <div class="card">
    <div class="card-title" style="color:#fde68a">📐 경험 법칙 (68 – 95 – 99.7)</div>
    <div class="emp-row">
      <div class="emp-card emp-1">
        <div class="emp-pct">68.3%</div>
        <div class="emp-range" id="empR1">−1.00 ~ 1.00</div>
        <div class="emp-label">μ ± 1σ 구간</div>
      </div>
      <div class="emp-card emp-2">
        <div class="emp-pct">95.4%</div>
        <div class="emp-range" id="empR2">−2.00 ~ 2.00</div>
        <div class="emp-label">μ ± 2σ 구간</div>
      </div>
      <div class="emp-card emp-3">
        <div class="emp-pct">99.7%</div>
        <div class="emp-range" id="empR3">−3.00 ~ 3.00</div>
        <div class="emp-label">μ ± 3σ 구간</div>
      </div>
    </div>
    <!-- 시각적 밴드 바 -->
    <div id="empBand" style="margin-top:16px;height:52px;position:relative;border-radius:14px;overflow:hidden"></div>
  </div>

  <!-- 통계 수치 -->
  <div class="card">
    <div class="card-title" style="color:#6ee7b7">📋 곡선 정보</div>
    <div class="stat-row">
      <div class="scard"><div class="sv" id="i-mu">0.00</div><div class="sl">평균 μ</div></div>
      <div class="scard"><div class="sv" id="i-si">1.00</div><div class="sl">표준편차 σ</div></div>
      <div class="scard"><div class="sv" id="i-va">1.00</div><div class="sl">분산 σ²</div></div>
      <div class="scard"><div class="sv" id="i-pk" style="color:#fbbf24">0.399</div><div class="sl">최댓값 f(μ)</div></div>
      <div class="scard"><div class="sv" id="i-fw" style="color:#6ee7b7">2.355</div><div class="sl">반치전폭 FWHM</div></div>
    </div>
  </div>

  <!-- 탐구 관찰 -->
  <div class="card">
    <div class="card-title" style="color:#f9a8d4">💡 탐구 관찰</div>
    <div id="obsBox"></div>
  </div>
</div>

<!-- ════════════════════════════════════════════════════════
     Tab 1 : 두 곡선 비교
════════════════════════════════════════════════════════ -->
<div id="pane1" style="display:none">

  <!-- 프리셋 -->
  <div class="card" style="padding:14px 18px">
    <div class="card-title" style="color:#94a3b8;margin-bottom:10px">🎯 비교 시나리오 프리셋</div>
    <div class="preset-row">
      <button class="preset-btn" id="prc0" onclick="setCmpPreset(0)">① μ만 다를 때</button>
      <button class="preset-btn" id="prc1" onclick="setCmpPreset(1)">② σ만 다를 때</button>
      <button class="preset-btn" id="prc2" onclick="setCmpPreset(2)">③ 둘 다 다를 때</button>
      <button class="preset-btn" id="prc3" onclick="setCmpPreset(3)">④ 대칭 배치</button>
    </div>
  </div>

  <!-- 두 곡선 컨트롤 -->
  <div class="cmp-grid">
    <div class="card card-a">
      <div class="card-title" style="color:#a5b4fc">🔵 곡선 A</div>
      <div class="slider-group">
        <div class="slider-label">
          <span>μ_A</span>
          <span class="badge" id="muADisp">−2.0</span>
        </div>
        <input type="range" class="r-mu" id="muA" min="-4" max="4" step="0.1" value="-2">
      </div>
      <div class="slider-group" style="margin-bottom:0">
        <div class="slider-label">
          <span>σ_A</span>
          <span class="badge badge-s" id="siADisp">1.0</span>
        </div>
        <input type="range" class="r-si" id="siA" min="0.3" max="3.0" step="0.1" value="1.0">
      </div>
    </div>
    <div class="card card-b">
      <div class="card-title" style="color:#fdba74">🟠 곡선 B</div>
      <div class="slider-group">
        <div class="slider-label">
          <span>μ_B</span>
          <span class="badge badge-b" id="muBDisp">2.0</span>
        </div>
        <input type="range" class="r-mub" id="muB" min="-4" max="4" step="0.1" value="2">
      </div>
      <div class="slider-group" style="margin-bottom:0">
        <div class="slider-label">
          <span>σ_B</span>
          <span class="badge badge-b" id="siBDisp">1.0</span>
        </div>
        <input type="range" class="r-sib" id="siB" min="0.3" max="3.0" step="0.1" value="1.0">
      </div>
    </div>
  </div>

  <!-- 캔버스 비교 -->
  <div class="card canvas-wrap" style="padding:0">
    <canvas id="c2" width="860" height="320"></canvas>
  </div>

  <!-- 비교 인사이트 -->
  <div class="card">
    <div class="card-title" style="color:#fbbf24">🔍 비교 분석</div>
    <div id="cmpBox"></div>
  </div>

</div><!-- /pane1 -->

<script>
// ── 수학 유틸 ─────────────────────────────────────────────────
const TAU = 2 * Math.PI;
const FWHM = 2 * Math.sqrt(2 * Math.log(2)); // ≈ 2.3548

function pdf(x, mu, si) {
  return Math.exp(-0.5 * ((x - mu) / si) ** 2) / (si * Math.sqrt(TAU));
}
function fmt(v, d = 2) { return parseFloat(v).toFixed(d); }

// ── 탭 전환 ───────────────────────────────────────────────────
let curTab = 0;
function switchTab(t) {
  curTab = t;
  document.getElementById('pane0').style.display = t === 0 ? '' : 'none';
  document.getElementById('pane1').style.display = t === 1 ? '' : 'none';
  document.getElementById('tabBtn0').className = 'tab' + (t === 0 ? ' active' : '');
  document.getElementById('tabBtn1').className = 'tab' + (t === 1 ? ' active' : '');
  if (t === 1) drawCmp();
}

// ── 캔버스 공통 설정 ──────────────────────────────────────────
const PAD = { t: 24, b: 44, l: 46, r: 18 };

function canvasSetup(c) {
  const ratio = window.devicePixelRatio || 1;
  const W = c.clientWidth || 860;
  c.width = W * ratio;
  c.height = 320 * ratio;
  const ctx = c.getContext('2d');
  ctx.scale(ratio, ratio);
  return { ctx, W, H: 320 };
}

function makeCoord(xMin, xMax, yMaxActual, W, H) {
  const cw = W - PAD.l - PAD.r;
  const ch = H - PAD.t - PAD.b;
  return {
    toX: x => PAD.l + (x - xMin) / (xMax - xMin) * cw,
    toY: y => PAD.t + ch - Math.max(0, Math.min(ch, (y / yMaxActual) * ch)),
    baseY: PAD.t + ch,
    cw, ch
  };
}

function drawBackground(ctx, W, H) {
  const bg = ctx.createLinearGradient(0, 0, 0, H);
  bg.addColorStop(0, '#0b0f1a');
  bg.addColorStop(1, '#070a12');
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);
}

function drawGrid(ctx, coord, xMin, xMax, step = 1) {
  ctx.strokeStyle = 'rgba(255,255,255,0.05)';
  ctx.lineWidth = 1;
  ctx.setLineDash([]);
  for (let x = Math.ceil(xMin / step) * step; x <= xMax; x += step) {
    ctx.beginPath();
    ctx.moveTo(coord.toX(x), PAD.t);
    ctx.lineTo(coord.toX(x), coord.baseY);
    ctx.stroke();
  }
}

function drawXAxis(ctx, coord, xMin, xMax, W, H) {
  // Axis line
  ctx.beginPath();
  ctx.moveTo(PAD.l, coord.baseY);
  ctx.lineTo(W - PAD.r, coord.baseY);
  ctx.strokeStyle = 'rgba(255,255,255,0.25)';
  ctx.lineWidth = 1.5;
  ctx.setLineDash([]);
  ctx.stroke();

  // Ticks + labels
  ctx.fillStyle = '#475569';
  ctx.font = '11px Segoe UI, sans-serif';
  ctx.textAlign = 'center';
  const step = (xMax - xMin) <= 10 ? 1 : 2;
  for (let x = Math.ceil(xMin); x <= xMax; x += step) {
    ctx.fillText(x, coord.toX(x), coord.baseY + 16);
  }
}

function drawNormalFill(ctx, coord, mu, si, xMin, xMax, color) {
  ctx.beginPath();
  let first = true;
  for (let px = 0; px <= coord.cw; px += 0.5) {
    const x = xMin + (px / coord.cw) * (xMax - xMin);
    const py = coord.toY(pdf(x, mu, si));
    if (first) { ctx.moveTo(PAD.l + px, py); first = false; }
    else ctx.lineTo(PAD.l + px, py);
  }
  ctx.lineTo(coord.toX(xMax), coord.baseY);
  ctx.lineTo(coord.toX(xMin), coord.baseY);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
}

function drawNormalCurve(ctx, coord, mu, si, xMin, xMax, strokeColor, glowColor, lw = 3) {
  ctx.beginPath();
  let first = true;
  for (let px = 0; px <= coord.cw; px += 0.5) {
    const x = xMin + (px / coord.cw) * (xMax - xMin);
    const py = coord.toY(pdf(x, mu, si));
    if (first) { ctx.moveTo(PAD.l + px, py); first = false; }
    else ctx.lineTo(PAD.l + px, py);
  }
  ctx.strokeStyle = strokeColor;
  ctx.lineWidth = lw;
  ctx.shadowBlur = 16;
  ctx.shadowColor = glowColor;
  ctx.setLineDash([]);
  ctx.stroke();
  ctx.shadowBlur = 0;
}

function drawVDash(ctx, coord, x, color, lw = 1) {
  ctx.beginPath();
  ctx.moveTo(coord.toX(x), PAD.t);
  ctx.lineTo(coord.toX(x), coord.baseY);
  ctx.strokeStyle = color;
  ctx.lineWidth = lw;
  ctx.setLineDash([5, 4]);
  ctx.stroke();
  ctx.setLineDash([]);
}

function drawPeakDot(ctx, coord, mu, si, strokeColor) {
  const peak = pdf(mu, mu, si);
  const px = coord.toX(mu);
  const py = coord.toY(peak);
  ctx.beginPath();
  ctx.arc(px, py, 5.5, 0, TAU);
  ctx.fillStyle = '#fff';
  ctx.fill();
  ctx.strokeStyle = strokeColor;
  ctx.lineWidth = 2.5;
  ctx.setLineDash([]);
  ctx.stroke();
  return { px, py, peak };
}

// ════════════════════════════════════════════════════════
//  Tab 0 : 단일 곡선
// ════════════════════════════════════════════════════════

function drawSingle() {
  const c = document.getElementById('c1');
  const { ctx, W, H } = canvasSetup(c);
  const mu = parseFloat(document.getElementById('mu1').value);
  const si = parseFloat(document.getElementById('si1').value);

  const xMin = -8, xMax = 8;
  const peak = pdf(mu, mu, si);
  const yMaxActual = peak * 1.22;
  const coord = makeCoord(xMin, xMax, yMaxActual, W, H);

  drawBackground(ctx, W, H);
  drawGrid(ctx, coord, xMin, xMax);

  // 3σ 채우기 (레이어 순서: 3σ → 2σ → 1σ)
  const bands = [
    { k: 3, fc: 'rgba(245,158,11,0.10)', edge: 'rgba(245,158,11,0.25)' },
    { k: 2, fc: 'rgba(16,185,129,0.12)', edge: 'rgba(16,185,129,0.30)' },
    { k: 1, fc: 'rgba(99,102,241,0.18)', edge: 'rgba(99,102,241,0.40)' },
  ];
  bands.forEach(({ k, fc }) => {
    const lo = Math.max(xMin, mu - k * si);
    const hi = Math.min(xMax, mu + k * si);
    ctx.beginPath();
    ctx.moveTo(coord.toX(lo), coord.baseY);
    for (let px = 0; px <= coord.cw; px += 0.5) {
      const x = xMin + (px / coord.cw) * (xMax - xMin);
      if (x < lo || x > hi) continue;
      ctx.lineTo(PAD.l + px, coord.toY(pdf(x, mu, si)));
    }
    ctx.lineTo(coord.toX(hi), coord.baseY);
    ctx.closePath();
    ctx.fillStyle = fc;
    ctx.fill();
  });

  // σ 경계선 (점선)
  const vLines = [
    [mu - 3*si, 'rgba(245,158,11,0.35)'], [mu + 3*si, 'rgba(245,158,11,0.35)'],
    [mu - 2*si, 'rgba(16,185,129,0.40)'], [mu + 2*si, 'rgba(16,185,129,0.40)'],
    [mu - si,   'rgba(99,102,241,0.50)'], [mu + si,   'rgba(99,102,241,0.50)'],
  ];
  vLines.forEach(([x, col]) => { if (x >= xMin && x <= xMax) drawVDash(ctx, coord, x, col); });

  // μ 기준선 (실선)
  ctx.beginPath();
  ctx.moveTo(coord.toX(mu), PAD.t);
  ctx.lineTo(coord.toX(mu), coord.baseY);
  ctx.strokeStyle = 'rgba(255,255,255,0.50)';
  ctx.lineWidth = 1.5;
  ctx.setLineDash([]);
  ctx.stroke();

  drawXAxis(ctx, coord, xMin, xMax, W, H);

  // σ 레이블 (x축 아래)
  ctx.font = 'bold 10px Segoe UI, sans-serif';
  ctx.textAlign = 'center';
  [
    [mu - si, 'μ−σ', '#818cf8'], [mu + si, 'μ+σ', '#818cf8'],
    [mu - 2*si, 'μ−2σ', '#34d399'], [mu + 2*si, 'μ+2σ', '#34d399'],
  ].forEach(([x, lbl, col]) => {
    if (x >= xMin + 0.2 && x <= xMax - 0.2) {
      ctx.fillStyle = col;
      ctx.fillText(lbl, coord.toX(x), coord.baseY + 30);
    }
  });

  // μ 레이블
  ctx.fillStyle = 'rgba(255,255,255,0.85)';
  ctx.font = 'bold 12px Segoe UI, sans-serif';
  ctx.fillText('μ', coord.toX(mu), coord.baseY + 30);

  // 곡선 그리기 (그라디언트 스트로크)
  const grad = ctx.createLinearGradient(PAD.l, 0, W - PAD.r, 0);
  grad.addColorStop(0, 'rgba(139,92,246,0.3)');
  grad.addColorStop(0.5, '#a78bfa');
  grad.addColorStop(1, 'rgba(139,92,246,0.3)');
  drawNormalFill(ctx, coord, mu, si, xMin, xMax, 'rgba(99,102,241,0.08)');
  drawNormalCurve(ctx, coord, mu, si, xMin, xMax, '#a78bfa', '#8b5cf6', 3);

  // 피크 점 + 레이블
  const { px: ppx, py: ppy } = drawPeakDot(ctx, coord, mu, si, '#a78bfa');
  ctx.fillStyle = '#e2e8f0';
  ctx.font = 'bold 12px Segoe UI, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(`f(μ) = ${fmt(peak, 4)}`, ppx, ppy - 14);

  // UI 업데이트
  document.getElementById('mu1Disp').textContent = fmt(mu);
  document.getElementById('si1Disp').textContent = fmt(si);
  document.getElementById('i-mu').textContent = fmt(mu);
  document.getElementById('i-si').textContent = fmt(si);
  document.getElementById('i-va').textContent = fmt(si * si);
  document.getElementById('i-pk').textContent = fmt(peak, 4);
  document.getElementById('i-fw').textContent = fmt(FWHM * si, 3);

  document.getElementById('empR1').textContent = `${fmt(mu - si)} ~ ${fmt(mu + si)}`;
  document.getElementById('empR2').textContent = `${fmt(mu - 2*si)} ~ ${fmt(mu + 2*si)}`;
  document.getElementById('empR3').textContent = `${fmt(mu - 3*si)} ~ ${fmt(mu + 3*si)}`;

  renderEmpBand(mu, si);
  renderObs(mu, si, peak);
}

function renderEmpBand(mu, si) {
  const el = document.getElementById('empBand');
  // 3σ → 2σ → 1σ 중첩 막대
  const pct1 = 100 * (2 * si) / (6 * si);   // 1σ width / 3σ total = 33.3%
  const pct2 = 100 * (4 * si) / (6 * si);   // 2σ width / 3σ total = 66.7%
  el.innerHTML = `
    <div style="position:relative;width:100%;height:52px;">
      <!-- 3σ 전체 -->
      <div style="position:absolute;inset:0;background:rgba(245,158,11,.18);border-radius:14px"></div>
      <!-- 2σ -->
      <div style="position:absolute;top:7px;left:${(100-pct2)/2}%;width:${pct2}%;height:38px;background:rgba(16,185,129,.22);border-radius:10px"></div>
      <!-- 1σ -->
      <div style="position:absolute;top:13px;left:${(100-pct1)/2}%;width:${pct1}%;height:26px;background:rgba(99,102,241,.30);border-radius:8px"></div>
      <!-- 중심 -->
      <div style="position:absolute;top:0;left:50%;transform:translateX(-50%);width:2px;height:52px;background:rgba(255,255,255,.45)"></div>
      <!-- 레이블 -->
      <div style="position:absolute;top:50%;left:6px;transform:translateY(-50%);font-size:10px;font-weight:800;color:rgba(245,158,11,.9)">99.7%</div>
      <div style="position:absolute;top:50%;right:6px;transform:translateY(-50%);font-size:10px;font-weight:800;color:rgba(245,158,11,.9)">99.7%</div>
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:10px;font-weight:800;color:rgba(99,102,241,.9)">68.3%</div>
    </div>`;
}

function renderObs(mu, si, peak) {
  const items = [];

  // μ 관찰
  if (Math.abs(mu) < 0.15) {
    items.push({ icon: '↔️', text: '현재 μ = 0입니다. 곡선이 <strong>원점에 대칭</strong>으로 놓여 있습니다.' });
  } else {
    const dir = mu > 0 ? '오른쪽' : '왼쪽';
    items.push({ icon: '↔️', text: `μ = ${fmt(mu)}으로 곡선이 ${dir}에 위치합니다. μ를 바꾸면 곡선이 <strong>좌우로 평행이동</strong>할 뿐, 모양(폭·높이)은 전혀 변하지 않습니다.` });
  }

  // σ 관찰
  if (si <= 0.6) {
    items.push({ icon: '📏', text: `σ = ${fmt(si)} — 아주 <strong>좁고 높은 첨봉형</strong> 곡선입니다. 데이터가 평균 주변에 매우 밀집되어 있음을 의미합니다.` });
  } else if (si >= 2.2) {
    items.push({ icon: '📏', text: `σ = ${fmt(si)} — 아주 <strong>넓고 낮은 완만형</strong> 곡선입니다. 데이터가 넓은 범위에 고르게 퍼져 있음을 의미합니다.` });
  } else {
    items.push({ icon: '📏', text: `σ = ${fmt(si)}입니다. σ가 커질수록 곡선은 <strong>넓고 낮게</strong>, 작아질수록 <strong>좁고 높게</strong> 변합니다.` });
  }

  // 최댓값 & σ 관계
  items.push({ icon: '🔺', text: `최댓값 f(μ) = <strong>${fmt(peak, 4)}</strong>은 σ에 반비례합니다.<br>σ가 2배 → 최댓값은 ½배, σ가 ½배 → 최댓값은 2배.` });

  // 넓이 = 1
  items.push({ icon: '∫', text: `어떤 μ·σ 값을 사용해도 <strong>곡선 아래의 넓이는 항상 1</strong>입니다.<br>σ가 커져 곡선이 낮아지는 대신, 더 넓게 펼쳐져 총 넓이를 보존합니다.` });

  document.getElementById('obsBox').innerHTML = items.map(({ icon, text }) =>
    `<div class="obs"><span class="obs-icon">${icon}</span><span class="obs-text">${text}</span></div>`
  ).join('');
}

// ── 프리셋 (단일) ─────────────────────────────────────────────
function setPreset1(mu, si) {
  document.getElementById('mu1').value = mu;
  document.getElementById('si1').value = si;
  document.getElementById('mu1Disp').textContent = fmt(mu);
  document.getElementById('si1Disp').textContent = fmt(si);
  drawSingle();
}

// ════════════════════════════════════════════════════════
//  Tab 1 : 두 곡선 비교
// ════════════════════════════════════════════════════════

function drawCmp() {
  const c = document.getElementById('c2');
  const { ctx, W, H } = canvasSetup(c);

  const muA = parseFloat(document.getElementById('muA').value);
  const siA = parseFloat(document.getElementById('siA').value);
  const muB = parseFloat(document.getElementById('muB').value);
  const siB = parseFloat(document.getElementById('siB').value);

  // 범위를 두 곡선이 모두 보이도록 자동 계산
  const margin = 4;
  const rawMin = Math.min(muA - 3.5*siA, muB - 3.5*siB) - margin * 0;
  const rawMax = Math.max(muA + 3.5*siA, muB + 3.5*siB) + margin * 0;
  const center = (rawMin + rawMax) / 2;
  const halfW = Math.max((rawMax - rawMin) / 2, 5);
  const xMin = Math.max(-10, center - halfW - 1.5);
  const xMax = Math.min(10, center + halfW + 1.5);

  const peakA = pdf(muA, muA, siA);
  const peakB = pdf(muB, muB, siB);
  const yMaxActual = Math.max(peakA, peakB) * 1.25;
  const coord = makeCoord(xMin, xMax, yMaxActual, W, H);

  drawBackground(ctx, W, H);
  drawGrid(ctx, coord, xMin, xMax, (xMax - xMin) > 12 ? 2 : 1);

  // 채우기
  drawNormalFill(ctx, coord, muA, siA, xMin, xMax, 'rgba(99,102,241,0.14)');
  drawNormalFill(ctx, coord, muB, siB, xMin, xMax, 'rgba(251,146,60,0.12)');

  // μ 기준선
  drawVDash(ctx, coord, muA, 'rgba(99,102,241,0.55)', 1.5);
  drawVDash(ctx, coord, muB, 'rgba(251,146,60,0.55)', 1.5);

  drawXAxis(ctx, coord, xMin, xMax, W, H);

  // 곡선
  drawNormalCurve(ctx, coord, muA, siA, xMin, xMax, '#a5b4fc', '#6366f1', 3);
  drawNormalCurve(ctx, coord, muB, siB, xMin, xMax, '#fdba74', '#f97316', 3);

  // 피크 점
  drawPeakDot(ctx, coord, muA, siA, '#a5b4fc');
  drawPeakDot(ctx, coord, muB, siB, '#fdba74');

  // μ 레이블 (x축 아래)
  ctx.font = 'bold 11px Segoe UI, sans-serif';
  ctx.textAlign = 'center';
  [[muA, 'μ_A', '#818cf8'], [muB, 'μ_B', '#fb923c']].forEach(([x, lbl, col]) => {
    ctx.fillStyle = col;
    ctx.fillText(lbl, coord.toX(x), coord.baseY + 30);
  });

  // 범례
  ctx.font = 'bold 12px Segoe UI, sans-serif';
  ctx.textAlign = 'left';
  [
    { label: `A: μ=${fmt(muA)}, σ=${fmt(siA)}, f(μ)=${fmt(peakA,3)}`, col: '#a5b4fc', y: 20 },
    { label: `B: μ=${fmt(muB)}, σ=${fmt(siB)}, f(μ)=${fmt(peakB,3)}`, col: '#fdba74', y: 38 },
  ].forEach(({ label, col, y }) => {
    ctx.fillStyle = col;
    ctx.fillRect(PAD.l + 8, PAD.t + y - 9, 18, 4);
    ctx.fillStyle = '#d1d5db';
    ctx.fillText(label, PAD.l + 32, PAD.t + y);
  });

  // UI 업데이트
  document.getElementById('muADisp').textContent = fmt(muA);
  document.getElementById('siADisp').textContent = fmt(siA);
  document.getElementById('muBDisp').textContent = fmt(muB);
  document.getElementById('siBDisp').textContent = fmt(siB);

  renderCmpInsights(muA, siA, peakA, muB, siB, peakB);
}

const CMP_PRESETS = [
  { muA: -2, siA: 1.0, muB: 2,  siB: 1.0,  label: 'μ만 다를 때' },
  { muA:  0, siA: 0.7, muB: 0,  siB: 2.0,  label: 'σ만 다를 때' },
  { muA: -1, siA: 0.8, muB: 2,  siB: 1.6,  label: '둘 다 다를 때' },
  { muA: -3, siA: 1.2, muB: 3,  siB: 1.2,  label: '대칭 배치' },
];

let cmpPresetIdx = 0;
function setCmpPreset(i) {
  cmpPresetIdx = i;
  const p = CMP_PRESETS[i];
  document.getElementById('muA').value = p.muA;
  document.getElementById('siA').value = p.siA;
  document.getElementById('muB').value = p.muB;
  document.getElementById('siB').value = p.siB;
  [0,1,2,3].forEach(j => {
    document.getElementById('prc' + j).className = 'preset-btn' + (j === i ? ' act' : '');
  });
  drawCmp();
}

function renderCmpInsights(muA, siA, peakA, muB, siB, peakB) {
  const items = [];
  const muSame = Math.abs(muA - muB) < 0.2;
  const siSame = Math.abs(siA - siB) < 0.15;

  // 위치 비교
  if (muSame) {
    items.push({ icon: '↔️', color: '#a5b4fc', bg: 'rgba(99,102,241,.08)', border: 'rgba(99,102,241,.25)',
      text: `두 곡선의 평균이 거의 같습니다 (μ ≈ ${fmt((muA+muB)/2)}). 평균이 같으면 곡선은 <strong>같은 위치</strong>에 있습니다.` });
  } else {
    const dir = muA < muB ? '곡선 A가 왼쪽, 곡선 B가 오른쪽' : '곡선 B가 왼쪽, 곡선 A가 오른쪽';
    items.push({ icon: '↔️', color: '#a5b4fc', bg: 'rgba(99,102,241,.08)', border: 'rgba(99,102,241,.25)',
      text: `${dir}에 위치합니다. 평균 차이: |μ_A − μ_B| = <strong>${fmt(Math.abs(muA-muB))}</strong>` });
  }

  // 폭·높이 비교
  if (siSame) {
    items.push({ icon: '📏', color: '#6ee7b7', bg: 'rgba(16,185,129,.08)', border: 'rgba(16,185,129,.25)',
      text: `표준편차가 같아 (σ ≈ ${fmt((siA+siB)/2)}) 두 곡선의 <strong>폭과 높이가 동일</strong>합니다. μ만 다르면 곡선은 단순히 평행이동합니다.` });
  } else if (siA < siB) {
    items.push({ icon: '📏', color: '#6ee7b7', bg: 'rgba(16,185,129,.08)', border: 'rgba(16,185,129,.25)',
      text: `σ_A(${fmt(siA)}) < σ_B(${fmt(siB)}) → <strong>곡선 A가 좁고 높으며</strong>, 곡선 B는 더 넓고 낮습니다. 표준편차가 클수록 데이터가 더 넓게 퍼집니다.` });
  } else {
    items.push({ icon: '📏', color: '#6ee7b7', bg: 'rgba(16,185,129,.08)', border: 'rgba(16,185,129,.25)',
      text: `σ_A(${fmt(siA)}) > σ_B(${fmt(siB)}) → <strong>곡선 B가 좁고 높으며</strong>, 곡선 A는 더 넓고 낮습니다.` });
  }

  // 최댓값
  items.push({ icon: '🔺', color: '#fbbf24', bg: 'rgba(245,158,11,.08)', border: 'rgba(245,158,11,.25)',
    text: `최댓값: A = <strong>${fmt(peakA,4)}</strong>, B = <strong>${fmt(peakB,4)}</strong>. ` +
      (Math.abs(peakA - peakB) < 0.002 ? '두 값이 거의 같습니다 (σ가 같기 때문).' :
       peakA > peakB ? 'σ_A가 작아 A의 최댓값이 더 큽니다.' : 'σ_B가 작아 B의 최댓값이 더 큽니다.') });

  // 넓이
  items.push({ icon: '∫', color: '#f9a8d4', bg: 'rgba(244,114,182,.08)', border: 'rgba(244,114,182,.25)',
    text: '두 곡선의 넓이는 모두 <strong>1</strong>입니다. σ가 커져 곡선이 낮아지더라도, 양쪽으로 펼쳐져 총 확률의 합은 항상 1을 유지합니다.' });

  document.getElementById('cmpBox').innerHTML = items.map(({ icon, color, bg, border, text }) => `
    <div class="insight" style="background:${bg};border-color:${border};margin-bottom:10px">
      <span class="obs-icon">${icon}</span>
      <span class="obs-text">${text}</span>
    </div>`
  ).join('');
}

// ── 이벤트 바인딩 ─────────────────────────────────────────────
document.getElementById('mu1').addEventListener('input', e => {
  document.getElementById('mu1Disp').textContent = fmt(e.target.value);
  drawSingle();
});
document.getElementById('si1').addEventListener('input', e => {
  document.getElementById('si1Disp').textContent = fmt(e.target.value);
  drawSingle();
});
['muA','siA','muB','siB'].forEach(id => {
  document.getElementById(id).addEventListener('input', e => {
    document.getElementById(id + 'Disp').textContent = fmt(e.target.value);
    drawCmp();
  });
});

// ── 초기화 ────────────────────────────────────────────────────
drawSingle();
</script>
</body>
</html>
"""

def render():
    st.header("📊 정규분포곡선 탐색기")
    st.markdown(
        "슬라이더를 움직여 **평균(μ)** 과 **표준편차(σ)** 가 달라질 때 "
        "정규분포 곡선이 어떻게 변하는지 직접 탐색해 보세요."
    )
    components.html(_HTML, height=1040)
