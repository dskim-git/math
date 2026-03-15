import base64
import os

import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 대사들 — 숨겨진 해골 찾기",
    "description": "홀바인의 「대사들」에 숨겨진 아나모르포시스 해골을 보는 각도를 바꿔가며 직접 발견해봅니다.",
    "order": 33,
    "hidden": True,
}

# ──────────────────────────────────────────────────────────────────────────────
# HTML template — PLACEHOLDER_AMBASSADORS is replaced with base64 image data
# ──────────────────────────────────────────────────────────────────────────────
_TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f172a; color: #e2e8f0;
  font-family: 'Segoe UI', 'Noto Sans KR', sans-serif;
  user-select: none; -webkit-user-select: none;
}
#app { max-width: 880px; margin: 0 auto; padding: 12px; }

/* Tabs */
.tabs { display: flex; gap: 6px; margin-bottom: 12px; }
.tab-btn {
  padding: 8px 22px; border-radius: 999px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer;
  font-size: 0.85rem; font-weight: 700; transition: all .15s;
}
.tab-btn.active { background: #6d28d9; color: #ede9fe; border-color: #a78bfa; }
.tab-btn:hover:not(.active) { border-color: #475569; color: #cbd5e1; }

/* Scene layout */
.scene-row {
  display: flex; gap: 10px; align-items: flex-start; margin-bottom: 10px;
}
#main-view {
  flex: 1; min-width: 0; background: #111827;
  border: 1px solid #334155; border-radius: 10px;
  overflow: hidden; position: relative;
  display: flex; align-items: center; justify-content: center;
  min-height: 200px;
}
#mainCvs { display: block; max-width: 100%; }
#loadMsg { color: #475569; font-size: 0.9rem; padding: 40px; }

/* Minimap */
.minimap-wrap {
  flex-shrink: 0; width: 152px;
  background: #1e293b; border: 1px solid #334155;
  border-radius: 10px; padding: 8px 6px 6px;
}
#mmCvs { display: block; }
.mm-title {
  text-align: center; font-size: 0.7rem; color: #64748b;
  margin-top: 4px; font-weight: 600;
}

/* Controls */
.controls {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 10px; padding: 12px 14px; margin-bottom: 8px;
}
.angle-display {
  text-align: center; font-size: 1rem; font-weight: 800;
  color: #a78bfa; margin-bottom: 8px;
}
.slider-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.sl-lbl { font-size: 0.72rem; color: #64748b; white-space: nowrap; }
#angleSlider { flex: 1; accent-color: #8b5cf6; cursor: pointer; height: 6px; }
.btn-row { display: flex; gap: 8px; flex-wrap: wrap; }
.ctrl-btn {
  padding: 7px 14px; border-radius: 8px; border: 1.5px solid #334155;
  background: #0f172a; color: #94a3b8; cursor: pointer;
  font-size: 0.78rem; font-weight: 700; transition: all .15s; white-space: nowrap;
}
.ctrl-btn:hover { border-color: #8b5cf6; color: #ddd6fe; }
.ctrl-btn.on { background: #4c1d95; color: #ede9fe; border-color: #8b5cf6; }

/* Status bar */
.status-bar {
  padding: 9px 13px; background: #0f172a;
  border-left: 4px solid #6d28d9; border-radius: 8px;
  font-size: 0.79rem; color: #94a3b8; line-height: 1.6;
  transition: border-color .3s, color .3s;
}
.status-bar.found { border-color: #f59e0b; color: #fde68a; }

/* Discovery popup */
#disco {
  display: none; position: fixed; inset: 0;
  background: rgba(0,0,0,.72); z-index: 200;
  align-items: center; justify-content: center;
}
#disco.show { display: flex; }
.disco-box {
  background: #1a1a2e; border: 2px solid #f59e0b;
  border-radius: 16px; padding: 28px 36px; text-align: center;
  max-width: 400px; animation: pop .3s ease-out; margin: 12px;
}
@keyframes pop { from { transform: scale(.7); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.disco-box .di { font-size: 2.8rem; margin-bottom: 10px; }
.disco-box h2 { color: #fde68a; font-size: 1.2rem; margin-bottom: 8px; }
.disco-box p  { color: #cbd5e1; font-size: 0.82rem; line-height: 1.7; margin-bottom: 14px; }
.disco-close {
  padding: 8px 22px; background: #f59e0b; border: none; border-radius: 8px;
  color: #1a1a2e; font-size: 0.88rem; font-weight: 800; cursor: pointer;
}
.disco-close:hover { background: #fbbf24; }

/* Math panel */
#math-panel { display: none; }
#math-panel.show { display: block; }
.mp { background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 14px 16px; }
.ms { margin-bottom: 16px; }
.mt { font-size: 0.88rem; font-weight: 800; color: #a78bfa; margin-bottom: 5px; }
.mb { font-size: 0.8rem; color: #94a3b8; line-height: 1.75; }
.mf {
  background: #1e293b; border: 1px solid #334155; border-radius: 8px;
  padding: 9px 14px; margin: 7px 0;
  font-family: 'Courier New', monospace; font-size: 0.9rem;
  color: #7dd3fc; text-align: center;
}
.hl { color: #f59e0b; font-weight: 700; }

/* cos calc */
.cos-box {
  background: #1e293b; border: 1px solid #475569;
  border-radius: 8px; padding: 11px 14px; margin-top: 10px;
}
.cos-ht { font-size: 0.8rem; font-weight: 700; color: #5eead4; margin-bottom: 7px; }
.cos-row { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.cos-row label { font-size: 0.76rem; color: #64748b; min-width: 54px; }
#cosSlider { flex: 1; accent-color: #14b8a6; }
#cosOut {
  font-size: 0.82rem; background: #0f172a;
  border-radius: 6px; padding: 7px 11px;
}

@media (max-width: 560px) {
  .scene-row { flex-direction: column; }
  .minimap-wrap { width: 100%; }
  #mmCvs { margin: 0 auto; display: block; }
}
</style>
</head>
<body>
<div id="app">

<div class="tabs">
  <button class="tab-btn active" id="tabSim">🎨 시뮬레이션</button>
  <button class="tab-btn" id="tabMath">📐 수학 원리</button>
</div>

<!-- ── Simulation ───────────────────────────────────────────────── -->
<div id="sim-panel">
  <div class="scene-row">
    <div id="main-view">
      <div id="loadMsg">이미지 불러오는 중…</div>
      <canvas id="mainCvs" style="display:none"></canvas>
    </div>
    <div class="minimap-wrap">
      <canvas id="mmCvs" width="140" height="120"></canvas>
      <div class="mm-title">위에서 본 관람 위치</div>
    </div>
  </div>

  <div class="controls">
    <div class="angle-display" id="angDisp">👁 정면 (0°)</div>
    <div class="slider-row">
      <span class="sl-lbl">정면 👁</span>
      <input type="range" id="angleSlider" min="0" max="76" value="0" step="1">
      <span class="sl-lbl">측면 👁</span>
    </div>
    <div class="btn-row">
      <button class="ctrl-btn" id="btnAnim">▶ 자동 이동</button>
      <button class="ctrl-btn" id="btnHint">💀 해골 힌트</button>
      <button class="ctrl-btn" id="btnReset">↺ 초기화</button>
    </div>
    <div class="slider-row" style="margin-top:8px;margin-bottom:0">
      <span class="sl-lbl">🐢 느리게</span>
      <input type="range" id="speedSlider" min="1" max="10" value="3" step="1" style="flex:1;accent-color:#a78bfa;height:6px;cursor:pointer">
      <span class="sl-lbl">빠르게 🐇</span>
    </div>
  </div>

  <div class="status-bar" id="statusBar">
    정면에서는 그림 하단에 이상한 대각선 얼룩처럼 보이는 부분이 있습니다.
    슬라이더를 오른쪽으로 밀어 측면에서 감상해보세요!
  </div>
</div>

<!-- ── Math panel ─────────────────────────────────────────────────── -->
<div id="math-panel">
<div class="mp">
  <div class="ms">
    <div class="mt">🎭 아나모르포시스(Anamorphosis)란?</div>
    <div class="mb">
      특정 각도로 바라볼 때만 올바른 형상이 드러나도록
      <span class="hl">의도적으로 왜곡된 그림</span>을 말합니다.
      「대사들」의 해골은 그림을 오른쪽에서 비스듬히 바라보아야 비로소 해골로 보입니다.
      정면에서 보면 그저 이상한 대각선 얼룩처럼 보입니다.
    </div>
  </div>

  <div class="ms">
    <div class="mt">📐 원근 압축의 수학</div>
    <div class="mb">
      관람객이 수직 정면에서 각도 <span class="hl">θ</span>만큼 비껴서 볼 때,
      그림의 수평 방향은 <span class="hl">cos θ</span>배로 압축되어 보입니다.
    </div>
    <div class="mf">보이는 너비 = 실제 너비 × cos θ</div>
    <div class="mb">
      따라서 화가가 측면 θ각도에서 정상으로 보이게 하려면,
      가로를 <span class="hl">1 / cos θ</span>배로 늘려 그려야 합니다.
    </div>
    <div class="mf">필요 늘림 배율 = 1 / cos θ</div>
    <div class="mb">
      「대사들」에서 해골이 제대로 보이는 각도는 약 <span class="hl">θ ≈ 75°</span>입니다:
    </div>
    <div class="mf">1 / cos 75° ≈ 1 / 0.259 ≈ <span class="hl">3.86배</span></div>
    <div class="mb">
      홀바인은 실제 해골 너비의 약 <span class="hl">3.86배</span>로 가로 방향만 잡아늘려
      납작한 타원 형태로 그려 넣었습니다. 75° 측면에서 보면 그 압축이 상쇄되어
      정상적인 해골 모양으로 보이는 것입니다.
    </div>

    <div class="cos-box">
      <div class="cos-ht">🔢 직접 계산해보기</div>
      <div class="cos-row">
        <label>각도 θ</label>
        <input type="range" id="cosSlider" min="0" max="89" value="75" step="1">
        <span id="cosAngle" style="font-size:.82rem;color:#e2e8f0;min-width:28px">75°</span>
      </div>
      <div id="cosOut">—</div>
    </div>
  </div>

  <div class="ms">
    <div class="mt">🤔 홀바인은 왜 해골을 숨겼을까?</div>
    <div class="mb">
      이 그림은 1533년 두 명의 프랑스 외교관을 그린 초상화입니다.
      권력·부·지식의 상징물로 가득한 화폭 속에 <span class="hl">죽음의 상징인 해골</span>을
      숨겨 "아무리 높은 권력자도 결국 죽음은 피할 수 없다"는 메시지를 담았다고 해석됩니다.
      이는 <span class="hl">메멘토 모리(Memento Mori)</span> 사상을 반영한 것입니다.
    </div>
  </div>

  <div class="ms" style="margin-bottom:0">
    <div class="mt">🖼 작품 정보</div>
    <div class="mb">
      <b style="color:#e2e8f0">한스 홀바인 (Hans Holbein the Younger)</b>,
      「대사들 The Ambassadors」, 1533<br>
      유화 · 207 × 209.5 cm · 런던 내셔널 갤러리 소장<br>
      좌: 장 드 댕트빌 / 우: 조르주 드 셀브
    </div>
  </div>
</div>
</div>

<!-- ── Discovery popup ───────────────────────────────────────────── -->
<div id="disco">
  <div class="disco-box">
    <div class="di">💀</div>
    <h2>해골을 발견했습니다!</h2>
    <p>
      홀바인은 죽음의 상징인 해골을 아나모르포시스 기법으로 숨겨두었습니다.<br>
      그림 오른쪽 <b>약 75° 측면</b>에서만 볼 수 있도록
      가로 방향으로 <b>약 3.86배</b> 늘려 그린 것입니다!
    </p>
    <button class="disco-close" id="discoClose">확인 ✓</button>
  </div>
</div>

</div><!-- #app -->

<script>
(function () {
'use strict';

/* ── Constants ────────────────────────────────────────────────────── */
const D      = 5.0;   // viewer–painting distance (painting-widths)
const SLICES = 240;   // vertical slice count for rendering

/* ── State ─────────────────────────────────────────────────────────── */
let angle      = 0;
let showHint   = false;
let animating  = false;
let animDir    = 1;
let rafId      = null;
let hintPhase  = 0;
let hintRafId  = null;
let discovered = false;
let imgLoaded  = false;

/* ── Elements ──────────────────────────────────────────────────────── */
const mainCvs    = document.getElementById('mainCvs');
const ctx        = mainCvs.getContext('2d');
const mmCvs      = document.getElementById('mmCvs');
const mCtx       = mmCvs.getContext('2d');
const loadMsg    = document.getElementById('loadMsg');
const angDisp    = document.getElementById('angDisp');
const statusBar  = document.getElementById('statusBar');
const angleSlider = document.getElementById('angleSlider');

/* ── Image ─────────────────────────────────────────────────────────── */
const img = new Image();
img.onload = () => {
  imgLoaded = true;
  loadMsg.style.display = 'none';
  mainCvs.style.display = 'block';
  fitCanvas();
  render();
};
img.onerror = () => { loadMsg.textContent = '이미지를 불러올 수 없습니다.'; };
img.src = 'data:image/jpeg;base64,' + 'PLACEHOLDER_AMBASSADORS';

/* ── Canvas sizing ─────────────────────────────────────────────────── */
function fitCanvas() {
  const w = document.getElementById('main-view').clientWidth - 2;
  const aspect = img.naturalHeight / img.naturalWidth;
  mainCvs.width  = w;
  mainCvs.height = Math.round(w * aspect);
  mainCvs.style.width  = w + 'px';
  mainCvs.style.height = Math.round(w * aspect) + 'px';
}
const ro = new ResizeObserver(() => { if (imgLoaded) { fitCanvas(); render(); } });
ro.observe(document.getElementById('main-view'));

/* ── Perspective projection ────────────────────────────────────────
 *
 *  The PAINTING is fixed on a wall.
 *  The VIEWER stands at position (D·sin θ, D·cos θ) on a horizontal arc,
 *  always looking toward the painting center at origin.
 *
 *  For a point (x_w, y_w) on the painting (x_w ∈ [-0.5, 0.5]):
 *
 *    depth   = D − x_w · sin θ
 *    screen_x = D · x_w · cos θ / depth        → ∈ [−0.5, 0.5] at θ=0
 *    screen_y = D · y_w       / depth
 *
 *  Canvas mapping (at θ=0 painting fills canvas exactly):
 *    canvas_x = cW/2 + screen_x · cW
 *    canvas_y = cH/2 + screen_y/aspect · cH
 *
 * ──────────────────────────────────────────────────────────────── */

function proj(fx, fy, sinT, cosT, aspect) {
  const x_w   = fx - 0.5;
  const y_w   = (fy - 0.5) * aspect;
  const depth = D - x_w * sinT;
  const sx    = D * x_w * cosT / depth;
  const sy    = D * y_w        / depth;
  const cW = mainCvs.width, cH = mainCvs.height;
  return {
    x: cW / 2 + sx * cW,
    y: cH / 2 + sy / aspect * cH,
  };
}

/* ── Main scene render ─────────────────────────────────────────────── */
function renderScene(θ_deg) {
  if (!imgLoaded) return;
  const θ      = θ_deg * Math.PI / 180;
  const sinT   = Math.sin(θ);
  const cosT   = Math.cos(θ);
  const cW     = mainCvs.width;
  const cH     = mainCvs.height;
  const imgW   = img.naturalWidth;
  const imgH   = img.naturalHeight;
  const aspect = imgH / imgW;

  /* Dark gallery background */
  ctx.fillStyle = '#18181b';
  ctx.fillRect(0, 0, cW, cH);

  /* Floor gradient hint */
  const floorGrad = ctx.createLinearGradient(0, cH * 0.85, 0, cH);
  floorGrad.addColorStop(0, 'rgba(0,0,0,0)');
  floorGrad.addColorStop(1, 'rgba(0,0,0,0.4)');
  ctx.fillStyle = floorGrad;
  ctx.fillRect(0, 0, cW, cH);

  ctx.imageSmoothingEnabled  = true;
  ctx.imageSmoothingQuality  = 'high';

  /* ── Slice-based perspective projection ── */
  for (let i = 0; i < SLICES; i++) {
    const x0   = i       / SLICES - 0.5;
    const x1   = (i + 1) / SLICES - 0.5;
    const xMid = (x0 + x1) / 2;

    const d0    = D - x0   * sinT;
    const d1    = D - x1   * sinT;
    const dMid  = D - xMid * sinT;

    /* Screen x for each vertical edge of slice */
    const sx0 = D * x0 * cosT / d0;
    const sx1 = D * x1 * cosT / d1;

    /* Canvas destination */
    const destX = cW / 2 + sx0 * cW;
    const destW = Math.max(0.5, (sx1 - sx0) * cW);

    /* Height: farther columns appear shorter */
    const destH = cH * D / dMid;
    const destY = (cH - destH) / 2;

    /* Source slice */
    const srcX = Math.round(i       / SLICES * imgW);
    const srcW = Math.max(1, Math.round((i + 1) / SLICES * imgW) - srcX);

    ctx.drawImage(img, srcX, 0, srcW, imgH, destX, destY, destW + 0.5, destH);
  }

  /* ── Skull hint overlay ── */
  if (showHint) {
    /*
     * Approximate skull region in painting-fraction coordinates.
     * The anamorphic skull runs diagonally across the lower-center area.
     * These bounds enclose the stretched skull shape.
     */
    const skull = [
      { fx: 0.18, fy: 0.79 },  // top-left
      { fx: 0.72, fy: 0.79 },  // top-right
      { fx: 0.72, fy: 0.93 },  // bottom-right
      { fx: 0.18, fy: 0.93 },  // bottom-left
    ];

    const pts = skull.map(({ fx, fy }) => proj(fx, fy, sinT, cosT, aspect));

    const alpha = 0.55 + 0.40 * Math.sin(hintPhase);
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth   = Math.max(2, cW * 0.0035);
    ctx.setLineDash([9, 6]);
    ctx.shadowColor = '#f59e0b';
    ctx.shadowBlur  = 14;
    ctx.beginPath();
    ctx.moveTo(pts[0].x, pts[0].y);
    pts.slice(1).forEach(p => ctx.lineTo(p.x, p.y));
    ctx.closePath();
    ctx.stroke();

    /* Label anchored to the top-right corner of the quad */
    ctx.setLineDash([]);
    ctx.shadowBlur = 0;
    ctx.fillStyle  = '#fbbf24';
    ctx.font       = `bold ${Math.max(11, cW * 0.02)}px 'Segoe UI'`;
    ctx.textAlign  = 'left';
    ctx.fillText('← 해골 영역', pts[1].x + 6, pts[1].y + 4);
    ctx.restore();
  }
}

/* ── Minimap (bird's-eye view) ──────────────────────────────────────
 *
 *  Shows the painting (horizontal bar) at the top and the viewer
 *  moving along a semicircular arc below it.
 *
 * ─────────────────────────────────────────────────────────────────── */
function drawMinimap(θ_deg) {
  const mW  = mmCvs.width;
  const mH  = mmCvs.height;
  const θ   = θ_deg * Math.PI / 180;
  const cx  = mW / 2;      // painting center x
  const py  = 22;          // painting y
  const R   = 72;          // arc radius (px)
  const pw  = 80;          // half-painting width (px)

  mCtx.clearRect(0, 0, mW, mH);

  /* Background */
  mCtx.fillStyle = '#0f172a';
  mCtx.fillRect(0, 0, mW, mH);

  /* Arc (viewer path) */
  mCtx.strokeStyle = '#334155';
  mCtx.lineWidth   = 1;
  mCtx.setLineDash([4, 4]);
  mCtx.beginPath();
  mCtx.arc(cx, py, R, 0, Math.PI);
  mCtx.stroke();
  mCtx.setLineDash([]);

  /* Angle sweep fill */
  if (θ_deg > 0) {
    mCtx.fillStyle = 'rgba(139,92,246,0.12)';
    mCtx.beginPath();
    mCtx.moveTo(cx, py);
    mCtx.arc(cx, py, R, Math.PI / 2, Math.PI / 2 + θ);
    mCtx.closePath();
    mCtx.fill();
  }

  /* Painting wall */
  mCtx.strokeStyle = '#94a3b8';
  mCtx.lineWidth   = 5;
  mCtx.lineCap     = 'round';
  mCtx.beginPath();
  mCtx.moveTo(cx - pw, py);
  mCtx.lineTo(cx + pw, py);
  mCtx.stroke();
  mCtx.lineCap = 'butt';

  /* "그림" label */
  mCtx.fillStyle  = '#fbbf24';
  mCtx.font       = 'bold 9px Segoe UI';
  mCtx.textAlign  = 'center';
  mCtx.fillText('그림', cx, py - 8);

  /* Viewing line (viewer → painting center) */
  const vx = cx + R * Math.sin(θ);
  const vy = py + R * Math.cos(θ);

  mCtx.strokeStyle = '#7dd3fc';
  mCtx.lineWidth   = 1.5;
  mCtx.setLineDash([5, 4]);
  mCtx.beginPath();
  mCtx.moveTo(vx, vy);
  mCtx.lineTo(cx, py);
  mCtx.stroke();
  mCtx.setLineDash([]);

  /* Viewer dot */
  mCtx.fillStyle = '#f43f5e';
  mCtx.beginPath();
  mCtx.arc(vx, vy, 6, 0, Math.PI * 2);
  mCtx.fill();

  /* Viewer eye icon direction line */
  const eyeAngle = Math.atan2(cx - vx, py - vy);
  const ex = vx + 12 * Math.sin(eyeAngle);
  const ey = vy + 12 * Math.cos(eyeAngle);
  mCtx.strokeStyle = '#f43f5e';
  mCtx.lineWidth   = 2;
  mCtx.beginPath();
  mCtx.moveTo(vx, vy);
  mCtx.lineTo(ex, ey);
  mCtx.stroke();

  /* "관람객" label */
  const offRight = vx >= cx;
  mCtx.fillStyle = '#f43f5e';
  mCtx.font      = '9px Segoe UI';
  mCtx.textAlign = offRight ? 'left' : 'right';
  mCtx.fillText('관람객', vx + (offRight ? 10 : -10), vy + (vy > py + 30 ? 14 : -6));

  /* Angle label */
  mCtx.fillStyle  = '#a78bfa';
  mCtx.font       = 'bold 12px Segoe UI';
  mCtx.textAlign  = 'center';
  mCtx.fillText(Math.round(θ_deg) + '°', mW / 2, mH - 6);
}

/* ── Combined render ────────────────────────────────────────────────── */
function render() {
  renderScene(angle);
  drawMinimap(angle);
}

/* ── Hint pulse loop ────────────────────────────────────────────────── */
function startHintLoop() {
  if (hintRafId) cancelAnimationFrame(hintRafId);
  (function loop() {
    hintPhase += 0.07;
    if (imgLoaded) renderScene(angle);
    if (showHint) hintRafId = requestAnimationFrame(loop);
  })();
}

/* ── Status messages ────────────────────────────────────────────────── */
const STATUS_MSGS = [
  [0,  0,  '정면에서는 그림 하단에 이상한 대각선 얼룩처럼 보이는 부분이 있습니다. 슬라이더를 오른쪽으로 밀어 측면에서 감상해보세요!'],
  [1,  34, '비스듬한 각도에서 바라보고 있습니다. 그림 하단의 이상한 모양을 집중해서 보세요. 무엇처럼 보이기 시작하나요?'],
  [35, 59, '반쯤 측면에서 보고 있습니다. 가로로 납작했던 모양이 점점 어떤 형체로 바뀌고 있나요?'],
  [60, 76, '💀 충분한 측면 각도입니다. 해골의 형체가 보이기 시작했나요? 홀바인이 1533년에 숨겨놓은 비밀입니다!'],
];

function updateStatus(a) {
  for (const [lo, hi, txt] of STATUS_MSGS) {
    if (a >= lo && a <= hi) {
      statusBar.textContent = txt;
      statusBar.classList.toggle('found', a >= 60);
      break;
    }
  }
  if (a === 0) angDisp.textContent = '👁 정면 (0°)';
  else if (a < 60) angDisp.textContent = `👁 ${a}° 각도에서 감상 중`;
  else angDisp.textContent = `🔍 ${a}° 측면 감상 중`;

  if (a >= 63 && !discovered) {
    discovered = true;
    document.getElementById('disco').classList.add('show');
  }
}

/* ── Slider ─────────────────────────────────────────────────────────── */
angleSlider.addEventListener('input', e => {
  if (animating) stopAnim();
  angle = +e.target.value;
  updateStatus(angle);
  render();
});

/* ── Auto-animate ────────────────────────────────────────────────────── */
const btnAnim = document.getElementById('btnAnim');
btnAnim.addEventListener('click', () => animating ? stopAnim() : startAnim());

function startAnim() {
  animating = true;
  animDir   = 1;
  btnAnim.classList.add('on');
  btnAnim.textContent = '⏸ 멈추기';
  (function step() {
    angle += animDir * (+document.getElementById('speedSlider').value * 0.18);
    if (angle >= 76) { angle = 76; animDir = -1; }
    if (angle <=  0) { angle  = 0; animDir =  1; }
    angleSlider.value = angle;
    updateStatus(angle);
    render();
    rafId = requestAnimationFrame(step);
  })();
}

function stopAnim() {
  animating = false;
  cancelAnimationFrame(rafId);
  btnAnim.classList.remove('on');
  btnAnim.textContent = '▶ 자동 이동';
}

/* ── Hint toggle ─────────────────────────────────────────────────────── */
const btnHint = document.getElementById('btnHint');
btnHint.addEventListener('click', () => {
  showHint = !showHint;
  btnHint.classList.toggle('on', showHint);
  if (showHint) startHintLoop();
  else { cancelAnimationFrame(hintRafId); if (imgLoaded) renderScene(angle); }
});

/* ── Reset ───────────────────────────────────────────────────────────── */
document.getElementById('btnReset').addEventListener('click', () => {
  if (animating) stopAnim();
  angle = 0;
  angleSlider.value = 0;
  discovered = false;
  updateStatus(0);
  render();
});

/* ── Discovery close ─────────────────────────────────────────────────── */
document.getElementById('discoClose').addEventListener('click', () => {
  document.getElementById('disco').classList.remove('show');
});

/* ── Tabs ────────────────────────────────────────────────────────────── */
document.getElementById('tabSim').addEventListener('click', () => {
  document.getElementById('sim-panel').style.display = '';
  document.getElementById('math-panel').classList.remove('show');
  document.getElementById('tabSim').classList.add('active');
  document.getElementById('tabMath').classList.remove('active');
});
document.getElementById('tabMath').addEventListener('click', () => {
  document.getElementById('sim-panel').style.display = 'none';
  document.getElementById('math-panel').classList.add('show');
  document.getElementById('tabSim').classList.remove('active');
  document.getElementById('tabMath').classList.add('active');
});

/* ── cos calculator ──────────────────────────────────────────────────── */
const cosSlider = document.getElementById('cosSlider');
const cosAngle  = document.getElementById('cosAngle');
const cosOut    = document.getElementById('cosOut');

function updateCos() {
  const θ    = +cosSlider.value;
  const rad  = θ * Math.PI / 180;
  const cosV = Math.cos(rad);
  const ratio = cosV < 0.005 ? '∞' : (1 / cosV).toFixed(3);
  cosAngle.textContent = θ + '°';
  cosOut.innerHTML =
    `cos ${θ}° ≈ <b style="color:#7dd3fc">${cosV.toFixed(4)}</b> &nbsp;→&nbsp; ` +
    `1 / cos ${θ}° ≈ <b style="color:#f59e0b">${ratio}</b>배`;
}
cosSlider.addEventListener('input', updateCos);
updateCos();

/* ── Initial state ───────────────────────────────────────────────────── */
updateStatus(0);

})();
</script>
</body>
</html>
"""


def _b64(fname: str) -> str:
    root = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "gifted_art")
    )
    with open(os.path.join(root, fname), "rb") as f:
        return base64.b64encode(f.read()).decode()


def render():
    st.header("💀 대사들 — 숨겨진 해골 찾기")
    st.caption("홀바인의 「대사들」에 담긴 아나모르포시스 해골을 보는 각도를 바꿔가며 직접 발견해봅니다.")

    with st.expander("💡 활동 안내", expanded=False):
        st.markdown(
            """
1. **시뮬레이션** 탭에서 슬라이더를 오른쪽으로 밀어 측면에서 그림을 감상해보세요.
2. 그림은 고정되어 있고, **관람객이 오른쪽으로 이동**하는 것을 시뮬레이션합니다.
3. **위에서 본 관람 위치** 미니맵으로 현재 관람 위치를 확인하세요.
4. **자동 이동** 버튼: 정면↔측면을 자동으로 왕복합니다.
5. **해골 힌트** 버튼: 그림에서 해골이 있는 영역을 표시합니다.
6. **수학 원리** 탭에서 cos θ 압축 공식을 직접 계산해볼 수 있습니다.
            """
        )

    try:
        img_b64 = _b64("Ambassadors.jpg")
    except Exception:
        st.error("assets/gifted_art/Ambassadors.jpg 파일을 찾을 수 없습니다.")
        return

    html = _TEMPLATE.replace("PLACEHOLDER_AMBASSADORS", img_b64)
    components.html(html, height=1200, scrolling=True)
