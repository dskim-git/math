import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "중복조합탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이 활동과 관련된 문제를 만들고 풀어보세요**"},
    {"key": "문제1", "label": "문제 1 (벽과 칸 방법 관련)", "type": "text_area", "height": 80},
    {"key": "답1",   "label": "문제 1의 답",                 "type": "text_input"},
    {"key": "문제2", "label": "문제 2 (부정방정식 관련)",    "type": "text_area", "height": 80},
    {"key": "답2",   "label": "문제 2의 답",                 "type": "text_input"},
    {"key": "문제3", "label": "문제 3 (자유롭게)",           "type": "text_area", "height": 80},
    {"key": "답3",   "label": "문제 3의 답",                 "type": "text_input"},
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title": "미니: 중복조합의 3가지 이해 방법",
    "description": "벽과 칸, 순서쌍 대응, 부정방정식으로 중복조합 공식 nHr = n+r-1Cr을 탐구합니다.",
    "order": 25,
    "hidden": True,
}


def render():
    st.header("🔢 중복조합의 3가지 이해 방법")
    st.caption(
        "중복을 허락하여 $r$개를 선택하는 경우의 수 "
        "$_{n}H_{r} = {}_{n+r-1}C_{r}$ 를 서로 다른 방법으로 탐구합니다."
    )
    components.html(_build_html(), height=1600, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


def _build_html() -> str:
    return r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[
    {left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}
  ]})"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',system-ui,sans-serif;background:#0e1117;color:#e2e8f0;padding:14px 10px;font-size:16px;}
h2{font-size:20px;font-weight:800;margin-bottom:6px;color:#f8fafc;}
h3{font-size:17px;font-weight:700;color:#fbbf24;margin:12px 0 6px;}
p{font-size:15px;line-height:1.7;color:#cbd5e1;margin-bottom:8px;}

/* Tab bar */
.tab-bar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px;}
.tab-btn{padding:10px 16px;border:1px solid #3a4060;border-radius:8px;background:#1a1f35;
  color:#9ba8c5;cursor:pointer;font-size:15px;font-weight:700;transition:all .2s;}
.tab-btn.active{background:#2c4a8c;border-color:#4c8bf5;color:#fff;}
.tab-panel{display:none;} .tab-panel.active{display:block;}

/* Card */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
  border-radius:16px;padding:18px 20px;margin-bottom:14px;backdrop-filter:blur(8px);}
.card-title{font-size:16px;font-weight:800;color:#fbbf24;margin-bottom:12px;display:flex;align-items:center;gap:8px;}

/* Formula box */
.fbox{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);
  border-radius:12px;padding:14px 18px;margin:12px 0;text-align:center;}
.fbox .big{font-size:28px;font-weight:900;color:#fbbf24;display:block;margin-bottom:6px;}

/* Sliders */
.ctrl{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-bottom:12px;}
.ctrl label{font-size:14px;color:#94a3b8;font-weight:700;letter-spacing:.04em;text-transform:uppercase;}
.ctrl input[type=range]{width:140px;-webkit-appearance:none;height:5px;border-radius:3px;
  background:linear-gradient(90deg,#f59e0b,#ef4444);outline:none;}
.ctrl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;
  border-radius:50%;background:#fff;border:3px solid #f59e0b;cursor:pointer;}
.val-badge{display:inline-block;min-width:30px;background:linear-gradient(135deg,#f59e0b,#ef4444);
  border-radius:8px;padding:2px 8px;font-weight:900;font-size:15px;text-align:center;color:#fff;}
.val-badge.blue{background:linear-gradient(135deg,#3b82f6,#6366f1);}

/* Stars & Bars */
.sb-row{display:flex;flex-wrap:wrap;gap:4px;margin:10px 0;align-items:center;}
.cell{width:36px;height:36px;border:2px solid rgba(255,255,255,.2);border-radius:7px;
  display:flex;align-items:center;justify-content:center;font-size:18px;cursor:pointer;
  transition:all .2s;user-select:none;}
.cell.obj{background:rgba(99,102,241,.15);color:#a5b4fc;cursor:default;}
.cell.wall{background:rgba(251,191,36,.25);border-color:#fbbf24;color:#fbbf24;font-size:22px;font-weight:900;}
.cell.clickable:hover{background:rgba(251,191,36,.15);border-color:#fbbf24;transform:scale(1.08);}
.cell.selected{background:rgba(251,191,36,.3);border-color:#fbbf24;color:#fbbf24;font-size:22px;font-weight:900;}
.cell.disabled{opacity:.35;cursor:not-allowed;}
.cell.disabled:hover{transform:none;}

/* Groups label */
.group-row{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0;align-items:center;}
.group{display:flex;flex-direction:column;align-items:center;gap:2px;}
.group-items{display:flex;gap:3px;}
.grp-cell{width:32px;height:32px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:16px;}
.group-label{font-size:13px;color:#94a3b8;font-weight:700;}
.sep{font-size:20px;color:#fbbf24;font-weight:900;margin:0 2px;align-self:flex-end;margin-bottom:8px;}

/* Ordered pair table */
.op-table{width:100%;border-collapse:collapse;font-size:14px;margin-top:8px;}
.op-table th{background:rgba(245,158,11,.2);color:#fbbf24;padding:9px 12px;font-weight:700;border:1px solid rgba(255,255,255,.08);}
.op-table td{padding:8px 12px;border:1px solid rgba(255,255,255,.06);color:#e2e8f0;text-align:center;}
.op-table tr:nth-child(even) td{background:rgba(255,255,255,.03);}
.op-table tr.highlight td{background:rgba(245,158,11,.12);color:#fbbf24;}
.op-table .arrow{color:#94a3b8;font-size:16px;}

/* Equation solver */
.eq-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0;}
.xi-box{display:flex;flex-direction:column;align-items:center;gap:4px;}
.xi-box label{font-size:13px;color:#94a3b8;font-weight:700;}
.xi-input{width:58px;height:44px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);
  border-radius:8px;color:#e2e8f0;font-size:18px;font-weight:700;text-align:center;}
.xi-input:focus{outline:none;border-color:#fbbf24;}
.xi-input.ok{border-color:#4ade80;background:rgba(74,222,128,.08);}
.xi-input.bad{border-color:#f87171;background:rgba(248,113,113,.08);}
.sum-info{font-size:15px;font-weight:700;padding:8px 16px;border-radius:8px;margin-top:8px;display:inline-block;}
.sum-ok{background:rgba(74,222,128,.15);color:#4ade80;border:1px solid #4ade80;}
.sum-bad{background:rgba(248,113,113,.15);color:#f87171;border:1px solid #f87171;}

/* KPI row */
.kpi-row{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0;}
.kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:10px 18px;text-align:center;min-width:90px;flex:1;}
.kpi .num{font-size:32px;font-weight:900;color:#fbbf24;}
.kpi .lbl{font-size:13px;color:#94a3b8;margin-top:4px;font-weight:600;}

/* Step arrow */
.steps{display:flex;flex-direction:column;gap:8px;margin:10px 0;}
.step{display:flex;align-items:flex-start;gap:10px;}
.step-num{min-width:28px;height:28px;border-radius:50%;background:rgba(245,158,11,.2);
  border:1px solid #fbbf24;color:#fbbf24;font-size:14px;font-weight:800;display:flex;
  align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;}
.step-body{font-size:15px;color:#cbd5e1;line-height:1.7;}
.step-math{color:#93c5fd;font-weight:700;}

/* Warn/ok badges */
.badge{display:inline-block;padding:4px 12px;border-radius:6px;font-size:14px;font-weight:700;}
.badge-ok{background:rgba(74,222,128,.15);color:#4ade80;}
.badge-warn{background:rgba(248,113,113,.15);color:#f87171;}
.badge-blue{background:rgba(96,165,250,.15);color:#60a5fa;}

.note{font-size:14px;color:#64748b;font-style:italic;margin-top:4px;}

/* Scrollable list */
.list-wrap{max-height:220px;overflow-y:auto;background:rgba(0,0,0,.2);border-radius:8px;padding:8px;}

/* Equation visual (1-boxes) */
.vis-box{width:34px;height:34px;border-radius:5px;display:flex;align-items:center;justify-content:center;
  font-size:16px;font-weight:700;border-width:2px;border-style:solid;}
.vis-caret{font-size:20px;line-height:1;text-align:center;}
.vis-label{font-size:14px;font-weight:800;text-align:center;}
.combo-chip{display:inline-block;background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);
  border-radius:6px;padding:4px 10px;font-size:14px;font-family:monospace;color:#a5b4fc;
  margin:3px;cursor:default;}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:2px}
::-webkit-scrollbar-thumb{background:rgba(245,158,11,.35);border-radius:2px}
</style>
</head>
<body>

<!-- ── 공식 헤더 ── -->
<div class="card">
  <div class="card-title">📌 중복조합 공식</div>
  <p>서로 다른 $n$개의 대상에서 <strong>중복을 허락</strong>하여 $r$개를 선택하는 경우의 수
    (순서는 고려하지 않음)</p>
  <div class="fbox">
    <span class="big">$_{n}H_{r} = {}_{n+r-1}C_{r} = {}_{n+r-1}C_{n-1}$</span>
    <span style="font-size:12px;color:#94a3b8;">아래 세 가지 방법으로 이 공식이 왜 성립하는지 알아봅니다.</span>
  </div>
</div>

<!-- ── 탭 바 ── -->
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab(this,'sb')">① 벽과 칸 방법</button>
  <button class="tab-btn" onclick="showTab(this,'op')">② 순서쌍 대응</button>
  <button class="tab-btn" onclick="showTab(this,'eq')">③ 부정방정식</button>
</div>

<!-- ══════════════════════════════════════════
     탭 1 : 벽과 칸 (Stars & Bars)
══════════════════════════════════════════ -->
<div class="tab-panel active" id="tab-sb">

  <div class="card">
    <div class="card-title">⚙️ n, r 설정</div>
    <div class="ctrl">
      <div>
        <label>n (종류 수) = <span id="sb-n-val" class="val-badge">3</span></label><br>
        <input type="range" id="sb-n" min="2" max="5" value="3"
               oninput="sbUpdate()">
      </div>
      <div>
        <label>r (선택 수) = <span id="sb-r-val" class="val-badge blue">3</span></label><br>
        <input type="range" id="sb-r" min="1" max="6" value="3"
               oninput="sbUpdate()">
      </div>
    </div>
    <div class="kpi-row">
      <div class="kpi"><div class="num" id="sb-nr1">5</div><div class="lbl">n+r−1</div></div>
      <div class="kpi"><div class="num" id="sb-n1">2</div><div class="lbl">n−1 (벽 수)</div></div>
      <div class="kpi"><div class="num" id="sb-ans">10</div><div class="lbl">ₙHᵣ = 경우의 수</div></div>
    </div>
  </div>

  <!-- 아이디어 설명 -->
  <div class="card">
    <div class="card-title">💡 핵심 아이디어</div>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <div class="step-body">
          $r$개의 대상을 선택하되 순서는 무시 → 선택한 결과를 <strong>종류별로 모아서</strong> 나열합니다.<br>
          <span class="note">예) {●,★,●,○,●} → ●●● ★ ○ (같은 것끼리 모음)</span>
        </div>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <div class="step-body">
          $n$가지 종류를 구분하려면 <strong class="step-math">n−1</strong>개의 벽(|)이 필요합니다.<br>
          <span class="note">예) n=3이면 ●●●|★|○ — 벽 2개로 3구역 구분</span>
        </div>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <div class="step-body">
          칸 $r$개 + 벽 $(n-1)$개 = <strong class="step-math">r+n−1</strong>개의 위치 중
          벽이 놓일 <strong class="step-math">n−1</strong>개를 고르면 됩니다.
        </div>
      </div>
      <div class="step">
        <div class="step-num">4</div>
        <div class="step-body">
          따라서 <span class="step-math">$_{n}H_{r} = {}_{n+r-1}C_{n-1} = {}_{n+r-1}C_{r}$</span>
        </div>
      </div>
    </div>
  </div>

  <!-- 인터랙티브: 벽 직접 배치 -->
  <div class="card">
    <div class="card-title">🖱️ 직접 벽을 배치해 보세요</div>
    <p id="sb-instr" style="font-size:12px;color:#94a3b8;margin-bottom:8px;"></p>
    <div class="sb-row" id="sb-cells"></div>
    <div id="sb-group-display" style="margin-top:12px;min-height:48px;"></div>
    <div id="sb-wall-status" style="margin-top:8px;font-size:13px;font-weight:700;"></div>
  </div>

  <!-- 전체 경우의 수 목록 -->
  <div class="card">
    <div class="card-title">📋 전체 선택 결과 목록</div>
    <p style="font-size:12px;color:#94a3b8;margin-bottom:8px;">
      아이콘: <span style="color:#a5b4fc">●</span> = 종류 1&nbsp;&nbsp;
              <span style="color:#86efac">★</span> = 종류 2&nbsp;&nbsp;
              <span style="color:#fca5a5">▲</span> = 종류 3&nbsp;&nbsp;
              <span style="color:#fde68a">◆</span> = 종류 4&nbsp;&nbsp;
              <span style="color:#c4b5fd">■</span> = 종류 5
    </p>
    <div class="list-wrap" id="sb-list"></div>
    <div class="note" id="sb-count-note" style="margin-top:6px;"></div>
  </div>
</div>

<!-- ══════════════════════════════════════════
     탭 2 : 순서쌍 대응
══════════════════════════════════════════ -->
<div class="tab-panel" id="tab-op">

  <div class="card">
    <div class="card-title">⚙️ n, r 설정</div>
    <div class="ctrl">
      <div>
        <label>n = <span id="op-n-val" class="val-badge">3</span></label><br>
        <input type="range" id="op-n" min="2" max="4" value="3" oninput="opUpdate()">
      </div>
      <div>
        <label>r = <span id="op-r-val" class="val-badge blue">2</span></label><br>
        <input type="range" id="op-r" min="1" max="4" value="2" oninput="opUpdate()">
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">💡 순서쌍 대응 아이디어</div>
    <div class="steps">
      <div class="step">
        <div class="step-num">A</div>
        <div class="step-body">
          집합 <strong>A</strong> : $1,2,\ldots,n$ 중 중복을 허락하여 $r$개를 선택한 경우를
          <strong>순서쌍</strong>으로 나타낸 것 (비내림차순: $a_1 \le a_2 \le \cdots \le a_r$)
        </div>
      </div>
      <div class="step">
        <div class="step-num">B</div>
        <div class="step-body">
          집합 <strong>B</strong> : A의 각 원소 $(a_1,a_2,\ldots,a_r)$에
          $(0,1,\ldots,r-1)$을 더하여 얻은 순서쌍
          $(a_1,\; a_2+1,\; \ldots,\; a_r+r-1)$<br>
          <span class="note">→ 각 성분이 서로 다른 <strong>순증가</strong> 순서쌍이 됩니다.</span>
        </div>
      </div>
      <div class="step">
        <div class="step-num">★</div>
        <div class="step-body">
          B의 원소는 $1,2,\ldots,n+r-1$ 중 <strong>중복 없이</strong> $r$개를 선택한 경우
          → <span class="step-math">${}_{n+r-1}C_{r}$</span>가지<br>
          $n(A)=n(B)$ 이므로 <span class="step-math">$_{n}H_{r} = {}_{n+r-1}C_{r}$</span>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">📊 A ↔ B 대응표</div>
    <p style="font-size:12px;color:#94a3b8;margin-bottom:8px;" id="op-subtitle"></p>
    <div style="overflow-x:auto;">
      <table class="op-table" id="op-table">
        <thead><tr>
          <th>A의 원소 $(a_1,\ldots,a_r)$</th>
          <th class="arrow">→</th>
          <th>B의 원소 $(b_1,\ldots,b_r)$</th>
          <th>검증</th>
        </tr></thead>
        <tbody id="op-tbody"></tbody>
      </table>
    </div>
    <div class="kpi-row" style="margin-top:12px;">
      <div class="kpi"><div class="num" id="op-nA">—</div><div class="lbl">n(A) = ₙHᵣ</div></div>
      <div class="kpi"><div class="num" id="op-nB">—</div><div class="lbl">n(B) = ₙ₊ᵣ₋₁Cᵣ</div></div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════
     탭 3 : 부정방정식
══════════════════════════════════════════ -->
<div class="tab-panel" id="tab-eq">

  <div class="card">
    <div class="card-title">⚙️ n, r 설정</div>
    <div class="ctrl">
      <div>
        <label>n = <span id="eq-n-val" class="val-badge">3</span></label><br>
        <input type="range" id="eq-n" min="2" max="5" value="3" oninput="eqUpdate()">
      </div>
      <div>
        <label>r = <span id="eq-r-val" class="val-badge blue">4</span></label><br>
        <input type="range" id="eq-r" min="1" max="8" value="4" oninput="eqUpdate()">
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">💡 부정방정식 연결</div>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <div class="step-body">
          $a_1, a_2, \ldots, a_n$ 중 중복 허락하여 $r$개 선택<br>
          → 각 $a_i$를 <strong>선택한 개수</strong>를 $x_i$라 하면
          <span class="step-math">$x_1+x_2+\cdots+x_n = r,\quad x_i \ge 0$</span>
        </div>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <div class="step-body">
          $y_i = x_i + 1$ ($y_i \ge 1$)로 치환하면<br>
          <span class="step-math">$y_1+y_2+\cdots+y_n = r+n,\quad y_i \ge 1$</span>
        </div>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <div class="step-body">
          $r+n$개의 1을 한 줄에 놓고 생기는 <strong>$r+n-1$개의 틈</strong> 중
          $n-1$개를 골라 $|$를 꽂으면 $y_i$가 결정됨<br>
          → <span class="step-math">${}_{r+n-1}C_{n-1} = {}_{n+r-1}C_{r}$</span>가지
        </div>
      </div>
    </div>
  </div>

  <!-- 인터랙티브: xi 직접 입력 -->
  <div class="card">
    <div class="card-title">🖱️ x₁, x₂, …, xₙ 값을 직접 입력해 보세요</div>
    <p style="font-size:12px;color:#94a3b8;margin-bottom:10px;">
      합이 $r$이 되는 음이 아닌 정수 해를 찾아보세요.
    </p>
    <div class="eq-row" id="eq-inputs"></div>
    <div id="eq-sum-info"></div>
    <div id="eq-visual" style="margin-top:14px;"></div>
    <div id="eq-mapping" style="margin-top:12px;font-size:15px;color:#cbd5e1;line-height:1.8;"></div>
  </div>

  <!-- 전체 해 목록 -->
  <div class="card">
    <div class="card-title">📋 전체 해 목록</div>
    <p style="font-size:12px;color:#94a3b8;margin-bottom:6px;">
      $x_1+\cdots+x_n = r$ ($x_i \ge 0$) 의 모든 해 (최대 120개 표시)
    </p>
    <div class="list-wrap" id="eq-list"></div>
    <div class="kpi-row" style="margin-top:10px;">
      <div class="kpi"><div class="num" id="eq-total">—</div><div class="lbl">전체 해의 수 = ₙHᵣ</div></div>
      <div class="kpi"><div class="num" id="eq-formula">—</div><div class="lbl">ₙ₊ᵣ₋₁Cᵣ 계산값</div></div>
    </div>
  </div>
</div>

<!-- ══════════ JS ══════════ -->
<script>
/* ─── 수학 유틸 ─── */
function comb(n, r) {
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  r = Math.min(r, n - r);
  let res = 1;
  for (let i = 0; i < r; i++) { res = res * (n - i) / (i + 1); }
  return Math.round(res);
}
const SYMBOLS = ['●','★','▲','◆','■'];
const COLORS  = ['#a5b4fc','#86efac','#fca5a5','#fde68a','#c4b5fd'];

/* ═══════════════════════════════════════
   TAB 1 : 벽과 칸 (Stars & Bars)
═══════════════════════════════════════ */
let sbN = 3, sbR = 3;
let sbSelected = new Set();   // 벽 위치 집합

function sbWallsNeeded() { return sbN - 1; }

function sbUpdate() {
  sbN = +document.getElementById('sb-n').value;
  sbR = +document.getElementById('sb-r').value;
  document.getElementById('sb-n-val').textContent = sbN;
  document.getElementById('sb-r-val').textContent = sbR;
  document.getElementById('sb-nr1').textContent = sbN + sbR - 1;
  document.getElementById('sb-n1').textContent = sbN - 1;
  document.getElementById('sb-ans').textContent = comb(sbN + sbR - 1, sbR);
  sbSelected = new Set();
  sbRenderCells();
  sbRenderList();
}

function sbRenderCells() {
  const total = sbN + sbR - 1;
  const needed = sbWallsNeeded();
  const instr = document.getElementById('sb-instr');
  instr.textContent =
    `총 ${total}칸 중 벽이 될 ${needed}칸을 클릭하여 선택하세요 (선택: ${sbSelected.size}/${needed})`;

  const wrap = document.getElementById('sb-cells');
  wrap.innerHTML = '';
  for (let i = 0; i < total; i++) {
    const d = document.createElement('div');
    const isWall = sbSelected.has(i);
    const full = sbSelected.size >= needed && !isWall;
    d.className = 'cell' + (isWall ? ' selected' : ' clickable') + (full ? ' disabled' : '');
    d.textContent = isWall ? '|' : (i + 1);
    d.style.color = isWall ? '#fbbf24' : '#94a3b8';
    if (!full || isWall) {
      d.addEventListener('click', () => {
        if (sbSelected.has(i)) sbSelected.delete(i);
        else if (sbSelected.size < needed) sbSelected.add(i);
        sbRenderCells();
        sbShowGroup();
      });
    }
    wrap.appendChild(d);
  }
  sbShowGroup();
}

function sbShowGroup() {
  const needed = sbWallsNeeded();
  const statusEl = document.getElementById('sb-wall-status');
  const groupEl  = document.getElementById('sb-group-display');

  if (sbSelected.size !== needed) {
    statusEl.innerHTML =
      `<span class="badge badge-warn">벽 ${needed-sbSelected.size}개 더 필요합니다</span>`;
    groupEl.innerHTML = '';
    return;
  }

  const wallPos = [...sbSelected].sort((a,b)=>a-b);
  // 벽 위치로 그룹 계산
  const counts = [];
  let prev = -1;
  for (const w of wallPos) {
    counts.push(w - prev - 1);   // 벽 이전 칸수
    prev = w;
  }
  counts.push((sbN + sbR - 1) - 1 - prev); // 마지막 구역

  let html = '<div class="group-row">';
  for (let g = 0; g < sbN; g++) {
    html += `<div class="group">
      <div class="group-items">`;
    for (let k = 0; k < counts[g]; k++) {
      html += `<div class="grp-cell" style="background:rgba(99,102,241,.15);color:${COLORS[g]}">${SYMBOLS[g]}</div>`;
    }
    if (counts[g] === 0) {
      html += `<div class="grp-cell" style="opacity:.25;color:#64748b">○</div>`;
    }
    html += `</div>
      <div class="group-label">${SYMBOLS[g]} ×${counts[g]}</div>
    </div>`;
    if (g < sbN - 1) html += '<div class="sep">|</div>';
  }
  html += '</div>';
  html += `<div style="font-size:12px;color:#94a3b8;margin-top:4px;">
    선택 결과: {${counts.map((c,i)=>Array(c).fill(SYMBOLS[i]).join('')).join('')}} 
    — 합계 ${counts.reduce((a,b)=>a+b,0)}개
  </div>`;

  const countStr = counts.map((c,i) => `${SYMBOLS[i]}×${c}`).join(', ');
  statusEl.innerHTML =
    `<span class="badge badge-ok">✓ 올바르게 배치! (${countStr})</span>`;
  groupEl.innerHTML = html;
}

function sbRenderList() {
  const combos = genCombsWithRep(sbN, sbR);
  const listEl = document.getElementById('sb-list');
  const noteEl = document.getElementById('sb-count-note');
  listEl.innerHTML = '';
  const show = Math.min(combos.length, 120);
  for (let i = 0; i < show; i++) {
    const c = combos[i];
    const span = document.createElement('span');
    span.className = 'combo-chip';
    span.textContent = c.map(x => SYMBOLS[x]).join('');
    listEl.appendChild(span);
  }
  noteEl.textContent = combos.length > 120
    ? `(전체 ${combos.length}개 중 120개 표시)`
    : `전체 ${combos.length}개`;
}

/* 중복조합 생성: 0~n-1 중 r개 비내림차순 */
function genCombsWithRep(n, r) {
  const result = [];
  function bt(start, cur) {
    if (cur.length === r) { result.push([...cur]); return; }
    for (let i = start; i < n; i++) { cur.push(i); bt(i, cur); cur.pop(); }
  }
  bt(0, []);
  return result;
}

/* ═══════════════════════════════════════
   TAB 2 : 순서쌍 대응
═══════════════════════════════════════ */
let opN = 3, opR = 2;

function opUpdate() {
  opN = +document.getElementById('op-n').value;
  opR = +document.getElementById('op-r').value;
  document.getElementById('op-n-val').textContent = opN;
  document.getElementById('op-r-val').textContent = opR;
  document.getElementById('op-subtitle').textContent =
    `n=${opN}, r=${opR} → A의 원소: 1~${opN} 중 중복허락 ${opR}개 선택 (비내림차순 순서쌍)`;

  const combos = genCombsWithRep(opN, opR);  // 0-indexed
  const tbody  = document.getElementById('op-tbody');
  tbody.innerHTML = '';

  const show = Math.min(combos.length, 30);
  for (let i = 0; i < show; i++) {
    const a = combos[i].map(x => x + 1);              // 1-indexed
    const b = a.map((ai, j) => ai + j);               // ai + j (j=0,1,...,r-1)
    const isStrict = b.every((v,j) => j===0 || v > b[j-1]);
    const inRange  = b.every(v => v >= 1 && v <= opN + opR - 1);
    const tr = document.createElement('tr');
    if (i % 5 === 0 || i === 0) tr.className = 'highlight';
    tr.innerHTML = `
      <td>(${a.join(', ')})</td>
      <td class="arrow">→</td>
      <td>(${b.join(', ')})</td>
      <td>${isStrict && inRange
          ? '<span class="badge badge-ok">순증가 ✓</span>'
          : '<span class="badge badge-warn">오류</span>'}</td>`;
    tbody.appendChild(tr);
  }
  if (combos.length > 30) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="4" style="color:#64748b;font-style:italic;">
      … (전체 ${combos.length}개 중 30개 표시)</td>`;
    tbody.appendChild(tr);
  }

  const nA = comb(opN + opR - 1, opR);
  const nB = comb(opN + opR - 1, opR);
  document.getElementById('op-nA').textContent = nA;
  document.getElementById('op-nB').textContent = nB;
}

/* ═══════════════════════════════════════
   TAB 3 : 부정방정식
═══════════════════════════════════════ */
let eqN = 3, eqR = 4;

function eqUpdate() {
  eqN = +document.getElementById('eq-n').value;
  eqR = +document.getElementById('eq-r').value;
  document.getElementById('eq-n-val').textContent = eqN;
  document.getElementById('eq-r-val').textContent = eqR;
  eqRenderInputs();
  eqRenderList();
}

function eqRenderInputs() {
  const wrap = document.getElementById('eq-inputs');
  wrap.innerHTML = '';
  for (let i = 0; i < eqN; i++) {
    const d = document.createElement('div');
    d.className = 'xi-box';
    d.innerHTML = `
      <label>x<sub>${i+1}</sub></label>
      <input type="number" class="xi-input" id="xi-${i}" value="0" min="0"
             oninput="eqCheckSum()">`;
    wrap.appendChild(d);
    if (i < eqN - 1) {
      const sp = document.createElement('div');
      sp.style.cssText = 'font-size:22px;color:#94a3b8;font-weight:700;align-self:flex-end;margin-bottom:8px;';
      sp.textContent = '+';
      wrap.appendChild(sp);
    }
  }
  const eq = document.createElement('div');
  eq.style.cssText = 'font-size:15px;color:#94a3b8;font-weight:700;align-self:flex-end;margin-bottom:8px;';
  eq.innerHTML = `= <span id="eq-target" style="color:#fbbf24;font-weight:900;">${eqR}</span>`;
  wrap.appendChild(eq);
  eqCheckSum();
}

function eqCheckSum() {
  document.getElementById('eq-target').textContent = eqR;
  let sum = 0;
  const vals = [];
  for (let i = 0; i < eqN; i++) {
    const el = document.getElementById(`xi-${i}`);
    const v  = Math.max(0, parseInt(el.value) || 0);
    el.value = v;
    sum += v;
    vals.push(v);
    el.className = 'xi-input';
  }
  const infoEl = document.getElementById('eq-sum-info');
  if (sum === eqR) {
    infoEl.innerHTML = `<span class="sum-info sum-ok">✓ 합 = ${sum} = r (올바른 해!)</span>`;
  } else {
    infoEl.innerHTML = `<span class="sum-info sum-bad">합 = ${sum} ≠ r=${eqR}</span>`;
  }

  // 매핑 표시 (yi = xi+1)
  if (sum === eqR) {
    const ys = vals.map(v => v+1);
    const ySum = ys.reduce((a,b)=>a+b, 0);
    eqRenderVisual(ys);
    const mapEl = document.getElementById('eq-mapping');
    mapEl.innerHTML = `
      <strong style="color:#93c5fd;">y<sub>i</sub> = x<sub>i</sub> + 1 치환:</strong><br>
      (${vals.join(', ')}) → (${ys.join(', ')})<br>
      합: ${ySum} = r+n = ${eqR+eqN} ✓<br>
      <span style="color:#86efac;">→ 이는 1~${eqN+eqR-1} 에서 중복 없이 ${eqR}개 선택한 조합에 해당합니다.</span>`;
  } else {
    document.getElementById('eq-visual').innerHTML = '';
    document.getElementById('eq-mapping').innerHTML = '';
  }
}

function eqRenderVisual(ys) {
  const GCOL = ['#a5b4fc','#86efac','#fca5a5','#fde68a','#c4b5fd','#fdba74','#67e8f9'];
  const GBG  = ['rgba(165,180,252,.12)','rgba(134,239,172,.12)','rgba(252,165,165,.12)',
                'rgba(253,230,138,.12)','rgba(196,181,253,.12)','rgba(253,186,116,.12)',
                'rgba(103,232,249,.12)'];
  const n     = ys.length;
  const total = ys.reduce((a,b)=>a+b, 0);
  const el    = document.getElementById('eq-visual');

  // 구조: [그룹 박스들] [| 칸막이 + ∧ + yi 레이블] [그룹 박스들] … [마지막 그룹 박스들] [yn 레이블]
  // 칸막이는 그룹 사이 GAP 위치에 세워지고, ∧ 는 그 아래에 배치 → 앞 그룹의 yi를 표기
  let html = `<div style="font-size:14px;color:#94a3b8;margin-bottom:10px;font-weight:600;">
    y<sub>1</sub>+y<sub>2</sub>+⋯+y<sub>${n}</sub> = <span style="color:#fbbf24;">${total}</span>
    &nbsp;(y<sub>i</sub>≥1)&nbsp;→&nbsp;
    1이 <strong style="color:#fbbf24;">${total}</strong>개인 칸 사이
    <strong style="color:#fbbf24;">${total-1}</strong>개 공간 중
    <strong style="color:#ef4444;">${n-1}</strong>개 선택:
  </div>
  <div style="display:flex;align-items:flex-start;flex-wrap:wrap;gap:0;">`;

  for (let g = 0; g < n; g++) {
    const col = GCOL[g % GCOL.length];
    const bg  = GBG[g % GBG.length];

    // 이 그룹의 박스들 (각 박스 아래에는 빈 공간 확보)
    for (let k = 0; k < ys[g]; k++) {
      html += `<div style="display:flex;flex-direction:column;align-items:center;width:37px;">
        <div style="width:34px;height:34px;border-radius:5px;border:2px solid ${col};
          background:${bg};color:${col};display:flex;align-items:center;
          justify-content:center;font-size:15px;font-weight:700;margin:0 1px;">1</div>
        <div style="height:44px;"></div>
      </div>`;
    }

    if (g < n - 1) {
      // 칸막이 열: 위쪽 = | 막대, 아래쪽 = ∧ + yi 레이블 (앞 그룹의 개수)
      html += `<div style="display:flex;flex-direction:column;align-items:center;width:22px;flex-shrink:0;">
        <div style="width:3px;height:36px;background:#fbbf24;border-radius:2px;margin:0 auto;"></div>
        <div style="color:${col};font-size:18px;font-weight:900;line-height:1.1;">∧</div>
        <div style="color:${col};font-size:12px;font-weight:800;text-align:center;
          white-space:nowrap;line-height:1.3;">y<sub>${g+1}</sub>=${ys[g]}</div>
      </div>`;
    } else {
      // 마지막 그룹: 칸막이 없이 yn 레이블만 표시
      html += `<div style="display:flex;flex-direction:column;align-items:flex-start;
          padding-left:8px;flex-shrink:0;">
        <div style="height:36px;"></div>
        <div style="height:20px;"></div>
        <div style="color:${col};font-size:12px;font-weight:800;white-space:nowrap;">y<sub>${n}</sub>=${ys[n-1]}</div>
      </div>`;
    }
  }

  html += '</div>';
  el.innerHTML = html;
}

function eqRenderList() {
  const solutions = genNonNegSolutions(eqN, eqR);
  const listEl = document.getElementById('eq-list');
  listEl.innerHTML = '';
  const show = Math.min(solutions.length, 120);
  for (let i = 0; i < show; i++) {
    const span = document.createElement('span');
    span.className = 'combo-chip';
    span.textContent = '(' + solutions[i].join(',') + ')';
    listEl.appendChild(span);
  }
  const total = solutions.length;
  const formula = comb(eqN + eqR - 1, eqR);
  document.getElementById('eq-total').textContent = total;
  document.getElementById('eq-formula').textContent = formula;
  const note = document.getElementById('eq-list').nextElementSibling;
  if (total > 120 && note) note.textContent = `(전체 ${total}개 중 120개 표시)`;
}

/* x1+...+xn = r, xi>=0 의 모든 해 생성 */
function genNonNegSolutions(n, r) {
  const result = [];
  function bt(i, rem, cur) {
    if (i === n - 1) { result.push([...cur, rem]); return; }
    for (let v = 0; v <= rem; v++) { cur.push(v); bt(i+1, rem-v, cur); cur.pop(); }
  }
  bt(0, r, []);
  return result;
}

/* ─── 탭 전환 ─── */
function showTab(btn, id) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  btn.classList.add('active');
}

/* ─── 초기화 ─── */
sbUpdate();
opUpdate();
eqUpdate();
</script>
</body>
</html>
"""
