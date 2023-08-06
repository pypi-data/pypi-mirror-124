from HDPython.base import *
from HDPython.v_function import *
from HDPython.v_entity_list import *
from HDPython.simulation import *

import  HDPython.converter.vhdl_v_class_helpers as  vc_helper
from HDPython.v_class import  v_class



class v_class_trans(v_class):
    def __init__(self,Name=None,varSigConst=None):
        super().__init__(Name,varSigConst)
        self.__hdl_converter__ = get_primitive_hdl_converter("v_class_trans" )() 
        self.__v_classType__ = v_classType_t.transition_t 

    def get_vhdl_name(self,Inout=None):
        if Inout is None:
            return str(self.__hdl_name__)
        

        if Inout== InOut_t.input_t:
            return vc_helper.append_hdl_name(str(self.__hdl_name__), "_s2m")
        
        if Inout== InOut_t.output_t:
            return vc_helper.append_hdl_name(str(self.__hdl_name__), "_m2s")
        
        return None

    def setInout(self,Inout):
        if self._Inout == Inout:
            return 
        
        if self._Inout == InOut_t.Internal_t:
            self.__inout_register__ = {}
            members = self.getMember()
            for x in members:
                self.__inout_register__[x["name"]] = x["symbol"]._Inout
                
                

       
        

        
        if Inout == InOut_t.Master_t:
            self._Inout = Inout
            members = self.getMember()
            for x in members:
                x["symbol"].setInout(self.__inout_register__[x["name"]])
            
            return
            
        if Inout == InOut_t.Slave_t:
            self._Inout = Inout
            members = self.getMember()
            for x in members:
                x["symbol"].setInout( InoutFlip(self.__inout_register__[x["name"]]))

            return

        if Inout == InOut_t.Internal_t:
            self._Inout = Inout
            members = self.getMember()
            for x in members:
                x["symbol"].setInout(self.__inout_register__[x["name"]])
            
            return

        self._Inout = Inout
        members = self.getMember()
        for x in members:
            x["symbol"].setInout(Inout)