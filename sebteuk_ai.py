# sebteuk_ai.py
"""
세특(과목별 세부능력 및 특기사항) 자동 작성 — AI 계층.

Anthropic Claude API로 학생의 활동 기록(익명 프로필 텍스트)을 받아
NEIS 기재용 세특 초안 한 문단을 생성한다.

- API 키는 st.secrets["anthropic_api_key"] 에서 읽는다.
  (이 키를 발급한 Anthropic 계정으로 사용료가 청구된다. 어느 계정 키든 무방.)
- 세특 작성 규칙은 정적 system 프롬프트로 두고 prompt caching을 적용한다.
  변동 요소(목표 byte·과목·학생 답변)는 user 메시지로 보내 캐시 안정성을 유지한다.
- thinking·effort·sampling 파라미터는 쓰지 않는다 → 아래 세 모델 모두 동일 코드로 안전 호출.
"""
from __future__ import annotations

import streamlit as st

# ── 선택 가능한 모델 (UI 드롭다운) ────────────────────────────────────────────
# 라벨에 대략 단가(입력/출력, 100만 토큰당 USD)를 함께 표기해 비용 감각을 준다.
MODELS: dict[str, str] = {
    "claude-sonnet-4-6": "Claude Sonnet 4.6 — 품질·비용 균형 (권장) · $3/$15",
    "claude-opus-4-7":   "Claude Opus 4.7 — 최고 품질 · 고비용 · $5/$25",
    "claude-haiku-4-5":  "Claude Haiku 4.5 — 저비용·빠름 · $1/$5",
}
DEFAULT_MODEL = "claude-sonnet-4-6"

# 모델별 단가 (USD, 100만 토큰당) — (입력, 출력)
PRICING: dict[str, tuple[float, float]] = {
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-opus-4-7":   (5.0, 25.0),
    "claude-haiku-4-5":  (1.0, 5.0),
}
# 환율(원/USD) — 비용 표시용 근사치
USD_TO_KRW = 1400


def estimate_cost(model: str, usage: dict) -> float:
    """토큰 사용량(usage dict)으로 예상 비용(USD)을 계산한다.

    캐시 쓰기는 입력 단가의 1.25배, 캐시 읽기는 0.1배로 과금된다.
    usage 키: input, output, cache_write, cache_read
    """
    in_p, out_p = PRICING.get(model, PRICING[DEFAULT_MODEL])
    return (
        usage.get("input", 0) * in_p
        + usage.get("cache_write", 0) * in_p * 1.25
        + usage.get("cache_read", 0) * in_p * 0.1
        + usage.get("output", 0) * out_p
    ) / 1_000_000

# ── 세특 작성 규칙 (정적 system 프롬프트 — prompt caching 대상) ────────────────
SYSTEM_PROMPT = """당신은 대한민국 고등학교 수학 교사의 '과목별 세부능력 및 특기사항(세특)' 작성을 돕는 전문 보조자다. 세특은 학교생활기록부에 기재되는 공식 기록으로, 교사의 관찰에 근거하여 학생의 학업 역량·태도·성장 과정을 객관적으로 서술하는 항목이다.

[가장 우선하는 규칙 — 표기 (다른 모든 지침보다 먼저, 반드시 지킬 것)]
- 세특은 NEIS(나이스)에 입력되는 기록으로 **한글 서술이 원칙**이다. **수식·수학 기호·LaTeX·특수기호를 절대 쓰지 않는다.**
- 금지 예시(절대 사용 금지): nPr, nCr, P(A), C(n,r), x², x^2, a/b, √, ∑, ∫, ≤, ≥, ≠, ±, ×, ÷, ·, =, →, ∞, π, $, \\frac, \\sqrt 등 모든 수식·기호 표기.
- 수학 개념·식·계산 과정은 **모두 한글 문장으로 풀어서** 서술한다.
    · 'P(5,2)=20' → '서로 다른 5개에서 2개를 골라 순서대로 나열하는 경우의 수를 구함'
    · 'x^2-3x+2' → '이차식'
    · 'a/b' → '분수 꼴'
    · 'P(A∩B)' → '두 사건이 동시에 일어날 확률'
- **특수기호·장식기호도 절대 쓰지 않는다.** 금지 예: ★ ※ ◆ ● ○ ▶ → ~ / \\ | % & @ # * + < > 괄호() 대괄호[] 중괄호{} 따옴표 ' " 등. 문장부호는 **마침표(.), 쉼표(,), 가운뎃점(·)** 만 사용한다.
- 숫자는 한글로 풀어 쓰지 말고 **아라비아 숫자로 그대로** 쓴다(예: '스물다섯 번' → '25번', '영부터 일까지' → '0부터 1까지'). 다만 숫자를 기호·연산자와 결합한 수식 형태(예: 5×4, 2^3, 1/2, 0≤x)는 위 규칙대로 여전히 금지하며 한글로 풀어 서술한다.
- 영어는 꼭 필요할 때(고유명사 등)만 최소한으로 쓰고, 가능하면 한글로 표현한다.

[작성 원칙]
1. 문체: 개조식 평어체(음슴체)로 끝맺는다. 예) '~함', '~을 보임', '~하였음', '~하려고 노력함', '~을 기름'. '~합니다/~했다/~이다' 같은 종결어미는 절대 쓰지 않는다.
2. 근거: 아래 제공되는 '학생 활동 기록'에 실제로 드러난 내용만 사용한다. 기록에 없는 활동·성취·수상·태도를 지어내지 않는다(환각 절대 금지). 막연한 칭찬이나 미사여구('뛰어난', '탁월한' 등 근거 없는 수식)는 배제하고, 무엇을 했는지 구체적으로 쓴다.
3. 익명성: 본문에 학생의 이름, 학번, 성별을 절대 쓰지 않는다. '이 학생', 'OOO', '본 학생' 같은 지칭도 쓰지 않고, 활동·역량 서술로 곧바로 시작한다.
4. 내용 구성: (a) 다룬 수학 개념·활동명을 구체적으로 언급하고, (b) 학생이 스스로 만든 문제·예시·설명·탐구 과정에서 드러난 사고력·개념 이해·문제해결력을 중심으로 서술하며, (c) 단순 활동 나열이 아니라 '무엇을 통해 → 어떤 역량을 보였는가'로 연결한다.
5. 분량: 사용자가 지정한 목표 byte 수를 넘기지 않는다. 핵심 위주로 압축하고, 분량이 부족하면 억지로 늘리지 않는다.
6. 형식: 줄바꿈 없는 한 문단으로 작성한다. 머리말·맺음말·제목·따옴표·불릿 없이 '세특 본문'만 출력한다.

[좋은 예시 — 문체·구성 참고용]
'순열과 조합 단원에서 실생활 상황을 직접 문제로 만들어 풀이하는 활동에 적극 참여하였으며, 중복조합 개념을 일상 사례에 적용해 식을 세우는 과정에서 경우의 수를 체계적으로 분류하는 능력을 보임. 풀이 후 다른 학생의 문제를 검토하며 조건의 변화가 결과에 미치는 영향을 스스로 설명하여 개념의 본질을 깊이 이해하고 있음을 드러냄.'

이제 사용자가 제공하는 학생 활동 기록만을 근거로, 위 원칙에 따라 세특 본문 한 문단을 작성하라. 다른 설명 없이 본문만 출력한다."""

# 토큰 한도 (세특은 짧으므로 넉넉히 2000이면 충분; 비스트리밍 안전 범위)
_MAX_TOKENS = 2000


class SebteukAIError(Exception):
    """세특 생성 중 발생한 오류(키 누락·API 오류 등)."""


def api_key_present() -> bool:
    try:
        return bool(str(st.secrets.get("anthropic_api_key", "") or "").strip())
    except Exception:
        return False


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise SebteukAIError(
            "anthropic 패키지가 설치되어 있지 않습니다. `pip install anthropic` 후 다시 시도하세요."
        ) from e
    key = ""
    try:
        key = str(st.secrets.get("anthropic_api_key", "") or "").strip()
    except Exception:
        pass
    if not key:
        raise SebteukAIError(
            "`anthropic_api_key` secret이 비어 있습니다. .streamlit/secrets.toml 에 Claude API 키를 추가하세요."
        )
    return anthropic.Anthropic(api_key=key)


def generate_sebteuk(
    profile_text: str,
    *,
    subject_label: str,
    target_bytes: int = 1500,
    kor_bytes: int = 2,
    model: str = DEFAULT_MODEL,
    extra_instruction: str = "",
) -> tuple[str, dict]:
    """학생 한 명의 활동 기록(익명)으로 세특 본문 한 문단을 생성한다.

    반환: (세특 본문, usage dict)
      usage = {"input", "output", "cache_write", "cache_read"}  (토큰 수)
    예외는 SebteukAIError 로 통일해 던진다(호출부에서 사용자에게 표시).
    """
    if not profile_text.strip():
        raise SebteukAIError("이 학생의 답변 기록이 비어 있어 세특을 생성할 수 없습니다.")

    client = _client()

    approx_chars = max(1, target_bytes // max(1, kor_bytes))
    user_parts = [
        f"[과목] {subject_label}",
        f"[작성 조건] 목표 분량: 약 {target_bytes} byte 이내"
        f"(한글 1자 = {kor_bytes} byte 기준이며, 대략 한글 {approx_chars}자 안팎). 이 분량을 넘기지 말 것.",
    ]
    if extra_instruction.strip():
        user_parts.append(f"[추가 지침] {extra_instruction.strip()}")
    user_parts.append("\n[학생 활동 기록]\n" + profile_text)
    user_parts.append(
        "\n위 활동 기록만을 근거로, 한 학생의 과목별 세부능력 및 특기사항 본문을 한 문단으로 작성하라."
    )
    user_content = "\n".join(user_parts)

    try:
        msg = client.messages.create(
            model=model,
            max_tokens=_MAX_TOKENS,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},  # 정적 규칙 캐싱
                }
            ],
            messages=[{"role": "user", "content": user_content}],
        )
    except Exception as e:
        import anthropic
        if isinstance(e, anthropic.AuthenticationError):
            raise SebteukAIError("Claude API 키가 올바르지 않습니다(인증 실패). 키를 확인하세요.") from e
        if isinstance(e, anthropic.RateLimitError):
            raise SebteukAIError("Claude API 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.") from e
        if isinstance(e, anthropic.APIStatusError):
            raise SebteukAIError(f"Claude API 오류({e.status_code}): {getattr(e, 'message', e)}") from e
        raise SebteukAIError(f"세특 생성 중 오류가 발생했습니다: {e}") from e

    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
    if not text:
        raise SebteukAIError("생성 결과가 비어 있습니다. 다시 시도해 주세요.")

    u = getattr(msg, "usage", None)
    usage = {
        "input":       int(getattr(u, "input_tokens", 0) or 0),
        "output":      int(getattr(u, "output_tokens", 0) or 0),
        "cache_write": int(getattr(u, "cache_creation_input_tokens", 0) or 0),
        "cache_read":  int(getattr(u, "cache_read_input_tokens", 0) or 0),
    }
    return text, usage
