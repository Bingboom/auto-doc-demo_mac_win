


.. _cmd-at+cmgl:

AT+CMGL：Message List
------------------------

Read a certain type of stored SMS, the messages will be read from the current storage selected by the +CPMS command.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+CMGL

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

    AT+CMGL
    
    OK




Notes
^^^^^^^^
See Example 37
