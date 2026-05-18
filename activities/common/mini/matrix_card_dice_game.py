# activities/common/mini/matrix_card_dice_game.py
"""
행렬 카드 주사위 게임
6면 주사위(+,−,×,0,½,2)로 진행하는 2인 행렬 대전 게임
×: 나=A×B, 친구=B×A (순서에 따라 점수 달라짐)
−: 나=A−B, 친구=B−A
숫자: 나=k×sum(내 카드), 친구=k×sum(친구 카드)
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "행렬카드주사위게임"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 '행렬 카드 주사위 게임'을 마치고 배운 내용을 정리해보세요**"},
    {"key": "mul_condition",
     "label": "1️⃣ 행렬 A×B의 곱셈이 가능하려면 어떤 조건이 필요한가요? 게임에서 경험한 상황을 예시로 설명해보세요.",
     "type": "text_area", "height": 110},
    {"key": "noncommutative",
     "label": "2️⃣ × 주사위가 나왔을 때 나와 친구의 점수가 달랐던 이유는 무엇인가요? A×B와 B×A의 차이를 설명해보세요.",
     "type": "text_area", "height": 110},
    {"key": "minus_round",
     "label": "3️⃣ − 주사위가 나왔을 때 나와 친구의 점수가 어떤 관계였나요? 왜 그런지 설명해보세요.",
     "type": "text_area", "height": 100},
    {"key": "strategy",
     "label": "4️⃣ 높은 점수를 얻기 위해 어떤 행렬 카드를 선택하는 것이 유리했나요? 자신만의 전략을 설명해보세요.",
     "type": "text_area", "height": 100},
    {"key": "새롭게알게된점",
     "label": "💡 이 활동을 통해 새롭게 알게 된 점",
     "type": "text_area", "height": 90},
    {"key": "느낀점",
     "label": "💬 이 활동을 하면서 느낀 점",
     "type": "text_area", "height": 90},
]

META = {
    "title":       "🎲 행렬 카드 주사위 게임",
    "description": "12장 행렬 카드와 6면 주사위(+,−,×,0,½,2)로 벌이는 2인 행렬 대전 게임",
    "order":       5,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>행렬 카드 주사위 게임</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#06090f;color:#c8d8ec;padding:8px;min-height:100vh}

/* tabs */
.tabs{display:flex;gap:6px;margin-bottom:12px}
.tb{flex:1;padding:10px 4px;text-align:center;border-radius:11px;border:2px solid #152035;
  background:#0a1525;color:#3d5878;font-size:.82rem;font-weight:800;cursor:pointer;transition:all .2s;line-height:1.4}
.tb.on{background:linear-gradient(135deg,#1d4ed8,#7c3aed);color:#fff;border-color:transparent;
  box-shadow:0 3px 16px rgba(99,102,241,.35)}
.panel{display:none}.panel.on{display:block}

/* rule card */
.rule-card{background:#0d1a2e;border:1px solid #1e3050;border-radius:14px;padding:16px;margin-bottom:10px}
.rule-title{font-size:1.05rem;font-weight:900;color:#fbbf24;margin-bottom:12px}
.rule-list{display:flex;flex-direction:column;gap:10px}
.rule-item{background:#060c18;border:1px solid #1a3050;border-radius:10px;padding:12px;display:flex;gap:10px;align-items:flex-start}
.rule-num{font-size:1.3rem;font-weight:900;color:#38bdf8;flex-shrink:0;min-width:28px}
.rule-text{font-size:.9rem;line-height:1.75;color:#94a3b8}
.rule-em{color:#fbbf24;font-weight:800}
.rule-em2{color:#f472b6;font-weight:800}

/* die preview in rule */
.die-faces-row{display:flex;gap:5px;flex-wrap:wrap;margin:8px 0}
.df{width:36px;height:36px;border-radius:7px;display:flex;align-items:center;justify-content:center;
  font-size:1rem;font-weight:900;border:1.5px solid #1e3050;background:#060c18}
.df.op{border-color:#f59e0b;color:#fbbf24}
.df.num{border-color:#a78bfa;color:#c4b5fd}
.rule-note{background:rgba(56,189,248,.07);border-left:3px solid #38bdf8;
  border-radius:0 8px 8px 0;padding:8px 12px;font-size:.82rem;color:#7dd3fc;margin-top:8px;line-height:1.7}

/* example table */
.ex-table{width:100%;border-collapse:collapse;font-size:.8rem;margin-top:8px}
.ex-table th{background:#0a1525;color:#64748b;font-weight:700;padding:6px 8px;border:1px solid #1a3050;text-align:center}
.ex-table td{padding:6px 8px;border:1px solid #0f1e30;text-align:center;vertical-align:middle}
.ex-table td.me{color:#93c5fd}
.ex-table td.fr{color:#f9a8d4}
.ex-table td.face{color:#fbbf24;font-size:1rem;font-weight:900}

/* matrix inline */
.mat-i{display:inline-flex;align-items:stretch;vertical-align:middle}
.mi-bl,.mi-br{width:6px;flex-shrink:0}
.mi-bl{border-top:2.5px solid currentColor;border-bottom:2.5px solid currentColor;
  border-left:2.5px solid currentColor;border-radius:3px 0 0 3px}
.mi-br{border-top:2.5px solid currentColor;border-bottom:2.5px solid currentColor;
  border-right:2.5px solid currentColor;border-radius:0 3px 3px 0}
.mi-g{display:grid;gap:3px;padding:4px 3px}
.mc{min-width:28px;height:26px;display:flex;align-items:center;justify-content:center;
  background:#0d1e30;border:1px solid #1e3a5c;border-radius:3px;
  font-size:.85rem;font-weight:700;font-family:'Courier New',monospace;color:#e2e8f0}
.mc.gold{background:rgba(251,191,36,.15);border-color:#f59e0b;color:#fbbf24}
.mc.purple{background:rgba(167,139,250,.15);border-color:#8b5cf6;color:#c4b5fd}
.mc.green{background:rgba(34,197,94,.15);border-color:#22c55e;color:#4ade80}

/* scoreboard */
.scoreboard{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;margin-bottom:12px}
.ps{background:#0d1a2e;border:2px solid #1e3050;border-radius:14px;padding:12px 10px;text-align:center}
.ps.me{border-color:#3b82f6}.ps.fr{border-color:#ec4899}
.ps-name{font-size:.78rem;font-weight:800;margin-bottom:4px}
.ps-name.me{color:#60a5fa}.ps-name.fr{color:#f472b6}
.ps-val{font-size:2.2rem;font-weight:900;line-height:1}
.ps-val.me{color:#93c5fd}.ps-val.fr{color:#f9a8d4}
.ps-sub{font-size:.62rem;color:#475569;margin-top:2px}
.round-info{text-align:center}
.rbadge{background:linear-gradient(135deg,#1d4ed8,#7c3aed);color:#fff;
  font-size:.85rem;font-weight:900;border-radius:10px;padding:6px 14px;display:inline-block;margin-bottom:4px}
.rsub{font-size:.7rem;color:#475569}

/* card grid */
.sec-label{font-size:.78rem;font-weight:800;color:#64748b;letter-spacing:.06em;margin:10px 0 6px}
.card-grid{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.crd{background:#0d1a2e;border:2px solid #1e3050;border-radius:10px;
  padding:9px 7px;cursor:pointer;transition:all .2s;text-align:center;flex-shrink:0}
.crd:hover:not(.used):not(.sel-me):not(.sel-fr){border-color:#3b82f6;transform:translateY(-2px)}
.crd.used{opacity:.28;cursor:default;filter:grayscale(.85)}
.crd.sel-me{border-color:#3b82f6;background:rgba(59,130,246,.12);
  box-shadow:0 0 14px rgba(59,130,246,.4);transform:translateY(-3px)}
.crd.sel-fr{border-color:#ec4899;background:rgba(236,72,153,.12);
  box-shadow:0 0 14px rgba(236,72,153,.4);transform:translateY(-3px)}
.clbl{font-size:.6rem;font-weight:700;margin-bottom:3px;color:#475569}
.clbl.me{color:#60a5fa}.clbl.fr{color:#f472b6}
.cshp{font-size:.58rem;color:#334155;margin-top:3px}

/* action zone */
.az{background:#0d1a2e;border:1px solid #1e3050;border-radius:14px;padding:14px;margin-bottom:10px}
.az-inner{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.die-wrap{display:flex;flex-direction:column;align-items:center;gap:5px;flex-shrink:0}
.die-face{width:80px;height:80px;border-radius:16px;border:2.5px solid #1e3050;
  background:#060c18;display:flex;align-items:center;justify-content:center;
  font-size:2.2rem;font-weight:900;color:#475569;transition:all .25s;user-select:none}
.die-face.rolled-op{border-color:#f59e0b;color:#fbbf24;box-shadow:0 0 22px rgba(245,158,11,.35)}
.die-face.rolled-num{border-color:#a78bfa;color:#c4b5fd;box-shadow:0 0 22px rgba(167,139,250,.35)}
.die-face.rolling{animation:droll .5s ease-out}
@keyframes droll{0%,100%{transform:scale(1)}25%{transform:scale(1.18)rotate(-9deg)}
  50%{transform:scale(.9)rotate(7deg)}75%{transform:scale(1.06)rotate(-4deg)}}
.die-label{font-size:.65rem;color:#475569;text-align:center}
.az-right{flex:1;min-width:0}
.az-ctx{font-size:.82rem;color:#64748b;margin-bottom:10px;line-height:1.6;
  background:#060c18;border-radius:8px;padding:8px 10px;border:1px solid #152035}
.btn-row{display:flex;gap:8px;flex-wrap:wrap}
.btn{padding:10px 16px;border-radius:10px;border:none;cursor:pointer;
  font-size:.83rem;font-weight:800;transition:all .18s;letter-spacing:.01em}
.btn:hover:not(:disabled){transform:translateY(-2px)}
.btn:disabled{opacity:.35;cursor:default;transform:none}
.btn-roll{background:linear-gradient(135deg,#d97706,#b45309);color:#fff;box-shadow:0 3px 10px rgba(217,119,6,.3)}
.btn-confirm{background:linear-gradient(135deg,#059669,#047857);color:#fff;box-shadow:0 3px 10px rgba(5,150,105,.25)}
.btn-next{background:linear-gradient(135deg,#1d4ed8,#7c3aed);color:#fff}
.btn-restart{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff}

/* calc zone */
.czn{display:none;background:#060c18;border:1px solid #1e3050;border-radius:12px;
  padding:12px;margin-bottom:10px}
.czn.show{display:block}
.czn-hdr{font-size:.72rem;font-weight:800;color:#475569;letter-spacing:.05em;margin-bottom:10px}
.pcalc-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}
.pcalc{background:#0a1525;border-radius:10px;padding:12px;min-width:0}
.pcalc.me{border:1px solid rgba(59,130,246,.3)}
.pcalc.fr{border:1px solid rgba(236,72,153,.3)}
.pcalc-hdr{font-size:.8rem;font-weight:800;padding-bottom:7px;margin-bottom:9px;
  border-bottom:1px solid #152035}
.pcalc-hdr.me{color:#60a5fa}.pcalc-hdr.fr{color:#f472b6}
.eq-row{display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin-bottom:5px}
.opsm{font-size:1.3rem;font-weight:900;color:#475569;flex-shrink:0}
.eqsm{font-size:1.1rem;font-weight:900;color:#475569;flex-shrink:0}
.sum-line{font-size:.82rem;color:#94a3b8;margin-top:5px}
.sum-val{color:#4ade80;font-weight:800}
.scalar-k{font-size:1.5rem;font-weight:900;color:#a78bfa;flex-shrink:0}
.bad-txt{color:#f87171;font-size:.82rem}
.dim-txt{color:#64748b;font-size:.72rem;margin-top:3px}
.pcalc-score{font-size:1.6rem;font-weight:900;margin-top:9px;padding-top:8px;
  border-top:1px solid #152035;letter-spacing:.02em}
.pcalc-score.me{color:#93c5fd}.pcalc-score.fr{color:#f9a8d4}
.rw-banner{font-size:.85rem;font-weight:800;text-align:center;padding:8px 14px;
  border-radius:8px;margin-top:2px}
.rw-banner.me{background:rgba(59,130,246,.1);color:#60a5fa;border:1px solid rgba(59,130,246,.25)}
.rw-banner.fr{background:rgba(236,72,153,.1);color:#f472b6;border:1px solid rgba(236,72,153,.25)}
.rw-banner.tie{background:rgba(251,191,36,.07);color:#fbbf24;border:1px solid rgba(251,191,36,.2)}

/* history */
.hist{display:none;background:#0a1525;border:1px solid #152035;border-radius:12px;
  padding:10px;margin-bottom:10px}
.hist-ttl{font-size:.7rem;font-weight:800;color:#475569;margin-bottom:6px;letter-spacing:.04em}
.hr{display:flex;align-items:center;gap:6px;padding:5px 0;border-bottom:1px solid #0f1e30;font-size:.74rem;flex-wrap:wrap}
.hr:last-child{border-bottom:none}
.h-rnd{color:#64748b;min-width:30px;font-weight:700}
.h-face{font-size:.95rem;font-weight:900;min-width:22px;text-align:center;color:#fbbf24}
.h-me{color:#93c5fd;font-weight:800;min-width:48px}
.h-fr{color:#f9a8d4;font-weight:800;min-width:48px}
.h-win{font-size:.67rem;font-weight:800;padding:1px 6px;border-radius:4px}
.h-win.me{background:rgba(59,130,246,.15);color:#60a5fa}
.h-win.fr{background:rgba(236,72,153,.15);color:#f472b6}
.h-win.tie{background:rgba(251,191,36,.1);color:#fbbf24}

/* final */
.final{display:none;text-align:center;padding:20px 10px}
.final.show{display:block}
.f-trophy{font-size:4rem;animation:bonce 1s ease infinite}
@keyframes bonce{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.f-title{font-size:1.5rem;font-weight:900;margin:10px 0 4px}
.f-sub{font-size:.88rem;color:#64748b;margin-bottom:16px}
.f-scores{display:flex;gap:12px;justify-content:center;margin-bottom:16px;flex-wrap:wrap}
.fsc{border-radius:14px;padding:16px 22px;min-width:110px}
.fsc.me{background:rgba(59,130,246,.1);border:2px solid rgba(59,130,246,.35)}
.fsc.fr{background:rgba(236,72,153,.1);border:2px solid rgba(236,72,153,.35)}
.fsc-nm{font-size:.78rem;font-weight:800;margin-bottom:5px}
.fsc-nm.me{color:#60a5fa}.fsc-nm.fr{color:#f472b6}
.fsc-v{font-size:2.6rem;font-weight:900}
.fsc-v.me{color:#93c5fd}.fsc-v.fr{color:#f9a8d4}
.fsc-s{font-size:.68rem;color:#475569;margin-top:3px}

/* particles */
.pt{position:fixed;pointer-events:none;border-radius:50%;z-index:9999;animation:ptf 1s ease-out forwards}
@keyframes ptf{0%{opacity:1;transform:translate(0,0)scale(1)}100%{opacity:0;transform:translate(var(--tx),var(--ty))scale(0)}}

@media(max-width:480px){.pcalc-grid{grid-template-columns:1fr}}
</style>
</head>
<body>

<!-- TABS -->
<div class="tabs">
  <div class="tb on" id="tb-rule" onclick="switchTab('rule')">📖 게임 규칙</div>
  <div class="tb"    id="tb-game" onclick="switchTab('game')">🎮 게임 시작</div>
</div>

<!-- ═══ RULE PANEL ═══ -->
<div class="panel on" id="panel-rule">
  <div class="rule-card">
    <div class="rule-title">🎲 행렬 카드 주사위 게임 규칙</div>

    <!-- die preview -->
    <div style="background:#060c18;border:1px solid #1a3050;border-radius:10px;padding:12px;margin-bottom:12px">
      <div style="font-size:.75rem;color:#64748b;font-weight:700;margin-bottom:8px">주사위 6면 (각 면에 하나씩)</div>
      <div class="die-faces-row">
        <div class="df op">+</div>
        <div class="df op">−</div>
        <div class="df op">×</div>
        <div class="df num">0</div>
        <div class="df num">½</div>
        <div class="df num">2</div>
      </div>
      <div style="font-size:.78rem;color:#94a3b8;line-height:1.7;margin-top:6px">
        <span style="color:#fbbf24;font-weight:800">+, −, ×</span> → 두 카드로 행렬 연산 &nbsp;|&nbsp;
        <span style="color:#c4b5fd;font-weight:800">0, ½, 2</span> → 자신의 카드에 실수배
      </div>
    </div>

    <div class="rule-list">
      <div class="rule-item">
        <div class="rule-num">①</div>
        <div class="rule-text">매 라운드, <span class="rule-em">나</span>와 <span class="rule-em2">친구</span>가 행렬 카드를 각각 1장씩 선택한다. 한 번 선택한 카드는 다시 선택할 수 없다.</div>
      </div>
      <div class="rule-item">
        <div class="rule-num">②</div>
        <div class="rule-text">주사위를 굴려 <span class="rule-em">+, −, ×</span> 중 하나가 나오면 행렬 연산을 수행한다.<br>
          <span class="rule-em">+</span>: 나와 친구 모두 A+B 결과의 성분 합을 점수로 한다.<br>
          <span class="rule-em">−</span>: <span class="rule-em">나</span>는 A−B, <span class="rule-em2">친구</span>는 B−A 결과의 성분 합을 점수로 한다.<br>
          <span class="rule-em">×</span>: <span class="rule-em">나</span>는 A×B, <span class="rule-em2">친구</span>는 B×A 결과의 성분 합을 점수로 한다.<br>
          연산이 불가능하면 0점. 음수 합이 나오면 0점 처리.
        </div>
      </div>
      <div class="rule-item">
        <div class="rule-num">③</div>
        <div class="rule-text">주사위가 <span class="rule-em">0, ½, 2</span> 중 하나가 나오면 각자 자신의 카드에 그 수를 실수배하고, 성분의 합을 점수로 한다.<br>
          나: <span class="rule-em">k × (내 카드 성분의 합)</span>, 친구: <span class="rule-em2">k × (친구 카드 성분의 합)</span></div>
      </div>
      <div class="rule-item">
        <div class="rule-num">④</div>
        <div class="rule-text">이 과정을 <span class="rule-em">6라운드</span> 반복하여 <span class="rule-em">최종 합산 점수가 큰 쪽</span>이 이긴다!</div>
      </div>
    </div>

    <div class="rule-note" style="margin-top:12px">
      💡 <strong>핵심 포인트:</strong> 행렬 곱셈에서 A×B와 B×A는 크기도, 값도 다를 수 있습니다! − 연산도 A−B와 B−A는 반대입니다. 어떤 카드를 선택하느냐에 따라 점수가 달라집니다.
    </div>

    <!-- example table -->
    <div style="margin-top:12px">
      <div style="font-size:.75rem;color:#64748b;font-weight:700;margin-bottom:6px">📌 예시 — 주사위: ×, 나: (1×2행렬), 친구: (2×1행렬)</div>
      <table class="ex-table">
        <tr><th>계산자</th><th>계산식</th><th>결과</th><th>점수</th></tr>
        <tr>
          <td class="me">👤 나</td>
          <td><span style="color:#fbbf24">(1 0)</span> × <span style="color:#c4b5fd">[[1],[4]]</span></td>
          <td style="color:#4ade80">[[1]] &nbsp; <small style="color:#64748b">(1×1)</small></td>
          <td class="me">1점</td>
        </tr>
        <tr>
          <td class="fr">👥 친구</td>
          <td><span style="color:#c4b5fd">[[1],[4]]</span> × <span style="color:#fbbf24">(1 0)</span></td>
          <td style="color:#4ade80">[[1,0],[4,0]] &nbsp; <small style="color:#64748b">(2×2)</small></td>
          <td class="fr">5점</td>
        </tr>
      </table>
      <div style="font-size:.72rem;color:#64748b;margin-top:5px">→ 같은 카드 두 장으로도 순서에 따라 결과가 완전히 달라집니다!</div>
    </div>
  </div>

  <div style="text-align:center;margin-top:4px">
    <button class="btn btn-next" onclick="switchTab('game')">🎮 게임 시작하기 ▶</button>
  </div>
</div>

<!-- ═══ GAME PANEL ═══ -->
<div class="panel" id="panel-game">

  <!-- scoreboard -->
  <div class="scoreboard">
    <div class="ps me">
      <div class="ps-name me">👤 나</div>
      <div class="ps-val me" id="score-me">0</div>
      <div class="ps-sub" id="wins-me">0승</div>
    </div>
    <div class="round-info">
      <div class="rbadge" id="rbadge">라운드 1 / 6</div>
      <div class="rsub"   id="rsub">카드를 선택하세요</div>
    </div>
    <div class="ps fr">
      <div class="ps-name fr">👥 친구</div>
      <div class="ps-val fr" id="score-fr">0</div>
      <div class="ps-sub" id="wins-fr">0승</div>
    </div>
  </div>

  <!-- card grid -->
  <div class="sec-label">🃏 행렬 카드 — 먼저 <span style="color:#60a5fa">나</span>의 카드, 다음에 <span style="color:#f472b6">친구</span>의 카드를 선택하세요</div>
  <div class="card-grid" id="card-grid"></div>

  <!-- action zone -->
  <div class="az">
    <div class="az-inner">
      <div class="die-wrap">
        <div class="die-face" id="die-face">?</div>
        <div class="die-label" id="die-label">주사위</div>
      </div>
      <div class="az-right">
        <div class="az-ctx" id="az-ctx">카드를 2장 선택한 후 주사위를 굴리세요.</div>
        <div class="btn-row">
          <button class="btn btn-roll"    id="btn-roll"    onclick="rollDice()"      disabled>🎲 주사위 굴리기</button>
          <button class="btn btn-confirm" id="btn-confirm" onclick="confirmRound()"  disabled>✅ 라운드 확정</button>
          <button class="btn btn-next"    id="btn-next"    onclick="nextRound()"     style="display:none">다음 라운드 ▶</button>
        </div>
      </div>
    </div>
  </div>

  <!-- calc zone -->
  <div class="czn" id="czn">
    <div class="czn-hdr">📐 이번 라운드 계산 결과</div>
    <div class="pcalc-grid">
      <div class="pcalc me">
        <div class="pcalc-hdr me">👤 나의 계산</div>
        <div id="pbody-me"></div>
        <div class="pcalc-score me" id="pscore-me"></div>
      </div>
      <div class="pcalc fr">
        <div class="pcalc-hdr fr">👥 친구의 계산</div>
        <div id="pbody-fr"></div>
        <div class="pcalc-score fr" id="pscore-fr"></div>
      </div>
    </div>
    <div class="rw-banner" id="rw-banner"></div>
  </div>

  <!-- history -->
  <div class="hist" id="hist">
    <div class="hist-ttl">📋 라운드 기록</div>
    <div id="hist-rows"></div>
  </div>

  <!-- final -->
  <div class="final" id="final">
    <div class="f-trophy" id="f-trophy">🏆</div>
    <div class="f-title" id="f-title"></div>
    <div class="f-sub"   id="f-sub"></div>
    <div class="f-scores">
      <div class="fsc me">
        <div class="fsc-nm me">👤 나</div>
        <div class="fsc-v me" id="f-me">0</div>
        <div class="fsc-s"   id="f-wins-me">0라운드 승</div>
      </div>
      <div class="fsc fr">
        <div class="fsc-nm fr">👥 친구</div>
        <div class="fsc-v fr" id="f-fr">0</div>
        <div class="fsc-s"   id="f-wins-fr">0라운드 승</div>
      </div>
    </div>
    <button class="btn btn-restart" onclick="restartGame()">🔄 다시 하기</button>
  </div>

</div><!-- /panel-game -->

<script>
/* ═══ DATA ═══ */
const CARDS = [
  {id:0,  data:[[2,0],[1,3]],  shape:[2,2]},
  {id:1,  data:[[0,2]],        shape:[1,2]},
  {id:2,  data:[[1],[1]],      shape:[2,1]},
  {id:3,  data:[[4,0],[3,1]],  shape:[2,2]},
  {id:4,  data:[[3],[1]],      shape:[2,1]},
  {id:5,  data:[[1,3],[2,5]],  shape:[2,2]},
  {id:6,  data:[[1,0]],        shape:[1,2]},
  {id:7,  data:[[3,2]],        shape:[1,2]},
  {id:8,  data:[[3,1]],        shape:[1,2]},
  {id:9,  data:[[1],[4]],      shape:[2,1]},
  {id:10, data:[[2,0],[1,2]],  shape:[2,2]},
  {id:11, data:[[3],[5]],      shape:[2,1]},
];
const FACES = ['+', '−', '×', '0', '½', '2'];

/* ═══ STATE ═══ */
let totalMe=0, totalFr=0, winsMe=0, winsFr=0;
let round=1;
let usedCards=new Set();
let selMe=null, selFr=null;
let pickState='me'; // 'me' | 'fr' | 'done'
let currentFace=null;
let roundDone=false;
let histData=[];

/* ═══ MATRIX HELPERS ═══ */
function matMul(A, B){
  const rA=A.shape[0], cA=A.shape[1], rB=B.shape[0], cB=B.shape[1];
  if(cA!==rB) return null;
  const res=[];
  for(let i=0;i<rA;i++){
    res.push([]);
    for(let j=0;j<cB;j++){
      let s=0;
      for(let k=0;k<cA;k++) s+=A.data[i][k]*B.data[k][j];
      res[i].push(s);
    }
  }
  return {data:res, shape:[rA,cB]};
}
function matAdd(A, B, op){
  if(A.shape[0]!==B.shape[0]||A.shape[1]!==B.shape[1]) return null;
  const s=op==='+'?1:-1;
  return {data:A.data.map((row,i)=>row.map((v,j)=>v+s*B.data[i][j])), shape:A.shape};
}
function sumElems(mat){ return mat.data.reduce((a,row)=>a+row.reduce((b,v)=>b+v,0),0); }

/* ═══ FORMAT MATRIX HTML ═══ */
function fmtMat(card, cls){
  const c=card.shape[1];
  const cells=card.data.map(row=>row.map(v=>`<div class="mc ${cls}">${v}</div>`).join('')).join('');
  return `<span class="mat-i" style="color:inherit">
    <span class="mi-bl"></span>
    <span class="mi-g" style="grid-template-columns:repeat(${c},28px)">${cells}</span>
    <span class="mi-br"></span>
  </span>`;
}

/* ═══ ROUND CALCULATION ═══ */
function calcRound(cMe, cFr, face){
  let scoreMe=0, scoreFr=0, htmlMe='', htmlFr='';

  if(face==='+'){
    const res=matAdd(cMe, cFr, '+');
    if(!res){
      scoreMe=scoreFr=0;
      const msg=`<span class="bad-txt">크기 불일치: ${cMe.shape.join('×')} + ${cFr.shape.join('×')} → 불가</span><div class="dim-txt">0점</div>`;
      htmlMe=htmlFr=msg;
    } else {
      const s=sumElems(res);
      scoreMe=scoreFr=s;
      const eq=mkEqHtml(cMe,'+',cFr,res);
      htmlMe=htmlFr=eq+`<div class="sum-line">성분의 합 = <span class="sum-val">${s}</span>점 <span style="color:#64748b;font-size:.72rem">(+는 두 사람 동일)</span></div>`;
    }
  }
  else if(face==='−'){
    const resAB=matAdd(cMe, cFr, '−');
    if(!resAB){
      scoreMe=scoreFr=0;
      const msg=`<span class="bad-txt">크기 불일치 → 불가</span><div class="dim-txt">0점</div>`;
      htmlMe=htmlFr=msg;
    } else {
      const resBA=matAdd(cFr, cMe, '−');
      const sAB=sumElems(resAB);
      const sBA=resBA?sumElems(resBA):0;
      scoreMe=Math.max(0,sAB);
      scoreFr=Math.max(0,sBA);
      htmlMe=mkEqHtml(cMe,'−',cFr,resAB)+`<div class="sum-line">성분의 합 = <span class="sum-val">${sAB}</span>${sAB<0?' <span style="color:#64748b;font-size:.72rem">→ 0점</span>':''}</div>`;
      htmlFr=mkEqHtml(cFr,'−',cMe,resBA)+`<div class="sum-line">성분의 합 = <span class="sum-val">${sBA}</span>${sBA<0?' <span style="color:#64748b;font-size:.72rem">→ 0점</span>':''}</div>`;
    }
  }
  else if(face==='×'){
    const AB=matMul(cMe, cFr); // 나: A×B
    const BA=matMul(cFr, cMe); // 친구: B×A
    const sAB=AB?sumElems(AB):null;
    const sBA=BA?sumElems(BA):null;
    scoreMe=sAB!==null?sAB:0;
    scoreFr=sBA!==null?sBA:0;
    if(AB){
      htmlMe=mkEqHtml(cMe,'×',cFr,AB)+`<div class="sum-line">성분의 합 = <span class="sum-val">${sAB}</span>점</div>`;
    } else {
      htmlMe=`<span class="bad-txt">나(${cMe.shape.join('×')}) × 친구(${cFr.shape.join('×')})<br>열수≠행수 → 곱셈 불가</span><div class="dim-txt">0점</div>`;
    }
    if(BA){
      htmlFr=mkEqHtml(cFr,'×',cMe,BA)+`<div class="sum-line">성분의 합 = <span class="sum-val">${sBA}</span>점</div>`;
    } else {
      htmlFr=`<span class="bad-txt">친구(${cFr.shape.join('×')}) × 나(${cMe.shape.join('×')})<br>열수≠행수 → 곱셈 불가</span><div class="dim-txt">0점</div>`;
    }
  }
  else {
    // scalar: '0','½','2'
    const k=face==='0'?0:face==='½'?0.5:2;
    const sMe=sumElems(cMe), sFr=sumElems(cFr);
    scoreMe=Math.round(k*sMe*100)/100;
    scoreFr=Math.round(k*sFr*100)/100;
    htmlMe=mkScalarHtml(face,k,cMe,sMe,scoreMe);
    htmlFr=mkScalarHtml(face,k,cFr,sFr,scoreFr);
  }

  return {scoreMe, scoreFr, htmlMe, htmlFr};
}

function mkEqHtml(A, op, B, result){
  return `<div class="eq-row">
    ${fmtMat(A,'gold')}
    <span class="opsm">${op}</span>
    ${fmtMat(B,'purple')}
    <span class="eqsm">=</span>
    ${fmtMat(result,'green')}
  </div>
  <div style="font-size:.72rem;color:#475569">결과 크기: ${result.shape.join('×')}</div>`;
}

function mkScalarHtml(face, k, card, s, score){
  return `<div class="eq-row">
    <span class="scalar-k">${face}</span>
    <span class="opsm">×</span>
    ${fmtMat(card,'gold')}
  </div>
  <div class="sum-line">${face} × (성분 합 ${s}) = <span class="sum-val">${score}</span>점</div>`;
}

/* ═══ CARD GRID ═══ */
function buildCardGrid(){
  document.getElementById('card-grid').innerHTML = CARDS.map(c=>{
    const cols=c.shape[1];
    const cells=c.data.map(row=>row.map(v=>`<div class="mc">${v}</div>`).join('')).join('');
    return `<div class="crd" id="crd-${c.id}" onclick="selectCard(${c.id})">
      <div class="clbl" id="clbl-${c.id}">카드${c.id+1}</div>
      <span class="mat-i" style="color:#64748b">
        <span class="mi-bl"></span>
        <span class="mi-g" style="grid-template-columns:repeat(${cols},28px)">${cells}</span>
        <span class="mi-br"></span>
      </span>
      <div class="cshp">${c.shape.join('×')}</div>
    </div>`;
  }).join('');
}

/* ═══ CARD SELECTION ═══ */
function selectCard(id){
  if(usedCards.has(id)||roundDone) return;
  if(pickState==='me'){
    if(selMe!==null){
      document.getElementById(`crd-${selMe}`).classList.remove('sel-me');
      const l=document.getElementById(`clbl-${selMe}`); l.textContent=`카드${selMe+1}`; l.className='clbl';
    }
    selMe=id;
    const el=document.getElementById(`crd-${id}`);
    el.classList.add('sel-me');
    const l=document.getElementById(`clbl-${id}`); l.textContent='👤 나'; l.className='clbl me';
    pickState='fr';
    document.getElementById('rsub').textContent='친구 카드를 선택하세요';
  } else if(pickState==='fr'){
    if(id===selMe) return;
    if(selFr!==null){
      document.getElementById(`crd-${selFr}`).classList.remove('sel-fr');
      const l=document.getElementById(`clbl-${selFr}`); l.textContent=`카드${selFr+1}`; l.className='clbl';
    }
    selFr=id;
    const el=document.getElementById(`crd-${id}`);
    el.classList.add('sel-fr');
    const l=document.getElementById(`clbl-${id}`); l.textContent='👥 친구'; l.className='clbl fr';
    pickState='done';
    document.getElementById('rsub').textContent='주사위를 굴리세요!';
    document.getElementById('btn-roll').disabled=false;
  }
}

/* ═══ DICE ROLL ═══ */
function rollDice(){
  document.getElementById('btn-roll').disabled=true;
  const el=document.getElementById('die-face');
  el.className='die-face rolling';
  let t=0;
  const timer=setInterval(()=>{
    el.textContent=FACES[Math.floor(Math.random()*6)];
    t++;
    if(t>12){
      clearInterval(timer);
      currentFace=FACES[Math.floor(Math.random()*6)];
      el.textContent=currentFace;
      el.className='die-face '+(isOp(currentFace)?'rolled-op':'rolled-num');
      document.getElementById('die-label').textContent=isOp(currentFace)?'연산 주사위':'실수배 주사위';
      showResult();
    }
  },70);
}
function isOp(f){ return f==='+'||f==='−'||f==='×'; }

/* ═══ SHOW RESULT ═══ */
function showResult(){
  const cMe=CARDS[selMe], cFr=CARDS[selFr];
  const {scoreMe, scoreFr, htmlMe, htmlFr}=calcRound(cMe, cFr, currentFace);

  document.getElementById('pbody-me').innerHTML=htmlMe;
  document.getElementById('pbody-fr').innerHTML=htmlFr;
  document.getElementById('pscore-me').textContent=`+${scoreMe}점`;
  document.getElementById('pscore-fr').textContent=`+${scoreFr}점`;

  // round winner
  let rw='tie';
  if(scoreMe>scoreFr){rw='me'; winsMe++;}
  else if(scoreFr>scoreMe){rw='fr'; winsFr++;}
  const wb=document.getElementById('rw-banner');
  wb.className='rw-banner '+rw;
  wb.textContent=rw==='me'?'👤 나의 라운드!':rw==='fr'?'👥 친구의 라운드!':'🤝 이번 라운드 동점!';

  // update totals
  totalMe+=scoreMe; totalFr+=scoreFr;
  document.getElementById('score-me').textContent=totalMe;
  document.getElementById('score-fr').textContent=totalFr;
  document.getElementById('wins-me').textContent=winsMe+'승';
  document.getElementById('wins-fr').textContent=winsFr+'승';

  // context
  const ctxMap={'+':'덧셈: A+B (순서 무관)','-':'뺄셈: 나=A−B, 친구=B−A','×':'곱셈: 나=A×B, 친구=B×A',
    '0':'실수배 0: 모든 성분 × 0','½':'실수배 ½: 모든 성분 × ½','2':'실수배 2: 모든 성분 × 2'};
  document.getElementById('az-ctx').textContent=ctxMap[currentFace]||currentFace;

  histData.push({round, face:currentFace, me:scoreMe, fr:scoreFr, winner:rw});

  document.getElementById('czn').classList.add('show');
  roundDone=true;
  document.getElementById('btn-confirm').disabled=false;
  if(scoreMe!==scoreFr) particles();
}

/* ═══ ROUND CONTROL ═══ */
function confirmRound(){
  document.getElementById('btn-confirm').disabled=true;
  renderHistory();
  if(round>=6){
    setTimeout(showFinal,600);
  } else {
    document.getElementById('btn-next').style.display='inline-block';
  }
  if(round>=6||totalMe!==totalFr) particles();
}

function nextRound(){
  usedCards.add(selMe); usedCards.add(selFr);
  document.getElementById(`crd-${selMe}`).classList.add('used');
  document.getElementById(`crd-${selFr}`).classList.add('used');
  document.getElementById(`crd-${selMe}`).classList.remove('sel-me');
  document.getElementById(`crd-${selFr}`).classList.remove('sel-fr');

  selMe=selFr=null; currentFace=null; roundDone=false; pickState='me'; round++;

  document.getElementById('rbadge').textContent=`라운드 ${round} / 6`;
  document.getElementById('rsub').textContent='카드를 선택하세요';
  document.getElementById('die-face').textContent='?';
  document.getElementById('die-face').className='die-face';
  document.getElementById('die-label').textContent='주사위';
  document.getElementById('az-ctx').textContent='카드를 2장 선택한 후 주사위를 굴리세요.';
  document.getElementById('czn').classList.remove('show');
  document.getElementById('btn-roll').disabled=true;
  document.getElementById('btn-confirm').disabled=true;
  document.getElementById('btn-next').style.display='none';

  // reset card labels for unused cards
  CARDS.forEach(c=>{
    if(!usedCards.has(c.id)){
      const l=document.getElementById(`clbl-${c.id}`);
      if(l){ l.textContent=`카드${c.id+1}`; l.className='clbl'; }
    }
  });
}

function renderHistory(){
  const wrap=document.getElementById('hist');
  wrap.style.display='block';
  document.getElementById('hist-rows').innerHTML=histData.map(h=>`
    <div class="hr">
      <span class="h-rnd">R${h.round}</span>
      <span class="h-face">${h.face}</span>
      <span style="color:#475569;font-size:.7rem">나</span>
      <span class="h-me">${h.me}pt</span>
      <span style="color:#475569;font-size:.7rem">친구</span>
      <span class="h-fr">${h.fr}pt</span>
      <span class="h-win ${h.winner}">${h.winner==='me'?'내 승':h.winner==='fr'?'친구 승':'동점'}</span>
    </div>`).join('');
}

/* ═══ FINAL ═══ */
function showFinal(){
  document.getElementById('final').classList.add('show');
  document.getElementById('f-me').textContent=totalMe;
  document.getElementById('f-fr').textContent=totalFr;
  document.getElementById('f-wins-me').textContent=winsMe+'라운드 승';
  document.getElementById('f-wins-fr').textContent=winsFr+'라운드 승';
  let trophy,title,sub,tc;
  if(totalMe>totalFr){trophy='🏆';title='내가 승리!';sub=`${totalMe} : ${totalFr}`;tc='#93c5fd';}
  else if(totalFr>totalMe){trophy='🥈';title='친구의 승리!';sub=`${totalMe} : ${totalFr}`;tc='#f9a8d4';}
  else{trophy='🤝';title='무승부!';sub=`${totalMe} : ${totalFr}`;tc='#fbbf24';}
  document.getElementById('f-trophy').textContent=trophy;
  document.getElementById('f-title').textContent=title;
  document.getElementById('f-title').style.color=tc;
  document.getElementById('f-sub').textContent=sub;
  particles(); particles();
}

function restartGame(){
  totalMe=totalFr=winsMe=winsFr=0; round=1;
  usedCards.clear(); selMe=selFr=null; currentFace=null;
  roundDone=false; pickState='me'; histData=[];
  ['score-me','score-fr'].forEach(id=>document.getElementById(id).textContent=0);
  document.getElementById('wins-me').textContent='0승';
  document.getElementById('wins-fr').textContent='0승';
  document.getElementById('rbadge').textContent='라운드 1 / 6';
  document.getElementById('rsub').textContent='카드를 선택하세요';
  document.getElementById('die-face').textContent='?';
  document.getElementById('die-face').className='die-face';
  document.getElementById('die-label').textContent='주사위';
  document.getElementById('az-ctx').textContent='카드를 2장 선택한 후 주사위를 굴리세요.';
  document.getElementById('czn').classList.remove('show');
  document.getElementById('btn-roll').disabled=true;
  document.getElementById('btn-confirm').disabled=true;
  document.getElementById('btn-next').style.display='none';
  document.getElementById('hist').style.display='none';
  document.getElementById('hist-rows').innerHTML='';
  document.getElementById('final').classList.remove('show');
  buildCardGrid();
}

/* ═══ TABS & PARTICLES ═══ */
function switchTab(tab){
  ['rule','game'].forEach(t=>{
    document.getElementById('panel-'+t).classList.toggle('on',t===tab);
    document.getElementById('tb-'+t).classList.toggle('on',t===tab);
  });
}
function particles(){
  const cols=['#22c55e','#fbbf24','#38bdf8','#a78bfa','#f87171','#fb923c'];
  const cx=window.innerWidth/2,cy=220;
  for(let i=0;i<20;i++){
    const p=document.createElement('div'); p.className='pt';
    const ang=Math.random()*Math.PI*2,dist=80+Math.random()*140;
    p.style.cssText=`left:${cx}px;top:${cy}px;background:${cols[Math.floor(Math.random()*cols.length)]};`+
      `width:${5+Math.random()*6}px;height:${5+Math.random()*6}px;`+
      `--tx:${Math.cos(ang)*dist}px;--ty:${Math.sin(ang)*dist-60}px;`+
      `animation-delay:${Math.random()*.15}s`;
    document.body.appendChild(p);
    setTimeout(()=>p.remove(),1200);
  }
}

/* ═══ INIT ═══ */
buildCardGrid();
</script>
</body>
</html>"""


def render():
    st.markdown("### 🎲 행렬 카드 주사위 게임")
    st.caption("6면 주사위(+, −, ×, 0, ½, 2)로 승부! × 주사위는 나=A×B, 친구=B×A로 점수가 달라져요.")
    components.html(_HTML, height=1500, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
