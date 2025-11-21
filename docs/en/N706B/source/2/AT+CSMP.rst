.. _cmd-at+csmp:

AT+CSMP：Set Text Mode Parameters
------------------------------------

In text mode, select the required values for additional parameters, set the validity period starting from when the message is received from the SMSC, or define the absolute time that terminates the validity period.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CSMP

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

    AT+CSMP
    
    OK

说明
^^^^
See Example 43
