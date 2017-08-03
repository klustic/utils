import argparse
import logging
import re


class FileSanitizer(object):
    IP_REGEX = re.compile('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

    def __init__(self, in_file, out_file='/dev/stdout'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.filter = {}
        self.infile = open(in_file)
        self.outfile = open(out_file, 'a')
        self._ip_gen = self.ip_generator()

    def _read_entry(self):
        for line in self.infile:
            yield line

    def sanitize(self):
        for entry in self._read_entry():
            self.outfile.write(self.sanitize_entry(entry))

    @staticmethod
    def ip_generator():
        for i in range(256):
            for j in range(256):
                for k in range(256):
                    yield '10.{0}.{1}.{2}'.format(i, j, k)

    def sanitize_entry(self, entry):
        for ip_addr in set(self.IP_REGEX.findall(entry)):
            if ip_addr not in self.filter:
                new_ip = self._ip_gen.next()
                self.filter[ip_addr] = {'re': re.compile(re.escape(ip_addr)), 'new_ip': new_ip}
                self.logger.debug('{0} -> {1}'.format(ip_addr, new_ip))
            repl_filter = self.filter.get(ip_addr)
            entry = repl_filter['re'].sub(repl_filter['new_ip'], entry)
        return entry


def main():
    parser = argparse.ArgumentParser(description='Sanitizes IP addresses from a file, rewriting them with'
                                     ' IP addresses from private 10. space.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-f', '--file', default=None, help='The file to sanitize (default=stdin)')
    parser.add_argument('-o', '--output', default='/dev/stdout', help='The file to write output to (default=stdout)')
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)8s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    if args.file is None:
        logging.warning('Reading data on stdin, if manually typing entries on a terminal separate with newlines')
        args.file = '/dev/stdin'
    FileSanitizer(in_file=args.file, out_file=args.output).sanitize()

if __name__ == '__main__':
    main()
