.. _cmd-at+cscs:

AT+CSCS：Set TE Character Set
--------------------------------

Set the format of the TE character set.
Command Format

Command Format
^^^^^^^^








**Execute Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+CSCS

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


    AT+CSCS
    
    OK



Notes
^^^^^^^^
Example 34
