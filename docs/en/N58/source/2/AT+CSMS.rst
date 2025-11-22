.. _cmd-at+csms:

AT+CSMS：Select SMS Service
------------------------------

Supported short messages include: sending (SMS-MO), receiving (SMS-MT), cell broadcast (SMS-CB).

Command Format
^^^^^^^^








**Execute Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+CSMS=<service><CR>

**Response：**
::


    <CR><LF>+CSMS: <mt>,<mo>,<bm>
    <CR><LF>OK<CR><LF>
    Or
    <CR><LF>ERROR<CR><LF>,<CR><LF>+CSMS: <service>,<mt>,<mo>,<bm>
    <CR><LF>OK<CR><LF>,<CR><LF>+CSMS: (list of supported <service>s)
    <CR><LF>OK<CR><LF>





**Query Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+CSMS?<CR>

**Response：**
::


    OK





**Test Command**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Command：**
::

    AT+CSMS=?<CR>

**Response：**
::


    OK




Parameters
^^^^^^^^


- **<service>**： SMS service mode selection

  - 0：GSM03.40/GSM03.41 Phase 2

  - 1：GSM03.40/GSM03.41 Phase 2+


- **<mt>,<mo>,<bm>**： Downlink/Uplink/Broadcast support

  - 0：Not supported

  - 1：Supported




Examples
^^^^^^^^


  
    
  

  

  



::


    AT+CSMS=1
    
    +CSMS: 1,1,1
    OK
    AT+CSMS=2
    
    ERROR
    AT+CSMS?
    
    +CSMS: 1,1,1,1
    OK
    AT+CSMS=?
    
    +CSMS: (0,1)
    OK



Notes
^^^^^^^^
Supports multiple short message service types
