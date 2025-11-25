


.. _cmd-at+cmgr:

AT+CMGR：Read Short Message
------------------------------

Read the short message in the current storage (must be set in advance using the AT+CPMS command).
If the status of the received SMS is unread, executing this command will change the SMS storage status to read.
Command Format

Command Format
^^^^^^^^








**Execute Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+CMGR

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


    AT+CMGR
    
    OK



Notes
^^^^^^^^
Example 36
