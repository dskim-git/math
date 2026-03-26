# activities/probability/mini/trial_event_vocab_game.py
"""
시행과 사건 용어 마스터 – 카드 선택 퀴즈 게임
시행, 표본공간, 사건, 근원사건의 개념을 인터랙티브 카드 게임으로 확인합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎯 시행과 사건 용어 마스터",
    "description": "시행·표본공간·사건·근원사건의 개념을 카드 선택 퀴즈 게임으로 확인합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "시행과사건"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 시행과 사건**"},
    {
        "key": "헷갈린용어",
        "label": "이 활동에서 가장 헷갈렸던 용어는? 헷갈렸던 이유도 함께 적어주세요.",
        "type": "text_area",
        "height": 80,
        "placeholder": "예) 사건과 근원사건의 차이가 헷갈렸다. 왜냐하면..."
    },
    {
        "key": "용어나만의설명",
        "label": "시행·표본공간·사건·근원사건을 자신의 말로 각각 설명해보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "시행: ...\n표본공간: ...\n사건: ...\n근원사건: ..."
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area",
        "height": 80
    },
    {
        "key": "느낀점",
        "label": "💬 이 활동을 하면서 느낀 점",
        "type": "text_area",
        "height": 80
    },
]

_GAME_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>시행과 사건 용어 마스터</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0f0c29 0%,#302b63 55%,#24243e 100%);
  color:#e2e8f0;min-height:720px;padding:14px 12px;
}
/* ── 헤더 ── */
.hdr{
  display:flex;justify-content:space-between;align-items:center;
  padding:10px 16px;background:rgba(255,255,255,.08);
  border-radius:12px;margin-bottom:14px;backdrop-filter:blur(8px);
}
.hdr-title{font-size:1.05rem;font-weight:700;color:#a78bfa;}
.score-badge{
  background:linear-gradient(135deg,#7c3aed,#4f46e5);
  border-radius:20px;padding:4px 14px;font-weight:700;font-size:.88rem;
}
/* ── 진행 바 ── */
.prog-wrap{margin-bottom:12px;}
.prog-labels{
  display:flex;justify-content:space-between;
  font-size:.78rem;color:#94a3b8;margin-bottom:5px;
}
.prog-track{
  background:rgba(255,255,255,.1);border-radius:999px;
  height:8px;overflow:hidden;
}
.prog-fill{
  height:100%;
  background:linear-gradient(90deg,#7c3aed,#06b6d4);
  border-radius:999px;transition:width .5s ease;
}
/* ── 시나리오 박스 ── */
.scenario{
  background:rgba(124,58,237,.14);
  border:1px solid rgba(124,58,237,.4);
  border-radius:12px;padding:10px 14px;margin-bottom:12px;
}
.scenario-ttl{font-size:.98rem;font-weight:700;color:#c4b5fd;margin-bottom:3px;}
.scenario-desc{font-size:.83rem;color:#94a3b8;font-family:'Courier New',monospace;}
/* ── 질문 카드 ── */
.q-card{
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  border-radius:14px;padding:14px 16px;margin-bottom:12px;
}
.concept-tag{
  display:inline-block;padding:3px 11px;border-radius:999px;
  font-size:.73rem;font-weight:600;margin-bottom:9px;
  background:linear-gradient(135deg,#0891b2,#0e7490);
}
.q-text{font-size:1.02rem;line-height:1.55;color:#f1f5f9;}
/* ── 힌트 ── */
.hint{
  background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);
  border-radius:8px;padding:8px 12px;font-size:.8rem;
  color:#fcd34d;margin-bottom:12px;
}
/* ── 선택지 그리드 ── */
.opt-grid{
  display:grid;grid-template-columns:1fr 1fr;
  gap:10px;margin-bottom:12px;
}
.opt{
  background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.15);
  border-radius:12px;padding:12px 10px;cursor:pointer;
  transition:all .2s;font-size:.86rem;line-height:1.45;
  color:#e2e8f0;text-align:center;
  min-height:62px;display:flex;align-items:center;justify-content:center;
  font-family:'Courier New',monospace;font-weight:500;
}
.opt:hover:not(.disabled){
  background:rgba(124,58,237,.28);border-color:#7c3aed;
  transform:translateY(-2px);
  box-shadow:0 4px 20px rgba(124,58,237,.35);
}
.opt.correct{
  background:rgba(16,185,129,.22);border-color:#10b981;
  color:#6ee7b7;animation:pulse .45s ease;
}
.opt.wrong{
  background:rgba(239,68,68,.15);border-color:#ef4444;
  color:#fca5a5;animation:shake .38s ease;
}
.opt.disabled{cursor:default;}
@keyframes pulse{
  0%{transform:scale(1)}50%{transform:scale(1.04)}100%{transform:scale(1)}
}
@keyframes shake{
  0%,100%{transform:translateX(0)}
  20%{transform:translateX(-6px)}40%{transform:translateX(6px)}
  60%{transform:translateX(-4px)}80%{transform:translateX(4px)}
}
/* ── 설명 ── */
.explain{
  border:1px solid rgba(16,185,129,.35);border-radius:12px;
  padding:12px 14px;margin-bottom:12px;font-size:.86rem;line-height:1.55;
  display:none;animation:slideUp .38s ease;
}
.explain.show{display:block;}
@keyframes slideUp{
  from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}
}
/* ── 다음 버튼 ── */
.btn-next{
  width:100%;padding:12px;border-radius:12px;border:none;
  background:linear-gradient(135deg,#7c3aed,#4f46e5);
  color:#fff;font-size:.98rem;font-weight:700;cursor:pointer;
  display:none;transition:all .2s;
  box-shadow:0 4px 15px rgba(124,58,237,.42);
}
.btn-next:hover{transform:translateY(-2px);box-shadow:0 6px 22px rgba(124,58,237,.52);}
.btn-next.show{display:block;}
/* ── 결과 화면 ── */
.result{display:none;text-align:center;padding:20px 10px;}
.result.show{display:block;animation:slideUp .5s ease;}
.r-emoji{font-size:3.8rem;margin-bottom:12px;}
.r-stars{font-size:1.7rem;letter-spacing:6px;margin-bottom:8px;}
.r-score{
  font-size:2.4rem;font-weight:900;
  background:linear-gradient(135deg,#a78bfa,#06b6d4);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin-bottom:6px;
}
.r-grade{font-size:1.12rem;color:#c4b5fd;font-weight:600;margin-bottom:14px;}
.r-msg{color:#94a3b8;font-size:.88rem;line-height:1.6;margin-bottom:18px;}
.r-detail{
  background:rgba(255,255,255,.06);border-radius:12px;
  padding:14px;margin-bottom:20px;text-align:left;
}
.d-row{
  display:flex;justify-content:space-between;align-items:center;
  padding:7px 0;border-bottom:1px solid rgba(255,255,255,.08);
  font-size:.83rem;
}
.d-row:last-child{border-bottom:none;}
.d-ok{color:#6ee7b7;font-weight:600;}
.d-ng{color:#fca5a5;font-weight:600;}
.btn-restart{
  padding:11px 30px;border-radius:12px;border:none;
  background:linear-gradient(135deg,#7c3aed,#06b6d4);
  color:#fff;font-size:.97rem;font-weight:700;cursor:pointer;
  box-shadow:0 4px 18px rgba(124,58,237,.42);transition:all .2s;
}
.btn-restart:hover{transform:translateY(-2px);}
</style>
</head>
<body>

<div class="hdr">
  <div class="hdr-title">🎯 시행과 사건 용어 마스터</div>
  <div>
    <span style="font-size:.78rem;color:#94a3b8;margin-right:6px;">점수</span>
    <span class="score-badge" id="scoreBadge">0 / 0</span>
  </div>
</div>

<div class="prog-wrap">
  <div class="prog-labels">
    <span id="progText">문제 1 / 10</span>
    <span id="progPct">0%</span>
  </div>
  <div class="prog-track"><div class="prog-fill" id="progFill" style="width:0%"></div></div>
</div>

<div id="qArea">
  <div class="scenario">
    <div class="scenario-ttl" id="scenTitle"></div>
    <div class="scenario-desc" id="scenDesc"></div>
  </div>
  <div class="q-card">
    <div class="concept-tag" id="cTag"></div>
    <div class="q-text" id="qText"></div>
  </div>
  <div class="hint" id="hintBox"></div>
  <div class="opt-grid" id="optGrid"></div>
  <div class="explain" id="explainBox"></div>
  <button class="btn-next" id="btnNext" onclick="nextQ()">다음 문제 →</button>
</div>

<div class="result" id="resultScreen">
  <div class="r-emoji" id="rEmoji"></div>
  <div class="r-stars" id="rStars"></div>
  <div class="r-score" id="rScore"></div>
  <div class="r-grade" id="rGrade"></div>
  <div class="r-msg" id="rMsg"></div>
  <div class="r-detail" id="rDetail"></div>
  <button class="btn-restart" onclick="restartGame()">🔄 다시 도전하기</button>
</div>

<script>
const RAW = [
  {
    sc:"🎲 시나리오 1: 주사위 1개를 던진다",
    desc:"일반 주사위(1~6면) 1개를 던지는 실험입니다.",
    q:"이 시행의 <b>표본공간 S</b>는?",
    tag:"📐 표본공간",
    opts:["S = {1, 2, 3, 4, 5, 6}","S = {홀수, 짝수}","S = {눈의 수}","S = {1, 2, 3}"],
    ans:0,
    hint:"💡 표본공간 = 시행에서 일어날 수 있는 모든 결과의 집합",
    exp:"표본공간은 시행에서 일어날 수 있는 <b>모든 결과의 집합</b>입니다.<br>주사위 눈은 1~6이므로 <b>S = {1, 2, 3, 4, 5, 6}</b>입니다."
  },
  {
    sc:"🎲 시나리오 1: 주사위 1개를 던진다",
    desc:"S = {1, 2, 3, 4, 5, 6}",
    q:"다음 중 <b>근원사건</b>에 해당하는 것은?",
    tag:"🔵 근원사건",
    opts:["{3}","{1, 2, 3, 4, 5, 6}","{홀수가 나오는 경우}","{1, 2, 3}"],
    ans:0,
    hint:"💡 근원사건 = 표본공간의 원소 단 1개로만 이루어진 사건",
    exp:"근원사건은 원소가 정확히 <b>1개</b>인 사건입니다.<br>{3}은 원소가 1개 → 근원사건 ✅<br>{1,2,3,4,5,6}은 표본공간 전체이고, {1,2,3}은 원소가 3개라 근원사건이 아닙니다."
  },
  {
    sc:"🎲 시나리오 1: 주사위 1개를 던진다",
    desc:"S = {1, 2, 3, 4, 5, 6}",
    q:"<b>홀수</b>의 눈이 나오는 사건 A는?",
    tag:"📋 사건",
    opts:["A = {1, 3, 5}","A = {2, 4, 6}","A = {1, 2, 3}","A = {3, 5}"],
    ans:0,
    hint:"💡 사건 = 표본공간의 부분집합 (조건을 만족하는 결과들의 모음)",
    exp:"홀수: 1, 3, 5 → <b>A = {1, 3, 5}</b><br>이 사건은 표본공간 S의 부분집합입니다."
  },
  {
    sc:"🎲 시나리오 1: 주사위 1개를 던진다",
    desc:"S = {1, 2, 3, 4, 5, 6}",
    q:"<b>소수</b>의 눈이 나오는 사건 B는?",
    tag:"📋 사건",
    opts:["B = {2, 3, 5}","B = {1, 3, 5}","B = {2, 4}","B = {1, 2, 3, 5}"],
    ans:0,
    hint:"💡 소수: 약수가 1과 자기 자신뿐인 수 — 1은 소수가 아님!",
    exp:"1~6 중 소수: 2, 3, 5 (1은 소수 ✗)<br>따라서 <b>B = {2, 3, 5}</b>"
  },
  {
    sc:"🪙 시나리오 2: 동전 3개를 동시에 던진다",
    desc:"앞면: H, 뒷면: T",
    q:"이 시행의 <b>표본공간의 원소 개수</b>는?",
    tag:"📐 표본공간",
    opts:["8개","6개","4개","2개"],
    ans:0,
    hint:"💡 동전 1개 → 2가지,  동전 n개 → 2ⁿ가지",
    exp:"각 동전은 H 또는 T(2가지), 동전이 3개이므로 2³ = <b>8가지</b><br>{HHH, HHT, HTH, HTT, THH, THT, TTH, TTT}"
  },
  {
    sc:"🪙 시나리오 2: 동전 3개를 동시에 던진다",
    desc:"S = {HHH, HHT, HTH, HTT, THH, THT, TTH, TTT}",
    q:"<b>앞면이 정확히 2개</b> 나오는 사건 C는?",
    tag:"📋 사건",
    opts:["C = {HHT, HTH, THH}","C = {HHH, HHT}","C = {HTT, THT, TTH}","C = {HHT, HTH}"],
    ans:0,
    hint:"💡 H가 2개, T가 1개인 경우를 모두 찾아보세요.",
    exp:"H가 2개·T가 1개인 경우: HHT, HTH, THH<br>→ <b>C = {HHT, HTH, THH}</b>"
  },
  {
    sc:"🪙 시나리오 2: 동전 3개를 동시에 던진다",
    desc:"S = {HHH, HHT, HTH, HTT, THH, THT, TTH, TTT}",
    q:"<b>모두 같은 면</b>이 나오는 사건 D는?",
    tag:"📋 사건",
    opts:["D = {HHH, TTT}","D = {HHH}","D = {TTT}","D = {HHH, HHT, TTH, TTT}"],
    ans:0,
    hint:"💡 모두 앞면이거나 모두 뒷면인 경우를 찾으세요.",
    exp:"모두 앞면(HHH) 또는 모두 뒷면(TTT)<br>→ <b>D = {HHH, TTT}</b>"
  },
  {
    sc:"🪙 시나리오 2: 동전 3개를 동시에 던진다",
    desc:"S = {HHH, HHT, HTH, HTT, THH, THT, TTH, TTT}",
    q:"다음 중 <b>근원사건</b>인 것은?",
    tag:"🔵 근원사건",
    opts:["{HTH}","{H, T}","{HHH, TTT}","{HHT, HTH, THH}"],
    ans:0,
    hint:"💡 근원사건은 원소가 반드시 1개!",
    exp:"근원사건은 원소가 정확히 <b>1개</b>인 사건입니다.<br>{HTH}: 원소 1개 → 근원사건 ✅<br>{HHH, TTT}: 원소 2개 → 근원사건 ✗"
  },
  {
    sc:"📚 시나리오 3: 용어 이해 확인",
    desc:"지금까지 배운 내용을 정리해 봅시다.",
    q:"다음 중 <b>시행</b>에 해당하는 것은?",
    tag:"⚡ 시행",
    opts:[
      "주사위를 던져 눈의 수를 관찰한다",
      "2 + 3을 계산하면 항상 5이다",
      "삼각형 내각의 합은 항상 180°이다",
      "방정식 x² = 4의 해는 ±2이다"
    ],
    ans:0,
    hint:"💡 시행: 같은 조건에서 반복 가능하고, 결과가 우연에 의해 결정되는 실험/관찰",
    exp:"시행의 조건: ① 같은 조건에서 반복 가능  ② 결과가 우연에 의해 결정<br>'주사위 던지기'는 두 조건 모두 만족 ✅<br>나머지는 결과가 항상 확정적입니다."
  },
  {
    sc:"📚 시나리오 3: 용어 이해 확인",
    desc:"동전 2개를 동시에 던진다. (앞: H, 뒤: T)",
    q:"이 시행의 <b>표본공간</b>은?",
    tag:"📐 표본공간",
    opts:["S = {HH, HT, TH, TT}","S = {HH, TT}","S = {H, T}","S = {HH, HT, TT}"],
    ans:0,
    hint:"💡 HT(1번 앞·2번 뒤)와 TH(1번 뒤·2번 앞)는 서로 다른 결과!",
    exp:"각 동전이 H 또는 T → HH, HT, TH, TT (4가지)<br><b>HT ≠ TH</b> (순서가 다르므로 별개의 결과!)<br>→ S = {HH, HT, TH, TT}"
  },
];

// ── 상태 ──────────────────────────────────────────────────────────
let cur = 0, score = 0, done = false;
let log = [];   // [{q, ok}]
let problems = [];

function shuffle(arr){
  const a=[...arr];
  for(let i=a.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
  return a;
}

function initGame(){
  // 선택지를 섞되 정답 인덱스 재계산
  problems = RAW.map(p=>{
    const idx=[0,1,2,3], sh=shuffle(idx);
    return{...p, opts:sh.map(i=>p.opts[i]), ans:sh.indexOf(p.ans)};
  });
  cur=0; score=0; done=false; log=[];
  document.getElementById('resultScreen').classList.remove('show');
  document.getElementById('qArea').style.display='block';
  renderQ();
}

function renderQ(){
  const total=problems.length;
  const p=problems[cur];
  const pct=Math.round(cur/total*100);

  // 진행
  document.getElementById('progText').textContent=`문제 ${cur+1} / ${total}`;
  document.getElementById('progPct').textContent=pct+'%';
  document.getElementById('progFill').style.width=pct+'%';
  document.getElementById('scoreBadge').textContent=`${score} / ${cur}`;

  // 시나리오
  document.getElementById('scenTitle').textContent=p.sc;
  document.getElementById('scenDesc').textContent=p.desc;

  // 태그·질문
  document.getElementById('cTag').textContent=p.tag;
  document.getElementById('qText').innerHTML=p.q;

  // 힌트
  document.getElementById('hintBox').textContent=p.hint;

  // 선택지
  const grid=document.getElementById('optGrid');
  grid.innerHTML='';
  p.opts.forEach((o,i)=>{
    const d=document.createElement('div');
    d.className='opt';
    d.innerHTML=o;
    d.onclick=()=>pick(i);
    grid.appendChild(d);
  });

  // 초기화
  const ex=document.getElementById('explainBox');
  ex.classList.remove('show');
  ex.style.background='';
  ex.style.borderColor='';
  document.getElementById('btnNext').classList.remove('show');
  done=false;
}

function pick(sel){
  if(done) return;
  done=true;
  const p=problems[cur];
  const ok=sel===p.ans;
  if(ok) score++;
  log.push({q:cur+1, ok});

  // 카드 피드백
  document.querySelectorAll('.opt').forEach((c,i)=>{
    c.classList.add('disabled');
    if(i===p.ans) c.classList.add('correct');
    else if(i===sel && !ok) c.classList.add('wrong');
  });

  // 설명
  const ex=document.getElementById('explainBox');
  ex.innerHTML=(ok?'✅ 정답! ':'❌ 틀렸습니다. ')+p.exp;
  ex.style.background=ok?'rgba(16,185,129,.1)':'rgba(239,68,68,.08)';
  ex.style.borderColor=ok?'rgba(16,185,129,.45)':'rgba(239,68,68,.4)';
  ex.classList.add('show');

  // 다음 버튼
  const btn=document.getElementById('btnNext');
  btn.textContent=cur===problems.length-1?'🏆 결과 보기':'다음 문제 →';
  btn.classList.add('show');

  // 점수 갱신
  document.getElementById('scoreBadge').textContent=`${score} / ${cur+1}`;
}

function nextQ(){
  cur++;
  if(cur>=problems.length) showResult();
  else renderQ();
}

function showResult(){
  document.getElementById('qArea').style.display='none';
  const total=problems.length;
  const pct=Math.round(score/total*100);

  document.getElementById('progFill').style.width='100%';
  document.getElementById('progText').textContent='완료!';
  document.getElementById('progPct').textContent='100%';
  document.getElementById('scoreBadge').textContent=`${score} / ${total}`;

  let emoji,stars,grade,msg;
  if(pct===100){
    emoji='🏆';stars='⭐⭐⭐';grade='완벽! 만점!';
    msg='모든 문제를 맞혔습니다! 시행과 사건의 개념을 완벽하게 이해했네요 🎉';
  }else if(pct>=80){
    emoji='🌟';stars='⭐⭐';grade='우수';
    msg='훌륭합니다! 대부분의 개념을 잘 이해했어요. 틀린 문제를 한 번 더 확인해 보세요.';
  }else if(pct>=60){
    emoji='👍';stars='⭐';grade='양호';
    msg='잘 했어요! 조금 더 연습하면 완벽해질 거예요. 다시 도전해 보세요!';
  }else{
    emoji='💪';stars='🌱';grade='분발 필요';
    msg='괜찮아요! 용어 정의를 천천히 복습하고 다시 도전해 보세요.';
  }

  document.getElementById('rEmoji').textContent=emoji;
  document.getElementById('rStars').textContent=stars;
  document.getElementById('rScore').textContent=`${score} / ${total}점`;
  document.getElementById('rGrade').textContent=grade+` (${pct}%)`;
  document.getElementById('rMsg').textContent=msg;

  const detail=document.getElementById('rDetail');
  detail.innerHTML='<div style="font-weight:700;margin-bottom:8px;font-size:.88rem;">📋 문제별 결과</div>'+
    log.map(r=>`<div class="d-row"><span>문제 ${r.q}</span><span class="${r.ok?'d-ok':'d-ng'}">${r.ok?'✅ 정답':'❌ 오답'}</span></div>`).join('');

  document.getElementById('resultScreen').classList.add('show');
}

function restartGame(){
  initGame();
}

// 시작
initGame();
</script>
</body>
</html>"""


def render():
    st.header("🎯 시행과 사건 용어 마스터")
    st.caption(
        "시행·표본공간·사건·근원사건의 개념을 카드 선택 게임으로 확인합니다. "
        "10문제를 풀고 개념을 확실히 다져보세요!"
    )

    components.html(_GAME_HTML, height=750, scrolling=False)

    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
