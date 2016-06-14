#!/usr/local/bin/python
# encoding: utf-8
"""
*Do a conesearch of sdss*

:Author:
    David Young

:Date Created:
    December 2, 2014

.. todo::
    

Usage:
    sloancone [-n] [(-f <outputFormat>)] [(-t <galaxyType>)] <ra> <dec> <arcsecRadius>

    -h, --help            show this help message
    -n, --nearest         show closest match only
    -f, --format          which format to output (csv, human)
    -t, --galaxyType      which galaxies to search (all, specz or photoz)
"""
################# GLOBAL IMPORTS ####################
import sys
import os
import readline
import glob
from time import sleep
from docopt import docopt
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython.csvtools import python_list_of_dictionaries_to_csv
from fundamentals import tools, times


def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when ``cone_search_sdss`` is run as a single script from the cl, or when installed as a cl command*
    """
    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="WARNING",
        options_first=True
    )
    arguments, settings, log, dbConn = su.setup()

    # tab completion for raw_input
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tab_complete)

    # unpack remaining cl arguments using `exec` to setup the variable names
    # automatically
    for arg, val in arguments.iteritems():
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        if isinstance(val, str) or isinstance(val, unicode):
            exec(varname + " = '%s'" % (val,))
        else:
            exec(varname + " = %s" % (val,))
        if arg == "--dbConn":
            dbConn = val
        log.debug('%s = %s' % (varname, val,))

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cone_search_sdss AT %s' %
        (startTime,))

    # set options interactively if user requests
    # if interactiveFlag:
    # x-raw-input
    # x-boolean-raw-input
    #     pass

    if not outputFormat:
        outputFormat = "human"

    # call the worker function
    search = cone_search_sdss(
        log=log,
        ra=ra,
        dec=dec,
        searchRadius=float(arcsecRadius),
        nearest=nearestFlag,
        outputFormat=outputFormat,
        galaxyType=galaxyType
    )
    results = search.get()

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cone_search_sdss AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return

###################################################################
# CLASSES                                                         #
###################################################################


class cone_search_sdss():

    """
    *The worker class for the cone_search_sdss module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``ra`` -- ra in sexigesimal or decimal degrees
        - ``dec`` -- dec in sexigesimal or decimal degrees
        - ``searchRadius`` -- search radius in arcsecs
        - ``nearest`` -- show closest match only
        - ``outputFormat`` -- output format (table or csv)

    .. todo::

    """

    # Initialisation
    def __init__(
            self,
            log,
            ra,
            dec,
            searchRadius,
            nearest,
            outputFormat="table",
            galaxyType="all"
    ):
        from . import sdss_square_search
        self.log = log
        log.debug("instansiating a new 'cone_search_sdss' object")
        self.ra = ra
        self.dec = dec
        self.searchRadius = searchRadius
        self.nearest = nearest
        self.outputFormat = outputFormat
        self.galaxyType = galaxyType
        # xt-self-arg-tmpx

        # Initial Actions
        # perform the initail square search
        squareSearch = sdss_square_search(
            log=self.log,
            ra=self.ra,
            dec=self.dec,
            searchRadius=self.searchRadius,
            galaxyType=self.galaxyType
        )
        self.squareResults = squareSearch.get()

        return None

    def close(self):
        del self
        return None

    # Method Attributes
    def get(self):
        """
        *get the cone_search_sdss object*

        **Return:**
            - ``cone_search_sdss``

        .. todo::

        """
        self.log.info('starting the ``get`` method')

        # sort results by angular separation
        from operator import itemgetter
        results = list(self.squareResults)
        results = sorted(
            results, key=itemgetter('separation_arcsec'), reverse=True)

        # order of results
        headers = ["sdss_name", "type", "ra", "dec", "specz", "specz_err", "photoz",
                   "photoz_err", "separation_arcsec", "separation_north_arcsec", "separation_east_arcsec"]

        import collections
        orderDict = collections.OrderedDict(sorted({}.items()))

        # filter out results greater than the search radius
        filteredResults = []
        for row in results:
            if row["separation_arcsec"] < self.searchRadius:
                orderDict = collections.OrderedDict(sorted({}.items()))
                for h in headers:
                    if h in row.keys():
                        orderDict[h] = row[h]
                filteredResults.append(orderDict)
            else:
                continue
        if self.nearest and len(filteredResults):
            orderDict = collections.OrderedDict(sorted({}.items()))
            for h in headers:
                if h in filteredResults[0].keys():
                    orderDict[h] = row[h]
            filteredResults = [orderDict]
            # filteredResults = [filteredResults[0]]

        if not len(filteredResults):
            orderDict = collections.OrderedDict(sorted({}.items()))
            for h in headers:
                if self.galaxyType == "all" or (self.galaxyType == "specz" and h not in ["photoz_err", "photoz"]) or (self.galaxyType == "photoz" and h not in ["specz", "specz_err"]):
                    orderDict[h] = ""
            filteredResults = [orderDict]

        # pretty format print
        if self.outputFormat == "csv":
            csvType = "machine"
        else:
            csvType = "human"
        results = python_list_of_dictionaries_to_csv(
            log=self.log,
            datalist=filteredResults,
            csvType=csvType
        )
        print results

        # sdss only allows 60 hits per minute
        sleep(1)

        self.log.info('completed the ``get`` method')
        return results

    # xt-class-method


if __name__ == '__main__':
    main()
