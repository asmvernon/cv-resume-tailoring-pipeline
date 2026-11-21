"""Tests for scripts/check_fit_profile.py. Run: python3 -m unittest discover -s tests"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

import yaml

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import check_fit_profile  # noqa: E402

EXAMPLE = os.path.join(HERE, "..", ".claude", "skills", "assess-job-fit",
                       "reference", "example-fit-profile.yaml")


def load_example():
    with open(EXAMPLE) as fh:
        return yaml.safe_load(fh)


class CheckFitProfileTest(unittest.TestCase):
    def test_example_is_valid(self):
        self.assertEqual(check_fit_profile.check(load_example()), [])

    def test_empty_profile_is_valid(self):
        self.assertEqual(check_fit_profile.check({}), [])

    def test_not_a_mapping(self):
        self.assertTrue(check_fit_profile.check(["a"]))

    def test_unknown_field(self):
        problems = check_fit_profile.check({"wieghts": {}})
        self.assertIn("unknown field 'wieghts'", problems)

    def test_weights_must_sum_to_one(self):
        problems = check_fit_profile.check({"weights": {"experience": 0.5, "company": 0.3}})
        self.assertTrue(any("add up to 0.8" in p for p in problems))

    def test_weight_out_of_range(self):
        problems = check_fit_profile.check({"weights": {"experience": 2, "company": -1}})
        self.assertTrue(any("weights.experience" in p for p in problems))

    def test_ratings_order_and_floor(self):
        problems = check_fit_profile.check(
            {"ratings": [{"min": 3, "label": "Good"}, {"min": 4, "label": "Strong"}]})
        self.assertTrue(any("highest min first" in p for p in problems))
        self.assertTrue(any("min 0" in p for p in problems))

    def test_rating_needs_label(self):
        problems = check_fit_profile.check({"ratings": [{"min": 0}]})
        self.assertTrue(any("ratings[0]" in p for p in problems))

    def test_work_authorisation_values(self):
        problems = check_fit_profile.check({"work_authorisation": {"US": "yes"}})
        self.assertTrue(any("work_authorisation.US" in p for p in problems))

    def test_adjustment_needs_why(self):
        problems = check_fit_profile.check(
            {"locations": {"adjustments": [{"match": "LA", "delta": -0.5}]}})
        self.assertTrue(any("adjustments[0]" in p for p in problems))

    def test_lists_of_text(self):
        problems = check_fit_profile.check(
            {"levels": {"best": "EM"}, "deal_breakers": "onsite"})
        self.assertTrue(any("levels.best" in p for p in problems))
        self.assertTrue(any("deal_breakers" in p for p in problems))

    def test_missing_file_is_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = check_fit_profile.main(["x", os.path.join(tmp, "none.yaml")])
            self.assertEqual(code, 0)
            self.assertIn("defaults", out.getvalue())

    def test_main_reports_problems(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "fit_profile.yaml")
            with open(path, "w") as fh:
                fh.write("weights: {experience: 0.9}\n")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = check_fit_profile.main(["x", path])
            self.assertEqual(code, 1)
            self.assertIn("add up to", out.getvalue())


if __name__ == "__main__":
    unittest.main()
