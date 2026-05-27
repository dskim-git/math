# pages/96_세특작성.py
"""
세특 자동 작성 (관리자 전용)

학생들이 성찰 기록 구글 시트(공통수학·확률과통계)에 제출한 답변을 바탕으로
Claude API를 이용해 학생별 과목별 세부능력 및 특기사항(세특) 초안을 생성한다.

접근 권한: 관리자(admin)만. (교사·학생·일반인 접근 불가)

생성물은 항상 '초안'이며 화면에서 편집 가능하다. 교사 검토 후 사용할 것.
개인정보 보호: 외부 AI에는 학번·이름을 보내지 않고 답변 내용만 전송하며,
학번 → 결과 매핑은 로컬에서 자동·정확하게 복원된다.
"""
import sys
import time
from io import StringIO
from pathlib import Path

_root = str(Path(__file__).parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

import pandas as pd
import streamlit as st

st.set_page_config(page_title="세특 작성", layout="wide")

from theme_utils import inject_dark_theme, inject_hide_nav
inject_dark_theme()
inject_hide_nav()

import sebteuk_utils as su
import sebteuk_ai as sai

# ── 상단 네비 ──────────────────────────────────────────────────────────────────
_top_l, _top_r = st.columns([4, 1])
with _top_r:
    if st.button("🏠 홈으로", use_container_width=True, key="_seb_home"):
        st.switch_page("home.py")

# ── 접근 제어: 관리자만 ────────────────────────────────────────────────────────
if not st.session_state.get("_authenticated", False):
    st.error("🔒 로그인이 필요합니다.")
    st.info("홈 화면에서 **관리자 계정**으로 로그인하세요.")
    st.stop()
if not st.session_state.get("_dev_mode", False):
    st.error("🔒 이 페이지는 **관리자(admin)** 전용입니다.")
    st.stop()

st.title("✍️ 세특 자동 작성")
st.caption(
    "성찰 기록 시트에 제출된 학생 답변을 바탕으로 Claude AI가 과목별 세특 초안을 생성합니다. "
    "결과는 반드시 검토·수정 후 사용하세요."
)

# ── API 키 상태 안내 ───────────────────────────────────────────────────────────
if not sai.api_key_present():
    st.warning(
        "⚠️ **Claude API 키가 아직 설정되지 않았습니다.** 답변 불러오기·미리보기는 되지만, "
        "세특 **생성**은 키를 넣어야 동작합니다.\n\n"
        "`.streamlit/secrets.toml` 파일에 다음 한 줄을 추가하세요 (원하는 Anthropic 계정의 키):\n"
        "```toml\nanthropic_api_key = \"sk-ant-...\"\n```"
    )

# ── 세션 상태 ──────────────────────────────────────────────────────────────────
ss = st.session_state
ss.setdefault("_seb_subject", "common")
ss.setdefault("_seb_bust", 0)
ss.setdefault("_seb_data", None)          # 로드된 데이터(dict)
ss.setdefault("_seb_loaded_subject", "")  # 현재 로드된 과목
ss.setdefault("_seb_results", {})         # {subject: {학번: 세특본문}}


def _results_for(subject_key: str) -> dict:
    return ss["_seb_results"].setdefault(subject_key, {})


# ── 1) 과목 선택 + 불러오기 ────────────────────────────────────────────────────
st.divider()
c1, c2 = st.columns([3, 1])
with c1:
    subject_key = st.selectbox(
        "과목",
        options=list(su.SUBJECTS.keys()),
        format_func=su.subject_label,
        key="_seb_subject",
    )
with c2:
    st.write("")
    st.write("")
    load_clicked = st.button("📥 답변 불러오기 / 새로고침", use_container_width=True, key="_seb_load")

if load_clicked:
    ss["_seb_bust"] += 1
    with st.spinner("성찰 시트에서 답변을 불러오는 중…"):
        ss["_seb_data"] = su.load_subject_reflections(subject_key, ss["_seb_bust"])
        ss["_seb_loaded_subject"] = subject_key

data = ss["_seb_data"]
if data is None or ss["_seb_loaded_subject"] != subject_key:
    st.info("위 **답변 불러오기** 버튼을 눌러 해당 과목의 학생 답변을 먼저 불러오세요.")
    st.stop()

if not data.get("ok", False):
    st.error(f"데이터를 불러오지 못했습니다: {data.get('error', '알 수 없는 오류')}")
    st.stop()

roster = su.student_roster(data)
n_acts_with_data = sum(1 for a in data["activities"] if a["n_rows"] > 0)

m1, m2, m3 = st.columns(3)
m1.metric("제출 학생 수", f"{len(roster)} 명")
m2.metric("답변이 있는 활동", f"{n_acts_with_data} 개")
m3.metric("총 탭(활동) 수", f"{len(data['activities'])} 개")

if not roster:
    st.warning("아직 제출된 답변이 없습니다.")
    st.stop()

# ── 2) 생성 설정 ───────────────────────────────────────────────────────────────
st.divider()
st.subheader("⚙️ 생성 설정")
sc1, sc2, sc3 = st.columns([2, 1, 1])
with sc1:
    model = st.selectbox(
        "AI 모델",
        options=list(sai.MODELS.keys()),
        format_func=lambda k: sai.MODELS[k],
        index=list(sai.MODELS.keys()).index(sai.DEFAULT_MODEL),
        key="_seb_model",
    )
with sc2:
    target_bytes = st.number_input(
        "목표 분량 (byte)", min_value=100, max_value=4000, value=1500, step=100,
        key="_seb_bytes",
        help="NEIS 과목별 세특은 보통 1500 byte 내외입니다.",
    )
with sc3:
    kor_bytes = st.radio(
        "한글 1자 = ?",
        options=[2, 3],
        format_func=lambda v: f"{v} byte",
        horizontal=True,
        key="_seb_korbytes",
        help="NEIS 환경에 따라 한글을 2byte(EUC-KR 관행) 또는 3byte(UTF-8)로 셉니다.",
    )
extra = st.text_input(
    "추가 지침 (선택)", key="_seb_extra",
    placeholder="예) 탐구 태도를 특히 강조 / 진로(통계학)와 연결 등",
)

with st.expander("💲 모델별 단가 안내", expanded=False):
    st.markdown(
        "API 단가는 **100만 토큰당 USD (입력 / 출력)** 입니다. "
        "토큰은 글자 조각 단위로, 한글 1자 ≈ 1.5~2 토큰입니다. "
        "아래 추정치는 학생 1명당 입력 약 1,300·출력 약 800 토큰 가정입니다.\n\n"
        "| 모델 | 입력/출력 | 학생 1명 | 30명(한 반) |\n"
        "|---|---|---|---|\n"
        "| Sonnet 4.6 (권장) | \\$3 / \\$15 | ~\\$0.016 (≈22원) | ~\\$0.48 (≈670원) |\n"
        "| Opus 4.7 | \\$5 / \\$25 | ~\\$0.027 (≈37원) | ~\\$0.80 (≈1,100원) |\n"
        "| Haiku 4.5 | \\$1 / \\$5 | ~\\$0.005 (≈7원) | ~\\$0.16 (≈220원) |\n\n"
        f"※ 환율 약 {sai.USD_TO_KRW:,}원/USD 근사. **prompt caching** 적용으로 같은 과목을 "
        "연달아 생성하면 입력 비용이 추가로 약 90% 절감됩니다. 실제 비용은 학생이 작성한 분량에 따라 달라집니다."
    )

results = _results_for(subject_key)

# ── 3) 작업 탭: 학생 1명 / 전체 일괄 ──────────────────────────────────────────
st.divider()
tab_one, tab_batch = st.tabs(["👤 학생 한 명씩", "📚 전체 일괄 생성"])

# ── 3-A) 학생 한 명 ────────────────────────────────────────────────────────────
with tab_one:
    labels = {f"{r['학번']}  {r['이름']}  (활동 {r['활동수']}개)": r["학번"] for r in roster}
    sel_label = st.selectbox("학생 선택", options=list(labels.keys()), key="_seb_one_sel")
    sel_num = labels[sel_label]
    sel_name = next((r["이름"] for r in roster if r["학번"] == sel_num), "")

    stu_acts = su.student_activities(data, sel_num)
    if len(stu_acts) >= 2:
        selected_acts = st.multiselect(
            f"세특에 반영할 활동 선택 (이 학생은 {len(stu_acts)}개 활동에 답변함)",
            options=stu_acts, default=stu_acts,
            key=f"_seb_acts_{subject_key}_{sel_num}",
        )
        if not selected_acts:
            st.warning("활동을 1개 이상 선택해야 세특을 생성할 수 있습니다.")
    else:
        selected_acts = stu_acts

    profile = su.build_profile_text(data, sel_num, selected_acts)
    with st.expander("📄 이 학생의 답변 보기 (선택한 활동만 · AI 입력 원본 — 학번·이름 제외)", expanded=False):
        st.markdown(f"**학번** `{sel_num}`　**이름** {sel_name}　**선택 활동** {len(selected_acts)}개")
        st.text(profile or "(선택된 답변 없음)")

    tb = int(target_bytes)

    def _byte_caption(text: str) -> None:
        n = su.neis_bytes(text, int(kor_bytes))
        st.caption(f"현재 {n} byte / 목표 {tb} byte"
                   + ("　🔴 **초과** — 줄여 주세요." if n > tb else "　🟢 적정"))

    def _generate_for(num: str) -> str:
        """초기 생성·다시 생성 공용. 생성 후 사용량을 기록한다."""
        text, usage = sai.generate_sebteuk(
            su.build_profile_text(data, num, selected_acts),
            subject_label=su.subject_label(subject_key),
            target_bytes=tb,
            kor_bytes=int(kor_bytes),
            model=model,
            extra_instruction=extra,
        )
        su.log_usage(model, su.subject_label(subject_key), 1,
                     usage, sai.estimate_cost(model, usage))
        su.load_usage_summary.clear()
        return text

    draftver_key = f"_seb_draftver_{subject_key}_{sel_num}"
    ss.setdefault(draftver_key, 0)

    # 아직 생성 전 → 생성 버튼
    if sel_num not in results:
        if st.button("✨ 세특 생성", type="primary", key="_seb_gen_one",
                     disabled=not sai.api_key_present() or not selected_acts,
                     use_container_width=True):
            try:
                with st.spinner(f"{sel_name} 학생의 세특을 생성하는 중…"):
                    results[sel_num] = _generate_for(sel_num)
                ss[draftver_key] += 1
                st.rerun()
            except sai.SebteukAIError as e:
                st.error(str(e))

    # 생성 후 → 초안 편집 + 다시 생성
    if sel_num in results:
        st.markdown("#### 🤖 AI 생성 초안")
        draft_key = f"_seb_draft_{subject_key}_{sel_num}_{ss[draftver_key]}"
        draft = st.text_area("세특 초안 (편집 가능)", value=results[sel_num],
                             height=180, key=draft_key)
        results[sel_num] = draft
        _byte_caption(draft)

        if st.button("🔄 다시 생성", key="_seb_regen",
                     disabled=not sai.api_key_present() or not selected_acts,
                     use_container_width=True):
            try:
                with st.spinner("세특을 다시 생성하는 중…"):
                    results[sel_num] = _generate_for(sel_num)
                ss[draftver_key] += 1
                st.rerun()
            except sai.SebteukAIError as e:
                st.error(str(e))

        # ── 최종 다듬기 & 시트 저장 ──────────────────────────────────────────
        st.divider()
        st.markdown("#### ✍️ 최종 다듬기 & 저장")
        st.caption(
            "아래 칸에 초안을 가져와 직접 수정한 뒤 저장하면, "
            f"**{su.subject_label(subject_key)}** 성찰 시트의 `세특기록` 탭에 "
            "학번·이름과 함께 기록됩니다(같은 학번은 덮어쓰기)."
        )

        ss.setdefault("_seb_final", {})
        finalver_key = f"_seb_finalver_{subject_key}_{sel_num}"
        ss.setdefault(finalver_key, 0)
        final_map_key = f"{subject_key}::{sel_num}"

        if st.button("⬇️ 위 초안 가져오기", key="_seb_pull", use_container_width=True):
            ss["_seb_final"][final_map_key] = results[sel_num]
            ss[finalver_key] += 1
            st.rerun()

        final_key = f"_seb_finaltext_{subject_key}_{sel_num}_{ss[finalver_key]}"
        final_val = ss["_seb_final"].get(final_map_key, "")
        final_text = st.text_area(
            "최종 세특 (직접 다듬는 칸)", value=final_val, height=180, key=final_key,
            placeholder="‘위 초안 가져오기’를 누르거나 직접 입력해 다듬으세요.",
        )
        ss["_seb_final"][final_map_key] = final_text
        _byte_caption(final_text)

        if st.button(
            f"📤 구글 시트에 저장  ·  {su.subject_label(subject_key)} → 세특기록",
            type="primary", key="_seb_save", use_container_width=True,
            disabled=not final_text.strip(),
        ):
            with st.spinner("저장 중…"):
                ok, msg = su.save_final_sebteuk(subject_key, sel_num, sel_name, final_text)
            if ok:
                st.success(
                    f"✅ {sel_name}({sel_num}) 학생의 세특을 "
                    f"`{su.subject_label(subject_key)} · 세특기록` 시트에 {msg}했습니다."
                )
            else:
                st.error(f"저장 실패: {msg}")

# ── 3-B) 전체 일괄 ─────────────────────────────────────────────────────────────
with tab_batch:
    st.write(f"제출 학생 **{len(roster)}명** 전체에 대해 세특을 한 번에 생성합니다.")
    st.caption("학생 수가 많으면 시간이 걸립니다. 생성 후 표에서 직접 수정할 수 있습니다.")

    bc1, bc2 = st.columns(2)
    with bc1:
        run_batch = st.button(
            "🚀 전체 생성", type="primary", key="_seb_run_batch",
            disabled=not sai.api_key_present(), use_container_width=True,
        )
    with bc2:
        only_missing = st.checkbox("이미 생성된 학생은 건너뛰기", value=True, key="_seb_skip_done")

    if run_batch:
        progress = st.progress(0.0, text="시작 중…")
        targets = [r for r in roster if not (only_missing and r["학번"] in results)]
        total = len(targets)
        fail = 0
        batch_usage = {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0}
        for i, r in enumerate(targets, start=1):
            num, name = r["학번"], r["이름"]
            progress.progress(i / max(1, total), text=f"{i}/{total} · {name}({num}) 생성 중…")
            try:
                profile = su.build_profile_text(data, num)
                text, usage = sai.generate_sebteuk(
                    profile,
                    subject_label=su.subject_label(subject_key),
                    target_bytes=int(target_bytes),
                    kor_bytes=int(kor_bytes),
                    model=model,
                    extra_instruction=extra,
                )
                results[num] = text
                for k in batch_usage:
                    batch_usage[k] += usage.get(k, 0)
            except sai.SebteukAIError as e:
                fail += 1
                results[num] = f"[생성 실패: {e}]"
            time.sleep(0.3)  # API rate limit 완화
        progress.empty()
        success = total - fail
        if success > 0:
            # 일괄 사용량을 1건으로 합산 기록
            su.log_usage(model, su.subject_label(subject_key), success,
                         batch_usage, sai.estimate_cost(model, batch_usage))
            su.load_usage_summary.clear()
        if fail:
            st.warning(f"완료 — 성공 {success}명 / 실패 {fail}명")
        else:
            st.success(f"완료 — {total}명 생성")

    # ── 결과 표 (편집 가능) + 내보내기 ────────────────────────────────────────
    if results:
        rows = []
        name_by_num = {r["학번"]: r["이름"] for r in roster}
        for num, text in sorted(results.items()):
            rows.append({
                "학번": num,
                "이름": name_by_num.get(num, ""),
                "세특": text,
                "byte": su.neis_bytes(text, int(kor_bytes)),
            })
        df = pd.DataFrame(rows, columns=["학번", "이름", "세특", "byte"])

        st.markdown("#### 📋 생성 결과 (세특 칸을 더블클릭하여 직접 수정 가능)")
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            disabled=["학번", "이름", "byte"],
            column_config={
                "세특": st.column_config.TextColumn("세특", width="large"),
                "byte": st.column_config.NumberColumn("byte", help="현재 byte 수"),
            },
            key=f"_seb_editor_{subject_key}",
        )
        # 편집 내용을 세션 결과에 반영
        for _, row in edited_df.iterrows():
            results[str(row["학번"])] = str(row["세특"])

        csv_buf = StringIO()
        edited_df[["학번", "이름", "세특"]].to_csv(csv_buf, index=False)
        st.download_button(
            "⬇️ CSV로 내보내기 (Excel 호환)",
            data=("﻿" + csv_buf.getvalue()).encode("utf-8"),  # BOM → Excel 한글 호환
            file_name=f"세특_{su.subject_label(subject_key)}.csv",
            mime="text/csv",
            use_container_width=True,
            key="_seb_dl_csv",
        )

# ── 누적 사용량 / 비용 (이 앱에서 생성한 전체 누적) ────────────────────────────
st.divider()
st.subheader("📊 누적 사용량 & 예상 비용")
_summary = su.load_usage_summary()
_krw = _summary["cost_usd"] * sai.USD_TO_KRW
u1, u2, u3 = st.columns(3)
u1.metric("누적 생성 세특", f"{_summary['students']:,} 건")
u2.metric("누적 토큰", f"{_summary['tokens_total']:,}")
u3.metric("누적 예상 비용", f"${_summary['cost_usd']:.3f}")
st.caption(
    f"≈ **{_krw:,.0f}원** (환율 약 {sai.USD_TO_KRW:,}원/USD 근사). "
    "이 앱에서 생성한 누적값이며, prompt caching·실제 분량에 따라 콘솔 청구액과 다를 수 있습니다. "
    "Anthropic은 잔액 조회 API를 제공하지 않으므로 **정확한 크레딧 잔액은 콘솔에서 확인**하세요."
)
uc1, uc2 = st.columns(2)
with uc1:
    if st.button("🔄 사용량 새로고침", use_container_width=True, key="_seb_usage_refresh"):
        su.load_usage_summary.clear()
        st.rerun()
with uc2:
    st.link_button(
        "🔗 Anthropic 콘솔에서 잔액·사용량 보기",
        "https://console.anthropic.com/settings/usage",
        use_container_width=True,
    )
