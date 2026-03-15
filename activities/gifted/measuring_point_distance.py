import base64
import io
import os

import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 거리점과 화가까지의 실제 거리",
    "description": "파르테논 신전·얀 베르메르·산타 마리아 노벨라 그림에서 소실점·거리점을 찾고, 자 도구로 거리를 재어 실제 거리를 유추합니다.",
    "order": 32,
    "hidden": True,
}

# ─── Generic canvas HTML template ─────────────────────────────────────────────
# Placeholders (replaced at runtime):
#   __CANVAS_W__    int      total canvas pixel width
#   __IMG_MAX_W__   int      max width for the painting/photo
#   __IMAGE_B64__   string   base64-encoded image data
#   __IMG_MIME__    string   MIME type (image/png or image/jpeg)
#   __STEPS_PANEL__ html     full steps-panel div
#   __CALC_BODY__   html     calculator input rows (no button/result)
#   __CALC_JS__     js       body of the calcBtn click handler
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
#app { max-width: 960px; margin: 0 auto; padding: 10px; }

.toolbar {
  background: #1e293b; border: 1px solid #334155; border-radius: 12px;
  padding: 8px 12px; margin-bottom: 8px;
  display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
}
.tool-group { display: flex; align-items: center; gap: 5px; }
.vsep { width: 1px; height: 26px; background: #334155; flex-shrink: 0; }
.tl-btn {
  padding: 5px 11px; border-radius: 7px; border: 1.5px solid #334155;
  background: #0f172a; color: #94a3b8; cursor: pointer;
  font-size: 0.77rem; font-weight: 700; transition: all .15s; white-space: nowrap;
}
.tl-btn.active { background: #78350f; color: #fde68a; border-color: #f59e0b; }
#btnRuler.active { background: #1e3a5f; color: #bfdbfe; border-color: #3b82f6; }
.tl-btn:hover:not(.active) { border-color: #475569; color: #cbd5e1; }
.tl-lbl { font-size: 0.72rem; color: #64748b; white-space: nowrap; }
.cswatch {
  width: 22px; height: 22px; border-radius: 5px; cursor: pointer;
  border: 2px solid transparent; transition: all .1s; flex-shrink: 0;
}
.cswatch.active { border-color: #f8fafc; transform: scale(1.2); box-shadow: 0 0 0 1px #0f172a; }
.cswatch:hover { transform: scale(1.1); }
input[type=color] {
  width: 26px; height: 26px; border: none; padding: 0;
  cursor: pointer; background: none; border-radius: 5px; overflow: hidden;
}
input[type=range] { width: 76px; accent-color: #14b8a6; }
#thickVal { font-size: 0.78rem; color: #5eead4; font-weight: 700; min-width: 14px; }
.act-btn {
  padding: 5px 11px; border-radius: 7px; border: 1.5px solid #334155;
  background: #0f172a; color: #94a3b8; cursor: pointer;
  font-size: 0.77rem; font-weight: 700; transition: all .15s; white-space: nowrap;
}
.act-btn:hover { border-color: #f43f5e; color: #fecdd3; }

.canvas-outer {
  background: #111827; border: 1px solid #334155; border-radius: 10px;
  overflow-x: auto; overflow-y: hidden; line-height: 0; position: relative;
}
#cvs { display: block; cursor: crosshair; touch-action: none; }
.canvas-loading {
  display: none; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%,-50%); font-size: 0.85rem; color: #475569;
}

.ruler-tip {
  margin-top: 6px; padding: 8px 12px; background: #1e3a5f;
  border-left: 3px solid #3b82f6; border-radius: 6px;
  font-size: 0.75rem; color: #93c5fd; display: none;
}
.ruler-color-row {
  display: flex; align-items: center; gap: 6px; margin-top: 8px; flex-wrap: wrap;
}
.ruler-color-lbl { font-size: 0.72rem; color: #64748b; white-space: nowrap; }
.rswatch {
  width: 22px; height: 22px; border-radius: 5px; cursor: pointer;
  border: 2px solid transparent; transition: all .1s; flex-shrink: 0;
}
.rswatch.active { border-color: #f8fafc; transform: scale(1.25); box-shadow: 0 0 0 1px #0f172a; }
.rswatch:hover { transform: scale(1.12); }
input[type=color]#rcpicker {
  width: 26px; height: 26px; border: none; padding: 0;
  cursor: pointer; background: none; border-radius: 5px; overflow: hidden;
}

.steps-panel {
  margin-top: 10px; background: #0f172a;
  border: 1px solid #1e3a5f; border-radius: 10px; overflow: hidden;
}
.steps-header {
  padding: 10px 14px; background: #1e293b;
  font-size: 0.88rem; font-weight: 800; color: #93c5fd;
  border-bottom: 1px solid #334155; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
}
.steps-body { padding: 14px; }
.step { display: flex; gap: 10px; margin-bottom: 12px; }
.step:last-child { margin-bottom: 0; }
.step-num {
  width: 24px; height: 24px; border-radius: 50%; background: #1e3a5f;
  color: #bfdbfe; font-size: 0.75rem; font-weight: 800;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.step-content { font-size: 0.8rem; color: #94a3b8; line-height: 1.7; }
.step-content strong { color: #bfdbfe; }
.step-content em { color: #64748b; font-style: normal; }

.calc-panel {
  margin-top: 10px; background: #022c22;
  border: 1px solid #14b8a6; border-radius: 10px; padding: 14px;
}
.calc-title { font-size: 0.88rem; font-weight: 800; color: #34d399; margin-bottom: 12px; }
.calc-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.calc-lbl { font-size: 0.78rem; color: #6ee7b7; min-width: 240px; }
.calc-input {
  width: 100px; padding: 4px 8px; border-radius: 6px;
  background: #064e3b; border: 1px solid #14b8a6; color: #ecfdf5;
  font-size: 0.8rem; text-align: right; outline: none;
}
.calc-input:focus { border-color: #34d399; }
.calc-btn {
  margin-top: 6px; padding: 7px 18px; border-radius: 7px;
  border: 1.5px solid #14b8a6; background: #065f46; color: #6ee7b7;
  cursor: pointer; font-size: 0.8rem; font-weight: 700; transition: all .15s;
}
.calc-btn:hover { background: #047857; color: #d1fae5; }
.calc-result {
  display: none; margin-top: 10px; padding: 12px;
  background: #065f46; border-radius: 8px;
  font-size: 0.8rem; color: #6ee7b7; line-height: 2;
}
.calc-result strong { color: #a7f3d0; }

@media (max-width: 600px) {
  .vsep { display: none; }
  .toolbar { gap: 6px; padding: 6px 8px; }
  .calc-lbl { min-width: unset; width: 100%; }
}
</style>
</head>
<body>
<div id="app">

<div class="toolbar">
  <div class="tool-group">
    <button class="tl-btn active" id="btnLine">📏 직선</button>
    <button class="tl-btn" id="btnFree">✏️ 자유선</button>
    <button class="tl-btn" id="btnRuler">📐 자</button>
    <button class="tl-btn" id="btnEraser">🧹 지우개</button>
  </div>
  <div class="vsep"></div>
  <div class="tool-group">
    <span class="tl-lbl">색상</span>
    <div class="cswatch active" style="background:#ef4444" data-c="#ef4444"></div>
    <div class="cswatch" style="background:#f97316" data-c="#f97316"></div>
    <div class="cswatch" style="background:#facc15" data-c="#facc15"></div>
    <div class="cswatch" style="background:#22c55e" data-c="#22c55e"></div>
    <div class="cswatch" style="background:#38bdf8" data-c="#38bdf8"></div>
    <div class="cswatch" style="background:#a78bfa" data-c="#a78bfa"></div>
    <div class="cswatch" style="background:#f8fafc" data-c="#f8fafc"></div>
    <input type="color" id="cpicker" value="#ef4444" title="직접 색상 선택">
  </div>
  <div class="vsep"></div>
  <div class="tool-group">
    <span class="tl-lbl">두께</span>
    <input type="range" id="thickSlider" min="1" max="12" value="3">
    <span id="thickVal">3</span>
  </div>
  <div class="vsep"></div>
  <div class="tool-group">
    <button class="act-btn" id="btnUndo">↩ 되돌리기</button>
    <button class="act-btn" id="btnClear">🗑 모두 지우기</button>
  </div>
</div>

<div class="ruler-tip" id="rulerTip">
  📐 <strong>자 도구</strong>: 드래그하여 자를 배치하세요. 끝점을 드래그해 조정, 우클릭으로 삭제.
  그림 밖으로 소실점이 있을 수 있으니 <strong>스크롤</strong>하여 찾아보세요.
  <div class="ruler-color-row">
    <span class="ruler-color-lbl">자 색상</span>
    <div class="rswatch active" style="background:#fbbf24" data-rc="#fbbf24"></div>
    <div class="rswatch" style="background:#f8fafc" data-rc="#f8fafc"></div>
    <div class="rswatch" style="background:#f43f5e" data-rc="#f43f5e"></div>
    <div class="rswatch" style="background:#34d399" data-rc="#34d399"></div>
    <div class="rswatch" style="background:#60a5fa" data-rc="#60a5fa"></div>
    <div class="rswatch" style="background:#e879f9" data-rc="#e879f9"></div>
    <input type="color" id="rcpicker" value="#fbbf24" title="자 색상 직접 선택">
  </div>
</div>

<div class="canvas-outer" id="cvsOuter">
  <canvas id="cvs"></canvas>
  <div class="canvas-loading" id="loadMsg">이미지 불러오는 중...</div>
</div>

__STEPS_PANEL__

<div class="calc-panel">
  <div class="calc-title">🧮 거리 계산기</div>
  __CALC_BODY__
  <button class="calc-btn" id="calcBtn">계산하기 →</button>
  <div class="calc-result" id="calcResult"></div>
</div>

</div><!-- #app -->

<script>
(function() {
'use strict';

const CANVAS_W   = __CANVAS_W__;
const IMG_MAX_W  = __IMG_MAX_W__;
const IMG_PAD_T  = 30;
const IMG_PAD_B  = 40;
const IMAGE_B64  = "__IMAGE_B64__";
const IMG_MIME   = "__IMG_MIME__";

const S = {
  tool: 'line',
  color: '#ef4444', thick: 3,
  rulerColor: '#fbbf24',
  drawing: false, sx: 0, sy: 0, freeStroke: null,
  strokes: [],
  rulers: [],
  rulerDrag: null,
  selectedRuler: -1,
  bgImg: null,
  imgX: 0, imgY: IMG_PAD_T, imgW: 0, imgH: 0,
};

const cvs = document.getElementById('cvs');
const ctx = cvs.getContext('2d');

// ── Coordinate helpers ────────────────────────────────────────────────────────
function pxCoords(e) {
  const r   = cvs.getBoundingClientRect();
  const scX = cvs.width  / r.width;
  const scY = cvs.height / r.height;
  const src = e.touches ? e.touches[0] : e;
  return { x: (src.clientX - r.left) * scX, y: (src.clientY - r.top) * scY };
}
function dist2(ax, ay, bx, by) {
  return Math.sqrt((ax-bx)**2 + (ay-by)**2);
}
function distToSeg(px, py, ax, ay, bx, by) {
  const dx = bx-ax, dy = by-ay, len2 = dx*dx + dy*dy;
  if (len2 < 1) return dist2(px, py, ax, ay);
  const t  = Math.max(0, Math.min(1, ((px-ax)*dx + (py-ay)*dy) / len2));
  return dist2(px, py, ax + t*dx, ay + t*dy);
}

// ── Image loader ──────────────────────────────────────────────────────────────
async function init() {
  document.getElementById('loadMsg').style.display = 'block';
  const img = await new Promise(res => {
    if (!IMAGE_B64) { res(null); return; }
    const i = new Image();
    i.onload  = () => res(i);
    i.onerror = () => res(null);
    i.src = 'data:' + IMG_MIME + ';base64,' + IMAGE_B64;
  });
  document.getElementById('loadMsg').style.display = 'none';
  S.bgImg = img;

  if (img) {
    const sc  = Math.min(IMG_MAX_W / img.naturalWidth, 1);
    S.imgW    = Math.round(img.naturalWidth  * sc);
    S.imgH    = Math.round(img.naturalHeight * sc);
    S.imgX    = Math.round((CANVAS_W - S.imgW) / 2);
  } else {
    S.imgW = IMG_MAX_W; S.imgH = 380;
    S.imgX = Math.round((CANVAS_W - S.imgW) / 2);
  }
  cvs.width  = CANVAS_W;
  cvs.height = S.imgY + S.imgH + IMG_PAD_B;
  cvs.style.width  = CANVAS_W + 'px';
  cvs.style.height = cvs.height + 'px';
  redraw();
}

// ── Draw helpers ──────────────────────────────────────────────────────────────
function drawStroke(c, st) {
  if (!st.pts || st.pts.length < 2) return;
  c.save();
  c.strokeStyle = st.color; c.lineWidth = st.thick;
  c.lineCap = 'round'; c.lineJoin = 'round';
  c.beginPath();
  if (st.type === 'line') {
    c.moveTo(st.pts[0].x, st.pts[0].y);
    c.lineTo(st.pts[st.pts.length-1].x, st.pts[st.pts.length-1].y);
  } else {
    c.moveTo(st.pts[0].x, st.pts[0].y);
    for (let i = 1; i < st.pts.length; i++) c.lineTo(st.pts[i].x, st.pts[i].y);
  }
  c.stroke();
  c.restore();
}

function drawRuler(c, r, selected) {
  const dx = r.x2 - r.x1, dy = r.y2 - r.y1;
  const len = Math.sqrt(dx*dx + dy*dy);
  if (len < 3) return;
  const angle = Math.atan2(dy, dx);
  const col = r.color || '#fbbf24';

  c.save();
  c.translate(r.x1, r.y1);
  c.rotate(angle);

  c.shadowColor = 'rgba(0,0,0,0.85)';
  c.shadowBlur  = 5;

  c.lineCap = 'square';
  c.strokeStyle = 'rgba(0,0,0,0.7)'; c.lineWidth = 7;
  c.beginPath(); c.moveTo(0, 0); c.lineTo(len, 0); c.stroke();
  c.strokeStyle = col; c.lineWidth = 4;
  c.beginPath(); c.moveTo(0, 0); c.lineTo(len, 0); c.stroke();

  [0, len].forEach(tx => {
    c.strokeStyle = 'rgba(0,0,0,0.7)'; c.lineWidth = 5;
    c.beginPath(); c.moveTo(tx, -13); c.lineTo(tx, 13); c.stroke();
    c.strokeStyle = col; c.lineWidth = 3;
    c.beginPath(); c.moveTo(tx, -13); c.lineTo(tx, 13); c.stroke();
  });

  c.shadowBlur = 0;
  for (let t = 0; t <= len; t += 20) {
    const h = t % 100 === 0 ? 10 : t % 50 === 0 ? 7 : 4;
    c.strokeStyle = 'rgba(0,0,0,0.6)'; c.lineWidth = 3;
    c.beginPath(); c.moveTo(t, 0); c.lineTo(t, h); c.stroke();
    c.strokeStyle = col; c.lineWidth = 1.5;
    c.beginPath(); c.moveTo(t, 0); c.lineTo(t, h); c.stroke();
  }

  c.save();
  const flip = Math.abs(angle) > Math.PI / 2;
  c.translate(len / 2, 0);
  if (flip) c.rotate(Math.PI);
  const label = Math.round(len) + ' px';
  c.font = 'bold 14px "Segoe UI", sans-serif';
  const tw = c.measureText(label).width;
  c.fillStyle = 'rgba(0,0,0,0.75)';
  c.beginPath();
  c.roundRect(-tw/2 - 6, -32, tw + 12, 20, 5);
  c.fill();
  c.fillStyle = col;
  c.textAlign = 'center'; c.textBaseline = 'alphabetic';
  c.fillText(label, 0, -15);
  c.restore();

  c.restore();

  [[r.x1, r.y1], [r.x2, r.y2]].forEach(([x, y]) => {
    c.beginPath(); c.arc(x, y, 9, 0, Math.PI*2);
    c.fillStyle = 'rgba(0,0,0,0.6)'; c.fill();
    c.beginPath(); c.arc(x, y, 7, 0, Math.PI*2);
    c.fillStyle = selected ? '#f97316' : col; c.fill();
    c.beginPath(); c.arc(x, y, 7, 0, Math.PI*2);
    c.strokeStyle = '#f8fafc'; c.lineWidth = 1.5; c.stroke();
  });
}

function redraw(previewStroke, previewRuler) {
  ctx.clearRect(0, 0, cvs.width, cvs.height);

  ctx.fillStyle = '#111827';
  ctx.fillRect(0, 0, cvs.width, cvs.height);

  if (S.bgImg) {
    ctx.drawImage(S.bgImg, S.imgX, S.imgY, S.imgW, S.imgH);
  } else {
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(S.imgX, S.imgY, S.imgW, S.imgH || 380);
    ctx.fillStyle = '#475569'; ctx.font = 'bold 16px Segoe UI';
    ctx.textAlign = 'center';
    ctx.fillText('이미지를 불러올 수 없습니다', CANVAS_W/2, S.imgY + 190);
    ctx.textAlign = 'left';
  }

  ctx.save();
  ctx.strokeStyle = '#334155'; ctx.lineWidth = 1;
  ctx.setLineDash([5, 5]);
  ctx.strokeRect(S.imgX, S.imgY, S.imgW, S.imgH);
  ctx.restore();


  S.strokes.forEach(st => drawStroke(ctx, st));
  if (previewStroke) {
    ctx.globalAlpha = 0.75;
    drawStroke(ctx, previewStroke);
    ctx.globalAlpha = 1;
  }

  S.rulers.forEach((r, i) => drawRuler(ctx, r, i === S.selectedRuler));
  if (previewRuler) {
    ctx.globalAlpha = 0.8;
    drawRuler(ctx, previewRuler, false);
    ctx.globalAlpha = 1;
  }
}

// ── Ruler hit test ────────────────────────────────────────────────────────────
function hitRuler(x, y) {
  for (let i = S.rulers.length - 1; i >= 0; i--) {
    const r = S.rulers[i];
    if (dist2(x, y, r.x1, r.y1) < 10) return { idx: i, type: 'ep1' };
    if (dist2(x, y, r.x2, r.y2) < 10) return { idx: i, type: 'ep2' };
    if (distToSeg(x, y, r.x1, r.y1, r.x2, r.y2) < 8) return { idx: i, type: 'body' };
  }
  return null;
}

// ── Pointer down ──────────────────────────────────────────────────────────────
cvs.addEventListener('pointerdown', e => {
  e.preventDefault();
  const { x, y } = pxCoords(e);

  if (S.tool === 'ruler') {
    const hit = hitRuler(x, y);
    if (hit) {
      S.selectedRuler = hit.idx;
      const r = S.rulers[hit.idx];
      S.rulerDrag = {
        type: hit.type, idx: hit.idx,
        ox: x, oy: y,
        ox1: r.x1, oy1: r.y1,
        ox2: r.x2, oy2: r.y2,
      };
    } else {
      S.selectedRuler = -1;
      S.rulerDrag = { type: 'new', x1: x, y1: y };
    }
    cvs.setPointerCapture(e.pointerId);
    redraw();
    return;
  }

  S.selectedRuler = -1;
  S.drawing = true;
  S.sx = x; S.sy = y;

  if (S.tool === 'eraser') {
    if (S.strokes.length) { S.strokes.pop(); redraw(); }
    S.drawing = false;
    return;
  }
  if (S.tool === 'free') {
    S.freeStroke = { type: 'free', color: S.color, thick: S.thick, pts: [{ x, y }] };
    S.strokes.push(S.freeStroke);
  }
  cvs.setPointerCapture(e.pointerId);
});

// ── Pointer move ──────────────────────────────────────────────────────────────
cvs.addEventListener('pointermove', e => {
  const { x, y } = pxCoords(e);

  if (S.tool === 'ruler') {
    if (S.rulerDrag) {
      const d = S.rulerDrag;
      if (d.type === 'new') {
        redraw(null, { x1: d.x1, y1: d.y1, x2: x, y2: y, color: S.rulerColor });
      } else {
        const r = S.rulers[d.idx];
        const dx = x - d.ox, dy = y - d.oy;
        if (d.type === 'ep1') { r.x1 = d.ox1 + dx; r.y1 = d.oy1 + dy; }
        else if (d.type === 'ep2') { r.x2 = d.ox2 + dx; r.y2 = d.oy2 + dy; }
        else { r.x1 = d.ox1 + dx; r.y1 = d.oy1 + dy; r.x2 = d.ox2 + dx; r.y2 = d.oy2 + dy; }
        redraw();
      }
    } else {
      const hit = hitRuler(x, y);
      cvs.style.cursor = hit
        ? (hit.type.startsWith('ep') ? 'grab' : 'move')
        : 'crosshair';
    }
    return;
  }

  if (!S.drawing) return;
  e.preventDefault();
  if (S.tool === 'line') {
    redraw({ type: 'line', color: S.color, thick: S.thick, pts: [{ x: S.sx, y: S.sy }, { x, y }] });
  } else if (S.tool === 'free' && S.freeStroke) {
    S.freeStroke.pts.push({ x, y });
    redraw();
  }
});

// ── Pointer up ────────────────────────────────────────────────────────────────
cvs.addEventListener('pointerup', e => {
  const { x, y } = pxCoords(e);

  if (S.tool === 'ruler') {
    if (S.rulerDrag) {
      const d = S.rulerDrag;
      if (d.type === 'new' && dist2(d.x1, d.y1, x, y) > 10) {
        S.rulers.push({ x1: d.x1, y1: d.y1, x2: x, y2: y, color: S.rulerColor });
        S.selectedRuler = S.rulers.length - 1;
      }
      S.rulerDrag = null;
      redraw();
    }
    return;
  }

  if (!S.drawing) return;
  S.drawing = false;
  if (S.tool === 'line') {
    const dx = x - S.sx, dy = y - S.sy;
    if (dx*dx + dy*dy > 25) {
      S.strokes.push({ type: 'line', color: S.color, thick: S.thick, pts: [{ x: S.sx, y: S.sy }, { x, y }] });
    }
    redraw();
  }
  S.freeStroke = null;
});

cvs.addEventListener('pointerleave', () => {
  if (S.drawing && S.tool === 'line') { S.drawing = false; redraw(); }
});

cvs.addEventListener('contextmenu', e => {
  e.preventDefault();
  const { x, y } = pxCoords(e);
  const hit = hitRuler(x, y);
  if (hit) {
    S.rulers.splice(hit.idx, 1);
    if (S.selectedRuler === hit.idx) S.selectedRuler = -1;
    else if (S.selectedRuler > hit.idx) S.selectedRuler--;
    redraw();
  }
});

// ── Tool buttons ──────────────────────────────────────────────────────────────
function setTool(t) {
  S.tool = t;
  const map = { btnLine: 'line', btnFree: 'free', btnRuler: 'ruler', btnEraser: 'eraser' };
  Object.entries(map).forEach(([id, val]) =>
    document.getElementById(id).classList.toggle('active', val === t)
  );
  cvs.style.cursor = t === 'eraser' ? 'cell' : 'crosshair';
  document.getElementById('rulerTip').style.display = t === 'ruler' ? 'block' : 'none';
}
document.getElementById('btnLine').addEventListener('click',   () => setTool('line'));
document.getElementById('btnFree').addEventListener('click',   () => setTool('free'));
document.getElementById('btnRuler').addEventListener('click',  () => setTool('ruler'));
document.getElementById('btnEraser').addEventListener('click', () => setTool('eraser'));

document.querySelectorAll('.rswatch').forEach(el => {
  el.addEventListener('click', () => {
    document.querySelectorAll('.rswatch').forEach(s => s.classList.remove('active'));
    el.classList.add('active');
    S.rulerColor = el.dataset.rc;
    document.getElementById('rcpicker').value = S.rulerColor;
    if (S.selectedRuler >= 0) {
      S.rulers[S.selectedRuler].color = S.rulerColor;
      redraw();
    }
  });
});
document.getElementById('rcpicker').addEventListener('input', e => {
  S.rulerColor = e.target.value;
  document.querySelectorAll('.rswatch').forEach(s => s.classList.remove('active'));
  if (S.selectedRuler >= 0) {
    S.rulers[S.selectedRuler].color = S.rulerColor;
    redraw();
  }
});

document.querySelectorAll('.cswatch').forEach(el => {
  el.addEventListener('click', () => {
    document.querySelectorAll('.cswatch').forEach(s => s.classList.remove('active'));
    el.classList.add('active');
    S.color = el.dataset.c;
    document.getElementById('cpicker').value = S.color;
  });
});
document.getElementById('cpicker').addEventListener('input', e => {
  S.color = e.target.value;
  document.querySelectorAll('.cswatch').forEach(s => s.classList.remove('active'));
});

document.getElementById('thickSlider').addEventListener('input', e => {
  S.thick = +e.target.value;
  document.getElementById('thickVal').textContent = S.thick;
});

document.getElementById('btnUndo').addEventListener('click', () => {
  if (S.tool === 'ruler' && S.rulers.length) {
    S.rulers.pop(); S.selectedRuler = -1;
  } else if (S.strokes.length) {
    S.strokes.pop();
  }
  redraw();
});
document.getElementById('btnClear').addEventListener('click', () => {
  S.strokes = []; S.rulers = []; S.selectedRuler = -1; redraw();
});

document.getElementById('stepsToggle').addEventListener('click', () => {
  const body  = document.getElementById('stepsBody');
  const arrow = document.getElementById('stepsArrow');
  const open  = body.style.display === 'block';
  body.style.display  = open ? 'none' : 'block';
  arrow.textContent   = open ? '▼' : '▲';
});

// ── Calculator ────────────────────────────────────────────────────────────────
document.getElementById('calcBtn').addEventListener('click', () => {
  __CALC_JS__
});

// ── Init ──────────────────────────────────────────────────────────────────────
init();
})();
</script>
</body>
</html>
"""


# ─── Helpers ───────────────────────────────────────────────────────────────────

def _b64(fname: str, max_w: int = 1200) -> str:
    """Load image from assets/gifted_art, resize if wider than max_w, return base64."""
    try:
        from PIL import Image  # type: ignore
        root = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "gifted_art")
        )
        fpath = os.path.join(root, fname)
        img = Image.open(fpath)
        if img.width > max_w:
            ratio = max_w / img.width
            img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        is_png = fname.lower().endswith(".png")
        if is_png:
            img.save(buf, format="PNG")
        else:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


def _steps_panel(title: str, steps: list[str]) -> str:
    items = "".join(
        f'<div class="step"><div class="step-num">{i+1}</div>'
        f'<div class="step-content">{s}</div></div>'
        for i, s in enumerate(steps)
    )
    return f"""<div class="steps-panel">
  <div class="steps-header" id="stepsToggle">
    🔍 {title} <span id="stepsArrow">▼</span>
  </div>
  <div class="steps-body" id="stepsBody" style="display:none">
    {items}
  </div>
</div>"""


def _make_html(
    img_b64: str,
    img_mime: str,
    canvas_w: int,
    img_max_w: int,
    steps_title: str,
    steps: list[str],
    calc_body: str,
    calc_js: str,
) -> str:
    return (
        _TEMPLATE
        .replace("__CANVAS_W__", str(canvas_w))
        .replace("__IMG_MAX_W__", str(img_max_w))
        .replace("__IMAGE_B64__", img_b64)
        .replace("__IMG_MIME__", img_mime)
        .replace("__STEPS_PANEL__", _steps_panel(steps_title, steps))
        .replace("__CALC_BODY__", calc_body)
        .replace("__CALC_JS__", calc_js)
    )


# ─── Tab 1: Parthenon ─────────────────────────────────────────────────────────

_PARTHENON_STEPS = [
    "<strong>📏 직선 도구</strong>로 파르테논 신전의 처마선·기둥 상단 수평선 등을 연장해 "
    "<strong>좌측·우측 소실점</strong>을 찾으세요.<br>"
    "빨간 선은 왼쪽 방향, 노란 선은 오른쪽 방향으로 구분해 그으면 좋습니다.<br>"
    "<em>소실점은 사진 밖 좌우 여백에 위치합니다 — 캔버스를 좌우로 스크롤해 확인하세요.</em>",

    "<strong>📐 자 도구</strong>를 선택해 <strong>좌측 소실점 ↔ 우측 소실점</strong> 사이 거리를 재세요.<br>"
    "드래그하면 자가 생기고 픽셀 수가 표시됩니다.<br>"
    "<em>자의 끝점(원)을 드래그해 위치를 정밀하게 조정할 수 있습니다.</em>",

    "자로 <strong>기둥의 높이</strong>(기둥 상단 → 하단)도 재세요.<br>"
    "파르테논 신전 기둥의 실제 높이는 약 <strong>11 m</strong>입니다.",

    "아래 <strong>계산기</strong>에 측정값을 입력하면 사진작가 ↔ 신전 사이의 실제 거리가 계산됩니다.<br>"
    "<em>원리: 좌/우 소실점 사이 거리의 ½ = 시점(화가)↔화면 거리, 이를 실제 축척으로 환산합니다.</em>",
]

_PARTHENON_CALC_BODY = """
  <div class="calc-row">
    <span class="calc-lbl">좌측 소실점 ↔ 우측 소실점 거리 (px)</span>
    <input type="number" class="calc-input" id="inVpDist" placeholder="자로 측정">
  </div>
  <div class="calc-row">
    <span class="calc-lbl">기둥 높이 (px)</span>
    <input type="number" class="calc-input" id="inColH" placeholder="자로 측정">
  </div>
  <div class="calc-row">
    <span class="calc-lbl">기둥 실제 높이 (m)</span>
    <input type="number" class="calc-input" id="inColReal" value="11">
  </div>
"""

_PARTHENON_CALC_JS = r"""
  const vpDist  = parseFloat(document.getElementById('inVpDist').value);
  const colH    = parseFloat(document.getElementById('inColH').value);
  const colReal = parseFloat(document.getElementById('inColReal').value) || 11;
  const res     = document.getElementById('calcResult');

  if (!vpDist || !colH || vpDist <= 0 || colH <= 0) {
    res.style.display = 'block';
    res.innerHTML = '⚠️ 소실점 간 거리와 기둥 높이를 자로 재서 입력해주세요.';
    return;
  }

  const eyePx    = vpDist / 2;
  const mPerPx   = colReal / colH;
  const realDist = eyePx * mPerPx;

  res.style.display = 'block';
  res.innerHTML = `
<strong>계산 과정</strong><br>
• 좌 ↔ 우 소실점 거리: <strong>${vpDist.toFixed(1)} px</strong><br>
• 시점 ↔ 화면 거리 (½ × VP 거리): <strong>${eyePx.toFixed(1)} px</strong><br>
• 축척: 기둥 실제 ${colReal} m ÷ ${colH.toFixed(1)} px = <strong>${mPerPx.toFixed(4)} m/px</strong><br>
• 사진작가 ↔ 신전 실제 거리 = ${eyePx.toFixed(1)} × ${mPerPx.toFixed(4)}<br>
&nbsp;&nbsp;≈ <strong style="font-size:1.15em;color:#34d399">${realDist.toFixed(1)} m</strong>
  `.trim();
"""


# ─── Tab 2: Vermeer — Allegory of the Art of Painting ────────────────────────

_VERMEER_STEPS = [
    "<strong>📏 직선 도구</strong>로 그림 속 바닥 타일의 격자선을 연장해 "
    "<strong>시심 V(소실점)</strong>를 찾으세요. V는 그림 안쪽, 수평선 위에 있습니다.",

    "<strong>📏 직선 도구</strong>로 바닥 타일의 <strong>대각선</strong>을 연장해 "
    "<strong>거리점 D</strong>를 찾으세요.<br>"
    "D는 V와 같은 수평선 위이며 그림 오른쪽 밖에 있습니다.<br>"
    "<em>캔버스를 오른쪽으로 스크롤하여 D를 찾아보세요.</em>",

    "<strong>📐 자 도구</strong>로 <strong>시심 V ↔ 거리점 D</strong> 사이의 거리를 재세요.<br>"
    "이 거리가 그림을 그릴 당시 화가 눈과 캔버스 사이의 거리에 해당합니다.",

    "<strong>📐 자 도구</strong>로 그림 속 <strong>여성의 키</strong>(발끝 → 정수리)를 재세요.<br>"
    "여성의 실제 키를 <strong>160 cm</strong>로 가정합니다.",

    "아래 <strong>계산기</strong>에 측정값을 입력하면 화가 ↔ 그림 사이의 실제 거리가 계산됩니다.<br>"
    "<em>원리: V↔D 거리(px) × (실제 키 ÷ 여성 키(px)) = 화가까지의 실제 거리</em>",
]

_VERMEER_CALC_BODY = """
  <div class="calc-row">
    <span class="calc-lbl">시심 V ↔ 거리점 D 거리 (px)</span>
    <input type="number" class="calc-input" id="inVD" placeholder="자로 측정">
  </div>
  <div class="calc-row">
    <span class="calc-lbl">그림 속 여성의 키 (px)</span>
    <input type="number" class="calc-input" id="inWomanH" placeholder="자로 측정">
  </div>
  <div class="calc-row">
    <span class="calc-lbl">여성의 실제 키 (cm)</span>
    <input type="number" class="calc-input" id="inWomanReal" value="160">
  </div>
"""

_VERMEER_CALC_JS = r"""
  const vd       = parseFloat(document.getElementById('inVD').value);
  const womanPx  = parseFloat(document.getElementById('inWomanH').value);
  const womanR   = parseFloat(document.getElementById('inWomanReal').value) || 160;
  const res      = document.getElementById('calcResult');

  if (!vd || !womanPx || vd <= 0 || womanPx <= 0) {
    res.style.display = 'block';
    res.innerHTML = '⚠️ V↔D 거리와 여성의 키를 자로 재서 입력해주세요.';
    return;
  }

  const cmPerPx  = womanR / womanPx;
  const realDist = vd * cmPerPx;

  res.style.display = 'block';
  res.innerHTML = `
<strong>계산 과정</strong><br>
• V ↔ D 거리: <strong>${vd.toFixed(1)} px</strong><br>
• 여성의 키: ${womanPx.toFixed(1)} px → 실제 ${womanR} cm<br>
• 축척: ${womanR} cm ÷ ${womanPx.toFixed(1)} px = <strong>${cmPerPx.toFixed(4)} cm/px</strong><br>
• 화가 ↔ 그림 실제 거리 = ${vd.toFixed(1)} × ${cmPerPx.toFixed(4)}<br>
&nbsp;&nbsp;≈ <strong style="font-size:1.15em;color:#34d399">${realDist.toFixed(1)} cm</strong>
&nbsp;&nbsp;(약 <strong>${(realDist/100).toFixed(2)} m</strong>)
  `.trim();
"""


# ─── Tab 3: Santa Maria Novella ───────────────────────────────────────────────

_STMARIA_STEPS = [
    "<strong>📏 직선 도구</strong>로 기둥·아치·바닥선 등을 연장해 "
    "<strong>소실점 V</strong>를 찾으세요. 정면을 향한 회랑의 중앙 수평선 위에 있습니다.",

    "<strong>📏 직선 도구</strong>로 바닥 타일의 <strong>대각선</strong>을 연장해 "
    "<strong>거리점 D</strong>를 찾으세요.<br>"
    "D는 V와 같은 수평선 위, V에서 좌측 또는 우측으로 떨어진 곳에 있습니다.<br>"
    "<em>캔버스를 스크롤해 D를 찾아보세요.</em>",

    "<strong>📐 자 도구</strong>로 <strong>소실점 V ↔ 거리점 D</strong> 사이의 거리를 재세요.",

    "<strong>📐 자 도구</strong>로 <strong>기둥의 높이</strong>(기둥 하단 → 상단 아치 시작점)를 재세요.<br>"
    "산타 마리아 노벨라 기둥의 실제 높이는 약 <strong>9 m</strong>입니다.",

    "아래 <strong>계산기</strong>에 측정값을 입력하면 사진작가 ↔ 내부 사이의 실제 거리가 계산됩니다.<br>"
    "<em>원리: V↔D 거리(px) × (실제 기둥 높이 ÷ 기둥 높이(px)) = 사진 촬영 거리</em>",
]

_STMARIA_CALC_BODY = """
  <div class="calc-row">
    <span class="calc-lbl">소실점 V ↔ 거리점 D 거리 (px)</span>
    <input type="number" class="calc-input" id="inVD" placeholder="자로 측정">
  </div>
  <div class="calc-row">
    <span class="calc-lbl">기둥 높이 (px)</span>
    <input type="number" class="calc-input" id="inColH" placeholder="자로 측정">
  </div>
  <div class="calc-row">
    <span class="calc-lbl">기둥 실제 높이 (m)</span>
    <input type="number" class="calc-input" id="inColReal" value="9">
  </div>
"""

_STMARIA_CALC_JS = r"""
  const vd      = parseFloat(document.getElementById('inVD').value);
  const colPx   = parseFloat(document.getElementById('inColH').value);
  const colReal = parseFloat(document.getElementById('inColReal').value) || 9;
  const res     = document.getElementById('calcResult');

  if (!vd || !colPx || vd <= 0 || colPx <= 0) {
    res.style.display = 'block';
    res.innerHTML = '⚠️ V↔D 거리와 기둥 높이를 자로 재서 입력해주세요.';
    return;
  }

  const mPerPx   = colReal / colPx;
  const realDist = vd * mPerPx;

  res.style.display = 'block';
  res.innerHTML = `
<strong>계산 과정</strong><br>
• V ↔ D 거리: <strong>${vd.toFixed(1)} px</strong><br>
• 기둥 높이: ${colPx.toFixed(1)} px → 실제 ${colReal} m<br>
• 축척: ${colReal} m ÷ ${colPx.toFixed(1)} px = <strong>${mPerPx.toFixed(5)} m/px</strong><br>
• 사진작가 ↔ 내부 실제 거리 = ${vd.toFixed(1)} × ${mPerPx.toFixed(5)}<br>
&nbsp;&nbsp;≈ <strong style="font-size:1.15em;color:#34d399">${realDist.toFixed(2)} m</strong>
  `.trim();
"""


# ─── render ───────────────────────────────────────────────────────────────────

def render():
    st.header("📐 거리점과 화가까지의 실제 거리")
    st.caption(
        "세 작품에서 소실점과 거리점을 찾고, 자 도구로 거리를 재어 실제 촬영·제작 거리를 유추합니다."
    )

    with st.expander("💡 활동 안내", expanded=False):
        st.markdown(
            """
1. **직선 도구**로 사진 속 평행선들을 연장해 **소실점 V**와 **거리점 D**를 찾습니다.
   - 소실점·거리점이 그림 밖에 있으면 캔버스를 **좌우 스크롤**하여 확인합니다.
2. **자(📐) 도구**로 V↔D 거리와 기준 사물의 크기를 픽셀 단위로 측정합니다.
   - 드래그하면 자가 생기고 픽셀 단위 길이가 표시됩니다.
   - 자의 끝점(원)을 드래그해 위치 조정, **우클릭**으로 자를 삭제합니다.
3. **계산기**에 측정값을 입력하면 실제 거리를 자동 계산합니다.
            """
        )

    tab1, tab2, tab3 = st.tabs([
        "파르테논 신전",
        "얀 베르메르 (회화의 알레고리)",
        "산타 마리아 노벨라",
    ])

    with tab1:
        try:
            img_b64 = _b64("parthenon.png")
            img_mime = "image/png"
        except Exception:
            img_b64 = ""
            img_mime = "image/png"
        html = _make_html(
            img_b64=img_b64,
            img_mime=img_mime,
            canvas_w=1320,
            img_max_w=620,
            steps_title="파르테논 신전 — 단계별 안내",
            steps=_PARTHENON_STEPS,
            calc_body=_PARTHENON_CALC_BODY,
            calc_js=_PARTHENON_CALC_JS,
        )
        components.html(html, height=1000, scrolling=True)

    with tab2:
        try:
            img_b64 = _b64("Allegory of the Art of Painting.jpg", max_w=1000)
            img_mime = "image/jpeg"
        except Exception:
            img_b64 = ""
            img_mime = "image/jpeg"
        html = _make_html(
            img_b64=img_b64,
            img_mime=img_mime,
            canvas_w=1600,
            img_max_w=440,
            steps_title="얀 베르메르 회화의 알레고리 — 단계별 안내",
            steps=_VERMEER_STEPS,
            calc_body=_VERMEER_CALC_BODY,
            calc_js=_VERMEER_CALC_JS,
        )
        components.html(html, height=1000, scrolling=True)

    with tab3:
        try:
            img_b64 = _b64("stmaria.jpg")
            img_mime = "image/jpeg"
        except Exception:
            img_b64 = ""
            img_mime = "image/jpeg"
        html = _make_html(
            img_b64=img_b64,
            img_mime=img_mime,
            canvas_w=1320,
            img_max_w=620,
            steps_title="산타 마리아 노벨라 — 단계별 안내",
            steps=_STMARIA_STEPS,
            calc_body=_STMARIA_CALC_BODY,
            calc_js=_STMARIA_CALC_JS,
        )
        components.html(html, height=1000, scrolling=True)
