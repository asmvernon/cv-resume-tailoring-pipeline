"""Tests for scripts/render_cover_letter.py's parsing and HTML building (no
browser needed). Run: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import render_cover_letter as rcl  # noqa: E402

LETTER = """Jane Doe
City, ST | (555) 010-0000 | jane@example.com

November 10, 2026

Hiring Team
Example Bio
South San Francisco, CA

Dear Example Bio Hiring Team,

First paragraph,
wrapped over two lines.

Second paragraph.

Sincerely,

Jane Doe
"""


class ParseTest(unittest.TestCase):
    def test_parses_all_parts(self):
        p = rcl.parse_letter(LETTER)
        self.assertEqual(p["name"], "Jane Doe")
        self.assertEqual(p["date"], "November 10, 2026")
        self.assertEqual(p["recipient"], ["Hiring Team", "Example Bio", "South San Francisco, CA"])
        self.assertEqual(p["salutation"], "Dear Example Bio Hiring Team,")
        self.assertEqual(p["paragraphs"], ["First paragraph, wrapped over two lines.",
                                           "Second paragraph."])
        self.assertEqual(p["sign_off"], "Sincerely,")
        self.assertEqual(p["typed_name"], "Jane Doe")

    def test_recipient_is_optional(self):
        p = rcl.parse_letter(LETTER.replace("Hiring Team\nExample Bio\nSouth San Francisco, CA\n\n", ""))
        self.assertEqual(p["recipient"], [])

    def test_uk_sign_off(self):
        p = rcl.parse_letter(LETTER.replace("Sincerely,", "Yours faithfully,"))
        self.assertEqual(p["sign_off"], "Yours faithfully,")

    def test_one_line_header_is_rejected(self):
        bad = LETTER.replace("Jane Doe\nCity", "Jane Doe City", 1)
        with self.assertRaises(rcl.LetterError):
            rcl.parse_letter(bad)

    def test_missing_salutation_is_rejected(self):
        with self.assertRaises(rcl.LetterError):
            rcl.parse_letter(LETTER.replace("Dear ", "Hello "))

    def test_missing_sign_off_is_rejected(self):
        with self.assertRaises(rcl.LetterError):
            rcl.parse_letter(LETTER.replace("Sincerely,", "Cheers"))


class HtmlTest(unittest.TestCase):
    def test_escapes_and_sets_paper(self):
        p = rcl.parse_letter(LETTER.replace("Second paragraph.", "R&D <teams>."))
        page = rcl.build_html(p, paper="a4")
        self.assertIn("R&amp;D &lt;teams&gt;.", page)
        self.assertIn("size: A4", page)
        self.assertNotIn("<img", page)


if __name__ == "__main__":
    unittest.main()
