import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 나비효과 — 로렌츠의 기상 모델",
    "description": "로렌츠 방정식으로 초기 조건의 미세한 차이가 결과를 얼마나 바꾸는지 직접 체험합니다.",
    "order": 22,
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

  .top-layout { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 14px; }

  .graph-wrap { flex: 1; min-width: 260px; display: flex; flex-direction: column; gap: 10px; }
  canvas.graph { display: block; width: 100%; background: #0f172a; border-radius: 10px; border: 1px solid #1e293b; }

  .panel { width: 210px; display: flex; flex-direction: column; gap: 10px; }
  .card {
    background: #1e293b; border-radius: 12px; padding: 12px;
    border: 1px solid #334155;
  }
  .card h3 { font-size: 0.82rem; font-weight: 700; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }

  .slider-row { display: flex; flex-direction: column; gap: 3px; margin-bottom: 8px; }
  .slider-row label { font-size: 0.8rem; color: #cbd5e1; display: flex; justify-content: space-between; }
  .slider-row label span { color: #38bdf8; font-weight: 700; }
  input[type=range] { width: 100%; accent-color: #38bdf8; cursor: pointer; }

  .btn-row { display: flex; gap: 6px; flex-wrap: wrap; }
  button {
    flex: 1; padding: 6px 8px; border: none; border-radius: 8px;
    font-size: 0.8rem; font-weight: 700; cursor: pointer; transition: all .15s;
  }
  button:active { transform: scale(.97); }
  .btn-run   { background: #22c55e; color: #fff; }
  .btn-run:hover { background: #16a34a; }
  .btn-run:disabled { background: #166534; color: #86efac; }
  .btn-stop  { background: #f59e0b; color: #fff; }
  .btn-stop:hover { background: #d97706; }
  .btn-reset { background: #475569; color: #fff; }
  .btn-reset:hover { background: #334155; }

  .diff-display {
    background: #0f172a; border-radius: 8px; padding: 8px;
    text-align: center;
  }
  .diff-display .val { font-size: 1.4rem; font-weight: 700; color: #38bdf8; }
  .diff-display .lbl { font-size: 0.75rem; color: #64748b; margin-top: 2px; }

  .meter-bar { background: #0f172a; border-radius: 999px; height: 10px; overflow: hidden; margin: 6px 0; }
  .meter-fill { height: 10px; border-radius: 999px; transition: width .2s, background .3s; }

  .phase-canvas-wrap { position: relative; }
  canvas.phase { display: block; width: 100%; border-radius: 10px; border: 1px solid #1e293b; background: #0f172a; }

  .legend { display: flex; gap: 12px; justify-content: center; font-size: 0.78rem; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 5px; }
  .legend-dot { width: 12px; height: 4px; border-radius: 2px; }

  .story-card {
    background: linear-gradient(135deg, #1a2744, #1e3a5f);
    border: 1px solid #3b82f6; border-radius: 12px;
    padding: 14px; margin-top: 12px;
    font-size: 0.83rem; color: #bfdbfe; line-height: 1.7;
  }
  .story-card .title { font-weight: 700; color: #60a5fa; margin-bottom: 6px; font-size: 0.95rem; }
  .story-card strong { color: #f8fafc; }

  .badge {
    display: inline-block; padding: 2px 8px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 700; margin-left: 4px;
    background: #1e40af; color: #bfdbfe;
  }
  .param-desc {
    font-size: 0.72rem; color: #64748b; line-height: 1.45;
    margin-top: 2px; padding: 4px 6px;
    background: #0f172a; border-radius: 5px;
  }
  .param-desc strong { color: #94a3b8; }
  .chaos-warn { color: #f472b6; font-weight: 700; }
</style>
</head>
<body>
<div id="app">
  <h2>🦋 나비효과 — 로렌츠의 기상 모델</h2>
  <p class="subtitle">소수점 몇 자리의 차이가 기상 예보를 어떻게 바꾸는지 관찰해보세요</p>

  <div class="top-layout">
    <div class="graph-wrap">
      <canvas class="graph" id="zGraph" height="220"></canvas>
      <canvas class="graph" id="diffGraph" height="140"></canvas>
      <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background:#38bdf8"></div><span>원본 (x₀ = 0)</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#f472b6"></div><span>미세 변화 (x₀ = δ)</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#fb923c"></div><span>두 궤적의 차이</span></div>
      </div>
    </div>

    <div class="panel">
      <div class="card">
        <h3>🔧 방정식 파라미터</h3>
        <div class="slider-row">
          <label>초기 x 차이 (δ) <span id="deltaV">0.001</span></label>
          <input type="range" id="deltaR" min="-6" max="-1" step="0.5" value="-3">
          <p class="param-desc">두 시뮬레이션의 <strong>시작 조건 차이</strong>.<br>예) 0.001 = 소수점 셋째 자리 반올림 오차</p>
        </div>
        <div class="slider-row">
          <label>σ — 공기 혼합 정도 <span id="sigmaV">10</span></label>
          <input type="range" id="sigmaR" min="5" max="20" step="0.5" value="10">
          <p class="param-desc">공기가 얼마나 빠르게 <strong>섞이는지</strong>를 나타냅니다.<br>클수록 대기가 더 활발히 움직입니다. (보통 10)</p>
        </div>
        <div class="slider-row">
          <label>ρ — 위아래 온도 차이 <span id="rhoV">28</span></label>
          <input type="range" id="rhoR" min="10" max="50" step="1" value="28">
          <p class="param-desc">지표면(뜨거움)과 상공(차가움)의 <strong>온도 차이</strong>.<br>크면 대류가 강해지고 날씨가 불안정해져요.<br><span class="chaos-warn">※ ρ ≈ 24.7 이상에서 카오스 발생!</span></p>
        </div>
        <div class="slider-row">
          <label>β — 대기층 모양 <span id="betaV">2.67</span></label>
          <input type="range" id="betaR" min="1" max="5" step="0.1" value="2.67">
          <p class="param-desc">대기층의 폭과 높이의 <strong>비율</strong>.<br>지구 대기에 맞는 기본값은 8/3 ≈ 2.67입니다.</p>
        </div>
        <div class="btn-row" style="margin-top:4px">
          <button class="btn-run" id="runBtn" onclick="startSim()">▶ 시작</button>
          <button class="btn-stop" onclick="stopSim()" id="stopBtn" disabled>⏸</button>
          <button class="btn-reset" onclick="resetSim()">↺</button>
        </div>
      </div>

      <div class="card">
        <h3>📏 현재 차이</h3>
        <div class="diff-display">
          <div class="val" id="diffVal">0.000</div>
          <div class="lbl">두 x 값의 차이</div>
        </div>
        <div class="meter-bar"><div class="meter-fill" id="mFill" style="width:0%;background:#22c55e;"></div></div>
        <p style="font-size:0.75rem;color:#94a3b8;text-align:center;" id="mLabel">시뮬레이션을 시작하세요</p>
      </div>

      <div class="card">
        <h3>⏱ 예측 한계</h3>
        <div style="font-size:0.8rem;color:#94a3b8;line-height:1.5;">
          두 궤적의 차이가<br>처음의 <strong style="color:#f8fafc;">10배</strong>가 될 때까지<br>걸린 시간:
          <div style="font-size:1.3rem;font-weight:700;color:#f472b6;margin-top:4px;" id="lyapunov">—</div>
          <div style="font-size:0.72rem;color:#64748b;">리아푸노프 시간 (예측 한계)</div>
        </div>
      </div>
    </div>
  </div>

  <div class="story-card">
    <div class="title">📖 로렌츠의 발견 (1961년)</div>
    로렌츠는 기상 시뮬레이션을 다시 실행하기 위해 중간 결과를 소수점 <strong>3자리</strong>만 입력했습니다 (원래는 6자리).
    그런데 컴퓨터가 내놓은 결과는 처음과 <strong>완전히 달랐습니다</strong>.<br><br>
    단순한 반올림 오차가 기상 예보 전체를 바꿔버린 것입니다.
    이것이 <strong>나비효과(Butterfly Effect)</strong>의 출발점입니다.
  </div>
</div>

<script>
// ── 로렌츠 방정식 ────────────────────────────────
let sigma = 10, rho = 28, beta = 8/3;
let delta = 0.001;

let state1 = null, state2 = null;
let zHistory1 = [], zHistory2 = [], diffHistory = [];

let running = false, animId = null, lastTs = null;
let t = 0;
let lyapTime = null;

function initStates() {
  state1 = { x: 0.1, y: 0.0, z: 0.5 };
  state2 = { x: 0.1 + delta, y: 0.0, z: 0.5 };
  zHistory1 = []; zHistory2 = []; diffHistory = [];
  t = 0; lyapTime = null;
  document.getElementById('lyapunov').textContent = '—';
  document.getElementById('diffVal').textContent = '0.000';
  document.getElementById('mFill').style.width = '0%';
  document.getElementById('mLabel').textContent = '시뮬레이션을 시작하세요';
}

function lorenzDeriv(s) {
  return {
    dx: sigma * (s.y - s.x),
    dy: s.x * (rho - s.z) - s.y,
    dz: s.x * s.y - beta * s.z
  };
}

function rk4(s, dt) {
  function add(a, b, scale) {
    return { x: a.x + scale*b.dx, y: a.y + scale*b.dy, z: a.z + scale*b.dz };
  }
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

const MAX_HIST = 600;

function step(dt) {
  const substeps = 10;
  const h = dt / substeps;
  for (let i = 0; i < substeps; i++) {
    state1 = rk4(state1, h);
    state2 = rk4(state2, h);
    t += h;
  }
  zHistory1.push(state1.z); if (zHistory1.length > MAX_HIST) zHistory1.shift();
  zHistory2.push(state2.z); if (zHistory2.length > MAX_HIST) zHistory2.shift();
  const diff = Math.abs(state1.x - state2.x);
  diffHistory.push(diff);   if (diffHistory.length > MAX_HIST) diffHistory.shift();

  // 리아푸노프 시간 (초기 차이의 10배)
  if (!lyapTime && diff > delta * 10) {
    lyapTime = t;
    document.getElementById('lyapunov').textContent = `t ≈ ${t.toFixed(1)}`;
  }
  updateHUD(diff);
}

function updateHUD(diff) {
  document.getElementById('diffVal').textContent = diff.toFixed(4);
  const ratio = Math.min(diff / 20, 1);
  const fill = document.getElementById('mFill');
  fill.style.width = (ratio*100).toFixed(0) + '%';
  fill.style.background = ratio < 0.2 ? '#22c55e' : ratio < 0.55 ? '#f59e0b' : '#ef4444';
  document.getElementById('mLabel').textContent =
    ratio < 0.05 ? '거의 차이 없음 — 예측 가능' :
    ratio < 0.2  ? '조금씩 벌어지는 중...' :
    ratio < 0.55 ? '차이가 커졌어요!' : '완전히 달라진 예측!';
}

// ── 그래프 그리기 ─────────────────────────────────
function drawZGraph() {
  const cv = document.getElementById('zGraph');
  const w = cv.width, h = cv.height;
  const ctx = cv.getContext('2d');
  ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, w, h);

  // 축 레이블
  ctx.fillStyle = '#475569'; ctx.font = '11px sans-serif';
  ctx.fillText('z (대류 강도)', 8, 14);

  function drawLine(data, color) {
    if (data.length < 2) return;
    const min = Math.min(...data) - 3;
    const max = Math.max(...data) + 3;
    ctx.beginPath();
    data.forEach((v, i) => {
      const x = (i / (MAX_HIST - 1)) * (w - 20) + 10;
      const y = h - 20 - ((v - min) / (max - min)) * (h - 30);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.globalAlpha = 0.85;
    ctx.stroke(); ctx.globalAlpha = 1;
  }
  drawLine(zHistory2, '#f472b6');
  drawLine(zHistory1, '#38bdf8');

  // 현재 시간 표시
  ctx.fillStyle = '#475569'; ctx.font = '10px sans-serif';
  ctx.fillText(`t = ${t.toFixed(1)}`, w - 60, h - 6);
}

function drawDiffGraph() {
  const cv = document.getElementById('diffGraph');
  const w = cv.width, h = cv.height;
  const ctx = cv.getContext('2d');
  ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, w, h);

  ctx.fillStyle = '#475569'; ctx.font = '11px sans-serif';
  ctx.fillText('두 궤적의 차이 |Δx|', 8, 14);

  if (diffHistory.length < 2) return;
  const maxD = Math.max(...diffHistory, 0.01);
  ctx.beginPath();
  diffHistory.forEach((v, i) => {
    const x = (i / (MAX_HIST - 1)) * (w - 20) + 10;
    const y = h - 16 - (v / maxD) * (h - 24);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  // 색상 그라데이션 (지수 성장 느낌)
  const grad = ctx.createLinearGradient(10, 0, w-10, 0);
  grad.addColorStop(0, '#22c55e'); grad.addColorStop(0.5, '#f59e0b'); grad.addColorStop(1, '#ef4444');
  ctx.strokeStyle = grad; ctx.lineWidth = 2; ctx.stroke();
}

function drawAll() { drawZGraph(); drawDiffGraph(); }

function loop(ts) {
  if (!running) return;
  if (!lastTs) lastTs = ts;
  const dt = Math.min((ts - lastTs) / 1000, 0.05);
  lastTs = ts;
  step(dt);
  drawAll();
  animId = requestAnimationFrame(loop);
}

function startSim() {
  if (running) return;
  if (!state1) initStates();
  running = true; lastTs = null;
  document.getElementById('runBtn').disabled = true;
  document.getElementById('stopBtn').disabled = false;
  animId = requestAnimationFrame(loop);
}
function stopSim() {
  running = false;
  if (animId) cancelAnimationFrame(animId);
  document.getElementById('runBtn').disabled = false;
  document.getElementById('stopBtn').disabled = true;
}
function resetSim() {
  stopSim();
  initStates();
  drawAll();
  document.getElementById('runBtn').disabled = false;
}

// ── 슬라이더 ─────────────────────────────────────
document.getElementById('deltaR').addEventListener('input', function() {
  delta = Math.pow(10, +this.value);
  document.getElementById('deltaV').textContent = delta.toExponential(0);
  resetSim();
});
document.getElementById('sigmaR').addEventListener('input', function() {
  sigma = +this.value;
  document.getElementById('sigmaV').textContent = sigma;
  resetSim();
});
document.getElementById('rhoR').addEventListener('input', function() {
  rho = +this.value;
  document.getElementById('rhoV').textContent = rho;
  resetSim();
});
document.getElementById('betaR').addEventListener('input', function() {
  beta = +this.value;
  document.getElementById('betaV').textContent = beta;
  resetSim();
});

// 초기 표시 업데이트
document.getElementById('deltaV').textContent = delta.toExponential(0);

// 캔버스 크기 맞추기
function resizeCanvases() {
  ['zGraph','diffGraph'].forEach(id => {
    const cv = document.getElementById(id);
    const w = cv.parentElement.clientWidth;
    cv.width = Math.max(w, 200);
  });
  drawAll();
}
window.addEventListener('resize', resizeCanvases);

initStates();
resizeCanvases();
drawAll();
</script>
</body>
</html>
"""


def render():
    st.title("🦋 나비효과 — 로렌츠의 기상 모델")
    st.markdown(
        """
        1961년 기상학자 **에드워드 로렌츠**는 기상 시뮬레이션을 재실행하기 위해  
        소수점 아래를 약간 반올림한 숫자를 입력했습니다.  
        그런데 결과는 처음과 **완전히 달랐습니다**.  
        이것이 **나비효과**의 발견 순간입니다.
        """
    )

    st.info("💡 **사용법**: δ(초기 차이) 슬라이더로 두 시뮬레이션의 시작 조건 차이를 조절하고, ▶ 시작을 눌러 관찰하세요. z 그래프에서 파란 선(원본)과 분홍 선(미세 변화)이 언제부터 갈라지는지 확인하세요!")

    components.html(HTML, height=1200, scrolling=False)

    st.markdown("---")
    st.markdown(
        """
        ### 📝 생각해보기

        1. δ = 0.001일 때와 δ = 0.000001일 때를 비교해보세요. **예측 한계(리아푸노프 시간)**가 어떻게 달라지나요?
        2. ρ(온도차) 값을 10까지 낮추면 어떻게 되나요? 카오스가 사라집니까?
        3. 로렌츠의 발견이 기상 예보에 어떤 의미를 지닐까요?
        """
    )
