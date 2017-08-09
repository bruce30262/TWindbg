# -*- coding: utf-8 -*- 

import pykd
import color
import sys
import traceback
import command
import context

context.init_arch()
context.init_context_handler()
command.set_aliases()

context.context_handler.print_context()

if len(sys.argv) >= 2: # user input TWindbg command
    cmd = sys.argv[1]
    if hasattr(command, cmd): # if the command mudule has the corresponded method, call it 
        getattr(command, cmd)()