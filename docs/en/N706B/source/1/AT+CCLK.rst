.. _cmd-at+cclk:

AT+CCLK：Clock Management
----------------------------

Set and query the module's real-time clock.
The set time takes effect immediately, is saved during power off, and the default clock is in the 0 timezone, using 1/4 timezone.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CCLK

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

    AT+CCLK
    
    OK

说明
^^^^
Example 16
