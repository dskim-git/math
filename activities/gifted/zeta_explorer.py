import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 리만 제타함수 탐험",
    "description": "조화급수에서 리만 제타함수까지 — 짝수와 홀수의 비밀, 그리고 리만 가설을 탐험합니다.",
    "order": 13,
    "hidden": True,
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans KR', sans-serif; background: #f8fafc; color: #1e293b; }
#app { max-width: 960px; margin: 0 auto; padding: 12px; }
h2 { font-size: 1.25rem; font-weight: 700; margin-bottom: 4px; }

/* ── 탭 ── */
.tab-row { display: flex; gap: 5px; margin-bottom: 12px; flex-wrap: wrap; }
.tab-btn {
  padding: 6px 13px; border-radius: 10px; border: 1.5px solid #e2e8f0;
  background: #f8fafc; font-size: 0.82rem; font-weight: 600;
  cursor: pointer; color: #64748b; transition: all .15s;
}
.tab-btn.active { background: #6366f1; color: #fff; border-color: #6366f1; }
.tab-btn:hover:not(.active) { background: #eef2ff; border-color: #a5b4fc; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }

/* ── 카드 ── */
.card { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 14px; margin-bottom: 10px; }
.card h3 { font-size: 0.97rem; font-weight: 700; margin-bottom: 8px; }

/* ── 버튼 ── */
button {
  padding: 6px 14px; border-radius: 8px; border: none;
  font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all .15s;
}
button:active { transform: translateY(1px); }
.btn-primary { background: #6366f1; color: #fff; }
.btn-primary:hover { background: #4f46e5; }
.btn-green { background: #10b981; color: #fff; }
.btn-green:hover { background: #059669; }
.btn-reset { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
.btn-reset:hover { background: #fecaca; }

/* ═══════════════════════════════
   TAB 1: 급수 탐험
═══════════════════════════════ */
.ctrl-bar { display: flex; gap: 7px; flex-wrap: wrap; align-items: center; margin: 8px 0; }
.series-info { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 8px 0; }
.s-card { border-radius: 12px; padding: 10px 14px; border: 2px solid; }
.harm-card  { border-color: #ef4444; background: #fff5f5; }
.basel-card { border-color: #3b82f6; background: #eff6ff; }
.s-card .sc-label { font-size: 0.82rem; font-weight: 700; margin-bottom: 3px; }
.s-card .sc-val   { font-size: 1.4rem; font-weight: 900; font-family: monospace; }
.harm-card  .sc-label, .harm-card  .sc-val { color: #dc2626; }
.basel-card .sc-label, .basel-card .sc-val { color: #2563eb; }
.s-card .sc-note { font-size: 0.73rem; margin-top: 2px; }
.harm-card  .sc-note { color: #dc2626; }
.basel-card .sc-note { color: #2563eb; }
#cvWrap { background: #0f172a; border-radius: 12px; padding: 10px; }
canvas { display: block; }
.cv-legend { font-size: 0.75rem; color: #94a3b8; text-align: center; margin-top: 5px; }

/* ═══════════════════════════════
   TAB 2: 제타 탐험기
═══════════════════════════════ */
.slider-wrap { margin: 10px 0; }
.slider-wrap label { font-size: 0.9rem; font-weight: 700; display: block; margin-bottom: 6px; }
input[type=range] { width: 100%; cursor: pointer; }
.zeta-result {
  text-align: center; padding: 18px; border-radius: 14px;
  background: linear-gradient(135deg, #1e293b, #334155); color: white; margin: 10px 0;
}
.zeta-result .zr-label { font-size: 0.85rem; opacity: .65; margin-bottom: 4px; }
.zeta-result .zr-num   { font-size: 2rem; font-weight: 900; font-family: monospace; color: #a5f3fc; }
.zeta-result .zr-exact { font-size: 1.05rem; margin-top: 6px; }
.even-badge { color: #fbbf24; font-weight: 700; }
.odd-badge  { color: #f87171; }

.zt { width: 100%; border-collapse: collapse; font-size: 0.84rem; }
.zt th { background: #6366f1; color: #fff; padding: 7px 10px; text-align: center; }
.zt td { padding: 6px 10px; border-bottom: 1px solid #e2e8f0; text-align: center; }
.zt tr.tr-even td { font-weight: 700; color: #1d4ed8; }
.zt tr.tr-odd  td { color: #64748b; }
.zt tr.tr-hi   td { background: #fef3c7 !important; font-weight: 700; }

/* ═══════════════════════════════
   TAB 3: 퀴즈
═══════════════════════════════ */
.quiz-hdr { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.score-badge {
  background: #6366f1; color: #fff; border-radius: 20px;
  padding: 3px 12px; font-size: 0.83rem; font-weight: 700;
}
.qprog { height: 7px; background: #e2e8f0; border-radius: 4px; margin-bottom: 10px; overflow: hidden; }
.qprog-fill { height: 100%; background: #6366f1; border-radius: 4px; transition: width .4s; }
.qcard {
  background: linear-gradient(135deg, #1e1b4b, #312e81);
  border-radius: 16px; padding: 20px; text-align: center; color: #fff; margin-bottom: 12px;
}
.qcard .qt { font-size: 0.87rem; opacity: .7; margin-bottom: 6px; }
.qcard .qv { font-size: 2rem; font-weight: 900; font-family: monospace; color: #a5f3fc; }
.choices { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.cho-btn {
  padding: 10px; border-radius: 12px; background: #fff; border: 2px solid #e2e8f0;
  font-size: 0.93rem; font-family: 'Courier New', monospace; font-weight: 600;
  cursor: pointer; transition: all .2s; color: #1e293b;
}
.cho-btn:hover:not(:disabled) { border-color: #6366f1; background: #eef2ff; }
.cho-btn.correct { background: #dcfce7; border-color: #16a34a; color: #15803d; }
.cho-btn.wrong   { background: #fee2e2; border-color: #dc2626; color: #dc2626; }
.qfb {
  text-align: center; padding: 9px; border-radius: 10px; margin-top: 8px;
  font-size: 0.9rem; font-weight: 700;
}
.qfb.ok  { background: #dcfce7; color: #15803d; }
.qfb.bad { background: #fee2e2; color: #dc2626; }

/* ═══════════════════════════════
   TAB 4: 리만 가설
═══════════════════════════════ */
#gWrap { background: #0f172a; border-radius: 12px; padding: 10px; }
.rinfo { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
.rtile { border-radius: 12px; padding: 12px 14px; border: 2px solid; }
.rtile-t { border-color: #f59e0b; background: #fffbeb; }
.rtile-n { border-color: #8b5cf6; background: #f5f3ff; }
.rtile .rt-title { font-size: 0.85rem; font-weight: 700; margin-bottom: 5px; }
.rtile-t .rt-title { color: #d97706; }
.rtile-n .rt-title { color: #7c3aed; }
.rtile p { font-size: 0.81rem; line-height: 1.55; color: #475569; }
.mil-badge {
  background: linear-gradient(135deg, #f59e0b, #ef4444); color: #fff;
  border-radius: 10px; padding: 10px 14px; text-align: center;
  font-size: 0.88rem; font-weight: 700; margin-top: 8px;
}

@media (max-width: 520px) {
  .series-info, .rinfo, .choices { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<div id="app">
  <h2>🔢 리만 제타함수 탐험</h2>
  <p style="font-size:0.82rem;color:#64748b;margin-bottom:10px;">
    조화급수에서 리만 가설까지 — 숫자 속에 숨은 π의 비밀을 함께 탐험해요!
  </p>

  <div class="tab-row">
    <button class="tab-btn active" onclick="showTab('series',this)">① 급수 탐험</button>
    <button class="tab-btn" onclick="showTab('calc',this)">② 제타 탐험기</button>
    <button class="tab-btn" onclick="showTab('quiz',this)">③ π 퀴즈</button>
    <button class="tab-btn" onclick="showTab('riemann',this)">④ 리만 가설</button>
    <button class="tab-btn" onclick="showTab('euler',this)">⑤ 오일러 곱</button>
  </div>

  <!-- ═══════════════════════════════════════════
       TAB 1: 급수 탐험
  ═══════════════════════════════════════════ -->
  <div id="tab-series" class="tab-panel active">
    <div class="card">
      <h3>📊 두 급수를 비교해보자!</h3>
      <p style="font-size:0.81rem;color:#64748b;margin-bottom:6px;">
        1부터 차례로 더해갈 때, 어떤 급수는 무한히 커지고 어떤 급수는 어느 값에 가까워집니다.
        항을 추가하면서 두 급수의 차이를 느껴보세요!
      </p>
      <div class="ctrl-bar">
        <button class="btn-primary" onclick="addTerms(1)">+ 1항 추가</button>
        <button class="btn-primary" onclick="addTerms(10)">+ 10항 추가</button>
        <button class="btn-primary" onclick="addTerms(100)">+ 100항 추가</button>
        <button class="btn-reset" onclick="resetSeries()">초기화</button>
        <span id="termCount" style="font-size:0.84rem;font-weight:700;color:#475569;">n = 0</span>
      </div>
      <div class="series-info">
        <div class="s-card harm-card">
          <div class="sc-label">조화급수 (s = 1)</div>
          <div class="sc-val" id="harmVal">0</div>
          <div class="sc-note">→ ∞ 발산!</div>
        </div>
        <div class="s-card basel-card">
          <div class="sc-label">바젤 급수 ζ(2)</div>
          <div class="sc-val" id="baselVal">0</div>
          <div class="sc-note">→ π²/6 ≈ 1.6449 수렴</div>
        </div>
      </div>
      <div id="cvWrap">
        <canvas id="cv1"></canvas>
      </div>
      <div class="cv-legend">빨간: 조화급수 &nbsp;|&nbsp; 파란: 바젤급수 (ζ(2)) &nbsp;|&nbsp; 점선: π²/6 ≈ 1.6449</div>
    </div>
    <div class="card">
      <h3>💡 왜 이렇게 다를까?</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.82rem;">
        <div style="padding:10px;background:#fff5f5;border-radius:10px;border:1px solid #fecaca;">
          <b style="color:#dc2626;">조화급수 (발산)</b><br>
          1 + 1/2 + 1/3 + 1/4 + …<br><br>
          더하는 값이 <b>천천히</b> 줄어서 결국 무한대!
        </div>
        <div style="padding:10px;background:#eff6ff;border-radius:10px;border:1px solid #bfdbfe;">
          <b style="color:#2563eb;">바젤 급수 (수렴)</b><br>
          1 + 1/4 + 1/9 + 1/16 + …<br><br>
          더하는 값이 <b>빠르게</b> 줄어서 π²/6에 수렴!
        </div>
      </div>
      <div style="margin-top:8px;padding:10px;background:#f0fdf4;border-radius:10px;border:1px solid #86efac;font-size:0.82rem;">
        💬 <b>생각해보기:</b> 조화급수의 처음 100개 항을 더하면 얼마나 될까요?
        얼마나 더해야 10을 넘을 수 있을까요? (실제로 엄청나게 많이 필요해요!)
      </div>
    </div>
  </div>

  <!-- ═══════════════════════════════════════════
       TAB 2: 제타 탐험기
  ═══════════════════════════════════════════ -->
  <div id="tab-calc" class="tab-panel">
    <div class="card">
      <h3>🔭 ζ(s) 탐험기</h3>
      <p style="font-size:0.81rem;color:#64748b;margin-bottom:8px;">
        s를 조절하며 ζ(s) = 1 + 1/2ˢ + 1/3ˢ + 1/4ˢ + ⋯ 값을 탐험해보세요.
        짝수와 홀수에서 어떤 차이가 나타날까요?
      </p>
      <div class="slider-wrap">
        <label>s = <span id="sVal" style="color:#6366f1;font-size:1.1rem;">2</span></label>
        <input type="range" min="2" max="10" step="1" value="2" id="sSlider" oninput="updateZeta()">
      </div>
      <div class="zeta-result">
        <div class="zr-label" id="zrLabel">ζ(2) =</div>
        <div class="zr-num" id="zrNum">1.644934</div>
        <div class="zr-exact" id="zrExact">
          <span class="even-badge">✨ 닫힌 꼴: π² / 6</span>
        </div>
      </div>
      <p style="font-size:0.77rem;color:#94a3b8;text-align:center;margin-bottom:8px;">
        (10,000항 부분합 — 실제 값에 매우 가깝게 수렴)
      </p>
    </div>
    <div class="card">
      <h3>📋 ζ(s) 값 표 — 패턴을 찾아보세요!</h3>
      <table class="zt">
        <thead>
          <tr><th>s</th><th>ζ(s) 근삿값</th><th>닫힌 꼴 표현</th></tr>
        </thead>
        <tbody id="ztBody"></tbody>
      </table>
      <div style="margin-top:8px;padding:10px;background:#fef9c3;border-radius:10px;border:1px solid #fde68a;font-size:0.82rem;">
        💡 <b>발견!</b> 짝수에서는 π가 나타나지만, 홀수에서는 닫힌 꼴이 없습니다.
        ζ(3) ≈ 1.20206은 "<b>아페리 상수</b>"라 불리며, 아직도 완전히 이해되지 않은 수입니다!
      </div>
    </div>
  </div>

  <!-- ═══════════════════════════════════════════
       TAB 3: π 퀴즈
  ═══════════════════════════════════════════ -->
  <div id="tab-quiz" class="tab-panel">
    <div class="card">
      <div class="quiz-hdr">
        <h3>🎯 짝수의 비밀 — π 퀴즈!</h3>
        <span class="score-badge" id="scoreDisp">0 / 0</span>
      </div>
      <p style="font-size:0.81rem;color:#64748b;margin-bottom:8px;">
        짝수 s에 대해 ζ(s)는 π의 거듭제곱 식으로 표현됩니다. 올바른 식을 골라보세요!
      </p>
      <div class="qprog"><div class="qprog-fill" id="qpFill" style="width:0%"></div></div>
      <div class="qcard">
        <div class="qt" id="qText">ζ(2) 의 닫힌 꼴은?</div>
        <div class="qv" id="qVal">ζ(2) ≈ 1.6449</div>
      </div>
      <div class="choices" id="choicesGrid"></div>
      <div class="qfb" id="qfb" style="display:none;"></div>
      <div style="text-align:center;margin-top:10px;display:flex;gap:8px;justify-content:center;">
        <button class="btn-primary" id="nextBtn" onclick="nextQ()" style="display:none;">다음 문제 →</button>
        <button class="btn-green" id="restartBtn" onclick="startQuiz()" style="display:none;">🔄 다시 도전!</button>
      </div>
    </div>
    <div class="card">
      <h3>📐 공식 패턴</h3>
      <div style="overflow-x:auto;">
        <table class="zt">
          <thead><tr><th>s (짝수)</th><th>ζ(s) 닫힌 꼴</th><th>분모 패턴</th></tr></thead>
          <tbody>
            <tr><td>2</td><td>π² / 6</td><td>6 = 2·3</td></tr>
            <tr><td>4</td><td>π⁴ / 90</td><td>90 = 2·3²·5</td></tr>
            <tr><td>6</td><td>π⁶ / 945</td><td>945 = 3³·5·7</td></tr>
            <tr><td>8</td><td>π⁸ / 9450</td><td>9450 = 2·3³·5²·7</td></tr>
            <tr><td>10</td><td>π¹⁰ / 93555</td><td>93555 = 3·5·7·11·...(베르누이 수 관련)</td></tr>
          </tbody>
        </table>
      </div>
      <p style="font-size:0.79rem;color:#64748b;margin-top:6px;">
        분모의 패턴이 복잡해 보이지만, 사실 <b>베르누이 수(Bernoulli numbers)</b>라는 특별한 수열로 통일되게 표현됩니다.
      </p>
    </div>
  </div>

  <!-- ═══════════════════════════════════════════
       TAB 4: 리만 가설
  ═══════════════════════════════════════════ -->
  <div id="tab-riemann" class="tab-panel">
    <div class="card">
      <h3>🌌 제타함수의 확장 — 실수 전체로!</h3>
      <p style="font-size:0.81rem;color:#64748b;margin-bottom:8px;">
        수학자들은 ζ(s)를 s &gt; 1의 범위를 넘어 모든 실수, 나아가 복소수까지 확장했습니다.
      </p>
      <div id="gWrap"><canvas id="gv"></canvas></div>
      <div class="cv-legend" style="margin-top:5px;">
        녹색: 수렴 영역 (s &gt; 1) &nbsp;|&nbsp; 보라: 해석적 연속 (s ≤ 0) &nbsp;|&nbsp;
        주황 점: 자명한 영점 (s = -2, -4, -6, ...) &nbsp;|&nbsp; 빨간 점선: s = 1 (극점, ∞)
      </div>
    </div>
    <div class="rinfo">
      <div class="rtile rtile-t">
        <div class="rt-title">🟠 자명한 영점 (Trivial Zeros)</div>
        <p>
          ζ(s) = 0이 되는 점 중 이해하기 쉬운 것들:<br>
          <b>s = -2, -4, -6, -8, …</b><br>
          (음의 짝수에서 모두 0이 됩니다)
        </p>
      </div>
      <div class="rtile rtile-n">
        <div class="rt-title">🟣 비자명 영점 (Non-trivial Zeros)</div>
        <p>
          복소수 영역으로 확장하면 더 신비로운 영점이 나타납니다!<br>
          첫 번째: <b>½ + 14.135i</b><br>
          이 영점들의 실수부는 모두 ½일까?
        </p>
      </div>
    </div>
    <div class="card" style="margin-top:0;">
      <h3>❓ 리만 가설이란?</h3>
      <p style="font-size:0.83rem;line-height:1.75;color:#475569;">
        1859년 베른하르트 리만은 ζ(s) = 0이 되는 "비자명 영점"들이 복소평면에서
        <b style="color:#7c3aed;">실수부 = ½</b>인 직선(임계선) 위에 모두 있다고 추측했습니다.<br><br>
        지금까지 컴퓨터로 계산한 <b>10조 개 이상의 영점</b>이 모두 이 직선 위에 있지만,
        아직 아무도 수학적으로 <b>완전히 증명하지 못했습니다!</b>
      </p>
      <div class="mil-badge">
        💰 클레이 수학연구소 "밀레니엄 난제" — 증명 시 상금 <b>$1,000,000 (약 13억 원)!</b>
      </div>
    </div>
    <div class="card">
      <h3>🔗 제타함수와 소수의 신비로운 연결</h3>
      <p style="font-size:0.83rem;line-height:1.75;color:#475569;">
        오일러 곱공식 (오일러가 발견!):
      </p>
      <div style="background:#1e293b;color:#f8fafc;border-radius:10px;padding:12px;font-family:monospace;text-align:center;font-size:1rem;margin:8px 0;">
        ζ(s) = <span style="color:#a5f3fc;">Σ 1/nˢ</span> = <span style="color:#fbbf24;">Π (소수 p에 대해) 1 / (1 - 1/pˢ)</span>
      </div>
      <p style="font-size:0.83rem;line-height:1.75;color:#475569;">
        이 공식 덕분에 ζ(s)의 영점이 소수의 분포와 직결됩니다.<br>
        리만 가설이 참이라면 <b>소수의 분포를 매우 정밀하게 예측</b>할 수 있습니다.
        소수의 비밀이 복소평면의 그 직선에 숨어 있는 것입니다! 🔑
      </p>
    </div>
  </div>

  <!-- ═══════════════════════════════════════════
       TAB 5: 오일러 곱공식
  ═══════════════════════════════════════════ -->
  <div id="tab-euler" class="tab-panel">
    <div class="card">
      <h3>✖️ 오일러 곱공식 — 소수가 ζ(s)를 만든다!</h3>
      <p style="font-size:0.81rem;color:#64748b;margin-bottom:8px;">
        ζ(s)는 놀랍게도 <b>소수들의 곱</b>으로 표현돼요! 소수를 하나씩 추가하며 ζ(s)에 가까워지는 과정을 관찰해보세요.
      </p>
      <div style="background:#1e293b;color:#f8fafc;border-radius:10px;padding:12px;font-family:monospace;text-align:center;font-size:0.9rem;margin:8px 0;line-height:2.2;">
        ζ(s) = <span style="color:#a5f3fc;">1/1<sup>s</sup> + 1/2<sup>s</sup> + 1/3<sup>s</sup> + …</span>
        &nbsp;=&nbsp;
        <span style="color:#fbbf24;">∏<sub>p 소수</sub> 1 / (1 − 1/p<sup>s</sup>)</span>
      </div>
      <div class="slider-wrap">
        <label>탐험할 s = <span id="eulerS" style="color:#f59e0b;font-size:1.15rem;">2</span></label>
        <input type="range" min="2" max="6" step="1" value="2" id="eulerSlider" oninput="onEulerSlider()">
        <div style="font-size:0.78rem;color:#94a3b8;margin-top:3px;">s=2 (π²/6) · s=3 (아페리 상수 ≈1.202) · s=4 (π⁴/90) · s=5 · s=6 (π⁶/945)</div>
      </div>
      <div class="ctrl-bar">
        <button class="btn-primary" onclick="addEulerPrime()">+ 소수 1개 추가</button>
        <button class="btn-green" onclick="addAllEulerPrimes()">20개까지 →</button>
        <button class="btn-reset" onclick="resetEuler()">초기화</button>
        <span id="eulerCountLabel" style="font-size:0.84rem;font-weight:700;color:#475569;">소수 0개</span>
      </div>
      <div class="series-info">
        <div class="s-card" style="border-color:#f59e0b;background:#fffbeb;">
          <div class="sc-label" style="color:#d97706;">부분 오일러 곱</div>
          <div class="sc-val" id="eulerProdVal" style="color:#d97706;">1.000000</div>
          <div class="sc-note" id="eulerPrimesNote" style="color:#d97706;">소수 없음</div>
        </div>
        <div class="s-card" style="border-color:#3b82f6;background:#eff6ff;">
          <div class="sc-label" style="color:#2563eb;">실제 ζ(<span id="eulerSSLabel">2</span>)</div>
          <div class="sc-val" id="eulerTrueVal" style="color:#2563eb;">1.644934</div>
          <div class="sc-note" id="eulerDiffNote" style="color:#2563eb;">차이: 0.644934</div>
        </div>
      </div>
      <div id="eulerCvWrap" style="background:#0f172a;border-radius:12px;padding:10px;">
        <canvas id="eulerCv"></canvas>
      </div>
      <div class="cv-legend">노란선: 부분 오일러 곱 수렴 과정 &nbsp;|&nbsp; 파란점선: ζ(s) 실제값 &nbsp;|&nbsp; 막대: 각 소수의 기여량</div>
    </div>

    <div class="card">
      <h3>🔬 왜 성립할까? — 등비급수와 소인수분해</h3>
      <p style="font-size:0.82rem;color:#475569;margin-bottom:6px;">
        소수 p &gt; 1이므로 0 &lt; 1/p<sup>s</sup> &lt; 1 → 등비급수 공식 적용 가능!
      </p>
      <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:10px;font-size:0.83rem;margin-bottom:8px;">
        <b style="color:#16a34a;">1 / (1 − 1/p<sup>s</sup>) = 1 + 1/p<sup>s</sup> + 1/p<sup>2s</sup> + 1/p<sup>3s</sup> + …</b>
      </div>
      <div style="overflow-x:auto;">
        <table class="zt">
          <thead><tr><th>소수 p</th><th>인수값 (s=2)</th><th>등비급수 전개</th><th>포함하는 수</th></tr></thead>
          <tbody id="eulerExpandTb"></tbody>
        </table>
      </div>
      <div id="eulerMagicDiv" style="display:none;margin-top:8px;padding:10px;background:#fef3c7;border-radius:10px;border:1px solid #fde68a;font-size:0.83rem;">
        <b>🪄 산술기본정리의 마법!</b><br>
        (p=2의 급수) × (p=3의 급수) = (1 + 1/4 + 1/16 + …) × (1 + 1/9 + 1/81 + …)<br>
        = 1 + 1/4 + 1/9 + 1/16 + 1/36 + 1/64 + … (2의 거듭제곱 × 3의 거듭제곱으로 만드는 수들)<br>
        모든 소수를 곱하면 → <b>모든 자연수 n의 1/n<sup>2</sup>이 정확히 한 번씩</b> 등장! (소인수분해의 유일성 덕분!)
      </div>
    </div>

    <div class="card">
      <h3>🎮 도전! 몇 개의 소수로 목표에 도달할까?</h3>
      <p style="font-size:0.81rem;color:#64748b;margin-bottom:8px;">
        ζ(2) ≈ 1.6449 값의 목표 비율에 도달하려면 소수가 <b>몇 개</b> 필요할지 예측해보세요!
      </p>
      <div class="ctrl-bar" style="align-items:center;flex-wrap:wrap;gap:6px;">
        <span style="font-size:0.85rem;font-weight:600;">목표:</span>
        <select id="eulerGoalPct" style="padding:5px 10px;border-radius:8px;border:1.5px solid #e2e8f0;font-size:0.85rem;cursor:pointer;background:#fff;">
          <option value="0.9">ζ(2)의 90%</option>
          <option value="0.95" selected>ζ(2)의 95%</option>
          <option value="0.99">ζ(2)의 99%</option>
          <option value="0.999">ζ(2)의 99.9%</option>
        </select>
        <input type="number" id="eulerGuessInput" min="1" max="50" placeholder="예측 개수"
          style="width:90px;padding:5px 8px;border-radius:8px;border:1.5px solid #e2e8f0;font-size:0.85rem;">
        <button class="btn-primary" onclick="checkEulerGuess()">확인!</button>
      </div>
      <div id="eulerGuessResult" style="display:none;margin-top:8px;padding:12px;border-radius:10px;text-align:center;font-size:0.9rem;font-weight:700;"></div>
    </div>
  </div>
</div>

<script>
// ─────────────────────────────────────────────
//  탭 전환
// ─────────────────────────────────────────────
function showTab(name, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  btn.classList.add('active');
  if (name === 'riemann') drawZetaGraph();
  if (name === 'series')  drawSeriesChart();
  if (name === 'euler')   drawEulerChart();
}

// ─────────────────────────────────────────────
//  ζ(s) 계산 (N항 부분합)
// ─────────────────────────────────────────────
function zetaSum(s, N) {
  let v = 0;
  for (let n = 1; n <= N; n++) v += Math.pow(n, -s);
  return v;
}

const PRECOMP = {
  2: 1.6449340668482, 3: 1.2020569031595, 4: 1.0823232337111,
  5: 1.0369277551433, 6: 1.0173430619844, 7: 1.0083492773819,
  8: 1.0040773561979, 9: 1.0020083928260, 10: 1.0009945751278,
};
const EXACT = {
  2: 'π² / 6', 4: 'π⁴ / 90', 6: 'π⁶ / 945',
  8: 'π⁸ / 9450', 10: 'π¹⁰ / 93555',
};

// ─────────────────────────────────────────────
//  TAB 1: 급수 탐험
// ─────────────────────────────────────────────
let hN = 0, hS = 0, bS = 0, hHist = [], bHist = [];
const TARGET = Math.PI * Math.PI / 6;

function addTerms(k) {
  for (let i = 0; i < k; i++) {
    hN++;
    hS += 1 / hN;
    bS += 1 / (hN * hN);
    if (hHist.length < 600) {
      hHist.push(Math.min(hS, 7));
      bHist.push(bS);
    }
  }
  document.getElementById('harmVal').textContent = hS.toFixed(4);
  document.getElementById('baselVal').textContent = bS.toFixed(6);
  document.getElementById('termCount').textContent = 'n = ' + hN;
  drawSeriesChart();
}

function resetSeries() {
  hN = 0; hS = 0; bS = 0; hHist = []; bHist = [];
  document.getElementById('harmVal').textContent = '0';
  document.getElementById('baselVal').textContent = '0';
  document.getElementById('termCount').textContent = 'n = 0';
  drawSeriesChart();
}

function drawSeriesChart() {
  const wrap = document.getElementById('cvWrap');
  const cv = document.getElementById('cv1');
  const dpr = window.devicePixelRatio || 1;
  const W = wrap.clientWidth - 20, H = 190;
  cv.width = W * dpr; cv.height = H * dpr;
  cv.style.width = W + 'px'; cv.style.height = H + 'px';
  const ctx = cv.getContext('2d');
  ctx.scale(dpr, dpr);

  const pL = 44, pR = 12, pT = 12, pB = 26;
  const w = W - pL - pR, h = H - pT - pB;
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, W, H);

  const maxY = hHist.length > 0 ? Math.max(Math.min(hS, 7), 2) : 2;
  const N = hHist.length;
  const toX = i => pL + (N > 1 ? i / (N - 1) : 0) * w;
  const toY = v => pT + h * (1 - v / maxY);

  // 격자
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1;
  for (let yv = 0; yv <= maxY; yv += 0.5) {
    const py = toY(yv);
    ctx.beginPath(); ctx.moveTo(pL, py); ctx.lineTo(pL + w, py); ctx.stroke();
    ctx.fillStyle = '#475569'; ctx.font = '10px monospace';
    ctx.textAlign = 'right'; ctx.fillText(yv.toFixed(1), pL - 3, py + 4);
  }

  // π²/6 점선
  const ty = toY(TARGET);
  if (ty >= pT && ty <= pT + h) {
    ctx.setLineDash([4, 3]); ctx.strokeStyle = '#60a5fa';
    ctx.lineWidth = 1.5; ctx.globalAlpha = 0.6;
    ctx.beginPath(); ctx.moveTo(pL, ty); ctx.lineTo(pL + w, ty); ctx.stroke();
    ctx.globalAlpha = 1; ctx.setLineDash([]);
    ctx.fillStyle = '#60a5fa'; ctx.font = '10px monospace';
    ctx.textAlign = 'left'; ctx.fillText('π²/6', pL + 4, ty - 3);
  }

  if (N < 2) {
    ctx.fillStyle = '#475569'; ctx.font = '13px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('항을 추가해보세요!', W / 2, H / 2);
    return;
  }

  // 조화급수 (빨간)
  ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2.5;
  ctx.beginPath();
  hHist.forEach((v, i) => {
    const x = toX(i), y = toY(v);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();

  // 바젤급수 (파란)
  ctx.strokeStyle = '#60a5fa'; ctx.lineWidth = 2.5;
  ctx.beginPath();
  bHist.forEach((v, i) => {
    const x = toX(i), y = toY(v);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();
}

// ─────────────────────────────────────────────
//  TAB 2: 제타 탐험기
// ─────────────────────────────────────────────
function updateZeta() {
  const s = parseInt(document.getElementById('sSlider').value);
  document.getElementById('sVal').textContent = s;
  const v = PRECOMP[s];
  document.getElementById('zrLabel').textContent = 'ζ(' + s + ') =';
  document.getElementById('zrNum').textContent = v.toFixed(6);
  const even = s % 2 === 0;
  document.getElementById('zrExact').innerHTML = even
    ? '<span class="even-badge">✨ 닫힌 꼴: ' + EXACT[s] + '</span>'
    : '<span class="odd-badge">🔒 홀수 s: 아직 닫힌 꼴이 없어요!</span>';

  document.querySelectorAll('#ztBody tr').forEach(tr => {
    tr.classList.toggle('tr-hi', parseInt(tr.dataset.s) === s);
  });
}

function buildTable() {
  const tb = document.getElementById('ztBody');
  tb.innerHTML = '';
  for (let s = 2; s <= 10; s++) {
    const v = PRECOMP[s];
    const even = s % 2 === 0;
    const tr = document.createElement('tr');
    tr.dataset.s = s;
    tr.className = even ? 'tr-even' : 'tr-odd';
    if (s === 2) tr.classList.add('tr-hi');
    tr.innerHTML = `<td>${s}${even ? ' ★' : ''}</td><td>${v.toFixed(6)}</td>` +
      `<td>${even ? EXACT[s] : '닫힌 꼴 없음 🔒'}</td>`;
    tb.appendChild(tr);
  }
}

// ─────────────────────────────────────────────
//  TAB 3: 퀴즈
// ─────────────────────────────────────────────
const QUESTIONS = [
  { s:2,  v:1.6449, correct:'π² / 6',      opts:['π² / 6','π² / 4','π² / 3','π / 6²'] },
  { s:4,  v:1.0823, correct:'π⁴ / 90',     opts:['π⁴ / 90','π⁴ / 45','π⁴ / 120','π² / 90'] },
  { s:6,  v:1.0173, correct:'π⁶ / 945',    opts:['π⁶ / 945','π⁶ / 480','π⁶ / 9450','π⁶ / 90'] },
  { s:8,  v:1.0041, correct:'π⁸ / 9450',   opts:['π⁸ / 945','π⁸ / 9450','π⁸ / 4725','π⁸ / 19440'] },
  { s:10, v:1.0010, correct:'π¹⁰ / 93555', opts:['π¹⁰ / 9450','π¹⁰ / 93555','π¹⁰ / 945²','π¹⁰ / 93500'] },
];
let qIdx = 0, qScore = 0, qAnswered = false, qList = [];

function shuffle(a) {
  const b = [...a];
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
}

function startQuiz() {
  qIdx = 0; qScore = 0; qAnswered = false;
  qList = shuffle(QUESTIONS);
  document.getElementById('nextBtn').style.display = 'none';
  document.getElementById('restartBtn').style.display = 'none';
  document.getElementById('qfb').style.display = 'none';
  document.getElementById('qpFill').style.width = '0%';
  updateScore();
  renderQ();
}

function renderQ() {
  qAnswered = false;
  const q = qList[qIdx];
  document.getElementById('qText').textContent = 'ζ(' + q.s + ') 의 닫힌 꼴은?';
  document.getElementById('qVal').textContent = 'ζ(' + q.s + ') ≈ ' + q.v.toFixed(4);
  document.getElementById('qfb').style.display = 'none';
  document.getElementById('nextBtn').style.display = 'none';
  document.getElementById('qpFill').style.width = (qIdx / qList.length * 100) + '%';

  const grid = document.getElementById('choicesGrid');
  grid.innerHTML = '';
  shuffle(q.opts).forEach(opt => {
    const btn = document.createElement('button');
    btn.className = 'cho-btn';
    btn.textContent = opt;
    btn.onclick = () => checkAns(opt, q.correct);
    grid.appendChild(btn);
  });
}

function checkAns(sel, correct) {
  if (qAnswered) return;
  qAnswered = true;
  const ok = sel === correct;
  if (ok) qScore++;
  document.querySelectorAll('.cho-btn').forEach(btn => {
    btn.disabled = true;
    if (btn.textContent === correct) btn.classList.add('correct');
    else if (btn.textContent === sel) btn.classList.add('wrong');
  });
  const fb = document.getElementById('qfb');
  fb.style.display = 'block';
  if (ok) {
    fb.className = 'qfb ok';
    fb.textContent = '🎉 정답! 정수들의 역수 합이 π로 표현된다니 신기하죠?';
  } else {
    fb.className = 'qfb bad';
    fb.textContent = '❌ 틀렸어요. 정답은 "' + correct + '" 입니다!';
  }
  updateScore();
  if (qIdx + 1 < qList.length) {
    document.getElementById('nextBtn').style.display = 'inline-block';
  } else {
    document.getElementById('qpFill').style.width = '100%';
    setTimeout(() => {
      const fb = document.getElementById('qfb');
      fb.style.display = 'block';
      if (qScore === qList.length) {
        fb.className = 'qfb ok';
        fb.textContent = '🏆 완벽! ' + qScore + '/' + qList.length + ' — 오일러도 깜짝 놀랄 실력!';
      } else {
        fb.className = 'qfb bad';
        fb.textContent = '최종 점수: ' + qScore + '/' + qList.length + ' — 다시 도전해봐요!';
      }
      document.getElementById('restartBtn').style.display = 'inline-block';
    }, 200);
  }
}

function nextQ() { qIdx++; document.getElementById('nextBtn').style.display = 'none'; renderQ(); }

function updateScore() {
  const attempted = qIdx + (qAnswered ? 1 : 0);
  document.getElementById('scoreDisp').textContent = qScore + ' / ' + attempted;
}

// ─────────────────────────────────────────────
//  TAB 4: 리만 그래프
// ─────────────────────────────────────────────
// 해석적 연속 값 (알려진 값들)
const ANALYTIC = [
  [-8,0],[-7,1/240],[-6,0],[-5,-1/252],[-4,0],[-3,1/120],[-2,0],[-1,-1/12],[0,-0.5],
];

function drawZetaGraph() {
  const wrap = document.getElementById('gWrap');
  const cv = document.getElementById('gv');
  const dpr = window.devicePixelRatio || 1;
  const W = wrap.clientWidth - 20, H = 210;
  cv.width = W * dpr; cv.height = H * dpr;
  cv.style.width = W + 'px'; cv.style.height = H + 'px';
  const ctx = cv.getContext('2d');
  ctx.scale(dpr, dpr);

  const pL = 44, pR = 14, pT = 16, pB = 28;
  const w = W - pL - pR, h = H - pT - pB;
  const sMin = -9, sMax = 10.5;
  const yMin = -2, yMax = 2.5;

  ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, W, H);

  const toX = s => pL + (s - sMin) / (sMax - sMin) * w;
  const toY = v => pT + (1 - (v - yMin) / (yMax - yMin)) * h;
  const clip = v => Math.max(yMin, Math.min(yMax, v));

  // 격자
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1;
  for (let yv = yMin; yv <= yMax; yv += 0.5) {
    const py = toY(yv);
    ctx.beginPath(); ctx.moveTo(pL, py); ctx.lineTo(pL + w, py); ctx.stroke();
    if (yv === Math.round(yv)) {
      ctx.fillStyle = '#475569'; ctx.font = '10px monospace';
      ctx.textAlign = 'right'; ctx.fillText(yv, pL - 3, py + 4);
    }
  }
  for (let sv = sMin; sv <= sMax; sv += 2) {
    const px = toX(sv);
    ctx.beginPath(); ctx.moveTo(px, pT); ctx.lineTo(px, pT + h); ctx.stroke();
    ctx.fillStyle = '#475569'; ctx.font = '10px monospace';
    ctx.textAlign = 'center'; ctx.fillText(sv, px, pT + h + 16);
  }

  // x축
  const y0 = toY(0);
  ctx.strokeStyle = '#64748b'; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(pL, y0); ctx.lineTo(pL + w, y0); ctx.stroke();

  // 수렴 영역 (s > 1.1): 녹색 실선
  ctx.strokeStyle = '#4ade80'; ctx.lineWidth = 2.5;
  ctx.beginPath();
  let started = false;
  for (let si = 110; si <= 1050; si += 5) {
    const s = si / 100;
    const v = clip(zetaSum(s, 2000));
    const x = toX(s), y = toY(v);
    if (!started) { ctx.moveTo(x, y); started = true; } else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // 해석적 연속 (s ≤ 0): 보라 점선
  ctx.setLineDash([5, 3]); ctx.strokeStyle = '#a78bfa'; ctx.lineWidth = 2;
  ctx.beginPath(); started = false;
  ANALYTIC.forEach(([s, v]) => {
    const x = toX(s), y = toY(clip(v));
    if (!started) { ctx.moveTo(x, y); started = true; } else ctx.lineTo(x, y);
  });
  ctx.stroke(); ctx.setLineDash([]);

  // s = 1 극점 (빨간 점선)
  const x1 = toX(1);
  ctx.setLineDash([3, 3]); ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(x1, pT); ctx.lineTo(x1, pT + h); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#ef4444'; ctx.font = '10px monospace'; ctx.textAlign = 'center';
  ctx.fillText('s=1 (∞)', x1, pT + 10);

  // 자명한 영점 (주황 점)
  [-2,-4,-6,-8].forEach(sz => {
    const x = toX(sz), y = toY(0);
    ctx.fillStyle = '#f59e0b';
    ctx.beginPath(); ctx.arc(x, y, 5.5, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#fde68a'; ctx.font = '9px monospace'; ctx.textAlign = 'center';
    ctx.fillText(sz, x, y - 8);
  });

  // ζ(0) = -1/2 표시
  const x0 = toX(0), y0v = toY(-0.5);
  ctx.fillStyle = '#c084fc';
  ctx.beginPath(); ctx.arc(x0, y0v, 4, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#c084fc'; ctx.font = '9px monospace'; ctx.textAlign = 'left';
  ctx.fillText('ζ(0)=-½', x0 + 4, y0v + 3);

  // 레이블
  ctx.fillStyle = '#4ade80'; ctx.font = '10px monospace'; ctx.textAlign = 'left';
  ctx.fillText('수렴 영역 (s>1)', toX(2), pT + 14);
  ctx.fillStyle = '#a78bfa';
  ctx.fillText('해석적 연속', toX(-8.5), pT + 14);
}

// ─────────────────────────────────────────────
//  TAB 5: 오일러 곱공식
// ─────────────────────────────────────────────
const PRIMES20 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71];
let eulerS = 2;
let eulerK = 0;
let eulerHistory = [1.0];

function eulerFactor(p, s) {
  return 1.0 / (1.0 - Math.pow(p, -s));
}

function eulerPartialProd(k, s) {
  let v = 1.0;
  for (let i = 0; i < k; i++) v *= eulerFactor(PRIMES20[i], s);
  return v;
}

function eulerRefreshDisplay() {
  const prod = eulerHistory[eulerK];
  const trueVal = PRECOMP[eulerS];
  document.getElementById('eulerProdVal').textContent = prod.toFixed(6);
  document.getElementById('eulerTrueVal').textContent = trueVal.toFixed(6);
  document.getElementById('eulerSSLabel').textContent = eulerS;
  document.getElementById('eulerDiffNote').textContent = '차이: ' + (trueVal - prod).toFixed(6);
  document.getElementById('eulerCountLabel').textContent = '소수 ' + eulerK + '개';
  document.getElementById('eulerPrimesNote').textContent =
    eulerK === 0 ? '소수 없음' : PRIMES20.slice(0, eulerK).join(', ');
  buildEulerTable();
  drawEulerChart();
}

function onEulerSlider() {
  eulerS = parseInt(document.getElementById('eulerSlider').value);
  document.getElementById('eulerS').textContent = eulerS;
  eulerHistory = [1.0];
  for (let i = 1; i <= eulerK; i++) eulerHistory.push(eulerPartialProd(i, eulerS));
  eulerRefreshDisplay();
}

function addEulerPrime() {
  if (eulerK >= PRIMES20.length) return;
  eulerK++;
  eulerHistory.push(eulerPartialProd(eulerK, eulerS));
  eulerRefreshDisplay();
}

function addAllEulerPrimes() {
  eulerK = 20;
  eulerHistory = [1.0];
  for (let i = 1; i <= 20; i++) eulerHistory.push(eulerPartialProd(i, eulerS));
  eulerRefreshDisplay();
}

function resetEuler() {
  eulerK = 0;
  eulerHistory = [1.0];
  const rDiv = document.getElementById('eulerGuessResult');
  if (rDiv) rDiv.style.display = 'none';
  eulerRefreshDisplay();
}

function buildEulerTable() {
  const tb = document.getElementById('eulerExpandTb');
  if (!tb) return;
  tb.innerHTML = '';
  const showK = Math.min(eulerK, 5);
  for (let i = 0; i < showK; i++) {
    const p = PRIMES20[i];
    const f = eulerFactor(p, 2);
    const tr = document.createElement('tr');
    const numsStr = [1, p, p*p, p*p*p].join(', ') + ', …';
    tr.innerHTML = `<td><b>${p}</b></td>
      <td style="font-weight:700;color:#7c3aed;">${f.toFixed(4)}</td>
      <td style="font-family:monospace;font-size:0.78rem;">1 + 1/${p}² + 1/${p*p}² + …</td>
      <td style="font-size:0.8rem;">${numsStr}</td>`;
    tb.appendChild(tr);
  }
  const magicDiv = document.getElementById('eulerMagicDiv');
  if (magicDiv) magicDiv.style.display = eulerK >= 2 ? 'block' : 'none';
}

function drawEulerChart() {
  const wrap = document.getElementById('eulerCvWrap');
  const cv = document.getElementById('eulerCv');
  if (!wrap || !cv) return;
  const dpr = window.devicePixelRatio || 1;
  const W = wrap.clientWidth - 20, H = 200;
  cv.width = W * dpr; cv.height = H * dpr;
  cv.style.width = W + 'px'; cv.style.height = H + 'px';
  const ctx = cv.getContext('2d');
  ctx.scale(dpr, dpr);

  const pL = 50, pR = 14, pT = 16, pB = 28;
  const w = W - pL - pR, h = H - pT - pB;
  ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, W, H);

  const trueVal = PRECOMP[eulerS];
  const yMin = 0.9, yMax = trueVal * 1.06;
  const N = eulerHistory.length;
  const toX = i => pL + (N > 1 ? i / (N - 1) : 0.5) * w;
  const toY = v => pT + (1 - (Math.min(v, yMax) - yMin) / (yMax - yMin)) * h;

  // 격자
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1;
  for (let yv = 0.9; yv <= yMax + 0.001; yv = Math.round((yv + 0.1) * 10) / 10) {
    const py = toY(yv);
    if (py < pT || py > pT + h) continue;
    ctx.beginPath(); ctx.moveTo(pL, py); ctx.lineTo(pL + w, py); ctx.stroke();
    ctx.fillStyle = '#475569'; ctx.font = '10px monospace'; ctx.textAlign = 'right';
    ctx.fillText(yv.toFixed(1), pL - 3, py + 4);
  }

  // 실제 ζ(s)값 점선
  const ty = toY(trueVal);
  if (ty >= pT && ty <= pT + h) {
    ctx.setLineDash([4, 3]); ctx.strokeStyle = '#60a5fa'; ctx.lineWidth = 1.5; ctx.globalAlpha = 0.7;
    ctx.beginPath(); ctx.moveTo(pL, ty); ctx.lineTo(pL + w, ty); ctx.stroke();
    ctx.globalAlpha = 1; ctx.setLineDash([]);
    ctx.fillStyle = '#60a5fa'; ctx.font = '10px monospace'; ctx.textAlign = 'left';
    ctx.fillText('ζ(' + eulerS + ')=' + trueVal.toFixed(4), pL + 4, ty - 3);
  }

  if (N < 2) {
    ctx.fillStyle = '#475569'; ctx.font = '13px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('소수를 추가해보세요!', W / 2, H / 2);
    return;
  }

  // 각 소수의 기여 막대
  const bw = Math.max(4, Math.min(w / (N + 1) * 0.6, 25));
  for (let i = 1; i < N; i++) {
    const x = toX(i);
    const y1 = toY(eulerHistory[i]);
    const y0 = toY(eulerHistory[i - 1]);
    ctx.fillStyle = `hsl(${180 + i * 28}, 70%, 60%)`;
    ctx.globalAlpha = 0.55;
    ctx.fillRect(x - bw / 2, Math.min(y1, y0), bw, Math.max(Math.abs(y1 - y0), 2));
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#94a3b8'; ctx.font = '9px monospace'; ctx.textAlign = 'center';
    ctx.fillText('p=' + PRIMES20[i - 1], x, pT + h + 15);
  }

  // 수렴 곡선 (노란)
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 2.5;
  ctx.beginPath();
  eulerHistory.forEach((v, i) => {
    const x = toX(i), y = toY(v);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();

  // 점
  eulerHistory.forEach((v, i) => {
    const x = toX(i), y = toY(v);
    ctx.fillStyle = '#fbbf24';
    ctx.beginPath(); ctx.arc(x, y, 4, 0, Math.PI * 2); ctx.fill();
  });
}

function checkEulerGuess() {
  const goalPct = parseFloat(document.getElementById('eulerGoalPct').value);
  const guess = parseInt(document.getElementById('eulerGuessInput').value);
  if (isNaN(guess) || guess < 1 || guess > 50) return;
  const target = PRECOMP[2] * goalPct;
  let needed = 0, prod = 1;
  for (let i = 0; i < PRIMES20.length; i++) {
    prod *= eulerFactor(PRIMES20[i], 2);
    needed++;
    if (prod >= target) break;
  }
  const res = document.getElementById('eulerGuessResult');
  res.style.display = 'block';
  const pctStr = (goalPct * 100) + '%';
  const diff = Math.abs(guess - needed);
  if (diff === 0) {
    res.style.cssText = 'display:block;padding:12px;border-radius:10px;text-align:center;font-size:0.9rem;font-weight:700;background:#dcfce7;color:#15803d;margin-top:8px;';
    res.innerHTML = '🎉 정답! 소수 <b>' + needed + '개</b> (2, 3, …, ' + PRIMES20[needed-1] + ')로 ζ(2)의 ' + pctStr + '에 도달!';
  } else if (diff <= 2) {
    res.style.cssText = 'display:block;padding:12px;border-radius:10px;text-align:center;font-size:0.9rem;font-weight:700;background:#fef9c3;color:#854d0e;margin-top:8px;';
    res.innerHTML = '😊 아깝! 정답은 <b>' + needed + '개</b>의 소수 (마지막: p=' + PRIMES20[needed-1] + ')입니다!';
  } else {
    res.style.cssText = 'display:block;padding:12px;border-radius:10px;text-align:center;font-size:0.9rem;font-weight:700;background:#fee2e2;color:#dc2626;margin-top:8px;';
    res.innerHTML = '❌ 정답은 <b>' + needed + '개</b>의 소수 (마지막: p=' + PRIMES20[needed-1] + ')! ' + (needed < guess ? '좀 더 적게' : '좀 더 많이') + ' 필요해요!';
  }
}

// ─────────────────────────────────────────────
//  초기화
// ─────────────────────────────────────────────
window.addEventListener('load', () => {
  buildTable();
  updateZeta();
  startQuiz();
  drawSeriesChart();
  eulerHistory = [1.0];
  buildEulerTable();
  drawEulerChart();
});
window.addEventListener('resize', () => {
  drawSeriesChart();
  if (document.getElementById('tab-riemann').classList.contains('active')) drawZetaGraph();
  if (document.getElementById('tab-euler').classList.contains('active')) drawEulerChart();
});
</script>
</body>
</html>
"""


def render():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] > .main { padding-top: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)
    components.html(HTML, height=1050, scrolling=True)
