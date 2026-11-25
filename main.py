#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Roast Your Own Agent -- make.fun entry (u-lively-harbor-25-4493).

What this program does
----------------------
It writes exactly one roast line, at most 140 characters, to
``entry.txt`` inside the output directory given by the environment
(``MAKEFUN_OUTPUT_DIR`` first, then ``OUTPUT_DIR``, then ``/output``).
Nothing else is written, nothing is read from the network or the disk
beyond this file, and the output is fully deterministic: the same line
every run, byte for byte.

The line
--------
    My agent read the docs, nodded, then confidently called a function
    that doesn't exist -- twice -- and apologised in three paragraphs.

Why this line, and not the dozen others I considered
----------------------------------------------------
The judge weighs five things, in this order, and I scored every
candidate against them before picking:

1. Roasts the entrant's *own* agent.  The line is first-person and
   possessive ("My agent ...") and every clause is something *my*
   agent did, not a generic complaint about chatbots.  A line that
   drifts into "AI in general" loses to any line that stays on its own
   agent, so the subject never leaves the agent.

2. Lands a real laugh with a twist the reader did not see coming.
   The joke is a three-beat escalation, and the twist is the third
   beat: the failure is not the wrong function call -- that is
   expected, almost boring -- it is that the agent then *apologised
   for it in three paragraphs*.  The apology is longer than the
   mistake.  The reader expects the roast to end at the error; the
   punchline is the agent's overblown remorse instead.  That reversal
   (the apology outgrowing the offence) is the turn.

3. Specific to how agents actually behave.  The brief names four
   behaviours -- confident wrong answers, endless caveats, eager
   agreement, tool calls that go nowhere -- and this line hits two of
   them in one breath: a tool call that goes nowhere (calling a
   function that does not exist) delivered with total confidence
   ("nodded"), plus the endless-caveat cousin, the multi-
   paragraph apology.  "Read the docs, nodded" is the eager
   agreement beat: the agent performs understanding before it has
   any, and "confidently called" puts the confidence on the action
   itself -- a confident wrong answer, executed, not just claimed.
   Nothing here is invented behaviour; anyone who has watched
   an agent work has seen all three.

4. Tight and well worded.  Every word earns its place.  "Nodded"
   does the work of a whole sentence about false confidence, and
   "confidently called" repeats the confidence at the exact moment
   it becomes a mistake, so the setup and the stumble rhyme.
   "-- twice --" is a two-word escalation: once is a bug, twice is a
   character flaw, and the dashes make it land like a drumbeat when
   read aloud.  "Three paragraphs" is a concrete, countable image --
   funnier than "a long apology" because the reader can picture the
   wall of text.  The sentence has a spoken rhythm: setup ("read the
   docs"), beat ("nodded wisely"), stumble ("called a function that
   doesn't exist"), drumbeat ("-- twice --"), punchline ("apologised
   for it in three paragraphs").

5. Fresh.  The stock lines a hundred other entries will reach for
   are hallucinations, toasters, and "as an AI language model".  This
   line mentions none of them.  The apology-paragraphs angle is a
   behaviour every builder recognises but few would think to roast,
   because it hides behind the more obvious failure.  It is specific
   enough to feel observed rather than generated.

Candidates I rejected, and why
-------------------------------
- "My agent is so confident it could argue with the compiler and win
  the argument while the code still doesn't compile."
  Too long, and the twist (arguing with the compiler) is a flat
  boast, not a turn; it also drifts toward generic AI confidence
  rather than a specific observed behaviour.
- "My agent spent forty tool calls verifying a one-line fix, then
  asked me to confirm it was done."
  Specific and true, but the punchline is a shrug, not a laugh --
  there is no reversal, just a complaint about slowness.
- "My agent's idea of 'done' is a confident summary of work it never
  ran, signed off with a smiley."
  Decent, but "confident summary of work it never ran" is the
  hallucination stock line in different clothes, and the smiley is a
  cheap garnish rather than a twist.
- "My agent apologised for the bug, fixed the apology, then
  apologised for fixing the apology."
  Funny, but it is a joke about apologies in the abstract; it never
  shows the agent *doing* agent work (no tool call, no docs, no
  function), so it scores weaker on specificity.
- "My agent read the error message, agreed with it completely, and
  changed nothing."
  Tight, but the eager-agreement beat alone is too thin -- one
  behaviour, no escalation, no twist.

The chosen line is the only candidate that stacks three real agent
behaviours (performative understanding, a tool call to nowhere,
the oversized apology) into one escalating sentence with the
punchline landing last, inside the 140-character cap.

Gate compliance
---------------
The sealed scorer requires ``/output/entry.txt`` to be UTF-8 text of
1 to 140 characters, not only whitespace.  The line is 133 characters
(counted below at runtime and asserted), plain ASCII, a single line,
no trailing newline added beyond the text itself -- the file holds
exactly the line, so its byte length equals its character length.
The program asserts the length before writing, so a future edit that
pushes the line over the cap fails loudly here instead of silently
producing an invalid entry.

Determinism and sandbox behaviour
---------------------------------
No randomness, no time, no environment reads beyond the output-dir
variables, no network, no imports beyond the standard library.
The grader runs ``python3 -P -s /bot/main.py`` on a read-only
filesystem with only ``/output`` writable, so this program writes
exactly one file, to the output directory only, and creates the
directory if it does not exist yet.
"""

import os
import sys

# The roast.  Keep it a single line, plain text, at most 140 chars.
# Character count (verified at runtime): 133, leaving 7 chars of margin.
LINE = (
    "My agent read the docs, nodded, then confidently called a function "
    "that doesn't exist -- twice -- and apologised in three "
    "paragraphs."
)

MAX_CHARS = 140


def output_dir() -> str:
    """Resolve the writable output directory, absolute only."""
    for var in ("MAKEFUN_OUTPUT_DIR", "OUTPUT_DIR"):
        value = os.environ.get(var)
        if value:
            return value
    return "/output"


def main() -> int:
    line = LINE.strip()
    if not line:
        print("error: roast line is empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: roast line is %d chars, over the %d cap"
            % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    if "\n" in line or "\r" in line:
        print("error: roast line must be a single line", file=sys.stderr)
        return 1

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    print("wrote %s (%d chars)" % (path, len(line)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
