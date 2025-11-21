.. _cmd-at+cmss:

AT+CMSS：Send Saved Short Message
------------------------------------

Send the short message (SMS-SUBMIT) located at the position specified by <index> in the memory. After the short message is successfully sent, the network returns the reference value <mr> to the terminal.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CMSS

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

    AT+CMSS
    
    OK

说明
^^^^
Example 40
