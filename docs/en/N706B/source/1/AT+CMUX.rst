.. _cmd-at+cmux:

AT+CMUX：Serial Port Multiplexing Command
--------------------------------------------

Enable the communication module's serial port multiplexing function.
Based on a physical communication serial port, virtualize two or even more serial ports through a standardized protocol, generally virtualizing three serial ports, one for external protocol stack dial-up internet access, and the other two for sending and receiving AT commands. It is recommended to use AT+CMUX=0 to enable the serial port multiplexing function.
Command Format

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CMUX

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

    AT+CMUX
    
    OK

说明
^^^^
Example 15
