import streamlit as st
import streamlit.components.v1 as components
import requests
import datetime

_GAS_URL = "https://script.google.com/macros/s/AKfycbwJd7W3jYTucIALzqNJUyHvmnT3nqDCEmRZXAsBlBl3IWQYhuYqyvkI3B280chlr0g/exec"
_SHEET_NAME = "모스부호"

META = {
    "title": "미니: 모스 부호와 중복순열",
    "description": "점(·)과 선(−) 2가지 기호로 n자리 신호를 만들 때 2ⁿ가지 경우를 시각화합니다.",
    "order": 999999,
    "hidden": True,
}

def render():
    st.header("📡 모스 부호와 중복순열")
    st.markdown("""
- 모스 부호는 **점(·)** 과 **선(−)** 2가지 기호만 사용합니다.
- $n$자리 신호를 만들 때 가능한 조합의 수는 $2^n$가지 → **중복순열** $\\_{2}\\Pi_{n} = 2^n$
- 아래에서 신호 길이를 바꾸며 모든 조합을 직접 확인해 보세요.
""")

    components.html("""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  body { font-family: system-ui, sans-serif; margin: 0; padding: 8px 12px 24px; background: #f8fafc; }
  .card { background: #fff; border: 1px solid #e5e7eb; border-radius: 14px; padding: 16px 20px; margin: 10px 0; }
  h3 { margin: 0 0 10px; font-size: 16px; }
  .ctrl label { font-size: 13px; color: #6b7280; font-weight: 600; }
  .val { display: inline-block; min-width: 28px; background: #eef2ff; border: 1px solid #c7d2fe;
         border-radius: 8px; padding: 2px 8px; font-weight: 700; font-size: 15px; text-align: center; }
  .formula { font-size: 22px; font-weight: 700; color: #1e40af; margin: 8px 0 4px; }
  .sub { font-size: 13px; color: #6b7280; margin-bottom: 12px; }
  .tree-wrap { overflow-x: auto; }
  .signal-grid { display: flex; flex-wrap: wrap; gap: 8px; max-height: 360px; overflow-y: auto;
                  padding: 8px; border: 1px solid #e5e7eb; border-radius: 10px; background: #f9fafb; }
  .signal { display: flex; gap: 3px; align-items: center; background: #fff;
             border: 1px solid #e5e7eb; border-radius: 8px; padding: 5px 8px; }
  .dot  { width: 8px; height: 8px; border-radius: 50%; background: #2563eb; }
  .dash { width: 22px; height: 8px; border-radius: 4px; background: #dc2626; }
  .legend { display: flex; gap: 16px; margin-bottom: 10px; font-size: 13px; }
  .leg-item { display: flex; gap: 6px; align-items: center; }
  .idx { font-size: 11px; color: #9ca3af; margin-top: 2px; }
  .highlight { border-color: #6366f1 !important; background: #eef2ff !important; }
  .info-row { display: flex; gap: 24px; align-items: center; flex-wrap: wrap; }
  .kpi { border: 1px solid #e5e7eb; border-radius: 12px; padding: 10px 20px; text-align: center; }
  .kpi .num { font-size: 28px; font-weight: 800; color: #111827; }
  .kpi .lbl { font-size: 12px; color: #6b7280; }
</style>
</head>
<body>

<div class="card">
  <h3>🎛 신호 길이 설정</h3>
  <div class="ctrl">
    <label>신호 길이 n = <span id="nVal" class="val">3</span></label><br>
    <input type="range" id="nRange" min="1" max="6" value="3" style="width:220px;margin-top:6px;">
  </div>

  <div class="legend" style="margin-top:12px;">
    <div class="leg-item"><div class="dot"></div> 점 (·)</div>
    <div class="leg-item"><div class="dash"></div> 선 (−)</div>
  </div>

  <div class="formula" id="formula">2³ = 8가지</div>
  <div class="sub">2가지 기호 중 중복을 허용하여 3자리를 나열: ₂Π₃ = 2³ = 8</div>

  <div class="info-row">
    <div class="kpi"><div class="num" id="totalNum">8</div><div class="lbl">총 경우의 수</div></div>
    <div class="kpi"><div class="num" id="pow2">2³</div><div class="lbl">공식 2ⁿ</div></div>
  </div>
</div>

<div class="card">
  <h3>📋 모든 신호 조합</h3>
  <div class="signal-grid" id="grid"></div>
</div>

<script>
const nRange = document.getElementById('nRange');
const nValEl = document.getElementById('nVal');

function superscript(n) {
  const sup = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶'};
  return String(n).split('').map(c => sup[c] || c).join('');
}

function* cartesian2(n) {
  if (n === 0) { yield []; return; }
  for (const rest of cartesian2(n - 1))
    for (const s of [0, 1]) yield [s, ...rest];
}

function update() {
  const n = parseInt(nRange.value);
  nValEl.textContent = n;
  const total = Math.pow(2, n);

  document.getElementById('formula').textContent = `2${superscript(n)} = ${total}가지`;
  document.querySelector('.sub').textContent =
    `2가지 기호 중 중복을 허용하여 ${n}자리를 나열: ₂Π${n} = 2${superscript(n)} = ${total}`;
  document.getElementById('totalNum').textContent = total;
  document.getElementById('pow2').textContent = `2${superscript(n)}`;

  const grid = document.getElementById('grid');
  grid.innerHTML = '';

  let i = 1;
  for (const combo of cartesian2(n)) {
    const div = document.createElement('div');
    div.className = 'signal';
    div.title = combo.map(s => s === 0 ? '·' : '−').join('');

    for (const s of combo) {
      const el = document.createElement('div');
      el.className = s === 0 ? 'dot' : 'dash';
      div.appendChild(el);
    }

    const idx = document.createElement('div');
    idx.className = 'idx';
    idx.textContent = i++;
    div.appendChild(idx);

    grid.appendChild(div);
  }
}

nRange.addEventListener('input', update);
update();
</script>
</body>
</html>
""", height=680)
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
                    st.balloons()
                else:
                    st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"제출 실패: {e}")
