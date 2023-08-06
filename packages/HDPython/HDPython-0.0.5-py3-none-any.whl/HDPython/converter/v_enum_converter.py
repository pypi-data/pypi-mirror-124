import os,sys,inspect

from HDPython.base import *
from HDPython.v_symbol import v_symbol
from HDPython.primitive_type_converter  import add_primitive_hdl_converter
from HDPython.lib_enums import  *
from HDPython.converter.hdl_converter_base import hdl_converter_base
from HDPython.v_enum import  v_enum
from  HDPython.object_name_maker import  make_object_name
import  HDPython.hdl_converter as  hdl


class v_enum_converter(hdl_converter_base):
    def __init__(self):
        super().__init__()

    def get_type_simple(self,obj):
        
        objTypeName = obj.name        

        enumNames =[e.name for e in obj._type ] 
        ret = make_object_name(objTypeName,enumNames)
        return ret 


    def def_includes(self,obj, name,parent):
        PackageName = hdl.get_type_simple(obj)+"_pack"
        return "  use work." + PackageName+".all;\n"
    def def_packet_header(self,obj, name,parent):
        if  parent and parent._issubclass_("v_class"):
             return ""
            
        # type T_STATE is (RESET, START, EXECUTE, FINISH);
        name = hdl.get_type_simple(obj)
        enumNames =[e.name for e in obj._type ] 
        start = "" 
        ret =  "\n  type " + name + " is ( \n    " 
        for x in enumNames:
            ret += start + x
            start = ",\n    "
        ret += "\n  );\n\n"
        return ret
    
    def get_packet_file_name(self, obj):

        return hdl.get_type_simple(obj)+"_pack.vhd"

    def get_packet_file_content(self, obj):

        h1  = hdl.def_packet_header(obj,None,None)
        PackageName = hdl.get_type_simple(obj)+"_pack"
        fileContent = """
library IEEE;
library work;
use IEEE.numeric_std.all;
use IEEE.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use work.HDPython_core.all;

package {PackageName} is 
{pack}
end {PackageName};


package body {PackageName} is

end  {PackageName};

""".format(
    PackageName=PackageName,
    pack=h1
)

        


        return fileContent
    
    def def_def_record_Member(self, obj, name, parent,Inout=None):
        if parent._issubclass_("v_class"):
            if obj._Inout == InOut_t.Slave_t:
                Inout = InoutFlip(Inout)
            return name + " : " + hdl.get_type_simple(obj)
       
        return ""

    def def_def_record_Member_Default(self, obj, name, parent,Inout=None):
        if parent._issubclass_("v_class"):
            if obj._Inout == InOut_t.Slave_t:
                Inout = InoutFlip(Inout)

            return name + " => " + str(v_enum((obj._type(value(obj)))))

        return ""
    
    def impl_process_header(self,obj):
        if obj._Inout != InOut_t.Internal_t:
            return ""
        
        if obj._varSigConst != varSig.variable_t:
            return ""

        VarSymb = get_varSig(obj._varSigConst)

        return VarSymb +" " +str(obj) + " : " +  hdl.get_type_simple(obj) +" := " + obj._type(value(obj.symbol)).name +";\n"

    
    def impl_architecture_header(self, obj):
        if obj._Inout != InOut_t.Internal_t:
            return ""
        
        if obj._varSigConst != varSig.signal_t or obj._varSigConst != varSig.signal_t:
            return ""

        VarSymb = get_varSig(obj._varSigConst)

        return VarSymb +" " +str(obj) + " : " +  hdl.get_type_simple(obj) +" := " +obj._type(value(obj.symbol)).name+";\n"


add_primitive_hdl_converter("v_enum" ,v_enum_converter)
