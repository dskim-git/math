META = {
    "title": "미니: 작도 도구 — E값의 이유",
    "description": "수직이등분선·수선·각의이등분선·평행선 도구가 각각 몇 E인지 단계별 애니메이션으로 탐구합니다.",
    "order": 41,
    "hidden": True,
}

import streamlit as st
import streamlit.components.v1 as components

_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; padding: 12px; }

.tool-tabs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 16px; }
.tool-tab {
  padding: 7px 16px; border-radius: 8px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer; font-size: 0.85rem; font-weight: 700;
  transition: all .15s;
}
.tool-tab:hover { border-color: #60a5fa; color: #bfdbfe; }
.tool-tab.active { background: #1d4ed8; border-color: #3b82f6; color: #fff; }
.badge-e {
  display: inline-block; padding: 1px 8px; border-radius: 5px;
  background: #1e3a5f; color: #7dd3fc; font-size: 0.8rem; font-weight: 800;
  border: 1px solid #0ea5e9; margin-left: 6px;
}

.panel { display: none; }
.panel.active { display: block; }

.step-area { display: flex; gap: 14px; align-items: flex-start; flex-wrap: wrap; }
.canvas-wrap { position: relative; flex-shrink: 0; }
canvas { border: 1.5px solid #334155; border-radius: 8px; background: #1e293b; display: block; }

.step-info { flex: 1; min-width: 200px; }
.step-counter { font-size: 0.8rem; color: #64748b; margin-bottom: 6px; }
.step-text {
  background: #1e293b; border: 1px solid #334155; border-radius: 8px;
  padding: 12px 14px; font-size: 0.9rem; line-height: 1.55; min-height: 80px;
  color: #e2e8f0;
}
.step-text .hl { color: #fbbf24; font-weight: 700; }
.step-text .ce { color: #34d399; font-weight: 800; }
.step-text .cl { color: #60a5fa; font-weight: 800; }
.step-text .cf { color: #94a3b8; }

.nav-btns { display: flex; gap: 8px; margin-top: 10px; align-items: center; }
.nav-btn {
  padding: 7px 18px; border-radius: 7px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer; font-size: 0.85rem; font-weight: 700;
  transition: all .15s;
}
.nav-btn:hover:not(:disabled) { background: #334155; color: #e2e8f0; }
.nav-btn:disabled { opacity: 0.35; cursor: default; }
.nav-btn.primary { background: #1d4ed8; border-color: #3b82f6; color: #fff; }
.nav-btn.primary:hover:not(:disabled) { background: #2563eb; }
.total-badge {
  margin-left: auto; padding: 4px 12px; border-radius: 6px;
  background: #0f3460; border: 1px solid #0ea5e9; color: #7dd3fc;
  font-size: 0.82rem; font-weight: 800;
}
</style>
</head>
<body>

<div class="tool-tabs">
  <button class="tool-tab active" onclick="showTool(0)">수직이등분선 <span class="badge-e">3E</span></button>
  <button class="tool-tab" onclick="showTool(1)">수선 (선 밖의 점) <span class="badge-e">3E</span></button>
  <button class="tool-tab" onclick="showTool(2)">수선 (선 위의 점) <span class="badge-e">3E</span></button>
  <button class="tool-tab" onclick="showTool(3)">각의 이등분선 <span class="badge-e">4E</span></button>
  <button class="tool-tab" onclick="showTool(4)">평행선 <span class="badge-e">4E</span></button>
</div>

<!-- ① 수직이등분선 3E -->
<div class="panel active" id="panel-0">
  <div class="step-area">
    <div class="canvas-wrap"><canvas id="cv0" width="340" height="260"></canvas></div>
    <div class="step-info">
      <div class="step-counter" id="sc0"></div>
      <div class="step-text" id="st0"></div>
      <div class="nav-btns">
        <button class="nav-btn" id="prev0" onclick="step(0,-1)" disabled>◀ 이전</button>
        <button class="nav-btn primary" id="next0" onclick="step(0,1)">다음 ▶</button>
        <span class="total-badge">총 3E</span>
      </div>
    </div>
  </div>
</div>

<!-- ② 수선 (선 밖의 점) 3E -->
<div class="panel" id="panel-1">
  <div class="step-area">
    <div class="canvas-wrap"><canvas id="cv1" width="340" height="260"></canvas></div>
    <div class="step-info">
      <div class="step-counter" id="sc1"></div>
      <div class="step-text" id="st1"></div>
      <div class="nav-btns">
        <button class="nav-btn" id="prev1" onclick="step(1,-1)" disabled>◀ 이전</button>
        <button class="nav-btn primary" id="next1" onclick="step(1,1)">다음 ▶</button>
        <span class="total-badge">총 3E</span>
      </div>
    </div>
  </div>
</div>

<!-- ③ 수선 (선 위의 점) 3E -->
<div class="panel" id="panel-2">
  <div class="step-area">
    <div class="canvas-wrap"><canvas id="cv2" width="340" height="260"></canvas></div>
    <div class="step-info">
      <div class="step-counter" id="sc2"></div>
      <div class="step-text" id="st2"></div>
      <div class="nav-btns">
        <button class="nav-btn" id="prev2" onclick="step(2,-1)" disabled>◀ 이전</button>
        <button class="nav-btn primary" id="next2" onclick="step(2,1)">다음 ▶</button>
        <span class="total-badge">총 3E</span>
      </div>
    </div>
  </div>
</div>

<!-- ④ 각의 이등분선 4E -->
<div class="panel" id="panel-3">
  <div class="step-area">
    <div class="canvas-wrap"><canvas id="cv3" width="340" height="260"></canvas></div>
    <div class="step-info">
      <div class="step-counter" id="sc3"></div>
      <div class="step-text" id="st3"></div>
      <div class="nav-btns">
        <button class="nav-btn" id="prev3" onclick="step(3,-1)" disabled>◀ 이전</button>
        <button class="nav-btn primary" id="next3" onclick="step(3,1)">다음 ▶</button>
        <span class="total-badge">총 4E</span>
      </div>
    </div>
  </div>
</div>

<!-- ⑤ 평행선 4E -->
<div class="panel" id="panel-4">
  <div class="step-area">
    <div class="canvas-wrap"><canvas id="cv4" width="340" height="260"></canvas></div>
    <div class="step-info">
      <div class="step-counter" id="sc4"></div>
      <div class="step-text" id="st4"></div>
      <div class="nav-btns">
        <button class="nav-btn" id="prev4" onclick="step(4,-1)" disabled>◀ 이전</button>
        <button class="nav-btn primary" id="next4" onclick="step(4,1)">다음 ▶</button>
        <span class="total-badge">총 4E</span>
      </div>
    </div>
  </div>
</div>

<script>
// ── 유틸 ────────────────────────────────────────────────────────────────────
function drawBg(ctx, w, h) { ctx.clearRect(0, 0, w, h); }

function dot(ctx, x, y, r, color) {
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2);
  ctx.fillStyle = color; ctx.fill();
}

function lineSegment(ctx, x1, y1, x2, y2, color, width) {
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = width || 1.5;
  ctx.setLineDash([]);
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  ctx.restore();
}

function fullLine(ctx, x1, y1, x2, y2, color, width, W, H) {
  // 두 점을 지나는 직선을 캔버스 전체로 연장하여 그림
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = width || 2;
  ctx.setLineDash([]);
  const dx = x2 - x1, dy = y2 - y1;
  let t0 = -1000, t1 = 1000;
  ctx.beginPath(); ctx.moveTo(x1 + dx*t0, y1 + dy*t0); ctx.lineTo(x1 + dx*t1, y1 + dy*t1);
  ctx.stroke();
  ctx.restore();
}

function circle(ctx, x, y, r, color, width) {
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = width || 1.5;
  ctx.setLineDash([]);
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI*2); ctx.stroke();
  ctx.restore();
}

function lbl(ctx, text, x, y, color, size) {
  ctx.save();
  ctx.fillStyle = color || '#94a3b8';
  ctx.font = (size || 13) + 'px Segoe UI';
  ctx.fillText(text, x, y);
  ctx.restore();
}

// ── 상태 ────────────────────────────────────────────────────────────────────
const states = [0, 0, 0, 0, 0];

// ── 단계 텍스트 ─────────────────────────────────────────────────────────────
const STEPS = [
  // 0: 수직이등분선 3E
  [
    { text: '<span class="hl">① E1</span> — A를 중심으로, AB 길이보다 긴 반지름의 <span class="ce">원</span>을 그립니다.' },
    { text: '<span class="hl">② E2</span> — B를 중심으로, <b>같은 반지름</b>의 <span class="ce">원</span>을 그립니다. 두 원의 교점을 P, Q라 합니다.' },
    { text: '<span class="hl">③ E3</span> — 교점 P, Q를 잇는 <span class="cl">직선</span>을 그립니다.<br>✅ 이것이 AB의 <b>수직이등분선</b>입니다!<br><br><span class="ce">원 2개</span> + <span class="cl">직선 1개</span> = <b>3E</b>' },
  ],
  // 1: 수선 (선 밖의 점) 3E
  [
    { text: '<span class="cf">점 A를 ℓ 위에 자유롭게 잡습니다 (0E).</span><br><span class="hl">① E1</span> — A를 중심으로 반지름 AP인 <span class="ce">원</span>을 그립니다. ℓ과의 교점(A 기준 반대편)을 B라 합니다.<br><small style="color:#64748b">원이 ℓ과 만나는 두 점은 A에서 같은 거리에 있습니다.</small>' },
    { text: '<span class="hl">② E2</span> — B를 중심으로 반지름 BP인 <span class="ce">원</span>을 그립니다.<br>두 원(A 중심, B 중심)의 교점은 P와 P′입니다.<br><small style="color:#64748b">A, B 모두 P와 P′에서 등거리 → A, B가 PP′의 수직이등분선 위에 있음</small>' },
    { text: '<span class="hl">③ E3</span> — P와 P′을 잇는 <span class="cl">직선</span>을 그립니다.<br>✅ PP′ ⊥ ℓ<br><br><span class="ce">원 2개</span> + <span class="cl">직선 1개</span> = <b>3E</b>' },
  ],
  // 2: 수선 (선 위의 점) 3E — 탈레스 정리 이용
  [
    { text: '<span class="cf">직선 밖의 임의의 점 Q를 자유롭게 잡습니다 (0E).</span><br><span class="hl">① E1</span> — Q를 중심으로 P를 지나는 <span class="ce">원</span>을 그립니다.<br>원이 직선 ℓ과 만나는 다른 점을 R이라 합니다.' },
    { text: '<span class="hl">② E2</span> — R과 Q(원의 중심)를 잇는 <span class="cl">직선</span>을 그립니다.<br>이 직선이 원과 만나는 다른 점을 S라 합니다.<br><small style="color:#64748b">R과 S는 원의 지름 양 끝점 (QR = QS = 반지름이므로 RS는 지름)</small>' },
    { text: '<span class="hl">③ E3</span> — S와 P를 잇는 <span class="cl">직선</span>을 그립니다.<br>✅ SP ⊥ ℓ<br><small style="color:#64748b">탈레스 정리: 지름 RS에 대한 원주각 ∠RPS = 90°<br>∴ SP ⊥ PR, 즉 SP ⊥ ℓ</small><br><br><span class="ce">원 1개</span> + <span class="cl">직선 2개</span> = <b>3E</b>' },
  ],
  // 3: 각의 이등분선 4E
  [
    { text: '<span class="hl">① E1</span> — 꼭짓점 O를 중심으로 <span class="ce">원</span>을 그립니다. 두 변과의 교점을 A, B라 합니다.' },
    { text: '<span class="hl">② E2</span> — A를 중심으로 <span class="ce">원</span>을 그립니다.' },
    { text: '<span class="hl">③ E3</span> — B를 중심으로 <b>같은 반지름</b>의 <span class="ce">원</span>을 그립니다. 두 원의 교점을 P라 합니다.' },
    { text: '<span class="hl">④ E4</span> — O와 P를 잇는 <span class="cl">직선(반직선)</span>을 그립니다.<br>✅ 이것이 <b>각의 이등분선</b>입니다!<br><br><span class="ce">원 3개</span> + <span class="cl">직선 1개</span> = <b>4E</b>' },
  ],
  // 4: 평행선 4E
  [
    { text: '<span class="cf">ℓ 위의 점 Q를 자유롭게 잡습니다 (0E).</span><br><span class="hl">① E1</span> — Q를 중심으로 반지름 QP인 <span class="ce">원</span>을 그립니다. ℓ과의 교점을 A라 합니다. (QA = QP = r)' },
    { text: '<span class="hl">② E2</span> — P를 중심으로 <b>같은 반지름 r</b>인 <span class="ce">원</span>을 그립니다.' },
    { text: '<span class="hl">③ E3</span> — A를 중심으로 <b>같은 반지름 r</b>인 <span class="ce">원</span>을 그립니다.<br>원 P와 원 A의 교점을 D라 합니다.<br><small style="color:#64748b">QAPD는 평행사변형: QA ∥ PD이고 |QA|=|PD|=r</small>' },
    { text: '<span class="hl">④ E4</span> — P와 D를 잇는 <span class="cl">직선</span>을 그립니다.<br>✅ PD ∥ ℓ<br><br><span class="ce">원 3개</span> + <span class="cl">직선 1개</span> = <b>4E</b>' },
  ],
];

// ── 그리기 함수들 ────────────────────────────────────────────────────────────

function draw0(cv, s) { // 수직이등분선
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  drawBg(ctx, W, H);

  const Ax = W*0.28, Ay = H*0.62;
  const Bx = W*0.72, By = H*0.62;
  const mx = (Ax+Bx)/2, my = Ay;
  const R = (Bx - Ax) * 0.62;
  const d = Bx - Ax;
  const h = Math.sqrt(R*R - (d/2)*(d/2));

  // 선분 AB (주어진)
  lineSegment(ctx, Ax-20, Ay, Bx+20, Ay, '#475569', 1.5);
  dot(ctx, Ax, Ay, 4, '#94a3b8'); lbl(ctx, 'A', Ax-14, Ay+4);
  dot(ctx, Bx, By, 4, '#94a3b8'); lbl(ctx, 'B', Bx+6,  By+4);

  if (s >= 1) { // E1: 원 A
    circle(ctx, Ax, Ay, R, '#3b82f6', 1.5);
  }
  if (s >= 2) { // E2: 원 B → 교점 P, Q
    circle(ctx, Bx, By, R, '#a78bfa', 1.5);
    const Px = mx, Py = my - h;
    const Qx = mx, Qy = my + h;
    dot(ctx, Px, Py, 4, '#fbbf24'); lbl(ctx, 'P', Px+5, Py-4, '#fbbf24');
    dot(ctx, Qx, Qy, 4, '#fbbf24'); lbl(ctx, 'Q', Qx+5, Qy+14, '#fbbf24');
  }
  if (s >= 3) { // E3: 수직이등분선
    fullLine(ctx, mx, my-h, mx, my+h, '#34d399', 2.5, W, H);
    lbl(ctx, '수직이등분선', mx+6, my-10, '#34d399', 11);
  }
}

function draw1(cv, s) { // 수선 (선 밖의 점)
  // 올바른 3E 작도:
  // - A: ℓ 위 자유롭게 선택 (0E)
  // - E1: 원(A, 반지름 AP) → ℓ과의 교점 B
  // - E2: 원(B, 반지름 BP) → 두 원의 교점 P와 P′
  // - E3: 직선 PP′ (= 수선)
  // 핵심: A, B 모두 |AP'|=|AP|, |BP'|=|BP| → A, B가 PP'의 수직이등분선 위 → A,B ∈ ℓ → ℓ ⊥ PP'
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  drawBg(ctx, W, H);

  const lY = H * 0.58;
  const Px = W * 0.58, Py = H * 0.18;
  // A: ℓ 위 자유롭게 선택
  const Ax = W * 0.22, Ay = lY;
  const rA = Math.sqrt((Px-Ax)**2 + (Py-Ay)**2);
  // B: 원(A, rA) ∩ ℓ — A를 기준으로 오른쪽 교점
  const Bx = Ax + rA, By = lY;
  const rB = Math.sqrt((Px-Bx)**2 + (Py-By)**2);
  // P′: P를 ℓ에 대해 반사시킨 점 (두 원의 두 번째 교점)
  const Ppx = Px, Ppy = 2*lY - Py;

  // 직선 ℓ
  lineSegment(ctx, 10, lY, W-10, lY, '#475569', 1.5);
  lbl(ctx, 'ℓ', W-16, lY+4);
  dot(ctx, Px, Py, 4, '#94a3b8'); lbl(ctx, 'P', Px+5, Py-4);

  if (s >= 1) { // E1: 원(A, AP)
    circle(ctx, Ax, Ay, rA, '#3b82f6', 1.5);
    dot(ctx, Ax, Ay, 4, '#fbbf24'); lbl(ctx, 'A', Ax-14, Ay-6, '#fbbf24');
    dot(ctx, Bx, By, 4, '#fbbf24'); lbl(ctx, 'B', Bx+5,  By-6, '#fbbf24');
  }
  if (s >= 2) { // E2: 원(B, BP)
    circle(ctx, Bx, By, rB, '#a78bfa', 1.5);
    // P′는 캔버스 안쪽에 있으면 점으로 표시
    if (Ppy <= H + 5) {
      dot(ctx, Ppx, Math.min(Ppy, H-4), 4, '#fbbf24');
      lbl(ctx, "P′", Ppx+5, Math.min(Ppy+14, H-2), '#fbbf24');
    }
  }
  if (s >= 3) { // E3: 직선 PP′ (수선)
    fullLine(ctx, Px, Py, Ppx, Ppy, '#34d399', 2.5, W, H);
    lbl(ctx, '수선', Px+6, lY+18, '#34d399', 11);
  }
}

function draw2(cv, s) { // 수선 (선 위의 점) — 탈레스 정리
  // 올바른 3E 작도:
  // - Q: ℓ 밖 임의 점 (자유, 0E)
  // - E1: 원(Q, QP) → R: ℓ과의 다른 교점
  // - E2: 직선 QR → S: 원과의 다른 교점 (RS가 지름)
  // - E3: 직선 SP ⊥ ℓ  (탈레스 정리: ∠RPS = 90°)
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  drawBg(ctx, W, H);

  const lY = H * 0.70;
  const Px = W * 0.45, Py = lY;
  // Q: 자유롭게 선택한 점 (ℓ 위, 왼쪽 위)
  const Qx = W * 0.28, Qy = H * 0.45;
  const r  = Math.sqrt((Px - Qx) ** 2 + (Py - Qy) ** 2);
  // R = 원(Q,r) ∩ ℓ의 두 번째 교점 = (2Qx − Px, lY)
  const Rx = 2 * Qx - Px, Ry = lY;
  // S = 지름 반대편 = 2Q − R = (Px, 2Qy − lY)
  const Sx = Px, Sy = 2 * Qy - lY;

  // 직선 ℓ
  lineSegment(ctx, 10, lY, W - 10, lY, '#475569', 1.5);
  lbl(ctx, 'ℓ', W - 16, lY + 4);
  dot(ctx, Px, Py, 4, '#94a3b8'); lbl(ctx, 'P', Px + 5, Py + 12);

  if (s >= 1) { // E1: 원(Q, QP) → R
    dot(ctx, Qx, Qy, 4, '#7dd3fc'); lbl(ctx, 'Q', Qx - 14, Qy - 2, '#7dd3fc');
    circle(ctx, Qx, Qy, r, '#3b82f6', 1.5);
    dot(ctx, Rx, Ry, 4, '#fbbf24'); lbl(ctx, 'R', Rx - 14, Ry + 14, '#fbbf24');
  }
  if (s >= 2) { // E2: 직선 QR (원의 지름) → S
    fullLine(ctx, Rx, Ry, Qx, Qy, '#a78bfa', 1.8, W, H);
    dot(ctx, Sx, Sy, 4, '#fbbf24'); lbl(ctx, 'S', Sx + 5, Sy - 4, '#fbbf24');
  }
  if (s >= 3) { // E3: 직선 SP → 수선
    fullLine(ctx, Sx, Sy, Px, Py, '#34d399', 2.5, W, H);
    lbl(ctx, '수선', Px + 6, lY - 18, '#34d399', 11);
  }
}

function draw3(cv, s) { // 각의 이등분선
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  drawBg(ctx, W, H);

  const O = {x: W*0.22, y: H*0.70};
  const e1 = {x: W*0.95, y: H*0.70};
  const e2 = {x: W*0.55, y: H*0.08};

  lineSegment(ctx, O.x, O.y, e1.x, e1.y, '#475569', 1.5);
  lineSegment(ctx, O.x, O.y, e2.x, e2.y, '#475569', 1.5);
  dot(ctx, O.x, O.y, 4, '#94a3b8'); lbl(ctx, 'O', O.x-16, O.y+4);

  const d1 = {x: e1.x-O.x, y: e1.y-O.y};
  const d2 = {x: e2.x-O.x, y: e2.y-O.y};
  const l1 = Math.sqrt(d1.x**2+d1.y**2), l2 = Math.sqrt(d2.x**2+d2.y**2);
  const u1 = {x:d1.x/l1, y:d1.y/l1}, u2 = {x:d2.x/l2, y:d2.y/l2};
  const R0 = W*0.22;
  const A = {x: O.x+u1.x*R0, y: O.y+u1.y*R0};
  const B = {x: O.x+u2.x*R0, y: O.y+u2.y*R0};
  const R2 = R0 * 0.65;

  // 교점 P 계산 (원 A, 원 B의 교점 중 O 바깥쪽)
  function circleIntersectOuter(c1, c2, ref, r) {
    const mx = (c1.x+c2.x)/2, my = (c1.y+c2.y)/2;
    const dd = Math.sqrt((c2.x-c1.x)**2+(c2.y-c1.y)**2) / 2;
    if (r <= dd) return null;
    const h = Math.sqrt(r*r - dd*dd);
    const nx = -(c2.y-c1.y)/Math.sqrt((c2.x-c1.x)**2+(c2.y-c1.y)**2);
    const ny =  (c2.x-c1.x)/Math.sqrt((c2.x-c1.x)**2+(c2.y-c1.y)**2);
    const p1 = {x:mx+nx*h, y:my+ny*h};
    const p2 = {x:mx-nx*h, y:my-ny*h};
    const d1 = (p1.x-ref.x)**2+(p1.y-ref.y)**2;
    const d2 = (p2.x-ref.x)**2+(p2.y-ref.y)**2;
    return d1 > d2 ? p1 : p2;
  }

  if (s >= 1) {
    circle(ctx, O.x, O.y, R0, '#3b82f6', 1.5);
    dot(ctx, A.x, A.y, 4, '#fbbf24'); lbl(ctx, 'A', A.x+5,  A.y+4,  '#fbbf24');
    dot(ctx, B.x, B.y, 4, '#fbbf24'); lbl(ctx, 'B', B.x-14, B.y-4,  '#fbbf24');
  }
  if (s >= 2) {
    circle(ctx, A.x, A.y, R2, '#a78bfa', 1.5);
  }
  if (s >= 3) {
    circle(ctx, B.x, B.y, R2, '#f472b6', 1.5);
    const P = circleIntersectOuter(A, B, O, R2);
    if (P) { dot(ctx, P.x, P.y, 4, '#fbbf24'); lbl(ctx, 'P', P.x+5, P.y-4, '#fbbf24'); }
  }
  if (s >= 4) {
    const P = circleIntersectOuter(A, B, O, R2);
    if (P) {
      const dv = {x: P.x-O.x, y: P.y-O.y};
      const dl = Math.sqrt(dv.x**2+dv.y**2);
      fullLine(ctx, O.x, O.y, O.x+dv.x/dl*300, O.y+dv.y/dl*300, '#34d399', 2.5, W, H);
      lbl(ctx, '이등분선', O.x+dv.x/dl*80+4, O.y+dv.y/dl*80-4, '#34d399', 11);
    }
  }
}

function draw4(cv, s) { // 평행선
  // 올바른 4E 작도 (세 원 모두 같은 반지름 r = QP):
  // - Q: ℓ 위 자유롭게 선택 (0E)
  // - E1: 원(Q, r=QP) → ℓ과의 교점 A (QA = r)
  // - E2: 원(P, r)
  // - E3: 원(A, r) → 원 P와의 교점 D
  // - E4: 직선 PD ∥ ℓ
  // 핵심: D = P + (A - Q) → QAPD 평행사변형 → PD ∥ QA ∥ ℓ
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  drawBg(ctx, W, H);

  const lY = H * 0.70;
  const Px = W * 0.50, Py = H * 0.25;
  const Qx = W * 0.22, Qy = lY;
  const r  = Math.sqrt((Px-Qx)**2 + (Py-Qy)**2);
  // A: 원(Q,r) ∩ ℓ — Q 오른쪽 교점
  const Ax = Qx + r, Ay = lY;
  // D: P + (A - Q) = (Px + r, Py)  [평행사변형 꼭짓점]
  const Dx = Px + r, Dy = Py;  // 참고: |DP| = r, |DA| = |QP| = r ✓

  // 직선 ℓ
  lineSegment(ctx, 10, lY, W-10, lY, '#475569', 1.5);
  lbl(ctx, 'ℓ', W-16, lY+4);
  dot(ctx, Px, Py, 4, '#94a3b8'); lbl(ctx, 'P', Px-14, Py);

  if (s >= 1) { // E1: 원(Q, r) → A
    dot(ctx, Qx, Qy, 4, '#7dd3fc'); lbl(ctx, 'Q', Qx-14, Qy+14, '#7dd3fc');
    circle(ctx, Qx, Qy, r, '#3b82f6', 1.5);
    dot(ctx, Ax, Ay, 4, '#fbbf24'); lbl(ctx, 'A', Ax+5, Ay-6, '#fbbf24');
  }
  if (s >= 2) { // E2: 원(P, r)
    circle(ctx, Px, Py, r, '#a78bfa', 1.5);
  }
  if (s >= 3) { // E3: 원(A, r) → D
    circle(ctx, Ax, Ay, r, '#f472b6', 1.5);
    // D는 원P와 원A의 교점 중 위쪽 (y 작은 쪽)
    dot(ctx, Dx, Dy, 4, '#fbbf24'); lbl(ctx, 'D', Dx+5, Dy-4, '#fbbf24');
  }
  if (s >= 4) { // E4: 직선 PD (평행선)
    fullLine(ctx, Px, Py, Dx, Dy, '#34d399', 2.5, W, H);
    lbl(ctx, '평행선', (Px+Dx)/2, Py-10, '#34d399', 11);
  }
}

const DRAW_FNS = [draw0, draw1, draw2, draw3, draw4];
const CVS = [0,1,2,3,4].map(i => document.getElementById('cv'+i));

function redraw(i) { DRAW_FNS[i](CVS[i], states[i]); }

function step(i, dir) {
  const max = STEPS[i].length;
  states[i] = Math.max(1, Math.min(max, states[i] + dir));
  redraw(i);
  const s = states[i];
  document.getElementById('st'+i).innerHTML = STEPS[i][s-1].text;
  document.getElementById('sc'+i).textContent = '단계 ' + s + ' / ' + max;
  document.getElementById('prev'+i).disabled = (s <= 1);
  document.getElementById('next'+i).disabled = (s >= max);
}

let activeTool = 0;
function showTool(i) {
  document.querySelectorAll('.tool-tab').forEach((t,j) => t.classList.toggle('active', j===i));
  document.querySelectorAll('.panel').forEach((p,j) => p.classList.toggle('active', j===i));
  activeTool = i;
  redraw(i);
}

// 초기화
(function init() {
  for (let i = 0; i < 5; i++) {
    states[i] = 1;
    redraw(i);
    document.getElementById('st'+i).innerHTML = STEPS[i][0].text;
    document.getElementById('sc'+i).textContent = '단계 1 / ' + STEPS[i].length;
    document.getElementById('prev'+i).disabled = true;
    document.getElementById('next'+i).disabled = (STEPS[i].length <= 1);
  }
})();
</script>
</body>
</html>
"""


def render():
    st.header("📐 작도 도구 — 왜 몇 E일까?")
    st.caption(
        "컴퍼스(원 = 1E)와 자(직선/반직선 = 1E)를 써서 각 도구를 만드는 단계별 과정을 살펴봅니다. "
        "▶ 다음 버튼을 눌러 한 단계씩 따라가 보세요."
    )
    components.html(_HTML, height=400, scrolling=False)
