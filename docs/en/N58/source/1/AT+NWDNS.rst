.. _cmd-at+nwdns:

AT+NWDNS：Domain Name Resolution
-----------------------------------

After dialing with the built-in protocol stack, query the DNS resolution result.
This command can only be executed after successfully dialing with AT+XIIC command.
The domain name is not validated for correctness; ensure the correctness of the input content.
Command format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+NWDNS

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

    AT+NWDNS
    
    OK

说明
^^^^
See Example 26
