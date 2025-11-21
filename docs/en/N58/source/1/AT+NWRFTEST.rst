.. _cmd-at+nwrftest:

AT+NWRFTEST：Module Strong Transmit and Receive Command (For Testing Only)
-----------------------------------------------------------------------------

Used to verify the module's strong transmit and receive capabilities in test mode, only testing the transmit power and receive power accuracy at the center frequency of each frequency band. Due to platform limitations, there are some errors in the accuracy of strong receive and transmit tests.
Strong transmit testing can only verify maximum transmit power of 23dB and 10dB, other values cannot be verified.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+NWRFTEST

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

    AT+NWRFTEST
    
    OK

说明
^^^^
Example 29
