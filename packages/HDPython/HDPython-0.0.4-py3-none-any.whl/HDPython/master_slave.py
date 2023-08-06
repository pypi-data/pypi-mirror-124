from HDPython.base import *
from HDPython.v_function import *
from HDPython.v_entity_list import *



from HDPython.v_class import  v_class
from HDPython.v_class_handle import  v_class_hanlde
from HDPython.object_factory import add_constructor
from HDPython.converter.v_class_handle_converter import v_class_hanlde_converter


class v_class_master_converter(v_class_hanlde_converter):
    def __init__(self):
        super().__init__()


class v_class_master(v_class_hanlde):

    def __init__(self,Name=None,varSigConst=None):
        super().__init__(Name,varSigConst)
        self.__hdl_converter__ = v_class_master_converter()
        self.__v_classType__  = v_classType_t.Master_t



class v_class_slave_converter(v_class_hanlde_converter):
    def __init__(self):
        super().__init__()


class v_class_slave(v_class_hanlde):

    def __init__(self,Name=None,varSigConst=None):
        super().__init__(Name,varSigConst)
        self.__hdl_converter__ = v_class_slave_converter()
        self.__v_classType__  = v_classType_t.Slave_t



def get_master(transObj):
    return transObj.get_master()

def get_salve(transObj):
    return transObj.get_slave()

def get_handle(transObj):
    if transObj._Inout == InOut_t.Slave_t:
        return get_salve(transObj)
    
    if transObj._Inout  == InOut_t.Master_t:
        return get_master(transObj)
    
    raise Exception("Unable to determint requiered handle")


add_constructor("v_class_slave", v_class_slave)
add_constructor("v_class_master",v_class_master)
