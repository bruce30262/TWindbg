# TWindbg
PEDA-like debugger UI for WinDbg

![context img](/img/context.PNG?raw=true)

# Introduction
This is a windbg extension ( using [pykd](https://pykd.codeplex.com/) ) to let user having a [PEDA-like](https://github.com/longld/peda) debugger UI in WinDbg.  
It will display the following context in each step/trace:  
- Registers
- Disassembled code near PC
- Contents of the stack pointer ( with basic smart dereference )  

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



# Note
Maybe ( just maybe ) I'll add some command to make WinDbg behave more like PEDA ( or other debugger like pwndbg, GEF... ) in the future.
