# activities/common/mini/linear_ineq_system_explorer.py
"""
연립일차부등식 수직선 탐구 & 단계별 풀기
- 수직선 시뮬레이터: 두 부등식의 해와 공통부분을 시각적으로 탐구
- 4문제 단계별 풀이 연습
- 4가지 패턴 정리 카드
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "연립일차부등식탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key": "풀이순서",
        "label": "연립일차부등식을 풀 때 어떤 순서로 접근했나요? 수직선을 활용한 풀이 과정을 자신의 말로 설명하세요.",
        "type": "text_area",
        "height": 110,
    },
    {
        "key": "공통부분없음",
        "label": "두 부등식의 해의 공통부분이 없는 경우는 어떤 상황인가요? 이번 활동에서 만난 예를 들어 수직선과 함께 설명하세요.",
        "type": "text_area",
        "height": 110,
    },
    {
        "key": "부호방향",
        "label": "일차부등식을 풀 때 계수가 음수이면 부등호 방향이 바뀌는 이유를 설명하고, 실수하기 쉬운 상황의 예를 하나 들어보세요.",
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
    "title": "📏 연립일차부등식 수직선 탐구",
    "description": "수직선 위에서 두 부등식의 해가 어떻게 겹치는지 직접 탐구하고, 교과서 문제를 단계별로 풀어보는 인터랙티브 활동입니다.",
    "order": 256,
    "hidden": False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>연립일차부등식 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(155deg,#031a1a 0%,#0a2020 55%,#051515 100%);
  color:#ccfbf1;padding:14px 12px 28px;min-height:100vh;
}
.shell{max-width:860px;margin:0 auto}
.hero{
  background:linear-gradient(135deg,rgba(13,148,136,.22),rgba(20,184,166,.08));
  border:1px solid rgba(94,234,212,.35);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hero-tag{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(94,234,212,.18);border:1px solid rgba(94,234,212,.35);
  border-radius:999px;padding:3px 12px;color:#5eead4;
  font-size:.74rem;font-weight:700;letter-spacing:.06em;margin-bottom:8px;
}
.hero h1{font-size:1.28rem;font-weight:900;color:#fff;margin-bottom:5px}
.hero p{color:#99f6e4;font-size:.86rem;line-height:1.65}
.hero strong{color:#5eead4}

.tabs{display:flex;gap:7px;margin-bottom:14px}
.tab-btn{
  flex:1;padding:10px 6px;border-radius:12px;
  background:rgba(94,234,212,.1);border:1px solid rgba(94,234,212,.2);
  color:#5eead4;font-size:.83rem;font-weight:700;cursor:pointer;
  transition:.18s;font-family:inherit;line-height:1.4;
}
.tab-btn:hover:not(.active){background:rgba(94,234,212,.2)}
.tab-btn.active{
  background:linear-gradient(135deg,#0d9488,#0f766e);
  border-color:#14b8a6;color:#fff;box-shadow:0 4px 14px rgba(13,148,136,.4);
}
.tab-panel{display:none}
.tab-panel.active{display:block;animation:fadeUp .3s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}

.card{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(94,234,212,.15);
  border-radius:14px;padding:14px 16px;margin-bottom:12px;
}
.card-title{font-size:1rem;font-weight:700;color:#5eead4;margin-bottom:10px}

.slider-row{display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap}
.sl-label{min-width:72px;font-size:.9rem;color:#99f6e4;font-weight:600}
input[type=range]{flex:1;min-width:100px;accent-color:#14b8a6;cursor:pointer}
.sl-val{min-width:28px;text-align:right;font-size:1rem;color:#fbbf24;font-weight:700}

select{
  background:#0d2a2a;border:1px solid rgba(94,234,212,.3);
  color:#ccfbf1;border-radius:8px;padding:4px 8px;font-family:inherit;font-size:.95rem;cursor:pointer;
  -webkit-appearance:auto;
}
select:focus{outline:none;border-color:#14b8a6}
select option{background:#0d2a2a;color:#ccfbf1}

.canvas-wrap{background:#071515;border-radius:12px;overflow:hidden;margin-bottom:10px}
canvas{display:block;width:100%}

.result-badge{
  padding:9px 14px;border-radius:10px;font-size:.92rem;font-weight:700;
  text-align:center;margin-top:6px;transition:.3s;line-height:1.6;
}
.rb-ok  {background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.4);color:#6ee7b7}
.rb-none{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.4);color:#fca5a5}
.rb-pt  {background:rgba(251,191,36,.1); border:1px solid rgba(251,191,36,.4); color:#fde68a}

.cases-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px}
@media(max-width:400px){.cases-grid{grid-template-columns:1fr}}
.case-card{
  background:rgba(255,255,255,.04);border:1.5px solid rgba(94,234,212,.18);
  border-radius:12px;padding:12px;
}
.case-label{font-size:.78rem;font-weight:700;color:#5eead4;margin-bottom:4px}
.case-sys{
  font-family:'Times New Roman',serif;font-style:italic;
  font-size:.9rem;color:#fde68a;margin-bottom:8px;
}
.case-canvas-wrap{background:#071515;border-radius:8px;overflow:hidden;margin-bottom:8px}
.case-result{
  display:inline-block;font-size:.82rem;font-weight:700;
  padding:3px 10px;border-radius:6px;
}
.cr-ok  {background:rgba(52,211,153,.15);color:#6ee7b7;border:1px solid rgba(52,211,153,.3)}
.cr-none{background:rgba(248,113,113,.15);color:#fca5a5;border:1px solid rgba(248,113,113,.3)}
.cr-pt  {background:rgba(251,191,36,.15); color:#fde68a;border:1px solid rgba(251,191,36,.3)}

/* practice */
.prob-tabs{display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap}
.prob-tab{
  padding:7px 14px;border-radius:10px;border:none;cursor:pointer;
  font-size:.84rem;font-weight:700;transition:.18s;font-family:inherit;
  background:rgba(94,234,212,.1);color:#5eead4;border:1px solid rgba(94,234,212,.2);
}
.prob-tab.active{background:linear-gradient(135deg,#0d9488,#0f766e);color:#fff;border-color:#14b8a6}
.prob-tab:hover:not(.active){background:rgba(94,234,212,.2)}

.prob-header{
  background:rgba(20,184,166,.08);border:1px solid rgba(94,234,212,.22);
  border-radius:12px;padding:12px 14px;margin-bottom:12px;
}
.prob-num{font-size:.78rem;font-weight:700;color:#0d9488;margin-bottom:6px;letter-spacing:.04em;text-transform:uppercase}
.prob-sys{display:flex;align-items:center;gap:8px}
.prob-brace{font-size:2.8rem;color:#5eead4;line-height:1;font-family:'Times New Roman',serif}
.prob-eqs{display:flex;flex-direction:column;gap:6px}
.prob-eq{font-family:'Times New Roman',serif;font-style:italic;font-size:1.05rem;color:#fde68a}

.step-card{
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
  border-radius:12px;padding:12px 14px;margin-bottom:10px;
}
.step-title{font-size:.8rem;font-weight:700;color:#99f6e4;margin-bottom:8px;letter-spacing:.04em}
.step-desc{font-size:.9rem;color:#94a3b8;margin-bottom:10px;line-height:1.75}

.opts{display:flex;flex-wrap:wrap;gap:7px;margin-top:4px}
.opt-btn{
  padding:7px 15px;border-radius:20px;
  border:1px solid rgba(94,234,212,.2);background:rgba(94,234,212,.06);
  color:#ccfbf1;cursor:pointer;font-size:.88rem;transition:all .18s;font-family:inherit;
}
.opt-btn:hover:not(:disabled){background:rgba(13,148,136,.25);border-color:#14b8a6}
.opt-btn.correct{background:rgba(52,211,153,.15);color:#6ee7b7;border-color:#34d399}
.opt-btn.wrong  {background:rgba(248,113,113,.1); color:#fca5a5;border-color:#f87171}
.opt-btn:disabled{cursor:default;opacity:.75}
.fb{font-size:.87rem;margin-top:6px;min-height:18px;line-height:1.6}
.fb.ok{color:#6ee7b7}.fb.ng{color:#fca5a5}

.done-banner{
  background:linear-gradient(135deg,rgba(13,148,136,.18),rgba(15,118,110,.1));
  border:1px solid #0d9488;border-radius:14px;
  padding:14px;text-align:center;margin-bottom:12px;display:none;
}
.btn{padding:8px 20px;border-radius:10px;border:none;cursor:pointer;font-size:.9rem;font-weight:700;transition:.18s;font-family:inherit}
.btn-p{background:linear-gradient(135deg,#0d9488,#0f766e);color:#fff;box-shadow:0 3px 12px rgba(13,148,136,.3)}
.btn-p:hover{opacity:.88;transform:translateY(-1px)}

@media(max-width:600px){
  .hero h1{font-size:1.05rem}
  .prob-eq{font-size:.92rem}
  .opt-btn{font-size:.82rem;padding:6px 11px}
  .tabs{gap:4px}
  .tab-btn{font-size:.76rem;padding:9px 4px}
}
</style>
</head>
<body>
<div class="shell">

<!-- HERO -->
<section class="hero">
  <div class="hero-tag">📏 연립일차부등식 탐구</div>
  <h1>수직선 위에서 공통부분을 찾아라!</h1>
  <p>두 부등식의 해를 <strong>한 수직선 위에</strong> 함께 나타내고,
     겹치는 부분(공통부분)을 찾는 것이 연립부등식 풀이의 핵심입니다.</p>
</section>

<!-- TABS -->
<div class="tabs">
  <button class="tab-btn active" id="tbT1" onclick="showTab('t1')">🔬 수직선 탐구</button>
  <button class="tab-btn"        id="tbT2" onclick="showTab('t2')">🎯 단계별 풀기</button>
  <button class="tab-btn"        id="tbT3" onclick="showTab('t3')">📋 경우 정리</button>
</div>

<!-- ══════════════ TAB 1: 수직선 탐구 ══════════════ -->
<div class="tab-panel active" id="t1">

  <div class="card">
    <div class="card-title">🔬 슬라이더로 공통부분을 직접 확인해 보자!</div>
    <p style="font-size:.87rem;color:#94a3b8;margin-bottom:14px;line-height:1.7">
      경계값과 부등호 방향을 바꿔보면서 두 해가 어떻게 겹치는지 관찰하세요.
    </p>

    <!-- 부등식 1 -->
    <div style="margin-bottom:12px">
      <div style="font-size:.85rem;font-weight:700;color:#5eead4;margin-bottom:7px">
        ① 부등식 1 <span style="font-size:.73rem;color:#4b5563;font-weight:400">（청록색）</span>
      </div>
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px">
        <span style="font-family:'Times New Roman',serif;font-style:italic;color:#fde68a;font-size:1.1rem">x</span>
        <select id="op1" onchange="draw()">
          <option value="lt">&lt;</option>
          <option value="le" selected>≤</option>
          <option value="gt">&gt;</option>
          <option value="ge">≥</option>
        </select>
        <span id="v1lbl" style="font-size:1.1rem;font-weight:700;color:#fbbf24;min-width:24px;text-align:center">3</span>
      </div>
      <div class="slider-row">
        <span class="sl-label">경계값</span>
        <input type="range" id="b1" min="-8" max="8" step="1" value="3" oninput="draw()">
        <span class="sl-val" id="b1lbl">3</span>
      </div>
    </div>

    <!-- 부등식 2 -->
    <div style="margin-bottom:14px">
      <div style="font-size:.85rem;font-weight:700;color:#fb923c;margin-bottom:7px">
        ② 부등식 2 <span style="font-size:.73rem;color:#4b5563;font-weight:400">（주황색）</span>
      </div>
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px">
        <span style="font-family:'Times New Roman',serif;font-style:italic;color:#fde68a;font-size:1.1rem">x</span>
        <select id="op2" onchange="draw()">
          <option value="lt">&lt;</option>
          <option value="le">&lt;= </option>
          <option value="gt">&gt;</option>
          <option value="ge" selected>≥</option>
        </select>
        <span id="v2lbl" style="font-size:1.1rem;font-weight:700;color:#fbbf24;min-width:24px;text-align:center">1</span>
      </div>
      <div class="slider-row">
        <span class="sl-label">경계값</span>
        <input type="range" id="b2" min="-8" max="8" step="1" value="1" oninput="draw()">
        <span class="sl-val" id="b2lbl">1</span>
      </div>
    </div>

    <div class="canvas-wrap"><canvas id="nlCv" height="170"></canvas></div>
    <div id="resBadge" class="result-badge rb-ok">계산 중...</div>
  </div>

  <!-- 핵심 정리 -->
  <div class="card" style="border-color:rgba(94,234,212,.3)">
    <div class="card-title">📌 연립부등식 풀이 3단계</div>
    <div style="font-size:.93rem;line-height:2.1;color:#99f6e4">
      <div><span style="color:#fbbf24;font-weight:700">①</span> 각 부등식의 해를 따로 구한다.</div>
      <div><span style="color:#fbbf24;font-weight:700">②</span> 두 해를 <strong style="color:#fde68a">한 수직선 위에</strong> 함께 나타낸다.</div>
      <div><span style="color:#fbbf24;font-weight:700">③</span> 두 해의 <strong style="color:#5eead4">공통부분</strong>을 구한다.</div>
    </div>
    <div style="margin-top:12px;display:flex;flex-direction:column;gap:7px;font-size:.88rem">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="background:rgba(52,211,153,.15);color:#6ee7b7;border:1px solid rgba(52,211,153,.3);border-radius:6px;padding:2px 10px;font-weight:700;white-space:nowrap">공통부분 있음</span>
        <span style="color:#94a3b8">→ 겹치는 구간이 연립부등식의 해</span>
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        <span style="background:rgba(248,113,113,.15);color:#fca5a5;border:1px solid rgba(248,113,113,.3);border-radius:6px;padding:2px 10px;font-weight:700;white-space:nowrap">공통부분 없음</span>
        <span style="color:#94a3b8">→ 연립부등식의 해는 존재하지 않음</span>
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        <span style="background:rgba(251,191,36,.15);color:#fde68a;border:1px solid rgba(251,191,36,.3);border-radius:6px;padding:2px 10px;font-weight:700;white-space:nowrap">공통값 1개</span>
        <span style="color:#94a3b8">→ 등호로 표현 (예: x = 2)</span>
      </div>
    </div>
  </div>

</div><!-- t1 -->

<!-- ══════════════ TAB 2: 단계별 풀기 ══════════════ -->
<div class="tab-panel" id="t2">

  <div class="prob-tabs">
    <button class="prob-tab active" id="pt0" onclick="goProb(0)">문제 1</button>
    <button class="prob-tab"        id="pt1" onclick="goProb(1)">문제 2</button>
    <button class="prob-tab"        id="pt2" onclick="goProb(2)">문제 3</button>
    <button class="prob-tab"        id="pt3" onclick="goProb(3)">문제 4</button>
  </div>

  <!-- ─────── 문제 0 ─────── -->
  <div id="prob0">
    <div class="prob-header">
      <div class="prob-num">📝 연습 문제 1 — 연립부등식을 푸시오.</div>
      <div class="prob-sys">
        <span class="prob-brace">{</span>
        <div class="prob-eqs">
          <div class="prob-eq"><em>x</em> − 5 &lt; −2<em>x</em> + 4 &nbsp; …… ①</div>
          <div class="prob-eq">3<em>x</em> + 3 ≥ 4<em>x</em> + 2 &nbsp; …… ②</div>
        </div>
      </div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 1 — 부등식 ① 풀기</div>
      <div class="step-desc"><em style="color:#fde68a">x − 5 &lt; −2x + 4</em><br>x를 좌변으로, 수를 우변으로 이항하면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p0s1','A')" data-q="p0s1" data-v="A">x &lt; 9</button>
        <button class="opt-btn" onclick="ans('p0s1','B')" data-q="p0s1" data-v="B">x &lt; 3</button>
        <button class="opt-btn" onclick="ans('p0s1','C')" data-q="p0s1" data-v="C">x &gt; 3</button>
      </div>
      <div class="fb" id="p0s1fb"></div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 2 — 부등식 ② 풀기</div>
      <div class="step-desc"><em style="color:#fde68a">3x + 3 ≥ 4x + 2</em><br>x를 좌변으로, 수를 우변으로 이항하면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p0s2','A')" data-q="p0s2" data-v="A">x ≤ −1</button>
        <button class="opt-btn" onclick="ans('p0s2','B')" data-q="p0s2" data-v="B">x ≥ 1</button>
        <button class="opt-btn" onclick="ans('p0s2','C')" data-q="p0s2" data-v="C">x ≤ 1</button>
      </div>
      <div class="fb" id="p0s2fb"></div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 3 — 공통부분 찾기</div>
      <div class="step-desc">① x &lt; 3 &nbsp;&nbsp; ② x ≤ 1 &nbsp;&nbsp; 수직선에서 겹치는 부분은?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p0s3','A')" data-q="p0s3" data-v="A">x &lt; 3</button>
        <button class="opt-btn" onclick="ans('p0s3','B')" data-q="p0s3" data-v="B">x ≤ 1</button>
        <button class="opt-btn" onclick="ans('p0s3','C')" data-q="p0s3" data-v="C">1 ≤ x &lt; 3</button>
      </div>
      <div class="fb" id="p0s3fb"></div>
    </div>

    <div id="done0" class="done-banner">
      <div style="font-size:1.5rem;margin-bottom:4px">🎉</div>
      <div style="font-size:1.05rem;color:#5eead4;font-weight:700;margin-bottom:4px">완료!</div>
      <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">
        ① x&lt;3 &nbsp;② x≤1 → 공통부분: <strong style="color:#6ee7b7">x ≤ 1</strong>
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goProb(1)">다음 문제 →</button>
    </div>
  </div>

  <!-- ─────── 문제 1 ─────── -->
  <div id="prob1" style="display:none">
    <div class="prob-header">
      <div class="prob-num">📝 연습 문제 2 — 연립부등식을 푸시오.</div>
      <div class="prob-sys">
        <span class="prob-brace">{</span>
        <div class="prob-eqs">
          <div class="prob-eq">2(<em>x</em> + 1) &gt; <em>x</em> − 4 &nbsp; …… ①</div>
          <div class="prob-eq">3 − <em>x</em> ≥ 3<em>x</em> − 5 &nbsp; …… ②</div>
        </div>
      </div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 1 — 부등식 ① 풀기</div>
      <div class="step-desc"><em style="color:#fde68a">2(x+1) &gt; x−4</em><br>괄호를 풀면 2x+2&gt;x−4, 이항하면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p1s1','A')" data-q="p1s1" data-v="A">x &gt; −6</button>
        <button class="opt-btn" onclick="ans('p1s1','B')" data-q="p1s1" data-v="B">x &lt; −6</button>
        <button class="opt-btn" onclick="ans('p1s1','C')" data-q="p1s1" data-v="C">x &gt; 6</button>
      </div>
      <div class="fb" id="p1s1fb"></div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 2 — 부등식 ② 풀기</div>
      <div class="step-desc"><em style="color:#fde68a">3−x ≥ 3x−5</em><br>x를 한쪽으로 모으면? (음수 계수 주의!)</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p1s2','A')" data-q="p1s2" data-v="A">x ≥ 2</button>
        <button class="opt-btn" onclick="ans('p1s2','B')" data-q="p1s2" data-v="B">x ≤ 8</button>
        <button class="opt-btn" onclick="ans('p1s2','C')" data-q="p1s2" data-v="C">x ≤ 2</button>
      </div>
      <div class="fb" id="p1s2fb"></div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 3 — 공통부분 찾기</div>
      <div class="step-desc">① x &gt; −6 &nbsp;&nbsp; ② x ≤ 2 &nbsp;&nbsp; 겹치는 부분은?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p1s3','A')" data-q="p1s3" data-v="A">x &gt; −6</button>
        <button class="opt-btn" onclick="ans('p1s3','B')" data-q="p1s3" data-v="B">−6 &lt; x ≤ 2</button>
        <button class="opt-btn" onclick="ans('p1s3','C')" data-q="p1s3" data-v="C">x ≤ 2</button>
      </div>
      <div class="fb" id="p1s3fb"></div>
    </div>

    <div id="done1" class="done-banner">
      <div style="font-size:1.5rem;margin-bottom:4px">🎉</div>
      <div style="font-size:1.05rem;color:#5eead4;font-weight:700;margin-bottom:4px">완료!</div>
      <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">
        ① x&gt;−6 &nbsp;② x≤2 → 공통부분: <strong style="color:#6ee7b7">−6 &lt; x ≤ 2</strong>
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goProb(2)">다음 문제 →</button>
    </div>
  </div>

  <!-- ─────── 문제 2 ─────── -->
  <div id="prob2" style="display:none">
    <div class="prob-header">
      <div class="prob-num">📝 연습 문제 3 — 연립부등식을 푸시오.</div>
      <div class="prob-sys">
        <span class="prob-brace">{</span>
        <div class="prob-eqs">
          <div class="prob-eq">2<em>x</em> − 3 &lt; −1 &nbsp; …… ①</div>
          <div class="prob-eq"><em>x</em> + 2 ≥ −<em>x</em> + 6 &nbsp; …… ②</div>
        </div>
      </div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 1 — 부등식 ① 풀기</div>
      <div class="step-desc"><em style="color:#fde68a">2x − 3 &lt; −1</em><br>이항하면 2x &lt; ? → x &lt; ?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p2s1','A')" data-q="p2s1" data-v="A">x &lt; −2</button>
        <button class="opt-btn" onclick="ans('p2s1','B')" data-q="p2s1" data-v="B">x &lt; 1</button>
        <button class="opt-btn" onclick="ans('p2s1','C')" data-q="p2s1" data-v="C">x &lt; 2</button>
      </div>
      <div class="fb" id="p2s1fb"></div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 2 — 부등식 ② 풀기</div>
      <div class="step-desc"><em style="color:#fde68a">x + 2 ≥ −x + 6</em><br>x를 한쪽으로 모으면?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p2s2','A')" data-q="p2s2" data-v="A">x ≥ 4</button>
        <button class="opt-btn" onclick="ans('p2s2','B')" data-q="p2s2" data-v="B">x ≤ 2</button>
        <button class="opt-btn" onclick="ans('p2s2','C')" data-q="p2s2" data-v="C">x ≥ 2</button>
      </div>
      <div class="fb" id="p2s2fb"></div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 3 — 공통부분 찾기</div>
      <div class="step-desc">① x &lt; 1 &nbsp;&nbsp; ② x ≥ 2 &nbsp;&nbsp; 수직선에서 겹치는 부분은?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p2s3','A')" data-q="p2s3" data-v="A">1 ≤ x &lt; 2</button>
        <button class="opt-btn" onclick="ans('p2s3','B')" data-q="p2s3" data-v="B">해 없음</button>
        <button class="opt-btn" onclick="ans('p2s3','C')" data-q="p2s3" data-v="C">x &lt; 1</button>
      </div>
      <div class="fb" id="p2s3fb"></div>
    </div>

    <div id="done2" class="done-banner">
      <div style="font-size:1.5rem;margin-bottom:4px">🎉</div>
      <div style="font-size:1.05rem;color:#5eead4;font-weight:700;margin-bottom:4px">완료!</div>
      <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">
        ① x&lt;1 &nbsp;② x≥2 → 공통부분 없음 → <strong style="color:#fca5a5">해가 없습니다</strong>
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goProb(3)">다음 문제 →</button>
    </div>
  </div>

  <!-- ─────── 문제 3 ─────── -->
  <div id="prob3" style="display:none">
    <div class="prob-header">
      <div class="prob-num">📝 연습 문제 4 — 연립부등식을 푸시오.</div>
      <div class="prob-sys">
        <span class="prob-brace">{</span>
        <div class="prob-eqs">
          <div class="prob-eq">4 − <em>x</em> ≥ 2<em>x</em> − 5 &nbsp; …… ①</div>
          <div class="prob-eq">5<em>x</em> − 5 ≥ 3<em>x</em> + 1 &nbsp; …… ②</div>
        </div>
      </div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 1 — 부등식 ① 풀기</div>
      <div class="step-desc"><em style="color:#fde68a">4−x ≥ 2x−5</em><br>이항 후 −3x ≥ −9, 양변을 −3으로 나누면? (부등호 방향 주의!)</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p3s1','A')" data-q="p3s1" data-v="A">x ≥ 3</button>
        <button class="opt-btn" onclick="ans('p3s1','B')" data-q="p3s1" data-v="B">x ≤ −3</button>
        <button class="opt-btn" onclick="ans('p3s1','C')" data-q="p3s1" data-v="C">x ≤ 3</button>
      </div>
      <div class="fb" id="p3s1fb"></div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 2 — 부등식 ② 풀기</div>
      <div class="step-desc"><em style="color:#fde68a">5x−5 ≥ 3x+1</em><br>이항 후 2x ≥ 6, x ≥ ?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p3s2','A')" data-q="p3s2" data-v="A">x ≥ 3</button>
        <button class="opt-btn" onclick="ans('p3s2','B')" data-q="p3s2" data-v="B">x ≥ −2</button>
        <button class="opt-btn" onclick="ans('p3s2','C')" data-q="p3s2" data-v="C">x ≤ 3</button>
      </div>
      <div class="fb" id="p3s2fb"></div>
    </div>

    <div class="step-card">
      <div class="step-title">STEP 3 — 공통부분 찾기</div>
      <div class="step-desc">① x ≤ 3 &nbsp;&nbsp; ② x ≥ 3 &nbsp;&nbsp; 수직선에서 겹치는 부분은?</div>
      <div class="opts">
        <button class="opt-btn" onclick="ans('p3s3','A')" data-q="p3s3" data-v="A">x = 3</button>
        <button class="opt-btn" onclick="ans('p3s3','B')" data-q="p3s3" data-v="B">해 없음</button>
        <button class="opt-btn" onclick="ans('p3s3','C')" data-q="p3s3" data-v="C">모든 실수</button>
      </div>
      <div class="fb" id="p3s3fb"></div>
    </div>

    <div id="done3" class="done-banner">
      <div style="font-size:1.5rem;margin-bottom:4px">🏆</div>
      <div style="font-size:1.05rem;color:#5eead4;font-weight:700;margin-bottom:4px">4문제 전부 완료! 훌륭해요!</div>
      <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">
        ① x≤3 &nbsp;② x≥3 → 딱 1점에서 만남 → <strong style="color:#fde68a">x = 3</strong>
      </p>
    </div>
  </div>

</div><!-- t2 -->

<!-- ══════════════ TAB 3: 경우 정리 ══════════════ -->
<div class="tab-panel" id="t3">

  <div class="card">
    <div class="card-title">📋 <em>a</em> &lt; <em>b</em> 일 때 — 4가지 패턴</div>
    <p style="font-size:.87rem;color:#94a3b8;margin-bottom:12px;line-height:1.7">
      두 부등식 해의 방향과 경계에 따라 공통부분이 달라집니다. 수직선으로 확인하세요!
    </p>
    <div class="cases-grid" id="casesGrid"></div>
  </div>

  <div class="card" style="background:rgba(251,191,36,.05);border-color:rgba(251,191,36,.22)">
    <div class="card-title" style="color:#fbbf24">⚠️ 특수한 경우 꼭 기억!</div>
    <div style="display:flex;flex-direction:column;gap:10px;font-size:.9rem">
      <div style="display:flex;align-items:flex-start;gap:10px">
        <span style="background:rgba(248,113,113,.15);color:#fca5a5;border:1px solid rgba(248,113,113,.3);border-radius:6px;padding:3px 10px;font-weight:700;min-width:90px;text-align:center;flex-shrink:0">해 없음</span>
        <span style="color:#94a3b8;line-height:1.7">두 해가 수직선에서 전혀 겹치지 않을 때<br>→ 연립부등식의 <strong style="color:#fca5a5">해는 존재하지 않습니다</strong></span>
      </div>
      <div style="display:flex;align-items:flex-start;gap:10px">
        <span style="background:rgba(251,191,36,.15);color:#fde68a;border:1px solid rgba(251,191,36,.3);border-radius:6px;padding:3px 10px;font-weight:700;min-width:90px;text-align:center;flex-shrink:0">한 점만</span>
        <span style="color:#94a3b8;line-height:1.7">두 해가 딱 한 점에서만 만날 때<br>→ 해를 <strong style="color:#fde68a">등호로 표현</strong> (예: x = 2)</span>
      </div>
    </div>
  </div>

</div><!-- t3 -->

</div><!-- shell -->
<script>
/* ── 높이 자동조절 ── */
function notifyH(){
  var h=Math.max(document.body.scrollHeight,document.documentElement.scrollHeight)+40;
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
new ResizeObserver(function(){notifyH();}).observe(document.body);
window.addEventListener('load',function(){
  draw();
  drawCases();
  setTimeout(notifyH,150);
});

/* ── 탭 전환 ── */
function showTab(name){
  ['t1','t2','t3'].forEach(function(id){
    document.getElementById(id).classList.toggle('active',id===name);
  });
  document.getElementById('tbT1').classList.toggle('active',name==='t1');
  document.getElementById('tbT2').classList.toggle('active',name==='t2');
  document.getElementById('tbT3').classList.toggle('active',name==='t3');
  setTimeout(notifyH,80);
}

/* ── 문제 전환 ── */
function goProb(n){
  for(var i=0;i<4;i++){
    document.getElementById('prob'+i).style.display=i===n?'block':'none';
    document.getElementById('pt'+i).classList.toggle('active',i===n);
  }
  setTimeout(notifyH,60);
}

/* ════════════ 구간 계산 헬퍼 ════════════ */
function toIv(op,b){
  if(op==='lt') return {lo:null,loI:false,hi:b,  hiI:false};
  if(op==='le') return {lo:null,loI:false,hi:b,  hiI:true};
  if(op==='gt') return {lo:b,  loI:false,hi:null,hiI:false};
  if(op==='ge') return {lo:b,  loI:true, hi:null,hiI:false};
}
function intersect(op1,b1,op2,b2){
  var a=toIv(op1,b1), c=toIv(op2,b2);
  var lo,loI,hi,hiI;
  if(a.lo===null&&c.lo===null){lo=null;loI=false;}
  else if(a.lo===null){lo=c.lo;loI=c.loI;}
  else if(c.lo===null){lo=a.lo;loI=a.loI;}
  else if(a.lo>c.lo){lo=a.lo;loI=a.loI;}
  else if(c.lo>a.lo){lo=c.lo;loI=c.loI;}
  else{lo=a.lo;loI=a.loI&&c.loI;}
  if(a.hi===null&&c.hi===null){hi=null;hiI=false;}
  else if(a.hi===null){hi=c.hi;hiI=c.hiI;}
  else if(c.hi===null){hi=a.hi;hiI=a.hiI;}
  else if(a.hi<c.hi){hi=a.hi;hiI=a.hiI;}
  else if(c.hi<a.hi){hi=c.hi;hiI=c.hiI;}
  else{hi=a.hi;hiI=a.hiI&&c.hiI;}
  if(lo!==null&&hi!==null){
    if(lo>hi) return null;
    if(lo===hi) return (loI&&hiI)?{type:'pt',val:lo}:null;
  }
  return {type:'iv',lo:lo,loI:loI,hi:hi,hiI:hiI};
}
function fmtIv(r){
  if(!r) return '해 없음';
  if(r.type==='pt') return 'x = '+r.val;
  var s='';
  if(r.lo!==null) s+=(r.loI?r.lo+' ≤ ':r.lo+' < ');
  s+='x';
  if(r.hi!==null) s+=(r.hiI?' ≤ ':' < ')+r.hi;
  return s;
}
function fmtSingle(op,b){
  var sym={lt:'<',le:'≤',gt:'>',ge:'≥'}[op];
  return 'x '+sym+' '+b;
}

/* ════════════ 수직선 그리기 공통 ════════════ */
function drawNL(cv,op1,b1,op2,b2,res,H,xMin,xMax,showLabels){
  var W=cv.offsetWidth||600;
  cv.width=W; cv.height=H;
  var ctx=cv.getContext('2d');
  ctx.clearRect(0,0,W,H);
  function tx(v){return (v-xMin)/(xMax-xMin)*W;}

  // showLabels: 0=없음, 1=점 숫자만, 2=전체(row레이블+축눈금)
  var full=showLabels===2||showLabels===true;
  var dots=showLabels>=1||showLabels===true;
  var rows=full?[H*.2,H*.5,H*.8]:[H*.22,H*.55,H*.85];

  function axis(y,col){
    ctx.strokeStyle=col||'rgba(255,255,255,.2)';ctx.lineWidth=1.2;
    ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();
    ctx.beginPath();ctx.moveTo(W-2,y);ctx.lineTo(W-10,y-4);ctx.lineTo(W-10,y+4);ctx.closePath();
    ctx.fillStyle=col||'rgba(255,255,255,.2)';ctx.fill();
    if(full){
      ctx.fillStyle='rgba(255,255,255,.28)';ctx.font='10px sans-serif';ctx.textAlign='center';
      for(var i=xMin+1;i<xMax;i++){
        ctx.beginPath();ctx.moveTo(tx(i),y-3);ctx.lineTo(tx(i),y+3);ctx.stroke();
        if(i%2===0) ctx.fillText(i,tx(i),y+14);
      }
    }
  }

  function bar(iv,y,col,thick){
    var x1=iv.lo===null?0:tx(iv.lo);
    var x2=iv.hi===null?W:tx(iv.hi);
    ctx.globalAlpha=.5;ctx.fillStyle=col;
    ctx.fillRect(x1,y-thick/2,x2-x1,thick);
    ctx.globalAlpha=1;
    [[iv.lo,iv.loI],[iv.hi,iv.hiI]].forEach(function(e){
      if(e[0]===null) return;
      ctx.beginPath();ctx.arc(tx(e[0]),y,5,0,Math.PI*2);
      ctx.fillStyle=e[1]?col:'#071515';ctx.fill();
      ctx.strokeStyle=col;ctx.lineWidth=2;ctx.stroke();
      if(dots){
        ctx.fillStyle=col;ctx.font='bold 10px sans-serif';ctx.textAlign='center';
        ctx.fillText(e[0],tx(e[0]),y-9);
      }
    });
  }

  var iv1=toIv(op1,b1),iv2=toIv(op2,b2);

  axis(rows[0],'rgba(94,234,212,.35)');
  bar(iv1,rows[0],'#5eead4',7);
  if(full){
    ctx.fillStyle='#5eead4';ctx.font='bold 10px sans-serif';ctx.textAlign='left';
    ctx.fillText('① '+fmtSingle(op1,b1),4,rows[0]-15);
  }

  axis(rows[1],'rgba(251,146,60,.35)');
  bar(iv2,rows[1],'#fb923c',7);
  if(full){
    ctx.fillStyle='#fb923c';ctx.font='bold 10px sans-serif';ctx.textAlign='left';
    ctx.fillText('② '+fmtSingle(op2,b2),4,rows[1]-15);
  }

  axis(rows[2],'rgba(52,211,153,.25)');
  if(full){
    ctx.fillStyle='#34d399';ctx.font='bold 10px sans-serif';ctx.textAlign='left';
    ctx.fillText('공통부분',4,rows[2]-15);
  }

  if(res===null){
    ctx.fillStyle='#fca5a5';ctx.font='bold 11px sans-serif';ctx.textAlign='center';
    ctx.fillText('없음',W/2,rows[2]+5);
  } else if(res.type==='pt'){
    ctx.beginPath();ctx.arc(tx(res.val),rows[2],6,0,Math.PI*2);
    ctx.fillStyle='#fbbf24';ctx.fill();
    ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
    if(dots){
      ctx.fillStyle='#fbbf24';ctx.font='bold 10px sans-serif';ctx.textAlign='center';
      ctx.fillText('x='+res.val,tx(res.val),rows[2]-11);
    }
  } else {
    bar(res,rows[2],'#34d399',9);
  }
}

/* ════════════ TAB1: 수직선 탐구 ════════════ */
function draw(){
  var b1=parseInt(document.getElementById('b1').value);
  var b2=parseInt(document.getElementById('b2').value);
  var op1=document.getElementById('op1').value;
  var op2=document.getElementById('op2').value;
  document.getElementById('v1lbl').textContent=b1;
  document.getElementById('b1lbl').textContent=b1;
  document.getElementById('v2lbl').textContent=b2;
  document.getElementById('b2lbl').textContent=b2;

  var res=intersect(op1,b1,op2,b2);
  var badge=document.getElementById('resBadge');
  var s1=fmtSingle(op1,b1), s2=fmtSingle(op2,b2);

  if(res===null){
    badge.className='result-badge rb-none';
    badge.innerHTML='<strong>①</strong> '+s1+' &nbsp;∩&nbsp; <strong>②</strong> '+s2+' &nbsp;→&nbsp; <strong style="color:#fca5a5">공통부분 없음 (해 없음)</strong>';
  } else if(res.type==='pt'){
    badge.className='result-badge rb-pt';
    badge.innerHTML='<strong>①</strong> '+s1+' &nbsp;∩&nbsp; <strong>②</strong> '+s2+' &nbsp;→&nbsp; <strong style="color:#fde68a">'+fmtIv(res)+'</strong>';
  } else {
    badge.className='result-badge rb-ok';
    badge.innerHTML='<strong>①</strong> '+s1+' &nbsp;∩&nbsp; <strong>②</strong> '+s2+' &nbsp;→&nbsp; <strong style="color:#6ee7b7">'+fmtIv(res)+'</strong>';
  }

  var cv=document.getElementById('nlCv');
  drawNL(cv,op1,b1,op2,b2,res,170,-9,9,2);
  setTimeout(notifyH,30);
}

/* ════════════ TAB3: 경우 정리 ════════════ */
function drawCases(){
  var CASES=[
    {lbl:'경우 1',sys:'{x &lt; a,  x &gt; b}',op1:'lt',b1:2,op2:'gt',b2:5,rc:'cr-none'},
    {lbl:'경우 2',sys:'{x &lt; a,  x ≥ b}', op1:'lt',b1:5,op2:'ge',b2:2,rc:'cr-ok'},
    {lbl:'경우 3',sys:'{x ≤ a,  x &gt; b}', op1:'le',b1:5,op2:'gt',b2:2,rc:'cr-ok'},
    {lbl:'경우 4',sys:'{x ≤ a,  x ≥ b}', op1:'le',b1:5,op2:'ge',b2:2,rc:'cr-ok'},
    {lbl:'특수 — 해 없음',sys:'예: x &lt; 3, x ≥ 5',op1:'lt',b1:3,op2:'ge',b2:5,rc:'cr-none'},
    {lbl:'특수 — 한 점', sys:'예: x ≤ 3, x ≥ 3', op1:'le',b1:3,op2:'ge',b2:3,rc:'cr-pt'},
  ];
  var grid=document.getElementById('casesGrid');
  grid.innerHTML='';
  CASES.forEach(function(c,idx){
    var cid='ccv'+idx;
    var r=intersect(c.op1,c.b1,c.op2,c.b2);
    var resText=r===null?'해 없음':r.type==='pt'?fmtIv(r):fmtIv(r);
    var div=document.createElement('div');
    div.className='case-card';
    div.innerHTML='<div class="case-label">'+c.lbl+'</div>'+
      '<div class="case-sys">'+c.sys+'</div>'+
      '<div class="case-canvas-wrap"><canvas id="'+cid+'" height="80"></canvas></div>'+
      '<span class="case-result '+c.rc+'">'+resText+'</span>';
    grid.appendChild(div);
    setTimeout((function(cid2,c2){return function(){
      var cv=document.getElementById(cid2);
      if(!cv) return;
      var r2=intersect(c2.op1,c2.b1,c2.op2,c2.b2);
      drawNL(cv,c2.op1,c2.b1,c2.op2,c2.b2,r2,80,0,8,1);
    };})(cid,c),30);
  });
}

/* ════════════ 연습 문제 정답 ════════════ */
var CORRECT={
  p0s1:'B',p0s2:'C',p0s3:'B',
  p1s1:'A',p1s2:'C',p1s3:'B',
  p2s1:'B',p2s2:'C',p2s3:'B',
  p3s1:'C',p3s2:'A',p3s3:'A',
};
var HINTS={
  p0s1:{
    A:'✗ x항: x+2x=3x → 3x<9 → x<3이에요.',
    B:'✓ 정답! x−5<−2x+4 → 3x<9 → x<3',
    C:'✗ 이항 후 계수가 양수이면 부등호 방향은 그대로예요.',
  },
  p0s2:{
    A:'✗ 3x−4x=−x, 수 이항: 3−2=1 → −x≥−1 → x≤1이에요.',
    B:'✗ 3x−4x=−x이므로 −x≥−1 → x≤1이에요.',
    C:'✓ 정답! 3x+3≥4x+2 → −x≥−1 → x≤1',
  },
  p0s3:{
    A:'✗ x<3이고 x≤1의 교집합에서 1이 3보다 작으므로 더 좁은 쪽을 취해요.',
    B:'✓ 정답! x<3이고 x≤1의 공통 → x≤1',
    C:'✗ 1≤x<3은 ②의 해 x≤1에 포함되지 않아요.',
  },
  p1s1:{
    A:'✓ 정답! 2x+2>x−4 → x>−6',
    B:'✗ 이항 후 x>? → x>−6이에요. 부등호 방향 확인!',
    C:'✗ 2x+2>x−4 → x>−4−2=−6이에요.',
  },
  p1s2:{
    A:'✗ 3−x≥3x−5 → −4x≥−8 → x≤2예요. ≥가 아니에요.',
    B:'✗ 이항하면 −4x≥−8 → 양변을 −4로 나누면 부등호 방향 바뀜 → x≤2예요.',
    C:'✓ 정답! 3−x≥3x−5 → −4x≥−8 → x≤2',
  },
  p1s3:{
    A:'✗ x>−6만 있으면 ② 조건이 빠져요. 두 조건을 모두 만족해야 해요.',
    B:'✓ 정답! x>−6이고 x≤2의 공통 → −6<x≤2',
    C:'✗ x≤2만 있으면 x>−6 조건이 빠져요.',
  },
  p2s1:{
    A:'✗ 2x<−1+3=2 → x<1이에요.',
    B:'✓ 정답! 2x−3<−1 → 2x<2 → x<1',
    C:'✗ 2x<2에서 2로 나누면 x<1이에요.',
  },
  p2s2:{
    A:'✗ x+x≥6−2=4 → 2x≥4 → x≥2이에요.',
    B:'✗ 이항하면 2x≥4 → x≥2예요.',
    C:'✓ 정답! x+2≥−x+6 → 2x≥4 → x≥2',
  },
  p2s3:{
    A:'✗ x<1이고 x≥2를 동시에 만족하는 x가 있나요? 수직선을 그려보세요!',
    B:'✓ 정답! x<1과 x≥2는 수직선에서 겹치지 않아요 → 해 없음!',
    C:'✗ x<1만 고려하면 ② 조건이 빠져요.',
  },
  p3s1:{
    A:'✗ −3x≥−9를 −3으로 나누면 부등호 방향이 바뀌어요 → x≤3이에요.',
    B:'✗ −3x≥−9에서 양변을 −3으로 나누면 x≤3이에요.',
    C:'✓ 정답! 4−x≥2x−5 → −3x≥−9 → x≤3',
  },
  p3s2:{
    A:'✓ 정답! 5x−3x≥1+5 → 2x≥6 → x≥3',
    B:'✗ 5x−5≥3x+1 → 2x≥6 → x≥3이에요.',
    C:'✗ x항 계수가 양수이므로 부등호 방향은 그대로예요.',
  },
  p3s3:{
    A:'✓ 정답! x≤3이고 x≥3의 공통 → x=3 (딱 한 점!)',
    B:'✗ 두 범위가 경계값 3에서 만나요! 해가 없는 게 아니에요.',
    C:'✗ x≤3이면서 x≥3인 범위는 딱 x=3뿐이에요.',
  },
};

var answered={};
var probKeys={0:['p0s1','p0s2','p0s3'],1:['p1s1','p1s2','p1s3'],2:['p2s1','p2s2','p2s3'],3:['p3s1','p3s2','p3s3']};

function ans(q,v){
  if(answered[q]) return;
  answered[q]=v;
  var ok=CORRECT[q]===v;
  var fb=document.getElementById(q+'fb');
  fb.className='fb '+(ok?'ok':'ng');
  fb.innerHTML=(HINTS[q]&&HINTS[q][v])||(ok?'✓ 정답!':'✗ 다시 시도!');
  document.querySelectorAll('[data-q="'+q+'"]').forEach(function(btn){
    btn.disabled=true;
    if(btn.dataset.v===CORRECT[q]) btn.classList.add('correct');
    else if(btn.dataset.v===v&&!ok) btn.classList.add('wrong');
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
    components.html(_HTML, height=1600, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
