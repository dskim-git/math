import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "파스칼삼각형성질탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이 활동과 관련된 이항계수·파스칼의 삼각형 문제 2개를 스스로 만들고 풀어보세요**"},
    {"key": "문제1", "label": "문제 1", "type": "text_area",  "height": 80},
    {"key": "답1",   "label": "문제 1의 답", "type": "text_input"},
    {"key": "문제2", "label": "문제 2", "type": "text_area",  "height": 80},
    {"key": "답2",   "label": "문제 2의 답", "type": "text_input"},
    {"key": "새롭게알게된점", "label": "💡 이 활동을 통해 새롭게 알게 된 점", "type": "text_area", "height": 100},
    {"key": "느낀점",        "label": "💬 이 활동을 통해 느낀 점",           "type": "text_area", "height": 100},
]

META = {
    "title":       "파스칼의 삼각형 성질 탐구",
    "description": "파스칼의 삼각형에서 이항계수의 6가지 성질을 직접 셀을 클릭하며 탐구하고 퀴즈로 확인합니다.",
    "order":       62,
    "hidden":      True,
}

HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f172a; color: #f1f5f9;
  font-family: 'Segoe UI', system-ui, sans-serif;
  overflow-x: hidden;
}
#app { max-width: 100%; padding: 10px 12px 20px; }

/* ── 탭 ── */
.tabs { display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 10px; }
.tab-btn {
  padding: 6px 10px; border-radius: 8px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer;
  font-size: 0.74rem; font-weight: 600; transition: all .15s; white-space: nowrap;
}
.tab-btn:hover  { border-color: #64748b; color: #e2e8f0; }
.tab-btn.active { background: #1d4ed8; border-color: #3b82f6; color: #fff; }
.tab-btn.quiz-tab.active { background: #7c3aed; border-color: #a78bfa; }

/* ── 성질 카드 ── */
.prop-card {
  background: #1e293b; border-radius: 11px; padding: 11px 13px; margin-bottom: 8px;
}
.prop-title   { font-size: 0.9rem; font-weight: 700; color: #f1f5f9; margin-bottom: 3px; }
.prop-formula {
  font-size: 0.82rem; color: #fbbf24; background: #0f172a;
  border-radius: 5px; padding: 3px 9px; display: inline-block;
  margin-bottom: 5px; font-family: 'Courier New', monospace;
}
.prop-hint { font-size: 0.76rem; color: #64748b; }

/* ── 뷰 토글 ── */
.view-toggle { display: flex; gap: 6px; align-items: center; margin-bottom: 6px; }
.vt-label { font-size: 0.76rem; color: #64748b; }
.vt-btn {
  padding: 3px 11px; border-radius: 6px; border: 1px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer; font-size: 0.76rem; font-weight: 600;
  transition: all .15s;
}
.vt-btn.active { background: #0f4c81; border-color: #3b82f6; color: #93c5fd; }

/* ── 삼각형: width:100%, overflow:hidden으로 가로 스크롤 없음 ── */
#triWrap {
  width: 100%; overflow: hidden;
  background: #0f172a; border-radius: 10px; padding: 2px 0;
}
#triWrap svg { display: block; width: 100%; height: auto; }
.tri-cell { cursor: pointer; }
.tri-cell rect { transition: fill .12s, stroke .12s; }
.tri-cell:hover rect { filter: brightness(1.25); }

/* ── 결과 ── */
#result {
  min-height: 36px; background: #1e293b; border-radius: 8px;
  padding: 7px 12px; margin-top: 6px;
  font-size: 0.83rem; color: #64748b; line-height: 1.6;
}

/* ── 퀴즈 ── */
.q-card {
  background: #1e293b; border-radius: 11px; padding: 13px 14px; margin-bottom: 11px;
  border: 2px solid transparent; transition: border-color .2s;
}
.q-card.correct { border-color: #059669; }
.q-card.wrong   { border-color: #dc2626; }
.q-num  { font-size: 0.68rem; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
.q-text { font-size: 0.86rem; color: #e2e8f0; margin-bottom: 9px; line-height: 1.5; }
.q-choices { display: flex; flex-direction: column; gap: 5px; }
.q-choice {
  padding: 7px 11px; border-radius: 7px; border: 1.5px solid #334155;
  background: #0f172a; color: #cbd5e1; cursor: pointer; font-size: 0.81rem;
  text-align: left; transition: all .15s;
}
.q-choice:hover:not(:disabled) { border-color: #3b82f6; color: #fff; background: #1e3a5f; }
.q-choice.sel-correct { background: #064e3b; border-color: #10b981; color: #6ee7b7; }
.q-choice.sel-wrong   { background: #450a0a; border-color: #f87171; color: #fca5a5; }
.q-choice.show-ans    { background: #064e3b; border-color: #10b981; color: #6ee7b7; }
.q-choice:disabled { cursor: default; }
.q-fb { font-size: 0.79rem; margin-top: 7px; padding: 5px 9px; border-radius: 5px; }
.q-fb.correct { background: #064e3b; color: #6ee7b7; }
.q-fb.wrong   { background: #450a0a; color: #fca5a5; }
.score-box { background: #1e293b; border-radius: 11px; padding: 14px; text-align: center; margin-top: 8px; }
.score-big { font-size: 2rem; font-weight: 900; color: #fbbf24; }
.score-msg { font-size: 0.84rem; color: #94a3b8; margin-top: 4px; }
.re-btn {
  display: inline-block; margin-top: 10px; padding: 7px 18px;
  background: #7c3aed; color: #fff; border-radius: 8px; border: none;
  cursor: pointer; font-weight: 700; font-size: 0.83rem;
}
</style>
</head>
<body>
<div id="app">

  <!-- 탭 -->
  <div class="tabs" id="tabBar">
    <button class="tab-btn active" data-tab="1">① 좌우대칭</button>
    <button class="tab-btn" data-tab="2">② 역삼각형</button>
    <button class="tab-btn" data-tab="3">③ 이항전개</button>
    <button class="tab-btn" data-tab="4">④ 행의 합</button>
    <button class="tab-btn" data-tab="5">⑤ 하키스틱</button>
    <button class="tab-btn" data-tab="6">⑥ 소수 행</button>
    <button class="tab-btn quiz-tab" data-tab="Q">🎯 퀴즈</button>
  </div>

  <!-- 성질 카드 -->
  <div class="prop-card" id="propCard">
    <div class="prop-title"   id="propTitle"></div>
    <div class="prop-formula" id="propFormula"></div>
    <div class="prop-hint"    id="propHint"></div>
  </div>

  <!-- 뷰 토글 -->
  <div class="view-toggle" id="viewToggle">
    <span class="vt-label">표시:</span>
    <button class="vt-btn active" id="btnNum">숫자</button>
    <button class="vt-btn"        id="btnComb">이항계수</button>
  </div>

  <!-- 하키스틱 방향 토글 (탭 5 전용) -->
  <div class="view-toggle" id="hockeyToggle" style="display:none">
    <span class="vt-label">방향:</span>
    <button class="vt-btn active" id="btnHockeyR">▶ 우방향 (열 고정)</button>
    <button class="vt-btn"        id="btnHockeyL">◀ 좌방향 (대각선 고정)</button>
  </div>

  <!-- 삼각형 -->
  <div id="triWrap"></div>

  <!-- 결과 -->
  <div id="result">셀을 클릭하면 해당 성질이 표시됩니다.</div>

  <!-- 퀴즈 패널 -->
  <div id="quizPanel" style="display:none">
    <div id="quizArea"></div>
  </div>

</div>

<script>
(function(){
"use strict";

// ── 이항계수 ──
function C(n, k) {
  if (k < 0 || k > n) return 0;
  if (k === 0 || k === n) return 1;
  k = Math.min(k, n - k);
  let r = 1;
  for (let i = 0; i < k; i++) r = r * (n - i) / (i + 1);
  return Math.round(r);
}
function isPrime(n) {
  if (n < 2) return false;
  for (let i = 2; i * i <= n; i++) if (n % i === 0) return false;
  return true;
}

// ── SVG 레이아웃 ──
// viewBox 고정 좌표계 + width="100%" → 컨테이너에 맞게 자동 스케일, 가로 스크롤 없음
const ROWS = 9;
const VW = 760, VH = 490;
const CW = 68, CH = 42, GAP_X = 8, GAP_Y = 10;
const PAD_X = 18, PAD_Y = 14;

function cellPos(r, c) {
  const usableW = VW - 2 * PAD_X;
  const rowW = (r + 1) * CW + r * GAP_X;
  const sx = PAD_X + (usableW - rowW) / 2;
  return { x: sx + c * (CW + GAP_X), y: PAD_Y + r * (CH + GAP_Y) };
}

// ── 상태 ──
let activeTab  = 1;
let viewMode   = 'num';
let hockeyDir  = 'right';   // 'right' | 'left'
let highlights = [];

// ── SVG 생성 ──
function buildSVG() {
  const hMap = {};
  highlights.forEach(h => { hMap[`${h.r},${h.c}`] = h; });

  // width="100%", height="auto", viewBox 고정 → 절대 가로 스크롤 없음
  let svg = `<svg xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 ${VW} ${VH}" width="100%" height="auto"
    preserveAspectRatio="xMidYMid meet">`;

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c <= r; c++) {
      const { x, y } = cellPos(r, c);
      const h      = hMap[`${r},${c}`];
      const fill   = h ? h.fill   : '#1e293b';
      const stroke = h ? h.stroke : '#334155';
      const tc     = h ? (h.textColor || '#f1f5f9') : '#cbd5e1';
      const val    = C(r, c);

      svg += `<g class="tri-cell" data-r="${r}" data-c="${c}">`;
      svg += `<rect x="${x}" y="${y}" width="${CW}" height="${CH}" rx="7"
        fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>`;

      if (viewMode === 'comb') {
        // nCr 표기: n·C·r 모두 아래 첨자(subscript) 위치
        // n(왼쪽 아래) C(중앙) r(오른쪽 아래)
        const cx = x + CW / 2;
        const cy = y + CH / 2;
        svg += `<text x="${cx-10}" y="${cy+13}" text-anchor="middle"
          font-size="11" fill="${tc}" font-family="serif" font-style="italic">${r}</text>`;
        svg += `<text x="${cx+1}" y="${cy+7}" text-anchor="middle"
          font-size="17" fill="${tc}" font-family="serif" font-weight="bold">C</text>`;
        svg += `<text x="${cx+12}" y="${cy+13}" text-anchor="middle"
          font-size="11" fill="${tc}" font-family="serif" font-style="italic">${c}</text>`;
      } else {
        const fs = val >= 10000 ? 9 : val >= 1000 ? 11 : val >= 100 ? 13 : 15;
        svg += `<text x="${x+CW/2}" y="${y+CH/2+fs*0.38}" text-anchor="middle"
          font-size="${fs}" fill="${tc}"
          font-family="'Segoe UI',system-ui,sans-serif" font-weight="700">${val}</text>`;
      }
      svg += '</g>';
    }
  }
  svg += '</svg>';
  return svg;
}

function renderTriangle() {
  const wrap = document.getElementById('triWrap');
  wrap.innerHTML = buildSVG();
  wrap.querySelectorAll('.tri-cell').forEach(g => {
    g.addEventListener('click', () => handleCellClick(+g.dataset.r, +g.dataset.c));
  });
}

// ── 결과 표시 ──
function setResult(html) {
  const el = document.getElementById('result');
  el.innerHTML = html;
  el.style.color = '#e2e8f0';
}
function clearResult() {
  const el = document.getElementById('result');
  el.innerHTML = '셀을 클릭하면 해당 성질이 표시됩니다.';
  el.style.color = '#64748b';
}

// ── 성질 핸들러 ──

// ① 좌우대칭
function doSymmetry(r, c) {
  const mirror = r - c;
  const isMid  = (c === mirror);
  const hl     = [];
  if (isMid) {
    hl.push({ r, c, fill: '#4c1d95', stroke: '#a78bfa', textColor: '#c4b5fd' });
  } else {
    const lo = Math.min(c, mirror), hi = Math.max(c, mirror);
    hl.push({ r, c: lo, fill: '#1d4ed8', stroke: '#60a5fa', textColor: '#bfdbfe' });
    hl.push({ r, c: hi, fill: '#065f46', stroke: '#34d399', textColor: '#a7f3d0' });
  }
  highlights = hl; renderTriangle();
  setResult(
    isMid
      ? `<span style="color:#c4b5fd">${r}C${c} = ${C(r,c)} &nbsp;←&nbsp; 중앙값 (자기 자신과 대칭)</span>`
      : `<span style="color:#60a5fa">${r}C${Math.min(c,mirror)} = ${C(r,Math.min(c,mirror))}</span>`
        + ` &nbsp;=&nbsp; `
        + `<span style="color:#34d399">${r}C${Math.max(c,mirror)} = ${C(r,Math.max(c,mirror))}</span>`
        + `&nbsp;&nbsp;✔&nbsp; <em>ₙCᵣ = ₙCₙ₋ᵣ</em>&nbsp;(n=${r}, r=${Math.min(c,mirror)}, n−r=${Math.max(c,mirror)})`
  );
}

// ② 역삼각형 (파스칼의 법칙)
function doPascal(r, c) {
  if (r === 0) {
    highlights = [{ r, c, fill: '#1e3a5f', stroke: '#3b82f6', textColor: '#93c5fd' }];
    renderTriangle();
    setResult('<span style="color:#fbbf24">0행은 위쪽 부모 셀이 없습니다.</span>');
    return;
  }
  const hl = [];
  const hasL = c > 0, hasR = c < r;
  if (hasL) hl.push({ r: r-1, c: c-1, fill: '#1d4ed8', stroke: '#60a5fa', textColor: '#bfdbfe' });
  if (hasR) hl.push({ r: r-1, c,      fill: '#1d4ed8', stroke: '#60a5fa', textColor: '#bfdbfe' });
  hl.push({ r, c, fill: '#065f46', stroke: '#34d399', textColor: '#a7f3d0' });
  highlights = hl; renderTriangle();

  const lv = hasL ? C(r-1,c-1) : 0, rv = hasR ? C(r-1,c) : 0;
  const ls = hasL ? `<span style="color:#60a5fa">${r-1}C${c-1}(=${lv})</span>` : '';
  const rs = hasR ? `<span style="color:#60a5fa">${r-1}C${c}(=${rv})</span>`   : '';
  setResult(
    [ls,rs].filter(Boolean).join(' + ')
    + ` = <span style="color:#34d399"><strong>${r}C${c} = ${lv+rv}</strong></span>`
    + `&nbsp;&nbsp;✔&nbsp;<em>ₙCᵣ = ₙ₋₁Cᵣ₋₁ + ₙ₋₁Cᵣ</em>`
  );
}

// ③ 이항전개
function doBinom(r, c) {
  highlights = Array.from({length: r+1}, (_, k) => ({
    r, c: k, fill: '#78350f', stroke: '#f59e0b', textColor: '#fde68a'
  }));
  renderTriangle();
  const terms = Array.from({length: r+1}, (_, k) => {
    const co = C(r,k), ae = r-k, be = k;
    let t = (co===1 && (ae>0||be>0)) ? '' : String(co);
    if (ae>0) t += ae===1?'a':`a^${ae}`;
    if (be>0) t += be===1?'b':`b^${be}`;
    return t||'1';
  });
  setResult(`<span style="color:#fbbf24">(a+b)<sup>${r}</sup> = ${terms.join(' + ')}</span>`);
}

// ④ 행의 합
function doRowSum(r, c) {
  highlights = Array.from({length: r+1}, (_, k) => ({
    r, c: k, fill: '#3b0764', stroke: '#a78bfa', textColor: '#e9d5ff'
  }));
  renderTriangle();
  const sum   = Array.from({length: r+1}, (_, k) => C(r,k)).reduce((a,b)=>a+b, 0);
  const parts = Array.from({length: r+1}, (_, k) => C(r,k)).join(' + ');
  setResult(
    `<span style="color:#a78bfa">행 ${r}: &nbsp;${parts} = <strong>${sum}</strong>`
    + ` = 2<sup>${r}</sup> = ${Math.pow(2,r)}</span>`
  );
}

// ⑤ 하키스틱 — 우방향: 열 c를 고정, (c,c)~(r,c) 합 = (r+1, c+1)
// Σᵢ₌ᶜʳ C(i,c) = C(r+1, c+1)
function doHockeyRight(r, c) {
  if (c > r) return;
  const hl = [];
  for (let row = c; row <= r; row++) {
    hl.push({ r: row, c, fill: '#1e3a5f', stroke: '#3b82f6', textColor: '#93c5fd' });
  }
  if (r+1 < ROWS) hl.push({ r: r+1, c: c+1, fill: '#064e3b', stroke: '#10b981', textColor: '#6ee7b7' });
  highlights = hl; renderTriangle();

  const parts = Array.from({length: r-c+1}, (_, i) => {
    const row = c+i; return `${row}C${c}(=${C(row,c)})`;
  }).join(' + ');
  const tipStr = r+1 < ROWS
    ? `<span style="color:#10b981"><strong>${r+1}C${c+1} = ${C(r+1,c+1)}</strong></span>`
    : `<strong>${C(r+1,c+1)}</strong>`;
  setResult(
    `<span style="color:#60a5fa">${parts}</span> = ${tipStr}`
    + `&nbsp;&nbsp;✔&nbsp;<em>우방향 하키스틱: Σᵢ₌ᶜᵐ ᵢCᶜ = ₘ₊₁Cᶜ₊₁</em>`
  );
}

// ⑤ 하키스틱 — 좌방향: 대각선 d = r-c를 고정
// 손잡이: (d,0)~(r,c)  대각선 방향 / 끝: (r+1, c)
// Σᵢ₌₀ᶜ C(d+i, i) = C(r+1, c)
function doHockeyLeft(r, c) {
  if (c > r) return;
  const d = r - c;  // 고정 대각선 번호
  const hl = [];
  for (let i = 0; i <= c; i++) {
    hl.push({ r: d+i, c: i, fill: '#1e3a5f', stroke: '#3b82f6', textColor: '#93c5fd' });
  }
  if (r+1 < ROWS) hl.push({ r: r+1, c, fill: '#064e3b', stroke: '#10b981', textColor: '#6ee7b7' });
  highlights = hl; renderTriangle();

  const parts = Array.from({length: c+1}, (_, i) => {
    return `${d+i}C${i}(=${C(d+i,i)})`;
  }).join(' + ');
  const tipStr = r+1 < ROWS
    ? `<span style="color:#10b981"><strong>${r+1}C${c} = ${C(r+1,c)}</strong></span>`
    : `<strong>${C(r+1,c)}</strong>`;
  setResult(
    `<span style="color:#60a5fa">${parts}</span> = ${tipStr}`
    + `&nbsp;&nbsp;✔&nbsp;<em>좌방향 하키스틱: Σᵢ₌₀ᶜ ₍𝒅₊ᵢ₎Cᵢ = ₍ᵣ₊₁₎Cᶜ</em>&nbsp;(대각선 d=${d})`
  );
}

function doHockey(r, c) {
  if (hockeyDir === 'right') doHockeyRight(r, c);
  else                        doHockeyLeft(r, c);
}

// ⑥ 소수 행
function doPrime(r, c) {
  if (r < 2) {
    highlights = [{ r, c, fill:'#1e3a5f', stroke:'#3b82f6', textColor:'#93c5fd' }];
    renderTriangle();
    setResult(`<span style="color:#fbbf24">행 ${r}은 소수 성질 적용 범위 밖입니다.</span>`);
    return;
  }
  const hl = [], notDiv = [];
  for (let k = 0; k <= r; k++) {
    const v = C(r,k), isEdge = (k===0||k===r), div = (v%r===0);
    if (!isEdge && !div) notDiv.push(k);
    hl.push({ r, c:k,
      fill:      isEdge?'#292524':(div?'#1a2e1a':'#3b1515'),
      stroke:    isEdge?'#78716c':(div?'#16a34a':'#dc2626'),
      textColor: isEdge?'#a8a29e':(div?'#86efac':'#f87171'),
    });
  }
  highlights = hl; renderTriangle();

  if (isPrime(r)) {
    setResult(`<span style="color:#86efac">p = ${r} (소수): 양 끝 1을 제외한 모든 수가 ${r}의 배수입니다. ✔</span>`);
  } else if (notDiv.length > 0) {
    const ex = notDiv.slice(0,3).map(k=>`${r}C${k}=${C(r,k)}`).join(', ');
    setResult(`<span style="color:#f87171">n = ${r} (합성수): ${ex} → ${r}의 배수 아님 ✘ (소수 성질 불성립)</span>`);
  } else {
    setResult(`<span style="color:#fbbf24">n = ${r} (합성수): 이 범위에서 우연히 모두 배수처럼 보이지만 소수 성질이 보장되지는 않습니다.</span>`);
  }
}

// ── 클릭 라우터 ──
function handleCellClick(r, c) {
  switch(activeTab) {
    case 1: doSymmetry(r,c); break;
    case 2: doPascal(r,c);   break;
    case 3: doBinom(r,c);    break;
    case 4: doRowSum(r,c);   break;
    case 5: doHockey(r,c);   break;
    case 6: doPrime(r,c);    break;
  }
}

// ── 탭 메타 정보 ──
const TAB_INFO = {
  1:{ title:'성질 ① 중앙 축을 기준으로 좌우대칭',
      formula:'ₙCᵣ = ₙCₙ₋ᵣ',
      hint:'셀을 클릭하면 그 셀과 대칭인 셀이 강조됩니다.' },
  2:{ title:'성질 ② 역삼각형의 숫자들 (파스칼의 법칙)',
      formula:'ₙCᵣ = ₙ₋₁Cᵣ₋₁ + ₙ₋₁Cᵣ',
      hint:'셀을 클릭하면 위의 두 부모 셀(파랑)과 합(초록)이 강조됩니다.' },
  3:{ title:'성질 ③ n번째 행 = (a+b)ⁿ의 전개식 계수',
      formula:'(a+b)ⁿ = Σ ₙCₖ aⁿ⁻ᵏ bᵏ',
      hint:'셀을 클릭하면 그 행 전체와 이항전개식이 표시됩니다.' },
  4:{ title:'성질 ④ n행의 모든 이항계수의 합 = 2ⁿ',
      formula:'Σₖ ₙCₖ = 2ⁿ',
      hint:'셀을 클릭하면 그 행의 합과 2ⁿ이 표시됩니다.' },
  5:{ title:'성질 ⑤ 하키스틱 법칙',
      formula:'우방향: ᵣCᵣ+ᵣ₊₁Cᵣ+…+ₘCᵣ = ₘ₊₁Cᵣ₊₁  |  좌방향: ₐC₀+ₐ₊₁C₁+…+ₘCᶜ = ₘ₊₁Cᶜ',
      hint:'방향 토글로 우·좌 버전을 선택 후 셀을 클릭하세요. 우방향=열 고정, 좌방향=대각선 고정.' },
  6:{ title:'성질 ⑥ 소수 번째 행 → 그 소수의 배수만 등장',
      formula:'p가 소수 ⇒ ₚCₖ ≡ 0 (mod p)  (k ≠ 0, p)',
      hint:'셀을 클릭하면 그 행 전체에서 소수 배수 여부가 강조됩니다. 2·3·5·7행과 4·6·8행을 비교해보세요.' },
};

function switchTab(tab) {
  activeTab  = tab;
  highlights = [];
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

  const isQ = (tab === 'Q');
  ['propCard','viewToggle','triWrap','result'].forEach(id => {
    document.getElementById(id).style.display = isQ ? 'none' : '';
  });
  document.getElementById('quizPanel').style.display = isQ ? '' : 'none';

  document.getElementById('hockeyToggle').style.display = (!isQ && tab === 5) ? '' : 'none';

  if (!isQ) {
    const info = TAB_INFO[tab];
    document.getElementById('propTitle').textContent   = info.title;
    document.getElementById('propFormula').textContent = info.formula;
    document.getElementById('propHint').textContent    = info.hint;
    clearResult();
    renderTriangle();
  }
}

// ── 뷰 토글 ──
document.getElementById('btnNum').addEventListener('click', () => {
  viewMode = 'num';
  document.getElementById('btnNum').classList.add('active');
  document.getElementById('btnComb').classList.remove('active');
  renderTriangle();
});
document.getElementById('btnComb').addEventListener('click', () => {
  viewMode = 'comb';
  document.getElementById('btnComb').classList.add('active');
  document.getElementById('btnNum').classList.remove('active');
  renderTriangle();
});

// ── 하키스틱 방향 토글 ──
document.getElementById('btnHockeyR').addEventListener('click', () => {
  hockeyDir = 'right';
  document.getElementById('btnHockeyR').classList.add('active');
  document.getElementById('btnHockeyL').classList.remove('active');
  highlights = []; clearResult(); renderTriangle();
});
document.getElementById('btnHockeyL').addEventListener('click', () => {
  hockeyDir = 'left';
  document.getElementById('btnHockeyL').classList.add('active');
  document.getElementById('btnHockeyR').classList.remove('active');
  highlights = []; clearResult(); renderTriangle();
});

// ── 탭 클릭 ──
document.getElementById('tabBar').addEventListener('click', e => {
  const btn = e.target.closest('.tab-btn');
  if (!btn) return;
  const t = btn.dataset.tab;
  switchTab(t === 'Q' ? 'Q' : +t);
});

// ── 퀴즈 ──
const QUIZ = [
  { q:'ₙCᵣ = ₙCₙ₋ᵣ 가 성립하는 근본적인 이유는?',
    choices:['r개를 선택하는 것은 (n−r)개를 제외하는 것과 같기 때문',
             '두 값이 우연히 같을 뿐이다',
             '이항정리에 의해 짝수 행만 대칭이다',
             '하키스틱 법칙 때문이다'],
    answer:0, explain:'r개를 뽑는 것 = (n−r)개를 남겨두는 것이므로 경우의 수가 같습니다.' },
  { q:'7번째 행(n=7)의 모든 수의 합은?',
    choices:['64','128','256','32'],
    answer:1, explain:'행 n의 합 = 2ⁿ이므로 2⁷ = 128' },
  { q:'역삼각형 성질에 따르면, ₅C₃ = ?',
    choices:['₄C₂ + ₄C₃','₄C₂ + ₄C₄','₄C₃ + ₄C₄','₅C₂ + ₅C₄'],
    answer:0, explain:'ₙCᵣ = ₙ₋₁Cᵣ₋₁ + ₙ₋₁Cᵣ → ₅C₃ = ₄C₂ + ₄C₃ = 6+4 = 10 ✓' },
  { q:'(a+b)⁵의 전개식에서 a²b³의 계수는?',
    choices:['5','10','15','20'],
    answer:1, explain:'₅C₃ = 10 (b를 3번, a를 2번 선택하는 경우의 수)' },
  { q:'하키스틱 법칙: ₂C₂ + ₃C₂ + ₄C₂ + ₅C₂ = ?',
    choices:['₅C₃','₆C₃','₆C₂','₅C₂'],
    answer:1, explain:'r=2, m=5이면 2C2+3C2+4C2+5C2 = 6C3 = 20 ✓' },
  { q:'p=7(소수)일 때, ₇C₃의 값은 7의 배수인가?',
    choices:['예, 35 = 5×7이므로 7의 배수',
             '아니오, 35는 7의 배수가 아님',
             '양 끝만 소수의 배수',
             '알 수 없음'],
    answer:0, explain:'₇C₃ = 35 = 5×7. 소수 p에서 양 끝(1) 제외 모두 p의 배수 ✓' },
  { q:'n=5 행의 수를 전부 나열하면?',
    choices:['1 4 6 4 1','1 5 10 10 5 1','1 5 10 5 1','1 6 15 20 15 6 1'],
    answer:1, explain:'5C0=1, 5C1=5, 5C2=10, 5C3=10, 5C4=5, 5C5=1' },
];

const quizScores = new Array(QUIZ.length).fill(null);

function buildQuiz() {
  const area = document.getElementById('quizArea');
  area.innerHTML = '';
  QUIZ.forEach((q, qi) => {
    const card = document.createElement('div');
    card.className = 'q-card'; card.id = `qcard-${qi}`;
    card.innerHTML = `<div class="q-num">문제 ${qi+1} / ${QUIZ.length}</div>
      <div class="q-text">${q.q}</div>
      <div class="q-choices" id="qch-${qi}"></div>
      <div class="q-fb" id="qfb-${qi}" style="display:none"></div>`;
    q.choices.forEach((ch, ci) => {
      const btn = document.createElement('button');
      btn.className = 'q-choice';
      btn.textContent = `${'①②③④'[ci]} ${ch}`;
      btn.addEventListener('click', () => onChoice(qi, ci));
      card.querySelector(`#qch-${qi}`).appendChild(btn);
    });
    area.appendChild(card);
  });
  const sb = document.createElement('div');
  sb.className = 'score-box'; sb.id = 'scoreBox';
  sb.innerHTML = `<div class="score-big" id="scoreBig">-</div>
    <div class="score-msg" id="scoreMsg">문제를 풀어보세요!</div>`;
  area.appendChild(sb);
}

function onChoice(qi, ci) {
  if (quizScores[qi] !== null) return;
  const ok = ci === QUIZ[qi].answer;
  quizScores[qi] = ok;
  const card = document.getElementById(`qcard-${qi}`);
  card.classList.add(ok ? 'correct' : 'wrong');
  card.querySelectorAll('.q-choice').forEach((b, i) => {
    b.disabled = true;
    if (i === QUIZ[qi].answer) b.classList.add('show-ans');
    else if (i === ci && !ok) b.classList.add('sel-wrong');
  });
  const fb = document.getElementById(`qfb-${qi}`);
  fb.style.display = 'block';
  fb.className = `q-fb ${ok?'correct':'wrong'}`;
  fb.textContent = (ok?'✔ 정답! ':'✘ 오답. ') + QUIZ[qi].explain;
  updateScore();
}

function updateScore() {
  const answered = quizScores.filter(s=>s!==null).length;
  const correct  = quizScores.filter(s=>s===true).length;
  document.getElementById('scoreBig').textContent = `${correct} / ${answered}`;
  const msg = answered < QUIZ.length
    ? `${answered}문제 완료 (${QUIZ.length-answered}문제 남음)`
    : `정답률 ${Math.round(correct/QUIZ.length*100)}% — ${
        correct===QUIZ.length?'🎉 완벽!':
        correct>=Math.ceil(QUIZ.length*.7)?'👏 잘했어요!':'📚 탭으로 돌아가 다시 탐구해봐요.'}`;
  document.getElementById('scoreMsg').textContent = msg;
  if (answered===QUIZ.length && !document.getElementById('reBtn')) {
    const btn = document.createElement('button');
    btn.className='re-btn'; btn.id='reBtn'; btn.textContent='다시 풀기';
    btn.addEventListener('click', ()=>{ quizScores.fill(null); buildQuiz(); });
    document.getElementById('scoreBox').appendChild(btn);
  }
}

// ── 초기화 ──
buildQuiz();
switchTab(1);

})();
</script>
</body>
</html>
"""


def render():
    st.header("🔺 파스칼의 삼각형 성질 탐구")
    st.caption("이항계수의 6가지 성질을 직접 셀을 클릭하며 탐구하고, 퀴즈로 확인합니다.")
    components.html(HTML, height=1000, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
