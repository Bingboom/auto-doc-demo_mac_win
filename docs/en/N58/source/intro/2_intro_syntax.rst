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

Command Types
----------------

.. csv-table::
   :header: "Type", "Command Syntax", "Response Syntax", "Description"
   :widths: 20, 25, 25, 30

   "Set", "AT+CMD=<VALUE><CR>", "OK or ERROR", "Write parameter"
   "Execute", "AT+CMD[=<VALUE>]<CR>", "response + OK", "Perform internal action"
   "Test", "AT+CMD=?<CR>", "response + OK", "Return available parameter list"
   "Query", "AT+CMD?<CR>", "response + OK", "Return current stored value"
   "URC", "<CR><LF>+CMD:<VALUE><CR><LF>", "N/A", "Unsolicited report from module"

Command Response Time
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


