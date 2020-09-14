#!/usr/bin/env python3
import os
import socket
import random

from pathlib import Path
from assemble import \
  html, mugshot, svg_circle_filled, svg_circle_empty, svg_circle_quater, \
  svg_circle_half

from base64 import b64encode, b64decode

HTML = f"""\
HTTP/1.1 200 OK

{html()}
"""

HTML_MUGSHOT = mugshot()

HTML_CIRCLE_FILLED_SVG = svg_circle_filled()
HTML_CIRCLE_EMPTY_SVG = svg_circle_empty()
HTML_CIRCLE_HALF_SVG = svg_circle_half()
HTML_CIRCLE_QUATER_SVG = svg_circle_quater()

def main():
  host, max_buff = '', 1024

  socket_in = socket.socket(
    socket.AF_INET, # IPv4.
    socket.SOCK_STREAM, # TCP.
  )

  port = int(''.join([str(random.choice(range(1,10))) for _ in range(4)]))

  socket_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  socket_in.bind((host, port))
  socket_in.listen(1)

  print(f"Hosting web-view of pdf on http://localhost:{port}")

  while True:
    connection, address = socket_in.accept()
    data = b""
    while True:
      data_part = connection.recv(max_buff)
      data += data_part
      if len(data_part) < max_buff:
        break

    data = data.decode('utf-8')
    if data.startswith(f"GET /static/mugshot_resized.jpg"):
      response = HTML_MUGSHOT
    elif data.startswith(f"GET /static/circle_full.svg"):
      response = HTML_CIRCLE_FILLED_SVG
    elif data.startswith(f"GET /static/circle_empty.svg"):
      response = HTML_CIRCLE_EMPTY_SVG
    elif data.startswith(f"GET /static/circle_half.svg"):
      response = HTML_CIRCLE_HALF_SVG
    elif data.startswith(f"GET /static/circle_quater.svg"):
      response = HTML_CIRCLE_QUATER_SVG
    else:
      response = HTML

    print(f'got: {data}')
#    print(f'sending: {response}')
    if type(response) == str:
      response = response.encode()
    connection.sendall(response)
    connection.close()

if __name__ == "__main__":
  main()

