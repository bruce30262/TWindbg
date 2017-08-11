# -*- coding: utf-8 -*- 

import pykd
import color
import sys
import command_handler
import context

# Init arch & context handler
context.init_arch()
context.init_context_handler()
# TWindbg command wrapper
command_handler.wrap_all_commands()
# Print out the current context
context.context_handler.print_context()
