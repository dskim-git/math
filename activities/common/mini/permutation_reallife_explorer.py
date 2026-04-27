# activities/common/mini/permutation_reallife_explorer.py
"""
순열 실생활 탐구 — 6가지 실생활 사례로 순열 개념을 인터랙티브하게 탐구하는 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "순열실생활탐구"

META = {
    "title":       "🎯 순열 실생활 탐구",
    "description": "줄 세우기·임원 선출·자연수 만들기·시상식·승부차기·비밀번호 6가지 사례를 직접 조작하며 순열 P(n,r)을 탐구합니다.",
    "order":       320,
    "hidden":      False,
}

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "순열개념",
        "label":  "① 순열이란 무엇인가요? 오늘 탐구한 사례를 바탕으로 순열의 특징을 나만의 말로 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "순서중요성",
        "label":  "② 순열에서 '순서'가 왜 중요한가요? 순서가 달라지면 어떻게 되는지 구체적인 사례를 들어 설명해보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "공식이해",
        "label":  "③ P(n,r) = n×(n-1)×…×(n-r+1) 에서 왜 하나씩 줄어들까요? 임원 선출이나 줄 세우기 사례로 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "신규사례",
        "label":  "④ 활동에서 다루지 않은 순열의 실생활 사례를 1가지 이상 직접 만들고 P(n,r)로 표현해보세요.",
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
  color:#dde8ff;padding:10px 12px 16px;
}
/* HEADER */
.hdr{text-align:center;padding:8px 0 12px}
.hdr-title{font-size:1.25rem;font-weight:700;color:#ffd700;
  text-shadow:0 0 18px rgba(255,215,0,.4);margin-bottom:6px}
.formula-banner{display:inline-block;background:rgba(255,215,0,.06);
  border:1px solid rgba(255,215,0,.25);border-radius:10px;padding:5px 14px;
  font-size:.82rem;color:#ffd700;font-family:'Courier New',monospace;letter-spacing:.5px}
/* TABS */
.tabs{display:flex;flex-wrap:wrap;gap:4px;margin:0 0 10px;
  background:rgba(255,255,255,.04);border-radius:12px;padding:5px}
.tab{flex:1;min-width:70px;padding:7px 4px;border:none;border-radius:8px;
  font-family:inherit;font-size:.73rem;font-weight:600;cursor:pointer;
  background:transparent;color:#7788aa;transition:all .2s;line-height:1.35}
.tab:hover{color:#dde8ff;background:rgba(255,255,255,.06)}
.tab.active{background:rgba(255,215,0,.12);color:#ffd700;border:1px solid rgba(255,215,0,.3)}
/* PANELS */
.panel{display:none}.panel.active{display:block;animation:fadein .25s ease}
@keyframes fadein{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
/* SCENARIO */
.sc-title{font-size:1rem;font-weight:700;margin-bottom:5px;display:flex;align-items:center;gap:6px}
.sc-sub{font-size:.78rem;color:#7788aa;margin-bottom:10px;line-height:1.6}
/* VISUAL AREA */
.vis{background:rgba(0,0,0,.3);border-radius:12px;padding:12px 10px;margin-bottom:9px;min-height:80px}
/* FORMULA ROW */
.frm{display:flex;align-items:center;gap:7px;background:rgba(255,215,0,.05);
  border:1px solid rgba(255,215,0,.2);border-radius:9px;padding:7px 11px;
  margin-bottom:8px;flex-wrap:wrap}
.frm-lbl{font-size:.75rem;color:#7788aa}
.frm-val{font-family:'Courier New',monospace;font-size:.88rem;color:#ffd700;font-weight:700}
/* PEOPLE */
.person{display:inline-flex;flex-direction:column;align-items:center;gap:3px;
  cursor:pointer;transition:transform .15s;user-select:none}
.person:hover{transform:translateY(-4px)}
.person.disabled{opacity:.3;pointer-events:none}
.p-circle{width:82px;height:82px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:2rem;font-weight:700;
  border:2px solid rgba(255,255,255,.25);transition:all .3s}
.p-name{font-size:.75rem;color:#9ca3af;margin-top:2px}
/* LINE ROW */
.lrow{display:flex;align-items:flex-end;gap:10px;justify-content:center;flex-wrap:wrap;padding:6px 0}
/* SLOTS */
.slot{border:2px dashed rgba(255,255,255,.2);border-radius:12px;padding:10px 12px;
  min-width:88px;text-align:center;transition:all .3s}
.slot.filled{border-style:solid;border-color:rgba(255,215,0,.45);background:rgba(255,215,0,.05)}
.slot-lbl{font-size:.7rem;color:#7788aa;margin-bottom:3px}
.slot-val{font-size:.92rem;font-weight:700;min-height:22px}
/* DIGIT CARDS */
.dcard{display:inline-flex;align-items:center;justify-content:center;
  width:72px;height:90px;border-radius:12px;font-size:2rem;font-weight:700;
  cursor:pointer;transition:all .2s;border:2px solid;user-select:none}
.dcard:hover:not(.used){transform:translateY(-5px);box-shadow:0 6px 16px rgba(0,0,0,.5)}
.dcard.used{opacity:.22;cursor:default;transform:none!important}
/* NUM BOXES */
.ndisp{display:flex;gap:8px;justify-content:center;align-items:center}
.nbox{width:88px;height:108px;border-radius:12px;background:rgba(0,0,0,.4);
  border:2px solid rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;
  font-size:3rem;font-weight:700;color:#6b7280;transition:all .35s}
.nbox.filled{border-color:rgba(16,185,129,.5);background:rgba(16,185,129,.08);color:#34d399}
/* PODIUM */
.podium-wrap{display:flex;align-items:flex-end;justify-content:center;gap:10px;padding:8px 0}
.podium-col{display:flex;flex-direction:column;align-items:center;gap:3px}
.pod-person{width:82px;height:82px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:2rem;border:2px solid rgba(255,255,255,.2);
  opacity:.45;transition:all .35s}
.pod-person.placed{opacity:1;animation:pop .3s ease}
.pod-block{border-radius:8px 8px 0 0;display:flex;align-items:center;justify-content:center;
  font-size:1.8rem;width:90px}
/* FIELD */
.field{background:linear-gradient(160deg,#064e3b,#065f46,#047857);
  border-radius:12px;padding:14px 10px;display:flex;flex-wrap:wrap;gap:10px;
  justify-content:center;align-items:center;border:2px solid rgba(255,255,255,.08)}
/* JERSEY */
.jersey{display:inline-flex;flex-direction:column;align-items:center;gap:3px;
  cursor:pointer;transition:opacity .2s,transform .15s}
.jersey:hover:not(.used){transform:translateY(-4px)}
.jersey.used{opacity:.28;pointer-events:none}
.jshirt{width:62px;height:72px;border-radius:8px 8px 6px 6px;display:flex;align-items:center;
  justify-content:center;font-size:1.4rem;font-weight:700;color:#fff;
  border:1.5px solid rgba(255,255,255,.3);position:relative}
.jnum-label{font-size:.68rem;color:rgba(255,255,255,.6)}
/* KICK SLOTS */
.kslots{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:10px}
.kslot{display:flex;flex-direction:column;align-items:center;gap:4px}
.kslot-num{font-size:.68rem;color:#7788aa}
.kslot-box{width:70px;height:84px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:1rem;font-weight:700;transition:all .3s;text-align:center}
/* LOCK */
.lockdisp{display:flex;gap:8px;justify-content:center;margin-bottom:12px}
.ldig{width:88px;height:108px;background:rgba(0,0,0,.5);border:2px solid rgba(139,92,246,.3);
  border-radius:12px;display:flex;align-items:center;justify-content:center;
  font-size:3rem;font-weight:700;color:#6b7280;transition:all .3s}
.ldig.filled{border-color:#8b5cf6;background:rgba(139,92,246,.13);color:#a78bfa;animation:pop .3s ease}
/* NUMPAD */
.numpad{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;max-width:300px;margin:0 auto}
.npbtn{padding:11px 4px;border:1.5px solid rgba(139,92,246,.35);border-radius:8px;
  background:rgba(139,92,246,.08);color:#a78bfa;font-size:1.1rem;font-weight:700;
  cursor:pointer;font-family:inherit;transition:all .2s}
.npbtn:hover:not(:disabled){background:rgba(139,92,246,.22);transform:translateY(-1px)}
.npbtn:disabled{opacity:.2;cursor:default;transform:none}
/* BUTTONS */
.btn{padding:6px 14px;border-radius:8px;border:1.5px solid rgba(255,255,255,.18);
  background:rgba(255,255,255,.06);color:#dde8ff;font-family:inherit;
  font-size:.8rem;cursor:pointer;transition:all .2s}
.btn:hover{background:rgba(255,255,255,.11);transform:translateY(-1px)}
.btn.gold{background:rgba(255,215,0,.09);border-color:rgba(255,215,0,.35);color:#ffd700}
.btn.gold:hover{background:rgba(255,215,0,.18)}
/* NOTICE */
.notice{background:rgba(59,130,246,.07);border:1px solid rgba(59,130,246,.22);
  border-radius:8px;padding:7px 11px;font-size:.76rem;color:#93c5fd;
  margin-top:6px;line-height:1.65}
/* BADGE */
.badge{display:inline-block;padding:4px 12px;border-radius:99px;
  background:linear-gradient(135deg,#059669,#047857);color:#ecfdf5;
  font-size:.78rem;font-weight:700;animation:pop .3s ease}
/* COUNT */
.cbox{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
  border-radius:9px;padding:7px 10px;text-align:center}
.cnum{font-size:1.9rem;font-weight:700;
  background:linear-gradient(135deg,#ffd700,#fb923c);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.clbl{font-size:.72rem;color:#7788aa;margin-top:1px}
/* SUMMARY TABLE */
.sumtbl{width:100%;border-collapse:collapse;font-size:.76rem}
.sumtbl th{text-align:left;padding:5px 6px;color:#7788aa;
  border-bottom:1px solid rgba(255,255,255,.1)}
.sumtbl td{padding:5px 6px;border-bottom:1px solid rgba(255,255,255,.05)}
/* SLIDER */
input[type=range]{accent-color:#ffd700}
@keyframes pop{0%{transform:scale(.7)}60%{transform:scale(1.1)}100%{transform:scale(1)}}
@keyframes flash{0%,100%{opacity:1}50%{opacity:.4}}
.flash{animation:flash .4s ease}
</style>
</head>
<body>

<!-- HEADER -->
<div class="hdr">
  <div class="hdr-title">🎯 순열 실생활 탐구</div>
  <div class="formula-banner">P(n, r) = n × (n−1) × ⋯ × (n−r+1) = n! / (n−r)!</div>
</div>

<!-- TABS -->
<div class="tabs" id="tabBar">
  <button class="tab active" onclick="switchTab(0)">👥<br>줄 세우기</button>
  <button class="tab" onclick="switchTab(1)">🏛️<br>임원 선출</button>
  <button class="tab" onclick="switchTab(2)">🔢<br>자연수</button>
  <button class="tab" onclick="switchTab(3)">🏆<br>시상식</button>
  <button class="tab" onclick="switchTab(4)">⚽<br>승부차기</button>
  <button class="tab" onclick="switchTab(5)">🔐<br>비밀번호</button>
</div>

<!-- ══ PANEL 0: 줄 세우기 ══ -->
<div id="p0" class="panel active">
  <div class="sc-title">👥 줄 세우기</div>
  <div class="sc-sub">
    n명을 한 줄로 세우는 경우의 수를 탐구합니다.<br>
    아래 인물을 클릭해 순서대로 자리에 배치해보세요!
  </div>
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap">
    <span style="font-size:.8rem;color:#7788aa">인원 수 n =</span>
    <input type="range" id="s1n" min="3" max="6" value="4"
      oninput="document.getElementById('s1nv').textContent=this.value;s1Init()" style="width:110px">
    <span id="s1nv" style="background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.3);
      border-radius:6px;padding:2px 10px;font-size:.95rem;font-weight:700;color:#ffd700">4</span>
    <span style="font-size:.78rem;color:#7788aa">명</span>
  </div>
  <div class="vis">
    <div style="font-size:.73rem;color:#7788aa;text-align:center;margin-bottom:6px">후보 클릭 → 자리 배정</div>
    <div id="s1pool" class="lrow" style="margin-bottom:14px"></div>
    <div style="font-size:.72rem;color:#ffd700;text-align:center;margin-bottom:6px">📍 자리 순서</div>
    <div id="s1slots" class="lrow"></div>
    <div id="s1msg" style="text-align:center;margin-top:8px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">한 줄 배치 방법:</span>
    <span class="frm-val" id="s1frm">P(4,4) = 4! = 4×3×2×1 = 24가지</span>
  </div>
  <div style="display:flex;gap:7px;flex-wrap:wrap;margin-bottom:8px">
    <button class="btn gold" onclick="s1Back()">⌫ 하나 되돌리기</button>
    <button class="btn" onclick="s1Init()">↩ 초기화</button>
  </div>
  <div class="notice">
    💡 <strong>n명 줄 세우기</strong>: 첫 자리 n가지, 두 번째 (n−1)가지, … 마지막 1가지<br>
    → <strong>P(n,n) = n!</strong> — 사람이 1명만 늘어도 경우의 수가 엄청나게 커집니다!
  </div>
</div>

<!-- ══ PANEL 1: 임원 선출 ══ -->
<div id="p1" class="panel">
  <div class="sc-title">🏛️ 임원 선출 (회장·부회장·총무)</div>
  <div class="sc-sub">
    5명의 후보 중 회장·부회장·총무를 뽑는 경우의 수를 탐구합니다.<br>
    후보를 클릭하면 차례대로 역할이 배정됩니다. 누가 어떤 역할을 맡느냐도 중요해요!
  </div>
  <div class="vis">
    <div style="font-size:.73rem;color:#7788aa;text-align:center;margin-bottom:6px">후보 클릭 → 역할 배정</div>
    <div id="s2cands" class="lrow" style="margin-bottom:12px"></div>
    <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
      <div class="slot" id="s2slot0"><div class="slot-lbl">👑 회장</div><div class="slot-val" id="s2f0">—</div></div>
      <div class="slot" id="s2slot1"><div class="slot-lbl">🥈 부회장</div><div class="slot-val" id="s2f1">—</div></div>
      <div class="slot" id="s2slot2"><div class="slot-lbl">📋 총무</div><div class="slot-val" id="s2f2">—</div></div>
    </div>
    <div id="s2msg" style="text-align:center;margin-top:9px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">배치 방법:</span>
    <span class="frm-val">P(5,3) = 5×4×3 = 60가지</span>
  </div>
  <div style="display:flex;gap:7px;margin-bottom:8px">
    <button class="btn" onclick="s2Reset()">↩ 다시하기</button>
  </div>
  <div class="notice">
    💡 회장 선택 <strong>5가지</strong> × 부회장 <strong>4가지</strong> × 총무 <strong>3가지</strong> = <strong>P(5,3) = 60가지</strong><br>
    같은 사람이 뽑혀도 역할이 다르면 다른 경우입니다. 순서(역할)가 중요해요!
  </div>
</div>

<!-- ══ PANEL 2: 자연수 만들기 ══ -->
<div id="p2" class="panel">
  <div class="sc-title">🔢 자연수 만들기</div>
  <div class="sc-sub">
    1, 2, 3, 4, 5 다섯 장의 카드로 세 자리 자연수를 만드는 경우의 수를 탐구합니다.<br>
    (같은 카드는 한 번만 사용할 수 있어요!)
  </div>
  <div class="vis">
    <div style="font-size:.73rem;color:#7788aa;text-align:center;margin-bottom:8px">카드를 클릭해 세 자리 수를 만들어보세요</div>
    <div id="s3cards" style="display:flex;gap:7px;justify-content:center;flex-wrap:wrap;margin-bottom:12px"></div>
    <div class="ndisp" id="s3disp"></div>
    <div id="s3msg" style="text-align:center;margin-top:9px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">만들 수 있는 세 자리 수:</span>
    <span class="frm-val">P(5,3) = 5×4×3 = 60가지</span>
  </div>
  <div style="display:flex;gap:7px;margin-bottom:8px">
    <button class="btn" onclick="s3Reset()">↩ 다시하기</button>
    <button class="btn gold" onclick="s3Back()">⌫ 하나 지우기</button>
  </div>
  <div class="notice">
    💡 백의 자리 <strong>5가지</strong> × 십의 자리 <strong>4가지</strong> × 일의 자리 <strong>3가지</strong> = <strong>P(5,3) = 60가지</strong><br>
    자리마다 선택지가 하나씩 줄어드는 이유는? 이미 쓴 카드는 재사용할 수 없기 때문!
  </div>
</div>

<!-- ══ PANEL 3: 시상식 ══ -->
<div id="p3" class="panel">
  <div class="sc-title">🏆 시상식 (1등·2등·3등)</div>
  <div class="sc-sub">
    6명의 선수 중 1·2·3등 수상자를 정하는 경우의 수를 탐구합니다.<br>
    선수를 클릭하면 순서대로 시상대에 오릅니다.
  </div>
  <div class="vis">
    <div id="s4athletes" class="lrow" style="margin-bottom:10px"></div>
    <div class="podium-wrap" id="s4podium"></div>
    <div id="s4msg" style="text-align:center;margin-top:6px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">수상자 선정 방법:</span>
    <span class="frm-val">P(6,3) = 6×5×4 = 120가지</span>
  </div>
  <div style="display:flex;gap:7px;margin-bottom:8px">
    <button class="btn" onclick="s4Reset()">↩ 다시하기</button>
  </div>
  <div class="notice">
    💡 1등 선택 <strong>6가지</strong> × 2등 선택 <strong>5가지</strong> × 3등 선택 <strong>4가지</strong> = <strong>P(6,3) = 120가지</strong><br>
    1등과 2등이 바뀌면 완전히 다른 결과! 등수(순서)가 다르면 다른 경우입니다.
  </div>
</div>

<!-- ══ PANEL 4: 승부차기 ══ -->
<div id="p4" class="panel">
  <div class="sc-title">⚽ 승부차기 선수 순서 정하기</div>
  <div class="sc-sub">
    축구팀 11명 중 승부차기를 찰 5명의 순서를 정하는 경우의 수를 탐구합니다.<br>
    선수 유니폼을 클릭하면 킥 순서가 배정됩니다!
  </div>
  <div class="vis">
    <div class="field" id="s5players"></div>
    <div style="font-size:.72rem;color:#6ee7b7;text-align:center;margin:7px 0 4px">⚽ 킥 순서 배정</div>
    <div class="kslots" id="s5kicks"></div>
    <div id="s5msg" style="text-align:center;margin-top:7px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">킥 순서 배정 방법:</span>
    <span class="frm-val">P(11,5) = 11×10×9×8×7 = 55,440가지</span>
  </div>
  <div style="display:flex;gap:7px;margin-bottom:8px">
    <button class="btn" onclick="s5Reset()">↩ 다시하기</button>
  </div>
  <div class="notice">
    💡 1번 키커 <strong>11</strong> × 2번 <strong>10</strong> × 3번 <strong>9</strong> × 4번 <strong>8</strong> × 5번 <strong>7</strong> = <strong>P(11,5) = 55,440가지</strong><br>
    킥 순서 전략이 이렇게나 다양합니다! 순서가 달라지면 심리전도 달라집니다.
  </div>
</div>

<!-- ══ PANEL 5: 비밀번호 ══ -->
<div id="p5" class="panel">
  <div class="sc-title">🔐 비밀번호 만들기</div>
  <div class="sc-sub">
    0~9 중 서로 다른 숫자 4개를 골라 만드는 비밀번호의 수를 탐구합니다.<br>
    (같은 숫자는 한 번만 사용!)
  </div>
  <div class="vis">
    <div id="s6lockicon" style="text-align:center;font-size:2.2rem;margin-bottom:7px">🔒</div>
    <div class="lockdisp" id="s6disp"></div>
    <div class="numpad" id="s6numpad"></div>
    <div id="s6msg" style="text-align:center;margin-top:9px;min-height:26px"></div>
  </div>
  <div class="frm">
    <span class="frm-lbl">만들 수 있는 비밀번호:</span>
    <span class="frm-val">P(10,4) = 10×9×8×7 = 5,040가지</span>
  </div>
  <div style="display:flex;gap:7px;margin-bottom:8px">
    <button class="btn" onclick="s6Reset()">↩ 다시하기</button>
    <button class="btn gold" onclick="s6Back()">⌫ 하나 지우기</button>
  </div>
  <div class="notice">
    💡 첫째 자리 <strong>10</strong> × 둘째 <strong>9</strong> × 셋째 <strong>8</strong> × 넷째 <strong>7</strong> = <strong>P(10,4) = 5,040가지</strong><br>
    숫자 4자리만으로도 5,040가지! 비밀번호가 왜 안전한지 이해되나요?
  </div>
</div>

<!-- ══ SUMMARY TABLE ══ -->
<div style="margin-top:14px;background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:11px">
  <div style="font-size:.88rem;font-weight:700;color:#ffd700;margin-bottom:8px">
    📊 탐구한 순열 사례 한눈에 보기
  </div>
  <table class="sumtbl">
    <thead>
      <tr>
        <th>사례</th><th style="text-align:center">P(n,r)</th>
        <th style="text-align:center">계산</th><th style="text-align:right">결과</th>
      </tr>
    </thead>
    <tbody style="color:#b8c8de">
      <tr><td>👥 4명 줄 세우기</td>
        <td style="text-align:center;font-family:'Courier New';color:#ffd700">P(4,4)</td>
        <td style="text-align:center">4×3×2×1</td>
        <td style="text-align:right;font-weight:700;color:#34d399">24가지</td></tr>
      <tr><td>🏛️ 5명 중 임원 3명 선출</td>
        <td style="text-align:center;font-family:'Courier New';color:#ffd700">P(5,3)</td>
        <td style="text-align:center">5×4×3</td>
        <td style="text-align:right;font-weight:700;color:#34d399">60가지</td></tr>
      <tr><td>🔢 5장 카드로 세 자리 수</td>
        <td style="text-align:center;font-family:'Courier New';color:#ffd700">P(5,3)</td>
        <td style="text-align:center">5×4×3</td>
        <td style="text-align:right;font-weight:700;color:#34d399">60가지</td></tr>
      <tr><td>🏆 6명 중 1·2·3등 시상</td>
        <td style="text-align:center;font-family:'Courier New';color:#ffd700">P(6,3)</td>
        <td style="text-align:center">6×5×4</td>
        <td style="text-align:right;font-weight:700;color:#34d399">120가지</td></tr>
      <tr><td>⚽ 11명 중 킥 순서 5명</td>
        <td style="text-align:center;font-family:'Courier New';color:#ffd700">P(11,5)</td>
        <td style="text-align:center">11×10×9×8×7</td>
        <td style="text-align:right;font-weight:700;color:#34d399">55,440가지</td></tr>
      <tr><td>🔐 0~9 중 4자리 비밀번호</td>
        <td style="text-align:center;font-family:'Courier New';color:#ffd700">P(10,4)</td>
        <td style="text-align:center">10×9×8×7</td>
        <td style="text-align:right;font-weight:700;color:#34d399">5,040가지</td></tr>
    </tbody>
  </table>
</div>

<script>
// ─── TAB SWITCHING ───────────────────────────────────────
function switchTab(i) {
  document.querySelectorAll('.tab').forEach((t,j) => t.classList.toggle('active', i===j));
  document.querySelectorAll('.panel').forEach((p,j) => p.classList.toggle('active', i===j));
}

// ─── UTILS ───────────────────────────────────────────────
function factorial(n) { let r=1; for(let i=2;i<=n;i++) r*=i; return r; }
function fyShuffle(a) {
  for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
  return a;
}
function pnr(n,r) { let v=1; for(let i=n;i>n-r;i--) v*=i; return v; }

const EMOJIS = ['👦','👧','🧑','👱','🧒','👩'];
const COLORS6 = ['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#06b6d4'];
const NAMES6  = ['민준','서연','지우','예린','준혁','수아'];

// ─── S1: 줄 세우기 ────────────────────────────────────────
let s1slots=[], s1used=new Set(), s1n=4;

function s1Init() {
  s1n = parseInt(document.getElementById('s1n').value);
  s1slots = Array(s1n).fill(null);
  s1used = new Set();
  const f = factorial(s1n);
  const parts = Array.from({length:s1n},(_,i)=>s1n-i);
  document.getElementById('s1frm').textContent =
    'P('+s1n+','+s1n+') = '+s1n+'! = '+parts.join('×')+' = '+f.toLocaleString()+'가지';
  document.getElementById('s1msg').innerHTML = '';
  s1Render();
}

function s1Render() {
  // 후보 풀
  document.getElementById('s1pool').innerHTML =
    Array.from({length:s1n},(_,i)=>`
      <div class="person ${s1used.has(i)?'disabled':''}" onclick="s1Pick(${i})">
        <div class="p-circle" style="background:${COLORS6[i]}">${EMOJIS[i]}</div>
        <div class="p-name">${NAMES6[i]}</div>
      </div>`).join('');
  // 자리 슬롯
  document.getElementById('s1slots').innerHTML =
    s1slots.map((v,i)=>`
      <div style="display:flex;flex-direction:column;align-items:center;gap:4px">
        <div style="font-size:.68rem;color:#ffd700;font-weight:600">${i+1}번째</div>
        <div class="slot ${v!==null?'filled':''}" style="padding:10px;min-width:90px;min-height:100px;
          display:flex;align-items:center;justify-content:center">
          ${v!==null
            ? `<div style="display:flex;flex-direction:column;align-items:center;gap:3px">
                 <div style="font-size:2.2rem">${EMOJIS[v]}</div>
                 <div style="font-size:.72rem;color:#d1d5db">${NAMES6[v]}</div>
               </div>`
            : '<div style="font-size:2rem;opacity:.15">?</div>'}
        </div>
      </div>`).join('');
  // 완성 메시지
  const filled = s1slots.filter(v=>v!==null).length;
  if(filled===s1n){
    const f = factorial(s1n);
    document.getElementById('s1msg').innerHTML =
      `<span class="badge">✅ 완성! P(${s1n},${s1n}) = ${f.toLocaleString()}가지 중 하나예요</span>`;
  } else if(filled>0){
    document.getElementById('s1msg').innerHTML =
      `<span style="font-size:.76rem;color:#7788aa">${filled}/${s1n} 배정됨 — 계속 클릭해보세요!</span>`;
  }
}

function s1Pick(i) {
  if(s1used.has(i)) return;
  const next=s1slots.findIndex(v=>v===null); if(next===-1) return;
  s1slots[next]=i; s1used.add(i); s1Render();
}

function s1Back() {
  const last=s1slots.map((v,i)=>v!==null?i:-1).filter(i=>i>=0).pop();
  if(last===undefined) return;
  s1used.delete(s1slots[last]); s1slots[last]=null;
  document.getElementById('s1msg').innerHTML=''; s1Render();
}

s1Init();

// ─── S2: 임원 선출 ────────────────────────────────────────
const S2C = [
  {name:'김민준',emoji:'👦',c:'#ef4444'},{name:'이서연',emoji:'👧',c:'#3b82f6'},
  {name:'박지우',emoji:'🧑',c:'#10b981'},{name:'최예린',emoji:'👱',c:'#f59e0b'},
  {name:'정준혁',emoji:'🧒',c:'#8b5cf6'},
];
let s2assigned=[null,null,null], s2used=new Set();

function s2Render() {
  document.getElementById('s2cands').innerHTML = S2C.map((c,i)=>`
    <div class="person ${s2used.has(i)?'disabled':''}" onclick="s2Pick(${i})">
      <div class="p-circle" style="background:${c.c}">${c.emoji}</div>
      <div class="p-name">${c.name}</div>
    </div>`).join('');
  const labels=['s2f0','s2f1','s2f2'], slots=['s2slot0','s2slot1','s2slot2'];
  s2assigned.forEach((v,i)=>{
    const el=document.getElementById(labels[i]);
    const sl=document.getElementById(slots[i]);
    if(v!==null){el.innerHTML=`<span style="color:${S2C[v].c}">${S2C[v].emoji} ${S2C[v].name}</span>`;sl.classList.add('filled');}
    else{el.textContent='—';sl.classList.remove('filled');}
  });
}

function s2Pick(i) {
  if(s2used.has(i)) return;
  const next=s2assigned.findIndex(v=>v===null); if(next===-1) return;
  s2assigned[next]=i; s2used.add(i); s2Render();
  const filled=s2assigned.filter(v=>v!==null).length;
  if(filled===3){
    const [r0,r1,r2]=s2assigned.map(x=>S2C[x].emoji+' '+S2C[x].name);
    document.getElementById('s2msg').innerHTML=
      `<span class="badge">✅ ${r0}(회장) · ${r1}(부회장) · ${r2}(총무) — 완성!</span>`;
  } else {
    const roleNames=['회장','부회장','총무'];
    document.getElementById('s2msg').innerHTML=
      `<span style="font-size:.76rem;color:#7788aa">${S2C[i].emoji} ${S2C[i].name}이(가) ${roleNames[next]}으로 배정됨 (${filled}/3)</span>`;
  }
}

function s2Reset(){s2assigned=[null,null,null];s2used=new Set();document.getElementById('s2msg').innerHTML='';s2Render();}
s2Render();

// ─── S3: 자연수 만들기 ───────────────────────────────────
const S3COLORS=[['#ef4444','239,68,68'],['#3b82f6','59,130,246'],
  ['#10b981','16,185,129'],['#f59e0b','245,158,11'],['#8b5cf6','139,92,246']];
let s3slots=[null,null,null],s3used=new Set();

function s3RenderCards(){
  document.getElementById('s3cards').innerHTML=[1,2,3,4,5].map((d,i)=>`
    <div class="dcard ${s3used.has(d)?'used':''}"
      style="background:rgba(${S3COLORS[i][1]},.14);border-color:${S3COLORS[i][0]};color:${S3COLORS[i][0]}"
      onclick="s3Pick(${d})">${d}</div>`).join('');
}

function s3RenderDisp(){
  const labels=['백의 자리','십의 자리','일의 자리'];
  document.getElementById('s3disp').innerHTML=
    s3slots.map((v,i)=>`
      <div style="display:flex;flex-direction:column;align-items:center;gap:3px">
        <div class="nbox ${v!==null?'filled':''}">${v!==null?v:'<span style="opacity:.2">?</span>'}</div>
        <div style="font-size:.62rem;color:#7788aa">${labels[i]}</div>
      </div>`).join('')+
    `<div style="font-size:1.1rem;color:#7788aa;align-self:center;padding-bottom:14px"> = </div>
     <div style="font-size:2rem;font-weight:700;color:${s3slots.every(v=>v!==null)?'#34d399':'#374151'};
       align-self:center;padding-bottom:14px;min-width:50px">
       ${s3slots.every(v=>v!==null)?s3slots.join(''):'???'}
     </div>`;
}

function s3Pick(d){
  if(s3used.has(d)) return;
  const next=s3slots.findIndex(v=>v===null); if(next===-1) return;
  s3slots[next]=d; s3used.add(d);
  s3RenderCards(); s3RenderDisp();
  if(s3slots.every(v=>v!==null)){
    document.getElementById('s3msg').innerHTML=
      `<span class="badge">✅ ${s3slots.join('')} 완성! P(5,3)=60가지 중 하나예요</span>`;}
}

function s3Back(){
  const last=s3slots.map((v,i)=>v!==null?i:-1).filter(i=>i>=0).pop();
  if(last===undefined) return;
  s3used.delete(s3slots[last]); s3slots[last]=null;
  document.getElementById('s3msg').innerHTML='';
  s3RenderCards(); s3RenderDisp();
}

function s3Reset(){s3slots=[null,null,null];s3used=new Set();document.getElementById('s3msg').innerHTML='';s3RenderCards();s3RenderDisp();}
s3Reset();

// ─── S4: 시상식 ──────────────────────────────────────────
const S4A=[
  {name:'이서준',emoji:'🏃',c:'#ef4444'},{name:'박민아',emoji:'🏃‍♀️',c:'#3b82f6'},
  {name:'김도현',emoji:'🤸',c:'#10b981'},{name:'최지은',emoji:'🤸‍♀️',c:'#f59e0b'},
  {name:'정우진',emoji:'🧗',c:'#8b5cf6'},{name:'신예슬',emoji:'🤾‍♀️',c:'#06b6d4'},
];
let s4podium=[null,null,null],s4used=new Set();

function s4RenderAthletes(){
  document.getElementById('s4athletes').innerHTML=S4A.map((a,i)=>`
    <div class="person ${s4used.has(i)?'disabled':''}" onclick="s4Pick(${i})">
      <div class="p-circle" style="background:${a.c}">${a.emoji}</div>
      <div class="p-name">${a.name}</div>
    </div>`).join('');
}

function s4RenderPodium(){
  // Visual layout: 2nd(left), 1st(center), 3rd(right)
  const order=[1,0,2];
  const medals=['🥇','🥈','🥉'];
  const heights=[110,82,62];
  const blockC=['#ca8a04','#94a3b8','#78716c'];
  document.getElementById('s4podium').innerHTML=order.map(rank=>{
    const v=s4podium[rank];
    const ath=v!==null?S4A[v]:null;
    return `<div class="podium-col">
      <div class="pod-person ${ath?'placed':''}" style="background:${ath?ath.c:'rgba(255,255,255,.07)'}">
        ${ath?ath.emoji:'?'}
      </div>
      <div style="font-size:.63rem;color:${ath?'#e2e8ff':'#4b5563'};min-height:13px;text-align:center">
        ${ath?ath.name:''}
      </div>
      <div class="pod-block" style="height:${heights[rank]}px;background:${blockC[rank]}">
        ${medals[rank]}
      </div>
    </div>`;
  }).join('');
}

function s4Pick(i){
  if(s4used.has(i)) return;
  const next=s4podium.findIndex(v=>v===null); if(next===-1) return;
  s4podium[next]=i; s4used.add(i);
  s4RenderAthletes(); s4RenderPodium();
  const medals=['🥇','🥈','🥉'];
  const filled=s4podium.filter(v=>v!==null).length;
  if(filled===3){
    const ns=s4podium.map(x=>S4A[x].emoji+S4A[x].name);
    document.getElementById('s4msg').innerHTML=
      `<span class="badge">🏆 ${ns[0]}(1등) · ${ns[1]}(2등) · ${ns[2]}(3등) — P(6,3)=120가지 중 하나!</span>`;
  } else {
    document.getElementById('s4msg').innerHTML=
      `<span style="font-size:.76rem;color:#7788aa">${medals[next]} ${S4A[i].emoji} ${S4A[i].name}이(가) ${next+1}등 입상! (${filled}/3)</span>`;
  }
}

function s4Reset(){s4podium=[null,null,null];s4used=new Set();document.getElementById('s4msg').innerHTML='';s4RenderAthletes();s4RenderPodium();}
s4RenderAthletes(); s4RenderPodium();

// ─── S5: 승부차기 ────────────────────────────────────────
const JERSEY_COLORS=['#dc2626','#2563eb','#059669','#d97706','#7c3aed',
  '#0891b2','#ea580c','#65a30d','#db2777','#0284c7','#9333ea'];
let s5kicks=Array(5).fill(null),s5used=new Set();

function s5Render(){
  document.getElementById('s5players').innerHTML=
    Array.from({length:11},(_,i)=>{
      const num=i+1, used=s5used.has(num);
      return `<div class="jersey ${used?'used':''}" onclick="s5Pick(${num})">
        <div class="jshirt" style="background:${JERSEY_COLORS[i]}">${num}</div>
        <div class="jnum-label">${num}번</div>
      </div>`;
    }).join('');
  document.getElementById('s5kicks').innerHTML=
    s5kicks.map((v,i)=>`
      <div class="kslot">
        <div class="kslot-num">${i+1}번 키커</div>
        <div class="kslot-box" style="background:${v?'rgba(16,185,129,.15)':'rgba(255,255,255,.04)'};
          border:2px ${v?'solid #10b981':'dashed rgba(255,255,255,.18)'};color:${v?'#34d399':'#4b5563'}">
          ${v?`<div style="text-align:center"><div style="font-size:.9rem;font-weight:700">${v}번</div><div style="font-size:.8rem">⚽</div></div>`:'?'}
        </div>
      </div>`).join('');
}

function s5Pick(num){
  if(s5used.has(num)) return;
  const next=s5kicks.findIndex(v=>v===null); if(next===-1) return;
  s5kicks[next]=num; s5used.add(num); s5Render();
  const filled=s5kicks.filter(v=>v!==null).length;
  if(filled===5){
    document.getElementById('s5msg').innerHTML=
      `<span class="badge">⚽ 킥 순서: ${s5kicks.join(' → ')} — P(11,5)=55,440가지 중 하나!</span>`;
  } else {
    document.getElementById('s5msg').innerHTML=
      `<span style="font-size:.76rem;color:#7788aa">${num}번 선수 → ${filled}번째 키커 배정 (${filled}/5)</span>`;
  }
}

function s5Reset(){s5kicks=Array(5).fill(null);s5used=new Set();document.getElementById('s5msg').innerHTML='';s5Render();}
s5Render();

// ─── S6: 비밀번호 ────────────────────────────────────────
let s6pw=Array(4).fill(null),s6used=new Set();

function s6Render(){
  document.getElementById('s6disp').innerHTML=
    s6pw.map(v=>`<div class="ldig ${v!==null?'filled':''}">${v!==null?v:'·'}</div>`).join('');
  document.getElementById('s6numpad').innerHTML=
    [0,1,2,3,4,5,6,7,8,9].map(d=>
      `<button class="npbtn" onclick="s6Pick(${d})" ${s6used.has(d)?'disabled':''}>${d}</button>`
    ).join('');
  document.getElementById('s6lockicon').textContent = s6pw.every(v=>v!==null)?'🔓':'🔒';
}

function s6Pick(d){
  if(s6used.has(d)) return;
  const next=s6pw.findIndex(v=>v===null); if(next===-1) return;
  s6pw[next]=d; s6used.add(d); s6Render();
  if(s6pw.every(v=>v!==null)){
    document.getElementById('s6msg').innerHTML=
      `<span class="badge">🔓 비밀번호 ${s6pw.join('')} 설정 완료! P(10,4)=5,040가지 중 하나!</span>`;
  } else {
    document.getElementById('s6msg').innerHTML=
      `<span style="font-size:.76rem;color:#7788aa">${s6pw.filter(v=>v!==null).length}/4 입력됨</span>`;
  }
}

function s6Back(){
  const last=s6pw.map((v,i)=>v!==null?i:-1).filter(i=>i>=0).pop();
  if(last===undefined) return;
  s6used.delete(s6pw[last]); s6pw[last]=null;
  document.getElementById('s6msg').innerHTML=''; s6Render();
}

function s6Reset(){s6pw=Array(4).fill(null);s6used=new Set();document.getElementById('s6msg').innerHTML='';s6Render();}
s6Render();
</script>
</body>
</html>"""


def render():
    st.markdown("### 🎯 순열 실생활 탐구")
    st.markdown(
        "실생활 속 **6가지 순열 사례**를 직접 조작하며 **P(n, r)** 의 의미를 탐구해보세요!"
    )
    components.html(_HTML, height=1250, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
