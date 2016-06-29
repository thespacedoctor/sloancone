import os
import nose
import shutil
import yaml
from sloancone.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="WARNING",
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


class test_cone_search():

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
        print this.get()

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
        print this.get()

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
        print this.get()

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
        print this.get()

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
        print this.get()

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
        print this.get()

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

        print csResults

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

        print csResults

    # def test_cone_search_function_exception(self):

    #     from sloancone.cone_search import cone_search
    #     try:
    #         this = cone_search(
    #             log=log,
    #             fakeKey="break the code"
    #         )
    #         this.get()
    #         assert False
    #     except Exception, e:
    #         assert True
    #         print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
