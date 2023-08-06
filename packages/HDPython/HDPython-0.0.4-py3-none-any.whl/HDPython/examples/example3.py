
import functools
import argparse
import os,sys,inspect
import copy


from HDPython.base import *
from HDPython.v_symbol import *
from HDPython.examples.axiStream import *
from HDPython.v_entity import *

from HDPython.simulation import *




class axiFilter(v_clk_entity):
    def __init__(self,clk=None):
        super().__init__( clk)
        self.Axi_in = port_Stream_Slave(axisStream(v_slv(32)))
        self.Axi_out = port_Stream_Master(axisStream(v_slv(32)))
        self.architecture()

        
    def architecture(self):
        @process()
        def _process1():
            axiSalve = axisStream_slave(self.Axi_in)
            axMaster = axisStream_master(self.Axi_out) 


            i_buff = v_slv(32)
            @rising_edge(self.clk)
            def proc():
                #print("axiPrint",value(  i_buff) )
                if axiSalve and axMaster:
                    i_buff << axiSalve
                    if i_buff < 10:
                        axMaster << axiSalve
                        #print("axiPrint valid",value( i_buff) )

class axiPrint(v_clk_entity):
    def __init__(self,clk=None):
        super().__init__( clk)
        self.Axi_in =  port_Stream_Slave(axisStream(v_slv(32)))
        self.architecture()

        
    def architecture(self):
        @process()
        def _process1():
            axiSalve = axisStream_slave(self.Axi_in)

            i_buff = v_slv(32)

            @rising_edge(self.clk)
            def proc():
                #print("axiPrint",value(i_buff) )
                if axiSalve :
                    i_buff << axiSalve
                    #print("axiPrint valid",value(i_buff) )



class clk_generator(v_entity):
    def __init__(self):
        super().__init__()
        self.clk = port_out(v_sl())
        self.architecture()

    def architecture(self):
        
        @process()
        def p1():

            @timed()
            def proc():
                self.clk << 1
                #print("======================")
                yield wait_for(10)
                self.clk << 0
                yield wait_for(10)


class rollingCounter(v_clk_entity):
    def __init__(self,clk=None,MaxCount=v_slv(32,100)):
        super().__init__( clk)
        self.Axi_out = port_Stream_Master( axisStream(v_slv(32)))
        self.MaxCount = port_in(v_slv(32,10))
        self.MaxCount << MaxCount
        self.architecture()
    
    def architecture(self):
        
        counter = v_slv(32)
        @process()
        def p2():
            v_Axi_out = axisStream_master(self.Axi_out)
            @rising_edge(self.clk)
            def proc():
                if v_Axi_out:
                    #print("counter", value( counter) )
                    v_Axi_out << counter
                
                    counter << counter + 1

                if counter > self.MaxCount:
                    counter << 0


class tb_entity(v_entity):
    def __init__(self):
        super().__init__()
        self.architecture()
        


    def architecture(self):
        clkgen = clk_generator()

        maxCount = v_slv(32,20)
        axiSource = rollingCounter(clkgen.clk,maxCount)
        axP       = axiPrint(clkgen.clk)
        axFilter  = axiFilter(clkgen.clk)
        
        axiSource | axFilter | axP
        
        end_architecture()


                




