#!/usr/local/bin/python
# encoding: utf-8
"""
*Given a location and some other parameters, download an SDSS image of that location in the sky*

:Author:
    David Young

:Date Created:
    July 18, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from astrocalc.coords import unit_conversion


class image():
    """
    *The worker class for the image module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``ra`` -- right-ascension of the sky-location
        - ``dec`` -- declination of the sky-location
        - ``downloadDirectory`` -- directory to download the image stamp to. Default *./*
        - ``filename`` -- path to download the image stamp to. Default *"sdss_stamp.jpeg"*
        - ``grid`` -- include grid and scale in stamp. Default *True*
        - ``label`` -- label. Default *False*
        - ``photocat`` -- mark photometrical catalogued sources. Default *False*
        - ``speccat`` -- mark spectrscopical catalogued objects. Default *False*
        - ``invertColors`` -- invert the image stamp colors. Default *False*
        - ``arcminWidth`` -- the width of the image stamp in arcmin. Default *5*
        - ``pixelWidth`` -- the width of the image stamp in pixels. Default *500*

    **Usage:**

        Here's an example where we turn on all options before we download the image:

        .. code-block:: python

            from sloancone import image
            imagestamp = image(
                log=log,
                settings=settings,
                ra="179.689293428354",
                dec="-0.454379056007667",
                downloadDirectory="/tmp",
                filename="sdss_stamp.jpeg",
                grid=True,
                label=True,
                photocat=True,
                speccat=True,
                invertColors=True,
                arcminWidth=5,
                pixelWidth=500
            )
            imagestamp.get()

        This produces a stamp at ``/tmp/sdss_stamp.jpeg`` that looks like this:

        .. image:: https://i.imgur.com/2w4ipqr.png
            :width: 800px
            :alt: SDSS image stamp with all options turned on
    """
    # Initialisation

    def __init__(
            self,
            log,
            ra,
            dec,
            downloadDirectory="./",
            filename="sdss_stamp.jpeg",
            settings=False,
            grid=True,
            label=False,
            photocat=False,
            speccat=False,
            invertColors=False,
            arcminWidth=5,
            pixelWidth=500
    ):
        self.log = log
        log.debug("instansiating a new 'image' object")
        self.settings = settings
        self.ra = ra
        self.dec = dec
        self.filename = filename
        self.downloadDirectory = downloadDirectory
        self.grid = grid
        self.label = label
        self.photocat = photocat
        self.speccat = speccat
        self.invertColors = invertColors
        self.arcminWidth = arcminWidth
        self.pixelWidth = pixelWidth

        # xt-self-arg-tmpx

        # INITIAL ACTIONS
        # CHECK SDSS COVERAGE BEFORE DOWNLOAD ATTEMPT
        from check_coverage import check_coverage
        # covered = True | False | 999 (i.e. not sure)
        self.covered = check_coverage(
            log=log,
            ra=self.ra,
            dec=self.dec
        ).get()

        return None

    def get(self):
        """
        *download the image*
        """
        self.log.info('starting the ``get`` method')

        ra = self.ra
        dec = self.dec
        if self.covered == False or self.covered == 999 or self.covered == "999":
            return

        self._download_sdss_image()

        self.log.info('completed the ``get`` method')
        return

    def _download_sdss_image(
            self):
        """*download sdss image*
        """
        self.log.info('starting the ``_download_sdss_image`` method')

        opt = ""
        if self.grid:
            opt += "G"

        if self.label:
            opt += "L"

        if self.photocat:
            opt += "P"

        if self.speccat:
            opt += "S"

        if self.invertColors:
            opt += "I"

        if len(opt):
            opt = "opt=%(opt)s&" % locals()

        width = self.pixelWidth

        scale = (self.arcminWidth * 60.) / width

        converter = unit_conversion(
            log=self.log
        )
        ra = converter.ra_sexegesimal_to_decimal(
            ra=self.ra
        )
        dec = converter.dec_sexegesimal_to_decimal(
            dec=self.dec
        )
        url = """http://skyservice.pha.jhu.edu/DR12/ImgCutout/getjpeg.aspx?ra=%(ra)s&dec=%(dec)s&scale=%(scale)s&%(opt)sPhotoObjs=on&width=%(width)s&height=%(width)s""" % locals(
        )

        from fundamentals.download import multiobject_download
        localUrls = multiobject_download(
            urlList=[url],
            downloadDirectory=self.downloadDirectory,
            log=self.log,
            timeStamp=False,
            timeout=180,
            concurrentDownloads=10,
            resetFilename=[self.filename],
            credentials=False,  # { 'username' : "...", "password", "..." }
            longTime=True,
            indexFilenames=False
        )

        print url

        self.log.info('completed the ``_download_sdss_image`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method
