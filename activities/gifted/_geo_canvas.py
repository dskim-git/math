# _geo_canvas.py
# ─────────────────────────────────────────────────────────────────────────────
#  Geometry Construction Canvas — reusable HTML/CSS/JS components
#
#  Exports:
#    PROBLEMS_CONFIG   dict[int, dict]   — problem definitions
#    GEO_CSS           str               — CSS (no <style> tags)
#    GEO_HTML          str               — HTML for the canvas section
#    GEO_JS_TEMPLATE   str               — JS with __CANVAS_PROBLEMS__ placeholder
#
#  Usage (in a parent activity file):
#    from activities.gifted._geo_canvas import (
#        PROBLEMS_CONFIG, GEO_CSS, GEO_HTML, GEO_JS_TEMPLATE
#    )
#    import json
#    js = GEO_JS_TEMPLATE.replace(
#        '__CANVAS_PROBLEMS__', json.dumps(PROBLEMS_CONFIG)
#    )
#    full_html = f"<style>{GEO_CSS}</style>{GEO_HTML}<script>{js}</script>"
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
#  PROBLEM DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

PROBLEMS_CONFIG = {
    1: {
        "title": "세 꼭짓점을 통한 평행사변형",
        "desc": "4개의 꼭짓점 중 3개의 꼭짓점이 주어진 평행사변형을 작도하세요.",
        "setup": [
            {"type": "point", "rx": 0.63, "ry": 0.38, "fixed": True, "label": "A"},
            {"type": "point", "rx": 0.40, "ry": 0.82, "fixed": True, "label": "B"},
            {"type": "point", "rx": 0.82, "ry": 0.82, "fixed": True, "label": "C"},
        ],
    },
    3: {
        "title": "해시",
        "desc": "두 쌍의 평행선에 의해 선분이 동일한 길이로 절단되도록 주어진 점을 지나는 직선을 작도하세요.",
        "setup": [
            # Pair 1: parallel lines (upper-left → lower-right)
            {"type": "given_segment", "rx1": 0.20, "ry1": 0.10, "rx2": 0.80, "ry2": 0.52},
            {"type": "given_segment", "rx1": 0.35, "ry1": 0.28, "rx2": 0.95, "ry2": 0.70},
            # Pair 2: parallel lines (upper-right → lower-left)
            {"type": "given_segment", "rx1": 0.20, "ry1": 0.52, "rx2": 0.80, "ry2": 0.10},
            {"type": "given_segment", "rx1": 0.35, "ry1": 0.70, "rx2": 0.95, "ry2": 0.28},
            # Given point P
            {"type": "point", "rx": 0.60, "ry": 0.88, "fixed": True, "label": "P"},
        ],
    },
    2: {
        "title": "정사각형에 내접하는 원",
        "desc": "정사각형에 내접하는 원을 작도하세요.",
        # 캔버스 700×500 기준: 가로 0.429×700=300px, 세로 0.6×500=300px → 정사각형
        "setup": [
            {"type": "point", "rx": 0.286, "ry": 0.20, "fixed": True, "label": "A"},
            {"type": "point", "rx": 0.714, "ry": 0.20, "fixed": True, "label": "B"},
            {"type": "point", "rx": 0.714, "ry": 0.80, "fixed": True, "label": "C"},
            {"type": "point", "rx": 0.286, "ry": 0.80, "fixed": True, "label": "D"},
            {"type": "segment", "p1": "A", "p2": "B"},
            {"type": "segment", "p1": "B", "p2": "C"},
            {"type": "segment", "p1": "C", "p2": "D"},
            {"type": "segment", "p1": "D", "p2": "A"},
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
#  CSS  (dark theme matching the app — no <style> tags)
# ─────────────────────────────────────────────────────────────────────────────

GEO_CSS = """
/* ── Geometry canvas section ── */
#geo-section {
  margin-top: 16px;
}

/* Problem header */
.geo-prob-header {
  background: #0f1f38;
  border: 1px solid #1e3a5f;
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 12px;
}
#geo-prob-num {
  font-size: 0.78rem;
  font-weight: 800;
  color: #fbbf24;
  margin-bottom: 2px;
}
#geo-prob-title {
  font-size: 1.05rem;
  font-weight: 900;
  color: #f1f5f9;
  margin-bottom: 4px;
}
#geo-prob-desc {
  font-size: 0.83rem;
  color: #94a3b8;
  line-height: 1.5;
}

/* Canvas wrapper */
.geo-wrap {
  background: #0f1f38;
  border: 1px solid #1e3a5f;
  border-radius: 12px;
  overflow: hidden;
}

/* ── Toolbar ── */
.geo-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 10px 12px;
  border-bottom: 1px solid #1e3a5f;
  background: #0a1628;
}
.geo-tool-btn {
  padding: 5px 11px;
  border-radius: 7px;
  border: 1.5px solid #334155;
  background: #1e293b;
  color: #94a3b8;
  cursor: pointer;
  font-size: 0.76rem;
  font-weight: 700;
  transition: all 0.15s;
  white-space: nowrap;
  user-select: none;
}
.geo-tool-btn:hover {
  border-color: #64748b;
  color: #f8fafc;
}
.geo-tool-btn.active {
  background: #0c4a6e;
  border-color: #38bdf8;
  color: #38bdf8;
  box-shadow: 0 0 8px rgba(56, 189, 248, 0.25);
}
.geo-tool-btn.danger {
  border-color: #7f1d1d;
  color: #fca5a5;
}
.geo-tool-btn.danger:hover {
  background: #7f1d1d;
  color: #fef2f2;
}
.geo-tool-btn.action {
  border-color: #44403c;
  color: #fbbf24;
}
.geo-tool-btn.action:hover {
  background: #292524;
  color: #fde68a;
}
.geo-tool-sep {
  width: 1px;
  background: #1e3a5f;
  margin: 2px 2px;
  align-self: stretch;
}

/* ── Counter bar ── */
.geo-counter-bar {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 7px 14px;
  border-bottom: 1px solid #1e3a5f;
  background: #0a1628;
  font-size: 0.78rem;
  flex-wrap: wrap;
}
.geo-counter-item {
  display: flex;
  align-items: center;
  gap: 5px;
}
.geo-counter-label {
  color: #475569;
  font-weight: 600;
}
.geo-counter-val {
  font-weight: 800;
  font-size: 0.9rem;
}
.geo-counter-val.L {
  color: #38bdf8;
}
.geo-counter-val.E {
  color: #c4b5fd;
}
.geo-counter-sep {
  color: #334155;
}
.geo-status-msg {
  margin-left: auto;
  font-size: 0.74rem;
  color: #64748b;
  font-style: italic;
}

/* ── Canvas ── */
#geo-canvas {
  display: block;
  width: 100%;
  background: #ffffff;
  cursor: crosshair;
  touch-action: none;
}
"""

# ─────────────────────────────────────────────────────────────────────────────
#  HTML  (the canvas section block — no inline styles except display:none)
# ─────────────────────────────────────────────────────────────────────────────

GEO_HTML = """
<div id="geo-section" style="display:none;">

  <!-- Problem header -->
  <div class="geo-prob-header">
    <div id="geo-prob-num">문제 #1</div>
    <div id="geo-prob-title"></div>
    <div id="geo-prob-desc"></div>
  </div>

  <!-- Canvas tool wrapper -->
  <div class="geo-wrap">

    <!-- Toolbar -->
    <div class="geo-toolbar">
      <!-- Construction tools -->
      <button class="geo-tool-btn" id="btn-move"       onclick="setTool('move')">이동</button>
      <button class="geo-tool-btn" id="btn-point"      onclick="setTool('point')">점</button>
      <button class="geo-tool-btn" id="btn-line"       onclick="setTool('line')">선 (+1L+1E)</button>
      <button class="geo-tool-btn" id="btn-circle"     onclick="setTool('circle')">원 (+1L+1E)</button>
      <div class="geo-tool-sep"></div>
      <button class="geo-tool-btn" id="btn-perp-bisector" onclick="setTool('perp-bisector')">수직이등분선 (+1L+3E)</button>
      <button class="geo-tool-btn" id="btn-perp"          onclick="setTool('perp')">수선 (+1L+3E)</button>
      <button class="geo-tool-btn" id="btn-angle-bisector" onclick="setTool('angle-bisector')">각의이등분선 (+1L+4E)</button>
      <button class="geo-tool-btn" id="btn-parallel"      onclick="setTool('parallel')">평행선 (+1L+4E)</button>
      <button class="geo-tool-btn" id="btn-intersect"     onclick="setTool('intersect')">교차</button>
      <div class="geo-tool-sep"></div>
      <!-- Action buttons -->
      <button class="geo-tool-btn danger" id="btn-delete"  onclick="setTool('delete')">삭제</button>
      <button class="geo-tool-btn action" onclick="undoGeo()">실행취소 (Ctrl+Z)</button>
      <button class="geo-tool-btn action" onclick="resetCanvas()">초기화</button>
      <div class="geo-tool-sep"></div>
      <button class="geo-tool-btn action" onclick="zoomIn()">＋ 확대</button>
      <button class="geo-tool-btn action" onclick="zoomOut()">－ 축소</button>
      <button class="geo-tool-btn action" onclick="zoomReset()">⊙ 전체</button>
    </div>

    <!-- Counter bar -->
    <div class="geo-counter-bar">
      <div class="geo-counter-item">
        <span class="geo-counter-label">사용:</span>
        <span class="geo-counter-val L" id="geo-cur-L">0L</span>
        <span class="geo-counter-sep">·</span>
        <span class="geo-counter-val E" id="geo-cur-E">0E</span>
      </div>
      <div id="geo-status-msg" class="geo-status-msg">도구를 선택하세요.</div>
    </div>

    <!-- Canvas -->
    <canvas id="geo-canvas" height="500"></canvas>

  </div>
</div>
"""

# ─────────────────────────────────────────────────────────────────────────────
#  JAVASCRIPT TEMPLATE
#  Replace __CANVAS_PROBLEMS__ with json.dumps(PROBLEMS_CONFIG) before use.
# ─────────────────────────────────────────────────────────────────────────────

GEO_JS_TEMPLATE = r"""
'use strict';

// ═══════════════════════════════════════════════════════════════
//  INJECTED PROBLEM DATA  (Python replaces the placeholder)
// ═══════════════════════════════════════════════════════════════
const CP = __CANVAS_PROBLEMS__;

// ═══════════════════════════════════════════════════════════════
//  STATE
// ═══════════════════════════════════════════════════════════════
/**
 * GS — Geometry State
 *  pts[]     : {id, x, y, fixed, label, helper}
 *  lines[]   : {id, p1, p2, lc, ec}   — p1/p2 are point IDs
 *  circles[] : {id, cid, rid, lc, ec} — cid=center ID, rid=radius-point ID
 *  segs[]     : {id, p1, p2}                     — display-only segments via point IDs
 *  gsegs[]    : {x1, y1, x2, y2}                 — display-only segments via absolute coords (no points shown)
 *  lc, ec    : running L / E totals
 *  history[] : JSON snapshots for undo
 *  nid       : next unique ID
 */
let GS = {
  pts: [], lines: [], circles: [], segs: [], gsegs: [],
  lc: 0, ec: 0, history: [], nid: 1,
};

let GW = 700, GH = 500;   // canvas logical dimensions (updated on resize)
let gTool  = 'move';       // active tool name
let gTS    = { step: 0, picks: [] };  // per-tool step state
let gHover = null;   // {type, id} hovered object
let gSnap  = null;   // {x, y, ptId?} snap target
let gDrag  = null;   // {ptId, ox, oy} drag state (move tool)
let gCurProb = null; // current problem number
let gZoom = { scale: 1, tx: 0, ty: 0 };  // pan/zoom state
let gPan  = null;  // {startSx, startSy, startTx, startTy} during pan drag

// ═══════════════════════════════════════════════════════════════
//  CANVAS SETUP
// ═══════════════════════════════════════════════════════════════
const _canvas = document.getElementById('geo-canvas');
const _ctx    = _canvas.getContext('2d');

/** Resize canvas to fill its CSS width while keeping a fixed aspect ratio. */
function resizeGeoCanvas() {
  const wrap = _canvas.parentElement;
  const w = wrap.clientWidth || 700;
  const h = Math.round(w * (500 / 700));
  _canvas.width  = w;
  _canvas.height = h;
  GW = w;
  GH = h;
}

/** Convert canvas-pixel (screen) coordinates to world coordinates. */
function screenToWorld(sx, sy) {
  return { x: (sx - gZoom.tx) / gZoom.scale, y: (sy - gZoom.ty) / gZoom.scale };
}
/** Convert world coordinates to canvas-pixel (screen) coordinates. */
function worldToScreen(wx, wy) {
  return { x: wx * gZoom.scale + gZoom.tx, y: wy * gZoom.scale + gZoom.ty };
}

window.addEventListener('resize', () => {
  if (gCurProb !== null) {
    resizeGeoCanvas();
    // Re-scale existing point coordinates from old dimensions
    // (simple approach: reinit; for production, scale pts)
    drawAll();
  }
});

// ═══════════════════════════════════════════════════════════════
//  INIT / RESET
// ═══════════════════════════════════════════════════════════════
/**
 * initCanvas(num) — show the canvas section and load problem num.
 * Called externally (e.g. when user picks a problem from a bingo cell).
 */
function initCanvas(num) {
  const prob = CP[num];

  // Reset geometry state
  GS = { pts: [], lines: [], circles: [], segs: [], gsegs: [], lc: 0, ec: 0, history: [], nid: 1 };
  gZoom = { scale: 1, tx: 0, ty: 0 };
  gTS = { step: 0, picks: [] };
  gCurProb = num;

  // Show the section
  document.getElementById('geo-section').style.display = 'block';

  // Update problem header
  document.getElementById('geo-prob-num').textContent   = '문제 #' + num;
  const pLE = (typeof PROBLEMS !== 'undefined' && PROBLEMS[num]) ? PROBLEMS[num] : null;
  const leHtml = pLE
    ? ' <span style="font-size:0.78rem;font-weight:800;color:#38bdf8">' + pLE.L + 'L</span>'
      + ' <span style="color:#334155;font-weight:400">·</span>'
      + ' <span style="font-size:0.78rem;font-weight:800;color:#c4b5fd">' + pLE.E + 'E</span>'
    : '';
  document.getElementById('geo-prob-title').innerHTML = (prob ? (prob.title || '') : '') + leHtml;
  document.getElementById('geo-prob-desc').textContent  = prob ? (prob.desc  || '') : '';

  // Resize canvas to container
  resizeGeoCanvas();

  // Build geometry from setup config
  if (prob && prob.setup) {
    prob.setup.forEach(function(item) {
      if (item.type === 'point') {
        const id = GS.nid++;
        GS.pts.push({
          id:     id,
          x:      item.rx * GW,
          y:      item.ry * GH,
          fixed:  !!item.fixed,
          label:  item.label || '',
          helper: false,
        });
      }
      if (item.type === 'segment') {
        const p1 = GS.pts.find(function(p) { return p.label === item.p1; });
        const p2 = GS.pts.find(function(p) { return p.label === item.p2; });
        if (p1 && p2) {
          GS.segs.push({ id: GS.nid++, p1: p1.id, p2: p2.id });
        }
      }
      if (item.type === 'given_segment') {
        GS.gsegs.push({
          x1: item.rx1 * GW, y1: item.ry1 * GH,
          x2: item.rx2 * GW, y2: item.ry2 * GH,
        });
      }
    });
  }

  setTool('move');
  updateGeoCount();
  drawAll();
}

/** resetCanvas() — re-initialize the current problem (keeps problem number). */
function resetCanvas() {
  if (gCurProb !== null) {
    initCanvas(gCurProb);
  }
}

// ═══════════════════════════════════════════════════════════════
//  TOOL MANAGEMENT
// ═══════════════════════════════════════════════════════════════
const TOOL_STATUS = {
  'move':           '점을 드래그하여 이동하세요.',
  'point':          '캔버스를 클릭하여 점을 찍으세요.',
  'line':           '두 점을 클릭하여 직선을 그으세요.',
  'circle':         '중심점을 클릭한 후 반지름 점을 클릭하세요.',
  'perp-bisector':  '두 점을 클릭하여 수직이등분선을 그으세요.',
  'perp':           '직선 또는 점을 먼저 클릭하세요.',
  'angle-bisector': '첫 번째 점(A)을 클릭하세요.',
  'parallel':       '직선을 클릭한 후 점을 클릭하세요.',
  'intersect':      '두 개의 선/원을 클릭하여 교점을 구하세요.',
  'delete':         '삭제할 선 또는 원을 클릭하세요.',
};

function setTool(name) {
  gTool = name;
  gTS   = { step: 0, picks: [] };
  gHover = null;
  gSnap  = null;

  // Update button states
  const TOOL_IDS = [
    'move','point','line','circle',
    'perp-bisector','perp','angle-bisector','parallel','intersect','delete',
  ];
  TOOL_IDS.forEach(function(t) {
    const btn = document.getElementById('btn-' + t);
    if (btn) btn.classList.toggle('active', t === name);
  });

  // Update status message
  const msg = document.getElementById('geo-status-msg');
  if (msg) msg.textContent = TOOL_STATUS[name] || '';

  drawAll();
}

// ═══════════════════════════════════════════════════════════════
//  UNDO / HISTORY
// ═══════════════════════════════════════════════════════════════
function saveHistory() {
  // Store a deep clone of pts/lines/circles/segs/lc/ec (not history itself)
  GS.history.push(JSON.stringify({
    pts:     GS.pts,
    lines:   GS.lines,
    circles: GS.circles,
    segs:    GS.segs,
    lc:      GS.lc,
    ec:      GS.ec,
    nid:     GS.nid,
  }));
  // Keep at most 50 snapshots to avoid unbounded memory
  if (GS.history.length > 50) GS.history.shift();
}

function undoGeo() {
  if (GS.history.length === 0) return;
  const snap = JSON.parse(GS.history.pop());
  GS.pts     = snap.pts;
  GS.lines   = snap.lines;
  GS.circles = snap.circles;
  GS.segs    = snap.segs;
  GS.lc      = snap.lc;
  GS.ec      = snap.ec;
  GS.nid     = snap.nid;
  gTS = { step: 0, picks: [] };
  updateGeoCount();
  drawAll();
}

// Ctrl+Z keyboard shortcut
document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
    e.preventDefault();
    undoGeo();
  }
});

// ═══════════════════════════════════════════════════════════════
//  COUNTER UI
// ═══════════════════════════════════════════════════════════════
function updateGeoCount() {
  const lEl = document.getElementById('geo-cur-L');
  const eEl = document.getElementById('geo-cur-E');
  if (lEl) lEl.textContent = GS.lc + 'L';
  if (eEl) eEl.textContent = GS.ec + 'E';
}

// ═══════════════════════════════════════════════════════════════
//  GEOMETRY HELPERS
// ═══════════════════════════════════════════════════════════════

/** Get a point object by id. */
function getPt(id) {
  return GS.pts.find(function(p) { return p.id === id; }) || null;
}

/** Get a line object by id. */
function getLine(id) {
  return GS.lines.find(function(l) { return l.id === id; }) || null;
}

/** Get a circle object by id. */
function getCircle(id) {
  return GS.circles.find(function(c) { return c.id === id; }) || null;
}

/**
 * llIntersect(l1, l2) — infinite line × infinite line intersection.
 * l1, l2 : line objects with p1/p2 point IDs.
 * Returns {x, y} or null if parallel.
 */
function llIntersect(l1, l2) {
  const a1 = getPt(l1.p1), b1 = getPt(l1.p2);
  const a2 = getPt(l2.p1), b2 = getPt(l2.p2);
  if (!a1 || !b1 || !a2 || !b2) return null;

  const dx1 = b1.x - a1.x, dy1 = b1.y - a1.y;
  const dx2 = b2.x - a2.x, dy2 = b2.y - a2.y;
  const denom = dx1 * dy2 - dy1 * dx2;
  if (Math.abs(denom) < 1e-10) return null;  // parallel

  const t = ((a2.x - a1.x) * dy2 - (a2.y - a1.y) * dx2) / denom;
  return { x: a1.x + t * dx1, y: a1.y + t * dy1 };
}

/**
 * lcIntersect(l, c) — infinite line × circle intersection.
 * Returns array of 0, 1, or 2 {x,y} points.
 */
function lcIntersect(l, c) {
  const a = getPt(l.p1), b = getPt(l.p2);
  const cen = getPt(c.cid), rad_pt = getPt(c.rid);
  if (!a || !b || !cen || !rad_pt) return [];

  const r  = Math.hypot(rad_pt.x - cen.x, rad_pt.y - cen.y);
  const dx = b.x - a.x, dy = b.y - a.y;
  const fx = a.x - cen.x, fy = a.y - cen.y;
  const A  = dx * dx + dy * dy;
  const B  = 2 * (fx * dx + fy * dy);
  const C  = fx * fx + fy * fy - r * r;
  const disc = B * B - 4 * A * C;

  if (disc < 0 || A < 1e-12) return [];
  if (Math.abs(disc) < 1e-10) {
    const t = -B / (2 * A);
    return [{ x: a.x + t * dx, y: a.y + t * dy }];
  }
  const sq = Math.sqrt(disc);
  const t1 = (-B + sq) / (2 * A);
  const t2 = (-B - sq) / (2 * A);
  return [
    { x: a.x + t1 * dx, y: a.y + t1 * dy },
    { x: a.x + t2 * dx, y: a.y + t2 * dy },
  ];
}

/**
 * ccIntersect(c1, c2) — circle × circle intersection.
 * Returns array of 0, 1, or 2 {x,y} points.
 */
function ccIntersect(c1, c2) {
  const cen1 = getPt(c1.cid), r1pt = getPt(c1.rid);
  const cen2 = getPt(c2.cid), r2pt = getPt(c2.rid);
  if (!cen1 || !r1pt || !cen2 || !r2pt) return [];

  const r1 = Math.hypot(r1pt.x - cen1.x, r1pt.y - cen1.y);
  const r2 = Math.hypot(r2pt.x - cen2.x, r2pt.y - cen2.y);
  const dx = cen2.x - cen1.x, dy = cen2.y - cen1.y;
  const d  = Math.hypot(dx, dy);

  if (d < 1e-10 || d > r1 + r2 + 1e-10 || d < Math.abs(r1 - r2) - 1e-10) return [];

  const a   = (r1 * r1 - r2 * r2 + d * d) / (2 * d);
  const hSq = r1 * r1 - a * a;
  if (hSq < 0) return [];
  const h  = Math.sqrt(Math.max(0, hSq));
  const mx = cen1.x + a * dx / d;
  const my = cen1.y + a * dy / d;

  if (h < 1e-10) return [{ x: mx, y: my }];
  return [
    { x: mx + h * dy / d, y: my - h * dx / d },
    { x: mx - h * dy / d, y: my + h * dx / d },
  ];
}

/**
 * footOnLine(l, px, py) — foot of perpendicular from point (px,py) to line l.
 * Returns {x, y}.
 */
function footOnLine(l, px, py) {
  const a = getPt(l.p1), b = getPt(l.p2);
  if (!a || !b) return null;
  const dx = b.x - a.x, dy = b.y - a.y;
  const len2 = dx * dx + dy * dy;
  if (len2 < 1e-12) return { x: a.x, y: a.y };
  const t = ((px - a.x) * dx + (py - a.y) * dy) / len2;
  return { x: a.x + t * dx, y: a.y + t * dy };
}

/**
 * distToLine(l, px, py) — distance from point to infinite line.
 */
function distToLine(l, px, py) {
  const a = getPt(l.p1), b = getPt(l.p2);
  if (!a || !b) return Infinity;
  const dx = b.x - a.x, dy = b.y - a.y;
  const len = Math.hypot(dx, dy);
  if (len < 1e-10) return Math.hypot(px - a.x, py - a.y);
  return Math.abs((py - a.y) * dx - (px - a.x) * dy) / len;
}

/**
 * distToCircle(c, px, py) — distance from point to circle edge.
 */
function distToCircle(c, px, py) {
  const cen = getPt(c.cid), rpt = getPt(c.rid);
  if (!cen || !rpt) return Infinity;
  const r = Math.hypot(rpt.x - cen.x, rpt.y - cen.y);
  return Math.abs(Math.hypot(px - cen.x, py - cen.y) - r);
}

// ─────────────────────────────────────────────────────────────────
//  findSnap(mx, my) — snaps to existing points (r=12) or
//                     computed intersection points (r=10).
//  Returns {x, y, ptId?}  or  null.
// ─────────────────────────────────────────────────────────────────
function findSnap(mx, my) {
  const SNAP_PT = 12 / gZoom.scale;
  const SNAP_IX = 10 / gZoom.scale;

  // 1. Snap to existing points
  let best = null, bestD = Infinity;
  GS.pts.forEach(function(p) {
    const d = Math.hypot(p.x - mx, p.y - my);
    if (d < SNAP_PT && d < bestD) { bestD = d; best = { x: p.x, y: p.y, ptId: p.id }; }
  });
  if (best) return best;

  // 2. Snap to computed intersections (line×line, line×circle, circle×circle)
  const allObjs = []
    .concat(GS.lines.map(function(l) { return { type: 'line', obj: l }; }))
    .concat(GS.circles.map(function(c) { return { type: 'circle', obj: c }; }));

  for (let i = 0; i < allObjs.length; i++) {
    for (let j = i + 1; j < allObjs.length; j++) {
      const A = allObjs[i], B = allObjs[j];
      let pts = [];
      if      (A.type === 'line'   && B.type === 'line')   { const r = llIntersect(A.obj, B.obj); if (r) pts = [r]; }
      else if (A.type === 'line'   && B.type === 'circle')  pts = lcIntersect(A.obj, B.obj);
      else if (A.type === 'circle' && B.type === 'line')    pts = lcIntersect(B.obj, A.obj);
      else if (A.type === 'circle' && B.type === 'circle')  pts = ccIntersect(A.obj, B.obj);

      pts.forEach(function(p) {
        const d = Math.hypot(p.x - mx, p.y - my);
        if (d < SNAP_IX && d < bestD) { bestD = d; best = { x: p.x, y: p.y }; }
      });
    }
  }
  return best;
}

// ─────────────────────────────────────────────────────────────────
//  pickObj(mx, my) — finds the nearest line or circle within
//                    click distance (10px for line, 10px for circle).
//  Returns {type, id, obj} or null.
// ─────────────────────────────────────────────────────────────────
function pickObj(mx, my) {
  const CLICK_DIST = 10 / gZoom.scale;
  let best = null, bestD = Infinity;

  GS.lines.forEach(function(l) {
    const d = distToLine(l, mx, my);
    if (d < CLICK_DIST && d < bestD) { bestD = d; best = { type: 'line', id: l.id, obj: l }; }
  });
  GS.circles.forEach(function(c) {
    const d = distToCircle(c, mx, my);
    if (d < CLICK_DIST && d < bestD) { bestD = d; best = { type: 'circle', id: c.id, obj: c }; }
  });
  return best;
}

// ─────────────────────────────────────────────────────────────────
//  pickPoint(mx, my) — finds existing point within 12px.
// ─────────────────────────────────────────────────────────────────
function pickPoint(mx, my) {
  const SNAP = 12 / gZoom.scale;
  let best = null, bestD = Infinity;
  GS.pts.forEach(function(p) {
    const d = Math.hypot(p.x - mx, p.y - my);
    if (d < SNAP && d < bestD) { bestD = d; best = p; }
  });
  return best;
}

// ─────────────────────────────────────────────────────────────────
//  addPoint(x, y, helper, label) — creates and returns a new point.
// ─────────────────────────────────────────────────────────────────
function addPoint(x, y, helper, label) {
  // Reuse an existing point if very close (avoid duplicate)
  const existing = GS.pts.find(function(p) { return Math.hypot(p.x - x, p.y - y) < 1; });
  if (existing) return existing;
  const id = GS.nid++;
  const pt = { id: id, x: x, y: y, fixed: false, label: label || '', helper: !!helper };
  GS.pts.push(pt);
  return pt;
}

// ─────────────────────────────────────────────────────────────────
//  getOrCreatePoint(snap, mx, my) — returns point from snap or
//  creates a new free point at (mx, my).
// ─────────────────────────────────────────────────────────────────
function getOrCreatePoint(snap, mx, my) {
  if (snap && snap.ptId !== undefined) return getPt(snap.ptId);
  if (snap) return addPoint(snap.x, snap.y, false, '');
  return addPoint(mx, my, false, '');
}

// ═══════════════════════════════════════════════════════════════
//  DRAWING
// ═══════════════════════════════════════════════════════════════
function drawAll() {
  const ctx = _ctx;
  ctx.clearRect(0, 0, GW, GH);

  // White background
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, GW, GH);

  ctx.save();
  ctx.translate(gZoom.tx, gZoom.ty);
  ctx.scale(gZoom.scale, gZoom.scale);

  // Light grid
  ctx.strokeStyle = '#f1f5f9';
  ctx.lineWidth   = 1 / gZoom.scale;
  const GRID_STEP = 40;
  for (let x = 0; x <= GW; x += GRID_STEP) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, GH); ctx.stroke();
  }
  for (let y = 0; y <= GH; y += GRID_STEP) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(GW, y); ctx.stroke();
  }

  // Display-only segments via point IDs (given geometry)
  ctx.strokeStyle = '#94a3b8';
  ctx.lineWidth   = 1.5 / gZoom.scale;
  ctx.setLineDash([5, 4]);
  GS.segs.forEach(function(s) {
    const a = getPt(s.p1), b = getPt(s.p2);
    if (!a || !b) return;
    ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
  });
  // Display-only segments via absolute coords (no endpoint dots)
  GS.gsegs.forEach(function(s) {
    ctx.beginPath(); ctx.moveTo(s.x1, s.y1); ctx.lineTo(s.x2, s.y2); ctx.stroke();
  });
  ctx.setLineDash([]);

  // Infinite lines
  GS.lines.forEach(function(l) {
    const a = getPt(l.p1), b = getPt(l.p2);
    if (!a || !b) return;
    const isHovered = gHover && gHover.type === 'line' && gHover.id === l.id;
    ctx.strokeStyle = isHovered ? '#f97316' : '#64748b';
    ctx.lineWidth   = (isHovered ? 2.5 : 1.5) / gZoom.scale;
    // Extend the line far beyond the canvas; clipping does the rest
    const dx = b.x - a.x, dy = b.y - a.y;
    const len = Math.hypot(dx, dy);
    if (len < 1e-10) return;
    const ux = dx / len, uy = dy / len;
    const FAR = 10000;
    ctx.beginPath();
    ctx.moveTo(a.x - ux * FAR, a.y - uy * FAR);
    ctx.lineTo(a.x + ux * FAR, a.y + uy * FAR);
    ctx.stroke();
  });

  // Circles
  GS.circles.forEach(function(c) {
    const cen = getPt(c.cid), rpt = getPt(c.rid);
    if (!cen || !rpt) return;
    const r = Math.hypot(rpt.x - cen.x, rpt.y - cen.y);
    const isHovered = gHover && gHover.type === 'circle' && gHover.id === c.id;
    ctx.strokeStyle = isHovered ? '#f97316' : '#64748b';
    ctx.lineWidth   = (isHovered ? 2.5 : 1.5) / gZoom.scale;
    ctx.beginPath();
    ctx.arc(cen.x, cen.y, r, 0, Math.PI * 2);
    ctx.stroke();
  });

  // Points
  GS.pts.forEach(function(p) {
    const isSnap   = gSnap  && gSnap.ptId === p.id;
    const isHovered = gHover && gHover.type === 'point' && gHover.id === p.id;

    // Snap indicator ring
    if (isSnap) {
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth   = 2 / gZoom.scale;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 14 / gZoom.scale, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Point circle
    ctx.beginPath();
    if (p.fixed) {
      ctx.arc(p.x, p.y, 6 / gZoom.scale, 0, Math.PI * 2);
      ctx.fillStyle   = isHovered ? '#f97316' : '#1d4ed8';
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth   = 2 / gZoom.scale;
      ctx.stroke();
    } else if (p.helper) {
      ctx.arc(p.x, p.y, 4 / gZoom.scale, 0, Math.PI * 2);
      ctx.fillStyle = isHovered ? '#f97316' : '#94a3b8';
      ctx.fill();
    } else {
      ctx.arc(p.x, p.y, 5 / gZoom.scale, 0, Math.PI * 2);
      ctx.fillStyle   = isHovered ? '#f97316' : '#0891b2';
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth   = 1.5 / gZoom.scale;
      ctx.stroke();
    }

    // Label
    if (p.label) {
      ctx.fillStyle = p.fixed ? '#1d4ed8' : '#0891b2';
      ctx.font      = 'bold ' + Math.round(13 / gZoom.scale) + 'px "Segoe UI", system-ui, sans-serif';
      ctx.fillText(p.label, p.x + 8 / gZoom.scale, p.y - 8 / gZoom.scale);
    }
  });

  // Snap indicator for non-point snap (intersection snap)
  if (gSnap && gSnap.ptId === undefined) {
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth   = 2 / gZoom.scale;
    ctx.beginPath();
    ctx.arc(gSnap.x, gSnap.y, 10 / gZoom.scale, 0, Math.PI * 2);
    ctx.stroke();
  }

  ctx.restore();

  // Tool preview (dashed amber) — drawn in screen space
  drawPreview(ctx);
}

/**
 * drawPreview — draws an in-progress construction preview
 * while the user is mid-way through a multi-step tool.
 * Called after ctx.restore(), so coordinates are in screen space.
 */
function drawPreview(ctx) {
  if (gTS.step === 0 || gTS.picks.length === 0) return;
  const mx = gTS._mx !== undefined ? gTS._mx : 0;
  const my = gTS._my !== undefined ? gTS._my : 0;
  // Convert world to screen for preview
  const s = worldToScreen(mx, my);
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 1.5;
  ctx.setLineDash([6, 4]);
  if (gTool === 'line' || gTool === 'perp-bisector') {
    if (gTS.picks.length >= 1) {
      const p = getPt(gTS.picks[0]);
      if (p) {
        const ps = worldToScreen(p.x, p.y);
        ctx.beginPath(); ctx.moveTo(ps.x, ps.y); ctx.lineTo(s.x, s.y); ctx.stroke();
      }
    }
  } else if (gTool === 'circle') {
    if (gTS.picks.length >= 1) {
      const p = getPt(gTS.picks[0]);
      if (p) {
        const ps = worldToScreen(p.x, p.y);
        const r = Math.hypot(s.x - ps.x, s.y - ps.y);
        ctx.beginPath(); ctx.arc(ps.x, ps.y, r, 0, Math.PI * 2); ctx.stroke();
      }
    }
  } else if (gTool === 'angle-bisector') {
    if (gTS.picks.length === 1) {
      const p1 = getPt(gTS.picks[0]);
      if (p1) {
        const p1s = worldToScreen(p1.x, p1.y);
        ctx.beginPath(); ctx.moveTo(p1s.x, p1s.y); ctx.lineTo(s.x, s.y); ctx.stroke();
      }
    } else if (gTS.picks.length === 2) {
      // picks[0]=A, picks[1]=B(vertex) — preview second arm from vertex
      const pA = getPt(gTS.picks[0]), pB = getPt(gTS.picks[1]);
      if (pA && pB) {
        const pAs = worldToScreen(pA.x, pA.y), pBs = worldToScreen(pB.x, pB.y);
        ctx.beginPath(); ctx.moveTo(pAs.x, pAs.y); ctx.lineTo(pBs.x, pBs.y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(pBs.x, pBs.y); ctx.lineTo(s.x, s.y); ctx.stroke();
      }
    }
  } else if (gTool === 'perp') {
    if (gTS.picks.length === 1 && gTS.picks[0].type === 'point') {
      // First pick was a point, preview line from point to mouse
      const p = getPt(gTS.picks[0].id);
      if (p) {
        const ps = worldToScreen(p.x, p.y);
        ctx.beginPath(); ctx.moveTo(ps.x, ps.y); ctx.lineTo(s.x, s.y); ctx.stroke();
      }
    }
  }
  ctx.setLineDash([]);
}

// ═══════════════════════════════════════════════════════════════
//  MOUSE / TOUCH EVENT HANDLING
// ═══════════════════════════════════════════════════════════════

/** Convert a client mouse/touch event to canvas logical coordinates. */
function evtToCanvas(e) {
  const rect = _canvas.getBoundingClientRect();
  const scaleX = GW / rect.width;
  const scaleY = GH / rect.height;
  let cx, cy;
  if (e.touches && e.touches.length > 0) {
    cx = e.touches[0].clientX;
    cy = e.touches[0].clientY;
  } else {
    cx = e.clientX;
    cy = e.clientY;
  }
  return { x: (cx - rect.left) * scaleX, y: (cy - rect.top) * scaleY };
}

// ── mousemove / touchmove ────────────────────────────────────────
function onMove(e) {
  if (gCurProb === null) return;
  e.preventDefault();
  const sc = evtToCanvas(e);  // screen coords
  const { x: mx, y: my } = screenToWorld(sc.x, sc.y);  // world coords

  // Pan drag (move tool on empty space)
  if (gPan) {
    gZoom.tx = gPan.startTx + (sc.x - gPan.startSx);
    gZoom.ty = gPan.startTy + (sc.y - gPan.startSy);
    drawAll();
    return;
  }

  // Store world coords for preview rendering
  gTS._mx = mx; gTS._my = my;

  if (gTool === 'move' && gDrag) {
    const p = getPt(gDrag.ptId);
    if (p && !p.fixed) {
      p.x = mx + gDrag.ox;
      p.y = my + gDrag.oy;
      drawAll();
    }
    return;
  }

  gSnap  = findSnap(mx, my);
  if (gTool === 'move') {
    const p = pickPoint(mx, my);
    gHover = p ? { type: 'point', id: p.id } : null;
  } else if (gTool === 'delete' || gTool === 'perp' || gTool === 'parallel' || gTool === 'intersect') {
    const obj = pickObj(mx, my);
    gHover = obj ? { type: obj.type, id: obj.id } : null;
  } else {
    gHover = null;
  }
  drawAll();
}

// ── mousedown / touchstart ───────────────────────────────────────
function onDown(e) {
  if (gCurProb === null) return;
  e.preventDefault();
  const sc = evtToCanvas(e);  // screen coords
  const { x: mx, y: my } = screenToWorld(sc.x, sc.y);  // world coords

  if (gTool === 'move') {
    const p = pickPoint(mx, my);
    if (p && !p.fixed) {
      gDrag = { ptId: p.id, ox: p.x - mx, oy: p.y - my };
    } else {
      // Start pan
      gPan = { startSx: sc.x, startSy: sc.y, startTx: gZoom.tx, startTy: gZoom.ty };
    }
    return;
  }

  handleToolClick(mx, my);
}

// ── mouseup / touchend ───────────────────────────────────────────
function onUp(e) {
  if (gDrag) { gDrag = null; drawAll(); }
  if (gPan)  { gPan  = null; }
}

// ─────────────────────────────────────────────────────────────────
//  TOOL CLICK DISPATCHER
// ─────────────────────────────────────────────────────────────────
function handleToolClick(mx, my) {
  switch (gTool) {
    case 'point':         toolPoint(mx, my);         break;
    case 'line':          toolLine(mx, my);           break;
    case 'circle':        toolCircle(mx, my);         break;
    case 'perp-bisector': toolPerpBisector(mx, my);   break;
    case 'perp':          toolPerp(mx, my);           break;
    case 'angle-bisector':toolAngleBisector(mx, my);  break;
    case 'parallel':      toolParallel(mx, my);       break;
    case 'intersect':     toolIntersect(mx, my);      break;
    case 'delete':        toolDelete(mx, my);         break;
    default: break;
  }
}

// ═══════════════════════════════════════════════════════════════
//  INDIVIDUAL TOOLS
// ═══════════════════════════════════════════════════════════════

// ── 점 (Point) ──────────────────────────────────────────────────
function toolPoint(mx, my) {
  saveHistory();
  const snap = findSnap(mx, my);
  const pt   = getOrCreatePoint(snap, mx, my);
  updateGeoCount(); drawAll();
}

// ── 선 (Line) — 2 clicks → +1L +1E ─────────────────────────────
function toolLine(mx, my) {
  const snap = findSnap(mx, my);

  if (gTS.step === 0) {
    saveHistory();
    const pt = getOrCreatePoint(snap, mx, my);
    gTS.picks = [pt.id];
    gTS.step  = 1;
  } else {
    // Step 1: second point
    let pt2;
    if (snap && snap.ptId !== undefined && snap.ptId !== gTS.picks[0]) {
      pt2 = getPt(snap.ptId);
    } else if (snap && snap.ptId === undefined) {
      pt2 = addPoint(snap.x, snap.y, false, '');
    } else {
      pt2 = addPoint(mx, my, false, '');
    }

    const id = GS.nid++;
    GS.lines.push({ id: id, p1: gTS.picks[0], p2: pt2.id, lc: 1, ec: 1 });
    GS.lc += 1; GS.ec += 1;
    gTS = { step: 0, picks: [] };
    updateGeoCount(); drawAll();
  }
}

// ── 원 (Circle) — center → radius pt → +1L +1E ──────────────────
function toolCircle(mx, my) {
  const snap = findSnap(mx, my);

  if (gTS.step === 0) {
    saveHistory();
    const pt = getOrCreatePoint(snap, mx, my);
    gTS.picks = [pt.id];
    gTS.step  = 1;
  } else {
    let rPt;
    if (snap && snap.ptId !== undefined && snap.ptId !== gTS.picks[0]) {
      rPt = getPt(snap.ptId);
    } else if (snap && snap.ptId === undefined) {
      rPt = addPoint(snap.x, snap.y, false, '');
    } else {
      rPt = addPoint(mx, my, false, '');
    }

    const id = GS.nid++;
    GS.circles.push({ id: id, cid: gTS.picks[0], rid: rPt.id, lc: 1, ec: 1 });
    GS.lc += 1; GS.ec += 1;
    gTS = { step: 0, picks: [] };
    updateGeoCount(); drawAll();
  }
}

// ── 수직이등분선 (Perpendicular Bisector) — 2 pts → +1L +3E ─────
//   Construction: midpoint M of AB, then perpendicular through M.
//   3E = 2 helper points (circles to find mid + intersection) + 1 line action.
//   Simplified here: we place midpoint as helper, perpendicular direction helper,
//   then add the line.
function toolPerpBisector(mx, my) {
  const snap = findSnap(mx, my);

  if (gTS.step === 0) {
    saveHistory();
    const pt = getOrCreatePoint(snap, mx, my);
    gTS.picks = [pt.id];
    gTS.step  = 1;
  } else {
    // Step 1: second point chosen
    let pt2;
    if (snap && snap.ptId !== undefined && snap.ptId !== gTS.picks[0]) {
      pt2 = getPt(snap.ptId);
    } else if (snap && snap.ptId === undefined) {
      pt2 = addPoint(snap.x, snap.y, false, '');
    } else {
      pt2 = addPoint(mx, my, false, '');
    }

    const p1 = getPt(gTS.picks[0]);
    if (!p1 || !pt2) { gTS = { step:0, picks:[] }; return; }

    // Midpoint (helper)
    const mx2 = (p1.x + pt2.x) / 2;
    const my2 = (p1.y + pt2.y) / 2;
    const mid = addPoint(mx2, my2, true, '');

    // Perpendicular direction: rotate (p2-p1) by 90°
    const dx = pt2.x - p1.x, dy = pt2.y - p1.y;
    const perp = addPoint(mx2 - dy, my2 + dx, true, '');  // helper at offset

    const id = GS.nid++;
    GS.lines.push({ id: id, p1: mid.id, p2: perp.id, lc: 1, ec: 3 });
    GS.lc += 1; GS.ec += 3;
    gTS = { step: 0, picks: [] };
    updateGeoCount(); drawAll();
  }
}

// ── 수선 (Perpendicular) — supports point-first or line-first order → +1L +3E ──
function toolPerp(mx, my) {
  if (gTS.step === 0) {
    // Detect what the user clicked first: a point or a line
    const snap   = findSnap(mx, my);
    const ptHit  = (snap && snap.ptId !== undefined) ? getPt(snap.ptId) : null;
    const lineHit = pickObj(mx, my);

    if (ptHit) {
      // Point first: wait for line
      saveHistory();
      gTS.picks = [{ type: 'point', id: ptHit.id }];
      gTS.step  = 1;
      const msg = document.getElementById('geo-status-msg');
      if (msg) msg.textContent = '수선을 내릴 직선을 클릭하세요.';
    } else if (lineHit && lineHit.type === 'line') {
      // Line first: wait for point
      saveHistory();
      gTS.picks = [{ type: 'line', id: lineHit.id }];
      gTS.step  = 1;
      const msg = document.getElementById('geo-status-msg');
      if (msg) msg.textContent = '수선이 지나갈 점을 클릭하세요.';
    }
  } else {
    const firstPick = gTS.picks[0];
    let l, pt;

    if (firstPick.type === 'point') {
      // First was point → now pick a line
      const lineHit = pickObj(mx, my);
      if (!lineHit || lineHit.type !== 'line') return;
      l  = getLine(lineHit.id);
      pt = getPt(firstPick.id);
    } else {
      // First was line → now pick a point
      const snap = findSnap(mx, my);
      if (snap && snap.ptId !== undefined) pt = getPt(snap.ptId);
      else if (snap) pt = addPoint(snap.x, snap.y, false, '');
      else pt = addPoint(mx, my, false, '');
      l = getLine(firstPick.id);
    }

    if (!l || !pt) { gTS = { step: 0, picks: [] }; return; }

    const foot = footOnLine(l, pt.x, pt.y);
    if (!foot) { gTS = { step: 0, picks: [] }; return; }

    // If pt is on the line (foot ≈ pt), use perpendicular direction from line
    let footPt;
    if (Math.hypot(foot.x - pt.x, foot.y - pt.y) < 1) {
      const la = getPt(l.p1), lb = getPt(l.p2);
      if (!la || !lb) { gTS = { step: 0, picks: [] }; return; }
      const ldx = lb.x - la.x, ldy = lb.y - la.y;
      const llen = Math.hypot(ldx, ldy);
      if (llen < 1e-10) { gTS = { step: 0, picks: [] }; return; }
      footPt = addPoint(pt.x - ldy / llen * 100, pt.y + ldx / llen * 100, true, '');
    } else {
      footPt = addPoint(foot.x, foot.y, true, '');
    }

    const id = GS.nid++;
    GS.lines.push({ id: id, p1: pt.id, p2: footPt.id, lc: 1, ec: 3 });
    GS.lc += 1; GS.ec += 3;
    gTS = { step: 0, picks: [] };
    updateGeoCount(); drawAll();
  }
}

// ── 각의이등분선 (Angle Bisector) — A, B(vertex), C → +1L +4E ───
//   Click order: A (first arm) → B (vertex) → C (second arm)
//   Direction = normalize(B→A) + normalize(B→C)
function toolAngleBisector(mx, my) {
  const snap = findSnap(mx, my);

  if (gTS.step === 0) {
    // Click first arm point (A)
    saveHistory();
    const pt = getOrCreatePoint(snap, mx, my);
    gTS.picks = [pt.id];
    gTS.step  = 1;
    const msg = document.getElementById('geo-status-msg');
    if (msg) msg.textContent = '꼭짓점(각의 중심)을 클릭하세요.';
  } else if (gTS.step === 1) {
    // Click vertex (B)
    let pt;
    if (snap && snap.ptId !== undefined && snap.ptId !== gTS.picks[0]) pt = getPt(snap.ptId);
    else if (snap && snap.ptId === undefined) pt = addPoint(snap.x, snap.y, false, '');
    else pt = addPoint(mx, my, false, '');
    gTS.picks.push(pt.id);
    gTS.step = 2;
    const msg = document.getElementById('geo-status-msg');
    if (msg) msg.textContent = '두 번째 점(C)을 클릭하세요.';
    drawAll();
  } else {
    // Click second arm point (C)
    let pt;
    if (snap && snap.ptId !== undefined && snap.ptId !== gTS.picks[0] && snap.ptId !== gTS.picks[1]) pt = getPt(snap.ptId);
    else if (snap && snap.ptId === undefined) pt = addPoint(snap.x, snap.y, false, '');
    else pt = addPoint(mx, my, false, '');

    // picks[0]=A, picks[1]=B(vertex), picks[2]=C
    const pA = getPt(gTS.picks[0]);
    const v  = getPt(gTS.picks[1]);
    const pC = pt;
    if (!pA || !v || !pC) { gTS = { step: 0, picks: [] }; return; }

    const dA = Math.hypot(pA.x - v.x, pA.y - v.y);
    const dC = Math.hypot(pC.x - v.x, pC.y - v.y);
    if (dA < 1e-10 || dC < 1e-10) { gTS = { step: 0, picks: [] }; return; }

    const uAx = (pA.x - v.x) / dA, uAy = (pA.y - v.y) / dA;
    const uCx = (pC.x - v.x) / dC, uCy = (pC.y - v.y) / dC;
    const bx = uAx + uCx, by = uAy + uCy;
    const bl = Math.hypot(bx, by);

    let bisHelper;
    if (bl > 1e-10) {
      bisHelper = addPoint(v.x + bx / bl * 100, v.y + by / bl * 100, true, '');
    } else {
      bisHelper = addPoint(v.x - uAy * 100, v.y + uAx * 100, true, '');
    }

    const id = GS.nid++;
    GS.lines.push({ id: id, p1: v.id, p2: bisHelper.id, lc: 1, ec: 4 });
    GS.lc += 1; GS.ec += 4;
    gTS = { step: 0, picks: [] };
    updateGeoCount(); drawAll();
  }
}

// ── 평행선 (Parallel Line) — point↔line either order → +1L +4E ──
function toolParallel(mx, my) {
  if (gTS.step === 0) {
    // Point takes priority over line (same pattern as toolPerp)
    const snap    = findSnap(mx, my);
    const ptHit   = (snap && snap.ptId !== undefined) ? getPt(snap.ptId) : null;
    const lineHit = pickObj(mx, my);

    if (ptHit) {
      // Point first: wait for line
      saveHistory();
      gTS.picks = [{ type: 'point', id: ptHit.id }];
      gTS.step  = 1;
      const msg = document.getElementById('geo-status-msg');
      if (msg) msg.textContent = '평행하게 만들 직선을 클릭하세요.';
    } else if (lineHit && lineHit.type === 'line') {
      // Line first: wait for point
      saveHistory();
      gTS.picks = [{ type: 'line', id: lineHit.id }];
      gTS.step  = 1;
      const msg = document.getElementById('geo-status-msg');
      if (msg) msg.textContent = '평행선이 지나갈 점을 클릭하세요.';
    }
  } else {
    const firstPick = gTS.picks[0];
    let l, pt;

    if (firstPick.type === 'point') {
      // First was point → now pick a line
      const lineHit = pickObj(mx, my);
      if (!lineHit || lineHit.type !== 'line') return;
      l  = getLine(lineHit.id);
      pt = getPt(firstPick.id);
    } else {
      // First was line → now pick a point
      const snap = findSnap(mx, my);
      if (snap && snap.ptId !== undefined) pt = getPt(snap.ptId);
      else if (snap) pt = addPoint(snap.x, snap.y, false, '');
      else pt = addPoint(mx, my, false, '');
      l = getLine(firstPick.id);
    }

    if (!l || !pt) { gTS = { step: 0, picks: [] }; return; }

    const a = getPt(l.p1), b = getPt(l.p2);
    if (!a || !b) { gTS = { step: 0, picks: [] }; return; }

    // Direction vector of original line
    const dx = b.x - a.x, dy = b.y - a.y;
    const len = Math.hypot(dx, dy);
    if (len < 1e-10) { gTS = { step: 0, picks: [] }; return; }

    // Second defining point of the parallel line (hidden helper)
    const helper = addPoint(pt.x + dx, pt.y + dy, true, '');

    const id = GS.nid++;
    GS.lines.push({ id: id, p1: pt.id, p2: helper.id, lc: 1, ec: 4 });
    GS.lc += 1; GS.ec += 4;
    gTS = { step: 0, picks: [] };
    updateGeoCount(); drawAll();
  }
}

// ── 교차 (Intersect) — 2 objs → place intersection point(s) ─────
function toolIntersect(mx, my) {
  const obj = pickObj(mx, my);
  if (!obj) return;

  if (gTS.step === 0) {
    saveHistory();
    gTS.picks = [{ type: obj.type, id: obj.id }];
    gTS.step  = 1;
    // Highlight first picked object
    gHover = { type: obj.type, id: obj.id };
    drawAll();
  } else {
    if (obj.id === gTS.picks[0].id) return;  // same object, ignore

    const A = gTS.picks[0];
    const B = { type: obj.type, id: obj.id };

    let pts = [];
    if (A.type === 'line' && B.type === 'line') {
      const r = llIntersect(getLine(A.id), getLine(B.id));
      if (r) pts = [r];
    } else if (A.type === 'line' && B.type === 'circle') {
      pts = lcIntersect(getLine(A.id), getCircle(B.id));
    } else if (A.type === 'circle' && B.type === 'line') {
      pts = lcIntersect(getLine(B.id), getCircle(A.id));
    } else if (A.type === 'circle' && B.type === 'circle') {
      pts = ccIntersect(getCircle(A.id), getCircle(B.id));
    }

    pts.forEach(function(p) { addPoint(p.x, p.y, false, ''); });

    gTS = { step: 0, picks: [] };
    gHover = null;
    updateGeoCount(); drawAll();
  }
}

// ── 삭제 (Delete) — click obj → remove ──────────────────────────
function toolDelete(mx, my) {
  const obj = pickObj(mx, my);
  if (!obj) return;
  saveHistory();

  if (obj.type === 'line') {
    const l = getLine(obj.id);
    if (l) { GS.lc -= (l.lc || 0); GS.ec -= (l.ec || 0); }
    GS.lines = GS.lines.filter(function(x) { return x.id !== obj.id; });
  } else if (obj.type === 'circle') {
    const c = getCircle(obj.id);
    if (c) { GS.lc -= (c.lc || 0); GS.ec -= (c.ec || 0); }
    GS.circles = GS.circles.filter(function(x) { return x.id !== obj.id; });
  }

  // Clamp counters to zero
  GS.lc = Math.max(0, GS.lc);
  GS.ec = Math.max(0, GS.ec);

  updateGeoCount(); drawAll();
}

// ═══════════════════════════════════════════════════════════════
//  ZOOM / PAN
// ═══════════════════════════════════════════════════════════════
function applyZoom(factor, cx, cy) {
  // cx, cy in canvas screen coordinates (center of zoom)
  gZoom.tx = cx - (cx - gZoom.tx) * factor;
  gZoom.ty = cy - (cy - gZoom.ty) * factor;
  gZoom.scale *= factor;
  drawAll();
}
function zoomIn()    { applyZoom(1.25, GW / 2, GH / 2); }
function zoomOut()   { applyZoom(1 / 1.25, GW / 2, GH / 2); }
function zoomReset() { gZoom = { scale: 1, tx: 0, ty: 0 }; drawAll(); }

// Mouse wheel zoom
_canvas.addEventListener('wheel', function(e) {
  e.preventDefault();
  const sc = evtToCanvas(e);
  applyZoom(e.deltaY < 0 ? 1.15 : 1 / 1.15, sc.x, sc.y);
}, { passive: false });

// ═══════════════════════════════════════════════════════════════
//  EVENT LISTENER REGISTRATION
// ═══════════════════════════════════════════════════════════════
_canvas.addEventListener('mousemove',  onMove,  { passive: false });
_canvas.addEventListener('mousedown',  onDown,  { passive: false });
_canvas.addEventListener('mouseup',    onUp,    { passive: false });
_canvas.addEventListener('mouseleave', onUp,    { passive: false });

// Touch equivalents
_canvas.addEventListener('touchmove',  onMove,  { passive: false });
_canvas.addEventListener('touchstart', onDown,  { passive: false });
_canvas.addEventListener('touchend',   onUp,    { passive: false });
_canvas.addEventListener('touchcancel',onUp,    { passive: false });
"""
