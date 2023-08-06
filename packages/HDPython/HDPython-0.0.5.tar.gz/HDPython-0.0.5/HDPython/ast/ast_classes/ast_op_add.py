from HDPython.ast.ast_classes.ast_base import v_ast_base, add_class
from HDPython.base import HDPython_base, value
import  HDPython.hdl_converter as  hdl



class v_add(v_ast_base):
    def __init__(self,lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self._type = lhs._type
        self.Value = str(self.lhs) + " + " +  str(self.rhs) 
        

    def get_value(self):
        return value(self.lhs) + value(self.rhs)

    def get_type(self):
        return self._type

    def __str__(self):
        if issubclass(type(self.lhs),HDPython_base):
            return hdl.impl_add(self.lhs, self.rhs)

        return str(self.lhs) + " + " +  str(self.rhs) 

    def get_symbol(self):
        return self.lhs

def body_add(astParser,Node):
    rhs =  astParser.Unfold_body(Node.right)
    lhs =  astParser.Unfold_body(Node.left)
    return v_add(lhs, rhs)


add_class("Add",body_add)