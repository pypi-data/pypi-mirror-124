from HDPython.base import *
from HDPython.v_symbol import *
from HDPython.v_entity import  *
from HDPython.examples.system_globals import  *


class v_entity_gsystem(v_entity):
    def __init__(self,gSystem=None):
        super().__init__()
        self.gSystem    =  port_in( system_globals() )
        self.clk        =  port_in( v_sl())
        if gSystem is not  None:
            self.gSystem <<  gSystem
            self.clk << gSystem.clk

    def _issubclass_(self,test):
        if super()._issubclass_(test):
            return True
        return "v_entity_gsystem" == test