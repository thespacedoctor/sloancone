#!/usr/local/bin/python
# encoding: utf-8
"""
*Perform a conesearch of SDSS at a given location with a specified search radius*

:Author:
    David Young

:Date Created:
    June 29, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
from time import sleep
os.environ['TERM'] = 'vt100'
from fundamentals import tools, times
from fundamentals.files import list_of_dictionaries_to_csv


class cone_search():
    """
    *The worker class for the cone_search module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``ra`` -- ra in sexigesimal or decimal degrees
        - ``dec`` -- dec in sexigesimal or decimal degrees
        - ``searchRadius`` -- search radius in arcsecs
        - ``nearest`` -- show closest match only
        - ``outputFormat`` -- output format (table or csv)

    **Usage:**
        .. todo::

            - add usage info
            - create a sublime snippet for usage

        .. code-block:: python 

            from sloancone.cone_search import cone_search
            csResults = cone_search(
                log=log,
                ra="12:45:23.2323",
                dec="30.343122",
                searchRadius=60.,
                nearest=False,
                outputFormat="table",
                galaxyType="all"
            ).get()

            print csResults 

        This code outputs the following:

        .. code-block:: plain

            +---------------------------+---------+-----------+----------+--------+------------+---------+-------------+--------------------+--------------------------+-------------------------+
            | sdss_name                 | type    | ra        | dec      | specz  | specz_err  | photoz  | photoz_err  | separation_arcsec  | separation_north_arcsec  | separation_east_arcsec  |
            +---------------------------+---------+-----------+----------+--------+------------+---------+-------------+--------------------+--------------------------+-------------------------+
            | SDSS J124521.85+302046.0  | galaxy  | 191.3410  | 30.3461  | None   | None       | 0.3443  | 0.1007      | 20.8856            | 10.8005                  | -17.8762                |
            | SDSS J124522.39+302100.4  | galaxy  | 191.3433  | 30.3501  | None   | None       | 0.3172  | 0.0901      | 27.4400            | 25.2212                  | -10.8094                |
            | SDSS J124522.08+302007.4  | galaxy  | 191.3420  | 30.3354  | None   | None       | 0.3672  | 0.1133      | 31.4720            | -27.7701                 | -14.8090                |
            | SDSS J124524.95+302105.7  | galaxy  | 191.3540  | 30.3516  | None   | None       | 0.2721  | 0.0311      | 37.8154            | 30.5314                  | 22.3124                 |
            | SDSS J124524.57+302000.2  | galaxy  | 191.3524  | 30.3334  | None   | None       | 0.4181  | 0.0965      | 39.1194            | -35.0377                 | 17.3979                 |
            | SDSS J124519.23+302042.5  | galaxy  | 191.3302  | 30.3452  | None   | None       | 0.2347  | 0.0749      | 52.2402            | 7.3538                   | -51.7200                |
            | SDSS J124521.36+301943.9  | galaxy  | 191.3390  | 30.3289  | None   | None       | 0.1978  | 0.0699      | 56.7372            | -51.3133                 | -24.2086                |
            | SDSS J124519.89+302115.9  | galaxy  | 191.3329  | 30.3544  | None   | None       | 0.9105  | 0.0821      | 59.3096            | 40.6688                  | -43.1703                |
            +---------------------------+---------+-----------+----------+--------+------------+---------+-------------+--------------------+--------------------------+-------------------------+

        To return results in a traditional CSV format:

        .. code-block:: python 

            from sloancone.cone_search import cone_search
            csResults = cone_search(
                log=log,
                ra="112.233432",
                dec="15:34:31.22",
                searchRadius=60.,
                nearest=True,
                outputFormat="csv",
                galaxyType="all"
            ).get()

            print csResults

        This code outputs the following:

        .. code-block:: plain

            sdss_name,type,ra,dec,specz,specz_err,photoz,photoz_err,separation_arcsec,separation_north_arcsec,separation_east_arcsec
            SDSS J072855.31+153454.6,galaxy,112.2305,15.5818,,,0.7211,0.0719,25.5528,23.4273,-10.2034

        To filter the result be a redshift type (``specz`` or ``photoz``)

        .. code-block:: python 

            from sloancone.cone_search import cone_search
            csResults = cone_search(
                log=log,
                ra="12:45:23.2323",
                dec="30.343122",
                searchRadius=600.,
                nearest=False,
                outputFormat="table",
                galaxyType="specz"
            ).get()

            print csResults 

        This code outputs the following:

        .. code-block:: plain

           +---------------------------+---------+-----------+----------+---------+------------+--------------------+--------------------------+-------------------------+
           | sdss_name                 | type    | ra        | dec      | specz   | specz_err  | separation_arcsec  | separation_north_arcsec  | separation_east_arcsec  |
           +---------------------------+---------+-----------+----------+---------+------------+--------------------+--------------------------+-------------------------+
           | SDSS J124540.06+301923.0  | galaxy  | 191.4169  | 30.3231  | 0.3629  | 0.0002     | 229.5373           | -72.2170                 | 217.8809                |
           | SDSS J124534.33+301624.6  | galaxy  | 191.3931  | 30.2735  | 0.2609  | 0.0000     | 288.8809           | -250.5509                | 143.7929                |
           | SDSS J124512.46+301502.3  | galaxy  | 191.3019  | 30.2506  | 0.5810  | 0.0002     | 360.9520           | -332.9018                | -139.5091               |
           | SDSS J124512.46+301502.3  | galaxy  | 191.3019  | 30.2506  | 0.5809  | 0.0002     | 360.9520           | -332.9018                | -139.5091               |
           | SDSS J124544.87+302435.6  | galaxy  | 191.4370  | 30.4099  | 0.2254  | 0.0000     | 369.1276           | 240.3704                 | 280.1380                |
           | SDSS J124547.42+302532.8  | galaxy  | 191.4476  | 30.4258  | 0.4473  | 0.0001     | 431.9371           | 297.5669                 | 313.0872                |
           | SDSS J124454.28+301700.6  | galaxy  | 191.2262  | 30.2835  | 0.2599  | 0.0000     | 431.9447           | -214.5446                | -374.8959               |
           | SDSS J124558.38+301904.7  | galaxy  | 191.4933  | 30.3180  | 0.1767  | 0.0000     | 463.9608           | -90.4407                 | 455.0606                |
           | SDSS J124544.31+301417.7  | galaxy  | 191.4347  | 30.2383  | 0.3632  | 0.0000     | 465.9112           | -377.4610                | 273.1236                |
           | SDSS J124543.24+301319.2  | galaxy  | 191.4302  | 30.2220  | 0.0669  | 0.0000     | 507.2387           | -436.0132                | 259.1979                |
           | SDSS J124557.99+302437.8  | galaxy  | 191.4916  | 30.4105  | 0.4469  | 0.0002     | 511.0694           | 242.6379                 | 449.7987                |
           | SDSS J124602.33+302241.3  | galaxy  | 191.5097  | 30.3782  | 0.4365  | 0.0001     | 521.5570           | 126.1410                 | 506.0733                |
           | SDSS J124602.33+302241.3  | galaxy  | 191.5097  | 30.3782  | 0.4365  | 0.0001     | 521.5570           | 126.1410                 | 506.0733                |
           | SDSS J124605.96+301913.6  | galaxy  | 191.5248  | 30.3205  | 0.1761  | 0.0000     | 559.2108           | -81.5693                 | 553.2298                |
           | SDSS J124439.37+301949.6  | galaxy  | 191.1640  | 30.3305  | 0.2219  | 0.0000     | 569.6536           | -45.5571                 | -567.8291               |
           | SDSS J124439.37+301949.6  | galaxy  | 191.1640  | 30.3305  | 0.2220  | 0.0000     | 569.6536           | -45.5571                 | -567.8291               |
           | SDSS J124538.93+302945.0  | galaxy  | 191.4122  | 30.4958  | 0.2252  | 0.0000     | 586.1380           | 549.8198                 | 203.1158                |
           | SDSS J124450.57+301333.8  | galaxy  | 191.2107  | 30.2261  | 0.4373  | 0.0001     | 597.1297           | -421.4088                | -423.0586               |
           | SDSS J124450.57+301333.8  | galaxy  | 191.2107  | 30.2261  | 0.4377  | 0.0001     | 597.1297           | -421.4088                | -423.0586               |
           +---------------------------+---------+-----------+----------+---------+------------+--------------------+--------------------------+-------------------------+

        Finally, we can also search for stars and galaxies by selecting ``galaxyType=False``:

        .. code-block:: python 

            from sloancone.cone_search import cone_search
            csResults = cone_search(
                log=log,
                ra="12:45:23.2323",
                dec="30.343122",
                searchRadius=60.,
                nearest=False,
                outputFormat="table",
                galaxyType=False
            ).get()

            print csResults

        .. code-block:: plain

            +---------------------------+---------+-----------+----------+----------+------------+---------+-------------+--------------------+--------------------------+-------------------------+
            | sdss_name                 | type    | ra        | dec      | specz    | specz_err  | photoz  | photoz_err  | separation_arcsec  | separation_north_arcsec  | separation_east_arcsec  |
            +---------------------------+---------+-----------+----------+----------+------------+---------+-------------+--------------------+--------------------------+-------------------------+
            | SDSS J124521.85+302046.0  | galaxy  | 191.3410  | 30.3461  | None     | None       | 0.3443  | 0.1007      | 20.8856            | 10.8005                  | -17.8762                |
            | SDSS J124524.92+302042.7  | star    | 191.3539  | 30.3452  | None     | None       | None    | None        | 23.2234            | 7.5490                   | 21.9622                 |
            | SDSS J124521.68+302016.9  | star    | 191.3403  | 30.3380  | -0.0001  | 0.0000     | None    | None        | 27.1558            | -18.2960                 | -20.0672                |
            | SDSS J124522.39+302100.4  | galaxy  | 191.3433  | 30.3501  | None     | None       | 0.3172  | 0.0901      | 27.4400            | 25.2212                  | -10.8094                |
            | SDSS J124522.08+302007.4  | galaxy  | 191.3420  | 30.3354  | None     | None       | 0.3672  | 0.1133      | 31.4720            | -27.7701                 | -14.8090                |
            | SDSS J124524.95+302105.7  | galaxy  | 191.3540  | 30.3516  | None     | None       | 0.2721  | 0.0311      | 37.8154            | 30.5314                  | 22.3124                 |
            | SDSS J124524.57+302000.2  | galaxy  | 191.3524  | 30.3334  | None     | None       | 0.4181  | 0.0965      | 39.1194            | -35.0377                 | 17.3979                 |
            | SDSS J124521.67+301955.1  | star    | 191.3403  | 30.3320  | None     | None       | None    | None        | 44.8763            | -40.0699                 | -20.2060                |
            | SDSS J124526.25+302103.7  | star    | 191.3594  | 30.3511  | None     | None       | None    | None        | 48.4191            | 28.5417                  | 39.1124                 |
            | SDSS J124519.23+302042.5  | galaxy  | 191.3302  | 30.3452  | None     | None       | 0.2347  | 0.0749      | 52.2402            | 7.3538                   | -51.7200                |
            | SDSS J124521.36+301943.9  | galaxy  | 191.3390  | 30.3289  | None     | None       | 0.1978  | 0.0699      | 56.7372            | -51.3133                 | -24.2086                |
            | SDSS J124522.15+301937.9  | star    | 191.3423  | 30.3272  | None     | None       | None    | None        | 58.9703            | -57.2852                 | -13.9962                |
            | SDSS J124519.89+302115.9  | galaxy  | 191.3329  | 30.3544  | None     | None       | 0.9105  | 0.0821      | 59.3096            | 40.6688                  | -43.1703                |
            | SDSS J124526.04+301947.9  | star    | 191.3585  | 30.3300  | None     | None       | None    | None        | 59.6986            | -47.3115                 | 36.4080                 |
            | SDSS J124524.95+302130.6  | star    | 191.3540  | 30.3585  | None     | None       | None    | None        | 59.7431            | 55.4049                  | 22.3502                 |
            +---------------------------+---------+-----------+----------+----------+------------+---------+-------------+--------------------+--------------------------+-------------------------+
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
            galaxyType=False
    ):
        from . import sdss_square_search
        self.log = log
        log.debug("instansiating a new 'cone_search' object")
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

    def get(self):
        """
        *get the cone_search object*

        **Return:**
            - ``cone_search``

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
            if float(row["separation_arcsec"]) < self.searchRadius:
                orderDict = collections.OrderedDict(sorted({}.items()))
                for h in headers:
                    if h in row.keys():
                        orderDict[h] = row[h]
                filteredResults.append(orderDict)
            else:
                pass

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
                if self.galaxyType == "all" or self.galaxyType == False or (self.galaxyType == "specz" and h not in ["photoz_err", "photoz"]) or (self.galaxyType == "photoz" and h not in ["specz", "specz_err"]):
                    orderDict[h] = ""
            filteredResults = [orderDict]

        # pretty format print
        if self.outputFormat == "csv":
            csvType = "machine"
        else:
            csvType = "human"

        results = list_of_dictionaries_to_csv(
            log=self.log,
            datalist=list(reversed(filteredResults)),
            csvType=csvType  # machine | human
        )

        # sdss only allows 60 hits per minute
        sleep(1)

        self.log.info('completed the ``get`` method')
        return results
