.. _cmd-at+csdh:

AT+CSDH：Display Text Mode Parameters
----------------------------------------

Set whether to display detailed header information in the result code in text mode. This command is valid in SMS text mode and requires sending AT+CMGF=1 to set to text mode.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CSDH

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

    AT+CSDH
    
    OK

说明
^^^^
See Example 44
