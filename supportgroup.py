#!/usr/bin/env python3
"""
Updated this to allow changing processes other than self:
    https://gist.github.com/epinna/8ce25ac36a7710cdd1806764c647cf99
"""
import argparse
import os
import re


def update_argv(pid, newargs=None):
    with open('/proc/{}/cmdline'.format(pid), 'rb') as f:
        cmdline = f.read()
        cmdline_len = len(cmdline) - 1
    if newargs is None:
        return cmdline_len
    with open('/proc/{}/maps'.format(pid)) as f:
        maps = f.read()
    stack_start, stack_end = [int(x, 16) for x in re.search('([0-9a-f]+)-([0-9a-f]+).*\[stack\]', maps).groups()]
    stack_size = stack_end - stack_start
    with open('/proc/{}/mem'.format(pid), 'rb+') as mem:
        mem.seek(stack_start)
        data = mem.read(stack_size)
        argv_addr = stack_start + data.find(cmdline)
        mem.seek(argv_addr)
        newargs = b'\x00'.join(newargs.strip(b'\x00').split(b' '))
        if len(newargs) > cmdline_len:
            newargs = newargs[:cmdline_len]
            print('WARNING: You gave too many characters. Truncating to "{}"...'.format(newargs.decode().replace('\x00',' ')))
        newargs += b'\x00'*(cmdline_len - len(newargs) + 1)
        mem.write(newargs)
    return len(newargs)


def main():
    parser = argparse.ArgumentParser(description='Renames a process in process list. Must be root!')
    parser.add_argument('-p', '--pid', required=True, type=int, help='PID of process to rename')
    parser.add_argument('--rename', default=None, type=str, help='The name/args to rename the process')
    args = parser.parse_args()

    if args.rename is None:
        print('You can rename the process name for pid={} with {} characters'.format(args.pid, update_argv(args.pid)))
    else:
        update_argv(args.pid, newargs=args.rename.encode())
        print('Process name updated!')
    return

if __name__ == '__main__':
    if os.geteuid() != 0:
        print('You must run this as root!')
    else:
        main()
