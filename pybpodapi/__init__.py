# !/usr/bin/python3
# -*- coding: utf-8 -*-
from confapp import conf
import loggingbootstrap

__version__ = "1.8.2"
__author__ = [
    "Ricardo Ribeiro",
    "Carlos Mão de Ferro",
    "Joshua Sanders",
    "Luís Teixeira",
]
__credits__ = ["Ricardo Ribeiro", "Carlos Mao de Ferro", "Luís Teixeira"]
__license__ = "MIT"
__maintainer__ = [
    "Ricardo Ribeiro",
    "Carlos Mão de Ferro",
    "Joshua Sanders",
    "Luís Teixeira",
]
__email__ = [
    "ricardojvr@gmail.com",
    "cajomferro@gmail.com",
    "joshua21@gmail.com",
    "micboucinha@gmail.com",
]
__status__ = "Development"


# load the user settings
try:
    import user_settings

    conf += user_settings
except:
    pass

conf += "pybpodapi.settings"

if conf.PYBPOD_API_LOG_LEVEL is not None:
    # setup different loggers for example script and api
    loggingbootstrap.create_double_logger(
        "pybpodapi",
        conf.PYBPOD_API_LOG_LEVEL,
        conf.PYBPOD_API_LOG_FILE,
        conf.PYBPOD_API_LOG_LEVEL,
    )
