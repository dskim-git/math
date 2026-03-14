import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 제타함수와 산술함수의 관계",
    "description": "1/ζ(s), ζ(s-1)/ζ(s), ζ(s)², ζ(s)×ζ(s-1)과 μ, φ, τ, σ 함수의 관계를 게임으로 탐구합니다.",
    "order": 14,
    "hidden": True,
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans KR', sans-serif; background: #0f172a; color: #f1f5f9; }
#app { max-width: 980px; margin: 0 auto; padding: 12px; }

/* ── 헤더 ── */
.hero { text-align: center; padding: 18px 10px 12px; }
.hero h1 { font-size: 1.45rem; font-weight: 900; color: #fbbf24; margin-bottom: 5px; }
.hero p  { font-size: 0.88rem; color: #94a3b8; }

/* ── 탭 ── */
.tab-row { display: flex; gap: 5px; margin-bottom: 14px; flex-wrap: wrap; justify-content: center; }
.tab-btn {
  padding: 7px 15px; border-radius: 20px; border: 1.5px solid #334155;
  background: #1e293b; font-size: 0.82rem; font-weight: 700;
  cursor: pointer; color: #94a3b8; transition: all .18s;
}
.tab-btn.active { background: #f59e0b; color: #0f172a; border-color: #f59e0b; }
.tab-btn:hover:not(.active) { background: #334155; color: #f1f5f9; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }

/* ── 카드 ── */
.card { background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 16px; margin-bottom: 12px; }
.card-title { font-size: 1rem; font-weight: 800; margin-bottom: 10px; }

/* ── 수식 배너 ── */
.formula-banner {
  background: linear-gradient(120deg, #1e3a5f, #1e293b);
  border: 2px solid #3b82f6; border-radius: 14px;
  padding: 14px 20px; margin-bottom: 14px; text-align: center;
}
.formula-banner .fb-main { font-size: 1.25rem; font-weight: 900; color: #93c5fd; margin-bottom: 4px; }
.formula-banner .fb-sub  { font-size: 0.8rem; color: #64748b; }

/* ── 버튼 ── */
button { padding: 7px 16px; border-radius: 10px; border: none; font-size: 0.84rem; font-weight: 700; cursor: pointer; transition: all .15s; }
button:active { transform: translateY(1px); }
.btn-blue   { background: #3b82f6; color: #fff; }
.btn-blue:hover   { background: #2563eb; }
.btn-green  { background: #10b981; color: #fff; }
.btn-green:hover  { background: #059669; }
.btn-yellow { background: #f59e0b; color: #0f172a; }
.btn-yellow:hover { background: #d97706; }
.btn-red    { background: #ef4444; color: #fff; }
.btn-red:hover    { background: #dc2626; }
.btn-gray   { background: #334155; color: #cbd5e1; }
.btn-gray:hover   { background: #475569; }
.btn-row { display: flex; gap: 7px; flex-wrap: wrap; margin-top: 10px; }

/* ── 색상 테마 ── */
.mu-col  { color: #f87171; }
.phi-col { color: #a78bfa; }
.tau-col { color: #60a5fa; }
.sig-col { color: #34d399; }
.zeta-col { color: #fbbf24; }

/* ── 테이블 ── */
.table-wrap { overflow-x: auto; max-height: 480px; overflow-y: auto; }
table.t { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
table.t th { background: #1d4ed8; color: #fff; padding: 8px 9px; text-align: center; position: sticky; top: 0; z-index: 2; white-space: nowrap; }
table.t td { padding: 6px 9px; text-align: center; border-bottom: 1px solid #1e293b; transition: background .1s; }
table.t tr:hover td { background: #1e3a5f !important; }
table.t tr.row-hi td { background: #172554 !important; }
.td-n   { font-weight: 900; color: #fbbf24; background: #0f172a !important; }
.mu-pos { color: #34d399; font-weight: 700; }
.mu-neg { color: #f87171; font-weight: 700; }
.mu-z   { color: #475569; }
.phi-v  { color: #a78bfa; font-weight: 700; }
.tau-v  { color: #60a5fa; font-weight: 700; }
.sig-v  { color: #34d399; font-weight: 700; }

/* ── 게임 ── */
.game-area {
  background: #020617; border: 2px solid #fbbf24; border-radius: 18px;
  padding: 20px; text-align: center; margin-bottom: 14px;
}
.game-q  { font-size: 1.1rem; font-weight: 700; margin-bottom: 6px; color: #e2e8f0; }
.game-q2 { font-size: 0.85rem; color: #94a3b8; margin-bottom: 18px; }
.choices { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.choice-btn {
  padding: 10px 22px; border-radius: 12px; border: 2px solid #334155;
  background: #1e293b; color: #e2e8f0; font-size: 1rem; font-weight: 700;
  cursor: pointer; transition: all .15s; min-width: 80px;
}
.choice-btn:hover { border-color: #f59e0b; color: #f59e0b; }
.choice-btn.correct { background: #064e3b; border-color: #34d399; color: #34d399; }
.choice-btn.wrong   { background: #450a0a; border-color: #ef4444; color: #ef4444; }
.choice-btn:disabled { cursor: default; }

.score-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.score-badge { background: #f59e0b; color: #0f172a; border-radius: 20px; padding: 3px 14px; font-size: 0.88rem; font-weight: 900; }
.lives { color: #f87171; font-size: 1.2rem; letter-spacing: 2px; }
.q-prog { height: 6px; background: #1e293b; border-radius: 4px; margin-bottom: 12px; }
.q-prog-fill { height: 100%; background: #f59e0b; border-radius: 4px; transition: width .4s; }

.result-box { background: #1e293b; border-radius: 14px; padding: 14px; margin-top: 10px; font-size: 0.85rem; color: #94a3b8; min-height: 40px; line-height: 1.7; }
.result-box .r-correct { color: #34d399; font-weight: 700; }
.result-box .r-wrong   { color: #f87171; font-weight: 700; }

.streak-badge { background: #7c3aed; color: #fff; border-radius: 20px; padding: 2px 10px; font-size: 0.78rem; font-weight: 700; margin-left: 8px; }

/* ── 시각화 패널 ── */
.viz-wrap { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 560px) { .viz-wrap { grid-template-columns: 1fr; } }
.vcard { border-radius: 14px; padding: 14px; border: 2px solid; }
.vcard-mu  { border-color: #f87171; background: #1c0a0a; }
.vcard-phi { border-color: #a78bfa; background: #150d2b; }
.vcard-tau { border-color: #60a5fa; background: #0d1b33; }
.vcard-sig { border-color: #34d399; background: #061a11; }
.vcard .vc-title { font-size: 0.97rem; font-weight: 900; margin-bottom: 8px; }
.vcard .vc-eq { font-size: 0.9rem; color: #94a3b8; margin-bottom: 10px; font-style: italic; }

/* 계단 시각화 */
.bar-row { display: flex; align-items: flex-end; gap: 3px; height: 110px; margin-top: 8px; }
.bar { border-radius: 4px 4px 0 0; min-width: 14px; flex: 1; transition: all .3s; position: relative; cursor: pointer; }
.bar:hover { opacity: 0.8; }
.bar .bar-val { position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
  font-size: 0.65rem; font-weight: 700; white-space: nowrap; }
.bar .bar-lbl { position: absolute; bottom: -18px; left: 50%; transform: translateX(-50%);
  font-size: 0.65rem; color: #64748b; white-space: nowrap; }

/* ── 디리클레 곱 시각화 ── */
.dc-area { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 8px; align-items: center; }
@media (max-width: 560px) { .dc-area { grid-template-columns: 1fr; } }
.dc-box { background: #0f172a; border-radius: 12px; padding: 10px; text-align: center; }
.dc-box .dc-label { font-size: 0.78rem; color: #64748b; margin-bottom: 4px; }
.dc-box .dc-val   { font-size: 1.4rem; font-weight: 900; }
.dc-op { font-size: 1.4rem; font-weight: 900; color: #fbbf24; text-align: center; }

/* ── 범례 ── */
.legend { display: flex; gap: 12px; flex-wrap: wrap; margin: 8px 0; font-size: 0.78rem; }
.leg-item { display: flex; align-items: center; gap: 5px; }
.leg-dot { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }

/* ── 슬라이더 ── */
.ctrl-row { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 10px; }
.ctrl-row label { font-size: 0.85rem; font-weight: 700; color: #94a3b8; }
input[type=range] { accent-color: #f59e0b; cursor: pointer; }
.rv { font-size: 1.1rem; font-weight: 900; color: #fbbf24; min-width: 30px; display: inline-block; text-align: center; }

/* ── 소수분해 표시 ── */
.pf-row { display: flex; flex-wrap: wrap; gap: 5px; margin: 8px 0; align-items: center; }
.pf-tag { padding: 3px 10px; border-radius: 8px; font-weight: 700; font-size: 0.82rem; }
.pf-mu  { background: #450a0a; color: #f87171; }
.pf-phi { background: #220f47; color: #c4b5fd; }
.pf-tau { background: #0d1b33; color: #93c5fd; }
.pf-sig { background: #061a11; color: #6ee7b7; }
.step-row { font-size: 0.8rem; color: #64748b; margin: 4px 0; line-height: 1.7; }
.hi { color: #fbbf24; font-weight: 700; }

/* ── 도전 ── */
.challenge-status { background: #1e3a5f; border-radius: 12px; padding: 12px; margin: 10px 0; text-align: center; }
.challenge-status .cs-score { font-size: 1.8rem; font-weight: 900; color: #fbbf24; }
.challenge-status .cs-label { font-size: 0.8rem; color: #94a3b8; }
.stars { font-size: 1.4rem; letter-spacing: 2px; }

/* ── 알림 토스트 ── */
#toast {
  position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(80px);
  background: #fbbf24; color: #0f172a; border-radius: 12px;
  padding: 10px 24px; font-weight: 700; font-size: 0.9rem;
  transition: transform .35s; z-index: 999; pointer-events: none;
}
#toast.show { transform: translateX(-50%) translateY(0); }

/* ── 응답형 ── */
@media (max-width: 480px) {
  .formula-banner .fb-main { font-size: 1rem; }
  .game-q { font-size: 0.95rem; }
}
</style>
</head>
<body>
<div id="app">

<div class="hero">
  <h1>⚡ 제타함수 × 산술함수 탐험</h1>
  <p>μ(n), φ(n), τ(n), σ(n)과 ζ(s)의 신비로운 관계를 발견하자!</p>
</div>

<!-- 탭 -->
<div class="tab-row">
  <button class="tab-btn active" onclick="showTab('tab-relation')">🔗 관계 탐구</button>
  <button class="tab-btn" onclick="showTab('tab-table')">📊 함수 테이블</button>
  <button class="tab-btn" onclick="showTab('tab-game')">🎮 퀴즈 게임</button>
  <button class="tab-btn" onclick="showTab('tab-dirichlet')">🧩 디리클레 급수</button>
</div>

<!-- ══════════════════════════════════════════════════════════
     TAB 1: 관계 탐구
══════════════════════════════════════════════════════════ -->
<div id="tab-relation" class="tab-panel active">

  <div class="card">
    <div class="card-title">🌟 핵심 공식 4개</div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
      <div class="vcard vcard-mu">
        <div class="vc-title mu-col">① 뫼비우스 함수 μ(n)</div>
        <div class="vc-eq">1/ζ(s) = Σ μ(n)/nˢ</div>
        <div style="font-size:0.78rem;color:#94a3b8;line-height:1.65;">
          ζ(s)의 역수 = μ(n)의 디리클레 급수<br>
          • μ(1)=1<br>
          • μ(n)=(-1)ᵏ, n이 서로 다른 소수 k개의 곱<br>
          • μ(n)=0, n이 제곱수 인수를 가질 때
        </div>
      </div>
      <div class="vcard vcard-phi">
        <div class="vc-title phi-col">② 오일러 파이 함수 φ(n)</div>
        <div class="vc-eq">ζ(s-1)/ζ(s) = Σ φ(n)/nˢ</div>
        <div style="font-size:0.78rem;color:#94a3b8;line-height:1.65;">
          ζ(s-1)과 ζ(s)의 비 = φ(n)의 급수<br>
          • φ(n) = n·∏(1-1/p)<br>
          • φ(n): 1~n 중 n과 서로소인 수의 개수
        </div>
      </div>
      <div class="vcard vcard-tau">
        <div class="vc-title tau-col">③ 약수 개수 τ(n)</div>
        <div class="vc-eq">[ζ(s)]² = Σ τ(n)/nˢ</div>
        <div style="font-size:0.78rem;color:#94a3b8;line-height:1.65;">
          ζ(s)의 제곱 = τ(n)의 급수<br>
          • τ(n) = (α₁+1)(α₂+1)···(αₖ+1)<br>
          • τ(n): n의 양의 약수의 개수
        </div>
      </div>
      <div class="vcard vcard-sig">
        <div class="vc-title sig-col">④ 약수 합 σ(n)</div>
        <div class="vc-eq">ζ(s)·ζ(s-1) = Σ σ(n)/nˢ</div>
        <div style="font-size:0.78rem;color:#94a3b8;line-height:1.65;">
          ζ(s)×ζ(s-1) = σ(n)의 급수<br>
          • σ(n) = 1+d₁+d₂+···+n<br>
          • σ(n): n의 양의 약수의 합
        </div>
      </div>
    </div>
  </div>

  <!-- n 선택 시각화 -->
  <div class="card">
    <div class="card-title">🔢 n을 골라 직접 계산해 보자!</div>
    <div class="ctrl-row">
      <label>n =</label>
      <input type="range" id="nSlider" min="1" max="36" value="12" oninput="updateN(this.value)">
      <span class="rv" id="nVal">12</span>
      <div style="display:flex;gap:5px;flex-wrap:wrap;">
        <button class="btn-blue" onclick="setN(1)">1</button>
        <button class="btn-blue" onclick="setN(2)">2</button>
        <button class="btn-blue" onclick="setN(6)">6</button>
        <button class="btn-blue" onclick="setN(12)">12</button>
        <button class="btn-blue" onclick="setN(30)">30</button>
        <button class="btn-blue" onclick="setN(36)">36</button>
      </div>
    </div>
    <div id="nDetail"></div>
  </div>

  <!-- 막대 비교 -->
  <div class="card">
    <div class="card-title">📈 n=1~20 함수값 비교</div>
    <div class="legend">
      <span class="leg-item"><span class="leg-dot" style="background:#f87171;"></span><span>μ(n)+1 (표시용)</span></span>
      <span class="leg-item"><span class="leg-dot" style="background:#a78bfa;"></span><span>φ(n)</span></span>
      <span class="leg-item"><span class="leg-dot" style="background:#60a5fa;"></span><span>τ(n)</span></span>
      <span class="leg-item"><span class="leg-dot" style="background:#34d399;"></span><span>σ(n)/n</span></span>
    </div>
    <div style="display:flex;gap:6px;margin-bottom:8px;flex-wrap:wrap;">
      <button class="btn-gray" onclick="setVizFunc('mu')" id="vbmu">μ(n)</button>
      <button class="btn-gray" onclick="setVizFunc('phi')" id="vbphi">φ(n)</button>
      <button class="btn-blue" onclick="setVizFunc('tau')" id="vbtau">τ(n)</button>
      <button class="btn-gray" onclick="setVizFunc('sigma')" id="vbsigma">σ(n)</button>
    </div>
    <canvas id="cvBar" width="900" height="160" style="width:100%;border-radius:10px;background:#0f172a;"></canvas>
    <div style="font-size:0.75rem;color:#64748b;text-align:center;margin-top:4px;">n = 1, 2, 3, ..., 20</div>
  </div>

</div>

<!-- ══════════════════════════════════════════════════════════
     TAB 2: 함수 테이블
══════════════════════════════════════════════════════════ -->
<div id="tab-table" class="tab-panel">
  <div class="card">
    <div class="card-title">📊 산술함수 값 테이블 (n = 1 ~ 50)</div>
    <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:8px;">
      소수행은 🟢, 완전수(σ=2n)는 🌟 표시. 행을 클릭하면 상세 계산을 볼 수 있어요.
    </div>
    <div class="legend" style="margin-bottom:10px;">
      <span class="leg-item"><span class="leg-dot" style="background:#14532d;width:18px;height:12px;"></span><span>소수</span></span>
      <span class="leg-item"><span class="leg-dot" style="background:#1e3a5f;width:18px;height:12px;"></span><span>완전수</span></span>
    </div>
    <div class="table-wrap">
      <table class="t" id="mainTable">
        <thead>
          <tr>
            <th>n</th>
            <th>소인수분해</th>
            <th class="mu-col">μ(n)</th>
            <th class="phi-col">φ(n)</th>
            <th class="tau-col">τ(n)</th>
            <th class="sig-col">σ(n)</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
    <div id="tableDetail" class="result-box" style="margin-top:10px;display:none;"></div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════
     TAB 3: 퀴즈 게임
══════════════════════════════════════════════════════════ -->
<div id="tab-game" class="tab-panel">

  <div class="score-bar">
    <div>
      <span class="score-badge" id="scoreDisp">점수: 0</span>
      <span class="streak-badge" id="streakDisp" style="display:none;">🔥 0 연속</span>
    </div>
    <span class="lives" id="livesDisp">❤️❤️❤️</span>
  </div>
  <div class="q-prog"><div class="q-prog-fill" id="qProgFill" style="width:0%"></div></div>

  <div class="game-area" id="gameArea">
    <div class="game-q" id="gameQ">아래 시작 버튼을 눌러 게임을 시작하세요!</div>
    <div class="game-q2" id="gameQ2"></div>
    <div class="choices" id="gameChoices"></div>
    <div class="result-box" id="gameResult" style="margin-top:12px;text-align:left;display:none;"></div>
  </div>

  <div class="btn-row" style="justify-content:center;">
    <button class="btn-yellow" id="startBtn" onclick="startGame()">🚀 게임 시작!</button>
    <button class="btn-gray" id="nextBtn" onclick="nextQ()" style="display:none;">다음 문제 ▶</button>
  </div>

  <div class="card" style="margin-top:10px;">
    <div class="card-title">📋 문제 유형 안내</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.8rem;color:#94a3b8;">
      <div>🔴 μ(n) 계산 — 소인수 개수와 제곱인수 확인</div>
      <div>🟣 φ(n) 계산 — 서로소인 수의 개수</div>
      <div>🔵 τ(n) 계산 — 약수의 개수</div>
      <div>🟢 σ(n) 계산 — 약수들의 합</div>
      <div>⭐ 공식 매칭 — 제타함수와의 관계식 연결</div>
      <div>🎯 역 추론 — 함수값으로 n 찾기</div>
    </div>
  </div>

</div>

<!-- ══════════════════════════════════════════════════════════
     TAB 4: 디리클레 급수
══════════════════════════════════════════════════════════ -->
<div id="tab-dirichlet" class="tab-panel">

  <div class="card">
    <div class="card-title">🧩 디리클레 급수 = 함수값의 합</div>
    <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:10px;line-height:1.7;">
      디리클레 급수 Σ f(n)/nˢ 의 처음 N개 항을 더해서 실제값과 얼마나 가까워지는지 확인해 보세요.<br>
      s가 클수록 더 빠르게 수렴합니다!
    </div>

    <div class="ctrl-row">
      <label>함수 선택:</label>
      <select id="dsFunc" onchange="updateDirichlet()" style="background:#334155;color:#f1f5f9;border:1px solid #475569;border-radius:8px;padding:5px 10px;font-size:0.88rem;">
        <option value="mu">μ(n) → 1/ζ(s)</option>
        <option value="phi">φ(n) → ζ(s-1)/ζ(s)</option>
        <option value="tau">τ(n) → [ζ(s)]²</option>
        <option value="sigma">σ(n) → ζ(s)·ζ(s-1)</option>
      </select>
    </div>
    <div class="ctrl-row">
      <label>s =</label>
      <input type="range" id="dsSlider" min="2" max="8" step="0.5" value="3"
             oninput="document.getElementById('dsVal').textContent=this.value; updateDirichlet()">
      <span class="rv" id="dsVal">3</span>
    </div>
    <div class="ctrl-row">
      <label>항 수 N =</label>
      <input type="range" id="dsN" min="1" max="100" value="20"
             oninput="document.getElementById('dsNVal').textContent=this.value; updateDirichlet()">
      <span class="rv" id="dsNVal">20</span>
    </div>

    <div id="dsResult"></div>

    <canvas id="cvDirichlet" width="900" height="180" style="width:100%;border-radius:10px;background:#0f172a;margin-top:10px;"></canvas>

    <div id="dsTermList" style="margin-top:10px;overflow-x:auto;"></div>
  </div>

  <div class="card">
    <div class="card-title">🔍 수렴 직관: 1/nˢ 의 크기</div>
    <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:10px;line-height:1.7;">
      s가 클수록 1/nˢ 가 빠르게 0에 가까워져서 급수가 더 빨리 수렴합니다.<br>
      s=1이면 조화급수(발산!), s=2면 π²/6 ≈ 1.645, s=4면 π⁴/90 ≈ 1.082
    </div>
    <div class="ctrl-row">
      <label>s =</label>
      <input type="range" id="convS" min="1" max="5" step="0.5" value="2"
             oninput="document.getElementById('convSVal').textContent=this.value; updateConv()">
      <span class="rv" id="convSVal">2</span>
    </div>
    <canvas id="cvConv" width="900" height="150" style="width:100%;border-radius:10px;background:#0f172a;"></canvas>
  </div>

</div>

</div><!-- #app -->
<div id="toast"></div>

<script>
// ══════════════════════════════════════════════════════════
//  기본 산술 함수
// ══════════════════════════════════════════════════════════
function primeFactors(n) {
  // { prime: exponent } 형태로 반환
  const f = {};
  let d = 2;
  while (d * d <= n) {
    while (n % d === 0) { f[d] = (f[d] || 0) + 1; n = Math.floor(n / d); }
    d++;
  }
  if (n > 1) f[n] = (f[n] || 0) + 1;
  return f;
}

function mobius(n) {
  const f = primeFactors(n);
  for (const p in f) if (f[p] >= 2) return 0;
  const k = Object.keys(f).length;
  return k % 2 === 0 ? 1 : -1;
}

function euler_phi(n) {
  const f = primeFactors(n);
  let r = n;
  for (const p in f) r = r / p * (p - 1);
  return Math.round(r);
}

function tau(n) {
  const f = primeFactors(n);
  let r = 1;
  for (const p in f) r *= (f[p] + 1);
  return r;
}

function sigma(n) {
  let s = 0;
  for (let i = 1; i <= n; i++) if (n % i === 0) s += i;
  return s;
}

function isPrime(n) {
  if (n < 2) return false;
  for (let i = 2; i <= Math.sqrt(n); i++) if (n % i === 0) return false;
  return true;
}

function factStr(n) {
  const f = primeFactors(n);
  if (Object.keys(f).length === 0) return '1';
  return Object.entries(f).map(([p, e]) => e > 1 ? `${p}^${e}` : p).join(' × ');
}

// ── 제타함수 (partial sum) ──
function zeta(s, N = 500) {
  let r = 0;
  for (let n = 1; n <= N; n++) r += 1 / Math.pow(n, s);
  return r;
}

// ══════════════════════════════════════════════════════════
//  탭 전환
// ══════════════════════════════════════════════════════════
function showTab(id) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  event.target.classList.add('active');
  if (id === 'tab-table') buildTable();
  if (id === 'tab-dirichlet') { updateDirichlet(); updateConv(); }
}

// ══════════════════════════════════════════════════════════
//  TAB 1: n 상세 보기
// ══════════════════════════════════════════════════════════
let currentN = 12;
let vizFunc = 'tau';

function setN(v) { document.getElementById('nSlider').value = v; updateN(v); }
function updateN(v) {
  currentN = parseInt(v);
  document.getElementById('nVal').textContent = v;
  renderNDetail(currentN);
}

function renderNDetail(n) {
  const f = primeFactors(n);
  const mu_v = mobius(n);
  const phi_v = euler_phi(n);
  const tau_v = tau(n);
  const sig_v = sigma(n);
  const ps = Object.keys(f); // prime list

  // 소인수분해 문자열
  let factHTML = ps.length === 0 ? '<span class="hi">1</span>' :
    ps.map(p => f[p] > 1 ? `<span class="hi">${p}<sup>${f[p]}</sup></span>` : `<span class="hi">${p}</span>`).join(' × ');

  // 약수 목록
  let divs = [];
  for (let i = 1; i <= n; i++) if (n % i === 0) divs.push(i);

  // φ(n) 단계
  let phiSteps = `n = ${n}`;
  if (ps.length > 0) {
    phiSteps += ` × ` + ps.map(p => `(1 - 1/${p})`).join(' × ') + ` = ${phi_v}`;
  }

  const muColor = mu_v > 0 ? '#34d399' : mu_v < 0 ? '#f87171' : '#475569';
  const perfect = sig_v === 2 * n;

  document.getElementById('nDetail').innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
      
      <div class="vcard vcard-mu">
        <div class="vc-title mu-col">μ(${n}) = <span style="color:${muColor}">${mu_v}</span></div>
        <div class="step-row">n = ${factHTML}</div>
        ${Object.values(f).some(e => e >= 2)
          ? `<div class="step-row">제곱인수 포함 → <span class="hi">μ = 0</span></div>`
          : `<div class="step-row">서로 다른 소수 <span class="hi">${ps.length}개</span> → (-1)^${ps.length} = <span class="hi">${mu_v}</span></div>`
        }
        <div class="step-row" style="margin-top:6px;color:#64748b;font-size:0.75rem;">
          공식: 1/ζ(s) = Σ μ(n)/nˢ
        </div>
      </div>

      <div class="vcard vcard-phi">
        <div class="vc-title phi-col">φ(${n}) = <span style="color:#a78bfa">${phi_v}</span></div>
        <div class="step-row">φ(${n}) = ${phiSteps}</div>
        <div style="font-size:0.76rem;color:#64748b;margin-top:3px;">
          1~${n} 중 ${n}과 서로소: ${phi_v}개
        </div>
        <div class="step-row" style="margin-top:6px;color:#64748b;font-size:0.75rem;">
          공식: ζ(s-1)/ζ(s) = Σ φ(n)/nˢ
        </div>
      </div>

      <div class="vcard vcard-tau">
        <div class="vc-title tau-col">τ(${n}) = <span style="color:#60a5fa">${tau_v}</span></div>
        <div class="step-row">약수: ${divs.join(', ')}</div>
        ${ps.length > 0
          ? `<div class="step-row">(${Object.values(f).map(e => e+'+1').join(')(')}) = ${tau_v}</div>`
          : `<div class="step-row">τ(1) = 1</div>`
        }
        <div class="step-row" style="margin-top:6px;color:#64748b;font-size:0.75rem;">
          공식: [ζ(s)]² = Σ τ(n)/nˢ
        </div>
      </div>

      <div class="vcard vcard-sig">
        <div class="vc-title sig-col">σ(${n}) = <span style="color:#34d399">${sig_v}</span></div>
        <div class="step-row">${divs.join(' + ')} = ${sig_v}</div>
        ${perfect ? `<div class="step-row" style="color:#fbbf24;font-weight:700;">🌟 완전수! σ(n) = 2n</div>` : ''}
        <div class="step-row" style="margin-top:6px;color:#64748b;font-size:0.75rem;">
          공식: ζ(s)·ζ(s-1) = Σ σ(n)/nˢ
        </div>
      </div>

    </div>`;
}

// ── 막대 그래프 ──
function setVizFunc(f) {
  vizFunc = f;
  ['mu','phi','tau','sigma'].forEach(x => {
    document.getElementById('vb'+x).className = x === f ? 'btn-blue' : 'btn-gray';
  });
  drawBarChart();
}

function drawBarChart() {
  const cv = document.getElementById('cvBar');
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);

  const N = 20;
  const vals = [];
  for (let n = 1; n <= N; n++) {
    if (vizFunc === 'mu') vals.push(mobius(n));
    else if (vizFunc === 'phi') vals.push(euler_phi(n));
    else if (vizFunc === 'tau') vals.push(tau(n));
    else vals.push(sigma(n));
  }

  const maxV = Math.max(...vals.map(Math.abs), 1);
  const minV = Math.min(...vals);
  const cols = { mu:'#f87171', phi:'#a78bfa', tau:'#60a5fa', sigma:'#34d399' };
  const col = cols[vizFunc];

  const barW = (W - 40) / N;
  const zeroY = minV < 0 ? H * 0.65 : H - 30;

  // 0선
  ctx.strokeStyle = '#334155'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(20, zeroY); ctx.lineTo(W - 20, zeroY); ctx.stroke();

  for (let i = 0; i < N; i++) {
    const n = i + 1;
    const v = vals[i];
    const barH = Math.abs(v) / (maxV || 1) * (minV < 0 ? H * 0.55 : H - 50);
    const x = 20 + i * barW + 2;
    const w = barW - 4;
    const y = v >= 0 ? zeroY - barH : zeroY;

    ctx.fillStyle = isPrime(n) ? '#fbbf24' : col;
    ctx.globalAlpha = 0.85;
    ctx.beginPath();
    ctx.roundRect ? ctx.roundRect(x, y, w, barH, 3) : ctx.rect(x, y, w, barH);
    ctx.fill();
    ctx.globalAlpha = 1;

    // 값 텍스트
    ctx.fillStyle = '#e2e8f0';
    ctx.font = `bold ${barW > 22 ? 9 : 7}px sans-serif`;
    ctx.textAlign = 'center';
    if (v >= 0) ctx.fillText(v, x + w/2, Math.max(y - 2, 10));
    else        ctx.fillText(v, x + w/2, y + barH + 12);

    // n 레이블
    ctx.fillStyle = '#64748b';
    ctx.font = '9px sans-serif';
    ctx.fillText(n, x + w/2, H - 4);
  }

  // 소수 범례
  ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 10px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('● 소수', 24, 14);
}

// ══════════════════════════════════════════════════════════
//  TAB 2: 테이블
// ══════════════════════════════════════════════════════════
let tableBuilt = false;
function buildTable() {
  if (tableBuilt) return;
  tableBuilt = true;
  const tbody = document.getElementById('tableBody');
  for (let n = 1; n <= 50; n++) {
    const mu_v = mobius(n);
    const phi_v = euler_phi(n);
    const tau_v = tau(n);
    const sig_v = sigma(n);
    const prime = isPrime(n);
    const perfect = sig_v === 2 * n;

    let rowCls = '';
    let nCell = `<td class="td-n">${n}</td>`;
    if (prime) { rowCls = 'row-hi'; nCell = `<td class="td-n">🟢 ${n}</td>`; }
    if (perfect) { rowCls = 'row-hi'; nCell = `<td class="td-n">🌟 ${n}</td>`; }

    const muCls = mu_v > 0 ? 'mu-pos' : mu_v < 0 ? 'mu-neg' : 'mu-z';
    const muSym = mu_v > 0 ? '+1' : mu_v < 0 ? '-1' : '0';

    const tr = document.createElement('tr');
    tr.className = rowCls;
    tr.innerHTML = `
      ${nCell}
      <td style="color:#64748b;font-size:0.76rem;">${factStr(n)}</td>
      <td class="${muCls}">${muSym}</td>
      <td class="phi-v">${phi_v}</td>
      <td class="tau-v">${tau_v}</td>
      <td class="sig-v">${sig_v}</td>
    `;
    tr.onclick = () => showTableDetail(n);
    tbody.appendChild(tr);
  }
}

function showTableDetail(n) {
  const f = primeFactors(n);
  const mu_v = mobius(n);
  const phi_v = euler_phi(n);
  const tau_v = tau(n);
  const sig_v = sigma(n);
  const divs = [];
  for (let i = 1; i <= n; i++) if (n % i === 0) divs.push(i);

  const el = document.getElementById('tableDetail');
  el.style.display = 'block';
  el.innerHTML = `
    <b style="color:#fbbf24;">n = ${n} 상세</b> &nbsp; 소인수분해: ${factStr(n)}<br><br>
    <span class="mu-col">μ(${n}) = ${mu_v}</span> &nbsp;·&nbsp;
    <span class="phi-col">φ(${n}) = ${phi_v}</span> &nbsp;·&nbsp;
    <span class="tau-col">τ(${n}) = ${tau_v}</span> &nbsp;·&nbsp;
    <span class="sig-col">σ(${n}) = ${sig_v}</span><br><br>
    약수: ${divs.map(d=>`<span style="color:#93c5fd">${d}</span>`).join(' + ')} = <b style="color:#34d399">${sig_v}</b>
  `;
}

// ══════════════════════════════════════════════════════════
//  TAB 3: 퀴즈 게임
// ══════════════════════════════════════════════════════════
let gameState = {
  score: 0, lives: 3, streak: 0, qNum: 0, total: 15,
  active: false, answered: false,
  curQ: null,
};

function makeQuestion() {
  const types = ['mu','phi','tau','sigma','formula_match','reverse_tau','reverse_sigma'];
  const type = types[Math.floor(Math.random() * types.length)];
  const n = Math.floor(Math.random() * 24) + 2; // 2~25

  let q, correct, choices = [], explain = '';

  if (type === 'mu') {
    correct = mobius(n);
    const opts = new Set([correct]);
    [-1, 0, 1].forEach(v => opts.add(v));
    choices = [...opts];
    q = `μ(${n}) = ?`;
    explain = `${n} = ${factStr(n)}<br>` +
      (Object.values(primeFactors(n)).some(e=>e>=2)
        ? `제곱인수가 있으므로 μ(${n}) = <b>0</b>`
        : `서로 다른 소인수 ${Object.keys(primeFactors(n)).length}개 → (-1)^${Object.keys(primeFactors(n)).length} = <b>${correct}</b>`);
    return { q, q2: `( n = ${factStr(n)} )`, type: 'int', correct, choices: shuffle(choices), explain };
  }

  if (type === 'phi') {
    correct = euler_phi(n);
    choices = genNearChoices(correct, 4, 1, n);
    q = `φ(${n}) = ?`;
    const ps = Object.keys(primeFactors(n));
    explain = `φ(${n}) = ${n}` + (ps.length ? ` × ` + ps.map(p=>`(1-1/${p})`).join('×') : '') + ` = <b>${correct}</b>`;
    return { q, q2: `( n = ${factStr(n)} )`, type: 'int', correct, choices, explain };
  }

  if (type === 'tau') {
    correct = tau(n);
    choices = genNearChoices(correct, 4, 1, 12);
    q = `τ(${n}) = ?`;
    const divs = [];
    for (let i=1;i<=n;i++) if(n%i===0) divs.push(i);
    explain = `약수: ${divs.join(', ')} → 개수 = <b>${correct}</b>`;
    return { q, q2: `( n = ${factStr(n)} )`, type: 'int', correct, choices, explain };
  }

  if (type === 'sigma') {
    correct = sigma(n);
    choices = genNearChoices(correct, 4, 1, n*3);
    q = `σ(${n}) = ?`;
    const divs = [];
    for (let i=1;i<=n;i++) if(n%i===0) divs.push(i);
    explain = `${divs.join(' + ')} = <b>${correct}</b>`;
    return { q, q2: `( n = ${factStr(n)} )`, type: 'int', correct, choices, explain };
  }

  if (type === 'formula_match') {
    const formulas = [
      { expr: '1/ζ(s)', func: 'μ(n)', desc: '뫼비우스 함수' },
      { expr: 'ζ(s-1)/ζ(s)', func: 'φ(n)', desc: '오일러 파이 함수' },
      { expr: '[ζ(s)]²', func: 'τ(n)', desc: '약수 개수 함수' },
      { expr: 'ζ(s)·ζ(s-1)', func: 'σ(n)', desc: '약수 합 함수' },
    ];
    const chosen = formulas[Math.floor(Math.random() * formulas.length)];
    correct = chosen.func;
    choices = shuffle(formulas.map(f => f.func));
    q = `Σ f(n)/nˢ = ${chosen.expr} 일 때, f(n) = ?`;
    explain = `${chosen.expr} = Σ <b>${chosen.func}</b>/nˢ<br>${chosen.desc}`;
    return { q, q2: '제타함수와 산술함수의 관계', type: 'str', correct, choices, explain };
  }

  if (type === 'reverse_tau') {
    // τ(n) = k 인 n 찾기 (소수 활용)
    const p = [2,3,5,7,11,13][Math.floor(Math.random()*6)];
    const target = 2;
    correct = p;
    const wrongs = [p*p, p+1, p*2].filter(x => tau(x) !== target && x !== p);
    choices = shuffle([correct, wrongs[0]||p+3, wrongs[1]||p*3, p*p]);
    choices = choices.slice(0, 4);
    q = `τ(n) = 2 가 되는 n의 예시는?`;
    explain = `τ(n) = 2 이면 약수가 1과 n뿐 → n은 <b>소수</b><br>τ(${p}) = 2 ✓`;
    return { q, q2: '약수 개수가 2인 수', type: 'int', correct, choices, explain };
  }

  // reverse_sigma: 완전수 찾기
  {
    const perfect_nums = [6, 28, 496];
    const np = perfect_nums[Math.floor(Math.random() * perfect_nums.length)];
    correct = np;
    choices = shuffle([np, np+1, np-1, np+6]);
    q = `σ(n) = 2n 을 만족하는 '완전수'는?`;
    explain = `σ(${np}) = ${sigma(np)} = 2×${np} ✓<br>완전수: 자기 자신을 제외한 약수의 합 = 자신`;
    return { q, q2: 'σ(n) = 2n 인 수', type: 'int', correct, choices, explain };
  }
}

function genNearChoices(correct, n, lo, hi) {
  const s = new Set([correct]);
  let tries = 0;
  while (s.size < n && tries < 200) {
    const delta = Math.floor(Math.random() * 8) - 4;
    const v = correct + delta;
    if (v >= lo && v <= hi && v !== correct) s.add(v);
    tries++;
  }
  // 만약 부족하면 임의값 추가
  let k = lo;
  while (s.size < n) { if (!s.has(k)) s.add(k); k++; }
  return shuffle([...s]).slice(0, n);
}

function shuffle(a) {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
}

function startGame() {
  gameState = { score: 0, lives: 3, streak: 0, qNum: 0, total: 15, active: true, answered: false, curQ: null };
  document.getElementById('startBtn').style.display = 'none';
  document.getElementById('gameResult').style.display = 'none';
  updateScoreDisplay();
  askQ();
}

function askQ() {
  if (gameState.qNum >= gameState.total || gameState.lives <= 0) {
    endGame(); return;
  }
  gameState.curQ = makeQuestion();
  gameState.answered = false;

  document.getElementById('gameQ').textContent = gameState.curQ.q;
  document.getElementById('gameQ2').textContent = gameState.curQ.q2;
  document.getElementById('gameResult').style.display = 'none';
  document.getElementById('nextBtn').style.display = 'none';

  document.getElementById('qProgFill').style.width =
    (gameState.qNum / gameState.total * 100) + '%';

  const choicesEl = document.getElementById('gameChoices');
  choicesEl.innerHTML = '';
  gameState.curQ.choices.forEach(c => {
    const btn = document.createElement('button');
    btn.className = 'choice-btn';
    btn.textContent = c;
    btn.onclick = () => answer(c, btn);
    choicesEl.appendChild(btn);
  });
}

function answer(val, btn) {
  if (gameState.answered) return;
  gameState.answered = true;
  gameState.qNum++;
  const q = gameState.curQ;

  const correct = (String(val) === String(q.correct));

  document.querySelectorAll('.choice-btn').forEach(b => {
    b.disabled = true;
    if (String(b.textContent) === String(q.correct)) b.classList.add('correct');
  });
  if (!correct) btn.classList.add('wrong');

  const resEl = document.getElementById('gameResult');
  resEl.style.display = 'block';

  if (correct) {
    gameState.streak++;
    let bonus = gameState.streak >= 3 ? 20 : 10;
    gameState.score += bonus;
    resEl.innerHTML = `<span class="r-correct">✅ 정답!</span> ${bonus}점 획득${gameState.streak>=3?` 🔥 ${gameState.streak}연속 보너스!`:''}
      <br><span style="color:#94a3b8;font-size:0.82rem;">${q.explain}</span>`;
    showToast(gameState.streak >= 3 ? `🔥 ${gameState.streak}연속! 대단해!` : '✅ 정답!');
  } else {
    gameState.streak = 0;
    gameState.lives--;
    resEl.innerHTML = `<span class="r-wrong">❌ 틀렸어요!</span> 정답: <b>${q.correct}</b>
      <br><span style="color:#94a3b8;font-size:0.82rem;">${q.explain}</span>`;
    showToast('❌ 오답! 힌트를 확인하세요');
  }

  updateScoreDisplay();
  document.getElementById('nextBtn').style.display = 'inline-block';
  if (gameState.qNum >= gameState.total || gameState.lives <= 0)
    document.getElementById('nextBtn').textContent = '결과 보기 ▶';
}

function nextQ() {
  document.getElementById('nextBtn').style.display = 'none';
  if (gameState.qNum >= gameState.total || gameState.lives <= 0) { endGame(); return; }
  askQ();
}

function endGame() {
  document.getElementById('qProgFill').style.width = '100%';
  const total = gameState.total;
  const stars = gameState.score >= 120 ? '⭐⭐⭐' : gameState.score >= 80 ? '⭐⭐' : '⭐';
  document.getElementById('gameQ').textContent = '게임 종료!';
  document.getElementById('gameQ2').textContent = '';
  document.getElementById('gameChoices').innerHTML = '';
  document.getElementById('gameResult').style.display = 'block';
  document.getElementById('gameResult').innerHTML = `
    <div style="text-align:center;padding:10px;">
      <div class="stars">${stars}</div>
      <div style="font-size:1.6rem;font-weight:900;color:#fbbf24;margin:8px 0;">${gameState.score}점</div>
      <div style="color:#94a3b8;font-size:0.85rem;">${total}문제 중 정답 ${Math.round(gameState.score/10)}개 (보너스 포함)</div>
    </div>`;
  document.getElementById('startBtn').textContent = '🔄 다시 하기';
  document.getElementById('startBtn').style.display = 'inline-block';
  document.getElementById('nextBtn').style.display = 'none';
}

function updateScoreDisplay() {
  document.getElementById('scoreDisp').textContent = `점수: ${gameState.score}`;
  const lv = '❤️'.repeat(gameState.lives) + '🖤'.repeat(3 - gameState.lives);
  document.getElementById('livesDisp').textContent = lv;
  const sb = document.getElementById('streakDisp');
  if (gameState.streak >= 2) { sb.style.display='inline-block'; sb.textContent=`🔥 ${gameState.streak} 연속`; }
  else sb.style.display = 'none';
}

// ══════════════════════════════════════════════════════════
//  TAB 4: 디리클레 급수
// ══════════════════════════════════════════════════════════
function updateDirichlet() {
  const fn = document.getElementById('dsFunc').value;
  const s  = parseFloat(document.getElementById('dsSlider').value);
  const N  = parseInt(document.getElementById('dsN').value);

  let partial = 0;
  let terms = [];
  for (let n = 1; n <= N; n++) {
    let f;
    if (fn === 'mu') f = mobius(n);
    else if (fn === 'phi') f = euler_phi(n);
    else if (fn === 'tau') f = tau(n);
    else f = sigma(n);
    const term = f / Math.pow(n, s);
    partial += term;
    terms.push({ n, f, term, partial });
  }

  // 이론값 계산
  const z = zeta(s);
  const z1 = (s > 1) ? zeta(s - 1) : NaN;
  let theoretical = NaN;
  let theoLabel = '';
  if (fn === 'mu') { theoretical = 1/z; theoLabel = `1/ζ(${s}) ≈ ${(1/z).toFixed(6)}`; }
  else if (fn === 'phi') { theoretical = z1/z; theoLabel = `ζ(${s-1})/ζ(${s}) ≈ ${(z1/z).toFixed(6)}`; }
  else if (fn === 'tau') { theoretical = z*z; theoLabel = `[ζ(${s})]² ≈ ${(z*z).toFixed(6)}`; }
  else { theoretical = z * z1; theoLabel = `ζ(${s})·ζ(${s-1}) ≈ ${(z*z1).toFixed(6)}`; }

  const err = Math.abs(partial - theoretical) / Math.abs(theoretical) * 100;
  document.getElementById('dsResult').innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:0.83rem;">
      <div class="vcard vcard-tau" style="text-align:center;">
        <div style="color:#64748b;font-size:0.75rem;">부분합 (N=${N}항)</div>
        <div style="font-size:1.3rem;font-weight:900;color:#60a5fa;">${partial.toFixed(6)}</div>
      </div>
      <div class="vcard vcard-sig" style="text-align:center;">
        <div style="color:#64748b;font-size:0.75rem;">이론값 (N→∞)</div>
        <div style="font-size:1.3rem;font-weight:900;color:#34d399;">${isNaN(theoretical) ? 'N/A' : theoretical.toFixed(6)}</div>
        <div style="font-size:0.72rem;color:#64748b;">${theoLabel}</div>
      </div>
      <div class="vcard vcard-phi" style="text-align:center;">
        <div style="color:#64748b;font-size:0.75rem;">오차율</div>
        <div style="font-size:1.3rem;font-weight:900;color:#a78bfa;">${isNaN(err) ? 'N/A' : err.toFixed(3) + '%'}</div>
      </div>
    </div>`;

  drawDirichletCanvas(terms, theoretical, fn);
  drawTermList(terms, fn);
}

function drawDirichletCanvas(terms, theoretical, fn) {
  const cv = document.getElementById('cvDirichlet');
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);

  const cols = { mu:'#f87171', phi:'#a78bfa', tau:'#60a5fa', sigma:'#34d399' };
  const col = cols[fn];

  const partials = terms.map(t => t.partial);
  const minV = Math.min(...partials, isNaN(theoretical) ? Infinity : theoretical);
  const maxV = Math.max(...partials, isNaN(theoretical) ? -Infinity : theoretical);
  const range = maxV - minV || 1;

  const px = (n) => 30 + (n / terms.length) * (W - 50);
  const py = (v) => H - 20 - ((v - minV) / range) * (H - 40);

  // 이론값 선
  if (!isNaN(theoretical)) {
    ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 1.5; ctx.setLineDash([5, 4]);
    ctx.beginPath(); ctx.moveTo(30, py(theoretical)); ctx.lineTo(W-10, py(theoretical)); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 10px sans-serif'; ctx.textAlign = 'right';
    ctx.fillText('이론값', W - 12, py(theoretical) - 4);
  }

  // 수렴 곡선
  ctx.strokeStyle = col; ctx.lineWidth = 2.5; ctx.setLineDash([]);
  ctx.beginPath();
  terms.forEach((t, i) => {
    const x = px(i+1), y = py(t.partial);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();

  // 점
  terms.forEach((t, i) => {
    const x = px(i+1), y = py(t.partial);
    ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, 3, 0, 2*Math.PI); ctx.fill();
  });

  // 축
  ctx.fillStyle = '#64748b'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText('n →', W - 20, H - 4);
  ctx.fillStyle = '#94a3b8'; ctx.font = '9px sans-serif';
  ctx.fillText(`수렴 과정 (s=${document.getElementById('dsSlider').value})`, W/2, 14);
}

function drawTermList(terms, fn) {
  const cols = { mu:'#f87171', phi:'#a78bfa', tau:'#60a5fa', sigma:'#34d399' };
  const col = cols[fn];
  let html = `<div style="overflow-x:auto;max-height:200px;overflow-y:auto;">
    <table class="t" style="font-size:0.76rem;">
      <thead><tr>
        <th>n</th><th>소인수분해</th>
        <th style="color:${col}">f(n)</th>
        <th>f(n)/nˢ</th>
        <th>부분합</th>
      </tr></thead><tbody>`;
  terms.slice(0, 30).forEach(t => {
    html += `<tr>
      <td class="td-n">${t.n}</td>
      <td style="color:#64748b;font-size:0.72rem;">${factStr(t.n)}</td>
      <td style="color:${col};font-weight:700;">${t.f}</td>
      <td style="color:#94a3b8;">${t.term.toFixed(6)}</td>
      <td style="color:#fbbf24;">${t.partial.toFixed(6)}</td>
    </tr>`;
  });
  html += '</tbody></table></div>';
  document.getElementById('dsTermList').innerHTML = html;
}

function updateConv() {
  const s = parseFloat(document.getElementById('convS').value);
  const cv = document.getElementById('cvConv');
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);

  const N = 30;
  const vals = Array.from({length:N}, (_,i)=>1/Math.pow(i+1,s));
  const maxV = vals[0];
  const bw = (W - 40) / N;

  vals.forEach((v, i) => {
    const bh = v / maxV * (H - 30);
    const x = 20 + i * bw + 1;
    const w = bw - 2;
    const y = H - 20 - bh;
    ctx.fillStyle = `hsl(${200 + i*3},70%,55%)`;
    ctx.globalAlpha = 0.85;
    ctx.fillRect(x, y, w, bh);
    ctx.globalAlpha = 1;
    if (i < 10) {
      ctx.fillStyle = '#e2e8f0';
      ctx.font = '8px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText((i+1), x+w/2, H-5);
    }
  });

  ctx.fillStyle = '#94a3b8'; ctx.font = '10px sans-serif'; ctx.textAlign = 'left';
  ctx.fillText(`s = ${s}일 때 1/nˢ 값 (n=1~30)`, 22, 14);
  if (s === 1) {
    ctx.fillStyle = '#f87171'; ctx.font = 'bold 10px sans-serif';
    ctx.fillText('⚠ s=1: 조화급수 → 발산!', 22, 30);
  }
}

// ══════════════════════════════════════════════════════════
//  토스트
// ══════════════════════════════════════════════════════════
let toastTimer;
function showToast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 1800);
}

// ══════════════════════════════════════════════════════════
//  초기화
// ══════════════════════════════════════════════════════════
window.onload = () => {
  updateN(12);
  drawBarChart();
  updateConv();
};
</script>
</body>
</html>
"""

def render():
    st.title("⚡ 미니: 제타함수와 산술함수의 관계")
    st.caption("μ(n), φ(n), τ(n), σ(n)이 ζ(s)와 어떻게 연결되는지 탐구합니다.")
    components.html(HTML, height=1500, scrolling=True)
