import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 이중진자와 카오스",
    "description": "이중진자 시뮬레이션으로 카오스 현상을 직접 체험합니다.",
    "order": 21,
    "hidden": True,
}

HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', 'Noto Sans KR', sans-serif; background: #0f172a; color: #e2e8f0; }
  #app { max-width: 900px; margin: 0 auto; padding: 16px; }
  h2 { font-size: 1.3rem; font-weight: 700; text-align: center; margin-bottom: 6px; color: #f8fafc; }
  .subtitle { text-align: center; font-size: 0.85rem; color: #94a3b8; margin-bottom: 14px; }

  .layout { display: flex; gap: 16px; flex-wrap: wrap; }
  .canvas-wrap { position: relative; flex: 1; min-width: 280px; }
  canvas { display: block; border-radius: 12px; background: #0f172a; border: 1px solid #1e293b; width: 100%; }

  .panel { width: 240px; display: flex; flex-direction: column; gap: 10px; }

  .card {
    background: #1e293b; border-radius: 12px; padding: 14px;
    border: 1px solid #334155;
  }
  .card h3 { font-size: 0.85rem; font-weight: 700; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px; }

  .slider-row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }
  .slider-row label { font-size: 0.82rem; color: #cbd5e1; display: flex; justify-content: space-between; }
  .slider-row label span { color: #38bdf8; font-weight: 700; }
  input[type=range] {
    width: 100%; accent-color: #38bdf8; height: 5px; cursor: pointer;
  }

  .btn-row { display: flex; gap: 6px; flex-wrap: wrap; }
  button {
    flex: 1; padding: 9px 6px; border: none; border-radius: 8px;
    font-size: 0.82rem; font-weight: 700; cursor: pointer; transition: all .15s;
    white-space: nowrap;
  }
  button:active { transform: scale(.97); }
  .btn-start  { background: #22c55e; color: #fff; }
  .btn-start:hover { background: #16a34a; }
  .btn-pause  { background: #f59e0b; color: #fff; }
  .btn-pause:hover { background: #d97706; }
  .btn-reset  { background: #475569; color: #fff; }
  .btn-reset:hover { background: #334155; }
  .btn-add    { background: #ea580c; color: #fff; font-size: 0.78rem; }
  .btn-add:hover { background: #c2410c; }
  .btn-clear  { background: #475569; color: #fff; font-size: 0.78rem; }
  .btn-clear:hover { background: #334155; }

  .info-box { background: #0f172a; border-radius: 8px; padding: 10px; font-size: 0.8rem; color: #94a3b8; line-height: 1.5; }
  .info-box strong { color: #f8fafc; }

  .trail-legend { display: flex; flex-direction: column; gap: 4px; font-size: 0.78rem; }
  .trail-legend .item { display: flex; align-items: center; gap: 6px; }
  .trail-legend .dot { width: 12px; height: 4px; border-radius: 2px; }

  .chaos-meter { margin-top: 6px; }
  .chaos-meter label { font-size: 0.8rem; color: #94a3b8; margin-bottom: 4px; display: block; }
  .meter-bar { background: #0f172a; border-radius: 999px; height: 8px; overflow: hidden; }
  .meter-fill { height: 8px; border-radius: 999px; transition: width .3s, background .3s; }

  .highlight-box {
    background: linear-gradient(135deg, #1e3a5f, #1e2a4a);
    border: 1px solid #3b82f6; border-radius: 10px; padding: 12px;
    font-size: 0.82rem; color: #bfdbfe; line-height: 1.6;
    margin-top: 12px;
  }
  .highlight-box .title { font-weight: 700; color: #60a5fa; margin-bottom: 6px; font-size: 0.9rem; }
</style>
</head>
<body>
<div id="app">
  <h2>🌀 이중진자 시뮬레이션</h2>
  <p class="subtitle">초기 조건의 작은 차이가 완전히 다른 결과를 만들어냅니다</p>

  <div class="layout">
    <div class="canvas-wrap">
      <canvas id="c" width="500" height="460"></canvas>
    </div>

    <div class="panel">
      <div class="card">
        <h3>⚙️ 초기 조건</h3>
        <div class="slider-row">
          <label>첫째 팔 길이 <span id="l1v">120</span></label>
          <input type="range" id="l1" min="60" max="160" value="120" step="5">
        </div>
        <div class="slider-row">
          <label>둘째 팔 길이 <span id="l2v">100</span></label>
          <input type="range" id="l2" min="60" max="160" value="100" step="5">
        </div>
        <div class="slider-row">
          <label>팔 1 초기 각도° <span id="a1v">150</span></label>
          <input type="range" id="a1" min="30" max="175" value="150" step="1">
        </div>
        <div class="slider-row">
          <label>팔 2 초기 각도° <span id="a2v">90</span></label>
          <input type="range" id="a2" min="30" max="175" value="90" step="1">
        </div>
        <div class="slider-row">
          <label>시뮬레이션 속도 <span id="spv">1.0x</span></label>
          <input type="range" id="speed" min="0.2" max="5" value="1" step="0.2">
        </div>
        <div class="btn-row" style="margin-top:4px">
          <button class="btn-start" id="startBtn" onclick="startSim()">▶ 시작</button>
          <button class="btn-pause" id="pauseBtn" onclick="pauseSim()" disabled>⏸</button>
          <button class="btn-reset" onclick="resetSim()">↺ 리셋</button>
        </div>
      </div>

      <div class="card">
        <h3>🎨 나비효과 직접 보기</h3>
        <div style="font-size:0.78rem;color:#cbd5e1;margin-bottom:10px;line-height:1.65;background:#0f172a;border-radius:8px;padding:8px;">
          버튼을 누르면 같은 시작 위치에서<br>
          팔 1 각도만 <strong style="color:#fbbf24;">딱 0.5° 다른</strong> 진자가 추가됩니다.<br><br>
          <span style="color:#38bdf8;">● 파란 진자</span> — 기준<br>
          <span style="color:#ff6b35;">● 주황 진자</span> — 0.5° 차이<br><br>
          처음엔 거의 겹쳐 움직이다가,<br>시간이 지나면 <strong style="color:#f8fafc;">완전히 다른 방향</strong>으로 갑니다!
        </div>
        <div class="btn-row">
          <button class="btn-add" onclick="addGhost()">+ 주황 진자 추가</button>
          <button class="btn-clear" onclick="clearGhosts()">✕ 지우기</button>
        </div>
        <div class="trail-legend" id="legend" style="margin-top:8px;"></div>
      </div>

      <div class="card">
        <h3>📊 혼돈 지수</h3>
        <div class="chaos-meter">
          <label>두 궤적이 얼마나 달라졌나?</label>
          <div class="meter-bar"><div class="meter-fill" id="meterFill" style="width:0%;background:#22c55e;"></div></div>
          <p style="font-size:0.78rem;color:#94a3b8;margin-top:4px;" id="meterLabel">비교 궤적을 추가하세요</p>
        </div>
      </div>

      <div class="highlight-box">
        <div class="title">💡 카오스란?</div>
        초기 조건의 아주 작은 차이가 시간이 지나면서 <strong>완전히 다른</strong> 결과를 낳는 현상.<br>
        이것이 바로 <strong>나비효과</strong>입니다!
      </div>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');

const g = 9.8;
let running = false;
let animId = null;
let lastTime = null;

// 팔 색상 팔레트 (파란 기준 / 주황 비교)
const PALETTE = ['#38bdf8','#ff6b35','#a3e635','#c084fc','#34d399','#fbbf24'];
let simSpeed = 1;

// 진자 상태 객체
function makePendulum(a1, a2, l1, l2, color) {
  return {
    a1: a1 * Math.PI / 180,
    a2: a2 * Math.PI / 180,
    w1: 0, w2: 0,
    l1, l2,
    m1: 1, m2: 1,
    trail: [],
    color,
    alive: true,
  };
}

let pendulums = [];
let mainPendulum = null;

function initMain() {
  const l1 = +document.getElementById('l1').value;
  const l2 = +document.getElementById('l2').value;
  const a1 = +document.getElementById('a1').value;
  const a2 = +document.getElementById('a2').value;
  mainPendulum = makePendulum(a1, a2, l1, l2, PALETTE[0]);
  pendulums = [mainPendulum];
  updateLegend();
}

function getPos(p) {
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const x1 = cx + p.l1 * Math.sin(p.a1);
  const y1 = cy + p.l1 * Math.cos(p.a1);
  const x2 = x1 + p.l2 * Math.sin(p.a2);
  const y2 = y1 + p.l2 * Math.cos(p.a2);
  return { cx, cy, x1, y1, x2, y2 };
}

// Runge-Kutta 4th order
function derivatives(p) {
  const { a1, a2, w1, w2, l1, l2, m1, m2 } = p;
  const d = a1 - a2;
  const M = m1 + m2;

  const da1 = w1;
  const da2 = w2;

  const num1 = -g*(2*m1+m2)*Math.sin(a1) - m2*g*Math.sin(a1-2*a2)
               - 2*Math.sin(d)*m2*(w2*w2*l2 + w1*w1*l1*Math.cos(d));
  const den1 = l1*(2*M - m2*Math.cos(2*d));
  const dw1 = num1/den1;

  const num2 = 2*Math.sin(d)*(w1*w1*l1*M + g*M*Math.cos(a1) + w2*w2*l2*m2*Math.cos(d));
  const den2 = l2*(2*M - m2*Math.cos(2*d));
  const dw2 = num2/den2;

  return { da1, da2, dw1, dw2 };
}

function rk4Step(p, dt) {
  function deriv(state) {
    const tmp = { ...p, ...state };
    return derivatives(tmp);
  }
  const s0 = { a1: p.a1, a2: p.a2, w1: p.w1, w2: p.w2 };
  const k1 = deriv(s0);
  const k2 = deriv({ a1: s0.a1+dt/2*k1.da1, a2: s0.a2+dt/2*k1.da2, w1: s0.w1+dt/2*k1.dw1, w2: s0.w2+dt/2*k1.dw2 });
  const k3 = deriv({ a1: s0.a1+dt/2*k2.da1, a2: s0.a2+dt/2*k2.da2, w1: s0.w1+dt/2*k2.dw1, w2: s0.w2+dt/2*k2.dw2 });
  const k4 = deriv({ a1: s0.a1+dt*k3.da1, a2: s0.a2+dt*k3.da2, w1: s0.w1+dt*k3.dw1, w2: s0.w2+dt*k3.dw2 });

  p.a1 += dt/6*(k1.da1+2*k2.da1+2*k3.da1+k4.da1);
  p.a2 += dt/6*(k1.da2+2*k2.da2+2*k3.da2+k4.da2);
  p.w1 += dt/6*(k1.dw1+2*k2.dw1+2*k3.dw1+k4.dw1);
  p.w2 += dt/6*(k1.dw2+2*k2.dw2+2*k3.dw2+k4.dw2);
}

const MAX_TRAIL = 400;

function stepAll(dt) {
  for (const p of pendulums) {
    rk4Step(p, dt);
    const pos = getPos(p);
    p.trail.push({ x: pos.x2, y: pos.y2 });
    if (p.trail.length > MAX_TRAIL) p.trail.shift();
  }
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 배경
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 피벗 눈금
  const cx = canvas.width / 2, cy = canvas.height / 2;
  ctx.beginPath();
  ctx.arc(cx, cy, 5, 0, Math.PI*2);
  ctx.fillStyle = '#64748b';
  ctx.fill();

  for (let i = pendulums.length - 1; i >= 0; i--) {
    const p = pendulums[i];
    const isMain = i === 0;
    const pos = getPos(p);
    const alpha = isMain ? 1.0 : 0.9;

    // 궤적
    if (p.trail.length > 1) {
      ctx.beginPath();
      ctx.moveTo(p.trail[0].x, p.trail[0].y);
      for (let j = 1; j < p.trail.length; j++) {
        ctx.lineTo(p.trail[j].x, p.trail[j].y);
      }
      ctx.strokeStyle = p.color;
      ctx.globalAlpha = isMain ? 0.45 : 0.7;
      ctx.lineWidth = isMain ? 1.5 : 2.5;
      ctx.stroke();
      ctx.globalAlpha = 1;
    }

    // 팔
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = p.color;
    ctx.lineWidth = isMain ? 3 : 2.5;
    ctx.beginPath(); ctx.moveTo(pos.cx, pos.cy); ctx.lineTo(pos.x1, pos.y1); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(pos.x1, pos.y1); ctx.lineTo(pos.x2, pos.y2); ctx.stroke();

    // 무게추 (비교 진자는 테두리 추가로 더 잘 보이게)
    ctx.fillStyle = p.color;
    ctx.beginPath(); ctx.arc(pos.x1, pos.y1, isMain?9:8, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(pos.x2, pos.y2, isMain?9:8, 0, Math.PI*2); ctx.fill();
    if (!isMain) {
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(pos.x2, pos.y2, 8, 0, Math.PI*2); ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  // 혼돈 지수 업데이트
  updateMeter();
}

function updateMeter() {
  if (pendulums.length < 2) {
    document.getElementById('meterFill').style.width = '0%';
    document.getElementById('meterLabel').textContent = '비교 궤적을 추가하세요';
    return;
  }
  const p0 = pendulums[0], p1 = pendulums[1];
  const pos0 = getPos(p0), pos1 = getPos(p1);
  const dist = Math.hypot(pos0.x2 - pos1.x2, pos0.y2 - pos1.y2);
  const maxDist = 300;
  const ratio = Math.min(dist / maxDist, 1);
  const pct = (ratio * 100).toFixed(0);
  const fill = document.getElementById('meterFill');
  fill.style.width = pct + '%';
  const hue = Math.round(ratio * 0) + (1-ratio)*120;
  fill.style.background = ratio < 0.3 ? '#22c55e' : ratio < 0.65 ? '#f59e0b' : '#ef4444';
  document.getElementById('meterLabel').textContent =
    ratio < 0.05 ? '거의 같은 궤적 (초기 단계)' :
    ratio < 0.3  ? `조금씩 달라지는 중... (${pct}%)` :
    ratio < 0.65 ? `많이 달라졌어요! (${pct}%)` :
                   `완전히 다른 궤적! 카오스! (${pct}%)`;
}

function loop(ts) {
  if (!running) return;
  if (lastTime === null) lastTime = ts;
  const elapsed = Math.min(ts - lastTime, 50);
  lastTime = ts;

  const substeps = 8;
  const dt = elapsed / 1000 * simSpeed / substeps;
  for (let i = 0; i < substeps; i++) stepAll(dt);

  draw();
  animId = requestAnimationFrame(loop);
}

function startSim() {
  if (running) return;
  if (!mainPendulum) initMain();
  running = true;
  lastTime = null;
  document.getElementById('startBtn').disabled = true;
  document.getElementById('pauseBtn').disabled = false;
  animId = requestAnimationFrame(loop);
}

function pauseSim() {
  running = false;
  if (animId) cancelAnimationFrame(animId);
  document.getElementById('startBtn').disabled = false;
  document.getElementById('pauseBtn').disabled = true;
}

function resetSim() {
  pauseSim();
  initMain();
  lastTime = null;
  draw();
  document.getElementById('startBtn').disabled = false;
}

function addGhost() {
  if (!mainPendulum) initMain();
  const offset = 0.5;
  const color = PALETTE[Math.min(pendulums.length, PALETTE.length - 1)];
  const ghost = makePendulum(
    mainPendulum.a1 * 180/Math.PI + offset,
    mainPendulum.a2 * 180/Math.PI,
    mainPendulum.l1, mainPendulum.l2, color
  );
  // 현재 진행 중인 상태로 동기화
  ghost.a1 = mainPendulum.a1 + offset * Math.PI/180;
  ghost.a2 = mainPendulum.a2;
  ghost.w1 = mainPendulum.w1;
  ghost.w2 = mainPendulum.w2;
  ghost.trail = [];
  pendulums.push(ghost);
  updateLegend();
}

function clearGhosts() {
  pendulums = [mainPendulum];
  updateLegend();
}

function updateLegend() {
  const el = document.getElementById('legend');
  if (pendulums.length <= 1) { el.innerHTML = ''; return; }
  el.innerHTML = pendulums.map((p, i) => `
    <div class="item">
      <div class="dot" style="background:${p.color}"></div>
      <span style="color:${p.color};font-size:0.78rem;">
        ${i===0 ? '● 기준 진자 (팔1=' + (p.a1*180/Math.PI).toFixed(1) + '°)' : `● 비교 진자 (팔1=${(p.a1*180/Math.PI).toFixed(1)}°)`}
      </span>
    </div>
  `).join('');
}

// 슬라이더 연동
['l1','l2','a1','a2'].forEach(id => {
  document.getElementById(id).addEventListener('input', function() {
    document.getElementById(id+'v').textContent = this.value;
    if (!running) { initMain(); draw(); }
  });
});
document.getElementById('speed').addEventListener('input', function() {
  simSpeed = +this.value;
  document.getElementById('spv').textContent = simSpeed.toFixed(1) + 'x';
});

// 초기화
initMain();
draw();

// 리사이즈 대응
function resizeCanvas() {
  const wrap = canvas.parentElement;
  const w = wrap.clientWidth;
  canvas.style.width = w + 'px';
  canvas.style.height = (w * 460/500) + 'px';
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();
</script>
</body>
</html>
"""


def render():
    st.title("🌀 이중진자 시뮬레이션 — 카오스 체험")
    st.markdown(
        """
        이중진자는 두 개의 막대가 연결된 단순한 구조입니다.  
        그런데 **초기 조건이 조금만 달라져도** 시간이 지나면 완전히 다른 움직임을 보입니다.  
        이것이 바로 **카오스(Chaos)** 현상의 핵심입니다.
        """
    )

    st.info("💡 **사용법**: ▶ 시작 → 궤적을 관찰한 뒤 **비교 궤적 추가** 버튼을 눌러보세요. 초기 각도가 0.5°만 달라도 결국 완전히 다른 궤적을 그립니다!")

    components.html(HTML, height=1050, scrolling=False)

    st.markdown("---")
    st.markdown(
        """
        ### 📝 생각해보기

        1. **비교 궤적을 추가했을 때**, 처음에는 두 궤적이 거의 겹쳐 보입니다. 언제부터 달라지기 시작하나요?
        2. 초기 각도 슬라이더를 바꿔서 **각도가 작을 때**(단진자에 가까울 때)와 **각도가 클 때**를 비교해보세요. 차이가 있나요?
        3. 이중진자의 움직임을 **미래에 정확히 예측**하는 것이 왜 어려울까요?
        """
    )
