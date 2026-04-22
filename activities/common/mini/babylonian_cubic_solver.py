# activities/common/mini/babylonian_cubic_solver.py
"""
바빌로니아인의 방정식 풀이 미니활동
바빌로니아인들이 n³+n² 표를 이용해 ax³+bx²=c 형태의 삼차방정식을 풀던
고대 수학적 방법을 직접 체험합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "바빌로니아방정식풀이"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "바빌로니아원리",
        "label":  "바빌로니아인들은 왜 ax³+bx²=c를 (a/b·x)³+(a/b·x)²=ca²/b³ 형태로 변환했을까요? 이 변환의 핵심 아이디어를 자신의 말로 설명해 보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "표의역할",
        "label":  "n³+n²의 표가 없었다면 바빌로니아인들은 어떻게 방정식을 풀었을까요? 표가 갖는 수학적·실용적 역할에 대해 생각해 보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "현대수학연결",
        "label":  "바빌로니아 방법과 오늘날 우리가 배운 방정식 풀이(인수분해, 근의 공식 등)는 어떤 점이 비슷하고 어떤 점이 다른가요?",
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
    "title":       "🏺 바빌로니아인의 방정식 풀이",
    "description": "4000년 전 바빌로니아인들이 n³+n² 표를 이용해 삼차방정식을 풀던 방법을 단계별로 체험합니다.",
    "order":       252,
    "hidden":      False,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>바빌로니아인의 방정식 풀이</title>
<style>
html { font-size: 16px; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', system-ui, sans-serif;
  background: linear-gradient(155deg, #1a0e05 0%, #2d1a08 40%, #1a0e05 100%);
  color: #f0e6d3;
  padding: 14px 12px 32px;
}

/* ─── Tabs ─── */
.tabs { display: flex; gap: 6px; margin-bottom: 16px; }
.tab {
  flex: 1; padding: 10px 6px; border: none; border-radius: 12px;
  background: rgba(255,255,255,0.06); color: #a89070;
  font-size: 0.8rem; font-weight: 700; cursor: pointer;
  transition: 0.2s; font-family: inherit; line-height: 1.5;
}
.tab.active { background: linear-gradient(135deg, #92400e, #b45309); color: #fef3c7; }
.tab:hover:not(.active) { background: rgba(255,255,255,0.1); color: #fde68a; }

/* ─── Screens ─── */
.screen { display: none; animation: fadeIn 0.3s ease; }
.screen.active { display: block; }
@keyframes fadeIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:none; } }

/* ─── Hero ─── */
.hero {
  background: linear-gradient(135deg, rgba(146,64,14,0.25), rgba(120,53,15,0.15));
  border: 1px solid rgba(251,191,36,0.3); border-radius: 14px;
  padding: 14px 18px; margin-bottom: 14px; text-align: center;
}
.hero h2 { font-size: 1.3rem; color: #fbbf24; margin-bottom: 6px; }
.hero p  { font-size: 0.9rem; color: #a89070; line-height: 1.7; }
.hero .highlight { color: #fde68a; font-weight: 700; }

/* ─── Card ─── */
.card {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(251,191,36,0.15);
  border-radius: 14px; padding: 16px 18px; margin-bottom: 14px;
}
.card-title {
  font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em;
  text-transform: uppercase; color: #fbbf24; margin-bottom: 12px;
}

/* ─── Math ─── */
.eq-box {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 1.45rem; color: #fde68a; text-align: center;
  background: rgba(253,230,138,0.07); border: 1px solid rgba(253,230,138,0.2);
  border-radius: 10px; padding: 14px 12px; margin: 10px 0;
  line-height: 1.7;
}
.math { font-family: 'Times New Roman', Georgia, serif; font-style: italic; color: #fde68a; }
.math-sm { font-family: 'Times New Roman', Georgia, serif; font-style: italic; color: #fbbf24; font-size: 0.95rem; }

/* ─── Buttons ─── */
.btn {
  padding: 10px 22px; border-radius: 10px; border: none; cursor: pointer;
  font-size: 0.92rem; font-weight: 700; transition: 0.18s; font-family: inherit;
}
.btn-amber { background: linear-gradient(135deg, #92400e, #b45309); color: #fef3c7; }
.btn-amber:hover { opacity: 0.88; transform: translateY(-1px); }
.btn-ghost { background: transparent; border: 1px solid rgba(251,191,36,0.3); color: #fde68a; }
.btn-ghost:hover { background: rgba(251,191,36,0.08); }
.btn-sm { padding: 7px 14px; font-size: 0.83rem; }

/* ─── Step indicator ─── */
.step-flow {
  display: flex; align-items: center; gap: 0; margin-bottom: 18px; flex-wrap: wrap;
}
.step-node {
  display: flex; align-items: center; justify-content: center;
  width: 34px; height: 34px; border-radius: 50%;
  font-size: 0.82rem; font-weight: 800; flex-shrink: 0;
  border: 2px solid rgba(251,191,36,0.25);
  background: rgba(255,255,255,0.04); color: #6b5a40;
  transition: 0.3s;
}
.step-node.done   { background: rgba(180,83,9,0.4); border-color: #b45309; color: #fde68a; }
.step-node.active { background: linear-gradient(135deg,#92400e,#b45309); border-color: #fbbf24; color: #fff; box-shadow: 0 0 10px rgba(251,191,36,0.4); }
.step-line { flex: 1; height: 2px; background: rgba(251,191,36,0.15); min-width: 10px; }
.step-line.done { background: rgba(180,83,9,0.5); }

/* ─── Table ─── */
.bab-table {
  width: 100%; border-collapse: collapse; font-size: 0.88rem;
  border-radius: 10px; overflow: hidden;
}
.bab-table th {
  background: rgba(146,64,14,0.4); color: #fbbf24; padding: 8px 10px;
  font-family: 'Times New Roman', Georgia, serif; font-style: italic; font-size: 1rem;
  text-align: center;
}
.bab-table td {
  padding: 6px 10px; text-align: center; border-top: 1px solid rgba(255,255,255,0.06);
  color: #d4b896; font-size: 0.88rem; transition: background 0.3s;
}
.bab-table tr:hover td { background: rgba(251,191,36,0.06); }
.bab-table tr.highlight-row td {
  background: rgba(251,191,36,0.18) !important; color: #fde68a; font-weight: 700;
  border-top: 1px solid rgba(251,191,36,0.4);
}
.bab-table td.n-col { font-family: 'Times New Roman', serif; font-style: italic; color: #fbbf24; }
.bab-table td.val-col { font-family: 'Times New Roman', serif; color: #f0e6d3; }

/* ─── Coeff sliders ─── */
.coeff-row {
  display: flex; align-items: center; gap: 8px; margin-bottom: 10px; flex-wrap: wrap;
}
.coeff-label { color: #a89070; font-size: 0.88rem; min-width: 20px; }
.coeff-ctrl { display: flex; align-items: center; gap: 0; }
.coeff-btn {
  width: 28px; height: 32px; border: 1px solid rgba(251,191,36,0.25);
  background: rgba(255,255,255,0.06); color: #fde68a; cursor: pointer;
  font-size: 1rem; font-weight: 700; font-family: inherit; transition: 0.15s;
  display: flex; align-items: center; justify-content: center;
}
.coeff-btn:first-child { border-radius: 8px 0 0 8px; }
.coeff-btn:last-child  { border-radius: 0 8px 8px 0; }
.coeff-btn:hover { background: rgba(251,191,36,0.2); border-color: #fbbf24; }
.coeff-val {
  width: 40px; height: 32px; border: 1px solid rgba(251,191,36,0.2);
  border-left: none; border-right: none;
  background: rgba(255,255,255,0.04); color: #fde68a;
  font-size: 1.05rem; font-weight: 700; text-align: center; font-family: inherit;
  display: flex; align-items: center; justify-content: center;
}
.op-sign { color: #6b5a40; font-size: 1.1rem; }

/* ─── Step reveal ─── */
.step-block {
  border: 1px solid rgba(251,191,36,0.15); border-radius: 12px;
  padding: 14px 16px; margin-bottom: 12px;
  background: rgba(255,255,255,0.03);
  animation: fadeIn 0.4s ease;
}
.step-num {
  font-size: 0.7rem; font-weight: 800; color: #b45309; letter-spacing: 0.08em;
  text-transform: uppercase; margin-bottom: 8px;
}
.arrow-row {
  display: flex; align-items: center; justify-content: center;
  gap: 14px; margin: 10px 0; flex-wrap: wrap;
}
.arrow-box {
  background: rgba(146,64,14,0.2); border: 1px solid rgba(251,191,36,0.2);
  border-radius: 10px; padding: 10px 16px; text-align: center;
  font-family: 'Times New Roman', Georgia, serif; font-size: 1.25rem; color: #fde68a;
  min-width: 130px;
}
.arrow-sym { color: #b45309; font-size: 1.6rem; font-weight: 300; }

/* ─── Result highlight ─── */
.result-badge {
  background: linear-gradient(135deg, rgba(146,64,14,0.3), rgba(180,83,9,0.2));
  border: 1px solid rgba(251,191,36,0.5); border-radius: 12px;
  padding: 14px 18px; text-align: center; margin-top: 10px;
  animation: fadeIn 0.5s ease;
}
.result-badge .big { font-size: 1.6rem; font-weight: 900; color: #fbbf24; margin: 6px 0; }
.result-badge .sub { font-size: 0.88rem; color: #a89070; }

/* ─── Quiz ─── */
.quiz-section { margin-top: 10px; }
.quiz-card { animation: fadeIn 0.3s ease; }
.choice-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(120px,1fr)); gap: 8px; margin: 12px 0; }
.choice-btn {
  padding: 12px 8px; border-radius: 10px;
  border: 2px solid rgba(251,191,36,0.25);
  background: rgba(255,255,255,0.04); color: #d4b896;
  font-size: 1rem; font-weight: 700; cursor: pointer; font-family: inherit;
  font-family: 'Times New Roman', serif; font-style: italic;
  transition: 0.18s; text-align: center;
}
.choice-btn:hover { border-color: #fbbf24; background: rgba(251,191,36,0.1); color: #fde68a; }
.choice-btn.correct { background: rgba(52,211,153,0.2); border-color: #34d399; color: #6ee7b7; pointer-events:none; }
.choice-btn.wrong   { background: rgba(248,113,113,0.15); border-color: #f87171; color: #fca5a5; pointer-events:none; }
.choice-btn.reveal  { background: rgba(52,211,153,0.1); border-color: rgba(52,211,153,0.5); color: #6ee7b7; pointer-events:none; }

.fb-box {
  border-radius: 10px; padding: 11px 14px; font-size: 0.88rem; line-height: 1.8;
  display: none; animation: fadeIn 0.3s ease; margin-top: 8px;
}
.fb-box.show { display: block; }
.fb-ok { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); color: #6ee7b7; }
.fb-ng { background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3); color: #fca5a5; }

/* ─── Progress ─── */
.progress-wrap { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.progress-track { flex: 1; height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg,#92400e,#fbbf24); border-radius: 3px; transition: width 0.4s; }
.progress-label { font-size: 0.8rem; color: #6b5a40; white-space: nowrap; }

/* ─── Score dots ─── */
.score-dots { display: flex; gap: 5px; flex-wrap: wrap; }
.s-dot {
  width: 22px; height: 22px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.68rem; font-weight: 700;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
  color: #6b5a40; transition: 0.3s;
}
.s-dot.ok   { background: rgba(52,211,153,0.25); border-color: rgba(52,211,153,0.5); color: #34d399; }
.s-dot.fail { background: rgba(248,113,113,0.2); border-color: rgba(248,113,113,0.4); color: #f87171; }

/* ─── Info box ─── */
.info-box {
  background: rgba(251,191,36,0.07); border: 1px solid rgba(251,191,36,0.2);
  border-radius: 10px; padding: 11px 14px; margin-bottom: 12px;
  font-size: 0.87rem; color: #c9a96e; line-height: 1.8;
}
.info-box strong { color: #fde68a; }

/* ─── Nav ─── */
.nav-row { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; }

/* ─── Final ─── */
.final-box { text-align: center; padding: 18px 10px; }
.big-score { font-size: 2.8rem; font-weight: 900; color: #fbbf24; line-height: 1.2; margin: 8px 0; }
.grade-txt  { font-size: 0.95rem; color: #a89070; margin-bottom: 14px; }

/* ─── Scroll hint ─── */
.scroll-hint { font-size: 0.78rem; color: #6b5a40; text-align: center; padding: 6px; margin-top: 4px; }
</style>
</head>
<body>

<!-- ═══ TABS ═══ -->
<div class="tabs">
  <button class="tab active" onclick="switchTab(0)" id="tab0">📜 활동 1<br>표 탐구</button>
  <button class="tab" onclick="switchTab(1)" id="tab1">🧮 활동 2<br>방정식 풀기</button>
  <button class="tab" onclick="switchTab(2)" id="tab2">🏆 활동 3<br>도전 문제</button>
</div>

<!-- ══════════════════════════════════════════════════
     SCREEN 0 — n³+n² 표 탐구
══════════════════════════════════════════════════ -->
<div class="screen active" id="screen0">

  <div class="hero">
    <h2>📜 바빌로니아인의 비밀 표</h2>
    <p>지금으로부터 약 <span class="highlight">4000년 전</span>, 바빌로니아인들은<br>
    <span class="highlight">n³ + n²</span>의 값을 계산한 표를 남겼습니다.<br>
    이 표가 어떻게 삼차방정식을 푸는 데 쓰였는지 탐구해 봅시다!</p>
  </div>

  <!-- 단계 1 : 표 채우기 -->
  <div class="card">
    <div class="card-title">① n³ + n² 표 채우기</div>
    <div class="info-box">
      바빌로니아인들은 <strong>n = 1부터 30</strong>까지 <strong>n³ + n²</strong>의 값을 모두 계산해 두었습니다.<br>
      아래 표의 빈칸에 들어갈 값을 직접 계산해 보세요!
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
      <!-- 입력 영역 -->
      <div>
        <div style="font-size:0.85rem;color:#a89070;margin-bottom:8px;">n 값을 선택하면 계산에 도전!</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;" id="nBtnGroup"></div>
        <div id="calcChallenge" style="display:none;">
          <div class="step-block">
            <div class="step-num">계산 도전 ─ n = <span id="selN">?</span></div>
            <div style="font-size:0.88rem;color:#a89070;margin-bottom:6px;">
              <span id="selN2">n</span>³ + <span id="selN3">n</span>² = ?
            </div>
            <div style="font-size:0.85rem;color:#6b5a40;margin-bottom:10px;">
              = <span id="cubeCalc" style="color:#fde68a">n</span>³ + <span id="sqCalc" style="color:#fde68a">n</span>² = ?
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;" id="answerBtns"></div>
            <div class="fb-box" id="calcFb"></div>
          </div>
        </div>
      </div>

      <!-- 완성된 표 -->
      <div>
        <div style="font-size:0.85rem;color:#a89070;margin-bottom:8px;">n³ + n² 완성 표</div>
        <div style="max-height:280px;overflow-y:auto;border-radius:10px;border:1px solid rgba(251,191,36,0.15);">
          <table class="bab-table" id="babTable">
            <thead><tr><th>n</th><th>n³ + n²</th></tr></thead>
            <tbody id="babTbody"></tbody>
          </table>
        </div>
        <div class="scroll-hint">↕ 스크롤하여 더 보기</div>
      </div>
    </div>

    <div class="nav-row">
      <div style="font-size:0.83rem;color:#6b5a40;">표 패턴이 보이나요?<br>연속된 두 행의 차이를 계산해 보세요!</div>
      <button class="btn btn-amber" onclick="switchTab(1)">다음 활동 →</button>
    </div>
  </div>

</div>

<!-- ══════════════════════════════════════════════════
     SCREEN 1 — 방정식 단계별 풀기
══════════════════════════════════════════════════ -->
<div class="screen" id="screen1">

  <div class="hero">
    <h2>🧮 바빌로니아인처럼 방정식 풀기</h2>
    <p>삼차방정식 <span class="highlight">ax³ + bx² = c</span>를<br>
    바빌로니아인의 방법으로 단계별로 풀어봅시다!</p>
  </div>

  <!-- 방정식 설정 -->
  <div class="card">
    <div class="card-title">① 방정식 직접 설정하기</div>
    <div class="info-box">
      계수 <strong>a</strong>, <strong>b</strong>, <strong>c</strong>를 조절하여 풀고 싶은 방정식을 만들어 보세요.<br>
      (단, 바빌로니아 표에서 찾을 수 있는 정수 해가 존재하도록 설계되어 있습니다)
    </div>

    <div class="coeff-row">
      <span class="coeff-label">a</span>
      <div class="coeff-ctrl">
        <button class="coeff-btn" onclick="adjABC(0,-1)">−</button>
        <div class="coeff-val" id="valA">25</div>
        <button class="coeff-btn" onclick="adjABC(0,+1)">+</button>
      </div>
      <span class="op-sign">x³ +</span>
      <span class="coeff-label">b</span>
      <div class="coeff-ctrl">
        <button class="coeff-btn" onclick="adjABC(1,-1)">−</button>
        <div class="coeff-val" id="valB">5</div>
        <button class="coeff-btn" onclick="adjABC(1,+1)">+</button>
      </div>
      <span class="op-sign">x² =</span>
      <span class="coeff-label">c</span>
      <div class="coeff-ctrl">
        <button class="coeff-btn" onclick="adjABC(2,-1)">−</button>
        <div class="coeff-val" id="valC">16</div>
        <button class="coeff-btn" onclick="adjABC(2,+1)">+</button>
      </div>
    </div>

    <div class="eq-box" id="eqDisplay">25x³ + 5x² = 16</div>
    <div style="text-align:center;font-size:0.82rem;color:#6b5a40;margin-bottom:10px;" id="solvHint"></div>

    <div style="text-align:center;">
      <button class="btn btn-amber" onclick="startSolve()" style="width:100%;font-size:1rem;padding:12px;">
        🏺 바빌로니아 방식으로 풀기!
      </button>
    </div>
  </div>

  <!-- 풀이 단계 -->
  <div id="solveSteps" style="display:none;">

    <!-- 단계 흐름 표시 -->
    <div class="card" style="padding:14px 18px 10px;">
      <div class="card-title">풀이 진행 단계</div>
      <div class="step-flow" id="stepFlow">
        <div class="step-node" id="sn0">1</div>
        <div class="step-line" id="sl0"></div>
        <div class="step-node" id="sn1">2</div>
        <div class="step-line" id="sl1"></div>
        <div class="step-node" id="sn2">3</div>
        <div class="step-line" id="sl2"></div>
        <div class="step-node" id="sn3">4</div>
        <div class="step-line" id="sl3"></div>
        <div class="step-node" id="sn4">5</div>
      </div>
    </div>

    <!-- Step 1: 양변 변환 -->
    <div class="card" id="stepCard0">
      <div class="card-title">단계 1 — 양변에 a²/b³ 곱하기</div>
      <div style="font-size:0.9rem;color:#a89070;line-height:1.85;margin-bottom:10px;">
        방정식 <span id="eq1orig" class="math-sm">ax³+bx²=c</span> 의 양변에
        <span id="eq1mul" class="math-sm">a²/b³</span>을 곱합니다.
      </div>
      <div class="arrow-row">
        <div class="arrow-box" id="step1left">ax³+bx²=c</div>
        <div class="arrow-sym">×<br><span style="font-size:0.9rem;font-style:italic;">a²/b³</span></div>
        <div class="arrow-box" id="step1right">?</div>
      </div>
      <div class="eq-box" id="step1result" style="font-size:1.2rem;margin-top:10px;">—</div>
      <div style="font-size:0.85rem;color:#a89070;margin-top:8px;line-height:1.7;" id="step1explain">
        <strong style="color:#fde68a">핵심:</strong>
        ax를 b로 나눈 값을 <em>y = (a/b)x</em>로 치환하면<br>
        <strong style="color:#fde68a">y³ + y² = ca²/b³</strong> 형태가 됩니다.
      </div>
      <div class="nav-row" style="margin-top:12px;">
        <div></div>
        <button class="btn btn-amber btn-sm" onclick="showStep(1)">다음 단계 →</button>
      </div>
    </div>

    <!-- Step 2: y 치환 -->
    <div class="card" id="stepCard1" style="display:none;">
      <div class="card-title">단계 2 — y = (a/b)x 로 치환</div>
      <div style="font-size:0.9rem;color:#a89070;line-height:1.85;margin-bottom:10px;">
        <span id="step2subst" class="math-sm">y = (a/b)x</span>로 놓으면
        방정식이 <strong style="color:#fde68a">y³ + y² = k</strong> 형태가 됩니다.
      </div>
      <div class="eq-box" id="step2result" style="font-size:1.3rem;">y³ + y² = k</div>
      <div style="text-align:center;margin:10px 0;">
        <span style="font-size:0.9rem;color:#a89070;">여기서 </span>
        <span class="math" id="step2k" style="font-size:1.3rem;">k = ?</span>
      </div>
      <div class="eq-box" id="step2kbox" style="font-size:1.1rem;background:rgba(251,191,36,0.1);border-color:rgba(251,191,36,0.4);">k = ca²/b³ = ?</div>
      <div class="nav-row" style="margin-top:12px;">
        <button class="btn btn-ghost btn-sm" onclick="showStep(0)">← 이전</button>
        <button class="btn btn-amber btn-sm" onclick="showStep(2)">다음 단계 →</button>
      </div>
    </div>

    <!-- Step 3: 표에서 찾기 -->
    <div class="card" id="stepCard2" style="display:none;">
      <div class="card-title">단계 3 — n³+n² 표에서 y 값 찾기</div>
      <div class="info-box">
        <strong>k = <span id="step3k">?</span></strong> 가 되는 n을 표에서 찾습니다.<br>
        표에서 n³+n² = k 인 행을 클릭해 보세요!
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
        <div>
          <div style="font-size:0.82rem;color:#a89070;margin-bottom:6px;">n³+n² 표 (클릭해서 찾기!)</div>
          <div style="max-height:260px;overflow-y:auto;border-radius:10px;border:1px solid rgba(251,191,36,0.15);">
            <table class="bab-table" id="lookupTable">
              <thead><tr><th>n</th><th>n³+n²</th></tr></thead>
              <tbody id="lookupTbody"></tbody>
            </table>
          </div>
          <div class="scroll-hint">↕ 스크롤하여 찾기</div>
        </div>
        <div>
          <div style="font-size:0.82rem;color:#a89070;margin-bottom:8px;">찾은 결과</div>
          <div id="lookupResult" class="result-badge" style="display:none;">
            <div style="font-size:0.85rem;color:#a89070;">n³ + n² = <span id="foundK" style="color:#fde68a">?</span></div>
            <div class="big">n = <span id="foundN">?</span></div>
            <div style="font-size:0.9rem;color:#fde68a;margin-top:4px;">∴ y = <span id="foundY">?</span></div>
          </div>
          <div id="lookupHint" style="font-size:0.83rem;color:#6b5a40;padding:10px;">
            왼쪽 표에서 k 값과 같은 행을 클릭하세요!
          </div>
        </div>
      </div>
      <div class="nav-row" style="margin-top:12px;">
        <button class="btn btn-ghost btn-sm" onclick="showStep(1)">← 이전</button>
        <button class="btn btn-amber btn-sm" id="step3Next" onclick="showStep(3)" style="display:none;">다음 단계 →</button>
      </div>
    </div>

    <!-- Step 4: x 역산 -->
    <div class="card" id="stepCard3" style="display:none;">
      <div class="card-title">단계 4 — y에서 x 역산하기</div>
      <div style="font-size:0.9rem;color:#a89070;line-height:1.85;margin-bottom:10px;">
        y = (a/b)x 이므로 x = (b/a)y 입니다.
      </div>
      <div class="arrow-row">
        <div class="arrow-box" id="step4y">y = ?</div>
        <div class="arrow-sym">÷<br><span style="font-size:0.9rem;font-style:italic;">a/b</span></div>
        <div class="arrow-box" id="step4x">x = ?</div>
      </div>
      <div class="eq-box" id="step4result" style="font-size:1.3rem;">x = (b/a) × y = ?</div>
      <div class="nav-row" style="margin-top:12px;">
        <button class="btn btn-ghost btn-sm" onclick="showStep(2)">← 이전</button>
        <button class="btn btn-amber btn-sm" onclick="showStep(4)">다음 단계 →</button>
      </div>
    </div>

    <!-- Step 5: 검증 -->
    <div class="card" id="stepCard4" style="display:none;">
      <div class="card-title">단계 5 — 답 검증하기</div>
      <div class="result-badge">
        <div style="font-size:1rem;color:#a89070;">최종 답</div>
        <div class="big" id="step5final">x = ?</div>
        <div class="sub" id="step5verify">검증 중...</div>
      </div>
      <div class="step-block" style="margin-top:12px;" id="step5checkBlock">
        <div class="step-num">검증 계산</div>
        <div style="font-size:0.88rem;color:#a89070;line-height:2;" id="step5calc">계산 중...</div>
      </div>
      <div class="nav-row" style="margin-top:12px;">
        <button class="btn btn-ghost btn-sm" onclick="showStep(3)">← 이전</button>
        <button class="btn btn-amber" onclick="switchTab(2)">도전 문제 풀러 가기! →</button>
      </div>
    </div>

  </div>

</div>

<!-- ══════════════════════════════════════════════════
     SCREEN 2 — 도전 문제
══════════════════════════════════════════════════ -->
<div class="screen" id="screen2">

  <div class="hero">
    <h2>🏆 바빌로니아인처럼 문제 풀기!</h2>
    <p>이제 직접 방정식을 분석하고 답을 찾아보세요.<br>
    바빌로니아 방법이 <span class="highlight">통하는지 안 통하는지</span>도 판단해야 합니다!</p>
  </div>

  <div class="progress-wrap">
    <div class="progress-track"><div class="progress-fill" id="qzFill" style="width:0%"></div></div>
    <span class="progress-label" id="qzLabel">0 / 5</span>
    <div class="score-dots" id="qzDots"></div>
  </div>

  <div id="qzSection">
    <div class="card quiz-card" id="qzCard">
      <div class="card-title" id="qzTitle">문제 1</div>
      <div class="eq-box" id="qzEq">—</div>
      <div style="font-size:0.87rem;color:#a89070;margin-bottom:10px;" id="qzDesc">—</div>
      <div class="choice-grid" id="qzChoices"></div>
      <div class="fb-box" id="qzFb"></div>
      <div style="text-align:right;margin-top:10px;">
        <button class="btn btn-amber btn-sm" id="qzNext" onclick="qzNextQ()" style="display:none">다음 문제 →</button>
      </div>
    </div>
  </div>

  <div id="qzFinal" style="display:none;">
    <div class="card final-box">
      <div style="font-size:2rem;margin-bottom:4px;">🏺 완료!</div>
      <div class="big-score" id="qzScore">—</div>
      <div class="grade-txt" id="qzMsg">—</div>
      <button class="btn btn-amber" onclick="qzReset()">다시 도전 🔄</button>
    </div>
    <div class="card">
      <div class="card-title">📌 바빌로니아 방법 핵심 정리</div>
      <div style="font-size:0.88rem;color:#a89070;line-height:2;">
        ① ax³ + bx² = c 형태인지 확인<br>
        ② 양변에 <em style="font-family:serif">a²/b³</em>을 곱해 <em style="font-family:serif">y³+y²=k</em>로 변환<br>
        ③ n³+n² 표에서 k가 되는 n을 탐색<br>
        ④ x = (b/a)·n 으로 역산<br>
        <span style="color:#fde68a;font-weight:700;">단,</span> k가 표에 없으면 이 방법으로는 풀 수 없음!
      </div>
    </div>
  </div>

</div>

<!-- ─────────────── SCRIPT ─────────────── -->
<script>

/* ── 공통 유틸 ── */
function notifyHeight(){
  const h = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight,
                     document.body.offsetHeight, document.documentElement.offsetHeight) + 24;
  window.parent.postMessage({isStreamlitMessage:true,type:'streamlit:setFrameHeight',args:{height:h}},'*');
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
function scheduleResize(d){
  const fire = ()=>{ notifyHeight(); setTimeout(notifyHeight, 80); setTimeout(notifyHeight, 250); };
  d ? setTimeout(fire, d) : fire();
}
new ResizeObserver(()=>scheduleResize(0)).observe(document.body);
window.addEventListener('load', ()=>{ scheduleResize(0); scheduleResize(300); });

function switchTab(idx){
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',i===idx));
  document.querySelectorAll('.screen').forEach((s,i)=>s.classList.toggle('active',i===idx));
  scheduleResize(60);
}

/* ── n³+n² 표 데이터 ── */
const BAB_TABLE = [];
for(let n=1;n<=30;n++) BAB_TABLE.push({n, val: n*n*n + n*n});

/* ════════════════════════════════════════
   SCREEN 0 — 표 탐구
════════════════════════════════════════ */

// n 선택 버튼
(function buildNBtns(){
  const group = document.getElementById('nBtnGroup');
  [1,2,3,4,5,6,7,8,10].forEach(n=>{
    const btn = document.createElement('button');
    btn.className = 'btn btn-ghost btn-sm';
    btn.style.fontFamily = 'Times New Roman, serif';
    btn.style.fontStyle = 'italic';
    btn.textContent = 'n = '+n;
    btn.onclick = ()=> startCalcChallenge(n);
    group.appendChild(btn);
  });
})();

// 표 생성
(function buildBabTable(){
  const tbody = document.getElementById('babTbody');
  BAB_TABLE.forEach(row=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `<td class="n-col">${row.n}</td><td class="val-col">${row.val.toLocaleString()}</td>`;
    tbody.appendChild(tr);
  });
})();

let _calcN = 0;
function startCalcChallenge(n){
  _calcN = n;
  const correct = n*n*n + n*n;
  document.getElementById('selN').textContent = n;
  document.getElementById('selN2').textContent = n;
  document.getElementById('selN3').textContent = n;
  document.getElementById('cubeCalc').textContent = n+'³ = '+n*n*n;
  document.getElementById('sqCalc').textContent   = n+'² = '+n*n;
  document.getElementById('calcFb').className = 'fb-box';
  document.getElementById('calcFb').innerHTML = '';

  // 4 보기 생성 (correct + 3 distractors)
  const pool = new Set([correct]);
  while(pool.size < 4){
    const delta = Math.floor(Math.random()*10+1)*(Math.random()<0.5?1:-1);
    const v = correct + delta;
    if(v>0) pool.add(v);
  }
  const choices = [...pool].sort(()=>Math.random()-0.5);
  const container = document.getElementById('answerBtns');
  container.innerHTML = '';
  choices.forEach(c=>{
    const b = document.createElement('button');
    b.className = 'btn btn-ghost btn-sm';
    b.textContent = c.toLocaleString();
    b.style.fontFamily = 'Times New Roman, serif';
    b.onclick = ()=> checkCalc(b, c, correct, choices);
    container.appendChild(b);
  });

  document.getElementById('calcChallenge').style.display = 'block';

  // 표에서 해당 행 강조
  const rows = document.querySelectorAll('#babTbody tr');
  rows.forEach((r,i)=>{
    r.classList.toggle('highlight-row', BAB_TABLE[i].n === n);
  });

  scheduleResize(30);
}

function checkCalc(btn, chosen, correct, choices){
  const ok = chosen === correct;
  const allBtns = document.getElementById('answerBtns').querySelectorAll('button');
  allBtns.forEach(b=>{ b.disabled=true; b.style.opacity='0.6'; });
  btn.style.opacity='1';
  btn.classList.add(ok?'correct':'wrong');

  // 정답 강조
  if(!ok){
    allBtns.forEach(b=>{
      if(parseInt(b.textContent.replace(/,/g,''))===correct) b.classList.add('reveal');
    });
  }

  const fb = document.getElementById('calcFb');
  fb.innerHTML = ok
    ? `✅ <strong>정답!</strong> ${_calcN}³ + ${_calcN}² = ${_calcN**3} + ${_calcN**2} = <strong>${correct.toLocaleString()}</strong>`
    : `❌ 오답. 정답은 <strong>${correct.toLocaleString()}</strong>입니다.<br>
       ${_calcN}³ = ${_calcN**3}, ${_calcN}² = ${_calcN**2} → 합 = ${correct}`;
  fb.className = 'fb-box show ' + (ok?'fb-ok':'fb-ng');
  scheduleResize(30);
}


/* ════════════════════════════════════════
   SCREEN 1 — 방정식 풀기
════════════════════════════════════════ */

// 예제: 25x³+5x²=16 → (5/5·x)=(5x)³+(5x)²=16*25/125=80/5=16... wait
// 실제 예제 목록 (정수 해 보장)
const PRESET_EQS = [
  {a:25, b:5, c:16, x:0.8, desc:'교과서 96p 예제'},      // y=5x, k=16*25/125=80, n=4, y=4, x=4/5
  {a:8,  b:4, c:9,  x:1.5, desc:'자연수 해 탐구'},        // y=2x, k=9*64/64=9... wait, let me recalc
  {a:1,  b:1, c:2,  x:1,   desc:'n=1인 경우'},            // y=x, k=2, n=1, x=1
  {a:1,  b:1, c:12, x:2,   desc:'n=2인 경우'},            // y=x, k=12, n=2, x=2
  {a:1,  b:1, c:36, x:3,   desc:'n=3인 경우'},            // y=x, k=36, n=3, x=3
];
// Verify: for {a,b,c}: k = c*a^2/b^3; look up n with n^3+n^2=k; x=b/a*n
// a=25,b=5,c=16: k=16*625/125=80 → n=4 → x=5/25*4=4/5=0.8 ✓
// a=8,b=4,c=9: k=9*64/64=9 → n? 1³+1²=2, 2³+2²=12... not 9. Bad.

// Better to just compute dynamically.
// 정수 n에 대해 방정식 생성: given a,b,n → c = n^3/(a^2/b^3) = n^3*b^3/a^2... wait
// ax³+bx²=c, x=b/a*n → a*(b/a*n)^3 + b*(b/a*n)^2 = c
// = a * b^3/a^3 * n^3 + b * b^2/a^2 * n^2
// = b^3/a^2 * n^3 + b^3/a^2 * n^2
// = b^3/a^2 * (n^3+n^2)
// So c = b^3/a^2 * (n^3+n^2)
// For c to be a nice number: need b^3/a^2*(n^3+n^2) integer
// Simplest: a=b → c = a*(n^3+n^2)/a^0 = n^3+n^2
// Or a=n, b=a=n: c = n^3/n^2 * (n^3+n^2) = n*(n^3+n^2)...

// Let's use: a=b case → x=n, c=n^3+n^2
// Preset examples with a=b=k gives x=n_answer
const GOOD_PRESETS = [
  {a:1, b:1, c:2,  label:'1x³ + 1x² = 2',   ans_n:1, desc:'가장 기본 예제'},
  {a:1, b:1, c:12, label:'x³ + x² = 12',    ans_n:2, desc:'n=2 탐구'},
  {a:1, b:1, c:36, label:'x³ + x² = 36',    ans_n:3, desc:'n=3 탐구'},
  {a:25,b:5, c:16, label:'25x³ + 5x² = 16', ans_n:4, desc:'교과서 96p 예제 (x = 4/5)'},
  {a:1, b:1, c:80, label:'x³ + x² = 80',    ans_n:4, desc:'n=4 탐구'},
];

let S = {a:25, b:5, c:16, curStep: -1};
let solveData = {};

function adjABC(idx, delta){
  if(idx===0) S.a = Math.max(1, Math.min(30, S.a+delta));
  if(idx===1) S.b = Math.max(1, Math.min(30, S.b+delta));
  if(idx===2) S.c = Math.max(1, Math.min(200, S.c+delta));
  updateEqDisplay();
}

function updateEqDisplay(){
  document.getElementById('valA').textContent = S.a;
  document.getElementById('valB').textContent = S.b;
  document.getElementById('valC').textContent = S.c;

  // Show equation
  const aStr = S.a===1?'':S.a;
  const bStr = S.b===1?'':S.b;
  document.getElementById('eqDisplay').textContent = `${aStr}x³ + ${bStr}x² = ${S.c}`;

  // Check if solvable with integer n
  // k = c*a^2/b^3 must = n^3+n^2 for some integer n
  const k = S.c * S.a * S.a / (S.b * S.b * S.b);
  const matchRow = BAB_TABLE.find(r=> Math.abs(r.val - k) < 1e-9);
  const hint = document.getElementById('solvHint');
  if(matchRow){
    const n = matchRow.n;
    const xNum = S.b * n, xDen = S.a;
    const g = gcd(xNum, xDen);
    const x = xNum===xDen ? '1' : (xDen===1 ? xNum : `${xNum/g}/${xDen/g}`);
    hint.textContent = `✅ 바빌로니아 방법으로 풀 수 있습니다! (k = ${k})`;
    hint.style.color = '#6ee7b7';
  } else {
    hint.textContent = `⚠️ k = ${k.toFixed(2)} — 표에 없어 이 방법으로는 풀기 어렵습니다.`;
    hint.style.color = '#fca5a5';
  }
}

function gcd(a,b){ return b===0?a:gcd(b,a%b); }
function fracStr(num, den){
  if(num===0) return '0';
  const g = gcd(Math.abs(num), Math.abs(den));
  const n=num/g, d=den/g;
  return d===1 ? `${n}` : `${n}/${d}`;
}

function startSolve(){
  const k = S.c * S.a * S.a / (S.b * S.b * S.b);
  const matchRow = BAB_TABLE.find(r=> Math.abs(r.val - k) < 1e-9);
  if(!matchRow){
    alert(`k = ${k.toFixed(3)} 은 n³+n² 표에 없습니다.\n다른 계수를 시도해 보세요!`);
    return;
  }

  // Compute all data
  const n = matchRow.n;
  const xFrac_num = S.b * n, xFrac_den = S.a;
  const g = gcd(xFrac_num, xFrac_den);
  const xn = xFrac_num/g, xd = xFrac_den/g;
  const xStr = xd===1 ? `${xn}` : `${xn}/${xd}`;
  const aOnB = fracStr(S.a, S.b);
  const bOnA = fracStr(S.b, S.a);

  solveData = { a:S.a, b:S.b, c:S.c, k, n, xn, xd, xStr, aOnB, bOnA };

  // Fill step 1
  document.getElementById('step1left').innerHTML =
    `${S.a}x³ + ${S.b}x² = ${S.c}`;
  document.getElementById('step1right').innerHTML =
    `(${S.a>1?S.a:''}/${S.b>1?S.b:1}·x)³ + (${S.a>1?S.a:''}/${S.b>1?S.b:1}·x)² = ${S.c}·${S.a}²/${S.b}³`;
  document.getElementById('step1result').textContent =
    `(${aOnB}x)³ + (${aOnB}x)² = ${k % 1 === 0 ? k : k.toFixed(4)}`;
  document.getElementById('eq1orig').textContent = `${S.a}x³ + ${S.b}x² = ${S.c}`;
  document.getElementById('eq1mul').textContent  = `${S.a}²/${S.b}³ = ${S.a**2}/${S.b**3}`;
  document.getElementById('step1explain').innerHTML =
    `<strong style="color:#fde68a">핵심:</strong> <em>y = ${aOnB}x</em> 로 치환하면<br>
     <strong style="color:#fde68a">y³ + y² = ${k % 1===0?k:k.toFixed(4)}</strong> 형태가 됩니다.`;

  // Fill step 2
  document.getElementById('step2subst').textContent = `y = (${S.a}/${S.b})x = ${aOnB}x`;
  document.getElementById('step2result').textContent = `y³ + y² = ${k%1===0?k:k.toFixed(4)}`;
  document.getElementById('step2k').textContent = `k = ${k%1===0?k:k.toFixed(4)}`;
  document.getElementById('step2kbox').innerHTML =
    `k = c·a²/b³ = ${S.c}·${S.a}²/${S.b}³ = ${S.c}·${S.a**2}/${S.b**3} = <strong>${k%1===0?k:k.toFixed(4)}</strong>`;

  // Fill step 3
  document.getElementById('step3k').textContent = k%1===0?k:k.toFixed(4);
  buildLookupTable(k);

  // Fill step 4
  document.getElementById('step4y').innerHTML = `y = ${n}`;
  document.getElementById('step4x').innerHTML = `x = (${bOnA}) × ${n} = ${xStr}`;
  document.getElementById('step4result').textContent =
    `x = (b/a) × n = (${S.b}/${S.a}) × ${n} = ${xStr}`;

  // Fill step 5
  document.getElementById('step5final').textContent = `x = ${xStr}`;
  // Verify
  const xVal = xn/xd;
  const lhs  = S.a * xVal**3 + S.b * xVal**2;
  const ok   = Math.abs(lhs - S.c) < 1e-6;
  document.getElementById('step5verify').innerHTML = ok
    ? `✅ ${S.a}×(${xStr})³ + ${S.b}×(${xStr})² = ${lhs.toFixed(4)} ≈ ${S.c} (검증 완료!)`
    : `⚠️ 검증 오류`;
  document.getElementById('step5calc').innerHTML =
    `<em>${S.a}x³ + ${S.b}x² = ${S.c}</em> 에 x = ${xStr} 대입<br>
     = ${S.a} × (${xStr})³ + ${S.b} × (${xStr})²<br>
     = ${S.a} × ${(xVal**3).toFixed(4)} + ${S.b} × ${(xVal**2).toFixed(4)}<br>
     = ${(S.a*xVal**3).toFixed(4)} + ${(S.b*xVal**2).toFixed(4)}<br>
     = <strong>${lhs.toFixed(4)}</strong> ${ok?'= '+S.c+' ✅':'≠ '+S.c+' ⚠️'}`;

  // Show solve section and first step
  document.getElementById('solveSteps').style.display = 'block';
  S.curStep = -1;
  showStep(0);
  scheduleResize(80);
}

function showStep(idx){
  // Update step nodes
  for(let i=0;i<5;i++){
    const node = document.getElementById('sn'+i);
    const line = document.getElementById('sl'+i);
    if(i < idx){ node.classList.add('done'); node.classList.remove('active'); }
    else if(i===idx){ node.classList.add('active'); node.classList.remove('done'); }
    else { node.classList.remove('done','active'); }
    if(line) line.classList.toggle('done', i<idx);
  }

  // Show/hide step cards
  for(let i=0;i<5;i++){
    const card = document.getElementById('stepCard'+i);
    if(card) card.style.display = i===idx?'block':'none';
  }
  S.curStep = idx;
  scheduleResize(60);

  // Scroll step card into view
  setTimeout(()=>{
    const card = document.getElementById('stepCard'+idx);
    if(card) card.scrollIntoView({behavior:'smooth', block:'nearest'});
  }, 100);
}

function buildLookupTable(targetK){
  const tbody = document.getElementById('lookupTbody');
  tbody.innerHTML = '';
  BAB_TABLE.forEach(row=>{
    const tr = document.createElement('tr');
    const isTarget = Math.abs(row.val - targetK) < 1e-9;
    if(isTarget) tr.classList.add('highlight-row');
    tr.innerHTML = `<td class="n-col">${row.n}</td><td class="val-col">${row.val.toLocaleString()}</td>`;
    tr.style.cursor = 'pointer';
    tr.onclick = ()=> lookupClick(row, targetK, tr);
    tbody.appendChild(tr);
  });
}

function lookupClick(row, targetK, tr){
  const isCorrect = Math.abs(row.val - targetK) < 1e-9;
  // Flash
  const allRows = document.querySelectorAll('#lookupTbody tr');
  allRows.forEach(r=> r.style.background='');

  if(isCorrect){
    tr.style.background = 'rgba(52,211,153,0.2)';
    const resultDiv = document.getElementById('lookupResult');
    document.getElementById('foundK').textContent = row.val.toLocaleString();
    document.getElementById('foundN').textContent = row.n;
    document.getElementById('foundY').textContent = row.n;
    resultDiv.style.display = 'block';
    document.getElementById('lookupHint').style.display = 'none';
    document.getElementById('step3Next').style.display = 'inline-block';
    scheduleResize(40);
  } else {
    tr.style.background = 'rgba(248,113,113,0.15)';
    document.getElementById('lookupHint').textContent =
      `n=${row.n}일 때 n³+n²=${row.val} ≠ ${targetK%1===0?targetK:targetK.toFixed(4)} 입니다. 계속 찾아보세요!`;
    document.getElementById('lookupHint').style.display = 'block';
    setTimeout(()=>{ tr.style.background=''; }, 800);
  }
}

// Init
updateEqDisplay();


/* ════════════════════════════════════════
   SCREEN 2 — 도전 문제
════════════════════════════════════════ */

const QZ_DATA = [
  {
    eq: 'x³ + x² = 2',
    desc: 'y = x로 치환하면 y³+y² = 2입니다. 표에서 n을 찾아 x를 구하세요.',
    choices: ['x = 1', 'x = 2', 'x = 3', 'x = 없음'],
    answer: 0,
    hint: `n=1일 때 1³+1² = 2 → y=1 → x = 1<br>검증: 1³+1² = 2 ✅`
  },
  {
    eq: '25x³ + 5x² = 16',
    desc: '교과서 96p 예제입니다. a=25, b=5이므로 y=(25/5)x=5x로 치환해 보세요.',
    choices: ['x = 4/5', 'x = 4', 'x = 5', 'x = 1/5'],
    answer: 0,
    hint: `y=5x로 치환 → (5x)³+(5x)² = 16×25/5³ = 80<br>n=4 → 4³+4² = 80 → y=4 → x=4/5 ✅`
  },
  {
    eq: 'x³ − 8x² + 21x − 270 = 0',
    desc: '이 방정식을 바빌로니아 방법으로 풀 수 있을까요? (ax³+bx²=c 형태로 변형 가능한지 확인하세요)',
    choices: ['x = 6 (풀 수 있음)', 'x = 10 (풀 수 있음)', '이 방법으론 풀 수 없음', 'x = 3 (풀 수 있음)'],
    answer: 2,
    hint: `이 방정식은 ax³+bx²=c 형태가 아닙니다.<br>
           x항(21x)과 상수항(−270)이 포함되어 있어<br>
           바빌로니아 방법을 직접 적용하기 어렵습니다.<br>
           <span style="color:#fde68a">→ 현대적 방법(인수정리+조립제법)을 사용해야 합니다!</span>`
  },
  {
    eq: 'x³ + x² = 36',
    desc: '표에서 n³+n²=36이 되는 n을 찾아 x를 구하세요.',
    choices: ['x = 2', 'x = 3', 'x = 4', 'x = 6'],
    answer: 1,
    hint: `n=3 → 3³+3² = 27+9 = 36 ✅<br>y=x (a=b=1) → x = 3`
  },
  {
    eq: '8x³ + 4x² = 9',
    desc: 'a=8, b=4일 때 k = c·a²/b³ = 9×64/64 = 9 입니다. 표에서 n을 찾아보세요.',
    choices: ['x = 1/2', 'x = 3/2', 'x = 3/4', 'x = 2/3'],
    answer: 0,
    hint: `k = 9×8²/4³ = 9×64/64 = 9<br>
           n=? → 2³+2² = 12 ≠ 9, 1³+1²=2 ≠ 9...<br>
           사실 k=9는 표에 없습니다! 정수 n이 없어요.<br>
           <span style="color:#fca5a5">⚠️ 잠깐 — 이 예제를 다시 확인: a=8,b=4,x=1/2 →<br>
           8×(1/2)³+4×(1/2)² = 8×1/8+4×1/4 = 1+1 = 2 ≠ 9</span><br>
           <span style="color:#fde68a">실제로는 x=1/2: 8·(1/8)+4·(1/4)=1+1=2. 이 방정식은 바빌로니아 방법이 맞지 않습니다.<br>
           선생님께 확인해 보세요!</span>`
  },
];

// Fix quiz 5: use a=1,b=1,c=80 (n=4, x=4)
QZ_DATA[4] = {
  eq: 'x³ + x² = 80',
  desc: '표에서 n³+n²=80이 되는 n을 찾아 x를 구하세요.',
  choices: ['x = 3', 'x = 4', 'x = 5', 'x = 6'],
  answer: 1,
  hint: `n=4 → 4³+4² = 64+16 = 80 ✅<br>y=x (a=b=1) → x = 4<br>검증: 4³+4² = 64+16 = 80 ✅`
};

let QZ = {data:[], idx:0, score:0, answered:false};

function qzInit(){
  QZ.data = [...QZ_DATA].sort(()=>Math.random()-0.5);
  QZ.idx = 0; QZ.score = 0; QZ.answered = false;
  buildQzDots();
  loadQz();
  document.getElementById('qzSection').style.display = 'block';
  document.getElementById('qzFinal').style.display   = 'none';
}

function buildQzDots(){
  const el = document.getElementById('qzDots');
  el.innerHTML = QZ.data.map((_,i)=>`<div class="s-dot" id="qd${i}">${i+1}</div>`).join('');
}

function loadQz(){
  const q = QZ.data[QZ.idx];
  const total = QZ.data.length;
  document.getElementById('qzFill').style.width = (QZ.idx/total*100)+'%';
  document.getElementById('qzLabel').textContent = `${QZ.idx}/${total}`;
  document.getElementById('qzTitle').textContent = `문제 ${QZ.idx+1}`;
  document.getElementById('qzEq').textContent = q.eq;
  document.getElementById('qzDesc').textContent = q.desc;
  document.getElementById('qzFb').className = 'fb-box';
  document.getElementById('qzFb').innerHTML = '';
  document.getElementById('qzNext').style.display = 'none';
  QZ.answered = false;

  const grid = document.getElementById('qzChoices');
  grid.innerHTML = '';
  q.choices.forEach((c,i)=>{
    const btn = document.createElement('button');
    btn.className = 'choice-btn';
    btn.textContent = c;
    btn.onclick = ()=> qzAnswer(i, q, grid.querySelectorAll('button'));
    grid.appendChild(btn);
  });
  scheduleResize(40);
}

function qzAnswer(idx, q, btns){
  if(QZ.answered) return;
  QZ.answered = true;
  const ok = idx === q.answer;
  if(ok) QZ.score++;

  btns.forEach((b,i)=>{
    if(i===q.answer) b.classList.add('correct');
    else if(i===idx && !ok) b.classList.add('wrong');
    else b.disabled = true;
  });

  const fb = document.getElementById('qzFb');
  fb.innerHTML = (ok?'✅ <strong>정답!</strong> ':'❌ <strong>오답.</strong> ') + q.hint;
  fb.className = 'fb-box show '+(ok?'fb-ok':'fb-ng');

  const dot = document.getElementById('qd'+QZ.idx);
  if(dot){ dot.classList.add(ok?'ok':'fail'); dot.textContent=ok?'✓':'✗'; }

  document.getElementById('qzNext').style.display = 'inline-block';
  scheduleResize(50);
}

function qzNextQ(){
  QZ.idx++;
  if(QZ.idx >= QZ.data.length){ qzShowFinal(); return; }
  loadQz();
}

function qzShowFinal(){
  document.getElementById('qzSection').style.display='none';
  document.getElementById('qzFinal').style.display='block';
  const total = QZ.data.length;
  document.getElementById('qzFill').style.width='100%';
  document.getElementById('qzLabel').textContent=`${total}/${total}`;
  document.getElementById('qzScore').textContent = `${QZ.score} / ${total}`;
  const msgs = [
    '다시 도전해봐요! 바빌로니아인도 연습이 필요했을 거예요 💪',
    '조금 더 연습하면 바빌로니아 수학자가 될 수 있어요! 📖',
    '점점 익숙해지고 있어요! 잘 하고 있습니다 👍',
    '훌륭해요! 바빌로니아 방법이 몸에 익었네요 ⭐',
    '완벽! 4000년 전 수학자들의 지혜를 완전히 이해했어요 🏺'
  ];
  document.getElementById('qzMsg').textContent = msgs[Math.min(Math.floor(QZ.score/(total/4)), 4)];
  scheduleResize(60);
}

function qzReset(){ qzInit(); scheduleResize(50); }

// Init
qzInit();

</script>
</body>
</html>"""


def render():
    components.html(_HTML, height=1150, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
