import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "모라게임"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 모라 게임과 같은 것이 있는 순열에 대한 탐구 질문**"},
    {"key": "경우의수계산",  "label": "세 사람이 모라 게임을 할 때 각자 0~5 손가락을 내면, 전체 가능한 경우의 수는 몇 가지인지 구하고 그 이유를 설명해 보세요.", "type": "text_area", "height": 90},
    {"key": "필승전략분석", "label": "기본 규칙(두 사람, 0~5 손가락, 합 맞히기)에서 경우의 수 표를 완성했을 때, 어떤 합을 불러야 이길 가능성이 높은지 이유와 함께 설명해 보세요.", "type": "text_area", "height": 90},
    {"key": "규칙변형아이디어", "label": "규칙을 바꾸어 새로운 모라 게임을 만들어 보고(예: 손가락 범위, 인원, 합·곱 판정 등), 그 게임의 필승 전략을 수학적으로 분석해 보세요.", "type": "text_area", "height": 100},
    {"key": "새롭게알게된점", "label": "💡 이 활동을 통해 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 이 활동을 통해 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title":       "미니: 손가락 게임 '모라'와 같은 것이 있는 순열",
    "description": "이탈리아 전통 손가락 게임 '모라'를 시뮬레이션하며 중복순열·같은 것이 있는 순열로 경우의 수를 분석하고 필승 전략을 탐구합니다.",
    "order":       21,
}

# ──────────────────────────────────────────────────────────────────────────────
_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
/* ── 기본 리셋 & 배경 ──────────────────────────────── */
*{box-sizing:border-box;margin:0;padding:0}
html,body{
  background:linear-gradient(135deg,#0a0f1e 0%,#0d1b2a 60%,#0a0f1e 100%);
  min-height:100vh;font-family:'Segoe UI',system-ui,sans-serif;
  color:#e2e8f0;font-size:14px;
}
.wrap{padding:16px;display:flex;flex-direction:column;gap:16px;max-width:860px;margin:0 auto}

/* ── 카드 ─────────────────────────────────────────── */
.card{
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
  border-radius:20px;padding:20px 24px;backdrop-filter:blur(12px);
}
.card-title{
  font-size:15px;font-weight:700;color:#fbbf24;margin-bottom:14px;
  display:flex;align-items:center;gap:8px;letter-spacing:.02em
}

/* ── 탭 ──────────────────────────────────────────── */
.tab-bar{display:flex;gap:8px;flex-wrap:wrap}
.tab-btn{
  padding:8px 18px;border-radius:12px;border:1px solid rgba(255,255,255,.15);
  background:rgba(255,255,255,.04);cursor:pointer;font-size:13px;font-weight:600;
  color:#94a3b8;transition:.2s;
}
.tab-btn:hover{background:rgba(255,255,255,.09);color:#e2e8f0}
.tab-btn.active{background:rgba(245,158,11,.2);color:#fbbf24;border-color:rgba(245,158,11,.4)}
.tab-panel{display:none}.tab-panel.active{display:block}

/* ── 손가락 그리드 ────────────────────────────────── */
.finger-grid{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:8px 0}
.finger-btn{
  width:64px;height:64px;border-radius:14px;border:2px solid rgba(255,255,255,.15);
  background:rgba(255,255,255,.04);cursor:pointer;font-size:32px;
  transition:.25s;display:flex;align-items:center;justify-content:center;
  position:relative;user-select:none;
}
.finger-btn:hover{background:rgba(245,158,11,.15);border-color:rgba(245,158,11,.4);transform:scale(1.1)}
.finger-btn.selected{
  background:rgba(245,158,11,.3);border-color:#fbbf24;
  box-shadow:0 0 14px rgba(245,158,11,.5);transform:scale(1.12)
}
.finger-label{
  position:absolute;bottom:3px;right:6px;font-size:10px;
  color:#94a3b8;font-weight:700;
}

/* ── 숫자 그리드 (불리는 숫자) ────────────────────── */
.num-grid{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:8px 0}
.num-btn{
  width:50px;height:50px;border-radius:12px;border:2px solid rgba(255,255,255,.15);
  background:rgba(255,255,255,.04);cursor:pointer;font-size:20px;font-weight:800;
  color:#e2e8f0;transition:.25s;display:flex;align-items:center;justify-content:center;
}
.num-btn:hover{background:rgba(99,102,241,.2);border-color:rgba(99,102,241,.5);transform:scale(1.08)}
.num-btn.selected{
  background:rgba(99,102,241,.35);border-color:#818cf8;
  box-shadow:0 0 14px rgba(99,102,241,.5);color:#fff
}

/* ── 액션 버튼 ───────────────────────────────────── */
.btn{
  padding:12px 28px;border-radius:14px;border:none;cursor:pointer;
  font-size:15px;font-weight:700;transition:.2s;letter-spacing:.02em;
}
.btn-primary{
  background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;
  box-shadow:0 4px 16px rgba(245,158,11,.4)
}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(245,158,11,.5)}
.btn-primary:disabled{opacity:.45;cursor:not-allowed;transform:none}
.btn-secondary{
  background:rgba(255,255,255,.07);color:#94a3b8;
  border:1px solid rgba(255,255,255,.15)
}
.btn-secondary:hover{background:rgba(255,255,255,.12);color:#e2e8f0}

/* ── 결과 표시 ───────────────────────────────────── */
.result-box{
  border-radius:16px;padding:18px 22px;text-align:center;margin:12px 0;
  font-size:22px;font-weight:800;letter-spacing:.04em;transition:.4s all;
}
.result-win{
  background:linear-gradient(135deg,rgba(16,185,129,.25),rgba(5,150,105,.15));
  border:2px solid rgba(16,185,129,.5);color:#6ee7b7;
  box-shadow:0 0 24px rgba(16,185,129,.2)
}
.result-lose{
  background:linear-gradient(135deg,rgba(239,68,68,.2),rgba(185,28,28,.15));
  border:2px solid rgba(239,68,68,.4);color:#fca5a5;
  box-shadow:0 0 24px rgba(239,68,68,.15)
}
.result-draw{
  background:linear-gradient(135deg,rgba(99,102,241,.2),rgba(67,56,202,.15));
  border:2px solid rgba(99,102,241,.4);color:#a5b4fc
}
.result-none{
  background:rgba(255,255,255,.03);border:1px dashed rgba(255,255,255,.15);
  color:#475569;font-size:14px;padding:14px 22px;
}

/* ── 스코어 KPI ──────────────────────────────────── */
.kpi-row{display:flex;gap:10px;flex-wrap:wrap}
.kpi{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:14px;padding:10px 18px;text-align:center;flex:1;min-width:80px
}
.kpi .num{font-size:30px;font-weight:900}
.kpi .lbl{font-size:10px;color:#94a3b8;margin-top:3px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
.kpi.green .num{color:#6ee7b7}
.kpi.red   .num{color:#fca5a5}
.kpi.blue  .num{color:#a5b4fc}
.kpi.gold  .num{color:#fbbf24}

/* ── 통계 표 ────────────────────────────────────── */
table{width:100%;border-collapse:collapse;font-size:13px}
th{background:rgba(245,158,11,.12);color:#fbbf24;padding:8px 12px;
   border:1px solid rgba(255,255,255,.08);text-align:center;font-weight:700}
td{background:rgba(255,255,255,.03);color:#e2e8f0;padding:7px 12px;
   border:1px solid rgba(255,255,255,.06);text-align:center}
.td-max{background:rgba(16,185,129,.15);color:#6ee7b7;font-weight:800}
.td-min{background:rgba(239,68,68,.1);color:#fca5a5}

/* ── 설명 박스 ───────────────────────────────────── */
.info-box{
  background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.2);
  border-radius:14px;padding:14px 18px;font-size:13px;line-height:1.8;color:#c7d2fe
}
.info-box b{color:#a5b4fc}
.hl{color:#fbbf24;font-weight:700}
.formula{
  background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.25);
  border-radius:12px;padding:10px 18px;text-align:center;font-size:18px;
  font-weight:800;color:#fbbf24;margin:10px 0;font-family:monospace
}

/* ── AI 전략 출력 ─────────────────────────────────── */
.ai-thought{
  background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.25);
  border-radius:14px;padding:14px 18px;font-size:13px;color:#ddd6fe;line-height:1.8;
  margin-bottom:8px;
}
.ai-thought b{color:#c4b5fd}

/* ── 손가락 이모지 표 ─────────────────────────────── */
.hand-row{display:flex;gap:6px;justify-content:center;margin:4px 0}
.hand-chip{
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  border-radius:10px;padding:6px 10px;font-size:22px;text-align:center;
  cursor:default;
}

/* 스크롤바 */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(245,158,11,.4);border-radius:3px}

/* 로그 */
.log-item{
  padding:8px 12px;border-radius:10px;font-size:12px;margin-bottom:6px;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);
  display:flex;gap:10px;align-items:center;
}
.log-w{border-left:3px solid #6ee7b7}
.log-l{border-left:3px solid #fca5a5}
.log-d{border-left:3px solid #a5b4fc}
.badge{
  font-size:10px;padding:2px 8px;border-radius:6px;font-weight:700;flex-shrink:0;
}
.badge-w{background:rgba(16,185,129,.25);color:#6ee7b7}
.badge-l{background:rgba(239,68,68,.2);color:#fca5a5}
.badge-d{background:rgba(99,102,241,.2);color:#a5b4fc}

.section-label{font-size:12px;color:#64748b;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}
</style>
</head>
<body>
<div class="wrap">

<!-- ══ 탭 네비게이션 ════════════════════════════════ -->
<div class="card" style="padding:14px 20px">
  <div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab('rules',this)">📖 게임 규칙</button>
    <button class="tab-btn"        onclick="switchTab('play',this)">🎮 게임 플레이</button>
    <button class="tab-btn"        onclick="switchTab('analysis',this)">📊 경우의 수 분석</button>
    <button class="tab-btn"        onclick="switchTab('strategy',this)">🧠 필승 전략 탐구</button>
  </div>
</div>

<!-- ══ 탭 1: 게임 규칙 ══════════════════════════════ -->
<div class="tab-panel active" id="tab-rules">
  <div class="card">
    <div class="card-title">📖 모라(Morra) 게임이란?</div>
    <div class="info-box" style="margin-bottom:14px">
      <b>'모라(Morra)'</b>는 고대 로마 시대부터 이탈리아 사람들이 즐겨온 손가락 게임입니다.<br>
      두 사람(또는 세 사람)이 <b>동시에</b> 손가락을 내밀면서, 동시에 두 사람이 내는
      <b>손가락 개수의 합</b>을 외칩니다. 자신이 말한 합과 실제 합이 일치하면 이깁니다!
    </div>

    <div class="card-title" style="margin-top:4px">🖐 기본 규칙 (두 사람 버전)</div>
    <div class="info-box">
      <b>① 준비</b>: 두 플레이어가 마주 보고 섭니다.<br>
      <b>② 동시에</b>: 0~5 중 하나를 손가락으로 표시하면서 동시에 두 손가락 합을 예측해 외칩니다.<br>
      &nbsp;&nbsp;　　  부를 수 있는 숫자 범위: <span class="hl">0부터 10</span> (0+0 ~ 5+5)<br>
      <b>③ 판정</b>: 실제 합 = 외친 숫자 → 이긴 사람에게 1점<br>
      &nbsp;&nbsp;　　  둘 다 맞히거나 둘 다 틀리면 → 무승부 (다시 진행)<br>
      <b>④ 목표</b>: 정해진 점수(기본: 3점)에 먼저 도달하면 승!
    </div>

    <div class="card-title" style="margin-top:18px">📐 교과서 예제: 세 사람이 7을 말하면?</div>
    <div class="info-box">
      세 사람이 각자 손가락을 내고, <b>세 명의 합 = 7</b>인 경우를 따져봅시다.<br>
      순서가 다르면 다른 경우로 셉니다 → <b>같은 것이 있는 순열</b> 활용!<br><br>
      예) (1, 1, 5): 숫자 1이 두 개, 5가 하나 → <span class="hl">3! ÷ 2!1! = 3</span>가지<br>
      예) (1, 2, 4): 모두 다른 수 → <span class="hl">3! = 6</span>가지<br>
      예) (2, 2, 3): 숫자 2가 두 개 → <span class="hl">3! ÷ 2! = 3</span>가지<br>
      예) (3, 3, 1): 숫자 3이 두 개 → <span class="hl">3! ÷ 2! = 3</span>가지<br><br>
      <b>합계: 6 + 3 + 3 + 3 = 15가지</b>
      <div class="formula">3! + 3!/2! + 3!/2! + 3!/2! = 6 + 3 + 3 + 3 = 15</div>
    </div>

    <div class="card-title" style="margin-top:18px">✋ 손가락 기호표</div>
    <div class="hand-row">
      <div class="hand-chip">✊<br><span style="font-size:12px;color:#94a3b8">0개</span></div>
      <div class="hand-chip">☝️<br><span style="font-size:12px;color:#94a3b8">1개</span></div>
      <div class="hand-chip">✌️<br><span style="font-size:12px;color:#94a3b8">2개</span></div>
      <div class="hand-chip">🤟<br><span style="font-size:12px;color:#94a3b8">3개</span></div>
      <div class="hand-chip">🖖<br><span style="font-size:12px;color:#94a3b8">4개</span></div>
      <div class="hand-chip">🖐<br><span style="font-size:12px;color:#94a3b8">5개</span></div>
    </div>
  </div>
</div>

<!-- ══ 탭 2: 게임 플레이 ════════════════════════════ -->
<div class="tab-panel" id="tab-play">
  <div class="card">
    <div class="card-title">🎮 모라 게임 플레이 (vs AI)</div>
    
    <!-- 모드 설정 -->
    <div style="display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap">
      <div>
        <div class="section-label">게임 모드</div>
        <div style="display:flex;gap:8px">
          <button class="tab-btn active" id="modeBtn2" onclick="setMode(2)">👥 2인 (기본)</button>
          <button class="tab-btn"        id="modeBtn3" onclick="setMode(3)">👥👤 3인</button>
        </div>
      </div>
      <div>
        <div class="section-label">AI 난이도</div>
        <div style="display:flex;gap:8px">
          <button class="tab-btn active" id="diffEasy"   onclick="setDiff('easy')">😊 쉬움</button>
          <button class="tab-btn"        id="diffNormal" onclick="setDiff('normal')">😐 보통</button>
          <button class="tab-btn"        id="diffHard"   onclick="setDiff('hard')">😈 어려움</button>
        </div>
        <div id="diffDesc" style="margin-top:8px;font-size:11px;color:#94a3b8;line-height:1.6;
          background:rgba(255,255,255,.04);border-radius:8px;padding:7px 12px;max-width:320px">
          🎲 AI가 손가락과 예측 숫자를 <b style="color:#e2e8f0">완전 무작위</b>로 선택합니다.
        </div>
      </div>
      <div>
        <div class="section-label">목표 점수</div>
        <div style="display:flex;gap:8px">
          <button class="tab-btn active" id="goal3" onclick="setGoal(3)">3점</button>
          <button class="tab-btn"        id="goal5" onclick="setGoal(5)">5점</button>
          <button class="tab-btn"        id="goal7" onclick="setGoal(7)">7점</button>
        </div>
      </div>
    </div>

    <!-- 점수판 -->
    <div class="kpi-row" style="margin-bottom:14px">
      <div class="kpi green"><div class="num" id="scorePlayer">0</div><div class="lbl">나 (승)</div></div>
      <div class="kpi red">  <div class="num" id="scoreAI">0</div>   <div class="lbl">AI (승)</div></div>
      <div class="kpi blue"> <div class="num" id="scoreDraw">0</div>  <div class="lbl">무승부</div></div>
      <div class="kpi gold"> <div class="num" id="scoreRound">0</div> <div class="lbl">라운드</div></div>
    </div>
    <div id="gameProgressBar" style="height:8px;border-radius:4px;background:rgba(255,255,255,.06);margin-bottom:16px;overflow:hidden">
      <div id="progressInner" style="height:100%;width:0%;background:linear-gradient(90deg,#10b981,#f59e0b);transition:.4s;border-radius:4px"></div>
    </div>

    <!-- 내 선택 -->
    <div class="section-label">① 내 손가락 선택</div>
    <div class="finger-grid" id="myFingers"></div>

    <!-- 내가 예측하는 합 -->
    <div class="section-label" style="margin-top:12px">② 내가 예측하는 합 (외칠 숫자)</div>
    <div class="num-grid" id="myGuess"></div>

    <!-- 플레이 버튼 -->
    <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap">
      <button class="btn btn-primary" id="playBtn" onclick="playRound()" disabled>
        ✊ 내기!
      </button>
      <button class="btn btn-secondary" onclick="resetGame()">🔄 게임 초기화</button>
    </div>

    <!-- 결과 -->
    <div id="roundResult" class="result-box result-none" style="margin-top:14px">
      손가락과 숫자를 선택한 뒤 "내기!" 버튼을 누르세요.
    </div>

    <!-- 이번 라운드 상세 -->
    <div id="roundDetail" style="display:none;margin-top:8px">
      <div class="info-box" id="roundDetailBox"></div>
    </div>
  </div>

  <!-- 게임 로그 -->
  <div class="card">
    <div class="card-title">📋 게임 기록</div>
    <div id="gameLog" style="max-height:240px;overflow-y:auto">
      <div style="color:#475569;font-size:13px;text-align:center;padding:20px">게임을 시작하면 기록이 쌓입니다.</div>
    </div>
  </div>
</div>

<!-- ══ 탭 3: 경우의 수 분석 ════════════════════════ -->
<div class="tab-panel" id="tab-analysis">
  <div class="card">
    <div class="card-title">📊 두 사람 모라: 합별 경우의 수</div>
    <div class="info-box" style="margin-bottom:14px">
      두 사람이 각각 <b>0~5</b> 손가락을 내는 모든 경우 = <span class="hl">6 × 6 = 36가지</span><br>
      각 합(0~10)별로 얼마나 많은 경우가 있는지 확인해 보세요!<br>
      <b>경우의 수가 큰 합을 외쳐야 이길 확률이 높아집니다.</b>
    </div>

    <!-- 합 선택 -->
    <div class="section-label">합을 선택하면 해당 경우를 모두 볼 수 있습니다</div>
    <div class="num-grid" id="analysisNums"></div>

    <!-- 막대 차트 -->
    <div style="margin:16px 0" id="barChart"></div>

    <!-- 선택된 합의 경우 목록 -->
    <div id="caseList" style="display:none">
      <div class="section-label" id="caseListTitle"></div>
      <div id="caseListContent" style="display:flex;flex-wrap:wrap;gap:8px"></div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">📐 세 사람 모라: 합별 경우의 수</div>
    <div class="info-box" style="margin-bottom:14px">
      세 사람이 각각 <b>0~5</b> 손가락 → 전체 <span class="hl">6³ = 216가지</span><br>
      같은 것이 있는 순열로 계산: 합이 s인 순열의 수 = Σ <b>3! ÷ (a!b!c!)</b>
    </div>
    <div id="barChart3"></div>
    <div class="num-grid" id="analysisNums3" style="margin-top:12px"></div>
    <div id="caseList3" style="display:none;margin-top:10px">
      <div class="section-label" id="caseList3Title"></div>
      <div id="caseList3Content" style="display:flex;flex-wrap:wrap;gap:8px"></div>
    </div>
  </div>
</div>

<!-- ══ 탭 4: 필승 전략 탐구 ══════════════════════════ -->
<div class="tab-panel" id="tab-strategy">
  <div class="card">
    <div class="card-title">🧠 필승 전략 시뮬레이션</div>
    <div class="info-box" style="margin-bottom:14px">
      아래에서 <b>나의 전략</b>과 <b>AI 전략</b>을 각각 고른 뒤, 1000번 시뮬레이션을 돌려보세요.<br>
      어떤 조합이 가장 유리한지 데이터로 확인해 봅시다!
    </div>

    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
      <div style="flex:1;min-width:200px">
        <div class="section-label">나의 전략</div>
        <div style="display:flex;flex-direction:column;gap:6px" id="myStratBtns">
          <button class="tab-btn active" onclick="setMyStrat('random')" id="s_my_random">🎲 무작위</button>
          <button class="tab-btn"        onclick="setMyStrat('max')"    id="s_my_max">📈 최빈 합 선택 (9: 경우의 수 최대)</button>
          <button class="tab-btn"        onclick="setMyStrat('even')"   id="s_my_even">🔢 짝수 선택 전략</button>
          <button class="tab-btn"        onclick="setMyStrat('odd')"    id="s_my_odd">🔣 홀수 선택 전략</button>
          <button class="tab-btn"        onclick="setMyStrat('mixed')"  id="s_my_mixed">🎯 5+6+7+8+9 균등 선택</button>
        </div>
      </div>
      <div style="flex:1;min-width:200px">
        <div class="section-label">AI 전략</div>
        <div style="display:flex;flex-direction:column;gap:6px" id="aiStratBtns">
          <button class="tab-btn active" onclick="setAIStrat('random')" id="s_ai_random">🎲 무작위</button>
          <button class="tab-btn"        onclick="setAIStrat('max')"    id="s_ai_max">📈 최빈 합 선택 (9)</button>
          <button class="tab-btn"        onclick="setAIStrat('even')"   id="s_ai_even">🔢 짝수 선택 전략</button>
          <button class="tab-btn"        onclick="setAIStrat('odd')"    id="s_ai_odd">🔣 홀수 선택 전략</button>
          <button class="tab-btn"        onclick="setAIStrat('mixed')"  id="s_ai_mixed">🎯 5+6+7+8+9 균등 선택</button>
        </div>
      </div>
    </div>

    <button class="btn btn-primary" onclick="runSimulation()">▶ 1000회 시뮬레이션 실행</button>

    <div id="simResult" style="margin-top:16px;display:none">
      <div class="kpi-row" style="margin-bottom:12px">
        <div class="kpi green"><div class="num" id="simWin">—</div><div class="lbl">나 승</div></div>
        <div class="kpi red">  <div class="num" id="simLose">—</div><div class="lbl">AI 승</div></div>
        <div class="kpi blue"> <div class="num" id="simDraw">—</div><div class="lbl">무승부</div></div>
      </div>
      <div id="simBar" style="height:28px;border-radius:8px;overflow:hidden;display:flex;gap:2px;margin-bottom:12px"></div>
      <div class="info-box" id="simAnalysis"></div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">💡 교과서 필승 전략 정리</div>
    <div class="info-box">
      <b>[규칙 변형 예시] 두 수의 곱이 홀수/짝수인지 맞히기</b><br><br>
      ① 곱이 홀수: (홀×홀) → 3×3 = <span class="hl">9가지</span><br>
      ② 곱이 짝수: (홀×짝), (짝×홀), (짝×짝) → 3×2 + 2×3 + 2×2 = <span class="hl">16가지</span><br><br>
      ➡ <b>짝수를 말하면 16/25 ≈ 64% 확률로 승리!</b><br><br>
      <b>[기본 규칙] 합이 9일 때 경우의 수가 최대 (10가지)</b><br>
      합 표:
      <span class="hl">0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:5, 7:4, 8:3, 9:2, 10:1</span>이 아니라...<br>
      실제 계산: 합 7이 6가지, <b>합 5·6이 공동 최대(6가지)</b>, 합 9 도달시 확률 최대<br>
      → 아래 분석 탭에서 직접 확인해보세요!
    </div>

    <div style="margin-top:16px">
      <div class="card-title">🔢 전략별 기대 승률 요약표</div>
      <table id="stratTable">
        <thead>
          <tr><th>나의 전략 ↓ / AI ↵</th><th>🎲 무작위</th><th>📈 최빈 합</th><th>🔢 짝수</th><th>🔣 홀수</th><th>🎯 균등</th></tr>
        </thead>
        <tbody id="stratTableBody">
          <tr><td colspan="6" style="color:#475569;text-align:center">시뮬레이션을 실행하면 값이 채워집니다</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

</div><!-- /wrap -->

<script>
// ═══════════════════════════════════════════════════════════
//  전역 상태
// ═══════════════════════════════════════════════════════════
const HAND = ['✊','☝️','✌️','🤟','🖖','🖐'];
let gameMode = 2, difficulty = 'easy', goalScore = 3;
let scorePlayer = 0, scoreAI = 0, scoreDraw = 0, roundNum = 0;
let selFinger = -1, selGuess = -1;
// 전략 시뮬레이션
let myStrat = 'random', aiStrat = 'random';
// 전략 표 캐시
const stratCache = {};

// ═══════════════════════════════════════════════════════════
//  탭 전환
// ═══════════════════════════════════════════════════════════
function switchTab(name, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  if (btn) btn.classList.add('active');
  if (name === 'analysis') buildAnalysis();
}

// ═══════════════════════════════════════════════════════════
//  게임 설정
// ═══════════════════════════════════════════════════════════
function setMode(m) {
  gameMode = m;
  ['modeBtn2','modeBtn3'].forEach(id => document.getElementById(id).classList.remove('active'));
  document.getElementById('modeBtn' + m).classList.add('active');
  resetGame();
  buildPlayUI();
}
const DIFF_DESC = {
  easy:   '🎲 AI가 손가락과 예측 숫자를 <b style="color:#e2e8f0">완전 무작위</b>로 선택합니다. 이길 확률이 낮아 연습에 적합해요.',
  normal: '🧐 AI가 내 손가락을 <b style="color:#e2e8f0">어느 정도 읽고</b> 실제 합 ±2 범위에서 예측합니다. 눈치 싸움이 시작됩니다!',
  hard:   '🤖 AI가 <b style="color:#e2e8f0">70% 확률로 정확한 합</b>을 예측하고 경우의 수가 가장 많은 합도 노립니다. 이기기 매우 어렵습니다!'
};
function setDiff(d) {
  difficulty = d;
  ['diffEasy','diffNormal','diffHard'].forEach(id => document.getElementById(id).classList.remove('active'));
  document.getElementById('diff' + d.charAt(0).toUpperCase() + d.slice(1)).classList.add('active');
  document.getElementById('diffDesc').innerHTML = DIFF_DESC[d];
}
function setGoal(g) {
  goalScore = g;
  ['goal3','goal5','goal7'].forEach(id => document.getElementById(id).classList.remove('active'));
  document.getElementById('goal' + g).classList.add('active');
  resetGame();
}

// ═══════════════════════════════════════════════════════════
//  플레이 UI 빌드
// ═══════════════════════════════════════════════════════════
function buildPlayUI() {
  // 손가락 선택
  const fg = document.getElementById('myFingers');
  fg.innerHTML = '';
  for (let i = 0; i <= 5; i++) {
    const btn = document.createElement('div');
    btn.className = 'finger-btn' + (selFinger === i ? ' selected' : '');
    btn.innerHTML = HAND[i] + '<span class="finger-label">' + i + '</span>';
    btn.onclick = () => selectFinger(i);
    fg.appendChild(btn);
  }

  // 숫자 선택 (모드에 따라 최대값 변화)
  const maxSum = gameMode === 2 ? 10 : 15;
  const ng = document.getElementById('myGuess');
  ng.innerHTML = '';
  for (let i = 0; i <= maxSum; i++) {
    const btn = document.createElement('div');
    btn.className = 'num-btn' + (selGuess === i ? ' selected' : '');
    btn.textContent = i;
    btn.onclick = () => selectGuess(i);
    ng.appendChild(btn);
  }

  updatePlayBtn();
}

function selectFinger(i) {
  selFinger = i;
  buildPlayUI();
}
function selectGuess(i) {
  selGuess = i;
  buildPlayUI();
}
function updatePlayBtn() {
  document.getElementById('playBtn').disabled = (selFinger < 0 || selGuess < 0);
}

// ═══════════════════════════════════════════════════════════
//  AI 로직
// ═══════════════════════════════════════════════════════════
function aiChooseFinger(diff) {
  if (diff === 'easy') return Math.floor(Math.random() * 6);
  // 보통 이상: 0~5 랜덤하되 약간 편향
  if (diff === 'normal') return Math.floor(Math.random() * 6);
  // 어려움: 전략적 (3~4 선호)
  const pool = [0,1,2,2,3,3,3,4,4,4,5,5];
  return pool[Math.floor(Math.random() * pool.length)];
}

function aiChooseGuess(myFinger, aiFinger, diff, mode) {
  const maxSum = mode === 2 ? 10 : 15;
  if (diff === 'easy') {
    // 쉬움: 완전 무작위
    return Math.floor(Math.random() * (maxSum + 1));
  }
  if (diff === 'normal') {
    // 보통: 실제 합 ± 2 중 랜덤
    const realSum = myFinger + aiFinger;
    const pool = [];
    for (let d = -2; d <= 2; d++) {
      const v = realSum + d;
      if (v >= 0 && v <= maxSum) pool.push(v);
    }
    pool.push(Math.floor(Math.random() * (maxSum + 1))); // 노이즈
    return pool[Math.floor(Math.random() * pool.length)];
  }
  // 어려움: 높은 확률로 실제 합, 가끔 "최빈 합" 노림
  if (Math.random() < 0.7) return myFinger + aiFinger;
  // 경우의 수 최대 합 중 하나 선택
  const freq = computeFreq2();
  const maxF = Math.max(...freq);
  const candidates = freq.map((f,i) => f===maxF?i:-1).filter(x=>x>=0);
  return candidates[Math.floor(Math.random() * candidates.length)];
}

function computeFreq2() {
  const freq = new Array(11).fill(0);
  for (let a = 0; a <= 5; a++)
    for (let b = 0; b <= 5; b++)
      freq[a + b]++;
  return freq;
}

// ═══════════════════════════════════════════════════════════
//  라운드 진행
// ═══════════════════════════════════════════════════════════
function playRound() {
  if (selFinger < 0 || selGuess < 0) return;

  roundNum++;

  // AI 선택
  const aiFinger  = aiChooseFinger(difficulty);
  const aiGuess   = aiChooseGuess(selFinger, aiFinger, difficulty, gameMode);

  // 세 사람 모드: AI 2명
  let ai2Finger = -1, ai2Guess = -1;
  if (gameMode === 3) {
    ai2Finger = aiChooseFinger(difficulty);
    ai2Guess  = aiChooseGuess(selFinger, ai2Finger, difficulty, gameMode);
  }

  // 실제 합
  const realSum = gameMode === 2
    ? selFinger + aiFinger
    : selFinger + aiFinger + ai2Finger;

  const playerHit = (selGuess === realSum);
  const aiHit     = (aiGuess  === realSum);
  const ai2Hit    = gameMode === 3 && (ai2Guess === realSum);

  let outcome; // 'win' | 'lose' | 'draw'
  if (gameMode === 2) {
    if (playerHit && !aiHit)  outcome = 'win';
    else if (!playerHit && aiHit) outcome = 'lose';
    else outcome = 'draw';
  } else {
    const hits = [playerHit, aiHit, ai2Hit];
    const nHit = hits.filter(Boolean).length;
    if (playerHit && nHit === 1) outcome = 'win';
    else if (!playerHit && nHit >= 1) outcome = 'lose';
    else outcome = 'draw';
  }

  // 점수 업데이트
  if (outcome === 'win')  scorePlayer++;
  else if (outcome === 'lose') scoreAI++;
  else scoreDraw++;

  document.getElementById('scorePlayer').textContent = scorePlayer;
  document.getElementById('scoreAI').textContent     = scoreAI;
  document.getElementById('scoreDraw').textContent   = scoreDraw;
  document.getElementById('scoreRound').textContent  = roundNum;

  // 진행 바
  const pct = Math.round((Math.max(scorePlayer, scoreAI) / goalScore) * 100);
  document.getElementById('progressInner').style.width = Math.min(pct, 100) + '%';

  // 결과 표시
  const resultBox = document.getElementById('roundResult');
  resultBox.className = 'result-box';
  if (outcome === 'win') {
    resultBox.classList.add('result-win');
    resultBox.textContent = '🎉 이겼습니다! 정답!';
  } else if (outcome === 'lose') {
    resultBox.classList.add('result-lose');
    resultBox.textContent = '😢 졌습니다! AI가 맞혔어요.';
  } else {
    resultBox.classList.add('result-draw');
    if (playerHit && aiHit) resultBox.textContent = '🤝 둘 다 맞혔어요! 무승부';
    else resultBox.textContent = '🤝 둘 다 틀렸어요! 무승부';
  }

  // 상세
  const detailBox = document.getElementById('roundDetail');
  detailBox.style.display = 'block';
  let detailHTML = gameMode === 2
    ? `<b>나:</b> ${HAND[selFinger]}(${selFinger}개) 외침: <b>${selGuess}</b> &nbsp;|&nbsp;
       <b>AI:</b> ${HAND[aiFinger]}(${aiFinger}개) 외침: <b>${aiGuess}</b><br>
       <b>실제 합: ${realSum}</b> &nbsp;→&nbsp; ${playerHit?'✅ 내 정답':'❌ 내 오답'} / ${aiHit?'✅ AI 정답':'❌ AI 오답'}`
    : `<b>나:</b> ${HAND[selFinger]}(${selFinger}) 외침: ${selGuess} &nbsp;|&nbsp;
       <b>AI₁:</b> ${HAND[aiFinger]}(${aiFinger}) 외침: ${aiGuess} &nbsp;|&nbsp;
       <b>AI₂:</b> ${HAND[ai2Finger]}(${ai2Finger}) 외침: ${ai2Guess}<br>
       <b>실제 합: ${realSum}</b>`;
  document.getElementById('roundDetailBox').innerHTML = detailHTML;

  // 로그 추가
  addLog(outcome, roundNum, selFinger, aiFinger, selGuess, aiGuess, realSum);

  // 게임 승리 체크
  if (scorePlayer >= goalScore || scoreAI >= goalScore) announceWinner();

  // 선택 초기화
  selFinger = -1; selGuess = -1;
  buildPlayUI();
}

function addLog(outcome, round, pF, aF, pG, aG, sum) {
  const log = document.getElementById('gameLog');
  if (log.querySelector('div[style]')) log.innerHTML = '';
  const item = document.createElement('div');
  item.className = 'log-item log-' + outcome.charAt(0);
  const badge = outcome === 'win' ? '<span class="badge badge-w">WIN</span>'
              : outcome === 'lose' ? '<span class="badge badge-l">LOSE</span>'
              : '<span class="badge badge-d">DRAW</span>';
  item.innerHTML = badge +
    `<span style="color:#64748b">#${round}</span>` +
    `${HAND[pF]}<b style="color:#e2e8f0">${pG}</b> vs ${HAND[aF]}<b style="color:#e2e8f0">${aG}</b>` +
    `<span style="color:#94a3b8">합=${sum}</span>`;
  log.insertBefore(item, log.firstChild);
}

function announceWinner() {
  const who = scorePlayer >= goalScore ? '🎉 축하합니다! 당신이 이겼습니다!' : '😢 AI가 이겼습니다. 다시 도전!';
  const resultBox = document.getElementById('roundResult');
  resultBox.className = 'result-box ' + (scorePlayer >= goalScore ? 'result-win' : 'result-lose');
  resultBox.textContent = who + '  최종: 나 ' + scorePlayer + ' : AI ' + scoreAI;
  document.getElementById('playBtn').disabled = true;
}

function resetGame() {
  scorePlayer = scoreAI = scoreDraw = roundNum = 0;
  selFinger = selGuess = -1;
  document.getElementById('scorePlayer').textContent = '0';
  document.getElementById('scoreAI').textContent = '0';
  document.getElementById('scoreDraw').textContent = '0';
  document.getElementById('scoreRound').textContent = '0';
  document.getElementById('progressInner').style.width = '0%';
  document.getElementById('roundResult').className = 'result-box result-none';
  document.getElementById('roundResult').textContent = '손가락과 숫자를 선택한 뒤 "내기!" 버튼을 누르세요.';
  document.getElementById('roundDetail').style.display = 'none';
  document.getElementById('gameLog').innerHTML = '<div style="color:#475569;font-size:13px;text-align:center;padding:20px">게임을 시작하면 기록이 쌓입니다.</div>';
  buildPlayUI();
}

// ═══════════════════════════════════════════════════════════
//  경우의 수 분석
// ═══════════════════════════════════════════════════════════
let analysisBuilt = false;
function buildAnalysis() {
  if (analysisBuilt) return;
  analysisBuilt = true;

  // ── 2인 분석 ──
  const freq2 = computeFreq2();
  const maxF2 = Math.max(...freq2);

  // 막대 차트 2인 (픽셀 높이 3행 구조)
  const bc2 = document.getElementById('barChart');
  const BAR_H2 = 90;
  let cRow2 = '<div style="display:flex;gap:4px;margin-bottom:3px">';
  let bRow2 = `<div style="display:flex;align-items:flex-end;gap:4px;height:${BAR_H2}px;border-bottom:1px solid rgba(255,255,255,.08)">`;
  let sRow2 = '<div style="display:flex;gap:4px;margin-top:3px">';
  freq2.forEach((f, s) => {
    const px = Math.max(2, Math.round((f / maxF2) * BAR_H2));
    const isMax = f === maxF2;
    const col = isMax ? 'linear-gradient(180deg,#10b981,#059669)' : 'linear-gradient(180deg,#6366f1,#4f46e5)';
    const shadow = isMax ? '0 0 10px rgba(16,185,129,.5)' : 'none';
    cRow2 += `<div style="flex:1;text-align:center;font-size:11px;font-weight:700;color:${isMax?'#6ee7b7':'#a5b4fc'}">${f}</div>`;
    bRow2 += `<div style="flex:1;min-width:0;height:${px}px;background:${col};border-radius:4px 4px 0 0;
      cursor:pointer;box-shadow:${shadow};transition:.25s" onclick="showCases2(${s})"
      onmouseover="this.style.opacity='.8'" onmouseout="this.style.opacity='1'"></div>`;
    sRow2 += `<div style="flex:1;text-align:center;font-size:11px;font-weight:600;color:#94a3b8;
      cursor:pointer" onclick="showCases2(${s})">${s}</div>`;
  });
  bc2.innerHTML = cRow2+'</div>' + bRow2+'</div>' + sRow2+'</div>'
    + '<div style="text-align:center;font-size:11px;color:#475569;margin-top:6px">합 (막대 또는 숫자 클릭 → 경우 목록)</div>';

  // 버튼 그리드 2인
  const an2 = document.getElementById('analysisNums');
  an2.innerHTML = '';
  freq2.forEach((f, s) => {
    const btn = document.createElement('div');
    btn.className = 'num-btn';
    btn.textContent = s;
    btn.title = f + '가지';
    btn.onclick = () => showCases2(s);
    an2.appendChild(btn);
  });

  // ── 3인 분석 ──
  const freq3 = new Array(16).fill(0);
  const cases3 = Array.from({length:16}, () => []);
  for (let a = 0; a <= 5; a++)
    for (let b = 0; b <= 5; b++)
      for (let c = 0; c <= 5; c++) {
        freq3[a+b+c]++;
        cases3[a+b+c].push([a,b,c]);
      }
  window._freq3 = freq3;
  window._cases3 = cases3;

  const maxF3 = Math.max(...freq3);
  const bc3 = document.getElementById('barChart3');
  const BAR_H3 = 90;
  let cRow3 = '<div style="display:flex;gap:3px;margin-bottom:3px">';
  let bRow3 = `<div style="display:flex;align-items:flex-end;gap:3px;height:${BAR_H3}px;border-bottom:1px solid rgba(255,255,255,.08)">`;
  let sRow3 = '<div style="display:flex;gap:3px;margin-top:3px">';
  freq3.forEach((f, s) => {
    if (f === 0) {
      cRow3 += '<div style="flex:1"></div>';
      bRow3 += '<div style="flex:1"></div>';
      sRow3 += `<div style="flex:1;text-align:center;font-size:10px;color:#334155">${s}</div>`;
      return;
    }
    const px = Math.max(2, Math.round((f / maxF3) * BAR_H3));
    const isMax = f === maxF3;
    const col = isMax ? 'linear-gradient(180deg,#f59e0b,#d97706)' : 'linear-gradient(180deg,#6366f1,#4f46e5)';
    const shadow = isMax ? '0 0 10px rgba(245,158,11,.5)' : 'none';
    cRow3 += `<div style="flex:1;text-align:center;font-size:10px;font-weight:700;color:${isMax?'#fbbf24':'#a5b4fc'}">${f}</div>`;
    bRow3 += `<div style="flex:1;min-width:0;height:${px}px;background:${col};border-radius:4px 4px 0 0;
      cursor:pointer;box-shadow:${shadow};transition:.25s" onclick="showCases3(${s})"
      onmouseover="this.style.opacity='.8'" onmouseout="this.style.opacity='1'"></div>`;
    sRow3 += `<div style="flex:1;text-align:center;font-size:10px;font-weight:600;color:#94a3b8;
      cursor:pointer" onclick="showCases3(${s})">${s}</div>`;
  });
  bc3.innerHTML = cRow3+'</div>' + bRow3+'</div>' + sRow3+'</div>'
    + '<div style="text-align:center;font-size:11px;color:#475569;margin-top:6px">합 (막대 또는 숫자 클릭 → 경우 목록)</div>';

  const an3 = document.getElementById('analysisNums3');
  an3.innerHTML = '';
  freq3.forEach((f, s) => {
    if (f === 0) return;
    const btn = document.createElement('div');
    btn.className = 'num-btn';
    btn.textContent = s;
    btn.title = f + '가지';
    btn.onclick = () => showCases3(s);
    an3.appendChild(btn);
  });
}

function showCases2(s) {
  const cases = [];
  for (let a = 0; a <= 5; a++)
    for (let b = 0; b <= 5; b++)
      if (a + b === s) cases.push([a, b]);

  const cl = document.getElementById('caseList');
  cl.style.display = 'block';
  document.getElementById('caseListTitle').textContent =
    `합 = ${s} 인 경우: 총 ${cases.length}가지`;
  const cc = document.getElementById('caseListContent');
  cc.innerHTML = cases.map(([a,b]) =>
    `<div style="background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);
      border-radius:10px;padding:8px 14px;font-size:18px;text-align:center;min-width:80px">
      ${HAND[a]}+${HAND[b]}<br>
      <span style="font-size:12px;color:#94a3b8;font-family:monospace">(${a}+${b}=${s})</span>
    </div>`
  ).join('');
}

function showCases3(s) {
  const cases = window._cases3[s] || [];
  const cl = document.getElementById('caseList3');
  cl.style.display = 'block';
  document.getElementById('caseList3Title').textContent =
    `합 = ${s} 인 경우: 총 ${cases.length}가지`;
  const cc = document.getElementById('caseList3Content');
  cc.innerHTML = cases.slice(0, 60).map(([a,b,c]) =>
    `<div style="background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.2);
      border-radius:10px;padding:6px 10px;font-size:16px;text-align:center;min-width:90px">
      ${HAND[a]}${HAND[b]}${HAND[c]}<br>
      <span style="font-size:11px;color:#94a3b8;font-family:monospace">(${a},${b},${c})</span>
    </div>`
  ).join('') + (cases.length > 60 ? `<div style="color:#64748b;font-size:12px;align-self:center">… +${cases.length-60}가지 더</div>` : '');
}

// ═══════════════════════════════════════════════════════════
//  전략 시뮬레이션
// ═══════════════════════════════════════════════════════════
function setMyStrat(s) {
  myStrat = s;
  document.querySelectorAll('#myStratBtns .tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('s_my_' + s).classList.add('active');
}
function setAIStrat(s) {
  aiStrat = s;
  document.querySelectorAll('#aiStratBtns .tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('s_ai_' + s).classList.add('active');
}

const STRATEGIES = ['random','max','even','odd','mixed'];
const STRAT_LABEL = {random:'🎲무작위',max:'📈최빈합',even:'🔢짝수',odd:'🔣홀수',mixed:'🎯균등'};

function stratPick(strat) {
  // 손가락: 0~5 무작위 (모든 전략 공통)
  const f = Math.floor(Math.random() * 6);
  let g;
  if (strat === 'random') {
    g = Math.floor(Math.random() * 11);
  } else if (strat === 'max') {
    // 경우의 수 최대 합들 중 하나 (5,6,7 모두 6가지)
    const maxSums = [5,6,7];
    g = maxSums[Math.floor(Math.random() * maxSums.length)];
  } else if (strat === 'even') {
    const evens = [0,2,4,6,8,10];
    g = evens[Math.floor(Math.random() * evens.length)];
  } else if (strat === 'odd') {
    const odds = [1,3,5,7,9];
    g = odds[Math.floor(Math.random() * odds.length)];
  } else { // mixed
    const pool = [5,5,6,6,7,7,8,9];
    g = pool[Math.floor(Math.random() * pool.length)];
  }
  return {f, g};
}

function oneRound(sA, sB) {
  const A = stratPick(sA);
  const B = stratPick(sB);
  const sum = A.f + B.f;
  const aHit = A.g === sum;
  const bHit = B.g === sum;
  if (aHit && !bHit) return 'win';
  if (!aHit && bHit) return 'lose';
  return 'draw';
}

function runSimulation() {
  const N = 1000;
  let w = 0, l = 0, d = 0;
  for (let i = 0; i < N; i++) {
    const r = oneRound(myStrat, aiStrat);
    if (r === 'win') w++;
    else if (r === 'lose') l++;
    else d++;
  }
  document.getElementById('simResult').style.display = 'block';
  document.getElementById('simWin').textContent  = w;
  document.getElementById('simLose').textContent = l;
  document.getElementById('simDraw').textContent = d;

  const total = w + l + d;
  const wP = (w/total*100).toFixed(1), lP = (l/total*100).toFixed(1), dP = (d/total*100).toFixed(1);
  document.getElementById('simBar').innerHTML =
    `<div style="flex:${w};background:#10b981;border-radius:6px 0 0 6px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;min-width:2px">${wP>5?wP+'%':''}</div>` +
    `<div style="flex:${d};background:#6366f1;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;min-width:2px">${dP>5?dP+'%':''}</div>` +
    `<div style="flex:${l};background:#ef4444;border-radius:0 6px 6px 0;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;min-width:2px">${lP>5?lP+'%':''}</div>`;

  const winRate = (w / (w+l) * 100).toFixed(1);
  const analysis = w > l
    ? `<b>내 전략(${STRAT_LABEL[myStrat]})</b>이 AI의 전략(${STRAT_LABEL[aiStrat]})을 이겼습니다! 승률(무승부 제외) <b>${winRate}%</b>`
    : w < l
    ? `AI의 전략(${STRAT_LABEL[aiStrat]})이 더 강합니다. 다른 전략을 시도해보세요. 내 승률 <b>${winRate}%</b>`
    : `두 전략의 승률이 비슷합니다 (${winRate}%).`;
  document.getElementById('simAnalysis').innerHTML = analysis;

  // 캐시에 저장 & 표 업데이트
  if (!stratCache[myStrat]) stratCache[myStrat] = {};
  stratCache[myStrat][aiStrat] = winRate;
  updateStratTable();
}

function updateStratTable() {
  const tbody = document.getElementById('stratTableBody');
  let html = '';
  STRATEGIES.forEach(ms => {
    html += `<tr><td style="text-align:left;font-weight:700;color:#e2e8f0">${STRAT_LABEL[ms]}</td>`;
    STRATEGIES.forEach(as => {
      const v = stratCache[ms] && stratCache[ms][as] !== undefined ? stratCache[ms][as] + '%' : '—';
      const pct = parseFloat(v);
      const cls = !isNaN(pct) ? (pct > 55 ? 'td-max' : pct < 45 ? 'td-min' : '') : '';
      html += `<td class="${cls}">${v}</td>`;
    });
    html += '</tr>';
  });
  tbody.innerHTML = html;
}

// ═══════════════════════════════════════════════════════════
//  초기화
// ═══════════════════════════════════════════════════════════
window.onload = () => {
  buildPlayUI();
};
</script>
</body>
</html>"""

# ──────────────────────────────────────────────────────────────────────────────
def render():
    st.header("✊ 손가락 게임 '모라'와 같은 것이 있는 순열")
    st.markdown("""
고대 로마부터 이탈리아 사람들이 즐겨온 손가락 게임 **'모라(Morra)'** 를 직접 플레이해 보고,
**같은 것이 있는 순열**로 경우의 수를 분석하며 필승 전략을 수학적으로 탐구해 봅시다!
""")

    components.html(_HTML, height=1500, scrolling=True)

    # ── 성찰 기록 폼 ───────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
