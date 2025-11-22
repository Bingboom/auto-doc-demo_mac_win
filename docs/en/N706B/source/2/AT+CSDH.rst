.. _cmd-at+csdh:

AT+CSDH：Display Text Mode Parameters
----------------------------------------

Set whether to display detailed header information in the result code in text mode. This command is valid in SMS text mode and requires sending AT+CMGF=1 to set to text mode.
Command Format

Command Format
^^^^^^^^








**Execute Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+CSDH

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


    AT+CSDH
    
    OK



Notes
^^^^^^^^
See Example 44
