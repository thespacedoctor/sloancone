#!/usr/local/bin/python
# encoding: utf-8
"""
*Get common file and folder paths for the host package*

:Author:
    David Young

:Date Created:
    October 24, 2013
"""
################# GLOBAL IMPORTS ####################
import sys
import os
from docopt import docopt


def getpackagepath():
    """
    *getpackagepath*
    """
    moduleDirectory = os.path.dirname(__file__)
    packagePath = os.path.dirname(__file__) + "/../"

    return packagePath


if __name__ == '__main__':
    main()
