import os
import nose
import shutil
import yaml
from sloancone import image
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


class test_image():

    def test_image_function(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="09:40:50.10",
            dec="-09:42:52.7",
            downloadDirectory=pathToOutputDir,
            filename="test_01.jpeg"
        )
        this.get()

    def test_image_function02(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="179.689293428354",
            dec="-0.454379056007667",
            downloadDirectory=pathToOutputDir,
            filename="test_02.jpeg",
            grid=False,
            label=False,
            photocat=False,
            speccat=False,
            invertColors=False,
            arcminWidth=5,
            pixelWidth=500
        )
        this.get()

    def test_image_function03(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="179.689293428354",
            dec="-0.454379056007667",
            downloadDirectory=pathToOutputDir,
            filename="test_03.jpeg",
            grid=True,
            label=False,
            photocat=False,
            speccat=False,
            invertColors=False,
            arcminWidth=5,
            pixelWidth=500
        )
        this.get()

    def test_image_function04(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="179.689293428354",
            dec="-0.454379056007667",
            downloadDirectory=pathToOutputDir,
            filename="test_04.jpeg",
            grid=False,
            label=True,
            photocat=False,
            speccat=False,
            invertColors=False,
            arcminWidth=5,
            pixelWidth=500
        )
        this.get()

    def test_image_function05(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="179.689293428354",
            dec="-0.454379056007667",
            downloadDirectory=pathToOutputDir,
            filename="test_05.jpeg",
            grid=False,
            label=False,
            photocat=True,
            speccat=False,
            invertColors=False,
            arcminWidth=5,
            pixelWidth=500
        )
        this.get()

    def test_image_function06(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="179.689293428354",
            dec="-0.454379056007667",
            downloadDirectory=pathToOutputDir,
            filename="test_06.jpeg",
            grid=False,
            label=False,
            photocat=False,
            speccat=True,
            invertColors=False,
            arcminWidth=5,
            pixelWidth=500
        )
        this.get()

    def test_image_function07(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="179.689293428354",
            dec="-0.454379056007667",
            downloadDirectory=pathToOutputDir,
            filename="test_07.jpeg",
            grid=False,
            label=False,
            photocat=False,
            speccat=False,
            invertColors=True,
            arcminWidth=5,
            pixelWidth=500
        )
        this.get()

    def test_image_function08(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="179.689293428354",
            dec="-0.454379056007667",
            downloadDirectory=pathToOutputDir,
            filename="test_08.jpeg",
            grid=False,
            label=False,
            photocat=False,
            speccat=False,
            invertColors=False,
            arcminWidth=50,
            pixelWidth=500
        )
        this.get()

    def test_image_function09(self):

        from sloancone import image
        this = image(
            log=log,
            settings=settings,
            ra="179.689293428354",
            dec="-0.454379056007667",
            downloadDirectory=pathToOutputDir,
            filename="test_09.jpeg",
            grid=True,
            label=True,
            photocat=True,
            speccat=True,
            invertColors=True,
            arcminWidth=5,
            pixelWidth=500
        )
        this.get()

    def test_image_function_exception(self):

        from sloancone import image
        try:
            this = image(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
