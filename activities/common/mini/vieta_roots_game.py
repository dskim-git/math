# activities/common/mini/vieta_roots_game.py
"""
근과 계수의 관계 & 두 수를 근으로 하는 이차방정식
이차방정식의 두 근이 계수와 어떻게 연결되는지를
4단계 인터랙티브 활동으로 탐구합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "근과계수의관계"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "vieta_설명",
        "label":  "이차방정식 ax²+bx+c=0의 두 근을 α, β라 할 때, α+β와 αβ를 a, b, c로 나타내고, 이 관계가 성립하는 이유를 인수분해 형태와 연결하여 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "역방향_이해",
        "label":  "두 수 p, q를 근으로 하고 x²의 계수가 1인 이차방정식을 만들 때, '두 근의 합'과 '두 근의 곱'이 각각 어떤 계수가 되는지 설명하고, 이것이 근과 계수의 관계와 어떻게 연결되는지 서술하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "활용전략",
        "label":  "2x²−3x−6=0의 두 근을 α, β라 할 때, α³+β³의 값을 근과 계수의 관계를 이용하여 구하세요. (풀이 과정을 서술하세요)",
        "type":   "text_area",
        "height": 110,
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
    "title":       "🔑 근과 계수의 관계 탐정단",
    "description": "이차방정식의 두 근과 계수의 관계, 두 수를 근으로 하는 이차방정식을 4단계 인터랙티브 활동으로 탐구합니다.",
    "order":       220,
    "hidden":      False,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>근과 계수의 관계 탐정단</title>
<style>
html{font-size:17px}
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(150deg,#0a0a1a 0%,#0d1b3e 50%,#0a1a0a 100%);
  color:#e2e8ff;
  padding:12px 10px 30px;
}

/* ── 상단 진행 탭 ── */
.tabs{display:flex;gap:4px;margin-bottom:16px;border-bottom:2px solid rgba(255,255,255,.1);padding-bottom:6px}
.tab{
  flex:1;padding:8px 4px;border:none;border-radius:8px 8px 0 0;
  background:rgba(255,255,255,.05);color:#94a3b8;font-size:.78rem;font-weight:700;
  cursor:pointer;transition:.25s;font-family:inherit;
}
.tab.active{background:linear-gradient(135deg,#7c3aed,#1d4ed8);color:#fff}
.tab.done{background:rgba(16,185,129,.15);color:#6ee7b7}
.tab:hover:not(.active){background:rgba(255,255,255,.1);color:#c4b5fd}

/* ── 화면 전환 ── */
.screen{display:none;animation:fadeIn .3s ease}
.screen.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

/* ── 카드 ── */
.card{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.12);
  border-radius:14px;padding:18px 16px;margin-bottom:14px;
}
.card-title{
  font-size:.75rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;
  color:#a78bfa;margin-bottom:10px;
}
.hero{
  background:linear-gradient(135deg,rgba(124,58,237,.2),rgba(29,78,216,.2));
  border:1px solid rgba(124,58,237,.4);
  border-radius:14px;padding:16px;margin-bottom:16px;text-align:center;
}
.hero h2{font-size:1.3rem;color:#c4b5fd;margin-bottom:6px}
.hero p{color:#94a3b8;font-size:.88rem;line-height:1.6}

/* ── 수식 강조 ── */
.eq{
  background:rgba(0,0,0,.3);border-radius:10px;padding:12px 16px;
  font-size:1.1rem;text-align:center;margin:10px 0;line-height:2;
  border:1px solid rgba(255,255,255,.08);
}
.hl-purple{color:#c4b5fd;font-weight:700}
.hl-yellow{color:#fde68a;font-weight:700}
.hl-green{color:#6ee7b7;font-weight:700}
.hl-pink{color:#f9a8d4;font-weight:700}

/* ── 버튼 ── */
.btn{
  padding:9px 20px;border:none;border-radius:8px;font-size:.9rem;font-weight:700;
  cursor:pointer;transition:.2s;font-family:inherit;
}
.btn-primary{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff}
.btn-primary:hover{transform:translateY(-1px);filter:brightness(1.15)}
.btn-success{background:linear-gradient(135deg,#059669,#0d9488);color:#fff}
.btn-success:hover{transform:translateY(-1px);filter:brightness(1.15)}
.btn-outline{background:transparent;border:1.5px solid #6d28d9;color:#a78bfa}
.btn-outline:hover{background:rgba(109,40,217,.2)}

/* ── 입력창 ── */
input.blank{
  width:72px;padding:6px 8px;background:rgba(255,255,255,.08);
  border:2px solid #6d28d9;border-radius:8px;color:#fff;
  font-size:1rem;text-align:center;font-family:inherit;
  outline:none;transition:.2s;
}
input.blank:focus{border-color:#a78bfa;background:rgba(255,255,255,.12)}
input.blank.correct{border-color:#10b981;background:rgba(16,185,129,.12);color:#6ee7b7}
input.blank.wrong{border-color:#ef4444;background:rgba(239,68,68,.1);color:#fca5a5;animation:shake .3s}

@keyframes shake{0%,100%{transform:none}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}

/* ── 피드백 ── */
.fb{margin-top:8px;padding:10px 14px;border-radius:8px;font-size:.88rem;line-height:1.6;display:none}
.fb.ok{display:block;background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.35);color:#6ee7b7}
.fb.err{display:block;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);color:#fca5a5}
.fb.info{display:block;background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.35);color:#c4b5fd}

/* ── Step1: 인수분해 연결 ── */
.factor-box{
  display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;
  font-size:1.05rem;margin:14px 0;
}
.fpart{
  padding:8px 14px;border-radius:10px;border:2px solid transparent;
  transition:.4s;cursor:default;font-weight:700;text-align:center;
}
.fpart.reveal{animation:popIn .4s cubic-bezier(.34,1.56,.64,1) forwards}
@keyframes popIn{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:scale(1)}}
.fpart-a{border-color:#7c3aed;color:#c4b5fd;background:rgba(124,58,237,.15)}
.fpart-b{border-color:#0d9488;color:#6ee7b7;background:rgba(13,148,136,.15)}
.fpart-c{border-color:#d97706;color:#fde68a;background:rgba(217,119,6,.15)}
.arrow-down{font-size:1.8rem;color:#6d28d9;margin:4px 0;text-align:center}
.conn-line{
  height:2px;width:80px;background:linear-gradient(90deg,#7c3aed,#0d9488);
  border-radius:1px;display:inline-block;vertical-align:middle;margin:0 4px;
}

/* ── Step2: 계산 카드 ── */
.calc-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0}
.calc-label{font-size:.95rem;color:#94a3b8;min-width:200px}
.step-hint{
  font-size:.8rem;color:#64748b;line-height:1.6;margin-top:6px;
  background:rgba(0,0,0,.2);border-radius:6px;padding:8px 10px;
}
.hint-toggle{
  font-size:.8rem;color:#7c3aed;cursor:pointer;text-decoration:underline;
  display:inline-block;margin-top:4px;background:none;border:none;font-family:inherit;
}
.sub-step{margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,.07)}
.sub-step:last-child{border-bottom:none}

/* ── Step3: 방정식 만들기 ── */
.make-eq{
  display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:1.05rem;margin:12px 0;
}
.make-eq span{color:#94a3b8}
.badge-root{
  background:rgba(124,58,237,.2);border:1.5px solid #7c3aed;
  border-radius:20px;padding:4px 14px;color:#c4b5fd;font-weight:700;
  white-space:nowrap;
}

/* ── Step4: 퀴즈 ── */
.choices{display:flex;flex-direction:column;gap:8px;margin-top:12px}
.choice-btn{
  padding:10px 16px;border:2px solid rgba(255,255,255,.1);
  border-radius:10px;background:rgba(255,255,255,.04);
  color:#e2e8ff;font-size:.95rem;cursor:pointer;text-align:left;
  transition:.2s;font-family:inherit;
}
.choice-btn:hover:not(:disabled){background:rgba(124,58,237,.15);border-color:#7c3aed}
.choice-btn.correct{border-color:#10b981;background:rgba(16,185,129,.12);color:#6ee7b7}
.choice-btn.wrong{border-color:#ef4444;background:rgba(239,68,68,.1);color:#fca5a5}

/* ── 점수 뱃지 ── */
.score-wrap{
  display:flex;align-items:center;justify-content:space-between;
  background:rgba(255,255,255,.04);border-radius:10px;padding:8px 14px;margin-bottom:14px;
}
.score-text{font-size:.85rem;color:#94a3b8}
.score-num{font-size:1.1rem;font-weight:800;color:#fde68a}
.progress-bar{flex:1;height:8px;background:rgba(255,255,255,.08);border-radius:4px;
  margin:0 12px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,#7c3aed,#0d9488);transition:.4s}

/* ── 완료 배너 ── */
.complete-banner{
  text-align:center;padding:20px;background:linear-gradient(135deg,rgba(16,185,129,.15),rgba(13,148,136,.1));
  border:1px solid rgba(16,185,129,.3);border-radius:14px;margin-top:10px;
}
.complete-banner h3{color:#6ee7b7;font-size:1.3rem;margin-bottom:8px}
.complete-banner p{color:#94a3b8;font-size:.9rem}
.star{display:inline-block;animation:spin 1s ease}
@keyframes spin{from{transform:rotate(0deg) scale(0)}to{transform:rotate(360deg) scale(1)}}
</style>
</head>
<body>

<!-- ── 탭 ── -->
<div class="tabs">
  <button class="tab active" id="tab0" onclick="goTab(0)">🔍 1단계<br><small>비밀 발견</small></button>
  <button class="tab" id="tab1" onclick="goTab(1)">🧮 2단계<br><small>계산 도장</small></button>
  <button class="tab" id="tab2" onclick="goTab(2)">🏗 3단계<br><small>방정식 건축</small></button>
  <button class="tab" id="tab3" onclick="goTab(3)">⚡ 4단계<br><small>스피드 퀴즈</small></button>
</div>

<!-- ════════════════════════════════════════════
     SCREEN 0 : 근과 계수 비밀 발견
════════════════════════════════════════════ -->
<div class="screen active" id="sc0">
  <div class="hero">
    <h2>🔍 이차방정식 속 숨겨진 비밀!</h2>
    <p>두 근 α, β가 방정식의 계수와 연결되어 있다?<br>
    인수분해 과정을 따라가며 비밀을 발견해봐요.</p>
  </div>

  <!-- 개념 박스 1: 인수분해로 이해하기 -->
  <div class="card">
    <div class="card-title">🧩 인수분해로 비밀 찾기</div>
    <p style="font-size:.9rem;color:#94a3b8;margin-bottom:10px">
      이차방정식 <span class="hl-purple">ax²+bx+c=0</span>의 두 근이 α, β이면,<br>
      인수분해하면 어떻게 될까요? 버튼을 눌러 단계별로 확인하세요!
    </p>

    <div id="factorStage">
      <!-- 시작식 -->
      <div class="eq">
        <span class="hl-purple">ax²+bx+c</span> = 0
      </div>
      <div class="arrow-down">↓</div>

      <!-- 단계 1: a로 묶기 -->
      <div class="eq" id="f1" style="opacity:.3;transition:.4s">
        <span class="hl-yellow">a</span>(<span class="hl-purple">x²</span> + <span class="hl-yellow">b/a</span>·x + <span class="hl-yellow">c/a</span>) = 0
      </div>
      <div class="arrow-down" id="f1arrow" style="opacity:.3;transition:.4s">↓</div>

      <!-- 단계 2: 인수분해 -->
      <div class="eq" id="f2" style="opacity:.3;transition:.4s">
        <span class="hl-yellow">a</span>(x − <span class="hl-green">α</span>)(x − <span class="hl-pink">β</span>) = 0
      </div>
      <div class="arrow-down" id="f2arrow" style="opacity:.3;transition:.4s">↓</div>

      <!-- 단계 3: 전개 -->
      <div class="eq" id="f3" style="opacity:.3;transition:.4s">
        <span class="hl-yellow">a</span>[x² − (<span class="hl-green">α</span>+<span class="hl-pink">β</span>)x + <span class="hl-green">α</span><span class="hl-pink">β</span>] = 0
      </div>
      <div class="arrow-down" id="f3arrow" style="opacity:.3;transition:.4s">↓</div>

      <!-- 단계 4: 계수 비교 -->
      <div class="card" id="f4" style="opacity:.3;transition:.4s;border-color:rgba(16,185,129,.4);background:rgba(16,185,129,.05)">
        <div class="card-title" style="color:#6ee7b7">✅ 계수 비교 → 근과 계수의 관계 완성!</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:6px">
          <div class="eq" style="background:rgba(124,58,237,.1);border-color:rgba(124,58,237,.3)">
            <span class="hl-green">α + β</span> = −<span class="hl-yellow">b/a</span>
          </div>
          <div class="eq" style="background:rgba(13,148,136,.1);border-color:rgba(13,148,136,.3)">
            <span class="hl-green">αβ</span> = <span class="hl-yellow">c/a</span>
          </div>
        </div>
        <p style="font-size:.82rem;color:#6ee7b7;text-align:center;margin-top:10px">
          두 근의 합 = −(x의 계수)/(x²의 계수) &nbsp;|&nbsp; 두 근의 곱 = (상수항)/(x²의 계수)
        </p>
      </div>
    </div>

    <div style="text-align:center;margin-top:12px">
      <button class="btn btn-primary" id="factorBtn" onclick="nextFactor()">다음 단계 →</button>
    </div>
    <div class="fb info" id="factorFb">
      이제 ax²+bx+c=0 ≡ a(x−α)(x−β)=0이므로,<br>
      전개하면 x²의 계수 비교: <strong>−(α+β) = b/a</strong>,
      상수항 비교: <strong>αβ = c/a</strong>가 됩니다!
    </div>
  </div>

  <!-- 직접 확인 -->
  <div class="card">
    <div class="card-title">✏️ 직접 확인해보기</div>
    <p style="font-size:.9rem;color:#94a3b8;margin-bottom:10px">
      이차방정식 <span class="hl-yellow">2x²−3x−6=0</span>에서 a=2, b=−3, c=−6일 때,<br>
      근과 계수의 관계로 두 근의 합과 곱을 구해보세요.
    </p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div>
        <div class="eq">α + β = −b/a = −(<span style="color:#f9a8d4">?</span>)/(<span style="color:#fde68a">?</span>)</div>
        <div class="calc-row" style="justify-content:center;margin-top:8px">
          <span style="color:#94a3b8">α+β =</span>
          <input class="blank" id="sumInput" type="text" placeholder="분수">
          <button class="btn btn-outline" onclick="checkSum()" style="padding:6px 12px">확인</button>
        </div>
        <div class="fb" id="sumFb"></div>
      </div>
      <div>
        <div class="eq">αβ = c/a = (<span style="color:#f9a8d4">?</span>)/(<span style="color:#fde68a">?</span>)</div>
        <div class="calc-row" style="justify-content:center;margin-top:8px">
          <span style="color:#94a3b8">αβ =</span>
          <input class="blank" id="prodInput" type="text" placeholder="값">
          <button class="btn btn-outline" onclick="checkProd()" style="padding:6px 12px">확인</button>
        </div>
        <div class="fb" id="prodFb"></div>
      </div>
    </div>
    <div class="fb" id="step0CompFb" style="margin-top:10px"></div>
  </div>

  <div style="text-align:right">
    <button class="btn btn-success" onclick="goTab(1)" id="go1Btn" style="display:none">2단계로 →</button>
  </div>
</div>

<!-- ════════════════════════════════════════════
     SCREEN 1 : 계산 도장 깨기
════════════════════════════════════════════ -->
<div class="screen" id="sc1">
  <div class="hero">
    <h2>🧮 계산 도장 깨기!</h2>
    <p><span class="hl-yellow">2x²−3x−6=0</span>의 두 근 α, β에 대해<br>
    α+β = 3/2, αβ = −3임을 이용하여 아래 식을 구하세요.</p>
  </div>

  <!-- (1) (α+1)(β+1) -->
  <div class="card">
    <div class="sub-step">
      <div class="card-title">📌 (1) (α+1)(β+1)</div>
      <div class="eq">(α+1)(β+1) = αβ + α + β + 1</div>
      <button class="hint-toggle" onclick="toggleHint('h1')">💡 힌트 보기</button>
      <div class="step-hint" id="h1" style="display:none">
        αβ + (α+β) + 1 = (−3) + (3/2) + 1 = ?
      </div>
      <div class="calc-row" style="margin-top:10px">
        <span class="calc-label">(α+1)(β+1) =</span>
        <input class="blank" id="c1" type="text" placeholder="분수">
        <button class="btn btn-outline" onclick="checkCalc(1)" style="padding:6px 12px">확인</button>
      </div>
      <div class="fb" id="fb1"></div>
    </div>

    <!-- (2) β/α + α/β -->
    <div class="sub-step">
      <div class="card-title">📌 (2) β/α + α/β</div>
      <div class="eq">β/α + α/β = (α²+β²)/(αβ) = <span class="hl-purple">[(α+β)²−2αβ]</span>/(αβ)</div>
      <button class="hint-toggle" onclick="toggleHint('h2')">💡 힌트 보기</button>
      <div class="step-hint" id="h2" style="display:none">
        α²+β² = (α+β)² − 2αβ = (3/2)² − 2×(−3) = 9/4 + 6 = 33/4<br>
        αβ = −3이므로 (33/4)/(−3) = ?
      </div>
      <div class="calc-row" style="margin-top:10px">
        <span class="calc-label">β/α + α/β =</span>
        <input class="blank" id="c2" type="text" placeholder="분수">
        <button class="btn btn-outline" onclick="checkCalc(2)" style="padding:6px 12px">확인</button>
      </div>
      <div class="fb" id="fb2"></div>
    </div>

    <!-- (3) (α-β)² -->
    <div class="sub-step">
      <div class="card-title">📌 (3) (α−β)²</div>
      <div class="eq">(α−β)² = (α+β)² − 4αβ</div>
      <button class="hint-toggle" onclick="toggleHint('h3')">💡 힌트 보기</button>
      <div class="step-hint" id="h3" style="display:none">
        (3/2)² − 4×(−3) = 9/4 + 12 = 9/4 + 48/4 = ?
      </div>
      <div class="calc-row" style="margin-top:10px">
        <span class="calc-label">(α−β)² =</span>
        <input class="blank" id="c3" type="text" placeholder="분수">
        <button class="btn btn-outline" onclick="checkCalc(3)" style="padding:6px 12px">확인</button>
      </div>
      <div class="fb" id="fb3"></div>
    </div>

    <!-- (4) α³+β³ -->
    <div class="sub-step">
      <div class="card-title">📌 (4) α³+β³</div>
      <div class="eq">α³+β³ = (α+β)³ − 3αβ(α+β)</div>
      <button class="hint-toggle" onclick="toggleHint('h4')">💡 힌트 보기</button>
      <div class="step-hint" id="h4" style="display:none">
        (3/2)³ − 3×(−3)×(3/2) = 27/8 + 27/2 = 27/8 + 108/8 = ?
      </div>
      <div class="calc-row" style="margin-top:10px">
        <span class="calc-label">α³+β³ =</span>
        <input class="blank" id="c4" type="text" placeholder="분수">
        <button class="btn btn-outline" onclick="checkCalc(4)" style="padding:6px 12px">확인</button>
      </div>
      <div class="fb" id="fb4"></div>
    </div>
  </div>

  <div id="step1Badges" style="display:none">
    <div class="fb ok" style="display:block;text-align:center;margin-bottom:10px">
      🎉 4문제를 모두 풀었어요! 근과 계수의 관계로 직접 근을 구하지 않아도 되네요!
    </div>
    <div style="text-align:right">
      <button class="btn btn-success" onclick="goTab(2)">3단계로 →</button>
    </div>
  </div>
</div>

<!-- ════════════════════════════════════════════
     SCREEN 2 : 방정식 건축
════════════════════════════════════════════ -->
<div class="screen" id="sc2">
  <div class="hero">
    <h2>🏗 방정식 건축가!</h2>
    <p>이번엔 역방향! 두 수가 주어졌을 때<br>
    <span class="hl-purple">x² − (두 근의 합)x + (두 근의 곱) = 0</span><br>
    공식을 이용해 이차방정식을 완성하세요.</p>
  </div>

  <!-- 공식 카드 -->
  <div class="card" style="border-color:rgba(124,58,237,.4);background:rgba(124,58,237,.05)">
    <div class="card-title">📐 공식 정리</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
      <div class="eq" style="font-size:.95rem">
        두 근의 합<br><span class="hl-yellow">α+β = S</span>
      </div>
      <div class="eq" style="font-size:.95rem">
        두 근의 곱<br><span class="hl-green">αβ = P</span>
      </div>
    </div>
    <div class="eq" style="margin-top:10px;font-size:1.1rem;border-color:rgba(124,58,237,.4)">
      x² − <span class="hl-yellow">S</span>x + <span class="hl-green">P</span> = 0
    </div>
  </div>

  <!-- 문제 1 -->
  <div class="card" id="m1card">
    <div class="card-title">📌 문제 1</div>
    <p style="margin-bottom:10px;font-size:.95rem">
      두 수 <span class="badge-root">−4</span> 와 <span class="badge-root">3</span> 을 근으로 하고 x²의 계수가 1인 이차방정식
    </p>
    <div style="font-size:.88rem;color:#94a3b8;margin-bottom:10px;line-height:1.8">
      합: (−4) + 3 = <span class="hl-yellow">?</span> &nbsp;|&nbsp; 곱: (−4) × 3 = <span class="hl-green">?</span>
    </div>
    <div class="make-eq">
      <span>x²</span>
      <span>−</span>
      <span>(</span>
      <input class="blank" id="m1s" type="number" placeholder="S" style="width:60px">
      <span>)x</span>
      <span>+</span>
      <span>(</span>
      <input class="blank" id="m1p" type="number" placeholder="P" style="width:60px">
      <span>)</span>
      <span>= 0</span>
    </div>
    <button class="btn btn-outline" onclick="checkMake(1)" style="margin-top:6px">확인</button>
    <div class="fb" id="mfb1"></div>
  </div>

  <!-- 문제 2 -->
  <div class="card" id="m2card">
    <div class="card-title">📌 문제 2</div>
    <p style="margin-bottom:10px;font-size:.95rem">
      두 수 <span class="badge-root">2+√5</span> 와 <span class="badge-root">2−√5</span> 를 근으로 하고 x²의 계수가 1인 이차방정식
    </p>
    <div style="font-size:.88rem;color:#94a3b8;margin-bottom:10px;line-height:1.8">
      합: (2+√5) + (2−√5) = <span class="hl-yellow">?</span> &nbsp;|&nbsp; 곱: (2+√5)(2−√5) = 4−5 = <span class="hl-green">?</span>
    </div>
    <div class="make-eq">
      <span>x²</span>
      <span>−</span>
      <span>(</span>
      <input class="blank" id="m2s" type="number" placeholder="S" style="width:60px">
      <span>)x</span>
      <span>+</span>
      <span>(</span>
      <input class="blank" id="m2p" type="number" placeholder="P" style="width:60px">
      <span>)</span>
      <span>= 0</span>
    </div>
    <button class="btn btn-outline" onclick="checkMake(2)" style="margin-top:6px">확인</button>
    <div class="fb" id="mfb2"></div>
  </div>

  <!-- 문제 3 -->
  <div class="card" id="m3card">
    <div class="card-title">📌 문제 3</div>
    <p style="margin-bottom:10px;font-size:.95rem">
      두 수 <span class="badge-root">1+3i</span> 와 <span class="badge-root">1−3i</span> 를 근으로 하고 x²의 계수가 1인 이차방정식
    </p>
    <div style="font-size:.88rem;color:#94a3b8;margin-bottom:10px;line-height:1.8">
      합: (1+3i) + (1−3i) = <span class="hl-yellow">?</span> &nbsp;|&nbsp; 곱: (1+3i)(1−3i) = 1+9 = <span class="hl-green">?</span>
    </div>
    <div class="make-eq">
      <span>x²</span>
      <span>−</span>
      <span>(</span>
      <input class="blank" id="m3s" type="number" placeholder="S" style="width:60px">
      <span>)x</span>
      <span>+</span>
      <span>(</span>
      <input class="blank" id="m3p" type="number" placeholder="P" style="width:60px">
      <span>)</span>
      <span>= 0</span>
    </div>
    <button class="btn btn-outline" onclick="checkMake(3)" style="margin-top:6px">확인</button>
    <div class="fb" id="mfb3"></div>
  </div>

  <div id="step2Complete" style="display:none">
    <div class="fb ok" style="display:block;text-align:center;margin-bottom:10px">
      🏆 3문제 모두 완성! 이제 두 근 → 방정식을 자유자재로 만들 수 있어요!
    </div>
    <div style="text-align:right">
      <button class="btn btn-success" onclick="goTab(3)">마지막 퀴즈 →</button>
    </div>
  </div>
</div>

<!-- ════════════════════════════════════════════
     SCREEN 3 : 스피드 퀴즈
════════════════════════════════════════════ -->
<div class="screen" id="sc3">
  <div class="hero">
    <h2>⚡ 스피드 퀴즈!</h2>
    <p>배운 내용을 총정리해봐요.<br>각 문제를 빠르게 맞춰보세요!</p>
  </div>

  <div class="score-wrap">
    <span class="score-text">진행도</span>
    <div class="progress-bar"><div class="progress-fill" id="qProgress" style="width:0%"></div></div>
    <span class="score-num" id="qScore">0 / 5</span>
  </div>

  <div id="quizArea"></div>
  <div id="quizComplete" style="display:none">
    <div class="complete-banner">
      <div class="star" style="font-size:2.5rem">⭐</div>
      <h3 id="finalMsg"></h3>
      <p id="finalSub"></p>
    </div>
  </div>
</div>

<script>
/* ═══════════════════════════════
   탭 전환
═══════════════════════════════ */
const tabs=['tab0','tab1','tab2','tab3'];
const screens=['sc0','sc1','sc2','sc3'];
const done=[false,false,false,false];

function goTab(i){
  tabs.forEach((t,j)=>{
    const el=document.getElementById(t);
    el.classList.remove('active','done');
    if(j===i) el.classList.add('active');
    else if(done[j]) el.classList.add('done');
  });
  screens.forEach((s,j)=>{
    document.getElementById(s).classList.toggle('active',j===i);
  });
  if(i===3 && !quizStarted) initQuiz();
  schedResize(100);
}

function schedResize(ms){
  setTimeout(()=>{
    const h=document.body.scrollHeight;
    window.parent.postMessage({type:'streamlit:setFrameHeight',height:h+20},'*');
  },ms);
}

/* ═══════════════════════════════
   SCREEN 0
═══════════════════════════════ */
let factorStep=0;
const FACTOR_GROUPS=[
  ['f1','f1arrow'],
  ['f2','f2arrow'],
  ['f3','f3arrow'],
  ['f4'],
];
function nextFactor(){
  if(factorStep>=FACTOR_GROUPS.length) return;
  FACTOR_GROUPS[factorStep].forEach(id=>{
    const el=document.getElementById(id);
    if(el){el.style.opacity='1';el.classList.add('reveal');}
  });
  factorStep++;
  if(factorStep>=FACTOR_GROUPS.length){
    document.getElementById('factorBtn').style.display='none';
    document.getElementById('factorFb').classList.add('info');
    document.getElementById('factorFb').style.display='block';
    schedResize(200);
  }
  schedResize(100);
}

let sumOk=false, prodOk=false;

function normalize(s){
  // Allow "3/2", "-3", "1.5" etc.
  s=s.trim().replace(/\s/g,'');
  // convert fraction to decimal
  const m=s.match(/^(-?\d+)\/(-?\d+)$/);
  if(m) return parseFloat(m[1])/parseFloat(m[2]);
  return parseFloat(s);
}

function checkSum(){
  const v=normalize(document.getElementById('sumInput').value);
  const fb=document.getElementById('sumFb');
  const inp=document.getElementById('sumInput');
  // α+β = -b/a = -(-3)/2 = 3/2
  if(Math.abs(v-1.5)<0.01){
    inp.classList.add('correct');
    fb.className='fb ok';
    fb.textContent='✅ 정확해요! α+β = −(−3)/2 = 3/2';
    sumOk=true;
    checkStep0();
  } else {
    inp.classList.add('wrong');
    setTimeout(()=>inp.classList.remove('wrong'),400);
    fb.className='fb err';
    fb.textContent='❌ 다시 생각해봐요. α+β = −b/a = −(−3)/2 = ?';
  }
  schedResize(100);
}

function checkProd(){
  const v=normalize(document.getElementById('prodInput').value);
  const fb=document.getElementById('prodFb');
  const inp=document.getElementById('prodInput');
  // αβ = c/a = -6/2 = -3
  if(Math.abs(v-(-3))<0.01){
    inp.classList.add('correct');
    fb.className='fb ok';
    fb.textContent='✅ 맞아요! αβ = c/a = (−6)/2 = −3';
    prodOk=true;
    checkStep0();
  } else {
    inp.classList.add('wrong');
    setTimeout(()=>inp.classList.remove('wrong'),400);
    fb.className='fb err';
    fb.textContent='❌ 다시 생각해봐요. αβ = c/a = (−6)/2 = ?';
  }
  schedResize(100);
}

function checkStep0(){
  if(sumOk && prodOk){
    done[0]=true;
    document.getElementById('tab0').classList.add('done');
    const fb=document.getElementById('step0CompFb');
    fb.className='fb ok';
    fb.style.display='block';
    fb.textContent='🎉 완벽해요! α+β=3/2, αβ=−3을 기억하세요. 2단계에서 활용합니다!';
    document.getElementById('go1Btn').style.display='inline-block';
    schedResize(100);
  }
}

/* ═══════════════════════════════
   SCREEN 1 — 계산 도장
═══════════════════════════════ */
// 정답: (1) -1/2, (2) -11/4, (3) 57/4, (4) 135/8
const CALC_ANS=[null, -0.5, -2.75, 14.25, 16.875];
const CALC_ANS_STR=[null,'−1/2','−11/4','57/4','135/8'];
const CALC_EXP=[null,
  'αβ+(α+β)+1 = (−3)+(3/2)+1 = −3+5/2 = −1/2',
  '(α²+β²)/(αβ) = [(3/2)²−2×(−3)]/(−3) = [9/4+6]/(−3) = (33/4)/(−3) = −11/4',
  '(α+β)²−4αβ = (3/2)²−4×(−3) = 9/4+12 = 57/4',
  '(α+β)³−3αβ(α+β) = (3/2)³−3×(−3)×(3/2) = 27/8+27/2 = 135/8'
];
let calcDone=0;
const calcOk=[false,false,false,false,false];

function toggleHint(id){
  const el=document.getElementById(id);
  el.style.display=el.style.display==='none'?'block':'none';
  schedResize(80);
}

function checkCalc(n){
  const v=normalize(document.getElementById('c'+n).value);
  const fb=document.getElementById('fb'+n);
  const inp=document.getElementById('c'+n);
  if(Math.abs(v-CALC_ANS[n])<0.02){
    inp.classList.add('correct');
    fb.className='fb ok';
    fb.textContent='✅ 정답! '+CALC_ANS_STR[n]+' — '+CALC_EXP[n];
    if(!calcOk[n]){ calcOk[n]=true; calcDone++; }
    if(calcDone>=4){
      done[1]=true;
      document.getElementById('tab1').classList.add('done');
      document.getElementById('step1Badges').style.display='block';
    }
  } else {
    inp.classList.add('wrong');
    setTimeout(()=>inp.classList.remove('wrong'),400);
    fb.className='fb err';
    fb.textContent='❌ 틀렸어요. 힌트를 참고해서 다시 계산해보세요!';
  }
  schedResize(100);
}

/* ═══════════════════════════════
   SCREEN 2 — 방정식 만들기
═══════════════════════════════ */
// 문제1: 근 -4,3 → S=-1, P=-12 → x²-(-1)x+(-12)=0 → x²+x-12=0
// x² - S*x + P = 0, 입력값은 S와 P
// 문제1: S=-4+3=-1, P=-4*3=-12
// 문제2: S=4, P=-1
// 문제3: S=2, P=10
const MAKE_ANS=[null,{s:-1,p:-12},{s:4,p:-1},{s:2,p:10}];
const MAKE_EXP=[null,
  '합: (−4)+3=−1, 곱: (−4)×3=−12 → x²−(−1)x+(−12)=0 즉 x²+x−12=0',
  '합: (2+√5)+(2−√5)=4, 곱: (2+√5)(2−√5)=4−5=−1 → x²−4x+(−1)=0 즉 x²−4x−1=0',
  '합: (1+3i)+(1−3i)=2, 곱: (1+3i)(1−3i)=1+9=10 → x²−2x+10=0'
];
let makeDone=0;
const makeOk=[false,false,false,false];

function checkMake(n){
  const sv=parseFloat(document.getElementById('m'+n+'s').value);
  const pv=parseFloat(document.getElementById('m'+n+'p').value);
  const fb=document.getElementById('mfb'+n);
  const ans=MAKE_ANS[n];
  const isOk=Math.abs(sv-ans.s)<0.01 && Math.abs(pv-ans.p)<0.01;
  if(isOk){
    document.getElementById('m'+n+'s').classList.add('correct');
    document.getElementById('m'+n+'p').classList.add('correct');
    fb.className='fb ok';
    fb.textContent='✅ 정확해요! '+MAKE_EXP[n];
    if(!makeOk[n]){ makeOk[n]=true; makeDone++; }
    if(makeDone>=3){
      done[2]=true;
      document.getElementById('tab2').classList.add('done');
      document.getElementById('step2Complete').style.display='block';
    }
  } else {
    document.getElementById('m'+n+'s').classList.add('wrong');
    document.getElementById('m'+n+'p').classList.add('wrong');
    setTimeout(()=>{
      document.getElementById('m'+n+'s').classList.remove('wrong');
      document.getElementById('m'+n+'p').classList.remove('wrong');
    },400);
    fb.className='fb err';
    fb.textContent='❌ 다시 계산해봐요. S(합)과 P(곱)를 먼저 구해보세요!';
  }
  schedResize(100);
}

/* ═══════════════════════════════
   SCREEN 3 — 퀴즈
═══════════════════════════════ */
const QUIZ=[
  {
    q:'이차방정식 x²−5x+6=0의 두 근을 α, β라 할 때, α+β의 값은?',
    choices:['5','−5','6','−6'],
    ans:0,
    tip:'근과 계수의 관계: α+β = −b/a = −(−5)/1 = 5'
  },
  {
    q:'이차방정식 3x²+6x−9=0의 두 근의 곱(αβ)은?',
    choices:['−3','3','−2','2'],
    ans:0,
    tip:'αβ = c/a = (−9)/3 = −3'
  },
  {
    q:'두 수 −2와 5를 근으로 하는 이차방정식(x²의 계수=1)은?',
    choices:['x²−3x−10=0','x²+3x−10=0','x²−3x+10=0','x²+3x+10=0'],
    ans:1,
    tip:'합: −2+5=3, 곱: (−2)×5=−10 → x²−3x+(−10)=0 = x²−3x−10=0? 아니요, x²−(합)x+(곱)=0 → x²−3x+(−10)=0. 잠깐, 선택지 확인: x²+3x−10이면 합이 −3이므로 틀림. x²−3x−10=0이면 합이 3, 곱이 −10 ✅'
  },
  {
    q:'x²+4x+1=0의 두 근 α, β에 대해 α²+β²의 값은?',
    choices:['14','16','18','20'],
    ans:0,
    tip:'α+β=−4, αβ=1 → α²+β²=(α+β)²−2αβ=16−2=14'
  },
  {
    q:'두 수 3+i와 3−i를 근으로 하는 이차방정식(x²의 계수=1)에서 상수항은?',
    choices:['10','9','8','6'],
    ans:0,
    tip:'곱: (3+i)(3−i)=9+1=10 → 상수항=αβ=10'
  }
];
// 문제 3 정답 수정: x²−3x−10=0
// 선택지0: x²−3x−10=0 (합=3, 곱=−10) ✅
QUIZ[2].ans=0;
QUIZ[2].choices=['x²−3x−10=0','x²+3x−10=0','x²−3x+10=0','x²+3x+10=0'];
QUIZ[2].tip='합: (−2)+5=3, 곱: (−2)×5=−10 → x²−3x+(−10)=0 즉 x²−3x−10=0';

let qIdx=0, qScore=0, qAnswered=false, quizStarted=false;

function initQuiz(){
  quizStarted=true;
  renderQ();
}

function renderQ(){
  if(qIdx>=QUIZ.length){
    document.getElementById('quizArea').style.display='none';
    const comp=document.getElementById('quizComplete');
    comp.style.display='block';
    done[3]=true;
    document.getElementById('tab3').classList.add('done');
    const pct=Math.round(qScore/QUIZ.length*100);
    document.getElementById('finalMsg').textContent=
      pct===100?'🌟 완벽한 점수! 근과 계수의 관계 마스터!':
      pct>=80?'🎉 훌륭해요! 거의 다 맞췄어요!':
      pct>=60?'👍 잘했어요! 틀린 부분을 복습해봐요.':'💪 다시 도전해봐요!';
    document.getElementById('finalSub').textContent=
      `${qScore}/${QUIZ.length} 정답 (${pct}%) — 오답은 힌트를 확인하세요!`;
    schedResize(200);
    return;
  }
  const q=QUIZ[qIdx];
  document.getElementById('quizArea').innerHTML=`
    <div class="card">
      <div class="card-title">📌 문제 ${qIdx+1} / ${QUIZ.length}</div>
      <p style="font-size:.95rem;line-height:1.7;margin-bottom:14px">${q.q}</p>
      <div class="choices">
        ${q.choices.map((c,i)=>`
          <button class="choice-btn" id="qch${i}" onclick="pick(${i})">${c}</button>
        `).join('')}
      </div>
      <div class="fb" id="qfb"></div>
      <button class="btn btn-primary" id="qNextBtn" onclick="nextQ()"
        style="display:none;margin-top:10px">다음 문제 →</button>
    </div>`;
  qAnswered=false;
  updateQProgress();
  schedResize(100);
}

function pick(i){
  if(qAnswered) return;
  qAnswered=true;
  const q=QUIZ[qIdx];
  const fb=document.getElementById('qfb');
  for(let j=0;j<q.choices.length;j++){
    const btn=document.getElementById('qch'+j);
    btn.disabled=true;
    if(j===q.ans) btn.classList.add('correct');
    else if(j===i && i!==q.ans) btn.classList.add('wrong');
  }
  if(i===q.ans){
    qScore++;
    fb.className='fb ok';
    fb.textContent='✅ 정답! '+q.tip;
  } else {
    fb.className='fb err';
    fb.textContent='❌ 틀렸어요. '+q.tip;
  }
  document.getElementById('qNextBtn').style.display='inline-block';
  updateQProgress();
  schedResize(100);
}

function nextQ(){
  qIdx++;
  renderQ();
}

function updateQProgress(){
  const pct=(qIdx/QUIZ.length)*100;
  document.getElementById('qProgress').style.width=pct+'%';
  document.getElementById('qScore').textContent=qScore+' / '+QUIZ.length;
}

/* 초기 높이 */
schedResize(200);
</script>
</body>
</html>"""


def render():
    st.set_page_config(page_title="근과 계수의 관계 탐정단", layout="wide")
    st.markdown(
        "<style>.main{max-width:100%}iframe{width:100%!important}</style>",
        unsafe_allow_html=True,
    )
    components.html(_HTML, height=1900, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
