import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 이항분포 그래프 시뮬레이터",
    "description": "n·p를 조절해 이항분포 그래프와 확률분포표를 실시간으로 탐색하고, P(a≤X≤b) 계산 및 분포 분석까지 수행합니다.",
    "order": 63,
}

_HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#e2e8f0;font-size:15px;padding:10px 12px 28px}

/* ── 공통 카드 ── */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:16px 20px;margin-bottom:14px}
.card-title{font-size:16px;font-weight:700;color:#fbbf24;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.divider{height:1px;background:rgba(255,255,255,.08);margin:12px 0}

/* ── 컨트롤 슬라이더 ── */
.ctrl-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:500px){.ctrl-grid{grid-template-columns:1fr}}
.ctrl-group{display:flex;flex-direction:column;gap:6px}
.ctrl-label{font-size:14px;color:#94a3b8;font-weight:600;display:flex;justify-content:space-between}
.ctrl-label .badge{background:linear-gradient(135deg,#f59e0b,#ef4444);border-radius:8px;padding:1px 12px;font-weight:900;font-size:16px;color:#1c1917}
.ctrl-label .badge-p{background:linear-gradient(135deg,#6366f1,#8b5cf6)}
input[type=range]{-webkit-appearance:none;height:7px;border-radius:4px;outline:none;width:100%;cursor:pointer}
.rn{background:linear-gradient(90deg,#f59e0b,#ef4444)}
.rp{background:linear-gradient(90deg,#6366f1,#8b5cf6)}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#fff;border:3px solid #f59e0b;cursor:pointer;box-shadow:0 0 10px rgba(245,158,11,.5)}
.rp::-webkit-slider-thumb{border-color:#8b5cf6;box-shadow:0 0 10px rgba(139,92,246,.5)}

/* ── 통계 칩 ── */
.stat-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}
.scard{flex:1;min-width:80px;background:rgba(0,0,0,.3);border-radius:12px;padding:10px 8px;text-align:center;border:1.5px solid rgba(255,255,255,.08)}
.scard.sc-mean{border-color:rgba(245,158,11,.5);background:rgba(245,158,11,.07)}
.scard.sc-var {border-color:rgba(99,102,241,.5);background:rgba(99,102,241,.07)}
.scard.sc-sig {border-color:rgba(16,185,129,.5);background:rgba(16,185,129,.07)}
.scard.sc-q   {border-color:rgba(244,114,182,.5);background:rgba(244,114,182,.07)}
.sv{font-size:22px;font-weight:900;transition:all .3s}
.sc-mean .sv{color:#fbbf24}
.sc-var  .sv{color:#a5b4fc}
.sc-sig  .sv{color:#6ee7b7}
.sc-q    .sv{color:#f9a8d4}
.sl{font-size:11px;color:#64748b;font-weight:600;margin-top:3px;text-transform:uppercase;letter-spacing:.04em}

/* ── 캔버스 차트 ── */
#chartWrap{width:100%;position:relative;height:240px;margin-top:8px}
#mainChart{width:100%;height:240px;display:block}
.chart-note{font-size:11px;color:#475569;text-align:center;margin-top:4px}

/* ── 범위 계산기 ── */
.range-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;align-items:end}
@media(max-width:500px){.range-grid{grid-template-columns:1fr 1fr}}
.num-group{display:flex;flex-direction:column;gap:5px}
.num-group label{font-size:13px;color:#94a3b8;font-weight:600}
.num-input{background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.15);border-radius:10px;padding:8px 12px;font-size:16px;color:#e2e8f0;width:100%;outline:none;transition:.2s;text-align:center}
.num-input:focus{border-color:#6366f1;background:rgba(99,102,241,.1)}
.calc-btn{background:linear-gradient(135deg,#6366f1,#8b5cf6);border:none;border-radius:10px;padding:10px;font-size:14px;font-weight:800;color:#fff;cursor:pointer;width:100%;transition:.2s;letter-spacing:.02em}
.calc-btn:hover{filter:brightness(1.1);transform:translateY(-1px)}
.prob-result{margin-top:12px;background:rgba(99,102,241,.12);border:1.5px solid rgba(99,102,241,.3);border-radius:14px;padding:14px 18px;text-align:center;min-height:50px}
.prob-big{font-size:28px;font-weight:900;color:#a5b4fc}
.prob-sub{font-size:13px;color:#64748b;margin-top:4px}
.prob-formula{font-size:14px;color:#94a3b8;margin-top:6px}

/* ── 확률분포표 ── */
.table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:13px}
th{background:rgba(99,102,241,.2);color:#a5b4fc;padding:7px 6px;text-align:center;border:1px solid rgba(255,255,255,.08);white-space:nowrap;font-size:13px;font-weight:700}
td{padding:6px 5px;text-align:center;border:1px solid rgba(255,255,255,.05);color:#e2e8f0;font-size:13px;transition:all .2s}
tr.hl-range td{background:rgba(99,102,241,.18)!important;color:#c4b5fd!important;font-weight:700}
tr.hl-mode td{background:rgba(245,158,11,.15)!important;color:#fde68a!important}
tr:hover td{background:rgba(255,255,255,.04)}
.td-x{font-weight:700;color:#94a3b8}
.td-prob{color:#e2e8f0}
.td-cum{color:#6ee7b7}
.td-bar{text-align:left;padding:4px 8px}
.mini-bar{height:10px;border-radius:3px;background:linear-gradient(90deg,#6366f1,#8b5cf6);min-width:2px;transition:width .35s ease}

/* ── 분석 패널 ── */
.analysis-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:480px){.analysis-grid{grid-template-columns:1fr}}
.acard{background:rgba(0,0,0,.25);border-radius:12px;padding:12px 14px;border:1px solid rgba(255,255,255,.07)}
.acard-title{font-size:12px;color:#64748b;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}
.acard-val{font-size:18px;font-weight:800;color:#e2e8f0;line-height:1.3}
.acard-sub{font-size:12px;color:#64748b;margin-top:4px;line-height:1.5}
.tag{display:inline-block;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:700;margin-right:4px;margin-top:4px}
.tag-sym{background:rgba(16,185,129,.2);color:#6ee7b7;border:1px solid rgba(16,185,129,.3)}
.tag-right{background:rgba(245,158,11,.2);color:#fbbf24;border:1px solid rgba(245,158,11,.3)}
.tag-left{background:rgba(239,68,68,.2);color:#fca5a5;border:1px solid rgba(239,68,68,.3)}
.tag-info{background:rgba(99,102,241,.2);color:#a5b4fc;border:1px solid rgba(99,102,241,.3)}

/* ── 애니메이션 ── */
@keyframes pop{0%{transform:scale(.8);opacity:0}60%{transform:scale(1.12)}100%{transform:scale(1);opacity:1}}
.pop{animation:pop .35s ease forwards}

::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(99,102,241,.4);border-radius:3px}
</style>
</head>
<body>

<!-- ① 컨트롤 + 통계 -->
<div class="card">
  <div class="card-title">⚙️ 이항분포 B(n, p) 설정</div>
  <div class="ctrl-grid">
    <div class="ctrl-group">
      <div class="ctrl-label">시행 횟수 <strong>n</strong> <span class="badge" id="dispN">10</span></div>
      <input type="range" id="rN" class="rn" min="1" max="30" value="10" step="1">
    </div>
    <div class="ctrl-group">
      <div class="ctrl-label">성공 확률 <strong>p</strong> <span class="badge badge-p" id="dispP">0.40</span></div>
      <input type="range" id="rP" class="rp" min="1" max="99" value="40" step="1">
    </div>
  </div>
  <div class="divider"></div>
  <div class="stat-row">
    <div class="scard sc-mean"><div class="sv" id="sMean">—</div><div class="sl">평균 E(X) = np</div></div>
    <div class="scard sc-var" ><div class="sv" id="sVar" >—</div><div class="sl">분산 V(X) = npq</div></div>
    <div class="scard sc-sig" ><div class="sv" id="sSig" >—</div><div class="sl">표준편차 σ(X)</div></div>
    <div class="scard sc-q"   ><div class="sv" id="sQ"   >—</div><div class="sl">q = 1 − p</div></div>
  </div>
</div>

<!-- ② 그래프 -->
<div class="card">
  <div class="card-title">📊 이항분포 그래프 (막대그래프)</div>
  <div id="chartWrap"><canvas id="mainChart"></canvas></div>
  <div class="chart-note">🟡 점선 = 평균(μ)&ensp;|&ensp;🟢 영역 = μ ± σ&ensp;|&ensp;🔵 일반 막대&ensp;|&ensp;🟣 범위 선택 막대</div>
</div>

<!-- ③ P(a≤X≤b) 계산기 -->
<div class="card">
  <div class="card-title">🧮 범위 확률 계산기 &nbsp;<span style="font-size:13px;color:#64748b;font-weight:400">P(a ≤ X ≤ b)</span></div>
  <div class="range-grid">
    <div class="num-group">
      <label>a (하한)</label>
      <input type="number" id="inputA" class="num-input" min="0" value="0">
    </div>
    <div class="num-group">
      <label>b (상한)</label>
      <input type="number" id="inputB" class="num-input" min="0" value="10">
    </div>
    <div class="num-group">
      <button class="calc-btn" onclick="calcRange()">▶ 계산하기</button>
    </div>
  </div>
  <div class="prob-result" id="probResult">
    <div style="color:#475569;font-size:14px">a, b 값을 입력하고 계산하기를 눌러주세요.</div>
  </div>
</div>

<!-- ④ 확률분포표 -->
<div class="card">
  <div class="card-title">📋 확률분포표</div>
  <div class="table-wrap">
    <table id="distTable">
      <thead>
        <tr>
          <th>X</th>
          <th>P(X=x)</th>
          <th>누적 F(x)</th>
          <th>상대 막대</th>
        </tr>
      </thead>
      <tbody id="distBody"></tbody>
    </table>
  </div>
  <div style="font-size:12px;color:#475569;margin-top:8px">
    🟡 주황색 행 = 최빈값(mode) &ensp;|&ensp; 🟣 보라색 행 = 선택된 P(a≤X≤b) 범위
  </div>
</div>

<!-- ⑤ 분포 분석 -->
<div class="card">
  <div class="card-title">🔍 분포 분석 리포트</div>
  <div class="analysis-grid" id="analysisGrid"></div>
</div>

<script>
// ──────────────────────────────────────────────
// 유틸
// ──────────────────────────────────────────────
function comb(n, k) {
  if (k < 0 || k > n) return 0;
  if (k === 0 || k === n) return 1;
  let r = 1;
  for (let i = 0; i < Math.min(k, n - k); i++) r = r * (n - i) / (i + 1);
  return r;
}
function pmf(n, p, k) {
  return comb(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
}
function roundN(v, d) { return +v.toFixed(d); }
function animPop(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');
}

// ──────────────────────────────────────────────
// 상태
// ──────────────────────────────────────────────
let curN = 10, curP = 0.4;
let rangeA = null, rangeB = null;

// ──────────────────────────────────────────────
// PMF 배열 생성
// ──────────────────────────────────────────────
function buildPMF(n, p) {
  const arr = [];
  for (let k = 0; k <= n; k++) arr.push(pmf(n, p, k));
  return arr;
}

// ──────────────────────────────────────────────
// 캔버스 차트
// ──────────────────────────────────────────────
function drawChart(n, p, probs, a, b) {
  const canvas = document.getElementById('mainChart');
  const wrap   = document.getElementById('chartWrap');
  const W = wrap.clientWidth || 600, H = 240;
  canvas.width = W; canvas.height = H;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, W, H);

  const mean = n * p, sigma = Math.sqrt(n * p * (1 - p));
  const maxP = Math.max(...probs);
  const xMin = 0, xMax = n, cnt = n + 1;

  const padL = 38, padR = 14, padT = 20, padB = 36;
  const plotW = W - padL - padR, plotH = H - padT - padB;
  const bw    = Math.max(2, plotW / cnt - 3);
  const xPos  = k => padL + (k + 0.5) * (plotW / cnt);

  // μ±σ 배경
  ctx.fillStyle = 'rgba(16,185,129,.07)';
  const lx = padL + Math.max(0, mean - sigma) * (plotW / cnt);
  const rx = padL + Math.min(n, mean + sigma) * (plotW / cnt) + plotW / cnt;
  ctx.fillRect(lx, padT, rx - lx, plotH);

  // y축 눈금
  const nTicks = 4;
  ctx.fillStyle = '#334155'; ctx.font = '10px sans-serif'; ctx.textAlign = 'right';
  for (let i = 0; i <= nTicks; i++) {
    const v = (maxP * i / nTicks);
    const y = padT + plotH * (1 - i / nTicks);
    ctx.fillStyle = '#334155';
    ctx.beginPath(); ctx.moveTo(padL - 3, y); ctx.lineTo(padL + plotW, y);
    ctx.strokeStyle = 'rgba(255,255,255,.05)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = '#475569'; ctx.fillText((v * 100).toFixed(1) + '%', padL - 5, y + 4);
  }

  // 막대
  for (let k = 0; k <= n; k++) {
    const bh  = plotH * (probs[k] / maxP);
    const bx  = xPos(k) - bw / 2;
    const by  = padT + plotH - bh;
    const inR = (a !== null && b !== null && k >= a && k <= b);

    let grad;
    if (inR) {
      grad = ctx.createLinearGradient(0, by, 0, by + bh);
      grad.addColorStop(0, 'rgba(139,92,246,.95)');
      grad.addColorStop(1, 'rgba(99,102,241,.7)');
    } else {
      grad = ctx.createLinearGradient(0, by, 0, by + bh);
      grad.addColorStop(0, 'rgba(59,130,246,.9)');
      grad.addColorStop(1, 'rgba(37,99,235,.6)');
    }
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.roundRect(bx, by, bw, bh, Math.min(4, bw * 0.3));
    ctx.fill();

    // 확률값 텍스트 (짧은 경우만)
    if (n <= 20 && bh > 20) {
      ctx.fillStyle = 'rgba(255,255,255,.7)';
      ctx.font = '9px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText((probs[k] * 100).toFixed(1) + '%', xPos(k), by - 3);
    }
  }

  // 평균 점선
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2.5; ctx.setLineDash([6, 4]);
  const mx = xPos(mean);
  ctx.beginPath(); ctx.moveTo(mx, padT); ctx.lineTo(mx, padT + plotH); ctx.stroke();
  ctx.setLineDash([]);

  // 평균 레이블
  ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 11px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText('μ=' + mean.toFixed(2), mx, padT - 4);

  // x축 레이블
  ctx.fillStyle = '#64748b'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
  const step = n > 20 ? Math.ceil(n / 15) : 1;
  for (let k = 0; k <= n; k += step) {
    ctx.fillText(k, xPos(k), H - padB + 16);
  }

  // x축 선
  ctx.strokeStyle = 'rgba(255,255,255,.15)'; ctx.lineWidth = 1; ctx.setLineDash([]);
  ctx.beginPath(); ctx.moveTo(padL, padT + plotH); ctx.lineTo(padL + plotW, padT + plotH); ctx.stroke();

  // x축 제목
  ctx.fillStyle = '#475569'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText('← 성공 횟수 X →', padL + plotW / 2, H - 4);
}

// ──────────────────────────────────────────────
// 확률분포표
// ──────────────────────────────────────────────
function buildTable(n, p, probs, modeK, a, b) {
  const tbody = document.getElementById('distBody');
  tbody.innerHTML = '';
  const maxProb = Math.max(...probs);
  let cum = 0;
  for (let k = 0; k <= n; k++) {
    cum += probs[k];
    const tr = document.createElement('tr');
    const inRange = (a !== null && b !== null && k >= a && k <= b);
    const isMode  = (probs[k] >= maxProb - 1e-10);
    if (inRange) tr.classList.add('hl-range');
    else if (isMode) tr.classList.add('hl-mode');

    const barW = Math.round((probs[k] / maxProb) * 120);
    tr.innerHTML = `
      <td class="td-x">${k}</td>
      <td class="td-prob">${(probs[k] * 100).toFixed(4)}%</td>
      <td class="td-cum">${(Math.min(cum, 1) * 100).toFixed(3)}%</td>
      <td class="td-bar"><div class="mini-bar" style="width:${barW}px"></div></td>`;
    tbody.appendChild(tr);
  }
}

// ──────────────────────────────────────────────
// 분석 리포트
// ──────────────────────────────────────────────
function buildAnalysis(n, p, probs) {
  const q     = 1 - p;
  const mean  = n * p;
  const vari  = n * p * q;
  const sigma = Math.sqrt(vari);
  const maxP  = Math.max(...probs);
  const modeK = probs.indexOf(maxP);

  // 왜도 방향
  const skew = (p < 0.5) ? '오른쪽 꼬리 (right-skewed)' :
               (p > 0.5) ? '왼쪽 꼬리 (left-skewed)' : '대칭 (symmetric, p=0.5)';
  const skewTag = (p < 0.5) ? 'tag-right' : (p > 0.5) ? 'tag-left' : 'tag-sym';

  // μ ± σ 범위
  const lo1 = Math.max(0, Math.ceil(mean - sigma));
  const hi1 = Math.min(n, Math.floor(mean + sigma));
  let probSig1 = 0;
  for (let k = lo1; k <= hi1; k++) probSig1 += probs[k];

  const lo2 = Math.max(0, Math.ceil(mean - 2 * sigma));
  const hi2 = Math.min(n, Math.floor(mean + 2 * sigma));
  let probSig2 = 0;
  for (let k = lo2; k <= hi2; k++) probSig2 += probs[k];

  // 집중도 (변동계수 역수)
  const cv = sigma / mean;
  const conc = cv < 0.2 ? '매우 집중' : cv < 0.4 ? '집중' : cv < 0.7 ? '보통' : '분산';

  // 최빈값이 여러 개인지
  const modes = probs.reduce((acc, v, i) => { if (v >= maxP - 1e-10) acc.push(i); return acc; }, []);

  // 비대칭도(피어슨)
  const pearson = (mean - modeK) / sigma;

  const items = [
    {
      title: '최빈값 (mode)',
      val: modes.length > 1 ? modes.join(', ') : modeK,
      sub: `P(X=${modeK}) = ${(maxP * 100).toFixed(3)}%가 가장 높습니다.`
    },
    {
      title: '분포 형태',
      val: `<span class="tag ${skewTag}">${p < 0.5 ? '우편포' : p > 0.5 ? '좌편포' : '대칭'}</span>`,
      sub: skew
    },
    {
      title: 'P(μ−σ ≤ X ≤ μ+σ)',
      val: (probSig1 * 100).toFixed(2) + '%',
      sub: `X가 ${lo1} ~ ${hi1} 범위에 있을 확률 (약 68% 기대)`
    },
    {
      title: 'P(μ−2σ ≤ X ≤ μ+2σ)',
      val: (probSig2 * 100).toFixed(2) + '%',
      sub: `X가 ${lo2} ~ ${hi2} 범위에 있을 확률 (약 95% 기대)`
    },
    {
      title: '집중도 (CV⁻¹)',
      val: `<span class="tag tag-info">${conc}</span>`,
      sub: `변동계수 σ/μ = ${cv.toFixed(3)} → 평균 대비 퍼진 정도`
    },
    {
      title: '피어슨 비대칭도',
      val: pearson.toFixed(3),
      sub: `(μ − mode) / σ ≈ 0이면 대칭, 양수면 우편포, 음수면 좌편포`
    },
    {
      title: '중앙값 근사',
      val: `≈ ${Math.floor(n * p + p > 0.5 ? 0 : -0) } ~ ${Math.ceil(n * p + (1-p))}`,
      sub: `이항분포의 중앙값은 floor(np) 또는 ceil(np) 사이에 있습니다.`
    },
    {
      title: 'X=0 확률 (전체 실패)',
      val: (probs[0] * 100).toFixed(4) + '%',
      sub: `n번 모두 실패할 확률 = q^n = ${q.toFixed(3)}^${n}`
    },
    {
      title: `X=${n} 확률 (전체 성공)`,
      val: (probs[n] * 100).toFixed(4) + '%',
      sub: `n번 모두 성공할 확률 = p^n = ${p.toFixed(3)}^${n}`
    },
    {
      title: '정규분포 근사 적합성',
      val: (n * p >= 5 && n * q >= 5)
        ? '<span class="tag tag-sym">근사 가능 ✓</span>'
        : '<span class="tag tag-left">근사 불충분 ✗</span>',
      sub: `np=${(n*p).toFixed(1)}, nq=${(n*q).toFixed(1)} — np≥5 이고 nq≥5 이면 정규근사 권장`
    },
  ];

  const grid = document.getElementById('analysisGrid');
  grid.innerHTML = '';
  items.forEach(item => {
    const d = document.createElement('div');
    d.className = 'acard';
    d.innerHTML = `
      <div class="acard-title">${item.title}</div>
      <div class="acard-val">${item.val}</div>
      <div class="acard-sub">${item.sub}</div>`;
    grid.appendChild(d);
  });
}

// ──────────────────────────────────────────────
// 메인 업데이트
// ──────────────────────────────────────────────
function update() {
  const n = curN, p = curP, q = 1 - p;
  const mean = n * p, vari = n * p * q, sigma = Math.sqrt(vari);
  const probs = buildPMF(n, p);
  const modeK = probs.indexOf(Math.max(...probs));

  // 통계 칩
  document.getElementById('dispN').textContent = n;
  document.getElementById('dispP').textContent = p.toFixed(2);
  ['sMean','sVar','sSig','sQ'].forEach(id => {
    const el = document.getElementById(id);
    const val = id==='sMean' ? mean.toFixed(3)
              : id==='sVar'  ? vari.toFixed(3)
              : id==='sSig'  ? sigma.toFixed(4)
              :                q.toFixed(3);
    el.textContent = val;
    el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');
  });

  // a, b 범위 입력 상한 조정
  document.getElementById('inputA').max = n;
  document.getElementById('inputB').max = n;
  if (+document.getElementById('inputB').value > n)
    document.getElementById('inputB').value = n;

  // 그래프
  drawChart(n, p, probs, rangeA, rangeB);

  // 분포표
  buildTable(n, p, probs, modeK, rangeA, rangeB);

  // 분석
  buildAnalysis(n, p, probs);
}

// ──────────────────────────────────────────────
// 범위 확률 계산
// ──────────────────────────────────────────────
function calcRange() {
  const n = curN, p = curP;
  const a = parseInt(document.getElementById('inputA').value);
  const b = parseInt(document.getElementById('inputB').value);

  if (isNaN(a) || isNaN(b) || a < 0 || b > n || a > b) {
    document.getElementById('probResult').innerHTML =
      `<div style="color:#f87171;font-size:14px">⚠ 올바른 범위를 입력해주세요. (0 ≤ a ≤ b ≤ ${n})</div>`;
    return;
  }

  rangeA = a; rangeB = b;
  const probs = buildPMF(n, p);
  let prob = 0;
  for (let k = a; k <= b; k++) prob += probs[k];

  const terms = [];
  for (let k = a; k <= Math.min(b, a + 4); k++) {
    terms.push(`P(X=${k}) = ${(probs[k]*100).toFixed(3)}%`);
  }
  if (b - a > 4) terms.push('...');

  document.getElementById('probResult').innerHTML = `
    <div class="prob-big">P(${a} ≤ X ≤ ${b}) = <span style="color:#c4b5fd">${(prob*100).toFixed(4)}%</span></div>
    <div class="prob-big" style="font-size:16px;margin-top:6px;color:#a5b4fc">≈ ${prob.toFixed(6)}</div>
    <div class="prob-formula">${terms.join(' + ')}</div>
    <div class="prob-sub">n=${n}, p=${p.toFixed(2)}의 이항분포 B(${n}, ${p.toFixed(2)})에서</div>`;

  // 그래프·분포표 재그리기 (범위 반영)
  drawChart(n, p, probs, a, b);
  buildTable(n, p, probs, probs.indexOf(Math.max(...probs)), a, b);
}

// ──────────────────────────────────────────────
// 이벤트 바인딩
// ──────────────────────────────────────────────
document.getElementById('rN').addEventListener('input', e => {
  curN = +e.target.value;
  rangeA = null; rangeB = null;
  document.getElementById('inputB').value = curN;
  update();
});
document.getElementById('rP').addEventListener('input', e => {
  curP = +e.target.value / 100;
  rangeA = null; rangeB = null;
  update();
});
document.getElementById('inputA').addEventListener('keydown', e => { if(e.key==='Enter') calcRange(); });
document.getElementById('inputB').addEventListener('keydown', e => { if(e.key==='Enter') calcRange(); });

window.addEventListener('resize', () => {
  const probs = buildPMF(curN, curP);
  drawChart(curN, curP, probs, rangeA, rangeB);
});

// 초기화
update();
</script>
</body>
</html>
"""


def render():
    st.header("📈 이항분포 그래프 시뮬레이터")
    components.html(_HTML, height=2400, scrolling=False)
