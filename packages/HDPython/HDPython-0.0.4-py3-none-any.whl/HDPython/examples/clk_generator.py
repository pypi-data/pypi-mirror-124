
import unittest
import functools
import argparse
import os,sys,inspect
import copy

from HDPython.base import *
from HDPython.v_symbol import *
from HDPython.v_entity import *
from HDPython.v_list import *




class clk_generator(v_entity):
    def __init__(self):
        super().__init__()
        self.clk = port_out(v_sl())
        self.architecture()
    
    @architecture
    def architecture(self):
        
        @timed()
        def proc():
            self.clk << 1
            #print("======================")
            yield wait_for(10)
            self.clk << 0
            yield wait_for(10)

