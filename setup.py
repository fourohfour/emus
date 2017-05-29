from setuptools import setup
import sys

if sys.version_info[0] is not 3:
    sys.exit("emus is a Python 3 package")

setup(
      name         = "emus"                              ,
      version      = "1.0"                               ,
      description  = "Emus: Table Compiler"              ,
      url          = "http://github.com/fourohfour/emus" ,
      author       = "FourOhFour"                        ,
      author_email = "404.fourohfour@gmail.com"          ,
      license      = "MIT"                               ,
      packages     = ["emus"]                            ,
      zip_safe     = False                               ,
      entry_points = {
          'console_scripts': ['emus=emus.emus:main']     ,
      }
     )

