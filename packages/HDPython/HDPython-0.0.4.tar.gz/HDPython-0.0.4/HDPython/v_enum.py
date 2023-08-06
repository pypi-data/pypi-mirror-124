import os,sys,inspect

from HDPython.base import *
from HDPython.v_symbol import v_symbol
from HDPython.primitive_type_converter import get_primitive_hdl_converter
from HDPython.lib_enums import  varSig, InOut_t



class v_enum(HDPython_base):
    def __init__(self,EnumIn,EnumVal=None,name=None, Inout = InOut_t.Internal_t,includes="",value=None,varSigConst=varSig.variable_t):
        super().__init__()
        self.__hdl_converter__ =get_primitive_hdl_converter("v_enum" )() 
        if type(EnumIn).__name__ == "EnumMeta":
            Enumtype = EnumIn
        elif type(type(EnumIn)).__name__ == "EnumMeta":
            Enumtype = type(EnumIn)
            EnumVal = EnumIn
            
        if EnumVal == None:
            EnumVal = Enumtype(0)

        if name == None:
            name = Enumtype.__name__

        self.symbol = v_symbol(name,EnumVal.value,Inout=Inout,includes=includes,value=EnumVal.value,varSigConst=varSigConst )
        self._type = Enumtype
        
        self.name = name
        self.__hdl_name__ = None
        self._Inout = Inout
        self._varSigConst = varSigConst

    def __lshift__(self, rhs):
        
        if isinstance(rhs,type(self)):
            self.symbol << rhs.symbol
            return 
        
        if isinstance(rhs,self._type):
            self.symbol << value(rhs)
            return 

        raise Exception("[ENUM] Unable tp connect different types", self, rhs)


        
    def _sim_get_new_storage(self):
        self.symbol._sim_get_new_storage()

    def set_simulation_param(self,module, name,writer):
        self.symbol.set_simulation_param(module, name, writer)
    
    def __repr__(self):
        ret = str(self._type(value(self.symbol)).name) +": "+ str(value(self.symbol))
        return ret
    
    def setInout(self,Inout):
        self.symbol.setInout(Inout)


    def set_varSigConst(self, varSigConst):
        self._varSigConst=varSigConst
        self.symbol.set_varSigConst(varSigConst)

    def isVarSigType(self, varSigType):
        return self.symbol.isVarSigType( varSigType)

    def _sim_get_value(self):
        return value(self.symbol)
    
    def __eq__(self,rhs):
        return value(self) == value(rhs) 
    
    def set_vhdl_name(self,name, Overwrite = False):
        if self.__hdl_name__ and self.__hdl_name__ != name and Overwrite == False:
            raise Exception("double Conversion to vhdl")
        else:
            self.__hdl_name__ = name



   
    

    def isInOutType(self, Inout):
        
        if Inout==None or self._Inout == Inout: 
            return True
        elif self._Inout== InOut_t.Master_t:
            mem = self.getMember(Inout)
            return len(mem) > 0
        elif self._Inout == InOut_t.Slave_t:
            if Inout == InOut_t.Master_t:
                Inout = InOut_t.Slave_t
            elif Inout == InOut_t.Slave_t:
                Inout = InOut_t.Master_t
            elif Inout == InOut_t.input_t:
                Inout = InOut_t.output_t
            elif Inout == InOut_t.output_t:
                Inout = InOut_t.input_t
            
            mem = self.getMember(Inout)
            return len(mem) > 0




    def __str__(self):
        if self.__hdl_name__:
            return self.__hdl_name__

        return self._type(value(self.symbol)).name 


    

    def _issubclass_(self,test):
        if super()._issubclass_(test):
            return True
        return "v_enum" == test
        
