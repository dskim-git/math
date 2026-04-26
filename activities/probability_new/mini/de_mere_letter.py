import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "미니: 드 메레의 편지",
    "description": "17세기 도박사 드 메레가 파스칼에게 보낸 편지 — 상금 분배 문제를 독립 사건의 확률로 탐구합니다.",
    "order": 9999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "드메레의편지"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 드 메레의 편지**"},
    {
        "key": "B승리확률",
        "label": "(1) 게임 중단 시점(A:2승, B:1승)에서 B가 남은 게임을 연속으로 이겨 최종 승리할 확률을 구하고, 각 게임 결과가 독립 사건인 이유를 설명해 보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "P(B가 4게임 이김) = 1/2, P(B가 5게임 이김) = 1/2, 두 사건은 독립이므로...",
    },
    {
        "key": "A승리확률",
        "label": "(2) 중단 시점에서 A가 최종 승리할 확률을 구해 보세요. (여사건을 이용하거나 경우를 직접 나열해도 됩니다.)",
        "type": "text_area",
        "height": 90,
        "placeholder": "A가 이기는 경우: ① 4게임에서 A 승, ② 4게임에서 B 승 + 5게임에서 A 승...",
    },
    {
        "key": "파스칼분배",
        "label": "(3) 파스칼의 분배 방식(A:48, B:16)이 공평하다고 생각하나요? 확률을 근거로 자신의 생각을 설명해 보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "A의 최종 승리 확률 3/4이므로 64의 3/4인 48 피스톨이 A의 몫...",
    },
    {
        "key": "독립사건연결",
        "label": "(4) 이 문제에서 '독립 사건'이 왜 핵심 개념인지 설명해 보세요. 만약 각 게임 결과가 독립이 아니었다면 어떻게 달라질까요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "각 게임 결과가 이전 게임에 영향을 받는다면 P(B가 2연승)을 단순히 1/2 × 1/2로 계산할 수 없어서...",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 새롭게 알게 된 점",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 느낀 점",
        "type": "text_area",
        "height": 80,
    },
]

# ── Tab HTMLs (각 탭은 독립된 완전한 HTML — st.tabs() 패턴으로 버튼 클릭 정상 동작) ──────

_HTML_LETTER = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;background:#0e1117;color:#e0e0e0;padding:14px;line-height:1.5;font-size:14px}
.sc{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px 22px}
.sc-title{font-size:16px;font-weight:700;color:#ffd54f;margin-bottom:14px}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;border:none;border-radius:10px;cursor:pointer;font-size:13px;font-weight:700;font-family:inherit;transition:all .2s}
.btn:hover{transform:translateY(-2px)}
.bg{background:linear-gradient(135deg,#F9A825,#F57F17);color:#1a0f00;box-shadow:0 4px 14px rgba(249,168,37,.3)}
.lw{background:linear-gradient(135deg,#1a1000,#2a1a00,#1a1000);border:2px solid #8B6914;border-radius:12px;padding:22px 26px;position:relative;overflow:hidden}
.lw::after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 28px,rgba(139,105,20,0.06) 28px,rgba(139,105,20,0.06) 29px);pointer-events:none}
.lhdr{color:#A0852A;font-size:12px;font-style:italic;text-align:right;margin-bottom:14px;opacity:.8}
.ltxt{color:#F0D080;font-size:13.5px;line-height:2;min-height:60px;position:relative;z-index:1}
.cursor{display:inline-block;width:2px;height:1em;background:#F0D080;animation:blink .8s infinite;vertical-align:text-bottom;margin-left:1px}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.hl-gold{color:#FFD700;font-weight:bold}
.hint{background:rgba(255,213,79,.06);border:1px solid rgba(255,213,79,.2);border-radius:10px;padding:12px 16px;margin-top:14px;font-size:13px;color:#ffd54f;text-align:center;display:none}
</style></head><body>
<div class="sc">
  <div class="sc-title">✉️ 드 메레의 편지 — 1654년 파리</div>
  <div class="lw">
    <div class="lhdr">파리, 1654년 여름 — 드 메레(de Méré)가 파스칼(Pascal)에게</div>
    <div class="ltxt" id="ltxt"><span class="cursor" id="cur"></span></div>
  </div>
  <div style="text-align:center;margin-top:14px" id="startBtn">
    <button class="btn bg" onclick="startLetter()">✉️ 편지 읽기</button>
  </div>
  <div class="hint" id="hint">
    📌 편지를 다 읽었나요? 위의 <strong>'🎮 게임 상황'</strong> 탭으로 이동하세요!
  </div>
</div>
<script>
const SEGS=[
  {t:'"파스칼, 나는 심각한 문제에 봉착했네. ',d:28},
  {t:'실력이 비슷한 A와 B가 각각 32피스톨(화폐 단위)을 걸고 게임을 했네. ',d:22,c:'gold'},
  {t:'총 5번의 게임을 하는데 3번을 먼저 이긴 사람이 64피스톨을 모두 가지기로 했지. ',d:22},
  {t:'그런데 A가 2번, B가 1번을 이긴 상황에서 ',d:35,c:'gold'},
  {t:'일이 생겨 게임을 그만둘 수밖에 없었네.',d:30},
  {t:'\\n\\n',d:80},
  {t:'여기서 문제가 생겼다네. ',d:35},
  {t:'다시 돈을 반씩 나누자니 두 번이나 이긴 A가 너무 억울할 것 같고, ',d:22},
  {t:'A에게 64피스톨을 다 주면 B가 남은 두 번을 모두 이길 수도 있으니 이 방법 역시 공평하지 않은 듯하네. ',d:18},
  {t:'어떻게 이 돈을 분배하는 것이 좋겠나?"',d:28,c:'gold'},
];
let li=0,ci=0;
function startLetter(){
  document.getElementById('startBtn').style.display='none';
  li=0;ci=0;
  document.getElementById('ltxt').innerHTML='<span class="cursor" id="cur"></span>';
  typeLtr();
}
function typeLtr(){
  if(li>=SEGS.length){
    document.getElementById('ltxt').innerHTML+='<br><br><span style="color:#ffd54f;font-size:12px">— 드 메레 (de Méré) 백작</span>';
    document.getElementById('hint').style.display='block';
    return;
  }
  const seg=SEGS[li];
  const cursor=document.getElementById('cur');
  if(ci<seg.t.length){
    const ch=seg.t[ci];
    let html;
    if(ch==='\\n') html='<br>';
    else if(seg.c==='gold') html='<span class="hl-gold">'+ch+'</span>';
    else html=ch==='<'?'&lt;':ch==='>'?'&gt;':ch;
    if(cursor) cursor.insertAdjacentHTML('beforebegin',html);
    ci++;
    setTimeout(typeLtr,seg.d);
  }else{li++;ci=0;setTimeout(typeLtr,8);}
}
</script></body></html>"""

_HTML_GAME = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;background:#0e1117;color:#e0e0e0;padding:14px;line-height:1.5;font-size:14px}
.sc{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px 22px}
.sc-title{font-size:16px;font-weight:700;color:#ffd54f;margin-bottom:14px}
.ibox{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:13px 16px;margin:8px 0;font-size:13px;line-height:1.7}
.hl-gold{color:#FFD700;font-weight:bold}
.sboard{display:flex;gap:14px;justify-content:center;align-items:center;margin:14px 0;flex-wrap:wrap}
.pcard{background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);border-radius:14px;padding:14px 26px;text-align:center;min-width:130px}
.pcard.lead{border-color:#ffd54f;background:rgba(255,213,79,0.07);box-shadow:0 0 22px rgba(255,213,79,0.12)}
.pname{font-size:22px;font-weight:900;color:#fff}
.pwins{font-size:50px;font-weight:900;line-height:1.1}
.pw-a{color:#64B5F6}.pw-b{color:#FF8A65}
.plbl{font-size:10px;color:#78909c;margin-top:4px;letter-spacing:.06em;text-transform:uppercase}
.wdots{display:flex;gap:6px;justify-content:center;margin-top:8px}
.wdot{width:14px;height:14px;border-radius:50%;background:rgba(255,255,255,0.12);border:2px solid rgba(255,255,255,0.2)}
.wdot.fa{background:#64B5F6;border-color:#64B5F6;box-shadow:0 0 8px rgba(100,181,246,.6)}
.wdot.fb{background:#FF8A65;border-color:#FF8A65;box-shadow:0 0 8px rgba(255,138,101,.6)}
.need{font-size:10px;color:#546e7a;text-align:center;margin-top:5px}
.vsbadge{font-size:24px;font-weight:900;color:#546e7a}
.stop{background:rgba(239,83,80,.12);border:1px solid rgba(239,83,80,.35);border-radius:10px;padding:11px 18px;text-align:center;color:#EF5350;font-size:14px;font-weight:bold;margin:10px 0;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.65}}
.guess-row{display:flex;align-items:center;gap:14px;justify-content:center;flex-wrap:wrap;margin:10px 0}
input[type=range]{width:170px;-webkit-appearance:none;height:6px;border-radius:3px;background:linear-gradient(90deg,#64B5F6,#FF8A65);outline:none;cursor:pointer}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#fff;border:3px solid #ffd54f;cursor:pointer;box-shadow:0 0 10px rgba(255,213,79,.5)}
.hint{background:rgba(255,213,79,.04);border:1px solid rgba(255,213,79,.15);border-radius:10px;padding:12px 16px;margin-top:14px;font-size:13px;color:#ffd54f;text-align:center}
</style></head><body>
<div class="sc">
  <div class="sc-title">🎮 게임 현황 — 중단 시점</div>
  <div style="text-align:center;color:#90caf9;font-size:13px;margin-bottom:12px">
    총 5번의 게임 중 <span class="hl-gold">먼저 3승</span>을 거두는 사람이
    <span class="hl-gold">64 피스톨</span>을 모두 가져갑니다
  </div>
  <div class="sboard">
    <div class="pcard lead">
      <div class="pname">A</div>
      <div class="pwins pw-a">2</div>
      <div class="plbl">현재 승수</div>
      <div class="wdots">
        <div class="wdot fa"></div><div class="wdot fa"></div><div class="wdot"></div>
      </div>
      <div class="need">3승까지 1승 더 필요</div>
    </div>
    <div class="vsbadge">VS</div>
    <div class="pcard">
      <div class="pname">B</div>
      <div class="pwins pw-b">1</div>
      <div class="plbl">현재 승수</div>
      <div class="wdots">
        <div class="wdot fb"></div><div class="wdot"></div><div class="wdot"></div>
      </div>
      <div class="need">3승까지 2승 더 필요</div>
    </div>
  </div>
  <div class="stop">⚠️ 갑작스러운 사정으로 게임이 중단되었습니다!</div>
  <div class="ibox" style="margin-top:12px">
    <div style="font-size:13px;font-weight:bold;color:#ffd54f;margin-bottom:8px">💰 어떻게 나누는 게 공평할까?</div>
    <div style="display:flex;flex-direction:column;gap:8px;font-size:13px;color:#b0bec5">
      <div style="display:flex;align-items:center;gap:10px;padding-bottom:7px;border-bottom:1px solid rgba(255,255,255,.06)">
        <span style="font-size:18px">🤔</span>
        <span><strong style="color:#FF8A65">방법 1: 반반</strong> — 각자 32 피스톨
          <span style="color:#EF5350;font-size:12px"> → A가 억울하지 않을까?</span></span>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span style="font-size:18px">🤔</span>
        <span><strong style="color:#64B5F6">방법 2: A에게 전부</strong> — A가 64 피스톨
          <span style="color:#EF5350;font-size:12px"> → B에게 불공평하지 않을까?</span></span>
      </div>
    </div>
  </div>
  <div style="margin-top:14px">
    <div style="font-size:13px;color:#78909c;text-align:center;margin-bottom:10px">
      🎯 당신이 생각하는 <strong style="color:#ffd54f">A의 공평한 몫</strong>은?
    </div>
    <div class="guess-row">
      <input type="range" id="gslider" min="0" max="64" value="32" step="1" oninput="upGuess()">
      <div>
        <span style="color:#64B5F6;font-weight:bold;font-size:17px">A: <span id="gA">32</span></span>
        <span style="color:#546e7a;margin:0 8px">|</span>
        <span style="color:#FF8A65;font-weight:bold;font-size:17px">B: <span id="gB">32</span></span>
        <span style="font-size:12px;color:#78909c"> 피스톨</span>
      </div>
    </div>
  </div>
  <div class="hint">📌 예측해 봤나요? 다음 탭 <strong>'🎲 시뮬레이션'</strong>으로 이동하세요!</div>
</div>
<script>
function upGuess(){
  const v=parseInt(document.getElementById('gslider').value);
  document.getElementById('gA').textContent=v;
  document.getElementById('gB').textContent=64-v;
}
</script>
</body></html>"""

_HTML_SIM = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;background:#0e1117;color:#e0e0e0;padding:14px;line-height:1.5;font-size:14px}
.sc{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px 22px}
.sc-title{font-size:16px;font-weight:700;color:#ffd54f;margin-bottom:14px}
.ibox{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:13px 16px;margin:8px 0;font-size:13px;line-height:1.7}
.ibox.blue{background:rgba(100,181,246,.06);border-color:rgba(100,181,246,.2)}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;border:none;border-radius:10px;cursor:pointer;font-size:13px;font-weight:700;font-family:inherit;transition:all .2s}
.btn:hover{transform:translateY(-2px)}
.btn:disabled{opacity:.45;cursor:not-allowed;transform:none!important}
.bp{background:linear-gradient(135deg,#1565c0,#0d47a1);color:#fff;box-shadow:0 4px 14px rgba(21,101,192,.3)}
.bs{background:linear-gradient(135deg,#2E7D32,#4CAF50);color:#fff;box-shadow:0 4px 14px rgba(76,175,80,.3)}
.br{background:linear-gradient(135deg,#B71C1C,#E53935);color:#fff}
.cstage{display:flex;gap:18px;justify-content:center;align-items:center;margin:14px 0;min-height:90px;flex-wrap:wrap}
.cwrap{display:flex;flex-direction:column;align-items:center;position:relative;padding-bottom:26px}
.coin{width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;border:3px solid transparent;transition:all .3s;user-select:none}
.coin.pend{background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.12);color:#37474f}
.coin.flp{animation:cspin .6s ease-in-out}
@keyframes cspin{0%{transform:rotateY(0deg)}50%{transform:rotateY(90deg) scale(.8)}100%{transform:rotateY(0deg)}}
.coin.ca{background:rgba(100,181,246,.15);border-color:#64B5F6;color:#64B5F6;box-shadow:0 0 18px rgba(100,181,246,.3)}
.coin.cb{background:rgba(255,138,101,.15);border-color:#FF8A65;color:#FF8A65;box-shadow:0 0 18px rgba(255,138,101,.3)}
.coin.csk{background:rgba(255,255,255,.02);border-color:rgba(255,255,255,.07);color:#263238}
.clbl{position:absolute;bottom:-2px;font-size:10px;color:#546e7a;white-space:nowrap}
.arr{color:#37474f;font-size:22px}
.rbadge{margin-top:14px;padding:10px 18px;border-radius:10px;font-size:14px;font-weight:bold;text-align:center;display:none}
.rbadge.ra{background:rgba(100,181,246,.12);border:1px solid #64B5F6;color:#64B5F6;display:block}
.rbadge.rb{background:rgba(255,138,101,.12);border:1px solid #FF8A65;color:#FF8A65;display:block}
.simgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:12px 0}
.sbox{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:12px;text-align:center}
.sbox .num{font-size:26px;font-weight:900;color:#e0e0e0}
.sbox .lbl{font-size:10px;color:#78909c;margin-top:4px;text-transform:uppercase;letter-spacing:.05em}
.pw-a{color:#64B5F6}.pw-b{color:#FF8A65}
.barwrap{margin:12px 0}
.barlabels{display:flex;justify-content:space-between;margin-bottom:6px;font-size:13px}
.bartrack{height:28px;background:rgba(255,255,255,.05);border-radius:14px;overflow:hidden;display:flex;position:relative}
.bara{height:100%;background:linear-gradient(90deg,#1565c0,#42a5f5);border-radius:14px 0 0 14px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:bold;color:#fff;transition:width .7s cubic-bezier(.4,0,.2,1);min-width:2px}
.barb{height:100%;background:linear-gradient(90deg,#d84315,#ff7043);border-radius:0 14px 14px 0;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:bold;color:#fff;transition:width .7s cubic-bezier(.4,0,.2,1);min-width:2px}
.barmark{position:absolute;top:0;bottom:0;width:2px;background:rgba(255,255,255,.45);pointer-events:none}
</style></head><body>
<div class="sc">
  <div class="sc-title">🎲 만약 게임이 계속되었다면?</div>
  <div class="ibox blue" style="margin-bottom:14px">
    각 게임에서 A·B가 이길 확률은 동일하게 <strong>1/2</strong>입니다.<br>
    <span style="color:#64B5F6">A는 1승</span>만 더 필요하고,
    <span style="color:#FF8A65">B는 2승</span>이 더 필요합니다.<br>
    <span style="color:#ffd54f;font-size:12px">▶ 버튼을 눌러 나머지 게임을 돌려보세요!</span>
  </div>
  <div class="ibox" style="padding:16px">
    <div style="font-size:11px;color:#546e7a;text-align:center;letter-spacing:.06em;text-transform:uppercase;margin-bottom:12px">한 번 시뮬레이션</div>
    <div class="cstage">
      <div class="cwrap">
        <div class="coin pend" id="c4">4게임</div>
        <div class="clbl">4번째 게임</div>
      </div>
      <div class="arr">→</div>
      <div class="cwrap">
        <div class="coin pend" id="c5">5게임</div>
        <div class="clbl">5번째 게임</div>
      </div>
      <div class="arr">→</div>
      <div class="cwrap">
        <div class="coin pend" id="cres" style="width:80px;height:80px;font-size:13px">결과</div>
        <div class="clbl">최종 승자</div>
      </div>
    </div>
    <div id="srbadge" class="rbadge"></div>
    <div style="text-align:center;margin-top:12px">
      <button class="btn bp" id="s1btn" onclick="simOne()">🎲 한 번 실행</button>
    </div>
  </div>
  <div class="ibox" style="padding:16px;margin-top:10px">
    <div style="font-size:11px;color:#546e7a;text-align:center;letter-spacing:.06em;text-transform:uppercase;margin-bottom:12px">몬테카를로 시뮬레이션</div>
    <div class="simgrid">
      <div class="sbox"><div class="num" id="totN">0</div><div class="lbl">총 횟수</div></div>
      <div class="sbox"><div class="num pw-a" id="aN">0</div><div class="lbl">A 최종 승리</div></div>
      <div class="sbox"><div class="num pw-b" id="bN">0</div><div class="lbl">B 최종 승리</div></div>
    </div>
    <div class="barwrap">
      <div class="barlabels">
        <span style="color:#64B5F6">A 승리 <span id="apct">-</span></span>
        <span style="color:#FF8A65">B 승리 <span id="bpct">-</span></span>
      </div>
      <div class="bartrack">
        <div class="bara" id="barA" style="width:50%"></div>
        <div class="barb" id="barB" style="width:50%"></div>
        <div class="barmark" style="left:75%" title="이론값 A=75%"></div>
      </div>
      <div style="font-size:10px;color:#37474f;text-align:right;margin-top:3px">│ 이론값 A=75%</div>
    </div>
    <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
      <button class="btn bs" onclick="mc(100)">▶ 100번</button>
      <button class="btn bs" onclick="mc(1000)">▶▶ 1,000번</button>
      <button class="btn bs" onclick="mc(10000)">▶▶▶ 10,000번</button>
      <button class="btn br" onclick="rst()">↺ 초기화</button>
    </div>
  </div>
</div>
<script>
let tot=0,aw=0,bw=0,running=false;
function simGame(){
  const g4=Math.random()<.5?'A':'B';
  if(g4==='A') return{g4,g5:null,w:'A'};
  const g5=Math.random()<.5?'A':'B';
  return{g4,g5,w:g5};
}
function sleep(ms){return new Promise(r=>setTimeout(r,ms));}
async function simOne(){
  if(running)return;
  running=true;
  const btn=document.getElementById('s1btn');
  btn.disabled=true;
  const c4=document.getElementById('c4'),c5=document.getElementById('c5');
  const cr=document.getElementById('cres'),rb=document.getElementById('srbadge');
  c4.className='coin pend';c4.textContent='4게임';
  c5.className='coin pend';c5.textContent='5게임';
  cr.className='coin pend';cr.textContent='결과';
  rb.className='rbadge';rb.textContent='';
  c4.classList.add('flp');
  await sleep(650);
  const r=simGame();
  if(r.g4==='A'){
    c4.className='coin ca';c4.textContent='A 승!';
    c5.className='coin csk';c5.textContent='불필요';
    await sleep(400);
    cr.className='coin ca';cr.textContent='🏆 A';
    rb.className='rbadge ra';rb.textContent='🎉 A 최종 승리! (3승 1패)';
  }else{
    c4.className='coin cb';c4.textContent='B 승!';
    await sleep(400);
    c5.classList.add('flp');
    await sleep(650);
    if(r.g5==='A'){
      c5.className='coin ca';c5.textContent='A 승!';
      await sleep(400);
      cr.className='coin ca';cr.textContent='🏆 A';
      rb.className='rbadge ra';rb.textContent='🎉 A 최종 승리! (3승 2패)';
    }else{
      c5.className='coin cb';c5.textContent='B 승!';
      await sleep(400);
      cr.className='coin cb';cr.textContent='🏆 B';
      rb.className='rbadge rb';rb.textContent='🎊 B 역전 승리! (2승 3패)';
    }
  }
  tot++;if(r.w==='A')aw++;else bw++;
  updStats();
  running=false;btn.disabled=false;
}
function mc(n){
  for(let i=0;i<n;i++){const r=simGame();if(r.w==='A')aw++;else bw++;}
  tot+=n;updStats();
}
function updStats(){
  document.getElementById('totN').textContent=tot.toLocaleString();
  document.getElementById('aN').textContent=aw.toLocaleString();
  document.getElementById('bN').textContent=bw.toLocaleString();
  if(tot>0){
    const ap=(aw/tot*100).toFixed(1),bp=(bw/tot*100).toFixed(1);
    document.getElementById('apct').textContent=ap+'%';
    document.getElementById('bpct').textContent=bp+'%';
    document.getElementById('barA').style.width=ap+'%';
    document.getElementById('barB').style.width=bp+'%';
  }
}
function rst(){
  tot=0;aw=0;bw=0;
  document.getElementById('totN').textContent='0';
  document.getElementById('aN').textContent='0';
  document.getElementById('bN').textContent='0';
  document.getElementById('apct').textContent='-';
  document.getElementById('bpct').textContent='-';
  document.getElementById('barA').style.width='50%';
  document.getElementById('barB').style.width='50%';
}
</script></body></html>"""

_HTML_PASCAL = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;background:#0e1117;color:#e0e0e0;padding:14px;line-height:1.5;font-size:14px}
.sc{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px 22px}
.sc-title{font-size:16px;font-weight:700;color:#ffd54f;margin-bottom:14px}
.ibox{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:13px 16px;margin:8px 0;font-size:13px;line-height:1.7}
.ibox.gold{background:rgba(255,213,79,.06);border-color:rgba(255,213,79,.2);color:#ffd54f}
.ibox.blue{background:rgba(100,181,246,.06);border-color:rgba(100,181,246,.2)}
.ibox.red{background:rgba(239,83,80,.06);border-color:rgba(239,83,80,.2)}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 20px;border:none;border-radius:10px;cursor:pointer;font-size:13px;font-weight:700;font-family:inherit;transition:all .2s}
.btn:hover{transform:translateY(-2px)}
.bg{background:linear-gradient(135deg,#F9A825,#F57F17);color:#1a0f00;box-shadow:0 4px 14px rgba(249,168,37,.3)}
.lw{background:linear-gradient(135deg,#1a1000,#2a1a00,#1a1000);border:2px solid #8B6914;border-radius:12px;padding:16px 20px;position:relative;overflow:hidden;margin-bottom:14px}
.lhdr{color:#A0852A;font-size:12px;font-style:italic;text-align:right;margin-bottom:8px;opacity:.8}
.pstep{background:rgba(255,213,79,.04);border:1px solid rgba(255,213,79,.13);border-radius:12px;padding:15px 18px;margin:10px 0;opacity:0;transform:translateY(18px);transition:all .55s cubic-bezier(.4,0,.2,1)}
.pstep.vis{opacity:1;transform:translateY(0)}
.snum{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;background:linear-gradient(135deg,#F9A825,#F57F17);border-radius:50%;color:#1a0f00;font-size:13px;font-weight:900;margin-right:9px;flex-shrink:0}
.stitle{font-size:14px;font-weight:700;color:#ffd54f;margin-bottom:8px;display:flex;align-items:center}
.scont{color:#b0bec5;font-size:13px;line-height:1.75;padding-left:36px}
.pgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:12px 0}
.prizec{border-radius:14px;padding:18px;text-align:center}
.prizec.pa{background:linear-gradient(135deg,rgba(21,101,192,.2),rgba(66,165,245,.08));border:2px solid rgba(66,165,245,.4)}
.prizec.pb{background:linear-gradient(135deg,rgba(216,67,21,.2),rgba(255,112,67,.08));border:2px solid rgba(255,112,67,.4)}
.pzname{font-size:20px;font-weight:900;color:#fff;margin-bottom:6px}
.pzamt{font-size:44px;font-weight:900;line-height:1.1}
.prizec.pa .pzamt{color:#64B5F6}.prizec.pb .pzamt{color:#FF8A65}
.pzunit{font-size:13px;color:#78909c;margin-top:3px}
.pzprob{font-size:12px;margin-top:8px}
.prizec.pa .pzprob{color:#90caf9}.prizec.pb .pzprob{color:#ffb294}
</style></head><body>
<div class="sc">
  <div class="sc-title">📜 파스칼의 답장</div>
  <div class="lw">
    <div class="lhdr">1654년 여름, 파스칼의 서재에서</div>
    <div style="color:#F0D080;font-size:13px;line-height:1.8;font-style:italic">
      "친애하는 드 메레, 만약 게임을 계속한다고 생각해 보게..."
    </div>
  </div>
  <div style="text-align:center;margin-bottom:14px">
    <button class="btn bg" id="revBtn" onclick="reveal()">💡 파스칼의 풀이 보기</button>
  </div>
  <div class="pstep" id="ps1">
    <div class="stitle"><span class="snum">1</span>게임을 끝까지 한다고 가정하자</div>
    <div class="scont">
      남은 최대 2번의 게임(4번째, 5번째)을 <strong style="color:#ffd54f">모두 진행</strong>한다고 가정합니다.<br>
      실제로는 먼저 3승 달성 시 끝나지만, 계산 편의를 위해 2번 모두 치른다고 봅니다.<br><br>
      <svg id="treeSvg" viewBox="0 0 480 178" style="width:100%;max-width:480px;display:block;margin:10px auto"></svg>
    </div>
  </div>
  <div class="pstep" id="ps2">
    <div class="stitle"><span class="snum">2</span>4번째 게임 결과 분석</div>
    <div class="scont">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:6px">
        <div class="ibox blue">
          <div style="color:#64B5F6;font-weight:bold;margin-bottom:5px">🏆 A 승 (확률 ½)</div>
          <div style="font-size:12px">A: 3승 달성 → A가 64 피스톨 전부 가져감</div>
        </div>
        <div class="ibox red" style="background:rgba(255,138,101,.07);border-color:rgba(255,138,101,.25)">
          <div style="color:#FF8A65;font-weight:bold;margin-bottom:5px">🎮 B 승 (확률 ½)</div>
          <div style="font-size:12px">A: 2승, B: 2승 → 동점! 5번째 게임으로</div>
        </div>
      </div>
      <div class="ibox gold" style="margin-top:10px;font-size:12px">
        💡 각 게임의 결과는 서로 <strong>독립</strong>입니다. 이전 게임 결과가 다음 게임에 영향을 주지 않아요!
      </div>
    </div>
  </div>
  <div class="pstep" id="ps3">
    <div class="stitle"><span class="snum">3</span>A는 4번째 게임 결과와 무관하게 32 피스톨은 확정</div>
    <div class="scont">
      4번째 게임에서 어떤 결과가 나오든:<br>
      <span style="color:#64B5F6">• A 승리 → A 64, B 0 피스톨</span><br>
      <span style="color:#FF8A65">• B 승리 → 동점 → 32 피스톨씩 나눠야 공평</span><br><br>
      <span style="color:#ffd54f">∴ A는 확정적으로 <strong>최소 32 피스톨</strong>을 받습니다.</span>
    </div>
  </div>
  <div class="pstep" id="ps4">
    <div class="stitle"><span class="snum">4</span>남은 32 피스톨은 5번째 게임의 기댓값으로 분배</div>
    <div class="scont">
      남은 32 피스톨은 5번째 게임 승자가 가져갑니다.<br>
      둘의 실력이 같으므로 각자 ½ 확률 → 32를 반반 나눔<br><br>
      <span style="color:#64B5F6">A의 추가 몫: 32 × ½ = <strong>16 피스톨</strong></span><br>
      <span style="color:#FF8A65">B의 추가 몫: 32 × ½ = <strong>16 피스톨</strong></span>
    </div>
  </div>
  <div class="pstep" id="ps5">
    <div class="stitle"><span class="snum">✓</span>최종 답: 공평한 상금 분배</div>
    <div class="scont">
      <div class="pgrid">
        <div class="prizec pa">
          <div class="pzname">A</div>
          <div class="pzamt">48</div>
          <div class="pzunit">피스톨</div>
          <div class="pzprob">32(확정) + 16(5번째 기댓값)<br>A 최종 승리 확률 = <strong>3/4</strong></div>
        </div>
        <div class="prizec pb">
          <div class="pzname">B</div>
          <div class="pzamt">16</div>
          <div class="pzunit">피스톨</div>
          <div class="pzprob">0(확정) + 16(5번째 기댓값)<br>B 최종 승리 확률 = <strong>1/4</strong></div>
        </div>
      </div>
      <div class="ibox gold" style="text-align:center;font-size:13px;margin-top:10px">
        64 × <strong style="color:#64B5F6">3/4</strong> = <strong style="color:#64B5F6">48</strong> 피스톨 (A의 몫)
        &nbsp;|&nbsp;
        64 × <strong style="color:#FF8A65">1/4</strong> = <strong style="color:#FF8A65">16</strong> 피스톨 (B의 몫)<br><br>
        🔑 각 게임이 <strong>독립 사건</strong>이기 때문에<br>
        P(B가 남은 2게임 모두 승) = P(B승) × P(B승) = ½ × ½ = <strong>1/4</strong>
      </div>
    </div>
  </div>
</div>
<script>
let step=0;
function reveal(){
  const steps=['ps1','ps2','ps3','ps4','ps5'];
  if(step>=steps.length)return;
  document.getElementById(steps[step]).classList.add('vis');
  step++;
  if(step===1) drawTree();
  if(step<steps.length) setTimeout(reveal,550);
  else document.getElementById('revBtn').textContent='✅ 풀이 완료!';
}
function drawTree(){
  const svg=document.getElementById('treeSvg');
  if(!svg)return;
  const W=480,H=178;
  const rx=W/2,ry=18;
  const l1ax=W*0.22,l1ay=90;
  const l1bx=W*0.78,l1by=90;
  const l2ax=W*0.62,l2ay=158;
  const l2bx=W*0.92,l2by=158;
  svg.innerHTML=`
<defs>
  <marker id="ar" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="rgba(255,255,255,.22)"/>
  </marker>
</defs>
<circle cx="${rx}" cy="${ry}" r="15" fill="rgba(255,213,79,.18)" stroke="#ffd54f" stroke-width="2"/>
<text x="${rx}" y="${ry+4}" text-anchor="middle" font-size="10" fill="#ffd54f" font-weight="bold">A:2 B:1</text>
<line x1="${rx}" y1="${ry+15}" x2="${l1ax}" y2="${l1ay-15}" stroke="rgba(100,181,246,.5)" stroke-width="1.5" marker-end="url(#ar)"/>
<text x="${(rx+l1ax)/2-28}" y="${(ry+l1ay)/2-2}" font-size="10" fill="rgba(255,255,255,.45)">A승(½)</text>
<circle cx="${l1ax}" cy="${l1ay}" r="15" fill="rgba(100,181,246,.18)" stroke="#64B5F6" stroke-width="2"/>
<text x="${l1ax}" y="${l1ay+4}" text-anchor="middle" font-size="9" fill="#64B5F6" font-weight="bold">A:3 B:1</text>
<text x="${l1ax}" y="${l1ay+30}" text-anchor="middle" font-size="11" fill="#64B5F6">🏆 A 승리</text>
<text x="${l1ax}" y="${l1ay+44}" text-anchor="middle" font-size="10" fill="rgba(100,181,246,.65)">P = ½</text>
<line x1="${rx}" y1="${ry+15}" x2="${l1bx}" y2="${l1by-15}" stroke="rgba(255,138,101,.5)" stroke-width="1.5" marker-end="url(#ar)"/>
<text x="${(rx+l1bx)/2+6}" y="${(ry+l1by)/2-2}" font-size="10" fill="rgba(255,255,255,.45)">B승(½)</text>
<circle cx="${l1bx}" cy="${l1by}" r="15" fill="rgba(255,138,101,.18)" stroke="#FF8A65" stroke-width="2"/>
<text x="${l1bx}" y="${l1by+4}" text-anchor="middle" font-size="9" fill="#FF8A65" font-weight="bold">A:2 B:2</text>
<line x1="${l1bx}" y1="${l1by+15}" x2="${l2ax}" y2="${l2ay-12}" stroke="rgba(100,181,246,.4)" stroke-width="1.5" marker-end="url(#ar)"/>
<text x="${(l1bx+l2ax)/2-22}" y="${(l1by+l2ay)/2+2}" font-size="9" fill="rgba(255,255,255,.38)">A승(½)</text>
<circle cx="${l2ax}" cy="${l2ay}" r="13" fill="rgba(100,181,246,.18)" stroke="#64B5F6" stroke-width="1.5"/>
<text x="${l2ax}" y="${l2ay+4}" text-anchor="middle" font-size="9" fill="#64B5F6" font-weight="bold">A 승리</text>
<line x1="${l1bx}" y1="${l1by+15}" x2="${l2bx}" y2="${l2by-12}" stroke="rgba(255,138,101,.4)" stroke-width="1.5" marker-end="url(#ar)"/>
<text x="${(l1bx+l2bx)/2+4}" y="${(l1by+l2by)/2+2}" font-size="9" fill="rgba(255,255,255,.38)">B승(½)</text>
<circle cx="${l2bx}" cy="${l2by}" r="13" fill="rgba(255,138,101,.18)" stroke="#FF8A65" stroke-width="1.5"/>
<text x="${l2bx}" y="${l2by+4}" text-anchor="middle" font-size="9" fill="#FF8A65" font-weight="bold">B 승리</text>
<text x="${l2ax}" y="${H-2}" text-anchor="middle" font-size="9" fill="rgba(100,181,246,.6)">P=¼</text>
<text x="${l2bx}" y="${H-2}" text-anchor="middle" font-size="9" fill="rgba(255,138,101,.6)">P=¼</text>
`;
}
</script></body></html>"""

_HTML_SUMMARY = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;background:#0e1117;color:#e0e0e0;padding:14px;line-height:1.5;font-size:14px}
.sc{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px 22px}
.sc-title{font-size:16px;font-weight:700;color:#ffd54f;margin-bottom:14px}
.ibox{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:13px 16px;margin:8px 0;font-size:13px;line-height:1.7}
.ibox.gold{background:rgba(255,213,79,.06);border-color:rgba(255,213,79,.2);color:#ffd54f}
.ibox.blue{background:rgba(100,181,246,.06);border-color:rgba(100,181,246,.2)}
.ibox.green{background:rgba(76,175,80,.06);border-color:rgba(76,175,80,.2)}
</style></head><body>
<div class="sc">
  <div class="sc-title">🧠 핵심 정리</div>
  <div class="ibox blue">
    <div style="font-size:14px;font-weight:bold;color:#64B5F6;margin-bottom:8px">📊 확률 계산</div>
    <div style="font-size:13px;color:#b0bec5;line-height:1.8">
      B가 최종 승리하려면 4번째 <strong>AND</strong> 5번째 게임을 모두 이겨야 합니다.<br>
      각 게임은 서로 <strong style="color:#ffd54f">독립</strong>이므로:<br>
      <code style="background:rgba(0,0,0,.3);padding:3px 10px;border-radius:6px;display:inline-block;margin-top:4px">
        P(B 최종 승) = P(B, 4게임) × P(B, 5게임) = ½ × ½ = <strong>1/4</strong>
      </code><br>
      <code style="background:rgba(0,0,0,.3);padding:3px 10px;border-radius:6px;display:inline-block;margin-top:4px">
        P(A 최종 승) = 1 − 1/4 = <strong>3/4</strong>
      </code>
    </div>
  </div>
  <div class="ibox gold">
    <div style="font-size:14px;font-weight:bold;margin-bottom:8px">🔑 왜 독립 사건인가?</div>
    <div style="font-size:13px;color:#b0bec5;line-height:1.8">
      각 게임에서의 승패는 이전 게임 결과와 <strong style="color:#ffd54f">무관</strong>합니다.<br>
      "4번째 게임에서 B가 이겼다"는 사건이<br>
      "5번째 게임에서 B가 이길" 확률에 영향을 주지 <strong style="color:#ffd54f">않습니다</strong>.<br>
      → 두 사건은 <strong style="color:#ffd54f">독립(independent)</strong>!
    </div>
  </div>
  <div class="ibox green">
    <div style="font-size:14px;font-weight:bold;color:#81C784;margin-bottom:8px">📜 역사적 의의</div>
    <div style="font-size:13px;color:#b0bec5;line-height:1.8">
      이 편지 왕래가 수학에서 <strong style="color:#81C784">확률론</strong>의 출발점이 되었습니다.<br>
      파스칼과 페르마가 주고받은 편지들을 통해<br>
      기댓값·확률의 개념이 최초로 수학적으로 정립되었어요.<br>
      <span style="color:#546e7a;font-size:11px">▸ 도박 문제에서 시작된 이 수학이 오늘날 통계, AI, 금융, 보험 등에 활용됩니다.</span>
    </div>
  </div>
</div>
</body></html>"""


def render():
    st.header("✉️ 드 메레의 편지 — 상금 분배와 독립 사건")
    t1, t2, t3, t4, t5 = st.tabs([
        "✉️ 편지 읽기", "🎮 게임 상황", "🎲 시뮬레이션", "📜 파스칼의 풀이", "🧠 핵심 정리"
    ])
    with t1:
        components.html(_HTML_LETTER, height=850, scrolling=False)
    with t2:
        components.html(_HTML_GAME, height=750, scrolling=False)
    with t3:
        components.html(_HTML_SIM, height=1000, scrolling=False)
    with t4:
        components.html(_HTML_PASCAL, height=1350, scrolling=False)
    with t5:
        components.html(_HTML_SUMMARY, height=650, scrolling=False)
    st.markdown("---")
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
