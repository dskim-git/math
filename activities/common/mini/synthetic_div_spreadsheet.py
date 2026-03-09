# activities/common/mini/synthetic_div_spreadsheet.py
"""
스프레드시트로 조립제법 구현하기
수업 이미지(3번째)처럼 엑셀 셀 수식 구조를 직접 따라가며 조립제법을 체험
"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests

# ── Google Sheets 연동 (공통수학1 전용) ─────────────────────────────────────
_GAS_URL    = "https://script.google.com/macros/s/AKfycbySLDnSYGfQmqrtpuMyIju5hiEf7Lesp6bnWzplm3oZD4WHXESl1XJmsXT_EVcKOJI/exec"
_SHEET_NAME = "조립제법스프레드시트"

META = {
    "title":       "📊 스프레드시트로 조립제법 구현",
    "description": "엑셀 스프레드시트의 셀 수식을 따라가며 조립제법을 직접 구현해 보는 활동",
    "order":       36,
    "hidden":      True,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>스프레드시트로 조립제법</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#e2e8f0;
     padding:14px 10px;min-height:600px;}

/* ── Tabs ── */
.tabs{display:flex;gap:6px;margin-bottom:18px;flex-wrap:wrap}
.tab-btn{padding:9px 20px;border-radius:10px;border:2px solid #1e293b;
         background:#141c2b;color:#7a8ea8;cursor:pointer;font-size:13.5px;
         font-weight:700;transition:all .2s}
.tab-btn.active{background:#14532d;border-color:#16a34a;color:#4ade80}
.tab-panel{display:none}.tab-panel.active{display:block}

/* ── Cards ── */
.card{background:#161e2e;border:1px solid #1e293b;border-radius:14px;
      padding:18px 20px;margin-bottom:14px}
.card-title{font-size:15px;font-weight:800;color:#4ade80;margin-bottom:12px;
            display:flex;align-items:center;gap:7px}
p,.note{font-size:13px;line-height:1.9;color:#c0cce0}
.note{color:#94a3b8}
strong{color:#e2e8f0}
ul{padding-left:18px;margin:6px 0}
ul li{font-size:13px;line-height:1.9;color:#c0cce0}

/* ── Instruction steps ── */
.instr-list{display:flex;flex-direction:column;gap:8px;margin:10px 0}
.instr-item{display:flex;gap:10px;align-items:flex-start;padding:10px 14px;
            background:#0d1b2e;border:1px solid #1e293b;border-radius:10px}
.instr-num{min-width:28px;height:28px;border-radius:50%;background:#14532d;
           color:#4ade80;font-size:12px;font-weight:800;
           display:flex;align-items:center;justify-content:center;flex-shrink:0}
.instr-text{font-size:12.5px;color:#c0cce0;line-height:1.8}
.instr-formula{font-family:'Courier New',monospace;background:#0b2010;
               color:#a7f3d0;padding:2px 8px;border-radius:5px;font-size:12.5px}

/* ── Spreadsheet Grid ── */
.sheet-wrap{overflow-x:auto;margin:4px 0 10px}
.sheet-grid{border-collapse:collapse;font-size:13.5px}
.sheet-grid .col-header{background:#0f2340;color:#7dd3fc;font-weight:700;
                        padding:6px 14px;border:1px solid #1e3a5f;text-align:center;
                        min-width:90px}
.sheet-grid .row-header{background:#0f2340;color:#7dd3fc;font-weight:700;
                        padding:6px 10px;border:1px solid #1e3a5f;text-align:center;
                        min-width:32px}

td.cell{border:1px solid #1e3a5f;min-width:90px;height:42px;
        text-align:center;vertical-align:middle;background:#0b1629}
td.cell.given{background:#0d2040;color:#7dd3fc;font-weight:700;font-size:14px}
td.cell.given-alpha{background:#1c1505;color:#fbbf24;font-weight:800;font-size:15px}

/* ── Formula Input Cells (top table) ── */
td.cell.formula-cell{background:#0a1a14;border:1.5px dashed #1a4030 !important;
                     min-width:110px}
td.cell.formula-cell:focus-within{border:2px solid #22c55e !important;
                                   background:#041510 !important}
.formula-input{width:100%;height:100%;min-height:40px;border:none;
               background:transparent;text-align:center;color:#86efac;
               font-size:12.5px;font-weight:700;font-family:'Courier New',monospace;
               outline:none;padding:6px 4px}
.formula-input::placeholder{color:#1e3a2a;font-style:italic;font-size:11px}
.formula-input.has-val{color:#86efac}
.formula-input.bad-val{color:#fca5a5}

/* ── Preview Cells (bottom table) ── */
td.cell.prev-empty{background:#0b1629;color:#273547;font-size:16px;font-weight:700}
td.cell.prev-correct{background:#052e16;color:#4ade80;font-weight:800;font-size:16px;
                     animation:prevFlash .4s ease}
td.cell.prev-wrong{background:#2d0a0a;color:#f87171;font-weight:800;font-size:16px}
@keyframes prevFlash{from{background:#0a5530}to{background:#052e16}}

/* ── Section labels ── */
.section-label{display:inline-block;font-size:12px;font-weight:700;
               padding:5px 12px;border-radius:7px;margin-bottom:6px}
.lbl-input{background:#041a10;color:#86efac;border:1px solid #14532d}
.lbl-output{background:#091223;color:#7dd3fc;border:1px solid #1e3a5f}

/* ── Formula bar ── */
.formula-bar{display:flex;align-items:center;gap:8px;background:#0f2340;
             border:1px solid #1e3a5f;border-radius:8px;padding:8px 14px;
             margin-bottom:10px;font-size:13px}
.formula-bar .cell-addr{color:#fbbf24;font-weight:800;min-width:28px;
                        font-family:monospace;font-size:14px}
.formula-bar .formula-text{color:#a7f3d0;font-family:'Courier New',monospace;flex:1;
                            font-size:12.5px}

/* ── Problem selector ── */
.problem-selector{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.prob-btn{padding:7px 16px;border-radius:8px;border:2px solid #1e3a5f;
          background:#141c2b;color:#7a8ea8;cursor:pointer;font-size:12.5px;
          font-weight:700;transition:all .2s}
.prob-btn.active{background:#14532d;border-color:#16a34a;color:#4ade80}

/* ── Action buttons ── */
.action-btns{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
.btn{padding:9px 22px;border:none;border-radius:8px;font-size:13px;
     font-weight:700;cursor:pointer;transition:.2s}
.btn-check{background:#16a34a;color:#fff}.btn-check:hover{background:#15803d}
.btn-hint{background:#0369a1;color:#fff}.btn-hint:hover{background:#0284c7}
.btn-reset{background:#1e293b;color:#94a3b8}.btn-reset:hover{background:#263547}
.btn-solve{background:#6b21a8;color:#fff}.btn-solve:hover{background:#7c3aed}

/* ── Feedback ── */
.feedback-area{margin-top:10px;min-height:24px;font-size:13px;font-weight:700}
.feedback-area.ok{color:#4ade80}.feedback-area.ng{color:#f87171}
.feedback-area.hint{color:#7dd3fc}

/* ── Result panel ── */
.result-panel{display:none;margin-top:14px;padding:16px;
              background:#052e16;border:1px solid #16a34a;border-radius:12px}
.result-panel h4{color:#4ade80;font-size:14px;font-weight:700;margin-bottom:8px}
.result-panel p{font-size:13px;line-height:1.8;color:#c0cce0}
.result-poly{font-size:16px;font-weight:800;color:#4ade80;margin:8px 0}

/* ── Progress ── */
.progress-wrap{display:flex;align-items:center;gap:8px;margin-bottom:12px}
.progress-track{flex:1;height:7px;background:#1e293b;border-radius:99px;overflow:hidden}
.prog-bar{height:100%;background:linear-gradient(90deg,#16a34a,#0d9488);
          transition:width .4s;border-radius:99px}
.score-badge{background:#14532d;color:#4ade80;border-radius:99px;
             padding:3px 12px;font-size:12px;font-weight:700}

/* ── Legend ── */
.legend{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 10px}
.legend-item{display:flex;align-items:center;gap:5px;font-size:11.5px;color:#94a3b8}
.legend-dot{width:12px;height:12px;border-radius:3px;flex-shrink:0}
.legend-dot.la{background:#1c1505;border:1px solid #fbbf24}
.legend-dot.lc{background:#0d2040;border:1px solid #7dd3fc}
.legend-dot.li{background:#0a1a14;border:1.5px dashed #1a4030}
.legend-dot.lo{background:#052e16;border:1px solid #16a34a}
</style>
</head>
<body>

<!-- Header -->
<div style="text-align:center;margin-bottom:16px">
  <div style="font-size:1.35rem;font-weight:800;color:#4ade80;margin-bottom:4px">
    📊 스프레드시트로 조립제법 구현
  </div>
  <div style="font-size:12.5px;color:#64748b">
    엑셀/구글 시트의 셀 수식 구조를 따라 조립제법을 직접 구현해 보세요
  </div>
</div>

<!-- Progress -->
<div class="progress-wrap">
  <div class="progress-track"><div class="prog-bar" id="progressBar" style="width:0%"></div></div>
  <div class="score-badge">해결 <span id="progressTxt">0/4</span></div>
</div>

<!-- Tabs -->
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('guide', this)">📋 구현 방법 설명</button>
  <button class="tab-btn" onclick="switchTab('practice', this)">🧮 직접 구현해보기</button>
</div>

<!-- ══════════════════ TAB: 설명 ══════════════════ -->
<div id="tab-guide" class="tab-panel active">
  <div class="card">
    <div class="card-title">📋 스프레드시트로 조립제법 구현하는 방법</div>
    <p>
      <strong>3x³ − 2x² + x − 4</strong>를 <strong>x − 2</strong>로 나눌 때
      스프레드시트(엑셀 또는 구글 시트)에서 다음과 같이 구현할 수 있습니다.
    </p>
  </div>

  <div class="card">
    <div class="card-title">① 셀 입력 규칙</div>
    <div class="instr-list">
      <div class="instr-item">
        <div class="instr-num">1</div>
        <div class="instr-text">
          셀 <strong>A1</strong>에 <strong>α (나누는 수)</strong> 를 입력합니다.
          <br>예시: A1 = <span class="instr-formula">2</span>
        </div>
      </div>
      <div class="instr-item">
        <div class="instr-num">2</div>
        <div class="instr-text">
          셀 <strong>B1, C1, D1, E1, ...</strong>에 다항식의
          <strong>최고차항부터 차례로 계수</strong>를 입력합니다.
          <br>예시: B1 = <span class="instr-formula">3</span>,
          C1 = <span class="instr-formula">-2</span>,
          D1 = <span class="instr-formula">1</span>,
          E1 = <span class="instr-formula">-4</span>
        </div>
      </div>
      <div class="instr-item">
        <div class="instr-num">3</div>
        <div class="instr-text">
          셀 <strong>B3</strong>에 <span class="instr-formula">=B1</span>을 입력합니다.
          <br>→ 맨 앞 계수를 그대로 내려씁니다 (b_{n-1} = a_n)
        </div>
      </div>
      <div class="instr-item">
        <div class="instr-num">4</div>
        <div class="instr-text">
          셀 <strong>C2</strong>: <span class="instr-formula">=A1*B3</span>
          &nbsp;(α × 앞 계수)<br>
          셀 <strong>C3</strong>: <span class="instr-formula">=C1+C2</span>
          &nbsp;(1행 + 2행)<br>
          셀 <strong>D2</strong>: <span class="instr-formula">=A1*C3</span><br>
          셀 <strong>D3</strong>: <span class="instr-formula">=D1+D2</span><br>
          셀 <strong>E2</strong>: <span class="instr-formula">=A1*D3</span><br>
          셀 <strong>E3</strong>: <span class="instr-formula">=E1+E2</span>
          &nbsp;← 마지막: <strong>나머지 R</strong>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">② 완성된 표 예시</div>
    <p style="margin-bottom:12px">
      위 규칙대로 입력하면 아래와 같은 표가 만들어집니다:
    </p>
    <div class="sheet-wrap">
      <table class="sheet-grid">
        <thead>
          <tr>
            <th class="col-header"></th>
            <th class="col-header">A</th>
            <th class="col-header">B</th>
            <th class="col-header">C</th>
            <th class="col-header">D</th>
            <th class="col-header">E</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="row-header">1</td>
            <td class="cell given-alpha">2</td>
            <td class="cell given">3</td>
            <td class="cell given" style="color:#f87171">−2</td>
            <td class="cell given">1</td>
            <td class="cell given" style="color:#f87171">−4</td>
          </tr>
          <tr>
            <td class="row-header">2</td>
            <td class="cell"></td>
            <td class="cell"></td>
            <td class="cell given" style="color:#60a5fa;font-size:12px">=A1×B3<br><strong style="font-size:14px">6</strong></td>
            <td class="cell given" style="color:#60a5fa;font-size:12px">=A1×C3<br><strong style="font-size:14px">8</strong></td>
            <td class="cell given" style="color:#60a5fa;font-size:12px">=A1×D3<br><strong style="font-size:14px">18</strong></td>
          </tr>
          <tr>
            <td class="row-header">3</td>
            <td class="cell"></td>
            <td class="cell given" style="color:#4ade80;font-size:12px">=B1<br><strong style="font-size:14px">3</strong></td>
            <td class="cell given" style="color:#4ade80;font-size:12px">=C1+C2<br><strong style="font-size:14px">4</strong></td>
            <td class="cell given" style="color:#4ade80;font-size:12px">=D1+D2<br><strong style="font-size:14px">9</strong></td>
            <td class="cell given" style="border-left:3px solid #f87171;color:#f87171;font-size:12px">=E1+E2<br><strong style="font-size:14px">14</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
    <p style="margin-top:10px">
      ✅ <strong>3행의 마지막 칸 E3 = 14</strong>이 <strong>나머지 R</strong>,
      나머지 앞 칸들 B3, C3, D3 = 3, 4, 9가 <strong>몫 Q(x) = 3x² + 4x + 9</strong>의 계수입니다.
    </p>
  </div>

  <div class="card">
    <div class="card-title">③ 수식 패턴 정리</div>
    <p>계수의 수가 <strong>n+1개</strong>인 n차 다항식을 x−α로 나눌 때:</p>
    <ul style="margin-top:8px">
      <li>A1 = α</li>
      <li>B1 ~ (n+2)1 = 계수 a_n, ..., a_0</li>
      <li><strong>3행 첫 번째</strong>: =B1 (그대로 내려쓰기)</li>
      <li><strong>2행 k번째</strong> (k≥2): =A1 × (k−1번째 3행 값)</li>
      <li><strong>3행 k번째</strong> (k≥2): =k번째 1행 + k번째 2행</li>
    </ul>
  </div>
</div><!-- /tab-guide -->

<!-- ══════════════════ TAB: 실습 ══════════════════ -->
<div id="tab-practice" class="tab-panel">

  <div style="background:#091223;border:1px solid #1e3a5f;border-radius:10px;
              padding:12px 16px;margin-bottom:14px;font-size:13px;line-height:2;color:#c0cce0">
    📝 <strong style="color:#86efac">위 표 (수식 입력)</strong>의 초록 빈 칸에
    엑셀 수식을 직접 입력하세요.
    (예: <span style="font-family:monospace;color:#a7f3d0">=B1</span>&nbsp;
         <span style="font-family:monospace;color:#a7f3d0">=A1*B3</span>&nbsp;
         <span style="font-family:monospace;color:#a7f3d0">=C1+C2</span>)<br>
    📊 <strong style="color:#7dd3fc">아래 표 (계산 결과)</strong>에는
    입력한 수식의 계산 결과값이 자동으로 표시됩니다.
  </div>

  <!-- Problem selector -->
  <div class="problem-selector" id="probSelector"></div>

  <!-- Legend -->
  <div class="legend">
    <div class="legend-item"><div class="legend-dot la"></div> α (주어짐)</div>
    <div class="legend-item"><div class="legend-dot lc"></div> 계수 (주어짐)</div>
    <div class="legend-item"><div class="legend-dot li"></div> 수식 입력 칸</div>
    <div class="legend-item"><div class="legend-dot lo"></div> 올바른 계산 결과</div>
  </div>

  <!-- Formula bar -->
  <div class="formula-bar">
    <span class="cell-addr" id="formulaCellAddr">—</span>
    <span style="color:#475569;font-size:12px;flex-shrink:0">힌트:</span>
    <span class="formula-text" id="formulaText">셀을 클릭하면 해당 칸의 수식 힌트가 표시됩니다</span>
  </div>

  <!-- TOP: Formula input table -->
  <div class="section-label lbl-input">📝 수식 입력 표 — 엑셀 수식으로 채워보세요</div>
  <div class="sheet-wrap"><table class="sheet-grid" id="formulaTable"></table></div>

  <!-- BOTTOM: Preview table -->
  <div class="section-label lbl-output" style="margin-top:12px">
    📊 계산 결과 표 — 수식 입력 즉시 자동 업데이트
  </div>
  <div class="sheet-wrap"><table class="sheet-grid" id="previewTable"></table></div>

  <!-- Buttons -->
  <div class="action-btns">
    <button class="btn btn-check" onclick="checkAll()">✅ 채점하기</button>
    <button class="btn btn-hint" onclick="showOneHint()">💡 힌트 (한 칸)</button>
    <button class="btn btn-solve" onclick="solveAll()">🔮 정답 보기</button>
    <button class="btn btn-reset" onclick="resetGrid()">↩ 초기화</button>
  </div>

  <div class="feedback-area" id="feedbackArea"></div>

  <div class="result-panel" id="resultPanel">
    <h4>🎉 완성!</h4>
    <p id="resultText"></p>
    <div class="result-poly" id="resultPoly"></div>
  </div>

</div><!-- /tab-practice -->

<script>
// ━━━━━━━━━━━━━━━━━━ TAB ━━━━━━━━━━━━━━━━━━
function switchTab(id, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  btn.classList.add('active');
}

// ━━━━━━━━━━━━━━━━━━ DATA ━━━━━━━━━━━━━━━━━━
const PROBS = [
  { label:'문제①', alpha:2,  coeffs:[3,-2,1,-4],    poly:'3x³ − 2x² + x − 4',    divisor:'x − 2' },
  { label:'문제②', alpha:-1, coeffs:[2,1,-3],        poly:'2x² + x − 3',           divisor:'x + 1' },
  { label:'문제③', alpha:2,  coeffs:[1,0,0,-8],      poly:'x³ − 8',                divisor:'x − 2' },
  { label:'문제④', alpha:1,  coeffs:[2,-3,0,4,-1],   poly:'2x⁴ − 3x³ + 4x − 1',   divisor:'x − 1' },
];
const colLetters = ['A','B','C','D','E','F','G'];
let curProb = 0;
const solvedSet = new Set();

// ━━━━━━━━━━━━━━━━━━ CELL DATA STORE ━━━━━━━━━━━━━━━━━━
let cellData = {};  // cellData[row][colIdx] = number | null
let formulaInfo = {};  // formulaInfo["row-col"] = { formula, desc }

function setCellValue(row, col, val) {
  if (!cellData[row]) cellData[row] = {};
  cellData[row][col] = val;
}
function getCellValue(row, col) {
  if (!cellData[row]) return null;
  const v = cellData[row][col];
  return (v !== undefined) ? v : null;
}
function initCellData(p) {
  cellData = {};
  setCellValue(1, 0, p.alpha);
  p.coeffs.forEach((c, i) => setCellValue(1, i + 1, c));
}

// ━━━━━━━━━━━━━━━━━━ SYNTHETIC DIVISION ━━━━━━━━━━━━━━━━━━
function synDiv(coeffs, alpha) {
  const n = coeffs.length;
  const r2 = new Array(n).fill(null);
  const r3 = new Array(n).fill(null);
  r3[0] = coeffs[0];
  for (let i = 1; i < n; i++) {
    r2[i] = alpha * r3[i - 1];
    r3[i] = coeffs[i] + r2[i];
  }
  return { r2, r3 };
}

// ━━━━━━━━━━━━━━━━━━ FORMULA EVALUATOR ━━━━━━━━━━━━━━━━━━
// Safely evaluates Excel-style formulas like =A1*B3, =C1+C2, =B1
function evalFormula(formula) {
  if (!formula || formula.trim() === '') return null;
  const f = formula.trim();
  if (!f.startsWith('=')) {
    const n = Number(f);
    return isNaN(n) ? null : n;
  }
  const expr = f.slice(1).trim();
  // Whitelist: only letters, digits, +, -, *, spaces, ()
  if (!/^[A-Za-z0-9+\-*\s()]+$/.test(expr)) return null;
  // Replace cell references (single letter + row number 1-3)
  let resolved = expr.replace(/([A-Za-z])([1-3])\b/gi, (m, col, rowStr) => {
    const colIdx = col.toUpperCase().charCodeAt(0) - 65;
    const row = parseInt(rowStr);
    if (colIdx < 0 || colIdx > 6) return '__MISS__';
    const val = getCellValue(row, colIdx);
    if (val === null || val === undefined) return '__MISS__';
    return '(' + val + ')';
  });
  if (resolved.includes('__MISS__')) return null;
  // After substitution only digits + operators allowed
  if (!/^[\d+\-*\s().]+$/.test(resolved)) return null;
  try {
    const r = Function('"use strict"; return (' + resolved + ')')();
    return (typeof r === 'number' && isFinite(r)) ? Math.round(r * 1e9) / 1e9 : null;
  } catch (e) { return null; }
}

// ━━━━━━━━━━━━━━━━━━ FORMULA HINT INFO ━━━━━━━━━━━━━━━━━━
function getCellFormulaInfo(row, colIdx, alpha) {
  const col = colLetters[colIdx];
  if (row === 3 && colIdx === 1) {
    return { formula: '=B1', desc: '맨 앞 계수 그대로 내려씁니다 (b_{n-1} = a_n)' };
  }
  if (row === 2 && colIdx >= 2) {
    const prev = colLetters[colIdx - 1];
    return { formula: `=A1*${prev}3`, desc: `α(=${alpha}) × ${prev}3` };
  }
  if (row === 3 && colIdx >= 2) {
    return { formula: `=${col}1+${col}2`, desc: `1행 계수 + 2행 값` };
  }
  return { formula: '', desc: '' };
}

// ━━━━━━━━━━━━━━━━━━ RECOMPUTE (dependency-order) ━━━━━━━━━━━━━━━━
// B3 → C2, C3 → D2, D3 → E2, E3 ...
function recomputeAll() {
  const n = PROBS[curProb].coeffs.length;

  // B3 (colIdx=1, row=3)
  const b3 = document.querySelector('#formulaTable input[data-row="3"][data-col="1"]');
  setCellValue(3, 1, b3 ? evalFormula(b3.value) : null);

  // col 2..n: row2 then row3
  for (let col = 2; col <= n; col++) {
    const r2 = document.querySelector(`#formulaTable input[data-row="2"][data-col="${col}"]`);
    setCellValue(2, col, r2 ? evalFormula(r2.value) : null);
    const r3 = document.querySelector(`#formulaTable input[data-row="3"][data-col="${col}"]`);
    setCellValue(3, col, r3 ? evalFormula(r3.value) : null);
  }
  updatePreviewTable();
}

// ━━━━━━━━━━━━━━━━━━ PREVIEW TABLE UPDATE ━━━━━━━━━━━━━━━━
function updatePreviewTable() {
  const p = PROBS[curProb];
  const ans = synDiv(p.coeffs, p.alpha);
  const n = p.coeffs.length;

  setPrev('prev-3-1', getCellValue(3, 1), ans.r3[0]);
  for (let col = 2; col <= n; col++) {
    setPrev(`prev-2-${col}`, getCellValue(2, col), ans.r2[col - 1]);
    setPrev(`prev-3-${col}`, getCellValue(3, col), ans.r3[col - 1]);
  }
}
function setPrev(id, val, expected) {
  const c = document.getElementById(id);
  if (!c) return;
  if (val === null || val === undefined) {
    c.textContent = '?'; c.className = 'cell prev-empty'; return;
  }
  c.textContent = val < 0 ? '−' + Math.abs(val) : String(val);
  c.className = Math.abs(val - expected) < 0.0001 ? 'cell prev-correct' : 'cell prev-wrong';
}

// ━━━━━━━━━━━━━━━━━━ TABLE BUILDERS ━━━━━━━━━━━━━━━━━━
function colHdr(n) {
  let h = '<thead><tr><th class="col-header"></th>';
  for (let c = 0; c <= n; c++) h += `<th class="col-header">${colLetters[c]}</th>`;
  return h + '</tr></thead>';
}
function fmtN(n) { return n < 0 ? '−' + Math.abs(n) : String(n); }

function buildFormulaTable(p) {
  formulaInfo = {};
  const n = p.coeffs.length;
  let html = colHdr(n) + '<tbody>';

  // Row 1: given
  html += '<tr><td class="row-header">1</td>';
  html += `<td class="cell given-alpha">${fmtN(p.alpha)}</td>`;
  for (let c = 1; c <= n; c++) html += `<td class="cell given">${fmtN(p.coeffs[c-1])}</td>`;
  html += '</tr>';

  // Row 2: formula inputs (A2, B2 empty; C2..end are inputs)
  html += '<tr><td class="row-header">2</td>';
  html += '<td class="cell"></td><td class="cell"></td>';
  for (let c = 2; c <= n; c++) {
    const fi = getCellFormulaInfo(2, c, p.alpha);
    formulaInfo[`2-${c}`] = fi;
    html += `<td class="cell formula-cell"><input class="formula-input" type="text"
      placeholder="${fi.formula}" data-row="2" data-col="${c}"
      onfocus="onFocus(2,${c})" oninput="recomputeAll()"></td>`;
  }
  html += '</tr>';

  // Row 3: formula inputs (A3 empty; B3..end are inputs)
  html += '<tr><td class="row-header">3</td><td class="cell"></td>';
  for (let c = 1; c <= n; c++) {
    const fi = getCellFormulaInfo(3, c, p.alpha);
    formulaInfo[`3-${c}`] = fi;
    const bdr = (c === n) ? 'border-left:3px solid #ef4444;' : '';
    html += `<td class="cell formula-cell" style="${bdr}"><input class="formula-input" type="text"
      placeholder="${fi.formula}" data-row="3" data-col="${c}"
      onfocus="onFocus(3,${c})" oninput="recomputeAll()"></td>`;
  }
  html += '</tr></tbody>';
  document.getElementById('formulaTable').innerHTML = html;
}

function buildPreviewTable(p) {
  const n = p.coeffs.length;
  let html = colHdr(n) + '<tbody>';

  // Row 1: same given values
  html += '<tr><td class="row-header">1</td>';
  html += `<td class="cell given-alpha">${fmtN(p.alpha)}</td>`;
  for (let c = 1; c <= n; c++) html += `<td class="cell given">${fmtN(p.coeffs[c-1])}</td>`;
  html += '</tr>';

  // Row 2
  html += '<tr><td class="row-header">2</td>';
  html += '<td class="cell"></td><td class="cell"></td>';
  for (let c = 2; c <= n; c++) html += `<td class="cell prev-empty" id="prev-2-${c}">?</td>`;
  html += '</tr>';

  // Row 3
  html += '<tr><td class="row-header">3</td><td class="cell"></td>';
  html += `<td class="cell prev-empty" id="prev-3-1">?</td>`;
  for (let c = 2; c <= n; c++) {
    const bdr = (c === n) ? 'border-left:3px solid #ef4444;' : '';
    html += `<td class="cell prev-empty" id="prev-3-${c}" style="${bdr}">?</td>`;
  }
  html += '</tr></tbody>';
  document.getElementById('previewTable').innerHTML = html;
}

// ━━━━━━━━━━━━━━━━━━ PROBLEM LOADING ━━━━━━━━━━━━━━━━━━
function buildProbSelector() {
  const sel = document.getElementById('probSelector');
  sel.innerHTML = '';
  PROBS.forEach((p, i) => {
    const btn = document.createElement('button');
    btn.className = 'prob-btn' + (i === curProb ? ' active' : '');
    btn.textContent = p.label + (solvedSet.has(i) ? ' ✅' : '');
    btn.onclick = () => loadProb(i);
    sel.appendChild(btn);
  });
}

function loadProb(idx) {
  curProb = idx;
  buildProbSelector();
  const p = PROBS[idx];
  initCellData(p);
  buildFormulaTable(p);
  buildPreviewTable(p);
  document.getElementById('feedbackArea').textContent = '';
  document.getElementById('feedbackArea').className = 'feedback-area';
  document.getElementById('resultPanel').style.display = 'none';
  document.getElementById('formulaCellAddr').textContent = '—';
  document.getElementById('formulaText').textContent = '셀을 클릭하면 해당 칸의 수식 힌트가 표시됩니다';
}

// ━━━━━━━━━━━━━━━━━━ CELL FOCUS ━━━━━━━━━━━━━━━━━━
function onFocus(row, col) {
  const fi = formulaInfo[`${row}-${col}`] || { formula: '', desc: '' };
  document.getElementById('formulaCellAddr').textContent = colLetters[col] + row;
  document.getElementById('formulaText').textContent =
    (fi.formula ? fi.formula : '?') + (fi.desc ? '  →  ' + fi.desc : '');
}

// ━━━━━━━━━━━━━━━━━━ CHECK ━━━━━━━━━━━━━━━━━━
function checkAll() {
  const p = PROBS[curProb];
  const ans = synDiv(p.coeffs, p.alpha);
  const n = p.coeffs.length;
  let allOk = true;
  let noFormula = false;

  function chk(row, col, expected) {
    const inp = document.querySelector(`#formulaTable input[data-row="${row}"][data-col="${col}"]`);
    if (!inp) return;
    if (inp.value.trim() === '') { allOk = false; return; }
    if (!inp.value.trim().startsWith('=')) noFormula = true;
    const val = getCellValue(row, col);
    if (val === null || Math.abs(val - expected) >= 0.0001) allOk = false;
  }
  chk(3, 1, ans.r3[0]);
  for (let col = 2; col <= n; col++) {
    chk(2, col, ans.r2[col - 1]);
    chk(3, col, ans.r3[col - 1]);
  }

  const fb = document.getElementById('feedbackArea');
  if (allOk) {
    fb.textContent = noFormula
      ? '✅ 값은 모두 맞습니다! = 로 시작하는 수식으로 작성하면 더욱 완벽해요.'
      : '🎉 모든 수식이 올바릅니다!';
    fb.className = 'feedback-area ' + (noFormula ? 'hint' : 'ok');
    solvedSet.add(curProb);
    buildProbSelector();
    showResult();
    updateProgress();
  } else {
    fb.textContent = '❌ 맞지 않는 칸이 있습니다. 아래 표의 빨간 셀을 확인하고 수식을 수정해보세요.';
    fb.className = 'feedback-area ng';
  }
}

// ━━━━━━━━━━━━━━━━━━ HINT ━━━━━━━━━━━━━━━━━━
function showOneHint() {
  const p = PROBS[curProb];
  const ans = synDiv(p.coeffs, p.alpha);
  const n = p.coeffs.length;

  function tryHint(row, col, expected) {
    const inp = document.querySelector(`#formulaTable input[data-row="${row}"][data-col="${col}"]`);
    if (!inp) return false;
    const val = getCellValue(row, col);
    if (inp.value.trim() !== '' && val !== null && Math.abs(val - expected) < 0.0001) return false;
    const fi = getCellFormulaInfo(row, col, p.alpha);
    inp.value = fi.formula;
    recomputeAll();
    const fb = document.getElementById('feedbackArea');
    fb.textContent = `💡 ${colLetters[col]}${row} 에 수식 ${fi.formula} 를 입력했습니다.`;
    fb.className = 'feedback-area hint';
    return true;
  }

  if (tryHint(3, 1, ans.r3[0])) return;
  for (let col = 2; col <= n; col++) {
    if (tryHint(2, col, ans.r2[col - 1])) return;
    if (tryHint(3, col, ans.r3[col - 1])) return;
  }
  document.getElementById('feedbackArea').textContent = '✅ 이미 모두 완성되었습니다!';
}

// ━━━━━━━━━━━━━━━━━━ SOLVE ALL ━━━━━━━━━━━━━━━━━━
function solveAll() {
  const p = PROBS[curProb];
  const n = p.coeffs.length;
  const fill = (row, col) => {
    const inp = document.querySelector(`#formulaTable input[data-row="${row}"][data-col="${col}"]`);
    if (inp) inp.value = getCellFormulaInfo(row, col, p.alpha).formula;
  };
  fill(3, 1);
  for (let col = 2; col <= n; col++) { fill(2, col); fill(3, col); }
  recomputeAll();
  solvedSet.add(curProb);
  buildProbSelector();
  showResult();
  updateProgress();
  const fb = document.getElementById('feedbackArea');
  fb.textContent = '🔮 정답 수식을 모두 표시했습니다.';
  fb.className = 'feedback-area hint';
}

// ━━━━━━━━━━━━━━━━━━ RESET ━━━━━━━━━━━━━━━━━━
function resetGrid() {
  document.querySelectorAll('#formulaTable .formula-input').forEach(i => { i.value = ''; });
  initCellData(PROBS[curProb]);
  updatePreviewTable();
  document.getElementById('feedbackArea').textContent = '';
  document.getElementById('resultPanel').style.display = 'none';
  document.getElementById('formulaCellAddr').textContent = '—';
  document.getElementById('formulaText').textContent = '셀을 클릭하면 해당 칸의 수식 힌트가 표시됩니다';
}

// ━━━━━━━━━━━━━━━━━━ RESULT ━━━━━━━━━━━━━━━━━━
function showResult() {
  const p = PROBS[curProb];
  const res = synDiv(p.coeffs, p.alpha);
  const n = p.coeffs.length;
  const R = res.r3[n - 1];
  let terms = [];
  for (let i = 0; i < n - 1; i++) {
    const coef = res.r3[i];
    const exp = n - 2 - i;
    if (coef === 0) continue;
    const abs = Math.abs(coef);
    const sign = coef < 0 ? '−' : (terms.length > 0 ? '+' : '');
    let t;
    if (exp === 0) t = sign + abs;
    else if (exp === 1) t = sign + (abs === 1 ? '' : abs) + 'x';
    else t = sign + (abs === 1 ? '' : abs) + 'x' + toSup(exp);
    terms.push(t);
  }
  const qStr = terms.join(' ') || '0';
  document.getElementById('resultText').innerHTML =
    `<strong>${p.poly}</strong> ÷ <strong>(${p.divisor})</strong>`;
  document.getElementById('resultPoly').textContent =
    '몫: Q(x) = ' + qStr + '  |  나머지: R = ' + (R < 0 ? '−' + Math.abs(R) : R);
  document.getElementById('resultPanel').style.display = 'block';
}

function toSup(n) {
  return String(n).split('').map(d => ['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹'][+d]).join('');
}
function updateProgress() {
  const cnt = solvedSet.size;
  document.getElementById('progressBar').style.width = (cnt / PROBS.length * 100) + '%';
  document.getElementById('progressTxt').textContent = cnt + '/' + PROBS.length;
}

// ─── INIT ───
buildProbSelector();
loadProb(0);
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────

def render():
    st.header("📊 스프레드시트로 조립제법 구현하기")
    st.caption(
        "엑셀/구글 시트에서 **셀 수식**을 이용해 조립제법을 구현하는 방법을 익히고, "
        "직접 스프레드시트 표를 완성해 보세요."
    )
    components.html(_HTML, height=1150, scrolling=True)
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_reflection_form(sheet_name: str, gas_url: str):
    st.divider()
    st.subheader("✍️ 활동 후 성찰 기록")
    st.caption("아래 질문에 답하고 **제출하기** 버튼을 눌러주세요.")

    with st.form(f"reflection_{sheet_name}", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            student_id = st.text_input("학번")
        with c2:
            name = st.text_input("이름")

        st.markdown("**📝 스프레드시트(엑셀)로 조립제법을 구현하는 문제 2개를 만들고 풀어보세요**")
        q1 = st.text_area("문제 1 (어떤 다항식을 어떤 일차식으로 나누는지 적어주세요)", height=70)
        a1 = st.text_input("문제 1의 답 (각 셀에 들어가는 값과 최종 몫·나머지)")
        q2 = st.text_area("문제 2 (어떤 다항식을 어떤 일차식으로 나누는지 적어주세요)", height=70)
        a2 = st.text_input("문제 2의 답 (각 셀에 들어가는 값과 최종 몫·나머지)")

        new_learning = st.text_area(
            "💡 스프레드시트 수식 구조와 조립제법이 어떻게 연결되는지 새롭게 알게 된 점",
            height=100
        )
        feeling = st.text_area("💬 이 활동을 하면서 느낀 점 (스프레드시트 활용에 대한 생각 포함)", height=90)

        submitted = st.form_submit_button("📤 제출하기", use_container_width=True, type="primary")

    if submitted:
        if not student_id or not name:
            st.warning("학번과 이름을 입력해주세요.")
        else:
            payload = {
                "sheet":       sheet_name,
                "timestamp":   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "학번":        student_id,
                "이름":        name,
                "문제1":       q1, "답1": a1,
                "문제2":       q2, "답2": a2,
                "새롭게알게된점": new_learning,
                "느낀점":      feeling,
            }
            try:
                resp = requests.post(gas_url, json=payload, timeout=10)
                if resp.status_code == 200:
                    st.success(f"✅ {name}님의 기록이 제출되었습니다!")
                    st.balloons()
                else:
                    st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"네트워크 오류: {e}")
