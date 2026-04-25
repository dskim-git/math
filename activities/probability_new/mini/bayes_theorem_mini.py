# activities/probability_new/mini/bayes_theorem_mini.py
"""
베이즈 정리 탐구 미니활동
탭1: 🍪 쿠키 상자   — 베이즈 정리 기본 개념 (직관적 이해)
탭2: 🧪 진단 키트   — 교과서 62p 조건부확률 실전 탐구
탭3: 📧 스팸 필터   — 베이즈 정리 활용 사례 1
탭4: 🏃 도핑 검사   — 베이즈 정리 활용 사례 2
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🔮 베이즈 정리 탐구",
    "description": "쿠키 상자·진단키트·스팸필터·도핑검사 4가지 상황으로 베이즈 정리의 핵심을 직관적으로 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "베이즈정리탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 베이즈 정리 탐구**"},
    {
        "key": "사전사후",
        "label": "쿠키 상자 활동에서 '사전확률'과 '사후확률'이 무엇인지 자신의 말로 설명해보세요. 새로운 단서(증거)가 확률을 어떻게 바꿨나요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "상자를 뽑기 전에는 A일 확률이 50%였는데, 딸기 쿠키가 나오자...",
    },
    {
        "key": "진단키트놀라움",
        "label": "진단 키트의 정확도가 95%~99%인데도 양성 판정자 중 실제 감염 확률이 낮을 수 있습니다. 왜 이런 일이 생기는지 설명해보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "감염률 자체가 낮으면 비감염자가 훨씬 많기 때문에...",
    },
    {
        "key": "공통원리",
        "label": "진단키트·스팸필터·도핑검사에서 공통으로 나타나는 베이즈 정리의 원리를 정리해보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "세 가지 모두 검사 전 확률(사전확률)에 검사 결과(가능도)를 반영해서...",
    },
    {
        "key": "실생활사례",
        "label": "베이즈 정리가 활용될 수 있는 다른 실생활 사례를 하나 떠올리고, 사전확률·새로운 증거·사후확률에 해당하는 것이 무엇인지 써보세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) 친구가 거짓말을 하는지 판단할 때 — 사전확률은 평소 거짓말 빈도...",
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
# TAB 1: 쿠키 상자 — 베이즈 정리 기본 개념
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB1 = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:14px 12px 28px;min-height:100vh}
.hdr{text-align:center;padding:16px 20px 12px;background:linear-gradient(135deg,rgba(251,191,36,.14),rgba(249,115,22,.1));border:1px solid rgba(251,191,36,.32);border-radius:14px;margin-bottom:12px}
.hdr h1{font-size:1.25rem;font-weight:700;color:#fbbf24;margin-bottom:5px}
.hdr p{font-size:.8rem;color:#94a3b8;line-height:1.6}
.section{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:13px;padding:13px 12px;margin-bottom:10px}
.sec-title{font-size:.93rem;font-weight:700;margin-bottom:9px;display:flex;align-items:center;gap:6px;color:#fbbf24}
.boxes-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.box-card{border-radius:11px;padding:11px;text-align:center}
.bx-a{background:rgba(59,130,246,.1);border:1.5px solid rgba(59,130,246,.4)}
.bx-b{background:rgba(249,115,22,.1);border:1.5px solid rgba(249,115,22,.4)}
.bx-name{font-size:.95rem;font-weight:700;margin-bottom:7px}
.bx-a .bx-name{color:#60a5fa}.bx-b .bx-name{color:#fb923c}
.ck-grid{display:flex;flex-wrap:wrap;gap:3px;justify-content:center;margin-bottom:7px;padding:2px}
.ck{font-size:1.1rem;line-height:1.2}
.bx-stat{font-size:.72rem;color:#94a3b8;line-height:1.8}
.bx-stat strong{color:#e2e8f0}
.concept{background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.28);border-radius:10px;padding:9px 11px;margin-top:9px;font-size:.79rem;color:#ddd6fe;line-height:1.7}
.concept .kw{color:#fbbf24;font-weight:700}
input[type=range]{width:100%;accent-color:#fbbf24;cursor:pointer;margin:5px 0}
.prob-row{display:flex;border-radius:8px;overflow:hidden;height:34px;margin:7px 0;border:1px solid rgba(255,255,255,.09)}
.pb-a{background:rgba(59,130,246,.45);display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:700;color:#bfdbfe;transition:width .35s;overflow:hidden;white-space:nowrap;min-width:0}
.pb-b{background:rgba(249,115,22,.45);display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:700;color:#fed7aa;flex:1;overflow:hidden;white-space:nowrap}
.prior-vals{display:flex;justify-content:space-between;font-size:.77rem;margin-top:2px}
.pv-a{color:#60a5fa;font-weight:700}.pv-b{color:#fb923c;font-weight:700}
.ev-row{display:flex;gap:8px;margin-top:9px}
.ev-btn{flex:1;padding:11px 6px;border-radius:11px;border:2px solid;font-size:.88rem;font-weight:700;cursor:pointer;transition:all .2s}
.ev-ch{background:rgba(120,53,15,.2);border-color:rgba(180,83,9,.5);color:#fcd34d}
.ev-ch:hover,.ev-ch.sel{background:rgba(120,53,15,.45);border-color:#fbbf24}
.ev-st{background:rgba(159,18,57,.2);border-color:rgba(190,18,60,.5);color:#fda4af}
.ev-st:hover,.ev-st.sel{background:rgba(159,18,57,.45);border-color:#fb7185}
.result-sec{background:rgba(139,92,246,.07);border:1px solid rgba(139,92,246,.3);border-radius:13px;padding:13px 12px;animation:fi .4s ease}
@keyframes fi{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
.res-hdr{font-size:.9rem;font-weight:700;color:#a78bfa;margin-bottom:11px}
.ba-grid{display:grid;grid-template-columns:1fr 32px 1fr;align-items:center;gap:6px;margin-bottom:11px}
.ba-col{text-align:center}
.ba-lbl{font-size:.66rem;color:#64748b;margin-bottom:4px;font-weight:600;letter-spacing:.03em}
.ba-bar{display:flex;border-radius:7px;overflow:hidden;height:46px;border:1px solid rgba(255,255,255,.09)}
.bas-a{background:rgba(59,130,246,.5);display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:700;color:#bfdbfe;transition:width .5s;overflow:hidden;white-space:nowrap;min-width:0}
.bas-b{background:rgba(249,115,22,.5);display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:700;color:#fed7aa;flex:1;overflow:hidden;white-space:nowrap}
.arr{font-size:1.4rem;color:#a78bfa;text-align:center}
.fml{background:rgba(0,0,0,.28);border:1px solid rgba(251,191,36,.22);border-radius:9px;padding:9px 11px;font-size:.72rem;font-family:'Courier New',monospace;line-height:2;color:#fde68a;margin-bottom:9px}
.fml .ans{color:#34d399;font-weight:700;font-size:.85rem}
.insight{background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.28);border-radius:9px;padding:9px 11px;font-size:.78rem;color:#6ee7b7;line-height:1.6}
</style></head>
<body>
<div class="hdr">
  <h1>🍪 쿠키 상자와 베이즈 정리</h1>
  <p>눈을 감고 두 상자 중 하나에서 쿠키를 꺼냈어요.<br>
  꺼낸 쿠키 종류로 "<span style="color:#fbbf24">어느 상자일 확률</span>"을 업데이트해봐요!</p>
</div>

<div class="section">
  <div class="sec-title">📦 두 상자의 쿠키 구성</div>
  <div class="boxes-row">
    <div class="box-card bx-a">
      <div class="bx-name">상자 A</div>
      <div class="ck-grid" id="boxA"></div>
      <div class="bx-stat"><strong>🍫 초콜릿</strong> 90%&nbsp;&nbsp;<strong>🍓 딸기</strong> 10%</div>
    </div>
    <div class="box-card bx-b">
      <div class="bx-name">상자 B</div>
      <div class="ck-grid" id="boxB"></div>
      <div class="bx-stat"><strong>🍫 초콜릿</strong> 20%&nbsp;&nbsp;<strong>🍓 딸기</strong> 80%</div>
    </div>
  </div>
  <div class="concept">
    <span class="kw">베이즈 정리</span>란? "새로운 사실(꺼낸 쿠키)을 알았을 때,
    내 생각(상자A일 확률)을 합리적으로 업데이트하는 방법"<br>
    → <span class="kw">사전확률</span>(관찰 전) + <span class="kw">새로운 증거</span> = <span class="kw">사후확률</span>(관찰 후)
  </div>
</div>

<div class="section">
  <div class="sec-title">🎲 Step 1: 사전확률 — 어느 상자를 뽑을 확률?</div>
  <div style="font-size:.79rem;color:#94a3b8;margin-bottom:6px">슬라이더로 상자 A를 선택할 확률을 조절해봐요. (기본: 50%씩 동일)</div>
  <input type="range" id="priorSl" min="10" max="90" step="5" value="50" oninput="onPrior()">
  <div class="prob-row">
    <div class="pb-a" id="pbA" style="width:50%">상자A&nbsp;50%</div>
    <div class="pb-b" id="pbB">상자B&nbsp;50%</div>
  </div>
  <div class="prior-vals">
    <span class="pv-a" id="pvA">P(상자A) = 0.50</span>
    <span class="pv-b" id="pvB">P(상자B) = 0.50</span>
  </div>
</div>

<div class="section">
  <div class="sec-title">🔍 Step 2: 증거 관찰 — 꺼낸 쿠키는?</div>
  <div style="font-size:.79rem;color:#94a3b8;margin-bottom:8px">쿠키 종류를 선택하면 베이즈 정리로 확률을 업데이트할게요!</div>
  <div class="ev-row">
    <button class="ev-btn ev-ch" id="btnCh" onclick="observe('C')">🍫 초콜릿 쿠키</button>
    <button class="ev-btn ev-st" id="btnSt" onclick="observe('S')">🍓 딸기 쿠키</button>
  </div>
</div>

<div id="resDiv" style="display:none" class="result-sec">
  <div class="res-hdr" id="resHdr">📊 베이즈 업데이트!</div>
  <div class="ba-grid">
    <div class="ba-col">
      <div class="ba-lbl">⬅ 사전확률 (관찰 전)</div>
      <div class="ba-bar" id="baBef"></div>
      <div style="display:flex;justify-content:space-between;font-size:.66rem;margin-top:3px">
        <span style="color:#60a5fa" id="befA"></span>
        <span style="color:#fb923c" id="befB"></span>
      </div>
    </div>
    <div class="arr">→</div>
    <div class="ba-col">
      <div class="ba-lbl">사후확률 (관찰 후) ➡</div>
      <div class="ba-bar" id="baAft"></div>
      <div style="display:flex;justify-content:space-between;font-size:.66rem;margin-top:3px">
        <span style="color:#60a5fa" id="aftA"></span>
        <span style="color:#fb923c" id="aftB"></span>
      </div>
    </div>
  </div>
  <div class="fml" id="fmlBox"></div>
  <div class="insight" id="insBox"></div>
</div>

<script>
var pA=0.5;
(function(){
  var ga=document.getElementById('boxA'),gb=document.getElementById('boxB');
  for(var i=0;i<10;i++){
    var s1=document.createElement('span');s1.className='ck';s1.textContent=i<9?'🍫':'🍓';ga.appendChild(s1);
    var s2=document.createElement('span');s2.className='ck';s2.textContent=i<2?'🍫':'🍓';gb.appendChild(s2);
  }
})();
function onPrior(){
  pA=parseInt(document.getElementById('priorSl').value)/100;
  var pB=1-pA,a=Math.round(pA*100),b=100-a;
  document.getElementById('pbA').style.width=a+'%';
  document.getElementById('pbA').textContent='상자A\u00a0'+a+'%';
  document.getElementById('pbB').textContent='상자B\u00a0'+b+'%';
  document.getElementById('pvA').textContent='P(상자A) = '+pA.toFixed(2);
  document.getElementById('pvB').textContent='P(상자B) = '+pB.toFixed(2);
  document.getElementById('resDiv').style.display='none';
  document.getElementById('btnCh').classList.remove('sel');
  document.getElementById('btnSt').classList.remove('sel');
}
function p2s(v){return (v*100).toFixed(1)+'%';}
function observe(ev){
  document.getElementById('btnCh').classList.toggle('sel',ev==='C');
  document.getElementById('btnSt').classList.toggle('sel',ev==='S');
  var pB=1-pA;
  var pEA=ev==='C'?0.9:0.1, pEB=ev==='C'?0.2:0.8;
  var num=pEA*pA, den=pEA*pA+pEB*pB, post=num/den, postB=1-post;
  var en=ev==='C'?'초콜릿':'딸기', ee=ev==='C'?'🍫':'🍓';
  document.getElementById('resHdr').textContent='📊 '+ee+' '+en+' 쿠키를 꺼냈을 때!';
  var beA=Math.round(pA*100);
  document.getElementById('baBef').innerHTML=
    '<div class="bas-a" style="width:'+beA+'%">'+p2s(pA)+'</div>'+
    '<div class="bas-b">'+p2s(pB)+'</div>';
  document.getElementById('befA').textContent='상자A '+p2s(pA);
  document.getElementById('befB').textContent='상자B '+p2s(pB);
  var afA=Math.round(post*100);
  document.getElementById('baAft').innerHTML=
    '<div class="bas-a" style="width:'+afA+'%">'+p2s(post)+'</div>'+
    '<div class="bas-b">'+p2s(postB)+'</div>';
  document.getElementById('aftA').textContent='상자A '+p2s(post);
  document.getElementById('aftB').textContent='상자B '+p2s(postB);
  document.getElementById('fmlBox').innerHTML=
    'P(상자A | '+en+') =<br>'+
    '\u00a0\u00a0P('+en+'|상자A) \u00d7 P(상자A)<br>'+
    '\u00a0\u00a0\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500<br>'+
    '\u00a0\u00a0P('+en+'|상자A)\u00d7P(상자A) + P('+en+'|상자B)\u00d7P(상자B)<br><br>'+
    '= '+pEA.toFixed(2)+' \u00d7 '+pA.toFixed(2)+'<br>'+
    '\u00a0\u00a0\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500<br>'+
    '\u00a0\u00a0'+pEA.toFixed(2)+'\u00d7'+pA.toFixed(2)+' + '+pEB.toFixed(2)+'\u00d7'+pB.toFixed(2)+'<br><br>'+
    '= '+num.toFixed(4)+' / '+den.toFixed(4)+' = <span class="ans">'+p2s(post)+'</span>';
  var chg=post>pA?'높아졌어요 \u2191':'낮아졌어요 \u2193';
  var why=ev==='C'
    ?'초콜릿 쿠키가 나왔어요! 상자A의 초콜릿 비율(90%)이 상자B(20%)보다 훨씬 높으니, 상자A일 가능성이'
    :'딸기 쿠키가 나왔어요! 상자B의 딸기 비율(80%)이 상자A(10%)보다 훨씬 높으니, 상자A일 가능성이';
  document.getElementById('insBox').innerHTML=
    ee+' '+why+' <strong>'+chg+'</strong><br>'+
    '사전확률 '+p2s(pA)+' \u2192 사후확률 <strong>'+p2s(post)+'</strong><br><br>'+
    '💡 슬라이더로 사전확률을 바꿔봐요! 사전확률이 달라지면 사후확률도 달라지나요?';
  document.getElementById('resDiv').style.display='block';
}
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: 진단 키트 — 교과서 62p 탐구
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB2 = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:14px 12px 28px;min-height:100vh}
.hdr{text-align:center;padding:16px 20px 12px;background:linear-gradient(135deg,rgba(20,184,166,.14),rgba(6,182,212,.1));border:1px solid rgba(20,184,166,.32);border-radius:14px;margin-bottom:12px}
.hdr h1{font-size:1.2rem;font-weight:700;color:#2dd4bf;margin-bottom:5px}
.hdr p{font-size:.79rem;color:#94a3b8;line-height:1.6}
.section{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:13px;padding:13px 12px;margin-bottom:10px}
.sec-title{font-size:.92rem;font-weight:700;margin-bottom:9px;display:flex;align-items:center;gap:6px;color:#2dd4bf}
.prob-box{background:rgba(0,0,0,.22);border:1px solid rgba(255,255,255,.08);border-radius:9px;padding:8px 10px;margin-bottom:7px;font-size:.79rem;color:#94a3b8;line-height:1.7}
.prob-box strong{color:#e2e8f0}
.sl-row{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:8px;margin-bottom:9px}
.sl-label{font-size:.77rem;color:#94a3b8;white-space:nowrap}
input[type=range]{accent-color:#2dd4bf;cursor:pointer}
.sl-val{font-size:.82rem;color:#2dd4bf;font-weight:700;font-family:monospace;min-width:38px;text-align:right}
table{width:100%;border-collapse:collapse;margin-bottom:8px;font-size:.79rem}
th,td{border:1px solid rgba(255,255,255,.14);padding:7px 9px;text-align:center}
th{background:rgba(45,212,191,.14);color:#2dd4bf;font-weight:700}
td{background:rgba(255,255,255,.03);transition:background .3s}
td.highlight{background:rgba(251,191,36,.18);color:#fbbf24;font-weight:700}
td.total{background:rgba(255,255,255,.07);color:#e2e8f0;font-weight:700}
td.key{background:rgba(239,68,68,.2);color:#fca5a5;font-weight:700;font-size:.88rem}
.result-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}
.rcard{border-radius:9px;padding:9px 10px;text-align:center}
.rc-a{background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.3)}
.rc-b{background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.3)}
.rc-ab{background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.3)}
.rc-ba{background:rgba(239,68,68,.12);border:1.5px solid rgba(239,68,68,.4)}
.rc-lbl{font-size:.67rem;color:#94a3b8;margin-bottom:3px;font-family:monospace}
.rc-val{font-size:1.1rem;font-weight:700;font-family:monospace}
.rc-a .rc-val{color:#60a5fa}.rc-b .rc-val{color:#fb923c}
.rc-ab .rc-val{color:#a78bfa}.rc-ba .rc-val{color:#fca5a5;font-size:1.35rem}
.warn-box{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.35);border-radius:10px;padding:9px 11px;font-size:.78rem;color:#fca5a5;line-height:1.6;margin-top:6px}
.ok-box{background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.28);border-radius:10px;padding:9px 11px;font-size:.78rem;color:#6ee7b7;line-height:1.6;margin-top:6px}
</style></head>
<body>
<div class="hdr">
  <h1>🧪 진단 키트 결과 속 조건부확률</h1>
  <p>교과서 62p 문제 — 슬라이더를 조절해 감염률과 검사 정확도가 결과에 어떤 영향을 주는지 탐구해봐요!</p>
</div>

<div class="section">
  <div class="sec-title">⚙️ 매개변수 설정 (기준: 100,000명 검사)</div>
  <div class="prob-box">
    <strong>문제 상황</strong>: 일반인 1000명 중 5명꼴로 감염되는 바이러스의 진단 키트.<br>
    이 키트는 <strong>감염자를 양성</strong>으로 판정할 확률 <strong>0.95</strong>, <strong>비감염자를 음성</strong>으로 판정할 확률 <strong>0.99</strong>.
  </div>
  <div class="sl-row">
    <span class="sl-label">감염률</span>
    <input type="range" id="slRate" min="1" max="50" step="1" value="5" oninput="calc()" style="width:100%">
    <span class="sl-val" id="valRate">0.5%</span>
  </div>
  <div class="sl-row">
    <span class="sl-label">민감도 P(양성|감염)</span>
    <input type="range" id="slSens" min="50" max="99" step="1" value="95" oninput="calc()" style="width:100%">
    <span class="sl-val" id="valSens">95%</span>
  </div>
  <div class="sl-row">
    <span class="sl-label">특이도 P(음성|비감염)</span>
    <input type="range" id="slSpec" min="50" max="99" step="1" value="99" oninput="calc()" style="width:100%">
    <span class="sl-val" id="valSpec">99%</span>
  </div>
</div>

<div class="section">
  <div class="sec-title">📋 분할표 (100,000명 기준)</div>
  <table>
    <thead><tr><th></th><th>양성 판정</th><th>음성 판정</th><th>합계</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:700;color:#94a3b8">감염자</td><td class="highlight" id="tTP">475</td><td id="tFN">25</td><td class="total" id="tI">500</td></tr>
      <tr><td style="font-weight:700;color:#94a3b8">비감염자</td><td id="tFP">995</td><td id="tTN">98505</td><td class="total" id="tC">99500</td></tr>
      <tr><td style="font-weight:700;color:#e2e8f0">합계</td><td class="total key" id="tTPos">1470</td><td class="total" id="tTNeg">98530</td><td class="total">100,000</td></tr>
    </tbody>
  </table>
  <div style="font-size:.71rem;color:#64748b">* 하이라이트(노란색) = 감염자이면서 양성 판정 / 빨간색 테두리 = 전체 양성 판정자</div>
</div>

<div class="section">
  <div class="sec-title">📊 조건부확률 계산 결과</div>
  <div class="result-grid">
    <div class="rcard rc-a"><div class="rc-lbl">P(A) = P(감염)</div><div class="rc-val" id="rPA">-</div></div>
    <div class="rcard rc-b"><div class="rc-lbl">P(B) = P(양성 판정)</div><div class="rc-val" id="rPB">-</div></div>
    <div class="rcard rc-ab"><div class="rc-lbl">P(A|B) = P(감염|양성)</div><div class="rc-val" id="rPAB">-</div></div>
    <div class="rcard rc-ba"><div class="rc-lbl">P(B|A) = P(양성|감염) = 민감도</div><div class="rc-val" id="rPBA">-</div></div>
  </div>
  <div id="insBox"></div>
</div>

<script>
function fmt(n){return n.toLocaleString();}
function fmtP(v){return (v*100).toFixed(2)+'%';}
function calc(){
  var rate=parseInt(document.getElementById('slRate').value)/1000;
  var sens=parseInt(document.getElementById('slSens').value)/100;
  var spec=parseInt(document.getElementById('slSpec').value)/100;
  document.getElementById('valRate').textContent=(rate*100).toFixed(1)+'%';
  document.getElementById('valSens').textContent=(sens*100).toFixed(0)+'%';
  document.getElementById('valSpec').textContent=(spec*100).toFixed(0)+'%';
  var N=100000;
  var inf=Math.round(N*rate), cln=N-inf;
  var tp=Math.round(inf*sens), fn=inf-tp;
  var tn=Math.round(cln*spec), fp=cln-tn;
  var tpos=tp+fp, tneg=fn+tn;
  document.getElementById('tTP').textContent=fmt(tp);
  document.getElementById('tFN').textContent=fmt(fn);
  document.getElementById('tI').textContent=fmt(inf);
  document.getElementById('tFP').textContent=fmt(fp);
  document.getElementById('tTN').textContent=fmt(tn);
  document.getElementById('tC').textContent=fmt(cln);
  document.getElementById('tTPos').textContent=fmt(tpos);
  document.getElementById('tTNeg').textContent=fmt(tneg);
  var pA=inf/N, pB=tpos/N;
  var pAgivenB=tpos>0?tp/tpos:0;
  var pBgivenA=sens;
  document.getElementById('rPA').textContent=fmtP(pA);
  document.getElementById('rPB').textContent=fmtP(pB);
  document.getElementById('rPAB').textContent=fmtP(pAgivenB);
  document.getElementById('rPBA').textContent=fmtP(pBgivenA);
  var ins='';
  if(pAgivenB<0.5){
    ins='<div class="warn-box">⚠️ <strong>놀라운 결과!</strong> 양성 판정을 받아도 실제로 감염됐을 확률이 '+fmtP(pAgivenB)+'밖에 안 돼요!<br>'+
      '이유: 감염률('+fmtP(pA)+')이 낮아서 비감염자가 훨씬 많고, 그 중 일부('+fmt(fp)+'명)가 양성으로 잘못 판정돼요.<br>'+
      '💡 감염률 슬라이더를 높이면 P(감염|양성)도 높아지는지 확인해봐요!</div>';
  } else {
    ins='<div class="ok-box">✅ 양성 판정 시 실제 감염 확률 '+fmtP(pAgivenB)+'. 감염률이 충분히 높으면 검사 결과를 더 신뢰할 수 있어요!<br>'+
      '💡 감염률 슬라이더를 다시 낮춰보면 어떻게 달라지나요?</div>';
  }
  ins+='<div style="margin-top:6px;font-size:.72rem;color:#64748b">베이즈 정리 검증: P(A|B) = P(B|A)\u00d7P(A) / P(B) = '+
    fmtP(pBgivenA)+'\u00d7'+fmtP(pA)+' / '+fmtP(pB)+' = '+fmtP(pBgivenA*pA/pB)+'</div>';
  document.getElementById('insBox').innerHTML=ins;
}
calc();
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: 스팸 필터 — 베이즈 정리 활용 1
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB3 = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:14px 12px 28px;min-height:100vh}
.hdr{text-align:center;padding:16px 20px 12px;background:linear-gradient(135deg,rgba(139,92,246,.14),rgba(99,102,241,.1));border:1px solid rgba(139,92,246,.32);border-radius:14px;margin-bottom:12px}
.hdr h1{font-size:1.2rem;font-weight:700;color:#a78bfa;margin-bottom:5px}
.hdr p{font-size:.79rem;color:#94a3b8;line-height:1.6}
.section{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:13px;padding:13px 12px;margin-bottom:10px}
.sec-title{font-size:.92rem;font-weight:700;margin-bottom:9px;display:flex;align-items:center;gap:6px;color:#a78bfa}
.context{background:rgba(0,0,0,.2);border:1px solid rgba(255,255,255,.08);border-radius:9px;padding:9px 11px;font-size:.79rem;color:#94a3b8;line-height:1.7;margin-bottom:10px}
.context strong{color:#e2e8f0}
.kw-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:10px}
.kw-card{border-radius:9px;padding:9px 10px;background:rgba(255,255,255,.04);border:1.5px solid rgba(255,255,255,.1);cursor:pointer;transition:all .18s;user-select:none}
.kw-card.checked-spam{background:rgba(239,68,68,.18);border-color:rgba(239,68,68,.55)}
.kw-card.checked-ham{background:rgba(52,211,153,.12);border-color:rgba(52,211,153,.45)}
.kw-top{display:flex;align-items:center;gap:5px;margin-bottom:5px}
.kw-check{width:16px;height:16px;border-radius:3px;border:2px solid rgba(255,255,255,.3);flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:.7rem}
.kw-card.checked-spam .kw-check{background:#ef4444;border-color:#ef4444;color:#fff}
.kw-card.checked-ham .kw-check{background:#34d399;border-color:#34d399;color:#fff}
.kw-word{font-size:.88rem;font-weight:700;color:#e2e8f0}
.kw-desc{font-size:.66rem;color:#64748b;margin-bottom:4px}
.kw-bars{display:flex;gap:4px}
.bar-mini-wrap{flex:1}
.bar-mini-lbl{font-size:.6rem;color:#94a3b8;margin-bottom:1px}
.bar-mini{height:7px;border-radius:3px;transition:width .3s}
.bm-spam{background:#ef4444}
.bm-ham{background:#34d399}
.kw-nums{display:flex;justify-content:space-between;font-size:.6rem;margin-top:2px}
.kw-s{color:#fca5a5}.kw-h{color:#86efac}
.meter-wrap{margin-bottom:10px}
.meter-lbl{font-size:.83rem;color:#94a3b8;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center}
.meter-lbl strong{font-size:1.1rem;font-family:monospace}
.meter-bar-bg{height:22px;border-radius:11px;background:rgba(255,255,255,.08);overflow:hidden;border:1px solid rgba(255,255,255,.1)}
.meter-fill{height:100%;border-radius:11px;transition:width .5s,background .5s;display:flex;align-items:center;justify-content:flex-end;padding-right:8px;font-size:.72rem;font-weight:700;color:#fff;min-width:0}
.verdict{text-align:center;padding:11px;border-radius:11px;font-size:1rem;font-weight:700;margin-bottom:8px;transition:all .4s}
.vd-spam{background:rgba(239,68,68,.2);border:1.5px solid rgba(239,68,68,.5);color:#fca5a5}
.vd-ham{background:rgba(52,211,153,.12);border:1.5px solid rgba(52,211,153,.4);color:#6ee7b7}
.vd-neutral{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.13);color:#94a3b8}
.calc-box{background:rgba(0,0,0,.25);border:1px solid rgba(139,92,246,.2);border-radius:9px;padding:8px 10px;font-size:.72rem;font-family:'Courier New',monospace;color:#c4b5fd;line-height:1.9}
.insight{background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.28);border-radius:9px;padding:9px 11px;font-size:.78rem;color:#6ee7b7;line-height:1.6;margin-top:8px}
</style></head>
<body>
<div class="hdr">
  <h1>📧 스팸 필터와 베이즈 정리</h1>
  <p>이메일의 단어들을 분석해 스팸 여부를 판단해봐요!<br>단어를 클릭해 이메일에 포함됐는지 체크하면 스팸 확률이 업데이트됩니다.</p>
</div>

<div class="section">
  <div class="sec-title">⚙️ 설정 — 베이즈 나이브 스팸 필터</div>
  <div class="context">
    <strong>상황</strong>: 받은 이메일 중 평균 <strong>40%가 스팸</strong>이에요.<br>
    아래 단어들이 스팸 메일과 정상 메일에 얼마나 자주 나타나는지 통계가 있어요.<br>
    이 이메일에 포함된 단어를 체크하면, 스팸일 확률이 계산됩니다!
  </div>
  <div class="kw-grid" id="kwGrid"></div>
  <div style="font-size:.7rem;color:#64748b">👆 단어 카드를 클릭해서 이메일에 포함된 단어를 선택하세요</div>
</div>

<div class="section">
  <div class="sec-title">📊 스팸 확률 미터</div>
  <div class="meter-wrap">
    <div class="meter-lbl">스팸 확률 <strong id="meterPct">40.0%</strong></div>
    <div class="meter-bar-bg">
      <div class="meter-fill" id="meterFill" style="width:40%;background:#f59e0b">40%</div>
    </div>
  </div>
  <div class="verdict vd-neutral" id="verdict">단어를 선택해봐요!</div>
  <div class="calc-box" id="calcBox">P(스팸) = 0.40 (사전확률, 선택된 단어 없음)</div>
</div>

<div id="insightDiv" style="display:none">
  <div class="insight" id="insightBox"></div>
</div>

<script>
var KWS=[
  {w:'무료',e:'free',ps:0.80,ph:0.05,checked:false},
  {w:'당첨',e:'winner',ps:0.70,ph:0.02,checked:false},
  {w:'긴급',e:'urgent',ps:0.60,ph:0.10,checked:false},
  {w:'광고',e:'ad',ps:0.65,ph:0.15,checked:false},
  {w:'할인',e:'discount',ps:0.50,ph:0.25,checked:false},
  {w:'이벤트',e:'event',ps:0.55,ph:0.20,checked:false},
  {w:'회의',e:'meeting',ps:0.05,ph:0.40,checked:false},
  {w:'숙제',e:'homework',ps:0.01,ph:0.35,checked:false},
  {w:'성적',e:'grade',ps:0.02,ph:0.30,checked:false},
  {w:'친구',e:'friend',ps:0.03,ph:0.45,checked:false},
];
var PRIOR_SPAM=0.40;

function buildGrid(){
  var el=document.getElementById('kwGrid');
  el.innerHTML='';
  KWS.forEach(function(k,i){
    var card=document.createElement('div');
    card.className='kw-card'+(k.checked?(k.ps>k.ph?' checked-spam':' checked-ham'):'');
    card.onclick=function(){toggle(i);};
    var spamW=Math.round(k.ps*100), hamW=Math.round(k.ph*100);
    card.innerHTML=
      '<div class="kw-top">'+
        '<div class="kw-check" id="ck'+i+'">'+(k.checked?'\u2714':'')+'</div>'+
        '<span class="kw-word">'+k.w+'</span>'+
        '<span style="font-size:.65rem;color:#64748b;margin-left:3px">('+k.e+')</span>'+
      '</div>'+
      '<div class="kw-desc">'+(k.ps>k.ph?'🚨 스팸에 자주 등장':'✅ 정상 메일에 자주 등장')+'</div>'+
      '<div class="kw-bars">'+
        '<div class="bar-mini-wrap">'+
          '<div class="bar-mini-lbl">스팸</div>'+
          '<div class="bar-mini bm-spam" style="width:'+spamW+'%"></div>'+
        '</div>'+
        '<div class="bar-mini-wrap">'+
          '<div class="bar-mini-lbl">정상</div>'+
          '<div class="bar-mini bm-ham" style="width:'+hamW+'%"></div>'+
        '</div>'+
      '</div>'+
      '<div class="kw-nums">'+
        '<span class="kw-s">스팸 '+spamW+'%</span>'+
        '<span class="kw-h">정상 '+hamW+'%</span>'+
      '</div>';
    el.appendChild(card);
  });
}
function toggle(i){
  KWS[i].checked=!KWS[i].checked;
  buildGrid();
  updateMeter();
}
function updateMeter(){
  var lS=Math.log(PRIOR_SPAM), lH=Math.log(1-PRIOR_SPAM);
  var selected=[];
  KWS.forEach(function(k){
    if(k.checked){lS+=Math.log(k.ps);lH+=Math.log(k.ph);selected.push(k);}
  });
  var maxL=Math.max(lS,lH);
  var eS=Math.exp(lS-maxL), eH=Math.exp(lH-maxL);
  var pSpam=eS/(eS+eH);
  var pct=(pSpam*100).toFixed(1);
  document.getElementById('meterPct').textContent=pct+'%';
  var fill=document.getElementById('meterFill');
  fill.style.width=pct+'%';
  var bg=pSpam>0.8?'#ef4444':pSpam>0.5?'#f59e0b':'#34d399';
  fill.style.background=bg;
  fill.textContent=pct+'%';
  var verdict=document.getElementById('verdict');
  if(selected.length===0){
    verdict.className='verdict vd-neutral';verdict.textContent='\ub2e8\uc5b4\ub97c \uc120\ud0dd\ud574\ubd10\uc694!';
  } else if(pSpam>0.8){
    verdict.className='verdict vd-spam';verdict.textContent='🚨 \uc2a4\ud338 \uc758\uc2ec! ('+pct+'%)';
  } else if(pSpam>0.5){
    verdict.className='verdict vd-spam';verdict.textContent='\u26a0\ufe0f \uc2a4\ud338 \uac00\ub2a5\uc131 \uc788\uc74c ('+pct+'%)';
  } else {
    verdict.className='verdict vd-ham';verdict.textContent='\u2705 \uc815\uc0c1 \uba54\uc77c \uac00\ub2a5\uc131 \ub192\uc74c ('+pct+'%)';
  }
  // Calc box
  var lines=['P(\uc2a4\ud338) = '+PRIOR_SPAM.toFixed(2)+' (사전확률)'];
  selected.forEach(function(k){
    lines.push("P('"+k.w+"'|\uc2a4\ud338) = "+k.ps.toFixed(2)+", P('"+k.w+"'|\uc815\uc0c1) = "+k.ph.toFixed(2));
  });
  if(selected.length>0){
    lines.push('\u2192 \ub098\uc774\ube0c \ubca0\uc774\uc988 \uacc4\uc0b0');
    lines.push('\uc0ac\ud6c4\ud655\ub960 P(\uc2a4\ud338|\ub2e8\uc5b4\ub4e4) \u2248 '+pct+'%');
  }
  document.getElementById('calcBox').innerHTML=lines.join('<br>');
  if(selected.length>0){
    var ins='';
    if(pSpam>0.8) ins='🚨 \uc120\ud0dd\ud55c \ub2e8\uc5b4\ub4e4\uc774 \uc2a4\ud338\uc5d0\uc11c \ub9ce\uc774 \ub098\ud0c0\ub098\ub294 \ud328\ud134\uc774\uc5d0\uc694! \uc2a4\ud338 \ud544\ud130\uac00 \uc774 \uba54\uc77c\uc744 \ud65c\ub2f9\uc73c\ub85c \ubd84\ub958\ud560 \uac70\uc608\uc694.';
    else if(pSpam>0.5) ins='\u26a0\ufe0f \uc2a4\ud338 \ub2e8\uc5b4\ub3c4 \uc788\uc9c0\ub9cc \uc815\uc0c1 \uba54\uc77c\uc5d0\ub3c4 \ub098\ud0c0\ub0a0 \uc218 \uc788\ub294 \ub2e8\uc5b4\ub3c4 \ud568\uaed8 \uc788\uc5b4\uc694. \ucd94\uac00 \ub2e8\uc11c\uac00 \ud544\uc694\ud574\uc694.';
    else ins='\u2705 \uc815\uc0c1 \uba54\uc77c\uc5d0 \uc790\uc8fc \ub098\ud0c0\ub098\ub294 \ub2e8\uc5b4\ub4e4\uc774\uc5d0\uc694! \uc2a4\ud338 \ud544\ud130\uac00 \uc774 \uba54\uc77c\uc744 \ud1b5\uacfc\uc2dc\ud0ac \uac70\uc608\uc694.';
    ins+='<br><br>💡 \ub2e8\uc5b4\ub97c \ud558\ub098\uc529 \uccb4\ud06c\ud558\uba74\uc11c \ud655\ub960\uc774 \uc5b4\ub5bb\uac8c \uce74\uc9c0\ub294\uc9c0 \ud655\uc778\ud574\ubcf4\uc138\uc694! (\ub098\uc774\ube0c \ubca0\uc774\uc988 \ud544\ud130\ub294 \uac01 \ub2e8\uc5b4\uac00 <strong>\ub3c5\ub9bd\uc801\uc73c\ub85c</strong> \uc2a4\ud338 \uc5ec\ubd80\uc5d0 \uc601\ud5a5\uc744 \uc900\ub2e4\uace0 \uac00\uc815\ud574\uc694.)';
    document.getElementById('insightBox').innerHTML=ins;
    document.getElementById('insightDiv').style.display='block';
  } else {
    document.getElementById('insightDiv').style.display='none';
  }
}
buildGrid();
updateMeter();
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: 도핑 검사 — 베이즈 정리 활용 2
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB4 = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:14px 12px 28px;min-height:100vh}
.hdr{text-align:center;padding:16px 20px 12px;background:linear-gradient(135deg,rgba(249,115,22,.14),rgba(239,68,68,.1));border:1px solid rgba(249,115,22,.32);border-radius:14px;margin-bottom:12px}
.hdr h1{font-size:1.2rem;font-weight:700;color:#fb923c;margin-bottom:5px}
.hdr p{font-size:.79rem;color:#94a3b8;line-height:1.6}
.section{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:13px;padding:13px 12px;margin-bottom:10px}
.sec-title{font-size:.92rem;font-weight:700;margin-bottom:9px;display:flex;align-items:center;gap:6px;color:#fb923c}
.story{background:rgba(0,0,0,.2);border:1px solid rgba(255,255,255,.08);border-radius:9px;padding:9px 11px;font-size:.79rem;color:#94a3b8;line-height:1.7;margin-bottom:10px}
.story strong{color:#e2e8f0}
.sl-row{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:8px;margin-bottom:9px}
.sl-label{font-size:.77rem;color:#94a3b8;white-space:nowrap}
input[type=range]{accent-color:#fb923c;cursor:pointer}
.sl-val{font-size:.82rem;color:#fb923c;font-weight:700;font-family:monospace;min-width:38px;text-align:right}
.person-grid{display:flex;flex-wrap:wrap;gap:3px;padding:5px;background:rgba(0,0,0,.2);border-radius:9px;margin-bottom:8px;min-height:60px}
.p-dot{width:14px;height:14px;border-radius:3px;transition:background .35s,border-color .35s;flex-shrink:0;border:1.5px solid transparent}
.p-tp{background:#ef4444;border-color:#dc2626}
.p-fp{background:rgba(249,115,22,.7);border-color:#f97316}
.p-fn{background:rgba(139,0,0,.6);border-color:#991b1b}
.p-tn{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.12)}
.legend{display:flex;flex-wrap:wrap;gap:8px;font-size:.68rem;margin-bottom:8px}
.leg{display:flex;align-items:center;gap:4px}
.ld{width:11px;height:11px;border-radius:2px;flex-shrink:0;border:1.5px solid}
table{width:100%;border-collapse:collapse;margin-bottom:8px;font-size:.79rem}
th,td{border:1px solid rgba(255,255,255,.14);padding:7px 9px;text-align:center}
th{background:rgba(249,115,22,.14);color:#fb923c;font-weight:700}
td{background:rgba(255,255,255,.03)}
td.hl{background:rgba(251,191,36,.18);color:#fbbf24;font-weight:700}
td.tot{background:rgba(255,255,255,.07);color:#e2e8f0;font-weight:700}
td.key{background:rgba(239,68,68,.2);color:#fca5a5;font-weight:700}
.big-result{text-align:center;padding:14px;border-radius:13px;margin-bottom:9px;transition:all .4s}
.br-num{font-size:2rem;font-weight:700;font-family:monospace}
.br-lbl{font-size:.78rem;margin-top:4px}
.br-hi{background:rgba(239,68,68,.15);border:1.5px solid rgba(239,68,68,.4)}
.br-hi .br-num{color:#f87171}
.br-ok{background:rgba(52,211,153,.1);border:1.5px solid rgba(52,211,153,.35)}
.br-ok .br-num{color:#34d399}
.warn-box{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.35);border-radius:10px;padding:9px 11px;font-size:.78rem;color:#fca5a5;line-height:1.6}
.ok-box{background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.28);border-radius:10px;padding:9px 11px;font-size:.78rem;color:#6ee7b7;line-height:1.6}
.compare{background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.28);border-radius:10px;padding:9px 11px;font-size:.78rem;color:#ddd6fe;line-height:1.6;margin-top:8px}
</style></head>
<body>
<div class="hdr">
  <h1>🏃 스포츠 도핑 검사와 베이즈 정리</h1>
  <p>양성 판정을 받은 선수가 실제로 도핑을 했을 확률은 얼마일까요?<br>진단 키트 문제와 비교하며 베이즈 정리의 핵심 원리를 탐구해봐요!</p>
</div>

<div class="section">
  <div class="sec-title">⚙️ 도핑 검사 설정 (기준: 1,000명 선수)</div>
  <div class="story">
    <strong>상황</strong>: 국제 스포츠 대회에 1,000명의 선수가 참가했어요.
    이 중 일부가 금지 약물을 복용했을 수 있어요.<br>
    도핑 검사는 매우 정확하지만, 완벽하지는 않아요.
    양성 판정을 받은 선수가 정말로 도핑을 했을 확률은 얼마일까요?
  </div>
  <div class="sl-row">
    <span class="sl-label">도핑 비율</span>
    <input type="range" id="slDop" min="1" max="100" step="1" value="20" oninput="calc()" style="width:100%">
    <span class="sl-val" id="valDop">2.0%</span>
  </div>
  <div class="sl-row">
    <span class="sl-label">민감도 P(양성|도핑)</span>
    <input type="range" id="slSens" min="70" max="99" step="1" value="99" oninput="calc()" style="width:100%">
    <span class="sl-val" id="valSens">99%</span>
  </div>
  <div class="sl-row">
    <span class="sl-label">특이도 P(음성|클린)</span>
    <input type="range" id="slSpec" min="70" max="99" step="1" value="95" oninput="calc()" style="width:100%">
    <span class="sl-val" id="valSpec">95%</span>
  </div>
</div>

<div class="section">
  <div class="sec-title">👥 1,000명 선수 시각화 (각 점 = 1명)</div>
  <div class="legend">
    <div class="leg"><div class="ld" style="background:#ef4444;border-color:#dc2626"></div><span style="color:#fca5a5">도핑 + 양성 (TP)</span></div>
    <div class="leg"><div class="ld" style="background:rgba(249,115,22,.7);border-color:#f97316"></div><span style="color:#fed7aa">클린 + 양성 (FP)</span></div>
    <div class="leg"><div class="ld" style="background:rgba(139,0,0,.6);border-color:#991b1b"></div><span style="color:#fca5a5">도핑 + 음성 (FN)</span></div>
    <div class="leg"><div class="ld" style="background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.12)"></div><span style="color:#64748b">클린 + 음성 (TN)</span></div>
  </div>
  <div class="person-grid" id="personGrid"></div>
</div>

<div class="section">
  <div class="sec-title">📋 분할표 (1,000명 기준)</div>
  <table>
    <thead><tr><th></th><th>양성 판정</th><th>음성 판정</th><th>합계</th></tr></thead>
    <tbody>
      <tr><td style="font-weight:700;color:#94a3b8">도핑 선수</td><td class="hl" id="tTP">-</td><td id="tFN">-</td><td class="tot" id="tD">-</td></tr>
      <tr><td style="font-weight:700;color:#94a3b8">클린 선수</td><td id="tFP">-</td><td id="tTN">-</td><td class="tot" id="tC">-</td></tr>
      <tr><td style="font-weight:700;color:#e2e8f0">합계</td><td class="tot key" id="tTPos">-</td><td class="tot" id="tTNeg">-</td><td class="tot">1,000</td></tr>
    </tbody>
  </table>
</div>

<div class="section">
  <div class="sec-title">🎯 핵심 결과: P(도핑 | 양성 판정) = ?</div>
  <div class="big-result br-hi" id="bigResult">
    <div class="br-num" id="bigNum">-</div>
    <div class="br-lbl" id="bigLbl">양성 판정을 받은 선수가 실제로 도핑했을 확률</div>
  </div>
  <div id="insBox"></div>
  <div class="compare">
    💡 <strong>진단 키트 탭과 비교해봐요!</strong><br>
    진단 키트(감염률 0.5%, 민감도 95%, 특이도 99%)와 이 도핑 검사를 비교하면,<br>
    공통점이 보이나요? <strong>낮은 기저 확률(사전확률)</strong>이 결과에 결정적인 역할을 해요.
  </div>
</div>

<script>
function fmt(n){return n.toLocaleString();}
function fmtP(v){return (v*100).toFixed(1)+'%';}
function calc(){
  var N=1000;
  var dopRate=parseInt(document.getElementById('slDop').value)/1000;
  var sens=parseInt(document.getElementById('slSens').value)/100;
  var spec=parseInt(document.getElementById('slSpec').value)/100;
  document.getElementById('valDop').textContent=(dopRate*100).toFixed(1)+'%';
  document.getElementById('valSens').textContent=(sens*100).toFixed(0)+'%';
  document.getElementById('valSpec').textContent=(spec*100).toFixed(0)+'%';
  var doping=Math.round(N*dopRate), clean=N-doping;
  var tp=Math.round(doping*sens), fn=doping-tp;
  var tn=Math.round(clean*spec), fp=clean-tn;
  var tpos=tp+fp, tneg=fn+tn;
  document.getElementById('tTP').textContent=fmt(tp);
  document.getElementById('tFN').textContent=fmt(fn);
  document.getElementById('tD').textContent=fmt(doping);
  document.getElementById('tFP').textContent=fmt(fp);
  document.getElementById('tTN').textContent=fmt(tn);
  document.getElementById('tC').textContent=fmt(clean);
  document.getElementById('tTPos').textContent=fmt(tpos);
  document.getElementById('tTNeg').textContent=fmt(tneg);
  var pDgivenPos=tpos>0?tp/tpos:0;
  document.getElementById('bigNum').textContent=fmtP(pDgivenPos);
  var br=document.getElementById('bigResult');
  br.className=pDgivenPos<0.5?'big-result br-hi':'big-result br-ok';
  var ins='';
  if(pDgivenPos<0.3){
    ins='<div class="warn-box">⚠️ <strong>충격적인 결과!</strong> 양성 판정을 받은 '+fmt(tpos)+'명 중 실제 도핑 선수는 '+fmt(tp)+'명('+fmtP(pDgivenPos)+')뿐!<br>'+
      '나머지 '+fmt(fp)+'명은 클린한데도 양성으로 잘못 판정된 선수예요 (거짓 양성).<br>'+
      '💡 도핑 비율 슬라이더를 올려보세요! 기저 확률이 높아질수록 결과가 어떻게 달라지나요?</div>';
  } else if(pDgivenPos<0.7){
    ins='<div class="warn-box">⚠️ 양성 판정자 중 도핑 확률 '+fmtP(pDgivenPos)+'. 아직 절반 정도만 실제 도핑 선수예요.<br>'+
      '검사 정확도가 높아도 기저 확률(도핑 비율)이 낮으면 거짓 양성이 많이 나와요.</div>';
  } else {
    ins='<div class="ok-box">✅ 도핑 비율이 충분히 높아서 양성 판정의 신뢰도가 '+fmtP(pDgivenPos)+'로 높아요!<br>'+
      '사전확률(도핑 비율)이 결과에 얼마나 큰 영향을 미치는지 보이나요?</div>';
  }
  document.getElementById('insBox').innerHTML=ins;
  // Person grid (show up to 200 dots for performance)
  var grid=document.getElementById('personGrid');
  grid.innerHTML='';
  var show=Math.min(N,200);
  var scale=show/N;
  var tp2=Math.round(tp*scale), fp2=Math.round(fp*scale), fn2=Math.round(fn*scale);
  var tn2=show-tp2-fp2-fn2;
  var order=[];
  for(var i=0;i<tp2;i++) order.push('p-tp');
  for(var i=0;i<fp2;i++) order.push('p-fp');
  for(var i=0;i<fn2;i++) order.push('p-fn');
  for(var i=0;i<tn2;i++) order.push('p-tn');
  order.forEach(function(c){
    var d=document.createElement('div');d.className='p-dot '+c;grid.appendChild(d);
  });
  if(N>200){
    var note=document.createElement('div');
    note.style.cssText='width:100%;font-size:.65rem;color:#64748b;padding:2px 4px;margin-top:2px';
    note.textContent='(시각화: '+show+'개 점 = '+N+'명 비례 표시)';
    grid.appendChild(note);
  }
}
calc();
</script>
</body></html>"""


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("🔮 베이즈 정리 탐구")
    st.caption(
        "쿠키 상자 · 진단키트 · 스팸필터 · 도핑검사 4가지 상황으로 "
        "베이즈 정리의 핵심 — '새로운 증거로 확률을 합리적으로 업데이트하기'를 탐구해봐요!"
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🍪 쿠키 상자",
        "🧪 진단 키트",
        "📧 스팸 필터",
        "🏃 도핑 검사",
    ])

    with tab1:
        components.html(_HTML_TAB1, height=1400, scrolling=False)

    with tab2:
        components.html(_HTML_TAB2, height=1200, scrolling=False)

    with tab3:
        components.html(_HTML_TAB3, height=1400, scrolling=False)

    with tab4:
        components.html(_HTML_TAB4, height=1400, scrolling=False)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
