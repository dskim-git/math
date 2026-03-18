import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 산술함수와 곱셈함수 탐구",
    "description": "τ(n), σ(n), φ(n), μ(n)을 직접 계산하고 곱셈함수의 신기한 성질을 탐구합니다.",
    "order": 12,
    "hidden": True,
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans KR', sans-serif; background: #f8fafc; color: #1e293b; }
#app { max-width: 960px; margin: 0 auto; padding: 12px; }
h2 { font-size: 1.25rem; font-weight: 700; margin-bottom: 6px; }

.tab-row { display: flex; gap: 5px; margin-bottom: 12px; flex-wrap: wrap; }
.tab-btn { padding: 6px 13px; border-radius: 10px; border: 1.5px solid #e2e8f0;
  background: #f8fafc; font-size: 0.82rem; font-weight: 600; cursor: pointer; color: #64748b; transition: all .15s; }
.tab-btn.active { background: #3b82f6; color: #fff; border-color: #3b82f6; }
.tab-btn:hover:not(.active) { background: #e0f2fe; border-color: #7dd3fc; }

.card { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 14px; margin-bottom: 10px; }
.card h3 { font-size: 0.97rem; font-weight: 700; margin-bottom: 8px; }

/* ── 함수 색상 ── */
.tau-color   { color: #1d4ed8; }
.sigma-color { color: #16a34a; }
.phi-color   { color: #7c3aed; }
.mu-color    { color: #d97706; }

/* ── 계산기 탭 ── */
.intro-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px; }
@media (max-width: 520px) { .intro-grid { grid-template-columns: 1fr; } }
.intro-card { border-radius: 12px; padding: 12px 14px; border: 2px solid; }
.intro-card .ic-name { font-size: 1.1rem; font-weight: 900; margin-bottom: 4px; }
.intro-card .ic-def  { font-size: 0.79rem; color: #475569; line-height: 1.5; }
.intro-card .ic-ex   { font-size: 0.76rem; color: #64748b; margin-top: 4px; }
.ic-tau   { background: #eff6ff; border-color: #93c5fd; }
.ic-sigma { background: #f0fdf4; border-color: #86efac; }
.ic-phi   { background: #fdf4ff; border-color: #d8b4fe; }
.ic-mu    { background: #fff7ed; border-color: #fcd34d; }
.input-area { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 14px; margin-bottom: 10px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.input-area label { font-weight: 700; font-size: 0.9rem; }
input[type=range] { flex: 1; min-width: 150px; accent-color: #3b82f6; }
input[type=number] { width: 75px; padding: 6px 8px; border-radius: 8px; border: 1.5px solid #cbd5e1;
  font-size: 1rem; font-weight: 700; text-align: center; background: #f8fafc; }
.n-display { font-size: 2.2rem; font-weight: 900; color: #1d4ed8; min-width: 56px; text-align: center; }
.factor-display { background: #1e293b; color: #f1f5f9; border-radius: 10px;
  padding: 10px 14px; font-size: 0.95rem; display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.factor-display .pfact { background: #3b82f6; color: #fff; padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.88rem; }
.factor-display .fmult { color: #94a3b8; }
.factor-display .feq { color: #fbbf24; font-weight: 700; margin: 0 4px; }
.func-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
@media (max-width: 560px) { .func-grid { grid-template-columns: 1fr; } }
.func-card { border-radius: 14px; padding: 14px; border: 2px solid; transition: transform .15s, box-shadow .15s; }
.func-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.08); }
.fc-tau   { background: #eff6ff; border-color: #93c5fd; }
.fc-sigma { background: #f0fdf4; border-color: #86efac; }
.fc-phi   { background: #fdf4ff; border-color: #d8b4fe; }
.fc-mu    { background: #fff7ed; border-color: #fcd34d; }
.func-name  { font-size: 1.3rem; font-weight: 900; margin-bottom: 2px; }
.func-value { font-size: 1.9rem; font-weight: 900; margin-bottom: 6px; }
.func-desc  { font-size: 0.77rem; color: #475569; margin-bottom: 8px; }
.func-steps { font-size: 0.79rem; line-height: 1.7; color: #334155; }
.func-steps .step { background: rgba(255,255,255,.7); border-radius: 8px; padding: 6px 10px; margin-top: 6px; }
.hval { font-weight: 700; font-size: 1.05em; }

/* ── 비교표 탭 ── */
.table-wrap { overflow-x: auto; max-height: 480px; overflow-y: auto; }
table.ftable { width: 100%; border-collapse: collapse; font-size: 0.81rem; }
table.ftable th { background: #1e293b; color: #fff; padding: 8px 10px; text-align: center; position: sticky; top: 0; z-index: 2; }
table.ftable td { padding: 6px 10px; text-align: center; border-bottom: 1px solid #e2e8f0; cursor: pointer; transition: background .1s; }
table.ftable tr:hover td { background: #f0f9ff !important; }
table.ftable tr.selected td { background: #dbeafe !important; }
.td-n { font-weight: 700; background: #f8fafc; }
.td-fact { font-size: 0.72rem; color: #64748b; max-width: 120px; }
.td-tau { color: #1d4ed8; font-weight: 700; }
.td-sigma { color: #16a34a; font-weight: 700; }
.td-phi { color: #7c3aed; font-weight: 700; }
.mu-pos { color: #059669; font-weight: 700; }
.mu-neg { color: #dc2626; font-weight: 700; }
.mu-zero { color: #94a3b8; font-weight: 700; }
.perfect-num td { background: #fef9c3 !important; }
.prime-row td { background: #f0fdf4 !important; }
.legend { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 8px; font-size: 0.77rem; align-items: center; }
.legend-dot { width: 12px; height: 12px; border-radius: 3px; display: inline-block; margin-right: 4px; }

/* ── 이론 카드 (다크) ── */
.theory-card { background: #1e293b; color: #f1f5f9; border-radius: 14px; padding: 14px 18px; margin-bottom: 10px; }
.theory-title { font-size: 1rem; font-weight: 700; color: #fbbf24; margin-bottom: 8px; }
.theory-line { font-size: 0.85rem; line-height: 1.9; }
.tmath { color: #93c5fd; font-style: italic; }
.temph { color: #6ee7b7; font-weight: 700; }

/* ── 공통 컨트롤 ── */
.select-row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 10px; }
.select-row label { font-size: 0.85rem; font-weight: 600; }
select.ss { padding: 6px 10px; border-radius: 8px; border: 1.5px solid #cbd5e1; font-size: 0.9rem; background: #f8fafc; cursor: pointer; }
.pbadge { display: inline-block; padding: 2px 8px; border-radius: 14px; font-size: 0.78rem; font-weight: 700; margin: 2px; }
.pb-tau   { background: #eff6ff; color: #1d4ed8; border: 1px solid #93c5fd; }
.pb-sigma { background: #f0fdf4; color: #16a34a; border: 1px solid #86efac; }
.pb-phi   { background: #fdf4ff; color: #7c3aed; border: 1px solid #d8b4fe; }
.pb-mu    { background: #fff7ed; color: #d97706; border: 1px solid #fcd34d; }
.range-ctrl { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 10px; }
.range-ctrl label { font-size: 0.85rem; font-weight: 600; }
.rv { font-size: 1.1rem; font-weight: 900; color: #1d4ed8; min-width: 30px; display: inline-block; text-align: center; }

/* ── 곱셈성 탐구 탭 ── */
.m3grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 10px 0; }
@media (max-width: 560px) { .m3grid { grid-template-columns: 1fr; } }
.mcell { border-radius: 12px; padding: 12px; text-align: center; border: 2px solid #e2e8f0; }
.mcell .mlabel { font-size: 0.79rem; color: #64748b; margin-bottom: 4px; }
.mcell .mbig { font-size: 1.45rem; font-weight: 900; }
.mcell .mfact { font-size: 0.72rem; color: #94a3b8; margin-top: 2px; }
.meq { text-align: center; font-size: 0.97rem; font-weight: 700; padding: 9px; border-radius: 10px; margin: 6px 0; }
.meq-ok  { background: #d1fae5; color: #065f46; }
.meq-err { background: #fee2e2; color: #991b1b; }
.cp-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.81rem; font-weight: 700; }
.cp-yes { background: #d1fae5; color: #065f46; }
.cp-no  { background: #fee2e2; color: #991b1b; }

/* ── 함수별 성질 탭 ── */
.fsrow { display: flex; gap: 6px; margin-bottom: 12px; flex-wrap: wrap; }
.fsb { padding: 8px 18px; border-radius: 10px; border: 2px solid; font-size: 0.88rem; font-weight: 700; cursor: pointer; transition: all .15s; }
.fsb-tau   { border-color: #93c5fd; color: #1d4ed8; background: #eff6ff; }
.fsb-tau.active   { background: #1d4ed8; color: #fff; }
.fsb-sigma { border-color: #86efac; color: #16a34a; background: #f0fdf4; }
.fsb-sigma.active { background: #16a34a; color: #fff; }
.fsb-phi   { border-color: #d8b4fe; color: #7c3aed; background: #fdf4ff; }
.fsb-phi.active   { background: #7c3aed; color: #fff; }
.fsb-mu    { border-color: #fcd34d; color: #d97706; background: #fff7ed; }
.fsb-mu.active    { background: #d97706; color: #fff; }

.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
@media (max-width: 560px) { .two-col { grid-template-columns: 1fr; } }
.prop-num { font-weight: 900; font-size: 0.92rem; margin-bottom: 4px; }

/* 약수 블록 */
.div-blocks { display: flex; flex-wrap: wrap; gap: 5px; margin: 8px 0; }
.dblk { padding: 5px 11px; border-radius: 8px; font-weight: 700; font-size: 0.83rem; border: 1.5px solid; }
.dblk-tau   { background: #dbeafe; color: #1e40af; border-color: #93c5fd; }
.dblk-sigma { background: #dcfce7; color: #14532d; border-color: #86efac; }

/* 등비수열 시각화 */
.series-row { display: flex; align-items: center; gap: 4px; flex-wrap: wrap; margin: 8px 0; }
.sterm { background: #d1fae5; color: #065f46; border: 1.5px solid #6ee7b7; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 0.85rem; }
.splus { color: #64748b; font-weight: 700; }
.seq   { color: #d97706; font-weight: 900; font-size: 1.1em; margin: 0 4px; }

/* 서로소 격자 */
.cg-wrap { display: flex; flex-wrap: wrap; gap: 4px; margin: 8px 0; }
.cg { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center;
  font-size: 0.77rem; font-weight: 700; transition: all .2s; border: 2px solid; }
.cg-co { background: #d1fae5; color: #065f46; border-color: #6ee7b7; }
.cg-no { background: #fee2e2; color: #991b1b; border-color: #fca5a5; opacity:.6; }
.cg-self { background: #1d4ed8; color: #fff; border-color: #1d4ed8; }

/* μ 합 시각화 */
.mu-sum-row { display: flex; flex-wrap: wrap; gap: 4px; align-items: center; margin: 8px 0; }
.muterm { padding: 4px 10px; border-radius: 8px; font-size: 0.81rem; font-weight: 700; border: 1.5px solid; }
.muterm-pos  { background: #d1fae5; color: #065f46; border-color: #6ee7b7; }
.muterm-neg  { background: #fee2e2; color: #991b1b; border-color: #fca5a5; }
.muterm-zero { background: #f1f5f9; color: #94a3b8; border-color: #e2e8f0; }

/* 뫼비우스 역산 테이블 */
table.mobtable { width: 100%; border-collapse: collapse; font-size: 0.8rem; margin-top: 8px; }
table.mobtable th { background: #334155; color: #fff; padding: 7px 8px; text-align: center; }
table.mobtable td { padding: 6px 8px; text-align: center; border-bottom: 1px solid #e2e8f0; }
table.mobtable .hl { color: #1d4ed8; font-weight: 700; }
.result-box { background: #eff6ff; border: 1.5px solid #93c5fd; border-radius: 10px; padding: 10px 14px; font-size: 0.86rem; margin-top: 8px; }

/* ── 퀴즈 탭 ── */
.score-bar { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 12px 16px; margin-bottom: 12px; display: flex; align-items: center; gap: 14px; }
.score-num { font-size: 1.5rem; font-weight: 900; color: #1d4ed8; }
.score-lbl { font-size: 0.83rem; color: #64748b; }
.btn-nq { padding: 8px 18px; background: #3b82f6; color: #fff; border: none; border-radius: 10px; font-weight: 700; cursor: pointer; font-size: 0.88rem; }
.btn-nq:hover { background: #2563eb; }
.qcard { background: #fff; border: 2px solid #e2e8f0; border-radius: 14px; padding: 16px; margin-bottom: 10px; }
.qcard .qq { font-size: 1rem; font-weight: 700; margin-bottom: 12px; }
.qopts { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.qopt { padding: 10px 12px; border-radius: 10px; border: 2px solid #e2e8f0; background: #f8fafc; cursor: pointer; font-weight: 600; text-align: center; transition: all .15s; font-size: 0.9rem; }
.qopt:hover:not([disabled]) { background: #eff6ff; border-color: #93c5fd; }
.qopt.correct { background: #d1fae5; border-color: #6ee7b7; color: #065f46; }
.qopt.wrong   { background: #fee2e2; border-color: #fca5a5; color: #991b1b; }
.qopt[disabled] { cursor: default; }
.qexplain { margin-top: 10px; padding: 10px 14px; border-radius: 8px; background: #eff6ff; border: 1px solid #bfdbfe; font-size: 0.83rem; line-height: 1.6; display: none; }
</style></head>
<body>
<div id="app">
<h2>🔢 산술함수와 곱셈함수 탐구</h2>
<p style="font-size:0.82rem;color:#64748b;margin-bottom:12px;">
  자연수 <em>n</em>에 대한 네 가지 함수를 직접 계산하고 각 함수의 신기한 성질을 발견해보세요!
</p>

<div class="tab-row">
  <button class="tab-btn active" id="tab-calc"  onclick="switchTab('calc')">🔢 함수 계산기</button>
  <button class="tab-btn"        id="tab-table" onclick="switchTab('table')">📊 비교표</button>
  <button class="tab-btn"        id="tab-mult"  onclick="switchTab('mult')">🧩 곱셈성 탐구</button>
  <button class="tab-btn"        id="tab-props" onclick="switchTab('props')">📐 함수별 성질</button>
  <button class="tab-btn"        id="tab-quiz"  onclick="switchTab('quiz')">🎮 퀴즈</button>
</div>

<!-- ═══════════════ TAB 1: 계산기 ═══════════════ -->
<div id="pane-calc">
  <div class="intro-grid">
    <div class="intro-card ic-tau">
      <div class="ic-name tau-color">τ(n) 타우 함수</div>
      <div class="ic-def"><em>n</em>의 <strong>약수의 개수</strong><br>τ(n) = Σ<sub>d|n</sub> 1</div>
      <div class="ic-ex">τ(6) = 4 &nbsp;(약수: 1,2,3,6)</div>
    </div>
    <div class="intro-card ic-sigma">
      <div class="ic-name sigma-color">σ(n) 시그마 함수</div>
      <div class="ic-def"><em>n</em>의 <strong>약수의 합</strong><br>σ(n) = Σ<sub>d|n</sub> d</div>
      <div class="ic-ex">σ(6) = 12 &nbsp;(1+2+3+6)</div>
    </div>
    <div class="intro-card ic-phi">
      <div class="ic-name phi-color">φ(n) 오일러 함수</div>
      <div class="ic-def"><em>n</em>이하 중 <em>n</em>과 <strong>서로 소인 수의 개수</strong></div>
      <div class="ic-ex">φ(6) = 2 &nbsp;(1과 5)</div>
    </div>
    <div class="intro-card ic-mu">
      <div class="ic-name mu-color">μ(n) 뫼비우스 함수</div>
      <div class="ic-def">제곱수 약수 있으면 <strong>0</strong>,<br>n=p₁p₂…p<sub>k</sub>이면 <strong>(−1)<sup>k</sup></strong></div>
      <div class="ic-ex">μ(1)=1, μ(6)=1, μ(4)=0</div>
    </div>
  </div>
  <div class="input-area">
    <label>n =</label>
    <span class="n-display" id="nDisplay">12</span>
    <input type="range" id="nSlider" min="1" max="100" value="12" oninput="onN(this.value)">
    <input type="number" id="nInput" min="1" max="100" value="12" oninput="onN(this.value)">
  </div>
  <div class="card" style="margin-bottom:10px;">
    <h3 style="margin-bottom:6px;">🔍 소인수분해</h3>
    <div class="factor-display" id="factorDisplay"></div>
  </div>
  <div class="func-grid" id="funcCards"></div>
</div>

<!-- ═══════════════ TAB 2: 비교표 ═══════════════ -->
<div id="pane-table" style="display:none;">
  <div class="card" style="margin-bottom:8px;">
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:8px;">
      <label style="font-weight:700;font-size:0.88rem;">범위: 1 ~</label>
      <select class="ss" id="tableRange" onchange="renderTable()">
        <option value="20">20</option><option value="30" selected>30</option><option value="50">50</option>
      </select>
    </div>
    <div class="legend">
      <span><span class="legend-dot" style="background:#fef9c3;border:1px solid #fde047;"></span>완전수 (σ=2n)</span>
      <span><span class="legend-dot" style="background:#f0fdf4;border:1px solid #86efac;"></span>소수</span>
    </div>
  </div>
  <div class="table-wrap">
    <table class="ftable"><thead><tr>
      <th>n</th><th>소인수분해</th>
      <th class="tau-color">τ(n)</th><th class="sigma-color">σ(n)</th>
      <th class="phi-color">φ(n)</th><th class="mu-color">μ(n)</th>
    </tr></thead><tbody id="ftableBody"></tbody></table>
  </div>
  <div class="card" id="tableDetail" style="margin-top:10px;display:none;"></div>
</div>

<!-- ═══════════════ TAB 3: 곱셈성 탐구 ═══════════════ -->
<div id="pane-mult" style="display:none;">
  <div class="theory-card">
    <div class="theory-title">📐 곱셈함수의 세 가지 성질</div>
    <div class="theory-line">
      <span class="temph">정의</span>: 서로 소인 두 자연수 <span class="tmath">m, n</span>에 대해
      <span class="tmath">f(mn) = f(m)·f(n)</span>을 만족하는 산술함수<br><br>
      <span style="color:#fbbf24;">성질 1</span>: 항등적으로 0이 아니면 <span class="tmath">f(1) = 1</span><br>
      <span style="color:#fbbf24;">성질 2</span>: <span class="tmath">n = p₁<sup>α₁</sup>···p<sub>k</sub><sup>α<sub>k</sub></sup></span>이면
      <span class="tmath">f(n) = f(p₁<sup>α₁</sup>)···f(p<sub>k</sub><sup>α<sub>k</sub></sup>)</span><br>
      <span style="color:#fbbf24;">성질 3</span>: <span class="tmath">f</span>가 곱셈함수이면
      <span class="tmath">g(n) = Σ<sub>d|n</sub> f(d)</span>도 곱셈함수<br><br>
      <span class="temph">τ, σ, φ 는 모두 곱셈함수</span> → 각각 f(d)=1, f(d)=d, f(d)=φ(d)로 성질 3 적용<br><br>
      <span class="temph">μ(n) 이 곱셈함수인 이유</span>
      &nbsp;(gcd(m,n)=1 일 때 μ(mn)=μ(m)μ(n) 증명)<br>
      <span style="color:#94a3b8;font-size:0.82rem;">
        경우 1: m 또는 n 이 제곱수를 인수로 가지면
        μ(m)=0 또는 μ(n)=0, mn 도 그 제곱수를 약수로 가지므로 μ(mn)=0 = μ(m)μ(n) ✓<br>
        경우 2: m=p₁p₂···p<sub>k</sub>, n=q₁q₂···q<sub>l</sub> (서로 다른 소수, p<sub>i</sub>≠q<sub>j</sub>)<br>
        &nbsp;&nbsp;→ mn = p₁···p<sub>k</sub>q₁···q<sub>l</sub> 이므로
        μ(mn) = (−1)<sup>k+l</sup> = (−1)<sup>k</sup>(−1)<sup>l</sup> = μ(m)μ(n) ✓
      </span>
    </div>
  </div>

  <div class="card">
    <h3>🔬 검증: f(mn) = f(m)·f(n)?</h3>
    <p style="font-size:0.82rem;color:#475569;margin-bottom:10px;">서로 소인 두 수 m, n을 골라 네 함수 모두 확인해보세요.</p>
    <div class="select-row">
      <label>m =</label>
      <select class="ss" id="multM" onchange="renderMult()"></select>
      <label>n =</label>
      <select class="ss" id="multN" onchange="renderMult()"></select>
      <span id="cpStatus"></span>
    </div>
    <div id="multResult"></div>
  </div>

  <div class="card" style="margin-top:10px;">
    <h3>🔬 성질 3 탐구: g(n) = Σ<sub>d|n</sub> f(d) 도 곱셈함수</h3>
    <p style="font-size:0.82rem;color:#475569;margin-bottom:10px;">
      f의 종류에 따라 g(n)이 잘 알려진 함수가 됩니다. μ(d)를 더하면 ε(n)이!
    </p>
    <div class="select-row">
      <label>n =</label>
      <select class="ss" id="p3N" onchange="renderProp3()"></select>
    </div>
    <div id="p3Result"></div>
  </div>
</div>

<!-- ═══════════════ TAB 4: 함수별 성질 ═══════════════ -->
<div id="pane-props" style="display:none;">
  <div class="fsrow">
    <button class="fsb fsb-tau active" id="fsb-tau"   onclick="showFunc('tau')">τ(n) 타우</button>
    <button class="fsb fsb-sigma"      id="fsb-sigma" onclick="showFunc('sigma')">σ(n) 시그마</button>
    <button class="fsb fsb-phi"        id="fsb-phi"   onclick="showFunc('phi')">φ(n) 오일러</button>
    <button class="fsb fsb-mu"         id="fsb-mu"    onclick="showFunc('mu')">μ(n) 뫼비우스</button>
  </div>

  <!-- τ(n) -->
  <div id="fp-tau">
    <div class="theory-card">
      <div class="theory-title">τ(n)의 성질</div>
      <div class="theory-line">
        <span style="color:#fbbf24;">성질 1</span>: <span class="temph">τ(n)은 곱셈함수</span>
        &nbsp;(f(d)=1은 곱셈함수 → 성질 3에 의해 g(n)=Σ1=τ(n)도 곱셈함수)<br>
        <span style="color:#fbbf24;">성질 2</span>: <span class="tmath">τ(p<sup>α</sup>) = α + 1</span>&nbsp;&nbsp;(α는 자연수, p는 소수)<br>
        <span style="color:#94a3b8;font-size:0.82rem;">
          &nbsp;&nbsp;p<sup>α</sup>의 모든 약수: 1, p, p², ..., p<sup>α</sup> → 개수 = α+1
        </span><br>
        <span style="color:#fbbf24;">성질 3</span>:
        <span class="tmath">n = p₁<sup>α₁</sup>···p<sub>k</sub><sup>α<sub>k</sub></sup></span>이면
        <span class="tmath">τ(n) = (α₁+1)(α₂+1)···(α<sub>k</sub>+1)</span>
      </div>
    </div>
    <div class="card">
      <h3>🔬 소수 거듭제곱의 약수: τ(p<sup>α</sup>) = α+1</h3>
      <div class="range-ctrl">
        <label>소수 p =</label>
        <select class="ss" id="tauP" onchange="renderTauPow()">
          <option>2</option><option>3</option><option>5</option><option>7</option>
        </select>
        <label>지수 α =</label>
        <span class="rv" id="tauAv">3</span>
        <input type="range" id="tauA" min="1" max="6" value="3" style="width:110px;"
          oninput="document.getElementById('tauAv').textContent=this.value; renderTauPow()">
      </div>
      <div id="tauPowResult"></div>
    </div>
    <div class="card">
      <h3>🔬 일반 공식: τ(n) = (α₁+1)···(α<sub>k</sub>+1)</h3>
      <div class="range-ctrl">
        <label>n =</label>
        <span class="rv" id="tauNv">60</span>
        <input type="range" id="tauNr" min="2" max="120" value="60" style="flex:1;min-width:120px;"
          oninput="document.getElementById('tauNv').textContent=this.value; renderTauGen()">
      </div>
      <div id="tauGenResult"></div>
    </div>
  </div>

  <!-- σ(n) -->
  <div id="fp-sigma" style="display:none;">
    <div class="theory-card">
      <div class="theory-title">σ(n)의 성질</div>
      <div class="theory-line">
        <span style="color:#fbbf24;">성질 1</span>: <span class="temph">σ(n)은 곱셈함수</span>
        &nbsp;(f(d)=d는 곱셈함수 → 성질 3에 의해 g(n)=Σd=σ(n)도 곱셈함수)<br>
        <span style="color:#fbbf24;">성질 2</span>:
        <span class="tmath">σ(p<sup>α</sup>) = (p<sup>α+1</sup>−1)/(p−1) = 1+p+p²+···+p<sup>α</sup></span><br>
        <span style="color:#94a3b8;font-size:0.82rem;">
          &nbsp;&nbsp;p<sup>α</sup>의 약수의 합 = 등비수열의 합
        </span><br>
        <span style="color:#fbbf24;">성질 3</span>:
        <span class="tmath">σ(n) = σ(p₁<sup>α₁</sup>)×σ(p₂<sup>α₂</sup>)×···×σ(p<sub>k</sub><sup>α<sub>k</sub></sup>)</span><br>
        <span style="color:#fbbf24;">완전수</span>: <span class="tmath">σ(n) = 2n</span>인 수
        &nbsp;(예: 6, 28, 496, 8128, …)
      </div>
    </div>
    <div class="card">
      <h3>🔬 등비수열의 합: σ(p<sup>α</sup>)</h3>
      <div class="range-ctrl">
        <label>소수 p =</label>
        <select class="ss" id="sigP" onchange="renderSigmaPow()">
          <option>2</option><option>3</option><option>5</option><option>7</option>
        </select>
        <label>지수 α =</label>
        <span class="rv" id="sigAv">3</span>
        <input type="range" id="sigA" min="1" max="5" value="3" style="width:110px;"
          oninput="document.getElementById('sigAv').textContent=this.value; renderSigmaPow()">
      </div>
      <div id="sigPowResult"></div>
    </div>
    <div class="card">
      <h3>🌟 완전수(σ(n)=2n) 탐구</h3>
      <div class="range-ctrl">
        <label>범위: 1 ~</label>
        <select class="ss" id="perfRange" onchange="renderPerfect()">
          <option value="50">50</option><option value="100" selected>100</option>
          <option value="500">500</option><option value="1000">1000</option>
        </select>
      </div>
      <div id="perfectResult"></div>
    </div>
  </div>

  <!-- φ(n) -->
  <div id="fp-phi" style="display:none;">
    <div class="theory-card">
      <div class="theory-title">φ(n)의 성질</div>
      <div class="theory-line">
        <span style="color:#fbbf24;">성질 1</span>: <span class="tmath">n</span>이 소수이면
        <span class="tmath">φ(n) = n − 1</span><br>
        <span style="color:#94a3b8;font-size:0.82rem;">
          &nbsp;&nbsp;n보다 작은 자연수가 모두 n과 서로 소이므로
        </span><br>
        <span style="color:#fbbf24;">성질 2</span>:
        <span class="tmath">φ(p<sup>α</sup>) = p<sup>α</sup>(1 − 1/p) = p<sup>α</sup> − p<sup>α−1</sup></span><br>
        <span style="color:#94a3b8;font-size:0.82rem;">
          &nbsp;&nbsp;p<sup>α</sup> 이하에서 p의 배수(p<sup>α</sup>/p개)를 제외한 나머지
        </span><br>
        <span style="color:#fbbf24;">성질 3</span>: <span class="temph">φ(n)은 곱셈함수</span><br>
        <span style="color:#fbbf24;">성질 4</span>:
        <span class="tmath">Σ<sub>d|n</sub> φ(d) = n</span>
        &nbsp;(n의 모든 약수에 대해 φ를 더하면 n)
      </div>
    </div>
    <div class="card">
      <h3>🔬 서로소 격자: φ(n) 시각화</h3>
      <p style="font-size:0.81rem;color:#475569;margin-bottom:8px;">
        초록 = <em>n</em>과 서로 소 &nbsp;|&nbsp; 빨강 = 공약수 있음 &nbsp;|&nbsp; 파랑 = n 자신
      </p>
      <div class="range-ctrl">
        <label>n =</label>
        <span class="rv" id="phiNv">12</span>
        <input type="range" id="phiNr" min="2" max="40" value="12" style="flex:1;min-width:120px;"
          oninput="document.getElementById('phiNv').textContent=this.value; renderPhiGrid()">
      </div>
      <div id="phiGridResult"></div>
    </div>
    <div class="card">
      <h3>🔬 성질 4: Σ<sub>d|n</sub> φ(d) = n</h3>
      <div class="range-ctrl">
        <label>n =</label>
        <select class="ss" id="phiSumN" onchange="renderPhiSum()">
          <!-- filled by JS -->
        </select>
      </div>
      <div id="phiSumResult"></div>
    </div>
  </div>

  <!-- μ(n) -->
  <div id="fp-mu" style="display:none;">
    <div class="theory-card">
      <div class="theory-title">μ(n)의 성질</div>
      <div class="theory-line">
        <span style="color:#fbbf24;">성질 1</span>: <span class="temph">μ(n)은 곱셈함수</span>
        &nbsp;(Tab 3 이론카드 참조)<br>
        <span style="color:#fbbf24;">성질 2</span>:
        <span class="tmath">Σ<sub>d|n</sub> μ(d) = ε(n)</span>
        &nbsp;(n=1이면 1, n&gt;1이면 0)<br>
        <span style="color:#94a3b8;font-size:0.82rem;">
          &nbsp;&nbsp;μ는 곱셈함수 → Σμ(d)도 곱셈함수 → p<sup>j</sup>에서 1+(−1)+0+···=0 확인
        </span><br>
        <span style="color:#fbbf24;">성질 3 (뫼비우스 역산 공식)</span>:
        <span class="tmath">g(n) = Σ<sub>d|n</sub> f(d)</span>이면
        <span class="tmath">f(n) = Σ<sub>d|n</sub> μ(d)g(n/d)</span><br>
        <span style="color:#fbbf24;">성질 4</span>:
        <span class="tmath">φ(n) = Σ<sub>d|n</sub> μ(d)·(n/d)</span>
        &nbsp;(Σ<sub>d|n</sub>φ(d)=n 에 역산 공식 적용)
      </div>
    </div>
    <div class="card">
      <h3>🔬 성질 2: Σ<sub>d|n</sub> μ(d) = ε(n)</h3>
      <div class="range-ctrl">
        <label>n =</label>
        <span class="rv" id="muNv">12</span>
        <input type="range" id="muNr" min="1" max="60" value="12" style="flex:1;min-width:120px;"
          oninput="document.getElementById('muNv').textContent=this.value; renderMuSum()">
      </div>
      <div id="muSumResult"></div>
    </div>
    <div class="card">
      <h3>🔬 성질 4: φ(n) = Σ<sub>d|n</sub> μ(d)·(n/d) — 뫼비우스 역산 공식 적용</h3>
      <p style="font-size:0.81rem;color:#475569;margin-bottom:8px;">
        Σ<sub>d|n</sub>φ(d) = n 임을 이미 알고 있으므로, g(n)=n, f(n)=φ(n)으로 놓고 역산 공식을 적용합니다.
      </p>
      <div class="range-ctrl">
        <label>n =</label>
        <select class="ss" id="mobN" onchange="renderMobius()">
          <!-- filled by JS -->
        </select>
      </div>
      <div id="mobiusResult"></div>
    </div>
  </div>
</div>

<!-- ═══════════════ TAB 5: 퀴즈 ═══════════════ -->
<div id="pane-quiz" style="display:none;">
  <div class="score-bar">
    <div>
      <div class="score-num" id="scoreNum">0 / 0</div>
      <div class="score-lbl">점수</div>
    </div>
    <div style="flex:1;"></div>
    <button class="btn-nq" onclick="newQuiz()">🎲 새 문제 세트</button>
  </div>
  <div id="quizBox"></div>
</div>

</div><!-- #app -->

<script>
// ════════════════════════════════
// MATH UTILITIES
// ════════════════════════════════
function factorize(n) {
  if (n <= 1) return {};
  const f = {}; let t = n;
  for (let p = 2; p * p <= t; p++) {
    while (t % p === 0) { f[p] = (f[p]||0)+1; t = Math.floor(t/p); }
  }
  if (t > 1) f[t] = (f[t]||0)+1;
  return f;
}
function tau(n)   { if(n===1)return 1; return Object.values(factorize(n)).reduce((a,e)=>a*(e+1),1); }
function sigma(n) { if(n===1)return 1; return Math.round(Object.entries(factorize(n)).reduce((a,[p,e])=>a*(Math.pow(+p,e+1)-1)/(+p-1),1)); }
function phi(n)   { if(n===1)return 1; return Math.round(Object.entries(factorize(n)).reduce((a,[p,e])=>a*Math.pow(+p,e)*(1-1/+p),1)); }
function mu(n)    { if(n===1)return 1; const f=factorize(n); if(Object.values(f).some(e=>e>1))return 0; return Math.pow(-1,Object.keys(f).length); }
function gcd(a,b) { while(b){let t=b;b=a%b;a=t;} return a; }
function divisors(n) { const d=[]; for(let i=1;i*i<=n;i++){if(n%i===0){d.push(i);if(i!==n/i)d.push(n/i);}} return d.sort((a,b)=>a-b); }
function factHTML(n) { if(n===1)return '1'; return Object.entries(factorize(n)).map(([p,e])=>e>1?`${p}<sup>${e}</sup>`:p).join('×'); }
function factText(n) { if(n===1)return '1'; return Object.entries(factorize(n)).map(([p,e])=>e>1?`${p}^${e}`:p).join('×'); }

// ════════════════════════════════
// TABS
// ════════════════════════════════
function switchTab(t) {
  ['calc','table','mult','props','quiz'].forEach(x => {
    document.getElementById('pane-'+x).style.display = x===t?'':'none';
    document.getElementById('tab-'+x).classList.toggle('active', x===t);
  });
  if(t==='table') renderTable();
  if(t==='mult')  initMult();
  if(t==='props') initProps();
  if(t==='quiz')  initQuiz();
}

// ════════════════════════════════
// TAB 1: CALCULATOR
// ════════════════════════════════
let curN = 12;
function onN(v) {
  v = Math.max(1,Math.min(100,+v||1)); curN=v;
  document.getElementById('nDisplay').textContent=v;
  document.getElementById('nSlider').value=v;
  document.getElementById('nInput').value=v;
  renderCalc(v);
}
function renderCalc(n) {
  const f=factorize(n), entries=Object.entries(f), divs=divisors(n);
  const fd=document.getElementById('factorDisplay');
  if(n===1) { fd.innerHTML='<span class="feq">n = 1</span><span style="color:#94a3b8;"> (소인수 없음)</span>'; }
  else {
    const parts=entries.map(([p,e])=>`<span class="pfact">${p}${e>1?'<sup>'+e+'</sup>':''}</span>`);
    fd.innerHTML=`<span class="feq">n = ${n} =</span> ${parts.join('<span class="fmult"> × </span>')}`;
  }
  const tauV=tau(n), sigV=sigma(n), phiV=phi(n), muV=mu(n);

  // τ steps
  let tS='';
  if(n===1) tS='<div class="step">τ(1) = 1 (정의)</div>';
  else {
    tS=`<div class="step">소인수분해: ${factHTML(n)}<br>
      τ(n) = ${entries.map(([,e])=>`(${e}+1)`).join('×')} = <span class="hval tau-color">${tauV}</span></div>
      <div class="step" style="font-size:.72rem;color:#64748b;">약수: ${divs.join(', ')}</div>`;
  }
  // σ steps
  let sS='';
  if(n===1) sS='<div class="step">σ(1) = 1 (정의)</div>';
  else {
    const symPartsS=entries.map(([p,e])=>{const pn=+p;return `(${pn}<sup>${+e+1}</sup>−1)/(${pn}−1)`;}).join(' × ');
    const numPartsS=entries.map(([p,e])=>{const pn=+p,num=Math.pow(pn,+e+1)-1,den=pn-1;return Math.round(num/den);}).join(' × ');
    sS=`<div class="step">σ(n) = ${symPartsS} = ${numPartsS} = <span class="hval sigma-color">${sigV}</span></div>
      <div class="step" style="font-size:.72rem;color:#64748b;">확인: ${divs.join('+')} = ${sigV}</div>`;
  }
  // φ steps
  let pS='';
  if(n===1) pS='<div class="step">φ(1) = 1 (정의)</div>';
  else {
    const symPartsP=entries.map(([p,e])=>{const pn=+p,pa=Math.pow(pn,+e);return `${pa}·(1−1/${pn})`;}).join(' × ');
    const numPartsP=entries.map(([p,e])=>{const pn=+p,pa=Math.pow(pn,+e);return Math.round(pa*(1-1/pn));}).join(' × ');
    pS=`<div class="step">φ(n) = ${symPartsP} = ${numPartsP} = <span class="hval phi-color">${phiV}</span></div>`;
    if(n<=30){const cps=[];for(let k=1;k<=n;k++)if(gcd(k,n)===1)cps.push(k);pS+=`<div class="step" style="font-size:.72rem;color:#64748b;">서로 소: ${cps.join(', ')}</div>`;}
  }
  // μ steps
  let mS='';
  if(n===1) mS='<div class="step">μ(1) = 1 (정의)</div>';
  else {
    const hasSq=Object.values(f).some(e=>e>1);
    if(hasSq){const [sp,se]=Object.entries(f).find(([,e])=>e>1);mS=`<div class="step">${sp}<sup>${se}</sup>이 약수 → 제곱수 약수 존재<br>μ(n) = <span class="hval mu-color">0</span></div>`;}
    else {const k=Object.keys(f).length;mS=`<div class="step">서로 다른 소인수 ${k}개<br>μ(n) = (−1)<sup>${k}</sup> = <span class="hval mu-color">${muV}</span></div>`;}
  }
  const pNote=sigV===2*n&&n>1?' 🌟 <strong>완전수!</strong>':'';
  document.getElementById('funcCards').innerHTML=`
    <div class="func-card fc-tau"><div class="func-name tau-color">τ(${n})</div><div class="func-value tau-color">${tauV}</div><div class="func-desc">약수의 개수</div><div class="func-steps">${tS}</div></div>
    <div class="func-card fc-sigma"><div class="func-name sigma-color">σ(${n})</div><div class="func-value sigma-color">${sigV}</div><div class="func-desc">약수의 합${pNote}</div><div class="func-steps">${sS}</div></div>
    <div class="func-card fc-phi"><div class="func-name phi-color">φ(${n})</div><div class="func-value phi-color">${phiV}</div><div class="func-desc">${n}과 서로 소인 수의 개수</div><div class="func-steps">${pS}</div></div>
    <div class="func-card fc-mu"><div class="func-name mu-color">μ(${n})</div><div class="func-value mu-color">${muV}</div><div class="func-desc">${muV===0?'제곱수 약수 존재':muV===1?'소인수 개수 짝수':'소인수 개수 홀수'}</div><div class="func-steps">${mS}</div></div>`;
}

// ════════════════════════════════
// TAB 2: TABLE
// ════════════════════════════════
let selRow=-1;
function renderTable() {
  const max=+document.getElementById('tableRange').value;
  let html='';
  for(let n=1;n<=max;n++){
    const tN=tau(n),sN=sigma(n),pN=phi(n),mN=mu(n);
    const isP=sN===2*n&&n>1, isPr=Object.keys(factorize(n)).length===1&&Object.values(factorize(n))[0]===1;
    let rc=n===selRow?'selected':isP?'perfect-num':isPr?'prime-row':'';
    const mc=mN>0?'mu-pos':mN<0?'mu-neg':'mu-zero';
    html+=`<tr class="${rc}" onclick="selRow=${n};renderTable();showDetail(${n})">
      <td class="td-n">${n}</td><td class="td-fact">${factHTML(n)}</td>
      <td class="td-tau">${tN}</td><td class="td-sigma">${sN}</td>
      <td class="td-phi">${pN}</td><td class="${mc}">${mN}</td></tr>`;
  }
  document.getElementById('ftableBody').innerHTML=html;
}
function showDetail(n) {
  const divs=divisors(n),tN=tau(n),sN=sigma(n),pN=phi(n),mN=mu(n);
  const isP=sN===2*n&&n>1,isPr=Object.keys(factorize(n)).length===1&&Object.values(factorize(n))[0]===1;
  let d=`<h3 style="margin-bottom:8px;">📌 n = ${n}</h3>
    <p style="font-size:.84rem;margin-bottom:6px;">소인수분해: <strong>${factHTML(n)}</strong></p>
    <p style="font-size:.84rem;margin-bottom:8px;">약수: ${divs.map(x=>`<span class="pbadge pb-tau">${x}</span>`).join('')}</p>
    <div style="display:flex;gap:6px;flex-wrap:wrap;">
      <span class="pbadge pb-tau">τ=${tN}</span><span class="pbadge pb-sigma">σ=${sN}</span>
      <span class="pbadge pb-phi">φ=${pN}</span><span class="pbadge pb-mu">μ=${mN}</span>
    </div>`;
  if(isP) d+=`<p style="margin-top:8px;color:#d97706;font-weight:700;font-size:.82rem;">🌟 완전수! σ(${n})=${sN}=2×${n}</p>`;
  if(isPr) d+=`<p style="margin-top:4px;color:#059669;font-weight:700;font-size:.82rem;">🔵 소수 → φ=${n}−1=${pN}, τ=2</p>`;
  const el=document.getElementById('tableDetail'); el.innerHTML=d; el.style.display='';
}

// ════════════════════════════════
// TAB 3: MULTIPLICATIVE
// ════════════════════════════════
function initMult() {
  const mS=document.getElementById('multM'), nS=document.getElementById('multN');
  if(mS.children.length===0){
    for(let i=2;i<=30;i++){mS.add(new Option(i,i));nS.add(new Option(i,i));}
    mS.value=4; nS.value=9;
  }
  const p3=document.getElementById('p3N');
  if(p3.children.length===0){for(let i=2;i<=30;i++)p3.add(new Option(i,i)); p3.value=12;}
  renderMult(); renderProp3();
}
function renderMult() {
  const m=+document.getElementById('multM').value, n=+document.getElementById('multN').value;
  const g=gcd(m,n), mn=m*n;
  document.getElementById('cpStatus').innerHTML=g===1
    ?`<span class="cp-badge cp-yes">gcd(${m},${n})=1 ✓ 서로 소!</span>`
    :`<span class="cp-badge cp-no">gcd(${m},${n})=${g} ✗ 서로 소 아님</span>`;
  if(g!==1){
    document.getElementById('multResult').innerHTML=`<div style="background:#fee2e2;border-radius:10px;padding:12px;color:#991b1b;font-size:.86rem;">⚠️ 서로 소가 아닙니다. 다른 수를 선택해보세요.</div>`;
    return;
  }
  const fns=[{name:'τ',fn:tau,bg:'#eff6ff',bc:'#93c5fd',tc:'#1d4ed8'},{name:'σ',fn:sigma,bg:'#f0fdf4',bc:'#86efac',tc:'#16a34a'},{name:'φ',fn:phi,bg:'#fdf4ff',bc:'#d8b4fe',tc:'#7c3aed'},{name:'μ',fn:mu,bg:'#fff7ed',bc:'#fcd34d',tc:'#d97706'}];
  let html=`<div class="m3grid">
    <div class="mcell" style="background:#f0f9ff;"><div class="mlabel">m</div><div class="mbig">${m}</div><div class="mfact">${factText(m)}</div></div>
    <div class="mcell" style="background:#f0fdf4;"><div class="mlabel">n</div><div class="mbig">${n}</div><div class="mfact">${factText(n)}</div></div>
    <div class="mcell" style="background:#fdf4ff;"><div class="mlabel">m×n</div><div class="mbig">${mn}</div><div class="mfact">${factText(mn)}</div></div>
  </div>`;
  fns.forEach(({name,fn,bg,bc,tc})=>{
    const fm=fn(m),fn2=fn(n),fmn=fn(mn),ok=fm*fn2===fmn;
    html+=`<div style="background:${bg};border-radius:12px;padding:11px;margin-bottom:7px;border:1px solid ${bc};">
      <div style="font-weight:700;color:${tc};margin-bottom:5px;">${name}(n) 검증</div>
      <div style="font-size:.85rem;line-height:2;">${name}(${m})=<strong>${fm}</strong>, ${name}(${n})=<strong>${fn2}</strong>, ${name}(${mn})=<strong>${fmn}</strong></div>
      <div class="meq ${ok?'meq-ok':'meq-err'}">${name}(${m})×${name}(${n}) = ${fm}×${fn2} = ${fm*fn2} ${ok?'= '+fmn+' = '+name+'('+mn+') ✓':'≠ '+fmn+' ✗'}</div>
    </div>`;
  });
  document.getElementById('multResult').innerHTML=html;
}
function renderProp3() {
  const n=+document.getElementById('p3N').value, divs=divisors(n);
  const tN=tau(n), sN=sigma(n), sumPhi=divs.reduce((a,d)=>a+phi(d),0);
  const muVals=divs.map(d=>mu(d)), muSum=muVals.reduce((a,v)=>a+v,0);
  const epsilon=n===1?1:0;
  let html=`<div style="background:#f8fafc;border-radius:10px;padding:10px;margin-bottom:8px;font-size:.84rem;">
    <strong>n=${n}</strong>의 약수: ${divs.map(d=>`<span class="pbadge pb-tau">${d}</span>`).join('')}
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:8px;">
    <div style="background:#eff6ff;border-radius:12px;padding:12px;border:1px solid #93c5fd;">
      <div style="font-weight:700;color:#1d4ed8;margin-bottom:6px;">f(d)=1 → g(n)=τ(n)</div>
      <div style="font-size:.82rem;line-height:1.9;">Σ 1 = ${divs.map(()=>'1').join('+')} = <strong class="tau-color">${tN}</strong> = τ(${n}) ✓</div>
    </div>
    <div style="background:#f0fdf4;border-radius:12px;padding:12px;border:1px solid #86efac;">
      <div style="font-weight:700;color:#16a34a;margin-bottom:6px;">f(d)=d → g(n)=σ(n)</div>
      <div style="font-size:.82rem;line-height:1.9;">Σ d = ${divs.join('+')} = <strong class="sigma-color">${sN}</strong> = σ(${n}) ✓</div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
    <div style="background:#fdf4ff;border-radius:12px;padding:12px;border:1px solid #d8b4fe;">
      <div style="font-weight:700;color:#7c3aed;margin-bottom:6px;">f(d)=φ(d) → Σφ(d)=n</div>
      <div style="font-size:.81rem;line-height:1.9;">${divs.map(d=>`φ(${d})`).join('+')} = ${divs.map(d=>phi(d)).join('+')} = <strong class="phi-color">${sumPhi}</strong> = ${n} ${sumPhi===n?'✓':'✗'}</div>
    </div>
    <div style="background:#fff7ed;border-radius:12px;padding:12px;border:1px solid #fcd34d;">
      <div style="font-weight:700;color:#d97706;margin-bottom:6px;">f(d)=μ(d) → Σμ(d)=ε(n)</div>
      <div style="font-size:.81rem;line-height:1.9;">${divs.map(d=>`μ(${d})`).join('+')} = ${muVals.map(v=>v<0?`(−${-v})`:String(v)).join('+')} = <strong class="mu-color">${muSum}</strong> = ε(${n}) = ${epsilon} ${muSum===epsilon?'✓':'✗'}</div>
      <div style="font-size:.72rem;color:#d97706;margin-top:4px;">ε(n): n=1이면 1, 나머지는 0</div>
    </div>
  </div>`;
  document.getElementById('p3Result').innerHTML=html;
}

// ════════════════════════════════
// TAB 4: FUNCTION PROPERTIES
// ════════════════════════════════
function initProps() {
  const pSumSel=document.getElementById('phiSumN');
  if(pSumSel.children.length===0){for(let i=2;i<=30;i++)pSumSel.add(new Option(i,i)); pSumSel.value=12;}
  const mobSel=document.getElementById('mobN');
  if(mobSel.children.length===0){for(let i=2;i<=30;i++)mobSel.add(new Option(i,i)); mobSel.value=12;}
  showFunc('tau');
}
function showFunc(fn) {
  ['tau','sigma','phi','mu'].forEach(f=>{
    document.getElementById('fp-'+f).style.display=f===fn?'':'none';
    document.getElementById('fsb-'+f).classList.toggle('active',f===fn);
  });
  if(fn==='tau')   {renderTauPow(); renderTauGen();}
  if(fn==='sigma') {renderSigmaPow(); renderPerfect();}
  if(fn==='phi')   {renderPhiGrid(); renderPhiSum();}
  if(fn==='mu')    {renderMuSum(); renderMobius();}
}

// ── τ ─────────────────────────────────
function renderTauPow() {
  const p=+document.getElementById('tauP').value, a=+document.getElementById('tauA').value;
  const divs=[]; for(let k=0;k<=a;k++) divs.push(Math.pow(p,k));
  const blocks=divs.map(d=>`<span class="dblk dblk-tau">${d}</span>`).join('');
  document.getElementById('tauPowResult').innerHTML=`
    <div style="font-size:.86rem;color:#475569;margin-bottom:6px;">
      <strong>${p}<sup>${a}</sup> = ${Math.pow(p,a)}</strong>의 약수:
    </div>
    <div class="div-blocks">${blocks}</div>
    <div class="result-box">
      p<sup>α</sup>의 약수: 1, ${p === 1?'':p+', '}${divs.filter((_,i)=>i>0&&i<a).map(v=>v).join(', ')}${a>1?', ':' '}${Math.pow(p,a)}<br>
      총 <strong>${a}+1 = ${a+1}개</strong> → <strong class="tau-color">τ(${p}<sup>${a}</sup>) = ${a}+1 = ${a+1}</strong>
    </div>`;
}
function renderTauGen() {
  const n=+document.getElementById('tauNr').value, f=factorize(n), entries=Object.entries(f), divs=divisors(n);
  const formula=entries.map(([p,e])=>`(${e}+1)`).join('×');
  const vals=entries.map(([p,e])=>e+1);
  const result=vals.reduce((a,v)=>a*v,1);
  let html=`<div style="font-size:.85rem;margin-bottom:8px;">
    <strong>n = ${n}</strong> = ${factHTML(n)}
  </div>
  <div style="background:#f8fafc;border-radius:10px;padding:10px;margin-bottom:8px;">
    <div style="font-size:.83rem;line-height:1.9;">`;
  entries.forEach(([p,e])=>{
    const pn=+p; const pDivs=[]; for(let k=0;k<=+e;k++) pDivs.push(Math.pow(pn,k));
    html+=`${p}<sup>${e}</sup>의 약수: ${pDivs.map(d=>`<span class="dblk dblk-tau" style="padding:3px 7px;font-size:.75rem;">${d}</span>`).join('')} → <strong>${+e}+1 = ${+e+1}개</strong><br>`;
  });
  html+=`</div></div>
  <div class="result-box">
    τ(${n}) = ${formula} = ${vals.join('×')} = <strong class="tau-color">${result}</strong>
    &nbsp;&nbsp;(약수 총 개수: ${divs.length}개 ✓)
  </div>`;
  document.getElementById('tauGenResult').innerHTML=html;
}

// ── σ ─────────────────────────────────
function renderSigmaPow() {
  const p=+document.getElementById('sigP').value, a=+document.getElementById('sigA').value;
  const terms=[]; for(let k=0;k<=a;k++) terms.push(Math.pow(p,k));
  const total=terms.reduce((s,v)=>s+v,0);
  const formula=Math.round((Math.pow(p,a+1)-1)/(p-1));
  const seriesHTML=terms.map(v=>`<span class="sterm">${v}</span>`).join('<span class="splus">+</span>');
  document.getElementById('sigPowResult').innerHTML=`
    <div style="font-size:.85rem;color:#475569;margin-bottom:8px;">
      <strong>${p}<sup>${a}</sup> = ${Math.pow(p,a)}</strong>의 약수의 합:
    </div>
    <div class="series-row">${seriesHTML}<span class="seq">=</span><span style="font-size:1.2rem;font-weight:900;color:#16a34a;">${total}</span></div>
    <div class="result-box" style="background:#f0fdf4;border-color:#86efac;">
      등비수열 합 공식: (${p}<sup>${a+1}</sup>−1)/(${p}−1) = (${Math.pow(p,a+1)}−1)/${p-1} = <strong class="sigma-color">${formula}</strong>
      ${total===formula?' ✓':''}
    </div>`;
}
function renderPerfect() {
  const max=+document.getElementById('perfRange').value;
  const perfects=[];
  for(let n=2;n<=max;n++){if(sigma(n)===2*n) perfects.push(n);}
  let html='';
  if(perfects.length===0){
    html=`<div style="color:#64748b;font-size:.85rem;">${max} 이하에 완전수가 없습니다.</div>`;
  } else {
    perfects.forEach(n=>{
      const divs=divisors(n);
      html+=`<div style="background:#fef9c3;border-radius:12px;padding:12px;margin-bottom:8px;border:1px solid #fde047;">
        <div style="font-weight:900;font-size:1.1rem;color:#92400e;margin-bottom:6px;">🌟 n = ${n}</div>
        <div style="font-size:.83rem;line-height:1.8;">
          약수: ${divs.join(', ')}<br>
          약수의 합: ${divs.join('+')} = <strong>${sigma(n)}</strong> = 2×${n} ✓<br>
          <span style="color:#92400e;">σ(${n}) = ${sigma(n)} = 2×${n}</span>
        </div>
      </div>`;
    });
  }
  html+=`<div style="font-size:.78rem;color:#94a3b8;margin-top:6px;">알려진 완전수: 6, 28, 496, 8128, 33550336, … (모두 짝수인지는 미해결 문제!)</div>`;
  document.getElementById('perfectResult').innerHTML=html;
}

// ── φ ─────────────────────────────────
function renderPhiGrid() {
  const n=+document.getElementById('phiNr').value, phiV=phi(n);
  let cells='';
  for(let k=1;k<=n;k++){
    const g=gcd(k,n);
    const cls=k===n?'cg cg-self':g===1?'cg cg-co':'cg cg-no';
    cells+=`<div class="${cls}">${k}</div>`;
  }
  document.getElementById('phiGridResult').innerHTML=`
    <div class="cg-wrap">${cells}</div>
    <div class="result-box" style="background:#fdf4ff;border-color:#d8b4fe;">
      φ(${n}) = <strong class="phi-color">${phiV}</strong>
      &nbsp;&nbsp;(초록색 숫자 개수: ${phiV}개)
      ${Object.keys(factorize(n)).length===1&&Object.values(factorize(n))[0]===1?`<br><span style="color:#7c3aed;font-size:.78rem;">${n}이 소수 → 1~${n-1} 모두 서로 소 → φ=${n}−1=${phiV}</span>`:''}
    </div>`;
}
function renderPhiSum() {
  const n=+document.getElementById('phiSumN').value, divs=divisors(n);
  const phiVals=divs.map(d=>phi(d));
  const total=phiVals.reduce((a,v)=>a+v,0);
  document.getElementById('phiSumResult').innerHTML=`
    <div style="font-size:.84rem;margin-bottom:8px;">
      <strong>n=${n}</strong>의 약수: ${divs.map(d=>`<span class="pbadge pb-phi">${d}</span>`).join('')}
    </div>
    <div style="background:#f8fafc;border-radius:10px;padding:10px;margin-bottom:8px;font-size:.82rem;line-height:2;">
      ${divs.map((d,i)=>`φ(${d}) = <strong>${phiVals[i]}</strong>`).join(' &nbsp;|&nbsp; ')}
    </div>
    <div class="result-box" style="background:#fdf4ff;border-color:#d8b4fe;">
      Σ<sub>d|${n}</sub> φ(d) = ${phiVals.join('+')} = <strong class="phi-color">${total}</strong> = ${n} ${total===n?'✓':'✗'}
      <br><span style="color:#7c3aed;font-size:.78rem;">φ의 성질 4: n의 모든 약수에 대해 φ를 더하면 항상 n이 됩니다!</span>
    </div>`;
}

// ── μ ─────────────────────────────────
function renderMuSum() {
  const n=+document.getElementById('muNr').value, divs=divisors(n);
  const muVals=divs.map(d=>mu(d)), total=muVals.reduce((a,v)=>a+v,0), epsilon=n===1?1:0;
  const termsHTML=divs.map((d,i)=>{
    const mv=muVals[i], cls=mv>0?'muterm muterm-pos':mv<0?'muterm muterm-neg':'muterm muterm-zero';
    return `<span class="${cls}">μ(${d})=${mv}</span>`;
  }).join('<span style="color:#64748b;font-weight:700;padding:0 4px;">+</span>');
  document.getElementById('muSumResult').innerHTML=`
    <div class="mu-sum-row">${termsHTML}</div>
    <div class="result-box" style="background:#fff7ed;border-color:#fcd34d;">
      합계 = ${muVals.join('+')} = <strong class="mu-color">${total}</strong>
      = ε(${n}) = <strong>${epsilon}</strong> ${total===epsilon?'✓':'✗'}
      <br><span style="color:#d97706;font-size:.78rem;">${n===1?'n=1이면 ε(1)=1':'n>1이면 ε(n)=0 (약수들의 μ값이 항상 상쇄됩니다!)'}</span>
    </div>`;
}
function renderMobius() {
  const n=+document.getElementById('mobN').value, divs=divisors(n);
  // φ(n) = Σ_{d|n} μ(d)·(n/d)
  const terms=divs.map(d=>({d, mud:mu(d), nd:n/d, val:mu(d)*(n/d)}));
  const total=terms.reduce((a,t)=>a+t.val,0);
  const phiV=phi(n);
  let tableRows=terms.map(t=>`
    <tr>
      <td>${t.d}</td>
      <td>${factHTML(t.d)}</td>
      <td class="${t.mud>0?'mu-pos':t.mud<0?'mu-neg':'mu-zero'}">${t.mud}</td>
      <td>${n}/${t.d} = ${t.nd}</td>
      <td class="hl">${t.mud}×${t.nd} = ${t.val}</td>
    </tr>`).join('');
  document.getElementById('mobiusResult').innerHTML=`
    <div style="overflow-x:auto;">
    <table class="mobtable">
      <thead><tr><th>약수 d</th><th>소인수분해</th><th class="mu-color">μ(d)</th><th>n/d</th><th>μ(d)·(n/d)</th></tr></thead>
      <tbody>${tableRows}</tbody>
    </table></div>
    <div class="result-box">
      φ(${n}) = Σ<sub>d|${n}</sub> μ(d)·(${n}/d) = ${terms.map(t=>t.val).join('+')} = <strong class="phi-color">${total}</strong>
      &nbsp;&nbsp;(직접계산 φ(${n})=${phiV}) ${total===phiV?'✓':'✗'}
    </div>`;
}

// ════════════════════════════════
// TAB 5: QUIZ
// ════════════════════════════════
let QS=[],QA=[],qScore=0,qAnswered=0;
function initQuiz(){if(QS.length===0)newQuiz();}
function newQuiz(){
  QS=[];QA=[];qScore=0;qAnswered=0;
  const pool=[
    n=>({q:`τ(${n}) = ?`,ans:tau(n),explain:`${n}=${factHTML(n)} → 약수: ${divisors(n).join(',')} → τ=<strong>${tau(n)}</strong>`,wrong:()=>genW(tau(n),'tau')}),
    n=>({q:`σ(${n}) = ?`,ans:sigma(n),explain:`약수의 합: ${divisors(n).join('+')}=<strong>${sigma(n)}</strong>`,wrong:()=>genW(sigma(n),'sigma')}),
    n=>({q:`φ(${n}) = ?`,ans:phi(n),explain:`${n}과 서로 소인 수 개수=<strong>${phi(n)}</strong>`,wrong:()=>genW(phi(n),'phi')}),
    n=>({q:`μ(${n}) = ?`,ans:mu(n),explain:`${factHTML(n)} → μ=<strong>${mu(n)}</strong>`,wrong:()=>[-1,0,1].filter(v=>v!==mu(n))}),
  ];
  for(let i=0;i<5;i++){
    const type=pool[Math.floor(Math.random()*pool.length)];
    const n=Math.floor(Math.random()*20)+2;
    const q=type(n), wrongs=q.wrong().slice(0,3);
    const opts=shuffle([q.ans,...wrongs]);
    QS.push({...q,opts}); QA.push(null);
  }
  updateScore(); renderQuiz();
}
function genW(correct,fn){
  const s=new Set();
  for(const v of [correct-2,correct-1,correct+1,correct+2,correct+3]) if(v!==correct&&v>0)s.add(v);
  for(let n=2;s.size<3&&n<=25;n++){const v=fn==='tau'?tau(n):fn==='sigma'?sigma(n):phi(n);if(v!==correct&&v>0)s.add(v);}
  return [...s];
}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function updateScore(){document.getElementById('scoreNum').textContent=`${qScore} / ${qAnswered}`;}
function renderQuiz(){
  let html='';
  QS.forEach((q,i)=>{
    const done=QA[i]!==null;
    html+=`<div class="qcard"><div class="qq">${i+1}. ${q.q}</div>
      <div class="qopts">${q.opts.map((opt,j)=>{
        let cls=''; if(done){if(opt===q.ans)cls='correct';else if(opt===QA[i])cls='wrong';}
        return `<button class="qopt ${cls}" ${done?'disabled':''} onclick="ansQ(${i},${opt})">${opt}</button>`;
      }).join('')}</div>
      <div class="qexplain" id="qe${i}" ${done?'style="display:block;"':''}>${done?(QA[i]===q.ans?'✅ 정답!':'❌ 오답!')+' &nbsp;'+q.explain:''}</div>
    </div>`;
  });
  document.getElementById('quizBox').innerHTML=html;
}
function ansQ(i,chosen){
  if(QA[i]!==null)return; QA[i]=chosen; qAnswered++; if(chosen===QS[i].ans)qScore++;
  updateScore();
  const card=document.getElementById('quizBox').querySelectorAll('.qcard')[i];
  card.querySelectorAll('.qopt').forEach((btn,j)=>{
    btn.disabled=true;
    if(QS[i].opts[j]===QS[i].ans)btn.classList.add('correct');
    else if(QS[i].opts[j]===chosen)btn.classList.add('wrong');
  });
  const ex=document.getElementById('qe'+i);
  ex.innerHTML=(chosen===QS[i].ans?'✅ 정답!':'❌ 오답!')+' &nbsp;'+QS[i].explain;
  ex.style.display='block';
}

// ════════════════════════════════
// INIT
// ════════════════════════════════
onN(12);
</script>
</body></html>"""


def render():
    st.header("🔢 미니: 산술함수와 곱셈함수")
    st.caption("τ(n), σ(n), φ(n), μ(n)을 직접 계산하고 곱셈함수의 신기한 성질을 탐구해 보세요!")
    components.html(HTML, height=2000, scrolling=True)
