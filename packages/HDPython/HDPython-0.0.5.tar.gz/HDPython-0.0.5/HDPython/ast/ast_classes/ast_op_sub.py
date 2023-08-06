from HDPython.ast.ast_classes.ast_base import v_ast_base, add_class
import  HDPython.hdl_converter as  hdl
from HDPython.base import HDPython_base

class v_sub(v_ast_base):
    def __init__(self,lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self._type = lhs._type
        

        

    def __str__(self):
        if issubclass(type(self.lhs),HDPython_base):
            return hdl.impl_sub(self.lhs, self.rhs)

        return str(self.lhs) + " - " +  str(self.rhs) 

def body_sub(astParser,Node):
    rhs =  astParser.Unfold_body(Node.right)
    lhs =  astParser.Unfold_body(Node.left)
    if issubclass( type(lhs),HDPython_base):
        return v_sub(lhs, rhs)

    var = astParser.get_variable(lhs.Value, Node)

    return v_sub(var, rhs)

add_class("Sub", body_sub)