#!/usr/local/bin/python
# encoding: utf-8
"""
*Given a location in the sky, check SDSS to see if the survey covered that region.*

:Author:
    David Young

:Date Created:
    June 29, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
import time
os.environ['TERM'] = 'vt100'
import requests
from fundamentals import tools
from astrocalc.coords import unit_conversion


# OR YOU CAN REMOVE THE CLASS BELOW AND ADD A WORKER FUNCTION ... SNIPPET TRIGGER BELOW
# xt-worker-def

class check_coverage():
    """
    *The worker class for the check_coverage module*

    **Key Arguments:**
        - ``log`` -- python logger
        - ``raDeg`` -- ra in decimal degrees
        - ``decDeg`` -- dec in decimal degrees
        - ``url`` -- the SDSS URL to ping (DR12 is the default)

    **Usage:**

        To test whether or not a location in the sky has been covered by the SDSS survey:

        .. code-block:: python 

            from sloancone import check_coverage
            # covered = True | False | 999 (i.e. not sure)
            covered = check_coverage(
                log=log,
                ra=122.3343,
                dec=45.34343
            ).get()  

            print covered

            # OUTPUT: True

        Coordinates can also be given in sexegesimal format:

        .. code-block:: python 

            from sloancone import check_coverage
            covered = check_coverage(
                log=log,
                ra="12:45:4.45466",
                dec="-25:22:34.3434"
            ).get()

            print covered

            # OUTPUT: False
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

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

        # 2. @flagged: what are the default attrributes each object could have? Add them to variable attribute set here
        # Variable Data Atrributes

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

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

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """
        *get the check_coverage object*

        **Return:**
            - ``check_coverage``

        .. todo::

            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        match = self._query_sdss()

        self.log.info('completed the ``get`` method')
        return match

    def _query_sdss(
            self):
        """* query sdss*

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_query_sdss`` method')

        raDeg = float(self.raDeg)
        decDeg = float(self.decDeg)

        raUpper = raDeg + 0.002
        raLower = raDeg - 0.002
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
        except Exception, e:
            self.log.error(
                "could not determine whether object is in SDSS DR12 footprint - failed with this error %s: " %
                (str(e),))
            return -1

        self.log.debug('result: %s' % (result,))

        if "No objects have been found" in result or "No entries have been found" in result:
            match = False
            print "This location %(raDeg)s, %(decDeg)s is NOT in the SDSS footprint" % locals()
        elif "cornsilk" in result or "Your query output" in result:
            match = True
            print "This location %(raDeg)s, %(decDeg)s IS in the SDSS footprint" % locals()
        elif "minute" in result:
            match = 999
            print "Not sure if location %(raDeg)s, %(decDeg)s in SDSS, try again shortly" % locals()
            print result
        else:
            match = 999
            print "Not sure if location %(raDeg)s, %(decDeg)s in SDSS, here's the resulting HTML:" % locals()
            print result

        time.sleep(1)

        self.log.debug('sdss match: %s' % (match,))

        self.log.info('completed the ``_query_sdss`` method')
        return match

    # use the tab-trigger below for new method
    def _query(
        self,
        sql,
        url,
        fmt,
        log
    ):
        """* query*

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python 

                usage code 

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_query`` method')

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

        self.log.info('completed the ``_query`` method')
        return response.content

    # use the tab-trigger below for new method
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

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx
