

from enum import Enum 
import copy
import  inspect 
from HDPython.base import *
import HDPython.core_pack_generator as core_gen
import HDPython.debug_vis as debug_vis
from HDPython.ast.AST_MemFunctionCalls import memFunctionCall
from  HDPython.base_helpers import *
from  HDPython.lib_enums import *
from HDPython.global_settings import *
import  functools 
import  HDPython.hdl_converter as  hdl

from HDPython.type_info import typeInfo

from typing import Sequence, TypeVar
T = TypeVar('T', bound='Copyable')

from HDPython.primitive_type_converter  import add_primitive_hdl_converter

class hdl_converter_base:
    __VHDL__OPS_to2str= {
        "Gt": ">",
        "Eq" : "=",
        "GtE" :">=",
        "LtE" :"<=",
        "Lt"  :"<"
    }

    get_dependency_objects_index = 0

    

    def __init__(self):
        self.MemfunctionCalls=[]
        self.IsConverted = False
        self.MissingTemplate = False
        self.extractedTypes = []






    def get_dependency_objects(self, obj, dep_list):
        self.get_dependency_objects_index += 1
        if self.get_dependency_objects_index > 10:
            self.get_dependency_objects_index -= 1
            return []

        dep_list += [getattr(obj, x[0]) for x in obj.__dict__.items() if issubclass(type(getattr(obj, x[0])),HDPython_base) and getattr(obj, x[0])._issubclass_("v_class")]

        
        for x in hdl.get_MemfunctionCalls(obj):
            dep_list += x.args

        dep_list = flatten_list(dep_list)
        ret     = remove_duplications(dep_list)
        ret     = remove_duplications_types(ret)
        old_length = 0
        newLength = len(ret)
        while newLength > old_length:
            old_length = newLength
            ret1 = []
            for x in ret:
                if x is obj:
                    continue
                if x is None:
                    continue
                if isInList_type(ret1, x):
                    continue
                ret1.append(hdl.get_dependency_objects(x,ret))
            
            ret1.append(obj)
            ret1 = flatten_list(ret1)
            ret1 = remove_duplications(ret1)
            ret1 = remove_duplications_types(ret1)
            ret = ret1
            newLength = len(ret)
        
        self.get_dependency_objects_index -= 1
        return ret
        
    def ops2str(self, ops):
        return  self.__VHDL__OPS_to2str[ops]

    def get_MemfunctionCalls(self,obj):
        primary = hdl.get_primary_object(obj)
        return primary.__hdl_converter__.MemfunctionCalls
    

    def FlagFor_TemplateMissing(self, obj):
        obj.__hdl_converter__.MissingTemplate  = True
        primary = hdl.get_primary_object(obj)
        primary.__hdl_converter__.MissingTemplate  = True

    def reset_TemplateMissing(self, obj):
        primary = hdl.get_primary_object(obj)
        primary.__hdl_converter__.MissingTemplate  = False  

    def isTemplateMissing(self,obj):
        primary = hdl.get_primary_object(obj)
        return primary.__hdl_converter__.MissingTemplate  

    def IsSucessfullConverted(self,obj):
        if hdl.isTemplateMissing(obj):
            return False
        return self.IsConverted

    def prepare_for_conversion(self,obj):
        for m in obj.__dict__:
            if not issubclass(type(m),HDPython_base0):
                continue 
            hdl.prepare_for_conversion(m)


    def convert_all_packages(self, obj, ouputFolder,x,FilesDone):
        if x.__abstract_type_info__.vetoHDLConversion:
            return 

        packetName =  hdl.get_packet_file_name(x)
        if packetName not in FilesDone:
            print_cnvt(str(gTemplateIndent)+ '<package_conversion name="'+type(x).__name__ +'">')
            gTemplateIndent.inc()
            hdl.prepare_for_conversion(x)
            hdl.reset_TemplateMissing(x)
            packet = hdl.get_packet_file_content(x)
            if packet and not (x.__hdl_converter__.MissingTemplate and not saveUnfinishedFiles()):
                file_set_content(ouputFolder+"/" +packetName,packet)
            FilesDone.append(packetName)
            if x.__hdl_converter__.MissingTemplate:
                print_cnvt(str(gTemplateIndent)+'<status ="failed">')
            else:
                print_cnvt(str(gTemplateIndent)+'<status ="sucess">')
            gTemplateIndent.deinc()
            print_cnvt(str(gTemplateIndent)+ '</package_conversion>')
        
    def convert_all_entities(self, obj, ouputFolder,x,FilesDone):
        entiyFileName =  hdl.get_entity_file_name(x)
        if entiyFileName not in FilesDone:
            print_cnvt(str(gTemplateIndent)+'<entity_conversion name="'+type(x).__name__ +'">')
            gTemplateIndent.inc()
            hdl.prepare_for_conversion(x)
            hdl.reset_TemplateMissing(x)
            try:
                entity_content = hdl.get_enity_file_content(x)
            except Exception as inst:
                raise Exception(["Error in entity Converion:\nEntityFileName: "+ entiyFileName], x,inst)
            if entity_content and not (x.__hdl_converter__.MissingTemplate and not saveUnfinishedFiles()):
                file_set_content(ouputFolder+"/" +entiyFileName,entity_content)
            FilesDone.append(entiyFileName)
            if x.__hdl_converter__.MissingTemplate:
                print_cnvt(str(gTemplateIndent)+'<status ="failed">')
            else:
                print_cnvt(str(gTemplateIndent)+'<status ="sucess">')
            gTemplateIndent.deinc()
            print_cnvt(str(gTemplateIndent)+"</entity_conversion>")
            #print_cnvt("processing")

    def convert_all_impl(self, obj, ouputFolder, FilesDone):
        FilesDone.clear()
        for x in gHDL_objectList:
            hdl.prepare_for_conversion(x)

        for x in gHDL_objectList:
            
            if hdl.IsSucessfullConverted(x):
                continue
            
            self.convert_all_packages(obj, ouputFolder,x,FilesDone)

            self.convert_all_entities(obj, ouputFolder,x,FilesDone)
            x.__hdl_converter__.IsConverted = True


    def convert_all(self, obj, ouputFolder):

        counter = 0
        
        FilesDone = ['']
        while len(FilesDone) > 0:
            counter += 1
            if counter > 10:
                raise Exception("unable to convert ")
           
            print_cnvt("<!--=======================-->")
            print_cnvt(str(gTemplateIndent)+ '<Converting Index="'+str(counter) +'">')
            gTemplateIndent.inc()
            self.convert_all_impl(obj, ouputFolder, FilesDone)
            gTemplateIndent.deinc()
            print_cnvt(str(gTemplateIndent)+ '</Converting>')

    def get_primary_object(self,obj):
        obj_packetName =  hdl.get_packet_file_name(obj)
        obj_entiyFileName =  hdl.get_entity_file_name(obj)
        i = 0 

        for x in gHDL_objectList_primary:
            if obj_packetName ==  x["packetName"] and obj_entiyFileName == x["entiyFileName"] and isinstance(obj, type(x["symbol"])): 
                return x["symbol"]

        for x in gHDL_objectList:
            i +=1 
            packetName =  hdl.get_packet_file_name(x)
            entiyFileName =  hdl.get_entity_file_name(x)
            if obj_packetName ==  packetName and obj_entiyFileName == entiyFileName and isinstance(obj, type(x)): 
                #print_cnvt(i)
                gHDL_objectList_primary.append({
                    "packetName"    : obj_packetName,
                    "entiyFileName" : obj_entiyFileName,
                    "symbol"            : x
                })
                return x

        gHDL_objectList.append(obj)

        gHDL_objectList_primary.append({
                    "packetName"    : obj_packetName,
                    "entiyFileName" : obj_entiyFileName,
                    "symbol"            : obj
        })
        return obj

    def get_packet_file_name(self, obj):
        return ""

    def get_packet_file_content(self, obj):
        return ""

    def get_enity_file_content(self, obj):
        return ""

    def get_entity_file_name(self, obj):
        return ""

    def get_type_simple(self,obj):
        return type(obj).__name__

    def get_type_simple_template(self,obj):
        return self.get_type_simple(obj)
        
    def impl_constructor(self,obj):
        return hdl.get_type_simple(obj)+"_ctr(" +value(obj)+")"

    def parse_file(self,obj):
        return ""

    def impl_includes(self,obj, name,parent):
        return self.def_includes(obj,name,parent)
        
    def def_includes(self,obj, name,parent):
        return ""

    def def_record_Member(self,obj, name,parent,Inout=None):
        return ""

    def def_record_Member_Default(self, obj,name,parent,Inout=None):
        return "" 

    def def_packet_header(self,obj, name,parent):
        return ""


    def def_packet_body(self,obj, name,parent):
        return ""

    def impl_entity_port(self, obj, name):
        ret =[]
        objName = str(obj)
        ret.append(name + " => " + objName)
        return  ret

    def impl_function_argument(self, obj,func_arg, arg):
        ret = []
        ys = hdl.extract_conversion_types(func_arg["symbol"])
        for y in ys:
            line = func_arg["name"] + y["suffix"]+ " => " + str(arg) + y["suffix"]
            ret.append(line)
            if y["symbol"]._varSigConst ==varSig.signal_t:
                members = y["symbol"].getMember()
                for m in members:
                    if m["symbol"].__writeRead__ == InOut_t.output_t or  m["symbol"].__writeRead__ == InOut_t.InOut_tt:
                        line = func_arg["name"] + y["suffix"]+"_"+ m["name"] +" => " + arg.__hdl_name__ + y["suffix"]  +"."+m["name"]
                        ret.append(line)
                        #print_cnvt(line)

        return ret

        
    def impl_get_attribute(self,obj, attName, parent = None):
        return str(obj) + "." +str(attName)

    def impl_slice(self,obj, sl,astParser=None):
        raise Exception("Not implemented")

    
    def impl_compare(self,obj, ops, rhs, astParser =None):
        return str(obj) + " " + hdl.ops2str(obj,ops)+" " + str(rhs)

    def impl_add(self,obj,args):
        return str(obj) + " + " + str(args)
    
    def impl_sub(self,obj,args):
        return str(obj) + " - " + str(args)

    def impl_multi(self,obj,args):
        return str(obj) + " * " + str(args)
        
    def impl_to_bool(self,obj, astParser):
        obj._add_input()
        astParser.add_read(obj)
        return "to_bool(" + str(obj) + ") "

    def impl_bit_and(self,obj,rhs,astParser):
        raise Exception("not Implemented")
        

    def function_name_modifier(self,obj,name, varSigSuffix):
        if name == "__bool__":
            return "to_bool"
        if name == "__len__":
            return "length"
        if name == "__lshift__":
            return "set_value" + varSigSuffix+"_lshift"
        if name == "__rshift__":
            return "get_value" + varSigSuffix+"_rshift"
        return name + varSigSuffix

    def impl_get_value(self,obj, ReturnToObj=None,astParser=None):

        astParser.add_read(obj)
        obj._add_input()
        return obj

    def impl_reasign_type(self, obj ):
        return obj

    def impl_reasign(self, obj, rhs, astParser=None,context_str=None):
        asOp = hdl.get_assiment_op(obj)    
        return str(obj) +asOp +  str(rhs)

    def impl_reasign_rshift_(self, obj, rhs, astParser=None,context_str=None):
        return hdl.impl_reasign(rhs, obj,astParser,context_str)

    def get_call_member_function(self, obj, name, args):
        args = [x.get_symbol() for x in args ]

 
        for x  in obj.__hdl_converter__.MemfunctionCalls:
            if x.name != name:
                continue
            if not x.isSameArgs(args):
                continue
            return x
 
        x =  memFunctionCall(
            name= name,
            args= args,
            obj= obj,
            call_func = None,
            func_args = None,
            setDefault = False,
            varSigIndependent = False
        )
        obj.__hdl_converter__.MemfunctionCalls.append(x)
        obj.IsConverted = False
        return x

    def impl_function_call(self, obj, name, args, astParser=None):
        
        primary = hdl.get_primary_object(obj)
        obj.__hdl_converter__ = primary.__hdl_converter__
        
        
        call_obj = hdl.get_call_member_function(obj, name, args)
        ret = call_obj.HDL_Call(astParser, args, obj)
        return ret




    

    def impl_symbol_instantiation(self,obj, VarSymb="variable"):
        print_cnvt("impl_symbol_instantiation is deprecated")
        return VarSymb +" " +str(obj) + " : " +obj._type +" := " + obj._type+"_null;\n"
        #return " -- No Generic symbol definition for object " + self.getName()

    def impl_architecture_header(self, obj):
        if obj._Inout != InOut_t.Internal_t:
            return ""
        
        if obj._varSigConst != varSig.signal_t or obj._varSigConst != varSig.signal_t:
            return ""

        VarSymb = get_varSig(obj._varSigConst)

        return VarSymb +" " +str(obj) + " : " +obj._type +" := " + obj._type+"_null;\n"
        
    def impl_architecture_body(self, obj):
        return ""


    def def_entity_port(self,obj):
        return ""


    def impl_process_sensitivity_list(self, obj):
        return []

    def impl_process_header(self,obj):
        if obj._Inout != InOut_t.Internal_t:
            return ""
        
        if obj._varSigConst != varSig.variable_t:
            return ""

        VarSymb = get_varSig(obj._varSigConst)

        return VarSymb +" " +str(obj) + " : " +obj._type +" := " + obj.DefaultValue +";\n"
    
    def impl_process_pull(self,obj,clk):
        return []

    def impl_process_push(self,obj,clk):
        return []

    def get_free_symbols(self,obj,name,parent_list=[]):
        return []



    def get_assiment_op(self, obj):
        varSigConst = obj._varSigConst
        raise_if(varSigConst== varSig.const_t, "cannot asign to constant")

        if varSigConst== varSig.signal_t:
            asOp = " <= "
        elif varSigConst== varSig.variable_t:
            asOp = " := "
        else: 
            asOp = " := "

        return asOp

    def get_Inout(self,obj,parent):
        inOut = obj._Inout
        if inOut == InOut_t.Default_t:
            return parent._Inout

        if parent._Inout == InOut_t.input_t or parent._Inout == InOut_t.Slave_t :
            inOut =InoutFlip(inOut)
        
        return inOut
        


    def InOut_t2str2(self, inOut):

        if inOut == InOut_t.input_t:
            return " in "
        
        if inOut == InOut_t.output_t:
            return " out "
        
        if inOut == InOut_t.InOut_tt:
            return " inout "
        
        return " in "

    def InOut_t2str3(self, obj, parent):
        inOut = obj._Inout
        if parent._Inout == InOut_t.input_t or parent._Inout == InOut_t.Slave_t :
            inOut =InoutFlip(inOut)

        if inOut == InOut_t.Default_t:
            inOut = parent._Inout 


        return self.InOut_t2str2(inOut)

    def InOut_t2str(self, obj):
        inOut = obj._Inout
        if inOut == InOut_t.input_t:
            return " in "
        
        if inOut == InOut_t.output_t:
            return " out "
        
        if inOut == InOut_t.InOut_tt:
            return " inout "
        
        inOut = obj.__writeRead__
        if inOut == InOut_t.input_t:
            return " in "
        
        if inOut == InOut_t.output_t:
            return " out "
        
        if inOut == InOut_t.InOut_tt:
            return " inout "
        
        raise Exception("unkown Inout type",inOut)

    def get_default_value(self,obj):
        return obj._type + "_null"


    def extract_conversion_types(self, obj, exclude_class_type=None,filter_inout=None):
        if filter_inout and obj._Inout != filter_inout: 
            return []
        return [{ "suffix":"", "symbol": obj}]

    def get_Name_array(self,obj):
        return hdl.get_type_simple(obj)+"_a"

    def length(self,obj):
        return "length(" +str(obj)+")"

    def to_arglist(self,obj, name,parent,withDefault = False,astParser=None):
        raise Exception("not implemented for class: ", type(obj).__name__)

    def get_inout_type_recursive(self, obj):
        if  obj._Inout != InOut_t.Internal_t:
            return obj._Inout
        return obj.__writeRead__  

    def Has_pushpull_function(self,obj, pushpull):
        return False
    
    def get_HDL_name(self, obj, parent,suffix):
        return str(parent.__hdl_name__) + suffix

add_primitive_hdl_converter("HDPython_base0",hdl_converter_base )
