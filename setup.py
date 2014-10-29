from setuptools import setup, find_packages
from os import path

GIANT_VERSION="1.4"


def get_file_contents(filename):
    fd = file(path.join(path.dirname(__file__), filename), "r")
    content = fd.read()
    fd.close()
    return content

setup(
    name = "giant2",
    version = GIANT_VERSION,
    description = "A stock analysis tool",
    long_description=get_file_contents("README.md"),
    author='seanchen',
    author_email='funningboy@gmail.com',
#    url='http://github.com/ajdiaz/whistler',
    packages=find_packages(),
    entry_points = {'scrapy': ['settings = crawler.settings']},
    scripts = ['bin/start.py'],
#    install_requires = [
#        "sleekxmpp>=1.0",
#        "pyasn1>=0.1.4",
#        "pyasn1-modules>=0.0.4",
#        "twitter>=1.9.4",
#        "bitly-api>=0.2",
#    ],
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Communications :: Chat',
    ],
)
