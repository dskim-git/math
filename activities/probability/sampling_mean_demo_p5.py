# activities/probability/sampling_mean_demo_p5.py
import json
import re
import urllib.parse as _url
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "모평균 vs 표본평균 (p5.js 시각화)",
    "description": "구글시트의 '원본' 데이터를 모집단으로 사용해 표본을 뽑고, 표본평균 분포를 시각화합니다.",
    "order": 25,
}

# ─────────────────────────────────────────────────────────────────────────────
# 유틸

def sheet_url_to_csv(url: str, sheet_name: str = "원본") -> str:
    """
    - 공유 링크/편집 링크 등 어떤 형태든 문서 ID만 추출해서
      gviz CSV 주소로 바꿉니다(시트 이름으로 접근).
    - 시트가 링크 공개(링크가 있는 모든 사용자 보기)이어야 합니다.
    예: https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&sheet=<인코딩된시트명>
    """
    m = re.search(r"/d/([a-zA-Z0-9\-_]+)", url)
    if not m:
        return url  # 이미 CSV일 수도 있으니 그대로
    doc_id = m.group(1)
    return f"https://docs.google.com/spreadsheets/d/{doc_id}/gviz/tq?tqx=out:csv&sheet={_url.quote(sheet_name)}"


@st.cache_data(ttl=60)
def load_population(csv_url: str) -> pd.DataFrame:
    df = pd.read_csv(csv_url)
    # 완전빈 컬럼 제거 & 칼럼 공백 정리
    df = df.dropna(axis=1, how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return df


def pick_numeric_column(df: pd.DataFrame) -> str:
    """'키' 같은 한국어/영어 후보 우선, 없으면 수치형 첫 컬럼."""
    prefs = ["키", "height", "Height", "키(cm)", "신장"]
    for name in prefs:
        if name in df.columns and pd.api.types.is_numeric_dtype(df[name]):
            return name
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            return c
    # 최후: 첫 컬럼
    return df.columns[0]


@dataclass
class SampleStats:
    mean: float
    std: float


def make_samples(values: np.ndarray, n: int, m: int, replace: bool, seed: int) -> Tuple[List[np.ndarray], List[SampleStats]]:
    rng = np.random.default_rng(seed)
    samples: List[np.ndarray] = []
    stats: List[SampleStats] = []
    N = len(values)
    n = max(1, min(n, N))
    for _ in range(m):
        idx = rng.choice(N, size=n, replace=replace)
        s = values[idx]
        samples.append(s)
        if len(s) >= 2:
            stats.append(SampleStats(mean=float(np.mean(s)), std=float(np.std(s, ddof=1))))
        else:
            stats.append(SampleStats(mean=float(np.mean(s)), std=float(np.nan)))
    return samples, stats


# ─────────────────────────────────────────────────────────────────────────────
# 페이지

def render():
    st.header("📏 모평균과 표본평균 (p5.js 시각화)")
    st.caption("제시한 구글시트의 **‘원본’** 시트를 모집단으로 사용합니다. 표본을 여러 개 만들고, 표본평균의 분포를 시각적으로 확인해 보세요.")

    DEFAULT_SHEET = "https://docs.google.com/spreadsheets/d/1APFg3_bk6NdclVvpjwzCKGXBq86u9732/edit?usp=sharing"
    with st.sidebar:
        st.subheader("⚙️ 데이터 설정")
        gsheet_url = st.text_input("구글시트 문서 링크", value=DEFAULT_SHEET)
        sheet_name = st.text_input("시트 이름", value="원본", help="띄어쓰기/한글 OK (링크 공개 필요)")
        csv_url = sheet_url_to_csv(gsheet_url, sheet_name)
        st.caption("자동 변환된 CSV 주소:")
        st.code(csv_url, language="text")

        st.subheader("⚙️ 표본 설정")
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                sample_size = st.number_input("표본 크기 n", min_value=1, max_value=1000, value=30, step=1)
            with col2:
                num_samples = st.number_input("표본 개수 m", min_value=1, max_value=500, value=50, step=1)
        col3, col4 = st.columns(2)
        with col3:
            replace = st.toggle("복원추출(With replacement)", value=True)
        with col4:
            seed = st.number_input("난수 시드", value=0, step=1)
        regen = st.button("표본 재생성", use_container_width=True)

    # ── 모집단 데이터 불러오기
    try:
        df = load_population(csv_url)
    except Exception as e:
        st.error(f"시트를 불러오지 못했습니다: {e}")
        return

    if df.empty:
        st.warning("시트가 비어 있거나 접근 권한이 없습니다.")
        return

    # 어떤 수치 컬럼을 쓸지 선택
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    default_col = pick_numeric_column(df)
    st.subheader("1) 모집단 데이터 미리보기")
    col_sel = st.selectbox("※ 사용할 수치 컬럼 선택", options=num_cols, index=max(0, num_cols.index(default_col)))
    st.dataframe(df, use_container_width=True, hide_index=True)

    values = df[col_sel].dropna().to_numpy(dtype=float)
    N = len(values)
    pop_mu = float(values.mean())
    pop_sigma = float(values.std(ddof=1))

    st.markdown(f"- 모집단 크기 **N={N}**, 평균 **μ={pop_mu:.3f}**, 표준편차 **σ={pop_sigma:.3f}**  \n"
                f"- 사용 컬럼: **{col_sel}**")

    # ── 표본 생성 (버튼 누를 때만 갱신)
    key_samples = "smd_samples"
    key_sstats  = "smd_sample_stats"
    key_last    = "smd_last_params"

    params = (tuple(values.tolist())[:3], N, sample_size, num_samples, replace, seed)  # 캐시키 유사
    if regen or key_samples not in st.session_state or st.session_state.get(key_last) != params:
        samples, sstats = make_samples(values, sample_size, num_samples, replace, seed)
        st.session_state[key_samples] = samples
        st.session_state[key_sstats] = sstats
        st.session_state[key_last] = params

    samples: List[np.ndarray] = st.session_state[key_samples]
    sstats : List[SampleStats] = st.session_state[key_sstats]

    # ── 4) 표본 표/통계
    st.subheader("2) 표본 표와 요약 통계")
    means = np.array([s.mean for s in sstats], dtype=float)
    stds  = np.array([s.std  for s in sstats], dtype=float)

    summary = pd.DataFrame({
        "표본번호": np.arange(1, len(samples)+1),
        "표본평균": means,
        "표본표준편차": stds
    })
    st.dataframe(summary.style.format({"표본평균":"{:.3f}", "표본표준편차":"{:.3f}"}),
                 use_container_width=True, hide_index=True)

    st.markdown("표본 상세 보기")
    sel_idx = st.selectbox("확대할 표본 선택", options=list(range(1, len(samples)+1)), index=0)
    cur_sample = samples[sel_idx-1]
    st.dataframe(pd.DataFrame({"표본값": cur_sample}),
                 use_container_width=True, hide_index=True)

    # ── 5) p5.js 시각화 ① 모집단 수직선 & 표본 하이라이트
    st.subheader("3) 모집단 수직선과 선택한 표본 하이라이트 (p5.js)")
    vmin, vmax = float(values.min()), float(values.max())
    vis_payload_1 = dict(
        values=values.tolist(),
        sample=cur_sample.tolist(),
        vmin=vmin, vmax=vmax,
        title=f"모집단({N}명) 수직선과 표본 #{sel_idx} (n={len(cur_sample)})"
    )
    components.html(f"""
    <div id="popline" style="width:100%;max-width:980px;margin:0 auto;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
    <script>
    const DATA1 = {json.dumps(vis_payload_1)};
    new p5((p)=>{
      let W=980,H=260, pad=40;
      p.setup=()=>{{ p.createCanvas(W,H).parent("popline"); p.noLoop(); }};
      function yMap(v) {{
        const ymin=DATA1.vmin, ymax=DATA1.vmax;
        return p.map(v, ymax, ymin, pad, H-pad);
      }}
      p.draw=()=>{{
        p.background(255);
        // 수직선
        p.stroke(50); p.strokeWeight(2);
        p.line(W*0.15, pad, W*0.15, H-pad);
        // 범위 라벨
        p.noStroke(); p.fill(0); p.textSize(13);
        p.textAlign(p.RIGHT,p.CENTER);
        p.text(DATA1.vmax.toFixed(2), W*0.145, pad);
        p.text(DATA1.vmin.toFixed(2), W*0.145, H-pad);
        p.textAlign(p.LEFT,p.TOP);
        p.text(DATA1.title, W*0.18, 12);

        // 표본값 집합(멀티셋) 카운트로 중복 처리
        const cnt = {{}};
        for (const x of DATA1.sample) cnt[x]= (cnt[x]||0)+1;

        // 모집단 점
        p.strokeWeight(0);
        for (const v of DATA1.values){{
          const y=yMap(v);
          const inSample = cnt[v]>0;
          if(inSample) {{ p.fill(230, 49, 70); cnt[v]-=1; }}
          else          {{ p.fill(160); }}
          p.circle(W*0.15, y, inSample?7:5);
        }}
      }};
    }});
    </script>
    """, height=280)

    # ── 6) p5.js 시각화 ② 정규분포(모집단 vs 표본평균) & 표본평균 위치
    st.subheader("4) 모집단 정규곡선 vs 표본평균 정규곡선 (p5.js)")
    samp_mu = float(np.mean(means))
    samp_sigma = float(np.std(means, ddof=1)) if len(means) >= 2 else float("nan")
    theo_sigma = pop_sigma / np.sqrt(sample_size) if sample_size > 0 else float("nan")

    vis_payload_2 = dict(
        mu_pop=pop_mu, sd_pop=pop_sigma,
        mu_bar=pop_mu, sd_bar=theo_sigma,  # 이론적 표본평균 분포
        sample_means=means.tolist(),
        highlight=float(np.mean(cur_sample)),
        title="정규곡선: 모집단 N(μ,σ) vs 표본평균 N(μ,σ/√n) & 표본평균 점"
    )

    components.html(f"""
    <div id="gauss" style="width:100%;max-width:980px;margin:0 auto;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
    <script>
    const D2 = {json.dumps(vis_payload_2)};
    new p5((p)=>{
      let W=980,H=320, pad=50, left=60, right=30, top=30, bottom=60;
      p.setup=()=>{{ p.createCanvas(W,H).parent("gauss"); p.noLoop(); p.textFont('sans-serif'); }};
      function pdf(x,mu,sd){{ return (1/(sd*Math.sqrt(2*Math.PI)))*Math.exp(-0.5*Math.pow((x-mu)/sd,2)); }}
      p.draw=()=>{{
        p.background(255);
        const mu = D2.mu_pop, sd = D2.sd_pop;
        const muB= D2.mu_bar, sdB= D2.sd_bar || 1e-6;

        // x범위 설정
        const xmin = Math.min(mu-4*sd, muB-6*sdB);
        const xmax = Math.max(mu+4*sd, muB+6*sdB);
        // y최대(두 곡선 중 최대값)
        let ymax=0;
        for(let i=0;i<600;i++){{ 
          const x = xmin + (xmax-xmin)*i/599;
          ymax = Math.max(ymax, pdf(x,mu,sd), pdf(x,muB,sdB));
        }}

        // 축
        const X = x=> p.map(x, xmin, xmax, left, W-right);
        const Y = y=> p.map(y, 0,   ymax, H-bottom, top);
        p.stroke(0); p.strokeWeight(1);
        p.line(left, H-bottom, W-right, H-bottom); // x-axis
        // 눈금
        p.fill(0); p.noStroke(); p.textSize(12); p.textAlign(p.CENTER, p.TOP);
        for(let t=-4; t<=4; t++){{
          const x = mu + t*sd;
          if(x<xmin || x>xmax) continue;
          const sx=X(x);
          p.stroke(200); p.line(sx, H-bottom, sx, top+5);
          p.noStroke(); p.text(x.toFixed(1), sx, H-bottom+6);
        }}
        p.textAlign(p.LEFT,p.TOP);
        p.text(D2.title, left, 6);

        // 모집단 곡선(파랑)
        p.noFill(); p.stroke(35,102,235); p.strokeWeight(2);
        p.beginShape();
        for(let i=0;i<600;i++){{
          const x = xmin + (xmax-xmin)*i/599;
          p.vertex(X(x), Y(pdf(x,mu,sd)));
        }}
        p.endShape();

        // 표본평균 곡선(주황)
        p.noFill(); p.stroke(245,128,37); p.strokeWeight(2);
        p.beginShape();
        for(let i=0;i<600;i++){{
          const x = xmin + (xmax-xmin)*i/599;
          p.vertex(X(x), Y(pdf(x,muB,sdB)));
        }}
        p.endShape();

        // 표본평균 점들
        p.noStroke();
        for(const m of D2.sample_means){{
          const sx=X(m);
          p.fill(0,0,0,70);
          p.circle(sx, H-bottom-12, 5);
        }}
        // 현재 선택 표본의 평균 하이라이트
        p.fill(230,49,70); p.circle(X(D2.highlight), H-bottom-12, 8);
        p.textAlign(p.CENTER,p.BOTTOM);
        p.text('현재 표본 평균 '+D2.highlight.toFixed(2), X(D2.highlight), H-bottom-18);
        // 범례
        p.textAlign(p.LEFT,p.BOTTOM);
        p.fill(35,102,235); p.rect(left, H-28, 18, 3); p.fill(0); p.text('모집단 N(μ,σ)', left+26, H-34);
        p.fill(245,128,37); p.rect(left+140, H-28, 18, 3); p.fill(0); p.text('표본평균 N(μ,σ/√n)', left+168, H-34);
      }};
    }});
    </script>
    """, height=340)

    # ── 7) 이론 vs 경험 비교
    st.subheader("5) 이론 vs 표본평균(경험) 비교")
    comp = pd.DataFrame({
        "구분": ["모집단", "표본평균(이론)", "표본평균(경험)"],
        "평균": [pop_mu, pop_mu, float(np.mean(means))],
        "분산": [pop_sigma**2, (pop_sigma**2)/(sample_size if sample_size>0 else np.nan), float(np.var(means, ddof=1)) if len(means)>=2 else np.nan],
        "표준편차": [pop_sigma, theo_sigma, float(np.std(means, ddof=1)) if len(means)>=2 else np.nan]
    })
    st.dataframe(comp.style.format({"평균":"{:.3f}","분산":"{:.3f}","표준편차":"{:.3f}"}), use_container_width=True, hide_index=True)

    st.info("※ ‘표본평균(이론)’의 표준편차는 **σ/√n**, 평균은 항상 **μ** 입니다. 표본을 많이 뽑을수록(큰 m) ‘표본평균(경험)’ 값들이 이론에 가까워집니다.")

# 스트림릿에서 호출
if __name__ == "__main__":
    render()
