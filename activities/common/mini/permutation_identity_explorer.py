# activities/common/mini/permutation_identity_explorer.py
"""
순열 등식 탐구 — nPr = n×(n-1)P(r-1) 와 nPr = (n-1)Pr + r×(n-1)P(r-1)
두 등식을 직접 조작·체험하며 탐구하는 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "순열등식탐구"

META = {
    "title":       "🔍 순열 등식 탐구",
    "description": "ₙPᵣ = n×ₙ₋₁Pᵣ₋₁ 와 ₙPᵣ = ₙ₋₁Pᵣ + r×ₙ₋₁Pᵣ₋₁ 두 등식을 직접 조작하며 발견합니다.",
    "order":       326,
    "hidden":      False,
}

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "eq1_meaning",
        "label":  "① 등식 ₙPᵣ = n × ₙ₋₁Pᵣ₋₁이 성립하는 이유를 '순열의 의미'로 자신만의 말로 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "eq2_meaning",
        "label":  "② 등식 ₙPᵣ = ₙ₋₁Pᵣ + r × ₙ₋₁Pᵣ₋₁에서 왜 두 경우로 나누었나요? 두 경우를 더할 수 있는 이유는 무엇인가요?",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "reallife_apply",
        "label":  "③ 실생활 탐구 중 가장 인상적인 예시를 고르고, 그 상황에서 두 등식이 각각 어떤 의미인지 설명해보세요.",
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

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(145deg,#060c1a,#0a1428,#050912);
  color:#dde8ff;padding:10px 12px 20px;
}
.hdr{text-align:center;padding:8px 0 12px}
.hdr-title{font-size:1.2rem;font-weight:700;color:#ffd700;
  text-shadow:0 0 18px rgba(255,215,0,.4);margin-bottom:3px}
.hdr-sub{font-size:.74rem;color:#7788aa}

/* MAIN TABS */
.main-tabs{display:flex;gap:4px;margin-bottom:12px;
  background:rgba(255,255,255,.04);border-radius:12px;padding:5px}
.main-tab{flex:1;padding:8px 4px;border:none;border-radius:8px;
  font-family:inherit;font-size:.73rem;font-weight:600;cursor:pointer;
  background:transparent;color:#7788aa;transition:all .2s;line-height:1.4;text-align:center}
.main-tab:hover{color:#dde8ff;background:rgba(255,255,255,.06)}
.main-tab.active{background:rgba(255,215,0,.12);color:#ffd700;border:1px solid rgba(255,215,0,.3)}
.main-panel{display:none}
.main-panel.active{display:block;animation:fadein .25s ease}

/* FORMULA BANNER */
.fml-wrap{background:rgba(255,215,0,.06);border:1.5px solid rgba(255,215,0,.3);
  border-radius:12px;padding:9px 14px;text-align:center;margin-bottom:11px}
.fml-main{font-size:1rem;font-weight:700;color:#ffd700;margin-bottom:3px}
.fml-cond{font-size:.7rem;color:#94a3b8}

/* LIVE EQUATION */
.live-eq{display:flex;align-items:center;justify-content:center;gap:8px;
  flex-wrap:wrap;background:rgba(16,185,129,.05);
  border:1px solid rgba(16,185,129,.2);border-radius:10px;
  padding:8px 12px;margin-bottom:10px}
.leq-lhs{font-family:'Courier New',monospace;color:#ffd700;font-weight:700;font-size:.86rem}
.leq-eq{color:#34d399;font-size:1.1rem;font-weight:700}
.leq-rhs{font-family:'Courier New',monospace;color:#67e8f9;font-weight:700;font-size:.86rem}

/* SLIDERS */
.sl-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  background:rgba(255,255,255,.03);border-radius:10px;padding:7px 12px;margin-bottom:10px}
.sl-lbl{font-size:.78rem;color:#7788aa}
.sl-val{background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.3);
  border-radius:6px;padding:2px 9px;font-size:.88rem;font-weight:700;color:#ffd700}
input[type=range]{accent-color:#ffd700;width:80px}

/* VIS AREA */
.vis{background:rgba(0,0,0,.25);border-radius:12px;padding:14px;margin-bottom:10px}
.vis-hint{font-size:.75rem;color:#7788aa;text-align:center;margin-bottom:10px;line-height:1.6}

/* SLOTS */
.slot-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:12px}
.slot-wrap{display:flex;flex-direction:column;align-items:center;gap:3px}
.slot{width:64px;height:70px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:1.25rem;font-weight:700;transition:all .3s}
.slot-lbl{font-size:.6rem;color:#7788aa}
.slot-empty{border:2px dashed rgba(255,255,255,.15);color:rgba(255,255,255,.12)}
.slot-first-empty{border:2.5px dashed #ffd700;background:rgba(255,215,0,.04);color:rgba(255,215,0,.3)}
.slot-filled-first{border:2.5px solid #ffd700;background:rgba(255,215,0,.1)}
.slot-filled{border:2px solid rgba(6,182,212,.5);background:rgba(6,182,212,.07)}
.slot-k{border:2.5px solid #f59e0b!important;background:rgba(245,158,11,.1)!important}

/* ITEMS */
.item-row{display:flex;gap:7px;justify-content:center;flex-wrap:wrap}
.item{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:.85rem;font-weight:700;
  border:2px solid;cursor:pointer;transition:all .22s;user-select:none}
.item:hover:not(.dim){transform:translateY(-3px);box-shadow:0 4px 12px rgba(0,0,0,.5)}
.item.dim{opacity:.16;pointer-events:none}
.item.special-k{animation:glowK 1.4s ease-in-out infinite alternate}
@keyframes glowK{from{box-shadow:0 0 6px rgba(245,158,11,.4)}to{box-shadow:0 0 16px rgba(245,158,11,.8)}}

/* RESULT FORMULA */
.result-formula{font-family:'Courier New',monospace;font-size:.9rem;color:#ffd700;
  background:rgba(255,215,0,.08);border:1.5px solid rgba(255,215,0,.25);
  border-radius:9px;padding:8px 12px;text-align:center;margin-top:10px;
  animation:pop .3s ease}
.vis-desc{font-size:.77rem;color:#94a3b8;text-align:center;margin-top:8px;
  min-height:34px;line-height:1.65}

/* INSIGHT */
.insight{background:rgba(59,130,246,.07);border:1px solid rgba(59,130,246,.22);
  border-radius:9px;padding:11px 14px;font-size:1.0rem;color:#93c5fd;
  margin-top:8px;line-height:1.75}

/* BUTTONS */
.btn{padding:6px 14px;border-radius:8px;border:1.5px solid;
  font-family:inherit;font-size:.8rem;cursor:pointer;transition:all .2s}
.btn:hover{transform:translateY(-1px)}
.btn-gray{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.15);color:#9ca3af}
.btn-blue{background:rgba(79,156,249,.1);border-color:rgba(79,156,249,.35);color:#4f9cf9}
.btn-gold{background:rgba(255,215,0,.08);border-color:rgba(255,215,0,.3);color:#ffd700}
.btn-row{display:flex;gap:7px;flex-wrap:wrap;margin-top:8px}

/* CASE TALLY */
.tally{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}
.tally-box{border-radius:10px;padding:10px;text-align:center}
.tally-i{background:rgba(59,130,246,.08);border:1.5px solid rgba(59,130,246,.3)}
.tally-ii{background:rgba(245,158,11,.08);border:1.5px solid rgba(245,158,11,.3)}
.tally-num{font-size:2rem;font-weight:700}
.tally-i .tally-num{color:#60a5fa}
.tally-ii .tally-num{color:#f59e0b}
.tally-lbl{font-size:.68rem;color:#7788aa;margin-top:2px;line-height:1.4}
.tally-sub{font-size:.7rem;font-family:'Courier New',monospace;margin-top:3px}
.tally-i .tally-sub{color:#93c5fd}
.tally-ii .tally-sub{color:#fbbf24}

/* PROGRESS */
.prog-wrap{background:rgba(255,255,255,.05);border-radius:99px;height:9px;
  margin-bottom:4px;overflow:hidden}
.prog-bar{height:100%;border-radius:99px;
  background:linear-gradient(90deg,#3b82f6,#8b5cf6,#f59e0b);transition:width .4s ease}
.prog-lbl{font-size:.7rem;color:#7788aa;text-align:center;margin-bottom:6px}

/* CLASS BADGE */
.class-badge{display:inline-block;padding:5px 14px;border-radius:99px;
  font-size:.8rem;font-weight:700;animation:pop .3s ease}
.class-i{background:rgba(59,130,246,.15);color:#60a5fa;border:1.5px solid rgba(59,130,246,.4)}
.class-ii{background:rgba(245,158,11,.15);color:#f59e0b;border:1.5px solid rgba(245,158,11,.4)}

/* K SELECTOR */
.k-sel{display:flex;gap:5px;justify-content:center;flex-wrap:wrap;margin-bottom:10px}
.k-btn{width:40px;height:40px;border-radius:50%;border:2px solid;
  font-family:inherit;font-size:.8rem;font-weight:700;cursor:pointer;transition:all .2s}
.k-btn:hover{transform:scale(1.1)}

/* RL TABS */
.rl-tabs{display:flex;gap:4px;margin-bottom:10px;flex-wrap:wrap}
.rl-tab{padding:7px 12px;border:1.5px solid rgba(255,255,255,.12);border-radius:8px;
  font-family:inherit;font-size:.76rem;cursor:pointer;background:transparent;
  color:#7788aa;transition:all .2s}
.rl-tab:hover{color:#dde8ff;background:rgba(255,255,255,.06)}
.rl-tab.active{background:rgba(167,139,250,.12);color:#a78bfa;border-color:rgba(167,139,250,.4)}
.rl-panel{display:none}
.rl-panel.active{display:block;animation:fadein .2s ease}

/* RUNNERS / PODIUM */
.runners-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px}
.runner{display:flex;flex-direction:column;align-items:center;gap:3px;
  cursor:pointer;transition:all .2s}
.runner:hover:not(.used){transform:translateY(-4px)}
.runner.used{opacity:.2;pointer-events:none}
.runner-c{width:62px;height:62px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:1.45rem;border:2px solid rgba(255,255,255,.2);
  transition:all .2s}
.runner-n{font-size:.62rem;color:#9ca3af}
.podium-wrap{display:flex;align-items:flex-end;justify-content:center;gap:8px;margin:6px 0 10px}
.pod-col{display:flex;flex-direction:column;align-items:center;gap:3px}
.pod-circle{width:66px;height:66px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:1.5rem;border:2px solid rgba(255,255,255,.15);
  opacity:.35;transition:all .3s}
.pod-circle.filled{opacity:1;animation:pop .3s ease}
.pod-block{border-radius:8px 8px 0 0;display:flex;align-items:center;
  justify-content:center;font-size:1.3rem;width:78px}

/* SONGS */
.songs-row{display:flex;gap:7px;justify-content:center;flex-wrap:wrap;margin-bottom:10px}
.song-card{display:flex;flex-direction:column;align-items:center;gap:3px;
  cursor:pointer;transition:all .2s;padding:7px 8px;border-radius:10px;
  border:1.5px solid rgba(255,255,255,.1);background:rgba(255,255,255,.03);min-width:56px}
.song-card:hover:not(.used){transform:translateY(-3px);border-color:rgba(167,139,250,.5)}
.song-card.used{opacity:.2;pointer-events:none}
.song-icon{font-size:1.5rem}
.song-name{font-size:.6rem;color:#9ca3af;text-align:center}
.playlist{display:flex;gap:7px;justify-content:center;flex-wrap:wrap;margin-bottom:8px}
.pl-slot{width:74px;border:2px dashed rgba(167,139,250,.3);border-radius:10px;
  padding:8px 5px;text-align:center;min-height:82px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;transition:all .3s;gap:3px}
.pl-slot.filled{border-style:solid;border-color:rgba(167,139,250,.6);
  background:rgba(167,139,250,.07)}
.pl-lbl{font-size:.6rem;color:#7788aa;margin-top:2px}

/* NUMPAD / LOCK */
.num-display{display:flex;gap:8px;justify-content:center;margin-bottom:10px}
.nbox{width:70px;height:84px;border-radius:11px;background:rgba(0,0,0,.4);
  border:2px solid rgba(255,255,255,.1);display:flex;align-items:center;
  justify-content:center;font-size:2.4rem;font-weight:700;color:#4b5563;transition:all .3s}
.nbox.filled{border-color:rgba(139,92,246,.6);background:rgba(139,92,246,.1);
  color:#a78bfa;animation:pop .3s ease}
.numpad{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;max-width:280px;margin:0 auto}
.npbtn{padding:10px 4px;border:1.5px solid rgba(139,92,246,.3);border-radius:8px;
  background:rgba(139,92,246,.07);color:#a78bfa;font-size:1rem;font-weight:700;
  cursor:pointer;font-family:inherit;transition:all .2s}
.npbtn:hover:not(:disabled){background:rgba(139,92,246,.22);transform:translateY(-1px)}
.npbtn:disabled{opacity:.2;cursor:default}

/* VERIFY TABLE */
.vtbl{width:100%;border-collapse:collapse;font-size:1.1rem;margin-top:6px}
.vtbl th{padding:7px 9px;text-align:left;color:#7788aa;
  border-bottom:1px solid rgba(255,255,255,.1)}
.vtbl td{padding:8px 9px;border-bottom:1px solid rgba(255,255,255,.05);vertical-align:middle}
.vtbl .mono{font-family:'Courier New',monospace;color:#e2e8ff}
.vtbl .ok{color:#34d399;font-weight:700}
.vtbl .chk{color:#34d399;font-size:1.4rem}
/* ARRANGEMENT LOG */
.arr-logs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}
.arr-log{border-radius:10px;padding:8px 10px}
.arr-log-i{background:rgba(59,130,246,.06);border:1.5px solid rgba(59,130,246,.25)}
.arr-log-ii{background:rgba(245,158,11,.06);border:1.5px solid rgba(245,158,11,.25)}
.arr-log-hdr{font-size:.72rem;font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:4px}
.arr-log-i .arr-log-hdr{color:#60a5fa}
.arr-log-ii .arr-log-hdr{color:#f59e0b}
.arr-log-body{display:flex;flex-wrap:wrap;gap:3px;min-height:28px}
.arr-chip{display:inline-flex;align-items:center;gap:2px;
  padding:3px 5px;border-radius:6px;background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.1);animation:pop .25s ease}
.arr-chip .ac{width:19px;height:19px;border-radius:50%;display:inline-flex;
  align-items:center;justify-content:center;font-size:.58rem;font-weight:700}
.arr-chip .ac-arr{font-size:.6rem;color:rgba(255,255,255,.3)}

.verify-section{display:none;animation:fadein .3s ease}
.verify-section.show{display:block}

@keyframes fadein{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
@keyframes pop{0%{transform:scale(.7)}60%{transform:scale(1.12)}100%{transform:scale(1)}}
</style>
</head>
<body>

<div class="hdr">
  <div class="hdr-title">🔍 순열 등식 탐구</div>
  <div class="hdr-sub">두 가지 순열 등식을 직접 조작하며 발견해봅시다</div>
</div>

<div class="main-tabs">
  <button class="main-tab active" onclick="switchMain(0)">① <sub>n</sub>P<sub>r</sub> = n × <sub>n−1</sub>P<sub>r−1</sub></button>
  <button class="main-tab" onclick="switchMain(1)">② <sub>n</sub>P<sub>r</sub> = <sub>n−1</sub>P<sub>r</sub> + r×<sub>n−1</sub>P<sub>r−1</sub></button>
  <button class="main-tab" onclick="switchMain(2)">🌍 실생활 탐구</button>
</div>


<!-- ══ PANEL 0: 등식 ① ══ -->
<div id="mp0" class="main-panel active">
  <div class="fml-wrap">
    <div class="fml-main"><sub>n</sub>P<sub>r</sub> = n × <sub>n−1</sub>P<sub>r−1</sub></div>
    <div class="fml-cond">( n ≥ 2,  1 ≤ r ≤ n )</div>
  </div>

  <div class="sl-row">
    <span class="sl-lbl">n =</span>
    <input type="range" id="e1n" min="2" max="6" value="4"
      oninput="e1nv.textContent=this.value;e1Init()">
    <span id="e1nv" class="sl-val">4</span>
    <span class="sl-lbl" style="margin-left:8px">r =</span>
    <input type="range" id="e1r" min="1" max="4" value="2"
      oninput="e1rv.textContent=this.value;e1Init()">
    <span id="e1rv" class="sl-val">2</span>
  </div>

  <div class="live-eq">
    <span class="leq-lhs" id="e1_lhs">4P2 = 12</span>
    <span class="leq-eq">=</span>
    <span class="leq-rhs" id="e1_rhs">4 × ₃P₁ = 4×3 = 12</span>
    <span style="color:#34d399">✓</span>
  </div>

  <div class="vis">
    <div class="vis-hint" id="e1_hint">
      💡 아래 원소 중 하나를 클릭해 <strong style="color:#ffd700">첫 번째 자리(금색 칸)</strong>에 배치해보세요!
    </div>
    <div class="slot-row" id="e1_slots"></div>
    <div class="item-row" id="e1_items"></div>
    <div class="vis-desc" id="e1_desc">원소를 클릭하면 슬롯에 차례대로 들어갑니다</div>
    <div id="e1_result" style="display:none" class="result-formula"></div>
  </div>

  <div class="btn-row">
    <button class="btn btn-gray" onclick="e1Init()">↩ 초기화</button>
  </div>

  <div class="insight">
    💡 <strong>핵심:</strong> 첫 번째 자리에 올 수 있는 원소는 <strong>n가지</strong>입니다.<br>
    그 원소를 고정하면 나머지 <strong>n−1개</strong> 중 <strong>r−1개</strong>를 나열하는
    <strong><sub>n−1</sub>P<sub>r−1</sub></strong>가지 방법이 남습니다.<br>
    ∴ <strong><sub>n</sub>P<sub>r</sub> = n × <sub>n−1</sub>P<sub>r−1</sub></strong>
  </div>
</div>


<!-- ══ PANEL 1: 등식 ② ══ -->
<div id="mp1" class="main-panel">
  <div class="fml-wrap">
    <div class="fml-main"><sub>n</sub>P<sub>r</sub> = <sub>n−1</sub>P<sub>r</sub> + r × <sub>n−1</sub>P<sub>r−1</sub></div>
    <div class="fml-cond">( n ≥ 2,  1 ≤ r ≤ n−1 )</div>
  </div>

  <div class="sl-row">
    <span class="sl-lbl">n =</span>
    <input type="range" id="e2n" min="3" max="6" value="4"
      oninput="e2nv.textContent=this.value;e2Init()">
    <span id="e2nv" class="sl-val">4</span>
    <span class="sl-lbl" style="margin-left:8px">r =</span>
    <input type="range" id="e2r" min="1" max="3" value="2"
      oninput="e2rv.textContent=this.value;e2Init()">
    <span id="e2rv" class="sl-val">2</span>
  </div>

  <div class="live-eq">
    <span class="leq-lhs" id="e2_lhs">4P2 = 12</span>
    <span class="leq-eq">=</span>
    <span class="leq-rhs" id="e2_rhs">₃P₂ + 2×₃P₁ = 6+6 = 12</span>
    <span style="color:#34d399">✓</span>
  </div>

  <div class="vis">
    <div class="vis-hint">
      <span id="e2_klabel" style="color:#f59e0b;font-weight:700">A★</span>가
      배열에 포함되는지 여부로 두 경우로 나눌 수 있습니다.<br>
      원소를 클릭해 <span id="e2_r_hint">2</span>개짜리 배열을 만들어 분류해보세요!
    </div>

    <div style="font-size:.7rem;color:#7788aa;text-align:center;margin-bottom:5px">
      ★ 특별 원소 k 선택:
    </div>
    <div class="k-sel" id="e2_ksel"></div>

    <div class="item-row" id="e2_items" style="margin-bottom:12px"></div>
    <div class="slot-row" id="e2_slots"></div>

    <div id="e2_badge" style="text-align:center;min-height:30px;margin-bottom:6px"></div>

    <div class="tally">
      <div class="tally-box tally-i">
        <div class="tally-num" id="e2_ci">0</div>
        <div class="tally-lbl">k 미포함 배열<br>(경우 i)</div>
        <div class="tally-sub" id="e2_ci_fml">목표: ?</div>
      </div>
      <div class="tally-box tally-ii">
        <div class="tally-num" id="e2_cii">0</div>
        <div class="tally-lbl">k 포함 배열<br>(경우 ii)</div>
        <div class="tally-sub" id="e2_cii_fml">목표: ?</div>
      </div>
    </div>

    <div class="prog-wrap">
      <div class="prog-bar" id="e2_prog" style="width:0%"></div>
    </div>
    <div class="prog-lbl" id="e2_prog_lbl">0 / ? 가지 발견</div>

    <!-- 발견한 배열 기록 -->
    <div class="arr-logs">
      <div class="arr-log arr-log-i">
        <div class="arr-log-hdr">🔵 경우 i: k 미포함 &nbsp;<span id="e2_ci_cnt" style="opacity:.6">(0가지)</span></div>
        <div class="arr-log-body" id="e2_log_i"></div>
      </div>
      <div class="arr-log arr-log-ii">
        <div class="arr-log-hdr">🟡 경우 ii: k 포함 &nbsp;<span id="e2_cii_cnt" style="opacity:.6">(0가지)</span></div>
        <div class="arr-log-body" id="e2_log_ii"></div>
      </div>
    </div>

    <div id="e2_complete" style="display:none;text-align:center;padding:8px;
      background:rgba(16,185,129,.07);border:1px solid rgba(16,185,129,.25);
      border-radius:9px;font-size:.82rem;font-weight:700;color:#34d399;animation:pop .4s ease">
      🎉 모든 경우 발견!&nbsp; 경우i + 경우ii = <span id="e2_total_txt"></span> = <sub>n</sub>P<sub>r</sub> ✓
    </div>
  </div>

  <div class="btn-row">
    <button class="btn btn-blue" onclick="e2Next()">▶ 다음 배열 시도</button>
    <button class="btn btn-gray" onclick="e2Init()">↩ 처음부터</button>
  </div>

  <div class="insight">
    💡 <strong>핵심:</strong> n개 중 r개를 고르는 모든 배열을<br>
    <strong style="color:#60a5fa">k가 없는 경우 (<sub>n−1</sub>P<sub>r</sub>가지)</strong>와
    <strong style="color:#f59e0b">k가 있는 경우 (r × <sub>n−1</sub>P<sub>r−1</sub>가지)</strong>로 나눌 수 있어요.<br>
    두 경우는 동시에 일어날 수 없으므로 합의 법칙으로 더합니다.<br>
    <em style="color:#7788aa">k 포함 시: 나머지 n−1개 중 r−1개를 먼저 배열하고, k를 r개 위치 중 하나에 삽입 → r × <sub>n−1</sub>P<sub>r−1</sub></em>
  </div>
</div>


<!-- ══ PANEL 2: 실생활 탐구 ══ -->
<div id="mp2" class="main-panel">
  <div style="font-size:.76rem;color:#7788aa;text-align:center;margin-bottom:10px">
    5개 중 3개를 선택·배열하는 실생활 상황 — 직접 조작하며 두 등식을 확인해봅시다!
  </div>

  <div class="rl-tabs">
    <button class="rl-tab active" onclick="switchRL(0)">🏅 달리기 시상</button>
    <button class="rl-tab" onclick="switchRL(1)">🎵 재생목록</button>
    <button class="rl-tab" onclick="switchRL(2)">🔐 자물쇠 번호</button>
  </div>

  <!-- RL0: 달리기 시상 -->
  <div id="rl0" class="rl-panel active">
    <div class="vis">
      <div style="font-size:.82rem;color:#ffd700;font-weight:700;text-align:center;margin-bottom:5px">
        🏃 달리기 대회 — 5명 중 금·은·동 시상
      </div>
      <div style="font-size:.74rem;color:#94a3b8;text-align:center;margin-bottom:10px">
        선수를 클릭해 시상대에 올려봅시다!
      </div>
      <div id="rl0_runners" class="runners-row"></div>
      <div class="podium-wrap" id="rl0_podium"></div>
      <div id="rl0_msg" style="text-align:center;min-height:22px;font-size:.76rem;color:#7788aa"></div>
    </div>
    <div class="verify-section" id="rl0_verify">
      <table class="vtbl">
        <thead><tr><th>등식</th><th>계산</th><th>결과</th><th></th></tr></thead>
        <tbody>
          <tr>
            <td style="color:#94a3b8;font-size:1.0rem">₅P₃</td>
            <td class="mono">5×4×3</td>
            <td class="ok">60가지</td><td></td>
          </tr>
          <tr>
            <td style="color:#ffd700;font-size:1.0rem;line-height:1.5">등식①<br>n×<sub>n-1</sub>P<sub>r-1</sub></td>
            <td class="mono">5 × ₄P₂<br>= 5×12</td>
            <td class="ok">60가지</td><td class="chk">✅</td>
          </tr>
          <tr>
            <td style="color:#60a5fa;font-size:1.0rem;line-height:1.5">등식②<br><sub>n-1</sub>P<sub>r</sub>+r×<sub>n-1</sub>P<sub>r-1</sub></td>
            <td class="mono">₄P₃+3×₄P₂<br>= 24+36</td>
            <td class="ok">60가지</td><td class="chk">✅</td>
          </tr>
        </tbody>
      </table>
      <div class="insight" style="margin-top:8px">
        💡 <strong>등식① 의미:</strong> 금메달 받을 선수를 5명 중 먼저 결정(5가지),
        나머지 4명 중 2명에게 은·동 배정(₄P₂=12가지)<br>
        💡 <strong>등식② 의미:</strong> 선수 A가 시상 <em>없는</em> 경우(₄P₃=24가지) +
        <em>받는</em> 경우(나머지 4명 중 2명 배열 후 A를 3자리 중 삽입 → 3×₄P₂=36가지)
      </div>
    </div>
    <div class="btn-row">
      <button class="btn btn-gray" onclick="rl0Reset()">↩ 다시하기</button>
    </div>
  </div>

  <!-- RL1: 재생목록 -->
  <div id="rl1" class="rl-panel">
    <div class="vis">
      <div style="font-size:.82rem;color:#ffd700;font-weight:700;text-align:center;margin-bottom:5px">
        🎵 재생목록 — 5곡 중 3곡을 순서대로 재생
      </div>
      <div style="font-size:.74rem;color:#94a3b8;text-align:center;margin-bottom:10px">
        곡을 클릭해 재생 순서를 정해봅시다!
      </div>
      <div class="songs-row" id="rl1_songs"></div>
      <div class="playlist" id="rl1_playlist"></div>
      <div id="rl1_msg" style="text-align:center;min-height:22px;font-size:.76rem;color:#7788aa"></div>
    </div>
    <div class="verify-section" id="rl1_verify">
      <table class="vtbl">
        <thead><tr><th>등식</th><th>계산</th><th>결과</th><th></th></tr></thead>
        <tbody>
          <tr>
            <td style="color:#94a3b8;font-size:1.0rem">₅P₃</td>
            <td class="mono">5×4×3</td>
            <td class="ok">60가지</td><td></td>
          </tr>
          <tr>
            <td style="color:#ffd700;font-size:1.0rem;line-height:1.5">등식①<br>n×<sub>n-1</sub>P<sub>r-1</sub></td>
            <td class="mono">5 × ₄P₂<br>= 5×12</td>
            <td class="ok">60가지</td><td class="chk">✅</td>
          </tr>
          <tr>
            <td style="color:#60a5fa;font-size:1.0rem;line-height:1.5">등식②<br><sub>n-1</sub>P<sub>r</sub>+r×<sub>n-1</sub>P<sub>r-1</sub></td>
            <td class="mono">₄P₃+3×₄P₂<br>= 24+36</td>
            <td class="ok">60가지</td><td class="chk">✅</td>
          </tr>
        </tbody>
      </table>
      <div class="insight" style="margin-top:8px">
        💡 <strong>등식① 의미:</strong> 첫 번째 곡을 5곡 중 먼저 선택(5가지),
        나머지 4곡 중 2곡 순서 결정(₄P₂=12가지)<br>
        💡 <strong>등식② 의미:</strong> 곡 ♩A가 재생목록에 <em>없는</em> 경우(₄P₃=24가지) +
        <em>있는</em> 경우(나머지 4곡 중 2곡 배열 후 ♩A 삽입 → 3×₄P₂=36가지)
      </div>
    </div>
    <div class="btn-row">
      <button class="btn btn-gray" onclick="rl1Reset()">↩ 다시하기</button>
    </div>
  </div>

  <!-- RL2: 자물쇠 번호 -->
  <div id="rl2" class="rl-panel">
    <div class="vis">
      <div style="font-size:.82rem;color:#ffd700;font-weight:700;text-align:center;margin-bottom:5px">
        🔐 자물쇠 번호 — 1~5 중 서로 다른 3자리
      </div>
      <div style="font-size:.74rem;color:#94a3b8;text-align:center;margin-bottom:8px">
        숫자를 클릭해 3자리 비밀번호를 만들어봅시다!
      </div>
      <div id="rl2_lock" style="text-align:center;font-size:2rem;margin-bottom:8px">🔒</div>
      <div class="num-display" id="rl2_disp"></div>
      <div class="numpad" id="rl2_pad"></div>
      <div id="rl2_msg" style="text-align:center;margin-top:8px;min-height:22px;
        font-size:.76rem;color:#7788aa"></div>
    </div>
    <div class="verify-section" id="rl2_verify">
      <table class="vtbl">
        <thead><tr><th>등식</th><th>계산</th><th>결과</th><th></th></tr></thead>
        <tbody>
          <tr>
            <td style="color:#94a3b8;font-size:1.0rem">₅P₃</td>
            <td class="mono">5×4×3</td>
            <td class="ok">60가지</td><td></td>
          </tr>
          <tr>
            <td style="color:#ffd700;font-size:1.0rem;line-height:1.5">등식①<br>n×<sub>n-1</sub>P<sub>r-1</sub></td>
            <td class="mono">5 × ₄P₂<br>= 5×12</td>
            <td class="ok">60가지</td><td class="chk">✅</td>
          </tr>
          <tr>
            <td style="color:#60a5fa;font-size:1.0rem;line-height:1.5">등식②<br><sub>n-1</sub>P<sub>r</sub>+r×<sub>n-1</sub>P<sub>r-1</sub></td>
            <td class="mono">₄P₃+3×₄P₂<br>= 24+36</td>
            <td class="ok">60가지</td><td class="chk">✅</td>
          </tr>
        </tbody>
      </table>
      <div class="insight" style="margin-top:8px">
        💡 <strong>등식① 의미:</strong> 첫 번째 자리를 5개 중 선택(5가지),
        나머지 4개 중 2개 순서 결정(₄P₂=12가지)<br>
        💡 <strong>등식② 의미:</strong> 숫자 1이 비밀번호에 <em>없는</em> 경우(₄P₃=24가지) +
        <em>있는</em> 경우(나머지 4개 중 2개 배열 후 1을 3자리 중 삽입 → 3×₄P₂=36가지)
      </div>
    </div>
    <div class="btn-row">
      <button class="btn btn-gray" onclick="rl2Reset()">↩ 다시하기</button>
      <button class="btn btn-gold" onclick="rl2Back()">⌫ 하나 지우기</button>
    </div>
  </div>

</div><!-- end mp2 -->


<script>
// ─── UTILS ───────────────────────────────────────────────────────
function pnr(n, r) {
  if (r === 0) return 1;
  if (r > n || n < 0) return 0;
  let v = 1;
  for (let i = n; i > n - r; i--) v *= i;
  return v;
}
const C = ['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#06b6d4'];
const L = ['A','B','C','D','E','F'];

function switchMain(i) {
  document.querySelectorAll('.main-tab').forEach((t,j)=>t.classList.toggle('active',i===j));
  document.querySelectorAll('.main-panel').forEach((p,j)=>p.classList.toggle('active',i===j));
}
function switchRL(i) {
  document.querySelectorAll('.rl-tab').forEach((t,j)=>t.classList.toggle('active',i===j));
  document.querySelectorAll('.rl-panel').forEach((p,j)=>p.classList.toggle('active',i===j));
}


// ─── PANEL 0: 등식 ① ─────────────────────────────────────────────
let e1_n=4, e1_r=2, e1_arr=[], e1_done=false;

function e1Init() {
  const rEl = document.getElementById('e1r');
  e1_n = parseInt(document.getElementById('e1n').value);
  rEl.max = e1_n;
  e1_r = Math.min(parseInt(rEl.value), e1_n);
  rEl.value = e1_r;
  document.getElementById('e1rv').textContent = e1_r;

  const lhs = pnr(e1_n, e1_r);
  const sub = pnr(e1_n-1, e1_r-1);
  document.getElementById('e1_lhs').textContent = e1_n+'P'+e1_r+' = '+lhs;
  document.getElementById('e1_rhs').textContent =
    e1_n+' × '+(e1_n-1)+'P'+(e1_r-1)+' = '+e1_n+'×'+sub+' = '+lhs;

  e1_arr = []; e1_done = false;
  document.getElementById('e1_result').style.display = 'none';
  document.getElementById('e1_hint').innerHTML =
    '💡 아래 원소 중 하나를 클릭해 <strong style="color:#ffd700">첫 번째 자리(금색 칸)</strong>에 배치해보세요!';
  document.getElementById('e1_desc').textContent = '원소를 클릭하면 슬롯에 차례대로 들어갑니다';
  e1Render();
}

function e1Render() {
  let sh = '';
  for (let i = 0; i < e1_r; i++) {
    const v = e1_arr[i];
    const filled = v !== undefined;
    let cls = 'slot ';
    if (filled) cls += (i===0 ? 'slot-filled-first' : 'slot-filled');
    else cls += (i===0 ? 'slot-first-empty' : 'slot-empty');
    const style = filled
      ? 'background:'+C[v]+'22;border-color:'+C[v]+';color:'+C[v]
      : '';
    sh += '<div class="slot-wrap"><div class="'+cls+'" style="'+style+'">'+
          (filled ? L[v] : (i===0 ? '?' : '···'))+'</div>'+
          '<div class="slot-lbl">'+(i+1)+'번째 자리</div></div>';
  }
  document.getElementById('e1_slots').innerHTML = sh;

  let ih = '';
  for (let i = 0; i < e1_n; i++) {
    const used = e1_arr.includes(i);
    ih += '<div class="item '+(used?'dim':'')+'" '+
          'style="background:'+C[i]+'22;border-color:'+C[i]+';color:'+C[i]+'" '+
          'onclick="e1Pick('+i+')">'+L[i]+'</div>';
  }
  document.getElementById('e1_items').innerHTML = ih;
}

function e1Pick(idx) {
  if (e1_done || e1_arr.includes(idx) || e1_arr.length >= e1_r) return;
  e1_arr.push(idx);

  if (e1_arr.length === 1) {
    document.getElementById('e1_desc').innerHTML =
      '✅ 첫 번째 자리에 <strong style="color:'+C[idx]+'">'+L[idx]+'</strong> 배치! '+
      '→ 남은 <strong>'+(e1_n-1)+'</strong>개 중 <strong>'+(e1_r-1)+'</strong>개를 더 골라보세요.';
  }

  if (e1_arr.length === e1_r) {
    e1_done = true;
    const sub = pnr(e1_n-1, e1_r-1);
    const total = pnr(e1_n, e1_r);
    document.getElementById('e1_desc').innerHTML =
      '🎉 완성! 첫 자리 선택 → <strong style="color:#ffd700">'+e1_n+'가지</strong> &nbsp;×&nbsp; '+
      '<sub>'+(e1_n-1)+'</sub>P<sub>'+(e1_r-1)+'</sub> = '+
      '<strong style="color:#67e8f9">'+sub+'</strong> &nbsp;= <strong style="color:#34d399">'+total+'</strong>';
    const resEl = document.getElementById('e1_result');
    resEl.style.display = 'block';
    resEl.textContent = e1_n+'P'+e1_r+' = '+e1_n+' × '+(e1_n-1)+'P'+(e1_r-1)+
                        ' = '+e1_n+'×'+sub+' = '+total+' ✓';
  }
  e1Render();
}


// ─── PANEL 1: 등식 ② ─────────────────────────────────────────────
let e2_n=4, e2_r=2, e2_k=0;
let e2_ci=0, e2_cii=0, e2_arr=[], e2_seen=new Set(), e2_done=false;
let e2_list_i=[], e2_list_ii=[];

function e2Init() {
  const rEl = document.getElementById('e2r');
  e2_n = parseInt(document.getElementById('e2n').value);
  rEl.max = e2_n - 1;
  e2_r = Math.min(parseInt(rEl.value), e2_n-1);
  if (e2_r < 1) e2_r = 1;
  rEl.value = e2_r;
  document.getElementById('e2rv').textContent = e2_r;
  if (e2_k >= e2_n) e2_k = 0;

  e2_ci = 0; e2_cii = 0; e2_arr = []; e2_seen = new Set(); e2_done = false;
  e2_list_i = []; e2_list_ii = [];

  const lhs = pnr(e2_n, e2_r);
  const a = pnr(e2_n-1, e2_r), b = e2_r * pnr(e2_n-1, e2_r-1);
  document.getElementById('e2_lhs').textContent = e2_n+'P'+e2_r+' = '+lhs;
  document.getElementById('e2_rhs').textContent =
    (e2_n-1)+'P'+e2_r+' + '+e2_r+'×'+(e2_n-1)+'P'+(e2_r-1)+' = '+a+'+'+b+' = '+lhs;

  document.getElementById('e2_r_hint').textContent = e2_r;
  document.getElementById('e2_klabel').textContent = L[e2_k]+'★';
  document.getElementById('e2_ci').textContent = '0';
  document.getElementById('e2_cii').textContent = '0';
  document.getElementById('e2_ci_fml').textContent = '목표: '+(e2_n-1)+'P'+e2_r+' = '+a+'가지';
  document.getElementById('e2_cii_fml').textContent = '목표: '+e2_r+'×'+(e2_n-1)+'P'+(e2_r-1)+' = '+b+'가지';
  document.getElementById('e2_badge').innerHTML = '';
  document.getElementById('e2_prog').style.width = '0%';
  document.getElementById('e2_prog_lbl').textContent = '0 / '+lhs+'가지 발견';
  document.getElementById('e2_complete').style.display = 'none';
  document.getElementById('e2_log_i').innerHTML = '';
  document.getElementById('e2_log_ii').innerHTML = '';
  document.getElementById('e2_ci_cnt').textContent = '(0가지)';
  document.getElementById('e2_cii_cnt').textContent = '(0가지)';
  e2RenderKSel();
  e2RenderItems();
  e2RenderSlots();
}

function e2RenderKSel() {
  let h = '';
  for (let i = 0; i < e2_n; i++) {
    const act = i === e2_k;
    h += '<button class="k-btn" onclick="e2SetK('+i+')" style="'+
         'background:'+(act ? C[i]+'33' : 'rgba(255,255,255,.05)')+';'+
         'border-color:'+(act ? C[i] : 'rgba(255,255,255,.2)')+';'+
         'color:'+(act ? C[i] : '#7788aa')+'">'+L[i]+'</button>';
  }
  document.getElementById('e2_ksel').innerHTML = h;
}

function e2SetK(idx) {
  e2_k = idx;
  document.getElementById('e2_klabel').textContent = L[idx]+'★';
  e2_arr = [];
  e2_ci = 0; e2_cii = 0; e2_seen = new Set(); e2_done = false;
  e2_list_i = []; e2_list_ii = [];
  document.getElementById('e2_badge').innerHTML = '';
  document.getElementById('e2_ci').textContent = '0';
  document.getElementById('e2_cii').textContent = '0';
  document.getElementById('e2_log_i').innerHTML = '';
  document.getElementById('e2_log_ii').innerHTML = '';
  document.getElementById('e2_ci_cnt').textContent = '(0가지)';
  document.getElementById('e2_cii_cnt').textContent = '(0가지)';
  document.getElementById('e2_prog').style.width = '0%';
  document.getElementById('e2_complete').style.display = 'none';
  const total = pnr(e2_n, e2_r);
  document.getElementById('e2_prog_lbl').textContent = '0 / '+total+'가지 발견';
  e2RenderKSel();
  e2RenderItems();
  e2RenderSlots();
}

function e2RenderItems() {
  let h = '';
  for (let i = 0; i < e2_n; i++) {
    const used = e2_arr.includes(i);
    const isK = i === e2_k;
    h += '<div class="item'+(used?' dim':'')+(isK?' special-k':'')+'" '+
         'style="background:'+C[i]+'22;border-color:'+C[i]+';color:'+C[i]+'" '+
         'onclick="e2PickItem('+i+')">'+L[i]+(isK?'★':'')+'</div>';
  }
  document.getElementById('e2_items').innerHTML = h;
}

function e2RenderSlots() {
  let h = '';
  for (let i = 0; i < e2_r; i++) {
    const v = e2_arr[i];
    const filled = v !== undefined;
    const isK = filled && v === e2_k;
    let cls = 'slot ';
    if (filled) cls += (isK ? 'slot-k' : 'slot-filled');
    else cls += 'slot-empty';
    const style = filled ? 'background:'+C[v]+'22;border-color:'+C[v]+';color:'+C[v] : '';
    h += '<div class="slot-wrap"><div class="'+cls+'" style="'+style+'">'+
         (filled ? L[v]+(isK?'★':'') : '?')+'</div>'+
         '<div class="slot-lbl">'+(i+1)+'번째</div></div>';
  }
  document.getElementById('e2_slots').innerHTML = h;
}

function e2PickItem(idx) {
  if (e2_arr.length >= e2_r || e2_arr.includes(idx)) return;
  e2_arr.push(idx);
  e2RenderItems();
  e2RenderSlots();
  if (e2_arr.length === e2_r) e2Classify();
}

function e2Classify() {
  const hasK = e2_arr.includes(e2_k);
  const key = e2_arr.join(',');
  const badgeEl = document.getElementById('e2_badge');

  if (hasK) {
    badgeEl.innerHTML = '<span class="class-badge class-ii">경우 ii) '+L[e2_k]+
      '★ 포함 → r×(n−1)P(r−1) 항에 해당</span>';
  } else {
    badgeEl.innerHTML = '<span class="class-badge class-i">경우 i) '+L[e2_k]+
      '★ 미포함 → (n−1)Pr 항에 해당</span>';
  }

  if (!e2_seen.has(key)) {
    e2_seen.add(key);
    if (hasK) { e2_cii++; e2_list_ii.push([...e2_arr]); }
    else       { e2_ci++;  e2_list_i.push([...e2_arr]); }
    document.getElementById('e2_ci').textContent = e2_ci;
    document.getElementById('e2_cii').textContent = e2_cii;
    e2RenderLists();

    const total = pnr(e2_n, e2_r);
    const pct = Math.min(100, Math.round(e2_seen.size / total * 100));
    document.getElementById('e2_prog').style.width = pct+'%';
    document.getElementById('e2_prog_lbl').textContent =
      e2_seen.size+' / '+total+'가지 발견 ('+pct+'%)';

    if (!e2_done && e2_seen.size >= total) {
      e2_done = true;
      const a = pnr(e2_n-1, e2_r), b = e2_r * pnr(e2_n-1, e2_r-1);
      const comp = document.getElementById('e2_complete');
      comp.style.display = 'block';
      document.getElementById('e2_total_txt').textContent = a+' + '+b+' = '+total;
    }
  }
}

function e2RenderLists() {
  function chipHtml(arr) {
    let h = '<div class="arr-chip">';
    for (let i = 0; i < arr.length; i++) {
      const idx = arr[i];
      if (i > 0) h += '<span class="ac-arr">→</span>';
      h += '<span class="ac" style="background:'+C[idx]+'33;border:1.5px solid '+C[idx]+
           ';color:'+C[idx]+'">'+L[idx]+(idx===e2_k?'★':'')+'</span>';
    }
    h += '</div>';
    return h;
  }
  document.getElementById('e2_log_i').innerHTML  = e2_list_i.map(chipHtml).join('');
  document.getElementById('e2_log_ii').innerHTML = e2_list_ii.map(chipHtml).join('');
  document.getElementById('e2_ci_cnt').textContent  = '('+e2_ci+'가지)';
  document.getElementById('e2_cii_cnt').textContent = '('+e2_cii+'가지)';
}

function e2Next() {
  e2_arr = [];
  document.getElementById('e2_badge').innerHTML = '';
  e2RenderItems();
  e2RenderSlots();
}


// ─── RL0: 달리기 시상 ─────────────────────────────────────────────
const RUNNERS = [
  {name:'민준',emoji:'🏃',c:'#ef4444'},
  {name:'서연',emoji:'🏃\u200d♀️',c:'#3b82f6'},
  {name:'지우',emoji:'🤸',c:'#10b981'},
  {name:'예린',emoji:'🤸\u200d♀️',c:'#f59e0b'},
  {name:'준혁',emoji:'🧗',c:'#8b5cf6'},
];
let rl0_podium=[null,null,null], rl0_used=new Set();

function rl0Render() {
  document.getElementById('rl0_runners').innerHTML = RUNNERS.map((r,i)=>
    '<div class="runner '+(rl0_used.has(i)?'used':'')+'" onclick="rl0Pick('+i+')">'+
    '<div class="runner-c" style="background:'+r.c+'33;border-color:'+r.c+'">'+r.emoji+'</div>'+
    '<div class="runner-n">'+r.name+'</div></div>'
  ).join('');

  const medals=['🥇','🥈','🥉'], heights=[100,76,60];
  const blockC=['#ca8a04','#94a3b8','#78716c'];
  const order=[1,0,2];
  document.getElementById('rl0_podium').innerHTML = order.map(rank => {
    const v = rl0_podium[rank];
    const r = v !== null ? RUNNERS[v] : null;
    return '<div class="pod-col">'+
      '<div class="pod-circle '+(r?'filled':'')+'" '+
      'style="background:'+(r?r.c+'33':'rgba(255,255,255,.06)')+';'+
      'border-color:'+(r?r.c:'rgba(255,255,255,.15)')+'">'+(r?r.emoji:'?')+'</div>'+
      '<div style="font-size:.6rem;min-height:13px;text-align:center;color:'+(r?'#e2e8ff':'#4b5563')+'">'+(r?r.name:'')+'</div>'+
      '<div class="pod-block" style="height:'+heights[rank]+'px;background:'+blockC[rank]+'">'+medals[rank]+'</div>'+
      '</div>';
  }).join('');
}

function rl0Pick(i) {
  if (rl0_used.has(i)) return;
  const next = rl0_podium.findIndex(v=>v===null);
  if (next === -1) return;
  rl0_podium[next] = i; rl0_used.add(i); rl0Render();
  const medals=['🥇','🥈','🥉'];
  if (rl0_podium.every(v=>v!==null)) {
    document.getElementById('rl0_msg').innerHTML =
      '<span style="color:#34d399;font-weight:700">🎉 시상 완성! ₅P₃=60가지 중 하나입니다</span>';
    document.getElementById('rl0_verify').classList.add('show');
  } else {
    document.getElementById('rl0_msg').textContent =
      medals[next]+' '+RUNNERS[i].name+' 배정! ('+rl0_podium.filter(v=>v!==null).length+'/3)';
  }
}

function rl0Reset() {
  rl0_podium=[null,null,null]; rl0_used=new Set();
  document.getElementById('rl0_msg').textContent='';
  document.getElementById('rl0_verify').classList.remove('show');
  rl0Render();
}
rl0Render();


// ─── RL1: 재생목록 ────────────────────────────────────────────────
const SONGS = [
  {name:'봄날',emoji:'🌸',c:'#f472b6'},
  {name:'파란하늘',emoji:'☁️',c:'#38bdf8'},
  {name:'달빛',emoji:'🌙',c:'#a78bfa'},
  {name:'여름',emoji:'🌊',c:'#34d399'},
  {name:'불꽃',emoji:'🔥',c:'#f59e0b'},
];
let rl1_playlist=[null,null,null], rl1_used=new Set();

function rl1RenderSongs() {
  document.getElementById('rl1_songs').innerHTML = SONGS.map((s,i)=>
    '<div class="song-card '+(rl1_used.has(i)?'used':'')+'" onclick="rl1Pick('+i+')" '+
    'style="'+(rl1_used.has(i)?'':'border-color:'+s.c+'44')+'">'+
    '<div class="song-icon">'+s.emoji+'</div>'+
    '<div class="song-name" style="color:'+s.c+'">'+s.name+'</div></div>'
  ).join('');
}

function rl1RenderPlaylist() {
  const labels=['1번째','2번째','3번째'];
  document.getElementById('rl1_playlist').innerHTML = rl1_playlist.map((v,i)=>
    '<div class="pl-slot '+(v!==null?'filled':'')+'" '+
    'style="'+(v!==null?'border-color:'+SONGS[v].c+';background:'+SONGS[v].c+'15':'')+'">'+
    (v!==null
      ? '<div style="font-size:1.4rem">'+SONGS[v].emoji+'</div>'+
        '<div style="font-size:.62rem;color:'+SONGS[v].c+'">'+SONGS[v].name+'</div>'
      : '<div style="font-size:1.4rem;opacity:.2">♪</div>')+
    '<div class="pl-lbl">'+labels[i]+'</div></div>'
  ).join('');
}

function rl1Pick(i) {
  if (rl1_used.has(i)) return;
  const next = rl1_playlist.findIndex(v=>v===null);
  if (next === -1) return;
  rl1_playlist[next] = i; rl1_used.add(i);
  rl1RenderSongs(); rl1RenderPlaylist();
  if (rl1_playlist.every(v=>v!==null)) {
    document.getElementById('rl1_msg').innerHTML =
      '<span style="color:#34d399;font-weight:700">🎉 재생목록 완성! ₅P₃=60가지 중 하나입니다</span>';
    document.getElementById('rl1_verify').classList.add('show');
  } else {
    document.getElementById('rl1_msg').textContent =
      (next+1)+'번째에 '+SONGS[i].name+' 추가! ('+(next+1)+'/3)';
  }
}

function rl1Reset() {
  rl1_playlist=[null,null,null]; rl1_used=new Set();
  document.getElementById('rl1_msg').textContent='';
  document.getElementById('rl1_verify').classList.remove('show');
  rl1RenderSongs(); rl1RenderPlaylist();
}
rl1RenderSongs(); rl1RenderPlaylist();


// ─── RL2: 자물쇠 ─────────────────────────────────────────────────
let rl2_pw=[null,null,null], rl2_used=new Set();

function rl2RenderDisp() {
  document.getElementById('rl2_disp').innerHTML =
    rl2_pw.map(v=>'<div class="nbox '+(v!==null?'filled':'')+'">'+
      (v!==null?v:'·')+'</div>').join('');
}

function rl2RenderPad() {
  document.getElementById('rl2_pad').innerHTML =
    [1,2,3,4,5].map(d=>
      '<button class="npbtn" onclick="rl2Pick('+d+')" '+
      (rl2_used.has(d)?'disabled':'')+'>'+d+'</button>'
    ).join('');
}

function rl2Pick(d) {
  if (rl2_used.has(d)) return;
  const next = rl2_pw.findIndex(v=>v===null);
  if (next === -1) return;
  rl2_pw[next] = d; rl2_used.add(d);
  rl2RenderDisp(); rl2RenderPad();
  if (rl2_pw.every(v=>v!==null)) {
    document.getElementById('rl2_lock').textContent = '🔓';
    document.getElementById('rl2_msg').innerHTML =
      '<span style="color:#34d399;font-weight:700">🎉 비밀번호 '+rl2_pw.join('-')+
      ' 완성! ₅P₃=60가지 중 하나입니다</span>';
    document.getElementById('rl2_verify').classList.add('show');
  } else {
    document.getElementById('rl2_msg').textContent =
      '입력 중... ('+rl2_pw.filter(v=>v!==null).length+'/3)';
  }
}

function rl2Back() {
  const lastIdx = rl2_pw.map((v,i)=>v!==null?i:-1).filter(i=>i>=0).pop();
  if (lastIdx === undefined) return;
  rl2_used.delete(rl2_pw[lastIdx]); rl2_pw[lastIdx] = null;
  document.getElementById('rl2_msg').textContent = '';
  document.getElementById('rl2_lock').textContent = '🔒';
  document.getElementById('rl2_verify').classList.remove('show');
  rl2RenderDisp(); rl2RenderPad();
}

function rl2Reset() {
  rl2_pw=[null,null,null]; rl2_used=new Set();
  document.getElementById('rl2_msg').textContent='';
  document.getElementById('rl2_lock').textContent='🔒';
  document.getElementById('rl2_verify').classList.remove('show');
  rl2RenderDisp(); rl2RenderPad();
}
rl2RenderDisp(); rl2RenderPad();


// ─── INIT ─────────────────────────────────────────────────────────
e1Init();
e2Init();
</script>
</body>
</html>"""


def render():
    st.markdown("### 🔍 순열 등식 탐구")
    st.markdown(
        "두 가지 **순열 등식**을 직접 조작하며 탐구해보세요!"
    )
    components.html(_HTML, height=1850, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
