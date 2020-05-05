Command-Line Usage
==================

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
    
