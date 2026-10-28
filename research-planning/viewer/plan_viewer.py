"""Build one Plan-Visual.html page from your planning files (student edition).

Usage, from your project folder:
    python research-planning/viewer/plan_viewer.py docs/planning
    python research-planning/viewer/plan_viewer.py docs/planning --check
    python research-planning/viewer/plan_viewer.py docs/planning -o other.html --built YYYY-MM-DD

Reads SPEC.md, RESOURCES.md and PLAN.md (written from the templates in
research-planning/templates/), checks that they fit together, and writes
docs/planning/Plan-Visual.html: one page that opens in any browser, with no
internet needed. It never changes the planning files. --check only lists
problems and writes nothing.

Exit 0 = no errors (warnings allowed); 1 = errors (all listed, nothing
written); 2 = usage or file error. Python 3.8+, standard library only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

TOOL = "plan-viewer (student edition)"
VERSION = "1.0.0"
TEMPLATE = Path(__file__).with_name("template.html")
MARKER = "/*__PLAN_DATA__*/null"
OUT_NAME = "Plan-Visual.html"

SPEC, RES, PLAN = "SPEC.md", "RESOURCES.md", "PLAN.md"
LABELS = "Plan-Labels.json"  # optional: {"labels": {"T-01": {"label": "...", "plain": "..."}}}
SOURCES = (SPEC, RES, PLAN)

ID = {
    "deliverable": re.compile(r"OUT-\d+"),
    "resource": re.compile(r"RES-\d+"),
    "task": re.compile(r"T-\d+"),
}
FIND = {k: re.compile(r"\b" + p.pattern + r"\b") for k, p in ID.items()}
NONE_VALUES = {"", "none", "n/a", "\u2014", "-", "nothing"}

# Task status -> (shown as, colour). Order here is the order on the page.
STATUSES = {
    "done": ("Done", "o2"),
    "ready for your check": ("Ready for your check", "o4"),
    "waiting for you": ("Waiting for you", "accent"),
    "working": ("Working", "o1"),
    "planned": ("Planned", "o5"),
}
REMOVED = ("removed", "dropped", "retired")

# Field names accepted on a task card (lower case, without any "(...)" qualifier).
FIELDS = {
    "objective": "objective", "goal": "objective",
    "serves": "serves",
    "inputs": "inputs", "input": "inputs",
    "outputs": "outputs", "output": "outputs",
    "depends on": "depends", "depends": "depends", "dependencies": "depends",
    "requires": "depends", "waits on": "depends",
    "steps": "steps", "step": "steps", "action": "steps", "actions": "steps",
    "checks": "checks", "check": "checks", "verification": "checks",
    "student decisions": "decisions", "student decision": "decisions",
    "student decisions needed": "decisions", "student decision needed": "decisions",
    "decisions": "decisions", "decision": "decisions",
    "status": "status",
}

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
# A closing '#' run is stripped only after whitespace, so "Clean in C#" keeps its '#'.
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
# 'Status: x', '- Status: x', '**Status:** x' and '**Status**: x' all count.
HEADER_RE = re.compile(r"^(?:[-*+]\s+)?(?:\*\*)?([A-Za-z][A-Za-z0-9 _-]*?)\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*(.*?)\s*(?:\*\*)?\s*$")
SEP_RE = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$")
CARD_RE = re.compile(r"^(T-\d+)\s*(?::|\u2014|\u2013|-)\s*(.*)$")
FIELD_RE = re.compile(r"^(?:[-*+]\s+)?(?:\*\*)?([A-Za-z][A-Za-z ]*?)\s*(?:\(([^)]*)\))?\s*(?:\*\*)?\s*:\s*(?:\*\*)?\s*(.*)$")
BULLET_RE = re.compile(r"^([-*+]|\d+[.)])\s+(.*)$")
RANGE_RE = re.compile(r"\b(T-(\d+))\s*(?:to|through|\u2013|\u2014|-)\s*(T-(\d+))\b")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDER_RE = re.compile(r"^\[[^\]]*\]$")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


class Problem(NamedTuple):
    kind: str  # "ERROR" | "WARN"
    rule: str
    file: str
    line: int | None
    text: str

    def __str__(self):
        loc = self.file if self.line is None else f"{self.file}:{self.line}"
        return f"{self.kind} {self.rule}: {loc}: {self.text}"

    @property
    def is_error(self):
        return self.kind == "ERROR"


class FileProblem(Exception):
    """A planning file that cannot be read at all (exit 2)."""


def _err(rule, file, line, text):
    return Problem("ERROR", rule, file, line, text)


def _warn(rule, file, line, text):
    return Problem("WARN", rule, file, line, text)


def _blank(s) -> bool:
    """Empty, 'none', or an unfilled template placeholder like '[fill in]'."""
    s = (s or "").strip()
    return s.lower().rstrip(".") in NONE_VALUES or bool(PLACEHOLDER_RE.match(s))


def _task_ids(text: str, known) -> list[str]:
    """Task IDs named in text, in order, once each. 'T-01 to T-04' (also 'through', '-', en or em
    dash) means every known task numbered from one end to the other."""
    nums = {t: int(t[2:]) for t in known}
    ids, pos = [], 0
    for m in RANGE_RE.finditer(text):
        ids += FIND["task"].findall(text[pos:m.start()])
        lo, hi = sorted((int(m.group(2)), int(m.group(4))))
        ids += sorted((t for t in nums if lo <= nums[t] <= hi), key=lambda t: (nums[t], t))
        # An end with no task card is kept, so it is reported; 'T-1' still finds T-01.
        ids += [e for e in (m.group(1), m.group(3)) if int(e[2:]) not in nums.values()]
        pos = m.end()
    ids += FIND["task"].findall(text[pos:])
    return list(dict.fromkeys(ids))


def _file_status(doc, problems):
    """The file's 'Status:' line. 'LOCKED 2026-11-02' stays as is; the unfilled template line
    'DRAFT | APPROVED | ...' is shown as DRAFT, with a warning."""
    hdr = doc.header("status")
    if hdr is None:
        return None
    s = hdr[0].strip()
    if "|" in s:
        problems.append(_warn("W-STATUS-TEMPLATE", doc.name, hdr[1],
                              f"'Status: {s}' still lists the template choices; keep the one that applies (shown as DRAFT)"))
    return "DRAFT" if not s or "|" in s else s


# --------------------------------------------------------------------------- markdown

def _split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


class Doc:
    """Line view of one Markdown file. Fenced code and HTML comments are skipped."""

    def __init__(self, name: str, text: str):
        self.name = name
        # Blank out comments but keep line numbers.
        text = COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
        self.lines = text.splitlines()
        n = len(self.lines)
        self.skip = [False] * n
        i = 0
        while i < n:
            m = FENCE_RE.match(self.lines[i])
            if not m:
                i += 1
                continue
            mark, j = m.group(1), i + 1
            while j < n and not self.lines[j].strip().startswith(mark[0] * len(mark)):
                j += 1
            for k in range(i, min(j, n - 1) + 1):
                self.skip[k] = True
            i = j + 1
        self.headings = []  # (idx, level, text)
        for i, line in enumerate(self.lines):
            m = None if self.skip[i] else HEADING_RE.match(line)
            if m:
                self.headings.append((i, len(m.group(1)), m.group(2).strip()))

    def end(self, idx, level, hi=None):
        hi = len(self.lines) if hi is None else hi
        for h, lv, _ in self.headings:
            if idx < h < hi and lv <= level:
                return h
        return hi

    def title(self, prefix):
        for h, lv, text in self.headings:
            if lv == 1:
                m = re.match(rf"^{prefix}\s*:\s*(.*)$", text, re.I)
                name = (m.group(1) if m else text).strip()
                return "" if _blank(name) else name
        return ""

    def header(self, key):
        """Value of a 'Key: value' line before the first '## ' heading, else None."""
        stop = next((h for h, lv, _ in self.headings if lv >= 2), len(self.lines))
        for i in range(stop):
            m = None if self.skip[i] else HEADER_RE.match(self.lines[i])
            if m and m.group(1).strip().lower() == key:
                return m.group(2), i + 1
        return None

    def section(self, name, prefix=False):
        want = name.lower()
        for h, lv, text in self.headings:
            t = text.lower()
            if lv == 2 and (t.startswith(want) if prefix else t == want):
                return h, h + 1, self.end(h, 2)
        return None

    def table(self, lo, hi):
        """First pipe table in lines [lo, hi): (header line, header cells, [(line, cells)]) or None."""
        for i in range(lo, hi):
            if self.skip[i] or not self.lines[i].lstrip().startswith("|"):
                continue
            if i + 1 >= hi or not SEP_RE.match(self.lines[i + 1].strip()):
                return None
            rows, j = [], i + 2
            while j < hi and not self.skip[j] and self.lines[j].lstrip().startswith("|"):
                rows.append((j + 1, _split_row(self.lines[j])))
                j += 1
            return i + 1, _split_row(self.lines[i]), rows
        return None

    def prose(self, lo, hi):
        out = [self.lines[i].strip() for i in range(lo, hi)
               if not self.skip[i] and self.lines[i].strip() and not _blank(self.lines[i])]
        return " ".join(out)


def _read_table(doc, section, problems, prefix=False, required=True):
    """Rows of the first table in a section as dicts keyed by lower-case column name."""
    sec = doc.section(section, prefix)
    if sec is None:
        if required:
            problems.append(_err("E-STRUCTURE", doc.name, None, f"missing section '## {section}'"))
        return None, None
    tbl = doc.table(sec[1], sec[2])
    if tbl is None:
        if required:
            problems.append(_err("E-STRUCTURE", doc.name, sec[0] + 1,
                                 f"'## {section}' has no table (a header row, then a |---| row)"))
        return None, None
    line, header, rows = tbl
    cols = [h.strip().lower() for h in header]
    out = []
    for ln, cells in rows:
        if any(c.strip() for c in cells[len(cols):]):
            problems.append(_warn("W-EXTRA-CELLS", doc.name, ln,
                                  f"row has {len(cells)} cells but '## {section}' has {len(cols)} columns; "
                                  f"the extra cells are not read (a '|' inside a cell must be written '\\|')"))
        cells = (cells + [""] * len(cols))[:len(cols)]
        if all(_blank(c) for c in cells):
            continue
        rec = {"_line": ln}
        for c, v in zip(cols, cells):
            rec.setdefault(c, v)
        out.append(rec)
    return out, (line, header)


# --------------------------------------------------------------------------- parse

def _parse_spec(doc, problems):
    spec = {"name": doc.title("SPEC"), "status": None, "goal": "", "deliverables": [], "ok": False}
    spec["status"] = _file_status(doc, problems)
    sec = doc.section("research question", prefix=True)
    if sec:
        spec["goal"] = doc.prose(sec[1], sec[2])
    rows, tbl = _read_table(doc, "Deliverables", problems)
    if rows is None:
        return spec
    cols = [h.strip() for h in tbl[1]]
    if "id" not in [c.lower() for c in cols]:
        problems.append(_err("E-STRUCTURE", doc.name, tbl[0], "'## Deliverables' table has no 'ID' column"))
        return spec
    spec["ok"] = True
    seen = set()
    shown = {"id", "short name", "what it shows", "resources"}
    for r in rows:
        did = r["id"].strip()
        if _blank(did):
            continue
        if not ID["deliverable"].fullmatch(did):
            problems.append(_err("E-STRUCTURE", doc.name, r["_line"], f"deliverable ID '{did}' should look like OUT-01"))
            continue
        if did in seen:
            problems.append(_err("E-STRUCTURE", doc.name, r["_line"], f"deliverable {did} is listed twice"))
            continue
        seen.add(did)
        name = r.get("short name", "")
        name = did if _blank(name) else name
        shows = r.get("what it shows", "")
        req = "\n".join(f"**{c}:** {r[c.lower()]}" for c in cols
                        if c.lower() not in shown and not _blank(r.get(c.lower(), "")))
        spec["deliverables"].append({"id": did, "name": name, "label": shows if not _blank(shows) else name,
                                     "req": req, "line": r["_line"]})
    return spec


def _parse_resources(doc, problems):
    res = {"items": [], "ok": False}
    rows, tbl = _read_table(doc, "Resources", problems)
    if rows is None:
        return res
    if "id" not in [h.strip().lower() for h in tbl[1]]:
        problems.append(_err("E-STRUCTURE", doc.name, tbl[0], "'## Resources' table has no 'ID' column"))
        return res
    res["ok"] = True
    seen = set()
    for r in rows:
        rid = r["id"].strip()
        if _blank(rid):
            continue
        if not ID["resource"].fullmatch(rid):
            problems.append(_err("E-STRUCTURE", doc.name, r["_line"], f"resource ID '{rid}' should look like RES-01"))
            continue
        if rid in seen:
            problems.append(_err("E-STRUCTURE", doc.name, r["_line"], f"resource {rid} is listed twice"))
            continue
        seen.add(rid)
        what, loc = r.get("what it is", ""), r.get("location", "")
        what, loc = ("" if _blank(what) else what), ("" if _blank(loc) else loc)
        res["items"].append({"id": rid, "label": what or loc or rid, "desc": loc, "line": r["_line"]})
    return res


def _parse_card(doc, h, lo, hi, tid, name):
    """Fields of one task card. Accepts '- Field: value' bullets or plain 'Field: value' lines;
    indented or unrecognised lines continue the field above; a blank line ends it."""
    card = {"id": tid, "name": name, "line": h + 1, "fields": {}, "checks": []}
    cur = None
    for i in range(lo, hi):
        if doc.skip[i]:
            continue
        raw = doc.lines[i]
        if not raw.strip():
            cur = None
            continue
        indented = raw[:1].isspace()
        m = None if indented else FIELD_RE.match(raw.strip())
        key = FIELDS.get(m.group(1).strip().lower()) if m else None
        if key:
            qual = (m.group(2) or "").strip()
            cur = {"qual": qual, "lines": [m.group(3).strip()] if m.group(3).strip() else [], "line": i + 1}
            if key == "checks":
                card["checks"].append(cur)
            else:
                card["fields"].setdefault(key, cur)
        elif cur is not None:
            cur["lines"].append(raw.strip())
    return card


def _field_text(card, key, sep=" "):
    f = card["fields"].get(key)
    return sep.join(f["lines"]).strip() if f else ""


def _check_items(card):
    out = []
    for f in card["checks"]:
        lines = [ln for ln in f["lines"] if ln]
        if _blank(" ".join(lines)):
            continue
        if any(BULLET_RE.match(ln) for ln in lines):
            items = []
            for ln in lines:
                m = BULLET_RE.match(ln)
                if m:
                    items.append(m.group(2))
                elif items:
                    items[-1] += " " + ln
                else:
                    items.append(ln)
        else:
            items = re.split(r"\s*;\s*", " ".join(lines))
        items = [s.strip().rstrip(".").strip() for s in items]
        items = [s for s in items if not _blank(s)]
        q = f["qual"]
        out += [f"{q[:1].upper() + q[1:]}: {s}" if q else s for s in items]
    return out


def _parse_plan(doc, problems):
    plan = {"name": doc.title("PLAN"), "status": None, "deadline": None,
            "groups": None, "cards": {}, "order": [], "ok": False}
    plan["status"] = _file_status(doc, problems)
    hdr = doc.header("deadline")
    if hdr and not _blank(hdr[0]):
        val = hdr[0].strip()
        try:
            if not DATE_RE.match(val):
                raise ValueError
            _dt.date.fromisoformat(val)
            plan["deadline"] = val
        except ValueError:
            problems.append(_warn("W-DEADLINE", doc.name, hdr[1], f"Deadline should be YYYY-MM-DD, not '{val}' (not shown)"))

    sec = doc.section("Task cards")
    if sec is None:
        problems.append(_err("E-STRUCTURE", doc.name, None, "missing section '## Task cards'"))
    else:
        plan["ok"] = True
        for h, lv, text in doc.headings:
            if not (sec[1] <= h < sec[2] and lv == 3):
                continue
            if not text.startswith("T-"):
                continue  # other sub-headings are allowed and ignored
            m = CARD_RE.match(text)
            if not m:
                problems.append(_err("E-STRUCTURE", doc.name, h + 1,
                                     f"task card heading should be '### T-01: <short name>', not '{text}'"))
                continue
            tid, name = m.group(1), m.group(2).strip()
            if tid in plan["cards"]:
                problems.append(_err("E-STRUCTURE", doc.name, h + 1, f"two task cards for {tid}"))
                continue
            plan["cards"][tid] = _parse_card(doc, h, h + 1, doc.end(h, 3, sec[2]), tid,
                                             tid if _blank(name) else name)
            plan["order"].append(tid)
        if not plan["order"]:
            problems.append(_err("E-STRUCTURE", doc.name, sec[0] + 1, "'## Task cards' has no '### T-01: <short name>' card"))

    rows, tbl = _read_table(doc, "Task groups", problems, prefix=True, required=False)
    if rows is not None:
        cols = [c.strip().lower() for c in tbl[1]]
        if "tasks" not in cols:
            problems.append(_warn("W-NO-GROUPS", doc.name, tbl[0], "task groups table has no 'Tasks' column; groups worked out from 'Depends on'"))
        else:
            why = next((c for c in ("why this order", "reason", "why") if c in cols), None)
            plan["groups"] = [{"cell": r["tasks"], "why": "" if not why or _blank(r[why]) else r[why],
                               "label": r.get("group", "").strip(), "line": r["_line"]}
                              for r in rows if not _blank(r["tasks"])]
    return plan


def _load_labels(d: Path, problems):
    p = d / LABELS
    if not p.is_file():
        return None
    try:
        obj = json.loads(p.read_bytes().decode("utf-8-sig"))
    except RecursionError:
        raise FileProblem(f"{LABELS} is nested too deeply to read; it should hold one 'labels' object "
                          f"(delete the file to build without it)") from None
    except (ValueError, UnicodeDecodeError) as e:
        problems.append(_err("E-LABEL-ID", LABELS, None, f"not valid JSON: {e}"))
        return None
    if not isinstance(obj, dict) or not isinstance(obj.get("labels"), dict):
        problems.append(_err("E-LABEL-ID", LABELS, None, "needs a 'labels' object keyed by ID"))
        return None
    return obj


def parse_planning(planning_dir):
    """Returns (model, problems). Raises OSError or FileProblem if a file exists but cannot be read."""
    d = Path(planning_dir)
    problems: list[Problem] = []
    model = {"sha256": {}, "labels": None,
             "spec": {"name": "", "status": None, "goal": "", "deliverables": [], "ok": False},
             "resources": {"items": [], "ok": False},
             "plan": {"name": "", "status": None, "deadline": None, "groups": None,
                      "cards": {}, "order": [], "ok": False}}
    parsers = {SPEC: ("spec", _parse_spec), RES: ("resources", _parse_resources), PLAN: ("plan", _parse_plan)}
    for name in SOURCES:
        p = d / name
        if not p.is_file():
            problems.append(_err("E-STRUCTURE", name, None, f"file not found in {d}"))
            continue
        raw = p.read_bytes()
        model["sha256"][name] = hashlib.sha256(raw).hexdigest()
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError as e:
            problems.append(_err("E-STRUCTURE", name, None, f"not UTF-8 text ({e.reason} at byte {e.start})"))
            continue
        key, fn = parsers[name]
        model[key] = fn(Doc(name, text), problems)
    model["labels"] = _load_labels(d, problems)
    return model, problems


# --------------------------------------------------------------------------- tasks and checks

def _did_you_mean(x, cards):
    """' (did you mean T-01?)' when x is 'T-1' and T-01 exists, else ''."""
    alt = [t for t in cards if t != x and int(t[2:]) == int(x[2:])]
    return f" (did you mean {alt[0]}?)" if len(alt) == 1 else ""


def _loops(tasks):
    """Groups of two or more tasks that wait on each other in a loop (strongly connected
    components of 'Depends on'), in plan order. Iterative, so long chains are fine."""
    index, low, on, stack, out, n = {}, {}, set(), [], [], 0
    for root in tasks:
        if root in index:
            continue
        work = [(root, iter(tasks[root]["deps"]))]
        index[root] = low[root] = n
        n += 1
        stack.append(root)
        on.add(root)
        while work:
            v, it = work[-1]
            w = next((x for x in it if x in tasks), None)
            if w is not None:
                if w not in index:
                    index[w] = low[w] = n
                    n += 1
                    stack.append(w)
                    on.add(w)
                    work.append((w, iter(tasks[w]["deps"])))
                elif w in on:
                    low[v] = min(low[v], index[w])
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = set()
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.add(w)
                    if w == v:
                        break
                if len(comp) > 1:
                    out.append(comp)
    order = list(tasks)
    return sorted(out, key=lambda c: min(order.index(x) for x in c))


def _loop_path(tasks, first, members):
    """Shortest loop from first back to first, inside members: [first, ..., last]."""
    prev, queue = {}, [first]
    for v in queue:
        for x in tasks[v]["deps"]:
            if x == first:
                path = [v]
                while path[-1] != first:
                    path.append(prev[path[-1]])
                return path[::-1]
            if x in members and x not in prev:
                prev[x] = v
                queue.append(x)
    return [first]


def _tasks(model, P):
    """Task records with groups assigned. Appends problems to P."""
    plan, spec = model["plan"], model["spec"]
    cards = plan["cards"]
    d_ids = {x["id"] for x in spec["deliverables"]}
    r_ids = {x["id"] for x in model["resources"]["items"]}
    removed = {t for t in plan["order"]
               if _field_text(cards[t], "status").lower().startswith(REMOVED)}
    live = [t for t in plan["order"] if t not in removed]

    tasks = {}
    for tid in live:
        c = cards[tid]
        f = {k: _field_text(c, k) for k in ("objective", "serves", "inputs", "outputs", "depends", "steps", "decisions", "status")}
        f = {k: "" if _blank(v) else v for k, v in f.items()}
        deps = [x for x in _task_ids(f["depends"], cards) if x != tid]
        in_tasks = [x for x in _task_ids(f["inputs"], cards) if x != tid]
        t = {"id": tid, "name": c["name"], "line": c["line"], "objective": "" if _blank(f["objective"]) else f["objective"],
             "deps": [], "delivers": [], "res": [], "ver": _check_items(c), "card": c,
             "decisions": "" if _blank(f["decisions"]) else f["decisions"]}
        for x in deps:
            if x in removed:
                P.append(_warn("W-REMOVED-DEP", PLAN, c["line"], f"{tid} depends on {x}, which is marked removed"))
            elif x not in cards:
                P.append(_err("E-UNKNOWN-REF", PLAN, c["line"], f"{tid} depends on {x}, which has no task card{_did_you_mean(x, cards)}"))
            else:
                t["deps"].append(x)
        for x in in_tasks:
            if x in cards and x not in removed and x not in deps:
                P.append(_warn("W-INPUT-DEP", PLAN, c["line"], f"{tid} uses output of {x} (Inputs) but does not list it in 'Depends on'"))
        for x in dict.fromkeys(FIND["deliverable"].findall(f["serves"])):
            if spec["ok"] and x not in d_ids:
                P.append(_err("E-UNKNOWN-REF", PLAN, c["line"], f"{tid} serves {x}, which is not in the SPEC.md deliverables"))
            else:
                t["delivers"].append(x)
        for x in dict.fromkeys(FIND["resource"].findall(f["inputs"])):
            if model["resources"]["ok"] and x not in r_ids:
                P.append(_err("E-UNKNOWN-REF", PLAN, c["line"], f"{tid} uses {x}, which is not in the RESOURCES.md table"))
            else:
                t["res"].append(x)
        if not t["ver"]:
            filled = [" ".join(ln for ln in fl["lines"] if ln).strip() for fl in c["checks"]]
            ph = next((s for s in filled if PLACEHOLDER_RE.match(s)), None)
            if ph:
                short = ph if len(ph) <= 50 else ph[:47].rstrip() + "...]"
                why = f"its 'Checks:' line still holds the template text {short}; replace it with your own checks"
            elif c["checks"]:
                why = "its 'Checks:' line is empty; list at least one check"
            else:
                why = "add a 'Checks:' line"
            P.append(_err("E-NO-VERIFY", PLAN, c["line"], f"{tid} has no checks ({why})"))
        st = f["status"].strip().lower()
        if not st or "|" in st:
            st = "planned"
        t["status"] = next((k for k in STATUSES if st.startswith(k)), st)
        out = []
        for key, title in (("inputs", "Inputs"), ("steps", "Steps"), ("outputs", "Outputs"), ("serves", "Serves")):
            fl = c["fields"].get(key)
            lines = [ln for ln in (fl["lines"] if fl else []) if ln]
            if lines and not _blank(" ".join(lines)):
                gap = "\n" if BULLET_RE.match(lines[0]) else " "
                out.append(f"**{title}:**{gap}" + "\n".join(lines))
        t["out"] = "\n\n".join(out)
        tasks[tid] = t

    # Loops in Depends on: one error per set of tasks caught in the same loop.
    loop_of = {}
    for i, members in enumerate(_loops(tasks)):
        loop_of.update(dict.fromkeys(members, i))
        first = min(members, key=live.index)
        path = _loop_path(tasks, first, members)
        text = "tasks wait on each other in a loop: " + " -> ".join(path + [first])
        rest = [x for x in live if x in members and x not in path]
        if rest:
            text += f" ({', '.join(rest)} also wait{'s' if len(rest) == 1 else ''} inside this loop)"
        P.append(_err("E-CYCLE", PLAN, tasks[first]["line"], text))

    # Groups.
    group_of, waves = {}, []
    groups = plan["groups"]
    if groups:
        for gi, g in enumerate(groups):
            cell = "" if PLACEHOLDER_RE.match(g["cell"].strip()) else g["cell"]
            for x in _task_ids(cell, cards):
                if x in removed:
                    continue
                if x not in tasks:
                    P.append(_err("E-UNKNOWN-REF", PLAN, g["line"],
                                  f"task group lists {x}, which has no task card{_did_you_mean(x, cards)}"))
                elif x in group_of:
                    P.append(_warn("W-GROUP-TWICE", PLAN, g["line"], f"{x} is in more than one group; shown in the first"))
                else:
                    group_of[x] = gi
            label = g["label"]
            waves.append({"k": f"Group {label}" if label and not _blank(label) and label.isdigit() else (label or f"Group {gi + 1}"),
                          "d": g["why"]})
    elif tasks:
        P.append(_warn("W-NO-GROUPS", PLAN, None, "no task groups filled in; groups worked out from 'Depends on'"))

    # Place tasks no group lists: with their latest dependency (or first), in dependency order.
    def level(n, seen=()):
        if n in group_of:
            return group_of[n]
        if n in seen:
            return 0
        ds = [level(x, seen + (n,)) for x in tasks[n]["deps"] if x in tasks]
        base = max(ds) if ds else 0
        return base if groups else (base + 1 if ds else 0)

    for n in tasks:
        if n not in group_of:
            if groups:
                P.append(_warn("W-NO-GROUP", PLAN, tasks[n]["line"], f"{n} is in no task group; shown with the tasks it waits on"))
            group_of[n] = level(n)
    if not groups:
        waves = [{"k": f"Group {i + 1}", "d": "worked out from 'Depends on'"}
                 for i in range(max(group_of.values(), default=-1) + 1)]
    for n, t in tasks.items():
        t["g"] = min(group_of[n], len(waves) - 1) if waves else 0
    for t in tasks.values():
        for x in t["deps"]:
            if t["id"] in loop_of and loop_of[t["id"]] == loop_of.get(x):
                continue  # already reported as E-CYCLE
            if x in tasks and tasks[x]["g"] > t["g"]:
                P.append(_err("E-SCHEDULE", PLAN, t["line"],
                              f"{t['id']} is in {waves[t['g']]['k']} but waits on {x}, which is in the later {waves[tasks[x]['g']]['k']}"))
    return [tasks[t] for t in live], waves


def validate(model):
    """All cross-file checks. Returns (problems, tasks, waves)."""
    P: list[Problem] = []
    tasks, waves = _tasks(model, P)
    produced = {d for t in tasks for d in t["delivers"]}
    for d in model["spec"]["deliverables"]:
        if d["id"] not in produced:
            P.append(_warn("W-NO-PRODUCER", SPEC, d["line"], f"{d['id']} is served by no task"))
    lab = model["labels"]
    if lab is not None:
        known = {t["id"] for t in tasks} | {d["id"] for d in model["spec"]["deliverables"]} \
            | {r["id"] for r in model["resources"]["items"]}
        for key, val in lab["labels"].items():
            if key not in known:
                P.append(_err("E-LABEL-ID", LABELS, None, f"label for '{key}', which is not a known task, deliverable or resource"))
            elif not isinstance(val, dict) or not isinstance(val.get("label"), str) or not val["label"].strip():
                P.append(_err("E-LABEL-ID", LABELS, None, f"label for '{key}' is empty"))
        srcs = lab.get("sources") if isinstance(lab.get("sources"), dict) else {}
        stale = [n for n in SOURCES if n in model["sha256"] and str(srcs.get(n, "")).lower() != model["sha256"][n]]
        if stale:
            P.append(_warn("W-STALE-LABELS", LABELS, None, f"{', '.join(stale)} changed since the labels were written"))
    return P, tasks, waves


# --------------------------------------------------------------------------- build

def build_page_data(model, tasks, waves, built, warnings):
    spec, plan = model["spec"], model["plan"]
    labels = model["labels"]["labels"] if model["labels"] else {}

    def lab(i, label, plain=""):
        v = labels.get(i)
        if isinstance(v, dict):
            if isinstance(v.get("label"), str) and v["label"].strip():
                label = v["label"]
            if isinstance(v.get("plain"), str) and v["plain"].strip():
                plain = v["plain"]
        return label, plain

    used = [k for k in STATUSES if any(t["status"] == k for t in tasks)]
    used += sorted({t["status"] for t in tasks} - set(STATUSES))
    extra = iter(["o3", "o1", "o4", "o5"] * 10)
    statuses = {k: {"n": STATUSES[k][0] if k in STATUSES else k[:1].upper() + k[1:],
                    "c": STATUSES[k][1] if k in STATUSES else next(extra)} for k in used}

    page_tasks = []
    for t in tasks:
        label, plain = lab(t["id"], t["name"], t["objective"])
        page_tasks.append({"id": t["id"], "name": t["name"], "status": t["status"], "s": t["g"], "e": t["g"] + 1,
                           "label": label, "plain": plain, "out": t["out"], "ver": t["ver"],
                           "res": t["res"], "deliv": t["delivers"], "deps": t["deps"],
                           "decisions": [t["decisions"]] if t["decisions"] else []})
    delivs = []
    for d in spec["deliverables"]:
        label, plain = lab(d["id"], d["label"])
        delivs.append({"id": d["id"], "name": d["name"], "label": label, "plain": plain,
                       "req": d["req"], "type": None, "fields": {}})
    resources = {}
    for r in model["resources"]["items"]:
        label, _ = lab(r["id"], r["label"])
        resources[r["id"]] = {"label": label, "desc": r["desc"]}

    lab_meta = {"by": None, "on": None, "stale": any(w.rule == "W-STALE-LABELS" for w in warnings)}
    if model["labels"]:
        wb = model["labels"].get("written_by")
        if isinstance(wb, dict):
            by = "/".join(str(wb[k]) for k in ("tool", "model") if wb.get(k))
            lab_meta["by"] = by or None
        elif isinstance(wb, str) and wb.strip():
            lab_meta["by"] = wb.strip()
        lab_meta["by"] = lab_meta["by"] or "unknown"
        if isinstance(model["labels"].get("date"), str):
            lab_meta["on"] = model["labels"]["date"]
    return {
        "title": plan["name"] or spec["name"] or "Research plan",
        "goal": spec["goal"],
        "status": plan["status"] or "DRAFT",
        "built": built,
        "deadline": plan["deadline"],
        "waves": waves,
        "statuses": statuses,
        "resources": resources,
        "tasks": page_tasks,
        "deliverables": delivs,
        "sources": {n: model["sha256"].get(n, "")[:12] for n in SOURCES},
        "labels": lab_meta,
        "tool": f"{TOOL} {VERSION}",
        "warnings": [str(w) for w in warnings],
    }


def render(page_data, template_path=TEMPLATE):
    tpl = Path(template_path).read_text(encoding="utf-8")
    if tpl.count(MARKER) != 1:
        raise ValueError(f"{template_path} must contain {MARKER} exactly once")
    blob = json.dumps(page_data, ensure_ascii=False, separators=(",", ":"))
    blob = (blob.replace("</", "<\\/").replace("<!--", "\\u003c!--")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    return tpl.replace(MARKER, blob)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(prog="plan_viewer.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("planning_dir", type=Path, help="folder with SPEC.md, RESOURCES.md, PLAN.md (usually docs/planning)")
    ap.add_argument("-o", "--out", type=Path, help=f"output file (default: <planning_dir>/{OUT_NAME})")
    ap.add_argument("--built", help="date shown on the page, YYYY-MM-DD (default: today)")
    ap.add_argument("--check", action="store_true", help="only list problems; write nothing")
    a = ap.parse_args(argv)

    if a.check and a.out is not None:
        print("error: --check writes nothing; do not combine it with -o", file=sys.stderr)
        return 2
    built = a.built or _dt.date.today().isoformat()
    try:
        if not DATE_RE.match(built):
            raise ValueError
        _dt.date.fromisoformat(built)
    except ValueError:
        print(f"error: --built must be YYYY-MM-DD, not {built!r}", file=sys.stderr)
        return 2
    if not a.planning_dir.is_dir():
        print(f"error: folder not found: {a.planning_dir}", file=sys.stderr)
        return 2
    try:
        model, problems = parse_planning(a.planning_dir)
    except OSError as e:
        print(f"error: cannot read planning files: {e}", file=sys.stderr)
        return 2
    except FileProblem as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    more, tasks, waves = validate(model)
    problems += more
    errors = [p for p in problems if p.is_error]
    warnings = [p for p in problems if not p.is_error]
    for p in errors + warnings:
        print(p, file=sys.stderr)
    if errors:
        print(f"{len(errors)} error(s), {len(warnings)} warning(s); nothing written", file=sys.stderr)
        return 1
    if a.check:
        print(f"ok ({len(warnings)} warning(s))")
        return 0
    out = (a.out or a.planning_dir / OUT_NAME).resolve()
    try:
        out.write_text(render(build_page_data(model, tasks, waves, built, warnings)), encoding="utf-8", newline="\n")
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(out.as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
