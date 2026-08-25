"""Pins the mechanics that make the 3-stage council (the "conductor" idea) work.

If a future change breaks one of these, the council quietly degrades into a
single-model app:
  - Stage 1: every member answers the bare query independently (no cross-talk).
  - Stage 2: reviewers see anonymized labels, never model identities.
  - Stage 3: the Chairman synthesizes from council material, not from scratch.

All model calls are stubbed; no network. Run from the project root:
    uv run python -m unittest discover -s tests -v
"""

import asyncio
import unittest
from unittest.mock import patch

from backend import council
from backend.config import COUNCIL_MODELS, CHAIRMAN_MODEL

FAKE_STAGE1 = [
    {"model": model, "response": f"stage1 answer #{i}"}
    for i, model in enumerate(COUNCIL_MODELS)
]


class Stage1Independence(unittest.TestCase):
    def test_every_member_gets_the_bare_query_only(self):
        captured = {}

        async def fake_parallel(models, messages):
            captured["models"] = models
            captured["messages"] = messages
            return {m: {"content": f"answer from {m}"} for m in models}

        with patch.object(council, "query_models_parallel", fake_parallel):
            results = asyncio.run(council.stage1_collect_responses("What is X?"))

        self.assertEqual(captured["models"], COUNCIL_MODELS)
        # The only content sent is the user's query itself: no other member's
        # output, no steering context.
        self.assertEqual(
            captured["messages"], [{"role": "user", "content": "What is X?"}]
        )
        self.assertEqual({r["model"] for r in results}, set(COUNCIL_MODELS))


class Stage2Anonymization(unittest.TestCase):
    def test_review_prompt_hides_model_identities(self):
        captured = {}

        async def fake_parallel(models, messages):
            captured["models"] = models
            captured["messages"] = messages
            return {m: {"content": "FINAL RANKING:\n1. Response A"} for m in models}

        with patch.object(council, "query_models_parallel", fake_parallel):
            rankings, label_to_model = asyncio.run(
                council.stage2_collect_rankings("What is X?", FAKE_STAGE1)
            )

        prompt = captured["messages"][0]["content"]
        for i, entry in enumerate(FAKE_STAGE1):
            self.assertNotIn(entry["model"], prompt)  # identities never leak
            self.assertIn(entry["response"], prompt)  # but every answer is reviewed
            self.assertIn(f"Response {chr(65 + i)}", prompt)
        # The mapping used for client-side display de-anonymizes correctly.
        self.assertEqual(
            label_to_model,
            {
                f"Response {chr(65 + i)}": entry["model"]
                for i, entry in enumerate(FAKE_STAGE1)
            },
        )
        # The reviewers are the council members themselves.
        self.assertEqual(captured["models"], COUNCIL_MODELS)
        self.assertEqual(len(rankings), len(COUNCIL_MODELS))


class Stage3Synthesis(unittest.TestCase):
    def test_chairman_synthesizes_from_all_council_material(self):
        stage2 = [
            {
                "model": model,
                "ranking": f"evaluation by seat {i}\nFINAL RANKING:\n1. Response A",
                "parsed_ranking": ["Response A"],
            }
            for i, model in enumerate(COUNCIL_MODELS)
        ]
        captured = {}

        async def fake_query(model, messages, timeout=120.0):
            captured["model"] = model
            captured["messages"] = messages
            return {"content": "the synthesis"}

        with patch.object(council, "query_model", fake_query):
            result = asyncio.run(
                council.stage3_synthesize_final("What is X?", FAKE_STAGE1, stage2)
            )

        self.assertEqual(captured["model"], CHAIRMAN_MODEL)
        prompt = captured["messages"][0]["content"]
        # The chairman is grounded in every response and every peer ranking.
        for entry in FAKE_STAGE1:
            self.assertIn(entry["response"], prompt)
        for entry in stage2:
            self.assertIn(entry["ranking"], prompt)
        self.assertEqual(result, {"model": CHAIRMAN_MODEL, "response": "the synthesis"})


class RankingParsing(unittest.TestCase):
    def test_numbered_final_ranking(self):
        text = (
            "Response A is thorough...\nResponse B is shallow...\n\n"
            "FINAL RANKING:\n1. Response B\n2. Response A\n3. Response C\n"
        )
        self.assertEqual(
            council.parse_ranking_from_text(text),
            ["Response B", "Response A", "Response C"],
        )

    def test_fallback_without_header(self):
        text = "I prefer Response C, then Response A."
        self.assertEqual(
            council.parse_ranking_from_text(text), ["Response C", "Response A"]
        )


class AggregateRankings(unittest.TestCase):
    def test_average_positions_sorted_best_first(self):
        label_to_model = {"Response A": "vendor/alpha", "Response B": "vendor/beta"}
        stage2 = [
            {"model": "vendor/alpha", "ranking": "FINAL RANKING:\n1. Response A\n2. Response B"},
            {"model": "vendor/beta", "ranking": "FINAL RANKING:\n1. Response B\n2. Response A"},
            {"model": "vendor/gamma", "ranking": "FINAL RANKING:\n1. Response A\n2. Response B"},
        ]
        aggregate = council.calculate_aggregate_rankings(stage2, label_to_model)
        self.assertEqual(
            aggregate,
            [
                {"model": "vendor/alpha", "average_rank": 1.33, "rankings_count": 3},
                {"model": "vendor/beta", "average_rank": 1.67, "rankings_count": 3},
            ],
        )


if __name__ == "__main__":
    unittest.main()
