"""Build the Research Guide PDF from guide.html with headless Chrome.

Usage:  python build.py [--out PATH] [--chrome PATH]

Default output: out/Research_Guide.pdf next to this script (git-ignored).

Standard library only, plus pypdf (optional) to stamp the PDF Title/Author
metadata. Chrome runs with a throwaway profile directory, so it never touches
an existing browser session. All paths are relative to this file.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "out" / "Research_Guide.pdf"
METADATA = {
    "/Title": "Agentic Research Workflow: A Practical Guide",
    "/Author": "Simone Paci",
}
CHROME_CANDIDATES = [
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def find_chrome(explicit=None):
    for c in ([explicit] if explicit else []) + CHROME_CANDIDATES:
        p = shutil.which(c) or (c if Path(c).is_file() else None)
        if p:
            return p
    sys.exit("Chrome/Chromium not found; pass --chrome PATH")


def remove_profile(profile):
    # Chrome can hold profile files for a moment after exit; retry briefly.
    for _ in range(10):
        shutil.rmtree(profile, ignore_errors=True)
        if not Path(profile).exists():
            return
        time.sleep(0.5)
    print(f"warning: could not remove Chrome profile {profile}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--chrome")
    args = ap.parse_args()

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    src = (HERE / "guide.html").as_uri()
    chrome = find_chrome(args.chrome)

    # Fresh, private Chrome profile beside this script (git-ignored, removed afterwards).
    profile = tempfile.mkdtemp(prefix=".chrome-profile-", dir=HERE)
    raw = out.with_suffix(".chrome.pdf")
    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--no-first-run",
        "--no-default-browser-check", "--disable-extensions",
        f"--user-data-dir={profile}",
        "--no-pdf-header-footer", "--print-to-pdf-no-header",
        f"--print-to-pdf={raw}", src,
    ]
    try:
        subprocess.run(cmd, check=True, timeout=120,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        remove_profile(profile)
    if not raw.is_file():
        sys.exit("Chrome did not produce a PDF")

    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        os.replace(raw, out)
        print(f"wrote {out} (pypdf missing: Author metadata not set)")
        return
    writer = PdfWriter(clone_from=PdfReader(str(raw)))
    writer.add_metadata(METADATA)
    with open(out, "wb") as fh:
        writer.write(fh)
    raw.unlink()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
