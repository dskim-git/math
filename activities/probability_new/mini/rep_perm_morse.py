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
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0a1a 0%,#0d1b2a 50%,#0a0a1a 100%);min-height:100vh;padding:16px;color:#e2e8f0}
  .card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:20px 24px;margin:12px 0;backdrop-filter:blur(10px)}
  .card-title{font-size:15px;font-weight:700;color:#67e8f9;margin-bottom:14px;display:flex;align-items:center;gap:8px;letter-spacing:.02em}
  .ctrl label{font-size:12px;color:#94a3b8;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .ctrl input[type=range]{width:220px;-webkit-appearance:none;height:6px;border-radius:3px;background:linear-gradient(90deg,#0ea5e9,#06b6d4);outline:none;margin-top:8px;display:block}
  .ctrl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#fff;border:3px solid #0ea5e9;cursor:pointer;box-shadow:0 0 10px rgba(14,165,233,.6)}
  .val{display:inline-block;min-width:36px;background:linear-gradient(135deg,#0ea5e9,#06b6d4);border-radius:10px;padding:3px 10px;font-weight:800;font-size:17px;text-align:center;color:#fff;box-shadow:0 2px 12px rgba(14,165,233,.5)}
  .formula-box{background:rgba(14,165,233,.1);border:1px solid rgba(14,165,233,.25);border-radius:14px;padding:14px 20px;margin:14px 0;text-align:center}
  .formula{font-size:26px;font-weight:800;color:#67e8f9;margin-bottom:4px}
  .sub{font-size:13px;color:#94a3b8}
  .legend{display:flex;gap:24px;margin:14px 0;flex-wrap:wrap}
  .leg-item{display:flex;gap:8px;align-items:center;font-size:13px;color:#cbd5e1;font-weight:600}
  .dot-demo{width:12px;height:12px;border-radius:50%;background:#67e8f9;box-shadow:0 0 8px #67e8f9}
  .dash-demo{width:30px;height:10px;border-radius:5px;background:#f472b6;box-shadow:0 0 8px #f472b6}
  .info-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:4px}
  .kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:12px 24px;text-align:center;min-width:110px}
  .kpi .num{font-size:32px;font-weight:900;color:#e2e8f0}
  .kpi .lbl{font-size:11px;color:#94a3b8;margin-top:4px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .signal-grid{display:flex;flex-wrap:wrap;gap:8px;max-height:340px;overflow-y:auto;padding:10px}
  .signal{display:flex;gap:5px;align-items:center;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:8px 10px;cursor:pointer;transition:.2s}
  .signal:hover{background:rgba(14,165,233,.15);border-color:rgba(14,165,233,.4);transform:scale(1.03)}
  .dot{width:10px;height:10px;border-radius:50%;background:#67e8f9;box-shadow:0 0 6px #67e8f9;flex-shrink:0}
  .dash{width:26px;height:10px;border-radius:5px;background:#f472b6;box-shadow:0 0 6px #f472b6;flex-shrink:0}
  .idx{font-size:10px;color:#64748b;margin-left:4px}
  ::-webkit-scrollbar{width:5px;height:5px}
  ::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
  ::-webkit-scrollbar-thumb{background:rgba(14,165,233,.4);border-radius:3px}
</style>
</head>
<body>

<div class="card">
  <div class="card-title">⚙️ 신호 길이 설정</div>
  <div class="ctrl">
    <label>신호 길이 n = <span id="nVal" class="val">3</span></label>
    <input type="range" id="nRange" min="1" max="6" value="3">
  </div>
  <div class="legend">
    <div class="leg-item"><div class="dot-demo"></div> 점 (·)</div>
    <div class="leg-item"><div class="dash-demo"></div> 선 (−)</div>
  </div>
  <div class="formula-box">
    <div class="formula" id="formula">2³ = 8가지</div>
    <div class="sub" id="sub">2가지 기호 중 중복을 허용하여 3자리를 나열: ₂Π₃ = 2³ = 8</div>
  </div>
  <div class="info-row">
    <div class="kpi"><div class="num" id="totalNum">8</div><div class="lbl">총 경우의 수</div></div>
    <div class="kpi"><div class="num" id="pow2">2³</div><div class="lbl">공식 2ⁿ</div></div>
  </div>
</div>

<div class="card">
  <div class="card-title">📡 모든 신호 조합</div>
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
  document.getElementById('sub').textContent =
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
    _render_quiz(_SHEET_NAME)
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_quiz(sheet_name: str):
    st.divider()
    st.subheader("🧩 확인 문제")
    st.caption("활동을 바탕으로 아래 문제를 풀어보세요. 답을 입력하고 **채점하기** 버튼을 눌러주세요.")

    QUIZ = [
        {
            "q": "모스 부호에서 점(·)과 선(−) 2가지 기호를 사용하여 길이 1~4의 신호를 모두 만들 때, 서로 다른 신호는 모두 몇 가지인지 구하시오. (길이 1짜리, 2짜리, 3짜리, 4짜리를 모두 합산)",
            "a": "30",
            "hint": "길이별로 각각 $2^1, 2^2, 2^3, 2^4$가지를 모두 더합니다.",
            "sol": "길이 1: $2^1 = 2$, 길이 2: $2^2 = 4$, 길이 3: $2^3 = 8$, 길이 4: $2^4 = 16$\n\n합계: $2 + 4 + 8 + 16 = 30$가지입니다."
        },
        {
            "q": "점(·)과 선(−) 이외에 '공백(□)' 기호를 추가하여 총 3가지 기호로 길이 4짜리 신호를 만들 때, 경우의 수는 모두 몇 가지인지 구하시오.",
            "a": "81",
            "hint": "3가지 기호를 4자리에 중복 허용하여 나열합니다.",
            "sol": "3가지 기호를 중복 허용하여 4자리 나열 → $3^4 = 81$가지입니다."
        },
        {
            "q": "모스 부호 2가지 기호로 n자리 신호를 만들 때, 경우의 수가 처음으로 100을 넘는 n의 값은 무엇인지 구하시오.",
            "a": "7",
            "hint": "$2^n > 100$을 만족하는 최솟값 n을 찾아보세요.",
            "sol": "$2^6 = 64 \\leq 100$, $2^7 = 128 > 100$\n\n따라서 $n = 7$입니다."
        },
    ]

    for i, item in enumerate(QUIZ):
        with st.container():
            st.markdown(f"**문제 {i+1}.** {item['q']}")
            col1, col2 = st.columns([3, 1])
            with col1:
                user_ans = st.text_input(f"답 입력 (문제 {i+1})", key=f"morse_q{i+1}", label_visibility="collapsed", placeholder="답을 입력하세요")
            with col2:
                check = st.button("채점하기", key=f"morse_check{i+1}", use_container_width=True)

            if check and user_ans.strip():
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
