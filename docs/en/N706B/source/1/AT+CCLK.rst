


.. _cmd-at+cclk:

AT+CCLK：Clock Management
----------------------------

Set and query the module's real-time clock.
The set time takes effect immediately, is saved during power off, and the default clock is in the 0 timezone, using 1/4 timezone.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+CCLK

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

    AT+CCLK
    
    OK




Notes
^^^^^^^^
Example 16
