# activities/probability_new/mini/simpsons_paradox_mini.py
"""
심프슨의 역설 미니활동
탭1: ⚾ 야구 투수 예제 – 직관 충격 체험 (단계적 공개)
탭2: 📚 다양한 예시 – 학과 입학률, 신약 임상 실험
탭3: 🎮 나만의 역설 만들기 챌린지 (인터랙티브 슬라이더)
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🔀 심프슨의 역설",
    "description": "부분에서 더 나은 것이 전체에서는 뒤처질 수 있다! 직관을 흔드는 심프슨의 역설을 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "심프슨의역설"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 심프슨의 역설**"},
    {
        "key": "역설발생조건",
        "label": "심프슨의 역설이 발생하는 핵심 이유는 무엇인가요? 야구 예제를 사용해 자신의 말로 설명해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "그룹별 표본 크기(경기 수)의 차이 때문에... 투수 B는 승률이 낮은 후반기에 더 많이 등판했기 때문에...",
    },
    {
        "key": "통계해석주의",
        "label": "이 역설은 통계 자료를 해석할 때 어떤 점을 조심해야 함을 알려주나요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "전체 통계만 보면 안 되고, 숨겨진 제3의 변수(예: 경기 시기, 환자 중증도)를...",
    },
    {
        "key": "다른사례",
        "label": "일상생활에서 심프슨의 역설이 나타날 수 있는 사례를 직접 생각해보세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) 두 학교의 수능 평균 점수 비교 시 학과 구성이 다를 때, 두 병원의 수술 성공률 비교 시...",
    },
    {
        "key": "역설만들기",
        "label": "탐구3(역설 만들기)에서 심프슨의 역설이 발생하도록 만들기 위한 조건은 무엇이었나요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "B가 유리한 그룹(높은 승률 구간)에 훨씬 더 많이 참여할 때...",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동으로 새롭게 알게 된 점",
        "type": "text_area",
        "height": 80,
    },
    {
        "key": "느낀점",
        "label": "💬 활동을 마친 후 느낀 점",
        "type": "text_area",
        "height": 80,
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1  – 야구 투수 예제 (단계적 공개)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB1 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:14px 12px 28px;min-height:100vh}
.hdr{text-align:center;padding:18px 16px 14px;background:linear-gradient(135deg,rgba(139,92,246,.18),rgba(109,40,217,.12));border:1px solid rgba(139,92,246,.4);border-radius:16px;margin-bottom:14px}
.hdr h1{font-size:1.35rem;color:#a78bfa;margin-bottom:5px}
.hdr p{font-size:.85rem;color:#94a3b8;line-height:1.5}
.card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:12px;padding:14px;margin-bottom:11px;transition:border-color .3s,background .3s}
.card.active{border-color:rgba(139,92,246,.5);background:rgba(139,92,246,.06)}
.card h2{font-size:.98rem;color:#a78bfa;margin-bottom:10px}
table{width:100%;border-collapse:collapse;font-size:.82rem;margin:7px 0}
th{background:rgba(139,92,246,.28);color:#c4b5fd;padding:6px 4px;text-align:center;font-size:.79rem}
td{padding:6px 4px;text-align:center;border-bottom:1px solid rgba(255,255,255,.06)}
.tr-total td{background:rgba(139,92,246,.13);font-weight:700}
.win{color:#4ade80;font-weight:700}.lose{color:#f87171;font-weight:700}
.bar-row{display:flex;align-items:center;gap:6px;margin-bottom:5px}
.bar-lbl{width:52px;font-size:.77rem;flex-shrink:0}
.bar-wrap{flex:1;background:rgba(255,255,255,.07);border-radius:5px;overflow:hidden}
.bar{height:22px;display:flex;align-items:center;justify-content:flex-end;padding-right:7px;font-size:.75rem;font-weight:700;color:#fff;border-radius:5px;transition:width .8s ease}
.bar-a{background:linear-gradient(90deg,#5b21b6,#7c3aed)}
.bar-b{background:linear-gradient(90deg,#0e7490,#0891b2)}
.btn{padding:8px 18px;border:none;border-radius:9px;font-size:.9rem;font-weight:700;cursor:pointer;transition:all .2s;margin:3px}
.btn-purple{background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff}
.btn-purple:hover{filter:brightness(1.15);transform:translateY(-1px)}
.btn-blue{background:linear-gradient(135deg,#0891b2,#0e7490);color:#fff}
.btn-blue:hover{filter:brightness(1.15);transform:translateY(-1px)}
.btn:disabled{opacity:.45;cursor:default;transform:none!important;filter:none!important}
.poll{text-align:center;padding:10px 0 4px}
.poll p{font-size:.98rem;font-weight:700;color:#e2e8f0;margin-bottom:9px}
.paradox-box{background:linear-gradient(135deg,rgba(234,179,8,.13),rgba(245,158,11,.06));border:2px solid rgba(234,179,8,.5);border-radius:14px;padding:14px;text-align:center;margin:11px 0}
.paradox-box h2{color:#fcd34d;font-size:1.15rem;margin-bottom:6px}
.paradox-box p{font-size:.85rem;color:#e2e8f0;line-height:1.55}
.res-row{display:flex;gap:10px;margin:11px 0;flex-wrap:wrap;align-items:center}
.res-card{flex:1;min-width:100px;border-radius:11px;padding:12px;text-align:center;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1)}
.res-card.winner{background:rgba(74,222,128,.1);border-color:rgba(74,222,128,.4)}
.res-card h3{font-size:.95rem;margin-bottom:4px}
.big-rate{font-size:1.65rem;font-weight:700;margin-bottom:3px}
.winner .big-rate{color:#4ade80}.loser .big-rate{color:#94a3b8}
.badge{display:inline-block;padding:2px 9px;border-radius:20px;font-size:.68rem;font-weight:700;margin-top:3px}
.badge-win{background:rgba(74,222,128,.2);color:#4ade80;border:1px solid rgba(74,222,128,.3)}
.badge-b{background:rgba(147,197,253,.15);color:#93c5fd;border:1px solid rgba(147,197,253,.25)}
.why{background:rgba(255,255,255,.03);border-left:3px solid #8b5cf6;border-radius:0 10px 10px 0;padding:11px 14px;margin:11px 0}
.why h3{color:#a78bfa;margin-bottom:7px;font-size:.92rem}
.why p,.why li{font-size:.82rem;color:#94a3b8;line-height:1.6}
.why ul{padding-left:14px;margin-top:5px}
.why strong{color:#e2e8f0}
.formula{background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.1);border-radius:9px;padding:11px;text-align:center;font-family:'Courier New',monospace;color:#fcd34d;margin:10px 0;font-size:.85rem;line-height:1.9}
.dots{display:flex;justify-content:center;gap:7px;margin:8px 0 12px}
.dot{width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,.18);transition:all .3s}
.dot.active{background:#8b5cf6;transform:scale(1.35)}
.dot.done{background:#4ade80}
.hidden{display:none!important}
.fade-in{animation:fi .4s ease}
@keyframes fi{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
.vs-mid{font-size:1.2rem;color:#64748b;flex-shrink:0}
.info-chip{background:rgba(0,0,0,.3);display:inline-flex;align-items:center;gap:7px;padding:6px 13px;border-radius:10px;margin-top:8px;font-size:.82rem}
</style>
</head>
<body>
<div class="hdr">
  <h1>⚾ 야구 투수 A vs B — 직관에 도전하기!</h1>
  <p>전반기에도, 후반기에도 투수 B가 더 높은 승률을 기록했습니다.<br>
  그렇다면 시즌 전체에서는 누가 더 잘한 투수일까요?</p>
</div>

<div class="dots">
  <div class="dot active" id="d0"></div>
  <div class="dot" id="d1"></div>
  <div class="dot" id="d2"></div>
  <div class="dot" id="d3"></div>
</div>

<!-- STEP 0: 전반기 -->
<div class="card active fade-in" id="s0">
  <h2>📊 Step 1 — 전반기 성적</h2>
  <table>
    <tr><th rowspan="2" style="width:18%"></th>
        <th colspan="3" style="border-right:1px solid rgba(139,92,246,.3)">투수 A</th>
        <th colspan="3">투수 B</th></tr>
    <tr><th>승</th><th>패</th><th style="border-right:1px solid rgba(139,92,246,.3)">승률</th>
        <th>승</th><th>패</th><th>승률</th></tr>
    <tr><td>전반기</td>
        <td>5</td><td>2</td><td class="lose" style="border-right:1px solid rgba(139,92,246,.15)">71.43%</td>
        <td>3</td><td>1</td><td class="win">75.00%</td></tr>
  </table>
  <div style="margin-top:10px">
    <div class="bar-row">
      <span class="bar-lbl" style="color:#a78bfa">투수 A</span>
      <div class="bar-wrap"><div class="bar bar-a" style="width:71.43%">71.43%</div></div>
    </div>
    <div class="bar-row">
      <span class="bar-lbl" style="color:#93c5fd">투수 B</span>
      <div class="bar-wrap"><div class="bar bar-b" style="width:75%">75.00%</div></div>
    </div>
  </div>
  <div style="text-align:center">
    <div class="info-chip">
      <span>전반기:</span>
      <strong style="color:#93c5fd">투수 B 우세</strong>
      <span style="color:#64748b">(+3.57%p)</span>
    </div>
  </div>
  <div style="text-align:center;margin-top:12px">
    <button class="btn btn-purple" id="btn0" onclick="nextStep(0)">후반기 성적 보기 →</button>
  </div>
</div>

<!-- STEP 1: 후반기 -->
<div class="card hidden" id="s1">
  <h2>📊 Step 2 — 후반기 성적</h2>
  <table>
    <tr><th rowspan="2" style="width:18%"></th>
        <th colspan="3" style="border-right:1px solid rgba(139,92,246,.3)">투수 A</th>
        <th colspan="3">투수 B</th></tr>
    <tr><th>승</th><th>패</th><th style="border-right:1px solid rgba(139,92,246,.3)">승률</th>
        <th>승</th><th>패</th><th>승률</th></tr>
    <tr><td>전반기</td>
        <td>5</td><td>2</td><td class="lose" style="border-right:1px solid rgba(139,92,246,.15)">71.43%</td>
        <td>3</td><td>1</td><td class="win">75.00%</td></tr>
    <tr><td>후반기</td>
        <td>4</td><td>3</td><td class="lose" style="border-right:1px solid rgba(139,92,246,.15)">57.14%</td>
        <td>7</td><td>5</td><td class="win">58.33%</td></tr>
  </table>
  <div style="margin-top:10px">
    <div style="font-size:.77rem;color:#64748b;margin-bottom:5px">후반기 승률 비교</div>
    <div class="bar-row">
      <span class="bar-lbl" style="color:#a78bfa">투수 A</span>
      <div class="bar-wrap"><div class="bar bar-a" style="width:57.14%">57.14%</div></div>
    </div>
    <div class="bar-row">
      <span class="bar-lbl" style="color:#93c5fd">투수 B</span>
      <div class="bar-wrap"><div class="bar bar-b" style="width:58.33%">58.33%</div></div>
    </div>
  </div>
  <div style="text-align:center">
    <div class="info-chip">
      <span>후반기도:</span>
      <strong style="color:#93c5fd">투수 B 우세</strong>
      <span style="color:#64748b">(+1.19%p)</span>
    </div>
  </div>
  <div class="poll">
    <p>🤔 그렇다면 시즌 전체에서는 누가 더 높은 승률일까요?</p>
    <button class="btn btn-purple" onclick="castVote('A')">투수 A가 더 높을 것 같다!</button>
    <button class="btn btn-blue" onclick="castVote('B')">투수 B가 더 높을 것 같다!</button>
  </div>
</div>

<!-- STEP 2: 예측 후 대기 -->
<div class="card hidden" id="s2">
  <div style="text-align:center;padding:8px 0">
    <div style="font-size:1rem;color:#e2e8f0;margin-bottom:6px">
      여러분의 예측: <strong id="vote-txt" style="color:#fcd34d">투수 ?</strong>가 전체에서 더 높다!
    </div>
    <div style="font-size:.84rem;color:#94a3b8;margin-bottom:12px">
      과연 예측이 맞을까요? 전체 시즌 성적을 확인해봅시다!
    </div>
    <button class="btn btn-purple" id="btn2" onclick="nextStep(2)" style="font-size:1rem;padding:11px 26px">
      🎬 전체 시즌 결과 공개!
    </button>
  </div>
</div>

<!-- STEP 3: 결과 공개 -->
<div class="card hidden" id="s3">
  <h2>🎯 Step 4 — 전체 시즌 최종 성적</h2>
  <table>
    <tr><th rowspan="2" style="width:18%"></th>
        <th colspan="3" style="border-right:1px solid rgba(139,92,246,.3)">투수 A</th>
        <th colspan="3">투수 B</th></tr>
    <tr><th>승</th><th>패</th><th style="border-right:1px solid rgba(139,92,246,.3)">승률</th>
        <th>승</th><th>패</th><th>승률</th></tr>
    <tr><td>전반기</td>
        <td>5</td><td>2</td><td class="lose" style="border-right:1px solid rgba(139,92,246,.15)">71.43%</td>
        <td>3</td><td>1</td><td class="win">75.00%</td></tr>
    <tr><td>후반기</td>
        <td>4</td><td>3</td><td class="lose" style="border-right:1px solid rgba(139,92,246,.15)">57.14%</td>
        <td>7</td><td>5</td><td class="win">58.33%</td></tr>
    <tr class="tr-total"><td>시즌 전체</td>
        <td>9</td><td>5</td><td class="win" style="border-right:1px solid rgba(139,92,246,.15)">64.29%</td>
        <td>10</td><td>6</td><td class="lose">62.50%</td></tr>
  </table>

  <div class="paradox-box">
    <h2>😱 반전! 시즌 전체에서는 <span style="color:#4ade80">투수 A</span>가 더 높다!</h2>
    <p>전반기·후반기 모두 B가 우세했는데,<br>
    시즌 전체에서는 A의 승률이 더 높습니다! (64.29% &gt; 62.50%)</p>
  </div>

  <div class="res-row">
    <div class="res-card winner">
      <h3 style="color:#4ade80">투수 A</h3>
      <div class="big-rate">64.29%</div>
      <div style="font-size:.73rem;color:#64748b">9승 5패</div>
      <span class="badge badge-win">🏆 전체 시즌 1위</span>
    </div>
    <div class="vs-mid">vs</div>
    <div class="res-card loser">
      <h3 style="color:#93c5fd">투수 B</h3>
      <div class="big-rate">62.50%</div>
      <div style="font-size:.73rem;color:#64748b">10승 6패</div>
      <span class="badge badge-b">전반기·후반기 1위</span>
    </div>
  </div>

  <div class="why">
    <h3>💡 왜 이런 역설이 생길까요? — 가중치의 마법</h3>
    <p>핵심은 <strong>그룹별 경기 수(가중치)가 서로 다르기 때문</strong>입니다.</p>
    <ul>
      <li>투수 A: <span style="color:#a78bfa">전반기 7경기</span>(고승률 구간) + 후반기 7경기 → 균등하게 분배</li>
      <li>투수 B: 전반기 4경기 + <span style="color:#93c5fd">후반기 12경기</span>(저승률 구간) → 저승률 구간 집중</li>
    </ul>
    <p style="margin-top:7px">B는 승률이 낮은 후반기에 훨씬 많이 등판했기 때문에,<br>
    전체 승률이 끌어내려졌습니다. 이것이 <strong style="color:#fcd34d">심프슨의 역설</strong>입니다!</p>
  </div>

  <div class="formula">
    b/a &gt; d/c &nbsp;&nbsp; 이고 &nbsp;&nbsp; f/e &gt; h/g &nbsp;&nbsp; 이어도<br>
    <span style="color:#f87171">(b+f)/(a+e) &gt; (d+h)/(c+g) 가 항상 성립하지는 않는다!</span>
  </div>

  <div style="background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.28);border-radius:10px;padding:11px 13px;font-size:.82rem;line-height:1.6">
    <strong style="color:#a78bfa">심프슨의 역설 (Simpson's Paradox)</strong><br>
    <span style="color:#94a3b8">1951년 영국 통계학자 에드워드 심프슨이 논문으로 정리한 역설.<br>
    각 부분 집단에서 성립하는 통계적 경향이 전체 집단에서는 역전될 수 있는 현상입니다.</span>
  </div>
</div>

<script>
function nextStep(from) {
  var s = ['s0','s1','s2','s3'];
  var d = ['d0','d1','d2','d3'];
  var to = from + 1;
  document.getElementById(s[from]).classList.remove('active');
  document.getElementById(d[from]).classList.remove('active');
  document.getElementById(d[from]).classList.add('done');
  var next = document.getElementById(s[to]);
  next.classList.remove('hidden');
  next.classList.add('fade-in','active');
  document.getElementById(d[to]).classList.add('active');
  if(from===0) document.getElementById('btn0').disabled=true;
  if(from===2) document.getElementById('btn2').disabled=true;
  setTimeout(function(){next.scrollIntoView({behavior:'smooth',block:'nearest'})},80);
}
function castVote(c) {
  document.getElementById('vote-txt').textContent = '투수 '+c;
  nextStep(1);
  document.querySelectorAll('#s1 .btn').forEach(function(b){b.disabled=true});
}
function reportHeight(){
  var h = document.documentElement.scrollHeight;
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
var _ro = new ResizeObserver(reportHeight);
_ro.observe(document.body);
reportHeight();
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2  – 다양한 예시 (학과 입학률 + 신약 임상 실험)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB2 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:14px 12px 28px;min-height:100vh}
.sec-hdr{text-align:center;padding:14px 14px 11px;border-radius:14px;margin-bottom:13px}
.sec-hdr.purple{background:linear-gradient(135deg,rgba(139,92,246,.18),rgba(109,40,217,.1));border:1px solid rgba(139,92,246,.38)}
.sec-hdr.teal{background:linear-gradient(135deg,rgba(20,184,166,.16),rgba(13,148,136,.1));border:1px solid rgba(20,184,166,.38)}
.sec-hdr h2{font-size:1.1rem;margin-bottom:4px}
.sec-hdr.purple h2{color:#a78bfa}
.sec-hdr.teal h2{color:#2dd4bf}
.sec-hdr p{font-size:.82rem;color:#94a3b8;line-height:1.45}
table{width:100%;border-collapse:collapse;font-size:.81rem;margin:7px 0}
th{padding:6px 4px;text-align:center;font-size:.78rem}
.th-purple{background:rgba(139,92,246,.28);color:#c4b5fd}
.th-teal{background:rgba(20,184,166,.22);color:#5eead4}
td{padding:6px 4px;text-align:center;border-bottom:1px solid rgba(255,255,255,.06)}
.tr-total td{font-weight:700}
.tr-total.purple-total td{background:rgba(139,92,246,.12)}
.tr-total.teal-total td{background:rgba(20,184,166,.1)}
.win{color:#4ade80;font-weight:700}.lose{color:#f87171;font-weight:700}
.bar-row{display:flex;align-items:center;gap:6px;margin-bottom:5px}
.bar-lbl{width:55px;font-size:.77rem;flex-shrink:0}
.bar-wrap{flex:1;background:rgba(255,255,255,.07);border-radius:5px;overflow:hidden}
.bar{height:22px;display:flex;align-items:center;justify-content:flex-end;padding-right:7px;font-size:.75rem;font-weight:700;color:#fff;border-radius:5px}
.bar-m{background:linear-gradient(90deg,#5b21b6,#7c3aed)}
.bar-f{background:linear-gradient(90deg,#be185d,#db2777)}
.bar-a{background:linear-gradient(90deg,#0e7490,#0891b2)}
.bar-b{background:linear-gradient(90deg,#065f46,#059669)}
.btn{padding:8px 18px;border:none;border-radius:9px;font-size:.88rem;font-weight:700;cursor:pointer;transition:all .2s;margin:3px}
.btn-purple{background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff}
.btn-teal{background:linear-gradient(135deg,#0d9488,#0f766e);color:#fff}
.btn:hover{filter:brightness(1.14);transform:translateY(-1px)}
.btn:disabled{opacity:.4;cursor:default;transform:none!important;filter:none!important}
.reveal-box{background:rgba(0,0,0,.25);border:1px dashed rgba(255,255,255,.15);border-radius:10px;padding:11px;margin:9px 0;text-align:center;min-height:60px}
.reveal-box p{font-size:.9rem;color:#64748b}
.paradox-box{border-radius:13px;padding:13px;text-align:center;margin:10px 0}
.paradox-box.purple{background:linear-gradient(135deg,rgba(234,179,8,.12),rgba(245,158,11,.06));border:2px solid rgba(234,179,8,.5)}
.paradox-box.teal{background:linear-gradient(135deg,rgba(52,211,153,.1),rgba(16,185,129,.05));border:2px solid rgba(52,211,153,.45)}
.paradox-box h3{font-size:1.05rem;margin-bottom:5px}
.paradox-box.purple h3{color:#fcd34d}
.paradox-box.teal h3{color:#34d399}
.paradox-box p{font-size:.83rem;color:#e2e8f0;line-height:1.5}
.why{border-left:3px solid;border-radius:0 10px 10px 0;padding:10px 13px;margin:10px 0}
.why.purple{background:rgba(139,92,246,.05);border-left-color:#8b5cf6}
.why.teal{background:rgba(20,184,166,.05);border-left-color:#14b8a6}
.why h4{font-size:.88rem;margin-bottom:6px}
.why.purple h4{color:#a78bfa}
.why.teal h4{color:#2dd4bf}
.why p,.why li{font-size:.8rem;color:#94a3b8;line-height:1.55}
.why ul{padding-left:14px;margin-top:4px}
.why strong{color:#e2e8f0}
.divider{border:none;border-top:1px solid rgba(255,255,255,.08);margin:18px 0}
.hidden{display:none!important}
.fade-in{animation:fi .4s ease}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.sub-lbl{font-size:.76rem;color:#64748b;margin-top:2px}
</style>
</head>
<body>

<!-- ── 예시 1: 학과 입학률 ── -->
<div class="sec-hdr purple">
  <h2>🎓 예시 1 — 학과별 입학률</h2>
  <p>1973년 캘리포니아 대학 입학 데이터에서 발견된 역설.<br>
  학과별로 보면 여학생 입학률이 더 높은데, 전체를 보면?</p>
</div>

<table>
  <tr><th rowspan="2" style="width:18%" class="th-purple"></th>
      <th colspan="3" class="th-purple" style="border-right:1px solid rgba(139,92,246,.3)">남학생</th>
      <th colspan="3" class="th-purple">여학생</th></tr>
  <tr><th class="th-purple">합격</th><th class="th-purple">불합격</th>
      <th class="th-purple" style="border-right:1px solid rgba(139,92,246,.3)">합격률</th>
      <th class="th-purple">합격</th><th class="th-purple">불합격</th>
      <th class="th-purple">합격률</th></tr>
  <tr><td>학과 A</td>
      <td>10</td><td>20</td><td class="lose" style="border-right:1px solid rgba(139,92,246,.1)">33.33%</td>
      <td>20</td><td>30</td><td class="win">40.00%</td></tr>
  <tr><td>학과 B</td>
      <td>50</td><td>20</td><td class="lose" style="border-right:1px solid rgba(139,92,246,.1)">71.43%</td>
      <td>30</td><td>10</td><td class="win">75.00%</td></tr>
</table>

<div style="margin:8px 0">
  <div class="bar-row">
    <span class="bar-lbl" style="color:#a78bfa">남 (학A)</span>
    <div class="bar-wrap"><div class="bar bar-m" style="width:33.33%">33.33%</div></div>
  </div>
  <div class="bar-row">
    <span class="bar-lbl" style="color:#db2777">여 (학A)</span>
    <div class="bar-wrap"><div class="bar bar-f" style="width:40%">40.00%</div></div>
  </div>
  <div class="bar-row">
    <span class="bar-lbl" style="color:#a78bfa">남 (학B)</span>
    <div class="bar-wrap"><div class="bar bar-m" style="width:71.43%">71.43%</div></div>
  </div>
  <div class="bar-row">
    <span class="bar-lbl" style="color:#db2777">여 (학B)</span>
    <div class="bar-wrap"><div class="bar bar-f" style="width:75%">75.00%</div></div>
  </div>
</div>
<p style="text-align:center;font-size:.83rem;color:#94a3b8">학과 A에서도, 학과 B에서도 <strong style="color:#db2777">여학생 합격률</strong>이 더 높습니다.</p>

<div id="reveal1-prompt" style="text-align:center;margin:11px 0">
  <p style="font-size:.95rem;font-weight:700;margin-bottom:8px">🤔 그렇다면 전체 합격률은 누가 더 높을까요?</p>
  <button class="btn btn-purple" onclick="showReveal1()">전체 결과 공개!</button>
</div>
<div id="reveal1" class="hidden">
  <table>
    <tr><th rowspan="2" style="width:18%" class="th-purple"></th>
        <th colspan="3" class="th-purple" style="border-right:1px solid rgba(139,92,246,.3)">남학생</th>
        <th colspan="3" class="th-purple">여학생</th></tr>
    <tr><th class="th-purple">합격</th><th class="th-purple">불합격</th>
        <th class="th-purple" style="border-right:1px solid rgba(139,92,246,.3)">합격률</th>
        <th class="th-purple">합격</th><th class="th-purple">불합격</th>
        <th class="th-purple">합격률</th></tr>
    <tr class="tr-total purple-total"><td>전체</td>
        <td>60</td><td>40</td><td class="win" style="border-right:1px solid rgba(139,92,246,.15)">60.00%</td>
        <td>50</td><td>40</td><td class="lose">55.56%</td></tr>
  </table>
  <div class="paradox-box purple fade-in" style="margin-top:10px">
    <h3>😱 전체에서는 남학생 합격률이 더 높다! (60% &gt; 55.56%)</h3>
    <p>두 학과 모두에서 여학생이 앞섰는데, 전체 합계에서는 역전!</p>
  </div>
  <div class="why purple">
    <h4>💡 왜 역전될까요?</h4>
    <ul>
      <li>여학생의 <strong>90명 중 50명(56%)</strong>이 합격률이 낮은 학과 A에 지원</li>
      <li>남학생의 <strong>100명 중 70명(70%)</strong>이 합격률이 높은 학과 B에 지원</li>
      <li>여학생이 더 경쟁이 치열한 학과에 몰렸기 때문에 전체 합격률이 낮아진 것!</li>
    </ul>
    <p style="margin-top:6px">실제로 <strong>학과 내 차별은 없지만</strong>, 전체 통계만 보면 차별처럼 보일 수 있습니다.</p>
  </div>
</div>

<hr class="divider">

<!-- ── 예시 2: 신약 임상 실험 ── -->
<div class="sec-hdr teal">
  <h2>💊 예시 2 — 신약 임상 실험</h2>
  <p>신약 A와 기존 치료법 B의 치료 성공률을 비교합니다.<br>
  (실제 1986년 신장 결석 치료 연구 데이터를 단순화한 예시)</p>
</div>

<table>
  <tr><th rowspan="2" style="width:20%" class="th-teal"></th>
      <th colspan="3" class="th-teal" style="border-right:1px solid rgba(20,184,166,.3)">신약 A</th>
      <th colspan="3" class="th-teal">기존 치료 B</th></tr>
  <tr><th class="th-teal">성공</th><th class="th-teal">실패</th>
      <th class="th-teal" style="border-right:1px solid rgba(20,184,166,.3)">성공률</th>
      <th class="th-teal">성공</th><th class="th-teal">실패</th>
      <th class="th-teal">성공률</th></tr>
  <tr><td>경증 환자<div class="sub-lbl">소결석</div></td>
      <td>81</td><td>6</td><td class="win" style="border-right:1px solid rgba(20,184,166,.1)">93.1%</td>
      <td>234</td><td>36</td><td class="lose">86.7%</td></tr>
  <tr><td>중증 환자<div class="sub-lbl">대결석</div></td>
      <td>192</td><td>71</td><td class="win" style="border-right:1px solid rgba(20,184,166,.1)">73.0%</td>
      <td>55</td><td>25</td><td class="lose">68.8%</td></tr>
</table>

<div style="margin:8px 0">
  <div class="bar-row">
    <span class="bar-lbl" style="color:#0891b2">A (경증)</span>
    <div class="bar-wrap"><div class="bar bar-a" style="width:93.1%">93.1%</div></div>
  </div>
  <div class="bar-row">
    <span class="bar-lbl" style="color:#059669">B (경증)</span>
    <div class="bar-wrap"><div class="bar bar-b" style="width:86.7%">86.7%</div></div>
  </div>
  <div class="bar-row">
    <span class="bar-lbl" style="color:#0891b2">A (중증)</span>
    <div class="bar-wrap"><div class="bar bar-a" style="width:73%">73.0%</div></div>
  </div>
  <div class="bar-row">
    <span class="bar-lbl" style="color:#059669">B (중증)</span>
    <div class="bar-wrap"><div class="bar bar-b" style="width:68.8%">68.8%</div></div>
  </div>
</div>
<p style="text-align:center;font-size:.83rem;color:#94a3b8">경증·중증 모두에서 <strong style="color:#2dd4bf">신약 A</strong>의 성공률이 더 높습니다.</p>

<div id="reveal2-prompt" style="text-align:center;margin:11px 0">
  <p style="font-size:.95rem;font-weight:700;margin-bottom:8px">🤔 그렇다면 전체 성공률은 어느 치료법이 더 높을까요?</p>
  <button class="btn btn-teal" onclick="showReveal2()">전체 결과 공개!</button>
</div>
<div id="reveal2" class="hidden">
  <table>
    <tr><th rowspan="2" style="width:20%" class="th-teal"></th>
        <th colspan="3" class="th-teal" style="border-right:1px solid rgba(20,184,166,.3)">신약 A</th>
        <th colspan="3" class="th-teal">기존 치료 B</th></tr>
    <tr><th class="th-teal">성공</th><th class="th-teal">실패</th>
        <th class="th-teal" style="border-right:1px solid rgba(20,184,166,.3)">성공률</th>
        <th class="th-teal">성공</th><th class="th-teal">실패</th>
        <th class="th-teal">성공률</th></tr>
    <tr class="tr-total teal-total"><td>전체</td>
        <td>273</td><td>77</td><td class="lose" style="border-right:1px solid rgba(20,184,166,.1)">78.0%</td>
        <td>289</td><td>61</td><td class="win">82.6%</td></tr>
  </table>
  <div class="paradox-box teal fade-in" style="margin-top:10px">
    <h3>😱 전체에서는 기존 치료 B의 성공률이 더 높다! (82.6% &gt; 78.0%)</h3>
    <p>경증·중증 모두에서 A가 앞섰는데, 전체 합계에서는 역전!</p>
  </div>
  <div class="why teal">
    <h4>💡 왜 역전될까요?</h4>
    <ul>
      <li>신약 A: <strong>350명 중 263명(75%)</strong>이 치료가 어려운 중증 환자</li>
      <li>기존치료 B: <strong>350명 중 270명(77%)</strong>이 치료가 쉬운 경증 환자</li>
      <li>의사들이 더 어려운 케이스에 신약을 쓰는 경향이 있어서 생긴 현상!</li>
      <li>중증 환자 비율이 높은 신약 A의 전체 성공률이 자연히 낮아진 것</li>
    </ul>
    <p style="margin-top:6px">이 경우 <strong>"제3의 변수"</strong>(환자 중증도)를 무시하면 신약이 더 나쁜 것처럼 보입니다.</p>
  </div>
</div>

<script>
function showReveal1(){
  document.getElementById('reveal1').classList.remove('hidden');
  document.getElementById('reveal1').classList.add('fade-in');
  document.getElementById('reveal1-prompt').querySelector('button').disabled=true;
  setTimeout(function(){document.getElementById('reveal1').scrollIntoView({behavior:'smooth',block:'nearest'})},80);
}
function showReveal2(){
  document.getElementById('reveal2').classList.remove('hidden');
  document.getElementById('reveal2').classList.add('fade-in');
  document.getElementById('reveal2-prompt').querySelector('button').disabled=true;
  setTimeout(function(){document.getElementById('reveal2').scrollIntoView({behavior:'smooth',block:'nearest'})},80);
}
function reportHeight(){
  var h = document.documentElement.scrollHeight;
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
var _ro = new ResizeObserver(reportHeight);
_ro.observe(document.body);
reportHeight();
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3  – 나만의 역설 만들기 (인터랙티브)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB3 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:14px 12px 28px;min-height:100vh}
.hdr{text-align:center;padding:16px 14px 12px;background:linear-gradient(135deg,rgba(234,179,8,.14),rgba(245,158,11,.07));border:1px solid rgba(234,179,8,.42);border-radius:16px;margin-bottom:14px}
.hdr h1{font-size:1.25rem;color:#fcd34d;margin-bottom:4px}
.hdr p{font-size:.82rem;color:#94a3b8;line-height:1.45}
.card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:12px;padding:13px;margin-bottom:11px}
.card h2{font-size:.95rem;margin-bottom:10px;color:#a78bfa}
/* 기본 설정 그리드 */
.setup-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:6px}
.group-box{border-radius:10px;padding:10px;text-align:center}
.group-box.g1{background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.3)}
.group-box.g2{background:rgba(244,63,94,.08);border:1px solid rgba(244,63,94,.28)}
.group-box h3{font-size:.88rem;margin-bottom:7px}
.group-box.g1 h3{color:#a78bfa}
.group-box.g2 h3{color:#fb7185}
.rate-line{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;font-size:.8rem}
.rate-chip{padding:3px 9px;border-radius:8px;font-weight:700;font-size:.82rem}
.chip-a{background:rgba(99,102,241,.25);color:#a5b4fc}
.chip-b{background:rgba(34,197,94,.18);color:#86efac}
.chip-win{background:rgba(74,222,128,.18);color:#4ade80;font-size:.72rem;border-radius:20px;padding:2px 8px}
/* 슬라이더 */
.slider-section h2{color:#fcd34d}
.slider-wrap{margin-bottom:14px}
.slider-wrap label{display:block;font-size:.85rem;color:#e2e8f0;margin-bottom:5px}
.slider-row{display:flex;align-items:center;gap:8px}
.slider-row input[type=range]{flex:1;accent-color:#8b5cf6;height:6px;cursor:pointer}
.slider-val{min-width:38px;text-align:right;font-weight:700;font-size:.9rem}
.ratio-vis{display:flex;height:18px;border-radius:5px;overflow:hidden;margin-top:5px}
.ratio-g1{background:linear-gradient(90deg,#5b21b6,#7c3aed);transition:width .3s}
.ratio-g2{background:linear-gradient(90deg,#9f1239,#e11d48);flex:1}
.ratio-txt{display:flex;justify-content:space-between;font-size:.72rem;color:#64748b;margin-top:3px}
/* 결과 */
.result-section h2{color:#4ade80}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}
.res-box{border-radius:11px;padding:12px;text-align:center;border:2px solid transparent;transition:all .4s}
.res-box h3{font-size:.9rem;margin-bottom:5px}
.res-box.char-a h3{color:#a5b4fc}
.res-box.char-b h3{color:#86efac}
.res-big{font-size:1.6rem;font-weight:700;margin-bottom:3px;transition:color .4s}
.detail-bars{margin:8px 0}
.db-row{display:flex;align-items:center;gap:5px;margin-bottom:4px;font-size:.72rem}
.db-lbl{width:42px;flex-shrink:0;color:#64748b}
.db-wrap{flex:1;background:rgba(255,255,255,.07);border-radius:4px;overflow:hidden}
.db-bar{height:16px;border-radius:4px;display:flex;align-items:center;justify-content:flex-end;padding-right:5px;font-size:.68rem;font-weight:700;color:#fff;transition:width .5s}
.verdict-banner{border-radius:13px;padding:12px;text-align:center;transition:all .4s;margin-top:2px}
.verdict-banner.normal{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1)}
.verdict-banner.paradox{background:linear-gradient(135deg,rgba(234,179,8,.15),rgba(245,158,11,.08));border:2px solid rgba(234,179,8,.55);animation:pulse .8s ease 3}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.015)}}
.verdict-banner h3{font-size:1rem;margin-bottom:4px}
.verdict-banner.normal h3{color:#94a3b8}
.verdict-banner.paradox h3{color:#fcd34d}
.verdict-banner p{font-size:.8rem;line-height:1.5}
.verdict-banner.normal p{color:#64748b}
.verdict-banner.paradox p{color:#e2e8f0}
/* 챌린지 */
.challenge-box{background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.28);border-radius:12px;padding:12px;margin-bottom:11px}
.challenge-box h2{color:#a78bfa;margin-bottom:6px;font-size:.95rem}
.challenge-box p{font-size:.8rem;color:#94a3b8;line-height:1.55}
.challenge-status{margin-top:8px;padding:7px 11px;border-radius:8px;font-size:.83rem;font-weight:700;text-align:center}
.status-locked{background:rgba(255,255,255,.05);color:#64748b}
.status-done{background:rgba(74,222,128,.15);color:#4ade80;border:1px solid rgba(74,222,128,.3)}
/* 힌트 */
.hint-box{background:rgba(255,255,255,.03);border-left:3px solid #fcd34d;border-radius:0 9px 9px 0;padding:9px 12px;font-size:.79rem;color:#94a3b8;line-height:1.55;margin-top:9px}
.hint-box strong{color:#fcd34d}
.tbl-mini{width:100%;font-size:.78rem;border-collapse:collapse;margin:7px 0}
.tbl-mini th{background:rgba(99,102,241,.2);color:#a5b4fc;padding:5px 4px;text-align:center}
.tbl-mini td{padding:5px 4px;text-align:center;border-bottom:1px solid rgba(255,255,255,.06)}
.tbl-mini .tr-total td{background:rgba(99,102,241,.1);font-weight:700}
.tw{color:#4ade80;font-weight:700}.tl{color:#f87171;font-weight:700}
</style>
</head>
<body>
<div class="hdr">
  <h1>🎮 나만의 역설 만들기 챌린지</h1>
  <p>두 게임 캐릭터의 던전 참여 비율을 조절해 심프슨의 역설을 만들어보세요!<br>
  <strong style="color:#fcd34d">목표:</strong> 두 그룹 모두에서 A가 이기지만, 전체에서는 B가 이기도록!</p>
</div>

<!-- 기본 설정 (고정) -->
<div class="card">
  <h2>⚙️ 기본 설정 (고정값)</h2>
  <p style="font-size:.8rem;color:#64748b;margin-bottom:9px">두 그룹의 승률은 고정되어 있습니다. 캐릭터별 그룹 참여 비율만 바꿀 수 있어요.</p>
  <div class="setup-grid">
    <div class="group-box g1">
      <h3>⚔️ 쉬운 던전 (그룹 1)</h3>
      <div class="rate-line">
        <span class="rate-chip chip-a">캐릭터 A</span>
        <span style="font-weight:700;color:#a5b4fc">90%</span>
      </div>
      <div class="rate-line">
        <span class="rate-chip chip-b">캐릭터 B</span>
        <span style="font-weight:700;color:#86efac">80%</span>
      </div>
      <span class="chip-win">→ A 항상 우세</span>
    </div>
    <div class="group-box g2">
      <h3>🐉 어려운 던전 (그룹 2)</h3>
      <div class="rate-line">
        <span class="rate-chip chip-a">캐릭터 A</span>
        <span style="font-weight:700;color:#a5b4fc">40%</span>
      </div>
      <div class="rate-line">
        <span class="rate-chip chip-b">캐릭터 B</span>
        <span style="font-weight:700;color:#86efac">30%</span>
      </div>
      <span class="chip-win">→ A 항상 우세</span>
    </div>
  </div>
</div>

<!-- 슬라이더 -->
<div class="card slider-section">
  <h2>🎚️ 참여 비율 조절 (여기서 바꿔보세요!)</h2>
  <p style="font-size:.79rem;color:#64748b;margin-bottom:11px">각 캐릭터가 전체 전투 중 쉬운 던전에 참여하는 비율</p>

  <div class="slider-wrap">
    <label>🟣 캐릭터 A — 쉬운 던전 참여 비율: <span id="pA-lbl" style="color:#a5b4fc;font-weight:700">50%</span></label>
    <div class="slider-row">
      <span style="font-size:.75rem;color:#64748b">0%</span>
      <input type="range" id="slA" min="0" max="100" value="50" oninput="update()">
      <span style="font-size:.75rem;color:#64748b">100%</span>
    </div>
    <div class="ratio-vis">
      <div class="ratio-g1" id="rv-a1" style="width:50%"></div>
      <div class="ratio-g2" id="rv-a2"></div>
    </div>
    <div class="ratio-txt">
      <span>⚔️ 쉬운 던전 <span id="pA-g1">50%</span></span>
      <span>🐉 어려운 던전 <span id="pA-g2">50%</span></span>
    </div>
  </div>

  <div class="slider-wrap">
    <label>🟢 캐릭터 B — 쉬운 던전 참여 비율: <span id="pB-lbl" style="color:#86efac;font-weight:700">50%</span></label>
    <div class="slider-row">
      <span style="font-size:.75rem;color:#64748b">0%</span>
      <input type="range" id="slB" min="0" max="100" value="50" oninput="update()">
      <span style="font-size:.75rem;color:#64748b">100%</span>
    </div>
    <div class="ratio-vis">
      <div class="ratio-g1" id="rv-b1" style="width:50%"></div>
      <div class="ratio-g2" id="rv-b2"></div>
    </div>
    <div class="ratio-txt">
      <span>⚔️ 쉬운 던전 <span id="pB-g1">50%</span></span>
      <span>🐉 어려운 던전 <span id="pB-g2">50%</span></span>
    </div>
  </div>
</div>

<!-- 결과 -->
<div class="card result-section">
  <h2>📊 전체 승률 결과</h2>
  <div class="res-grid">
    <div class="res-box char-a" id="box-a">
      <h3>캐릭터 A</h3>
      <div class="res-big" id="rate-a">65.0%</div>
      <div class="detail-bars">
        <div class="db-row">
          <span class="db-lbl">⚔️ 쉬운</span>
          <div class="db-wrap"><div class="db-bar" id="db-a1" style="width:90%;background:linear-gradient(90deg,#4338ca,#6366f1)">90%</div></div>
        </div>
        <div class="db-row">
          <span class="db-lbl">🐉 어려운</span>
          <div class="db-wrap"><div class="db-bar" id="db-a2" style="width:40%;background:linear-gradient(90deg,#4338ca,#6366f1)">40%</div></div>
        </div>
      </div>
      <div id="label-a" style="font-size:.72rem;color:#64748b">계산 중...</div>
    </div>
    <div class="res-box char-b" id="box-b">
      <h3>캐릭터 B</h3>
      <div class="res-big" id="rate-b">55.0%</div>
      <div class="detail-bars">
        <div class="db-row">
          <span class="db-lbl">⚔️ 쉬운</span>
          <div class="db-wrap"><div class="db-bar" id="db-b1" style="width:80%;background:linear-gradient(90deg,#065f46,#059669)">80%</div></div>
        </div>
        <div class="db-row">
          <span class="db-lbl">🐉 어려운</span>
          <div class="db-wrap"><div class="db-bar" id="db-b2" style="width:30%;background:linear-gradient(90deg,#065f46,#059669)">30%</div></div>
        </div>
      </div>
      <div id="label-b" style="font-size:.72rem;color:#64748b">계산 중...</div>
    </div>
  </div>

  <div class="verdict-banner normal" id="verdict">
    <h3 id="verdict-h">⚔️ 현재 상태: 정상 (역설 없음)</h3>
    <p id="verdict-p">A가 전체에서도 우세합니다. 슬라이더를 움직여 역설을 만들어보세요!</p>
  </div>
</div>

<!-- 챌린지 -->
<div class="challenge-box">
  <h2>🏆 챌린지 — 역설을 만들어라!</h2>
  <p>쉬운 던전과 어려운 던전 모두에서 A가 이기지만,<br>
  전체 승률에서는 B가 이기도록 슬라이더를 조절해보세요.</p>
  <div class="challenge-status status-locked" id="ch-status">
    🔒 미완성 — B가 전체에서 더 높아지도록 조절해보세요!
  </div>
</div>

<!-- 현재 수치 표 -->
<div class="card">
  <h2>📋 현재 설정 수치 요약</h2>
  <table class="tbl-mini">
    <tr><th></th>
        <th colspan="2">캐릭터 A</th>
        <th colspan="2">캐릭터 B</th></tr>
    <tr><th></th>
        <th>참여비율</th><th>승률</th>
        <th>참여비율</th><th>승률</th></tr>
    <tr><td>⚔️ 쉬운 던전</td>
        <td id="tb-a1p">50%</td><td class="tw">90%</td>
        <td id="tb-b1p">50%</td><td class="tw">80%</td></tr>
    <tr><td>🐉 어려운 던전</td>
        <td id="tb-a2p">50%</td><td class="tw">40%</td>
        <td id="tb-b2p">50%</td><td class="tw">30%</td></tr>
    <tr class="tr-total"><td>전체</td>
        <td colspan="2" id="tb-ar">—</td>
        <td colspan="2" id="tb-br">—</td></tr>
  </table>
  <div class="hint-box">
    <strong>힌트:</strong> 역설이 일어나려면 B가 높은 승률 구간(쉬운 던전)에,
    A가 낮은 승률 구간(어려운 던전)에 더 많이 참여해야 합니다.<br>
    수학적으로: <strong>B의 쉬운 던전 비율 &gt; A의 쉬운 던전 비율 + 20%p</strong> 일 때 역설이 생깁니다.
  </div>
</div>

<script>
function update(){
  var pA = parseInt(document.getElementById('slA').value)/100;
  var pB = parseInt(document.getElementById('slB').value)/100;

  // 슬라이더 레이블
  document.getElementById('pA-lbl').textContent = Math.round(pA*100)+'%';
  document.getElementById('pB-lbl').textContent = Math.round(pB*100)+'%';
  document.getElementById('pA-g1').textContent = Math.round(pA*100)+'%';
  document.getElementById('pA-g2').textContent = Math.round((1-pA)*100)+'%';
  document.getElementById('pB-g1').textContent = Math.round(pB*100)+'%';
  document.getElementById('pB-g2').textContent = Math.round((1-pB)*100)+'%';
  document.getElementById('rv-a1').style.width = (pA*100)+'%';
  document.getElementById('rv-b1').style.width = (pB*100)+'%';

  // 전체 승률 계산 (그룹별 고정 승률 × 참여비율의 가중합)
  var rA = 0.9*pA + 0.4*(1-pA);  // A: 쉬운 90%, 어려운 40%
  var rB = 0.8*pB + 0.3*(1-pB);  // B: 쉬운 80%, 어려운 30%
  var rAp = (rA*100).toFixed(1);
  var rBp = (rB*100).toFixed(1);

  document.getElementById('rate-a').textContent = rAp+'%';
  document.getElementById('rate-b').textContent = rBp+'%';
  document.getElementById('tb-a1p').textContent = Math.round(pA*100)+'%';
  document.getElementById('tb-a2p').textContent = Math.round((1-pA)*100)+'%';
  document.getElementById('tb-b1p').textContent = Math.round(pB*100)+'%';
  document.getElementById('tb-b2p').textContent = Math.round((1-pB)*100)+'%';
  document.getElementById('tb-ar').innerHTML = '<span class="'+(rA>=rB?'tw':'tl')+'">'+rAp+'%</span>';
  document.getElementById('tb-br').innerHTML = '<span class="'+(rB>rA?'tw':'tl')+'">'+rBp+'%</span>';

  // 부분 성적 설명 레이블
  document.getElementById('label-a').textContent =
    '쉬운 '+Math.round(pA*100)+'% + 어려운 '+Math.round((1-pA)*100)+'%';
  document.getElementById('label-b').textContent =
    '쉬운 '+Math.round(pB*100)+'% + 어려운 '+Math.round((1-pB)*100)+'%';

  var isParadox = rB > rA;  // A wins in both groups (fixed), B wins overall

  // 결과 카드 스타일
  var boxA = document.getElementById('box-a');
  var boxB = document.getElementById('box-b');
  var rateA = document.getElementById('rate-a');
  var rateB = document.getElementById('rate-b');
  if(isParadox){
    boxA.style.background='rgba(248,113,113,.07)';
    boxA.style.borderColor='rgba(248,113,113,.3)';
    boxB.style.background='rgba(74,222,128,.1)';
    boxB.style.borderColor='rgba(74,222,128,.4)';
    rateA.style.color='#f87171';
    rateB.style.color='#4ade80';
  } else {
    boxA.style.background='rgba(99,102,241,.1)';
    boxA.style.borderColor='rgba(99,102,241,.35)';
    boxB.style.background='rgba(255,255,255,.04)';
    boxB.style.borderColor='rgba(255,255,255,.09)';
    rateA.style.color='#a5b4fc';
    rateB.style.color='#86efac';
  }

  // 판정 배너
  var v = document.getElementById('verdict');
  var vh = document.getElementById('verdict-h');
  var vp = document.getElementById('verdict-p');
  var ch = document.getElementById('ch-status');
  if(isParadox){
    v.className='verdict-banner paradox';
    vh.textContent='🎉 심프슨의 역설 달성!';
    vp.innerHTML='<strong>A가 두 그룹 모두에서 이기지만 전체에서는 B가 이깁니다!</strong><br>'
      +'(쉬운: A 90% &gt; B 80% ✓, 어려운: A 40% &gt; B 30% ✓, 전체: A '+rAp+'% &lt; B '+rBp+'% !)';
    ch.className='challenge-status status-done';
    ch.textContent='🏆 챌린지 완성! 심프슨의 역설을 성공적으로 만들었습니다!';
  } else {
    var diff = (rA - rB)*100;
    v.className='verdict-banner normal';
    vh.textContent='⚔️ 현재: 정상 (역설 없음)';
    vp.textContent='A가 전체에서도 우세합니다 (차이: +'+(diff.toFixed(1))+'%p). 슬라이더를 움직여 역설을 만들어보세요!';
    ch.className='challenge-status status-locked';
    ch.textContent='🔒 미완성 — B의 쉬운 던전 비율을 A보다 훨씬 높게 조절해보세요!';
  }
}
update();
function reportHeight(){
  var h = document.documentElement.scrollHeight;
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
var _ro = new ResizeObserver(reportHeight);
_ro.observe(document.body);
reportHeight();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("🔀 심프슨의 역설")
    st.caption(
        "부분의 통계가 전체의 통계를 배반한다! "
        "야구·입학률·의학 세 가지 예시로 심프슨의 역설을 탐구하고, "
        "나만의 역설도 직접 만들어봐요."
    )

    tab1, tab2, tab3 = st.tabs([
        "⚾ 탐구1: 야구 투수 예제",
        "📚 탐구2: 다양한 예시",
        "🎮 탐구3: 나만의 역설 만들기",
    ])

    with tab1:
        components.html(_HTML_TAB1, height=1600, scrolling=False)

    with tab2:
        components.html(_HTML_TAB2, height=1850, scrolling=False)

    with tab3:
        components.html(_HTML_TAB3, height=1580, scrolling=False)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
