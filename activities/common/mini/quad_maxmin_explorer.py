# activities/common/mini/quad_maxmin_explorer.py
"""
이차함수의 최대·최소 탐구 실험실
실수 전체 / 닫힌 구간 / 열린 구간에서 이차함수의 최댓값·최솟값을
인터랙티브 그래프로 탐구하는 미니활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "이차함수최대최소탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 탐구를 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "실수전체",
        "label":  "실수 전체에서 이차함수 y=a(x-p)²+q의 최대·최소는 어떻게 결정되나요? a의 부호와 꼭짓점을 연결하여 설명하세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "닫힌구간케이스",
        "label":  "닫힌 구간 [α, β]에서 최댓값·최솟값을 구할 때, 대칭축 x=p의 위치에 따라 왜 케이스를 나눠야 하는지 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "열린구간차이",
        "label":  "열린 구간 (α, β)에서는 닫힌 구간과 달리 최대·최솟값이 존재하지 않을 수 있습니다. 어떤 경우에 존재하지 않는지, 그래프를 이용해 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "끝값포함이유",
        "label":  "구간의 끝점 포함 여부(열린/닫힌)가 최대·최솟값의 존재에 영향을 미치는 이유를 자신의 말로 설명하세요.",
        "type":   "text_area",
        "height": 100,
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
    "title":       "📈 이차함수의 최대·최소 탐구",
    "description": "실수 전체·닫힌 구간·열린 구간에서 이차함수의 최댓값과 최솟값이 어떻게 결정되는지 인터랙티브 그래프로 탐구하는 활동입니다.",
    "order":       240,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>이차함수 최대·최소 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(155deg,#060917 0%,#0e1630 60%,#080f1c 100%);
  color:#e2e8ff;
  padding:14px 12px 32px;
  min-height:100vh;
}

/* ── Tabs ── */
.tabs{display:flex;gap:6px;margin-bottom:18px;flex-wrap:wrap}
.tab-btn{
  padding:9px 16px;border:none;border-radius:10px 10px 0 0;
  background:#1a2340;color:#8899cc;cursor:pointer;font-size:.88rem;
  font-family:inherit;transition:all .2s;border-bottom:2px solid transparent;
}
.tab-btn:hover{background:#233060;color:#c0d0ff}
.tab-btn.active{background:#2a3a70;color:#fff;border-bottom:2px solid #6888ff;font-weight:700}
.tab-panel{display:none}
.tab-panel.active{display:block}

/* ── Sections ── */
.sec{
  background:rgba(255,255,255,.04);border:1px solid rgba(100,130,255,.18);
  border-radius:14px;padding:20px 18px;margin-bottom:18px;
}
.sec-title{font-size:1.05rem;font-weight:700;color:#a0c4ff;margin-bottom:10px}
.sec-desc{font-size:.9rem;color:#b0bde0;line-height:1.65;margin-bottom:14px}

/* ── Canvas wrapper ── */
.canvas-wrap{display:flex;justify-content:center;margin:6px 0}
canvas{border-radius:10px;background:#0a0f22;border:1px solid rgba(100,130,255,.25)}

/* ── Zoom bar ── */
.zoom-bar{display:flex;align-items:center;gap:6px;justify-content:flex-end;margin-bottom:4px}
.zoom-bar span.zlabel{font-size:.75rem;color:#5566aa}
.zbtn{
  padding:4px 10px;border-radius:6px;border:1px solid rgba(100,130,255,.35);
  background:rgba(30,50,110,.7);color:#a0c4ff;cursor:pointer;
  font-family:inherit;font-size:.8rem;transition:all .18s;
}
.zbtn:hover{background:rgba(60,90,180,.8);color:#fff}
.zpct{font-size:.78rem;color:#7888bb;min-width:38px;text-align:right}

/* ── Sliders ── */
.ctrl-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px 20px;margin:12px 0}
.ctrl-item{display:flex;flex-direction:column;gap:4px}
.ctrl-label{font-size:.82rem;color:#8899cc}
.ctrl-val{font-size:.85rem;color:#7be0b0;font-weight:700}
input[type=range]{
  width:100%;accent-color:#6888ff;cursor:pointer;height:6px;
}
.ctrl-row{display:flex;align-items:center;gap:8px;margin:4px 0}
.ctrl-row label{font-size:.82rem;color:#b0bde0;cursor:pointer}
input[type=checkbox]{accent-color:#ff8870;width:16px;height:16px;cursor:pointer}

/* ── Info boxes ── */
.info-box{
  background:rgba(100,200,120,.1);border:1px solid rgba(100,200,120,.3);
  border-radius:10px;padding:14px 16px;margin-top:12px;font-size:.88rem;
  line-height:1.7;
}
.warn-box{
  background:rgba(255,180,60,.08);border:1px solid rgba(255,180,60,.3);
  border-radius:10px;padding:14px 16px;margin-top:12px;font-size:.88rem;
  line-height:1.7;
}
.result-box{
  background:rgba(104,136,255,.12);border:1px solid rgba(104,136,255,.35);
  border-radius:12px;padding:16px 18px;margin-top:14px;
}
.result-title{font-size:.88rem;color:#7cb0ff;margin-bottom:8px;font-weight:700}
.result-val{font-size:1.05rem;font-weight:700;color:#fff;line-height:1.8}
.tag-max{color:#ff8870;font-weight:700}
.tag-min{color:#7be0b0;font-weight:700}
.tag-none{color:#ff6b6b;font-style:italic}

/* ── Case badges ── */
.case-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}
.case-card{
  background:rgba(255,255,255,.05);border:1px solid rgba(100,130,255,.2);
  border-radius:10px;padding:12px;cursor:pointer;transition:all .2s;
}
.case-card:hover{background:rgba(104,136,255,.15);border-color:#6888ff}
.case-card.active{background:rgba(104,136,255,.22);border-color:#88aaff;box-shadow:0 0 10px rgba(104,136,255,.3)}
.case-card h4{font-size:.85rem;color:#a0c4ff;margin-bottom:6px}
.case-card p{font-size:.78rem;color:#8899cc;line-height:1.5}

/* ── Quiz ── */
.quiz-wrap{margin-top:10px}
.quiz-q{font-size:.92rem;color:#c8d8ff;margin-bottom:10px;line-height:1.6}
.quiz-opts{display:flex;flex-direction:column;gap:7px}
.opt-btn{
  padding:9px 14px;border-radius:9px;border:1px solid rgba(100,130,255,.3);
  background:rgba(255,255,255,.04);color:#b0bde0;cursor:pointer;text-align:left;
  font-family:inherit;font-size:.86rem;transition:all .2s;
}
.opt-btn:hover{background:rgba(104,136,255,.18);color:#fff}
.opt-btn.correct{background:rgba(60,200,100,.2);border-color:#3cc864;color:#7be0b0}
.opt-btn.wrong{background:rgba(255,80,80,.15);border-color:#ff5050;color:#ff8888}
.quiz-feedback{margin-top:10px;font-size:.88rem;line-height:1.6;padding:10px 14px;border-radius:9px}
.quiz-feedback.ok{background:rgba(60,200,100,.1);border:1px solid rgba(60,200,100,.3);color:#7be0b0}
.quiz-feedback.ng{background:rgba(255,80,80,.1);border:1px solid rgba(255,80,80,.3);color:#ff8888}
.quiz-nav{display:flex;gap:10px;margin-top:14px;align-items:center}
.nav-btn{
  padding:8px 18px;border-radius:9px;border:none;background:#2a3a70;
  color:#c0d0ff;cursor:pointer;font-family:inherit;font-size:.86rem;
  transition:background .2s;
}
.nav-btn:hover{background:#3a4e90}
.quiz-progress{font-size:.8rem;color:#6677aa;margin-left:auto}

/* ── Highlight ── */
.hl{color:#ffd700;font-weight:700}
.hl-green{color:#7be0b0;font-weight:700}
.hl-red{color:#ff8870;font-weight:700}
.hl-blue{color:#88ccff;font-weight:700}

/* ── Axis concept cards ── */
.concept-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0}
.concept-card{
  background:rgba(255,255,255,.05);border:1px solid rgba(100,130,255,.2);
  border-radius:12px;padding:14px;
}
.concept-card h3{font-size:.9rem;color:#a0c4ff;margin-bottom:8px}
.concept-card p{font-size:.82rem;color:#8899cc;line-height:1.6}
.sym-tag{display:inline-block;padding:2px 8px;border-radius:6px;font-size:.8rem;font-weight:700;margin:2px}
.sym-a-pos{background:rgba(120,200,255,.2);color:#88ddff}
.sym-a-neg{background:rgba(255,150,100,.2);color:#ffaa80}

.step-list{list-style:none;padding:0;margin:8px 0}
.step-list li{
  padding:6px 10px 6px 28px;position:relative;font-size:.85rem;
  color:#b0bde0;line-height:1.5;border-left:2px solid rgba(104,136,255,.3);
  margin-bottom:4px;
}
.step-list li::before{
  content:attr(data-n);position:absolute;left:-12px;top:6px;
  width:20px;height:20px;background:#2a3a70;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:.75rem;color:#88aaff;font-weight:700;
  line-height:20px;text-align:center;
}
</style>
</head>
<body>

<!-- ═══ MAIN TABS ═══ -->
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('t1',this)">🌐 탭 1 · 실수 전체에서 최대·최소</button>
  <button class="tab-btn" onclick="switchTab('t2',this)">📏 탭 2 · 닫힌 구간 케이스 분석</button>
  <button class="tab-btn" onclick="switchTab('t3',this)">🔬 탭 3 · 인터랙티브 그래프 실험실</button>
  <button class="tab-btn" onclick="switchTab('t4',this)">✏️ 탭 4 · 연습 문제</button>
</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- TAB 1: 실수 전체에서 최대·최소 -->
<!-- ══════════════════════════════════════════════════ -->
<div class="tab-panel active" id="tab-t1">

<div class="sec">
  <div class="sec-title">🌐 실수 전체에서 이차함수의 최대·최소</div>
  <div class="sec-desc">
    이차함수 <span class="hl">y = a(x−p)² + q</span>에서 a의 부호에 따라 최대·최소가 달라집니다.<br>
    아래 슬라이더로 <strong>a, p, q</strong>를 바꿔 보면서 그래프 모양과 최대·최소 관계를 탐구해 보세요.
  </div>

  <div class="ctrl-grid">
    <div class="ctrl-item">
      <span class="ctrl-label">계수 a (<span id="t1aVal">1.0</span>)</span>
      <input type="range" id="t1a" min="-3" max="3" step="0.5" value="1" oninput="drawT1()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">꼭짓점 x좌표 p (<span id="t1pVal">0</span>)</span>
      <input type="range" id="t1p" min="-4" max="4" step="0.5" value="0" oninput="drawT1()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">꼭짓점 y좌표 q (<span id="t1qVal">0</span>)</span>
      <input type="range" id="t1q" min="-4" max="4" step="0.5" value="0" oninput="drawT1()">
    </div>
  </div>

  <div class="zoom-bar">
    <span class="zlabel">확대·축소</span>
    <button class="zbtn" onclick="chZoom('t1',1.25)">＋</button>
    <button class="zbtn" onclick="chZoom('t1',0.8)">－</button>
    <button class="zbtn" onclick="chZoom('t1',0)">↺</button>
    <span class="zpct" id="t1ZP">100%</span>
  </div>
  <div class="canvas-wrap"><canvas id="c1" width="520" height="320"></canvas></div>

  <div class="result-box" id="t1result">
    <div class="result-title">📊 분석 결과</div>
    <div class="result-val" id="t1msg">슬라이더를 움직여 보세요.</div>
  </div>
</div>

<div class="sec">
  <div class="sec-title">💡 핵심 정리</div>
  <div class="concept-grid">
    <div class="concept-card">
      <h3><span class="sym-tag sym-a-pos">a &gt; 0</span> 아래로 볼록</h3>
      <p>
        꼭짓점이 <strong>가장 낮은 점</strong>이므로<br>
        x = p일 때 <span class="tag-min">최솟값 q</span>를 가집니다.<br><br>
        최댓값은 <span class="tag-none">존재하지 않습니다</span><br>
        (x → ±∞이면 y → +∞)
      </p>
    </div>
    <div class="concept-card">
      <h3><span class="sym-tag sym-a-neg">a &lt; 0</span> 위로 볼록</h3>
      <p>
        꼭짓점이 <strong>가장 높은 점</strong>이므로<br>
        x = p일 때 <span class="tag-max">최댓값 q</span>를 가집니다.<br><br>
        최솟값은 <span class="tag-none">존재하지 않습니다</span><br>
        (x → ±∞이면 y → −∞)
      </p>
    </div>
  </div>
  <div class="info-box">
    ⚠️ <strong>a = 0이면 이차함수가 아닙니다!</strong> 반드시 a ≠ 0이어야 합니다.<br>
    슬라이더에서 a = 0 근처로 가면 어떻게 되는지 확인해 보세요.
  </div>
</div>

</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- TAB 2: 닫힌 구간 케이스 분석 -->
<!-- ══════════════════════════════════════════════════ -->
<div class="tab-panel" id="tab-t2">

<div class="sec">
  <div class="sec-title">📏 닫힌 구간 [α, β]에서의 최대·최소</div>
  <div class="sec-desc">
    닫힌 구간에서는 <span class="hl">대칭축(꼭짓점) x = p</span>와 <span class="hl">양 끝점 x = α, x = β</span>에서 최대·최소가 결정됩니다.<br>
    대칭축이 구간 안에 있는지 밖에 있는지에 따라 케이스가 달라집니다.
  </div>

  <div class="case-grid">
    <div class="case-card active" id="case1" onclick="selectCase(1)">
      <h4>📌 케이스 1 · α ≤ p ≤ β (대칭축이 구간 안)</h4>
      <p>꼭짓점이 구간 안에 있으므로<br>x=α, x=p, x=β의 함수값을 비교</p>
    </div>
    <div class="case-card" id="case2" onclick="selectCase(2)">
      <h4>📌 케이스 2 · p &lt; α (대칭축이 구간 왼쪽)</h4>
      <p>구간 안에서 단조증가(a>0) 또는<br>단조감소(a<0) → 끝점만 비교</p>
    </div>
    <div class="case-card" id="case3" onclick="selectCase(3)">
      <h4>📌 케이스 3 · p &gt; β (대칭축이 구간 오른쪽)</h4>
      <p>구간 안에서 단조감소(a>0) 또는<br>단조증가(a<0) → 끝점만 비교</p>
    </div>
    <div class="case-card" id="case4" onclick="selectCase(4)">
      <h4>📌 케이스 4 · 혼합 연습</h4>
      <p>직접 슬라이더를 조작하여<br>케이스를 판별하는 연습</p>
    </div>
  </div>

  <div class="zoom-bar">
    <span class="zlabel">확대·축소</span>
    <button class="zbtn" onclick="chZoom('t2',1.25)">＋</button>
    <button class="zbtn" onclick="chZoom('t2',0.8)">－</button>
    <button class="zbtn" onclick="chZoom('t2',0)">↺</button>
    <span class="zpct" id="t2ZP">100%</span>
  </div>
  <canvas id="c2" width="520" height="300" style="display:block;margin:4px auto;border-radius:10px;background:#0a0f22;border:1px solid rgba(100,130,255,.25)"></canvas>

  <div id="caseControls" style="display:none;margin:8px 0">
    <div class="ctrl-grid">
      <div class="ctrl-item">
        <span class="ctrl-label">계수 a (<span id="c4aVal">1.0</span>)</span>
        <input type="range" id="c4a" min="-2" max="2" step="0.5" value="1" oninput="drawCase4()">
      </div>
      <div class="ctrl-item">
        <span class="ctrl-label">대칭축 p (<span id="c4pVal">0</span>)</span>
        <input type="range" id="c4p" min="-5" max="5" step="0.5" value="0" oninput="drawCase4()">
      </div>
      <div class="ctrl-item">
        <span class="ctrl-label">왼쪽 끝 α (<span id="c4aLVal">-2</span>)</span>
        <input type="range" id="c4aL" min="-5" max="4" step="0.5" value="-2" oninput="drawCase4()">
      </div>
      <div class="ctrl-item">
        <span class="ctrl-label">오른쪽 끝 β (<span id="c4bVal">2</span>)</span>
        <input type="range" id="c4b" min="-4" max="5" step="0.5" value="2" oninput="drawCase4()">
      </div>
    </div>
  </div>

  <div class="result-box" id="caseResult">
    <div class="result-title" id="caseResTitle">케이스 1 분석</div>
    <div class="result-val" id="caseResMsg"></div>
  </div>
</div>

<div class="sec">
  <div class="sec-title">📝 최대·최소 구하는 방법 요약</div>
  <ul class="step-list">
    <li data-n="1">함수식을 <strong>y = a(x−p)² + q</strong> (꼭짓점 형태)로 변환합니다.</li>
    <li data-n="2">대칭축 <strong>x = p</strong>와 구간 [α, β]의 관계를 파악합니다.</li>
    <li data-n="3">대칭축이 구간 안에 있으면 <strong>x=α, x=p, x=β</strong>의 함수값을 모두 구합니다.</li>
    <li data-n="4">대칭축이 구간 밖에 있으면 <strong>x=α, x=β</strong>의 함수값만 비교합니다.</li>
    <li data-n="5">그 중 가장 큰 값이 최댓값, 가장 작은 값이 최솟값입니다.</li>
  </ul>
</div>

</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- TAB 3: 인터랙티브 실험실 -->
<!-- ══════════════════════════════════════════════════ -->
<div class="tab-panel" id="tab-t3">

<div class="sec">
  <div class="sec-title">🔬 인터랙티브 그래프 실험실</div>
  <div class="sec-desc">
    계수·꼭짓점·구간을 자유롭게 조작하고, <strong>구간의 끝점 포함 여부(열린/닫힌)</strong>를 바꿔 보세요.<br>
    그래프에서 최댓값·최솟값이 어떻게 달라지는지 직접 확인할 수 있습니다.
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 24px;margin:10px 0">
    <div class="ctrl-item">
      <span class="ctrl-label">계수 a (<span id="t3aVal">1.0</span>)</span>
      <input type="range" id="t3a" min="-3" max="3" step="0.5" value="1" oninput="drawT3()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">꼭짓점 p (<span id="t3pVal">0</span>)</span>
      <input type="range" id="t3p" min="-5" max="5" step="0.5" value="0" oninput="drawT3()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">꼭짓점 q (<span id="t3qVal">0</span>)</span>
      <input type="range" id="t3q" min="-5" max="5" step="0.5" value="0" oninput="drawT3()">
    </div>
    <div class="ctrl-item" style="grid-column:1/-1">
      <span class="ctrl-label" style="margin-bottom:2px">구간 설정 (α ≤ β)</span>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
        <div>
          <div style="display:flex;justify-content:space-between;font-size:.8rem;color:#7899bb;margin-bottom:2px">
            <span>왼쪽 끝 α</span><span id="t3aLVal">-3</span>
          </div>
          <input type="range" id="t3aL" min="-8" max="7" step="0.5" value="-3" oninput="drawT3()">
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;font-size:.8rem;color:#7899bb;margin-bottom:2px">
            <span>오른쪽 끝 β</span><span id="t3bVal">3</span>
          </div>
          <input type="range" id="t3b" min="-7" max="8" step="0.5" value="3" oninput="drawT3()">
        </div>
      </div>
    </div>
    <div style="display:flex;gap:24px;grid-column:1/-1;margin-top:4px">
      <div class="ctrl-row">
        <input type="checkbox" id="t3leftClose" checked onchange="drawT3()">
        <label for="t3leftClose">왼쪽 끝 <span style="color:#ff8870">α 포함</span> (닫힌 쪽)</label>
      </div>
      <div class="ctrl-row">
        <input type="checkbox" id="t3rightClose" checked onchange="drawT3()">
        <label for="t3rightClose">오른쪽 끝 <span style="color:#ff8870">β 포함</span> (닫힌 쪽)</label>
      </div>
    </div>
  </div>

  <div class="zoom-bar">
    <span class="zlabel">확대·축소</span>
    <button class="zbtn" onclick="chZoom('t3',1.25)">＋</button>
    <button class="zbtn" onclick="chZoom('t3',0.8)">－</button>
    <button class="zbtn" onclick="chZoom('t3',0)">↺</button>
    <span class="zpct" id="t3ZP">100%</span>
  </div>
  <div class="canvas-wrap"><canvas id="c3" width="540" height="340"></canvas></div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px">
    <div class="result-box">
      <div class="result-title">📊 최댓값</div>
      <div class="result-val" id="t3max">—</div>
    </div>
    <div class="result-box">
      <div class="result-title">📊 최솟값</div>
      <div class="result-val" id="t3min">—</div>
    </div>
  </div>

  <div class="result-box" style="margin-top:10px">
    <div class="result-title">🔍 현재 상태 분석</div>
    <div class="result-val" id="t3analysis" style="font-size:.88rem;line-height:1.8"></div>
  </div>
</div>

<div class="sec">
  <div class="sec-title">🧪 탐구 미션</div>
  <div class="sec-desc" style="margin-bottom:0">
    아래 상황을 만들어 보고 무슨 일이 일어나는지 관찰하세요!
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px">
    <button class="opt-btn" onclick="setPreset(1)">🎯 미션 1: 꼭짓점이 구간 정중앙</button>
    <button class="opt-btn" onclick="setPreset(2)">🎯 미션 2: 꼭짓점이 구간 왼쪽 밖</button>
    <button class="opt-btn" onclick="setPreset(3)">🎯 미션 3: 열린구간, 최솟값 없음</button>
    <button class="opt-btn" onclick="setPreset(4)">🎯 미션 4: 열린구간, 최댓값도 없음</button>
    <button class="opt-btn" onclick="setPreset(5)">🎯 미션 5: a&lt;0, 꼭짓점이 구간 안</button>
    <button class="opt-btn" onclick="setPreset(6)">🎯 미션 6: 아주 좁은 구간 탐색</button>
  </div>
  <div class="info-box" id="missionMsg" style="display:none;margin-top:10px"></div>
</div>

</div>

<!-- ══════════════════════════════════════════════════ -->
<!-- TAB 4: 연습 문제 -->
<!-- ══════════════════════════════════════════════════ -->
<div class="tab-panel" id="tab-t4">

<div class="sec">
  <div class="sec-title">✏️ 연습 문제</div>
  <div class="sec-desc">탐구한 내용을 바탕으로 문제를 풀어 보세요. 힌트를 활용할 수 있습니다.</div>

  <div class="quiz-wrap" id="quizWrap">
    <!-- 문제는 JS로 렌더링 -->
  </div>
  <div class="quiz-nav">
    <button class="nav-btn" onclick="prevQuiz()">◀ 이전</button>
    <button class="nav-btn" onclick="nextQuiz()">다음 ▶</button>
    <span class="quiz-progress" id="quizProg">1 / 6</span>
  </div>
</div>

</div>

<!-- ═══════════ JAVASCRIPT ═══════════ -->
<script>
/* ─── Tab switch ─── */
function switchTab(id, btn){
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  btn.classList.add('active');
  if(id==='t1') setTimeout(drawT1,50);
  if(id==='t2') setTimeout(()=>selectCase(currentCase),50);
  if(id==='t3') setTimeout(drawT3,50);
  if(id==='t4') setTimeout(renderQuiz,50);
}

/* ═══════════════════════════════════════
   공통 드로잉 유틸리티
   ─ 뷰포트 자동 계산 + 줌 지원
═══════════════════════════════════════ */

// 탭별 줌 배율
const zoom={t1:1.0, t2:1.0, t3:1.0};

function chZoom(tab, factor){
  if(factor===0) zoom[tab]=1.0;
  else zoom[tab]=Math.max(0.15, Math.min(8, zoom[tab]*factor));
  document.getElementById(tab+'ZP').textContent=Math.round(zoom[tab]*100)+'%';
  if(tab==='t1') drawT1();
  else if(tab==='t2'){ if(currentCase<4) drawCase(currentCase); else drawCase4(); }
  else if(tab==='t3') drawT3();
}

/**
 * 주요 세계 좌표 포인트들을 받아 캔버스에 맞는 뷰포트를 계산한다.
 * @returns {ox, oy, sc, xMin, xMax, yMin, yMax} - 캔버스 원점, 스케일, 가시 세계 범위
 */
function computeView(keyXs, keyYs, W, H, zoomFactor){
  let xLo=Math.min(...keyXs), xHi=Math.max(...keyXs);
  let yLo=Math.min(...keyYs), yHi=Math.max(...keyYs);
  let xSpan=Math.max(xHi-xLo, 2);
  let ySpan=Math.max(yHi-yLo, 2);
  // 여백 추가
  let xPad=xSpan*0.22, yPad=ySpan*0.22;
  let x0=xLo-xPad, x1=xHi+xPad;
  let y0=yLo-yPad, y1=yHi+yPad;
  // 레이블 여백을 고려한 스케일 계산
  let margin=44;
  let scX=(W-margin*2)/(x1-x0);
  let scY=(H-margin*2)/(y1-y0);
  let sc=Math.min(scX,scY)*zoomFactor;
  sc=Math.max(3, Math.min(250, sc));
  // 중심 맞추기
  let midX=(x0+x1)/2, midY=(y0+y1)/2;
  let ox=W/2 - midX*sc;
  let oy=H/2 + midY*sc;
  // 가시 세계 범위 (캔버스 전체 기준)
  return {
    ox, oy, sc,
    xMin: -ox/sc,      xMax: (W-ox)/sc,
    yMin: (oy-H)/sc,   yMax: oy/sc
  };
}

/** 그리드 간격을 보기 좋은 값으로 선택 */
function niceStep(span){
  if(span<=0) return 1;
  let rough=span/6;
  let p=Math.pow(10, Math.floor(Math.log10(rough)));
  let f=rough/p;
  return (f<1.5?1 : f<3.5?2 : f<7.5?5 : 10)*p;
}

/** 축 + 격자 그리기 (뷰포트 자동) */
function drawAxesAuto(ctx, W, H, v){
  let {ox,oy,sc,xMin,xMax,yMin,yMax}=v;
  let xStep=niceStep(xMax-xMin);
  let yStep=niceStep(yMax-yMin);

  // 격자
  ctx.setLineDash([3,5]); ctx.lineWidth=1;
  ctx.strokeStyle='rgba(150,170,220,.3)';
  for(let gx=Math.ceil(xMin/xStep)*xStep; gx<=xMax*1.001; gx+=xStep){
    let px=ox+gx*sc;
    ctx.beginPath();ctx.moveTo(px,0);ctx.lineTo(px,H);ctx.stroke();
  }
  for(let gy=Math.ceil(yMin/yStep)*yStep; gy<=yMax*1.001; gy+=yStep){
    let py=oy-gy*sc;
    ctx.beginPath();ctx.moveTo(0,py);ctx.lineTo(W,py);ctx.stroke();
  }
  ctx.setLineDash([]);

  // x축, y축
  ctx.strokeStyle='rgba(180,200,255,.75)'; ctx.lineWidth=1.5;
  let ayC=Math.max(0,Math.min(H,oy)); // x축 y 위치 (캔버스 내 클램프)
  let axC=Math.max(0,Math.min(W,ox)); // y축 x 위치
  ctx.beginPath();ctx.moveTo(0,ayC);ctx.lineTo(W,ayC);ctx.stroke();
  ctx.beginPath();ctx.moveTo(axC,0);ctx.lineTo(axC,H);ctx.stroke();

  // 눈금 레이블
  ctx.fillStyle='rgba(160,180,230,.8)'; ctx.font='10px sans-serif';
  for(let gx=Math.ceil(xMin/xStep)*xStep; gx<=xMax*1.001; gx+=xStep){
    if(Math.abs(gx)<xStep*0.05) continue;
    let px=ox+gx*sc;
    let ly=Math.min(Math.max(oy,8),H-6)+12;
    ctx.textAlign='center';
    let lbl=parseFloat(gx.toFixed(4));
    ctx.fillText(lbl, px, ly);
  }
  for(let gy=Math.ceil(yMin/yStep)*yStep; gy<=yMax*1.001; gy+=yStep){
    if(Math.abs(gy)<yStep*0.05) continue;
    let py=oy-gy*sc;
    let lx=Math.min(Math.max(ox,4),W-4)-4;
    ctx.textAlign='right';
    let lbl=parseFloat(gy.toFixed(4));
    ctx.fillText(lbl, lx, py+4);
  }

  // 축 이름
  ctx.fillStyle='rgba(190,210,255,.9)'; ctx.font='bold 12px sans-serif';
  ctx.textAlign='center';
  ctx.fillText('x', W-6, Math.min(Math.max(oy-6,10),H-4));
  ctx.fillText('y', Math.min(Math.max(ox+10,10),W-4), 10);
  if(oy>=0&&oy<=H&&ox>=0&&ox<=W)
    ctx.fillText('O', Math.max(ox-8,6), Math.min(oy+14,H-4));
}

/** 포물선 경로 그리기 */
function drawParabola(ctx, a, p, q, v, xFrom, xTo, color, dash){
  let {ox,oy,sc}=v;
  ctx.strokeStyle=color; ctx.lineWidth=2.5;
  ctx.setLineDash(dash?[6,5]:[]);
  ctx.beginPath();
  let steps=Math.max(200, Math.round((xTo-xFrom)*60));
  let dx=(xTo-xFrom)/steps;
  let first=true;
  for(let i=0;i<=steps;i++){
    let wx=xFrom+i*dx;
    let wy=a*(wx-p)*(wx-p)+q;
    let px2=ox+wx*sc, py2=oy-wy*sc;
    if(first){ctx.moveTo(px2,py2);first=false;}else ctx.lineTo(px2,py2);
  }
  ctx.stroke(); ctx.setLineDash([]);
}

/** 점 그리기 (filled=채워진 원, 아니면 빈 원) */
function dot(ctx, wx, wy, v, color, filled, r){
  r=r||6;
  let px2=v.ox+wx*v.sc, py2=v.oy-wy*v.sc;
  ctx.beginPath();ctx.arc(px2,py2,r,0,Math.PI*2);
  if(filled){ctx.fillStyle=color;ctx.fill();}
  else{ctx.strokeStyle=color;ctx.lineWidth=2.5;ctx.stroke();}
}

/** 텍스트 레이블 */
function label(ctx, text, wx, wy, v, color, offX, offY){
  let px2=v.ox+wx*v.sc, py2=v.oy-wy*v.sc;
  ctx.fillStyle=color||'#fff';
  ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
  ctx.fillText(text, px2+(offX||0), py2+(offY||-10));
}

/** 수평 점선 (최대·최소 표시선) */
function hDash(ctx, wy, v, W, color){
  let py2=v.oy-wy*v.sc;
  ctx.strokeStyle=color; ctx.lineWidth=1; ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(0,py2);ctx.lineTo(W,py2);ctx.stroke();
  ctx.setLineDash([]);
}

/** 수직 점선 (대칭축) */
function vDash(ctx, wx, v, H, color){
  let px2=v.ox+wx*v.sc;
  ctx.strokeStyle=color; ctx.lineWidth=1.5; ctx.setLineDash([5,4]);
  ctx.beginPath();ctx.moveTo(px2,0);ctx.lineTo(px2,H);ctx.stroke();
  ctx.setLineDash([]);
}

/* ═══════════════════════════════════════
   TAB 1 · 실수 전체에서 최대·최소
═══════════════════════════════════════ */
function drawT1(){
  let a=parseFloat(document.getElementById('t1a').value)||0.1;
  let p=parseFloat(document.getElementById('t1p').value);
  let q=parseFloat(document.getElementById('t1q').value);
  document.getElementById('t1aVal').textContent=a.toFixed(1);
  document.getElementById('t1pVal').textContent=p.toFixed(1);
  document.getElementById('t1qVal').textContent=q.toFixed(1);

  let cvs=document.getElementById('c1');
  let W=cvs.width, H=cvs.height;
  let ctx=cvs.getContext('2d');
  ctx.clearRect(0,0,W,H);

  // 뷰포트 자동 계산: 꼭짓점 ± xSpread 범위
  let xSpread=Math.max(3.5, Math.min(9, 2.8/Math.sqrt(Math.abs(a))));
  let keyXs=[p-xSpread, p, p+xSpread];
  let keyYs=keyXs.map(x=>a*(x-p)*(x-p)+q);

  let v=computeView(keyXs, keyYs, W, H, zoom.t1);
  drawAxesAuto(ctx,W,H,v);

  // 전체 포물선 (점선: 무한히 연장됨을 암시)
  drawParabola(ctx,a,p,q,v, v.xMin, v.xMax, 'rgba(104,136,255,.3)', true);
  // 실선 포물선
  drawParabola(ctx,a,p,q,v, v.xMin, v.xMax, '#6888ff', false);

  // 대칭축 점선
  vDash(ctx,p,v,H,'rgba(255,215,0,.4)');
  ctx.fillStyle='rgba(255,215,0,.7)';ctx.font='11px sans-serif';ctx.textAlign='center';
  let vxPx=v.ox+p*v.sc;
  ctx.fillText(`x=${p}`, vxPx, 13);

  // 꼭짓점
  dot(ctx,p,q,v,'#ffd700',true,8);
  let offY=a>0?-16:10;
  label(ctx,`꼭짓점 (${p}, ${q})`,p,q,v,'#ffd700',0,offY);

  // 결과 메시지
  let msg='';
  if(a>0){
    msg=`<span class="hl-blue">a = ${a} &gt; 0</span> → 아래로 볼록 포물선<br>`+
        `x = ${p}일 때 <span class="tag-min">최솟값 ${q}</span><br>`+
        `<span class="tag-none">최댓값은 존재하지 않습니다</span> (x → ±∞ 이면 y → +∞)`;
  } else if(a<0){
    msg=`<span class="hl-red">a = ${a} &lt; 0</span> → 위로 볼록 포물선<br>`+
        `x = ${p}일 때 <span class="tag-max">최댓값 ${q}</span><br>`+
        `<span class="tag-none">최솟값은 존재하지 않습니다</span> (x → ±∞ 이면 y → −∞)`;
  } else {
    msg=`<span style="color:#ff6b6b">a = 0 이면 이차함수가 아닙니다!</span>`;
  }
  document.getElementById('t1msg').innerHTML=msg;
}

/* ═══════════════════════════════════════
   TAB 2 · 닫힌 구간 케이스 분석
═══════════════════════════════════════ */
let currentCase=1;
function selectCase(n){
  currentCase=n;
  for(let i=1;i<=4;i++) document.getElementById('case'+i).classList.toggle('active',i===n);
  document.getElementById('caseControls').style.display=(n===4)?'block':'none';
  if(n<4) drawCase(n); else drawCase4();
}

function drawCase(n){
  const presets=[null,
    {a:1, p:0,  q:-1, aL:-3, b:3},
    {a:1, p:-4, q:0,  aL:-2, b:3},
    {a:1, p:4,  q:0,  aL:-3, b:2},
  ];
  let pr=presets[n];
  _drawCase(pr.a, pr.p, pr.q, pr.aL, pr.b, n);
}

function drawCase4(){
  let a=parseFloat(document.getElementById('c4a').value)||0.5;
  let p=parseFloat(document.getElementById('c4p').value);
  let aL=parseFloat(document.getElementById('c4aL').value);
  let b=parseFloat(document.getElementById('c4b').value);
  document.getElementById('c4aVal').textContent=a.toFixed(1);
  document.getElementById('c4pVal').textContent=p.toFixed(1);
  document.getElementById('c4aLVal').textContent=aL.toFixed(1);
  document.getElementById('c4bVal').textContent=b.toFixed(1);
  if(aL>=b) b=aL+0.5;
  _drawCase(a, p, 0, aL, b, 4);
}

function _drawCase(a, p, q, aL, b, caseN){
  if(caseN===4) q=0;

  let fA=a*(aL-p)*(aL-p)+q;
  let fB=a*(b-p)*(b-p)+q;
  let fP=q;
  let inRange=(aL<=p && p<=b);

  // 뷰포트 핵심 포인트 수집
  let span=Math.max(b-aL, 1);
  let kxs=[aL, b, aL-span*0.18, b+span*0.18];
  if(inRange) kxs.push(p);
  let kys=kxs.map(x=>a*(x-p)*(x-p)+q);
  kys.push(0); // 원점 y=0 포함

  let cvs=document.getElementById('c2');
  let W=cvs.width, H=cvs.height;
  let ctx=cvs.getContext('2d');
  ctx.clearRect(0,0,W,H);

  let v=computeView(kxs, kys, W, H, zoom.t2);
  drawAxesAuto(ctx,W,H,v);

  // 전체 포물선 (점선)
  drawParabola(ctx,a,p,q,v, v.xMin, v.xMax, 'rgba(104,136,255,.2)', true);
  // 구간 내 포물선 (실선)
  drawParabola(ctx,a,p,q,v, aL, b, '#6888ff', false);

  // 후보 포인트 및 최대·최소 표시
  let pts=[];
  pts.push({x:aL, y:fA, lbl:`f(α)=${fA.toFixed(2)}`});
  pts.push({x:b,  y:fB, lbl:`f(β)=${fB.toFixed(2)}`});
  if(inRange) pts.push({x:p, y:fP, lbl:`f(p)=${fP.toFixed(2)}`});

  let ys=pts.map(pt=>pt.y);
  let maxY=Math.max(...ys), minY=Math.min(...ys);

  // 최대·최소 수평 점선
  hDash(ctx,maxY,v,W,'rgba(255,136,112,.5)');
  hDash(ctx,minY,v,W,'rgba(123,224,176,.5)');

  // 대칭축 수직 점선
  vDash(ctx,p,v,H,'rgba(255,215,0,.45)');
  ctx.fillStyle='rgba(255,215,0,.75)';ctx.font='11px sans-serif';ctx.textAlign='center';
  ctx.fillText(`x=${p}`, v.ox+p*v.sc, H-5);

  pts.forEach(pt=>{
    let isMax=Math.abs(pt.y-maxY)<0.001;
    let isMin=Math.abs(pt.y-minY)<0.001;
    let col=isMax?'#ff8870':isMin?'#7be0b0':'#ccddff';

    // 강조 링
    if(isMax||isMin){
      let px2=v.ox+pt.x*v.sc, py2=v.oy-pt.y*v.sc;
      ctx.fillStyle=isMax?'rgba(255,136,112,.15)':'rgba(123,224,176,.15)';
      ctx.strokeStyle=isMax?'rgba(255,136,112,.6)':'rgba(123,224,176,.6)';
      ctx.lineWidth=1.5;
      ctx.beginPath();ctx.arc(px2,py2,15,0,Math.PI*2);ctx.fill();ctx.stroke();
    }

    dot(ctx,pt.x,pt.y,v,col,true,7);
    // 레이블 방향: 최대는 위, 최소는 아래 (단 꼭짓점이 바닥이면 반대)
    let lOff=(pt.y>=maxY&&a<0)||(pt.y===minY&&a>0)?-18:14;
    label(ctx,pt.lbl,pt.x,pt.y,v,col,0,lOff);
  });

  // 결과 텍스트
  let titles=['',
    '케이스 1 · 대칭축이 구간 안 (α ≤ p ≤ β)',
    '케이스 2 · 대칭축이 구간 왼쪽 (p &lt; α)',
    '케이스 3 · 대칭축이 구간 오른쪽 (p &gt; β)',
    '직접 조작 결과'];
  let analysis='';
  if(inRange){
    analysis=`대칭축 <span class="hl">x = ${p}</span>이 구간 [${aL}, ${b}] 안에 있습니다.<br>`+
      `x=α(${aL}), x=p(${p}), x=β(${b})의 함수값 비교:<br>`+
      `f(α) = ${fA.toFixed(2)},&nbsp; f(p) = ${fP.toFixed(2)},&nbsp; f(β) = ${fB.toFixed(2)}<br>`+
      `→ <span class="tag-max">최댓값 = ${maxY.toFixed(2)}</span>&nbsp;&nbsp;<span class="tag-min">최솟값 = ${minY.toFixed(2)}</span>`;
  } else {
    analysis=`대칭축 <span class="hl">x = ${p}</span>이 구간 [${aL}, ${b}] 밖에 있습니다.<br>`+
      `끝점 x=α(${aL}), x=β(${b})의 함수값만 비교:<br>`+
      `f(α) = ${fA.toFixed(2)},&nbsp; f(β) = ${fB.toFixed(2)}<br>`+
      `→ <span class="tag-max">최댓값 = ${maxY.toFixed(2)}</span>&nbsp;&nbsp;<span class="tag-min">최솟값 = ${minY.toFixed(2)}</span>`;
  }
  document.getElementById('caseResTitle').innerHTML=titles[caseN];
  document.getElementById('caseResMsg').innerHTML=analysis;
}

/* ═══════════════════════════════════════
   TAB 3 · 인터랙티브 실험실
═══════════════════════════════════════ */
function drawT3(){
  let a=parseFloat(document.getElementById('t3a').value)||0.5;
  let p=parseFloat(document.getElementById('t3p').value);
  let q=parseFloat(document.getElementById('t3q').value);
  let aL=parseFloat(document.getElementById('t3aL').value);
  let b=parseFloat(document.getElementById('t3b').value);
  let lClose=document.getElementById('t3leftClose').checked;
  let rClose=document.getElementById('t3rightClose').checked;

  document.getElementById('t3aVal').textContent=a.toFixed(1);
  document.getElementById('t3pVal').textContent=p.toFixed(1);
  document.getElementById('t3qVal').textContent=q.toFixed(1);
  document.getElementById('t3aLVal').textContent=aL.toFixed(1);
  document.getElementById('t3bVal').textContent=b.toFixed(1);

  if(aL>=b) b=aL+0.5;

  // 후보값 계산
  let fA=a*(aL-p)*(aL-p)+q;
  let fB=a*(b-p)*(b-p)+q;
  let pInside=(p>aL && p<b);
  let pOnLeft=(p===aL), pOnRight=(p===b);

  // 뷰포트 자동 계산: 구간 끝점 + 꼭짓점 + 약간의 여유
  let span=Math.max(b-aL, 1);
  let kxs=[aL, b, aL-span*0.15, b+span*0.15];
  if(pInside||pOnLeft||pOnRight) kxs.push(p);
  let kys=kxs.map(x=>a*(x-p)*(x-p)+q);
  kys.push(0);

  let cvs=document.getElementById('c3');
  let W=cvs.width, H=cvs.height;
  let ctx=cvs.getContext('2d');
  ctx.clearRect(0,0,W,H);

  let v=computeView(kxs, kys, W, H, zoom.t3);
  drawAxesAuto(ctx,W,H,v);

  // 구간 음영
  ctx.fillStyle='rgba(104,136,255,.07)';
  let x1c=v.ox+aL*v.sc, x2c=v.ox+b*v.sc;
  ctx.fillRect(x1c,0,x2c-x1c,H);

  // 전체 포물선 (점선)
  drawParabola(ctx,a,p,q,v, v.xMin,v.xMax, 'rgba(104,136,255,.18)', true);
  // 구간 포물선 (실선)
  let eps=(b-aL)*0.0005;
  drawParabola(ctx,a,p,q,v, aL+(lClose?0:eps), b-(rClose?0:eps), '#6888ff', false);

  // 대칭축 점선
  vDash(ctx,p,v,H,'rgba(255,215,0,.4)');

  // 구간 레이블
  let lBracket=lClose?'[':'(', rBracket=rClose?']':')';
  ctx.fillStyle='rgba(104,136,255,.8)';ctx.font='12px sans-serif';ctx.textAlign='center';
  ctx.fillText(`${lBracket}${aL}, ${b}${rBracket}`, (x1c+x2c)/2, H-5);

  // 꼭짓점 (구간 안에 있을 때)
  if(pInside){
    dot(ctx,p,q,v,'#ffd700',true,6);
  }

  // 끝점 마커 (닫힌=채운 원, 열린=빈 원)
  dot(ctx,aL,fA,v,'#ff8870',lClose,7);
  dot(ctx,b, fB,v,'#ff8870',rClose,7);

  // ── 최대·최소 계산 (샘플링) ──
  let candidates=[];
  if(pInside)   candidates.push({x:p,  y:q});
  if(lClose)    candidates.push({x:aL, y:fA});
  if(rClose)    candidates.push({x:b,  y:fB});
  // 닫힌 경계에서의 꼭짓점 (p=aL 또는 p=b이고 닫힌 경우)
  if(pOnLeft&&lClose)  candidates.push({x:p, y:q});
  if(pOnRight&&rClose) candidates.push({x:p, y:q});

  let pseudoCands=[];
  if(!lClose) pseudoCands.push({x:aL,y:fA});
  if(!rClose) pseudoCands.push({x:b, y:fB});

  // 샘플링으로 실제 극값 추정
  let sampleMax=-Infinity, sampleMin=Infinity;
  let sEps=(b-aL)*0.0005;
  let left=lClose?aL:aL+sEps, right=rClose?b:b-sEps;
  for(let t=0;t<=2000;t++){
    let x=left+(right-left)*t/2000;
    let y=a*(x-p)*(x-p)+q;
    if(y>sampleMax) sampleMax=y;
    if(y<sampleMin) sampleMin=y;
  }

  let attainedMax=candidates.some(c=>Math.abs(c.y-sampleMax)<0.001);
  let attainedMin=candidates.some(c=>Math.abs(c.y-sampleMin)<0.001);
  let boundaryIsMax=pseudoCands.some(c=>Math.abs(c.y-sampleMax)<0.001);
  let boundaryIsMin=pseudoCands.some(c=>Math.abs(c.y-sampleMin)<0.001);

  // ── 최대·최소 강조 표시 ──
  hDash(ctx, sampleMax, v, W, 'rgba(255,136,112,.45)');
  hDash(ctx, sampleMin, v, W, 'rgba(123,224,176,.45)');

  candidates.forEach(c=>{
    let isMax=Math.abs(c.y-sampleMax)<0.001 && attainedMax;
    let isMin=Math.abs(c.y-sampleMin)<0.001 && attainedMin;
    if(isMax){
      dot(ctx,c.x,c.y,v,'#ff8870',true,9);
      label(ctx,'최대',c.x,c.y,v,'#ff8870',0, a<0?-18:14);
    }
    if(isMin){
      dot(ctx,c.x,c.y,v,'#7be0b0',true,9);
      label(ctx,'최소',c.x,c.y,v,'#7be0b0',0, a>0?-18:14);
    }
  });

  // ── 결과 텍스트 ──
  let maxTxt='', minTxt='';
  if(attainedMax)
    maxTxt=`<span class="tag-max">최댓값 = ${sampleMax.toFixed(3)}</span>`;
  else if(boundaryIsMax)
    maxTxt=`<span class="tag-none">최댓값 없음</span> <span style="color:#888;font-size:.85rem">(${sampleMax.toFixed(3)}에 한없이 가까워지지만 도달 안 함)</span>`;
  else
    maxTxt=`<span class="tag-none">최댓값 없음</span>`;

  if(attainedMin)
    minTxt=`<span class="tag-min">최솟값 = ${sampleMin.toFixed(3)}</span>`;
  else if(boundaryIsMin)
    minTxt=`<span class="tag-none">최솟값 없음</span> <span style="color:#888;font-size:.85rem">(${sampleMin.toFixed(3)}에 한없이 가까워지지만 도달 안 함)</span>`;
  else
    minTxt=`<span class="tag-none">최솟값 없음</span>`;

  document.getElementById('t3max').innerHTML=maxTxt;
  document.getElementById('t3min').innerHTML=minTxt;

  let axisInside=(aL<p&&p<b)?'구간 <span class="hl">안</span>에 있습니다':
                 (p<=aL)?'구간의 <span class="hl-red">왼쪽 밖</span>에 있습니다':
                         '구간의 <span class="hl-red">오른쪽 밖</span>에 있습니다';
  document.getElementById('t3analysis').innerHTML=
    `함수: <span class="hl">y = ${a}(x − ${p})² + ${q}</span> &nbsp; 구간: <span class="hl">${lBracket}${aL}, ${b}${rBracket}</span><br>`+
    `대칭축 x = ${p}은 ${axisInside}.<br>`+
    `왼쪽 끝 <span class="hl">${lBracket} = ${lClose?'닫힌(포함)':'열린(미포함)'}</span>,&nbsp;`+
    `오른쪽 끝 <span class="hl">${rBracket} = ${rClose?'닫힌(포함)':'열린(미포함)'}</span>`;
}

/* ─── Presets ─── */
const missionTexts=[null,
  '🎯 미션 1: a=1, p=0, q=0, 구간 [-3, 3], 닫힌구간. 꼭짓점이 정중앙에 있어 최솟값은 꼭짓점 값, 최댓값은 양 끝점 중 더 먼 쪽에서!',
  '🎯 미션 2: a=1, p=-5, 구간 [-2, 3]. 대칭축이 구간 왼쪽 밖 → 구간에서 단조증가 → 최솟값=f(α), 최댓값=f(β)',
  '🎯 미션 3: a=1, p=0, 구간 (-3, 3) 열린구간. 꼭짓점(최솟값 후보)은 구간 안이라 최솟값 존재! 하지만 최댓값은 양 끝이 열려있어 존재하지 않음.',
  '🎯 미션 4: a=1, p=-5, 구간 (-2, 3) 열린구간. 단조증가인데 양 끝 모두 열려있음 → 최솟값도 최댓값도 존재하지 않음!',
  '🎯 미션 5: a=-1(위로볼록), p=1, 구간 [-2, 4]. 꼭짓점이 최댓값 후보, 끝점이 최솟값 후보!',
  '🎯 미션 6: 아주 좁은 구간 [0.9, 1.1]에서의 최대·최소. 구간이 좁아도 원리는 같습니다!'
];
function setPreset(n){
  const presets=[null,
    {a:1,p:0,q:0,aL:-3,b:3,lC:true,rC:true},
    {a:1,p:-5,q:0,aL:-2,b:3,lC:true,rC:true},
    {a:1,p:0,q:0,aL:-3,b:3,lC:false,rC:false},
    {a:1,p:-5,q:0,aL:-2,b:3,lC:false,rC:false},
    {a:-1,p:1,q:2,aL:-2,b:4,lC:true,rC:true},
    {a:2,p:1,q:0,aL:0.9,b:1.1,lC:true,rC:true},
  ];
  let pr=presets[n];
  document.getElementById('t3a').value=pr.a;
  document.getElementById('t3p').value=pr.p;
  document.getElementById('t3q').value=pr.q;
  document.getElementById('t3aL').value=pr.aL;
  document.getElementById('t3b').value=pr.b;
  document.getElementById('t3leftClose').checked=pr.lC;
  document.getElementById('t3rightClose').checked=pr.rC;
  let mBox=document.getElementById('missionMsg');
  mBox.style.display='block';
  mBox.innerHTML=missionTexts[n];
  drawT3();
}

/* ─── TAB 4: Quiz ─── */
const QUIZZES=[
  {
    q:'이차함수 y = (x−2)² − 3에서 실수 전체를 정의역으로 할 때, 다음 중 옳은 것은?',
    opts:['최댓값은 −3이다.','최솟값은 −3이다.','최댓값과 최솟값이 모두 존재한다.','최댓값도 최솟값도 존재하지 않는다.'],
    ans:1,
    hint:'a = 1 > 0이므로 아래로 볼록. 꼭짓점은 (2, −3).',
    exp:'a = 1 > 0이므로 아래로 볼록 포물선. x=2일 때 최솟값 −3. 최댓값은 없음.'
  },
  {
    q:'이차함수 y = −2(x+1)² + 5에서 실수 전체를 정의역으로 할 때 최댓값은?',
    opts:['−1','5','−5','존재하지 않는다'],
    ans:1,
    hint:'a = −2 < 0이므로 위로 볼록. 꼭짓점은 (−1, 5).',
    exp:'a < 0 이므로 위로 볼록. 꼭짓점 (−1, 5)에서 최댓값 5. 최솟값은 없음.'
  },
  {
    q:'y = (x−1)² − 2를 닫힌 구간 [−1, 3]에서 정의할 때, 최댓값은?',
    opts:['−2','2','6','7'],
    ans:1,
    hint:'대칭축 x=1이 [−1, 3] 안에 있음. f(−1), f(1), f(3)을 비교하세요.',
    exp:'f(−1)=(−1−1)²−2=4−2=2, f(1)=0−2=−2, f(3)=(3−1)²−2=4−2=2. 최댓값=2.'
  },
  {
    q:'y = x² − 4x + 3을 닫힌 구간 [0, 5]에서 정의할 때 최솟값은?',
    opts:['3','0','−1','−2'],
    ans:2,
    hint:'완전제곱식으로 변환: y = (x−2)² − 1. 대칭축 x=2가 [0,5] 안.',
    exp:'y=(x−2)²−1. f(0)=3, f(2)=−1, f(5)=8. 최솟값=−1 (x=2에서).'
  },
  {
    q:'y = (x−2)² − 1을 열린 구간 (0, 2)에서 정의할 때 최솟값은?',
    opts:['−1','0','존재하지 않는다','3'],
    ans:2,
    hint:'구간 (0, 2)에서 x=2는 포함되지 않습니다. 대칭축 x=2는 구간 경계에 있어요.',
    exp:'x=2에서 최솟값 −1이 되어야 하지만 x=2는 열린 구간에 포함되지 않음. y는 −1에 가까워지지만 도달하지 않으므로 최솟값 없음.'
  },
  {
    q:'y = −(x−1)² + 4를 닫힌 구간 [−1, 4]에서 정의할 때 최솟값은?',
    opts:['4','−5','0','−1'],
    ans:1,
    hint:'a = −1 < 0이므로 위로 볼록. 끝점에서 최솟값을 찾아야 합니다.',
    exp:'f(−1)=−(−1−1)²+4=−4+4=0, f(1)=4, f(4)=−(4−1)²+4=−9+4=−5. 최솟값=−5 (x=4).'
  },
];

let quizIdx=0;
let quizAnswered=[];

function renderQuiz(){
  if(!QUIZZES) return;
  if(quizAnswered.length!==QUIZZES.length) quizAnswered=Array(QUIZZES.length).fill(null);
  let q=QUIZZES[quizIdx];
  let html=`<div class="quiz-q">문제 ${quizIdx+1}. ${q.q}</div>`;
  html+=`<div class="quiz-opts">`;
  q.opts.forEach((o,i)=>{
    let cls='opt-btn';
    if(quizAnswered[quizIdx]!==null){
      if(i===q.ans) cls+=' correct';
      else if(i===quizAnswered[quizIdx]) cls+=' wrong';
    }
    html+=`<button class="${cls}" onclick="answerQuiz(${i})">${String.fromCharCode(9312+i)} ${o}</button>`;
  });
  html+=`</div>`;
  if(quizAnswered[quizIdx]!==null){
    let ok=(quizAnswered[quizIdx]===q.ans);
    html+=`<div class="quiz-feedback ${ok?'ok':'ng'}">`;
    if(ok) html+=`✅ 정답입니다! ${q.exp}`;
    else html+=`❌ 다시 생각해 보세요. 💡 힌트: ${q.hint}<br><br>정답: ${q.exp}`;
    html+=`</div>`;
  } else {
    html+=`<div style="margin-top:10px;font-size:.8rem;color:#5566aa">💡 힌트: ${q.hint}</div>`;
  }
  document.getElementById('quizWrap').innerHTML=html;
  document.getElementById('quizProg').textContent=`${quizIdx+1} / ${QUIZZES.length}`;
}

function answerQuiz(i){
  if(quizAnswered[quizIdx]!==null) return;
  quizAnswered[quizIdx]=i;
  renderQuiz();
}
function nextQuiz(){if(quizIdx<QUIZZES.length-1){quizIdx++;renderQuiz();}}
function prevQuiz(){if(quizIdx>0){quizIdx--;renderQuiz();}}

/* ─── Init ─── */
window.addEventListener('load',()=>{
  drawT1();
  drawCase(1);
  document.getElementById('caseResMsg').innerHTML=
    '케이스 카드를 클릭하거나 그래프를 확인하세요.';
  // init case1
  setTimeout(()=>{selectCase(1);},100);
});
</script>
</body>
</html>
"""

def render():
    st.set_page_config(page_title="이차함수의 최대·최소 탐구", layout="wide")
    st.markdown(
        """
        <style>
        .main { max-width: 100%; }
        iframe { width: 100% !important; height: 2600px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    components.html(_HTML, height=2400, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
