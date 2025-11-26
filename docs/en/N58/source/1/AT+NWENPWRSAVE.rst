


.. _cmd-at+nwenpwrsave:

AT+NWENPWRSAVE：Sleep Setting
--------------------------------

Set whether to allow the module to enter sleep mode. This command does not save settings after power off.
The module DTR signal is low by default:
After sending the command to allow entering sleep mode, and the module DTR signal is low (or high), all circuits of the module must be allowed to enter sleep state for the module to enter sleep.
Command format

Command Format
^^^^^^^^







**Execute Command**

Command：
::

    AT+NWENPWRSAVE

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

    AT+NWENPWRSAVE
    
    OK




Notes
^^^^^^^^
See Example 27
