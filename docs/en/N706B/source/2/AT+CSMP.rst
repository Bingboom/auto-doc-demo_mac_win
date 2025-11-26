


.. _cmd-at+csmp:

AT+CSMP：Set Text Mode Parameters
------------------------------------

In text mode, select the required values for additional parameters, set the validity period starting from when the message is received from the SMSC, or define the absolute time that terminates the validity period.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+CSMP

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

    AT+CSMP
    
    OK




Notes
^^^^^^^^
See Example 43
