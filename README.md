[![Python 2&3](https://img.shields.io/badge/Python-2%20%26%203-green.svg)](https://github.com/bruce30262/TWindbg/)
[![Code Climate](https://codeclimate.com/github/bruce30262/TWindbg/badges/gpa.svg)](https://codeclimate.com/github/bruce30262/TWindbg)
[![Issue Count](https://codeclimate.com/github/bruce30262/TWindbg/badges/issue_count.svg)](https://codeclimate.com/github/bruce30262/TWindbg)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](http://choosealicense.com/licenses/mit/)


# TWindbg
PEDA-like debugger UI for WinDbg

![context img](/img/context.PNG?raw=true)

# Introduction
This is a windbg extension ( using [pykd](https://githomelab.ru/pykd/pykd) ) to let user having a [PEDA-like](https://github.com/longld/peda) debugger UI in WinDbg.  
It will display the following context in each step/trace:  
- Registers
- Disassembled code near PC
- Contents of the stack pointer ( with basic smart dereference )  

It also supports some peda-like commands ( see the [support commands](#support-commands) section )

For now it supports both x86 & x64 WinDbg.

# Dependencies
* Python 2/3  
> For now the extension is Python2/3 compatible.  
> However since now [Python2 has reached the EOL](https://www.python.org/doc/sunset-python-2/), all the feature will be tested on Python3 from now on.  
> I'll try my best to keep this extension as a Python2/3 compatible project, however there's still a possibility that I might drop the support of Python2 in the future.
* [pykd](https://githomelab.ru/pykd/pykd)

# Installation
* Install Python2/3  
* Install pykd  
    - Download [Pykd-Ext](https://githomelab.ru/pykd/pykd-ext/-/wikis/Downloads), unpack `pykd.dll` to the `[WinDbg Directory]\x86(or x64)\winext\` directory.  
        + This will allow you to run python in Windbg.  
    - In the Windbg command line, enter command `.load pykd` to load the pykd module.  
    - Enter `!pip install pykd` to install the pykd python package.  
        + Upgrade the pykd module with command `!pip install --upgrade pykd`.  
        + If something went wrong during the installation with `pip install`, try installing the wheel package instead of the one on PyPI. You can download the wheel package [here](https://githomelab.ru/pykd/pykd/-/wikis/All%20Releases).
* Download the repository
* Install the matrix theme by double-clicking the [matrix_theme.reg](/matrix_theme.reg)
  - The matrix theme is required for letting the [color theme](/TWindbg/color.py) work in TWindbg
  - You can preview the theme by importing the [matrix_theme.WEW](/matrix_theme.WEW) workspace into WinDbg.
* Copy the [TWindbg](/TWindbg) folder into `[WinDbg Directory]\x64\winext\` & `[WinDbg Directory]\x86\winext\`

# Usage
## Launch TWindbg manually
* Open an executable or attach to a process with WinDbg
* Use `.load pykd` to load the `pykd` extension
* Use `!py -g winext\TWindbg\TWindbg.py` to launch TWindbg

## Launch TWindbg with command
```
[PATH_TO_WINDBG] -a pykd -c "!py -g winext\TWindbg\TWindbg.py"
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
