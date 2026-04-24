# activities/common/mini/abs_value_ineq_explorer.py
"""
절댓값을 포함한 일차부등식 탐구
- 절댓값 = 거리 시각화 놀이터
- |x|<a / |x|>a 공식 탐구 & 수직선 시각화
- 범위 나누기 단계별 실전 풀기 (4문제)
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "절댓값부등식탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key": "거리의미",
        "label": "|x − a|가 수직선 위에서 어떤 의미를 가지는지 설명하고, 이것이 절댓값 부등식 풀이에서 왜 핵심이 되는지 서술하세요.",
        "type": "text_area",
        "height": 110,
    },
    {
        "key": "공식이유",
        "label": "a > 0일 때 |x| < a의 해가 −a < x < a가 되는 이유를, 수직선 위의 거리 개념을 이용해 설명하세요.",
        "type": "text_area",
        "height": 110,
    },
    {
        "key": "범위나누기",
        "label": "|x + 1| + |x − 4| 처럼 절댓값 기호가 두 개 이상일 때 왜 구간을 나누어야 하나요? 임계점이 무엇인지 포함해서 설명하세요.",
        "type": "text_area",
        "height": 110,
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 이 활동을 하면서 느낀 점",
        "type": "text_area",
        "height": 90,
    },
]

META = {
    "title": "📐 절댓값 부등식 탐구",
    "description": "절댓값을 거리로 시각화하고, |x|<a · |x|>a 공식을 수직선에서 탐구한 뒤, 범위를 나누는 실전 문제를 단계별로 풀어보는 인터랙티브 활동입니다.",
    "order": 257,
    "hidden": False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>절댓값 부등식 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(155deg,#1a0f00 0%,#241500 55%,#120a00 100%);
  color:#fef3c7;padding:14px 12px 28px;min-height:100vh;
}
.shell{max-width:860px;margin:0 auto}
.hero{
  background:linear-gradient(135deg,rgba(217,119,6,.22),rgba(245,158,11,.08));
  border:1px solid rgba(251,191,36,.35);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hero-tag{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(251,191,36,.18);border:1px solid rgba(251,191,36,.35);
  border-radius:999px;padding:3px 12px;color:#fbbf24;
  font-size:.74rem;font-weight:700;letter-spacing:.06em;margin-bottom:8px;
}
.hero h1{font-size:1.28rem;font-weight:900;color:#fff;margin-bottom:5px}
.hero p{color:#fde68a;font-size:.86rem;line-height:1.65}
.hero strong{color:#fbbf24}
.tabs{display:flex;gap:7px;margin-bottom:14px}
.tab-btn{
  flex:1;padding:10px 6px;border-radius:12px;
  background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.2);
  color:#fbbf24;font-size:.83rem;font-weight:700;cursor:pointer;
  transition:.18s;font-family:inherit;line-height:1.4;
}
.tab-btn:hover:not(.active){background:rgba(251,191,36,.2)}
.tab-btn.active{
  background:linear-gradient(135deg,#d97706,#b45309);
  border-color:#f59e0b;color:#fff;box-shadow:0 4px 14px rgba(217,119,6,.4);
}
.tab-panel{display:none}
.tab-panel.active{display:block;animation:fadeUp .3s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
.card{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(251,191,36,.15);
  border-radius:14px;padding:14px 16px;margin-bottom:12px;
}
.card-title{font-size:1rem;font-weight:700;color:#fbbf24;margin-bottom:10px}
.slider-row{display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap}
.sl-label{min-width:56px;font-size:.88rem;color:#fde68a;font-weight:600}
input[type=range]{flex:1;min-width:100px;accent-color:#f59e0b;cursor:pointer}
.sl-val{min-width:32px;text-align:center;font-size:1rem;color:#fbbf24;font-weight:700;
  background:rgba(251,191,36,.12);border-radius:6px;padding:1px 6px}
.canvas-wrap{background:#0d0800;border-radius:12px;overflow:hidden;margin-bottom:10px}
canvas{display:block;width:100%}
.formula-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px}
@media(max-width:420px){.formula-grid{grid-template-columns:1fr}}
.f-card{border-radius:16px;padding:16px;border:2px solid}
.f-lt{background:rgba(52,211,153,.07);border-color:rgba(52,211,153,.35)}
.f-gt{background:rgba(248,113,113,.07);border-color:rgba(248,113,113,.35)}
.f-tag{font-size:.7rem;font-weight:800;letter-spacing:.06em;margin-bottom:8px;
  padding:3px 10px;border-radius:6px;display:inline-block}
.f-tag-lt{background:rgba(52,211,153,.2);color:#34d399}
.f-tag-gt{background:rgba(248,113,113,.2);color:#f87171}
.f-main{font-family:'Times New Roman',serif;font-size:1.1rem;color:#fde68a;margin:8px 0}
.f-arrow{color:#94a3b8;font-size:.9rem;margin:4px 0}
.f-sol{font-family:'Times New Roman',serif;font-size:1.05rem;font-weight:700}
.f-sol-lt{color:#6ee7b7}
.f-sol-gt{color:#fca5a5}
.f-memo{font-size:.78rem;color:#6b7280;margin-top:8px;line-height:1.6}
.toggle-row{display:flex;gap:8px;margin-bottom:12px}
.tog-btn{
  flex:1;padding:9px;border-radius:10px;border:none;cursor:pointer;
  font-size:.88rem;font-weight:700;transition:.18s;font-family:inherit;
}
.tog-lt{background:rgba(52,211,153,.12);color:#34d399;border:1.5px solid rgba(52,211,153,.3)}
.tog-gt{background:rgba(248,113,113,.1);color:#f87171;border:1.5px solid rgba(248,113,113,.3)}
.tog-lt.on{background:rgba(52,211,153,.28);box-shadow:0 0 12px rgba(52,211,153,.3)}
.tog-gt.on{background:rgba(248,113,113,.22);box-shadow:0 0 12px rgba(248,113,113,.25)}
.sol-badge{
  padding:10px 14px;border-radius:10px;font-size:.95rem;font-weight:700;
  text-align:center;margin-top:8px;line-height:1.6;
}
.sb-lt{background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.35);color:#6ee7b7}
.sb-gt{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.35);color:#fca5a5}
.prob-tabs{display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap}
.prob-tab{
  padding:7px 14px;border-radius:10px;border:1px solid rgba(251,191,36,.2);
  background:rgba(251,191,36,.08);color:#fbbf24;cursor:pointer;
  font-size:.84rem;font-weight:700;transition:.18s;font-family:inherit;
}
.prob-tab.active{background:linear-gradient(135deg,#d97706,#b45309);color:#fff;border-color:#f59e0b}
.prob-tab:hover:not(.active){background:rgba(251,191,36,.18)}
.prob-header{
  background:rgba(245,158,11,.08);border:1px solid rgba(251,191,36,.22);
  border-radius:12px;padding:12px 14px;margin-bottom:12px;
}
.prob-num{font-size:.78rem;font-weight:700;color:#d97706;margin-bottom:6px;letter-spacing:.04em}
.prob-eq{font-family:'Times New Roman',serif;font-style:italic;font-size:1.15rem;color:#fde68a}
.step-card{
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
  border-radius:12px;padding:12px 14px;margin-bottom:10px;
}
.step-title{font-size:.8rem;font-weight:700;color:#fde68a;margin-bottom:8px;letter-spacing:.04em}
.step-desc{font-size:.9rem;color:#94a3b8;margin-bottom:10px;line-height:1.8}
.opts{display:flex;flex-wrap:wrap;gap:7px;margin-top:4px}
.opt-btn{
  padding:7px 15px;border-radius:20px;
  border:1px solid rgba(251,191,36,.2);background:rgba(251,191,36,.06);
  color:#fef3c7;cursor:pointer;font-size:.88rem;transition:all .18s;font-family:inherit;
}
.opt-btn:hover:not(:disabled){background:rgba(217,119,6,.28);border-color:#f59e0b}
.opt-btn.correct{background:rgba(52,211,153,.15);color:#6ee7b7;border-color:#34d399}
.opt-btn.wrong{background:rgba(248,113,113,.1);color:#fca5a5;border-color:#f87171}
.opt-btn:disabled{cursor:default;opacity:.75}
.fb{font-size:.87rem;margin-top:6px;min-height:18px;line-height:1.6}
.fb.ok{color:#6ee7b7}.fb.ng{color:#fca5a5}
.done-banner{
  background:linear-gradient(135deg,rgba(217,119,6,.18),rgba(180,83,9,.1));
  border:1px solid #d97706;border-radius:14px;
  padding:14px;text-align:center;margin-bottom:12px;display:none;
}
.btn{padding:8px 20px;border-radius:10px;border:none;cursor:pointer;font-size:.9rem;font-weight:700;transition:.18s;font-family:inherit}
.btn-p{background:linear-gradient(135deg,#d97706,#b45309);color:#fff;box-shadow:0 3px 12px rgba(217,119,6,.3)}
.btn-p:hover{opacity:.88;transform:translateY(-1px)}
.key-box{
  background:rgba(251,191,36,.07);border:1.5px solid rgba(251,191,36,.25);
  border-radius:12px;padding:12px 16px;margin-bottom:12px;
}
.key-title{font-size:.8rem;font-weight:700;color:#fbbf24;margin-bottom:8px;letter-spacing:.05em}
.key-row{display:flex;align-items:flex-start;gap:8px;margin-bottom:6px;font-size:.88rem;line-height:1.7}
.key-num{color:#fbbf24;font-weight:700;min-width:20px;flex-shrink:0}
.dist-display{
  text-align:center;padding:10px;
  background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.3);
  border-radius:12px;margin-bottom:10px;
}
.dist-val{font-size:2.2rem;font-weight:900;color:#fbbf24;line-height:1.1}
.dist-label{font-size:.82rem;color:#d97706;margin-top:2px}
@media(max-width:600px){
  .hero h1{font-size:1.05rem}
  .f-main{font-size:.92rem}
  .tab-btn{font-size:.76rem;padding:9px 4px}
  .prob-eq{font-size:1rem}
}
</style>
</head>
<body>
<div class="shell">

<!-- HERO -->
<section class="hero">
  <div class="hero-tag">📐 절댓값 부등식 탐구</div>
  <h1>|x|는 <em style="color:#fbbf24">거리</em>다 — 수직선에서 직접 확인!</h1>
  <p>절댓값은 수직선 위에서 <strong>두 점 사이의 거리</strong>를 나타냅니다.<br>
     거리의 관점으로 보면 절댓값 부등식의 해석이 단번에 보입니다!</p>
</section>

<!-- TABS -->
<div class="tabs">
  <button class="tab-btn active" id="tbT1" onclick="showTab('t1')">📏 거리 탐구</button>
  <button class="tab-btn"        id="tbT2" onclick="showTab('t2')">🔭 공식 탐구</button>
  <button class="tab-btn"        id="tbT3" onclick="showTab('t3')">🎯 실전 풀기</button>
</div>

<!-- ══════════════ TAB 1: 거리 탐구 ══════════════ -->
<div class="tab-panel active" id="t1">

  <div class="card">
    <div class="card-title">📏 절댓값 = 수직선 위의 거리!</div>
    <p style="font-size:.87rem;color:#94a3b8;margin-bottom:14px;line-height:1.8">
      슬라이더로 <span style="color:#fbbf24;font-weight:700">x</span>와
      <span style="color:#60a5fa;font-weight:700">a</span>를 움직이면서
      <strong style="color:#fde68a">|x − a|</strong>가 두 점 사이의 거리임을 확인하세요.
    </p>

    <div class="slider-row">
      <span class="sl-label" style="color:#fbbf24">점 x</span>
      <input type="range" id="slX" min="-9" max="9" step="1" value="3" oninput="drawDist()">
      <span class="sl-val" id="lblX" style="color:#fbbf24">3</span>
    </div>
    <div class="slider-row">
      <span class="sl-label" style="color:#60a5fa">점 a</span>
      <input type="range" id="slA" min="-5" max="5" step="1" value="0" oninput="drawDist()">
      <span class="sl-val" id="lblA" style="color:#60a5fa">0</span>
    </div>

    <div class="dist-display" id="distDisplay">
      <div class="dist-val" id="distVal">3</div>
      <div class="dist-label" id="distLabel">|3 − 0| = 3</div>
    </div>

    <div class="canvas-wrap"><canvas id="cvDist" height="140"></canvas></div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;font-size:.84rem">
      <div style="background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.18);border-radius:10px;padding:10px">
        <div style="color:#fbbf24;font-weight:700;margin-bottom:4px">a = 0일 때</div>
        <div style="font-family:'Times New Roman',serif;font-style:italic;color:#fde68a;font-size:1rem">|x| = x와 원점 0 사이의 거리</div>
      </div>
      <div style="background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.18);border-radius:10px;padding:10px">
        <div style="color:#60a5fa;font-weight:700;margin-bottom:4px">a ≠ 0일 때</div>
        <div style="font-family:'Times New Roman',serif;font-style:italic;color:#fde68a;font-size:1rem">|x − a| = x와 점 a 사이의 거리</div>
      </div>
    </div>
  </div>

  <div class="key-box">
    <div class="key-title">🔑 핵심 정리</div>
    <div class="key-row"><span class="key-num">①</span><span style="color:#d1d5db">|x| ≥ 0 → 절댓값은 항상 <strong style="color:#fbbf24">0 이상</strong></span></div>
    <div class="key-row"><span class="key-num">②</span>
      <span style="color:#d1d5db">
        |x| =
        <span style="font-family:'Times New Roman',serif;font-style:italic;color:#fde68a">&nbsp;x (x ≥ 0), &nbsp;−x (x &lt; 0)</span>
      </span>
    </div>
    <div class="key-row"><span class="key-num">③</span>
      <span style="color:#d1d5db">절댓값 기호 안의 식 = 0이 되는 x의 값이 <strong style="color:#fbbf24">범위를 나누는 기준</strong></span>
    </div>
  </div>

</div><!-- t1 -->

<!-- ══════════════ TAB 2: 공식 탐구 ══════════════ -->
<div class="tab-panel" id="t2">

  <div class="formula-grid">
    <div class="f-card f-lt">
      <div class="f-tag f-tag-lt">① &lt; 형</div>
      <div class="f-main">|x| &lt; a &nbsp;(a &gt; 0)</div>
      <div class="f-arrow">⬇ 원점에서 거리가 a 미만</div>
      <div class="f-sol f-sol-lt">−a &lt; x &lt; a</div>
      <div class="f-memo">수직선: −a와 a 사이의 구간<br>(경계 포함 여부: ≤ 이면 경계 포함)</div>
    </div>
    <div class="f-card f-gt">
      <div class="f-tag f-tag-gt">② &gt; 형</div>
      <div class="f-main">|x| &gt; a &nbsp;(a &gt; 0)</div>
      <div class="f-arrow">⬇ 원점에서 거리가 a 초과</div>
      <div class="f-sol f-sol-gt">x &lt; −a &nbsp;또는&nbsp; x &gt; a</div>
      <div class="f-memo">수직선: −a 왼쪽 + a 오른쪽의 두 구간<br>(경계 포함 여부: ≥ 이면 경계 포함)</div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">🔭 수직선으로 직접 확인!</div>
    <p style="font-size:.86rem;color:#94a3b8;margin-bottom:12px;line-height:1.7">
      a값과 부등호 방향을 바꿔가면서 수직선의 해가 어떻게 달라지는지 관찰하세요.
    </p>

    <div class="toggle-row">
      <button class="tog-btn tog-lt on" id="togLt" onclick="setMode('lt')">
        |x| &lt; a &nbsp;(−a &lt; x &lt; a)
      </button>
      <button class="tog-btn tog-gt" id="togGt" onclick="setMode('gt')">
        |x| &gt; a &nbsp;(x &lt; −a 또는 x &gt; a)
      </button>
    </div>

    <div class="slider-row">
      <span class="sl-label">a</span>
      <input type="range" id="slA2" min="1" max="8" step="1" value="3" oninput="drawFormula()">
      <span class="sl-val" id="lblA2">3</span>
    </div>
    <div style="font-size:.84rem;color:#94a3b8;margin-bottom:8px">
      <span id="fmlaExpr" style="font-family:'Times New Roman',serif;font-size:1rem;color:#fde68a">|x| &lt; 3</span>
      &nbsp;의 해:&nbsp;
      <span id="fmlaSol" style="font-weight:700;color:#6ee7b7">−3 &lt; x &lt; 3</span>
    </div>

    <div class="canvas-wrap"><canvas id="cvFml" height="90"></canvas></div>
    <div id="fmlBadge" class="sol-badge sb-lt">계산 중...</div>
  </div>

  <!-- |x-a| 확장 인터랙티브 -->
  <div class="card" style="border-color:rgba(251,191,36,.3)">
    <div class="card-title">💡 |x − a| 로 확장하면? — 직접 탐구!</div>
    <p style="font-size:.86rem;color:#94a3b8;margin-bottom:12px;line-height:1.75">
      기준점 <span style="color:#60a5fa;font-weight:700">a</span>와
      반지름 <span style="color:#f97316;font-weight:700">r</span>을 바꿔보면서
      수직선의 해 구간이 어떻게 달라지는지 확인하세요.
    </p>

    <div class="formula-grid" style="margin-bottom:12px">
      <div class="f-card f-lt">
        <div class="f-tag f-tag-lt">① &lt; 형</div>
        <div class="f-main">|x − a| &lt; r</div>
        <div class="f-arrow">⬇ 점 a에서 거리 r 미만</div>
        <div class="f-sol f-sol-lt">a − r &lt; x &lt; a + r</div>
      </div>
      <div class="f-card f-gt">
        <div class="f-tag f-tag-gt">② &gt; 형</div>
        <div class="f-main">|x − a| &gt; r</div>
        <div class="f-arrow">⬇ 점 a에서 거리 r 초과</div>
        <div class="f-sol f-sol-gt">x &lt; a − r &nbsp;또는&nbsp; x &gt; a + r</div>
      </div>
    </div>

    <div class="toggle-row">
      <button class="tog-btn tog-lt on" id="togExtLt" onclick="setExtMode('lt')">
        |x − a| &lt; r
      </button>
      <button class="tog-btn tog-gt" id="togExtGt" onclick="setExtMode('gt')">
        |x − a| &gt; r
      </button>
    </div>

    <div class="slider-row">
      <span class="sl-label" style="color:#60a5fa">기준 a</span>
      <input type="range" id="slEA" min="-5" max="5" step="1" value="2" oninput="drawExt()">
      <span class="sl-val" id="lblEA" style="color:#60a5fa">2</span>
    </div>
    <div class="slider-row">
      <span class="sl-label" style="color:#f97316">반지름 r</span>
      <input type="range" id="slER" min="1" max="7" step="1" value="5" oninput="drawExt()">
      <span class="sl-val" id="lblER" style="color:#f97316">5</span>
    </div>

    <!-- 수식 전개 표시 -->
    <div style="background:rgba(255,255,255,.04);border-radius:12px;padding:12px 14px;margin-bottom:10px;font-size:.95rem;line-height:2.2;text-align:center">
      <span id="extExpr" style="font-family:'Times New Roman',serif;color:#fde68a;font-size:1.1rem">|x − 2| &lt; 5</span>
      <span style="color:#6b7280;margin:0 8px">→</span>
      <span id="extStep" style="font-family:'Times New Roman',serif;color:#94a3b8;font-size:.95rem">2 − 5 &lt; x &lt; 2 + 5</span>
      <span style="color:#6b7280;margin:0 8px">→</span>
      <span id="extSol"  style="font-family:'Times New Roman',serif;font-size:1.05rem;font-weight:700;color:#6ee7b7">−3 &lt; x &lt; 7</span>
    </div>

    <div class="canvas-wrap"><canvas id="cvExt" height="120"></canvas></div>
    <div id="extBadge" class="sol-badge sb-lt" style="margin-top:6px">계산 중...</div>
  </div>

</div><!-- t2 -->

<!-- ══════════════ TAB 3: 실전 풀기 ══════════════ -->
<div class="tab-panel" id="t3">

  <div class="prob-tabs">
    <button class="prob-tab active" id="pt0" onclick="goP(0)">문제 1</button>
    <button class="prob-tab"        id="pt1" onclick="goP(1)">문제 2</button>
    <button class="prob-tab"        id="pt2" onclick="goP(2)">문제 3</button>
    <button class="prob-tab"        id="pt3" onclick="goP(3)">문제 4</button>
  </div>

  <!-- ─── 문제 0 ─── -->
  <div id="p0">
    <div class="prob-header">
      <div class="prob-num">📝 문제 1 — 다음 부등식을 푸시오.</div>
      <div class="prob-eq">|x − 3| &lt; 5</div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 1 — 유형 파악</div>
      <div class="step-desc">이 부등식은 |x − a| &lt; r 꼴입니다. a와 r의 값은?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q0s1','A')" data-q="q0s1" data-v="A">a = 3, r = 5</button>
        <button class="opt-btn" onclick="ans('q0s1','B')" data-q="q0s1" data-v="B">a = −3, r = 5</button>
        <button class="opt-btn" onclick="ans('q0s1','C')" data-q="q0s1" data-v="C">a = 5, r = 3</button>
      </div>
      <div class="fb" id="q0s1fb"></div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 2 — 공식 적용</div>
      <div class="step-desc">|x − 3| &lt; 5 → 3 − 5 &lt; x &lt; 3 + 5. 따라서 해는?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q0s2','A')" data-q="q0s2" data-v="A">−8 &lt; x &lt; 8</button>
        <button class="opt-btn" onclick="ans('q0s2','B')" data-q="q0s2" data-v="B">−2 &lt; x &lt; 8</button>
        <button class="opt-btn" onclick="ans('q0s2','C')" data-q="q0s2" data-v="C">−2 &lt; x &lt; 2</button>
      </div>
      <div class="fb" id="q0s2fb"></div>
    </div>
    <div id="done0" class="done-banner">
      <div style="font-size:1.5rem;margin-bottom:4px">🎉</div>
      <div style="font-size:1.05rem;color:#fbbf24;font-weight:700;margin-bottom:4px">완료!</div>
      <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">
        |x − 3| &lt; 5 → <strong style="color:#6ee7b7">−2 &lt; x &lt; 8</strong>
        &nbsp;(점 3에서 거리가 5 미만인 구간)
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goP(1)">다음 문제 →</button>
    </div>
  </div>

  <!-- ─── 문제 1 ─── -->
  <div id="p1" style="display:none">
    <div class="prob-header">
      <div class="prob-num">📝 문제 2 — 다음 부등식을 푸시오.</div>
      <div class="prob-eq">|2x − 6| ≥ 4</div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 1 — |2x − 6|을 |2(x − 3)|로 변형</div>
      <div class="step-desc">|2x − 6| = |2||x − 3| = 2|x − 3|. 따라서 원래 부등식과 동치인 것은?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q1s1','A')" data-q="q1s1" data-v="A">|x − 3| ≥ 2</button>
        <button class="opt-btn" onclick="ans('q1s1','B')" data-q="q1s1" data-v="B">|x − 3| ≥ 4</button>
        <button class="opt-btn" onclick="ans('q1s1','C')" data-q="q1s1" data-v="C">|x − 3| ≥ 8</button>
      </div>
      <div class="fb" id="q1s1fb"></div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 2 — |x − 3| ≥ 2 풀기</div>
      <div class="step-desc">|x − a| ≥ r → x ≤ a − r 또는 x ≥ a + r. a = 3, r = 2를 대입하면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q1s2','A')" data-q="q1s2" data-v="A">1 ≤ x ≤ 5</button>
        <button class="opt-btn" onclick="ans('q1s2','B')" data-q="q1s2" data-v="B">x ≤ 1 또는 x ≥ 5</button>
        <button class="opt-btn" onclick="ans('q1s2','C')" data-q="q1s2" data-v="C">x ≤ −1 또는 x ≥ 1</button>
      </div>
      <div class="fb" id="q1s2fb"></div>
    </div>
    <div id="done1" class="done-banner">
      <div style="font-size:1.5rem;margin-bottom:4px">🎉</div>
      <div style="font-size:1.05rem;color:#fbbf24;font-weight:700;margin-bottom:4px">완료!</div>
      <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">
        2|x − 3| ≥ 4 → |x − 3| ≥ 2 → <strong style="color:#fca5a5">x ≤ 1 또는 x ≥ 5</strong>
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goP(2)">다음 문제 →</button>
    </div>
  </div>

  <!-- ─── 문제 2 ─── -->
  <div id="p2" style="display:none">
    <div class="prob-header">
      <div class="prob-num">📝 문제 3 — 범위를 나누어 푸시오.</div>
      <div class="prob-eq">|x − 1| ≥ 2x − 5</div>
    </div>
    <div style="background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.2);border-radius:10px;padding:10px;margin-bottom:12px;font-size:.86rem;color:#d1d5db;line-height:1.8">
      💡 우변에 x가 있으면 <strong style="color:#fbbf24">공식 직접 적용 불가</strong>.<br>
      임계점 <strong style="color:#fbbf24">x = 1</strong>을 기준으로 경우를 나눕니다.
    </div>
    <div class="step-card">
      <div class="step-title">STEP 1 — x ≥ 1일 때 풀기</div>
      <div class="step-desc">|x − 1| = x − 1 이므로 x − 1 ≥ 2x − 5, 이항하면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q2s1','A')" data-q="q2s1" data-v="A">x ≤ 4 &nbsp;→ 교집합: 1 ≤ x ≤ 4</button>
        <button class="opt-btn" onclick="ans('q2s1','B')" data-q="q2s1" data-v="B">x ≥ 4 &nbsp;→ 교집합: x ≥ 4</button>
        <button class="opt-btn" onclick="ans('q2s1','C')" data-q="q2s1" data-v="C">x ≤ −4 &nbsp;→ 교집합: 없음</button>
      </div>
      <div class="fb" id="q2s1fb"></div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 2 — x &lt; 1일 때 풀기</div>
      <div class="step-desc">|x − 1| = −(x − 1) = 1 − x 이므로 1 − x ≥ 2x − 5, 이항하면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q2s2','A')" data-q="q2s2" data-v="A">x ≤ 2 &nbsp;→ 교집합: x &lt; 1</button>
        <button class="opt-btn" onclick="ans('q2s2','B')" data-q="q2s2" data-v="B">x ≥ 2 &nbsp;→ 교집합: 없음</button>
        <button class="opt-btn" onclick="ans('q2s2','C')" data-q="q2s2" data-v="C">x ≤ −2 &nbsp;→ 교집합: x &lt; −2</button>
      </div>
      <div class="fb" id="q2s2fb"></div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 3 — 합집합 (최종 답)</div>
      <div class="step-desc">① 1 ≤ x ≤ 4 &nbsp;&nbsp; ② x &lt; 1 을 합치면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q2s3','A')" data-q="q2s3" data-v="A">x ≤ 4</button>
        <button class="opt-btn" onclick="ans('q2s3','B')" data-q="q2s3" data-v="B">1 ≤ x ≤ 4</button>
        <button class="opt-btn" onclick="ans('q2s3','C')" data-q="q2s3" data-v="C">x &lt; 4</button>
      </div>
      <div class="fb" id="q2s3fb"></div>
    </div>
    <div id="done2" class="done-banner">
      <div style="font-size:1.5rem;margin-bottom:4px">🎉</div>
      <div style="font-size:1.05rem;color:#fbbf24;font-weight:700;margin-bottom:4px">완료!</div>
      <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">
        ① 1 ≤ x ≤ 4 &nbsp;② x &lt; 1 → 합집합:
        <strong style="color:#6ee7b7">x ≤ 4</strong>
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goP(3)">다음 문제 →</button>
    </div>
  </div>

  <!-- ─── 문제 3 ─── -->
  <div id="p3" style="display:none">
    <div class="prob-header">
      <div class="prob-num">📝 문제 4 — 절댓값이 두 개! 세 구간으로 나누어 푸시오.</div>
      <div class="prob-eq">|x + 1| + |x − 4| &lt; 7</div>
    </div>
    <div style="background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.2);border-radius:10px;padding:10px;margin-bottom:12px;font-size:.86rem;color:#d1d5db;line-height:1.8">
      💡 임계점: <strong style="color:#fbbf24">x = −1</strong> (x+1=0) 과 <strong style="color:#fbbf24">x = 4</strong> (x−4=0)<br>
      → 세 구간으로 나눕니다: x &lt; −1 / −1 ≤ x &lt; 4 / x ≥ 4
    </div>
    <div class="step-card">
      <div class="step-title">STEP 1 — x &lt; −1 일 때</div>
      <div class="step-desc">|x+1| = −(x+1), |x−4| = −(x−4)<br>→ −(x+1) + (−(x−4)) = −x−1−x+4 = −2x+3 &lt; 7<br>이항하면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q3s1','A')" data-q="q3s1" data-v="A">x &gt; −2 &nbsp;→ 교집합: −2 &lt; x &lt; −1</button>
        <button class="opt-btn" onclick="ans('q3s1','B')" data-q="q3s1" data-v="B">x &gt; 2 &nbsp;→ 교집합: 없음</button>
        <button class="opt-btn" onclick="ans('q3s1','C')" data-q="q3s1" data-v="C">x &gt; −5 &nbsp;→ 교집합: −5 &lt; x &lt; −1</button>
      </div>
      <div class="fb" id="q3s1fb"></div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 2 — −1 ≤ x &lt; 4 일 때</div>
      <div class="step-desc">|x+1| = x+1, |x−4| = −(x−4) = 4−x<br>→ (x+1) + (4−x) = 5 &lt; 7 &nbsp;항상 참!<br>이 구간 전체가 해인가요?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q3s2','A')" data-q="q3s2" data-v="A">예, 전체 구간: −1 ≤ x &lt; 4</button>
        <button class="opt-btn" onclick="ans('q3s2','B')" data-q="q3s2" data-v="B">아니요, 5 &lt; 7이 거짓이므로 해 없음</button>
        <button class="opt-btn" onclick="ans('q3s2','C')" data-q="q3s2" data-v="C">일부만 해: −1 ≤ x ≤ 0</button>
      </div>
      <div class="fb" id="q3s2fb"></div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 3 — x ≥ 4 일 때</div>
      <div class="step-desc">|x+1| = x+1, |x−4| = x−4<br>→ (x+1) + (x−4) = 2x−3 &lt; 7<br>이항하면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q3s3','A')" data-q="q3s3" data-v="A">x &lt; 5 &nbsp;→ 교집합: 4 ≤ x &lt; 5</button>
        <button class="opt-btn" onclick="ans('q3s3','B')" data-q="q3s3" data-v="B">x &lt; 2 &nbsp;→ 교집합: 없음</button>
        <button class="opt-btn" onclick="ans('q3s3','C')" data-q="q3s3" data-v="C">x &lt; 10 &nbsp;→ 교집합: 4 ≤ x &lt; 10</button>
      </div>
      <div class="fb" id="q3s3fb"></div>
    </div>
    <div class="step-card">
      <div class="step-title">STEP 4 — 세 구간 합집합 (최종 답)</div>
      <div class="step-desc">① −2 &lt; x &lt; −1 &nbsp;② −1 ≤ x &lt; 4 &nbsp;③ 4 ≤ x &lt; 5 를 합치면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('q3s4','A')" data-q="q3s4" data-v="A">−2 &lt; x &lt; 5</button>
        <button class="opt-btn" onclick="ans('q3s4','B')" data-q="q3s4" data-v="B">−1 ≤ x &lt; 4</button>
        <button class="opt-btn" onclick="ans('q3s4','C')" data-q="q3s4" data-v="C">−2 &lt; x &lt; 4</button>
      </div>
      <div class="fb" id="q3s4fb"></div>
    </div>
    <div id="done3" class="done-banner">
      <div style="font-size:1.5rem;margin-bottom:4px">🏆</div>
      <div style="font-size:1.05rem;color:#fbbf24;font-weight:700;margin-bottom:4px">4문제 완료! 대단해요!</div>
      <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">
        세 구간 합집합 → <strong style="color:#6ee7b7">−2 &lt; x &lt; 5</strong>
      </p>
    </div>
  </div>

</div><!-- t3 -->
</div><!-- shell -->
<script>
/* ── 높이 조절 ── */
function notifyH(){
  var h=Math.max(document.body.scrollHeight,document.documentElement.scrollHeight)+40;
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
new ResizeObserver(function(){notifyH();}).observe(document.body);
window.addEventListener('load',function(){
  drawDist();
  drawFormula();
  drawExt();
  setTimeout(notifyH,150);
});

/* ── 탭 ── */
function showTab(n){
  ['t1','t2','t3'].forEach(function(id){
    document.getElementById(id).classList.toggle('active',id===n);
  });
  document.getElementById('tbT1').classList.toggle('active',n==='t1');
  document.getElementById('tbT2').classList.toggle('active',n==='t2');
  document.getElementById('tbT3').classList.toggle('active',n==='t3');
  setTimeout(notifyH,80);
}

/* ── 문제 전환 ── */
function goP(n){
  for(var i=0;i<4;i++){
    document.getElementById('p'+i).style.display=i===n?'block':'none';
    document.getElementById('pt'+i).classList.toggle('active',i===n);
  }
  setTimeout(notifyH,60);
}

/* ════════════ TAB1: 거리 탐구 캔버스 ════════════ */
function drawDist(){
  var x=parseInt(document.getElementById('slX').value);
  var a=parseInt(document.getElementById('slA').value);
  document.getElementById('lblX').textContent=x;
  document.getElementById('lblA').textContent=a;

  var dist=Math.abs(x-a);
  document.getElementById('distVal').textContent=dist;
  document.getElementById('distLabel').textContent=
    '|'+x+' − '+(a===0?'0':a)+'| = '+dist;

  var cv=document.getElementById('cvDist');
  var W=cv.offsetWidth||600;
  cv.width=W; cv.height=140;
  var ctx=cv.getContext('2d');
  ctx.clearRect(0,0,W,140);

  var xMin=-10,xMax=10;
  function px(v){return (v-xMin)/(xMax-xMin)*W;}

  /* axis */
  ctx.strokeStyle='rgba(255,255,255,.2)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(0,70);ctx.lineTo(W,70);ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,.2)';
  ctx.beginPath();ctx.moveTo(W,70);ctx.lineTo(W-8,66);ctx.lineTo(W-8,74);ctx.closePath();ctx.fill();

  /* tick marks */
  ctx.fillStyle='rgba(255,255,255,.3)';ctx.font='10px sans-serif';ctx.textAlign='center';
  for(var i=xMin+1;i<xMax;i++){
    ctx.strokeStyle='rgba(255,255,255,.15)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(px(i),67);ctx.lineTo(px(i),73);ctx.stroke();
    if(i%2===0){ctx.fillStyle='rgba(255,255,255,.35)';ctx.fillText(i,px(i),86);}
  }

  /* distance bar */
  var xa=Math.min(px(x),px(a)), xb=Math.max(px(x),px(a));
  ctx.globalAlpha=0.25;ctx.fillStyle='#f59e0b';
  ctx.fillRect(xa,60,xb-xa,20);
  ctx.globalAlpha=1;

  /* arc above */
  if(xb>xa){
    ctx.strokeStyle='#f59e0b';ctx.lineWidth=2.5;
    ctx.beginPath();
    ctx.arc((xa+xb)/2,70,(xb-xa)/2,Math.PI,0);
    ctx.stroke();
  }

  /* point a */
  ctx.beginPath();ctx.arc(px(a),70,7,0,Math.PI*2);
  ctx.fillStyle=a===0?'rgba(255,255,255,.6)':'#60a5fa';ctx.fill();
  ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle=a===0?'rgba(255,255,255,.9)':'#93c5fd';
  ctx.font='bold 11px sans-serif';ctx.textAlign='center';
  ctx.fillText(a===0?'0':'a='+a,px(a),58);

  /* point x */
  ctx.beginPath();ctx.arc(px(x),70,8,0,Math.PI*2);
  ctx.fillStyle='#f59e0b';ctx.fill();
  ctx.strokeStyle='#fde68a';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle='#fde68a';
  ctx.font='bold 12px sans-serif';ctx.textAlign='center';
  ctx.fillText('x='+x,px(x),50);

  /* distance label in arc */
  if(dist>0){
    ctx.fillStyle='#fbbf24';ctx.font='bold 11px sans-serif';ctx.textAlign='center';
    ctx.fillText(dist,  (xa+xb)/2,  35);
  }
  setTimeout(notifyH,20);
}

/* ════════════ TAB2: 공식 탐구 캔버스 ════════════ */
var fMode='lt';
function setMode(m){
  fMode=m;
  document.getElementById('togLt').classList.toggle('on',m==='lt');
  document.getElementById('togGt').classList.toggle('on',m==='gt');
  drawFormula();
}
function drawFormula(){
  var a=parseInt(document.getElementById('slA2').value);
  document.getElementById('lblA2').textContent=a;

  var exprTxt = fMode==='lt' ? '|x| &lt; '+a : '|x| &gt; '+a;
  var solTxt  = fMode==='lt' ? '−'+a+' &lt; x &lt; '+a : 'x &lt; −'+a+' 또는 x &gt; '+a;
  document.getElementById('fmlaExpr').innerHTML=exprTxt;
  document.getElementById('fmlaSol').innerHTML=solTxt;

  var badge=document.getElementById('fmlBadge');
  if(fMode==='lt'){
    badge.className='sol-badge sb-lt';
    badge.innerHTML='해: <strong>−'+a+' &lt; x &lt; '+a+'</strong>';
  } else {
    badge.className='sol-badge sb-gt';
    badge.innerHTML='해: <strong>x &lt; −'+a+' 또는 x &gt; '+a+'</strong>';
  }

  var cv=document.getElementById('cvFml');
  var W=cv.offsetWidth||600;
  cv.width=W;cv.height=90;
  var ctx=cv.getContext('2d');
  ctx.clearRect(0,0,W,90);
  var xMin=-10,xMax=10;
  function px(v){return (v-xMin)/(xMax-xMin)*W;}
  var y=50;

  ctx.strokeStyle='rgba(255,255,255,.2)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,.2)';
  ctx.beginPath();ctx.moveTo(W,y);ctx.lineTo(W-8,y-4);ctx.lineTo(W-8,y+4);ctx.closePath();ctx.fill();
  ctx.fillStyle='rgba(255,255,255,.3)';ctx.font='10px sans-serif';ctx.textAlign='center';
  for(var i=xMin+1;i<xMax;i++){
    ctx.strokeStyle='rgba(255,255,255,.15)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(px(i),y-3);ctx.lineTo(px(i),y+3);ctx.stroke();
    if(i%2===0){ctx.fillStyle='rgba(255,255,255,.35)';ctx.fillText(i,px(i),y+15);}
  }

  var col=fMode==='lt'?'#34d399':'#f87171';
  ctx.globalAlpha=0.3;ctx.fillStyle=col;
  if(fMode==='lt'){
    ctx.fillRect(px(-a),y-8,px(a)-px(-a),16);
  } else {
    ctx.fillRect(0,y-8,px(-a)-0,16);
    ctx.fillRect(px(a),y-8,W-px(a),16);
  }
  ctx.globalAlpha=1;

  [[- a,fMode==='lt'],[a,fMode==='lt']].forEach(function(e){
    ctx.beginPath();ctx.arc(px(e[0]),y,5,0,Math.PI*2);
    ctx.fillStyle=e[1]?'#0d0800':col;ctx.fill();
    ctx.strokeStyle=col;ctx.lineWidth=2;ctx.stroke();
    ctx.fillStyle=col;ctx.font='bold 11px sans-serif';ctx.textAlign='center';
    ctx.fillText(e[0],px(e[0]),y-12);
  });
  setTimeout(notifyH,20);
}

/* ════════════ TAB2: |x-a| 확장 탐구 캔버스 ════════════ */
var extMode='lt';
function setExtMode(m){
  extMode=m;
  document.getElementById('togExtLt').classList.toggle('on',m==='lt');
  document.getElementById('togExtGt').classList.toggle('on',m==='gt');
  drawExt();
}
function drawExt(){
  var a=parseInt(document.getElementById('slEA').value);
  var r=parseInt(document.getElementById('slER').value);
  document.getElementById('lblEA').textContent=a;
  document.getElementById('lblER').textContent=r;

  var lo=a-r, hi=a+r;
  var ltSign=extMode==='lt';

  /* 수식 전개 텍스트 */
  var opSym = ltSign ? '&lt;' : '&gt;';
  var aSgn  = a>=0 ? a : '('+a+')';
  document.getElementById('extExpr').innerHTML =
    '|x &minus; '+aSgn+'| '+opSym+' '+r;
  document.getElementById('extStep').innerHTML =
    aSgn+' &minus; '+r+' '+opSym+' x '+opSym+' '+aSgn+' + '+r;

  var solHTML, badgeClass;
  if(ltSign){
    solHTML='<span style="color:#6ee7b7">'+lo+' &lt; x &lt; '+hi+'</span>';
    badgeClass='sol-badge sb-lt';
    document.getElementById('extBadge').innerHTML=
      '해:&nbsp;<strong>'+lo+' &lt; x &lt; '+hi+'</strong>';
  } else {
    solHTML='<span style="color:#fca5a5">x &lt; '+lo+'&nbsp; 또는 &nbsp;x &gt; '+hi+'</span>';
    badgeClass='sol-badge sb-gt';
    document.getElementById('extBadge').innerHTML=
      '해:&nbsp;<strong>x &lt; '+lo+' 또는 x &gt; '+hi+'</strong>';
  }
  document.getElementById('extSol').innerHTML=solHTML;
  document.getElementById('extBadge').className=badgeClass;

  /* 캔버스 */
  var cv=document.getElementById('cvExt');
  var W=cv.offsetWidth||600;
  cv.width=W; cv.height=120;
  var ctx=cv.getContext('2d');
  ctx.clearRect(0,0,W,120);

  /* 범위를 a±r 이 잘 보이도록 동적 축 범위 설정 */
  var margin=3;
  var axMin=Math.min(lo,a)-margin;
  var axMax=Math.max(hi,a)+margin;
  /* 최소 스팬 확보 */
  if(axMax-axMin<12){var mid=(axMin+axMax)/2;axMin=mid-6;axMax=mid+6;}
  function px(v){return (v-axMin)/(axMax-axMin)*W;}

  var y=65;
  var col=ltSign?'#34d399':'#f87171';

  /* 축 */
  ctx.strokeStyle='rgba(255,255,255,.2)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,.2)';
  ctx.beginPath();ctx.moveTo(W,y);ctx.lineTo(W-8,y-4);ctx.lineTo(W-8,y+4);ctx.closePath();ctx.fill();

  /* 눈금 */
  var span=axMax-axMin;
  var step=span<=8?1:span<=16?2:5;
  var tickStart=Math.ceil(axMin/step)*step;
  ctx.font='10px sans-serif';ctx.fillStyle='rgba(255,255,255,.3)';ctx.textAlign='center';
  for(var v=tickStart;v<=axMax;v+=step){
    ctx.strokeStyle='rgba(255,255,255,.15)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(px(v),y-3);ctx.lineTo(px(v),y+3);ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,.3)';ctx.fillText(v,px(v),y+16);
  }

  /* 해 구간 칠하기 */
  ctx.globalAlpha=0.28;ctx.fillStyle=col;
  if(ltSign){
    ctx.fillRect(px(lo),y-9,px(hi)-px(lo),18);
  } else {
    ctx.fillRect(0,y-9,px(lo),18);
    ctx.fillRect(px(hi),y-9,W-px(hi),18);
  }
  ctx.globalAlpha=1;

  /* 경계점 a-r, a+r */
  [[lo,'lo'],[hi,'hi']].forEach(function(e){
    var xp=px(e[0]);
    ctx.beginPath();ctx.arc(xp,y,5,0,Math.PI*2);
    ctx.fillStyle='#0d0800';ctx.fill();
    ctx.strokeStyle=col;ctx.lineWidth=2.2;ctx.stroke();
    ctx.fillStyle=col;ctx.font='bold 10px sans-serif';ctx.textAlign='center';
    ctx.fillText(e[0],xp,y-13);
  });

  /* r 화살표 (거리 표시) */
  var pA=px(a), pHi=px(hi), pLo=px(lo);
  /* 오른쪽 r 화살표 */
  ctx.strokeStyle='#f97316';ctx.lineWidth=1.5;
  ctx.setLineDash([3,3]);
  ctx.beginPath();ctx.moveTo(pA,y-28);ctx.lineTo(pHi,y-28);ctx.stroke();
  ctx.setLineDash([]);
  ctx.beginPath();ctx.moveTo(pHi,y-28);ctx.lineTo(pHi-6,y-32);ctx.moveTo(pHi,y-28);ctx.lineTo(pHi-6,y-24);ctx.stroke();
  ctx.fillStyle='#f97316';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
  ctx.fillText('r='+r,(pA+pHi)/2,y-34);

  /* 기준점 a */
  ctx.beginPath();ctx.arc(pA,y,6,0,Math.PI*2);
  ctx.fillStyle='#60a5fa';ctx.fill();
  ctx.strokeStyle='#93c5fd';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle='#93c5fd';ctx.font='bold 11px sans-serif';ctx.textAlign='center';
  ctx.fillText('a='+a,pA,y+30);

  setTimeout(notifyH,20);
}

/* ════════════ 정답 처리 ════════════ */
var CORRECT={
  q0s1:'A',q0s2:'B',
  q1s1:'A',q1s2:'B',
  q2s1:'A',q2s2:'A',q2s3:'A',
  q3s1:'A',q3s2:'A',q3s3:'A',q3s4:'A',
};
var HINTS={
  q0s1:{
    A:'✓ 정답! |x − 3| < 5에서 a=3, r=5',
    B:'✗ x − a 형태에서 a는 빼는 수입니다. a=3이에요.',
    C:'✗ |x − a| < r 형태에서 r이 절댓값 오른쪽 숫자예요.',
  },
  q0s2:{
    A:'✗ a=3, r=5이므로 3−5=−2, 3+5=8이에요.',
    B:'✓ 정답! −2 < x < 8',
    C:'✗ a=3을 기준으로 ±5 범위예요.',
  },
  q1s1:{
    A:'✓ 정답! |2||x−3| = 2|x−3| ≥ 4 → |x−3| ≥ 2',
    B:'✗ 양변을 2로 나눠야 해요 → |x−3| ≥ 4/2 = 2',
    C:'✗ 양변을 2로 나누면 |x−3| ≥ 2예요.',
  },
  q1s2:{
    A:'✗ ≥ 형태는 두 구간이 분리돼요! 사이가 아닙니다.',
    B:'✓ 정답! x ≤ 3−2=1 또는 x ≥ 3+2=5',
    C:'✗ a=3, r=2이므로 x ≤ 3−2=1 또는 x ≥ 3+2=5예요.',
  },
  q2s1:{
    A:'✓ 정답! x−1≥2x−5 → −x≥−4 → x≤4. x≥1과의 교집합: 1≤x≤4',
    B:'✗ 이항하면 −x≥−4 → x≤4이에요.',
    C:'✗ x−1≥2x−5에서 이항하면 −x≥−4 → x≤4예요.',
  },
  q2s2:{
    A:'✓ 정답! 1−x≥2x−5 → −3x≥−6 → x≤2. x<1과의 교집합: x<1',
    B:'✗ 1−x≥2x−5 → −3x≥−6 → x≤2 (방향 주의!)',
    C:'✗ 이항 후 −3x≥−6 → x≤2이에요. 계수 부호 확인!',
  },
  q2s3:{
    A:'✓ 정답! ①1≤x≤4 ②x<1의 합집합 → x≤4',
    B:'✗ ②의 해 x<1도 포함해야 해요.',
    C:'✗ x=4는 ①에서 포함(≤)이므로 x≤4예요.',
  },
  q3s1:{
    A:'✓ 정답! −2x<4 → x>−2. x<−1과의 교집합: −2<x<−1',
    B:'✗ −2x+3<7 → −2x<4 → x>−2예요. (−2로 나누면 부호 방향 바뀜!)',
    C:'✓ 정답과 다릅니다. −2x<4 → x>−2이고 교집합은 −2<x<−1이에요.',
  },
  q3s2:{
    A:'✓ 정답! 5<7은 항상 참 → 이 구간 전체가 해',
    B:'✗ 5<7은 참이에요! 항상 성립하므로 이 구간 전체가 해입니다.',
    C:'✗ 5<7은 x에 무관하게 항상 참이므로 구간 전체가 해예요.',
  },
  q3s3:{
    A:'✓ 정답! 2x−3<7 → 2x<10 → x<5. x≥4와의 교집합: 4≤x<5',
    B:'✗ 2x<10에서 x<5이고 교집합은 4≤x<5예요.',
    C:'✗ 2x−3<7 → 2x<10 → x<5이에요.',
  },
  q3s4:{
    A:'✓ 정답! ①−2<x<−1, ②−1≤x<4, ③4≤x<5 → 합집합: −2<x<5',
    B:'✗ ①과 ③도 포함해야 해요. 세 구간을 모두 합쳐보세요.',
    C:'✗ ③ 4≤x<5도 포함해야 해요. 합집합: −2<x<5',
  },
};

var answered={};
var probKeys={
  0:['q0s1','q0s2'],
  1:['q1s1','q1s2'],
  2:['q2s1','q2s2','q2s3'],
  3:['q3s1','q3s2','q3s3','q3s4'],
};

function ans(q,v){
  if(answered[q]) return;
  answered[q]=v;
  var ok=CORRECT[q]===v;
  var fb=document.getElementById(q+'fb');
  fb.className='fb '+(ok?'ok':'ng');
  fb.innerHTML=(HINTS[q]&&HINTS[q][v])||(ok?'✓ 정답!':'✗ 다시 한번 생각해 보세요!');
  document.querySelectorAll('[data-q="'+q+'"]').forEach(function(b){
    b.disabled=true;
    if(b.dataset.v===CORRECT[q]) b.classList.add('correct');
    else if(b.dataset.v===v&&!ok) b.classList.add('wrong');
  });
  for(var n=0;n<4;n++){
    if(probKeys[n].every(function(k){return answered[k]===CORRECT[k];})){
      var d=document.getElementById('done'+n);
      if(d) d.style.display='block';
    }
  }
  setTimeout(notifyH,60);
}
</script>
</body>
</html>"""


def render():
    components.html(_HTML, height=1900, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
