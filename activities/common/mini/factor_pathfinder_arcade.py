"""
인수분해 패스파인더 아케이드
다양한 인수분해 문제를 보고 적절한 풀이 전략을 분류하는 활동
"""

import streamlit as st
import streamlit.components.v1 as components

from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "인수분해패스파인더"

_QUESTIONS = [
    {
        "type": "markdown",
        "text": "**📝 오늘 연습한 5가지 인수분해 전략을 떠올리며 나만의 분류 기준을 정리해 보세요.**",
    },
    {
        "key": "문제1",
        "label": "문제 1 : 서로 다른 전략이 필요한 인수분해 문제 2개를 직접 만들어 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "답1",
        "label": "문제 1의 답 : 각 문제에 어떤 전략을 먼저 적용할지와 이유를 간단히 써 보세요.",
        "type": "text_area",
        "height": 100,
    },
    {
        "key": "문제2",
        "label": "문제 2 : 오늘 활동 중 가장 헷갈렸던 분류 사례 1개를 쓰고, 왜 헷갈렸는지 적어 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "답2",
        "label": "문제 2의 답 : 다음에 같은 유형을 만나면 어떤 순서로 판단할지 체크리스트를 만들어 보세요.",
        "type": "text_area",
        "height": 100,
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점", "label": "💬 느낀 점", "type": "text_area", "height": 90},
]

META = {
    "title": "🧭 인수분해 패스파인더 아케이드",
    "description": "문제를 보고 5가지 인수분해 전략 중 가장 적절한 길을 고르는 분류형 게임 활동입니다.",
  "order": 110,
}

_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>인수분해 패스파인더 아케이드</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','SUIT','Noto Sans KR',sans-serif;
  color:#f3f8ff;
  min-height:100vh;
  background:
    radial-gradient(circle at 8% 10%,rgba(255,186,73,.20),transparent 26%),
    radial-gradient(circle at 90% 18%,rgba(34,211,238,.22),transparent 28%),
    radial-gradient(circle at 65% 92%,rgba(74,222,128,.14),transparent 30%),
    linear-gradient(165deg,#09101f 0%,#131b2f 46%,#1a2440 100%);
  padding:16px 10px 26px;
}

:root{
  --panel:#101b2de6;
  --line:#cbd5e11f;
  --accent:#f59e0b;
  --sky:#22d3ee;
  --mint:#4ade80;
  --rose:#fb7185;
  --ink:#d9e8ff;
}

.shell{max-width:1140px;margin:0 auto}
.hero{
  border-radius:24px;
  padding:22px 22px 18px;
  border:1px solid #ffffff2a;
  background:linear-gradient(135deg,rgba(26,38,64,.92),rgba(15,26,46,.88));
  box-shadow:0 28px 70px #00000052;
  position:relative;
  overflow:hidden;
}
.hero:before,.hero:after{content:'';position:absolute;border-radius:999px;pointer-events:none}
.hero:before{width:240px;height:240px;background:radial-gradient(circle,#fbbf2463,transparent 70%);top:-120px;right:-50px}
.hero:after{width:220px;height:220px;background:radial-gradient(circle,#22d3ee55,transparent 70%);left:-80px;bottom:-130px}
.badge{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;background:#f59e0b22;border:1px solid #fcd34d4d;color:#fde68a;font-weight:800;font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;margin-bottom:10px}
.hero h1{font-size:1.95rem;line-height:1.22;margin-bottom:8px}
.hero p{font-size:.95rem;color:#c5d7f0;line-height:1.74;max-width:820px}

.method-grid{margin-top:14px;display:grid;grid-template-columns:repeat(5,1fr);gap:10px}
.method-chip{
  border-radius:14px;
  padding:11px 10px;
  border:1px solid #ffffff24;
  background:#0f172a91;
  min-height:110px;
}
.method-chip h3{font-size:.86rem;color:#f8fbff;margin-bottom:6px}
.method-chip p{font-size:.78rem;color:#b7c9e3;line-height:1.5}

.board{margin-top:14px;display:grid;grid-template-columns:1.15fr .85fr;gap:12px}
.panel{
  border-radius:20px;
  border:1px solid var(--line);
  background:var(--panel);
  backdrop-filter:blur(8px);
  padding:16px;
}
.section-title{display:flex;align-items:center;gap:8px;font-size:.92rem;font-weight:900;color:#93c5fd;margin-bottom:10px}

.hud{display:grid;grid-template-columns:repeat(2,1fr);gap:9px}
.hud-card{border-radius:14px;padding:12px;background:linear-gradient(180deg,#0f1a2b,#0c1422);border:1px solid #ffffff1f}
.hud-label{font-size:.75rem;color:#9cb4d6;margin-bottom:6px}
.hud-value{font-size:1.2rem;font-weight:900;color:#f9fdff}
.hud-sub{font-size:.78rem;color:#a9c0df;margin-top:2px}

.problem-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.problem-title{font-size:1.08rem;font-weight:900;color:#f8fbff}
.problem-note{font-size:.86rem;line-height:1.6;color:#b7cae3}
.stage-pill{padding:6px 11px;border-radius:999px;background:#22d3ee1f;border:1px solid #67e8f9a0;color:#a5f3fc;font-weight:800;font-size:.76rem}
.math-box{border-radius:16px;padding:16px;background:#0b1525;border:1px solid #cbd5e124;min-height:78px;display:flex;align-items:center;justify-content:center;font-size:1.28rem;margin-bottom:11px}

.options{display:grid;grid-template-columns:1fr;gap:8px}
.option-btn{
  border-radius:13px;
  border:1px solid #ffffff26;
  background:linear-gradient(135deg,#0f1d33,#12233f);
  color:#e6f1ff;
  text-align:left;
  padding:11px 13px;
  font-size:.9rem;
  font-weight:800;
  cursor:pointer;
  transition:transform .16s,box-shadow .16s,border-color .16s,filter .16s;
}
.option-btn span{display:block;font-size:.78rem;font-weight:500;color:#aec4e2;margin-top:4px;line-height:1.45}
.option-btn:hover{transform:translateY(-1px);box-shadow:0 10px 20px #0206175e;border-color:#bae6fd8f}
.option-btn.selected{border-color:#fcd34d;background:linear-gradient(135deg,#3b2a0b,#2a344f)}
.option-btn.correct{border-color:#4ade80;background:linear-gradient(135deg,#123422,#103324)}
.option-btn.wrong{border-color:#fb7185;background:linear-gradient(135deg,#3d1221,#321724)}
.option-btn.locked{pointer-events:none;opacity:.82}

.btn-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.btn{
  border:none;
  border-radius:999px;
  padding:9px 15px;
  font-weight:900;
  font-size:.84rem;
  cursor:pointer;
}
.btn-check{background:linear-gradient(135deg,#f59e0b,#f97316);color:#fff}
.btn-hint{background:#22d3ee24;border:1px solid #67e8f980;color:#a5f3fc}
.btn-next{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;display:none}
.btn-restart{background:#e2e8f01f;border:1px solid #cbd5e15c;color:#dbe7f6;display:none}

.feedback{min-height:26px;margin-top:8px;font-size:.86rem;font-weight:900}
.feedback.ok{color:#86efac}
.feedback.ng{color:#fda4af}

.hint{display:none;margin-top:9px;border-radius:12px;padding:10px 11px;background:#38bdf81a;border:1px solid #67e8f961;color:#bdf3ff;font-size:.82rem;line-height:1.6}
.hint.show{display:block;animation:fadeIn .25s ease}

.mini-quiz{margin-top:12px;border-radius:18px;padding:14px;background:linear-gradient(140deg,#1b283e,#112036);border:1px solid #ffffff24;display:none}
.mini-quiz.show{display:block;animation:fadeIn .3s ease}
.mini-title{font-size:.96rem;font-weight:900;color:#f8fbff;margin-bottom:8px}
.mini-problem{font-size:1.03rem;color:#f8fbff;margin:8px 0 10px;min-height:34px}
.mini-actions{display:flex;gap:8px;flex-wrap:wrap}
.mini-action{padding:8px 11px;border-radius:10px;border:1px solid #ffffff2d;background:#0f1d33;color:#e6f1ff;font-size:.82rem;font-weight:800;cursor:pointer}
.mini-action.good{border-color:#4ade80;color:#dcfce7}
.mini-action.bad{border-color:#fb7185;color:#fecdd3}
.mini-score{margin-top:9px;font-size:.84rem;color:#bbd6f5;font-weight:700}

.summary{margin-top:12px;border-radius:18px;padding:15px;background:linear-gradient(140deg,#0f3a27cc,#153e75b8);border:1px solid #86efac66;display:none}
.summary.show{display:block;animation:fadeIn .35s ease}
.summary h3{font-size:1.15rem;margin-bottom:8px}
.summary p{font-size:.9rem;color:#d9f7e7;line-height:1.7}

@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

@media (max-width:1080px){
  .method-grid{grid-template-columns:repeat(2,1fr)}
  .board{grid-template-columns:1fr}
}
@media (max-width:620px){
  body{padding:10px 7px 18px}
  .hero{padding:16px}
  .hero h1{font-size:1.55rem}
  .method-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="shell">
  <section class="hero">
    <div class="badge">Factorization Strategy Lab</div>
    <h1>🧭 인수분해 패스파인더 아케이드</h1>
    <p>
      문제를 보자마자 계산부터 시작하지 말고, 먼저 <strong>어떤 길로 갈지</strong>를 고르는 연습을 해봅시다.
      아래 다섯 전략 중 가장 알맞은 방법을 선택하고, 마지막 스피드 미니게임에서 분류 감각을 완성하세요.
    </p>

    <div class="method-grid">
      <article class="method-chip">
        <h3>① 공식 바로 적용</h3>
        <p>완전제곱식, 제곱의 차, 세제곱식 등 패턴이 바로 보일 때.</p>
      </article>
      <article class="method-chip">
        <h3>② 치환 인수분해</h3>
        <p>반복되는 식이 보이면 한 문자로 두고 단순한 식으로 바꿀 때.</p>
      </article>
      <article class="method-chip">
        <h3>③ 식 변형 후 인수분해</h3>
        <p>항을 더하고 빼서 제곱의 차나 공식 형태를 억지로 만들어 줄 때.</p>
      </article>
      <article class="method-chip">
        <h3>④ 한 문자 정리</h3>
        <p>문자가 여러 개면 한 문자 기준으로 정리해 이차식처럼 다룰 때.</p>
      </article>
      <article class="method-chip">
        <h3>⑤ 인수정리 활용</h3>
        <p>고차식에서 유리근 후보를 점검하며 일차인수를 찾아 내려갈 때.</p>
      </article>
    </div>
  </section>

  <section class="board">
    <section class="panel">
      <div class="problem-head">
        <div>
          <div class="problem-title" id="problemTitle">사례 분류 미션</div>
          <div class="problem-note" id="problemNote"></div>
        </div>
        <div class="stage-pill" id="stagePill">문제 1 / 10</div>
      </div>
      <div class="math-box" id="problemMath"></div>
      <div class="options" id="optionBox"></div>
      <div class="feedback" id="feedback"></div>
      <div class="hint" id="hint"></div>
      <div class="btn-row">
        <button class="btn btn-check" onclick="checkAnswer()">분류 확인</button>
        <button class="btn btn-hint" onclick="showHint()">힌트</button>
        <button class="btn btn-next" id="nextBtn" onclick="nextProblem()">다음 사례</button>
        <button class="btn btn-restart" id="restartBtn" onclick="restartAll()">처음부터 다시</button>
      </div>

      <section class="mini-quiz" id="miniQuizBox">
        <div class="mini-title">⚡ 최종 미니게임: 20초 전략 스냅</div>
        <p style="font-size:.82rem;color:#b7cae3;line-height:1.6">
          20초 안에 최대한 많이 맞혀 보세요. 핵심은 계산이 아니라 <strong>전략 분류 속도</strong>입니다.
        </p>
        <div class="mini-problem" id="miniProblem"></div>
        <div class="mini-actions" id="miniActions"></div>
        <div class="mini-score" id="miniScore"></div>
      </section>

      <section class="summary" id="summaryBox">
        <h3>🏁 학습 정리 완료</h3>
        <p id="summaryText"></p>
      </section>
    </section>

    <section class="panel">
      <div class="section-title">📊 진행 대시보드</div>
      <div class="hud">
        <article class="hud-card">
          <div class="hud-label">정답 개수</div>
          <div class="hud-value" id="correctCount">0</div>
          <div class="hud-sub">사례 분류 정답</div>
        </article>
        <article class="hud-card">
          <div class="hud-label">정확도</div>
          <div class="hud-value" id="accuracy">0%</div>
          <div class="hud-sub" id="accuracySub">아직 시작 전</div>
        </article>
        <article class="hud-card">
          <div class="hud-label">힌트 사용</div>
          <div class="hud-value" id="hintCount">0</div>
          <div class="hud-sub">적게 쓸수록 좋아요</div>
        </article>
        <article class="hud-card">
          <div class="hud-label">최종 게임 점수</div>
          <div class="hud-value" id="miniBest">0</div>
          <div class="hud-sub">20초 최고 기록</div>
        </article>
      </div>

      <div style="margin-top:12px;border-top:1px solid #ffffff1f;padding-top:12px">
        <div class="section-title">🧩 분류 체크포인트</div>
        <p style="font-size:.84rem;line-height:1.7;color:#b9cde9">
          1) 공식이 바로 보이는가?<br>
          2) 같은 모양이 반복되는가?<br>
          3) 항을 더하고 빼면 구조가 살아나는가?<br>
          4) 한 문자 기준으로 정리하면 쉬워지는가?<br>
          5) 고차식이라면 인수정리 후보부터 점검할 수 있는가?
        </p>
      </div>
    </section>
  </section>
</div>

<script>
const METHOD_INFO = [
  {
    id:'formula',
    name:'공식 바로 적용',
    tip:'완전제곱식, 제곱의 차, 세제곱 공식을 먼저 눈으로 찾으세요.'
  },
  {
    id:'substitution',
    name:'치환 인수분해',
    tip:'반복 블록이 보이면 t로 치환해 차수를 낮춥니다.'
  },
  {
    id:'transform',
    name:'식 변형 후 인수분해',
    tip:'필요한 항을 더하고 빼서 제곱의 차 같은 구조를 만듭니다.'
  },
  {
    id:'single_var',
    name:'한 문자 정리',
    tip:'다문자식을 한 문자에 대한 이차식처럼 정리해 봅니다.'
  },
  {
    id:'factor_theorem',
    name:'인수정리 활용',
    tip:'유리근 후보를 점검해 일차인수를 찾고 차수를 낮춥니다.'
  }
];

const BASE_CASES = [
  {
    latex:'x^2-9',
    answer:'formula',
    note:'패턴이 바로 드러나는 대표형입니다.',
    hint:'두 항이 모두 제곱이고 뺄셈입니다. $a^2-b^2$ 형태를 먼저 떠올리세요.'
  },
  {
    latex:'x^4+2x^2+1',
    answer:'substitution',
    note:'같은 모양의 항이 반복됩니다.',
    hint:'$x^2$를 하나의 문자로 보면 $t^2+2t+1$입니다.'
  },
  {
    latex:'x^4+x^2+1',
    answer:'transform',
    note:'이미지 예시처럼 식을 다듬어 구조를 만듭니다.',
    hint:'$x^4+2x^2+1- x^2$처럼 더하고 빼면 제곱의 차로 이어집니다.'
  },
  {
    latex:'2x^2+xy-y^2+3x+1',
    answer:'single_var',
    note:'문자가 두 개 이상일 때 정리 기준을 먼저 잡습니다.',
    hint:'$x$에 대한 이차식으로 묶어 보면 계수가 $y$를 포함하는 형태가 됩니다.'
  },
  {
    latex:'2x^3-5x^2-4x+3',
    answer:'factor_theorem',
    note:'삼차식 이상에서는 후보 점검이 강력합니다.',
    hint:'상수항 약수와 최고차항 계수 약수로 유리근 후보를 먼저 정리하세요.'
  },
  {
    latex:'y^4-10y^2+9',
    answer:'substitution',
    note:'제곱 항이 반복되는 전형적인 치환형입니다.',
    hint:'$t=y^2$로 치환하면 $t^2-10t+9$로 단순해집니다.'
  },
  {
    latex:'a^2+2ab+b^2-16',
    answer:'formula',
    note:'완전제곱식과 제곱의 차 공식을 연속으로 적용하는 유형입니다.',
    hint:'앞의 세 항이 $(a+b)^2$이고, 전체는 $(a+b)^2-4^2$ 꼴입니다.'
  },
  {
    latex:'x^2y-xy^2+y^2z-yz^2+z^2x-zx^2',
    answer:'single_var',
    note:'여러 문자식은 구조를 정리하며 공통 인수를 찾습니다.',
    hint:'같은 차수, 같은 문자 조합을 기준으로 순서를 정리해 보세요.'
  },
  {
    latex:'8m^3+1',
    answer:'formula',
    note:'세제곱 공식이 바로 보이는 문제입니다.',
    hint:'$(2m)^3+1^3$로 보면 합의 세제곱 공식을 바로 적용할 수 있습니다.'
  },
  {
    latex:'3x^4+3x^2+x+8',
    answer:'factor_theorem',
    note:'고차식에서는 유리근 후보 탐색으로 시작합니다.',
    hint:'유리근이 없을 수도 있지만, 출발은 후보 점검입니다.'
  }
];

const MINI_ROUND = [
  {latex:'x^2-6x+9', answer:'formula'},
  {latex:'x^4-5x^2+4', answer:'substitution'},
  {latex:'x^4+3x^2+4', answer:'transform'},
  {latex:'x^2+xy-2y^2', answer:'single_var'},
  {latex:'x^3-6x^2+11x-6', answer:'factor_theorem'},
  {latex:'a^4-1', answer:'transform'},
  {latex:'z^4+4z^2+4', answer:'substitution'},
  {latex:'p^3-27', answer:'formula'},
  {latex:'x^2y+3xy+2y', answer:'single_var'},
  {latex:'2x^3+x^2-8x-4', answer:'factor_theorem'}
];

const state = {
  index:0,
  cases:[],
  selected:'',
  checked:false,
  correct:0,
  attempts:0,
  hints:0,
  bestMini:0,
  miniRunning:false,
  miniTime:20,
  miniScore:0,
  miniIndex:0,
  miniTicker:null
};

function renderMath(latex){
  if(window.katex){
    try{return katex.renderToString(latex,{throwOnError:false,displayMode:false});}
    catch(error){}
  }
  return latex;
}

function renderInlineMathText(text){
  if(!window.katex) return text;
  return text.replace(/\$([^$]+)\$/g,(match, expr)=>{
    try{
      return katex.renderToString(expr,{throwOnError:false,displayMode:false});
    }catch(error){
      return match;
    }
  });
}

function waitForKatexAndRerender(){
  if(window.katex) return;
  let attempts = 0;
  const timer = setInterval(()=>{
    attempts += 1;
    if(window.katex){
      clearInterval(timer);
      renderCase();
      if(state.miniRunning) renderMiniProblem();
    }
    if(attempts >= 60) clearInterval(timer);
  },120);
}

function setHud(){
  document.getElementById('correctCount').textContent = String(state.correct);
  const acc = state.attempts ? Math.round((state.correct / state.attempts) * 100) : 0;
  document.getElementById('accuracy').textContent = acc + '%';
  document.getElementById('accuracySub').textContent = state.attempts ? '시도 ' + state.attempts + '회' : '아직 시작 전';
  document.getElementById('hintCount').textContent = String(state.hints);
  document.getElementById('miniBest').textContent = String(state.bestMini);
}

function buildOptions(){
  const wrap = document.getElementById('optionBox');
  wrap.innerHTML = '';
  METHOD_INFO.forEach((method)=>{
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'option-btn';
    btn.innerHTML = method.name + '<span>' + method.tip + '</span>';
    if(state.selected === method.id) btn.classList.add('selected');
    if(state.checked){
      btn.classList.add('locked');
      if(method.id === state.cases[state.index].answer) btn.classList.add('correct');
      else if(state.selected === method.id) btn.classList.add('wrong');
    }
    btn.onclick = ()=>selectOption(method.id);
    wrap.appendChild(btn);
  });
}

function selectOption(id){
  if(state.checked) return;
  state.selected = id;
  buildOptions();
}

function resetFeedback(){
  const fb = document.getElementById('feedback');
  fb.textContent = '';
  fb.className = 'feedback';
}

function renderCase(){
  const current = state.cases[state.index];
  document.getElementById('problemTitle').textContent = '사례 ' + (state.index + 1) + ' - 어떤 전략이 가장 먼저 적절할까?';
  document.getElementById('problemNote').textContent = current.note;
  document.getElementById('problemMath').innerHTML = renderMath(current.latex);
  document.getElementById('stagePill').textContent = '문제 ' + (state.index + 1) + ' / ' + state.cases.length;
  document.getElementById('hint').className = 'hint';
  document.getElementById('hint').innerHTML = renderInlineMathText(current.hint);
  document.getElementById('nextBtn').style.display = 'none';
  document.getElementById('summaryBox').classList.remove('show');
  resetFeedback();
  buildOptions();
  setHud();
}

function showHint(){
  const hint = document.getElementById('hint');
  if(!hint.classList.contains('show')){
    state.hints += 1;
    setHud();
  }
  hint.classList.add('show');
}

function checkAnswer(){
  if(state.checked || !state.selected) return;
  const current = state.cases[state.index];
  state.attempts += 1;
  const ok = state.selected === current.answer;
  if(ok) state.correct += 1;
  state.checked = true;
  const fb = document.getElementById('feedback');
  const answerName = METHOD_INFO.find((item)=>item.id === current.answer).name;
  fb.textContent = ok
    ? '정답입니다. 이 사례는 "' + answerName + '" 접근이 가장 자연스럽습니다.'
    : '이번 사례의 핵심 전략은 "' + answerName + '" 입니다. 포인트를 다시 확인해 보세요.';
  fb.className = ok ? 'feedback ok' : 'feedback ng';
  buildOptions();
  if(state.index < state.cases.length - 1){
    document.getElementById('nextBtn').style.display = 'inline-flex';
  } else {
    finishLearning();
  }
  setHud();
}

function nextProblem(){
  if(!state.checked) return;
  state.index += 1;
  state.selected = '';
  state.checked = false;
  renderCase();
}

function finishLearning(){
  const box = document.getElementById('summaryBox');
  const text = document.getElementById('summaryText');
  const acc = state.attempts ? Math.round((state.correct / state.attempts) * 100) : 0;
  let guide = '분류 정확도 ' + acc + '%입니다. ';
  if(acc >= 90) guide += '전략 선택 감각이 매우 좋습니다. 이제 실제 계산에서도 시작점을 빠르게 잡을 수 있습니다.';
  else if(acc >= 70) guide += '대부분 잘 분류했습니다. 헷갈린 유형은 힌트 문장을 다시 보며 기준을 고정해 보세요.';
  else guide += '아직 기준이 흔들립니다. 계산 전에 체크포인트 5문항을 먼저 확인하는 습관을 추천합니다.';
  text.textContent = guide;
  box.classList.add('show');
  document.getElementById('restartBtn').style.display = 'inline-flex';
  showMiniQuiz();
}

function shuffle(arr){
  const list = arr.slice();
  for(let i=list.length-1;i>0;i--){
    const j = Math.floor(Math.random()*(i+1));
    const tmp = list[i];
    list[i] = list[j];
    list[j] = tmp;
  }
  return list;
}

let miniDeck = [];

function showMiniQuiz(){
  document.getElementById('miniQuizBox').classList.add('show');
  startMiniRound();
}

function startMiniRound(){
  if(state.miniTicker) clearInterval(state.miniTicker);
  state.miniRunning = true;
  state.miniTime = 20;
  state.miniScore = 0;
  state.miniIndex = 0;
  miniDeck = shuffle(MINI_ROUND);
  renderMiniProblem();
  state.miniTicker = setInterval(()=>{
    state.miniTime -= 1;
    if(state.miniTime <= 0){
      endMiniRound();
    }
    updateMiniScore();
  },1000);
  updateMiniScore();
}

function renderMiniProblem(){
  if(!state.miniRunning) return;
  const problem = miniDeck[state.miniIndex % miniDeck.length];
  document.getElementById('miniProblem').innerHTML = renderMath(problem.latex);
  const actionWrap = document.getElementById('miniActions');
  actionWrap.innerHTML = '';
  METHOD_INFO.forEach((method)=>{
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'mini-action';
    button.textContent = method.name;
    button.onclick = ()=>miniPick(method.id, button);
    actionWrap.appendChild(button);
  });
}

function miniPick(id, button){
  if(!state.miniRunning) return;
  const problem = miniDeck[state.miniIndex % miniDeck.length];
  const good = id === problem.answer;
  if(good){
    state.miniScore += 1;
    button.classList.add('good');
  } else {
    button.classList.add('bad');
  }
  setTimeout(()=>{
    state.miniIndex += 1;
    renderMiniProblem();
  },130);
  updateMiniScore();
}

function updateMiniScore(){
  const node = document.getElementById('miniScore');
  node.textContent = '남은 시간 ' + state.miniTime + '초 | 이번 점수 ' + state.miniScore + '점 | 최고 점수 ' + state.bestMini + '점';
}

function endMiniRound(){
  if(state.miniTicker) clearInterval(state.miniTicker);
  state.miniRunning = false;
  if(state.miniScore > state.bestMini) state.bestMini = state.miniScore;
  setHud();
  updateMiniScore();
  const actionWrap = document.getElementById('miniActions');
  actionWrap.innerHTML = '';
  const retry = document.createElement('button');
  retry.type = 'button';
  retry.className = 'mini-action good';
  retry.textContent = '다시 도전';
  retry.onclick = startMiniRound;
  actionWrap.appendChild(retry);
}

function restartAll(){
  state.index = 0;
  state.cases = shuffle(BASE_CASES);
  state.selected = '';
  state.checked = false;
  state.correct = 0;
  state.attempts = 0;
  state.hints = 0;
  document.getElementById('restartBtn').style.display = 'none';
  document.getElementById('miniQuizBox').classList.remove('show');
  if(state.miniTicker) clearInterval(state.miniTicker);
  renderCase();
}

state.cases = shuffle(BASE_CASES);
renderCase();
waitForKatexAndRerender();
</script>
</body>
</html>
"""


def render():
    st.set_page_config(page_title="인수분해 패스파인더 아케이드", layout="wide")

    st.markdown(
        """
        <style>
        .main { max-width: 100%; }
        iframe { width: 100% !important; height: 2400px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(_HTML, height=1200, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
