.. _cmd-at+cpin:

AT+CPIN：Input PIN Code
--------------------------

Query the PIN status and input the PIN code.
To input the PIN code, the current SIM card must be locked (AT+CLCK="SC",1,"1234") and the module must be restarted to input the PIN code. After three incorrect PIN entries, a PUK code will be required to unlock.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CPIN

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

    AT+CPIN
    
    OK

说明
^^^^
Example 17
