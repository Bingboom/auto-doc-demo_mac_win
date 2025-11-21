.. _cmd-at+nstgetrssi:

AT+NSTGETRSSI：Get Receive Power of the Module in Strong Receive Mode (For Testing Only)
-------------------------------------------------------------------------------------------

Used to verify the module's receive power in test mode, strong receive test accuracy will have some errors.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+NSTGETRSSI

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

    AT+NSTGETRSSI
    
    OK

说明
^^^^
Example 30
