.. _cmd-at+gsn:

AT+GSN：Get Communication Module IMEI Number
-----------------------------------------------

Obtain the product serial number of the module, which is the IMEI number (International Mobile Equipment Identity).
Command Syntax

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+GSN

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

    AT+GSN
    
    OK

说明
^^^^
See Example 9
