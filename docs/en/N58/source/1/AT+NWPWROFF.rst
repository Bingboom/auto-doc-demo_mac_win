


.. _cmd-at+nwpwroff:

AT+NWPWROFF：Module Power Off Command
----------------------------------------

Module power off command. Before sending AT+NWPWROFF, the POWERKEY pin level of the module must be suspended or pulled high. After returning OK, if a reboot is needed, the POWERKEY pin level can be pulled low.
Command Format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+NWPWROFF

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

    AT+NWPWROFF
    
    OK




Notes
^^^^^^^^
Example 28
