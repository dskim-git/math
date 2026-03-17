"""
거듭제곱 나머지 부스터
나머지정리로 큰 수의 나머지를 빠르게 구하는 게임형 활동
"""
import streamlit as st
import streamlit.components.v1 as components

from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "거듭제곱나머지부스터"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 나머지정리로 큰 수의 나머지를 구하는 과정을 직접 만들어 보세요**"},
    {
        "key": "문제1",
        "label": "문제 1 : 큰 수의 거듭제곱을 어떤 수로 나누는 문제를 하나 만들고, x-1 또는 x+1 중 어떤 식으로 연결할지 써 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "답1",
        "label": "문제 1의 답 : 대입할 x의 값과 다항식의 나머지 R을 써 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "문제2",
        "label": "문제 2 : 홀수 지수일 때와 짝수 지수일 때 나머지가 어떻게 달라질 수 있는지 예를 들어 설명해 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "답2",
        "label": "문제 2의 답 : 최종 나머지를 어떻게 정리했는지 서술해 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점", "label": "💬 느낀 점", "type": "text_area", "height": 90},
]

META = {
    "title": "🚀 거듭제곱 나머지 부스터",
    "description": "나머지정리를 이용해 거듭제곱으로 표현된 큰 수를 특정 수로 나눌 때의 나머지를 빠르게 찾는 게임형 활동입니다.",
    "order": 107,
}

_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>거듭제곱 나머지 부스터</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Trebuchet MS','Segoe UI',sans-serif;
  background:
    radial-gradient(circle at top left,rgba(251,191,36,.20),transparent 24%),
    radial-gradient(circle at top right,rgba(59,130,246,.16),transparent 28%),
    linear-gradient(155deg,#16110a 0%,#1b2433 50%,#0f172a 100%);
  color:#fff7ed;
  min-height:100vh;
  padding:14px 10px 24px;
}
.shell{max-width:1120px;margin:0 auto}
.hero{position:relative;overflow:hidden;border:1px solid rgba(251,191,36,.16);background:linear-gradient(135deg,rgba(29,19,10,.92),rgba(21,26,40,.88));border-radius:28px;padding:20px;box-shadow:0 24px 70px rgba(0,0,0,.34);margin-bottom:16px}
.hero:before{content:'';position:absolute;inset:auto -80px -120px auto;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,rgba(251,191,36,.16),transparent 72%);pointer-events:none}
.hero:after{content:'';position:absolute;inset:-100px auto auto -90px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(59,130,246,.12),transparent 72%);pointer-events:none}
.hero > *{position:relative;z-index:1}
.eyebrow{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.24);color:#fde68a;font-size:.77rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px}
.hero h1{font-size:1.9rem;line-height:1.2;color:#fff7ed;margin-bottom:8px;font-weight:900}
.hero p{max-width:780px;line-height:1.75;color:#f4dcc2;font-size:.96rem}

.hud{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0 16px}
.hud-card{padding:14px;border-radius:18px;background:linear-gradient(180deg,rgba(30,41,59,.74),rgba(17,24,39,.82));border:1px solid rgba(251,191,36,.12)}
.hud-label{font-size:.75rem;color:#f2c885;margin-bottom:6px}
.hud-value{font-size:1.26rem;font-weight:900;color:#fff7ed}
.hud-sub{font-size:.8rem;color:#d6b992;margin-top:4px}

.grid{display:grid;grid-template-columns:1.1fr .9fr;gap:14px;margin-bottom:14px}
.card{border-radius:22px;background:rgba(10,15,24,.74);border:1px solid rgba(251,191,36,.12);padding:16px}
.card-title{display:flex;align-items:center;gap:8px;font-size:.95rem;font-weight:800;color:#fde68a;margin-bottom:10px}
.problem{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;flex-wrap:wrap}
.expression{font-size:1.55rem;font-weight:900;color:#fff7ed;line-height:1.4}
.note{font-size:.91rem;line-height:1.75;color:#f4dcc2;margin-top:8px}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.badge{padding:7px 10px;border-radius:999px;background:rgba(59,130,246,.12);border:1px solid rgba(125,211,252,.2);color:#cdeeff;font-size:.8rem;font-weight:700}
.formula{min-width:250px;padding:14px 16px;border-radius:18px;background:rgba(30,41,59,.72);border:1px solid rgba(148,163,184,.16)}
.formula-label{font-size:.73rem;color:#f2c885;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px}
.formula-math{font-size:1.15rem;color:#fff7ed;min-height:40px;display:flex;align-items:center}

.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}
.step{border-radius:20px;background:rgba(10,15,24,.78);border:1px solid rgba(251,191,36,.12);padding:16px;display:flex;flex-direction:column;gap:12px;min-height:250px}
.step-num{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(251,191,36,.14);border:1px solid rgba(251,191,36,.26);color:#fde68a;font-size:.9rem;font-weight:900;flex-shrink:0}
.step-name{font-size:.98rem;font-weight:800;color:#fff7ed}
.step-desc{font-size:.84rem;line-height:1.6;color:#e3cdb6;margin-top:4px}
.choice-wrap{display:flex;flex-wrap:wrap;gap:8px}
.choice{padding:9px 12px;border-radius:14px;border:1px solid rgba(148,163,184,.18);background:rgba(30,41,59,.88);color:#fff7ed;font-size:.9rem;font-weight:800;cursor:pointer;transition:transform .18s,box-shadow .18s,border-color .18s,background .18s;user-select:none}
.choice:hover{transform:translateY(-2px);border-color:rgba(251,191,36,.38);box-shadow:0 10px 22px rgba(2,8,23,.35)}
.choice.selected{background:linear-gradient(135deg,rgba(251,191,36,.26),rgba(59,130,246,.18));border-color:#fcd34d;color:#fff7ed}
.tip{padding:11px 12px;border-radius:14px;background:rgba(59,130,246,.08);border:1px solid rgba(125,211,252,.18);font-size:.83rem;line-height:1.7;color:#d9efff}
.warn{padding:12px 14px;border-radius:14px;background:rgba(251,191,36,.10);border:1px solid rgba(251,191,36,.22);font-size:.84rem;line-height:1.75;color:#fde68a}
.feedback{min-height:24px;font-size:.86rem;font-weight:800;color:#fcd34d;margin-bottom:10px}
.actions{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.btn{border:none;border-radius:999px;padding:10px 16px;font-size:.84rem;font-weight:900;cursor:pointer;transition:transform .18s,filter .18s}
.btn:hover{transform:translateY(-1px);filter:brightness(1.06)}
.btn-check{background:linear-gradient(135deg,#f59e0b,#ea580c);color:#fff}
.btn-hint{background:rgba(59,130,246,.16);color:#dbeafe;border:1px solid rgba(125,211,252,.22)}
.btn-reset{background:rgba(71,85,105,.26);color:#dbe5f5}
.btn-next{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;display:none}
.reveal{display:none;border-radius:22px;padding:16px;background:linear-gradient(135deg,rgba(34,197,94,.16),rgba(251,191,36,.12));border:1px solid rgba(187,247,208,.22);margin-top:14px}
.reveal.show{display:block;animation:popIn .35s ease}
@keyframes popIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.reveal-title{font-size:1rem;font-weight:900;color:#f0fdf4;margin-bottom:8px}
.reveal-text{font-size:.92rem;line-height:1.8;color:#eefced}
.trail{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.trail-card{padding:11px 12px;border-radius:16px;background:rgba(15,23,42,.6);border:1px solid rgba(187,247,208,.16)}
.trail-label{font-size:.73rem;color:#bbf7d0;margin-bottom:5px}
.trail-value{font-size:.92rem;color:#f8fafc;font-weight:800;line-height:1.6}

@media (max-width:980px){
  .grid{grid-template-columns:1fr}
  .hud{grid-template-columns:repeat(3,1fr)}
  .steps{grid-template-columns:repeat(2,1fr)}
}
@media (max-width:560px){
  body{padding:10px 8px 20px}
  .hero{padding:16px}
  .hero h1{font-size:1.45rem}
  .hud{grid-template-columns:1fr}
  .steps{grid-template-columns:1fr}
  .expression{font-size:1.25rem}
  .trail{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="shell">
  <section class="hero">
    <div class="eyebrow">Remainder Booster</div>
    <h1>🚀 거듭제곱 나머지 부스터</h1>
    <p>
      큰 수를 직접 계산하지 말고, <strong>나머지정리</strong>로 순간이동하듯 나머지를 찾아 보세요.
      어떤 식은 <strong>x-1</strong>, 어떤 식은 <strong>x+1</strong>을 잡으면 지수가 커도 한 번에 정리됩니다.
    </p>
  </section>

  <div class="hud">
    <div class="hud-card">
      <div class="hud-label">현재 미션</div>
      <div class="hud-value" id="missionNow">1 / 6</div>
      <div class="hud-sub">총 6문제</div>
    </div>
    <div class="hud-card">
      <div class="hud-label">연속 성공</div>
      <div class="hud-value" id="streak">0</div>
      <div class="hud-sub">streak</div>
    </div>
    <div class="hud-card">
      <div class="hud-label">부스터 점수</div>
      <div class="hud-value" id="score">0</div>
      <div class="hud-sub">정답마다 +10</div>
    </div>
  </div>

  <div class="grid">
    <section class="card">
      <div class="card-title">🎮 이번 미션</div>
      <div class="problem">
        <div>
          <div class="expression" id="expression"></div>
          <div class="note" id="note"></div>
          <div class="badges">
            <div class="badge" id="badge1"></div>
            <div class="badge" id="badge2"></div>
          </div>
        </div>
        <div class="formula">
          <div class="formula-label">기본 틀</div>
          <div class="formula-math" id="formula"></div>
        </div>
      </div>
    </section>

    <section class="card">
      <div class="card-title">🧠 공략 힌트</div>
      <div class="tip">
        나누는 수가 밑보다 1 작으면 <strong>x-1</strong>, 밑보다 1 크면 <strong>x+1</strong>을 먼저 의심해 보세요.
        그다음 그 일차식을 0으로 만드는 값을 대입해 다항식의 나머지 R을 바로 찾으면 됩니다.
      </div>
    </section>
  </div>

  <div class="steps">
    <section class="step">
      <div style="display:flex;align-items:center;gap:10px"><div class="step-num">1</div><div class="step-name">일차식 고르기</div></div>
      <div class="step-desc">어떤 일차식으로 나머지정리를 연결할지 선택하세요.</div>
      <div class="choice-wrap" id="formChoices"></div>
    </section>
    <section class="step">
      <div style="display:flex;align-items:center;gap:10px"><div class="step-num">2</div><div class="step-name">대입값 정하기</div></div>
      <div class="step-desc">방금 고른 일차식을 0으로 만드는 값을 찾으세요.</div>
      <div class="choice-wrap" id="subChoices"></div>
    </section>
    <section class="step">
      <div style="display:flex;align-items:center;gap:10px"><div class="step-num">3</div><div class="step-name">다항식의 나머지</div></div>
      <div class="step-desc">x의 그 값을 넣었을 때 x^n의 나머지 R을 고르세요.</div>
      <div class="warn">
        여기서는 <strong>다항식의 나머지 R</strong>를 고릅니다. R이 음수일 수도 있습니다.
      </div>
      <div class="choice-wrap" id="polyRemChoices"></div>
    </section>
    <section class="step">
      <div style="display:flex;align-items:center;gap:10px"><div class="step-num">4</div><div class="step-name">최종 나머지</div></div>
      <div class="step-desc">실제 큰 수를 나누었을 때의 나머지를 선택하세요.</div>
      <div class="warn">
        <strong>최종 나머지</strong>는 0 이상 나누는 수 미만이어야 합니다. 3단계의 R과 다르면 여기서 다시 고쳐 씁니다.
      </div>
      <div class="choice-wrap" id="finalChoices"></div>
    </section>
  </div>

  <div class="feedback" id="feedback"></div>

  <div class="actions">
    <button class="btn btn-check" onclick="checkMission()">⚡ 부스터 발동</button>
    <button class="btn btn-hint" onclick="showHint()">💡 힌트</button>
    <button class="btn btn-reset" onclick="resetSelections()">↺ 선택 초기화</button>
    <button class="btn btn-next" id="nextBtn" onclick="nextMission()">다음 미션</button>
  </div>

  <section class="reveal" id="reveal">
    <div class="reveal-title">✅ 부스터 성공</div>
    <div class="reveal-text" id="revealText"></div>
    <div class="trail">
      <div class="trail-card"><div class="trail-label">선택한 일차식</div><div class="trail-value" id="trailForm"></div></div>
      <div class="trail-card"><div class="trail-label">대입값</div><div class="trail-value" id="trailSub"></div></div>
      <div class="trail-card"><div class="trail-label">다항식 나머지</div><div class="trail-value" id="trailPolyRem"></div></div>
      <div class="trail-card"><div class="trail-label">최종 나머지</div><div class="trail-value" id="trailFinal"></div></div>
    </div>
  </section>
</div>

<script>
const MISSIONS = [
  {
    title:'워밍업',
    expression:'103^100 을 102로 나눈 나머지',
    hint:'102는 103보다 1 작습니다.',
    relation:'102 = 103 - 1',
    formulaLatex:'x^{100}=(x-1)Q(x)+R',
    form:'x-1',
    sub:'1',
    polyRem:'1',
    final:'1',
    finalOptions:['0','1','2','101'],
    reveal:'x=1을 대입하면 R=1이고, 다시 x=103을 대입하면 103^{100}=102Q(103)+1 입니다.'
  },
  {
    title:'미러 점프',
    expression:'98^100 을 99로 나눈 나머지',
    hint:'99는 98보다 1 큽니다.',
    relation:'99 = 98 + 1',
    formulaLatex:'x^{100}=(x+1)Q(x)+R',
    form:'x+1',
    sub:'-1',
    polyRem:'1',
    final:'1',
    finalOptions:['1','-1','98','99'],
    reveal:'x=-1을 대입하면 R=(-1)^{100}=1 이고, x=98을 넣으면 98^{100}=99Q(98)+1 입니다.'
  },
  {
    title:'홀수 지수 트랩',
    expression:'49^31 을 50으로 나눈 나머지',
    hint:'50는 49보다 1 큽니다.',
    relation:'50 = 49 + 1',
    formulaLatex:'x^{31}=(x+1)Q(x)+R',
    form:'x+1',
    sub:'-1',
    polyRem:'-1',
    final:'49',
    finalOptions:['-1','1','49','50'],
    reveal:'x=-1을 대입하면 R=(-1)^{31}=-1 입니다. 따라서 49^{31}=50Q(49)-1 이고, 나머지는 49로 고쳐 써야 합니다.'
  },
  {
    title:'직진 부스터',
    expression:'202^35 을 201로 나눈 나머지',
    hint:'201은 202보다 1 작습니다.',
    relation:'201 = 202 - 1',
    formulaLatex:'x^{35}=(x-1)Q(x)+R',
    form:'x-1',
    sub:'1',
    polyRem:'1',
    final:'1',
    finalOptions:['0','1','35','200'],
    reveal:'x=1을 넣으면 R=1, 다시 x=202를 넣으면 202^{35}=201Q(202)+1 입니다.'
  },
  {
    title:'음수 나머지 변환',
    expression:'76^45 을 77로 나눈 나머지',
    hint:'77은 76보다 1 큽니다.',
    relation:'77 = 76 + 1',
    formulaLatex:'x^{45}=(x+1)Q(x)+R',
    form:'x+1',
    sub:'-1',
    polyRem:'-1',
    final:'76',
    finalOptions:['-1','1','76','77'],
    reveal:'x=-1을 넣으면 R=(-1)^{45}=-1 입니다. 따라서 76^{45}=77Q(76)-1 이고, 나머지는 76입니다.'
  },
  {
    title:'보너스 미션',
    expression:'1001^23 을 1000으로 나눈 나머지',
    hint:'1000은 1001보다 1 작습니다.',
    relation:'1000 = 1001 - 1',
    formulaLatex:'x^{23}=(x-1)Q(x)+R',
    form:'x-1',
    sub:'1',
    polyRem:'1',
    final:'1',
    finalOptions:['0','1','23','999'],
    reveal:'나누는 수가 밑보다 1 작으면 x-1 구조를 바로 생각하면 됩니다. 여기서는 언제나 나머지가 1입니다.'
  }
];

const state = {
  index:0,
  streak:0,
  score:0,
  solved:false,
  selected:{form:null,sub:null,polyRem:null,final:null}
};

function mathHTML(latex){
  if(window.katex){
    try{
      return katex.renderToString(latex,{throwOnError:false,displayMode:false});
    }catch(error){}
  }
  return latex;
}

function setChoices(targetId, options, key){
  const container = document.getElementById(targetId);
  container.innerHTML = '';
  options.forEach((value)=>{
    const button = document.createElement('button');
    button.className = 'choice';
    button.type = 'button';
    button.textContent = value;
    if(state.selected[key] === value) button.classList.add('selected');
    button.onclick = ()=>{
      if(state.solved) return;
      state.selected[key] = value;
      renderChoices();
    };
    container.appendChild(button);
  });
}

function renderChoices(){
  const mission = MISSIONS[state.index];
  setChoices('formChoices', ['x-1','x+1','x-2','x+2'], 'form');
  setChoices('subChoices', ['1','-1','0','2'], 'sub');
  setChoices('polyRemChoices', ['1','-1','0','2'], 'polyRem');
  setChoices('finalChoices', mission.finalOptions, 'final');
}

function renderMission(){
  const mission = MISSIONS[state.index];
  document.getElementById('missionNow').textContent = (state.index + 1) + ' / ' + MISSIONS.length;
  document.getElementById('streak').textContent = String(state.streak);
  document.getElementById('score').textContent = String(state.score);
  document.getElementById('expression').textContent = mission.expression;
  document.getElementById('note').textContent = mission.hint;
  document.getElementById('badge1').textContent = mission.title;
  document.getElementById('badge2').textContent = mission.relation;
  document.getElementById('formula').innerHTML = mathHTML(mission.formulaLatex);
  document.getElementById('feedback').textContent = '';
  document.getElementById('reveal').className = 'reveal';
  document.getElementById('nextBtn').style.display = state.solved ? 'inline-flex' : 'none';
  renderChoices();
}

function resetSelections(){
  state.selected = {form:null,sub:null,polyRem:null,final:null};
  state.solved = false;
  document.getElementById('feedback').textContent = '';
  document.getElementById('reveal').className = 'reveal';
  document.getElementById('nextBtn').style.display = 'none';
  renderChoices();
}

function showHint(){
  const mission = MISSIONS[state.index];
  document.getElementById('feedback').textContent = '힌트: ' + mission.hint + ' ' + mission.relation + ' 이 되도록 먼저 식을 맞춰 보세요.';
}

function checkMission(){
  const mission = MISSIONS[state.index];
  const selected = state.selected;
  if(!selected.form || !selected.sub || !selected.polyRem || !selected.final){
    document.getElementById('feedback').textContent = '네 단계의 선택을 모두 채운 뒤 부스터를 발동하세요.';
    return;
  }

  if(
    selected.form === mission.form &&
    selected.sub === mission.sub &&
    selected.polyRem === mission.polyRem &&
    selected.final === mission.polyRem &&
    mission.final !== mission.polyRem
  ){
    document.getElementById('feedback').textContent = '3단계까지는 맞았습니다. 하지만 R과 최종 나머지는 다를 수 있습니다. 나머지는 0 이상 나누는 수 미만으로 다시 고쳐 써야 합니다.';
    state.streak = 0;
    document.getElementById('streak').textContent = '0';
    return;
  }

  const ok = selected.form === mission.form && selected.sub === mission.sub && selected.polyRem === mission.polyRem && selected.final === mission.final;
  if(!ok){
    state.streak = 0;
    document.getElementById('streak').textContent = '0';
    document.getElementById('feedback').textContent = '조금만 더 점검해 보세요. 일차식을 0으로 만드는 값과 지수의 홀짝을 먼저 보시면 됩니다.';
    return;
  }

  state.solved = true;
  state.streak += 1;
  state.score += 10;
  document.getElementById('streak').textContent = String(state.streak);
  document.getElementById('score').textContent = String(state.score);
  document.getElementById('feedback').textContent = '정답입니다. 나머지정리 부스터가 정확히 작동했습니다.';
  document.getElementById('nextBtn').style.display = 'inline-flex';
  document.getElementById('reveal').className = 'reveal show';
  document.getElementById('revealText').innerHTML = mission.reveal;
  document.getElementById('trailForm').textContent = mission.form;
  document.getElementById('trailSub').textContent = 'x = ' + mission.sub;
  document.getElementById('trailPolyRem').textContent = 'R = ' + mission.polyRem;
  document.getElementById('trailFinal').textContent = mission.final;
}

function nextMission(){
  if(!state.solved) return;
  if(state.index < MISSIONS.length - 1){
    state.index += 1;
    resetSelections();
    renderMission();
  } else {
    document.getElementById('feedback').textContent = '모든 나머지 부스터 미션을 완료했습니다.';
    document.getElementById('nextBtn').style.display = 'none';
  }
}

resetSelections();
renderMission();
</script>
</body>
</html>
"""


def render():
    st.set_page_config(page_title="거듭제곱 나머지 부스터", layout="wide")

    st.markdown(
        """
        <style>
        .main { max-width: 100%; }
        iframe { width: 100% !important; height: 1900px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(_HTML, height=1900, scrolling=False)

    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()