


.. _cmd-ate1:

ATE1：/ATE0: Turn On & Off Echo
----------------------------------

Turn on (or off) the module's AT command echo function.
The module's default echo function is in the on state.
This setting does not persist after power off.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    ATE1

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

    ATE1
    
    OK




Notes
^^^^^^^^
Example 23
