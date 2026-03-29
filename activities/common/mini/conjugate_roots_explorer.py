# activities/common/mini/conjugate_roots_explorer.py
"""
켤레근 탐정단 – 이차방정식의 켤레근 탐구
이차방정식의 켤레근(무리수·허수)이 생기는 이유를
개념 탐구 → 대입 증명 → 퀴즈 → 역추적의 4단계로 자연스럽게 이해하는 미니활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "켤레근탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "켤레근이유",
        "label":  "실수 계수 이차방정식 ax²+bx+c=0에서 한 근이 p+qi (q≠0)이면, 다른 한 근이 반드시 p−qi인 이유를 '복소수의 상등 조건'과 연결하여 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "조건중요성",
        "label":  "무리수 켤레근 법칙(p+q√m → p−q√m)이 성립하려면 계수가 반드시 유리수여야 합니다. 허수 켤레근 법칙(p+qi → p−qi)에서는 계수가 실수여야 하고요. '계수의 조건'이 왜 이렇게 중요한지, PPT에 나온 반례(계수가 무리수이거나 허수인 방정식)를 떠올리며 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "활용풀이",
        "label":  "이차방정식 x²+bx+c=0의 한 근이 3+2i일 때, b와 c의 값을 켤레근 성질을 이용하여 구하세요. (풀이 과정을 쓰세요)",
        "type":   "text_area",
        "height": 100,
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
    "title":       "🔮 켤레근 탐정단!",
    "description": "이차방정식의 켤레근(무리수·허수)이 생기는 이유를 탐구·대입 증명·퀴즈·역추적의 4단계로 이해하는 활동입니다.",
    "order":       210,
    "hidden":      False,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>켤레근 탐정단</title>
<style>
html{font-size:18px}
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Segoe UI',system-ui,sans-serif;
  background:linear-gradient(155deg,#080118 0%,#150838 55%,#081426 100%);
  color:#e2e8ff;padding:14px 12px 28px;font-size:1rem;
}

/* ── 단계 진행바 ── */
.stepbar{display:flex;gap:5px;margin-bottom:16px}
.sbar{flex:1;height:6px;border-radius:3px;background:rgba(255,255,255,.1);transition:.35s}
.sbar.done{background:#6d28d9}
.sbar.active{background:#a78bfa}

/* ── 화면 전환 ── */
.screen{display:none;animation:fadeIn .3s ease}
.screen.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}

/* ── 히어로 ── */
.hero{
  background:linear-gradient(135deg,rgba(109,40,217,.22),rgba(59,130,246,.12));
  border:1px solid rgba(167,139,250,.3);border-radius:16px;
  padding:14px 18px;margin-bottom:14px;text-align:center;
}
.hero h2{font-size:1.45rem;color:#c4b5fd;margin-bottom:5px}
.hero p{font-size:1rem;color:#a5b4fc;line-height:1.6}

/* ── 카드 ── */
.card{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:14px 16px;margin-bottom:12px;
}
.card-title{font-size:1.05rem;font-weight:700;margin-bottom:8px}

/* ── 태그 ── */
.tag{display:inline-block;font-size:.82rem;padding:2px 9px;border-radius:99px;font-weight:700;margin-bottom:6px}
.tag-rat{background:rgba(52,211,153,.18);color:#34d399;border:1px solid rgba(52,211,153,.35)}
.tag-real{background:rgba(196,181,253,.18);color:#c4b5fd;border:1px solid rgba(196,181,253,.35)}

/* ── 수식 ── */
.math{font-family:'Times New Roman',Georgia,serif;font-style:italic;color:#fde68a;font-size:1.05em}
.mblock{
  font-family:'Times New Roman',Georgia,serif;font-style:italic;color:#fde68a;
  background:rgba(253,230,138,.07);border:1px solid rgba(253,230,138,.18);
  border-radius:8px;padding:10px 14px;text-align:center;font-size:1.25rem;margin:8px 0;
  line-height:2;
}
.c1{color:#f0abfc;font-weight:700;font-family:'Times New Roman',serif;font-style:italic;font-size:1.05em}
.c2{color:#6ee7b7;font-weight:700;font-family:'Times New Roman',serif;font-style:italic;font-size:1.05em}
.re{color:#34d399;font-weight:700}
.im{color:#f0abfc;font-weight:700}

/* ── 계수 입력 계산기 ── */
.calc-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.coeff-in{
  width:66px;padding:6px 8px;border-radius:8px;text-align:center;
  background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);
  color:#e2e8ff;font-size:1.05rem;
}
.result-box{
  background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.3);
  border-radius:10px;padding:12px 14px;margin-top:8px;
  font-size:1rem;line-height:1.8;
}

/* ── 증명 단계 ── */
.step-box{
  background:rgba(255,255,255,.035);border-left:3px solid #7c3aed;
  border-radius:0 8px 8px 0;padding:10px 13px;margin-bottom:7px;
  display:none;animation:fadeIn .3s ease;
}
.step-box.show{display:block}
.step-lbl{font-size:.82rem;color:#a78bfa;font-weight:700;margin-bottom:5px;letter-spacing:.04em}
.step-eq{font-family:'Times New Roman',serif;font-size:1.2rem;color:#fde68a;margin:4px 0;line-height:1.7}

/* ── 퀴즈 ── */
.quiz-meta{display:flex;justify-content:space-between;font-size:.9rem;color:#64748b;margin-bottom:8px}
.quiz-eq{font-size:1.1rem;margin-bottom:5px;line-height:1.65}
.quiz-hint{font-size:1rem;color:#93c5fd;margin-bottom:12px}
.choices{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:8px}
@media(max-width:500px){.choices{grid-template-columns:1fr}}
.choice{
  padding:12px 8px;border-radius:10px;text-align:center;cursor:pointer;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  font-family:'Times New Roman',serif;font-style:italic;font-size:1.1rem;
  color:#e2e8ff;transition:.18s;user-select:none;
}
.choice:hover:not(.locked){background:rgba(124,58,237,.28);border-color:#7c3aed}
.choice.correct{background:rgba(52,211,153,.2);border-color:#34d399;color:#34d399;cursor:default}
.choice.wrong{background:rgba(239,68,68,.18);border-color:#ef4444;color:#ef4444;cursor:default}
.choice.reveal{background:rgba(52,211,153,.1);border-color:#34d399;color:#34d399;cursor:default}
.choice.locked{cursor:default}
.qfb{font-size:.92rem;padding:7px 11px;border-radius:6px;margin-top:4px;display:none;line-height:1.55}
.qfb.show{display:block}
.qfb.ok{background:rgba(52,211,153,.14);color:#34d399}
.qfb.ng{background:rgba(239,68,68,.14);color:#f87171}

/* ── 역추적 ── */
.eq-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;
  font-size:1.2rem;font-family:'Times New Roman',serif;font-style:italic;margin:10px 0}
.eq-blank{
  width:58px;padding:5px 6px;border-radius:6px;text-align:center;
  background:rgba(255,255,255,.08);border:2px solid rgba(124,58,237,.4);
  color:#fde68a;font-size:1.1rem;font-family:'Times New Roman',serif;
  transition:.2s;
}
.eq-blank.ok{border-color:#34d399;background:rgba(52,211,153,.14)}
.eq-blank.ng{border-color:#ef4444;background:rgba(239,68,68,.14)}

/* ── 버튼 ── */
.btn{padding:9px 20px;border-radius:10px;border:none;cursor:pointer;
  font-size:.95rem;font-weight:700;transition:.18s}
.btn-p{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff}
.btn-p:hover{transform:translateY(-1px);box-shadow:0 4px 14px rgba(124,58,237,.4)}
.btn-o{background:transparent;border:1px solid rgba(255,255,255,.2);color:#e2e8ff}
.btn-o:hover{background:rgba(255,255,255,.07)}
.nav-row{display:flex;justify-content:space-between;align-items:center;
  margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,.07)}
.nav-label{font-size:.88rem;color:#475569}

/* ── 결과 ── */
.final-box{text-align:center;padding:22px 10px}
.big-score{font-size:3.4rem;font-weight:900;color:#a78bfa;line-height:1.2;margin:8px 0}
.grade-txt{font-size:1.1rem;color:#c4b5fd}
.done-banner{
  background:rgba(250,204,21,.08);border:1px solid rgba(250,204,21,.3);
  border-radius:12px;padding:16px 18px;text-align:center;margin-top:12px;
}
</style>
</head>
<body>

<!-- 진행바 -->
<div class="stepbar">
  <div class="sbar active" id="sb0"></div>
  <div class="sbar" id="sb1"></div>
  <div class="sbar" id="sb2"></div>
  <div class="sbar" id="sb3"></div>
</div>

<!-- ═══════════════════════════════════════════════
     SCREEN 1 : 켤레근이란? (개념 + 계산기)
═══════════════════════════════════════════════ -->
<div class="screen active" id="sc1">
  <div class="hero">
    <h2>🔍 켤레근이란?</h2>
    <p>이차방정식의 두 근이 서로 <strong>켤레 관계</strong>에 있다는 건 무슨 뜻일까요?<br>
    계수의 종류에 따라 두 가지 켤레근이 등장합니다!</p>
  </div>

  <!-- 두 종류 카드 -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">
    <div class="card" style="border-color:rgba(52,211,153,.3)">
      <span class="tag tag-rat">유리수 계수 (a,b,c ∈ 유리수)</span>
      <div class="card-title" style="color:#34d399">무리수 켤레근</div>
      <div class="mblock">
        한 근이 <span class="c1">p + q√m</span><br>
        ↓<br>
        다른 근은 <span class="c2">p − q√m</span>
      </div>
      <p style="font-size:.88rem;color:#6ee7b7">단, p·q는 유리수, √m은 무리수</p>
    </div>
    <div class="card" style="border-color:rgba(196,181,253,.3)">
      <span class="tag tag-real">실수 계수 (a,b,c ∈ 실수)</span>
      <div class="card-title" style="color:#c4b5fd">허수 켤레근</div>
      <div class="mblock">
        한 근이 <span class="c1">p + qi</span><br>
        ↓<br>
        다른 근은 <span class="c2">p − qi</span>
      </div>
      <p style="font-size:.88rem;color:#c4b5fd">단, p·q는 실수, q ≠ 0</p>
    </div>
  </div>

  <!-- 계산기 -->
  <div class="card">
    <div class="card-title">🧮 직접 확인해봐! — 계수를 바꿔가며 두 근의 관계를 관찰하세요</div>
    <div class="calc-row">
      <span class="math">a</span> =
      <input class="coeff-in" id="ca" type="number" value="1">
      <span class="math">b</span> =
      <input class="coeff-in" id="cb" type="number" value="-2">
      <span class="math">c</span> =
      <input class="coeff-in" id="cc" type="number" value="5">
      <button class="btn btn-p" onclick="calcRoots()">근 구하기</button>
    </div>
    <p style="font-size:.9rem;color:#64748b;margin-bottom:8px">
      예시 시도: b=-6,c=2 (무리수 켤레근) / b=-2,c=5 (허수 켤레근) / b=-5,c=4 (유리수 근)
    </p>
    <div class="result-box" id="rootResult"></div>
  </div>

  <div class="nav-row">
    <span class="nav-label">1 / 4</span>
    <button class="btn btn-p" onclick="goTo(2)">다음: 왜 그럴까? →</button>
  </div>
</div>

<!-- ═══════════════════════════════════════════════
     SCREEN 2 : 대입 증명 (단계별)
═══════════════════════════════════════════════ -->
<div class="screen" id="sc2">
  <div class="hero">
    <h2>🔬 직접 대입해서 확인하기</h2>
    <p><span class="math" style="color:#e2e8ff">x² − 2x + 5 = 0</span>의 두 근
    <span class="c1">1+2i</span>와 <span class="c2">1−2i</span>를<br>
    방정식에 직접 대입해서 둘 다 근임을 확인해 봐요!</p>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px">
    <!-- 왼쪽: 1+2i 대입 -->
    <div class="card">
      <div class="card-title" style="color:#f0abfc">x = <span class="c1">1+2i</span> 대입</div>
      <div class="step-box show" id="p1s1">
        <div class="step-lbl">STEP 1 — x² 계산</div>
        <div class="step-eq">(1+2<em>i</em>)²</div>
        <div class="step-eq">= 1 + 4<em>i</em> + 4<em>i</em>²</div>
        <div class="step-eq">= 1 + 4<em>i</em> + 4·(−1)</div>
        <div class="step-eq">= <span class="re">−3</span> + <span class="im">4<em>i</em></span></div>
      </div>
      <div class="step-box" id="p1s2">
        <div class="step-lbl">STEP 2 — −2x 계산</div>
        <div class="step-eq">−2(1+2<em>i</em>)</div>
        <div class="step-eq">= <span class="re">−2</span> <span class="im">−4<em>i</em></span></div>
      </div>
      <div class="step-box" id="p1s3">
        <div class="step-lbl">STEP 3 — 합산 (+5 포함)</div>
        <div class="step-eq">(<span class="re">−3</span>+<span class="im">4<em>i</em></span>) + (<span class="re">−2</span><span class="im">−4<em>i</em></span>) + <span class="re">5</span></div>
        <div class="step-eq">= (<span class="re">−3−2+5</span>) + (<span class="im">4−4</span>)<em>i</em></div>
        <div class="step-eq" style="color:#34d399;font-weight:700">= 0 + 0·<em>i</em> = 0 ✓</div>
      </div>
    </div>

    <!-- 오른쪽: 1−2i 대입 -->
    <div class="card">
      <div class="card-title" style="color:#6ee7b7">x = <span class="c2">1−2i</span> 대입</div>
      <div class="step-box show" id="p2s1">
        <div class="step-lbl">STEP 1 — x² 계산</div>
        <div class="step-eq">(1−2<em>i</em>)²</div>
        <div class="step-eq">= 1 − 4<em>i</em> + 4<em>i</em>²</div>
        <div class="step-eq">= 1 − 4<em>i</em> + 4·(−1)</div>
        <div class="step-eq">= <span class="re">−3</span> <span class="im">−4<em>i</em></span></div>
      </div>
      <div class="step-box" id="p2s2">
        <div class="step-lbl">STEP 2 — −2x 계산</div>
        <div class="step-eq">−2(1−2<em>i</em>)</div>
        <div class="step-eq">= <span class="re">−2</span> + <span class="im">4<em>i</em></span></div>
      </div>
      <div class="step-box" id="p2s3">
        <div class="step-lbl">STEP 3 — 합산 (+5 포함)</div>
        <div class="step-eq">(<span class="re">−3</span><span class="im">−4<em>i</em></span>) + (<span class="re">−2</span>+<span class="im">4<em>i</em></span>) + <span class="re">5</span></div>
        <div class="step-eq">= (<span class="re">−3−2+5</span>) + (<span class="im">−4+4</span>)<em>i</em></div>
        <div class="step-eq" style="color:#34d399;font-weight:700">= 0 + 0·<em>i</em> = 0 ✓</div>
      </div>
    </div>
  </div>

  <div style="text-align:center;margin-bottom:10px">
    <button class="btn btn-p" id="btnStep" onclick="showStep()">▶ 다음 단계 보기</button>
  </div>

  <!-- 핵심 인사이트 -->
  <div class="card" id="insightBox" style="display:none;border-color:rgba(250,204,21,.35)">
    <div class="card-title" style="color:#fcd34d">💡 핵심 발견!</div>
    <p style="font-size:1rem;line-height:1.8;color:#e2e8ff">
      두 근 <span class="c1">1+2i</span> 와 <span class="c2">1−2i</span>는 실수부(<span class="re">1</span>)가 <strong>같고</strong>,
      허수부(<span class="im">2</span>)는 <strong>부호만 반대</strong>예요.<br>
      그래서 실수부끼리의 합산은 그대로 0이 되고, 허수부끼리는 +4i와 −4i가 상쇄되어 역시 0이 됩니다.<br>
      <strong>→ 켤레복소수는 '실수부 동일 + 허수부 부호 반대' 구조 때문에 항상 함께 나타납니다!</strong>
    </p>
  </div>

  <!-- 일반화 카드 -->
  <div class="card" id="generalBox" style="display:none;border-color:rgba(196,181,253,.3)">
    <div class="card-title" style="color:#c4b5fd">📐 일반화</div>
    <p style="font-size:1rem;line-height:1.8;color:#e2e8ff">
      <strong>실수 계수</strong> <span class="math">ax²+bx+c=0</span>에 <span class="c1">x = p+qi</span>를 대입하면<br>
      실수부 조건: <span class="re">ap²−aq²+bp+c = 0</span><br>
      허수부 조건: <span class="im">2apq+bq = 0</span><br><br>
      이 두 조건이 만족될 때, <span class="c2">x = p−qi</span>를 대입하면
      실수부는 똑같이 0, 허수부는 부호만 반대라 역시 0이 됩니다.<br>
      <strong>따라서 켤레복소수는 항상 쌍으로 근이 됩니다.</strong>
    </p>
  </div>

  <div class="nav-row">
    <button class="btn btn-o" onclick="goTo(1)">← 이전</button>
    <span class="nav-label">2 / 4</span>
    <button class="btn btn-p" onclick="goTo(3)">다음: 퀴즈 →</button>
  </div>
</div>

<!-- ═══════════════════════════════════════════════
     SCREEN 3 : 켤레근 맞추기 퀴즈
═══════════════════════════════════════════════ -->
<div class="screen" id="sc3">
  <div class="hero">
    <h2>🎯 켤레근 맞추기 퀴즈!</h2>
    <p>이차방정식과 한 근이 주어졌을 때, 나머지 한 근을 골라보세요.</p>
  </div>

  <div id="quizCard"></div>
  <div id="quizFinal" style="display:none" class="final-box">
    <div style="font-size:1.6rem">🎉 퀴즈 완료!</div>
    <div class="big-score" id="finalScore"></div>
    <div class="grade-txt" id="finalGrade"></div>
  </div>

  <div class="nav-row">
    <button class="btn btn-o" onclick="goTo(2)">← 이전</button>
    <span class="nav-label" id="qLabel">3 / 4</span>
    <button class="btn btn-p" id="btnNQ" onclick="nextQ()" style="display:none">다음 문제 →</button>
    <button class="btn btn-p" id="btnToS4" onclick="goTo(4)" style="display:none">다음: 역추적 챌린지 →</button>
  </div>
</div>

<!-- ═══════════════════════════════════════════════
     SCREEN 4 : 역추적 챌린지
═══════════════════════════════════════════════ -->
<div class="screen" id="sc4">
  <div class="hero">
    <h2>🔄 역추적 챌린지!</h2>
    <p>두 켤레근이 주어졌을 때, 이차방정식을 완성하세요.<br>
    <span style="font-size:.92rem;color:#94a3b8">힌트: 두 근의 합 = −b, 두 근의 곱 = c (최고차항 계수 1일 때)</span></p>
  </div>

  <!-- 문제 1 -->
  <div class="card" id="r1card">
    <div class="card-title">📌 문제 1</div>
    <p style="font-size:1.05rem;margin-bottom:10px">
      두 근이 <span class="c1">1+2<em>i</em></span> 와 <span class="c2">1−2<em>i</em></span> 인<br>
      이차방정식(최고차항 계수 1)을 구하세요.
    </p>
    <div style="background:rgba(255,255,255,.04);border-radius:8px;padding:9px 13px;margin-bottom:10px;font-size:.97rem;color:#94a3b8;line-height:1.9">
      두 근의 합: (1+2<em>i</em>) + (1−2<em>i</em>) = <strong style="color:#fde68a">?</strong>
      → <em>x</em>² 앞 계수가 1이면 <strong style="color:#fde68a">−b = 합</strong><br>
      두 근의 곱: (1+2<em>i</em>)(1−2<em>i</em>) = 1² + 2² = <strong style="color:#fde68a">?</strong>
      → <strong style="color:#fde68a">c = 곱</strong>
    </div>
    <div class="eq-row">
      <span><em>x</em>²</span>
      <span>−</span>
      <input class="eq-blank" id="r1b" type="number" placeholder="?">
      <span><em>x</em></span>
      <span>+</span>
      <input class="eq-blank" id="r1c" type="number" placeholder="?">
      <span>= 0</span>
    </div>
    <button class="btn btn-p" onclick="checkR(1)" style="margin-top:6px">확인</button>
    <div class="qfb" id="r1fb"></div>
  </div>

  <!-- 문제 2 -->
  <div class="card" id="r2card">
    <div class="card-title">📌 문제 2</div>
    <p style="font-size:1.05rem;margin-bottom:10px">
      두 근이 <span class="c1">3+√5</span> 와 <span class="c2">3−√5</span> 인<br>
      이차방정식(최고차항 계수 1)을 구하세요.
    </p>
    <div style="background:rgba(255,255,255,.04);border-radius:8px;padding:9px 13px;margin-bottom:10px;font-size:.97rem;color:#94a3b8;line-height:1.9">
      두 근의 합: (3+√5) + (3−√5) = <strong style="color:#fde68a">?</strong><br>
      두 근의 곱: (3+√5)(3−√5) = 3² − (√5)² = 9 − 5 = <strong style="color:#fde68a">?</strong>
    </div>
    <div class="eq-row">
      <span><em>x</em>²</span>
      <span>−</span>
      <input class="eq-blank" id="r2b" type="number" placeholder="?">
      <span><em>x</em></span>
      <span>+</span>
      <input class="eq-blank" id="r2c" type="number" placeholder="?">
      <span>= 0</span>
    </div>
    <button class="btn btn-p" onclick="checkR(2)" style="margin-top:6px">확인</button>
    <div class="qfb" id="r2fb"></div>
  </div>

  <!-- 완료 배너 -->
  <div id="allDone" class="done-banner" style="display:none">
    <div style="font-size:2rem;margin-bottom:6px">🏆</div>
    <div style="font-size:1.2rem;color:#fcd34d;font-weight:700;margin-bottom:8px">모든 챌린지 완료!</div>
    <p style="font-size:1rem;color:#94a3b8;line-height:1.75">
      이차방정식에서 켤레근이 항상 쌍으로 나타나는 이유,<br>
      두 켤레근으로 방정식을 역추적하는 방법까지 완전 정복했어요!<br>
      아래 성찰 질문도 꼼꼼히 답해보세요 💜
    </p>
  </div>

  <div class="nav-row">
    <button class="btn btn-o" onclick="goTo(3)">← 이전</button>
    <span class="nav-label">4 / 4</span>
    <span></span>
  </div>
</div>

<!-- ─────────────────────────────────────────── -->
<script>
/* ── iframe 높이 자동 조정 ──────────────────── */
function notifyHeight(){
  const h = Math.max(
    document.body.scrollHeight,
    document.documentElement.scrollHeight,
    document.body.offsetHeight,
    document.documentElement.offsetHeight
  ) + 40;
  // Streamlit components.html listens for this format
  window.parent.postMessage({isStreamlitMessage:true, type:'streamlit:setFrameHeight', args:{height:h}}, '*');
  // Also try simpler format as fallback
  window.parent.postMessage({type:'streamlit:setFrameHeight', height:h}, '*');
}
// Fire after paint so layout is complete
function scheduleResize(delay){
  setTimeout(()=>{ notifyHeight(); setTimeout(notifyHeight, 150); }, delay||0);
}
const ro = new ResizeObserver(()=>scheduleResize(0));
ro.observe(document.body);
window.addEventListener('load', ()=>scheduleResize(100));

/* ── 화면 전환 ─────────────────────────────── */
let cur = 1;
function goTo(n) {
  document.getElementById('sc'+cur).classList.remove('active');
  document.getElementById('sb'+(cur-1)).classList.remove('active');
  document.getElementById('sb'+(cur-1)).classList.add('done');
  cur = n;
  document.getElementById('sc'+n).classList.add('active');
  document.getElementById('sb'+(n-1)).classList.remove('done');
  document.getElementById('sb'+(n-1)).classList.add('active');
  window.scrollTo(0,0);
  scheduleResize(50);
}

/* ── Screen 1: 근 계산기 ────────────────────── */
function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b];}return a;}
function fmtNum(n,d){
  // n/d as fraction or integer string
  if(d===0)return '0';
  const g=gcd(Math.abs(Math.round(n)),Math.abs(d));
  const rn=Math.round(n)/g, rd=d/g;
  if(rd===1)return String(rn);
  return `${rn}/${rd}`;
}
function simplifySqrt(D){
  // find largest k² dividing D; return {k,m}
  let k=1;
  for(let i=Math.floor(Math.sqrt(D));i>=2;i--){
    if(D%(i*i)===0){k=i;break;}
  }
  return {k,m:D/(k*k)};
}

function calcRoots(){
  const a=parseFloat(document.getElementById('ca').value)||1;
  const b=parseFloat(document.getElementById('cb').value)||0;
  const c=parseFloat(document.getElementById('cc').value)||0;
  const D=b*b-4*a*c;
  const el=document.getElementById('rootResult');

  let html=`<div style="margin-bottom:10px;font-size:.97rem;color:#94a3b8">
    방정식: <span class="math">${a}x² + (${b})x + (${c}) = 0</span><br>
    판별식 <em>D</em> = <em>b</em>² − 4<em>ac</em> = ${b*b} − ${4*a*c} = <strong style="color:#fde68a">${D}</strong>
  </div>`;

  if(Math.abs(D)<1e-9){
    const p=fmtNum(-b,2*a);
    html+=`<div>D = 0 → 중근: <span class="math">${p}</span><br>
    <span style="font-size:.8rem;color:#64748b">(두 근이 같으므로 켤레 관계 없음)</span></div>`;
  } else if(D<0){
    const p=fmtNum(-b,2*a);
    const {k,m}=simplifySqrt(-D);
    const qn=k, qd=2*Math.abs(a);
    const qStr=fmtNum(qn,qd);
    html+=`<div style="margin-bottom:10px">
      <span style="color:#94a3b8;font-size:.94rem">D &lt; 0 → <strong style="color:#c4b5fd">허수 켤레근</strong></span><br>
      <span class="c1" style="font-size:1.3rem">${p} + ${qStr}<em>i</em></span>
      &nbsp;와&nbsp;
      <span class="c2" style="font-size:1.3rem">${p} − ${qStr}<em>i</em></span>
    </div>
    <div style="background:rgba(196,181,253,.12);border-radius:8px;padding:8px 12px;font-size:.95rem;color:#c4b5fd">
      ✨ 실수부 <strong>${p}</strong>는 같고, 허수부의 부호만 반대입니다.<br>
      → 두 근은 서로 <strong>켤레복소수</strong> 관계!
    </div>`;
  } else {
    const sqD=Math.sqrt(D);
    const isPerfect=Math.abs(sqD-Math.round(sqD))<0.0001;
    if(isPerfect){
      const s=Math.round(sqD);
      const r1=fmtNum(-b+s,2*a), r2=fmtNum(-b-s,2*a);
      html+=`<div>D &gt; 0, 완전제곱수 → 유리수 근: <span class="math">${r1}, ${r2}</span><br>
      <span style="font-size:.92rem;color:#64748b">두 근이 유리수이므로 켤레 무리수/복소수 관계는 해당 없음</span></div>`;
    } else {
      const {k,m}=simplifySqrt(D);
      const p=fmtNum(-b,2*a);
      const qn=k, qd=2*Math.abs(a);
      const qStr=fmtNum(qn,qd);
      const mDisplay=(qStr==='1')?`√${m}`:`${qStr}√${m}`;
      html+=`<div style="margin-bottom:10px">
        <span style="color:#94a3b8;font-size:.94rem">D &gt; 0, 완전제곱수 ✗ → <strong style="color:#34d399">무리수 켤레근</strong></span><br>
        <span class="c1" style="font-size:1.3rem">${p} + ${mDisplay}</span>
        &nbsp;와&nbsp;
        <span class="c2" style="font-size:1.3rem">${p} − ${mDisplay}</span>
      </div>
      <div style="background:rgba(52,211,153,.1);border-radius:8px;padding:8px 12px;font-size:.95rem;color:#6ee7b7">
        ✨ 유리수 부분 <strong>${p}</strong>는 같고, 무리수 부분의 부호만 반대입니다.<br>
        → 두 근은 서로 <strong>켤레 무리수</strong> 관계!
      </div>`;
    }
  }
  el.innerHTML=html;
}
calcRoots();

/* ── Screen 2: 단계별 증명 ──────────────────── */
let pStep=1;
function showStep(){
  pStep++;
  if(pStep===2){
    document.getElementById('p1s2').classList.add('show');
    document.getElementById('p2s2').classList.add('show');
  }
  if(pStep===3){
    document.getElementById('p1s3').classList.add('show');
    document.getElementById('p2s3').classList.add('show');
    document.getElementById('insightBox').style.display='block';
    document.getElementById('generalBox').style.display='block';
    document.getElementById('btnStep').style.display='none';
  }
  scheduleResize(50);
}

/* ── Screen 3: 퀴즈 ─────────────────────────── */
const QS=[
  {
    eq:'x² − 4x + 13 = 0',
    given:'한 근: <span class="c1">2 + 3<em>i</em></span>',
    choices:['2 − 3<em>i</em>','−2 + 3<em>i</em>','2 + 3<em>i</em>'],
    ans:0,
    tip:'실수 계수 이차방정식의 허수근은 켤레복소수 쌍으로 나타납니다. 실수부(2)는 그대로, 허수부 부호만 반전!'
  },
  {
    eq:'x² − 6x + 2 = 0',
    given:'한 근: <span class="c1">3 + √7</span>',
    choices:['3 − √7','−3 + √7','3 + √7'],
    ans:0,
    tip:'유리수 계수이면 무리수 켤레근 법칙! 유리수 부분(3)은 그대로, 무리수 부분 부호만 반전!'
  },
  {
    eq:'x² + 2x + 5 = 0',
    given:'한 근: <span class="c1">−1 + 2<em>i</em></span>',
    choices:['1 − 2<em>i</em>','−1 − 2<em>i</em>','1 + 2<em>i</em>'],
    ans:1,
    tip:'실수부 −1은 그대로, 허수부 +2i의 부호만 바뀌어 −1 − 2i가 켤레근입니다.'
  },
  {
    eq:'x² − 8x + 11 = 0',
    given:'한 근: <span class="c1">4 + √5</span>',
    choices:['4 − √5','−4 + √5','4 + √5'],
    ans:0,
    tip:'유리수 부분(4)은 그대로, 무리수 부분(√5)의 부호만 바뀌어 4 − √5가 켤레근입니다.'
  },
  {
    eq:'x² + 4x + 29 = 0',
    given:'한 근: <span class="c1">−2 + 5<em>i</em></span>',
    choices:['2 + 5<em>i</em>','2 − 5<em>i</em>','−2 − 5<em>i</em>'],
    ans:2,
    tip:'실수부 −2는 그대로, 허수부 +5i의 부호만 바뀌어 −2 − 5i가 켤레근입니다.'
  }
];
let qIdx=0, score=0, qAnswered=false;

function renderQ(){
  const q=QS[qIdx];
  document.getElementById('quizCard').innerHTML=`
    <div class="card">
      <div class="quiz-meta">
        <span>문제 ${qIdx+1} / ${QS.length}</span>
        <span style="color:#a78bfa">점수 ${score} / ${qIdx}</span>
      </div>
      <div class="quiz-eq"><strong>방정식:</strong> <span class="math">${q.eq}</span></div>
      <div class="quiz-hint">${q.given}</div>
      <p style="font-size:.94rem;color:#64748b;margin-bottom:10px">다른 한 근은?</p>
      <div class="choices">
        ${q.choices.map((c,i)=>`<div class="choice" id="ch${i}" onclick="pick(${i})">${c}</div>`).join('')}
      </div>
      <div class="qfb" id="qfb"></div>
    </div>`;
  qAnswered=false;
  document.getElementById('btnNQ').style.display='none';
  document.getElementById('btnToS4').style.display='none';
}

function pick(i){
  if(qAnswered)return;
  qAnswered=true;
  const q=QS[qIdx];
  const fb=document.getElementById('qfb');
  document.querySelectorAll('.choice').forEach(c=>{c.classList.add('locked');c.onclick=null;});
  if(i===q.ans){
    score++;
    document.getElementById('ch'+i).classList.add('correct');
    fb.className='qfb show ok';
    fb.textContent='✓ 정답! '+q.tip;
  } else {
    document.getElementById('ch'+i).classList.add('wrong');
    document.getElementById('ch'+q.ans).classList.add('reveal');
    fb.className='qfb show ng';
    fb.textContent='✗ 오답. '+q.tip;
  }
  if(qIdx<QS.length-1){
    document.getElementById('btnNQ').style.display='inline-block';
  } else {
    showFinal();
  }
}

function nextQ(){qIdx++;renderQ();}

function showFinal(){
  document.getElementById('quizCard').style.display='none';
  document.getElementById('quizFinal').style.display='block';
  document.getElementById('finalScore').textContent=score+' / '+QS.length;
  const g=['다시 한번 도전해봐요! 💪','조금 더 연습하면 잘 할 수 있어요! 📖','잘 하고 있어요! 👍','훌륭해요! ⭐','완벽 정복! 🏆'];
  document.getElementById('finalGrade').textContent=g[score]||g[0];
  document.getElementById('btnToS4').style.display='inline-block';
  scheduleResize(50);
}

renderQ();

/* ── Screen 4: 역추적 ────────────────────────── */
const ANSWERS={1:{b:2,c:5},2:{b:6,c:4}};
const r_done={1:false,2:false};

function checkR(n){
  const bv=parseFloat(document.getElementById(`r${n}b`).value);
  const cv=parseFloat(document.getElementById(`r${n}c`).value);
  const fb=document.getElementById(`r${n}fb`);
  const bi=document.getElementById(`r${n}b`);
  const ci=document.getElementById(`r${n}c`);
  const ans=ANSWERS[n];
  bi.classList.remove('ok','ng');
  ci.classList.remove('ok','ng');
  if(bv===ans.b && cv===ans.c){
    bi.classList.add('ok');ci.classList.add('ok');
    fb.className='qfb show ok';
    if(n===1) fb.innerHTML='✓ 정답! <em>x</em>²−2<em>x</em>+5=0<br><span style="font-size:.88rem">합=2 → b=2, 곱=1²+2²=5 → c=5</span>';
    else fb.innerHTML='✓ 정답! <em>x</em>²−6<em>x</em>+4=0<br><span style="font-size:.88rem">합=6 → b=6, 곱=9−5=4 → c=4</span>';
    r_done[n]=true;
    if(r_done[1]&&r_done[2]){ document.getElementById('allDone').style.display='block'; scheduleResize(50); }
  } else {
    bi.classList.add('ng');ci.classList.add('ng');
    fb.className='qfb show ng';
    if(n===1) fb.innerHTML='✗ 다시 시도! 두 근의 합 = (1+2i)+(1−2i) = ?, 두 근의 곱 = (1+2i)(1−2i) = ?';
    else fb.innerHTML='✗ 다시 시도! 두 근의 합 = ?, (3+√5)(3−√5) = 3²−(√5)² = ?';
    setTimeout(()=>{bi.classList.remove('ng');ci.classList.remove('ng');},1400);
  }
}
</script>
</body>
</html>"""


def render():
    st.set_page_config(page_title="켤레근 탐정단", layout="wide")
    st.markdown(
        "<style>.main{max-width:100%}iframe{width:100%!important}</style>",
        unsafe_allow_html=True,
    )
    components.html(_HTML, height=1700, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
