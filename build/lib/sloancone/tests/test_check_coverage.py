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

class test_check_coverage(unittest.TestCase):

    def test_check_coverage_function(self):

        from sloancone import check_coverage
        covered = check_coverage(
            log=log,
            ra="122.3343",
            dec="45.34343"
        ).get()

        print(covered)

    def test_check_coverage_function2(self):

        from sloancone import check_coverage
        covered = check_coverage(
            log=log,
            ra=122.3343,
            dec=-45.34343
        ).get()

        print(covered)

    def test_check_coverage_function3(self):

        from sloancone import check_coverage
        covered = check_coverage(
            log=log,
            ra="12:45:4.45466",
            dec="-25:22:34.3434"
        ).get()

        print(covered)

    def test_check_coverage_function_exception(self):
        from sloancone import check_coverage
        try:
            this = check_coverage(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
