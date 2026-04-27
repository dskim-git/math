# activities/common/mini/addition_multiplication_rule.py
"""
합의 법칙 vs 곱의 법칙 판별 챌린지
실생활 12가지 사례를 보고 합의/곱의 법칙을 판별하는 게임형 미니활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "합곱법칙판별챌린지"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "구별기준",
        "label":  "① 합의 법칙과 곱의 법칙을 구별하는 나만의 기준을 만들어 보세요. 어떤 상황에서 합의 법칙을, 어떤 상황에서 곱의 법칙을 사용해야 할까요?",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "어려운사례",
        "label":  "② 활동 중 가장 헷갈렸던 사례는 무엇이었나요? 왜 헷갈렸는지 설명하고, 올바른 풀이 방법을 적어보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "실생활연결",
        "label":  "③ 활동에서 제시된 것 외에, 합의 법칙이나 곱의 법칙이 사용되는 실생활 사례를 1가지씩 직접 만들어 보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "핵심단어",
        "label":  "④ 문제에서 합의 법칙임을 나타내는 핵심 단어와 곱의 법칙임을 나타내는 핵심 단어는 각각 무엇이었나요?",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "새롭게알게된점",
        "label":  "💡 이 활동을 통해 새롭게 알게 된 점",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "느낀점",
        "label":  "💬 이 활동을 하면서 느낀 점",
        "type":   "text_area",
        "height": 90,
    },
]

META = {
    "title":       "🎮 합·곱 법칙 판별 챌린지",
    "description": "실생활 12가지 사례를 보고 합의 법칙과 곱의 법칙 중 어느 것을 써야 할지 판별하는 게임형 탐구 활동입니다.",
    "order":       311,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>합·곱 법칙 판별 챌린지</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(145deg,#080d1c 0%,#0c1428 55%,#06091a 100%);
  color:#e2e8ff;
  padding:12px 14px 20px;
}

/* ── 헤더 ── */
.hdr{text-align:center;margin-bottom:14px}
.hdr h1{font-size:1.35rem;color:#ffd700;text-shadow:0 0 20px rgba(255,215,0,.4);margin-bottom:3px}
.hdr p{font-size:.8rem;color:#7788aa}

/* ── 진행 바 ── */
.prog-wrap{margin-bottom:12px}
.prog-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}
.prog-lbl{font-size:.78rem;color:#7788aa}
.score-badge{background:linear-gradient(135deg,#ffd700,#ff9944);color:#1a0a00;
  padding:3px 12px;border-radius:99px;font-size:.8rem;font-weight:700}
.prog-track{width:100%;height:7px;background:rgba(255,255,255,.07);border-radius:99px;overflow:hidden}
.prog-fill{height:100%;background:linear-gradient(90deg,#7c3aed,#2563eb);
  border-radius:99px;transition:width .4s ease}

/* ── 인트로 화면 ── */
#intro{}
.intro-h{font-size:1rem;color:#e2e8ff;text-align:center;margin-bottom:4px}
.intro-sub{font-size:.78rem;color:#7788aa;text-align:center;margin-bottom:16px}
.rule-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px}
.rule-card{border-radius:12px;padding:13px 11px}
.rc-sum{background:linear-gradient(145deg,#1e0d30,#140920);border:2px solid #7c3aed}
.rc-mul{background:linear-gradient(145deg,#07192e,#050f1c);border:2px solid #0891b2}
.rc-icon{font-size:1.8rem;margin-bottom:5px}
.rc-name{font-size:.95rem;font-weight:700;margin-bottom:5px}
.rc-sum .rc-name{color:#c084fc}
.rc-mul .rc-name{color:#22d3ee}
.rc-desc{font-size:.75rem;color:#aabbcc;line-height:1.55;margin-bottom:7px}
.rc-formula{font-family:'Courier New',monospace;font-size:.88rem;font-weight:700;
  padding:5px 9px;border-radius:7px}
.rc-sum .rc-formula{background:rgba(124,58,237,.15);color:#e879f9;border:1px solid rgba(124,58,237,.35)}
.rc-mul .rc-formula{background:rgba(8,145,178,.12);color:#22d3ee;border:1px solid rgba(8,145,178,.35)}
.rc-tip{font-size:.73rem;color:#667799;margin-top:6px;font-style:italic}

/* 인트로 시각화 */
.rv{display:flex;align-items:center;gap:5px;margin:8px 0;flex-wrap:wrap}
.rv-grp{display:flex;flex-direction:column;align-items:center;gap:2px}
.rv-emj{font-size:.95rem;line-height:1.2}
.rv-lbl{font-size:.65rem;color:#7788aa}
.rv-op{font-size:1.1rem;font-weight:700}
.rv-op.or{color:#e879f9}
.rv-op.mul{color:#22d3ee}

.btn-start{display:block;width:100%;max-width:280px;margin:0 auto;
  background:linear-gradient(135deg,#ffd700,#ff9944);color:#1a0a00;
  border:none;border-radius:12px;padding:12px 0;font-size:1rem;font-weight:700;
  cursor:pointer;font-family:inherit;box-shadow:0 4px 16px rgba(255,215,0,.3);transition:all .2s}
.btn-start:hover{transform:translateY(-2px);box-shadow:0 6px 22px rgba(255,215,0,.5)}

/* ── 퀴즈 화면 ── */
#quiz{display:none}
.sc-card{border-radius:13px;padding:14px;margin-bottom:0}

/* 시각 이미지 */
.visual-row{display:flex;align-items:center;justify-content:center;
  gap:20px;flex-wrap:wrap;background:rgba(0,0,0,.3);
  border-radius:10px;padding:16px 12px;margin-bottom:11px;min-height:140px}
.vg{display:flex;flex-direction:column;align-items:center;gap:6px;
  padding:12px 14px;border-radius:9px;border:1.5px solid}
.vg-emojis{font-size:2.8rem;line-height:1.25;text-align:center;letter-spacing:3px}
.vg-name{font-size:.78rem;font-weight:700;text-align:center}
.vg-count{font-size:1.1rem;font-weight:700;font-family:'Courier New',monospace;
  background:rgba(0,0,0,.3);padding:2px 9px;border-radius:5px;margin-top:1px}

/* 스토리 */
.story{font-size:.83rem;line-height:1.72;color:#b8c8de;margin-bottom:9px}
.story strong{color:#ffd700}
.kw-box{display:inline-block;background:rgba(255,215,0,.1);
  border:1px solid rgba(255,215,0,.3);border-radius:6px;padding:3px 10px;
  font-size:.77rem;color:#ffd700;margin-bottom:10px}
.sc-q{font-size:.86rem;font-weight:700;color:#e2e8ff;background:rgba(255,255,255,.06);
  border-left:3px solid #ffd700;padding:7px 11px;border-radius:0 7px 7px 0;margin-bottom:12px}

/* 선택 버튼 */
.choice-row{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.btn-c{padding:11px 6px;border:2px solid;border-radius:11px;font-size:.88rem;
  font-weight:700;cursor:pointer;font-family:inherit;transition:all .2s;line-height:1.3;text-align:center}
.btn-sum{background:rgba(124,58,237,.1);border-color:#7c3aed;color:#c084fc}
.btn-sum:hover:not(:disabled){background:rgba(124,58,237,.25);transform:translateY(-2px);
  box-shadow:0 4px 14px rgba(124,58,237,.35)}
.btn-mul{background:rgba(8,145,178,.1);border-color:#0891b2;color:#22d3ee}
.btn-mul:hover:not(:disabled){background:rgba(8,145,178,.2);transform:translateY(-2px);
  box-shadow:0 4px 14px rgba(8,145,178,.3)}
.btn-c:disabled{opacity:.55;cursor:default;transform:none!important}
.btn-c.correct{background:rgba(39,174,96,.2)!important;border-color:#27ae60!important;
  color:#66ffcc!important;box-shadow:0 0 14px rgba(39,174,96,.4)}
.btn-c.wrong{background:rgba(231,76,60,.18)!important;border-color:#e74c3c!important;color:#ff9999!important}

/* 피드백 */
.fb-box{display:none;margin-top:11px;padding:11px 13px;border-radius:10px;animation:fadein .3s ease}
.fb-ok{background:rgba(39,174,96,.1);border:1.5px solid #27ae60}
.fb-ng{background:rgba(231,76,60,.1);border:1.5px solid #e74c3c}
.fb-title{font-size:.95rem;font-weight:700;margin-bottom:5px}
.fb-ok .fb-title{color:#66ffcc}
.fb-ng .fb-title{color:#ff9999}
.fb-explain{font-size:.8rem;color:#aabbdd;line-height:1.6;margin-bottom:7px}
.fb-explain strong{color:#e2e8ff}
.fb-formula{font-family:'Courier New',monospace;background:rgba(0,0,0,.35);
  padding:6px 11px;border-radius:6px;font-size:.88rem;color:#ffd700;margin-bottom:7px}
.btn-next{width:100%;padding:9px;background:linear-gradient(135deg,#4f9cf9,#7c3aed);
  border:none;border-radius:9px;color:#fff;font-size:.88rem;font-weight:700;
  cursor:pointer;font-family:inherit;margin-top:4px;transition:all .2s}
.btn-next:hover{transform:translateY(-1px);box-shadow:0 4px 14px rgba(79,156,249,.4)}

/* ── 결과 화면 ── */
#results{display:none;text-align:center}
.res-icon{font-size:3.5rem;margin-bottom:8px}
.res-title{font-size:1.2rem;font-weight:700;color:#ffd700;margin-bottom:5px}
.res-score{font-size:2.2rem;font-weight:700;margin:8px 0;
  background:linear-gradient(135deg,#ffd700,#ff9944);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.res-msg{font-size:.83rem;color:#aabbdd;margin-bottom:14px;line-height:1.65}
.res-summary{text-align:left;margin-bottom:14px}
.res-row{display:flex;align-items:center;gap:7px;padding:6px 10px;
  border-radius:7px;margin-bottom:4px;font-size:.8rem;background:rgba(255,255,255,.04)}
.res-row.rr-ok{border-left:3px solid #27ae60}
.res-row.rr-ng{border-left:3px solid #e74c3c}
.rr-icon{font-size:.9rem}
.rr-title{flex:1;color:#99aabb}
.rr-ans{font-weight:700;font-size:.76rem}
.rr-ok .rr-ans{color:#66ffcc}
.rr-ng .rr-ans{color:#ff9999}
.btn-restart{background:linear-gradient(135deg,#ffd700,#ff9944);color:#1a0a00;
  border:none;border-radius:11px;padding:11px 28px;font-size:.92rem;font-weight:700;
  cursor:pointer;font-family:inherit;transition:all .2s}
.btn-restart:hover{transform:translateY(-2px);box-shadow:0 4px 18px rgba(255,215,0,.4)}

/* 뱃지 */
.badge-row{display:flex;gap:8px;justify-content:center;margin-bottom:12px;flex-wrap:wrap}
.badge{padding:5px 14px;border-radius:99px;font-size:.78rem;font-weight:700}
.badge-sum{background:rgba(124,58,237,.2);border:1px solid #7c3aed;color:#c084fc}
.badge-mul{background:rgba(8,145,178,.15);border:1px solid #0891b2;color:#22d3ee}

@keyframes fadein{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
@keyframes pop{0%{transform:scale(.8)}60%{transform:scale(1.1)}100%{transform:scale(1)}}
.pop{animation:pop .3s ease}

@media(max-width:520px){
  .rule-grid{grid-template-columns:1fr}
  .choice-row{grid-template-columns:1fr}
}
</style>
</head>
<body>

<div class="hdr">
  <h1>🎮 합·곱 법칙 판별 챌린지</h1>
  <p>실생활 사례를 보고 합의 법칙인지 곱의 법칙인지 맞혀보세요!</p>
</div>

<!-- ══ 인트로 ══ -->
<div id="intro">
  <p class="intro-h">경우의 수를 세는 두 가지 법칙</p>
  <p class="intro-sub">두 법칙의 차이를 확인하고 챌린지를 시작하세요!</p>

  <div class="rule-grid">
    <div class="rule-card rc-sum">
      <div class="rc-icon">➕</div>
      <div class="rc-name">합의 법칙</div>
      <div class="rv">
        <div class="rv-grp"><div class="rv-emj">🍱🍱🍱🍱</div><div class="rv-lbl">분식 4가지</div></div>
        <div class="rv-op or">또는</div>
        <div class="rv-grp"><div class="rv-emj">🍚🍚🍚</div><div class="rv-lbl">한식 3가지</div></div>
      </div>
      <div class="rc-desc">A <strong style="color:#e879f9">또는</strong> B 중 <strong>하나만</strong> 선택할 때<br>두 사건이 동시에 일어나지 않으면</div>
      <div class="rc-formula">경우의 수 = A + B</div>
      <div class="rc-tip">💡 키워드: "또는", "중에서 하나", "~이거나"</div>
    </div>

    <div class="rule-card rc-mul">
      <div class="rc-icon">✖️</div>
      <div class="rc-name">곱의 법칙</div>
      <div class="rv">
        <div class="rv-grp"><div class="rv-emj">👕👕👕</div><div class="rv-lbl">상의 3가지</div></div>
        <div class="rv-op mul">×</div>
        <div class="rv-grp"><div class="rv-emj">👖👖👖👖</div><div class="rv-lbl">하의 4가지</div></div>
      </div>
      <div class="rc-desc">A <strong style="color:#22d3ee">그리고</strong> B를 <strong>각각 하나씩</strong> 선택할 때<br>두 사건을 동시에 결정하면</div>
      <div class="rc-formula">경우의 수 = A × B</div>
      <div class="rc-tip">💡 키워드: "각각", "~하고 ~도", "동시에"</div>
    </div>
  </div>

  <button class="btn-start" onclick="startGame()">🚀 챌린지 시작하기!</button>
</div>

<!-- ══ 퀴즈 ══ -->
<div id="quiz">
  <div class="prog-wrap">
    <div class="prog-row">
      <span class="prog-lbl" id="pLbl">문제 1 / 12</span>
      <span class="score-badge">⭐ <span id="sNum">0</span> / 12</span>
    </div>
    <div class="prog-track"><div class="prog-fill" id="pFill" style="width:0%"></div></div>
  </div>
  <div id="qArea"></div>
</div>

<!-- ══ 결과 ══ -->
<div id="results">
  <div class="res-icon" id="resIcon">🏆</div>
  <div class="res-title">챌린지 완료!</div>
  <div class="res-score" id="resScore">12 / 12</div>
  <div class="badge-row">
    <span class="badge badge-sum">합의 법칙</span>
    <span class="badge badge-mul">곱의 법칙</span>
  </div>
  <div class="res-msg" id="resMsg"></div>
  <div class="res-summary" id="resSummary"></div>
  <button class="btn-restart" onclick="restart()">🔄 다시 도전하기</button>
</div>

<script>
const SCENARIOS = [
  {
    rule:"sum",
    bg:"linear-gradient(145deg,#160a28,#0e0619)",border:"#7c3aed",
    title:"🍽️ 점심 메뉴 선택",
    groups:[
      {emojis:"🍱🍱🍱🍱",name:"분식집 메뉴",count:4,c:"#c084fc",bc:"rgba(124,58,237,.3)"},
      {emojis:"🍚🍚🍚",name:"한식집 메뉴",count:3,c:"#74b9ff",bc:"rgba(37,99,235,.3)"}
    ],
    op:"또는",opClass:"or",
    story:"점심시간! 배고픈 민준이는 학교 앞 식당가에서 밥을 먹기로 했어요. 분식집에는 <strong>4가지 메뉴</strong>가, 한식집에는 <strong>3가지 메뉴</strong>가 있어요. 두 식당 중 <strong>한 곳만</strong> 갈 수 있다면, 메뉴를 선택하는 경우의 수는?",
    kw:"두 식당 중 '한 곳만' → 합의 법칙의 신호!",
    q:"❓ 점심 메뉴를 선택하는 경우의 수는 몇 가지?",
    formula:"4 + 3 = 7가지",
    explain:"분식집과 한식집 중 <strong>하나만</strong> 갑니다. '또는' 관계이므로 <strong>합의 법칙</strong>을 적용해요."
  },
  {
    rule:"mul",
    bg:"linear-gradient(145deg,#07172a,#050e1c)",border:"#0891b2",
    title:"👗 교복 코디 완성",
    groups:[
      {emojis:"👕👕👕",name:"상의 종류",count:3,c:"#c084fc",bc:"rgba(124,58,237,.25)"},
      {emojis:"👖👖👖👖",name:"하의 종류",count:4,c:"#22d3ee",bc:"rgba(8,145,178,.25)"}
    ],
    op:"×",opClass:"mul",
    story:"체육복 대신 교복을 입어야 하는 날! 지우의 옷장엔 상의가 <strong>흰 셔츠·체크 남방·후드티</strong> 3가지, 하의가 <strong>검정 바지·청바지·슬랙스·반바지</strong> 4가지 있어요. 상의와 하의를 <strong>각각 하나씩</strong> 골라 입는다면 코디의 경우의 수는?",
    kw:"상의'도' 선택하고 하의'도' 선택 → 곱의 법칙의 신호!",
    q:"❓ 교복 코디의 경우의 수는 몇 가지?",
    formula:"3 × 4 = 12가지",
    explain:"상의 3가지 각각에 대해 하의 4가지를 모두 짝지을 수 있어요. 두 가지를 <strong>동시에 결정</strong>하므로 <strong>곱의 법칙</strong>을 적용해요."
  },
  {
    rule:"sum",
    bg:"linear-gradient(145deg,#0d1a2e,#070f1c)",border:"#2563eb",
    title:"🚌 학교 가는 길",
    groups:[
      {emojis:"🚌🚌🚌",name:"버스 노선",count:3,c:"#feca57",bc:"rgba(234,179,8,.25)"},
      {emojis:"🚇🚇",name:"지하철 노선",count:2,c:"#54a0ff",bc:"rgba(37,99,235,.25)"}
    ],
    op:"또는",opClass:"or",
    story:"은서는 집에서 학교까지 버스나 지하철로 통학해요. 학교로 가는 <strong>버스 노선은 3가지</strong>, <strong>지하철 노선은 2가지</strong>가 있어요. 버스와 지하철 중 <strong>하나의 교통수단</strong>만 이용한다면 이동 방법은 몇 가지일까요?",
    kw:"버스 '또는' 지하철, 하나만 이용 → 합의 법칙의 신호!",
    q:"❓ 학교 가는 방법의 경우의 수는 몇 가지?",
    formula:"3 + 2 = 5가지",
    explain:"버스와 지하철은 동시에 이용할 수 없어요. '또는' 관계이므로 <strong>합의 법칙</strong>을 적용해요."
  },
  {
    rule:"mul",
    bg:"linear-gradient(145deg,#081c10,#050f09)",border:"#059669",
    title:"🍦 아이스크림 주문",
    groups:[
      {emojis:"🍦🍦",name:"콘 종류",count:2,c:"#feca57",bc:"rgba(234,179,8,.25)"},
      {emojis:"🍓🍫🥝🍋🫐",name:"맛 종류",count:5,c:"#ff7675",bc:"rgba(220,38,38,.2)"}
    ],
    op:"×",opClass:"mul",
    story:"아이스크림 가게에 도착한 수아! 콘 종류는 <strong>와플콘·슈가콘</strong> 2가지, 아이스크림 맛은 <strong>딸기·초콜릿·키위·레몬·블루베리</strong> 5가지예요. 콘과 맛을 <strong>각각 하나씩</strong> 고른다면 아이스크림 선택의 경우의 수는?",
    kw:"콘'도' 선택하고 맛'도' 선택 → 곱의 법칙의 신호!",
    q:"❓ 아이스크림 선택의 경우의 수는 몇 가지?",
    formula:"2 × 5 = 10가지",
    explain:"콘 1종류마다 맛 5가지를 각각 짝지을 수 있어요. 두 가지를 <strong>각각 선택</strong>하므로 <strong>곱의 법칙</strong>을 적용해요."
  },
  {
    rule:"sum",
    bg:"linear-gradient(145deg,#1c0a22,#110617)",border:"#9333ea",
    title:"🎬 주말 영화 한 편",
    groups:[
      {emojis:"🎬🎬🎬🎬🎬",name:"액션 영화",count:5,c:"#ff7675",bc:"rgba(220,38,38,.2)"},
      {emojis:"🎭🎭🎭🎭",name:"로맨스 영화",count:4,c:"#f8b4b4",bc:"rgba(244,114,182,.2)"}
    ],
    op:"또는",opClass:"or",
    story:"주말에 영화를 보려는 준혁이! OTT에 <strong>액션 영화 5편</strong>과 <strong>로맨스 영화 4편</strong>이 올라왔어요. 이번 주말엔 <strong>한 편만</strong> 볼 수 있다면 선택할 수 있는 영화는 몇 편일까요?",
    kw:"액션 '또는' 로맨스 중 한 편만 → 합의 법칙의 신호!",
    q:"❓ 선택할 수 있는 영화의 경우의 수는 몇 가지?",
    formula:"5 + 4 = 9편",
    explain:"액션과 로맨스 중 <strong>한 편만</strong> 선택해요. '또는' 관계이므로 <strong>합의 법칙</strong>을 적용해요."
  },
  {
    rule:"mul",
    bg:"linear-gradient(145deg,#08182e,#050f1e)",border:"#1d4ed8",
    title:"✈️ 여행 계획 세우기",
    groups:[
      {emojis:"✈️✈️✈️",name:"항공편",count:3,c:"#74b9ff",bc:"rgba(29,78,216,.25)"},
      {emojis:"🏨🏨🏨🏨",name:"숙소",count:4,c:"#55efc4",bc:"rgba(5,150,105,.25)"}
    ],
    op:"×",opClass:"mul",
    story:"방학을 맞아 제주도 여행을 계획 중인 현지 가족! 이용할 수 있는 <strong>항공편이 3가지</strong>, 묵을 수 있는 <strong>숙소가 4곳</strong> 있어요. 항공편과 숙소를 <strong>각각 하나씩</strong> 예약한다면 경우의 수는?",
    kw:"항공편'도' 결정하고 숙소'도' 결정 → 곱의 법칙의 신호!",
    q:"❓ 여행 계획의 경우의 수는 몇 가지?",
    formula:"3 × 4 = 12가지",
    explain:"항공편 3가지 각각에 대해 숙소 4가지를 짝지을 수 있어요. <strong>두 가지를 동시에 결정</strong>하므로 <strong>곱의 법칙</strong>을 적용해요."
  },
  {
    rule:"sum",
    bg:"linear-gradient(145deg,#1a1608,#100e05)",border:"#ca8a04",
    title:"🍬 편의점 간식 선택",
    groups:[
      {emojis:"🍪🍪🍪",name:"과자류",count:3,c:"#feca57",bc:"rgba(234,179,8,.25)"},
      {emojis:"🧃🧃🧃🧃",name:"음료류",count:4,c:"#48dbfb",bc:"rgba(8,145,178,.25)"}
    ],
    op:"또는",opClass:"or",
    story:"수업이 끝난 후 배고픈 태민이가 편의점에 들렀어요. 오늘은 용돈이 부족해서 <strong>과자 3가지</strong>와 <strong>음료 4가지</strong> 중 <strong>하나만</strong> 살 수 있어요. 살 수 있는 간식의 경우의 수는?",
    kw:"과자 '또는' 음료 중 하나만 구매 → 합의 법칙의 신호!",
    q:"❓ 간식을 선택하는 경우의 수는 몇 가지?",
    formula:"3 + 4 = 7가지",
    explain:"과자와 음료 중 <strong>하나만</strong> 살 수 있어요. '또는' 관계이므로 <strong>합의 법칙</strong>을 적용해요."
  },
  {
    rule:"mul",
    bg:"linear-gradient(145deg,#1a0820,#0f0414)",border:"#be185d",
    title:"🎁 선물 포장 꾸미기",
    groups:[
      {emojis:"📦📦📦",name:"포장 상자",count:3,c:"#f59e0b",bc:"rgba(245,158,11,.2)"},
      {emojis:"🎀🎀🎀🎀",name:"리본 색상",count:4,c:"#f472b6",bc:"rgba(236,72,153,.2)"}
    ],
    op:"×",opClass:"mul",
    story:"친구 생일 선물을 포장하려는 유나! 포장 상자는 <strong>하트·줄무늬·도트 무늬</strong> 3가지, 리본 색상은 <strong>빨강·파랑·노랑·보라</strong> 4가지예요. 상자와 리본을 <strong>각각 하나씩</strong> 고른다면 포장 방법은 몇 가지일까요?",
    kw:"상자'도' 고르고 리본'도' 고르기 → 곱의 법칙의 신호!",
    q:"❓ 선물 포장 방법의 경우의 수는 몇 가지?",
    formula:"3 × 4 = 12가지",
    explain:"상자 3가지 각각에 리본 4가지를 짝지을 수 있어요. <strong>두 가지를 동시에 결정</strong>하므로 <strong>곱의 법칙</strong>을 적용해요."
  },
  {
    rule:"sum",
    bg:"linear-gradient(145deg,#0e1c2e,#080f1c)",border:"#3b82f6",
    title:"🎸 방과후 동아리 선택",
    groups:[
      {emojis:"🎸🎸🎸",name:"현악기 동아리",count:3,c:"#feca57",bc:"rgba(234,179,8,.25)"},
      {emojis:"🎺🎺🎺🎺",name:"관악기 동아리",count:4,c:"#ff9f43",bc:"rgba(249,115,22,.2)"}
    ],
    op:"또는",opClass:"or",
    story:"동아리를 정해야 하는 수현이! 현악기 동아리 <strong>(기타·바이올린·첼로)</strong> 3개와 관악기 동아리 <strong>(플루트·클라리넷·트럼펫·색소폰)</strong> 4개 중 <strong>하나만</strong> 들어갈 수 있어요. 동아리 선택의 경우의 수는?",
    kw:"현악기 '또는' 관악기 동아리 하나만 → 합의 법칙의 신호!",
    q:"❓ 동아리를 선택하는 경우의 수는 몇 가지?",
    formula:"3 + 4 = 7가지",
    explain:"두 종류의 동아리 중 <strong>하나만</strong> 선택할 수 있어요. '또는' 관계이므로 <strong>합의 법칙</strong>을 적용해요."
  },
  {
    rule:"mul",
    bg:"linear-gradient(145deg,#1a0a08,#0f0604)",border:"#c2410c",
    title:"🍔 세트 메뉴 만들기",
    groups:[
      {emojis:"🍔🌮🍕",name:"메인 메뉴",count:3,c:"#fb923c",bc:"rgba(249,115,22,.2)"},
      {emojis:"🥤🧋🍵🍺",name:"음료 메뉴",count:4,c:"#fbbf24",bc:"rgba(245,158,11,.2)"}
    ],
    op:"×",opClass:"mul",
    story:"패스트푸드점에서 세트 메뉴를 주문하려는 재훈이! 메인 메뉴는 <strong>버거·타코·피자</strong> 3가지, 음료는 <strong>콜라·버블티·커피·맥주</strong> 4가지예요. 메인과 음료를 <strong>각각 하나씩</strong> 골라 세트를 구성하면 경우의 수는?",
    kw:"메인'도' 고르고 음료'도' 고르기 → 곱의 법칙의 신호!",
    q:"❓ 세트 메뉴 구성의 경우의 수는 몇 가지?",
    formula:"3 × 4 = 12가지",
    explain:"메인 3가지 각각에 음료 4가지를 짝지을 수 있어요. <strong>두 가지를 동시에 결정</strong>하므로 <strong>곱의 법칙</strong>을 적용해요."
  },
  {
    rule:"sum",
    bg:"linear-gradient(145deg,#0a1e1a,#060f0d)",border:"#0f766e",
    title:"⚽ 방과후 체육 신청",
    groups:[
      {emojis:"⚽🏀🏸",name:"구기 종목",count:3,c:"#34d399",bc:"rgba(5,150,105,.25)"},
      {emojis:"🏊🏊🏊🏊",name:"수영 강좌",count:4,c:"#38bdf8",bc:"rgba(14,165,233,.25)"}
    ],
    op:"또는",opClass:"or",
    story:"방과후 체육 활동을 신청하는 도현이! 구기 종목 <strong>(축구·농구·배드민턴)</strong> 3가지와 수영 강좌 <strong>(자유형·배영·평영·접영)</strong> 4가지 중 <strong>하나만</strong> 신청할 수 있어요. 신청 가능한 경우의 수는?",
    kw:"구기 '또는' 수영 중 하나만 → 합의 법칙의 신호!",
    q:"❓ 방과후 체육 신청의 경우의 수는 몇 가지?",
    formula:"3 + 4 = 7가지",
    explain:"구기 종목과 수영 강좌 중 <strong>하나만</strong> 선택할 수 있어요. '또는' 관계이므로 <strong>합의 법칙</strong>을 적용해요."
  },
  {
    rule:"mul",
    bg:"linear-gradient(145deg,#180818,#0e0510)",border:"#9d174d",
    title:"🔐 자물쇠 비밀번호",
    groups:[
      {emojis:"🔤🔤🔤···",name:"알파벳 대문자 (A~Z)",count:26,c:"#6ee7b7",bc:"rgba(5,150,105,.2)"},
      {emojis:"0️⃣1️⃣···9️⃣",name:"한 자리 숫자 (0~9)",count:10,c:"#fbbf24",bc:"rgba(245,158,11,.2)"}
    ],
    op:"×",opClass:"mul",
    story:"자물쇠 비밀번호를 설정하는 나은이! 비밀번호는 <strong>알파벳 대문자 1개</strong>와 <strong>한 자리 숫자 1개</strong>의 조합이에요 (예: A5, Z3). 알파벳 대문자는 A~Z까지 <strong>26가지</strong>, 숫자는 0~9까지 <strong>10가지</strong>예요. 만들 수 있는 비밀번호는 몇 가지일까요?",
    kw:"알파벳'도' 고르고 숫자'도' 고르기 → 곱의 법칙의 신호!",
    q:"❓ 만들 수 있는 비밀번호의 경우의 수는 몇 가지?",
    formula:"26 × 10 = 260가지",
    explain:"알파벳 26가지 각각에 숫자 10가지를 짝지을 수 있어요. <strong>두 가지를 동시에 결정</strong>하므로 <strong>곱의 법칙</strong>을 적용해요."
  }
];

// 시나리오 순서 섞기
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

let scenarios = [];
let idx = 0, score = 0, answered = [];

function startGame() {
  scenarios = shuffle(SCENARIOS);
  idx = 0; score = 0; answered = [];
  document.getElementById('intro').style.display = 'none';
  document.getElementById('quiz').style.display = 'block';
  render(0);
}

function render(i) {
  const s = scenarios[i];
  const n = i + 1, total = scenarios.length;
  document.getElementById('pLbl').textContent = `문제 ${n} / ${total}`;
  document.getElementById('sNum').textContent = score;
  document.getElementById('pFill').style.width = (i / total * 100) + '%';

  const vgs = s.groups.map(g => `
    <div class="vg" style="border-color:${g.bc};background:${g.bc}">
      <div class="vg-emojis">${g.emojis}</div>
      <div class="vg-name" style="color:${g.c}">${g.name}</div>
      <div class="vg-count" style="color:${g.c}">${g.count}가지</div>
    </div>
  `).join('');

  document.getElementById('qArea').innerHTML = `
    <div class="sc-card" style="background:${s.bg};border:1.5px solid ${s.border}">
      <div style="font-size:.88rem;font-weight:700;color:#ffd700;margin-bottom:10px">${s.title}</div>
      <div class="visual-row">${vgs}</div>
      <div class="story">${s.story}</div>
      <div class="kw-box">🔑 ${s.kw}</div>
      <div class="sc-q">${s.q}</div>
      <div class="choice-row">
        <button class="btn-c btn-sum" onclick="choose('sum',this)">➕ 합의 법칙<br><span style="font-size:.75rem;font-weight:400">(경우의 수를 더한다)</span></button>
        <button class="btn-c btn-mul" onclick="choose('mul',this)">✖️ 곱의 법칙<br><span style="font-size:.75rem;font-weight:400">(경우의 수를 곱한다)</span></button>
      </div>
      <div class="fb-box" id="fb"></div>
    </div>
  `;
}

function choose(choice, btn) {
  const s = scenarios[idx];
  const correct = choice === s.rule;
  if (correct) score++;
  answered.push({ title: s.title, correct, rule: s.rule });

  // 버튼 피드백
  const btns = btn.closest('.choice-row').querySelectorAll('.btn-c');
  btns.forEach(b => b.disabled = true);
  const correctClass = s.rule === 'sum' ? 'btn-sum' : 'btn-mul';
  btn.classList.add(correct ? 'correct' : 'wrong');
  btn.closest('.choice-row').querySelectorAll('.' + correctClass).forEach(b => b.classList.add('correct'));

  // 피드백 박스
  const fb = document.getElementById('fb');
  fb.className = 'fb-box ' + (correct ? 'fb-ok' : 'fb-ng');
  fb.style.display = 'block';
  fb.innerHTML = `
    <div class="fb-title">${correct ? '✅ 정답이에요!' : '❌ 아쉬워요!'}</div>
    <div class="fb-explain">${s.explain}</div>
    <div class="fb-formula">📐 ${s.formula}</div>
    <button class="btn-next pop" onclick="next()">${idx + 1 < scenarios.length ? '다음 문제 →' : '결과 보기 🏁'}</button>
  `;

  document.getElementById('sNum').textContent = score;
}

function next() {
  idx++;
  if (idx >= scenarios.length) { showResults(); return; }
  render(idx);
}

function showResults() {
  document.getElementById('quiz').style.display = 'none';
  const res = document.getElementById('results');
  res.style.display = 'block';

  const pct = score / scenarios.length;
  let icon, msg;
  if (pct === 1)      { icon = '🏆'; msg = '완벽해요! 합의 법칙과 곱의 법칙을 완전히 마스터했어요! 두 법칙의 핵심 키워드를 정확히 파악하고 있군요 🎉'; }
  else if (pct >= .8) { icon = '🌟'; msg = '훌륭해요! 두 법칙의 차이를 잘 이해하고 있어요. 틀린 문제를 다시 한번 살펴보면 완벽해질 거예요!'; }
  else if (pct >= .6) { icon = '👍'; msg = '잘했어요! 조금 더 연습이 필요하지만 기초는 잡혔어요. \'또는\'과 \'각각\' 키워드를 다시 생각해 보세요.'; }
  else                { icon = '💪'; msg = '도전 정신이 멋져요! 합의 법칙과 곱의 법칙의 핵심 차이를 한 번 더 복습하고 다시 도전해 보세요!'; }

  document.getElementById('resIcon').textContent = icon;
  document.getElementById('resScore').textContent = score + ' / ' + scenarios.length;
  document.getElementById('resMsg').textContent = msg.replace(/'/g,"'");

  const rows = answered.map(a => `
    <div class="res-row ${a.correct ? 'rr-ok' : 'rr-ng'}">
      <span class="rr-icon">${a.correct ? '✅' : '❌'}</span>
      <span class="rr-title">${a.title}</span>
      <span class="rr-ans">${a.rule === 'sum' ? '합의 법칙' : '곱의 법칙'}</span>
    </div>
  `).join('');
  document.getElementById('resSummary').innerHTML = rows;
  document.getElementById('pFill').style.width = '100%';
}

function restart() {
  document.getElementById('results').style.display = 'none';
  document.getElementById('intro').style.display = 'block';
}
</script>
</body>
</html>"""


def render():
    st.markdown("### 🎮 합·곱 법칙 판별 챌린지")
    st.markdown(
        "실생활 속 **12가지 사례**를 보고 **합의 법칙**인지 **곱의 법칙**인지 판별해 보세요!"
    )
    components.html(_HTML, height=980, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
