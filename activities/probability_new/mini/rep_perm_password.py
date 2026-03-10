import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form
import datetime

# ──────────────────────────────────────────────────────────
# Google Apps Script Web App URL
# 배포 후 아래 문자열을 실제 URL로 교체하세요.
_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "비밀번호탐색기"

_QUESTIONS = [
    {"type": 'markdown', "text": '**📝 이 활동으로 해결할 수 있는 문제 3개 (문제와 답 모두 작성)**'},
    {"key": '문제1', "label": '문제 1', "type": 'text_area', "height": 80},
    {"key": '답1', "label": '문제 1의 답', "type": 'text_input'},
    {"key": '문제2', "label": '문제 2', "type": 'text_area', "height": 80},
    {"key": '답2', "label": '문제 2의 답', "type": 'text_input'},
    {"key": '문제3', "label": '문제 3', "type": 'text_area', "height": 80},
    {"key": '답3', "label": '문제 3의 답', "type": 'text_input'},
    {"key": '새롭게알게된점', "label": '💡 이 활동을 통해 새롭게 알게 된 점', "type": 'text_area', "height": 100},
    {"key": '느낀점', "label": '💬 이 활동을 통해 느낀 점', "type": 'text_area', "height": 100},
]

META = {
    "title": "미니: 비밀번호 경우의 수 탐색기",
    "description": "k가지 문자를 n자리로 나열할 때의 중복순열 수(kⁿ)를 탐색합니다.",
    "order": 999999,
    "hidden": True,
}

def render():
    st.header("🔐 비밀번호 경우의 수 탐색기")
    st.markdown("""
- **중복순열**: 서로 다른 $k$가지 문자 중에서 **중복을 허용**하여 $n$자리를 나열하는 경우의 수는 $k^n$
- 아래에서 자릿수와 사용할 문자 종류 수를 바꿔가며 경우의 수가 어떻게 달라지는지 확인해 보세요.
""")

    components.html("""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0f172a 100%);min-height:100vh;padding:16px;color:#e2e8f0}
  .card{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:20px 24px;margin:12px 0;backdrop-filter:blur(12px)}
  .card-title{font-size:15px;font-weight:700;color:#a5b4fc;margin-bottom:14px;display:flex;align-items:center;gap:8px}
  .row{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start;margin-bottom:14px}
  .ctrl label{display:block;font-size:12px;color:#94a3b8;margin-bottom:6px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .ctrl input[type=range]{width:200px;-webkit-appearance:none;height:6px;border-radius:3px;background:linear-gradient(90deg,#6366f1,#22d3ee);outline:none}
  .ctrl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#fff;border:3px solid #6366f1;cursor:pointer;box-shadow:0 0 8px rgba(99,102,241,.5)}
  .val{display:inline-block;min-width:36px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:10px;padding:3px 10px;font-weight:800;font-size:17px;text-align:center;color:#fff;box-shadow:0 2px 12px rgba(99,102,241,.4)}
  .formula-box{background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);border-radius:14px;padding:14px 20px;margin:12px 0;text-align:center}
  .formula{font-size:26px;font-weight:800;color:#a5b4fc;margin-bottom:4px;letter-spacing:.02em}
  .sub{font-size:13px;color:#94a3b8}
  .chars-display{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}
  .ch{background:linear-gradient(135deg,#0ea5e9,#6366f1);border-radius:10px;padding:5px 12px;font-weight:800;font-size:16px;color:#fff;box-shadow:0 2px 8px rgba(99,102,241,.35);min-width:32px;text-align:center}
  .compare{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:4px}
  .cbox{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:16px;text-align:center;transition:.3s}
  .cbox.highlight{background:rgba(99,102,241,.15);border-color:rgba(99,102,241,.4)}
  .cbox .lbl{font-size:11px;color:#94a3b8;margin-bottom:6px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .cbox .num{font-size:30px;font-weight:900;color:#e2e8f0;margin-bottom:4px}
  .cbox .formula-lbl{font-size:13px;color:#6366f1;font-weight:700}
  .list-wrap{max-height:280px;overflow-y:auto;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:10px;background:rgba(0,0,0,.2)}
  .list-grid{display:flex;flex-wrap:wrap;gap:6px}
  .chip{background:rgba(99,102,241,.2);border:1px solid rgba(99,102,241,.4);border-radius:8px;padding:4px 10px;font-size:13px;font-family:'JetBrains Mono',monospace;color:#c7d2fe;transition:.2s}
  .chip:hover{background:rgba(99,102,241,.4);transform:scale(1.05)}
  .warn{color:#fbbf24;font-size:13px;margin-top:8px}
  .list-info{font-size:12px;color:#94a3b8;margin-bottom:8px}
  ::-webkit-scrollbar{width:5px;height:5px}
  ::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:3px}
  ::-webkit-scrollbar-thumb{background:rgba(99,102,241,.5);border-radius:3px}
</style>
</head>
<body>

<div class="card">
  <div class="card-title">⚙️ 설정</div>
  <div class="row">
    <div class="ctrl">
      <label>자릿수 n = <span id="nVal" class="val">4</span></label>
      <input type="range" id="nRange" min="1" max="6" value="4">
    </div>
    <div class="ctrl">
      <label>문자 종류 k = <span id="kVal" class="val">10</span></label>
      <input type="range" id="kRange" min="2" max="10" value="10">
    </div>
  </div>
  <div style="font-size:12px;color:#94a3b8;font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px">사용 문자</div>
  <div id="charsDisplay" class="chars-display"></div>
</div>

<div class="card">
  <div class="formula-box">
    <div class="formula" id="formula">10⁴ = 10,000가지</div>
    <div class="sub" id="sub">서로 다른 10가지 숫자 중 중복을 허용하여 4자리를 만들 때</div>
  </div>
  <div class="compare">
    <div class="cbox highlight">
      <div class="lbl">중복순열 (중복 허용)</div>
      <div class="num" id="repVal">10,000</div>
      <div class="formula-lbl" id="repFormula">10⁴</div>
    </div>
    <div class="cbox">
      <div class="lbl">순열 (중복 불가)</div>
      <div class="num" id="permVal">5,040</div>
      <div class="formula-lbl" id="permFormula">₁₀P₄</div>
    </div>
  </div>
</div>

<div class="card">
  <div class="card-title">📋 전체 목록</div>
  <div class="list-info" id="listInfo"></div>
  <div class="list-wrap">
    <div class="list-grid" id="listGrid"></div>
  </div>
  <div class="warn" id="warnMsg"></div>
</div>

<script>
const ALL_CHARS = ['0','1','2','3','4','5','6','7','8','9'];

const nRange = document.getElementById('nRange');
const kRange = document.getElementById('kRange');
const nVal   = document.getElementById('nVal');
const kVal   = document.getElementById('kVal');

function superscript(n) {
  const sup = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
  return String(n).split('').map(c => sup[c]||c).join('');
}
function subscript(n) {
  const sub = {'0':'₀','1':'₁','2':'₂','3':'₃','4':'₄','5':'₅','6':'₆','7':'₇','8':'₈','9':'₉','1':'₁','0':'₀'};
  return String(n).split('').map(c => sub[c]||c).join('');
}
function perm(n, r) {
  if (r > n) return 0;
  let r2 = 1; for (let i = n; i > n - r; i--) r2 *= i; return r2;
}
function* cartesian(arr, n) {
  if (n === 0) { yield []; return; }
  for (const rest of cartesian(arr, n - 1))
    for (const a of arr) yield [a, ...rest];
}

function update() {
  const n = parseInt(nRange.value);
  const k = parseInt(kRange.value);
  nVal.textContent = n;
  kVal.textContent = k;

  const chars = ALL_CHARS.slice(0, k);
  const BASE_COLORS = ['#6366f1','#0ea5e9','#10b981','#f59e0b','#ef4444','#a855f7','#ec4899','#14b8a6','#f97316','#84cc16'];
  const cd = document.getElementById('charsDisplay');
  cd.innerHTML = chars.map((c,i)=>`<span class="ch" style="background:${BASE_COLORS[i]};box-shadow:0 2px 8px ${BASE_COLORS[i]}66">${c}</span>`).join('');

  const rep  = Math.pow(k, n);
  const pm   = perm(k, n);

  document.getElementById('formula').textContent = `${k}${superscript(n)} = ${rep.toLocaleString()}가지`;
  document.getElementById('sub').textContent = `서로 다른 ${k}가지 숫자 중 중복을 허용하여 ${n}자리를 만들 때`;

  document.getElementById('repVal').textContent = rep.toLocaleString();
  document.getElementById('repFormula').textContent = `${k}${superscript(n)}`;
  document.getElementById('permVal').textContent = pm > 0 ? pm.toLocaleString() : '—';
  document.getElementById('permFormula').textContent = k >= n ? `${subscript(k)}P${subscript(n)}` : '(k < n이면 불가)';

  const MAX = 500;
  const grid = document.getElementById('listGrid');
  const warn = document.getElementById('warnMsg');
  const info = document.getElementById('listInfo');

  grid.innerHTML = '';
  if (rep <= MAX) {
    warn.textContent = '';
    info.textContent = `${rep}가지 전체 표시`;
    for (const combo of cartesian(chars, n)) {
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = combo.join('');
      grid.appendChild(chip);
    }
  } else {
    info.textContent = `처음 ${MAX}개 미리보기`;
    let count = 0;
    for (const combo of cartesian(chars, n)) {
      if (count >= MAX) break;
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = combo.join('');
      grid.appendChild(chip);
      count++;
    }
    warn.textContent = `⚠ 총 ${rep.toLocaleString()}가지 중 처음 ${MAX}개만 표시합니다.`;
  }
}

nRange.addEventListener('input', update);
kRange.addEventListener('input', update);
update();
</script>
</body>
</html>
""", height=720)
    _render_quiz(_SHEET_NAME)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


def _render_quiz(sheet_name: str):
    st.divider()
    st.subheader("🧩 확인 문제")
    st.caption("활동을 바탕으로 아래 문제를 풀어보세요. 답을 입력하고 **채점하기** 버튼을 눌러주세요.")

    QUIZ = [
        {
            "q": "0~9의 숫자를 사용하여 만들 수 있는 4자리 비밀번호의 수는 모두 몇 가지인지 구하시오. 단, 각 자리에 같은 숫자를 반복 사용할 수 있습니다.",
            "a": "10000",
            "hint": "10가지 숫자를 4자리에 중복 허용하여 나열합니다.",
            "sol": "각 자리마다 0~9 중 하나를 독립적으로 선택할 수 있으므로 $10^4 = 10{,}000$가지입니다."
        },
        {
            "q": "대소문자를 구별하지 않고 a~z 알파벳 26가지를 중복 허용하여 3자리 암호를 만들 때, 첫 번째 자리가 반드시 모음(a, e, i, o, u) 5가지 중 하나여야 한다면 만들 수 있는 암호는 모두 몇 가지인지 구하시오.",
            "a": "3380",
            "hint": "첫 번째 자리 5가지, 나머지 두 자리는 각각 26가지입니다.",
            "sol": "첫 번째 자리: 5가지 (모음), 나머지 두 자리: 26가지씩 → $5 \\times 26^2 = 5 \\times 676 = 3{,}380$가지입니다."
        },
        {
            "q": "0~9의 숫자를 중복 허용하여 4자리 비밀번호를 만들 때와, 중복 없이(같은 숫자 불가) 4자리 비밀번호를 만들 때의 경우의 수의 차를 구하시오.",
            "a": "4960",
            "hint": "중복 허용: $10^4$, 중복 불가: $_{10}P_4$를 계산하여 뺍니다.",
            "sol": "중복 허용: $10^4 = 10{,}000$가지, 중복 불가: $_{10}P_4 = 10 \\times 9 \\times 8 \\times 7 = 5{,}040$가지 → 차: $10{,}000 - 5{,}040 = 4{,}960$가지입니다."
        },
    ]

    quiz_data = QUIZ
    if f"quiz_checked_{sheet_name}" not in st.session_state:
        st.session_state[f"quiz_checked_{sheet_name}"] = [False, False, False]

    for i, item in enumerate(quiz_data):
        with st.container():
            st.markdown(f"**문제 {i+1}.** {item['q']}")
            col1, col2 = st.columns([3, 1])
            with col1:
                user_ans = st.text_input(f"답 입력 (문제 {i+1})", key=f"pw_q{i+1}", label_visibility="collapsed", placeholder="답을 입력하세요")
            with col2:
                check = st.button("채점하기", key=f"pw_check{i+1}", use_container_width=True)

            if check and user_ans.strip():
                correct = str(item['a']).strip()
                user_stripped = user_ans.strip().replace(',', '').replace(' ', '')
                correct_stripped = str(item['a']).replace(',', '').replace(' ', '')
                is_correct = user_stripped == correct_stripped
                if is_correct:
                    st.success("✅ 정답입니다!")
                else:
                    st.error(f"❌ 틀렸습니다. 정답은 **{item['a']}** 입니다.")
                with st.expander("💡 풀이 보기"):
                    st.markdown(item['sol'])
            elif check and not user_ans.strip():
                st.warning("답을 입력해주세요.")
        st.markdown("---")
