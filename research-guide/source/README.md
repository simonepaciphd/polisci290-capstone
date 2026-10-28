# Research Guide — PDF source

HTML/CSS source for `../Agentic_Research_Workflow_Research_Guide.pdf`
("Agentic Research Workflow: A Practical Guide"). `guide.html` holds the
content, `guide.css` the print layout (US Letter, 8 pages), and `build.py`
prints it to PDF with headless Chrome and stamps the Title/Author metadata.

## Build

```
python build.py
```

Writes `out/Research_Guide.pdf` (git-ignored). Options: `--out PATH`,
`--chrome PATH`. Needs Chrome/Chromium (or Edge); `pypdf` is optional and only
used to set the metadata. Chrome runs with a throwaway profile
(`.chrome-profile-*/`, git-ignored) that is deleted after the build.

To publish, review the built PDF and copy it over
`../Agentic_Research_Workflow_Research_Guide.pdf` by hand.

## Page breaks

Page breaks are forced with `class="pb"` elements in `guide.html`, placed to
reproduce the original 8-page layout. They do not reflow: after any content
edit, re-check every page and move, add or remove `pb` breaks as needed.

## Fonts and licence

`fonts/FreeSans.ttf` and `fonts/FreeSansBold.ttf` are from GNU FreeFont
release 20120503 (https://ftp.gnu.org/gnu/freefont/freefont-ttf-20120503.zip),
licensed under the GNU GPL v3 or later with the font exception: embedding the
font in a document does not by itself put the document under the GPL. See
`fonts/COPYING` (GPL text), `fonts/README` (licence summary and font
exception) and `fonts/AUTHORS`.
