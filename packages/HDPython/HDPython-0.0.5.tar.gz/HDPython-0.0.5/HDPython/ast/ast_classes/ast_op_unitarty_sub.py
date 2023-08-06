
from HDPython.ast.ast_classes.ast_base import v_ast_base, add_class
from HDPython.base import HDPython_base
from HDPython.lib_enums import varSig

class v_USubOP(v_ast_base):
    def __init__(self,obj):
        self.obj = obj
        self._type = obj._type
    
    def __str__(self):

        return  " -(" + str(self.obj) +")"

def body_unfol_USub(astParser,Node):
    arg = astParser.Unfold_body(Node.operand)
    if issubclass(type(arg),HDPython_base) and arg._varSigConst==varSig.unnamed_const:
        arg.nextValue = -arg.nextValue
        arg.set_vhdl_name(str(arg.nextValue) , True)
        return arg

    return v_USubOP(arg)

add_class('USub' , body_unfol_USub)