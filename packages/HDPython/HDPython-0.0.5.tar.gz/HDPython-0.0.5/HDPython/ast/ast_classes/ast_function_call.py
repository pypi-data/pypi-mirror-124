from HDPython.ast.ast_classes.ast_base import v_ast_base, add_class
import  HDPython.hdl_converter as  hdl
from HDPython.v_function  import v_free_function_template
from HDPython.base import *
from HDPython.to_v_object import to_v_object

class v_call(v_ast_base):
    def __init__(self,memFunc, symbol, vhdl):
        self.memFunc = memFunc    
        self.symbol  =  symbol
        
        self.__hdl_name__ =vhdl
        
        self._type = symbol._type if hasattr(symbol, "_type") else None

    def __str__(self):
            return str(self.__hdl_name__) 
        
    def get_type(self):
        return self.symbol._type

    def get_symbol(self):
        return self.symbol

def body_unfold_call_local_func(astParser,Node):

    FuncName = Node.func.id
    args = list()
    args_2 = list()
    for x in Node.args:
        ar_local = astParser.Unfold_body(x)
        args.append(ar_local)
        args_2.append(get_symbol(ar_local))

    kwargs = {}
    for x in Node.keywords:
        kwargs[x.arg] = get_symbol(astParser.Unfold_body(x.value))
    
    r = astParser.local_function[Node.func.id](*args_2,**kwargs)
    
    f = astParser.local_function[Node.func.id]
    if hasattr(f,"description") and f.description is None: 
        f.description = v_free_function_template(f.funcrec,FuncName)
        gHDL_objectList.append(f.description)
        
        vhdl = hdl.impl_function_call(f.description, FuncName, args,astParser)

    if hasattr(f,"description") and f.description is not None: 
       
        vhdl = hdl.impl_function_call(f.description, FuncName, args,astParser)
    else:
        start = ""
        vhdl = str(Node.func.id) +"(" 
        for x in args:
            vhdl+= start + str(x)
            start  =', '
        
        vhdl += ")"

    if vhdl is None:
        astParser.Missing_template=True
        vhdl = "$$missing Template$$"

    
    ret = v_call(str(Node.func.id),r, vhdl)
    return ret


def body_unfold_call(astParser,Node):
    if hasattr(Node.func, 'id'):
        if Node.func.id in astParser._unfold_symbol_fun_arg:
            return astParser._unfold_symbol_fun_arg[Node.func.id](astParser, Node.args,Node.keywords)
        if Node.func.id in astParser.local_function:
            return body_unfold_call_local_func( astParser ,Node)
        
        raise Exception("unknown function")

    if hasattr(Node.func, 'value'):
        obj = astParser.Unfold_body(Node.func.value)
        #obj = astParser.getInstantByName(Node.func.value.id)
        memFunc = Node.func.attr
        f = getattr(obj,memFunc)

        args = list()
        for x in Node.args:
            args.append(astParser.Unfold_body(x))
        
        gf_type = isFunction()
        set_isFunction(True)
        if len(args) == 0:
            r = f()  # find out how to forward args 
        elif len(Node.args) == 1:
            r = f(args[0])  # find out how to forward args
        elif len(Node.args) == 2:
            r = f(args[0],args[1])  # find out how to forward args
        set_isFunction(gf_type)

        r = v_copy(to_v_object(r))
        vhdl =hdl.impl_function_call(obj, memFunc,[obj]+ args,astParser)
        r.set_vhdl_name(vhdl)
        ret = v_call(memFunc,r, vhdl)
        return ret

    if hasattr(Node.func, 'func'):
        return body_unfold_call(astParser,Node.func)


    raise Exception("Unknown call type")


add_class("Call", body_unfold_call)

