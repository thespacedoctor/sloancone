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

class test_cone_search(unittest.TestCase):

    def test_cone_search_function(self):

        from sloancone.cone_search import cone_search
        this = cone_search(
            log=log,
            ra="12:45:23.2323",
            dec="30.343122",
            searchRadius=60.,
            nearest=True,
            outputFormat="table",
            galaxyType="all"
        )
        print(this.get())

        from sloancone.cone_search import cone_search
        this = cone_search(
            log=log,
            ra="12:45:23.2323",
            dec="30.343122",
            searchRadius=60.,
            nearest=False,
            outputFormat="table",
            galaxyType="all"
        )
        print(this.get())

    def test_cone_search_function2(self):

        from sloancone.cone_search import cone_search
        this = cone_search(
            log=log,
            ra="112.233432",
            dec="15:34:31.22",
            searchRadius=60.,
            nearest=True,
            outputFormat="table",
            galaxyType="all"
        )
        print(this.get())

        from sloancone.cone_search import cone_search
        this = cone_search(
            log=log,
            ra="112.233432",
            dec="15:34:31.22",
            searchRadius=60.,
            nearest=False,
            outputFormat="table",
            galaxyType="all"
        )
        print(this.get())

    def test_cone_search_function3(self):

        from sloancone.cone_search import cone_search
        this = cone_search(
            log=log,
            ra="112.233432",
            dec="15:34:31.22",
            searchRadius=60.,
            nearest=True,
            outputFormat="csv",
            galaxyType="all"
        )
        print(this.get())

        from sloancone.cone_search import cone_search
        this = cone_search(
            log=log,
            ra="112.233432",
            dec="15:34:31.22",
            searchRadius=60.,
            nearest=False,
            outputFormat="csv",
            galaxyType="all"
        )
        print(this.get())

    def test_cone_search_function4(self):

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

        print(csResults)

    def test_cone_search_function5(self):

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

        print(csResults)

    def test_cone_search_function_exception(self):

        from sloancone.cone_search import cone_search
        try:
            this = cone_search(
                log=log,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
