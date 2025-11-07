.. _cmd-at+csms:

AT+CSMS：选择短信服务
---------------

用于支持的短消息包括：发送（SMS-MO）、接收（SMS-MT）、小区广播（SMS-CB）。

命令格式
^^^^^^^^




**执行命令**
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






**查询命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CSMS?<CR>

**响应：**

::


    <CR><LF>+CSMS: <mt>,<mo>,<bm>
    <CR><LF>OK<CR><LF>
    Or
    <CR><LF>ERROR<CR><LF>,<CR><LF>+CSMS: <service>,<mt>,<mo>,<bm>
    <CR><LF>OK<CR><LF>,<CR><LF>+CSMS: (list of supported <service>s)
    <CR><LF>OK<CR><LF>






**测试命令**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    AT+CSMS=?<CR>

**响应：**

::


    <CR><LF>+CSMS: <mt>,<mo>,<bm>
    <CR><LF>OK<CR><LF>
    Or
    <CR><LF>ERROR<CR><LF>,<CR><LF>+CSMS: <service>,<mt>,<mo>,<bm>
    <CR><LF>OK<CR><LF>,<CR><LF>+CSMS: (list of supported <service>s)
    <CR><LF>OK<CR><LF>





参数
^^^^


- **<service>**：
  
    短信服务模式选择


- **<mt>,<mo>,<bm>**：
  
    下行/上行/广播支持




说明
^^^^
支持多种短消息服务类型

示例命令
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
