import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "함수의개수탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 함수의 종류별 개수를 구하는 문제를 각각 만들어보세요 (문제와 답 모두 작성)**"},
    {"key": "문제1", "label": "📌 문제 1 — 함수 또는 일대일함수의 개수", "type": "text_area", "height": 80},
    {"key": "답1",   "label": "문제 1의 답",  "type": "text_input"},
    {"key": "문제2", "label": "📌 문제 2 — 순증가 또는 순감소함수의 개수", "type": "text_area", "height": 80},
    {"key": "답2",   "label": "문제 2의 답",  "type": "text_input"},
    {"key": "문제3", "label": "📌 문제 3 — 단조증가 또는 단조감소함수의 개수", "type": "text_area", "height": 80},
    {"key": "답3",   "label": "문제 3의 답",  "type": "text_input"},
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title": "미니: 함수의 개수와 경우의 수",
    "description": "중복순열·순열·조합·중복조합으로 함수·일대일함수·순증가·단조증가 함수의 개수를 탐구합니다.",
    "order": 27,
    "hidden": True,
}


def render():
    st.header("🔢 함수의 개수 탐구")
    st.caption(
        "집합 A = {a₁, …, aₘ}, B = {b₁, …, bₙ}에서 함수 f : A → B의 종류별 개수를 "
        "중복순열·순열·조합·중복조합으로 탐구합니다."
    )
    components.html(_build_html(), height=2000, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
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
body{font-family:'Noto Sans KR',system-ui,sans-serif;background:#0e1117;color:#e2e8f0;padding:12px 10px;font-size:15px;}

/* ── 탭 ─────────────────────────────────────────── */
.tab-bar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px;}
.tab-btn{padding:9px 13px;border:1px solid #3a4060;border-radius:9px;background:#1a1f35;
  color:#9ba8c5;cursor:pointer;font-size:13px;font-weight:700;transition:all .2s;line-height:1.3;}
.tab-btn.active{background:#2c4a8c;border-color:#4c8bf5;color:#fff;}
.panel{display:none;} .panel.active{display:block;}

/* ── 카드 ────────────────────────────────────────── */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
  border-radius:16px;padding:16px 18px;margin-bottom:12px;backdrop-filter:blur(6px);}
.card-title{font-size:15px;font-weight:800;color:#fbbf24;margin-bottom:11px;
  display:flex;align-items:center;gap:7px;}

/* ── 공식 박스 ───────────────────────────────────── */
.fbox{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);
  border-radius:12px;padding:13px 18px;margin:10px 0;text-align:center;}
.fbox .big{font-size:24px;font-weight:900;color:#fbbf24;display:block;margin-bottom:4px;}
.fbox .sub{font-size:13px;color:#94a3b8;}

/* ── 슬라이더 ────────────────────────────────────── */
.ctrl{display:flex;flex-wrap:wrap;gap:18px;align-items:center;
  background:rgba(255,255,255,.03);border-radius:10px;padding:12px 14px;margin:10px 0;}
.ctrl-item{display:flex;flex-direction:column;gap:5px;}
.ctrl-item label{font-size:12px;color:#94a3b8;font-weight:700;letter-spacing:.04em;text-transform:uppercase;}
.slider-row{display:flex;align-items:center;gap:8px;}
input[type=range]{width:130px;-webkit-appearance:none;height:5px;border-radius:3px;
  background:linear-gradient(90deg,#3b82f6,#6366f1);outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;
  border-radius:50%;background:#fff;border:3px solid #6366f1;cursor:pointer;}
.badge{display:inline-block;min-width:28px;background:linear-gradient(135deg,#3b82f6,#6366f1);
  border-radius:8px;padding:2px 8px;font-weight:900;font-size:14px;text-align:center;color:#fff;}
.badge.orange{background:linear-gradient(135deg,#f59e0b,#ef4444);}
.badge.green{background:linear-gradient(135deg,#10b981,#059669);}

/* ── 단계별 곱셈기 ───────────────────────────────── */
.steps{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0;align-items:center;}
.step-box{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  border-radius:10px;padding:8px 12px;text-align:center;min-width:50px;}
.step-box .s-lbl{font-size:11px;color:#94a3b8;font-weight:600;}
.step-box .s-val{font-size:18px;font-weight:900;color:#fbbf24;margin-top:2px;}
.step-times{font-size:19px;color:#64748b;font-weight:700;}
.step-eq{font-size:19px;color:#64748b;font-weight:700;}

/* ── 결과 박스 ───────────────────────────────────── */
.result-box{background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px 18px;margin:10px 0;text-align:center;}
.result-box .r-formula{font-size:18px;font-weight:700;color:#a5b4fc;margin-bottom:4px;}
.result-box .r-value{font-size:38px;font-weight:900;color:#e2e8f0;}
.result-box .r-hint{font-size:12px;color:#64748b;margin-top:4px;}

/* ── 경고 박스 ───────────────────────────────────── */
.warn-box{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.25);
  border-radius:10px;padding:9px 14px;color:#f87171;font-size:13px;margin:8px 0;}

/* ── 키포인트 ────────────────────────────────────── */
.kp{background:rgba(251,191,36,.07);border-left:3px solid #fbbf24;
  border-radius:0 8px 8px 0;padding:8px 14px;margin:8px 0;font-size:14px;color:#e2e8f0;line-height:1.7;}

/* ── SVG 다이어그램 ──────────────────────────────── */
.diagram-wrap{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);
  border-radius:12px;padding:8px;margin:10px 0;overflow-x:auto;text-align:center;}

/* ── 버튼 ────────────────────────────────────────── */
.btn{padding:8px 16px;border:none;border-radius:8px;cursor:pointer;
  font-size:14px;font-weight:700;transition:all .2s;margin:4px 2px;}
.btn-primary{background:linear-gradient(135deg,#3b82f6,#6366f1);color:#fff;}
.btn-primary:hover{opacity:.85;transform:translateY(-1px);}
.btn-orange{background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;}
.btn-orange:hover{opacity:.85;transform:translateY(-1px);}
.btn-green{background:linear-gradient(135deg,#10b981,#059669);color:#fff;}
.btn-green:hover{opacity:.85;transform:translateY(-1px);}

p{line-height:1.75;color:#cbd5e1;margin-bottom:8px;font-size:14px;}
h3{font-size:15px;font-weight:700;color:#f8fafc;margin:12px 0 6px;}
ul,ol{padding-left:18px;}li{line-height:1.8;color:#cbd5e1;font-size:14px;}

/* ── 요약 표 ─────────────────────────────────────── */
.sum-table{width:100%;border-collapse:collapse;font-size:14px;margin-top:8px;}
.sum-table th{background:rgba(245,158,11,.2);color:#fbbf24;padding:9px 10px;
  font-weight:700;border:1px solid rgba(255,255,255,.08);text-align:center;}
.sum-table td{padding:8px 10px;border:1px solid rgba(255,255,255,.06);
  color:#e2e8f0;text-align:center;}
.sum-table tr:nth-child(even) td{background:rgba(255,255,255,.03);}
.sum-table .hl{color:#fbbf24;font-weight:700;}

/* ── 퀴즈 ────────────────────────────────────────── */
.quiz-q{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:14px 16px;margin-bottom:10px;}
.quiz-q .q-badge{display:inline-block;background:rgba(99,102,241,.3);color:#a5b4fc;
  border-radius:6px;padding:2px 8px;font-size:12px;font-weight:800;margin-bottom:8px;}
.quiz-q .q-text{font-size:15px;font-weight:600;color:#e2e8f0;margin-bottom:10px;line-height:1.6;}
.quiz-input{width:110px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.2);
  border-radius:8px;color:#e2e8f0;font-size:17px;font-weight:700;padding:6px 10px;text-align:center;}
.quiz-input:focus{outline:none;border-color:#6366f1;}
.quiz-hint{font-size:12px;color:#64748b;margin-left:8px;}
.q-row{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:4px;}
.q-feedback{font-size:14px;font-weight:700;padding:5px 12px;border-radius:7px;display:none;}
.q-feedback.correct{background:rgba(74,222,128,.1);color:#4ade80;border:1px solid rgba(74,222,128,.3);display:block;}
.q-feedback.wrong{background:rgba(239,68,68,.1);color:#f87171;border:1px solid rgba(239,68,68,.3);display:block;}

.score-box{background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.3);
  border-radius:14px;padding:18px;text-align:center;margin-top:14px;display:none;}
.score-box .sc{font-size:44px;font-weight:900;color:#fbbf24;}
.score-box .sc-msg{font-size:15px;color:#e2e8f0;margin-top:6px;}

.type-badge{display:inline-block;border-radius:6px;padding:2px 8px;font-size:11px;font-weight:800;margin-left:6px;}
.tb-rp{background:rgba(239,68,68,.2);color:#fca5a5;}
.tb-p{background:rgba(59,130,246,.2);color:#93c5fd;}
.tb-c{background:rgba(16,185,129,.2);color:#6ee7b7;}
.tb-h{background:rgba(168,85,247,.2);color:#d8b4fe;}

/* ── 모든 경우의 수 목록 ─────────────────────────────────────────────── */
.am-wrap{margin-top:14px;}
.am-title{font-size:13px;font-weight:700;color:#94a3b8;margin-bottom:7px;letter-spacing:.01em;}
.am-grid{display:flex;flex-wrap:wrap;gap:4px;max-height:210px;overflow-y:auto;
  padding:9px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.07);border-radius:10px;}
.am-grid::-webkit-scrollbar{width:4px;}.am-grid::-webkit-scrollbar-track{background:transparent;}
.am-grid::-webkit-scrollbar-thumb{background:rgba(255,255,255,.15);border-radius:2px;}
.am-item{font-size:12px;color:#475569;padding:3px 7px;border-radius:6px;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.05);
  font-family:'Courier New',monospace;white-space:nowrap;line-height:1.4;transition:background .1s;}
.am-cur{color:#fbbf24 !important;font-weight:900 !important;
  background:rgba(251,191,36,.15) !important;border-color:rgba(251,191,36,.5) !important;
  font-size:13px !important;box-shadow:0 0 7px rgba(251,191,36,.3);}
.am-toomany{font-size:12px;color:#475569;margin-top:7px;padding:5px 8px;
  background:rgba(255,255,255,.02);border-radius:6px;}
</style>
</head>
<body>

<!-- ══ 탭 바 ══════════════════════════════════════════════════════════════ -->
<div class="tab-bar">
  <button class="tab-btn active" onclick="switchTab('t1',this)">① 함수<br><small>$_n\Pi_m = n^m$</small></button>
  <button class="tab-btn" onclick="switchTab('t2',this)">② 일대일함수<br><small>$_nP_m$</small></button>
  <button class="tab-btn" onclick="switchTab('t3',this)">③ 순증가/감소<br><small>$_nC_m$</small></button>
  <button class="tab-btn" onclick="switchTab('t4',this)">④ 단조증가/감소<br><small>$_nH_m$</small></button>
  <button class="tab-btn" onclick="switchTab('t5',this)">✅ 요약 &amp; 확인문제</button>
</div>

<!-- ══ 패널 1: 함수 (중복순열) ════════════════════════════════════════════ -->
<div id="t1" class="panel active">

  <div class="card">
    <div class="card-title">📌 함수란?</div>
    <p>함수 $f: A \to B$는 A의 <strong>각 원소</strong>를 B의 원소 <strong>정확히 하나</strong>에 대응시키는 규칙입니다.
    B의 같은 원소에 여러 번 대응해도 괜찮습니다.</p>
    <div class="fbox">
      <span class="big">$a_i \;\to\; B$의 $n$가지 중 1개 선택</span>
      <span class="sub">$m$개의 원소가 각각 독립적으로 n가지 중 선택 → 곱의 법칙</span>
    </div>
    <p><strong>함수의 개수</strong> $= \underbrace{n \times n \times \cdots \times n}_{m\text{개}} = n^m = {}_n\Pi_m$</p>
    <div class="kp">💡 B의 원소를 <strong>중복해서 선택</strong>할 수 있으므로 → <strong>중복순열</strong>!</div>
  </div>

  <div class="card">
    <div class="card-title">🎛️ 인터랙티브 탐구</div>
    <div class="ctrl">
      <div class="ctrl-item">
        <label>m = |A|</label>
        <div class="slider-row">
          <input type="range" id="m1" min="1" max="5" value="3" oninput="update1()">
          <span class="badge orange" id="mv1">3</span>
        </div>
      </div>
      <div class="ctrl-item">
        <label>n = |B|</label>
        <div class="slider-row">
          <input type="range" id="n1" min="1" max="6" value="4" oninput="update1()">
          <span class="badge" id="nv1">4</span>
        </div>
      </div>
    </div>
    <h3>단계별 선택 횟수</h3>
    <div id="steps1" class="steps"></div>
    <div id="result1" class="result-box"></div>
    <div class="diagram-wrap">
      <svg id="svg1" style="max-width:100%;"></svg>
    </div>
    <button class="btn btn-orange" onclick="newExample1()">🎲 새 예시 보기</button>
    <div class="am-wrap" id="allMaps1"></div>
  </div>

</div>

<!-- ══ 패널 2: 일대일함수 (순열) ══════════════════════════════════════════ -->
<div id="t2" class="panel">

  <div class="card">
    <div class="card-title">📌 일대일함수(단사함수)란?</div>
    <p>일대일함수는 A의 <strong>서로 다른 원소</strong>를 B의 <strong>서로 다른 원소</strong>에 대응시킵니다.
    즉, B의 원소를 중복 사용 불가!</p>
    <div class="fbox">
      <span class="big">$a_1 \to n$가지, $\; a_2 \to (n-1)$가지, $\; \cdots$</span>
      <span class="sub">앞에서 고른 것을 제외하고 선택 → 순열</span>
    </div>
    <p><strong>일대일함수의 개수</strong> $= n(n-1)(n-2)\cdots(n-m+1) = {}_nP_m$</p>
    <div class="kp">⚠️ 일대일함수가 존재하려면 반드시 $m \le n$ 이어야 합니다.</div>
  </div>

  <div class="card">
    <div class="card-title">🎛️ 인터랙티브 탐구</div>
    <div class="ctrl">
      <div class="ctrl-item">
        <label>m = |A|</label>
        <div class="slider-row">
          <input type="range" id="m2" min="1" max="5" value="3" oninput="update2()">
          <span class="badge orange" id="mv2">3</span>
        </div>
      </div>
      <div class="ctrl-item">
        <label>n = |B|</label>
        <div class="slider-row">
          <input type="range" id="n2" min="1" max="6" value="4" oninput="update2()">
          <span class="badge" id="nv2">4</span>
        </div>
      </div>
    </div>
    <div id="warn2" class="warn-box" style="display:none;">⚠️ m &gt; n 이면 일대일함수가 존재하지 않습니다! (개수 = 0)</div>
    <h3>단계별 선택 횟수</h3>
    <div id="steps2" class="steps"></div>
    <div id="result2" class="result-box"></div>
    <div class="diagram-wrap">
      <svg id="svg2" style="max-width:100%;"></svg>
    </div>
    <button class="btn btn-orange" onclick="newExample2()">🎲 새 예시 보기</button>
    <div class="am-wrap" id="allMaps2"></div>
  </div>

</div>

<!-- ══ 패널 3: 순증가/순감소함수 (조합) ══════════════════════════════════ -->
<div id="t3" class="panel">

  <div class="card">
    <div class="card-title">📌 순증가함수 / 순감소함수란?</div>
    <p><strong>순증가함수</strong>: $x &lt; y \Rightarrow f(x) &lt; f(y)$ &nbsp;|&nbsp;
       <strong>순감소함수</strong>: $x &lt; y \Rightarrow f(x) &gt; f(y)$</p>
    <p>B에서 서로 다른 m개의 값을 고르면, 그 순서가 딱 하나로 결정됩니다!</p>
    <div class="fbox">
      <span class="big">B의 $n$개 중 $m$개 선택 (중복 없이) → 조합</span>
      <span class="sub">고른 m개를 작은 순서대로 배열하면 → 순증가함수 1개, 큰 순서대로 → 순감소함수 1개</span>
    </div>
    <p>순증가함수의 개수 $= {}_nC_m$ &nbsp;&nbsp; 순감소함수의 개수 $= {}_nC_m$</p>
    <div class="kp">💡 B에서 m개를 중복 없이 선택하면 순서가 유일하게 결정됨 → <strong>조합</strong>!</div>
  </div>

  <div class="card">
    <div class="card-title">🎛️ 인터랙티브 탐구</div>
    <div class="ctrl">
      <div class="ctrl-item">
        <label>m = |A|</label>
        <div class="slider-row">
          <input type="range" id="m3" min="1" max="5" value="3" oninput="update3()">
          <span class="badge orange" id="mv3">3</span>
        </div>
      </div>
      <div class="ctrl-item">
        <label>n = |B|</label>
        <div class="slider-row">
          <input type="range" id="n3" min="1" max="6" value="5" oninput="update3()">
          <span class="badge" id="nv3">5</span>
        </div>
      </div>
    </div>
    <div id="warn3" class="warn-box" style="display:none;">⚠️ m &gt; n 이면 순증가/감소함수가 존재하지 않습니다! (개수 = 0)</div>
    <div id="result3" class="result-box"></div>
    <div class="diagram-wrap">
      <svg id="svg3" style="max-width:100%;"></svg>
    </div>
    <button class="btn btn-orange" onclick="newExample3()">🎲 새 예시 보기</button>
    <div class="am-wrap" id="allMaps3"></div>
    <h3>왜 조합인가요?</h3>
    <div id="why3" style="margin-top:6px;"></div>
  </div>

</div>

<!-- ══ 패널 4: 단조증가/단조감소함수 (중복조합) ══════════════════════════ -->
<div id="t4" class="panel">

  <div class="card">
    <div class="card-title">📌 단조증가함수 / 단조감소함수란?</div>
    <p><strong>단조증가함수</strong>: $x &lt; y \Rightarrow f(x) \le f(y)$ &nbsp;|&nbsp;
       <strong>단조감소함수</strong>: $x &lt; y \Rightarrow f(x) \ge f(y)$</p>
    <p>순증가와 달리 <strong>같은 값에 여러 번 대응될 수 있습니다</strong> (중복 허용).</p>
    <div class="fbox">
      <span class="big">B의 $n$개 중 $m$개 선택 (중복 허용) → 중복조합</span>
      <span class="sub">고른 m개를 작은 순서대로 배열하면 → 단조증가함수 1개</span>
    </div>
    <p>단조증가함수의 개수 $= {}_nH_m = {}_{n+m-1}C_m$ &nbsp;&nbsp; 단조감소함수의 개수 $= {}_nH_m$</p>
    <div class="kp">💡 B에서 m개를 <strong>중복 허용</strong>해서 선택하면 순서가 유일하게 결정됨 → <strong>중복조합</strong>!</div>
  </div>

  <div class="card">
    <div class="card-title">🎛️ 인터랙티브 탐구</div>
    <div class="ctrl">
      <div class="ctrl-item">
        <label>m = |A|</label>
        <div class="slider-row">
          <input type="range" id="m4" min="1" max="5" value="3" oninput="update4()">
          <span class="badge orange" id="mv4">3</span>
        </div>
      </div>
      <div class="ctrl-item">
        <label>n = |B|</label>
        <div class="slider-row">
          <input type="range" id="n4" min="1" max="6" value="4" oninput="update4()">
          <span class="badge" id="nv4">4</span>
        </div>
      </div>
    </div>
    <div id="result4" class="result-box"></div>
    <div class="diagram-wrap">
      <svg id="svg4" style="max-width:100%;"></svg>
    </div>
    <button class="btn btn-orange" onclick="newExample4()">🎲 새 예시 보기</button>
    <div class="am-wrap" id="allMaps4"></div>
    <h3>순증가 vs 단조증가 비교</h3>
    <div id="compare4" style="margin-top:6px;"></div>
  </div>

</div>

<!-- ══ 패널 5: 요약 & 확인문제 ════════════════════════════════════════════ -->
<div id="t5" class="panel">

  <div class="card">
    <div class="card-title">📊 4가지 함수의 개수 요약</div>
    <div class="ctrl">
      <div class="ctrl-item">
        <label>m = |A|</label>
        <div class="slider-row">
          <input type="range" id="ms" min="1" max="5" value="3" oninput="updateSummary()">
          <span class="badge orange" id="mvs">3</span>
        </div>
      </div>
      <div class="ctrl-item">
        <label>n = |B|</label>
        <div class="slider-row">
          <input type="range" id="ns" min="1" max="6" value="5" oninput="updateSummary()">
          <span class="badge" id="nvs">5</span>
        </div>
      </div>
    </div>
    <div style="overflow-x:auto;">
      <table class="sum-table" id="sumTable">
        <thead>
          <tr>
            <th>함수 종류</th><th>조건</th><th>사용 공식</th><th>개수</th>
          </tr>
        </thead>
        <tbody id="sumBody"></tbody>
      </table>
    </div>
  </div>

  <div class="card">
    <div class="card-title">✅ 확인 문제</div>
    <p style="margin-bottom:12px;color:#94a3b8;">각 문제의 답을 입력하고 <strong>확인</strong> 버튼을 누르세요.</p>

    <!-- Q1 -->
    <div class="quiz-q" id="qq1">
      <div class="q-badge">Q1 <span class="type-badge tb-rp">중복순열</span></div>
      <div class="q-text">$A=\{1,2,3\},\; B=\{1,2,3,4\}$ 일 때, 함수 $f:A \to B$ 의 개수는?</div>
      <div class="q-row">
        <input class="quiz-input" id="qi1" type="number" placeholder="답 입력">
        <button class="btn btn-primary" onclick="checkQ(1,64)">확인</button>
        <span class="quiz-hint">힌트: $n^m$</span>
      </div>
      <div class="q-feedback" id="qf1"></div>
    </div>

    <!-- Q2 -->
    <div class="quiz-q" id="qq2">
      <div class="q-badge">Q2 <span class="type-badge tb-p">순열</span></div>
      <div class="q-text">$A=\{1,2,3\},\; B=\{1,2,3,4\}$ 일 때, 일대일함수 $f:A \to B$ 의 개수는?</div>
      <div class="q-row">
        <input class="quiz-input" id="qi2" type="number" placeholder="답 입력">
        <button class="btn btn-primary" onclick="checkQ(2,24)">확인</button>
        <span class="quiz-hint">힌트: $_4P_3$</span>
      </div>
      <div class="q-feedback" id="qf2"></div>
    </div>

    <!-- Q3 -->
    <div class="quiz-q" id="qq3">
      <div class="q-badge">Q3 <span class="type-badge tb-c">조합</span></div>
      <div class="q-text">$A=\{1,2,3\},\; B=\{1,2,3,4,5\}$ 일 때, 순증가함수 $f:A \to B$ 의 개수는?</div>
      <div class="q-row">
        <input class="quiz-input" id="qi3" type="number" placeholder="답 입력">
        <button class="btn btn-primary" onclick="checkQ(3,10)">확인</button>
        <span class="quiz-hint">힌트: $_5C_3$</span>
      </div>
      <div class="q-feedback" id="qf3"></div>
    </div>

    <!-- Q4 -->
    <div class="quiz-q" id="qq4">
      <div class="q-badge">Q4 <span class="type-badge tb-h">중복조합</span></div>
      <div class="q-text">$A=\{1,2,3\},\; B=\{1,2,3,4\}$ 일 때, 단조증가함수 $f:A \to B$ 의 개수는?</div>
      <div class="q-row">
        <input class="quiz-input" id="qi4" type="number" placeholder="답 입력">
        <button class="btn btn-primary" onclick="checkQ(4,20)">확인</button>
        <span class="quiz-hint">힌트: $_4H_3 = {}_6C_3$</span>
      </div>
      <div class="q-feedback" id="qf4"></div>
    </div>

    <!-- Q5 -->
    <div class="quiz-q" id="qq5">
      <div class="q-badge">Q5 <span class="type-badge tb-c">조합</span></div>
      <div class="q-text">$A=\{1,2,3,4\},\; B=\{1,2,3,4,5,6\}$ 일 때, 순감소함수 $f:A \to B$ 의 개수는?</div>
      <div class="q-row">
        <input class="quiz-input" id="qi5" type="number" placeholder="답 입력">
        <button class="btn btn-primary" onclick="checkQ(5,15)">확인</button>
        <span class="quiz-hint">힌트: $_6C_4$</span>
      </div>
      <div class="q-feedback" id="qf5"></div>
    </div>

    <!-- Q6 -->
    <div class="quiz-q" id="qq6">
      <div class="q-badge">Q6 <span class="type-badge tb-h">중복조합</span></div>
      <div class="q-text">$A=\{1,2,3,4\},\; B=\{1,2,3,4,5\}$ 일 때, 단조감소함수 $f:A \to B$ 의 개수는?</div>
      <div class="q-row">
        <input class="quiz-input" id="qi6" type="number" placeholder="답 입력">
        <button class="btn btn-primary" onclick="checkQ(6,70)">확인</button>
        <span class="quiz-hint">힌트: $_5H_4 = {}_8C_4$</span>
      </div>
      <div class="q-feedback" id="qf6"></div>
    </div>

    <!-- Q7: 응용 문제 -->
    <div class="quiz-q" id="qq7">
      <div class="q-badge">Q7 ⭐ 심화 <span class="type-badge tb-rp">중복순열</span><span class="type-badge tb-p">순열</span></div>
      <div class="q-text">$A=\{1,2,3\},\; B=\{1,2,3,4,5\}$ 일 때, <br>
        함수 $f:A \to B$ 의 개수에서 일대일함수의 개수를 뺀 값은?
        <br><small style="color:#94a3b8;">(일대일이 아닌 함수의 개수)</small>
      </div>
      <div class="q-row">
        <input class="quiz-input" id="qi7" type="number" placeholder="답 입력">
        <button class="btn btn-primary" onclick="checkQ(7,65)">확인</button>
        <span class="quiz-hint">힌트: $5^3 - {}_5P_3$</span>
      </div>
      <div class="q-feedback" id="qf7"></div>
    </div>

    <div style="text-align:center;margin-top:14px;">
      <button class="btn btn-green" onclick="checkAll()">📊 전체 채점</button>
    </div>
    <div class="score-box" id="scoreBox">
      <div class="sc" id="scoreText"></div>
      <div class="sc-msg" id="scoreMsg"></div>
    </div>
  </div>

</div>

<!-- ══ 스크립트 ═══════════════════════════════════════════════════════════ -->
<script>
// ── 탭 전환 ──────────────────────────────────────────────────────────────
function switchTab(id, btn) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
  setTimeout(() => {
    if (typeof renderMathInElement !== 'undefined') {
      renderMathInElement(document.getElementById(id), {
        delimiters: [{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]
      });
    }
  }, 50);
}

// ── 수학 헬퍼 ─────────────────────────────────────────────────────────────
function fact(n) {
  if (n <= 1) return 1;
  let r = 1; for (let i = 2; i <= n; i++) r *= i; return r;
}
function perm(n, r) { if (r > n || r < 0 || n < 0) return 0; return fact(n)/fact(n-r); }
function comb(n, r) {
  if (r > n || r < 0 || n < 0) return 0;
  return fact(n)/(fact(r)*fact(n-r));
}
function repPerm(n, m) { return Math.pow(n, m); }
function repComb(n, m) { return comb(n+m-1, m); }

// ── SVG 다이어그램 ────────────────────────────────────────────────────────
const COLORS = ['#60a5fa','#34d399','#f472b6','#a78bfa','#fb923c'];

function arrowSVG(x1, y1, x2, y2, color, r) {
  r = r || 20;
  const dx = x2-x1, dy = y2-y1;
  const len = Math.sqrt(dx*dx+dy*dy);
  if (len < 1) return `<circle cx="${x1}" cy="${y1}" r="5" fill="${color}" opacity=".7"/>`;
  const ux = dx/len, uy = dy/len;
  const sx = x1+ux*r, sy = y1+uy*r;
  const ex = x2-ux*r, ey = y2-uy*r;
  const ax = ex-ux*9, ay = ey-uy*9;
  const px = -uy, py = ux;
  const p1x = ax+px*5, p1y = ay+py*5;
  const p2x = ax-px*5, p2y = ay-py*5;
  return `<line x1="${sx}" y1="${sy}" x2="${ax}" y2="${ay}" stroke="${color}" stroke-width="2" stroke-linecap="round" opacity=".85"/>
          <polygon points="${ex},${ey} ${p1x},${p1y} ${p2x},${p2y}" fill="${color}" opacity=".85"/>`;
}

function drawDiagram(svgId, m, n, mapping) {
  const svg = document.getElementById(svgId);
  if (!svg) return;
  const STEP = 46, PAD = 34, AX = 65, BX = 265;
  const H = Math.max(m, n) * STEP + PAD * 2;
  const W = 330;
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.setAttribute('width', W);
  svg.setAttribute('height', H);

  // A 노드 y 좌표 (STEP/2 추가로 타원 중앙 정렬)
  const ay = i => PAD + i * STEP + (Math.max(n, m) - m) * STEP / 2 + STEP / 2;
  const by = j => PAD + j * STEP + (Math.max(n, m) - n) * STEP / 2 + STEP / 2;

  let html = '';
  // 타원 배경 힌트
  html += `<ellipse cx="${AX}" cy="${H/2}" rx="38" ry="${m*STEP/2+14}" fill="rgba(99,102,241,.08)" stroke="rgba(99,102,241,.25)" stroke-width="1.5"/>`;
  html += `<ellipse cx="${BX}" cy="${H/2}" rx="38" ry="${n*STEP/2+14}" fill="rgba(245,158,11,.08)" stroke="rgba(245,158,11,.25)" stroke-width="1.5"/>`;
  // 라벨
  html += `<text x="${AX}" y="14" text-anchor="middle" font-size="14" font-weight="800" fill="#a5b4fc">A</text>`;
  html += `<text x="${BX}" y="14" text-anchor="middle" font-size="14" font-weight="800" fill="#fbbf24">B</text>`;
  // 화살표
  if (mapping) {
    for (let i = 0; i < m; i++) {
      html += arrowSVG(AX, ay(i), BX, by(mapping[i]), COLORS[i % COLORS.length], 20);
    }
  }
  // A 노드
  for (let i = 0; i < m; i++) {
    const yy = ay(i);
    html += `<circle cx="${AX}" cy="${yy}" r="19" fill="rgba(99,102,241,.25)" stroke="#6366f1" stroke-width="1.5"/>`;
    html += `<text x="${AX}" y="${yy+5}" text-anchor="middle" font-size="13" font-weight="700" fill="#a5b4fc">a${i+1}</text>`;
  }
  // B 노드
  for (let j = 0; j < n; j++) {
    const yy = by(j);
    html += `<circle cx="${BX}" cy="${yy}" r="19" fill="rgba(245,158,11,.18)" stroke="#fbbf24" stroke-width="1.5"/>`;
    html += `<text x="${BX}" y="${yy+5}" text-anchor="middle" font-size="13" font-weight="700" fill="#fbbf24">b${j+1}</text>`;
  }
  svg.innerHTML = html;
}

// ── 랜덤 매핑 생성자 ─────────────────────────────────────────────────────
function randomFunc(m, n) {
  return Array.from({length:m}, () => Math.floor(Math.random()*n));
}
function randomInj(m, n) {
  if (m > n) return null;
  const arr = Array.from({length:n}, (_,i) => i);
  for (let i = 0; i < m; i++) {
    const j = Math.floor(Math.random()*(n-i))+i;
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.slice(0, m);
}
function randomStrict(m, n) {
  if (m > n) return null;
  const arr = Array.from({length:n}, (_,i) => i);
  for (let i = arr.length-1; i > 0; i--) {
    const j = Math.floor(Math.random()*(i+1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.slice(0, m).sort((a,b)=>a-b);
}
function randomMono(m, n) {
  const arr = Array.from({length:m}, () => Math.floor(Math.random()*n));
  return arr.sort((a,b)=>a-b);
}

// ── 모든 경우 열거 & 렌더 ──────────────────────────────────────────────
const GEN_LIMIT = 500;

function genAllFuncs(m, n) {
  const res = [];
  function go(cur) {
    if (cur.length === m) { res.push(cur.slice()); return; }
    for (let j = 0; j < n; j++) { cur.push(j); go(cur); cur.pop(); }
  }
  go([]); return res;
}
function genAllInj(m, n) {
  if (m > n) return [];
  const res = [], used = new Array(n).fill(false);
  function go(cur) {
    if (cur.length === m) { res.push(cur.slice()); return; }
    for (let j = 0; j < n; j++) {
      if (!used[j]) { used[j]=true; cur.push(j); go(cur); cur.pop(); used[j]=false; }
    }
  }
  go([]); return res;
}
function genAllStrict(m, n) {
  if (m > n) return [];
  const res = [];
  function go(cur, s) {
    if (cur.length === m) { res.push(cur.slice()); return; }
    for (let j = s; j < n; j++) { cur.push(j); go(cur, j+1); cur.pop(); }
  }
  go([], 0); return res;
}
function genAllMono(m, n) {
  const res = [];
  function go(cur, s) {
    if (cur.length === m) { res.push(cur.slice()); return; }
    for (let j = s; j < n; j++) { cur.push(j); go(cur, j); cur.pop(); }
  }
  go([], 0); return res;
}
function mapsEq(a, b) {
  return a && b && a.length === b.length && a.every((v,i) => v===b[i]);
}
function renderAllMaps(cid, total, genFn, cur) {
  const el = document.getElementById(cid);
  if (!el) return;
  if (!total) { el.innerHTML = ''; return; }
  let html = `<div class="am-title">📋 가능한 모든 경우 — 총 <strong style="color:#e2e8f0">${total}가지</strong></div>`;
  if (total > GEN_LIMIT) {
    html += `<div class="am-toomany">경우의 수가 너무 많아 (${total}가지) 목록을 생략합니다.</div>`;
    el.innerHTML = html; return;
  }
  const all = genFn();
  html += '<div class="am-grid">';
  for (const mp of all) {
    const str = '(' + mp.map(v => 'b'+(v+1)).join(', ') + ')';
    html += `<span class="am-item${mapsEq(mp, cur) ? ' am-cur' : ''}">${str}</span>`;
  }
  html += '</div>';
  el.innerHTML = html;
  // 현재 예시를 스크롤해서 보이게
  const curEl = el.querySelector('.am-cur');
  if (curEl) {
    const grid = el.querySelector('.am-grid');
    if (grid) setTimeout(() => { grid.scrollTop = Math.max(0, curEl.offsetTop - grid.offsetTop - grid.clientHeight/2 + curEl.clientHeight/2); }, 30);
  }
}

// ── 단계 박스 HTML ───────────────────────────────────────────────────────
function stepsHTML(labels, sep) {
  let h = '<div class="steps">';
  for (let i = 0; i < labels.length; i++) {
    if (i > 0) h += `<span class="step-times">${sep || '×'}</span>`;
    h += `<div class="step-box"><div class="s-lbl">${labels[i].lbl}</div><div class="s-val">${labels[i].val}</div></div>`;
  }
  h += '</div>';
  return h;
}

// ════════════════════════════════════════════════════════════════════════
// 패널 1: 함수
// ════════════════════════════════════════════════════════════════════════
let map1 = null;
function update1() {
  const m = +document.getElementById('m1').value;
  const n = +document.getElementById('n1').value;
  document.getElementById('mv1').textContent = m;
  document.getElementById('nv1').textContent = n;
  const cnt = repPerm(n, m);
  const labs = Array.from({length:m}, (_,i)=>({lbl:`a${i+1}`, val:n}));
  document.getElementById('steps1').innerHTML = stepsHTML(labs);
  document.getElementById('result1').innerHTML =
    `<div class="r-formula">$_${n}\\Pi_${m} = ${n}^{${m}}$</div>
     <div class="r-value">${cnt}</div>
     <div class="r-hint">함수 f:A→B의 개수</div>`;
  if (!map1 || map1.length !== m) map1 = randomFunc(m, n);
  map1 = map1.map(v => Math.min(v, n-1));
  drawDiagram('svg1', m, n, map1);
  if (typeof renderMathInElement !== 'undefined') {
    renderMathInElement(document.getElementById('result1'), {
      delimiters:[{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}]
    });
  }
  renderAllMaps('allMaps1', repPerm(n, m), () => genAllFuncs(m, n), map1);
}
function newExample1() {
  const m = +document.getElementById('m1').value;
  const n = +document.getElementById('n1').value;
  map1 = randomFunc(m, n);
  drawDiagram('svg1', m, n, map1);
  renderAllMaps('allMaps1', repPerm(n, m), () => genAllFuncs(m, n), map1);
}

// ════════════════════════════════════════════════════════════════════════
// 패널 2: 일대일함수
// ════════════════════════════════════════════════════════════════════════
let map2 = null;
function update2() {
  const m = +document.getElementById('m2').value;
  const n = +document.getElementById('n2').value;
  document.getElementById('mv2').textContent = m;
  document.getElementById('nv2').textContent = n;
  const warn = document.getElementById('warn2');
  if (m > n) {
    warn.style.display = 'block';
    document.getElementById('steps2').innerHTML = '';
    document.getElementById('result2').innerHTML =
      `<div class="r-formula">$_${n}P_${m}$</div><div class="r-value">0</div><div class="r-hint">m &gt; n 이므로 존재하지 않음</div>`;
    drawDiagram('svg2', m, n, null);
    renderAllMaps('allMaps2', 0, null, null);
    return;
  }
  warn.style.display = 'none';
  const cnt = perm(n, m);
  const labs = Array.from({length:m}, (_,i)=>({lbl:`a${i+1}`, val:n-i}));
  document.getElementById('steps2').innerHTML = stepsHTML(labs);
  document.getElementById('result2').innerHTML =
    `<div class="r-formula">$_${n}P_${m} = ${n}\\times${n-1}\\times\\cdots\\times${n-m+1}$</div>
     <div class="r-value">${cnt}</div>
     <div class="r-hint">일대일함수 f:A→B의 개수</div>`;
  map2 = randomInj(m, n);
  drawDiagram('svg2', m, n, map2);
  if (typeof renderMathInElement !== 'undefined') {
    renderMathInElement(document.getElementById('result2'), {
      delimiters:[{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}]
    });
  }
  renderAllMaps('allMaps2', perm(n, m), () => genAllInj(m, n), map2);
}
function newExample2() {
  const m = +document.getElementById('m2').value;
  const n = +document.getElementById('n2').value;
  if (m > n) return;
  map2 = randomInj(m, n);
  drawDiagram('svg2', m, n, map2);
  renderAllMaps('allMaps2', perm(n, m), () => genAllInj(m, n), map2);
}

// ════════════════════════════════════════════════════════════════════════
// 패널 3: 순증가/순감소함수
// ════════════════════════════════════════════════════════════════════════
let map3 = null;
function update3() {
  const m = +document.getElementById('m3').value;
  const n = +document.getElementById('n3').value;
  document.getElementById('mv3').textContent = m;
  document.getElementById('nv3').textContent = n;
  const warn = document.getElementById('warn3');
  if (m > n) {
    warn.style.display = 'block';
    document.getElementById('result3').innerHTML =
      `<div class="r-formula">$_${n}C_${m}$</div><div class="r-value">0</div><div class="r-hint">m &gt; n 이므로 존재하지 않음</div>`;
    drawDiagram('svg3', m, n, null);
    document.getElementById('why3').innerHTML = '';
    renderAllMaps('allMaps3', 0, null, null);
    return;
  }
  warn.style.display = 'none';
  const cnt = comb(n, m);
  document.getElementById('result3').innerHTML =
    `<div class="r-formula">순증가: $_${n}C_${m}$ &nbsp;&nbsp; 순감소: $_${n}C_${m}$</div>
     <div class="r-value">${cnt}</div>
     <div class="r-hint">각 방향별 개수 (순증가 / 순감소 각각)</div>`;
  map3 = randomStrict(m, n);
  drawDiagram('svg3', m, n, map3);
  // 왜 조합?
  const sel = map3 ? map3.map(v => `b${v+1}`).join(', ') : '';
  document.getElementById('why3').innerHTML = sel ?
    `<div class="kp">예시에서 B의 원소 <strong>{${sel}}</strong> 을 선택했습니다.<br>
    이 ${m}개를 오름차순으로 배열 → 순증가함수 1개 확정!<br>
    B의 ${n}개 중 ${m}개를 선택하는 방법 = $_${n}C_${m}$ = <strong>${cnt}가지</strong></div>` : '';
  if (typeof renderMathInElement !== 'undefined') {
    renderMathInElement(document.getElementById('result3'), {
      delimiters:[{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}]
    });
    renderMathInElement(document.getElementById('why3'), {
      delimiters:[{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}]
    });
  }
  renderAllMaps('allMaps3', cnt, () => genAllStrict(m, n), map3);
}
function newExample3() {
  const m = +document.getElementById('m3').value;
  const n = +document.getElementById('n3').value;
  if (m > n) return;
  map3 = randomStrict(m, n);
  drawDiagram('svg3', m, n, map3);
  const sel = map3.map(v => `b${v+1}`).join(', ');
  const cnt = comb(n, m);
  document.getElementById('why3').innerHTML =
    `<div class="kp">예시에서 B의 원소 <strong>{${sel}}</strong> 을 선택했습니다.<br>
    이 ${m}개를 오름차순으로 배열 → 순증가함수 1개 확정!<br>
    B의 ${n}개 중 ${m}개를 선택하는 방법 = $_{${n}}C_{${m}}$ = <strong>${cnt}가지</strong></div>`;
  if (typeof renderMathInElement !== 'undefined') {
    renderMathInElement(document.getElementById('why3'), {
      delimiters:[{left:'$',right:'$',display:false}]
    });
  }
  renderAllMaps('allMaps3', cnt, () => genAllStrict(m, n), map3);
}

// ════════════════════════════════════════════════════════════════════════
// 패널 4: 단조증가/단조감소함수
// ════════════════════════════════════════════════════════════════════════
let map4 = null;
function update4() {
  const m = +document.getElementById('m4').value;
  const n = +document.getElementById('n4').value;
  document.getElementById('mv4').textContent = m;
  document.getElementById('nv4').textContent = n;
  const cnt = repComb(n, m);
  const strictCnt = (m <= n) ? comb(n, m) : 0;
  document.getElementById('result4').innerHTML =
    `<div class="r-formula">$_${n}H_${m} = {}_{${n+m-1}}C_${m}$</div>
     <div class="r-value">${cnt}</div>
     <div class="r-hint">단조증가함수 f:A→B의 개수</div>`;
  map4 = randomMono(m, n);
  drawDiagram('svg4', m, n, map4);
  renderAllMaps('allMaps4', cnt, () => genAllMono(m, n), map4);
  document.getElementById('compare4').innerHTML =
    `<table class="sum-table" style="max-width:380px;">
      <tr><th>종류</th><th>공식</th><th>개수</th></tr>
      <tr><td>순증가함수</td><td>$_${n}C_${m}$</td><td class="hl">${strictCnt}</td></tr>
      <tr><td>단조증가함수</td><td>$_${n}H_${m}$</td><td class="hl">${cnt}</td></tr>
      <tr><td style="color:#94a3b8;font-size:12px;">단조 ≥ 순증가</td><td colspan="2" style="color:#94a3b8;font-size:12px;">같은 값 대응 허용 여부 차이</td></tr>
    </table>`;
  if (typeof renderMathInElement !== 'undefined') {
    renderMathInElement(document.getElementById('result4'), {
      delimiters:[{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}]
    });
    renderMathInElement(document.getElementById('compare4'), {
      delimiters:[{left:'$',right:'$',display:false}]
    });
  }
}
function newExample4() {
  const m = +document.getElementById('m4').value;
  const n = +document.getElementById('n4').value;
  map4 = randomMono(m, n);
  drawDiagram('svg4', m, n, map4);
  renderAllMaps('allMaps4', repComb(n, m), () => genAllMono(m, n), map4);
}

// ════════════════════════════════════════════════════════════════════════
// 패널 5: 요약 표
// ════════════════════════════════════════════════════════════════════════
function updateSummary() {
  const m = +document.getElementById('ms').value;
  const n = +document.getElementById('ns').value;
  document.getElementById('mvs').textContent = m;
  document.getElementById('nvs').textContent = n;

  const rows = [
    {
      name: '함수',
      cond: '제약 없음',
      formula: `$_${n}\\Pi_${m} = ${n}^{${m}}$`,
      cnt: repPerm(n, m)
    },
    {
      name: '일대일함수',
      cond: '$m \\le n$ 필요',
      formula: `$_${n}P_${m}$`,
      cnt: m <= n ? perm(n, m) : 0
    },
    {
      name: '순증가함수',
      cond: '$m \\le n$ 필요',
      formula: `$_${n}C_${m}$`,
      cnt: m <= n ? comb(n, m) : 0
    },
    {
      name: '순감소함수',
      cond: '$m \\le n$ 필요',
      formula: `$_${n}C_${m}$`,
      cnt: m <= n ? comb(n, m) : 0
    },
    {
      name: '단조증가함수',
      cond: '제약 없음',
      formula: `$_${n}H_${m} = {}_{${n+m-1}}C_${m}$`,
      cnt: repComb(n, m)
    },
    {
      name: '단조감소함수',
      cond: '제약 없음',
      formula: `$_${n}H_${m} = {}_{${n+m-1}}C_${m}$`,
      cnt: repComb(n, m)
    },
  ];

  let html = '';
  for (const r of rows) {
    html += `<tr><td>${r.name}</td><td>${r.cond}</td><td>${r.formula}</td><td class="hl">${r.cnt}</td></tr>`;
  }
  document.getElementById('sumBody').innerHTML = html;
  if (typeof renderMathInElement !== 'undefined') {
    renderMathInElement(document.getElementById('sumTable'), {
      delimiters:[{left:'$',right:'$',display:false}]
    });
  }
}

// ════════════════════════════════════════════════════════════════════════
// 퀴즈
// ════════════════════════════════════════════════════════════════════════
const ANSWERS = {1:64, 2:24, 3:10, 4:20, 5:15, 6:70, 7:65};
const CORRECT_MSG = {
  1: '🎉 맞아요! 4³ = 64가지',
  2: '🎉 맞아요! ₄P₃ = 4×3×2 = 24가지',
  3: '🎉 맞아요! ₅C₃ = 10가지',
  4: '🎉 맞아요! ₄H₃ = ₆C₃ = 20가지',
  5: '🎉 맞아요! ₆C₄ = 15가지',
  6: '🎉 맞아요! ₅H₄ = ₈C₄ = 70가지',
  7: '🎉 맞아요! 5³ - ₅P₃ = 125 - 60 = 65가지',
};
const WRONG_MSG = {
  1: `❌ 다시 생각해봐요. n^m = 4³ = 64`,
  2: `❌ 다시 생각해봐요. ₄P₃ = 4×3×2 = 24`,
  3: `❌ 다시 생각해봐요. ₅C₃ = 10`,
  4: `❌ 다시 생각해봐요. ₄H₃ = ₆C₃ = 20`,
  5: `❌ 다시 생각해봐요. ₆C₄ = 15`,
  6: `❌ 다시 생각해봐요. ₅H₄ = ₈C₄ = 70`,
  7: `❌ 다시 생각해봐요. 5³ - ₅P₃ = 125 - 60 = 65`,
};

function checkQ(idx, ans) {
  const val = parseInt(document.getElementById('qi'+idx).value);
  const fb = document.getElementById('qf'+idx);
  fb.className = 'q-feedback';
  if (isNaN(val)) { fb.className = 'q-feedback wrong'; fb.textContent = '숫자를 입력해주세요.'; return; }
  if (val === ans) {
    fb.className = 'q-feedback correct';
    fb.textContent = CORRECT_MSG[idx];
  } else {
    fb.className = 'q-feedback wrong';
    fb.textContent = WRONG_MSG[idx];
  }
}

function checkAll() {
  let correct = 0;
  for (let i = 1; i <= 7; i++) {
    const val = parseInt(document.getElementById('qi'+i).value);
    if (val === ANSWERS[i]) correct++;
  }
  const box = document.getElementById('scoreBox');
  box.style.display = 'block';
  document.getElementById('scoreText').textContent = `${correct} / 7`;
  const msgs = ['다시 한번 개념을 복습해봐요!','조금 더 연습이 필요해요!','잘 하고 있어요!','거의 다 맞았어요!','완벽해요! 🎊'];
  document.getElementById('scoreMsg').textContent = msgs[Math.min(Math.floor(correct/7*4), 4)];
  box.scrollIntoView({behavior:'smooth'});
}

// ── 초기화 ────────────────────────────────────────────────────────────────
window.addEventListener('load', () => {
  update1();
  update2();
  update3();
  update4();
  updateSummary();
});
</script>

</body>
</html>
"""
