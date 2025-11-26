


.. _cmd-at+cmgw:

AT+CMGW：Write Short Message
-------------------------------

Write a short message to the storage, after successful storage, return the location information <index>.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+CMGW

Response：
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

    AT+CMGW
    
    OK




Notes
^^^^^^^^
See Example 39
