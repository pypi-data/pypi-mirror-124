from HDPython.v_class_handle import v_class_hanlde
from enum import Enum, auto
import pandas as pd 
from HDPython import *
from  HDPython.examples import *

from .helpers import Folders_isSame, vhdl_conversion, do_simulation,printf, printff
from HDPython.test_handler import add_test



class registerT(v_record):
    def __init__(self) -> None:
        super().__init__()
        self.addr = v_slv(16)
        self.val  = v_slv(16)

class globals_t(v_record):
    def __init__(self) -> None:
        super().__init__()
        self.clk = v_sl()
        self.rst = v_sl()
        self.reg = registerT()

def tb_vec_type():
    return v_list(v_slv(5),10)


class trigger_bits_pack(v_record):
    def __init__(self) -> None:
        super().__init__()
        self.data = tb_vec_type()
        self.time_stamp = v_slv(32)
        self.time_stamp_fine = v_slv(32)


class trigger_bits_buffer_t(v_class_hanlde):
    def __init__(self) -> None:
        super().__init__()
        self.tb_buffer      = v_signal(v_list(v_slv(5), 10))
        self.trigger_mask   = v_signal(v_slv(10))

    def push_back(self,  data_in ):
        self.tb_buffer << (data_in & self.tb_buffer[1:] )

    def set_trigger_mask(self,   trigger_mask):
        self.trigger_mask << trigger_mask

    def get_trigger_bits(self):
        ret  = v_slv(5)
        for I in self.tb_buffer:
            if self.trigger_mask[I]:
                ret << (ret or self.tb_buffer[I])
        return ret
        
  
    def rising_edge(self):
        return  self.tb_buffer[0] == 0  and self.tb_buffer[1] > 0
  





class optional_trigger_bits(v_record):
    def __init__(self) -> None:
        super().__init__()
        self.TriggerBits =  tb_vec_type()
        self.valid           =  v_sl()


class tb_edge_detection(v_entity):
    def __init__(self, gSystem:globals_t) -> None:
        super().__init__()
        self.gSystem = port_in(gSystem)
        self.gSystem << gSystem
        self.TriggerBits     =  port_in(tb_vec_type())
        self.TriggerBits_out =  port_out(optional_trigger_bits())
        
        self.architecture()


    @architecture
    def architecture(self):
        buff = v_list(trigger_bits_buffer_t(), len(self.TriggerBits) )
        TriggerMask = v_slv(10)

        @rising_edge(self.gSystem.clk)
        def proc():
            self.TriggerBits_out.valid << 0
            for ind in range(len(buff)):
                self.TriggerBits_out.TriggerBits[ind].reset()
                buff[ind].push_back(self.TriggerBits[ind])
                buff[ind].set_trigger_mask(TriggerMask)
                if buff[ind].rising_edge():
                    self.TriggerBits_out.TriggerBits[ind] << buff[ind].get_trigger_bits()
                    self.TriggerBits_out.valid << 1
                

        end_architecture()


class trigger_scaler(v_entity):
    def __init__(self, gSystem:globals_t, reg_out :registerT) -> None:
        super().__init__()
        self.gSystem = port_in(gSystem)
        self.gSystem << gSystem
        self.reg_out  = port_out(registerT())
        reg_out << self.reg_out

        self.trigger_bits_in  = pipeline_in(optional_trigger_bits())
        self.trigger_bits_out = pipeline_out(optional_trigger_bits())
        self.trigger_bits_out << self.trigger_bits_in

        self.architecture()

    @architecture
    def architecture(self):
        pass

class package_maker(v_entity):
    def __init__(self, gSystem:globals_t, reg_out :registerT) -> None:
        super().__init__()
        self.gSystem = port_in(gSystem)
        self.gSystem << gSystem

        self.trigger_bits_in  = pipeline_in(optional_trigger_bits())
        self.TX_triggerBits   = pipeline_out(axisStream(trigger_bits_pack()))

        self.architecture()

    @architecture
    def architecture(self):
        counter = v_slv(64)
        tx = get_handle(self.TX_triggerBits)
        buff = v_variable(trigger_bits_pack())
        @rising_edge(self.gSystem.clk)
        def proc():
            counter << counter + 1
            if tx and self.trigger_bits_in.valid:
                buff.time_stamp<< counter[32:]
                buff.time_stamp_fine<< counter[0:32]
                buff.data << self.trigger_bits_in.TriggerBits 
                
                tx << buff
            




class TX_TriggerBitSZ(v_entity):
    def __init__(self, gSystem:globals_t):
        super().__init__()
        self.gSystem = port_in(gSystem)
        self.gSystem << gSystem
        self.reg_out  = port_out(registerT())
        self.TARGET_TB_in  = port_in(tb_vec_type())
        self.TX_triggerBits = port_out(axisStream(trigger_bits_pack()))

        self.architecture()

    @architecture
    def architecture(self):
        edge_det = tb_edge_detection(self.gSystem) 

        self.TARGET_TB_in \
            | \
        edge_det 
        
        edge_det \
            | trigger_scaler(self.gSystem)  \
            |\
        self.reg_out
        
        edge_det\
            | package_maker(self.gSystem )  \
            | ax_fifo(self.gSystem.clk, trigger_bits_pack())\
            | \
        self.TX_triggerBits

        end_architecture()




@vhdl_conversion
def trigger_bits_test2vhdl(OutputPath, f= None):
    tb = tb_edge_detection(globals_t())  
    return tb


def test_trigger_bits_test2vhdl():
    return trigger_bits_test2vhdl("tests/trigger_bits_test2vhdl/") 

add_test("trigger_bits_test2vhdl", test_trigger_bits_test2vhdl)