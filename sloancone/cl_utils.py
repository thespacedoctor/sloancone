#!/usr/bin/env python
# encoding: utf-8
"""
Documentation for sloancone can be found here: http://sloancone.readthedocs.org

Usage:
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
"""
from __future__ import print_function
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
from docopt import docopt
from fundamentals import tools, times
from subprocess import Popen, PIPE, STDOUT

def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]

def main(arguments=None):
    """
    *The main function used when `cl_utils.py` is run as a single script from the cl, or when installed as a cl command*
    """
    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="WARNING",
        options_first=False,
        projectName="sloancone",
        defaultSettingsFile=True
    )
    arguments, settings, log, dbConn = su.setup()

    # tab completion for raw_input
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tab_complete)

    # UNPACK REMAINING CL ARGUMENTS USING `EXEC` TO SETUP THE VARIABLE NAMES
    # AUTOMATICALLY
    a = {}
    for arg, val in list(arguments.items()):
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        a[varname] = val
        if arg == "--dbConn":
            dbConn = val
            a["dbConn"] = val
        log.debug('%s = %s' % (varname, val,))

    search = a["search"]
    covered = a["covered"]
    nearest = a["nearest"]
    fformat = a["format"]
    galaxyType = a["galaxyType"]

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cl_utils.py AT %s' %
        (startTime,))

    # set options interactively if user requests
    if "interactiveFlag" in a and a["interactiveFlag"]:

        # load previous settings
        moduleDirectory = os.path.dirname(__file__) + "/resources"
        pathToPickleFile = "%(moduleDirectory)s/previousSettings.p" % locals()
        try:
            with open(pathToPickleFile):
                pass
            previousSettingsExist = True
        except:
            previousSettingsExist = False
        previousSettings = {}
        if previousSettingsExist:
            previousSettings = pickle.load(open(pathToPickleFile, "rb"))

        # x-raw-input
        # x-boolean-raw-input
        # x-raw-input-with-default-value-from-previous-settings

        # save the most recently used requests
        pickleMeObjects = []
        pickleMe = {}
        theseLocals = locals()
        for k in pickleMeObjects:
            pickleMe[k] = theseLocals[k]
        pickle.dump(pickleMe, open(pathToPickleFile, "wb"))

    if a["init"]:
        from os.path import expanduser
        home = expanduser("~")
        filepath = home + "/.config/sloancone/sloancone.yaml"
        try:
            cmd = """open %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        try:
            cmd = """start %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        return

    # CALL FUNCTIONS/OBJECTS
    # CALL THE WORKER FUNCTION
    if search:
        cs = cone_search(
            log=log,
            ra=ra,
            dec=dec,
            searchRadius=float(arcsecRadius),
            nearest=nearestFlag,
            outputFormat=outputFormat,
            galaxyType=galaxyType
        )
        results = cs.get()
        print(results)

    # COVERED = TRUE | FALSE | 999 (I.E. NOT SURE)
    if covered:
        check = check_coverage(
            log=log,
            ra=ra,
            dec=dec
        ).get()
        print(check)

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return

if __name__ == '__main__':
    main()
