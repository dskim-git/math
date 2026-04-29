import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🌺 하디-바인베르크 법칙",
    "description": "분꽃 유전자 빈도가 세대를 거쳐도 변하지 않는 이유를 이항분포로 직접 탐구합니다.",
    "order": 67,
}

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "하디바인베르크법칙"

_QUESTIONS = [
    {"type": "markdown", "text": "**🌺 하디-바인베르크 법칙 – 성찰 질문**"},
    {
        "key": "유전자형비율",
        "label": "R 유전자 빈도가 p일 때 RR, RW, WW의 비율은? 이항분포 (p+q)²와 어떻게 연결되는지 설명하세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "RR = p², RW = 2pq, WW = q² ... (p+q)²를 전개하면...",
    },
    {
        "key": "빈도유지이유",
        "label": "2세대에서 R 유전자 빈도가 여전히 p가 되는 과정을 수식으로 설명해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "P(R 포함) = RR인 경우 + RW의 절반 = p² + ½×2pq = p² + pq = ...",
    },
    {
        "key": "법칙깨지는경우",
        "label": "하디-바인베르크 법칙이 성립하지 않는 조건을 2가지 이상 적어보세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) 자연선택이 작용할 때... / 소규모 집단에서 유전적 부동이 일어날 때...",
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",         "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]


_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:#060b14;color:#e2e8f0;
  padding:14px 14px 24px;
}
@keyframes popIn{
  0%{transform:scale(0) rotate(-20deg);opacity:0}
  70%{transform:scale(1.15) rotate(3deg)}
  100%{transform:scale(1) rotate(0);opacity:1}
}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes glow{0%,100%{box-shadow:0 0 0 rgba(253,224,71,0)}50%{box-shadow:0 0 16px rgba(253,224,71,.35)}}

h1{text-align:center;font-size:1.3rem;font-weight:800;color:#fde68a;margin-bottom:4px}
.sub{text-align:center;font-size:.78rem;color:#94a3b8;margin-bottom:14px}

/* Gene intro cards */
.gene-row{display:flex;gap:8px;margin-bottom:12px}
.gene-card{
  flex:1;border-radius:12px;padding:10px 6px;text-align:center;
  border:1.5px solid;transition:transform .2s
}
.gene-card:hover{transform:translateY(-3px)}
.gc-rr{border-color:rgba(248,113,113,.45);background:rgba(248,113,113,.1)}
.gc-rw{border-color:rgba(244,114,182,.45);background:rgba(244,114,182,.1)}
.gc-ww{border-color:rgba(134,239,172,.45);background:rgba(134,239,172,.1)}
.gene-em{font-size:1.7rem}
.gene-tp{font-size:.9rem;font-weight:800;margin:3px 0}
.c-rr{color:#f87171}.c-rw{color:#f9a8d4}.c-ww{color:#86efac}
.gene-fr{font-size:.7rem;color:#94a3b8}

/* Cards */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:14px;margin-bottom:12px}
.ctitle{font-size:.85rem;font-weight:700;color:#c4b5fd;margin-bottom:10px;display:flex;align-items:center;gap:6px}

/* Slider */
.srow{display:flex;gap:10px;align-items:center;margin-bottom:8px}
input[type=range]{flex:1;accent-color:#6366f1;cursor:pointer}
.badge{border-radius:8px;padding:3px 10px;font-size:.82rem;font-weight:700;min-width:76px;text-align:center}
.badge-r{background:rgba(248,113,113,.2);color:#f87171}
.badge-w{background:rgba(134,239,172,.2);color:#86efac}
.geno-bar{display:flex;height:22px;border-radius:8px;overflow:hidden;gap:1px;margin-top:6px}
.gb-seg{display:flex;align-items:center;justify-content:center;font-size:.62rem;font-weight:700;color:rgba(255,255,255,.85);transition:width .5s ease;overflow:hidden;white-space:nowrap}
.gb-rr{background:rgba(239,68,68,.7)}
.gb-rw{background:rgba(236,72,153,.65)}
.gb-ww{background:rgba(34,197,94,.6)}

/* Garden */
.garden{display:flex;flex-wrap:wrap;gap:3px;justify-content:center;padding:8px;background:rgba(0,0,0,.3);border-radius:10px;min-height:68px}
.f{font-size:14px;cursor:default;display:inline-block;animation:popIn .35s ease-out both}
.f:hover{transform:scale(1.4)}
.gleg{display:flex;justify-content:center;gap:12px;font-size:.7rem;color:#94a3b8;margin-top:6px;flex-wrap:wrap}

/* Punnett */
.prow{display:flex;gap:10px;align-items:flex-start}
table.pt{width:100%;border-collapse:collapse;min-width:170px}
table.pt td{text-align:center;padding:7px 4px;border:1px solid rgba(255,255,255,.1);font-size:.78rem}
.ph{background:rgba(255,255,255,.08);color:#cbd5e1;font-size:.72rem}
.prr{background:rgba(248,113,113,.18);color:#fca5a5;font-weight:700}
.prw{background:rgba(244,114,182,.18);color:#f9a8d4;font-weight:700}
.pww{background:rgba(134,239,172,.18);color:#86efac;font-weight:700}
.psub{color:#64748b;font-size:.68rem}

/* Calc */
.cbox{
  flex:1.2;background:rgba(99,102,241,.09);border:1px solid rgba(99,102,241,.22);
  border-radius:10px;padding:10px 11px;font-size:.77rem;line-height:1.95
}
.ceq{font-family:'Courier New',monospace;color:#c4b5fd;display:block}
.cres{
  color:#fde68a;font-weight:700;font-size:.82rem;
  border-top:1px dashed rgba(253,224,71,.25);padding-top:.3rem;margin-top:.2rem;display:block
}
.clbl{color:#64748b;font-size:.7rem;display:block;margin-top:.4rem}

/* Freq compare */
.fcmp{display:flex;gap:8px;align-items:stretch}
.fcol{flex:1}
.fct{font-size:.72rem;color:#94a3b8;text-align:center;margin-bottom:6px;font-weight:600}
.br{display:flex;align-items:center;gap:5px;margin-bottom:5px}
.bl{font-size:.68rem;width:30px;color:#94a3b8}
.bbg{flex:1;height:16px;background:rgba(255,255,255,.08);border-radius:8px;overflow:hidden}
.bf{height:100%;border-radius:8px;transition:width .65s ease;display:flex;align-items:center;padding-left:5px;font-size:.6rem;font-weight:700;color:rgba(255,255,255,.75)}
.br-r{background:linear-gradient(90deg,#dc2626,#f87171)}
.br-w{background:linear-gradient(90deg,#16a34a,#86efac)}
.bval{font-size:.7rem;width:28px;text-align:right}
.eq-mid{display:flex;align-items:center;justify-content:center;font-size:1.6rem;color:#4ade80;padding:0 2px}

/* Insight */
.insight{
  background:rgba(253,224,71,.08);border:1px solid rgba(253,224,71,.25);
  border-radius:10px;padding:10px 12px;font-size:.8rem;line-height:1.7;margin-top:10px;
  animation:glow 2s ease-in-out infinite
}
.hl{color:#fde68a;font-weight:800}

/* Multi-gen */
.mg-track{display:flex;gap:4px;margin-top:10px;overflow-x:auto;padding-bottom:2px}
.mg-block{
  min-width:42px;flex:1;border-radius:8px;padding:7px 3px;text-align:center;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
  animation:fadeUp .4s ease-out both
}
.mg-r{color:#f87171;font-weight:700;font-size:.82rem}
.mg-lbl{color:#64748b;font-size:.6rem;margin-top:2px}

/* Buttons */
.btn{
  border:none;border-radius:20px;padding:8px 22px;font-size:.82rem;font-weight:700;
  cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px
}
.btn-v{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white}
.btn-a{background:linear-gradient(135deg,#f59e0b,#fbbf24);color:#1c1917}
.btn:hover{transform:scale(1.06);filter:brightness(1.1)}
.btn:active{transform:scale(.96)}
.center{text-align:center}
.mt8{margin-top:8px}
.mt10{margin-top:10px}
.sep{border:none;border-top:1px solid rgba(255,255,255,.06);margin:4px 0 10px}
</style>
</head>
<body>

<h1>🌺 하디-바인베르크 법칙 탐구</h1>
<div class="sub">분꽃 유전자 빈도는 세대가 바뀌어도 변할까? · 이항분포로 직접 확인!</div>

<!-- Gene type cards -->
<div class="gene-row">
  <div class="gene-card gc-rr">
    <div class="gene-em">🌺</div>
    <div class="gene-tp c-rr">RR</div>
    <div class="gene-fr">빨간색</div>
    <div class="gene-fr" id="card-rr">비율 p²</div>
  </div>
  <div class="gene-card gc-rw">
    <div class="gene-em">🌸</div>
    <div class="gene-tp c-rw">RW</div>
    <div class="gene-fr">분홍색</div>
    <div class="gene-fr" id="card-rw">비율 2pq</div>
  </div>
  <div class="gene-card gc-ww">
    <div class="gene-em">🌼</div>
    <div class="gene-tp c-ww">WW</div>
    <div class="gene-fr">흰색</div>
    <div class="gene-fr" id="card-ww">비율 q²</div>
  </div>
</div>

<!-- Slider -->
<div class="card">
  <div class="ctitle">🎛️ R 유전자 빈도 <em>p</em> 설정해보기</div>
  <div class="srow">
    <span class="badge badge-r">R&nbsp;<span id="pVal">0.60</span></span>
    <input type="range" id="pSlider" min="5" max="95" value="60" step="5" oninput="updateAll()">
    <span class="badge badge-w">W&nbsp;<span id="qVal">0.40</span></span>
  </div>
  <div class="geno-bar">
    <div class="gb-seg gb-rr" id="gbar-rr" style="width:36%">RR</div>
    <div class="gb-seg gb-rw" id="gbar-rw" style="width:48%">RW</div>
    <div class="gb-seg gb-ww" id="gbar-ww" style="width:16%">WW</div>
  </div>
  <div style="font-size:.67rem;color:#64748b;text-align:center;margin-top:4px">(p+q)² = p²·RR + 2pq·RW + q²·WW</div>
</div>

<!-- Garden -->
<div class="card">
  <div class="ctitle">🌱 꽃밭 시각화 (100그루)</div>
  <div class="garden" id="garden"></div>
  <div class="gleg" id="gleg"></div>
</div>

<!-- Punnett + Calc -->
<div class="card">
  <div class="ctitle">🔬 교배 분석 — 다음 세대 유전자 빈도는?</div>
  <div class="prow">
    <div>
      <div style="font-size:.72rem;color:#94a3b8;text-align:center;margin-bottom:6px">퍼넷 사각형</div>
      <table class="pt">
        <tr>
          <td class="ph">×</td>
          <td class="ph">🌺 R <span style="color:#f87171">(p)</span></td>
          <td class="ph">🌼 W <span style="color:#86efac">(q)</span></td>
        </tr>
        <tr>
          <td class="ph">🌺 R <span style="color:#f87171">(p)</span></td>
          <td class="prr">🌺 RR<br><span class="psub" id="v-rr">p²</span></td>
          <td class="prw">🌸 RW<br><span class="psub" id="v-rw">pq</span></td>
        </tr>
        <tr>
          <td class="ph">🌼 W <span style="color:#86efac">(q)</span></td>
          <td class="prw">🌸 WR<br><span class="psub" id="v-wr">pq</span></td>
          <td class="pww">🌼 WW<br><span class="psub" id="v-ww">q²</span></td>
        </tr>
      </table>
    </div>
    <div class="cbox">
      <span class="clbl">R 유전자 빈도 (다음 세대)</span>
      <span class="ceq" id="calc-r1">RR 기여: p² = ?</span>
      <span class="ceq" id="calc-r2">RW 절반: pq = ?</span>
      <span class="cres" id="calc-rres">= p ✅</span>
      <hr class="sep">
      <span class="clbl">W 유전자 빈도 (다음 세대)</span>
      <span class="ceq" id="calc-w1">WW 기여: q² = ?</span>
      <span class="ceq" id="calc-w2">WR 절반: pq = ?</span>
      <span class="cres" id="calc-wres">= q ✅</span>
    </div>
  </div>
</div>

<!-- Freq compare -->
<div class="card">
  <div class="ctitle">📊 세대 전후 유전자 빈도 비교</div>
  <div class="fcmp">
    <div class="fcol">
      <div class="fct">현재 세대</div>
      <div class="br">
        <div class="bl">R</div>
        <div class="bbg"><div class="bf br-r" id="b1r" style="width:60%">p</div></div>
        <div class="bval c-rr" id="bv1r">0.60</div>
      </div>
      <div class="br">
        <div class="bl">W</div>
        <div class="bbg"><div class="bf br-w" id="b1w" style="width:40%">q</div></div>
        <div class="bval c-ww" id="bv1w">0.40</div>
      </div>
    </div>
    <div class="eq-mid" id="eqSign">=</div>
    <div class="fcol">
      <div class="fct">다음 세대</div>
      <div class="br">
        <div class="bl">R</div>
        <div class="bbg"><div class="bf br-r" id="b2r" style="width:60%">p</div></div>
        <div class="bval c-rr" id="bv2r">0.60</div>
      </div>
      <div class="br">
        <div class="bl">W</div>
        <div class="bbg"><div class="bf br-w" id="b2w" style="width:40%">q</div></div>
        <div class="bval c-ww" id="bv2w">0.40</div>
      </div>
    </div>
  </div>
  <div class="insight" id="eqInsight"></div>
</div>

<!-- Multi-gen -->
<div class="card">
  <div class="ctitle">🔄 여러 세대 반복 — 빈도가 진짜 유지될까?</div>
  <div class="center">
    <button class="btn btn-a" onclick="runMultiGen()">▶ 10세대 시뮬레이션!</button>
  </div>
  <div id="mgSection" style="display:none">
    <div style="font-size:.7rem;color:#94a3b8;text-align:center;margin:8px 0 2px">각 세대의 R 유전자 빈도</div>
    <div class="mg-track" id="mgTrack"></div>
    <div class="insight mt10" id="mgInsight"></div>
  </div>
</div>

<script>
let _p = 0.60;

function updateAll() {
  const p = parseInt(document.getElementById('pSlider').value) / 100;
  const q = (1 - p);
  _p = p;

  document.getElementById('pVal').textContent = p.toFixed(2);
  document.getElementById('qVal').textContent = q.toFixed(2);

  // Gene cards
  const rr = (p*p).toFixed(3), rw = (2*p*q).toFixed(3), ww = (q*q).toFixed(3);
  document.getElementById('card-rr').textContent = 'p² = ' + rr;
  document.getElementById('card-rw').textContent = '2pq = ' + rw;
  document.getElementById('card-ww').textContent = 'q² = ' + ww;

  // Genotype bar
  document.getElementById('gbar-rr').style.width = (p*p*100).toFixed(1) + '%';
  document.getElementById('gbar-rw').style.width = (2*p*q*100).toFixed(1) + '%';
  document.getElementById('gbar-ww').style.width = (q*q*100).toFixed(1) + '%';

  // Punnett
  document.getElementById('v-rr').textContent = 'p² = ' + rr;
  document.getElementById('v-rw').textContent = 'pq = ' + (p*q).toFixed(3);
  document.getElementById('v-wr').textContent = 'pq = ' + (p*q).toFixed(3);
  document.getElementById('v-ww').textContent = 'q² = ' + ww;

  // Calc
  document.getElementById('calc-r1').textContent = 'RR 기여: p² = ' + rr;
  document.getElementById('calc-r2').textContent = 'RW 절반: pq = ' + (p*q).toFixed(3);
  document.getElementById('calc-rres').innerHTML =
    '= ' + (p*p + p*q).toFixed(3) + ' = p(p+q) = <b style="color:#f87171">' + p.toFixed(2) + '</b> ✅';
  document.getElementById('calc-w1').textContent = 'WW 기여: q² = ' + ww;
  document.getElementById('calc-w2').textContent = 'WR 절반: pq = ' + (p*q).toFixed(3);
  document.getElementById('calc-wres').innerHTML =
    '= ' + (q*q + p*q).toFixed(3) + ' = q(p+q) = <b style="color:#86efac">' + q.toFixed(2) + '</b> ✅';

  // Freq bars
  ['b1r','b2r'].forEach(id => {
    document.getElementById(id).style.width = (p*100)+'%';
  });
  ['b1w','b2w'].forEach(id => {
    document.getElementById(id).style.width = (q*100)+'%';
  });
  document.getElementById('bv1r').textContent = p.toFixed(2);
  document.getElementById('bv1w').textContent = q.toFixed(2);
  document.getElementById('bv2r').textContent = p.toFixed(2);
  document.getElementById('bv2w').textContent = q.toFixed(2);

  document.getElementById('eqInsight').innerHTML =
    '<span class="hl">🎉 발견!</span> p = <b style="color:#f87171">' + p.toFixed(2) + '</b> 로 시작하면 ' +
    '다음 세대도 R 빈도 = <b style="color:#f87171">' + p.toFixed(2) + '</b>, ' +
    'W 빈도 = <b style="color:#86efac">' + q.toFixed(2) + '</b><br>' +
    '<b style="color:#fde68a">p값을 어떻게 바꿔도 빈도가 그대로!</b> → 이것이 하디-바인베르크 법칙입니다.';

  // Garden
  renderGarden(p, q);

  // Reset multi-gen
  document.getElementById('mgSection').style.display = 'none';
}

function renderGarden(p, q) {
  const g = document.getElementById('garden');
  const leg = document.getElementById('gleg');
  g.innerHTML = '';
  const total = 100;
  const rrN = Math.round(p * p * total);
  const rwN = Math.round(2 * p * q * total);
  const wwN = total - rrN - rwN;
  const arr = [
    ...Array(rrN).fill('🌺'),
    ...Array(rwN).fill('🌸'),
    ...Array(wwN).fill('🌼'),
  ];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  arr.forEach((em, i) => {
    const sp = document.createElement('span');
    sp.className = 'f';
    sp.textContent = em;
    sp.style.animationDelay = Math.min(i * 6, 300) + 'ms';
    g.appendChild(sp);
  });
  leg.innerHTML =
    '🌺 RR <b style="color:#f87171">' + rrN + '그루</b>&nbsp;&nbsp;' +
    '🌸 RW <b style="color:#f9a8d4">' + rwN + '그루</b>&nbsp;&nbsp;' +
    '🌼 WW <b style="color:#86efac">' + wwN + '그루</b>';
}

function runMultiGen() {
  const p0 = _p;
  const gens = [];
  let cur = p0;
  for (let i = 0; i < 10; i++) {
    gens.push(parseFloat(cur.toFixed(4)));
    const cq = 1 - cur;
    cur = cur * cur + cur * cq; // = p (always)
  }
  const track = document.getElementById('mgTrack');
  track.innerHTML = '';
  gens.forEach((gp, i) => {
    const d = document.createElement('div');
    d.className = 'mg-block';
    d.style.animationDelay = (i * 55) + 'ms';
    d.innerHTML =
      '<div class="mg-r">' + gp.toFixed(2) + '</div>' +
      '<div class="mg-lbl">' + (i + 1) + '세대</div>';
    track.appendChild(d);
  });
  document.getElementById('mgInsight').innerHTML =
    '<span class="hl">📌 결론!</span> p = ' + p0.toFixed(2) + ' 로 시작해도 ' +
    '<b style="color:#fde68a">10세대 내내 R 유전자 빈도가 ' + p0.toFixed(2) + ' 로 유지!</b><br>' +
    '유전적 평형 상태에서는 세대를 거듭해도 유전자 빈도가 변하지 않습니다.';
  document.getElementById('mgSection').style.display = 'block';
}

updateAll();
</script>
</body>
</html>
"""


def render():
    st.markdown("#### 🌺 하디-바인베르크 법칙 탐구")
    st.caption(
        "분꽃 유전자 빈도가 세대를 거쳐도 변하지 않는 이유를 이항분포로 직접 확인합니다."
    )

    components.html(_HTML, height=1600, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
