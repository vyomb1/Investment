"""No-network tests: brief framing, council client flow, memo rendering, CLI.

The one structural invariant to protect: a run sends the council exactly one
brief, and all investment framing lives in that brief — so every council
member deliberates over the same input (Stage 1 independence is preserved
upstream). Run: uv run python -m unittest discover -s tests -v
"""

import asyncio
import contextlib
import datetime
import io
import json
import tempfile
import unittest
from pathlib import Path

import httpx

from investment.__main__ import main, render_memo, slugify
from investment.briefs import build_brief
from investment.council_client import deliberate

COUNCIL_RESULT = {
    "stage1": [
        {"model": "vendor-a/alpha", "response": "alpha analysis"},
        {"model": "vendor-b/beta", "response": "beta analysis"},
    ],
    "stage2": [
        {
            "model": "vendor-a/alpha",
            "ranking": "FINAL RANKING:\n1. Response B\n2. Response A",
            "parsed_ranking": ["Response B", "Response A"],
        },
        {
            "model": "vendor-b/beta",
            "ranking": "FINAL RANKING:\n1. Response B\n2. Response A",
            "parsed_ranking": ["Response B", "Response A"],
        },
    ],
    "stage3": {"model": "vendor-b/beta", "response": "the chairman synthesis"},
    "metadata": {
        "label_to_model": {"Response A": "vendor-a/alpha", "Response B": "vendor-b/beta"},
        "aggregate_rankings": [
            {"model": "vendor-b/beta", "average_rank": 1.0, "rankings_count": 2},
            {"model": "vendor-a/alpha", "average_rank": 2.0, "rankings_count": 2},
        ],
    },
}


def council_mock(captured: list) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        if request.url.path == "/api/conversations":
            return httpx.Response(
                200,
                json={"id": "conv-1", "created_at": "", "title": "New Conversation", "messages": []},
            )
        if request.url.path == "/api/conversations/conv-1/message":
            return httpx.Response(200, json=COUNCIL_RESULT)
        return httpx.Response(404)

    return httpx.MockTransport(handler)


class BriefFraming(unittest.TestCase):
    def test_brief_carries_question_and_full_structure(self):
        brief = build_brief("Should I overweight semis?")
        self.assertIn("Question: Should I overweight semis?", brief)
        for section in ("Thesis", "Bull case", "Bear case", "Key risks", "change your mind", "Confidence"):
            self.assertIn(section, brief)
        self.assertIn("not financial advice", brief)
        self.assertNotIn("Context provided by the researcher", brief)

    def test_context_is_included_when_given(self):
        brief = build_brief("Q?", context="FY25 revenue grew 40%")
        self.assertIn("Context provided by the researcher:", brief)
        self.assertIn("FY25 revenue grew 40%", brief)


class CouncilClient(unittest.TestCase):
    def test_deliberate_sends_the_brief_and_returns_the_deliberation(self):
        captured = []
        result = asyncio.run(deliberate("the one brief", transport=council_mock(captured)))

        self.assertEqual(result, COUNCIL_RESULT)
        self.assertEqual(len(captured), 2)
        # The message request carries the brief verbatim as the query.
        body = json.loads(captured[1].content)
        self.assertEqual(body, {"content": "the one brief"})


class MemoRendering(unittest.TestCase):
    def test_memo_layout(self):
        when = datetime.datetime(2026, 8, 25, 14, 30)
        memo = render_memo("Should I overweight semis?", COUNCIL_RESULT, when)

        self.assertIn("# Investment memo: Should I overweight semis?", memo)
        self.assertIn("Not financial advice", memo)
        self.assertIn("the chairman synthesis", memo)
        # Standings sorted best-first with both members.
        self.assertIn("| 1 | vendor-b/beta | 1.0 | 2 |", memo)
        self.assertIn("| 2 | vendor-a/alpha | 2.0 | 2 |", memo)
        # Each member's analysis appears in the appendix.
        self.assertIn("alpha analysis", memo)
        self.assertIn("beta analysis", memo)
        # Synthesis comes before the appendix.
        self.assertLess(memo.index("Chairman's synthesis"), memo.index("Appendix"))

    def test_slugify(self):
        self.assertEqual(slugify("Should I overweight semis?!"), "should-i-overweight-semis")
        self.assertEqual(len(slugify("x" * 100)), 40)
        self.assertEqual(slugify("???"), "question")


class CliFlow(unittest.TestCase):
    def test_cli_writes_a_memo(self):
        with tempfile.TemporaryDirectory() as tmp:
            with contextlib.redirect_stdout(io.StringIO()) as out:
                code = main(
                    ["Should I overweight semis?", "--out-dir", tmp],
                    transport=council_mock([]),
                )

            self.assertEqual(code, 0)
            memos = list(Path(tmp).glob("*-should-i-overweight-semis.md"))
            self.assertEqual(len(memos), 1)
            self.assertIn("the chairman synthesis", memos[0].read_text())
            self.assertIn("Memo written to", out.getvalue())


if __name__ == "__main__":
    unittest.main()
