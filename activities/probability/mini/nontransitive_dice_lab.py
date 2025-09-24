import json
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "비정규 주사위 대결 실험 (A/B/C 커스텀·6칸 입력)",
    "description": "세 주사위의 6면을 직접 입력하고, 한 번/두 번 합 비교의 승률을 이론·시뮬레이션으로 확인 + p5.js 굴리기 애니메이션",
    "order": 35,
}

# ─────────────────────────────────────────────────────────────────────────────
# 계산 유틸
def prob_single_gt(F: list[int], G: list[int]) -> tuple[float, float, float]:
    """한 번 던지기: P(F>G), P(F<G), P(F=G)."""
    F_arr = np.array(F)
    G_arr = np.array(G)
    m, n = len(F_arr), len(G_arr)
    gt = (F_arr[:, None] > G_arr[None, :]).sum()
    lt = (F_arr[:, None] < G_arr[None, :]).sum()
    eq = m * n - gt - lt
    tot = m * n
    return gt / tot, lt / tot, eq / tot

def sum_distribution(F: list[int]) -> dict[int, int]:
    """두 번 던져 합의 분포: 합 -> 경우의 수(순서쌍 포함)."""
    A = np.array(F)
    sums = (A[:, None] + A[None, :]).ravel()
    u, c = np.unique(sums, return_counts=True)
    return dict(zip(u.tolist(), c.tolist()))

def prob_double_sum_gt(F: list[int], G: list[int]) -> tuple[float, float, float]:
    """두 번 합 비교: P(SF>SG), P(SF<SG), P(SF=SG) 정확 계산."""
    import bisect
    dF = sum_distribution(F)
    dG = sum_distribution(G)
    totF = len(F) * len(F)
    totG = len(G) * len(G)
    sF = sorted(dF.items())  # (합, cnt)
    sG = sorted(dG.items())
    g_keys = [k for k, _ in sG]
    g_cnts = np.array([c for _, c in sG], dtype=np.int64)
    g_cum = np.cumsum(g_cnts)
    gt = 0
    eq = 0
    for s, cF in sF:
        idx = bisect.bisect_left(g_keys, s)   # s 미만
        g_less = g_cum[idx - 1] if idx > 0 else 0
        gt += cF * g_less
        if idx < len(g_keys) and g_keys[idx] == s:
            eq += cF * dG[s]
    total = totF * totG
    lt = total - gt - eq
    return gt / total, lt / total, eq / total

def simulate_vs(F: list[int], G: list[int], trials: int, mode: str = "single", seed: int | None = None) -> tuple[float, float, float]:
    """시뮬레이션 승/패/무 추정."""
    rng = np.random.default_rng(seed)
    m, n = len(F), len(G)
    F_arr = np.array(F, dtype=int)
    G_arr = np.array(G, dtype=int)

    if mode == "single":
        rollF = F_arr[rng.integers(0, m, size=trials)]
        rollG = G_arr[rng.integers(0, n, size=trials)]
    else:
        rollF = F_arr[rng.integers(0, m, size=trials)] + F_arr[rng.integers(0, m, size=trials)]
        rollG = G_arr[rng.integers(0, n, size=trials)] + G_arr[rng.integers(0, n, size=trials)]

    gt = (rollF > rollG).sum()
    lt = (rollF < rollG).sum()
    eq = trials - gt - lt
    return gt / trials, lt / trials, eq / trials

def pairwise_table(names: list[str], probs: dict[tuple[str, str], tuple[float, float, float]]) -> pd.DataFrame:
    """행이 열을 이길 확률 P(row > col) 매트릭스."""
    mat = []
    for r in names:
        row = []
        for c in names:
            if r == c:
                row.append(np.nan)
            else:
                row.append(probs[(r, c)][0])
        mat.append(row)
    return pd.DataFrame(mat, index=names, columns=names)

def nontransitive_arrow(df_win: pd.DataFrame, names=("A", "B", "C")) -> str | None:
    a, b, c = names
    try:
        if df_win.loc[a, b] > 0.5 and df_win.loc[b, c] > 0.5 and df_win.loc[c, a] > 0.5:
            return f"{a} → {b} → {c} → {a}"
    except Exception:
        pass
    return None

# ─────────────────────────────────────────────────────────────────────────────
# UI 유틸
def six_face_inputs(label: str, defaults: list[int]) -> list[int]:
    st.caption(f"**{label}** 면값(6칸)")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    boxes = []
    for i, (c, d) in enumerate(zip([c1, c2, c3, c4, c5, c6], defaults), start=1):
        with c:
            v = st.number_input(f"{label}{i}", value=int(d), step=1, format="%d", key=f"{label}_f{i}")
            boxes.append(int(v))
    return boxes

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.header("🎲 비정규 주사위 실험실 (6칸 입력 + 이론/시뮬 + 애니메이션)")

    with st.expander("면값 설정 (각 6칸)", expanded=True):
        colA, colB, colC = st.columns(3)
        with colA:
            A = six_face_inputs("A", [3, 3, 3, 3, 3, 6])
        with colB:
            B = six_face_inputs("B", [2, 2, 2, 5, 5, 5])
        with colC:
            C = six_face_inputs("C", [1, 4, 4, 4, 4, 4])

    names = ["A", "B", "C"]
    dice = {"A": A, "B": B, "C": C}

    # 요약(각 주사위의 값 분포)
    st.subheader("주사위 값 분포 요약")
    c1, c2, c3 = st.columns(3)
    for (nm, F), c in zip(dice.items(), (c1, c2, c3)):
        with c:
            s = pd.Series(F)
            st.metric(f"{nm} 면 개수", len(F))
            st.dataframe(s.value_counts().sort_index(), use_container_width=True, height=150)

    st.divider()

    # 비교 모드 설정 + 시뮬레이션
    st.subheader("모드 선택 및 시뮬레이션")
    mode = st.radio("비교 모드", ["한 번 던져 큰 수 승", "한 주사위를 두 번 던져 **합** 비교"], horizontal=True)
    mode_key = "single" if mode.startswith("한 번") else "double"

    colL, colR = st.columns([2, 1])
    with colR:
        trials = st.slider("시뮬레이션 시행 수", 100, 200_000, 20_000, step=1000)
        seed = st.number_input("난수 시드(0=랜덤)", value=0, min_value=0, step=1, format="%d")
        run = st.button("🔁 시뮬레이션 실행", use_container_width=True)

    # 정확 계산 (항상 즉시 계산)
    exact = {}
    for x in names:
        for y in names:
            if x == y:
                continue
            if mode_key == "single":
                exact[(x, y)] = prob_single_gt(dice[x], dice[y])
            else:
                exact[(x, y)] = prob_double_sum_gt(dice[x], dice[y])

    df_exact = pairwise_table(names, exact)

    # 시뮬레이션 (버튼 눌렀을 때/초기 표시)
    if "nd_sim" not in st.session_state or run:
        sim = {}
        rng_seed_base = None if seed == 0 else seed
        for i, x in enumerate(names):
            for j, y in enumerate(names):
                if x == y:
                    continue
                sim[(x, y)] = simulate_vs(
                    dice[x], dice[y], trials=trials, mode=mode_key,
                    seed=(None if rng_seed_base is None else rng_seed_base + i * 10 + j)
                )
        st.session_state["nd_sim"] = sim
        st.session_state["nd_trials"] = trials
        st.session_state["nd_mode"] = mode_key
    sim = st.session_state["nd_sim"]

    df_sim = pairwise_table(names, sim)

    with colL:
        st.write("**행이 열을 이길 확률(이론)**")
        st.dataframe((df_exact * 100).round(2), use_container_width=True)
    with colR:
        st.write("**행이 열을 이길 확률(시뮬)**")
        st.dataframe((df_sim * 100).round(2), use_container_width=True)

    diff = (df_sim - df_exact)
    st.write("**시뮬 − 이론 (오차, %p)**")
    st.dataframe((diff * 100).round(2), use_container_width=True)

    note = nontransitive_arrow(df_exact, names)
    if note:
        st.success(f"🔄 비추이성 패턴 감지: **{note}**  (모드: {'1회' if mode_key=='single' else '2회 합'})")

    # 자세한 승/패/무 표
    st.markdown("### 세부 표 (승/패/무)")
    rows = []
    for x in names:
        for y in names:
            if x == y:
                continue
            ex = exact[(x, y)]
            si = sim[(x, y)]
            rows.append({
                "대결": f"{x} vs {y}",
                "이론 P(win/lose/tie)": f"{ex[0]:.3f} / {ex[1]:.3f} / {ex[2]:.3f}",
                "시뮬 P(win/lose/tie)": f"{si[0]:.3f} / {si[1]:.3f} / {si[2]:.3f}",
            })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()

    # ─────────────────────────────────────────────────────────────────────────
    # p5.js 애니메이션: 선택한 두 주사위를 굴려서 결과를 시각화(1회/2회합)
    st.subheader("🎞️ p5.js 애니메이션: 주사위 굴리기")
    pair = st.selectbox("시각화할 대결", ["A vs B", "A vs C", "B vs C"])
    vis_mode = st.radio("애니메이션 모드", ["한 번 던지기", "두 번 던져 합"], horizontal=True)
    left, right = pair.split(" vs ")
    faces_payload = {
        "A": A, "B": B, "C": C,
        "left": left, "right": right,
        "mode": ("single" if vis_mode.startswith("한 번") else "double")
    }

    html = f"""
    <div id="wrap" style="width:100%;max-width:900px;margin:0 auto;">
      <div style="margin:.25rem 0 .5rem 0;">
        <button id="rollBtn" style="padding:.5rem 1rem;">🎲 ROLL</button>
        <span id="resultLabel" style="margin-left:12px;font-weight:600;"></span>
      </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
    <script>
    const DICE = {json.dumps(faces_payload)};
    function choice(arr) {{ return arr[Math.floor(Math.random()*arr.length)]; }}

    let W=900,H=280, rolling=0, targetL=[], targetR=[], shownL=[], shownR=[];
    function setup(){{
      const cnv = createCanvas(W,H);
      cnv.parent(document.getElementById('wrap'));
      textFont('Helvetica'); textAlign(CENTER,CENTER);
      resetShown();
      document.getElementById('rollBtn').onclick = triggerRoll;
    }}
    function resetShown(){{
      shownL = [choice(DICE[DICE.left])];
      shownR = [choice(DICE[DICE.right])];
    }}
    function triggerRoll(){{
      const left = DICE.left, right = DICE.right;
      if (DICE.mode==='single') {{
        targetL = [choice(DICE[left])];
        targetR = [choice(DICE[right])];
      }} else {{
        targetL = [choice(DICE[left]), choice(DICE[left])];
        targetR = [choice(DICE[right]), choice(DICE[right])];
      }}
      rolling = 22; // 프레임 수
      document.getElementById('resultLabel').textContent = '';
    }}
    function draw(){{
      background(255);
      noStroke();
      // 라벨
      fill(0); textSize(16);
      text(DICE.left + "  vs  " + DICE.right + "   ("+(DICE.mode==='single'?'1회':'2회합')+")", width/2, 18);
      // 판
      drawDiePanel(width*0.25-90, 50, shownL, '#1976D2');
      drawDiePanel(width*0.75-90, 50, shownR, '#C62828');

      if(rolling>0){{
        // 구르는 연출: 매 프레임 랜덤값 보여주기
        if (DICE.mode==='single') {{
          shownL = [choice(DICE[DICE.left])];
          shownR = [choice(DICE[DICE.right])];
        }} else {{
          shownL = [choice(DICE[DICE.left]), choice(DICE[DICE.left])];
          shownR = [choice(DICE[DICE.right]), choice(DICE[DICE.right])];
        }}
        rolling--;
        if(rolling===0){{
          shownL = targetL.slice();
          shownR = targetR.slice();
          // 승자 계산
          const sumL = shownL.reduce((a,b)=>a+b,0);
          const sumR = shownR.reduce((a,b)=>a+b,0);
          let msg = '';
          if (sumL>sumR) msg = DICE.left + " 승 ("+sumL+" > "+sumR+")";
          else if (sumL<sumR) msg = DICE.right + " 승 ("+sumL+" < "+sumR+")";
          else msg = "무승부 ("+sumL+" = "+sumR+")";
          document.getElementById('resultLabel').textContent = msg;
        }}
      }}
    }}
    function drawDiePanel(x,y,vals, baseColor){{
      const isDouble = (DICE.mode!=='single');
      const boxW=180, boxH=isDouble?190:160;
      // 프레임
      push();
      stroke('#999'); fill('#FAFAFA'); strokeWeight(1.2);
      rect(x,y, boxW, boxH, 12);
      // 주사위(1개 또는 2개)
      const dy = isDouble? 64 : 48;
      for(let i=0;i<vals.length;i++){{
        drawDie(x+boxW/2 - 55 + (isDouble? i*110:0), y+60, 80, vals[i], baseColor);
      }}
      // 합
      const s = vals.reduce((a,b)=>a+b,0);
      noStroke(); fill('#333'); textSize(18);
      text("합: "+s, x+boxW/2, y+boxH-22);
      pop();
    }}
    function drawDie(cx, cy, size, val, colorHex){{
      push();
      rectMode(CENTER);
      stroke('#333'); strokeWeight(2); fill(colorHex);
      rect(cx, cy, size, size, 14);
      fill('#fff'); textSize(28); text(val, cx, cy);
      pop();
    }}
    </script>
    """
    components.html(html, height=330)
