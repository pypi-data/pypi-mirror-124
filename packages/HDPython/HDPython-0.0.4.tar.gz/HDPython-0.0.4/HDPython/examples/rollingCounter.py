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



class rollingCounter(v_clk_entity):
    def __init__(self,clk=None,MaxCount=v_slv(32,100)):
        super().__init__( clk)
        self.Axi_out = port_Stream_Master( axisStream(v_slv(32)))
        self.MaxCount = port_in(v_slv(32,10))
        self.MaxCount << MaxCount
        self.architecture()
    
    def architecture(self):
        
        counter = v_slv(32)
        v_Axi_out = get_master(self.Axi_out)
        @rising_edge(self.clk)
        def proc():
            if v_Axi_out:
                v_Axi_out << counter
                
                counter << counter + 1

            if counter > self.MaxCount:
                counter << 0

        end_architecture()