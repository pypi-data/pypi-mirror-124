from HDPython import *
from  HDPython.examples import *

from .helpers import Folders_isSame, vhdl_conversion, do_simulation,printf
from HDPython.test_handler import add_test



class Var_sig_class(v_class_master):
    def __init__(self):
        super().__init__()
        self.sTest1 = v_signal(v_slv(32))
        self.sTest2 = v_signal(v_slv(32))
        self.sTest3 = v_signal(v_slv(32))
        self.vTest1 = v_variable(v_slv(32))
        self.vTest2 = v_variable(v_slv(32))
        self.vTest3 = v_variable(v_slv(32))

    def f1(self):
        self.vTest1 << 5
        self.sTest1 << 4

    def f2(self, x):
        self.vTest2 << x
        self.sTest2 << x


class var_sig_impl(v_entity):
    def __init__(self):
        super().__init__()
        self.clk= port_in(v_sl())
        self.architecture()

    @architecture
    def architecture(self):
        vs_clas = Var_sig_class()
        data = v_slv(32)
        @rising_edge(self.clk)
        def proc():
            vs_clas.sTest3 << data
            vs_clas.vTest3 << data
            vs_clas.f1()
            vs_clas.f2(data)
            data << data + 1
            printf(str(value(data)) + " " +str(value(vs_clas.vTest1)) + " " +str(value(vs_clas.vTest2)) + " " +str(value(vs_clas.vTest3)) + " " +str(value(vs_clas.sTest1))+ " " +str(value(vs_clas.sTest2)) + " " +str(value(vs_clas.sTest3))+"\n")
            
            
        end_architecture()

class var_sig_tb(v_entity):
    def __init__(self):
        super().__init__()
        self.architecture()

    @architecture
    def architecture(self):
        clkgen = clk_generator()
        vs_impl = var_sig_impl()
        vs_impl.clk << clkgen.clk
            
        end_architecture()

@do_simulation
def var_sig_tb_sim(OutputPath, f= None):
    
    tb1 = var_sig_tb()
    return tb1

def test_var_sig_tb_sim():
    return var_sig_tb_sim("tests/var_sig_class_sim/") 

add_test("var_sig_tb_sim", test_var_sig_tb_sim)


@vhdl_conversion
def var_sig_tb_2vhdl(OutputPath, f= None):
    
    tb1 = var_sig_tb()
    return tb1

def test_RamHandler_2vhdl():
    return var_sig_tb_2vhdl("tests/var_sig_class/") 

#add_test("var_sig_tb_2vhdl", test_RamHandler_2vhdl)