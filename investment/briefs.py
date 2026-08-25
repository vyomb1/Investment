"""Builds the analyst brief sent to the council.

The council forwards one query verbatim to every member (Stage 1), so the
entire investment framing lives here, in the query itself. One brief per
run, identical for every member — that is what keeps Stage 1 independent.
"""

BRIEF_TEMPLATE = """\
You are acting as an independent investment analyst. Give your own view; do not hedge toward an imagined consensus.

Question: {question}
{context_block}
Structure your answer exactly as:
1. Thesis — your view in one paragraph
2. Bull case — the strongest arguments for
3. Bear case — the strongest arguments against
4. Key risks and unknowns
5. What evidence would change your mind
6. Confidence — low, medium, or high, and why

Be concrete and quantitative where you can. If you lack current data, say so plainly rather than inventing figures. This is research input, not financial advice."""


def build_brief(question: str, context: str | None = None) -> str:
    context_block = ""
    if context:
        context_block = f"\nContext provided by the researcher:\n{context.strip()}\n"
    return BRIEF_TEMPLATE.format(question=question.strip(), context_block=context_block)
