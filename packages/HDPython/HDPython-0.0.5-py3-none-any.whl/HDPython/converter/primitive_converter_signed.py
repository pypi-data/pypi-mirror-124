
from HDPython.converter.primitive_type_converter_base import *


class v_signed_converter(v_symbol_converter):
    primitive_type = "signed"

    def __init__(self ,inc_str):
        super().__init__(inc_str)


    def impl_compare(self ,obj:"v_symbol", ops, rhs, astParser):
        astParser.add_read(obj)
        obj._add_input()
        if issubclass(type(rhs) ,HDPython_base):
            astParser.add_read(rhs)
            rhs._add_input()

        return str(obj) + "  "+ hdl.ops2str(ops) +" " + str(rhs)



    def impl_reasign(self, obj: "v_symbol", rhs, astParser=None, context_str=None):
        if astParser:
            astParser.add_write(obj)
        obj._add_output()
        target = str(obj)


        if issubclass(type(rhs), HDPython_base0) and str(obj.__Driver__) != 'process' and str(obj.__Driver__) != 'function':
            obj.__Driver__ = rhs

        asOp = hdl.get_assiment_op(obj)
        if str(rhs) == '0':
            return target + asOp + " (others => '0')"

        if issubclass(type(rhs), HDPython_base):
            if rhs.get_type() == 'integer':
                return """{dest} {asOp} to_signed({src}, {dest}'length)""".format(
                    dest=target,
                    src=str(rhs),
                    asOp=asOp
                )



        
            if 'std_logic_vector' in rhs.get_type() :
                return """{dest} {asOp} signed({src})""".format(
                    dest=target,
                    src=str(rhs),
                    asOp=asOp
                )

            return target + asOp + str(hdl.impl_get_value(rhs, obj, astParser=astParser))


        if type(rhs).__name__ == "v_Num":
            return """{dest} {asOp} to_signed({src}, {dest}'length)""".format(
                dest=target,
                src=str(rhs.value),
                asOp=asOp
            )

        rhs_str = str(rhs)
        if rhs_str.isnumeric():
            return """{dest} {asOp} to_signed({src}, {dest}'length)""".format(
                dest=target,
                src=rhs_str,
                asOp=asOp
            )

        return target + asOp + str(rhs)

    def impl_slice(self, obj:"v_symbol", sl, astParser=None):
        astParser.add_read(obj)
        obj._add_input()
        sl.set_source(obj)
        if type(sl).__name__ == "v_slice":
            ret = v_signed(Inout=obj._Inout, varSigConst=obj._varSigConst)
            ret.__hdl_name__ = obj.__hdl_name__ + "(" + str(sl) + ")"
        else:
            ret = v_sl(Inout=obj._Inout, varSigConst=obj._varSigConst)
            index = hdl.impl_get_value(sl, v_uint())
            ret.__hdl_name__ = obj.__hdl_name__ + "(" + str(index) + ")"

        return ret

    def impl_reasign_rshift_(self, obj:"v_symbol", rhs, astParser=None, context_str=None):
        if issubclass(type(obj), HDPython_base0) and issubclass(type(rhs), HDPython_base0):
            if "signed" in str(value(rhs._type)):
                if astParser:
                    astParser.add_write(rhs)
                rhs._add_output()
                obj._add_input()
                asOp = hdl.get_assiment_op(rhs)
                top = "ah_min(" + str(rhs) + "'length, "+str(obj) + "'length)"
                return str(rhs) + "( " +top +" downto 0)" + asOp + str(obj) + "( " +top +" downto 0)"

        return hdl.impl_reasign(rhs, obj, astParser, context_str)

    def get_type_simple(self, obj: "v_symbol"):
        ret = obj._type
        if issubclass(type(obj._type),v_symbol):
            return obj.primitive_type + "(" + str(obj.Bitwidth_raw) + " - 1 downto 0)"
        sp1 = int(ret.split("downto")[0].split("(")[1])
        sp2 = int(ret.split("downto")[1].split(")")[0])
        sp3 = sp1 - sp2 + 1
        ret = "signed" + str(sp3)
        return ret

    def impl_get_value(self, obj: "v_symbol", ReturnToObj=None, astParser=None):
        if astParser:
            astParser.add_read(obj)
        obj._add_input()
        if ReturnToObj.get_type() == obj._type:
            return obj

        if ReturnToObj.get_type() == "integer":
            return "to_integer(" + str(obj) + ")"
        if ReturnToObj.get_type() == "uinteger":
            return "to_integer(" + str(obj) + ")"
        return obj

    def get_type_func_arg(self, obj: "v_symbol"):
        return "signed"

    def get_default_value(self,obj:"v_symbol"):
        if str(obj.DefaultValue) == '0':
            Default = "(others => '0')"
            return Default

        
        if type(obj.DefaultValue).__name__ == "int":
            Default = """to_signed({src}, {BitWidth})""".format(
                src=obj.DefaultValue,
                BitWidth=obj.BitWidth
            )
            return Default

        if issubclass(type(obj.DefaultValue), HDPython_base0) and get_type(obj.DefaultValue):
            default1 = "to_signed("+ str(obj.DefaultValue)   + ", "+str(obj.Bitwidth_raw) +")"
            return default1
            


        return obj.DefaultValue

add_primitive_hdl_converter(v_signed_converter.primitive_type, v_signed_converter)
