#!/usr/bin/env python3
import os
import socket

from assemble import html
HTML = f"""\
HTTP/1.1 200 OK

{html()}
"""

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
    print(f'got: {data}')
    connection.sendall(HTML.encode())
    connection.close()

if __name__ == "__main__":
  main()
