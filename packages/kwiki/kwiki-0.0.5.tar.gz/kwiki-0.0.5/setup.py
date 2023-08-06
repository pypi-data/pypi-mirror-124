from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'A parser of the Kurdish wiktionary (Wikiferheng)'
LONG_DESCRIPTION = 'A module that parse the Kurdish wiktionary with some useful and easy-to-use functions'

# Setting up
setup(
    name="kwiki",
    version=VERSION,
    author="Jagar Yousef",
    author_email="<jagar.yousef@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_data={find_packages()[0]: ['wikiferheng.json']},
    include_package_data=True,
    setup_requires=['wheel'],
    url='https://github.com/kurd-cc/kwiki',
    keywords=['kurdish', 'language', 'language-processing', 'kurmanji', 'wiktionary', 'parser'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# 1. python setup.py sdist bdist_wheel
# 2. twine upload --skip-existing dist/*