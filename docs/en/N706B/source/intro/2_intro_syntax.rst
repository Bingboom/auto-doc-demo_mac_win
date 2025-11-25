AT Syntax
=============================

Definition
-------------

- **<CR>**: Carriage return  
- **<LF>**: Line feed  
- **<..>**: Parameter name; angle brackets are *not* preserved in the actual AT command  
- **[..]**: Optional parameter; square brackets are *not* preserved in the actual AT command  
- **(space)**: Space character  

Syntax Description
---------------------

**Prefix Description:**  
"AT" or "at" is used as the command prefix. The module recognizes only these forms as valid AT commands.

**Command Fields:**

- **Standard Commands**: Defined by 3GPP TS 27007, 27005 or ITU-T Recommendation V.250  
- **Proprietary Commands**: Neoway-extended command set

**Connector Description:**  
“+” and “$” are used as the connector between the prefix and the command field.  
See each command section for detailed behavior.

**Termination Character:**  
By default, **<CR>** is used as the termination character for every AT command (value: **0x0D**).

**Command Response Syntax:**

.. code-block::

   <CR><LF>response<CR><LF>

The response field may contain multiple lines/messages depending on the command.

**Command Result Syntax:**

::

   <CR><LF>OK<CR><LF>
   <CR><LF>ERROR<CR><LF>

**OK** indicates successful execution, while **ERROR** indicates failure.

3. Command Types
----------------

.. csv-table::
   :header: "Type", "Command Syntax", "Response Syntax", "Description"
   :widths: 20, 25, 25, 30

   "Set", "AT+CMD=<VALUE><CR>", "OK or ERROR", "Write parameter"
   "Execute", "AT+CMD[=<VALUE>]<CR>", "response + OK", "Perform internal action"
   "Test", "AT+CMD=?<CR>", "response + OK", "Return available parameter list"
   "Query", "AT+CMD?<CR>", "response + OK", "Return current stored value"
   "URC", "<CR><LF>+CMD:<VALUE><CR><LF>", "N/A", "Unsolicited report from module"

4. Command Response Time
------------------------

After receiving an AT command, the module requires some time to process it internally.  
The response duration depends on the type of command.

For commands involving simple parameter operations (read/write), the module typically responds immediately,  
with a default maximum response time of **300 ms**.

Commands involving SIM/USIM card operations, network interactions, or peripheral control may take several seconds  
to tens of seconds. The actual duration depends on:

- SIM/USIM card content (e.g., number of contacts or SMS stored)  
- Network quality, signal strength, and congestion  
- Peripheral device type and operating state  




The table below lists typical response times for selected commands.  
Commands not listed usually have a maximum response time of approximately **300 ms**.

.. list-table::
   :header-rows: 1
   :widths: 15 45 20
   :align: center

   * - No.
     - Command
     - Timeout (s)


   * - 1
     - AT+COPS
     - 180

   * - 2
     - AT+CLCK
     - 15

   * - 3
     - ATD*99#
     - 30

   * - 4
     - AT+CMGR
     - 30

   * - 5
     - AT+CMGL
     - 30

   * - 6
     - AT+CMGS
     - 30

   * - 7
     - AT+XIIC
     - 60

   * - 8
     - AT+TCPSETUP
     - 60

   * - 9
     - AT+TCPSEND
     - 30

   * - 10
     - AT+TCPCLOSE
     - 5

   * - 11
     - AT+UDPSETUP
     - 30

   * - 12
     - AT+UDPSEND
     - 30

   * - 13
     - AT+TCPLISTENMODE
     - 30

   * - 14
     - AT+TCPLISTEN
     - 30

   * - 15
     - AT+CLOSELISTEN
     - 5

   * - 16
     - AT+CLOSECLIENT
     - 5

   * - 17
     - AT+TCPREADS
     - 30

   * - 18
     - AT+TCPSENDS
     - 30

   * - 19
     - AT+CLIENTSTATUS
     - 30

   * - 20
     - AT+TCPACKS
     - 30

   * - 21
     - AT+TCPTRANS
     - 60

   * - 22
     - AT+FTPLOGIN
     - 30

   * - 23
     - AT+FTPLOGOUT
     - 30

   * - 24
     - AT+FTPGET
     - 30

   * - 25
     - AT+FTPPUT
     - 30

   * - 26
     - AT+FTPSIZE
     - 30

   * - 27
     - AT+HTTPSETUP
     - 60

   * - 28
     - AT+HTTPACTION
     - 60

