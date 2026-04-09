# activities/probability_new/mini/birthday_paradox_mini.py
"""
생일 역설 미니활동
탭1: 원리 이해 (시뮬레이션 + 수식 유도 + 확률 탐색기)
탭2: 예시 분석 (생일 표 MCQ)
탭3: 우리 반 생일 탐구 (실제 데이터 수집 + 분석)
"""
import datetime
from datetime import timezone, timedelta

import requests
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎂 생일 역설 탐구",
    "description": "우리 반에 생일이 같은 친구가 있을 확률은? 여사건의 확률로 생일 역설을 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "생일역설"
_KST = timezone(timedelta(hours=9))

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 생일 역설**"},
    {
        "key": "여사건이유",
        "label": "생일 역설 계산에서 여사건 P(Aᶜ)를 먼저 구하는 이유는 무엇인가요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "P(A)를 직접 계산하기 어려운 이유와 P(Aᶜ) = P(생일이 모두 다른 사건)을 먼저 계산하는 이유를 써보세요.",
    },
    {
        "key": "직관과차이",
        "label": "23명이면 P(A) > 50%라는 결과가 여러분의 예상과 어떻게 달랐나요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "처음에 예상한 인원 수, 실제 결과와의 차이, 그 이유...",
    },
    {
        "key": "우리반결과",
        "label": "탐구3에서 우리 반 생일 탐구 결과를 이론적 확률과 비교해 서술해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "같은 생일 쌍이 있었는지, 이론적 확률은 얼마였는지, 결과가 이론과 일치했는지...",
    },
    {
        "key": "한계점",
        "label": "이 계산에서 1년=365일, 모든 날 균등 확률로 가정했습니다. 실제와 다른 점은 무엇일까요?",
        "type": "text_area",
        "height": 80,
        "placeholder": "윤년, 생일 분포의 불균등성(예: 9~10월생이 많음), 쌍둥이 등...",
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
# TAB 1 HTML  (원리 이해)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB1 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);
  color:#e2e8f0;padding:14px 12px 24px;min-height:100vh;
}
.hdr{
  text-align:center;padding:14px 20px 10px;
  background:linear-gradient(135deg,rgba(234,179,8,.14),rgba(249,115,22,.14));
  border:1px solid rgba(234,179,8,.32);border-radius:14px;margin-bottom:12px;
}
.hdr h1{font-size:1.25rem;font-weight:700;color:#fbbf24;margin-bottom:3px}
.hdr p{font-size:.8rem;color:#94a3b8;margin-top:3px}
.section{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
  border-radius:13px;padding:13px 12px;margin-bottom:11px;
}
.sec-title{font-size:.92rem;font-weight:700;margin-bottom:8px;color:#fbbf24;display:flex;align-items:center;gap:6px}
.sec-desc{font-size:.79rem;color:#94a3b8;margin-bottom:11px;line-height:1.55}

/* Simulation */
.sim-wrap{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start}
canvas#bdCircle{display:block;border-radius:10px;background:#060c18;flex-shrink:0}
.sim-panel{flex:1;min-width:155px}
.prob-box{
  background:rgba(0,0,0,.35);border-radius:10px;padding:9px 10px;margin-bottom:7px;text-align:center;
  border:1px solid rgba(255,255,255,.08);
}
.prob-lbl{font-size:.68rem;color:#94a3b8;margin-bottom:2px}
.prob-num{font-size:1.75rem;font-weight:700;font-family:monospace;color:#22c55e;transition:color .35s}
.prob-num.mid{color:#f59e0b}.prob-num.hi{color:#ef4444}
.pbar-wrap{height:9px;background:rgba(255,255,255,.1);border-radius:5px;overflow:hidden;margin:5px 0 2px}
.pbar-fill{height:100%;border-radius:5px;background:#22c55e;transition:width .4s,background .4s;width:0%}
.pbar-ticks{display:flex;justify-content:space-between;font-size:.58rem;color:#475569}
.n-count{font-size:.79rem;color:#94a3b8;text-align:center;margin:4px 0}
.match-box{
  border-radius:7px;padding:6px 8px;font-size:.76rem;text-align:center;
  background:rgba(239,68,68,.14);border:1px solid rgba(239,68,68,.38);
  color:#fca5a5;margin-bottom:6px;line-height:1.45;
}
.act-btn{
  width:100%;padding:7px;border-radius:8px;border:none;cursor:pointer;
  background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;
  font-weight:700;font-size:.85rem;margin-bottom:5px;transition:opacity .15s;
}
.act-btn:hover{opacity:.85}.act-btn:disabled{opacity:.4;cursor:default}
.rst-btn{
  width:100%;padding:6px;border-radius:7px;border:1px solid rgba(255,255,255,.14);
  background:rgba(255,255,255,.05);color:#94a3b8;cursor:pointer;font-size:.79rem;
}
.rst-btn:hover{background:rgba(255,255,255,.09);color:#e2e8f0}
.bd-list{
  margin-top:9px;max-height:90px;overflow-y:auto;
  border:1px solid rgba(255,255,255,.07);border-radius:7px;
  padding:5px;font-size:.7rem;line-height:1.8;
}
.bd-tag{
  display:inline-block;margin:1px 3px;padding:1px 6px;
  border-radius:4px;font-family:monospace;cursor:default;
}
.bd-tag.nm{background:rgba(255,255,255,.08);color:#cbd5e1}
.bd-tag.mt{background:rgba(239,68,68,.22);color:#fca5a5;border:1px solid rgba(239,68,68,.4);font-weight:700}

/* Formula */
.step-grid{display:flex;flex-direction:column;gap:7px;margin-bottom:11px}
.step-card{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
  border-radius:9px;padding:9px 11px;display:flex;align-items:center;gap:9px;
}
.step-n{
  width:26px;height:26px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-weight:700;font-size:.8rem;
  background:rgba(234,179,8,.18);color:#fbbf24;border:1px solid rgba(234,179,8,.28);
}
.step-txt{flex:1;font-size:.81rem;color:#cbd5e1;line-height:1.5}
.blank-btn{
  padding:2px 12px;border-radius:5px;border:2px dashed rgba(99,102,241,.55);
  background:rgba(99,102,241,.1);color:#a5b4fc;cursor:pointer;
  font-size:.85rem;font-family:monospace;font-weight:700;transition:all .15s;min-width:44px;text-align:center;
}
.blank-btn:hover{border-color:rgba(99,102,241,.9);background:rgba(99,102,241,.18)}
.blank-btn.ok{
  border:2px solid rgba(34,197,94,.5);background:rgba(34,197,94,.14);
  color:#86efac;cursor:default;
}
.formula-box{
  background:rgba(0,0,0,.3);border:1px solid rgba(234,179,8,.28);
  border-radius:10px;padding:11px 13px;text-align:center;
}
.formula-box .eq{font-family:'Courier New',monospace;font-size:.83rem;color:#fde68a;line-height:2.1}
.formula-box .result{font-size:.88rem;color:#34d399;font-weight:700;margin-top:6px}

/* Graph */
.slider-row{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.slider-row label{font-size:.8rem;color:#94a3b8;white-space:nowrap}
input[type=range]{flex:1;accent-color:#eab308;cursor:pointer}
.s-val{font-size:.86rem;color:#fbbf24;font-family:monospace;font-weight:700;min-width:28px;text-align:right}
.stat-row{display:flex;gap:8px;justify-content:center;margin-bottom:8px;flex-wrap:wrap}
.stat-card{
  background:rgba(0,0,0,.28);border:1px solid rgba(255,255,255,.09);
  border-radius:9px;padding:7px 16px;text-align:center;
}
.stat-card .sv{font-size:1.45rem;font-weight:700;font-family:monospace}
.stat-card .sl{font-size:.66rem;color:#94a3b8;margin-top:2px}
canvas#gC{display:block;border-radius:8px;background:#060c18;width:100%}
.th-note{font-size:.72rem;color:#94a3b8;text-align:center;margin-top:5px}
.th-note .hl{color:#fbbf24;font-weight:700}
</style>
</head>
<body>
<div class="hdr">
  <h1>🎂 탐구1: 생일 역설 — 원리 이해</h1>
  <p>여사건 P(Aᶜ)를 먼저 구해서 P(A) = 1 − P(Aᶜ)를 탐구해봐요!</p>
</div>

<!-- Section A: Simulation -->
<div class="section">
  <div class="sec-title">🎭 시뮬레이션 — 한 명씩 방에 입장시켜 보세요!</div>
  <div class="sec-desc">버튼을 눌러 한 명씩 방에 입장시켜 보세요. 같은 생일인 친구가 언제 처음 나타날지 예상해보세요.</div>
  <div class="sim-wrap">
    <canvas id="bdCircle" width="230" height="230"></canvas>
    <div class="sim-panel">
      <div class="prob-box">
        <div class="prob-lbl">P(A) = P(같은 생일 쌍 ≥ 1쌍)</div>
        <div class="prob-num" id="probNum">0.0000</div>
        <div class="pbar-wrap"><div class="pbar-fill" id="pFill"></div></div>
        <div class="pbar-ticks"><span>0</span><span>0.5</span><span>1</span></div>
      </div>
      <div class="n-count" id="nCnt">👤 0명 입장</div>
      <div class="match-box" id="mBox" style="display:none"></div>
      <button class="act-btn" onclick="addPerson()" id="addBtn">🚶 한 명 더!</button>
      <button class="rst-btn" onclick="resetSim()">↺ 초기화</button>
    </div>
  </div>
  <div class="bd-list" id="bdList" style="display:none"></div>
</div>

<!-- Section B: Formula -->
<div class="section">
  <div class="sec-title">📐 수식 유도 — 빈칸을 눌러 확인해보세요!</div>
  <div class="sec-desc">
    <b style="color:#fde68a">사건 A</b>: 적어도 두 명의 생일이 같은 사건<br>
    <b style="color:#a5b4fc">사건 Aᶜ</b>: 모든 n명의 생일이 다른 사건 (여사건)<br><br>
    P(A) = 1 − P(Aᶜ) 이므로, P(Aᶜ)를 먼저 구해봅시다!
  </div>
  <div class="step-grid">
    <div class="step-card">
      <div class="step-n">1</div>
      <div class="step-txt">
        1번째 사람: 어떤 생일이든 OK →
        <span style="color:#fde68a;font-family:monospace;font-weight:700">365</span>/365 = 1
      </div>
    </div>
    <div class="step-card">
      <div class="step-n">2</div>
      <div class="step-txt">
        2번째 사람: 1번째와 다른 생일 →
        <button class="blank-btn" id="b1" onclick="reveal('b1','364')">?</button> / 365
      </div>
    </div>
    <div class="step-card">
      <div class="step-n">3</div>
      <div class="step-txt">
        3번째 사람: 앞 두 명과 다른 생일 →
        <button class="blank-btn" id="b2" onclick="reveal('b2','363')">?</button> / 365
      </div>
    </div>
    <div class="step-card">
      <div class="step-n">n</div>
      <div class="step-txt">
        n번째 사람: 앞 n−1명과 다른 생일 →
        <button class="blank-btn" id="b3" onclick="reveal('b3','365−n+1')">?</button> / 365
      </div>
    </div>
  </div>
  <div class="formula-box">
    <div class="eq">P(Aᶜ) = (365 × 364 × 363 × ··· × (365−n+1)) / 365ⁿ</div>
    <div class="eq">= ₃₆₅Pₙ / 365ⁿ</div>
    <div class="result">∴  P(A) = 1 − P(Aᶜ) = 1 − ₃₆₅Pₙ / 365ⁿ</div>
  </div>
</div>

<!-- Section C: Graph -->
<div class="section">
  <div class="sec-title">📊 인원 수에 따른 확률 탐색</div>
  <div class="sec-desc">슬라이더를 움직여 n명일 때 P(A)가 얼마인지 확인해보세요. P(A) > 0.5가 되는 최솟값은?</div>
  <div class="slider-row">
    <label>n =</label>
    <input type="range" id="nSl" min="2" max="80" value="20" oninput="updateGraph()">
    <span class="s-val" id="nVl">20</span>명
  </div>
  <div class="stat-row">
    <div class="stat-card"><div class="sv" id="svP" style="color:#22c55e">0.4114</div><div class="sl">P(A) 값</div></div>
    <div class="stat-card"><div class="sv" id="svC" style="color:#60a5fa">0.5886</div><div class="sl">P(Aᶜ) 값</div></div>
  </div>
  <canvas id="gC" height="155"></canvas>
  <div class="th-note" id="thNote">
    n = <span class="hl">23</span>명일 때 처음으로 P(A) > 0.5 — 이것이 바로 "생일 역설"!
  </div>
</div>

<script>
/* ── 공통 ── */
var DIM=[31,28,31,30,31,30,31,31,30,31,30,31];
var COLORS=['#60a5fa','#34d399','#a78bfa','#fb923c','#f472b6','#facc15',
            '#38bdf8','#4ade80','#c084fc','#fd8a5e','#fbcfe8','#fef08a',
            '#7dd3fc','#6ee7b7','#d8b4fe','#fdba74','#fcd34d','#a5f3fc'];
function doy(m,d){var t=d;for(var i=0;i<m-1;i++)t+=DIM[i];return t;}
function rbd(){var m=Math.floor(Math.random()*12)+1;var d=Math.floor(Math.random()*DIM[m-1])+1;
  return{m:m,d:d,doy:doy(m,d),str:(m<10?'0':'')+m+'.'+(d<10?'0':'')+d};}
function calcP(n){
  if(n<=1)return 0;if(n>=366)return 1;
  var lp=0;for(var i=0;i<n;i++)lp+=Math.log((365-i)/365);
  return 1-Math.exp(lp);
}

/* ── Simulation ── */
var cv=document.getElementById('bdCircle');
var ctx=cv.getContext('2d');
var CW=cv.width,CH=cv.height,CX=CW/2,CY=CH/2,CR=CW*0.35;
var people=[],matches=[];
function a2xy(doy){
  var a=(doy/365)*2*Math.PI-Math.PI/2;
  return{x:CX+CR*Math.cos(a),y:CY+CR*Math.sin(a)};
}
function drawCircle(){
  ctx.clearRect(0,0,CW,CH);
  ctx.fillStyle='#060c18';ctx.beginPath();ctx.arc(CX,CY,CR+16,0,2*Math.PI);ctx.fill();
  /* ring */
  ctx.beginPath();ctx.arc(CX,CY,CR,0,2*Math.PI);
  ctx.strokeStyle='rgba(148,163,184,0.22)';ctx.lineWidth=2;ctx.stroke();
  /* month ticks */
  for(var m=0;m<12;m++){
    var a=(m/12)*2*Math.PI-Math.PI/2;
    ctx.beginPath();
    ctx.moveTo(CX+(CR-5)*Math.cos(a),CY+(CR-5)*Math.sin(a));
    ctx.lineTo(CX+(CR+7)*Math.cos(a),CY+(CR+7)*Math.sin(a));
    ctx.strokeStyle='rgba(100,116,139,0.75)';ctx.lineWidth=1.5;ctx.stroke();
    var lr=CR+14;
    ctx.fillStyle='rgba(100,116,139,0.85)';ctx.font='6.5px Segoe UI';
    ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText((m+1)+'월',CX+lr*Math.cos(a),CY+lr*Math.sin(a));
  }
  /* match lines */
  matches.forEach(function(pr){
    var p1=a2xy(pr[0].doy),p2=a2xy(pr[1].doy);
    ctx.beginPath();ctx.moveTo(p1.x,p1.y);ctx.lineTo(p2.x,p2.y);
    ctx.strokeStyle='rgba(239,68,68,0.55)';ctx.lineWidth=1.5;ctx.stroke();
  });
  /* dots */
  people.forEach(function(p){
    var pos=a2xy(p.doy);
    if(p.isMatch){
      ctx.beginPath();ctx.arc(pos.x,pos.y,8,0,2*Math.PI);
      ctx.strokeStyle='rgba(239,68,68,0.45)';ctx.lineWidth=1.5;ctx.stroke();
    }
    ctx.beginPath();ctx.arc(pos.x,pos.y,p.isMatch?5.5:3.5,0,2*Math.PI);
    ctx.fillStyle=p.isMatch?'#ef4444':p.color;ctx.fill();
  });
  /* center */
  ctx.fillStyle='#475569';ctx.font='bold 11px Segoe UI';
  ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.fillText(people.length+'명',CX,CY);
}
function updateProb(){
  var p=calcP(people.length);
  var el=document.getElementById('probNum');
  el.textContent=p.toFixed(4);
  el.className='prob-num'+(p>=0.5?' hi':p>=0.25?' mid':'');
  var fill=document.getElementById('pFill');
  fill.style.width=Math.min(p*100,100)+'%';
  fill.style.background=p>=0.5?'#ef4444':p>=0.25?'#f59e0b':'#22c55e';
  document.getElementById('nCnt').textContent='👤 '+people.length+'명 입장';
}
function addPerson(){
  if(people.length>=80){document.getElementById('addBtn').disabled=true;return;}
  var bd=rbd();bd.color=COLORS[people.length%COLORS.length];bd.isMatch=false;
  var found=false;
  people.forEach(function(q){if(q.doy===bd.doy){q.isMatch=true;bd.isMatch=true;matches.push([q,bd]);found=true;}});
  people.push(bd);
  var mb=document.getElementById('mBox');
  if(found){
    var lines=matches.map(function(pr){return pr[0].str;});
    mb.innerHTML='🎉 같은 생일 발견! <b>'+[...new Set(lines)].join(', ')+'</b>';
    mb.style.display='block';
  }
  var listEl=document.getElementById('bdList');
  listEl.style.display='block';
  var sp=document.createElement('span');
  sp.className='bd-tag '+(bd.isMatch?'mt':'nm');
  sp.textContent=bd.str;sp.title=people.length+'번째';
  listEl.appendChild(sp);
  drawCircle();updateProb();
}
function resetSim(){
  people=[];matches=[];
  document.getElementById('mBox').style.display='none';
  document.getElementById('bdList').innerHTML='';
  document.getElementById('bdList').style.display='none';
  document.getElementById('addBtn').disabled=false;
  drawCircle();updateProb();
}
drawCircle();updateProb();

/* ── Formula blanks ── */
function reveal(id,val){
  var btn=document.getElementById(id);
  btn.textContent=val;btn.classList.add('ok');
}

/* ── Graph ── */
var gC=document.getElementById('gC');
var gCtx=gC.getContext('2d');
function updateGraph(){
  var n=parseInt(document.getElementById('nSl').value);
  document.getElementById('nVl').textContent=n;
  var p=calcP(n),pc=1-p;
  document.getElementById('svP').textContent=p.toFixed(4);
  document.getElementById('svC').textContent=pc.toFixed(4);
  document.getElementById('svP').style.color=p>=0.5?'#ef4444':p>=0.25?'#f59e0b':'#22c55e';
  var th=document.getElementById('thNote');
  if(p>=0.5){
    th.innerHTML='🎉 n = <span class="hl">'+n+'</span>명일 때 P(A) ≥ 0.5! 생일이 같은 쌍이 있을 확률이 더 높아요.';
  }else{
    th.innerHTML='n = <span class="hl">23</span>명일 때 처음으로 P(A) > 0.5 — 이것이 바로 "생일 역설"!';
  }
  drawGraph(n);
}
function drawGraph(selN){
  var W=gC.width,H=gC.height;
  var pl=34,pr=10,pt=12,pb=22;
  var gW=W-pl-pr,gH=H-pt-pb;
  gCtx.clearRect(0,0,W,H);
  gCtx.fillStyle='#060c18';gCtx.fillRect(0,0,W,H);
  /* axes */
  gCtx.strokeStyle='rgba(100,116,139,0.45)';gCtx.lineWidth=1;
  gCtx.beginPath();gCtx.moveTo(pl,pt);gCtx.lineTo(pl,pt+gH);gCtx.lineTo(pl+gW,pt+gH);gCtx.stroke();
  /* Y ticks */
  gCtx.fillStyle='#64748b';gCtx.font='8px Segoe UI';
  gCtx.textAlign='right';gCtx.textBaseline='middle';
  [0,0.25,0.5,0.75,1].forEach(function(v){
    var y=pt+gH*(1-v);
    gCtx.fillText(v.toFixed(2),pl-3,y);
    gCtx.strokeStyle='rgba(100,116,139,0.15)';
    gCtx.beginPath();gCtx.moveTo(pl,y);gCtx.lineTo(pl+gW,y);gCtx.stroke();
  });
  /* X ticks */
  gCtx.textAlign='center';gCtx.textBaseline='top';gCtx.fillStyle='#64748b';
  [0,20,40,60,80].forEach(function(v){
    var x=pl+(v/80)*gW;gCtx.fillText(v,x,pt+gH+3);
  });
  /* 0.5 dashed */
  var y5=pt+gH*0.5;
  gCtx.setLineDash([4,4]);gCtx.strokeStyle='rgba(234,179,8,0.5)';gCtx.lineWidth=1;
  gCtx.beginPath();gCtx.moveTo(pl,y5);gCtx.lineTo(pl+gW,y5);gCtx.stroke();
  /* n=23 dashed */
  var x23=pl+(23/80)*gW;
  gCtx.strokeStyle='rgba(234,179,8,0.38)';
  gCtx.beginPath();gCtx.moveTo(x23,pt);gCtx.lineTo(x23,pt+gH);gCtx.stroke();
  gCtx.setLineDash([]);
  gCtx.fillStyle='#fbbf24';gCtx.font='7.5px Segoe UI';
  gCtx.textAlign='center';gCtx.fillText('23',x23,pt+1);
  /* curve */
  var grad=gCtx.createLinearGradient(pl,0,pl+gW,0);
  grad.addColorStop(0,'#22c55e');grad.addColorStop(0.33,'#f59e0b');grad.addColorStop(0.65,'#ef4444');
  gCtx.beginPath();
  for(var n=2;n<=80;n++){
    var p=calcP(n);
    var x=pl+((n-2)/78)*gW,y=pt+gH*(1-p);
    n===2?gCtx.moveTo(x,y):gCtx.lineTo(x,y);
  }
  gCtx.strokeStyle=grad;gCtx.lineWidth=2;gCtx.stroke();
  /* selected dot */
  if(selN>=2&&selN<=80){
    var ps=calcP(selN);
    var xs=pl+((selN-2)/78)*gW,ys=pt+gH*(1-ps);
    gCtx.beginPath();gCtx.arc(xs,ys,5,0,2*Math.PI);
    gCtx.fillStyle='#fff';gCtx.fill();
    gCtx.strokeStyle='#fbbf24';gCtx.lineWidth=2;gCtx.stroke();
  }
}
/* init & resize */
(function(){
  function rsz(){gC.width=Math.max(gC.parentElement.clientWidth-4,280);drawGraph(parseInt(document.getElementById('nSl').value));}
  rsz();window.addEventListener('resize',rsz);
})();
updateGraph();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 HTML  (예시 분석)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB2 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);
  color:#e2e8f0;padding:14px 12px 24px;min-height:100vh;
}
.hdr{
  text-align:center;padding:14px 20px 10px;
  background:linear-gradient(135deg,rgba(139,92,246,.14),rgba(59,130,246,.14));
  border:1px solid rgba(139,92,246,.3);border-radius:14px;margin-bottom:12px;
}
.hdr h1{font-size:1.2rem;font-weight:700;color:#a78bfa;margin-bottom:3px}
.hdr p{font-size:.79rem;color:#94a3b8}
.section{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:13px;padding:13px 12px;margin-bottom:11px;}
.sec-title{font-size:.9rem;font-weight:700;margin-bottom:9px;color:#a78bfa;display:flex;align-items:center;gap:6px}
.sec-desc{font-size:.78rem;color:#94a3b8;margin-bottom:10px;line-height:1.55}

/* Score */
.score-bar{display:flex;gap:9px;justify-content:center;margin-bottom:11px;flex-wrap:wrap}
.sc{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:9px;padding:6px 16px;text-align:center}
.sc .num{font-size:1.3rem;font-weight:700}.sc .lbl{font-size:.64rem;color:#94a3b8}
.sc-ok .num{color:#34d399}.sc-tot .num{color:#60a5fa}

/* Birthday table */
.legend{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px;font-size:.75rem}
.leg-item{display:flex;align-items:center;gap:5px}
.leg-dot{width:12px;height:12px;border-radius:3px;flex-shrink:0}
.bd-table{width:100%;border-collapse:collapse;margin-bottom:8px}
.bd-table td{
  padding:6px 8px;text-align:center;
  border:1px solid rgba(255,255,255,.09);
  font-family:monospace;font-size:.84rem;
  background:rgba(255,255,255,.04);color:#cbd5e1;
}
.bd-table td.c-or{background:rgba(245,158,11,.28);color:#fef3c7;border-color:rgba(245,158,11,.45);font-weight:700}
.bd-table td.c-gn{background:rgba(34,197,94,.2);color:#dcfce7;border-color:rgba(34,197,94,.38);font-weight:700}
.bd-table td.c-yw{background:rgba(234,179,8,.22);color:#fef9c3;border-color:rgba(234,179,8,.38);font-weight:700}
.bd-table td.empty{background:rgba(0,0,0,.08);border-color:rgba(255,255,255,.04);color:transparent}

/* MCQ */
.q-card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:11px;padding:12px 13px;margin-bottom:9px}
.q-card.qok{border-color:rgba(52,211,153,.4);background:rgba(52,211,153,.06)}
.q-card.qng{border-color:rgba(239,68,68,.35);background:rgba(239,68,68,.05)}
.q-num{font-size:.72rem;color:#a78bfa;font-weight:700;margin-bottom:5px}
.q-text{font-size:.84rem;color:#e2e8f0;margin-bottom:9px;line-height:1.5}
.choices{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:7px}
.cbtn{
  padding:5px 14px;border-radius:7px;border:1px solid rgba(255,255,255,.14);
  background:rgba(255,255,255,.06);color:#cbd5e1;cursor:pointer;font-size:.8rem;transition:all .15s;
}
.cbtn:hover{background:rgba(139,92,246,.2);border-color:rgba(139,92,246,.5);color:#ddd6fe}
.cbtn:disabled{cursor:default;opacity:.8}
.cbtn.ok{background:rgba(52,211,153,.2);border-color:rgba(52,211,153,.55);color:#6ee7b7;font-weight:700}
.cbtn.ng{background:rgba(239,68,68,.18);border-color:rgba(239,68,68,.45);color:#fca5a5}
.cbtn.reveal{background:rgba(52,211,153,.15);border-color:rgba(52,211,153,.4);color:#6ee7b7}
.fb{font-size:.77rem;border-radius:7px;padding:7px 9px;line-height:1.5;display:none}
.fb.show{display:block}
.fb.fok{background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.3);color:#a7f3d0}
.fb.fng{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.28);color:#fecaca}
</style>
</head>
<body>
<div class="hdr">
  <h1>📋 탐구2: 예시 분석 — 생일 표 탐구</h1>
  <p>실제 한 학급 34명의 생일 데이터를 보고 질문에 답해보세요!</p>
</div>

<!-- Score -->
<div class="score-bar">
  <div class="sc sc-ok"><div class="num" id="scOk">0</div><div class="lbl">정답</div></div>
  <div class="sc sc-tot"><div class="num">5</div><div class="lbl">전체 문제</div></div>
</div>

<!-- Birthday table -->
<div class="section">
  <div class="sec-title">📅 한 학급 34명의 생일 표</div>
  <div class="legend">
    <div class="leg-item"><div class="leg-dot" style="background:#f59e0b"></div><span>08.14 쌍</span></div>
    <div class="leg-item"><div class="leg-dot" style="background:#22c55e"></div><span>04.04 쌍</span></div>
    <div class="leg-item"><div class="leg-dot" style="background:#eab308"></div><span>02.14 쌍</span></div>
  </div>
  <table class="bd-table">
    <tr><td>12.12</td><td>10.11</td><td class="c-or">08.14</td><td class="c-gn">04.04</td></tr>
    <tr><td>12.23</td><td>06.25</td><td>11.16</td><td>11.14</td></tr>
    <tr><td class="c-yw">02.14</td><td>08.30</td><td>07.09</td><td>01.12</td></tr>
    <tr><td class="c-gn">04.04</td><td>04.03</td><td>01.17</td><td>10.02</td></tr>
    <tr><td>12.31</td><td>05.07</td><td>05.24</td><td>02.01</td></tr>
    <tr><td class="c-yw">02.14</td><td>07.02</td><td>11.02</td><td>07.14</td></tr>
    <tr><td>06.14</td><td>04.10</td><td>08.06</td><td>03.10</td></tr>
    <tr><td>11.07</td><td>02.05</td><td>04.12</td><td class="empty">-</td></tr>
    <tr><td class="c-or">08.14</td><td>01.06</td><td>06.13</td><td class="empty">-</td></tr>
  </table>
</div>

<!-- Questions -->
<div class="section">
  <div class="sec-title">❓ 탐구 문제</div>

  <!-- Q1 -->
  <div class="q-card" id="qc1">
    <div class="q-num">문제 1</div>
    <div class="q-text">위 표에 기록된 학생은 총 몇 명인가요?</div>
    <div class="choices">
      <button class="cbtn" data-ok="0" onclick="ans(1,this)">30명</button>
      <button class="cbtn" data-ok="0" onclick="ans(1,this)">32명</button>
      <button class="cbtn" data-ok="1" onclick="ans(1,this)">34명</button>
      <button class="cbtn" data-ok="0" onclick="ans(1,this)">36명</button>
    </div>
    <div class="fb" id="fb1">✅ 정답! 4열 × 7행 + 3명 × 2행 = 28 + 6 = 34명입니다.</div>
  </div>

  <!-- Q2 -->
  <div class="q-card" id="qc2">
    <div class="q-num">문제 2</div>
    <div class="q-text">위 표에서 생일이 같은 학생 쌍은 총 몇 쌍인가요? (색 표시 참고)</div>
    <div class="choices">
      <button class="cbtn" data-ok="0" onclick="ans(2,this)">1쌍</button>
      <button class="cbtn" data-ok="0" onclick="ans(2,this)">2쌍</button>
      <button class="cbtn" data-ok="1" onclick="ans(2,this)">3쌍</button>
      <button class="cbtn" data-ok="0" onclick="ans(2,this)">4쌍</button>
    </div>
    <div class="fb" id="fb2">✅ 정답! 08.14 쌍, 04.04 쌍, 02.14 쌍으로 총 3쌍입니다.</div>
  </div>

  <!-- Q3 -->
  <div class="q-card" id="qc3">
    <div class="q-num">문제 3</div>
    <div class="q-text">다음 중 표에서 생일이 같은 학생이 <b>없는</b> 날짜는?</div>
    <div class="choices">
      <button class="cbtn" data-ok="0" onclick="ans(3,this)">04.04</button>
      <button class="cbtn" data-ok="0" onclick="ans(3,this)">02.14</button>
      <button class="cbtn" data-ok="0" onclick="ans(3,this)">08.14</button>
      <button class="cbtn" data-ok="1" onclick="ans(3,this)">11.14</button>
    </div>
    <div class="fb" id="fb3">✅ 정답! 11.14는 2행 4열에 한 명뿐이고 같은 생일 학생이 없습니다.<br>04.04·02.14·08.14는 각각 2명씩 있어요.</div>
  </div>

  <!-- Q4 -->
  <div class="q-card" id="qc4">
    <div class="q-num">문제 4</div>
    <div class="q-text">34명 집단에서 적어도 두 명의 생일이 같을 <b>이론적 확률</b>에 가장 가까운 값은?<br><small style="color:#64748b">(P(A) = 1 − ₃₆₅P₃₄ / 365³⁴)</small></div>
    <div class="choices">
      <button class="cbtn" data-ok="0" onclick="ans(4,this)">약 50%</button>
      <button class="cbtn" data-ok="0" onclick="ans(4,this)">약 65%</button>
      <button class="cbtn" data-ok="1" onclick="ans(4,this)">약 80%</button>
      <button class="cbtn" data-ok="0" onclick="ans(4,this)">약 95%</button>
    </div>
    <div class="fb" id="fb4">✅ 정답! n=34일 때 P(A) ≈ 0.7953 → 약 80%입니다.<br>실제로 3쌍이나 발견된 것이 수학적으로 자연스러운 결과예요!</div>
  </div>

  <!-- Q5 -->
  <div class="q-card" id="qc5">
    <div class="q-num">문제 5</div>
    <div class="q-text">적어도 두 명의 생일이 같을 확률이 처음으로 <b>50%를 넘는</b> 최소 인원은?</div>
    <div class="choices">
      <button class="cbtn" data-ok="0" onclick="ans(5,this)">18명</button>
      <button class="cbtn" data-ok="0" onclick="ans(5,this)">20명</button>
      <button class="cbtn" data-ok="1" onclick="ans(5,this)">23명</button>
      <button class="cbtn" data-ok="0" onclick="ans(5,this)">30명</button>
    </div>
    <div class="fb" id="fb5">✅ 정답! n=22일 때 P(A) ≈ 0.476, n=23일 때 P(A) ≈ 0.507 → 23명부터 50% 초과!<br>이것이 생일 역설의 핵심 — 생각보다 적은 인원이에요.</div>
  </div>
</div>

<script>
var score=0,done={};
function addScore(ok){if(ok)score++;document.getElementById('scOk').textContent=score;}
function ans(n,btn){
  if(done[n])return;done[n]=true;
  var ok=btn.getAttribute('data-ok')==='1';
  var card=document.getElementById('qc'+n);
  var fb=document.getElementById('fb'+n);
  var btns=card.querySelectorAll('.cbtn');
  btns.forEach(function(b){b.disabled=true;if(b.getAttribute('data-ok')==='1')b.classList.add('reveal');});
  if(ok){btn.classList.add('ok');card.classList.add('qok');fb.className='fb show fok';}
  else{
    btn.classList.add('ng');card.classList.add('qng');
    fb.className='fb show fng';
    fb.innerHTML='❌ 틀렸어요! '+fb.innerHTML.replace('✅ 정답! ','');
  }
  addScore(ok);
}
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 Python  (우리 반 생일 탐구)
# ─────────────────────────────────────────────────────────────────────────────
_BD_SHEET_NAME = _SHEET_NAME + "_생일"
_BD_HEADER = ["제출시각", "학번", "이름", "생일"]


def _get_or_create_birthday_ws():
    """생일 데이터 워크시트를 반환합니다. 없으면 자동 생성합니다."""
    import gspread
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    gc = gspread.authorize(creds)
    sheet_id = st.secrets.get("reflection_spreadsheet_probability_new", "")
    if not sheet_id:
        raise ValueError("`reflection_spreadsheet_probability_new` secret 없음")
    sh = gc.open_by_key(sheet_id)
    try:
        ws = sh.worksheet(_BD_SHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=_BD_SHEET_NAME, rows=2000, cols=4)
        ws.append_row(_BD_HEADER)
    return ws


@st.cache_data(ttl=60, show_spinner=False)
def _load_birthday_data(_cache_key: int = 0):
    try:
        ws = _get_or_create_birthday_ws()
        records = ws.get_all_records()
        if not records:
            return None, None
        import pandas as pd
        return pd.DataFrame(records), None
    except Exception as e:
        return None, str(e)


def _save_birthday(short_id: str, student_name: str, birthday_str: str) -> str | None:
    """생일을 gspread로 직접 저장합니다. 성공 시 None, 실패 시 에러 메시지 반환."""
    try:
        ws = _get_or_create_birthday_ws()
        now_str = datetime.datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now_str, short_id, student_name, birthday_str])
        return None
    except Exception as e:
        return str(e)


def _render_birthday_collection():
    st.markdown("### 🏫 탐구3: 우리 반 생일 탐구")
    st.info(
        "📌 **데이터는 어디에 저장되나요?**  \n"
        "여러분이 입력한 생일은 이 앱과 연결된 **Google 스프레드시트**의 "
        f"`{_BD_SHEET_NAME}` 시트에 직접 저장됩니다. "
        "시트가 없으면 자동으로 만들어집니다! 🗂️"
    )

    student_id = st.session_state.get("_user_id", "")
    student_name = st.session_state.get("_user_name", "")

    if not student_id:
        st.warning("📋 로그인 후 참여할 수 있습니다.")
        return

    short_id = (
        student_id[4:]
        if len(student_id) >= 9 and student_id[:2] == "20"
        else student_id
    )

    st.markdown(f"**학번**: `{student_id}`　**이름**: **{student_name}**")
    st.markdown("---")
    st.markdown("#### 🎂 내 생일 입력하기")

    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox(
            "월 선택", range(1, 13),
            format_func=lambda x: f"{x}월",
            key="bd_month_sel",
        )
    with col2:
        max_day = days_in_month[month - 1]
        day = st.selectbox(
            "일 선택", range(1, max_day + 1),
            format_func=lambda x: f"{x}일",
            key="bd_day_sel",
        )

    birthday_str = f"{month:02d}.{day:02d}"
    st.caption(f"입력할 생일: **{birthday_str}**")

    if st.button("🎂 생일 등록하기", type="primary", key="bd_submit_btn"):
        err = _save_birthday(short_id, student_name, birthday_str)
        if err is None:
            st.success(f"✅ {student_name}님의 생일 **{birthday_str}**이(가) 등록되었습니다!")
            st.cache_data.clear()
        else:
            st.error(f"저장 오류: {err}")

    st.markdown("---")

    # ── Analysis ──
    col_h, col_btn = st.columns([6, 1])
    with col_h:
        st.markdown("#### 📊 우리 반 생일 분석 결과")
    with col_btn:
        if st.button("🔄", key="bd_refresh_btn", help="새로고침"):
            st.cache_data.clear()
            st.rerun()

    df, err = _load_birthday_data(st.session_state.get("_bd_cache_key", 0))

    if err:
        st.error(f"데이터 로드 오류: {err}")
        return

    if df is None or df.empty:
        st.info("아직 등록된 생일이 없습니다. 첫 번째로 등록해보세요! 🎉")
        return

    import math
    from collections import Counter

    # 중복 제거: 학번당 최신 생일만 사용
    if "학번" in df.columns and "생일" in df.columns:
        df_latest = df.drop_duplicates(subset=["학번"], keep="last")
    else:
        df_latest = df

    n = len(df_latest)
    bd_counts = Counter(df_latest["생일"].astype(str).tolist())
    matching = {d: c for d, c in bd_counts.items() if c >= 2}
    total_pairs = sum((c * (c - 1)) // 2 for c in matching.values())

    # 이론적 확률
    log_pc = sum(math.log((365 - i) / 365) for i in range(min(n, 365)))
    p_theory = 1 - math.exp(log_pc) if n < 366 else 1.0

    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("👥 참여 인원", f"{n}명")
    m2.metric("🎂 같은 생일 쌍", f"{total_pairs}쌍")
    m3.metric("📊 이론적 확률 P(A)", f"{p_theory:.1%}")

    if total_pairs > 0:
        st.success("🎉 **같은 생일을 가진 학생들이 발견되었습니다!**")
        for date, count in sorted(matching.items()):
            names = df_latest[df_latest["생일"].astype(str) == date]["이름"].tolist()
            st.markdown(f"- **{date}** — {', '.join(names)} ({count}명)")
    else:
        if p_theory >= 0.5:
            st.warning(
                f"⚠️ 이론적으로 같은 생일 쌍이 있을 확률이 **{p_theory:.1%}**인데, "
                "아직 발견되지 않았네요! 더 많은 학생이 입력하면 달라질 수 있어요."
            )
        else:
            st.info(
                f"아직 같은 생일 쌍이 없습니다. "
                f"(현재 {n}명 참여, 이론적 확률 {p_theory:.1%})"
            )

    # Full list
    with st.expander("📋 전체 생일 목록 보기"):
        import pandas as pd
        disp = df_latest[["이름", "생일"]].sort_values("생일").reset_index(drop=True)
        disp.index += 1
        st.dataframe(disp, use_container_width=True)

    # 탐구 질문
    st.markdown("---")
    st.markdown(
        "**🔍 탐구해보세요!**\n"
        "1. 현재 학급 인원(n명)에서 이론적으로 예상되는 확률 P(A)는 얼마인가요?\n"
        "2. 실제 결과는 이론과 일치하나요? 왜 그럴까요?\n"
        "3. 생일 분포가 365일에 균등하지 않다면 확률이 어떻게 달라질까요?"
    )


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("🎂 생일 역설 탐구")
    st.caption(
        "우리 반에 생일이 같은 친구가 있을 확률은? "
        "여사건의 확률 P(A) = 1 − P(Aᶜ)을 활용해 생일 역설을 탐구해봐요!"
    )

    tab1, tab2, tab3 = st.tabs([
        "🎭 탐구1: 원리 이해",
        "📋 탐구2: 예시 분석",
        "🏫 탐구3: 우리 반 탐구",
    ])

    with tab1:
        components.html(_HTML_TAB1, height=1220, scrolling=False)

    with tab2:
        components.html(_HTML_TAB2, height=1550, scrolling=False)

    with tab3:
        _render_birthday_collection()

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
