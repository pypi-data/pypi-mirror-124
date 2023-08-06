from HDPython.ast.ast_classes.ast_base import  add_class
import  HDPython.hdl_converter as  hdl

def body_unfold_BitAnd(astParser,Node,keywords=None):
    rhs =  astParser.Unfold_body(Node.right)
    lhs =  astParser.Unfold_body(Node.left)
    ret = hdl.impl_bit_and(lhs, rhs,  astParser)
    return ret

add_class("BitAnd",body_unfold_BitAnd)