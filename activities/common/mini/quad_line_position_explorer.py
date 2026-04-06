# activities/common/mini/quad_line_position_explorer.py
"""
이차함수 그래프와 직선의 위치관계 탐구 실험실
이차함수 y=ax²+bx+c와 직선 y=mx+n의 위치관계를
판별식 D=(b-m)²-4a(c-n)로 탐구합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "이차함수직선위치관계"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "판별식연결",
        "label":  "이차함수 y=ax²+bx+c와 직선 y=mx+n의 위치관계를 왜 판별식으로 판단할 수 있는지, 연립방정식을 세우는 과정과 연결하여 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "D등호조건",
        "label":  "D=0일 때 '접한다'는 것이 기하학적으로 무슨 의미인지, D>0, D<0과 비교하여 설명하세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "k범위풀이",
        "label":  "연습문제 중 하나를 골라 풀이 과정을 쓰고, 판별식을 어떻게 활용했는지 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "항상두점",
        "label":  "생각 넓히기에서 y=x²−2x+1의 그래프와 y=kx+4는 k의 값에 관계없이 항상 두 점에서 만납니다. 이것이 왜 성립하는지 판별식 또는 그래프를 이용하여 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "새롭게알게된점",
        "label":  "💡 이 활동을 통해 새롭게 알게 된 점",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "느낀점",
        "label":  "💬 이 활동을 하면서 느낀 점",
        "type":   "text_area",
        "height": 90,
    },
]

META = {
    "title":       "📐 이차함수·직선 위치관계 실험실",
    "description": "이차함수 그래프와 직선의 위치관계(두 점·접함·만나지 않음)를 판별식으로 탐구하고, k 범위 문제까지 익히는 인터랙티브 활동입니다.",
    "order":       235,
    "hidden":      False,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>이차함수와 직선의 위치관계</title>
<style>
html { font-size: 16px; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', system-ui, sans-serif;
  background: linear-gradient(155deg, #060917 0%, #0e1630 60%, #080f1c 100%);
  color: #e2e8ff;
  padding: 14px 12px 28px;
  min-height: 100vh;
}

/* ── Main Tabs ── */
.tabs { display: flex; gap: 6px; margin-bottom: 16px; }
.tab {
  flex: 1; padding: 10px 4px;
  border: none; border-radius: 10px; cursor: pointer;
  font-size: .92rem; font-weight: 700; letter-spacing: -.3px;
  background: rgba(255,255,255,.06); color: #94a3b8;
  transition: background .2s, color .2s;
}
.tab.active { background: #4f46e5; color: #fff; }
.tab:hover:not(.active) { background: rgba(79,70,229,.25); color: #c7d2fe; }

/* ── Practice Sub-tabs ── */
.sub-tabs { display: flex; gap: 4px; margin-bottom: 14px; }
.sub-tab {
  flex: 1; padding: 8px 4px;
  border: none; border-radius: 8px; cursor: pointer;
  font-size: .88rem; font-weight: 700;
  background: rgba(255,255,255,.05); color: #94a3b8;
  transition: background .2s, color .2s;
}
.sub-tab.active { background: #6d28d9; color: #fff; }
.sub-tab:hover:not(.active) { background: rgba(109,40,217,.25); color: #c4b5fd; }

/* ── Cards ── */
.card {
  background: rgba(255,255,255,.05);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 14px;
  padding: 16px 14px;
  margin-bottom: 14px;
}
.card-title { font-size: 1.05rem; font-weight: 700; color: #a5b4fc; margin-bottom: 10px; }

/* ── Sliders ── */
.slider-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }
.slider-label { min-width: 60px; font-size: .95rem; color: #c7d2fe; font-weight: 600; }
input[type=range] { flex: 1; min-width: 120px; accent-color: #818cf8; cursor: pointer; }
.slider-val { min-width: 36px; text-align: right; font-size: .95rem; color: #fde68a; font-weight: 700; }

/* ── Canvas ── */
.canvas-wrap { position: relative; background: #0a0f23; border-radius: 12px; overflow: hidden; margin-bottom: 12px; }
canvas { display: block; width: 100%; }

/* ── D-badge ── */
.d-badge {
  display: inline-block; padding: 6px 16px; border-radius: 20px;
  font-size: 1rem; font-weight: 700; margin: 8px 0;
  transition: background .3s, color .3s;
}
.d-pos  { background: #14532d; color: #86efac; border: 1px solid #4ade80; }
.d-zero { background: #713f12; color: #fde68a; border: 1px solid #fbbf24; }
.d-neg  { background: #4c0519; color: #fca5a5; border: 1px solid #f87171; }

/* ── Equation display ── */
.eq-box {
  background: rgba(79,70,229,.12); border: 1px solid rgba(99,102,241,.3);
  border-radius: 10px; padding: 10px 14px; font-size: .97rem;
  line-height: 2; margin-bottom: 10px; color: #c7d2fe;
}
.eq-box em   { color: #fde68a; font-style: normal; font-weight: 700; }
.eq-box .red   { color: #f87171; font-weight: 700; }
.eq-box .green { color: #86efac; font-weight: 700; }
.eq-box .gold  { color: #fcd34d; font-weight: 700; }

/* ── Practice ── */
.prob-card {
  background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.1);
  border-radius: 14px; padding: 16px 14px; margin-bottom: 14px;
}
.prob-num { font-size: .88rem; font-weight: 700; color: #818cf8; margin-bottom: 8px; }
.prob-text { font-size: 1rem; line-height: 1.8; margin-bottom: 12px; color: #e2e8ff; }
.sub-q { margin-bottom: 12px; }
.sub-q label { font-size: .97rem; color: #c7d2fe; display: block; margin-bottom: 6px; }
.opts { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }
.opt-btn {
  padding: 7px 16px; border-radius: 20px;
  border: 1px solid rgba(255,255,255,.2); background: rgba(255,255,255,.05);
  color: #e2e8ff; cursor: pointer; font-size: .93rem; transition: all .2s;
}
.opt-btn:hover { background: rgba(99,102,241,.25); border-color: #818cf8; }
.opt-btn.correct { background: #14532d; color: #86efac; border-color: #4ade80; }
.opt-btn.wrong   { background: #4c0519; color: #fca5a5; border-color: #f87171; }
.opt-btn:disabled { cursor: default; opacity: .75; }

.fb { font-size: .9rem; margin-top: 6px; min-height: 20px; }
.fb.ok { color: #86efac; }
.fb.ng { color: #fca5a5; }

/* ── Challenge layout ── */
.chall-layout { display: flex; gap: 14px; flex-wrap: wrap; align-items: flex-start; }
.chall-questions { flex: 1; min-width: 240px; }
.chall-graph-panel {
  flex: 0 0 260px; background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.1); border-radius: 12px;
  padding: 12px 10px;
}
.chall-canvas-wrap { background: #0a0f23; border-radius: 8px; overflow: hidden; margin-bottom: 8px; }
.chall-canvas-wrap canvas { display: block; width: 100%; }

/* ── Challenge hint ── */
.challenge-hint {
  background: rgba(250,204,21,.07); border: 1px solid rgba(250,204,21,.25);
  border-radius: 10px; padding: 10px 14px; font-size: .93rem;
  color: #fde68a; line-height: 1.8; margin-bottom: 12px; display: none;
}

/* ── Buttons ── */
.btn { padding: 9px 22px; border-radius: 22px; border: none; cursor: pointer; font-size: .95rem; font-weight: 700; transition: opacity .2s; }
.btn:hover { opacity: .85; }
.btn-p { background: #4f46e5; color: #fff; }
.btn-o { background: rgba(255,255,255,.08); color: #a5b4fc; border: 1px solid #4f46e5; }

/* ── Done banner ── */
.done-banner {
  background: linear-gradient(135deg,rgba(79,70,229,.3),rgba(109,40,217,.3));
  border: 1px solid #6d28d9; border-radius: 14px;
  padding: 18px 16px; text-align: center; margin-bottom: 14px;
}

.hidden { display: none; }
</style>
</head>
<body>

<!-- Main Tabs -->
<div class="tabs">
  <button class="tab active" onclick="goTab(0)">🔬 그래프 탐구</button>
  <button class="tab" onclick="goTab(1)">✏️ 연습문제</button>
  <button class="tab" onclick="goTab(2)">🌟 생각 넓히기</button>
</div>

<!-- ══════════════════════ TAB 0: 그래프 탐구 ══════════════════════ -->
<div id="tab0">

  <div class="card">
    <div class="card-title">🔬 이차함수와 직선을 직접 움직여 보자!</div>
    <p style="font-size:.93rem;color:#94a3b8;margin-bottom:12px">
      슬라이더를 조절해서 이차함수와 직선의 위치관계가 어떻게 바뀌는지 관찰하세요.
    </p>
    <div class="canvas-wrap"><canvas id="gc" height="300"></canvas></div>
    <div id="dBadge" class="d-badge d-pos">D = … 계산 중</div>

    <div style="margin-top:12px;margin-bottom:4px;font-size:.88rem;color:#818cf8;font-weight:700">
      📈 이차함수  y = x² + bx + c  (a=1 고정)
    </div>
    <div class="slider-row">
      <span class="slider-label">b =</span>
      <input type="range" id="sb" min="-6" max="6" step="0.5" value="-2" oninput="drawGraph()">
      <span class="slider-val" id="vb">-2</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">c =</span>
      <input type="range" id="sc" min="-8" max="8" step="0.5" value="1" oninput="drawGraph()">
      <span class="slider-val" id="vc">1</span>
    </div>
    <div style="margin-top:10px;margin-bottom:4px;font-size:.88rem;color:#f472b6;font-weight:700">
      📏 직선  y = mx + n
    </div>
    <div class="slider-row">
      <span class="slider-label">m =</span>
      <input type="range" id="sm" min="-6" max="6" step="0.5" value="1" oninput="drawGraph()">
      <span class="slider-val" id="vm">1</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">n =</span>
      <input type="range" id="sn" min="-10" max="10" step="0.5" value="-2" oninput="drawGraph()">
      <span class="slider-val" id="vn">-2</span>
    </div>
  </div>

  <div class="card">
    <div class="card-title">🧮 판별식으로 위치관계 판단하기</div>
    <div class="eq-box" id="eqBox">계산 중...</div>
    <div id="conclusionBox" style="font-size:.97rem;color:#e2e8ff;line-height:1.8"></div>
  </div>

  <div class="card" style="border-color:rgba(99,102,241,.35)">
    <div class="card-title">📌 핵심 정리</div>
    <div style="font-size:.93rem;line-height:1.9;color:#c7d2fe">
      이차함수 <em style="color:#a5b4fc">y = ax² + bx + c</em>의 그래프와
      직선 <em style="color:#f9a8d4">y = mx + n</em>의 교점의 개수<br>
      ⟺ 이차방정식 <em style="color:#fde68a">ax² + (b−m)x + (c−n) = 0</em>의 실근의 개수<br>
      ⟺ 판별식 <em style="color:#fde68a">D = (b−m)² − 4a(c−n)</em>의 부호
    </div>
    <div style="margin-top:12px;display:flex;flex-direction:column;gap:6px;font-size:.93rem">
      <div style="display:flex;align-items:center;gap:10px">
        <span style="background:#14532d;color:#86efac;border-radius:20px;padding:3px 12px;font-weight:700;white-space:nowrap">D &gt; 0</span>
        <span style="color:#94a3b8">서로 다른 두 점에서 만난다 (교점 2개)</span>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span style="background:#713f12;color:#fde68a;border-radius:20px;padding:3px 12px;font-weight:700;white-space:nowrap">D = 0</span>
        <span style="color:#94a3b8">한 점에서 만난다 — 접한다 (교점 1개)</span>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span style="background:#4c0519;color:#fca5a5;border-radius:20px;padding:3px 12px;font-weight:700;white-space:nowrap">D &lt; 0</span>
        <span style="color:#94a3b8">만나지 않는다 (교점 0개)</span>
      </div>
    </div>
  </div>

</div>

<!-- ══════════════════════ TAB 1: 연습문제 ══════════════════════ -->
<div id="tab1" class="hidden">

  <div class="sub-tabs">
    <button class="sub-tab active" onclick="goProb(0)">문제 1</button>
    <button class="sub-tab" onclick="goProb(1)">문제 2</button>
    <button class="sub-tab" onclick="goProb(2)">문제 3</button>
  </div>

  <!-- ───── 문제 1 ───── -->
  <div id="prob0">
    <div class="card" style="background:rgba(99,102,241,.08);border-color:rgba(99,102,241,.3);margin-bottom:14px">
      <div style="font-size:1rem;font-weight:700;color:#a5b4fc;margin-bottom:6px">📝 문제 1</div>
      <div style="font-size:1rem;line-height:1.9;color:#e2e8ff">
        이차함수 <strong>y = x² + 2x − 5</strong>의 그래프와
        직선 <strong>y = 4x + k</strong>의 위치 관계가 다음과 같도록
        실수 k의 값 또는 범위를 정하시오.
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 1 — 연립방정식 세우기</div>
      <div class="prob-text">
        교점을 찾으려면 두 식을 같다고 놓으면 됩니다.<br>
        <em style="color:#fde68a">x² + 2x − 5 = 4x + k</em><br>
        정리하면 어떤 이차방정식이 될까요?
      </div>
      <div class="sub-q">
        <label>정리한 이차방정식을 고르세요:</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('s1','A')" data-q="s1" data-v="A">x² − 2x + (5+k) = 0</button>
          <button class="opt-btn" onclick="ans('s1','B')" data-q="s1" data-v="B">x² − 2x − (5+k) = 0</button>
          <button class="opt-btn" onclick="ans('s1','C')" data-q="s1" data-v="C">x² + 6x − (5+k) = 0</button>
        </div>
        <div class="fb" id="s1fb"></div>
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 2 — 판별식 D 계산하기</div>
      <div class="prob-text">
        이차방정식 <em style="color:#fde68a">x² − 2x − (5+k) = 0</em>의 판별식<br>
        <em style="color:#a5b4fc">D = (−2)² − 4·1·(−5−k)</em> 를 전개하면?
      </div>
      <div class="sub-q">
        <label>D를 k로 표현한 식을 고르세요:</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('s2','A')" data-q="s2" data-v="A">D = 4k + 24</button>
          <button class="opt-btn" onclick="ans('s2','B')" data-q="s2" data-v="B">D = 4k − 24</button>
          <button class="opt-btn" onclick="ans('s2','C')" data-q="s2" data-v="C">D = 4k + 4</button>
        </div>
        <div class="fb" id="s2fb"></div>
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 3 — 위치관계에 따른 k 범위 / 값</div>
      <div style="font-size:.93rem;color:#94a3b8;margin-bottom:12px">D = 4k + 24 임을 이용해 각 조건의 정답을 골라보세요.</div>
      <div class="sub-q">
        <label><strong>(1) 서로 다른 두 점에서 만난다</strong> — D &gt; 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('q1','A')" data-q="q1" data-v="A">k &lt; −6</button>
          <button class="opt-btn" onclick="ans('q1','B')" data-q="q1" data-v="B">k &gt; 6</button>
          <button class="opt-btn" onclick="ans('q1','C')" data-q="q1" data-v="C">k &gt; −6</button>
        </div>
        <div class="fb" id="q1fb"></div>
      </div>
      <div class="sub-q">
        <label><strong>(2) 한 점에서 만난다 (접한다)</strong> — D = 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('q2','A')" data-q="q2" data-v="A">k = 6</button>
          <button class="opt-btn" onclick="ans('q2','B')" data-q="q2" data-v="B">k = −6</button>
          <button class="opt-btn" onclick="ans('q2','C')" data-q="q2" data-v="C">k = −24</button>
        </div>
        <div class="fb" id="q2fb"></div>
      </div>
      <div class="sub-q">
        <label><strong>(3) 만나지 않는다</strong> — D &lt; 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('q3','A')" data-q="q3" data-v="A">k &lt; −6</button>
          <button class="opt-btn" onclick="ans('q3','B')" data-q="q3" data-v="B">k &gt; −6</button>
          <button class="opt-btn" onclick="ans('q3','C')" data-q="q3" data-v="C">k &lt; 6</button>
        </div>
        <div class="fb" id="q3fb"></div>
      </div>
    </div>

    <div id="p1Done" class="done-banner hidden">
      <div style="font-size:1.6rem;margin-bottom:4px">🎉</div>
      <div style="font-size:1.1rem;color:#fcd34d;font-weight:700;margin-bottom:4px">문제 1 완료!</div>
      <p style="font-size:.93rem;color:#94a3b8;line-height:1.7">
        D = 4k+24 &nbsp;→&nbsp; D&gt;0: k&gt;−6 &nbsp;|&nbsp; D=0: k=−6 &nbsp;|&nbsp; D&lt;0: k&lt;−6
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goProb(1)">문제 2 →</button>
    </div>
  </div>

  <!-- ───── 문제 2 ───── -->
  <div id="prob1" class="hidden">
    <div class="card" style="background:rgba(99,102,241,.08);border-color:rgba(99,102,241,.3);margin-bottom:14px">
      <div style="font-size:1rem;font-weight:700;color:#a5b4fc;margin-bottom:6px">📝 문제 2</div>
      <div style="font-size:1rem;line-height:1.9;color:#e2e8ff">
        이차함수 <strong>y = x² − 6x + 5</strong>의 그래프와
        직선 <strong>y = 2x + k</strong>의 위치 관계가 다음과 같도록
        실수 k의 값 또는 범위를 정하시오.
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 1 — 연립방정식 세우기</div>
      <div class="prob-text">
        <em style="color:#fde68a">x² − 6x + 5 = 2x + k</em><br>
        정리하면 어떤 이차방정식이 될까요?
      </div>
      <div class="sub-q">
        <label>정리한 이차방정식을 고르세요:</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p2s1','A')" data-q="p2s1" data-v="A">x² − 4x + (5−k) = 0</button>
          <button class="opt-btn" onclick="ans('p2s1','B')" data-q="p2s1" data-v="B">x² − 8x + (5−k) = 0</button>
          <button class="opt-btn" onclick="ans('p2s1','C')" data-q="p2s1" data-v="C">x² − 8x + (5+k) = 0</button>
        </div>
        <div class="fb" id="p2s1fb"></div>
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 2 — 판별식 D 계산하기</div>
      <div class="prob-text">
        이차방정식 <em style="color:#fde68a">x² − 8x + (5−k) = 0</em>의 판별식<br>
        <em style="color:#a5b4fc">D = (−8)² − 4·1·(5−k)</em> 를 전개하면?
      </div>
      <div class="sub-q">
        <label>D를 k로 표현한 식을 고르세요:</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p2s2','A')" data-q="p2s2" data-v="A">D = 4k − 44</button>
          <button class="opt-btn" onclick="ans('p2s2','B')" data-q="p2s2" data-v="B">D = 4k + 20</button>
          <button class="opt-btn" onclick="ans('p2s2','C')" data-q="p2s2" data-v="C">D = 4k + 44</button>
        </div>
        <div class="fb" id="p2s2fb"></div>
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 3 — 위치관계에 따른 k 범위 / 값</div>
      <div style="font-size:.93rem;color:#94a3b8;margin-bottom:12px">D = 4k + 44 임을 이용해 각 조건의 정답을 골라보세요.</div>
      <div class="sub-q">
        <label><strong>(1) 서로 다른 두 점에서 만난다</strong> — D &gt; 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p2q1','A')" data-q="p2q1" data-v="A">k &gt; −11</button>
          <button class="opt-btn" onclick="ans('p2q1','B')" data-q="p2q1" data-v="B">k &lt; −11</button>
          <button class="opt-btn" onclick="ans('p2q1','C')" data-q="p2q1" data-v="C">k &gt; 11</button>
        </div>
        <div class="fb" id="p2q1fb"></div>
      </div>
      <div class="sub-q">
        <label><strong>(2) 한 점에서 만난다 (접한다)</strong> — D = 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p2q2','A')" data-q="p2q2" data-v="A">k = 11</button>
          <button class="opt-btn" onclick="ans('p2q2','B')" data-q="p2q2" data-v="B">k = −44</button>
          <button class="opt-btn" onclick="ans('p2q2','C')" data-q="p2q2" data-v="C">k = −11</button>
        </div>
        <div class="fb" id="p2q2fb"></div>
      </div>
      <div class="sub-q">
        <label><strong>(3) 만나지 않는다</strong> — D &lt; 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p2q3','A')" data-q="p2q3" data-v="A">k &lt; 11</button>
          <button class="opt-btn" onclick="ans('p2q3','B')" data-q="p2q3" data-v="B">k &lt; −11</button>
          <button class="opt-btn" onclick="ans('p2q3','C')" data-q="p2q3" data-v="C">k &gt; −11</button>
        </div>
        <div class="fb" id="p2q3fb"></div>
      </div>
    </div>

    <div id="p2Done" class="done-banner hidden">
      <div style="font-size:1.6rem;margin-bottom:4px">🎉</div>
      <div style="font-size:1.1rem;color:#fcd34d;font-weight:700;margin-bottom:4px">문제 2 완료!</div>
      <p style="font-size:.93rem;color:#94a3b8;line-height:1.7">
        D = 4k+44 &nbsp;→&nbsp; D&gt;0: k&gt;−11 &nbsp;|&nbsp; D=0: k=−11 &nbsp;|&nbsp; D&lt;0: k&lt;−11
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goProb(2)">문제 3 →</button>
    </div>
  </div>

  <!-- ───── 문제 3 ───── -->
  <div id="prob2" class="hidden">
    <div class="card" style="background:rgba(99,102,241,.08);border-color:rgba(99,102,241,.3);margin-bottom:14px">
      <div style="font-size:1rem;font-weight:700;color:#a5b4fc;margin-bottom:6px">📝 문제 3</div>
      <div style="font-size:1rem;line-height:1.9;color:#e2e8ff">
        이차함수 <strong>y = x² + 3x − 2</strong>의 그래프와
        직선 <strong>y = x + k</strong>의 위치 관계가 다음과 같도록
        실수 k의 값 또는 범위를 정하시오.
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 1 — 연립방정식 세우기</div>
      <div class="prob-text">
        <em style="color:#fde68a">x² + 3x − 2 = x + k</em><br>
        정리하면 어떤 이차방정식이 될까요?
      </div>
      <div class="sub-q">
        <label>정리한 이차방정식을 고르세요:</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p3s1','A')" data-q="p3s1" data-v="A">x² + 2x + (2+k) = 0</button>
          <button class="opt-btn" onclick="ans('p3s1','B')" data-q="p3s1" data-v="B">x² + 4x − (2+k) = 0</button>
          <button class="opt-btn" onclick="ans('p3s1','C')" data-q="p3s1" data-v="C">x² + 2x − (2+k) = 0</button>
        </div>
        <div class="fb" id="p3s1fb"></div>
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 2 — 판별식 D 계산하기</div>
      <div class="prob-text">
        이차방정식 <em style="color:#fde68a">x² + 2x − (2+k) = 0</em>의 판별식<br>
        <em style="color:#a5b4fc">D = (2)² − 4·1·(−2−k)</em> 를 전개하면?
      </div>
      <div class="sub-q">
        <label>D를 k로 표현한 식을 고르세요:</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p3s2','A')" data-q="p3s2" data-v="A">D = 4k + 12</button>
          <button class="opt-btn" onclick="ans('p3s2','B')" data-q="p3s2" data-v="B">D = 4k − 12</button>
          <button class="opt-btn" onclick="ans('p3s2','C')" data-q="p3s2" data-v="C">D = 4k + 16</button>
        </div>
        <div class="fb" id="p3s2fb"></div>
      </div>
    </div>

    <div class="prob-card">
      <div class="prob-num">STEP 3 — 위치관계에 따른 k 범위 / 값</div>
      <div style="font-size:.93rem;color:#94a3b8;margin-bottom:12px">D = 4k + 12 임을 이용해 각 조건의 정답을 골라보세요.</div>
      <div class="sub-q">
        <label><strong>(1) 서로 다른 두 점에서 만난다</strong> — D &gt; 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p3q1','A')" data-q="p3q1" data-v="A">k &lt; −3</button>
          <button class="opt-btn" onclick="ans('p3q1','B')" data-q="p3q1" data-v="B">k &gt; −3</button>
          <button class="opt-btn" onclick="ans('p3q1','C')" data-q="p3q1" data-v="C">k &gt; 3</button>
        </div>
        <div class="fb" id="p3q1fb"></div>
      </div>
      <div class="sub-q">
        <label><strong>(2) 한 점에서 만난다 (접한다)</strong> — D = 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p3q2','A')" data-q="p3q2" data-v="A">k = −3</button>
          <button class="opt-btn" onclick="ans('p3q2','B')" data-q="p3q2" data-v="B">k = 3</button>
          <button class="opt-btn" onclick="ans('p3q2','C')" data-q="p3q2" data-v="C">k = −12</button>
        </div>
        <div class="fb" id="p3q2fb"></div>
      </div>
      <div class="sub-q">
        <label><strong>(3) 만나지 않는다</strong> — D &lt; 0 이면?</label>
        <div class="opts">
          <button class="opt-btn" onclick="ans('p3q3','A')" data-q="p3q3" data-v="A">k &gt; −3</button>
          <button class="opt-btn" onclick="ans('p3q3','B')" data-q="p3q3" data-v="B">k &lt; 3</button>
          <button class="opt-btn" onclick="ans('p3q3','C')" data-q="p3q3" data-v="C">k &lt; −3</button>
        </div>
        <div class="fb" id="p3q3fb"></div>
      </div>
    </div>

    <div id="p3Done" class="done-banner hidden">
      <div style="font-size:1.6rem;margin-bottom:4px">🏅</div>
      <div style="font-size:1.1rem;color:#fcd34d;font-weight:700;margin-bottom:4px">문제 3 완료! 연습문제 마스터!</div>
      <p style="font-size:.93rem;color:#94a3b8;line-height:1.7">
        D = 4k+12 &nbsp;→&nbsp; D&gt;0: k&gt;−3 &nbsp;|&nbsp; D=0: k=−3 &nbsp;|&nbsp; D&lt;0: k&lt;−3<br>
        이제 생각 넓히기에 도전해 보세요!
      </p>
      <button class="btn btn-p" style="margin-top:8px" onclick="goTab(2)">생각 넓히기 →</button>
    </div>
  </div>

</div>

<!-- ══════════════════════ TAB 2: 생각 넓히기 ══════════════════════ -->
<div id="tab2" class="hidden">

  <div class="card" style="background:rgba(250,204,21,.06);border-color:rgba(250,204,21,.3);margin-bottom:16px">
    <div style="font-size:.88rem;font-weight:700;color:#fbbf24;margin-bottom:6px">⭐ 생각 넓히기</div>
    <div style="font-size:1.02rem;line-height:1.9;color:#e2e8ff">
      이차함수 <strong>y = x² − 2x + 1</strong>의 그래프와
      직선 <strong>y = kx + 4</strong>는 실수 k의 값에 관계없이
      항상 서로 다른 두 점에서 만남을 다음 두 가지 방법으로 설명해 보자.
    </div>
  </div>

  <!-- 방법 1 -->
  <div class="prob-card">
    <div class="prob-num">방법 1 — 이차방정식의 판별식 이용하기</div>

    <div class="sub-q" style="margin-bottom:14px">
      <label>① 두 식을 연립하면 어떤 이차방정식이 되나요?</label>
      <div class="opts">
        <button class="opt-btn" onclick="ans('c1','A')" data-q="c1" data-v="A">x² + (2+k)x + 3 = 0</button>
        <button class="opt-btn" onclick="ans('c1','B')" data-q="c1" data-v="B">x² − (2+k)x + 5 = 0</button>
        <button class="opt-btn" onclick="ans('c1','C')" data-q="c1" data-v="C">x² − (2+k)x − 3 = 0</button>
      </div>
      <div class="fb" id="c1fb"></div>
    </div>

    <div class="sub-q" style="margin-bottom:14px">
      <label>② 이 이차방정식의 판별식 D = (2+k)² − 4·1·(−3) 을 전개하면?</label>
      <div class="opts">
        <button class="opt-btn" onclick="ans('c2','A')" data-q="c2" data-v="A">D = (2+k)² − 12</button>
        <button class="opt-btn" onclick="ans('c2','B')" data-q="c2" data-v="B">D = (2+k)² + 12</button>
        <button class="opt-btn" onclick="ans('c2','C')" data-q="c2" data-v="C">D = (k−2)² + 12</button>
      </div>
      <div class="fb" id="c2fb"></div>
    </div>

    <div class="sub-q">
      <label>③ D = (2+k)² + 12 가 항상 D &gt; 0인 이유는?</label>
      <div class="opts">
        <button class="opt-btn" onclick="ans('c3','A')" data-q="c3" data-v="A">(2+k)² ≥ 0 이므로 D ≥ 12 &gt; 0</button>
        <button class="opt-btn" onclick="ans('c3','B')" data-q="c3" data-v="B">12 &gt; 0 이기만 하면 항상 D &gt; 0</button>
        <button class="opt-btn" onclick="ans('c3','C')" data-q="c3" data-v="C">k가 항상 양수이므로 D &gt; 0</button>
      </div>
      <div class="fb" id="c3fb"></div>
    </div>
  </div>

  <!-- 방법 2 — 그래프 이용하기 (flex layout) -->
  <div class="prob-card">
    <div class="prob-num">방법 2 — 그래프 이용하기</div>

    <div class="chall-layout">

      <!-- 왼쪽: 질문들 -->
      <div class="chall-questions">
        <p style="font-size:.91rem;color:#94a3b8;margin-bottom:12px;line-height:1.7">
          직선 y = kx + 4는 기울기 k에 관계없이 항상 한 점을 지납니다.<br>
          오른쪽 그래프에서 슬라이더를 움직이며 확인해 보세요!
        </p>

        <div class="sub-q" style="margin-bottom:14px">
          <label>① 직선 y = kx + 4가 항상 지나는 점은? (x=0 대입)</label>
          <div class="opts">
            <button class="opt-btn" onclick="ans('g1','A')" data-q="g1" data-v="A">(4, 0)</button>
            <button class="opt-btn" onclick="ans('g1','B')" data-q="g1" data-v="B">(0, k)</button>
            <button class="opt-btn" onclick="ans('g1','C')" data-q="g1" data-v="C">(0, 4)</button>
          </div>
          <div class="fb" id="g1fb"></div>
        </div>

        <div class="sub-q" style="margin-bottom:14px">
          <label>② x=0에서 이차함수값은? → 고정점 (0,4)와 위치 비교</label>
          <div class="opts">
            <button class="opt-btn" onclick="ans('g2','A')" data-q="g2" data-v="A">y=3 → 고정점이 포물선보다 위</button>
            <button class="opt-btn" onclick="ans('g2','B')" data-q="g2" data-v="B">y=1 → 고정점이 포물선보다 위</button>
            <button class="opt-btn" onclick="ans('g2','C')" data-q="g2" data-v="C">y=4 → 고정점이 포물선 위에 있음</button>
          </div>
          <div class="fb" id="g2fb"></div>
        </div>

        <div class="sub-q">
          <label>③ y = x² − 2x + 1의 꼭짓점은? (완전제곱식으로 변환)</label>
          <div class="opts">
            <button class="opt-btn" onclick="ans('g3','A')" data-q="g3" data-v="A">꼭짓점 (1, 0) — 최솟값 0</button>
            <button class="opt-btn" onclick="ans('g3','B')" data-q="g3" data-v="B">꼭짓점 (−1, 0) — 최솟값 0</button>
            <button class="opt-btn" onclick="ans('g3','C')" data-q="g3" data-v="C">꼭짓점 (1, 2) — 최솟값 2</button>
          </div>
          <div class="fb" id="g3fb"></div>
        </div>

        <!-- 그래프 설명 (방법1 완료 시 등장) -->
        <div id="graphExplain" class="challenge-hint" style="margin-top:10px">
          ✨ y = (x−1)² → 꼭짓점 (1,0), 최솟값 0.<br>
          x=0에서 포물선값은 1이고 고정점 y = 4 &gt; 1<br>
          → 고정점 (0,4)가 포물선 위에 있습니다.<br>
          포물선은 양끝으로 +∞ → k가 어떤 값이든<br>
          직선은 반드시 포물선과 두 번 만납니다!
        </div>
      </div>

      <!-- 오른쪽: 그래프 -->
      <div class="chall-graph-panel">
        <div style="font-size:.82rem;color:#a5b4fc;font-weight:700;margin-bottom:6px;text-align:center">
          📊 그래프로 확인하기
        </div>
        <div class="chall-canvas-wrap">
          <canvas id="challCanvas" height="240"></canvas>
        </div>
        <div style="font-size:.83rem;color:#94a3b8;margin-bottom:4px">기울기 k 조절:</div>
        <div style="display:flex;align-items:center;gap:8px">
          <input type="range" id="challK" min="-5" max="5" step="0.5" value="1"
                 oninput="drawChallGraph()" style="flex:1;accent-color:#f472b6">
          <span id="challKval" style="min-width:32px;color:#fde68a;font-weight:700;font-size:.9rem">1</span>
        </div>
        <div style="margin-top:8px;font-size:.8rem;color:#64748b;line-height:1.6">
          <span style="color:#818cf8">■</span> y=(x−1)²&nbsp;&nbsp;
          <span style="color:#f472b6">■</span> y=kx+4<br>
          <span style="color:#fbbf24">●</span> 고정점 (0,4)&nbsp;&nbsp;
          <span style="color:#86efac">●</span> 교점
        </div>
      </div>

    </div><!-- end chall-layout -->
  </div>

  <!-- 완료 배너 -->
  <div id="challDone" class="done-banner hidden">
    <div style="font-size:1.8rem;margin-bottom:6px">🏆</div>
    <div style="font-size:1.15rem;color:#fcd34d;font-weight:700;margin-bottom:8px">생각 넓히기 완료!</div>
    <p style="font-size:.95rem;color:#94a3b8;line-height:1.75">
      D = (2+k)² + 12 ≥ 12 &gt; 0 → 항상 D &gt; 0<br>
      → 이차함수와 직선은 k에 관계없이 <strong style="color:#86efac">항상 두 점에서 만납니다!</strong><br><br>
      아래 성찰 질문도 꼼꼼히 답해보세요 💜
    </p>
  </div>

</div><!-- end tab2 -->

<script>
/* ══════════════ Tab / Prob navigation ══════════════ */
function goTab(n){
  ['tab0','tab1','tab2'].forEach((id,i)=>{
    document.getElementById(id).classList.toggle('hidden', i!==n);
  });
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',i===n));
  scheduleResize(80);
}

function goProb(n){
  ['prob0','prob1','prob2'].forEach((id,i)=>{
    document.getElementById(id).classList.toggle('hidden', i!==n);
  });
  document.querySelectorAll('.sub-tab').forEach((t,i)=>t.classList.toggle('active',i===n));
  scheduleResize(80);
}

function scheduleResize(ms){
  setTimeout(()=>{
    const h = document.body.scrollHeight + 40;
    window.parent.postMessage({type:'streamlit:setFrameHeight', height:h},'*');
  }, ms);
}
window.addEventListener('load', ()=>{
  drawGraph();
  drawChallGraph();
  scheduleResize(300);
});

/* ══════════════ Main Graph (Tab 0) ══════════════ */
const canvas = document.getElementById('gc');

function drawGraph(){
  const b = parseFloat(document.getElementById('sb').value);
  const c = parseFloat(document.getElementById('sc').value);
  const m = parseFloat(document.getElementById('sm').value);
  const n = parseFloat(document.getElementById('sn').value);

  document.getElementById('vb').textContent = b%1===0?b:b.toFixed(1);
  document.getElementById('vc').textContent = c%1===0?c:c.toFixed(1);
  document.getElementById('vm').textContent = m%1===0?m:m.toFixed(1);
  document.getElementById('vn').textContent = n%1===0?n:n.toFixed(1);

  const a=1, D=(b-m)*(b-m)-4*a*(c-n);
  const Dval=Math.round(D*100)/100;

  const badge=document.getElementById('dBadge');
  if(D>0.001){
    badge.className='d-badge d-pos';
    badge.textContent=`D = ${Dval} > 0  →  서로 다른 두 점에서 만난다 ✓`;
  } else if(D<-0.001){
    badge.className='d-badge d-neg';
    badge.textContent=`D = ${Dval} < 0  →  만나지 않는다 ✗`;
  } else {
    badge.className='d-badge d-zero';
    badge.textContent=`D ≈ 0  →  한 점에서 만난다 (접한다) ◎`;
  }

  const bm=Math.round((b-m)*100)/100, cn=Math.round((c-n)*100)/100;
  const t1=Math.round((b-m)*(b-m)*100)/100, t2=Math.round(4*a*(c-n)*100)/100;
  const fmt=v=>v>=0?`+${v}`:String(v);
  const Dcol=D>0.001?'green':D<-0.001?'red':'gold';
  document.getElementById('eqBox').innerHTML=
    `이차함수 <em>y = x²${fmt(b)}x${fmt(c)}</em> 와 직선 <em style="color:#f9a8d4">y = ${m}x${fmt(n)}</em> 을 연립하면<br>`+
    `⟹ x²${fmt(bm)}x${fmt(cn)} = 0<br>`+
    `⟹ D = <em class="gold">(${bm})²</em> − 4·<em class="gold">(${cn})</em> = ${t1} − ${t2} = <em class="${Dcol}">${Dval}</em>`;

  const cb=document.getElementById('conclusionBox');
  if(D>0.001)      cb.innerHTML='<span style="color:#86efac">✅ D &gt; 0 → 서로 다른 두 점에서 만납니다.</span>';
  else if(D<-0.001)cb.innerHTML='<span style="color:#fca5a5">❌ D &lt; 0 → 만나지 않습니다.</span>';
  else             cb.innerHTML='<span style="color:#fbbf24">◎ D = 0 → 한 점에서 만납니다 (접합니다).</span>';

  const W=canvas.offsetWidth||340;
  canvas.width=W; canvas.height=300;
  const ctx=canvas.getContext('2d');
  ctx.clearRect(0,0,W,300);

  const xMin=-6,xMax=6,yMin=-8,yMax=12;
  const toX=xv=>(xv-xMin)/(xMax-xMin)*W;
  const toY=yv=>(1-(yv-yMin)/(yMax-yMin))*300;

  ctx.strokeStyle='rgba(255,255,255,0.07)'; ctx.lineWidth=1;
  for(let gx=-6;gx<=6;gx++){ctx.beginPath();ctx.moveTo(toX(gx),0);ctx.lineTo(toX(gx),300);ctx.stroke();}
  for(let gy=-8;gy<=12;gy+=2){ctx.beginPath();ctx.moveTo(0,toY(gy));ctx.lineTo(W,toY(gy));ctx.stroke();}
  ctx.strokeStyle='rgba(255,255,255,0.35)'; ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(0,toY(0));ctx.lineTo(W,toY(0));ctx.stroke();
  ctx.beginPath();ctx.moveTo(toX(0),0);ctx.lineTo(toX(0),300);ctx.stroke();

  ctx.strokeStyle='#818cf8'; ctx.lineWidth=2.5; ctx.beginPath();
  let first=true;
  for(let px=0;px<=W;px++){
    const xv=xMin+(px/W)*(xMax-xMin), yv=xv*xv+b*xv+c;
    if(yv<yMin-2||yv>yMax+2){first=true;continue;}
    first?ctx.moveTo(px,toY(yv)):ctx.lineTo(px,toY(yv)); first=false;
  }
  ctx.stroke();

  ctx.strokeStyle='#f472b6'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(toX(xMin),toY(m*xMin+n)); ctx.lineTo(toX(xMax),toY(m*xMax+n)); ctx.stroke();

  ctx.font='bold 12px sans-serif';
  ctx.fillStyle='#a5b4fc'; ctx.textAlign='left';
  ctx.fillText(`y = x²${fmt(b)}x${fmt(c)}`, 8, 18);
  ctx.fillStyle='#f9a8d4';
  ctx.fillText(`y = ${m}x${fmt(n)}`, 8, 34);

  const B2=b-m, C2=c-n, disc=B2*B2-4*C2;
  if(disc>=-1e-9){
    const sqD=Math.sqrt(Math.max(0,disc));
    const roots=disc>1e-9?[(-B2+sqD)/2,(-B2-sqD)/2]:[(-B2)/2];
    roots.forEach(rx=>{
      if(rx<xMin-0.1||rx>xMax+0.1)return;
      const ry=m*rx+n;
      if(ry<yMin-0.1||ry>yMax+0.1)return;
      ctx.beginPath(); ctx.arc(toX(rx),toY(ry),7,0,Math.PI*2);
      ctx.fillStyle=disc>1e-9?'#86efac':'#fbbf24'; ctx.fill();
      ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
      ctx.fillStyle='#fff'; ctx.font='11px sans-serif'; ctx.textAlign='center';
      ctx.fillText(`(${Math.round(rx*100)/100}, ${Math.round(ry*100)/100})`, toX(rx), toY(ry)-12);
    });
  }
  scheduleResize(50);
}

/* ══════════════ Challenge Graph (Tab 2 방법2) ══════════════ */
function drawChallGraph(){
  const kEl=document.getElementById('challK');
  const k=parseFloat(kEl.value);
  document.getElementById('challKval').textContent=k%1===0?k:k.toFixed(1);

  const cv=document.getElementById('challCanvas');
  const W=cv.offsetWidth||260;
  cv.width=W; cv.height=240;
  const ctx=cv.getContext('2d');
  ctx.clearRect(0,0,W,240);

  const xMin=-2,xMax=5,yMin=-1,yMax=10;
  const toX=xv=>(xv-xMin)/(xMax-xMin)*W;
  const toY=yv=>(1-(yv-yMin)/(yMax-yMin))*240;

  // Grid
  ctx.strokeStyle='rgba(255,255,255,0.07)'; ctx.lineWidth=1;
  for(let gx=-2;gx<=5;gx++){ctx.beginPath();ctx.moveTo(toX(gx),0);ctx.lineTo(toX(gx),240);ctx.stroke();}
  for(let gy=-1;gy<=10;gy++){ctx.beginPath();ctx.moveTo(0,toY(gy));ctx.lineTo(W,toY(gy));ctx.stroke();}

  // Axes
  ctx.strokeStyle='rgba(255,255,255,0.3)'; ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(0,toY(0));ctx.lineTo(W,toY(0));ctx.stroke();
  ctx.beginPath();ctx.moveTo(toX(0),0);ctx.lineTo(toX(0),240);ctx.stroke();

  // Axis labels
  ctx.fillStyle='rgba(255,255,255,0.3)'; ctx.font='10px sans-serif'; ctx.textAlign='center';
  for(let gx=-1;gx<=4;gx++) if(gx!==0) ctx.fillText(gx, toX(gx), toY(0)+13);
  ctx.textAlign='right';
  for(let gy=2;gy<=8;gy+=2) ctx.fillText(gy, toX(0)-3, toY(gy)+4);

  // Parabola y=(x-1)²
  ctx.strokeStyle='#818cf8'; ctx.lineWidth=2.5; ctx.beginPath();
  let first=true;
  for(let px=0;px<=W;px++){
    const xv=xMin+(px/W)*(xMax-xMin), yv=(xv-1)*(xv-1);
    if(yv<yMin-0.5||yv>yMax+0.5){first=true;continue;}
    first?ctx.moveTo(px,toY(yv)):ctx.lineTo(px,toY(yv)); first=false;
  }
  ctx.stroke();

  // Line y=kx+4
  ctx.strokeStyle='#f472b6'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(toX(xMin),toY(k*xMin+4)); ctx.lineTo(toX(xMax),toY(k*xMax+4)); ctx.stroke();

  // Fixed point (0,4) — gold
  ctx.beginPath(); ctx.arc(toX(0),toY(4),7,0,Math.PI*2);
  ctx.fillStyle='#fbbf24'; ctx.fill();
  ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
  ctx.fillStyle='#fde68a'; ctx.font='bold 10px sans-serif'; ctx.textAlign='left';
  ctx.fillText('(0,4)', toX(0)+9, toY(4)-3);

  // Parabola at x=0: (0,1) — purple dot
  ctx.beginPath(); ctx.arc(toX(0),toY(1),4,0,Math.PI*2);
  ctx.fillStyle='#a5b4fc'; ctx.fill();
  ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke();
  ctx.fillStyle='#c7d2fe'; ctx.font='10px sans-serif'; ctx.textAlign='left';
  ctx.fillText('(0,1)', toX(0)+9, toY(1)+13);

  // Intersection points
  // x²-(2+k)x-3=0
  const disc=(2+k)*(2+k)+12;
  if(disc>=0){
    const sqD=Math.sqrt(disc);
    const B2=-(2+k);
    [(-B2+sqD)/2, (-B2-sqD)/2].forEach(rx=>{
      if(rx<xMin-0.1||rx>xMax+0.1)return;
      const ry=k*rx+4;
      if(ry<yMin-0.1||ry>yMax+0.5)return;
      ctx.beginPath(); ctx.arc(toX(rx),toY(ry),6,0,Math.PI*2);
      ctx.fillStyle='#86efac'; ctx.fill();
      ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
    });
  }

  // D label
  const Dval=Math.round(disc*10)/10;
  ctx.fillStyle='#fde68a'; ctx.font='bold 10px sans-serif'; ctx.textAlign='left';
  ctx.fillText(`D=(2+k)²+12 = ${Dval}`, 4, 14);

  scheduleResize(50);
}

/* ══════════════ Answers ══════════════ */
const CORRECT = {
  s1:'B',  s2:'A',  q1:'C',  q2:'B',  q3:'A',
  p2s1:'B', p2s2:'C', p2q1:'A', p2q2:'C', p2q3:'B',
  p3s1:'C', p3s2:'A', p3q1:'B', p3q2:'A', p3q3:'C',
  c1:'C', c2:'B', c3:'A',
  g1:'C', g2:'B', g3:'A',
};

const HINTS = {
  s1:{
    A:'✗ 다시 시도! 상수항: −5를 이항하면 −k, 즉 −5−k = −(5+k)예요. 부호 확인!',
    B:'✓ 정답! x²+2x−5=4x+k → x²+(2−4)x+(−5−k)=0 → x²−2x−(5+k)=0',
    C:'✗ 다시 시도! x항: 2x−4x = (2−4)x = −2x예요. +6x가 아니에요.',
  },
  s2:{
    A:'✓ 정답! D=(−2)²−4·(−5−k)=4+20+4k=4k+24',
    B:'✗ 다시 시도! −4ac = −4·(−5−k) = +4(5+k) = +20+4k예요. 부호 확인!',
    C:'✗ 다시 시도! 4+4(5+k) = 4+20+4k = 24+4k예요. 다시 계산해 보세요.',
  },
  q1:{
    A:'✗ 다시 시도! 4k+24>0 → 4k>−24 → k>? 부등호 방향에 주의!',
    B:'✗ 다시 시도! 4k>−24에서 양변을 4로 나누면 k>−6이에요.',
    C:'✓ 정답! D=4k+24>0 → 4k>−24 → k>−6',
  },
  q2:{
    A:'✗ 다시 시도! 4k+24=0 → 4k=−24 → k=?',
    B:'✓ 정답! D=4k+24=0 → 4k=−24 → k=−6',
    C:'✗ 다시 시도! 24를 4로 나누면 6이에요. k=−6이에요.',
  },
  q3:{
    A:'✓ 정답! D=4k+24<0 → 4k<−24 → k<−6',
    B:'✗ 다시 시도! D<0이 되려면 4k+24<0 → 4k<−24 → k<?',
    C:'✗ 다시 시도! 4k<−24를 k에 대해 풀어보세요.',
  },
  p2s1:{
    A:'✗ 다시 시도! x항: −6x−2x=(−6−2)x=−8x예요. −4x가 아니에요.',
    B:'✓ 정답! x²−6x+5=2x+k → x²−8x+(5−k)=0',
    C:'✗ 다시 시도! 상수항: 5−k이에요. 이항하면 −k이므로 +(5+k)가 아니에요.',
  },
  p2s2:{
    A:'✗ 다시 시도! D=64−4(5−k)=64−20+4k=44+4k예요. 부호 확인!',
    B:'✗ 다시 시도! 64−20+4k를 계산하면? 64−20=44이에요.',
    C:'✓ 정답! D=(−8)²−4(5−k)=64−20+4k=4k+44',
  },
  p2q1:{
    A:'✓ 정답! D=4k+44>0 → 4k>−44 → k>−11',
    B:'✗ 다시 시도! 4k>−44에서 양변을 4로 나누면 k>−11이에요.',
    C:'✗ 다시 시도! 4k+44>0 → 4k>−44 → k>?',
  },
  p2q2:{
    A:'✗ 다시 시도! 4k+44=0 → 4k=−44 → k=−11이에요. +11이 아니에요.',
    B:'✗ 다시 시도! 44를 4로 나누면 11이에요. k=−11이에요.',
    C:'✓ 정답! D=4k+44=0 → 4k=−44 → k=−11',
  },
  p2q3:{
    A:'✗ 다시 시도! 4k+44<0 → 4k<−44 → k<−11이에요.',
    B:'✓ 정답! D=4k+44<0 → 4k<−44 → k<−11',
    C:'✗ 다시 시도! D<0이 되려면 4k<−44 → k<?',
  },
  p3s1:{
    A:'✗ 다시 시도! 상수항: −2−k = −(2+k)이에요. +(2+k)가 아니에요.',
    B:'✗ 다시 시도! x항: 3x−x=(3−1)x=2x예요. +4x가 아니에요.',
    C:'✓ 정답! x²+3x−2=x+k → x²+(3−1)x+(−2−k)=0 → x²+2x−(2+k)=0',
  },
  p3s2:{
    A:'✓ 정답! D=(2)²−4·(−2−k)=4+4(2+k)=4+8+4k=4k+12',
    B:'✗ 다시 시도! c=−(2+k)이므로 −4ac=−4·(−(2+k))=+4(2+k)예요. 부호 확인!',
    C:'✗ 다시 시도! 4+4(2+k)=4+8+4k=12+4k예요. +16이 아니에요.',
  },
  p3q1:{
    A:'✗ 다시 시도! 4k+12>0 → 4k>−12 → k>−3이에요. 부등호 방향 확인!',
    B:'✓ 정답! D=4k+12>0 → 4k>−12 → k>−3',
    C:'✗ 다시 시도! 4k>−12에서 양변을 4로 나누면 k>−3이에요.',
  },
  p3q2:{
    A:'✓ 정답! D=4k+12=0 → 4k=−12 → k=−3',
    B:'✗ 다시 시도! 4k=−12 → k=−3이에요. +3이 아니에요.',
    C:'✗ 다시 시도! 12를 4로 나누면 3이에요. k=−3이에요.',
  },
  p3q3:{
    A:'✗ 다시 시도! D<0이 되려면 4k+12<0 → 4k<−12 → k<?',
    B:'✗ 다시 시도! 4k<−12 → k<−3이에요. <3이 아니에요.',
    C:'✓ 정답! D=4k+12<0 → 4k<−12 → k<−3',
  },
  c1:{
    A:'✗ 다시 시도! kx를 이항하면 −kx예요. −2x−kx=−(2+k)x이고, 상수항은 1−4=−3이에요.',
    B:'✗ 다시 시도! 상수항은 1−4=−3이어야 해요. +5가 아니에요.',
    C:'✓ 정답! x²−2x+1=kx+4 → x²−(2+k)x+(1−4)=0 → x²−(2+k)x−3=0',
  },
  c2:{
    A:'✗ 다시 시도! c=−3이므로 −4ac=−4·(−3)=+12예요. 부호 확인!',
    B:'✓ 정답! D=(2+k)²−4·(−3)=(2+k)²+12',
    C:'✗ 다시 시도! b=−(2+k)이므로 b²=(2+k)²이에요. (k−2)²이 아니에요.',
  },
  c3:{
    A:'✓ 정답! 어떤 실수 제곱도 ≥0이므로 (2+k)²≥0 → D=(2+k)²+12≥12>0',
    B:'✗ 다시 시도! 12만으로는 부족해요. (2+k)²≥0임도 함께 사용해야 해요.',
    C:'✗ 다시 시도! k는 음수일 수도 있어요. (2+k)²의 성질로 설명해야 해요.',
  },
  g1:{
    A:'✗ 다시 시도! x=0을 대입하면 y=k·0+4=4이에요. (4,0)이 아니에요.',
    B:'✗ 다시 시도! x=0을 대입하면 y=4예요. k와는 무관해요.',
    C:'✓ 정답! x=0 대입 → y=k·0+4=4. 기울기 k에 관계없이 항상 (0,4)!',
  },
  g2:{
    A:'✗ 다시 시도! x=0을 y=x²−2x+1에 대입하면 0−0+1=1이에요. y=3이 아니에요.',
    B:'✓ 정답! y=0²−2·0+1=1. 고정점 y좌표 4>1 → 고정점이 포물선보다 위에 있어요!',
    C:'✗ 다시 시도! x=0일 때 포물선값은 1이에요. 4가 아니에요.',
  },
  g3:{
    A:'✓ 정답! y=(x−1)²이므로 꼭짓점 (1,0), 최솟값 0. 양끝으로 +∞!',
    B:'✗ 다시 시도! y=(x−1)²로 변환하면 꼭짓점 x좌표는 +1이에요. −1이 아니에요.',
    C:'✗ 다시 시도! y=x²−2x+1=(x−1)²+?로 변환해 보세요.',
  },
};

const answered = {};

// sets of questions that need ALL correct to unlock next step
const p1Keys   = ['s1','s2','q1','q2','q3'];
const p2Keys   = ['p2s1','p2s2','p2q1','p2q2','p2q3'];
const p3Keys   = ['p3s1','p3s2','p3q1','p3q2','p3q3'];
const challM1  = ['c1','c2','c3'];
const challAll = ['c1','c2','c3','g1','g2','g3'];

function ans(q, v){
  if(answered[q]) return;
  answered[q] = v;

  const isRight = CORRECT[q] === v;
  const fb = document.getElementById(q+'fb');
  fb.className = 'fb ' + (isRight ? 'ok' : 'ng');
  fb.textContent = (HINTS[q] && HINTS[q][v]) || (isRight ? '✓ 정답!' : '✗ 다시 시도!');

  document.querySelectorAll(`[data-q="${q}"]`).forEach(btn=>{
    btn.disabled = true;
    if(btn.dataset.v === CORRECT[q]) btn.classList.add('correct');
    else if(btn.dataset.v === v && !isRight) btn.classList.add('wrong');
  });

  if(p1Keys.every(k=>answered[k]===CORRECT[k]))
    document.getElementById('p1Done').classList.remove('hidden');
  if(p2Keys.every(k=>answered[k]===CORRECT[k]))
    document.getElementById('p2Done').classList.remove('hidden');
  if(p3Keys.every(k=>answered[k]===CORRECT[k]))
    document.getElementById('p3Done').classList.remove('hidden');

  if(challM1.every(k=>answered[k]===CORRECT[k]))
    document.getElementById('graphExplain').style.display='block';
  if(challAll.every(k=>answered[k]===CORRECT[k]))
    document.getElementById('challDone').classList.remove('hidden');

  scheduleResize(80);
}
</script>
</body>
</html>"""


def render():
    st.set_page_config(page_title="이차함수·직선 위치관계 실험실", layout="wide")
    st.markdown(
        "<style>.main{max-width:100%}iframe{width:100%!important}</style>",
        unsafe_allow_html=True,
    )
    components.html(_HTML, height=1800, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
