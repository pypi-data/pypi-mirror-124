
import unittest
import functools
import argparse
import os,sys,inspect
import copy

from HDPython.base import *
from HDPython.v_symbol import *
from HDPython.examples.axiStream import *
from HDPython.v_entity import *
from HDPython.v_list import *

from HDPython.tests.helpers import *

class axiPrint(v_clk_entity):
    def __init__(self,clk=None):
        super().__init__(clk)
        self.Axi_in =  port_Stream_Slave(axisStream(v_slv(32)))
        self.architecture()

        
    def architecture(self):
        axiSalve =  get_salve(self.Axi_in)

        i_buff = v_slv(32)

        @rising_edge(self.clk)
        def proc():
            
            if axiSalve :
                i_buff << axiSalve
                printf("axiPrint valid: "+str(value(i_buff)) )
        
        end_architecture()