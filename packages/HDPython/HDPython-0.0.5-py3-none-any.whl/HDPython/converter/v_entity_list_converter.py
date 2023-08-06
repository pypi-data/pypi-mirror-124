import  functools 

import os,sys,inspect

from HDPython.base import *
from HDPython.v_symbol import *

from HDPython.primitive_type_converter  import add_primitive_hdl_converter
from HDPython.converter.hdl_converter_base import hdl_converter_base



class v_entity_list_converter(hdl_converter_base):
        def __init__(self):
            super().__init__()
        def impl_architecture_header(self, obj):
            ret = "--------------------------"+ obj.__hdl_name__  +"-----------------\n"
            VarSymb = "signal"
            i = 0
            for x in obj.nexted_entities:
                i+=1
                if x["symbol"].__hdl_name__ is None or x["temp"]:
                    x["temp"] = True
                    tempName = obj.__hdl_name__ +"_"+ str(i) + "_" +type(x["symbol"]).__name__
                    x["symbol"].set_vhdl_name(tempName)
                    ret += hdl.impl_architecture_header(x["symbol"])
            ret += "-------------------------- end "+ obj.__hdl_name__  +"-----------------\n"
            return ret


        def impl_architecture_body(self, obj):
            
            ret = ""
            i = 0
            start = ""
            for x in obj.nexted_entities:
                i+=1
                if  x["symbol"].__hdl_name__ is None or x["temp"]:
                    x["temp"] = True
                    tempName = str(obj.__hdl_name__) +"_"+  str(i) + "_" +type(x["symbol"]).__name__
                    if not x["symbol"].__hdl_name__:
                        x["symbol"].set_vhdl_name(tempName)
                    ret += start + hdl.impl_architecture_body(x["symbol"])
                    start = ";\n  "
            


            return ret

        def def_includes(self,obj, name,parent):
            bufffer = ""
            
            for x in obj.nexted_entities:
                bufffer += hdl.def_includes(x["symbol"], None, None)

            ret  = make_unique_includes(bufffer)

            return ret

add_primitive_hdl_converter("v_entity_list" ,v_entity_list_converter)
