# activities/common/mini/cubic_quartic_equation_explorer.py
"""
삼·사차방정식 풀이 전략 탐구 미니활동
① 풀이법 분류 게임 – 인수분해 공식 vs 인수정리+조립제법
② 대수학의 기본정리 – 복소수 범위에서 n차방정식은 정확히 n개의 근
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "삼차사차방정식탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "분류기준",
        "label":  "삼·사차방정식을 풀 때 '인수분해 공식'을 쓸지 '인수정리+조립제법'을 쓸지 어떻게 판단하나요? 자신만의 판단 기준을 서술하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "기본정리발견",
        "label":  "대수학의 기본정리 탐구에서 계수를 여러 가지로 바꿔보며 발견한 것을 써 보세요. (예: 실수 계수 방정식에서 허근이 나타날 때의 규칙 등)",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "켤레근연결",
        "label":  "삼차방정식의 근이 '실근 1개 + 허근 2개'로 나타날 때, 두 허근은 어떤 관계인가요? 켤레근 성질과 연결하여 설명하세요.",
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
    "title":       "🔢 삼·사차방정식 풀이 탐구",
    "description": "풀이 전략 분류 게임과 대수학의 기본정리 탐구 두 가지 활동으로 삼·사차방정식을 깊이 이해합니다.",
    "order":       251,
    "hidden":      False,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>삼·사차방정식 풀이 탐구</title>
<style>
html { font-size: 17px; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', system-ui, sans-serif;
  background: linear-gradient(155deg, #030b1a 0%, #0a1832 55%, #040d1c 100%);
  color: #e2e8ff;
  padding: 14px 12px 28px;
}

/* ── Tabs ── */
.tabs { display: flex; gap: 6px; margin-bottom: 16px; }
.tab {
  flex: 1; padding: 10px 6px; border: none; border-radius: 12px;
  background: rgba(255,255,255,0.06); color: #94a3b8;
  font-size: 0.82rem; font-weight: 700; cursor: pointer;
  transition: 0.2s; font-family: inherit; line-height: 1.45;
}
.tab.active { background: linear-gradient(135deg, #1d4ed8, #0e7490); color: #fff; }
.tab:hover:not(.active) { background: rgba(255,255,255,0.11); color: #c4b5fd; }

/* ── Screens ── */
.screen { display: none; animation: fadeIn 0.3s ease; }
.screen.active { display: block; }
@keyframes fadeIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:none; } }

/* ── Hero ── */
.hero {
  background: linear-gradient(135deg, rgba(29,78,216,0.2), rgba(14,116,144,0.12));
  border: 1px solid rgba(96,165,250,0.3); border-radius: 14px;
  padding: 14px 18px; margin-bottom: 14px; text-align: center;
}
.hero h2 { font-size: 1.35rem; color: #93c5fd; margin-bottom: 5px; }
.hero p  { font-size: 0.95rem; color: #94a3b8; line-height: 1.65; }

/* ── Card ── */
.card {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 14px; padding: 14px 16px; margin-bottom: 12px;
}
.card-title {
  font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em;
  text-transform: uppercase; color: #60a5fa; margin-bottom: 10px;
}

/* ── Math display ── */
.eq-box {
  font-family: 'Times New Roman', Georgia, serif; font-style: italic;
  font-size: 1.55rem; color: #fde68a; text-align: center;
  background: rgba(253,230,138,0.07); border: 1px solid rgba(253,230,138,0.18);
  border-radius: 10px; padding: 16px 12px; margin: 10px 0;
  line-height: 1.6; letter-spacing: 0.02em;
}
.math { font-family: 'Times New Roman', Georgia, serif; font-style: italic; color: #fde68a; }

/* ── Buttons ── */
.btn {
  padding: 9px 20px; border-radius: 10px; border: none; cursor: pointer;
  font-size: 0.92rem; font-weight: 700; transition: 0.18s; font-family: inherit;
}
.btn-blue  { background: linear-gradient(135deg, #1d4ed8, #0e7490); color: #fff; }
.btn-blue:hover  { opacity: 0.88; transform: translateY(-1px); }
.btn-ghost { background: transparent; border: 1px solid rgba(255,255,255,0.2); color: #e2e8ff; }
.btn-ghost:hover { background: rgba(255,255,255,0.07); }

/* ── Classification buttons ── */
.classify-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0; }
.cls-btn {
  padding: 14px 10px; border-radius: 12px; border: 2px solid; cursor: pointer;
  font-size: 0.88rem; font-weight: 700; transition: 0.18s; font-family: inherit;
  line-height: 1.5; text-align: center;
}
.cls-formula {
  background: rgba(52,211,153,0.08); border-color: rgba(52,211,153,0.35); color: #6ee7b7;
}
.cls-formula:hover { background: rgba(52,211,153,0.2); border-color: #34d399; }
.cls-synthetic {
  background: rgba(167,139,250,0.08); border-color: rgba(167,139,250,0.35); color: #c4b5fd;
}
.cls-synthetic:hover { background: rgba(167,139,250,0.2); border-color: #a78bfa; }
.cls-btn.locked { cursor: default; pointer-events: none; }
.cls-btn.correct { animation: flashGreen 0.4s ease; }
.cls-btn.wrong   { animation: flashRed 0.4s ease; }
@keyframes flashGreen {
  0%,100% {} 50% { background: rgba(52,211,153,0.45); border-color: #34d399; }
}
@keyframes flashRed {
  0%,100% {} 50% { background: rgba(248,113,113,0.4); border-color: #f87171; }
}

/* ── Feedback box ── */
.fb-box {
  border-radius: 10px; padding: 12px 14px; font-size: 0.9rem; line-height: 1.75;
  display: none; animation: fadeIn 0.3s ease;
}
.fb-box.show { display: block; }
.fb-ok  { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); color: #6ee7b7; }
.fb-ng  { background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3); color: #fca5a5; }

/* ── Progress bar ── */
.progress-wrap { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; }
.progress-track {
  flex: 1; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden;
}
.progress-fill { height: 100%; background: linear-gradient(90deg,#1d4ed8,#0e7490); border-radius: 3px; transition: width 0.4s ease; }
.progress-label { font-size: 0.82rem; color: #64748b; white-space: nowrap; }

/* ── Score dots ── */
.score-dots { display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 8px; }
.s-dot {
  width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; font-weight: 700; background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.1); color: #64748b; transition: 0.3s;
}
.s-dot.ok   { background: rgba(52,211,153,0.25); border-color: rgba(52,211,153,0.5); color: #34d399; }
.s-dot.fail { background: rgba(248,113,113,0.2); border-color: rgba(248,113,113,0.4); color: #f87171; }

/* ── Final result ── */
.final-box { text-align: center; padding: 20px 10px; }
.big-score { font-size: 3rem; font-weight: 900; color: #60a5fa; line-height: 1.2; margin: 8px 0; }
.grade-txt  { font-size: 1rem; color: #94a3b8; margin-bottom: 14px; }

/* ── Coefficient input row ── */
.coeff-section { margin-bottom: 14px; }
.coeff-eq-row {
  display: flex; align-items: center; flex-wrap: wrap; gap: 6px;
  margin-bottom: 12px; background: rgba(255,255,255,0.03);
  border-radius: 10px; padding: 10px 12px;
}
.coeff-term { display: flex; align-items: center; gap: 4px; }
.coeff-term-label {
  font-family: 'Times New Roman', Georgia, serif; font-style: italic;
  color: #94a3b8; font-size: 1.1rem; white-space: nowrap;
}
.coeff-ctrl { display: flex; align-items: center; gap: 0; }
.coeff-btn {
  width: 26px; height: 30px; border: 1px solid rgba(255,255,255,0.15);
  background: rgba(255,255,255,0.07); color: #e2e8ff; cursor: pointer;
  font-size: 1rem; font-weight: 700; font-family: inherit; transition: 0.15s;
  display: flex; align-items: center; justify-content: center;
}
.coeff-btn:first-child { border-radius: 6px 0 0 6px; }
.coeff-btn:last-child  { border-radius: 0 6px 6px 0; }
.coeff-btn:hover { background: rgba(96,165,250,0.25); border-color: #60a5fa; }
.coeff-val {
  width: 36px; height: 30px; border: 1px solid rgba(255,255,255,0.15);
  border-left: none; border-right: none;
  background: rgba(255,255,255,0.04); color: #fde68a;
  font-size: 1rem; font-weight: 700; text-align: center; font-family: inherit;
  display: flex; align-items: center; justify-content: center;
}
.op-sign { color: #64748b; font-size: 1.1rem; padding: 0 2px; }

/* ── Degree selector ── */
.deg-toggle { display: flex; gap: 8px; margin-bottom: 16px; }
.deg-btn {
  flex: 1; padding: 10px; border-radius: 10px; border: 2px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.04); color: #94a3b8;
  font-size: 1rem; font-weight: 700; cursor: pointer; font-family: inherit; transition: 0.2s;
}
.deg-btn.active { background: rgba(29,78,216,0.25); border-color: #60a5fa; color: #93c5fd; }
.deg-btn:hover:not(.active) { border-color: rgba(255,255,255,0.25); color: #e2e8ff; }

/* ── Root display ── */
.roots-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px; margin-bottom: 12px;
}
.root-card {
  background: rgba(255,255,255,0.04); border-radius: 10px; padding: 10px 12px;
  border-left: 3px solid; animation: fadeIn 0.4s ease;
}
.root-card.real    { border-color: #34d399; }
.root-card.complex { border-color: #a78bfa; }
.root-num { font-size: 0.72rem; color: #64748b; font-weight: 700; margin-bottom: 3px; }
.root-val { font-family: 'Times New Roman', Georgia, serif; font-style: italic; font-size: 1.15rem; }
.root-val.real    { color: #6ee7b7; }
.root-val.complex { color: #c4b5fd; }
.root-type {
  display: inline-block; font-size: 0.72rem; font-weight: 700; padding: 1px 7px;
  border-radius: 99px; margin-top: 4px;
}
.root-type.real    { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.root-type.complex { background: rgba(167,139,250,0.15); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); }

/* ── Theorem badge ── */
.theorem-badge {
  background: linear-gradient(135deg, rgba(29,78,216,0.2), rgba(14,116,144,0.15));
  border: 1px solid rgba(96,165,250,0.4); border-radius: 12px;
  padding: 14px 16px; text-align: center; margin-top: 10px;
  animation: fadeIn 0.5s ease;
}
.theorem-badge .big { font-size: 1.4rem; font-weight: 900; color: #93c5fd; margin: 4px 0; }
.theorem-badge .sub { font-size: 0.9rem; color: #64748b; }

/* ── Canvas ── */
.canvas-wrap { display: flex; justify-content: center; margin-bottom: 10px; }
canvas { border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); max-width: 100%; }

/* ── Nav row ── */
.nav-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.07);
}
</style>
</head>
<body>

<!-- ── TABS ── -->
<div class="tabs">
  <button class="tab active" onclick="switchTab(0)" id="tab0">🃏 활동 1<br>풀이 전략 분류</button>
  <button class="tab" onclick="switchTab(1)" id="tab1">🔮 활동 2<br>대수학의 기본정리</button>
</div>

<!-- ══════════════════════════════════════════════════
     SCREEN 0 ─ 풀이 전략 분류 게임
══════════════════════════════════════════════════ -->
<div class="screen active" id="screen0">

  <div class="hero">
    <h2>🃏 삼·사차방정식 풀이 전략 분류 게임</h2>
    <p>아래 방정식을 보고, 어떤 방법으로 풀지 선택하세요!<br>
    <strong style="color:#34d399;">인수분해 공식</strong> 이용 &nbsp;|&nbsp;
    <strong style="color:#c4b5fd;">인수정리 + 조립제법</strong> 이용</p>
  </div>

  <!-- 진행 표시 -->
  <div class="progress-wrap">
    <div class="progress-track"><div class="progress-fill" id="pFill" style="width:0%"></div></div>
    <span class="progress-label" id="pLabel">0 / 12</span>
    <div class="score-dots" id="scoreDots"></div>
  </div>

  <!-- 퀴즈 카드 -->
  <div id="quizSection">
    <div class="card">
      <div class="card-title" id="qType">방정식 유형</div>
      <div class="eq-box" id="qEq">—</div>
      <p style="font-size:0.88rem;color:#64748b;text-align:center;margin-bottom:4px;">이 방정식의 풀이 방법은?</p>
      <div class="classify-row">
        <button class="cls-btn cls-formula" id="btnFormula" onclick="classify('formula')">
          ✅ 인수분해 공식<br>
          <span style="font-size:0.78rem;font-weight:400;color:#94a3b8;">합·차 공식 / 치환 이용</span>
        </button>
        <button class="cls-btn cls-synthetic" id="btnSynthetic" onclick="classify('synthetic')">
          🔢 인수정리 + 조립제법<br>
          <span style="font-size:0.78rem;font-weight:400;color:#94a3b8;">유리근 찾고 나눗셈</span>
        </button>
      </div>
      <div class="fb-box" id="qFb"></div>
      <div style="text-align:right;margin-top:10px;">
        <button class="btn btn-blue" id="btnNext" onclick="nextQ()" style="display:none">다음 문제 →</button>
      </div>
    </div>
  </div>

  <!-- 최종 결과 -->
  <div id="finalSection" style="display:none">
    <div class="card final-box">
      <div style="font-size:1.8rem;margin-bottom:4px;">🏆 게임 완료!</div>
      <div class="big-score" id="finalScore">—</div>
      <div class="grade-txt" id="finalMsg">—</div>
      <button class="btn btn-blue" onclick="resetGame()">다시 도전 🔄</button>
    </div>
    <!-- 복습 카드 -->
    <div class="card">
      <div class="card-title">📌 핵심 정리</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
        <div style="background:rgba(52,211,153,0.07);border:1px solid rgba(52,211,153,0.25);border-radius:10px;padding:12px;">
          <div style="color:#34d399;font-weight:700;margin-bottom:6px;font-size:0.9rem;">인수분해 공식 이용</div>
          <ul style="font-size:0.83rem;color:#94a3b8;line-height:1.9;padding-left:16px;">
            <li><em style="font-family:serif">a³ ± b³</em> 형태</li>
            <li>완전세제곱 패턴</li>
            <li><em style="font-family:serif">t = x²</em> 치환 가능한 형태</li>
          </ul>
        </div>
        <div style="background:rgba(167,139,250,0.07);border:1px solid rgba(167,139,250,0.25);border-radius:10px;padding:12px;">
          <div style="color:#c4b5fd;font-weight:700;margin-bottom:6px;font-size:0.9rem;">인수정리 + 조립제법</div>
          <ul style="font-size:0.83rem;color:#94a3b8;line-height:1.9;padding-left:16px;">
            <li>공식이 바로 보이지 않을 때</li>
            <li>상수항의 약수로 근 후보 탐색</li>
            <li>조립제법으로 인수 분리</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

</div>

<!-- ══════════════════════════════════════════════════
     SCREEN 1 ─ 대수학의 기본정리 탐구
══════════════════════════════════════════════════ -->
<div class="screen" id="screen1">

  <div class="hero">
    <h2>🔮 대수학의 기본정리 탐구</h2>
    <p>계수를 직접 조작해 방정식의 모든 근을 확인하세요.<br>
    복소수 범위에서 <strong style="color:#93c5fd;">n차방정식은 정확히 n개의 근</strong>을 가집니다!</p>
  </div>

  <!-- 차수 선택 -->
  <div class="card">
    <div class="card-title">① 방정식 차수 선택</div>
    <div class="deg-toggle">
      <button class="deg-btn active" id="deg3" onclick="setDegree(3)">3차방정식<br><span style="font-size:0.78rem;font-weight:400;color:#94a3b8;">ax³+bx²+cx+d=0</span></button>
      <button class="deg-btn" id="deg4" onclick="setDegree(4)">4차방정식<br><span style="font-size:0.78rem;font-weight:400;color:#94a3b8;">ax⁴+bx³+cx²+dx+e=0</span></button>
    </div>

    <!-- 계수 입력 -->
    <div class="card-title">② 계수 설정 (정수)</div>
    <div class="coeff-section" id="coeffSection"></div>
    <div id="eqPreview" class="eq-box" style="font-size:1.2rem;margin-bottom:12px;">—</div>

    <button class="btn btn-blue" onclick="solveEq()" style="width:100%;font-size:1rem;padding:12px;">
      🔍 모든 근 구하기
    </button>
  </div>

  <!-- 결과 -->
  <div id="resultSection" style="display:none">
    <div class="card">
      <div class="card-title">③ 근 탐색 결과</div>
      <div id="rootsGrid" class="roots-grid"></div>
      <div id="theoremBadge" class="theorem-badge"></div>
    </div>

    <div class="card">
      <div class="card-title">④ 복소 평면에서 근의 위치</div>
      <p style="font-size:0.83rem;color:#64748b;margin-bottom:8px;">
        가로축: 실수부(Re) &nbsp;|&nbsp; 세로축: 허수부(Im) &nbsp;|&nbsp; 점의 색 = 근 번호
      </p>
      <div class="canvas-wrap">
        <canvas id="complexPlane" width="480" height="380"></canvas>
      </div>
      <div id="planeInfo" style="font-size:0.83rem;color:#64748b;text-align:center;"></div>
    </div>
  </div>

</div>

<!-- ─────────────────────── SCRIPT ─────────────────────── -->
<script>

/* ─── iframe height ─── */
function notifyHeight(){
  const h = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight) + 40;
  window.parent.postMessage({isStreamlitMessage:true,type:'streamlit:setFrameHeight',args:{height:h}},'*');
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
function scheduleResize(d){ setTimeout(()=>{ notifyHeight(); setTimeout(notifyHeight,150); }, d||0); }
new ResizeObserver(()=>scheduleResize(0)).observe(document.body);
window.addEventListener('load',()=>scheduleResize(100));

/* ─── Tab switching ─── */
function switchTab(idx){
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',i===idx));
  document.querySelectorAll('.screen').forEach((s,i)=>s.classList.toggle('active',i===idx));
  scheduleResize(50);
}

/* ════════════════════════════════════════════════════════
   TAB 1 — 풀이 전략 분류 게임
════════════════════════════════════════════════════════ */
const EQ_DATA = [
  /* 인수분해 공식 */
  { eq: 'x³ − 8 = 0',          type:'formula',
    hint:'<b>8 = 2³</b> → a³−b³ 공식!<br>(x−2)(x²+2x+4) = 0<br>∴ x = 2, <span style="color:#c4b5fd">x = −1±√3 i</span>' },
  { eq: 'x³ − 64 = 0',         type:'formula',
    hint:'<b>64 = 4³</b> → a³−b³ 공식!<br>(x−4)(x²+4x+16) = 0<br>∴ x = 4, <span style="color:#c4b5fd">x = −2±2√3 i</span>' },
  { eq: 'x³ + 27 = 0',         type:'formula',
    hint:'<b>27 = 3³</b> → a³+b³ 공식!<br>(x+3)(x²−3x+9) = 0<br>∴ x = −3, <span style="color:#c4b5fd">x = 3±3√3 i / 2</span>' },
  { eq: 'x³ + 3x² + 3x + 1 = 0', type:'formula',
    hint:'계수 1·3·3·1 → <b>완전세제곱!</b><br>(x+1)³ = 0<br>∴ x = −1 (삼중근)' },
  { eq: 'x⁴ − 2x² − 8 = 0',   type:'formula',
    hint:'<b>t = x²</b>으로 치환 → t²−2t−8=0<br>(t−4)(t+2)=0 → (x²−4)(x²+2)=0<br>∴ x = ±2, <span style="color:#c4b5fd">x = ±√2 i</span>' },
  { eq: 'x⁴ + x² − 6 = 0',    type:'formula',
    hint:'<b>t = x²</b>으로 치환 → t²+t−6=0<br>(t+3)(t−2)=0 → (x²+3)(x²−2)=0<br>∴ x = ±√2, <span style="color:#c4b5fd">x = ±√3 i</span>' },
  /* 인수정리 + 조립제법 */
  { eq: 'x³ − 3x² + 4x − 2 = 0', type:'synthetic',
    hint:'f(1) = 1−3+4−2 = <b>0</b> → x=1이 근!<br>조립제법: (x−1)(x²−2x+2)=0<br>∴ x = 1, <span style="color:#c4b5fd">x = 1±i</span>' },
  { eq: 'x³ + x² − 3x − 6 = 0',  type:'synthetic',
    hint:'f(2) = 8+4−6−6 = <b>0</b> → x=2가 근!<br>조립제법: (x−2)(x²+3x+3)=0<br>∴ x = 2, <span style="color:#c4b5fd">x = (−3±√3 i)/2</span>' },
  { eq: 'x³ + 2x² − 5x − 6 = 0', type:'synthetic',
    hint:'f(−1) = −1+2+5−6 = <b>0</b> → x=−1이 근!<br>조립제법: (x+1)(x²+x−6)=(x+1)(x+3)(x−2)=0<br>∴ x = −1, −3, 2' },
  { eq: 'x³ − x² − x − 2 = 0',   type:'synthetic',
    hint:'f(2) = 8−4−2−2 = <b>0</b> → x=2가 근!<br>조립제법: (x−2)(x²+x+1)=0<br>∴ x = 2, <span style="color:#c4b5fd">x = (−1±√3 i)/2</span>' },
  { eq: 'x⁴ + 5x³ + 5x² − 5x − 6 = 0', type:'synthetic',
    hint:'f(1)=0 → x=1이 근! 조립제법 후<br>f₁(−6)=0 → x=−6도 근!<br>∴ x = 1, −6, −1±i (4개의 근)' },
  { eq: 'x⁴ − x³ − 7x² + x + 6 = 0',   type:'synthetic',
    hint:'f(1)=0, f(2)=0 두 근 발견!<br>조립제법 반복: (x−1)(x−2)(x+1)(x+3)=0<br>∴ x = 1, 2, −1, −3 (모두 실근)' },
];

// Shuffle
function shuffle(arr){ return arr.sort(()=>Math.random()-0.5); }

let G = { data:[], idx:0, score:0, answered:false };

function initGame(){
  G.data = shuffle([...EQ_DATA]);
  G.idx = 0; G.score = 0; G.answered = false;
  buildDots();
  loadQ();
  document.getElementById('quizSection').style.display='block';
  document.getElementById('finalSection').style.display='none';
}

function buildDots(){
  const el = document.getElementById('scoreDots');
  el.innerHTML = G.data.map((_,i)=>`<div class="s-dot" id="sd${i}">${i+1}</div>`).join('');
}

function loadQ(){
  const q = G.data[G.idx];
  const total = G.data.length;
  document.getElementById('pFill').style.width = (G.idx/total*100)+'%';
  document.getElementById('pLabel').textContent = `${G.idx} / ${total}`;
  document.getElementById('qType').textContent = `문제 ${G.idx+1}`;
  document.getElementById('qEq').textContent = q.eq;
  document.getElementById('qFb').className = 'fb-box';
  document.getElementById('qFb').innerHTML = '';
  document.getElementById('btnNext').style.display = 'none';
  document.getElementById('btnFormula').classList.remove('locked','correct','wrong');
  document.getElementById('btnSynthetic').classList.remove('locked','correct','wrong');
  G.answered = false;
  scheduleResize(30);
}

function classify(choice){
  if(G.answered) return;
  G.answered = true;
  const q = G.data[G.idx];
  const correct = q.type === choice;
  if(correct) G.score++;

  const fbEl = document.getElementById('qFb');
  document.getElementById('btnFormula').classList.add('locked');
  document.getElementById('btnSynthetic').classList.add('locked');

  const chosenBtn = choice==='formula'?document.getElementById('btnFormula'):document.getElementById('btnSynthetic');
  chosenBtn.classList.add(correct?'correct':'wrong');

  fbEl.innerHTML = (correct
    ? '<span style="color:#34d399;font-weight:700">✅ 정답!</span> '
    : '<span style="color:#f87171;font-weight:700">❌ 오답!</span> 정답: ' +
      (q.type==='formula'
        ? '<strong style="color:#34d399">인수분해 공식</strong><br>'
        : '<strong style="color:#c4b5fd">인수정리 + 조립제법</strong><br>')
  ) + q.hint;
  fbEl.className = 'fb-box show ' + (correct?'fb-ok':'fb-ng');

  const dot = document.getElementById('sd'+G.idx);
  if(dot){ dot.classList.add(correct?'ok':'fail'); dot.textContent=correct?'✓':'✗'; }

  document.getElementById('btnNext').style.display = 'inline-block';
  scheduleResize(50);
}

function nextQ(){
  G.idx++;
  if(G.idx >= G.data.length){ showFinal(); return; }
  loadQ();
}

function showFinal(){
  document.getElementById('quizSection').style.display='none';
  document.getElementById('finalSection').style.display='block';
  const total = G.data.length;
  document.getElementById('pFill').style.width='100%';
  document.getElementById('pLabel').textContent=`${total} / ${total}`;
  document.getElementById('finalScore').textContent = `${G.score} / ${total}`;
  const msgs = [
    '다시 한번 도전해봐요! 💪',
    '조금 더 연습하면 잘 할 수 있어요! 📖',
    '점점 잘 되고 있어요! 👍',
    '훌륭해요! 풀이 전략이 잡히고 있어요 ⭐',
    '완벽에 가까워요! 아주 잘 했어요 🌟',
    '완벽 정복! 방정식 전문가 🏆'
  ];
  const idx = Math.min(Math.floor(G.score/(total/5)), msgs.length-1);
  document.getElementById('finalMsg').textContent = msgs[idx];
  scheduleResize(60);
}

function resetGame(){ initGame(); scheduleResize(50); }

initGame();


/* ════════════════════════════════════════════════════════
   TAB 2 — 대수학의 기본정리
════════════════════════════════════════════════════════ */

let T2 = { degree: 3, coeffs: [1,-3,4,-2] };

const TERM_LABELS3 = ['x³', 'x²', 'x', ''];
const TERM_LABELS4 = ['x⁴', 'x³', 'x²', 'x', ''];
const DEFAULT3 = [1, -3, 4, -2];
const DEFAULT4 = [1, -2, -3, 4, 4];
const ROOT_COLORS = ['#f87171','#34d399','#60a5fa','#fbbf24'];

function setDegree(d){
  T2.degree = d;
  T2.coeffs = d===3 ? [...DEFAULT3] : [...DEFAULT4];
  document.getElementById('deg3').classList.toggle('active', d===3);
  document.getElementById('deg4').classList.toggle('active', d===4);
  buildCoeffRow();
  document.getElementById('resultSection').style.display='none';
  scheduleResize(30);
}

function buildCoeffRow(){
  const labels = T2.degree===3 ? TERM_LABELS3 : TERM_LABELS4;
  const n = T2.coeffs.length;
  let html = '<div class="coeff-eq-row">';
  for(let i=0;i<n;i++){
    if(i>0) html += `<span class="op-sign" id="opSign${i}">+</span>`;
    html += `<div class="coeff-term">
      <div class="coeff-ctrl">
        <button class="coeff-btn" onclick="adjCoeff(${i},-1)">−</button>
        <div class="coeff-val" id="cv${i}">${T2.coeffs[i]}</div>
        <button class="coeff-btn" onclick="adjCoeff(${i},+1)">+</button>
      </div>
      <span class="coeff-term-label">${labels[i]}</span>
    </div>`;
  }
  html += '<span style="font-size:1.1rem;color:#94a3b8;padding:0 4px"> = 0</span></div>';
  document.getElementById('coeffSection').innerHTML = html;
  updatePreview();
}

function adjCoeff(i, delta){
  let v = T2.coeffs[i] + delta;
  // Leading coefficient must not be 0
  if(i===0 && v===0) v = delta>0?1:-1;
  // Clamp to ±9
  v = Math.max(-9, Math.min(9, v));
  T2.coeffs[i] = v;
  document.getElementById('cv'+i).textContent = v;
  updatePreview();
}

function updatePreview(){
  const n = T2.coeffs.length;
  const labels = T2.degree===3 ? TERM_LABELS3 : TERM_LABELS4;
  let s = '';
  for(let i=0;i<n;i++){
    const c = T2.coeffs[i];
    if(c===0 && i>0 && i<n-1){ // hide zero middle terms
      if(i>0) document.getElementById('opSign'+i) && (document.getElementById('opSign'+i).style.display='none');
      document.getElementById('cv'+i).style.color='#475569';
      continue;
    }
    if(i>0 && document.getElementById('opSign'+i)){
      document.getElementById('opSign'+i).style.display='';
      document.getElementById('opSign'+i).textContent = c>=0?'+':'−';
    }
    document.getElementById('cv'+i).style.color='#fde68a';
    const absC = Math.abs(c);
    const lbl = labels[i];
    if(i===0){
      s += (c===-1&&lbl?'−':c===1&&lbl?'':c<0?('−'+absC):c+'');
    } else {
      const sgn = c>0?' + ':' − ';
      s += (absC===1&&lbl ? sgn : sgn+absC);
    }
    s += lbl;
    if(i<n-1) s += ' ';
  }
  document.getElementById('eqPreview').textContent = s.trim() + ' = 0';
}

/* ─── Durand-Kerner method ─── */
function durandKerner(coeffs){
  const n = coeffs.length-1;
  if(n===0) return [];
  if(n===1) return [{r:-coeffs[1]/coeffs[0],i:0}];
  const a = coeffs[0];
  const p = coeffs.map(c=>c/a);

  function evPoly(z){
    let re=p[0],im=0;
    for(let k=1;k<=n;k++){
      const nr=re*z.r-im*z.i+p[k];
      const ni=re*z.i+im*z.r;
      re=nr; im=ni;
    }
    return {r:re,i:im};
  }

  // Init: powers of w=0.4+0.9i
  const WR=0.4,WI=0.9;
  let roots=[]; let wr=1,wi=0;
  for(let k=0;k<n;k++){
    roots.push({r:wr,i:wi});
    const nr=wr*WR-wi*WI, ni=wr*WI+wi*WR;
    wr=nr; wi=ni;
  }

  for(let iter=0;iter<600;iter++){
    let maxD=0;
    for(let i=0;i<n;i++){
      const fz=evPoly(roots[i]);
      let dr=1,di=0;
      for(let j=0;j<n;j++){
        if(j===i) continue;
        const qr=roots[i].r-roots[j].r, qi=roots[i].i-roots[j].i;
        const nr=dr*qr-di*qi, ni=dr*qi+di*qr;
        dr=nr; di=ni;
      }
      const d2=dr*dr+di*di;
      if(d2<1e-300) continue;
      const delR=(fz.r*dr+fz.i*di)/d2;
      const delI=(fz.i*dr-fz.r*di)/d2;
      roots[i].r-=delR; roots[i].i-=delI;
      maxD=Math.max(maxD,Math.sqrt(delR*delR+delI*delI));
    }
    if(maxD<1e-13) break;
  }
  return roots;
}

function fmtRoot(z){
  const EPS=5e-7;
  const re = Math.abs(z.r)<EPS ? 0 : Math.round(z.r*10000)/10000;
  const im = Math.abs(z.i)<EPS ? 0 : Math.round(z.i*10000)/10000;
  if(im===0) return {str: re.toString(), type:'real'};
  if(re===0){
    const s = im===1?'i' : im===-1?'−i' : (im<0?(im+'i'):(im+'i'));
    return {str: s, type:'complex'};
  }
  const sign = im>0?' + ':' − ';
  const aimStr = Math.abs(im)===1?'i':(Math.abs(im)+'i');
  return {str: re + sign + aimStr, type:'complex'};
}

function solveEq(){
  const roots = durandKerner(T2.coeffs);
  const n = roots.length;

  // Sort: real roots first, then complex by imaginary part descending
  roots.sort((a,b)=>{
    const ia=Math.abs(a.i)<5e-7,ib=Math.abs(b.i)<5e-7;
    if(ia&&!ib) return -1;
    if(!ia&&ib) return 1;
    return b.i-a.i;
  });

  // Roots grid
  let gridHtml='';
  roots.forEach((r,i)=>{
    const {str,type}=fmtRoot(r);
    gridHtml+=`<div class="root-card ${type}">
      <div class="root-num">근 ${i+1}</div>
      <div class="root-val ${type}"><em>x</em> = ${str}</div>
      <span class="root-type ${type}">${type==='real'?'실근':'허근'}</span>
    </div>`;
  });
  document.getElementById('rootsGrid').innerHTML=gridHtml;

  // Theorem badge
  const realCnt  = roots.filter(r=>Math.abs(r.i)<5e-7).length;
  const cmplxCnt = n-realCnt;
  document.getElementById('theoremBadge').innerHTML=`
    <div style="font-size:1.6rem;margin-bottom:4px;">✅</div>
    <div class="big">이 ${n}차방정식은 복소수 범위에서<br>정확히 <em style="font-style:italic;">${n}개</em>의 근을 가집니다!</div>
    <div class="sub" style="margin-top:6px;">실근 ${realCnt}개 &nbsp;+&nbsp; 허근 ${cmplxCnt}개</div>
    <div class="sub" style="margin-top:4px;font-size:0.8rem;">※ 대수학의 기본정리: 복소수 계수 n차방정식은 중복을 포함하여 정확히 n개의 근을 가집니다.</div>
  `;

  document.getElementById('resultSection').style.display='block';
  drawComplexPlane(roots);
  scheduleResize(60);
}

/* ─── Complex plane canvas ─── */
function drawComplexPlane(roots){
  const canvas=document.getElementById('complexPlane');
  const ctx=canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  const PAD=50;

  // Clear
  const g=ctx.createLinearGradient(0,0,W,H);
  g.addColorStop(0,'#040b1a'); g.addColorStop(1,'#080d1e');
  ctx.fillStyle=g; ctx.fillRect(0,0,W,H);

  // Determine scale
  let minR=-3,maxR=3,minI=-3,maxI=3;
  roots.forEach(r=>{
    minR=Math.min(minR,r.r-0.5); maxR=Math.max(maxR,r.r+0.5);
    minI=Math.min(minI,r.i-0.5); maxI=Math.max(maxI,r.i+0.5);
  });
  // Symmetric around 0
  const absR=Math.max(Math.abs(minR),Math.abs(maxR),1.5);
  const absI=Math.max(Math.abs(minI),Math.abs(maxI),1.5);
  const range=Math.max(absR,absI)*1.2;

  const innerW=W-PAD*2, innerH=H-PAD*2;
  const OX=W/2, OY=H/2;
  const scaleX=innerW/(range*2), scaleY=innerH/(range*2);
  const sc=Math.min(scaleX,scaleY);

  function toPx(re,im){ return [OX+re*sc, OY-im*sc]; }

  // Grid
  ctx.strokeStyle='rgba(255,255,255,0.06)'; ctx.lineWidth=0.8;
  const step=range>5?2:range>2?1:0.5;
  for(let v=-range;v<=range;v+=step){
    const [x1]=toPx(v,-range), [x2]=toPx(v,range);
    ctx.beginPath(); ctx.moveTo(x1,toPx(v,-range)[1]); ctx.lineTo(x2,toPx(v,range)[1]); ctx.stroke();
    const [y1]=toPx(-range,v), [y2]=toPx(range,v);
    ctx.beginPath(); ctx.moveTo(toPx(-range,v)[0],toPx(-range,v)[1]); ctx.lineTo(toPx(range,v)[0],toPx(range,v)[1]); ctx.stroke();
  }

  // Axes
  ctx.strokeStyle='rgba(255,255,255,0.35)'; ctx.lineWidth=1.5;
  const [ax1,ay1]=toPx(-range,0), [ax2,ay2]=toPx(range,0);
  ctx.beginPath(); ctx.moveTo(ax1,ay1); ctx.lineTo(ax2,ay2); ctx.stroke();
  const [bx1,by1]=toPx(0,-range), [bx2,by2]=toPx(0,range);
  ctx.beginPath(); ctx.moveTo(bx1,by1); ctx.lineTo(bx2,by2); ctx.stroke();

  // Axis labels
  ctx.fillStyle='rgba(255,255,255,0.45)'; ctx.font='italic 13px Times New Roman';
  ctx.textAlign='left'; ctx.fillText('Re', ax2-18, ay2-8);
  ctx.textAlign='center'; ctx.fillText('Im', bx2, by2+16);

  // Tick labels
  ctx.fillStyle='rgba(255,255,255,0.3)'; ctx.font='10px Malgun Gothic';
  ctx.textAlign='center';
  for(let v=-Math.floor(range);v<=Math.floor(range);v++){
    if(v===0) continue;
    const [px]=toPx(v,0);
    ctx.fillText(v,px,OY+13);
  }
  ctx.textAlign='right';
  for(let v=-Math.floor(range);v<=Math.floor(range);v++){
    if(v===0) continue;
    const [,py]=toPx(0,v);
    ctx.fillText(v,OX-6,py+4);
  }

  // Plot roots
  roots.forEach((r,i)=>{
    const [px,py]=toPx(r.r,r.i);
    const col=ROOT_COLORS[i%ROOT_COLORS.length];
    // Glow
    ctx.shadowColor=col; ctx.shadowBlur=14;
    ctx.fillStyle=col;
    ctx.beginPath(); ctx.arc(px,py,7,0,Math.PI*2); ctx.fill();
    ctx.shadowBlur=0;
    // Ring
    ctx.strokeStyle=col; ctx.lineWidth=1.5; ctx.globalAlpha=0.4;
    ctx.beginPath(); ctx.arc(px,py,12,0,Math.PI*2); ctx.stroke();
    ctx.globalAlpha=1;
    // Label
    ctx.fillStyle=col; ctx.font='bold 11px Malgun Gothic';
    ctx.textAlign='center';
    const off = py<OY ? -16 : 18;
    ctx.fillText('근'+(i+1), px, py+off);
  });

  // Info text
  const EPS=5e-7;
  const realCnt=roots.filter(r=>Math.abs(r.i)<EPS).length;
  document.getElementById('planeInfo').textContent=
    `실근(Re 축 위): ${realCnt}개 | 허근(Re 축 밖): ${roots.length-realCnt}개`;
}

// Init Tab 2
setDegree(3);

</script>
</body>
</html>"""


def render():
    components.html(_HTML, height=2300, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
