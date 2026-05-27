#!/usr/bin/env python3
"""
generate_report_html.py
Converts the latest council_emails_*.docx into report.html for councildata.ai.

Usage:
    python3 scripts/generate_report_html.py /path/to/council_emails_MMYYYY.docx [--month "May 2026"] [--compiled "27 May 2026"]

If no docx path is given, auto-detects the newest council_emails_*.docx in ../
"""
import re, sys, glob, os
from pathlib import Path

try:
    import mammoth
except ImportError:
    sys.exit("mammoth not installed — run: pip install mammoth")

REPO_ROOT = Path(__file__).resolve().parents[1]
COUNCIL_WORK = REPO_ROOT.parent  # /home/azureuser/council-work


def find_latest_docx():
    candidates = sorted(glob.glob(str(COUNCIL_WORK / "council_emails_*.docx")))
    if not candidates:
        sys.exit(f"No council_emails_*.docx found in {COUNCIL_WORK}")
    return candidates[-1]


def convert(docx_path: str, month: str, compiled: str) -> str:
    with open(docx_path, "rb") as f:
        result = mammoth.convert_to_html(f)
    body = result.value

    # Promote numbered section headers:
    # <p><a id="section_N"></a><strong>N. Title</strong></p> → <h2>
    body = re.sub(
        r'<p>(<a id="section_\d+"></a>)<strong>(\d+\.\s+[^<]{3,120})</strong></p>',
        r'<h2>\1\2</h2>',
        body,
    )

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Central Coast Economic Data Updates \u2014 {month}</title>
  <style>
    :root {{
      --ink: #0e1a2b; --ink-soft: #3a4a5e; --paper: #f7f5ee;
      --accent: #1b3a5b; --highlight: #d4a017; --rule: #e5dfd0;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: var(--paper); color: var(--ink); line-height: 1.65;
      margin: 0; padding: 0; -webkit-font-smoothing: antialiased;
    }}
    header {{
      background: var(--accent); color: white; padding: 1rem 2rem;
      display: flex; align-items: center; justify-content: space-between;
    }}
    header .brand {{ font-weight: 700; font-size: 1.05rem; letter-spacing: -0.01em; }}
    header .brand .dot {{ color: var(--highlight); }}
    header a {{ color: rgba(255,255,255,0.75); font-size: 0.88rem; text-decoration: none; }}
    header a:hover {{ color: white; }}
    .doc-header {{
      max-width: 860px; margin: 2.5rem auto 0; padding: 0 1.5rem 1.25rem;
      border-bottom: 2px solid var(--accent);
    }}
    .doc-header h1 {{
      font-size: 1.7rem; font-weight: 800; color: var(--accent);
      margin: 0 0 0.25rem; letter-spacing: -0.02em;
    }}
    .doc-header .meta {{ font-size: 0.85rem; color: var(--ink-soft); }}
    .content {{ max-width: 860px; margin: 0 auto; padding: 1.5rem 1.5rem 4rem; }}
    h2 {{
      font-size: 1.1rem; font-weight: 700; color: white;
      margin: 2.5rem 0 0.75rem; padding: 0.65rem 1rem;
      background: var(--accent); border-radius: 6px;
    }}
    h2 a {{ color: inherit; text-decoration: none; }}
    p {{ margin: 0.55rem 0; font-size: 0.95rem; }}
    strong {{ color: var(--ink); }}
    a {{ color: var(--accent); }}
    a:hover {{ color: #284e75; }}
    img {{ max-width: 100%; height: auto; border-radius: 6px; margin: 0.75rem 0; border: 1px solid var(--rule); display: block; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.88rem; }}
    th {{ background: var(--accent); color: white; padding: 7px 10px; text-align: left; font-weight: 600; }}
    td {{ padding: 6px 10px; border-bottom: 1px solid var(--rule); }}
    tr:hover td {{ background: white; }}
    ul, ol {{ margin: 0.5rem 0 0.5rem 1.25rem; }}
    li {{ margin-bottom: 0.3rem; font-size: 0.95rem; }}
    footer {{
      border-top: 1px solid var(--rule); padding: 1.5rem;
      text-align: center; color: var(--ink-soft); font-size: 0.82rem;
    }}
    @media (max-width: 600px) {{
      .doc-header h1 {{ font-size: 1.3rem; }}
      .content {{ padding: 1rem 1rem 3rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="brand">councildata<span class="dot">.</span>ai</div>
    <a href="/">&#8592; Back to tools</a>
  </header>
  <div class="doc-header">
    <h1>Central Coast Economic Data Updates</h1>
    <div class="meta">{month} &nbsp;&middot;&nbsp; Compiled {compiled} &nbsp;&middot;&nbsp; Central Coast Council, NSW</div>
  </div>
  <div class="content">
    {body}
  </div>
  <footer>CouncilData.ai &middot; A <a href="https://seechange.com.au">See-Change</a> initiative &middot; Data sourced from Council economic updates</footer>
</body>
</html>"""


def main():
    args = sys.argv[1:]
    docx_path = None
    month = None
    compiled = None

    i = 0
    while i < len(args):
        if args[i] == "--month" and i + 1 < len(args):
            month = args[i + 1]; i += 2
        elif args[i] == "--compiled" and i + 1 < len(args):
            compiled = args[i + 1]; i += 2
        else:
            docx_path = args[i]; i += 1

    if not docx_path:
        docx_path = find_latest_docx()
        print(f"Auto-detected: {docx_path}")

    if not month:
        # Guess from filename e.g. council_emails_may2026.docx
        name = Path(docx_path).stem  # council_emails_may2026
        parts = name.replace("council_emails_", "").split("_")
        month = parts[0].capitalize() + " " + parts[1] if len(parts) >= 2 else "Latest"

    if not compiled:
        from datetime import date
        compiled = date.today().strftime("%-d %B %Y")

    print(f"Converting {docx_path}")
    print(f"Month: {month} | Compiled: {compiled}")

    html = convert(docx_path, month, compiled)
    out = REPO_ROOT / "report.html"
    out.write_text(html, encoding="utf-8")
    size_mb = len(html.encode("utf-8")) / 1024 / 1024
    print(f"Written: {out} ({size_mb:.1f} MB)")
    print()
    print("Next steps:")
    print(f"  cd {REPO_ROOT}")
    print("  git add report.html")
    print(f'  git commit -m "report: update to {month}"')
    print("  git push origin main")


if __name__ == "__main__":
    main()
