#!/usr/bin/env python3
"""
Render a tailored resume/CV Markdown file (resumes/<slug>/resume.md) to PDF.

Pipeline: light Markdown preprocessing -> pandoc (HTML5, embedded CSS) ->
headless Chromium "print to PDF". Output is text-based (selectable, ATS-
parseable), single column, using .claude/skills/render-resume-pdf/resume.css.

Usage:
  python3 scripts/render_resume_pdf.py resumes/<slug>/resume.md [-o out.pdf]
      [--paper letter|a4] [--font-size PT] [--title TITLE]

Defaults: writes resume.pdf next to the input; Letter paper (US); the
stylesheet's body font size; PDF title "Resume". Use --paper a4 for UK CVs,
and --font-size / --title where a market's spec sets a minimum body size or
calls the document a CV. Prints the page count; exits 1 on failure.

Requires: pandoc, and a Chromium/Chrome binary (found via $CHROMIUM, then
/opt/pw-browsers/chromium, then chromium/chromium-browser/google-chrome on
PATH, then Google Chrome's default macOS install).
"""
import argparse, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / ".claude/skills/render-resume-pdf/resume.css"


def find_chromium():
    cands = [os.environ.get("CHROMIUM"), "/opt/pw-browsers/chromium",
             shutil.which("chromium"), shutil.which("chromium-browser"),
             shutil.which("google-chrome"),
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    for c in cands:
        if c and os.path.exists(c):
            return c
    sys.exit("No Chromium/Chrome binary found; set $CHROMIUM.")


def preprocess(md: str) -> str:
    lines = md.split("\n")
    out = []
    # The resume format starts with a name line and a contact line (plain
    # text); give them classes so they render as a header, not one paragraph.
    if len(lines) >= 2 and not lines[0].startswith("#"):
        out.append(f'<p class="name">{lines[0].strip()}</p>')
        out.append(f'<p class="contact">{lines[1].strip()}</p>')
        out.append("")
        lines = lines[2:]
    for line in lines:
        # pandoc needs a blank line before a list that follows a text line
        # (e.g. a "**Title** | dates" line directly above its bullets).
        if line.startswith("- ") and out and out[-1].strip() and not out[-1].startswith("- "):
            out.append("")
        out.append(line)
    return "\n".join(out)


def page_count(pdf: Path):
    if shutil.which("pdfinfo"):
        r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
        m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
        if m:
            return int(m.group(1))
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume_md")
    ap.add_argument("-o", "--output")
    ap.add_argument("--paper", choices=["letter", "a4"], default="letter")
    ap.add_argument("--font-size", type=float,
                    help="body font size in pt (default: the stylesheet's)")
    ap.add_argument("--title", default="Resume",
                    help='PDF metadata title (default: "Resume")')
    a = ap.parse_args()
    src = Path(a.resume_md)
    out = Path(a.output) if a.output else src.with_suffix(".pdf")
    if not shutil.which("pandoc"):
        sys.exit("pandoc not found.")
    css = CSS.read_text()
    if a.paper == "a4":
        css = css.replace("size: Letter", "size: A4")
    if a.font_size:
        css, n = re.subn(r"(body \{[^}]*font-size: )[\d.]+pt", rf"\g<1>{a.font_size:g}pt", css)
        if n != 1:
            sys.exit("Couldn't find the body font size in resume.css.")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "in.md").write_text(preprocess(src.read_text()))
        (td / "resume.css").write_text(css)
        subprocess.run(["pandoc", str(td / "in.md"), "-f", "markdown-smart",
                        "-t", "html5", "-s", "--metadata", f"pagetitle={a.title}",
                        "--css", str(td / "resume.css"), "--embed-resources",
                        "-o", str(td / "resume.html")], check=True)
        subprocess.run([find_chromium(), "--headless", "--no-sandbox",
                        "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out.resolve()}",
                        (td / "resume.html").resolve().as_uri()],
                       check=True, capture_output=True)
    if not out.exists():
        sys.exit("PDF was not produced.")
    print(f"Wrote {out} ({page_count(out)} page(s))")


if __name__ == "__main__":
    main()
