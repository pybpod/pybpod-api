# !/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.4.0.beta"
__author__ = ['Joshua Sanders', 'Carlos Mão de Ferro']
__credits__ = ["Carlos Mao de Ferro", "Ricardo Ribeiro"]
__license__ = "Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>"
__maintainer__ = ['Joshua Sanders', 'Carlos Mão de Ferro', 'Ricardo Ribeiro']
__email__ = ['joshua21@gmail.com', 'cajomferro@gmail.com', 'ricardojvr@gmail.com']
__status__ = "Development"


from pysettings import conf
import loggingbootstrap

#load the user settings
try:
	import user_settings
	conf += user_settings
except:
	pass

conf += 'pybpodapi.settings'


if conf.PYBPOD_API_LOG_LEVEL is not None:
	# setup different loggers for example script and api
	loggingbootstrap.create_double_logger("pybpodapi", conf.PYBPOD_API_LOG_LEVEL, conf.PYBPOD_API_LOG_FILE, conf.PYBPOD_API_LOG_LEVEL)
