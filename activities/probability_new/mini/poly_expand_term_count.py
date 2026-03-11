import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "다항식전개항개수"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이 활동과 관련된 문제를 만들고 풀어보세요**"},
    {"key": "문제1", "label": "문제 1 (중복조합으로 풀 수 있는 항 개수 문제)", "type": "text_area", "height": 80},
    {"key": "답1",   "label": "문제 1의 답", "type": "text_input"},
    {"key": "문제2", "label": "문제 2 (이항정리로 풀어야 하는 항 개수 문제)", "type": "text_area", "height": 80},
    {"key": "답2",   "label": "문제 2의 답", "type": "text_input"},
    {"key": "문제3", "label": "문제 3 (두 방법 중 어느 것을 쓸지 판단하는 문제)", "type": "text_area", "height": 80},
    {"key": "답3",   "label": "문제 3의 답", "type": "text_input"},
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title": "미니: 다항식 전개의 항 개수",
    "description": "다항식 전개에서 항의 개수를 중복조합 또는 이항정리로 구하는 방법을 탐구합니다.",
    "order": 26,
    "hidden": True,
}


def render():
    st.header("🔢 다항식 전개의 항의 개수")
    st.caption(
        "$(x+y+z)^n$ 처럼 여러 변수의 일차식은 **중복조합**, "
        "$(1+x+x^2)^n$ 처럼 한 문자의 이차 이상 다항식은 **이항정리** — "
        "두 경우를 확실히 구분해 봅시다!"
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
body{font-family:'Noto Sans KR',system-ui,sans-serif;background:#0e1117;color:#e2e8f0;padding:14px 10px;font-size:15px;}
h2{font-size:19px;font-weight:800;margin-bottom:6px;color:#f8fafc;}
h3{font-size:16px;font-weight:700;color:#fbbf24;margin:12px 0 6px;}
p,li{font-size:14px;line-height:1.75;color:#cbd5e1;margin-bottom:6px;}
ul{padding-left:18px;}

/* === Tab === */
.tab-bar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px;}
.tab-btn{padding:10px 16px;border:1px solid #3a4060;border-radius:10px;background:#1a1f35;
  color:#9ba8c5;cursor:pointer;font-size:14px;font-weight:700;transition:all .2s;}
.tab-btn.active{background:#2c3e7a;border-color:#4c8bf5;color:#fff;}
.tab-panel{display:none;animation:fadeIn .25s ease;}
.tab-panel.active{display:block;}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

/* === Card === */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
  border-radius:16px;padding:16px 18px;margin-bottom:14px;backdrop-filter:blur(8px);}
.card-title{font-size:15px;font-weight:800;color:#fbbf24;margin-bottom:10px;display:flex;align-items:center;gap:8px;}

/* === Highlight boxes === */
.fbox{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);
  border-radius:12px;padding:13px 16px;margin:10px 0;text-align:center;}
.fbox .big{font-size:22px;font-weight:900;color:#fbbf24;display:block;margin-bottom:4px;}
.fbox-blue{background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.3);
  border-radius:12px;padding:13px 16px;margin:10px 0;text-align:center;}
.fbox-blue .big{font-size:22px;font-weight:900;color:#a5b4fc;display:block;margin-bottom:4px;}
.fbox-green{background:rgba(74,222,128,.07);border:1px solid rgba(74,222,128,.3);
  border-radius:12px;padding:13px 16px;margin:10px 0;text-align:center;}
.fbox-green .big{font-size:22px;font-weight:900;color:#4ade80;display:block;margin-bottom:4px;}

/* === Key difference banner === */
.diff-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0;}
.diff-cell{border-radius:12px;padding:14px 16px;}
.diff-cell.yellow{background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.35);}
.diff-cell.purple{background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.35);}
.diff-cell h4{font-size:14px;font-weight:800;margin-bottom:8px;}
.diff-cell.yellow h4{color:#fbbf24;}
.diff-cell.purple h4{color:#a5b4fc;}
.diff-cell p{font-size:13px;color:#cbd5e1;margin-bottom:4px;}

/* === Slider control === */
.ctrl{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;margin-bottom:12px;}
.ctrl-item{display:flex;flex-direction:column;gap:6px;}
.ctrl-item label{font-size:13px;color:#94a3b8;font-weight:700;letter-spacing:.03em;}
.ctrl input[type=range]{width:150px;-webkit-appearance:none;height:5px;border-radius:3px;
  background:linear-gradient(90deg,#f59e0b,#ef4444);outline:none;}
.ctrl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;
  border-radius:50%;background:#fff;border:3px solid #f59e0b;cursor:pointer;}
.ctrl input[type=range].blue{background:linear-gradient(90deg,#6366f1,#3b82f6);}
.ctrl input[type=range].blue::-webkit-slider-thumb{border-color:#6366f1;}
.val-badge{display:inline-block;min-width:28px;background:linear-gradient(135deg,#f59e0b,#ef4444);
  border-radius:7px;padding:2px 9px;font-weight:900;font-size:15px;text-align:center;color:#fff;}
.val-badge.blue{background:linear-gradient(135deg,#6366f1,#3b82f6);}
.val-badge.green{background:linear-gradient(135deg,#22c55e,#15803d);}

/* === KPI === */
.kpi-row{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0;}
.kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:10px 18px;text-align:center;min-width:90px;flex:1;}
.kpi .num{font-size:30px;font-weight:900;color:#fbbf24;}
.kpi .num.blue{color:#a5b4fc;}
.kpi .lbl{font-size:12px;color:#94a3b8;margin-top:3px;font-weight:600;}

/* === Step list === */
.steps{display:flex;flex-direction:column;gap:8px;margin:10px 0;}
.step{display:flex;align-items:flex-start;gap:10px;}
.step-num{min-width:26px;height:26px;border-radius:50%;background:rgba(245,158,11,.2);
  border:1px solid #fbbf24;color:#fbbf24;font-size:13px;font-weight:800;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;}
.step-num.blue{background:rgba(99,102,241,.2);border-color:#6366f1;color:#a5b4fc;}
.step-body{font-size:14px;color:#cbd5e1;line-height:1.75;}

/* === Monomial chip grid === */
.chip-grid{display:flex;flex-wrap:wrap;gap:5px;max-height:200px;overflow-y:auto;
  background:rgba(0,0,0,.18);border-radius:10px;padding:10px;margin:8px 0;}
.chip{display:inline-block;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);
  border-radius:7px;padding:4px 9px;font-size:13px;font-family:monospace;color:#e2e8f0;}
.chip.yellow{background:rgba(245,158,11,.1);border-color:rgba(245,158,11,.3);color:#fde68a;}
.chip.purple{background:rgba(99,102,241,.12);border-color:rgba(99,102,241,.3);color:#c4b5fd;}
.chip.green{background:rgba(74,222,128,.08);border-color:rgba(74,222,128,.25);color:#86efac;}

/* === Classification quiz === */
.quiz-card{border-radius:14px;padding:16px 18px;margin-bottom:12px;cursor:pointer;transition:all .2s;
  border:2px solid transparent;user-select:none;}
.quiz-card:hover{transform:translateY(-2px);}
.quiz-card.unanswered{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.12);}
.quiz-card.correct{background:rgba(74,222,128,.08);border-color:#4ade80;}
.quiz-card.wrong{background:rgba(248,113,113,.08);border-color:#f87171;}
.quiz-card h4{font-size:15px;font-weight:800;color:#f8fafc;margin-bottom:8px;}
.quiz-btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;}
.quiz-btn{padding:8px 18px;border-radius:8px;border:1px solid;font-size:14px;font-weight:700;
  cursor:pointer;transition:all .2s;}
.quiz-btn:disabled{opacity:.45;cursor:not-allowed;}
.quiz-btn.yellow{background:rgba(245,158,11,.12);border-color:rgba(245,158,11,.4);color:#fbbf24;}
.quiz-btn.yellow:not(:disabled):hover{background:rgba(245,158,11,.25);}
.quiz-btn.purple{background:rgba(99,102,241,.12);border-color:rgba(99,102,241,.4);color:#a5b4fc;}
.quiz-btn.purple:not(:disabled):hover{background:rgba(99,102,241,.25);}
.quiz-feedback{margin-top:10px;font-size:14px;line-height:1.7;display:none;}
.quiz-feedback.show{display:block;}
.score-bar{height:8px;border-radius:4px;background:rgba(255,255,255,.08);margin:12px 0;}
.score-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,#4ade80,#22c55e);
  transition:width .5s ease;}

/* === Compare table === */
.cmp-table{width:100%;border-collapse:collapse;font-size:14px;margin-top:8px;}
.cmp-table th{background:rgba(255,255,255,.06);padding:10px 12px;font-weight:800;
  border:1px solid rgba(255,255,255,.1);text-align:center;}
.cmp-table td{padding:9px 12px;border:1px solid rgba(255,255,255,.07);color:#e2e8f0;text-align:center;}
.cmp-table tr.row-y td:first-child{background:rgba(245,158,11,.1);color:#fbbf24;font-weight:700;}
.cmp-table tr.row-p td:first-child{background:rgba(99,102,241,.1);color:#a5b4fc;font-weight:700;}
.cmp-table .head-y{color:#fbbf24;font-weight:800;}
.cmp-table .head-p{color:#a5b4fc;font-weight:800;}

::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:2px}
::-webkit-scrollbar-thumb{background:rgba(245,158,11,.35);border-radius:2px}
</style>
</head>
<body>

<!-- ── 핵심 개념 비교 배너 ── -->
<div class="card">
  <div class="card-title">🔍 핵심 구분 — 어떤 방법을 써야 할까?</div>
  <div class="diff-grid">
    <div class="diff-cell yellow">
      <h4>🟡 중복조합 (nHr)</h4>
      <p><strong>밑이 여러 변수의 일차식</strong></p>
      <p>예) $(x+y+z)^4$, $(a+b+c+d)^3$</p>
      <p style="margin-top:8px;font-size:12px;color:#94a3b8;">각 항은 $x^i y^j z^k$ (i+j+k=n)<br>
        → 지수 합이 n인 음의 정수가 아닌 정수 순서쌍의 수<br>
        → <strong style="color:#fbbf24;">$_{n}\text{H}_{r}$ 공식 적용!</strong></p>
    </div>
    <div class="diff-cell purple">
      <h4>🟣 이항정리</h4>
      <p><strong>밑이 한 문자의 이차 이상</strong></p>
      <p>예) $(1+x+x^2)^3$, $(x+x^2)^5$</p>
      <p style="margin-top:8px;font-size:12px;color:#94a3b8;">여러 항의 차수가 같아질 수 있음<br>
        → 동류항 합산으로 항 개수 감소<br>
        → <strong style="color:#a5b4fc;">이항정리로 최고·최저 차수 확인!</strong></p>
    </div>
  </div>
  <p style="font-size:13px;color:#64748b;margin-top:4px;">
    💡 두 탭에서 슬라이더를 조작하며 차이를 직접 느껴보세요!
  </p>
</div>

<!-- ── 탭 바 ── -->
<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab(this,'tab-rc')">🟡 여러 변수 일차식 → 중복조합</button>
  <button class="tab-btn"        onclick="showTab(this,'tab-bi')">🟣 한 문자 고차식 → 이항정리</button>
  <button class="tab-btn"        onclick="showTab(this,'tab-cmp')">📊 비교 & 정리</button>
  <button class="tab-btn"        onclick="showTab(this,'tab-quiz')">🎮 분류 퀴즈</button>
</div>

<!-- ════════════════════════════════════════
     탭 1 : 여러 변수 일차식 → 중복조합
════════════════════════════════════════ -->
<div class="tab-panel active" id="tab-rc">

  <div class="card">
    <div class="card-title">⚙️ 설정 — $(x_1 + x_2 + \cdots + x_k)^n$ 꼴</div>
    <div class="ctrl">
      <div class="ctrl-item">
        <label>변수 개수 $k$ = <span id="rc-k-val" class="val-badge">3</span></label>
        <input type="range" id="rc-k" min="2" max="5" value="3" oninput="rcUpdate()">
      </div>
      <div class="ctrl-item">
        <label>지수 $n$ = <span id="rc-n-val" class="val-badge">4</span></label>
        <input type="range" id="rc-n" min="1" max="6" value="4" oninput="rcUpdate()">
      </div>
    </div>
    <div id="rc-expr" style="font-size:18px;font-weight:800;color:#f8fafc;margin-bottom:12px;"></div>
  </div>

  <div class="card">
    <div class="card-title">🔍 왜 중복조합인가?</div>
    <div class="steps" id="rc-steps"></div>
  </div>

  <div class="card">
    <div class="card-title">📐 계산 결과</div>
    <div class="kpi-row" id="rc-kpi"></div>
    <div id="rc-formula" class="fbox"></div>
  </div>

  <div class="card">
    <div class="card-title">📦 실제 단항식 목록 <span id="rc-count-badge" style="font-size:13px;color:#94a3b8;font-weight:400;"></span></div>
    <div class="chip-grid" id="rc-chips"></div>
  </div>

</div>

<!-- ════════════════════════════════════════
     탭 2 : 한 문자 고차식 → 이항정리
════════════════════════════════════════ -->
<div class="tab-panel" id="tab-bi">

  <div class="card">
    <div class="card-title">⚙️ 설정 — $(x^0 + x^1 + \cdots + x^d)^n$ 꼴</div>
    <div id="bi-warn-msg" style="display:none;color:#f87171;font-size:13px;margin-bottom:8px;padding:8px 12px;background:rgba(248,113,113,.08);border-radius:8px;border:1px solid rgba(248,113,113,.25);">
      ⚠️ 선택된 범위에서 단항식 목록이 너무 많습니다. 슬라이더를 줄여주세요.
    </div>
    <div class="ctrl">
      <div class="ctrl-item">
        <label>최고 차수 $d$ = <span id="bi-d-val" class="val-badge blue">2</span></label>
        <input type="range" class="blue" id="bi-d" min="1" max="4" value="2" oninput="biUpdate()">
      </div>
      <div class="ctrl-item">
        <label>지수 $n$ = <span id="bi-n-val" class="val-badge blue">3</span></label>
        <input type="range" class="blue" id="bi-n" min="1" max="6" value="3" oninput="biUpdate()">
      </div>
    </div>
    <div id="bi-expr" style="font-size:18px;font-weight:800;color:#f8fafc;margin-bottom:12px;"></div>
  </div>

  <div class="card">
    <div class="card-title">🔍 왜 이항정리인가? — 동류항 합산</div>
    <div class="steps" id="bi-steps"></div>
  </div>

  <div class="card">
    <div class="card-title">📐 계산 결과</div>
    <div class="kpi-row" id="bi-kpi"></div>
    <div id="bi-formula" class="fbox-blue"></div>
  </div>

  <div class="card">
    <div class="card-title">📦 동류항 합산 전 단항식 목록 <span id="bi-count-badge" style="font-size:13px;color:#94a3b8;font-weight:400;"></span></div>
    <p style="font-size:13px;color:#64748b;">같은 색 칩 = 동류항 (합산되면 계수만 다른 하나의 항)</p>
    <div class="chip-grid" id="bi-chips-before"></div>
    <div style="margin-top:10px;">
      <p style="font-size:13px;color:#94a3b8;margin-bottom:6px;">▶ 동류항 합산 후 (서로 다른 항만)</p>
      <div class="chip-grid" id="bi-chips-after"></div>
    </div>
  </div>

</div>

<!-- ════════════════════════════════════════
     탭 3 : 비교 & 정리
════════════════════════════════════════ -->
<div class="tab-panel" id="tab-cmp">

  <div class="card">
    <div class="card-title">📊 두 경우 한눈에 비교</div>
    <table class="cmp-table">
      <thead>
        <tr>
          <th></th>
          <th class="head-y">🟡 여러 변수 일차식</th>
          <th class="head-p">🟣 한 문자 고차식</th>
        </tr>
      </thead>
      <tbody>
        <tr class="row-y">
          <td>예시</td>
          <td>$(x+y+z)^4$</td>
          <td>$(1+x+x^2)^3$</td>
        </tr>
        <tr class="row-y">
          <td>일반항</td>
          <td>$\dfrac{n!}{i!\,j!\,k!}x^i y^j z^k$</td>
          <td>각 항의 계수는 이항(다항)정리에 의해 결정됨<br><span style="font-size:12px;color:#94a3b8;">→ $(1+x+x^2)^3$의 $x^3$ 항의 계수: $1+6+1=7$가지 방법</span></td>
        </tr>
        <tr class="row-y">
          <td>동류항?</td>
          <td style="color:#4ade80;">❌ 없음 (변수가 다름)</td>
          <td style="color:#f87171;">✅ 있음 (차수가 겹침)</td>
        </tr>
        <tr class="row-y">
          <td>항 개수</td>
          <td>$_{k+n-1}C_{n}$ = $_{k}H_{n}$</td>
          <td>최고차수 $dn$, 최저차수 $0$<br>→ $dn+1$개 이하</td>
        </tr>
        <tr class="row-y">
          <td>방법</td>
          <td style="color:#fbbf24;font-weight:800;">중복조합</td>
          <td style="color:#a5b4fc;font-weight:800;">이항정리 (다항정리)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <div class="card-title">💡 핵심 판단 기준</div>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <div class="step-body">전개식의 각 항이 <strong>서로 다른 변수의 곱</strong>인가? → <strong style="color:#fbbf24;">중복조합</strong><br>
          예) $x^2 y z$, $y^3$, $z^4$ → 모두 차수가 다른 단항식, 절대 합쳐지지 않음</div>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <div class="step-body">전개식의 각 항이 <strong>같은 변수 $x$의 거듭제곱</strong>인가? → <strong style="color:#a5b4fc;">이항정리</strong><br>
          예) $(1+x+x^2)^3$ 에서 $x^3$이 나오는 방법: $1\cdot x^3$, $x\cdot x^2$, $x^3\cdot 1$ 등 → 같은 차수끼리 합산</div>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <div class="step-body"><strong>한 문자 고차식의 항 개수</strong> = (최고 차수 $dn$) − (최저 차수 $0$) + 1 = $dn+1$<br>
          단, 실제로 등장하지 않는 차수가 없으므로 <strong>정확히 $dn+1$개</strong>!</div>
      </div>
    </div>
    <div class="fbox-green" style="margin-top:12px;">
      <span class="big">$(1+x+x^2)^3 = x^6+3x^5+6x^4+7x^3+6x^2+3x+1$</span>
      <span style="font-size:13px;color:#86efac;">최고차 $2\times3=6$, 최저차 $0$ → $6-0+1=7$개 ✅</span>
    </div>
  </div>

  <div class="card">
    <div class="card-title">⚡ 빠른 암기 트릭</div>
    <ul style="padding-left:20px;">
      <li style="margin-bottom:10px;"><strong style="color:#fbbf24;">변수가 $k$개</strong>인 일차식을 $n$제곱 → $_{k+n-1}C_n$개<br>
        <span style="font-size:12px;color:#64748b;">예) 3변수, 4제곱: $_{3+4-1}C_4 = {}_6C_4 = 15$</span></li>
      <li style="margin-bottom:10px;"><strong style="color:#a5b4fc;">1개 변수</strong>의 $d$차식을 $n$제곱 → $dn+1$개<br>
        <span style="font-size:12px;color:#64748b;">예) 2차식, 3제곱: $2\times3+1 = 7$</span></li>
    </ul>
  </div>

</div>

<!-- ════════════════════════════════════════
     탭 4 : 분류 퀴즈
════════════════════════════════════════ -->
<div class="tab-panel" id="tab-quiz">

  <div class="card">
    <div class="card-title">🎮 분류 퀴즈 — 중복조합 vs 이항정리</div>
    <p>각 식에 알맞은 풀이 방법을 선택하세요. 정답 후 항의 개수도 확인해 보세요!</p>
    <div class="score-bar"><div class="score-fill" id="score-fill" style="width:0%"></div></div>
    <p id="score-txt" style="font-size:13px;color:#94a3b8;margin-bottom:14px;">진행: 0 / 8</p>
    <div id="quiz-container"></div>
    <button id="reset-btn" onclick="resetQuiz()"
      style="margin-top:12px;padding:10px 22px;border-radius:10px;border:1px solid rgba(245,158,11,.4);
             background:rgba(245,158,11,.1);color:#fbbf24;font-size:14px;font-weight:700;cursor:pointer;">
      🔄 처음부터 다시
    </button>
  </div>

</div>

<!-- ════════════════
     JavaScript
════════════════ -->
<script>
// ── 탭 전환 ──
function showTab(btn, id) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(id).classList.add('active');
  renderMathIfNeeded();
}
function renderMathIfNeeded() {
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [
        {left:'$$',right:'$$',display:true},
        {left:'$',right:'$',display:false}
      ]
    });
  }
}

// ── 수학 헬퍼 ──
function comb(n, r) {
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  r = Math.min(r, n - r);
  let res = 1;
  for (let i = 0; i < r; i++) res = res * (n - i) / (i + 1);
  return Math.round(res);
}
function varName(i, k) {
  if (k <= 4) return ['x','y','z','w'][i];
  return 'x_{' + (i+1) + '}';
}

// ──────────────────────────────────────────
// 탭 1 : 여러 변수 일차식 → 중복조합
// ──────────────────────────────────────────
function rcUpdate() {
  const k = +document.getElementById('rc-k').value;
  const n = +document.getElementById('rc-n').value;
  document.getElementById('rc-k-val').textContent = k;
  document.getElementById('rc-n-val').textContent = n;

  // 수식 표현
  const vars = Array.from({length:k}, (_,i) => varName(i,k)).join('+');
  document.getElementById('rc-expr').innerHTML = '$(' + vars + ')^{'+n+'}$';

  // 단계별 설명
  const stepsEl = document.getElementById('rc-steps');
  const varList = Array.from({length:k}, (_,i) => varName(i,k));
  const varStr = varList.join(', ');
  const exponents = varList.map(v => 'i_{'+v+'}').join('+');
  stepsEl.innerHTML = `
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">전개하면 각 항은 $${varList.map(v=>v+'^{i_{'+v+'}}').join('')}$ 꼴입니다.<br>
        단, 각 지수는 음이 아닌 정수이고 합이 $n$: $${varList.map(v=>'i_{'+v+'}').join('+')} = ${n}$</div>
    </div>
    <div class="step">
      <div class="step-num">2</div>
      <div class="step-body">변수가 <strong style="color:#fbbf24;">${k}개</strong>이므로 각 항을 결정하는 것은<br>
        '합이 $${n}$인 음의 정수가 아닌 정수 순서쌍 $(${varStr})$의 수'와 같습니다.</div>
    </div>
    <div class="step">
      <div class="step-num">3</div>
      <div class="step-body">이 순서쌍의 수 = <strong style="color:#fbbf24;">$_{${k}}H_{${n}} = {}_{${k+n-1}}C_{${n}}$</strong><br>
        "<strong>${k}종류</strong>에서 중복 허용하여 <strong>${n}개</strong>를 택하는 경우의 수"와 같음!</div>
    </div>
    <div class="step">
      <div class="step-num">4</div>
      <div class="step-body">서로 다른 변수의 곱이므로 <strong>동류항이 생기지 않아</strong><br>
        항 개수 = 순서쌍 개수 = <strong style="color:#fbbf24;">${comb(k+n-1,n)}개</strong></div>
    </div>
  `;

  // KPI
  const total = comb(k + n - 1, n);
  document.getElementById('rc-kpi').innerHTML = `
    <div class="kpi"><div class="num">${k}</div><div class="lbl">변수 종류 (k)</div></div>
    <div class="kpi"><div class="num">${n}</div><div class="lbl">지수 (n)</div></div>
    <div class="kpi"><div class="num">${k+n-1}</div><div class="lbl">k+n−1</div></div>
    <div class="kpi"><div class="num">${total}</div><div class="lbl">항의 개수</div></div>
  `;
  document.getElementById('rc-formula').innerHTML =
    `<span class="big">$_{${k}}H_{${n}} = {}_{${k+n-1}}C_{${n}} = ${total}$</span>
     <span style="font-size:13px;color:#94a3b8;">서로 다른 항의 개수</span>`;

  // 단항식 목록 (k≤3, n≤5일 때만 나열)
  const chipsEl = document.getElementById('rc-chips');
  if (k <= 3 && n <= 5) {
    const chips = [];
    const colors = ['yellow','purple','green'];
    if (k === 2) {
      for (let a = n; a >= 0; a--) {
        const b = n - a;
        chips.push({label: makeMonoLabel(varList,[a,b]), col:'yellow'});
      }
    } else if (k === 3) {
      for (let a = n; a >= 0; a--)
        for (let b = n-a; b >= 0; b--) {
          const c = n-a-b;
          chips.push({label: makeMonoLabel(varList,[a,b,c]), col:'yellow'});
        }
    }
    document.getElementById('rc-count-badge').textContent = `(${chips.length}개)`;
    chipsEl.innerHTML = chips.map(c=>`<span class="chip ${c.col}">${c.label}</span>`).join('');
  } else {
    document.getElementById('rc-count-badge').textContent = '';
    chipsEl.innerHTML = `<span style="color:#64748b;font-size:13px;">k≤3, n≤5일 때 단항식 목록을 표시합니다.</span>`;
  }

  renderMathIfNeeded();
}

function makeMonoLabel(vars, exps) {
  let s = '';
  for (let i = 0; i < vars.length; i++) {
    if (exps[i] === 0) continue;
    s += vars[i] + (exps[i] > 1 ? exps[i] : '');
  }
  return s || '1';
}

// ──────────────────────────────────────────
// 탭 2 : 한 문자 고차식 → 이항정리
// ──────────────────────────────────────────
function biUpdate() {
  const d = +document.getElementById('bi-d').value;
  const n = +document.getElementById('bi-n').value;
  document.getElementById('bi-d-val').textContent = d;
  document.getElementById('bi-n-val').textContent = n;

  // 식 표현
  const terms = Array.from({length:d+1}, (_,i) => i===0?'1':(i===1?'x':'x^{'+i+'}'));
  const exprStr = '(' + terms.join('+') + ')^{'+n+'}';
  document.getElementById('bi-expr').innerHTML = '$' + exprStr + '$';

  // 단계별 설명
  const stepsEl = document.getElementById('bi-steps');
  const maxDeg = d * n;
  stepsEl.innerHTML = `
    <div class="step">
      <div class="step-num blue">1</div>
      <div class="step-body">전개 시 선택 조합 $(e_0,e_1,\\ldots,e_{${d}})$ (합 $=${n}$)에 대해 각 항은<br>
        $x^{0\\cdot e_0 + 1\\cdot e_1 + \\cdots + ${d}\\cdot e_{${d}}} = x^{e_1+2e_2+\\cdots+${d}e_{${d}}}$ 꼴</div>
    </div>
    <div class="step">
      <div class="step-num blue">2</div>
      <div class="step-body">지수 = $e_1+2e_2+\\cdots+${d}e_{${d}}$ → 최솟값 $0$, 최댓값 $${d}\\times${n}=${maxDeg}$<br>
        하지만 <strong style="color:#a5b4fc;">서로 다른 조합이 같은 지수를 줄 수 있어요!</strong><br>
        → 동류항이 생겨 항이 합산됩니다.</div>
    </div>
    <div class="step">
      <div class="step-num blue">3</div>
      <div class="step-body">중복조합으로는 개수를 셀 수 <strong>없고</strong>,<br>
        실제 지수 $0, 1, 2, \\ldots, ${maxDeg}$ 가 모두 등장하는지 확인해야 합니다.<br>
        → <strong style="color:#a5b4fc;">이항(다항)정리로 계수를 직접 계산</strong>하는 것이 정석!</div>
    </div>
    <div class="step">
      <div class="step-num blue">4</div>
      <div class="step-body">결론: 서로 다른 항의 개수 = <strong style="color:#a5b4fc;">최고차수 − 최저차수 + 1 = $${maxDeg}+1 = ${maxDeg+1}$개</strong></div>
    </div>
  `;

  // KPI
  const rawCount = Math.pow(d+1, n); // 전개 전 항 수 (다항정리 합산 전)
  document.getElementById('bi-kpi').innerHTML = `
    <div class="kpi"><div class="num blue">${d}</div><div class="lbl">최고차수 (d)</div></div>
    <div class="kpi"><div class="num blue">${n}</div><div class="lbl">지수 (n)</div></div>
    <div class="kpi"><div class="num blue">${maxDeg}</div><div class="lbl">최고차수 d×n</div></div>
    <div class="kpi"><div class="num blue">${maxDeg+1}</div><div class="lbl">서로 다른 항 수</div></div>
  `;
  document.getElementById('bi-formula').innerHTML =
    `<span class="big" style="color:#a5b4fc;">항 개수 = $d\\cdot n + 1 = ${d}\\times${n}+1 = ${maxDeg+1}$</span>
     <span style="font-size:13px;color:#94a3b8;">최저차 0 ~ 최고차 ${maxDeg}의 모든 정수 차수가 등장</span>`;

  // 동류항 합산 전/후 목록
  const warnEl = document.getElementById('bi-warn-msg');
  const beforeEl = document.getElementById('bi-chips-before');
  const afterEl = document.getElementById('bi-chips-after');
  document.getElementById('bi-count-badge').textContent = '';

  if (d <= 3 && n <= 4) {
    warnEl.style.display = 'none';
    const COLORS = ['#fde68a','#c4b5fd','#86efac','#93c5fd','#fca5a5','#fdba74','#a5f3fc'];
    // 동류항 합산 전: 모든 (e0,...,ed) 조합 나열
    const before = [];
    function gen(idx, rem, cur) {
      if (idx === d) {
        cur.push(rem);
        const deg = cur.reduce((s,v,i)=>s+i*v, 0);
        before.push({e: [...cur], deg});
        cur.pop();
        return;
      }
      for (let v = rem; v >= 0; v--) {
        cur.push(v);
        gen(idx+1, rem-v, cur);
        cur.pop();
      }
    }
    gen(0, n, []);
    document.getElementById('bi-count-badge').textContent = `(합산 전 ${before.length}개)`;
    const colorMap = {};
    before.forEach(item => {
      if (!(item.deg in colorMap)) colorMap[item.deg] = COLORS[item.deg % COLORS.length];
    });
    beforeEl.innerHTML = before.map(item => {
      const label = 'x^{'+item.deg+'}';
      const col = colorMap[item.deg];
      return `<span class="chip" style="background:${col}22;border-color:${col}55;color:${col};"
        title="${item.e.map((v,i)=>'e'+i+'='+v).join(', ')}">$${label}$</span>`;
    }).join('');
    afterEl.innerHTML = Array.from({length:maxDeg+1},(_,i)=>{
      const col = COLORS[i % COLORS.length];
      return `<span class="chip" style="background:${col}22;border-color:${col}55;color:${col};">$x^{${i}}$</span>`;
    }).join('');
  } else {
    warnEl.style.display = 'block';
    beforeEl.innerHTML = `<span style="color:#64748b;font-size:13px;">d≤3, n≤4일 때 목록을 표시합니다.</span>`;
    afterEl.innerHTML = `<span style="color:#64748b;font-size:13px;"></span>`;
  }

  renderMathIfNeeded();
}

// ──────────────────────────────────────────
// 탭 4 : 분류 퀴즈
// ──────────────────────────────────────────
const QUIZ_DATA = [
  {
    expr: '(x+y+z)^4',
    katex: '(x+y+z)^4',
    type: 'rc',
    answer: 15,
    explanation: '3개 변수의 일차식 → 중복조합: $_{3}H_{4} = {}_{6}C_{4} = 15$개',
  },
  {
    expr: '(a+b+c+d)^3',
    katex: '(a+b+c+d)^3',
    type: 'rc',
    answer: 20,
    explanation: '4개 변수의 일차식 → 중복조합: $_{4}H_{3} = {}_{6}C_{3} = 20$개',
  },
  {
    expr: '(1+x+x^2)^3',
    katex: '(1+x+x^2)^3',
    type: 'bi',
    answer: 7,
    explanation: '한 문자 2차식 → 이항정리: 최고차 $2\\times3=6$, 항 개수 $6+1=7$개',
  },
  {
    expr: '(x+y)^5',
    katex: '(x+y)^5',
    type: 'rc',
    answer: 6,
    explanation: '2개 변수의 일차식 → 중복조합: $_{2}H_{5} = {}_{6}C_{5} = 6$개',
  },
  {
    expr: '(1+x+x^2+x^3)^2',
    katex: '(1+x+x^2+x^3)^2',
    type: 'bi',
    answer: 7,
    explanation: '한 문자 3차식 → 이항정리: 최고차 $3\\times2=6$, 항 개수 $6+1=7$개',
  },
  {
    expr: '(x+y+z+w)^2',
    katex: '(x+y+z+w)^2',
    type: 'rc',
    answer: 10,
    explanation: '4개 변수의 일차식 → 중복조합: $_{4}H_{2} = {}_{5}C_{2} = 10$개',
  },
  {
    expr: '(x+x^2)^4',
    katex: '(x+x^2)^4',
    type: 'bi',
    answer: 5,
    explanation: '한 문자: 최저차 $1\\times4=4$, 최고차 $2\\times4=8$, 항 개수 $8-4+1=5$개',
  },
  {
    expr: '(x+y+z)^6',
    katex: '(x+y+z)^6',
    type: 'rc',
    answer: 28,
    explanation: '3개 변수의 일차식 → 중복조합: $_{3}H_{6} = {}_{8}C_{6} = 28$개',
  },
];

let quizState = [];

function resetQuiz() {
  quizState = QUIZ_DATA.map(() => ({answered: false, correct: false}));
  renderQuiz();
}

function renderQuiz() {
  const container = document.getElementById('quiz-container');
  container.innerHTML = QUIZ_DATA.map((q, i) => {
    const st = quizState[i];
    const cardClass = !st.answered ? 'unanswered' : (st.correct ? 'correct' : 'wrong');
    const icon = !st.answered ? '' : (st.correct ? '✅ ' : '❌ ');
    return `
      <div class="quiz-card ${cardClass}" id="qcard-${i}">
        <h4>${icon}Q${i+1}. $${q.katex}$ 를 전개할 때 서로 다른 항의 개수는?</h4>
        <div class="quiz-btns">
          <button class="quiz-btn yellow" onclick="answerQuiz(${i},'rc')"
            ${st.answered ? 'disabled' : ''}>🟡 중복조합</button>
          <button class="quiz-btn purple" onclick="answerQuiz(${i},'bi')"
            ${st.answered ? 'disabled' : ''}>🟣 이항정리</button>
        </div>
        <div class="quiz-feedback ${st.answered ? 'show' : ''}" id="qfeed-${i}">
          ${st.answered ? `<strong>${st.correct ? '🎉 정답!' : '😅 오답!'}</strong> ${q.explanation}<br>
          <strong>→ 서로 다른 항의 개수: <span style="color:#fbbf24;">${q.answer}개</span></strong>` : ''}
        </div>
      </div>`;
  }).join('');
  updateScore();
  renderMathIfNeeded();
}

function answerQuiz(i, chosen) {
  const q = QUIZ_DATA[i];
  quizState[i].answered = true;
  quizState[i].correct = (chosen === q.type);
  renderQuiz();
}

function updateScore() {
  const total = QUIZ_DATA.length;
  const done = quizState.filter(s => s.answered).length;
  const correct = quizState.filter(s => s.correct).length;
  document.getElementById('score-txt').textContent =
    `진행: ${done} / ${total}  |  정답: ${correct}개`;
  document.getElementById('score-fill').style.width = (done / total * 100) + '%';
}

// ── 초기 실행 ──
rcUpdate();
biUpdate();
resetQuiz();
</script>
</body>
</html>
"""
