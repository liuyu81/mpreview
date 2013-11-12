mpreview.py
===========

python script for rendering metapost graph.


usage
-----
`mpreview` scans the given metapost graph (`.mp`) for the list of all figures and place each of them in an indiviaual page of the generated (multi-page) postscript file (`.ps`).

    $ python mpreview.py sample.mp

post-processing
---------------
When the postscript file is available, one can extract individual pages through, say, [`psselect`](http://knackered.org/angus/psutils/psselect.html), and convert them into standalone graphs such as embedded postscript (`.eps`), i.e.,

    $ psselect -p1 sample.ps fig01.ps
    $ ps2eps --ignoreBB fig01.ps


dependencies
------------

* latex toolchain (`mpost` / `latex` / `dvips`)
* python (2.6+, 3.x)
* which.py (optional)
