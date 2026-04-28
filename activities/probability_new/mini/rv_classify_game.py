import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "확률변수분류게임"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요.**"},
    {"key": "분류기준",   "label": "이산확률변수와 연속확률변수를 구분하는 핵심 기준을 자신의 말로 설명해 보세요.",             "type": "text_area", "height": 90},
    {"key": "헷갈린사례", "label": "처음에 헷갈렸던 사례가 있었나요? 왜 헷갈렸는지, 어떻게 해결했는지 적어 보세요.",           "type": "text_area", "height": 90},
    {"key": "나만의예시", "label": "이산확률변수와 연속확률변수의 예시를 일상생활에서 각각 하나씩 직접 만들어 보세요.",         "type": "text_area", "height": 90},
    {"key": "새롭게알게된점", "label": "💡 이 활동을 통해 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 이 활동을 통해 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title": "미니: 이산 vs 연속 확률변수 분류 게임",
    "description": "실생활 사례 카드를 이산·연속 확률변수로 분류하는 게임형 활동",
    "order": 999,
    "hidden": True,
}

_HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);min-height:100vh;padding:16px;color:#e2e8f0}

/* ── Header ── */
.header{display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:12px 20px;margin-bottom:14px}
.header-title{font-size:17px;font-weight:800;color:#fbbf24}
.header-sub{font-size:11px;color:#64748b;margin-top:2px}
.score-box{display:flex;gap:16px;text-align:center}
.score-num{font-size:22px;font-weight:900;color:#fbbf24;display:block}
.score-lbl{font-size:11px;color:#94a3b8}

/* ── Progress ── */
.prog-wrap{background:rgba(255,255,255,.08);border-radius:10px;height:8px;margin-bottom:8px;overflow:hidden}
.prog-bar{height:100%;background:linear-gradient(90deg,#10b981,#34d399);border-radius:10px;transition:width .5s ease}
.counter{text-align:center;font-size:12px;color:#64748b;margin-bottom:12px}

/* ── Legend ── */
.legend{display:flex;gap:10px;justify-content:center;margin-bottom:14px;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:7px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:7px 13px;font-size:12px;color:#94a3b8}
.dot-d{width:11px;height:11px;border-radius:50%;background:#818cf8;flex-shrink:0}
.dot-c{width:11px;height:11px;border-radius:50%;background:#f472b6;flex-shrink:0}

/* ── Card ── */
@keyframes slideIn{from{opacity:0;transform:translateX(50px)}to{opacity:1;transform:translateX(0)}}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-10px)}40%{transform:translateX(10px)}60%{transform:translateX(-7px)}80%{transform:translateX(7px)}}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.025)}100%{transform:scale(1)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}

.card{background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.15);border-radius:22px;padding:26px 22px;text-align:center;margin-bottom:14px;animation:slideIn .4s ease}
.card.ok{border-color:rgba(52,211,153,.6);background:rgba(52,211,153,.07);animation:pulse .45s ease}
.card.ng{border-color:rgba(248,113,113,.6);background:rgba(248,113,113,.07);animation:shake .5s ease}
.card-icon{font-size:50px;margin-bottom:10px}
.card-title{font-size:17px;font-weight:800;color:#fbbf24;margin-bottom:9px}
.card-desc{font-size:14px;color:#cbd5e1;line-height:1.65}

/* ── Buttons ── */
.btn-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
.btn-cls{padding:15px 10px;border-radius:16px;border:2px solid;font-size:14px;font-weight:700;cursor:pointer;transition:all .2s ease;line-height:1.4}
.btn-d{background:rgba(99,102,241,.15);border-color:rgba(99,102,241,.4);color:#a5b4fc}
.btn-d:hover:not(:disabled){background:rgba(99,102,241,.28);border-color:rgba(99,102,241,.7);transform:translateY(-2px);box-shadow:0 8px 20px rgba(99,102,241,.3)}
.btn-c{background:rgba(236,72,153,.15);border-color:rgba(236,72,153,.4);color:#f9a8d4}
.btn-c:hover:not(:disabled){background:rgba(236,72,153,.28);border-color:rgba(236,72,153,.7);transform:translateY(-2px);box-shadow:0 8px 20px rgba(236,72,153,.3)}
.btn-cls:disabled{opacity:.45;cursor:not-allowed;transform:none!important;box-shadow:none!important}
.btn-sub{font-size:10px;font-weight:400;opacity:.8}

/* ── Feedback ── */
.feedback{border-radius:14px;padding:13px 16px;margin-bottom:12px;font-size:13px;line-height:1.6;display:none;animation:fadeUp .3s ease}
.feedback.ok{background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);color:#6ee7b7}
.feedback.ng{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);color:#fca5a5}
.fb-title{font-weight:700;font-size:15px;margin-bottom:5px}
.fb-why{color:#94a3b8;margin-top:6px;font-size:12px}

/* ── Next button ── */
.btn-next{width:100%;padding:13px;border-radius:14px;background:linear-gradient(135deg,#fbbf24,#f59e0b);border:none;color:#1a1a2e;font-size:15px;font-weight:800;cursor:pointer;transition:all .2s ease;display:none}
.btn-next:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(251,191,36,.4)}

/* ── Results ── */
.results{display:none;text-align:center;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:22px;padding:24px 20px}
.res-emoji{font-size:60px;margin-bottom:10px}
.res-title{font-size:22px;font-weight:800;color:#fbbf24;margin-bottom:6px}
.res-score{font-size:44px;font-weight:900;margin:10px 0}
.res-desc{color:#94a3b8;font-size:13px;margin-bottom:18px}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px}
.res-card{border-radius:14px;padding:14px;border:1px solid;text-align:center}
.res-d{background:rgba(99,102,241,.1);border-color:rgba(99,102,241,.3)}
.res-c{background:rgba(236,72,153,.1);border-color:rgba(236,72,153,.3)}
.res-card .rlbl{font-size:11px;color:#94a3b8;margin-bottom:4px}
.res-card .rval{font-size:26px;font-weight:800}
.res-d .rval{color:#a5b4fc}
.res-c .rval{color:#f9a8d4}

.btn-restart{width:100%;padding:13px;border-radius:14px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border:none;color:#fff;font-size:15px;font-weight:700;cursor:pointer;transition:all .2s ease;margin-bottom:4px}
.btn-restart:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(99,102,241,.4)}

/* ── Mistake list ── */
.miss-hdr{font-size:13px;font-weight:700;color:#fca5a5;margin-bottom:8px;text-align:left}
.miss-item{background:rgba(255,255,255,.03);border:1px solid rgba(248,113,113,.2);border-radius:12px;padding:11px 14px;margin-bottom:7px;text-align:left}
.miss-top{display:flex;align-items:center;gap:7px;margin-bottom:4px}
.miss-icon{font-size:20px}
.miss-name{font-weight:700;color:#fca5a5;font-size:13px}
.miss-desc{font-size:12px;color:#94a3b8}
.miss-ans{font-size:12px;color:#6ee7b7;margin-top:3px}
.miss-why{font-size:12px;color:#64748b;margin-top:3px}

::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-thumb{background:rgba(251,191,36,.4);border-radius:3px}
</style>
</head>
<body>

<!-- ── Game Screen ── -->
<div id="game">
  <div class="header">
    <div>
      <div class="header-title">🎮 확률변수 분류 게임</div>
      <div class="header-sub">카드를 이산 또는 연속 확률변수로 분류해 보세요!</div>
    </div>
    <div class="score-box">
      <div><span class="score-num" id="sScore">0</span><span class="score-lbl">정답</span></div>
      <div><span class="score-num" id="sTotal">0</span><span class="score-lbl">전체</span></div>
    </div>
  </div>

  <div class="prog-wrap"><div class="prog-bar" id="progBar" style="width:0%"></div></div>
  <div class="counter" id="counter">1 / 20</div>

  <div class="legend">
    <div class="legend-item"><div class="dot-d"></div>이산확률변수 — 셀 수 있는 값 (자연수)</div>
    <div class="legend-item"><div class="dot-c"></div>연속확률변수 — 범위 내 모든 실수</div>
  </div>

  <div class="card" id="card">
    <div class="card-icon" id="cIcon"></div>
    <div class="card-title" id="cTitle"></div>
    <div class="card-desc" id="cDesc"></div>
  </div>

  <div class="btn-row">
    <button class="btn-cls btn-d" id="btnD" onclick="ans('discrete')">
      🔵 이산확률변수<br><span class="btn-sub">값을 셀 수 있다 (0, 1, 2, …)</span>
    </button>
    <button class="btn-cls btn-c" id="btnC" onclick="ans('continuous')">
      🔴 연속확률변수<br><span class="btn-sub">범위 내 모든 실수 값 가능</span>
    </button>
  </div>

  <div class="feedback" id="fb">
    <div class="fb-title" id="fbTitle"></div>
    <div id="fbText"></div>
    <div class="fb-why" id="fbWhy"></div>
  </div>

  <button class="btn-next" id="btnNext" onclick="nextCard()">다음 문제 →</button>
</div>

<!-- ── Results Screen ── -->
<div class="results" id="results">
  <div class="res-emoji" id="rEmoji"></div>
  <div class="res-title" id="rTitle"></div>
  <div class="res-score" id="rScore"></div>
  <div class="res-desc" id="rDesc"></div>
  <div class="res-grid">
    <div class="res-card res-d"><div class="rlbl">🔵 이산확률변수</div><div class="rval" id="rD"></div></div>
    <div class="res-card res-c"><div class="rlbl">🔴 연속확률변수</div><div class="rval" id="rC"></div></div>
  </div>
  <div id="missList"></div>
  <button class="btn-restart" onclick="restart()">🔄 다시 도전하기</button>
</div>

<script>
const DECK = [
  // ── 이산확률변수 ──
  {icon:"🎯", title:"양궁 과녁 적중 횟수",
   desc:"양궁 선수가 화살 10발을 쏠 때, 10점 과녁에 맞힌 화살의 개수",
   type:"discrete", reason:"화살을 맞힌 횟수는 0, 1, 2, …, 10 중 하나의 정수값만 가집니다. (셀 수 있음)"},
  {icon:"📱", title:"카카오톡 메시지 수",
   desc:"하루 동안 내가 받은 카카오톡 메시지의 총 개수",
   type:"discrete", reason:"메시지 수는 0, 1, 2, 3, … 처럼 셀 수 있는 자연수 값을 가집니다."},
  {icon:"🎲", title:"주사위 눈의 합",
   desc:"주사위 두 개를 동시에 던졌을 때 나오는 두 눈의 합",
   type:"discrete", reason:"눈의 합은 2, 3, 4, …, 12 중 하나의 값만 가집니다. (유한개, 셀 수 있음)"},
  {icon:"🏀", title:"자유투 성공 횟수",
   desc:"농구 선수가 자유투 20번 중 성공한 횟수",
   type:"discrete", reason:"성공 횟수는 0, 1, 2, …, 20 중 하나의 정수값만 가집니다."},
  {icon:"✅", title:"수능 맞힌 문제 수",
   desc:"수능 국어 45문항 중 한 학생이 맞힌 문제의 수",
   type:"discrete", reason:"0, 1, 2, …, 45 사이의 정수값만 가능합니다. (유한개)"},
  {icon:"🎰", title:"로또 일치 번호 수",
   desc:"로또 복권 한 장에서 추첨 번호와 일치하는 번호의 개수",
   type:"discrete", reason:"0, 1, 2, 3, 4, 5, 6 중 하나의 값만 가집니다. (유한개)"},
  {icon:"🐟", title:"잡힌 물고기 수",
   desc:"어부가 하루 동안 그물로 잡은 물고기의 수",
   type:"discrete", reason:"물고기 수는 0, 1, 2, 3, … 처럼 셀 수 있는 자연수 값을 가집니다."},
  {icon:"💌", title:"하루 이메일 수",
   desc:"회사원이 하루 동안 받은 업무 이메일의 수",
   type:"discrete", reason:"이메일 수는 0, 1, 2, 3, … 처럼 셀 수 있는 자연수 값을 가집니다."},
  {icon:"🦟", title:"모기에 물린 횟수",
   desc:"야외 캠핑 하룻밤 동안 모기에 물린 횟수",
   type:"discrete", reason:"물린 횟수는 0, 1, 2, 3, … 처럼 셀 수 있는 자연수 값을 가집니다."},
  {icon:"🚌", title:"버스 탑승 승객 수",
   desc:"오전 8시 등교 시간대 버스 한 대에 탑승한 승객 수",
   type:"discrete", reason:"승객 수는 0, 1, 2, 3, … 처럼 셀 수 있는 자연수 값을 가집니다."},
  // ── 연속확률변수 ──
  {icon:"📏", title:"학생의 키",
   desc:"고등학생 한 명을 임의로 선택했을 때 그 학생의 키 (cm)",
   type:"continuous", reason:"키는 160.3, 172.85, 158.0123, … 처럼 어떤 범위 내의 모든 실수 값을 가질 수 있습니다."},
  {icon:"⏱️", title:"100m 달리기 기록",
   desc:"학생이 100m 달리기를 완주하는 데 걸리는 시간 (초)",
   type:"continuous", reason:"기록은 10.5초, 12.47초, 11.823초 … 처럼 어느 범위 안의 모든 실수 값이 가능합니다."},
  {icon:"🌡️", title:"서울 낮 기온",
   desc:"특정 날 낮 12시 서울의 기온 (°C)",
   type:"continuous", reason:"기온은 23.5°C, 27.14°C, 19.001°C … 처럼 어느 범위 내의 모든 실수 값을 가질 수 있습니다."},
  {icon:"⛽", title:"자동차 연비",
   desc:"어떤 자동차가 연료 1L로 달릴 수 있는 거리 (km/L)",
   type:"continuous", reason:"연비는 12.3, 15.7, 11.85 … 처럼 특정 범위 내의 모든 실수 값을 가집니다."},
  {icon:"⏳", title:"카페 대기 시간",
   desc:"카페에서 주문 후 음료를 받을 때까지 기다리는 시간 (분)",
   type:"continuous", reason:"대기 시간은 2.5분, 3.14분, 4.82분 … 처럼 어느 범위 안의 모든 실수 값이 가능합니다."},
  {icon:"🔋", title:"스마트폰 배터리 지속 시간",
   desc:"스마트폰을 완충했을 때 배터리가 지속되는 시간 (시간)",
   type:"continuous", reason:"사용 시간은 8.3시간, 10.47시간, 9.8시간 … 처럼 실수 값을 가질 수 있습니다."},
  {icon:"🌧️", title:"하루 강수량",
   desc:"특정 날 서울의 하루 동안 내린 비의 양 (mm)",
   type:"continuous", reason:"강수량은 5.3mm, 12.7mm, 0.85mm … 처럼 어느 범위 내의 모든 실수 값을 가집니다."},
  {icon:"💊", title:"알약 한 개의 무게",
   desc:"공장에서 생산된 진통제 알약 한 개의 무게 (g)",
   type:"continuous", reason:"무게는 0.498g, 0.502g, 0.4997g … 처럼 어느 범위 내의 실수 값을 가질 수 있습니다."},
  {icon:"🏃", title:"마라톤 완주 시간",
   desc:"마라톤 선수가 42.195km를 완주하는 데 걸리는 시간 (시간)",
   type:"continuous", reason:"완주 시간은 2.5시간, 3.15시간, 2.87시간 … 처럼 어느 범위 내의 모든 실수 값을 가질 수 있습니다."},
  {icon:"🍕", title:"피자의 지름",
   desc:"피자 가게에서 직접 구운 원형 피자의 지름 (cm)",
   type:"continuous", reason:"피자 지름은 30.1cm, 29.85cm, 30.42cm … 처럼 어느 범위 내의 실수 값을 가집니다."},
];

let cards=[], cur=0, score=0, dC=0, cC=0, dT=0, cT=0, answered=false, mistakes=[];

function shuffle(a){const b=[...a];for(let i=b.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b;}

function init(){
  cards=shuffle(DECK); cur=0; score=0; dC=0; cC=0; dT=0; cT=0; answered=false; mistakes=[];
  document.getElementById('game').style.display='';
  document.getElementById('results').style.display='none';
  document.getElementById('sScore').textContent='0';
  document.getElementById('sTotal').textContent=cards.length;
  showCard();
}

function showCard(){
  const c=cards[cur];
  document.getElementById('cIcon').textContent=c.icon;
  document.getElementById('cTitle').textContent=c.title;
  document.getElementById('cDesc').textContent=c.desc;
  const el=document.getElementById('card');
  el.className='card'; el.style.animation='none'; el.offsetHeight; el.style.animation='slideIn .4s ease';
  document.getElementById('btnD').disabled=false;
  document.getElementById('btnC').disabled=false;
  document.getElementById('fb').style.display='none';
  document.getElementById('btnNext').style.display='none';
  answered=false;
  document.getElementById('counter').textContent=(cur+1)+' / '+cards.length;
  document.getElementById('progBar').style.width=((cur/cards.length)*100)+'%';
}

function ans(type){
  if(answered)return;
  answered=true;
  const c=cards[cur];
  const ok=type===c.type;
  document.getElementById('btnD').disabled=true;
  document.getElementById('btnC').disabled=true;
  const card=document.getElementById('card');
  const fb=document.getElementById('fb');
  if(ok){
    score++;
    card.className='card ok';
    fb.className='feedback ok';
    document.getElementById('fbTitle').textContent='✅ 정답!';
    document.getElementById('fbText').textContent='"'+c.title+'"는 '+(c.type==='discrete'?'🔵 이산확률변수':'🔴 연속확률변수')+'입니다.';
    if(c.type==='discrete')dC++;else cC++;
  } else {
    card.className='card ng';
    fb.className='feedback ng';
    document.getElementById('fbTitle').textContent='❌ 아쉽네요!';
    document.getElementById('fbText').textContent='"'+c.title+'"는 '+(c.type==='discrete'?'🔵 이산확률변수':'🔴 연속확률변수')+'입니다.';
    mistakes.push(c);
  }
  document.getElementById('fbWhy').textContent='💡 '+c.reason;
  if(c.type==='discrete')dT++;else cT++;
  document.getElementById('sScore').textContent=score;
  fb.style.display='block';
  document.getElementById('btnNext').style.display='block';
}

function nextCard(){
  cur++;
  if(cur>=cards.length) showResults();
  else showCard();
}

function showResults(){
  document.getElementById('game').style.display='none';
  document.getElementById('results').style.display='block';
  const pct=Math.round(score/cards.length*100);
  let emoji,title,desc;
  if(pct>=90){emoji='🏆';title='완벽해요!';desc='이산·연속 확률변수를 완벽하게 구분했습니다!';}
  else if(pct>=75){emoji='🎉';title='훌륭해요!';desc='대부분 정확하게 분류했어요. 거의 다 왔습니다!';}
  else if(pct>=55){emoji='💪';title='잘했어요!';desc='절반 이상 맞혔어요. 틀린 문제를 확인해 보세요.';}
  else{emoji='📚';title='다시 도전!';desc='틀린 문제를 꼼꼼히 보고 다시 도전해 보세요!';}
  document.getElementById('rEmoji').textContent=emoji;
  document.getElementById('rTitle').textContent=title;
  document.getElementById('rScore').innerHTML='<span style="color:#fbbf24">'+score+'</span> / '+cards.length+' <span style="font-size:18px;color:#94a3b8">('+pct+'%)</span>';
  document.getElementById('rDesc').textContent=desc;
  document.getElementById('rD').textContent=dC+'/'+dT;
  document.getElementById('rC').textContent=cC+'/'+cT;
  const ml=document.getElementById('missList');
  ml.innerHTML='';
  if(mistakes.length>0){
    const h=document.createElement('div');h.className='miss-hdr';h.textContent='❌ 틀린 문제 ('+mistakes.length+'개) — 다시 확인해요!';ml.appendChild(h);
    mistakes.forEach(m=>{
      const d=document.createElement('div');d.className='miss-item';
      d.innerHTML='<div class="miss-top"><span class="miss-icon">'+m.icon+'</span><span class="miss-name">'+m.title+'</span></div>'
        +'<div class="miss-desc">'+m.desc+'</div>'
        +'<div class="miss-ans">✅ 정답: '+(m.type==='discrete'?'이산확률변수':'연속확률변수')+'</div>'
        +'<div class="miss-why">💡 '+m.reason+'</div>';
      ml.appendChild(d);
    });
  }
  document.getElementById('progBar').style.width='100%';
}

function restart(){init();}
init();
</script>
</body>
</html>
"""


def render():
    st.header("🎮 이산 vs 연속 확률변수 분류 게임")
    st.markdown("""
확률변수는 가질 수 있는 **값의 범위**에 따라 두 종류로 나뉩니다.

| 구분 | 이산확률변수 | 연속확률변수 |
|------|------------|------------|
| 값의 특성 | **셀 수 있는** 유한개 또는 자연수와 대응 | 어떤 **범위 안의 모든 실수** |
| 예시 | 주사위 눈, 맞힌 문제 수 | 키, 몸무게, 기온 |

아래 카드를 보고 **이산확률변수**인지 **연속확률변수**인지 분류해 보세요!
""")

    components.html(_HTML, height=760, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
