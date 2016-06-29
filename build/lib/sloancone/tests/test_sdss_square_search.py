import os
import nose
import shutil
from sloancone import sdss_square_search
from sloancone.utKit import utKit

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# xnose-class-to-test-main-command-line-function-of-module


class test_sdss_square_search():

    def test_sdss_square_search_function_01(self):
        kwargs = {}
        kwargs["log"] = log
        kwargs["ra"] = 179.5
        kwargs["dec"] = -1.0
        kwargs["searchRadius"] = 10.0
        # xt-kwarg_key_and_value

        search = sdss_square_search(**kwargs)
        search.get()

    def test_sdss_square_search_function_02(self):
        kwargs = {}
        kwargs["log"] = log
        kwargs["ra"] = "23:23:13.23234"
        kwargs["dec"] = "-01:00:00.22323"
        kwargs["searchRadius"] = 170.0
        # xt-kwarg_key_and_value

        search = sdss_square_search(**kwargs)
        search.get()

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
