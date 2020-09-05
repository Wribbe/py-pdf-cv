#!/usr/bin/env python3

import os
import re

from base64 import b64encode, b64decode

from pathlib import Path

ALIGN_START = "__align__start"
ALIGN_END = "__align__end"

def align(text):
  """ White-space align and return the lines of the supplied text. """

  out = []
  indents = [0]
  len_whitespace = lambda l: len(l)-len(l.lstrip())

  for line in text.splitlines():

    if not line.strip():
      continue

    if line.strip() == ALIGN_START:
      indent = len_whitespace(line)
      if not indent:
        indent = len_whitespace(out[-1])
      indents.append(indent)
      continue
    elif line.strip() == ALIGN_END:
      indents.pop()
      continue

    line = f"{' '*indents[-1]}{line}"
    out.append(line)

  # If the text starts with whitespace, assume it is consistent and remove.
  text = os.linesep.join(out)
  ws_all = len_whitespace(text)
  if ws_all:
    text = os.linesep.join([l[ws_all:] for l in text.splitlines()])
  return text


def html():
  """ Read files from disk, assemble and return complete html structure. """


  def read(path):

    text = Path(path).read_text()

    out = []
    for line in text.splitlines():
      if line.strip().startswith("<img "):
        path = Path(line.split('src=')[-1][1:-2])
        if path.suffix == 'svg':
          line = read(path)
      out.append(line)
    text = os.linesep.join(out)

    return os.linesep.join([
      ALIGN_START,
      text.strip(os.linesep),
      ALIGN_END,
    ])

  cv_css, cv_html, cv_js = read("cv.css"), read("cv.html"), read("cv.js")

  html= f"""\
    <!doctype html>
    <html>
      <head>
        <title>CV - Stefan Eng</title>
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

linend = lambda t: '\r\n'.join([l.strip() for l in t.splitlines()])

def mugshot():

  data = open(Path('static','mugshot_resized.jpg'), 'rb').read()

  header = align(f"""
    HTTP/1.0 200 OK
    Content-Type: image/jpeg
    Content-Length: {len(data)}
    Accept-Ranges: bytes
    Server: custom
  """)
  header = linend(header)+"\r\n"*2
  response = header.encode()+data
  return response

def box_svg():

  data = open(Path('static','box.svg'), 'rb').read()

  header = align(f"""
    HTTP/1.0 200 OK
    Content-Type: image/svg+xml
    Content-Length: {len(data)}
    Accept-Ranges: bytes
    Server: custom
  """)
  header = linend(header)+"\r\n"*2
  response = header.encode()+data
  return response


def main():
  """ Entry point for the script, complete the full assembly and print. """

  main_python_runner = Path('python.py').read_text()
  html_expanded = html()
  html_expanded = html_expanded.replace("{","{{").replace("}", "}}")
  main_python_runner = main_python_runner.replace('{html()}', html_expanded)

  out = []
  for line in main_python_runner.splitlines():
    if line.startswith('from assemble'):
      continue
    out.append(line)

  main_python_runner = os.linesep.join(out)
  methods = [m[:-2] for m in re.findall(r'\w+\(\)', main_python_runner)]

  for method in methods:
    if method in ['main'] or method not in globals():
      continue
    main_python_runner = main_python_runner.replace(
      f"{method}()", f"b64decode({b64encode(globals()[method]())})"
    )

  print(main_python_runner)

if __name__ == "__main__":
  main()
