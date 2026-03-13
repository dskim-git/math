# activities/probability_new/mini/binomial_theorem_apply.py
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "이항정리활용"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이항정리 활용 성찰 질문**"},
    {"key": "인상깊은공식",
     "label": "⭐ 오늘 배운 8가지 공식 중 가장 인상 깊었던 것과 그 이유를 적어보세요",
     "type": "text_area", "height": 90},
    {"key": "유도원리",
     "label": "🔍 이항정리에서 새 공식을 만드는 원리(대입·미분·적분·곱 분해 등)를 자신의 말로 설명해보세요",
     "type": "text_area", "height": 100},
    {"key": "활용문제",
     "label": "📐 오늘 배운 공식 하나를 활용해서 문제를 직접 만들고 풀어보세요",
     "type": "text_area", "height": 100},
    {"key": "새롭게알게된점",
     "label": "💡 이 활동을 통해 새롭게 알게 된 점",
     "type": "text_area", "height": 80},
    {"key": "느낀점",
     "label": "💬 이 활동을 통해 느낀 점",
     "type": "text_area", "height": 80},
]

META = {
    "title":       "미니: 이항정리의 활용",
    "description": "(1+x)ⁿ 대입·미분·적분으로 이항계수 8가지 성질을 직접 도출하는 탐험·카드·퀴즈 활동",
    "order":       35,
    "hidden":      True,
}

_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="initApp()"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', sans-serif; background: #f8fafc; color: #1e293b; padding: 10px; font-size: 14px; }

.tab-nav { display: flex; gap: 4px; margin-bottom: 14px; border-bottom: 2px solid #e2e8f0; }
.tab-btn { padding: 9px 16px; border: none; background: none; cursor: pointer; font-size: 13px; font-weight: 600; color: #64748b; border-bottom: 3px solid transparent; margin-bottom: -2px; transition: all 0.2s; }
.tab-btn:hover { color: #3b82f6; }
.tab-btn.active { color: #3b82f6; border-bottom-color: #3b82f6; }
.tab-pane { display: none; }
.tab-pane.active { display: block; }

.card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 16px; margin-bottom: 12px; }
.card h3 { font-size: 15px; font-weight: 700; margin-bottom: 6px; }
.card p { font-size: 12px; color: #64748b; margin-bottom: 10px; }

.n-row { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.n-label { font-size: 14px; font-weight: 700; color: #475569; }
.n-btn { width: 34px; height: 34px; border: 2px solid #cbd5e1; border-radius: 8px; background: #fff; cursor: pointer; font-size: 15px; font-weight: 700; color: #475569; transition: all 0.15s; }
.n-btn:hover { border-color: #3b82f6; color: #3b82f6; }
.n-btn.active { border-color: #3b82f6; background: #3b82f6; color: #fff; }

.formula-display { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 10px; padding: 12px 14px; margin-bottom: 12px; min-height: 52px; text-align: center; font-size: 13px; overflow-x: auto; }

.x-btns { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 12px; }
.xb { padding: 8px 13px; border: 2px solid; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 700; transition: all 0.15s; }
.xb-1  { border-color: #22c55e; color: #16a34a; background: #f0fdf4; }
.xb-1:hover,.xb-1.on  { background: #16a34a; color: #fff; }
.xb-m1 { border-color: #ef4444; color: #dc2626; background: #fef2f2; }
.xb-m1:hover,.xb-m1.on { background: #dc2626; color: #fff; }
.xb-d  { border-color: #f59e0b; color: #d97706; background: #fffbeb; }
.xb-d:hover,.xb-d.on  { background: #d97706; color: #fff; }
.xb-i  { border-color: #06b6d4; color: #0891b2; background: #ecfeff; }
.xb-i:hover,.xb-i.on  { background: #0891b2; color: #fff; }
.xb-2  { border-color: #8b5cf6; color: #7c3aed; background: #faf5ff; }
.xb-2:hover,.xb-2.on  { background: #7c3aed; color: #fff; }

.result-box { background: #fafafa; border: 2px solid #e2e8f0; border-radius: 10px; padding: 12px 14px; min-height: 52px; }
.result-box.on { border-color: #3b82f6; background: #eff6ff; }
.res-tag { font-size: 12px; font-weight: 700; margin-bottom: 8px; }
.res-formula { text-align: center; margin: 8px 0; overflow-x: auto; }
.res-note { font-size: 12px; color: #475569; margin-top: 10px; background: #f8fafc; padding: 6px 10px; border-radius: 6px; border-left: 3px solid #94a3b8; }

.sum-table { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 6px; }
.sum-table th { background: #f1f5f9; padding: 8px; border: 1px solid #e2e8f0; text-align: left; font-weight: 600; }
.sum-table td { padding: 8px; border: 1px solid #e2e8f0; vertical-align: middle; }
.sum-table tr:nth-child(even) td { background: #fafafa; }

/* Cards */
.group-hd { font-size: 12px; font-weight: 700; color: #475569; padding: 5px 10px; background: #f1f5f9; border-radius: 6px; border-left: 3px solid #3b82f6; margin: 12px 0 8px 0; }
.cards-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 4px; }
@media (max-width: 540px) { .cards-grid { grid-template-columns: 1fr; } }

.flip-card { perspective: 800px; height: 190px; cursor: pointer; }
.flip-inner { position: relative; width: 100%; height: 100%; transition: transform 0.55s; transform-style: preserve-3d; }
.flip-card.flipped .flip-inner { transform: rotateY(180deg); }
.flip-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; -webkit-backface-visibility: hidden; border-radius: 12px; padding: 12px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; overflow: hidden; }
.flip-front { background: #fff; }
.flip-back  { background: #fffbf0; border-color: #fde68a; transform: rotateY(180deg); }
.fnum { position: absolute; top: 10px; right: 12px; font-size: 20px; font-weight: 800; color: #e2e8f0; }
.fbadge { display: inline-block; padding: 2px 9px; border-radius: 999px; font-size: 11px; font-weight: 700; margin-bottom: 8px; width: fit-content; }
.bs { background: #dcfce7; color: #166534; }
.bc { background: #fff7ed; color: #c2410c; }
.bp { background: #ede9fe; color: #5b21b6; }
.bk { background: #e0f2fe; color: #075985; }
.fform { flex: 1; display: flex; align-items: center; justify-content: center; overflow: hidden; font-size: 11px; padding: 0 4px; }
.fhint { font-size: 10px; color: #94a3b8; text-align: right; margin-top: auto; flex-shrink: 0; }
.btitle { font-size: 12px; font-weight: 700; color: #1e293b; margin-bottom: 6px; flex-shrink: 0; }
.bkey  { font-size: 11px; text-align: center; margin: 4px 0; overflow: hidden; flex: 1; display: flex; align-items: center; justify-content: center; }
.bnote { font-size: 11px; color: #475569; margin-top: auto; background: #fef9c3; padding: 5px 8px; border-radius: 5px; line-height: 1.5; flex-shrink: 0; }

/* Quiz */
.qprog-text { font-size: 12px; color: #64748b; margin-bottom: 4px; }
.qbar-wrap { height: 5px; background: #e2e8f0; border-radius: 999px; margin-bottom: 12px; }
.qbar { height: 100%; background: #3b82f6; border-radius: 999px; transition: width 0.4s; }
.qq { font-size: 14px; font-weight: 600; margin-bottom: 14px; line-height: 1.7; }
.qchoices { display: flex; flex-direction: column; gap: 7px; margin-bottom: 12px; }
.qch { padding: 9px 12px; border: 2px solid #e2e8f0; border-radius: 9px; cursor: pointer; font-size: 12px; background: #fff; text-align: left; transition: all 0.15s; display: block; width: 100%; line-height: 1.5; }
.qch:hover:not([disabled]) { border-color: #93c5fd; background: #eff6ff; }
.qch.ok  { border-color: #22c55e !important; background: #f0fdf4 !important; color: #166534; font-weight: 700; }
.qch.ng  { border-color: #ef4444 !important; background: #fef2f2 !important; color: #991b1b; }
.qch.show-ok { border-color: #22c55e !important; background: #f0fdf4 !important; color: #166534; }
.qfb { display: none; padding: 9px 12px; border-radius: 8px; font-size: 12px; margin-bottom: 10px; line-height: 1.6; }
.qfb.show { display: block; }
.qfb.ok  { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }
.qfb.ng  { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
.qnav { display: flex; justify-content: space-between; align-items: center; }
.qscore { font-size: 12px; font-weight: 700; color: #64748b; }
.qnext { padding: 7px 18px; background: #3b82f6; color: #fff; border: none; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer; display: none; }
.qnext.show { display: inline-block; }
.qresult { text-align: center; padding: 20px; }
.qresult h2 { font-size: 24px; margin-bottom: 6px; }
.qscore-big { font-size: 44px; font-weight: 800; color: #3b82f6; line-height: 1.2; }
.qresult p { color: #64748b; font-size: 13px; margin: 8px 0 16px; }
.qrestart { padding: 9px 22px; background: #3b82f6; color: #fff; border: none; border-radius: 10px; font-size: 13px; font-weight: 700; cursor: pointer; }
</style>
</head>
<body>

<div class="tab-nav">
  <button class="tab-btn active" onclick="swTab('explore',this)">🔢 대입 탐험</button>
  <button class="tab-btn" onclick="swTab('cards',this)">📋 공식 카드</button>
  <button class="tab-btn" onclick="swTab('quiz',this)">🎯 도전 퀴즈</button>
</div>

<!-- ═══ TAB 1: EXPLORE ═══ -->
<div id="pane-explore" class="tab-pane active">

  <div class="card">
    <h3>🧮 이항정리 대입 탐험기</h3>
    <p>n을 고르고 버튼을 눌러 이항정리 <span id="base-formula"></span>에서 어떤 공식이 나오는지 확인하세요!</p>

    <div class="n-row">
      <span class="n-label">n =</span>
      <button class="n-btn" onclick="setN(2,this)">2</button>
      <button class="n-btn active" onclick="setN(3,this)">3</button>
      <button class="n-btn" onclick="setN(4,this)">4</button>
      <button class="n-btn" onclick="setN(5,this)">5</button>
      <button class="n-btn" onclick="setN(6,this)">6</button>
    </div>

    <div class="formula-display" id="gformula"></div>

    <div class="x-btns">
      <button class="xb xb-1"  onclick="doSub('x1',this)">✅ x = 1 대입</button>
      <button class="xb xb-m1" onclick="doSub('xm1',this)">🔴 x = −1 대입</button>
      <button class="xb xb-d"  onclick="doSub('diff',this)">📐 미분 후 x=1</button>
      <button class="xb xb-i"  onclick="doSub('intg',this)">∫ 적분 (0→1)</button>
      <button class="xb xb-2"  onclick="doSub('x2',this)">💜 x = 2 대입 (보너스)</button>
    </div>

    <div class="result-box" id="rbox">
      <p style="color:#94a3b8;font-size:12px;text-align:center;">↑ 위의 버튼을 눌러 대입해 보세요!</p>
    </div>
  </div>

  <div class="card">
    <h3>📌 유도 방법 요약표</h3>
    <table class="sum-table">
      <thead><tr><th style="width:35%">방법</th><th>도출되는 공식</th></tr></thead>
      <tbody>
        <tr><td>x = 1 대입</td>   <td id="st1"></td></tr>
        <tr><td>x = −1 대입</td>  <td id="st2"></td></tr>
        <tr><td>미분 후 x=1</td>   <td id="st3"></td></tr>
        <tr><td>0→1 적분</td>      <td id="st4"></td></tr>
      </tbody>
    </table>
  </div>

</div>

<!-- ═══ TAB 2: CARDS ═══ -->
<div id="pane-cards" class="tab-pane">
  <div class="card" style="padding:10px 14px 8px;">
    <p style="margin-bottom:0;">카드를 <strong>클릭</strong>하면 도출 방법이 나타납니다! 다시 클릭하면 앞면으로 돌아와요 🔄</p>
  </div>

  <div class="group-hd">📌 이항정리에 값 대입하기 — 공식 ①②</div>
  <div class="cards-grid">
    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-inner">
        <div class="flip-face flip-front">
          <div class="fnum">①</div>
          <span class="fbadge bs">x = 1 대입</span>
          <div class="fform" id="cf1f"></div>
          <div class="fhint">클릭 → 유도 방법 ▶</div>
        </div>
        <div class="flip-face flip-back">
          <div class="btitle">✅ (★)에서 x = 1 대입</div>
          <div class="bkey" id="cf1b"></div>
          <div class="bnote">이항계수의 합 = 2ⁿ<br>n개 원소의 모든 부분집합의 수!</div>
        </div>
      </div>
    </div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-inner">
        <div class="flip-face flip-front">
          <div class="fnum">②</div>
          <span class="fbadge bs">x = −1 대입</span>
          <div class="fform" id="cf2f"></div>
          <div class="fhint">클릭 → 유도 방법 ▶</div>
        </div>
        <div class="flip-face flip-back">
          <div class="btitle">🔴 (★)에서 x = −1 대입</div>
          <div class="bkey" id="cf2b"></div>
          <div class="bnote">짝수 번째 합 = 홀수 번째 합<br>교대 부호 합은 항상 0!</div>
        </div>
      </div>
    </div>
  </div>

  <div class="group-hd">📐 미분·적분 활용하기 — 공식 ③④</div>
  <div class="cards-grid">
    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-inner">
        <div class="flip-face flip-front">
          <div class="fnum">③</div>
          <span class="fbadge bc">미분 후 x=1</span>
          <div class="fform" id="cf3f"></div>
          <div class="fhint">클릭 → 유도 방법 ▶</div>
        </div>
        <div class="flip-face flip-back">
          <div class="btitle">📐 (★)의 양변 미분 후 x=1 대입</div>
          <div class="bkey" id="cf3b"></div>
          <div class="bnote">k를 곱한 이항계수의 합 = n·2ⁿ⁻¹</div>
        </div>
      </div>
    </div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-inner">
        <div class="flip-face flip-front">
          <div class="fnum">④</div>
          <span class="fbadge bc">0→1 적분</span>
          <div class="fform" id="cf4f"></div>
          <div class="fhint">클릭 → 유도 방법 ▶</div>
        </div>
        <div class="flip-face flip-back">
          <div class="btitle">∫ (★)의 양변을 0~1 구간 적분</div>
          <div class="bkey" id="cf4b"></div>
          <div class="bnote">분모가 1씩 커지는 이항계수 합<br>= (2ⁿ⁺¹−1)/(n+1)</div>
        </div>
      </div>
    </div>
  </div>

  <div class="group-hd">🔮 (1+x)^(m+n) 곱 분해 — 공식 ⑤⑥ (반데몬드 항등식)</div>
  <div class="cards-grid">
    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-inner">
        <div class="flip-face flip-front">
          <div class="fnum">⑤</div>
          <span class="fbadge bp">반데몬드 항등식</span>
          <div class="fform" id="cf5f"></div>
          <div class="fhint">클릭 → 유도 방법 ▶</div>
        </div>
        <div class="flip-face flip-back">
          <div class="btitle">🔮 양변의 x^r 계수 비교</div>
          <div class="bkey" id="cf5b"></div>
          <div class="bnote">(1+x)^{m+n} = (1+x)^m·(1+x)^n<br>의 x^r 계수를 비교하면 성립!</div>
        </div>
      </div>
    </div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-inner">
        <div class="flip-face flip-front">
          <div class="fnum">⑥</div>
          <span class="fbadge bp">제곱합 공식</span>
          <div class="fform" id="cf6f"></div>
          <div class="fhint">클릭 → 유도 방법 ▶</div>
        </div>
        <div class="flip-face flip-back">
          <div class="btitle">🔮 반데몬드의 특수한 경우</div>
          <div class="bkey" id="cf6b"></div>
          <div class="bnote">⑤에서 m=n, r=n으로 놓고<br>C(n,k)=C(n,n−k)를 이용!</div>
        </div>
      </div>
    </div>
  </div>

  <div class="group-hd">🔺 파스칼 삼각형 성질 — 공식 ⑦⑧</div>
  <div class="cards-grid">
    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-inner">
        <div class="flip-face flip-front">
          <div class="fnum">⑦</div>
          <span class="fbadge bk">파스칼 성질 1</span>
          <div class="fform" id="cf7f"></div>
          <div class="fhint">클릭 → 유도 방법 ▶</div>
        </div>
        <div class="flip-face flip-back">
          <div class="btitle">🔺 파스칼 항등식을 행 방향으로 반복</div>
          <div class="bkey" id="cf7b"></div>
          <div class="bnote">파스칼 삼각형에서 대각선 방향의<br>이항계수를 누적 합산한 결과!</div>
        </div>
      </div>
    </div>
    <div class="flip-card" onclick="this.classList.toggle('flipped')">
      <div class="flip-inner">
        <div class="flip-face flip-front">
          <div class="fnum">⑧</div>
          <span class="fbadge bk">파스칼 성질 2</span>
          <div class="fform" id="cf8f"></div>
          <div class="fhint">클릭 → 유도 방법 ▶</div>
        </div>
        <div class="flip-face flip-back">
          <div class="btitle">🔺 파스칼 항등식을 열 방향으로 반복</div>
          <div class="bkey" id="cf8b"></div>
          <div class="bnote">파스칼 삼각형의 같은 r열을<br>아래로 누적 합산한 결과! (n≥r)</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══ TAB 3: QUIZ ═══ -->
<div id="pane-quiz" class="tab-pane">
  <div class="card" id="quiz-container">
    <div class="qprog-text" id="qprog">문제 1 / 8</div>
    <div class="qbar-wrap"><div class="qbar" id="qbar" style="width:0%"></div></div>
    <div class="qq" id="qq"></div>
    <div class="qchoices" id="qchoices"></div>
    <div class="qfb" id="qfb"></div>
    <div class="qnav">
      <span class="qscore" id="qscore">점수: 0 / 0</span>
      <button class="qnext" id="qnext" onclick="nextQ()">다음 문제 →</button>
    </div>
  </div>
  <div class="card qresult" id="quiz-result" style="display:none;">
    <h2>🎉 퀴즈 완료!</h2>
    <div class="qscore-big" id="qrsc"></div>
    <p id="qrmsg"></p>
    <button class="qrestart" onclick="startQuiz()">다시 도전하기 🔄</button>
  </div>
</div>

<script>
// ─── KaTeX helpers ─────────────────────────────────────────────────────────
function K(s, el, d) {
  try { katex.render(s, el, { throwOnError: false, displayMode: !!d }); }
  catch(e) { el.textContent = s; }
}
function C(n, k) {
  if (k < 0 || k > n) return 0;
  if (k === 0 || k === n) return 1;
  let r = 1;
  for (let i = 0; i < k; i++) r = r * (n - i) / (i + 1);
  return Math.round(r);
}
function gel(id) { return document.getElementById(id); }

// ─── State ────────────────────────────────────────────────────────────────
let curN = 3;

// ─── Tabs ─────────────────────────────────────────────────────────────────
function swTab(name, btn) {
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  gel('pane-' + name).classList.add('active');
  btn.classList.add('active');
}

// ─── N selector ───────────────────────────────────────────────────────────
function setN(n, btn) {
  curN = n;
  document.querySelectorAll('.n-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.xb').forEach(b => b.classList.remove('on'));
  renderGeneral();
  const rb = gel('rbox');
  rb.className = 'result-box';
  rb.innerHTML = '<p style="color:#94a3b8;font-size:12px;text-align:center;">↑ 위의 버튼을 눌러 대입해 보세요!</p>';
}

function renderGeneral() {
  const n = curN;
  let terms = [];
  for (let k = 0; k <= n; k++) {
    const c = C(n, k);
    if (k === 0) terms.push(String(c));
    else if (k === 1) terms.push(c + 'x');
    else terms.push(c + 'x^{' + k + '}');
  }
  K('(1+x)^{' + n + '} = ' + terms.join('+'), gel('gformula'), true);
}

// ─── Substitutions ────────────────────────────────────────────────────────
function doSub(mode, btn) {
  document.querySelectorAll('.xb').forEach(b => b.classList.remove('on'));
  btn.classList.add('on');
  const n = curN;
  const rb = gel('rbox');
  rb.className = 'result-box on';

  if (mode === 'x1') {
    const sum = Math.pow(2, n);
    const terms = Array.from({length: n+1}, (_, k) => '\\binom{' + n + '}{' + k + '}').join('+');
    rb.innerHTML = '<div class="res-tag" style="color:#166534">✅ x = 1을 대입하면</div>'
      + '<div class="res-formula" id="rr1"></div>'
      + '<div class="res-formula" id="rr2"></div>'
      + '<div class="res-note">이항계수의 합 = 2<sup>' + n + '</sup> = <strong>' + sum + '</strong> &nbsp; n개 원소의 모든 부분집합의 수와 같습니다!</div>';
    K('(1+1)^{' + n + '} = 2^{' + n + '} = ' + sum, gel('rr1'), true);
    K(terms + ' = ' + sum, gel('rr2'), true);

  } else if (mode === 'xm1') {
    const terms = Array.from({length: n+1}, (_, k) => {
      const s = k % 2 === 0 ? '' : '-';
      return (k === 0 ? '' : (k % 2 === 0 ? '+' : '-')) + '\\binom{' + n + '}{' + k + '}';
    }).join('');
    rb.innerHTML = '<div class="res-tag" style="color:#dc2626">🔴 x = −1을 대입하면</div>'
      + '<div class="res-formula" id="rr1"></div>'
      + '<div class="res-formula" id="rr2"></div>'
      + '<div class="res-note">교대 부호 이항계수의 합 = <strong>0</strong> &nbsp; 짝수 번째 합 = 홀수 번째 합!</div>';
    K('(1+(-1))^{' + n + '} = 0^{' + n + '} = 0', gel('rr1'), true);
    K(terms + ' = 0', gel('rr2'), true);

  } else if (mode === 'diff') {
    const sum = n * Math.pow(2, n - 1);
    const terms = Array.from({length: n}, (_, i) => {
      const k = i + 1;
      return (k === 1 ? '' : k + '\\cdot') + '\\binom{' + n + '}{' + k + '}';
    }).join('+');
    rb.innerHTML = '<div class="res-tag" style="color:#d97706">📐 양변을 x로 미분한 후 x=1 대입</div>'
      + '<div class="res-formula" id="rr1"></div>'
      + '<div class="res-formula" id="rr2"></div>'
      + '<div class="res-formula" id="rr3"></div>'
      + '<div class="res-note">k를 곱한 이항계수의 합 = n × 2<sup>n−1</sup> = <strong>' + sum + '</strong></div>';
    K('\\text{미분:}\\quad n(1+x)^{n-1} = \\textstyle\\sum_{k=1}^{n}k\\binom{n}{k}x^{k-1}', gel('rr1'), true);
    K('\\text{x=1 대입:}\\quad ' + n + '\\cdot 2^{' + (n-1) + '} = ' + terms, gel('rr2'), true);
    K('\\Rightarrow\\; ' + terms + ' = ' + sum, gel('rr3'), true);

  } else if (mode === 'intg') {
    const num = Math.pow(2, n + 1) - 1;
    const den = n + 1;
    const terms = Array.from({length: n+1}, (_, k) => '\\dfrac{\\binom{' + n + '}{' + k + '}}{' + (k+1) + '}').join('+');
    rb.innerHTML = '<div class="res-tag" style="color:#0891b2">∫ 양변을 0부터 1까지 적분</div>'
      + '<div class="res-formula" id="rr1"></div>'
      + '<div class="res-formula" id="rr2"></div>'
      + '<div class="res-note">분모가 1씩 커지는 이항계수 합 = (2<sup>' + (n+1) + '</sup>−1)/' + den + ' = <strong>' + (num/den).toFixed(4) + '</strong></div>';
    K('\\int_0^1(1+x)^{' + n + '}dx = \\left[\\dfrac{(1+x)^{' + (n+1) + '}}{' + den + '}\\right]_0^1 = \\dfrac{2^{' + (n+1) + '}-1}{' + den + '}', gel('rr1'), true);
    K(terms + ' = \\dfrac{' + num + '}{' + den + '}', gel('rr2'), true);

  } else if (mode === 'x2') {
    const sum = Math.pow(3, n);
    const terms = Array.from({length: n+1}, (_, k) => {
      if (k === 0) return '\\binom{' + n + '}{0}';
      if (k === 1) return '2\\binom{' + n + '}{1}';
      return '2^{' + k + '}\\binom{' + n + '}{' + k + '}';
    }).join('+');
    rb.innerHTML = '<div class="res-tag" style="color:#7c3aed">💜 x = 2를 대입하면</div>'
      + '<div class="res-formula" id="rr1"></div>'
      + '<div class="res-formula" id="rr2"></div>'
      + '<div class="res-note">2^k를 곱한 이항계수 합 = 3<sup>' + n + '</sup> = <strong>' + sum + '</strong> &nbsp; (3진법 전개!)</div>';
    K('(1+2)^{' + n + '} = 3^{' + n + '} = ' + sum, gel('rr1'), true);
    K(terms + ' = ' + sum, gel('rr2'), true);
  }
}

// ─── Summary table ────────────────────────────────────────────────────────
function renderTable() {
  K('\\binom{n}{0}+\\binom{n}{1}+\\cdots+\\binom{n}{n}=2^n', gel('st1'));
  K('\\binom{n}{0}-\\binom{n}{1}+\\cdots+(-1)^n\\binom{n}{n}=0', gel('st2'));
  K('\\binom{n}{1}+2\\binom{n}{2}+\\cdots+n\\binom{n}{n}=n\\cdot 2^{n-1}', gel('st3'));
  K('\\binom{n}{0}+\\dfrac{\\binom{n}{1}}{2}+\\cdots+\\dfrac{\\binom{n}{n}}{n+1}=\\dfrac{2^{n+1}-1}{n+1}', gel('st4'));
}

// ─── Formula cards ────────────────────────────────────────────────────────
const FDATA = [
  {
    f: '\\binom{n}{0}+\\binom{n}{1}+\\cdots+\\binom{n}{n}=2^n',
    b: '(1+1)^n=2^n \\;\\Rightarrow\\; \\displaystyle\\sum_{k=0}^n\\binom{n}{k}=2^n'
  },
  {
    f: '\\binom{n}{0}-\\binom{n}{1}+\\binom{n}{2}-\\cdots+(-1)^n\\binom{n}{n}=0',
    b: '(1{-}1)^n=0 \\;\\Rightarrow\\; \\displaystyle\\sum_{k=0}^n(-1)^k\\binom{n}{k}=0'
  },
  {
    f: '\\binom{n}{1}+2\\binom{n}{2}+\\cdots+n\\binom{n}{n}=n\\cdot 2^{n-1}',
    b: '\\tfrac{d}{dx}(1{+}x)^n\\big|_{x=1}:\\; n\\cdot 2^{n-1}=\\textstyle\\sum_{k=1}^n k\\binom{n}{k}'
  },
  {
    f: '\\binom{n}{0}+\\dfrac{\\binom{n}{1}}{2}+\\cdots+\\dfrac{\\binom{n}{n}}{n+1}=\\dfrac{2^{n+1}-1}{n+1}',
    b: '\\displaystyle\\int_0^1(1{+}x)^ndx=\\dfrac{2^{n+1}-1}{n+1}=\\sum_{k=0}^n\\dfrac{\\binom{n}{k}}{k+1}'
  },
  {
    f: '\\displaystyle\\sum_{k=0}^{r}\\binom{m}{k}\\binom{n}{r-k}=\\binom{m+n}{r}',
    b: '(1{+}x)^{m+n}=(1{+}x)^m(1{+}x)^n\\text{의 }x^r\\text{ 계수 비교}'
  },
  {
    f: '\\binom{n}{0}^2+\\binom{n}{1}^2+\\cdots+\\binom{n}{n}^2=\\binom{2n}{n}',
    b: '\\text{⑤에서 }m{=}n,\\,r{=}n\\text{: }\\,\\binom{n}{k}=\\binom{n}{n-k}\\text{ 이용}'
  },
  {
    f: '\\binom{n}{0}+\\binom{n+1}{1}+\\binom{n+2}{2}+\\cdots+\\binom{n+r}{r}=\\binom{n+r+1}{r}',
    b: '\\binom{n{+}r{+}1}{r}=\\binom{n{+}r}{r}+\\binom{n{+}r}{r-1}=\\cdots \\text{(반복)}'
  },
  {
    f: '\\binom{r}{r}+\\binom{r+1}{r}+\\binom{r+2}{r}+\\cdots+\\binom{n}{r}=\\binom{n+1}{r+1}\\;(n\\geq r)',
    b: '\\binom{r}{r}=\\binom{r+1}{r+1}\\text{, 이후 }\\binom{k+1}{r+1}+\\binom{k+1}{r}=\\binom{k+2}{r+1}\\text{ 반복}'
  },
];

function renderCards() {
  FDATA.forEach((d, i) => {
    const fi = gel('cf' + (i+1) + 'f');
    const bi = gel('cf' + (i+1) + 'b');
    if (fi) K(d.f, fi, true);
    if (bi) K(d.b, bi, false);
  });
}

// ─── Quiz ─────────────────────────────────────────────────────────────────
const QUIZ = [
  {
    q: '이항정리 (1+x)ⁿ에서 x = 1을 대입하면 나오는 공식은?',
    ch: [
      '\\binom{n}{0}+\\binom{n}{1}+\\cdots+\\binom{n}{n}=2^n',
      '\\binom{n}{0}-\\binom{n}{1}+\\cdots+(-1)^n\\binom{n}{n}=0',
      '\\binom{n}{1}+2\\binom{n}{2}+\\cdots+n\\binom{n}{n}=n\\cdot 2^{n-1}',
      '\\binom{n}{0}+\\frac{\\binom{n}{1}}{2}+\\cdots=\\frac{2^{n+1}-1}{n+1}',
    ],
    ans: 0,
    ex: 'x=1을 대입하면 (1+1)ⁿ=2ⁿ이 되고, 우변 각 항의 xᵏ=1이 되어 이항계수의 합 = 2ⁿ이 도출됩니다.'
  },
  {
    q: '이항계수의 교대 부호 합( ₙC₀−ₙC₁+ₙC₂−⋯ )이 0이 됨을 보이려면?',
    ch: ['x = 2 대입', 'x = −1 대입', '양변 미분 후 x=1 대입', '양변을 0~1 적분'],
    ans: 1,
    plain: true,
    ex: 'x=−1을 대입하면 (1−1)ⁿ=0ⁿ=0이 되고, 우변이 교대 부호 이항계수의 합이 됩니다.'
  },
  {
    q: 'ₙC₁ + 2·ₙC₂ + ⋯ + n·ₙCₙ = n·2ⁿ⁻¹ 을 도출하는 방법은?',
    ch: ['x = 1 대입', 'x = −1 대입', '양변을 x로 미분한 후 x=1 대입', '양변을 0~1 적분'],
    ans: 2,
    plain: true,
    ex: '(1+x)ⁿ을 미분하면 n(1+x)ⁿ⁻¹=Σk·C(n,k)·xᵏ⁻¹. x=1 대입 → n·2ⁿ⁻¹=Σk·C(n,k).'
  },
  {
    q: 'ₙC₀ + ₙC₁/2 + ₙC₂/3 + ⋯ + ₙCₙ/(n+1) = (2ⁿ⁺¹−1)/(n+1) 을 유도하는 방법은?',
    ch: ['x = 1 대입', 'x = −1 대입', '양변 미분 후 x=1 대입', '양변을 0에서 1까지 적분'],
    ans: 3,
    plain: true,
    ex: '(1+x)ⁿ을 0~1에서 적분: [(1+x)ⁿ⁺¹/(n+1)]₀¹=(2ⁿ⁺¹−1)/(n+1). 우변 적분하면 ΣC(n,k)/(k+1).'
  },
  {
    q: '반데몬드 항등식 Σ(ₘCₖ×ₙCᵣ₋ₖ) = ₘ₊ₙCᵣ 는 어떻게 유도하나요?',
    ch: [
      '이항정리에 x=1 대입',
      '(1+x)^{m+n}=(1+x)^m·(1+x)^n 의 x^r 계수 비교',
      '파스칼 항등식 반복 적용',
      '미분 후 x=1 대입',
    ],
    ans: 1,
    plain: true,
    ex: '(1+x)^{m+n}의 x^r 계수는 C(m+n,r). (1+x)^m·(1+x)^n의 x^r 계수는 ΣC(m,k)·C(n,r-k). 양변이 같으므로 성립!'
  },
  {
    q: 'n=4 일 때,  ₄C₀ + ₄C₁ + ₄C₂ + ₄C₃ + ₄C₄ 의 값은?',
    ch: ['8', '12', '16', '32'],
    ans: 2,
    plain: true,
    ex: '공식 ①: n=4이면 2⁴=16. 실제로 1+4+6+4+1=16.'
  },
  {
    q: 'n=3 일 때,  ₃C₀ − ₃C₁ + ₃C₂ − ₃C₃ 의 값은?',
    ch: ['−2', '−1', '0', '1'],
    ans: 2,
    plain: true,
    ex: '공식 ②: 1−3+3−1=0. 교대 부호 합은 항상 0!'
  },
  {
    q: '(ₙC₀)²+(ₙC₁)²+⋯+(ₙCₙ)² = ₂ₙCₙ 은 어떤 항등식의 특수한 경우인가요?',
    ch: [
      '이항정리에 x=−1 대입',
      '반데몬드 항등식에서 m=n, r=n으로 놓은 것',
      '파스칼 성질 ⑦',
      '양변 미분 후 대입',
    ],
    ans: 1,
    plain: true,
    ex: '반데몬드 ΣC(n,k)·C(n,n−k)=C(2n,n) 에서 C(n,k)=C(n,n−k)이므로 ΣC(n,k)²=C(2n,n).'
  },
];

let qIdx = 0, qSc = 0, qTot = 0, qDone = false;

function startQuiz() {
  qIdx = 0; qSc = 0; qTot = 0; qDone = false;
  gel('quiz-container').style.display = '';
  gel('quiz-result').style.display = 'none';
  renderQ();
}

function renderQ() {
  const q = QUIZ[qIdx];
  gel('qprog').textContent = '문제 ' + (qIdx+1) + ' / ' + QUIZ.length;
  gel('qbar').style.width = (qIdx / QUIZ.length * 100) + '%';
  gel('qscore').textContent = '점수: ' + qSc + ' / ' + qTot;
  gel('qfb').className = 'qfb';
  gel('qnext').className = 'qnext';
  qDone = false;

  gel('qq').textContent = q.q;

  const cc = gel('qchoices');
  cc.innerHTML = '';
  q.ch.forEach((c, ci) => {
    const b = document.createElement('button');
    b.className = 'qch';
    if (!q.plain && c.includes('\\')) {
      try { K(c, b, false); } catch(e) { b.textContent = c; }
    } else {
      b.textContent = c;
    }
    b.onclick = () => pick(ci);
    cc.appendChild(b);
  });
}

function pick(ci) {
  if (qDone) return;
  qDone = true; qTot++;
  const q = QUIZ[qIdx];
  const ok = (ci === q.ans);
  if (ok) qSc++;
  gel('qscore').textContent = '점수: ' + qSc + ' / ' + qTot;
  const btns = gel('qchoices').querySelectorAll('.qch');
  btns.forEach((b, i) => {
    b.disabled = true;
    if (i === q.ans) b.classList.add((ok && i === ci) ? 'ok' : 'show-ok');
    if (i === ci && !ok) b.classList.add('ng');
  });
  const fb = gel('qfb');
  fb.className = 'qfb show ' + (ok ? 'ok' : 'ng');
  fb.textContent = (ok ? '✅ 정답! ' : '❌ 아쉽네요. ') + q.ex;
  gel('qnext').className = 'qnext show';
}

function nextQ() {
  qIdx++;
  if (qIdx >= QUIZ.length) showResult();
  else renderQ();
}

function showResult() {
  gel('quiz-container').style.display = 'none';
  gel('quiz-result').style.display = '';
  gel('qrsc').textContent = qSc + ' / ' + QUIZ.length;
  const p = qSc / QUIZ.length;
  let msg = '';
  if (p >= 0.875) msg = '🏆 완벽합니다! 이항정리의 활용 달인이군요!';
  else if (p >= 0.625) msg = '👏 잘했어요! 틀린 문제는 공식 카드 탭에서 복습해보세요.';
  else if (p >= 0.375) msg = '💪 조금 더 노력해봐요! 대입 탐험 탭부터 다시 확인해보세요.';
  else msg = '📖 공식 카드 탭을 꼼꼼히 읽고 다시 도전해보세요!';
  gel('qrmsg').textContent = msg;
}

// ─── Init ─────────────────────────────────────────────────────────────────
function initApp() {
  K('(1+x)^n', gel('base-formula'), false);
  renderGeneral();
  renderTable();
  renderCards();
  startQuiz();
}
</script>
</body>
</html>"""


def render():
    st.header("🧮 이항정리의 활용")
    st.markdown(
        "이항정리 $(1+x)^n$에 값을 **대입·미분·적분**하거나, "
        "$(1+x)^{m+n}=(1+x)^m\\cdot(1+x)^n$으로 분해하면 "
        "이항계수의 다양한 성질 **8가지**를 도출할 수 있습니다. "
        "세 탭을 순서대로 탐구하고 퀴즈로 실력을 확인해보세요!"
    )
    components.html(_HTML, height=1100, scrolling=True)
    st.markdown("---")
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
