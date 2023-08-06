from filecmp import dircmp
import functools
import argparse
import os,sys,inspect
import copy


from HDPython import *

import HDPython.examples as  ahe
import HDPython.debug_vis as debug_vis

from .helpers import Folders_isSame, vhdl_conversion, do_simulation
from HDPython.test_handler import add_test


def clock_t():
    clk   =  v_sl() 
    clk.__isFreeType__ = True
    return clk 

class SerialDataConfig(v_record):
    def __init__(self):
        super().__init__()
        self.row_Select            =  v_slv(3)
        self.column_select         =  v_slv(6)
        self.ASIC_NUM              =  v_slv(5)
        self.force_test_pattern    =  v_sl() 
        self.sample_start          =  v_slv(5)
        self.sample_stop           =  v_slv(5)


class register_t(v_record):
    def __init__(self):
        super().__init__()
        self.address   = v_slv(16) 
        self.value     = v_slv(16) 
        


class klm_globals(v_record):
    def __init__(self):
        super().__init__()
        self.clk   =  clock_t() 
        self.rst   =  v_sl() 
        self.reg   =  register_t() 

class InputDelay(v_entity):
    def __init__(self,k_globals =None,InputType = v_slv(32),Delay=0):
        super().__init__()
        self.globals  = port_Slave(klm_globals())
        if k_globals != None:
            self.globals  << k_globals
        self.ConfigIn = port_Stream_Slave(ahe.axisStream( InputType))
        self.ConfigOut = port_Stream_Master(ahe.axisStream( InputType))
        self.Delay = Delay
        self.architecture()

    @architecture
    def architecture(self):

        pipe2 = delay(times=self.Delay,obj=self)
        end_architecture()


def delay(times,obj):
    pipe1 = obj.ConfigIn |  ahe.stream_delay_one(obj.globals.clk,  obj.ConfigIn.data) 
    for _ in range(times):
        pipe1 |   ahe.stream_delay_one(obj.globals.clk,  obj.ConfigIn.data) 
            

    pipe1 |   obj.ConfigOut
    return pipe1

class InputDelay_print(v_entity):
    def __init__(self,k_globals =None,InputType =v_slv(32)):
        super().__init__()
        self.globals  = port_Slave(klm_globals())
        if k_globals != None:
            self.globals << k_globals
        self.ConfigIn = port_Stream_Slave(ahe.axisStream( InputType))
        self.architecture()

    @architecture
    def architecture(self):
        d =  v_copy(self.ConfigIn.data)
        ax_slave = get_salve(self.ConfigIn)
        counter = v_int(0)
        @rising_edge(self.globals.clk)
        def proc():
            counter << counter + 1
            if ax_slave :
               ax_slave >> d  
               #print("InputDelay_print", value(d))
            
            if counter > 15:
                counter << 0


        end_architecture()

class dataSource(v_clk_entity):
    def __init__(self,clk,outputType =v_slv(32)):
        super().__init__(clk)


        self.DataOut = port_Stream_Master(ahe.axisStream( outputType))
        self.architecture()

    @architecture
    def architecture(self):
        mast = get_handle(self.DataOut)
        data = v_slv(32,5)

        @rising_edge(self.clk)
        def proc():
            if mast:
                mast << data
                data << data + 2

        end_architecture()
           

class InputDelay_tb(v_entity):
    def __init__(self):
        super().__init__()
        self.architecture()

    @architecture
    def architecture(self):
        clkgen = ahe.clk_generator()
        k_globals =klm_globals()
        data = v_slv(32,5)


        dut  = InputDelay(k_globals,Delay=5) 

        axprint  =   InputDelay_print(k_globals)

        axprint.ConfigIn << dut.ConfigOut
        k_globals.clk << clkgen.clk

        d_source  =   dataSource(k_globals.clk)
        dut.ConfigIn << d_source.DataOut




        end_architecture()




def InputDelay2vhdl(OutputPath):
    g_global_reset()
    tb  =InputDelay_tb()
    convert_to_hdl(tb, OutputPath +"/output/" + "InputDelay_tb")

 



class InputDelay_tb_sim(v_entity):
    def __init__(self,f):
        super().__init__()
        self.f = f
        self.architecture()

    @architecture
    def architecture(self):
        clkgen = ahe.clk_generator()
        k_globals =klm_globals()
        data = v_slv(32,0)


        dut  = InputDelay(k_globals,Delay=5) 

        axprint  =   InputDelay_print(k_globals)

        axprint.ConfigIn << dut.ConfigOut
        k_globals.clk << clkgen.clk

        d_source  =   dataSource(k_globals.clk)
        dut.ConfigIn << d_source.DataOut

        @rising_edge(clkgen.clk)
        def proc():
            data << data +1
            
            self.f.write(str(value(data)) +", " + str(value(d_source.DataOut.data))+", " +str(value(dut.ConfigOut.data)) + '\n')


        end_architecture()

@do_simulation
def InputDelay_sim(OutputPath, f):
    
    tb  =InputDelay_tb_sim(f)
    return tb
    

    
    
def test_InputDelay_sim():
    return InputDelay_sim("tests/ex1/")

add_test("InputDelay_sim", test_InputDelay_sim)

@vhdl_conversion
def InputDelay2vhdl(OutputPath):

    tb  =InputDelay_tb()
    return tb

def test_InputDelay2vhdl():
    return InputDelay2vhdl("tests/ex1_vhdl/")

add_test("InputDelay2vhdl", test_InputDelay2vhdl)