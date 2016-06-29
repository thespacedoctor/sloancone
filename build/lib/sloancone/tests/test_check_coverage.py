import os
import nose
import shutil
import yaml
from sloancone import check_coverage, cl_utils
from sloancone.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="sloancone",
    tunnel=False
)
arguments, settings, log, dbConn = su.setup()

# load settings
stream = file(
    "/Users/Dave/.config/sloancone/sloancone.yaml", 'r')
settings = yaml.load(stream)
stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()


class test_check_coverage():

    def test_check_coverage_function(self):

        from sloancone import check_coverage
        covered = check_coverage(
            log=log,
            ra="122.3343",
            dec="45.34343"
        ).get()

        print covered

    def test_check_coverage_function2(self):

        from sloancone import check_coverage
        covered = check_coverage(
            log=log,
            ra=122.3343,
            dec=-45.34343
        ).get()

        print covered

    def test_check_coverage_function3(self):

        from sloancone import check_coverage
        covered = check_coverage(
            log=log,
            ra="12:45:4.45466",
            dec="-25:22:34.3434"
        ).get()

        print covered

    # def test_check_coverage_function_exception(self):

    #     from sloancone import check_coverage
    #     try:
    #         this = check_coverage(
    #             log=log,
    #             settings=settings,
    #             fakeKey="break the code"
    #         )
    #         this.get()
    #         assert False
    #     except Exception, e:
    #         assert True
    #         print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
