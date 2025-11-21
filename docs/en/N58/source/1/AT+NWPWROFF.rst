.. _cmd-at+nwpwroff:

AT+NWPWROFF：Module Power Off Command
----------------------------------------

Module power off command. Before sending AT+NWPWROFF, the POWERKEY pin level of the module must be suspended or pulled high. After returning OK, if a reboot is needed, the POWERKEY pin level can be pulled low.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+NWPWROFF

**响应：**

::

    <CR><LF>OK<CR><LF>

参数
^^^^
- **<service>**： 短信服务模式选择
- 0：GSM03.40/GSM03.41 Phase 2
- 1：GSM03.40/GSM03.41 Phase 2+
- **<mt>,<mo>,<bm>**： 下行/上行/广播支持
- 0：不支持
- 1：支持
命令示例
^^^^^^^^
::

    AT+NWPWROFF
    
    OK

说明
^^^^
Example 28
