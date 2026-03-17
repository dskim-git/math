"""
인수 후보 레이더
인수정리를 적용하기 전에 가능한 x의 후보를 찾는 훈련 활동
"""
import streamlit as st
import streamlit.components.v1 as components

from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "인수후보레이더"

_QUESTIONS = [
  {"type": "markdown", "text": "**📝 이 활동에서 연습한 내용을 바탕으로 직접 후보 찾기 문제를 만들어 보세요**"},
    {
        "key": "문제1",
    "label": "문제 1 : 계수가 정수인 다항식 하나를 만들고, 최고차항의 계수와 상수항의 약수를 각각 써 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "답1",
    "label": "문제 1의 답 : 인수정리에 사용할 x의 후보를 모두 써 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "문제2",
    "label": "문제 2 : 후보 중 하나를 골라 왜 먼저 대입해 보고 싶은지 설명해 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "답2",
    "label": "문제 2의 답 : 그 후보를 골라 인수정리를 어떻게 적용할지 간단히 써 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점", "label": "💬 느낀 점", "type": "text_area", "height": 90},
]

META = {
    "title": "🎯 인수 후보 레이더",
    "description": "상수항과 최고차항의 약수를 이용해 인수정리에 넣어 볼 x의 후보를 빠르게 골라내는 게임형 활동입니다.",
    "order": 108,
}

_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>인수 후보 레이더</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Trebuchet MS','Segoe UI',sans-serif;
  background:
    radial-gradient(circle at top left,rgba(34,197,94,.22),transparent 24%),
    radial-gradient(circle at top right,rgba(14,165,233,.18),transparent 28%),
    linear-gradient(160deg,#08121c 0%,#0b1b2b 45%,#111827 100%);
  color:#e5f0ff;
  min-height:100vh;
  padding:14px 10px 24px;
}
.shell{max-width:1120px;margin:0 auto}
.hero{
  position:relative;
  overflow:hidden;
  border:1px solid rgba(125,211,252,.16);
  background:linear-gradient(135deg,rgba(12,24,37,.9),rgba(16,34,51,.82));
  border-radius:24px;
  padding:20px 20px 18px;
  box-shadow:0 24px 70px rgba(0,0,0,.32);
  margin-bottom:16px;
}
.hero:before,.hero:after{
  content:'';
  position:absolute;
  border-radius:50%;
  pointer-events:none;
}
.hero:before{
  width:280px;height:280px;right:-80px;top:-120px;
  background:radial-gradient(circle,rgba(16,185,129,.18),transparent 70%);
}
.hero:after{
  width:220px;height:220px;left:-50px;bottom:-120px;
  background:radial-gradient(circle,rgba(56,189,248,.15),transparent 72%);
}
.eyebrow{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;background:rgba(14,165,233,.12);border:1px solid rgba(125,211,252,.2);color:#8ce7ff;font-size:.77rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px}
.hero h1{font-size:1.9rem;line-height:1.2;color:#f8fbff;margin-bottom:8px}
.hero p{max-width:780px;line-height:1.7;color:#b7cae4;font-size:.96rem}

.topbar{display:grid;grid-template-columns:1.2fr .8fr;gap:14px;margin-bottom:14px}
.panel{
  background:rgba(7,15,24,.72);
  border:1px solid rgba(148,163,184,.16);
  border-radius:20px;
  padding:16px;
  backdrop-filter:blur(10px);
}
.panel-title{display:flex;align-items:center;gap:8px;font-size:.92rem;font-weight:800;color:#8ce7ff;margin-bottom:10px}
.theorem{line-height:1.85;color:#d9e7f7;font-size:.93rem}
.theorem strong{color:#f8fafc}
.chips-inline{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.mini-chip{padding:6px 10px;border-radius:999px;background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.26);color:#c7f9d4;font-size:.8rem;font-weight:700}

.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.hud-card{padding:14px;border-radius:18px;background:linear-gradient(180deg,rgba(15,23,42,.82),rgba(10,15,25,.82));border:1px solid rgba(125,211,252,.14)}
.hud-label{font-size:.75rem;color:#86a5c8;margin-bottom:6px}
.hud-value{font-size:1.3rem;font-weight:900;color:#f8fbff}
.hud-sub{font-size:.8rem;color:#9fb8d4;margin-top:4px}

.arena{position:relative;border-radius:24px;background:linear-gradient(180deg,rgba(8,18,30,.94),rgba(8,16,28,.88));border:1px solid rgba(125,211,252,.16);padding:18px;overflow:hidden}
.arena:before{
  content:'';
  position:absolute;inset:0;
  background:
    radial-gradient(circle at center,rgba(16,185,129,.1),transparent 0 20%,rgba(255,255,255,0) 20%),
    repeating-radial-gradient(circle at center,rgba(56,189,248,.06) 0 2px,transparent 2px 58px),
    linear-gradient(rgba(125,211,252,.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(125,211,252,.05) 1px,transparent 1px);
  background-size:auto,auto,48px 48px,48px 48px;
  opacity:.55;
  pointer-events:none;
}
.arena > *{position:relative;z-index:1}

.mission-row{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap;margin-bottom:14px}
.mission-copy{max-width:720px}
.mission-tag{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.26);color:#fde68a;font-size:.77rem;font-weight:800;margin-bottom:10px}
.mission-title{font-size:1.28rem;font-weight:900;color:#f8fbff;margin-bottom:8px}
.mission-note{font-size:.92rem;color:#aac2dd;line-height:1.7}
.poly-box{
  min-width:260px;
  padding:14px 16px;
  border-radius:18px;
  background:rgba(15,23,42,.72);
  border:1px solid rgba(125,211,252,.16);
  text-align:center;
}
.poly-label{font-size:.73rem;color:#86a5c8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px}
.poly-math{font-size:1.2rem;color:#f8fbff;min-height:44px;display:flex;align-items:center;justify-content:center}

.step-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px}
.step-card{
  border-radius:20px;
  background:rgba(9,15,24,.78);
  border:1px solid rgba(148,163,184,.14);
  padding:16px;
  min-height:370px;
  display:flex;
  flex-direction:column;
  gap:12px;
}
.step-head{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.step-num{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(14,165,233,.18);border:1px solid rgba(125,211,252,.26);color:#8ce7ff;font-size:.92rem;font-weight:900;flex-shrink:0}
.step-name{font-size:1rem;font-weight:800;color:#f8fbff}
.step-desc{font-size:.84rem;line-height:1.6;color:#97b1cc;margin-top:4px}
.status-pill{padding:5px 10px;border-radius:999px;font-size:.72rem;font-weight:800;white-space:nowrap}
.status-lock{background:rgba(71,85,105,.18);color:#94a3b8}
.status-live{background:rgba(14,165,233,.14);color:#8ce7ff}
.status-done{background:rgba(34,197,94,.14);color:#bbf7d0}

.choice-wrap{display:flex;flex-wrap:wrap;gap:8px}
.choice{
  padding:9px 13px;
  border-radius:14px;
  border:1px solid rgba(148,163,184,.18);
  background:rgba(15,23,42,.85);
  color:#e5f0ff;
  font-size:.9rem;
  font-weight:800;
  cursor:pointer;
  transition:transform .18s,box-shadow .18s,border-color .18s,background .18s;
  user-select:none;
}
.choice:hover{transform:translateY(-2px);border-color:rgba(125,211,252,.42);box-shadow:0 10px 22px rgba(2,8,23,.35)}
.choice.selected{background:linear-gradient(135deg,rgba(14,165,233,.26),rgba(34,197,94,.18));border-color:#67e8f9;color:#f8fbff}
.choice.locked{opacity:.45;cursor:not-allowed}

.tip-box{padding:11px 12px;border-radius:14px;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.18);font-size:.83rem;line-height:1.7;color:#f7dd8b}
.hint-box{display:none;padding:11px 12px;border-radius:14px;background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.18);font-size:.83rem;line-height:1.7;color:#cffcd8}
.hint-box.show{display:block}

.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:auto}
.btn{
  border:none;
  border-radius:999px;
  padding:9px 16px;
  font-size:.84rem;
  font-weight:900;
  cursor:pointer;
  transition:transform .18s,filter .18s;
}
.btn:hover{transform:translateY(-1px);filter:brightness(1.06)}
.btn-check{background:linear-gradient(135deg,#06b6d4,#2563eb);color:#fff}
.btn-hint{background:rgba(251,191,36,.16);color:#fde68a;border:1px solid rgba(251,191,36,.24)}
.btn-reset{background:rgba(71,85,105,.26);color:#dbe5f5}
.btn-next{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;display:none}

.feedback{min-height:24px;font-size:.86rem;font-weight:800}
.feedback.ok{color:#86efac}
.feedback.ng{color:#fca5a5}

.reveal{
  margin-top:14px;
  border-radius:20px;
  padding:16px;
  background:linear-gradient(135deg,rgba(22,163,74,.14),rgba(14,165,233,.14));
  border:1px solid rgba(74,222,128,.22);
  display:none;
}
.reveal.show{display:block;animation:popIn .35s ease}
@keyframes popIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.reveal-title{font-size:1rem;font-weight:900;color:#dcfce7;margin-bottom:8px}
.reveal-text{font-size:.92rem;line-height:1.8;color:#d9fbe4}
.root-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.root-badge{padding:7px 11px;border-radius:999px;background:rgba(240,253,244,.12);border:1px solid rgba(187,247,208,.3);color:#f0fdf4;font-size:.84rem;font-weight:800}

.summary{
  margin-top:16px;
  display:none;
  border-radius:24px;
  padding:20px;
  background:linear-gradient(135deg,rgba(34,197,94,.16),rgba(59,130,246,.14));
  border:1px solid rgba(134,239,172,.22);
}
.summary.show{display:block}
.summary h3{font-size:1.25rem;color:#f0fdf4;margin-bottom:10px}
.summary p{font-size:.94rem;line-height:1.8;color:#d8f8e2}

.pulse{animation:pulseGlow .55s ease}
@keyframes pulseGlow{
  0%{box-shadow:0 0 0 rgba(34,197,94,0)}
  50%{box-shadow:0 0 0 8px rgba(34,197,94,.12)}
  100%{box-shadow:0 0 0 rgba(34,197,94,0)}
}

@media (max-width:980px){
  .topbar{grid-template-columns:1fr}
  .hud{grid-template-columns:repeat(2,1fr)}
  .step-grid{grid-template-columns:1fr}
  .step-card{min-height:auto}
}
@media (max-width:560px){
  body{padding:10px 8px 20px}
  .hero{padding:16px}
  .hero h1{font-size:1.5rem}
  .hud{grid-template-columns:1fr 1fr}
  .panel,.arena{padding:14px}
  .mission-title{font-size:1.1rem}
}
</style>
</head>
<body>
<div class="shell">
  <section class="hero">
    <div class="eyebrow">Factor Theorem Radar</div>
    <h1>🎯 인수 후보 레이더</h1>
    <p>
      조립제법을 시작하기 전에 가장 먼저 해야 할 일은 <strong>인수정리에 넣어 볼 x의 후보</strong>를 빠르게 좁히는 것입니다.
      각 임무에서 상수항의 약수, 최고차항의 약수를 골라낸 뒤 가능한 후보를 모두 포착해 보세요.
    </p>
  </section>

  <div class="topbar">
    <section class="panel">
      <div class="panel-title">📡 레이더 원리</div>
      <div class="theorem">
        계수가 정수인 다항식 <strong>f(x)</strong>가 일차인수 <strong>ax-b</strong>를 가지면,<br>
        <strong>b</strong>는 상수항의 약수이고 <strong>a</strong>는 최고차항의 계수의 약수입니다.<br>
        따라서 인수정리에 넣어 볼 후보는 <strong>x = b/a</strong> 꼴에서 나옵니다.
      </div>
      <div class="chips-inline">
        <div class="mini-chip">1단계: 상수항 약수 찾기</div>
        <div class="mini-chip">2단계: 최고차항 약수 찾기</div>
        <div class="mini-chip">3단계: x 후보 전부 선택</div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-title">🛰️ 진행 현황</div>
      <div class="hud">
        <div class="hud-card">
          <div class="hud-label">현재 임무</div>
          <div class="hud-value" id="missionNow">1 / 6</div>
          <div class="hud-sub">순서대로 진행</div>
        </div>
        <div class="hud-card">
          <div class="hud-label">완료한 임무</div>
          <div class="hud-value" id="missionDone">0</div>
          <div class="hud-sub">총 6개</div>
        </div>
        <div class="hud-card">
          <div class="hud-label">힌트 사용</div>
          <div class="hud-value" id="hintCount">0</div>
          <div class="hud-sub">적게 쓸수록 좋음</div>
        </div>
        <div class="hud-card">
          <div class="hud-label">레이더 정확도</div>
          <div class="hud-value" id="accuracy">0%</div>
          <div class="hud-sub" id="accuracySub">아직 스캔 전</div>
        </div>
      </div>
    </section>
  </div>

  <section class="arena">
    <div class="mission-row">
      <div class="mission-copy">
        <div class="mission-tag" id="missionTag">훈련 임무 1</div>
        <div class="mission-title" id="missionTitle">후보를 모두 포착하라</div>
        <div class="mission-note" id="missionNote"></div>
      </div>
      <div class="poly-box">
        <div class="poly-label">현재 다항식</div>
        <div class="poly-math" id="polyMath"></div>
      </div>
    </div>

    <div class="step-grid">
      <section class="step-card" id="step1Card">
        <div class="step-head">
          <div>
            <div style="display:flex;align-items:center;gap:10px">
              <div class="step-num">1</div>
              <div class="step-name">상수항의 약수 찾기</div>
            </div>
            <div class="step-desc" id="constDesc"></div>
          </div>
          <div class="status-pill status-live" id="status1">진행 중</div>
        </div>
        <div class="tip-box">상수항의 절댓값을 나누어떨어지게 만드는 양의 정수들을 먼저 고르세요.</div>
        <div class="choice-wrap" id="constChoices"></div>
        <div class="hint-box" id="hint1"></div>
        <div class="feedback" id="feedback1"></div>
        <div class="btn-row">
          <button class="btn btn-check" onclick="checkDivisors('const')">약수 스캔</button>
          <button class="btn btn-hint" onclick="showHint(1)">힌트 보기</button>
          <button class="btn btn-reset" onclick="resetStep('const')">선택 초기화</button>
        </div>
      </section>

      <section class="step-card" id="step2Card">
        <div class="step-head">
          <div>
            <div style="display:flex;align-items:center;gap:10px">
              <div class="step-num">2</div>
              <div class="step-name">최고차항 약수 찾기</div>
            </div>
            <div class="step-desc" id="leadDesc"></div>
          </div>
          <div class="status-pill status-lock" id="status2">잠김</div>
        </div>
        <div class="tip-box">최고차항의 계수의 약수를 찾으면 분모 후보가 정리됩니다.</div>
        <div class="choice-wrap" id="leadChoices"></div>
        <div class="hint-box" id="hint2"></div>
        <div class="feedback" id="feedback2"></div>
        <div class="btn-row">
          <button class="btn btn-check" onclick="checkDivisors('lead')">약수 스캔</button>
          <button class="btn btn-hint" onclick="showHint(2)">힌트 보기</button>
          <button class="btn btn-reset" onclick="resetStep('lead')">선택 초기화</button>
        </div>
      </section>

      <section class="step-card" id="step3Card">
        <div class="step-head">
          <div>
            <div style="display:flex;align-items:center;gap:10px">
              <div class="step-num">3</div>
              <div class="step-name">인수정리 후보 포착</div>
            </div>
            <div class="step-desc">가능한 x 값을 모두 선택하세요. 부호 ±도 꼭 챙겨야 합니다.</div>
          </div>
          <div class="status-pill status-lock" id="status3">잠김</div>
        </div>
        <div class="tip-box">x = b/a 꼴에서 나오는 값을 기약분수로 정리해 한 번씩만 남기면 됩니다.</div>
        <div class="choice-wrap" id="candidateChoices"></div>
        <div class="hint-box" id="hint3"></div>
        <div class="feedback" id="feedback3"></div>
        <div class="btn-row">
          <button class="btn btn-check" onclick="checkCandidates()">후보 스캔 완료</button>
          <button class="btn btn-hint" onclick="showHint(3)">힌트 보기</button>
          <button class="btn btn-reset" onclick="resetStep('candidate')">선택 초기화</button>
          <button class="btn btn-next" id="nextBtn" onclick="nextProblem()">다음 임무</button>
        </div>
      </section>
    </div>

    <section class="reveal" id="revealBox">
      <div class="reveal-title">✅ 스캔 완료</div>
      <div class="reveal-text" id="revealText"></div>
      <div class="root-list" id="rootList"></div>
    </section>

    <section class="summary" id="summaryBox">
      <h3>🏁 모든 레이더 임무 완료</h3>
      <p>
        이제 다항식을 보면 바로 <strong>상수항의 약수</strong>, <strong>최고차항의 약수</strong>, <strong>x = b/a 형태의 후보</strong>를 연결해서 생각할 수 있어야 합니다.
        아래 성찰 기록에는 직접 만든 문제와 후보 찾기 과정을 적어 보세요.
      </p>
    </section>
  </section>
</div>

<script>
const PROBLEMS = [
  {
    title:'훈련 임무 1',
    subtitle:'최고차항 계수가 1인 식부터 빠르게 익혀 봅시다.',
    polyLatex:'P(x)=x^3-2x^2-5x+6',
    leading:1,
    constant:6,
    constOptions:[1,2,3,6,4,5,9],
    leadOptions:[1,2,3],
    candidateDecoys:['1/2','-1/2','4','-4'],
    actualRoots:['-2','1','3'],
    note:'최고차항 계수가 1이면 분모 후보는 1뿐이므로 정수 후보만 보면 됩니다.'
  },
  {
    title:'훈련 임무 2',
    subtitle:'분모 후보가 1과 2로 늘어나면 반정수 후보도 함께 챙겨야 합니다.',
    polyLatex:'Q(x)=2x^3-9x^2+7x+6',
    leading:2,
    constant:6,
    constOptions:[1,2,3,6,4,5,9],
    leadOptions:[1,2,4],
    candidateDecoys:['1/4','-1/4','4','-4','5/2'],
    actualRoots:['-1/2','2','3'],
    note:'상수항 약수 1, 2, 3, 6과 최고차항 약수 1, 2를 조합해 후보를 만들어야 합니다.'
  },
  {
    title:'훈련 임무 3',
    subtitle:'최고차항 계수가 3이면 1/3, 2/3 같은 후보가 새로 생깁니다.',
    polyLatex:'R(x)=3x^3+14x^2+13x-6',
    leading:3,
    constant:-6,
    constOptions:[1,2,3,6,4,5,9],
    leadOptions:[1,3,2,4],
    candidateDecoys:['1/6','-1/6','4','-4','5/3'],
    actualRoots:['-3','-2','1/3'],
    note:'상수항이 음수여도 약수는 절댓값으로 찾고, 마지막 후보 단계에서 ±를 함께 붙입니다.'
  },
  {
    title:'훈련 임무 4',
    subtitle:'최고차항 계수가 4이면 같은 값으로 약분되는 분수들을 조심해야 합니다.',
    polyLatex:'S(x)=4x^3+5x^2-7x-2',
    leading:4,
    constant:-2,
    constOptions:[1,2,4,6,8],
    leadOptions:[1,2,4,3,6],
    candidateDecoys:['3/4','-3/4','3','-3'],
    actualRoots:['-2','1','-1/4'],
    note:'2/4는 1/2와 같은 값입니다. 기약분수로 정리해 후보를 한 번만 남기세요.'
  },
  {
    title:'훈련 임무 5',
    subtitle:'여러 후보 중 실제로는 일부만 0을 만들더라도 후보 목록은 넓게 잡아야 합니다.',
    polyLatex:'T(x)=3x^3-7x^2-18x-8',
    leading:3,
    constant:-8,
    constOptions:[1,2,4,8,3,5,6],
    leadOptions:[1,3,2,4],
    candidateDecoys:['1/8','-1/8','5/3','-5/3','3'],
    actualRoots:['-2','-2/3','4'],
    note:'실제 근을 아직 모를 때는 빼지 말고, 조건에 맞는 후보를 모두 남겨 둬야 합니다.'
  },
  {
    title:'보너스 임무',
    subtitle:'이미지 예시와 같은 상황입니다. 후보를 찾았다고 해서 꼭 유리근이 있는 것은 아닙니다.',
    polyLatex:'P(x)=3x^4+3x^2+x+8',
    leading:3,
    constant:8,
    constOptions:[1,2,4,8,3,5,6],
    leadOptions:[1,3,2,4],
    candidateDecoys:['3','-3','1/8','-1/8','5/3'],
    actualRoots:[],
    note:'후보 찾기는 출발점입니다. 그다음에 실제로 대입해서 0이 되는지 확인해야 합니다.'
  }
];

const state = {
  index:0,
  solved:0,
  hints:0,
  checks:0,
  perfectChecks:0,
  step1Done:false,
  step2Done:false,
  step3Done:false,
  hintShown:{1:false,2:false,3:false},
  selectedConst:new Set(),
  selectedLead:new Set(),
  selectedCandidates:new Set()
};

function divisors(n){
  const value = Math.abs(n);
  const result = [];
  for(let i=1;i<=value;i++){
    if(value % i === 0) result.push(i);
  }
  return result;
}

function gcd(a,b){
  let x = Math.abs(a);
  let y = Math.abs(b);
  while(y){
    const temp = x % y;
    x = y;
    y = temp;
  }
  return x || 1;
}

function formatRational(num, den){
  if(den < 0){
    num *= -1;
    den *= -1;
  }
  const g = gcd(num, den);
  num /= g;
  den /= g;
  if(den === 1) return String(num);
  return num + '/' + den;
}

function rationalToNumber(text){
  if(text.includes('/')){
    const parts = text.split('/').map(Number);
    return parts[0] / parts[1];
  }
  return Number(text);
}

function sortedRationals(values){
  return [...values].sort((left,right)=>{
    const numDiff = rationalToNumber(left) - rationalToNumber(right);
    if(Math.abs(numDiff) > 1e-9) return numDiff;
    return left.length - right.length;
  });
}

function candidateSet(problem){
  const result = new Set();
  const pDivs = divisors(problem.constant);
  const qDivs = divisors(problem.leading);
  pDivs.forEach((p)=>{
    qDivs.forEach((q)=>{
      result.add(formatRational(p, q));
      result.add(formatRational(-p, q));
    });
  });
  return sortedRationals(result);
}

function candidateOptions(problem){
  const merged = new Set(candidateSet(problem));
  problem.candidateDecoys.forEach((value)=>merged.add(value));
  return sortedRationals(merged);
}

function mathHTML(latex){
  if(window.katex){
    try{
      return katex.renderToString(latex,{throwOnError:false,displayMode:false});
    }catch(error){}
  }
  return latex;
}

function waitForKatexAndRerender(){
  if(window.katex) return;
  let attempts = 0;
  const timer = setInterval(()=>{
    attempts += 1;
    if(window.katex){
      clearInterval(timer);
      renderProblem();
    }
    if(attempts >= 60) clearInterval(timer);
  },120);
}

function setChoiceGroup(targetId, options, selectedSet, group, locked){
  const container = document.getElementById(targetId);
  container.innerHTML = '';
  options.forEach((value)=>{
    const button = document.createElement('button');
    button.className = 'choice';
    button.type = 'button';
    button.textContent = group === 'candidate' ? 'x = ' + value : String(value);
    if(selectedSet.has(String(value))) button.classList.add('selected');
    if(locked) button.classList.add('locked');
    button.onclick = ()=>toggleChoice(group, String(value), locked);
    container.appendChild(button);
  });
}

function toggleChoice(group, value, locked){
  if(locked) return;
  const setRef = group === 'const' ? state.selectedConst : group === 'lead' ? state.selectedLead : state.selectedCandidates;
  if(setRef.has(value)) setRef.delete(value);
  else setRef.add(value);
  renderChoices();
}

function renderChoices(){
  const problem = PROBLEMS[state.index];
  setChoiceGroup('constChoices', problem.constOptions, state.selectedConst, 'const', false);
  setChoiceGroup('leadChoices', problem.leadOptions, state.selectedLead, 'lead', !state.step1Done);
  setChoiceGroup('candidateChoices', candidateOptions(problem), state.selectedCandidates, 'candidate', !state.step2Done || state.step3Done);
}

function updateStatuses(){
  const s1 = document.getElementById('status1');
  const s2 = document.getElementById('status2');
  const s3 = document.getElementById('status3');
  s1.className = 'status-pill ' + (state.step1Done ? 'status-done' : 'status-live');
  s1.textContent = state.step1Done ? '완료' : '진행 중';
  s2.className = 'status-pill ' + (state.step2Done ? 'status-done' : state.step1Done ? 'status-live' : 'status-lock');
  s2.textContent = state.step2Done ? '완료' : state.step1Done ? '진행 중' : '잠김';
  s3.className = 'status-pill ' + (state.step3Done ? 'status-done' : state.step2Done ? '진행 중' : '잠김');
  s3.textContent = state.step3Done ? '완료' : state.step2Done ? '진행 중' : '잠김';
}

function clearFeedback(){
  ['feedback1','feedback2','feedback3'].forEach((id)=>{
    const node = document.getElementById(id);
    node.textContent = '';
    node.className = 'feedback';
  });
}

function setFeedback(id, ok, text){
  const node = document.getElementById(id);
  node.textContent = text;
  node.className = ok ? 'feedback ok' : 'feedback ng';
}

function setHud(){
  document.getElementById('missionNow').textContent = (state.index + 1) + ' / ' + PROBLEMS.length;
  document.getElementById('missionDone').textContent = String(state.solved);
  document.getElementById('hintCount').textContent = String(state.hints);
  const accuracy = state.checks ? Math.round((state.perfectChecks / state.checks) * 100) : 0;
  document.getElementById('accuracy').textContent = accuracy + '%';
  document.getElementById('accuracySub').textContent = state.checks ? '정확한 스캔 ' + state.perfectChecks + '회' : '아직 스캔 전';
}

function renderProblem(){
  const problem = PROBLEMS[state.index];
  document.getElementById('missionTag').textContent = problem.title;
  document.getElementById('missionTitle').textContent = '가능한 x 후보를 모두 포착하라';
  document.getElementById('missionNote').textContent = problem.subtitle + ' ' + problem.note;
  document.getElementById('polyMath').innerHTML = mathHTML(problem.polyLatex);
  document.getElementById('constDesc').textContent = '|상수항| = ' + Math.abs(problem.constant) + '의 약수를 선택하세요.';
  document.getElementById('leadDesc').textContent = '최고차항의 계수 = ' + Math.abs(problem.leading) + '의 약수를 선택하세요.';
  document.getElementById('hint1').className = 'hint-box';
  document.getElementById('hint2').className = 'hint-box';
  document.getElementById('hint3').className = 'hint-box';
  document.getElementById('hint1').textContent = '상수항의 절댓값 ' + Math.abs(problem.constant) + '을 나누어떨어지게 하는 양의 정수만 고르면 됩니다.';
  document.getElementById('hint2').textContent = '최고차항의 계수 ' + Math.abs(problem.leading) + '을 나누어떨어지게 하는 양의 정수만 남기세요.';
  document.getElementById('hint3').textContent = '1단계 값들을 분자 후보 b, 2단계 값들을 분모 후보 a로 두고 x = ±b/a를 만듭니다.';
  document.getElementById('nextBtn').style.display = state.step3Done ? 'inline-flex' : 'none';
  const reveal = document.getElementById('revealBox');
  reveal.className = 'reveal';
  document.getElementById('rootList').innerHTML = '';
  document.getElementById('summaryBox').classList.remove('show');
  clearFeedback();
  updateStatuses();
  renderChoices();
  setHud();
}

function compareSet(selected, expectedValues){
  const expected = new Set(expectedValues.map(String));
  if(selected.size !== expected.size) return false;
  for(const item of selected){
    if(!expected.has(String(item))) return false;
  }
  return true;
}

function flashCard(cardId){
  const node = document.getElementById(cardId);
  node.classList.remove('pulse');
  void node.offsetWidth;
  node.classList.add('pulse');
}

function checkDivisors(type){
  const problem = PROBLEMS[state.index];
  const isConst = type === 'const';
  if(!isConst && !state.step1Done) return;
  state.checks += 1;
  const expected = isConst ? divisors(problem.constant) : divisors(problem.leading);
  const chosen = isConst ? state.selectedConst : state.selectedLead;
  const ok = compareSet(chosen, expected);
  if(ok) state.perfectChecks += 1;
  if(isConst){
    state.step1Done = ok || state.step1Done;
    setFeedback('feedback1', ok, ok ? '정확합니다. 이제 최고차항의 약수를 찾아 분모 후보를 정리하세요.' : '다시 보세요. 빠진 약수나 약수가 아닌 수가 섞여 있습니다.');
    if(ok) flashCard('step1Card');
  } else {
    state.step2Done = ok || state.step2Done;
    setFeedback('feedback2', ok, ok ? '좋습니다. 이제 x = ±b/a 꼴의 후보를 모두 포착하세요.' : '분모 후보를 다시 정리해 보세요. 최고차항의 계수의 약수만 남아야 합니다.');
    if(ok) flashCard('step2Card');
  }
  updateStatuses();
  renderChoices();
  setHud();
}

function checkCandidates(){
  if(!state.step2Done) return;
  state.checks += 1;
  const problem = PROBLEMS[state.index];
  const expected = candidateSet(problem);
  const ok = compareSet(state.selectedCandidates, expected);
  if(ok) state.perfectChecks += 1;
  state.step3Done = ok || state.step3Done;
  setFeedback('feedback3', ok, ok ? '후보 포착 완료. 이제 실제로 어떤 값을 먼저 대입할지 생각해 보세요.' : '후보가 부족하거나 함정 카드가 섞였습니다. ±와 기약분수를 다시 점검하세요.');
  if(ok){
    flashCard('step3Card');
    document.getElementById('nextBtn').style.display = 'inline-flex';
    showReveal(problem, expected);
    if(state.solved === state.index){
      state.solved += 1;
    }
  }
  updateStatuses();
  renderChoices();
  setHud();
}

function showReveal(problem, expected){
  const reveal = document.getElementById('revealBox');
  const rootList = document.getElementById('rootList');
  rootList.innerHTML = '';
  const revealText = document.getElementById('revealText');
  reveal.className = 'reveal show';
  revealText.innerHTML = '가능한 후보는 <strong>' + expected.join(', ') + '</strong> 입니다.<br>';
  if(problem.actualRoots.length){
    revealText.innerHTML += '이 식에서는 이 후보들 가운데 실제로 0을 만드는 값도 있습니다. 아래 값부터 인수정리로 점검해 볼 수 있습니다.';
    problem.actualRoots.forEach((root)=>{
      const badge = document.createElement('div');
      badge.className = 'root-badge';
      badge.textContent = 'P(' + root + ') = 0';
      rootList.appendChild(badge);
    });
  } else {
    revealText.innerHTML += '하지만 이번 식은 후보는 있어도 실제 유리근은 없습니다. 후보 찾기와 실제 근 존재는 다른 단계라는 점을 기억하세요.';
    const badge = document.createElement('div');
    badge.className = 'root-badge';
    badge.textContent = '유리근 없음';
    rootList.appendChild(badge);
  }
}

function showHint(step){
  if(!state.hintShown[step]){
    state.hints += 1;
    state.hintShown[step] = true;
    setHud();
  }
  const node = document.getElementById('hint' + step);
  node.classList.add('show');
}

function resetStep(type){
  if(type === 'const') state.selectedConst = new Set();
  if(type === 'lead') state.selectedLead = new Set();
  if(type === 'candidate') state.selectedCandidates = new Set();
  renderChoices();
}

function resetProblemState(){
  state.step1Done = false;
  state.step2Done = false;
  state.step3Done = false;
  state.hintShown = {1:false,2:false,3:false};
  state.selectedConst = new Set();
  state.selectedLead = new Set();
  state.selectedCandidates = new Set();
}

function nextProblem(){
  if(!state.step3Done) return;
  if(state.index < PROBLEMS.length - 1){
    state.index += 1;
    resetProblemState();
    renderProblem();
  } else {
    document.getElementById('summaryBox').classList.add('show');
    document.getElementById('nextBtn').style.display = 'none';
  }
}

resetProblemState();
renderProblem();
waitForKatexAndRerender();
</script>
</body>
</html>
"""


def render():
    st.set_page_config(page_title="인수 후보 레이더", layout="wide")

    st.markdown(
        """
        <style>
        .main { max-width: 100%; }
        iframe { width: 100% !important; height: 2300px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(_HTML, height=2300, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()