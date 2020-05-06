#!/usr/local/bin/python
# encoding: utf-8
"""
*Given a location in the sky, check SDSS to see if the survey covered that region.*

:Author:
    David Young
"""
from __future__ import print_function
from builtins import str
from builtins import object
import sys
import os
import time
os.environ['TERM'] = 'vt100'
import requests
from fundamentals import tools
from astrocalc.coords import unit_conversion

class check_coverage(object):
    """
    *The worker class for the check_coverage module*

    **Key Arguments**

    - ``log`` -- python logger
    - ``raDeg`` -- ra in decimal degrees
    - ``decDeg`` -- dec in decimal degrees
    - ``url`` -- the SDSS URL to ping (DR12 is the default)
    

    **Usage**

    To test whether or not a location in the sky has been covered by the SDSS survey:

    ```python
    from sloancone import check_coverage
    # covered = True | False | 999 (i.e. not sure)
    covered = check_coverage(
        log=log,
        ra=122.3343,
        dec=45.34343
    ).get()  

    print(covered)

    # OUTPUT: True
    ```

    Coordinates can also be given in sexegesimal format:

    ```python
    from sloancone import check_coverage
    covered = check_coverage(
        log=log,
        ra="12:45:4.45466",
        dec="-25:22:34.3434"
    ).get()

    print(covered)

    # OUTPUT: False
    ```
    
    """
    # Initialisation

    def __init__(
            self,
            log,
            ra,
            dec,
            url="http://skyserver.sdss.org/dr12/en/tools/search/x_sql.aspx"
    ):
        self.log = log
        log.debug("instansiating a new 'check_coverage' object")
        self.ra = ra
        self.dec = dec
        self.url = url
        # xt-self-arg-tmpx

        # Initial Actions

        converter = unit_conversion(
            log=self.log
        )
        self.raDeg = converter.ra_sexegesimal_to_decimal(
            ra=ra
        )
        self.decDeg = converter.dec_sexegesimal_to_decimal(
            dec=dec
        )

        return None

    def get(self):
        """
        *get the check_coverage object*

        **Return**

        - ``check_coverage``
        
        """
        self.log.debug('starting the ``get`` method')

        match = self._query_sdss()

        self.log.debug('completed the ``get`` method')
        return match

    def _query_sdss(
            self):
        """* query sdss*
        """
        self.log.debug('starting the ``_query_sdss`` method')

        raDeg = float(self.raDeg)
        decDeg = float(self.decDeg)

        raUpper = raDeg + 0.02
        raLower = raDeg - 0.02
        declUpper = decDeg + 0.02
        declLower = decDeg - 0.02

        ################ >ACTION(S) ################
        sqlQuery = "SELECT TOP 1 rerun, camcol, field FROM PhotoObj WHERE ra BETWEEN %s and %s AND dec BETWEEN %s and %s" % (
            raLower, raUpper, declLower, declUpper,)
        self.log.debug('sqlQuery: %s' % (sqlQuery,))
        try:
            self.log.debug(
                "attempting to determine whether object is in SDSS DR12 footprint")
            result = self._query(
                sql=sqlQuery,
                url=self.url,
                fmt="html",
                log=self.log)
        except Exception as e:
            self.log.error(
                "could not determine whether object is in SDSS DR12 footprint - failed with this error %s: " %
                (str(e),))
            return -1

        self.log.debug('result: %s' % (result,))

        strResult = str(result)

        if "No objects have been found" in strResult or "No entries have been found" in strResult:
            match = False
            print(
                "This location %(raDeg)s, %(decDeg)s is NOT in the SDSS footprint" % locals())
        elif "cornsilk" in strResult or "Your query output" in strResult:
            match = True
            print(
                "This location %(raDeg)s, %(decDeg)s IS in the SDSS footprint" % locals())
        elif "minute" in strResult:
            match = 999
            print(
                "Not sure if location %(raDeg)s, %(decDeg)s in SDSS, try again shortly" % locals())
            print(strResult)
        else:
            match = 999
            print(
                "Not sure if location %(raDeg)s, %(decDeg)s in SDSS, here's the resulting HTML:" % locals())
            print(strResult)

        print("  See for yourself: http://skyserver.sdss.org/dr12/en/tools/chart/image.aspx?ra=%(raDeg)s&dec=%(decDeg)s&scale=0.8&opt=G&PhotoObjs=off&width=500&height=500" % locals())

        time.sleep(1)

        self.log.debug('sdss match: %s' % (match,))

        self.log.debug('completed the ``_query_sdss`` method')
        return match

    def _query(
        self,
        sql,
        url,
        fmt,
        log
    ):
        """* query*
        """
        self.log.debug('starting the ``_query`` method')

        try:
            response = requests.get(
                url=url,
                params={
                    "cmd": self._filtercomment(sql),
                    "format": fmt,
                },
                headers={
                    "Cookie": "ASP.NET_SessionId=d0fiwrodvk4rdf21gh3jzr3t; SERVERID=dsa003",
                },
            )
            # print('Response HTTP Status Code: {status_code}'.format(
            #     status_code=response.status_code))
            # print('Response HTTP Response Body: {content}'.format(
            #     content=response.content))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

        self.log.debug('completed the ``_query`` method')
        return response.content

    def _filtercomment(
            self,
            sql):
        "Get rid of comments starting with --"
        import os
        fsql = ''
        for line in sql.split('\n'):
            fsql += line.split('--')[0] + ' ' + os.linesep
        return fsql

    # use the tab-trigger below for new method
    # xt-class-method
