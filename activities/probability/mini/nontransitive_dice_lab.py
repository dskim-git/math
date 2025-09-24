import streamlit as st
import numpy as np
import pandas as pd

META = {
    "title": "비정규 주사위 대결 실험 (A/B/C 커스텀)",
    "description": "세 주사위의 면값을 직접 설정하고, 한 번 던지기 / 두 번 합 비교의 승률을 이론·시뮬레이션으로 확인",
    "order": 35,  # 원하는 위치로 조정
}

# -----------------------------
# 유틸
# -----------------------------
def parse_faces(text: str) -> list[int]:
    """
    "3,3,3,3,3,6" → [3,3,3,3,3,6]
    공백 허용, 빈 값/문자 제거. 정수만 허용.
    """
    faces = []
    for tok in text.replace(" ", "").split(","):
        if tok == "":
            continue
        try:
            faces.append(int(tok))
        except Exception:
            raise ValueError(f"면값 '{tok}' 은(는) 정수가 아닙니다.")
    if not faces:
        raise ValueError("최소 1개의 면값이 필요합니다.")
    return faces

def prob_single_gt(F: list[int], G: list[int]) -> tuple[float,float,float]:
    """
    한 번 던지기: P(F>G), P(F<G), P(F=G).
    F, G는 '면 리스트' (중복 허용) → 모든 조합을 동일확률로 계산.
    """
    m, n = len(F), len(G)
    F_arr = np.array(F)
    G_arr = np.array(G)
    # 브로드캐스팅으로 모든 쌍 비교
    gt = (F_arr[:, None] > G_arr[None, :]).sum()
    lt = (F_arr[:, None] < G_arr[None, :]).sum()
    eq = m*n - gt - lt
    return gt/(m*n), lt/(m*n), eq/(m*n)

def sum_distribution(F: list[int]) -> dict[int, int]:
    """
    두 번 던져 합의 분포: 합값 -> (경우의 수)
    (중복 면 포함, 순서쌍 (i,j) 전부 카운트)
    """
    F_arr = np.array(F)
    sums = (F_arr[:, None] + F_arr[None, :]).ravel()
    unique, counts = np.unique(sums, return_counts=True)
    return dict(zip(unique.tolist(), counts.tolist()))

def prob_double_sum_gt(F: list[int], G: list[int]) -> tuple[float,float,float]:
    """
    두 번 던져 합 비교: P(SF>SG), P(SF<SG), P(SF=SG)
    분포 컨볼루션을 정밀 계산으로 비교.
    """
    dF = sum_distribution(F)  # 합 s의 경우의 수
    dG = sum_distribution(G)
    totF = len(F) * len(F)    # F의 합 경우의 수 전체
    totG = len(G) * len(G)

    # 누적합 방식으로 빠르게 계산하려면 정렬된 키 활용
    sF = sorted(dF.items())  # [(합, count), ...]
    sG = sorted(dG.items())

    # G의 누적 분포(합 미만)의 누적 카운트 준비
    g_keys = [k for k,_ in sG]
    g_cnts = np.array([c for _,c in sG], dtype=np.int64)
    g_cumsum = np.cumsum(g_cnts)                  # ≤ key 누적
    # 합 < x 인 누적을 얻으려면 'x보다 작은 인덱스'를 찾기
    import bisect

    gt = 0  # F합 > G합
    eq = 0  # 동일
    for s, cF in sF:
        # G합이 s보다 작은 모든 경우의 수
        idx = bisect.bisect_left(g_keys, s)  # s 미만
        g_less = g_cumsum[idx-1] if idx > 0 else 0
        gt += cF * g_less
        # G합이 s와 같은 경우의 수
        if idx < len(g_keys) and g_keys[idx] == s:
            eq += cF * dG[s]

    total = totF * totG
    lt = total - gt - eq
    return gt/total, lt/total, eq/total

def simulate_vs(F: list[int], G: list[int], trials: int, mode: str = "single", seed: int | None = None) -> tuple[float,float,float]:
    """
    시뮬레이션으로 승/패/무 확률 추정.
    mode: "single" 한 번 던지기, "double" 두 번 던져 합 비교
    """
    rng = np.random.default_rng(seed)
    m, n = len(F), len(G)

    # 인덱스 뽑아서 면값 매핑 → 중복면도 균등확률
    if mode == "single":
        idxF = rng.integers(0, m, size=trials)
        idxG = rng.integers(0, n, size=trials)
        rollF = np.array(F, dtype=int)[idxF]
        rollG = np.array(G, dtype=int)[idxG]
    else:
        idxF1 = rng.integers(0, m, size=trials)
        idxF2 = rng.integers(0, m, size=trials)
        idxG1 = rng.integers(0, n, size=trials)
        idxG2 = rng.integers(0, n, size=trials)
        rollF = np.array(F, dtype=int)[idxF1] + np.array(F, dtype=int)[idxF2]
        rollG = np.array(G, dtype=int)[idxG1] + np.array(G, dtype=int)[idxG2]

    gt = (rollF > rollG).sum()
    lt = (rollF < rollG).sum()
    eq = trials - gt - lt
    return gt/trials, lt/trials, eq/trials

def pairwise_table(names: list[str], probs: dict[tuple[str,str], tuple[float,float,float]]) -> pd.DataFrame:
    """
    A,B,C 쌍들의 P(win)만을 매트릭스로 정리 (행이 열을 이길 확률).
    probs[(X,Y)] = (P(X>Y), P(X<Y), P(=))
    """
    mat = []
    for r in names:
        row = []
        for c in names:
            if r == c:
                row.append(np.nan)
            else:
                pwin = probs[(r,c)][0]
                row.append(pwin)
        mat.append(row)
    df = pd.DataFrame(mat, index=names, columns=names)
    return df

def nontransitive_arrow(df_win: pd.DataFrame, names=("A","B","C")) -> str | None:
    """
    비반사적 순환(A>B, B>C, C>A) 탐지. 해당하면 "A → B → C → A" 반환.
    """
    a,b,c = names
    try:
        if df_win.loc[a,b] > 0.5 and df_win.loc[b,c] > 0.5 and df_win.loc[c,a] > 0.5:
            return f"{a} → {b} → {c} → {a}"
    except Exception:
        pass
    return None

# -----------------------------
# UI
# -----------------------------
def render():
    st.header("🎲 비정규(커스텀) 주사위 A/B/C 대결 실험")

    st.markdown(
        """
        **설정 방법**  
        - 각 주사위의 면값을 콤마로 입력하세요. (예: `3,3,3,3,3,6`)  
        - 중복 입력을 인정합니다(면 갯수와 비율 자체가 주사위를 정의).  
        - 아래에서 **모드**를 선택해 *정확 계산*과 *시뮬레이션* 결과를 함께 봅니다.
        """
    )

    with st.expander("예시 불러오기(클릭)", expanded=True):
        col = st.columns(3)
        with col[0]:
            facesA = st.text_input("A의 면값", "3,3,3,3,3,6")
        with col[1]:
            facesB = st.text_input("B의 면값", "2,2,2,5,5,5")
        with col[2]:
            facesC = st.text_input("C의 면값", "1,4,4,4,4,4")

    # 파싱 & 검증
    try:
        A = parse_faces(facesA)
        B = parse_faces(facesB)
        C = parse_faces(facesC)
    except Exception as e:
        st.error(f"면값 입력 오류: {e}")
        return

    names = ["A","B","C"]
    dice  = {"A": A, "B": B, "C": C}

    # 요약 보여주기
    c1, c2, c3 = st.columns(3)
    for (nm, F), c in zip(dice.items(), (c1,c2,c3)):
        with c:
            s = pd.Series(F)
            c.metric(f"{nm} 면 개수", len(F))
            st.caption(f"{nm} 고유값/도수")
            st.dataframe(s.value_counts().sort_index(), use_container_width=True, height=160)

    st.divider()

    mode = st.radio("비교 모드", ["한 번 던져 큰 수 승", "한 주사위를 두 번 던져 **합** 비교"], horizontal=True)
    mode_key = "single" if mode.startswith("한 번") else "double"

    sim_trials = st.slider("시뮬레이션 시행 수", 100, 200_000, 20_000, step=100)
    seed = st.number_input("난수 시드(재현용, 비워두면 무작위)", value=0, min_value=0, step=1, format="%d")

    # -----------------------------
    # 정확 계산
    # -----------------------------
    st.subheader("📐 정확 계산 (이론값)")
    exact = {}
    for x in names:
        for y in names:
            if x == y:
                continue
            if mode_key == "single":
                exact[(x,y)] = prob_single_gt(dice[x], dice[y])
            else:
                exact[(x,y)] = prob_double_sum_gt(dice[x], dice[y])

    df_exact = pairwise_table(names, exact)
    st.write("**행이 열을 이길 확률** (P(row > col))")
    st.dataframe((df_exact*100).round(2).astype("float"), use_container_width=True)

    note = nontransitive_arrow(df_exact, names)
    if note:
        st.success(f"🔄 비추이성 발견! **{note}** (모드: {mode})")

    # -----------------------------
    # 시뮬레이션
    # -----------------------------
    st.subheader("🧪 시뮬레이션")
    sim = {}
    for x in names:
        for y in names:
            if x == y:
                continue
            gt, lt, eq = simulate_vs(dice[x], dice[y], trials=sim_trials, mode=mode_key, seed=(None if seed==0 else seed+hash((x,y))%10_000))
            sim[(x,y)] = (gt, lt, eq)

    df_sim = pairwise_table(names, sim)
    cA, cB = st.columns(2)
    with cA:
        st.write("**행이 열을 이길 확률(시뮬레이션)**")
        st.dataframe((df_sim*100).round(2).astype("float"), use_container_width=True)
    with cB:
        # 정확 vs 시뮬 비교 차이
        diff = (df_sim - df_exact)
        st.write("**시뮬 − 이론** (오차)")
        st.dataframe((diff*100).round(2).astype("float"), use_container_width=True)

    st.caption("참고: 동점(tie)은 별도로 집계되며, 위 표는 **승률**만을 표시합니다. 자세한 승/패/무는 아래 표에서 확인하세요.")

    # 세부 결과(승/패/무)
    st.markdown("### 세부 표 (승/패/무)")
    det_rows = []
    for x in names:
        for y in names:
            if x == y: 
                continue
            ex = exact[(x,y)]
            si = sim[(x,y)]
            det_rows.append({
                "대결": f"{x} vs {y}",
                "정확값 P(win/lose/tie)": f"{ex[0]:.3f} / {ex[1]:.3f} / {ex[2]:.3f}",
                "시뮬값 P(win/lose/tie)": f"{si[0]:.3f} / {si[1]:.3f} / {si[2]:.3f}",
            })
    st.dataframe(pd.DataFrame(det_rows), use_container_width=True, hide_index=True)

    st.divider()
    st.info(
        "💡 팁\n"
        "- ‘면값’을 바꾸면 곧바로 이론값이 갱신됩니다.\n"
        "- 시뮬레이션 시행 수를 크게 하면 이론값에 수렴하는 것을 볼 수 있어요.\n"
        "- 두 번 합 모드에서는 각 주사위의 ‘합 분포’가 달라져 승패가 역전될 수 있습니다."
    )
