#!/usr/bin/env python3
""" Dumps readable maps from memory to disk, for a given PID """
import argparse
import os
import re
def get_maps(pid):
    maps = []
    with open('/proc/{}/maps'.format(pid)) as f:
        for line in f:
            m = re.search('([a-f0-9]+)-([a-f0-9]+)\sr(.{3})\s.*?(\s+|\S+)$', line)
            if m is None:
                continue
            start, end, perms, name = m.groups()
            if name.isspace():
                name = 'unknown'
            name = name.strip('[]')
            maps.append((int(start, 16), int(end, 16), perms, name))
    return maps
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pid', default='self', help='The PID of the program to memdump')
    parser.add_argument('--datadir', default='data', help='The PID of the program to memdump')
    args = parser.parse_args()
    output_dir = os.path.abspath(args.datadir)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    f = open('/proc/{}/mem'.format(args.pid), 'rb')
    for start, end, perms, name in get_maps(args.pid):
        if 'heap' in name or 'stack' in name or 'unknown' in name:
            ofname = os.path.join(output_dir, '{}_{:x}-{:x}.dmp'.format(name, start, end))
            f.seek(start)
            with open(ofname, 'wb') as of:
                try:
                    of.write(f.read(end-start))
                except Exception as e:
                    continue
            print('[+] memory written to {}'.format(ofname))
    f.close()
if __name__ == '__main__':
    main()

