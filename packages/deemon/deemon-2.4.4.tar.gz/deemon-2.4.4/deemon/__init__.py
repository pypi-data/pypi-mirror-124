#!/usr/bin/env python3
from deemon.utils import startup

__version__ = '2.4.4'
__dbversion__ = '3.3'

appdata = startup.get_appdata_dir()
startup.init_appdata_dir(appdata)
