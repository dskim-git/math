# activities/common/mini/combination_identity_explorer.py
"""
조합 등식 탐구 — 4가지 조합 등식을 실생활 상황에서 직접 조작하며 탐구하는 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "조합등식탐구"

META = {
    "title":       "🔢 조합 등식 탐구",
    "description": "4가지 조합 등식을 실생활 상황에서 직접 조작하며 '조합의 의미'로 탐구합니다.",
    "order":       342,
    "hidden":      False,
}

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "eq1_insight",
        "label":  "① ₙCᵣ = ₙCₙ₋ᵣ 가 성립하는 이유를 조합의 의미로 자신의 말로 설명해보세요. (아이스크림 선택 상황을 이용해도 좋아요!)",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "eq2_insight",
        "label":  "② ₙCᵣ = ₙ₋₁Cᵣ + ₙ₋₁Cᵣ₋₁ 에서 왜 두 경우로 나누었나요? 두 경우가 서로 겹치지 않으면서 전체를 이루는 이유는 무엇인가요?",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "eq3_insight",
        "label":  "③ r·ₙCᵣ = n·ₙ₋₁Cᵣ₋₁ 에서 '팀 먼저 뽑고 대표 선출'과 '대표 먼저 선출하고 팀 완성'이 같은 결과를 내는 이유를 설명해보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "eq4_insight",
        "label":  "④ ₙCᵣ × ᵣCₖ = ₙCₖ × ₙ₋ₖCᵣ₋ₖ 에서 두 방법이 '같은 상황을 다른 순서로 센 것'임을 자신의 말로 설명해보세요.",
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
  color:#dde8ff;padding:10px 12px 28px;
}

/* HEADER */
.hdr{text-align:center;padding:10px 0 14px}
.hdr-title{font-size:1.4rem;font-weight:700;color:#ffd700;
  text-shadow:0 0 22px rgba(255,215,0,.45);letter-spacing:.5px}
.hdr-sub{font-size:.76rem;color:#7788aa;margin-top:5px}

/* STARS */
.stars-wrap{display:flex;justify-content:center;gap:14px;margin-bottom:16px;
  background:rgba(255,255,255,.03);border-radius:14px;padding:10px 14px}
.star-item{text-align:center;font-size:.63rem;color:#374151;transition:all .3s;cursor:default}
.star-item .star-ico{font-size:1.8rem;filter:grayscale(1) opacity(.28);
  transition:all .45s;display:block;margin-bottom:2px}
.star-item.earned .star-ico{filter:none;animation:starPop .55s ease}
.star-item.earned{color:#7788aa}
@keyframes starPop{
  0%{transform:scale(.4) rotate(-25deg)}
  55%{transform:scale(1.3) rotate(8deg)}
  100%{transform:scale(1) rotate(0)}
}

/* MAIN TABS */
.id-tabs{display:flex;gap:5px;margin-bottom:14px;flex-wrap:wrap}
.id-tab{flex:1;min-width:138px;padding:10px 7px;
  border:1.5px solid rgba(255,255,255,.1);border-radius:11px;
  font-family:inherit;font-size:.68rem;font-weight:600;
  cursor:pointer;background:rgba(255,255,255,.02);color:#7788aa;
  transition:all .22s;text-align:center;line-height:1.55}
.id-tab:hover{color:#dde8ff;background:rgba(255,255,255,.07)}
.id-tab.active{color:#ffd700;background:rgba(255,215,0,.1);
  border-color:rgba(255,215,0,.42)}
.id-tab.done{color:#34d399;background:rgba(52,211,153,.07);
  border-color:rgba(52,211,153,.38)}
.id-panel{display:none}
.id-panel.active{display:block;animation:fadein .3s ease}
@keyframes fadein{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}

/* FORMULA CARD */
.fml-card{
  background:linear-gradient(135deg,rgba(255,215,0,.1),rgba(255,215,0,.03));
  border:2px solid rgba(255,215,0,.38);border-radius:15px;
  padding:13px 18px;margin-bottom:13px;text-align:center}
.fml-main{font-size:1.28rem;font-weight:700;color:#ffd700;margin-bottom:4px}
.fml-cond{font-size:.71rem;color:#94a3b8}

/* CONTEXT */
.ctx{background:rgba(103,232,249,.04);border-left:3.5px solid rgba(103,232,249,.38);
  border-radius:0 10px 10px 0;padding:10px 13px;margin-bottom:12px;
  font-size:.79rem;color:#94a3b8;line-height:1.75}
.ctx strong{color:#67e8f9}
.ctx em{color:#c4b5fd;font-style:normal}

/* INSTRUCTION */
.instr{background:rgba(255,255,255,.03);border:1px dashed rgba(255,255,255,.15);
  border-radius:9px;padding:9px 13px;margin-bottom:11px;
  font-size:.78rem;color:#cbd5e1;line-height:1.65;text-align:center}

/* ITEMS GRID */
.items-grid{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;
  padding:14px 10px;background:rgba(0,0,0,.22);border-radius:14px;margin-bottom:13px}
.ic{width:80px;height:94px;border-radius:14px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:5px;
  font-size:2rem;cursor:pointer;border:2.5px solid;
  transition:all .25s;user-select:none;position:relative}
.ic .ic-lbl{font-size:.65rem;font-weight:700;line-height:1.1;text-align:center}
.ic:hover:not(.ic-dim):not(.ic-done-item){transform:translateY(-5px) scale(1.07);z-index:2}
.ic-normal{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.14);color:#7788aa}
.ic-normal .ic-lbl{color:#6b7280}
.ic-sel{background:rgba(79,156,249,.16);border-color:#4f9cf9;color:#93c5fd;
  transform:translateY(-4px);box-shadow:0 5px 18px rgba(79,156,249,.35)}
.ic-sel .ic-lbl{color:#93c5fd}
.ic-rej{background:rgba(251,146,60,.12);border-color:rgba(251,146,60,.55);color:#fdba74}
.ic-rej .ic-lbl{color:#fb923c}
.ic-gold{background:rgba(251,191,36,.15);border-color:#fbbf24;color:#fbbf24;
  box-shadow:0 4px 16px rgba(251,191,36,.3)}
.ic-gold .ic-lbl{color:#fbbf24}
.ic-star-glow{animation:glowstar 1.5s ease-in-out infinite alternate}
.ic-dim{opacity:.18;pointer-events:none}
.ic-done-item{cursor:default}
@keyframes glowstar{
  from{box-shadow:0 0 8px rgba(251,191,36,.5)}
  to{box-shadow:0 0 22px rgba(251,191,36,.95)}
}

/* COMPARE GRID */
.compare{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-bottom:13px}
.compare-col{border-radius:13px;padding:12px}
.compare-left{background:rgba(79,156,249,.07);border:1.5px solid rgba(79,156,249,.26)}
.compare-right{background:rgba(251,146,60,.07);border:1.5px solid rgba(251,146,60,.26)}
.compare-head{font-size:.8rem;font-weight:700;margin-bottom:8px}
.compare-left .compare-head{color:#60a5fa}
.compare-right .compare-head{color:#fb923c}
.compare-desc{font-size:.74rem;color:#94a3b8;line-height:1.65;margin-bottom:8px}
.compare-desc strong{color:#cbd5e1}
.step-lbl{font-size:.72rem;font-weight:700;margin-bottom:5px}
.step-lbl-blue{color:#4f9cf9}
.step-lbl-gold{color:#fbbf24}
.step-lbl-dim{opacity:.38}

/* SMALL ITEMS */
.sm-items{display:flex;flex-wrap:wrap;gap:5px;min-height:44px;
  padding:5px;background:rgba(0,0,0,.18);border-radius:9px;
  align-items:center;margin-bottom:7px}
.sic{width:60px;height:70px;border-radius:11px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:3px;
  font-size:1.55rem;cursor:pointer;border:2px solid;
  transition:all .22s;user-select:none}
.sic .sic-lbl{font-size:.6rem;font-weight:700;text-align:center}
.sic:hover:not(.sic-dim){transform:translateY(-3px) scale(1.06)}
.sic-normal{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.14);color:#7788aa}
.sic-normal .sic-lbl{color:#6b7280}
.sic-sel{background:rgba(79,156,249,.16);border-color:#4f9cf9;color:#93c5fd;
  transform:translateY(-2px)}
.sic-sel .sic-lbl{color:#93c5fd}
.sic-gold{background:rgba(251,191,36,.16);border-color:#fbbf24;color:#fbbf24}
.sic-gold .sic-lbl{color:#fbbf24}
.sic-orange{background:rgba(251,146,60,.14);border-color:#fb923c;color:#fdba74}
.sic-orange .sic-lbl{color:#fb923c}
.sic-dim{opacity:.18;pointer-events:none}

/* RESULT BOX */
.result-box{font-family:'Courier New',monospace;font-size:.92rem;color:#ffd700;
  background:rgba(255,215,0,.08);border:1.5px solid rgba(255,215,0,.26);
  border-radius:10px;padding:8px 12px;text-align:center;margin-top:6px;
  min-height:36px;line-height:1.5}

/* TALLY */
.tally-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.tbox{border-radius:12px;padding:12px;text-align:center}
.tbox-blue{background:rgba(59,130,246,.08);border:2px solid rgba(59,130,246,.3)}
.tbox-orange{background:rgba(251,146,60,.08);border:2px solid rgba(251,146,60,.3)}
.tbox-num{font-size:2.5rem;font-weight:700;line-height:1}
.tbox-blue .tbox-num{color:#60a5fa}
.tbox-orange .tbox-num{color:#fb923c}
.tbox-lbl{font-size:.68rem;color:#7788aa;margin-top:4px;line-height:1.45}
.tbox-formula{font-family:'Courier New',monospace;font-size:.73rem;margin-top:5px}
.tbox-blue .tbox-formula{color:#93c5fd}
.tbox-orange .tbox-formula{color:#fdba74}

/* PROGRESS */
.prog-wrap{background:rgba(255,255,255,.06);border-radius:99px;height:8px;
  overflow:hidden;margin-bottom:3px}
.prog-bar{height:100%;border-radius:99px;transition:width .4s ease;
  background:linear-gradient(90deg,#3b82f6,#8b5cf6,#f59e0b)}
.prog-lbl{font-size:.7rem;color:#7788aa;text-align:center;margin-bottom:9px}

/* COMBO LOG */
.combo-log{max-height:110px;overflow-y:auto;background:rgba(0,0,0,.22);
  border-radius:9px;padding:7px 10px;font-size:.71rem;color:#94a3b8;
  line-height:1.85;margin-bottom:10px}
.combo-log::-webkit-scrollbar{width:4px}
.combo-log::-webkit-scrollbar-thumb{background:rgba(255,255,255,.15);border-radius:4px}

/* LIVE EQ */
.live-eq{display:flex;align-items:center;justify-content:center;gap:10px;
  background:rgba(0,0,0,.3);border:1.5px solid rgba(255,255,255,.1);
  border-radius:12px;padding:11px 14px;margin-bottom:11px;flex-wrap:wrap}
.leq-lhs{font-family:'Courier New',monospace;font-size:1.05rem;
  font-weight:700;color:#4f9cf9}
.leq-sign{color:#4b5563;font-size:1.5rem;font-weight:700;transition:color .3s}
.leq-rhs{font-family:'Courier New',monospace;font-size:1.05rem;
  font-weight:700;color:#fb923c}

/* SUCCESS BANNER */
.success{background:linear-gradient(135deg,rgba(52,211,153,.15),rgba(52,211,153,.04));
  border:2.5px solid rgba(52,211,153,.52);border-radius:15px;
  padding:16px;text-align:center;margin-bottom:11px;display:none}
.success.show{display:block;animation:pop .5s ease}
.success-emoji{font-size:2.6rem;margin-bottom:5px}
.success-title{color:#34d399;font-weight:700;font-size:1.05rem;margin-bottom:6px}
.success-body{font-size:.8rem;color:#6ee7b7;line-height:1.7}
.success-body strong{color:#a7f3d0}
@keyframes pop{0%{transform:scale(.8);opacity:0}60%{transform:scale(1.04)}100%{transform:scale(1);opacity:1}}

/* CTRL */
.ctrl-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:11px;
  background:rgba(255,255,255,.03);border-radius:9px;padding:8px 12px}
.ctrl-lbl{font-size:.8rem;color:#7788aa}
.ctrl-val{background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.28);
  border-radius:6px;padding:2px 9px;font-size:.9rem;font-weight:700;color:#ffd700}
input[type=range]{accent-color:#ffd700;width:88px;cursor:pointer}

/* BUTTONS */
.btn{padding:7px 16px;border-radius:9px;border:1.5px solid;font-family:inherit;
  font-size:.8rem;cursor:pointer;transition:all .2s;font-weight:600}
.btn:hover{transform:translateY(-1px)}
.btn-gray{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.14);color:#9ca3af}
.btn-gold{background:rgba(255,215,0,.08);border-color:rgba(255,215,0,.3);color:#ffd700}
.btn-row{display:flex;gap:7px;flex-wrap:wrap;margin-top:4px}

/* NOTE BOX */
.note{background:rgba(167,139,250,.06);border:1px solid rgba(167,139,250,.2);
  border-radius:9px;padding:9px 12px;margin-bottom:10px;
  font-size:.76rem;color:#c4b5fd;line-height:1.65}
</style>
</head>
<body>

<!-- HEADER -->
<div class="hdr">
  <div class="hdr-title">🔢 조합 등식 탐구</div>
  <div class="hdr-sub">4가지 조합 등식을 실생활로 직접 체험하며 이해해 보세요!</div>
</div>

<!-- STARS -->
<div class="stars-wrap">
  <div class="star-item" id="star0">
    <span class="star-ico">⭐</span>등식①
  </div>
  <div class="star-item" id="star1">
    <span class="star-ico">⭐</span>등식②
  </div>
  <div class="star-item" id="star2">
    <span class="star-ico">⭐</span>등식③
  </div>
  <div class="star-item" id="star3">
    <span class="star-ico">⭐</span>등식④
  </div>
</div>

<!-- TABS -->
<div class="id-tabs">
  <button class="id-tab active" id="tab0" onclick="showTab(0)">
    ① ₙCᵣ = ₙCₙ₋ᵣ<br><span style="font-size:.63rem;opacity:.75">대칭성</span>
  </button>
  <button class="id-tab" id="tab1" onclick="showTab(1)">
    ② ₙCᵣ = ₙ₋₁Cᵣ + ₙ₋₁Cᵣ₋₁<br><span style="font-size:.63rem;opacity:.75">포함/제외</span>
  </button>
  <button class="id-tab" id="tab2" onclick="showTab(2)">
    ③ r·ₙCᵣ = n·ₙ₋₁Cᵣ₋₁<br><span style="font-size:.63rem;opacity:.75">대표 선출</span>
  </button>
  <button class="id-tab" id="tab3" onclick="showTab(3)">
    ④ ₙCᵣ×ᵣCₖ = ₙCₖ×ₙ₋ₖCᵣ₋ₖ<br><span style="font-size:.63rem;opacity:.75">두 팀 나누기</span>
  </button>
</div>

<!-- ═══════════════════════════════════════════════════════ -->
<!-- PANEL 1: nCr = nC(n-r)                                  -->
<!-- ═══════════════════════════════════════════════════════ -->
<div class="id-panel active" id="panel0">
  <div class="fml-card">
    <div class="fml-main">ₙCᵣ = ₙCₙ₋ᵣ</div>
    <div class="fml-cond">단, 0 ≤ r ≤ n</div>
  </div>
  <div class="ctx">
    <strong>🍦 아이스크림 가게</strong><br>
    n가지 맛 중 r가지를 선택할 때,<br>
    <em>"r가지를 고르는 방법"</em>과 <em>"나머지 n−r가지를 제외하는 방법"</em>은 사실 같은 일입니다!<br>
    슬라이더로 n, r을 바꿔 보고, 아이스크림을 직접 골라보세요.
  </div>
  <div class="ctrl-row">
    <span class="ctrl-lbl">전체 맛 수 <strong>n</strong></span>
    <input type="range" min="4" max="8" value="6" oninput="e1SetN(+this.value)">
    <span class="ctrl-val" id="e1_n_val">6</span>
    <span class="ctrl-lbl" style="margin-left:10px">선택할 수 <strong>r</strong></span>
    <input type="range" min="0" max="6" value="2" id="e1_r_slider" oninput="e1SetR(+this.value)">
    <span class="ctrl-val" id="e1_r_val">2</span>
  </div>
  <div class="instr">
    👆 <strong id="e1_instr_n">6</strong>가지 아이스크림 중 <strong id="e1_instr_r">2</strong>가지를 클릭해 골라보세요!
  </div>
  <div class="items-grid" id="e1_items"></div>

  <div class="compare">
    <div class="compare-col compare-left">
      <div class="compare-head">🔵 선택한 것 (ₙCᵣ 쪽)</div>
      <div id="e1_sel_area" style="min-height:52px;display:flex;flex-wrap:wrap;gap:7px;align-items:center;padding:6px">
        <span style="font-size:.72rem;color:#374151">여기에 선택 표시됩니다...</span>
      </div>
      <div class="result-box" id="e1_lhs">₆C₂ = 15</div>
    </div>
    <div class="compare-col compare-right">
      <div class="compare-head">🟠 제외된 것 (ₙCₙ₋ᵣ 쪽)</div>
      <div id="e1_rej_area" style="min-height:52px;display:flex;flex-wrap:wrap;gap:7px;align-items:center;padding:6px">
        <span style="font-size:.72rem;color:#374151">선택하면 제외된 것이 표시됩니다...</span>
      </div>
      <div class="result-box" id="e1_rhs">₆C₄ = 15</div>
    </div>
  </div>

  <div class="live-eq">
    <span class="leq-lhs" id="e1_eq_lhs">₆C₂ = 15</span>
    <span class="leq-sign" id="e1_eq_sign">≟</span>
    <span class="leq-rhs" id="e1_eq_rhs">₆C₄ = 15</span>
  </div>

  <div class="success" id="e1_success">
    <div class="success-emoji">🎉</div>
    <div class="success-title">발견했어요!</div>
    <div class="success-body" id="e1_body">
      r가지를 선택하는 경우의 수 = n−r가지를 제외하는 경우의 수!<br>
      선택 = "버리지 않을 것을 고르는 것"
    </div>
  </div>

  <div class="note">
    💡 <strong>핵심 아이디어:</strong> r개를 선택하면 나머지 n−r개는 자동으로 제외됩니다.<br>
    즉, "선택할 r개를 고르는 것"과 "제외할 n−r개를 고르는 것"은 완전히 같은 행동이에요!
  </div>
  <div class="btn-row">
    <button class="btn btn-gray" onclick="e1Reset()">🔄 초기화</button>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════ -->
<!-- PANEL 2: nCr = (n-1)Cr + (n-1)C(r-1)                   -->
<!-- ═══════════════════════════════════════════════════════ -->
<div class="id-panel" id="panel1">
  <div class="fml-card">
    <div class="fml-main">ₙCᵣ = ₙ₋₁Cᵣ + ₙ₋₁Cᵣ₋₁</div>
    <div class="fml-cond">단, 1 ≤ r ≤ n−1</div>
  </div>
  <div class="ctx">
    <strong>🏫 학교 대표팀 선발 (n=5, r=2)</strong><br>
    5명의 학생 중 2명을 대표로 선발합니다. <em>⭐ 은별</em>이가 포함되는지 여부에 따라 경우를 나눠보세요!<br>
    <em>i) 은별 포함</em> → 나머지 4명 중 1명 추가 = ₄C₁ = 4가지<br>
    <em>ii) 은별 제외</em> → 은별 빼고 4명 중 2명 선발 = ₄C₂ = 6가지<br>
    합계: 4 + 6 = <strong>₅C₂ = 10가지</strong>
  </div>
  <div class="instr">
    👆 <strong>⭐ 은별</strong>이를 포함해서도, 제외해서도 선발해보세요!<br>
    학생 2명을 클릭하면 자동으로 분류됩니다. 총 <strong>10가지</strong> 조합을 모두 찾아보세요!
  </div>
  <div class="items-grid" id="e2_items"></div>

  <div class="tally-row">
    <div class="tbox tbox-blue">
      <div class="tbox-num" id="e2_cnt_in">0</div>
      <div class="tbox-lbl">⭐ 은별 <strong>포함</strong> 팀</div>
      <div class="tbox-formula" id="e2_f_in">ₙ₋₁Cᵣ₋₁ = ₄C₁ = 4</div>
    </div>
    <div class="tbox tbox-orange">
      <div class="tbox-num" id="e2_cnt_out">0</div>
      <div class="tbox-lbl">⭐ 은별 <strong>제외</strong> 팀</div>
      <div class="tbox-formula" id="e2_f_out">ₙ₋₁Cᵣ = ₄C₂ = 6</div>
    </div>
  </div>
  <div class="prog-wrap"><div class="prog-bar" id="e2_prog" style="width:0%"></div></div>
  <div class="prog-lbl" id="e2_prog_lbl">0 / 10가지 발견</div>
  <div class="combo-log" id="e2_log"></div>

  <div class="success" id="e2_success">
    <div class="success-emoji">🎊</div>
    <div class="success-title">10가지를 모두 발견했어요!</div>
    <div class="success-body">
      <strong>⭐ 은별 포함:</strong> ₄C₁ = 4가지<br>
      <strong>⭐ 은별 제외:</strong> ₄C₂ = 6가지<br>
      4 + 6 = 10 = <strong>₅C₂</strong> &nbsp;✓
    </div>
  </div>

  <div class="note">
    💡 <strong>핵심 아이디어:</strong> 특정 원소 k를 고려하면 전체 경우는 반드시<br>
    "k 포함(n−1C r−1)" 또는 "k 제외(n−1Cr)" 중 하나입니다. 이 둘은 겹치지 않으므로 더할 수 있어요!
  </div>
  <div class="btn-row">
    <button class="btn btn-gray" onclick="e2Reset()">🔄 초기화</button>
    <button class="btn btn-gold" onclick="e2ShowAll()">✨ 모두 보기</button>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════ -->
<!-- PANEL 3: r·nCr = n·(n-1)C(r-1)                         -->
<!-- ═══════════════════════════════════════════════════════ -->
<div class="id-panel" id="panel2">
  <div class="fml-card">
    <div class="fml-main">r · ₙCᵣ = n · ₙ₋₁Cᵣ₋₁</div>
    <div class="fml-cond">단, 1 ≤ r ≤ n</div>
  </div>
  <div class="ctx">
    <strong>⚽ 동아리 팀 구성 + 대표 선출 (n=5, r=3)</strong><br>
    5명 중 3명의 팀을 구성하고 그 팀에서 대표 1명을 선출하는 방법의 수를<br>
    <em>두 가지 방법</em>으로 세어봅시다. 결과가 같나요?
  </div>

  <div class="compare">
    <div class="compare-col compare-left">
      <div class="compare-head">🔵 방법 1 (좌변: r·ₙCᵣ)</div>
      <div class="compare-desc">
        <strong>① 팀 3명 먼저 선발</strong> → ₅C₃ = 10가지<br>
        <strong>② 팀원 중 대표 1명 선출</strong> → 3가지<br>
        합계 = 10 × 3 = <strong>30가지</strong>
      </div>
      <div class="step-lbl step-lbl-blue" id="e3_lbl_s1a">① 팀원 3명 클릭해 선발하세요</div>
      <div class="sm-items" id="e3_m1_pool"></div>
      <div class="step-lbl step-lbl-gold step-lbl-dim" id="e3_lbl_s2a">② 팀원 중 대표 1명을 클릭하세요 (팀 완성 후)</div>
      <div class="sm-items" id="e3_m1_rep_pool"></div>
      <div class="result-box" id="e3_m1_result">r·ₙCᵣ = 3 × ₅C₃ = 30</div>
    </div>
    <div class="compare-col compare-right">
      <div class="compare-head">🟠 방법 2 (우변: n·ₙ₋₁Cᵣ₋₁)</div>
      <div class="compare-desc">
        <strong>① 대표 1명 먼저 선출</strong> → 5가지<br>
        <strong>② 나머지 4명 중 팀원 2명 선발</strong> → ₄C₂ = 6가지<br>
        합계 = 5 × 6 = <strong>30가지</strong>
      </div>
      <div class="step-lbl step-lbl-gold" id="e3_lbl_s1b">① 대표가 될 1명을 먼저 클릭하세요</div>
      <div class="sm-items" id="e3_m2_pool"></div>
      <div class="step-lbl step-lbl-blue step-lbl-dim" id="e3_lbl_s2b">② 나머지 중 팀원 2명 클릭 (대표 선출 후)</div>
      <div class="sm-items" id="e3_m2_team_pool"></div>
      <div class="result-box" id="e3_m2_result">n·ₙ₋₁Cᵣ₋₁ = 5 × ₄C₂ = 30</div>
    </div>
  </div>

  <div class="success" id="e3_success">
    <div class="success-emoji">🌟</div>
    <div class="success-title">두 방법 모두 완성! 결과가 같네요!</div>
    <div class="success-body">
      방법 1 (팀→대표): r·ₙCᵣ = 3 × 10 = <strong>30</strong><br>
      방법 2 (대표→팀): n·ₙ₋₁Cᵣ₋₁ = 5 × 6 = <strong>30</strong><br>
      ∴ r·ₙCᵣ = n·ₙ₋₁Cᵣ₋₁
    </div>
  </div>

  <div class="note">
    💡 <strong>핵심 아이디어:</strong> "팀 먼저 뽑고 대표 선출" = "대표 먼저 뽑고 팀 완성"<br>
    두 방법 모두 같은 (팀, 대표) 쌍을 세기 때문에 결과가 반드시 같습니다!
  </div>
  <div class="btn-row">
    <button class="btn btn-gray" onclick="e3Reset()">🔄 초기화</button>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════ -->
<!-- PANEL 4: nCr × rCk = nCk × (n-k)C(r-k)                 -->
<!-- ═══════════════════════════════════════════════════════ -->
<div class="id-panel" id="panel3">
  <div class="fml-card">
    <div class="fml-main">ₙCᵣ × ᵣCₖ = ₙCₖ × ₙ₋ₖCᵣ₋ₖ</div>
    <div class="fml-cond">단, 0 &lt; k &lt; r ≤ n</div>
  </div>
  <div class="ctx">
    <strong>🏃 체육대회 두 팀 배정 (n=5, r=3, k=2)</strong><br>
    5명 중 3명을 선발해 <em>A팀(2명)</em>과 <em>B팀(1명)</em>으로 배정하는 방법의 수를<br>
    <em>두 가지 방법</em>으로 세어봅시다. 결과가 같나요?
  </div>

  <div class="compare">
    <div class="compare-col compare-left">
      <div class="compare-head">🔵 방법 1 (좌변: ₅C₃ × ₃C₂)</div>
      <div class="compare-desc">
        <strong>① 5명 중 3명 선발</strong> → ₅C₃ = 10가지<br>
        <strong>② 선발된 3명 중 A팀 2명 지정</strong> → ₃C₂ = 3가지<br>
        나머지 1명은 자동으로 B팀!<br>
        합계 = 10 × 3 = <strong>30가지</strong>
      </div>
      <div class="step-lbl step-lbl-blue" id="e4_lbl_s1a">① 3명 선발 클릭</div>
      <div class="sm-items" id="e4_m1_pool"></div>
      <div class="step-lbl" id="e4_lbl_s2a" style="color:#f472b6;font-size:.72rem;font-weight:700;margin-bottom:5px" class="step-lbl-dim">② A팀 2명 지정 클릭 (선발 완료 후)</div>
      <div class="sm-items" id="e4_m1_ateam_pool"></div>
      <div id="e4_m1_bteam_info" style="font-size:.7rem;color:#fb923c;min-height:18px;margin-bottom:5px"></div>
      <div class="result-box" id="e4_m1_result">₅C₃ × ₃C₂ = 10 × 3 = 30</div>
    </div>
    <div class="compare-col compare-right">
      <div class="compare-head">🟠 방법 2 (우변: ₅C₂ × ₃C₁)</div>
      <div class="compare-desc">
        <strong>① A팀 2명 바로 선택</strong> → ₅C₂ = 10가지<br>
        <strong>② 나머지 3명 중 B팀 1명 선택</strong> → ₃C₁ = 3가지<br>
        합계 = 10 × 3 = <strong>30가지</strong>
      </div>
      <div class="step-lbl step-lbl-blue" id="e4_lbl_s1b">① A팀 2명 클릭</div>
      <div class="sm-items" id="e4_m2_pool"></div>
      <div class="step-lbl step-lbl-gold step-lbl-dim" id="e4_lbl_s2b">② B팀 1명 클릭 (A팀 선택 후)</div>
      <div class="sm-items" id="e4_m2_bteam_pool"></div>
      <div class="result-box" id="e4_m2_result">₅C₂ × ₃C₁ = 10 × 3 = 30</div>
    </div>
  </div>

  <div class="success" id="e4_success">
    <div class="success-emoji">🏆</div>
    <div class="success-title">두 방법 모두 완성! 결과가 같네요!</div>
    <div class="success-body">
      방법 1 (선발→팀 분리): ₅C₃ × ₃C₂ = 10 × 3 = <strong>30</strong><br>
      방법 2 (A팀→B팀 순서): ₅C₂ × ₃C₁ = 10 × 3 = <strong>30</strong><br>
      ∴ ₙCᵣ × ᵣCₖ = ₙCₖ × ₙ₋ₖCᵣ₋ₖ
    </div>
  </div>

  <div class="note">
    💡 <strong>핵심 아이디어:</strong> "먼저 전체 선발 후 팀 분리" = "A팀 먼저, B팀 나중에"<br>
    두 방법 모두 같은 (A팀, B팀) 배정을 세고 있기 때문에 결과가 반드시 같습니다!
  </div>
  <div class="btn-row">
    <button class="btn btn-gray" onclick="e4Reset()">🔄 초기화</button>
  </div>
</div>

<script>
/* ====================================================
   UTILITIES
   ==================================================== */
function C(n, r) {
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  r = Math.min(r, n - r);
  let v = 1;
  for (let i = 0; i < r; i++) v = v * (n - i) / (i + 1);
  return Math.round(v);
}

const S0=['₀','₁','₂','₃','₄','₅','₆','₇','₈','₉'];
function sub(n){return String(n).split('').map(c=>S0[+c]).join('');}
function Cstr(n,r){return sub(n)+'C'+sub(r);}

const DONE = new Set();
function markDone(i) {
  if (DONE.has(i)) return;
  DONE.add(i);
  document.getElementById('tab'+i).classList.add('done');
  document.getElementById('star'+i).classList.add('earned');
}

function showTab(i) {
  document.querySelectorAll('.id-tab').forEach((t,j)=>t.classList.toggle('active',i===j));
  document.querySelectorAll('.id-panel').forEach((p,j)=>p.classList.toggle('active',i===j));
}

/* ====================================================
   IDENTITY 1 — nCr = nC(n-r)
   ==================================================== */
const FLAVORS = ['🍓','🍫','🍵','🍋','🥭','🍑','🍇','🍒'];
const FLABELS = ['딸기','초코','녹차','레몬','망고','복숭아','포도','체리'];
let e1n=6, e1r=2, e1sel=new Set(), e1matched=false;

function e1Init() {
  document.getElementById('e1_r_slider').max = e1n;
  e1Render(); e1UpdateEq();
}

function e1SetN(v) {
  e1n = v; document.getElementById('e1_n_val').textContent=v;
  document.getElementById('e1_instr_n').textContent=v;
  if (e1r > e1n) { e1r = e1n; document.getElementById('e1_r_slider').value=e1r; }
  document.getElementById('e1_r_slider').max = v;
  e1r = +document.getElementById('e1_r_slider').value;
  document.getElementById('e1_r_val').textContent = e1r;
  document.getElementById('e1_instr_r').textContent = e1r;
  e1sel = new Set(); e1matched = false;
  document.getElementById('e1_success').classList.remove('show');
  e1Render(); e1UpdateEq();
}

function e1SetR(v) {
  e1r = v;
  document.getElementById('e1_r_val').textContent = v;
  document.getElementById('e1_instr_r').textContent = v;
  e1sel = new Set(); e1matched = false;
  document.getElementById('e1_success').classList.remove('show');
  e1Render(); e1UpdateEq();
}

function e1Render() {
  const c = document.getElementById('e1_items');
  c.innerHTML = '';
  for (let i=0;i<e1n;i++) {
    const sel = e1sel.has(i);
    const d = document.createElement('div');
    d.className = 'ic ' + (sel?'ic-sel':'ic-normal');
    d.innerHTML = `<span>${FLAVORS[i]}</span><span class="ic-lbl">${FLABELS[i]}</span>`;
    d.onclick = ()=>e1Toggle(i);
    c.appendChild(d);
  }
  // sel/rej visual areas
  const sa = document.getElementById('e1_sel_area');
  const ra = document.getElementById('e1_rej_area');
  if (e1sel.size===0) {
    sa.innerHTML='<span style="font-size:.72rem;color:#374151">선택하세요...</span>';
    ra.innerHTML='<span style="font-size:.72rem;color:#374151">선택하면 제외된 것이 여기 표시됩니다...</span>';
  } else {
    sa.innerHTML=[...e1sel].map(i=>
      `<span style="font-size:2.2rem;background:rgba(79,156,249,.1);border:1.5px solid rgba(79,156,249,.4);border-radius:10px;padding:5px 8px">${FLAVORS[i]}</span>`
    ).join('');
    const rej=[];
    for(let i=0;i<e1n;i++) if(!e1sel.has(i)) rej.push(i);
    ra.innerHTML = rej.map(i=>
      `<span style="font-size:2.2rem;background:rgba(251,146,60,.1);border:1.5px solid rgba(251,146,60,.4);border-radius:10px;padding:5px 8px">${FLAVORS[i]}</span>`
    ).join('');
  }
}

function e1Toggle(i) {
  if (e1sel.has(i)) { e1sel.delete(i); e1matched=false; document.getElementById('e1_success').classList.remove('show'); }
  else if (e1sel.size < e1r) { e1sel.add(i); }
  e1Render(); e1UpdateEq();
  if (e1sel.size===e1r && !e1matched) e1ShowMatch();
}

function e1UpdateEq() {
  const lv=C(e1n,e1r), rv=C(e1n,e1n-e1r);
  const ls=Cstr(e1n,e1r), rs=Cstr(e1n,e1n-e1r);
  document.getElementById('e1_lhs').textContent = ls+' = '+lv;
  document.getElementById('e1_rhs').textContent = rs+' = '+rv;
  document.getElementById('e1_eq_lhs').textContent = ls+' = '+lv;
  document.getElementById('e1_eq_rhs').textContent = rs+' = '+rv;
  const sgn = document.getElementById('e1_eq_sign');
  if (e1sel.size===e1r) { sgn.textContent='='; sgn.style.color='#34d399'; }
  else { sgn.textContent='≟'; sgn.style.color='#4b5563'; }
}

function e1ShowMatch() {
  e1matched = true;
  const lv=C(e1n,e1r), rv=C(e1n,e1n-e1r);
  document.getElementById('e1_body').innerHTML =
    `<strong style="color:#4f9cf9">${Cstr(e1n,e1r)} = ${lv}</strong> (선택한 것들)&nbsp;&nbsp;=&nbsp;&nbsp;<strong style="color:#fb923c">${Cstr(e1n,e1n-e1r)} = ${rv}</strong> (제외된 것들)<br>
    선택 = "버리지 않을 것을 고르는 것" → 항상 같은 경우의 수!`;
  document.getElementById('e1_success').classList.add('show');
  markDone(0);
}

function e1Reset() {
  e1sel=new Set(); e1matched=false;
  document.getElementById('e1_success').classList.remove('show');
  e1Render(); e1UpdateEq();
}

/* ====================================================
   IDENTITY 2 — nCr = (n-1)Cr + (n-1)C(r-1)
   n=5, r=2, special idx=0 (은별)
   All 10 pairs: {0,1}{0,2}{0,3}{0,4}{1,2}{1,3}{1,4}{2,3}{2,4}{3,4}
   ==================================================== */
const PEOPLE2 = ['⭐','🦁','🌸','🐯','🌊'];
const PNAMES2 = ['은별','도윤','세아','준서','하린'];
const PCOLORS2 = ['#fbbf24','#60a5fa','#f472b6','#fb923c','#34d399'];
let e2sel=[], e2in=new Set(), e2out=new Set(), e2done=false;

function e2Init() { e2Render(); }

function e2Render() {
  const c = document.getElementById('e2_items');
  c.innerHTML='';
  PEOPLE2.forEach((em,i)=>{
    const sel=e2sel.includes(i), sp=(i===0&&!sel);
    const d=document.createElement('div');
    d.className='ic '+(sel?'ic-sel':'ic-normal')+(sp?' ic-star-glow':'');
    d.style.borderColor = sel ? PCOLORS2[i] : (sp?'#fbbf24':'rgba(255,255,255,.14)');
    if(sel) d.style.background=PCOLORS2[i]+'25';
    d.innerHTML=`<span>${em}</span><span class="ic-lbl" style="color:${PCOLORS2[i]}">${PNAMES2[i]}</span>`;
    d.onclick=()=>e2Pick(i);
    c.appendChild(d);
  });
}

function e2Pick(i) {
  if (e2sel.includes(i)) { e2sel=e2sel.filter(x=>x!==i); e2Render(); return; }
  if (e2sel.length>=2) return;
  e2sel.push(i);
  e2Render();
  if (e2sel.length===2) e2Classify();
}

function e2Classify() {
  const pair=[...e2sel].sort((a,b)=>a-b);
  const key=pair.join(',');
  const hasSpecial=pair.includes(0);
  const names=pair.map(i=>PNAMES2[i]);
  const log=document.getElementById('e2_log');
  let msg='';
  if (hasSpecial) {
    if (!e2in.has(key)) {
      e2in.add(key);
      msg=`<span style="color:#60a5fa">⭐ 포함</span> [${names.join(', ')}] — 새 발견!`;
    } else { msg=`<span style="color:#4b5563">⭐ 포함 [${names.join(', ')}] — 이미 탐색함</span>`; }
  } else {
    if (!e2out.has(key)) {
      e2out.add(key);
      msg=`<span style="color:#fb923c">❌ 제외</span> [${names.join(', ')}] — 새 발견!`;
    } else { msg=`<span style="color:#4b5563">❌ 제외 [${names.join(', ')}] — 이미 탐색함</span>`; }
  }
  log.innerHTML = msg + '<br>' + log.innerHTML;
  document.getElementById('e2_cnt_in').textContent = e2in.size;
  document.getElementById('e2_cnt_out').textContent = e2out.size;
  const tot=e2in.size+e2out.size;
  document.getElementById('e2_prog').style.width=(tot/10*100)+'%';
  document.getElementById('e2_prog_lbl').textContent=tot+' / 10가지 발견';
  if (e2in.size===4) {
    document.getElementById('e2_f_in').textContent='ₙ₋₁Cᵣ₋₁ = ₄C₁ = 4 ✓';
    document.getElementById('e2_f_in').style.color='#34d399';
  }
  if (e2out.size===6) {
    document.getElementById('e2_f_out').textContent='ₙ₋₁Cᵣ = ₄C₂ = 6 ✓';
    document.getElementById('e2_f_out').style.color='#34d399';
  }
  if (tot===10 && !e2done) { e2done=true; document.getElementById('e2_success').classList.add('show'); markDone(1); }
  setTimeout(()=>{ e2sel=[]; e2Render(); }, 550);
}

function e2ShowAll() {
  e2in=new Set(['0,1','0,2','0,3','0,4']);
  e2out=new Set(['1,2','1,3','1,4','2,3','2,4','3,4']);
  document.getElementById('e2_cnt_in').textContent=4;
  document.getElementById('e2_cnt_out').textContent=6;
  document.getElementById('e2_prog').style.width='100%';
  document.getElementById('e2_prog_lbl').textContent='10 / 10가지 발견';
  document.getElementById('e2_f_in').textContent='ₙ₋₁Cᵣ₋₁ = ₄C₁ = 4 ✓';
  document.getElementById('e2_f_in').style.color='#34d399';
  document.getElementById('e2_f_out').textContent='ₙ₋₁Cᵣ = ₄C₂ = 6 ✓';
  document.getElementById('e2_f_out').style.color='#34d399';
  document.getElementById('e2_log').innerHTML=[
    '<span style="color:#60a5fa">⭐ 포함</span> [은별, 도윤]',
    '<span style="color:#60a5fa">⭐ 포함</span> [은별, 세아]',
    '<span style="color:#60a5fa">⭐ 포함</span> [은별, 준서]',
    '<span style="color:#60a5fa">⭐ 포함</span> [은별, 하린]',
    '<span style="color:#fb923c">❌ 제외</span> [도윤, 세아]',
    '<span style="color:#fb923c">❌ 제외</span> [도윤, 준서]',
    '<span style="color:#fb923c">❌ 제외</span> [도윤, 하린]',
    '<span style="color:#fb923c">❌ 제외</span> [세아, 준서]',
    '<span style="color:#fb923c">❌ 제외</span> [세아, 하린]',
    '<span style="color:#fb923c">❌ 제외</span> [준서, 하린]',
  ].join('<br>');
  if (!e2done) { e2done=true; document.getElementById('e2_success').classList.add('show'); markDone(1); }
}

function e2Reset() {
  e2sel=[]; e2in=new Set(); e2out=new Set(); e2done=false;
  document.getElementById('e2_cnt_in').textContent='0';
  document.getElementById('e2_cnt_out').textContent='0';
  document.getElementById('e2_f_in').textContent='ₙ₋₁Cᵣ₋₁ = ₄C₁ = 4';
  document.getElementById('e2_f_in').style.color='';
  document.getElementById('e2_f_out').textContent='ₙ₋₁Cᵣ = ₄C₂ = 6';
  document.getElementById('e2_f_out').style.color='';
  document.getElementById('e2_prog').style.width='0%';
  document.getElementById('e2_prog_lbl').textContent='0 / 10가지 발견';
  document.getElementById('e2_log').innerHTML='';
  document.getElementById('e2_success').classList.remove('show');
  e2Render();
}

/* ====================================================
   IDENTITY 3 — r·nCr = n·(n-1)C(r-1)
   n=5, r=3 → LHS=3×10=30, RHS=5×6=30
   ==================================================== */
const P5E=['🦁','🌸','🐯','🌊','🔥'];
const P5N=['도윤','세아','준서','하린','지호'];
const P5C=['#60a5fa','#f472b6','#fb923c','#34d399','#a78bfa'];

let e3m1sel=[], e3m1rep=-1, e3m1done=false;
let e3m2rep=-1, e3m2team=[], e3m2done=false;

function e3Init() { e3RenderM1(); e3RenderM2(); }

function e3RenderM1() {
  // pool: pick 3
  const pool=document.getElementById('e3_m1_pool');
  pool.innerHTML='';
  P5E.forEach((em,i)=>{
    const sel=e3m1sel.includes(i);
    const dim=!sel&&e3m1sel.length>=3;
    const d=document.createElement('div');
    d.className='sic '+(sel?'sic-sel':(dim?'sic-dim':'sic-normal'));
    if(sel){d.style.borderColor=P5C[i];d.style.background=P5C[i]+'22';}
    d.innerHTML=`<span>${em}</span><span class="sic-lbl" style="color:${sel?P5C[i]:'#6b7280'}">${P5N[i]}</span>`;
    if(!dim||sel) d.onclick=()=>e3M1PickTeam(i);
    pool.appendChild(d);
  });
  // rep pool: only when team is ready
  const rp=document.getElementById('e3_m1_rep_pool');
  const lbl2=document.getElementById('e3_lbl_s2a');
  if (e3m1sel.length<3) {
    rp.innerHTML='<span style="font-size:.7rem;color:#374151">팀 3명 선발 후 활성화됩니다</span>';
    lbl2.classList.add('step-lbl-dim');
  } else {
    lbl2.classList.remove('step-lbl-dim');
    rp.innerHTML='';
    e3m1sel.forEach(i=>{
      const isRep=(e3m1rep===i);
      const d=document.createElement('div');
      d.className='sic '+(isRep?'sic-gold':'sic-sel');
      d.style.borderColor=isRep?'#fbbf24':P5C[i];
      d.style.background=isRep?'rgba(251,191,36,.18)':P5C[i]+'22';
      d.innerHTML=`<span>${P5E[i]}</span><span class="sic-lbl" style="color:${isRep?'#fbbf24':P5C[i]}">${P5N[i]}${isRep?'👑':''}</span>`;
      d.onclick=()=>e3M1PickRep(i);
      rp.appendChild(d);
    });
  }
}

function e3M1PickTeam(i) {
  if (e3m1done) return;
  if (e3m1sel.includes(i)) { e3m1sel=e3m1sel.filter(x=>x!==i); e3m1rep=-1; }
  else if (e3m1sel.length<3) { e3m1sel.push(i); }
  e3RenderM1();
}

function e3M1PickRep(i) {
  if (e3m1done) return;
  e3m1rep=i; e3RenderM1();
  setTimeout(()=>e3CheckM1(), 100);
}

function e3CheckM1() {
  if (e3m1rep===-1) return;
  e3m1done=true;
  const tnames=e3m1sel.map(i=>P5N[i]+(i===e3m1rep?'👑':'')).join(', ');
  document.getElementById('e3_m1_result').innerHTML=
    `팀 [${tnames}] 완성!<br>r·ₙCᵣ = 3 × ₅C₃ = 3 × 10 = <strong>30</strong>`;
  if (e3m2done) e3ShowMatch();
}

function e3RenderM2() {
  const pool=document.getElementById('e3_m2_pool');
  pool.innerHTML='';
  P5E.forEach((em,i)=>{
    const isRep=(e3m2rep===i);
    const done=e3m2rep!==-1;
    const d=document.createElement('div');
    d.className='sic '+(isRep?'sic-gold':(done?'sic-dim':'sic-normal'));
    if(isRep){d.style.borderColor='#fbbf24';d.style.background='rgba(251,191,36,.18)';}
    d.innerHTML=`<span>${em}</span><span class="sic-lbl" style="color:${isRep?'#fbbf24':'#6b7280'}">${P5N[i]}${isRep?'👑':''}</span>`;
    if(!done) d.onclick=()=>e3M2PickRep(i);
    pool.appendChild(d);
  });
  const tp=document.getElementById('e3_m2_team_pool');
  const lbl2b=document.getElementById('e3_lbl_s2b');
  if (e3m2rep===-1) {
    tp.innerHTML='<span style="font-size:.7rem;color:#374151">대표 선출 후 활성화됩니다</span>';
    lbl2b.classList.add('step-lbl-dim');
  } else {
    lbl2b.classList.remove('step-lbl-dim');
    tp.innerHTML='';
    P5E.forEach((em,i)=>{
      if (i===e3m2rep) return;
      const sel=e3m2team.includes(i);
      const dim=!sel&&e3m2team.length>=2;
      const d=document.createElement('div');
      d.className='sic '+(sel?'sic-sel':(dim?'sic-dim':'sic-normal'));
      if(sel){d.style.borderColor=P5C[i];d.style.background=P5C[i]+'22';}
      d.innerHTML=`<span>${em}</span><span class="sic-lbl" style="color:${sel?P5C[i]:'#6b7280'}">${P5N[i]}</span>`;
      if(!dim||sel) d.onclick=()=>e3M2PickTeam(i);
      tp.appendChild(d);
    });
  }
}

function e3M2PickRep(i) {
  if (e3m2done) return;
  e3m2rep=i; e3m2team=[]; e3RenderM2();
}

function e3M2PickTeam(i) {
  if (e3m2done) return;
  if (e3m2team.includes(i)) { e3m2team=e3m2team.filter(x=>x!==i); }
  else if (e3m2team.length<2) { e3m2team.push(i); }
  e3RenderM2();
  if (e3m2team.length===2) setTimeout(()=>e3CheckM2(), 100);
}

function e3CheckM2() {
  e3m2done=true;
  const allNames=[P5N[e3m2rep]+'👑', ...e3m2team.map(i=>P5N[i])].join(', ');
  document.getElementById('e3_m2_result').innerHTML=
    `팀 [${allNames}] 완성!<br>n·ₙ₋₁Cᵣ₋₁ = 5 × ₄C₂ = 5 × 6 = <strong>30</strong>`;
  if (e3m1done) e3ShowMatch();
}

function e3ShowMatch() {
  document.getElementById('e3_success').classList.add('show');
  markDone(2);
}

function e3Reset() {
  e3m1sel=[]; e3m1rep=-1; e3m1done=false;
  e3m2rep=-1; e3m2team=[]; e3m2done=false;
  document.getElementById('e3_m1_result').textContent='r·ₙCᵣ = 3 × ₅C₃ = 30';
  document.getElementById('e3_m2_result').textContent='n·ₙ₋₁Cᵣ₋₁ = 5 × ₄C₂ = 30';
  document.getElementById('e3_success').classList.remove('show');
  e3RenderM1(); e3RenderM2();
}

/* ====================================================
   IDENTITY 4 — nCr × rCk = nCk × (n-k)C(r-k)
   n=5, r=3, k=2 → LHS=10×3=30, RHS=10×3=30
   ==================================================== */
const P5E4=['🦁','🌸','🐯','🌊','🔥'];
const P5N4=['도윤','세아','준서','하린','지호'];
const P5C4=['#60a5fa','#f472b6','#fb923c','#34d399','#a78bfa'];

let e4m1sel=[], e4m1ateam=[], e4m1done=false;
let e4m2ateam=[], e4m2bteam=[], e4m2done=false;

function e4Init() { e4RenderM1(); e4RenderM2(); }

function e4RenderM1() {
  // pool: pick 3 from 5
  const pool=document.getElementById('e4_m1_pool');
  pool.innerHTML='';
  P5E4.forEach((em,i)=>{
    const sel=e4m1sel.includes(i);
    const dim=!sel&&e4m1sel.length>=3;
    const d=document.createElement('div');
    d.className='sic '+(sel?'sic-sel':(dim?'sic-dim':'sic-normal'));
    if(sel){d.style.borderColor=P5C4[i];d.style.background=P5C4[i]+'22';}
    d.innerHTML=`<span>${em}</span><span class="sic-lbl" style="color:${sel?P5C4[i]:'#6b7280'}">${P5N4[i]}</span>`;
    if(!dim||sel) d.onclick=()=>e4M1PickSel(i);
    pool.appendChild(d);
  });
  // A-team pool: pick 2 from selected 3
  const ap=document.getElementById('e4_m1_ateam_pool');
  const lbl2a=document.getElementById('e4_lbl_s2a');
  if (e4m1sel.length<3) {
    ap.innerHTML='<span style="font-size:.7rem;color:#374151">3명 선발 후 활성화됩니다</span>';
    lbl2a.style.opacity='.38';
  } else {
    lbl2a.style.opacity='1';
    ap.innerHTML='';
    e4m1sel.forEach(i=>{
      const inA=e4m1ateam.includes(i);
      const dim=!inA&&e4m1ateam.length>=2;
      const d=document.createElement('div');
      d.className='sic '+(inA?'sic-sel':(dim?'sic-dim':'sic-normal'));
      if(inA){d.style.borderColor='#f472b6';d.style.background='rgba(244,114,182,.18)';}
      d.innerHTML=`<span>${P5E4[i]}</span><span class="sic-lbl" style="color:${inA?'#f472b6':'#6b7280'}">${P5N4[i]}${inA?' A':''}</span>`;
      if(!dim||inA) d.onclick=()=>e4M1PickA(i);
      ap.appendChild(d);
    });
  }
  // B-team info
  const bi=document.getElementById('e4_m1_bteam_info');
  if (e4m1ateam.length===2) {
    const btm=e4m1sel.filter(i=>!e4m1ateam.includes(i));
    bi.textContent='🟠 B팀: '+btm.map(i=>P5N4[i]).join(', ')+' (자동 배정)';
  } else { bi.textContent=''; }
}

function e4M1PickSel(i) {
  if (e4m1done) return;
  if (e4m1sel.includes(i)) { e4m1sel=e4m1sel.filter(x=>x!==i); e4m1ateam=[]; }
  else if (e4m1sel.length<3) { e4m1sel.push(i); }
  e4RenderM1();
}

function e4M1PickA(i) {
  if (e4m1done) return;
  if (e4m1ateam.includes(i)) { e4m1ateam=e4m1ateam.filter(x=>x!==i); }
  else if (e4m1ateam.length<2) { e4m1ateam.push(i); }
  e4RenderM1();
  if (e4m1ateam.length===2) setTimeout(()=>e4CheckM1(), 100);
}

function e4CheckM1() {
  e4m1done=true;
  const btm=e4m1sel.filter(i=>!e4m1ateam.includes(i));
  const anames=e4m1ateam.map(i=>P5N4[i]).join(', ');
  const bnames=btm.map(i=>P5N4[i]).join(', ');
  document.getElementById('e4_m1_result').innerHTML=
    `A팀[${anames}] B팀[${bnames}] 완성!<br>₅C₃ × ₃C₂ = 10 × 3 = <strong>30</strong>`;
  if (e4m2done) e4ShowMatch();
}

function e4RenderM2() {
  const pool=document.getElementById('e4_m2_pool');
  pool.innerHTML='';
  P5E4.forEach((em,i)=>{
    const inA=e4m2ateam.includes(i);
    const dim=!inA&&e4m2ateam.length>=2;
    const d=document.createElement('div');
    d.className='sic '+(inA?'sic-sel':(dim?'sic-dim':'sic-normal'));
    if(inA){d.style.borderColor='#f472b6';d.style.background='rgba(244,114,182,.18)';}
    d.innerHTML=`<span>${em}</span><span class="sic-lbl" style="color:${inA?'#f472b6':'#6b7280'}">${P5N4[i]}${inA?' A':''}</span>`;
    if(!dim||inA) d.onclick=()=>e4M2PickA(i);
    pool.appendChild(d);
  });
  const bp=document.getElementById('e4_m2_bteam_pool');
  const lbl2b=document.getElementById('e4_lbl_s2b');
  if (e4m2ateam.length<2) {
    bp.innerHTML='<span style="font-size:.7rem;color:#374151">A팀 2명 선택 후 활성화됩니다</span>';
    lbl2b.classList.add('step-lbl-dim');
  } else {
    lbl2b.classList.remove('step-lbl-dim');
    bp.innerHTML='';
    P5E4.forEach((em,i)=>{
      if (e4m2ateam.includes(i)) return;
      const inB=e4m2bteam.includes(i);
      const dim=!inB&&e4m2bteam.length>=1;
      const d=document.createElement('div');
      d.className='sic '+(inB?'sic-orange':(dim?'sic-dim':'sic-normal'));
      if(inB){d.style.borderColor='#fb923c';d.style.background='rgba(251,146,60,.18)';}
      d.innerHTML=`<span>${em}</span><span class="sic-lbl" style="color:${inB?'#fb923c':'#6b7280'}">${P5N4[i]}${inB?' B':''}</span>`;
      if(!dim||inB) d.onclick=()=>e4M2PickB(i);
      bp.appendChild(d);
    });
  }
}

function e4M2PickA(i) {
  if (e4m2done) return;
  if (e4m2ateam.includes(i)) { e4m2ateam=e4m2ateam.filter(x=>x!==i); e4m2bteam=[]; }
  else if (e4m2ateam.length<2) { e4m2ateam.push(i); }
  e4RenderM2();
}

function e4M2PickB(i) {
  if (e4m2done) return;
  if (e4m2bteam.includes(i)) { e4m2bteam=e4m2bteam.filter(x=>x!==i); }
  else if (e4m2bteam.length<1) { e4m2bteam.push(i); }
  e4RenderM2();
  if (e4m2bteam.length===1) setTimeout(()=>e4CheckM2(), 100);
}

function e4CheckM2() {
  e4m2done=true;
  const anames=e4m2ateam.map(i=>P5N4[i]).join(', ');
  const bnames=e4m2bteam.map(i=>P5N4[i]).join(', ');
  document.getElementById('e4_m2_result').innerHTML=
    `A팀[${anames}] B팀[${bnames}] 완성!<br>₅C₂ × ₃C₁ = 10 × 3 = <strong>30</strong>`;
  if (e4m1done) e4ShowMatch();
}

function e4ShowMatch() {
  document.getElementById('e4_success').classList.add('show');
  markDone(3);
}

function e4Reset() {
  e4m1sel=[]; e4m1ateam=[]; e4m1done=false;
  e4m2ateam=[]; e4m2bteam=[]; e4m2done=false;
  document.getElementById('e4_m1_result').textContent='₅C₃ × ₃C₂ = 10 × 3 = 30';
  document.getElementById('e4_m2_result').textContent='₅C₂ × ₃C₁ = 10 × 3 = 30';
  document.getElementById('e4_m1_bteam_info').textContent='';
  document.getElementById('e4_success').classList.remove('show');
  e4RenderM1(); e4RenderM2();
}

/* ====================================================
   INIT ALL
   ==================================================== */
e1Init(); e2Init(); e3Init(); e4Init();
</script>
</body>
</html>
"""


def render():
    st.markdown("### 🔢 조합 등식 탐구")
    st.markdown(
        "수업에서 배운 **4가지 조합 등식**을 실생활 상황에서 직접 체험하며 이해해 보세요!"
    )
    components.html(_HTML, height=2200, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
