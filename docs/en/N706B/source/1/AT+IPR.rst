


.. _cmd-at+ipr:

AT+IPR：Set Module Baud Rate
-------------------------------

Set the module baud rate, saved by default when powered off.
If the baud rate query returns 0, it indicates that the module baud rate is adaptive. The default is adaptive baud rate (Note: adaptive baud rate does not exceed 115200).
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+IPR

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

    AT+IPR
    
    OK




Notes
^^^^^^^^
Example 13
