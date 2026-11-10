#!/usr/bin/env python3
"""
Render a cover letter (resumes/<slug>/cover_letter.md) to a one-page,
text-based PDF in letter layout: name and contact header, date, recipient
block, salutation, paragraphs, sign-off, optional signature image, typed name.

The Markdown layout it expects is documented in
.claude/skills/write-cover-letter/reference/cover-letter-principles.md
("Layout of cover_letter.md"): blocks separated by one blank line, starting
with a two-line name/contact header.

Usage:
  python3 scripts/render_cover_letter.py resumes/<slug>/cover_letter.md
      [-o out.pdf] [--paper letter|a4] [--signature signature.png]

Defaults: writes cover_letter.pdf next to the input, on Letter paper. Use
--paper a4 for UK letters. The signature image is optional and is never
copied into the repo; the PDF embeds it. Prints the page count; exits 1 on
failure.

Requires a Chromium/Chrome binary, found the same way as
render_resume_pdf.py ($CHROMIUM, /opt/pw-browsers/chromium, PATH, macOS).
"""
import argparse
import base64
import html
import mimetypes
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_resume_pdf import find_chromium, page_count  # noqa: E402

SIGN_OFF_RE = re.compile(
    r"^(sincerely|yours sincerely|yours faithfully|yours truly|best regards|"
    r"kind regards|regards|best wishes|with thanks|thank you),?$", re.I)

CSS = """
@page { size: %(paper)s; margin: 0.6in 0.7in; }
body { font-family: "Liberation Sans", Arial, Helvetica, sans-serif;
       font-size: 10pt; line-height: 1.38; color: #111; margin: 0; }
p { margin: 0 0 9pt; }
.name { font-size: 17pt; font-weight: bold; margin: 0 0 3pt; }
.contact { font-size: 8.5pt; color: #444; border-bottom: 1px solid #999;
           padding-bottom: 8pt; margin-bottom: 14pt; }
.block { margin-bottom: 12pt; }
.signoff { margin-bottom: 0; }
.signature { height: 34pt; display: block; margin: 2pt 0 2pt -3pt; }
.typed { margin-top: %(typed_gap)s; }
"""


class LetterError(ValueError):
    pass


def parse_letter(md: str) -> dict:
    """Split a cover_letter.md into its parts. Raises LetterError if the
    layout doesn't match the one the principles file documents."""
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]
    if len(blocks) < 5:
        raise LetterError("Too few blocks: expected header, date, salutation, "
                          "paragraphs, sign-off and name.")
    header = blocks[0].split("\n")
    if len(header) != 2:
        raise LetterError("The first block must be exactly two lines: the name, "
                          "then the contact line.")
    sal_i = next((i for i, b in enumerate(blocks) if b.startswith("Dear ")), None)
    if sal_i is None or sal_i < 2:
        raise LetterError('No salutation ("Dear ...") after the date.')
    off_i = next((i for i in range(sal_i + 1, len(blocks))
                  if SIGN_OFF_RE.match(blocks[i].strip())), None)
    if off_i is None:
        raise LetterError('No sign-off line (e.g. "Sincerely," or "Yours sincerely,").')
    if off_i != len(blocks) - 2:
        raise LetterError("Expected exactly one block, the typed name, after the sign-off.")
    paragraphs = [" ".join(b.split()) for b in blocks[sal_i + 1:off_i]]
    if not paragraphs:
        raise LetterError("No paragraphs between the salutation and the sign-off.")
    return {
        "name": header[0].strip(),
        "contact": header[1].strip(),
        "date": blocks[1].strip(),
        "recipient": [l.strip() for l in "\n".join(blocks[2:sal_i]).split("\n") if l.strip()],
        "salutation": blocks[sal_i].strip(),
        "paragraphs": paragraphs,
        "sign_off": blocks[off_i].strip(),
        "typed_name": blocks[-1].strip(),
    }


def build_html(letter: dict, paper: str = "letter", signature: Path = None) -> str:
    e = html.escape
    sig = ""
    if signature:
        mime = mimetypes.guess_type(signature.name)[0] or "image/png"
        data = base64.b64encode(signature.read_bytes()).decode()
        sig = f'<img class="signature" alt="" src="data:{mime};base64,{data}">'
    css = CSS % {"paper": "A4" if paper == "a4" else "Letter",
                 "typed_gap": "0" if signature else "28pt"}
    recipient = (f'<p class="block">{"<br>".join(e(l) for l in letter["recipient"])}</p>'
                 if letter["recipient"] else "")
    paras = "".join(f"<p>{e(p)}</p>" for p in letter["paragraphs"])
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<title>Cover Letter</title><style>{css}</style></head><body>'
            f'<p class="name">{e(letter["name"])}</p>'
            f'<p class="contact">{e(letter["contact"])}</p>'
            f'<p class="block">{e(letter["date"])}</p>{recipient}'
            f'<p>{e(letter["salutation"])}</p>{paras}'
            f'<p class="signoff">{e(letter["sign_off"])}</p>{sig}'
            f'<p class="typed">{e(letter["typed_name"])}</p></body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("letter_md")
    ap.add_argument("-o", "--output")
    ap.add_argument("--paper", choices=["letter", "a4"], default="letter")
    ap.add_argument("--signature", help="optional signature image (PNG or JPEG)")
    a = ap.parse_args()
    src = Path(a.letter_md)
    out = Path(a.output) if a.output else src.with_suffix(".pdf")
    sig = Path(a.signature) if a.signature else None
    if sig and not sig.is_file():
        sys.exit(f"Signature image not found: {sig}")
    try:
        letter = parse_letter(src.read_text())
    except LetterError as err:
        sys.exit(f"{src}: {err}")
    with tempfile.TemporaryDirectory() as td:
        page = Path(td) / "letter.html"
        page.write_text(build_html(letter, a.paper, sig))
        subprocess.run([find_chromium(), "--headless", "--no-sandbox",
                        "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out.resolve()}", page.resolve().as_uri()],
                       check=True, capture_output=True)
    if not out.exists():
        sys.exit("PDF was not produced.")
    pages = page_count(out)
    print(f"Wrote {out} ({pages} page(s))")
    if pages != 1:
        print("A cover letter should fit on one page: cut words, not the font size.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
