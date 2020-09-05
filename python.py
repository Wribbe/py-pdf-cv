#!/usr/bin/env python3
import os
import socket

from pathlib import Path
from assemble import html, mugshot, box_svg

from base64 import b64encode, b64decode

HTML = f"""\
HTTP/1.1 200 OK

{html()}
"""

HTML_MUGSHOT = mugshot()

HTML_BOX_SVG = box_svg()

def main():
  host, port, max_buff = '', 8800, 1024
  socket_in = socket.socket(
    socket.AF_INET, # IPv4.
    socket.SOCK_STREAM, # TCP.
  )
  socket_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  socket_in.bind((host, port))
  socket_in.listen(1)
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
    elif data.startswith(f"GET /static/box.svg"):
      response = HTML_BOX_SVG
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

