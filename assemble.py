#!/usr/bin/env python3

import os
from pathlib import Path


def align(text):
  """ White-space align and return the lines of the supplied text. """

  out = []

  # Some helper methods.
  len_whitespace = lambda l: len(l)-len(l.lstrip())
  closing_tag = lambda l: l.lstrip().startswith('</')

  # Iterate over all the lines of the supplied text.
  # Initial whitespace-length set to first line of text.
  lines = text.splitlines()
  w_prev = len_whitespace(lines[0])
  for line in text.splitlines():
    w_line = len_whitespace(line)
    if w_line < w_prev and not closing_tag(line):
      if line.startswith('}'):
        # Ensure correct alignment on css closing-brackets.
        line = f"{' '*(w_prev-2)}{line}"
      else:
        line = f"{' '*w_prev}{line}"
      w_line = len_whitespace(line)
    w_prev = w_line
    out.append(line)

  # If the text starts with whitespace, assume it is consistent and remove.
  text = os.linesep.join(out)
  w_all = len_whitespace(text)
  if w_all:
    text = os.linesep.join([l[w_all:] for l in text.splitlines()])
  return text


def html():
  """ Read files from disk, assemble and return complete html structure. """

  read = lambda p: Path(p).read_text().strip(os.linesep)
  cv_css, cv_html, cv_js = read("cv.css"), read("cv.html"), read("cv.js")

  html= f"""\
    <!doctype html>
    <html>
      <head>
        <style>
          {cv_css}
        </style>
      </head>
      <body>
        {cv_html}
      </body>
      <script>
        {cv_js}
      </script>
    </html>
  """

  return align(html)


def main():
  """ Entry point for the script, complete the full assembly and print. """

  main_python_runner = Path('python.py').read_text()
  html_expanded = html()
  html_expanded = html_expanded.replace("{","{{").replace("}", "}}")
  main_python_runner = main_python_runner.replace('{html()}', html_expanded)
  print(main_python_runner)

if __name__ == "__main__":
  main()
