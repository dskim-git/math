# activities/probability_new/mini/conditional_prob_explorer.py
"""
조건부확률 vs 확률 탐험기
- 3가지 상황(주사위, 상자 속 공, 숫자 카드)
- 사건 후보 중 A, B 직접 선택
- P(A), P(B), P(A∩B), P(B|A), P(A|B) 자동 계산 및 시각화
- 조건부확률과 확률의 차이를 발견하는 탐구 활동
"""
import json
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🔍 조건부확률 탐험기",
    "description": "주사위·공·카드 상황에서 사건 A, B를 직접 선택하고 P(A), P(B), P(A|B), P(B|A), P(A∩B)를 비교하며 조건부확률의 개념을 발견합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "조건부확률탐험기"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 조건부확률 탐험기**"},
    {
        "key": "조건부확률vs확률",
        "label": "P(B|A)와 P(B)가 다른 경우를 하나 소개하고, 왜 다른지 자신의 말로 설명해보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "예) 주사위에서 A = 홀수, B = 소수로 선택했을 때...",
    },
    {
        "key": "순서차이",
        "label": "P(A|B)와 P(B|A)가 다른 예를 찾고, 왜 순서가 중요한지 설명해보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "조건 사건에 따라 표본공간이 달라지기 때문에...",
    },
    {
        "key": "독립발견",
        "label": "P(B|A) = P(B)가 되는 경우(독립사건)를 탐구 중 발견했나요? 어떤 상황이었는지 써보세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) 상황 1에서 A = 홀수, B = 3의 배수로 선택했더니...",
    },
    {
        "key": "교집합vs조건부",
        "label": "P(A∩B)와 P(B|A)는 어떻게 다른가요? 수식과 함께 설명해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "P(A∩B) = n(A∩B)/n(S) 이고, P(B|A) = n(A∩B)/n(A) 이므로...",
    },
    {
        "key": "새로알게된점",
        "label": "💡 이 활동에서 새롭게 알게 된 점",
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

# ── 시나리오 데이터 (Python) ──────────────────────────────────────────────────
_SC = [
    {
        "id": 0,
        "icon": "🎲",
        "name": "주사위",
        "sit": "주사위 한 개를 던지는 시행을 생각해봐요.<br>표본공간 <b>S = &#123;1, 2, 3, 4, 5, 6&#125;</b>, n(S) = 6 으로 모든 결과가 동일한 확률로 나타납니다.",
        "n": 6,
        "el": [1, 2, 3, 4, 5, 6],
        "ev": [
            {"l": "홀수",     "d": "&#123;1, 3, 5&#125;",        "e": [1, 3, 5]},
            {"l": "짝수",     "d": "&#123;2, 4, 6&#125;",        "e": [2, 4, 6]},
            {"l": "소수",     "d": "&#123;2, 3, 5&#125;",        "e": [2, 3, 5]},
            {"l": "3의 배수", "d": "&#123;3, 6&#125;",           "e": [3, 6]},
            {"l": "4 이상",   "d": "&#123;4, 5, 6&#125;",        "e": [4, 5, 6]},
            {"l": "6의 약수", "d": "&#123;1, 2, 3, 6&#125;",     "e": [1, 2, 3, 6]},
        ],
    },
    {
        "id": 1,
        "icon": "🎱",
        "name": "상자 속 공",
        "sit": "상자에 1부터 15까지 자연수가 적힌 <b>공 15개</b>가 들어 있습니다.<br>임의로 공 1개를 꺼내는 시행에서 표본공간 <b>S = &#123;1, 2, …, 15&#125;</b>, n(S) = 15 입니다.",
        "n": 15,
        "el": list(range(1, 16)),
        "ev": [
            {"l": "홀수",      "d": "&#123;1,3,5,7,9,11,13,15&#125;",  "e": [1,3,5,7,9,11,13,15]},
            {"l": "소수",      "d": "&#123;2,3,5,7,11,13&#125;",        "e": [2,3,5,7,11,13]},
            {"l": "3의 배수",  "d": "&#123;3,6,9,12,15&#125;",          "e": [3,6,9,12,15]},
            {"l": "5의 배수",  "d": "&#123;5,10,15&#125;",              "e": [5,10,15]},
            {"l": "12의 약수", "d": "&#123;1,2,3,4,6,12&#125;",         "e": [1,2,3,4,6,12]},
            {"l": "10 이하",   "d": "&#123;1,2,…,10&#125;",             "e": list(range(1, 11))},
        ],
    },
    {
        "id": 2,
        "icon": "🃏",
        "name": "숫자 카드",
        "sit": "1부터 20까지 자연수가 적힌 <b>카드 20장</b> 중에서 1장을 임의로 뽑습니다.<br>표본공간 <b>S = &#123;1, 2, …, 20&#125;</b>, n(S) = 20 입니다.",
        "n": 20,
        "el": list(range(1, 21)),
        "ev": [
            {"l": "홀수",       "d": "&#123;1,3,5,…,19&#125;",           "e": list(range(1,20,2))},
            {"l": "짝수",       "d": "&#123;2,4,6,…,20&#125;",           "e": list(range(2,21,2))},
            {"l": "4의 배수",   "d": "&#123;4,8,12,16,20&#125;",         "e": [4,8,12,16,20]},
            {"l": "소수",       "d": "&#123;2,3,5,7,11,13,17,19&#125;",  "e": [2,3,5,7,11,13,17,19]},
            {"l": "5의 배수",   "d": "&#123;5,10,15,20&#125;",           "e": [5,10,15,20]},
            {"l": "완전제곱수", "d": "&#123;1,4,9,16&#125;",             "e": [1,4,9,16]},
            {"l": "10 이하",    "d": "&#123;1,2,…,10&#125;",             "e": list(range(1, 11))},
        ],
    },
]


# ── CSS ──────────────────────────────────────────────────────────────────────
_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);
  color:#e2e8f0;padding:14px 12px 30px;min-height:100vh;
}
.hdr{
  text-align:center;padding:18px 20px 16px;
  background:linear-gradient(135deg,rgba(139,92,246,.18),rgba(59,130,246,.12));
  border:1px solid rgba(139,92,246,.4);border-radius:16px;margin-bottom:14px;
}
.hdr h1{font-size:1.3rem;font-weight:700;color:#a78bfa;margin-bottom:7px}
.hdr .fml{
  font-size:.95rem;color:#fcd34d;font-family:'Courier New',monospace;
  background:rgba(0,0,0,.35);display:inline-block;
  padding:5px 18px;border-radius:8px;margin:5px 0;
}
.hdr p{font-size:.81rem;color:#94a3b8;margin-top:6px;line-height:1.5}
.tabs{
  display:flex;gap:6px;margin-bottom:14px;
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:6px;
}
.tab{
  flex:1;padding:9px 6px;border-radius:9px;border:2px solid transparent;
  background:transparent;color:#64748b;
  font-weight:700;font-size:.8rem;cursor:pointer;
  transition:all .2s;line-height:1.35;
}
.tab:hover{color:#94a3b8;background:rgba(255,255,255,.05)}
.tab.active{background:rgba(139,92,246,.18);border-color:rgba(139,92,246,.55);color:#a78bfa}
.tab-pane{display:none}
.tab-pane.active{display:block}
.section{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  border-radius:14px;padding:16px 15px;margin-bottom:10px;
}
.sec-title{font-size:.97rem;font-weight:700;margin-bottom:8px;display:flex;align-items:center;gap:6px}
.sec-desc{font-size:.81rem;color:#94a3b8;line-height:1.65;margin-bottom:12px}
.situation{
  background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.13);
  border-radius:11px;padding:11px 14px;margin-bottom:14px;
}
.sit-label{font-size:.68rem;color:#94a3b8;font-weight:700;letter-spacing:.05em;margin-bottom:5px}
.sit-body{font-size:.88rem;color:#e2e8f0;line-height:1.8}
.sit-body b{color:#fbbf24}
.evt-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.evt-col-head{
  font-size:.73rem;font-weight:700;letter-spacing:.04em;
  padding:6px 10px;border-radius:8px;margin-bottom:7px;text-align:center;
}
.lbl-A{background:rgba(59,130,246,.22);color:#60a5fa;border:1px solid rgba(59,130,246,.4)}
.lbl-B{background:rgba(249,115,22,.22);color:#fb923c;border:1px solid rgba(249,115,22,.4)}
.evt-btn{
  width:100%;padding:7px 9px;border-radius:9px;
  border:2px solid rgba(255,255,255,.13);
  background:rgba(255,255,255,.055);color:#e2e8f0;
  font-size:.78rem;font-weight:600;cursor:pointer;
  transition:all .18s;text-align:left;margin-bottom:5px;display:block;
}
.evt-btn:hover{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.28)}
.evt-btn.selA{background:rgba(59,130,246,.28);border-color:#3b82f6;color:#93c5fd}
.evt-btn.selB{background:rgba(249,115,22,.28);border-color:#f97316;color:#fde68a}
.evt-btn.dis{cursor:not-allowed;opacity:.38;pointer-events:none}
.evt-btn .en{font-weight:700;font-size:.82rem;display:block}
.evt-btn .ed{font-size:.68rem;color:#94a3b8;display:block;margin-top:1px}
.evt-btn.selA .ed{color:#93c5fd}
.evt-btn.selB .ed{color:#fde68a}
.rst-btn{
  padding:5px 10px;border-radius:7px;border:1px solid rgba(255,255,255,.18);
  background:rgba(255,255,255,.05);color:#94a3b8;font-size:.71rem;
  cursor:pointer;margin-top:3px;width:100%;
}
.rst-btn:hover{background:rgba(255,255,255,.1);color:#e2e8f0}
.ss-label{font-size:.73rem;color:#94a3b8;margin-bottom:6px;font-weight:600}
.ss-grid{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:9px}
.ss-cell{
  width:38px;height:38px;border-radius:8px;border:2px solid;
  display:flex;align-items:center;justify-content:center;
  font-size:.82rem;font-weight:700;transition:all .3s;
}
.ss-none{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.1);color:#4b5563}
.ss-A{background:rgba(59,130,246,.3);border-color:#3b82f6;color:#93c5fd}
.ss-B{background:rgba(249,115,22,.3);border-color:#f97316;color:#fde68a}
.ss-AB{background:rgba(139,92,246,.38);border-color:#8b5cf6;color:#ddd6fe}
.ss-legend{display:flex;gap:9px;flex-wrap:wrap;font-size:.68rem;color:#94a3b8;margin-bottom:13px}
.ss-legend span{display:flex;align-items:center;gap:3px}
.ldot{width:9px;height:9px;border-radius:2px;flex-shrink:0;border:1.5px solid}
.ld-A{background:rgba(59,130,246,.3);border-color:#3b82f6}
.ld-B{background:rgba(249,115,22,.3);border-color:#f97316}
.ld-AB{background:rgba(139,92,246,.38);border-color:#8b5cf6}
.ld-n{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.15)}
.results{
  background:rgba(139,92,246,.08);
  border:1px solid rgba(139,92,246,.32);
  border-radius:14px;padding:15px 14px;
  animation:fi .4s ease;
}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.res-title{
  font-size:.88rem;font-weight:700;color:#a78bfa;
  margin-bottom:11px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;
}
.res-evts{font-size:.73rem;font-weight:400;color:#94a3b8}
.prob-wrap{display:grid;grid-template-columns:210px 1fr;gap:14px;align-items:start;margin-bottom:12px}
canvas.vc{
  display:block;border-radius:11px;
  background:rgba(0,0,0,.35);
  border:1px solid rgba(255,255,255,.1);
}
.pcards{display:flex;flex-direction:column;gap:7px}
.pcard{
  background:rgba(255,255,255,.055);border:1.5px solid rgba(255,255,255,.13);
  border-radius:9px;padding:8px 12px;
  display:flex;justify-content:space-between;align-items:center;gap:6px;
}
.pcard.hl{background:rgba(139,92,246,.18);border-color:rgba(139,92,246,.45)}
.pcard.hl2{background:rgba(251,191,36,.1);border-color:rgba(251,191,36,.35)}
.pc-lbl{font-size:.75rem;color:#94a3b8;font-family:'Courier New',monospace;flex-shrink:0}
.pc-val{font-size:.95rem;font-weight:700;color:#fbbf24;font-family:'Courier New',monospace;white-space:nowrap}
.pc-dec{font-size:.7rem;color:#64748b;margin-left:5px;font-family:'Courier New',monospace}
.insights{display:flex;flex-direction:column;gap:7px}
.ins{padding:9px 12px;border-radius:9px;font-size:.79rem;line-height:1.65}
.ins-diff{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.32);color:#fca5a5}
.ins-same{background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.32);color:#6ee7b7}
.ins-info{background:rgba(251,191,36,.09);border:1px solid rgba(251,191,36,.28);color:#fde68a}
.ins-zero{background:rgba(156,163,175,.08);border:1px solid rgba(156,163,175,.22);color:#d1d5db}
.ins strong{font-weight:700}
.hint-prompt{
  text-align:center;padding:26px 20px;
  color:#475569;font-size:.83rem;
  border:1.5px dashed rgba(255,255,255,.1);border-radius:11px;
}
"""

# ── JS (순수 문자열 — f-string 아님) ─────────────────────────────────────────
_JS = r"""
var ST = [{A:null,B:null},{A:null,B:null},{A:null,B:null}];

/* gcd / 분수 표기 */
function gcd(a,b){while(b){var t=b;b=a%b;a=t;}return a;}
function frac(n,d){
  if(d===0)return '-';if(n===0)return '0';
  var g=gcd(n,d);var a=n/g,b=d/g;
  return b===1?''+a:a+'/'+b;
}
function dec(n,d){
  if(d===0)return '';return ' \u2248 '+(n/d).toFixed(3);
}

/* 확률 계산 */
function calc(si){
  var sc=SC[si],st=ST[si];
  if(st.A===null||st.B===null)return null;
  var eA=sc.ev[st.A],eB=sc.ev[st.B];
  var sA=new Set(eA.e.map(String)), sB=new Set(eB.e.map(String));
  var nA=sA.size, nB=sB.size;
  var nAB=eA.e.filter(function(x){return sB.has(String(x));}).length;
  var n=sc.n;
  return {
    nA:nA,nB:nB,nAB:nAB,n:n,sA:sA,sB:sB,
    pA:frac(nA,n),   pA_d:dec(nA,n),
    pB:frac(nB,n),   pB_d:dec(nB,n),
    pAB:frac(nAB,n), pAB_d:dec(nAB,n),
    pBgA: nA>0 ? frac(nAB,nA) : null,
    pBgA_d: nA>0 ? dec(nAB,nA) : '',
    pAgB: nB>0 ? frac(nAB,nB) : null,
    pAgB_d: nB>0 ? dec(nAB,nB) : '',
    isIndep: nA>0 && (nAB*n === nB*nA)
  };
}

/* 인사이트 */
function makeInsights(p, eA, eB){
  var ins=[];
  if(p.nAB===0){
    ins.push({c:'ins-zero', t:'&empty; A&cap;B = &empty; &rarr; 두 사건은 <strong>배반사건</strong>! P(B|A) = 0, P(A|B) = 0이에요.'});
  } else {
    if(p.isIndep){
      ins.push({c:'ins-same', t:'&check; P(B|A) = '+p.pBgA+' = P(B) = '+p.pB+' &rarr; <strong>사건 A, B는 서로 독립!</strong> A가 일어나도 B의 확률이 변하지 않아요.'});
    } else {
      ins.push({c:'ins-diff', t:'&#9889; P(B|A) = '+p.pBgA+' &ne; P(B) = '+p.pB+' &rarr; <strong>사건 A가 일어나면 B의 확률이 달라져요!</strong> 이것이 조건부확률이 필요한 이유예요.'});
    }
    var pAgBEqpA = p.nB>0 && (p.nAB*p.n === p.nA*p.nB);
    if(pAgBEqpA){
      ins.push({c:'ins-same', t:'&check; P(A|B) = '+p.pAgB+' = P(A) = '+p.pA+' &rarr; B가 일어나도 A의 확률이 변하지 않아요.'});
    } else {
      ins.push({c:'ins-diff', t:'&#9889; P(A|B) = '+p.pAgB+' &ne; P(A) = '+p.pA+' &rarr; B 조건 하에서 A의 확률도 달라져요!'});
    }
    if(p.nA === p.nB){
      ins.push({c:'ins-info', t:'&#128161; P(A|B) = P(B|A) = '+p.pBgA+' &mdash; n(A)=n(B)라 우연히 같아졌어요. <strong>일반적으로 P(A|B) &ne; P(B|A)</strong>임을 기억하세요!'});
    } else {
      ins.push({c:'ins-info', t:'&#128161; P(A|B) = '+p.pAgB+', &nbsp; P(B|A) = '+p.pBgA+' &rarr; <strong>조건 순서가 바뀌면 조건부확률도 달라져요!</strong>'});
    }
  }
  return ins;
}

/* 탭 전환 */
function sw(btn){
  document.querySelectorAll('.tab-pane').forEach(function(p){p.classList.remove('active');});
  document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('active');});
  document.getElementById(btn.dataset.t).classList.add('active');
  btn.classList.add('active');
}

/* 사건 선택 */
function selEvt(si, i, w){
  var st=ST[si];
  if(w==='A' && st.B===i) return;
  if(w==='B' && st.A===i) return;
  if(w==='A') st.A = (st.A===i) ? null : i;
  else        st.B = (st.B===i) ? null : i;
  updateUI(si);
}
function rst(si, w){
  if(w==='A') ST[si].A=null; else ST[si].B=null;
  updateUI(si);
}

/* UI 갱신 */
function updateUI(si){
  var sc=SC[si], st=ST[si];

  /* 버튼 스타일 */
  for(var i=0;i<sc.ev.length;i++){
    var ba=document.getElementById('b'+si+'A'+i);
    var bb=document.getElementById('b'+si+'B'+i);
    if(ba){
      ba.className='evt-btn'+(st.A===i?' selA':'')+(st.B===i?' dis':'');
    }
    if(bb){
      bb.className='evt-btn'+(st.B===i?' selB':'')+(st.A===i?' dis':'');
    }
  }

  /* 표본공간 색칠 */
  var sA=st.A!==null?new Set(sc.ev[st.A].e.map(String)):new Set();
  var sB=st.B!==null?new Set(sc.ev[st.B].e.map(String)):new Set();
  sc.el.forEach(function(x){
    var cell=document.getElementById('c'+si+'x'+x);
    if(!cell)return;
    var inA=sA.has(String(x)), inB=sB.has(String(x));
    cell.className='ss-cell '+(inA&&inB?'ss-AB':inA?'ss-A':inB?'ss-B':'ss-none');
  });

  /* 결과 */
  updateResults(si);
}

function updateResults(si){
  var sc=SC[si], st=ST[si];
  var resDiv=document.getElementById('res'+si);
  if(st.A===null||st.B===null){
    resDiv.className='hint-prompt';
    resDiv.innerHTML='&#128070; 사건 A와 사건 B를 모두 선택하면<br>확률 계산 결과와 벤다이어그램이 나타납니다!';
    return;
  }
  var p=calc(si);
  var eA=sc.ev[st.A], eB=sc.ev[st.B];
  var insHTML=makeInsights(p,eA,eB).map(function(ins){
    return '<div class="ins '+ins.c+'">'+ins.t+'</div>';
  }).join('');

  resDiv.className='results';
  resDiv.innerHTML=
    '<div class="res-title">&#128202; 계산 결과 <span class="res-evts">사건 A = '+eA.l+' &nbsp;/&nbsp; 사건 B = '+eB.l+'</span></div>'
    +'<div class="prob-wrap">'
      +'<div><canvas class="vc" id="vc'+si+'" width="210" height="172"></canvas></div>'
      +'<div class="pcards">'
        +'<div class="pcard"><span class="pc-lbl">P(A) = P('+eA.l+')</span>'
          +'<span class="pc-val">'+p.pA+'<span class="pc-dec">'+p.pA_d+'</span></span></div>'
        +'<div class="pcard"><span class="pc-lbl">P(B) = P('+eB.l+')</span>'
          +'<span class="pc-val">'+p.pB+'<span class="pc-dec">'+p.pB_d+'</span></span></div>'
        +'<div class="pcard"><span class="pc-lbl">P(A&cap;B)</span>'
          +'<span class="pc-val">'+p.pAB+'<span class="pc-dec">'+p.pAB_d+'</span></span></div>'
        +'<div class="pcard hl"><span class="pc-lbl">P(B|A) = P(A&cap;B)/P(A)</span>'
          +'<span class="pc-val">'+(p.pBgA||'&minus;')+'<span class="pc-dec">'+p.pBgA_d+'</span></span></div>'
        +'<div class="pcard hl2"><span class="pc-lbl">P(A|B) = P(A&cap;B)/P(B)</span>'
          +'<span class="pc-val">'+(p.pAgB||'&minus;')+'<span class="pc-dec">'+p.pAgB_d+'</span></span></div>'
      +'</div>'
    +'</div>'
    +'<div class="insights">'+insHTML+'</div>';

  setTimeout(function(){
    var c=document.getElementById('vc'+si);
    if(c) drawVenn(c,si);
  }, 60);
}

/* 벤다이어그램 */
function drawVenn(canvas, si){
  var sc=SC[si], p=calc(si);
  if(!p)return;
  var ctx=canvas.getContext('2d'), W=canvas.width, H=canvas.height;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='rgba(8,12,24,.88)'; ctx.fillRect(0,0,W,H);

  var cx=W/2, cy=H/2+12;
  var maxR=52;
  var rA=maxR*Math.sqrt(p.nA/sc.n)+9;
  var rB=maxR*Math.sqrt(p.nB/sc.n)+9;
  var dist;
  if(p.nAB===0){ dist=rA+rB+5; }
  else if(p.nAB===Math.min(p.nA,p.nB)){ dist=Math.abs(rA-rB)+3; }
  else{
    var dMax=rA+rB, dMin=Math.abs(rA-rB)+5;
    var ov=(p.nA>0)?p.nAB/p.nA:0;
    dist=dMax-ov*(dMax-dMin)*1.7;
    dist=Math.max(dMin,Math.min(dMax-3,dist));
  }
  var xA=cx-dist/2, xB=cx+dist/2;

  /* S 테두리 */
  ctx.strokeStyle='rgba(255,255,255,.13)'; ctx.lineWidth=1.5;
  ctx.strokeRect(7,7,W-14,H-14);
  ctx.fillStyle='rgba(255,255,255,.28)'; ctx.font='11px Segoe UI';
  ctx.textAlign='right'; ctx.textBaseline='top';
  ctx.fillText('S', W-10, 9);

  /* A */
  ctx.beginPath(); ctx.arc(xA,cy,rA,0,2*Math.PI);
  ctx.fillStyle='rgba(59,130,246,.22)'; ctx.fill();
  ctx.strokeStyle='#3b82f6'; ctx.lineWidth=2; ctx.stroke();
  /* B */
  ctx.beginPath(); ctx.arc(xB,cy,rB,0,2*Math.PI);
  ctx.fillStyle='rgba(249,115,22,.22)'; ctx.fill();
  ctx.strokeStyle='#f97316'; ctx.lineWidth=2; ctx.stroke();
  /* A∩B */
  if(p.nAB>0){
    ctx.save();
    ctx.beginPath(); ctx.arc(xA,cy,rA,0,2*Math.PI); ctx.clip();
    ctx.beginPath(); ctx.arc(xB,cy,rB,0,2*Math.PI);
    ctx.fillStyle='rgba(139,92,246,.42)'; ctx.fill();
    ctx.restore();
    ctx.save();
    ctx.beginPath(); ctx.arc(xA,cy,rA,0,2*Math.PI); ctx.clip();
    ctx.beginPath(); ctx.arc(xB,cy,rB,0,2*Math.PI);
    ctx.strokeStyle='#8b5cf6'; ctx.lineWidth=1.5; ctx.stroke();
    ctx.restore();
  }

  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.font='bold 13px Segoe UI'; ctx.fillStyle='#93c5fd';
  ctx.fillText('A', xA-rA*0.46, cy-5);
  ctx.font='10px Courier New'; ctx.fillText(p.pA, xA-rA*0.46, cy+9);
  ctx.font='bold 13px Segoe UI'; ctx.fillStyle='#fdba74';
  ctx.fillText('B', xB+rB*0.46, cy-5);
  ctx.font='10px Courier New'; ctx.fillText(p.pB, xB+rB*0.46, cy+9);
  if(p.nAB>0){
    var mx=(xA+xB)/2;
    ctx.font='bold 9px Segoe UI'; ctx.fillStyle='#ddd6fe';
    ctx.fillText('A\u2229B', mx, cy-7);
    ctx.font='9px Courier New'; ctx.fillText(p.pAB, mx, cy+6);
  }
}
"""


# ── HTML 생성 (Python으로 정적 생성) ─────────────────────────────────────────
def _build_html() -> str:
    # 시나리오 HTML 생성
    scenarios_html = ""
    for sc in _SC:
        si = sc["id"]
        active_cls = " active" if si == 0 else ""

        # 이벤트 버튼 A
        evts_a = ""
        for i, ev in enumerate(sc["ev"]):
            evts_a += (
                f'<button id="b{si}A{i}" class="evt-btn"'
                f' onclick="selEvt({si},{i},\'A\')">'
                f'<span class="en">{ev["l"]}</span>'
                f'<span class="ed">{ev["d"]}</span></button>'
            )

        # 이벤트 버튼 B
        evts_b = ""
        for i, ev in enumerate(sc["ev"]):
            evts_b += (
                f'<button id="b{si}B{i}" class="evt-btn"'
                f' onclick="selEvt({si},{i},\'B\')">'
                f'<span class="en">{ev["l"]}</span>'
                f'<span class="ed">{ev["d"]}</span></button>'
            )

        # 표본공간 셀
        ss_cells = ""
        for el in sc["el"]:
            ss_cells += f'<div class="ss-cell ss-none" id="c{si}x{el}">{el}</div>'

        scenarios_html += f"""
<div id="t{si}" class="tab-pane{active_cls}">
  <div class="section">
    <div class="sec-title">{sc["icon"]} {sc["name"]} — 상황 설명</div>
    <div class="situation">
      <div class="sit-label">📌 시행 상황</div>
      <div class="sit-body">{sc["sit"]}</div>
    </div>
    <div class="sec-title" style="margin-top:14px">🎯 사건 선택</div>
    <div class="sec-desc">
      아래 사건 후보 중 <strong style="color:#60a5fa">사건 A</strong>와
      <strong style="color:#fb923c">사건 B</strong>를 각각 하나씩 골라보세요.<br>
      같은 사건은 선택할 수 없어요. 선택 후 확률이 어떻게 바뀌는지 관찰해봐요!
    </div>
    <div class="evt-row">
      <div>
        <div class="evt-col-head lbl-A">🔵 사건 A 선택</div>
        {evts_a}
        <button class="rst-btn" onclick="rst({si},'A')">↺ A 선택 취소</button>
      </div>
      <div>
        <div class="evt-col-head lbl-B">🟠 사건 B 선택</div>
        {evts_b}
        <button class="rst-btn" onclick="rst({si},'B')">↺ B 선택 취소</button>
      </div>
    </div>
    <div class="ss-label">📦 표본공간 S — {sc["n"]}개 결과</div>
    <div class="ss-grid">{ss_cells}</div>
    <div class="ss-legend">
      <span><div class="ldot ld-A"></div>A만 속함</span>
      <span><div class="ldot ld-B"></div>B만 속함</span>
      <span><div class="ldot ld-AB"></div>A와 B 모두 (A∩B)</span>
      <span><div class="ldot ld-n"></div>어디에도 없음</span>
    </div>
    <div id="res{si}" class="hint-prompt">
      👆 사건 A와 사건 B를 모두 선택하면<br>확률 계산 결과와 벤다이어그램이 나타납니다!
    </div>
  </div>
</div>"""

    # JS에 삽입할 SC 데이터 (JSON)
    sc_json = json.dumps(
        [{"n": sc["n"], "el": sc["el"], "ev": sc["ev"]} for sc in _SC],
        ensure_ascii=False,
    )

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{_CSS}</style>
</head>
<body>

<div class="hdr">
  <h1>🔍 조건부확률 탐험기</h1>
  <div class="fml">P(B|A) = P(A∩B) / P(A) &nbsp; (단, P(A) ≠ 0)</div>
  <p>사건 A와 B를 직접 선택하고 P(A), P(B), P(A∩B), P(B|A), P(A|B)를 비교해봐요!<br>
  조건부확률과 일반 확률이 어떻게 다른지 스스로 발견해보세요 🔍</p>
</div>

<div class="tabs">
  <button class="tab active" data-t="t0" onclick="sw(this)">🎲 상황 1<br><span style="font-size:.7rem;font-weight:400">주사위</span></button>
  <button class="tab" data-t="t1" onclick="sw(this)">🎱 상황 2<br><span style="font-size:.7rem;font-weight:400">상자 속 공</span></button>
  <button class="tab" data-t="t2" onclick="sw(this)">🃏 상황 3<br><span style="font-size:.7rem;font-weight:400">숫자 카드</span></button>
</div>

{scenarios_html}

<script>
var SC = {sc_json};
{_JS}
</script>
</body>
</html>"""


_HTML = _build_html()


def render():
    st.subheader("🔍 조건부확률 탐험기")
    st.caption(
        "주사위, 상자 속 공, 숫자 카드 3가지 상황에서 사건 A, B를 직접 선택하고 "
        "P(A), P(B), P(A∩B), P(B|A), P(A|B)를 비교하며 조건부확률의 의미를 발견해봐요!"
    )
    components.html(_HTML, height=1600, scrolling=False)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
