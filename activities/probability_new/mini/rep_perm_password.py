import streamlit as st
import streamlit.components.v1 as components
import requests
import datetime

# ──────────────────────────────────────────────────────────
# Google Apps Script Web App URL
# 배포 후 아래 문자열을 실제 URL로 교체하세요.
_GAS_URL = "https://script.google.com/macros/s/AKfycbwJd7W3jYTucIALzqNJUyHvmnT3nqDCEmRZXAsBlBl3IWQYhuYqyvkI3B280chlr0g/exec"
_SHEET_NAME = "비밀번호탐색기"

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
  body { font-family: system-ui, sans-serif; margin: 0; padding: 8px 12px 24px; background: #f8fafc; }
  .card { background: #fff; border: 1px solid #e5e7eb; border-radius: 14px; padding: 16px 20px; margin: 10px 0; }
  .row { display: flex; gap: 32px; flex-wrap: wrap; align-items: flex-start; margin-bottom: 12px; }
  .ctrl label { display: block; font-size: 13px; color: #6b7280; margin-bottom: 4px; font-weight: 600; }
  .ctrl input[type=range] { width: 200px; }
  .val { display: inline-block; min-width: 32px; background: #eef2ff; border: 1px solid #c7d2fe;
          border-radius: 8px; padding: 2px 8px; font-weight: 700; font-size: 15px; text-align: center; }
  .formula { font-size: 22px; font-weight: 700; color: #1e40af; margin: 4px 0 12px; }
  .sub { font-size: 13px; color: #6b7280; }
  .list-wrap { max-height: 320px; overflow-y: auto; border: 1px solid #e5e7eb; border-radius: 10px;
               padding: 10px; background: #f9fafb; }
  .list-grid { display: flex; flex-wrap: wrap; gap: 6px; }
  .chip { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;
          padding: 3px 8px; font-size: 13px; font-family: monospace; }
  .warn { color: #b45309; font-size: 13px; margin-top: 6px; }
  .chars-display { display: flex; gap: 6px; flex-wrap: wrap; margin: 6px 0 10px; }
  .ch { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;
        padding: 4px 10px; font-weight: 700; font-size: 15px; }
  h3 { margin: 0 0 10px; font-size: 16px; }
  .compare { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
  .cbox { border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px; text-align: center; }
  .cbox .lbl { font-size: 12px; color: #6b7280; }
  .cbox .num { font-size: 26px; font-weight: 800; color: #111827; }
</style>
</head>
<body>

<div class="card">
  <h3>🎛 설정</h3>
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

  <div>사용 문자: <span id="charsDisplay" class="chars-display"></span></div>

  <div class="formula" id="formula"></div>
  <div class="sub" id="sub"></div>
</div>

<div class="card">
  <div class="compare">
    <div class="cbox">
      <div class="lbl">중복순열 수 (중복 허용)</div>
      <div class="num" id="repVal">—</div>
      <div class="lbl" id="repFormula"></div>
    </div>
    <div class="cbox">
      <div class="lbl">순열 수 (중복 불가)</div>
      <div class="num" id="permVal">—</div>
      <div class="lbl" id="permFormula"></div>
    </div>
  </div>
</div>

<div class="card" id="listCard">
  <h3>📋 전체 목록 <span id="listInfo" class="sub"></span></h3>
  <div class="list-wrap">
    <div class="list-grid" id="listGrid"></div>
  </div>
  <div class="warn" id="warnMsg"></div>
</div>

<script>
const ALL_CHARS = ['0','1','2','3','4','5','6','7','8','9'];
const COLORS = ['🔴','🟠','🟡','🟢','🔵','🟣','🟤','⚫','⚪','🩷'];

const nRange = document.getElementById('nRange');
const kRange = document.getElementById('kRange');
const nVal   = document.getElementById('nVal');
const kVal   = document.getElementById('kVal');

function factorial(x) {
  if (x <= 1) return 1;
  let r = 1; for (let i = 2; i <= x; i++) r *= i; return r;
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
  const cd = document.getElementById('charsDisplay');
  cd.innerHTML = chars.map(c => `<span class="ch">${c}</span>`).join('');

  const rep  = Math.pow(k, n);
  const pm   = perm(k, n);

  document.getElementById('formula').textContent = `경우의 수: ${k}^${n} = ${rep.toLocaleString()}가지`;
  document.getElementById('sub').textContent = `서로 다른 ${k}가지 숫자 중 중복을 허용하여 ${n}자리를 만들 때`;

  document.getElementById('repVal').textContent = rep.toLocaleString();
  document.getElementById('repFormula').textContent = `${k}^${n}`;
  document.getElementById('permVal').textContent = pm.toLocaleString();
  document.getElementById('permFormula').textContent = k >= n ? `${k}P${n} = ${pm.toLocaleString()}` : '(k < n이므로 불가)';

  const MAX = 500;
  const grid = document.getElementById('listGrid');
  const warn = document.getElementById('warnMsg');
  const info = document.getElementById('listInfo');

  if (rep <= MAX) {
    grid.innerHTML = '';
    warn.textContent = '';
    info.textContent = `(${rep}가지 전체 표시)`;
    let count = 0;
    for (const combo of cartesian(chars, n)) {
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = combo.join('');
      grid.appendChild(chip);
      count++;
    }
  } else {
    grid.innerHTML = '';
    warn.textContent = `경우의 수가 ${rep.toLocaleString()}가지로 너무 많아 목록은 표시하지 않습니다.`;
    info.textContent = '';
    let count = 0;
    for (const combo of cartesian(chars, n)) {
      if (count >= MAX) break;
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = combo.join('');
      grid.appendChild(chip);
      count++;
    }
    warn.textContent += ` (처음 ${MAX}개만 미리보기)`;
  }
}

nRange.addEventListener('input', update);
kRange.addEventListener('input', update);
update();
</script>
</body>
</html>
""", height=700)
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_reflection_form(sheet_name: str, gas_url: str):
    st.divider()
    st.subheader("✍️ 활동 후 성찰 기록")
    st.caption("아래 질문에 답하고 **제출하기** 버튼을 눌러주세요.")

    with st.form(f"reflection_{sheet_name}", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            student_id = st.text_input("학번")
        with c2:
            name = st.text_input("이름")

        st.markdown("**📝 이 활동으로 해결할 수 있는 문제 3개 (문제와 답 모두 작성)**")
        q1 = st.text_area("문제 1", height=80)
        a1 = st.text_input("문제 1의 답")
        q2 = st.text_area("문제 2", height=80)
        a2 = st.text_input("문제 2의 답")
        q3 = st.text_area("문제 3", height=80)
        a3 = st.text_input("문제 3의 답")

        new_learning = st.text_area("💡 이 활동을 통해 새롭게 알게 된 점", height=100)
        feeling = st.text_area("💬 이 활동을 통해 느낀 점", height=100)

        submitted = st.form_submit_button("📤 제출하기", use_container_width=True, type="primary")

    if submitted:
        if not student_id or not name:
            st.warning("학번과 이름을 입력해주세요.")
        elif gas_url == "YOUR_GAS_WEB_APP_URL":
            st.error("⚠️ Google Sheets 연동 URL이 아직 설정되지 않았습니다. 선생님께 문의하세요.")
        else:
            payload = {
                "sheet":     sheet_name,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "학번":    student_id,
                "이름":    name,
                "문제1":   q1, "답1":  a1,
                "문제2":   q2, "답2":  a2,
                "문제3":   q3, "답3":  a3,
                "새롭게알게된점": new_learning,
                "느낀점":   feeling,
            }
            try:
                resp = requests.post(gas_url, json=payload, timeout=10)
                if resp.status_code == 200:
                    st.success(f"✅ {name}님의 활동 기록이 제출되었습니다!")
                else:
                    st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"제출 실패: {e}")
