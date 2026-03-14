import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 로렌츠 끌개 — 불규칙 속의 규칙",
    "description": "3D 로렌츠 끌개를 직접 회전시키며 카오스 속의 아름다운 구조를 탐구합니다.",
    "order": 23,
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
  h2 { font-size: 1.3rem; font-weight: 700; text-align: center; margin-bottom: 4px; color: #f8fafc; }
  .subtitle { text-align: center; font-size: 0.85rem; color: #94a3b8; margin-bottom: 14px; }

  .layout { display: flex; gap: 14px; flex-wrap: wrap; }

  .canvas-area { flex: 1; min-width: 260px; position: relative; }
  canvas#lorenz { display: block; width: 100%; border-radius: 14px; background: #050a14; border: 1px solid #1e293b; cursor: grab; }
  canvas#lorenz.dragging { cursor: grabbing; }
  .drag-hint { text-align: center; font-size: 0.75rem; color: #475569; margin-top: 5px; }

  .panel { width: 210px; display: flex; flex-direction: column; gap: 10px; }
  .card { background: #1e293b; border-radius: 12px; padding: 12px; border: 1px solid #334155; }
  .card h3 { font-size: 0.82rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }

  .slider-row { display: flex; flex-direction: column; gap: 3px; margin-bottom: 8px; }
  .slider-row label { font-size: 0.8rem; color: #cbd5e1; display: flex; justify-content: space-between; }
  .slider-row label span { color: #a5f3fc; font-weight: 700; }
  input[type=range] { width: 100%; accent-color: #a5f3fc; cursor: pointer; }

  .btn-row { display: flex; gap: 6px; flex-wrap: wrap; }
  button {
    flex: 1; padding: 6px 8px; border: none; border-radius: 8px;
    font-size: 0.8rem; font-weight: 700; cursor: pointer; transition: all .15s;
  }
  button:active { transform: scale(.97); }
  .btn-play   { background: #22c55e; color: #fff; }
  .btn-play.paused { background: #f59e0b; }
  .btn-reset  { background: #475569; color: #fff; }
  .btn-view   { background: #4f46e5; color: #fff; font-size: 0.75rem; }
  .btn-view:hover { background: #3730a3; }
  .btn-color  { background: #0e7490; color: #fff; font-size: 0.75rem; }
  .btn-color:hover { background: #0c5a70; }

  .view-btns { display: flex; gap: 4px; flex-wrap: wrap; }
  .view-btns button { flex: 0 0 calc(50% - 2px); font-size: 0.71rem; padding: 5px 4px; }

  .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .stat-box { background: #0f172a; border-radius: 8px; padding: 7px; text-align: center; }
  .stat-box .val { font-size: 1rem; font-weight: 700; color: #a5f3fc; }
  .stat-box .lbl { font-size: 0.68rem; color: #64748b; margin-top: 1px; }

  .concept-card {
    background: linear-gradient(135deg, #1a2a1a, #142814);
    border: 1px solid #22c55e40; border-radius: 12px;
    padding: 14px; margin-top: 10px;
    font-size: 0.82rem; color: #bbf7d0; line-height: 1.7;
  }
  .concept-card .title { font-weight: 700; color: #4ade80; margin-bottom: 8px; font-size: 0.95rem; }
  .concept-card strong { color: #f8fafc; }

  .color-schemes { display: flex; gap: 4px; flex-wrap: wrap; }
  .color-swatch {
    width: 24px; height: 24px; border-radius: 6px; cursor: pointer;
    border: 2px solid transparent; transition: border-color .15s;
  }
  .color-swatch.active { border-color: #f8fafc; }

  .progress-ring { text-align: center; padding: 4px 0; }
  .progress-ring .num { font-size: 1.2rem; font-weight: 700; color: #a5f3fc; }
  .progress-ring .lbl { font-size: 0.72rem; color: #64748b; }

  .param-desc {
    font-size: 0.71rem; color: #64748b; line-height: 1.45;
    margin-top: 2px; padding: 4px 6px;
    background: #0f172a; border-radius: 5px;
  }
  .param-desc strong { color: #94a3b8; }
  .chaos-on  { color: #f472b6; font-weight: 700; }
  .chaos-off { color: #22c55e; font-weight: 700; }
</style>
</head>
<body>
<div id="app">
  <h2>🌀 로렌츠 끌개 — 불규칙 속의 규칙성</h2>
  <p class="subtitle">예측 불가능한 카오스 궤적이 그려내는 아름다운 나비 모양 구조</p>

  <div class="layout">
    <div class="canvas-area">
      <canvas id="lorenz" width="500" height="460"></canvas>
      <p class="drag-hint">🖱 드래그로 3D 회전 | 스크롤로 줌</p>
    </div>

    <div class="panel">
      <div class="card">
        <h3>⚙️ 파라미터</h3>
        <div class="slider-row">
          <label>σ — 공기 혼합 속도 <span id="sV">10.0</span></label>
          <input type="range" id="sR" min="1" max="20" step="0.5" value="10">
          <p class="param-desc">(시그마) 공기가 얼마나 빠르게 <strong>섞이는지</strong>.<br>10이 지구 대기 비율입니다.</p>
        </div>
        <div class="slider-row">
          <label>ρ — 위아래 온도차 <span id="rV">28.0</span></label>
          <input type="range" id="rR" min="10" max="60" step="0.5" value="28">
          <p class="param-desc">(로) 대기 위아래 사이 <strong>온도 차이</strong>.<br><span class="chaos-off">▶ ~24 이하</span> : 일정한 패턴으로 수렴<br><span class="chaos-on">▶ 24.7 이상</span> : 카오스 시작! 나비 모양 등장</p>
        </div>
        <div class="slider-row">
          <label>β — 대기층 모양 <span id="bV">2.67</span></label>
          <input type="range" id="bR" min="0.5" max="6" step="0.1" value="2.67">
          <p class="param-desc">(베타) 대기층의 <strong>넣이와 폭의 비율</strong>.<br>8/3 ≈ 2.67이 지구 대기 기본값입니다.</p>
        </div>
        <div class="slider-row">
          <label>속도 <span id="spV">1.0x</span></label>
          <input type="range" id="spR" min="0.1" max="5" step="0.1" value="1">
        </div>
        <div class="btn-row" style="margin-top:4px">
          <button class="btn-play" id="playBtn" onclick="togglePlay()">⏸ 일시정지</button>
          <button class="btn-reset" onclick="resetAll()">↺ 리셋</button>
        </div>
      </div>

      <div class="card">
        <h3>🎨 색상 테마</h3>
        <div class="color-schemes" id="colorSwatches"></div>
      </div>

      <div class="card">
        <h3>📐 시점 선택</h3>
        <div class="view-btns">
          <button class="btn-view" onclick="setView(0,0)">정면 (XZ)</button>
          <button class="btn-view" onclick="setView(Math.PI/2,0)">측면 (YZ)</button>
          <button class="btn-view" onclick="setView(0,Math.PI/2)">위 (XY)</button>
          <button class="btn-view" onclick="setView(0.5,0.4)">3D 사선</button>
        </div>
      </div>

      <div class="card">
        <h3>📊 현재 상태</h3>
        <div class="stat-grid">
          <div class="stat-box"><div class="val" id="xVal">—</div><div class="lbl">x</div></div>
          <div class="stat-box"><div class="val" id="yVal">—</div><div class="lbl">y</div></div>
          <div class="stat-box"><div class="val" id="zVal">—</div><div class="lbl">z</div></div>
          <div class="stat-box"><div class="val" id="ptNum">0</div><div class="lbl">점의 수</div></div>
        </div>
        <div class="progress-ring" style="margin-top:6px">
          <div class="num" id="wingCount">0</div>
          <div class="lbl">날개 전환 횟수</div>
        </div>
      </div>
    </div>
  </div>

  <div class="concept-card">
    <div class="title">🔍 끌개(Attractor)란?</div>

    로렌츠는 다음 세 가지 관계를 자분방정식으로 표현했습니다:<br>
    · <strong>x</strong> : 대연류의 회전 속도 &nbsp;· <strong>y</strong> : 수평 온도 차이 &nbsp;· <strong>z</strong> : 수직 온도 차<br>
    이 세 값이 시간에 따라 변하는 경로를 <strong>3차원 공간에 점으로 찍으면</strong> 바로 이 그림이 나옵니다.<br><br>

    카오스 구역(ρ ≥ 24.7)에서는 궤적이 <strong>예측 불가능</strong>하지만,<br>
    염청나게 오래 관찰해도 궤적은 항상 이 <strong>나비 모양과 끝개(Attractor) 안에서만</strong> 움직입니다.<br>
    진정 같은 경로를 절대 반복하지 않으면서도, 특정 영역 밖으로는 나가지 않는 것입니다.<br><br>
    <strong>불규칙 속의 규칙성</strong> — 이것이 카오스의 숨겨진 아름다움입니다.
  </div>
</div>

<script>
// ── 파라미터 ──────────────────────────────────────
let sigma = 10, rho = 28, beta = 8/3;
let speed = 1;

// ── 궤적 데이터 ───────────────────────────────────
let trail = [];
const MAX_TRAIL = 5000;
let state = { x: 0.1, y: 0.0, z: 0.5 };
let t = 0;
let playing = true;
let animId = null;

// ── 카운터 ────────────────────────────────────────
let wingCount = 0;
let lastWing = 0; // +1 = right wing, -1 = left wing

// ── 색상 테마 ─────────────────────────────────────
const COLOR_THEMES = [
  { name: 'cyan',    stops: ['#0ea5e9','#6366f1','#a855f7'] },
  { name: 'fire',    stops: ['#ef4444','#f97316','#facc15'] },
  { name: 'forest',  stops: ['#22c55e','#84cc16','#ecfccb'] },
  { name: 'rose',    stops: ['#f472b6','#e879f9','#c084fc'] },
  { name: 'ocean',   stops: ['#06b6d4','#0891b2','#0e7490'] },
  { name: 'gold',    stops: ['#fbbf24','#f59e0b','#d97706'] },
];
let colorTheme = 0;

// ── 3D 회전 상태 ──────────────────────────────────
let rotX = 0.3, rotY = 0.2, rotZ = 0;
let lastMouse = null;
let isDragging = false;
let zoomFactor = 1;

// ── 캔버스 ────────────────────────────────────────
const canvas = document.getElementById('lorenz');
const ctx = canvas.getContext('2d');

function lorenzDeriv(s) {
  return {
    dx: sigma * (s.y - s.x),
    dy: s.x * (rho - s.z) - s.y,
    dz: s.x * s.y - beta * s.z
  };
}
function rk4Step(s, dt) {
  function add(a, b, h) { return { x:a.x+h*b.dx, y:a.y+h*b.dy, z:a.z+h*b.dz }; }
  const k1 = lorenzDeriv(s);
  const k2 = lorenzDeriv(add(s, k1, dt/2));
  const k3 = lorenzDeriv(add(s, k2, dt/2));
  const k4 = lorenzDeriv(add(s, k3, dt));
  return {
    x: s.x + dt/6*(k1.dx+2*k2.dx+2*k3.dx+k4.dx),
    y: s.y + dt/6*(k1.dy+2*k2.dy+2*k3.dy+k4.dy),
    z: s.z + dt/6*(k1.dz+2*k2.dz+2*k3.dz+k4.dz),
  };
}

// ── 3D → 2D 투영 ──────────────────────────────────
function project(x, y, z) {
  // 중심 정규화 (로렌츠 좌표는 대략 ±20 × ±30 × 0~50)
  const nx = x / 25;
  const ny = y / 25;
  const nz = (z - 25) / 25;

  // rotX (x축 기준 회전)
  const y1 = ny * Math.cos(rotX) - nz * Math.sin(rotX);
  const z1 = ny * Math.sin(rotX) + nz * Math.cos(rotX);
  // rotY (y축 기준 회전)
  const x2 = nx * Math.cos(rotY) + z1 * Math.sin(rotY);
  const z2 = -nx * Math.sin(rotY) + z1 * Math.cos(rotY);
  // rotZ (z축 기준 회전)
  const x3 = x2 * Math.cos(rotZ) - y1 * Math.sin(rotZ);
  const y3 = x2 * Math.sin(rotZ) + y1 * Math.cos(rotZ);

  // 원근 투영
  const fov = 3;
  const scale = (fov / (fov + z2)) * 200 * zoomFactor;
  const cx = canvas.width  / 2;
  const cy = canvas.height / 2;
  return { sx: cx + x3 * scale, sy: cy - y3 * scale, depth: z2 };
}

// ── 그리기 ────────────────────────────────────────
function draw() {
  ctx.fillStyle = '#050a14';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (trail.length < 2) return;

  const theme = COLOR_THEMES[colorTheme];
  const n = trail.length;

  for (let i = 1; i < n; i++) {
    const ratio = i / n;
    // 그라데이션 색상 계산
    const stops = theme.stops;
    let r, g, b;
    if (ratio < 0.5) {
      const t = ratio * 2;
      r = lerpColor(stops[0], stops[1], t);
    } else {
      const t = (ratio - 0.5) * 2;
      r = lerpColor(stops[1], stops[2], t);
    }

    const p0 = project(trail[i-1].x, trail[i-1].y, trail[i-1].z);
    const p1 = project(trail[i].x, trail[i].y, trail[i].z);

    ctx.beginPath();
    ctx.moveTo(p0.sx, p0.sy);
    ctx.lineTo(p1.sx, p1.sy);
    ctx.strokeStyle = r;
    ctx.globalAlpha = 0.5 + ratio * 0.5;
    ctx.lineWidth = ratio > 0.97 ? 2.5 : 1;
    ctx.stroke();
  }
  ctx.globalAlpha = 1;

  // 현재 점
  if (n > 0) {
    const last = trail[n-1];
    const projected = project(last.x, last.y, last.z);
    ctx.beginPath();
    ctx.arc(projected.sx, projected.sy, 4, 0, Math.PI*2);
    ctx.fillStyle = '#f8fafc';
    ctx.fill();
    ctx.beginPath();
    ctx.arc(projected.sx, projected.sy, 7, 0, Math.PI*2);
    ctx.strokeStyle = '#f8fafc50';
    ctx.lineWidth = 1;
    ctx.stroke();
  }
}

function lerpColor(c1, c2, t) {
  const hex = h => parseInt(h.slice(1), 16);
  const r1 = (hex(c1)>>16)&0xff, g1=(hex(c1)>>8)&0xff, b1=hex(c1)&0xff;
  const r2 = (hex(c2)>>16)&0xff, g2=(hex(c2)>>8)&0xff, b2=hex(c2)&0xff;
  const r = Math.round(r1+t*(r2-r1)), g = Math.round(g1+t*(g2-g1)), bv = Math.round(b1+t*(b2-b1));
  return `rgb(${r},${g},${bv})`;
}

// ── 애니메이션 루프 ───────────────────────────────
let lastTs = null;
const DT_BASE = 0.005;

function loop(ts) {
  if (!playing) return;
  if (!lastTs) lastTs = ts;
  const wallDt = Math.min(ts - lastTs, 50) / 1000;
  lastTs = ts;

  const steps = Math.round(speed * 8);
  const dt = wallDt * speed / steps;
  for (let i = 0; i < steps; i++) {
    state = rk4Step(state, DT_BASE * speed);
    trail.push({ ...state });
    if (trail.length > MAX_TRAIL) trail.shift();

    // 날개 전환 감지
    const w = state.x > 0 ? 1 : -1;
    if (w !== lastWing && lastWing !== 0) { wingCount++; }
    lastWing = w;
  }
  t += wallDt * speed;

  updateHUD();
  draw();
  animId = requestAnimationFrame(loop);
}

function updateHUD() {
  const s = state;
  document.getElementById('xVal').textContent = s.x.toFixed(1);
  document.getElementById('yVal').textContent = s.y.toFixed(1);
  document.getElementById('zVal').textContent = s.z.toFixed(1);
  document.getElementById('ptNum').textContent = trail.length;
  document.getElementById('wingCount').textContent = wingCount;
}

function togglePlay() {
  playing = !playing;
  const btn = document.getElementById('playBtn');
  if (playing) {
    btn.textContent = '⏸ 일시정지';
    btn.classList.remove('paused');
    lastTs = null;
    animId = requestAnimationFrame(loop);
  } else {
    btn.textContent = '▶ 재생';
    btn.classList.add('paused');
    if (animId) cancelAnimationFrame(animId);
  }
}

function resetAll() {
  playing = true;
  if (animId) cancelAnimationFrame(animId);
  state = { x: 0.1, y: 0.0, z: 0.5 };
  trail = []; t = 0; wingCount = 0; lastWing = 0;
  lastTs = null;
  document.getElementById('playBtn').textContent = '⏸ 일시정지';
  document.getElementById('playBtn').classList.remove('paused');
  animId = requestAnimationFrame(loop);
}

// ── 시점 설정 ─────────────────────────────────────
function setView(rx, ry) {
  rotX = rx; rotY = ry; rotZ = 0;
  draw();
}

// ── 드래그로 3D 회전 ──────────────────────────────
canvas.addEventListener('mousedown', e => { isDragging = true; lastMouse = { x: e.clientX, y: e.clientY }; canvas.classList.add('dragging'); });
document.addEventListener('mouseup', () => { isDragging = false; canvas.classList.remove('dragging'); });
document.addEventListener('mousemove', e => {
  if (!isDragging || !lastMouse) return;
  const dx = e.clientX - lastMouse.x;
  const dy = e.clientY - lastMouse.y;
  rotY += dx * 0.008;
  rotX += dy * 0.008;
  lastMouse = { x: e.clientX, y: e.clientY };
  if (!playing) draw();
});

// 터치 지원
canvas.addEventListener('touchstart', e => { e.preventDefault(); const t = e.touches[0]; isDragging = true; lastMouse = { x: t.clientX, y: t.clientY }; }, { passive: false });
document.addEventListener('touchend', () => { isDragging = false; });
document.addEventListener('touchmove', e => {
  if (!isDragging || !lastMouse) return;
  const t = e.touches[0];
  const dx = t.clientX - lastMouse.x;
  const dy = t.clientY - lastMouse.y;
  rotY += dx * 0.008; rotX += dy * 0.008;
  lastMouse = { x: t.clientX, y: t.clientY };
  if (!playing) draw();
}, { passive: false });

// 스크롤 줌
canvas.addEventListener('wheel', e => {
  e.preventDefault();
  zoomFactor = Math.max(0.3, Math.min(3, zoomFactor - e.deltaY * 0.001));
  if (!playing) draw();
}, { passive: false });

// ── 슬라이더 ─────────────────────────────────────
document.getElementById('sR').addEventListener('input', function() { sigma = +this.value; document.getElementById('sV').textContent = sigma.toFixed(1); resetAll(); });
document.getElementById('rR').addEventListener('input', function() { rho = +this.value;   document.getElementById('rV').textContent = rho.toFixed(1);   resetAll(); });
document.getElementById('bR').addEventListener('input', function() { beta = +this.value;  document.getElementById('bV').textContent = beta.toFixed(2);  resetAll(); });
document.getElementById('spR').addEventListener('input', function() { speed = +this.value; document.getElementById('spV').textContent = speed.toFixed(1) + 'x'; });

// ── 색상 스와치 ───────────────────────────────────
const swatchDiv = document.getElementById('colorSwatches');
COLOR_THEMES.forEach((theme, i) => {
  const div = document.createElement('div');
  div.className = 'color-swatch' + (i === 0 ? ' active' : '');
  div.style.background = `linear-gradient(135deg, ${theme.stops[0]}, ${theme.stops[2]})`;
  div.title = theme.name;
  div.onclick = () => {
    colorTheme = i;
    document.querySelectorAll('.color-swatch').forEach((s, j) => s.classList.toggle('active', j === i));
    if (!playing) draw();
  };
  swatchDiv.appendChild(div);
});

// ── 캔버스 크기 조정 ──────────────────────────────
function resizeCanvas() {
  const w = canvas.parentElement.clientWidth;
  canvas.width  = Math.max(w, 200);
  canvas.height = Math.round(canvas.width * 460 / 500);
  if (!playing) draw();
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// ── 시작 ─────────────────────────────────────────
animId = requestAnimationFrame(loop);
</script>
</body>
</html>
"""


def render():
    st.title("🌀 로렌츠 끌개 — 불규칙 속의 규칙성")
    st.markdown(
        """
        카오스 궤적은 **예측 불가능**합니다.  
        그런데 아무리 오래 관찰해도 궤적은 **특정 모양 안에서만** 돌아다닙니다.  
        이 구조를 **이상한 끌개(Strange Attractor)** 라고 합니다.
        """
    )

    st.info("💡 **사용법**: 마우스 드래그로 3D 회전, 스크롤로 줌. σ·ρ·β 파라미터를 바꾸면 끌개 모양이 달라집니다. ρ를 10으로 낮추면 카오스가 사라집니다!")

    components.html(HTML, height=1300, scrolling=False)

    st.markdown("---")
    st.markdown(
        """
        ### 📝 생각해보기

        1. 끌개를 오래 관찰했을 때, 궤적은 **어디로든 가나요**, 아니면 **특정 범위 안**에 머무르나요?
        2. 두 날개(왼쪽/오른쪽) 중 어느 쪽으로 갈지 예측할 수 있나요? 가능하다면 어떤 방법으로 예측할 수 있을까요?
        3. ρ 값을 바꿀 때 끌개 모양이 어떻게 달라지나요? ρ = 10으로 낮추면 무슨 일이 생기나요?
        4. "불규칙 속의 규칙성"이란 무슨 뜻인지 자신의 말로 설명해보세요.
        """
    )
