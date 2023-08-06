from HDPython import *
from  HDPython.examples import *
from .helpers import Folders_isSame, vhdl_conversion, do_simulation
from HDPython.test_handler import add_test


class Counter(v_clk_entity):
    def __init__(self, clk , InputType=v_slv(32)):
        super().__init__(clk)
        self.Data_out = port_Stream_Master(axisStream( InputType))
        self.architecture()

    @architecture
    def architecture(self):
        data = v_slv(32)
        data2 = v_slv(32)
        data_out = get_handle(self.Data_out)
        @rising_edge(self.clk)
        def proc():
            data << data + 1
            if data_out and data > 10:
                data_out << data2
                data2   << data2 + 1
                data << 0

        end_architecture()

class tb(v_entity):
    def __init__(self):
        super().__init__()
        self.architecture()



    @architecture
    def architecture(self):
        clkgen = clk_generator()
        cnt    = Counter(clkgen.clk)

        cnt_out = get_handle(cnt.Data_out)
        data = v_slv(32)
        data2 = v_slv(32)
        opt_data = optional_t()
        @rising_edge(clkgen.clk)
        def proc():
            cnt_out >> data
            cnt_out >> opt_data 
            
           

        end_architecture()

@vhdl_conversion
def ex32vhdl(OutputPath):
    tb1 = tb()
        
    return tb1

def test_ex32vhdl():
    return ex32vhdl("tests/ex1_vhdl/")

#add_test("ex32vhdl", test_ex32vhdl)

