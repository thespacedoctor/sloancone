sloancone 
=========================

*SDSS conesearching tools via the CL. Pull down conesearch results, or simply check whether or not a location in the sky has been covered by SDSS.*.

Usage
======

.. code-block:: bash 
   
    sloancone search [-n] [(-f <outputFormat>)] [(-t <galaxyType>)] <ra> <dec> <arcsecRadius>
    sloancone covered <ra> <dec>

    COMMANDS
    ========
    search                do a conesearch and report the resulting matches
    covered               test whether or not a location in the sky was covered by SDSS

    -h, --help            show this help message
    -n, --nearest         show closest match only
    -f, --format          which format to output (csv, table). Default table
    -t, --galaxyType      which galaxies to search (None, all, specz or photoz). Default None, i.e. return galaxies and stars
    
Documentation
=============

Documentation for sloancone is hosted by `Read the Docs <http://sloancone.readthedocs.org/en/stable/>`__ (last `stable version <http://sloancone.readthedocs.org/en/stable/>`__ and `latest version <http://sloancone.readthedocs.org/en/latest/>`__).

Installation
============

The easiest way to install sloancone us to use ``pip``:

.. code:: bash

    pip install sloancone

Or you can clone the `github repo <https://github.com/thespacedoctor/sloancone>`__ and install from a local version of the code:

.. code:: bash

    git clone git@github.com:thespacedoctor/sloancone.git
    cd sloancone
    python setup.py install

To upgrade to the latest version of sloancone use the command:

.. code:: bash

    pip install sloancone --upgrade


Development
-----------

If you want to tinker with the code, then install in development mode.
This means you can modify the code from your cloned repo:

.. code:: bash

    git clone git@github.com:thespacedoctor/sloancone.git
    cd sloancone
    python setup.py develop

`Pull requests <https://github.com/thespacedoctor/sloancone/pulls>`__
are welcomed!


Issues
------

Please report any issues
`here <https://github.com/thespacedoctor/sloancone/issues>`__.

License
=======

Copyright (c) 2016 David Young

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

