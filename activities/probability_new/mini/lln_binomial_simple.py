import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🔬 큰 수의 법칙 탐구",
    "description": "동전 던지기 시뮬레이션으로 n이 커질수록 상대도수 X/n이 수학적 확률 p에 가까워지는 큰 수의 법칙을 궤적으로 직접 체험합니다.",
    "order": 66,
}

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "큰수의법칙탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 큰 수의 법칙 – 성찰 질문**"},
    {
        "key": "수식의미",
        "label": "큰 수의 법칙 lim(n→∞) P(|X/n − p| < h) = 1 이 무엇을 뜻하는지, 시뮬레이션 경험을 바탕으로 설명해보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "n이 커질수록 상대도수 X/n이 수학적 확률 p 로부터 h 이상 벗어날 확률이..."
    },
    {
        "key": "h역할",
        "label": "h(허용 오차) 값을 크게/작게 바꿨을 때 '범위 안 비율'이 어떻게 달라졌나요? 왜 그런 결과가 나왔는지 설명하세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "h가 클수록 / 작을수록..."
    },
    {
        "key": "n과비율",
        "label": "n(시행 횟수)을 20 → 100 → 300 → 500으로 바꿔가며 실험했을 때, '범위 안 비율'의 변화 추세를 설명하세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "n이 작을 때는 경로들이 ... n이 커질수록 ..."
    },
    {
        "key": "실생활연결",
        "label": "큰 수의 법칙이 실생활에서 활용되는 사례를 2가지 이상 써보세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) 보험료 산정 시... / 여론조사에서..."
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",         "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]


_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:#060b14;color:#e2e8f0;
  padding:10px 12px 12px;
}

/* ── 헤더 ── */
.hdr{
  text-align:center;padding:10px 16px 8px;
  background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(6,182,212,.12));
  border:1px solid rgba(99,102,241,.3);border-radius:16px;margin-bottom:10px;
}
.hdr h1{
  font-size:1.1rem;font-weight:900;
  background:linear-gradient(135deg,#a5b4fc,#22d3ee);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px;
}
.formula-box{
  display:inline-block;
  border:2px solid rgba(253,224,71,.45);border-radius:9px;
  background:rgba(0,0,0,.35);padding:5px 18px 7px;margin-bottom:4px;
}
.fdesc{font-size:.7rem;color:#94a3b8;margin-bottom:3px;line-height:1.5;}
.fmain{font-size:.95rem;font-style:italic;color:#fde68a;letter-spacing:.02em;}
.hdr .note{font-size:.65rem;color:#64748b;margin-top:3px;}

/* ── 2단 레이아웃 ── */
.layout{display:grid;grid-template-columns:200px 1fr;gap:10px;margin-bottom:8px;}
@media(max-width:560px){.layout{grid-template-columns:1fr;}}

/* ── 기호 카드 ── */
.sym-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;margin-bottom:8px;}
.sc{padding:5px 4px;border-radius:7px;text-align:center;border-left:3px solid;}
.sc-p {background:rgba(245,158,11,.08);border-color:#f59e0b;}
.sc-xn{background:rgba(6,182,212,.08); border-color:#06b6d4;}
.sc-h {background:rgba(167,139,250,.08);border-color:#a78bfa;}
.sv{font-size:.9rem;font-weight:900;}
.sc-p .sv{color:#fbbf24;}.sc-xn .sv{color:#22d3ee;}.sc-h .sv{color:#c4b5fd;}
.sd{font-size:.58rem;color:#94a3b8;margin-top:1px;line-height:1.3;}

/* ── 슬라이더 ── */
.pg{margin-bottom:7px;}
.pl{font-size:.72rem;color:#94a3b8;font-weight:700;display:flex;justify-content:space-between;align-items:center;margin-bottom:2px;}
.pv{font-size:.88rem;font-weight:900;padding:1px 7px;border-radius:5px;min-width:38px;text-align:center;}
.pv-p{background:rgba(245,158,11,.15);color:#fbbf24;}
.pv-h{background:rgba(167,139,250,.15);color:#c4b5fd;}
.pv-n{background:rgba(6,182,212,.15);color:#22d3ee;}
.pv-m{background:rgba(34,197,94,.15);color:#4ade80;}
input[type=range]{-webkit-appearance:none;height:5px;border-radius:4px;outline:none;width:100%;cursor:pointer;}
.r-p{background:linear-gradient(90deg,#f59e0b,#ef4444);}
.r-h{background:linear-gradient(90deg,#8b5cf6,#a78bfa);}
.r-n{background:linear-gradient(90deg,#0891b2,#06b6d4);}
.r-m{background:linear-gradient(90deg,#16a34a,#22c55e);}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#fff;cursor:pointer;}

/* ── 버튼 / 진행 ── */
.btn-run{
  width:100%;padding:9px;border:none;border-radius:10px;
  background:linear-gradient(135deg,#4f46e5,#06b6d4);
  color:#fff;font-size:.85rem;font-weight:800;cursor:pointer;transition:all .18s;
  margin-top:6px;
}
.btn-run:hover{filter:brightness(1.15);transform:translateY(-1px);}
.btn-run:disabled{opacity:.4;cursor:not-allowed;transform:none;}
.prog-wrap{height:4px;background:rgba(0,0,0,.3);border-radius:100px;overflow:hidden;margin-top:5px;display:none;}
.prog-bar{height:100%;background:linear-gradient(90deg,#6366f1,#06b6d4);width:0%;transition:width .08s;}

/* ── 결과 요약 ── */
.res-cards{display:none;grid-template-columns:1fr 1fr;gap:5px;margin-top:7px;}
.rcard{background:rgba(0,0,0,.3);border:1.5px solid rgba(255,255,255,.07);border-radius:8px;padding:6px;text-align:center;}
.rcard.hl{border-color:rgba(99,102,241,.5);background:rgba(99,102,241,.08);}
.rcard-lbl{font-size:.58rem;color:#64748b;font-weight:700;letter-spacing:.04em;text-transform:uppercase;}
.rcard-val{font-size:1.25rem;font-weight:900;line-height:1.1;margin:2px 0;}
.rcard-sub{font-size:.58rem;color:#475569;}
.rv-in{color:#4ade80;}.rv-rat{background:linear-gradient(135deg,#a5b4fc,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}

/* ── 차트 ── */
.chart-wrap{background:rgba(0,0,0,.3);border-radius:12px;overflow:hidden;height:320px;position:relative;}
canvas{display:block;width:100%;height:100%;}
.legend{display:none;flex-wrap:wrap;gap:8px;padding:5px 8px;font-size:.68rem;color:#94a3b8;background:rgba(255,255,255,.03);border-radius:8px;margin-top:5px;}
.li{display:flex;align-items:center;gap:4px;}
.ld-p{width:20px;height:0;border-top:2px dashed #fbbf24;}
.ld-band{width:18px;height:9px;border-radius:3px;background:rgba(139,92,246,.35);border:1px solid rgba(167,139,250,.5);}

/* ── 반복별 테이블 ── */
.tbl-card{display:none;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:10px 12px;margin-top:8px;}
.tbl-title{font-size:.8rem;font-weight:800;margin-bottom:6px;color:#e2e8f0;}
.tbl-sub{font-size:.68rem;color:#64748b;margin-bottom:8px;line-height:1.5;}
.tbl-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;}
table{border-collapse:collapse;font-size:.7rem;}
th{background:rgba(99,102,241,.15);color:#a5b4fc;padding:5px 7px;text-align:center;border:1px solid rgba(255,255,255,.07);font-weight:700;white-space:nowrap;}
td{padding:4px 6px;text-align:center;border:1px solid rgba(255,255,255,.05);color:#cbd5e1;min-width:44px;}
.td-rep{color:#22d3ee;font-weight:700;white-space:nowrap;}
.td-in{background:rgba(34,197,94,.18) !important;color:#4ade80;font-weight:700;}
.td-out{background:rgba(248,113,113,.1) !important;color:#f87171;}
.td-crit{background:rgba(253,224,71,.22) !important;color:#fde68a;font-weight:800;outline:2px solid rgba(253,224,71,.5);outline-offset:-2px;}

/* 인사이트 */
.insight{display:none;background:linear-gradient(135deg,rgba(99,102,241,.08),rgba(6,182,212,.08));border:1px solid rgba(99,102,241,.25);border-radius:9px;padding:8px 12px;font-size:.75rem;line-height:1.7;color:#c7d2fe;margin-top:8px;}
.insight strong{color:#a5b4fc;}

@keyframes fadeUp{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}
.fu{animation:fadeUp .35s ease forwards;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.4;}}
.pulsing{animation:pulse 1.1s ease infinite;}
</style>
</head>
<body>

<!-- 헤더 -->
<div class="hdr">
  <h1>🔬 큰 수의 법칙 탐구</h1>
  <div class="formula-box">
    <div class="fdesc">사건 A의 확률이 <i>p</i>일 때, <i>n</i>번 독립시행에서 A가 일어난 횟수를 <i>X</i>라 하면,<br>임의의 양수 <i>h</i>에 대하여</div>
    <div class="fmain">lim<sub>n→∞</sub> P(&thinsp;|&thinsp;<sup>X</sup>/<sub>n</sub>&thinsp;−&thinsp;p&thinsp;|&thinsp;&lt;&thinsp;h&thinsp;)&thinsp;=&thinsp;1</div>
  </div>
  <div class="note">X/n : 상대도수(통계적 확률) &nbsp;·&nbsp; p : 수학적 확률 &nbsp;·&nbsp; h : 임의의 양수</div>
</div>

<!-- 2단 -->
<div class="layout">

  <!-- 왼쪽 컨트롤 -->
  <div>
    <div class="sym-row">
      <div class="sc sc-p"><div class="sv">p</div><div class="sd">수학적<br>확률</div></div>
      <div class="sc sc-xn"><div class="sv">X/n</div><div class="sd">상대도수<br>(실험값)</div></div>
      <div class="sc sc-h"><div class="sv">h</div><div class="sd">허용<br>오차</div></div>
    </div>

    <div class="pg">
      <div class="pl">수학적 확률 <i>p</i> <span class="pv pv-p" id="lbl-p">0.50</span></div>
      <input type="range" class="r-p" id="sl-p" min="10" max="90" value="50" step="5">
    </div>
    <div class="pg">
      <div class="pl">허용 오차 <i>h</i> <span class="pv pv-h" id="lbl-h">0.10</span></div>
      <input type="range" class="r-h" id="sl-h" min="2" max="30" value="10" step="1">
    </div>
    <div class="pg">
      <div class="pl">시행 횟수 <i>n</i> <span class="pv pv-n" id="lbl-n">100</span></div>
      <input type="range" class="r-n" id="sl-n" min="10" max="500" value="100" step="5">
    </div>
    <div class="pg">
      <div class="pl">반복 횟수 <i>m</i> <span class="pv pv-m" id="lbl-m">15</span></div>
      <input type="range" class="r-m" id="sl-m" min="1" max="30" value="15" step="1">
    </div>

    <button class="btn-run" id="btn-run" onclick="runSim()">▶ 시뮬레이션 실행</button>
    <div class="prog-wrap" id="prog-wrap"><div class="prog-bar" id="prog-bar"></div></div>

    <div class="res-cards" id="res-cards">
      <div class="rcard">
        <div class="rcard-lbl">h 안 반복</div>
        <div class="rcard-val rv-in" id="res-in">—</div>
        <div class="rcard-sub">/ <span id="res-tot">—</span> 회</div>
      </div>
      <div class="rcard hl">
        <div class="rcard-lbl">범위 안 비율</div>
        <div class="rcard-val rv-rat" id="res-rat">—</div>
        <div class="rcard-sub">≈ P(|X/n−p|&lt;h)</div>
      </div>
    </div>
  </div>

  <!-- 오른쪽 차트 -->
  <div>
    <div class="chart-wrap"><canvas id="mainChart"></canvas></div>
    <div class="legend" id="legend">
      <div class="li"><div class="ld-p"></div>수학적 확률 p</div>
      <div class="li"><div class="ld-band"></div>±h 허용 범위</div>
      <div class="li" style="color:#94a3b8;">각 색상 = 반복 1회 (X/n 궤적)</div>
    </div>
  </div>
</div>

<!-- 반복별 테이블 -->
<div class="tbl-card" id="tbl-card">
  <div class="tbl-title">📋 반복별 상대도수 X/n 기록</div>
  <div class="tbl-sub">
    각 셀: 해당 시행 횟수 k에서의 상대도수 X<sub>k</sub>/k &nbsp;|&nbsp;
    <span style="color:#4ade80;font-weight:700;">■ 초록</span> = h 범위 안 (|X/n−p| &lt; h) &nbsp;|&nbsp;
    <span style="color:#f87171;font-weight:700;">■ 빨강</span> = 범위 밖 &nbsp;|&nbsp;
    <span style="color:#fde68a;font-weight:700;">★ 노랑 테두리</span> = 처음으로 범위 안 진입한 n 값
  </div>
  <div class="tbl-scroll"><table id="sim-table"></table></div>
  <div class="insight" id="insight"></div>
</div>

<script>
// ── 색상 팔레트 (m 최대 30) ──
function getColor(i, m, alpha) {
  const hue = (i / Math.max(m - 1, 1)) * 300; // 0(빨강)~300(보라) HSL
  return `hsla(${hue},85%,65%,${alpha})`;
}

// ── 슬라이더 바인딩 ──
function bind(id, lbl, fmt) {
  const sl = document.getElementById(id);
  const lb = document.getElementById(lbl);
  sl.addEventListener('input', () => lb.textContent = fmt(+sl.value));
}
bind('sl-p', 'lbl-p', v => (v/100).toFixed(2));
bind('sl-h', 'lbl-h', v => (v/100).toFixed(2));
bind('sl-n', 'lbl-n', v => v);
bind('sl-m', 'lbl-m', v => v);

// ── 시뮬레이션 ──
function runSim() {
  const p = +document.getElementById('sl-p').value / 100;
  const h = +document.getElementById('sl-h').value / 100;
  const n = +document.getElementById('sl-n').value;
  const m = +document.getElementById('sl-m').value;

  const btn = document.getElementById('btn-run');
  btn.disabled = true; btn.textContent = '⏳ 계산 중…'; btn.classList.add('pulsing');
  const pw = document.getElementById('prog-wrap'), pb = document.getElementById('prog-bar');
  pw.style.display = 'block'; pb.style.width = '0%';

  setTimeout(() => {
    const paths = [];
    let inside = 0;
    for (let i = 0; i < m; i++) {
      let heads = 0;
      const path = new Float32Array(n);
      for (let k = 0; k < n; k++) {
        if (Math.random() < p) heads++;
        path[k] = heads / (k + 1);
      }
      paths.push(path);
      if (Math.abs(path[n - 1] - p) < h) inside++;
      pb.style.width = ((i + 1) / m * 100) + '%';
    }
    const ratio = inside / m;

    // UI 업데이트
    const rc = document.getElementById('res-cards');
    rc.style.display = 'grid'; rc.classList.add('fu');
    document.getElementById('res-in').textContent  = inside;
    document.getElementById('res-tot').textContent = m;
    document.getElementById('res-rat').textContent = (ratio * 100).toFixed(1) + '%';
    document.getElementById('legend').style.display = 'flex';

    drawChart(paths, p, h, n, m);
    buildTable(paths, p, h, n, m);
    buildInsight(paths, p, h, n, m, inside, ratio);

    btn.disabled = false; btn.textContent = '▶ 시뮬레이션 실행'; btn.classList.remove('pulsing');
    setTimeout(() => { pw.style.display = 'none'; pb.style.width = '0%'; }, 400);
  }, 20);
}

// ── 차트 (각 반복 = 서로 다른 색상 궤적) ──
function drawChart(paths, p, h, n, m) {
  const canvas = document.getElementById('mainChart');
  const W = canvas.parentElement.clientWidth || 500;
  const H = 320;
  canvas.width = W; canvas.height = H;
  const ctx = canvas.getContext('2d');

  const PAD = {top:22, right:58, bottom:44, left:48};
  const cW = W - PAD.left - PAD.right;
  const cH = H - PAD.top  - PAD.bottom;

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = 'rgba(0,0,0,.2)'; ctx.fillRect(0, 0, W, H);

  function toX(k) { return PAD.left + (k / (n - 1 || 1)) * cW; }
  function toY(v) { return PAD.top  + (1 - Math.max(0, Math.min(1, v))) * cH; }

  // 격자
  ctx.strokeStyle = 'rgba(255,255,255,.055)'; ctx.lineWidth = 1;
  for (let v = 0; v <= 10; v += 2) {
    const yy = toY(v / 10);
    ctx.beginPath(); ctx.moveTo(PAD.left, yy); ctx.lineTo(PAD.left + cW, yy); ctx.stroke();
  }

  // ±h 띠
  const yTop = toY(Math.min(1, p + h)), yBot = toY(Math.max(0, p - h));
  ctx.fillStyle = 'rgba(99,102,241,.1)';
  ctx.fillRect(PAD.left, yTop, cW, yBot - yTop);
  ctx.strokeStyle = 'rgba(167,139,250,.5)'; ctx.lineWidth = 1; ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(PAD.left, yTop); ctx.lineTo(PAD.left+cW, yTop); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(PAD.left, yBot); ctx.lineTo(PAD.left+cW, yBot); ctx.stroke();
  ctx.setLineDash([]);

  // 각 반복 궤적 (고유 색상)
  const step = n > 200 ? Math.ceil(n / 200) : 1;
  for (let i = 0; i < m; i++) {
    const path  = paths[i];
    const color = getColor(i, m, 0.75);
    ctx.strokeStyle = color; ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(toX(0), toY(path[0]));
    for (let k = step; k < n; k += step) ctx.lineTo(toX(k), toY(path[k]));
    ctx.lineTo(toX(n - 1), toY(path[n - 1]));
    ctx.stroke();
    // 끝점 강조
    const isIn = Math.abs(path[n-1] - p) < h;
    ctx.beginPath();
    ctx.arc(toX(n-1), toY(path[n-1]), 4, 0, Math.PI*2);
    ctx.fillStyle = isIn ? 'rgba(74,222,128,.9)' : 'rgba(248,113,113,.9)';
    ctx.fill();
  }

  // p 기준선
  const yP = toY(p);
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2; ctx.setLineDash([7,4]);
  ctx.beginPath(); ctx.moveTo(PAD.left, yP); ctx.lineTo(PAD.left+cW, yP); ctx.stroke();
  ctx.setLineDash([]);

  // Y축 눈금
  ctx.fillStyle = '#64748b'; ctx.font = '11px Segoe UI'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
  for (let v = 0; v <= 10; v += 2) ctx.fillText((v/10).toFixed(1), PAD.left-5, toY(v/10));
  // Y축 제목
  ctx.save(); ctx.translate(13, PAD.top + cH/2); ctx.rotate(-Math.PI/2);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#94a3b8'; ctx.font = '11px Segoe UI';
  ctx.fillText('상대도수 X/n', 0, 0); ctx.restore();

  // X축 눈금
  ctx.fillStyle = '#64748b'; ctx.font = '11px Segoe UI'; ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  const ticks = n <= 50 ? [1,Math.round(n/4),Math.round(n/2),Math.round(3*n/4),n]
                        : [1,Math.round(n/4),Math.round(n/2),Math.round(3*n/4),n];
  ticks.forEach(k => {
    const xx = toX(k-1);
    ctx.fillText(k, xx, PAD.top+cH+5);
  });
  ctx.fillStyle = '#94a3b8'; ctx.font = '11px Segoe UI'; ctx.textBaseline = 'bottom';
  ctx.fillText('시행 횟수 n', PAD.left + cW/2, H - 3);

  // 우측 레이블
  ctx.fillStyle = '#fbbf24'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('p='+p.toFixed(2), PAD.left+cW+3, yP);
  ctx.fillStyle = '#a5b4fc'; ctx.font = '10px Segoe UI';
  ctx.fillText('p+h', PAD.left+cW+3, yTop);
  ctx.fillText('p−h', PAD.left+cW+3, yBot);
}

// ── 반복별 테이블 ──
function buildTable(paths, p, h, n, m) {
  document.getElementById('tbl-card').style.display = 'block';
  const table = document.getElementById('sim-table');

  // 표시할 n 체크포인트 (최대 12개 열)
  const checkpoints = makeCheckpoints(n, 12);

  // 헤더
  let thead = '<thead><tr><th>반복</th>';
  checkpoints.forEach(k => { thead += `<th>n=${k}</th>`; });
  thead += '<th>n=${n} 최종</th>'.replace('${n}', n);
  thead += '</tr></thead>';

  // 체크포인트별 범위 안 개수 누적용
  const colInCount = new Array(checkpoints.length + 1).fill(0);

  // 바디
  let tbody = '<tbody>';
  paths.forEach((path, i) => {
    const color = getColor(i, m, 1);
    tbody += `<tr><td class="td-rep" style="color:${color};">반복 ${i+1}</td>`;

    let firstIn = -1;
    for (let ci = 0; ci < checkpoints.length; ci++) {
      const k = checkpoints[ci] - 1;
      if (Math.abs(path[k] - p) < h) { firstIn = ci; break; }
    }
    const finalIn = Math.abs(path[n-1] - p) < h;
    if (firstIn === -1 && finalIn) firstIn = checkpoints.length;

    checkpoints.forEach((k, ci) => {
      const val    = path[k - 1].toFixed(3);
      const inBand = Math.abs(path[k-1] - p) < h;
      const isCrit = (ci === firstIn);
      const cls    = isCrit ? 'td-crit' : (inBand ? 'td-in' : 'td-out');
      if (inBand) colInCount[ci]++;
      tbody += `<td class="${cls}">${val}${isCrit ? ' ★' : ''}</td>`;
    });

    // 최종 열
    const fval       = path[n-1].toFixed(3);
    const isCritFinal = (firstIn === checkpoints.length);
    const fcls        = isCritFinal ? 'td-crit' : (finalIn ? 'td-in' : 'td-out');
    if (finalIn) colInCount[checkpoints.length]++;
    tbody += `<td class="${fcls}">${fval}${isCritFinal ? ' ★' : ''}</td>`;

    tbody += '</tr>';
  });

  // ── 요약 행: 각 n별 h 범위 안 개수 / 비율 ──
  tbody += '<tr style="border-top:2px solid rgba(253,224,71,.4);background:rgba(0,0,0,.3);">';
  tbody += '<td style="font-size:.65rem;font-weight:800;color:#fde68a;white-space:nowrap;">h 안<br>개수/비율</td>';
  [...checkpoints, n].forEach((_, ci) => {
    const cnt  = colInCount[ci];
    const pct  = (cnt / m * 100).toFixed(0);
    const hi   = cnt / m >= 0.8;
    const mid  = cnt / m >= 0.5;
    const clr  = hi ? '#4ade80' : (mid ? '#fbbf24' : '#f87171');
    tbody += `<td style="font-size:.68rem;font-weight:800;color:${clr};line-height:1.3;">
      ${cnt}/${m}<br><span style="font-size:.62rem;opacity:.85;">${pct}%</span>
    </td>`;
  });
  tbody += '</tr>';

  tbody += '</tbody>';

  table.innerHTML = thead + tbody;
}

function makeCheckpoints(n, maxCols) {
  if (n <= maxCols) return Array.from({length: n}, (_, i) => i + 1);
  const step = Math.ceil(n / (maxCols));
  const pts = [];
  for (let k = step; k <= n; k += step) pts.push(k);
  if (pts[pts.length-1] !== n) { pts.pop(); pts.push(n); }
  return pts.slice(0, maxCols);
}

function buildInsight(paths, p, h, n, m, inside, ratio) {
  const box = document.getElementById('insight');
  box.style.display = 'block';
  const pct = (ratio * 100).toFixed(1);
  const outside = m - inside;
  box.innerHTML = `
    💡 <strong>결과 분석</strong> &nbsp;(n=${n}, p=${p.toFixed(2)}, h=${h.toFixed(2)})<br>
    ${m}번 반복 중 최종 상대도수가 h 범위 <strong style="color:#4ade80;">안</strong>: <strong>${inside}회</strong>,
    범위 <strong style="color:#f87171;">밖</strong>: <strong>${outside}회</strong><br>
    → P(|X/n − p| &lt; h) ≈ <strong>${pct}%</strong>
    ${ratio >= 0.9 ? ' &nbsp;✅ 큰 수의 법칙 잘 작동 중!' : (ratio >= 0.7 ? ' &nbsp;⬆ n을 더 키워보세요!' : ' &nbsp;⬆ n 또는 h를 더 키워보세요!')}
  `;
}
</script>
</body>
</html>
"""


def render():
    st.markdown("#### 🔬 큰 수의 법칙 탐구")
    st.caption(
        "n번 시행에서 상대도수 X/n의 궤적을 반복별로 색을 달리해 그려보면서 큰 수의 법칙을 직접 체험합니다."
    )

    components.html(_HTML, height=1600, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
