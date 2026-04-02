# activities/probability/mini/monty_hall_mini.py
from pathlib import Path
import base64
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "몬티홀시뮬레이터"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 몬티홀 시뮬레이션을 충분히 체험한 뒤, 아래 질문에 답해 보세요.**"},
    {"key": "교체전략이유",  "label": "Q1. 교체 전략이 유지 전략보다 왜 유리한지 자신의 말로 설명하세요.\n(힌트: 처음 선택이 맞을 확률 1/3, 틀릴 확률 2/3 으로부터)", "type": "text_area", "height": 110},
    {"key": "조건부확률표현", "label": "Q2. 몬티가 염소 문을 열어준 *이후* 상황을 조건부확률 P(자동차 | 나머지 문) 로 표현해 보세요.", "type": "text_area", "height": 110},
    {"key": "그래프해석",    "label": "Q3. 자동 시뮬레이션 그래프에서 승률이 어떻게 변해갔나요? 처음에 왜 들쭉날쭉하다가 안정될까요? (관련 수학 법칙도 써보세요)", "type": "text_area", "height": 100},
    {"key": "확장탭결과",   "label": "Q4. 확장 탭에서 문·자동차 개수를 바꿔보며 알게 된 점을 쓰세요. (교체 전략의 이점이 가장 커지는 경우 vs 작아지는 경우)", "type": "text_area", "height": 100},
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title": "미니: 몬티홀 문제 시뮬레이터",
    "description": "유지 vs 교체 전략을 직접 체험하며 조건부확률의 핵심을 이해합니다. 기본(3문)·확장(N문) 탭 제공.",
    "hidden": True,
    "order": 9999999,
}

def _img_uri(path: Path) -> str:
    if not path.exists():
        return ""
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"

def render():
    here = Path(__file__).parent.parent  # activities/probability/
    goat_uri = _img_uri(here / "monty_hall_assets" / "goat.png")
    car_uri  = _img_uri(here / "monty_hall_assets" / "car.png")

    html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
/* ── Reset & Base ─────────────────────────────────────── */
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI','Apple SD Gothic Neo',sans-serif;background:#f4f6ff;color:#1a1a2e;font-size:14px;}
.app{max-width:780px;margin:0 auto;padding:12px 16px 20px;}

/* ── Tabs ────────────────────────────────────────────── */
.tab-nav{display:flex;gap:0;background:#dee2e6;border-radius:12px;padding:4px;margin-bottom:14px;}
.tab-btn{flex:1;padding:10px 8px;border:none;background:transparent;cursor:pointer;font-size:13px;font-weight:800;border-radius:8px;transition:all .15s;color:#868e96;}
.tab-btn.active{background:#fff;color:#3b5bdb;box-shadow:0 1px 6px rgba(0,0,0,.1);}
.tab-pane{display:none;}
.tab-pane.active{display:block;}

/* ── Sliders (ext) ───────────────────────────────────── */
.sliders-row{display:flex;gap:14px;background:#fff;border-radius:12px;padding:12px 14px;margin-bottom:10px;box-shadow:0 1px 6px rgba(0,0,0,.06);}
.slider-grp{flex:1;}
.slider-lbl{font-size:12px;font-weight:800;color:#495057;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;}
.slider-lbl span{font-size:18px;font-weight:900;color:#3b5bdb;}
input[type=range]{width:100%;accent-color:#3b5bdb;height:4px;}

/* ── Theory box ──────────────────────────────────────── */
.theory-box{background:#fff9db;border:2px solid #ffd43b;border-radius:10px;padding:8px 14px;font-size:12px;line-height:1.8;text-align:center;margin-bottom:10px;}

/* ── Phase label ─────────────────────────────────────── */
.phase-lbl{text-align:center;font-size:15px;font-weight:800;color:#3b5bdb;background:#e7f5ff;border-radius:8px;padding:7px 12px;margin-bottom:10px;min-height:36px;display:flex;align-items:center;justify-content:center;}

/* ── Doors ───────────────────────────────────────────── */
.doors-row{display:flex;gap:10px;justify-content:center;margin-bottom:12px;flex-wrap:wrap;}
.door-wrap{display:flex;flex-direction:column;align-items:center;gap:6px;}
.door{
  background:linear-gradient(160deg,#c8932a 0%,#7a4a10 100%);
  border-radius:10px 10px 4px 4px;border:3px solid #5c3409;
  cursor:pointer;position:relative;overflow:hidden;
  transition:transform .15s,box-shadow .15s,background .3s;
  display:flex;align-items:center;justify-content:center;
  box-shadow:2px 4px 10px rgba(0,0,0,.22);
}
.door::before{content:'';position:absolute;top:6px;left:6px;right:6px;bottom:6px;border:1.5px solid rgba(255,255,255,.15);border-radius:6px;pointer-events:none;}
.door:hover:not(.nohov){transform:translateY(-4px) scale(1.04);box-shadow:0 10px 24px rgba(0,0,0,.3);}
.door.chosen{border-color:#2f9e44;box-shadow:0 0 0 3px #51cf66,0 6px 16px rgba(0,0,0,.2);}
.door.opened{background:linear-gradient(160deg,#f8f0e3 0%,#e8d5b0 100%);}
.door.final{border-color:#e67700;box-shadow:0 0 0 3px #ffd43b,0 6px 16px rgba(0,0,0,.2);}
.door.nohov{cursor:default;}
.door-num{font-weight:900;color:rgba(255,255,255,.25);pointer-events:none;user-select:none;transition:opacity .3s;}
.door.opened .door-num{opacity:0;}
.door-knob{background:#e8b87a;border-radius:50%;border:2px solid #7a4a10;position:absolute;right:9px;top:50%;transform:translateY(-50%);transition:opacity .3s;}
.door.opened .door-knob{opacity:0;}
.door-img{object-fit:contain;opacity:0;transition:opacity .45s ease;position:absolute;}
.door-img.show{opacity:1;}
.dbadge{font-size:9px;font-weight:800;padding:2px 6px;border-radius:20px;position:absolute;bottom:5px;left:50%;transform:translateX(-50%);white-space:nowrap;}
.bg{background:#ffe8cc;color:#b34700;}
.bc{background:#d3f9d8;color:#1e6e32;}
.by{background:#ffe066;color:#7a5800;}
.door-lbl{font-size:12px;font-weight:800;color:#495057;padding:2px 10px;border-radius:20px;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.1);}

/* ── Action row ──────────────────────────────────────── */
.act-row{display:flex;gap:10px;justify-content:center;margin-bottom:10px;min-height:48px;align-items:center;flex-wrap:wrap;}
.btn{padding:10px 26px;border-radius:12px;border:none;font-size:14px;font-weight:800;cursor:pointer;transition:all .15s;}
.b-stay{background:#4dabf7;color:#fff;box-shadow:0 3px 8px rgba(77,171,247,.4);}
.b-stay:hover{background:#339af0;transform:translateY(-2px);}
.b-switch{background:#ff6b6b;color:#fff;box-shadow:0 3px 8px rgba(255,107,107,.4);}
.b-switch:hover{background:#fa5252;transform:translateY(-2px);}
.b-reset{background:#dee2e6;color:#495057;}
.b-reset:hover{background:#ced4da;transform:translateY(-2px);}

/* ── Result banner ───────────────────────────────────── */
.result{text-align:center;padding:10px 16px;border-radius:12px;font-size:17px;font-weight:800;margin-bottom:10px;display:none;animation:pop .3s ease;}
@keyframes pop{from{transform:scale(.85);opacity:0;}to{transform:scale(1);opacity:1;}}
.result.win{background:#d3f9d8;color:#2b8a3e;border:2px solid #8ce99a;display:block;}
.result.lose{background:#ffe3e3;color:#c92a2a;border:2px solid #ffa8a8;display:block;}

/* ── Bottom 2-col ────────────────────────────────────── */
.bot{display:flex;gap:12px;margin-top:2px;}
.lp{flex:1;min-width:0;display:flex;flex-direction:column;gap:8px;}
.rp{width:310px;flex-shrink:0;display:flex;flex-direction:column;gap:8px;}

/* ── Stats ───────────────────────────────────────────── */
.stats-box{background:#fff;border-radius:12px;padding:11px 13px;box-shadow:0 2px 8px rgba(0,0,0,.07);}
.box-title{font-weight:800;font-size:12px;margin-bottom:8px;color:#868e96;}
.s-row{display:flex;align-items:center;gap:8px;margin-bottom:6px;}
.s-lbl{width:32px;font-size:11px;font-weight:800;flex-shrink:0;text-align:center;}
.s-bar-bg{flex:1;height:20px;background:#f1f3f5;border-radius:6px;overflow:hidden;position:relative;}
.s-bar{height:100%;border-radius:6px;transition:width .5s cubic-bezier(.4,0,.2,1);}
.bar-s{background:linear-gradient(90deg,#74c0fc,#339af0);}
.bar-w{background:linear-gradient(90deg,#ff8787,#fa5252);}
.s-mark{width:1.5px;height:100%;background:#495057;position:absolute;top:0;opacity:.35;}
.s-pct{width:118px;text-align:right;font-size:11px;font-weight:700;flex-shrink:0;color:#495057;}

/* ── Batch ───────────────────────────────────────────── */
.batch-box{background:#fff;border-radius:12px;padding:11px 13px;box-shadow:0 2px 8px rgba(0,0,0,.07);}
.br{display:flex;align-items:center;gap:7px;margin-bottom:5px;}
.br-lbl{width:32px;font-size:11px;font-weight:800;flex-shrink:0;text-align:center;}
.bbtns{display:flex;gap:4px;flex-wrap:wrap;}
.bx{padding:5px 11px;font-size:11px;border-radius:7px;border:none;cursor:pointer;font-weight:800;transition:all .12s;}
.bx-s{background:#dbe4ff;color:#364fc7;}
.bx-s:hover{background:#bac8ff;}
.bx-w{background:#ffe0e0;color:#c92a2a;}
.bx-w:hover{background:#ffc9c9;}
.bx-g{background:#f1f3f5;color:#495057;}
.bx-g:hover{background:#e9ecef;}

/* ── Auto-sim (right panel) ──────────────────────────── */
.auto-box{background:#fff;border-radius:12px;padding:11px 13px;box-shadow:0 2px 8px rgba(0,0,0,.07);display:flex;flex-direction:column;flex:1;}
.auto-btns{display:flex;gap:6px;margin-bottom:8px;flex-wrap:wrap;}
.a-stay{background:#e7f5ff;color:#1971c2;border:none;padding:6px 12px;border-radius:8px;font-size:12px;font-weight:800;cursor:pointer;transition:all .12s;}
.a-stay:hover{background:#d0ebff;}
.a-switch{background:#fff5f5;color:#c92a2a;border:none;padding:6px 12px;border-radius:8px;font-size:12px;font-weight:800;cursor:pointer;transition:all .12s;}
.a-switch:hover{background:#ffe3e3;}
.a-stop{background:#f8f9fa;color:#868e96;border:1.5px solid #dee2e6;padding:6px 12px;border-radius:8px;font-size:12px;font-weight:800;cursor:pointer;display:none;}
.a-stop.show{display:block;}
canvas{width:100%;border-radius:6px;display:block;background:#fafbff;}
.legend{display:flex;gap:10px;justify-content:center;margin-top:5px;flex-wrap:wrap;}
.leg{display:flex;align-items:center;gap:4px;font-size:10px;color:#495057;}
.ld{width:18px;height:3px;border-radius:2px;flex-shrink:0;}
.ldd{width:18px;height:0;border-top:2px dashed;flex-shrink:0;}

/* ── Quiz tab ────────────────────────────────────────── */
.q-sec{background:#fff;border-radius:14px;padding:14px 16px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,.07);}
.q-sec h3{font-size:13px;font-weight:900;color:#3b5bdb;margin-bottom:12px;padding-bottom:7px;border-bottom:2px solid #e7f5ff;}
.step-card{background:#f8f9ff;border-radius:10px;padding:11px 13px;margin-bottom:9px;border-left:4px solid #4dabf7;}
.step-card.green{border-left-color:#2f9e44;background:#f4fef6;}
.step-card.violet{border-left-color:#845ef7;background:#f8f4ff;}
.step-head{font-size:10px;font-weight:900;color:#4dabf7;margin-bottom:4px;letter-spacing:.6px;text-transform:uppercase;}
.step-card.green .step-head{color:#2f9e44;}
.step-card.violet .step-head{color:#845ef7;}
.step-title{font-size:13px;font-weight:800;margin-bottom:8px;}
.fill-row{display:flex;align-items:center;gap:6px;margin:5px 0;font-size:13px;flex-wrap:wrap;line-height:1.8;}
.fi{width:46px;text-align:center;border:2px solid #4dabf7;border-radius:6px;padding:3px 4px;font-size:14px;font-weight:800;outline:none;transition:border-color .2s;}
.fi:focus{border-color:#339af0;box-shadow:0 0 0 2px rgba(77,171,247,.2);}
.fi.ok{border-color:#2f9e44!important;background:#d3f9d8;color:#2b8a3e;}
.fi.ng{border-color:#c92a2a!important;background:#ffe3e3;animation:shake .3s;}
@keyframes shake{0%,100%{transform:translateX(0);}25%{transform:translateX(-4px);}75%{transform:translateX(4px);}}
.chk-btn{padding:3px 9px;border-radius:6px;border:none;background:#4dabf7;color:#fff;font-size:11px;font-weight:800;cursor:pointer;}
.chk-btn:hover{background:#339af0;}
.fb{font-size:11px;font-weight:800;min-width:60px;}
.fb.ok{color:#2f9e44;}.fb.ng{color:#c92a2a;}
.mcq-opt{display:flex;align-items:flex-start;gap:8px;padding:7px 10px;border-radius:8px;cursor:pointer;border:1.5px solid #e9ecef;margin-bottom:5px;font-size:12px;transition:border-color .15s;user-select:none;}
.mcq-opt:hover{border-color:#4dabf7;}
.mcq-opt.correct{background:#d3f9d8;border-color:#2f9e44;}
.mcq-opt.wrong{background:#ffe3e3;border-color:#c92a2a;}
.mcq-opt.reveal-correct{background:#d3f9d8;border-color:#2f9e44;}
.mcq-btn{padding:5px 14px;border-radius:7px;border:none;background:#845ef7;color:#fff;font-size:12px;font-weight:800;cursor:pointer;margin-top:5px;}
.mcq-btn:hover{background:#7950f2;}
.formula-box{background:#f8f9ff;border:1.5px solid #4dabf7;border-radius:10px;padding:10px 14px;margin:7px 0;font-size:12px;line-height:2.1;}
.hl-b{color:#1971c2;font-weight:900;}.hl-r{color:#c92a2a;font-weight:900;}.hl-g{color:#2b8a3e;font-weight:900;}
.reveal-all-btn{padding:5px 12px;border-radius:7px;border:1.5px solid #dee2e6;background:#f8f9fa;color:#495057;font-size:11px;font-weight:800;cursor:pointer;margin-top:4px;}
.reveal-all-btn:hover{background:#e9ecef;}
.insight-box{background:#fff3bf;border:2px solid #ffd43b;border-radius:10px;padding:9px 13px;font-size:12px;line-height:1.8;margin:7px 0;}
.case-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0;}
.case-card{background:#fff;border-radius:10px;padding:10px 12px;border:1.5px solid #dee2e6;font-size:12px;line-height:1.9;}
.case-card h4{font-size:12px;font-weight:900;margin-bottom:5px;}
.case-card.car-case{border-color:#bac8ff;background:#f0f4ff;}
.case-card.goat-case{border-color:#ffc9c9;background:#fff5f5;}
</style>
</head>
<body>
<div class="app">

<!-- ═══ TAB NAV ════════════════════════════════════════ -->
<div class="tab-nav">
  <button class="tab-btn active" id="btn-b" onclick="switchTab('b')">🎯 기본 몬티홀</button>
  <button class="tab-btn"        id="btn-e" onclick="switchTab('e')">🔢 확장 몬티홀</button>
  <button class="tab-btn"        id="btn-p" onclick="switchTab('p')">📐 수학적 원리</button>
</div>

<!-- ═══ TAB BASIC ══════════════════════════════════════ -->
<div id="tab-b" class="tab-pane active">
  <div class="theory-box">📐 이론값 &nbsp;|&nbsp; <strong>유지</strong> = 1/3 ≈ 33.3% &nbsp;&nbsp; <strong>교체</strong> = 2/3 ≈ 66.7%</div>
  <div class="phase-lbl" id="b-phase">아래 문 중 하나를 선택하세요 🚪</div>
  <div class="doors-row" id="b-doors"></div>
  <div class="act-row"   id="b-act"></div>
  <div class="result"    id="b-res"></div>
  <div class="bot">
    <div class="lp">
      <div class="stats-box">
        <div class="box-title">📊 누적 통계</div>
        <div class="s-row">
          <div class="s-lbl" style="color:#1971c2">유지</div>
          <div class="s-bar-bg">
            <div class="s-bar bar-s" id="b-bs" style="width:0%"></div>
            <div class="s-mark" style="left:33.3%"></div>
          </div>
          <div class="s-pct" id="b-ps">0승/0회 (0%)</div>
        </div>
        <div class="s-row">
          <div class="s-lbl" style="color:#c92a2a">교체</div>
          <div class="s-bar-bg">
            <div class="s-bar bar-w" id="b-bw" style="width:0%"></div>
            <div class="s-mark" style="left:66.7%"></div>
          </div>
          <div class="s-pct" id="b-pw">0승/0회 (0%)</div>
        </div>
      </div>
      <div class="batch-box">
        <div class="box-title">⚡ 일괄 시뮬레이션</div>
        <div class="br">
          <div class="br-lbl" style="color:#1971c2">유지</div>
          <div class="bbtns">
            <button class="bx bx-s" onclick="batch('b',100,false)">100</button>
            <button class="bx bx-s" onclick="batch('b',1000,false)">1,000</button>
            <button class="bx bx-s" onclick="batch('b',10000,false)">10,000</button>
          </div>
        </div>
        <div class="br">
          <div class="br-lbl" style="color:#c92a2a">교체</div>
          <div class="bbtns">
            <button class="bx bx-w" onclick="batch('b',100,true)">100</button>
            <button class="bx bx-w" onclick="batch('b',1000,true)">1,000</button>
            <button class="bx bx-w" onclick="batch('b',10000,true)">10,000</button>
          </div>
        </div>
        <div class="br" style="margin-top:2px">
          <div class="br-lbl"></div>
          <button class="bx bx-g" onclick="resetAll('b')">전체 초기화</button>
        </div>
      </div>
    </div>
    <div class="rp">
      <div class="auto-box">
        <div class="box-title">📈 실시간 수렴 그래프</div>
        <div class="auto-btns">
          <button class="a-stay"   onclick="startAuto('b',false)">▶ 유지 자동 시뮬</button>
          <button class="a-switch" onclick="startAuto('b',true)">▶ 교체 자동 시뮬</button>
          <button class="a-stop"   id="b-stop" onclick="stopAuto()">■ 정지</button>
        </div>
        <canvas id="b-cvs" height="180"></canvas>
        <div class="legend">
          <div class="leg"><div class="ld" style="background:#339af0"></div>유지 실험</div>
          <div class="leg"><div class="ld" style="background:#fa5252"></div>교체 실험</div>
          <div class="leg"><div class="ldd" style="border-color:#339af0"></div>유지 이론</div>
          <div class="leg"><div class="ldd" style="border-color:#fa5252"></div>교체 이론</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══ TAB EXTENDED ══════════════════════════════════ -->
<div id="tab-e" class="tab-pane">
  <div class="sliders-row">
    <div class="slider-grp">
      <div class="slider-lbl">문의 개수 <span id="e-nv">3</span>개</div>
      <input type="range" id="e-n" min="3" max="10" value="3" oninput="onSlider()">
    </div>
    <div class="slider-grp">
      <div class="slider-lbl">자동차 개수 <span id="e-kv">1</span>대</div>
      <input type="range" id="e-k" min="1" max="8" value="1" oninput="onSlider()">
    </div>
  </div>
  <div class="theory-box" id="e-theory">...</div>
  <div class="phase-lbl" id="e-phase">아래 문 중 하나를 선택하세요 🚪</div>
  <div class="doors-row" id="e-doors"></div>
  <div class="act-row"   id="e-act"></div>
  <div class="result"    id="e-res"></div>
  <div class="bot">
    <div class="lp">
      <div class="stats-box">
        <div class="box-title">📊 누적 통계</div>
        <div class="s-row">
          <div class="s-lbl" style="color:#1971c2">유지</div>
          <div class="s-bar-bg">
            <div class="s-bar bar-s" id="e-bs" style="width:0%"></div>
            <div class="s-mark" id="e-sm-s" style="left:33.3%"></div>
          </div>
          <div class="s-pct" id="e-ps">0승/0회 (0%)</div>
        </div>
        <div class="s-row">
          <div class="s-lbl" style="color:#c92a2a">교체</div>
          <div class="s-bar-bg">
            <div class="s-bar bar-w" id="e-bw" style="width:0%"></div>
            <div class="s-mark" id="e-sm-w" style="left:66.7%"></div>
          </div>
          <div class="s-pct" id="e-pw">0승/0회 (0%)</div>
        </div>
      </div>
      <div class="batch-box">
        <div class="box-title">⚡ 일괄 시뮬레이션</div>
        <div class="br">
          <div class="br-lbl" style="color:#1971c2">유지</div>
          <div class="bbtns">
            <button class="bx bx-s" onclick="batch('e',100,false)">100</button>
            <button class="bx bx-s" onclick="batch('e',1000,false)">1,000</button>
            <button class="bx bx-s" onclick="batch('e',10000,false)">10,000</button>
          </div>
        </div>
        <div class="br">
          <div class="br-lbl" style="color:#c92a2a">교체</div>
          <div class="bbtns">
            <button class="bx bx-w" onclick="batch('e',100,true)">100</button>
            <button class="bx bx-w" onclick="batch('e',1000,true)">1,000</button>
            <button class="bx bx-w" onclick="batch('e',10000,true)">10,000</button>
          </div>
        </div>
        <div class="br" style="margin-top:2px">
          <div class="br-lbl"></div>
          <button class="bx bx-g" onclick="resetAll('e')">전체 초기화</button>
        </div>
      </div>
    </div>
    <div class="rp">
      <div class="auto-box">
        <div class="box-title">📈 실시간 수렴 그래프</div>
        <div class="auto-btns">
          <button class="a-stay"   onclick="startAuto('e',false)">▶ 유지 자동 시뮬</button>
          <button class="a-switch" onclick="startAuto('e',true)">▶ 교체 자동 시뮬</button>
          <button class="a-stop"   id="e-stop" onclick="stopAuto()">■ 정지</button>
        </div>
        <canvas id="e-cvs" height="180"></canvas>
        <div class="legend">
          <div class="leg"><div class="ld" style="background:#339af0"></div>유지 실험</div>
          <div class="leg"><div class="ld" style="background:#fa5252"></div>교체 실험</div>
          <div class="leg"><div class="ldd" style="border-color:#339af0"></div>유지 이론</div>
          <div class="leg"><div class="ldd" style="border-color:#fa5252"></div>교체 이론</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══ TAB MATH ══════════════════════════════════════ -->
<div id="tab-p" class="tab-pane">

<!-- ── Part 1: 기본 확률 계산 ──────────────────────── -->
<div class="q-sec">
  <h3>Part 1. 기본 몬티홀 — 단계별 확률 계산 (문 3개, 자동차 1개)</h3>

  <div class="step-card">
    <div class="step-head">STEP 1</div>
    <div class="step-title">처음 선택의 확률</div>
    <p style="font-size:12px;margin-bottom:8px;">문이 3개이고 자동차는 1대입니다. 임의로 문 하나를 선택할 때:</p>
    <div class="fill-row">
      P(🚗) &nbsp;=&nbsp; <input class="fi" id="p1a" maxlength="2"> / 3
      <button class="chk-btn" onclick="chk('p1a',['1'],'f1a')">확인</button>
      <span class="fb" id="f1a"></span>
    </div>
    <div class="fill-row">
      P(🐐) &nbsp;=&nbsp; <input class="fi" id="p1b" maxlength="2"> / 3
      <button class="chk-btn" onclick="chk('p1b',['2'],'f1b')">확인</button>
      <span class="fb" id="f1b"></span>
    </div>
    <button class="reveal-all-btn" onclick="revealGroup(['p1a','1','f1a','p1b','2','f1b'])">정답 보기</button>
  </div>

  <div class="step-card">
    <div class="step-head">STEP 2</div>
    <div class="step-title">두 가지 경우로 나누어 분석</div>
    <div class="case-grid">
      <div class="case-card car-case">
        <h4>경우 A: 처음 선택 = 🚗 &nbsp;<span style="font-weight:400;color:#868e96">(확률 1/3)</span></h4>
        <div>남은 2개 문: 🐐🐐</div>
        <div>몬티가 <strong>🐐 1개</strong> 공개</div>
        <div>남은 1개 문: <strong class="hl-r">🐐</strong></div>
        <div style="margin-top:4px;">유지 → <span class="hl-g">🚗 승리</span></div>
        <div>교체 → <span class="hl-r">🐐 패배</span></div>
      </div>
      <div class="case-card goat-case">
        <h4>경우 B: 처음 선택 = 🐐 &nbsp;<span style="font-weight:400;color:#868e96">(확률 2/3)</span></h4>
        <div>남은 2개 문: 🚗🐐</div>
        <div>몬티가 <strong>🐐 1개</strong>만 공개 가능</div>
        <div>남은 1개 문: <strong class="hl-g">🚗</strong></div>
        <div style="margin-top:4px;">유지 → <span class="hl-r">🐐 패배</span></div>
        <div>교체 → <span class="hl-g">🚗 승리</span></div>
      </div>
    </div>
    <div class="insight-box">💡 핵심: 경우 B에서 몬티는 <strong>반드시 🐐 문만</strong> 열 수 있습니다. 나머지 문에 자동차가 "몰립니다"!</div>
  </div>

  <div class="step-card green">
    <div class="step-head">STEP 3</div>
    <div class="step-title">전략별 승률 계산</div>
    <div class="formula-box">
      <div>P(<span class="hl-b">유지</span> 전략 승리) = P(경우 A) = <input class="fi" id="p3a" maxlength="2" style="border-color:#2f9e44;"> / 3 &nbsp;≈ 33.3%
        <button class="chk-btn" style="background:#2f9e44" onclick="chk('p3a',['1'],'f3a')">확인</button>
        <span class="fb" id="f3a"></span>
      </div>
      <div>P(<span class="hl-r">교체</span> 전략 승리) = P(경우 B) × 1 = <input class="fi" id="p3b" maxlength="2" style="border-color:#fa5252;"> / 3 &nbsp;≈ 66.7%
        <button class="chk-btn" style="background:#fa5252" onclick="chk('p3b',['2'],'f3b')">확인</button>
        <span class="fb" id="f3b"></span>
      </div>
    </div>
    <div class="fill-row" style="margin-top:4px;font-size:12px;">
      → 교체 전략이 유지 전략보다 &nbsp;<input class="fi" id="p3c" maxlength="2" style="width:38px;"> 배 유리합니다!
      <button class="chk-btn" onclick="chk('p3c',['2'],'f3c')">확인</button>
      <span class="fb" id="f3c"></span>
    </div>
    <button class="reveal-all-btn" onclick="revealGroup(['p3a','1','f3a','p3b','2','f3b','p3c','2','f3c'])">정답 보기</button>
  </div>
</div>

<!-- ── Part 2: 흔한 오해 퀴즈 ───────────────────────── -->
<div class="q-sec">
  <h3>Part 2. 자주 묻는 질문 — 맞는 것을 고르세요</h3>

  <!-- MCQ 1 -->
  <div class="step-card">
    <div class="step-head">QUIZ 1</div>
    <div class="step-title">몬티가 문을 연 후 남은 문이 2개입니다. 자동차가 있을 확률은 50%/50%인가요?</div>
    <div id="mcq1">
      <div class="mcq-opt" onclick="selectMCQ('mcq1',0)"><span>①</span> 맞다. 남은 문이 2개이므로 각각 1/2이다.</div>
      <div class="mcq-opt" onclick="selectMCQ('mcq1',1)"><span>②</span> 틀리다. 처음 선택한 문은 여전히 1/3이고, 나머지 문은 2/3이다.</div>
      <div class="mcq-opt" onclick="selectMCQ('mcq1',2)"><span>③</span> 처음 선택을 취소하고 다시 고르면 50%가 된다.</div>
    </div>
    <button class="mcq-btn" onclick="checkMCQ('mcq1',1,'mfb1')">정답 확인</button>
    <div class="fb" id="mfb1" style="margin-top:5px;font-size:12px;line-height:1.6;"></div>
  </div>

  <!-- MCQ 2 -->
  <div class="step-card">
    <div class="step-head">QUIZ 2</div>
    <div class="step-title">만약 몬티가 자동차 위치를 모르고 아무 문이나 열었는데 우연히 염소였다면?</div>
    <div id="mcq2">
      <div class="mcq-opt" onclick="selectMCQ('mcq2',0)"><span>①</span> 교체 전략 승률은 여전히 2/3이다.</div>
      <div class="mcq-opt" onclick="selectMCQ('mcq2',1)"><span>②</span> 이 경우 교체 전략 승률은 1/2이 된다.</div>
      <div class="mcq-opt" onclick="selectMCQ('mcq2',2)"><span>③</span> 교체 전략 승률은 1/3이 된다.</div>
    </div>
    <button class="mcq-btn" onclick="checkMCQ('mcq2',1,'mfb2')">정답 확인</button>
    <div class="fb" id="mfb2" style="margin-top:5px;font-size:12px;line-height:1.6;"></div>
  </div>

  <!-- MCQ 3 -->
  <div class="step-card">
    <div class="step-head">QUIZ 3</div>
    <div class="step-title">문이 100개이고, 몬티가 98개의 염소 문을 열었습니다. 교체해야 할까요?</div>
    <div id="mcq3">
      <div class="mcq-opt" onclick="selectMCQ('mcq3',0)"><span>①</span> 교체한다. 교체 전략 승률 = 99/100 = 99%</div>
      <div class="mcq-opt" onclick="selectMCQ('mcq3',1)"><span>②</span> 상관없다. 남은 2개 문이므로 50%/50%이다.</div>
      <div class="mcq-opt" onclick="selectMCQ('mcq3',2)"><span>③</span> 유지한다. 이미 고른 문이 맞을 확률이 높아졌다.</div>
    </div>
    <button class="mcq-btn" onclick="checkMCQ('mcq3',0,'mfb3')">정답 확인</button>
    <div class="fb" id="mfb3" style="margin-top:5px;font-size:12px;line-height:1.6;"></div>
  </div>
</div>

<!-- ── Part 3: 확장 공식 유도 ────────────────────────── -->
<div class="q-sec">
  <h3>Part 3. 확장 몬티홀 — 일반 공식 유도</h3>
  <p style="font-size:12px;color:#868e96;margin-bottom:10px;">먼저 구체적인 예(5문, 2차)로 계산한 뒤, 일반 공식을 유도합니다.</p>

  <div class="step-card">
    <div class="step-head">예시 계산 — 문 5개, 자동차 2대</div>
    <div class="step-title">유지 전략 승률</div>
    <div class="fill-row">
      P(유지 승리) = (자동차 수) / (전체 문 수) =
      <input class="fi" id="e1a" maxlength="2"> / <input class="fi" id="e1b" maxlength="2">
      <button class="chk-btn" onclick="chkPair('e1a','2','e1b','5','ef1')">확인</button>
      <span class="fb" id="ef1"></span>
    </div>
  </div>

  <div class="step-card">
    <div class="step-head">예시 계산 — 교체 전략 분석</div>
    <div class="step-title">경우를 나누어 계산합니다</div>
    <div class="case-grid">
      <div class="case-card car-case">
        <h4>처음 선택 = 🚗 <span style="font-weight:400">(확률 2/5)</span></h4>
        <div>남은 4개: 🚗<input class="fi" id="e2a" maxlength="1" style="width:36px;">개, 🐐<input class="fi" id="e2b" maxlength="1" style="width:36px;">개
          <button class="chk-btn" onclick="chkPair('e2a','1','e2b','3','ef2')">확인</button>
          <span class="fb" id="ef2"></span>
        </div>
        <div>몬티 공개 후 남은 3개 중 🚗: <input class="fi" id="e2c" maxlength="1" style="width:36px;">개
          <button class="chk-btn" onclick="chk('e2c',['1'],'ef2c')">확인</button>
          <span class="fb" id="ef2c"></span>
        </div>
        <div>교체 후 승률 = <strong>1/3</strong></div>
      </div>
      <div class="case-card goat-case">
        <h4>처음 선택 = 🐐 <span style="font-weight:400">(확률 3/5)</span></h4>
        <div>남은 4개: 🚗<input class="fi" id="e3a" maxlength="1" style="width:36px;">개, 🐐<input class="fi" id="e3b" maxlength="1" style="width:36px;">개
          <button class="chk-btn" onclick="chkPair('e3a','2','e3b','2','ef3')">확인</button>
          <span class="fb" id="ef3"></span>
        </div>
        <div>몬티 공개 후 남은 3개 중 🚗: <input class="fi" id="e3c" maxlength="1" style="width:36px;">개
          <button class="chk-btn" onclick="chk('e3c',['2'],'ef3c')">확인</button>
          <span class="fb" id="ef3c"></span>
        </div>
        <div>교체 후 승률 = <strong>2/3</strong></div>
      </div>
    </div>
    <button class="reveal-all-btn" onclick="revealGroup(['e2a','1','ef2','e2b','3','ef2','e2c','1','ef2c','e3a','2','ef3','e3b','2','ef3','e3c','2','ef3c'])">정답 보기</button>
  </div>

  <div class="step-card green">
    <div class="step-head">예시 최종 계산</div>
    <div class="step-title">P(교체 승리) — 빈칸을 채우세요</div>
    <div class="formula-box">
      P(교체 승리)
      &nbsp;=&nbsp; 2/5 × 1/3 &nbsp;+&nbsp; 3/5 × 2/3<br>
      &nbsp;=&nbsp; <input class="fi" id="e4a" maxlength="2"> / 15 &nbsp;+&nbsp; <input class="fi" id="e4b" maxlength="2"> / 15
      <button class="chk-btn" onclick="chkPair('e4a','2','e4b','6','ef4')">확인</button>
      <span class="fb" id="ef4"></span>
      <br>
      &nbsp;=&nbsp; <input class="fi" id="e4c" maxlength="2"> / 15 &nbsp;≈ 53.3%
      <button class="chk-btn" onclick="chk('e4c',['8'],'ef4c')">확인</button>
      <span class="fb" id="ef4c"></span>
    </div>
    <button class="reveal-all-btn" onclick="revealGroup(['e4a','2','ef4','e4b','6','ef4','e4c','8','ef4c'])">정답 보기</button>
  </div>

  <div class="step-card violet">
    <div class="step-head">일반화 — n문, k자동차</div>
    <div class="step-title">위 과정을 n, k로 일반화하면:</div>
    <div class="formula-box">
      P(유지 승리) &nbsp;=&nbsp; <span class="hl-b">k / n</span><br><br>
      P(교체 승리)<br>
      &nbsp;=&nbsp; <span class="hl-b">k/n</span> × (k−1)/(n−2) &nbsp;+&nbsp; <span class="hl-r">(n−k)/n</span> × k/(n−2)<br>
      &nbsp;=&nbsp; k / [n(n−2)] × [(k−1) + (n−k)]<br>
      &nbsp;=&nbsp; k / [n(n−2)] × (n−1)<br>
      &nbsp;=&nbsp; <span class="hl-g">k(n−1) / [n(n−2)]</span>
    </div>
    <div class="insight-box" style="margin-top:8px;">
      💡 검증: n=5, k=2 → 2×4/(5×3) = 8/15 ✓ &nbsp;&nbsp; n=3, k=1 → 1×2/(3×1) = 2/3 ✓
    </div>
    <div class="step-title" style="margin-top:10px;">연습 문제: n=4, k=1일 때 교체 전략의 승률은?</div>
    <div class="fill-row">
      P(교체) = 1 × 3 / (4 × 2) = <input class="fi" id="e5a" maxlength="2"> / <input class="fi" id="e5b" maxlength="2">
      <button class="chk-btn" onclick="chkPair('e5a','3','e5b','8','ef5')">확인</button>
      <span class="fb" id="ef5"></span>
    </div>
    <div class="fill-row">
      P(유지) = 1 / 4 = <input class="fi" id="e5c" maxlength="3"> (소수로)
      <button class="chk-btn" onclick="chk('e5c',['0.25','1/4','25%'],'ef5c')">확인</button>
      <span class="fb" id="ef5c"></span>
    </div>
    <button class="reveal-all-btn" onclick="revealGroup(['e5a','3','ef5','e5b','8','ef5','e5c','0.25','ef5c'])">정답 보기</button>
  </div>
</div>

</div><!-- tab-p -->

</div><!-- .app -->
<script>
const GOAT = "__GOAT__";
const CAR  = "__CAR__";

// ── Utils ─────────────────────────────────────────────────────
function ri(n){ return Math.floor(Math.random()*n); }
function g(id){ return document.getElementById(id); }
function setText(id,v){ g(id).textContent = v; }

// ── Basic state ───────────────────────────────────────────────
var bCar=-1, bChosen=-1, bRev=-1, bPhase=0;
var bSW=0, bST=0, bWW=0, bWT=0; // stay wins/total, switch wins/total

// ── Extended state ────────────────────────────────────────────
var eN=3, eK=1;
var eCars=[], eChosen=-1, eRev=-1, ePhase=0;
var eSW=0, eST=0, eWW=0, eWT=0;

// ── Graph data (auto-sim trajectories only) ───────────────────
var gd = { b:{stay:[],sw:[]}, e:{stay:[],sw:[]} };

// ── Auto-sim ──────────────────────────────────────────────────
var atimer=null, aTab=null, aStrat=null, aW=0, aG=0;
var AUTO_MAX=500, AUTO_BATCH=10, AUTO_MS=55;

// ── Tab switching ─────────────────────────────────────────────
function switchTab(t){
  ['b','e','p'].forEach(function(x){
    g('tab-'+x).classList.toggle('active', x===t);
    g('btn-'+x).classList.toggle('active', x===t);
  });
  if(t==='e') updateExtTheory();
  if(t==='b'||t==='e') setTimeout(function(){ drawGraph(t); },50);
}

// ══════════════════════════════════════════════════════════════
//  BASIC GAME
// ══════════════════════════════════════════════════════════════
function bInit(){
  bCar=ri(3); bChosen=-1; bRev=-1; bPhase=0;
  bRender();
  setText('b-phase','아래 문 중 하나를 선택하세요 🚪');
  setActs('b-act',[]);
  hideRes('b-res');
}

function bRender(){
  var row=g('b-doors'); row.innerHTML='';
  for(var i=0;i<3;i++){
    var open  = bPhase===2 || (bPhase===1 && i===bRev);
    var chose = bPhase<2 && i===bChosen;
    var fin   = bPhase===2 && i===bChosen;
    row.appendChild(makeDoor(i, bCar, open, chose, fin, 150, 200, 44, bPhase, i===bRev, bPhase, 'b'));
  }
}

function bChoose(i){
  if(bPhase!==0) return;
  bChosen=i;
  for(var j=0;j<3;j++){ if(j!==bCar && j!==bChosen){bRev=j;break;} }
  bPhase=1; bRender();
  setText('b-phase','문 '+(bRev+1)+'에 염소가 있네요! — 문 '+(bChosen+1)+'을(를) 유지할까요, 교체할까요?');
  setActs('b-act',[
    {label:'✋ 유지하기', cls:'btn b-stay',   fn:function(){bDecide(false);}},
    {label:'🔄 교체하기', cls:'btn b-switch', fn:function(){bDecide(true);}},
  ]);
}

function bDecide(sw){
  if(bPhase!==1) return;
  if(sw){ for(var j=0;j<3;j++){ if(j!==bChosen&&j!==bRev){bChosen=j;break;} } }
  bPhase=2;
  var won=bChosen===bCar;
  if(sw){bWT++;if(won)bWW++;}else{bST++;if(won)bSW++;}
  bRender(); updateStats('b');
  showRes('b-res', won, (sw?'교체':'유지')+' 전략 — '+(won?'🎉 자동차를 얻었어요!':'🐐 아쉽게도 염소네요!'));
  setText('b-phase','자동차는 문 '+(bCar+1)+'에 있었어요!');
  setActs('b-act',[{label:'🔁 다시 하기',cls:'btn b-reset',fn:bInit}]);
}

// ══════════════════════════════════════════════════════════════
//  EXTENDED GAME
// ══════════════════════════════════════════════════════════════
function eInit(){
  eCars=[];
  while(eCars.length<eK){ var c=ri(eN); if(eCars.indexOf(c)<0) eCars.push(c); }
  eChosen=-1; eRev=-1; ePhase=0;
  eRender();
  setText('e-phase','아래 문 중 하나를 선택하세요 🚪');
  setActs('e-act',[]);
  hideRes('e-res');
}

function getDim(n){
  var avail=700-(n-1)*8;
  var w=Math.min(140, Math.max(50, Math.floor(avail/n)));
  return {w:w, h:Math.round(w*1.45)};
}

function eRender(){
  var row=g('e-doors'); row.innerHTML='';
  var dim=getDim(eN);
  var fs=Math.max(12,Math.min(38,Math.round(dim.w*0.3)));
  for(var i=0;i<eN;i++){
    var isCar=eCars.indexOf(i)>=0;
    var open  = ePhase===2 || (ePhase===1 && i===eRev);
    var chose = ePhase<2 && i===eChosen;
    var fin   = ePhase===2 && i===eChosen;
    var d=makeDoor(i, isCar?i:-1, open, chose, fin, dim.w, dim.h, fs, ePhase, i===eRev, ePhase, 'e');
    // override isCar for makeDoor: pass carIndex list differently
    // rebuild the img src properly
    var img=d.querySelector('.door-img');
    if(img) img.src = isCar ? CAR : GOAT;
    row.appendChild(d);
  }
}

function eChoose(i){
  if(ePhase!==0) return;
  eChosen=i;
  for(var j=0;j<eN;j++){
    if(eCars.indexOf(j)<0 && j!==eChosen){eRev=j;break;}
  }
  if(eRev<0){eInit();return;}
  ePhase=1; eRender();
  setText('e-phase','문 '+(eRev+1)+'에 염소가 있네요! — 문 '+(eChosen+1)+'을(를) 유지할까요, 교체할까요?');
  setActs('e-act',[
    {label:'✋ 유지하기', cls:'btn b-stay',   fn:function(){eDecide(false);}},
    {label:'🔄 교체하기', cls:'btn b-switch', fn:function(){eDecide(true);}},
  ]);
}

function eDecide(sw){
  if(ePhase!==1) return;
  if(sw){
    var cands=[];
    for(var j=0;j<eN;j++){ if(j!==eChosen&&j!==eRev) cands.push(j); }
    eChosen=cands[ri(cands.length)];
  }
  ePhase=2;
  var won=eCars.indexOf(eChosen)>=0;
  if(sw){eWT++;if(won)eWW++;}else{eST++;if(won)eSW++;}
  eRender(); updateStats('e');
  showRes('e-res', won, (sw?'교체':'유지')+' 전략 — '+(won?'🎉 자동차를 얻었어요!':'🐐 아쉽게도 염소네요!'));
  var cl=eCars.map(function(c){return '문 '+(c+1);}).join(', ');
  setText('e-phase','자동차는 '+cl+'에 있었어요!');
  setActs('e-act',[{label:'🔁 다시 하기',cls:'btn b-reset',fn:eInit}]);
}

// ── Door factory ──────────────────────────────────────────────
// For basic tab: carRef = bCar (int). For ext tab: carRef = isCar?i:-1 (then img src patched later)
function makeDoor(i, carRef, open, chose, fin, w, h, fs, phase, isRevd, ph, tab){
  var isCar = (i===carRef);
  var wrap=document.createElement('div'); wrap.className='door-wrap';
  var door=document.createElement('div');
  var cls='door';
  if(open)  cls+=' opened';
  if(chose) cls+=' chosen';
  if(fin)   cls+=' final';
  if(ph>0)  cls+=' nohov';
  door.className=cls;
  door.style.width=w+'px'; door.style.height=h+'px';
  var knobSize=Math.max(6,Math.round(w*0.08));
  var knobRight=Math.max(6,Math.round(w*0.09));

  var badges='';
  if(ph===2){
    badges+='<div class="dbadge '+(isCar?'bc':'bg')+'">'+(isCar?'🚗':'🐐')+'</div>';
  } else if(isRevd && ph>=1){
    badges+='<div class="dbadge bg">🐐</div>';
  }
  if(fin) badges+='<div class="dbadge by" style="bottom:'+(ph===2?20:5)+'px">👉</div>';

  door.innerHTML='<div style="position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center;">'
    +'<span class="door-num" style="font-size:'+fs+'px">'+(i+1)+'</span>'
    +'<img class="door-img'+(open?' show':'')+'" src="'+(isCar?CAR:GOAT)+'" style="max-width:'+Math.round(w*.78)+'px;max-height:'+Math.round(h*.78)+'px;" />'
    +'<div class="door-knob" style="width:'+knobSize+'px;height:'+knobSize+'px;right:'+knobRight+'px;"></div>'
    +badges+'</div>';

  if(ph===0){
    (function(idx,t){
      door.onclick=function(){ if(t==='b') bChoose(idx); else eChoose(idx); };
    })(i,tab);
  }
  var lbl=document.createElement('div'); lbl.className='door-lbl';
  lbl.style.fontSize=Math.max(10,Math.min(12,Math.round(w*.085)+8))+'px';
  lbl.textContent='문 '+(i+1);
  wrap.appendChild(door); wrap.appendChild(lbl);
  return wrap;
}

// ── Slider ────────────────────────────────────────────────────
function onSlider(){
  var nEl=g('e-n'), kEl=g('e-k');
  eN=parseInt(nEl.value);
  kEl.max=eN-2;
  eK=Math.min(parseInt(kEl.value), eN-2);
  if(eK<1) eK=1;
  kEl.value=eK;
  setText('e-nv', eN);
  setText('e-kv', eK);
  updateExtTheory();
  stopAuto();
  gd.e.stay=[]; gd.e.sw=[];
  drawGraph('e');
  eInit();
}

function updateExtTheory(){
  var n=eN, k=eK;
  var sp = k/n;
  var wp = k*(n-1)/(n*(n-2));
  g('e-theory').innerHTML='📐 이론값 (문 '+n+'개, 자동차 '+k+'대) &nbsp;|&nbsp; '
    +'<strong>유지</strong> = '+k+'/'+n+' ≈ '+(sp*100).toFixed(1)+'%'
    +' &nbsp;&nbsp; '
    +'<strong>교체</strong> = '+k+'×'+(n-1)+'/('+n+'×'+(n-2)+') ≈ '+(wp*100).toFixed(1)+'%';
  g('e-sm-s').style.left=(sp*100).toFixed(2)+'%';
  g('e-sm-w').style.left=(wp*100).toFixed(2)+'%';
}

// ── Single game logic ─────────────────────────────────────────
function runOne(numD, numC, sw){
  var cars=[]; while(cars.length<numC){ var c=ri(numD); if(cars.indexOf(c)<0) cars.push(c); }
  var choice=ri(numD);
  var rev=-1;
  for(var j=0;j<numD;j++){ if(cars.indexOf(j)<0 && j!==choice){rev=j;break;} }
  if(rev<0) return cars.indexOf(choice)>=0;
  var fin=choice;
  if(sw){
    var cands=[];
    for(var j=0;j<numD;j++){ if(j!==choice&&j!==rev) cands.push(j); }
    fin=cands[ri(cands.length)];
  }
  return cars.indexOf(fin)>=0;
}

// ── Batch sim ─────────────────────────────────────────────────
function batch(tab, n, sw){
  var numD=tab==='b'?3:eN, numC=tab==='b'?1:eK;
  var wins=0;
  for(var i=0;i<n;i++){ if(runOne(numD,numC,sw)) wins++; }
  if(tab==='b'){
    if(sw){bWT+=n;bWW+=wins;}else{bST+=n;bSW+=wins;}
  } else {
    if(sw){eWT+=n;eWW+=wins;}else{eST+=n;eSW+=wins;}
  }
  updateStats(tab);
}

// ── Auto-sim ──────────────────────────────────────────────────
function startAuto(tab, sw){
  stopAuto();
  aTab=tab; aStrat=sw?'sw':'stay'; aW=0; aG=0;
  gd[tab][aStrat]=[];
  var sid=tab==='b'?'b-stop':'e-stop';
  g(sid).classList.add('show');
  atimer=setInterval(autoStep, AUTO_MS);
}

function autoStep(){
  var sw=aStrat==='sw';
  var numD=aTab==='b'?3:eN, numC=aTab==='b'?1:eK;
  var wins=0, cnt=0;
  for(var i=0;i<AUTO_BATCH&&aG<AUTO_MAX;i++){
    var won=runOne(numD,numC,sw);
    if(won){wins++;aW++;}
    aG++; cnt++;
    // record every game up to 100, then every 5
    if(aG<=100 || aG%5===0){
      gd[aTab][aStrat].push({n:aG, r:aW/aG});
    }
  }
  if(cnt===0){stopAuto();return;}
  if(aTab==='b'){
    if(sw){bWT+=cnt;bWW+=wins;}else{bST+=cnt;bSW+=wins;}
  } else {
    if(sw){eWT+=cnt;eWW+=wins;}else{eST+=cnt;eSW+=wins;}
  }
  updateStats(aTab);
  drawGraph(aTab);
  if(aG>=AUTO_MAX) stopAuto();
}

function stopAuto(){
  if(atimer){clearInterval(atimer);atimer=null;}
  ['b-stop','e-stop'].forEach(function(id){ g(id).classList.remove('show'); });
  aTab=null;
}

// ── Graph drawing ─────────────────────────────────────────────
function theory(tab){
  if(tab==='b') return {s:1/3, w:2/3};
  var n=eN,k=eK;
  return {s:k/n, w:k*(n-1)/(n*(n-2))};
}

function drawGraph(tab){
  var cvs=g(tab==='b'?'b-cvs':'e-cvs');
  if(!cvs) return;
  var dw=cvs.offsetWidth||cvs.parentElement.offsetWidth||290;
  cvs.width=dw;
  var W=cvs.width, H=cvs.height;
  var P={t:10,r:12,b:22,l:38};
  var pw=W-P.l-P.r, ph=H-P.t-P.b;
  var ctx=cvs.getContext('2d');
  ctx.clearRect(0,0,W,H);

  // bg + border
  ctx.fillStyle='#fafbff'; ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='#dee2e6'; ctx.lineWidth=1;
  ctx.strokeRect(P.l,P.t,pw,ph);

  // grid & y-labels
  ctx.fillStyle='#adb5bd'; ctx.font='9px sans-serif'; ctx.textAlign='right';
  for(var p=0;p<=4;p++){
    var y=P.t+ph*(1-p/4);
    ctx.strokeStyle='#eee'; ctx.lineWidth=.5;
    ctx.beginPath(); ctx.moveTo(P.l,y); ctx.lineTo(P.l+pw,y); ctx.stroke();
    ctx.fillStyle='#adb5bd'; ctx.fillText((p*25)+'%',P.l-3,y+3);
  }

  var th=theory(tab);

  // theoretical dashed lines
  function thline(rate, col){
    var y=P.t+ph*(1-rate);
    ctx.save(); ctx.strokeStyle=col; ctx.lineWidth=1.5;
    ctx.setLineDash([5,4]); ctx.globalAlpha=.7;
    ctx.beginPath(); ctx.moveTo(P.l,y); ctx.lineTo(P.l+pw,y); ctx.stroke();
    ctx.restore();
  }
  thline(th.s,'#74c0fc'); thline(th.w,'#ff8787');

  // x-axis label
  var data=gd[tab];
  var all=data.stay.concat(data.sw);
  var maxN=all.length>0?Math.max.apply(null,all.map(function(d){return d.n;})):100;
  maxN=Math.max(maxN,50);

  ctx.fillStyle='#adb5bd'; ctx.font='9px sans-serif'; ctx.textAlign='center';
  ctx.fillText('시뮬레이션 횟수 →', P.l+pw/2, H-3);

  // data line
  function dataline(arr, col){
    if(arr.length<2) return;
    ctx.save(); ctx.strokeStyle=col; ctx.lineWidth=2; ctx.lineJoin='round';
    ctx.beginPath();
    arr.forEach(function(pt,i){
      var x=P.l+(pt.n/maxN)*pw;
      var y=P.t+ph*(1-pt.r);
      if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    });
    ctx.stroke();
    // end dot + label
    var last=arr[arr.length-1];
    var lx=P.l+(last.n/maxN)*pw, ly=P.t+ph*(1-last.r);
    ctx.fillStyle=col;
    ctx.beginPath(); ctx.arc(lx,ly,4,0,Math.PI*2); ctx.fill();
    ctx.font='bold 10px sans-serif';
    ctx.textAlign=lx>P.l+pw*0.7?'right':'left';
    ctx.fillText((last.r*100).toFixed(1)+'%', lx+(lx>P.l+pw*0.7?-7:7), ly-6);
    ctx.restore();
  }
  dataline(data.stay,'#339af0');
  dataline(data.sw,  '#fa5252');
}

// ── Stats ─────────────────────────────────────────────────────
function updateStats(tab){
  if(tab==='b'){
    var sp=bST>0?bSW/bST*100:0, wp=bWT>0?bWW/bWT*100:0;
    g('b-bs').style.width=sp+'%'; g('b-bw').style.width=wp+'%';
    setText('b-ps',bSW+'승/'+bST+'회 ('+sp.toFixed(1)+'%)');
    setText('b-pw',bWW+'승/'+bWT+'회 ('+wp.toFixed(1)+'%)');
  } else {
    var sp=eST>0?eSW/eST*100:0, wp=eWT>0?eWW/eWT*100:0;
    g('e-bs').style.width=sp+'%'; g('e-bw').style.width=wp+'%';
    setText('e-ps',eSW+'승/'+eST+'회 ('+sp.toFixed(1)+'%)');
    setText('e-pw',eWW+'승/'+eWT+'회 ('+wp.toFixed(1)+'%)');
  }
}

// ── Reset ─────────────────────────────────────────────────────
function resetAll(tab){
  stopAuto();
  if(tab==='b'){
    bSW=bST=bWW=bWT=0; gd.b.stay=[]; gd.b.sw=[];
    updateStats('b'); drawGraph('b'); bInit();
  } else {
    eSW=eST=eWW=eWT=0; gd.e.stay=[]; gd.e.sw=[];
    updateStats('e'); drawGraph('e'); eInit();
  }
}

// ── Action helpers ────────────────────────────────────────────
function setActs(id, btns){
  var row=g(id); row.innerHTML='';
  btns.forEach(function(b){
    var btn=document.createElement('button');
    btn.className=b.cls; btn.textContent=b.label; btn.onclick=b.fn;
    row.appendChild(btn);
  });
}
function showRes(id,win,msg){
  var el=g(id); el.className='result '+(win?'win':'lose'); el.textContent=msg;
}
function hideRes(id){ g(id).className='result'; }

// ── Init ──────────────────────────────────────────────────────
bInit();
onSlider();  // sets eN,eK, calls eInit, updateExtTheory

setTimeout(function(){ drawGraph('b'); drawGraph('e'); }, 80);

// ── Quiz functions ────────────────────────────────────────────
var MCQ_EXPLAIN = {
  mcq1: {
    wrong: '아직 다시 생각해보세요.',
    right: '✓ 정답! 처음 선택한 문의 확률(1/3)은 몬티가 문을 연 후에도 변하지 않습니다. 남은 "다른 문들"에 걸려 있던 2/3 확률이 공개되지 않은 1개의 문에 집중됩니다.'
  },
  mcq2: {
    wrong: '아직 다시 생각해보세요.',
    right: '✓ 정답! 몬티가 자동차 위치를 모르고 우연히 염소를 공개한 경우, "자동차를 공개할 수도 있었는데 염소가 나온" 추가 정보가 생깁니다. 이 경우 교체 전략 승률은 1/2이 됩니다. 몬티의 지식이 핵심입니다!'
  },
  mcq3: {
    wrong: '아직 다시 생각해보세요.',
    right: '✓ 정답! 처음 선택의 확률은 1/100. 나머지 99/100이 교체할 1개의 문에 집중됩니다. 무조건 교체해야 합니다!'
  }
};

var mcqSelected = {};

function selectMCQ(id, idx){
  var opts = g(id).querySelectorAll('.mcq-opt');
  opts.forEach(function(o,i){ o.style.background = i===idx ? '#e7f5ff' : ''; o.style.borderColor = i===idx ? '#4dabf7' : '#e9ecef'; });
  mcqSelected[id] = idx;
}

function checkMCQ(id, correct, fbId){
  var sel = mcqSelected[id];
  if(sel === undefined){ g(fbId).textContent='먼저 선택지를 골라주세요!'; g(fbId).className='fb ng'; return; }
  var opts = g(id).querySelectorAll('.mcq-opt');
  opts.forEach(function(o,i){
    o.style.background=''; o.style.borderColor='';
    if(i===correct) o.classList.add('reveal-correct');
    else if(i===sel && i!==correct) o.classList.add('wrong');
  });
  var exp = MCQ_EXPLAIN[id];
  var fb = g(fbId);
  if(sel===correct){ fb.className='fb ok'; fb.textContent=exp.right; }
  else { fb.className='fb ng'; fb.textContent=exp.wrong; }
}

function chk(inputId, answers, fbId){
  var val = g(inputId).value.trim();
  var inp = g(inputId);
  var ok = answers.indexOf(val) >= 0;
  inp.classList.toggle('ok', ok);
  inp.classList.toggle('ng', !ok);
  if(!ok) setTimeout(function(){ inp.classList.remove('ng'); }, 500);
  var fb = g(fbId);
  fb.className = 'fb ' + (ok ? 'ok' : 'ng');
  fb.textContent = ok ? '✓ 정답!' : '✗ 다시 생각해보세요';
}

function chkPair(id1, ans1, id2, ans2, fbId){
  var v1=g(id1).value.trim(), v2=g(id2).value.trim();
  var ok = v1===ans1 && v2===ans2;
  [id1,id2].forEach(function(id,i){
    var a=i===0?ans1:ans2;
    var v=i===0?v1:v2;
    g(id).classList.toggle('ok', v===a);
    g(id).classList.toggle('ng', v!==a);
    if(v!==a) setTimeout(function(){ g(id).classList.remove('ng'); },500);
  });
  var fb=g(fbId);
  fb.className='fb '+(ok?'ok':'ng');
  fb.textContent=ok?'✓ 정답!':'✗ 두 칸 모두 확인해보세요';
}

// revealGroup(['inputId','answer','fbId',  'inputId2','answer2','fbId2', ...])
function revealGroup(arr){
  for(var i=0;i<arr.length;i+=3){
    var inp=g(arr[i]), ans=arr[i+1], fbEl=g(arr[i+2]);
    inp.value=ans; inp.classList.add('ok'); inp.classList.remove('ng');
    if(fbEl){ fbEl.className='fb ok'; fbEl.textContent='✓'; }
  }
}
</script>
</body>
</html>
""".replace("__GOAT__", goat_uri).replace("__CAR__", car_uri)

    components.html(html, height=1000, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
