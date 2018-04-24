# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os

from pyforms import conf as settings
from pybpodapi.bpod.bpod_com_protocol_modules import BpodCOMProtocolModules
from pybpodapi.com.messaging.trial      import Trial
from pybpodapi.com.messaging.session_info   import SessionInfo

from datetime import datetime as datetime_now
import pybpodapi

from pybpodapi.session import Session


logger = logging.getLogger(__name__)


class BpodIO(BpodCOMProtocolModules):
    """
    Bpod I/O logic.
    """
    def __init__(self, serial_port=None, workspace_path=None, protocol_name=None, sync_channel=None, sync_mode=None):
        self.workspace_path = workspace_path if workspace_path  is not None else settings.PYBPOD_SESSION_PATH
        self.protocol_name  = protocol_name  if protocol_name   is not None else settings.PROTOCOL_NAME

        super(BpodIO,self).__init__(serial_port, sync_channel, sync_mode)
        
        self.session += SessionInfo("This is a PYBPOD file. Find more info at http://pybpod.readthedocs.io")
        self.session += SessionInfo( Session.INFO_BPODAPI_VERSION, pybpodapi.__version__)
        self.session += SessionInfo( Session.INFO_PROTOCOL_NAME,    self.protocol_name )
        self.session += SessionInfo( Session.INFO_SESSION_STARTED,  self.session.start_timestamp )
        
    def create_session(self):
        return Session(os.path.join(self.workspace_path, self.protocol_name)) if self.workspace_path else  Session()
        
    
    def close(self):
        """
        Close connection with Bpod
        """
        super(BpodIO, self).close()
        
    def __del__(self):
        if hasattr(self, 'session') and self.session:
            del self._session
        


    @property
    def workspace_path(self):
        return self._workspace_path  # type: str

    @workspace_path.setter
    def workspace_path(self, value):
        self._workspace_path = value  # type: str

    @property
    def protocol_name(self):
        return self._protocol_name  # type: str

    @protocol_name.setter
    def protocol_name(self, value):
        self._protocol_name = value  # type: str