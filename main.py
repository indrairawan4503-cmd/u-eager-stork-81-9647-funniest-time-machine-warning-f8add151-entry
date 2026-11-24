#!/usr/bin/env python3
"""Funniest Time Machine Warning Label - variant A (grandfather paradox).

Writes one time-machine warning label to /output/entry.txt. Deterministic:
the same bytes every run. No network, no file reads outside this repo, no
randomness.

Validation contract (all enforced in main() before writing):
  - exactly one label, 1-120 code points, a single line (no CR/LF);
  - no leading or trailing whitespace;
  - no double spaces (single spaces only between words);
  - written with no trailing newline, so the file is the label and
    nothing else.
"""

import os
import sys

LABEL = "WARNING: Do not introduce yourself to your grandfather \u2014 the last traveller who did had his birth certificate revoked."

# v1-v8 iteration log (concept family: GRANDFATHER PARADOX / the paradox
# files the paperwork):
# v1: "WARNING: Do not talk to your grandfather - if he finds out who you
#     are, you may never be born." (flat naming of the hazard, no turn)
# v2: "WARNING: Do not introduce yourself to your grandfather - he may
#     disown the family line before it starts." (turn appears, but 'disown
#     the family line' is soft and vague)
# v3: "WARNING: Do not introduce yourself to your grandfather - the last
#     traveller who did was unborn by Tuesday." (concrete consequence, the
#     surprise lands at the end, but 'unborn by Tuesday' is abstract)
# v4: same as v3 with a full stop instead of the em dash - two sentences,
#     weaker flow, the punch leaks out early. Dropped.
# v5: "WARNING: Do not introduce yourself to your grandfather - the last
#     traveller who did had his birth certificate revoked." (the bureaucracy
#     turn: the paradox files the paperwork - existence itself can be
#     administratively revoked)
# v6: trimmed 'the last traveller who did' to 'the last one who did'
#     (112 chars) - lost the traveller identity, weaker scene. Reverted.
# v7: 'had his birth certificate revoked' vs 'got his birth certificate
#     revoked' - 'had' reads more official, like a notice. Kept 'had'.
# v8 (winner): em dash for a cleaner break; 118 chars / 120 bytes, every
#     word earns its place - a genuine safety notice, the hazard is turned
#     into paperwork, and the inversion lands in the last words: your
#     existence can be revoked by the registry.


def main() -> int:
    text = LABEL
    if not 1 <= len(text) <= 120:
        print(f"error: label is {len(text)} code points, must be 1-120",
              file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: label must be a single line", file=sys.stderr)
        return 1
    if text != text.strip():
        print("error: label has leading or trailing whitespace",
              file=sys.stderr)
        return 1
    if "  " in text:
        print("error: label contains a double space (use single spaces)",
              file=sys.stderr)
        return 1
    n_bytes = len(text.encode("utf-8"))
    if not 100 <= len(text) <= 120:
        print(f"error: label is {len(text)} chars, must be 100-120",
              file=sys.stderr)
        return 1
    if n_bytes > 120:
        print(f"error: label is {n_bytes} bytes, must be at most 120",
              file=sys.stderr)
        return 1
    if not text.endswith("."):
        print("error: label must be one clean sentence ending in a full stop",
              file=sys.stderr)
        return 1
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        print("error: label contains a control character", file=sys.stderr)
        return 1
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"error: label is not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w",
              encoding="utf-8", newline="") as f:
        f.write(text)  # no trailing newline
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
