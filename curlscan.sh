# Paste this into your bash terminal, then use `curlscan` as a command:
# $ curlscan
# Usage: curlscan <ip|domain>
# $ curlscan www.google.com
# www.google.com    80	OPEN
# ^C

curlscan() { if [ $# -ne 1 ]; then echo "Usage: curlscan <ip|domain>"; return; fi; for port in {1..65535}; do curl -m1 -s http://${1}:${port} &>/dev/null; case $? in 7) status=CLOSED;; 28) continue;; *) status=OPEN;; esac; printf "${1} %5d\t%s\n" ${port} ${status}; done; }
