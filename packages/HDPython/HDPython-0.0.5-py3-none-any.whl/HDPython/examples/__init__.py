from HDPython.examples.axiStream import axisStream , axisStream_slave,axisStream_master
#import HDPython.examples.axiStream as ax
from HDPython.examples import clk_generator as clk_gen 
from HDPython.examples import counter   as cntr
from HDPython.examples import edgeDetection  as e_detection
from HDPython.examples import inputDelayTest  as iDelay
from HDPython.examples import ram_handle  as ram_h
from HDPython.examples import rollingCounter as r_counter
from HDPython.examples import system_globals  as sys_globals
from HDPython.examples import axi_stream_delay  as ax_s_delay
from HDPython.examples import optional_t as opt_t
from HDPython.examples import small_buffer as sb

from HDPython.examples import axi_fifo as ax_fifo

from HDPython.examples import axiPrint as axiPrint




## HDPython.examples.clk_generator
clk_generator  = clk_gen.clk_generator

## HDPython.examples.counter
time_span   = cntr.time_span
counter     = cntr.counter

## edgeDetection
edgeDetection  = e_detection.edgeDetection

## inputDelayTest
InputDelay_tb = iDelay.InputDelay_tb

## ram_handle
ram_handle = ram_h.ram_handle
ram_handle_master = ram_h.ram_handle_master

##  rollingCounter
rollingCounter = r_counter.rollingCounter


## system_globals
system_globals        = sys_globals.system_globals
register_t            = sys_globals.register_t
system_globals_delay  = sys_globals.system_globals_delay
register_handler      = sys_globals.register_handler
register_storage      = sys_globals.register_storage

stream_delay = ax_s_delay.stream_delay
stream_delay_one = ax_s_delay.stream_delay_one


#optional_t
optional_t = opt_t.optional_t


small_buffer = sb.small_buffer

axiFifo = ax_fifo.axiFifo

axiPrint = axiPrint.axiPrint