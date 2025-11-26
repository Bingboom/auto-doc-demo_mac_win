


.. _cmd-at+cpin:

AT+CPIN：Input PIN Code
--------------------------

Query the PIN status and input the PIN code.
To input the PIN code, the current SIM card must be locked (AT+CLCK="SC",1,"1234") and the module must be restarted to input the PIN code. After three incorrect PIN entries, a PUK code will be required to unlock.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+CPIN

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

    AT+CPIN
    
    OK




Notes
^^^^^^^^
Example 17
