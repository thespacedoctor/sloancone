from __future__ import print_function
from builtins import str
import os
import unittest
import shutil
import yaml
from sloancone.utKit import utKit
from fundamentals import tools
from os.path import expanduser
home = expanduser("~")

packageDirectory = utKit("").get_project_root()
settingsFile = packageDirectory + "/test_settings.yaml"

su = tools(
    arguments={"settingsFile": settingsFile},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName=None,
    defaultSettingsFile=False
)
arguments, settings, log, dbConn = su.setup()

# SETUP PATHS TO COMMON DIRECTORIES FOR TEST DATA
moduleDirectory = os.path.dirname(__file__)
pathToInputDir = moduleDirectory + "/input/"
pathToOutputDir = moduleDirectory + "/output/"

try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

class test_sdss_square_search(unittest.TestCase):

    def test_sdss_square_search_function_01(self):
        from sloancone import sdss_square_search
        kwargs = {}
        kwargs["log"] = log
        kwargs["ra"] = 179.5
        kwargs["dec"] = -1.0
        kwargs["searchRadius"] = 10.0
        # xt-kwarg_key_and_value

        search = sdss_square_search(**kwargs)
        search.get()

    def test_sdss_square_search_function_02(self):
        from sloancone import sdss_square_search
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
