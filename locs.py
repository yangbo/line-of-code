# This is a Python script to count line of code under specified directory.
# Borrow from https://code.activestate.com/recipes/580709-lines-of-code-loc/
#
# Author: Bob Yang
# Create Time: 2022-05-06
# Description:
#   Basic Lines-Of-Code counter in Python source files, reporting the
#   number of blank, comment and source code lines and total number of
#   lines in all java files scanned.

# Usage example:

# % python locs.py -rec ./Projects
# 343 *.java files in: ['D:\\projects\\Projects']
# 5868 blank (10.6%), 12843 comment (23.2%), 36728 source (66.2%), 49571 source+comment (89.4%), 55439 total lines
# (0.241 secs, 229978 lines/sec)
# Extract all src into ./all_src.txt

# Scan multiple directory
# % python3 locs.py -rec ./Projects ./Projects2
# 343 *.java files in: ['D:\\projects\\Projects']
# 5868 blank (10.6%), 12843 comment (23.2%), 36728 source (66.2%), 49571 source+comment (89.4%), 55439 total lines
# (0.241 secs, 229978 lines/sec)
# Extract all src into ./all_src.txt

# Statistic line of code and extract all java source code to one big file './all_src.java'
# % python locs.py -rec -ext ./Projects
# 343 *.java files in: ['D:\\projects\\Projects']
# 5868 blank (10.6%), 12843 comment (23.2%), 36728 source (66.2%), 49571 source+comment (89.4%), 55439 total lines
# (0.241 secs, 229978 lines/sec)
# Extract all src into ./all_src.txt

# % python3 locs.py -h
# usage: locs.py [-help] [-recurse] [-extract] [-verbose] <file_or_dir_name> ...

# Tested with 64-bit Python 3.6 on Windows 10 only.

from glob import iglob
from os.path import basename, exists, isdir, join
from time import time

__all__ = ('Loc',)
__version__ = '22.05.06'


class Loc(object):
    """Lines-Of-Code accumulator.
    """
    blank = 0
    comment = 0
    files = 0
    source = 0
    ext = '.java'
    all_src_file = './all_src.txt'
    _time0 = 0

    _recurse = False  # process dirs
    _verbose = False  # print details
    _extract = False  # extract all code into one big source file named './all-src.txt'

    def __init__(self, recurse=False, verbose=False, extract=False):
        self._recurse = recurse
        self._verbose = verbose
        self._time0 = time()
        self._extract = extract
        self.big_file = None
        self.scan_dirs = []

    def __str__(self):
        s = time() - self._time0
        n = self.source + self.comment + self.blank
        p = int(n / s) if n > s > 0 else '-'
        t = ['%s *%s files in: %s' % (self.files, self.ext, self.scan_dirs),
             self._bcst(self.blank, self.comment, self.source),
             '(%.3f secs, %s lines/sec)' % (s, p)]
        rep = '\n'.join(t)
        if self._extract and self.big_file:
            rep += f"\nExtract all src into {self.big_file.name}"
        return rep

    @staticmethod
    def _bcst(blank, comment, source):
        t, n = [], blank + comment + source
        for a, v in (('blank', blank),
                     ('comment', comment),
                     ('source', source),
                     ('source+comment', source+comment),
                     ):
            p = ' (%.1f%%)' % ((v * 100.0) / n,) if n > 0 else ''
            t.append('%s %s%s' % (v, a, p))
        t.append('%s total lines' % (n,))
        return ', '.join(t)

    def adir(self, name):
        """Process a directory.
        """
        if self._recurse:
            if self._verbose:
                print(' dir %s: %s' % (name, '...'))
                b, c, s = self.blank, self.comment, self.source
                self.aglob(join(name, '*'))
                b = self.blank - b
                c = self.comment - c
                s = self.source - s
                t = name, self._bcst(b, c, s)
                print(' dir %s: %s' % t)
            else:
                self.aglob(join(name, '*'))

    def afile(self, name):
        """Process a file.
        """
        if name.endswith(self.ext) and exists(name):
            b = c = s = 0
            in_comment = False
            with open(name, 'rb') as f:
                for t in f.readlines():
                    ts = t.strip()
                    if not ts:
                        b += 1
                    # for java comments is like '/* ... */' or //
                    # elif t.startswith(b'#'):  # Python 3+
                    #     c += 1
                    elif ts.startswith(b"//"):  # Python 3+
                        c += 1
                    elif ts.startswith(b"/*"):
                        c += 1
                        in_comment = True
                    elif ts.endswith(b"*/"):
                        c += 1
                        in_comment = False
                    # must be placed on last to let '*/' have chance to close comment status
                    elif in_comment:
                        c += 1
                    else:
                        s += 1
                        self.append_src(t.rstrip())

            self.blank += b
            self.comment += c
            self.source += s
            self.files += 1
            if self._verbose:
                t = self.files, name, self._bcst(b, c, s)
                print('file %s %s: %s' % t)

    def aglob(self, wild):
        """Process a possible wildcard.
        """
        for t in iglob(wild):
            if isdir(t):
                self.adir(t)
            else:
                self.afile(t)

    def open_big_src(self):
        self.big_file = open(Loc.all_src_file, 'wb') if self._extract else None

    def append_src(self, t):
        """Append line to big src file"""
        if self.big_file:
            self.big_file.write(t)
            self.big_file.write(b'\n')

    def close_src(self):
        """close big src file"""
        if self.big_file:
            self.big_file.close()


if __name__ == '__main__':

    import sys

    argv0 = basename(sys.argv[0])

    loc = Loc()
    try:
        for arg in sys.argv[1:]:
            if not arg.startswith('-'):
                loc.scan_dirs.append(arg)
                loc.aglob(arg)

            elif '-help'.startswith(arg):
                print('usage: %s [-help] [-recurse] [-verbose] [-extract] <file_or_dir_name> ...' % (argv0,))
                sys.exit(0)
            elif '-recurse'.startswith(arg):
                loc._recurse = True
            elif '-extract'.startswith(arg):
                loc._extract = True
                loc.open_big_src()
            elif '-verbose'.startswith(arg):
                loc._verbose = True
            elif arg != '--':
                print('%s: invalid option: %r' % (argv0, arg))
                sys.exit(1)
        loc.close_src()

    except KeyboardInterrupt:
        print('')

    print('%s' % (loc,))
