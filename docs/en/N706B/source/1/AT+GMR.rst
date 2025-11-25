.. _cmd-at+gmr:

AT+GMR：Query Version Information
------------------------------------

Query software version information.
Command Format

Command Format
^^^^^^^^








**Execute Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+GMR

**Response：**
::


    <CR><LF>OK<CR><LF>




Parameters
^^^^^^^^


- **<service>**： 短信服务模式选择

  - 0：GSM03.40/GSM03.41 Phase 2

  - 1：GSM03.40/GSM03.41 Phase 2+


- **<mt>,<mo>,<bm>**： 下行/上行/广播支持

  - 0：不支持

  - 1：支持




Examples
^^^^^^^^


  
    
  



::


    AT+CSMS=1
    
    +CSMS: 1,1,1
    OK



Notes
^^^^^^^^
Example 2
