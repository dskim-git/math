# activities/common/mini/complex_number_terms.py
"""
복소수의 핵심 용어 탐구 – 복소수 정복! 분류 마스터
3단계 퀴즈(분류 / 실수·허수부분 찾기 / O·X 판별)로
복소수의 기본 용어와 성질을 재미있게 익히는 활동입니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 ─────────────────────────────────────────────────────
_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "복소수용어"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "분류설명",
        "label":  "복소수 3−2i의 실수부분과 허수부분을 쓰고, 이 수가 실수·허수·순허수 중 어디에 해당하는지 이유와 함께 설명하세요.",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "포함관계",
        "label":  "복소수·실수·허수·순허수의 포함 관계를 말이나 그림으로 나타내고 설명해 보세요. (예: 순허수 ⊂ ...)",
        "type":   "text_area",
        "height": 90,
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
    "title":       "🌀 복소수 정복! 용어 마스터",
    "description": "복소수 핵심 용어(실수·허수·순허수, 실수부분·허수부분)를 3단계 퀴즈로 정복하는 활동입니다.",
    "order":       200,
}

# ─────────────────────────────────────────────────────────────────────────────
_GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>복소수 정복</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(160deg,#0f0c29 0%,#2d1b69 55%,#11022e 100%);
  color:#e2e8f0;min-height:820px;padding:14px 12px;
  overflow-x:hidden;
}

/* ── 화면 전환 ── */
.screen{display:none;animation:fadeIn .35s ease}
.screen.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}

/* ── 공통 타이포 ── */
h2{text-align:center;color:#a78bfa;font-size:1.35rem;margin-bottom:5px;letter-spacing:-.01em}
.subtitle{text-align:center;color:#c4b5fd;font-size:.83rem;margin-bottom:16px}

/* ── Phase 뱃지 / 점수 ── */
.top-bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.phase-badge{
  display:inline-block;
  background:rgba(167,139,250,.18);border:1.5px solid #7c3aed;
  border-radius:99px;padding:3px 14px;font-size:.76rem;color:#c4b5fd;font-weight:600;
}
.score-badge{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(245,158,11,.12);border:1.5px solid #f59e0b;
  border-radius:99px;padding:3px 12px;font-size:.8rem;color:#fcd34d;font-weight:700;
}

/* ── 진행 바 ── */
.prog-wrap{display:flex;align-items:center;gap:8px;margin-bottom:12px}
.prog-bar{flex:1;height:8px;background:rgba(255,255,255,.1);border-radius:99px;overflow:hidden}
.prog-fill{height:100%;background:linear-gradient(90deg,#a855f7,#6366f1);border-radius:99px;transition:width .4s ease}
.prog-label{font-size:.74rem;color:#9ca3af;white-space:nowrap;min-width:44px;text-align:right}

/* ── 문제 카드 ── */
.q-card{
  background:rgba(255,255,255,.05);backdrop-filter:blur(8px);
  border:1.5px solid rgba(167,139,250,.28);border-radius:16px;
  padding:18px 16px;margin-bottom:12px;text-align:center;
  box-shadow:0 4px 24px rgba(0,0,0,.5);
}
.q-type-label{font-size:.72rem;color:#9ca3af;margin-bottom:8px;letter-spacing:.05em;text-transform:uppercase}
.complex-expr{
  font-size:2rem;font-weight:800;color:#f5f3ff;
  margin-bottom:8px;line-height:1.4;letter-spacing:.01em;
}
.complex-expr em{color:#c084fc;font-style:italic}
.q-text{font-size:.94rem;color:#d1d5db;line-height:1.6;max-width:460px;margin:0 auto}
.q-text em{color:#c084fc;font-style:italic}

/* ── 분류 버튼 ── */
.btn-row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:12px}
.choice-btn{
  padding:10px 22px;border-radius:12px;border:2px solid transparent;
  font-size:.93rem;font-weight:700;cursor:pointer;transition:all .18s;
  min-width:90px;color:#fff;
}
.choice-btn:hover{transform:translateY(-2px);filter:brightness(1.15)}
.choice-btn:disabled{opacity:.45;cursor:default;transform:none;filter:none}
.choice-btn.correct{border-color:#10b981!important;box-shadow:0 0 0 3px rgba(16,185,129,.35);animation:popIn .35s}
.choice-btn.wrong{border-color:#ef4444!important;box-shadow:0 0 0 3px rgba(239,68,68,.25)}
@keyframes popIn{0%,100%{transform:scale(1)}50%{transform:scale(1.07)}}

.real-btn{background:rgba(16,185,129,.22);border-color:#34d399}
.imag-btn{background:rgba(59,130,246,.22);border-color:#60a5fa}
.pureimag-btn{background:rgba(139,92,246,.22);border-color:#a78bfa}
.o-btn{background:rgba(16,185,129,.22);border-color:#34d399;font-size:1rem;min-width:80px}
.x-btn{background:rgba(239,68,68,.22);border-color:#f87171;font-size:1rem;min-width:80px}

/* ── Phase 2 선택지 ── */
.parts-section{margin-bottom:10px}
.parts-label{
  font-size:.8rem;color:#c4b5fd;font-weight:700;
  margin-bottom:7px;display:block;
}
.parts-label em{color:#c084fc;font-style:italic}
.part-opt-row{display:flex;gap:8px;flex-wrap:wrap}
.part-opt{
  padding:8px 18px;border-radius:10px;
  border:2px solid rgba(167,139,250,.22);
  background:rgba(255,255,255,.04);color:#e2e8f0;
  font-size:.9rem;font-weight:700;cursor:pointer;transition:all .18s;
  min-width:58px;text-align:center;
}
.part-opt em{color:#c084fc;font-style:italic}
.part-opt:hover{border-color:#a78bfa;background:rgba(167,139,250,.18)}
.part-opt.correct{border-color:#34d399!important;background:rgba(16,185,129,.3)!important;color:#6ee7b7!important}
.part-opt.wrong{border-color:#f87171!important;background:rgba(239,68,68,.2)!important;color:#fca5a5!important}
.part-opt:disabled{opacity:.45;cursor:default}

/* ── 피드백 ── */
.feedback{
  border-radius:10px;padding:10px 14px;margin-bottom:10px;
  font-size:.88rem;line-height:1.55;transition:all .25s;
}
.feedback.correct{background:rgba(16,185,129,.14);border:1px solid #34d399;color:#6ee7b7}
.feedback.wrong{background:rgba(239,68,68,.13);border:1px solid #f87171;color:#fca5a5}
.feedback.hidden{visibility:hidden;min-height:42px}
.feedback em{font-style:italic}
.feedback b{font-weight:700}

/* ── 다음 버튼 ── */
.next-btn{
  display:block;margin:4px auto 0;padding:9px 30px;
  background:linear-gradient(135deg,#7c3aed,#4f46e5);
  border:none;border-radius:99px;color:#fff;
  font-size:.92rem;font-weight:700;cursor:pointer;
  transition:.18s;box-shadow:0 4px 14px rgba(124,58,237,.45);
}
.next-btn:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(124,58,237,.55)}
.next-btn:disabled{opacity:.45;cursor:default;transform:none}

/* ── 인트로 박스 ── */
.intro-box{
  background:rgba(255,255,255,.05);border:1.5px solid rgba(167,139,250,.26);
  border-radius:16px;padding:18px 16px;margin-bottom:14px;
}
.intro-row{display:flex;align-items:flex-start;gap:10px;padding:6px 0;font-size:.88rem;line-height:1.55}
.intro-icon{font-size:1.3rem;min-width:32px;text-align:center;padding-top:1px}
.rule-box{
  background:rgba(99,102,241,.1);border-left:3px solid #818cf8;
  border-radius:0 10px 10px 0;padding:10px 14px;margin:8px 0;
  font-size:.86rem;color:#c7d2fe;line-height:1.65;
}
.rule-box em{color:#c084fc;font-style:italic}
.rule-box b{color:#e2e8f0}

/* ── 전환 (Break) 화면 ── */
.break-box{
  background:rgba(255,255,255,.05);border:1.5px solid rgba(167,139,250,.26);
  border-radius:16px;padding:22px 18px;text-align:center;margin-bottom:16px;
}
.break-icon{font-size:3rem;margin-bottom:8px}
.break-title{font-size:1.15rem;font-weight:700;color:#f0abfc;margin-bottom:10px}
.break-desc{font-size:.88rem;color:#c4b5fd;line-height:1.7;text-align:left}
.break-desc b{color:#e2e8f0}
.break-desc em{color:#c084fc;font-style:italic}

/* ── 결과 화면 ── */
.result-wrap{text-align:center}
.result-circle{
  width:130px;height:130px;border-radius:50%;
  border:4px solid #a78bfa;background:rgba(139,92,246,.18);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  margin:12px auto 16px;box-shadow:0 0 40px rgba(139,92,246,.35);
}
.result-emoji{font-size:2.4rem;line-height:1}
.result-score{font-size:1.05rem;font-weight:800;color:#e2e8f0;margin-top:4px}
.result-max{font-size:.74rem;color:#9ca3af}
.result-msg{font-size:.9rem;color:#c4b5fd;line-height:1.7;margin-bottom:16px;padding:0 8px}
.result-bar-wrap{background:rgba(255,255,255,.08);border-radius:99px;height:12px;overflow:hidden;margin:10px 0}
.result-bar-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#a855f7,#6366f1);transition:width 1s ease}

/* ── 벤다이어그램 안내 카드 ── */
.venn-mini{
  display:flex;gap:8px;align-items:center;justify-content:center;
  flex-wrap:wrap;margin:10px 0;
}
.venn-chip{
  border-radius:99px;padding:4px 14px;font-size:.8rem;font-weight:700;border:2px solid;
}
.venn-complex{background:rgba(99,102,241,.2);border-color:#818cf8;color:#c7d2fe}
.venn-real{background:rgba(16,185,129,.2);border-color:#34d399;color:#6ee7b7}
.venn-imag{background:rgba(59,130,246,.2);border-color:#60a5fa;color:#93c5fd}
.venn-pure{background:rgba(139,92,246,.2);border-color:#a78bfa;color:#d8b4fe}
.venn-arrow{color:#6b7280;font-size:1rem}
</style>
</head>
<body>

<!-- ════════════════════════════════════════════════════════
     인트로 화면
════════════════════════════════════════════════════════ -->
<div id="introScreen" class="screen active">
  <h2>🌀 복소수 정복! 용어 마스터</h2>
  <p class="subtitle">3단계 퀴즈로 복소수 핵심 용어를 완전히 정복해 봅시다!</p>

  <div class="intro-box">
    <div class="intro-row">
      <span class="intro-icon">1️⃣</span>
      <div>
        <strong style="color:#f0abfc">Phase 1 · 복소수 분류관</strong> &nbsp;(8문제)<br>
        주어진 수가 <span style="color:#6ee7b7">실수</span>인지, <span style="color:#93c5fd">허수</span>인지, <span style="color:#d8b4fe">순허수</span>인지 분류해요.
      </div>
    </div>
    <div class="intro-row">
      <span class="intro-icon">2️⃣</span>
      <div>
        <strong style="color:#f0abfc">Phase 2 · 성분 해독기</strong> &nbsp;(5문제)<br>
        복소수의 <strong>실수부분 a</strong>와 <strong>허수부분 b</strong>를 찾아요.
      </div>
    </div>
    <div class="intro-row">
      <span class="intro-icon">3️⃣</span>
      <div>
        <strong style="color:#f0abfc">Phase 3 · O/X 판별대</strong> &nbsp;(5문제)<br>
        복소수에 관한 설명이 맞으면 ⭕, 틀리면 ❌!
      </div>
    </div>
  </div>

  <div class="rule-box">
    💡 복소수 <em>a + bi</em> 에서<br>
    &nbsp;&nbsp;• <b>실수부분</b> = <b>a</b>&nbsp;&nbsp;|&nbsp;&nbsp;<b>허수부분</b> = <b>b</b>&nbsp; (⚠️ <em>bi</em>가 아니라 <b>b</b> 입니다!)
    <br>
    &nbsp;&nbsp;• <b style="color:#6ee7b7">b = 0</b> → 실수 &nbsp;|&nbsp; <b style="color:#93c5fd">b ≠ 0</b> → 허수 &nbsp;|&nbsp; <b style="color:#d8b4fe">a = 0, b ≠ 0</b> → 순허수
  </div>

  <br>
  <button class="next-btn" onclick="startPhase1()">▶ 게임 시작!</button>
</div>


<!-- ════════════════════════════════════════════════════════
     게임 화면 (Phase 1 / 2 / 3 공용)
════════════════════════════════════════════════════════ -->
<div id="gameScreen" class="screen">
  <div class="top-bar">
    <div class="phase-badge" id="phaseBadge">Phase 1 · 분류관</div>
    <div class="score-badge">⭐ <span id="scoreDisp">0</span>점</div>
  </div>
  <div class="prog-wrap">
    <div class="prog-bar"><div class="prog-fill" id="progFill" style="width:0%"></div></div>
    <div class="prog-label" id="progLabel">1 / 8</div>
  </div>

  <!-- 문제 카드 -->
  <div class="q-card">
    <div class="q-type-label" id="qTypeLabel">다음 수를 분류하세요</div>
    <div class="complex-expr" id="complexExpr"></div>
    <div class="q-text" id="qText"></div>
  </div>

  <!-- Phase 1 : 분류 버튼 -->
  <div id="classifyArea">
    <div class="btn-row">
      <button class="choice-btn real-btn"     id="realBtn"  onclick="answerClassify('실수')">실수</button>
      <button class="choice-btn imag-btn"     id="imagBtn"  onclick="answerClassify('허수')">허수</button>
      <button class="choice-btn pureimag-btn" id="pureBtn"  onclick="answerClassify('순허수')">순허수</button>
    </div>
  </div>

  <!-- Phase 2 : 부분 찾기 -->
  <div id="partsArea" style="display:none">
    <div class="parts-section">
      <span class="parts-label">🟢 실수부분 <b>a</b> 는?</span>
      <div class="part-opt-row" id="realOptRow"></div>
    </div>
    <div class="parts-section">
      <span class="parts-label">🟣 허수부분 <b>b</b> 는? &nbsp;<small style="color:#6b7280;font-weight:400">(<em>bi</em> 아닌 b 값)</small></span>
      <div class="part-opt-row" id="imagOptRow"></div>
    </div>
  </div>

  <!-- Phase 3 : O/X -->
  <div id="oxArea" style="display:none">
    <div class="btn-row">
      <button class="choice-btn o-btn" id="oBtn" onclick="answerOX('O')">⭕ O (참)</button>
      <button class="choice-btn x-btn" id="xBtn" onclick="answerOX('X')">❌ X (거짓)</button>
    </div>
  </div>

  <div class="feedback hidden" id="feedbackBox"></div>
  <button class="next-btn" id="nextBtn" onclick="nextQuestion()" style="display:none">다음 ▶</button>
</div>


<!-- ════════════════════════════════════════════════════════
     Phase 전환 (Break) 화면
════════════════════════════════════════════════════════ -->
<div id="breakScreen" class="screen">
  <div class="break-box">
    <div class="break-icon" id="breakIcon">🎯</div>
    <div class="break-title" id="breakTitle">Phase 완료!</div>
    <div class="break-desc" id="breakDesc"></div>
  </div>
  <button class="next-btn" onclick="startNextPhase()">다음 단계로 ▶</button>
</div>


<!-- ════════════════════════════════════════════════════════
     결과 화면
════════════════════════════════════════════════════════ -->
<div id="resultScreen" class="screen">
  <h2>🏆 완주 축하!</h2>

  <div class="result-wrap">
    <div class="result-circle">
      <div class="result-emoji" id="resultEmoji">🌟</div>
      <div class="result-score" id="resultScore">0점</div>
      <div class="result-max" id="resultMax">/ 0점</div>
    </div>
    <div class="result-bar-wrap">
      <div class="result-bar-fill" id="resultBarFill" style="width:0%"></div>
    </div>
    <div class="result-msg" id="resultMsg"></div>
  </div>

  <div class="venn-mini">
    <span class="venn-chip venn-complex">복소수</span>
    <span class="venn-arrow">⊃</span>
    <span class="venn-chip venn-real">실수</span>
    <span style="color:#6b7280;padding:0 2px">+</span>
    <span class="venn-chip venn-imag">허수</span>
    <span class="venn-arrow">⊃</span>
    <span class="venn-chip venn-pure">순허수</span>
  </div>
  <p style="text-align:center;font-size:.78rem;color:#6b7280;margin-bottom:14px">포함 관계: 순허수 ⊂ 허수 ⊂ 복소수 &nbsp;|&nbsp; 실수 ⊂ 복소수</p>

  <button class="next-btn" onclick="restartGame()">🔄 처음부터 다시</button>
</div>


<!-- ════════════════════════════════════════════════════════
     JavaScript
════════════════════════════════════════════════════════ -->
<script>
// ──────────────────────────────────────────────
// 게임 데이터
// ──────────────────────────────────────────────

// Phase 1: 분류 (실수 / 허수 / 순허수)
const P1 = [
  { html:"3",                   type:"실수",   hint:"3 = 3 + 0·<em>i</em> → 허수부분이 0이므로 <b>실수</b>입니다." },
  { html:"2 + √5",              type:"실수",   hint:"√5는 실수이므로 2+√5도 <b>실수</b>입니다. (허수부분 = 0)" },
  { html:"1 − 2<em>i</em>",     type:"허수",   hint:"허수부분 = −2 ≠ 0 → <b>허수</b> (실수가 아닌 복소수)" },
  { html:"4<em>i</em>",         type:"순허수", hint:"실수부분=0, 허수부분=4≠0 → <b>순허수</b>" },
  { html:"−7",                  type:"실수",   hint:"−7 = −7 + 0·<em>i</em> → 허수부분=0 → <b>실수</b>" },
  { html:"√2 + <em>i</em>",     type:"허수",   hint:"허수부분=1≠0 → <b>허수</b>" },
  { html:"−3<em>i</em>",        type:"순허수", hint:"실수부분=0, 허수부분=−3≠0 → <b>순허수</b>" },
  { html:"0",                   type:"실수",   hint:"0 = 0 + 0·<em>i</em> → 허수부분=0 → <b>실수</b> (0도 복소수!)" },
];

// Phase 2: 실수부분·허수부분 찾기
// realOpts/imagOpts: 4개 선택지, realAns/imagAns: 정답 인덱스 (0-based)
const P2 = [
  {
    html:"3 + 4<em>i</em>",
    realOpts:["3","4","7","0"],    realAns:0,
    imagOpts:["4","3","−4","0"],   imagAns:0,
    hint:"3 + 4<em>i</em> → 실수부분=<b>3</b>, 허수부분=<b>4</b>"
  },
  {
    html:"5 − <em>i</em>",
    realOpts:["5","−1","1","6"],   realAns:0,
    imagOpts:["−1","1","5","−5"],  imagAns:0,
    hint:"5 − <em>i</em> = 5 + (−1)<em>i</em> → 실수부분=<b>5</b>, 허수부분=<b>−1</b>"
  },
  {
    html:"−2<em>i</em>",
    realOpts:["0","−2","2","−2"],  realAns:0,
    imagOpts:["−2","0","2","−2<em>i</em>"], imagAns:0,
    hint:"0 + (−2)<em>i</em> → 실수부분=<b>0</b>, 허수부분=<b>−2</b> &nbsp;(순허수!)"
  },
  {
    html:"√3",
    realOpts:["√3","0","3","−√3"], realAns:0,
    imagOpts:["0","√3","1","−1"],  imagAns:0,
    hint:"√3 = √3 + 0<em>i</em> → 실수부분=<b>√3</b>, 허수부분=<b>0</b> &nbsp;(실수!)"
  },
  {
    html:"−1 − 3<em>i</em>",
    realOpts:["−1","−3","1","3"],  realAns:0,
    imagOpts:["−3","−1","3","1"],  imagAns:0,
    hint:"−1 + (−3)<em>i</em> → 실수부분=<b>−1</b>, 허수부분=<b>−3</b>"
  },
];

// Phase 3: O/X 퀴즈
const P3 = [
  {
    text:"복소수 <em>a+bi</em>에서 허수부분은 <em>bi</em>이다.",
    ans:"X",
    hint:"허수부분은 <em>bi</em>가 아니라 <b>b</b>입니다. 실수·허수부분 모두 실수 값이에요!"
  },
  {
    text:"모든 실수는 복소수이다.",
    ans:"O",
    hint:"a = a + 0·<em>i</em> 이므로 모든 실수는 복소수입니다."
  },
  {
    text:"복소수끼리는 크기(대소)를 비교할 수 있다.",
    ans:"X",
    hint:"허수를 포함한 복소수는 대소 비교가 <b>불가능</b>합니다. (실수끼리는 비교 가능)"
  },
  {
    text:"순허수는 허수에 속한다.",
    ans:"O",
    hint:"순허수(a=0, b≠0)는 허수(b≠0)의 특수한 경우로 허수에 속합니다."
  },
  {
    text:"2 + 0<em>i</em>는 허수이다.",
    ans:"X",
    hint:"허수부분 b=0이므로 <b>실수</b>입니다. 2+0<em>i</em> = 2."
  },
];

// ──────────────────────────────────────────────
// 상태 변수
// ──────────────────────────────────────────────
let phase    = 0;
let qIdx     = 0;
let score    = 0;
let answered = false;

// Phase 2 전용
let p2RealDone = false;
let p2ImagDone = false;
let p2ErrCount = 0;

// 점수 최대값
const MAX_SCORE = P1.length * 10 + P2.length * 10 + P3.length * 10;

// ──────────────────────────────────────────────
// 유틸
// ──────────────────────────────────────────────
function shuffle(arr){
  const a = [...arr];
  for(let i = a.length-1; i > 0; i--){
    const j = Math.floor(Math.random() * (i+1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function showScreen(id){
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function updateScore(){
  document.getElementById('scoreDisp').textContent = score;
}

function showFeedback(type, html){
  const fb = document.getElementById('feedbackBox');
  fb.className = 'feedback ' + type;
  fb.innerHTML = html;
}
function hideFeedback(){
  const fb = document.getElementById('feedbackBox');
  fb.className = 'feedback hidden';
  fb.innerHTML = '';
}

// ──────────────────────────────────────────────
// 시작 / 전환
// ──────────────────────────────────────────────
function startPhase1(){
  phase = 1; qIdx = 0; score = 0;
  updateScore();
  showScreen('gameScreen');
  loadQuestion();
}

function startNextPhase(){
  phase++;
  qIdx = 0;
  showScreen('gameScreen');
  loadQuestion();
}

function restartGame(){
  phase = 0; qIdx = 0; score = 0; answered = false;
  updateScore();
  showScreen('introScreen');
}

// ──────────────────────────────────────────────
// 문제 로드
// ──────────────────────────────────────────────
function loadQuestion(){
  answered    = false;
  p2RealDone  = false;
  p2ImagDone  = false;
  p2ErrCount  = 0;

  // 영역 숨기기
  document.getElementById('classifyArea').style.display = 'none';
  document.getElementById('partsArea').style.display    = 'none';
  document.getElementById('oxArea').style.display       = 'none';
  document.getElementById('nextBtn').style.display      = 'none';
  hideFeedback();

  let data, total;

  if(phase === 1){
    data  = P1[qIdx];
    total = P1.length;
    document.getElementById('phaseBadge').textContent  = 'Phase 1 · 분류관';
    document.getElementById('qTypeLabel').textContent  = '다음 수는 실수, 허수, 순허수 중 어느 것인가요?';
    document.getElementById('complexExpr').innerHTML   = data.html;
    document.getElementById('qText').innerHTML         = '';
    document.getElementById('classifyArea').style.display = 'block';
    ['realBtn','imagBtn','pureBtn'].forEach(id=>{
      const b = document.getElementById(id);
      b.disabled = false;
      b.classList.remove('correct','wrong');
    });

  } else if(phase === 2){
    data  = P2[qIdx];
    total = P2.length;
    document.getElementById('phaseBadge').textContent  = 'Phase 2 · 성분 해독기';
    document.getElementById('qTypeLabel').textContent  = '다음 복소수의 실수부분 a와 허수부분 b를 찾으세요.';
    document.getElementById('complexExpr').innerHTML   = data.html;
    document.getElementById('qText').innerHTML         = '';
    document.getElementById('partsArea').style.display = 'block';
    renderPartsOptions(data);

  } else {
    data  = P3[qIdx];
    total = P3.length;
    document.getElementById('phaseBadge').textContent = 'Phase 3 · O/X 판별대';
    document.getElementById('qTypeLabel').textContent = '다음 설명이 맞으면 ⭕ O, 틀리면 ❌ X!';
    document.getElementById('complexExpr').innerHTML  = '';
    document.getElementById('qText').innerHTML        = data.text;
    document.getElementById('oxArea').style.display   = 'block';
    ['oBtn','xBtn'].forEach(id=>{
      const b = document.getElementById(id);
      b.disabled = false;
      b.classList.remove('correct','wrong');
    });
  }

  // 진행 바
  document.getElementById('progFill').style.width   = (qIdx / total * 100) + '%';
  document.getElementById('progLabel').textContent  = (qIdx+1) + ' / ' + total;
}

// ──────────────────────────────────────────────
// Phase 2: 선택지 렌더링 (셔플 포함)
// ──────────────────────────────────────────────
function renderPartsOptions(data){
  // 실수부분 셔플
  const realOrder = shuffle([0,1,2,3]);
  let newRealAns  = realOrder.indexOf(data.realAns);
  // 허수부분 셔플
  const imagOrder = shuffle([0,1,2,3]);
  let newImagAns  = imagOrder.indexOf(data.imagAns);

  const rRow = document.getElementById('realOptRow');
  const iRow = document.getElementById('imagOptRow');
  rRow.innerHTML = '';
  iRow.innerHTML = '';

  realOrder.forEach((origIdx, pos) => {
    const b = document.createElement('button');
    b.className = 'part-opt';
    b.innerHTML = data.realOpts[origIdx];
    rRow.appendChild(b);
  });

  imagOrder.forEach((origIdx, pos) => {
    const b = document.createElement('button');
    b.className = 'part-opt';
    b.innerHTML = data.imagOpts[origIdx];
    iRow.appendChild(b);
  });

  // 이벤트 핸들러 (클로저로 정답 인덱스 전달)
  [...rRow.querySelectorAll('.part-opt')].forEach((b, pos) => {
    b.onclick = () => selectPart('real', pos, newRealAns, data.hint);
  });
  [...iRow.querySelectorAll('.part-opt')].forEach((b, pos) => {
    b.onclick = () => selectPart('imag', pos, newImagAns, data.hint);
  });
}

// ──────────────────────────────────────────────
// Phase 1: 분류 답변
// ──────────────────────────────────────────────
function answerClassify(choice){
  if(answered) return;
  answered = true;
  const data   = P1[qIdx];
  const correct = choice === data.type;

  const map = {'실수':'realBtn','허수':'imagBtn','순허수':'pureBtn'};
  ['실수','허수','순허수'].forEach(t => document.getElementById(map[t]).disabled = true);

  document.getElementById(map[choice]).classList.add(correct ? 'correct' : 'wrong');
  if(!correct) document.getElementById(map[data.type]).classList.add('correct');

  if(correct){ score += 10; updateScore(); }

  showFeedback(
    correct ? 'correct' : 'wrong',
    (correct ? '✅ 정답! ' : '❌ 아쉬워요! ') + data.hint
  );
  document.getElementById('nextBtn').style.display = 'block';
}

// ──────────────────────────────────────────────
// Phase 2: 실수부분·허수부분 선택
// ──────────────────────────────────────────────
function selectPart(part, idx, ansIdx, hint){
  if(part === 'real' && p2RealDone) return;
  if(part === 'imag' && p2ImagDone) return;

  const rowId = part === 'real' ? 'realOptRow' : 'imagOptRow';
  const btns  = [...document.getElementById(rowId).querySelectorAll('.part-opt')];
  btns.forEach(b => b.disabled = true);

  const correct = idx === ansIdx;
  btns[idx].classList.add(correct ? 'correct' : 'wrong');
  if(!correct){
    btns[ansIdx].classList.add('correct');
    p2ErrCount++;
  }
  if(correct) score += 5;
  updateScore();

  if(part === 'real') p2RealDone = true;
  else                p2ImagDone = true;

  if(p2RealDone && p2ImagDone){
    answered = true;
    const allOk = p2ErrCount === 0;
    showFeedback(
      allOk ? 'correct' : 'wrong',
      (allOk ? '✅ 완벽! ' : '💡 확인해볼까요? ') + hint
    );
    document.getElementById('nextBtn').style.display = 'block';
  }
}

// ──────────────────────────────────────────────
// Phase 3: O/X 답변
// ──────────────────────────────────────────────
function answerOX(choice){
  if(answered) return;
  answered = true;
  const data    = P3[qIdx];
  const correct = choice === data.ans;

  const oBtn = document.getElementById('oBtn');
  const xBtn = document.getElementById('xBtn');
  oBtn.disabled = true;
  xBtn.disabled = true;

  const chosen  = choice === 'O' ? oBtn : xBtn;
  const correct_ = data.ans === 'O' ? oBtn : xBtn;
  chosen.classList.add(correct ? 'correct' : 'wrong');
  if(!correct) correct_.classList.add('correct');

  if(correct){ score += 10; updateScore(); }

  showFeedback(
    correct ? 'correct' : 'wrong',
    (correct ? '✅ 정답! ' : '❌ 아쉬워요! ') + data.hint
  );
  document.getElementById('nextBtn').style.display = 'block';
}

// ──────────────────────────────────────────────
// 다음 문제 / Phase 전환
// ──────────────────────────────────────────────
function nextQuestion(){
  qIdx++;
  const maxQ = phase === 1 ? P1.length : phase === 2 ? P2.length : P3.length;

  if(qIdx >= maxQ){
    if(phase === 3){
      showResult();
    } else {
      showBreak();
    }
  } else {
    loadQuestion();
  }
}

function showBreak(){
  const info = [
    {
      icon:'🎯',
      title:'Phase 1 완료!',
      desc:`
        <b>핵심 정리</b><br>
        복소수 <em>a + bi</em> 에서<br>
        &nbsp;• <b>b = 0</b>   → <b style="color:#6ee7b7">실수</b><br>
        &nbsp;• <b>b ≠ 0</b>   → <b style="color:#93c5fd">허수</b> (실수가 아닌 복소수)<br>
        &nbsp;• <b>a = 0, b ≠ 0</b> → <b style="color:#d8b4fe">순허수</b><br><br>
        <b>포함 관계:</b> 순허수 ⊂ 허수 ⊂ 복소수 &nbsp;/&nbsp; 실수 ⊂ 복소수
      `
    },
    {
      icon:'⚗️',
      title:'Phase 2 완료!',
      desc:`
        <b>핵심 정리</b><br>
        <em>a + bi</em> 에서 실수부분=<b>a</b>, 허수부분=<b>b</b><br>
        ⚠️ 허수부분은 <b><em>bi</em>가 아니라 b</b> (실수 값!)입니다.<br><br>
        예) 5 − <em>i</em>&nbsp;&nbsp;→&nbsp;&nbsp;실수부분 = <b>5</b>, 허수부분 = <b>−1</b>
      `
    }
  ][phase - 1];

  document.getElementById('breakIcon').textContent  = info.icon;
  document.getElementById('breakTitle').textContent = info.title;
  document.getElementById('breakDesc').innerHTML    = info.desc;
  showScreen('breakScreen');
}

// ──────────────────────────────────────────────
// 최종 결과
// ──────────────────────────────────────────────
function showResult(){
  const pct = Math.round(score / MAX_SCORE * 100);

  let emoji, msg;
  if(pct >= 90){       emoji='🏆'; msg='완벽해요! 복소수 용어를 완전히 정복했군요! 🌟'; }
  else if(pct >= 70){  emoji='🎉'; msg='훌륭해요! 거의 다 알고 있네요. 틀린 부분을 복습해 봅시다.'; }
  else if(pct >= 50){  emoji='😊'; msg='잘 했어요! 핵심 정리를 다시 한 번 읽고 도전해 봐요.'; }
  else{                emoji='💪'; msg='아직 어렵지요? 위의 rule-box를 참고해서 다시 도전해 봐요!'; }

  document.getElementById('resultEmoji').textContent   = emoji;
  document.getElementById('resultScore').textContent   = score + '점';
  document.getElementById('resultMax').textContent     = '/ ' + MAX_SCORE + '점  (' + pct + '%)';
  document.getElementById('resultMsg').textContent     = msg;

  // 바 애니메이션
  setTimeout(() => {
    document.getElementById('resultBarFill').style.width = pct + '%';
  }, 100);

  showScreen('resultScreen');
}

// 초기화
updateScore();
</script>
</body>
</html>
"""


def render():
    st.markdown("## 🌀 복소수 정복! 용어 마스터")
    st.caption(
        "복소수의 핵심 용어를 3단계 퀴즈로 익혀 봅시다. "
        "게임을 완료한 후 아래 성찰 폼을 작성해 주세요."
    )
    components.html(_GAME_HTML, height=820, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
