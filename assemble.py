#!/usr/bin/env python3
import os
from pathlib import Path

read = lambda p: Path(p).read_text().strip(os.linesep)

html_cv, javascript = read("cv.html"), read("cv.js")

def align(text):
  out = []
  lines = text.splitlines()
  len_whitespace = lambda l: len(l)-len(l.lstrip())
  tag_closing = lambda l: l.lstrip().startswith('</')

  for prev, current in zip([""]+lines, lines+[""]):
    w_prev, w_current = len_whitespace(prev), len_whitespace(current)
    if w_current < w_prev and not tag_closing(current):
      current = f"{' '*w_prev}{current}"
    out.append(current)
  out = out[:-1]
  return os.linesep.join(out)

html= align(f"""\
<!doctype html>
<html>
  <head>
  </head>
  <body>
    {html_cv}
  </body>
  <script>
    {javascript}
  </script>
</html>
""")

print(html)
