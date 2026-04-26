import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "솔직한설문의비밀"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 무작위 응답 기법 – 성찰 질문**"},
    {
        "key": "독립시행이유",
        "label": "동전 던지기와 민감한 질문에 대한 응답은 서로 독립인가요? 독립인 이유를 설명해 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "조사자모름이유",
        "label": "조사자는 왜 개인의 실제 응답을 알 수 없을까요? 이 방법이 응답자의 익명성을 보장하는 원리를 설명해 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "확률계산",
        "label": "학생 200명 조사에서 120명이 '예'라고 답했다면, 실제로 민감한 경험을 한 학생은 몇 명으로 추정되나요? 풀이도 함께 써보세요.",
        "type": "text_area",
        "height": 100,
    },
    {
        "key": "한계와개선",
        "label": "이 방법의 한계나 개선할 수 있는 점이 있다면 무엇인지 생각해 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title":       "🎲 솔직한 설문의 비밀 – 무작위 응답 기법",
    "description": "동전 던지기 무작위성으로 민감한 설문에서도 솔직한 답변을 얻는 통계 기법을 체험합니다.",
    "order":       999999,
    "hidden":      True,
}

_HTML = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);min-height:100vh;padding:16px 14px 32px;color:#e2e8f0}

/* ── cards ── */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:20px 22px;margin:14px 0;backdrop-filter:blur(10px)}
.card-title{font-size:16px;font-weight:800;margin-bottom:14px;display:flex;align-items:center;gap:8px;letter-spacing:.02em}

/* ── section title ── */
.section-label{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#64748b;margin-bottom:8px}

/* ── problem scene ── */
.scene{display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;padding:10px 0}
.person{text-align:center}
.avatar{font-size:56px;line-height:1}
.bubble{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:10px 16px;font-size:13px;color:#cbd5e1;max-width:200px;margin-top:8px;position:relative}
.bubble::after{content:'';position:absolute;top:-10px;left:50%;transform:translateX(-50%);border:5px solid transparent;border-bottom-color:rgba(255,255,255,.15)}
.arrow-big{font-size:40px;color:#475569}
.problem-q{background:rgba(239,68,68,.1);border:2px solid rgba(239,68,68,.4);border-radius:16px;padding:14px 20px;text-align:center;max-width:280px}
.problem-q .q-emoji{font-size:36px}
.problem-q .q-text{font-size:13px;color:#fca5a5;margin-top:6px;font-weight:600}
.problem-q .q-worry{font-size:12px;color:#f87171;margin-top:4px;opacity:.8}

/* ── method steps ── */
.method-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:4px}
@media(max-width:520px){.method-grid{grid-template-columns:1fr}}
.method-card{border-radius:16px;padding:16px;text-align:center}
.method-card.q1{background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.35)}
.method-card.q2{background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.35)}
.method-card .mc-icon{font-size:40px;margin-bottom:8px}
.method-card .mc-title{font-weight:800;font-size:14px;margin-bottom:6px}
.method-card.q1 .mc-title{color:#fbbf24}
.method-card.q2 .mc-title{color:#a5b4fc}
.method-card .mc-desc{font-size:13px;color:#94a3b8;line-height:1.6}
.coin-bridge{display:flex;align-items:center;justify-content:center;gap:8px;margin:12px 0;font-size:13px;color:#64748b}
.coin-bridge .cb-coin{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:50%;width:52px;height:52px;display:flex;align-items:center;justify-content:center;font-size:26px}
.cb-arr{font-size:20px;color:#475569}
.cb-item{text-align:center;font-size:12px;color:#94a3b8}
.cb-item span{display:block;font-weight:700;color:#e2e8f0}

/* ── coin flip simulator ── */
.coin-area{text-align:center;padding:10px 0 4px}
.coin{width:110px;height:110px;border-radius:50%;margin:0 auto 12px;display:flex;align-items:center;justify-content:center;font-size:52px;cursor:pointer;user-select:none;position:relative;transition:transform .08s;box-shadow:0 4px 24px rgba(0,0,0,.5)}
.coin.heads{background:linear-gradient(135deg,#fbbf24,#f59e0b);border:4px solid #d97706}
.coin.tails{background:linear-gradient(135deg,#94a3b8,#64748b);border:4px solid #475569}
.coin.spinning{animation:coinSpin .6s linear infinite}
@keyframes coinSpin{
  0%{transform:rotateY(0deg) scale(1)}
  25%{transform:rotateY(90deg) scale(0.7)}
  50%{transform:rotateY(180deg) scale(1)}
  75%{transform:rotateY(270deg) scale(0.7)}
  100%{transform:rotateY(360deg) scale(1)}
}
.coin:hover{transform:scale(1.05)}
.coin-result{min-height:56px;margin-top:6px}
.result-banner{border-radius:14px;padding:12px 20px;font-size:14px;font-weight:700;text-align:center;animation:fadeIn .4s}
@keyframes fadeIn{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
.result-banner.heads-res{background:rgba(245,158,11,.15);border:1px solid rgba(245,158,11,.4);color:#fbbf24}
.result-banner.tails-res{background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.4);color:#a5b4fc}
.flip-btn{background:linear-gradient(135deg,#6366f1,#8b5cf6);border:none;border-radius:12px;color:#fff;font-size:15px;font-weight:700;padding:10px 32px;cursor:pointer;transition:.2s;box-shadow:0 2px 14px rgba(99,102,241,.4);margin-top:4px}
.flip-btn:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(99,102,241,.5)}
.flip-btn:active{transform:scale(.97)}

/* ── case tabs ── */
.case-tabs{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:16px}
.case-tab{padding:8px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);cursor:pointer;font-size:12px;font-weight:700;color:#64748b;transition:.2s;white-space:nowrap}
.case-tab:hover{color:#94a3b8;background:rgba(255,255,255,.07)}
.case-tab.active{background:rgba(99,102,241,.2);color:#a5b4fc;border-color:rgba(99,102,241,.4)}
.case-pane{display:none}.case-pane.active{display:block}

/* ── case cards ── */
.case-header{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.case-emoji{font-size:44px}
.case-info .ci-q{font-size:15px;font-weight:800;color:#e2e8f0}
.case-info .ci-sub{font-size:12px;color:#64748b;margin-top:3px}
.survey-box{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:14px 18px;margin:12px 0}
.survey-q{font-size:14px;color:#fbbf24;font-weight:700;margin-bottom:6px}
.procedure-list{list-style:none;display:flex;flex-direction:column;gap:7px}
.procedure-list li{display:flex;align-items:flex-start;gap:10px;font-size:13px;color:#cbd5e1}
.proc-num{background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:50%;width:22px;height:22px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;margin-top:1px}
.q-pills{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.q-pill{border-radius:12px;padding:8px 14px;font-size:13px;font-weight:700}
.q-pill.p1{background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.3);color:#fbbf24}
.q-pill.p2{background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.3);color:#a5b4fc}

/* ── estimation calculator ── */
.calc-wrap{background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.25);border-radius:16px;padding:16px 20px;margin-top:12px}
.calc-title{font-size:13px;font-weight:800;color:#34d399;margin-bottom:12px}
.calc-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.calc-label{font-size:12px;color:#94a3b8;font-weight:600;min-width:90px}
input[type=range]{-webkit-appearance:none;height:6px;border-radius:3px;background:linear-gradient(90deg,#10b981,#059669);outline:none;width:160px;cursor:pointer;flex-shrink:0}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#fff;border:3px solid #10b981;cursor:pointer;box-shadow:0 0 8px rgba(16,185,129,.5)}
.vbadge{display:inline-block;min-width:40px;background:linear-gradient(135deg,#10b981,#059669);border-radius:8px;padding:2px 8px;font-weight:800;font-size:14px;text-align:center;color:#fff;box-shadow:0 1px 8px rgba(16,185,129,.4)}
.formula-display{background:rgba(255,255,255,.04);border-radius:12px;padding:12px 16px;margin:10px 0;font-size:13px;color:#94a3b8;line-height:1.8}
.formula-display .fv{color:#34d399;font-weight:800;font-size:15px}
.formula-display .fv2{color:#fbbf24;font-weight:800}
.answer-box{background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.4);border-radius:12px;padding:12px 18px;text-align:center;margin-top:8px}
.answer-box .ans-label{font-size:12px;color:#6ee7b7;font-weight:600;margin-bottom:4px}
.answer-box .ans-val{font-size:28px;font-weight:900;color:#10b981}
.answer-box .ans-sub{font-size:12px;color:#6ee7b7;margin-top:3px}

/* ── formula explainer ── */
.formula-big{background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.25);border-radius:16px;padding:16px 20px;margin:12px 0}
.fb-title{font-size:12px;color:#818cf8;font-weight:800;letter-spacing:.05em;margin-bottom:10px}
.fb-expr{font-size:15px;color:#c7d2fe;font-family:monospace;line-height:2;word-break:break-all}
.fb-parts{display:flex;flex-direction:column;gap:6px;margin-top:10px}
.fb-part{display:flex;align-items:flex-start;gap:10px;font-size:13px;color:#cbd5e1}
.fb-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;margin-top:5px}
.dot-b{background:#fbbf24}.dot-a{background:#a5b4fc}.dot-bc{background:#34d399}.dot-res{background:#f472b6}

/* ── progress bar ── */
.pbar-wrap{background:rgba(255,255,255,.06);border-radius:8px;height:20px;overflow:hidden;margin:6px 0}
.pbar-fill{height:100%;border-radius:8px;transition:width .5s;display:flex;align-items:center;justify-content:flex-end;padding-right:8px;font-size:11px;font-weight:700;color:#fff;min-width:0}
.pbar-fill.yes-bar{background:linear-gradient(90deg,#10b981,#059669)}
.pbar-fill.real-bar{background:linear-gradient(90deg,#f59e0b,#d97706)}

/* ── sim counters ── */
.sim-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}
.sim-kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:10px;text-align:center}
.sim-kpi .sk-num{font-size:26px;font-weight:900}
.sim-kpi .sk-lbl{font-size:11px;color:#64748b;margin-top:2px;font-weight:600}
.sim-kpi.kpi-total .sk-num{color:#e2e8f0}
.sim-kpi.kpi-yes .sk-num{color:#34d399}
.sim-kpi.kpi-est .sk-num{color:#fbbf24}
.sim-log{max-height:160px;overflow-y:auto;display:flex;flex-direction:column;gap:4px;margin-top:8px}
.log-item{display:flex;align-items:center;gap:8px;font-size:12px;padding:5px 10px;border-radius:8px;animation:fadeIn .25s}
.log-item.li-yes{background:rgba(16,185,129,.08);border-left:3px solid #10b981;color:#6ee7b7}
.log-item.li-no{background:rgba(99,102,241,.08);border-left:3px solid #6366f1;color:#a5b4fc}
.sim-btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.sim-btn{border:none;border-radius:10px;font-size:13px;font-weight:700;padding:9px 18px;cursor:pointer;transition:.2s}
.sim-btn.primary{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;box-shadow:0 2px 12px rgba(99,102,241,.4)}
.sim-btn.primary:hover{transform:translateY(-2px)}
.sim-btn.secondary{background:rgba(255,255,255,.06);color:#94a3b8;border:1px solid rgba(255,255,255,.1)}
.sim-btn.secondary:hover{background:rgba(255,255,255,.1)}
.sim-btn.fast{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;box-shadow:0 2px 10px rgba(245,158,11,.4)}
.sim-btn.fast:hover{transform:translateY(-2px)}

::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(99,102,241,.4);border-radius:3px}
</style>
</head>
<body>

<!-- ════════════════════════════════════════════════
  SECTION 1 : 문제 상황
════════════════════════════════════════════════ -->
<div class="card">
  <div class="card-title" style="color:#f87171">🤔 민감한 질문, 솔직하게 답할 수 있을까?</div>
  <div class="scene">
    <div class="person">
      <div class="avatar">👧</div>
      <div class="bubble" style="border-color:rgba(239,68,68,.4)">
        "솔직히 말하면 창피할 것 같은데…"
      </div>
    </div>
    <div class="arrow-big">←</div>
    <div class="problem-q">
      <div class="q-emoji">📋</div>
      <div class="q-text">설문지</div>
      <div class="q-worry" style="font-size:14px;color:#fca5a5;margin-top:8px">"학교에서 분리배출을<br>하지 않은 경험이 있나요?"</div>
    </div>
    <div class="arrow-big">→</div>
    <div class="person">
      <div class="avatar">👦</div>
      <div class="bubble" style="border-color:rgba(239,68,68,.4)">
        "다들 보는데… 그냥 '아니요' 라고 쓸게요"
      </div>
    </div>
  </div>
  <div style="margin-top:14px;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.25);border-radius:12px;padding:12px 16px;font-size:13px;color:#fca5a5;text-align:center">
    😰 민감한 주제일수록 솔직한 답변을 얻기 어렵다!<br>
    <span style="color:#f87171;font-weight:700">→ 거짓 응답 → 통계 왜곡 → 잘못된 결론</span>
  </div>
</div>

<!-- ════════════════════════════════════════════════
  SECTION 2 : 해결 방법 – 무작위 응답 기법
════════════════════════════════════════════════ -->
<div class="card">
  <div class="card-title" style="color:#34d399">🎲 해결책: 동전 던지기를 활용하자!</div>
  <p style="font-size:13px;color:#94a3b8;margin-bottom:14px">
    조사자가 모르게 응답자가 몰래 동전 1개를 던집니다.
  </p>

  <div class="coin-bridge">
    <div class="cb-item"><div class="cb-coin">🪙</div><span>동전 던지기</span></div>
    <div class="cb-arr">→</div>
    <div class="cb-item"><div class="cb-coin">☀️</div><span style="color:#fbbf24">앞면</span></div>
    <div class="cb-arr">→</div>
    <div class="cb-item" style="color:#fbbf24"><span>설문지 1</span>무조건 '예'</div>
    <div style="font-size:24px;color:#475569;padding:0 4px">|</div>
    <div class="cb-item"><div class="cb-coin">🌙</div><span style="color:#a5b4fc">뒷면</span></div>
    <div class="cb-arr">→</div>
    <div class="cb-item" style="color:#a5b4fc"><span>설문지 2</span>솔직하게 응답</div>
  </div>

  <div class="method-grid" style="margin-top:14px">
    <div class="method-card q1">
      <div class="mc-icon">☀️</div>
      <div class="mc-title">앞면 → 설문지 1</div>
      <div class="mc-desc">"무조건 <strong style="color:#fbbf24">'예'</strong>라고 답하세요."<br><br>실제 경험과 무관하게 예라고 답함</div>
    </div>
    <div class="method-card q2">
      <div class="mc-icon">🌙</div>
      <div class="mc-title">뒷면 → 설문지 2</div>
      <div class="mc-desc">실제 민감한 질문에 솔직하게 <strong style="color:#a5b4fc">예/아니요</strong>로 답함<br><br>조사자는 동전 결과를 모름!</div>
    </div>
  </div>

  <div style="margin-top:14px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.25);border-radius:12px;padding:12px 16px;font-size:13px;color:#6ee7b7;text-align:center">
    💡 조사자는 응답자가 어느 설문지를 뽑았는지 <strong style="color:#34d399">알 수 없다!</strong><br>
    → 개인의 솔직한 답이 보호되면서도, 전체 통계로 진실을 추정할 수 있다
  </div>
</div>

<!-- ════════════════════════════════════════════════
  SECTION 3 : 직접 체험 시뮬레이터
════════════════════════════════════════════════ -->
<div class="card">
  <div class="card-title" style="color:#a5b4fc">🎮 내가 응답자라면? 직접 체험해보자!</div>
  <p style="font-size:12px;color:#64748b;margin-bottom:4px">
    아래 동전을 클릭해서 던져보세요. 어느 설문지를 뽑았는지 확인하세요.
  </p>

  <div class="coin-area">
    <div class="coin heads" id="flipCoin" onclick="flipCoin()" title="클릭해서 던지기!">🪙</div>
    <button class="flip-btn" onclick="flipCoin()">🎲 동전 던지기!</button>
    <div class="coin-result" id="coinResult"></div>
  </div>
</div>

<!-- ════════════════════════════════════════════════
  SECTION 4 : 사례 탐구 (4가지)
════════════════════════════════════════════════ -->
<div class="card">
  <div class="card-title" style="color:#fbbf24">📊 사례로 알아보는 무작위 응답 기법</div>

  <div class="case-tabs">
    <button class="case-tab active" onclick="showCase(0)">🗑 분리배출</button>
    <button class="case-tab" onclick="showCase(1)">📱 수업 중 핸드폰</button>
    <button class="case-tab" onclick="showCase(2)">🍱 급식 남기기</button>
    <button class="case-tab" onclick="showCase(3)">😴 전날 공부 안 함</button>
  </div>

  <!-- Case 0: 분리배출 -->
  <div class="case-pane active" id="case-0">
    <div class="case-header">
      <div class="case-emoji">🗑️</div>
      <div class="case-info">
        <div class="ci-q">학교에서 분리배출을 하지 않은 경험이 있나요?</div>
        <div class="ci-sub">학생 100명 대상 설문 | 동전 앞면 확률 = 1/2</div>
      </div>
    </div>
    <div class="survey-box">
      <div class="survey-q">🪙 동전 던지기 결과에 따라 설문지를 선택</div>
      <div class="q-pills">
        <div class="q-pill p1">☀️ 앞면 → 설문지 1: 무조건 '예'</div>
        <div class="q-pill p2">🌙 뒷면 → 설문지 2: 솔직하게 예/아니요</div>
      </div>
    </div>
    <div class="calc-wrap">
      <div class="calc-title">📐 역추정 계산기</div>
      <div class="calc-row">
        <div class="calc-label">전체 응답자 수</div>
        <input type="range" id="s0-n" min="50" max="300" value="100" step="10" oninput="calcCase(0)">
        <span class="vbadge" id="s0-n-v">100</span>명
      </div>
      <div class="calc-row">
        <div class="calc-label">'예' 응답 수</div>
        <input type="range" id="s0-yes" min="10" max="290" value="70" step="1" oninput="calcCase(0)">
        <span class="vbadge" id="s0-yes-v" style="background:linear-gradient(135deg,#10b981,#059669)">70</span>명
      </div>
      <div class="formula-display" id="s0-formula"></div>
      <div class="answer-box" id="s0-answer"></div>
    </div>
  </div>

  <!-- Case 1: 수업 중 핸드폰 -->
  <div class="case-pane" id="case-1">
    <div class="case-header">
      <div class="case-emoji">📱</div>
      <div class="case-info">
        <div class="ci-q">수업 시간에 몰래 핸드폰을 사용한 경험이 있나요?</div>
        <div class="ci-sub">학생 120명 대상 설문 | 동전 앞면 확률 = 1/2</div>
      </div>
    </div>
    <div class="survey-box">
      <div class="survey-q">🪙 동전 던지기 결과에 따라 설문지를 선택</div>
      <div class="q-pills">
        <div class="q-pill p1">☀️ 앞면 → 설문지 1: 무조건 '예'</div>
        <div class="q-pill p2">🌙 뒷면 → 설문지 2: 솔직하게 예/아니요</div>
      </div>
    </div>
    <div class="calc-wrap">
      <div class="calc-title">📐 역추정 계산기</div>
      <div class="calc-row">
        <div class="calc-label">전체 응답자 수</div>
        <input type="range" id="s1-n" min="50" max="300" value="120" step="10" oninput="calcCase(1)">
        <span class="vbadge" id="s1-n-v">120</span>명
      </div>
      <div class="calc-row">
        <div class="calc-label">'예' 응답 수</div>
        <input type="range" id="s1-yes" min="10" max="290" value="84" step="1" oninput="calcCase(1)">
        <span class="vbadge" id="s1-yes-v" style="background:linear-gradient(135deg,#10b981,#059669)">84</span>명
      </div>
      <div class="formula-display" id="s1-formula"></div>
      <div class="answer-box" id="s1-answer"></div>
    </div>
  </div>

  <!-- Case 2: 급식 남기기 -->
  <div class="case-pane" id="case-2">
    <div class="case-header">
      <div class="case-emoji">🍱</div>
      <div class="case-info">
        <div class="ci-q">급식 음식을 몰래 버린 경험이 있나요?</div>
        <div class="ci-sub">학생 80명 대상 설문 | 동전 앞면 확률 = 1/2</div>
      </div>
    </div>
    <div class="survey-box">
      <div class="survey-q">🪙 동전 던지기 결과에 따라 설문지를 선택</div>
      <div class="q-pills">
        <div class="q-pill p1">☀️ 앞면 → 설문지 1: 무조건 '예'</div>
        <div class="q-pill p2">🌙 뒷면 → 설문지 2: 솔직하게 예/아니요</div>
      </div>
    </div>
    <div class="calc-wrap">
      <div class="calc-title">📐 역추정 계산기</div>
      <div class="calc-row">
        <div class="calc-label">전체 응답자 수</div>
        <input type="range" id="s2-n" min="50" max="300" value="80" step="10" oninput="calcCase(2)">
        <span class="vbadge" id="s2-n-v">80</span>명
      </div>
      <div class="calc-row">
        <div class="calc-label">'예' 응답 수</div>
        <input type="range" id="s2-yes" min="10" max="290" value="52" step="1" oninput="calcCase(2)">
        <span class="vbadge" id="s2-yes-v" style="background:linear-gradient(135deg,#10b981,#059669)">52</span>명
      </div>
      <div class="formula-display" id="s2-formula"></div>
      <div class="answer-box" id="s2-answer"></div>
    </div>
  </div>

  <!-- Case 3: 전날 공부 안 함 -->
  <div class="case-pane" id="case-3">
    <div class="case-header">
      <div class="case-emoji">😴</div>
      <div class="case-info">
        <div class="ci-q">시험 전날 공부를 전혀 하지 않은 경험이 있나요?</div>
        <div class="ci-sub">학생 150명 대상 설문 | 동전 앞면 확률 = 1/2</div>
      </div>
    </div>
    <div class="survey-box">
      <div class="survey-q">🪙 동전 던지기 결과에 따라 설문지를 선택</div>
      <div class="q-pills">
        <div class="q-pill p1">☀️ 앞면 → 설문지 1: 무조건 '예'</div>
        <div class="q-pill p2">🌙 뒷면 → 설문지 2: 솔직하게 예/아니요</div>
      </div>
    </div>
    <div class="calc-wrap">
      <div class="calc-title">📐 역추정 계산기</div>
      <div class="calc-row">
        <div class="calc-label">전체 응답자 수</div>
        <input type="range" id="s3-n" min="50" max="300" value="150" step="10" oninput="calcCase(3)">
        <span class="vbadge" id="s3-n-v">150</span>명
      </div>
      <div class="calc-row">
        <div class="calc-label">'예' 응답 수</div>
        <input type="range" id="s3-yes" min="10" max="290" value="105" step="1" oninput="calcCase(3)">
        <span class="vbadge" id="s3-yes-v" style="background:linear-gradient(135deg,#10b981,#059669)">105</span>명
      </div>
      <div class="formula-display" id="s3-formula"></div>
      <div class="answer-box" id="s3-answer"></div>
    </div>
  </div>
</div>

<!-- ════════════════════════════════════════════════
  SECTION 5 : 수식 설명
════════════════════════════════════════════════ -->
<div class="card">
  <div class="card-title" style="color:#c7d2fe">🔢 확률 공식으로 이해하기</div>
  <div class="formula-big">
    <div class="fb-title">📌 사건 정의</div>
    <div class="fb-parts">
      <div class="fb-part"><div class="fb-dot dot-a"></div><span><strong style="color:#a5b4fc">A</strong> : 실제로 민감한 경험이 있는 사건</span></div>
      <div class="fb-part"><div class="fb-dot dot-b"></div><span><strong style="color:#fbbf24">B</strong> : 동전 앞면 → 설문지 1 선택 (P(B) = 1/2)</span></div>
      <div class="fb-part"><div class="fb-dot dot-bc"></div><span><strong style="color:#34d399">B<sup>c</sup></strong> : 동전 뒷면 → 설문지 2 선택 (P(B<sup>c</sup>) = 1/2)</span></div>
    </div>
  </div>
  <div class="formula-big">
    <div class="fb-title">📌 '예'라고 답할 확률</div>
    <div class="fb-expr">
      P(예라고 답함)<br>
      = P(B) + P(A ∩ B<sup>c</sup>)<br>
      = P(B) + P(A)·P(B<sup>c</sup>)  ← A와 B는 독립!<br>
      = 1/2 + P(A)·(1/2)
    </div>
    <div class="fb-parts" style="margin-top:12px">
      <div class="fb-part"><div class="fb-dot dot-b"></div><span>P(B): 앞면이 나와서 무조건 '예'라고 답하는 경우</span></div>
      <div class="fb-part"><div class="fb-dot dot-bc"></div><span>P(A∩B<sup>c</sup>): 뒷면이 나왔고 실제로 경험도 있는 경우</span></div>
    </div>
  </div>
  <div class="formula-big">
    <div class="fb-title">📌 역으로 P(A) 추정하기</div>
    <div class="fb-expr">
      P(예라고 답함) = 1/2 + P(A)/2<br><br>
      ∴ P(A) = 2×P(예라고 답함) − 1
    </div>
    <div style="margin-top:10px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);border-radius:10px;padding:10px 14px;font-size:13px;color:#fbbf24">
      💡 예시: 100명 중 70명이 '예'라고 답했다면<br>
      P(A) = 2 × 0.7 − 1 = <strong>0.4</strong> → 실제 경험자는 약 <strong>40명</strong>으로 추정!
    </div>
  </div>
</div>

<!-- ════════════════════════════════════════════════
  SECTION 6 : 가상 설문 시뮬레이션
════════════════════════════════════════════════ -->
<div class="card">
  <div class="card-title" style="color:#f472b6">🎯 우리 반 가상 설문 시뮬레이터</div>
  <p style="font-size:12px;color:#64748b;margin-bottom:12px">
    실제 경험 비율을 설정하고 설문을 진행해보세요. 결과가 어떻게 나오는지 확인하세요!
  </p>

  <div class="calc-row">
    <div class="calc-label" style="min-width:130px">실제 경험자 비율 p</div>
    <input type="range" id="sim-p" min="0" max="100" value="40" oninput="updateSimUI()">
    <span class="vbadge" id="sim-p-v" style="background:linear-gradient(135deg,#f59e0b,#d97706)">40</span>%
  </div>

  <div class="sim-grid">
    <div class="sim-kpi kpi-total"><div class="sk-num" id="sim-total">0</div><div class="sk-lbl">총 응답자</div></div>
    <div class="sim-kpi kpi-yes"><div class="sk-num" id="sim-yes">0</div><div class="sk-lbl">'예' 응답</div></div>
    <div class="sim-kpi kpi-est"><div class="sk-num" id="sim-est">—</div><div class="sk-lbl">추정 경험자%</div></div>
  </div>

  <div style="margin:8px 0 4px;font-size:11px;color:#64748b">응답 비율</div>
  <div class="pbar-wrap"><div class="pbar-fill yes-bar" id="sim-yes-bar" style="width:0%">0%</div></div>
  <div style="font-size:11px;color:#64748b;margin-top:8px">추정된 실제 경험자 비율</div>
  <div class="pbar-wrap"><div class="pbar-fill real-bar" id="sim-real-bar" style="width:0%">0%</div></div>

  <div class="sim-log" id="sim-log"></div>

  <div class="sim-btn-row">
    <button class="sim-btn primary" onclick="simOne()">한 명 응답</button>
    <button class="sim-btn fast" onclick="simMany(10)">10명 추가</button>
    <button class="sim-btn fast" onclick="simMany(30)">30명 추가</button>
    <button class="sim-btn secondary" onclick="simReset()">초기화</button>
  </div>
</div>

<script>
// ── Coin flip ─────────────────────────────────────────────────
function flipCoin(){
  const coin = document.getElementById('flipCoin');
  const res  = document.getElementById('coinResult');
  coin.className = 'coin spinning';
  res.innerHTML  = '';
  setTimeout(()=>{
    const isHeads = Math.random() < 0.5;
    coin.className = 'coin ' + (isHeads ? 'heads' : 'tails');
    coin.textContent = isHeads ? '☀️' : '🌙';
    res.innerHTML = isHeads
      ? '<div class="result-banner heads-res">☀️ 앞면! → 설문지 1 선택 → 무조건 <strong>"예"</strong>라고 답하세요</div>'
      : '<div class="result-banner tails-res">🌙 뒷면! → 설문지 2 선택 → 민감한 질문에 <strong>솔직하게</strong> 답하세요</div>';
  }, 700);
}

// ── Case tabs ─────────────────────────────────────────────────
function showCase(idx){
  document.querySelectorAll('.case-tab').forEach((t,i)=>{
    t.classList.toggle('active', i===idx);
  });
  document.querySelectorAll('.case-pane').forEach((p,i)=>{
    p.classList.toggle('active', i===idx);
  });
  calcCase(idx);
}

// ── Estimation calculator ──────────────────────────────────────
function calcCase(idx){
  const nEl   = document.getElementById('s'+idx+'-n');
  const yesEl = document.getElementById('s'+idx+'-yes');
  const fEl   = document.getElementById('s'+idx+'-formula');
  const aEl   = document.getElementById('s'+idx+'-answer');
  if(!nEl) return;

  const n   = parseInt(nEl.value);
  const yes = Math.min(parseInt(yesEl.value), n);

  document.getElementById('s'+idx+'-n-v').textContent   = n;
  document.getElementById('s'+idx+'-yes-v').textContent = yes;

  // clamp yes slider max
  yesEl.max = n;
  if(parseInt(yesEl.value) > n) yesEl.value = n;

  const pYes = yes / n;
  const pA   = 2 * pYes - 1;
  const estN = Math.max(0, Math.round(pA * n));
  const pct  = (pA * 100).toFixed(1);

  fEl.innerHTML =
    `P(예라고 답함) = <span class="fv">${yes}</span> / <span class="fv">${n}</span> = <span class="fv">${pYes.toFixed(4)}</span><br>`+
    `P(A) = 2 × ${pYes.toFixed(4)} − 1 = <span class="fv2">${pA.toFixed(4)}</span>`;

  if(pA < 0){
    aEl.innerHTML = `<div class="ans-label">⚠ '예' 응답이 너무 적습니다</div><div class="ans-val" style="color:#f87171">음수 → 0%</div>`;
  } else {
    aEl.innerHTML =
      `<div class="ans-label">실제 경험자 추정</div>`+
      `<div class="ans-val">약 ${estN}명 (${pct}%)</div>`+
      `<div class="ans-sub">${n}명 중 약 ${pct}%가 실제 경험자로 추정됩니다</div>`;
  }
}

// ── Simulation ────────────────────────────────────────────────
let simTotal=0, simYesCount=0;

function updateSimUI(){
  document.getElementById('sim-p-v').textContent = document.getElementById('sim-p').value;
}

function simOne(){
  const realP = parseInt(document.getElementById('sim-p').value)/100;
  const isHeads = Math.random()<0.5;
  let answeredYes;
  let reason;
  if(isHeads){
    answeredYes = true;
    reason = '☀️ 앞면 → 설문지 1 → 무조건 "예"';
  } else {
    const hasExp = Math.random() < realP;
    answeredYes = hasExp;
    reason = hasExp ? '🌙 뒷면 → 설문지 2 → "예" (경험 있음)' : '🌙 뒷면 → 설문지 2 → "아니요" (경험 없음)';
  }

  simTotal++;
  if(answeredYes) simYesCount++;

  const log = document.getElementById('sim-log');
  const item = document.createElement('div');
  item.className = 'log-item ' + (answeredYes ? 'li-yes' : 'li-no');
  item.innerHTML = `<strong>#${simTotal}</strong> ${reason} → <strong>${answeredYes?'✅ 예':'❌ 아니요'}</strong>`;
  log.prepend(item);
  if(log.children.length > 50) log.lastChild.remove();

  refreshSim();
}

function simMany(cnt){
  for(let i=0;i<cnt;i++) simOne();
}

function simReset(){
  simTotal=0; simYesCount=0;
  document.getElementById('sim-log').innerHTML='';
  refreshSim();
}

function refreshSim(){
  document.getElementById('sim-total').textContent = simTotal;
  document.getElementById('sim-yes').textContent   = simYesCount;

  const pYes = simTotal>0 ? simYesCount/simTotal : 0;
  const pA   = Math.max(0, 2*pYes - 1);
  const pct  = simTotal>0 ? (pA*100).toFixed(1) : '—';

  document.getElementById('sim-est').textContent = simTotal>0 ? pct+'%' : '—';

  const yBarW = Math.round(pYes*100);
  const rBarW = Math.round(pA*100);
  const yBar  = document.getElementById('sim-yes-bar');
  const rBar  = document.getElementById('sim-real-bar');
  yBar.style.width = yBarW+'%';
  yBar.textContent = yBarW>8 ? yBarW+'%' : '';
  rBar.style.width = rBarW+'%';
  rBar.textContent = rBarW>8 ? rBarW+'%' : '';
}

// init
calcCase(0);
calcCase(1);
calcCase(2);
calcCase(3);
</script>

</body>
</html>
"""

def render():
    st.header("🎲 솔직한 설문의 비밀 – 무작위 응답 기법")
    st.caption("민감한 질문에도 솔직한 답변을 유도하는 확률 기반 설문 기법을 체험해봅니다.")

    components.html(_HTML, height=3400, scrolling=False)

    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
