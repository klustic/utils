import socket
import sys

if len(sys.argv) != 2:
  print('Usage: {} <file>'.format(sys.argv[0]))
  sys.exit(1)

with open(sys.argv[1]) as f:
  domains = set(f.read().split())

for domain in domains:
  ip = socket.gethostbyname(domain)
  print('{},{}'.format(domain, ip))
