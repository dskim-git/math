# activities/probability/mini/census_or_sample_quiz.py
"""
전수조사 vs 표본조사 판별 퀴즈
다양한 실생활 상황을 보고 어떤 조사 방법이 더 적절한지 판단하는 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "🧐 전수조사 vs 표본조사 퀴즈",
    "description": "주어진 상황에서 전수조사와 표본조사 중 어떤 방법이 더 알맞은지 판단해 보는 퀴즈 활동",
    "order": 999999,
    "hidden": True,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>전수조사 vs 표본조사 퀴즈</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 100%);
  color:#e2e8f0;padding:18px;min-height:100vh;
  font-size:17px;line-height:1.55;
}

/* ============ HEADER ============ */
.header{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:16px;flex-wrap:wrap;gap:10px;
}
.title-area{display:flex;align-items:center;gap:10px}
.title-area .ti{font-size:1.8rem}
.title-area .tt{font-size:1.15rem;font-weight:900;color:#fef3c7}

.progress-area{
  flex:1;min-width:240px;display:flex;align-items:center;gap:12px;
  background:rgba(15,23,42,.5);padding:8px 14px;border-radius:12px;
  border:1px solid rgba(99,102,241,.25);
}
.prog-text{font-size:.95rem;font-weight:800;color:#a5b4fc;white-space:nowrap}
.prog-track{
  flex:1;height:11px;background:#1e293b;border-radius:6px;overflow:hidden;
  box-shadow:inset 0 1px 2px rgba(0,0,0,.4);
}
.prog-fill{
  height:100%;background:linear-gradient(90deg,#6366f1,#22d3ee,#10b981);
  border-radius:6px;width:0%;transition:width .45s cubic-bezier(.4,0,.2,1);
}
.score-pill{
  font-size:.95rem;font-weight:900;color:#fbbf24;
  background:rgba(251,191,36,.1);border:1.5px solid rgba(251,191,36,.35);
  padding:6px 14px;border-radius:10px;white-space:nowrap;
}

/* ============ PANELS ============ */
.screen{display:none;animation:fadeIn .4s ease}
.screen.on{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

/* ============ INTRO ============ */
.intro-card{
  background:linear-gradient(135deg,rgba(79,70,229,.15),rgba(34,211,238,.1));
  border:2px solid rgba(99,102,241,.35);
  border-radius:22px;padding:30px 24px;text-align:center;
  box-shadow:0 8px 32px rgba(99,102,241,.18);
}
.intro-emoji{font-size:5rem;animation:bounce 2s ease-in-out infinite;line-height:1}
@keyframes bounce{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-12px) rotate(3deg)}}
.intro-title{font-size:1.85rem;font-weight:900;color:#fef3c7;margin:14px 0 8px}
.intro-sub{font-size:1.05rem;color:#cbd5e1;margin-bottom:22px;line-height:1.8}

.method-row{
  display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin:18px 0 22px;
}
.method{
  flex:1;min-width:240px;max-width:340px;
  background:rgba(15,23,42,.6);border-radius:16px;padding:16px 14px;
  border:2px solid;
}
.method.census{border-color:rgba(59,130,246,.5)}
.method.sample{border-color:rgba(249,115,22,.5)}
.method .mt{font-size:1.2rem;font-weight:900;margin-bottom:8px}
.method.census .mt{color:#60a5fa}
.method.sample .mt{color:#fb923c}
.method .md{font-size:.95rem;color:#cbd5e1;line-height:1.7}

.intro-tip{
  background:rgba(34,197,94,.08);border-left:4px solid #22c55e;
  border-radius:0 12px 12px 0;padding:14px 18px;text-align:left;
  font-size:.98rem;color:#86efac;line-height:1.8;margin-bottom:22px;
}
.intro-tip strong{color:#bbf7d0}

.btn-start{
  font-size:1.25rem;font-weight:900;padding:14px 38px;border:none;
  border-radius:14px;cursor:pointer;
  background:linear-gradient(135deg,#6366f1,#22d3ee);color:#fff;
  box-shadow:0 6px 24px rgba(99,102,241,.4);
  transition:all .2s;
}
.btn-start:hover{transform:translateY(-3px);box-shadow:0 9px 28px rgba(99,102,241,.55)}
.btn-start:active{transform:translateY(-1px)}

/* ============ QUIZ ============ */
.q-card{
  background:rgba(15,23,42,.7);
  border:2px solid rgba(99,102,241,.25);
  border-radius:20px;padding:24px 22px;
  box-shadow:0 6px 24px rgba(0,0,0,.3);
}

.q-icon-wrap{
  text-align:center;margin-bottom:14px;
}
.q-icon{
  font-size:4.5rem;display:inline-block;line-height:1;
  filter:drop-shadow(0 4px 10px rgba(99,102,241,.4));
  animation:popIcon .5s cubic-bezier(.34,1.56,.64,1);
}
@keyframes popIcon{0%{transform:scale(.3) rotate(-15deg);opacity:0}100%{transform:scale(1) rotate(0);opacity:1}}

.q-tag{
  display:inline-block;font-size:.9rem;font-weight:800;
  padding:5px 14px;border-radius:999px;
  background:rgba(99,102,241,.15);color:#a5b4fc;
  border:1px solid rgba(99,102,241,.3);margin-bottom:10px;
}
.q-text{
  font-size:1.35rem;font-weight:800;color:#f8fafc;
  text-align:center;line-height:1.65;margin-bottom:6px;
  padding:0 4px;
}
.q-sub{
  font-size:1rem;color:#94a3b8;text-align:center;line-height:1.7;
  margin-bottom:22px;
}

.choice-row{
  display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;
}
@media(max-width:520px){.choice-row{grid-template-columns:1fr}}
.choice{
  font-size:1.2rem;font-weight:900;padding:22px 14px;
  border:3px solid;border-radius:16px;cursor:pointer;
  transition:all .2s;background:transparent;
  display:flex;flex-direction:column;align-items:center;gap:8px;
  position:relative;overflow:hidden;
}
.choice .ce{font-size:2rem;line-height:1}
.choice .cl{font-size:1.25rem}
.choice .cd{font-size:.82rem;font-weight:600;opacity:.85}

.choice.census{border-color:#3b82f6;color:#60a5fa;background:rgba(59,130,246,.06)}
.choice.census:hover:not(:disabled){
  background:rgba(59,130,246,.18);transform:translateY(-3px);
  box-shadow:0 6px 18px rgba(59,130,246,.3);
}
.choice.sample{border-color:#f97316;color:#fb923c;background:rgba(249,115,22,.06)}
.choice.sample:hover:not(:disabled){
  background:rgba(249,115,22,.18);transform:translateY(-3px);
  box-shadow:0 6px 18px rgba(249,115,22,.3);
}
.choice:disabled{cursor:default;transform:none}
.choice.correct{
  border-color:#22c55e !important;color:#4ade80 !important;
  background:rgba(34,197,94,.18) !important;
  box-shadow:0 0 0 4px rgba(34,197,94,.12), 0 6px 18px rgba(34,197,94,.3);
  animation:correctPulse .6s ease;
}
@keyframes correctPulse{0%{transform:scale(1)}40%{transform:scale(1.05)}100%{transform:scale(1)}}
.choice.wrong{
  border-color:#ef4444 !important;color:#f87171 !important;
  background:rgba(239,68,68,.15) !important;
  animation:shake .45s ease;
}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-7px)}75%{transform:translateX(7px)}}

.choice.dimmed{opacity:.4;filter:grayscale(.5)}

/* ============ FEEDBACK ============ */
.fb{
  display:none;border-radius:14px;padding:16px 18px;margin-top:6px;
  font-size:1rem;line-height:1.75;border:2px solid;
  animation:slideUp .35s ease;
}
.fb.on{display:block}
@keyframes slideUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.fb.ok{background:rgba(34,197,94,.1);border-color:rgba(34,197,94,.4);color:#bbf7d0}
.fb.bad{background:rgba(239,68,68,.08);border-color:rgba(239,68,68,.35);color:#fecaca}
.fb-head{font-size:1.1rem;font-weight:900;margin-bottom:8px;display:flex;align-items:center;gap:8px}
.fb-ans{
  font-weight:800;color:#fef3c7;padding:6px 12px;
  background:rgba(251,191,36,.12);border-radius:8px;display:inline-block;
  margin:4px 0;
}
.fb-exp{color:#e2e8f0;font-size:1rem;line-height:1.8;margin-top:6px}

/* ============ NAV ============ */
.nav-row{
  display:flex;gap:10px;margin-top:16px;justify-content:flex-end;
}
.btn-nav{
  font-size:1.05rem;font-weight:900;padding:12px 24px;
  border:none;border-radius:12px;cursor:pointer;transition:all .2s;
}
.btn-next{
  background:linear-gradient(135deg,#6366f1,#22d3ee);color:#fff;
  box-shadow:0 4px 14px rgba(99,102,241,.35);
}
.btn-next:hover{transform:translateY(-2px);box-shadow:0 7px 20px rgba(99,102,241,.5)}
.btn-next:disabled{opacity:.4;cursor:default;transform:none;box-shadow:none}

/* ============ RESULT ============ */
.res-card{
  background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(236,72,153,.1));
  border:2px solid rgba(99,102,241,.35);
  border-radius:22px;padding:28px 22px;text-align:center;
}
.res-emoji{font-size:5rem;line-height:1;animation:bounce 2s ease-in-out infinite}
.res-title{font-size:1.7rem;font-weight:900;color:#fef3c7;margin:12px 0 6px}
.res-score{
  font-size:3rem;font-weight:900;color:#fbbf24;
  font-family:'Courier New',monospace;margin:8px 0;
}
.res-rate{font-size:1.1rem;color:#cbd5e1;margin-bottom:12px}
.stars{font-size:1.8rem;letter-spacing:6px;margin:6px 0 16px}

.res-summary{
  display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin:14px 0 20px;
}
.summ-item{
  background:rgba(15,23,42,.6);border:1.5px solid;border-radius:14px;
  padding:12px 20px;min-width:120px;
}
.summ-item .sv{font-size:1.8rem;font-weight:900;line-height:1.1;font-family:'Courier New',monospace}
.summ-item .sl{font-size:.85rem;font-weight:700;margin-top:4px}
.summ-item.ok{border-color:rgba(34,197,94,.4)}
.summ-item.ok .sv{color:#4ade80}.summ-item.ok .sl{color:#86efac}
.summ-item.bad{border-color:rgba(239,68,68,.35)}
.summ-item.bad .sv{color:#f87171}.summ-item.bad .sl{color:#fca5a5}

.btn-retry{
  font-size:1.15rem;font-weight:900;padding:13px 34px;border:none;
  border-radius:14px;cursor:pointer;
  background:linear-gradient(135deg,#f97316,#fbbf24);color:#1e293b;
  box-shadow:0 5px 18px rgba(249,115,22,.4);transition:all .2s;
  margin-right:8px;
}
.btn-retry:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(249,115,22,.55)}
.btn-review{
  font-size:1.1rem;font-weight:900;padding:13px 26px;border:none;
  border-radius:14px;cursor:pointer;
  background:rgba(99,102,241,.2);color:#a5b4fc;
  border:2px solid rgba(99,102,241,.4);transition:all .2s;
}
.btn-review:hover{background:rgba(99,102,241,.32);transform:translateY(-2px)}

/* ============ REVIEW ============ */
.review-list{margin-top:20px;text-align:left;display:none}
.review-list.on{display:block}
.rv-title{font-size:1.15rem;font-weight:900;color:#fef3c7;margin-bottom:12px;text-align:center}
.rv-item{
  background:rgba(15,23,42,.7);border-radius:14px;padding:14px 16px;
  margin-bottom:10px;border-left:5px solid;font-size:.97rem;line-height:1.7;
}
.rv-item.ok{border-left-color:#22c55e}
.rv-item.bad{border-left-color:#ef4444}
.rv-head{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.rv-num{
  background:rgba(99,102,241,.18);color:#a5b4fc;font-weight:900;
  padding:3px 10px;border-radius:8px;font-size:.85rem;
}
.rv-ic{font-size:1.7rem;line-height:1}
.rv-q{font-size:1rem;font-weight:700;color:#e2e8f0;flex:1}
.rv-tag{
  font-size:.8rem;font-weight:800;padding:3px 9px;border-radius:6px;
  white-space:nowrap;
}
.rv-tag.ok{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.35)}
.rv-tag.bad{background:rgba(239,68,68,.12);color:#f87171;border:1px solid rgba(239,68,68,.3)}
.rv-exp{color:#94a3b8;font-size:.92rem;margin-top:4px;padding-left:6px;border-left:2px solid #334155}
.rv-exp strong{color:#fbbf24}

/* ============ CONFETTI ============ */
.confetti{
  position:fixed;width:10px;height:10px;pointer-events:none;
  z-index:9999;border-radius:2px;
  animation:fall 1.4s cubic-bezier(.25,.46,.45,.94) forwards;
}
@keyframes fall{
  0%{opacity:1;transform:translateY(-20px) rotate(0deg)}
  100%{opacity:0;transform:translate(var(--tx),100vh) rotate(720deg)}
}
</style>
</head>
<body>

<!-- ============ HEADER ============ -->
<div class="header" id="header" style="display:none">
  <div class="title-area">
    <span class="ti">🧐</span>
    <span class="tt">전수조사 vs 표본조사</span>
  </div>
  <div class="progress-area">
    <span class="prog-text" id="prog-text">1 / 24</span>
    <div class="prog-track"><div class="prog-fill" id="prog-fill"></div></div>
  </div>
  <div class="score-pill" id="score-pill">⭐ 0점</div>
</div>

<!-- ============ INTRO ============ -->
<div class="screen on" id="screen-intro">
  <div class="intro-card">
    <div class="intro-emoji">🔍</div>
    <div class="intro-title">전수조사 vs 표본조사</div>
    <div class="intro-sub">
      주어진 상황에서 <strong style="color:#fef3c7">어떤 조사 방법이 더 적절한지</strong> 골라 보세요!<br>
      총 <strong style="color:#fbbf24">24개</strong>의 다양한 상황이 준비되어 있어요.
    </div>

    <div class="method-row">
      <div class="method census">
        <div class="mt">🏫 전수조사</div>
        <div class="md">모집단 <strong>전체</strong>를 조사하는 방법</div>
      </div>
      <div class="method sample">
        <div class="mt">📊 표본조사</div>
        <div class="md">모집단의 <strong>일부분</strong>(표본)만 조사하는 방법</div>
      </div>
    </div>

    <div class="intro-tip">
      💡 <strong>표본조사가 어울리는 상황</strong><br>
      ① 모집단이 너무 커서 다 조사하기 곤란할 때<br>
      ② 조사 비용·시간이 너무 많이 들 때<br>
      ③ 한 번 조사하면 그것이 <strong>파괴</strong>되는 경우(파괴조사)
    </div>

    <button class="btn-start" onclick="startQuiz()">🚀 퀴즈 시작하기</button>
  </div>
</div>

<!-- ============ QUIZ ============ -->
<div class="screen" id="screen-quiz">
  <div class="q-card">
    <div class="q-icon-wrap"><span class="q-icon" id="q-icon">📋</span></div>
    <div style="text-align:center"><span class="q-tag" id="q-tag">상황</span></div>
    <div class="q-text" id="q-text"></div>
    <div class="q-sub" id="q-sub"></div>

    <div class="choice-row">
      <button class="choice census" id="ch-census" onclick="answer('census')">
        <span class="ce">🏫</span>
        <span class="cl">전수조사</span>
        <span class="cd">모집단 전체를 조사</span>
      </button>
      <button class="choice sample" id="ch-sample" onclick="answer('sample')">
        <span class="ce">📊</span>
        <span class="cl">표본조사</span>
        <span class="cd">표본을 뽑아 조사</span>
      </button>
    </div>

    <div class="fb" id="fb">
      <div class="fb-head" id="fb-head"></div>
      <div>알맞은 조사 방법: <span class="fb-ans" id="fb-ans"></span></div>
      <div class="fb-exp" id="fb-exp"></div>
    </div>

    <div class="nav-row">
      <button class="btn-nav btn-next" id="btn-next" onclick="nextQuestion()" disabled>다음 문제 ▶</button>
    </div>
  </div>
</div>

<!-- ============ RESULT ============ -->
<div class="screen" id="screen-result">
  <div class="res-card">
    <div class="res-emoji" id="res-emoji">🎉</div>
    <div class="res-title" id="res-title">퀴즈 완료!</div>
    <div class="res-score" id="res-score">0 / 24</div>
    <div class="res-rate" id="res-rate"></div>
    <div class="stars" id="res-stars">⭐⭐⭐⭐⭐</div>

    <div class="res-summary">
      <div class="summ-item ok">
        <div class="sv" id="cnt-ok">0</div>
        <div class="sl">정답</div>
      </div>
      <div class="summ-item bad">
        <div class="sv" id="cnt-bad">0</div>
        <div class="sl">오답</div>
      </div>
    </div>

    <button class="btn-review" onclick="toggleReview()">📖 문제별 해설 보기</button>
    <button class="btn-retry" onclick="restartQuiz()">🔄 다시 도전</button>

    <div class="review-list" id="review-list">
      <div class="rv-title">📝 문제별 풀이</div>
      <div id="review-body"></div>
    </div>
  </div>
</div>

<script>
/* ════════════════ QUESTION BANK ════════════════ */
/* 정답이 골고루 섞이도록 의도적으로 순서를 배치했어요 */
const QUESTIONS = [
  { icon:"🏫", q:"우리 반 학생 28명의 평균 신장 조사",
    sub:"학급 전체를 대상으로 한 키 조사", ans:"census",
    exp:"모집단(학급 28명)이 매우 작아 <strong>전체를 조사</strong>해도 큰 부담이 없어요. 작은 모집단은 전수조사로 정확한 자료를 얻을 수 있어요." },
  { icon:"💡", q:"어느 형광등 공장에서 생산된 형광등의 평균 수명",
    sub:"수명을 측정하려면 끝까지 켜야 함", ans:"sample",
    exp:"수명을 끝까지 측정하면 형광등이 <strong>다 타버려 못 쓰게 돼요</strong>(파괴조사). 일부만 뽑아 조사하는 표본조사가 적절해요." },
  { icon:"🗳️", q:"대통령 국정 지지율 여론조사",
    sub:"국민의 정치적 의견 파악", ans:"sample",
    exp:"우리나라 성인 약 <strong>4천만 명을 모두 조사</strong>하는 것은 비용과 시간이 너무 많이 들어요. 표본조사로 비교적 빠르고 저렴하게 파악해요." },
  { icon:"🩺", q:"우리 학교 전체 학생의 매년 시력 검사",
    sub:"보건교사가 학생 한 명 한 명을 검진", ans:"census",
    exp:"학생 개개인의 건강 상태를 정확히 파악해야 하므로 <strong>모든 학생을 검사</strong>해요. 학교 보건 시스템에서 매년 시행하는 대표적인 전수조사예요." },
  { icon:"🚗", q:"새로 출시된 자동차의 충돌 안전성 검사",
    sub:"차량을 벽에 부딪쳐 안전성 평가", ans:"sample",
    exp:"한 번 충돌 시험을 하면 차가 <strong>완전히 파손</strong>돼요. 전수조사를 하면 팔 차가 남지 않으므로 표본조사가 필수예요." },
  { icon:"🏠", q:"5년마다 시행되는 인구주택총조사",
    sub:"전 국민과 모든 주택의 현황 파악", ans:"census",
    exp:"국가 정책 수립의 기초가 되는 자료이므로 <strong>모든 국민·주택</strong>을 대상으로 해요. 통계청이 5년마다 시행하는 대표적인 전수조사예요." },
  { icon:"🥫", q:"통조림 공장의 식품 위생 검사",
    sub:"통조림을 개봉하여 내용물 검사", ans:"sample",
    exp:"통조림을 열어 검사하면 <strong>상품 가치를 잃게 돼요</strong>(파괴조사). 표본을 뽑아 검사하는 품질관리 방식을 사용해요." },
  { icon:"📺", q:"TV 프로그램의 시청률 조사",
    sub:"가구별 시청 채널과 시간 파악", ans:"sample",
    exp:"전국 가구 전부를 조사하는 것은 <strong>현실적으로 불가능</strong>하고 비용이 매우 커요. 일부 표본 가구에 측정기를 설치해 추정해요." },
  { icon:"🗳️", q:"우리나라 국회의원 300명의 출신 학교 분포",
    sub:"국회의원 한 명씩 모두 조사", ans:"census",
    exp:"국회의원은 단 <strong>300명</strong>으로 모집단이 작고 명단이 공개되어 있어, 전수조사를 통해 정확한 자료를 얻는 것이 적절해요." },
  { icon:"🔋", q:"휴대폰 배터리의 충·방전 수명 검사",
    sub:"수백 회 반복 충전하여 성능 측정", ans:"sample",
    exp:"수명 테스트에는 <strong>오랜 시간과 파괴적 시험</strong>이 필요해요. 시간과 비용을 절약하려면 표본조사가 적절해요." },
  { icon:"🎵", q:"동아리 부원 12명이 가장 좋아하는 음악 장르",
    sub:"우리 동아리 전체 선호도 조사", ans:"census",
    exp:"단 <strong>12명</strong>인 작은 모집단이라 모두에게 물어보는 것이 가장 빠르고 정확해요." },
  { icon:"💧", q:"한강의 물 오염도(BOD) 측정",
    sub:"강물의 생물학적 산소 요구량 검사", ans:"sample",
    exp:"한강의 모든 물을 검사할 수 없고, 물은 <strong>시간·공간에 따라 끊임없이 변해요</strong>. 여러 지점·시간대의 표본을 뽑아 측정해요." },
  { icon:"⚾", q:"야구공의 반발력 검사",
    sub:"공을 강한 압력으로 측정하여 평가", ans:"sample",
    exp:"반발력 시험 후에는 공이 <strong>변형되거나 손상</strong>되어 경기에 쓸 수 없어요. 표본을 뽑아 품질을 확인해요." },
  { icon:"📚", q:"우리 학교 도서관의 책 권수 조사",
    sub:"보유한 모든 책의 개수 파악", ans:"census",
    exp:"도서관의 모든 책은 <strong>대출 시스템에 등록</strong>되어 있어 전수조사가 가능하고, 정확한 권수를 알아야 하므로 표본은 부적절해요." },
  { icon:"🇰🇷", q:"우리나라 만 20세 성인 남성의 평균 키",
    sub:"성인 남성 약 30만 명의 신장 분석", ans:"sample",
    exp:"성인 남성 전체를 측정하는 것은 <strong>비용·시간이 너무 큼</strong>. 무작위로 뽑은 표본의 평균을 통해 모평균을 추정해요." },
  { icon:"🍜", q:"라면 공장에서 생산되는 라면의 평균 중량",
    sub:"포장된 라면의 정량 충족 여부", ans:"sample",
    exp:"라면은 <strong>계속해서 대량 생산</strong>되고, 검사하면 포장을 뜯어야 해요. 일부 표본을 뽑아 평균 중량을 추정해요." },
  { icon:"🎓", q:"OO고등학교 졸업생 전원의 진학·취업 현황",
    sub:"한 학년 약 300명의 진로 파악", ans:"census",
    exp:"학교 차원에서 졸업생 한 명 한 명의 진로를 확인할 수 있고, 모집단이 작아 <strong>전수조사로 완전한 자료</strong>를 만들 수 있어요." },
  { icon:"🩸", q:"헌혈된 혈액 전체의 안전성·이상 유무 검사",
    sub:"질병 검사로 혈액을 일부 소모", ans:"sample",
    exp:"헌혈 안전 검사는 모든 혈액을 다 쓰면 <strong>수혈할 혈액이 남지 않아요</strong>. 표본조사로 품질 관리를 해요. (※ 실제로는 모든 혈액에 기초 검사를 하지만 정밀 항목은 표본 검사함)" },
  { icon:"🛒", q:"어느 편의점의 어제 하루 매출 총액",
    sub:"하루 동안 판매된 상품 금액의 합", ans:"census",
    exp:"<strong>POS 시스템에 모든 거래</strong>가 기록되므로 영수증 전체를 합산하면 정확한 매출을 알 수 있어요." },
  { icon:"🐟", q:"어느 큰 호수에 사는 물고기의 총 마릿수",
    sub:"호수 전체 어류 자원 추정", ans:"sample",
    exp:"호수의 물고기는 <strong>다 잡아낼 수 없고 헤아리기 곤란</strong>해요. '포획-재포획법' 같은 표본조사 기법으로 추정해요." },
  { icon:"🎆", q:"폭죽 공장의 폭죽 불량률 검사",
    sub:"불을 붙여 정상 작동 여부 확인", ans:"sample",
    exp:"폭죽을 점화하면 <strong>한 번에 다 타버려요</strong>(파괴조사). 표본을 뽑아 불량률을 추정하는 것이 적절해요." },
  { icon:"🏆", q:"이번 올림픽 한국 금메달리스트들의 평균 나이",
    sub:"우리나라 금메달 수상자 전원 조사", ans:"census",
    exp:"금메달리스트는 <strong>명단이 공식적으로 확정</strong>되어 있고 인원도 많지 않아 전수조사로 정확한 평균을 구할 수 있어요." },
  { icon:"🔩", q:"공장에서 생산된 나사 10만 개의 불량률",
    sub:"하루 생산량 중 불량품 비율 조사", ans:"sample",
    exp:"전수 검사하면 시간·비용이 너무 크고, 검사 과정에서 나사가 손상될 수도 있어요. 일부 표본을 뽑아 <strong>불량률을 추정</strong>해요." },
  { icon:"🧑‍🏫", q:"어느 회사 임직원 45명의 평균 연봉",
    sub:"인사팀이 보유한 급여 자료 활용", ans:"census",
    exp:"회사에 <strong>모든 직원의 급여 자료</strong>가 이미 있으므로, 표본을 뽑을 필요 없이 전수조사가 가능하고 더 정확해요." },
];

/* ════════════════ STATE ════════════════ */
let currentQ = 0;
let score = 0;
let answers = [];  // {q,picked,correct}

const TOTAL = QUESTIONS.length;

/* ════════════════ HELPERS ════════════════ */
function $(id){return document.getElementById(id)}

function showScreen(name){
  ['intro','quiz','result'].forEach(s=>{
    $('screen-'+s).classList.toggle('on', s===name);
  });
}

function updateHeader(){
  $('prog-text').textContent = `${Math.min(currentQ+1, TOTAL)} / ${TOTAL}`;
  $('prog-fill').style.width = `${(currentQ/TOTAL)*100}%`;
  $('score-pill').textContent = `⭐ ${score}점`;
}

/* ════════════════ INTRO ════════════════ */
function startQuiz(){
  currentQ = 0; score = 0; answers = [];
  $('header').style.display = 'flex';
  showScreen('quiz');
  renderQuestion();
}

/* ════════════════ QUESTION ════════════════ */
function renderQuestion(){
  const q = QUESTIONS[currentQ];
  $('q-icon').textContent = q.icon;
  $('q-text').textContent = q.q;
  $('q-sub').textContent = q.sub;
  $('q-tag').textContent = `상황 ${currentQ+1}`;

  $('ch-census').className = 'choice census';
  $('ch-sample').className = 'choice sample';
  $('ch-census').disabled = false;
  $('ch-sample').disabled = false;
  $('fb').className = 'fb';
  $('btn-next').disabled = true;
  $('btn-next').textContent = (currentQ === TOTAL-1) ? '결과 보기 🏆' : '다음 문제 ▶';

  // restart icon animation
  const icon = $('q-icon');
  icon.style.animation = 'none';
  void icon.offsetWidth;
  icon.style.animation = 'popIcon .5s cubic-bezier(.34,1.56,.64,1)';

  updateHeader();
}

function answer(picked){
  const q = QUESTIONS[currentQ];
  const correct = (picked === q.ans);
  const chPicked = $('ch-' + picked);
  const chOther  = $('ch-' + (picked === 'census' ? 'sample' : 'census'));
  const chAns    = $('ch-' + q.ans);

  $('ch-census').disabled = true;
  $('ch-sample').disabled = true;

  if(correct){
    chPicked.classList.add('correct');
    chOther.classList.add('dimmed');
    score += 1;
    confettiBurst();
  } else {
    chPicked.classList.add('wrong');
    chAns.classList.add('correct');
  }

  // feedback panel
  const fb = $('fb');
  fb.classList.remove('ok','bad');
  fb.classList.add('on', correct?'ok':'bad');
  $('fb-head').innerHTML = correct
    ? '✅ <span>정답이에요!</span>'
    : '❌ <span>아쉬워요, 다시 확인해 봐요.</span>';
  $('fb-ans').textContent = q.ans === 'census' ? '🏫 전수조사' : '📊 표본조사';
  $('fb-exp').innerHTML = q.exp;

  answers.push({ idx: currentQ, picked, correct });
  $('btn-next').disabled = false;
  updateHeader();
}

function nextQuestion(){
  if(currentQ === TOTAL-1){
    showResult();
  } else {
    currentQ += 1;
    renderQuestion();
  }
}

/* ════════════════ RESULT ════════════════ */
function showResult(){
  $('header').style.display = 'none';
  showScreen('result');

  const ok = score;
  const bad = TOTAL - score;
  const rate = score / TOTAL;

  $('res-score').textContent = `${ok} / ${TOTAL}`;
  $('cnt-ok').textContent = ok;
  $('cnt-bad').textContent = bad;
  $('res-rate').textContent = `정답률 ${Math.round(rate*100)}%`;

  let emoji, title, stars;
  if(rate === 1){ emoji='🏆'; title='완벽해요! 만점입니다!'; stars='⭐⭐⭐⭐⭐'; }
  else if(rate >= 0.9){ emoji='🥇'; title='훌륭해요! 거의 다 맞혔어요!'; stars='⭐⭐⭐⭐⭐'; }
  else if(rate >= 0.75){ emoji='🥈'; title='잘했어요! 조금만 더!'; stars='⭐⭐⭐⭐'; }
  else if(rate >= 0.5){ emoji='🥉'; title='꽤 했어요. 해설을 보고 정리해봐요!'; stars='⭐⭐⭐'; }
  else if(rate >= 0.3){ emoji='💪'; title='다시 한 번 도전해봐요!'; stars='⭐⭐'; }
  else { emoji='📖'; title='개념을 다시 살펴봐요!'; stars='⭐'; }

  $('res-emoji').textContent = emoji;
  $('res-title').textContent = title;
  $('res-stars').textContent = stars;

  // build review
  buildReview();
  if(rate === 1) setTimeout(bigConfetti, 200);
}

function buildReview(){
  const body = $('review-body');
  body.innerHTML = answers.map((a, i) => {
    const q = QUESTIONS[a.idx];
    const ansLabel = q.ans === 'census' ? '🏫 전수조사' : '📊 표본조사';
    const pickedLabel = a.picked === 'census' ? '🏫 전수조사' : '📊 표본조사';
    return `
      <div class="rv-item ${a.correct?'ok':'bad'}">
        <div class="rv-head">
          <span class="rv-num">Q${i+1}</span>
          <span class="rv-ic">${q.icon}</span>
          <span class="rv-q">${q.q}</span>
          <span class="rv-tag ${a.correct?'ok':'bad'}">${a.correct?'정답':'오답'}</span>
        </div>
        <div style="margin:4px 0;font-size:.9rem;color:#cbd5e1">
          내 답: <strong>${pickedLabel}</strong> &nbsp;|&nbsp;
          정답: <strong style="color:#fbbf24">${ansLabel}</strong>
        </div>
        <div class="rv-exp">${q.exp}</div>
      </div>
    `;
  }).join('');
}

function toggleReview(){
  $('review-list').classList.toggle('on');
}

function restartQuiz(){
  $('review-list').classList.remove('on');
  startQuiz();
}

/* ════════════════ CONFETTI ════════════════ */
function confettiBurst(){
  const colors = ['#fbbf24','#22c55e','#22d3ee','#a78bfa','#f87171','#fb923c'];
  const cx = window.innerWidth/2;
  const cy = window.innerHeight/3;
  for(let i=0;i<18;i++){
    const c = document.createElement('div');
    c.className = 'confetti';
    const a = Math.random() * Math.PI * 2;
    const d = 80 + Math.random() * 160;
    c.style.cssText = `left:${cx}px;top:${cy}px;background:${colors[i%6]};`+
      `width:${7+Math.random()*6}px;height:${7+Math.random()*6}px;`+
      `--tx:${Math.cos(a)*d}px;--ty:${Math.sin(a)*d}px;`+
      `animation-delay:${Math.random()*.12}s;`;
    document.body.appendChild(c);
    setTimeout(()=>c.remove(), 1500);
  }
}

function bigConfetti(){
  const colors = ['#fbbf24','#22c55e','#22d3ee','#a78bfa','#f87171','#fb923c','#ec4899','#10b981'];
  for(let i=0;i<60;i++){
    const c = document.createElement('div');
    c.className = 'confetti';
    const startX = Math.random() * window.innerWidth;
    const tx = (Math.random()-0.5) * 300;
    c.style.cssText = `left:${startX}px;top:-20px;background:${colors[i%colors.length]};`+
      `width:${8+Math.random()*8}px;height:${8+Math.random()*8}px;`+
      `--tx:${tx}px;--ty:${window.innerHeight}px;`+
      `animation-duration:${1.5+Math.random()*1.2}s;`+
      `animation-delay:${Math.random()*.6}s;`;
    document.body.appendChild(c);
    setTimeout(()=>c.remove(), 3000);
  }
}
</script>
</body>
</html>"""


def render():
    st.markdown("### 🧐 전수조사 vs 표본조사 퀴즈")
    st.caption("다양한 상황을 보고 어떤 조사 방법이 더 적절한지 골라봐요. 모든 문제에는 해설이 함께 제공돼요!")
    components.html(_HTML, height=1100, scrolling=True)
