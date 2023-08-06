import HDPython.ast.ast_classes.ast_base as ast_base
import HDPython.ast.ast_classes.ast_slice as slice
import HDPython.ast.ast_classes.ast_for as v_for
import HDPython.ast.ast_classes.ast_yield as ast_yiel
import HDPython.ast.ast_classes.ast_return as ast_return
import HDPython.ast.ast_classes.ast_if as ast_if
import HDPython.ast.ast_classes.ast_compare as ast_compare
import HDPython.ast.ast_classes.ast_Attribute as ast_Attribute
import HDPython.ast.ast_classes.ast_op_bool as ast_op_bool
import HDPython.ast.ast_classes.ast_op_bit_or as ast_op_bit_or
import HDPython.ast.ast_classes.ast_op_multi as ast_op_multi
import HDPython.ast.ast_classes.ast_op_bit_and as ast_op_bit_and
import HDPython.ast.ast_classes.ast_op_add as ast_op_add
import HDPython.ast.ast_classes.ast_op_not as ast_op_not
import HDPython.ast.ast_classes.ast_op_unitarty_sub as ast_op_unitarty_sub
import HDPython.ast.ast_classes.ast_function_architeture
import HDPython.ast.ast_classes.ast_function_porcess_combinational
import HDPython.ast.ast_classes.ast_function_porcess_timed
import HDPython.ast.ast_classes.ast_function_process
import HDPython.ast.ast_classes.ast_function_process_body
import HDPython.ast.ast_classes.ast_FunctionDef
import HDPython.ast.ast_classes.ast_switch
import HDPython.ast.ast_classes.ast_continue
import HDPython.ast.ast_classes.ast_op_sub
import HDPython.ast.ast_classes.ast_Num
import HDPython.ast.ast_classes.ast_op
import HDPython.ast.ast_classes.ast_assignment
import HDPython.ast.ast_classes.ast_op_stream_out
import HDPython.ast.ast_classes.ast_op_stream_in
import HDPython.ast.ast_classes.ast_subscript
import HDPython.ast.ast_classes.ast_function_call
import HDPython.ast.ast_classes.ast_name
import HDPython.ast.ast_classes.ast_expr
import HDPython.ast.ast_classes.ast_constant
import HDPython.ast.ast_classes.ast_list
import HDPython.ast.ast_classes.ast_op_unary


g_ast_class_register  = ast_base.g_ast_class_register
g_ast_function_call  = ast_base.g_ast_function_call
Node_line_col_2_str  = ast_base.Node_line_col_2_str
