[![Python 2.7](https://img.shields.io/badge/Python-2.7-green.svg)](https://github.com/bruce30262/TWindbg/)
[![Code Climate](https://codeclimate.com/github/bruce30262/TWindbg/badges/gpa.svg)](https://codeclimate.com/github/bruce30262/TWindbg)
[![Issue Count](https://codeclimate.com/github/bruce30262/TWindbg/badges/issue_count.svg)](https://codeclimate.com/github/bruce30262/TWindbg)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://choosealicense.com/licenses/mit/)


# TWindbg
PEDA-like debugger UI for WinDbg

![context img](/img/context.PNG?raw=true)

# Introduction
This is a windbg extension ( using [pykd](https://pykd.codeplex.com/) ) to let user having a [PEDA-like](https://github.com/longld/peda) debugger UI in WinDbg.  
It will display the following context in each step/trace:  
- Registers
- Disassembled code near PC
- Contents of the stack pointer ( with basic smart dereference )  

It also supports some peda-like commands ( see the [support commands](#support-commands) section )

For now it supports both x86 & x64 WinDbg.

# Dependencies
* Python2.7 ( The extension has NOT been tested on Python3 )
* [pykd](https://pykd.codeplex.com/)

# Installation
* Install Python2.7 & pykd
* Download the repository
* Install the matrix theme by double-clicking the [matrix_theme.reg](/matrix_theme.reg)
  - The matrix theme is required for letting the [color theme](/TWindbg/color.py) work in TWindbg
  - You can preview the theme by importing the [matrix_theme.WEW](/matrix_theme.WEW) workspace into WinDbg.
* Copy the [TWindbg](/TWindbg) folder into `[WinDbg Directory]\x64\winext\` & `[WinDbg Directory]\x86\winext\`

# Usage
## Launch TWindbg manually
* Open an executable or attach to a process with WinDbg
* Use `.load pykd.pyd` to load the `pykd` extension
* Use `!py -g winext\TWindbg\TWindbg.py` to launch TWindbg

## Launch TWindbg with command
```
[PATH_TO_WINDBG] -a pykd.pyd -c "!py -g winext\TWindbg\TWindbg.py"
```
Or you can write a [simple batch file](/batch/TWindbg_x64.bat) for the sake of convenience.

After that you can just use `t` or `p` to see if the extension is working.

# Support Commands
* `TWindbg`: List all the command in TWindbg
* `ctx`: Print out the current context
* `tel / telescope`: Display memory content at an address with smart dereferences
![tel img](/img/tel.PNG?raw=true)

# Note
Maybe ( just maybe ) I'll add more command to make WinDbg behave more like PEDA ( or other debugger like pwndbg, GEF... ) in the future.
