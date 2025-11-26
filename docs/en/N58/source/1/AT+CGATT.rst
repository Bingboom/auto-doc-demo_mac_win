


.. _cmd-at+cgatt:

AT+CGATT：Set GPRS Attach and Detach
---------------------------------------

This command is used to query and set GPRS attach and detach. It does not persist after power off.
By default, the module actively performs GPRS attach.
Before establishing a PPP connection, ensure that GPRS is in the attached state. Add the query command AT+CGATT?:
If the return value is 1, you can directly proceed with the PPP connection; if the return value is 0, manual attachment is required, i.e., AT+CGATT=1.
Command Format

Command Format
^^^^^^^^








**Execute Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+CGATT

**Response：**
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


    AT+CGATT
    
    OK



Notes
^^^^^^^^
Example 22
