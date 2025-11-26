


.. _cmd-at+xgauth:

AT+XGAUTH：User Authentication
---------------------------------

PDP authentication.
This command should be placed after the AT+CGDCONT command. Currently, there is a growing demand for user identity authentication in various places within private networks, using the internal protocol stack, this command needs to be used, so please add this command in the code flow.
The default username and password for Unicom cards are "card" and "card".
<cid> corresponds to <cid> in +CGDCONT.
The maximum string length allowed for <name> and <pwd> is 50.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+XGAUTH

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

    AT+XGAUTH
    
    OK




Notes
^^^^^^^^
Example 21
