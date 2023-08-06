from HDPython.base import *
from HDPython.v_function import *
from HDPython.v_entity_list import *
from HDPython.converter.v_class_converter import v_class_converter
from HDPython.v_class import   v_class
from HDPython.ast.AST_MemFunctionCalls import memFunctionCall
from HDPython.object_factory import add_constructor

from HDPython.primitive_type_converter  import add_primitive_hdl_converter

from  HDPython.lib_enums import varSig

class v_record_converter(v_class_converter):
    def __init__(self):
        super().__init__()
        self.functionNameVetoList.append("reset")



    def append_reset(self, obj):
        self.MemfunctionCalls.append(
        memFunctionCall(
            name= "reset",
            args=  [obj],
            obj= obj,
            call_func = call_func_record_reset,
            func_args = None,
            setDefault = False,
            varSigIndependent = True
        )
     )


    def make_connection(self, obj, name, parent):
        obj.pull_var = self.getConnecting_procedure_record(obj, "pull",varSig.variable_t)
        obj.push_var = self.getConnecting_procedure_record(obj, "push",varSig.variable_t)

        obj.pull_sig = self.getConnecting_procedure_record(obj, "pull",varSig.signal_t)
        obj.push_sig = self.getConnecting_procedure_record(obj, "push",varSig.signal_t)


    def getConnecting_procedure_record(self, obj, PushPull, varSig_):

        varSig_str  = "" if varSig_ == varSig.variable_t else " signal "
        assign = " := " if varSig_ == varSig.variable_t else " <= "
        name = PushPull+"_01" if varSig_ == varSig.variable_t else PushPull + "_11"

        if PushPull == "push":
            inout = " out "
            line = "data_IO  <=  self;"
        else:
            inout = " in "
            line = "self  " + assign +" data_IO;"

        type_name  = self.get_type_simple(obj)
        args = "signal clk: in std_logic; " + varSig_str+ "self : inout " + type_name + "; signal data_IO : " + inout + " " + type_name

        ret = v_procedure(
            name=name,
            argumentList=args,
            body=line,
            isFreeFunction=True,
            IsEmpty=False
        )

        return ret

    def impl_get_attribute(self,obj, attName,parent=None):
        return obj.get_vhdl_name() + "." +str(attName)
    
    def impl_reasign(self, obj, rhs, astParser=None,context_str=None):

        if rhs._Inout == InOut_t.Master_t:
            raise Exception("cannot read from Master")

        if rhs._Inout == InOut_t.output_t:
            raise Exception("cannot read from Output")
            
        if rhs._type != obj._type:
            raise Exception("cannot assigne different types.", str(obj), rhs._type, obj._type )

        asOp = hdl.get_assiment_op(obj)
        obj._add_output()
        return obj.get_vhdl_name() + asOp +  rhs.get_vhdl_name()
    
    def impl_reasign_rshift_(self, obj, rhs, astParser=None,context_str=None):
        return hdl.impl_reasign(rhs,obj,astParser,context_str)
    
def call_func_record_reset(obj, name, args, astParser=None,func_args=None):
    asOp = hdl.get_assiment_op(args[0])
    val =  hdl.impl_get_init_values(args[0],args[0])
    
    ret =  str(args[0])  + asOp + val
    args[0]._add_output()
    return ret

add_primitive_hdl_converter("v_record",v_record_converter )
