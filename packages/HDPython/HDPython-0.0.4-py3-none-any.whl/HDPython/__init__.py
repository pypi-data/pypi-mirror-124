from  HDPython.base import HDPython_base,HDPython_base0,architecture,end_architecture
from  HDPython.base import InOut_t,varSig,v_classType_t,v_dataObject,v_variable,v_signal,v_const
from  HDPython.base import port_out, variable_port_out, port_in, variable_port_in, port_Master, variable_port_Master, pipeline_in
from  HDPython.base import  pipeline_out, signal_port_Master, port_Stream_Master, signal_port_Slave, port_Slave, variable_port_Slave
from  HDPython.base import port_Stream_Slave, v_copy, convert_to_hdl, value, print_cnvt_set_file
from  HDPython.v_symbol import v_bool, v_sl ,v_slv, v_int , v_signed , v_unsigned, resize, v_symbol,v_symbol_reset
import HDPython.base as  ahb
from  HDPython.v_list import v_list

from  HDPython.v_entity import  process , timed , v_create, wait_for, combinational, v_switch , v_case, rising_edge, v_entity  ,v_clk_entity 
from  HDPython.v_entity_list import v_entity_list

from  HDPython.v_class  import v_class
from  HDPython.v_enum  import v_enum

import HDPython.simulation  as ah_simulation

from HDPython.v_Package  import v_package

from HDPython.v_class_trans import v_class_trans

from HDPython.v_record import v_record, v_data_record

from  HDPython.master_slave import get_master, get_salve, get_handle, v_class_master,v_class_slave
import HDPython.converter.primitive_type_converter_base as hdl_converter_base
import HDPython.converter.primitive_converter_bool as hdl_converter_bool
import HDPython.converter.primitive_converter_integer as hdl_converter_integer
import HDPython.converter.primitive_converter_signed as hdl_converter_signed
import HDPython.converter.primitive_converter_sl as hdl_converter_sl
import HDPython.converter.primitive_converter_sl as hdl_converter_sl
import HDPython.converter.primitive_converter_slv as hdl_converter_slv
import HDPython.converter.primitive_converter_uinteger as hdl_converter_uinteger
import HDPython.converter.primitive_converter_unsigned as hdl_converter_unsigned

import HDPython.converter.v_entity_converter as hdl_v_entity_converter
import HDPython.converter.v_list_converter as hdl_v_list_converter
import HDPython.converter.v_record_converter as hdl_v_record_converter
import HDPython.converter.v_class_handle_converter as hdl_v_class_handle_converter
import HDPython.converter.v_class_trans_converter as hdl_v_class_trans_converter

import HDPython.converter.v_free_function_template_converter as v_free_function_template_converter
import HDPython.converter.v_entity_list_converter as hdl_v_entity_list_converter
import HDPython.converter.v_enum_converter as hdl_v_enum_converter
import HDPython.converter.hdl_converter_base as hdl_hdl_converter_base
import HDPython.converter.v_package_converter as hdl_v_package_converter
import HDPython.converter.v_function_converter as hdl_v_function_converter












## v_entity



## v_entity_list





## HDPython.simulation 
#gsimulation = ah_simulation.gsimulation
run_simulation = ah_simulation.run_simulation












def g_global_reset():
    ahb.g_global_reset()
    v_symbol_reset()
    ah_simulation.Simulation_reset()