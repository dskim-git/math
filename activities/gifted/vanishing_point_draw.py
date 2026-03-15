import base64
import os

import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 소실점 찾기 — 직선 그리기 활동",
    "description": "사진과 그림 위에 직선을 그려 1점·2점·3점 투시의 소실점을 직접 찾아봅니다.",
    "order": 31,
    "hidden": True,
}

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

.cat-tabs { display: flex; gap: 6px; margin-bottom: 8px; flex-wrap: wrap; }
.cat-btn {
  padding: 8px 18px; border-radius: 999px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer;
  font-size: 0.85rem; font-weight: 700; transition: all .15s;
}
.cat-btn.active { background: #0f766e; color: #ecfeff; border-color: #14b8a6; }
.cat-btn:hover:not(.active) { border-color: #475569; color: #cbd5e1; }

.img-tabs { display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 8px; }
.img-tab {
  padding: 6px 13px; border-radius: 8px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer;
  font-size: 0.78rem; font-weight: 600; transition: all .15s;
}
.img-tab.active { background: #1e3a5f; color: #bfdbfe; border-color: #3b82f6; }
.img-tab:hover:not(.active) { border-color: #475569; color: #cbd5e1; }

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

.canvas-wrap {
  background: #111827; border: 1px solid #334155; border-radius: 10px;
  overflow: hidden; line-height: 0; position: relative;
}
#cvs { display: block; margin: 0 auto; cursor: crosshair; touch-action: none; }
.canvas-loading {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
  font-size: 0.85rem; color: #475569;
}

.hint {
  margin-top: 8px; padding: 10px 14px; background: #0f172a;
  border-left: 4px solid #3b82f6; border-radius: 8px;
}
.hint-title { font-size: 0.85rem; font-weight: 800; color: #93c5fd; margin-bottom: 3px; }
.hint-text { font-size: 0.78rem; color: #94a3b8; line-height: 1.6; }
.ans-row { display: flex; align-items: center; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
.ans-btn {
  padding: 6px 14px; border-radius: 8px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer;
  font-size: 0.78rem; font-weight: 700; transition: all .15s;
}
.ans-btn:hover { border-color: #14b8a6; color: #ccfbf1; }
.stroke-count { font-size: 0.75rem; color: #475569; }
.ans-box {
  display: none; margin-top: 6px; padding: 10px 14px;
  background: #022c22; border: 1px solid #14b8a6;
  border-radius: 8px; font-size: 0.8rem; color: #6ee7b7; line-height: 1.8;
}

@media (max-width: 600px) {
  .vsep { display: none; }
  .toolbar { gap: 6px; padding: 6px 8px; }
}
</style>
</head>
<body>
<div id="app">

<div class="cat-tabs">
  <button class="cat-btn active" data-cat="concept">📐 개념 학습 (1·2·3점 투시)</button>
  <button class="cat-btn" data-cat="practice">🔍 소실점 찾기 실습</button>
</div>

<div id="tabs-concept" class="img-tabs">
  <button class="img-tab active" data-set="concept" data-i="0">1점 투시</button>
  <button class="img-tab" data-set="concept" data-i="1">2점 투시</button>
  <button class="img-tab" data-set="concept" data-i="2">3점 투시</button>
</div>
<div id="tabs-practice" class="img-tabs" style="display:none">
  <button class="img-tab active" data-set="practice" data-i="0">아테네 학당</button>
  <button class="img-tab" data-set="practice" data-i="1">최후의 만찬</button>
  <button class="img-tab" data-set="practice" data-i="2">전주 정동성당</button>
  <button class="img-tab" data-set="practice" data-i="3">파르테논 신전</button>
</div>

<div class="toolbar">
  <div class="tool-group">
    <button class="tl-btn active" id="btnLine">📏 직선</button>
    <button class="tl-btn" id="btnFree">✏️ 자유선</button>
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

<div class="canvas-wrap" id="cvsWrap">
  <canvas id="cvs"></canvas>
  <div class="canvas-loading" id="loadMsg">이미지 불러오는 중...</div>
</div>

<div class="hint">
  <div class="hint-title" id="hintTitle">—</div>
  <div class="hint-text" id="hintText">—</div>
</div>
<div class="ans-row">
  <button class="ans-btn" id="ansBtn">💡 정답 확인하기</button>
  <span class="stroke-count" id="strokeCount"></span>
</div>
<div class="ans-box" id="ansBox"></div>

</div>

<script>
(function() {
'use strict';

const IMGDATA = {
  p1:         "PLACEHOLDER_P1",
  p2:         "PLACEHOLDER_P2",
  p3:         "PLACEHOLDER_P3",
  athens:     "PLACEHOLDER_ATHENS",
  lastsupper: "PLACEHOLDER_LASTSUPPER",
  jungdong:   "PLACEHOLDER_JUNGDONG",
  parthenon:  "PLACEHOLDER_PARTHENON",
};

const SETS = {
  concept: [
    {
      key: 'p1', label: '1점 투시 (평행선 원근법)',
      hint: '소실점이 1개입니다. 깊이 방향의 평행선(도로, 레일, 복도 등)을 연장하면 화면 안의 한 점으로 모입니다. 빨간 선으로 수렴 방향을 그어보세요.',
      answer: '✅ 소실점 1개. 수평선(지평선) 위에 위치하며 모든 깊이 방향 선이 그 한 점으로 수렴합니다. 집중감이 강해 도로·복도·기찻길 장면에서 자주 쓰이며, 1점 투시에서는 시심(V)과 소실점이 일치합니다.'
    },
    {
      key: 'p2', label: '2점 투시 (사선 원근법)',
      hint: '소실점이 2개입니다. 건물 왼쪽 면의 선들과 오른쪽 면의 선들이 각각 다른 방향으로 수렴합니다. 두 가지 색으로 구분해 그어보세요.',
      answer: '✅ 소실점 2개. 수평선의 양쪽에 각 하나씩 위치합니다. 건물 모서리를 측면에서 볼 때 왼쪽 면 → 왼쪽 소실점, 오른쪽 면 → 오른쪽 소실점으로 각각 수렴합니다. 웅장한 건물 표현에 많이 쓰입니다.'
    },
    {
      key: 'p3', label: '3점 투시 (공간 원근법)',
      hint: '소실점이 3개입니다. 좌·우·위(또는 아래) 세 방향으로 선이 모입니다. 세 가지 색으로 각 방향의 선을 구분해 그어보세요.',
      answer: '✅ 소실점 3개. 좌우 소실점 2개 + 수직 방향 소실점 1개(위 또는 아래). 높은 건물을 올려다보거나 내려다볼 때 수직선도 수렴하면서 3번째 소실점이 생깁니다. 초고층 빌딩 표현에 사용됩니다.'
    },
  ],
  practice: [
    {
      key: 'athens', label: '아테네 학당 (라파엘로, 1509–1511)',
      hint: '아치형 천장, 바닥 타일, 벽면의 선들을 따라 그어보세요. 몇 점 투시일까요?',
      answer: '✅ 1점 투시. 소실점은 1개로 플라톤·아리스토텔레스가 서 있는 중앙에 위치합니다. 라파엘로가 시선이 두 철학자에게 자연스럽게 집중되도록 의도적으로 설계한 구성입니다.'
    },
    {
      key: 'lastsupper', label: '최후의 만찬 (레오나르도 다빈치, 1495–1498)',
      hint: '천장의 격자 구조, 벽의 수평선, 창문 틀 선들을 연장해 보세요. 어느 점으로 모이나요?',
      answer: '✅ 1점 투시. 소실점은 1개로 예수 그리스도의 얼굴 뒤에 정확히 위치합니다. 다빈치가 수학적 원근법을 활용해 모든 시선이 예수에게 집중되도록 구성했습니다.'
    },
    {
      key: 'jungdong', label: '전주 정동성당',
      hint: '성당 기둥·지붕의 수평 선(빨강)과 탑의 수직 선(초록)을 각각 다른 색으로 그어보세요.',
      answer: '✅ 2~3점 투시. 성당 벽면 수평선 → 좌·우 소실점(2개), 탑의 수직 선들 → 위쪽 소실점(1개) 추가. 카메라 앵글에 따라 2점 또는 3점 투시로 해석할 수 있습니다.'
    },
    {
      key: 'parthenon', label: '파르테논 신전 (그리스 아테네)',
      hint: '지붕 처마의 사선, 기둥 상단·하단의 수평선들을 연장해 보세요. 소실점은 몇 개인가요?',
      answer: '✅ 2점 투시. 신전 왼쪽 측면 선들 → 왼쪽 소실점, 정면(기둥열) 선들 → 오른쪽 소실점. 소실점 2개가 화면 바깥 멀리 위치해 매우 완만하게 수렴합니다.'
    },
  ],
};

const S = {
  cat: 'concept', set: 'concept', idx: 0,
  tool: 'line', color: '#ef4444', thick: 3,
  drawing: false, sx: 0, sy: 0, freeStroke: null,
  strokes: {},
  imgCache: {}, bgImg: null,
};

// Init per-image stroke storage
['concept', 'practice'].forEach(set =>
  SETS[set].forEach(it => { S.strokes[it.key] = []; })
);

const cvs = document.getElementById('cvs');
const ctx = cvs.getContext('2d');

function pxCoords(e) {
  const r = cvs.getBoundingClientRect();
  const scaleX = cvs.width / r.width;
  const scaleY = cvs.height / r.height;
  const cx = e.touches ? e.touches[0].clientX : e.clientX;
  const cy = e.touches ? e.touches[0].clientY : e.clientY;
  return { x: (cx - r.left) * scaleX, y: (cy - r.top) * scaleY };
}

function loadImg(key) {
  return new Promise(res => {
    if (S.imgCache[key]) { res(S.imgCache[key]); return; }
    const b64 = IMGDATA[key];
    if (!b64) { res(null); return; }
    const img = new Image();
    img.onload = () => { S.imgCache[key] = img; res(img); };
    img.onerror = () => res(null);
    const mime = (key === 'p1' || key === 'p2' || key === 'p3') ? 'image/jpeg' : 'image/png';
    img.src = 'data:' + mime + ';base64,' + b64;
  });
}

function curItem() { return SETS[S.set][S.idx]; }

async function showImage(set, idx) {
  S.set = set; S.idx = idx;
  const it = curItem();
  document.getElementById('loadMsg').style.display = 'block';
  const img = await loadImg(it.key);
  document.getElementById('loadMsg').style.display = 'none';
  S.bgImg = img;
  if (img) {
    const isPortrait = img.naturalHeight > img.naturalWidth;
    const dispW = isPortrait ? 460 : 920;
    const scale = dispW / img.naturalWidth;
    cvs.width  = dispW;
    cvs.height = Math.round(img.naturalHeight * scale);
    cvs.style.width = dispW + 'px';
  } else {
    cvs.width = 920; cvs.height = 518;
    cvs.style.width = '920px';
  }
  redraw();
  updateInfo();
}

function drawStroke(c, st) {
  if (!st.pts || st.pts.length < 2) return;
  c.save();
  c.strokeStyle = st.color;
  c.lineWidth = st.thick;
  c.lineCap = 'round';
  c.lineJoin = 'round';
  c.beginPath();
  if (st.type === 'line') {
    c.moveTo(st.pts[0].x, st.pts[0].y);
    c.lineTo(st.pts[st.pts.length - 1].x, st.pts[st.pts.length - 1].y);
  } else {
    c.moveTo(st.pts[0].x, st.pts[0].y);
    for (let i = 1; i < st.pts.length; i++) c.lineTo(st.pts[i].x, st.pts[i].y);
  }
  c.stroke();
  c.restore();
}

function redraw(previewStroke) {
  ctx.clearRect(0, 0, cvs.width, cvs.height);
  if (S.bgImg) {
    ctx.drawImage(S.bgImg, 0, 0, cvs.width, cvs.height);
  } else {
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, cvs.width, cvs.height);
    ctx.fillStyle = '#475569';
    ctx.font = 'bold 20px Segoe UI';
    ctx.textAlign = 'center';
    ctx.fillText('이미지를 불러올 수 없습니다', cvs.width / 2, cvs.height / 2);
    ctx.textAlign = 'left';
  }
  const strokes = S.strokes[curItem().key];
  strokes.forEach(st => drawStroke(ctx, st));
  if (previewStroke) {
    ctx.globalAlpha = 0.75;
    drawStroke(ctx, previewStroke);
    ctx.globalAlpha = 1;
  }
  updateStrokeCount();
}

function updateInfo() {
  const it = curItem();
  document.getElementById('hintTitle').textContent = it.label;
  document.getElementById('hintText').textContent = it.hint;
  const ab = document.getElementById('ansBox');
  ab.style.display = 'none';
  ab.textContent = it.answer;
  updateStrokeCount();
}

function updateStrokeCount() {
  const n = S.strokes[curItem().key].length;
  document.getElementById('strokeCount').textContent = n > 0 ? `선 ${n}개 그림` : '';
}

// ── Pointer / Touch events ────────────────────────────────────────────────────
cvs.addEventListener('pointerdown', e => {
  e.preventDefault();
  const { x, y } = pxCoords(e);
  S.drawing = true;
  S.sx = x; S.sy = y;

  if (S.tool === 'eraser') {
    const arr = S.strokes[curItem().key];
    if (arr.length) { arr.pop(); redraw(); }
    S.drawing = false;
    return;
  }
  if (S.tool === 'free') {
    S.freeStroke = { type: 'free', color: S.color, thick: S.thick, pts: [{ x, y }] };
    S.strokes[curItem().key].push(S.freeStroke);
  }
  cvs.setPointerCapture(e.pointerId);
});

cvs.addEventListener('pointermove', e => {
  if (!S.drawing) return;
  e.preventDefault();
  const { x, y } = pxCoords(e);
  if (S.tool === 'line') {
    redraw({ type: 'line', color: S.color, thick: S.thick, pts: [{ x: S.sx, y: S.sy }, { x, y }] });
  } else if (S.tool === 'free' && S.freeStroke) {
    S.freeStroke.pts.push({ x, y });
    redraw();
  }
});

cvs.addEventListener('pointerup', e => {
  if (!S.drawing) return;
  S.drawing = false;
  const { x, y } = pxCoords(e);
  if (S.tool === 'line') {
    const dx = x - S.sx, dy = y - S.sy;
    if (dx * dx + dy * dy > 25) {
      S.strokes[curItem().key].push({
        type: 'line', color: S.color, thick: S.thick,
        pts: [{ x: S.sx, y: S.sy }, { x, y }]
      });
    }
    redraw();
  }
  S.freeStroke = null;
});

cvs.addEventListener('pointerleave', e => {
  if (S.drawing && S.tool === 'line') { S.drawing = false; redraw(); }
});

// ── Tool buttons ──────────────────────────────────────────────────────────────
function setTool(t) {
  S.tool = t;
  document.getElementById('btnLine').classList.toggle('active', t === 'line');
  document.getElementById('btnFree').classList.toggle('active', t === 'free');
  document.getElementById('btnEraser').classList.toggle('active', t === 'eraser');
  cvs.style.cursor = t === 'eraser' ? 'cell' : 'crosshair';
}
document.getElementById('btnLine').addEventListener('click', () => setTool('line'));
document.getElementById('btnFree').addEventListener('click', () => setTool('free'));
document.getElementById('btnEraser').addEventListener('click', () => setTool('eraser'));

// ── Color swatches ────────────────────────────────────────────────────────────
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

// ── Thickness ─────────────────────────────────────────────────────────────────
document.getElementById('thickSlider').addEventListener('input', e => {
  S.thick = +e.target.value;
  document.getElementById('thickVal').textContent = S.thick;
});

// ── Undo / Clear ──────────────────────────────────────────────────────────────
document.getElementById('btnUndo').addEventListener('click', () => {
  S.strokes[curItem().key].pop();
  redraw();
});
document.getElementById('btnClear').addEventListener('click', () => {
  S.strokes[curItem().key] = [];
  redraw();
});

// ── Category tabs ─────────────────────────────────────────────────────────────
document.querySelectorAll('.cat-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    S.cat = btn.dataset.cat;
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tabs-concept').style.display = S.cat === 'concept' ? 'flex' : 'none';
    document.getElementById('tabs-practice').style.display = S.cat === 'practice' ? 'flex' : 'none';
    document.querySelectorAll(`#tabs-${S.cat} .img-tab`).forEach((b, i) =>
      b.classList.toggle('active', i === 0)
    );
    showImage(S.cat, 0);
  });
});

// ── Image tabs ────────────────────────────────────────────────────────────────
document.querySelectorAll('.img-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const set = btn.dataset.set;
    const idx = +btn.dataset.i;
    document.querySelectorAll(`#tabs-${set} .img-tab`).forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    showImage(set, idx);
  });
});

// ── Answer toggle ─────────────────────────────────────────────────────────────
document.getElementById('ansBtn').addEventListener('click', () => {
  const b = document.getElementById('ansBox');
  b.style.display = b.style.display === 'none' ? 'block' : 'none';
});

// ── Init ──────────────────────────────────────────────────────────────────────
showImage('concept', 0);
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


def _build_html(imgs: dict) -> str:
    h = _TEMPLATE
    for key, val in imgs.items():
        h = h.replace(f"PLACEHOLDER_{key.upper()}", val)
    return h


def render():
    st.header("🎨 소실점 찾기 — 직선 그리기 활동")
    st.caption("사진과 그림 위에 직선을 그어 1점·2점·3점 투시의 소실점을 직접 찾아봅니다.")

    with st.expander("💡 활동 안내", expanded=False):
        st.markdown(
            """
1. **개념 학습** 탭에서 1점·2점·3점 투시 예시 그림에 직선을 그어 소실점을 확인합니다.
2. **소실점 찾기 실습** 탭에서 유명 작품·건물 사진에서 소실점을 직접 찾아봅니다.
3. `📏 직선` 도구: 마우스 클릭→드래그로 직선을 긋습니다 (소실점 탐색에 가장 유용).
4. `✏️ 자유선` 도구: 드래그로 자유롭게 그립니다.
5. `🧹 지우개` 도구: 클릭하면 가장 마지막 선을 삭제합니다.
6. 색상·두께를 바꿔가며 방향이 다른 선을 색으로 구분해 그어보세요.
            """
        )

    keys_files = [
        ("p1",         "1점투시.jpg"),
        ("p2",         "2점투시.jpg"),
        ("p3",         "3점투시.jpg"),
        ("athens",     "athens.png"),
        ("lastsupper", "lastsupper.png"),
        ("jungdong",   "jungdongsungdang.png"),
        ("parthenon",  "parthenon.png"),
    ]
    imgs: dict = {}
    for key, fname in keys_files:
        try:
            imgs[key] = _b64(fname)
        except Exception:
            imgs[key] = ""

    components.html(_build_html(imgs), height=1500, scrolling=True)
