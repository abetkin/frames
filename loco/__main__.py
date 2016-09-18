"""
loco: "Logical" coroutines.
Usage:
    loco [--] [ <arg>... ]
    loco -h | --help
"""

import sys
import six
import docopt

from .main import DiscoverLocos

DiscoverLocos()

# FIXME discover in the launched script too 


a = docopt.docopt(__doc__)
sys.argv = a['<arg>']

import ipdb
with ipdb.launch_ipdb_on_exception():

    with open(a['<arg>'][0], "rb") as f:
        six.exec_(compile(f.read(), a['<arg>'][0], 'exec'))

