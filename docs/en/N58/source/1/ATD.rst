


.. _cmd-atd:

ATD：*99#: GPRS
------------------

Use an external protocol stack to perform GPRS dialing connection.
Before dialing, ensure that CREG has registered successfully and that the APN is set.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    ATD

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

    ATD
    
    OK




Notes
^^^^^^^^
Example 24
