.. _cmd-at+csms:

AT+CSMS：Select SMS Service
------------------------------

Supported short messages include: sending (SMS-MO), receiving (SMS-MT), cell broadcast (SMS-CB).

命令格式
^^^^^^^^
**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CSMS=<service><CR>

**响应：**

::

    <CR><LF>+CSMS: <mt>,<mo>,<bm>
    <CR><LF>OK<CR><LF>
    Or
    <CR><LF>ERROR<CR><LF>,<CR><LF>+CSMS: <service>,<mt>,<mo>,<bm>
    <CR><LF>OK<CR><LF>,<CR><LF>+CSMS: (list of supported <service>s)
    <CR><LF>OK<CR><LF>

**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CSMS?<CR>

**响应：**

::

    OK

**命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CSMS=?<CR>

**响应：**

::

    OK

参数
^^^^
- **<service>**： SMS service mode selection
- 0：GSM03.40/GSM03.41 Phase 2
- 1：GSM03.40/GSM03.41 Phase 2+
- **<mt>,<mo>,<bm>**： Downlink/Uplink/Broadcast support
- 0：Not supported
- 1：Supported
命令示例
^^^^^^^^
::

    AT+CSMS=1
    
    +CSMS: 1,1,1
    OK
    AT+CSMS=2
    
    ERROR
    AT+CSMS?
    
    +CSMS: 1,1,1,1
    OK
    AT+CSMS=?
    
    +CSMS: (0,1)
    OK

说明
^^^^
Supports multiple short message service types
