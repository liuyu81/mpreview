#!/usr/bin/env python
# $Id: mpreview.py,v 1.4 2011-03-04 01:13:58 liuyu Exp $

import re
import os
import sys

try:
    from which import which
except ImportError as e:
    def which(s):
        return s
    pass

MPOST = [which("mpost"), "--tex=latex", "-interaction=batchmode",
         "%(input)s.mp", ]
LATEX = [which("latex"), "%(input)s.tex", ]
DVIPS = [which("dvips"), "%(input)s.dvi", ]


def get_figure_list(mp):
    lof = []
    for line in mp:
        m = re.match("\s*beginfig\(\s*(\d+)\s*\)\s*;?\s*", line)
        if not m:
            continue
        lof.append(m.groups(1)[0])
    return lof


def get_tex_file(fn, fglist):
    tex = "%s"
    for i in fglist:
        fig = ".".join([fn, i])
        tex = tex % "\\includegraphics{" + fig + "}\n\\newpage\n%s"""
    tex = tex % ""
    tex = """\\documentclass{article}
\\pagestyle{empty}
\\usepackage{graphicx}
\\usepackage[margin=1cm]{geometry}
\\begin{document}
\\centering
%s\\end{document}""" % tex
    return tex


def do_mpost(fn):
    status = os.system(" ".join(MPOST) % {'input': fn})
    if status != 0:
        return False
    return True


def do_latex(fn):
    status = os.system(" ".join(LATEX) % {'input': fn})
    if status != 0:
        return False
    return True


def do_dvips(fn):
    status = os.system(" ".join(DVIPS) % {'input': fn})
    if status != 0:
        return False
    return True


def do_clean(prefix, extra=["mptextmp.mp", "mptextmp.mpx", "mpxerr.tex"]):
    for ext in ["tex", "aux", "log", "dvi", "mpx"]:
        fn = ".".join([prefix, ext])
        if os.access(fn, os.F_OK | os.W_OK):
            os.remove(fn)
    for fn in extra:
        if os.access(fn, os.F_OK | os.W_OK):
            os.remove(fn)
    return True


def main(args):
    # prepare argument parser
    import argparse
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-v] [-l] figure.mp\n       %(prog)s -h",
        add_help=False,
        epilog="author: LIU Yu <liuyu@opencps.net>",
        description="python script for rendering metapost graph")
    parser.add_argument(
        dest='fn', metavar='figure.mp', type=str, nargs=argparse.OPTIONAL,
        help="metapost graph")
    parser.add_argument(
        '-v', '--verbose', dest='verbose', action='store_true', default=False,
        help="verbose mode")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-l', '--list', dest='lof', action='store_true', default=False,
        help="list all figures")
    group.add_argument(
        '-h', '--help', dest='help', action='store_true', default=False,
        help="show help message")
    cookbook = parser.parse_args(args)

    # show help message
    if not cookbook.fn:
        sys.stdout.write(parser.format_help())
        return os.EX_OK

    # load metapost source
    tup = cookbook.fn.strip().split('.')
    if len(tup) > 1 and tup[-1] == "mp":
        tup = tup[:-1]
    fn = ".".join(tup)
    mpfile = ".".join([fn, "mp"])
    texfile = ".".join([fn, "tex"])
    dvifile = ".".join([fn, "dvi"])

    if not os.access(mpfile, os.F_OK | os.R_OK):
        sys.stderr.write("file missing or inaccessible\n")
        return os.EX_OK

    f = open(mpfile, 'rb')
    lof = get_figure_list(f.readlines())
    f.close()

    # list all figures
    if cookbook.lof:
        for i in lof:
            sys.stdout.write(str(i))
            sys.stdout.write("\n")
        return os.EX_OK

    # render preview
    f = open(texfile, 'wb')
    f.write(get_tex_file(fn, lof))
    f.close()

    do_mpost(fn)
    do_latex(fn)
    do_dvips(fn)
    do_clean(fn)

    return os.EX_OK


if __name__ == "__main__":
    try:
        exitcode = main(sys.argv[1:])
    except SystemExit as e:
        exitcode = e
    except Exception as e:
        sys.stderr.write(str(e))
        exitcode = os.EX_SOFTWARE
    sys.exit(exitcode)
