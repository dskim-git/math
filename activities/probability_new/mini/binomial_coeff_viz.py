import json
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "이항정리계수시각화"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이 활동으로 해결할 수 있는 문제 3개 (문제와 답 모두 작성)**"},
    {"key": "문제1", "label": "문제 1", "type": "text_area", "height": 80},
    {"key": "답1",   "label": "문제 1의 답", "type": "text_input"},
    {"key": "문제2", "label": "문제 2", "type": "text_area", "height": 80},
    {"key": "답2",   "label": "문제 2의 답", "type": "text_input"},
    {"key": "문제3", "label": "문제 3", "type": "text_area", "height": 80},
    {"key": "답3",   "label": "문제 3의 답", "type": "text_input"},
    {"key": "새롭게알게된점", "label": "💡 이 활동을 통해 새롭게 알게 된 점", "type": "text_area", "height": 100},
    {"key": "느낀점",        "label": "💬 이 활동을 통해 느낀 점",           "type": "text_area", "height": 100},
]

META = {
    "title":       "미니: 이항정리 계수의 탄생",
    "description": "각 인수에서 a 또는 b를 선택하는 과정으로 이항계수가 만들어지는 원리를 시각적으로 탐구합니다.",
    "order":       10,
}


def render():
    user_id   = st.session_state.get("_user_id", "")
    user_name = st.session_state.get("_user_name", "")
    short_id  = (user_id[4:] if len(user_id) >= 9 and user_id[:2] == "20" else user_id)

    st.header("🔢 이항정리 계수의 탄생")
    st.markdown(
        "$(a+b)^n$ 전개 시 **특정 항의 계수는 왜 그 값일까요?** "
        "각 일차식 $(a+b)$에서 $a$ 또는 $b$ 중 하나를 **선택**하는 방법의 수가 바로 계수입니다. "
        "네 개의 탭을 탐구하며 이항정리의 본질을 파악해보세요!"
    )
    components.html(_build_html(short_id, user_name, _GAS_URL), height=1000, scrolling=True)
    st.markdown("---")
    _render_ranking()
    st.markdown("---")
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner=False)
def _load_ranking_data(sheet_id: str) -> tuple:
    """이항정리 도전 모드 랭킹 데이터를 구글 시트에서 읽어옵니다.
    Returns: (records: list, error: str | None)
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        creds = Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"]),
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        client = gspread.authorize(creds)
        ws = client.open_by_key(sheet_id).worksheet("이항정리랭킹")
        return ws.get_all_records(), None
    except Exception as e:
        return [], str(e)


def _render_ranking() -> None:
    """도전 모드 학번별 최고점 랭킹을 Streamlit으로 표시합니다."""
    st.subheader("🏆 도전 모드 랭킹")
    col_h, col_btn = st.columns([5, 1])
    with col_btn:
        if st.button("🔄 새로고침", key="rank_refresh_btn"):
            st.cache_data.clear()
            st.rerun()

    try:
        sheet_id = st.secrets["reflection_spreadsheet_probability_new"]
    except Exception:
        sheet_id = ""

    records, err = _load_ranking_data(sheet_id)

    if err:
        st.error(f"랭킹을 불러오지 못했습니다.\n\n```\n{err}\n```")
        return

    if not records:
        st.info("아직 도전 기록이 없습니다. 첫 번째 도전자가 되어보세요! 🎯")
        return

    # 학번별 최고점 집계
    best: dict = {}
    for r in records:
        sid  = str(r.get("학번", "")).strip()
        name = str(r.get("이름", "")).strip()
        try:
            score = int(r.get("점수", 0) or 0)
        except (ValueError, TypeError):
            score = 0
        diff_lbl = str(r.get("난이도", "")).strip()
        if sid and (sid not in best or score > best[sid]["최고점"]):
            best[sid] = {"학번": sid, "이름": name, "최고점": score, "난이도": diff_lbl}

    ranked = sorted(best.values(), key=lambda x: -x["최고점"])

    # 현재 사용자 학번 (강조 표시용)
    cur_id   = st.session_state.get("_user_id", "")
    short_me = cur_id[4:] if len(cur_id) >= 9 and cur_id[:2] == "20" else cur_id

    medals = ["🥇", "🥈", "🥉"]
    rows_html = ""
    for i, row in enumerate(ranked[:20]):
        medal  = medals[i] if i < 3 else f"{i + 1}위"
        is_me  = row["학번"] == short_me
        tr_sty = ' style="background:rgba(139,92,246,.18);font-weight:700;"' if is_me else ""
        me_tag = " &nbsp;<span style='color:#a78bfa;font-size:11px'>← 나</span>" if is_me else ""
        rows_html += (
            f"<tr{tr_sty}>"
            f"<td style='text-align:center;font-size:18px;padding:8px 10px'>{medal}</td>"
            f"<td style='padding:8px 10px'>{row['이름']}{me_tag}</td>"
            f"<td style='text-align:right;padding:8px 10px;color:#fbbf24;font-weight:800'>{row['최고점']:,}점</td>"
            f"<td style='text-align:center;padding:8px 10px;color:#94a3b8;font-size:12px'>{row['난이도']}</td>"
            f"</tr>"
        )

    table_html = (
        "<style>"
        ".rank-tbl{width:100%;border-collapse:collapse;font-size:14px}"
        ".rank-tbl th{padding:7px 10px;background:rgba(255,255,255,.04);"
        "color:#475569;font-size:11px;letter-spacing:.05em;text-transform:uppercase;"
        "border-bottom:1px solid rgba(255,255,255,.07)}"
        ".rank-tbl td{border-bottom:1px solid rgba(255,255,255,.04);color:#e2e8f0}"
        ".rank-tbl tr:hover td{background:rgba(255,255,255,.03)}"
        "</style>"
        "<table class='rank-tbl'>"
        "<thead><tr>"
        "<th style='width:52px'>순위</th><th>이름</th>"
        "<th style='text-align:right'>최고점</th><th style='text-align:center'>최고 난이도</th>"
        "</tr></thead>"
        f"<tbody>{rows_html}</tbody></table>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
def _build_html(short_id: str, user_name: str, gas_url_str: str) -> str:
    init = (
        '<script>const _U={id:' + json.dumps(short_id)
        + ',name:' + json.dumps(user_name)
        + ',gasUrl:' + json.dumps(gas_url_str) + '};</script>'
    )
    raw = r"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',system-ui,sans-serif;
  background:linear-gradient(135deg,#08101f 0%,#0d1a2e 60%,#08101f 100%);
  min-height:100vh;padding:14px 12px;color:#e2e8f0}

/* ── Tabs ────────────────────────────────── */
.tab-bar{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}
.tab-btn{padding:9px 18px;border-radius:14px;border:1.5px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.04);cursor:pointer;font-size:13px;font-weight:700;
  color:#64748b;transition:all .2s;letter-spacing:.02em}
.tab-btn.active{background:rgba(139,92,246,.22);color:#c4b5fd;
  border-color:rgba(139,92,246,.5);box-shadow:0 0 14px rgba(139,92,246,.2)}
.tab-btn:hover:not(.active){background:rgba(255,255,255,.07);color:#e2e8f0}
.pane{display:none}.pane.show{display:block}

/* ── Card ───────────────────────────────── */
.card{background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08);
  border-radius:18px;padding:18px 20px;margin-bottom:14px}
.card-title{font-size:13px;font-weight:700;color:#a78bfa;margin-bottom:14px;
  letter-spacing:.02em;display:flex;align-items:center;gap:7px}

/* ── Controls ───────────────────────────── */
.ctrl-row{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin-bottom:10px}
.ctrl-group{display:flex;flex-direction:column;gap:6px}
.ctrl-label{font-size:11px;color:#64748b;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
input[type=range]{-webkit-appearance:none;width:180px;height:6px;
  border-radius:3px;background:rgba(255,255,255,.12);outline:none}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;
  border-radius:50%;background:#8b5cf6;cursor:pointer;
  box-shadow:0 0 10px rgba(139,92,246,.7);border:2px solid #fff}
.badge{display:inline-flex;align-items:center;justify-content:center;min-width:34px;
  background:linear-gradient(135deg,#8b5cf6,#6366f1);border-radius:10px;padding:2px 10px;
  font-weight:900;font-size:18px;color:#fff;box-shadow:0 2px 12px rgba(139,92,246,.4)}
.badge-g{background:linear-gradient(135deg,#059669,#0d9488)}

/* ── Tab-1 Selection visual ─────────────── */
.sel-scroll{max-height:360px;overflow-y:auto;padding:4px 2px}
.sel-row{display:flex;align-items:center;gap:3px;padding:4px 8px;border-radius:10px;
  margin-bottom:4px;background:rgba(255,255,255,.014);
  border:1px solid rgba(255,255,255,.04);transition:background .2s;
  animation:pop .25s ease both}
.sel-row:hover{background:rgba(139,92,246,.08);border-color:rgba(139,92,246,.2)}
@keyframes pop{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
.row-idx{color:#334155;font-size:11px;min-width:22px;text-align:right;flex-shrink:0}
.factor{display:flex;align-items:center;font-size:15px;flex-shrink:0}
.paren{color:#475569;font-size:16px}
.la,.lb{display:inline-flex;align-items:center;justify-content:center;
  width:22px;height:22px;border-radius:50%;font-weight:800;font-size:13px;
  transition:all .3s;color:#64748b}
.sel-a{background:#7c3aed;color:#fff;box-shadow:0 0 10px rgba(124,58,237,.8)}
.sel-b{background:#047857;color:#fff;box-shadow:0 0 10px rgba(4,120,87,.8)}
.plus-sign{color:#2d3748;font-size:12px;margin:0 1px}
.row-arrow{color:#22d3ee;font-size:13px;margin:0 6px;flex-shrink:0}
.row-seq{font-family:monospace;font-size:15px;font-weight:800;color:#fbbf24;
  min-width:48px;flex-shrink:0}
.row-eq{color:#475569;font-size:12px;margin:0 3px;flex-shrink:0}
.row-mono{font-size:13px;font-style:italic;color:#a78bfa;flex-shrink:0}
.summary-box{background:linear-gradient(135deg,rgba(139,92,246,.12),rgba(99,102,241,.08));
  border:1px solid rgba(139,92,246,.35);border-radius:14px;padding:16px 20px;
  text-align:center;margin-top:10px}
.sum-formula{font-size:22px;font-weight:900;color:#c4b5fd;letter-spacing:.02em}
.sum-sub{font-size:13px;color:#64748b;margin-top:6px}
.sum-coeff{font-size:28px;font-weight:900;color:#4ade80}

/* ── Tab-2 Expansion ───────────────────── */
.exp-heading{font-size:16px;color:#94a3b8;margin-bottom:12px;line-height:1.6}
.terms-wrap{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:14px}
.term-chip{background:rgba(255,255,255,.04);border:1.5px solid rgba(255,255,255,.1);
  border-radius:12px;padding:8px 16px;font-size:15px;font-weight:700;cursor:pointer;
  transition:all .2s;color:#e2e8f0;white-space:nowrap}
.term-chip.sel{background:rgba(16,185,129,.18);border-color:rgba(16,185,129,.5);
  color:#6ee7b7;box-shadow:0 0 15px rgba(16,185,129,.2);transform:translateY(-2px)}
.term-chip:hover:not(.sel){background:rgba(255,255,255,.07)}
.op-sign{color:#475569;font-size:18px;font-weight:700;align-self:center}
.breakdown{background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.2);
  border-radius:14px;padding:16px;animation:pop .25s ease}
.bd-title{font-size:13px;font-weight:700;color:#6ee7b7;margin-bottom:12px}
.bd-grid{display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:center}
.bd-box{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
  border-radius:12px;padding:10px 16px;text-align:center;min-width:80px}
.bd-expr{font-size:14px;color:#94a3b8;margin-bottom:4px}
.bd-v{font-size:22px;font-weight:900;color:#fbbf24}
.bd-l{font-size:11px;color:#475569;margin-top:4px;font-weight:600}
.bd-op{font-size:20px;color:#475569;font-weight:700}
.bd-res{background:rgba(74,222,128,.08);border:1.5px solid rgba(74,222,128,.35);
  border-radius:12px;padding:10px 16px;text-align:center;min-width:80px}
.bd-rv{font-size:26px;font-weight:900;color:#4ade80}

/* ── Tab-2 Pascal ──────────────────────── */
.pascal-outer{overflow-x:auto;padding:4px 0}
.p-row{display:flex;justify-content:center;gap:4px;margin:3px 0;align-items:center}
.p-lbl{font-size:10px;color:#334155;min-width:28px;text-align:right;margin-right:3px}
.p-cell{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);
  border-radius:8px;min-width:32px;height:26px;display:flex;align-items:center;
  justify-content:center;font-size:12px;font-weight:600;color:#64748b;
  transition:all .2s;cursor:default}
.p-cell.hi{background:rgba(139,92,246,.3);border-color:rgba(139,92,246,.6);
  color:#c4b5fd;box-shadow:0 0 12px rgba(139,92,246,.3);transform:scale(1.12)}

/* ── Tab-3 Quiz ────────────────────────── */
.quiz-wrap{max-width:600px;margin:0 auto}
.quiz-problem{background:linear-gradient(135deg,rgba(245,158,11,.1),rgba(249,115,22,.07));
  border:1.5px solid rgba(245,158,11,.3);border-radius:18px;padding:22px;
  text-align:center;margin-bottom:14px}
.quiz-exp{font-size:28px;font-weight:900;color:#fbbf24;margin-bottom:8px}
.quiz-ask{font-size:13px;color:#94a3b8;margin-bottom:8px}
.quiz-target{font-size:22px;font-weight:800;color:#f97316}
.input-row{display:flex;gap:10px;justify-content:center;align-items:center;margin:14px 0}
.num-inp{background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.15);
  border-radius:12px;color:#e2e8f0;font-size:22px;font-weight:800;
  padding:8px 16px;width:130px;text-align:center;outline:none;transition:all .2s}
.num-inp:focus{border-color:#8b5cf6;box-shadow:0 0 12px rgba(139,92,246,.35)}
.btn{padding:10px 24px;border-radius:12px;border:none;font-size:14px;font-weight:800;
  cursor:pointer;transition:all .2s;letter-spacing:.02em}
.btn-p{background:linear-gradient(135deg,#8b5cf6,#6366f1);color:#fff;
  box-shadow:0 4px 16px rgba(139,92,246,.4)}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(139,92,246,.5)}
.btn-s{background:rgba(255,255,255,.07);color:#94a3b8;
  border:1px solid rgba(255,255,255,.12)}
.btn-s:hover{background:rgba(255,255,255,.11);color:#e2e8f0}
.feedback{border-radius:14px;padding:14px 20px;text-align:center;font-size:15px;
  font-weight:700;animation:pop .3s ease;display:none}
.fb-ok{background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.4);color:#6ee7b7}
.fb-ng{background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.4);color:#fca5a5}
.score-row{display:flex;gap:10px;justify-content:center;margin-bottom:14px;flex-wrap:wrap}
.score-box{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
  border-radius:14px;padding:10px 22px;text-align:center;min-width:88px}
.sc-n{font-size:26px;font-weight:900}
.sc-l{font-size:11px;color:#475569;font-weight:600;margin-top:3px;letter-spacing:.04em}
.hint-box{background:rgba(99,102,241,.07);border:1px solid rgba(99,102,241,.2);
  border-radius:14px;padding:14px;margin-top:10px;animation:pop .3s ease;display:none}
.hint-title{font-size:13px;font-weight:700;color:#818cf8;margin-bottom:8px}
.hint-body{font-size:14px;color:#94a3b8;line-height:2}

/* ── Tab-4 Challenge ───────────────────── */
.challenge-wrap{max-width:600px;margin:0 auto}
.timer-ring{position:relative;display:inline-block;margin-bottom:12px}
.timer-svg{transform:rotate(-90deg)}
.timer-text{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-size:32px;font-weight:900;color:#fbbf24;text-shadow:0 0 20px rgba(251,191,36,.5)}
.chal-score-row{display:flex;gap:10px;justify-content:center;margin-bottom:14px;flex-wrap:wrap}
.chal-score-box{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
  border-radius:14px;padding:10px 20px;text-align:center;min-width:88px}
.chal-sn{font-size:26px;font-weight:900}
.chal-sl{font-size:11px;color:#475569;font-weight:600;margin-top:3px}
.combo-ring{display:none;background:linear-gradient(135deg,rgba(251,191,36,.2),rgba(249,115,22,.15));
  border:2px solid rgba(251,191,36,.4);border-radius:14px;padding:8px 20px;
  text-align:center;margin:0 auto 14px;max-width:200px}
.combo-lbl{font-size:11px;color:#fbbf24;font-weight:700;letter-spacing:.08em}
.combo-val{font-size:28px;font-weight:900;color:#fbbf24;
  text-shadow:0 0 15px rgba(251,191,36,.6)}
.chal-problem{background:linear-gradient(135deg,rgba(99,102,241,.1),rgba(139,92,246,.08));
  border:1.5px solid rgba(99,102,241,.3);border-radius:18px;padding:20px;
  text-align:center;margin-bottom:12px}
.chal-exp{font-size:26px;font-weight:900;color:#c4b5fd;margin-bottom:6px}
.chal-ask{font-size:13px;color:#64748b;margin-bottom:6px}
.chal-target{font-size:20px;font-weight:800;color:#a78bfa}
.diff-badge{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;
  border-radius:8px;font-size:11px;font-weight:700;margin-bottom:8px}
.diff-easy{background:rgba(16,185,129,.2);color:#6ee7b7;border:1px solid rgba(16,185,129,.3)}
.diff-mid{background:rgba(245,158,11,.2);color:#fbbf24;border:1px solid rgba(245,158,11,.3)}
.diff-hard{background:rgba(239,68,68,.2);color:#fca5a5;border:1px solid rgba(239,68,68,.3)}
.gameover{background:linear-gradient(135deg,rgba(139,92,246,.15),rgba(99,102,241,.1));
  border:2px solid rgba(139,92,246,.4);border-radius:20px;padding:24px;text-align:center}
.go-title{font-size:26px;font-weight:900;color:#c4b5fd;margin-bottom:6px}
.go-score{font-size:48px;font-weight:900;color:#fbbf24;margin:10px 0;
  text-shadow:0 0 20px rgba(251,191,36,.5)}
.go-msg{font-size:14px;color:#64748b;margin-bottom:14px}
.go-best{font-size:14px;color:#a78bfa;font-weight:700}

/* ── pq buttons ────────────────────────── */
.pq-row{display:flex;align-items:center;gap:8px}
.pq-btn{width:28px;height:28px;border-radius:8px;border:1.5px solid rgba(255,255,255,.12);
  background:rgba(255,255,255,.05);cursor:pointer;font-size:18px;font-weight:800;
  color:#94a3b8;display:flex;align-items:center;justify-content:center;
  transition:all .2s;line-height:1;user-select:none}
.pq-btn:hover{background:rgba(255,255,255,.12);color:#e2e8f0}

/* ── Difficulty selector ────────────────  */
.diff-row{display:flex;gap:8px;margin-bottom:14px;justify-content:center}
.diff-btn{padding:8px 22px;border-radius:12px;border:1.5px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.04);cursor:pointer;font-size:13px;font-weight:700;
  color:#64748b;transition:all .2s}
.diff-btn.active-easy{background:rgba(16,185,129,.2);color:#6ee7b7;
  border-color:rgba(16,185,129,.4)}
.diff-btn.active-mid{background:rgba(245,158,11,.2);color:#fbbf24;
  border-color:rgba(245,158,11,.4)}
.diff-btn.active-hard{background:rgba(239,68,68,.2);color:#fca5a5;
  border-color:rgba(239,68,68,.4)}

/* ── Scrollbar ──────────────────────────── */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(139,92,246,.4);border-radius:3px}
</style>
</head>
<body>

<div class="tab-bar">
  <button class="tab-btn active" onclick="switchTab('viz',this)">🔍 선택 시각화</button>
  <button class="tab-btn" onclick="switchTab('gen',this)">📐 일반 이항식</button>
  <button class="tab-btn" onclick="switchTab('quiz',this)">🎯 계수 퀴즈</button>
  <button class="tab-btn" onclick="switchTab('chal',this)">🏆 도전 모드</button>
</div>

<!-- ═══════════════════════════════════════
     TAB 1 – 선택 시각화
     ═══════════════════════════════════════ -->
<div id="pane-viz" class="pane show">

  <div class="card">
    <div class="card-title">⚙️ 탐구 설정</div>
    <div class="ctrl-row">
      <div class="ctrl-group">
        <div class="ctrl-label">n (지수) = <span id="nBadge" class="badge">4</span></div>
        <input type="range" id="nSlider" min="1" max="8" value="4" oninput="onN()">
      </div>
      <div class="ctrl-group">
        <div class="ctrl-label">a의 지수 k = <span id="kBadge" class="badge">3</span></div>
        <input type="range" id="kSlider" min="0" max="4" value="3" oninput="onK()">
      </div>
    </div>
    <div style="font-size:11px;color:#334155;margin-top:4px">
      🟣 보라색 = a 선택 &nbsp;|&nbsp; 🟢 초록색 = b 선택
    </div>
  </div>

  <div class="card">
    <div class="card-title" id="vizTitle">🎯 목표 항이 만들어지는 모든 선택</div>
    <div class="sel-scroll" id="selGrid"></div>
    <div class="summary-box" id="vizSummary" style="display:none">
      <div class="sum-formula" id="sumFormula"></div>
      <div class="sum-sub"     id="sumSub"></div>
    </div>
  </div>

</div><!-- /pane-viz -->

<!-- ═══════════════════════════════════════
     TAB 2 – 일반 이항식
     ═══════════════════════════════════════ -->
<div id="pane-gen" class="pane">

  <div class="card">
    <div class="card-title">⚙️ 탐구 설정</div>
    <div class="ctrl-row">
      <div class="ctrl-group">
        <div class="ctrl-label">n (지수) = <span id="eNBadge" class="badge">4</span></div>
        <input type="range" id="eNSlider" min="1" max="7" value="4" oninput="onEN()">
      </div>
      <div class="ctrl-group">
        <div class="ctrl-label">a의 계수 p</div>
        <div class="pq-row">
          <button class="pq-btn" onclick="adjustPQ('p',-1)">−</button>
          <span id="pBadge" class="badge">1</span>
          <button class="pq-btn" onclick="adjustPQ('p',1)">+</button>
        </div>
      </div>
      <div class="ctrl-group">
        <div class="ctrl-label">b의 계수 q</div>
        <div class="pq-row">
          <button class="pq-btn" onclick="adjustPQ('q',-1)">−</button>
          <span id="qBadge" class="badge badge-g">1</span>
          <button class="pq-btn" onclick="adjustPQ('q',1)">+</button>
        </div>
      </div>
    </div>
    <div style="font-size:11px;color:#334155;margin-top:4px">p, q 범위: −5 ~ 5 (0 제외)</div>
  </div>

  <div class="card">
    <div class="card-title">📖 전개식 — 항을 클릭하면 계수 분해를 확인할 수 있어요!</div>
    <div class="exp-heading" id="expHeading"></div>
    <div class="terms-wrap"  id="termsWrap"></div>
    <div class="breakdown"   id="breakdown" style="display:none"></div>
  </div>

  <div class="card">
    <div class="card-title">🔺 파스칼의 삼각형 (현재 n 행 강조)</div>
    <div class="pascal-outer"><div id="pascalWrap"></div></div>
  </div>

</div><!-- /pane-gen -->

<!-- ═══════════════════════════════════════
     TAB 3 – 계수 퀴즈
     ═══════════════════════════════════════ -->
<div id="pane-quiz" class="pane">
  <div class="quiz-wrap">
    <div class="score-row">
      <div class="score-box"><div class="sc-n" id="scOk"  style="color:#4ade80">0</div><div class="sc-l">정답</div></div>
      <div class="score-box"><div class="sc-n" id="scNg"  style="color:#f87171">0</div><div class="sc-l">오답</div></div>
      <div class="score-box"><div class="sc-n" id="scRt"  style="color:#fbbf24">—</div><div class="sc-l">정답률</div></div>
      <div class="score-box"><div class="sc-n" id="scTr"  style="color:#a78bfa">0</div><div class="sc-l">도전</div></div>
    </div>
    <div class="quiz-problem">
      <div class="quiz-exp"    id="qExp"></div>
      <div class="quiz-ask">전개식에서 다음 항의 <strong>계수</strong>를 구하시오.</div>
      <div class="quiz-target" id="qTarget"></div>
    </div>
    <div class="input-row">
      <input type="number" class="num-inp" id="qInput" placeholder="계수 입력"
             onkeydown="if(event.key==='Enter')checkAns()">
      <button class="btn btn-p" onclick="checkAns()">확인 ✓</button>
      <button class="btn btn-s" onclick="newQ()">새 문제 🔄</button>
    </div>
    <div class="feedback"  id="qFeedback"></div>
    <div class="hint-box"  id="qHint">
      <div class="hint-title">💡 풀이 과정</div>
      <div class="hint-body" id="qHintBody"></div>
    </div>
  </div>
</div><!-- /pane-quiz -->

<!-- ═══════════════════════════════════════
     TAB 4 – 도전 모드
     ═══════════════════════════════════════ -->
<div id="pane-chal" class="pane">
  <div class="challenge-wrap">

    <!-- 난이도 선택 -->
    <div class="diff-row" id="diffRow">
      <button class="diff-btn active-easy" id="dEasy" onclick="setDiff('easy',this)">🌱 쉬움</button>
      <button class="diff-btn"             id="dMid"  onclick="setDiff('mid',this)">🔥 보통</button>
      <button class="diff-btn"             id="dHard" onclick="setDiff('hard',this)">⚡ 어려움</button>
    </div>

    <!-- Start screen -->
    <div id="chalStart" style="text-align:center">
      <div style="font-size:48px;margin-bottom:10px">⏱️</div>
      <div style="font-size:18px;font-weight:700;color:#c4b5fd;margin-bottom:8px">60초 동안 최대한 많이 맞춰보세요!</div>
      <div style="font-size:13px;color:#64748b;margin-bottom:18px;line-height:1.8">
        연속 정답 시 콤보 보너스 × 배율 획득<br>
        🌱 쉬움 = n≤3 &nbsp;|&nbsp; 🔥 보통 = n≤5 &nbsp;|&nbsp; ⚡ 어려움 = n≤7
      </div>
      <button class="btn btn-p" style="font-size:16px;padding:14px 40px" onclick="startChallenge()">🏁 시작!</button>
    </div>

    <!-- Game screen -->
    <div id="chalGame" style="display:none">
      <div style="display:flex;justify-content:center;margin-bottom:4px">
        <div class="timer-ring">
          <svg class="timer-svg" width="90" height="90" viewBox="0 0 90 90">
            <circle cx="45" cy="45" r="38" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="7"/>
            <circle id="timerArc" cx="45" cy="45" r="38" fill="none"
                    stroke="#fbbf24" stroke-width="7"
                    stroke-dasharray="238.76" stroke-dashoffset="0"
                    stroke-linecap="round" style="transition:stroke-dashoffset .9s linear"/>
          </svg>
          <div class="timer-text" id="timerText">60</div>
        </div>
      </div>

      <div class="chal-score-row">
        <div class="chal-score-box"><div class="chal-sn" id="cScore" style="color:#fbbf24">0</div><div class="chal-sl">점수</div></div>
        <div class="chal-score-box"><div class="chal-sn" id="cOk"    style="color:#4ade80">0</div><div class="chal-sl">정답</div></div>
        <div class="chal-score-box"><div class="chal-sn" id="cNg"    style="color:#f87171">0</div><div class="chal-sl">오답</div></div>
      </div>

      <div class="combo-ring" id="comboRing">
        <div class="combo-lbl">COMBO</div>
        <div class="combo-val" id="comboVal">× 1</div>
      </div>

      <div class="chal-problem">
        <div id="cDiffBadge" class="diff-badge diff-easy" style="margin:0 auto 8px">🌱 쉬움</div>
        <div class="chal-exp"    id="cExp"></div>
        <div class="chal-ask">다음 항의 <strong>계수</strong>를 구하시오.</div>
        <div class="chal-target" id="cTarget"></div>
      </div>

      <div class="input-row">
        <input type="number" class="num-inp" id="cInput" placeholder="계수 입력"
               onkeydown="if(event.key==='Enter')checkChal()">
        <button class="btn btn-p" onclick="checkChal()">확인 ✓</button>
      </div>

      <div class="feedback" id="cFeedback"></div>
    </div>

    <!-- Game over screen -->
    <div id="chalOver" style="display:none">
      <div class="gameover">
        <div class="go-title">⏰ 시간 종료!</div>
        <div class="go-score" id="goScore">0점</div>
        <div class="go-msg"   id="goMsg"></div>
        <div class="go-best"  id="goBest"></div>
        <div id="scoreSubmitStatus" style="font-size:12px;color:#64748b;margin-top:6px"></div>
        <button class="btn btn-p" style="margin-top:14px;font-size:15px;padding:12px 36px"
                onclick="restartChallenge()">다시 도전 🔄</button>
      </div>
    </div>

  </div>
</div><!-- /pane-chal -->


<script>
// ════════════════════════════════════════════════════
//  UTILITY
// ════════════════════════════════════════════════════
function C(n,k){
  if(k<0||k>n)return 0;
  if(k===0||k===n)return 1;
  k=Math.min(k,n-k);
  let r=1;
  for(let i=0;i<k;i++) r=r*(n-i)/(i+1);
  return Math.round(r);
}

/** All C(n,k) selections: 1=pick a, 0=pick b */
function genSel(n,k){
  const out=[];
  function go(pos,rem,cur){
    if(rem===0){
      const a=[...cur]; while(a.length<n)a.push(0);
      out.push(a); return;
    }
    if(pos>=n||(n-pos)<rem) return;
    go(pos+1,rem-1,[...cur,1]);
    go(pos+1,rem,  [...cur,0]);
  }
  go(0,k,[]);
  return out;
}

/** HTML superscript version of monomial */
function mono(r,nk){
  let s='';
  if(r===1)      s+='a';
  else if(r>1)   s+=`a<sup>${r}</sup>`;
  if(nk===1)     s+='b';
  else if(nk>1)  s+=`b<sup>${nk}</sup>`;
  return s||'1';
}

/** Unicode superscript text version */
const SUPMAP={'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function usup(n){ return n===1?'':String(n).split('').map(c=>SUPMAP[c]||c).join(''); }
function monoTxt(r,nk){
  let s='';
  if(r>0)  s+='a'+usup(r);
  if(nk>0) s+='b'+usup(nk);
  return s||'1';
}

// ════════════════════════════════════════════════════
//  TAB SWITCHING
// ════════════════════════════════════════════════════
let quizReady=false;
function switchTab(name,btn){
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('show'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('pane-'+name).classList.add('show');
  btn.classList.add('active');
  if(name==='gen') renderGen();
  if(name==='quiz'&&!quizReady){newQ();quizReady=true;}
}

// ════════════════════════════════════════════════════
//  TAB 1 – 선택 시각화
// ════════════════════════════════════════════════════
let vN=4, vK=3;

function onN(){
  vN=parseInt(document.getElementById('nSlider').value);
  document.getElementById('nBadge').textContent=vN;
  const ks=document.getElementById('kSlider');
  ks.max=vN;
  if(vK>vN){vK=vN; ks.value=vK;}
  document.getElementById('kBadge').textContent=vK;
  renderViz();
}
function onK(){
  vK=parseInt(document.getElementById('kSlider').value);
  document.getElementById('kBadge').textContent=vK;
  renderViz();
}

function renderViz(){
  const n=vN, k=vK, nk=n-k;
  const tgt=mono(k,nk);
  document.getElementById('vizTitle').innerHTML=
    `🎯 (a+b)<sup>${n}</sup> 전개 → <span style="color:#fbbf24">${tgt}</span> 항이 만들어지는 모든 선택`;

  const sels=genSel(n,k);
  const grid=document.getElementById('selGrid');
  grid.innerHTML='';

  sels.forEach((sel,i)=>{
    const row=document.createElement('div');
    row.className='sel-row';
    row.style.animationDelay=(i*0.03)+'s';
    let h=`<span class="row-idx">${i+1}</span>`;
    for(let j=0;j<n;j++){
      const pa=sel[j]===1;
      h+=`<span class="factor">`+
         `<span class="paren">(</span>`+
         `<span class="la${pa?' sel-a':''}">a</span>`+
         `<span class="plus-sign">+</span>`+
         `<span class="lb${!pa?' sel-b':''}">b</span>`+
         `<span class="paren">)</span></span>`;
    }
    const seq=sel.map(x=>x?'a':'b').join('');
    h+=`<span class="row-arrow">→</span>`+
       `<span class="row-seq">${seq}</span>`+
       `<span class="row-eq">=</span>`+
       `<span class="row-mono">${monoTxt(k,nk)}</span>`;
    row.innerHTML=h;
    grid.appendChild(row);
  });

  const cnt=sels.length;
  const sum=document.getElementById('vizSummary');
  sum.style.display='block';
  document.getElementById('sumFormula').innerHTML=
    `C(${n}, ${k}) = <span class="sum-coeff">${cnt}</span>`;
  document.getElementById('sumSub').innerHTML=
    `${n}개의 인수 중 <strong style="color:#c4b5fd">${k}개</strong>에서 a를 선택하는 방법 = ` +
    `(a+b)<sup>${n}</sup>에서 ${tgt} 항의 계수 = <strong style="color:#4ade80;font-size:20px">${cnt}</strong>`;
}

// ════════════════════════════════════════════════════
//  TAB 2 – 일반 이항식
// ════════════════════════════════════════════════════
let eN=4, eP=1, eQ=1, selTerm=-1;

function onEN(){
  eN=parseInt(document.getElementById('eNSlider').value);
  document.getElementById('eNBadge').textContent=eN;
  selTerm=-1; renderGen();
}
function adjustPQ(w,d){
  if(w==='p'){
    eP=Math.max(-5,Math.min(5,eP+d));
    if(eP===0) eP+=d;
    document.getElementById('pBadge').textContent=eP;
  } else {
    eQ=Math.max(-5,Math.min(5,eQ+d));
    if(eQ===0) eQ+=d;
    document.getElementById('qBadge').textContent=eQ;
  }
  selTerm=-1; renderGen();
}

function renderGen(){
  const n=eN, p=eP, q=eQ;
  const ps=p<0?'−':'', pc=Math.abs(p)===1?'':Math.abs(p);
  const qs=q<0?'−':'+', qc=Math.abs(q)===1?'':Math.abs(q);
  document.getElementById('expHeading').innerHTML=
    `<span style="color:#c4b5fd;font-size:18px;font-weight:800">`+
    `(${ps}${pc}a ${qs} ${qc}b)<sup>${n}</sup></span> 의 전개식`;

  const wrap=document.getElementById('termsWrap');
  wrap.innerHTML='';
  let first=true;
  for(let r=n;r>=0;r--){
    const nk=n-r;
    const coeff=C(n,r)*Math.pow(p,r)*Math.pow(q,nk);
    const absC=Math.abs(coeff);
    if(!first){
      const op=document.createElement('span');
      op.className='op-sign';
      op.textContent=coeff>=0?'+':'−';
      wrap.appendChild(op);
    } else if(coeff<0){
      const neg=document.createElement('span');
      neg.className='op-sign'; neg.textContent='−';
      wrap.appendChild(neg);
    }
    first=false;
    const chip=document.createElement('span');
    chip.className='term-chip'+(selTerm===r?' sel':'');
    let txt='';
    if(r===0&&nk===0) txt=''+absC;
    else { txt=(absC===1?'':''+absC); if(r>0)txt+=r===1?'a':`a<sup>${r}</sup>`; if(nk>0)txt+=nk===1?'b':`b<sup>${nk}</sup>`; }
    chip.innerHTML=txt;
    chip.onclick=()=>{ selTerm=(selTerm===r)?-1:r; renderGen(); };
    wrap.appendChild(chip);
  }

  const bd=document.getElementById('breakdown');
  if(selTerm>=0){
    const r=selTerm, nk2=n-r;
    const cn=C(n,r), pr=Math.pow(p,r), qnk=Math.pow(q,nk2);
    const tot=cn*pr*qnk;
    const prX=r===0?'1':(r===1?`(${p})`:`(${p})<sup>${r}</sup>`);
    const qX=nk2===0?'1':(nk2===1?`(${q})`:`(${q})<sup>${nk2}</sup>`);
    bd.style.display='block';
    bd.innerHTML=
      `<div class="bd-title">📦 ${mono(r,nk2)} 항의 계수 분해</div>`+
      `<div class="bd-grid">`+
        `<div class="bd-box"><div class="bd-expr">C(${n},${r})</div>`+
          `<div class="bd-v" style="color:#4ade80">${cn}</div>`+
          `<div class="bd-l">${n}개 중 ${r}개에서 a 선택</div></div>`+
        `<div class="bd-op">×</div>`+
        `<div class="bd-box"><div class="bd-expr">${prX}</div>`+
          `<div class="bd-v" style="color:#fbbf24">${pr}</div>`+
          `<div class="bd-l">a 계수 ${p}의 ${r}제곱</div></div>`+
        `<div class="bd-op">×</div>`+
        `<div class="bd-box"><div class="bd-expr">${qX}</div>`+
          `<div class="bd-v" style="color:#f9a8d4">${qnk}</div>`+
          `<div class="bd-l">b 계수 ${q}의 ${nk2}제곱</div></div>`+
        `<div class="bd-op">=</div>`+
        `<div class="bd-res"><div class="bd-rv">${tot}</div><div class="bd-l">계수</div></div>`+
      `</div>`+
      `<div style="font-size:13px;color:#64748b;text-align:center;margin-top:10px">`+
        `C(${n},${r}) × (${p})<sup>${r}</sup> × (${q})<sup>${nk2}</sup> `+
        `= ${cn} × ${pr} × ${qnk} = <strong style="color:#4ade80">${tot}</strong>`+
      `</div>`;
  } else { bd.style.display='none'; }

  renderPascal(n);
}

function renderPascal(hiN){
  const wrap=document.getElementById('pascalWrap');
  wrap.innerHTML='';
  const rows=Math.max(hiN,5);
  for(let n=0;n<=Math.min(rows,9);n++){
    const row=document.createElement('div');
    row.className='p-row';
    const lbl=document.createElement('span');
    lbl.className='p-lbl'; lbl.textContent='n='+n;
    row.appendChild(lbl);
    for(let k=0;k<=n;k++){
      const cell=document.createElement('div');
      cell.className='p-cell'+(n===hiN?' hi':'');
      cell.textContent=C(n,k);
      cell.title=`C(${n},${k})=${C(n,k)}`;
      row.appendChild(cell);
    }
    wrap.appendChild(row);
  }
}

// ════════════════════════════════════════════════════
//  TAB 3 – 계수 퀴즈
// ════════════════════════════════════════════════════
let qN,qP,qQ,qR,qAns,qAnswered=false;
let scOk=0,scNg=0;

function newQ(){
  qAnswered=false;
  qN=Math.floor(Math.random()*5)+2;
  do{qP=Math.floor(Math.random()*7)-3;}while(qP===0);
  do{qQ=Math.floor(Math.random()*7)-3;}while(qQ===0);
  qR=Math.floor(Math.random()*(qN+1));
  const nk=qN-qR;
  qAns=C(qN,qR)*Math.pow(qP,qR)*Math.pow(qQ,nk);
  const ps=qP<0?'−':'', pc=Math.abs(qP)===1?'':Math.abs(qP);
  const qs=qQ<0?'−':'+', qc=Math.abs(qQ)===1?'':Math.abs(qQ);
  document.getElementById('qExp').innerHTML=`(${ps}${pc}a ${qs} ${qc}b)<sup>${qN}</sup>`;
  document.getElementById('qTarget').innerHTML=
    (qR===0&&nk===0)?'상수항의 계수':mono(qR,nk)+'의 계수';
  const inp=document.getElementById('qInput');
  inp.value=''; inp.disabled=false; inp.style.borderColor='';
  document.getElementById('qFeedback').style.display='none';
  document.getElementById('qHint').style.display='none';
}

function checkAns(){
  if(qAnswered){newQ();return;}
  const v=parseInt(document.getElementById('qInput').value);
  if(isNaN(v)){document.getElementById('qInput').style.borderColor='#f87171';return;}
  document.getElementById('qInput').style.borderColor='';
  qAnswered=true;
  document.getElementById('qInput').disabled=true;
  const fb=document.getElementById('qFeedback');
  fb.style.display='block';
  const nk=qN-qR, cn=C(qN,qR), pr=Math.pow(qP,qR), qnk=Math.pow(qQ,nk);
  if(v===qAns){
    scOk++; fb.className='feedback fb-ok'; fb.innerHTML=`🎉 정답! 계수는 <strong>${qAns}</strong>`;
  } else {
    scNg++; fb.className='feedback fb-ng'; fb.innerHTML=`❌ 아쉬워요. 정답은 <strong>${qAns}</strong>`;
  }
  const tot=scOk+scNg;
  document.getElementById('scOk').textContent=scOk;
  document.getElementById('scNg').textContent=scNg;
  document.getElementById('scRt').textContent=Math.round(scOk/tot*100)+'%';
  document.getElementById('scTr').textContent=tot;
  const hint=document.getElementById('qHint');
  hint.style.display='block';
  document.getElementById('qHintBody').innerHTML=
    `C(${qN},${qR}) × (${qP})<sup>${qR}</sup> × (${qQ})<sup>${nk}</sup><br>`+
    `= <strong style="color:#c4b5fd">${cn}</strong> × `+
    `<strong style="color:#fbbf24">${pr}</strong> × `+
    `<strong style="color:#f9a8d4">${qnk}</strong>`+
    ` = <strong style="color:#4ade80;font-size:20px">${qAns}</strong>`;
}

// ════════════════════════════════════════════════════
//  TAB 4 – 도전 모드
// ════════════════════════════════════════════════════
let diff='easy', chalTimer=null;
let cScore=0, cOk=0, cNg=0, combo=0, highScore=0;
let cN,cP,cQ,cR,cAns,cAnswered=false,timeLeft=60;
const TOTAL_SEC=60, ARC=238.76;

const DIFF_CFG={
  easy: {nMax:3, pMax:2, qMax:2, base:10, label:'🌱 쉬움', cls:'diff-easy'},
  mid:  {nMax:5, pMax:3, qMax:3, base:20, label:'🔥 보통' , cls:'diff-mid'},
  hard: {nMax:7, pMax:5, qMax:5, base:30, label:'⚡ 어려움', cls:'diff-hard'},
};

function setDiff(d,btn){
  diff=d;
  document.querySelectorAll('.diff-btn').forEach(b=>{
    b.className='diff-btn';
  });
  btn.className='diff-btn active-'+d;
}

function startChallenge(){
  document.getElementById('chalStart').style.display='none';
  document.getElementById('diffRow').style.display='none';
  document.getElementById('chalGame').style.display='block';
  document.getElementById('chalOver').style.display='none';
  cScore=0; cOk=0; cNg=0; combo=0; timeLeft=TOTAL_SEC;
  updateChalUI();
  newChalQ();
  chalTimer=setInterval(tick,1000);
}

function tick(){
  timeLeft--;
  document.getElementById('timerText').textContent=timeLeft;
  document.getElementById('timerArc').style.strokeDashoffset=
    (ARC*(1-timeLeft/TOTAL_SEC)).toFixed(2);
  if(timeLeft<=10) document.getElementById('timerArc').style.stroke='#f87171';
  if(timeLeft<=0) endChallenge();
}

function endChallenge(){
  clearInterval(chalTimer); chalTimer=null;
  const finalScore = cScore;  // 게임 종료 시점 점수를 즉시 고정
  document.getElementById('chalGame').style.display='none';
  const over=document.getElementById('chalOver');
  over.style.display='block';
  if(finalScore>highScore) highScore=finalScore;
  document.getElementById('goScore').textContent=finalScore+'점';
  const msgs=['잘했어요! 계속 연습해 보세요.','훌륭해요! 이항정리 마스터!','대단해요! 완벽한 실력이에요!'];
  const lvl=finalScore<100?0:finalScore<250?1:2;
  document.getElementById('goMsg').innerHTML=
    `✅ ${cOk}문제 정답 &nbsp;|&nbsp; ❌ ${cNg}문제 오답 &nbsp;|&nbsp; `+msgs[lvl];
  document.getElementById('goBest').textContent=`🏅 최고 기록: ${highScore}점`;
  // JS → GAS 자동 제출 (로그인 학생만)
  const statusEl=document.getElementById('scoreSubmitStatus');
  if(!_U.id || !_U.gasUrl){
    statusEl.textContent='ℹ️ 로그인 학생만 랭킹에 기록됩니다.';
    return;
  }
  if(finalScore<=0){
    statusEl.textContent='ℹ️ 0점은 랭킹에 기록되지 않습니다.';
    return;
  }
  statusEl.textContent=`📡 점수(${finalScore}점) 저장 중...`;
  statusEl.style.color='#94a3b8';
  const now=new Date();
  const kst=new Date(now.getTime()+9*3600*1000);
  const ts=kst.toISOString().replace('T',' ').slice(0,19);
  const payload=JSON.stringify({
    sheet:'이항정리랭킹', timestamp:ts,
    학번:_U.id, 이름:_U.name,
    점수:finalScore,
    난이도:DIFF_CFG[diff].label
  });
  fetch(_U.gasUrl,{method:'POST',body:payload,
    headers:{'Content-Type':'text/plain'},redirect:'follow'})
  .then(r=>{
    if(!r.ok && r.status!==0) throw new Error(r.status);
    statusEl.textContent='✅ 점수 저장 완료! 아래 랭킹을 새로고침하세요.';
    statusEl.style.color='#6ee7b7';
  }).catch(()=>{
    statusEl.textContent='⚠️ 점수 저장 실패 (잠시 후 다시 시도하세요)';
    statusEl.style.color='#fca5a5';
  });
}

function restartChallenge(){
  document.getElementById('chalOver').style.display='none';
  document.getElementById('chalStart').style.display='block';
  document.getElementById('diffRow').style.display='flex';
  // Reset diff badge
  document.querySelectorAll('.diff-btn').forEach(b=>b.className='diff-btn');
  document.getElementById('d'+diff.charAt(0).toUpperCase()+diff.slice(1)).className='diff-btn active-'+diff;
  document.getElementById('timerArc').style.stroke='#fbbf24';
  document.getElementById('timerArc').style.strokeDashoffset='0';
  document.getElementById('timerText').textContent='60';
}

function newChalQ(){
  cAnswered=false;
  const cfg=DIFF_CFG[diff];
  cN=Math.floor(Math.random()*cfg.nMax)+1+Math.floor(cfg.nMax/3);
  cN=Math.min(cN,cfg.nMax);
  do{cP=Math.floor(Math.random()*(cfg.pMax*2+1))-cfg.pMax;}while(cP===0);
  do{cQ=Math.floor(Math.random()*(cfg.qMax*2+1))-cfg.qMax;}while(cQ===0);
  cR=Math.floor(Math.random()*(cN+1));
  const nk=cN-cR;
  cAns=C(cN,cR)*Math.pow(cP,cR)*Math.pow(cQ,nk);
  const ps=cP<0?'−':'', pc=Math.abs(cP)===1?'':Math.abs(cP);
  const qs=cQ<0?'−':'+', qc=Math.abs(cQ)===1?'':Math.abs(cQ);
  document.getElementById('cExp').innerHTML=`(${ps}${pc}a ${qs} ${qc}b)<sup>${cN}</sup>`;
  document.getElementById('cTarget').innerHTML=
    (cR===0&&nk===0)?'상수항의 계수':mono(cR,nk)+'의 계수';
  const badge=document.getElementById('cDiffBadge');
  badge.className='diff-badge '+cfg.cls;
  badge.textContent=cfg.label;
  const inp=document.getElementById('cInput');
  inp.value=''; inp.disabled=false; inp.style.borderColor=''; inp.focus();
  document.getElementById('cFeedback').style.display='none';
}

function checkChal(){
  if(!chalTimer||cAnswered) return;
  const v=parseInt(document.getElementById('cInput').value);
  if(isNaN(v)){document.getElementById('cInput').style.borderColor='#f87171';return;}
  document.getElementById('cInput').style.borderColor='';
  cAnswered=true;
  document.getElementById('cInput').disabled=true;
  const cfg=DIFF_CFG[diff];
  const fb=document.getElementById('cFeedback');
  fb.style.display='block';
  if(v===cAns){
    cOk++; combo++;
    const mul=Math.min(combo,3);
    const pts=cfg.base*mul; cScore+=pts;
    fb.className='feedback fb-ok';
    fb.innerHTML=`🎉 정답! <strong>+${pts}점</strong>${combo>=2?' (×'+mul+' 콤보!)':''}`;
    updateCombo(combo);
  } else {
    cNg++; combo=0;
    const penalty=10;
    cScore=Math.max(0, cScore-penalty);
    fb.className='feedback fb-ng';
    fb.innerHTML=`❌ 아쉬워요! 답은 <strong>${cAns}</strong> &nbsp;<span style="color:#f87171;font-weight:800">−${penalty}점</span>`;
    updateCombo(0);
  }
  updateChalUI();
  setTimeout(()=>{if(chalTimer)newChalQ();},900);
}

function updateChalUI(){
  document.getElementById('cScore').textContent=cScore;
  document.getElementById('cOk').textContent=cOk;
  document.getElementById('cNg').textContent=cNg;
}

function updateCombo(c){
  const ring=document.getElementById('comboRing');
  const val=document.getElementById('comboVal');
  ring.style.display= c>=2 ? 'block' : 'none';
  val.textContent='× '+Math.min(c,3);
  if(c>=3) val.style.color='#f97316';
  else if(c>=2) val.style.color='#fbbf24';
  else val.style.color='#94a3b8';
}

// ════════════════════════════════════════════════════
//  INIT
// ════════════════════════════════════════════════════
renderViz();
</script>
</body></html>"""
    # <head> 닫기 바로 앞에 _U 삽입 (줄바꿈 방식 대신 태그 단위로 교체 → CRLF 무관)
    return raw.replace('</head>', init + '</head>', 1)
