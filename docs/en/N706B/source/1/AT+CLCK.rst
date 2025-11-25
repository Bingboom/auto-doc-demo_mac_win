


.. _cmd-at+clck:

AT+CLCK：PIN Enable and Query Function Command
-------------------------------------------------

Lock, unlock, and query MT and network devices. Set this parameter, and it will take effect after restarting the module.
Command Format

Command Format
^^^^^^^^








**Execute Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+CLCK

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


    AT+CLCK
    
    OK



Notes
^^^^^^^^
Example 18
