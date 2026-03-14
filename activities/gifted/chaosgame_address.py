import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 카오스 게임으로 이해하는 시에르핀스키 삼각형",
    "description": "L, T, R 주소와 중점 이동 규칙을 따라가며 카오스 게임의 결과가 왜 시에르핀스키 삼각형이 되는지 탐구합니다.",
    "order": 27,
    "hidden": True,
}

HTML = r"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f172a;
  color: #e2e8f0;
  font-family: 'Segoe UI', 'Noto Sans KR', sans-serif;
}
#app { max-width: 980px; margin: 0 auto; padding: 12px; }
.tabs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
.tab-btn {
  padding: 7px 14px; border-radius: 999px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer;
  font-size: 0.82rem; font-weight: 700; transition: all .15s;
}
.tab-btn.active { background: #0f766e; color: #ecfeff; border-color: #14b8a6; }
.pane { display: none; }
.pane.active { display: block; }
.card {
  background: #1e293b; border: 1px solid #334155; border-radius: 14px;
  padding: 14px; margin-bottom: 12px;
}
.title {
  font-size: 1rem; font-weight: 800; color: #f8fafc; margin-bottom: 8px;
}
.sub {
  font-size: 0.82rem; color: #94a3b8; line-height: 1.7; margin-bottom: 10px;
}
.controls { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.btn {
  padding: 8px 14px; border-radius: 10px; border: 1px solid #334155;
  background: #0f172a; color: #e2e8f0; cursor: pointer; font-weight: 700;
  transition: all .15s;
}
.btn:hover { border-color: #14b8a6; color: #ccfbf1; }
.btn.vertex-l { border-color: #f59e0b; color: #fde68a; }
.btn.vertex-t { border-color: #38bdf8; color: #bae6fd; }
.btn.vertex-r { border-color: #f43f5e; color: #fecdd3; }
.badge-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.badge {
  background: #0f172a; border: 1px solid #334155; border-radius: 999px;
  padding: 6px 10px; font-size: 0.78rem; color: #cbd5e1;
}
.kbd {
  display: inline-block; min-width: 22px; text-align: center; border-radius: 6px;
  padding: 1px 6px; font-weight: 800; color: #0f172a; margin: 0 3px;
}
.kbd.l { background: #f59e0b; }
.kbd.t { background: #38bdf8; }
.kbd.r { background: #f43f5e; color: #fff; }
#traceWrap, #stageWrap { background: #0f172a; border-radius: 14px; padding: 8px; }
#traceWrap svg, #stageWrap svg { width: 100%; height: auto; display: block; }
.explain {
  background: #0f172a; border-left: 4px solid #14b8a6; border-radius: 10px;
  padding: 12px 14px; color: #cbd5e1; font-size: 0.82rem; line-height: 1.8;
}
.grid2 {
  display: grid; grid-template-columns: 1.35fr 1fr; gap: 12px;
}
.stat-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 10px 0;
}
.stat {
  background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 12px; text-align: center;
}
.stat .lbl { font-size: 0.72rem; color: #64748b; margin-bottom: 4px; }
.stat .val { font-size: 1.2rem; font-weight: 900; color: #5eead4; }
.stage-ctrl { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 10px; }
.range { width: 220px; accent-color: #14b8a6; }
#cloudCanvas {
  width: 100%; max-width: 620px; height: auto; display: block;
  background: #0b1220; border-radius: 14px; border: 1px solid #334155;
}
.note {
  font-size: 0.78rem; color: #94a3b8; line-height: 1.7; margin-top: 8px;
}
.prefix-box {
  background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 12px;
}
.prefix-line { font-size: 0.82rem; color: #cbd5e1; line-height: 1.8; }
@media (max-width: 800px) {
  .grid2 { grid-template-columns: 1fr; }
  .stat-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<div id="app">
  <div class="tabs">
    <button class="tab-btn active" data-tab="trace">① 주소 추적</button>
    <button class="tab-btn" data-tab="stage">② 단계와 주소</button>
    <button class="tab-btn" data-tab="cloud">③ 무작위 실험</button>
  </div>

  <div id="pane-trace" class="pane active">
    <div class="card">
      <div class="title">주소 L, T, R를 따라가면 점의 위치가 계속 좁혀진다</div>
      <div class="sub">
        시작점은 삼각형 내부의 임의의 점입니다. 이후 꼭짓점 쪽으로 <strong>중점 이동</strong>을 반복하면,
        점은 무작위로 움직이는 것처럼 보여도 사실은 <strong>주소</strong>가 정한 작은 삼각형 안으로 계속 들어갑니다.
      </div>
      <div class="badge-row">
        <div class="badge">주사위 1,2 → <span class="kbd l">L</span></div>
        <div class="badge">주사위 3,4 → <span class="kbd t">T</span></div>
        <div class="badge">주사위 5,6 → <span class="kbd r">R</span></div>
      </div>
      <div class="controls">
        <button class="btn" id="resetRandomBtn">새 시작점</button>
        <button class="btn" id="undoBtn">한 단계 뒤로</button>
        <button class="btn" id="clearBtn">주소 초기화</button>
        <button class="btn" id="presetRBtn">예시 R</button>
        <button class="btn" id="presetLRBtn">예시 LR</button>
        <button class="btn" id="presetTLRBtn">예시 TLR</button>
      </div>
      <div class="controls">
        <button class="btn vertex-l" data-add="L">L로 이동</button>
        <button class="btn vertex-t" data-add="T">T로 이동</button>
        <button class="btn vertex-r" data-add="R">R로 이동</button>
      </div>
      <div class="grid2">
        <div id="traceWrap"></div>
        <div>
          <div class="stat-grid">
            <div class="stat"><div class="lbl">현재 주소</div><div class="val" id="addrText">없음</div></div>
            <div class="stat"><div class="lbl">이동 횟수</div><div class="val" id="stepText">0</div></div>
            <div class="stat"><div class="lbl">가능 영역</div><div class="val" id="countText">1개</div></div>
          </div>
          <div class="explain" id="traceExplain"></div>
        </div>
      </div>
    </div>
  </div>

  <div id="pane-stage" class="pane">
    <div class="card">
      <div class="title">주소 길이가 n이면 가능한 작은 삼각형은 3ⁿ개</div>
      <div class="sub">
        길이 1의 주소는 L, T, R 세 개이고, 길이 2의 주소는 LL, LT, LR, ..., RR처럼 9개가 됩니다.
        즉, 단계가 하나 늘 때마다 가능한 주소가 3배로 늘어나고, 각 삼각형의 한 변 길이는 1/2배가 됩니다.
      </div>
      <div class="stage-ctrl">
        <span>단계 n</span>
        <input class="range" id="stageSlider" type="range" min="0" max="6" value="0">
        <strong id="stageLabel">0</strong>
      </div>
      <div id="stageWrap"></div>
      <div class="stat-grid">
        <div class="stat"><div class="lbl">주소 개수</div><div class="val" id="stageCount">1</div></div>
        <div class="stat"><div class="lbl">한 변 길이</div><div class="val" id="stageSide">1</div></div>
        <div class="stat"><div class="lbl">남는 넓이</div><div class="val" id="stageArea">1</div></div>
      </div>
      <div class="explain" id="stageExplain"></div>
    </div>
  </div>

  <div id="pane-cloud" class="pane">
    <div class="card">
      <div class="title">무작위로 던져도 점들은 시에르핀스키 삼각형 영역으로 끌려든다</div>
      <div class="sub">
        아래 실험은 무작위로 L, T, R를 선택해 중점 이동을 반복한 결과입니다.
        처음에는 흩어져 보이지만, 충분히 반복하면 점들이 특정 주소 삼각형들 안에만 남게 됩니다.
      </div>
      <div class="controls">
        <button class="btn" data-cloud="200">200개</button>
        <button class="btn" data-cloud="1000">1000개</button>
        <button class="btn" data-cloud="5000">5000개</button>
        <button class="btn" data-cloud="15000">15000개</button>
        <button class="btn" id="cloudReseedBtn">다시 생성</button>
      </div>
      <canvas id="cloudCanvas" width="620" height="520"></canvas>
      <div class="prefix-box" style="margin-top:10px;">
        <div class="prefix-line"><strong>핵심 해석</strong></div>
        <div class="prefix-line" id="cloudExplain"></div>
      </div>
      <div class="note">
        점 하나하나는 무작위로 찍히지만, 각 점은 결국 어떤 주소열 L/T/R...의 규칙을 따릅니다.
        그래서 전체 집합은 아무 곳에나 퍼지지 않고, 반복된 주소 분할의 공통 부분인 시에르핀스키 삼각형으로 모입니다.
      </div>
    </div>
  </div>
</div>

<script>
(function(){
"use strict";

const W = 620, H = 420;
const L = { x: 90,  y: 360, label: 'L', color: '#f59e0b' };
const T = { x: 310, y: 42,  label: 'T', color: '#38bdf8' };
const R = { x: 530, y: 360, label: 'R', color: '#f43f5e' };
const V = { L, T, R };

let startPoint = randomPointInTriangle();
let sequence = [];
let history = [startPoint];
let cloudSeed = 1;

function midpoint(a, b) {
  return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
}

function randomPointInTriangle() {
  let u = Math.random();
  let v = Math.random();
  if (u + v > 1) {
    u = 1 - u;
    v = 1 - v;
  }
  const w = 1 - u - v;
  return {
    x: u * L.x + v * T.x + w * R.x,
    y: u * L.y + v * T.y + w * R.y,
  };
}

function addressTriangle(seq) {
  let tri = [L, T, R];
  for (const ch of seq) {
    tri = tri.map(point => midpoint(point, V[ch]));
  }
  return tri;
}

function addStep(ch) {
  const curr = history[history.length - 1];
  const next = midpoint(curr, V[ch]);
  sequence.push(ch);
  history.push(next);
  renderTrace();
}

function runPreset(seqText) {
  sequence = [];
  history = [startPoint];
  for (const ch of seqText) addStep(ch);
}

function formatAddress(seq) {
  return seq.length ? seq.join('') : '없음';
}

function triToPoints(tri) {
  return tri.map(p => `${p.x},${p.y}`).join(' ');
}

function renderTrace() {
  const addr = formatAddress(sequence);
  const tri = addressTriangle(sequence);
  const lines = [];
  for (let i = 0; i < history.length - 1; i++) {
    lines.push(`<line x1="${history[i].x}" y1="${history[i].y}" x2="${history[i+1].x}" y2="${history[i+1].y}" stroke="#a3e635" stroke-width="2.2" opacity="0.85" />`);
  }
  const dots = history.map((p, i) => {
    const fill = i === 0 ? '#fde047' : i === history.length - 1 ? '#2563eb' : '#facc15';
    const r = i === history.length - 1 ? 6.2 : 5.3;
    return `<circle cx="${p.x}" cy="${p.y}" r="${r}" fill="${fill}" stroke="#0f172a" stroke-width="1.5" />`;
  }).join('');

  const svg = `
    <svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
      <polygon points="${triToPoints([L,T,R])}" fill="#111827" stroke="#475569" stroke-width="2" />
      <polygon points="${triToPoints(tri)}" fill="rgba(20,184,166,0.28)" stroke="#2dd4bf" stroke-width="2.2" />
      <line x1="${L.x}" y1="${L.y}" x2="${T.x}" y2="${T.y}" stroke="#64748b" stroke-width="1.4" />
      <line x1="${T.x}" y1="${T.y}" x2="${R.x}" y2="${R.y}" stroke="#64748b" stroke-width="1.4" />
      <line x1="${R.x}" y1="${R.y}" x2="${L.x}" y2="${L.y}" stroke="#64748b" stroke-width="1.4" />
      ${lines.join('')}
      ${dots}
      <circle cx="${L.x}" cy="${L.y}" r="7" fill="#f59e0b" /><circle cx="${T.x}" cy="${T.y}" r="7" fill="#38bdf8" /><circle cx="${R.x}" cy="${R.y}" r="7" fill="#f43f5e" />
      <text x="${L.x - 20}" y="${L.y + 6}" font-size="22" font-weight="800" fill="#f8fafc">L</text>
      <text x="${T.x - 7}" y="${T.y - 16}" font-size="22" font-weight="800" fill="#f8fafc">T</text>
      <text x="${R.x + 16}" y="${R.y + 6}" font-size="22" font-weight="800" fill="#f8fafc">R</text>
    </svg>`;
  document.getElementById('traceWrap').innerHTML = svg;
  document.getElementById('addrText').textContent = addr;
  document.getElementById('stepText').textContent = sequence.length;
  document.getElementById('countText').textContent = `${Math.pow(3, sequence.length)}개`;

  let msg = '아직 이동하지 않았으므로 점은 큰 삼각형 전체 어디에나 있을 수 있습니다.';
  if (sequence.length === 1) {
    const ch = sequence[0];
    msg = `첫 이동이 ${ch}이면, 새 점은 항상 ${ch} 주소의 절반 삼각형 안에 들어갑니다. 즉 무작위 이동이 아니라 첫 글자가 점의 위치를 즉시 제한합니다.`;
  } else if (sequence.length >= 2) {
    msg = `주소 ${addr}는 길이 ${sequence.length}의 선택 기록입니다. 점은 이제 ${sequence.length}번 연속으로 절반씩 잘린 ${addr} 영역 안에 있어야 합니다. 주소가 길어질수록 가능한 영역이 더 작아지고, 이 중첩이 시에르핀스키 삼각형을 만듭니다.`;
  }
  document.getElementById('traceExplain').textContent = msg;
}

function drawStageTriangle(svgParts, tri, depth, maxDepth) {
  if (depth === maxDepth) {
    svgParts.push(`<polygon points="${triToPoints(tri)}" fill="#b59a46" stroke="#0f172a" stroke-width="0.8" />`);
    return;
  }
  const a = tri[0], b = tri[1], c = tri[2];
  const ab = midpoint(a, b), bc = midpoint(b, c), ac = midpoint(a, c);
  drawStageTriangle(svgParts, [a, ab, ac], depth + 1, maxDepth);
  drawStageTriangle(svgParts, [ab, b, bc], depth + 1, maxDepth);
  drawStageTriangle(svgParts, [ac, bc, c], depth + 1, maxDepth);
}

function renderStage(n) {
  const svgParts = [];
  drawStageTriangle(svgParts, [L, T, R], 0, n);
  const svg = `
    <svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="${W}" height="${H}" fill="#0f172a" rx="14" />
      ${svgParts.join('')}
      <circle cx="${L.x}" cy="${L.y}" r="5.6" fill="#f59e0b" />
      <circle cx="${T.x}" cy="${T.y}" r="5.6" fill="#38bdf8" />
      <circle cx="${R.x}" cy="${R.y}" r="5.6" fill="#f43f5e" />
      <text x="${L.x - 18}" y="${L.y + 6}" font-size="19" font-weight="800" fill="#f8fafc">L</text>
      <text x="${T.x - 6}" y="${T.y - 14}" font-size="19" font-weight="800" fill="#f8fafc">T</text>
      <text x="${R.x + 14}" y="${R.y + 6}" font-size="19" font-weight="800" fill="#f8fafc">R</text>
    </svg>`;
  document.getElementById('stageWrap').innerHTML = svg;
  document.getElementById('stageLabel').textContent = n;
  document.getElementById('stageCount').textContent = Math.pow(3, n);
  document.getElementById('stageSide').textContent = n === 0 ? '1' : `1/${Math.pow(2,n)}`;
  const areaNum = Math.pow(3, n);
  const areaDen = Math.pow(4, n);
  document.getElementById('stageArea').textContent = n === 0 ? '1' : `${areaNum}/${areaDen}`;
  document.getElementById('stageExplain').textContent = `단계 ${n}에서는 길이 ${n}의 주소가 모두 등장합니다. 주소 하나는 작은 삼각형 하나에 대응하므로 총 ${Math.pow(3, n)}개의 삼각형이 남고, 각 삼각형의 한 변 길이는 1/${Math.pow(2, n)}가 됩니다. 따라서 남는 넓이는 (3/4)^${n} 입니다.`;
}

function mulberry32(a) {
  return function() {
    let t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function renderCloud(total) {
  const canvas = document.getElementById('cloudCanvas');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#0b1220';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 1.4;
  ctx.beginPath(); ctx.moveTo(L.x, L.y); ctx.lineTo(T.x, T.y); ctx.lineTo(R.x, R.y); ctx.closePath(); ctx.stroke();

  const rand = mulberry32(cloudSeed++);
  let p = randomPointInTriangle();
  const warmup = 20;
  const counts = { L: 0, T: 0, R: 0 };

  for (let i = 0; i < total + warmup; i++) {
    const r = rand();
    let ch = 'L';
    if (r >= 1/3 && r < 2/3) ch = 'T';
    if (r >= 2/3) ch = 'R';
    p = midpoint(p, V[ch]);
    if (i >= warmup) {
      counts[ch] += 1;
      ctx.fillStyle = ch === 'L' ? 'rgba(245,158,11,0.72)' : ch === 'T' ? 'rgba(56,189,248,0.72)' : 'rgba(244,63,94,0.72)';
      ctx.fillRect(p.x, p.y, total >= 5000 ? 1.4 : 2.2, total >= 5000 ? 1.4 : 2.2);
    }
  }

  ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.arc(L.x, L.y, 6, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = '#38bdf8'; ctx.beginPath(); ctx.arc(T.x, T.y, 6, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = '#f43f5e'; ctx.beginPath(); ctx.arc(R.x, R.y, 6, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = '#f8fafc'; ctx.font = 'bold 20px Segoe UI';
  ctx.fillText('L', L.x - 20, L.y + 8);
  ctx.fillText('T', T.x - 7, T.y - 15);
  ctx.fillText('R', R.x + 15, R.y + 8);

  document.getElementById('cloudExplain').textContent = `${total}개의 점을 찍어도 가운데 큰 역삼각형과 그 안의 작은 빈틈들은 계속 비어 있습니다. 이는 각 점이 매번 L, T, R 중 한 주소 삼각형으로 절반씩 들어가며, 결코 제거된 중앙 구멍 영역으로는 들어가지 못하기 때문입니다.`;
}

function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tab));
  document.querySelectorAll('.pane').forEach(pane => pane.classList.remove('active'));
  document.getElementById(`pane-${tab}`).classList.add('active');
}

Array.from(document.querySelectorAll('.tab-btn')).forEach(btn => {
  btn.addEventListener('click', () => switchTab(btn.dataset.tab));
});
Array.from(document.querySelectorAll('[data-add]')).forEach(btn => {
  btn.addEventListener('click', () => addStep(btn.dataset.add));
});
Array.from(document.querySelectorAll('[data-cloud]')).forEach(btn => {
  btn.addEventListener('click', () => renderCloud(+btn.dataset.cloud));
});

document.getElementById('resetRandomBtn').addEventListener('click', () => {
  startPoint = randomPointInTriangle();
  sequence = [];
  history = [startPoint];
  renderTrace();
});
document.getElementById('undoBtn').addEventListener('click', () => {
  if (!sequence.length) return;
  sequence.pop();
  history.pop();
  renderTrace();
});
document.getElementById('clearBtn').addEventListener('click', () => {
  sequence = [];
  history = [startPoint];
  renderTrace();
});
document.getElementById('presetRBtn').addEventListener('click', () => runPreset('R'));
document.getElementById('presetLRBtn').addEventListener('click', () => runPreset('LR'));
document.getElementById('presetTLRBtn').addEventListener('click', () => runPreset('TLR'));
document.getElementById('stageSlider').addEventListener('input', e => renderStage(+e.target.value));
document.getElementById('cloudReseedBtn').addEventListener('click', () => renderCloud(5000));

renderTrace();
renderStage(0);
renderCloud(5000);
})();
</script>
</body>
</html>
"""


def render():
    st.header("🌀 카오스 게임으로 이해하는 시에르핀스키 삼각형")
    st.caption("주소 L, T, R와 중점 이동 규칙을 따라가며, 무작위 반복이 왜 시에르핀스키 삼각형을 만드는지 탐구합니다.")

    with st.expander("💡 활동 안내", expanded=False):
        st.markdown(
            """
1. `주소 추적` 탭에서 시작점을 정한 뒤 L, T, R를 눌러 점이 어떤 작은 삼각형 안으로 들어가는지 확인합니다.
2. `예시 R`, `예시 LR`, `예시 TLR` 버튼으로 수업에서 본 주소 사례를 바로 확인합니다.
3. `단계와 주소` 탭에서 단계 $n$이 커질수록 가능한 주소 삼각형 수가 $3^n$개로 늘어나는 모습을 봅니다.
4. `무작위 실험` 탭에서 점 수를 늘려 보면, 무작위처럼 보여도 점들이 특정 영역으로만 모이는 이유를 확인할 수 있습니다.
            """
        )

    components.html(HTML, height=1260, scrolling=True)
