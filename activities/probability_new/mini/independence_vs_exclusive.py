import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "미니: 독립과 배반 탐구",
    "description": "배반 vs 독립 분류 게임, 독립의 성질 시각화, 독립의 비추이성(삼단논법 불성립) 탐구",
    "hidden": True,
    "order": 9999999,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "독립과배반탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 독립과 배반 탐구**"},
    {
        "key": "배반vs독립",
        "label": "배반(A∩B=∅)과 독립(P(A∩B)=P(A)P(B))은 어떻게 다른가요? \"배반이면 종속이다\"가 참인 이유를 자신의 말로 설명해보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "배반이면 P(B|A)=0이 되는데...",
    },
    {
        "key": "혼동이유",
        "label": "많은 학생들이 배반을 독립과 혼동합니다. 왜 그런 착각이 생길까요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "두 개념의 어떤 점이 혼동을 유발하나요?",
    },
    {
        "key": "독립4쌍",
        "label": "A와 B가 독립이면 (A, Bᶜ), (Aᶜ, B), (Aᶜ, Bᶜ)도 모두 독립입니다. 확률 사각형과 연결 지어 설명해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "격자 구조에서 각 칸의 넓이는...",
    },
    {
        "key": "비추이성",
        "label": "A,B 독립 + B,C 독립이어도 A,C가 종속일 수 있습니다. 주사위 예시에서 왜 그런지 설명해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "A={홀수}, B={3,4}, C={소수}에서 A∩C를 계산해보면...",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 새롭게 알게 된 점",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 활동을 마친 후 느낀 점",
        "type": "text_area",
        "height": 80,
    },
]

# ──────────────────────────────────────────────────────────────────────────────
# Tab 1: 배반 vs 독립 분류 게임
# ──────────────────────────────────────────────────────────────────────────────

_TAB1_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;background:#0e1117;color:#e0e0e0;padding:14px;font-size:14px;line-height:1.5}
.hd{color:#90caf9;font-size:17px;font-weight:bold;margin-bottom:4px}
.sub{color:#78909c;font-size:12px;margin-bottom:14px}
.sbar{background:#1e2335;border:1px solid #2d3548;border-radius:10px;padding:10px 16px;display:flex;align-items:center;gap:18px;margin-bottom:14px;flex-wrap:wrap}
.sv{font-weight:bold;font-size:20px}.gold{color:#ffd54f}.grn{color:#a5d6a7}.red{color:#ef9a9a}
.rbtn{margin-left:auto;background:#455a64;color:#eee;border:none;padding:7px 15px;border-radius:8px;cursor:pointer;font-size:13px}
.rbtn:hover{background:#607d8b}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}
.card{background:#1a1f2e;border:2px solid #2d3548;border-radius:12px;padding:15px;transition:border-color .3s}
.card.ok{border-color:#4caf50}.card.bad{border-color:#ef5350}
.ctit{font-size:14px;font-weight:bold;color:#64b5f6;margin-bottom:3px}
.cctx{font-size:11px;color:#90caf9;margin-bottom:9px}
.ebox{background:#1e2740;border-radius:8px;padding:10px 12px;margin-bottom:10px}
.ea{color:#ef9a9a;font-size:13px;margin-bottom:2px}
.eb{color:#90caf9;font-size:13px;margin-bottom:6px}
.ei{color:#78909c;font-size:11px}
.btns{display:flex;gap:8px;flex-wrap:wrap}
.btn{padding:7px 13px;border-radius:8px;border:none;cursor:pointer;font-size:12px;font-weight:bold;transition:opacity .15s,transform .1s}
.btn:hover:not(:disabled){opacity:.82;transform:scale(1.05)}
.btn:disabled{opacity:.4;cursor:default;transform:none}
.br{background:#ef5350;color:#fff}.bb{background:#42a5f5;color:#000}.bg{background:#78909c;color:#fff}
.fb{margin-top:10px;padding:8px 12px;border-radius:8px;font-size:12px;display:none;line-height:1.55}
.fb.ok{background:#1b5e20;color:#c8e6c9}.fb.bad{background:#7f0000;color:#ffcdd2}
.sum{margin-top:18px;background:#111827;border:1px solid #1e3a5f;border-radius:10px;padding:16px 18px;display:none}
.stit{color:#ffd54f;font-size:15px;font-weight:bold;margin-bottom:10px}
.kp{border-left:4px solid #42a5f5;background:#0d1e33;padding:9px 13px;border-radius:0 6px 6px 0;margin-bottom:8px;font-size:13px;color:#cfd8dc;line-height:1.6}
.kp.warn{border-left-color:#ff8f00}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:bold;margin-right:4px}
.b-r{background:#ef5350;color:#fff}.b-b{background:#42a5f5;color:#000}.b-g{background:#78909c;color:#fff}
</style></head><body>
<div class="hd">사건 분류 게임: 배반? 독립? 종속?</div>
<div class="sub">두 사건 A, B의 관계를 판단하고 버튼을 눌러보세요!</div>
<div class="sbar">
  <div>점수 <span class="sv gold" id="sc">0</span><span style="color:#aaa">/6</span></div>
  <div>✅ 정답 <span class="sv grn" id="cc">0</span></div>
  <div>❌ 오답 <span class="sv red" id="wc">0</span></div>
  <button class="rbtn" id="resetBtn">🔄 다시하기</button>
</div>
<div class="grid" id="grid"></div>
<div class="sum" id="sum">
  <div class="stit">🔑 핵심 정리</div>
  <div class="kp">
    <span class="badge b-r">배반</span> A∩B = ∅ — 두 사건이 동시에 일어날 수 없다.<br>
    → P(B|A) = 0 이므로, P(B) > 0이면 P(B|A) ≠ P(B) <b>→ 배반이면 반드시 종속!</b>
  </div>
  <div class="kp">
    <span class="badge b-b">독립</span> P(A∩B) = P(A)·P(B) — 한 사건이 다른 사건의 확률에 영향 없음.<br>
    → A∩B ≠ ∅ 가능! 즉, <b>겹쳐도 됩니다.</b>
  </div>
  <div class="kp warn">⚠️ <b>배반 ≠ 독립</b> — 완전히 다른 개념!<br>
    배반 → 반드시 종속 &nbsp;|&nbsp; 독립 → 반드시 A∩B ≠ ∅ (P(A),P(B)>0인 경우)</div>
</div>
<script>
var S=[
  {title:"🎲 시나리오 1",ctx:"주사위 한 번 던지기",
   a:"A = {2, 4, 6} &nbsp; (짝수)",b:"B = {1, 3, 5} &nbsp; (홀수)",
   info:"A∩B = ∅ &nbsp;|&nbsp; P(A)=1/2 &nbsp; P(B)=1/2",
   ans:"r",ex:"A∩B=∅ → 배반! P(B|A)=0 ≠ P(B)=1/2 이므로 종속입니다."},
  {title:"🎲 시나리오 2",ctx:"주사위 한 번 던지기",
   a:"A = {2, 4, 6} &nbsp; (짝수)",b:"B = {3, 6} &nbsp; (3의 배수)",
   info:"A∩B = {6} &nbsp;|&nbsp; P(A)=1/2, P(B)=1/3, P(A∩B)=1/6",
   ans:"b",ex:"P(A∩B)=1/6 = (1/2)×(1/3) = P(A)P(B) ✓ → 서로 독립!"},
  {title:"🎲 시나리오 3",ctx:"주사위 한 번 던지기",
   a:"A = {1, 2, 3} &nbsp; (3 이하)",b:"B = {1, 2, 3, 4} &nbsp; (4 이하)",
   info:"A∩B = {1,2,3} &nbsp;|&nbsp; P(A)=1/2, P(B)=2/3, P(A∩B)=1/2",
   ans:"g",ex:"P(A∩B)=1/2 ≠ P(A)P(B)=1/3 → 종속! A⊂B이므로 A가 일어나면 B는 반드시 일어납니다."},
  {title:"🪙 시나리오 4",ctx:"동전 한 번 던지기",
   a:"A = {앞면}",b:"B = {뒷면}",
   info:"A∩B = ∅ &nbsp;|&nbsp; P(A)=1/2, P(B)=1/2",
   ans:"r",ex:"A∩B=∅ → 배반! 앞면이 나오면 뒷면이 절대 나올 수 없습니다 → 종속."},
  {title:"🃏 시나리오 5",ctx:"트럼프 카드 52장에서 1장 뽑기",
   a:"A = 하트 &nbsp; (13장)",b:"B = K (킹) &nbsp; (4장)",
   info:"A∩B = 하트K (1장) &nbsp;|&nbsp; P(A)=1/4, P(B)=1/13, P(A∩B)=1/52",
   ans:"b",ex:"P(A∩B)=1/52 = (1/4)×(1/13) = P(A)P(B) ✓ → 독립! 무늬와 숫자는 서로 무관합니다."},
  {title:"🎲 시나리오 6",ctx:"주사위 한 번 던지기",
   a:"A = {2, 3, 5} &nbsp; (소수)",b:"B = {2, 4, 6} &nbsp; (짝수)",
   info:"A∩B = {2} &nbsp;|&nbsp; P(A)=1/2, P(B)=1/2, P(A∩B)=1/6",
   ans:"g",ex:"P(A∩B)=1/6 ≠ P(A)P(B)=1/4 → 종속! 겹치지만(A∩B≠∅) 독립은 아닌 대표 사례!"}
];
var done=new Array(6).fill(false),cc=0,wc=0;

function pick(i,c){
  if(done[i])return;done[i]=true;
  var s=S[i];
  var card=document.getElementById('cd'+i);
  var fb=document.getElementById('fb'+i);
  var btns=document.getElementById('br'+i).querySelectorAll('button');
  for(var k=0;k<btns.length;k++) btns[k].disabled=true;
  if(c===s.ans){card.classList.add('ok');fb.className='fb ok';fb.textContent='✅ 정답! '+s.ex;cc++;}
  else{card.classList.add('bad');fb.className='fb bad';fb.textContent='❌ 틀렸어요. '+s.ex;wc++;}
  fb.style.display='block';
  document.getElementById('sc').textContent=cc;
  document.getElementById('cc').textContent=cc;
  document.getElementById('wc').textContent=wc;
  var allDone=true;for(var j=0;j<done.length;j++){if(!done[j])allDone=false;}
  if(allDone) document.getElementById('sum').style.display='block';
}

function build(){
  var g=document.getElementById('grid');g.innerHTML='';
  for(var i=0;i<S.length;i++){
    (function(idx){
      var s=S[idx];
      var d=document.createElement('div');
      d.className='card';d.id='cd'+idx;
      d.innerHTML='<div class="ctit">'+s.title+'</div>'
        +'<div class="cctx">'+s.ctx+'</div>'
        +'<div class="ebox"><div class="ea">'+s.a+'</div><div class="eb">'+s.b+'</div><div class="ei">'+s.info+'</div></div>'
        +'<div class="btns" id="br'+idx+'"></div>'
        +'<div class="fb" id="fb'+idx+'"></div>';
      g.appendChild(d);
      var btns=document.getElementById('br'+idx);
      var b1=document.createElement('button');b1.className='btn br';b1.textContent='🔴 배반';
      b1.addEventListener('click',function(){pick(idx,'r');});
      var b2=document.createElement('button');b2.className='btn bb';b2.textContent='🔵 독립';
      b2.addEventListener('click',function(){pick(idx,'b');});
      var b3=document.createElement('button');b3.className='btn bg';b3.textContent='⬜ 종속';
      b3.addEventListener('click',function(){pick(idx,'g');});
      btns.appendChild(b1);btns.appendChild(b2);btns.appendChild(b3);
    })(i);
  }
  document.getElementById('sum').style.display='none';
}

function resetGame(){
  done=new Array(6).fill(false);cc=0;wc=0;
  document.getElementById('sc').textContent=0;
  document.getElementById('cc').textContent=0;
  document.getElementById('wc').textContent=0;
  build();
}

document.getElementById('resetBtn').addEventListener('click',resetGame);
build();
</script></body></html>"""

# ──────────────────────────────────────────────────────────────────────────────
# Tab 2: 독립의 성질 — 확률 사각형 + 4쌍 확인
# ──────────────────────────────────────────────────────────────────────────────

_TAB2_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;background:#0e1117;color:#e0e0e0;padding:14px;font-size:14px;line-height:1.5}
.hd{color:#90caf9;font-size:17px;font-weight:bold;margin-bottom:4px}
.sub{color:#78909c;font-size:12px;margin-bottom:14px}
.ctrl-box{background:#1a1f2e;border:1px solid #2d3548;border-radius:10px;padding:14px 18px;margin-bottom:16px;display:flex;gap:32px;flex-wrap:wrap;align-items:flex-end}
.ctrl-item{display:flex;flex-direction:column;gap:6px}
.ctrl-label{font-size:13px;color:#90caf9}
.ctrl-val{font-size:20px;font-weight:bold;color:#ffd54f;text-align:center;min-width:50px}
input[type=range]{width:200px;accent-color:#42a5f5;cursor:pointer}
/* 핵심: Y축을 flex 형제 컬럼으로 — 절대위치 제거 */
.viz-outer{display:flex;gap:12px;align-items:flex-start;flex-wrap:nowrap;margin-bottom:16px}
.y-col{width:76px;flex-shrink:0;display:flex;flex-direction:column}
.y-seg{display:flex;align-items:center;justify-content:flex-end;padding-right:5px;font-size:11px;color:#ffd54f;font-weight:bold;white-space:nowrap}
.rect-col{flex-shrink:0}
#rectDiv{position:relative;width:360px;height:340px;border-radius:8px;overflow:hidden;border:1px solid #444}
.rg{position:absolute;display:flex;align-items:center;justify-content:center;flex-direction:column;transition:all .25s}
.axis-x{display:flex;width:360px;margin-top:5px}
.ax-seg{text-align:center;font-size:11px;color:#ffd54f;font-weight:bold;overflow:hidden;white-space:nowrap}
.axis-label-x{font-size:11px;color:#90a4ae;margin-top:3px;text-align:center;width:360px}
.props-box{background:#1a1f2e;border:1px solid #2d3548;border-radius:10px;padding:12px;flex-shrink:0;width:185px}
.props-title{color:#64b5f6;font-weight:bold;font-size:13px;margin-bottom:8px}
.prop-row{background:#0d1e33;border-radius:8px;padding:7px 10px;margin-bottom:6px;font-size:11px;line-height:1.6}
.pair{color:#ffd54f;font-weight:bold;font-size:12px}
.chk{color:#a5d6a7;font-weight:bold}
.note{background:#0d2137;border-left:4px solid #ffd54f;border-radius:0 8px 8px 0;padding:12px 16px;font-size:13px;color:#cfd8dc;line-height:1.7}
.note b{color:#ffd54f}
</style></head><body>
<div class="hd">독립의 성질: 독립이면 4쌍 모두 독립!</div>
<div class="sub">슬라이더로 P(A)와 P(B)를 바꿔보세요. A와 B가 독립이면, 아래 4쌍이 모두 독립임을 확인하세요.</div>

<div class="ctrl-box">
  <div class="ctrl-item">
    <div class="ctrl-label">P(A)</div>
    <input type="range" id="slA" min="10" max="90" value="40" oninput="update()">
    <div class="ctrl-val" id="valA">0.40</div>
  </div>
  <div class="ctrl-item">
    <div class="ctrl-label">P(B)</div>
    <input type="range" id="slB" min="10" max="90" value="30" oninput="update()">
    <div class="ctrl-val" id="valB">0.30</div>
  </div>
  <div style="font-size:12px;color:#546e7a;align-self:center;padding-bottom:4px">
    ※ A와 B가 독립일 때 확률 사각형
  </div>
</div>

<!-- Y축을 flex 형제로 배치: 절대위치 없음 → 클리핑 없음 -->
<div class="viz-outer">
  <div class="y-col" id="yCol">
    <div class="y-seg" id="ySeg1" style="height:238px">P(B)=0.30</div>
    <div class="y-seg" id="ySeg2" style="height:102px">P(Bᶜ)=0.70</div>
  </div>
  <div class="rect-col">
    <div id="rectDiv">
      <div class="rg" id="r1" style="background:#1565c0;left:0;top:0"></div>
      <div class="rg" id="r2" style="background:#4a148c;top:0"></div>
      <div class="rg" id="r3" style="background:#1b5e20;left:0"></div>
      <div class="rg" id="r4" style="background:#4e342e"></div>
    </div>
    <div class="axis-x" id="axisX"></div>
    <div class="axis-label-x">← A → | ← Aᶜ →</div>
  </div>
  <div class="props-box">
    <div class="props-title">📋 4쌍 독립 확인</div>
    <div id="props"></div>
  </div>
</div>

<div class="note" id="note"></div>

<script>
var RW=360,RH=340;
function update(){
  var pa=parseInt(document.getElementById('slA').value)/100;
  var pb=parseInt(document.getElementById('slB').value)/100;
  document.getElementById('valA').textContent=pa.toFixed(2);
  document.getElementById('valB').textContent=pb.toFixed(2);
  var pac=1-pa,pbc=1-pb;
  var xd=pa*RW, yd=(1-pb)*RH;

  // Y축 레이블 (flex 형제 → 클리핑 없음)
  var s1=document.getElementById('ySeg1');
  s1.style.height=yd+'px';
  s1.textContent='P(B)='+pb.toFixed(2);
  var s2=document.getElementById('ySeg2');
  s2.style.height=(RH-yd)+'px';
  s2.textContent='P(B\u1D9C)='+pbc.toFixed(2);

  // 4개 영역
  var r1=document.getElementById('r1');
  r1.style.cssText='background:#1565c0;position:absolute;left:0;top:0;width:'+xd+'px;height:'+yd+'px;display:flex;align-items:center;justify-content:center;flex-direction:column;';
  r1.innerHTML='<div style="font-size:12px;font-weight:bold;color:rgba(255,255,255,.9)">A\u2229B</div><div style="font-size:10px;color:rgba(255,255,255,.75)">'+(pa*pb).toFixed(3)+'</div>';

  var r2=document.getElementById('r2');
  r2.style.cssText='background:#4a148c;position:absolute;left:'+xd+'px;top:0;width:'+(RW-xd)+'px;height:'+yd+'px;display:flex;align-items:center;justify-content:center;flex-direction:column;';
  r2.innerHTML='<div style="font-size:12px;font-weight:bold;color:rgba(255,255,255,.9)">A\u1D9C\u2229B</div><div style="font-size:10px;color:rgba(255,255,255,.75)">'+(pac*pb).toFixed(3)+'</div>';

  var r3=document.getElementById('r3');
  r3.style.cssText='background:#1b5e20;position:absolute;left:0;top:'+yd+'px;width:'+xd+'px;height:'+(RH-yd)+'px;display:flex;align-items:center;justify-content:center;flex-direction:column;';
  r3.innerHTML='<div style="font-size:12px;font-weight:bold;color:rgba(255,255,255,.9)">A\u2229B\u1D9C</div><div style="font-size:10px;color:rgba(255,255,255,.75)">'+(pa*pbc).toFixed(3)+'</div>';

  var r4=document.getElementById('r4');
  r4.style.cssText='background:#4e342e;position:absolute;left:'+xd+'px;top:'+yd+'px;width:'+(RW-xd)+'px;height:'+(RH-yd)+'px;display:flex;align-items:center;justify-content:center;flex-direction:column;';
  r4.innerHTML='<div style="font-size:12px;font-weight:bold;color:rgba(255,255,255,.9)">A\u1D9C\u2229B\u1D9C</div><div style="font-size:10px;color:rgba(255,255,255,.75)">'+(pac*pbc).toFixed(3)+'</div>';

  // X축 레이블
  document.getElementById('axisX').innerHTML=
    '<div class="ax-seg" style="width:'+xd+'px">P(A)='+pa.toFixed(2)+'</div>'+
    '<div class="ax-seg" style="width:'+(RW-xd)+'px">P(A\u1D9C)='+pac.toFixed(2)+'</div>';

  // 4쌍 확인
  var pairs=[
    {la:'A, B',    pX:pa,  pY:pb,  pXY:pa*pb,   lx:'P(A)',   ly:'P(B)'},
    {la:'A, B\u1D9C',  pX:pa,  pY:pbc, pXY:pa*pbc,  lx:'P(A)',   ly:'P(B\u1D9C)'},
    {la:'A\u1D9C, B',  pX:pac, pY:pb,  pXY:pac*pb,  lx:'P(A\u1D9C)', ly:'P(B)'},
    {la:'A\u1D9C, B\u1D9C', pX:pac, pY:pbc, pXY:pac*pbc, lx:'P(A\u1D9C)', ly:'P(B\u1D9C)'},
  ];
  document.getElementById('props').innerHTML=pairs.map(function(p){
    return '<div class="prop-row">'
      +'<span class="pair">'+p.la+' 독립?</span><br>'
      +'<span style="color:#90caf9;font-family:monospace;font-size:10px">'+p.lx+'\xd7'+p.ly+'</span><br>'
      +'<span style="color:#78909c;font-size:10px">'+p.pX.toFixed(2)+'\xd7'+p.pY.toFixed(2)+'='+p.pXY.toFixed(4)+'</span>'
      +' <span class="chk">\u2713</span></div>';
  }).join('');

  document.getElementById('note').innerHTML=
    '<b>\U0001F4A1 확률 사각형 읽는 법</b><br>'
    +'가로 = P(A) 또는 P(A\u1D9C), 세로 = P(B) 또는 P(B\u1D9C)<br>'
    +'각 칸의 <b>넓이 = 가로 × 세로 = 두 사건 각각의 확률의 곱</b><br>'
    +'\u21D2 이 <b>격자(grid) 구조</b>가 독립의 본질! 4쌍 모두 자동으로 독립이 됩니다.';
}
update();
</script></body></html>"""

# ──────────────────────────────────────────────────────────────────────────────
# Tab 3: 독립의 비추이성 — 주사위 예시 (삼단논법 불성립)
# ──────────────────────────────────────────────────────────────────────────────

_TAB3_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;background:#0e1117;color:#e0e0e0;padding:14px;font-size:14px;line-height:1.5}
.hd{color:#90caf9;font-size:17px;font-weight:bold;margin-bottom:4px}
.sub{color:#78909c;font-size:12px;margin-bottom:14px}
.warn-box{background:#1a1200;border:1px solid #f9a825;border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:13px;color:#fff8e1;line-height:1.7}
.warn-box b{color:#ffd54f}
.dice-section{background:#1a1f2e;border:1px solid #2d3548;border-radius:10px;padding:14px 18px;margin-bottom:14px}
.ds-title{color:#64b5f6;font-size:14px;font-weight:bold;margin-bottom:10px}
.dice-grid{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:10px}
.die{width:92px;height:92px;border-radius:14px;border:2px solid #555;background:#1e2740;display:flex;align-items:center;justify-content:center;font-size:48px;line-height:1;color:#90a4ae;transition:all .3s;position:relative;cursor:default;flex-shrink:0}
.die .dlabel{position:absolute;bottom:-22px;left:0;right:0;text-align:center;font-size:11px;font-weight:bold}
.die.inA{border-color:#ef5350;background:#7f0000;color:#ffcdd2}
.die.inB{border-color:#42a5f5;background:#0d47a1;color:#b3e5fc}
.die.inC{border-color:#66bb6a;background:#1b5e20;color:#c8e6c9}
.die.inAB{border-color:#ab47bc;background:#4a148c;color:#e1bee7}
.die.inBC{border-color:#26c6da;background:#006064;color:#b2ebf2}
.die.inAC{border-color:#ff7043;background:#bf360c;color:#ffccbc}
.die.inABC{border-color:#fff;background:#424242;color:#fff}
.legend{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.leg-item{display:flex;align-items:center;gap:5px;font-size:11px}
.leg-dot{width:14px;height:14px;border-radius:4px;flex-shrink:0}
.step-btn-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.step-btn{padding:9px 18px;border-radius:8px;border:none;cursor:pointer;font-size:13px;font-weight:bold;transition:opacity .15s,transform .1s;background:#37474f;color:#eee}
.step-btn.active{background:#1565c0;color:#fff}
.step-btn:hover:not(:disabled){opacity:.85;transform:scale(1.03)}
.step-btn:disabled{opacity:.35;cursor:default}
.calc-box{background:#111827;border:1px solid #1e3a5f;border-radius:10px;padding:14px 18px;font-size:13px;line-height:1.9}
.calc-title{color:#ffd54f;font-weight:bold;font-size:14px;margin-bottom:8px}
.calc-row{margin-bottom:4px}
.ok{color:#a5d6a7;font-weight:bold}.bad{color:#ef9a9a;font-weight:bold}
.hl{background:#1a3a1a;border-left:3px solid #66bb6a;padding:6px 10px;border-radius:0 6px 6px 0;margin:8px 0}
.hl.warn{background:#3a1a00;border-left-color:#ff8f00}
.conclusion{background:#1a2744;border:1px solid #1e3a5f;border-radius:8px;padding:12px 16px;margin-top:10px;font-size:13px;line-height:1.7}
.concl-title{color:#ffd54f;font-size:15px;font-weight:bold;margin-bottom:8px}
.kp{border-left:4px solid #42a5f5;background:#0d1e33;padding:8px 12px;border-radius:0 6px 6px 0;margin-bottom:8px;color:#cfd8dc}
.kp.warn{border-left-color:#ff8f00}
</style></head><body>
<div class="hd">독립의 비추이성 — 삼단논법은 통하지 않는다!</div>
<div class="sub">A와 B가 독립이고, B와 C가 독립이라도 → A와 C가 독립이라는 보장은 없습니다.</div>

<div class="warn-box">
  ⚠️ <b>착각 주의!</b><br>
  &nbsp;&nbsp;"A와 B가 독립" + "B와 C가 독립" → "A와 C도 독립"? <b>이건 항상 성립하지 않습니다!</b><br>
  아래 주사위 예시로 직접 확인해보세요.
</div>

<div class="dice-section">
  <div class="ds-title">🎲 주사위 한 번 던지기 — 사건 정의</div>
  <div style="margin-bottom:12px;font-size:13px;color:#cfd8dc;line-height:1.8">
    <span style="color:#ef9a9a;font-weight:bold">A = {1,3,5}</span> &nbsp;(홀수인 눈) &nbsp;|&nbsp;
    <span style="color:#90caf9;font-weight:bold">B = {3,4}</span> &nbsp;(3 또는 4의 눈) &nbsp;|&nbsp;
    <span style="color:#a5d6a7;font-weight:bold">C = {2,3,5}</span> &nbsp;(소수인 눈)
  </div>
  <div class="legend">
    <div class="leg-item"><div class="leg-dot" style="background:#7f0000;border:1px solid #ef5350"></div>A만</div>
    <div class="leg-item"><div class="leg-dot" style="background:#0d47a1;border:1px solid #42a5f5"></div>B만</div>
    <div class="leg-item"><div class="leg-dot" style="background:#1b5e20;border:1px solid #66bb6a"></div>C만</div>
    <div class="leg-item"><div class="leg-dot" style="background:#4a148c;border:1px solid #ab47bc"></div>A∩B</div>
    <div class="leg-item"><div class="leg-dot" style="background:#006064;border:1px solid #26c6da"></div>B∩C</div>
    <div class="leg-item"><div class="leg-dot" style="background:#bf360c;border:1px solid #ff7043"></div>A∩C</div>
  </div>
  <div class="dice-grid" id="diceGrid"></div>
  <div style="color:#546e7a;font-size:11px;margin-top:28px">* 각 눈의 색깔은 어느 사건에 속하는지 나타냅니다.</div>
</div>

<div class="step-btn-row">
  <button class="step-btn active" id="btn0">📋 사건 확인</button>
  <button class="step-btn" id="btn1">① A, B 독립?</button>
  <button class="step-btn" id="btn2">② B, C 독립?</button>
  <button class="step-btn" id="btn3">③ A, C 독립? 🔥</button>
  <button class="step-btn" id="btn4">🔑 결론</button>
</div>

<div id="calcArea"></div>

<script>
var membership=[
  {n:1, inA:true,  inB:false, inC:false},
  {n:2, inA:false, inB:false, inC:true},
  {n:3, inA:true,  inB:true,  inC:true},
  {n:4, inA:false, inB:true,  inC:false},
  {n:5, inA:true,  inB:false, inC:true},
  {n:6, inA:false, inB:false, inC:false},
];

function dieClass(m){
  if(m.inA&&m.inB&&m.inC) return 'inABC';
  if(m.inA&&m.inB) return 'inAB';
  if(m.inB&&m.inC) return 'inBC';
  if(m.inA&&m.inC) return 'inAC';
  if(m.inA) return 'inA';
  if(m.inB) return 'inB';
  if(m.inC) return 'inC';
  return '';
}

function dieLabel(m){
  var parts=[];
  if(m.inA) parts.push('<span style="color:#ef9a9a">A</span>');
  if(m.inB) parts.push('<span style="color:#90caf9">B</span>');
  if(m.inC) parts.push('<span style="color:#a5d6a7">C</span>');
  return parts.length ? parts.join('') : '<span style="color:#546e7a">–</span>';
}

var faces=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685'];
var grid=document.getElementById('diceGrid');
for(var i=0;i<membership.length;i++){
  var m=membership[i];
  var d=document.createElement('div');
  d.className='die '+dieClass(m);
  d.innerHTML=faces[i]+'<div class="dlabel">'+dieLabel(m)+'</div>';
  d.style.marginBottom='26px';
  grid.appendChild(d);
}

var steps=[
  '<div class="calc-box">'
  +'<div class="calc-title">📋 사건 정리</div>'
  +'<div class="calc-row">표본공간 S = {1, 2, 3, 4, 5, 6}</div>'
  +'<div class="calc-row" style="color:#ef9a9a"><b>A = {1, 3, 5}</b> &nbsp;→ P(A) = 3/6 = <b>1/2</b></div>'
  +'<div class="calc-row" style="color:#90caf9"><b>B = {3, 4}</b> &nbsp;→ P(B) = 2/6 = <b>1/3</b></div>'
  +'<div class="calc-row" style="color:#a5d6a7"><b>C = {2, 3, 5}</b> &nbsp;→ P(C) = 3/6 = <b>1/2</b></div>'
  +'<div style="color:#78909c;margin-top:8px;font-size:12px">단계별로 독립 여부를 확인해보세요. ①②③ 버튼을 순서대로 눌러보세요!</div>'
  +'</div>',

  '<div class="calc-box">'
  +'<div class="calc-title">① A와 B는 서로 독립인가?</div>'
  +'<div class="calc-row">A∩B = {1,3,5} ∩ {3,4} = <b>{3}</b></div>'
  +'<div class="calc-row">P(A∩B) = 1/6</div>'
  +'<div class="calc-row">P(A) × P(B) = 1/2 × 1/3 = <b>1/6</b></div>'
  +'<div class="hl">P(A∩B) = 1/6 = P(A)·P(B) = 1/6 &nbsp;<span class="ok">✓ A와 B는 서로 독립!</span></div>'
  +'</div>',

  '<div class="calc-box">'
  +'<div class="calc-title">② B와 C는 서로 독립인가?</div>'
  +'<div class="calc-row">B∩C = {3,4} ∩ {2,3,5} = <b>{3}</b></div>'
  +'<div class="calc-row">P(B∩C) = 1/6</div>'
  +'<div class="calc-row">P(B) × P(C) = 1/3 × 1/2 = <b>1/6</b></div>'
  +'<div class="hl">P(B∩C) = 1/6 = P(B)·P(C) = 1/6 &nbsp;<span class="ok">✓ B와 C도 서로 독립!</span></div>'
  +'<div style="color:#78909c;margin-top:8px;font-size:12px">✅ A,B 독립 &amp; B,C 독립 → A,C도 독립?? 확인해봅시다!</div>'
  +'</div>',

  '<div class="calc-box">'
  +'<div class="calc-title">③ A와 C는 서로 독립인가? 🔥</div>'
  +'<div class="calc-row">A∩C = {1,3,5} ∩ {2,3,5} = <b>{3, 5}</b></div>'
  +'<div class="calc-row">P(A∩C) = 2/6 = <b>1/3</b></div>'
  +'<div class="calc-row">P(A) × P(C) = 1/2 × 1/2 = <b>1/4</b></div>'
  +'<div class="hl warn">P(A∩C) = 1/3 &nbsp;≠&nbsp; P(A)·P(C) = 1/4 &nbsp;<span class="bad">✗ A와 C는 종속!</span></div>'
  +'<div style="color:#ffcc02;margin-top:10px;font-size:13px;font-weight:bold">😲 A,B 독립 + B,C 독립 이어도 A,C는 독립이 아닙니다!</div>'
  +'</div>',

  '<div class="conclusion">'
  +'<div class="concl-title">🔑 핵심 결론</div>'
  +'<div class="kp"><b>A와 B가 독립</b> + <b>B와 C가 독립</b>이라고 해서 <b>A와 C도 독립</b>인 것은 <b>아닙니다!</b><br>'
  +'독립에서는 <b>삼단논법이 성립하지 않습니다.</b></div>'
  +'<div class="kp warn"><b>독립은 "전파"되지 않습니다.</b><br>'
  +'두 쌍 각각의 독립 여부를 항상 직접 P(A∩B)=P(A)P(B)로 확인해야 합니다!</div>'
  +'<div style="color:#78909c;font-size:12px;margin-top:8px">이 예시: A={홀수}, B={3,4}, C={소수} → A,B 독립 ✓ &nbsp; B,C 독립 ✓ &nbsp; A,C 종속 ✗</div>'
  +'</div>',
];

function showStep(i){
  for(var k=0;k<5;k++){
    var b=document.getElementById('btn'+k);
    if(b) b.className='step-btn'+(k===i?' active':'');
  }
  document.getElementById('calcArea').innerHTML=steps[i];
}

for(var si=0;si<5;si++){
  (function(idx){
    document.getElementById('btn'+idx).addEventListener('click',function(){showStep(idx);});
  })(si);
}
showStep(0);
</script></body></html>"""


# ──────────────────────────────────────────────────────────────────────────────
# render()
# ──────────────────────────────────────────────────────────────────────────────

def render():
    st.subheader("🎯 사건의 독립과 배반 탐구")

    tabs = st.tabs([
        "① 배반 vs 독립 분류 게임",
        "② 독립의 성질",
        "③ 독립의 비추이성",
    ])

    with tabs[0]:
        components.html(_TAB1_HTML, height=1080, scrolling=True)

    with tabs[1]:
        components.html(_TAB2_HTML, height=760, scrolling=True)

    with tabs[2]:
        components.html(_TAB3_HTML, height=920, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
